#!/usr/bin/env python3
"""Fail-closed protected-mathematics QA through classical Unit 30."""

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
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-30.pdf"
OUT = ROOT / "qa" / "UNIT_30_PROTECTED_SURFACES.json"
BASELINE = ROOT / "qa" / "UNIT_28_PROTECTED_SURFACES.json"
MACHINE = ROOT / "qa" / "UNITS_01_30_MACHINE_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra."

FACTS = {
    BASELINE: (2533, "d9e737e3319f62d7560cbad20737c27b80b40c27536e3dca36d4632c98f18b2e"),
    MACHINE: (4526, "55e2044bc7423ba049adf9a1153c46c2dd957f5d147a85ee8ec1dfae3a850362"),
    ROOT / "qa" / "UNIT_29_TRANSLATION_QA.json": (6802, "7789a7a131bcf44946204f52c328e24fa96fee0c1e24383994d4485437bffb81"),
    ROOT / "qa" / "UNIT_30_TRANSLATION_QA.json": (6973, "788f6cb2245c5daef6a70fad25879c35d2234e43240e83be1bca1fc32c976916"),
    ROOT / "scripts" / "qa_unit29_translation.py": (21338, "cb400484aa6187c3ddba367f1ae24b6e7ed588cf0922d709134ff929313ca456"),
    ROOT / "scripts" / "qa_unit30_translation.py": (25461, "905031f60db2bc069da1edeb06273673631fc7746d5e9df1237e24ecab17440e"),
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


def fact(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular: {path}")
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }


def require_fact(path: Path) -> dict[str, Any]:
    row = fact(path)
    require((row["bytes"], row["sha256"]) == FACTS[path], f"identity drift: {row['path']}")
    return row


def normalize(value: str) -> str:
    return re.sub(r"\s+", "", value)


def literal_lists(path: Path) -> dict[str, list[str]]:
    wanted = {"protected_lecture", "protected_worksheet", "protected_solutions"}
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: dict[str, list[str]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or not isinstance(node.value, (ast.List, ast.Tuple)):
            continue
        names = [target.id for target in node.targets if isinstance(target, ast.Name)]
        for name in names:
            if name not in wanted:
                continue
            values = [
                item.value
                for item in node.value.elts
                if isinstance(item, ast.Constant) and isinstance(item.value, str)
            ]
            require(len(values) == len(node.value.elts), f"nonliteral protected list: {path.name}:{name}")
            require(name not in found, f"duplicate protected list: {path.name}:{name}")
            found[name] = values
    require(set(found) == wanted, f"protected lists incomplete: {path.name}")
    return found


def main() -> int:
    bound = {path.relative_to(ROOT).as_posix(): require_fact(path) for path in FACTS}
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    machine = json.loads(MACHINE.read_text(encoding="utf-8"))
    require(baseline.get("status") == "PASS" and baseline.get("through_unit") == 28,
            "Unit 28 protected baseline")
    require(machine.get("status") == "PASS" and machine.get("through_unit") == 30,
            "Unit 30 machine QA")
    require(machine.get("provenance") == MODEL, "machine provenance")

    annotations = [
        node.get_text()
        for node in BeautifulSoup(HTML.read_text(encoding="utf-8"), "html.parser").find_all("annotation")
        if node.get("encoding") == "application/x-tex"
    ]
    require(len(annotations) == machine["coverage"]["mathml_nodes"] == 11322,
            "MathML/TeX annotation count")
    annotation_blob = normalize("\n".join(annotations))

    unit_rows: dict[str, Any] = {}
    all_tokens: list[str] = []
    for unit in (29, 30):
        translation_path = ROOT / "qa" / f"UNIT_{unit}_TRANSLATION_QA.json"
        implementation = ROOT / "scripts" / f"qa_unit{unit}_translation.py"
        translation = json.loads(translation_path.read_text(encoding="utf-8"))
        require(translation.get("status") == "PASS" and translation.get("unit") == unit,
                f"Unit {unit} translation QA")
        require(translation.get("provenance") == MODEL, f"Unit {unit} provenance")
        lists = literal_lists(implementation)
        source_map = {
            "protected_lecture": SOURCE / f"lecture-{unit}.md",
            "protected_worksheet": SOURCE / f"worksheet-{unit}.md",
            "protected_solutions": SOURCE / f"worksheet-{unit}-solutions.md",
        }
        surface_rows: dict[str, Any] = {}
        for name, tokens in lists.items():
            require(tokens and len(tokens) == len(set(tokens)), f"Unit {unit} token topology: {name}")
            source_path = source_map[name]
            source_blob = normalize(source_path.read_text(encoding="utf-8"))
            missing_source = [token for token in tokens if normalize(token) not in source_blob]
            missing_html = [token for token in tokens if normalize(token) not in annotation_blob]
            require(not missing_source, f"Unit {unit} protected source missing: {missing_source}")
            require(not missing_html, f"Unit {unit} protected HTML missing: {missing_html}")
            source_row = fact(source_path)
            expected = translation["bound_facts"][source_row["path"]]
            require((source_row["bytes"], source_row["sha256"]) ==
                    (expected["bytes"], expected["sha256"]), f"Unit {unit} bound source drift: {name}")
            surface_rows[name] = {
                "source": source_row,
                "tokens": len(tokens),
                "source_missing": 0,
                "html_missing": 0,
            }
            all_tokens.extend(tokens)
        correction_ids = translation["translation"]["correction_bindings"]
        expected_corrections = (
            [f"AGC-CORR-{number:04d}" for number in range(126, 130)]
            if unit == 29 else
            [f"AGC-CORR-{number:04d}" for number in range(130, 136)]
        )
        require(correction_ids == expected_corrections, f"Unit {unit} correction interval")
        unit_rows[str(unit)] = {
            "translation_qa": bound[translation_path.relative_to(ROOT).as_posix()],
            "implementation": bound[implementation.relative_to(ROOT).as_posix()],
            "surfaces": surface_rows,
            "tokens": sum(len(tokens) for tokens in lists.values()),
            "correction_disclosures": correction_ids,
        }

    require(len(all_tokens) == 42, "Units 29-30 protected-token count")
    require(len(set(all_tokens)) >= 39, "Units 29-30 protected-token uniqueness")

    html_fact = fact(HTML)
    pdf_fact = fact(PDF)
    require((html_fact["bytes"], html_fact["sha256"]) ==
            (machine["html"]["bytes"], machine["html"]["sha256"]), "HTML/machine identity")
    require((pdf_fact["bytes"], pdf_fact["sha256"]) ==
            (machine["pdf"]["bytes"], machine["pdf"]["sha256"]), "PDF/machine identity")
    reader = PdfReader(PDF, strict=True)
    require(not reader.is_encrypted and len(reader.pages) == 504, "PDF page/encryption binding")
    terminal_text = normalize("\n".join((page.extract_text() or "") for page in reader.pages[468:]))
    pdf_markers = [
        "Kuliah 29: Proyeksi dan Kurva Proyektif Terparametrisasi",
        "Soal 29.10", "Solusi Soal 29.3",
        "Kuliah 30: Teorema Bézout", "Soal 30.12", "Solusi Soal 30.4",
        "Kredit media Unit 29", "Kredit media Unit 30",
    ]
    for marker in pdf_markers:
        require(normalize(marker) in terminal_text, f"terminal PDF marker missing: {marker}")

    receipt = {
        "schema": "ag-bridge-protected-surfaces-v6",
        "status": "PASS",
        "verified_date": "2026-08-28",
        "through_unit": 30,
        "baseline": bound[BASELINE.relative_to(ROOT).as_posix()],
        "machine_qa": bound[MACHINE.relative_to(ROOT).as_posix()],
        "units": unit_rows,
        "protected_token_count": len(all_tokens),
        "unique_protected_token_count": len(set(all_tokens)),
        "source_missing": 0,
        "html_missing": 0,
        "html_mathml_annotations": len(annotations),
        "pdf_terminal_pages_checked": 36,
        "pdf_terminal_markers": pdf_markers,
        "checks": [
            "accepted Unit 28 protected baseline is PASS and byte-pinned",
            "Unit 29 and Unit 30 translation receipts and their verifier implementations are byte-pinned",
            "all 42 selected mathematical surfaces remain in source and HTML TeX annotations",
            "all cumulative HTML/PDF identities match machine QA",
            "terminal PDF contains both final lectures, final exercises, public solutions, and media-credit boundaries",
            "all ten tracked Unit 29-30 corrections remain explicitly bound",
        ],
        "provenance": MODEL,
    }
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "receipt": OUT.relative_to(ROOT).as_posix(),
                      "bytes": OUT.stat().st_size, "sha256": digest(OUT),
                      "protected_tokens": len(all_tokens)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
