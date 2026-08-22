#!/usr/bin/env python3
"""Fail-closed replay and closure QA for the cumulative Units 1--2 backend."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "scripts" / "export_backend_units_01_02.py"
BACKEND = ROOT / "backend" / "units-01-02"
MANIFEST = BACKEND / "MANIFEST.json"
RECEIPT = ROOT / "qa" / "UNITS_01_02_BACKEND_QA.json"
BASELINE = ROOT / "backend" / "unit-01"
BUILD_RECEIPT_PATH = ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json"
AUTHORITY_MANIFEST_PATH = ROOT / "authority" / "wikiversity" / "unit-02" / "UNIT_AUTHORITY_MANIFEST.json"
UNIT1_MAP_PATH = ROOT / "authority" / "wikiversity" / "worksheet-01-solutions" / "ORDERED_EXERCISE_MAP.json"
UNIT2_MAP_PATH = ROOT / "authority" / "wikiversity" / "unit-02" / "ORDERED_EXERCISE_MAP.json"
CORRECTIONS_PATH = ROOT / "00_control" / "CORRECTIONS.csv"

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


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def snapshot() -> tuple[str, dict[str, dict[str, Any]]]:
    manifest_sha256 = digest(MANIFEST)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = {row["path"]: {"bytes": row["bytes"], "sha256": row["sha256"]} for row in manifest["files"]}
    rows[MANIFEST.relative_to(ROOT).as_posix()] = {
        "bytes": MANIFEST.stat().st_size,
        "sha256": manifest_sha256,
    }
    for path, expected in rows.items():
        local = ROOT / path
        require(local.stat().st_size == expected["bytes"], f"Export snapshot byte mismatch: {path}")
        require(digest(local) == expected["sha256"], f"Export snapshot hash mismatch: {path}")
    return manifest_sha256, rows


def replay() -> tuple[str, str, str]:
    subprocess.run([sys.executable, str(EXPORTER)], cwd=ROOT, check=True, capture_output=True, text=True)
    first_manifest, first_files = snapshot()
    subprocess.run([sys.executable, str(EXPORTER)], cwd=ROOT, check=True, capture_output=True, text=True)
    second_manifest, second_files = snapshot()
    require(first_manifest == second_manifest, "Nondeterministic manifest replay")
    require(first_files == second_files, "Nondeterministic export-file replay")
    tree_sha256 = text_digest(canonical(first_files))
    return first_manifest, second_manifest, tree_sha256


first_manifest_sha256, second_manifest_sha256, export_tree_sha256 = replay()
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
require(manifest["through_unit"] == 2, "Manifest is not cumulative through Unit 2")
require(manifest["scope"] == "cumulative Units 1--2", "Manifest scope mismatch")

for row in manifest["files"] + manifest["source_bindings"]:
    path = ROOT / row["path"]
    require(path.is_file(), f"Manifest-bound file absent: {row['path']}")
    require(path.stat().st_size == row["bytes"], f"Manifest-bound byte mismatch: {row['path']}")
    require(digest(path) == row["sha256"], f"Manifest-bound hash mismatch: {row['path']}")

schema = json.loads((BACKEND / "record.schema.json").read_text(encoding="utf-8"))
validator = Draft202012Validator(schema)
combined_bytes = (BACKEND / "records.jsonl").read_bytes()
require(combined_bytes.count(b"\n") == combined_bytes.count(b"\r\n"), "JSONL contains a bare LF")
combined_lines = combined_bytes.decode("utf-8").splitlines()
require(all(line for line in combined_lines), "JSONL contains a blank line")
combined_records: list[dict[str, Any]] = []
schema_errors: list[str] = []
for line_number, line in enumerate(combined_lines, start=1):
    record = json.loads(line)
    require(canonical(record) == line, f"Noncanonical JSONL record at line {line_number}")
    schema_errors.extend(error.message for error in validator.iter_errors(record))
    combined_records.append(record)
require(not schema_errors, f"JSON Schema errors: {schema_errors[:5]}")

class_lines: list[str] = []
for entity_class in schema["properties"]["entity_class"]["enum"]:
    path = BACKEND / f"{entity_class}.jsonl"
    raw = path.read_bytes()
    require(raw.count(b"\n") == raw.count(b"\r\n"), f"{path.name} contains a bare LF")
    for line in raw.decode("utf-8").splitlines():
        record = json.loads(line)
        require(record["entity_class"] == entity_class, f"Wrong class in {path.name}")
        require(canonical(record) == line, f"Noncanonical class projection in {path.name}")
        class_lines.append(line)
require(class_lines == combined_lines, "Combined JSONL is not the exact ordered union of class projections")

baseline_raw_by_id: dict[str, str] = {}
for line in (BASELINE / "records.jsonl").read_text(encoding="utf-8").splitlines():
    baseline_raw_by_id[json.loads(line)["stable_id"]] = line
cumulative_raw_by_id = {json.loads(line)["stable_id"]: line for line in combined_lines}
require(len(baseline_raw_by_id) == 684, "Frozen Unit 1 baseline record count changed")
for stable_id, baseline_line in baseline_raw_by_id.items():
    require(cumulative_raw_by_id.get(stable_id) == baseline_line, f"Unit 1 record bytes changed: {stable_id}")

ids = [record["stable_id"] for record in combined_records]
id_set = set(ids)
require(len(ids) == len(id_set), "Duplicate stable ID")
require(
    all(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", stable_id) for stable_id in ids),
    "Malformed stable ID",
)
require({record["entity_class"] for record in combined_records} == REQUIRED_CLASSES, "Entity-family closure mismatch")

by_id = {record["stable_id"]: record for record in combined_records}
class_ids = {
    entity_class: {record["stable_id"] for record in combined_records if record["entity_class"] == entity_class}
    for entity_class in REQUIRED_CLASSES
}
for record in combined_records:
    if record["parent_id"]:
        require(record["parent_id"] in id_set, f"Missing parent for {record['stable_id']}")
    if record["resource_id"]:
        require(record["resource_id"] in class_ids["resource"], f"Missing resource for {record['stable_id']}")
    if record["edition_id"]:
        require(record["edition_id"] in class_ids["edition"], f"Missing edition for {record['stable_id']}")
    if record["rights_id"]:
        require(record["rights_id"] in class_ids["rights"], f"Missing rights for {record['stable_id']}")
    for concept_id in record["concept_ids"]:
        require(concept_id in class_ids["concept"], f"Missing concept {concept_id} for {record['stable_id']}")
    if record["entity_class"] == "relation":
        payload = record["payload"]
        require(payload.get("subject_id") in id_set, f"Missing relation subject for {record['stable_id']}")
        require(payload.get("object_id") in id_set, f"Missing relation object for {record['stable_id']}")

counts = Counter(record["entity_class"] for record in combined_records)
require(dict(sorted(counts.items())) == manifest["counts"], "Manifest class counts do not replay")
require(len(combined_records) == manifest["record_count"], "Manifest record count does not replay")

build_receipt = json.loads(BUILD_RECEIPT_PATH.read_text(encoding="utf-8"))
require(build_receipt["schema"] == "ag-bridge-build-receipt-v2", "Reader build receipt schema mismatch")
require(build_receipt["through_unit"] == 2, "Reader build receipt scope mismatch")
require(manifest["reader_binding"]["build_receipt_sha256"] == digest(BUILD_RECEIPT_PATH), "Reader receipt binding mismatch")
for row in build_receipt["inputs"] + build_receipt["outputs"]:
    path = ROOT / row["path"]
    require(path.is_file(), f"Reader-bound file absent: {row['path']}")
    require(path.stat().st_size == row["bytes"], f"Reader-bound byte mismatch: {row['path']}")
    require(digest(path) == row["sha256"], f"Reader-bound hash mismatch: {row['path']}")
current_artifacts = {
    record["path"]: record
    for record in combined_records
    if record["entity_class"] == "artifact" and record["stable_id"].startswith("artifact.units0102.")
}
for path in [row["path"] for row in build_receipt["outputs"]] + [BUILD_RECEIPT_PATH.relative_to(ROOT).as_posix()]:
    require(path in current_artifacts, f"Current reader artifact record absent: {path}")
for path, record in current_artifacts.items():
    local = ROOT / path
    require(local.stat().st_size == record["payload"]["bytes"], f"Artifact byte mismatch: {path}")
    require(digest(local) == record["content_sha256"], f"Artifact hash mismatch: {path}")
cumulative_edition = by_id["edition.algebraic-geometry-bridge-id.units-01-02.2026-08-22"]
require(cumulative_edition["content_sha256"] == digest(BUILD_RECEIPT_PATH), "Cumulative edition receipt hash mismatch")

authority_manifest = json.loads(AUTHORITY_MANIFEST_PATH.read_text(encoding="utf-8"))
require(authority_manifest["unit_number"] == 2, "Authority manifest unit mismatch")
authority_dir = AUTHORITY_MANIFEST_PATH.parent
for row in authority_manifest["files"]:
    path = authority_dir / row["file"]
    require(path.is_file(), f"Unit 2 authority file absent: {row['file']}")
    require(path.stat().st_size == row["bytes"], f"Unit 2 authority byte mismatch: {row['file']}")
    require(digest(path) == row["sha256"], f"Unit 2 authority hash mismatch: {row['file']}")


def yaml_metadata(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    require(lines and lines[0] == "---", f"Missing YAML metadata: {path.name}")
    end = lines.index("---", 1)
    result: dict[str, str] = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            result[match.group(1)] = match.group(2).strip().strip('"')
    return result


lecture_meta = yaml_metadata(ROOT / "source" / "id-ID" / "lecture-02.md")
worksheet_meta = yaml_metadata(ROOT / "source" / "id-ID" / "worksheet-02.md")
for metadata, authority, label in (
    (lecture_meta, authority_manifest["lecture"], "lecture"),
    (worksheet_meta, authority_manifest["worksheet"], "worksheet"),
):
    require(int(metadata["upstream_pageid"]) == authority["pageid"], f"Unit 2 {label} pageid mismatch")
    require(int(metadata["upstream_revid"]) == authority["revid"], f"Unit 2 {label} revid mismatch")
    require(metadata["upstream_mediawiki_sha1"] == authority["mediawiki_sha1"], f"Unit 2 {label} SHA-1 mismatch")
    require(metadata["upstream_timestamp"] == authority["timestamp"], f"Unit 2 {label} timestamp mismatch")


def heading_ids(path: Path, pattern: str) -> list[str]:
    ids_found = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.search(r"\{#([^}]+)\}\s*$", line)
        if match and re.fullmatch(pattern, match.group(1)):
            ids_found.append(match.group(1))
    return ids_found


exercise_solution_summary: dict[str, dict[str, Any]] = {}
typed_solves = {
    (record["payload"]["subject_id"], record["payload"]["object_id"])
    for record in combined_records
    if record["entity_class"] == "relation"
    and record["payload"].get("relation_type") == "solves"
    and record["payload"].get("typed_family_projection") is True
}
for unit_number, expected_exercises, expected_solutions, map_path in (
    (1, 28, 7, UNIT1_MAP_PATH),
    (2, 27, 9, UNIT2_MAP_PATH),
):
    worksheet_path = ROOT / "source" / "id-ID" / f"worksheet-{unit_number:02d}.md"
    solutions_path = ROOT / "source" / "id-ID" / f"worksheet-{unit_number:02d}-solutions.md"
    exercises = heading_ids(worksheet_path, rf"br-ak-2025-2026-w{unit_number:02d}-ex-\d{{2}}")
    solutions = heading_ids(solutions_path, rf"br-ak-2025-2026-w{unit_number:02d}-sol-\d{{2}}")
    require(len(exercises) == expected_exercises, f"Unit {unit_number} exercise heading count mismatch")
    require(len(solutions) == expected_solutions, f"Unit {unit_number} solution heading count mismatch")
    authority_map = json.loads(map_path.read_text(encoding="utf-8"))
    if unit_number == 1:
        mapped_numbers = sorted(int(str(row["exercise_number"]).split(".")[-1]) for row in authority_map["entries"])
        mapped_rows = {int(str(row["exercise_number"]).split(".")[-1]): row for row in authority_map["entries"]}
    else:
        mapped_numbers = sorted(int(row["exercise_number"]) for row in authority_map["entries"] if row.get("has_public_solution"))
        mapped_rows = {int(row["exercise_number"]): row for row in authority_map["entries"] if row.get("has_public_solution")}
    source_solution_numbers = sorted(int(identifier.rsplit("-", 1)[-1]) for identifier in solutions)
    require(source_solution_numbers == mapped_numbers, f"Unit {unit_number} solution-map mismatch")
    expected_exercise_families = {f"exercise.{identifier}" for identifier in exercises}
    expected_solution_families = {f"solution.{identifier}" for identifier in solutions}
    require(expected_exercise_families <= class_ids["exercise"], f"Unit {unit_number} exercise-family projection missing")
    require(expected_solution_families <= class_ids["solution"], f"Unit {unit_number} solution-family projection missing")
    for number, authority_row in mapped_rows.items():
        solution_id = f"solution.br-ak-2025-2026-w{unit_number:02d}-sol-{number:02d}"
        exercise_id = f"exercise.br-ak-2025-2026-w{unit_number:02d}-ex-{number:02d}"
        require((solution_id, exercise_id) in typed_solves, f"Typed solve relation absent: {solution_id}")
        binding = by_id[solution_id]["provenance"]["exercise_solution_authority"]
        require(binding["map_sha256"] == digest(map_path), f"Solution map hash absent: {solution_id}")
        require(binding["upstream"]["revid"] == authority_row["revid"], f"Solution revid mismatch: {solution_id}")
        require(binding["upstream"]["mediawiki_sha1"] == authority_row["mediawiki_sha1"], f"Solution SHA-1 mismatch: {solution_id}")
    exercise_solution_summary[f"unit_{unit_number:02d}"] = {
        "exercise_count": len(exercises),
        "solution_count": len(solutions),
        "map_sha256": digest(map_path),
        "typed_solve_relations": len(mapped_numbers),
    }
require(len(class_ids["exercise"]) == 55, "Cumulative exercise-family count mismatch")
require(len(class_ids["solution"]) == 16, "Cumulative solution-family count mismatch")


def verify_rights(unit_number: int, rights_name: str, closure_name: str, expected_positions: int) -> dict[str, Any]:
    rights_path = ROOT / "authority" / rights_name
    closure_path = ROOT / "authority" / closure_name
    rows = read_csv(rights_path)
    closure = json.loads(closure_path.read_text(encoding="utf-8"))
    require(len(rows) == expected_positions, f"Unit {unit_number} rights-row count mismatch")
    require(closure["reader_media_positions"] == expected_positions, f"Unit {unit_number} media-position mismatch")
    require(closure["rights_sha256"] == digest(rights_path), f"Unit {unit_number} rights closure hash mismatch")
    unique_local_paths: set[str] = set()
    for row in rows:
        asset_id = row["asset_id"]
        require(asset_id in class_ids["asset"], f"Asset record absent: {asset_id}")
        asset = by_id[asset_id]
        primary_path = ROOT / row["local_path"]
        require(primary_path.stat().st_size == int(row["local_bytes"]), f"Asset bytes mismatch: {asset_id}")
        require(digest(primary_path) == row["local_sha256"], f"Asset hash mismatch: {asset_id}")
        require(asset["path"] == row["local_path"], f"Asset path mismatch: {asset_id}")
        require(asset["content_sha256"] == row["local_sha256"], f"Asset record hash mismatch: {asset_id}")
        rights_id = f"rights.{asset_id}"
        require(asset["rights_id"] == rights_id and rights_id in class_ids["rights"], f"Asset rights missing: {asset_id}")
        require(by_id[rights_id]["payload"]["license"] == row["license_short"], f"Asset license mismatch: {asset_id}")
        unique_local_paths.add(row["local_path"])
        if row["pdf_local_path"]:
            companion = ROOT / row["pdf_local_path"]
            require(companion.stat().st_size == int(row["pdf_local_bytes"]), f"Companion bytes mismatch: {asset_id}")
            require(digest(companion) == row["pdf_local_sha256"], f"Companion hash mismatch: {asset_id}")
            unique_local_paths.add(row["pdf_local_path"])
    require(len(unique_local_paths) == closure["unique_local_assets"], f"Unit {unit_number} unique-asset closure mismatch")
    return {
        "positions": len(rows),
        "unique_local_assets": len(unique_local_paths),
        "rights_sha256": digest(rights_path),
        "closure_sha256": digest(closure_path),
    }


rights_summary = {
    "unit_01": verify_rights(1, "RIGHTS.csv", "ASSET_CLOSURE.json", 23),
    "unit_02": verify_rights(2, "RIGHTS-unit-02.csv", "ASSET_CLOSURE-unit-02.json", 2),
}
require(len(class_ids["asset"]) == 25, "Cumulative primary-asset count mismatch")

correction_rows = read_csv(CORRECTIONS_PATH)
require(len(correction_rows) == 7, "Current correction ledger does not contain seven rows")
require(len(class_ids["correction"]) == 7, "Cumulative correction-family count mismatch")
correction_relations = {
    (record["payload"]["subject_id"], record["payload"]["object_id"])
    for record in combined_records
    if record["entity_class"] == "relation" and record["payload"].get("relation_type") in {"corrects", "adapts"}
}
for row in correction_rows:
    stable_id = f"correction.{row['correction_id'].lower()}"
    require(stable_id in class_ids["correction"], f"Correction record absent: {stable_id}")
    correction = by_id[stable_id]
    require(correction["source_local_id"] == row["correction_id"], f"Correction local ID mismatch: {stable_id}")
    require(correction["content_sha256"] == text_digest("\u241f".join(row.values())), f"Correction row hash mismatch: {stable_id}")
    require(correction["payload"]["kind"] == row["kind"], f"Correction kind mismatch: {stable_id}")
    require(correction["payload"]["scope"] == row["scope"], f"Correction scope mismatch: {stable_id}")
    require(correction["payload"]["mathematical_effect"] == row["mathematical_effect"], f"Correction effect mismatch: {stable_id}")
    require(correction["status"] == row["status"], f"Correction status mismatch: {stable_id}")
    for affected_unit_id in correction["payload"]["affected_unit_ids"]:
        require(affected_unit_id in class_ids["unit"], f"Correction target absent: {stable_id} -> {affected_unit_id}")
        require((stable_id, affected_unit_id) in correction_relations, f"Correction relation absent: {stable_id} -> {affected_unit_id}")

correction_summary = {
    "rows": len(correction_rows),
    "ledger_sha256": digest(CORRECTIONS_PATH),
    "applied_before_publication": sorted(
        row["correction_id"] for row in correction_rows if row["status"] == "applied_before_publication"
    ),
}

secret_pattern = re.compile(
    r"(?:github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{20,}|(?:sk|rk)-[A-Za-z0-9_-]{20,}|ZENODO_ACCESS_TOKEN\s*[:=]\s*\S+)",
    flags=re.IGNORECASE,
)
for path in [MANIFEST, *[ROOT / row["path"] for row in manifest["files"]]]:
    require(secret_pattern.search(path.read_text(encoding="utf-8")) is None, f"Credential-shaped text in {path.name}")

result = {
    "schema": "ag-bridge-backend-qa-receipt-v2",
    "tested_build_utc": manifest["generated_from_build_utc"],
    "status": "PASS",
    "through_unit": 2,
    "manifest_path": MANIFEST.relative_to(ROOT).as_posix(),
    "manifest_sha256": second_manifest_sha256,
    "export_tree_sha256": export_tree_sha256,
    "deterministic_double_replay": first_manifest_sha256 == second_manifest_sha256,
    "record_count": len(combined_records),
    "class_counts": dict(sorted(counts.items())),
    "jsonl_parse_errors": 0,
    "json_schema_errors": 0,
    "unique_and_well_formed_stable_ids": True,
    "unit_1_record_bytes_preserved": len(baseline_raw_by_id),
    "parent_closure": True,
    "relation_endpoint_closure": True,
    "resource_edition_rights_and_concept_closure": True,
    "class_projection_round_trip": True,
    "source_and_export_hash_replay": True,
    "reader_binding": {
        "build_receipt_sha256": digest(BUILD_RECEIPT_PATH),
        "output_count": len(build_receipt["outputs"]),
        "outputs": build_receipt["outputs"],
    },
    "authority_binding": {
        "unit_2_manifest_sha256": digest(AUTHORITY_MANIFEST_PATH),
        "file_count": len(authority_manifest["files"]),
        "lecture_revid": authority_manifest["lecture"]["revid"],
        "worksheet_revid": authority_manifest["worksheet"]["revid"],
    },
    "exercise_solution_mapping": exercise_solution_summary,
    "rights_and_assets": rights_summary,
    "corrections": correction_summary,
    "credential_findings": 0,
    "check_families": [
        "jsonl_parse_canonical_serialization_and_json_schema",
        "stable_id_uniqueness_format_and_unit1_byte_preservation",
        "parent_relation_resource_edition_rights_and_concept_closure",
        "class_projection_round_trip",
        "deterministic_double_export_and_file_tree_identity",
        "reader_build_receipt_input_output_and_artifact_hash_bindings",
        "unit2_revision_authority_manifest_and_file_hash_replay",
        "unit1_unit2_exercise_solution_family_and_map_closure",
        "unit1_unit2_component_rights_asset_and_companion_hash_closure",
        "seven_row_correction_ledger_hash_payload_target_and_relation_closure",
        "credential_pattern_scan",
    ],
    "replay_command": f'"{sys.executable}" "{Path(__file__).relative_to(ROOT).as_posix()}"',
    "exporter": {
        "path": EXPORTER.relative_to(ROOT).as_posix(),
        "sha256": digest(EXPORTER),
    },
    "qa_script": {
        "path": Path(__file__).relative_to(ROOT).as_posix(),
        "sha256": digest(Path(__file__)),
    },
}
receipt_text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
require(secret_pattern.search(receipt_text) is None, "Credential-shaped text in backend QA receipt")
RECEIPT.write_bytes(receipt_text.replace("\n", "\r\n").encode("utf-8"))
print(json.dumps(result, ensure_ascii=False))
