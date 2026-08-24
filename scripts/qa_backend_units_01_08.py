#!/usr/bin/env python3
"""Independent fail-closed QA for the cumulative native backend through Unit 8."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend" / "units-01-08"
BASELINE = ROOT / "backend" / "units-01-07"
MANIFEST_PATH = BACKEND / "MANIFEST.json"
RECORDS_PATH = BACKEND / "records.jsonl"
OUTPUT = ROOT / "qa" / "UNITS_01_08_BACKEND_QA.json"
MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."


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


manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
require(manifest.get("schema") == "ag-bridge-backend-export-manifest-v2", "Unexpected backend manifest schema")
require(manifest.get("through_unit") == 8, "Backend manifest is not through Unit 8")
require(manifest.get("record_count", 0) >= 1, "Backend manifest has no records")

raw_lines = RECORDS_PATH.read_text(encoding="utf-8").splitlines()
records: list[dict[str, Any]] = []
for index, raw in enumerate(raw_lines, start=1):
    record = json.loads(raw)
    require(canonical(record) == raw, f"Noncanonical JSONL record at line {index}: {record.get('stable_id')}")
    records.append(record)

ids = [record["stable_id"] for record in records]
id_set = set(ids)
require(len(ids) == len(id_set), "Duplicate stable ID in cumulative backend")
require(len(records) == manifest["record_count"], "Manifest record count mismatch")
counts = Counter(record["entity_class"] for record in records)
require(dict(sorted(counts.items())) == manifest["counts"], "Manifest entity counts mismatch")
required_classes = {
    "program", "course", "resource", "edition", "unit", "segment", "exercise", "solution",
    "concept", "term", "asset", "relation", "rights", "correction", "qa_event", "artifact",
}
require(required_classes <= set(counts), "Required entity classes are incomplete")

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

# The Unit 7 cumulative backend is the exact frozen input for this replay.
baseline_lines = (BASELINE / "records.jsonl").read_text(encoding="utf-8").splitlines()
baseline_by_id = {json.loads(line)["stable_id"]: json.loads(line) for line in baseline_lines}
cumulative_by_id = {record["stable_id"]: record for record in records}
require(len(baseline_by_id) == 5182, "Unit 7 baseline record count changed")
require(set(baseline_by_id) <= id_set, "Cumulative backend dropped a Unit 7 stable ID")
require(all(cumulative_by_id[key] == value for key, value in baseline_by_id.items()), "Unit 7 baseline payload changed")

authority = manifest["authority_bindings"]
for binding in authority.values():
    path = ROOT / binding["path"]
    require(path.is_file(), f"Missing authority binding {binding['path']}")
    require(path.stat().st_size == binding["bytes"] if "bytes" in binding else True, f"Authority byte witness mismatch {binding['path']}")
    require(digest(path) == binding["sha256"], f"Authority hash witness mismatch {binding['path']}")

for entry in manifest["files"] + manifest["source_bindings"]:
    path = ROOT / entry["path"]
    require(path.is_file(), f"Missing backend binding {entry['path']}")
    require(path.stat().st_size == entry["bytes"], f"Backend byte witness mismatch {entry['path']}")
    require(digest(path) == entry["sha256"], f"Backend hash witness mismatch {entry['path']}")

build = json.loads((ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json").read_text(encoding="utf-8"))
machine = json.loads((ROOT / "qa" / "UNITS_01_08_MACHINE_QA.json").read_text(encoding="utf-8"))
visual = json.loads((ROOT / "qa" / "UNITS_01_08_VISUAL_QA.json").read_text(encoding="utf-8"))
responsive = json.loads((ROOT / "qa" / "UNITS_01_08_RESPONSIVE_QA.json").read_text(encoding="utf-8"))
protected = json.loads((ROOT / "qa" / "UNIT_08_PROTECTED_SURFACES.json").read_text(encoding="utf-8"))
require(build.get("through_unit") == 8, "Reader build is not through Unit 8")
require(machine.get("status") == "PASS", "Machine reader QA did not pass")
require(visual.get("result") == "PASS", "Visual reader QA did not pass")
require(responsive.get("status") == "PASS", "Responsive reader QA did not pass")
require(protected.get("unit") == 8, "Protected Unit 8 surface receipt mismatch")

unit8_map = json.loads((ROOT / "authority" / "wikiversity" / "unit-08" / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))
unit8_rights = (ROOT / "authority" / "RIGHTS-unit-08.csv").read_text(encoding="utf-8").splitlines()
require(unit8_map["exercise_count"] == 24 and unit8_map["solution_count"] == 2, "Unit 8 exercise map count mismatch")
require(len(unit8_rights) == 7, "Unit 8 rights CSV row count mismatch")
unit8_exercises = {f"br-ak-2025-2026-w08-ex-{n:02d}" for n in range(1, 25)}
unit8_solutions = {f"br-ak-2025-2026-w08-sol-{n:02d}" for n in (9, 17)}
require(unit8_exercises <= id_set, "Unit 8 exercise stable-ID closure incomplete")
require(unit8_solutions <= id_set, "Unit 8 solution stable-ID closure incomplete")
require({"correction.agc-corr-0020", "correction.agc-corr-0021", "correction.agc-adapt-0017", "correction.agc-adapt-0018", "correction.agc-adapt-0019", "correction.agc-adapt-0020"} <= id_set, "Unit 8 correction closure incomplete")

rights_rows = [record for record in records if record["entity_class"] == "rights" and record["stable_id"].startswith("rights.br-ak-u08-")]
asset_rows = [record for record in records if record["entity_class"] == "asset" and record["stable_id"].startswith("br-ak-u08-")]
require(len(rights_rows) == 6 and len(asset_rows) == 6, "Unit 8 media rights/asset closure mismatch")
require(MODEL_PROVENANCE in (ROOT / "source" / "id-ID" / "frontmatter-units-01-08.md").read_text(encoding="utf-8"), "Model provenance is absent from Unit 8 frontmatter")

course = cumulative_by_id["course.o016-d100.algebraic-geometry-bridge"]
require(course["payload"].get("napkin_disposition", "").startswith("optional reference evidence only"), "Stale Napkin requirement survives")
require(any(r["stable_id"] == "relation.units0107.architecture-bgk-required" for r in records), "BGK architecture relation is absent")

receipt = {
    "schema": "ag-bridge-backend-qa-v4",
    "result": "PASS",
    "through_unit": 8,
    "backend": {
        "manifest_path": "backend/units-01-08/MANIFEST.json",
        "manifest_sha256": digest(MANIFEST_PATH),
        "records_path": "backend/units-01-08/records.jsonl",
        "records_sha256": digest(RECORDS_PATH),
        "record_count": len(records),
        "counts": dict(sorted(counts.items())),
        "unit_7_baseline_record_count": len(baseline_by_id),
        "unit_7_baseline_exactly_preserved": True,
    },
    "unit_8": {
        "exercise_count": len(unit8_exercises),
        "public_solution_count": len(unit8_solutions),
        "media_rights_positions": len(rights_rows),
        "media_assets": len(asset_rows),
        "correction_ids": sorted({"AGC-CORR-0020", "AGC-CORR-0021", "AGC-ADAPT-0017", "AGC-ADAPT-0018", "AGC-ADAPT-0019", "AGC-ADAPT-0020"}),
    },
    "reader_evidence": {
        "build_receipt_sha256": digest(ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json"),
        "machine_qa_sha256": digest(ROOT / "qa" / "UNITS_01_08_MACHINE_QA.json"),
        "visual_qa_sha256": digest(ROOT / "qa" / "UNITS_01_08_VISUAL_QA.json"),
        "responsive_qa_sha256": digest(ROOT / "qa" / "UNITS_01_08_RESPONSIVE_QA.json"),
        "protected_surfaces_sha256": digest(ROOT / "qa" / "UNIT_08_PROTECTED_SURFACES.json"),
    },
    "provenance": MODEL_PROVENANCE,
    "validation": {
        "canonical_jsonl": True,
        "unique_stable_ids": True,
        "parent_and_relation_closure": True,
        "baseline_exact_preservation": True,
        "authority_and_binding_hashes": True,
        "reader_build_and_visual_qa": True,
    },
}
OUTPUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"result": "PASS", "records": len(records), "manifest_sha256": digest(MANIFEST_PATH), "qa": OUTPUT.as_posix()}, ensure_ascii=False))

