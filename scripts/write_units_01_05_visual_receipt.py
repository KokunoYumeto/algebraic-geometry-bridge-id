from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-05.pdf"
RENDER_DIR = ROOT / "tmp" / "pdfs" / "units-01-05-final"
RECEIPT = ROOT / "qa" / "UNITS_01_05_VISUAL_QA.json"

EXPECTED_PDF_SHA256 = "17a5bad9fa92db95593f5c16f1a9aa59c989714848f53b22304b6addc50b9b44"
EXPECTED_PAGE_COUNT = 96
EXPECTED_PIXEL_SIZE = (827, 1170)
EXPECTED_CONTACTS = {
    "contact-01-12.png": "e5512be3441f8db390ff3580e7b07acdcbefed8c5af6dfa02c388bc05059a073",
    "contact-13-24.png": "8b5991d260e866f928269ca53703971e6987877e021265bb5563dc2109097130",
    "contact-25-36.png": "db4d5b3d47d510045a775359da37a63d39be526be9f332abffbccdb8d83ac5be",
    "contact-37-48.png": "156154d2da4758f15708a537a2e34e8539ff91b71c5dcf53e580e975eb6c4356",
    "contact-49-60.png": "2864af72e7b238040a08e1066bb0d60bdbbacf4f8a5d608aa3b5ff57ac29a87d",
    "contact-61-72.png": "1abf9299b93b2eec07bf7282eb7574a840cbf973f82a255f2ee674a158382d97",
    "contact-73-84.png": "81a7840c239651795aa6fcc8decf63c186ff703808209b446a5a9d3dc79d176e",
    "contact-85-96.png": "5061777787a2441f68db6405d759da3c6e718034c3c11247923c5f5f433ce9a4",
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

expected_names = [f"page-{number:02d}.png" for number in range(1, EXPECTED_PAGE_COUNT + 1)]
pages = sorted(RENDER_DIR.glob("page-*.png"))
if [path.name for path in pages] != expected_names:
    raise SystemExit("Render set is not the exact contiguous page-01..page-96 sequence")

contacts = []
for name, expected_sha256 in EXPECTED_CONTACTS.items():
    path = RENDER_DIR / name
    if digest(path) != expected_sha256:
        raise SystemExit(f"Contact-sheet SHA-256 mismatch: {name}")
    contacts.append(
        {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": expected_sha256,
            "pages": name.removeprefix("contact-").removesuffix(".png"),
        }
    )

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
    "through_unit": 5,
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
        "dpi": 100,
        "page_pixel_dimensions": {"width": EXPECTED_PIXEL_SIZE[0], "height": EXPECTED_PIXEL_SIZE[1]},
        "contact_sheets": contacts,
        "pages": page_entries,
    },
    "review": {
        "contact_sheets_reviewed_all_pages": True,
        "reviewed_full_size_pages": [49, 64, 67, 68, 86, 89, 90, 92, 93, 94],
        "checks": {
            "page_sequence_numbering_and_unit_transitions": "PASS",
            "unit_05_lecture_worksheet_solution_and_credit_transitions": "PASS",
            "dense_math_layout_and_legibility": "PASS",
            "figures_scale_alignment_and_captions": "PASS",
            "source_star_markers_visible_in_headings": "PASS",
            "tall_hydrant_float_scaled_inside_A4_body": "PASS",
            "mathml_compatible_fraction_unchanged_in_pdf": "PASS",
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
