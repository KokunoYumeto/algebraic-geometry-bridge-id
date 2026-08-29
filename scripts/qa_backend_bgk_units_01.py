#!/usr/bin/env python3
"""Fail-closed deterministic replay and closure QA for BGK Unit 1."""

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
EXPORTER = ROOT / "scripts" / "export_backend_bgk_units_01.py"
BACKEND = ROOT / "backend" / "bgk-units-01"
MANIFEST = BACKEND / "MANIFEST.json"
RECORDS = BACKEND / "records.jsonl"
CLASSICAL_RECORDS = ROOT / "backend" / "units-01-30" / "records.jsonl"
RECEIPT = ROOT / "qa" / "BGK_UNITS_01_BACKEND_QA.json"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def run_exporter() -> dict[str, str]:
    process = subprocess.run([sys.executable, str(EXPORTER)], cwd=ROOT, check=True, capture_output=True, text=True)
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
    raise RuntimeError("BGK native backend double replay is not byte deterministic")

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
if manifest.get("through_unit") != 1 or manifest.get("exercise_count") != 17 or manifest.get("public_solution_count") != 0:
    raise RuntimeError("BGK Unit 1 manifest scope drifted")

for binding in manifest["files"] + manifest["source_bindings"]:
    path = ROOT / binding["path"]
    if not path.is_file() or path.stat().st_size != binding["bytes"] or digest(path) != binding["sha256"]:
        raise RuntimeError(f"BGK backend binding replay mismatch: {binding['path']}")

schema = json.loads((BACKEND / "record.schema.json").read_text(encoding="utf-8"))
validator = Draft202012Validator(schema)
records = [json.loads(line) for line in RECORDS.read_text(encoding="utf-8").splitlines() if line.strip()]
schema_errors: list[str] = []
for row in records:
    schema_errors.extend(error.message for error in validator.iter_errors(row))
if schema_errors:
    raise RuntimeError(f"BGK backend JSON Schema errors: {schema_errors[:5]}")

class_records: list[dict] = []
for entity_class in schema["properties"]["entity_class"]["enum"]:
    path = BACKEND / f"{entity_class}.jsonl"
    if not path.is_file():
        raise RuntimeError(f"Missing BGK class projection: {path.name}")
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row["entity_class"] != entity_class:
            raise RuntimeError(f"Wrong entity class in {path.name}: {row['stable_id']}")
        class_records.append(row)

if [canonical(row) for row in records] != [canonical(row) for row in sorted(class_records, key=lambda row: (row["entity_class"], row["stable_id"]))]:
    raise RuntimeError("BGK records.jsonl is not the exact ordered union of class projections")

ids = [row["stable_id"] for row in records]
id_set = set(ids)
if len(ids) != len(id_set):
    raise RuntimeError("Duplicate BGK stable ID")
for row in records:
    if row["parent_id"] is not None and row["parent_id"] not in id_set:
        raise RuntimeError(f"Missing BGK parent: {row['stable_id']}")
    if row["rights_id"] is not None and row["rights_id"] not in id_set:
        raise RuntimeError(f"Missing BGK rights record: {row['stable_id']}")
    if any(concept_id not in id_set for concept_id in row["concept_ids"]):
        raise RuntimeError(f"Missing BGK concept record: {row['stable_id']}")
    if row["entity_class"] == "relation":
        if row["payload"]["subject_id"] not in id_set or row["payload"]["object_id"] not in id_set:
            raise RuntimeError(f"Missing BGK relation endpoint: {row['stable_id']}")

counts = dict(sorted(Counter(row["entity_class"] for row in records).items()))
if counts != manifest["counts"] or len(records) != manifest["record_count"]:
    raise RuntimeError("BGK manifest count replay mismatch")

source_heading_ids = [
    row["stable_id"] for row in records
    if row["source_local_id"] == row["stable_id"] and row["stable_id"].startswith("br-bgk-2019-")
    and row["payload"].get("heading_level") is not None
]
if len(source_heading_ids) != manifest["source_heading_id_count"] or not all(value.startswith("br-bgk-2019-") for value in source_heading_ids):
    raise RuntimeError("BGK source-heading namespace closure failed")

exercise_ids = sorted(row["stable_id"] for row in records if row["entity_class"] == "exercise")
if exercise_ids != [f"br-bgk-2019-w01-ex{number:02d}" for number in range(1, 18)]:
    raise RuntimeError("BGK exercise IDs are not the exact 17-unit closure")
if any(row["entity_class"] == "solution" for row in records):
    raise RuntimeError("BGK backend invented a source solution")

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
    raise RuntimeError("Credential-like material found in BGK backend")

result = {
    "schema": "ag-bridge-bgk-native-backend-qa-receipt-v1",
    "tested_authority_utc": manifest["generated_from_authority_utc"],
    "status": "PASS",
    "through_unit": 1,
    "manifest_path": MANIFEST.relative_to(ROOT).as_posix(),
    "manifest_sha256": second["manifest_sha256"],
    "records_path": RECORDS.relative_to(ROOT).as_posix(),
    "records_bytes": RECORDS.stat().st_size,
    "records_sha256": second["records_sha256"],
    "record_count": len(records),
    "class_counts": counts,
    "source_heading_id_count": len(source_heading_ids),
    "exercise_count": len(exercise_ids),
    "public_solution_count": 0,
    "component_asset_count": counts.get("asset", 0),
    "deterministic_double_replay": True,
    "all_export_file_hashes_stable": first_file_hashes == second_file_hashes,
    "json_schema_errors": 0,
    "class_projection_round_trip": True,
    "unique_stable_ids": True,
    "parent_rights_concept_and_relation_endpoint_closure": True,
    "source_heading_namespace": "br-bgk-2019-*",
    "classical_collision_baseline": {
        "path": CLASSICAL_RECORDS.relative_to(ROOT).as_posix(),
        "sha256": digest(CLASSICAL_RECORDS),
        "classical_stable_id_count": len(classical_ids),
        "intersection_count": len(intersection),
    },
    "zero_public_solution_closure": True,
    "credential_pattern_hits": 0,
    "model_provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
    "exporter": {"path": EXPORTER.relative_to(ROOT).as_posix(), "bytes": EXPORTER.stat().st_size, "sha256": digest(EXPORTER)},
    "qa_script": {"path": Path(__file__).relative_to(ROOT).as_posix(), "bytes": Path(__file__).stat().st_size, "sha256": digest(Path(__file__))},
}
RECEIPT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(result, ensure_ascii=False))
