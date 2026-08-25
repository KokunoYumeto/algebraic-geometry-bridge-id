#!/usr/bin/env python3
"""Bind the completed in-app-browser responsive inspection for Units 1-24."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "build" / "reader-id" / "index.html"
CSS = ROOT / "source" / "id-ID" / "reader.css"
MACHINE_QA = ROOT / "qa" / "UNITS_01_24_MACHINE_QA.json"
RECEIPT = ROOT / "qa" / "UNITS_01_24_RESPONSIVE_QA.json"

EXPECTED = {
    HTML: "3753f3a8dc15d8aa1916ecd461b555c3b854139e216cef18d92e6c699258d61f",
    CSS: "51136e5adae36e8f2f51f834cd0fa43bf5902c3152406a05af4d4e7bbcd874cc",
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
        raise SystemExit(f"responsive input changed: {path.relative_to(ROOT)} {actual_hash}")

html = HTML.read_text(encoding="utf-8")
machine = json.loads(MACHINE_QA.read_text(encoding="utf-8"))
measured = {
    "images": len(re.findall(r"<img\b", html)),
    "mathml_nodes": len(re.findall(r"<math\b", html)),
}
if measured != {"images": 83, "mathml_nodes": 9514}:
    raise SystemExit(f"unexpected responsive surface counts: {measured}")
if machine.get("status") != "PASS" or machine.get("through_unit") != 24:
    raise SystemExit("cumulative machine QA is not the expected PASS boundary")

receipt = {
    "schema": "ag-bridge-responsive-qa-v1",
    "checked_date": "2026-08-25",
    "status": "PASS",
    "through_unit": 24,
    "browser": "Codex In-app Browser",
    "served_url": "http://127.0.0.1:49123/index.html",
    "artifact": {
        "path": HTML.relative_to(ROOT).as_posix(),
        "bytes": HTML.stat().st_size,
        "sha256": EXPECTED[HTML],
        "title": "Kurva Aljabar - Unit 1-24",
        "language": "id-ID",
        "mathml_nodes": measured["mathml_nodes"],
        "images": measured["images"],
        "broken_images": 0,
        "images_with_empty_alt": 0,
        "browser_console_warnings_or_errors_in_fresh_tab": 0,
    },
    "responsive_source": {
        "path": CSS.relative_to(ROOT).as_posix(),
        "bytes": CSS.stat().st_size,
        "sha256": EXPECTED[CSS],
        "display_math_overflow": "local horizontal auto-scroll",
        "long_code_and_asset_path_wrapping": "overflow-wrap:anywhere; word-break:break-word",
    },
    "machine_qa": {
        "path": MACHINE_QA.relative_to(ROOT).as_posix(),
        "bytes": MACHINE_QA.stat().st_size,
        "sha256": EXPECTED[MACHINE_QA],
    },
    "desktop": {
        "viewport_width": 1440,
        "viewport_height": 1000,
        "document_client_width": 1425,
        "document_scroll_width": 1425,
        "body_width": 1224,
        "body_fill_fraction": 0.858947,
        "centering_delta_px": 0.0556,
        "page_horizontal_overflow": False,
        "locally_scrollable_math_blocks": 0,
        "images_beyond_viewport": 0,
        "visual_result": "PASS",
    },
    "mobile": {
        "viewport_width": 390,
        "viewport_height": 844,
        "document_client_width": 375,
        "document_scroll_width": 375,
        "page_horizontal_overflow": False,
        "display_math_blocks": 2353,
        "locally_scrollable_math_blocks": 153,
        "display_math_overflow_style": "auto",
        "overflow_blocks_without_auto": 0,
        "images_beyond_viewport": 0,
        "long_unit_24_asset_path_right_edge_px": 353.5,
        "unit_24_heading_in_view_and_legible": True,
        "visual_result": "PASS",
    },
    "topology": {
        "browser_dom_ids": 2555,
        "browser_dom_unique_ids": 2555,
        "internal_anchor_links": 1380,
        "missing_internal_anchor_targets": 0,
        "loaded_images": 83,
        "images_with_nonempty_alt": 83,
        "mathml_nodes": 9514,
        "unit_24_ids": 35,
    },
    "boundary_inspection": {
        "desktop_frontmatter_reviewed": True,
        "mobile_frontmatter_reviewed": True,
        "desktop_unit_24_reviewed": True,
        "mobile_unit_24_reviewed": True,
        "unit_24_heading": "Kuliah 24: Garis Singgung dan Gelanggang Deret Pangkat Formal",
        "unit_24_worksheet_target_present": True,
        "unit_24_public_solutions_target_present": True,
        "unit_24_media_credits_target_present": True,
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
        "The cumulative self-contained reader is centered and page-filling at desktop width, "
        "reflows at phone width without document-level horizontal overflow, confines oversized "
        "mathematics to local auto-scrolling blocks, wraps long code and asset paths, loads all "
        "83 embedded images with nonempty alternative text, closes all 1380 internal anchors, "
        "and produces no browser warning or error in a fresh test tab."
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
