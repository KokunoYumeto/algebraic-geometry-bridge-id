#!/usr/bin/env python3
"""Fail-closed cumulative reader QA through the frozen Unit 24 milestone."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "reader-id"
HTML = BUILD / "index.html"
PDF = BUILD / "algebraic-geometry-bridge-id-units-01-24.pdf"
RECEIPT = BUILD / "BUILD_RECEIPT.json"
OUT = ROOT / "qa" / "UNITS_01_24_MACHINE_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra."
BASELINE_FACTS = {
    "qa/UNITS_01_21_MACHINE_QA.json": (7308, "adace78a568ecb84c97077965d82a4ca13a849b7455db0b8872546486dcabdd0"),
    "qa/UNIT_21_PROTECTED_SURFACES.json": (1977, "35eee319508f364c73f32627ffb69b376bd15bb978e4d1694765dc06538eb6ba"),
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
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular file: {path}")
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }


def check_fact(relative: str, expected: tuple[int, str]) -> dict[str, Any]:
    actual = fact(ROOT / relative)
    require((actual["bytes"], actual["sha256"]) == expected, f"identity drift for {relative}")
    return actual


def checked_receipt_path(relative: str) -> Path:
    require(not Path(relative).is_absolute() and ".." not in Path(relative).parts, f"unsafe receipt path: {relative}")
    candidate = (ROOT / relative).resolve()
    require(candidate.is_relative_to(ROOT.resolve()), f"receipt path escapes task root: {relative}")
    return candidate


def find_evidence(payload: dict[str, Any], relative: str) -> tuple[int, str]:
    stack: list[Any] = [payload]
    matches: list[tuple[int, str]] = []
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            if item.get("path") == relative and isinstance(item.get("bytes"), int) and isinstance(item.get("sha256"), str):
                matches.append((item["bytes"], item["sha256"]))
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
    require(matches and len(set(matches)) == 1, f"missing/ambiguous per-unit evidence: {relative}")
    return matches[0]


def pdf_pages(parts: list[str], marker: str) -> list[int]:
    # PDF text extraction may insert whitespace inside a rendered word (for
    # example, ``Formal`` can emerge as ``F ormal`` around a font boundary).
    # Remove whitespace only; preserve every letter, digit, and punctuation
    # mark so the boundary marker remains exact in content and order.
    compact_marker = re.sub(r"\s+", "", marker)
    matches = [
        index
        for index, text in enumerate(parts, start=1)
        if compact_marker in re.sub(r"\s+", "", text)
    ]
    require(matches, f"PDF marker absent: {marker}")
    return matches


def first_heading(raw: str) -> str:
    match = re.search(r"^#\s+(.+?)(?:\s+\{#[^}]+\})?\s*$", raw, flags=re.M)
    require(match is not None, "source first heading absent")
    return match.group(1).strip()


def last_heading(raw: str, prefix: str, unit: int) -> str:
    matches = re.findall(rf"^#+\s+({re.escape(prefix)}\s+{unit}\.\d+)\b.*$", raw, flags=re.M)
    require(matches, f"source {prefix} marker absent for Unit {unit}")
    return matches[-1]


def main() -> int:
    baseline_facts = [check_fact(relative, expected) for relative, expected in BASELINE_FACTS.items()]
    baseline = json.loads((ROOT / "qa" / "UNITS_01_21_MACHINE_QA.json").read_text(encoding="utf-8"))
    protected_baseline = json.loads((ROOT / "qa" / "UNIT_21_PROTECTED_SURFACES.json").read_text(encoding="utf-8"))
    require(baseline.get("status") == "PASS" and baseline.get("through_unit") == 21 and baseline.get("language") == "id-ID", "Unit 21 machine baseline status/scope")
    require(protected_baseline.get("status") == "PASS" and protected_baseline.get("through_unit") == 21, "Unit 21 protected baseline status/scope")

    build = json.loads(RECEIPT.read_text(encoding="utf-8"))
    require(build.get("schema") == "ag-bridge-build-receipt-v2", "build receipt schema")
    require(build.get("through_unit") == 24 and build.get("language") == "id-ID", "build scope/language")
    require(build.get("title") == "Kurva Aljabar - Unit 1-24", "build title")
    input_rows = {row["path"]: row for row in build.get("inputs", [])}
    output_rows = {row["path"]: row for row in build.get("outputs", [])}
    require(len(input_rows) == len(build.get("inputs", [])), "duplicate build input path")
    require(len(output_rows) == len(build.get("outputs", [])), "duplicate build output path")
    expected_outputs = {
        "build/reader-id/index.html",
        "build/reader-id/algebraic-geometry-bridge-id-units-01-24.pdf",
    }
    require(set(output_rows) == expected_outputs, "build output set")
    for relative in expected_outputs:
        path = checked_receipt_path(relative)
        row = output_rows[relative]
        require(path.is_file() and not path.is_symlink(), f"missing/nonregular reader output: {relative}")
        require((path.stat().st_size, digest(path)) == (row["bytes"], row["sha256"]), f"reader output/receipt drift: {relative}")
    for row in build.get("inputs", []):
        path = checked_receipt_path(row["path"])
        require(path.is_file() and not path.is_symlink(), f"receipt input missing/nonregular: {row['path']}")
        require((path.stat().st_size, digest(path)) == (row["bytes"], row["sha256"]), f"receipt input drift: {row['path']}")
    for log_name in ("pandoc-html.log", "pandoc-pdf.log"):
        log = BUILD / log_name
        require(log.is_file() and log.stat().st_size == 0, f"Pandoc warning log is nonempty/missing: {log_name}")

    source_rows = [row for row in build["inputs"] if row["path"].startswith("source/id-ID/") and row["path"].endswith(".md")]
    source_paths = [checked_receipt_path(row["path"]) for row in source_rows]
    source_raw = "\n".join(path.read_text(encoding="utf-8") for path in source_paths)
    lecture_units = {int(match.group(1)) for row in source_rows if (match := re.fullmatch(r"source/id-ID/lecture-(\d{2})\.md", row["path"]))}
    worksheet_units = {int(match.group(1)) for row in source_rows if (match := re.fullmatch(r"source/id-ID/worksheet-(\d{2})\.md", row["path"]))}
    solution_units = {int(match.group(1)) for row in source_rows if (match := re.fullmatch(r"source/id-ID/worksheet-(\d{2})-solutions\.md", row["path"]))}
    require(lecture_units == worksheet_units == solution_units == set(range(1, 25)), "contiguous source unit closure")
    require("source/id-ID/frontmatter-units-01-24.md" in input_rows, "Unit 24 frontmatter build input")
    require(MODEL in (ROOT / "source" / "id-ID" / "frontmatter-units-01-24.md").read_text(encoding="utf-8"), "exact model provenance in frontmatter")

    unit_qas: dict[int, dict[str, Any]] = {}
    authority_summary: dict[str, Any] = {}
    new_id_count = 0
    exercise_increment = 0
    solution_increment = 0
    media_increment = 0
    html_markers: list[str] = []
    pdf_boundaries: dict[int, tuple[str, str, str | None, str]] = {}
    evidence: list[dict[str, Any]] = []
    for unit in range(22, 25):
        qa_path = ROOT / "qa" / f"UNIT_{unit}_TRANSLATION_QA.json"
        qa_payload = json.loads(qa_path.read_text(encoding="utf-8"))
        require(qa_payload.get("status") == "PASS" and qa_payload.get("unit") == unit, f"Unit {unit} QA status/scope")
        require(qa_payload.get("provenance") == MODEL, f"Unit {unit} QA provenance")
        unit_qas[unit] = qa_payload
        evidence.append(fact(qa_path))

        core_names = [
            f"source/id-ID/lecture-{unit:02d}.md",
            f"source/id-ID/worksheet-{unit:02d}.md",
            f"source/id-ID/worksheet-{unit:02d}-solutions.md",
            f"source/id-ID/media-credits-unit-{unit:02d}.md",
        ]
        require(all(name in input_rows for name in core_names), f"Unit {unit} source build-input closure")
        for relative in core_names:
            expected = find_evidence(qa_payload, relative)
            path = ROOT / relative
            require((path.stat().st_size, digest(path)) == expected, f"Unit {unit} source/per-unit-QA drift: {relative}")
            require((input_rows[relative]["bytes"], input_rows[relative]["sha256"]) == expected, f"Unit {unit} source/build-receipt drift: {relative}")

        authority_paths = {
            "manifest": f"authority/wikiversity/unit-{unit}/UNIT_AUTHORITY_MANIFEST.json",
            "map": f"authority/wikiversity/unit-{unit}/ORDERED_EXERCISE_MAP.json",
            "rights": f"authority/RIGHTS-unit-{unit}.csv",
            "closure": f"authority/ASSET_CLOSURE-unit-{unit}.json",
        }
        authority_facts: dict[str, tuple[int, str]] = {}
        for key, relative in authority_paths.items():
            expected = find_evidence(qa_payload, relative)
            path = ROOT / relative
            require((path.stat().st_size, digest(path)) == expected, f"Unit {unit} authority/per-unit-QA drift: {relative}")
            authority_facts[key] = expected
        manifest = json.loads((ROOT / authority_paths["manifest"]).read_text(encoding="utf-8"))
        mapping = json.loads((ROOT / authority_paths["map"]).read_text(encoding="utf-8"))
        closure = json.loads((ROOT / authority_paths["closure"]).read_text(encoding="utf-8"))
        require(manifest.get("unit_number") == unit, f"manifest unit {unit}")
        require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, f"lecture closure Unit {unit}")
        require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, f"worksheet closure Unit {unit}")
        require(mapping.get("unit") == unit and isinstance(mapping.get("exercise_count"), int), f"exercise map Unit {unit}")
        solutions = [row["exercise_number"] for row in mapping["entries"] if row.get("has_public_solution")]
        exercises = mapping["exercise_count"]
        media = closure.get("reader_media_positions")
        require(isinstance(media, int) and media >= 0, f"media closure Unit {unit}")
        translation = qa_payload["translation"]
        require(translation.get("exercises") == exercises, f"Unit {unit} translated exercise count")
        require(translation.get("public_solutions") == len(solutions), f"Unit {unit} translated solution count")
        require(translation.get("reader_images") == media, f"Unit {unit} translated media count")

        core_raw = "\n".join((ROOT / name).read_text(encoding="utf-8") for name in core_names[:3])
        core_ids = re.findall(r"\{#([A-Za-z][A-Za-z0-9_.:-]*)\}", core_raw)
        credit_ids = re.findall(r"\{#([A-Za-z][A-Za-z0-9_.:-]*)\}", (ROOT / core_names[3]).read_text(encoding="utf-8"))
        edition_slug = "2012" if unit == 24 else "2025-2026"
        required_roots = {
            f"br-ak-{edition_slug}-l{unit:02d}",
            f"br-ak-{edition_slug}-w{unit:02d}",
            f"br-ak-{edition_slug}-w{unit:02d}-solutions",
        }
        require(required_roots <= set(core_ids), f"Unit {unit} source-edition stable-root transition")
        wrong_slug = "2025-2026" if unit == 24 else "2012"
        require(not any(identifier.startswith(f"br-ak-{wrong_slug}-") for identifier in core_ids), f"Unit {unit} wrong source-edition stable-ID namespace")
        require(
            len(core_ids) + len(credit_ids) == translation.get("stable_ids"),
            f"Unit {unit} source/control stable-ID count",
        )
        require(len(re.findall(rf"^### Soal {unit}\.\d+", core_raw, flags=re.M)) == exercises, f"Unit {unit} source exercise topology")
        require(len(re.findall(rf"^## Solusi Soal {unit}\.\d+", core_raw, flags=re.M)) == len(solutions), f"Unit {unit} source solution topology")
        new_id_count += len(core_ids) + len(credit_ids)
        exercise_increment += exercises
        solution_increment += len(solutions)
        media_increment += media

        lecture_raw = (ROOT / core_names[0]).read_text(encoding="utf-8")
        worksheet_raw = (ROOT / core_names[1]).read_text(encoding="utf-8")
        solutions_raw = (ROOT / core_names[2]).read_text(encoding="utf-8")
        credit_raw = (ROOT / core_names[3]).read_text(encoding="utf-8")
        lecture_marker = first_heading(lecture_raw)
        exercise_marker = last_heading(worksheet_raw, "Soal", unit)
        solution_marker = last_heading(solutions_raw, "Solusi Soal", unit) if solutions else None
        credit_marker = first_heading(credit_raw)
        html_markers.extend(marker for marker in (lecture_marker, exercise_marker, solution_marker, credit_marker) if marker)
        pdf_boundaries[unit] = (lecture_marker, exercise_marker, solution_marker, credit_marker)
        authority_summary[str(unit)] = {
            "exercises": exercises,
            "solutions": solutions,
            "media_positions": media,
            "manifest_sha256": authority_facts["manifest"][1],
            "translation_qa_sha256": digest(qa_path),
        }

    stable_ids = re.findall(r"\{#([A-Za-z][A-Za-z0-9_.:-]*)\}", source_raw)
    require(len(stable_ids) == len(set(stable_ids)), f"stable source ID uniqueness: {len(stable_ids)}")
    exercise_count = len(re.findall(r"^### Soal \d+\.\d+", source_raw, flags=re.M))
    solution_count = len(re.findall(r"^## Solusi Soal \d+\.\d+", source_raw, flags=re.M))
    baseline_coverage = baseline["coverage"]
    require(len(stable_ids) == baseline_coverage["stable_source_ids"] + new_id_count, "measured cumulative stable-ID closure")
    require(exercise_count == baseline_coverage["exercises"] + exercise_increment, "measured cumulative exercise closure")
    require(solution_count == baseline_coverage["public_source_solutions"] + solution_increment, "measured cumulative solution closure")
    expected_media = baseline_coverage["reader_media_positions"] + media_increment
    require(MODEL in source_raw, "exact model provenance")
    require(all(token not in source_raw.casefold() for token in ("todo", "fixme", "tbd", "placeholder")), "source placeholder residue")
    require(not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|access[_-]?token|bearer\s+[A-Za-z0-9._-]{20,}", source_raw, flags=re.I), "secret-like source content")

    html_raw = HTML.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_raw, "html.parser")
    require(soup.html is not None and soup.html.get("lang") == "id-ID", "HTML language")
    require(soup.title is not None and soup.title.get_text(strip=True) == "Kurva Aljabar - Unit 1-24", "HTML title")
    html_ids = [tag["id"] for tag in soup.find_all(id=True)]
    require(len(html_ids) == len(set(html_ids)), "HTML ID uniqueness")
    html_id_set = set(html_ids)
    require(not [identifier for identifier in stable_ids if identifier not in html_id_set], "source IDs absent from HTML")
    images = soup.find_all("img")
    require(len(images) == expected_media, f"HTML media/source closure: {len(images)} != {expected_media}")
    require(all(image.get("alt", "").strip() for image in images), "empty HTML image alt")
    require(all(not str(image.get("src", "")).startswith(("http://", "https://")) for image in images), "remote HTML image")
    internal = [anchor.get("href", "")[1:] for anchor in soup.find_all("a", href=True) if anchor.get("href", "").startswith("#")]
    require(not [target for target in internal if target not in html_id_set], "broken internal anchor")
    mathml_nodes = len(soup.find_all("math"))
    tex_annotations = [tag for tag in soup.find_all("annotation") if tag.get("encoding") == "application/x-tex"]
    require(mathml_nodes > baseline_coverage["mathml_nodes"], "cumulative MathML did not advance")
    require(len(tex_annotations) == mathml_nodes, "MathML/TeX annotation closure")
    require("１３２人目" in html_raw, "accepted Japanese creator account absent from cumulative HTML")
    html_text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
    for marker in html_markers:
        require(marker in html_text, f"HTML marker absent: {marker}")
    require("pending_component_audit" not in html_raw and "<!-- QA:" not in html_raw, "HTML unresolved marker")

    reader = PdfReader(PDF, strict=True)
    require(not reader.is_encrypted, "PDF encrypted")
    require(reader.metadata is not None and reader.metadata.title == "Kurva Aljabar - Unit 1-24", "PDF title metadata")
    require(len(reader.pages) > baseline["pdf"]["pages"], "cumulative PDF did not advance")
    pdf_text_parts: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        box = page.mediabox
        require(abs(float(box.width) - 595.276) < 1 and abs(float(box.height) - 841.89) < 1, f"non-A4 page {index}")
        pdf_text_parts.append(page.extract_text() or "")
    marker_pages: dict[str, int] = {}
    main_sequence: list[int] = []
    credit_sequence: list[int] = []
    for unit in range(22, 25):
        lecture_marker, exercise_marker, solution_marker, credit_marker = pdf_boundaries[unit]
        exercise_page = max(pdf_pages(pdf_text_parts, exercise_marker))
        lecture_candidates = [page for page in pdf_pages(pdf_text_parts, lecture_marker) if page <= exercise_page]
        require(lecture_candidates, f"PDF lecture boundary cannot be disambiguated: Unit {unit}")
        lecture_page = max(lecture_candidates)
        unit_sequence = [lecture_page, exercise_page]
        if solution_marker:
            solution_page = max(pdf_pages(pdf_text_parts, solution_marker))
            require(exercise_page <= solution_page, f"PDF solution precedes worksheet: Unit {unit}")
            marker_pages[solution_marker] = solution_page
            unit_sequence.append(solution_page)
        credit_page = max(pdf_pages(pdf_text_parts, credit_marker))
        marker_pages.update({lecture_marker: lecture_page, exercise_marker: exercise_page, credit_marker: credit_page})
        main_sequence.extend(unit_sequence)
        credit_sequence.append(credit_page)
    require(main_sequence == sorted(main_sequence), "PDF terminal main-content order")
    require(credit_sequence == sorted(credit_sequence) and min(credit_sequence) >= main_sequence[-1], "PDF consolidated media-credit order")
    terminal_start = marker_pages[pdf_boundaries[22][0]]
    terminal_text = "\n".join(pdf_text_parts[terminal_start - 1 :])
    require("pending_component_audit" not in terminal_text, "PDF unresolved marker")

    result = {
        "schema": "ag-bridge-cumulative-reader-qa-v4",
        "status": "PASS",
        "verified_date": "2026-08-25",
        "through_unit": 24,
        "language": "id-ID",
        "coverage": {
            "lectures": len(lecture_units),
            "worksheets": len(worksheet_units),
            "exercises": exercise_count,
            "public_source_solutions": solution_count,
            "reader_media_positions": expected_media,
            "stable_source_ids": len(stable_ids),
            "mathml_nodes": mathml_nodes,
        },
        "html": {
            "path": HTML.relative_to(ROOT).as_posix(), "bytes": HTML.stat().st_size, "sha256": digest(HTML),
            "ids": len(html_ids), "images": len(images), "mathml_nodes": mathml_nodes,
            "tex_annotations": len(tex_annotations), "internal_links": len(internal),
            "broken_internal_links": 0, "remote_images": 0, "empty_alt": 0,
        },
        "pdf": {
            "path": PDF.relative_to(ROOT).as_posix(), "bytes": PDF.stat().st_size, "sha256": digest(PDF),
            "pages": len(reader.pages), "paper": "A4", "encrypted": False,
            "terminal_start_page": terminal_start,
            "terminal_pages_checked": len(reader.pages) - terminal_start + 1,
            "terminal_marker_pages": marker_pages,
        },
        "build_receipt": {
            "path": RECEIPT.relative_to(ROOT).as_posix(), "bytes": RECEIPT.stat().st_size, "sha256": digest(RECEIPT),
            "input_count": len(build["inputs"]), "source_markdown_input_count": len(source_rows), "output_count": len(build["outputs"]),
            "html_log_bytes": 0, "pdf_log_bytes": 0,
        },
        "authority_units_22_24": authority_summary,
        "baseline_and_checkpoint_facts": baseline_facts + evidence,
        "checks": [
            "exact Units 1-21 machine/protected baselines bound",
            "Units 22-24 authority and translation QA identities replayed dynamically from PASS receipts",
            f"all {len(build['inputs'])} build-receipt inputs replayed from recorded bytes and hashes",
            "cumulative IDs, exercises, solutions, and media measured from bound source/authority inputs",
            "HTML IDs, MathML/TeX annotations, media alts, anchors, and local resources closed",
            "PDF metadata, A4 geometry, measured terminal boundary, and ordered markers closed",
            "Pandoc warning logs empty; no placeholder or secret-like source content",
        ],
        "provenance": MODEL,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "receipt": OUT.relative_to(ROOT).as_posix(), "bytes": OUT.stat().st_size, "sha256": digest(OUT), "pages": len(reader.pages), "mathml": mathml_nodes, "stable_ids": len(stable_ids)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
