#!/usr/bin/env python3
"""Fail-closed deterministic, prefix-identity QA for BGK Units 1--6."""

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
EXPORTER = ROOT / "scripts" / "export_backend_bgk_units_01_06.py"
BACKEND = ROOT / "backend" / "bgk-units-01-06"
BASE = ROOT / "backend" / "bgk-units-01-04"
MANIFEST = BACKEND / "MANIFEST.json"
RECORDS = BACKEND / "records.jsonl"
CLASSICAL_RECORDS = ROOT / "backend" / "units-01-30" / "records.jsonl"
UNIT5_TRANSLATION_QA = ROOT / "qa" / "BGK_UNIT_05_TRANSLATION_QA.json"
UNIT6_TRANSLATION_QA = ROOT / "qa" / "BGK_UNIT_06_TRANSLATION_QA.json"
READER_QA = ROOT / "qa" / "BGK_UNITS_01_06_READER_QA.json"
RECEIPT = ROOT / "qa" / "BGK_UNITS_01_06_BACKEND_QA.json"
MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def canonical(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


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
    path.name: digest(path) for path in sorted(BACKEND.iterdir(), key=lambda item: item.name)
    if path.is_file()
}
second = run_exporter()
second_file_hashes = {
    path.name: digest(path) for path in sorted(BACKEND.iterdir(), key=lambda item: item.name)
    if path.is_file()
}
if first != second or first_file_hashes != second_file_hashes:
    raise RuntimeError("Cumulative BGK Units 1--6 backend double replay is not byte deterministic")

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if (manifest.get("through_unit") != 6 or manifest.get("exercise_count") != 101 or
        manifest.get("unit5_exercise_count") != 11 or manifest.get("unit6_exercise_count") != 19 or
        manifest.get("public_solution_count") != 3 or manifest.get("unit5_public_solution_count") != 1 or
        manifest.get("unit6_public_solution_count") != 0 or manifest.get("component_asset_count") != 6 or
        manifest.get("units_05_06_component_asset_count") != 0 or
        manifest.get("units_05_06_appended_term_record_count") != 20 or
        manifest.get("unit5_correction_count") != 6 or manifest.get("unit6_correction_count") != 5):
    raise RuntimeError("Cumulative BGK Units 1--6 manifest scope drifted")
if manifest.get("model_provenance") != MODEL_PROVENANCE:
    raise RuntimeError("Exact model provenance is absent from cumulative BGK manifest")
for binding in manifest["files"] + manifest["source_bindings"]:
    path = ROOT / binding["path"]
    if not path.is_file() or path.stat().st_size != binding["bytes"] or digest(path) != binding["sha256"]:
        raise RuntimeError(f"Cumulative BGK backend binding replay mismatch: {binding['path']}")

base_bytes = (BASE / "records.jsonl").read_bytes()
records_bytes = RECORDS.read_bytes()
if not records_bytes.startswith(base_bytes) or records_bytes[:len(base_bytes)] != base_bytes:
    raise RuntimeError("Accepted Units 1--4 records are not the exact byte prefix")

schema = json.loads((BACKEND / "record.schema.json").read_text(encoding="utf-8"))
validator = Draft202012Validator(schema)
records = read_jsonl(RECORDS)
schema_errors = [error.message for row in records for error in validator.iter_errors(row)]
if schema_errors:
    raise RuntimeError(f"Cumulative BGK backend JSON Schema errors: {schema_errors[:5]}")

base_records = read_jsonl(BASE / "records.jsonl")
base_ids = {row["stable_id"] for row in base_records}
if len(base_records) != len(base_ids) or len(base_records) != manifest["units_01_04_baseline_record_count"]:
    raise RuntimeError("Units 1--4 immutable baseline count drifted")
if [canonical(row) for row in records[:len(base_records)]] != [canonical(row) for row in base_records]:
    raise RuntimeError("Units 1--4 logical record prefix drifted")

entity_classes = list(schema["properties"]["entity_class"]["enum"])
class_records: list[dict] = []
class_prefix_hashes: dict[str, str] = {}
for entity_class in entity_classes:
    base_path = BASE / f"{entity_class}.jsonl"
    path = BACKEND / f"{entity_class}.jsonl"
    if not path.is_file() or not path.read_bytes().startswith(base_path.read_bytes()):
        raise RuntimeError(f"Units 1--4 {entity_class} projection is not an exact byte prefix")
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
new_records = records[len(base_records):]
if len(new_records) != manifest["units_05_06_added_record_count"]:
    raise RuntimeError("Cumulative BGK Units 5--6 added-record count mismatch")

expected_exercises = (
    [f"br-bgk-2019-w01-ex{n:02d}" for n in range(1, 18)] +
    [f"br-bgk-2019-w02-ex{n:02d}" for n in range(1, 28)] +
    [f"br-bgk-2019-w03-ex{n:02d}" for n in range(1, 19)] +
    [f"br-bgk-2019-w04-ex{n:02d}" for n in range(1, 10)] +
    [f"br-bgk-2019-w05-ex{n:02d}" for n in range(1, 12)] +
    [f"br-bgk-2019-w06-ex{n:02d}" for n in range(1, 20)]
)
exercise_ids = sorted(row["stable_id"] for row in records if row["entity_class"] == "exercise")
if exercise_ids != sorted(expected_exercises):
    raise RuntimeError("Cumulative BGK exercise IDs are not exact 17+27+18+9+11+19 closure")
solution_ids = sorted(row["stable_id"] for row in records if row["entity_class"] == "solution")
expected_solutions = [
    "br-bgk-2019-w02-ex04-solution",
    "br-bgk-2019-w03-ex01-solution",
    "br-bgk-2019-w05-ex05-solution",
]
if solution_ids != expected_solutions:
    raise RuntimeError("Cumulative BGK public-solution IDs are not the exact frozen closure")
new_solution_ids = {row["stable_id"] for row in new_records if row["entity_class"] == "solution"}
if new_solution_ids != {"br-bgk-2019-w05-ex05-solution"}:
    raise RuntimeError("Units 5--6 invented or omitted a public solution record")

asset_ids = {row["stable_id"] for row in records if row["entity_class"] == "asset"}
base_asset_ids = {row["stable_id"] for row in base_records if row["entity_class"] == "asset"}
if asset_ids != base_asset_ids or len(asset_ids) != 6:
    raise RuntimeError("Units 5--6 violated their zero-reader-media component closure")
if any(row["entity_class"] == "segment" and row["payload"].get("kind") == "image" for row in new_records):
    raise RuntimeError("Units 5--6 backend appended an image block despite zero-media closure")

unit5_qa = json.loads(UNIT5_TRANSLATION_QA.read_text(encoding="utf-8"))
unit6_qa = json.loads(UNIT6_TRANSLATION_QA.read_text(encoding="utf-8"))
expected_unit5_terms = {f"AGT-{n:04d}" for n in range(324, 334)}
expected_unit6_terms = {f"AGT-{n:04d}" for n in range(334, 344)}
if set(unit5_qa["terminology_ids_added"]) != expected_unit5_terms or set(unit6_qa["terminology_ids_added"]) != expected_unit6_terms:
    raise RuntimeError("Units 5--6 terminology-QA identity drifted")
new_term_ids = {row["source_local_id"] for row in new_records if row["entity_class"] == "term"}
if new_term_ids != expected_unit5_terms | expected_unit6_terms:
    raise RuntimeError("Units 5--6 appended terminology record closure drifted")

expected_unit5_corrections = {f"AGC-CORR-{n:04d}" for n in range(159, 165)}
expected_unit6_corrections = {f"AGC-CORR-{n:04d}" for n in range(165, 170)}
if set(unit5_qa["correction_ids"]) != expected_unit5_corrections or set(unit6_qa["correction_ids"]) != expected_unit6_corrections:
    raise RuntimeError("Units 5--6 correction-QA identity drifted")
new_correction_ids = {row["source_local_id"] for row in new_records if row["entity_class"] == "correction"}
if new_correction_ids != expected_unit5_corrections | expected_unit6_corrections:
    raise RuntimeError("Units 5--6 appended correction record closure drifted")

source_heading_ids = [
    row["stable_id"] for row in records
    if row["source_local_id"] == row["stable_id"] and
    row["stable_id"].startswith("br-bgk-2019-") and
    row["payload"].get("heading_level") is not None
]
if len(source_heading_ids) != manifest["source_heading_id_count"] or len(source_heading_ids) != 256:
    raise RuntimeError("Cumulative BGK source-heading count drifted")
new_source_heading_ids = [value for value in source_heading_ids if value not in base_ids]
if len(new_source_heading_ids) != 76:
    raise RuntimeError("Units 5--6 plus cumulative frontmatter source-heading count drifted")
if (sum(value.startswith("br-bgk-2019-l05") or value.startswith("br-bgk-2019-w05")
        for value in new_source_heading_ids) != 29 or
        sum(value.startswith("br-bgk-2019-l06") or value.startswith("br-bgk-2019-w06")
            for value in new_source_heading_ids) != 45 or
        sum(value.startswith("br-bgk-2019-front-01-06") for value in new_source_heading_ids) != 2):
    raise RuntimeError("Units 5--6 or cumulative frontmatter heading partition drifted")

if not new_records or any(row["provenance"].get("model") != MODEL_PROVENANCE for row in new_records):
    raise RuntimeError("Exact model provenance is missing from one or more Units 5--6 records")

qa_event_ids = {row["stable_id"] for row in records if row["entity_class"] == "qa_event"}
required_qa_events = {
    "qa.br-bgk-2019.u05.authority-closure",
    "qa.br-bgk-2019.u05.translation-closure",
    "qa.br-bgk-2019.u05.media-closure",
    "qa.br-bgk-2019.u06.authority-closure",
    "qa.br-bgk-2019.u06.translation-closure",
    "qa.br-bgk-2019.u06.media-closure",
    "qa.br-bgk-2019.u06.reader-closure",
}
if not required_qa_events.issubset(qa_event_ids):
    raise RuntimeError("Units 5--6 authority, translation, media, and reader QA events are not all bound")
reader_qa = json.loads(READER_QA.read_text(encoding="utf-8"))
reader_event = next(row for row in records if row["stable_id"] == "qa.br-bgk-2019.u06.reader-closure")
if (reader_event["payload"].get("html_sha256") != reader_qa["html"]["sha256"] or
        reader_event["payload"].get("pdf_sha256") != reader_qa["pdf"]["sha256"] or
        reader_event["payload"].get("pdf_pages") != reader_qa["pdf"]["pages_pypdf"]):
    raise RuntimeError("BGK Units 1--6 reader QA hash/page binding drifted")

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
    "through_unit": 6,
    "manifest_path": MANIFEST.relative_to(ROOT).as_posix(),
    "manifest_bytes": MANIFEST.stat().st_size,
    "manifest_sha256": second["manifest_sha256"],
    "records_path": RECORDS.relative_to(ROOT).as_posix(),
    "records_bytes": RECORDS.stat().st_size,
    "records_sha256": second["records_sha256"],
    "record_count": len(records),
    "units_01_04_baseline_record_count": len(base_records),
    "units_05_06_added_record_count": len(new_records),
    "class_counts": counts,
    "source_heading_id_count": len(source_heading_ids),
    "cumulative_frontmatter_heading_id_count": 2,
    "unit5_source_heading_id_count": 29,
    "unit6_source_heading_id_count": 45,
    "exercise_count": len(exercise_ids),
    "unit5_exercise_count": 11,
    "unit6_exercise_count": 19,
    "public_solution_count": len(solution_ids),
    "unit5_public_solution_count": 1,
    "unit6_public_solution_count": 0,
    "component_asset_count": len(asset_ids),
    "units_05_06_component_asset_count": 0,
    "unit5_term_count": len(expected_unit5_terms),
    "unit6_term_count": len(expected_unit6_terms),
    "unit5_correction_count": len(expected_unit5_corrections),
    "unit6_correction_count": len(expected_unit6_corrections),
    "deterministic_double_replay": True,
    "all_export_file_hashes_stable": first_file_hashes == second_file_hashes,
    "json_schema_errors": 0,
    "records_set_projection_round_trip": True,
    "units_01_04_records_byte_prefix_identity": True,
    "units_01_04_class_projection_byte_prefix_identity": True,
    "units_01_04_records_prefix_bytes": len(base_bytes),
    "units_01_04_records_prefix_sha256": digest(BASE / "records.jsonl"),
    "units_01_04_class_prefix_sha256": class_prefix_hashes,
    "unique_stable_ids": True,
    "parent_rights_concept_and_relation_endpoint_closure": True,
    "source_heading_namespace": "br-bgk-2019-*",
    "exact_101_exercise_three_public_solution_closure": True,
    "authority_translation_reader_and_zero_media_qa_bound": True,
    "exact_units_05_06_terminology_and_correction_ledger_closure": True,
    "all_units_05_06_records_carry_exact_model_provenance": True,
    "bgk_classical_stable_id_intersection_count": 0,
    "credential_pattern_hits": 0,
    "reader": {
        "qa_path": READER_QA.relative_to(ROOT).as_posix(),
        "qa_sha256": digest(READER_QA),
        "html_sha256": reader_qa["html"]["sha256"],
        "pdf_sha256": reader_qa["pdf"]["sha256"],
        "pdf_pages": reader_qa["pdf"]["pages_pypdf"],
    },
    "model_provenance": MODEL_PROVENANCE,
}
RECEIPT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"status": "PASS", "receipt": RECEIPT.relative_to(ROOT).as_posix(),
                  "record_count": len(records), "records_sha256": second["records_sha256"]},
                 ensure_ascii=False))
