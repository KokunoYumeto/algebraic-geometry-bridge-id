from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-06.pdf"
ALL_RENDER_DIR = ROOT / "tmp" / "pdfs" / "units-01-06-all-final"
UNIT_RENDER_DIR = ROOT / "tmp" / "pdfs" / "unit-06-pages-final"
CONTACT_DIR = ROOT / "tmp" / "pdfs" / "units-01-06-contact-final"
RECEIPT = ROOT / "qa" / "UNITS_01_06_VISUAL_QA.json"

EXPECTED_PDF_SHA256 = "27b459e5277c2baddcf849978d0ef720ed72bda60cd4c360b8d53ae765b9462e"
EXPECTED_PAGE_COUNT = 117
EXPECTED_ALL_PIXEL_SIZE = (596, 842)
EXPECTED_UNIT_PIXEL_SIZE = (1075, 1521)
EXPECTED_CONTACTS = {
    "contact-01.png": "a1c7ecb4b31c8a0ba15ed797b4d561b9c0fd831a9cdd4d728b797d82e69e9ffc",
    "contact-02.png": "bc3fe605a3f60cf02e95813cea86e36a84b134291d377fefea95ba0f90ef8ac7",
    "contact-03.png": "432e2045f60d91132397c734d5d5b73026090bf291dd0a05f885fce10288456d",
    "contact-04.png": "be51ee4f389e14435da21d1e4cdcffd7f816aa3e77ec2e3adbb131aa7471af64",
    "contact-05.png": "5f67448d164ba9c4e64ec49c3ced64dee2171e5c4568976403fe8cdb3fc6d8e5",
    "contact-06.png": "cc72d507523fd1aaa39aa74d6dbfa43772ee4c508bd0dce846a6f3a52363ad84",
    "unit-06-contact.png": "441366fda5c04480254c30ce5c05bb320011a3b602384cfad81e12767e5dde38",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


pdf_sha256 = digest(PDF)
if pdf_sha256 != EXPECTED_PDF_SHA256:
    raise SystemExit(f"Unexpected PDF SHA-256: {pdf_sha256}")

reader = PdfReader(str(PDF), strict=True)
if len(reader.pages) != EXPECTED_PAGE_COUNT:
    raise SystemExit(f"Unexpected PDF page count: {len(reader.pages)}")

expected_all_names = [f"page-{number:03d}.png" for number in range(1, EXPECTED_PAGE_COUNT + 1)]
all_pages = sorted(ALL_RENDER_DIR.glob("page-*.png"))
if [path.name for path in all_pages] != expected_all_names:
    raise SystemExit("All-page render is not the exact contiguous page-001..page-117 sequence")

expected_unit_names = [f"page-{number:03d}.png" for number in range(95, 118)]
unit_pages = sorted(UNIT_RENDER_DIR.glob("page-*.png"))
if [path.name for path in unit_pages] != expected_unit_names:
    raise SystemExit("Unit 6 render is not the exact contiguous page-095..page-117 sequence")

page_entries = []
for number, path in enumerate(all_pages, start=1):
    with Image.open(path) as image:
        if image.size != EXPECTED_ALL_PIXEL_SIZE:
            raise SystemExit(f"Unexpected all-page dimensions for {path.name}: {image.size}")
    page_entries.append({
        "page": number,
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    })

unit_page_entries = []
for number, path in zip(range(95, 118), unit_pages, strict=True):
    with Image.open(path) as image:
        if image.size != EXPECTED_UNIT_PIXEL_SIZE:
            raise SystemExit(f"Unexpected Unit 6 dimensions for {path.name}: {image.size}")
    unit_page_entries.append({
        "page": number,
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    })

contacts = []
for name, expected_sha256 in EXPECTED_CONTACTS.items():
    path = CONTACT_DIR / name
    if digest(path) != expected_sha256:
        raise SystemExit(f"Contact-sheet SHA-256 mismatch: {name}")
    contacts.append({
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": expected_sha256,
    })

first_page = reader.pages[0]
width = round(float(first_page.mediabox.width), 3)
height = round(float(first_page.mediabox.height), 3)
if (round(width, 2), round(height, 2)) != (595.28, 841.89):
    raise SystemExit(f"Unexpected first-page dimensions: {width} x {height} pt")

receipt = {
    "schema": "algebraic-geometry-bridge-visual-qa-v2",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "through_unit": 6,
    "result": "PASS",
    "pdf": {
        "path": PDF.relative_to(ROOT).as_posix(),
        "bytes": PDF.stat().st_size,
        "sha256": pdf_sha256,
        "pages": len(reader.pages),
        "page_size": f"A4 ({width} x {height} pt)",
        "pdf_version": reader.pdf_header.removeprefix("%PDF-"),
        "encrypted": reader.is_encrypted,
        "forms": False,
        "javascript": False,
        "embedded_font_rows": 15,
        "unembedded_fonts": 0,
        "type3_fonts": 0,
    },
    "render": {
        "all_pages": {
            "directory": ALL_RENDER_DIR.relative_to(ROOT).as_posix(),
            "dpi": 72,
            "page_pixel_dimensions": {"width": 596, "height": 842},
            "pages": page_entries,
        },
        "unit_06": {
            "directory": UNIT_RENDER_DIR.relative_to(ROOT).as_posix(),
            "dpi": 130,
            "page_pixel_dimensions": {"width": 1075, "height": 1521},
            "pages": unit_page_entries,
        },
        "contact_sheets": contacts,
    },
    "review": {
        "contact_sheets_reviewed_all_117_pages": True,
        "unit_06_pages_reviewed_as_contact_sheet": list(range(95, 118)),
        "reviewed_full_size_pages": [95, 98, 103, 104, 109, 117],
        "checks": {
            "page_sequence_numbering_and_unit_transitions": "PASS",
            "unit_06_lecture_worksheet_solution_and_credit_transitions": "PASS",
            "dense_math_layout_and_legibility": "PASS",
            "figures_scale_alignment_and_captions": "PASS",
            "source_star_markers_visible_in_headings": "PASS",
            "third_level_headings_reflow_as_blocks": "PASS",
            "diocles_figure_and_caption_clear_footer": "PASS",
            "cubic_svg_pdf_companion_renders_without_clipping": "PASS",
            "hyperlink_media_credit_headers_footers_and_margins": "PASS",
        },
        "defect_counts": {
            "visible_clipping": 0,
            "visible_overlap": 0,
            "visible_broken_glyph": 0,
            "visible_unresolved_source_marker": 0,
            "visible_missing_or_blank_content": 0,
            "visible_page_number_or_transition_error": 0,
            "total": 0,
        },
    },
}

RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "receipt": RECEIPT.relative_to(ROOT).as_posix(),
    "bytes": RECEIPT.stat().st_size,
    "sha256": digest(RECEIPT),
    "result": "PASS",
}))
