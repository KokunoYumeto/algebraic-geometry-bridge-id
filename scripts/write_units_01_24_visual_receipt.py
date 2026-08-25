#!/usr/bin/env python3
"""Bind the completed 417-page visual inspection for Units 1-24."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-24.pdf"
MANIFEST = ROOT / "qa" / "UNITS_01_24_VISUAL_PAGE_MANIFEST.json"
MACHINE_QA = ROOT / "qa" / "UNITS_01_24_MACHINE_QA.json"
CONTACT_DIR = ROOT / "tmp" / "pdfs" / "units-01-24-contact"
RECEIPT = ROOT / "qa" / "UNITS_01_24_VISUAL_QA.json"

EXPECTED = {
    PDF: "407343d0a203e25cb6d5357907da4b6a66c6a4836c5e5fcf17b4599621d1a473",
    MANIFEST: "b68bcdad06e95f4f95d2b13926f2ac63d09a3c4b49282c5a7acd7b944ef60054",
    MACHINE_QA: "8c9e0fdf4817c6fef955007abdca4b49eb4e3dbddcc12804b04646ac1ac3dbd3",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


for path, expected_hash in EXPECTED.items():
    actual_hash = digest(path)
    if actual_hash != expected_hash:
        raise SystemExit(f"visual input changed: {path.relative_to(ROOT)} {actual_hash}")

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
machine = json.loads(MACHINE_QA.read_text(encoding="utf-8"))
if manifest.get("status") != "PASS" or manifest.get("through_unit") != 24:
    raise SystemExit("visual page manifest is not the expected PASS boundary")
if machine.get("status") != "PASS" or machine.get("through_unit") != 24:
    raise SystemExit("machine QA is not the expected PASS boundary")
render = manifest["render"]
if render["page_count"] != 417 or len(render["pages"]) != 417:
    raise SystemExit("visual page manifest does not close all 417 pages")

contacts = sorted(CONTACT_DIR.glob("pages-*.png"))
expected_names = [f"pages-{start:03d}-{min(start + 19, 417):03d}.png" for start in range(1, 418, 20)]
if [path.name for path in contacts] != expected_names:
    raise SystemExit("contact sheet inventory is not the exact 21-sheet boundary")
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
    "checked_date": "2026-08-25",
    "status": "PASS",
    "result": "PASS",
    "through_unit": 24,
    "pdf": {
        "path": PDF.relative_to(ROOT).as_posix(),
        "bytes": PDF.stat().st_size,
        "sha256": EXPECTED[PDF],
        "pages": 417,
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
            f"pages {start}-{min(start + 19, 417)}" for start in range(1, 418, 20)
        ],
        "full_size_pages_checked": [
            21, 22, 23, 24, 25, 141, 145, 146, 156, 162, 165, 166, 175,
            200, 210, 212, 228, 246, 259, 271, 277, 278, 365, 369, 372,
            373, 374, 376, 380, 382, 389, 400, 410, 411, 417,
        ],
        "checks": {
            "all_pages_populated_and_legible": "PASS",
            "consistent_margins_and_absolute_page_numbers": "PASS",
            "no_clipping_overlap_black_boxes_or_broken_glyphs": "PASS",
            "units_22_24_transitions_exercises_and_solutions_intact": "PASS",
            "four_rasterized_svg_figures_sharp_centered_and_credited": "PASS",
            "unit_24_solution_page_411_intact": "PASS",
            "media_credits_through_page_417_intact": "PASS",
            "final_page_termination_intact": "PASS",
            "intentionally_sparse_page_410_not_blank": "PASS",
        },
    },
    "review_segments": [
        {
            "pages": [1, 140],
            "contact_sheets": 7,
            "result": "PASS",
            "finding": "No blank, clipping, overlap, glyph, black-box, figure, margin, or page-number defects.",
        },
        {
            "pages": [141, 280],
            "contact_sheets": 7,
            "result": "PASS",
            "finding": "No reader-layout or mathematical-rendering defects; montage labels were correctly distinguished from page content.",
        },
        {
            "pages": [281, 417],
            "contact_sheets": 7,
            "result": "PASS",
            "finding": "Units 22-24, all four converted figures, exercises, solutions, credits, and the final boundary are clean.",
        },
    ],
    "programmatic_page_number_check": {
        "method": "pdftotext -layout on selected final PDF pages",
        "result": "Selected extracted footers equal their absolute PDF page numbers.",
    },
    "findings_resolved_before_freeze": [
        "Long Unit 22 asset-path text was made breakable before the final rebuild.",
        "The four Unit 22 SVG assets were deterministically rasterized for the PDF path while preserving semantic HTML SVGs.",
    ],
    "conclusion": (
        "All 417 final PDF pages were rasterized and reviewed through 21 contact sheets, with "
        "representative and high-risk pages additionally checked at full resolution. No unresolved "
        "visual, mathematical, media, pagination, or formatting defect remains."
    ),
    "provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
}

RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "receipt": RECEIPT.relative_to(ROOT).as_posix(),
    "bytes": RECEIPT.stat().st_size,
    "sha256": digest(RECEIPT),
    "result": "PASS",
}, ensure_ascii=False))
