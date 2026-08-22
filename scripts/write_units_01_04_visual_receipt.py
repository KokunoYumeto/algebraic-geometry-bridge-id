from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-04.pdf"
RENDER_DIR = ROOT / "tmp" / "pdfs" / "units-01-04-7b6b824c"
CONTACT_SHEET = RENDER_DIR / "contact-sheet.png"
UNIT4_CONTACT_SHEET = RENDER_DIR / "unit-04-contact-sheet.png"
RECEIPT = ROOT / "qa" / "UNITS_01_04_VISUAL_QA.json"

EXPECTED_PDF_SHA256 = "7b6b824cbd9deb575b321554ca274e40500ed6f6f0d228cec8ef005e70108e37"
EXPECTED_CONTACT_SHEET_SHA256 = "8d9fc35256779c680ddf9f73b2f4df20e2ffbf6c8ab2fa323c1759ad5f15c71f"
EXPECTED_UNIT4_CONTACT_SHEET_SHA256 = "6034b930631f2198738d5a0614fb147e6f737fbc8fd2ffb6c149fcdaa7b8d7f9"
EXPECTED_PAGE_COUNT = 80
EXPECTED_PIXEL_SIZE = (910, 1287)


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

expected_names = [f"page-{number:02d}.png" for number in range(1, EXPECTED_PAGE_COUNT + 1)]
pages = sorted(RENDER_DIR.glob("page-*.png"))
if [path.name for path in pages] != expected_names:
    raise SystemExit("Render set is not the exact contiguous page-01..page-80 sequence")

if digest(CONTACT_SHEET) != EXPECTED_CONTACT_SHEET_SHA256:
    raise SystemExit("Contact-sheet SHA-256 does not match the reviewed sheet")
if digest(UNIT4_CONTACT_SHEET) != EXPECTED_UNIT4_CONTACT_SHEET_SHA256:
    raise SystemExit("Unit 4 contact-sheet SHA-256 does not match the reviewed sheet")

page_entries = []
for number, path in enumerate(pages, start=1):
    with Image.open(path) as image:
        if image.size != EXPECTED_PIXEL_SIZE:
            raise SystemExit(f"Unexpected pixel dimensions for {path.name}: {image.size}")
    page_entries.append(
        {
            "page": number,
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": digest(path),
        }
    )

first_page = reader.pages[0]
width = round(float(first_page.mediabox.width), 3)
height = round(float(first_page.mediabox.height), 3)
if (round(width, 2), round(height, 2)) != (595.28, 841.89):
    raise SystemExit(f"Unexpected first-page dimensions: {width} x {height} pt")

receipt = {
    "schema": "algebraic-geometry-bridge-visual-qa-v1",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "through_unit": 4,
    "pdf": {
        "path": PDF.relative_to(ROOT).as_posix(),
        "bytes": PDF.stat().st_size,
        "sha256": pdf_sha256,
        "pages": len(reader.pages),
        "page_size": f"A4 ({width} x {height} pt)",
        "pdf_version": reader.pdf_header.removeprefix("%PDF-"),
    },
    "render": {
        "directory": RENDER_DIR.relative_to(ROOT).as_posix(),
        "dpi": 110,
        "page_pixel_dimensions": {
            "width": EXPECTED_PIXEL_SIZE[0],
            "height": EXPECTED_PIXEL_SIZE[1],
        },
        "contact_sheet": {
            "path": CONTACT_SHEET.relative_to(ROOT).as_posix(),
            "bytes": CONTACT_SHEET.stat().st_size,
            "sha256": digest(CONTACT_SHEET),
        },
        "pages": page_entries,
        "unit_04_contact_sheet": {
            "path": UNIT4_CONTACT_SHEET.relative_to(ROOT).as_posix(),
            "bytes": UNIT4_CONTACT_SHEET.stat().st_size,
            "sha256": digest(UNIT4_CONTACT_SHEET),
            "pages": "60-80",
        },
    },
    "review": {
        "contact_sheet_reviewed_all_pages": True,
        "reviewed_full_size_pages": [60, 63, 66, 68, 70, 71, 74, 76, 78, 80],
        "checks": {
            "page_sequence_and_numbering": "PASS",
            "unit_3_to_unit_4_transition": "PASS",
            "unit_4_lecture_and_worksheet_transitions": "PASS",
            "unit_4_solution_and_media_credit_transitions": "PASS",
            "dense_math_layout_and_legibility": "PASS",
            "figures_scale_alignment_and_captions": "PASS",
            "worksheet_definitions_hint_stars_and_points": "PASS",
            "hyperlink_and_media_credit_layout": "PASS",
            "headers_footers_centering_and_margins": "PASS",
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
    "result": "PASS",
}

RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(
    json.dumps(
        {
            "receipt": RECEIPT.relative_to(ROOT).as_posix(),
            "bytes": RECEIPT.stat().st_size,
            "sha256": digest(RECEIPT),
            "result": "PASS",
        }
    )
)
