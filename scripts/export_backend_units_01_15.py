#!/usr/bin/env python3
"""Export the deterministic cumulative native backend through Unit 15.

The frozen Units 1--12 backend is an append-only baseline. Every one of its
8,491 canonical JSONL records is carried forward with its original serialized
payload bytes. This exporter adds only the cumulative edition boundary,
reader/source structures for Units 13--15, typed exercise/solution projections,
component rights/assets, frozen authority artifacts, and deterministic reader
QA evidence.

The script is intentionally fail-closed. It will not write the Unit 15
backend until the cumulative reader build and all four named QA receipts exist,
pass, bind the final source bytes, and identify the through-Unit-15 reader.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "backend" / "units-01-12"
OUT = ROOT / "backend" / "units-01-15"

BUILD_RECEIPT_PATH = ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json"
MACHINE_QA_PATH = ROOT / "qa" / "UNITS_01_15_MACHINE_QA.json"
VISUAL_QA_PATH = ROOT / "qa" / "UNITS_01_15_VISUAL_QA.json"
RESPONSIVE_QA_PATH = ROOT / "qa" / "UNITS_01_15_RESPONSIVE_QA.json"
PROTECTED_QA_PATH = ROOT / "qa" / "UNIT_15_PROTECTED_SURFACES.json"
CORRECTIONS_PATH = ROOT / "00_control" / "CORRECTIONS.csv"
TERMINOLOGY_PATH = ROOT / "00_control" / "TERMINOLOGY.csv"

BASELINE_MANIFEST_SHA256 = "9c22a4eb308fd5d50cca9151f3617b833fe800749de8087038386af952a683ce"
BASELINE_RECORDS_SHA256 = "914d659bde3a32bce7f10b39f3f0ec12f852cffdfb6f83c12ca150d0ba1d3925"
BASELINE_SCHEMA_SHA256 = "4dbb0acff7e301420250f30cbe9457fd2df4469d820c82d3a30c7f09b7c2bc41"
BASELINE_RECORD_COUNT = 8491

WORKFLOW_ID = "workflow.o016-d100.algebraic-geometry-bridge-id"
BRENNER_RESOURCE = "resource.brenner.algebraische-kurven.2025-2026"
BRENNER_EDITION = "edition.brenner.algebraische-kurven.prefix-freeze.2026-08-21"
LOCAL_RESOURCE = "resource.algebraic-geometry-bridge-id.editorial-layer"
PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-12.2026-08-24"
CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-15.2026-08-24"
TEXT_RIGHTS = "rights.brenner-course-text.cc-by-sa-4.0"
EDITORIAL_RIGHTS = "rights.derivative-editorial.cc-by-sa-4.0"
MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."
BASE_SCHEMA = "ag-bridge-backend-record"
RECORD_SCHEMA_VERSION = "1.0.0"

SOURCE_FILES = [
    ROOT / "source" / "id-ID" / "frontmatter-units-01-15.md",
    ROOT / "source" / "id-ID" / "lecture-13.md",
    ROOT / "source" / "id-ID" / "worksheet-13.md",
    ROOT / "source" / "id-ID" / "worksheet-13-solutions.md",
    ROOT / "source" / "id-ID" / "media-credits-unit-13.md",
    ROOT / "source" / "id-ID" / "lecture-14.md",
    ROOT / "source" / "id-ID" / "worksheet-14.md",
    ROOT / "source" / "id-ID" / "worksheet-14-solutions.md",
    ROOT / "source" / "id-ID" / "media-credits-unit-14.md",
    ROOT / "source" / "id-ID" / "lecture-15.md",
    ROOT / "source" / "id-ID" / "worksheet-15.md",
    ROOT / "source" / "id-ID" / "worksheet-15-solutions.md",
    ROOT / "source" / "id-ID" / "media-credits-unit-15.md",
]

# Filled only after the three independent translation workers froze their
# source files.  These hashes are also independently replayed from the reader
# BUILD_RECEIPT input inventory before any output is written.
EXPECTED_SOURCE_SHA256 = {
    "source/id-ID/frontmatter-units-01-15.md": "d0a7f7d3d8c76789212caef445f39b15b61caed88a1662ca825ba4956b628cb5",
    "source/id-ID/lecture-13.md": "6b2c8a6aac3c80a3bf45cdb83db085e59f72f09bb7829528f2719c6b7af178fa",
    "source/id-ID/worksheet-13.md": "b9dbf3ee514c8e7d59bdf60ba4617cb0b8a38b5e299cc65af53cdd8e7f56adcd",
    "source/id-ID/worksheet-13-solutions.md": "787b24f616ac7823c88b7f45ea827df5bbdea34be111bb36822d542121e89774",
    "source/id-ID/media-credits-unit-13.md": "f5aa7d11bb7fd29860bdaec51fdb03790fdd6361e6f0ef2b4fbac72040de1341",
    "source/id-ID/lecture-14.md": "64b2519967638116cb3f98a2a200ad23efb5212e5c5c24b7f53e93ad2211f2d4",
    "source/id-ID/worksheet-14.md": "45dc11df386efc92ff537be1c53d7e2d9f16938be2fe5cd8eeb14eac347059cc",
    "source/id-ID/worksheet-14-solutions.md": "d64c25e2062d8a437465e7bb64d192e6d3ae347cdd6780c02e5146331cbe44dd",
    "source/id-ID/media-credits-unit-14.md": "b7960d839016c9f6705c1fdba68685a889c1af3261d2339190931e5f9f8b3dc3",
    "source/id-ID/lecture-15.md": "e1affd57e9f9d33f7e85a2b8c8fe993ecd821d1fff1075588f51dca2014763b4",
    "source/id-ID/worksheet-15.md": "feb6d9c38b669718c548608865f416eb1b3a03ac2d1ce6fac92cb5a288f48784",
    "source/id-ID/worksheet-15-solutions.md": "49fecc0631064c646bd8fe2707f2ab84f8e33f32e9c4f99028b4dc9f508ec948",
    "source/id-ID/media-credits-unit-15.md": "ccb29926735e5cdf47f628e2a66cf8c8e9017d64f3357a116e7e5abec3c41734",
}

TERMINOLOGY_CONCEPTS = {
    "AGT-0076": ("concept.multiplicative-system", "multiplicative system"),
    "AGT-0077": ("concept.idempotent-element", "idempotent element"),
    "AGT-0078": ("concept.product-ring", "product ring"),
    "AGT-0079": ("concept.connected-ring", "connected ring"),
    "AGT-0080": ("concept.clopen-set", "clopen set"),
    "AGT-0081": ("concept.saturated-multiplicative-system", "saturated multiplicative system"),
    "AGT-0082": ("concept.non-zero-divisor", "non-zero-divisor"),
    "AGT-0083": ("concept.algebraic-function", "algebraic function"),
    "AGT-0084": ("concept.regular-function", "regular function"),
    "AGT-0085": ("concept.structure-ring", "structure ring"),
    "AGT-0086": ("concept.section-ring", "section ring"),
    "AGT-0087": ("concept.structure-sheaf", "structure sheaf"),
    "AGT-0088": ("concept.presheaf", "presheaf"),
    "AGT-0089": ("concept.sheaf", "sheaf"),
    "AGT-0090": ("concept.restriction-map", "restriction map"),
    "AGT-0091": ("concept.minimal-prime-ideal", "minimal prime ideal"),
    "AGT-0092": ("concept.ultrafilter", "ultrafilter"),
    "AGT-0093": ("concept.holomorphic", "holomorphic"),
    "AGT-0094": ("concept.affine-variety", "affine variety"),
    "AGT-0095": ("concept.quasi-affine-variety", "quasi-affine variety"),
    "AGT-0096": ("concept.local-ring", "local ring"),
    "AGT-0097": ("concept.localization-at-prime-ideal", "localization at a prime ideal"),
    "AGT-0098": ("concept.topological-filter", "topological filter"),
    "AGT-0099": ("concept.neighborhood-filter", "neighborhood filter"),
    "AGT-0100": ("concept.directed-set", "directed set"),
    "AGT-0101": ("concept.directed-system", "directed system"),
    "AGT-0102": ("concept.colimit", "colimit"),
    "AGT-0103": ("concept.stalk", "stalk"),
    "AGT-0104": ("concept.function-field", "function field"),
    "AGT-0105": ("concept.colimit", "colimit"),
}

CORRECTION_TARGETS = {
    "AGC-CORR-0028": "br-ak-2025-2026-w13-ex-29",
    "AGC-CORR-0029": "br-ak-2025-2026-w13-sol-11",
    "AGC-CORR-0030": "br-ak-2025-2026-w13-sol-20",
    "AGC-CORR-0031": "br-ak-2025-2026-w14-sol-07",
    "AGC-CORR-0032": "br-ak-2025-2026-l15-def-08",
    "AGC-CORR-0033": "br-ak-2025-2026-w15-sol-19",
}

UNIT_SPEC: dict[int, dict[str, Any]] = {
    13: {
        "manifest": ROOT / "authority" / "wikiversity" / "unit-13" / "UNIT_AUTHORITY_MANIFEST.json",
        "map": ROOT / "authority" / "wikiversity" / "unit-13" / "ORDERED_EXERCISE_MAP.json",
        "rights": ROOT / "authority" / "RIGHTS-unit-13.csv",
        "closure": ROOT / "authority" / "ASSET_CLOSURE-unit-13.json",
        "exercise_count": 37,
        "solutions": (3, 6, 8, 9, 11, 14, 15, 17, 20, 21, 24, 27, 28, 31),
        "media_count": 2,
        "binary_surfaces": 4,
        "expected": {
            "manifest": "dc86b4d124c7e775fb635a1f9672a8b8faadc4ff2259b0779f7bac6302d18848",
            "map": "f954f09c996c8aa22f94ec826a1503b135a7b4fb9f9e0d5d6ff21f36a519e52a",
            "rights": "cdf370a6e3d7b80e137e6eb98a1180519b0cb97865ee39197de07c37e1a3c825",
            "closure": "771a8f09fd262838873e1390c43cae7da1f3989b74d8d2a7f67a856da9ea5e23",
        },
    },
    14: {
        "manifest": ROOT / "authority" / "wikiversity" / "unit-14" / "UNIT_AUTHORITY_MANIFEST.json",
        "map": ROOT / "authority" / "wikiversity" / "unit-14" / "ORDERED_EXERCISE_MAP.json",
        "rights": ROOT / "authority" / "RIGHTS-unit-14.csv",
        "closure": ROOT / "authority" / "ASSET_CLOSURE-unit-14.json",
        "exercise_count": 27,
        "solutions": (2, 7),
        "media_count": 1,
        "binary_surfaces": 1,
        "expected": {
            "manifest": "a63c3481d0a9cfa9b960f12c9bf0eec9a5d39cecfb61eddb8f9d96190e52e83e",
            "map": "0d223f7f3c56c4714736dfc6eb3dbd40dc8cd3cb30a05f66281a6f2b1b875dbe",
            "rights": "9c377f7c679ff0730bcd075201a4d587a322f004b118b0e31fc9c51b267e8973",
            "closure": "8fd50fae2515e6150e3d81c98573dd7bb204211e787d68405f7c3b03aab452d0",
        },
    },
    15: {
        "manifest": ROOT / "authority" / "wikiversity" / "unit-15" / "UNIT_AUTHORITY_MANIFEST.json",
        "map": ROOT / "authority" / "wikiversity" / "unit-15" / "ORDERED_EXERCISE_MAP.json",
        "rights": ROOT / "authority" / "RIGHTS-unit-15.csv",
        "closure": ROOT / "authority" / "ASSET_CLOSURE-unit-15.json",
        "exercise_count": 29,
        "solutions": (6, 9, 19, 22),
        "media_count": 1,
        "binary_surfaces": 2,
        "expected": {
            "manifest": "86e394725e766838f01eb035ca53044c4d3b85ff20eb99f8fecda9c2a0156425",
            "map": "3c8c41458f5418ff858a58748ba4b23bc0a8cb34d9c386c155806b4482760470",
            "rights": "28ed5e373e07f80cef981315733e53069bdcf8f14c4447d1d21c3fabb2b5f4d7",
            "closure": "cdf6371ba9e44f9828f166f8da5ecfe4b6141e0b9ba0c7c02a5dfba156fea0a4",
        },
    },
}

REQUIRED_CLASSES = {
    "artifact", "asset", "concept", "correction", "course", "edition",
    "exercise", "program", "qa_event", "relation", "resource", "rights",
    "segment", "solution", "term", "unit",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def text_digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_crlf(path: Path, text: str) -> None:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    path.write_bytes(normalized.replace("\n", "\r\n").encode("utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


for path, expected in (
    (BASELINE / "MANIFEST.json", BASELINE_MANIFEST_SHA256),
    (BASELINE / "records.jsonl", BASELINE_RECORDS_SHA256),
    (BASELINE / "record.schema.json", BASELINE_SCHEMA_SHA256),
):
    require(path.is_file(), f"Missing frozen Units 1--12 baseline file: {rel(path)}")
    require(digest(path) == expected, f"Frozen Units 1--12 baseline hash mismatch: {rel(path)}")

baseline_raw_by_id: dict[str, str] = {}
baseline_records: list[dict[str, Any]] = []
for raw_line in (BASELINE / "records.jsonl").read_text(encoding="utf-8").splitlines():
    record = json.loads(raw_line)
    require(canonical(record) == raw_line, f"Noncanonical baseline record: {record.get('stable_id')}")
    require(record["stable_id"] not in baseline_raw_by_id, f"Duplicate baseline stable ID: {record['stable_id']}")
    baseline_raw_by_id[record["stable_id"]] = raw_line
    baseline_records.append(record)
require(len(baseline_records) == BASELINE_RECORD_COUNT, "Frozen Units 1--12 record count changed")

for unit, spec in UNIT_SPEC.items():
    for key in ("manifest", "map", "rights", "closure"):
        path = spec[key]
        require(path.is_file(), f"Missing Unit {unit} authority input: {rel(path)}")
        require(digest(path) == spec["expected"][key], f"Unit {unit} {key} frozen hash mismatch")

build_receipt = json.loads(BUILD_RECEIPT_PATH.read_text(encoding="utf-8"))
require(build_receipt.get("schema") == "ag-bridge-build-receipt-v2", "Unexpected reader build receipt schema")
require(build_receipt.get("through_unit") == 15, "Reader build receipt is not through Unit 15")
require(MODEL_PROVENANCE in (ROOT / "source" / "id-ID" / "frontmatter-units-01-15.md").read_text(encoding="utf-8"), "Exact model provenance is absent from Unit 15 frontmatter")

receipt_inputs = {row["path"]: row for row in build_receipt.get("inputs", [])}
require(set(EXPECTED_SOURCE_SHA256) == {rel(path) for path in SOURCE_FILES}, "Final source-hash closure is incomplete or contains an unexpected path")
for path in SOURCE_FILES:
    path_key = rel(path)
    require(path.is_file(), f"Missing Unit 13--15 source input: {path_key}")
    actual = digest(path)
    require(actual == EXPECTED_SOURCE_SHA256[path_key], f"Final source hash changed: {path_key}")
    witness = receipt_inputs.get(path_key)
    require(witness is not None, f"Reader build receipt does not bind {path_key}")
    require(witness.get("bytes") == path.stat().st_size, f"Reader input byte count changed: {path_key}")
    require(witness.get("sha256") == actual, f"Reader input hash changed: {path_key}")

reader_outputs = {row["path"]: row for row in build_receipt.get("outputs", [])}
required_reader_outputs = (
    ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-15.pdf",
    ROOT / "build" / "reader-id" / "index.html",
)
for path in required_reader_outputs:
    key = rel(path)
    require(path.is_file(), f"Missing cumulative reader output: {key}")
    witness = reader_outputs.get(key)
    require(witness is not None, f"Reader build receipt does not bind {key}")
    require(witness.get("bytes") == path.stat().st_size, f"Reader output byte count changed: {key}")
    require(witness.get("sha256") == digest(path), f"Reader output hash changed: {key}")

qa_specs = [
    ("qa.units0115.machine", MACHINE_QA_PATH, "source_math_topology_build_accessibility", "status"),
    ("qa.units0115.visual", VISUAL_QA_PATH, "all_page_and_full_resolution_visual_layout", "result"),
    ("qa.units0115.responsive", RESPONSIVE_QA_PATH, "desktop_and_mobile_reader_reflow", "status"),
    ("qa.unit15.protected", PROTECTED_QA_PATH, "units_13_15_authority_formula_exercise_solution_media_fidelity", "status"),
]
qa_payloads: dict[str, dict[str, Any]] = {}
for stable_id, path, _kind, status_key in qa_specs:
    require(path.is_file(), f"Missing required reader QA receipt: {rel(path)}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    require(payload.get(status_key) == "PASS", f"Reader QA did not pass: {rel(path)}")
    if path != PROTECTED_QA_PATH:
        require(payload.get("through_unit") == 15, f"Reader QA is not through Unit 15: {rel(path)}")
    else:
        require(payload.get("unit") == 15, "Protected-surface receipt is not the Unit 15 release boundary")
    qa_payloads[stable_id] = payload

timestamp = build_receipt["built_utc"]


def make_record(
    entity_class: str,
    stable_id: str,
    *,
    source_local_id: str | None = None,
    parent_id: str | None = None,
    order: int | None = None,
    path: str | None = None,
    resource_id: str | None = None,
    edition_id: str | None = None,
    source_locator: str | None = None,
    content_sha256: str | None = None,
    language: str = "und",
    translation_state: str = "source_frozen",
    provenance: dict[str, Any] | None = None,
    concept_ids: list[str] | None = None,
    prerequisite_ids: list[str] | None = None,
    rights_id: str | None = None,
    status: str = "active",
    supersedes: str | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    full_provenance = {"model_provenance": MODEL_PROVENANCE}
    full_provenance.update(provenance or {})
    return {
        "schema": BASE_SCHEMA,
        "schema_version": RECORD_SCHEMA_VERSION,
        "entity_class": entity_class,
        "stable_id": stable_id,
        "source_local_id": source_local_id,
        "parent_id": parent_id,
        "order": order,
        "path": path,
        "resource_id": resource_id,
        "edition_id": edition_id,
        "source_locator": source_locator,
        "content_sha256": content_sha256,
        "language": language,
        "translation_state": translation_state,
        "provenance": full_provenance,
        "concept_ids": sorted(set(concept_ids or [])),
        "prerequisite_ids": sorted(set(prerequisite_ids or [])),
        "rights_id": rights_id,
        "status": status,
        "timestamp": timestamp,
        "responsible_workflow": WORKFLOW_ID,
        "supersedes": supersedes,
        "payload": payload or {},
    }


records: list[dict[str, Any]] = list(baseline_records)
new_records: list[dict[str, Any]] = []


def add(record: dict[str, Any]) -> None:
    records.append(record)
    new_records.append(record)


authority_manifests: dict[int, dict[str, Any]] = {}
exercise_maps: dict[int, dict[str, Any]] = {}
solution_entries: dict[int, dict[int, dict[str, Any]]] = {}
rights_rows: dict[int, list[dict[str, str]]] = {}
asset_closures: dict[int, dict[str, Any]] = {}
for unit, spec in UNIT_SPEC.items():
    authority_manifests[unit] = json.loads(spec["manifest"].read_text(encoding="utf-8"))
    exercise_maps[unit] = json.loads(spec["map"].read_text(encoding="utf-8"))
    rights_rows[unit] = read_csv(spec["rights"])
    asset_closures[unit] = json.loads(spec["closure"].read_text(encoding="utf-8"))
    manifest = authority_manifests[unit]
    exercise_map = exercise_maps[unit]
    require(manifest.get("unit_number") == unit, f"Unit {unit} authority manifest identity mismatch")
    require(exercise_map.get("unit") == unit, f"Unit {unit} exercise map identity mismatch")
    require(exercise_map.get("exercise_count") == spec["exercise_count"], f"Unit {unit} exercise count mismatch")
    require(exercise_map.get("solution_count") == len(spec["solutions"]), f"Unit {unit} solution count mismatch")
    public = {int(row["exercise_number"]): row for row in exercise_map["entries"] if row.get("has_public_solution")}
    require(tuple(sorted(public)) == spec["solutions"], f"Unit {unit} public-solution identity mismatch")
    solution_entries[unit] = public
    require(len(rights_rows[unit]) == spec["media_count"], f"Unit {unit} rights row count mismatch")
    require(asset_closures[unit].get("unit") == unit, f"Unit {unit} asset closure identity mismatch")
    require(asset_closures[unit].get("reader_media_positions") == spec["media_count"], f"Unit {unit} media-position count mismatch")
    require(asset_closures[unit].get("unique_local_assets") == spec["binary_surfaces"], f"Unit {unit} local-asset count mismatch")

add(
    make_record(
        "edition",
        CUMULATIVE_EDITION,
        source_local_id="units-01-15",
        parent_id=LOCAL_RESOURCE,
        resource_id=LOCAL_RESOURCE,
        edition_id=CUMULATIVE_EDITION,
        source_locator=rel(BUILD_RECEIPT_PATH),
        content_sha256=digest(BUILD_RECEIPT_PATH),
        language="id-ID",
        translation_state="built",
        rights_id=EDITORIAL_RIGHTS,
        supersedes=PREVIOUS_EDITION,
        provenance={
            "units_01_12_baseline_manifest_sha256": BASELINE_MANIFEST_SHA256,
            "authority": {
                str(unit): {
                    key: digest(spec[key]) for key in ("manifest", "map", "rights", "closure")
                }
                for unit, spec in UNIT_SPEC.items()
            },
        },
        payload={
            "title": build_receipt["title"],
            "through_unit": 15,
            "source_edition_id": BRENNER_EDITION,
            "reader_outputs": build_receipt["outputs"],
            "build_receipt_sha256": digest(BUILD_RECEIPT_PATH),
            "translation_change_notice": True,
            "non_endorsement": True,
            "model_provenance": MODEL_PROVENANCE,
        },
    )
)

terminology_rows = {
    row["term_id"]: row
    for row in read_csv(TERMINOLOGY_PATH)
    if row.get("term_id") in TERMINOLOGY_CONCEPTS
}
require(set(terminology_rows) == set(TERMINOLOGY_CONCEPTS), "Units 13--15 terminology ledger closure mismatch")

correction_rows = {
    row["correction_id"]: row
    for row in read_csv(CORRECTIONS_PATH)
    if row.get("correction_id") in CORRECTION_TARGETS
}
require(set(correction_rows) == set(CORRECTION_TARGETS), "Units 13--15 correction ledger closure mismatch")

new_concept_records: list[dict[str, Any]] = []
new_term_records: list[dict[str, Any]] = []
known_concept_ids = {
    record["stable_id"] for record in records if record["entity_class"] == "concept"
}
for term_id in sorted(TERMINOLOGY_CONCEPTS):
    row = terminology_rows[term_id]
    concept_id, canonical_label = TERMINOLOGY_CONCEPTS[term_id]
    row_sha256 = text_digest(canonical(row))
    concept = make_record(
        "concept",
        concept_id,
        source_local_id=row["source_term"],
        resource_id=BRENNER_RESOURCE,
        edition_id=CUMULATIVE_EDITION,
        source_locator=rel(TERMINOLOGY_PATH),
        content_sha256=row_sha256,
        language="und",
        translation_state="translated",
        provenance={"terminology_row_id": term_id},
        rights_id=EDITORIAL_RIGHTS,
        status=row["status"],
        payload={"canonical_label": canonical_label},
    )
    if concept_id not in known_concept_ids:
        add(concept)
        new_concept_records.append(concept)
        known_concept_ids.add(concept_id)

    term = make_record(
        "term",
        f"term.{term_id.casefold()}.id-id",
        source_local_id=term_id,
        parent_id=concept_id,
        resource_id=BRENNER_RESOURCE,
        edition_id=CUMULATIVE_EDITION,
        source_locator=rel(TERMINOLOGY_PATH),
        content_sha256=row_sha256,
        language=row["target_language"],
        translation_state="translated",
        provenance={"terminology_row_id": term_id},
        concept_ids=[concept_id],
        rights_id=EDITORIAL_RIGHTS,
        status=row["status"],
        payload={
            "preferred_target": row["preferred_target"],
            "rationale": row["rationale"],
            "rejected_or_variant": row["rejected_or_variant"],
            "scope": row["scope"],
            "source_language": row["source_language"],
            "source_term": row["source_term"],
        },
    )
    add(term)
    new_term_records.append(term)

term_needles = [
    (record["payload"].get("preferred_target", "").casefold(), record["parent_id"])
    for record in records
    if record["entity_class"] == "term"
    and record["payload"].get("preferred_target")
    and record.get("parent_id")
]


def concept_ids_for(content: str) -> list[str]:
    low = content.casefold()
    return sorted({concept_id for needle, concept_id in term_needles if needle in low})


heading_re = re.compile(r"^(#{1,6})\s+(.*?)\s+\{#([^}]+)\}\s*$")


def strip_yaml(lines: list[str]) -> tuple[list[str], dict[str, str]]:
    if not lines or lines[0].strip() != "---":
        return lines, {}
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration as exc:
        raise SystemExit("Unclosed source front matter") from exc
    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            metadata[match.group(1)] = match.group(2).strip().strip('"')
    return ["" for _ in range(end + 1)] + lines[end + 1 :], metadata


def classify_unit(identifier: str, title: str) -> str:
    low = title.casefold()
    if re.search(r"-sol-\d+$", identifier) or low.startswith("solusi soal"):
        return "solution"
    if re.search(r"-w\d{2}-ex-\d+$", identifier):
        return "exercise"
    if re.search(r"-l\d{2}-ex-\d+$", identifier):
        return "example"
    if "-def-" in identifier:
        return "definition"
    if "-lem-" in identifier and identifier.endswith("-proof"):
        return "proof"
    if "-lem-" in identifier:
        return "lemma"
    if any(token in identifier for token in ("-thm-", "-prop-")) and identifier.endswith("-proof"):
        return "proof"
    if "-thm-" in identifier:
        return "theorem"
    if "-prop-" in identifier:
        return "proposition"
    if identifier.endswith(("-practice", "-submission", "-submit")):
        return "exercise_group"
    if identifier.startswith("agc-media-credits"):
        return "credits"
    if re.search(r"-s\d+$", identifier) or identifier.startswith("agc-front-"):
        return "section"
    if re.search(r"-(?:l|w)\d{2}$", identifier) or identifier.endswith("-solutions"):
        return "unit"
    return "section"


def compact_upstream(row: dict[str, Any]) -> dict[str, Any]:
    return {
        key: row[key]
        for key in (
            "title", "pageid", "revid", "parentid", "timestamp",
            "mediawiki_sha1", "oldid_url", "xml_file", "xml_bytes",
            "xml_sha256", "html_file", "html_bytes", "html_sha256",
        )
        if key in row
    }


def source_unit_number(source_path: Path) -> int | None:
    match = re.search(r"(?:lecture|worksheet|media-credits-unit)-(\d{2})", source_path.name)
    return int(match.group(1)) if match else None


def source_provenance(source_path: Path, metadata: dict[str, str], identifier: str) -> dict[str, Any]:
    unit = source_unit_number(source_path)
    result: dict[str, Any] = {
        "source_edition_id": None if source_path.name.startswith(("frontmatter-", "media-credits-")) else BRENNER_EDITION,
        "source_file": {"path": rel(source_path), "bytes": source_path.stat().st_size, "sha256": digest(source_path)},
    }
    if unit is None:
        result["authority_units"] = {
            str(number): {"manifest_path": rel(spec["manifest"]), "manifest_sha256": digest(spec["manifest"])}
            for number, spec in UNIT_SPEC.items()
        }
        return result

    spec = UNIT_SPEC[unit]
    result["authority"] = {
        "unit": unit,
        "manifest_path": rel(spec["manifest"]),
        "manifest_sha256": digest(spec["manifest"]),
        "exercise_map_path": rel(spec["map"]),
        "exercise_map_sha256": digest(spec["map"]),
        "rights_path": rel(spec["rights"]),
        "rights_sha256": digest(spec["rights"]),
        "asset_closure_path": rel(spec["closure"]),
        "asset_closure_sha256": digest(spec["closure"]),
    }
    if source_path.name == f"lecture-{unit:02d}.md":
        result["upstream"] = compact_upstream(authority_manifests[unit]["lecture"])
    elif source_path.name == f"worksheet-{unit:02d}.md":
        result["upstream"] = compact_upstream(authority_manifests[unit]["worksheet"])
    elif source_path.name == f"worksheet-{unit:02d}-solutions.md":
        match = re.search(r"-sol-(\d+)$", identifier)
        result["exercise_solution_map"] = {
            "path": rel(spec["map"]),
            "sha256": digest(spec["map"]),
            "worksheet_revid": exercise_maps[unit]["worksheet"]["revid"],
        }
        result["upstream"] = compact_upstream(solution_entries[unit][int(match.group(1))]) if match else compact_upstream(exercise_maps[unit]["worksheet"])
    elif source_path.name.startswith("media-credits-"):
        result["component_rights"] = {"path": rel(spec["rights"]), "sha256": digest(spec["rights"])}
    else:
        result["upstream"] = {
            key: metadata[key]
            for key in ("upstream_title", "upstream_pageid", "upstream_revid", "upstream_timestamp", "upstream_mediawiki_sha1", "source_url")
            if key in metadata
        }
    return result


all_new_units: list[dict[str, Any]] = []
all_new_segments: list[dict[str, Any]] = []
image_parent_by_path: dict[str, str] = {}
global_unit_order = max(record["order"] or 0 for record in baseline_records if record["entity_class"] == "unit")
global_segment_order = max(record["order"] or 0 for record in baseline_records if record["entity_class"] == "segment")
global_segment_counter: defaultdict[str, int] = defaultdict(int)

for source_path in SOURCE_FILES:
    original_lines = source_path.read_text(encoding="utf-8").splitlines()
    lines, metadata = strip_yaml(original_lines)
    heading_rows: list[tuple[int, int, str, str]] = []
    for index, line in enumerate(lines):
        match = heading_re.match(line)
        if match:
            heading_rows.append((index, len(match.group(1)), match.group(2), match.group(3)))
    require(heading_rows, f"No stable heading IDs in {rel(source_path)}")

    stack: list[tuple[int, str]] = []
    for heading_position, (line_index, level, title, identifier) in enumerate(heading_rows):
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent_id = stack[-1][1] if stack else CUMULATIVE_EDITION
        stack.append((level, identifier))
        next_boundary = len(lines)
        for next_index, next_level, _, _ in heading_rows[heading_position + 1 :]:
            if next_level <= level:
                next_boundary = next_index
                break
        region = "\n".join(lines[line_index:next_boundary]).strip() + "\n"
        global_unit_order += 1
        editorial = source_path.name.startswith(("frontmatter-", "media-credits-"))
        source_resource = LOCAL_RESOURCE if editorial else BRENNER_RESOURCE
        unit_record = make_record(
            "unit",
            identifier,
            source_local_id=metadata.get("upstream_title") if level == 1 else identifier,
            parent_id=parent_id,
            order=global_unit_order,
            path=f"{rel(source_path)}#{identifier}",
            resource_id=source_resource,
            edition_id=CUMULATIVE_EDITION,
            source_locator=f"{rel(source_path)}:{line_index + 1}",
            content_sha256=text_digest(region),
            language="id-ID",
            translation_state="built",
            provenance=source_provenance(source_path, metadata, identifier),
            concept_ids=concept_ids_for(region),
            rights_id=EDITORIAL_RIGHTS if editorial else TEXT_RIGHTS,
            payload={
                "unit_type": classify_unit(identifier, title),
                "heading_level": level,
                "title_markdown": title,
                "source_file_sha256": digest(source_path),
            },
        )
        add(unit_record)
        all_new_units.append(unit_record)

    active_id = CUMULATIVE_EDITION
    block: list[tuple[int, str]] = []

    def flush_block() -> None:
        nonlocal_block = list(block)
        block.clear()
        if not nonlocal_block:
            return
        first_line = nonlocal_block[0][0]
        content = "\n".join(line for _, line in nonlocal_block).strip()
        if not content or (content.startswith("<!--") and content.endswith("-->")):
            return
        global_segment_counter[active_id] += 1
        editorial = source_path.name.startswith(("frontmatter-", "media-credits-"))
        source_resource = LOCAL_RESOURCE if editorial else BRENNER_RESOURCE
        global global_segment_order
        global_segment_order += 1
        segment_id = f"{active_id}.seg-{global_segment_counter[active_id]:03d}"
        if content.startswith("!["):
            segment_type = "figure_reference"
        elif content.startswith("$$") or content.startswith("\\["):
            segment_type = "display_math"
        elif content.startswith(("- ", "1. ", "2. ", "3. ")):
            segment_type = "list"
        elif content.startswith("\\begin") or content.startswith("\\end"):
            segment_type = "raw_tex"
        else:
            segment_type = "prose"
        segment = make_record(
            "segment",
            segment_id,
            parent_id=active_id,
            order=global_segment_order,
            path=f"{rel(source_path)}:{first_line}",
            resource_id=source_resource,
            edition_id=CUMULATIVE_EDITION,
            source_locator=f"{rel(source_path)}:{first_line}",
            content_sha256=text_digest(content),
            language="id-ID",
            translation_state="built",
            provenance=source_provenance(source_path, metadata, active_id),
            concept_ids=concept_ids_for(content),
            rights_id=EDITORIAL_RIGHTS if editorial else TEXT_RIGHTS,
            payload={"segment_type": segment_type, "markdown": content},
        )
        add(segment)
        all_new_segments.append(segment)
        image_match = re.fullmatch(r"!\[[^\]]*\]\(([^)]+)\)", content)
        if image_match:
            require(image_match.group(1) not in image_parent_by_path, f"Duplicate reader image path {image_match.group(1)}")
            image_parent_by_path[image_match.group(1)] = active_id

    for line_number, line in enumerate(lines, start=1):
        heading = heading_re.match(line)
        if heading:
            flush_block()
            active_id = heading.group(3)
        elif not line.strip():
            flush_block()
        else:
            block.append((line_number, line))
    flush_block()

# Close exercises and solutions against the frozen ordered maps before adding
# typed projections.
for unit, spec in UNIT_SPEC.items():
    exercise_ids = {
        row["stable_id"] for row in all_new_units
        if row["payload"].get("unit_type") == "exercise" and f"-w{unit:02d}-ex-" in row["stable_id"]
    }
    solution_ids = {
        row["stable_id"] for row in all_new_units
        if row["payload"].get("unit_type") == "solution" and f"-w{unit:02d}-sol-" in row["stable_id"]
    }
    expected_exercises = {f"br-ak-2025-2026-w{unit:02d}-ex-{number:02d}" for number in range(1, spec["exercise_count"] + 1)}
    expected_solutions = {f"br-ak-2025-2026-w{unit:02d}-sol-{number:02d}" for number in spec["solutions"]}
    require(exercise_ids == expected_exercises, f"Unit {unit} translated exercise stable-ID closure mismatch")
    require(solution_ids == expected_solutions, f"Unit {unit} translated solution stable-ID closure mismatch")

# Component rights and assets are distinct records; SVG reader assets retain
# their raster PDF companion inside the same asset record.
asset_records: list[dict[str, Any]] = []
for unit, rows in rights_rows.items():
    for row in rows:
        local_path = ROOT / row["local_path"]
        require(local_path.is_file(), f"Missing Unit {unit} reader asset: {row['local_path']}")
        require(local_path.stat().st_size == int(row["local_bytes"]), f"Unit {unit} asset byte count mismatch: {row['asset_id']}")
        require(digest(local_path) == row["local_sha256"], f"Unit {unit} asset hash mismatch: {row['asset_id']}")
        if row["pdf_local_path"]:
            companion_path = ROOT / row["pdf_local_path"]
            require(companion_path.is_file(), f"Missing Unit {unit} PDF companion: {row['pdf_local_path']}")
            require(companion_path.stat().st_size == int(row["pdf_local_bytes"]), f"Unit {unit} companion byte count mismatch: {row['asset_id']}")
            require(digest(companion_path) == row["pdf_local_sha256"], f"Unit {unit} companion hash mismatch: {row['asset_id']}")
        require(row["local_path"] in image_parent_by_path, f"Unit {unit} asset has no reader image position: {row['asset_id']}")
        rights_id = f"rights.{row['asset_id']}"
        add(
            make_record(
                "rights",
                rights_id,
                source_local_id=row["metadata_title"],
                resource_id=BRENNER_RESOURCE,
                edition_id=CUMULATIVE_EDITION,
                source_locator=row["description_url"],
                content_sha256=row["local_sha256"],
                provenance={
                    "unit": unit,
                    "rights_path": rel(UNIT_SPEC[unit]["rights"]),
                    "rights_sha256": digest(UNIT_SPEC[unit]["rights"]),
                },
                payload={
                    "license": row["license_short"],
                    "license_url": row["license_url"] or None,
                    "usage_terms": row["usage_terms"] or None,
                    "creator_or_artist": row["artist"] or row["uploader"],
                    "uploader": row["uploader"],
                    "credit": row["credit"],
                    "attribution_required": row["attribution_required"].lower() == "true",
                    "scope": row["asset_id"],
                },
            )
        )
        asset = make_record(
            "asset",
            row["asset_id"],
            source_local_id=row["resource_title"],
            parent_id=image_parent_by_path[row["local_path"]],
            order=int(row["reader_order"]),
            path=row["local_path"],
            resource_id=BRENNER_RESOURCE,
            edition_id=CUMULATIVE_EDITION,
            source_locator=row["description_url"],
            content_sha256=row["local_sha256"],
            translation_state="built",
            provenance={
                "unit": unit,
                "asset_closure_path": rel(UNIT_SPEC[unit]["closure"]),
                "asset_closure_sha256": digest(UNIT_SPEC[unit]["closure"]),
            },
            rights_id=rights_id,
            payload={
                "caption_id": row["asset_id"],
                "selected_form": row["selected_form"],
                "bytes": int(row["local_bytes"]),
                "width": int(row["local_width"]),
                "height": int(row["local_height"]),
                "mime": row["mime"],
                "source_original_url": row["original_url"],
                "selected_url": row["selected_url"],
                "pdf_companion": (
                    {"path": row["pdf_local_path"], "bytes": int(row["pdf_local_bytes"]), "sha256": row["pdf_local_sha256"]}
                    if row["pdf_local_path"] else None
                ),
            },
        )
        add(asset)
        asset_records.append(asset)

typed_records: list[dict[str, Any]] = []
for unit_record in all_new_units:
    unit_type = unit_record["payload"].get("unit_type")
    if unit_type not in {"exercise", "solution"}:
        continue
    number_match = re.search(r"-(?:ex|sol)-(\d+)$", unit_record["stable_id"])
    require(number_match is not None, f"Typed record has no number: {unit_record['stable_id']}")
    number = int(number_match.group(1))
    unit_match = re.search(r"-w(\d{2})-", unit_record["stable_id"])
    require(unit_match is not None, f"Typed record has no worksheet unit: {unit_record['stable_id']}")
    unit_number = int(unit_match.group(1))
    provenance: dict[str, Any] = {
        "indexed_unit_id": unit_record["stable_id"],
        "indexed_unit_record_sha256": text_digest(canonical(unit_record)),
        "compatibility_projection": True,
        "source_provenance": unit_record["provenance"],
    }
    if unit_type == "solution":
        provenance["exercise_solution_authority"] = {
            "map_path": rel(UNIT_SPEC[unit_number]["map"]),
            "map_sha256": digest(UNIT_SPEC[unit_number]["map"]),
            "upstream": compact_upstream(solution_entries[unit_number][number]),
        }
    typed = make_record(
        unit_type,
        f"{unit_type}.{unit_record['stable_id']}",
        source_local_id=unit_record["source_local_id"],
        parent_id=unit_record["stable_id"],
        order=number,
        path=unit_record["path"],
        resource_id=unit_record["resource_id"],
        edition_id=CUMULATIVE_EDITION,
        source_locator=unit_record["source_locator"],
        content_sha256=unit_record["content_sha256"],
        language="id-ID",
        translation_state="built",
        provenance=provenance,
        concept_ids=unit_record["concept_ids"],
        rights_id=unit_record["rights_id"],
        payload={"unit_id": unit_record["stable_id"], "exercise_number": number, "family": unit_type},
    )
    add(typed)
    typed_records.append(typed)

new_correction_records: list[dict[str, Any]] = []
source_unit_ids = {record["stable_id"] for record in all_new_units}
require(set(CORRECTION_TARGETS.values()) <= source_unit_ids, "A Units 13--15 correction target is absent from the translated source IDs")
for correction_id in sorted(CORRECTION_TARGETS):
    row = correction_rows[correction_id]
    affected_id = CORRECTION_TARGETS[correction_id]
    correction = make_record(
        "correction",
        f"correction.{correction_id.casefold()}",
        source_local_id=correction_id,
        resource_id=BRENNER_RESOURCE if correction_id.startswith("AGC-CORR-") else LOCAL_RESOURCE,
        edition_id=CUMULATIVE_EDITION,
        source_locator=rel(CORRECTIONS_PATH),
        content_sha256=text_digest(canonical(row)),
        language="id-ID",
        translation_state="built",
        provenance={"authority_identity": row["authority_identity"]},
        rights_id=EDITORIAL_RIGHTS,
        status=row["status"],
        payload={
            "affected_unit_ids": [affected_id],
            "authority_observation": row["authority_observation"],
            "kind": row["kind"],
            "mathematical_effect": row["mathematical_effect"],
            "publication_gate": row["status"],
            "scope": row["scope"],
            "target_action": row["target_action"],
        },
    )
    add(correction)
    new_correction_records.append(correction)

qa_records: list[dict[str, Any]] = []
for stable_id, path, qa_kind, _status_key in qa_specs:
    qa_record = make_record(
        "qa_event",
        stable_id,
        parent_id=CUMULATIVE_EDITION,
        resource_id=LOCAL_RESOURCE,
        edition_id=CUMULATIVE_EDITION,
        source_locator=rel(path),
        content_sha256=digest(path),
        translation_state="built",
        rights_id=EDITORIAL_RIGHTS,
        status="passed",
        payload={"qa_kind": qa_kind, "result": qa_payloads[stable_id]},
    )
    add(qa_record)
    qa_records.append(qa_record)

authority_paths = [spec[key] for unit, spec in UNIT_SPEC.items() for key in ("manifest", "map", "rights", "closure")]
artifact_paths = [
    ROOT / "build" / "reader-id" / "index.html",
    ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-15.pdf",
    BUILD_RECEIPT_PATH,
    MACHINE_QA_PATH,
    VISUAL_QA_PATH,
    RESPONSIVE_QA_PATH,
    PROTECTED_QA_PATH,
    *authority_paths,
]
artifact_records: list[dict[str, Any]] = []
for number, artifact_path in enumerate(artifact_paths, start=1):
    artifact_id = f"artifact.units0115.{number:02d}.{artifact_path.name.casefold().replace('_', '-').replace('.', '-')}"
    artifact = make_record(
        "artifact",
        artifact_id,
        parent_id=CUMULATIVE_EDITION,
        order=number,
        path=rel(artifact_path),
        resource_id=LOCAL_RESOURCE,
        edition_id=CUMULATIVE_EDITION,
        source_locator=rel(artifact_path),
        content_sha256=digest(artifact_path),
        language="id-ID" if artifact_path.suffix in {".html", ".pdf"} else "und",
        translation_state="built",
        rights_id=EDITORIAL_RIGHTS,
        payload={
            "bytes": artifact_path.stat().st_size,
            "media_type": {".html": "text/html", ".pdf": "application/pdf", ".json": "application/json", ".csv": "text/csv"}.get(artifact_path.suffix, "application/octet-stream"),
            "build_receipt": rel(BUILD_RECEIPT_PATH),
        },
    )
    add(artifact)
    artifact_records.append(artifact)

relation_counter = 0


def add_relation(relation_type: str, subject_id: str, object_id: str, *, source_locator: str, payload: dict[str, Any] | None = None) -> None:
    global relation_counter
    relation_counter += 1
    add(
        make_record(
            "relation",
            f"relation.units0115.{relation_counter:04d}",
            order=relation_counter,
            resource_id=LOCAL_RESOURCE,
            edition_id=CUMULATIVE_EDITION,
            source_locator=source_locator,
            content_sha256=text_digest(f"{relation_type}\u241f{subject_id}\u241f{object_id}"),
            translation_state="built",
            rights_id=EDITORIAL_RIGHTS,
            payload={"relation_type": relation_type, "subject_id": subject_id, "object_id": object_id, **(payload or {})},
        )
    )


add_relation("extends", CUMULATIVE_EDITION, PREVIOUS_EDITION, source_locator=rel(BUILD_RECEIPT_PATH))
add_relation("derived_from", CUMULATIVE_EDITION, BRENNER_EDITION, source_locator=rel(BUILD_RECEIPT_PATH))
for term in new_term_records:
    add_relation("labels", term["stable_id"], term["parent_id"], source_locator=rel(TERMINOLOGY_PATH))
for correction in new_correction_records:
    correction_id = correction["source_local_id"]
    relation_type = "corrects" if correction_id.startswith("AGC-CORR-") else "adapts"
    add_relation(relation_type, correction["stable_id"], CORRECTION_TARGETS[correction_id], source_locator=rel(CORRECTIONS_PATH))
for unit_record in all_new_units:
    add_relation("contains", unit_record["parent_id"], unit_record["stable_id"], source_locator=unit_record["source_locator"])
    for concept_id in unit_record["concept_ids"]:
        add_relation("uses_concept", unit_record["stable_id"], concept_id, source_locator=unit_record["source_locator"])
for previous, following in zip(all_new_units, all_new_units[1:]):
    add_relation("precedes", previous["stable_id"], following["stable_id"], source_locator=following["source_locator"])
for unit, public in solution_entries.items():
    for number in sorted(public):
        add_relation("solves", f"br-ak-2025-2026-w{unit:02d}-sol-{number:02d}", f"br-ak-2025-2026-w{unit:02d}-ex-{number:02d}", source_locator=rel(UNIT_SPEC[unit]["map"]))
        add_relation("solves", f"solution.br-ak-2025-2026-w{unit:02d}-sol-{number:02d}", f"exercise.br-ak-2025-2026-w{unit:02d}-ex-{number:02d}", source_locator=rel(UNIT_SPEC[unit]["map"]), payload={"typed_family_projection": True})
for asset in asset_records:
    add_relation("illustrates", asset["stable_id"], asset["parent_id"], source_locator=asset["source_locator"])
for typed in typed_records:
    add_relation("indexes_unit", typed["stable_id"], typed["parent_id"], source_locator=typed["source_locator"])
for qa_record in qa_records:
    add_relation("validated_by", CUMULATIVE_EDITION, qa_record["stable_id"], source_locator=qa_record["source_locator"])
for artifact in artifact_records:
    add_relation("emits", CUMULATIVE_EDITION, artifact["stable_id"], source_locator=rel(BUILD_RECEIPT_PATH))

ids = [record["stable_id"] for record in records]
duplicates = sorted(stable_id for stable_id, count in Counter(ids).items() if count > 1)
require(not duplicates, f"Duplicate stable IDs: {duplicates}")
require({record["entity_class"] for record in records} == REQUIRED_CLASSES, "Required entity-family closure mismatch")
id_set = set(ids)
for record in records:
    if record["parent_id"] is not None:
        require(record["parent_id"] in id_set, f"Missing parent {record['parent_id']} for {record['stable_id']}")
    for field in ("resource_id", "edition_id", "rights_id"):
        endpoint = record.get(field)
        if endpoint is not None:
            require(endpoint in id_set, f"Missing {field} endpoint {endpoint} for {record['stable_id']}")
    for concept_id in record.get("concept_ids", []):
        require(concept_id in id_set, f"Missing concept endpoint {concept_id} for {record['stable_id']}")
    if record["entity_class"] == "relation":
        require(record["payload"].get("subject_id") in id_set, f"Missing relation subject for {record['stable_id']}")
        require(record["payload"].get("object_id") in id_set, f"Missing relation object for {record['stable_id']}")

schema = json.loads((BASELINE / "record.schema.json").read_text(encoding="utf-8"))
schema["$id"] = "https://example.invalid/algebraic-geometry-bridge/backend-record-units-01-15-v1.schema.json"
schema["title"] = "Algebraic Geometry Bridge cumulative backend record through Units 1--15"
schema["properties"]["entity_class"]["enum"] = sorted(REQUIRED_CLASSES)

records_sorted = sorted(records, key=lambda row: (row["entity_class"], row["stable_id"]))


def serialized_record(record: dict[str, Any]) -> str:
    return baseline_raw_by_id.get(record["stable_id"], canonical(record))


serialized_lines = [serialized_record(record) for record in records_sorted]
require(serialized_lines == [serialized_record(record) for record in records_sorted], "Nondeterministic in-memory serialization")
require(all(serialized_record(record) == baseline_raw_by_id[record["stable_id"]] for record in baseline_records), "Units 1--12 record bytes changed in memory")

OUT.mkdir(parents=True, exist_ok=True)
schema_path = OUT / "record.schema.json"
write_crlf(schema_path, json.dumps(schema, ensure_ascii=False, indent=2) + "\n")
combined_path = OUT / "records.jsonl"
write_crlf(combined_path, "".join(line + "\n" for line in serialized_lines))

class_paths: list[Path] = []
for entity_class in sorted(REQUIRED_CLASSES):
    path = OUT / f"{entity_class}.jsonl"
    class_records = [record for record in records_sorted if record["entity_class"] == entity_class]
    write_crlf(path, "".join(serialized_record(record) + "\n" for record in class_records))
    class_paths.append(path)

counts = Counter(record["entity_class"] for record in records_sorted)
export_files = [schema_path, combined_path, *class_paths]
source_binding_paths = [
    BASELINE / "MANIFEST.json",
    BASELINE / "records.jsonl",
    BASELINE / "record.schema.json",
    *SOURCE_FILES,
    BUILD_RECEIPT_PATH,
    MACHINE_QA_PATH,
    VISUAL_QA_PATH,
    RESPONSIVE_QA_PATH,
    PROTECTED_QA_PATH,
    *authority_paths,
    CORRECTIONS_PATH,
    TERMINOLOGY_PATH,
    Path(__file__),
    ROOT / "scripts" / "qa_backend_units_01_15.py",
]
for path in source_binding_paths:
    require(path.is_file(), f"Missing backend source binding: {rel(path)}")

manifest = {
    "schema": "ag-bridge-backend-export-manifest-v2",
    "schema_version": "1.2.0",
    "record_schema_version": RECORD_SCHEMA_VERSION,
    "generated_from_build_utc": timestamp,
    "through_unit": 15,
    "scope": "cumulative Units 1--15",
    "encoding": "UTF-8",
    "serialization": "canonical JSON Lines: records and keys sorted, compact separators, CRLF; frozen Units 1--12 records carried forward byte-for-byte",
    "record_count": len(records_sorted),
    "counts": {key: counts[key] for key in sorted(counts)},
    "files": [{"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)} for path in export_files],
    "source_bindings": [{"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)} for path in source_binding_paths],
    "units_01_12_baseline": {
        "manifest_path": "backend/units-01-12/MANIFEST.json",
        "manifest_sha256": BASELINE_MANIFEST_SHA256,
        "records_path": "backend/units-01-12/records.jsonl",
        "records_sha256": BASELINE_RECORDS_SHA256,
        "schema_path": "backend/units-01-12/record.schema.json",
        "schema_sha256": BASELINE_SCHEMA_SHA256,
        "record_count": BASELINE_RECORD_COUNT,
        "record_bytes_preserved": True,
        "stable_ids_and_payloads_preserved": True,
    },
    "reader_binding": {
        "build_receipt_path": rel(BUILD_RECEIPT_PATH),
        "build_receipt_sha256": digest(BUILD_RECEIPT_PATH),
        "through_unit": 15,
        "outputs": build_receipt["outputs"],
    },
    "authority_bindings": {
        f"unit_{unit}": {
            key: {"path": rel(spec[key]), "sha256": digest(spec[key])}
            for key in ("manifest", "map", "rights", "closure")
        }
        for unit, spec in UNIT_SPEC.items()
    },
    "model_provenance": MODEL_PROVENANCE,
    "validation": {
        "unique_stable_ids": True,
        "parent_resource_edition_rights_and_relation_endpoint_closure": True,
        "required_entity_class_closure": True,
        "units_01_12_record_bytes_and_payloads_preserved": True,
        "unit_13_15_source_hashes_match_reader_receipt": True,
        "authority_maps_rights_assets_and_solution_closure": True,
        "units_13_15_terminology_and_correction_ledger_closure": True,
        "reader_machine_visual_responsive_and_protected_qa_pass": True,
        "deterministic_double_replay_required": True,
    },
}
manifest_path = OUT / "MANIFEST.json"
write_crlf(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

print(json.dumps({
    "result": "PASS",
    "records": len(records_sorted),
    "new_records": len(new_records),
    "counts": manifest["counts"],
    "units_01_12_records_preserved": BASELINE_RECORD_COUNT,
    "manifest": rel(manifest_path),
    "manifest_sha256": digest(manifest_path),
    "model_provenance": MODEL_PROVENANCE,
}, ensure_ascii=False))
