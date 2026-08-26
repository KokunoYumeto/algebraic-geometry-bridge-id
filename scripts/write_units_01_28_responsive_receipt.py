#!/usr/bin/env python3
"""Bind the completed browser responsive inspection for Units 1--28."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "build" / "reader-id" / "index.html"
CSS = ROOT / "source" / "id-ID" / "reader.css"
MACHINE_QA = ROOT / "qa" / "UNITS_01_28_MACHINE_QA.json"
RECEIPT = ROOT / "qa" / "UNITS_01_28_RESPONSIVE_QA.json"

EXPECTED = {
    HTML: (23412216, "b7cef9e6c08b696bde2f875a4766e6c35e975d4fd0901e414c3896014bbd9c10"),
    CSS: (1782, "51136e5adae36e8f2f51f834cd0fa43bf5902c3152406a05af4d4e7bbcd874cc"),
    MACHINE_QA: (3083, "c666cb1186f516cead5ebd1a16de616856c99013cd94983826c974aebbdf776f"),
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


for path, expected in EXPECTED.items():
    actual = (path.stat().st_size, digest(path))
    if actual != expected:
        raise SystemExit(f"responsive input changed: {path.relative_to(ROOT)} {actual}")

html = HTML.read_text(encoding="utf-8")
machine = json.loads(MACHINE_QA.read_text(encoding="utf-8"))
measured = {
    "images": len(re.findall(r"<img\b", html)),
    "mathml_nodes": len(re.findall(r"<math\b", html)),
}
if measured != {"images": 98, "mathml_nodes": 10717}:
    raise SystemExit(f"unexpected responsive surface counts: {measured}")
if machine.get("status") != "PASS" or machine.get("through_unit") != 28:
    raise SystemExit("cumulative machine QA is not the expected PASS boundary")

receipt = {
    "schema": "ag-bridge-responsive-qa-v2",
    "checked_date": "2026-08-26",
    "status": "PASS",
    "through_unit": 28,
    "browser": "Codex In-app Browser",
    "served_url": "http://127.0.0.1:49128/index.html",
    "artifact": {
        "path": HTML.relative_to(ROOT).as_posix(),
        "bytes": EXPECTED[HTML][0],
        "sha256": EXPECTED[HTML][1],
        "title": "Kurva Aljabar - Unit 1-28",
        "language": "id-ID",
        "mathml_nodes": measured["mathml_nodes"],
        "images": measured["images"],
        "broken_images": 0,
        "images_with_empty_alt": 0,
        "browser_console_warnings_or_errors_in_fresh_tab": 0,
    },
    "responsive_source": {
        "path": CSS.relative_to(ROOT).as_posix(),
        "bytes": EXPECTED[CSS][0],
        "sha256": EXPECTED[CSS][1],
        "display_math_overflow": "local horizontal auto-scroll",
        "long_code_and_asset_path_wrapping": "overflow-wrap:anywhere; word-break:break-word",
    },
    "machine_qa": {
        "path": MACHINE_QA.relative_to(ROOT).as_posix(),
        "bytes": EXPECTED[MACHINE_QA][0],
        "sha256": EXPECTED[MACHINE_QA][1],
    },
    "desktop": {
        "viewport_width": 1440,
        "viewport_height": 1000,
        "document_client_width": 1425,
        "document_scroll_width": 1425,
        "body_width": 1224,
        "body_fill_fraction": 0.8589473684210527,
        "centering_delta_px": -0.0555572509765625,
        "page_horizontal_overflow": False,
        "display_math_blocks": 2697,
        "locally_scrollable_math_blocks": 0,
        "overflow_blocks_without_auto": 0,
        "images_beyond_viewport": 0,
        "visual_result": "PASS",
    },
    "mobile": {
        "viewport_width": 390,
        "viewport_height": 844,
        "document_client_width": 375,
        "document_scroll_width": 375,
        "body_width": 375.1111145019531,
        "page_horizontal_overflow": False,
        "display_math_blocks": 2697,
        "locally_scrollable_math_blocks": 170,
        "display_math_overflow_style": "auto",
        "overflow_blocks_without_auto": 0,
        "images_beyond_viewport": 0,
        "long_unit_28_asset_path_right_edge_px": 288.2291564941406,
        "unit_28_heading_in_view_and_legible": True,
        "visual_result": "PASS",
    },
    "topology": {
        "browser_dom_ids": 2843,
        "browser_dom_unique_ids": 2843,
        "internal_anchor_links": 1520,
        "missing_internal_anchor_targets": 0,
        "loaded_images": 98,
        "images_with_nonempty_alt": 98,
        "mathml_nodes": 10717,
        "unit_28_source_namespace_ids": 43,
        "unit_28_media_credit_ids": 1,
    },
    "unit_28_media": {
        "image_count": 4,
        "all_loaded": True,
        "all_alt_text_nonempty": True,
        "all_contained_at_mobile_width": True,
        "rendered_width_px": [263.1111145019531, 263.1041564941406, 263.1041564941406, 263.1041564941406],
        "natural_dimensions_px": [[500, 500], [900, 594], [985, 1077], [1308, 1004]],
    },
    "boundary_inspection": {
        "desktop_frontmatter_reviewed": True,
        "mobile_frontmatter_reviewed": True,
        "desktop_unit_28_reviewed": True,
        "mobile_unit_28_reviewed": True,
        "unit_28_heading": "Kuliah 28: Varietas Proyektif dan Kurva Bidang Proyektif",
        "unit_28_worksheet_target_present": True,
        "unit_28_solution_target_present": True,
        "unit_28_media_credits_target_present": True,
    },
    "verification": {
        "all_images_embedded_and_loaded": True,
        "all_image_alt_text_nonempty": True,
        "desktop_and_mobile_title_and_language_match": True,
        "desktop_body_centered": True,
        "desktop_is_page_filling": True,
        "desktop_has_no_pagewide_overflow": True,
        "mobile_has_no_pagewide_overflow": True,
        "mobile_math_overflow_is_contained": True,
        "long_code_and_asset_paths_are_contained": True,
        "internal_anchor_targets_complete": True,
        "fresh_browser_console_clean": True,
    },
    "conclusion": (
        "The cumulative self-contained reader is centered and page-filling at desktop "
        "width, reflows at phone width without document-level horizontal overflow, "
        "confines all 170 oversized mobile mathematics blocks to local scrolling, wraps "
        "long paths, loads all 98 images with nonempty alternative text, closes all 1,520 "
        "internal anchors, and produces no browser warning or error."
    ),
    "provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
}

RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({
    "receipt": RECEIPT.relative_to(ROOT).as_posix(),
    "bytes": RECEIPT.stat().st_size,
    "sha256": digest(RECEIPT),
    "result": "PASS",
}, ensure_ascii=False))
