#!/usr/bin/env python3
"""Export the deterministic, locale-aware backend for bounded reader Unit 1."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "backend" / "unit-01"
WORKFLOW_ID = "workflow.o016-d100.algebraic-geometry-bridge-id"
PROGRAM_ID = "program.complete-mathematics-curriculum.id.v0"
COURSE_ID = "course.o016-d100.algebraic-geometry-bridge"
BRENNER_RESOURCE = "resource.brenner.algebraische-kurven.2025-2026"
BRENNER_EDITION = "edition.brenner.algebraische-kurven.prefix-freeze.2026-08-21"
NAPKIN_RESOURCE = "resource.chen.infinitely-large-napkin"
NAPKIN_EDITION = "edition.chen.napkin.e50be9a0"
LOCAL_RESOURCE = "resource.algebraic-geometry-bridge-id.editorial-layer"
DERIVATIVE_EDITION = "edition.algebraic-geometry-bridge-id.unit-01.2026-08-21"
TEXT_RIGHTS = "rights.brenner-course-text.cc-by-sa-4.0"
EDITORIAL_RIGHTS = "rights.derivative-editorial.cc-by-sa-4.0"
NAPKIN_TEXT_RIGHTS = "rights.napkin-text.cc-by-sa-4.0"
NAPKIN_SOURCE_RIGHTS = "rights.napkin-source.gpl-3.0"

SOURCE_FILES = [
    ROOT / "source" / "id-ID" / "frontmatter.md",
    ROOT / "source" / "id-ID" / "lecture-01.md",
    ROOT / "source" / "id-ID" / "worksheet-01.md",
    ROOT / "source" / "id-ID" / "worksheet-01-solutions.md",
    ROOT / "source" / "id-ID" / "media-credits.md",
]

SCHEMA_VERSION = "1.0.0"
BASE_SCHEMA = "ag-bridge-backend-record"
BUILD_RECEIPT = json.loads(
    (ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json").read_text(encoding="utf-8")
)
TIMESTAMP = BUILD_RECEIPT["built_utc"]


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
    return {
        "schema": BASE_SCHEMA,
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


def add(record: dict[str, Any]) -> None:
    records.append(record)


goal_path = ROOT / "00_control" / "CURRENT_GOAL_AND_WORKFLOW.md"
prefix_receipt_path = ROOT / "authority" / "wikiversity" / "COURSE_PREFIX_RECEIPT.json"
prefix_receipt = json.loads(prefix_receipt_path.read_text(encoding="utf-8"))
napkin_freeze_path = ROOT / "authority" / "NAPKIN_PART20_AUTHORITY_FREEZE.md"

add(
    make_record(
        "program",
        PROGRAM_ID,
        source_local_id="curriculum-v0-id",
        order=16,
        path="O016/D100",
        resource_id=LOCAL_RESOURCE,
        edition_id=DERIVATIVE_EDITION,
        source_locator=rel(goal_path),
        content_sha256=digest(goal_path),
        language="id-ID",
        translation_state="built",
        rights_id=EDITORIAL_RIGHTS,
        payload={
            "title": "Kurikulum matematika lengkap — edisi Bahasa Indonesia",
            "curriculum_admission": "separate_pending_decision",
            "lane_output_remains_independently_valuable": True,
        },
    )
)
add(
    make_record(
        "course",
        COURSE_ID,
        source_local_id="O016/D100",
        parent_id=PROGRAM_ID,
        order=16,
        path="O016/D100",
        resource_id=BRENNER_RESOURCE,
        edition_id=DERIVATIVE_EDITION,
        source_locator=rel(goal_path),
        content_sha256=digest(goal_path),
        language="id-ID",
        translation_state="built",
        prerequisite_ids=[
            "concept.abstract-algebra",
            "concept.communtative-algebra-foundations",
            "concept.general-topology-foundations",
        ],
        rights_id=TEXT_RIGHTS,
        payload={
            "role": "Algebraic Geometry Bridge",
            "dominant_spine": "Holger Brenner, Algebraische Kurven (Osnabrück 2025–2026)",
            "bounded_extent": "30 lectures and 30 worksheets, followed by a compact schemes transition",
            "curriculum_admission": "pending_external_selection",
        },
    )
)

add(
    make_record(
        "resource",
        BRENNER_RESOURCE,
        source_local_id="Kurs:Algebraische Kurven (Osnabrück 2025-2026)",
        source_locator="https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)",
        content_sha256=prefix_receipt["capture_sha256"],
        language="de",
        rights_id=TEXT_RIGHTS,
        payload={
            "title": "Algebraische Kurven (Osnabrück 2025–2026)",
            "creator": "Holger Brenner",
            "host": "German Wikiversity",
            "page_count_in_prefix": prefix_receipt["page_count"],
            "course_root": prefix_receipt["course_root"],
            "course_prefix_classes": prefix_receipt["classes"],
        },
    )
)
add(
    make_record(
        "resource",
        NAPKIN_RESOURCE,
        source_local_id="github.com/vEnhance/napkin",
        source_locator="https://github.com/vEnhance/napkin",
        content_sha256=digest(napkin_freeze_path),
        language="en",
        rights_id=NAPKIN_TEXT_RIGHTS,
        payload={
            "title": "An Infinitely Large Napkin",
            "creator": "Evan Chen",
            "use_in_lane": "bounded donor for the compact affine-schemes transition only",
            "component_rights_separated": True,
        },
    )
)
add(
    make_record(
        "resource",
        LOCAL_RESOURCE,
        source_local_id="algebraic-geometry-bridge-id",
        source_locator=rel(ROOT / "source" / "id-ID" / "frontmatter.md"),
        content_sha256=digest(ROOT / "source" / "id-ID" / "frontmatter.md"),
        language="id-ID",
        translation_state="built",
        rights_id=EDITORIAL_RIGHTS,
        payload={
            "title": "Kurva Aljabar — edisi Bahasa Indonesia",
            "relationship": "independent translation, reader, and connective editorial layer",
            "non_endorsement": True,
        },
    )
)

add(
    make_record(
        "edition",
        BRENNER_EDITION,
        source_local_id="course-root-revid-1074230",
        parent_id=BRENNER_RESOURCE,
        resource_id=BRENNER_RESOURCE,
        edition_id=BRENNER_EDITION,
        source_locator=rel(prefix_receipt_path),
        content_sha256=digest(prefix_receipt_path),
        language="de",
        rights_id=TEXT_RIGHTS,
        payload={
            "freeze_date": "2026-08-21",
            "course_root_revid": 1074230,
            "prefix_manifest_sha256": prefix_receipt["manifest_sha256"],
            "current_text_authority": "per-page revisions in the frozen prefix manifest",
            "official_pdf_role": "older visual/build witness, not current text authority",
        },
    )
)
add(
    make_record(
        "edition",
        NAPKIN_EDITION,
        source_local_id="e50be9a0b2b12d080c273619424d0ee13372cc91",
        parent_id=NAPKIN_RESOURCE,
        resource_id=NAPKIN_RESOURCE,
        edition_id=NAPKIN_EDITION,
        source_locator="https://github.com/vEnhance/napkin/tree/e50be9a0b2b12d080c273619424d0ee13372cc91",
        content_sha256="a88cdf86cbb749cd9528074bd1789224725cdbf4439b1e580457dd1db06008d7",
        language="en",
        rights_id=NAPKIN_TEXT_RIGHTS,
        translation_state="source_frozen",
        payload={
            "commit": "e50be9a0b2b12d080c273619424d0ee13372cc91",
            "tree": "023467410bdf924c8fd38ac04009b4c887cbfb5e",
            "part": "Part XX — Algebraic Geometry II: Affine Schemes",
            "whole_tree_build_state": "blocked_on_bounded_windows_baseline",
            "modified_source_rights_id": NAPKIN_SOURCE_RIGHTS,
        },
    )
)
add(
    make_record(
        "edition",
        DERIVATIVE_EDITION,
        source_local_id="unit-01",
        parent_id=LOCAL_RESOURCE,
        resource_id=LOCAL_RESOURCE,
        edition_id=DERIVATIVE_EDITION,
        source_locator=rel(ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json"),
        content_sha256=digest(ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json"),
        language="id-ID",
        translation_state="visually_checked",
        rights_id=EDITORIAL_RIGHTS,
        payload={
            "title": "Kurva Aljabar — Unit 1",
            "source_edition_id": BRENNER_EDITION,
            "translation_change_notice": True,
            "non_endorsement": True,
        },
    )
)

rights_records = [
    make_record(
        "rights",
        TEXT_RIGHTS,
        resource_id=BRENNER_RESOURCE,
        edition_id=BRENNER_EDITION,
        source_locator="https://de.wikiversity.org/wiki/Holger_Brenner/Lizenzerkl%C3%A4rung?oldid=1073083",
        content_sha256=digest(ROOT / "authority" / "wikiversity" / "included-license-api.json"),
        language="de",
        payload={
            "license": "CC BY-SA 4.0",
            "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
            "creator": "Holger Brenner",
            "scope": "course text, all course subpages, and included pages; Commons media excluded",
            "attribution_required": True,
            "share_alike_required": True,
        },
    ),
    make_record(
        "rights",
        EDITORIAL_RIGHTS,
        resource_id=LOCAL_RESOURCE,
        edition_id=DERIVATIVE_EDITION,
        source_locator=rel(ROOT / "source" / "id-ID" / "frontmatter.md"),
        content_sha256=digest(ROOT / "source" / "id-ID" / "frontmatter.md"),
        language="id-ID",
        translation_state="built",
        payload={
            "license": "CC BY-SA 4.0",
            "scope": "translated course text and derivative editorial text; third-party media excluded",
            "change_notice": "Indonesian translation and re-typesetting, 2026",
            "non_endorsement": True,
        },
    ),
    make_record(
        "rights",
        NAPKIN_TEXT_RIGHTS,
        resource_id=NAPKIN_RESOURCE,
        edition_id=NAPKIN_EDITION,
        source_locator="https://github.com/vEnhance/napkin/blob/e50be9a0b2b12d080c273619424d0ee13372cc91/LICENSE.md",
        content_sha256="e77286d2a0ff092119ada1c1b3e239707b86d81aed00917c5e22ade5f19f02a4",
        language="en",
        payload={"license": "CC BY-SA 4.0", "scope": "Napkin text and generated PDF"},
    ),
    make_record(
        "rights",
        NAPKIN_SOURCE_RIGHTS,
        resource_id=NAPKIN_RESOURCE,
        edition_id=NAPKIN_EDITION,
        source_locator="https://github.com/vEnhance/napkin/blob/e50be9a0b2b12d080c273619424d0ee13372cc91/LICENSE.md",
        content_sha256="e77286d2a0ff092119ada1c1b3e239707b86d81aed00917c5e22ade5f19f02a4",
        language="en",
        payload={"license": "GPL-3.0", "scope": "distributed source and modified build source"},
    ),
]
for item in rights_records:
    add(item)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


rights_rows = read_csv(ROOT / "authority" / "RIGHTS.csv")
for row in rights_rows:
    asset_id = row["asset_id"]
    component_rights_id = f"rights.{asset_id}"
    add(
        make_record(
            "rights",
            component_rights_id,
            source_local_id=row["commons_metadata_title"],
            resource_id=BRENNER_RESOURCE,
            edition_id=DERIVATIVE_EDITION,
            source_locator=row["description_url"],
            content_sha256=row["local_sha256"],
            language="und",
            payload={
                "license": row["license_short"],
                "license_url": row["license_url"] or None,
                "usage_terms": row["usage_terms"] or None,
                "creator_or_artist": row["artist"] or row["uploader"],
                "uploader": row["uploader"],
                "attribution_required": row["attribution_required"].lower() == "true",
                "scope": asset_id,
            },
        )
    )
    add(
        make_record(
            "asset",
            asset_id,
            source_local_id=row["resource_title"],
            parent_id="br-ak-2025-2026-l01",
            order=int(row["reader_order"]),
            path=row["local_path"],
            resource_id=BRENNER_RESOURCE,
            edition_id=DERIVATIVE_EDITION,
            source_locator=row["description_url"],
            content_sha256=row["local_sha256"],
            language="und",
            translation_state="built",
            rights_id=component_rights_id,
            payload={
                "caption_id": row["reader_caption_id"],
                "selected_form": row["selected_form"],
                "bytes": int(row["local_bytes"]),
                "width": int(row["local_width"]),
                "height": int(row["local_height"]),
                "mime": row["mime"],
                "source_original_url": row["original_url"],
                "selected_url": row["selected_url"],
                "pdf_companion": (
                    {
                        "path": row["pdf_local_path"],
                        "bytes": int(row["pdf_local_bytes"]),
                        "sha256": row["pdf_local_sha256"],
                        "derivation": row["pdf_companion_source_url"],
                    }
                    if row["pdf_local_path"]
                    else None
                ),
            },
        )
    )


concept_map = {
    "AGT-0001": "concept.algebraic-curve",
    "AGT-0002": "concept.plane-algebraic-curve",
    "AGT-0003": "concept.affine",
    "AGT-0004": "concept.base-field",
    "AGT-0005": "concept.polynomial-ring",
    "AGT-0006": "concept.zero-locus",
    "AGT-0007": "concept.solution-set",
    "AGT-0008": "concept.algebraically-closed-field",
    "AGT-0009": "concept.irreducibility",
    "AGT-0010": "concept.rational-function",
    "AGT-0011": "concept.pole",
    "AGT-0012": "concept.fundamental-theorem-of-algebra",
    "AGT-0013": "concept.scheme",
    "AGT-0014": "concept.affine-scheme",
    "AGT-0015": "concept.structure-sheaf",
    "AGT-0016": "concept.stalk",
    "AGT-0017": "concept.locally-ringed-space",
    "AGT-0018": "concept.gluing-data",
}
term_rows = read_csv(ROOT / "00_control" / "TERMINOLOGY.csv")
for row in term_rows:
    concept_id = concept_map[row["term_id"]]
    add(
        make_record(
            "concept",
            concept_id,
            source_local_id=row["source_term"],
            resource_id=BRENNER_RESOURCE if row["source_language"] == "de" else NAPKIN_RESOURCE,
            edition_id=DERIVATIVE_EDITION,
            source_locator=rel(ROOT / "00_control" / "TERMINOLOGY.csv"),
            content_sha256=text_digest(row["source_term"]),
            language="und",
            translation_state="translated" if row["status"] == "admitted" else "draft",
            rights_id=EDITORIAL_RIGHTS,
            status=row["status"],
            payload={"canonical_label": concept_id.removeprefix("concept.").replace("-", " ")},
        )
    )
    add(
        make_record(
            "term",
            f"term.{row['term_id'].lower()}.id-id",
            source_local_id=row["term_id"],
            parent_id=concept_id,
            resource_id=BRENNER_RESOURCE if row["source_language"] == "de" else NAPKIN_RESOURCE,
            edition_id=DERIVATIVE_EDITION,
            source_locator=rel(ROOT / "00_control" / "TERMINOLOGY.csv"),
            content_sha256=text_digest("\u241f".join(row.values())),
            language="id-ID",
            translation_state="translated" if row["status"] == "admitted" else "draft",
            concept_ids=[concept_id],
            rights_id=EDITORIAL_RIGHTS,
            status=row["status"],
            payload={
                "source_language": row["source_language"],
                "source_term": row["source_term"],
                "preferred_target": row["preferred_target"],
                "rejected_or_variant": row["rejected_or_variant"] or None,
                "scope": row["scope"],
                "rationale": row["rationale"],
            },
        )
    )


heading_re = re.compile(r"^(#{1,6})\s+(.*?)\s+\{#([^}]+)\}\s*$")


def strip_yaml(lines: list[str]) -> tuple[list[str], dict[str, str]]:
    if not lines or lines[0].strip() != "---":
        return lines, {}
    end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            value = match.group(2).strip().strip('"')
            metadata[match.group(1)] = value
    return ["" for _ in range(end + 1)] + lines[end + 1 :], metadata


def classify_unit(identifier: str, title: str) -> str:
    low = title.casefold()
    if "-sol-" in identifier or low.startswith("solusi soal"):
        return "solution"
    if "-w01-ex-" in identifier:
        return "exercise"
    if "-l01-ex-" in identifier:
        return "example"
    if "-def-" in identifier:
        return "definition"
    if "-lem-" in identifier and identifier.endswith("-proof"):
        return "proof"
    if "-lem-" in identifier:
        return "lemma"
    if "-thm-" in identifier and identifier.endswith("-proof"):
        return "proof"
    if "-thm-" in identifier:
        return "theorem"
    if identifier.endswith(("-practice", "-submit")):
        return "exercise_group"
    if identifier == "agc-media-credits":
        return "credits"
    if re.search(r"-s\d+$", identifier) or identifier.startswith("agc-front-"):
        return "section"
    if identifier.endswith(("-l01", "-w01", "-solutions")):
        return "unit"
    return "section"


all_units: list[dict[str, Any]] = []
all_segments: list[dict[str, Any]] = []
unit_regions: dict[str, str] = {}
image_parent_by_path: dict[str, str] = {}
global_unit_order = 0
global_segment_order = 0

for source_path in SOURCE_FILES:
    original_lines = source_path.read_text(encoding="utf-8").splitlines()
    lines, metadata = strip_yaml(original_lines)
    heading_rows: list[tuple[int, int, str, str]] = []
    for index, line in enumerate(lines):
        match = heading_re.match(line)
        if match:
            heading_rows.append((index, len(match.group(1)), match.group(2), match.group(3)))

    stack: list[tuple[int, str]] = []
    file_units: list[dict[str, Any]] = []
    for hpos, (line_index, level, title, identifier) in enumerate(heading_rows):
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent_id = stack[-1][1] if stack else DERIVATIVE_EDITION
        stack.append((level, identifier))
        next_boundary = len(lines)
        for next_index, next_level, _, _ in heading_rows[hpos + 1 :]:
            if next_level <= level:
                next_boundary = next_index
                break
        region = "\n".join(lines[line_index:next_boundary]).strip() + "\n"
        unit_regions[identifier] = region
        global_unit_order += 1
        source_resource = (
            BRENNER_RESOURCE
            if source_path.name in {"lecture-01.md", "worksheet-01.md", "worksheet-01-solutions.md"}
            else LOCAL_RESOURCE
        )
        source_rights = TEXT_RIGHTS if source_resource == BRENNER_RESOURCE else EDITORIAL_RIGHTS
        upstream = {
            key: metadata[key]
            for key in (
                "upstream_title",
                "upstream_pageid",
                "upstream_revid",
                "upstream_timestamp",
                "upstream_mediawiki_sha1",
                "source_url",
            )
            if key in metadata
        }
        concept_ids = [
            concept_map[row["term_id"]]
            for row in term_rows
            if row["preferred_target"].casefold() in region.casefold()
        ]
        unit = make_record(
            "unit",
            identifier,
            source_local_id=metadata.get("upstream_title") if level == 1 else identifier,
            parent_id=parent_id,
            order=global_unit_order,
            path=f"{rel(source_path)}#{identifier}",
            resource_id=source_resource,
            edition_id=DERIVATIVE_EDITION,
            source_locator=f"{rel(source_path)}:{line_index + 1}",
            content_sha256=text_digest(region),
            language="id-ID",
            translation_state="built",
            provenance={
                "source_edition_id": BRENNER_EDITION if source_resource == BRENNER_RESOURCE else None,
                "upstream": upstream,
            },
            concept_ids=concept_ids,
            rights_id=source_rights,
            payload={
                "unit_type": classify_unit(identifier, title),
                "heading_level": level,
                "title_markdown": title,
                "source_file_sha256": digest(source_path),
            },
        )
        add(unit)
        all_units.append(unit)
        file_units.append(unit)

    active_id = DERIVATIVE_EDITION
    segment_counter: defaultdict[str, int] = defaultdict(int)
    block: list[tuple[int, str]] = []

    def flush_block() -> None:
        global global_segment_order, block
        if not block:
            return
        first_line = block[0][0]
        content = "\n".join(line for _, line in block).strip()
        block = []
        if not content or (content.startswith("<!--") and content.endswith("-->")):
            return
        segment_counter[active_id] += 1
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
        source_resource = (
            BRENNER_RESOURCE
            if source_path.name in {"lecture-01.md", "worksheet-01.md", "worksheet-01-solutions.md"}
            else LOCAL_RESOURCE
        )
        concept_ids = [
            concept_map[row["term_id"]]
            for row in term_rows
            if row["preferred_target"].casefold() in content.casefold()
        ]
        segment = make_record(
            "segment",
            segment_id,
            parent_id=active_id,
            order=global_segment_order,
            path=f"{rel(source_path)}:{first_line}",
            resource_id=source_resource,
            edition_id=DERIVATIVE_EDITION,
            source_locator=f"{rel(source_path)}:{first_line}",
            content_sha256=text_digest(content),
            language="id-ID",
            translation_state="built",
            provenance={"source_edition_id": BRENNER_EDITION if source_resource == BRENNER_RESOURCE else None},
            concept_ids=concept_ids,
            rights_id=TEXT_RIGHTS if source_resource == BRENNER_RESOURCE else EDITORIAL_RIGHTS,
            payload={"segment_type": segment_type, "markdown": content},
        )
        add(segment)
        all_segments.append(segment)
        image_match = re.fullmatch(r"!\[[^\]]*\]\(([^)]+)\)", content)
        if image_match:
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


relation_counter = 0


def add_relation(
    relation_type: str,
    subject_id: str,
    object_id: str,
    *,
    source_locator: str,
    payload: dict[str, Any] | None = None,
) -> None:
    global relation_counter
    relation_counter += 1
    add(
        make_record(
            "relation",
            f"relation.unit01.{relation_counter:04d}",
            order=relation_counter,
            resource_id=LOCAL_RESOURCE,
            edition_id=DERIVATIVE_EDITION,
            source_locator=source_locator,
            content_sha256=text_digest(f"{relation_type}\u241f{subject_id}\u241f{object_id}"),
            language="und",
            translation_state="built",
            rights_id=EDITORIAL_RIGHTS,
            payload={
                "relation_type": relation_type,
                "subject_id": subject_id,
                "object_id": object_id,
                **(payload or {}),
            },
        )
    )


add_relation("contains", PROGRAM_ID, COURSE_ID, source_locator=rel(goal_path))
add_relation("depends_on", COURSE_ID, BRENNER_RESOURCE, source_locator=rel(goal_path))
add_relation("depends_on", COURSE_ID, NAPKIN_RESOURCE, source_locator=rel(goal_path), payload={"scope": "later affine-schemes transition only"})
add_relation("translates", DERIVATIVE_EDITION, BRENNER_EDITION, source_locator=rel(ROOT / "source" / "id-ID" / "frontmatter.md"))
for unit in all_units:
    add_relation("contains", unit["parent_id"], unit["stable_id"], source_locator=unit["source_locator"])
    for concept_id in unit["concept_ids"]:
        add_relation("uses_concept", unit["stable_id"], concept_id, source_locator=unit["source_locator"])

for previous, following in zip(all_units, all_units[1:]):
    add_relation("precedes", previous["stable_id"], following["stable_id"], source_locator=following["source_locator"])

for exercise_number in (4, 5, 12, 13, 14, 20, 21):
    add_relation(
        "solves",
        f"br-ak-2025-2026-w01-sol-{exercise_number:02d}",
        f"br-ak-2025-2026-w01-ex-{exercise_number:02d}",
        source_locator=rel(ROOT / "authority" / "wikiversity" / "worksheet-01-solutions" / "ORDERED_EXERCISE_MAP.json"),
    )

for row in rights_rows:
    parent = image_parent_by_path.get(row["local_path"], "br-ak-2025-2026-l01")
    add_relation("illustrates", row["asset_id"], parent, source_locator=row["description_url"])

for term_row in term_rows:
    term_id = f"term.{term_row['term_id'].lower()}.id-id"
    add_relation("translates", term_id, concept_map[term_row["term_id"]], source_locator=rel(ROOT / "00_control" / "TERMINOLOGY.csv"))


for row in read_csv(ROOT / "00_control" / "CORRECTIONS.csv"):
    affected_units = []
    scope = row["scope"]
    if "solution_1_13" in scope:
        affected_units = ["br-ak-2025-2026-w01-sol-13"]
    elif "lecture_1" in scope:
        affected_units = ["br-ak-2025-2026-l01"]
    elif scope in {"pdf_gif_surfaces", "pdf_svg_surface"}:
        affected_units = ["br-ak-2025-2026-l01"]
    correction = make_record(
        "correction",
        f"correction.{row['correction_id'].lower()}",
        source_local_id=row["correction_id"],
        resource_id=BRENNER_RESOURCE,
        edition_id=DERIVATIVE_EDITION,
        source_locator=rel(ROOT / "00_control" / "CORRECTIONS.csv"),
        content_sha256=text_digest("\u241f".join(row.values())),
        language="id-ID",
        translation_state="built",
        provenance={"authority_identity": row["authority_identity"]},
        rights_id=EDITORIAL_RIGHTS,
        status=row["status"],
        payload={
            "kind": row["kind"],
            "scope": scope,
            "authority_observation": row["authority_observation"],
            "target_action": row["target_action"],
            "mathematical_effect": row["mathematical_effect"],
            "affected_unit_ids": affected_units,
            "upstream_report_disposition": "defer_to_single_bounded_post-corpus_report_if_still_material",
        },
    )
    add(correction)
    for affected in affected_units:
        add_relation("corrects" if row["kind"] == "source_precision" else "adapts", correction["stable_id"], affected, source_locator=correction["source_locator"])


machine_qa_path = ROOT / "qa" / "UNIT_01_MACHINE_QA.json"
visual_qa_path = ROOT / "qa" / "UNIT_01_VISUAL_QA.json"
for stable_id, qa_path, qa_kind in (
    ("qa.unit01.machine", machine_qa_path, "source_math_topology_build_accessibility"),
    ("qa.unit01.visual", visual_qa_path, "visual"),
):
    qa = json.loads(qa_path.read_text(encoding="utf-8"))
    add(
        make_record(
            "qa_event",
            stable_id,
            parent_id=DERIVATIVE_EDITION,
            resource_id=LOCAL_RESOURCE,
            edition_id=DERIVATIVE_EDITION,
            source_locator=rel(qa_path),
            content_sha256=digest(qa_path),
            language="und",
            translation_state="visually_checked" if qa_kind == "visual" else "built",
            rights_id=EDITORIAL_RIGHTS,
            status="passed" if qa.get("status", qa.get("result")) == "PASS" else "failed",
            payload={"qa_kind": qa_kind, "result": qa},
        )
    )


artifact_paths = [
    ROOT / "build" / "reader-id" / "index.html",
    ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-unit-01.pdf",
    ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json",
    machine_qa_path,
    visual_qa_path,
    ROOT / "authority" / "RIGHTS.csv",
    ROOT / "authority" / "ASSET_CLOSURE.json",
    prefix_receipt_path,
]
for number, artifact_path in enumerate(artifact_paths, start=1):
    artifact_id = f"artifact.unit01.{number:02d}.{artifact_path.name.casefold().replace('_', '-').replace('.', '-')}"
    add(
        make_record(
            "artifact",
            artifact_id,
            parent_id=DERIVATIVE_EDITION,
            order=number,
            path=rel(artifact_path),
            resource_id=LOCAL_RESOURCE,
            edition_id=DERIVATIVE_EDITION,
            source_locator=rel(artifact_path),
            content_sha256=digest(artifact_path),
            language="id-ID" if artifact_path.suffix in {".html", ".pdf"} else "und",
            translation_state="visually_checked" if artifact_path.suffix in {".html", ".pdf"} else "built",
            rights_id=EDITORIAL_RIGHTS,
            payload={
                "bytes": artifact_path.stat().st_size,
                "media_type": {
                    ".html": "text/html",
                    ".pdf": "application/pdf",
                    ".json": "application/json",
                    ".csv": "text/csv",
                }.get(artifact_path.suffix, "application/octet-stream"),
                "build_receipt": rel(ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json"),
            },
        )
    )


required_classes = {
    "program",
    "course",
    "resource",
    "edition",
    "unit",
    "concept",
    "segment",
    "term",
    "asset",
    "relation",
    "rights",
    "qa_event",
    "artifact",
    "correction",
}

ids = [record["stable_id"] for record in records]
if len(ids) != len(set(ids)):
    duplicates = sorted(stable_id for stable_id, count in Counter(ids).items() if count > 1)
    raise SystemExit(f"Duplicate stable IDs: {duplicates}")

present_classes = {record["entity_class"] for record in records}
if present_classes != required_classes:
    raise SystemExit(f"Entity class closure mismatch: {sorted(required_classes - present_classes)}")

id_set = set(ids)
for record in records:
    if record["parent_id"] and record["parent_id"] not in id_set:
        raise SystemExit(f"Missing parent {record['parent_id']} for {record['stable_id']}")
    for key in (
        "schema",
        "schema_version",
        "entity_class",
        "stable_id",
        "language",
        "translation_state",
        "provenance",
        "concept_ids",
        "prerequisite_ids",
        "status",
        "timestamp",
        "responsible_workflow",
        "payload",
    ):
        if key not in record:
            raise SystemExit(f"Missing {key} in {record['stable_id']}")

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://example.invalid/algebraic-geometry-bridge/backend-record-v1.schema.json",
    "title": "Algebraic Geometry Bridge backend record v1",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema",
        "schema_version",
        "entity_class",
        "stable_id",
        "source_local_id",
        "parent_id",
        "order",
        "path",
        "resource_id",
        "edition_id",
        "source_locator",
        "content_sha256",
        "language",
        "translation_state",
        "provenance",
        "concept_ids",
        "prerequisite_ids",
        "rights_id",
        "status",
        "timestamp",
        "responsible_workflow",
        "supersedes",
        "payload",
    ],
    "properties": {
        "schema": {"const": BASE_SCHEMA},
        "schema_version": {"const": SCHEMA_VERSION},
        "entity_class": {"enum": sorted(required_classes)},
        "stable_id": {"type": "string", "minLength": 1},
        "source_local_id": {"type": ["string", "null"]},
        "parent_id": {"type": ["string", "null"]},
        "order": {"type": ["integer", "null"]},
        "path": {"type": ["string", "null"]},
        "resource_id": {"type": ["string", "null"]},
        "edition_id": {"type": ["string", "null"]},
        "source_locator": {"type": ["string", "null"]},
        "content_sha256": {"type": ["string", "null"], "pattern": "^[0-9a-f]{64}$"},
        "language": {"type": "string"},
        "translation_state": {
            "enum": [
                "source_frozen",
                "queued",
                "draft",
                "translated",
                "structurally_verified",
                "mathematically_reviewed",
                "language_reviewed",
                "built",
                "visually_checked",
                "published",
                "superseded",
                "blocked",
            ]
        },
        "provenance": {"type": "object"},
        "concept_ids": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
        "prerequisite_ids": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
        "rights_id": {"type": ["string", "null"]},
        "status": {"type": "string"},
        "timestamp": {"type": "string"},
        "responsible_workflow": {"type": "string"},
        "supersedes": {"type": ["string", "null"]},
        "payload": {"type": "object"},
    },
}

OUT.mkdir(parents=True, exist_ok=True)
schema_path = OUT / "record.schema.json"
schema_path.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

records_sorted = sorted(records, key=lambda row: (row["entity_class"], row["stable_id"]))
combined_path = OUT / "records.jsonl"
combined_path.write_text(
    "".join(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for record in records_sorted),
    encoding="utf-8",
)

class_paths: list[Path] = []
for entity_class in sorted(required_classes):
    path = OUT / f"{entity_class}.jsonl"
    class_records = [record for record in records_sorted if record["entity_class"] == entity_class]
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for record in class_records),
        encoding="utf-8",
    )
    class_paths.append(path)

counts = Counter(record["entity_class"] for record in records_sorted)
export_files = [schema_path, combined_path, *class_paths]
manifest = {
    "schema": "ag-bridge-backend-export-manifest-v1",
    "schema_version": SCHEMA_VERSION,
    "generated_from_build_utc": TIMESTAMP,
    "unit": "unit-01",
    "encoding": "UTF-8",
    "serialization": "canonical JSON Lines: sorted records and keys, compact separators, LF",
    "record_count": len(records_sorted),
    "counts": {key: counts[key] for key in sorted(counts)},
    "files": [
        {"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)}
        for path in export_files
    ],
    "source_bindings": [
        {"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path)}
        for path in [
            *SOURCE_FILES,
            ROOT / "00_control" / "TERMINOLOGY.csv",
            ROOT / "00_control" / "CORRECTIONS.csv",
            ROOT / "authority" / "RIGHTS.csv",
            ROOT / "authority" / "ASSET_CLOSURE.json",
            ROOT / "build" / "reader-id" / "BUILD_RECEIPT.json",
            machine_qa_path,
            visual_qa_path,
        ]
    ],
    "validation": {
        "unique_stable_ids": True,
        "parent_closure": True,
        "required_entity_class_closure": True,
        "deterministic_replay_required": True,
    },
}
manifest_path = OUT / "MANIFEST.json"
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(
    json.dumps(
        {
            "result": "PASS",
            "records": len(records_sorted),
            "counts": manifest["counts"],
            "manifest": rel(manifest_path),
            "manifest_sha256": digest(manifest_path),
        },
        ensure_ascii=False,
    )
)
