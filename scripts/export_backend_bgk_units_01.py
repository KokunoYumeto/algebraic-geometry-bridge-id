#!/usr/bin/env python3
"""Export the deterministic native backend for BGK Unit 1.

This is a deliberately separate namespace from the completed
``backend/units-01-30`` classical-course backend.  It binds the frozen
Wikiversity authority, the four Indonesian source documents, the exact
exercise/solution closure, and the component media rights into the same
strong native record contract used by the classical reader.
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
OUT = ROOT / "backend" / "bgk-units-01"
SCHEMA_NAME = "ag-bridge-backend-record"
SCHEMA_VERSION = "1.0.0"
WORKFLOW_ID = "workflow.o016-d100.algebraic-geometry-bridge-id"
PROGRAM_ID = "program.br-bgk-2019.id"
COURSE_ID = "course.o016-d100.bgk-bridge"
SOURCE_RESOURCE = "resource.brenner.bgk.wikiversity.2019-2020"
PDF_RESOURCE = "resource.brenner.bgk.official-pdf-witnesses"
LOCAL_RESOURCE = "resource.bgk-id.editorial-layer"
SOURCE_EDITION = "edition.brenner.bgk.unit-01.freeze-2026-08-28"
DERIVATIVE_EDITION = "edition.bgk-id.units-01.2026-08-28"
SEMANTIC_RIGHTS = "rights.bgk-semantic-text.cc-by-sa-4.0"
PDF_RIGHTS = "rights.bgk-official-pdf.component-notices-3.0-and-4.0"
EDITORIAL_RIGHTS = "rights.bgk-id.derivative.cc-by-sa-4.0"
ASSET_RIGHTS = "rights.bgk.tangent-bundle.public-domain"
MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."

SOURCE_DIR = ROOT / "source" / "id-ID" / "bgk"
SOURCE_FILES = [
    SOURCE_DIR / "frontmatter-bgk-units-01.md",
    SOURCE_DIR / "lecture-01.md",
    SOURCE_DIR / "worksheet-01.md",
    SOURCE_DIR / "worksheet-01-solutions.md",
]
COURSE_MANIFEST_PATH = ROOT / "authority" / "wikiversity-bgk" / "course" / "COURSE_AUTHORITY_MANIFEST.json"
UNIT_MANIFEST_PATH = ROOT / "authority" / "wikiversity-bgk" / "unit-01" / "UNIT_AUTHORITY_MANIFEST.json"
EXERCISE_MAP_PATH = ROOT / "authority" / "wikiversity-bgk" / "unit-01" / "ORDERED_EXERCISE_MAP.json"
RIGHTS_PATH = ROOT / "authority" / "RIGHTS-bgk-unit-01.csv"
ASSET_CLOSURE_PATH = ROOT / "authority" / "ASSET_CLOSURE-bgk-unit-01.json"
AUTHORITY_QA_PATH = ROOT / "qa" / "BGK_UNIT_01_AUTHORITY_QA.json"
COURSE_QA_PATH = ROOT / "qa" / "BGK_COURSE_AUTHORITY_QA.json"
CLASSICAL_RECORDS = ROOT / "backend" / "units-01-30" / "records.jsonl"
TERMINOLOGY_PATH = ROOT / "00_control" / "TERMINOLOGY.csv"
CORRECTIONS_PATH = ROOT / "00_control" / "CORRECTIONS.csv"

ENTITY_CLASSES = [
    "artifact",
    "asset",
    "concept",
    "correction",
    "course",
    "edition",
    "exercise",
    "program",
    "qa_event",
    "relation",
    "resource",
    "rights",
    "segment",
    "solution",
    "term",
    "unit",
]


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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


for required in [
    *SOURCE_FILES,
    COURSE_MANIFEST_PATH,
    UNIT_MANIFEST_PATH,
    EXERCISE_MAP_PATH,
    RIGHTS_PATH,
    ASSET_CLOSURE_PATH,
    AUTHORITY_QA_PATH,
    COURSE_QA_PATH,
    CLASSICAL_RECORDS,
    TERMINOLOGY_PATH,
    CORRECTIONS_PATH,
]:
    require(required.is_file(), f"Required BGK backend input is absent: {rel(required)}")

course_manifest = read_json(COURSE_MANIFEST_PATH)
unit_manifest = read_json(UNIT_MANIFEST_PATH)
exercise_map = read_json(EXERCISE_MAP_PATH)
asset_closure = read_json(ASSET_CLOSURE_PATH)
authority_qa = read_json(AUTHORITY_QA_PATH)
course_qa = read_json(COURSE_QA_PATH)
require(unit_manifest.get("unit_number") == 1, "BGK Unit 1 authority identity mismatch")
require(exercise_map.get("unit") == 1, "BGK exercise-map identity mismatch")
require(exercise_map.get("exercise_count") == 17, "BGK Unit 1 must contain exactly 17 exercises")
require(exercise_map.get("solution_count") == 0, "BGK Unit 1 unexpectedly exposes public solutions")
require(all(not row.get("has_public_solution") for row in exercise_map["entries"]), "BGK solution closure is not negative")
require(asset_closure.get("unit") == 1 and asset_closure.get("unique_local_assets") == 1, "BGK Unit 1 asset closure mismatch")
require(authority_qa.get("status") == "PASS" and course_qa.get("status") == "PASS", "Frozen BGK authority QA is not PASS")
TIMESTAMP = unit_manifest["frozen_utc"]

with RIGHTS_PATH.open("r", encoding="utf-8-sig", newline="") as stream:
    rights_rows = list(csv.DictReader(stream))
require(len(rights_rows) == 1, "BGK Unit 1 must have exactly one component-rights row")
rights_row = rights_rows[0]
asset_rows = asset_closure["assets"]
require(len(asset_rows) == 1, "BGK Unit 1 must have exactly one frozen media asset")
asset_row = asset_rows[0]
asset_path = ROOT / rights_row["local_path"]
require(asset_path.is_file(), "Frozen BGK media asset is absent")
require(asset_path.stat().st_size == int(rights_row["local_bytes"]), "Frozen BGK media byte count drifted")
require(digest(asset_path) == rights_row["local_sha256"] == asset_row["local_sha256"], "Frozen BGK media hash drifted")
require(rights_row["asset_id"] == asset_row["asset_id"] == "br-bgk-u01-media-001", "BGK asset ID drifted")
with TERMINOLOGY_PATH.open("r", encoding="utf-8-sig", newline="") as stream:
    bgk_term_rows = [row for row in csv.DictReader(stream) if row.get("scope") == "BGK" and row.get("status") == "admitted"]
require([row["term_id"] for row in bgk_term_rows] == [f"AGT-{number:04d}" for number in range(277, 290)],
        "BGK Unit 1 terminology ledger closure is not AGT-0277..AGT-0289")
with CORRECTIONS_PATH.open("r", encoding="utf-8-sig", newline="") as stream:
    correction_ledger = {row["correction_id"]: row for row in csv.DictReader(stream) if row.get("correction_id")}
require(all(f"AGC-CORR-{number:04d}" in correction_ledger for number in range(136, 142)),
        "BGK Unit 1 correction ledger closure is not AGC-CORR-0136..0141")


def record_schema() -> dict[str, Any]:
    nullable_string = {"type": ["string", "null"]}
    nullable_integer = {"type": ["integer", "null"]}
    required = [
        "schema", "schema_version", "entity_class", "stable_id", "source_local_id",
        "parent_id", "order", "path", "resource_id", "edition_id", "source_locator",
        "content_sha256", "language", "translation_state", "provenance", "concept_ids",
        "prerequisite_ids", "rights_id", "status", "timestamp", "responsible_workflow",
        "supersedes", "payload",
    ]
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://example.invalid/algebraic-geometry-bridge/bgk-backend-record-units-01-v1.schema.json",
        "title": "BGK Indonesian native backend record through Unit 1",
        "type": "object",
        "additionalProperties": False,
        "required": required,
        "properties": {
            "schema": {"const": SCHEMA_NAME},
            "schema_version": {"const": SCHEMA_VERSION},
            "entity_class": {"enum": ENTITY_CLASSES},
            "stable_id": {"type": "string", "minLength": 1},
            "source_local_id": nullable_string,
            "parent_id": nullable_string,
            "order": nullable_integer,
            "path": nullable_string,
            "resource_id": nullable_string,
            "edition_id": nullable_string,
            "source_locator": nullable_string,
            "content_sha256": {"type": ["string", "null"], "pattern": "^[0-9a-f]{64}$"},
            "language": {"type": "string"},
            "translation_state": {"enum": [
                "source_frozen", "queued", "draft", "translated", "structurally_verified",
                "mathematically_reviewed", "language_reviewed", "built", "visually_checked",
                "published", "superseded", "blocked",
            ]},
            "provenance": {"type": "object"},
            "concept_ids": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
            "prerequisite_ids": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
            "rights_id": nullable_string,
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "responsible_workflow": {"type": "string"},
            "supersedes": nullable_string,
            "payload": {"type": "object"},
        },
    }


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
        "provenance": provenance or {},
        "concept_ids": sorted(set(concept_ids or [])),
        "prerequisite_ids": sorted(set(prerequisite_ids or [])),
        "rights_id": rights_id,
        "status": status,
        "timestamp": TIMESTAMP,
        "responsible_workflow": WORKFLOW_ID,
        "supersedes": supersedes,
        "payload": payload or {},
    }


records: list[dict[str, Any]] = []


def add(row: dict[str, Any]) -> None:
    records.append(row)


add(make_record(
    "program", PROGRAM_ID, source_local_id="curriculum-v0-id", order=16, path="O016/D100",
    resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION, language="id-ID",
    translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
    payload={"role": "D100", "title": "Program matematika Bahasa Indonesia", "curriculum_admission_separate": True},
))
add(make_record(
    "course", COURSE_ID, source_local_id="O016/D100-BGK", parent_id=PROGRAM_ID, order=16,
    path="O016/D100/BGK", resource_id=SOURCE_RESOURCE, edition_id=DERIVATIVE_EDITION,
    source_locator=rel(COURSE_MANIFEST_PATH), content_sha256=digest(COURSE_MANIFEST_PATH),
    language="id-ID", translation_state="structurally_verified", rights_id=SEMANTIC_RIGHTS,
    prerequisite_ids=["concept.br-bgk-2019.linear-algebra", "concept.br-bgk-2019.general-topology"],
    payload={
        "title": "Bundel, Berkas, dan Kohomologi",
        "source_title": "Bündel, Garben und Kohomologie (Osnabrück 2019-2020)",
        "creator": "Holger Brenner", "source_unit_count": 30, "backend_through_unit": 1,
        "non_endorsement": True,
    },
))

add(make_record(
    "resource", SOURCE_RESOURCE, source_local_id=unit_manifest["source_identity"]["course_title"],
    parent_id=COURSE_ID, source_locator="https://de.wikiversity.org/wiki/Kurs:B%C3%BCndel,_Garben_und_Kohomologie_(Osnabr%C3%BCck_2019-2020)",
    content_sha256=digest(COURSE_MANIFEST_PATH), language="de", rights_id=SEMANTIC_RIGHTS,
    payload={"title": "Bündel, Garben und Kohomologie (Osnabrück 2019-2020)", "creator": "Holger Brenner", "host": "German Wikiversity", "semantic_units": 30},
))
add(make_record(
    "resource", PDF_RESOURCE, source_local_id="official-pdf-witnesses", parent_id=COURSE_ID,
    source_locator=rel(UNIT_MANIFEST_PATH), content_sha256=digest(UNIT_MANIFEST_PATH), language="de",
    rights_id=PDF_RIGHTS, payload={"role": "visual and numbering witnesses, not semantic authority", "component_notice_discrepancy_preserved": True},
))
add(make_record(
    "resource", LOCAL_RESOURCE, source_local_id="bgk-id", parent_id=COURSE_ID,
    source_locator=rel(SOURCE_FILES[0]), content_sha256=digest(SOURCE_FILES[0]), language="id-ID",
    translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
    payload={"title": "Bundel, Berkas, dan Kohomologi - edisi Bahasa Indonesia", "relationship": "independent translation and reader", "non_endorsement": True, "model_provenance": MODEL_PROVENANCE},
))

add(make_record(
    "edition", SOURCE_EDITION, source_local_id="bgk-unit-01-authority-freeze", parent_id=SOURCE_RESOURCE,
    resource_id=SOURCE_RESOURCE, edition_id=SOURCE_EDITION, source_locator=rel(UNIT_MANIFEST_PATH),
    content_sha256=digest(UNIT_MANIFEST_PATH), language="de", rights_id=SEMANTIC_RIGHTS,
    payload={
        "unit": 1, "lecture_pageid": unit_manifest["lecture"]["pageid"], "lecture_revid": unit_manifest["lecture"]["revid"],
        "worksheet_pageid": unit_manifest["worksheet"]["pageid"], "worksheet_revid": unit_manifest["worksheet"]["revid"],
        "exercise_count": 17, "public_solution_count": 0,
    },
))
add(make_record(
    "edition", DERIVATIVE_EDITION, source_local_id="bgk-id-units-01", parent_id=LOCAL_RESOURCE,
    resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION, source_locator=rel(SOURCE_FILES[0]),
    content_sha256=digest(SOURCE_FILES[0]), language="id-ID", translation_state="structurally_verified",
    rights_id=EDITORIAL_RIGHTS, payload={"through_unit": 1, "source_edition": SOURCE_EDITION, "status": "complete source translation; pre-reader-publication backend", "model_provenance": MODEL_PROVENANCE},
))

for rights_id, parent, title, license_name, payload in [
    (SEMANTIC_RIGHTS, SOURCE_RESOURCE, "Frozen semantic course text", "CC BY-SA 4.0", {"url": "https://creativecommons.org/licenses/by-sa/4.0/", "attribution_required": True, "share_alike": True}),
    (PDF_RIGHTS, PDF_RESOURCE, "Official PDF witness notices", "component notices preserved", {"current_commons_metadata": "CC BY-SA 4.0", "embedded_pdf_notice": "CC BY-SA 3.0", "blanket_relicensing_claim": False}),
    (EDITORIAL_RIGHTS, LOCAL_RESOURCE, "Indonesian translation and editorial layer", "CC BY-SA 4.0", {"url": "https://creativecommons.org/licenses/by-sa/4.0/", "attribution_required": True, "share_alike": True}),
    (ASSET_RIGHTS, SOURCE_RESOURCE, "Tangent_bundle.svg component", "Public domain", {"commons_template": "{{PD-self}}", "attribution_required": False, "source_inline_label": rights_row["source_course_inline_license_label"]}),
]:
    add(make_record("rights", rights_id, parent_id=parent, resource_id=parent, edition_id=DERIVATIVE_EDITION,
                    source_locator=rel(RIGHTS_PATH), content_sha256=digest(RIGHTS_PATH), rights_id=rights_id,
                    payload={"title": title, "license": license_name, **payload}))

concept_specs = {
    "linear-algebra": ("aljabar linear", ["persamaan linear", "eliminasi Gauss", "ruang penyelesaian"]),
    "general-topology": ("topologi umum", ["ruang topologis", "Hausdorff", "homeomorf"]),
    "parameter-dependent-systems": ("sistem linear bergantung parameter", ["bergantung pada parameter", "ruang parameter"]),
    "vector-bundle": ("bundel vektor", ["bundel vektor", "ruang total", "ruang basis"]),
    "local-trivialization": ("trivialisasi lokal", ["trivialisasi", "penutup terbuka"]),
    "bundle-morphism": ("homomorfisme bundel", ["homomorfisme bundel", "isomorfisme bundel"]),
    "tangent-bundle": ("bundel tangen", ["bundel tangen", "ruang tangen"]),
    "manifold": ("manifold terdiferensial", ["manifold", "bagan"]),
    "total-differential": ("diferensial total", ["diferensial total", "pemetaan tangen"]),
    "cross-product": ("hasil kali silang", ["hasil kali silang"]),
}
concept_ids_by_key: dict[str, str] = {}
for order, (key, (label, keywords)) in enumerate(concept_specs.items(), start=1):
    concept_id = f"concept.br-bgk-2019.{key}"
    concept_ids_by_key[key] = concept_id
    add(make_record("concept", concept_id, source_local_id=key, parent_id=COURSE_ID, order=order,
                    resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION, language="id-ID",
                    translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
                    payload={"preferred_label": label, "matching_keywords": keywords}))


def concepts_for(text: str) -> list[str]:
    lowered = text.casefold()
    return [concept_ids_by_key[key] for key, (_, keywords) in concept_specs.items() if any(word.casefold() in lowered for word in keywords)]


for order, ledger_row in enumerate(bgk_term_rows, start=1):
    bound_concepts = concepts_for(ledger_row["preferred_target"] + " " + ledger_row["source_term"])
    parent_id = bound_concepts[0] if bound_concepts else COURSE_ID
    add(make_record(
        "term", f"term.br-bgk-2019.{ledger_row['term_id'].casefold()}",
        source_local_id=ledger_row["term_id"], parent_id=parent_id, order=order,
        resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION,
        source_locator=f"{rel(TERMINOLOGY_PATH)}#{ledger_row['term_id']}",
        content_sha256=text_digest(canonical(ledger_row)), language="id-ID",
        translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
        concept_ids=bound_concepts,
        payload={"ledger_row": ledger_row, "scope": "BGK Unit 1"},
    ))


heading_re = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]+\{#([^}]+)\}[ \t]*$", re.MULTILINE)
yaml_id_re = re.compile(r"^stable_id:[ \t]*['\"]?([^'\"\r\n]+)", re.MULTILINE)
exercise_by_number = {int(row["exercise_number"]): row for row in exercise_map["entries"]}
source_heading_ids: list[str] = []
source_doc_roots: dict[str, str] = {}
image_segment_id: str | None = None


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
        require(yaml_match.group(1).strip() == headings[0].group(3), f"YAML/top-heading stable ID mismatch in {rel(path)}")
    source_doc_roots[rel(path)] = headings[0].group(3)
    stack: list[tuple[int, str]] = []
    for heading_index, match in enumerate(headings):
        level = len(match.group(1))
        title = match.group(2).strip()
        stable_id = match.group(3).strip()
        require(stable_id.startswith("br-bgk-2019-"), f"Non-BGK stable heading ID in {rel(path)}: {stable_id}")
        require(stable_id not in source_heading_ids, f"Duplicate BGK source stable ID: {stable_id}")
        source_heading_ids.append(stable_id)
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent_id = stack[-1][1] if stack else DERIVATIVE_EDITION
        stack.append((level, stable_id))
        local_end = headings[heading_index + 1].start() if heading_index + 1 < len(headings) else len(body)
        local_markdown = body[match.start():local_end].strip() + "\n"
        body_start = match.end()
        local_body = body[body_start:local_end].strip()
        exercise_match = re.search(r"-ex(\d{2})$", stable_id)
        if level == 1:
            entity_class = "unit"
        elif exercise_match:
            entity_class = "exercise"
        else:
            entity_class = "segment"
        payload: dict[str, Any] = {
            "title": title,
            "heading_level": level,
            "document_order": source_order,
            "local_markdown": local_markdown,
            "inline_math_delimiter_count": len(re.findall(r"(?<!\$)\$(?!\$)", local_markdown)),
            "display_math_block_count": len(re.findall(r"\$\$(.*?)\$\$", local_markdown, re.DOTALL)),
        }
        if entity_class == "exercise":
            number = int(exercise_match.group(1))
            mapped = exercise_by_number.get(number)
            require(mapped is not None, f"Exercise {number} absent from the frozen exercise map")
            payload.update({
                "exercise_number": number,
                "source_entity": mapped["exercise_title"],
                "source_solution_title": mapped["solution_title"],
                "has_public_solution": mapped["has_public_solution"],
                "prompt_markdown": local_body,
            })
        add(make_record(
            entity_class, stable_id, source_local_id=stable_id, parent_id=parent_id,
            order=heading_index + 1, path=rel(path), resource_id=LOCAL_RESOURCE,
            edition_id=DERIVATIVE_EDITION, source_locator=f"{rel(path)}#{stable_id}",
            content_sha256=text_digest(local_markdown), language="id-ID",
            translation_state="structurally_verified", provenance={
                "source_edition": SOURCE_EDITION, "model": MODEL_PROVENANCE,
                "source_file_sha256": digest(path),
            }, concept_ids=concepts_for(title + "\n" + local_body), rights_id=EDITORIAL_RIGHTS,
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
                require("authority/assets/bgk-tangent-bundle-500.png" in block, "Unexpected BGK Unit 1 image target")
                block_payload["asset_id"] = rights_row["asset_id"]
                image_segment_id = block_id
            add(make_record(
                "segment", block_id, source_local_id=block_id, parent_id=stable_id,
                order=block_index, path=rel(path), resource_id=LOCAL_RESOURCE,
                edition_id=DERIVATIVE_EDITION, source_locator=f"{rel(path)}#{stable_id}:block-{block_index}",
                content_sha256=text_digest(block + "\n"), language="id-ID",
                translation_state="structurally_verified", provenance={"source_file_sha256": digest(path)},
                concept_ids=concepts_for(block), rights_id=EDITORIAL_RIGHTS, payload=block_payload,
            ))

expected_exercise_ids = [f"br-bgk-2019-w01-ex{number:02d}" for number in range(1, 18)]
actual_exercise_ids = sorted(row["stable_id"] for row in records if row["entity_class"] == "exercise")
require(actual_exercise_ids == expected_exercise_ids, "Translated exercise ID closure is not exactly br-bgk-2019-w01-ex01..ex17")
require(image_segment_id is not None, "BGK tangent-bundle image is not represented in source blocks")
require(not any(row["entity_class"] == "solution" for row in records), "A solution record was invented despite zero source solutions")

add(make_record(
    "asset", rights_row["asset_id"], source_local_id=rights_row["resource_title"], parent_id=SOURCE_RESOURCE,
    order=1, path=rights_row["local_path"], resource_id=SOURCE_RESOURCE, edition_id=SOURCE_EDITION,
    source_locator=rights_row["description_url"], content_sha256=rights_row["local_sha256"], rights_id=ASSET_RIGHTS,
    payload={
        "repository": rights_row["repository"], "caption": rights_row["reader_caption_id"], "alt": rights_row["reader_alt_id"],
        "bytes": int(rights_row["local_bytes"]), "width": int(rights_row["local_width"]), "height": int(rights_row["local_height"]),
        "mime": rights_row["mime"], "license": rights_row["license_short"],
        "thumbnail_dimension_discrepancy": rights_row["thumbnail_dimension_discrepancy"],
    },
))

correction_specs = [
    ("0136", "br-bgk-2019-l01-exa-01", "Ruang serat di atas titik nol dicetak dengan urutan faktor yang salah.", "{(0,0)}\\times\\mathbb R^2"),
    ("0137", "br-bgk-2019-l01-exa-01", "Prosa sumber mengulang hasil kali tersebut sebagai ruang basis, bertentangan dengan domain bijeksi.", "\\mathbb R^2\\setminus\\{(0,0)\\}"),
    ("0138", "br-bgk-2019-l01-exa-03", "Vektor syarat kedua memakai nama koordinat (e,f,g) yang tidak cocok dengan sistem.", "(d,e,f)"),
    ("0139", "br-bgk-2019-l01-exa-03", "Komponen tengah hasil kali silang sumber adalah -af+ce.", "-af+cd"),
    ("0140", "br-bgk-2019-l01-def-01", "Diagram sumber memakai R^n sementara definisi menetapkan rank r.", "R^r"),
    ("0141", "br-bgk-2019-l01-exa-02", "Titik nol dan cakupan hasil kali dicetak tanpa tanda kurung tuple dan cakupan hasil kali yang tegas.", "(\\mathbb R^3\\setminus\\{(0,0,0)\\})\\times\\mathbb R^3"),
]
record_ids_now = {row["stable_id"] for row in records}
for order, (ledger_number, parent, issue, adopted) in enumerate(correction_specs, start=1):
    require(parent in record_ids_now, f"Correction parent is absent: {parent}")
    ledger_id = f"AGC-CORR-{ledger_number}"
    ledger_row = correction_ledger[ledger_id]
    add(make_record(
        "correction", f"correction.br-bgk-2019.u01.{ledger_number}", source_local_id=ledger_id,
        parent_id=parent, order=order, resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION,
        source_locator=f"{rel(CORRECTIONS_PATH)}#{ledger_id}", content_sha256=text_digest(canonical(ledger_row)),
        language="id-ID", translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
        payload={"source_issue": issue, "adopted_reading": adopted, "ledger_row": ledger_row, "disclosed_in_reader": True, "silent_change": False},
    ))

artifact_paths = [
    *SOURCE_FILES, COURSE_MANIFEST_PATH, UNIT_MANIFEST_PATH, EXERCISE_MAP_PATH, RIGHTS_PATH,
    ASSET_CLOSURE_PATH, AUTHORITY_QA_PATH, COURSE_QA_PATH,
    TERMINOLOGY_PATH, CORRECTIONS_PATH,
    ROOT / "authority" / "artifacts" / "bgk-lecture-01-official.pdf",
    ROOT / "authority" / "artifacts" / "bgk-worksheet-01-official.pdf",
]
for order, path in enumerate(artifact_paths, start=1):
    require(path.is_file(), f"Bound BGK artifact is absent: {rel(path)}")
    suffix = path.suffix.casefold()
    media_type = {".md": "text/markdown", ".json": "application/json", ".csv": "text/csv", ".pdf": "application/pdf"}.get(suffix, "application/octet-stream")
    rights_id = PDF_RIGHTS if suffix == ".pdf" else (EDITORIAL_RIGHTS if path in SOURCE_FILES else SEMANTIC_RIGHTS)
    add(make_record(
        "artifact", f"artifact.br-bgk-2019.u01.{order:02d}", source_local_id=path.name,
        parent_id=DERIVATIVE_EDITION, order=order, path=rel(path), resource_id=LOCAL_RESOURCE,
        edition_id=DERIVATIVE_EDITION, source_locator=rel(path), content_sha256=digest(path),
        language="id-ID" if path in SOURCE_FILES else "und",
        translation_state="structurally_verified" if path in SOURCE_FILES else "source_frozen",
        rights_id=rights_id, payload={"bytes": path.stat().st_size, "media_type": media_type},
    ))

add(make_record(
    "qa_event", "qa.br-bgk-2019.u01.authority-closure", source_local_id="BGK_UNIT_01_AUTHORITY_QA",
    parent_id=DERIVATIVE_EDITION, order=1, path=rel(AUTHORITY_QA_PATH), resource_id=LOCAL_RESOURCE,
    edition_id=DERIVATIVE_EDITION, source_locator=rel(AUTHORITY_QA_PATH), content_sha256=digest(AUTHORITY_QA_PATH),
    translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
    payload={"status": "PASS", "exercise_count": 17, "public_solution_count": 0, "asset_count": 1},
))

# Materialize explicit graph edges after all content entities exist.  Relation
# records themselves are deliberately excluded from this loop, avoiding a
# recursive relation-of-relation graph.
non_relations = list(records)
relation_order = 0
for row in non_relations:
    if row["parent_id"] is None:
        continue
    relation_order += 1
    add(make_record(
        "relation", f"relation.br-bgk-2019.u01.{relation_order:04d}", parent_id=COURSE_ID,
        order=relation_order, resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION,
        content_sha256=text_digest(row["parent_id"] + "\ncontains\n" + row["stable_id"]),
        translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
        payload={"subject_id": row["parent_id"], "predicate": "contains", "object_id": row["stable_id"]},
    ))
relation_order += 1
add(make_record(
    "relation", f"relation.br-bgk-2019.u01.{relation_order:04d}", parent_id=COURSE_ID,
    order=relation_order, resource_id=LOCAL_RESOURCE, edition_id=DERIVATIVE_EDITION,
    content_sha256=text_digest(image_segment_id + "\ndepicts-with\n" + rights_row["asset_id"]),
    translation_state="structurally_verified", rights_id=EDITORIAL_RIGHTS,
    payload={"subject_id": image_segment_id, "predicate": "depicts_with", "object_id": rights_row["asset_id"]},
))

ids = [row["stable_id"] for row in records]
require(len(ids) == len(set(ids)), "Duplicate BGK backend stable ID")
id_set = set(ids)
for row in records:
    require(row["parent_id"] is None or row["parent_id"] in id_set, f"Missing parent for {row['stable_id']}")
    require(all(concept_id in id_set for concept_id in row["concept_ids"]), f"Missing concept binding for {row['stable_id']}")
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
require(all(stable_id.startswith("br-bgk-2019-") for stable_id in source_heading_ids), "Source ID namespace escaped br-bgk-2019-*")

OUT.mkdir(parents=True, exist_ok=True)
schema_path = OUT / "record.schema.json"
schema_path.write_text(json.dumps(record_schema(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

sorted_records = sorted(records, key=lambda row: (row["entity_class"], row["stable_id"]))
by_class: dict[str, list[dict[str, Any]]] = {entity_class: [] for entity_class in ENTITY_CLASSES}
for row in sorted_records:
    by_class[row["entity_class"]].append(row)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    payload = "".join(canonical(row) + "\r\n" for row in rows).encode("utf-8")
    path.write_bytes(payload)


write_jsonl(OUT / "records.jsonl", sorted_records)
for entity_class in ENTITY_CLASSES:
    write_jsonl(OUT / f"{entity_class}.jsonl", by_class[entity_class])

export_files = [schema_path, OUT / "records.jsonl", *[OUT / f"{name}.jsonl" for name in ENTITY_CLASSES]]
source_bindings = [
    *SOURCE_FILES, COURSE_MANIFEST_PATH, UNIT_MANIFEST_PATH, EXERCISE_MAP_PATH, RIGHTS_PATH,
    ASSET_CLOSURE_PATH, AUTHORITY_QA_PATH, COURSE_QA_PATH, asset_path,
    TERMINOLOGY_PATH, CORRECTIONS_PATH,
    ROOT / "authority" / "artifacts" / "bgk-lecture-01-official.pdf",
    ROOT / "authority" / "artifacts" / "bgk-worksheet-01-official.pdf",
    CLASSICAL_RECORDS, Path(__file__), ROOT / "scripts" / "qa_backend_bgk_units_01.py",
]
for path in source_bindings:
    require(path.is_file(), f"Backend source binding is absent: {rel(path)}")

counts = dict(sorted(Counter(row["entity_class"] for row in sorted_records).items()))
manifest = {
    "schema": "ag-bridge-bgk-native-backend-export-manifest-v1",
    "schema_version": "1.0.0",
    "record_schema_version": SCHEMA_VERSION,
    "generated_from_authority_utc": TIMESTAMP,
    "through_unit": 1,
    "scope": "BGK cumulative Unit 1; namespace separate from classical Units 1--30",
    "encoding": "UTF-8",
    "serialization": "canonical JSON Lines: records and keys sorted, compact separators, CRLF",
    "record_count": len(sorted_records),
    "counts": counts,
    "source_heading_id_count": len(source_heading_ids),
    "source_heading_namespace": "br-bgk-2019-*",
    "exercise_count": 17,
    "public_solution_count": 0,
    "component_asset_count": 1,
    "files": [{"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)} for path in export_files],
    "source_bindings": [{"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)} for path in source_bindings],
    "classical_collision_baseline": {
        "path": rel(CLASSICAL_RECORDS), "bytes": CLASSICAL_RECORDS.stat().st_size,
        "sha256": digest(CLASSICAL_RECORDS), "stable_id_count": len(classical_ids), "intersection_count": 0,
    },
    "model_provenance": MODEL_PROVENANCE,
    "validation": {
        "unique_stable_ids": True,
        "parent_rights_concept_and_relation_endpoint_closure": True,
        "source_heading_ids_preserved": True,
        "br_bgk_2019_namespace_disjoint_from_classical": True,
        "exact_17_exercise_zero_solution_closure": True,
        "authority_and_component_rights_bound": True,
        "deterministic_double_replay_required": True,
    },
}
(OUT / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"status": "PASS", "output": rel(OUT), "record_count": len(sorted_records), "counts": counts}, ensure_ascii=False))
