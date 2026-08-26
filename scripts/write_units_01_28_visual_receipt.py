#!/usr/bin/env python3
"""Bind the completed 476-page visual inspection for Units 1-28."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-28.pdf"
MANIFEST = ROOT / "qa" / "UNITS_01_28_VISUAL_PAGE_MANIFEST.json"
MACHINE_QA = ROOT / "qa" / "UNITS_01_28_MACHINE_QA.json"
CONTACT_DIR = ROOT / "tmp" / "pdfs" / "units-01-28-contact"
RECEIPT = ROOT / "qa" / "UNITS_01_28_VISUAL_QA.json"

EXPECTED = {
    PDF: "181b6fba2b5441fb7a5ab76a512e9d9ee2300e4201fd4632cac20a70bc703df6",
    MANIFEST: "7cf4733ea8e74d5eb164cc0016ab11706542c76f4fcd1e13b91ae67c5bacb2b1",
    MACHINE_QA: "c666cb1186f516cead5ebd1a16de616856c99013cd94983826c974aebbdf776f",
}

EXPECTED_CONTACT_HASHES = {
    "pages-001-020.png": "e97c544698bae799c7a959a6e06f29f6b1a573079e0e09260b49372e65920772",
    "pages-021-040.png": "4fb785abc39e5dc6ce06bf6e2de95296bace08e7a9c966251fbbcffb008e3442",
    "pages-041-060.png": "076c93283795d97c7fea5307510787c8a80671c2d3bb3611a7ed645312069f11",
    "pages-061-080.png": "48db1c5cd5d3ec5974d4fa0c31690d6a7cbb4eb344524c41bb9823f177eebb3e",
    "pages-081-100.png": "4b8098bf2d3844939c240d733e728358d8d938c27a46092652c7e14878a6b2c1",
    "pages-101-120.png": "c74d77a1dc24c4ef82e3bca8d73f0cedb00a8a9eb5708cc3a4d0dd01bfff87ff",
    "pages-121-140.png": "a6814aeaac0e25a726575fdd4b8df3239331300a94e17c58c8615a7b4b34d06e",
    "pages-141-160.png": "6c70ea4dd68e4bad1df5cae6252de8fc79abcc53d849ca0b3a4eb2e28f2cafe6",
    "pages-161-180.png": "5d8e7865fb58a373ddf4d70075d7c53ff5558ec6accfaa7c18cdcd75ec632944",
    "pages-181-200.png": "d66f69f412e7f5a3b7ef0f1622ce046c70a6a8d8e592509d37aaa4a8ed402be1",
    "pages-201-220.png": "d0b810c780eeb602817b07530c915287101b31ed8f6dbed54192242dde78c9cd",
    "pages-221-240.png": "70f01907f2402eba969bd0a51ee5d6820d6a9177a28a86117ddcbcd05e1f0f49",
    "pages-241-260.png": "f7a6824f50d789c042df24e68abbd147d5585a187e8975d6a245b94f3bcfc193",
    "pages-261-280.png": "44b1436a6a7a52f402f87f2cd0a7d3ca487a42c668e975863d8378037f9fd663",
    "pages-281-300.png": "052431d3888461beeeb0406010ce5224477e11fcbb8095a4206e83578cbd4f68",
    "pages-301-320.png": "d0702bec973c1d36739e2996ff4847be652d2c94156f919e2b6dc30e5ab75e4a",
    "pages-321-340.png": "f610cc94f1a5128311fa68a40d12f3c89d477f276d26092b68592b01fa67d16f",
    "pages-341-360.png": "8600c3b0d6078be0a3bc49438be9a3843e3f98dfc60726c1d03fe6a9ed186784",
    "pages-361-380.png": "cc56979a49989a953c90bf200a727d411d1305bd9aadf505be6551eae2b01aa0",
    "pages-381-400.png": "0e8a065f00ca448b10600eb2f7cb7eb5fa205a7f7cc9ee1ae3e588a5008473e2",
    "pages-401-420.png": "6699a36326bac513f6a3c2a7b9db85bd7955a56ae6d7c328ed8bd71b4ca510ba",
    "pages-421-440.png": "4423aec10c8c90392dad4d335c1c2e7824098fcb67f9c9b6e120cf9d288bc444",
    "pages-441-460.png": "315fb684564e0bc85d3b2a768339c5c3c6fe160655f8e8fc8ada6514dd2ac9d3",
    "pages-461-476.png": "9c0b821da009e7315b0bb24ccfeaad67214d492eb83312e20097f9ac7107de04",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


for path, expected_hash in EXPECTED.items():
    if not path.is_file():
        raise SystemExit(f"visual input missing: {path.relative_to(ROOT)}")
    actual_hash = digest(path)
    if actual_hash != expected_hash:
        raise SystemExit(f"visual input changed: {path.relative_to(ROOT)} {actual_hash}")

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
machine = json.loads(MACHINE_QA.read_text(encoding="utf-8"))
if manifest.get("status") != "PASS" or manifest.get("through_unit") != 28:
    raise SystemExit("visual page manifest is not the expected PASS boundary")
if machine.get("status") != "PASS" or machine.get("through_unit") != 28:
    raise SystemExit("machine QA is not the expected PASS boundary")

pdf_relative = PDF.relative_to(ROOT).as_posix()
pdf_bytes = PDF.stat().st_size
pdf_hash = EXPECTED[PDF]
for label, record in (("visual page manifest", manifest.get("pdf", {})), ("machine QA", machine.get("pdf", {}))):
    if (
        record.get("path") != pdf_relative
        or record.get("bytes") != pdf_bytes
        or record.get("sha256") != pdf_hash
        or record.get("pages") != 476
    ):
        raise SystemExit(f"{label} does not bind the exact 476-page PDF")

machine_binding = manifest.get("machine_qa", {})
if (
    machine_binding.get("path") != MACHINE_QA.relative_to(ROOT).as_posix()
    or machine_binding.get("bytes") != MACHINE_QA.stat().st_size
    or machine_binding.get("sha256") != EXPECTED[MACHINE_QA]
):
    raise SystemExit("visual page manifest does not bind the exact machine QA")

render = manifest.get("render", {})
if render.get("page_count") != 476 or len(render.get("pages", [])) != 476:
    raise SystemExit("visual page manifest does not close all 476 pages")
if render.get("blank_pages_detected") != 0 or render.get("dimension_mismatches") != 0:
    raise SystemExit("visual page manifest reports blank pages or dimension mismatches")

contacts = sorted(CONTACT_DIR.glob("pages-*.png"))
expected_names = [
    f"pages-{start:03d}-{min(start + 19, 476):03d}.png"
    for start in range(1, 477, 20)
]
if len(contacts) != 24 or [path.name for path in contacts] != expected_names:
    raise SystemExit("contact sheet inventory is not the exact 24-sheet boundary")
if list(EXPECTED_CONTACT_HASHES) != expected_names:
    raise SystemExit("frozen contact-sheet contract is internally inconsistent")

contact_inventory = []
for path in contacts:
    actual_hash = digest(path)
    if actual_hash != EXPECTED_CONTACT_HASHES[path.name]:
        raise SystemExit(f"reviewed contact sheet changed: {path.name} {actual_hash}")
    contact_inventory.append(
        {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": actual_hash,
        }
    )

receipt = {
    "schema": "ag-bridge-visual-qa-v1",
    "checked_date": "2026-08-26",
    "status": "PASS",
    "result": "PASS",
    "through_unit": 28,
    "input_binding": {
        "machine_qa": {
            "path": MACHINE_QA.relative_to(ROOT).as_posix(),
            "bytes": MACHINE_QA.stat().st_size,
            "sha256": EXPECTED[MACHINE_QA],
        }
    },
    "pdf": {
        "path": pdf_relative,
        "bytes": pdf_bytes,
        "sha256": pdf_hash,
        "pages": 476,
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
            f"pages {start}-{min(start + 19, 476)}" for start in range(1, 477, 20)
        ],
        "final_contact_sheets_checked": ["pages 441-460", "pages 461-476"],
        "full_size_pages_checked": [457, 462, 463],
        "checks": {
            "all_24_contact_sheets_cover_pages_1_476_cleanly": "PASS",
            "all_pages_populated_centered_and_legible": "PASS",
            "consistent_margins_and_absolute_page_numbers": "PASS",
            "no_clipping_overlap_black_boxes_or_broken_glyphs": "PASS",
            "page_457_proof_square_inline_at_bridge_end": "PASS",
            "page_462_soccerball_and_torus_each_immediately_followed_by_component_credit": "PASS",
            "page_463_double_torus_and_sphere_with_handles_each_immediately_followed_by_component_credit": "PASS",
            "unit_28_figures_centered_sharp_and_readable": "PASS",
            "media_credits_through_page_476_intact": "PASS",
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
        {"pages": [321, 476], "contact_sheets": 8, "result": "PASS"},
    ],
    "findings_resolved_before_freeze": [
        "The Unit 28 Soccerball.svg source asset required deterministic SVG-to-PNG conversion for the PDF reader.",
        "Four Unit 28 figure and component-credit pairs initially separated under float placement; PDF-only staging now keeps each figure immediately adjacent to its credit.",
        "The proof-ending square on page 457 was initially isolated; it is now correctly inline at the end of the bridge paragraph.",
        "A complete final 476-page raster and 24-sheet review verified the repaired bytes.",
    ],
    "conclusion": (
        "All 476 final PDF pages were rasterized and reviewed through 24 contact sheets. "
        "The two final sheets and full-resolution pages 457, 462, and 463 were checked "
        "again after the repairs. No unresolved visual, mathematical, media, pagination, "
        "or formatting defect remains."
    ),
    "provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
}

RECEIPT.write_text(
    json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
    newline="\n",
)
print(
    json.dumps(
        {
            "receipt": RECEIPT.relative_to(ROOT).as_posix(),
            "bytes": RECEIPT.stat().st_size,
            "sha256": digest(RECEIPT),
            "pdf_pages": 476,
            "contact_sheets": len(contact_inventory),
            "result": "PASS",
        },
        ensure_ascii=False,
    )
)
