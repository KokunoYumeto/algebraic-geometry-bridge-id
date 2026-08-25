#!/usr/bin/env python3
"""Fail-closed cumulative reader QA through the frozen Unit 21 milestone."""

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
QA = ROOT / "qa"
HTML = BUILD / "index.html"
PDF = BUILD / "algebraic-geometry-bridge-id-units-01-21.pdf"
RECEIPT = BUILD / "BUILD_RECEIPT.json"
OUT = QA / "UNITS_01_21_MACHINE_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra."

BASELINE_FACTS = {
    "qa/UNITS_01_18_MACHINE_QA.json": (9029, "fdd7a3b70d74bb8454440c28eb6a8840e8da448bcd57a7a86cefbb8f29b43f00"),
    "qa/UNIT_18_PROTECTED_SURFACES.json": (1566, "29a6a329361515dadc7c6399538a010a3717c43e38fb9564ac681b8670786bc9"),
}
UNIT_QA_FACTS = {
    19: ("qa/UNIT_19_INTEGRATION_QA.json", 5865, "fe546d8499bc63dedb08c3548eb42322924338ea5e183af7ff9fc66f48a6601a"),
    20: ("qa/UNIT_20_TRANSLATION_QA.json", 3748, "6c4bc4eb66feccf91d0d53f81c08726857a6edb3dbee93b66b0487b83a4b2725"),
    21: ("qa/UNIT_21_TRANSLATION_QA.json", 5436, "a999af2ab40124cbe8bb593239ce17b9e99515d70253ac1869f2934426a7ff75"),
}
BUILD_FACTS = {
    "build/reader-id/BUILD_RECEIPT.json": (31430, "71b4e362d354c3c9ff827c60b791a00ccc8544b8039aebc3a6eb753261dc32e1"),
    "build/reader-id/index.html": (12388419, "ae658bee5191e4d0be529d38ec7eb9fd2e287295237be4bbb98a58b4709c6700"),
    "build/reader-id/algebraic-geometry-bridge-id-units-01-21.pdf": (7409373, "b95fd1ed0ea75294cd4562b7f2f36e920e247e2da5e1b039e99e975f9797a3e6"),
    "build/reader-id/pandoc-html.log": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "build/reader-id/pandoc-pdf.log": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
}
UNIT_SPEC = {
    19: {
        "manifest": (83621, "52245060a54f973b4fba19878eec234904430b9e5058defdbd9feaa7a868080e"),
        "map": (6379, "f75bcc8e564cef327687b486bb074fa8c799b065994f4a1d79e7abf2b78b30dd"),
        "rights": (2066, "1feb699d361be0379de5c785cc6c073adf3d47d31c8b07df3db1d3fc6ed7bdb1"),
        "closure": (4042, "4ee0c05610b30f25038484a4dc147bdcddda9ebb29cfbded53d4e72a5b32be4e"),
        "exercises": 15,
        "solutions": [4, 12],
        "media": 1,
    },
    20: {
        "manifest": (129387, "b063e5edc556cd18598389083ea27ea7f255edfe2ae00e13ebf24de76e5b37d7"),
        "map": (13502, "c74da7b0627cf8c8c694c0a9f20e94b0c7dc00ecd6c95b72ad21ae4a6c5c07ea"),
        "rights": (2024, "09b85688b10784cf2c7e7aec9d017eb4d0403faf0b96ef8561b789168d19f565"),
        "closure": (4809, "5ab57774999d4f293533a8fb14ad4e50d6caa1fba3d2664428c32d15f935c185"),
        "exercises": 23,
        "solutions": [1, 3, 4, 5, 12, 13, 14, 17],
        "media": 1,
    },
    21: {
        "manifest": (142834, "d85444ddfc66c8e77d52db3f3abc0a186e5dd598789edaaf890b3c09cf00f923"),
        "map": (9992, "9329621bbdd62df63f01d7298dc2a4a65a296211db131f8d8730b7d308fd5f47"),
        "rights": (443, "6b8de6f5a63f32d9f22e7fb69c98ba2d787121a2437a392602571504c2a1c544"),
        "closure": (5705, "8708a399d7c950101609281c14fe4e48eb02aa70335a7ad6cf7ef4194e9bc483"),
        "exercises": 26,
        "solutions": [3, 8],
        "media": 0,
    },
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


def check_fact(relative: str, fact: tuple[int, str]) -> dict[str, Any]:
    path = ROOT / relative
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular file: {relative}")
    actual = (path.stat().st_size, digest(path))
    require(actual == fact, f"identity drift for {relative}: {actual} != {fact}")
    return {"path": relative, "bytes": actual[0], "sha256": actual[1]}


def checked_receipt_path(relative: str) -> Path:
    candidate = (ROOT / relative).resolve()
    require(candidate.is_relative_to(ROOT.resolve()), f"receipt path escapes task root: {relative}")
    require(".." not in Path(relative).parts and not Path(relative).is_absolute(), f"unsafe receipt path: {relative}")
    return candidate


def pdf_pages(parts: list[str], marker: str) -> list[int]:
    matches = [index for index, text in enumerate(parts, start=1) if marker in text]
    require(matches, f"PDF marker absent: {marker}")
    return matches


def main() -> int:
    facts: list[dict[str, Any]] = []
    baseline_payloads: dict[str, Any] = {}
    for relative, fact in BASELINE_FACTS.items():
        facts.append(check_fact(relative, fact))
        payload = json.loads((ROOT / relative).read_text(encoding="utf-8"))
        require(payload.get("status") == "PASS" and payload.get("through_unit") == 18, f"baseline status/scope: {relative}")
        baseline_payloads[relative] = payload
    baseline = baseline_payloads["qa/UNITS_01_18_MACHINE_QA.json"]
    require(baseline["language"] == "id-ID", "baseline language")

    unit_qas: dict[int, Any] = {}
    for unit, (relative, byte_count, sha256) in UNIT_QA_FACTS.items():
        facts.append(check_fact(relative, (byte_count, sha256)))
        payload = json.loads((ROOT / relative).read_text(encoding="utf-8"))
        require(payload.get("status") == "PASS" and payload.get("unit") == unit, f"Unit {unit} QA status/scope")
        require(payload.get("provenance") == MODEL, f"Unit {unit} QA provenance")
        unit_qas[unit] = payload

    for relative, fact in BUILD_FACTS.items():
        facts.append(check_fact(relative, fact))

    authority_summary: dict[str, Any] = {}
    for unit, spec in UNIT_SPEC.items():
        paths = {
            "manifest": f"authority/wikiversity/unit-{unit}/UNIT_AUTHORITY_MANIFEST.json",
            "map": f"authority/wikiversity/unit-{unit}/ORDERED_EXERCISE_MAP.json",
            "rights": f"authority/RIGHTS-unit-{unit}.csv",
            "closure": f"authority/ASSET_CLOSURE-unit-{unit}.json",
        }
        for key, relative in paths.items():
            facts.append(check_fact(relative, spec[key]))
        manifest = json.loads((ROOT / paths["manifest"]).read_text(encoding="utf-8"))
        mapping = json.loads((ROOT / paths["map"]).read_text(encoding="utf-8"))
        closure = json.loads((ROOT / paths["closure"]).read_text(encoding="utf-8"))
        qa_payload = unit_qas[unit]
        qa_authority_hash = qa_payload["authority"].get("manifest_sha256")
        if qa_authority_hash is None:
            qa_authority_hash = qa_payload["authority"]["manifest"]["sha256"]
        require(qa_authority_hash == spec["manifest"][1], f"Unit {unit} QA/manifest binding")
        require(manifest["unit_number"] == unit, f"manifest unit {unit}")
        require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, f"lecture closure unit {unit}")
        require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, f"worksheet closure unit {unit}")
        require(mapping["unit"] == unit and mapping["exercise_count"] == spec["exercises"], f"exercise count unit {unit}")
        solutions = [row["exercise_number"] for row in mapping["entries"] if row["has_public_solution"]]
        require(solutions == spec["solutions"], f"solution topology unit {unit}")
        require(closure["unit"] == unit and closure["reader_media_positions"] == spec["media"], f"media positions unit {unit}")
        require(qa_payload["translation"]["exercises"] == spec["exercises"], f"Unit {unit} translation exercise count")
        require(qa_payload["translation"]["public_solutions"] == len(spec["solutions"]), f"Unit {unit} translation solution count")
        authority_summary[str(unit)] = {
            "exercises": spec["exercises"],
            "solutions": solutions,
            "media_positions": spec["media"],
            "manifest_sha256": spec["manifest"][1],
            "translation_qa_sha256": UNIT_QA_FACTS[unit][2],
        }

    build_receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    require(build_receipt["schema"] == "ag-bridge-build-receipt-v2", "build receipt schema")
    require(build_receipt["through_unit"] == 21 and build_receipt["language"] == "id-ID", "build scope/language")
    require(build_receipt["title"] == "Kurva Aljabar - Unit 1-21", "build title")
    input_rows = {row["path"]: row for row in build_receipt["inputs"]}
    output_rows = {row["path"]: row for row in build_receipt["outputs"]}
    require(len(input_rows) == len(build_receipt["inputs"]), "duplicate build input path")
    require(len(output_rows) == len(build_receipt["outputs"]), "duplicate build output path")
    expected_outputs = {
        "build/reader-id/index.html",
        "build/reader-id/algebraic-geometry-bridge-id-units-01-21.pdf",
    }
    require(set(output_rows) == expected_outputs, "build output set")
    for relative in expected_outputs:
        fact = BUILD_FACTS[relative]
        require((output_rows[relative]["bytes"], output_rows[relative]["sha256"]) == fact, f"receipt output identity: {relative}")
    for row in build_receipt["inputs"]:
        path = checked_receipt_path(row["path"])
        require(path.is_file() and not path.is_symlink(), f"receipt input missing/nonregular: {row['path']}")
        require(path.stat().st_size == row["bytes"] and digest(path) == row["sha256"], f"receipt input drift: {row['path']}")

    source_rows = [row for row in build_receipt["inputs"] if row["path"].startswith("source/id-ID/") and row["path"].endswith(".md")]
    source_paths = [checked_receipt_path(row["path"]) for row in source_rows]
    source_raw = "\n".join(path.read_text(encoding="utf-8") for path in source_paths)
    lecture_units = {int(match.group(1)) for row in source_rows if (match := re.fullmatch(r"source/id-ID/lecture-(\d{2})\.md", row["path"]))}
    worksheet_units = {int(match.group(1)) for row in source_rows if (match := re.fullmatch(r"source/id-ID/worksheet-(\d{2})\.md", row["path"]))}
    solution_units = {int(match.group(1)) for row in source_rows if (match := re.fullmatch(r"source/id-ID/worksheet-(\d{2})-solutions\.md", row["path"]))}
    require(lecture_units == worksheet_units == solution_units == set(range(1, 22)), "contiguous source unit closure")

    stable_ids = re.findall(r"\{#([A-Za-z][A-Za-z0-9_.:-]*)\}", source_raw)
    require(len(stable_ids) == len(set(stable_ids)), f"stable source ID uniqueness: {len(stable_ids)}")
    exercise_count = len(re.findall(r"^### Soal \d+\.\d+", source_raw, flags=re.M))
    solution_count = len(re.findall(r"^## Solusi Soal \d+\.\d+", source_raw, flags=re.M))

    new_id_count = 0
    for unit in range(19, 22):
        core_names = [f"source/id-ID/lecture-{unit:02d}.md", f"source/id-ID/worksheet-{unit:02d}.md", f"source/id-ID/worksheet-{unit:02d}-solutions.md"]
        require(all(name in input_rows for name in core_names), f"Unit {unit} core build inputs")
        core_raw = "\n".join((ROOT / name).read_text(encoding="utf-8") for name in core_names)
        core_ids = re.findall(r"\{#([A-Za-z][A-Za-z0-9_.:-]*)\}", core_raw)
        require(len(core_ids) == unit_qas[unit]["translation"]["stable_ids"], f"Unit {unit} core stable IDs")
        require(len(re.findall(r"^### Soal \d+\.\d+", core_raw, flags=re.M)) == UNIT_SPEC[unit]["exercises"], f"Unit {unit} source exercise topology")
        require(len(re.findall(r"^## Solusi Soal \d+\.\d+", core_raw, flags=re.M)) == len(UNIT_SPEC[unit]["solutions"]), f"Unit {unit} source solution topology")
        credit_name = f"source/id-ID/media-credits-unit-{unit:02d}.md"
        require(credit_name in input_rows, f"Unit {unit} media-credit build input")
        credit_ids = re.findall(r"\{#([A-Za-z][A-Za-z0-9_.:-]*)\}", (ROOT / credit_name).read_text(encoding="utf-8"))
        new_id_count += len(core_ids) + len(credit_ids)
    baseline_coverage = baseline["coverage"]
    require(len(stable_ids) == baseline_coverage["stable_source_ids"] + new_id_count, "measured cumulative stable-ID closure")
    require(exercise_count == baseline_coverage["exercises"] + sum(UNIT_SPEC[unit]["exercises"] for unit in UNIT_SPEC), "measured cumulative exercise closure")
    require(solution_count == baseline_coverage["public_source_solutions"] + sum(len(UNIT_SPEC[unit]["solutions"]) for unit in UNIT_SPEC), "measured cumulative solution closure")
    expected_media = baseline_coverage["reader_media_positions"] + sum(UNIT_SPEC[unit]["media"] for unit in UNIT_SPEC)
    require(MODEL in source_raw, "exact model provenance")
    require(all(token not in source_raw.casefold() for token in ("todo", "fixme", "tbd", "placeholder")), "source placeholder residue")
    require(not re.search(r"gh[pousr]_[A-Za-z0-9]{20,}|access[_-]?token|bearer\s+[A-Za-z0-9._-]{20,}", source_raw, flags=re.I), "secret-like source content")

    html_raw = HTML.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_raw, "html.parser")
    require(soup.html is not None and soup.html.get("lang") == "id-ID", "HTML language")
    require(soup.title is not None and soup.title.get_text(strip=True) == "Kurva Aljabar - Unit 1-21", "HTML title")
    html_ids = [tag["id"] for tag in soup.find_all(id=True)]
    require(len(html_ids) == len(set(html_ids)), "HTML ID uniqueness")
    html_id_set = set(html_ids)
    missing_ids = [identifier for identifier in stable_ids if identifier not in html_id_set]
    require(not missing_ids, f"source IDs absent from HTML: {missing_ids[:5]}")
    images = soup.find_all("img")
    require(len(images) == expected_media, f"HTML media/source closure: {len(images)} != {expected_media}")
    require(all(image.get("alt", "").strip() for image in images), "empty HTML image alt")
    require(all(not str(image.get("src", "")).startswith(("http://", "https://")) for image in images), "remote HTML image")
    internal = [anchor.get("href", "")[1:] for anchor in soup.find_all("a", href=True) if anchor.get("href", "").startswith("#")]
    broken = [target for target in internal if target not in html_id_set]
    require(not broken, f"broken internal anchors: {broken[:5]}")
    mathml_nodes = len(soup.find_all("math"))
    tex_annotations = [tag for tag in soup.find_all("annotation") if tag.get("encoding") == "application/x-tex"]
    require(mathml_nodes > baseline_coverage["mathml_nodes"], "cumulative MathML did not advance")
    require(len(tex_annotations) == mathml_nodes, "MathML/TeX annotation closure")
    require("１３２人目" in html_raw, "exact Japanese creator account absent from HTML")
    html_text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
    html_markers = (
        "Kuliah 19: Penyajian sebagai Gelanggang Faktor dan Keintegralan",
        "Soal 19.15",
        "Solusi Soal 19.12",
        "Kredit media Unit 19",
        "Kuliah 20: Gelanggang Normal dan Normalisasi",
        "Soal 20.23",
        "Solusi Soal 20.17",
        "Kredit media Unit 20",
        "Kuliah 21: Gelanggang Valuasi Diskret dan Lema Nakayama",
        "Soal 21.26",
        "Solusi Soal 21.8",
        "Kredit media Unit 21",
    )
    for marker in html_markers:
        require(marker in html_text, f"HTML marker absent: {marker}")
    require("pending_component_audit" not in html_raw and "<!-- QA:" not in html_raw, "HTML unresolved marker")

    reader = PdfReader(PDF, strict=True)
    require(not reader.is_encrypted, "PDF encrypted")
    require(reader.metadata is not None and reader.metadata.title == "Kurva Aljabar - Unit 1-21", "PDF title metadata")
    require(len(reader.pages) > baseline["pdf"]["pages"], "cumulative PDF did not advance")
    pdf_text_parts: list[str] = []
    for index, page in enumerate(reader.pages, start=1):
        box = page.mediabox
        require(abs(float(box.width) - 595.276) < 1 and abs(float(box.height) - 841.89) < 1, f"non-A4 page {index}")
        pdf_text_parts.append(page.extract_text() or "")
    pdf_boundaries = {
        19: ("Kuliah 19", "Soal 19.15", "Solusi Soal 19.12", "Kredit media Unit 19"),
        20: ("Kuliah 20", "Soal 20.23", "Solusi Soal 20.17", "Kredit media Unit 20"),
        21: ("Kuliah 21", "Soal 21.26", "Solusi Soal 21.8", "Kredit media Unit 21"),
    }
    marker_pages: dict[str, int] = {}
    main_sequence: list[int] = []
    credit_sequence: list[int] = []
    for unit in range(19, 22):
        lecture_marker, exercise_marker, solution_marker, credit_marker = pdf_boundaries[unit]
        exercise_page = max(pdf_pages(pdf_text_parts, exercise_marker))
        solution_page = max(pdf_pages(pdf_text_parts, solution_marker))
        lecture_candidates = [page for page in pdf_pages(pdf_text_parts, lecture_marker) if page <= exercise_page]
        require(lecture_candidates, f"PDF lecture boundary cannot be disambiguated: Unit {unit}")
        lecture_page = max(lecture_candidates)
        credit_page = max(pdf_pages(pdf_text_parts, credit_marker))
        marker_pages.update({lecture_marker: lecture_page, exercise_marker: exercise_page, solution_marker: solution_page, credit_marker: credit_page})
        main_sequence.extend((lecture_page, exercise_page, solution_page))
        credit_sequence.append(credit_page)
    require(main_sequence == sorted(main_sequence), "PDF terminal main-content order")
    require(credit_sequence == sorted(credit_sequence) and min(credit_sequence) >= main_sequence[-1], "PDF consolidated media-credit order")
    terminal_start = marker_pages["Kuliah 19"]
    terminal_text = "\n".join(pdf_text_parts[terminal_start - 1 :])
    require("pending_component_audit" not in terminal_text, "PDF unresolved marker")

    result = {
        "schema": "ag-bridge-cumulative-reader-qa-v4",
        "status": "PASS",
        "verified_date": "2026-08-25",
        "through_unit": 21,
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
            "path": "build/reader-id/index.html",
            "bytes": HTML.stat().st_size,
            "sha256": digest(HTML),
            "ids": len(html_ids),
            "images": len(images),
            "mathml_nodes": mathml_nodes,
            "tex_annotations": len(tex_annotations),
            "internal_links": len(internal),
            "broken_internal_links": 0,
            "remote_images": 0,
            "empty_alt": 0,
        },
        "pdf": {
            "path": "build/reader-id/algebraic-geometry-bridge-id-units-01-21.pdf",
            "bytes": PDF.stat().st_size,
            "sha256": digest(PDF),
            "pages": len(reader.pages),
            "paper": "A4",
            "encrypted": False,
            "terminal_start_page": terminal_start,
            "terminal_pages_checked": len(reader.pages) - terminal_start + 1,
            "terminal_marker_pages": marker_pages,
        },
        "build_receipt": {
            "path": "build/reader-id/BUILD_RECEIPT.json",
            "bytes": RECEIPT.stat().st_size,
            "sha256": digest(RECEIPT),
            "input_count": len(build_receipt["inputs"]),
            "source_markdown_input_count": len(source_rows),
            "output_count": len(build_receipt["outputs"]),
            "html_log_bytes": BUILD_FACTS["build/reader-id/pandoc-html.log"][0],
            "pdf_log_bytes": BUILD_FACTS["build/reader-id/pandoc-pdf.log"][0],
        },
        "authority_units_19_21": authority_summary,
        "baseline_and_checkpoint_facts": facts,
        "checks": [
            "exact Units 1-18 machine/protected baseline bound",
            "exact Units 19-21 authority and translation/integration QA bound",
            f"all {len(build_receipt['inputs'])} build-receipt inputs replayed from their recorded bytes and hashes",
            "cumulative IDs, exercises, solutions, and media measured from bound source/authority inputs",
            "HTML IDs, MathML/TeX annotations, media alts, anchors, and local resources closed",
            "PDF metadata, A4 geometry, measured page boundary, and ordered terminal markers closed",
            "Pandoc warning logs empty",
            "no placeholder or secret-like source content",
        ],
        "provenance": MODEL,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": "PASS",
                "receipt": OUT.relative_to(ROOT).as_posix(),
                "bytes": OUT.stat().st_size,
                "sha256": digest(OUT),
                "pages": len(reader.pages),
                "mathml": mathml_nodes,
                "stable_ids": len(stable_ids),
                "exercises": exercise_count,
                "solutions": solution_count,
                "images": len(images),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
