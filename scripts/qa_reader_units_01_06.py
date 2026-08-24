#!/usr/bin/env python3
"""Fail-closed structural, mathematical-surface, and artifact QA through Unit 6."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader

import qa_reader_units_01_05 as previous


base = previous.prior
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "id-ID"
BUILD = ROOT / "build" / "reader-id"
CSS = SOURCE / "reader.css"
PDF_HEADER = SOURCE / "pdf-header.tex"
PDF = BUILD / "algebraic-geometry-bridge-id-units-01-06.pdf"
HTML = BUILD / "index.html"
RECEIPT = BUILD / "BUILD_RECEIPT.json"
HTML_LOG = BUILD / "pandoc-html.log"
PDF_LOG = BUILD / "pandoc-pdf.log"
OUT = ROOT / "qa" / "UNITS_01_06_MACHINE_QA.json"
EXPECTED_PDF_PAGES = 117

SOURCES = (
    SOURCE / "frontmatter-units-01-06.md",
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
    SOURCE / "lecture-06.md",
    SOURCE / "worksheet-06.md",
    SOURCE / "worksheet-06-solutions.md",
    SOURCE / "media-credits.md",
    SOURCE / "media-credits-unit-02.md",
    SOURCE / "media-credits-unit-03.md",
    SOURCE / "media-credits-unit-04.md",
    SOURCE / "media-credits-unit-05.md",
    SOURCE / "media-credits-unit-06.md",
)

EXPECTED = dict(previous.EXPECTED)
EXPECTED.update(
    {
        SOURCE / "lecture-06.md": {"math": 142, "images": 3, "headers": 17},
        SOURCE / "worksheet-06.md": {"math": 109, "images": 0, "exercises": 30, "headers": 33},
        SOURCE / "worksheet-06-solutions.md": {"math": 105, "images": 0, "solutions": 9, "headers": 10},
    }
)


def verify_unit6_authority() -> dict:
    path = ROOT / "authority" / "wikiversity" / "unit-06" / "UNIT_AUTHORITY_MANIFEST.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    base.require(manifest["unit_number"] == 6, "Unit 6 manifest unit")
    base.require(manifest["lecture"]["revid"] == 1112253, "Unit 6 lecture revision")
    base.require(manifest["worksheet"]["revid"] == 1059354, "Unit 6 worksheet revision")
    base.require(manifest["lecture_transclusion_closure"]["requested_template_count"] == 95, "Unit 6 lecture template count")
    base.require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 95, "Unit 6 lecture captured transclusions")
    base.require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "Unit 6 lecture missing transclusion")
    base.require(manifest["worksheet_transclusion_closure"]["requested_template_count"] == 110, "Unit 6 worksheet template count")
    base.require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 110, "Unit 6 worksheet captured transclusions")
    base.require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "Unit 6 worksheet missing transclusion")
    for row in manifest["files"]:
        witness = path.parent / row["file"]
        base.require(
            witness.stat().st_size == row["bytes"] and base.digest(witness) == row["sha256"],
            f"Unit 6 authority replay {row['file']}",
        )
    pdf_pages = []
    for row in manifest["official_pdf_witnesses"]:
        witness = ROOT / row["local_path"]
        base.require(
            witness.stat().st_size == row["local_bytes"] and base.digest(witness) == row["local_sha256"],
            f"Unit 6 official PDF replay {witness.name}",
        )
        pdf_pages.append(len(PdfReader(witness).pages))
    base.require(sorted(pdf_pages) == [7, 9], "Unit 6 official PDF page closure")
    base.require(
        base.digest(path) == "b1dcf2007e4740e7123421d2510ecd86dbf4a91b35ea83db99fbf5c77a9e01dd",
        "Unit 6 authority manifest identity",
    )
    return {
        "manifest_sha256": base.digest(path),
        "file_count": len(manifest["files"]),
        "lecture_revid": 1112253,
        "worksheet_revid": 1059354,
        "official_pdf_pages": pdf_pages,
    }


def main() -> int:
    for path in (*SOURCES, CSS, PDF_HEADER, HTML, PDF, RECEIPT, HTML_LOG, PDF_LOG):
        base.require(path.is_file() and not path.is_symlink(), f"missing/nonregular input {path}")

    combined = "\n".join(path.read_text(encoding="utf-8") for path in SOURCES)
    base.require("<!-- QA:" not in combined, "unresolved QA marker")
    base.require("pending_component_audit" not in combined, "pending rights marker")
    base.require("translation_status: draft" not in combined, "draft translation marker")
    base.require("\t" not in combined, "tab in reader source")
    visible = re.sub(r"<!--.*?-->", "", combined, flags=re.S)
    visible = re.sub(r"^---\n.*?\n---$", "", visible, flags=re.S | re.M)
    base.require(
        re.search(r"\b(Es sei|Zeige|Bestimme|Somit|Damit|Nullstellengebilde|Aufgaben zum Abgeben|Beweis|Körper|Menge|Abbildung)\b", visible) is None,
        "active untranslated German prose marker",
    )
    base.require(re.search(r"github_pat_|ghp_[A-Za-z0-9]{20,}|ZENODO_ACCESS_TOKEN", combined) is None, "credential-shaped text")
    base.require(combined.count("**Catatan edisi:**") == 4, "edition-note closure")
    base.require("G(X,Y)=F(X,Y,1)" in combined, "Unit 6 dehomogenized polynomial clarification")
    base.require("Tidak ada\nsolusi tambahan yang dibuat" in combined, "Unit 6 no-invented-solution notice")

    corrections = (ROOT / "00_control" / "CORRECTIONS.csv").read_text(encoding="utf-8")
    for marker in ("AGC-CORR-0010", "AGC-ADAPT-0008", "AGC-ADAPT-0009", "AGC-ADAPT-0010", "AGC-ADAPT-0011"):
        base.require(marker in corrections, f"Unit 6 delta ledger marker {marker}")

    css_text = CSS.read_text(encoding="utf-8")
    base.require('math[display="block"]' in css_text, "responsive display-math selector missing")
    base.require("overflow-x: auto" in css_text, "local display-math overflow rule missing")
    base.require("overflow-wrap: anywhere" in css_text, "long-link wrapping rule missing")
    header_text = PDF_HEADER.read_text(encoding="utf-8")
    base.require("\\usepackage{pifont}" in header_text, "PDF star fallback header missing")
    base.require("\\renewcommand\\subsubsection" in header_text, "PDF block-heading reflow missing")

    ids: list[str] = []
    ast_summary: dict[str, dict[str, int]] = {}
    for path in SOURCES:
        ids.extend(base.source_ids(path))
        if path in EXPECTED:
            counts = base.ast_counts(base.pandoc_ast(path))
            expectation = EXPECTED[path]
            base.require(counts.get("Math", 0) == expectation["math"], f"{path.name} math count")
            base.require(counts.get("Image", 0) == expectation["images"], f"{path.name} image count")
            base.require(counts.get("Header", 0) == expectation["headers"], f"{path.name} header count")
            if "exercises" in expectation:
                count = len(re.findall(r"^### Soal \d+\.\d+", path.read_text(encoding="utf-8"), flags=re.M))
                base.require(count == expectation["exercises"], f"{path.name} exercise count")
            if "solutions" in expectation:
                count = len(re.findall(r"^## Solusi Soal \d+\.\d+", path.read_text(encoding="utf-8"), flags=re.M))
                base.require(count == expectation["solutions"], f"{path.name} solution count")
            ast_summary[path.name] = {key: counts.get(key, 0) for key in ("Header", "Math", "Image")}
    base.require(len(ids) == len(set(ids)) == 334, f"stable ID closure: {len(ids)}")
    base.require(all(identifier.startswith(("agc-", "br-ak-2025-2026-")) for identifier in ids), "noncanonical stable ID")

    solution_summary = {
        "unit_01": base.verify_solution_map(1, SOURCE / "worksheet-01-solutions.md", 28, 7),
        "unit_02": base.verify_solution_map(2, SOURCE / "worksheet-02-solutions.md", 27, 9),
        "unit_03": base.verify_solution_map(3, SOURCE / "worksheet-03-solutions.md", 22, 2),
        "unit_04": base.verify_solution_map(4, SOURCE / "worksheet-04-solutions.md", 30, 6),
        "unit_05": base.verify_solution_map(5, SOURCE / "worksheet-05-solutions.md", 27, 4),
        "unit_06": base.verify_solution_map(6, SOURCE / "worksheet-06-solutions.md", 30, 9),
    }
    rights_summary = {
        "unit_01": base.verify_rights("RIGHTS.csv", "ASSET_CLOSURE.json", 23, 26),
        "unit_02": base.verify_rights("RIGHTS-unit-02.csv", "ASSET_CLOSURE-unit-02.json", 2, 3),
        "unit_03": base.verify_rights("RIGHTS-unit-03.csv", "ASSET_CLOSURE-unit-03.json", 4, 4),
        "unit_04": base.verify_rights("RIGHTS-unit-04.csv", "ASSET_CLOSURE-unit-04.json", 9, 11),
        "unit_05": base.verify_rights("RIGHTS-unit-05.csv", "ASSET_CLOSURE-unit-05.json", 3, 4),
        "unit_06": base.verify_rights("RIGHTS-unit-06.csv", "ASSET_CLOSURE-unit-06.json", 3, 4),
    }
    authority_summary = {
        "unit_03": base.verify_unit3_authority(),
        "unit_04": base.verify_unit4_authority(),
        "unit_05": previous.verify_unit5_authority(),
        "unit_06": verify_unit6_authority(),
    }

    html_bytes = HTML.read_bytes()
    soup = BeautifulSoup(html_bytes, "html.parser")
    base.require(soup.html is not None and soup.html.get("lang") == "id-ID", "HTML language")
    base.require(soup.title is not None and soup.title.get_text(strip=True) == "Kurva Aljabar - Unit 1-6", "HTML title")
    for identifier in ids:
        base.require(len(soup.select(f"[id='{identifier}']")) == 1, f"HTML ID closure {identifier}")
    html_ids = {node.get("id") for node in soup.find_all(id=True)}
    missing_internal = sorted(
        href[1:]
        for node in soup.find_all(href=True)
        if (href := node.get("href", "")).startswith("#") and href[1:] not in html_ids
    )
    base.require(not missing_internal, f"broken internal HTML links: {missing_internal[:5]}")
    images = soup.find_all("img")
    base.require(len(images) == 44, f"HTML image count {len(images)}")
    base.require(all(image.get("alt", "").strip() for image in images), "missing HTML image alt text")
    base.require(all(not re.match(r"https?://", image.get("src", "")) for image in images), "remote HTML image")
    base.require(len(soup.find_all("math")) == 2150, f"HTML MathML count {len(soup.find_all('math'))}")
    html_text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
    for marker in (
        "Kuliah 6: Parametrisasi Polinomial dan Rasional",
        "Soal 6.30 - 4 poin",
        "Solusi Soal 6.25",
        "Kredit media Unit 6",
    ):
        base.require(marker in html_text, f"HTML marker absent: {marker}")
    base.require("★" in html_text, "HTML source-star markers absent")
    base.require(re.search(rb"github_pat_|ghp_[A-Za-z0-9]{20,}", html_bytes) is None, "credential in HTML")

    for log in (HTML_LOG, PDF_LOG):
        text = log.read_text(encoding="utf-8")
        base.require(not re.search(r"Warning|Error|Missing|not found|Overfull|Underfull", text, flags=re.I), f"build warning in {log.name}")

    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    base.require(receipt["schema"] == "ag-bridge-build-receipt-v2", "build receipt schema")
    base.require(receipt["through_unit"] == 6, "build receipt scope")
    for row in receipt["inputs"]:
        path = ROOT / row["path"]
        base.require(path.stat().st_size == row["bytes"] and base.digest(path) == row["sha256"], f"build input replay {row['path']}")
    input_paths = {row["path"] for row in receipt["inputs"]}
    base.require("source/id-ID/pdf-header.tex" in input_paths, "PDF header absent from build receipt")
    output_names = {Path(row["path"]).name for row in receipt["outputs"]}
    base.require(output_names == {HTML.name, PDF.name}, "build output closure")
    for row in receipt["outputs"]:
        path = BUILD / Path(row["path"]).name
        base.require(path.stat().st_size == row["bytes"] and base.digest(path) == row["sha256"], f"build output replay {row['path']}")

    reader = PdfReader(PDF, strict=True)
    base.require(not reader.is_encrypted, "PDF encrypted")
    base.require(len(reader.pages) == EXPECTED_PDF_PAGES, f"PDF pages {len(reader.pages)}")
    base.require(reader.metadata is not None and reader.metadata.title == "Kurva Aljabar - Unit 1-6", "PDF title metadata")
    pdf_text = re.sub(r"\s+", " ", "\n".join(page.extract_text() or "" for page in reader.pages))
    for marker in (
        "Kuliah 5: Komponen Homogen",
        "Kuliah 6: Parametrisasi Polinomial dan Rasional",
        "Soal 6.30 - 4 poin",
        "Solusi Soal 6.25",
        "Kredit media Unit 6",
    ):
        base.require(marker in pdf_text, f"PDF text marker absent: {marker}")
    base.require("pending_component_audit" not in pdf_text, "pending marker in PDF")

    pdffonts = base.shutil.which("pdffonts")
    base.require(bool(pdffonts), "pdffonts unavailable")
    fonts = subprocess.run([pdffonts, str(PDF)], capture_output=True, text=True, encoding="utf-8", check=True).stdout
    font_rows = [line.split() for line in fonts.splitlines()[2:] if line.strip()]
    base.require(font_rows and all("yes" in row for row in font_rows), "PDF contains an unembedded font")
    base.require(all("Type 3" not in line for line in fonts.splitlines()), "PDF contains Type 3 font")
    base.require(any("Dingbats" in line or "Zapf" in line for line in fonts.splitlines()), "PDF black-star fallback font absent")

    result = {
        "schema": "ag-bridge-machine-qa-receipt-v3",
        "tested_build_utc": receipt["built_utc"],
        "status": "PASS",
        "through_unit": 6,
        "stable_ids": len(ids),
        "ast_surfaces": ast_summary,
        "solutions": solution_summary,
        "rights": rights_summary,
        "authority": authority_summary,
        "html": {
            "bytes": HTML.stat().st_size,
            "sha256": base.digest(HTML),
            "images": len(images),
            "mathml_nodes": len(soup.find_all("math")),
            "broken_internal_links": 0,
            "remote_images": 0,
            "build_warnings": 0,
            "responsive_css_sha256": base.digest(CSS),
        },
        "pdf": {
            "bytes": PDF.stat().st_size,
            "sha256": base.digest(PDF),
            "pages": len(reader.pages),
            "encrypted": False,
            "font_rows": len(font_rows),
            "unembedded_fonts": 0,
            "type3_fonts": 0,
            "build_warnings": 0,
            "source_star_fallback_embedded": True,
            "block_heading_reflow": True,
        },
        "build_receipt": {"bytes": RECEIPT.stat().st_size, "sha256": base.digest(RECEIPT)},
        "qa_script": {"path": Path(__file__).relative_to(ROOT).as_posix(), "sha256": base.digest(Path(__file__))},
        "check_families": [
            "source_placeholders_language_notes_deltas_and_secrets",
            "pandoc_math_image_heading_and_stable_id_surfaces",
            "exercise_solution_revision_and_witness_closure",
            "component_rights_and_asset_hash_closure",
            "unit3_through_unit6_authority_and_official_pdf_hash_replay",
            "html_language_alt_mathml_internal_links_local_assets_and_star_markers",
            "warning_free_build_and_input_output_receipt_replay",
            "pdf_structure_metadata_text_embedded_fonts_star_fallback_and_heading_reflow",
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
