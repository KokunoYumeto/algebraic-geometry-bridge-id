#!/usr/bin/env python3
"""Fail-closed replay and closure checks for the Unit 1 backend export."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
import subprocess
import sys

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "scripts" / "export_backend_unit1.py"
BACKEND = ROOT / "backend" / "unit-01"
MANIFEST = BACKEND / "MANIFEST.json"
RECEIPT = ROOT / "qa" / "UNIT_01_BACKEND_QA.json"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def replay() -> tuple[str, str]:
    subprocess.run([sys.executable, str(EXPORTER)], cwd=ROOT, check=True, capture_output=True, text=True)
    first = digest(MANIFEST)
    subprocess.run([sys.executable, str(EXPORTER)], cwd=ROOT, check=True, capture_output=True, text=True)
    second = digest(MANIFEST)
    if first != second:
        raise RuntimeError(f"Nondeterministic manifest replay: {first} != {second}")
    return first, second


first_manifest_sha256, second_manifest_sha256 = replay()
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

for row in manifest["files"] + manifest["source_bindings"]:
    path = ROOT / row["path"]
    if path.stat().st_size != row["bytes"] or digest(path) != row["sha256"]:
        raise RuntimeError(f"Manifest replay mismatch: {row['path']}")

schema_path = BACKEND / "record.schema.json"
schema = json.loads(schema_path.read_text(encoding="utf-8"))
validator = Draft202012Validator(schema)
combined_records = [json.loads(line) for line in (BACKEND / "records.jsonl").read_text(encoding="utf-8").splitlines()]
errors = []
for record in combined_records:
    errors.extend(validator.iter_errors(record))
if errors:
    raise RuntimeError(f"JSON Schema errors: {[error.message for error in errors[:5]]}")

class_records = []
for entity_class in schema["properties"]["entity_class"]["enum"]:
    path = BACKEND / f"{entity_class}.jsonl"
    for line in path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        if record["entity_class"] != entity_class:
            raise RuntimeError(f"Wrong class in {path.name}: {record['stable_id']}")
        class_records.append(record)

canonical = lambda value: json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
if [canonical(row) for row in combined_records] != [
    canonical(row) for row in sorted(class_records, key=lambda row: (row["entity_class"], row["stable_id"]))
]:
    raise RuntimeError("Combined JSONL is not the exact ordered union of class projections")

ids = [record["stable_id"] for record in combined_records]
id_set = set(ids)
if len(ids) != len(id_set):
    raise RuntimeError("Duplicate stable ID")
for record in combined_records:
    if record["parent_id"] and record["parent_id"] not in id_set:
        raise RuntimeError(f"Missing parent for {record['stable_id']}")
    if record["entity_class"] == "relation":
        for endpoint in (record["payload"]["subject_id"], record["payload"]["object_id"]):
            if endpoint not in id_set:
                raise RuntimeError(f"Missing relation endpoint {endpoint}")

counts = Counter(record["entity_class"] for record in combined_records)
if dict(sorted(counts.items())) != manifest["counts"]:
    raise RuntimeError("Manifest class counts do not replay")
if len(combined_records) != manifest["record_count"]:
    raise RuntimeError("Manifest record count does not replay")

result = {
    "schema": "ag-bridge-backend-qa-receipt-v1",
    "tested_build_utc": manifest["generated_from_build_utc"],
    "status": "PASS",
    "manifest_path": MANIFEST.relative_to(ROOT).as_posix(),
    "manifest_sha256": second_manifest_sha256,
    "deterministic_double_replay": first_manifest_sha256 == second_manifest_sha256,
    "record_count": len(combined_records),
    "class_counts": dict(sorted(counts.items())),
    "json_schema_errors": 0,
    "unique_stable_ids": True,
    "parent_closure": True,
    "relation_endpoint_closure": True,
    "class_projection_round_trip": True,
    "source_and_export_hash_replay": True,
    "exporter": {
        "path": EXPORTER.relative_to(ROOT).as_posix(),
        "sha256": digest(EXPORTER),
    },
    "qa_script": {
        "path": Path(__file__).relative_to(ROOT).as_posix(),
        "sha256": digest(Path(__file__)),
    },
}
RECEIPT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False))
