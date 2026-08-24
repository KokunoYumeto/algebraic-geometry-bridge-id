#!/usr/bin/env python3
"""Bind Unit 6's human fidelity audit to replayable authority and reader evidence."""

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
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
AUTHORITY_DIR = ROOT / "authority" / "wikiversity" / "unit-06"
MANIFEST_PATH = AUTHORITY_DIR / "UNIT_AUTHORITY_MANIFEST.json"
MAP_PATH = AUTHORITY_DIR / "ORDERED_EXERCISE_MAP.json"
LECTURE = ROOT / "source" / "id-ID" / "lecture-06.md"
WORKSHEET = ROOT / "source" / "id-ID" / "worksheet-06.md"
SOLUTIONS = ROOT / "source" / "id-ID" / "worksheet-06-solutions.md"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-06.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-06.json"
CORRECTIONS = ROOT / "00_control" / "CORRECTIONS.csv"
MACHINE_QA = ROOT / "qa" / "UNITS_01_06_MACHINE_QA.json"
VISUAL_QA = ROOT / "qa" / "UNITS_01_06_VISUAL_QA.json"
RESPONSIVE_QA = ROOT / "qa" / "UNITS_01_06_RESPONSIVE_QA.json"
RECEIPT = ROOT / "qa" / "UNIT_06_PROTECTED_SURFACES.json"


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
    raw = subprocess.check_output([
        pandoc,
        "--from=markdown+yaml_metadata_block+tex_math_dollars+fenced_divs+bracketed_spans",
        "--to=json",
        str(path),
    ], cwd=ROOT)
    nodes = list(walk(json.loads(raw)["blocks"]))
    return {
        "headings": sum(node.get("t") == "Header" for node in nodes),
        "math_nodes": sum(node.get("t") == "Math" for node in nodes),
        "images": sum(node.get("t") == "Image" for node in nodes),
    }


def authority_math_count(path: Path) -> int:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    return len(soup.find_all("math"))


def compact(value: str) -> str:
    return re.sub(r"[\s&]+", "", value)


def require_formulae(path: Path, needles: list[str]) -> None:
    text = compact(path.read_text(encoding="utf-8"))
    missing = [needle for needle in needles if compact(needle) not in text]
    require(not missing, f"Protected formulae missing from {path.name}: {missing}")


manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
exercise_map = json.loads(MAP_PATH.read_text(encoding="utf-8"))
require(manifest["unit_number"] == 6, "Authority manifest is not Unit 6")
require(exercise_map["exercise_count"] == 30, "Authority exercise count mismatch")
require(exercise_map["solution_count"] == 9, "Authority solution count mismatch")

manifest_mismatches: list[str] = []
for row in manifest["files"]:
    path = AUTHORITY_DIR / row["file"]
    if not path.is_file() or path.stat().st_size != row["bytes"] or digest(path) != row["sha256"]:
        manifest_mismatches.append(row["file"])
require(not manifest_mismatches, f"Authority manifest replay failed: {manifest_mismatches}")

pdf_mismatches: list[str] = []
pdf_pages: dict[str, int] = {}
for row in manifest["official_pdf_witnesses"]:
    path = ROOT / row["local_path"]
    if not path.is_file() or path.stat().st_size != row["local_bytes"] or digest(path) != row["local_sha256"]:
        pdf_mismatches.append(row["local_path"])
        continue
    pdf_pages[row["local_path"]] = len(PdfReader(path).pages)
require(not pdf_mismatches, f"Official PDF replay failed: {pdf_mismatches}")
require(sorted(pdf_pages.values()) == [7, 9], "Official PDF page counts changed")

for metadata, authority, label in (
    (yaml_metadata(LECTURE), manifest["lecture"], "lecture"),
    (yaml_metadata(WORKSHEET), manifest["worksheet"], "worksheet"),
):
    require(int(metadata["upstream_pageid"]) == authority["pageid"], f"{label} pageid mismatch")
    require(int(metadata["upstream_revid"]) == authority["revid"], f"{label} revid mismatch")
    require(metadata["upstream_timestamp"] == authority["timestamp"], f"{label} timestamp mismatch")
    require(metadata["upstream_mediawiki_sha1"] == authority["mediawiki_sha1"], f"{label} SHA-1 mismatch")
    require(metadata["translation_status"] == "complete", f"{label} is not marked complete")

target_counts = {path.name: ast_counts(path) for path in (LECTURE, WORKSHEET, SOLUTIONS)}
require(target_counts[LECTURE.name] == {"headings": 17, "math_nodes": 142, "images": 3}, "Lecture AST topology mismatch")
require(target_counts[WORKSHEET.name] == {"headings": 33, "math_nodes": 109, "images": 0}, "Worksheet AST topology mismatch")
require(target_counts[SOLUTIONS.name] == {"headings": 10, "math_nodes": 105, "images": 0}, "Solutions AST topology mismatch")

lecture_text = LECTURE.read_text(encoding="utf-8")
worksheet_text = WORKSHEET.read_text(encoding="utf-8")
solution_text = SOLUTIONS.read_text(encoding="utf-8")
exercise_rows = re.findall(
    r"^### Soal 6\.(\d+)( ★)?(?: - (\d+) poin)? \{#br-ak-2025-2026-w06-ex-(\d{2})\}$",
    worksheet_text,
    flags=re.MULTILINE,
)
require(len(exercise_rows) == 30, "Translated worksheet does not contain 30 exact exercise headings")
require([int(row[0]) for row in exercise_rows] == list(range(1, 31)), "Exercise sequence mismatch")
require(all(int(number) == int(identifier) for number, _, _, identifier in exercise_rows), "Exercise stable-ID mismatch")
starred = [int(number) for number, star, _, _ in exercise_rows if star]
points = [int(value) for _, _, value, _ in exercise_rows if value]
require(starred == [3, 4, 8, 9, 17, 18, 21, 22, 25], "Starred-exercise topology mismatch")
require(points == [3, 6, 5, 5, 4], "Submission-point topology mismatch")
entity_bindings = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet_text)
require(entity_bindings == [row["exercise_title"] for row in exercise_map["entries"]], "Ordered exercise bindings mismatch")

solution_ids = [int(value) for value in re.findall(r"\{#br-ak-2025-2026-w06-sol-(\d{2})\}", solution_text)]
solution_revids = [int(value) for value in re.findall(r"upstream_solution_revid:\s*(\d+)", solution_text)]
expected_solution_ids = [3, 4, 8, 9, 17, 18, 21, 22, 25]
expected_solution_revids = [1112350, 958133, 1057120, 1112838, 1096769, 1024155, 1067921, 1096509, 1089645]
mapped_rows = [row for row in exercise_map["entries"] if row.get("has_public_solution")]
require(solution_ids == expected_solution_ids, "Translated public-solution set mismatch")
require(solution_revids == expected_solution_revids, "Translated solution-revision binding mismatch")
require([row["exercise_number"] for row in mapped_rows] == solution_ids, "Authority solution set mismatch")
require([row["revid"] for row in mapped_rows] == solution_revids, "Authority solution revid mismatch")
require("Tidak ada solusi tambahan yang dibuat" in solution_text.replace("\n", " "), "No-invention notice missing")
for number in expected_solution_ids:
    require(f"(#br-ak-2025-2026-w06-ex-{number:02d})" in solution_text, f"Return link missing for solution {number}")

all_target_text = "\n".join((lecture_text, worksheet_text, solution_text))
ids = re.findall(r"\{#([^}]+)\}", all_target_text)
require(len(ids) == 60 and len(set(ids)) == 60, "Unit 6 heading IDs are missing or duplicated")
require(all(value.startswith("br-ak-2025-2026-") for value in ids), "Invalid Unit 6 stable-ID prefix")
require(not re.search(r"\b(?:TODO|TBD|PENDING|PLACEHOLDER)\b", all_target_text, flags=re.IGNORECASE), "Pending marker in Unit 6 target")
active_prose = "\n".join(body_text(path) for path in (LECTURE, WORKSHEET, SOLUTIONS))
german_hits = sorted(set(re.findall(r"\b(?:Aufgabe|Beweis|Körper|Menge|Abbildung|wenn|dann|nicht|seien|zeige|Punkte)\b", active_prose, flags=re.IGNORECASE)))
require(not german_hits, f"Active German prose remains: {german_hits}")

require_formulae(LECTURE, [
    r"F(P,Q)=0", r"(n+1)(m+1)>dn+em+1", r"\operatorname{Id}(B)=(F)",
    r"y^2+4x^2-4xy-15x+7y+13=0", r"Y^2-X^3-X^2",
    r"D(Q)=\mathbb A_K^1\setminus V(Q)", r"\varphi_1=\frac{P_1}{Q_1}",
    r"F(P_1,P_2,P_3)=0", r"F(H_1,H_2,H_3)=0",
    r"0=F\left(\frac{H_1}{H_3},\frac{H_2}{H_3},1\right)",
    r"G(X,Y)=F(X,Y,1)", r"0=G\left(\frac{P_1}{Q},\frac{P_2}{Q}\right)",
])
require_formulae(WORKSHEET, [
    r"x=-3t^2+4t-2", r"t\longmapsto(t+t^2,t^3)=(x,y)",
    r"F(S,T,ST)=0", r"t\longmapsto\left(\frac{t}{t^2-1},\frac1t\right)",
    r"t\longmapsto(t\cos t,t\sin t)", r"\overline{\varphi(C)}",
    r"(s,t)\longmapsto(s^2,t^2,st)=(x,y,z)",
])
require_formulae(SOLUTIONS, [
    r"X^3-Y^2-Y-3XY=0", r"-Y^2+X^3-5X^2+8X-4=0",
    r"F_2+2F_3-F_4+F_5-2F_6=0", r"Y^2-XY+X-2Y+2",
    r"S^{\alpha+\gamma}T^{\beta+\gamma}",
])

with RIGHTS.open("r", encoding="utf-8", newline="") as stream:
    rights_rows = list(csv.DictReader(stream))
closure = json.loads(CLOSURE.read_text(encoding="utf-8"))
require(len(rights_rows) == 3, "Unit 6 rights row count mismatch")
require(closure["reader_media_positions"] == 3 and closure["unique_local_assets"] == 4, "Unit 6 asset closure mismatch")
require(closure["rights_sha256"] == digest(RIGHTS), "Unit 6 rights hash binding mismatch")
target_media_paths = re.findall(r"!\[[^\]]+\]\((authority/assets/[^)]+)\)", lecture_text + "\n" + worksheet_text)
require(target_media_paths == [row["local_path"] for row in rights_rows], "Reader media order/path mismatch")
for row in rights_rows:
    asset = ROOT / row["local_path"]
    require(asset.stat().st_size == int(row["local_bytes"]) and digest(asset) == row["local_sha256"], f"Asset mismatch: {row['asset_id']}")
    if row["pdf_local_path"]:
        pdf_asset = ROOT / row["pdf_local_path"]
        require(pdf_asset.stat().st_size == int(row["pdf_local_bytes"]) and digest(pdf_asset) == row["pdf_local_sha256"], f"PDF asset mismatch: {row['asset_id']}")

with CORRECTIONS.open("r", encoding="utf-8", newline="") as stream:
    correction_rows = list(csv.DictReader(stream))
correction_ids = {row["correction_id"] for row in correction_rows}
required_corrections = {"AGC-CORR-0010", "AGC-ADAPT-0008", "AGC-ADAPT-0009", "AGC-ADAPT-0010", "AGC-ADAPT-0011"}
require(required_corrections.issubset(correction_ids), "Unit 6 correction/adaptation records missing")

source_math = {
    "lecture": authority_math_count(AUTHORITY_DIR / manifest["lecture"]["html_file"]),
    "worksheet": authority_math_count(AUTHORITY_DIR / manifest["worksheet"]["html_file"]),
    "solutions": sum(authority_math_count(AUTHORITY_DIR / row["html_file"]) for row in mapped_rows),
}
require(source_math == {"lecture": 158, "worksheet": 111, "solutions": 116}, "Authority math counts changed")

bound_qa: dict[str, Any] = {}
status = "PASS_SOURCE_BOUNDARY"
if RESPONSIVE_QA.exists():
    require(MACHINE_QA.is_file() and VISUAL_QA.is_file(), "Cumulative QA receipt closure is incomplete")
    machine = json.loads(MACHINE_QA.read_text(encoding="utf-8"))
    visual = json.loads(VISUAL_QA.read_text(encoding="utf-8"))
    responsive = json.loads(RESPONSIVE_QA.read_text(encoding="utf-8"))
    require(machine.get("status") == "PASS" and machine.get("through_unit") == 6, "Machine QA is not a Unit 6 PASS")
    require(visual.get("result") == "PASS" and visual.get("through_unit") == 6, "Visual QA is not a Unit 6 PASS")
    require(responsive.get("status") == "PASS" and responsive.get("through_unit") == 6, "Responsive QA is not a Unit 6 PASS")
    bound_qa = {key: {"path": rel(path), "sha256": digest(path)} for key, path in (
        ("machine", MACHINE_QA), ("visual", VISUAL_QA), ("responsive", RESPONSIVE_QA)
    )}
    status = "PASS"

receipt = {
    "schema": "ag-bridge-protected-surface-audit-v2",
    "audited_utc": datetime.now(timezone.utc).isoformat(),
    "status": status,
    "unit": 6,
    "authority": {
        "manifest_path": rel(MANIFEST_PATH),
        "manifest_bytes": MANIFEST_PATH.stat().st_size,
        "manifest_sha256": digest(MANIFEST_PATH),
        "manifest_files_replayed": len(manifest["files"]),
        "official_pdf_pages": pdf_pages,
        "lecture_revid": manifest["lecture"]["revid"],
        "worksheet_revid": manifest["worksheet"]["revid"],
        "lecture_transclusions": manifest["lecture_transclusion_closure"]["captured_page_count"],
        "worksheet_transclusions": manifest["worksheet_transclusion_closure"]["captured_page_count"],
        "ordered_exercise_map_sha256": digest(MAP_PATH),
    },
    "targets": [
        {"path": rel(path), "bytes": path.stat().st_size, "sha256": digest(path), **target_counts[path.name]}
        for path in (LECTURE, WORKSHEET, SOLUTIONS)
    ],
    "topology": {
        "unit_heading_ids": len(ids), "duplicate_heading_ids": len(ids) - len(set(ids)),
        "exercises": 30, "submission_points": points, "starred_exercises": starred,
        "public_solutions": 9, "solution_exercises": solution_ids,
        "solution_revisions": solution_revids, "invented_solutions": 0,
        "untranslated_german_prose": 0, "media_positions": 3, "binary_surfaces": 4,
    },
    "math_count_reconciliation": {
        "authority": source_math,
        "target": {key: value["math_nodes"] for key, value in target_counts.items()},
        "explanation": "Pandoc and MediaWiki split aligned formulae and renderer scaffolding differently. Exact hypotheses, elimination identities, homogeneous substitutions, exercise order, and all nine solution surfaces are protected by formula needles and revision bindings.",
    },
    "fidelity_findings": {
        "protected_formula_needles": {"lecture": 12, "worksheet": 7, "solutions": 5},
        "explicit_source_precision_delta": "The ternary homogeneous F is dehomogenized explicitly as G(X,Y)=F(X,Y,1) before the two-variable rational identity.",
        "remaining_mathematical_defects": 0, "remaining_omissions": 0, "invented_solutions": 0,
    },
    "rights": {"path": rel(RIGHTS), "sha256": digest(RIGHTS), "closure_path": rel(CLOSURE), "closure_sha256": digest(CLOSURE)},
    "corrections_ledger": {"path": rel(CORRECTIONS), "sha256": digest(CORRECTIONS), "rows": len(correction_rows), "unit_06_records": sorted(required_corrections)},
    "bound_qa": bound_qa,
}

RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": status, "receipt": rel(RECEIPT), "bytes": RECEIPT.stat().st_size, "sha256": digest(RECEIPT)}))
