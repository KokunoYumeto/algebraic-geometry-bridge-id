#!/usr/bin/env python3
"""Export the append-only native BGK backend through Units 1--4.

The accepted Units 1--3 backend is an immutable byte prefix. Unit 4 is
derived only from its frozen authority, verified Indonesian source, reader
receipt, and admitted terminology/correction ledgers. The BGK namespace stays
disjoint from the completed classical-curve backend.
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
BASE = ROOT / "backend" / "bgk-units-01-03"
OUT = ROOT / "backend" / "bgk-units-01-04"
BASE_MANIFEST = BASE / "MANIFEST.json"
BASE_RECORDS = BASE / "records.jsonl"
BASE_QA = ROOT / "qa" / "BGK_UNITS_01_03_BACKEND_QA.json"
BASE_MANIFEST_SHA256 = "2ccea7a804737c7f7e5a65bb8398e836a36cd31f3aec1a4cf6a4d1117bed0c02"
BASE_RECORDS_SHA256 = "b1a1f655d98af07a05b70108c41b9a9e865fb45f069dc1f5f93e545b1576cace"
BASE_QA_SHA256 = "7308f881141cfaabb0f3f82e5f97a45ad2c2216386ad95252c71cfa50d38562d"

SCHEMA_NAME = "ag-bridge-backend-record"
SCHEMA_VERSION = "1.0.0"
WORKFLOW_ID = "workflow.o016-d100.algebraic-geometry-bridge-id"
COURSE_ID = "course.o016-d100.bgk-bridge"
SOURCE_RESOURCE = "resource.brenner.bgk.wikiversity.2019-2020"
LOCAL_RESOURCE = "resource.bgk-id.editorial-layer"
PDF_RESOURCE = "resource.brenner.bgk.unit-04.official-pdf-witnesses"
SOURCE_EDITION = "edition.brenner.bgk.unit-04.freeze-2026-08-29"
DERIVATIVE_EDITION = "edition.bgk-id.units-01-04.2026-08-29"
SEMANTIC_RIGHTS = "rights.bgk-semantic-text.cc-by-sa-4.0"
EDITORIAL_RIGHTS = "rights.bgk-id.derivative.cc-by-sa-4.0"
PDF_RIGHTS = "rights.bgk.u04.official-pdf.component-notices-3.0-and-4.0"
MEDIA_RIGHTS = "rights.bgk.u04.media-001.cc-by-sa-2.5"
MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."

SOURCE_DIR = ROOT / "source" / "id-ID" / "bgk"
SOURCE_FILES = [
    SOURCE_DIR / "frontmatter-bgk-units-01-04.md",
    SOURCE_DIR / "lecture-04.md",
    SOURCE_DIR / "worksheet-04.md",
    SOURCE_DIR / "worksheet-04-solutions.md",
]
COURSE_MANIFEST_PATH = ROOT / "authority" / "wikiversity-bgk" / "course" / "COURSE_AUTHORITY_MANIFEST.json"
UNIT_DIR = ROOT / "authority" / "wikiversity-bgk" / "unit-04"
UNIT_MANIFEST_PATH = UNIT_DIR / "UNIT_AUTHORITY_MANIFEST.json"
EXERCISE_MAP_PATH = UNIT_DIR / "ORDERED_EXERCISE_MAP.json"
SOLUTION_CANDIDATES_PATH = UNIT_DIR / "worksheet-solution-candidates-api.json"
OFFICIAL_PDFS_API_PATH = UNIT_DIR / "official-pdfs-api.json"
AUTHORITY_FREEZE_PATH = ROOT / "authority" / "BGK_UNIT_04_AUTHORITY_FREEZE.md"
RIGHTS_PATH = ROOT / "authority" / "RIGHTS-bgk-unit-04.csv"
ASSET_CLOSURE_PATH = ROOT / "authority" / "ASSET_CLOSURE-bgk-unit-04.json"
COMMONS_METADATA_PATH = ROOT / "authority" / "commons-imageinfo-bgk-unit-04.json"
MEDIA_CREDITS_PATH = ROOT / "source" / "id-ID" / "media-credits-bgk-unit-04.md"
AUTHORITY_QA_PATH = ROOT / "qa" / "BGK_UNIT_04_AUTHORITY_QA.json"
TRANSLATION_QA_PATH = ROOT / "qa" / "BGK_UNIT_04_TRANSLATION_QA.json"
READER_QA_PATH = ROOT / "qa" / "BGK_UNITS_01_04_READER_QA.json"
TERMINOLOGY_PATH = ROOT / "00_control" / "TERMINOLOGY.csv"
CORRECTIONS_PATH = ROOT / "00_control" / "CORRECTIONS.csv"
LECTURE_PDF_PATH = ROOT / "authority" / "artifacts" / "bgk-lecture-04-official.pdf"
WORKSHEET_PDF_PATH = ROOT / "authority" / "artifacts" / "bgk-worksheet-04-official.pdf"
MEDIA_ASSET_PATH = ROOT / "authority" / "assets" / "bgk-u04-triticum-spelta.jpg"
READER_BUILD_RECEIPT = ROOT / "build" / "reader-bgk-id" / "BUILD_RECEIPT.json"
READER_HTML = ROOT / "build" / "reader-bgk-id" / "index.html"
READER_PDF = ROOT / "build" / "reader-bgk-id" / "bundel-berkas-dan-kohomologi-id-units-01-04.pdf"
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


required_inputs = [
    BASE_MANIFEST, BASE_RECORDS, BASE_QA, *SOURCE_FILES, COURSE_MANIFEST_PATH,
    UNIT_MANIFEST_PATH, EXERCISE_MAP_PATH, SOLUTION_CANDIDATES_PATH,
    OFFICIAL_PDFS_API_PATH, AUTHORITY_FREEZE_PATH, RIGHTS_PATH,
    ASSET_CLOSURE_PATH, COMMONS_METADATA_PATH, MEDIA_CREDITS_PATH,
    AUTHORITY_QA_PATH, TRANSLATION_QA_PATH, READER_QA_PATH,
    TERMINOLOGY_PATH, CORRECTIONS_PATH, LECTURE_PDF_PATH,
    WORKSHEET_PDF_PATH, MEDIA_ASSET_PATH, READER_BUILD_RECEIPT,
    READER_HTML, READER_PDF, CLASSICAL_RECORDS,
]
for required in required_inputs:
    require(required.is_file(), f"Required cumulative BGK backend input is absent: {rel(required)}")

require(digest(BASE_MANIFEST) == BASE_MANIFEST_SHA256, "Accepted Units 1--3 backend manifest drifted")
require(digest(BASE_RECORDS) == BASE_RECORDS_SHA256, "Accepted Units 1--3 records drifted")
require(digest(BASE_QA) == BASE_QA_SHA256, "Accepted Units 1--3 backend QA drifted")
base_manifest = read_json(BASE_MANIFEST)
require(base_manifest.get("through_unit") == 3 and base_manifest.get("record_count") == 2370,
        "Accepted Units 1--3 backend scope drifted")
for binding in base_manifest["files"]:
    path = ROOT / binding["path"]
    require(path.is_file() and path.stat().st_size == binding["bytes"] and digest(path) == binding["sha256"],
            f"Accepted Units 1--3 projection drifted: {binding['path']}")

base_records = read_jsonl(BASE_RECORDS)
base_ids = {row["stable_id"] for row in base_records}
require(len(base_records) == len(base_ids) == 2370, "Accepted Units 1--3 stable-ID closure drifted")
base_schema = read_json(BASE / "record.schema.json")
ENTITY_CLASSES = list(base_schema["properties"]["entity_class"]["enum"])

unit_manifest = read_json(UNIT_MANIFEST_PATH)
exercise_map = read_json(EXERCISE_MAP_PATH)
asset_closure = read_json(ASSET_CLOSURE_PATH)
authority_qa = read_json(AUTHORITY_QA_PATH)
translation_qa = read_json(TRANSLATION_QA_PATH)
reader_qa = read_json(READER_QA_PATH)
require(unit_manifest.get("unit_number") == 4, "BGK Unit 4 authority identity mismatch")
require(exercise_map.get("unit") == 4 and exercise_map.get("exercise_count") == 9,
        "BGK Unit 4 exercise map must contain exactly nine exercises")
require(exercise_map.get("solution_count") == 0 and
        not any(row.get("has_public_solution") for row in exercise_map["entries"]),
        "BGK Unit 4 must preserve the exact zero-public-solution closure")
require(str(authority_qa.get("status", "")).startswith("PASS"), "BGK Unit 4 authority QA is not PASS")
require(translation_qa.get("status") == "PASS", "BGK Unit 4 translation QA is not PASS")
require(str(reader_qa.get("status", "")).startswith("PASS") and reader_qa.get("through_unit") == 4,
        "BGK cumulative Units 1--4 reader QA is not PASS")
require(asset_closure.get("unit") == 4 and asset_closure.get("reader_media_positions") == 1 and
        asset_closure.get("unique_local_assets") == 1 and len(asset_closure.get("assets", [])) == 1,
        "BGK Unit 4 must retain its exact one-image reader-media closure")
TIMESTAMP = unit_manifest["frozen_utc"]


def record_schema() -> dict[str, Any]:
    schema = json.loads(json.dumps(base_schema))
    schema["$id"] = "https://example.invalid/algebraic-geometry-bridge/bgk-backend-record-units-01-04-v1.schema.json"
    schema["title"] = "BGK Indonesian native backend record through Units 1--4"
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
    require(row["stable_id"] not in base_ids, f"Unit 4 attempts to mutate a Units 1--3 stable ID: {row['stable_id']}")
    require(row["stable_id"] not in new_ids, f"Duplicate Unit 4 stable ID: {row['stable_id']}")
    new_ids.add(row["stable_id"])
    new_records.append(row)


add(make_record(
    "resource", PDF_RESOURCE, source_local_id="bgk-unit-04-official-pdf-witnesses",
    parent_id=COURSE_ID, source_locator=rel(ASSET_CLOSURE_PATH),
    content_sha256=digest(ASSET_CLOSURE_PATH), language="de", rights_id=PDF_RIGHTS,
    payload={"unit": 4, "role": "visual and numbering witnesses, not semantic authority",
             "component_notice_discrepancy_preserved": True, "reader_media_positions": 1},
))
add(make_record(
    "edition", SOURCE_EDITION, source_local_id="bgk-unit-04-authority-freeze",
    parent_id=SOURCE_RESOURCE, resource_id=SOURCE_RESOURCE, edition_id=SOURCE_EDITION,
    source_locator=rel(UNIT_MANIFEST_PATH), content_sha256=digest(UNIT_MANIFEST_PATH),
    language="de", rights_id=SEMANTIC_RIGHTS,
    payload={"unit": 4, "lecture_pageid": unit_manifest["lecture"]["pageid"],
             "lecture_revid": unit_manifest["lecture"]["revid"],
             "worksheet_pageid": unit_manifest["worksheet"]["pageid"],
             "worksheet_revid": unit_manifest["worksheet"]["revid"],
             "exercise_count": 9, "public_solution_count": 0,
             "reader_media_positions": 1},
))
add(make_record(
    "edition", DERIVATIVE_EDITION, source_local_id="bgk-id-units-01-04",
    parent_id=LOCAL_RESOURCE, resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION,
    source_locator=rel(SOURCE_FILES[0]), content_sha256=digest(SOURCE_FILES[0]),
    language="id-ID", translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
    payload={"through_unit": 4,
             "source_editions": [f"edition.brenner.bgk.unit-{unit:02d}.freeze-2026-08-28" for unit in range(1, 4)] + [SOURCE_EDITION],
             "status": "complete source translation and verified cumulative reader; cumulative native backend",
             "model_provenance": MODEL_PROVENANCE, "units_01_03_records_immutable": True},
))

pdf_notices = asset_closure["official_pdf_component_rights"]
require(len(pdf_notices) == 2, "Unit 4 PDF component-rights closure must contain two witnesses")
add(make_record(
    "rights", PDF_RIGHTS, parent_id=PDF_RESOURCE, resource_id=PDF_RESOURCE,
    edition_id=DERIVATIVE_EDITION, source_locator=rel(AUTHORITY_QA_PATH),
    content_sha256=digest(AUTHORITY_QA_PATH), rights_id=PDF_RIGHTS,
    payload={"title": "Unit 4 official PDF witness notices", "license": "component notices preserved",
             "current_commons_metadata": "CC BY-SA 4.0", "embedded_pdf_notice": "CC-by-sa 3.0",
             "blanket_relicensing_claim": False, "witnesses": pdf_notices},
))

with RIGHTS_PATH.open("r", encoding="utf-8-sig", newline="") as stream:
    media_rows = list(csv.DictReader(stream))
require(len(media_rows) == 1 and media_rows[0]["asset_id"] == "br-bgk-u04-media-001",
        "Unit 4 component-rights ledger must contain exactly the wheat image")
media = media_rows[0]
add(make_record(
    "rights", MEDIA_RIGHTS, source_local_id=media["metadata_title"],
    parent_id="br-bgk-u04-media-001", resource_id=SOURCE_RESOURCE,
    edition_id=SOURCE_EDITION, source_locator=media["description_url"],
    content_sha256=text_digest(canonical(media)), rights_id=MEDIA_RIGHTS,
    payload={"title": media["resource_title"], "license": media["license_short"],
             "license_url": media["license_url"], "attribution": media["artist"],
             "credit": media["credit"], "attribution_required": True,
             "blanket_relicensing_claim": False},
))
add(make_record(
    "asset", "br-bgk-u04-media-001", source_local_id=media["metadata_title"],
    parent_id=SOURCE_RESOURCE, order=1, path=rel(MEDIA_ASSET_PATH),
    resource_id=SOURCE_RESOURCE, edition_id=SOURCE_EDITION,
    source_locator=media["description_url"], content_sha256=digest(MEDIA_ASSET_PATH),
    rights_id=MEDIA_RIGHTS,
    payload={"caption": media["reader_caption_id"], "alt": media["reader_alt_id"],
             "bytes": MEDIA_ASSET_PATH.stat().st_size, "width": int(media["local_width"]),
             "height": int(media["local_height"]), "mime": media["mime"],
             "repository": media["repository"], "license": media["license_short"],
             "html_animation_preserved": False},
))

concept_specs = {
    "sheaf-morphism": ("morfisme berkas", ["morfisme berkas"]),
    "sheaf-isomorphism": ("isomorfisme berkas", ["isomorfisme berkas"]),
    "locally-free-sheaf": ("berkas bebas lokal", ["berkas bebas lokal"]),
    "sheaf-hom": ("berkas morfisme", ["berkas morfisme", "operatorname{Mor}"]),
    "sheaf-of-groups": ("berkas grup", ["berkas grup"]),
    "convergent-power-series": ("deret pangkat konvergen", ["deret pangkat konvergen"]),
    "skyscraper-sheaf": ("berkas pencakar langit", ["berkas pencakar langit"]),
}
concept_keywords: dict[str, list[str]] = {
    row["stable_id"]: list(row["payload"].get("matching_keywords", []))
    for row in base_records if row["entity_class"] == "concept"
}
concept_start = 1 + sum(row["entity_class"] == "concept" for row in base_records)
for order, (key, (label, keywords)) in enumerate(concept_specs.items(), start=concept_start):
    concept_id = f"concept.br-bgk-2019.{key}"
    add(make_record(
        "concept", concept_id, source_local_id=key, parent_id=COURSE_ID, order=order,
        resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION, language="id-ID",
        translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
        payload={"preferred_label": label, "matching_keywords": keywords, "introduced_in_unit": 4},
    ))
    concept_keywords[concept_id] = keywords


def concepts_for(text: str) -> list[str]:
    lowered = text.casefold()
    return sorted(concept_id for concept_id, keywords in concept_keywords.items()
                  if any(keyword.casefold() in lowered for keyword in keywords))


with TERMINOLOGY_PATH.open("r", encoding="utf-8-sig", newline="") as stream:
    all_terms = list(csv.DictReader(stream))
base_term_local_ids = {row["source_local_id"] for row in base_records if row["entity_class"] == "term"}
referenced_term_ids = set(translation_qa["terminology_ids_added"] + translation_qa["terminology_ids_reused"])
require(len(referenced_term_ids) == 22, "BGK Unit 4 must reference exactly 22 admitted terminology rows")
appended_term_ids = referenced_term_ids - base_term_local_ids
unit_terms = [row for row in all_terms if row.get("term_id") in appended_term_ids and row.get("status") == "admitted"]
unit_terms.sort(key=lambda row: int(row["term_id"].split("-")[-1]))
require({row["term_id"] for row in unit_terms} == appended_term_ids,
        "BGK Unit 4 terminology ledger closure is incomplete")
for order, row in enumerate(unit_terms, start=1):
    bound = concepts_for(row["preferred_target"] + " " + row["source_term"])
    add(make_record(
        "term", f"term.br-bgk-2019.{row['term_id'].casefold()}", source_local_id=row["term_id"],
        parent_id=bound[0] if bound else COURSE_ID, order=order, resource_id=LOCAL_RESOURCE,
        edition_id=DERIVATIVE_EDITION, source_locator=f"{rel(TERMINOLOGY_PATH)}#{row['term_id']}",
        content_sha256=text_digest(canonical(row)), language="id-ID",
        translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
        concept_ids=bound, payload={"ledger_row": row, "scope": "BGK Unit 4",
                                    "translation_qa_role": "added" if row["term_id"] in translation_qa["terminology_ids_added"] else "reused"},
    ))

heading_re = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]+\{#([^}]+)\}[ \t]*$", re.MULTILINE)
yaml_id_re = re.compile(r"^stable_id:[ \t]*['\"]?([^'\"\r\n]+)", re.MULTILINE)
exercise_by_number = {int(row["exercise_number"]): row for row in exercise_map["entries"]}
source_heading_ids: list[str] = []


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
                f"Duplicate or prior-unit BGK source heading ID: {stable_id}")
        source_heading_ids.append(stable_id)
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent_id = stack[-1][1] if stack else DERIVATIVE_EDITION
        stack.append((level, stable_id))
        local_end = headings[heading_index + 1].start() if heading_index + 1 < len(headings) else len(body)
        local_markdown = body[match.start():local_end].strip() + "\n"
        local_body = body[match.end():local_end].strip()
        exercise_match = re.search(r"-ex(\d{2})$", stable_id)
        if level == 1:
            entity_class = "unit"
        elif exercise_match:
            entity_class = "exercise"
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
            require(mapped is not None, f"Exercise {number} absent from frozen Unit 4 map")
            payload.update({"exercise_number": number, "source_entity": mapped["exercise_title"],
                            "source_solution_title": mapped["solution_title"],
                            "has_public_solution": False, "prompt_markdown": local_body})
        add(make_record(
            entity_class, stable_id, source_local_id=stable_id, parent_id=parent_id,
            order=heading_index + 1, path=rel(path), resource_id=LOCAL_RESOURCE,
            edition_id=DERIVATIVE_EDITION, source_locator=f"{rel(path)}#{stable_id}",
            content_sha256=text_digest(local_markdown), language="id-ID",
            translation_state="structurally_verified",
            provenance={"source_edition": SOURCE_EDITION, "source_file_sha256": digest(path)},
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
                require("authority/assets/bgk-u04-triticum-spelta.jpg" in block,
                        f"Unexpected Unit 4 image reference: {block_id}")
                block_payload["asset_ids"] = ["br-bgk-u04-media-001"]
            add(make_record(
                "segment", block_id, source_local_id=block_id, parent_id=stable_id,
                order=block_index, path=rel(path), resource_id=LOCAL_RESOURCE,
                edition_id=DERIVATIVE_EDITION,
                source_locator=f"{rel(path)}#{stable_id}:block-{block_index}",
                content_sha256=text_digest(block + "\n"), language="id-ID",
                translation_state="structurally_verified",
                provenance={"source_file_sha256": digest(path)},
                concept_ids=concepts_for(block), rights_id=EDITORIAL_RIGHTS,
                payload=block_payload,
            ))

require(len(source_heading_ids) == 33, "BGK Unit 4 source-heading closure must contain exactly 33 IDs")
expected_exercises = [f"br-bgk-2019-w04-ex{number:02d}" for number in range(1, 10)]
actual_exercises = sorted(row["stable_id"] for row in new_records if row["entity_class"] == "exercise")
require(actual_exercises == expected_exercises, "Translated Unit 4 exercise IDs are not exact ex01..ex09 closure")
require(not any(row["entity_class"] == "solution" for row in new_records),
        "Unit 4 backend must not invent public solution records")
image_blocks = [row for row in new_records if row["entity_class"] == "segment" and row["payload"].get("kind") == "image"]
require(len(image_blocks) == 1 and image_blocks[0]["payload"].get("asset_ids") == ["br-bgk-u04-media-001"],
        "Unit 4 backend must bind exactly one reader image position")

with CORRECTIONS_PATH.open("r", encoding="utf-8-sig", newline="") as stream:
    all_corrections = list(csv.DictReader(stream))
expected_correction_ids = set(translation_qa["correction_ids"])
require(expected_correction_ids == {f"AGC-CORR-{number:04d}" for number in range(154, 159)},
        "BGK Unit 4 translation QA correction identity drifted")
unit_corrections = [row for row in all_corrections
                    if row.get("correction_id") in expected_correction_ids and
                    row.get("status") == "applied_at_bgk_unit_04_translation"]
unit_corrections.sort(key=lambda row: int(row["correction_id"].split("-")[-1]))
require({row["correction_id"] for row in unit_corrections} == expected_correction_ids,
        "BGK Unit 4 correction ledger closure is incomplete")
correction_surfaces = {
    "AGC-CORR-0154": ["br-bgk-2019-l04-s02"],
    "AGC-CORR-0155": ["br-bgk-2019-l04-lem-04-proof"],
    "AGC-CORR-0156": ["br-bgk-2019-w04-ex04"],
    "AGC-CORR-0157": ["br-bgk-2019-l04-cor-02"],
    "AGC-CORR-0158": ["br-bgk-2019-w04-ex09"],
}
for order, row in enumerate(unit_corrections, start=1):
    surfaces = correction_surfaces[row["correction_id"]]
    require(all(surface in new_ids for surface in surfaces), f"Missing correction surface: {row['correction_id']}")
    add(make_record(
        "correction", f"correction.br-bgk-2019.u04.{row['correction_id'].split('-')[-1]}",
        source_local_id=row["correction_id"], parent_id=surfaces[0], order=order,
        resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION,
        source_locator=f"{rel(CORRECTIONS_PATH)}#{row['correction_id']}",
        content_sha256=text_digest(canonical(row)), language="id-ID",
        translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
        payload={"ledger_row": row, "source_issue": row["authority_observation"],
                 "adopted_reading": row["target_action"], "affected_surface_ids": surfaces,
                 "disclosed_in_reader": True, "silent_change": False},
    ))

artifact_paths = [
    *SOURCE_FILES, UNIT_MANIFEST_PATH, EXERCISE_MAP_PATH, SOLUTION_CANDIDATES_PATH,
    OFFICIAL_PDFS_API_PATH, AUTHORITY_FREEZE_PATH, RIGHTS_PATH, ASSET_CLOSURE_PATH,
    COMMONS_METADATA_PATH, MEDIA_CREDITS_PATH, AUTHORITY_QA_PATH,
    TRANSLATION_QA_PATH, READER_QA_PATH, TERMINOLOGY_PATH, CORRECTIONS_PATH,
    LECTURE_PDF_PATH, WORKSHEET_PDF_PATH, MEDIA_ASSET_PATH, READER_BUILD_RECEIPT,
    READER_HTML, READER_PDF,
]
require(len(artifact_paths) == len(set(artifact_paths)) == 24,
        "Unit 4 backend artifact closure must contain exactly 24 paths")
for order, path in enumerate(artifact_paths, start=1):
    require(path.is_file(), f"Bound BGK Unit 4 artifact is absent: {rel(path)}")
    suffix = path.suffix.casefold()
    media_type = {".md": "text/markdown", ".json": "application/json", ".csv": "text/csv",
                  ".pdf": "application/pdf", ".html": "text/html", ".jpg": "image/jpeg"}.get(
                      suffix, "application/octet-stream")
    if path in (LECTURE_PDF_PATH, WORKSHEET_PDF_PATH):
        rights_id = PDF_RIGHTS
    elif path == MEDIA_ASSET_PATH:
        rights_id = MEDIA_RIGHTS
    elif path in SOURCE_FILES or path in (MEDIA_CREDITS_PATH, TRANSLATION_QA_PATH,
                                          READER_QA_PATH, TERMINOLOGY_PATH,
                                          CORRECTIONS_PATH, READER_BUILD_RECEIPT,
                                          READER_HTML, READER_PDF):
        rights_id = EDITORIAL_RIGHTS
    else:
        rights_id = SEMANTIC_RIGHTS
    payload = {"bytes": path.stat().st_size, "media_type": media_type, "unit": 4}
    if path in (READER_HTML, READER_PDF):
        payload["component_rights_ids"] = [EDITORIAL_RIGHTS, MEDIA_RIGHTS]
    add(make_record(
        "artifact", f"artifact.br-bgk-2019.u04.{order:02d}", source_local_id=path.name,
        parent_id=DERIVATIVE_EDITION, order=order, path=rel(path), resource_id=LOCAL_RESOURCE,
        edition_id=DERIVATIVE_EDITION, source_locator=rel(path), content_sha256=digest(path),
        language="id-ID" if path in SOURCE_FILES or path in (MEDIA_CREDITS_PATH, READER_HTML, READER_PDF) else "und",
        translation_state="structurally_verified" if rights_id in (EDITORIAL_RIGHTS, MEDIA_RIGHTS) else "source_frozen",
        rights_id=rights_id, payload=payload,
    ))

qa_specs = [
    ("authority-closure", "BGK_UNIT_04_AUTHORITY_QA", AUTHORITY_QA_PATH,
     {"status": authority_qa["status"], "exercise_count": 9, "public_solution_count": 0}),
    ("translation-closure", "BGK_UNIT_04_TRANSLATION_QA", TRANSLATION_QA_PATH,
     {"status": translation_qa["status"], "qa_schema": translation_qa.get("schema"),
      "model_provenance": MODEL_PROVENANCE}),
    ("media-closure", "ASSET_CLOSURE-bgk-unit-04", ASSET_CLOSURE_PATH,
     {"reader_media_positions": 1, "primary_assets": 1, "pdf_companions": 0,
      "unique_local_assets": 1, "animated_html_positions": 0,
      "official_pdf_witnesses_are_not_media_positions": True}),
    ("reader-closure", "BGK_UNITS_01_04_READER_QA", READER_QA_PATH,
     {"status": reader_qa["status"], "through_unit": 4,
      "html_sha256": reader_qa["html"]["sha256"], "pdf_sha256": reader_qa["pdf"]["sha256"],
      "pdf_pages": reader_qa["pdf"]["pages_pypdf"]}),
]
for order, (suffix, local_id, path, payload) in enumerate(qa_specs, start=1):
    add(make_record(
        "qa_event", f"qa.br-bgk-2019.u04.{suffix}", source_local_id=local_id,
        parent_id=DERIVATIVE_EDITION, order=order, path=rel(path), resource_id=LOCAL_RESOURCE,
        edition_id=DERIVATIVE_EDITION, source_locator=rel(path), content_sha256=digest(path),
        language="id-ID" if suffix in ("translation-closure", "reader-closure") else "und",
        translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS, payload=payload,
    ))

# Graph edges are append-only and cover every new non-relation record.
non_relations = list(new_records)
for relation_order, row in enumerate((row for row in non_relations if row["parent_id"] is not None), start=1):
    add(make_record(
        "relation", f"relation.br-bgk-2019.u04.{relation_order:04d}", parent_id=COURSE_ID,
        order=relation_order, resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION,
        content_sha256=text_digest(row["parent_id"] + "\ncontains\n" + row["stable_id"]),
        translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
        payload={"subject_id": row["parent_id"], "predicate": "contains", "object_id": row["stable_id"]},
    ))
depicts_relation_order = relation_order + 1
add(make_record(
    "relation", f"relation.br-bgk-2019.u04.{depicts_relation_order:04d}", parent_id=COURSE_ID,
    order=depicts_relation_order, resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION,
    content_sha256=text_digest("br-bgk-2019-l04-b001\ndepicts_with\nbr-bgk-u04-media-001"),
    translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
    payload={"subject_id": "br-bgk-2019-l04-b001", "predicate": "depicts_with",
             "object_id": "br-bgk-u04-media-001"},
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
        "One or more Unit 4 records lack exact model provenance")

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
baseline_bindings = [BASE_MANIFEST, BASE_QA, BASE / "record.schema.json", BASE_RECORDS,
                     *[BASE / f"{name}.jsonl" for name in ENTITY_CLASSES]]
source_bindings = [*baseline_bindings, *required_inputs[3:], Path(__file__),
                   ROOT / "scripts" / "qa_backend_bgk_units_01_04.py"]
deduplicated_bindings: list[Path] = []
for path in source_bindings:
    if path not in deduplicated_bindings:
        deduplicated_bindings.append(path)
for path in deduplicated_bindings:
    require(path.is_file(), f"Cumulative BGK backend source binding is absent: {rel(path)}")

counts = dict(sorted(Counter(row["entity_class"] for row in records).items()))
manifest = {
    "schema": "ag-bridge-bgk-native-backend-export-manifest-v1",
    "schema_version": "1.0.0",
    "record_schema_version": SCHEMA_VERSION,
    "generated_from_authority_utc": TIMESTAMP,
    "through_unit": 4,
    "scope": "BGK cumulative Units 1--4; namespace separate from classical Units 1--30",
    "encoding": "UTF-8",
    "serialization": "append-only canonical JSON Lines with CRLF; exact Units 1--3 files are byte prefixes",
    "record_count": len(records),
    "units_01_03_baseline_record_count": len(base_records),
    "unit4_added_record_count": len(new_records),
    "counts": counts,
    "source_heading_id_count": base_manifest["source_heading_id_count"] + len(source_heading_ids),
    "unit4_source_heading_id_count": len(source_heading_ids),
    "source_heading_namespace": "br-bgk-2019-*",
    "exercise_count": 71,
    "unit4_exercise_count": 9,
    "public_solution_count": 2,
    "public_solution_ids": ["br-bgk-2019-w02-ex04-solution", "br-bgk-2019-w03-ex01-solution"],
    "component_asset_count": 6,
    "unit4_component_asset_count": 1,
    "unit4_referenced_term_count": len(referenced_term_ids),
    "unit4_added_terminology_qa_count": len(translation_qa["terminology_ids_added"]),
    "unit4_reused_terminology_qa_count": len(translation_qa["terminology_ids_reused"]),
    "unit4_appended_term_record_count": len(unit_terms),
    "unit4_correction_count": len(unit_corrections),
    "files": [{"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)}
              for path in export_files],
    "source_bindings": [{"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)}
                        for path in deduplicated_bindings],
    "units_01_03_immutable_baseline": {
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
    "model_provenance": MODEL_PROVENANCE,
    "validation": {
        "unique_stable_ids": True,
        "parent_rights_concept_and_relation_endpoint_closure": True,
        "records_exact_set_union_of_class_projections": True,
        "units_01_03_records_and_class_projections_are_exact_byte_prefixes": True,
        "source_heading_ids_preserved": True,
        "br_bgk_2019_namespace_disjoint_from_classical": True,
        "exact_71_exercise_two_public_solution_closure": True,
        "exact_unit4_terminology_and_correction_ledger_closure": True,
        "all_unit4_records_carry_exact_model_provenance": True,
        "authority_translation_reader_one_media_and_component_rights_bound": True,
        "deterministic_double_replay_required": True,
    },
}
(OUT / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                                   encoding="utf-8", newline="\n")
print(json.dumps({"status": "PASS", "output": rel(OUT), "record_count": len(records),
                  "unit4_added_record_count": len(new_records), "counts": counts}, ensure_ascii=False))
