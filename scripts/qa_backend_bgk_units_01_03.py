#!/usr/bin/env python3
"""Fail-closed deterministic, prefix-identity QA for BGK Units 1--3."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "scripts" / "export_backend_bgk_units_01_03.py"
BACKEND = ROOT / "backend" / "bgk-units-01-03"
BASE = ROOT / "backend" / "bgk-units-01-02"
MANIFEST = BACKEND / "MANIFEST.json"
RECORDS = BACKEND / "records.jsonl"
CLASSICAL_RECORDS = ROOT / "backend" / "units-01-30" / "records.jsonl"
TRANSLATION_QA = ROOT / "qa" / "BGK_UNIT_03_TRANSLATION_QA.json"
RECEIPT = ROOT / "qa" / "BGK_UNITS_01_03_BACKEND_QA.json"
MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def run_exporter() -> dict[str, str]:
    process = subprocess.run([sys.executable, str(EXPORTER)], cwd=ROOT, check=True,
                             capture_output=True, text=True)
    return {"stdout_sha256": hashlib.sha256(process.stdout.encode("utf-8")).hexdigest(),
            "manifest_sha256": digest(MANIFEST), "records_sha256": digest(RECORDS)}


first = run_exporter()
first_file_hashes = {path.name: digest(path) for path in sorted(BACKEND.iterdir(), key=lambda p: p.name)
                     if path.is_file()}
second = run_exporter()
second_file_hashes = {path.name: digest(path) for path in sorted(BACKEND.iterdir(), key=lambda p: p.name)
                      if path.is_file()}
if first != second or first_file_hashes != second_file_hashes:
    raise RuntimeError("Cumulative BGK Units 1--3 backend double replay is not byte deterministic")

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if (manifest.get("through_unit") != 3 or manifest.get("exercise_count") != 62 or
        manifest.get("unit3_exercise_count") != 18 or manifest.get("public_solution_count") != 2 or
        manifest.get("component_asset_count") != 5 or manifest.get("unit3_component_asset_count") != 0):
    raise RuntimeError("Cumulative BGK Units 1--3 manifest scope drifted")
if manifest.get("model_provenance") != MODEL_PROVENANCE:
    raise RuntimeError("Exact model provenance is absent from cumulative BGK manifest")
for binding in manifest["files"] + manifest["source_bindings"]:
    path = ROOT / binding["path"]
    if not path.is_file() or path.stat().st_size != binding["bytes"] or digest(path) != binding["sha256"]:
        raise RuntimeError(f"Cumulative BGK backend binding replay mismatch: {binding['path']}")

base_bytes = (BASE / "records.jsonl").read_bytes()
records_bytes = RECORDS.read_bytes()
if not records_bytes.startswith(base_bytes) or records_bytes[:len(base_bytes)] != base_bytes:
    raise RuntimeError("Accepted Units 1--2 records are not the exact byte prefix")

schema = json.loads((BACKEND / "record.schema.json").read_text(encoding="utf-8"))
validator = Draft202012Validator(schema)
records = read_jsonl(RECORDS)
schema_errors = [error.message for row in records for error in validator.iter_errors(row)]
if schema_errors:
    raise RuntimeError(f"Cumulative BGK backend JSON Schema errors: {schema_errors[:5]}")

base_records = read_jsonl(BASE / "records.jsonl")
base_ids = {row["stable_id"] for row in base_records}
if len(base_records) != len(base_ids) or len(base_records) != manifest["units_01_02_baseline_record_count"]:
    raise RuntimeError("Units 1--2 immutable baseline count drifted")
if [canonical(row) for row in records[:len(base_records)]] != [canonical(row) for row in base_records]:
    raise RuntimeError("Units 1--2 logical record prefix drifted")

entity_classes = list(schema["properties"]["entity_class"]["enum"])
class_records: list[dict] = []
class_prefix_hashes: dict[str, str] = {}
for entity_class in entity_classes:
    base_path = BASE / f"{entity_class}.jsonl"
    path = BACKEND / f"{entity_class}.jsonl"
    if not path.is_file() or not path.read_bytes().startswith(base_path.read_bytes()):
        raise RuntimeError(f"Units 1--2 {entity_class} projection is not an exact byte prefix")
    rows = read_jsonl(path)
    if any(row["entity_class"] != entity_class for row in rows):
        raise RuntimeError(f"Wrong entity class in {path.name}")
    class_records.extend(rows)
    class_prefix_hashes[entity_class] = digest(base_path)
if Counter(canonical(row) for row in records) != Counter(canonical(row) for row in class_records):
    raise RuntimeError("records.jsonl is not the exact set union of class projections")

ids = [row["stable_id"] for row in records]
id_set = set(ids)
if len(ids) != len(id_set):
    raise RuntimeError("Duplicate cumulative BGK stable ID")
for row in records:
    if row["parent_id"] is not None and row["parent_id"] not in id_set:
        raise RuntimeError(f"Missing cumulative BGK parent: {row['stable_id']}")
    if row["rights_id"] is not None and row["rights_id"] not in id_set:
        raise RuntimeError(f"Missing cumulative BGK rights record: {row['stable_id']}")
    if any(concept_id not in id_set for concept_id in row["concept_ids"]):
        raise RuntimeError(f"Missing cumulative BGK concept record: {row['stable_id']}")
    if row["entity_class"] == "relation" and (
            row["payload"]["subject_id"] not in id_set or row["payload"]["object_id"] not in id_set):
        raise RuntimeError(f"Missing cumulative BGK relation endpoint: {row['stable_id']}")

counts = dict(sorted(Counter(row["entity_class"] for row in records).items()))
if counts != manifest["counts"] or len(records) != manifest["record_count"]:
    raise RuntimeError("Cumulative BGK manifest count replay mismatch")
if len(records) - len(base_records) != manifest["unit3_added_record_count"]:
    raise RuntimeError("Cumulative BGK Unit 3 added-record count mismatch")

expected_exercises = ([f"br-bgk-2019-w01-ex{n:02d}" for n in range(1, 18)] +
                      [f"br-bgk-2019-w02-ex{n:02d}" for n in range(1, 28)] +
                      [f"br-bgk-2019-w03-ex{n:02d}" for n in range(1, 19)])
exercise_ids = sorted(row["stable_id"] for row in records if row["entity_class"] == "exercise")
if exercise_ids != sorted(expected_exercises):
    raise RuntimeError("Cumulative BGK exercise IDs are not exact 17+27+18 closure")
solution_rows = sorted((row for row in records if row["entity_class"] == "solution"),
                       key=lambda row: row["stable_id"])
if [row["stable_id"] for row in solution_rows] != [
        "br-bgk-2019-w02-ex04-solution", "br-bgk-2019-w03-ex01-solution"]:
    raise RuntimeError("Cumulative BGK public-solution IDs are not the exact frozen closure")
u3_solution = solution_rows[1]
if (u3_solution["parent_id"] != "br-bgk-2019-w03-ex01" or
        u3_solution["payload"].get("invented") is not False or
        u3_solution["payload"].get("source_pageid") != 125430 or
        u3_solution["payload"].get("source_revid") != 1095037):
    raise RuntimeError("BGK Unit 3 solution is not the exact frozen public Exercise 3.1 solution")

asset_ids = {row["stable_id"] for row in records if row["entity_class"] == "asset"}
base_asset_ids = {row["stable_id"] for row in base_records if row["entity_class"] == "asset"}
if asset_ids != base_asset_ids or len(asset_ids) != 5:
    raise RuntimeError("Unit 3 zero-media closure altered the accepted component assets")

translation_qa = json.loads(TRANSLATION_QA.read_text(encoding="utf-8"))
referenced_terms = set(translation_qa["terminology_ids_added"] + translation_qa["terminology_ids_reused"])
all_term_local_ids = {row["source_local_id"] for row in records if row["entity_class"] == "term"}
if len(referenced_terms) != 34 or not referenced_terms.issubset(all_term_local_ids):
    raise RuntimeError("BGK Unit 3 terminology references are not fully represented")
base_term_local_ids = {row["source_local_id"] for row in base_records if row["entity_class"] == "term"}
unit3_term_local_ids = {row["source_local_id"] for row in records[len(base_records):]
                        if row["entity_class"] == "term"}
if unit3_term_local_ids != referenced_terms - base_term_local_ids:
    raise RuntimeError("BGK Unit 3 appended terminology record closure drifted")
unit3_correction_ids = {row["source_local_id"] for row in records[len(base_records):]
                        if row["entity_class"] == "correction"}
if unit3_correction_ids != {f"AGC-CORR-{n:04d}" for n in range(149, 154)}:
    raise RuntimeError("BGK Unit 3 correction closure is not exactly AGC-CORR-0149..0153")

source_heading_ids = [row["stable_id"] for row in records
                      if row["source_local_id"] == row["stable_id"] and
                      row["stable_id"].startswith("br-bgk-2019-") and
                      row["payload"].get("heading_level") is not None]
if len(source_heading_ids) != manifest["source_heading_id_count"]:
    raise RuntimeError("Cumulative BGK source-heading count drifted")
unit3_heading_ids = [value for value in source_heading_ids if value not in base_ids]
if len(unit3_heading_ids) != manifest["unit3_source_heading_id_count"] or len(unit3_heading_ids) != 58:
    raise RuntimeError("BGK Unit 3 source-heading count drifted")

new_records = records[len(base_records):]
if not new_records or any(row["provenance"].get("model") != MODEL_PROVENANCE for row in new_records):
    raise RuntimeError("Exact model provenance is missing from one or more Unit 3 records")

qa_event_ids = {row["stable_id"] for row in records if row["entity_class"] == "qa_event"}
required_qa_events = {"qa.br-bgk-2019.u03.authority-closure",
                      "qa.br-bgk-2019.u03.translation-closure",
                      "qa.br-bgk-2019.u03.media-closure"}
if not required_qa_events.issubset(qa_event_ids):
    raise RuntimeError("BGK Unit 3 authority, translation, and zero-media QA events are not all bound")

classical_ids: set[str] = set()
with CLASSICAL_RECORDS.open("r", encoding="utf-8") as stream:
    for line in stream:
        if line.strip():
            classical_ids.add(json.loads(line)["stable_id"])
intersection = sorted(id_set & classical_ids)
if intersection:
    raise RuntimeError(f"BGK/classical stable-ID collision: {intersection[:5]}")

secret_patterns = [
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]{16,}", re.IGNORECASE),
    re.compile(r"(?:api[_-]?key|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{12,}", re.IGNORECASE),
]
serialized = RECORDS.read_text(encoding="utf-8")
if any(pattern.search(serialized) for pattern in secret_patterns):
    raise RuntimeError("Credential-like material found in cumulative BGK backend")

result = {
    "schema": "ag-bridge-bgk-native-backend-qa-receipt-v1",
    "tested_authority_utc": manifest["generated_from_authority_utc"],
    "status": "PASS",
    "through_unit": 3,
    "manifest_path": MANIFEST.relative_to(ROOT).as_posix(),
    "manifest_bytes": MANIFEST.stat().st_size,
    "manifest_sha256": second["manifest_sha256"],
    "records_path": RECORDS.relative_to(ROOT).as_posix(),
    "records_bytes": RECORDS.stat().st_size,
    "records_sha256": second["records_sha256"],
    "record_count": len(records),
    "units_01_02_baseline_record_count": len(base_records),
    "unit3_added_record_count": len(new_records),
    "class_counts": counts,
    "source_heading_id_count": len(source_heading_ids),
    "unit3_source_heading_id_count": len(unit3_heading_ids),
    "exercise_count": len(exercise_ids),
    "unit3_exercise_count": 18,
    "public_solution_count": len(solution_rows),
    "component_asset_count": len(asset_ids),
    "unit3_component_asset_count": 0,
    "unit3_referenced_term_count": len(referenced_terms),
    "unit3_appended_term_record_count": len(unit3_term_local_ids),
    "unit3_correction_count": len(unit3_correction_ids),
    "deterministic_double_replay": True,
    "all_export_file_hashes_stable": first_file_hashes == second_file_hashes,
    "json_schema_errors": 0,
    "records_set_projection_round_trip": True,
    "units_01_02_records_byte_prefix_identity": True,
    "units_01_02_class_projection_byte_prefix_identity": True,
    "units_01_02_records_prefix_bytes": len(base_bytes),
    "units_01_02_records_prefix_sha256": digest(BASE / "records.jsonl"),
    "units_01_02_class_prefix_sha256": class_prefix_hashes,
    "unique_stable_ids": True,
    "parent_rights_concept_and_relation_endpoint_closure": True,
    "source_heading_namespace": "br-bgk-2019-*",
    "exact_62_exercise_two_public_solution_closure": True,
    "authority_translation_and_zero_media_qa_bound": True,
    "exact_unit3_terminology_and_correction_ledger_closure": True,
    "all_unit3_records_carry_exact_model_provenance": True,
    "credential_pattern_hits": 0,
    "model_provenance": MODEL_PROVENANCE,
    "classical_collision_baseline": {
        "path": CLASSICAL_RECORDS.relative_to(ROOT).as_posix(),
        "sha256": digest(CLASSICAL_RECORDS),
        "classical_stable_id_count": len(classical_ids),
        "intersection_count": len(intersection),
    },
    "exporter": {"path": EXPORTER.relative_to(ROOT).as_posix(), "bytes": EXPORTER.stat().st_size,
                 "sha256": digest(EXPORTER)},
    "qa_script": {"path": Path(__file__).relative_to(ROOT).as_posix(),
                  "bytes": Path(__file__).stat().st_size, "sha256": digest(Path(__file__))},
}
RECEIPT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8", newline="\n")
print(json.dumps(result, ensure_ascii=False))
