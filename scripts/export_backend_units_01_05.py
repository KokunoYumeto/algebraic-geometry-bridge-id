#!/usr/bin/env python3
"""Export the deterministic cumulative backend through reader Units 1--5.

The verified Units 1--4 JSONL is a compatibility baseline. Its 2,775 records
are carried forward with their canonical record bytes unchanged; Unit 5,
cumulative-edition, terminology, QA, artifact, and relation records are added.
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
BASELINE = ROOT / "backend" / "units-01-04"
OUT = ROOT / "backend" / "units-01-05"
BUILD_RECEIPT_PATH = ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json"
MACHINE_QA_PATH = ROOT / "qa" / "UNITS_01_05_MACHINE_QA.json"
VISUAL_QA_PATH = ROOT / "qa" / "UNITS_01_05_VISUAL_QA.json"
RESPONSIVE_QA_PATH = ROOT / "qa" / "UNITS_01_05_RESPONSIVE_QA.json"
PROTECTED_QA_PATH = ROOT / "qa" / "UNIT_05_PROTECTED_SURFACES.json"
AUTHORITY_MANIFEST_PATH = ROOT / "authority" / "wikiversity" / "unit-05" / "UNIT_AUTHORITY_MANIFEST.json"
UNIT5_MAP_PATH = ROOT / "authority" / "wikiversity" / "unit-05" / "ORDERED_EXERCISE_MAP.json"
UNIT5_RIGHTS_PATH = ROOT / "authority" / "RIGHTS-unit-05.csv"
UNIT5_ASSET_CLOSURE_PATH = ROOT / "authority" / "ASSET_CLOSURE-unit-05.json"
CORRECTIONS_PATH = ROOT / "00_control" / "CORRECTIONS.csv"
TERMINOLOGY_PATH = ROOT / "00_control" / "TERMINOLOGY.csv"

BASELINE_MANIFEST_SHA256 = "5c548ca6b5257840b25f721b0e5548b89eb872b264d3d82a3afb7e7fb5186ac1"
BASELINE_RECORDS_SHA256 = "65434f1f6503d90569f39e2faa43d6d7bdcc752ea0a21e7ddae2d36c9d68c059"
BASELINE_SCHEMA_SHA256 = "519ab6508174375b38c737c7ff31c17dd5af8c8b8dfce4dbcdfc0b96fa9226cb"
BASELINE_RECORD_COUNT = 2775

WORKFLOW_ID = "workflow.o016-d100.algebraic-geometry-bridge-id"
BRENNER_RESOURCE = "resource.brenner.algebraische-kurven.2025-2026"
BRENNER_EDITION = "edition.brenner.algebraische-kurven.prefix-freeze.2026-08-21"
LOCAL_RESOURCE = "resource.algebraic-geometry-bridge-id.editorial-layer"
PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-04.2026-08-22"
CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-05.2026-08-22"
TEXT_RIGHTS = "rights.brenner-course-text.cc-by-sa-4.0"
EDITORIAL_RIGHTS = "rights.derivative-editorial.cc-by-sa-4.0"
BASE_SCHEMA = "ag-bridge-backend-record"
RECORD_SCHEMA_VERSION = "1.0.0"

NEW_SOURCE_FILES = [
    ROOT / "source" / "id-ID" / "frontmatter-units-01-05.md",
    ROOT / "source" / "id-ID" / "lecture-05.md",
    ROOT / "source" / "id-ID" / "worksheet-05.md",
    ROOT / "source" / "id-ID" / "worksheet-05-solutions.md",
    ROOT / "source" / "id-ID" / "media-credits-unit-05.md",
]

REQUIRED_CLASSES = {
    "program",
    "course",
    "resource",
    "edition",
    "unit",
    "segment",
    "exercise",
    "solution",
    "concept",
    "term",
    "asset",
    "relation",
    "rights",
    "correction",
    "qa_event",
    "artifact",
}

NEW_CONCEPTS = {
    "AGT-0036": ("concept.homogeneous-component", "homogeneous component"),
    "AGT-0037": ("concept.homogeneous-polynomial", "homogeneous polynomial"),
    "AGT-0038": ("concept.total-degree", "total degree"),
    "AGT-0039": ("concept.noether-normalization", "Noether normalization"),
    "AGT-0040": ("concept.polynomial-map", "polynomial map"),
    "AGT-0041": ("concept.affine-linear-equivalence", "affine-linear equivalence"),
    "AGT-0042": ("concept.integral-ring-extension", "integral ring extension"),
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


for path, expected in (
    (BASELINE / "MANIFEST.json", BASELINE_MANIFEST_SHA256),
    (BASELINE / "records.jsonl", BASELINE_RECORDS_SHA256),
    (BASELINE / "record.schema.json", BASELINE_SCHEMA_SHA256),
):
    actual = digest(path)
    if actual != expected:
        raise SystemExit(f"Frozen Units 1--4 baseline mismatch: {rel(path)} {actual} != {expected}")

baseline_raw_by_id: dict[str, str] = {}
baseline_records: list[dict[str, Any]] = []
for raw_line in (BASELINE / "records.jsonl").read_text(encoding="utf-8").splitlines():
    record = json.loads(raw_line)
    if canonical(record) != raw_line:
        raise SystemExit(f"Noncanonical frozen baseline record: {record['stable_id']}")
    baseline_raw_by_id[record["stable_id"]] = raw_line
    baseline_records.append(record)
if len(baseline_records) != BASELINE_RECORD_COUNT or len(baseline_raw_by_id) != BASELINE_RECORD_COUNT:
    raise SystemExit("Frozen Units 1--4 record-count or stable-ID closure mismatch")

build_receipt = json.loads(BUILD_RECEIPT_PATH.read_text(encoding="utf-8"))
if build_receipt.get("schema") != "ag-bridge-build-receipt-v2" or build_receipt.get("through_unit") != 5:
    raise SystemExit("Current reader build receipt is not the Units 1--5 authority")
timestamp = build_receipt["built_utc"]
authority_manifest = json.loads(AUTHORITY_MANIFEST_PATH.read_text(encoding="utf-8"))
unit5_map = json.loads(UNIT5_MAP_PATH.read_text(encoding="utf-8"))
if authority_manifest.get("unit_number") != 5:
    raise SystemExit("Unit 5 authority manifest has the wrong unit number")
if unit5_map.get("exercise_count") != 27 or unit5_map.get("solution_count") != 4:
    raise SystemExit("Unit 5 exercise/solution authority map mismatch")


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
        "provenance": provenance or {},
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


add(
    make_record(
        "edition",
        CUMULATIVE_EDITION,
        source_local_id="units-01-05",
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
            "units_01_04_baseline_manifest_sha256": BASELINE_MANIFEST_SHA256,
            "unit_5_authority_manifest_sha256": digest(AUTHORITY_MANIFEST_PATH),
            "unit_5_exercise_map_sha256": digest(UNIT5_MAP_PATH),
        },
        payload={
            "title": build_receipt["title"],
            "through_unit": 5,
            "source_edition_id": BRENNER_EDITION,
            "build_receipt_sha256": digest(BUILD_RECEIPT_PATH),
            "reader_outputs": build_receipt["outputs"],
            "translation_change_notice": True,
            "non_endorsement": True,
        },
    )
)

terminology_rows = read_csv(TERMINOLOGY_PATH)
new_terminology_rows = [row for row in terminology_rows if row["term_id"] in NEW_CONCEPTS]
if [row["term_id"] for row in new_terminology_rows] != list(NEW_CONCEPTS):
    raise SystemExit("Unit 5 terminology rows are missing or out of order")
for row in new_terminology_rows:
    concept_id, canonical_label = NEW_CONCEPTS[row["term_id"]]
    row_hash = text_digest("\u241f".join(row.values()))
    add(
        make_record(
            "concept",
            concept_id,
            source_local_id=row["source_term"],
            resource_id=BRENNER_RESOURCE,
            edition_id=CUMULATIVE_EDITION,
            source_locator=rel(TERMINOLOGY_PATH),
            content_sha256=row_hash,
            translation_state="translated",
            rights_id=EDITORIAL_RIGHTS,
            status=row["status"],
            payload={"canonical_label": canonical_label},
        )
    )
    add(
        make_record(
            "term",
            f"term.{row['term_id'].lower()}.id-id",
            source_local_id=row["term_id"],
            parent_id=concept_id,
            resource_id=BRENNER_RESOURCE,
            edition_id=CUMULATIVE_EDITION,
            source_locator=rel(TERMINOLOGY_PATH),
            content_sha256=row_hash,
            language="id-ID",
            translation_state="translated",
            concept_ids=[concept_id],
            rights_id=EDITORIAL_RIGHTS,
            status=row["status"],
            payload={
                "source_language": row["source_language"],
                "source_term": row["source_term"],
                "preferred_target": row["preferred_target"],
                "rejected_or_variant": row["rejected_or_variant"],
                "scope": row["scope"],
                "rationale": row["rationale"],
            },
        )
    )

new_correction_ids = [
    "AGC-CORR-0007",
    "AGC-CORR-0008",
    "AGC-CORR-0009",
    "AGC-ADAPT-0004",
    "AGC-ADAPT-0005",
    "AGC-ADAPT-0006",
    "AGC-ADAPT-0007",
]
new_correction_rows = [
    row for row in read_csv(CORRECTIONS_PATH)
    if row["correction_id"] in set(new_correction_ids)
]
if [row["correction_id"] for row in new_correction_rows] != new_correction_ids:
    raise SystemExit("Unit 5 correction/adaptation rows are missing or out of order")
correction_targets = {
    "AGC-CORR-0007": ["br-ak-2025-2026-l05-cor-01-proof"],
    "AGC-CORR-0008": ["br-ak-2025-2026-l05-s03"],
    "AGC-CORR-0009": ["br-ak-2025-2026-w05-sol-03"],
    "AGC-ADAPT-0004": [
        "br-ak-2025-2026-w01",
        "br-ak-2025-2026-w02",
        "br-ak-2025-2026-w03",
        "br-ak-2025-2026-w04",
        "br-ak-2025-2026-w05",
    ],
    "AGC-ADAPT-0005": ["agc-media-credits-unit-01"],
    "AGC-ADAPT-0006": ["br-ak-2025-2026-l04"],
    "AGC-ADAPT-0007": ["br-ak-2025-2026-w02-sol-16"],
}
for row in new_correction_rows:
    is_adaptation = row["correction_id"].startswith("AGC-ADAPT-")
    add(
        make_record(
            "correction",
            f"correction.{row['correction_id'].lower()}",
            source_local_id=row["correction_id"],
            resource_id=LOCAL_RESOURCE if is_adaptation else BRENNER_RESOURCE,
            edition_id=CUMULATIVE_EDITION,
            source_locator=rel(CORRECTIONS_PATH),
            content_sha256=text_digest("\u241f".join(row.values())),
            language="id-ID",
            translation_state="built",
            provenance={"authority_identity": row["authority_identity"]},
            rights_id=EDITORIAL_RIGHTS,
            status=row["status"],
            payload={
                "kind": row["kind"],
                "scope": row["scope"],
                "authority_observation": row["authority_observation"],
                "target_action": row["target_action"],
                "mathematical_effect": row["mathematical_effect"],
                "affected_unit_ids": correction_targets[row["correction_id"]],
                "publication_gate": row["status"],
            },
        )
    )


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
    end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
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
            "title",
            "pageid",
            "revid",
            "parentid",
            "timestamp",
            "mediawiki_sha1",
            "oldid_url",
            "xml_file",
            "xml_bytes",
            "xml_sha256",
            "html_file",
            "html_bytes",
            "html_sha256",
        )
        if key in row
    }


unit5_solution_entries = {
    int(row["exercise_number"]): row
    for row in unit5_map["entries"]
    if row.get("has_public_solution")
}


def source_provenance(source_path: Path, metadata: dict[str, str], identifier: str) -> dict[str, Any]:
    editorial = source_path.name in {"frontmatter-units-01-05.md", "media-credits-unit-05.md"}
    result: dict[str, Any] = {
        "source_edition_id": None if editorial else BRENNER_EDITION,
        "unit_5_authority_manifest": {
            "path": rel(AUTHORITY_MANIFEST_PATH),
            "sha256": digest(AUTHORITY_MANIFEST_PATH),
        },
    }
    if source_path.name == "lecture-05.md":
        result["upstream"] = compact_upstream(authority_manifest["lecture"])
    elif source_path.name == "worksheet-05.md":
        result["upstream"] = compact_upstream(authority_manifest["worksheet"])
    elif source_path.name == "worksheet-05-solutions.md":
        match = re.search(r"-sol-(\d+)$", identifier)
        result["exercise_solution_map"] = {
            "path": rel(UNIT5_MAP_PATH),
            "sha256": digest(UNIT5_MAP_PATH),
            "worksheet_revid": unit5_map["worksheet"]["revid"],
        }
        result["upstream"] = (
            compact_upstream(unit5_solution_entries[int(match.group(1))])
            if match
            else compact_upstream(unit5_map["worksheet"])
        )
    else:
        result["upstream"] = {
            key: metadata[key]
            for key in (
                "upstream_title",
                "upstream_pageid",
                "upstream_revid",
                "upstream_timestamp",
                "upstream_mediawiki_sha1",
                "source_url",
            )
            if key in metadata
        }
    return result


all_new_units: list[dict[str, Any]] = []
all_new_segments: list[dict[str, Any]] = []
image_parent_by_path: dict[str, str] = {}
global_unit_order = max(record["order"] or 0 for record in baseline_records if record["entity_class"] == "unit")
global_segment_order = max(record["order"] or 0 for record in baseline_records if record["entity_class"] == "segment")

for source_path in NEW_SOURCE_FILES:
    original_lines = source_path.read_text(encoding="utf-8").splitlines()
    lines, metadata = strip_yaml(original_lines)
    heading_rows: list[tuple[int, int, str, str]] = []
    for index, line in enumerate(lines):
        match = heading_re.match(line)
        if match:
            heading_rows.append((index, len(match.group(1)), match.group(2), match.group(3)))

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
        source_resource = BRENNER_RESOURCE if not source_path.name.startswith(("frontmatter-", "media-credits-")) else LOCAL_RESOURCE
        unit = make_record(
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
            rights_id=TEXT_RIGHTS if source_resource == BRENNER_RESOURCE else EDITORIAL_RIGHTS,
            payload={
                "unit_type": classify_unit(identifier, title),
                "heading_level": level,
                "title_markdown": title,
                "source_file_sha256": digest(source_path),
            },
        )
        add(unit)
        all_new_units.append(unit)

    active_id = CUMULATIVE_EDITION
    segment_counter: defaultdict[str, int] = defaultdict(int)
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
        segment_counter[active_id] += 1
        nonlocal_source_resource = BRENNER_RESOURCE if not source_path.name.startswith(("frontmatter-", "media-credits-")) else LOCAL_RESOURCE
        global global_segment_order
        global_segment_order += 1
        segment_id = f"{active_id}.seg-{segment_counter[active_id]:03d}"
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
            resource_id=nonlocal_source_resource,
            edition_id=CUMULATIVE_EDITION,
            source_locator=f"{rel(source_path)}:{first_line}",
            content_sha256=text_digest(content),
            language="id-ID",
            translation_state="built",
            provenance=source_provenance(source_path, metadata, active_id),
            concept_ids=concept_ids_for(content),
            rights_id=TEXT_RIGHTS if nonlocal_source_resource == BRENNER_RESOURCE else EDITORIAL_RIGHTS,
            payload={"segment_type": segment_type, "markdown": content},
        )
        add(segment)
        all_new_segments.append(segment)
        image_match = re.fullmatch(r"!\[[^\]]*\]\(([^)]+)\)", content)
        if image_match:
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

unit5_rights_rows = read_csv(UNIT5_RIGHTS_PATH)
if len(unit5_rights_rows) != 3:
    raise SystemExit("Unit 5 rights closure does not contain three positions")
for row in unit5_rights_rows:
    component_rights_id = f"rights.{row['asset_id']}"
    add(
        make_record(
            "rights",
            component_rights_id,
            source_local_id=row["commons_metadata_title"],
            resource_id=BRENNER_RESOURCE,
            edition_id=CUMULATIVE_EDITION,
            source_locator=row["description_url"],
            content_sha256=row["local_sha256"],
            payload={
                "license": row["license_short"],
                "license_url": row["license_url"] or None,
                "usage_terms": row["usage_terms"] or None,
                "creator_or_artist": row["artist"] or row["uploader"],
                "uploader": row["uploader"],
                "attribution_required": row["attribution_required"].lower() == "true",
                "scope": row["asset_id"],
            },
        )
    )
    add(
        make_record(
            "asset",
            row["asset_id"],
            source_local_id=row["resource_title"],
            parent_id=image_parent_by_path.get(row["local_path"], "br-ak-2025-2026-l05"),
            order=int(row["reader_order"]),
            path=row["local_path"],
            resource_id=BRENNER_RESOURCE,
            edition_id=CUMULATIVE_EDITION,
            source_locator=row["description_url"],
            content_sha256=row["local_sha256"],
            translation_state="built",
            rights_id=component_rights_id,
            payload={
                "caption_id": row["reader_caption_id"],
                "selected_form": row["selected_form"],
                "bytes": int(row["local_bytes"]),
                "width": int(row["local_width"]),
                "height": int(row["local_height"]),
                "mime": row["mime"],
                "source_original_url": row["original_url"],
                "selected_url": row["selected_url"],
                "pdf_companion": (
                    {
                        "path": row["pdf_local_path"],
                        "bytes": int(row["pdf_local_bytes"]),
                        "sha256": row["pdf_local_sha256"],
                    }
                    if row["pdf_local_path"]
                    else None
                ),
            },
        )
    )

all_unit_records = [record for record in records if record["entity_class"] == "unit"]
typed_records: list[dict[str, Any]] = []
for unit in all_new_units:
    unit_type = unit["payload"].get("unit_type")
    if unit_type not in {"exercise", "solution"}:
        continue
    match = re.search(r"-(?:ex|sol)-(\d+)$", unit["stable_id"])
    exercise_number = int(match.group(1)) if match else None
    provenance: dict[str, Any] = {
        "indexed_unit_id": unit["stable_id"],
        "indexed_unit_record_sha256": text_digest(canonical(unit)),
        "compatibility_projection": True,
        "source_provenance": unit.get("provenance", {}),
    }
    if unit_type == "solution" and exercise_number is not None:
        provenance["exercise_solution_authority"] = {
            "map_path": rel(UNIT5_MAP_PATH),
            "map_sha256": digest(UNIT5_MAP_PATH),
            "upstream": compact_upstream(unit5_solution_entries[exercise_number]),
        }
    typed = make_record(
        unit_type,
        f"{unit_type}.{unit['stable_id']}",
        source_local_id=unit["source_local_id"],
        parent_id=unit["stable_id"],
        order=exercise_number,
        path=unit["path"],
        resource_id=unit["resource_id"],
        edition_id=unit["edition_id"],
        source_locator=unit["source_locator"],
        content_sha256=unit["content_sha256"],
        language=unit["language"],
        translation_state=unit["translation_state"],
        provenance=provenance,
        concept_ids=unit["concept_ids"],
        rights_id=unit["rights_id"],
        status=unit["status"],
        payload={
            "unit_id": unit["stable_id"],
            "exercise_number": exercise_number,
            "family": unit_type,
        },
    )
    add(typed)
    typed_records.append(typed)

qa_specs = [
    ("qa.units0105.machine", MACHINE_QA_PATH, "source_math_topology_build_accessibility", "status"),
    ("qa.units0105.visual", VISUAL_QA_PATH, "all_page_and_full_resolution_visual_layout", "result"),
    ("qa.units0105.responsive", RESPONSIVE_QA_PATH, "desktop_and_mobile_reader_reflow", "status"),
    ("qa.unit05.protected", PROTECTED_QA_PATH, "authority_formula_exercise_solution_and_media_fidelity", "status"),
]
for stable_id, path, qa_kind, status_key in qa_specs:
    qa_payload = json.loads(path.read_text(encoding="utf-8"))
    qa_status = qa_payload.get(status_key)
    add(
        make_record(
            "qa_event",
            stable_id,
            parent_id=CUMULATIVE_EDITION,
            resource_id=LOCAL_RESOURCE,
            edition_id=CUMULATIVE_EDITION,
            source_locator=rel(path),
            content_sha256=digest(path),
            translation_state="built",
            rights_id=EDITORIAL_RIGHTS,
            status="passed" if qa_status == "PASS" else "failed",
            payload={"qa_kind": qa_kind, "result": qa_payload},
        )
    )

artifact_paths = [
    ROOT / "build" / "reader-id" / "index.html",
    ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-05.pdf",
    BUILD_RECEIPT_PATH,
    MACHINE_QA_PATH,
    VISUAL_QA_PATH,
    RESPONSIVE_QA_PATH,
    PROTECTED_QA_PATH,
    AUTHORITY_MANIFEST_PATH,
    UNIT5_MAP_PATH,
    UNIT5_RIGHTS_PATH,
    UNIT5_ASSET_CLOSURE_PATH,
]
new_artifact_ids: list[str] = []
for number, artifact_path in enumerate(artifact_paths, start=1):
    artifact_id = f"artifact.units0105.{number:02d}.{artifact_path.name.casefold().replace('_', '-').replace('.', '-')}"
    new_artifact_ids.append(artifact_id)
    add(
        make_record(
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
                "media_type": {
                    ".html": "text/html",
                    ".pdf": "application/pdf",
                    ".json": "application/json",
                    ".csv": "text/csv",
                }.get(artifact_path.suffix, "application/octet-stream"),
                "build_receipt": rel(BUILD_RECEIPT_PATH),
            },
        )
    )

relation_counter = 0


def add_relation(
    relation_type: str,
    subject_id: str,
    object_id: str,
    *,
    source_locator: str,
    payload: dict[str, Any] | None = None,
) -> None:
    global relation_counter
    relation_counter += 1
    add(
        make_record(
            "relation",
            f"relation.units0105.{relation_counter:04d}",
            order=relation_counter,
            resource_id=LOCAL_RESOURCE,
            edition_id=CUMULATIVE_EDITION,
            source_locator=source_locator,
            content_sha256=text_digest(f"{relation_type}\u241f{subject_id}\u241f{object_id}"),
            translation_state="built",
            rights_id=EDITORIAL_RIGHTS,
            payload={
                "relation_type": relation_type,
                "subject_id": subject_id,
                "object_id": object_id,
                **(payload or {}),
            },
        )
    )


add_relation("extends", CUMULATIVE_EDITION, PREVIOUS_EDITION, source_locator=rel(BUILD_RECEIPT_PATH))
for unit in all_new_units:
    add_relation("contains", unit["parent_id"], unit["stable_id"], source_locator=unit["source_locator"])
    for concept_id in unit["concept_ids"]:
        add_relation("uses_concept", unit["stable_id"], concept_id, source_locator=unit["source_locator"])
for previous, following in zip(all_new_units, all_new_units[1:]):
    add_relation("precedes", previous["stable_id"], following["stable_id"], source_locator=following["source_locator"])
for exercise_number in sorted(unit5_solution_entries):
    add_relation(
        "solves",
        f"br-ak-2025-2026-w05-sol-{exercise_number:02d}",
        f"br-ak-2025-2026-w05-ex-{exercise_number:02d}",
        source_locator=rel(UNIT5_MAP_PATH),
    )
for row in unit5_rights_rows:
    add_relation(
        "illustrates",
        row["asset_id"],
        image_parent_by_path.get(row["local_path"], "br-ak-2025-2026-l05"),
        source_locator=row["description_url"],
    )
for typed in typed_records:
    add_relation("indexes_unit", typed["stable_id"], typed["parent_id"], source_locator=typed["source_locator"])
for exercise_number in sorted(unit5_solution_entries):
    add_relation(
        "solves",
        f"solution.br-ak-2025-2026-w05-sol-{exercise_number:02d}",
        f"exercise.br-ak-2025-2026-w05-ex-{exercise_number:02d}",
        source_locator=rel(UNIT5_MAP_PATH),
        payload={"typed_family_projection": True},
    )
for row in new_terminology_rows:
    concept_id, _ = NEW_CONCEPTS[row["term_id"]]
    add_relation(
        "labels",
        f"term.{row['term_id'].lower()}.id-id",
        concept_id,
        source_locator=rel(TERMINOLOGY_PATH),
    )
for artifact_id in new_artifact_ids:
    add_relation("emits", CUMULATIVE_EDITION, artifact_id, source_locator=rel(BUILD_RECEIPT_PATH))

ids = [record["stable_id"] for record in records]
if len(ids) != len(set(ids)):
    duplicates = sorted(stable_id for stable_id, count in Counter(ids).items() if count > 1)
    raise SystemExit(f"Duplicate stable IDs: {duplicates}")
if {record["entity_class"] for record in records} != REQUIRED_CLASSES:
    raise SystemExit("Required entity-family closure mismatch")
id_set = set(ids)
for record in records:
    if record["parent_id"] and record["parent_id"] not in id_set:
        raise SystemExit(f"Missing parent {record['parent_id']} for {record['stable_id']}")
    if record["entity_class"] == "relation":
        for endpoint in (record["payload"]["subject_id"], record["payload"]["object_id"]):
            if endpoint not in id_set:
                raise SystemExit(f"Missing relation endpoint {endpoint}")

schema = json.loads((BASELINE / "record.schema.json").read_text(encoding="utf-8"))
schema["$id"] = "https://example.invalid/algebraic-geometry-bridge/backend-record-units-01-05-v1.schema.json"
schema["title"] = "Algebraic Geometry Bridge cumulative backend record through Units 1--5"
schema["properties"]["entity_class"]["enum"] = sorted(REQUIRED_CLASSES)

OUT.mkdir(parents=True, exist_ok=True)
schema_path = OUT / "record.schema.json"
write_crlf(schema_path, json.dumps(schema, ensure_ascii=False, indent=2) + "\n")

records_sorted = sorted(records, key=lambda row: (row["entity_class"], row["stable_id"]))


def serialized_record(record: dict[str, Any]) -> str:
    return baseline_raw_by_id.get(record["stable_id"], canonical(record))


combined_path = OUT / "records.jsonl"
write_crlf(combined_path, "".join(serialized_record(record) + "\n" for record in records_sorted))

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
    *NEW_SOURCE_FILES,
    BUILD_RECEIPT_PATH,
    MACHINE_QA_PATH,
    VISUAL_QA_PATH,
    RESPONSIVE_QA_PATH,
    PROTECTED_QA_PATH,
    AUTHORITY_MANIFEST_PATH,
    UNIT5_MAP_PATH,
    UNIT5_RIGHTS_PATH,
    UNIT5_ASSET_CLOSURE_PATH,
    CORRECTIONS_PATH,
    TERMINOLOGY_PATH,
    Path(__file__),
    ROOT / "scripts" / "qa_backend_units_01_05.py",
]
manifest = {
    "schema": "ag-bridge-backend-export-manifest-v2",
    "schema_version": "1.2.0",
    "record_schema_version": RECORD_SCHEMA_VERSION,
    "generated_from_build_utc": timestamp,
    "through_unit": 5,
    "scope": "cumulative Units 1--5",
    "encoding": "UTF-8",
    "serialization": "canonical JSON Lines: records and keys sorted, compact separators, baseline-compatible CRLF",
    "record_count": len(records_sorted),
    "counts": {key: counts[key] for key in sorted(counts)},
    "files": [
        {"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)} for path in export_files
    ],
    "source_bindings": [
        {"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)} for path in source_binding_paths
    ],
    "units_01_04_baseline": {
        "manifest_path": "backend/units-01-04/MANIFEST.json",
        "manifest_sha256": BASELINE_MANIFEST_SHA256,
        "records_path": "backend/units-01-04/records.jsonl",
        "records_sha256": BASELINE_RECORDS_SHA256,
        "record_count": BASELINE_RECORD_COUNT,
        "record_bytes_preserved": True,
    },
    "reader_binding": {
        "build_receipt_path": rel(BUILD_RECEIPT_PATH),
        "build_receipt_sha256": digest(BUILD_RECEIPT_PATH),
        "through_unit": build_receipt["through_unit"],
        "outputs": build_receipt["outputs"],
    },
    "authority_bindings": {
        "unit_5_manifest": {"path": rel(AUTHORITY_MANIFEST_PATH), "sha256": digest(AUTHORITY_MANIFEST_PATH)},
        "unit_5_exercise_map": {"path": rel(UNIT5_MAP_PATH), "sha256": digest(UNIT5_MAP_PATH)},
        "unit_5_rights": {"path": rel(UNIT5_RIGHTS_PATH), "sha256": digest(UNIT5_RIGHTS_PATH)},
        "unit_5_asset_closure": {"path": rel(UNIT5_ASSET_CLOSURE_PATH), "sha256": digest(UNIT5_ASSET_CLOSURE_PATH)},
    },
    "validation": {
        "unique_stable_ids": True,
        "parent_closure": True,
        "relation_endpoint_closure": True,
        "required_entity_class_closure": True,
        "units_01_04_record_bytes_preserved": True,
        "deterministic_double_replay_required": True,
    },
}
manifest_path = OUT / "MANIFEST.json"
write_crlf(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

print(
    json.dumps(
        {
            "result": "PASS",
            "records": len(records_sorted),
            "counts": manifest["counts"],
            "units_01_04_records_preserved": BASELINE_RECORD_COUNT,
            "manifest": rel(manifest_path),
            "manifest_sha256": digest(manifest_path),
        },
        ensure_ascii=False,
    )
)
