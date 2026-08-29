#!/usr/bin/env python3
"""Fail-closed deterministic and cumulative-identity QA for BGK Units 1--2."""

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
EXPORTER = ROOT / "scripts" / "export_backend_bgk_units_01_02.py"
BACKEND = ROOT / "backend" / "bgk-units-01-02"
BASE = ROOT / "backend" / "bgk-units-01"
MANIFEST = BACKEND / "MANIFEST.json"
RECORDS = BACKEND / "records.jsonl"
CLASSICAL_RECORDS = ROOT / "backend" / "units-01-30" / "records.jsonl"
RECEIPT = ROOT / "qa" / "BGK_UNITS_01_02_BACKEND_QA.json"
MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def jsonl_bytes(rows: list[dict]) -> bytes:
    return "".join(canonical(row) + "\r\n" for row in rows).encode("utf-8")


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def run_exporter() -> dict[str, str]:
    process = subprocess.run([sys.executable, str(EXPORTER)], cwd=ROOT, check=True,
                             capture_output=True, text=True)
    return {
        "stdout_sha256": hashlib.sha256(process.stdout.encode("utf-8")).hexdigest(),
        "manifest_sha256": digest(MANIFEST),
        "records_sha256": digest(RECORDS),
    }


first = run_exporter()
first_file_hashes = {
    path.name: digest(path)
    for path in sorted(BACKEND.iterdir(), key=lambda item: item.name)
    if path.is_file()
}
second = run_exporter()
second_file_hashes = {
    path.name: digest(path)
    for path in sorted(BACKEND.iterdir(), key=lambda item: item.name)
    if path.is_file()
}
if first != second or first_file_hashes != second_file_hashes:
    raise RuntimeError("Cumulative BGK native backend double replay is not byte deterministic")

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if (manifest.get("through_unit") != 2 or manifest.get("exercise_count") != 44 or
        manifest.get("unit2_exercise_count") != 27 or manifest.get("public_solution_count") != 1 or
        manifest.get("component_asset_count") != 5 or manifest.get("unit2_component_asset_count") != 4):
    raise RuntimeError("Cumulative BGK Units 1--2 manifest scope drifted")
if manifest.get("model_provenance") != MODEL_PROVENANCE:
    raise RuntimeError("Exact model provenance is absent from cumulative BGK manifest")

for binding in manifest["files"] + manifest["source_bindings"]:
    path = ROOT / binding["path"]
    if not path.is_file() or path.stat().st_size != binding["bytes"] or digest(path) != binding["sha256"]:
        raise RuntimeError(f"Cumulative BGK backend binding replay mismatch: {binding['path']}")

schema = json.loads((BACKEND / "record.schema.json").read_text(encoding="utf-8"))
validator = Draft202012Validator(schema)
records = read_jsonl(RECORDS)
schema_errors: list[str] = []
for row in records:
    schema_errors.extend(error.message for error in validator.iter_errors(row))
if schema_errors:
    raise RuntimeError(f"Cumulative BGK backend JSON Schema errors: {schema_errors[:5]}")

entity_classes = list(schema["properties"]["entity_class"]["enum"])
class_records: list[dict] = []
for entity_class in entity_classes:
    path = BACKEND / f"{entity_class}.jsonl"
    if not path.is_file():
        raise RuntimeError(f"Missing cumulative BGK class projection: {path.name}")
    rows = read_jsonl(path)
    if any(row["entity_class"] != entity_class for row in rows):
        raise RuntimeError(f"Wrong entity class in {path.name}")
    class_records.extend(rows)
if [canonical(row) for row in records] != [canonical(row) for row in sorted(
        class_records, key=lambda row: (row["entity_class"], row["stable_id"]))]:
    raise RuntimeError("Cumulative records.jsonl is not the exact ordered union of class projections")

base_records = read_jsonl(BASE / "records.jsonl")
base_ids = {row["stable_id"] for row in base_records}
if len(base_records) != len(base_ids) or len(base_records) != manifest["unit1_baseline_record_count"]:
    raise RuntimeError("Unit 1 immutable baseline count drifted")
for entity_class in entity_classes:
    baseline_bytes = (BASE / f"{entity_class}.jsonl").read_bytes()
    cumulative_baseline_rows = [row for row in read_jsonl(BACKEND / f"{entity_class}.jsonl")
                                if row["stable_id"] in base_ids]
    if jsonl_bytes(cumulative_baseline_rows) != baseline_bytes:
        raise RuntimeError(f"Unit 1 {entity_class} payload or record bytes changed in cumulative projection")

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
    if row["entity_class"] == "relation":
        if row["payload"]["subject_id"] not in id_set or row["payload"]["object_id"] not in id_set:
            raise RuntimeError(f"Missing cumulative BGK relation endpoint: {row['stable_id']}")

counts = dict(sorted(Counter(row["entity_class"] for row in records).items()))
if counts != manifest["counts"] or len(records) != manifest["record_count"]:
    raise RuntimeError("Cumulative BGK manifest count replay mismatch")
if len(records) - len(base_records) != manifest["unit2_added_record_count"]:
    raise RuntimeError("Cumulative BGK Unit 2 added-record count mismatch")

unit1_exercises = [f"br-bgk-2019-w01-ex{number:02d}" for number in range(1, 18)]
unit2_exercises = [f"br-bgk-2019-w02-ex{number:02d}" for number in range(1, 28)]
exercise_ids = sorted(row["stable_id"] for row in records if row["entity_class"] == "exercise")
if exercise_ids != sorted(unit1_exercises + unit2_exercises):
    raise RuntimeError("Cumulative BGK exercise IDs are not exact 17+27 closure")
solution_rows = [row for row in records if row["entity_class"] == "solution"]
if ([row["stable_id"] for row in solution_rows] != ["br-bgk-2019-w02-ex04-solution"] or
        solution_rows[0]["parent_id"] != "br-bgk-2019-w02-ex04" or
        solution_rows[0]["payload"].get("invented") is not False or
        solution_rows[0]["payload"].get("source_pageid") != 77727 or
        solution_rows[0]["payload"].get("source_revid") != 1096699):
    raise RuntimeError("Cumulative BGK public solution is not exact frozen Exercise 2.4 closure")

expected_assets = {
    "br-bgk-u01-media-001",
    "br-bgk-u02-media-001",
    "br-bgk-u02-media-002",
    "br-bgk-u02-media-003",
    "br-bgk-u02-media-003-pdf-frame-001",
}
asset_ids = {row["stable_id"] for row in records if row["entity_class"] == "asset"}
if asset_ids != expected_assets:
    raise RuntimeError("Cumulative BGK component-asset IDs are not exact 1+4 closure")

qa_event_ids = {row["stable_id"] for row in records if row["entity_class"] == "qa_event"}
required_qa_events = {
    "qa.br-bgk-2019.u02.authority-closure",
    "qa.br-bgk-2019.u02.translation-closure",
    "qa.br-bgk-2019.u02.media-closure",
}
if not required_qa_events.issubset(qa_event_ids):
    raise RuntimeError("BGK Unit 2 authority, translation, and media QA events are not all bound")

expected_unit2_term_ids = {
    "AGT-0241",
    *(f"AGT-{number:04d}" for number in range(290, 299)),
}
unit2_term_ids = {
    row["source_local_id"] for row in records
    if row["stable_id"] not in base_ids and row["entity_class"] == "term"
}
if unit2_term_ids != expected_unit2_term_ids:
    raise RuntimeError("BGK Unit 2 terminology closure is not exactly AGT-0241 and AGT-0290..AGT-0298")
expected_unit2_correction_ids = {f"AGC-CORR-{number:04d}" for number in range(142, 149)}
unit2_correction_ids = {
    row["source_local_id"] for row in records
    if row["stable_id"] not in base_ids and row["entity_class"] == "correction"
}
if unit2_correction_ids != expected_unit2_correction_ids:
    raise RuntimeError("BGK Unit 2 correction closure is not exactly AGC-CORR-0142..AGC-CORR-0148")

source_heading_ids = [
    row["stable_id"] for row in records
    if row["source_local_id"] == row["stable_id"] and row["stable_id"].startswith("br-bgk-2019-")
    and row["payload"].get("heading_level") is not None
]
if len(source_heading_ids) != manifest["source_heading_id_count"]:
    raise RuntimeError("Cumulative BGK source-heading count drifted")
unit2_heading_ids = [value for value in source_heading_ids if value not in base_ids]
if len(unit2_heading_ids) != manifest["unit2_source_heading_id_count"]:
    raise RuntimeError("BGK Unit 2 source-heading count drifted")

new_records = [row for row in records if row["stable_id"] not in base_ids]
if not new_records or any(row["provenance"].get("model") != MODEL_PROVENANCE for row in new_records):
    raise RuntimeError("Exact model provenance is missing from one or more Unit 2 records")

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
    re.compile(r"(?:api[_-]?key|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9._~+/=-]{12,}",
               re.IGNORECASE),
]
serialized = RECORDS.read_text(encoding="utf-8")
if any(pattern.search(serialized) for pattern in secret_patterns):
    raise RuntimeError("Credential-like material found in cumulative BGK backend")

result = {
    "schema": "ag-bridge-bgk-native-backend-qa-receipt-v1",
    "tested_authority_utc": manifest["generated_from_authority_utc"],
    "status": "PASS",
    "through_unit": 2,
    "manifest_path": MANIFEST.relative_to(ROOT).as_posix(),
    "manifest_bytes": MANIFEST.stat().st_size,
    "manifest_sha256": second["manifest_sha256"],
    "records_path": RECORDS.relative_to(ROOT).as_posix(),
    "records_bytes": RECORDS.stat().st_size,
    "records_sha256": second["records_sha256"],
    "record_count": len(records),
    "unit1_baseline_record_count": len(base_records),
    "unit2_added_record_count": len(records) - len(base_records),
    "class_counts": counts,
    "source_heading_id_count": len(source_heading_ids),
    "unit2_source_heading_id_count": len(unit2_heading_ids),
    "exercise_count": len(exercise_ids),
    "unit2_exercise_count": len(unit2_exercises),
    "public_solution_count": len(solution_rows),
    "component_asset_count": len(asset_ids),
    "deterministic_double_replay": True,
    "all_export_file_hashes_stable": first_file_hashes == second_file_hashes,
    "json_schema_errors": 0,
    "class_projection_round_trip": True,
    "unit1_class_projection_byte_identity": True,
    "unique_stable_ids": True,
    "parent_rights_concept_and_relation_endpoint_closure": True,
    "source_heading_namespace": "br-bgk-2019-*",
    "exact_44_exercise_one_public_solution_closure": True,
    "authority_translation_and_media_qa_bound": True,
    "unit2_term_count": len(unit2_term_ids),
    "unit2_correction_count": len(unit2_correction_ids),
    "exact_unit2_terminology_and_correction_ledger_closure": True,
    "all_unit2_records_carry_exact_model_provenance": True,
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
