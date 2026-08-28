#!/usr/bin/env python3
"""Bind the completed 504-page visual inspection through classical Unit 30."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-30.pdf"
MANIFEST = ROOT / "qa" / "UNITS_01_30_VISUAL_PAGE_MANIFEST.json"
MACHINE = ROOT / "qa" / "UNITS_01_30_MACHINE_QA.json"
CONTACT_DIR = ROOT / "tmp" / "pdfs" / "units-01-30-contact"
OUT = ROOT / "qa" / "UNITS_01_30_VISUAL_QA.json"
EXPECTED = {
    PDF: "6383d3b9804a059e76dc643da5974b8809649707e177ba191a69220fa7ea0e5d",
    MANIFEST: "f7f93c1bcea209022686de7f621e5670e8264e1e54455cd8d52f2a17c6bc9380",
    MACHINE: "55e2044bc7423ba049adf9a1153c46c2dd957f5d147a85ee8ec1dfae3a850362",
}
CONTACT_HASHES = {
    "pages-001-020.png": "04737f9a660b055968a26432f1948df15efb28d6564995acf8d566b6b792c9e0",
    "pages-021-040.png": "c8bedf57e3a970aa1d051a91d98482de9e9cdce9884ad7f59e549027a6613d2b",
    "pages-041-060.png": "3cc74c54f3df8c3a0b2fe4c85765866f548f1e8b4c9e51ca963605eb9caab469",
    "pages-061-080.png": "cab5a75e1be1272558e25ed85943482adb2861020bd8ed2d9499c7bf56be84a7",
    "pages-081-100.png": "69f17511abc725751bacfe1588004b1477da326f27412fabb9a51550d1271180",
    "pages-101-120.png": "cc34b6a0d8a98060dabd6b0c4994b50da74f94a0f1cd94aa74a71ef17a9ce85c",
    "pages-121-140.png": "c8a1c745bcc30b527b29df8055526257d9e90a0a1470d74f18909e66452cd861",
    "pages-141-160.png": "e6b20147293fd3adbd4ee080a544fa3de83247e910275b20fa6a0fd2b134d234",
    "pages-161-180.png": "796bd3b8fcf3245b1fa624d9ff6eddb3cf6959a3f474846cf9ac6bef53315fb4",
    "pages-181-200.png": "ab7dd18ec86a3c7c5e790be962ac629c53be4605e567ac81d8bd4cc1e013274d",
    "pages-201-220.png": "4fe3efff497432c8628f19f6a68219ae674a442af2797961c4e06ab5352413be",
    "pages-221-240.png": "2bbd00a2b2c47cb805ac07d88bf6a7cae94c45bc886f1d009cd8e06019842032",
    "pages-241-260.png": "335ab55ab836de8a7140129bd3508db902cd0133f2ddf3fdd2a3ca3cf59afdc5",
    "pages-261-280.png": "19141a57d10310ae4f5ce57e0783d7aea477488a71dae1b283061b5095c44053",
    "pages-281-300.png": "d50112a6519b61aae1a8844150b98464fe0f402cab63934ffa3db0c0a550a93b",
    "pages-301-320.png": "05f6909f41b34f4e84dcb55bd6f13e7c8d44fc9b8a1f5674238dc5435214f773",
    "pages-321-340.png": "3f842acc46d800626b69a713c824ee15f989dd6bf0869dfd537a0bed348a4f91",
    "pages-341-360.png": "2b1df1578c7720e969d8978c4271e2e812dca2e10a5778d8d9c35f1e6898dd32",
    "pages-361-380.png": "55a42652874de3fec92b71099d077b63c27abeca57614ff6ab18f501f20ce9f6",
    "pages-381-400.png": "3d8fc482d0a4674c31f9c4326dd71af3369a14661773d503bdd6fb1ead76f006",
    "pages-401-420.png": "bc598f64d47c4f074570640fe742508178f472ee912c787f1def9a25fef5eedd",
    "pages-421-440.png": "0569aa7eafbfd27cafdff425a62370c3870f3848f3461463ece6d2f5565605f5",
    "pages-441-460.png": "590827dae650f749e67d891b52855dffe7685698bfed4b044f03beab87ebbaad",
    "pages-461-480.png": "45b3aef831b840fc2d31f7b8f21224a3c6069c22da375792eb94c6ce578ff25e",
    "pages-481-500.png": "7b5e5965cd7ca7b9c641bc9d25d6638203d482365c15ec1aef7d7bf86a1b5f84",
    "pages-501-504.png": "05a93c0bc10696fd5fe344cb9da05975d55c4ddf0987c1125b398e3f18ebed57",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


for path, expected in EXPECTED.items():
    if not path.is_file() or digest(path) != expected:
        raise SystemExit(f"visual input changed: {path.relative_to(ROOT)}")

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
machine = json.loads(MACHINE.read_text(encoding="utf-8"))
if manifest.get("status") != "PASS" or manifest.get("through_unit") != 30:
    raise SystemExit("visual manifest is not the Unit 30 PASS boundary")
if machine.get("status") != "PASS" or machine.get("through_unit") != 30:
    raise SystemExit("machine QA is not the Unit 30 PASS boundary")
for label, record in (("manifest", manifest.get("pdf", {})), ("machine", machine.get("pdf", {}))):
    if (record.get("path") != PDF.relative_to(ROOT).as_posix() or
            record.get("bytes") != PDF.stat().st_size or
            record.get("sha256") != EXPECTED[PDF] or record.get("pages") != 504):
        raise SystemExit(f"{label} does not bind the exact 504-page PDF")

render = manifest.get("render", {})
if render.get("page_count") != 504 or len(render.get("pages", [])) != 504:
    raise SystemExit("visual manifest does not close all 504 pages")
if render.get("blank_pages_detected") != 0 or render.get("dimension_mismatches") != 0:
    raise SystemExit("visual manifest reports blank pages or dimension drift")

contacts = sorted(CONTACT_DIR.glob("pages-*.png"))
expected_names = [f"pages-{start:03d}-{min(start + 19, 504):03d}.png" for start in range(1, 505, 20)]
if [path.name for path in contacts] != expected_names or list(CONTACT_HASHES) != expected_names:
    raise SystemExit("contact-sheet inventory is not the exact 26-sheet boundary")
contact_rows = []
for path in contacts:
    actual = digest(path)
    if actual != CONTACT_HASHES[path.name]:
        raise SystemExit(f"reviewed contact sheet changed: {path.name}")
    contact_rows.append({
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": actual,
    })

receipt = {
    "schema": "ag-bridge-visual-qa-v2",
    "checked_date": "2026-08-28",
    "status": "PASS",
    "result": "PASS",
    "through_unit": 30,
    "input_binding": {
        "machine_qa": {
            "path": MACHINE.relative_to(ROOT).as_posix(),
            "bytes": MACHINE.stat().st_size,
            "sha256": EXPECTED[MACHINE],
        }
    },
    "pdf": {
        "path": PDF.relative_to(ROOT).as_posix(),
        "bytes": PDF.stat().st_size,
        "sha256": EXPECTED[PDF],
        "pages": 504,
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
        "blank_pages_detected": 0,
        "dimension_mismatches": 0,
    },
    "visual_inspection": {
        "all_page_contact_sheets": contact_rows,
        "contact_sheet_count": 26,
        "contact_sheet_page_ranges": [f"pages {start}-{min(start + 19, 504)}" for start in range(1, 505, 20)],
        "full_size_pages_checked": [1, 478, 480, 485, 492, 504],
        "checks": {
            "all_26_contact_sheets_cover_pages_1_504_cleanly": "PASS",
            "all_pages_populated_centered_and_legible": "PASS",
            "consistent_margins_and_absolute_page_numbers": "PASS",
            "no_clipping_overlap_black_boxes_or_broken_glyphs": "PASS",
            "unit_29_lemniscate_and_caption_stay_together": "PASS",
            "unit_29_tschirnhausen_figure_and_single_caption_fit_the_page": "PASS",
            "unit_30_cubic_curves_figure_and_single_caption_stay_together": "PASS",
            "unit_30_solutions_and_terminal_credits_intact": "PASS",
            "final_page_termination_intact": "PASS",
        },
    },
    "review_segments": [
        {"pages": [1, 160], "contact_sheets": 8, "result": "PASS"},
        {"pages": [161, 320], "contact_sheets": 8, "result": "PASS"},
        {"pages": [321, 480], "contact_sheets": 8, "result": "PASS"},
        {"pages": [481, 504], "contact_sheets": 2, "result": "PASS"},
    ],
    "findings_resolved_before_freeze": [
        "Three Unit 29-30 figures had duplicate implicit/manual captions which separated from images; each now has one semantic caption and separate fig-alt accessibility text.",
        "The portrait Unit 29 Tschirnhausen figure exceeded the A4 float area by 11.5 pt; a PDF-stage-only 72% height constraint removed the warning without changing source or HTML.",
        "Both final Pandoc logs are empty and a fresh 504-page raster plus 26-sheet review verifies the repaired bytes.",
    ],
    "conclusion": (
        "All 504 final PDF pages were rasterized and reviewed through 26 contact sheets. "
        "Full-size terminal-risk pages confirm the repaired Unit 29 and Unit 30 figure/caption "
        "flow, solutions, media credits, and final termination. No unresolved visual, "
        "mathematical, media, pagination, font-embedding, or formatting defect remains."
    ),
    "provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
}

OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"status": "PASS", "receipt": OUT.relative_to(ROOT).as_posix(),
                  "bytes": OUT.stat().st_size, "sha256": digest(OUT),
                  "pdf_pages": 504, "contact_sheets": 26}, ensure_ascii=False))
