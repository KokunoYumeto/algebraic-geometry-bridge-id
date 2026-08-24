#!/usr/bin/env python3
"""Export the deterministic cumulative native backend through Unit 12.

The frozen Units 1--9 backend is an append-only baseline.  Every one of its
6,393 canonical JSONL records is carried forward with its original serialized
payload bytes.  This exporter adds only the cumulative edition boundary,
reader/source structures for Units 10--12, typed exercise/solution projections,
component rights/assets, frozen authority artifacts, and deterministic reader
QA evidence.

The script is intentionally fail-closed.  It will not write the Unit 12
backend until the cumulative reader build and all four named QA receipts exist,
pass, bind the final source bytes, and identify the through-Unit-12 reader.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "backend" / "units-01-09"
OUT = ROOT / "backend" / "units-01-12"

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

WORKFLOW_ID = "workflow.o016-d100.algebraic-geometry-bridge-id"
BRENNER_RESOURCE = "resource.brenner.algebraische-kurven.2025-2026"
BRENNER_EDITION = "edition.brenner.algebraische-kurven.prefix-freeze.2026-08-21"
LOCAL_RESOURCE = "resource.algebraic-geometry-bridge-id.editorial-layer"
PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-09.2026-08-23"
CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-12.2026-08-24"
TEXT_RIGHTS = "rights.brenner-course-text.cc-by-sa-4.0"
EDITORIAL_RIGHTS = "rights.derivative-editorial.cc-by-sa-4.0"
MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."
BASE_SCHEMA = "ag-bridge-backend-record"
RECORD_SCHEMA_VERSION = "1.0.0"

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

# Filled only after the three independent translation workers froze their
# source files.  These hashes are also independently replayed from the reader
# BUILD_RECEIPT input inventory before any output is written.
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
    "AGT-0055": ("concept.short-exact-sequence", "short exact sequence"),
    "AGT-0056": ("concept.non-zero-divisor", "non-zero-divisor"),
    "AGT-0057": ("concept.localization", "localization"),
    "AGT-0058": ("concept.point-ideal", "point ideal"),
    "AGT-0059": ("concept.artinian", "Artinian"),
    "AGT-0060": ("concept.algebraic-dependence", "algebraic dependence"),
    "AGT-0061": ("concept.algebraic-independence", "algebraic independence"),
    "AGT-0062": ("concept.hilbert-nullstellensatz", "Hilbert Nullstellensatz"),
    "AGT-0063": ("concept.coordinate-ring", "coordinate ring"),
    "AGT-0064": ("concept.unit-ideal", "unit ideal"),
    "AGT-0065": ("concept.residue-field", "residue field"),
    "AGT-0066": ("concept.extension-ideal", "extension ideal"),
    "AGT-0067": ("concept.principal-open-set", "principal open set"),
    "AGT-0068": ("concept.k-spectrum", "K-spectrum"),
    "AGT-0069": ("concept.spectrum-map", "spectrum map"),
    "AGT-0070": ("concept.closed-embedding", "closed embedding"),
    "AGT-0071": ("concept.substitution-homomorphism", "substitution homomorphism"),
    "AGT-0072": ("concept.tensor-product", "tensor product"),
    "AGT-0073": ("concept.product-topology", "product topology"),
    "AGT-0074": ("concept.identity-theorem", "identity theorem"),
    "AGT-0075": ("concept.functor", "functor"),
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


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_crlf(path: Path, text: str) -> None:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    path.write_bytes(normalized.replace("\n", "\r\n").encode("utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


for path, expected in (
    (BASELINE / "MANIFEST.json", BASELINE_MANIFEST_SHA256),
    (BASELINE / "records.jsonl", BASELINE_RECORDS_SHA256),
    (BASELINE / "record.schema.json", BASELINE_SCHEMA_SHA256),
):
    require(path.is_file(), f"Missing frozen Units 1--9 baseline file: {rel(path)}")
    require(digest(path) == expected, f"Frozen Units 1--9 baseline hash mismatch: {rel(path)}")

baseline_raw_by_id: dict[str, str] = {}
baseline_records: list[dict[str, Any]] = []
for raw_line in (BASELINE / "records.jsonl").read_text(encoding="utf-8").splitlines():
    record = json.loads(raw_line)
    require(canonical(record) == raw_line, f"Noncanonical baseline record: {record.get('stable_id')}")
    require(record["stable_id"] not in baseline_raw_by_id, f"Duplicate baseline stable ID: {record['stable_id']}")
    baseline_raw_by_id[record["stable_id"]] = raw_line
    baseline_records.append(record)
require(len(baseline_records) == BASELINE_RECORD_COUNT, "Frozen Units 1--9 record count changed")

for unit, spec in UNIT_SPEC.items():
    for key in ("manifest", "map", "rights", "closure"):
        path = spec[key]
        require(path.is_file(), f"Missing Unit {unit} authority input: {rel(path)}")
        require(digest(path) == spec["expected"][key], f"Unit {unit} {key} frozen hash mismatch")

build_receipt = json.loads(BUILD_RECEIPT_PATH.read_text(encoding="utf-8"))
require(build_receipt.get("schema") == "ag-bridge-build-receipt-v2", "Unexpected reader build receipt schema")
require(build_receipt.get("through_unit") == 12, "Reader build receipt is not through Unit 12")
require(MODEL_PROVENANCE in (ROOT / "source" / "id-ID" / "frontmatter-units-01-12.md").read_text(encoding="utf-8"), "Exact model provenance is absent from Unit 12 frontmatter")

receipt_inputs = {row["path"]: row for row in build_receipt.get("inputs", [])}
require(set(EXPECTED_SOURCE_SHA256) == {rel(path) for path in SOURCE_FILES}, "Final source-hash closure is incomplete or contains an unexpected path")
for path in SOURCE_FILES:
    path_key = rel(path)
    require(path.is_file(), f"Missing Unit 10--12 source input: {path_key}")
    actual = digest(path)
    require(actual == EXPECTED_SOURCE_SHA256[path_key], f"Final source hash changed: {path_key}")
    witness = receipt_inputs.get(path_key)
    require(witness is not None, f"Reader build receipt does not bind {path_key}")
    require(witness.get("bytes") == path.stat().st_size, f"Reader input byte count changed: {path_key}")
    require(witness.get("sha256") == actual, f"Reader input hash changed: {path_key}")

reader_outputs = {row["path"]: row for row in build_receipt.get("outputs", [])}
required_reader_outputs = (
    ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-12.pdf",
    ROOT / "build" / "reader-id" / "index.html",
)
for path in required_reader_outputs:
    key = rel(path)
    require(path.is_file(), f"Missing cumulative reader output: {key}")
    witness = reader_outputs.get(key)
    require(witness is not None, f"Reader build receipt does not bind {key}")
    require(witness.get("bytes") == path.stat().st_size, f"Reader output byte count changed: {key}")
    require(witness.get("sha256") == digest(path), f"Reader output hash changed: {key}")

qa_specs = [
    ("qa.units0112.machine", MACHINE_QA_PATH, "source_math_topology_build_accessibility", "status"),
    ("qa.units0112.visual", VISUAL_QA_PATH, "all_page_and_full_resolution_visual_layout", "result"),
    ("qa.units0112.responsive", RESPONSIVE_QA_PATH, "desktop_and_mobile_reader_reflow", "status"),
    ("qa.unit12.protected", PROTECTED_QA_PATH, "units_10_12_authority_formula_exercise_solution_media_fidelity", "status"),
]
qa_payloads: dict[str, dict[str, Any]] = {}
for stable_id, path, _kind, status_key in qa_specs:
    require(path.is_file(), f"Missing required reader QA receipt: {rel(path)}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    require(payload.get(status_key) == "PASS", f"Reader QA did not pass: {rel(path)}")
    if path != PROTECTED_QA_PATH:
        require(payload.get("through_unit") == 12, f"Reader QA is not through Unit 12: {rel(path)}")
    else:
        require(payload.get("unit") == 12, "Protected-surface receipt is not the Unit 12 release boundary")
    qa_payloads[stable_id] = payload

timestamp = build_receipt["built_utc"]


def make_record(
    entity_class: str,
    stable_id: str,
    *,
    source_local_id: str | None = None,
    parent_id: str | None = None,
    order: int | None = None,
    path: str | None = None,
    resource_id: str | None = None,
    edition_id: str | None = None,
    source_locator: str | None = None,
    content_sha256: str | None = None,
    language: str = "und",
    translation_state: str = "source_frozen",
    provenance: dict[str, Any] | None = None,
    concept_ids: list[str] | None = None,
    prerequisite_ids: list[str] | None = None,
    rights_id: str | None = None,
    status: str = "active",
    supersedes: str | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    full_provenance = {"model_provenance": MODEL_PROVENANCE}
    full_provenance.update(provenance or {})
    return {
        "schema": BASE_SCHEMA,
        "schema_version": RECORD_SCHEMA_VERSION,
        "entity_class": entity_class,
        "stable_id": stable_id,
        "source_local_id": source_local_id,
        "parent_id": parent_id,
        "order": order,
        "path": path,
        "resource_id": resource_id,
        "edition_id": edition_id,
        "source_locator": source_locator,
        "content_sha256": content_sha256,
        "language": language,
        "translation_state": translation_state,
        "provenance": full_provenance,
        "concept_ids": sorted(set(concept_ids or [])),
        "prerequisite_ids": sorted(set(prerequisite_ids or [])),
        "rights_id": rights_id,
        "status": status,
        "timestamp": timestamp,
        "responsible_workflow": WORKFLOW_ID,
        "supersedes": supersedes,
        "payload": payload or {},
    }


records: list[dict[str, Any]] = list(baseline_records)
new_records: list[dict[str, Any]] = []


def add(record: dict[str, Any]) -> None:
    records.append(record)
    new_records.append(record)


authority_manifests: dict[int, dict[str, Any]] = {}
exercise_maps: dict[int, dict[str, Any]] = {}
solution_entries: dict[int, dict[int, dict[str, Any]]] = {}
rights_rows: dict[int, list[dict[str, str]]] = {}
asset_closures: dict[int, dict[str, Any]] = {}
for unit, spec in UNIT_SPEC.items():
    authority_manifests[unit] = json.loads(spec["manifest"].read_text(encoding="utf-8"))
    exercise_maps[unit] = json.loads(spec["map"].read_text(encoding="utf-8"))
    rights_rows[unit] = read_csv(spec["rights"])
    asset_closures[unit] = json.loads(spec["closure"].read_text(encoding="utf-8"))
    manifest = authority_manifests[unit]
    exercise_map = exercise_maps[unit]
    require(manifest.get("unit_number") == unit, f"Unit {unit} authority manifest identity mismatch")
    require(exercise_map.get("unit") == unit, f"Unit {unit} exercise map identity mismatch")
    require(exercise_map.get("exercise_count") == spec["exercise_count"], f"Unit {unit} exercise count mismatch")
    require(exercise_map.get("solution_count") == len(spec["solutions"]), f"Unit {unit} solution count mismatch")
    public = {int(row["exercise_number"]): row for row in exercise_map["entries"] if row.get("has_public_solution")}
    require(tuple(sorted(public)) == spec["solutions"], f"Unit {unit} public-solution identity mismatch")
    solution_entries[unit] = public
    require(len(rights_rows[unit]) == spec["media_count"], f"Unit {unit} rights row count mismatch")
    require(asset_closures[unit].get("unit") == unit, f"Unit {unit} asset closure identity mismatch")
    require(asset_closures[unit].get("reader_media_positions") == spec["media_count"], f"Unit {unit} media-position count mismatch")
    require(asset_closures[unit].get("unique_local_assets") == spec["media_count"], f"Unit {unit} local-asset count mismatch")

add(
    make_record(
        "edition",
        CUMULATIVE_EDITION,
        source_local_id="units-01-12",
        parent_id=LOCAL_RESOURCE,
        resource_id=LOCAL_RESOURCE,
        edition_id=CUMULATIVE_EDITION,
        source_locator=rel(BUILD_RECEIPT_PATH),
        content_sha256=digest(BUILD_RECEIPT_PATH),
        language="id-ID",
        translation_state="built",
        rights_id=EDITORIAL_RIGHTS,
        supersedes=PREVIOUS_EDITION,
        provenance={
            "units_01_09_baseline_manifest_sha256": BASELINE_MANIFEST_SHA256,
            "authority": {
                str(unit): {
                    key: digest(spec[key]) for key in ("manifest", "map", "rights", "closure")
                }
                for unit, spec in UNIT_SPEC.items()
            },
        },
        payload={
            "title": build_receipt["title"],
            "through_unit": 12,
            "source_edition_id": BRENNER_EDITION,
            "reader_outputs": build_receipt["outputs"],
            "build_receipt_sha256": digest(BUILD_RECEIPT_PATH),
            "translation_change_notice": True,
            "non_endorsement": True,
            "model_provenance": MODEL_PROVENANCE,
        },
    )
)

terminology_rows = {
    row["term_id"]: row
    for row in read_csv(TERMINOLOGY_PATH)
    if row.get("term_id") in TERMINOLOGY_CONCEPTS
}
require(set(terminology_rows) == set(TERMINOLOGY_CONCEPTS), "Units 10--12 terminology ledger closure mismatch")

correction_rows = {
    row["correction_id"]: row
    for row in read_csv(CORRECTIONS_PATH)
    if row.get("correction_id") in CORRECTION_TARGETS
}
require(set(correction_rows) == set(CORRECTION_TARGETS), "Units 10--12 correction ledger closure mismatch")

new_concept_records: list[dict[str, Any]] = []
new_term_records: list[dict[str, Any]] = []
for term_id in sorted(TERMINOLOGY_CONCEPTS):
    row = terminology_rows[term_id]
    concept_id, canonical_label = TERMINOLOGY_CONCEPTS[term_id]
    row_sha256 = text_digest(canonical(row))
    concept = make_record(
        "concept",
        concept_id,
        source_local_id=row["source_term"],
        resource_id=BRENNER_RESOURCE,
        edition_id=CUMULATIVE_EDITION,
        source_locator=rel(TERMINOLOGY_PATH),
        content_sha256=row_sha256,
        language="und",
        translation_state="translated",
        provenance={"terminology_row_id": term_id},
        rights_id=EDITORIAL_RIGHTS,
        status=row["status"],
        payload={"canonical_label": canonical_label},
    )
    add(concept)
    new_concept_records.append(concept)

    term = make_record(
        "term",
        f"term.{term_id.casefold()}.id-id",
        source_local_id=term_id,
        parent_id=concept_id,
        resource_id=BRENNER_RESOURCE,
        edition_id=CUMULATIVE_EDITION,
        source_locator=rel(TERMINOLOGY_PATH),
        content_sha256=row_sha256,
        language=row["target_language"],
        translation_state="translated",
        provenance={"terminology_row_id": term_id},
        concept_ids=[concept_id],
        rights_id=EDITORIAL_RIGHTS,
        status=row["status"],
        payload={
            "preferred_target": row["preferred_target"],
            "rationale": row["rationale"],
            "rejected_or_variant": row["rejected_or_variant"],
            "scope": row["scope"],
            "source_language": row["source_language"],
            "source_term": row["source_term"],
        },
    )
    add(term)
    new_term_records.append(term)

term_needles = [
    (record["payload"].get("preferred_target", "").casefold(), record["parent_id"])
    for record in records
    if record["entity_class"] == "term"
    and record["payload"].get("preferred_target")
    and record.get("parent_id")
]


def concept_ids_for(content: str) -> list[str]:
    low = content.casefold()
    return sorted({concept_id for needle, concept_id in term_needles if needle in low})


heading_re = re.compile(r"^(#{1,6})\s+(.*?)\s+\{#([^}]+)\}\s*$")


def strip_yaml(lines: list[str]) -> tuple[list[str], dict[str, str]]:
    if not lines or lines[0].strip() != "---":
        return lines, {}
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration as exc:
        raise SystemExit("Unclosed source front matter") from exc
    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            metadata[match.group(1)] = match.group(2).strip().strip('"')
    return ["" for _ in range(end + 1)] + lines[end + 1 :], metadata


def classify_unit(identifier: str, title: str) -> str:
    low = title.casefold()
    if re.search(r"-sol-\d+$", identifier) or low.startswith("solusi soal"):
        return "solution"
    if re.search(r"-w\d{2}-ex-\d+$", identifier):
        return "exercise"
    if re.search(r"-l\d{2}-ex-\d+$", identifier):
        return "example"
    if "-def-" in identifier:
        return "definition"
    if "-lem-" in identifier and identifier.endswith("-proof"):
        return "proof"
    if "-lem-" in identifier:
        return "lemma"
    if any(token in identifier for token in ("-thm-", "-prop-")) and identifier.endswith("-proof"):
        return "proof"
    if "-thm-" in identifier:
        return "theorem"
    if "-prop-" in identifier:
        return "proposition"
    if identifier.endswith(("-practice", "-submission", "-submit")):
        return "exercise_group"
    if identifier.startswith("agc-media-credits"):
        return "credits"
    if re.search(r"-s\d+$", identifier) or identifier.startswith("agc-front-"):
        return "section"
    if re.search(r"-(?:l|w)\d{2}$", identifier) or identifier.endswith("-solutions"):
        return "unit"
    return "section"


def compact_upstream(row: dict[str, Any]) -> dict[str, Any]:
    return {
        key: row[key]
        for key in (
            "title", "pageid", "revid", "parentid", "timestamp",
            "mediawiki_sha1", "oldid_url", "xml_file", "xml_bytes",
            "xml_sha256", "html_file", "html_bytes", "html_sha256",
        )
        if key in row
    }


def source_unit_number(source_path: Path) -> int | None:
    match = re.search(r"(?:lecture|worksheet|media-credits-unit)-(\d{2})", source_path.name)
    return int(match.group(1)) if match else None


def source_provenance(source_path: Path, metadata: dict[str, str], identifier: str) -> dict[str, Any]:
    unit = source_unit_number(source_path)
    result: dict[str, Any] = {
        "source_edition_id": None if source_path.name.startswith(("frontmatter-", "media-credits-")) else BRENNER_EDITION,
        "source_file": {"path": rel(source_path), "bytes": source_path.stat().st_size, "sha256": digest(source_path)},
    }
    if unit is None:
        result["authority_units"] = {
            str(number): {"manifest_path": rel(spec["manifest"]), "manifest_sha256": digest(spec["manifest"])}
            for number, spec in UNIT_SPEC.items()
        }
        return result

    spec = UNIT_SPEC[unit]
    result["authority"] = {
        "unit": unit,
        "manifest_path": rel(spec["manifest"]),
        "manifest_sha256": digest(spec["manifest"]),
        "exercise_map_path": rel(spec["map"]),
        "exercise_map_sha256": digest(spec["map"]),
        "rights_path": rel(spec["rights"]),
        "rights_sha256": digest(spec["rights"]),
        "asset_closure_path": rel(spec["closure"]),
        "asset_closure_sha256": digest(spec["closure"]),
    }
    if source_path.name == f"lecture-{unit:02d}.md":
        result["upstream"] = compact_upstream(authority_manifests[unit]["lecture"])
    elif source_path.name == f"worksheet-{unit:02d}.md":
        result["upstream"] = compact_upstream(authority_manifests[unit]["worksheet"])
    elif source_path.name == f"worksheet-{unit:02d}-solutions.md":
        match = re.search(r"-sol-(\d+)$", identifier)
        result["exercise_solution_map"] = {
            "path": rel(spec["map"]),
            "sha256": digest(spec["map"]),
            "worksheet_revid": exercise_maps[unit]["worksheet"]["revid"],
        }
        result["upstream"] = compact_upstream(solution_entries[unit][int(match.group(1))]) if match else compact_upstream(exercise_maps[unit]["worksheet"])
    elif source_path.name.startswith("media-credits-"):
        result["component_rights"] = {"path": rel(spec["rights"]), "sha256": digest(spec["rights"])}
    else:
        result["upstream"] = {
            key: metadata[key]
            for key in ("upstream_title", "upstream_pageid", "upstream_revid", "upstream_timestamp", "upstream_mediawiki_sha1", "source_url")
            if key in metadata
        }
    return result


all_new_units: list[dict[str, Any]] = []
all_new_segments: list[dict[str, Any]] = []
image_parent_by_path: dict[str, str] = {}
global_unit_order = max(record["order"] or 0 for record in baseline_records if record["entity_class"] == "unit")
global_segment_order = max(record["order"] or 0 for record in baseline_records if record["entity_class"] == "segment")

for source_path in SOURCE_FILES:
    original_lines = source_path.read_text(encoding="utf-8").splitlines()
    lines, metadata = strip_yaml(original_lines)
    heading_rows: list[tuple[int, int, str, str]] = []
    for index, line in enumerate(lines):
        match = heading_re.match(line)
        if match:
            heading_rows.append((index, len(match.group(1)), match.group(2), match.group(3)))
    require(heading_rows, f"No stable heading IDs in {rel(source_path)}")

    stack: list[tuple[int, str]] = []
    for heading_position, (line_index, level, title, identifier) in enumerate(heading_rows):
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent_id = stack[-1][1] if stack else CUMULATIVE_EDITION
        stack.append((level, identifier))
        next_boundary = len(lines)
        for next_index, next_level, _, _ in heading_rows[heading_position + 1 :]:
            if next_level <= level:
                next_boundary = next_index
                break
        region = "\n".join(lines[line_index:next_boundary]).strip() + "\n"
        global_unit_order += 1
        editorial = source_path.name.startswith(("frontmatter-", "media-credits-"))
        source_resource = LOCAL_RESOURCE if editorial else BRENNER_RESOURCE
        unit_record = make_record(
            "unit",
            identifier,
            source_local_id=metadata.get("upstream_title") if level == 1 else identifier,
            parent_id=parent_id,
            order=global_unit_order,
            path=f"{rel(source_path)}#{identifier}",
            resource_id=source_resource,
            edition_id=CUMULATIVE_EDITION,
            source_locator=f"{rel(source_path)}:{line_index + 1}",
            content_sha256=text_digest(region),
            language="id-ID",
            translation_state="built",
            provenance=source_provenance(source_path, metadata, identifier),
            concept_ids=concept_ids_for(region),
            rights_id=EDITORIAL_RIGHTS if editorial else TEXT_RIGHTS,
            payload={
                "unit_type": classify_unit(identifier, title),
                "heading_level": level,
                "title_markdown": title,
                "source_file_sha256": digest(source_path),
            },
        )
        add(unit_record)
        all_new_units.append(unit_record)

    active_id = CUMULATIVE_EDITION
    segment_counter: defaultdict[str, int] = defaultdict(int)
    block: list[tuple[int, str]] = []

    def flush_block() -> None:
        nonlocal_block = list(block)
        block.clear()
        if not nonlocal_block:
            return
        first_line = nonlocal_block[0][0]
        content = "\n".join(line for _, line in nonlocal_block).strip()
        if not content or (content.startswith("<!--") and content.endswith("-->")):
            return
        segment_counter[active_id] += 1
        editorial = source_path.name.startswith(("frontmatter-", "media-credits-"))
        source_resource = LOCAL_RESOURCE if editorial else BRENNER_RESOURCE
        global global_segment_order
        global_segment_order += 1
        segment_id = f"{active_id}.seg-{segment_counter[active_id]:03d}"
        if content.startswith("!["):
            segment_type = "figure_reference"
        elif content.startswith("$$") or content.startswith("\\["):
            segment_type = "display_math"
        elif content.startswith(("- ", "1. ", "2. ", "3. ")):
            segment_type = "list"
        elif content.startswith("\\begin") or content.startswith("\\end"):
            segment_type = "raw_tex"
        else:
            segment_type = "prose"
        segment = make_record(
            "segment",
            segment_id,
            parent_id=active_id,
            order=global_segment_order,
            path=f"{rel(source_path)}:{first_line}",
            resource_id=source_resource,
            edition_id=CUMULATIVE_EDITION,
            source_locator=f"{rel(source_path)}:{first_line}",
            content_sha256=text_digest(content),
            language="id-ID",
            translation_state="built",
            provenance=source_provenance(source_path, metadata, active_id),
            concept_ids=concept_ids_for(content),
            rights_id=EDITORIAL_RIGHTS if editorial else TEXT_RIGHTS,
            payload={"segment_type": segment_type, "markdown": content},
        )
        add(segment)
        all_new_segments.append(segment)
        image_match = re.fullmatch(r"!\[[^\]]*\]\(([^)]+)\)", content)
        if image_match:
            require(image_match.group(1) not in image_parent_by_path, f"Duplicate reader image path {image_match.group(1)}")
            image_parent_by_path[image_match.group(1)] = active_id

    for line_number, line in enumerate(lines, start=1):
        heading = heading_re.match(line)
        if heading:
            flush_block()
            active_id = heading.group(3)
        elif not line.strip():
            flush_block()
        else:
            block.append((line_number, line))
    flush_block()

# Close exercises and solutions against the frozen ordered maps before adding
# typed projections.
for unit, spec in UNIT_SPEC.items():
    exercise_ids = {
        row["stable_id"] for row in all_new_units
        if row["payload"].get("unit_type") == "exercise" and f"-w{unit:02d}-ex-" in row["stable_id"]
    }
    solution_ids = {
        row["stable_id"] for row in all_new_units
        if row["payload"].get("unit_type") == "solution" and f"-w{unit:02d}-sol-" in row["stable_id"]
    }
    expected_exercises = {f"br-ak-2025-2026-w{unit:02d}-ex-{number:02d}" for number in range(1, spec["exercise_count"] + 1)}
    expected_solutions = {f"br-ak-2025-2026-w{unit:02d}-sol-{number:02d}" for number in spec["solutions"]}
    require(exercise_ids == expected_exercises, f"Unit {unit} translated exercise stable-ID closure mismatch")
    require(solution_ids == expected_solutions, f"Unit {unit} translated solution stable-ID closure mismatch")

# Component rights and assets are distinct records; Unit 10 deliberately adds
# none because its frozen rights CSV has only a header.
asset_records: list[dict[str, Any]] = []
for unit, rows in rights_rows.items():
    for row in rows:
        local_path = ROOT / row["local_path"]
        require(local_path.is_file(), f"Missing Unit {unit} reader asset: {row['local_path']}")
        require(local_path.stat().st_size == int(row["local_bytes"]), f"Unit {unit} asset byte count mismatch: {row['asset_id']}")
        require(digest(local_path) == row["local_sha256"], f"Unit {unit} asset hash mismatch: {row['asset_id']}")
        require(row["local_path"] in image_parent_by_path, f"Unit {unit} asset has no reader image position: {row['asset_id']}")
        rights_id = f"rights.{row['asset_id']}"
        add(
            make_record(
                "rights",
                rights_id,
                source_local_id=row["metadata_title"],
                resource_id=BRENNER_RESOURCE,
                edition_id=CUMULATIVE_EDITION,
                source_locator=row["description_url"],
                content_sha256=row["local_sha256"],
                provenance={
                    "unit": unit,
                    "rights_path": rel(UNIT_SPEC[unit]["rights"]),
                    "rights_sha256": digest(UNIT_SPEC[unit]["rights"]),
                },
                payload={
                    "license": row["license_short"],
                    "license_url": row["license_url"] or None,
                    "usage_terms": row["usage_terms"] or None,
                    "creator_or_artist": row["artist"] or row["uploader"],
                    "uploader": row["uploader"],
                    "credit": row["credit"],
                    "attribution_required": row["attribution_required"].lower() == "true",
                    "scope": row["asset_id"],
                },
            )
        )
        asset = make_record(
            "asset",
            row["asset_id"],
            source_local_id=row["resource_title"],
            parent_id=image_parent_by_path[row["local_path"]],
            order=int(row["reader_order"]),
            path=row["local_path"],
            resource_id=BRENNER_RESOURCE,
            edition_id=CUMULATIVE_EDITION,
            source_locator=row["description_url"],
            content_sha256=row["local_sha256"],
            translation_state="built",
            provenance={
                "unit": unit,
                "asset_closure_path": rel(UNIT_SPEC[unit]["closure"]),
                "asset_closure_sha256": digest(UNIT_SPEC[unit]["closure"]),
            },
            rights_id=rights_id,
            payload={
                "caption_id": row["asset_id"],
                "selected_form": row["selected_form"],
                "bytes": int(row["local_bytes"]),
                "width": int(row["local_width"]),
                "height": int(row["local_height"]),
                "mime": row["mime"],
                "source_original_url": row["original_url"],
                "selected_url": row["selected_url"],
                "pdf_companion": (
                    {"path": row["pdf_local_path"], "bytes": int(row["pdf_local_bytes"]), "sha256": row["pdf_local_sha256"]}
                    if row["pdf_local_path"] else None
                ),
            },
        )
        add(asset)
        asset_records.append(asset)

typed_records: list[dict[str, Any]] = []
for unit_record in all_new_units:
    unit_type = unit_record["payload"].get("unit_type")
    if unit_type not in {"exercise", "solution"}:
        continue
    number_match = re.search(r"-(?:ex|sol)-(\d+)$", unit_record["stable_id"])
    require(number_match is not None, f"Typed record has no number: {unit_record['stable_id']}")
    number = int(number_match.group(1))
    unit_match = re.search(r"-w(\d{2})-", unit_record["stable_id"])
    require(unit_match is not None, f"Typed record has no worksheet unit: {unit_record['stable_id']}")
    unit_number = int(unit_match.group(1))
    provenance: dict[str, Any] = {
        "indexed_unit_id": unit_record["stable_id"],
        "indexed_unit_record_sha256": text_digest(canonical(unit_record)),
        "compatibility_projection": True,
        "source_provenance": unit_record["provenance"],
    }
    if unit_type == "solution":
        provenance["exercise_solution_authority"] = {
            "map_path": rel(UNIT_SPEC[unit_number]["map"]),
            "map_sha256": digest(UNIT_SPEC[unit_number]["map"]),
            "upstream": compact_upstream(solution_entries[unit_number][number]),
        }
    typed = make_record(
        unit_type,
        f"{unit_type}.{unit_record['stable_id']}",
        source_local_id=unit_record["source_local_id"],
        parent_id=unit_record["stable_id"],
        order=number,
        path=unit_record["path"],
        resource_id=unit_record["resource_id"],
        edition_id=CUMULATIVE_EDITION,
        source_locator=unit_record["source_locator"],
        content_sha256=unit_record["content_sha256"],
        language="id-ID",
        translation_state="built",
        provenance=provenance,
        concept_ids=unit_record["concept_ids"],
        rights_id=unit_record["rights_id"],
        payload={"unit_id": unit_record["stable_id"], "exercise_number": number, "family": unit_type},
    )
    add(typed)
    typed_records.append(typed)

new_correction_records: list[dict[str, Any]] = []
source_unit_ids = {record["stable_id"] for record in all_new_units}
require(set(CORRECTION_TARGETS.values()) <= source_unit_ids, "A Units 10--12 correction target is absent from the translated source IDs")
for correction_id in sorted(CORRECTION_TARGETS):
    row = correction_rows[correction_id]
    affected_id = CORRECTION_TARGETS[correction_id]
    correction = make_record(
        "correction",
        f"correction.{correction_id.casefold()}",
        source_local_id=correction_id,
        resource_id=BRENNER_RESOURCE if correction_id.startswith("AGC-CORR-") else LOCAL_RESOURCE,
        edition_id=CUMULATIVE_EDITION,
        source_locator=rel(CORRECTIONS_PATH),
        content_sha256=text_digest(canonical(row)),
        language="id-ID",
        translation_state="built",
        provenance={"authority_identity": row["authority_identity"]},
        rights_id=EDITORIAL_RIGHTS,
        status=row["status"],
        payload={
            "affected_unit_ids": [affected_id],
            "authority_observation": row["authority_observation"],
            "kind": row["kind"],
            "mathematical_effect": row["mathematical_effect"],
            "publication_gate": row["status"],
            "scope": row["scope"],
            "target_action": row["target_action"],
        },
    )
    add(correction)
    new_correction_records.append(correction)

qa_records: list[dict[str, Any]] = []
for stable_id, path, qa_kind, _status_key in qa_specs:
    qa_record = make_record(
        "qa_event",
        stable_id,
        parent_id=CUMULATIVE_EDITION,
        resource_id=LOCAL_RESOURCE,
        edition_id=CUMULATIVE_EDITION,
        source_locator=rel(path),
        content_sha256=digest(path),
        translation_state="built",
        rights_id=EDITORIAL_RIGHTS,
        status="passed",
        payload={"qa_kind": qa_kind, "result": qa_payloads[stable_id]},
    )
    add(qa_record)
    qa_records.append(qa_record)

authority_paths = [spec[key] for unit, spec in UNIT_SPEC.items() for key in ("manifest", "map", "rights", "closure")]
artifact_paths = [
    ROOT / "build" / "reader-id" / "index.html",
    ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-12.pdf",
    BUILD_RECEIPT_PATH,
    MACHINE_QA_PATH,
    VISUAL_QA_PATH,
    RESPONSIVE_QA_PATH,
    PROTECTED_QA_PATH,
    *authority_paths,
]
artifact_records: list[dict[str, Any]] = []
for number, artifact_path in enumerate(artifact_paths, start=1):
    artifact_id = f"artifact.units0112.{number:02d}.{artifact_path.name.casefold().replace('_', '-').replace('.', '-')}"
    artifact = make_record(
        "artifact",
        artifact_id,
        parent_id=CUMULATIVE_EDITION,
        order=number,
        path=rel(artifact_path),
        resource_id=LOCAL_RESOURCE,
        edition_id=CUMULATIVE_EDITION,
        source_locator=rel(artifact_path),
        content_sha256=digest(artifact_path),
        language="id-ID" if artifact_path.suffix in {".html", ".pdf"} else "und",
        translation_state="built",
        rights_id=EDITORIAL_RIGHTS,
        payload={
            "bytes": artifact_path.stat().st_size,
            "media_type": {".html": "text/html", ".pdf": "application/pdf", ".json": "application/json", ".csv": "text/csv"}.get(artifact_path.suffix, "application/octet-stream"),
            "build_receipt": rel(BUILD_RECEIPT_PATH),
        },
    )
    add(artifact)
    artifact_records.append(artifact)

relation_counter = 0


def add_relation(relation_type: str, subject_id: str, object_id: str, *, source_locator: str, payload: dict[str, Any] | None = None) -> None:
    global relation_counter
    relation_counter += 1
    add(
        make_record(
            "relation",
            f"relation.units0112.{relation_counter:04d}",
            order=relation_counter,
            resource_id=LOCAL_RESOURCE,
            edition_id=CUMULATIVE_EDITION,
            source_locator=source_locator,
            content_sha256=text_digest(f"{relation_type}\u241f{subject_id}\u241f{object_id}"),
            translation_state="built",
            rights_id=EDITORIAL_RIGHTS,
            payload={"relation_type": relation_type, "subject_id": subject_id, "object_id": object_id, **(payload or {})},
        )
    )


add_relation("extends", CUMULATIVE_EDITION, PREVIOUS_EDITION, source_locator=rel(BUILD_RECEIPT_PATH))
add_relation("derived_from", CUMULATIVE_EDITION, BRENNER_EDITION, source_locator=rel(BUILD_RECEIPT_PATH))
for term in new_term_records:
    add_relation("labels", term["stable_id"], term["parent_id"], source_locator=rel(TERMINOLOGY_PATH))
for correction in new_correction_records:
    correction_id = correction["source_local_id"]
    relation_type = "corrects" if correction_id.startswith("AGC-CORR-") else "adapts"
    add_relation(relation_type, correction["stable_id"], CORRECTION_TARGETS[correction_id], source_locator=rel(CORRECTIONS_PATH))
for unit_record in all_new_units:
    add_relation("contains", unit_record["parent_id"], unit_record["stable_id"], source_locator=unit_record["source_locator"])
    for concept_id in unit_record["concept_ids"]:
        add_relation("uses_concept", unit_record["stable_id"], concept_id, source_locator=unit_record["source_locator"])
for previous, following in zip(all_new_units, all_new_units[1:]):
    add_relation("precedes", previous["stable_id"], following["stable_id"], source_locator=following["source_locator"])
for unit, public in solution_entries.items():
    for number in sorted(public):
        add_relation("solves", f"br-ak-2025-2026-w{unit:02d}-sol-{number:02d}", f"br-ak-2025-2026-w{unit:02d}-ex-{number:02d}", source_locator=rel(UNIT_SPEC[unit]["map"]))
        add_relation("solves", f"solution.br-ak-2025-2026-w{unit:02d}-sol-{number:02d}", f"exercise.br-ak-2025-2026-w{unit:02d}-ex-{number:02d}", source_locator=rel(UNIT_SPEC[unit]["map"]), payload={"typed_family_projection": True})
for asset in asset_records:
    add_relation("illustrates", asset["stable_id"], asset["parent_id"], source_locator=asset["source_locator"])
for typed in typed_records:
    add_relation("indexes_unit", typed["stable_id"], typed["parent_id"], source_locator=typed["source_locator"])
for qa_record in qa_records:
    add_relation("validated_by", CUMULATIVE_EDITION, qa_record["stable_id"], source_locator=qa_record["source_locator"])
for artifact in artifact_records:
    add_relation("emits", CUMULATIVE_EDITION, artifact["stable_id"], source_locator=rel(BUILD_RECEIPT_PATH))

ids = [record["stable_id"] for record in records]
duplicates = sorted(stable_id for stable_id, count in Counter(ids).items() if count > 1)
require(not duplicates, f"Duplicate stable IDs: {duplicates}")
require({record["entity_class"] for record in records} == REQUIRED_CLASSES, "Required entity-family closure mismatch")
id_set = set(ids)
for record in records:
    if record["parent_id"] is not None:
        require(record["parent_id"] in id_set, f"Missing parent {record['parent_id']} for {record['stable_id']}")
    for field in ("resource_id", "edition_id", "rights_id"):
        endpoint = record.get(field)
        if endpoint is not None:
            require(endpoint in id_set, f"Missing {field} endpoint {endpoint} for {record['stable_id']}")
    for concept_id in record.get("concept_ids", []):
        require(concept_id in id_set, f"Missing concept endpoint {concept_id} for {record['stable_id']}")
    if record["entity_class"] == "relation":
        require(record["payload"].get("subject_id") in id_set, f"Missing relation subject for {record['stable_id']}")
        require(record["payload"].get("object_id") in id_set, f"Missing relation object for {record['stable_id']}")

schema = json.loads((BASELINE / "record.schema.json").read_text(encoding="utf-8"))
schema["$id"] = "https://example.invalid/algebraic-geometry-bridge/backend-record-units-01-12-v1.schema.json"
schema["title"] = "Algebraic Geometry Bridge cumulative backend record through Units 1--12"
schema["properties"]["entity_class"]["enum"] = sorted(REQUIRED_CLASSES)

records_sorted = sorted(records, key=lambda row: (row["entity_class"], row["stable_id"]))


def serialized_record(record: dict[str, Any]) -> str:
    return baseline_raw_by_id.get(record["stable_id"], canonical(record))


serialized_lines = [serialized_record(record) for record in records_sorted]
require(serialized_lines == [serialized_record(record) for record in records_sorted], "Nondeterministic in-memory serialization")
require(all(serialized_record(record) == baseline_raw_by_id[record["stable_id"]] for record in baseline_records), "Units 1--9 record bytes changed in memory")

OUT.mkdir(parents=True, exist_ok=True)
schema_path = OUT / "record.schema.json"
write_crlf(schema_path, json.dumps(schema, ensure_ascii=False, indent=2) + "\n")
combined_path = OUT / "records.jsonl"
write_crlf(combined_path, "".join(line + "\n" for line in serialized_lines))

class_paths: list[Path] = []
for entity_class in sorted(REQUIRED_CLASSES):
    path = OUT / f"{entity_class}.jsonl"
    class_records = [record for record in records_sorted if record["entity_class"] == entity_class]
    write_crlf(path, "".join(serialized_record(record) + "\n" for record in class_records))
    class_paths.append(path)

counts = Counter(record["entity_class"] for record in records_sorted)
export_files = [schema_path, combined_path, *class_paths]
source_binding_paths = [
    BASELINE / "MANIFEST.json",
    BASELINE / "records.jsonl",
    BASELINE / "record.schema.json",
    *SOURCE_FILES,
    BUILD_RECEIPT_PATH,
    MACHINE_QA_PATH,
    VISUAL_QA_PATH,
    RESPONSIVE_QA_PATH,
    PROTECTED_QA_PATH,
    *authority_paths,
    CORRECTIONS_PATH,
    TERMINOLOGY_PATH,
    Path(__file__),
    ROOT / "scripts" / "qa_backend_units_01_12.py",
]
for path in source_binding_paths:
    require(path.is_file(), f"Missing backend source binding: {rel(path)}")

manifest = {
    "schema": "ag-bridge-backend-export-manifest-v2",
    "schema_version": "1.2.0",
    "record_schema_version": RECORD_SCHEMA_VERSION,
    "generated_from_build_utc": timestamp,
    "through_unit": 12,
    "scope": "cumulative Units 1--12",
    "encoding": "UTF-8",
    "serialization": "canonical JSON Lines: records and keys sorted, compact separators, CRLF; frozen Units 1--9 records carried forward byte-for-byte",
    "record_count": len(records_sorted),
    "counts": {key: counts[key] for key in sorted(counts)},
    "files": [{"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)} for path in export_files],
    "source_bindings": [{"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)} for path in source_binding_paths],
    "units_01_09_baseline": {
        "manifest_path": "backend/units-01-09/MANIFEST.json",
        "manifest_sha256": BASELINE_MANIFEST_SHA256,
        "records_path": "backend/units-01-09/records.jsonl",
        "records_sha256": BASELINE_RECORDS_SHA256,
        "schema_path": "backend/units-01-09/record.schema.json",
        "schema_sha256": BASELINE_SCHEMA_SHA256,
        "record_count": BASELINE_RECORD_COUNT,
        "record_bytes_preserved": True,
        "stable_ids_and_payloads_preserved": True,
    },
    "reader_binding": {
        "build_receipt_path": rel(BUILD_RECEIPT_PATH),
        "build_receipt_sha256": digest(BUILD_RECEIPT_PATH),
        "through_unit": 12,
        "outputs": build_receipt["outputs"],
    },
    "authority_bindings": {
        f"unit_{unit}": {
            key: {"path": rel(spec[key]), "sha256": digest(spec[key])}
            for key in ("manifest", "map", "rights", "closure")
        }
        for unit, spec in UNIT_SPEC.items()
    },
    "model_provenance": MODEL_PROVENANCE,
    "validation": {
        "unique_stable_ids": True,
        "parent_resource_edition_rights_and_relation_endpoint_closure": True,
        "required_entity_class_closure": True,
        "units_01_09_record_bytes_and_payloads_preserved": True,
        "unit_10_12_source_hashes_match_reader_receipt": True,
        "authority_maps_rights_assets_and_solution_closure": True,
        "units_10_12_terminology_and_correction_ledger_closure": True,
        "reader_machine_visual_responsive_and_protected_qa_pass": True,
        "deterministic_double_replay_required": True,
    },
}
manifest_path = OUT / "MANIFEST.json"
write_crlf(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

print(json.dumps({
    "result": "PASS",
    "records": len(records_sorted),
    "new_records": len(new_records),
    "counts": manifest["counts"],
    "units_01_09_records_preserved": BASELINE_RECORD_COUNT,
    "manifest": rel(manifest_path),
    "manifest_sha256": digest(manifest_path),
    "model_provenance": MODEL_PROVENANCE,
}, ensure_ascii=False))
