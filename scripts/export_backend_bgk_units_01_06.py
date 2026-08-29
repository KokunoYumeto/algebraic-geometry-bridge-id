#!/usr/bin/env python3
"""Export the append-only native BGK backend through Units 1--6.

The accepted Units 1--4 backend is an immutable byte prefix. Units 5 and 6
are derived only from their frozen authority, verified Indonesian sources,
the cumulative reader receipt/QA, and admitted terminology/correction ledgers.
The BGK namespace remains disjoint from the classical-curve backend.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "backend" / "bgk-units-01-04"
OUT = ROOT / "backend" / "bgk-units-01-06"
BASE_MANIFEST = BASE / "MANIFEST.json"
BASE_RECORDS = BASE / "records.jsonl"
BASE_QA = ROOT / "qa" / "BGK_UNITS_01_04_BACKEND_QA.json"
BASE_MANIFEST_SHA256 = "a72b3b274fa1fc1d21459b8de9e76c4c0d4cb949c14eb09df62bef9f9c3ac357"
BASE_RECORDS_SHA256 = "f72ec15d7d036df7272d043968b888a61cffae8475ef8ce7206dbf1bcb3aeb04"
BASE_QA_SHA256 = "3473c17b988669337d4dbdb9042689b4ea7e5350d931bce32d08d0baae0cc7ef"

SCHEMA_NAME = "ag-bridge-backend-record"
SCHEMA_VERSION = "1.0.0"
WORKFLOW_ID = "workflow.o016-d100.algebraic-geometry-bridge-id"
COURSE_ID = "course.o016-d100.bgk-bridge"
SOURCE_RESOURCE = "resource.brenner.bgk.wikiversity.2019-2020"
LOCAL_RESOURCE = "resource.bgk-id.editorial-layer"
SEMANTIC_RIGHTS = "rights.bgk-semantic-text.cc-by-sa-4.0"
EDITORIAL_RIGHTS = "rights.bgk-id.derivative.cc-by-sa-4.0"
MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."
DERIVATIVE_EDITION = "edition.bgk-id.units-01-06.2026-08-29"

SOURCE_DIR = ROOT / "source" / "id-ID" / "bgk"
FRONTMATTER = SOURCE_DIR / "frontmatter-bgk-units-01-06.md"
COURSE_MANIFEST = ROOT / "authority" / "wikiversity-bgk" / "course" / "COURSE_AUTHORITY_MANIFEST.json"
TERMINOLOGY = ROOT / "00_control" / "TERMINOLOGY.csv"
CORRECTIONS = ROOT / "00_control" / "CORRECTIONS.csv"
READER_QA = ROOT / "qa" / "BGK_UNITS_01_06_READER_QA.json"
READER_RECEIPT = ROOT / "build" / "reader-bgk-id" / "BUILD_RECEIPT.json"
READER_HTML = ROOT / "build" / "reader-bgk-id" / "index.html"
READER_PDF = ROOT / "build" / "reader-bgk-id" / "bundel-berkas-dan-kohomologi-id-units-01-06.pdf"
CLASSICAL_RECORDS = ROOT / "backend" / "units-01-30" / "records.jsonl"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


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


def canonical(record: dict[str, Any]) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def jsonl_bytes(rows: list[dict[str, Any]]) -> bytes:
    return "".join(canonical(row) + "\r\n" for row in rows).encode("utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def unique_paths(paths: list[Path]) -> list[Path]:
    result: list[Path] = []
    for path in paths:
        if path not in result:
            result.append(path)
    return result


UNIT: dict[int, dict[str, Any]] = {}
for number in (5, 6):
    unit_dir = ROOT / "authority" / "wikiversity-bgk" / f"unit-{number:02d}"
    UNIT[number] = {
        "dir": unit_dir,
        "manifest": unit_dir / "UNIT_AUTHORITY_MANIFEST.json",
        "exercise_map": unit_dir / "ORDERED_EXERCISE_MAP.json",
        "candidates": unit_dir / "worksheet-solution-candidates-api.json",
        "pdf_api": unit_dir / "official-pdfs-api.json",
        "authority_freeze": ROOT / "authority" / f"BGK_UNIT_{number:02d}_AUTHORITY_FREEZE.md",
        "authority_qa": ROOT / "qa" / f"BGK_UNIT_{number:02d}_AUTHORITY_QA.json",
        "translation_qa": ROOT / "qa" / f"BGK_UNIT_{number:02d}_TRANSLATION_QA.json",
        "rights": ROOT / "authority" / f"RIGHTS-bgk-unit-{number:02d}.csv",
        "closure": ROOT / "authority" / f"ASSET_CLOSURE-bgk-unit-{number:02d}.json",
        "commons": ROOT / "authority" / f"commons-imageinfo-bgk-unit-{number:02d}.json",
        "credits": ROOT / "source" / "id-ID" / f"media-credits-bgk-unit-{number:02d}.md",
        "lecture_pdf": ROOT / "authority" / "artifacts" / f"bgk-lecture-{number:02d}-official.pdf",
        "worksheet_pdf": ROOT / "authority" / "artifacts" / f"bgk-worksheet-{number:02d}-official.pdf",
        "sources": [
            SOURCE_DIR / f"lecture-{number:02d}.md",
            SOURCE_DIR / f"worksheet-{number:02d}.md",
            SOURCE_DIR / f"worksheet-{number:02d}-solutions.md",
        ],
        "exercise_count": 11 if number == 5 else 19,
        "solution_count": 1 if number == 5 else 0,
        "source_edition": f"edition.brenner.bgk.unit-{number:02d}.freeze-2026-08-29",
        "pdf_resource": f"resource.brenner.bgk.unit-{number:02d}.official-pdf-witnesses",
        "pdf_rights": f"rights.bgk.u{number:02d}.official-pdf.component-notices-3.0-and-4.0",
    }


required_initial = [
    BASE_MANIFEST, BASE_RECORDS, BASE_QA, FRONTMATTER, COURSE_MANIFEST,
    TERMINOLOGY, CORRECTIONS, READER_QA, READER_RECEIPT, READER_HTML,
    READER_PDF, CLASSICAL_RECORDS,
]
for config in UNIT.values():
    required_initial.extend([
        config["manifest"], config["exercise_map"], config["candidates"], config["pdf_api"],
        config["authority_freeze"], config["authority_qa"], config["translation_qa"],
        config["rights"], config["closure"], config["commons"], config["credits"],
        config["lecture_pdf"], config["worksheet_pdf"], *config["sources"],
    ])
for required in unique_paths(required_initial):
    require(required.is_file(), f"Required cumulative BGK Units 1--6 backend input is absent: {rel(required)}")

require(digest(BASE_MANIFEST) == BASE_MANIFEST_SHA256, "Accepted Units 1--4 backend manifest drifted")
require(digest(BASE_RECORDS) == BASE_RECORDS_SHA256, "Accepted Units 1--4 records drifted")
require(digest(BASE_QA) == BASE_QA_SHA256, "Accepted Units 1--4 backend QA drifted")
base_manifest = read_json(BASE_MANIFEST)
require(base_manifest.get("through_unit") == 4 and base_manifest.get("record_count") == 2919,
        "Accepted Units 1--4 backend scope drifted")
for binding in base_manifest["files"]:
    path = ROOT / binding["path"]
    require(path.is_file() and path.stat().st_size == binding["bytes"] and digest(path) == binding["sha256"],
            f"Accepted Units 1--4 projection drifted: {binding['path']}")

base_records = read_jsonl(BASE_RECORDS)
base_ids = {row["stable_id"] for row in base_records}
require(len(base_records) == len(base_ids) == 2919, "Accepted Units 1--4 stable-ID closure drifted")
base_schema = read_json(BASE / "record.schema.json")
ENTITY_CLASSES = list(base_schema["properties"]["entity_class"]["enum"])

reader_qa = read_json(READER_QA)
reader_receipt = read_json(READER_RECEIPT)
require(str(reader_qa.get("status", "")).startswith("PASS") and reader_qa.get("through_unit") == 6,
        "BGK cumulative Units 1--6 reader QA is not PASS")
require(reader_qa.get("model_provenance") == MODEL_PROVENANCE,
        "BGK Units 1--6 reader QA lacks exact model provenance")
require(reader_receipt.get("through_unit") == 6, "BGK Units 1--6 build receipt scope drifted")
receipt_outputs = {row["path"]: row for row in reader_receipt.get("outputs", [])}
for path in (READER_HTML, READER_PDF):
    binding = receipt_outputs.get(rel(path))
    require(binding is not None and path.stat().st_size == binding["bytes"] and digest(path) == binding["sha256"],
            f"BGK reader build-receipt output drifted: {rel(path)}")
require(reader_qa["html"]["sha256"] == digest(READER_HTML) and
        reader_qa["pdf"]["sha256"] == digest(READER_PDF),
        "BGK reader QA hashes do not bind the current cumulative outputs")

for number, config in UNIT.items():
    manifest = read_json(config["manifest"])
    exercise_map = read_json(config["exercise_map"])
    authority_qa = read_json(config["authority_qa"])
    translation_qa = read_json(config["translation_qa"])
    closure = read_json(config["closure"])
    require(manifest.get("unit_number") == number, f"BGK Unit {number} authority identity mismatch")
    require(exercise_map.get("unit") == number and
            exercise_map.get("exercise_count") == config["exercise_count"] and
            exercise_map.get("solution_count") == config["solution_count"],
            f"BGK Unit {number} exercise/solution topology drifted")
    public = [row for row in exercise_map["entries"] if row.get("has_public_solution")]
    require(len(public) == config["solution_count"], f"BGK Unit {number} public-solution map drifted")
    if number == 5:
        require(int(public[0]["exercise_number"]) == 5,
                "BGK Unit 5 public solution must be exactly Exercise 5.5")
    require(str(authority_qa.get("status", "")).startswith("PASS"),
            f"BGK Unit {number} authority QA is not PASS")
    require(translation_qa.get("status") == "PASS",
            f"BGK Unit {number} translation QA is not PASS")
    require(translation_qa.get("model_provenance", MODEL_PROVENANCE) == MODEL_PROVENANCE,
            f"BGK Unit {number} translation QA model provenance drifted")
    require(closure.get("unit") == number and closure.get("reader_media_positions") == 0 and
            closure.get("unique_local_assets") == 0 and closure.get("assets") == [],
            f"BGK Unit {number} must retain its verified zero-reader-media closure")
    for section in ("authority", "media_and_rights", "translation_files"):
        for binding in translation_qa.get(section, []):
            path = ROOT / binding["path"]
            require(path.is_file() and path.stat().st_size == binding["bytes"] and digest(path) == binding["sha256"],
                    f"BGK Unit {number} translation-QA binding drifted: {binding['path']}")

TIMESTAMP = read_json(UNIT[6]["manifest"])["frozen_utc"]


def record_schema() -> dict[str, Any]:
    schema = json.loads(json.dumps(base_schema))
    schema["$id"] = "https://example.invalid/algebraic-geometry-bridge/bgk-backend-record-units-01-06-v1.schema.json"
    schema["title"] = "BGK Indonesian native backend record through Units 1--6"
    return schema


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
    require(entity_class in ENTITY_CLASSES, f"Unsupported entity class: {entity_class}")
    actual_provenance = dict(provenance or {})
    actual_provenance["model"] = MODEL_PROVENANCE
    return {
        "schema": SCHEMA_NAME,
        "schema_version": SCHEMA_VERSION,
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
        "provenance": actual_provenance,
        "concept_ids": sorted(set(concept_ids or [])),
        "prerequisite_ids": sorted(set(prerequisite_ids or [])),
        "rights_id": rights_id,
        "status": status,
        "timestamp": TIMESTAMP,
        "responsible_workflow": WORKFLOW_ID,
        "supersedes": supersedes,
        "payload": payload or {},
    }


new_records: list[dict[str, Any]] = []
new_ids: set[str] = set()


def add(row: dict[str, Any]) -> None:
    require(row["stable_id"] not in base_ids, f"Units 5--6 attempt to mutate Units 1--4 ID: {row['stable_id']}")
    require(row["stable_id"] not in new_ids, f"Duplicate Units 5--6 stable ID: {row['stable_id']}")
    new_ids.add(row["stable_id"])
    new_records.append(row)


add(make_record(
    "edition", DERIVATIVE_EDITION, source_local_id="bgk-id-units-01-06",
    parent_id=LOCAL_RESOURCE, resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION,
    source_locator=rel(FRONTMATTER), content_sha256=digest(FRONTMATTER), language="id-ID",
    translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
    payload={
        "through_unit": 6,
        "source_editions": [f"edition.brenner.bgk.unit-{unit:02d}.freeze-2026-08-28" for unit in range(1, 4)] +
                           ["edition.brenner.bgk.unit-04.freeze-2026-08-29"] +
                           [UNIT[5]["source_edition"], UNIT[6]["source_edition"]],
        "status": "complete source translation and verified cumulative reader; cumulative native backend",
        "model_provenance": MODEL_PROVENANCE,
        "units_01_04_records_immutable": True,
    },
))

unit_manifests: dict[int, dict[str, Any]] = {}
exercise_maps: dict[int, dict[str, Any]] = {}
authority_qas: dict[int, dict[str, Any]] = {}
translation_qas: dict[int, dict[str, Any]] = {}
for number, config in UNIT.items():
    unit_manifests[number] = read_json(config["manifest"])
    exercise_maps[number] = read_json(config["exercise_map"])
    authority_qas[number] = read_json(config["authority_qa"])
    translation_qas[number] = read_json(config["translation_qa"])
    closure = read_json(config["closure"])
    add(make_record(
        "resource", config["pdf_resource"], source_local_id=f"bgk-unit-{number:02d}-official-pdf-witnesses",
        parent_id=COURSE_ID, source_locator=rel(config["closure"]), content_sha256=digest(config["closure"]),
        language="de", rights_id=config["pdf_rights"],
        payload={"unit": number, "role": "visual and numbering witnesses, not semantic authority",
                 "component_notice_discrepancy_preserved": True, "reader_media_positions": 0},
    ))
    add(make_record(
        "edition", config["source_edition"], source_local_id=f"bgk-unit-{number:02d}-authority-freeze",
        parent_id=SOURCE_RESOURCE, resource_id=SOURCE_RESOURCE, edition_id=config["source_edition"],
        source_locator=rel(config["manifest"]), content_sha256=digest(config["manifest"]),
        language="de", rights_id=SEMANTIC_RIGHTS,
        payload={"unit": number,
                 "lecture_pageid": unit_manifests[number]["lecture"]["pageid"],
                 "lecture_revid": unit_manifests[number]["lecture"]["revid"],
                 "worksheet_pageid": unit_manifests[number]["worksheet"]["pageid"],
                 "worksheet_revid": unit_manifests[number]["worksheet"]["revid"],
                 "exercise_count": config["exercise_count"],
                 "public_solution_count": config["solution_count"],
                 "reader_media_positions": 0},
    ))
    pdf_notices = closure["official_pdf_component_rights"]
    require(len(pdf_notices) == 2, f"BGK Unit {number} PDF rights closure must contain two witnesses")
    add(make_record(
        "rights", config["pdf_rights"], parent_id=config["pdf_resource"],
        resource_id=config["pdf_resource"], edition_id=DERIVATIVE_EDITION,
        source_locator=rel(config["authority_qa"]), content_sha256=digest(config["authority_qa"]),
        rights_id=config["pdf_rights"],
        payload={"title": f"Unit {number} official PDF witness notices",
                 "license": "component notices preserved", "current_commons_metadata": "CC BY-SA 4.0",
                 "embedded_pdf_notice": "CC-by-sa 3.0", "blanket_relicensing_claim": False,
                 "witnesses": pdf_notices},
    ))


CONCEPT_SPECS: dict[int, dict[str, tuple[str, list[str]]]] = {
    5: {
        "sheafification": ("berkasisasi", ["berkasisasi"]),
        "compatibility-condition": ("syarat kompatibilitas", ["syarat kompatibilitas"]),
        "subsheaf": ("subberkas", ["subberkas"]),
        "kernel-sheaf": ("berkas kernel", ["berkas kernel"]),
        "image-sheaf": ("berkas citra", ["berkas citra"]),
        "quotient-sheaf": ("berkas hasil bagi", ["berkas hasil bagi"]),
        "locally-constant-sheaf": ("berkas konstan lokal", ["berkas konstan lokal"]),
        "zero-sheaf": ("berkas nol", ["berkas nol"]),
        "common-refinement": ("penghalusan bersama", ["penghalusan bersama"]),
        "abelian-group-sheaf-homomorphism": ("homomorfisme berkas grup komutatif", ["homomorfisme berkas grup komutatif"]),
    },
    6: {
        "sheaf-sequence": ("barisan berkas", ["barisan berkas"]),
        "exact-sequence": ("barisan eksak", ["barisan eksak"]),
        "covering-map": ("pemetaan ruang penutup", ["pemetaan ruang penutup", "ruang penutup"]),
        "left-exact-functor": ("funktor eksak-kiri", ["funktor eksak-kiri"]),
        "global-evaluation": ("evaluasi global", ["evaluasi global"]),
        "direct-image": ("dorong maju", ["dorong maju"]),
        "inverse-image": ("tarik balik", ["tarik balik"]),
        "topological-group-sheaf-sequence": ("barisan berkas grup topologis", ["barisan berkas grup topologis"]),
        "continuous-section": ("seksi kontinu", ["seksi kontinu"]),
        "fiber-product": ("produk serat", ["produk serat"]),
    },
}
TERM_TO_CONCEPT = {
    **{f"AGT-{n:04d}": key for n, key in zip(range(324, 334), CONCEPT_SPECS[5])},
    **{f"AGT-{n:04d}": key for n, key in zip(range(334, 344), CONCEPT_SPECS[6])},
}
concept_keywords: dict[str, list[str]] = {
    row["stable_id"]: list(row["payload"].get("matching_keywords", []))
    for row in base_records if row["entity_class"] == "concept"
}
concept_order = 1 + sum(row["entity_class"] == "concept" for row in base_records)
for number in (5, 6):
    for key, (label, keywords) in CONCEPT_SPECS[number].items():
        concept_id = f"concept.br-bgk-2019.{key}"
        require(concept_id not in base_ids, f"New concept unexpectedly exists in Units 1--4: {concept_id}")
        add(make_record(
            "concept", concept_id, source_local_id=key, parent_id=COURSE_ID, order=concept_order,
            resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION, language="id-ID",
            translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
            payload={"preferred_label": label, "matching_keywords": keywords, "introduced_in_unit": number},
        ))
        concept_keywords[concept_id] = keywords
        concept_order += 1


def concepts_for(text: str) -> list[str]:
    lowered = text.casefold()
    return sorted(concept_id for concept_id, keywords in concept_keywords.items()
                  if any(keyword.casefold() in lowered for keyword in keywords))


with TERMINOLOGY.open("r", encoding="utf-8-sig", newline="") as stream:
    all_terms = [{key: value for key, value in row.items() if key is not None}
                 for row in csv.DictReader(stream)]
base_term_ids = {row["source_local_id"] for row in base_records if row["entity_class"] == "term"}
unit_term_ids: dict[int, set[str]] = {}
for number in (5, 6):
    qa = translation_qas[number]
    referenced = set(qa.get("terminology_ids_added", []) + qa.get("terminology_ids_reused", []))
    expected = {f"AGT-{n:04d}" for n in (range(324, 334) if number == 5 else range(334, 344))}
    require(referenced == expected, f"BGK Unit {number} terminology-QA identity drifted")
    unit_term_ids[number] = referenced
for order, term_id in enumerate(sorted(unit_term_ids[5] | unit_term_ids[6]), start=1):
    require(term_id not in base_term_ids, f"Units 5--6 terminology unexpectedly duplicates baseline: {term_id}")
    matches = [row for row in all_terms if row.get("term_id") == term_id and row.get("status") == "admitted"]
    require(len(matches) == 1, f"Admitted terminology row missing or duplicated: {term_id}")
    row = matches[0]
    unit_number = 5 if term_id in unit_term_ids[5] else 6
    concept_id = f"concept.br-bgk-2019.{TERM_TO_CONCEPT[term_id]}"
    add(make_record(
        "term", f"term.br-bgk-2019.{term_id.casefold()}", source_local_id=term_id,
        parent_id=concept_id, order=order, resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION,
        source_locator=f"{rel(TERMINOLOGY)}#{term_id}", content_sha256=text_digest(canonical(row)),
        language="id-ID", translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
        concept_ids=[concept_id],
        payload={"ledger_row": row, "scope": f"BGK Unit {unit_number}", "translation_qa_role": "added"},
    ))


heading_re = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]+\{#([^}]+)\}[ \t]*$", re.MULTILINE)
yaml_id_re = re.compile(r"^stable_id:[ \t]*['\"]?([^'\"\r\n]+)", re.MULTILINE)
source_heading_ids: dict[int, list[str]] = {5: [], 6: []}
frontmatter_heading_ids: list[str] = []


def split_frontmatter(text: str) -> tuple[str, str]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return "", normalized
    end = normalized.find("\n---\n", 4)
    require(end >= 0, "Unclosed source front matter")
    return normalized[4:end], normalized[end + 5:]


def block_kind(block: str) -> str:
    stripped = block.strip()
    if stripped.startswith("$$") and stripped.endswith("$$"):
        return "display_math"
    if stripped.startswith("```{=latex}"):
        return "raw_latex"
    if "![" in stripped and "](" in stripped:
        return "image"
    if stripped.startswith("<!--"):
        return "source_comment"
    if stripped.startswith(">"):
        return "blockquote"
    if re.match(r"^(?:[-*+] |\d+\. )", stripped):
        return "list"
    return "paragraph"


source_plan: list[tuple[int, Path]] = [(6, FRONTMATTER)]
source_plan.extend((5, path) for path in UNIT[5]["sources"])
source_plan.extend((6, path) for path in UNIT[6]["sources"])
for document_order, (number, path) in enumerate(source_plan, start=1):
    text = path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)
    headings = list(heading_re.finditer(body))
    require(headings, f"No stable headings found in {rel(path)}")
    yaml_match = yaml_id_re.search(frontmatter)
    if yaml_match:
        require(yaml_match.group(1).strip() == headings[0].group(3),
                f"YAML/top-heading stable-ID mismatch in {rel(path)}")
    stack: list[tuple[int, str]] = []
    exercise_by_number = {int(row["exercise_number"]): row for row in exercise_maps[number]["entries"]}
    for heading_index, match in enumerate(headings):
        level = len(match.group(1))
        title = match.group(2).strip()
        stable_id = match.group(3).strip()
        require(stable_id.startswith("br-bgk-2019-"), f"Non-BGK stable heading ID: {stable_id}")
        require(stable_id not in base_ids and stable_id not in new_ids,
                f"Duplicate or prior-unit BGK source heading ID: {stable_id}")
        if path == FRONTMATTER:
            frontmatter_heading_ids.append(stable_id)
        else:
            source_heading_ids[number].append(stable_id)
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent_id = stack[-1][1] if stack else DERIVATIVE_EDITION
        stack.append((level, stable_id))
        local_end = headings[heading_index + 1].start() if heading_index + 1 < len(headings) else len(body)
        local_markdown = body[match.start():local_end].strip() + "\n"
        local_body = body[match.end():local_end].strip()
        exercise_match = re.search(r"-ex(\d{2})$", stable_id)
        solution_match = re.search(r"-ex(\d{2})-solution$", stable_id)
        if level == 1:
            entity_class = "unit"
        elif exercise_match:
            entity_class = "exercise"
        elif solution_match:
            entity_class = "solution"
            parent_id = stable_id.rsplit("-solution", 1)[0]
        else:
            entity_class = "segment"
        payload: dict[str, Any] = {
            "title": title,
            "heading_level": level,
            "document_order": document_order,
            "local_markdown": local_markdown,
            "inline_math_delimiter_count": len(re.findall(r"(?<!\$)\$(?!\$)", local_markdown)),
            "display_math_block_count": len(re.findall(r"\$\$(.*?)\$\$", local_markdown, re.DOTALL)),
        }
        if exercise_match:
            exercise_number = int(exercise_match.group(1))
            mapped = exercise_by_number.get(exercise_number)
            require(mapped is not None, f"Exercise {number}.{exercise_number} absent from frozen map")
            payload.update({"exercise_number": exercise_number,
                            "source_entity": mapped["exercise_title"],
                            "source_solution_title": mapped["solution_title"],
                            "has_public_solution": mapped["has_public_solution"],
                            "prompt_markdown": local_body})
        if solution_match:
            solution_number = int(solution_match.group(1))
            mapped = exercise_by_number.get(solution_number)
            require(number == 5 and solution_number == 5 and mapped and mapped["has_public_solution"],
                    "Translated BGK solution is not exact public Exercise 5.5")
            payload.update({"exercise_number": solution_number, "exercise_id": parent_id,
                            "source_solution_title": mapped["solution_title"],
                            "source_pageid": mapped["pageid"], "source_revid": mapped["revid"],
                            "source_mediawiki_sha1": mapped["mediawiki_sha1"],
                            "solution_markdown": local_body, "invented": False})
        source_edition = UNIT[number]["source_edition"] if path != FRONTMATTER else None
        add(make_record(
            entity_class, stable_id, source_local_id=stable_id, parent_id=parent_id,
            order=heading_index + 1, path=rel(path), resource_id=LOCAL_RESOURCE,
            edition_id=DERIVATIVE_EDITION, source_locator=f"{rel(path)}#{stable_id}",
            content_sha256=text_digest(local_markdown), language="id-ID",
            translation_state="structurally_verified",
            provenance={"source_edition": source_edition, "source_file_sha256": digest(path)},
            concept_ids=concepts_for(title + "\n" + local_body), rights_id=EDITORIAL_RIGHTS,
            payload=payload,
        ))
        if not local_body:
            continue
        blocks = [block.strip() for block in re.split(r"\n[ \t]*\n", local_body) if block.strip()]
        for block_index, block in enumerate(blocks, start=1):
            block_id = f"{stable_id}-b{block_index:03d}"
            kind = block_kind(block)
            require(kind != "image", f"Units 5--6 have zero-media closure but image Markdown appears: {block_id}")
            add(make_record(
                "segment", block_id, source_local_id=block_id, parent_id=stable_id,
                order=block_index, path=rel(path), resource_id=LOCAL_RESOURCE,
                edition_id=DERIVATIVE_EDITION,
                source_locator=f"{rel(path)}#{stable_id}:block-{block_index}",
                content_sha256=text_digest(block + "\n"), language="id-ID",
                translation_state="structurally_verified",
                provenance={"source_file_sha256": digest(path)}, concept_ids=concepts_for(block),
                rights_id=EDITORIAL_RIGHTS,
                payload={"kind": kind, "markdown": block + "\n",
                         "display_math_count": len(re.findall(r"\$\$(.*?)\$\$", block, re.DOTALL)),
                         "inline_math_delimiter_count": len(re.findall(r"(?<!\$)\$(?!\$)", block))},
            ))

require(len(frontmatter_heading_ids) == 2, "Cumulative Units 1--6 frontmatter must expose exactly two stable headings")
require(len(source_heading_ids[5]) == 29, "BGK Unit 5 source-heading closure must contain exactly 29 IDs")
require(len(source_heading_ids[6]) == 45, "BGK Unit 6 source-heading closure must contain exactly 45 IDs")
for number, count in ((5, 11), (6, 19)):
    expected = {f"br-bgk-2019-w{number:02d}-ex{exercise:02d}" for exercise in range(1, count + 1)}
    actual = {row["stable_id"] for row in new_records if row["entity_class"] == "exercise" and
              row["stable_id"].startswith(f"br-bgk-2019-w{number:02d}-")}
    require(actual == expected, f"BGK Unit {number} translated exercise-ID closure drifted")
solutions = {row["stable_id"] for row in new_records if row["entity_class"] == "solution"}
require(solutions == {"br-bgk-2019-w05-ex05-solution"},
        "Units 5--6 must append exactly the frozen public solution for Exercise 5.5")

with CORRECTIONS.open("r", encoding="utf-8-sig", newline="") as stream:
    all_corrections = [{key: value for key, value in row.items() if key is not None}
                       for row in csv.DictReader(stream)]
CORRECTION_SURFACES = {
    "AGC-CORR-0159": ["br-bgk-2019-l05-def-01"],
    "AGC-CORR-0160": ["br-bgk-2019-l05-exa-02"],
    "AGC-CORR-0161": ["br-bgk-2019-l05-exa-02"],
    "AGC-CORR-0162": ["br-bgk-2019-l05-lem-02-proof"],
    "AGC-CORR-0163": ["br-bgk-2019-w05-ex05-solution"],
    "AGC-CORR-0164": ["br-bgk-2019-l05-lem-01-proof"],
    "AGC-CORR-0165": ["br-bgk-2019-w06-ex06"],
    "AGC-CORR-0166": ["br-bgk-2019-w06-ex14", "br-bgk-2019-w06-ex15"],
    "AGC-CORR-0167": ["br-bgk-2019-w06-ex15"],
    "AGC-CORR-0168": ["br-bgk-2019-l06-exa-01"],
    "AGC-CORR-0169": ["br-bgk-2019-l06-lem-05-proof"],
}
for number, expected_range in ((5, range(159, 165)), (6, range(165, 170))):
    expected = {f"AGC-CORR-{value:04d}" for value in expected_range}
    require(set(translation_qas[number]["correction_ids"]) == expected,
            f"BGK Unit {number} correction-QA identity drifted")
    rows = [row for row in all_corrections if row.get("correction_id") in expected and
            row.get("status") == f"applied_at_bgk_unit_{number:02d}_translation"]
    rows.sort(key=lambda row: int(row["correction_id"].split("-")[-1]))
    require({row["correction_id"] for row in rows} == expected,
            f"BGK Unit {number} correction ledger closure is incomplete")
    for order, row in enumerate(rows, start=1):
        correction_id = row["correction_id"]
        surfaces = CORRECTION_SURFACES[correction_id]
        require(all(surface in new_ids for surface in surfaces), f"Missing correction surface: {correction_id}")
        add(make_record(
            "correction", f"correction.br-bgk-2019.u{number:02d}.{correction_id.split('-')[-1]}",
            source_local_id=correction_id, parent_id=surfaces[0], order=order,
            resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION,
            source_locator=f"{rel(CORRECTIONS)}#{correction_id}",
            content_sha256=text_digest(canonical(row)), language="id-ID",
            translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
            payload={"ledger_row": row, "source_issue": row["authority_observation"],
                     "adopted_reading": row["target_action"], "affected_surface_ids": surfaces,
                     "disclosed_in_reader": True, "silent_change": False},
        ))


artifact_paths_by_unit: dict[int, list[Path]] = {5: [], 6: []}
for number in (5, 6):
    qa = translation_qas[number]
    bound = [ROOT / row["path"] for section in ("authority", "media_and_rights", "translation_files")
             for row in qa.get(section, [])]
    bound.extend([UNIT[number]["authority_qa"], UNIT[number]["authority_freeze"]])
    artifact_paths_by_unit[number] = unique_paths(bound)
artifact_paths_by_unit[6].extend([
    FRONTMATTER, TERMINOLOGY, CORRECTIONS, READER_QA, READER_RECEIPT, READER_HTML, READER_PDF,
])
artifact_paths_by_unit[6] = unique_paths(artifact_paths_by_unit[6])
for number in (5, 6):
    for order, path in enumerate(artifact_paths_by_unit[number], start=1):
        require(path.is_file(), f"Bound BGK Unit {number} artifact is absent: {rel(path)}")
        suffix = path.suffix.casefold()
        media_type = {".md": "text/markdown", ".json": "application/json", ".csv": "text/csv",
                      ".pdf": "application/pdf", ".html": "text/html", ".xml": "application/xml",
                      ".tex": "text/x-tex"}.get(suffix, "application/octet-stream")
        if path in (UNIT[number]["lecture_pdf"], UNIT[number]["worksheet_pdf"]):
            rights_id = UNIT[number]["pdf_rights"]
        elif path in UNIT[number]["sources"] or path in (UNIT[number]["credits"],
                                                         UNIT[number]["translation_qa"],
                                                         FRONTMATTER, TERMINOLOGY, CORRECTIONS,
                                                         READER_QA, READER_RECEIPT, READER_HTML, READER_PDF):
            rights_id = EDITORIAL_RIGHTS
        else:
            rights_id = SEMANTIC_RIGHTS
        payload = {"bytes": path.stat().st_size, "media_type": media_type, "unit": number}
        if path in (READER_HTML, READER_PDF):
            payload["component_rights_ids"] = [EDITORIAL_RIGHTS]
        add(make_record(
            "artifact", f"artifact.br-bgk-2019.u{number:02d}.{order:03d}",
            source_local_id=path.name, parent_id=DERIVATIVE_EDITION, order=order,
            path=rel(path), resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION,
            source_locator=rel(path), content_sha256=digest(path),
            language="id-ID" if rights_id == EDITORIAL_RIGHTS else "und",
            translation_state="structurally_verified" if rights_id == EDITORIAL_RIGHTS else "source_frozen",
            rights_id=rights_id, payload=payload,
        ))

for number in (5, 6):
    qa_specs = [
        ("authority-closure", f"BGK_UNIT_{number:02d}_AUTHORITY_QA", UNIT[number]["authority_qa"],
         {"status": authority_qas[number]["status"], "exercise_count": UNIT[number]["exercise_count"],
          "public_solution_count": UNIT[number]["solution_count"]}),
        ("translation-closure", f"BGK_UNIT_{number:02d}_TRANSLATION_QA", UNIT[number]["translation_qa"],
         {"status": translation_qas[number]["status"], "qa_schema": translation_qas[number].get("schema"),
          "model_provenance": MODEL_PROVENANCE}),
        ("media-closure", f"ASSET_CLOSURE-bgk-unit-{number:02d}", UNIT[number]["closure"],
         {"reader_media_positions": 0, "primary_assets": 0, "pdf_companions": 0,
          "unique_local_assets": 0, "official_pdf_witnesses_are_not_media_positions": True}),
    ]
    if number == 6:
        qa_specs.append(
            ("reader-closure", "BGK_UNITS_01_06_READER_QA", READER_QA,
             {"status": reader_qa["status"], "through_unit": 6,
              "html_sha256": reader_qa["html"]["sha256"],
              "pdf_sha256": reader_qa["pdf"]["sha256"],
              "pdf_pages": reader_qa["pdf"]["pages_pypdf"]})
        )
    for order, (suffix, local_id, path, payload) in enumerate(qa_specs, start=1):
        add(make_record(
            "qa_event", f"qa.br-bgk-2019.u{number:02d}.{suffix}", source_local_id=local_id,
            parent_id=DERIVATIVE_EDITION, order=order, path=rel(path), resource_id=LOCAL_RESOURCE,
            edition_id=DERIVATIVE_EDITION, source_locator=rel(path), content_sha256=digest(path),
            language="id-ID" if suffix in ("translation-closure", "reader-closure") else "und",
            translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS, payload=payload,
        ))

# Append-only graph edges cover every new non-relation record.
non_relations = list(new_records)
for relation_order, row in enumerate((row for row in non_relations if row["parent_id"] is not None), start=1):
    add(make_record(
        "relation", f"relation.br-bgk-2019.u05-u06.{relation_order:05d}", parent_id=COURSE_ID,
        order=relation_order, resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION,
        content_sha256=text_digest(row["parent_id"] + "\ncontains\n" + row["stable_id"]),
        translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
        payload={"subject_id": row["parent_id"], "predicate": "contains", "object_id": row["stable_id"]},
    ))

records = base_records + new_records
ids = [row["stable_id"] for row in records]
require(len(ids) == len(set(ids)), "Duplicate cumulative BGK backend stable ID")
id_set = set(ids)
for row in records:
    require(row["parent_id"] is None or row["parent_id"] in id_set, f"Missing parent for {row['stable_id']}")
    require(row["rights_id"] is None or row["rights_id"] in id_set, f"Missing rights for {row['stable_id']}")
    require(all(concept_id in id_set for concept_id in row["concept_ids"]),
            f"Missing concept binding for {row['stable_id']}")
    if row["entity_class"] == "relation":
        require(row["payload"]["subject_id"] in id_set and row["payload"]["object_id"] in id_set,
                f"Missing relation endpoint for {row['stable_id']}")

classical_ids: set[str] = set()
with CLASSICAL_RECORDS.open("r", encoding="utf-8") as stream:
    for line in stream:
        if line.strip():
            classical_ids.add(json.loads(line)["stable_id"])
overlap = sorted(id_set & classical_ids)
require(not overlap, f"BGK/classical stable-ID collision: {overlap[:5]}")
require(new_records and all(row["provenance"].get("model") == MODEL_PROVENANCE for row in new_records),
        "One or more Units 5--6 records lack exact model provenance")

new_sorted = sorted(new_records, key=lambda row: (row["entity_class"], row["stable_id"]))
new_by_class: dict[str, list[dict[str, Any]]] = {entity_class: [] for entity_class in ENTITY_CLASSES}
for row in new_sorted:
    new_by_class[row["entity_class"]].append(row)

OUT.mkdir(parents=True, exist_ok=True)
schema_path = OUT / "record.schema.json"
schema_path.write_text(json.dumps(record_schema(), ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8", newline="\n")
(OUT / "records.jsonl").write_bytes(BASE_RECORDS.read_bytes() + jsonl_bytes(new_sorted))
for entity_class in ENTITY_CLASSES:
    (OUT / f"{entity_class}.jsonl").write_bytes(
        (BASE / f"{entity_class}.jsonl").read_bytes() + jsonl_bytes(new_by_class[entity_class]))

export_files = [schema_path, OUT / "records.jsonl", *[OUT / f"{name}.jsonl" for name in ENTITY_CLASSES]]
translation_bound_paths: list[Path] = []
for number in (5, 6):
    qa = translation_qas[number]
    translation_bound_paths.extend(ROOT / row["path"] for section in ("authority", "media_and_rights", "translation_files")
                                   for row in qa.get(section, []))
source_bindings = unique_paths([
    BASE_MANIFEST, BASE_QA, BASE / "record.schema.json", BASE_RECORDS,
    *[BASE / f"{name}.jsonl" for name in ENTITY_CLASSES],
    FRONTMATTER, COURSE_MANIFEST, TERMINOLOGY, CORRECTIONS, READER_QA,
    READER_RECEIPT, READER_HTML, READER_PDF, CLASSICAL_RECORDS,
    *translation_bound_paths,
    *[UNIT[number][name] for number in (5, 6) for name in
      ("manifest", "exercise_map", "candidates", "pdf_api", "authority_freeze",
       "authority_qa", "translation_qa", "rights", "closure", "commons", "credits",
       "lecture_pdf", "worksheet_pdf")],
    Path(__file__), ROOT / "scripts" / "qa_backend_bgk_units_01_06.py",
])
for path in source_bindings:
    require(path.is_file(), f"Cumulative BGK backend source binding is absent: {rel(path)}")

counts = dict(sorted(Counter(row["entity_class"] for row in records).items()))
exercise_ids = sorted(row["stable_id"] for row in records if row["entity_class"] == "exercise")
solution_ids = sorted(row["stable_id"] for row in records if row["entity_class"] == "solution")
asset_ids = sorted(row["stable_id"] for row in records if row["entity_class"] == "asset")
manifest = {
    "schema": "ag-bridge-bgk-native-backend-export-manifest-v1",
    "schema_version": "1.0.0",
    "record_schema_version": SCHEMA_VERSION,
    "generated_from_authority_utc": TIMESTAMP,
    "through_unit": 6,
    "scope": "BGK cumulative Units 1--6; namespace separate from classical Units 1--30",
    "encoding": "UTF-8",
    "serialization": "append-only canonical JSON Lines with CRLF; exact Units 1--4 files are byte prefixes",
    "record_count": len(records),
    "units_01_04_baseline_record_count": len(base_records),
    "units_05_06_added_record_count": len(new_records),
    "counts": counts,
    "source_heading_id_count": base_manifest["source_heading_id_count"] + len(frontmatter_heading_ids) +
                               len(source_heading_ids[5]) + len(source_heading_ids[6]),
    "cumulative_frontmatter_heading_id_count": len(frontmatter_heading_ids),
    "unit5_source_heading_id_count": len(source_heading_ids[5]),
    "unit6_source_heading_id_count": len(source_heading_ids[6]),
    "source_heading_namespace": "br-bgk-2019-*",
    "exercise_count": len(exercise_ids),
    "unit5_exercise_count": 11,
    "unit6_exercise_count": 19,
    "public_solution_count": len(solution_ids),
    "public_solution_ids": solution_ids,
    "unit5_public_solution_count": 1,
    "unit6_public_solution_count": 0,
    "component_asset_count": len(asset_ids),
    "units_05_06_component_asset_count": 0,
    "unit5_term_count": len(unit_term_ids[5]),
    "unit6_term_count": len(unit_term_ids[6]),
    "units_05_06_appended_term_record_count": 20,
    "unit5_correction_count": 6,
    "unit6_correction_count": 5,
    "files": [{"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)}
              for path in export_files],
    "source_bindings": [{"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)}
                        for path in source_bindings],
    "units_01_04_immutable_baseline": {
        "manifest_path": rel(BASE_MANIFEST), "manifest_sha256": digest(BASE_MANIFEST),
        "records_path": rel(BASE_RECORDS), "records_sha256": digest(BASE_RECORDS),
        "record_count": len(base_records), "records_byte_prefix_identity": True,
        "class_projection_byte_prefix_identity": True,
    },
    "classical_collision_baseline": {
        "path": rel(CLASSICAL_RECORDS), "bytes": CLASSICAL_RECORDS.stat().st_size,
        "sha256": digest(CLASSICAL_RECORDS), "stable_id_count": len(classical_ids),
        "intersection_count": 0,
    },
    "reader_binding": {
        "qa_path": rel(READER_QA), "qa_sha256": digest(READER_QA),
        "receipt_path": rel(READER_RECEIPT), "receipt_sha256": digest(READER_RECEIPT),
        "html_path": rel(READER_HTML), "html_sha256": digest(READER_HTML),
        "pdf_path": rel(READER_PDF), "pdf_sha256": digest(READER_PDF),
        "pdf_pages": reader_qa["pdf"]["pages_pypdf"],
    },
    "model_provenance": MODEL_PROVENANCE,
    "validation": {
        "unique_stable_ids": True,
        "parent_rights_concept_and_relation_endpoint_closure": True,
        "records_exact_set_union_of_class_projections": True,
        "units_01_04_records_and_class_projections_are_exact_byte_prefixes": True,
        "source_heading_ids_preserved": True,
        "br_bgk_2019_namespace_disjoint_from_classical": True,
        "exact_101_exercise_three_public_solution_closure": True,
        "exact_units_05_06_terminology_and_correction_ledger_closure": True,
        "all_units_05_06_records_carry_exact_model_provenance": True,
        "authority_translation_reader_zero_media_and_component_rights_bound": True,
        "deterministic_double_replay_required": True,
    },
}
(OUT / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                   encoding="utf-8", newline="\n")
print(json.dumps({"status": "PASS", "output": rel(OUT), "record_count": len(records),
                  "units_05_06_added_record_count": len(new_records), "counts": counts},
                 ensure_ascii=False))
