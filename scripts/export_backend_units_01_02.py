#!/usr/bin/env python3
"""Export a deterministic cumulative backend through reader Units 1--2.

The frozen Unit 1 JSONL is an immutable compatibility baseline.  Its 684
records are carried into the cumulative export with their canonical record
bytes unchanged; new cumulative and Unit 2 records are added alongside them.
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
BASELINE = ROOT / "backend" / "unit-01"
OUT = ROOT / "backend" / "units-01-02"
BUILD_RECEIPT_PATH = ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json"
MACHINE_QA_PATH = ROOT / "qa" / "UNITS_01_02_MACHINE_QA.json"
AUTHORITY_MANIFEST_PATH = ROOT / "authority" / "wikiversity" / "unit-02" / "UNIT_AUTHORITY_MANIFEST.json"
UNIT1_MAP_PATH = ROOT / "authority" / "wikiversity" / "worksheet-01-solutions" / "ORDERED_EXERCISE_MAP.json"
UNIT2_MAP_PATH = ROOT / "authority" / "wikiversity" / "unit-02" / "ORDERED_EXERCISE_MAP.json"
UNIT1_RIGHTS_PATH = ROOT / "authority" / "RIGHTS.csv"
UNIT1_ASSET_CLOSURE_PATH = ROOT / "authority" / "ASSET_CLOSURE.json"
UNIT2_RIGHTS_PATH = ROOT / "authority" / "RIGHTS-unit-02.csv"
UNIT2_ASSET_CLOSURE_PATH = ROOT / "authority" / "ASSET_CLOSURE-unit-02.json"
CORRECTIONS_PATH = ROOT / "00_control" / "CORRECTIONS.csv"

BASELINE_MANIFEST_SHA256 = "45d160a3710a8654d7c163bf565a88d7a0fc66380be7efb3da89c4e5e7abd42f"
BASELINE_RECORDS_SHA256 = "469369311ab2b1b415195bf8ec1e3f7c4fdc8ccafd53af4aae690cc7a89bdd95"
BASELINE_SCHEMA_SHA256 = "b63956eebee7313173aa199b78a0e8684aca445aedb7f6c2c417dfa59df3fa3f"
BASELINE_RECORD_COUNT = 684

WORKFLOW_ID = "workflow.o016-d100.algebraic-geometry-bridge-id"
BRENNER_RESOURCE = "resource.brenner.algebraische-kurven.2025-2026"
BRENNER_EDITION = "edition.brenner.algebraische-kurven.prefix-freeze.2026-08-21"
LOCAL_RESOURCE = "resource.algebraic-geometry-bridge-id.editorial-layer"
UNIT1_EDITION = "edition.algebraic-geometry-bridge-id.unit-01.2026-08-21"
CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-02.2026-08-22"
TEXT_RIGHTS = "rights.brenner-course-text.cc-by-sa-4.0"
EDITORIAL_RIGHTS = "rights.derivative-editorial.cc-by-sa-4.0"
BASE_SCHEMA = "ag-bridge-backend-record"
RECORD_SCHEMA_VERSION = "1.0.0"

NEW_SOURCE_FILES = [
    ROOT / "source" / "id-ID" / "frontmatter-units-01-02.md",
    ROOT / "source" / "id-ID" / "lecture-02.md",
    ROOT / "source" / "id-ID" / "worksheet-02.md",
    ROOT / "source" / "id-ID" / "worksheet-02-solutions.md",
    ROOT / "source" / "id-ID" / "media-credits-unit-02.md",
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


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


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
        raise SystemExit(f"Frozen Unit 1 baseline mismatch: {rel(path)} {actual} != {expected}")

baseline_raw_by_id: dict[str, str] = {}
baseline_records: list[dict[str, Any]] = []
for raw_line in (BASELINE / "records.jsonl").read_text(encoding="utf-8").splitlines():
    record = json.loads(raw_line)
    if canonical(record) != raw_line:
        raise SystemExit(f"Noncanonical frozen Unit 1 record: {record['stable_id']}")
    baseline_raw_by_id[record["stable_id"]] = raw_line
    baseline_records.append(record)
if len(baseline_records) != BASELINE_RECORD_COUNT or len(baseline_raw_by_id) != BASELINE_RECORD_COUNT:
    raise SystemExit("Frozen Unit 1 record-count or stable-ID closure mismatch")

build_receipt = json.loads(BUILD_RECEIPT_PATH.read_text(encoding="utf-8"))
if build_receipt.get("schema") != "ag-bridge-build-receipt-v2" or build_receipt.get("through_unit") != 2:
    raise SystemExit("Current reader build receipt is not the Units 1--2 authority")
timestamp = build_receipt["built_utc"]
authority_manifest = json.loads(AUTHORITY_MANIFEST_PATH.read_text(encoding="utf-8"))
unit1_map = json.loads(UNIT1_MAP_PATH.read_text(encoding="utf-8"))
unit2_map = json.loads(UNIT2_MAP_PATH.read_text(encoding="utf-8"))
if authority_manifest.get("unit_number") != 2:
    raise SystemExit("Unit 2 authority manifest has the wrong unit number")
if unit1_map.get("exercise_count") != 28 or unit1_map.get("solution_count") != 7:
    raise SystemExit("Unit 1 exercise/solution authority map mismatch")
if unit2_map.get("exercise_count") != 27 or unit2_map.get("solution_count") != 9:
    raise SystemExit("Unit 2 exercise/solution authority map mismatch")


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
        source_local_id="units-01-02",
        parent_id=LOCAL_RESOURCE,
        resource_id=LOCAL_RESOURCE,
        edition_id=CUMULATIVE_EDITION,
        source_locator=rel(BUILD_RECEIPT_PATH),
        content_sha256=digest(BUILD_RECEIPT_PATH),
        language="id-ID",
        translation_state="built",
        rights_id=EDITORIAL_RIGHTS,
        supersedes=UNIT1_EDITION,
        provenance={
            "unit_1_baseline_manifest_sha256": BASELINE_MANIFEST_SHA256,
            "unit_2_authority_manifest_sha256": digest(AUTHORITY_MANIFEST_PATH),
            "unit_2_exercise_map_sha256": digest(UNIT2_MAP_PATH),
        },
        payload={
            "title": build_receipt["title"],
            "through_unit": 2,
            "source_edition_id": BRENNER_EDITION,
            "build_receipt_sha256": digest(BUILD_RECEIPT_PATH),
            "reader_outputs": build_receipt["outputs"],
            "translation_change_notice": True,
            "non_endorsement": True,
        },
    )
)

baseline_terms = [row for row in baseline_records if row["entity_class"] == "term"]
term_needles = [
    (row["payload"].get("preferred_target", "").casefold(), row["parent_id"])
    for row in baseline_terms
    if row["payload"].get("preferred_target") and row.get("parent_id")
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
    if identifier.endswith(("-practice", "-submit")):
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


unit1_solution_entries = {
    int(str(row["exercise_number"]).split(".")[-1]): row for row in unit1_map["entries"]
}
unit2_solution_entries = {
    int(row["exercise_number"]): row for row in unit2_map["entries"] if row.get("has_public_solution")
}


def source_provenance(source_path: Path, metadata: dict[str, str], identifier: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "source_edition_id": BRENNER_EDITION if source_path.name not in {"frontmatter-units-01-02.md", "media-credits-unit-02.md"} else None,
        "unit_2_authority_manifest": {
            "path": rel(AUTHORITY_MANIFEST_PATH),
            "sha256": digest(AUTHORITY_MANIFEST_PATH),
        },
    }
    if source_path.name == "lecture-02.md":
        result["upstream"] = compact_upstream(authority_manifest["lecture"])
    elif source_path.name == "worksheet-02.md":
        result["upstream"] = compact_upstream(authority_manifest["worksheet"])
    elif source_path.name == "worksheet-02-solutions.md":
        match = re.search(r"-sol-(\d+)$", identifier)
        result["exercise_solution_map"] = {
            "path": rel(UNIT2_MAP_PATH),
            "sha256": digest(UNIT2_MAP_PATH),
            "worksheet_revid": unit2_map["worksheet"]["revid"],
        }
        result["upstream"] = (
            compact_upstream(unit2_solution_entries[int(match.group(1))])
            if match
            else compact_upstream(unit2_map["worksheet"])
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
global_unit_order = max(row["order"] or 0 for row in baseline_records if row["entity_class"] == "unit")
global_segment_order = max(row["order"] or 0 for row in baseline_records if row["entity_class"] == "segment")

for source_path in NEW_SOURCE_FILES:
    original_lines = source_path.read_text(encoding="utf-8").splitlines()
    lines, metadata = strip_yaml(original_lines)
    heading_rows: list[tuple[int, int, str, str]] = []
    for index, line in enumerate(lines):
        match = heading_re.match(line)
        if match:
            heading_rows.append((index, len(match.group(1)), match.group(2), match.group(3)))

    stack: list[tuple[int, str]] = []
    for hpos, (line_index, level, title, identifier) in enumerate(heading_rows):
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent_id = stack[-1][1] if stack else CUMULATIVE_EDITION
        stack.append((level, identifier))
        next_boundary = len(lines)
        for next_index, next_level, _, _ in heading_rows[hpos + 1 :]:
            if next_level <= level:
                next_boundary = next_index
                break
        region = "\n".join(lines[line_index:next_boundary]).strip() + "\n"
        global_unit_order += 1
        source_resource = (
            BRENNER_RESOURCE
            if source_path.name in {"lecture-02.md", "worksheet-02.md", "worksheet-02-solutions.md"}
            else LOCAL_RESOURCE
        )
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
        source_resource = (
            BRENNER_RESOURCE
            if source_path.name in {"lecture-02.md", "worksheet-02.md", "worksheet-02-solutions.md"}
            else LOCAL_RESOURCE
        )
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
            rights_id=TEXT_RIGHTS if source_resource == BRENNER_RESOURCE else EDITORIAL_RIGHTS,
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

unit2_rights_rows = read_csv(UNIT2_RIGHTS_PATH)
for row in unit2_rights_rows:
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
            parent_id=image_parent_by_path.get(row["local_path"], "br-ak-2025-2026-l02"),
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
                        "derivation": row["pdf_companion_source_url"],
                    }
                    if row["pdf_local_path"]
                    else None
                ),
            },
        )
    )

existing_correction_ids = {
    record["stable_id"] for record in records if record["entity_class"] == "correction"
}
new_correction_records: list[dict[str, Any]] = []
for row in read_csv(CORRECTIONS_PATH):
    stable_id = f"correction.{row['correction_id'].lower()}"
    if stable_id in existing_correction_ids:
        continue
    affected_units: list[str]
    if row["scope"] == "worksheet_2_exercise_2_16":
        affected_units = ["br-ak-2025-2026-w02-ex-16", "br-ak-2025-2026-w02-sol-16"]
    elif row["scope"] == "worksheet_2_exercise_2_21":
        affected_units = ["br-ak-2025-2026-w02-ex-21"]
    elif row["scope"] == "worksheet_solution_2_09":
        affected_units = ["br-ak-2025-2026-w02-sol-09"]
    else:
        raise SystemExit(f"Unmapped cumulative correction scope: {row['scope']}")
    correction = make_record(
        "correction",
        stable_id,
        source_local_id=row["correction_id"],
        resource_id=BRENNER_RESOURCE,
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
            "affected_unit_ids": affected_units,
            "publication_gate": "applied_before_publication",
        },
    )
    add(correction)
    new_correction_records.append(correction)

all_unit_records = [row for row in records if row["entity_class"] == "unit"]
typed_records: list[dict[str, Any]] = []
for unit in all_unit_records:
    unit_type = unit["payload"].get("unit_type")
    if unit_type not in {"exercise", "solution"}:
        continue
    match = re.search(r"-(?:ex|sol)-(\d+)$", unit["stable_id"])
    exercise_number = int(match.group(1)) if match else None
    provenance: dict[str, Any] = {
        "indexed_unit_id": unit["stable_id"],
        "indexed_unit_record_sha256": text_digest(
            baseline_raw_by_id.get(unit["stable_id"], canonical(unit))
        ),
        "compatibility_projection": True,
        "source_provenance": unit.get("provenance", {}),
    }
    if unit_type == "solution" and exercise_number is not None:
        if "-w01-" in unit["stable_id"]:
            provenance["exercise_solution_authority"] = {
                "map_path": rel(UNIT1_MAP_PATH),
                "map_sha256": digest(UNIT1_MAP_PATH),
                "upstream": compact_upstream(unit1_solution_entries[exercise_number]),
            }
        elif "-w02-" in unit["stable_id"]:
            provenance["exercise_solution_authority"] = {
                "map_path": rel(UNIT2_MAP_PATH),
                "map_sha256": digest(UNIT2_MAP_PATH),
                "upstream": compact_upstream(unit2_solution_entries[exercise_number]),
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

machine_qa = json.loads(MACHINE_QA_PATH.read_text(encoding="utf-8"))
add(
    make_record(
        "qa_event",
        "qa.units0102.machine",
        parent_id=CUMULATIVE_EDITION,
        resource_id=LOCAL_RESOURCE,
        edition_id=CUMULATIVE_EDITION,
        source_locator=rel(MACHINE_QA_PATH),
        content_sha256=digest(MACHINE_QA_PATH),
        translation_state="built",
        rights_id=EDITORIAL_RIGHTS,
        status="passed" if machine_qa.get("status") == "PASS" else "failed",
        payload={"qa_kind": "source_math_topology_build_accessibility", "result": machine_qa},
    )
)

artifact_paths = [
    ROOT / "build" / "reader-id" / "index.html",
    ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-02.pdf",
    BUILD_RECEIPT_PATH,
    MACHINE_QA_PATH,
    AUTHORITY_MANIFEST_PATH,
    UNIT2_MAP_PATH,
    UNIT2_RIGHTS_PATH,
    UNIT2_ASSET_CLOSURE_PATH,
]
new_artifact_ids: list[str] = []
for number, artifact_path in enumerate(artifact_paths, start=1):
    artifact_id = f"artifact.units0102.{number:02d}.{artifact_path.name.casefold().replace('_', '-').replace('.', '-')}"
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
            f"relation.units0102.{relation_counter:04d}",
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


add_relation("extends", CUMULATIVE_EDITION, UNIT1_EDITION, source_locator=rel(BUILD_RECEIPT_PATH))
for unit in all_new_units:
    add_relation("contains", unit["parent_id"], unit["stable_id"], source_locator=unit["source_locator"])
    for concept_id in unit["concept_ids"]:
        add_relation("uses_concept", unit["stable_id"], concept_id, source_locator=unit["source_locator"])
for previous, following in zip(all_new_units, all_new_units[1:]):
    add_relation("precedes", previous["stable_id"], following["stable_id"], source_locator=following["source_locator"])
for exercise_number in sorted(unit2_solution_entries):
    add_relation(
        "solves",
        f"br-ak-2025-2026-w02-sol-{exercise_number:02d}",
        f"br-ak-2025-2026-w02-ex-{exercise_number:02d}",
        source_locator=rel(UNIT2_MAP_PATH),
    )
for row in unit2_rights_rows:
    add_relation(
        "illustrates",
        row["asset_id"],
        image_parent_by_path.get(row["local_path"], "br-ak-2025-2026-l02"),
        source_locator=row["description_url"],
    )
for correction in new_correction_records:
    for affected_unit_id in correction["payload"]["affected_unit_ids"]:
        add_relation("corrects", correction["stable_id"], affected_unit_id, source_locator=correction["source_locator"])
for typed in typed_records:
    add_relation("indexes_unit", typed["stable_id"], typed["parent_id"], source_locator=typed["source_locator"])
for unit_number, solution_entries in ((1, unit1_solution_entries), (2, unit2_solution_entries)):
    for exercise_number in sorted(solution_entries):
        add_relation(
            "solves",
            f"solution.br-ak-2025-2026-w{unit_number:02d}-sol-{exercise_number:02d}",
            f"exercise.br-ak-2025-2026-w{unit_number:02d}-ex-{exercise_number:02d}",
            source_locator=rel(UNIT1_MAP_PATH if unit_number == 1 else UNIT2_MAP_PATH),
            payload={"typed_family_projection": True},
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
schema["$id"] = "https://example.invalid/algebraic-geometry-bridge/backend-record-units-01-02-v1.schema.json"
schema["title"] = "Algebraic Geometry Bridge cumulative backend record through Units 1--2"
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
    AUTHORITY_MANIFEST_PATH,
    UNIT1_MAP_PATH,
    UNIT2_MAP_PATH,
    UNIT1_RIGHTS_PATH,
    UNIT1_ASSET_CLOSURE_PATH,
    UNIT2_RIGHTS_PATH,
    UNIT2_ASSET_CLOSURE_PATH,
    CORRECTIONS_PATH,
    Path(__file__),
    ROOT / "scripts" / "qa_backend_units_01_02.py",
]
manifest = {
    "schema": "ag-bridge-backend-export-manifest-v2",
    "schema_version": "1.1.0",
    "record_schema_version": RECORD_SCHEMA_VERSION,
    "generated_from_build_utc": timestamp,
    "through_unit": 2,
    "scope": "cumulative Units 1--2",
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
    "unit_1_baseline": {
        "manifest_path": "backend/unit-01/MANIFEST.json",
        "manifest_sha256": BASELINE_MANIFEST_SHA256,
        "records_path": "backend/unit-01/records.jsonl",
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
        "unit_2_manifest": {"path": rel(AUTHORITY_MANIFEST_PATH), "sha256": digest(AUTHORITY_MANIFEST_PATH)},
        "unit_1_exercise_map": {"path": rel(UNIT1_MAP_PATH), "sha256": digest(UNIT1_MAP_PATH)},
        "unit_2_exercise_map": {"path": rel(UNIT2_MAP_PATH), "sha256": digest(UNIT2_MAP_PATH)},
        "unit_1_rights": {"path": rel(UNIT1_RIGHTS_PATH), "sha256": digest(UNIT1_RIGHTS_PATH)},
        "unit_2_rights": {"path": rel(UNIT2_RIGHTS_PATH), "sha256": digest(UNIT2_RIGHTS_PATH)},
    },
    "validation": {
        "unique_stable_ids": True,
        "parent_closure": True,
        "relation_endpoint_closure": True,
        "required_entity_class_closure": True,
        "unit_1_record_bytes_preserved": True,
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
            "unit_1_records_preserved": BASELINE_RECORD_COUNT,
            "manifest": rel(manifest_path),
            "manifest_sha256": digest(manifest_path),
        },
        ensure_ascii=False,
    )
)
