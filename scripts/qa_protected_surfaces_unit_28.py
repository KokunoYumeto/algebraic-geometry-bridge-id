#!/usr/bin/env python3
"""Fail-closed protected-surface QA for the cumulative Unit 28 reader."""

from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "id-ID"
HTML = ROOT / "build" / "reader-id" / "index.html"
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-28.pdf"
OUT = ROOT / "qa" / "UNIT_28_PROTECTED_SURFACES.json"
BASELINE = ROOT / "qa" / "UNIT_27_PROTECTED_SURFACES.json"
MACHINE = ROOT / "qa" / "UNITS_01_28_MACHINE_QA.json"
TRANSLATION = ROOT / "qa" / "UNIT_28_TRANSLATION_QA.json"
IMPLEMENTATION = ROOT / "scripts" / "qa_unit28_translation.py"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra."
BASELINE_FACT = (4122, "ca04c18753768b6741073342d47e6ba9fb6535b20382a29b53af20cb4be840ec")
MACHINE_FACT = (3083, "c666cb1186f516cead5ebd1a16de616856c99013cd94983826c974aebbdf776f")
TRANSLATION_FACT = (6913, "30095ba6d0621030c1a6d63d340ddb7d7d77fff424b2c28841d77e3e46da03ab")
IMPLEMENTATION_FACT = (18770, "a5f415df95328f66b0c61091b3197e620db309df98f110053e695aebbafbbb87")
PROTECTED_NAMES = {
    "protected_lecture": (SOURCE / "lecture-28.md", 9),
    "protected_worksheet": (SOURCE / "worksheet-28.md", 7),
    "protected_solution": (SOURCE / "worksheet-28-solutions.md", 3),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def normalize(value: str) -> str:
    return re.sub(r"\s+", "", value)


def fact(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular file: {path}")
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }


def require_fact(path: Path, expected: tuple[int, str], label: str) -> dict[str, Any]:
    row = fact(path)
    require((row["bytes"], row["sha256"]) == expected, f"{label} identity drift")
    return row


def literal_protected_lists() -> dict[str, list[str]]:
    tree = ast.parse(IMPLEMENTATION.read_text(encoding="utf-8"), filename=str(IMPLEMENTATION))
    found: dict[str, list[str]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, (ast.List, ast.Tuple)):
            continue
        names = [target.id for target in node.targets if isinstance(target, ast.Name)]
        for name in names:
            if name not in PROTECTED_NAMES:
                continue
            values = [
                item.value
                for item in node.value.elts
                if isinstance(item, ast.Constant) and isinstance(item.value, str)
            ]
            require(len(values) == len(node.value.elts), f"nonliteral protected list: {name}")
            require(name not in found, f"duplicate protected list: {name}")
            found[name] = values
    require(set(found) == set(PROTECTED_NAMES), "protected lists are incomplete")
    return found


def main() -> int:
    baseline_fact = require_fact(BASELINE, BASELINE_FACT, "Unit 27 protected baseline")
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    require(baseline.get("status") == "PASS" and baseline.get("through_unit") == 27, "Unit 27 protected baseline status/scope")

    machine_fact = require_fact(MACHINE, MACHINE_FACT, "Unit 28 machine QA")
    machine = json.loads(MACHINE.read_text(encoding="utf-8"))
    require(machine.get("status") == "PASS" and machine.get("through_unit") == 28, "Unit 28 machine status/scope")
    require(machine.get("provenance") == MODEL, "machine provenance")

    translation_fact = require_fact(TRANSLATION, TRANSLATION_FACT, "Unit 28 translation QA")
    implementation_fact = require_fact(IMPLEMENTATION, IMPLEMENTATION_FACT, "Unit 28 translation-QA implementation")
    translation = json.loads(TRANSLATION.read_text(encoding="utf-8"))
    require(translation.get("status") == "PASS" and translation.get("unit") == 28, "translation status/scope")
    require(translation.get("provenance") == MODEL, "translation provenance")

    bound = translation.get("bound_facts", {})
    required_sources = {
        "source/id-ID/lecture-28.md",
        "source/id-ID/worksheet-28.md",
        "source/id-ID/worksheet-28-solutions.md",
        "source/id-ID/media-credits-unit-28.md",
    }
    require(required_sources <= set(bound), "translation QA lacks Unit 28 source closure")
    for relative in required_sources:
        row = fact(ROOT / relative)
        expected = bound[relative]
        require((row["bytes"], row["sha256"]) == (expected["bytes"], expected["sha256"]), f"source identity drift: {relative}")

    lists = literal_protected_lists()
    all_tokens: list[str] = []
    surface_rows: dict[str, Any] = {}
    for name, (source, expected_count) in PROTECTED_NAMES.items():
        tokens = lists[name]
        require(len(tokens) == expected_count, f"protected-token count: {name}")
        require(len(tokens) == len(set(tokens)), f"duplicate protected token: {name}")
        normalized_source = normalize(source.read_text(encoding="utf-8"))
        missing = [token for token in tokens if normalize(token) not in normalized_source]
        require(not missing, f"protected source surface missing: {name}: {missing}")
        surface_rows[name] = {
            "source": source.relative_to(ROOT).as_posix(),
            "tokens": len(tokens),
            "source_missing": 0,
        }
        all_tokens.extend(tokens)
    require(len(all_tokens) == 19 and len(set(all_tokens)) == 18, "protected-token topology")

    correction_ids = translation.get("translation", {}).get("correction_bindings", [])
    require(correction_ids == [f"AGC-CORR-{number:04d}" for number in range(115, 126)], "Unit 28 correction interval")
    require(translation.get("translation", {}).get("visible_editorial_bridges") == 2, "editorial-bridge disclosures")

    html_fact = fact(HTML)
    require((html_fact["bytes"], html_fact["sha256"]) == (machine["html"]["bytes"], machine["html"]["sha256"]), "HTML/machine identity")
    soup = BeautifulSoup(HTML.read_text(encoding="utf-8"), "html.parser")
    annotations = [
        node.get_text()
        for node in soup.find_all("annotation")
        if node.get("encoding") == "application/x-tex"
    ]
    require(len(annotations) == machine["coverage"]["mathml_nodes"], "MathML/TeX annotation count")
    annotation_blob = normalize("\n".join(annotations))
    missing_html = [token for token in all_tokens if normalize(token) not in annotation_blob]
    require(not missing_html, f"protected HTML TeX surface missing: {missing_html}")

    pdf_fact = fact(PDF)
    require((pdf_fact["bytes"], pdf_fact["sha256"]) == (machine["pdf"]["bytes"], machine["pdf"]["sha256"]), "PDF/machine identity")
    reader = PdfReader(PDF, strict=True)
    require(not reader.is_encrypted and len(reader.pages) == machine["pdf"]["pages"] == 476, "PDF page/encryption binding")
    terminal_start = machine["pdf"]["terminal_start_page"]
    terminal_parts = [reader.pages[index].extract_text() or "" for index in range(terminal_start - 1, len(reader.pages))]
    terminal_blob = normalize("\n".join(terminal_parts))
    markers = [
        "Kuliah 28: Varietas Proyektif dan Kurva Bidang Proyektif",
        "Soal 28.14",
        "Solusi Soal 28.10",
        "Kredit media Unit 28",
    ]
    for marker in markers:
        require(normalize(marker) in terminal_blob, f"terminal PDF marker missing: {marker}")

    receipt = {
        "schema": "ag-bridge-protected-surfaces-v5",
        "status": "PASS",
        "verified_date": "2026-08-26",
        "through_unit": 28,
        "unit_27_baseline": baseline_fact,
        "machine_qa": machine_fact,
        "translation_qa": translation_fact,
        "translation_qa_implementation": implementation_fact,
        "unit_28": surface_rows,
        "protected_token_count": len(all_tokens),
        "unique_protected_token_count": len(set(all_tokens)),
        "source_missing": 0,
        "html_mathml_annotations": len(annotations),
        "html_missing": 0,
        "pdf_terminal_start_page": terminal_start,
        "pdf_terminal_pages_checked": len(terminal_parts),
        "pdf_terminal_markers": markers,
        "correction_disclosures": correction_ids,
        "editorial_bridge_disclosures": 2,
        "checks": [
            "exact Unit 27 protected-surface baseline is PASS and byte-pinned",
            "cumulative Unit 28 machine QA and output identities are PASS",
            "Unit 28 translation QA, implementation, and four-file source closure are byte-pinned",
            "nineteen protected mathematical tokens remain in source and HTML TeX annotations",
            "terminal PDF range contains the Unit 28 lecture, final exercise, sole public solution, and credits boundaries",
            "all eleven Unit 28 corrections and both editorial bridges are explicitly disclosed",
        ],
        "provenance": MODEL,
    }
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "receipt": OUT.relative_to(ROOT).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
