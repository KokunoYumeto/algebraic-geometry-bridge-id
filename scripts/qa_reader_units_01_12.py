#!/usr/bin/env python3
"""Fail-closed cumulative reader QA through the frozen Unit 12 milestone.

Units 1--9 are bound to their previously audited receipts.  Units 10--12 are
replayed directly from frozen source, authority, solution, rights, build, HTML,
and PDF surfaces.  The script intentionally refuses a merely similar rebuild.
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

from bs4 import BeautifulSoup
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import qa_reader_units_01_09 as baseline  # noqa: E402


base = baseline.base
SOURCE = ROOT / "source" / "id-ID"
BUILD = ROOT / "build" / "reader-id"
QA = ROOT / "qa"
CSS = SOURCE / "reader.css"
PDF_HEADER = SOURCE / "pdf-header.tex"
HTML = BUILD / "index.html"
PDF = BUILD / "algebraic-geometry-bridge-id-units-01-12.pdf"
BUILD_RECEIPT = BUILD / "BUILD_RECEIPT.json"
HTML_LOG = BUILD / "pandoc-html.log"
PDF_LOG = BUILD / "pandoc-pdf.log"
CORRECTIONS = ROOT / "00_control" / "CORRECTIONS.csv"
OUT = QA / "UNITS_01_12_MACHINE_QA.json"

EXPECTED_PDF_PAGES = 215
EXPECTED_HTML_IMAGES = 65
EXPECTED_HTML_MATHML = 4499
EXPECTED_HTML_HEADINGS = {"h1": 50, "h2": 113, "h3": 452, "h4": 56, "h5": 0, "h6": 0}
EXPECTED_STABLE_IDS = 670
EXPECTED_EXERCISES = 330
EXPECTED_PUBLIC_SOLUTIONS = 55

FROZEN_BUILD = {
    "receipt": {"bytes": 22731, "sha256": "9650aefa3dfd8c19c4e40c700e4c0afadc0c3c3599fa55cc46c28fec30000fdb"},
    "html": {"bytes": 9396856, "sha256": "29b8bc205bff3776ed231ac64064d8cfa53bbf42b1a674690a60c1b0fee8016d"},
    "pdf": {"bytes": 5981024, "sha256": "3213bee4e472c11c480bb2241077ffad4fb62d95ac590f3448a6fbd188c9159d"},
}

BASELINE_WITNESSES = {
    QA / "UNITS_01_09_MACHINE_QA.json": (10003, "da948c9c375a1f0e7e9e5ab8d0528b8ae6e0b38de7fb403b247d44a5ae76e3f7"),
    QA / "UNITS_01_09_VISUAL_QA.json": (45835, "adda6de86647d48deeebc3ac44ae638bf9d2fb4fa2c7e8cf82db6c7e113bd4e3"),
    QA / "UNITS_01_09_RESPONSIVE_QA.json": (2140, "25a3deddf8cf8b7f2830a843c6a6c4a7d0bf398641b6d4b49f8acc8911c9530a"),
    QA / "UNIT_09_PROTECTED_SURFACES.json": (3402, "0deab1dbe378cfc7cbc0061e210146250671749cff8ed84ee3c88667fe7fb5b0"),
    ROOT / "scripts" / "qa_reader_units_01_09.py": (7062, "dcc0e770891af732bed504fa1928c312638662151a040803340fb458c07ef245"),
}

NEW_SOURCE_HASHES = {
    SOURCE / "frontmatter-units-01-12.md": (2925, "b1ff35e4f17b8cab93489dc28eaab1d15b77f6212859a4cc9eae67527cabd8ce"),
    SOURCE / "lecture-10.md": (14540, "08a496387da53cefb7e1f427fa8d762465d31c18618be7ea897fe8246da21e6d"),
    SOURCE / "worksheet-10.md": (13115, "aa3a60bf17308df5d07ae88941eaf3cda9171a17e4ddd9e9c8c84053ee1d0f62"),
    SOURCE / "worksheet-10-solutions.md": (7794, "1ccbbc4377c44889f4659a54c6cba8e5314eb32b2443a9d74352aeb631a56a08"),
    SOURCE / "lecture-11.md": (15657, "268324606509f055a70c35d782982108763d58ccc2993e33e42d80e54aea4dcb"),
    SOURCE / "worksheet-11.md": (12609, "92f97d3eb40474184b678ba80c4f804b1d81600380fe14a322a19143905ecb39"),
    SOURCE / "worksheet-11-solutions.md": (2636, "9799331d7eb1ed32b3d9c092b54d5e77bad71dab831090065f347a0d50c3b2a2"),
    SOURCE / "media-credits-unit-11.md": (723, "423cdad2e676539994766627b9ff48aa20f337ea4b6ed806bee565481c50f7a3"),
    SOURCE / "lecture-12.md": (18692, "bab84765bec69ceef42a658579aa02162b45d4e1b2cdf55331031b1663596cd4"),
    SOURCE / "worksheet-12.md": (13722, "e4228a331ce1471dbef7e8f408ceaab309b8b92f51400a011998944e347fea99"),
    SOURCE / "worksheet-12-solutions.md": (3244, "aea4ad61cfc3bb7412f6690a850377c9418021aa5ff226173b51f9fb9b06d516"),
    SOURCE / "media-credits-unit-12.md": (1622, "aefe17911251cd292ae4431441f122003a5307b2b9205918809e5c077de593c0"),
}

NEW_AST = {
    SOURCE / "frontmatter-units-01-12.md": {"headers": 2, "math": 0, "images": 0},
    SOURCE / "lecture-10.md": {"headers": 21, "math": 231, "images": 0},
    SOURCE / "worksheet-10.md": {"headers": 32, "math": 186, "images": 0, "exercises": 29},
    SOURCE / "worksheet-10-solutions.md": {"headers": 7, "math": 98, "images": 0, "solutions": 6},
    SOURCE / "lecture-11.md": {"headers": 26, "math": 188, "images": 1},
    SOURCE / "worksheet-11.md": {"headers": 30, "math": 131, "images": 0, "exercises": 26},
    SOURCE / "worksheet-11-solutions.md": {"headers": 3, "math": 23, "images": 0, "solutions": 2},
    SOURCE / "media-credits-unit-11.md": {"headers": 1, "math": 0, "images": 0},
    SOURCE / "lecture-12.md": {"headers": 20, "math": 205, "images": 4},
    SOURCE / "worksheet-12.md": {"headers": 33, "math": 138, "images": 0, "exercises": 30},
    SOURCE / "worksheet-12-solutions.md": {"headers": 3, "math": 29, "images": 0, "solutions": 2},
    SOURCE / "media-credits-unit-12.md": {"headers": 1, "math": 0, "images": 0},
}

BASELINE_CONTENT = tuple(path for path in baseline.SOURCES if path.name != "frontmatter-units-01-09.md")
NEW_CONTENT = (
    SOURCE / "lecture-10.md",
    SOURCE / "worksheet-10.md",
    SOURCE / "worksheet-10-solutions.md",
    SOURCE / "lecture-11.md",
    SOURCE / "worksheet-11.md",
    SOURCE / "worksheet-11-solutions.md",
    SOURCE / "media-credits-unit-11.md",
    SOURCE / "lecture-12.md",
    SOURCE / "worksheet-12.md",
    SOURCE / "worksheet-12-solutions.md",
    SOURCE / "media-credits-unit-12.md",
)
SOURCES = (SOURCE / "frontmatter-units-01-12.md", *BASELINE_CONTENT, *NEW_CONTENT)

EXPECTED_AST = dict(baseline.EXPECTED)
EXPECTED_AST.update(NEW_AST)

CORRECTION_BINDINGS = {
    "AGC-ADAPT-0021": ("worksheet_solution_10_6", "applied_before_unit_12_build"),
    "AGC-ADAPT-0022": ("worksheet_solution_10_17", "applied_before_unit_12_build"),
    "AGC-CORR-0023": ("lecture_11_polynomial_induction", "applied_before_unit_12_build"),
    "AGC-ADAPT-0024": ("worksheet_11_exercise_11_19", "applied_before_unit_12_build"),
    "AGC-ADAPT-0025": ("worksheet_solution_12_6", "applied_before_unit_12_build"),
    "AGC-ADAPT-0026": ("lecture_12_spectrum_injection_proof", "applied_before_unit_12_build"),
    "AGC-CORR-0027": ("worksheet_solution_10_6", "applied_before_unit_12_release"),
}

UNIT_SPEC = {
    10: {
        "manifest_sha256": "f8b4f8bf12a0613f774352df31941d79a35d9eed10f2d8fb5570f9ffe07bfb43",
        "manifest_bytes": 128797,
        "files": 43,
        "revids": (1051326, 1058833),
        "transclusions": (124, 154),
        "map_sha256": "972e36256d128916533a33be1d2feedfdecbd133a0dbba96193a85477cf7e92c",
        "exercises": 29,
        "solutions": 6,
        "solution_numbers": [1, 6, 9, 16, 17, 20],
        "solution_revids": [1028855, 1068028, 1068729, 536882, 743216, 1112824],
        "rights_sha256": "688820e2de7916d7c3299fca0a3ce5d415cdb325e3061ffd5f9ca8220ffc617f",
        "closure_sha256": "981122ef8078677affd5735ffe022be8c08359717dc5794c21c7fb591fc15738",
        "positions": 0,
        "surfaces": 0,
        "official_pdfs": {
            "authority/artifacts/lecture-10-official.pdf": (173582, "f6b21e2efba10c44148c5a2ee07a4a2cccb7dbdbdc4642aa8cf6c4334c3d5085", 7),
            "authority/artifacts/worksheet-10-official.pdf": (149763, "0aa9a939acacb8022a80d532212986d881f6bf9ac37e238e60b4e2128459e0ba", 7),
        },
    },
    11: {
        "manifest_sha256": "ea2d4936bb27e88b2863f8fecbddd5570992c432aee66c72066597709da65a47",
        "manifest_bytes": 113533,
        "files": 34,
        "revids": (1051329, 1062657),
        "transclusions": (115, 129),
        "map_sha256": "6298bafd7656e4653b504706b437e89de7faa92a75fac10c31d51ad9644a20cf",
        "exercises": 26,
        "solutions": 2,
        "solution_numbers": [6, 7],
        "solution_revids": [1094883, 1112854],
        "rights_sha256": "54dd27757dc7a7a2084c2c333d0405483377d6e8ce4d52f2c3f3fdb487bfeb99",
        "closure_sha256": "eecc6bb22fbead45c6cdf064fcce66c3d39ca24453b35455b31f865212895c55",
        "positions": 1,
        "surfaces": 1,
        "official_pdfs": {
            "authority/artifacts/lecture-11-official.pdf": (181044, "5f608194d133bb71f94f52721ea3750711cf55af2bce576c8e80ac5255994250", 7),
            "authority/artifacts/worksheet-11-official.pdf": (141094, "c1a3247173b3b61820490e223e61871dfa06a15e9d51e202ca1f4f0259f647e8", 7),
        },
    },
    12: {
        "manifest_sha256": "181ce377bd68639b12511a9b1402ca03fd76c6107325195d3aa51a81b7286559",
        "manifest_bytes": 122858,
        "files": 35,
        "revids": (1112280, 1067822),
        "transclusions": (124, 143),
        "map_sha256": "a37f874ffa17dd35ed4375f2956786793e475fcd5e2ded0333207c546e7e91db",
        "exercises": 30,
        "solutions": 2,
        "solution_numbers": [6, 12],
        "solution_revids": [1068040, 1089724],
        "rights_sha256": "d645f9f0898da0d7b4c918900677f837846a3d16d5fb6424e77547ff2847b691",
        "closure_sha256": "058cd370d365150ea39a62ca0ed151189d6cf4b4e3cfcca27e9030eea148cea4",
        "positions": 4,
        "surfaces": 4,
        "official_pdfs": {
            "authority/artifacts/lecture-12-official.pdf": (209080, "a24ec1fac2445ad6c80ea84dea31021bbc8ebf3be16cd6e43accc88ed13b7bf3", 9),
            "authority/artifacts/worksheet-12-official.pdf": (147209, "7e4e7c66b6488b09a03d6ce381f701c2a8a9c5e91b83cd3b476b60981042ac07", 7),
        },
    },
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def require_regular(path: Path) -> None:
    base.require(path.is_file() and not path.is_symlink(), f"missing/nonregular input: {rel(path)}")


def visible_markdown(raw: str) -> str:
    raw = re.sub(r"\A---\s*\n.*?\n---\s*(?:\n|\Z)", "", raw, flags=re.S)
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    raw = re.sub(r"(?:^|\n)(?:```|~~~).*?(?:\n```|\n~~~)(?:\n|\Z)", "\n", raw, flags=re.S)
    raw = re.sub(r"`[^`\n]*`", "", raw)
    raw = re.sub(r"\]\([^)]*\)", "]", raw)
    return raw


def replay_baseline() -> dict:
    for path, (expected_bytes, expected_hash) in BASELINE_WITNESSES.items():
        require_regular(path)
        base.require(path.stat().st_size == expected_bytes, f"Unit 9 baseline bytes changed: {rel(path)}")
        base.require(base.digest(path) == expected_hash, f"Unit 9 baseline hash changed: {rel(path)}")

    machine = json.loads((QA / "UNITS_01_09_MACHINE_QA.json").read_text(encoding="utf-8"))
    visual = json.loads((QA / "UNITS_01_09_VISUAL_QA.json").read_text(encoding="utf-8"))
    responsive = json.loads((QA / "UNITS_01_09_RESPONSIVE_QA.json").read_text(encoding="utf-8"))
    protected = json.loads((QA / "UNIT_09_PROTECTED_SURFACES.json").read_text(encoding="utf-8"))
    base.require(machine.get("status") == "PASS" and machine.get("through_unit") == 9, "Unit 9 machine baseline is not PASS")
    base.require(machine.get("stable_ids") == 493, "Unit 9 stable-ID baseline drift")
    base.require(machine.get("html", {}).get("images") == 60 and machine.get("html", {}).get("mathml_nodes") == 3262, "Unit 9 HTML baseline drift")
    base.require(machine.get("pdf", {}).get("pages") == 174, "Unit 9 PDF baseline drift")
    base.require(visual.get("result") == "PASS" and visual.get("through_unit") == 9, "Unit 9 visual baseline is not PASS")
    base.require(responsive.get("status") == "PASS" and responsive.get("through_unit") == 9, "Unit 9 responsive baseline is not PASS")
    base.require(protected.get("status") == "PASS" and protected.get("unit") == 9, "Unit 9 protected baseline is not PASS")
    expected_bound = {
        "machine": BASELINE_WITNESSES[QA / "UNITS_01_09_MACHINE_QA.json"][1],
        "visual": BASELINE_WITNESSES[QA / "UNITS_01_09_VISUAL_QA.json"][1],
        "responsive": BASELINE_WITNESSES[QA / "UNITS_01_09_RESPONSIVE_QA.json"][1],
    }
    base.require(
        {key: protected["bound_qa"][key]["sha256"] for key in expected_bound} == expected_bound,
        "Unit 9 protected receipt no longer binds the frozen QA triplet",
    )
    return {
        "through_unit": 9,
        "stable_ids": 493,
        "machine_sha256": expected_bound["machine"],
        "visual_sha256": expected_bound["visual"],
        "responsive_sha256": expected_bound["responsive"],
        "protected_sha256": BASELINE_WITNESSES[QA / "UNIT_09_PROTECTED_SURFACES.json"][1],
        "qa_script_sha256": BASELINE_WITNESSES[ROOT / "scripts" / "qa_reader_units_01_09.py"][1],
    }


def verify_authority(unit: int, spec: dict) -> dict:
    directory = ROOT / "authority" / "wikiversity" / f"unit-{unit:02d}"
    path = directory / "UNIT_AUTHORITY_MANIFEST.json"
    require_regular(path)
    base.require(path.stat().st_size == spec["manifest_bytes"], f"Unit {unit} authority manifest bytes")
    base.require(base.digest(path) == spec["manifest_sha256"], f"Unit {unit} authority manifest identity")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    base.require(manifest.get("unit_number") == unit, f"Unit {unit} authority unit number")
    base.require((manifest["lecture"]["revid"], manifest["worksheet"]["revid"]) == spec["revids"], f"Unit {unit} authority revisions")
    for label, expected in zip(("lecture", "worksheet"), spec["transclusions"]):
        closure = manifest[f"{label}_transclusion_closure"]
        base.require(manifest[label]["template_count"] == expected, f"Unit {unit} {label} template count")
        base.require(closure["requested_template_count"] == expected, f"Unit {unit} {label} requested transclusions")
        base.require(closure["captured_page_count"] == expected, f"Unit {unit} {label} captured transclusions")
        base.require(closure["missing_page_count"] == 0, f"Unit {unit} {label} missing transclusion")
    base.require(len(manifest["files"]) == spec["files"], f"Unit {unit} authority file count")
    for row in manifest["files"]:
        witness = directory / row["file"]
        require_regular(witness)
        base.require(witness.stat().st_size == row["bytes"], f"Unit {unit} authority file bytes: {row['file']}")
        base.require(base.digest(witness) == row["sha256"], f"Unit {unit} authority file hash: {row['file']}")

    observed_pdf_paths = {row["local_path"] for row in manifest["official_pdf_witnesses"]}
    base.require(observed_pdf_paths == set(spec["official_pdfs"]), f"Unit {unit} official-PDF path closure")
    pdf_pages = {}
    for row in manifest["official_pdf_witnesses"]:
        expected_bytes, expected_hash, expected_pages = spec["official_pdfs"][row["local_path"]]
        witness = ROOT / row["local_path"]
        require_regular(witness)
        base.require(row["local_bytes"] == expected_bytes and row["local_sha256"] == expected_hash, f"Unit {unit} manifest PDF binding")
        base.require(witness.stat().st_size == expected_bytes and base.digest(witness) == expected_hash, f"Unit {unit} official PDF replay: {row['local_path']}")
        actual_pages = len(PdfReader(witness, strict=True).pages)
        base.require(actual_pages == expected_pages, f"Unit {unit} official PDF pages: {row['local_path']}")
        pdf_pages[row["local_path"]] = actual_pages
    return {
        "manifest_sha256": spec["manifest_sha256"],
        "manifest_files_replayed": len(manifest["files"]),
        "lecture_revid": spec["revids"][0],
        "worksheet_revid": spec["revids"][1],
        "lecture_transclusions": spec["transclusions"][0],
        "worksheet_transclusions": spec["transclusions"][1],
        "official_pdf_pages": pdf_pages,
    }


def verify_corrections() -> dict:
    require_regular(CORRECTIONS)
    with CORRECTIONS.open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    by_id = {row["correction_id"]: row for row in rows}
    base.require(len(by_id) == len(rows), "duplicate correction ID")
    for correction_id, (scope, status) in CORRECTION_BINDINGS.items():
        row = by_id.get(correction_id)
        base.require(row is not None, f"missing correction ledger row: {correction_id}")
        base.require(row["scope"] == scope, f"correction scope drift: {correction_id}")
        base.require(row["status"] == status, f"correction status drift: {correction_id}")
    return {
        "path": rel(CORRECTIONS),
        "bytes": CORRECTIONS.stat().st_size,
        "sha256": base.digest(CORRECTIONS),
        "rows": len(rows),
        "bindings": {key: {"scope": value[0], "status": value[1]} for key, value in CORRECTION_BINDINGS.items()},
    }


def main() -> int:
    baseline_summary = replay_baseline()
    for path in (*SOURCES, CSS, PDF_HEADER, HTML, PDF, BUILD_RECEIPT, HTML_LOG, PDF_LOG, CORRECTIONS):
        require_regular(path)
    base.require(len(SOURCES) == 48 and len(set(SOURCES)) == 48, "cumulative build-source closure")

    for path, (expected_bytes, expected_hash) in NEW_SOURCE_HASHES.items():
        base.require(path.stat().st_size == expected_bytes, f"frozen source bytes changed: {rel(path)}")
        base.require(base.digest(path) == expected_hash, f"frozen source hash changed: {rel(path)}")

    raw_by_path = {path: path.read_text(encoding="utf-8") for path in SOURCES}
    combined = "\n".join(raw_by_path.values())
    visible = "\n".join(visible_markdown(raw) for raw in raw_by_path.values())
    placeholder_re = re.compile(r"\b(?:TODO|TBD|FIXME|XXX|PLACEHOLDER|TRANSLATE)\b|pending_component_audit|<!--\s*QA:", re.I)
    secret_re = re.compile(r"github_pat_|ghp_[A-Za-z0-9]{20,}|ZENODO_ACCESS_TOKEN|access_token\s*[:=]", re.I)
    german_re = re.compile(r"\b(Es sei|Zeige|Beweise|Wir betrachten|Dann gilt|genau dann|Aufgabe|Beweis|Körper|Ring|Polynomring|Koordinatenring)\b")
    base.require(placeholder_re.search(combined) is None, "placeholder/unfinished marker in cumulative source")
    base.require(secret_re.search(combined) is None, "credential-shaped text in cumulative source")
    base.require(german_re.search(visible) is None, "active untranslated German prose in cumulative source")
    base.require("\ufffd" not in combined and "\x00" not in combined, "mojibake/NUL in cumulative source")
    base.require("\t" not in combined, "literal tab in cumulative source")
    base.require(re.search(r"!\[[^\]]*\]\(https?://", combined) is None, "remote image in cumulative source")
    base.require("OpenAI Codex gpt-5.6-sol, Ultra." in raw_by_path[SOURCE / "frontmatter-units-01-12.md"], "exact model provenance absent")

    ids: list[str] = []
    ast_summary: dict[str, dict[str, int]] = {}
    for path in SOURCES:
        ids.extend(base.source_ids(path))
        if path not in EXPECTED_AST:
            continue
        expectation = EXPECTED_AST[path]
        counts = base.ast_counts(base.pandoc_ast(path))
        for key, ast_key in (("headers", "Header"), ("math", "Math"), ("images", "Image")):
            base.require(counts.get(ast_key, 0) == expectation[key], f"{path.name} {ast_key} count")
        if "exercises" in expectation:
            observed = len(re.findall(r"^### Soal \d+\.\d+", raw_by_path[path], flags=re.M))
            base.require(observed == expectation["exercises"], f"{path.name} exercise count")
        if "solutions" in expectation:
            observed = len(re.findall(r"^## Solusi Soal \d+\.\d+", raw_by_path[path], flags=re.M))
            base.require(observed == expectation["solutions"], f"{path.name} public-solution count")
        ast_summary[path.name] = {key: counts.get(key, 0) for key in ("Header", "Math", "Image")}
    base.require(len(ids) == len(set(ids)) == EXPECTED_STABLE_IDS, f"stable-ID closure: {len(ids)}")
    base.require(all(identifier.startswith(("agc-", "br-ak-2025-2026-")) for identifier in ids), "noncanonical stable ID")
    base.require(sum(row.get("exercises", 0) for row in EXPECTED_AST.values()) == EXPECTED_EXERCISES, "cumulative exercise topology constant")
    base.require(sum(row.get("solutions", 0) for row in EXPECTED_AST.values()) == EXPECTED_PUBLIC_SOLUTIONS, "cumulative solution topology constant")

    solution_summary = dict(json.loads((QA / "UNITS_01_09_MACHINE_QA.json").read_text(encoding="utf-8"))["solutions"])
    rights_summary = dict(json.loads((QA / "UNITS_01_09_MACHINE_QA.json").read_text(encoding="utf-8"))["rights"])
    authority_summary = {}
    for unit, spec in UNIT_SPEC.items():
        map_path = ROOT / "authority" / "wikiversity" / f"unit-{unit:02d}" / "ORDERED_EXERCISE_MAP.json"
        rights_path = ROOT / "authority" / f"RIGHTS-unit-{unit:02d}.csv"
        closure_path = ROOT / "authority" / f"ASSET_CLOSURE-unit-{unit:02d}.json"
        base.require(base.digest(map_path) == spec["map_sha256"], f"Unit {unit} exercise-map identity")
        base.require(base.digest(rights_path) == spec["rights_sha256"], f"Unit {unit} rights identity")
        base.require(base.digest(closure_path) == spec["closure_sha256"], f"Unit {unit} asset-closure identity")
        summary = base.verify_solution_map(unit, SOURCE / f"worksheet-{unit:02d}-solutions.md", spec["exercises"], spec["solutions"])
        mapping = json.loads(map_path.read_text(encoding="utf-8"))
        public = [row for row in mapping["entries"] if row.get("has_public_solution")]
        base.require([row["exercise_number"] for row in public] == spec["solution_numbers"], f"Unit {unit} public-solution numbers")
        base.require([row["revid"] for row in public] == spec["solution_revids"], f"Unit {unit} public-solution revisions")
        solution_summary[f"unit_{unit:02d}"] = summary
        rights_summary[f"unit_{unit:02d}"] = base.verify_rights(
            f"RIGHTS-unit-{unit:02d}.csv", f"ASSET_CLOSURE-unit-{unit:02d}.json", spec["positions"], spec["surfaces"]
        )
        authority_summary[f"unit_{unit:02d}"] = verify_authority(unit, spec)

    correction_summary = verify_corrections()

    base.require(BUILD_RECEIPT.stat().st_size == FROZEN_BUILD["receipt"]["bytes"], "build receipt bytes changed")
    base.require(base.digest(BUILD_RECEIPT) == FROZEN_BUILD["receipt"]["sha256"], "build receipt hash changed")
    receipt = json.loads(BUILD_RECEIPT.read_text(encoding="utf-8"))
    base.require(receipt.get("schema") == "ag-bridge-build-receipt-v2", "build receipt schema")
    base.require(receipt.get("through_unit") == 12 and receipt.get("language") == "id-ID", "build receipt scope/language")
    base.require(receipt.get("title") == "Kurva Aljabar - Unit 1-12", "build receipt title")
    input_paths: set[str] = set()
    root_resolved = ROOT.resolve()
    for row in receipt.get("inputs", []):
        relative = Path(row["path"])
        path = (ROOT / relative).resolve()
        base.require(path.is_relative_to(root_resolved), f"build input escapes lane: {row['path']}")
        base.require(row["path"] not in input_paths, f"duplicate build input: {row['path']}")
        input_paths.add(row["path"])
        require_regular(path)
        base.require(path.stat().st_size == row["bytes"] and base.digest(path) == row["sha256"], f"build input replay: {row['path']}")
    required_inputs = {rel(path) for path in SOURCES} | {rel(CSS), rel(PDF_HEADER)}
    base.require(required_inputs <= input_paths, "build receipt omits a cumulative reader input")
    output_rows = {row["path"]: row for row in receipt.get("outputs", [])}
    base.require(set(output_rows) == {rel(PDF), rel(HTML)}, "build output closure")
    for path, key in ((HTML, "html"), (PDF, "pdf")):
        expected = FROZEN_BUILD[key]
        row = output_rows[rel(path)]
        base.require(path.stat().st_size == expected["bytes"] == row["bytes"], f"{key.upper()} bytes")
        base.require(base.digest(path) == expected["sha256"] == row["sha256"], f"{key.upper()} hash")

    html_text_raw = HTML.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_text_raw, "html.parser")
    base.require(soup.html is not None and soup.html.get("lang") == "id-ID", "HTML language")
    base.require(soup.title is not None and soup.title.get_text(strip=True) == "Kurva Aljabar - Unit 1-12", "HTML title")
    dom_ids = [node.get("id") for node in soup.find_all(id=True)]
    base.require(len(dom_ids) == len(set(dom_ids)), "duplicate HTML ID")
    for identifier in ids:
        base.require(dom_ids.count(identifier) == 1, f"HTML source-ID closure: {identifier}")
    html_id_set = set(dom_ids)
    broken_internal = sorted(
        href[1:]
        for node in soup.find_all(href=True)
        if (href := unquote(node.get("href", ""))).startswith("#") and href[1:] not in html_id_set
    )
    base.require(not broken_internal, f"broken internal HTML links: {broken_internal[:5]}")
    images = soup.find_all("img")
    base.require(len(images) == EXPECTED_HTML_IMAGES, f"HTML image count: {len(images)}")
    base.require(all(image.get("alt", "").strip() for image in images), "missing HTML image alt text")
    base.require(all(image.get("src", "").startswith("data:image/") for image in images), "nonembedded/remote HTML image")
    mathml_nodes = len(soup.find_all("math"))
    base.require(mathml_nodes == EXPECTED_HTML_MATHML, f"HTML MathML count: {mathml_nodes}")
    heading_counts = Counter(node.name for node in soup.find_all(re.compile(r"^h[1-6]$")))
    observed_headings = {level: heading_counts.get(level, 0) for level in EXPECTED_HTML_HEADINGS}
    base.require(observed_headings == EXPECTED_HTML_HEADINGS, f"HTML heading topology: {observed_headings}")
    html_visible = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
    for marker in (
        "Kuliah 10: Modul Noether dan Nullstellensatz Hilbert", "Soal 10.29 - 3 poin", "Solusi Soal 10.20",
        "Kuliah 11: Nullstellensatz Hilbert dan Gelanggang Koordinat", "Soal 11.26 (4 poin)", "Solusi Soal 11.7", "Kredit media Unit 11",
        "Kuliah 12:", "Funktorialitasnya", "Soal 12.30 (5 poin)", "Solusi Soal 12.12", "Kredit media Unit 12",
    ):
        base.require(marker in html_visible, f"HTML milestone marker absent: {marker}")
    base.require(placeholder_re.search(html_text_raw) is None, "placeholder in HTML")
    base.require(secret_re.search(html_text_raw) is None, "credential-shaped text in HTML")

    css_text = CSS.read_text(encoding="utf-8")
    base.require('math[display="block"]' in css_text and "overflow-x: auto" in css_text, "responsive display-math CSS absent")
    base.require("overflow-wrap: anywhere" in css_text, "long-link wrapping CSS absent")
    header_text = PDF_HEADER.read_text(encoding="utf-8")
    base.require("\\usepackage{pifont}" in header_text, "PDF source-star fallback absent")
    base.require("\\renewcommand\\subsubsection" in header_text, "PDF block-heading reflow absent")
    for log in (HTML_LOG, PDF_LOG):
        base.require(log.stat().st_size == 0, f"nonempty Pandoc log: {log.name}")
        base.require(re.search(r"Warning|Error|Missing|not found|Overfull|Underfull", log.read_text(encoding="utf-8"), flags=re.I) is None, f"build warning: {log.name}")

    reader = PdfReader(PDF, strict=True)
    base.require(not reader.is_encrypted, "PDF encrypted")
    base.require(len(reader.pages) == EXPECTED_PDF_PAGES, f"PDF pages: {len(reader.pages)}")
    base.require(reader.metadata is not None and reader.metadata.title == "Kurva Aljabar - Unit 1-12", "PDF title metadata")
    base.require(reader.metadata.author == "Holger Brenner (karya sumber)", "PDF author metadata")
    for page_number, page in enumerate(reader.pages, start=1):
        width, height = float(page.mediabox.width), float(page.mediabox.height)
        base.require(abs(width - 595.28) < 0.05 and abs(height - 841.89) < 0.05, f"non-A4 PDF page: {page_number}")
    pdf_text = re.sub(r"\s+", " ", "\n".join(page.extract_text() or "" for page in reader.pages))
    for marker in ("Kuliah 10", "Soal 10.29", "Solusi Soal 10.20", "Kuliah 11", "Soal 11.26", "Solusi Soal 11.7", "Kuliah 12", "Soal 12.30", "Solusi Soal 12.12", "Kredit media Unit 12"):
        base.require(marker in pdf_text, f"PDF milestone marker absent: {marker}")
    base.require(placeholder_re.search(pdf_text) is None, "placeholder in PDF text")
    base.require(secret_re.search(pdf_text) is None, "credential-shaped text in PDF text")

    pdffonts = base.shutil.which("pdffonts")
    base.require(bool(pdffonts), "pdffonts unavailable")
    fonts = subprocess.run([pdffonts, str(PDF)], capture_output=True, text=True, encoding="utf-8", check=True).stdout
    font_rows = [line for line in fonts.splitlines()[2:] if line.strip()]
    parsed_fonts = [re.search(r"\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", line) for line in font_rows]
    base.require(font_rows and all(match is not None for match in parsed_fonts), "unparseable pdffonts output")
    base.require(all(match.group(1) == "yes" for match in parsed_fonts if match), "PDF contains an unembedded font")
    base.require(all("Type 3" not in line for line in font_rows), "PDF contains a Type 3 font")
    base.require(any("Dingbats" in line or "Zapf" in line for line in font_rows), "PDF source-star fallback font absent")

    result = {
        "schema": "ag-bridge-machine-qa-receipt-v4",
        "tested_build_utc": receipt["built_utc"],
        "status": "PASS",
        "through_unit": 12,
        "units_01_09_baseline": baseline_summary,
        "stable_ids": len(ids),
        "exercise_count": EXPECTED_EXERCISES,
        "public_solution_count": EXPECTED_PUBLIC_SOLUTIONS,
        "ast_surfaces": ast_summary,
        "frozen_source_hashes": {
            rel(path): {"bytes": expected[0], "sha256": expected[1]} for path, expected in NEW_SOURCE_HASHES.items()
        },
        "solutions": solution_summary,
        "rights": rights_summary,
        "authority": authority_summary,
        "corrections_ledger": correction_summary,
        "html": {
            "bytes": HTML.stat().st_size,
            "sha256": base.digest(HTML),
            "images": len(images),
            "mathml_nodes": mathml_nodes,
            "heading_levels": observed_headings,
            "dom_ids": len(dom_ids),
            "source_ids_closed": len(ids),
            "broken_internal_links": 0,
            "remote_or_unembedded_images": 0,
            "missing_alt_text": 0,
            "build_warnings": 0,
            "responsive_css_sha256": base.digest(CSS),
        },
        "pdf": {
            "bytes": PDF.stat().st_size,
            "sha256": base.digest(PDF),
            "pages": len(reader.pages),
            "page_size": "A4 (595.28 x 841.89 pt)",
            "encrypted": False,
            "font_rows": len(font_rows),
            "unembedded_fonts": 0,
            "type3_fonts": 0,
            "build_warnings": 0,
            "source_star_fallback_embedded": True,
            "block_heading_reflow": True,
        },
        "build_receipt": {
            "path": rel(BUILD_RECEIPT),
            "bytes": BUILD_RECEIPT.stat().st_size,
            "sha256": base.digest(BUILD_RECEIPT),
            "inputs_replayed": len(receipt["inputs"]),
            "outputs_replayed": len(receipt["outputs"]),
        },
        "qa_script": {"path": rel(Path(__file__)), "sha256": base.digest(Path(__file__))},
        "check_families": [
            "frozen_units_01_09_machine_visual_responsive_protected_and_script_receipts",
            "all_source_placeholder_german_mojibake_secret_provenance_and_stable_id_closure",
            "exact_pandoc_ast_math_image_heading_and_330_exercise_55_solution_topology",
            "units_10_12_solution_revision_witness_rights_asset_and_authority_pdf_replay",
            "six_exact_source_correction_ledger_bindings",
            "exact_unit_12_build_receipt_input_output_and_warning_free_log_replay",
            "html_language_heading_mathml_alt_embedded_image_internal_link_and_id_closure",
            "pdf_a4_metadata_text_embedded_fonts_star_fallback_and_heading_reflow",
        ],
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "receipt": rel(OUT), "bytes": OUT.stat().st_size, "sha256": base.digest(OUT)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
