#!/usr/bin/env python3
"""Independent fail-closed QA for the cumulative native backend through Unit 12."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend" / "units-01-12"
BASELINE = ROOT / "backend" / "units-01-09"
MANIFEST_PATH = BACKEND / "MANIFEST.json"
RECORDS_PATH = BACKEND / "records.jsonl"
SCHEMA_PATH = BACKEND / "record.schema.json"
OUTPUT = ROOT / "qa" / "UNITS_01_12_BACKEND_QA.json"

BUILD_RECEIPT_PATH = ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json"
MACHINE_QA_PATH = ROOT / "qa" / "UNITS_01_12_MACHINE_QA.json"
VISUAL_QA_PATH = ROOT / "qa" / "UNITS_01_12_VISUAL_QA.json"
RESPONSIVE_QA_PATH = ROOT / "qa" / "UNITS_01_12_RESPONSIVE_QA.json"
PROTECTED_QA_PATH = ROOT / "qa" / "UNIT_12_PROTECTED_SURFACES.json"
CORRECTIONS_PATH = ROOT / "00_control" / "CORRECTIONS.csv"
TERMINOLOGY_PATH = ROOT / "00_control" / "TERMINOLOGY.csv"

BASELINE_MANIFEST_SHA256 = "54b87a82373b5ba0660fe204141a50602875942e5a9f1a9dc98c760f5b382eac"
BASELINE_RECORDS_SHA256 = "40f7cf1747ea8e62829594e5d01af7db827820d39a3377b5c4e105d82411bbd6"
BASELINE_SCHEMA_SHA256 = "160cd547c0590d8d90633564051b7cd05822ae482b837b55f1c119f6de4264af"
BASELINE_RECORD_COUNT = 6393

CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-12.2026-08-24"
PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-09.2026-08-23"
MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."

SOURCE_FILES = [
    ROOT / "source" / "id-ID" / "frontmatter-units-01-12.md",
    ROOT / "source" / "id-ID" / "lecture-10.md",
    ROOT / "source" / "id-ID" / "worksheet-10.md",
    ROOT / "source" / "id-ID" / "worksheet-10-solutions.md",
    ROOT / "source" / "id-ID" / "lecture-11.md",
    ROOT / "source" / "id-ID" / "worksheet-11.md",
    ROOT / "source" / "id-ID" / "worksheet-11-solutions.md",
    ROOT / "source" / "id-ID" / "media-credits-unit-11.md",
    ROOT / "source" / "id-ID" / "lecture-12.md",
    ROOT / "source" / "id-ID" / "worksheet-12.md",
    ROOT / "source" / "id-ID" / "worksheet-12-solutions.md",
    ROOT / "source" / "id-ID" / "media-credits-unit-12.md",
]

EXPECTED_SOURCE_SHA256 = {
    "source/id-ID/frontmatter-units-01-12.md": "b1ff35e4f17b8cab93489dc28eaab1d15b77f6212859a4cc9eae67527cabd8ce",
    "source/id-ID/lecture-10.md": "08a496387da53cefb7e1f427fa8d762465d31c18618be7ea897fe8246da21e6d",
    "source/id-ID/worksheet-10.md": "aa3a60bf17308df5d07ae88941eaf3cda9171a17e4ddd9e9c8c84053ee1d0f62",
    "source/id-ID/worksheet-10-solutions.md": "1ccbbc4377c44889f4659a54c6cba8e5314eb32b2443a9d74352aeb631a56a08",
    "source/id-ID/lecture-11.md": "268324606509f055a70c35d782982108763d58ccc2993e33e42d80e54aea4dcb",
    "source/id-ID/worksheet-11.md": "92f97d3eb40474184b678ba80c4f804b1d81600380fe14a322a19143905ecb39",
    "source/id-ID/worksheet-11-solutions.md": "9799331d7eb1ed32b3d9c092b54d5e77bad71dab831090065f347a0d50c3b2a2",
    "source/id-ID/media-credits-unit-11.md": "423cdad2e676539994766627b9ff48aa20f337ea4b6ed806bee565481c50f7a3",
    "source/id-ID/lecture-12.md": "bab84765bec69ceef42a658579aa02162b45d4e1b2cdf55331031b1663596cd4",
    "source/id-ID/worksheet-12.md": "e4228a331ce1471dbef7e8f408ceaab309b8b92f51400a011998944e347fea99",
    "source/id-ID/worksheet-12-solutions.md": "aea4ad61cfc3bb7412f6690a850377c9418021aa5ff226173b51f9fb9b06d516",
    "source/id-ID/media-credits-unit-12.md": "aefe17911251cd292ae4431441f122003a5307b2b9205918809e5c077de593c0",
}

TERMINOLOGY_CONCEPTS = {
    "AGT-0055": "concept.short-exact-sequence",
    "AGT-0056": "concept.non-zero-divisor",
    "AGT-0057": "concept.localization",
    "AGT-0058": "concept.point-ideal",
    "AGT-0059": "concept.artinian",
    "AGT-0060": "concept.algebraic-dependence",
    "AGT-0061": "concept.algebraic-independence",
    "AGT-0062": "concept.hilbert-nullstellensatz",
    "AGT-0063": "concept.coordinate-ring",
    "AGT-0064": "concept.unit-ideal",
    "AGT-0065": "concept.residue-field",
    "AGT-0066": "concept.extension-ideal",
    "AGT-0067": "concept.principal-open-set",
    "AGT-0068": "concept.k-spectrum",
    "AGT-0069": "concept.spectrum-map",
    "AGT-0070": "concept.closed-embedding",
    "AGT-0071": "concept.substitution-homomorphism",
    "AGT-0072": "concept.tensor-product",
    "AGT-0073": "concept.product-topology",
    "AGT-0074": "concept.identity-theorem",
    "AGT-0075": "concept.functor",
}

CORRECTION_TARGETS = {
    "AGC-ADAPT-0021": "br-ak-2025-2026-w10-sol-06",
    "AGC-ADAPT-0022": "br-ak-2025-2026-w10-sol-17",
    "AGC-CORR-0023": "br-ak-2025-2026-l11-thm-03-proof",
    "AGC-ADAPT-0024": "br-ak-2025-2026-w11-ex-19",
    "AGC-ADAPT-0025": "br-ak-2025-2026-w12-sol-06",
    "AGC-ADAPT-0026": "br-ak-2025-2026-l12-thm-01-proof",
    "AGC-CORR-0027": "br-ak-2025-2026-w10-sol-06",
}

UNIT_SPEC: dict[int, dict[str, Any]] = {
    10: {
        "manifest": ROOT / "authority" / "wikiversity" / "unit-10" / "UNIT_AUTHORITY_MANIFEST.json",
        "map": ROOT / "authority" / "wikiversity" / "unit-10" / "ORDERED_EXERCISE_MAP.json",
        "rights": ROOT / "authority" / "RIGHTS-unit-10.csv",
        "closure": ROOT / "authority" / "ASSET_CLOSURE-unit-10.json",
        "exercise_count": 29,
        "solutions": (1, 6, 9, 16, 17, 20),
        "media_count": 0,
        "expected": {
            "manifest": "f8b4f8bf12a0613f774352df31941d79a35d9eed10f2d8fb5570f9ffe07bfb43",
            "map": "972e36256d128916533a33be1d2feedfdecbd133a0dbba96193a85477cf7e92c",
            "rights": "688820e2de7916d7c3299fca0a3ce5d415cdb325e3061ffd5f9ca8220ffc617f",
            "closure": "981122ef8078677affd5735ffe022be8c08359717dc5794c21c7fb591fc15738",
        },
    },
    11: {
        "manifest": ROOT / "authority" / "wikiversity" / "unit-11" / "UNIT_AUTHORITY_MANIFEST.json",
        "map": ROOT / "authority" / "wikiversity" / "unit-11" / "ORDERED_EXERCISE_MAP.json",
        "rights": ROOT / "authority" / "RIGHTS-unit-11.csv",
        "closure": ROOT / "authority" / "ASSET_CLOSURE-unit-11.json",
        "exercise_count": 26,
        "solutions": (6, 7),
        "media_count": 1,
        "expected": {
            "manifest": "ea2d4936bb27e88b2863f8fecbddd5570992c432aee66c72066597709da65a47",
            "map": "6298bafd7656e4653b504706b437e89de7faa92a75fac10c31d51ad9644a20cf",
            "rights": "54dd27757dc7a7a2084c2c333d0405483377d6e8ce4d52f2c3f3fdb487bfeb99",
            "closure": "eecc6bb22fbead45c6cdf064fcce66c3d39ca24453b35455b31f865212895c55",
        },
    },
    12: {
        "manifest": ROOT / "authority" / "wikiversity" / "unit-12" / "UNIT_AUTHORITY_MANIFEST.json",
        "map": ROOT / "authority" / "wikiversity" / "unit-12" / "ORDERED_EXERCISE_MAP.json",
        "rights": ROOT / "authority" / "RIGHTS-unit-12.csv",
        "closure": ROOT / "authority" / "ASSET_CLOSURE-unit-12.json",
        "exercise_count": 30,
        "solutions": (6, 12),
        "media_count": 4,
        "expected": {
            "manifest": "181ce377bd68639b12511a9b1402ca03fd76c6107325195d3aa51a81b7286559",
            "map": "a37f874ffa17dd35ed4375f2956786793e475fcd5e2ded0333207c546e7e91db",
            "rights": "d645f9f0898da0d7b4c918900677f837846a3d16d5fb6424e77547ff2847b691",
            "closure": "058cd370d365150ea39a62ca0ed151189d6cf4b4e3cfcca27e9030eea148cea4",
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
    require(path.is_file(), f"Missing Units 1--9 baseline file: {rel(path)}")
    require(digest(path) == expected, f"Units 1--9 baseline hash changed: {rel(path)}")

manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
require(manifest.get("schema") == "ag-bridge-backend-export-manifest-v2", "Unexpected backend manifest schema")
require(manifest.get("through_unit") == 12, "Backend manifest is not through Unit 12")
require(manifest.get("scope") == "cumulative Units 1--12", "Backend manifest scope mismatch")
require(manifest.get("model_provenance") == MODEL_PROVENANCE, "Backend manifest model provenance mismatch")
require(manifest.get("record_count", 0) > BASELINE_RECORD_COUNT, "Backend has no Units 10--12 extension")
require(schema.get("title", "").endswith("Units 1--12"), "Backend record schema title is stale")

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
# object.  This proves stable-ID and payload-byte identity for all 6,393 rows.
baseline_lines = (BASELINE / "records.jsonl").read_text(encoding="utf-8").splitlines()
baseline_raw_by_id = {json.loads(line)["stable_id"]: line for line in baseline_lines}
require(len(baseline_raw_by_id) == BASELINE_RECORD_COUNT, "Units 1--9 baseline count changed")
require(set(baseline_raw_by_id) <= set(raw_by_id), "Backend dropped a Units 1--9 stable ID")
require(all(raw_by_id[key] == raw for key, raw in baseline_raw_by_id.items()), "A Units 1--9 record payload byte changed")

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
require(build.get("schema") == "ag-bridge-build-receipt-v2" and build.get("through_unit") == 12, "Reader build receipt mismatch")
require(machine.get("status") == "PASS" and machine.get("through_unit") == 12, "Machine reader QA mismatch")
require(visual.get("result") == "PASS" and visual.get("through_unit") == 12, "Visual reader QA mismatch")
require(responsive.get("status") == "PASS" and responsive.get("through_unit") == 12, "Responsive reader QA mismatch")
require(protected.get("status") == "PASS" and protected.get("unit") == 12, "Protected Unit 12 release-boundary receipt mismatch")

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
    ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-12.pdf",
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
require(source_heading_ids <= id_set, "Backend dropped a Unit 10--12 source heading")

with TERMINOLOGY_PATH.open("r", encoding="utf-8", newline="") as stream:
    terminology_rows = {
        row["term_id"]: row
        for row in csv.DictReader(stream)
        if row.get("term_id") in TERMINOLOGY_CONCEPTS
    }
require(set(terminology_rows) == set(TERMINOLOGY_CONCEPTS), "Units 10--12 terminology ledger closure mismatch")
expected_term_ids: set[str] = set()
expected_concept_ids: set[str] = set()
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
    require(term.get("content_sha256") == row_sha256 and concept.get("content_sha256") == row_sha256, f"Terminology ledger hash mismatch for {term_id}")

with CORRECTIONS_PATH.open("r", encoding="utf-8", newline="") as stream:
    correction_rows = {
        row["correction_id"]: row
        for row in csv.DictReader(stream)
        if row.get("correction_id") in CORRECTION_TARGETS
    }
require(set(correction_rows) == set(CORRECTION_TARGETS), "Units 10--12 correction ledger closure mismatch")
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
    expected_exercise_ids.update(f"exercise.br-ak-2025-2026-w{unit:02d}-ex-{number:02d}" for number in range(1, spec["exercise_count"] + 1))
    expected_solution_ids.update(f"solution.br-ak-2025-2026-w{unit:02d}-sol-{number:02d}" for number in spec["solutions"])
    expected_assets.update(row["asset_id"] for row in rights_rows)
    expected_rights.update(f"rights.{row['asset_id']}" for row in rights_rows)
    unit_findings[str(unit)] = {
        "exercise_count": spec["exercise_count"],
        "public_solution_count": len(spec["solutions"]),
        "solution_exercise_numbers": list(spec["solutions"]),
        "media_positions": spec["media_count"],
        "manifest_sha256": digest(spec["manifest"]),
        "exercise_map_sha256": digest(spec["map"]),
        "rights_sha256": digest(spec["rights"]),
        "asset_closure_sha256": digest(spec["closure"]),
    }

require(expected_exercise_ids <= id_set, "Typed exercise closure for Units 10--12 is incomplete")
require(expected_solution_ids <= id_set, "Typed solution closure for Units 10--12 is incomplete")
require(expected_assets <= id_set, "Unit 10--12 asset closure is incomplete")
require(expected_rights <= id_set, "Unit 10--12 rights closure is incomplete")
require(not ({record["stable_id"] for record in records if record["entity_class"] == "asset" and record.get("edition_id") == CUMULATIVE_EDITION} - expected_assets), "Unexpected Unit 10--12 asset record")

edition = next((record for record in records if record["stable_id"] == CUMULATIVE_EDITION), None)
require(edition is not None, "Cumulative Unit 12 edition record is absent")
require(edition.get("supersedes") == PREVIOUS_EDITION, "Cumulative edition lineage mismatch")
require(edition["payload"].get("through_unit") == 12, "Cumulative edition payload boundary mismatch")
require(edition["payload"].get("model_provenance") == MODEL_PROVENANCE, "Edition model provenance mismatch")

new_records = [record for record in records if record["stable_id"] not in baseline_raw_by_id]
require(new_records, "No new records were exported")
require(all(record.get("provenance", {}).get("model_provenance") == MODEL_PROVENANCE for record in new_records), "A new record lacks exact model provenance")
required_qa_ids = {"qa.units0112.machine", "qa.units0112.visual", "qa.units0112.responsive", "qa.unit12.protected"}
require(required_qa_ids <= id_set, "Reader QA-event closure is incomplete")

relations = [record for record in records if record["entity_class"] == "relation" and record["stable_id"].startswith("relation.units0112.")]
relation_counts = Counter(record["payload"].get("relation_type") for record in relations)
require(relation_counts["solves"] == 2 * len(expected_solution_ids), "Untyped/typed solution relations are incomplete")
require(relation_counts["illustrates"] == len(expected_assets), "Asset illustration relations are incomplete")
require(relation_counts["validated_by"] == 4, "Reader QA relations are incomplete")
require(relation_counts["extends"] == 1 and relation_counts["derived_from"] == 1, "Edition lineage/source relations are incomplete")
require(relation_counts["labels"] == len(TERMINOLOGY_CONCEPTS), "Terminology label relations are incomplete")
require(relation_counts["adapts"] == 5 and relation_counts["corrects"] == 2, "Correction/adaptation relations are incomplete")
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

baseline_block = manifest.get("units_01_09_baseline", {})
require(baseline_block.get("record_count") == BASELINE_RECORD_COUNT, "Manifest baseline count mismatch")
require(baseline_block.get("record_bytes_preserved") is True, "Manifest does not assert byte preservation")
require(baseline_block.get("stable_ids_and_payloads_preserved") is True, "Manifest does not assert payload preservation")

receipt = {
    "schema": "ag-bridge-backend-qa-v6",
    "result": "PASS",
    "through_unit": 12,
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
        "units_01_09_baseline_record_count": BASELINE_RECORD_COUNT,
        "units_01_09_baseline_records_exactly_preserved": True,
    },
    "units_10_12": unit_findings,
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
        "new_concept_count": len(expected_concept_ids),
        "corrections_path": rel(CORRECTIONS_PATH),
        "corrections_sha256": digest(CORRECTIONS_PATH),
        "new_correction_count": len(expected_correction_ids),
    },
    "model_provenance": MODEL_PROVENANCE,
    "validation": {
        "canonical_jsonl_and_schema_surface": True,
        "unique_stable_ids": True,
        "parent_resource_edition_rights_concept_and_relation_closure": True,
        "units_01_09_record_and_payload_byte_identity": True,
        "source_hashes_match_frozen_values_and_reader_inputs": True,
        "authority_manifest_map_rights_asset_solution_closure": True,
        "units_10_12_terminology_and_correction_ledger_closure": True,
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
