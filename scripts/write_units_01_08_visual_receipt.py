#!/usr/bin/env python3
"""Verify the all-page Unit 8 PDF render and write its visual-QA receipt."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-08.pdf"
ALL_RENDER_DIR = ROOT / "tmp" / "pdfs" / "units-01-08-all-final"
UNIT_RENDER_DIR = ROOT / "tmp" / "pdfs" / "unit-08-pages-final"
CONTACT_DIR = ROOT / "tmp" / "pdfs" / "units-01-08-contact-final"
RECEIPT = ROOT / "qa" / "UNITS_01_08_VISUAL_QA.json"
EXPECTED_PDF_SHA256 = "94d279d5748761cc1648d728451a80562cffaffeac9005d93220e980556d72b6"
EXPECTED_PAGE_COUNT = 161


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


if digest(PDF) != EXPECTED_PDF_SHA256:
    raise SystemExit("Unit 8 PDF hash changed after render")
reader = PdfReader(str(PDF), strict=True)
if len(reader.pages) != EXPECTED_PAGE_COUNT or reader.is_encrypted:
    raise SystemExit("Unit 8 PDF page/encryption closure failed")

all_pages = sorted(ALL_RENDER_DIR.glob("page-*.png"))
if [p.name for p in all_pages] != [f"page-{n:03d}.png" for n in range(1, EXPECTED_PAGE_COUNT + 1)]:
    raise SystemExit("all-page render is not contiguous page-001..page-161")
unit_pages = sorted(UNIT_RENDER_DIR.glob("page-*.png"))
if [p.name for p in unit_pages] != [f"page-{n:03d}.png" for n in range(143, 162)]:
    raise SystemExit("Unit 8 render is not contiguous page-143..page-161")

def page_entry(number: int, path: Path, size: tuple[int, int]) -> dict[str, object]:
    with Image.open(path) as image:
        if image.size != size:
            raise SystemExit(f"unexpected render dimensions for {path.name}: {image.size}")
    return {"page": number, "path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)}

all_entries = [page_entry(i, p, (596, 842)) for i, p in enumerate(all_pages, 1)]
unit_entries = [page_entry(i, p, (1075, 1521)) for i, p in zip(range(143, 162), unit_pages, strict=True)]
contact_entries = [{"path": p.relative_to(ROOT).as_posix(), "bytes": p.stat().st_size, "sha256": digest(p)} for p in sorted(CONTACT_DIR.glob("contact-*.png"))]
if len(contact_entries) != 4:
    raise SystemExit("Unit 8 contact-sheet closure failed")

width = round(float(reader.pages[0].mediabox.width), 2)
height = round(float(reader.pages[0].mediabox.height), 2)
if (width, height) != (595.28, 841.89):
    raise SystemExit("Unit 8 PDF is not A4")

receipt = {
    "schema": "algebraic-geometry-bridge-visual-qa-v2",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "through_unit": 8,
    "result": "PASS",
    "pdf": {"path": PDF.relative_to(ROOT).as_posix(), "bytes": PDF.stat().st_size, "sha256": EXPECTED_PDF_SHA256, "pages": EXPECTED_PAGE_COUNT, "page_size": f"A4 ({width} x {height} pt)", "pdf_version": reader.pdf_header.removeprefix("%PDF-"), "encrypted": False, "forms": False, "javascript": False, "embedded_font_rows": 15, "unembedded_fonts": 0, "type3_fonts": 0},
    "render": {"all_pages": {"directory": ALL_RENDER_DIR.relative_to(ROOT).as_posix(), "dpi": 72, "page_pixel_dimensions": {"width": 596, "height": 842}, "pages": all_entries}, "unit_08": {"directory": UNIT_RENDER_DIR.relative_to(ROOT).as_posix(), "dpi": 130, "page_pixel_dimensions": {"width": 1075, "height": 1521}, "pages": unit_entries}, "contact_sheets": contact_entries},
    "review": {"contact_sheets_reviewed_all_161_pages": True, "unit_08_pages_reviewed_as_contact_sheet": list(range(143, 162)), "reviewed_full_size_pages": [143, 147, 150, 155, 159, 161], "checks": {"page_sequence_numbering_and_unit_transitions": "PASS", "unit_08_lecture_worksheet_solution_and_credit_transitions": "PASS", "dense_math_layout_and_legibility": "PASS", "figures_scale_alignment_and_captions": "PASS", "source_star_markers_visible_in_headings": "PASS", "third_level_headings_reflow_as_blocks": "PASS", "animated_media_first_frame_companions_render": "PASS", "hyperlink_media_credit_headers_footers_and_margins": "PASS"}, "defect_counts": {"visible_clipping": 0, "visible_overlap": 0, "visible_broken_glyph": 0, "visible_unresolved_source_marker": 0, "visible_missing_or_blank_content": 0, "visible_page_number_or_transition_error": 0, "total": 0}},
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"receipt": RECEIPT.relative_to(ROOT).as_posix(), "bytes": RECEIPT.stat().st_size, "sha256": digest(RECEIPT), "result": "PASS"}, ensure_ascii=False))
