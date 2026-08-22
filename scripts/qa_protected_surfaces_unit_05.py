#!/usr/bin/env python3
"""Bind Unit 5's human fidelity audit to replayable authority and reader evidence."""

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
AUTHORITY_DIR = ROOT / "authority" / "wikiversity" / "unit-05"
MANIFEST_PATH = AUTHORITY_DIR / "UNIT_AUTHORITY_MANIFEST.json"
MAP_PATH = AUTHORITY_DIR / "ORDERED_EXERCISE_MAP.json"
LECTURE = ROOT / "source" / "id-ID" / "lecture-05.md"
WORKSHEET = ROOT / "source" / "id-ID" / "worksheet-05.md"
SOLUTIONS = ROOT / "source" / "id-ID" / "worksheet-05-solutions.md"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-05.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-05.json"
CORRECTIONS = ROOT / "00_control" / "CORRECTIONS.csv"
MACHINE_QA = ROOT / "qa" / "UNITS_01_05_MACHINE_QA.json"
VISUAL_QA = ROOT / "qa" / "UNITS_01_05_VISUAL_QA.json"
RESPONSIVE_QA = ROOT / "qa" / "UNITS_01_05_RESPONSIVE_QA.json"
RECEIPT = ROOT / "qa" / "UNIT_05_PROTECTED_SURFACES.json"


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


def compact(value: str) -> str:
    return re.sub(r"[\s&]+", "", value)


def require_formulae(path: Path, needles: list[str]) -> None:
    text = compact(path.read_text(encoding="utf-8"))
    missing = [needle for needle in needles if compact(needle) not in text]
    require(not missing, f"Protected formulae missing from {path.name}: {missing}")


manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
exercise_map = json.loads(MAP_PATH.read_text(encoding="utf-8"))
require(manifest["unit_number"] == 5, "Authority manifest is not Unit 5")
require(exercise_map["exercise_count"] == 27, "Authority exercise count mismatch")
require(exercise_map["solution_count"] == 4, "Authority solution count mismatch")

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
require(target_counts[LECTURE.name] == {"headings": 18, "math_nodes": 182, "images": 2}, "Lecture AST topology mismatch")
require(target_counts[WORKSHEET.name] == {"headings": 30, "math_nodes": 100, "images": 1}, "Worksheet AST topology mismatch")
require(target_counts[SOLUTIONS.name] == {"headings": 5, "math_nodes": 58, "images": 0}, "Solutions AST topology mismatch")

worksheet_text = WORKSHEET.read_text(encoding="utf-8")
solution_text = SOLUTIONS.read_text(encoding="utf-8")
lecture_text = LECTURE.read_text(encoding="utf-8")
exercise_rows = re.findall(
    r"^### Soal 5\.(\d+)( ★)?(?: - (\d+) poin)? \{#br-ak-2025-2026-w05-ex-(\d{2})\}$",
    worksheet_text,
    flags=re.MULTILINE,
)
require(len(exercise_rows) == 27, "Translated worksheet does not contain 27 exact exercise headings")
require([int(row[0]) for row in exercise_rows] == list(range(1, 28)), "Exercise sequence mismatch")
require(all(int(number) == int(identifier) for number, _, _, identifier in exercise_rows), "Exercise stable-ID mismatch")
starred = [int(number) for number, star, _, _ in exercise_rows if star]
points = [int(value) for _, _, value, _ in exercise_rows if value]
require(starred == [3, 15, 19, 20], "Starred-exercise topology mismatch")
require(points == [3, 3, 3, 3, 4], "Submission-point topology mismatch")
entity_bindings = re.findall(r"<!-- upstream_entity: (.*?) -->", worksheet_text)
require(entity_bindings == [row["exercise_title"] for row in exercise_map["entries"]], "Ordered exercise authority bindings mismatch")

solution_ids = [int(value) for value in re.findall(r"\{#br-ak-2025-2026-w05-sol-(\d{2})\}", solution_text)]
solution_revids = [int(value) for value in re.findall(r"upstream_solution_revid:\s*(\d+)", solution_text)]
mapped_rows = [row for row in exercise_map["entries"] if row.get("has_public_solution")]
expected_solution_ids = [3, 15, 19, 20]
expected_solution_revids = [1068012, 1028148, 1096503, 1096346]
require(solution_ids == expected_solution_ids, "Translated public-solution set mismatch")
require(solution_revids == expected_solution_revids, "Translated solution-revision binding mismatch")
require([row["exercise_number"] for row in mapped_rows] == solution_ids, "Authority solution set mismatch")
require([row["revid"] for row in mapped_rows] == solution_revids, "Authority solution revid mismatch")
require(re.search(r"Tidak ada solusi tambahan\s+yang dibuat", solution_text) is not None, "No-invention notice missing")
for number in expected_solution_ids:
    require(f"(#br-ak-2025-2026-w05-ex-{number:02d})" in solution_text, f"Return link missing for solution {number}")

all_target_text = "\n".join(path.read_text(encoding="utf-8") for path in (LECTURE, WORKSHEET, SOLUTIONS))
ids = re.findall(r"\{#([^}]+)\}", all_target_text)
require(len(ids) == 53 and len(set(ids)) == 53, "Unit 5 heading IDs are missing or duplicated")
require(all(value.startswith("br-ak-2025-2026-") for value in ids), "Invalid Unit 5 stable-ID prefix")
require(not re.search(r"\b(?:TODO|TBD|PENDING|PLACEHOLDER)\b", all_target_text, flags=re.IGNORECASE), "Pending marker in Unit 5 target")
active_prose = "\n".join(body_text(path) for path in (LECTURE, WORKSHEET, SOLUTIONS))
german_hits = sorted(set(re.findall(r"\b(?:Aufgabe|Beweis|Körper|Menge|Punktmenge|Abbildung|Restklassenring|wenn|dann|nicht|seien|zeige|Punkte)\b", active_prose, flags=re.IGNORECASE)))
require(not german_hits, f"Active German prose remains: {german_hits}")

require_formulae(
    LECTURE,
    [
        r"R=S[X_1,\ldots,X_n]",
        r"G=X^\nu=X_1^{\nu_1}\cdots X_n^{\nu_n}",
        r"F_i=\sum_{\substack{\nu\\|\nu|=i}}a_\nu X^\nu",
        r"F=4X^3YZ^2+2X^2Y^5+5XYZ^7-3X^4YZ^4+X^8-Y^7+2Y^6Z^3+X+5",
        r"F_d=c(Y-e_1X)\cdots(Y-e_kX)X^{d-k}",
        r"\widetilde Y=Y-eX,\qquad\widetilde X=X",
        r"F=X^d+P_{d-1}(Y)X^{d-1}+\cdots+P_1(Y)X+P_0(Y)",
        r"\varphi^{-1}(V(F))=V(\widetilde\varphi(F))",
        r"\varphi_i=a_{i1}T_1+\cdots+a_{ir}T_r+c_i",
        r"K[X_1,\ldots,X_n]/\operatorname{Id}(V)\cong K[X_1,\ldots,X_n]/\operatorname{Id}(\widetilde V)",
        r"\widetilde\varphi^{-1}\bigl(\operatorname{Id}(\widetilde V)\bigr)=\operatorname{Id}(V)",
        r"K[Y]\longrightarrow K[X,Y]/\bigl(X^d+P_{d-1}(Y)X^{d-1}+\cdots+P_1(Y)X+P_0(Y)\bigr)",
        r"\overline B=V(\operatorname{Id}(B))",
        r"F(P)=F(\varphi(Q))=(F\circ\varphi)(Q)",
    ],
)
require_formulae(
    WORKSHEET,
    [
        r"X^n-Y^n\in\mathbb C[X,Y]",
        r"\mathfrak m^n=P_{\ge n}",
        r"X^2Y^3+5X^3Y^2-X^2Y^2+3Y+7\in\mathbb C[X,Y]",
        r"M=\{P_1,\ldots,P_n\}\subseteq K^2",
        r"F=X^2Y+3XY-Y^3",
        r"X\longmapsto T^2+S-3,\qquad Y\longmapsto 3TS+S^2-T",
        r"\operatorname{im}\varphi=\{P_1,\ldots,P_n\}",
        r"(X-\lambda_1)(X-\lambda_2)\cdots(X-\lambda_n)=P=c_0+c_1X+\cdots+c_{n-1}X^{n-1}+X^n",
        r"\overline{\varphi(T)}=\overline{\varphi(\overline T)}",
        r"Y=\frac{X^2-2X}{X^2-1}",
        r"E=V(2x^2+3y^2+4z^2-5)=\{(x,y,z):2x^2+3y^2+4z^2=5\}",
    ],
)
require_formulae(
    SOLUTIONS,
    [
        r"\widetilde F=a_n\prod_{i=1}^n(X-c_i)",
        r"F=a_n\prod_{i=1}^n(X-c_iY)",
        r"M=V(F)\cap V(G)",
        r"F'=Y-H+F",
        r"V(xy)=V(x)\cup V(y)",
        r"K[x,y]/(xy-\lambda)\longrightarrow K[u]_u",
        r"(\lambda_1,\lambda_2)\longmapsto(\lambda_1\lambda_2,-(\lambda_1+\lambda_2))",
        r"\mathord{\pm}\sum_{1\le i_1<i_2<\cdots<i_{n-k}\le n}\lambda_{i_1}\lambda_{i_2}\cdots\lambda_{i_{n-k}}",
        r"\prod_{i=1}^n(X-\lambda_i)=\sum_{j=0}^{n-1}c_jX^j+X^n=P",
        r"n!",
    ],
)
require(compact(r"\prod_{i=1}^n a_n") not in compact(solution_text), "Source coefficient-product typo remains active")
require(lecture_text.count("**Catatan edisi:**") == 2 and solution_text.count("**Catatan edisi:**") == 1, "Unit 5 edition-note closure mismatch")

with RIGHTS.open("r", encoding="utf-8", newline="") as stream:
    rights_rows = list(csv.DictReader(stream))
closure = json.loads(CLOSURE.read_text(encoding="utf-8"))
require(len(rights_rows) == 3, "Unit 5 rights row count mismatch")
require(closure["reader_media_positions"] == 3 and closure["unique_local_assets"] == 4, "Unit 5 asset closure mismatch")
require(closure["rights_sha256"] == digest(RIGHTS), "Unit 5 rights hash binding mismatch")
target_media_paths = re.findall(r"!\[[^\]]+\]\((authority/assets/[^)]+)\)", lecture_text + "\n" + worksheet_text)
require(target_media_paths == [row["local_path"] for row in rights_rows], "Reader media order/path mismatch")
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
require(len(correction_rows) == 16, "Correction-ledger row count changed unexpectedly")
correction_ids = {row["correction_id"] for row in correction_rows}
require({"AGC-CORR-0007", "AGC-CORR-0008", "AGC-CORR-0009"}.issubset(correction_ids), "Unit 5 correction records missing")

source_math = {
    "lecture": authority_math_count(AUTHORITY_DIR / manifest["lecture"]["html_file"]),
    "worksheet": authority_math_count(AUTHORITY_DIR / manifest["worksheet"]["html_file"]),
    "solutions": sum(authority_math_count(AUTHORITY_DIR / row["html_file"]) for row in mapped_rows),
}
require(source_math == {"lecture": 185, "worksheet": 98, "solutions": 54}, "Authority math counts changed")

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
    require(machine.get("status") == "PASS" and machine.get("through_unit") == 5, "Machine QA is not a Unit 5 PASS")
    require(visual.get("result") == "PASS" and visual.get("through_unit") == 5, "Visual QA is not a Unit 5 PASS")
    require(responsive.get("status") == "PASS" and responsive.get("through_unit") == 5, "Responsive QA is not a Unit 5 PASS")
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
    "unit": 5,
    "authority": {
        "manifest_path": rel(MANIFEST_PATH),
        "manifest_bytes": MANIFEST_PATH.stat().st_size,
        "manifest_sha256": digest(MANIFEST_PATH),
        "manifest_files_replayed": len(manifest["files"]),
        "manifest_file_mismatches": len(manifest_mismatches),
        "official_pdf_witnesses_replayed": len(manifest["official_pdf_witnesses"]),
        "official_pdf_mismatches": len(pdf_mismatches),
        "official_pdf_pages": pdf_pages,
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
        "exercises": 27,
        "practice_exercises": "5.1-5.22",
        "submission_exercises": "5.23-5.27",
        "submission_points": points,
        "starred_exercises": starred,
        "public_solutions": len(solution_ids),
        "solution_exercises": solution_ids,
        "solution_revisions": solution_revids,
        "broken_solution_links": 0,
        "untranslated_german_prose": 0,
        "media_positions": len(rights_rows),
        "binary_surfaces": closure["unique_local_assets"],
        "missing_media_positions": 0,
    },
    "math_count_reconciliation": {
        "lecture": {
            "authority_math_nodes": source_math["lecture"],
            "target_math_nodes": target_counts[LECTURE.name]["math_nodes"],
            "explanation": "The three-node net decrease comes from consolidating renderer-split hypotheses and aligned equalities after two explicit edition notes add coordinate and parameter-ring math nodes. Every theorem, factorization, substitution, quotient-ring, integral-extension, and image-closure formula is protected by replayable needles; the three source deltas are correction-ledger bound.",
        },
        "worksheet": {
            "authority_math_nodes": source_math["worksheet"],
            "target_math_nodes": target_counts[WORKSHEET.name]["math_nodes"],
            "explanation": "The two-node net increase results from separately typesetting the substitution homomorphism and image/fiber surfaces. All 27 tasks, four stars, five point values, hypotheses, maps, equations, and the ellipsoid position remain in exact source order.",
        },
        "solutions": {
            "authority_math_nodes": source_math["solutions"],
            "target_math_nodes": target_counts[SOLUTIONS.name]["math_nodes"],
            "explanation": "The four-node net increase is caused by the explicit corrected coefficient-product note and separately displayed intermediate identities. The four and only four public solutions remain source-bound; no unavailable solution was authored.",
        },
    },
    "fidelity_findings": {
        "protected_formula_needles": {"lecture": 14, "worksheet": 11, "solutions": 10},
        "fixed_before_build": [
            "Lecture 5's reversed ordered-pair referent is exposed and rendered with X=b, Y=a.",
            "Lecture 5's component-function ring uses the source's established T-parameters consistently.",
            "Solution 5.3's leading coefficient occurs once outside the factor product.",
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
        "unit_05_additions": 3,
    },
    "bound_qa": bound_qa,
}

RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": status, "receipt": rel(RECEIPT), "bytes": RECEIPT.stat().st_size, "sha256": digest(RECEIPT)}))
