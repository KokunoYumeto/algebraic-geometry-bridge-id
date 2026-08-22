#!/usr/bin/env python3
"""Fail-closed structural, mathematical-surface, and artifact QA through Unit 5."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader

import qa_reader_units_01_04 as prior


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "id-ID"
BUILD = ROOT / "build" / "reader-id"
CSS = SOURCE / "reader.css"
PDF_HEADER = SOURCE / "pdf-header.tex"
PDF = BUILD / "algebraic-geometry-bridge-id-units-01-05.pdf"
HTML = BUILD / "index.html"
RECEIPT = BUILD / "BUILD_RECEIPT.json"
HTML_LOG = BUILD / "pandoc-html.log"
PDF_LOG = BUILD / "pandoc-pdf.log"
OUT = ROOT / "qa" / "UNITS_01_05_MACHINE_QA.json"
EXPECTED_PDF_PAGES = 96

SOURCES = (
    SOURCE / "frontmatter-units-01-05.md",
    SOURCE / "lecture-01.md",
    SOURCE / "worksheet-01.md",
    SOURCE / "worksheet-01-solutions.md",
    SOURCE / "lecture-02.md",
    SOURCE / "worksheet-02.md",
    SOURCE / "worksheet-02-solutions.md",
    SOURCE / "lecture-03.md",
    SOURCE / "worksheet-03.md",
    SOURCE / "worksheet-03-solutions.md",
    SOURCE / "lecture-04.md",
    SOURCE / "worksheet-04.md",
    SOURCE / "worksheet-04-solutions.md",
    SOURCE / "lecture-05.md",
    SOURCE / "worksheet-05.md",
    SOURCE / "worksheet-05-solutions.md",
    SOURCE / "media-credits.md",
    SOURCE / "media-credits-unit-02.md",
    SOURCE / "media-credits-unit-03.md",
    SOURCE / "media-credits-unit-04.md",
    SOURCE / "media-credits-unit-05.md",
)

EXPECTED = dict(prior.EXPECTED)
EXPECTED.update(
    {
        SOURCE / "lecture-05.md": {"math": 182, "images": 2, "headers": 18},
        SOURCE / "worksheet-05.md": {"math": 100, "images": 1, "exercises": 27, "headers": 30},
        SOURCE / "worksheet-05-solutions.md": {"math": 58, "images": 0, "solutions": 4, "headers": 5},
    }
)


def verify_unit5_authority() -> dict:
    path = ROOT / "authority" / "wikiversity" / "unit-05" / "UNIT_AUTHORITY_MANIFEST.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    prior.require(manifest["unit_number"] == 5, "Unit 5 manifest unit")
    prior.require(manifest["lecture"]["revid"] == 1051269, "Unit 5 lecture revision")
    prior.require(manifest["worksheet"]["revid"] == 1062652, "Unit 5 worksheet revision")
    prior.require(manifest["lecture_transclusion_closure"]["requested_template_count"] == 101, "Unit 5 lecture template count")
    prior.require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 101, "Unit 5 lecture captured transclusions")
    prior.require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "Unit 5 lecture missing transclusion")
    prior.require(manifest["worksheet_transclusion_closure"]["requested_template_count"] == 115, "Unit 5 worksheet template count")
    prior.require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 115, "Unit 5 worksheet captured transclusions")
    prior.require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "Unit 5 worksheet missing transclusion")
    for row in manifest["files"]:
        witness = path.parent / row["file"]
        prior.require(witness.stat().st_size == row["bytes"] and prior.digest(witness) == row["sha256"], f"Unit 5 authority replay {row['file']}")
    pdf_pages = []
    for row in manifest["official_pdf_witnesses"]:
        witness = ROOT / row["local_path"]
        prior.require(witness.stat().st_size == row["local_bytes"] and prior.digest(witness) == row["local_sha256"], f"Unit 5 official PDF replay {witness.name}")
        pdf_pages.append(len(PdfReader(witness).pages))
    prior.require(sorted(pdf_pages) == [7, 9], "Unit 5 official PDF page closure")
    return {
        "manifest_sha256": prior.digest(path),
        "file_count": len(manifest["files"]),
        "lecture_revid": 1051269,
        "worksheet_revid": 1062652,
        "official_pdf_pages": pdf_pages,
    }


def main() -> int:
    for path in (*SOURCES, CSS, PDF_HEADER, HTML, PDF, RECEIPT, HTML_LOG, PDF_LOG):
        prior.require(path.is_file() and not path.is_symlink(), f"missing/nonregular input {path}")

    combined = "\n".join(path.read_text(encoding="utf-8") for path in SOURCES)
    prior.require("<!-- QA:" not in combined, "unresolved QA marker")
    prior.require("pending_component_audit" not in combined, "pending rights marker")
    prior.require("translation_status: draft" not in combined, "draft translation marker")
    prior.require("\t" not in combined, "tab in reader source")
    visible = re.sub(r"<!--.*?-->", "", combined, flags=re.S)
    visible = re.sub(r"^---\n.*?\n---$", "", visible, flags=re.S | re.M)
    prior.require(
        re.search(r"\b(Es sei|Zeige|Bestimme|Somit|Damit|Nullstellengebilde|Aufgaben zum Abgeben|Beweis|Körper|Menge|Abbildung)\b", visible) is None,
        "active untranslated German prose marker",
    )
    prior.require(re.search(r"github_pat_|ghp_[A-Za-z0-9]{20,}|ZENODO_ACCESS_TOKEN", combined) is None, "credential-shaped text")
    prior.require("Petunjuk sumber" in combined and "Jangan gunakan Soal 3.18" in combined, "Unit 3 source hint")
    prior.require("V(\\mathfrak p)=\\varnothing" in combined and "\\mathfrak p=(X^2+1)" in combined, "Unit 4 edition note")
    prior.require(combined.count("**Catatan edisi:**") == 4, "edition-note closure")
    prior.require("setelah menetapkan $Y=a$" in combined, "Unit 5 coordinate-order note")
    prior.require("gelanggang fungsi komponen" in combined, "Unit 5 parameter-ring note")
    prior.require("faktor $a_n^n$" in combined, "Unit 5 coefficient-product note")
    prior.require(r"{1\over X^2+Y^2+1}" not in combined, "raw TeX fraction remains")
    prior.require(r"\frac{1}{X^2+Y^2+1}" in combined, "MathML-compatible fraction absent")

    css_text = CSS.read_text(encoding="utf-8")
    prior.require('math[display="block"]' in css_text, "responsive display-math selector missing")
    prior.require("overflow-x: auto" in css_text, "local display-math overflow rule missing")
    prior.require("overflow-wrap: anywhere" in css_text, "long-link wrapping rule missing")
    prior.require("\\usepackage{pifont}" in PDF_HEADER.read_text(encoding="utf-8"), "PDF star fallback header missing")

    ids: list[str] = []
    ast_summary: dict[str, dict[str, int]] = {}
    for path in SOURCES:
        ids.extend(prior.source_ids(path))
        if path in EXPECTED:
            counts = prior.ast_counts(prior.pandoc_ast(path))
            expectation = EXPECTED[path]
            prior.require(counts.get("Math", 0) == expectation["math"], f"{path.name} math count")
            prior.require(counts.get("Image", 0) == expectation["images"], f"{path.name} image count")
            prior.require(counts.get("Header", 0) == expectation["headers"], f"{path.name} header count")
            if "exercises" in expectation:
                count = len(re.findall(r"^### Soal \d+\.\d+", path.read_text(encoding="utf-8"), flags=re.M))
                prior.require(count == expectation["exercises"], f"{path.name} exercise count")
            if "solutions" in expectation:
                count = len(re.findall(r"^## Solusi Soal \d+\.\d+", path.read_text(encoding="utf-8"), flags=re.M))
                prior.require(count == expectation["solutions"], f"{path.name} solution count")
            ast_summary[path.name] = {key: counts.get(key, 0) for key in ("Header", "Math", "Image")}
    prior.require(len(ids) == len(set(ids)) == 273, f"stable ID closure: {len(ids)}")
    prior.require(all(identifier.startswith(("agc-", "br-ak-2025-2026-")) for identifier in ids), "noncanonical stable ID")

    solution_summary = {
        "unit_01": prior.verify_solution_map(1, SOURCE / "worksheet-01-solutions.md", 28, 7),
        "unit_02": prior.verify_solution_map(2, SOURCE / "worksheet-02-solutions.md", 27, 9),
        "unit_03": prior.verify_solution_map(3, SOURCE / "worksheet-03-solutions.md", 22, 2),
        "unit_04": prior.verify_solution_map(4, SOURCE / "worksheet-04-solutions.md", 30, 6),
        "unit_05": prior.verify_solution_map(5, SOURCE / "worksheet-05-solutions.md", 27, 4),
    }
    rights_summary = {
        "unit_01": prior.verify_rights("RIGHTS.csv", "ASSET_CLOSURE.json", 23, 26),
        "unit_02": prior.verify_rights("RIGHTS-unit-02.csv", "ASSET_CLOSURE-unit-02.json", 2, 3),
        "unit_03": prior.verify_rights("RIGHTS-unit-03.csv", "ASSET_CLOSURE-unit-03.json", 4, 4),
        "unit_04": prior.verify_rights("RIGHTS-unit-04.csv", "ASSET_CLOSURE-unit-04.json", 9, 11),
        "unit_05": prior.verify_rights("RIGHTS-unit-05.csv", "ASSET_CLOSURE-unit-05.json", 3, 4),
    }
    authority_summary = {
        "unit_03": prior.verify_unit3_authority(),
        "unit_04": prior.verify_unit4_authority(),
        "unit_05": verify_unit5_authority(),
    }

    html_bytes = HTML.read_bytes()
    soup = BeautifulSoup(html_bytes, "html.parser")
    prior.require(soup.html is not None and soup.html.get("lang") == "id-ID", "HTML language")
    prior.require(soup.title is not None and soup.title.get_text(strip=True) == "Kurva Aljabar - Unit 1-5", "HTML title")
    for identifier in ids:
        prior.require(len(soup.select(f"[id='{identifier}']")) == 1, f"HTML ID closure {identifier}")
    html_ids = {node.get("id") for node in soup.find_all(id=True)}
    missing_internal = sorted(
        href[1:]
        for node in soup.find_all(href=True)
        if (href := node.get("href", "")).startswith("#") and href[1:] not in html_ids
    )
    prior.require(not missing_internal, f"broken internal HTML links: {missing_internal[:5]}")
    images = soup.find_all("img")
    prior.require(len(images) == 41, f"HTML image count {len(images)}")
    prior.require(all(image.get("alt", "").strip() for image in images), "missing HTML image alt text")
    prior.require(all(not re.match(r"https?://", image.get("src", "")) for image in images), "remote HTML image")
    prior.require(len(soup.find_all("math")) == 1794, f"HTML MathML count {len(soup.find_all('math'))}")
    html_text = soup.get_text(" ", strip=True)
    for marker in (
        "Kuliah 5: Komponen Homogen",
        "Soal 5.27 - 4 poin",
        "Solusi Soal 5.20",
        "Kredit media Unit 5",
    ):
        prior.require(marker in html_text, f"HTML marker absent: {marker}")
    prior.require("★" in html_text, "HTML source-star markers absent")
    prior.require(re.search(rb"github_pat_|ghp_[A-Za-z0-9]{20,}", html_bytes) is None, "credential in HTML")

    for log in (HTML_LOG, PDF_LOG):
        text = log.read_text(encoding="utf-8")
        prior.require(not re.search(r"Warning|Error|Missing|not found|Overfull|Underfull", text, flags=re.I), f"build warning in {log.name}")

    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    prior.require(receipt["schema"] == "ag-bridge-build-receipt-v2", "build receipt schema")
    prior.require(receipt["through_unit"] == 5, "build receipt scope")
    for row in receipt["inputs"]:
        path = ROOT / row["path"]
        prior.require(path.stat().st_size == row["bytes"] and prior.digest(path) == row["sha256"], f"build input replay {row['path']}")
    input_paths = {row["path"] for row in receipt["inputs"]}
    prior.require("source/id-ID/pdf-header.tex" in input_paths, "PDF header absent from build receipt")
    output_names = {Path(row["path"]).name for row in receipt["outputs"]}
    prior.require(output_names == {HTML.name, PDF.name}, "build output closure")
    for row in receipt["outputs"]:
        path = BUILD / Path(row["path"]).name
        prior.require(path.stat().st_size == row["bytes"] and prior.digest(path) == row["sha256"], f"build output replay {row['path']}")

    reader = PdfReader(PDF, strict=True)
    prior.require(not reader.is_encrypted, "PDF encrypted")
    prior.require(len(reader.pages) == EXPECTED_PDF_PAGES, f"PDF pages {len(reader.pages)}")
    prior.require(reader.metadata is not None and reader.metadata.title == "Kurva Aljabar - Unit 1-5", "PDF title metadata")
    pdf_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    for marker in (
        "Kuliah 4: Ketaktereduksian, Komponen, dan Irisan Kurva",
        "Kredit media Unit 4",
        "Kuliah 5: Komponen Homogen",
        "Soal 5.27 - 4 poin",
        "Solusi Soal 5.20",
        "Kredit media Unit 5",
    ):
        prior.require(marker in pdf_text, f"PDF text marker absent: {marker}")
    prior.require("pending_component_audit" not in pdf_text, "pending marker in PDF")

    pdffonts = prior.shutil.which("pdffonts")
    prior.require(bool(pdffonts), "pdffonts unavailable")
    fonts = subprocess.run([pdffonts, str(PDF)], capture_output=True, text=True, encoding="utf-8", check=True).stdout
    font_rows = [line.split() for line in fonts.splitlines()[2:] if line.strip()]
    prior.require(font_rows and all("yes" in row for row in font_rows), "PDF contains an unembedded font")
    prior.require(all("Type 3" not in line for line in fonts.splitlines()), "PDF contains Type 3 font")
    prior.require(any("Dingbats" in line or "Zapf" in line for line in fonts.splitlines()), "PDF black-star fallback font absent")

    result = {
        "schema": "ag-bridge-machine-qa-receipt-v3",
        "tested_build_utc": receipt["built_utc"],
        "status": "PASS",
        "through_unit": 5,
        "stable_ids": len(ids),
        "ast_surfaces": ast_summary,
        "solutions": solution_summary,
        "rights": rights_summary,
        "authority": authority_summary,
        "html": {
            "bytes": HTML.stat().st_size,
            "sha256": prior.digest(HTML),
            "images": len(images),
            "mathml_nodes": len(soup.find_all("math")),
            "broken_internal_links": 0,
            "remote_images": 0,
            "build_warnings": 0,
            "responsive_css_sha256": prior.digest(CSS),
        },
        "pdf": {
            "bytes": PDF.stat().st_size,
            "sha256": prior.digest(PDF),
            "pages": len(reader.pages),
            "encrypted": False,
            "font_rows": len(font_rows),
            "unembedded_fonts": 0,
            "type3_fonts": 0,
            "build_warnings": 0,
            "source_star_fallback_embedded": True,
        },
        "build_receipt": {"bytes": RECEIPT.stat().st_size, "sha256": prior.digest(RECEIPT)},
        "qa_script": {"path": Path(__file__).relative_to(ROOT).as_posix(), "sha256": prior.digest(Path(__file__))},
        "check_families": [
            "source_placeholders_language_notes_and_secrets",
            "pandoc_math_image_heading_and_stable_id_surfaces",
            "exercise_solution_revision_and_witness_closure",
            "component_rights_and_asset_hash_closure",
            "unit3_unit4_unit5_authority_and_official_pdf_hash_replay",
            "html_language_alt_mathml_internal_links_local_assets_and_star_markers",
            "warning_free_build_and_input_output_receipt_replay",
            "pdf_structure_metadata_text_embedded_fonts_and_star_fallback",
        ],
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
