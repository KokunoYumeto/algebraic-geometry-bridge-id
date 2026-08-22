#!/usr/bin/env python3
"""Bind Unit 4's human fidelity audit to replayable authority and reader evidence."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_DIR = ROOT / "authority" / "wikiversity" / "unit-04"
MANIFEST_PATH = AUTHORITY_DIR / "UNIT_AUTHORITY_MANIFEST.json"
MAP_PATH = AUTHORITY_DIR / "ORDERED_EXERCISE_MAP.json"
LECTURE = ROOT / "source" / "id-ID" / "lecture-04.md"
WORKSHEET = ROOT / "source" / "id-ID" / "worksheet-04.md"
SOLUTIONS = ROOT / "source" / "id-ID" / "worksheet-04-solutions.md"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-04.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-04.json"
CORRECTIONS = ROOT / "00_control" / "CORRECTIONS.csv"
MACHINE_QA = ROOT / "qa" / "UNITS_01_04_MACHINE_QA.json"
VISUAL_QA = ROOT / "qa" / "UNITS_01_04_VISUAL_QA.json"
RESPONSIVE_QA = ROOT / "qa" / "UNITS_01_04_RESPONSIVE_QA.json"
RECEIPT = ROOT / "qa" / "UNIT_04_PROTECTED_SURFACES.json"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def yaml_metadata(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    require(lines and lines[0] == "---", f"Missing YAML metadata: {path.name}")
    end = lines.index("---", 1)
    result: dict[str, str] = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            result[match.group(1)] = match.group(2).strip().strip('"')
    return result


def body_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        text = text.split("---\n", 2)[2]
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def ast_counts(path: Path) -> dict[str, int]:
    pandoc = shutil.which("pandoc")
    require(pandoc is not None, "Pandoc is not on PATH")
    raw = subprocess.check_output(
        [
            pandoc,
            "--from=markdown+yaml_metadata_block+tex_math_dollars+fenced_divs+bracketed_spans",
            "--to=json",
            str(path),
        ],
        cwd=ROOT,
    )
    nodes = list(walk(json.loads(raw)["blocks"]))
    return {
        "headings": sum(node.get("t") == "Header" for node in nodes),
        "math_nodes": sum(node.get("t") == "Math" for node in nodes),
        "images": sum(node.get("t") == "Image" for node in nodes),
    }


def authority_math_count(path: Path) -> int:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    return len(soup.find_all("math"))


manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
exercise_map = json.loads(MAP_PATH.read_text(encoding="utf-8"))
require(manifest["unit_number"] == 4, "Authority manifest is not Unit 4")
require(exercise_map["exercise_count"] == 30, "Authority exercise count mismatch")
require(exercise_map["solution_count"] == 6, "Authority solution count mismatch")

manifest_mismatches: list[str] = []
for row in manifest["files"]:
    path = AUTHORITY_DIR / row["file"]
    if not path.is_file() or path.stat().st_size != row["bytes"] or digest(path) != row["sha256"]:
        manifest_mismatches.append(row["file"])
require(not manifest_mismatches, f"Authority manifest replay failed: {manifest_mismatches}")

lecture_meta = yaml_metadata(LECTURE)
worksheet_meta = yaml_metadata(WORKSHEET)
for metadata, authority, label in (
    (lecture_meta, manifest["lecture"], "lecture"),
    (worksheet_meta, manifest["worksheet"], "worksheet"),
):
    require(int(metadata["upstream_pageid"]) == authority["pageid"], f"{label} pageid mismatch")
    require(int(metadata["upstream_revid"]) == authority["revid"], f"{label} revid mismatch")
    require(metadata["upstream_timestamp"] == authority["timestamp"], f"{label} timestamp mismatch")
    require(metadata["upstream_mediawiki_sha1"] == authority["mediawiki_sha1"], f"{label} SHA-1 mismatch")
    require(metadata["translation_status"] == "complete", f"{label} is not marked complete")

target_counts = {
    LECTURE.name: ast_counts(LECTURE),
    WORKSHEET.name: ast_counts(WORKSHEET),
    SOLUTIONS.name: ast_counts(SOLUTIONS),
}
require(target_counts[LECTURE.name] == {"headings": 15, "math_nodes": 169, "images": 7}, "Lecture AST topology mismatch")
require(target_counts[WORKSHEET.name] == {"headings": 33, "math_nodes": 115, "images": 2}, "Worksheet AST topology mismatch")
require(target_counts[SOLUTIONS.name] == {"headings": 7, "math_nodes": 102, "images": 0}, "Solutions AST topology mismatch")

worksheet_text = WORKSHEET.read_text(encoding="utf-8")
solution_text = SOLUTIONS.read_text(encoding="utf-8")
lecture_text = LECTURE.read_text(encoding="utf-8")
exercise_rows = re.findall(
    r"^### Soal 4\.(\d+)( ★)?(?: - (\d+) poin)? \{#br-ak-2025-2026-w04-ex-(\d{2})\}$",
    worksheet_text,
    flags=re.MULTILINE,
)
require(len(exercise_rows) == 30, "Translated worksheet does not contain 30 exact exercise headings")
require([int(row[0]) for row in exercise_rows] == list(range(1, 31)), "Exercise sequence mismatch")
require(all(int(number) == int(identifier) for number, _, _, identifier in exercise_rows), "Exercise stable-ID mismatch")
starred = [int(number) for number, star, _, _ in exercise_rows if star]
points = [int(value) for _, _, value, _ in exercise_rows if value]
require(starred == [10, 11, 12, 14, 15, 17], "Starred-exercise topology mismatch")
require(points == [6, 3, 4, 3, 4, 4], "Submission-point topology mismatch")
require(len(re.findall(r"<!-- upstream_entity:", worksheet_text)) == 30, "Exercise authority bindings mismatch")

solution_ids = [int(value) for value in re.findall(r"\{#br-ak-2025-2026-w04-sol-(\d{2})\}", solution_text)]
solution_revids = [int(value) for value in re.findall(r"upstream_solution_revid:\s*(\d+)", solution_text)]
mapped_rows = [row for row in exercise_map["entries"] if row.get("has_public_solution")]
expected_solution_ids = [10, 11, 12, 14, 15, 17]
expected_solution_revids = [1067858, 1067949, 1110006, 1075363, 1072981, 485196]
require(solution_ids == expected_solution_ids, "Translated public-solution set mismatch")
require(solution_revids == expected_solution_revids, "Translated solution-revision binding mismatch")
require([row["exercise_number"] for row in mapped_rows] == solution_ids, "Authority solution set mismatch")
require([row["revid"] for row in mapped_rows] == solution_revids, "Authority solution revid mismatch")
require(re.search(r"Tidak ada solusi tambahan\s+yang dibuat", solution_text) is not None, "No-invention notice missing")
for number in expected_solution_ids:
    require(f"(#br-ak-2025-2026-w04-ex-{number:02d})" in solution_text, f"Return link missing for solution {number}")

all_target_text = "\n".join(path.read_text(encoding="utf-8") for path in (LECTURE, WORKSHEET, SOLUTIONS))
ids = re.findall(r"\{#([^}]+)\}", all_target_text)
require(len(ids) == 55 and len(set(ids)) == 55, "Unit 4 heading IDs are missing or duplicated")
require(all(value.startswith("br-ak-2025-2026-") for value in ids), "Invalid Unit 4 stable-ID prefix")
require(not re.search(r"\b(?:TODO|TBD|PENDING|PLACEHOLDER)\b", all_target_text, flags=re.IGNORECASE), "Pending marker in Unit 4 target")
active_prose = "\n".join(body_text(path) for path in (LECTURE, WORKSHEET, SOLUTIONS))
german_hits = sorted(set(re.findall(r"\b(?:Aufgabe|Beweis|Körper|Menge|Punktmenge|Abbildung|Restklassenring|wenn|dann|nicht|seien|beweise)\b", active_prose, flags=re.IGNORECASE)))
require(not german_hits, f"Active German prose remains: {german_hits}")

require("V(\\mathfrak p)=\\varnothing" in worksheet_text and "\\mathfrak p=(X^2+1)" in worksheet_text, "Exercise 4.6 edition note missing")
require("E_2" in lecture_text and "parallel" not in lecture_text.casefold(), "Corrected E2 referent missing")
require("Soal 9.20" in worksheet_text, "Exercise 4.25 source hint missing")
require("domain ideal utama" in worksheet_text, "Exercise 4.27 source note missing")
require("Soal 1.28" in worksheet_text and "Korolari 4.9" in worksheet_text, "Exercise 4.28 source hint missing")
require("pemetaan tertutup" in worksheet_text and "pemetaan terbuka" in worksheet_text, "Source topology definitions missing")

with RIGHTS.open("r", encoding="utf-8", newline="") as stream:
    rights_rows = list(csv.DictReader(stream))
closure = json.loads(CLOSURE.read_text(encoding="utf-8"))
require(len(rights_rows) == 9, "Unit 4 rights row count mismatch")
require(closure["reader_media_positions"] == 9 and closure["unique_local_assets"] == 11, "Unit 4 asset closure mismatch")
require(closure["rights_sha256"] == digest(RIGHTS), "Unit 4 rights hash binding mismatch")
for row in rights_rows:
    asset = ROOT / row["local_path"]
    require(asset.stat().st_size == int(row["local_bytes"]), f"Asset byte mismatch: {row['asset_id']}")
    require(digest(asset) == row["local_sha256"], f"Asset hash mismatch: {row['asset_id']}")
    if row["pdf_local_path"]:
        pdf_asset = ROOT / row["pdf_local_path"]
        require(pdf_asset.stat().st_size == int(row["pdf_local_bytes"]), f"PDF asset byte mismatch: {row['asset_id']}")
        require(digest(pdf_asset) == row["pdf_local_sha256"], f"PDF asset hash mismatch: {row['asset_id']}")

with CORRECTIONS.open("r", encoding="utf-8", newline="") as stream:
    correction_rows = list(csv.DictReader(stream))
require(len(correction_rows) == 9, "Correction-ledger row count changed unexpectedly")
correction_ids = {row["correction_id"] for row in correction_rows}
require({"AGC-CORR-0005", "AGC-CORR-0006"}.issubset(correction_ids), "Unit 4 correction records missing")

source_math = {
    "lecture": authority_math_count(AUTHORITY_DIR / manifest["lecture"]["html_file"]),
    "worksheet": authority_math_count(AUTHORITY_DIR / manifest["worksheet"]["html_file"]),
    "solutions": sum(authority_math_count(AUTHORITY_DIR / row["html_file"]) for row in mapped_rows),
}
require(source_math == {"lecture": 175, "worksheet": 121, "solutions": 100}, "Authority math counts changed")

targets = [
    {"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path), **target_counts[path.name]}
    for path in (LECTURE, WORKSHEET, SOLUTIONS)
]

bound_qa: dict[str, Any] = {}
status = "PASS_SOURCE_BOUNDARY"
if MACHINE_QA.exists() or VISUAL_QA.exists() or RESPONSIVE_QA.exists():
    require(MACHINE_QA.is_file() and VISUAL_QA.is_file() and RESPONSIVE_QA.is_file(), "Cumulative QA receipt closure is incomplete")
    machine = json.loads(MACHINE_QA.read_text(encoding="utf-8"))
    visual = json.loads(VISUAL_QA.read_text(encoding="utf-8"))
    responsive = json.loads(RESPONSIVE_QA.read_text(encoding="utf-8"))
    require(machine.get("status") == "PASS" and machine.get("through_unit") == 4, "Machine QA is not a Unit 4 PASS")
    require(visual.get("result") == "PASS" and visual.get("through_unit") == 4, "Visual QA is not a Unit 4 PASS")
    require(responsive.get("status") == "PASS" and responsive.get("through_unit") == 4, "Responsive QA is not a Unit 4 PASS")
    bound_qa = {
        "machine_receipt_path": rel(MACHINE_QA),
        "machine_receipt_sha256": digest(MACHINE_QA),
        "visual_receipt_path": rel(VISUAL_QA),
        "visual_receipt_sha256": digest(VISUAL_QA),
        "responsive_receipt_path": rel(RESPONSIVE_QA),
        "responsive_receipt_sha256": digest(RESPONSIVE_QA),
    }
    status = "PASS"

receipt = {
    "schema": "ag-bridge-protected-surface-audit-v1",
    "audited_utc": datetime.now(timezone.utc).isoformat(),
    "status": status,
    "unit": 4,
    "authority": {
        "manifest_path": rel(MANIFEST_PATH),
        "manifest_bytes": MANIFEST_PATH.stat().st_size,
        "manifest_sha256": digest(MANIFEST_PATH),
        "manifest_files_replayed": len(manifest["files"]),
        "manifest_file_mismatches": len(manifest_mismatches),
        "lecture": {
            **{key: manifest["lecture"][key] for key in ("pageid", "revid", "parentid", "timestamp", "mediawiki_sha1")},
            "transclusions_requested": manifest["lecture_transclusion_closure"]["requested_template_count"],
            "transclusions_captured": manifest["lecture_transclusion_closure"]["captured_page_count"],
            "transclusions_missing": manifest["lecture_transclusion_closure"]["missing_page_count"],
        },
        "worksheet": {
            **{key: manifest["worksheet"][key] for key in ("pageid", "revid", "parentid", "timestamp", "mediawiki_sha1")},
            "transclusions_requested": manifest["worksheet_transclusion_closure"]["requested_template_count"],
            "transclusions_captured": manifest["worksheet_transclusion_closure"]["captured_page_count"],
            "transclusions_missing": manifest["worksheet_transclusion_closure"]["missing_page_count"],
        },
        "ordered_exercise_map_path": rel(MAP_PATH),
        "ordered_exercise_map_bytes": MAP_PATH.stat().st_size,
        "ordered_exercise_map_sha256": digest(MAP_PATH),
    },
    "targets": targets,
    "topology": {
        "unit_heading_ids": len(ids),
        "duplicate_heading_ids": len(ids) - len(set(ids)),
        "invalid_id_patterns": 0,
        "exercises": 30,
        "practice_exercises": "4.1-4.24",
        "submission_exercises": "4.25-4.30",
        "submission_points": points,
        "starred_exercises": starred,
        "public_solutions": len(solution_ids),
        "solution_exercises": solution_ids,
        "solution_revisions": solution_revids,
        "broken_solution_links": 0,
        "untranslated_german_prose": 0,
        "source_notes_and_hints_preserved": ["4.25", "4.27", "4.28"],
        "source_topology_definitions_preserved": ["pemetaan tertutup", "pemetaan terbuka"],
        "media_positions": len(rights_rows),
        "binary_surfaces": closure["unique_local_assets"],
        "missing_media_positions": 0,
    },
    "math_count_reconciliation": {
        "lecture": {
            "authority_math_nodes": source_math["lecture"],
            "target_math_nodes": target_counts[LECTURE.name]["math_nodes"],
            "explanation": "The six-node net decrease is accounted for by consolidation of paired conditions, ideals, and aligned equalities; the factorization and final ideal identity remain present. The target explicitly typesets the source-prose nonzero denominator-clearing polynomial and uses isomorphism notation for quotient identification. The source's repeated E1 referent is rendered as the intended E2 and is correction-ledger bound.",
        },
        "worksheet": {
            "authority_math_nodes": source_math["worksheet"],
            "target_math_nodes": target_counts[WORKSHEET.name]["math_nodes"],
            "explanation": "The six-node net decrease comes from consolidating renderer-split hypotheses, displays, projection formulas, and alternatives. The edition note for Exercise 4.6 adds three explicit math nodes for the omitted empty-zero-locus counterexample; all source task formulas remain present.",
        },
        "solutions": {
            "authority_math_nodes": source_math["solutions"],
            "target_math_nodes": target_counts[SOLUTIONS.name]["math_nodes"],
            "explanation": "The two-node net increase is caused by separately typesetting prose variables and residue classes. The local polynomial-degree index in Solution 4.12 is renamed from the source's overloaded n to m without changing the argument; aligned equalities are semantically preserved.",
        },
    },
    "fidelity_findings": {
        "fixed_before_build": [
            "Worksheet 4.6 source omission is exposed in a non-invasive edition note.",
            "Lecture 4's repeated E1 referent is rendered as the intended E2.",
        ],
        "remaining_mathematical_defects": 0,
        "remaining_omissions": 0,
        "invented_solutions": 0,
    },
    "rights": {
        "path": rel(RIGHTS),
        "bytes": RIGHTS.stat().st_size,
        "sha256": digest(RIGHTS),
        "closure_path": rel(CLOSURE),
        "closure_sha256": digest(CLOSURE),
    },
    "corrections_ledger": {
        "path": rel(CORRECTIONS),
        "bytes": CORRECTIONS.stat().st_size,
        "sha256": digest(CORRECTIONS),
        "rows": len(correction_rows),
        "unit_04_additions": 2,
    },
    "comparison_script": {
        "path": "scripts/compare_math_surfaces.py",
        "bytes": (ROOT / "scripts" / "compare_math_surfaces.py").stat().st_size,
        "sha256": digest(ROOT / "scripts" / "compare_math_surfaces.py"),
    },
    "bound_qa": bound_qa,
}

RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": status, "receipt": rel(RECEIPT), "bytes": RECEIPT.stat().st_size, "sha256": digest(RECEIPT)}))
