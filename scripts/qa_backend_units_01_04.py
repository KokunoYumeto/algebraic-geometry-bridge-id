#!/usr/bin/env python3
"""Fail-closed replay and closure QA for the cumulative Units 1--4 backend."""

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
EXPORTER = ROOT / "scripts" / "export_backend_units_01_04.py"
BACKEND = ROOT / "backend" / "units-01-04"
MANIFEST = BACKEND / "MANIFEST.json"
RECEIPT = ROOT / "qa" / "UNITS_01_04_BACKEND_QA.json"
BASELINE = ROOT / "backend" / "units-01-03"
BUILD_RECEIPT_PATH = ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json"
AUTHORITY_MANIFEST_PATH = ROOT / "authority" / "wikiversity" / "unit-04" / "UNIT_AUTHORITY_MANIFEST.json"
UNIT4_MAP_PATH = ROOT / "authority" / "wikiversity" / "unit-04" / "ORDERED_EXERCISE_MAP.json"
RIGHTS_PATH = ROOT / "authority" / "RIGHTS-unit-04.csv"
CLOSURE_PATH = ROOT / "authority" / "ASSET_CLOSURE-unit-04.json"
CORRECTIONS_PATH = ROOT / "00_control" / "CORRECTIONS.csv"
TERMINOLOGY_PATH = ROOT / "00_control" / "TERMINOLOGY.csv"

BASELINE_RECORDS_SHA256 = "5a54ed0b813145b57d3e81db41bc36c01cb94f9c39c7711f086117a09bb85a89"
BASELINE_RECORD_COUNT = 2003
CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-04.2026-08-22"

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

NEW_TERM_BINDINGS = {
    "AGT-0025": ("concept.irreducible-component", "komponen tak tereduksi"),
    "AGT-0026": ("concept.prime-ideal", "ideal prima"),
    "AGT-0027": ("concept.fraction-field", "medan pecahan"),
    "AGT-0028": ("concept.rational-function-field", "medan fungsi rasional"),
    "AGT-0029": ("concept.integral-domain", "domain integral"),
    "AGT-0030": ("concept.quotient-ring", "gelanggang hasil bagi"),
    "AGT-0031": ("concept.unique-factorization-domain", "domain faktorisasi tunggal"),
    "AGT-0032": ("concept.principal-ideal-domain", "domain ideal utama"),
    "AGT-0033": ("concept.closed-map", "pemetaan tertutup"),
    "AGT-0034": ("concept.open-map", "pemetaan terbuka"),
    "AGT-0035": ("concept.connected-space", "terhubung"),
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


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
    return first_manifest, second_manifest, text_digest(canonical(first_files))


first_manifest_sha256, second_manifest_sha256, export_tree_sha256 = replay()
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
require(manifest["through_unit"] == 4, "Manifest is not cumulative through Unit 4")
require(manifest["scope"] == "cumulative Units 1--4", "Manifest scope mismatch")

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
require(all(combined_lines), "JSONL contains a blank line")
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

require(digest(BASELINE / "records.jsonl") == BASELINE_RECORDS_SHA256, "Units 1--3 baseline hash changed")
baseline_raw_by_id: dict[str, str] = {}
for line in (BASELINE / "records.jsonl").read_text(encoding="utf-8").splitlines():
    baseline_raw_by_id[json.loads(line)["stable_id"]] = line
cumulative_raw_by_id = {json.loads(line)["stable_id"]: line for line in combined_lines}
require(len(baseline_raw_by_id) == BASELINE_RECORD_COUNT, "Frozen Units 1--3 baseline record count changed")
for stable_id, baseline_line in baseline_raw_by_id.items():
    require(cumulative_raw_by_id.get(stable_id) == baseline_line, f"Units 1--3 record bytes changed: {stable_id}")

ids = [record["stable_id"] for record in combined_records]
id_set = set(ids)
require(len(ids) == len(id_set), "Duplicate stable ID")
require(all(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", stable_id) for stable_id in ids), "Malformed stable ID")
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
        require(record["payload"].get("subject_id") in id_set, f"Missing relation subject for {record['stable_id']}")
        require(record["payload"].get("object_id") in id_set, f"Missing relation object for {record['stable_id']}")

counts = Counter(record["entity_class"] for record in combined_records)
require(dict(sorted(counts.items())) == manifest["counts"], "Manifest class counts do not replay")
require(len(combined_records) == manifest["record_count"], "Manifest record count does not replay")

build_receipt = json.loads(BUILD_RECEIPT_PATH.read_text(encoding="utf-8"))
require(build_receipt["schema"] == "ag-bridge-build-receipt-v2", "Reader build receipt schema mismatch")
require(build_receipt["through_unit"] == 4, "Reader build receipt scope mismatch")
require(manifest["reader_binding"]["build_receipt_sha256"] == digest(BUILD_RECEIPT_PATH), "Reader receipt binding mismatch")
for row in build_receipt["inputs"] + build_receipt["outputs"]:
    path = ROOT / row["path"]
    require(path.is_file(), f"Reader-bound file absent: {row['path']}")
    require(path.stat().st_size == row["bytes"], f"Reader-bound byte mismatch: {row['path']}")
    require(digest(path) == row["sha256"], f"Reader-bound hash mismatch: {row['path']}")

current_artifacts = {
    record["path"]: record
    for record in combined_records
    if record["entity_class"] == "artifact" and record["stable_id"].startswith("artifact.units0104.")
}
required_artifact_paths = [row["path"] for row in build_receipt["outputs"]] + [
    BUILD_RECEIPT_PATH.relative_to(ROOT).as_posix(),
    "qa/UNITS_01_04_MACHINE_QA.json",
    "qa/UNITS_01_04_VISUAL_QA.json",
    "qa/UNITS_01_04_RESPONSIVE_QA.json",
    "qa/UNIT_04_PROTECTED_SURFACES.json",
]
for path in required_artifact_paths:
    require(path in current_artifacts, f"Current reader artifact record absent: {path}")
for path, record in current_artifacts.items():
    local = ROOT / path
    require(local.stat().st_size == record["payload"]["bytes"], f"Artifact byte mismatch: {path}")
    require(digest(local) == record["content_sha256"], f"Artifact hash mismatch: {path}")
require(by_id[CUMULATIVE_EDITION]["content_sha256"] == digest(BUILD_RECEIPT_PATH), "Cumulative edition receipt hash mismatch")

authority_manifest = json.loads(AUTHORITY_MANIFEST_PATH.read_text(encoding="utf-8"))
require(authority_manifest["unit_number"] == 4, "Authority manifest unit mismatch")
authority_dir = AUTHORITY_MANIFEST_PATH.parent
for row in authority_manifest["files"]:
    path = authority_dir / row["file"]
    require(path.is_file(), f"Unit 4 authority file absent: {row['file']}")
    require(path.stat().st_size == row["bytes"], f"Unit 4 authority byte mismatch: {row['file']}")
    require(digest(path) == row["sha256"], f"Unit 4 authority hash mismatch: {row['file']}")


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


for source_name, authority_key in (("lecture-04.md", "lecture"), ("worksheet-04.md", "worksheet")):
    metadata = yaml_metadata(ROOT / "source" / "id-ID" / source_name)
    authority = authority_manifest[authority_key]
    require(int(metadata["upstream_pageid"]) == authority["pageid"], f"{source_name} pageid mismatch")
    require(int(metadata["upstream_revid"]) == authority["revid"], f"{source_name} revid mismatch")
    require(metadata["upstream_mediawiki_sha1"] == authority["mediawiki_sha1"], f"{source_name} SHA-1 mismatch")
    require(metadata["upstream_timestamp"] == authority["timestamp"], f"{source_name} timestamp mismatch")


def heading_ids(path: Path, pattern: str) -> list[str]:
    ids_found = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.search(r"\{#([^}]+)\}\s*$", line)
        if match and re.fullmatch(pattern, match.group(1)):
            ids_found.append(match.group(1))
    return ids_found


worksheet_path = ROOT / "source" / "id-ID" / "worksheet-04.md"
solutions_path = ROOT / "source" / "id-ID" / "worksheet-04-solutions.md"
exercises = heading_ids(worksheet_path, r"br-ak-2025-2026-w04-ex-\d{2}")
solutions = heading_ids(solutions_path, r"br-ak-2025-2026-w04-sol-\d{2}")
require(len(exercises) == 30, "Unit 4 exercise heading count mismatch")
require(len(solutions) == 6, "Unit 4 solution heading count mismatch")
authority_map = json.loads(UNIT4_MAP_PATH.read_text(encoding="utf-8"))
mapped_rows = {int(row["exercise_number"]): row for row in authority_map["entries"] if row.get("has_public_solution")}
mapped_numbers = sorted(mapped_rows)
source_solution_numbers = sorted(int(identifier.rsplit("-", 1)[-1]) for identifier in solutions)
require(source_solution_numbers == mapped_numbers == [10, 11, 12, 14, 15, 17], "Unit 4 solution-map mismatch")
require({f"exercise.{identifier}" for identifier in exercises} <= class_ids["exercise"], "Unit 4 exercise projections missing")
require({f"solution.{identifier}" for identifier in solutions} <= class_ids["solution"], "Unit 4 solution projections missing")

typed_solves = {
    (record["payload"]["subject_id"], record["payload"]["object_id"])
    for record in combined_records
    if record["entity_class"] == "relation"
    and record["payload"].get("relation_type") == "solves"
    and record["payload"].get("typed_family_projection") is True
}
for number, authority_row in mapped_rows.items():
    solution_id = f"solution.br-ak-2025-2026-w04-sol-{number:02d}"
    exercise_id = f"exercise.br-ak-2025-2026-w04-ex-{number:02d}"
    require((solution_id, exercise_id) in typed_solves, f"Typed solve relation absent: {solution_id}")
    binding = by_id[solution_id]["provenance"]["exercise_solution_authority"]
    require(binding["map_sha256"] == digest(UNIT4_MAP_PATH), f"Solution map hash absent: {solution_id}")
    require(binding["upstream"]["revid"] == authority_row["revid"], f"Solution revid mismatch: {solution_id}")
    require(binding["upstream"]["mediawiki_sha1"] == authority_row["mediawiki_sha1"], f"Solution SHA-1 mismatch: {solution_id}")
require(len(class_ids["exercise"]) == 107, "Cumulative exercise-family count mismatch")
require(len(class_ids["solution"]) == 24, "Cumulative solution-family count mismatch")

rights_rows = read_csv(RIGHTS_PATH)
closure = json.loads(CLOSURE_PATH.read_text(encoding="utf-8"))
require(len(rights_rows) == 9, "Unit 4 rights-row count mismatch")
require(closure["reader_media_positions"] == 9, "Unit 4 media-position mismatch")
require(closure["rights_sha256"] == digest(RIGHTS_PATH), "Unit 4 rights closure hash mismatch")
unique_local_paths: set[str] = set()
for row in rights_rows:
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
        companion_path = ROOT / row["pdf_local_path"]
        require(companion_path.stat().st_size == int(row["pdf_local_bytes"]), f"PDF companion bytes mismatch: {asset_id}")
        require(digest(companion_path) == row["pdf_local_sha256"], f"PDF companion hash mismatch: {asset_id}")
        require(asset["payload"]["pdf_companion"] == {
            "path": row["pdf_local_path"],
            "bytes": int(row["pdf_local_bytes"]),
            "sha256": row["pdf_local_sha256"],
        }, f"PDF companion record mismatch: {asset_id}")
        unique_local_paths.add(row["pdf_local_path"])
    else:
        require(asset["payload"]["pdf_companion"] is None, f"Unexpected PDF companion: {asset_id}")
require(len(unique_local_paths) == closure["unique_local_assets"] == 11, "Unit 4 unique-asset closure mismatch")
require(len(class_ids["asset"]) == 38, "Cumulative primary-asset count mismatch")

terminology_rows = read_csv(TERMINOLOGY_PATH)
terminology_by_id = {row["term_id"]: row for row in terminology_rows}
for term_id, (concept_id, preferred_target) in NEW_TERM_BINDINGS.items():
    require(term_id in terminology_by_id, f"Terminology control row missing: {term_id}")
    term_stable_id = f"term.{term_id.lower()}.id-id"
    require(concept_id in class_ids["concept"], f"Concept record missing: {concept_id}")
    require(term_stable_id in class_ids["term"], f"Term record missing: {term_stable_id}")
    require(by_id[term_stable_id]["parent_id"] == concept_id, f"Term parent mismatch: {term_stable_id}")
    require(by_id[term_stable_id]["payload"]["preferred_target"] == preferred_target, f"Term value mismatch: {term_stable_id}")
require(len(class_ids["concept"]) == 35 and len(class_ids["term"]) == 35, "Cumulative terminology-family count mismatch")

correction_rows = read_csv(CORRECTIONS_PATH)
require(len(correction_rows) == 9, "Current correction ledger does not contain nine rows")
require(len(class_ids["correction"]) == 9, "Cumulative correction-family count mismatch")
for row in correction_rows:
    stable_id = f"correction.{row['correction_id'].lower()}"
    require(stable_id in class_ids["correction"], f"Correction record absent: {stable_id}")
    correction = by_id[stable_id]
    require(correction["content_sha256"] == text_digest("\u241f".join(row.values())), f"Correction row hash mismatch: {stable_id}")
    require(correction["payload"]["kind"] == row["kind"], f"Correction kind mismatch: {stable_id}")
    require(correction["status"] == row["status"], f"Correction status mismatch: {stable_id}")

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
    "through_unit": 4,
    "manifest_path": MANIFEST.relative_to(ROOT).as_posix(),
    "manifest_sha256": second_manifest_sha256,
    "export_tree_sha256": export_tree_sha256,
    "deterministic_double_replay": first_manifest_sha256 == second_manifest_sha256,
    "record_count": len(combined_records),
    "class_counts": dict(sorted(counts.items())),
    "jsonl_parse_errors": 0,
    "json_schema_errors": 0,
    "unique_and_well_formed_stable_ids": True,
    "units_01_03_record_bytes_preserved": len(baseline_raw_by_id),
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
        "unit_4_manifest_sha256": digest(AUTHORITY_MANIFEST_PATH),
        "file_count": len(authority_manifest["files"]),
        "lecture_revid": authority_manifest["lecture"]["revid"],
        "worksheet_revid": authority_manifest["worksheet"]["revid"],
    },
    "exercise_solution_mapping": {
        "unit_04": {
            "exercise_count": len(exercises),
            "solution_count": len(solutions),
            "map_sha256": digest(UNIT4_MAP_PATH),
            "typed_solve_relations": len(mapped_numbers),
        },
        "cumulative_exercises": len(class_ids["exercise"]),
        "cumulative_solutions": len(class_ids["solution"]),
    },
    "rights_and_assets": {
        "unit_04": {
            "positions": len(rights_rows),
            "unique_local_assets": len(unique_local_paths),
            "rights_sha256": digest(RIGHTS_PATH),
            "closure_sha256": digest(CLOSURE_PATH),
        },
        "cumulative_assets": len(class_ids["asset"]),
    },
    "terminology": {
        "control_sha256": digest(TERMINOLOGY_PATH),
        "unit_04_rows": sorted(NEW_TERM_BINDINGS),
        "cumulative_concepts": len(class_ids["concept"]),
        "cumulative_terms": len(class_ids["term"]),
    },
    "corrections": {
        "rows": len(correction_rows),
        "ledger_sha256": digest(CORRECTIONS_PATH),
        "unit_04_additions": 2,
    },
    "credential_findings": 0,
    "check_families": [
        "jsonl_parse_canonical_serialization_and_json_schema",
        "stable_id_uniqueness_format_and_units0103_byte_preservation",
        "parent_relation_resource_edition_rights_and_concept_closure",
        "class_projection_round_trip",
        "deterministic_double_export_and_file_tree_identity",
        "reader_build_receipt_input_output_and_artifact_hash_bindings",
        "unit4_revision_authority_manifest_and_file_hash_replay",
        "unit4_exercise_solution_family_and_map_closure",
        "unit4_component_rights_asset_and_hash_closure",
        "unit4_terminology_control_and_concept_term_closure",
        "nine_row_correction_ledger_hash_closure",
        "credential_pattern_scan",
    ],
    "replay_command": f'"{sys.executable}" "{Path(__file__).relative_to(ROOT).as_posix()}"',
    "exporter": {"path": EXPORTER.relative_to(ROOT).as_posix(), "sha256": digest(EXPORTER)},
    "qa_script": {"path": Path(__file__).relative_to(ROOT).as_posix(), "sha256": digest(Path(__file__))},
}
receipt_text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
require(secret_pattern.search(receipt_text) is None, "Credential-shaped text in backend QA receipt")
RECEIPT.write_bytes(receipt_text.replace("\n", "\r\n").encode("utf-8"))
print(json.dumps(result, ensure_ascii=False))
