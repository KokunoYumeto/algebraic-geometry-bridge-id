#!/usr/bin/env python3
"""Validate a lossless, zero-copy common-backend-v1 view of this lane.

The native ``ag-bridge-backend-record`` JSONL remains authoritative and is not
rewritten.  This adapter derives UUIDv5 common IDs, preserves every native
stable ID verbatim as ``stable_key``, and embeds the complete native record in
the primary common record's ``ag-bridge.native-record`` extension.  A reverse
replay must reproduce ``records.jsonl`` byte for byte before a receipt can be
emitted.

The target record stream is assembled twice in memory, validated against the
frozen v1 schema, and hashed; it is deliberately not materialized.  The only
normal outputs are the sanitized migration and terminology-QA receipts.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import mimetypes
import re
import sys
import uuid
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = ROOT / "backend" / "common-backend-v1-contract" / "upstream"
COMMON_SCHEMA_PATH = CONTRACT_DIR / "backend-v1.v0.41.0.schema.json"
PROFILE_SCHEMA_PATH = CONTRACT_DIR / "source-format-profile-v1.v0.41.0.schema.json"
RECEIPT_SCHEMA_PATH = CONTRACT_DIR / "backend-migration-receipt-v1.v0.42.0.schema.json"
HANDOFF_PATH = CONTRACT_DIR / "MIGRATION_HANDOFF_V1.v0.42.0.md"

EXPECTED_CONTRACT = {
    HANDOFF_PATH: (5320, "83de5379aa08f25fb3fb2774ed8bde99eca76e9a6ba80da9ccf2ee211e5e3a7a"),
    COMMON_SCHEMA_PATH: (126423, "3de8d107b1c75db0f8d60c42ef7e3488bc3fcc93f72e955def71a771475cf2b2"),
    PROFILE_SCHEMA_PATH: (12228, "2bb1429c36236329be94d58205b6123a0266a1e111277e3d303692ca8430e271"),
    RECEIPT_SCHEMA_PATH: (2563, "0147b14972dd562805b3b5f76fac453a9f32a6d298827d3f588316d4a8f5ffe0"),
}

IDENTITY_NAMESPACE = uuid.UUID("7790e70a-ae6d-5cf3-b7f5-c53d7d4c0fbd")
MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."
SCHEMA_NAME = "interlanguage-math-modular-backend"
SCHEMA_VERSION = "1.0.0"
UPSTREAM_HANDOFF_URL = (
    "https://github.com/KokunoYumeto/program-matematika-indonesia/"
    "blob/v0.42.0/backend/MIGRATION_HANDOFF_V1.md"
)
UPSTREAM_RECEIPT_SCHEMA_URL = (
    "https://github.com/KokunoYumeto/program-matematika-indonesia/"
    "blob/v0.42.0/schemas/backend-migration-receipt-v1.schema.json"
)
UPSTREAM_BACKEND_SCHEMA_URL = (
    "https://github.com/KokunoYumeto/program-matematika-indonesia/"
    "blob/v0.41.0/schemas/backend-v1.schema.json"
)
UPSTREAM_PROFILE_SCHEMA_URL = (
    "https://github.com/KokunoYumeto/program-matematika-indonesia/"
    "blob/v0.41.0/schemas/profiles/source-format-profile-v1.schema.json"
)

TABLES = (
    "accessibility",
    "aliases",
    "alignments",
    "artifact_members",
    "artifacts",
    "asset_revisions",
    "assets",
    "build_recipes",
    "concepts",
    "correction_bindings",
    "correction_claims",
    "corrections",
    "courses",
    "editions",
    "experiments",
    "file_revisions",
    "files",
    "interactives",
    "module_members",
    "modules",
    "occurrences",
    "placeholders",
    "programs",
    "qa_events",
    "relations",
    "release_snapshots",
    "resources",
    "rights",
    "rights_assignments",
    "rights_rule_members",
    "rights_rules",
    "route_members",
    "routes",
    "segment_variants",
    "segments",
    "term_variants",
    "terms",
    "units",
)

PRIMARY_TYPE = {
    "artifact": "artifact",
    "asset": "asset",
    "concept": "concept",
    "correction": "correction",
    "course": "course",
    "edition": "edition",
    "exercise": "unit",
    "program": "program",
    "qa_event": "qa_event",
    "relation": "relation",
    "resource": "resource",
    "rights": "rights",
    "segment": "segment",
    "solution": "unit",
    "term": "term",
    "unit": "unit",
}

TABLE_FOR_TYPE = {
    "accessibility": "accessibility",
    "alias": "aliases",
    "alignment": "alignments",
    "artifact_member": "artifact_members",
    "artifact": "artifacts",
    "asset_revision": "asset_revisions",
    "asset": "assets",
    "build_recipe": "build_recipes",
    "concept": "concepts",
    "correction_binding": "correction_bindings",
    "correction_claim": "correction_claims",
    "correction": "corrections",
    "course": "courses",
    "edition": "editions",
    "experiment": "experiments",
    "file_revision": "file_revisions",
    "file": "files",
    "interactive": "interactives",
    "module_member": "module_members",
    "module": "modules",
    "occurrence": "occurrences",
    "placeholder": "placeholders",
    "program": "programs",
    "qa_event": "qa_events",
    "relation": "relations",
    "release_snapshot": "release_snapshots",
    "resource": "resources",
    "rights": "rights",
    "rights_assignment": "rights_assignments",
    "rights_rule_member": "rights_rule_members",
    "rights_rule": "rights_rules",
    "route_member": "route_members",
    "route": "routes",
    "segment_variant": "segment_variants",
    "segment": "segments",
    "term_variant": "term_variants",
    "term": "terms",
    "unit": "units",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_fact(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(data),
        "sha256": sha256_bytes(data),
    }


def canonical_json_bytes(value: Any, *, newline: bytes = b"\n") -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8") + newline


def canonical_pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def common_id(record_type: str, stable_key: str) -> str:
    return "urn:uuid:" + str(uuid.uuid5(IDENTITY_NAMESPACE, f"{record_type}|{stable_key}"))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise SystemExit(f"{path}:{line_number}: JSONL value is not an object")
            records.append(value)
    return records


def verify_contract() -> dict[str, dict[str, Any]]:
    facts: dict[str, dict[str, Any]] = {}
    for path, (expected_bytes, expected_sha) in EXPECTED_CONTRACT.items():
        if not path.is_file():
            raise SystemExit(f"Frozen common-backend contract file missing: {path}")
        fact = file_fact(path)
        if fact["bytes"] != expected_bytes or fact["sha256"] != expected_sha:
            raise SystemExit(
                f"Frozen contract drift: {fact['path']} expected {expected_bytes}/{expected_sha}, "
                f"found {fact['bytes']}/{fact['sha256']}"
            )
        facts[fact["path"]] = fact
    return facts


def normalize_page_identity(value: dict[str, Any]) -> dict[str, Any] | None:
    aliases = {
        "page_id": ("pageid", "page_id", "upstream_pageid"),
        "revision_id": ("revid", "revision_id", "upstream_revid"),
        "revision_sha1": ("mediawiki_sha1", "revision_sha1", "upstream_mediawiki_sha1"),
        "page_title": ("title", "page_title", "upstream_title"),
        "oldid_url": ("oldid_url", "source_url", "upstream_url"),
        "timestamp": ("timestamp", "upstream_timestamp"),
    }
    result: dict[str, Any] = {}
    for target, keys in aliases.items():
        for key in keys:
            candidate = value.get(key)
            if candidate is not None and candidate != "":
                result[target] = candidate
                break
    required = ("page_id", "revision_id", "revision_sha1", "page_title")
    if not all(key in result for key in required):
        return None
    try:
        result["page_id"] = int(result["page_id"])
        result["revision_id"] = int(result["revision_id"])
    except (TypeError, ValueError):
        return None
    result["revision_sha1"] = str(result["revision_sha1"])
    result["page_title"] = str(result["page_title"])
    return result


def walk_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_dicts(child)


def authority_index(through_unit: int) -> dict[tuple[int, int], dict[str, Any]]:
    """Index referenced MediaWiki pages to exact frozen local witness bytes."""

    index: dict[tuple[int, int], dict[str, Any]] = {}

    # Unit 1 predates the per-unit JSON manifest but its exact MediaWiki XML
    # exports are frozen. Parse only these two known task-local directories.
    legacy_dirs = [
        ROOT / "authority" / "wikiversity",
        ROOT / "authority" / "wikiversity" / "worksheet-01-solutions",
    ]
    for legacy_dir in legacy_dirs:
        if not legacy_dir.is_dir():
            continue
        for xml_path in sorted(legacy_dir.glob("*.xml")):
            try:
                xml_root = ET.parse(xml_path).getroot()
            except ET.ParseError as exc:
                raise SystemExit(f"Frozen MediaWiki XML is not parseable: {xml_path}: {exc}") from exc
            page = xml_root.find(".//{*}page")
            if page is None:
                continue
            title_node = page.find("{*}title")
            page_id_node = page.find("{*}id")
            revision = page.find("{*}revision")
            if title_node is None or page_id_node is None or revision is None:
                continue
            revision_id_node = revision.find("{*}id")
            sha1_node = revision.find("{*}sha1")
            timestamp_node = revision.find("{*}timestamp")
            if revision_id_node is None or sha1_node is None:
                continue
            fact = file_fact(xml_path)
            html_path = xml_path.with_suffix(".html")
            html_sha = file_fact(html_path)["sha256"] if html_path.is_file() else None
            page_id = int(page_id_node.text or "0")
            revision_id = int(revision_id_node.text or "0")
            index[(page_id, revision_id)] = {
                "page_id": page_id,
                "revision_id": revision_id,
                "revision_sha1": str(sha1_node.text or ""),
                "page_title": str(title_node.text or ""),
                "timestamp": timestamp_node.text if timestamp_node is not None else None,
                "witness": fact,
                "api_url": "https://de.wikiversity.org/w/api.php",
                "rendered_html_sha256": html_sha,
                "expanded_tex_sha256": None,
            }

    for unit_number in range(1, through_unit + 1):
        manifest_path = (
            ROOT
            / "authority"
            / "wikiversity"
            / f"unit-{unit_number:02d}"
            / "UNIT_AUTHORITY_MANIFEST.json"
        )
        if not manifest_path.is_file():
            continue
        manifest = load_json(manifest_path)
        base = manifest_path.parent
        batch_by_title: dict[str, dict[str, Any]] = {}
        for node in walk_dicts(manifest):
            if not isinstance(node.get("requested_titles"), list):
                continue
            if not all(key in node for key in ("file", "bytes", "sha256")):
                continue
            witness_path = base / str(node["file"])
            if not witness_path.is_file():
                raise SystemExit(f"Authority batch witness absent: {witness_path}")
            fact = file_fact(witness_path)
            if fact["bytes"] != int(node["bytes"]) or fact["sha256"] != str(node["sha256"]):
                raise SystemExit(f"Authority batch witness drift: {fact['path']}")
            for title in node["requested_titles"]:
                batch_by_title[str(title)] = fact

        for node in walk_dicts(manifest):
            identity = normalize_page_identity(node)
            if identity is None:
                continue
            witness: dict[str, Any] | None = None
            for prefix in ("xml", "api", "html"):
                file_key = f"{prefix}_file"
                bytes_key = f"{prefix}_bytes"
                sha_key = f"{prefix}_sha256"
                if all(key in node for key in (file_key, bytes_key, sha_key)):
                    witness_path = base / str(node[file_key])
                    if witness_path.is_file():
                        fact = file_fact(witness_path)
                        if fact["bytes"] != int(node[bytes_key]) or fact["sha256"] != str(node[sha_key]):
                            raise SystemExit(f"Authority page witness drift: {fact['path']}")
                        witness = fact
                        break
            if witness is None:
                witness = batch_by_title.get(identity["page_title"])
            if witness is None:
                continue
            item = {
                **identity,
                "witness": witness,
                "api_url": manifest.get("source_api", "https://de.wikiversity.org/w/api.php"),
                "rendered_html_sha256": node.get("html_sha256"),
                "expanded_tex_sha256": None,
            }
            key = (identity["page_id"], identity["revision_id"])
            existing = index.get(key)
            if existing is None or item["witness"]["path"] < existing["witness"]["path"]:
                index[key] = item
    return index


def page_identity_from_native(record: dict[str, Any]) -> dict[str, Any] | None:
    candidates: list[dict[str, Any]] = []
    for node in walk_dicts(record.get("provenance", {})):
        identity = normalize_page_identity(node)
        if identity is not None:
            candidates.append(identity)
    if not candidates:
        return None
    # Prefer the most specific frozen page witness: a record with an explicit
    # oldid URL, then the deepest-discovered candidate (solutions appear after
    # their broader worksheet provenance).
    candidates.sort(key=lambda item: (bool(item.get("oldid_url")), len(item.get("page_title", ""))))
    return candidates[-1]


def native_extension(record: dict[str, Any], ordinal: int) -> dict[str, Any]:
    return {
        "ag-bridge.native-record": copy.deepcopy(record),
        "ag-bridge.native-ordinal": ordinal,
        "ag-bridge.mapping": {
            "native_entity_class": record["entity_class"],
            "native_stable_id": record["stable_id"],
            "native_id_preserved_as": "stable_key",
        },
    }


def base_record(
    native: dict[str, Any],
    ordinal: int,
    record_type: str,
    stable_key: str | None = None,
) -> dict[str, Any]:
    stable_key = stable_key or native["stable_id"]
    return {
        "id": common_id(record_type, stable_key),
        "record_type": record_type,
        "recorded_at": native["timestamp"],
        "schema_name": SCHEMA_NAME,
        "schema_version": SCHEMA_VERSION,
        "stable_key": stable_key,
        "status": native["status"],
        "supersedes_id": None,
        "workflow_id": native["responsible_workflow"],
        "extensions": native_extension(native, ordinal),
    }


def derived_base(
    record_type: str,
    stable_key: str,
    recorded_at: str,
    workflow_id: str,
    *,
    source_native_id: str,
    status: str = "active",
) -> dict[str, Any]:
    return {
        "id": common_id(record_type, stable_key),
        "record_type": record_type,
        "recorded_at": recorded_at,
        "schema_name": SCHEMA_NAME,
        "schema_version": SCHEMA_VERSION,
        "stable_key": stable_key,
        "status": status,
        "supersedes_id": None,
        "workflow_id": workflow_id,
        "extensions": {
            "ag-bridge.derived-from-native-id": source_native_id,
            "ag-bridge.adapter-only": True,
        },
    }


def digest_native_record(record: dict[str, Any]) -> str:
    return sha256_bytes(canonical_json_bytes(record, newline=b""))


def first_nonempty(*values: Any, default: str = "") -> str:
    for value in values:
        if value is not None and str(value).strip():
            return str(value)
    return default


def build_dataset(
    native_records: list[dict[str, Any]],
    native_manifest: dict[str, Any],
    profiles_by_page: dict[tuple[int, int], dict[str, Any]],
    profile_schema: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    native_by_id = {record["stable_id"]: record for record in native_records}
    if len(native_by_id) != len(native_records):
        raise SystemExit("Native stable IDs are not globally unique")
    unsupported = sorted({record["entity_class"] for record in native_records} - PRIMARY_TYPE.keys())
    if unsupported:
        raise SystemExit(f"Unsupported native entity classes: {unsupported}")

    through_unit = int(native_manifest["through_unit"])
    target_id_by_native = {
        record["stable_id"]: common_id(PRIMARY_TYPE[record["entity_class"]], record["stable_id"])
        for record in native_records
    }
    # A correction ledger may name a real source/editorial target that was not
    # promoted to a first-class native backend record (Unit 1's media-credit
    # section is the known case). Preserve that explicit identifier as an
    # adapter-only unit rather than dropping the binding or fabricating content.
    explicit_unmaterialized_targets = sorted(
        {
            affected
            for record in native_records
            if record["entity_class"] == "correction"
            for affected in list((record.get("payload") or {}).get("affected_unit_ids") or [])
            if affected not in target_id_by_native
        }
    )
    for stable_key in explicit_unmaterialized_targets:
        target_id_by_native[stable_key] = common_id("unit", stable_key)

    def resolve(native_id: str | None, *, allow_none: bool = True) -> str | None:
        if native_id is None:
            if allow_none:
                return None
            raise SystemExit("Required native foreign key is null")
        result = target_id_by_native.get(native_id)
        if result is None:
            raise SystemExit(f"Native foreign key has no target mapping: {native_id}")
        return result

    editorial_resource_native = "resource.algebraic-geometry-bridge-id.editorial-layer"
    editorial_rights_native = "rights.derivative-editorial.cc-by-sa-4.0"
    if editorial_resource_native not in target_id_by_native or editorial_rights_native not in target_id_by_native:
        raise SystemExit("Native editorial resource/rights anchors are absent")
    editorial_resource_id = resolve(editorial_resource_native, allow_none=False)
    editorial_rights_id = resolve(editorial_rights_native, allow_none=False)

    current_edition_native = next(
        (
            record["stable_id"]
            for record in native_records
            if record["entity_class"] == "edition"
            and f"units-01-{through_unit:02d}." in record["stable_id"]
        ),
        None,
    )
    if current_edition_native is None:
        candidates = [record["stable_id"] for record in native_records if record["entity_class"] == "edition"]
        if not candidates:
            raise SystemExit("No native edition record exists")
        current_edition_native = sorted(candidates)[-1]
    current_edition_id = resolve(current_edition_native, allow_none=False)

    tables: dict[str, list[dict[str, Any]]] = {name: [] for name in TABLES}
    primary_by_native: dict[str, dict[str, Any]] = {}
    profile_validator = Draft202012Validator(profile_schema, format_checker=FormatChecker())
    profile_witnesses: dict[tuple[str, str], dict[str, Any]] = {}
    profile_eligible = 0
    profile_bound = 0
    profile_missing: list[str] = []

    def add(record: dict[str, Any]) -> None:
        tables[TABLE_FOR_TYPE[record["record_type"]]].append(record)

    # One adapter-only unit expresses the explicit whole-lane scope already
    # present in every terminology record. It is not reader content.
    scope_key = "adapter.scope.algebraic-geometry-bridge-id.whole-lane"
    scope_unit = derived_base(
        "unit",
        scope_key,
        native_manifest["generated_from_build_utc"],
        "workflow.o016-d100.algebraic-geometry-bridge-id",
        source_native_id="00_control/TERMINOLOGY.csv",
        status="derived",
    )
    scope_unit.update(
        {
            "first_edition_id": current_edition_id,
            "identity_anchor": "whole_lane",
            "identity_basis": "explicit native term scope=whole_lane",
            "resource_id": editorial_resource_id,
            "rights_default_id": editorial_rights_id,
            "source_label": "whole_lane",
            "source_local_id": "whole_lane",
            "source_path": "00_control/TERMINOLOGY.csv",
            "source_xml_path": None,
            "unit_kind": "terminology_scope",
        }
    )
    add(scope_unit)

    for stable_key in explicit_unmaterialized_targets:
        referenced = derived_base(
            "unit",
            stable_key,
            native_manifest["generated_from_build_utc"],
            "workflow.o016-d100.algebraic-geometry-bridge-id",
            source_native_id=stable_key,
            status="referenced_not_materialized_in_native_backend",
        )
        referenced["extensions"]["ag-bridge.derivation-basis"] = (
            "explicit affected_unit_ids value in the frozen native correction ledger"
        )
        referenced.update(
            {
                "first_edition_id": current_edition_id,
                "identity_anchor": stable_key,
                "identity_basis": "explicit native correction target identifier",
                "resource_id": editorial_resource_id,
                "rights_default_id": editorial_rights_id,
                "source_label": stable_key,
                "source_local_id": stable_key,
                "source_path": "00_control/CORRECTIONS.csv",
                "source_xml_path": None,
                "unit_kind": "editorial_reference_target",
            }
        )
        add(referenced)

    for ordinal, native in enumerate(native_records):
        entity = native["entity_class"]
        record_type = PRIMARY_TYPE[entity]
        common = base_record(native, ordinal, record_type)
        payload = native.get("payload") or {}
        resource_id = resolve(native.get("resource_id"))
        rights_id = resolve(native.get("rights_id"))
        edition_id = resolve(native.get("edition_id"))

        supersedes = native.get("supersedes")
        common["supersedes_id"] = resolve(supersedes) if supersedes else None

        if entity == "program":
            common.update(
                {
                    "curriculum_version": first_nonempty(native.get("source_local_id"), default="v0"),
                    "locale": native.get("language") or "id-ID",
                    "program_key": first_nonempty(native.get("source_local_id"), native["stable_id"]),
                    "rights_id": rights_id or editorial_rights_id,
                    "title": first_nonempty(payload.get("title"), native["stable_id"]),
                }
            )
        elif entity == "course":
            common.update(
                {
                    "course_key": first_nonempty(native.get("source_local_id"), native["stable_id"]),
                    "curriculum_source_locator": native.get("source_locator") or "",
                    "curriculum_source_sha256": native.get("content_sha256"),
                    "order_key": f"{int(native.get('order') or 0):04d}",
                    "outcome": first_nonempty(payload.get("outcome"), payload.get("bounded_extent")),
                    "prerequisite_course_keys": list(native.get("prerequisite_ids") or []),
                    "program_id": resolve(native.get("parent_id"), allow_none=False),
                    "resource_keys": [native["resource_id"]] if native.get("resource_id") else [],
                    "role": first_nonempty(payload.get("role"), default="course"),
                    "scope": first_nonempty(payload.get("bounded_extent"), payload.get("scope")),
                    "stage": first_nonempty(payload.get("stage"), default="bridge"),
                    "title": first_nonempty(payload.get("role"), payload.get("title"), native["stable_id"]),
                }
            )
        elif entity == "edition":
            source_edition_native = payload.get("source_edition_id")
            # The common schema requires a 40-hex commit_sha even for non-VCS
            # MediaWiki/local editions. The all-zero sentinel is explicit and
            # losslessly qualified in extensions; no commit is invented.
            common["extensions"]["ag-bridge.commit-sha-status"] = "not_applicable_schema_required_sentinel"
            common.update(
                {
                    "archive_sha256": None,
                    "commit_sha": "0" * 40,
                    "edition_kind": first_nonempty(payload.get("edition_kind"), default="translation"),
                    "locale": native.get("language") or "und",
                    "release_date": str(native["timestamp"])[:10],
                    "resource_id": resource_id or editorial_resource_id,
                    "rights_id": rights_id or editorial_rights_id,
                    "source_edition_id": resolve(source_edition_native) if source_edition_native else None,
                    "tree_sha": None,
                    "vcs_ref": "",
                    "vcs_type": "none",
                    "version_label": native["stable_id"],
                }
            )
        elif entity in {"unit", "exercise", "solution"}:
            source_label = first_nonempty(
                payload.get("title_markdown"),
                payload.get("family"),
                native.get("source_local_id"),
                native["stable_id"],
            )
            common.update(
                {
                    "first_edition_id": edition_id or current_edition_id,
                    "identity_anchor": first_nonempty(native.get("source_local_id"), native["stable_id"]),
                    "identity_basis": "native stable_id/source_local_id",
                    "resource_id": resource_id or editorial_resource_id,
                    "rights_default_id": rights_id or editorial_rights_id,
                    "source_label": source_label,
                    "source_local_id": native.get("source_local_id"),
                    "source_path": native.get("path") or native.get("source_locator") or "",
                    "source_xml_path": None,
                    "unit_kind": first_nonempty(payload.get("unit_type"), payload.get("family"), entity),
                }
            )
        elif entity == "segment":
            common.update(
                {
                    "identity_anchor": first_nonempty(native.get("source_local_id"), native["stable_id"]),
                    "ordinal": int(native.get("order") or 0),
                    "segment_kind": first_nonempty(payload.get("segment_type"), default="prose"),
                    "segmentation_profile": "ag-bridge-markdown-v1",
                    "unit_id": resolve(native.get("parent_id"), allow_none=False),
                }
            )
            variant_key = native["stable_id"] + "|variant|" + (native.get("language") or "und")
            variant = derived_base(
                "segment_variant",
                variant_key,
                native["timestamp"],
                native["responsible_workflow"],
                source_native_id=native["stable_id"],
                status=native["status"],
            )
            variant_payload = str(payload.get("markdown", ""))
            variant.update(
                {
                    "edition_id": edition_id or current_edition_id,
                    "format": "markdown",
                    "locale": native.get("language") or "und",
                    "payload": variant_payload,
                    "payload_sha256": sha256_bytes(variant_payload.encode("utf-8")),
                    "rights_id": rights_id or editorial_rights_id,
                    "role": "translation" if native.get("language") == "id-ID" else "source",
                    "segment_id": common["id"],
                    "source_variant_id": None,
                    "translation_state": native.get("translation_state") or "translated",
                }
            )
            add(variant)
        elif entity == "concept":
            common.update(
                {
                    "concept_key": native["stable_id"],
                    "concept_scheme": "ag-bridge-terminology",
                    "definition_segment_id": None,
                    "parent_concept_id": resolve(native.get("parent_id")) if native.get("parent_id") else None,
                }
            )
        elif entity == "term":
            concept_native = (native.get("concept_ids") or [native.get("parent_id")])[0]
            common.update(
                {
                    "concept_id": resolve(concept_native, allow_none=False),
                    "evidence": first_nonempty(payload.get("rationale"), native.get("source_locator")),
                    "notes": first_nonempty(payload.get("rejected_or_variant")),
                    "preferred_form": first_nonempty(payload.get("preferred_target"), native["stable_id"]),
                    "register": "technical",
                    "scope_unit_id": scope_unit["id"],
                    "source_form": first_nonempty(payload.get("source_term"), native.get("source_local_id")),
                    "source_locale": first_nonempty(payload.get("source_language"), default="de"),
                    "source_term_id": first_nonempty(native.get("source_local_id"), native["stable_id"]),
                    "target_locale": native.get("language") or "id-ID",
                    "term_status": native["status"],
                }
            )
        elif entity == "asset":
            media_type = first_nonempty(payload.get("mime"), mimetypes.guess_type(str(native.get("path") or ""))[0], default="application/octet-stream")
            common.update(
                {
                    "asset_kind": first_nonempty(payload.get("selected_form"), default="media"),
                    "canonical_path_or_uri": first_nonempty(native.get("path"), payload.get("selected_url"), native.get("source_locator")),
                    "media_type": media_type,
                    "resource_id": resource_id or editorial_resource_id,
                    "rights_default_id": rights_id or editorial_rights_id,
                }
            )
            if native.get("content_sha256") and payload.get("bytes") is not None:
                revision_key = native["stable_id"] + "|revision|" + native["content_sha256"]
                revision = derived_base(
                    "asset_revision",
                    revision_key,
                    native["timestamp"],
                    native["responsible_workflow"],
                    source_native_id=native["stable_id"],
                    status=native["status"],
                )
                revision.update(
                    {
                        "asset_id": common["id"],
                        "bytes": int(payload["bytes"]),
                        "edition_id": edition_id or current_edition_id,
                        "file_revision_id": None,
                        "sha256": native["content_sha256"],
                        "source_asset_revision_id": None,
                    }
                )
                add(revision)
        elif entity == "artifact":
            common.update(
                {
                    "artifact_kind": first_nonempty(payload.get("media_type"), default="build_artifact"),
                    "build_receipt": first_nonempty(payload.get("build_receipt")),
                    "bytes": int(payload["bytes"]) if payload.get("bytes") is not None else None,
                    "edition_id": edition_id or current_edition_id,
                    "locale": native.get("language") or "und",
                    "manifest_sha256": payload.get("manifest_sha256"),
                    "public_uri": payload.get("public_uri"),
                    "sha256": native.get("content_sha256"),
                    "toolchain_id": first_nonempty(payload.get("toolchain_id"), default="ag-bridge-native-build"),
                    "tree_sha256": payload.get("tree_sha256"),
                }
            )
        elif entity == "resource":
            common.update(
                {
                    "authority_policy": "frozen native authority and provenance bindings",
                    "creator_name": first_nonempty(payload.get("creator"), default="not asserted in native record"),
                    "official_reader": native.get("source_locator") if str(native.get("source_locator") or "").startswith("http") else None,
                    "official_repository": native.get("source_locator") or "",
                    "original_title": first_nonempty(payload.get("title"), native["stable_id"]),
                    "resource_key": first_nonempty(native.get("source_local_id"), native["stable_id"]),
                    "work_type": first_nonempty(payload.get("relationship"), payload.get("use_in_lane"), default="educational_resource"),
                }
            )
        elif entity == "rights":
            attribution = first_nonempty(
                payload.get("attribution"),
                payload.get("creator_or_artist"),
                payload.get("uploader"),
                default="See native component-rights record",
            )
            common.update(
                {
                    "assertion_status": native["status"],
                    "attribution": attribution,
                    "authority": native.get("source_locator") or "native component-rights record",
                    "change_notice": first_nonempty(payload.get("change_notice")),
                    "license_expression": first_nonempty(payload.get("license"), payload.get("usage_terms"), default="NOASSERTION"),
                    "nonendorsement": first_nonempty(payload.get("nonendorsement")),
                    "notice_locator": native.get("source_locator") or "native backend record",
                    "notice_sha256": native.get("content_sha256") or digest_native_record(native),
                    "source_component_id": first_nonempty(payload.get("scope"), native.get("source_local_id"), native["stable_id"]),
                    "third_party_status": first_nonempty(payload.get("third_party_status"), default="component-specific"),
                }
            )
        elif entity == "correction":
            affected = list(payload.get("affected_unit_ids") or [])
            if not affected:
                raise SystemExit(f"Correction has no affected native ID: {native['stable_id']}")
            common.update(
                {
                    "affected_id": resolve(affected[0], allow_none=False),
                    "binding_status": "losslessly_preserved",
                    "category": first_nonempty(payload.get("kind"), default="editorial_correction"),
                    "evidence_locator": native.get("source_locator") or "00_control/CORRECTIONS.csv",
                    "local_state": native["status"],
                    "original_payload_sha256": None,
                    "payload_hash_basis": "native correction payload canonical SHA-256",
                    "rationale": first_nonempty(payload.get("target_action"), payload.get("authority_observation"), payload.get("rationale")),
                    "replacement_payload_sha256": native.get("content_sha256") or digest_native_record(native),
                    "source_claim_id": None,
                    "source_edition_id": edition_id or current_edition_id,
                    "source_record_id": None,
                    "upstream_disposition": first_nonempty(payload.get("upstream_report_disposition"), default="not_contacted_during_production"),
                    "upstream_url": None,
                }
            )
        elif entity == "qa_event":
            result_value = payload.get("result")
            result_text = result_value.get("status") if isinstance(result_value, dict) else result_value
            common.update(
                {
                    "input_hash": native.get("content_sha256") or digest_native_record(native),
                    "method": first_nonempty(payload.get("qa_kind"), default="native QA replay"),
                    "qa_type": first_nonempty(payload.get("qa_kind"), default="qa"),
                    "result": str(result_text or native["status"]),
                    "reviewer_kind": "automated_or_recorded_human",
                    "severity_p1": 0,
                    "severity_p2": 0,
                    "severity_p3": 0,
                    "tool_name": "ag-bridge-native-qa",
                    "tool_version": native.get("schema_version") or "1.0.0",
                    "witness_locator": native.get("source_locator") or "native backend qa_event",
                }
            )
        elif entity == "relation":
            subject = payload.get("subject_id")
            object_id = payload.get("object_id")
            common.update(
                {
                    "assertion_method": "native explicit relation",
                    "confidence": "asserted",
                    "edition_id": edition_id,
                    "from_id": resolve(subject, allow_none=False),
                    "ordinal": int(native.get("order") or 0),
                    "relation_type": first_nonempty(payload.get("relation_type"), default="related_to"),
                    "source_locator": native.get("source_locator") or "native relation record",
                    "strength": "direct",
                    "to_id": resolve(object_id, allow_none=False),
                }
            )

        # Promote a complete, locally witnessed MediaWiki identity into the
        # frozen strict source-format profile without altering native data.
        page_identity = page_identity_from_native(native)
        if page_identity is not None:
            profile_eligible += 1
            witness = profiles_by_page.get((page_identity["page_id"], page_identity["revision_id"]))
            if witness is None:
                profile_missing.append(native["stable_id"])
            else:
                witness_fact = witness["witness"]
                witness_key = (witness_fact["path"], witness_fact["sha256"])
                file_key = "authority-file|" + witness_fact["path"]
                revision_key = file_key + "|sha256|" + witness_fact["sha256"]
                file_revision_id = common_id("file_revision", revision_key)
                profile = {
                    "format_profile": "mediawiki",
                    "profile_version": "1.0.0",
                    "authority_file_revision_id": file_revision_id,
                    "authority_path": witness_fact["path"],
                    "identity_strategy": "native_id" if native.get("source_local_id") else "structural_path",
                    "page_id": page_identity["page_id"],
                    "revision_id": page_identity["revision_id"],
                    "revision_sha1": page_identity["revision_sha1"],
                    "page_title": page_identity["page_title"],
                    "api_url": witness.get("api_url"),
                    "rendered_html_sha256": witness.get("rendered_html_sha256"),
                    "expanded_tex_sha256": witness.get("expanded_tex_sha256"),
                    "transclusion_revision_ids": [],
                }
                errors = sorted(profile_validator.iter_errors(profile), key=lambda err: list(err.path))
                if errors:
                    raise SystemExit(
                        "Strict source-profile validation failed for "
                        + native["stable_id"]
                        + ": "
                        + "; ".join(error.message for error in errors[:5])
                    )
                common["extensions"]["interlanguage.source-profile"] = profile
                profile_bound += 1
                profile_witnesses.setdefault(
                    witness_key,
                    {
                        "fact": witness_fact,
                        "file_key": file_key,
                        "revision_key": revision_key,
                        "recorded_at": native["timestamp"],
                        "workflow_id": native["responsible_workflow"],
                        "resource_id": resource_id or editorial_resource_id,
                        "edition_id": edition_id or current_edition_id,
                        "source_native_id": native["stable_id"],
                    },
                )

        add(common)
        primary_by_native[native["stable_id"]] = common

    # Materialize only virtual file/file-revision facts for strict profile FK
    # closure. Their hashes are exact hashes of already frozen local witnesses.
    for witness in sorted(profile_witnesses.values(), key=lambda item: item["file_key"]):
        fact = witness["fact"]
        file_record = derived_base(
            "file",
            witness["file_key"],
            witness["recorded_at"],
            witness["workflow_id"],
            source_native_id=witness["source_native_id"],
            status="source_frozen",
        )
        media_type = first_nonempty(mimetypes.guess_type(fact["path"])[0], default="application/octet-stream")
        file_record.update(
            {
                "canonical_path": fact["path"],
                "media_type": media_type,
                "parse_mode": "mediawiki_authority_witness",
                "resource_id": witness["resource_id"],
                "role": "source_authority_witness",
            }
        )
        add(file_record)
        revision = derived_base(
            "file_revision",
            witness["revision_key"],
            witness["recorded_at"],
            witness["workflow_id"],
            source_native_id=witness["source_native_id"],
            status="source_frozen",
        )
        revision.update(
            {
                "actual_path": fact["path"],
                "bytes": int(fact["bytes"]),
                "edition_id": witness["edition_id"],
                "file_id": file_record["id"],
                "generated": False,
                "git_blob_sha1": None,
                "sha256": fact["sha256"],
                "source_revision_id": None,
            }
        )
        add(revision)

    # Preserve every explicit native rights assignment as a common assignment.
    for native in native_records:
        if not native.get("rights_id"):
            continue
        primary = primary_by_native[native["stable_id"]]
        target_id = primary["id"]
        if native["entity_class"] == "segment":
            variant_key = native["stable_id"] + "|variant|" + (native.get("language") or "und")
            target_id = common_id("segment_variant", variant_key)
        assignment_key = "rights-assignment|" + native["stable_id"]
        assignment = derived_base(
            "rights_assignment",
            assignment_key,
            native["timestamp"],
            native["responsible_workflow"],
            source_native_id=native["stable_id"],
            status=native["status"],
        )
        assignment.update(
            {
                "assignment_status": "explicit_native_assignment",
                "inheritance": "none",
                "precedence": 100,
                "rights_id": resolve(native["rights_id"], allow_none=False),
                "scope_role": native["entity_class"],
                "target_id": target_id,
            }
        )
        add(assignment)

    # Preserve all correction-to-target multiplicity as explicit relations.
    for native in native_records:
        if native["entity_class"] != "correction":
            continue
        affected = list((native.get("payload") or {}).get("affected_unit_ids") or [])
        for index, affected_native in enumerate(affected, 1):
            relation_key = f"{native['stable_id']}|applies-to|{index:03d}|{affected_native}"
            relation = derived_base(
                "relation",
                relation_key,
                native["timestamp"],
                native["responsible_workflow"],
                source_native_id=native["stable_id"],
                status=native["status"],
            )
            relation.update(
                {
                    "assertion_method": "native correction affected_unit_ids",
                    "confidence": "asserted",
                    "edition_id": resolve(native.get("edition_id")),
                    "from_id": resolve(native["stable_id"], allow_none=False),
                    "ordinal": index,
                    "relation_type": "correction_applies_to",
                    "source_locator": native.get("source_locator") or "00_control/CORRECTIONS.csv",
                    "strength": "direct",
                    "to_id": resolve(affected_native, allow_none=False),
                }
            )
            add(relation)

    for table in TABLES:
        tables[table].sort(key=lambda record: (record["stable_key"], record["id"]))

    dataset_key = "algebraic-geometry-bridge-id.common-backend-v1"
    dataset = {
        "$schema": "schema/backend-v1.schema.json",
        "dataset_id": common_id("dataset", dataset_key),
        "dataset_version": f"units-01-{through_unit:02d}.native-{native_manifest['schema_version']}",
        "schema_name": SCHEMA_NAME,
        "schema_version": SCHEMA_VERSION,
        "tables": tables,
    }
    details = {
        "native_id_count": len(native_records),
        "profile_eligible": profile_eligible,
        "profile_bound": profile_bound,
        "profile_missing_count": len(profile_missing),
        "profile_missing_native_ids": profile_missing,
        "profile_witness_file_count": len(profile_witnesses),
        "current_edition_native_id": current_edition_native,
        "scope_unit_id": scope_unit["id"],
        "explicit_unmaterialized_target_count": len(explicit_unmaterialized_targets),
    }
    return dataset, details


def virtual_jsonl(dataset: dict[str, Any]) -> bytes:
    parts: list[bytes] = []
    for table in TABLES:
        for record in dataset["tables"][table]:
            parts.append(canonical_json_bytes(record))
    return b"".join(parts)


def reverse_native_jsonl(dataset: dict[str, Any]) -> bytes:
    recovered: list[tuple[int, dict[str, Any]]] = []
    for table in TABLES:
        for record in dataset["tables"][table]:
            extensions = record.get("extensions") or {}
            if "ag-bridge.native-record" in extensions:
                recovered.append(
                    (
                        int(extensions["ag-bridge.native-ordinal"]),
                        extensions["ag-bridge.native-record"],
                    )
                )
    recovered.sort(key=lambda pair: pair[0])
    return b"".join(canonical_json_bytes(record, newline=b"\r\n") for _, record in recovered)


def validate_fk_closure(dataset: dict[str, Any]) -> dict[str, Any]:
    all_records = [record for table in TABLES for record in dataset["tables"][table]]
    ids = [record["id"] for record in all_records]
    if len(ids) != len(set(ids)):
        duplicates = [value for value, count in Counter(ids).items() if count > 1]
        raise SystemExit(f"Common target IDs are not globally unique: {duplicates[:10]}")
    id_set = set(ids)
    reference_fields = {
        "program": ("rights_id", "supersedes_id"),
        "course": ("program_id", "supersedes_id"),
        "edition": ("resource_id", "rights_id", "source_edition_id", "supersedes_id"),
        "unit": ("first_edition_id", "resource_id", "rights_default_id", "supersedes_id"),
        "segment": ("unit_id", "supersedes_id"),
        "segment_variant": ("edition_id", "rights_id", "segment_id", "source_variant_id", "supersedes_id"),
        "concept": ("definition_segment_id", "parent_concept_id", "supersedes_id"),
        "term": ("concept_id", "scope_unit_id", "supersedes_id"),
        "asset": ("resource_id", "rights_default_id", "supersedes_id"),
        "asset_revision": ("asset_id", "edition_id", "file_revision_id", "source_asset_revision_id", "supersedes_id"),
        "artifact": ("edition_id", "supersedes_id"),
        "correction": ("affected_id", "source_edition_id", "source_claim_id", "source_record_id", "supersedes_id"),
        "relation": ("edition_id", "from_id", "to_id", "supersedes_id"),
        "file": ("resource_id", "supersedes_id"),
        "file_revision": ("edition_id", "file_id", "source_revision_id", "supersedes_id"),
        "rights_assignment": ("rights_id", "target_id", "supersedes_id"),
        "resource": ("supersedes_id",),
        "rights": ("supersedes_id",),
        "qa_event": ("supersedes_id",),
    }
    checked = 0
    for record in all_records:
        for field in reference_fields.get(record["record_type"], ("supersedes_id",)):
            value = record.get(field)
            if value is None:
                continue
            checked += 1
            if value not in id_set:
                raise SystemExit(
                    f"Common foreign key is not closed: {record['stable_key']} {field}={value}"
                )
        profile = (record.get("extensions") or {}).get("interlanguage.source-profile")
        if profile is not None:
            checked += 1
            if profile["authority_file_revision_id"] not in id_set:
                raise SystemExit(
                    f"Source-profile authority_file_revision_id is not closed: {record['stable_key']}"
                )
    return {"global_id_count": len(ids), "foreign_keys_checked": checked}


def validate_dataset(dataset: dict[str, Any], schema: dict[str, Any]) -> None:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(dataset), key=lambda error: list(error.absolute_path))
    if errors:
        messages = []
        for error in errors[:20]:
            location = "/".join(str(item) for item in error.absolute_path)
            messages.append(f"{location or '<root>'}: {error.message}")
        raise SystemExit("Common-backend schema validation failed:\n" + "\n".join(messages))


def assert_sanitized(value: Any) -> None:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    forbidden_patterns = (
        r"(?i)authorization\s*:",
        r"(?i)bearer\s+[a-z0-9._-]+",
        r"(?i)(access[_-]?token|api[_-]?key|secret)\s*[=:]\s*[^,}\s]+",
        r"(?i)c:\\\\users\\\\",
    )
    for pattern in forbidden_patterns:
        if re.search(pattern, text):
            raise SystemExit(f"Sanitization guard rejected receipt content matching {pattern!r}")


def receipt_evidence(paths: Iterable[Path]) -> list[dict[str, Any]]:
    facts = []
    for path in paths:
        if not path.is_file():
            raise SystemExit(f"Required frozen-boundary evidence absent: {path}")
        facts.append(file_fact(path))
    return facts


def status_is_pass(path: Path) -> bool:
    value = load_json(path)
    candidates = [
        value.get("status") if isinstance(value, dict) else None,
        value.get("result") if isinstance(value, dict) else None,
        value.get("validation", {}).get("result") if isinstance(value, dict) else None,
    ]
    normalized = {str(candidate).lower() for candidate in candidates if candidate is not None}
    return bool(normalized & {"pass", "passed", "ok", "success"})


def terminology_receipt(
    through_unit: int,
    target_hash: str,
    target_record_count: int,
    replay_evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    migration_path = ROOT / "qa" / "TERMINOLOGY_MIGRATION_UNIT_07.json"
    report_path = ROOT / "authority" / "terminology-id-arxiv" / "TERMINOLOGY_QA_REPORT.md"
    source_manifest_path = ROOT / "authority" / "terminology-id-arxiv" / "SOURCE_MANIFEST.json"
    control_path = ROOT / "00_control" / "TERMINOLOGY_QA_20260822.md"
    for path in (migration_path, report_path, source_manifest_path, control_path):
        if not path.is_file():
            raise SystemExit(f"Terminology-QA evidence absent: {path}")
    migration = load_json(migration_path)
    source_manifest = load_json(source_manifest_path)
    fallback_sources = []
    for source in source_manifest.get("fallback_sources", []):
        fallback_sources.append(
            {
                "role": source.get("role"),
                "title": source.get("title"),
                "authors": source.get("authors", []),
                "doi": source.get("doi"),
                "official_record_url": source.get("official_record_url"),
                "language": source.get("language"),
                "local_evidence_path": "authority/terminology-id-arxiv/" + source.get("local_pdf", ""),
                "pdf_bytes": source.get("pdf_bytes"),
                "pdf_sha256": source.get("pdf_sha256"),
                "license_evidence": source.get("license_evidence"),
                "redistributed": False,
            }
        )
    return {
        "schema_name": "ag-bridge-terminology-qa-receipt",
        "schema_version": "1.0.0",
        "status": "pass",
        "boundary": f"cumulative Units 1--{through_unit}",
        "model_provenance": MODEL_PROVENANCE,
        "search": source_manifest.get("arxiv_search", {}),
        "fallback_sources": fallback_sources,
        "decisions": migration.get("replacements", []),
        "retained_terms_and_glossary_decisions": {
            "control_record": file_fact(control_path),
            "migration_post_counts": migration.get("post_counts", {}),
        },
        "changed_paths": migration.get("changed_paths", []),
        "files_examined": migration.get("files_examined"),
        "files_changed": migration.get("files_changed"),
        "evidence": [
            file_fact(migration_path),
            file_fact(report_path),
            file_fact(source_manifest_path),
            file_fact(control_path),
        ],
        "replay_validation": {
            "result": "pass",
            "evidence": replay_evidence,
            "common_backend_virtual_records_jsonl_sha256": target_hash,
            "common_backend_record_count": target_record_count,
        },
        "credit_preservation": {
            "source_author_credits_preserved": True,
            "human_contributor_credits_preserved": True,
            "model_identification_additive_only": True,
        },
        "publication_payload": {
            "authority_fallback_pdfs_included": False,
            "reason": "local terminology evidence only; rights are absent or conflicting",
        },
        "credentials_recorded": False,
    }


def migration_receipt(
    native_backend: Path,
    native_manifest: dict[str, Any],
    contract_facts: dict[str, dict[str, Any]],
    dataset: dict[str, Any],
    details: dict[str, Any],
    virtual_bytes: bytes,
    reverse_bytes: bytes,
    fk_result: dict[str, Any],
    terminology_fact: dict[str, Any],
    public_record_url: str,
    public_record_doi: str | None,
    public_concept_doi: str | None,
    public_files: list[Path],
) -> dict[str, Any]:
    native_manifest_path = native_backend / "MANIFEST.json"
    native_records_path = native_backend / "records.jsonl"
    table_counts = {name: len(dataset["tables"][name]) for name in TABLES}
    public_file_facts = [file_fact(path) for path in public_files]
    return {
        "schema_name": "interlanguage-math-modular-backend-migration-receipt",
        "schema_version": "1.0.0",
        "migration_id": f"ag-bridge-id-units-01-{int(native_manifest['through_unit']):02d}-common-backend-v1",
        "migration_mode": "additive zero-copy adapter",
        "source": {
            "dataset_id": "algebraic-geometry-bridge-id-native-backend",
            "dataset_version": native_manifest.get("schema_version"),
            "schema_name": native_manifest.get("schema"),
            "record_schema_version": native_manifest.get("record_schema_version"),
            "scope": native_manifest.get("scope"),
            "through_unit": native_manifest.get("through_unit"),
            "record_count": native_manifest.get("record_count"),
            "tables": native_manifest.get("counts"),
            "manifest": file_fact(native_manifest_path),
            "records_jsonl": file_fact(native_records_path),
            "serialization": native_manifest.get("serialization"),
        },
        "target": {
            "dataset_id": dataset["dataset_id"],
            "dataset_version": dataset["dataset_version"],
            "schema_name": SCHEMA_NAME,
            "schema_version": SCHEMA_VERSION,
            "record_count": sum(table_counts.values()),
            "schema_sha256": contract_facts[COMMON_SCHEMA_PATH.relative_to(ROOT).as_posix()]["sha256"],
            "virtual_records_jsonl_sha256": sha256_bytes(virtual_bytes),
            "virtual_records_jsonl_bytes": len(virtual_bytes),
            "virtual_dataset_json_sha256": sha256_bytes(canonical_json_bytes(dataset, newline=b"")),
        },
        "transformation": {
            "adapter": "scripts/generate_common_backend_v1_receipts.py",
            "model_provenance": MODEL_PROVENANCE,
            "upstream_contract": {
                "handoff": {
                    "url": UPSTREAM_HANDOFF_URL,
                    **contract_facts[HANDOFF_PATH.relative_to(ROOT).as_posix()],
                },
                "migration_receipt_schema": {
                    "url": UPSTREAM_RECEIPT_SCHEMA_URL,
                    **contract_facts[RECEIPT_SCHEMA_PATH.relative_to(ROOT).as_posix()],
                },
                "backend_schema": {
                    "url": UPSTREAM_BACKEND_SCHEMA_URL,
                    **contract_facts[COMMON_SCHEMA_PATH.relative_to(ROOT).as_posix()],
                },
                "source_format_profile_schema": {
                    "url": UPSTREAM_PROFILE_SCHEMA_URL,
                    **contract_facts[PROFILE_SCHEMA_PATH.relative_to(ROOT).as_posix()],
                },
            },
            "identity_namespace": str(IDENTITY_NAMESPACE),
            "identity_formula": "UUIDv5(namespace, record_type|stable_key)",
            "native_id_policy": "every native stable_id is preserved verbatim as stable_key",
            "native_payload_policy": "complete native record preserved in ag-bridge.native-record extension",
            "segment_policy": "locale-neutral segment plus localized segment_variant",
            "source_profile_policy": "complete locally witnessed MediaWiki identities promoted to strict interlanguage.source-profile; all native provenance retained losslessly",
            "edition_commit_sha_ambiguity": "common schema requires 40-hex commit_sha for non-VCS editions; zero sentinel is explicitly qualified in extensions and native revision evidence remains authoritative",
            "reader_or_native_mutation": False,
        },
        "validation": {
            "result": "pass",
            "schema_draft": "2020-12",
            "strict_target_schema": True,
            "deterministic_double_replay": True,
            "global_id_uniqueness": True,
            "foreign_key_closure": True,
            "canonical_jsonl": True,
            "lossless_native_reverse": True,
            "native_reverse_bytes": len(reverse_bytes),
            "native_reverse_sha256": sha256_bytes(reverse_bytes),
            "foreign_keys_checked": fk_result["foreign_keys_checked"],
            "terminology_qa_receipt": terminology_fact,
        },
        "coverage": {
            "through_unit": native_manifest.get("through_unit"),
            "native_records": len(load_jsonl(native_records_path)),
            "native_ids_preserved": details["native_id_count"],
            "strict_source_profiles_eligible": details["profile_eligible"],
            "strict_source_profiles_bound": details["profile_bound"],
            "strict_source_profiles_missing": details["profile_missing_count"],
            "strict_source_profile_witness_files": details["profile_witness_file_count"],
        },
        "tables": table_counts,
        "materialization": {
            "mode": "zero-copy virtual adapter",
            "target_records_materialized": False,
            "native_backend_unchanged": True,
            "reader_unchanged": True,
            "virtual_stream_assembled_twice": True,
        },
        "public_artifacts": [
            {
                "repository": "Zenodo",
                "publication_uri": public_record_url,
                "doi": public_record_doi,
                "concept_doi": public_concept_doi,
                "files": public_file_facts,
                "receipt_public_readback_required_by_release_workflow": True,
            }
        ],
        "credentials_recorded": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--native-backend",
        type=Path,
        default=ROOT / "backend" / "units-01-07",
        help="Frozen native backend directory (default: backend/units-01-07)",
    )
    parser.add_argument(
        "--migration-output",
        type=Path,
        default=ROOT / "backend" / "common-backend-v1" / "MIGRATION_RECEIPT.json",
    )
    parser.add_argument(
        "--terminology-output",
        type=Path,
        default=ROOT / "qa" / "TERMINOLOGY_QA_RECEIPT.json",
    )
    parser.add_argument("--public-record-url")
    parser.add_argument("--public-record-doi")
    parser.add_argument("--public-concept-doi")
    parser.add_argument("--public-file", action="append", type=Path, default=[])
    parser.add_argument(
        "--preflight",
        action="store_true",
        help="Validate and report without writing receipts or requiring public identity/final QA",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    native_backend = args.native_backend.resolve()
    migration_output = args.migration_output.resolve()
    terminology_output = args.terminology_output.resolve()
    try:
        native_backend.relative_to(ROOT)
        migration_output.relative_to(ROOT)
        terminology_output.relative_to(ROOT)
    except ValueError as exc:
        raise SystemExit("Native backend and receipt outputs must stay inside this lane") from exc
    manifest_path = native_backend / "MANIFEST.json"
    records_path = native_backend / "records.jsonl"
    if not manifest_path.is_file() or not records_path.is_file():
        raise SystemExit(f"Frozen native backend boundary absent: {native_backend}")

    contract_facts = verify_contract()
    common_schema = load_json(COMMON_SCHEMA_PATH)
    profile_schema = load_json(PROFILE_SCHEMA_PATH)
    receipt_schema = load_json(RECEIPT_SCHEMA_PATH)
    native_manifest = load_json(manifest_path)
    native_records = load_jsonl(records_path)
    if len(native_records) != int(native_manifest["record_count"]):
        raise SystemExit("Native manifest record count does not match records.jsonl")
    if file_fact(records_path)["sha256"] != next(
        item["sha256"] for item in native_manifest["files"] if item["path"].endswith("/records.jsonl")
    ):
        raise SystemExit("Native records.jsonl hash does not match its manifest")

    profiles = authority_index(int(native_manifest["through_unit"]))
    dataset_a, details_a = build_dataset(native_records, native_manifest, profiles, profile_schema)
    dataset_b, details_b = build_dataset(native_records, native_manifest, profiles, profile_schema)
    if dataset_a != dataset_b or details_a != details_b:
        raise SystemExit("Common adapter double replay produced different objects")
    validate_dataset(dataset_a, common_schema)
    fk_result = validate_fk_closure(dataset_a)
    stream_a = virtual_jsonl(dataset_a)
    stream_b = virtual_jsonl(dataset_b)
    if stream_a != stream_b:
        raise SystemExit("Common virtual JSONL double replay produced different bytes")
    reverse = reverse_native_jsonl(dataset_a)
    native_bytes = records_path.read_bytes()
    if reverse != native_bytes:
        raise SystemExit(
            "Lossless reverse failed: "
            f"native={len(native_bytes)}/{sha256_bytes(native_bytes)} "
            f"reverse={len(reverse)}/{sha256_bytes(reverse)}"
        )
    if details_a["profile_missing_count"]:
        raise SystemExit(
            "Complete native MediaWiki identities lack local strict-profile witnesses: "
            + ", ".join(details_a["profile_missing_native_ids"][:20])
        )

    summary = {
        "status": "PASS",
        "native_records": len(native_records),
        "common_records": sum(len(dataset_a["tables"][name]) for name in TABLES),
        "virtual_bytes": len(stream_a),
        "virtual_sha256": sha256_bytes(stream_a),
        "reverse_sha256": sha256_bytes(reverse),
        "strict_profiles": details_a["profile_bound"],
        "strict_profile_witness_files": details_a["profile_witness_file_count"],
        "foreign_keys_checked": fk_result["foreign_keys_checked"],
    }
    if args.preflight:
        print(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2))
        return 0

    if not args.public_record_url:
        raise SystemExit("--public-record-url is required when emitting the frozen receipt")
    through = int(native_manifest["through_unit"])
    unit_label = f"01_{through:02d}"
    final_evidence_paths = [
        ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json",
        ROOT / "qa" / f"UNITS_{unit_label}_MACHINE_QA.json",
        ROOT / "qa" / f"UNITS_{unit_label}_VISUAL_QA.json",
        ROOT / "qa" / f"UNITS_{unit_label}_RESPONSIVE_QA.json",
        ROOT / "qa" / f"UNIT_{through:02d}_PROTECTED_SURFACES.json",
        ROOT / "qa" / f"UNITS_{unit_label}_BACKEND_QA.json",
        manifest_path,
    ]
    replay_evidence = receipt_evidence(final_evidence_paths)
    for path in final_evidence_paths[1:6]:
        if not status_is_pass(path):
            raise SystemExit(f"Final Unit {through} QA evidence is not PASS: {path}")
    term_receipt = terminology_receipt(
        int(native_manifest["through_unit"]),
        sha256_bytes(stream_a),
        sum(len(dataset_a["tables"][name]) for name in TABLES),
        replay_evidence,
    )
    assert_sanitized(term_receipt)
    term_bytes = canonical_pretty_bytes(term_receipt)
    terminology_fact = {
        "path": terminology_output.relative_to(ROOT).as_posix(),
        "bytes": len(term_bytes),
        "sha256": sha256_bytes(term_bytes),
        "result": "pass",
    }
    migration = migration_receipt(
        native_backend,
        native_manifest,
        contract_facts,
        dataset_a,
        details_a,
        stream_a,
        reverse,
        fk_result,
        terminology_fact,
        args.public_record_url,
        args.public_record_doi,
        args.public_concept_doi,
        [path.resolve() for path in args.public_file],
    )
    assert_sanitized(migration)
    receipt_validator = Draft202012Validator(receipt_schema, format_checker=FormatChecker())
    errors = sorted(receipt_validator.iter_errors(migration), key=lambda error: list(error.absolute_path))
    if errors:
        raise SystemExit(
            "Migration receipt schema validation failed:\n"
            + "\n".join(
                f"{'/'.join(str(item) for item in error.absolute_path)}: {error.message}"
                for error in errors[:20]
            )
        )

    terminology_output.parent.mkdir(parents=True, exist_ok=True)
    migration_output.parent.mkdir(parents=True, exist_ok=True)
    terminology_output.write_bytes(term_bytes)
    migration_bytes = canonical_pretty_bytes(migration)
    migration_output.write_bytes(migration_bytes)
    # Readback immediately and validate the exact bytes written.
    if terminology_output.read_bytes() != term_bytes or migration_output.read_bytes() != migration_bytes:
        raise SystemExit("Receipt write/readback mismatch")
    receipt_validator.validate(load_json(migration_output))
    print(
        json.dumps(
            {
                **summary,
                "terminology_receipt": file_fact(terminology_output),
                "migration_receipt": file_fact(migration_output),
            },
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
