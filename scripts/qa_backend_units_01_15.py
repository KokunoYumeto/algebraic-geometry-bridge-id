#!/usr/bin/env python3
"""Independent fail-closed QA for the cumulative native backend through Unit 15."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend" / "units-01-15"
BASELINE = ROOT / "backend" / "units-01-12"
MANIFEST_PATH = BACKEND / "MANIFEST.json"
RECORDS_PATH = BACKEND / "records.jsonl"
SCHEMA_PATH = BACKEND / "record.schema.json"
OUTPUT = ROOT / "qa" / "UNITS_01_15_BACKEND_QA.json"

BUILD_RECEIPT_PATH = ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json"
MACHINE_QA_PATH = ROOT / "qa" / "UNITS_01_15_MACHINE_QA.json"
VISUAL_QA_PATH = ROOT / "qa" / "UNITS_01_15_VISUAL_QA.json"
RESPONSIVE_QA_PATH = ROOT / "qa" / "UNITS_01_15_RESPONSIVE_QA.json"
PROTECTED_QA_PATH = ROOT / "qa" / "UNIT_15_PROTECTED_SURFACES.json"
CORRECTIONS_PATH = ROOT / "00_control" / "CORRECTIONS.csv"
TERMINOLOGY_PATH = ROOT / "00_control" / "TERMINOLOGY.csv"

BASELINE_MANIFEST_SHA256 = "9c22a4eb308fd5d50cca9151f3617b833fe800749de8087038386af952a683ce"
BASELINE_RECORDS_SHA256 = "914d659bde3a32bce7f10b39f3f0ec12f852cffdfb6f83c12ca150d0ba1d3925"
BASELINE_SCHEMA_SHA256 = "4dbb0acff7e301420250f30cbe9457fd2df4469d820c82d3a30c7f09b7c2bc41"
BASELINE_RECORD_COUNT = 8491

CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-15.2026-08-24"
PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-12.2026-08-24"
MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."

SOURCE_FILES = [
    ROOT / "source" / "id-ID" / "frontmatter-units-01-15.md",
    ROOT / "source" / "id-ID" / "lecture-13.md",
    ROOT / "source" / "id-ID" / "worksheet-13.md",
    ROOT / "source" / "id-ID" / "worksheet-13-solutions.md",
    ROOT / "source" / "id-ID" / "media-credits-unit-13.md",
    ROOT / "source" / "id-ID" / "lecture-14.md",
    ROOT / "source" / "id-ID" / "worksheet-14.md",
    ROOT / "source" / "id-ID" / "worksheet-14-solutions.md",
    ROOT / "source" / "id-ID" / "media-credits-unit-14.md",
    ROOT / "source" / "id-ID" / "lecture-15.md",
    ROOT / "source" / "id-ID" / "worksheet-15.md",
    ROOT / "source" / "id-ID" / "worksheet-15-solutions.md",
    ROOT / "source" / "id-ID" / "media-credits-unit-15.md",
]

EXPECTED_SOURCE_SHA256 = {
    "source/id-ID/frontmatter-units-01-15.md": "d0a7f7d3d8c76789212caef445f39b15b61caed88a1662ca825ba4956b628cb5",
    "source/id-ID/lecture-13.md": "6b2c8a6aac3c80a3bf45cdb83db085e59f72f09bb7829528f2719c6b7af178fa",
    "source/id-ID/worksheet-13.md": "b9dbf3ee514c8e7d59bdf60ba4617cb0b8a38b5e299cc65af53cdd8e7f56adcd",
    "source/id-ID/worksheet-13-solutions.md": "787b24f616ac7823c88b7f45ea827df5bbdea34be111bb36822d542121e89774",
    "source/id-ID/media-credits-unit-13.md": "f5aa7d11bb7fd29860bdaec51fdb03790fdd6361e6f0ef2b4fbac72040de1341",
    "source/id-ID/lecture-14.md": "64b2519967638116cb3f98a2a200ad23efb5212e5c5c24b7f53e93ad2211f2d4",
    "source/id-ID/worksheet-14.md": "45dc11df386efc92ff537be1c53d7e2d9f16938be2fe5cd8eeb14eac347059cc",
    "source/id-ID/worksheet-14-solutions.md": "d64c25e2062d8a437465e7bb64d192e6d3ae347cdd6780c02e5146331cbe44dd",
    "source/id-ID/media-credits-unit-14.md": "b7960d839016c9f6705c1fdba68685a889c1af3261d2339190931e5f9f8b3dc3",
    "source/id-ID/lecture-15.md": "e1affd57e9f9d33f7e85a2b8c8fe993ecd821d1fff1075588f51dca2014763b4",
    "source/id-ID/worksheet-15.md": "feb6d9c38b669718c548608865f416eb1b3a03ac2d1ce6fac92cb5a288f48784",
    "source/id-ID/worksheet-15-solutions.md": "49fecc0631064c646bd8fe2707f2ab84f8e33f32e9c4f99028b4dc9f508ec948",
    "source/id-ID/media-credits-unit-15.md": "ccb29926735e5cdf47f628e2a66cf8c8e9017d64f3357a116e7e5abec3c41734",
}

TERMINOLOGY_CONCEPTS = {
    "AGT-0076": "concept.multiplicative-system",
    "AGT-0077": "concept.idempotent-element",
    "AGT-0078": "concept.product-ring",
    "AGT-0079": "concept.connected-ring",
    "AGT-0080": "concept.clopen-set",
    "AGT-0081": "concept.saturated-multiplicative-system",
    "AGT-0082": "concept.non-zero-divisor",
    "AGT-0083": "concept.algebraic-function",
    "AGT-0084": "concept.regular-function",
    "AGT-0085": "concept.structure-ring",
    "AGT-0086": "concept.section-ring",
    "AGT-0087": "concept.structure-sheaf",
    "AGT-0088": "concept.presheaf",
    "AGT-0089": "concept.sheaf",
    "AGT-0090": "concept.restriction-map",
    "AGT-0091": "concept.minimal-prime-ideal",
    "AGT-0092": "concept.ultrafilter",
    "AGT-0093": "concept.holomorphic",
    "AGT-0094": "concept.affine-variety",
    "AGT-0095": "concept.quasi-affine-variety",
    "AGT-0096": "concept.local-ring",
    "AGT-0097": "concept.localization-at-prime-ideal",
    "AGT-0098": "concept.topological-filter",
    "AGT-0099": "concept.neighborhood-filter",
    "AGT-0100": "concept.directed-set",
    "AGT-0101": "concept.directed-system",
    "AGT-0102": "concept.colimit",
    "AGT-0103": "concept.stalk",
    "AGT-0104": "concept.function-field",
    "AGT-0105": "concept.colimit",
}

CORRECTION_TARGETS = {
    "AGC-CORR-0028": "br-ak-2025-2026-w13-ex-29",
    "AGC-CORR-0029": "br-ak-2025-2026-w13-sol-11",
    "AGC-CORR-0030": "br-ak-2025-2026-w13-sol-20",
    "AGC-CORR-0031": "br-ak-2025-2026-w14-sol-07",
    "AGC-CORR-0032": "br-ak-2025-2026-l15-def-08",
    "AGC-CORR-0033": "br-ak-2025-2026-w15-sol-19",
}

UNIT_SPEC: dict[int, dict[str, Any]] = {
    13: {
        "manifest": ROOT / "authority" / "wikiversity" / "unit-13" / "UNIT_AUTHORITY_MANIFEST.json",
        "map": ROOT / "authority" / "wikiversity" / "unit-13" / "ORDERED_EXERCISE_MAP.json",
        "rights": ROOT / "authority" / "RIGHTS-unit-13.csv",
        "closure": ROOT / "authority" / "ASSET_CLOSURE-unit-13.json",
        "exercise_count": 37,
        "solutions": (3, 6, 8, 9, 11, 14, 15, 17, 20, 21, 24, 27, 28, 31),
        "media_count": 2,
        "binary_surfaces": 4,
        "expected": {
            "manifest": "dc86b4d124c7e775fb635a1f9672a8b8faadc4ff2259b0779f7bac6302d18848",
            "map": "f954f09c996c8aa22f94ec826a1503b135a7b4fb9f9e0d5d6ff21f36a519e52a",
            "rights": "cdf370a6e3d7b80e137e6eb98a1180519b0cb97865ee39197de07c37e1a3c825",
            "closure": "771a8f09fd262838873e1390c43cae7da1f3989b74d8d2a7f67a856da9ea5e23",
        },
    },
    14: {
        "manifest": ROOT / "authority" / "wikiversity" / "unit-14" / "UNIT_AUTHORITY_MANIFEST.json",
        "map": ROOT / "authority" / "wikiversity" / "unit-14" / "ORDERED_EXERCISE_MAP.json",
        "rights": ROOT / "authority" / "RIGHTS-unit-14.csv",
        "closure": ROOT / "authority" / "ASSET_CLOSURE-unit-14.json",
        "exercise_count": 27,
        "solutions": (2, 7),
        "media_count": 1,
        "binary_surfaces": 1,
        "expected": {
            "manifest": "a63c3481d0a9cfa9b960f12c9bf0eec9a5d39cecfb61eddb8f9d96190e52e83e",
            "map": "0d223f7f3c56c4714736dfc6eb3dbd40dc8cd3cb30a05f66281a6f2b1b875dbe",
            "rights": "9c377f7c679ff0730bcd075201a4d587a322f004b118b0e31fc9c51b267e8973",
            "closure": "8fd50fae2515e6150e3d81c98573dd7bb204211e787d68405f7c3b03aab452d0",
        },
    },
    15: {
        "manifest": ROOT / "authority" / "wikiversity" / "unit-15" / "UNIT_AUTHORITY_MANIFEST.json",
        "map": ROOT / "authority" / "wikiversity" / "unit-15" / "ORDERED_EXERCISE_MAP.json",
        "rights": ROOT / "authority" / "RIGHTS-unit-15.csv",
        "closure": ROOT / "authority" / "ASSET_CLOSURE-unit-15.json",
        "exercise_count": 29,
        "solutions": (6, 9, 19, 22),
        "media_count": 1,
        "binary_surfaces": 2,
        "expected": {
            "manifest": "86e394725e766838f01eb035ca53044c4d3b85ff20eb99f8fecda9c2a0156425",
            "map": "3c8c41458f5418ff858a58748ba4b23bc0a8cb34d9c386c155806b4482760470",
            "rights": "28ed5e373e07f80cef981315733e53069bdcf8f14c4447d1d21c3fabb2b5f4d7",
            "closure": "cdf6371ba9e44f9828f166f8da5ecfe4b6141e0b9ba0c7c02a5dfba156fea0a4",
        },
    },
}

REQUIRED_CLASSES = {
    "artifact", "asset", "concept", "correction", "course", "edition",
    "exercise", "program", "qa_event", "relation", "resource", "rights",
    "segment", "solution", "term", "unit",
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


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


for path, expected in (
    (BASELINE / "MANIFEST.json", BASELINE_MANIFEST_SHA256),
    (BASELINE / "records.jsonl", BASELINE_RECORDS_SHA256),
    (BASELINE / "record.schema.json", BASELINE_SCHEMA_SHA256),
):
    require(path.is_file(), f"Missing Units 1--12 baseline file: {rel(path)}")
    require(digest(path) == expected, f"Units 1--12 baseline hash changed: {rel(path)}")

manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
require(manifest.get("schema") == "ag-bridge-backend-export-manifest-v2", "Unexpected backend manifest schema")
require(manifest.get("through_unit") == 15, "Backend manifest is not through Unit 15")
require(manifest.get("scope") == "cumulative Units 1--15", "Backend manifest scope mismatch")
require(manifest.get("model_provenance") == MODEL_PROVENANCE, "Backend manifest model provenance mismatch")
require(manifest.get("record_count", 0) > BASELINE_RECORD_COUNT, "Backend has no Units 13--15 extension")
require(schema.get("title", "").endswith("Units 1--15"), "Backend record schema title is stale")

raw_lines = RECORDS_PATH.read_text(encoding="utf-8").splitlines()
records: list[dict[str, Any]] = []
raw_by_id: dict[str, str] = {}
schema_keys = set(schema["properties"])
required_keys = set(schema["required"])
for index, raw in enumerate(raw_lines, start=1):
    record = json.loads(raw)
    stable_id = record.get("stable_id")
    require(canonical(record) == raw, f"Noncanonical JSONL record at line {index}: {stable_id}")
    require(stable_id not in raw_by_id, f"Duplicate stable ID at line {index}: {stable_id}")
    require(required_keys <= set(record), f"Schema-required field missing from {stable_id}")
    require(set(record) <= schema_keys, f"Schema-forbidden field present in {stable_id}")
    require(record.get("entity_class") in REQUIRED_CLASSES, f"Unknown entity class in {stable_id}")
    content_sha = record.get("content_sha256")
    require(content_sha is None or re.fullmatch(r"[0-9a-f]{64}", content_sha) is not None, f"Invalid content hash in {stable_id}")
    records.append(record)
    raw_by_id[stable_id] = raw

require(len(records) == manifest["record_count"], "Manifest record count mismatch")
counts = Counter(record["entity_class"] for record in records)
require(dict(sorted(counts.items())) == manifest["counts"], "Manifest entity counts mismatch")
require(set(counts) == REQUIRED_CLASSES, "Required entity-class closure mismatch")

# Every baseline line must survive exactly, not merely as an equivalent parsed
# object. This proves stable-ID and payload-byte identity for all 8,491 rows.
baseline_lines = (BASELINE / "records.jsonl").read_text(encoding="utf-8").splitlines()
baseline_raw_by_id = {json.loads(line)["stable_id"]: line for line in baseline_lines}
require(len(baseline_raw_by_id) == BASELINE_RECORD_COUNT, "Units 1--12 baseline count changed")
require(set(baseline_raw_by_id) <= set(raw_by_id), "Backend dropped a Units 1--12 stable ID")
require(all(raw_by_id[key] == raw for key, raw in baseline_raw_by_id.items()), "A Units 1--12 record payload byte changed")

id_set = set(raw_by_id)
for record in records:
    if record.get("parent_id") is not None:
        require(record["parent_id"] in id_set, f"Missing parent {record['parent_id']} for {record['stable_id']}")
    for field in ("resource_id", "edition_id", "rights_id"):
        value = record.get(field)
        if value is not None:
            require(value in id_set, f"Missing {field} endpoint {value} for {record['stable_id']}")
    for concept_id in record.get("concept_ids", []):
        require(concept_id in id_set, f"Missing concept endpoint {concept_id} for {record['stable_id']}")
    if record["entity_class"] == "relation":
        payload = record["payload"]
        require(payload.get("subject_id") in id_set, f"Missing relation subject for {record['stable_id']}")
        require(payload.get("object_id") in id_set, f"Missing relation object for {record['stable_id']}")

for entry in manifest["files"] + manifest["source_bindings"]:
    path = ROOT / entry["path"]
    require(path.is_file(), f"Missing backend binding: {entry['path']}")
    require(path.stat().st_size == entry["bytes"], f"Backend binding byte mismatch: {entry['path']}")
    require(digest(path) == entry["sha256"], f"Backend binding hash mismatch: {entry['path']}")

build = json.loads(BUILD_RECEIPT_PATH.read_text(encoding="utf-8"))
machine = json.loads(MACHINE_QA_PATH.read_text(encoding="utf-8"))
visual = json.loads(VISUAL_QA_PATH.read_text(encoding="utf-8"))
responsive = json.loads(RESPONSIVE_QA_PATH.read_text(encoding="utf-8"))
protected = json.loads(PROTECTED_QA_PATH.read_text(encoding="utf-8"))
require(build.get("schema") == "ag-bridge-build-receipt-v2" and build.get("through_unit") == 15, "Reader build receipt mismatch")
require(machine.get("status") == "PASS" and machine.get("through_unit") == 15, "Machine reader QA mismatch")
require(visual.get("result") == "PASS" and visual.get("through_unit") == 15, "Visual reader QA mismatch")
require(responsive.get("status") == "PASS" and responsive.get("through_unit") == 15, "Responsive reader QA mismatch")
require(protected.get("status") == "PASS" and protected.get("unit") == 15, "Protected Unit 15 release-boundary receipt mismatch")

input_witnesses = {row["path"]: row for row in build.get("inputs", [])}
require(set(EXPECTED_SOURCE_SHA256) == {rel(path) for path in SOURCE_FILES}, "Final source-hash closure is incomplete")
for path in SOURCE_FILES:
    key = rel(path)
    require(path.is_file(), f"Missing source file: {key}")
    actual = digest(path)
    require(actual == EXPECTED_SOURCE_SHA256[key], f"Frozen source hash changed: {key}")
    witness = input_witnesses.get(key)
    require(witness is not None, f"Reader receipt does not bind source: {key}")
    require(witness.get("bytes") == path.stat().st_size and witness.get("sha256") == actual, f"Reader source witness mismatch: {key}")

output_witnesses = {row["path"]: row for row in build.get("outputs", [])}
for path in (
    ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-15.pdf",
    ROOT / "build" / "reader-id" / "index.html",
):
    key = rel(path)
    require(path.is_file(), f"Missing reader artifact: {key}")
    witness = output_witnesses.get(key)
    require(witness is not None, f"Reader receipt does not bind artifact: {key}")
    require(witness.get("bytes") == path.stat().st_size and witness.get("sha256") == digest(path), f"Reader output witness mismatch: {key}")

heading_re = re.compile(r"^(#{1,6})\s+(.*?)\s+\{#([^}]+)\}\s*$", re.MULTILINE)
source_heading_ids: set[str] = set()
for path in SOURCE_FILES:
    found = {match.group(3) for match in heading_re.finditer(path.read_text(encoding="utf-8"))}
    require(found, f"Source has no stable heading IDs: {rel(path)}")
    require(not source_heading_ids.intersection(found), f"Duplicate stable heading IDs introduced by {rel(path)}")
    source_heading_ids.update(found)
require(source_heading_ids <= id_set, "Backend dropped a Unit 13--15 source heading")

with TERMINOLOGY_PATH.open("r", encoding="utf-8", newline="") as stream:
    terminology_rows = {
        row["term_id"]: row
        for row in csv.DictReader(stream)
        if row.get("term_id") in TERMINOLOGY_CONCEPTS
    }
require(set(terminology_rows) == set(TERMINOLOGY_CONCEPTS), "Units 13--15 terminology ledger closure mismatch")
expected_term_ids: set[str] = set()
expected_concept_ids: set[str] = set()
expected_new_concept_ids: set[str] = set()
first_term_for_new_concept: dict[str, str] = {}
for term_id, concept_id in TERMINOLOGY_CONCEPTS.items():
    term_stable_id = f"term.{term_id.casefold()}.id-id"
    expected_term_ids.add(term_stable_id)
    expected_concept_ids.add(concept_id)
    require(term_stable_id in id_set and concept_id in id_set, f"Missing terminology backend pair for {term_id}")
    term = next(record for record in records if record["stable_id"] == term_stable_id)
    concept = next(record for record in records if record["stable_id"] == concept_id)
    row = terminology_rows[term_id]
    row_sha256 = text_digest(canonical(row))
    require(term["entity_class"] == "term" and concept["entity_class"] == "concept", f"Wrong terminology entity class for {term_id}")
    require(term["source_local_id"] == term_id and term["parent_id"] == concept_id, f"Terminology identity mismatch for {term_id}")
    require(term.get("concept_ids") == [concept_id], f"Terminology concept projection mismatch for {term_id}")
    require(term["payload"].get("preferred_target") == row["preferred_target"], f"Terminology target mismatch for {term_id}")
    require(term.get("content_sha256") == row_sha256, f"Terminology ledger hash mismatch for {term_id}")
    if concept_id not in baseline_raw_by_id:
        expected_new_concept_ids.add(concept_id)
        first_term_for_new_concept.setdefault(concept_id, term_id)

for concept_id, term_id in first_term_for_new_concept.items():
    concept = next(record for record in records if record["stable_id"] == concept_id)
    expected_hash = text_digest(canonical(terminology_rows[term_id]))
    require(concept.get("content_sha256") == expected_hash, f"New concept ledger hash mismatch for {concept_id}")

with CORRECTIONS_PATH.open("r", encoding="utf-8", newline="") as stream:
    correction_rows = {
        row["correction_id"]: row
        for row in csv.DictReader(stream)
        if row.get("correction_id") in CORRECTION_TARGETS
    }
require(set(correction_rows) == set(CORRECTION_TARGETS), "Units 13--15 correction ledger closure mismatch")
expected_correction_ids: set[str] = set()
for correction_id, affected_id in CORRECTION_TARGETS.items():
    stable_id = f"correction.{correction_id.casefold()}"
    expected_correction_ids.add(stable_id)
    require(stable_id in id_set, f"Missing correction backend record for {correction_id}")
    correction = next(record for record in records if record["stable_id"] == stable_id)
    row = correction_rows[correction_id]
    require(correction["entity_class"] == "correction", f"Wrong correction entity class for {correction_id}")
    require(correction["source_local_id"] == correction_id, f"Correction identity mismatch for {correction_id}")
    require(correction["payload"].get("affected_unit_ids") == [affected_id], f"Correction target mismatch for {correction_id}")
    require(affected_id in source_heading_ids, f"Correction target is not a translated source heading: {correction_id}")
    require(correction.get("content_sha256") == text_digest(canonical(row)), f"Correction ledger hash mismatch for {correction_id}")

unit_findings: dict[str, Any] = {}
expected_assets: set[str] = set()
expected_rights: set[str] = set()
expected_exercise_ids: set[str] = set()
expected_solution_ids: set[str] = set()
for unit, spec in UNIT_SPEC.items():
    for key in ("manifest", "map", "rights", "closure"):
        path = spec[key]
        require(path.is_file(), f"Missing Unit {unit} authority file: {rel(path)}")
        require(digest(path) == spec["expected"][key], f"Unit {unit} {key} frozen hash changed")
    exercise_map = json.loads(spec["map"].read_text(encoding="utf-8"))
    closure = json.loads(spec["closure"].read_text(encoding="utf-8"))
    with spec["rights"].open("r", encoding="utf-8", newline="") as stream:
        rights_rows = list(csv.DictReader(stream))
    public = tuple(sorted(int(row["exercise_number"]) for row in exercise_map["entries"] if row.get("has_public_solution")))
    require(exercise_map.get("exercise_count") == spec["exercise_count"], f"Unit {unit} exercise count changed")
    require(public == spec["solutions"], f"Unit {unit} public-solution map changed")
    require(len(rights_rows) == spec["media_count"], f"Unit {unit} rights-row count changed")
    require(closure.get("reader_media_positions") == spec["media_count"], f"Unit {unit} asset-closure count changed")
    require(closure.get("unique_local_assets") == spec["binary_surfaces"], f"Unit {unit} binary-surface closure changed")
    for row in rights_rows:
        local_path = ROOT / row["local_path"]
        require(local_path.is_file(), f"Missing Unit {unit} asset: {row['local_path']}")
        require(local_path.stat().st_size == int(row["local_bytes"]) and digest(local_path) == row["local_sha256"], f"Unit {unit} asset identity changed: {row['asset_id']}")
        if row["pdf_local_path"]:
            companion = ROOT / row["pdf_local_path"]
            require(companion.is_file(), f"Missing Unit {unit} PDF companion: {row['pdf_local_path']}")
            require(companion.stat().st_size == int(row["pdf_local_bytes"]) and digest(companion) == row["pdf_local_sha256"], f"Unit {unit} PDF companion identity changed: {row['asset_id']}")
    expected_exercise_ids.update(f"exercise.br-ak-2025-2026-w{unit:02d}-ex-{number:02d}" for number in range(1, spec["exercise_count"] + 1))
    expected_solution_ids.update(f"solution.br-ak-2025-2026-w{unit:02d}-sol-{number:02d}" for number in spec["solutions"])
    expected_assets.update(row["asset_id"] for row in rights_rows)
    expected_rights.update(f"rights.{row['asset_id']}" for row in rights_rows)
    unit_findings[str(unit)] = {
        "exercise_count": spec["exercise_count"],
        "public_solution_count": len(spec["solutions"]),
        "solution_exercise_numbers": list(spec["solutions"]),
        "media_positions": spec["media_count"],
        "binary_surfaces": spec["binary_surfaces"],
        "manifest_sha256": digest(spec["manifest"]),
        "exercise_map_sha256": digest(spec["map"]),
        "rights_sha256": digest(spec["rights"]),
        "asset_closure_sha256": digest(spec["closure"]),
    }

require(expected_exercise_ids <= id_set, "Typed exercise closure for Units 13--15 is incomplete")
require(expected_solution_ids <= id_set, "Typed solution closure for Units 13--15 is incomplete")
require(expected_assets <= id_set, "Unit 13--15 asset closure is incomplete")
require(expected_rights <= id_set, "Unit 13--15 rights closure is incomplete")
require(not ({record["stable_id"] for record in records if record["entity_class"] == "asset" and record.get("edition_id") == CUMULATIVE_EDITION} - expected_assets), "Unexpected Unit 13--15 asset record")
for unit, spec in UNIT_SPEC.items():
    with spec["rights"].open("r", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            asset = next(record for record in records if record["stable_id"] == row["asset_id"])
            expected_companion = (
                {"path": row["pdf_local_path"], "bytes": int(row["pdf_local_bytes"]), "sha256": row["pdf_local_sha256"]}
                if row["pdf_local_path"] else None
            )
            require(asset.get("path") == row["local_path"] and asset.get("content_sha256") == row["local_sha256"], f"Unit {unit} asset record identity mismatch: {row['asset_id']}")
            require(asset.get("payload", {}).get("pdf_companion") == expected_companion, f"Unit {unit} asset companion record mismatch: {row['asset_id']}")

edition = next((record for record in records if record["stable_id"] == CUMULATIVE_EDITION), None)
require(edition is not None, "Cumulative Unit 15 edition record is absent")
require(edition.get("supersedes") == PREVIOUS_EDITION, "Cumulative edition lineage mismatch")
require(edition["payload"].get("through_unit") == 15, "Cumulative edition payload boundary mismatch")
require(edition["payload"].get("model_provenance") == MODEL_PROVENANCE, "Edition model provenance mismatch")

new_records = [record for record in records if record["stable_id"] not in baseline_raw_by_id]
require(new_records, "No new records were exported")
require(all(record.get("provenance", {}).get("model_provenance") == MODEL_PROVENANCE for record in new_records), "A new record lacks exact model provenance")
required_qa_ids = {"qa.units0115.machine", "qa.units0115.visual", "qa.units0115.responsive", "qa.unit15.protected"}
require(required_qa_ids <= id_set, "Reader QA-event closure is incomplete")

relations = [record for record in records if record["entity_class"] == "relation" and record["stable_id"].startswith("relation.units0115.")]
relation_counts = Counter(record["payload"].get("relation_type") for record in relations)
require(relation_counts["solves"] == 2 * len(expected_solution_ids), "Untyped/typed solution relations are incomplete")
require(relation_counts["illustrates"] == len(expected_assets), "Asset illustration relations are incomplete")
require(relation_counts["validated_by"] == 4, "Reader QA relations are incomplete")
require(relation_counts["extends"] == 1 and relation_counts["derived_from"] == 1, "Edition lineage/source relations are incomplete")
require(relation_counts["labels"] == len(TERMINOLOGY_CONCEPTS), "Terminology label relations are incomplete")
require(relation_counts.get("adapts", 0) == 0 and relation_counts["corrects"] == 6, "Correction relations are incomplete")
actual_label_pairs = {
    (record["payload"]["subject_id"], record["payload"]["object_id"])
    for record in relations
    if record["payload"].get("relation_type") == "labels"
}
expected_label_pairs = {
    (f"term.{term_id.casefold()}.id-id", concept_id)
    for term_id, concept_id in TERMINOLOGY_CONCEPTS.items()
}
require(actual_label_pairs == expected_label_pairs, "Terminology label relation endpoints mismatch")
actual_correction_pairs = {
    (record["payload"].get("relation_type"), record["payload"]["subject_id"], record["payload"]["object_id"])
    for record in relations
    if record["payload"].get("relation_type") in {"adapts", "corrects"}
}
expected_correction_pairs = {
    (
        "corrects" if correction_id.startswith("AGC-CORR-") else "adapts",
        f"correction.{correction_id.casefold()}",
        affected_id,
    )
    for correction_id, affected_id in CORRECTION_TARGETS.items()
}
require(actual_correction_pairs == expected_correction_pairs, "Correction/adaptation relation endpoints mismatch")

baseline_block = manifest.get("units_01_12_baseline", {})
require(baseline_block.get("record_count") == BASELINE_RECORD_COUNT, "Manifest baseline count mismatch")
require(baseline_block.get("record_bytes_preserved") is True, "Manifest does not assert byte preservation")
require(baseline_block.get("stable_ids_and_payloads_preserved") is True, "Manifest does not assert payload preservation")

receipt = {
    "schema": "ag-bridge-backend-qa-v6",
    "result": "PASS",
    "through_unit": 15,
    "backend": {
        "manifest_path": rel(MANIFEST_PATH),
        "manifest_sha256": digest(MANIFEST_PATH),
        "records_path": rel(RECORDS_PATH),
        "records_sha256": digest(RECORDS_PATH),
        "schema_path": rel(SCHEMA_PATH),
        "schema_sha256": digest(SCHEMA_PATH),
        "record_count": len(records),
        "new_record_count": len(new_records),
        "counts": dict(sorted(counts.items())),
        "units_01_12_baseline_record_count": BASELINE_RECORD_COUNT,
        "units_01_12_baseline_records_exactly_preserved": True,
    },
    "units_13_15": unit_findings,
    "reader_evidence": {
        "build_receipt_sha256": digest(BUILD_RECEIPT_PATH),
        "machine_qa_sha256": digest(MACHINE_QA_PATH),
        "visual_qa_sha256": digest(VISUAL_QA_PATH),
        "responsive_qa_sha256": digest(RESPONSIVE_QA_PATH),
        "protected_surfaces_sha256": digest(PROTECTED_QA_PATH),
    },
    "ledger_evidence": {
        "terminology_path": rel(TERMINOLOGY_PATH),
        "terminology_sha256": digest(TERMINOLOGY_PATH),
        "new_term_count": len(expected_term_ids),
        "new_concept_count": len(expected_new_concept_ids),
        "corrections_path": rel(CORRECTIONS_PATH),
        "corrections_sha256": digest(CORRECTIONS_PATH),
        "new_correction_count": len(expected_correction_ids),
    },
    "model_provenance": MODEL_PROVENANCE,
    "validation": {
        "canonical_jsonl_and_schema_surface": True,
        "unique_stable_ids": True,
        "parent_resource_edition_rights_concept_and_relation_closure": True,
        "units_01_12_record_and_payload_byte_identity": True,
        "source_hashes_match_frozen_values_and_reader_inputs": True,
        "authority_manifest_map_rights_asset_solution_closure": True,
        "units_13_15_terminology_and_correction_ledger_closure": True,
        "reader_build_machine_visual_responsive_and_protected_qa": True,
        "exact_model_provenance_on_every_new_record": True,
    },
}
OUTPUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "result": "PASS",
    "records": len(records),
    "new_records": len(new_records),
    "manifest_sha256": digest(MANIFEST_PATH),
    "records_sha256": digest(RECORDS_PATH),
    "qa": rel(OUTPUT),
}, ensure_ascii=False))
