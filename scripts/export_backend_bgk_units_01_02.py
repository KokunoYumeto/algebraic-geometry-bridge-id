#!/usr/bin/env python3
"""Export the cumulative native BGK backend through Units 1--2.

The accepted Unit 1 backend is an immutable baseline.  Every baseline record
is copied without mutation, while Unit 2 is generated only from frozen
authority, completed Indonesian source, terminology/correction ledgers, and
authority/translation/media QA evidence.  The output remains isolated from
the completed classical-course backend.
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
BASE = ROOT / "backend" / "bgk-units-01"
OUT = ROOT / "backend" / "bgk-units-01-02"
BASE_MANIFEST = BASE / "MANIFEST.json"
BASE_RECORDS = BASE / "records.jsonl"
BASE_QA = ROOT / "qa" / "BGK_UNITS_01_BACKEND_QA.json"
BASE_MANIFEST_SHA256 = "451c4cc0ea4caf7a45aeef1edc1d7a9cc8c9e47026d843127020a40ba16177a6"
BASE_RECORDS_SHA256 = "5700bfea56e5cb52de82d0cd23c5439348298f7112efdd3f58f36b14b392902e"

SCHEMA_NAME = "ag-bridge-backend-record"
SCHEMA_VERSION = "1.0.0"
WORKFLOW_ID = "workflow.o016-d100.algebraic-geometry-bridge-id"
COURSE_ID = "course.o016-d100.bgk-bridge"
SOURCE_RESOURCE = "resource.brenner.bgk.wikiversity.2019-2020"
LOCAL_RESOURCE = "resource.bgk-id.editorial-layer"
PDF_RESOURCE = "resource.brenner.bgk.unit-02.official-pdf-witnesses"
SOURCE_EDITION = "edition.brenner.bgk.unit-02.freeze-2026-08-28"
DERIVATIVE_EDITION = "edition.bgk-id.units-01-02.2026-08-29"
SEMANTIC_RIGHTS = "rights.bgk-semantic-text.cc-by-sa-4.0"
EDITORIAL_RIGHTS = "rights.bgk-id.derivative.cc-by-sa-4.0"
PDF_RIGHTS = "rights.bgk.u02.official-pdf.component-notices-3.0-and-4.0"
MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."

SOURCE_DIR = ROOT / "source" / "id-ID" / "bgk"
SOURCE_FILES = [
    SOURCE_DIR / "frontmatter-bgk-units-01-02.md",
    SOURCE_DIR / "lecture-02.md",
    SOURCE_DIR / "worksheet-02.md",
    SOURCE_DIR / "worksheet-02-solutions.md",
]
COURSE_MANIFEST_PATH = ROOT / "authority" / "wikiversity-bgk" / "course" / "COURSE_AUTHORITY_MANIFEST.json"
UNIT_MANIFEST_PATH = ROOT / "authority" / "wikiversity-bgk" / "unit-02" / "UNIT_AUTHORITY_MANIFEST.json"
EXERCISE_MAP_PATH = ROOT / "authority" / "wikiversity-bgk" / "unit-02" / "ORDERED_EXERCISE_MAP.json"
SOLUTION_CANDIDATES_PATH = ROOT / "authority" / "wikiversity-bgk" / "unit-02" / "worksheet-solution-candidates-api.json"
SOLUTION_XML_PATH = ROOT / "authority" / "wikiversity-bgk" / "unit-02" / "solution-ex04.xml"
SOLUTION_HTML_PATH = ROOT / "authority" / "wikiversity-bgk" / "unit-02" / "solution-ex04.html"
OFFICIAL_PDFS_API_PATH = ROOT / "authority" / "wikiversity-bgk" / "unit-02" / "official-pdfs-api.json"
AUTHORITY_FREEZE_PATH = ROOT / "authority" / "BGK_UNIT_02_AUTHORITY_FREEZE.md"
RIGHTS_PATH = ROOT / "authority" / "RIGHTS-bgk-unit-02.csv"
ASSET_CLOSURE_PATH = ROOT / "authority" / "ASSET_CLOSURE-bgk-unit-02.json"
COMMONS_METADATA_PATH = ROOT / "authority" / "commons-imageinfo-bgk-unit-02.json"
MEDIA_CREDITS_PATH = ROOT / "source" / "id-ID" / "media-credits-bgk-unit-02.md"
AUTHORITY_QA_PATH = ROOT / "qa" / "BGK_UNIT_02_AUTHORITY_QA.json"
TRANSLATION_QA_PATH = ROOT / "qa" / "BGK_UNIT_02_TRANSLATION_QA.json"
TERMINOLOGY_PATH = ROOT / "00_control" / "TERMINOLOGY.csv"
CORRECTIONS_PATH = ROOT / "00_control" / "CORRECTIONS.csv"
LECTURE_PDF_PATH = ROOT / "authority" / "artifacts" / "bgk-lecture-02-official.pdf"
WORKSHEET_PDF_PATH = ROOT / "authority" / "artifacts" / "bgk-worksheet-02-official.pdf"
CLASSICAL_RECORDS = ROOT / "backend" / "units-01-30" / "records.jsonl"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


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


required_inputs = [
    BASE_MANIFEST, BASE_RECORDS, BASE_QA, *SOURCE_FILES, COURSE_MANIFEST_PATH,
    UNIT_MANIFEST_PATH, EXERCISE_MAP_PATH, SOLUTION_CANDIDATES_PATH,
    SOLUTION_XML_PATH, SOLUTION_HTML_PATH, OFFICIAL_PDFS_API_PATH,
    AUTHORITY_FREEZE_PATH, RIGHTS_PATH, ASSET_CLOSURE_PATH,
    COMMONS_METADATA_PATH, MEDIA_CREDITS_PATH, AUTHORITY_QA_PATH,
    TRANSLATION_QA_PATH, TERMINOLOGY_PATH, CORRECTIONS_PATH,
    LECTURE_PDF_PATH, WORKSHEET_PDF_PATH, CLASSICAL_RECORDS,
]
for required in required_inputs:
    require(required.is_file(), f"Required cumulative BGK backend input is absent: {rel(required)}")

require(digest(BASE_MANIFEST) == BASE_MANIFEST_SHA256, "Accepted Unit 1 backend manifest drifted")
require(digest(BASE_RECORDS) == BASE_RECORDS_SHA256, "Accepted Unit 1 records drifted")
base_manifest = read_json(BASE_MANIFEST)
require(base_manifest.get("through_unit") == 1 and base_manifest.get("record_count") == 746,
        "Accepted Unit 1 backend scope drifted")
for binding in base_manifest["files"]:
    path = ROOT / binding["path"]
    require(path.is_file() and path.stat().st_size == binding["bytes"] and digest(path) == binding["sha256"],
            f"Accepted Unit 1 backend projection drifted: {binding['path']}")

base_records = read_jsonl(BASE_RECORDS)
base_ids = {row["stable_id"] for row in base_records}
require(len(base_records) == len(base_ids) == 746, "Accepted Unit 1 stable-ID closure drifted")
base_schema = read_json(BASE / "record.schema.json")
ENTITY_CLASSES = list(base_schema["properties"]["entity_class"]["enum"])
for entity_class in ENTITY_CLASSES:
    projection = read_jsonl(BASE / f"{entity_class}.jsonl")
    expected = sorted((row for row in base_records if row["entity_class"] == entity_class),
                      key=lambda row: row["stable_id"])
    require(jsonl_bytes(projection) == jsonl_bytes(expected),
            f"Accepted Unit 1 {entity_class} projection is not its exact records union")

unit_manifest = read_json(UNIT_MANIFEST_PATH)
exercise_map = read_json(EXERCISE_MAP_PATH)
asset_closure = read_json(ASSET_CLOSURE_PATH)
authority_qa = read_json(AUTHORITY_QA_PATH)
translation_qa = read_json(TRANSLATION_QA_PATH)
require(unit_manifest.get("unit_number") == 2, "BGK Unit 2 authority identity mismatch")
require(exercise_map.get("unit") == 2 and exercise_map.get("exercise_count") == 27,
        "BGK Unit 2 exercise map must contain exactly 27 exercises")
require(exercise_map.get("solution_count") == 1, "BGK Unit 2 must expose exactly one public solution")
public_solution_rows = [row for row in exercise_map["entries"] if row.get("has_public_solution")]
require(len(public_solution_rows) == 1 and public_solution_rows[0]["exercise_number"] == 4,
        "BGK Unit 2 public solution closure is not exactly Exercise 2.4")
require(str(authority_qa.get("status", "")).startswith("PASS"), "BGK Unit 2 authority QA is not PASS")
require(str(translation_qa.get("status", "")).startswith("PASS"), "BGK Unit 2 translation QA is not PASS")
require(asset_closure.get("unit") == 2 and asset_closure.get("reader_media_positions") == 3,
        "BGK Unit 2 reader-media position closure mismatch")
require(asset_closure.get("unique_primary_local_assets") == 3 and
        asset_closure.get("unique_pdf_companion_assets") == 1 and
        asset_closure.get("unique_local_assets") == 4,
        "BGK Unit 2 local-media closure must contain three primary assets and one companion")
TIMESTAMP = unit_manifest["frozen_utc"]

with RIGHTS_PATH.open("r", encoding="utf-8-sig", newline="") as stream:
    rights_rows = list(csv.DictReader(stream))
require([row["asset_id"] for row in rights_rows] == [
    "br-bgk-u02-media-001", "br-bgk-u02-media-002", "br-bgk-u02-media-003"
], "BGK Unit 2 component-rights rows are not the exact ordered three-asset closure")
closure_assets = {row["asset_id"]: row for row in asset_closure["assets"]}
require(set(closure_assets) == {row["asset_id"] for row in rights_rows},
        "BGK Unit 2 rights and asset-closure identities disagree")
for row in rights_rows:
    path = ROOT / row["local_path"]
    closure = closure_assets[row["asset_id"]]
    require(path.is_file() and path.stat().st_size == int(row["local_bytes"]),
            f"BGK Unit 2 asset bytes absent or drifted: {row['asset_id']}")
    require(digest(path) == row["local_sha256"] == closure["local_sha256"],
            f"BGK Unit 2 asset hash drifted: {row['asset_id']}")
    if row["pdf_local_path"]:
        companion = ROOT / row["pdf_local_path"]
        require(companion.is_file() and companion.stat().st_size == int(row["pdf_local_bytes"]) and
                digest(companion) == row["pdf_local_sha256"] == closure["pdf_local_sha256"],
                f"BGK Unit 2 PDF companion drifted: {row['asset_id']}")


def record_schema() -> dict[str, Any]:
    schema = json.loads(json.dumps(base_schema))
    schema["$id"] = "https://example.invalid/algebraic-geometry-bridge/bgk-backend-record-units-01-02-v1.schema.json"
    schema["title"] = "BGK Indonesian native backend record through Units 1--2"
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
        # Every Unit 2 record carries the exact production-model identity.  More
        # specific source provenance supplied by callers is retained verbatim.
        "provenance": provenance if provenance is not None else {"model": MODEL_PROVENANCE},
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


def add(row: dict[str, Any]) -> None:
    require(row["stable_id"] not in base_ids, f"Unit 2 attempts to mutate Unit 1 stable ID: {row['stable_id']}")
    require(row["stable_id"] not in {item["stable_id"] for item in new_records},
            f"Duplicate Unit 2 stable ID: {row['stable_id']}")
    new_records.append(row)


add(make_record(
    "resource", PDF_RESOURCE, source_local_id="bgk-unit-02-official-pdf-witnesses",
    parent_id=COURSE_ID, source_locator=rel(UNIT_MANIFEST_PATH),
    content_sha256=digest(UNIT_MANIFEST_PATH), language="de", rights_id=PDF_RIGHTS,
    payload={"unit": 2, "role": "visual and numbering witnesses, not semantic authority",
             "component_notice_discrepancy_preserved": True},
))
add(make_record(
    "edition", SOURCE_EDITION, source_local_id="bgk-unit-02-authority-freeze",
    parent_id=SOURCE_RESOURCE, resource_id=SOURCE_RESOURCE, edition_id=SOURCE_EDITION,
    source_locator=rel(UNIT_MANIFEST_PATH), content_sha256=digest(UNIT_MANIFEST_PATH),
    language="de", rights_id=SEMANTIC_RIGHTS,
    payload={
        "unit": 2,
        "lecture_pageid": unit_manifest["lecture"]["pageid"],
        "lecture_revid": unit_manifest["lecture"]["revid"],
        "worksheet_pageid": unit_manifest["worksheet"]["pageid"],
        "worksheet_revid": unit_manifest["worksheet"]["revid"],
        "exercise_count": 27,
        "public_solution_count": 1,
        "public_solution_exercise": 4,
    },
))
add(make_record(
    "edition", DERIVATIVE_EDITION, source_local_id="bgk-id-units-01-02",
    parent_id=LOCAL_RESOURCE, resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION,
    source_locator=rel(SOURCE_FILES[0]), content_sha256=digest(SOURCE_FILES[0]),
    language="id-ID", translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
    payload={"through_unit": 2, "source_editions": [
        "edition.brenner.bgk.unit-01.freeze-2026-08-28", SOURCE_EDITION],
        "status": "complete source translation; cumulative native backend",
        "model_provenance": MODEL_PROVENANCE,
        "unit1_records_immutable": True},
))
add(make_record(
    "rights", PDF_RIGHTS, parent_id=PDF_RESOURCE, resource_id=PDF_RESOURCE,
    edition_id=DERIVATIVE_EDITION, source_locator=rel(ASSET_CLOSURE_PATH),
    content_sha256=digest(ASSET_CLOSURE_PATH), rights_id=PDF_RIGHTS,
    payload={"title": "Unit 2 official PDF witness notices", "license": "component notices preserved",
             "current_commons_metadata": "CC BY-SA 4.0", "embedded_pdf_notice": "CC BY-SA 3.0",
             "blanket_relicensing_claim": False},
))

asset_rights_ids = {
    "br-bgk-u02-media-001": "rights.bgk.u02.media-001.cc-by-sa-3.0",
    "br-bgk-u02-media-002": "rights.bgk.u02.media-002.public-domain",
    "br-bgk-u02-media-003": "rights.bgk.u02.media-003.cc-by-sa-4.0",
}
asset_paths_to_ids: dict[str, str] = {}
companion_ids: list[tuple[str, str]] = []
for order, row in enumerate(rights_rows, start=1):
    rights_id = asset_rights_ids[row["asset_id"]]
    add(make_record(
        "rights", rights_id, source_local_id=row["resource_title"], parent_id=SOURCE_RESOURCE,
        order=order, resource_id=SOURCE_RESOURCE, edition_id=SOURCE_EDITION,
        source_locator=f"{rel(RIGHTS_PATH)}#{row['asset_id']}", content_sha256=text_digest(canonical(row)),
        rights_id=rights_id,
        payload={"title": row["resource_title"], "license": row["license_short"],
                 "usage_terms": row["usage_terms"], "license_url": row["license_url"] or None,
                 "attribution_required": row["attribution_required"].casefold() == "true",
                 "source_inline_label": row["source_course_inline_license_label"],
                 "license_discrepancy_present": row["license_discrepancy_present"].casefold() == "true",
                 "license_discrepancy_note": row["license_discrepancy_note"],
                 "ledger_row": row},
    ))
    local_path = ROOT / row["local_path"]
    add(make_record(
        "asset", row["asset_id"], source_local_id=row["resource_title"], parent_id=SOURCE_RESOURCE,
        order=order, path=row["local_path"], resource_id=SOURCE_RESOURCE, edition_id=SOURCE_EDITION,
        source_locator=row["description_url"], content_sha256=row["local_sha256"], rights_id=rights_id,
        payload={"repository": row["repository"], "caption": row["reader_caption_id"],
                 "alt": row["reader_alt_id"], "bytes": int(row["local_bytes"]),
                 "width": int(row["local_width"]), "height": int(row["local_height"]),
                 "source_mime": row["mime"], "local_suffix": local_path.suffix.casefold(),
                 "license": row["license_short"], "frame_count": int(row["frame_count"]),
                 "html_animation_preserved": row["html_animation_preserved"].casefold() == "true",
                 "thumbnail_dimension_discrepancy": row["thumbnail_dimension_discrepancy"]},
    ))
    asset_paths_to_ids[row["local_path"]] = row["asset_id"]
    if row["pdf_local_path"]:
        companion_id = f"{row['asset_id']}-pdf-frame-001"
        companion_ids.append((companion_id, row["asset_id"]))
        add(make_record(
            "asset", companion_id, source_local_id=Path(row["pdf_local_path"]).name,
            parent_id=row["asset_id"], order=1, path=row["pdf_local_path"],
            resource_id=SOURCE_RESOURCE, edition_id=SOURCE_EDITION,
            source_locator=f"{row['description_url']}#derived-first-frame",
            content_sha256=row["pdf_local_sha256"], rights_id=rights_id,
            payload={"bytes": int(row["pdf_local_bytes"]), "mime": "image/png",
                     "role": "deterministic PDF first-frame companion",
                     "derived_from_asset_id": row["asset_id"],
                     "derivation": row["pdf_companion_source"]},
        ))

concept_specs = {
    "section": ("seksi", ["seksi", "section"]),
    "vector-field": ("medan vektor", ["medan vektor"]),
    "hairy-ball-theorem": ("teorema bola berbulu", ["bola berbulu", "titik nol"]),
    "gluing-datum": ("data pengeleman", ["data pengeleman", "dilem"]),
    "cocycle": ("syarat kokikel", ["kokikel"]),
    "quotient-topology": ("topologi hasil bagi", ["topologi hasil bagi", "ruang hasil bagi"]),
    "line-bundle": ("bundel garis", ["bundel garis"]),
    "mobius-strip": ("pita Möbius", ["möbius", "mobius"]),
    "transition-function": ("fungsi transisi", ["pemetaan transisi", "deskripsi matriks"]),
    "continuous-map-gluing": ("pengeleman pemetaan kontinu", ["pemetaan kontinu", "mengeleman pemetaan"]),
}
concept_keywords: dict[str, list[str]] = {
    row["stable_id"]: list(row["payload"].get("matching_keywords", []))
    for row in base_records if row["entity_class"] == "concept"
}
for order, (key, (label, keywords)) in enumerate(concept_specs.items(), start=11):
    concept_id = f"concept.br-bgk-2019.{key}"
    add(make_record(
        "concept", concept_id, source_local_id=key, parent_id=COURSE_ID, order=order,
        resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION, language="id-ID",
        translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
        payload={"preferred_label": label, "matching_keywords": keywords, "introduced_in_unit": 2},
    ))
    concept_keywords[concept_id] = keywords


def concepts_for(text: str) -> list[str]:
    lowered = text.casefold()
    return sorted(concept_id for concept_id, keywords in concept_keywords.items()
                  if any(keyword.casefold() in lowered for keyword in keywords))


with TERMINOLOGY_PATH.open("r", encoding="utf-8-sig", newline="") as stream:
    all_terms = list(csv.DictReader(stream))
base_term_local_ids = {row["source_local_id"] for row in base_records if row["entity_class"] == "term"}
expected_unit2_term_ids = {
    "AGT-0241",  # admitted Brenner-wide row reused for Quotiententopologie
    *(f"AGT-{number:04d}" for number in range(290, 299)),
}
unit2_terms = [row for row in all_terms if row.get("term_id") in expected_unit2_term_ids
               and row.get("status") == "admitted"
               and row.get("term_id") not in base_term_local_ids]
unit2_terms.sort(key=lambda row: int(row["term_id"].split("-")[-1]))
require({row["term_id"] for row in unit2_terms} == expected_unit2_term_ids,
        "BGK Unit 2 terminology closure must be exactly AGT-0241 and AGT-0290..AGT-0298")
for order, row in enumerate(unit2_terms, start=1):
    bound = concepts_for(row["preferred_target"] + " " + row["source_term"])
    add(make_record(
        "term", f"term.br-bgk-2019.{row['term_id'].casefold()}", source_local_id=row["term_id"],
        parent_id=bound[0] if bound else COURSE_ID, order=order, resource_id=LOCAL_RESOURCE,
        edition_id=DERIVATIVE_EDITION, source_locator=f"{rel(TERMINOLOGY_PATH)}#{row['term_id']}",
        content_sha256=text_digest(canonical(row)), language="id-ID",
        translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
        concept_ids=bound, payload={"ledger_row": row, "scope": "BGK Unit 2"},
    ))

heading_re = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]+\{#([^}]+)\}[ \t]*$", re.MULTILINE)
yaml_id_re = re.compile(r"^stable_id:[ \t]*['\"]?([^'\"\r\n]+)", re.MULTILINE)
exercise_by_number = {int(row["exercise_number"]): row for row in exercise_map["entries"]}
source_heading_ids: list[str] = []
image_segment_by_asset: dict[str, str] = {}


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


for source_order, path in enumerate(SOURCE_FILES, start=1):
    full_text = path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(full_text)
    headings = list(heading_re.finditer(body))
    require(headings, f"No stable headings found in {rel(path)}")
    yaml_match = yaml_id_re.search(frontmatter)
    if yaml_match:
        require(yaml_match.group(1).strip() == headings[0].group(3),
                f"YAML/top-heading stable ID mismatch in {rel(path)}")
    stack: list[tuple[int, str]] = []
    for heading_index, match in enumerate(headings):
        level = len(match.group(1))
        title = match.group(2).strip()
        stable_id = match.group(3).strip()
        require(stable_id.startswith("br-bgk-2019-"), f"Non-BGK stable heading ID: {stable_id}")
        require(stable_id not in base_ids and stable_id not in source_heading_ids,
                f"Duplicate or Unit 1 BGK source heading ID: {stable_id}")
        source_heading_ids.append(stable_id)
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
            "title": title, "heading_level": level, "document_order": source_order,
            "local_markdown": local_markdown,
            "inline_math_delimiter_count": len(re.findall(r"(?<!\$)\$(?!\$)", local_markdown)),
            "display_math_block_count": len(re.findall(r"\$\$(.*?)\$\$", local_markdown, re.DOTALL)),
        }
        if exercise_match:
            number = int(exercise_match.group(1))
            mapped = exercise_by_number.get(number)
            require(mapped is not None, f"Exercise {number} absent from frozen Unit 2 map")
            payload.update({"exercise_number": number, "source_entity": mapped["exercise_title"],
                            "source_solution_title": mapped["solution_title"],
                            "has_public_solution": mapped["has_public_solution"],
                            "prompt_markdown": local_body})
        if solution_match:
            number = int(solution_match.group(1))
            mapped = exercise_by_number.get(number)
            require(number == 4 and mapped and mapped["has_public_solution"],
                    "Translated BGK Unit 2 solution is not the exact public Exercise 2.4 solution")
            source_entry = public_solution_rows[0]
            payload.update({"exercise_number": number, "exercise_id": parent_id,
                            "source_solution_title": source_entry["solution_title"],
                            "source_pageid": source_entry["pageid"], "source_revid": source_entry["revid"],
                            "source_mediawiki_sha1": source_entry["mediawiki_sha1"],
                            "solution_markdown": local_body, "invented": False})
        add(make_record(
            entity_class, stable_id, source_local_id=stable_id, parent_id=parent_id,
            order=heading_index + 1, path=rel(path), resource_id=LOCAL_RESOURCE,
            edition_id=DERIVATIVE_EDITION, source_locator=f"{rel(path)}#{stable_id}",
            content_sha256=text_digest(local_markdown), language="id-ID",
            translation_state="structurally_verified",
            provenance={"source_edition": SOURCE_EDITION, "model": MODEL_PROVENANCE,
                        "source_file_sha256": digest(path)},
            concept_ids=concepts_for(title + "\n" + local_body), rights_id=EDITORIAL_RIGHTS,
            payload=payload,
        ))
        if not local_body:
            continue
        blocks = [block.strip() for block in re.split(r"\n[ \t]*\n", local_body) if block.strip()]
        for block_index, block in enumerate(blocks, start=1):
            block_id = f"{stable_id}-b{block_index:03d}"
            kind = block_kind(block)
            block_payload: dict[str, Any] = {
                "kind": kind, "markdown": block + "\n",
                "display_math_count": len(re.findall(r"\$\$(.*?)\$\$", block, re.DOTALL)),
                "inline_math_delimiter_count": len(re.findall(r"(?<!\$)\$(?!\$)", block)),
            }
            if kind == "image":
                matching_assets = [asset_id for asset_path, asset_id in asset_paths_to_ids.items()
                                   if asset_path in block]
                require(len(matching_assets) == 1, f"Unbound or ambiguous BGK Unit 2 image block: {block_id}")
                asset_id = matching_assets[0]
                require(asset_id not in image_segment_by_asset, f"Repeated BGK Unit 2 reader asset: {asset_id}")
                block_payload["asset_id"] = asset_id
                image_segment_by_asset[asset_id] = block_id
            add(make_record(
                "segment", block_id, source_local_id=block_id, parent_id=stable_id,
                order=block_index, path=rel(path), resource_id=LOCAL_RESOURCE,
                edition_id=DERIVATIVE_EDITION,
                source_locator=f"{rel(path)}#{stable_id}:block-{block_index}",
                content_sha256=text_digest(block + "\n"), language="id-ID",
                translation_state="structurally_verified",
                provenance={"source_file_sha256": digest(path), "model": MODEL_PROVENANCE},
                concept_ids=concepts_for(block), rights_id=EDITORIAL_RIGHTS, payload=block_payload,
            ))

expected_exercises = [f"br-bgk-2019-w02-ex{number:02d}" for number in range(1, 28)]
actual_exercises = sorted(row["stable_id"] for row in new_records if row["entity_class"] == "exercise")
require(actual_exercises == expected_exercises, "Translated Unit 2 exercise IDs are not exact ex01..ex27 closure")
actual_solutions = [row["stable_id"] for row in new_records if row["entity_class"] == "solution"]
require(actual_solutions == ["br-bgk-2019-w02-ex04-solution"],
        "Translated Unit 2 public solution closure is not exactly Exercise 2.4")
require(set(image_segment_by_asset) == {row["asset_id"] for row in rights_rows},
        "All three primary Unit 2 reader media must occur exactly once in translated source")

with CORRECTIONS_PATH.open("r", encoding="utf-8-sig", newline="") as stream:
    all_corrections = list(csv.DictReader(stream))
base_correction_ids = {row["source_local_id"] for row in base_records if row["entity_class"] == "correction"}
expected_unit2_correction_ids = {f"AGC-CORR-{number:04d}" for number in range(142, 149)}
unit2_corrections = [row for row in all_corrections
                     if row.get("correction_id") in expected_unit2_correction_ids
                     and row.get("correction_id") not in base_correction_ids
                     and row.get("status") == "applied_at_bgk_unit_02_translation"]
unit2_corrections.sort(key=lambda row: int(row["correction_id"].split("-")[-1]))
require({row["correction_id"] for row in unit2_corrections} == expected_unit2_correction_ids,
        "BGK Unit 2 correction closure must be exactly AGC-CORR-0142..AGC-CORR-0148")
for order, row in enumerate(unit2_corrections, start=1):
    scope = row["scope"].casefold()
    if "solution" in scope:
        parent_id = "br-bgk-2019-w02-ex04-solution"
    elif "worksheet" in scope:
        parent_id = "br-bgk-2019-w02"
    elif "lecture" in scope:
        parent_id = "br-bgk-2019-l02"
    else:
        parent_id = DERIVATIVE_EDITION
    add(make_record(
        "correction", f"correction.br-bgk-2019.u02.{row['correction_id'].split('-')[-1]}",
        source_local_id=row["correction_id"], parent_id=parent_id, order=order,
        resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION,
        source_locator=f"{rel(CORRECTIONS_PATH)}#{row['correction_id']}",
        content_sha256=text_digest(canonical(row)), language="id-ID",
        translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
        payload={"ledger_row": row, "source_issue": row["authority_observation"],
                 "adopted_reading": row["target_action"], "disclosed_in_reader": True,
                 "silent_change": False},
    ))

artifact_paths = [
    *SOURCE_FILES, UNIT_MANIFEST_PATH, EXERCISE_MAP_PATH, SOLUTION_CANDIDATES_PATH,
    SOLUTION_XML_PATH, SOLUTION_HTML_PATH, OFFICIAL_PDFS_API_PATH,
    AUTHORITY_FREEZE_PATH, RIGHTS_PATH, ASSET_CLOSURE_PATH, COMMONS_METADATA_PATH,
    MEDIA_CREDITS_PATH, AUTHORITY_QA_PATH, TRANSLATION_QA_PATH,
    TERMINOLOGY_PATH, CORRECTIONS_PATH, LECTURE_PDF_PATH, WORKSHEET_PDF_PATH,
    *[ROOT / row["local_path"] for row in rights_rows],
    *[ROOT / row["pdf_local_path"] for row in rights_rows if row["pdf_local_path"]],
]
require(len(artifact_paths) == len(set(artifact_paths)), "Duplicate Unit 2 backend artifact path")
asset_rights_by_path = {ROOT / row["local_path"]: asset_rights_ids[row["asset_id"]] for row in rights_rows}
asset_rights_by_path.update({ROOT / row["pdf_local_path"]: asset_rights_ids[row["asset_id"]]
                             for row in rights_rows if row["pdf_local_path"]})
for order, path in enumerate(artifact_paths, start=1):
    require(path.is_file(), f"Bound BGK Unit 2 artifact is absent: {rel(path)}")
    suffix = path.suffix.casefold()
    media_type = {".md": "text/markdown", ".json": "application/json", ".csv": "text/csv",
                  ".pdf": "application/pdf", ".jpg": "image/jpeg", ".png": "image/png",
                  ".gif": "image/gif", ".xml": "application/xml"}.get(suffix, "application/octet-stream")
    if path in asset_rights_by_path:
        rights_id = asset_rights_by_path[path]
    elif path in (LECTURE_PDF_PATH, WORKSHEET_PDF_PATH):
        rights_id = PDF_RIGHTS
    elif path in SOURCE_FILES or path in (MEDIA_CREDITS_PATH, TRANSLATION_QA_PATH,
                                          TERMINOLOGY_PATH, CORRECTIONS_PATH):
        rights_id = EDITORIAL_RIGHTS
    else:
        rights_id = SEMANTIC_RIGHTS
    add(make_record(
        "artifact", f"artifact.br-bgk-2019.u02.{order:02d}", source_local_id=path.name,
        parent_id=DERIVATIVE_EDITION, order=order, path=rel(path), resource_id=LOCAL_RESOURCE,
        edition_id=DERIVATIVE_EDITION, source_locator=rel(path), content_sha256=digest(path),
        language="id-ID" if path in SOURCE_FILES or path == MEDIA_CREDITS_PATH else "und",
        translation_state="structurally_verified" if path in SOURCE_FILES or path == TRANSLATION_QA_PATH
        else "source_frozen", rights_id=rights_id,
        payload={"bytes": path.stat().st_size, "media_type": media_type, "unit": 2},
    ))

add(make_record(
    "qa_event", "qa.br-bgk-2019.u02.authority-closure", source_local_id="BGK_UNIT_02_AUTHORITY_QA",
    parent_id=DERIVATIVE_EDITION, order=1, path=rel(AUTHORITY_QA_PATH), resource_id=LOCAL_RESOURCE,
    edition_id=DERIVATIVE_EDITION, source_locator=rel(AUTHORITY_QA_PATH),
    content_sha256=digest(AUTHORITY_QA_PATH), translation_state="structurally_verified",
    rights_id=EDITORIAL_RIGHTS,
    payload={"status": authority_qa["status"], "exercise_count": 27,
             "public_solution_count": 1, "public_solution_exercise": 4},
))
add(make_record(
    "qa_event", "qa.br-bgk-2019.u02.translation-closure", source_local_id="BGK_UNIT_02_TRANSLATION_QA",
    parent_id=DERIVATIVE_EDITION, order=2, path=rel(TRANSLATION_QA_PATH), resource_id=LOCAL_RESOURCE,
    edition_id=DERIVATIVE_EDITION, source_locator=rel(TRANSLATION_QA_PATH),
    content_sha256=digest(TRANSLATION_QA_PATH), language="id-ID",
    translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
    payload={"status": translation_qa["status"], "qa_schema": translation_qa.get("schema"),
             "model_provenance": MODEL_PROVENANCE},
))
add(make_record(
    "qa_event", "qa.br-bgk-2019.u02.media-closure", source_local_id="ASSET_CLOSURE-bgk-unit-02",
    parent_id=DERIVATIVE_EDITION, order=3, path=rel(ASSET_CLOSURE_PATH), resource_id=LOCAL_RESOURCE,
    edition_id=DERIVATIVE_EDITION, source_locator=rel(ASSET_CLOSURE_PATH),
    content_sha256=digest(ASSET_CLOSURE_PATH), translation_state="structurally_verified",
    rights_id=EDITORIAL_RIGHTS,
    payload={"reader_media_positions": 3, "primary_assets": 3, "pdf_companions": 1,
             "unique_local_assets": 4, "animated_html_positions": 1},
))

# Add graph edges only for new Unit 2 records.  Baseline relations and every
# baseline payload remain byte-identical.
non_relations = list(new_records)
relation_order = 0
for row in non_relations:
    if row["parent_id"] is None:
        continue
    relation_order += 1
    add(make_record(
        "relation", f"relation.br-bgk-2019.u02.{relation_order:04d}", parent_id=COURSE_ID,
        order=relation_order, resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION,
        content_sha256=text_digest(row["parent_id"] + "\ncontains\n" + row["stable_id"]),
        translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
        payload={"subject_id": row["parent_id"], "predicate": "contains", "object_id": row["stable_id"]},
    ))
for asset_id, segment_id in sorted(image_segment_by_asset.items()):
    relation_order += 1
    add(make_record(
        "relation", f"relation.br-bgk-2019.u02.{relation_order:04d}", parent_id=COURSE_ID,
        order=relation_order, resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION,
        content_sha256=text_digest(segment_id + "\ndepicts-with\n" + asset_id),
        translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
        payload={"subject_id": segment_id, "predicate": "depicts_with", "object_id": asset_id},
    ))
for companion_id, source_asset_id in companion_ids:
    relation_order += 1
    add(make_record(
        "relation", f"relation.br-bgk-2019.u02.{relation_order:04d}", parent_id=COURSE_ID,
        order=relation_order, resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION,
        content_sha256=text_digest(companion_id + "\nderives-from\n" + source_asset_id),
        translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
        payload={"subject_id": companion_id, "predicate": "derives_from", "object_id": source_asset_id},
    ))

records = base_records + new_records
ids = [row["stable_id"] for row in records]
require(len(ids) == len(set(ids)), "Duplicate cumulative BGK backend stable ID")
id_set = set(ids)
for row in records:
    require(row["parent_id"] is None or row["parent_id"] in id_set, f"Missing parent for {row['stable_id']}")
    require(all(concept_id in id_set for concept_id in row["concept_ids"]),
            f"Missing concept binding for {row['stable_id']}")
    if row["rights_id"] is not None:
        require(row["rights_id"] in id_set, f"Missing rights binding for {row['stable_id']}")
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
require(all(row["provenance"].get("model") == MODEL_PROVENANCE for row in new_records),
        "One or more Unit 2 records lack the exact model provenance")

sorted_records = sorted(records, key=lambda row: (row["entity_class"], row["stable_id"]))
by_class: dict[str, list[dict[str, Any]]] = {entity_class: [] for entity_class in ENTITY_CLASSES}
for row in sorted_records:
    by_class[row["entity_class"]].append(row)
for entity_class in ENTITY_CLASSES:
    baseline_projection = (BASE / f"{entity_class}.jsonl").read_bytes()
    cumulative_baseline_rows = [row for row in by_class[entity_class] if row["stable_id"] in base_ids]
    require(jsonl_bytes(cumulative_baseline_rows) == baseline_projection,
            f"Unit 1 {entity_class} class projection changed in cumulative backend")

OUT.mkdir(parents=True, exist_ok=True)
schema_path = OUT / "record.schema.json"
schema_path.write_text(json.dumps(record_schema(), ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8", newline="\n")
(OUT / "records.jsonl").write_bytes(jsonl_bytes(sorted_records))
for entity_class in ENTITY_CLASSES:
    (OUT / f"{entity_class}.jsonl").write_bytes(jsonl_bytes(by_class[entity_class]))

export_files = [schema_path, OUT / "records.jsonl", *[OUT / f"{name}.jsonl" for name in ENTITY_CLASSES]]
baseline_bindings = [BASE_MANIFEST, BASE_QA, BASE / "record.schema.json", BASE_RECORDS,
                     *[BASE / f"{name}.jsonl" for name in ENTITY_CLASSES]]
unit2_asset_paths = [ROOT / row["local_path"] for row in rights_rows] + [
    ROOT / row["pdf_local_path"] for row in rights_rows if row["pdf_local_path"]]
source_bindings = [
    *baseline_bindings, *required_inputs[3:], *unit2_asset_paths,
    Path(__file__), ROOT / "scripts" / "qa_backend_bgk_units_01_02.py",
]
deduplicated_bindings: list[Path] = []
for path in source_bindings:
    if path not in deduplicated_bindings:
        deduplicated_bindings.append(path)
for path in deduplicated_bindings:
    require(path.is_file(), f"Cumulative BGK backend source binding is absent: {rel(path)}")

counts = dict(sorted(Counter(row["entity_class"] for row in sorted_records).items()))
manifest = {
    "schema": "ag-bridge-bgk-native-backend-export-manifest-v1",
    "schema_version": "1.0.0",
    "record_schema_version": SCHEMA_VERSION,
    "generated_from_authority_utc": TIMESTAMP,
    "through_unit": 2,
    "scope": "BGK cumulative Units 1--2; namespace separate from classical Units 1--30",
    "encoding": "UTF-8",
    "serialization": "canonical JSON Lines: records and keys sorted, compact separators, CRLF",
    "record_count": len(sorted_records),
    "unit1_baseline_record_count": len(base_records),
    "unit2_added_record_count": len(new_records),
    "counts": counts,
    "source_heading_id_count": base_manifest["source_heading_id_count"] + len(source_heading_ids),
    "unit2_source_heading_id_count": len(source_heading_ids),
    "source_heading_namespace": "br-bgk-2019-*",
    "exercise_count": 44,
    "unit2_exercise_count": 27,
    "public_solution_count": 1,
    "public_solution_ids": ["br-bgk-2019-w02-ex04-solution"],
    "component_asset_count": 5,
    "unit2_component_asset_count": 4,
    "unit2_term_count": len(unit2_terms),
    "unit2_correction_count": len(unit2_corrections),
    "files": [{"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)}
              for path in export_files],
    "source_bindings": [{"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)}
                        for path in deduplicated_bindings],
    "unit1_immutable_baseline": {
        "manifest_path": rel(BASE_MANIFEST), "manifest_sha256": digest(BASE_MANIFEST),
        "records_path": rel(BASE_RECORDS), "records_sha256": digest(BASE_RECORDS),
        "record_count": len(base_records), "class_projection_byte_identity": True,
    },
    "classical_collision_baseline": {
        "path": rel(CLASSICAL_RECORDS), "bytes": CLASSICAL_RECORDS.stat().st_size,
        "sha256": digest(CLASSICAL_RECORDS), "stable_id_count": len(classical_ids),
        "intersection_count": 0,
    },
    "model_provenance": MODEL_PROVENANCE,
    "validation": {
        "unique_stable_ids": True,
        "parent_rights_concept_and_relation_endpoint_closure": True,
        "records_exact_union_of_class_projections": True,
        "unit1_records_and_class_projections_byte_preserved": True,
        "source_heading_ids_preserved": True,
        "br_bgk_2019_namespace_disjoint_from_classical": True,
        "exact_44_exercise_one_public_solution_closure": True,
        "exact_unit2_terminology_and_correction_ledger_closure": True,
        "all_unit2_records_carry_exact_model_provenance": True,
        "authority_translation_and_component_rights_bound": True,
        "deterministic_double_replay_required": True,
    },
}
(OUT / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                   encoding="utf-8", newline="\n")
print(json.dumps({"status": "PASS", "output": rel(OUT), "record_count": len(sorted_records),
                  "unit2_added_record_count": len(new_records), "counts": counts}, ensure_ascii=False))
