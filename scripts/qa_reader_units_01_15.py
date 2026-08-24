#!/usr/bin/env python3
"""Fail-closed cumulative reader QA through the frozen Unit 15 milestone.

Units 1--12 are bound to their previously audited receipts. Units 13--15 are
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
import qa_reader_units_01_12 as baseline  # noqa: E402


base = baseline.base
SOURCE = ROOT / "source" / "id-ID"
BUILD = ROOT / "build" / "reader-id"
QA = ROOT / "qa"
CSS = SOURCE / "reader.css"
PDF_HEADER = SOURCE / "pdf-header.tex"
HTML = BUILD / "index.html"
PDF = BUILD / "algebraic-geometry-bridge-id-units-01-15.pdf"
BUILD_RECEIPT = BUILD / "BUILD_RECEIPT.json"
HTML_LOG = BUILD / "pandoc-html.log"
PDF_LOG = BUILD / "pandoc-pdf.log"
CORRECTIONS = ROOT / "00_control" / "CORRECTIONS.csv"
OUT = QA / "UNITS_01_15_MACHINE_QA.json"

EXPECTED_PDF_PAGES = 267
EXPECTED_HTML_IMAGES = 69
EXPECTED_HTML_MATHML = 5989
EXPECTED_HTML_HEADINGS = {"h1": 62, "h2": 146, "h3": 585, "h4": 69, "h5": 0, "h6": 0}
EXPECTED_STABLE_IDS = 861
EXPECTED_EXERCISES = 423
EXPECTED_PUBLIC_SOLUTIONS = 75

FROZEN_BUILD = {
    "receipt": {"bytes": 26028, "sha256": "0468085b9dd2e98f1a8b586b53c2b4e4e16b93562a6d611acf26f09e18eeb7d2"},
    "html": {"bytes": 10196592, "sha256": "b4d6090cdaade5498e8021bab473497235f962e29fd28a2a9fb8e9a1f26ef4b9"},
    "pdf": {"bytes": 6502255, "sha256": "e56aae414a9d7e252485d06e7da790fae9bf972514c8fe47fc31d26eddd3699c"},
}

BASELINE_WITNESSES = {
    QA / "UNITS_01_12_MACHINE_QA.json": (16212, "55ccc57fb61a2dd69e802d816521460d919176f35c99838c1bb7109de3c5897e"),
    QA / "UNITS_01_12_VISUAL_QA.json": (3178, "ef306f95ac740dcc5d1a7192dbfd37c2189108eca9d1e671942a61e8cd18b5c6"),
    QA / "UNITS_01_12_RESPONSIVE_QA.json": (2792, "f53f433e1d4db1e2ba7a3e488e1d81f5e55f47750bf134842b931453f2a3bfe3"),
    QA / "UNIT_12_PROTECTED_SURFACES.json": (9411, "75c9725cb79bb3a4b3e7e889ca661310cc6fdef5e1fdaa91fa58ee4d58648b33"),
    ROOT / "scripts" / "qa_reader_units_01_12.py": (32036, "7d1a081287a65a5149ee4a8e1250707a0eaef904a312218557658914aa48a0e7"),
}

NEW_SOURCE_HASHES = {
    SOURCE / "frontmatter-units-01-15.md": (2887, "d0a7f7d3d8c76789212caef445f39b15b61caed88a1662ca825ba4956b628cb5"),
    SOURCE / "lecture-13.md": (14295, "6b2c8a6aac3c80a3bf45cdb83db085e59f72f09bb7829528f2719c6b7af178fa"),
    SOURCE / "worksheet-13.md": (16401, "b9dbf3ee514c8e7d59bdf60ba4617cb0b8a38b5e299cc65af53cdd8e7f56adcd"),
    SOURCE / "worksheet-13-solutions.md": (15292, "787b24f616ac7823c88b7f45ea827df5bbdea34be111bb36822d542121e89774"),
    SOURCE / "media-credits-unit-13.md": (742, "f5aa7d11bb7fd29860bdaec51fdb03790fdd6361e6f0ef2b4fbac72040de1341"),
    SOURCE / "lecture-14.md": (13617, "64b2519967638116cb3f98a2a200ad23efb5212e5c5c24b7f53e93ad2211f2d4"),
    SOURCE / "worksheet-14.md": (15430, "45dc11df386efc92ff537be1c53d7e2d9f16938be2fe5cd8eeb14eac347059cc"),
    SOURCE / "worksheet-14-solutions.md": (4048, "d64c25e2062d8a437465e7bb64d192e6d3ae347cdd6780c02e5146331cbe44dd"),
    SOURCE / "media-credits-unit-14.md": (403, "b7960d839016c9f6705c1fdba68685a889c1af3261d2339190931e5f9f8b3dc3"),
    SOURCE / "lecture-15.md": (16666, "e1affd57e9f9d33f7e85a2b8c8fe993ecd821d1fff1075588f51dca2014763b4"),
    SOURCE / "worksheet-15.md": (13700, "feb6d9c38b669718c548608865f416eb1b3a03ac2d1ce6fac92cb5a288f48784"),
    SOURCE / "worksheet-15-solutions.md": (6476, "49fecc0631064c646bd8fe2707f2ab84f8e33f32e9c4f99028b4dc9f508ec948"),
    SOURCE / "media-credits-unit-15.md": (424, "ccb29926735e5cdf47f628e2a66cf8c8e9017d64f3357a116e7e5abec3c41734"),
}

NEW_AST = {
    SOURCE / "frontmatter-units-01-15.md": {"headers": 2, "math": 0, "images": 0},
    SOURCE / "lecture-13.md": {"headers": 19, "math": 188, "images": 2},
    SOURCE / "worksheet-13.md": {"headers": 40, "math": 202, "images": 0, "exercises": 37},
    SOURCE / "worksheet-13-solutions.md": {"headers": 15, "math": 189, "images": 0, "solutions": 14},
    SOURCE / "media-credits-unit-13.md": {"headers": 1, "math": 0, "images": 0},
    SOURCE / "lecture-14.md": {"headers": 19, "math": 192, "images": 1},
    SOURCE / "worksheet-14.md": {"headers": 32, "math": 194, "images": 0, "exercises": 27},
    SOURCE / "worksheet-14-solutions.md": {"headers": 3, "math": 50, "images": 0, "solutions": 2},
    SOURCE / "media-credits-unit-14.md": {"headers": 1, "math": 0, "images": 0},
    SOURCE / "lecture-15.md": {"headers": 23, "math": 204, "images": 1},
    SOURCE / "worksheet-15.md": {"headers": 32, "math": 177, "images": 0, "exercises": 29},
    SOURCE / "worksheet-15-solutions.md": {"headers": 5, "math": 87, "images": 0, "solutions": 4},
    SOURCE / "media-credits-unit-15.md": {"headers": 1, "math": 0, "images": 0},
}

BASELINE_CONTENT = tuple(path for path in baseline.SOURCES if path.name != "frontmatter-units-01-12.md")
NEW_CONTENT = (
    SOURCE / "lecture-13.md",
    SOURCE / "worksheet-13.md",
    SOURCE / "worksheet-13-solutions.md",
    SOURCE / "media-credits-unit-13.md",
    SOURCE / "lecture-14.md",
    SOURCE / "worksheet-14.md",
    SOURCE / "worksheet-14-solutions.md",
    SOURCE / "media-credits-unit-14.md",
    SOURCE / "lecture-15.md",
    SOURCE / "worksheet-15.md",
    SOURCE / "worksheet-15-solutions.md",
    SOURCE / "media-credits-unit-15.md",
)
SOURCES = (SOURCE / "frontmatter-units-01-15.md", *BASELINE_CONTENT, *NEW_CONTENT)

EXPECTED_AST = dict(baseline.EXPECTED_AST)
EXPECTED_AST.update(NEW_AST)

CORRECTION_BINDINGS = {
    "AGC-CORR-0028": ("worksheet_13_exercise_13_29", "applied_at_unit_13_translation"),
    "AGC-CORR-0029": ("worksheet_solution_13_11", "applied_at_unit_13_translation"),
    "AGC-CORR-0030": ("worksheet_solution_13_20", "applied_at_unit_13_translation"),
    "AGC-CORR-0031": ("worksheet_solution_14_7", "applied_at_unit_14_translation"),
    "AGC-CORR-0032": ("lecture_15_colimit_representative", "applied_at_unit_15_translation"),
    "AGC-CORR-0033": ("worksheet_solution_15_19", "applied_at_unit_15_translation"),
}

UNIT_SPEC = {
    13: {
        "manifest_sha256": "dc86b4d124c7e775fb635a1f9672a8b8faadc4ff2259b0779f7bac6302d18848",
        "manifest_bytes": 149341,
        "files": 60,
        "revids": (1112285, 1065092),
        "transclusions": (142, 171),
        "map_sha256": "f954f09c996c8aa22f94ec826a1503b135a7b4fb9f9e0d5d6ff21f36a519e52a",
        "exercises": 37,
        "solutions": 14,
        "solution_numbers": [3, 6, 8, 9, 11, 14, 15, 17, 20, 21, 24, 27, 28, 31],
        "solution_revids": [1023890, 663088, 1112836, 1060069, 1023327, 1089391, 1029221, 1113410, 1095814, 1096486, 1060010, 1094892, 1089663, 1065090],
        "rights_sha256": "cdf370a6e3d7b80e137e6eb98a1180519b0cb97865ee39197de07c37e1a3c825",
        "closure_sha256": "771a8f09fd262838873e1390c43cae7da1f3989b74d8d2a7f67a856da9ea5e23",
        "positions": 2,
        "surfaces": 4,
        "official_pdfs": {
            "authority/artifacts/lecture-13-official.pdf": (242286, "185e4bfd91ff1814bed56af0c6eb619acaef772161b99232312d688c0690bd95", 7),
            "authority/artifacts/worksheet-13-official.pdf": (175801, "789444e8297ce0f896eb449a944c74e7555c959a01acfe66d329e05501c341bc", 9),
        },
    },
    14: {
        "manifest_sha256": "a63c3481d0a9cfa9b960f12c9bf0eec9a5d39cecfb61eddb8f9d96190e52e83e",
        "manifest_bytes": 123197,
        "files": 35,
        "revids": (1051343, 1061213),
        "transclusions": (106, 164),
        "map_sha256": "0d223f7f3c56c4714736dfc6eb3dbd40dc8cd3cb30a05f66281a6f2b1b875dbe",
        "exercises": 27,
        "solutions": 2,
        "solution_numbers": [2, 7],
        "solution_revids": [1068085, 1095255],
        "rights_sha256": "9c377f7c679ff0730bcd075201a4d587a322f004b118b0e31fc9c51b267e8973",
        "closure_sha256": "8fd50fae2515e6150e3d81c98573dd7bb204211e787d68405f7c3b03aab452d0",
        "positions": 1,
        "surfaces": 1,
        "official_pdfs": {
            "authority/artifacts/lecture-14-official.pdf": (935025, "2e8707f9041d6b9560c5e52a45981a3ee894ee47e747d9b4fd606a6998aa2241", 7),
            "authority/artifacts/worksheet-14-official.pdf": (169746, "352cccfd0d3ac8688ea25f179dfa6898b3fd2596f8c4b4ef2c198a65c50cde99", 9),
        },
    },
    15: {
        "manifest_sha256": "86e394725e766838f01eb035ca53044c4d3b85ff20eb99f8fecda9c2a0156425",
        "manifest_bytes": 116332,
        "files": 38,
        "revids": (1051357, 1062620),
        "transclusions": (116, 142),
        "map_sha256": "3c8c41458f5418ff858a58748ba4b23bc0a8cb34d9c386c155806b4482760470",
        "exercises": 29,
        "solutions": 4,
        "solution_numbers": [6, 9, 19, 22],
        "solution_revids": [663110, 1095144, 1112864, 1089392],
        "rights_sha256": "28ed5e373e07f80cef981315733e53069bdcf8f14c4447d1d21c3fabb2b5f4d7",
        "closure_sha256": "cdf6371ba9e44f9828f166f8da5ecfe4b6141e0b9ba0c7c02a5dfba156fea0a4",
        "positions": 1,
        "surfaces": 2,
        "official_pdfs": {
            "authority/artifacts/lecture-15-official.pdf": (206189, "f8682cc415719772732e897d005be59f1f261c24a7cb8b1b71886d972b1c92ed", 9),
            "authority/artifacts/worksheet-15-official.pdf": (160974, "242b92bb6c752d3ed4d49d1396f3643376c2e7140fd2e99db22b2b99eb99c59a", 7),
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
        base.require(path.stat().st_size == expected_bytes, f"Unit 12 baseline bytes changed: {rel(path)}")
        base.require(base.digest(path) == expected_hash, f"Unit 12 baseline hash changed: {rel(path)}")

    machine = json.loads((QA / "UNITS_01_12_MACHINE_QA.json").read_text(encoding="utf-8"))
    visual = json.loads((QA / "UNITS_01_12_VISUAL_QA.json").read_text(encoding="utf-8"))
    responsive = json.loads((QA / "UNITS_01_12_RESPONSIVE_QA.json").read_text(encoding="utf-8"))
    protected = json.loads((QA / "UNIT_12_PROTECTED_SURFACES.json").read_text(encoding="utf-8"))
    base.require(machine.get("status") == "PASS" and machine.get("through_unit") == 12, "Unit 12 machine baseline is not PASS")
    base.require(machine.get("stable_ids") == 670, "Unit 12 stable-ID baseline drift")
    base.require(machine.get("html", {}).get("images") == 65 and machine.get("html", {}).get("mathml_nodes") == 4499, "Unit 12 HTML baseline drift")
    base.require(machine.get("pdf", {}).get("pages") == 215, "Unit 12 PDF baseline drift")
    base.require(visual.get("result") == "PASS" and visual.get("through_unit") == 12, "Unit 12 visual baseline is not PASS")
    base.require(responsive.get("status") == "PASS" and responsive.get("through_unit") == 12, "Unit 12 responsive baseline is not PASS")
    base.require(protected.get("status") == "PASS" and protected.get("unit") == 12, "Unit 12 protected baseline is not PASS")
    expected_bound = {
        "machine": BASELINE_WITNESSES[QA / "UNITS_01_12_MACHINE_QA.json"][1],
        "visual": BASELINE_WITNESSES[QA / "UNITS_01_12_VISUAL_QA.json"][1],
        "responsive": BASELINE_WITNESSES[QA / "UNITS_01_12_RESPONSIVE_QA.json"][1],
    }
    base.require(
        {key: protected["bound_qa"][key]["sha256"] for key in expected_bound} == expected_bound,
        "Unit 12 protected receipt no longer binds the frozen QA triplet",
    )
    return {
        "through_unit": 12,
        "stable_ids": 670,
        "machine_sha256": expected_bound["machine"],
        "visual_sha256": expected_bound["visual"],
        "responsive_sha256": expected_bound["responsive"],
        "protected_sha256": BASELINE_WITNESSES[QA / "UNIT_12_PROTECTED_SURFACES.json"][1],
        "qa_script_sha256": BASELINE_WITNESSES[ROOT / "scripts" / "qa_reader_units_01_12.py"][1],
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
    base.require(len(SOURCES) == 60 and len(set(SOURCES)) == 60, "cumulative build-source closure")

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
    base.require("OpenAI Codex gpt-5.6-sol, Ultra." in raw_by_path[SOURCE / "frontmatter-units-01-15.md"], "exact model provenance absent")

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

    solution_summary = dict(json.loads((QA / "UNITS_01_12_MACHINE_QA.json").read_text(encoding="utf-8"))["solutions"])
    rights_summary = dict(json.loads((QA / "UNITS_01_12_MACHINE_QA.json").read_text(encoding="utf-8"))["rights"])
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
    base.require(receipt.get("through_unit") == 15 and receipt.get("language") == "id-ID", "build receipt scope/language")
    base.require(receipt.get("title") == "Kurva Aljabar - Unit 1-15", "build receipt title")
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
    base.require(soup.title is not None and soup.title.get_text(strip=True) == "Kurva Aljabar - Unit 1-15", "HTML title")
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
        "Kuliah 13: Himpunan Terbuka", "Soal 13.37 (6 poin)", "Solusi Soal 13.31", "Kredit media Unit 13",
        "Kuliah 14: Fungsi Aljabar pada Varietas", "Soal 14.27 (4 poin)", "Solusi Soal 14.7", "Kredit media Unit 14",
        "Kuliah 15: Varietas Afin dan Kuasiafin", "Soal 15.29 (4 poin)", "Solusi Soal 15.22", "Kredit media Unit 15",
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
    base.require(reader.metadata is not None and reader.metadata.title == "Kurva Aljabar - Unit 1-15", "PDF title metadata")
    base.require(reader.metadata.author == "Holger Brenner (karya sumber)", "PDF author metadata")
    for page_number, page in enumerate(reader.pages, start=1):
        width, height = float(page.mediabox.width), float(page.mediabox.height)
        base.require(abs(width - 595.28) < 0.05 and abs(height - 841.89) < 0.05, f"non-A4 PDF page: {page_number}")
    pdf_text = re.sub(r"\s+", " ", "\n".join(page.extract_text() or "" for page in reader.pages))
    for marker in ("Kuliah 13", "Soal 13.37", "Solusi Soal 13.31", "Kuliah 14", "Soal 14.27", "Solusi Soal 14.7", "Kuliah 15", "Soal 15.29", "Solusi Soal 15.22", "Kredit media Unit 15"):
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
        "through_unit": 15,
        "units_01_12_baseline": baseline_summary,
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
            "frozen_units_01_12_machine_visual_responsive_protected_and_script_receipts",
            "all_source_placeholder_german_mojibake_secret_provenance_and_stable_id_closure",
            "exact_pandoc_ast_math_image_heading_and_423_exercise_75_solution_topology",
            "units_13_15_solution_revision_witness_rights_asset_and_authority_pdf_replay",
            "six_exact_source_correction_ledger_bindings",
            "exact_unit_15_build_receipt_input_output_and_warning_free_log_replay",
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
