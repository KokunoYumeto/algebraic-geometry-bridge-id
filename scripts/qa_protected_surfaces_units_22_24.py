#!/usr/bin/env python3
"""Verify protected mathematical surfaces for cumulative Units 22--24."""

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
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-24.pdf"
OUT = ROOT / "qa" / "UNIT_24_PROTECTED_SURFACES.json"
BASELINE = ROOT / "qa" / "UNIT_21_PROTECTED_SURFACES.json"
MACHINE = ROOT / "qa" / "UNITS_01_24_MACHINE_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra."
BASELINE_FACT = (1977, "35eee319508f364c73f32627ffb69b376bd15bb978e4d1694765dc06538eb6ba")


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


def literal_string_lists(script: Path) -> list[list[str]]:
    """Return literal protected-token candidates without executing QA code."""
    tree = ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
    candidates: list[list[str]] = []
    for node in ast.walk(tree):
        value: ast.AST | None = None
        names: list[str] = []
        if isinstance(node, ast.Assign):
            value = node.value
            names = [target.id for target in node.targets if isinstance(target, ast.Name)]
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            value = node.value
            names = [node.target.id]
        if value is None or not any("protected" in name.casefold() for name in names):
            continue
        try:
            literal = ast.literal_eval(value)
        except (ValueError, TypeError, SyntaxError):
            continue
        if isinstance(literal, (list, tuple)) and literal and all(isinstance(item, str) for item in literal):
            candidates.append(list(literal))
    return candidates


def protected_tokens(unit: int, expected_count: int) -> tuple[Path, list[str]]:
    script = ROOT / "scripts" / f"qa_unit{unit}_translation.py"
    require(script.is_file() and not script.is_symlink(), f"missing Unit {unit} translation QA implementation")
    matching = [tokens for tokens in literal_string_lists(script) if len(tokens) == expected_count]
    require(len(matching) == 1, f"Unit {unit} protected-token literal is absent or ambiguous")
    require(len(matching[0]) == len(set(matching[0])), f"Unit {unit} protected-token list contains duplicates")
    return script, matching[0]


def source_facts(payload: dict[str, Any], unit: int) -> dict[str, tuple[int, str]]:
    rows = payload.get("translation", {}).get("source_and_control_facts", [])
    result: dict[str, tuple[int, str]] = {}
    expected = {
        f"source/id-ID/lecture-{unit:02d}.md",
        f"source/id-ID/worksheet-{unit:02d}.md",
        f"source/id-ID/worksheet-{unit:02d}-solutions.md",
        f"source/id-ID/media-credits-unit-{unit:02d}.md",
    }
    for row in rows:
        if row.get("path") in expected:
            result[row["path"]] = (row["bytes"], row["sha256"])
    require(set(result) == expected, f"Unit {unit} QA lacks exact four-file source closure")
    return result


def correction_bindings(payload: dict[str, Any]) -> list[str]:
    translation = payload.get("translation", {})
    values: list[str] = []
    for key, value in translation.items():
        if "binding" not in key.casefold() or not isinstance(value, list):
            continue
        values.extend(item for item in value if isinstance(item, str) and item.startswith("AGC-CORR-"))
    return values


def first_heading(raw: str, level: int) -> str:
    match = re.search(rf"^{'#' * level}\s+(.+?)(?:\s+\{{#[^}}]+\}})?\s*$", raw, flags=re.M)
    require(match is not None, f"missing level-{level} heading")
    return match.group(1).strip()


def last_numbered_heading(raw: str, prefix: str, unit: int) -> str:
    matches = re.findall(rf"^#+\s+({re.escape(prefix)}\s+{unit}\.\d+)\b.*$", raw, flags=re.M)
    require(matches, f"missing {prefix} heading for Unit {unit}")
    return matches[-1]


def main() -> int:
    baseline = fact(BASELINE)
    require((baseline["bytes"], baseline["sha256"]) == BASELINE_FACT, "Unit 21 protected baseline drift")
    baseline_payload = json.loads(BASELINE.read_text(encoding="utf-8"))
    require(baseline_payload.get("status") == "PASS" and baseline_payload.get("through_unit") == 21, "Unit 21 protected baseline status/scope")

    machine = json.loads(MACHINE.read_text(encoding="utf-8"))
    require(machine.get("status") == "PASS" and machine.get("through_unit") == 24, "cumulative Unit 24 machine QA status/scope")
    require(machine.get("provenance") == MODEL, "cumulative machine-QA provenance")

    unit_qas: dict[int, dict[str, Any]] = {}
    source_checks: dict[str, dict[str, Any]] = {}
    all_tokens: list[str] = []
    all_corrections: list[str] = []
    pdf_markers: list[str] = []
    qa_facts: list[dict[str, Any]] = []
    for unit in range(22, 25):
        qa_path = ROOT / "qa" / f"UNIT_{unit}_TRANSLATION_QA.json"
        payload = json.loads(qa_path.read_text(encoding="utf-8"))
        require(payload.get("status") == "PASS" and payload.get("unit") == unit, f"Unit {unit} translation QA status/scope")
        require(payload.get("provenance") == MODEL, f"Unit {unit} translation QA provenance")
        unit_qas[unit] = payload
        qa_facts.append(fact(qa_path))

        bound_sources = source_facts(payload, unit)
        raw_parts: list[str] = []
        for relative, expected in bound_sources.items():
            path = ROOT / relative
            require(path.is_file() and not path.is_symlink(), f"Unit {unit} source missing/nonregular: {relative}")
            require((path.stat().st_size, digest(path)) == expected, f"Unit {unit} source/QA identity drift: {relative}")
            if path.name != f"media-credits-unit-{unit:02d}.md":
                raw_parts.append(path.read_text(encoding="utf-8"))
        core_raw = "\n".join(raw_parts)
        core_ids = set(re.findall(r"\{#([A-Za-z][A-Za-z0-9_.:-]*)\}", core_raw))
        edition_slug = "2012" if unit == 24 else "2025-2026"
        require(
            {
                f"br-ak-{edition_slug}-l{unit:02d}",
                f"br-ak-{edition_slug}-w{unit:02d}",
                f"br-ak-{edition_slug}-w{unit:02d}-solutions",
            }
            <= core_ids,
            f"Unit {unit} source-edition stable-root transition",
        )
        wrong_slug = "2025-2026" if unit == 24 else "2012"
        require(not any(identifier.startswith(f"br-ak-{wrong_slug}-") for identifier in core_ids), f"Unit {unit} wrong source-edition stable-ID namespace")

        expected_count = payload.get("translation", {}).get("protected_math_checks")
        require(isinstance(expected_count, int) and expected_count > 0, f"Unit {unit} protected-math count")
        qa_script, tokens = protected_tokens(unit, expected_count)
        normalized = normalize(core_raw)
        missing = [token for token in tokens if normalize(token) not in normalized]
        require(not missing, f"protected source math absent in Unit {unit}: {missing}")
        source_checks[str(unit)] = {
            "tokens": len(tokens),
            "source_files": 3,
            "missing": 0,
            "translation_qa": fact(qa_path),
            "translation_qa_implementation": fact(qa_script),
        }
        all_tokens.extend(tokens)
        all_corrections.extend(correction_bindings(payload))

        lecture_raw = (SOURCE / f"lecture-{unit:02d}.md").read_text(encoding="utf-8")
        worksheet_raw = (SOURCE / f"worksheet-{unit:02d}.md").read_text(encoding="utf-8")
        solutions_raw = (SOURCE / f"worksheet-{unit:02d}-solutions.md").read_text(encoding="utf-8")
        pdf_markers.extend((first_heading(lecture_raw, 1), last_numbered_heading(worksheet_raw, "Soal", unit)))
        if re.search(rf"^##\s+Solusi Soal\s+{unit}\.\d+", solutions_raw, flags=re.M):
            pdf_markers.append(last_numbered_heading(solutions_raw, "Solusi Soal", unit))

    require(len(all_tokens) == len(set(all_tokens)), "cross-unit protected-token duplicate")
    require(len(all_corrections) == len(set(all_corrections)), "cross-unit correction binding duplicate")
    if all_corrections:
        numbers = sorted(int(value.rsplit("-", 1)[1]) for value in all_corrections)
        require(numbers == list(range(71, numbers[-1] + 1)), "Units 22--24 correction binding interval is not contiguous from AGC-CORR-0071")

    html_fact = fact(HTML)
    require((html_fact["bytes"], html_fact["sha256"]) == (machine["html"]["bytes"], machine["html"]["sha256"]), "HTML/machine identity binding")
    soup = BeautifulSoup(HTML.read_text(encoding="utf-8"), "html.parser")
    annotations = [tag.get_text() for tag in soup.find_all("annotation") if tag.get("encoding") == "application/x-tex"]
    annotation_blob = normalize("\n".join(annotations))
    missing_html = [token for token in all_tokens if normalize(token) not in annotation_blob]
    require(not missing_html, f"protected TeX annotations absent from HTML: {missing_html}")
    require(len(annotations) == machine["coverage"]["mathml_nodes"], "HTML TeX annotations/machine MathML binding")

    pdf_fact = fact(PDF)
    require((pdf_fact["bytes"], pdf_fact["sha256"]) == (machine["pdf"]["bytes"], machine["pdf"]["sha256"]), "PDF/machine identity binding")
    reader = PdfReader(PDF, strict=True)
    require(not reader.is_encrypted and len(reader.pages) == machine["pdf"]["pages"], "PDF encryption/page binding")
    terminal_start = machine["pdf"]["terminal_start_page"]
    require(isinstance(terminal_start, int) and 1 <= terminal_start <= len(reader.pages), "terminal start page")
    terminal_parts = [reader.pages[index].extract_text() or "" for index in range(terminal_start - 1, len(reader.pages))]
    terminal_text = "\n".join(terminal_parts)
    compact_terminal_text = re.sub(r"\s+", "", terminal_text)
    for marker in pdf_markers:
        require(
            re.sub(r"\s+", "", marker) in compact_terminal_text,
            f"protected terminal PDF marker absent: {marker}",
        )

    receipt = {
        "schema": "ag-bridge-protected-surfaces-v4",
        "status": "PASS",
        "verified_date": "2026-08-25",
        "through_unit": 24,
        "unit_21_baseline": baseline,
        "machine_qa": fact(MACHINE),
        "units_22_24": source_checks,
        "protected_token_count": len(all_tokens),
        "source_missing": 0,
        "html_mathml_annotations": len(annotations),
        "html_missing": 0,
        "pdf_terminal_start_page": terminal_start,
        "pdf_terminal_pages_checked": len(terminal_parts),
        "pdf_terminal_markers": pdf_markers,
        "correction_and_bridge_disclosures": all_corrections,
        "checks": [
            "exact Unit 21 protected-surface baseline is PASS and byte-pinned",
            "cumulative Unit 24 machine QA and output identities are PASS",
            "Units 22-24 translation math gates and source identities are PASS",
            "protected token lists are extracted without executing their per-unit QA implementations",
            "all protected source formulas survive as HTML TeX annotations",
            "measured terminal PDF range contains every Unit 22-24 lecture, worksheet, and public-solution boundary",
            "all Unit 22-24 correction bindings form one deduplicated contiguous ledger interval",
        ],
        "evidence": qa_facts,
        "provenance": MODEL,
    }
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "receipt": OUT.relative_to(ROOT).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
