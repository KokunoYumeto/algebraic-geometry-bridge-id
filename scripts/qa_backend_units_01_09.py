#!/usr/bin/env python3
"""Independent fail-closed QA for the cumulative native backend through Unit 9."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend" / "units-01-09"
BASELINE = ROOT / "backend" / "units-01-08"
MANIFEST_PATH = BACKEND / "MANIFEST.json"
RECORDS_PATH = BACKEND / "records.jsonl"
OUTPUT = ROOT / "qa" / "UNITS_01_09_BACKEND_QA.json"
MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."

UNIT8_MANIFEST_SHA256 = "b019122587e5bca0b2224e2cf9ac05a879e6b53e228ee09ca2e04a68c970b337"
UNIT8_RECORDS_SHA256 = "7ac2d40a553741648ef3e5136802247cd3004ea41e3733496aabb0d7c273f973"
UNIT8_SCHEMA_SHA256 = "8c98c4999faabe8356129f6b5de0a8482022ebd04c315b673e2a7cbfbacbb917"
UNIT8_RECORD_COUNT = 5787


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


require(digest(BASELINE / "MANIFEST.json") == UNIT8_MANIFEST_SHA256, "Unit 8 manifest baseline hash changed")
require(digest(BASELINE / "records.jsonl") == UNIT8_RECORDS_SHA256, "Unit 8 records baseline hash changed")
require(digest(BASELINE / "record.schema.json") == UNIT8_SCHEMA_SHA256, "Unit 8 schema baseline hash changed")

manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
require(manifest.get("schema") == "ag-bridge-backend-export-manifest-v2", "Unexpected backend manifest schema")
require(manifest.get("through_unit") == 9, "Backend manifest is not through Unit 9")
require(manifest.get("record_count", 0) >= UNIT8_RECORD_COUNT, "Backend manifest has no Unit 9 extension")

raw_lines = RECORDS_PATH.read_text(encoding="utf-8").splitlines()
records: list[dict[str, Any]] = []
raw_by_id: dict[str, str] = {}
for index, raw in enumerate(raw_lines, start=1):
    record = json.loads(raw)
    require(canonical(record) == raw, f"Noncanonical JSONL record at line {index}: {record.get('stable_id')}")
    stable_id = record["stable_id"]
    require(stable_id not in raw_by_id, f"Duplicate stable ID at line {index}: {stable_id}")
    records.append(record)
    raw_by_id[stable_id] = raw

require(len(records) == manifest["record_count"], "Manifest record count mismatch")
counts = Counter(record["entity_class"] for record in records)
require(dict(sorted(counts.items())) == manifest["counts"], "Manifest entity counts mismatch")
required_classes = {
    "program", "course", "resource", "edition", "unit", "segment", "exercise", "solution",
    "concept", "term", "asset", "relation", "rights", "correction", "qa_event", "artifact",
}
require(required_classes <= set(counts), "Required entity classes are incomplete")

# Every Unit 8 baseline line must survive byte-for-byte in the Unit 9 replay.
baseline_lines = (BASELINE / "records.jsonl").read_text(encoding="utf-8").splitlines()
baseline_raw_by_id = {json.loads(line)["stable_id"]: line for line in baseline_lines}
require(len(baseline_raw_by_id) == UNIT8_RECORD_COUNT, "Unit 8 baseline record count changed")
require(set(baseline_raw_by_id) <= set(raw_by_id), "Cumulative backend dropped a Unit 8 stable ID")
require(all(raw_by_id[key] == value for key, value in baseline_raw_by_id.items()), "Unit 8 baseline payload bytes changed")

id_set = set(raw_by_id)
for record in records:
    parent_id = record.get("parent_id")
    if parent_id is not None:
        require(parent_id in id_set, f"Missing parent {parent_id} for {record['stable_id']}")
    for field in ("resource_id", "edition_id", "rights_id"):
        value = record.get(field)
        if value is not None:
            require(value in id_set, f"Missing {field} endpoint {value} for {record['stable_id']}")
    for concept_id in record.get("concept_ids", []):
        require(concept_id in id_set, f"Missing concept endpoint {concept_id} for {record['stable_id']}")
    if record["entity_class"] == "relation":
        payload = record.get("payload", {})
        for field in ("subject_id", "object_id"):
            require(payload.get(field) in id_set, f"Missing relation endpoint {payload.get(field)}")

for entry in manifest["files"] + manifest["source_bindings"]:
    path = ROOT / entry["path"]
    require(path.is_file(), f"Missing backend binding {entry['path']}")
    require(path.stat().st_size == entry["bytes"], f"Backend byte witness mismatch {entry['path']}")
    require(digest(path) == entry["sha256"], f"Backend hash witness mismatch {entry['path']}")

build = json.loads((ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json").read_text(encoding="utf-8"))
machine = json.loads((ROOT / "qa" / "UNITS_01_09_MACHINE_QA.json").read_text(encoding="utf-8"))
visual = json.loads((ROOT / "qa" / "UNITS_01_09_VISUAL_QA.json").read_text(encoding="utf-8"))
responsive = json.loads((ROOT / "qa" / "UNITS_01_09_RESPONSIVE_QA.json").read_text(encoding="utf-8"))
protected = json.loads((ROOT / "qa" / "UNIT_09_PROTECTED_SURFACES.json").read_text(encoding="utf-8"))
require(build.get("through_unit") == 9, "Reader build is not through Unit 9")
require(machine.get("status") == "PASS", "Machine reader QA did not pass")
require(visual.get("result") == "PASS", "Visual reader QA did not pass")
require(responsive.get("status") == "PASS", "Responsive reader QA did not pass")
require(protected.get("unit") == 9, "Protected Unit 9 surface receipt mismatch")

unit9_map = json.loads((ROOT / "authority" / "wikiversity" / "unit-09" / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
unit9_rights = (ROOT / "authority" / "RIGHTS-unit-09.csv").read_text(encoding="utf-8").splitlines()
require(unit9_map["exercise_count"] == 24 and unit9_map["solution_count"] == 3, "Unit 9 exercise map count mismatch")
require(len(unit9_rights) == 2, "Unit 9 rights CSV row count mismatch")
unit9_exercises = {f"br-ak-2025-2026-w09-ex-{n:02d}" for n in range(1, 25)}
unit9_solutions = {f"br-ak-2025-2026-w09-sol-{n:02d}" for n in (6, 13, 18)}
require(unit9_exercises <= id_set, "Unit 9 exercise stable-ID closure incomplete")
require(unit9_solutions <= id_set, "Unit 9 solution stable-ID closure incomplete")
rights_rows = [r for r in records if r["entity_class"] == "rights" and r["stable_id"].startswith("rights.br-ak-u09-")]
asset_rows = [r for r in records if r["entity_class"] == "asset" and r["stable_id"].startswith("br-ak-u09-")]
require(len(rights_rows) == 1 and len(asset_rows) == 1, "Unit 9 media rights/asset closure mismatch")
require(MODEL_PROVENANCE in (ROOT / "source" / "id-ID" / "frontmatter-units-01-09.md").read_text(encoding="utf-8"), "Model provenance is absent from Unit 9 frontmatter")

course = next(record for record in records if record["stable_id"] == "course.o016-d100.algebraic-geometry-bridge")
require(course["payload"].get("napkin_disposition", "").startswith("optional reference evidence only"), "Stale Napkin requirement survives")
require(any(r["stable_id"] == "relation.units0107.architecture-bgk-required" for r in records), "BGK architecture relation is absent")

receipt = {
    "schema": "ag-bridge-backend-qa-v5",
    "result": "PASS",
    "through_unit": 9,
    "backend": {
        "manifest_path": "backend/units-01-09/MANIFEST.json",
        "manifest_sha256": digest(MANIFEST_PATH),
        "records_path": "backend/units-01-09/records.jsonl",
        "records_sha256": digest(RECORDS_PATH),
        "record_count": len(records),
        "counts": dict(sorted(counts.items())),
        "unit_8_baseline_record_count": len(baseline_raw_by_id),
        "unit_8_baseline_exactly_preserved": True,
    },
    "unit_9": {
        "exercise_count": len(unit9_exercises),
        "public_solution_count": len(unit9_solutions),
        "media_rights_positions": len(rights_rows),
        "media_assets": len(asset_rows),
        "solution_exercise_numbers": [6, 13, 18],
    },
    "reader_evidence": {
        "build_receipt_sha256": digest(ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json"),
        "machine_qa_sha256": digest(ROOT / "qa" / "UNITS_01_09_MACHINE_QA.json"),
        "visual_qa_sha256": digest(ROOT / "qa" / "UNITS_01_09_VISUAL_QA.json"),
        "responsive_qa_sha256": digest(ROOT / "qa" / "UNITS_01_09_RESPONSIVE_QA.json"),
        "protected_surfaces_sha256": digest(ROOT / "qa" / "UNIT_09_PROTECTED_SURFACES.json"),
    },
    "provenance": MODEL_PROVENANCE,
    "validation": {
        "canonical_jsonl": True,
        "unique_stable_ids": True,
        "parent_and_relation_closure": True,
        "unit_8_baseline_exact_preservation": True,
        "authority_and_binding_hashes": True,
        "reader_build_and_visual_qa": True,
    },
}
OUTPUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"result": "PASS", "records": len(records), "manifest_sha256": digest(MANIFEST_PATH), "qa": OUTPUT.as_posix()}, ensure_ascii=False))
