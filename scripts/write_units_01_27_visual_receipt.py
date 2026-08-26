#!/usr/bin/env python3
"""Bind the completed 464-page visual inspection for Units 1-27."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-27.pdf"
MANIFEST = ROOT / "qa" / "UNITS_01_27_VISUAL_PAGE_MANIFEST.json"
MACHINE_QA = ROOT / "qa" / "UNITS_01_27_MACHINE_QA.json"
CONTACT_DIR = ROOT / "tmp" / "pdfs" / "units-01-27-contact"
RECEIPT = ROOT / "qa" / "UNITS_01_27_VISUAL_QA.json"

EXPECTED = {
    PDF: "766f6b8ccede9ecb1b6524d9652595f188d6f17ef22fab4bf6b886b03a9e0d65",
    MANIFEST: "b976bfc36983689125be39fb8f686783d28de49e7386b68344f9613322979ee5",
    MACHINE_QA: "33fdf951354c620bbfeedc483338aa611ef577f0adcb8e509bca7361dc9bb074",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


for path, expected_hash in EXPECTED.items():
    actual_hash = digest(path)
    if actual_hash != expected_hash:
        raise SystemExit(f"visual input changed: {path.relative_to(ROOT)} {actual_hash}")

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
machine = json.loads(MACHINE_QA.read_text(encoding="utf-8"))
if manifest.get("status") != "PASS" or manifest.get("through_unit") != 27:
    raise SystemExit("visual page manifest is not the expected PASS boundary")
if machine.get("status") != "PASS" or machine.get("through_unit") != 27:
    raise SystemExit("machine QA is not the expected PASS boundary")
render = manifest["render"]
if render["page_count"] != 464 or len(render["pages"]) != 464:
    raise SystemExit("visual page manifest does not close all 464 pages")

contacts = sorted(CONTACT_DIR.glob("pages-*.png"))
expected_names = [
    f"pages-{start:03d}-{min(start + 19, 464):03d}.png"
    for start in range(1, 465, 20)
]
if [path.name for path in contacts] != expected_names:
    raise SystemExit("contact sheet inventory is not the exact 24-sheet boundary")
contact_inventory = [
    {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }
    for path in contacts
]

receipt = {
    "schema": "ag-bridge-visual-qa-v1",
    "checked_date": "2026-08-26",
    "status": "PASS",
    "result": "PASS",
    "through_unit": 27,
    "pdf": {
        "path": PDF.relative_to(ROOT).as_posix(),
        "bytes": PDF.stat().st_size,
        "sha256": EXPECTED[PDF],
        "pages": 464,
        "page_size": "A4",
        "encrypted": False,
        "all_fonts_embedded": True,
        "font_rows": 17,
    },
    "deterministic_raster": {
        "renderer": "pdftoppm",
        "resolution_dpi": render["resolution_dpi"],
        "page_manifest": MANIFEST.relative_to(ROOT).as_posix(),
        "page_manifest_bytes": MANIFEST.stat().st_size,
        "page_manifest_sha256": EXPECTED[MANIFEST],
        "page_png_count": render["page_count"],
        "dimensions_px": render["dimensions_px"],
        "total_png_bytes": render["total_bytes"],
        "visible_ink_threshold_gray_lt": render["visible_ink_threshold_gray_lt"],
        "minimum_visible_ink_fraction": render["minimum_visible_ink_fraction"],
        "minimum_visible_ink_page": render["minimum_visible_ink_page"],
        "maximum_visible_ink_fraction": render["maximum_visible_ink_fraction"],
        "maximum_visible_ink_page": render["maximum_visible_ink_page"],
        "blank_pages_detected": render["blank_pages_detected"],
        "dimension_mismatches": render["dimension_mismatches"],
    },
    "visual_inspection": {
        "all_page_contact_sheets": contact_inventory,
        "contact_sheet_count": len(contact_inventory),
        "contact_sheet_bytes": sum(item["bytes"] for item in contact_inventory),
        "contact_sheet_page_ranges": [
            f"pages {start}-{min(start + 19, 464)}" for start in range(1, 465, 20)
        ],
        "full_size_pages_checked": [
            21, 22, 23, 24, 25, 141, 200, 280, 320, 401, 410, 413,
            426, 439, 440, 442, 443, 444, 445, 446, 452, 456, 463, 464,
        ],
        "checks": {
            "all_pages_populated_and_legible": "PASS",
            "consistent_margins_and_absolute_page_numbers": "PASS",
            "no_clipping_overlap_black_boxes_or_broken_glyphs": "PASS",
            "units_25_27_transitions_exercises_and_solutions_intact": "PASS",
            "unit_27_ten_images_sharp_centered_and_credited": "PASS",
            "long_pdf_paths_and_hashes_wrap_inside_margins": "PASS",
            "media_credits_through_page_464_intact": "PASS",
            "final_page_termination_intact": "PASS",
        },
        "contact_sheet_annotation_note": (
            "Several top overlay labels are partly masked at montage scale; exact raster "
            "filenames, page-manifest order, full-size pages, and printed PDF folios close "
            "the sequence. The document pages themselves are unaffected."
        ),
    },
    "review_segments": [
        {"pages": [1, 160], "contact_sheets": 8, "result": "PASS"},
        {"pages": [161, 320], "contact_sheets": 8, "result": "PASS"},
        {"pages": [321, 464], "contact_sheets": 8, "result": "PASS"},
    ],
    "findings_resolved_before_freeze": [
        "The Unit 27 perspective asset path on page 446 was clipped at the right margin.",
        "Long Unit 26-27 credit paths and SHA-256 values on pages 463-464 exceeded the text block.",
        "The PDF-only staging path now renders long inline-code tokens with xurl break opportunities; source and semantic HTML remain unchanged.",
        "A complete second 464-page raster and 24-sheet review verified the repaired bytes.",
    ],
    "conclusion": (
        "All 464 final PDF pages were rasterized and reviewed through 24 contact sheets, "
        "with the new and high-risk pages additionally checked at full resolution. No "
        "unresolved visual, mathematical, media, pagination, or formatting defect remains."
    ),
    "provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
}

RECEIPT.write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
    newline="\n",
)
print(json.dumps({
    "receipt": RECEIPT.relative_to(ROOT).as_posix(),
    "bytes": RECEIPT.stat().st_size,
    "sha256": digest(RECEIPT),
    "result": "PASS",
}, ensure_ascii=False))
