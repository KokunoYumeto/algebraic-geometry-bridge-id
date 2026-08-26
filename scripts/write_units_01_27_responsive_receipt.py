#!/usr/bin/env python3
"""Bind the completed in-app-browser responsive inspection for Units 1-27."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "build" / "reader-id" / "index.html"
CSS = ROOT / "source" / "id-ID" / "reader.css"
MACHINE_QA = ROOT / "qa" / "UNITS_01_27_MACHINE_QA.json"
RECEIPT = ROOT / "qa" / "UNITS_01_27_RESPONSIVE_QA.json"

EXPECTED = {
    HTML: "8edd2fc31c30e7e5454f31cf18b6f3f117e1a7108766c839a33cf896cdd24b66",
    CSS: "51136e5adae36e8f2f51f834cd0fa43bf5902c3152406a05af4d4e7bbcd874cc",
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
        raise SystemExit(f"responsive input changed: {path.relative_to(ROOT)} {actual_hash}")

html = HTML.read_text(encoding="utf-8")
machine = json.loads(MACHINE_QA.read_text(encoding="utf-8"))
measured = {
    "images": len(re.findall(r"<img\b", html)),
    "mathml_nodes": len(re.findall(r"<math\b", html)),
}
if measured != {"images": 94, "mathml_nodes": 10426}:
    raise SystemExit(f"unexpected responsive surface counts: {measured}")
if machine.get("status") != "PASS" or machine.get("through_unit") != 27:
    raise SystemExit("cumulative machine QA is not the expected PASS boundary")

receipt = {
    "schema": "ag-bridge-responsive-qa-v1",
    "checked_date": "2026-08-26",
    "status": "PASS",
    "through_unit": 27,
    "browser": "Codex In-app Browser",
    "served_url": "http://127.0.0.1:49127/index.html",
    "artifact": {
        "path": HTML.relative_to(ROOT).as_posix(),
        "bytes": HTML.stat().st_size,
        "sha256": EXPECTED[HTML],
        "title": "Kurva Aljabar - Unit 1-27",
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
        "body_fill_fraction": 0.8589473684210527,
        "centering_delta_px": -0.0555572509765625,
        "page_horizontal_overflow": False,
        "display_math_blocks": 2640,
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
        "display_math_blocks": 2640,
        "locally_scrollable_math_blocks": 170,
        "display_math_overflow_style": "auto",
        "overflow_blocks_without_auto": 0,
        "images_beyond_viewport": 0,
        "long_unit_27_asset_path_right_edge_px": 353.5,
        "unit_27_heading_in_view_and_legible": True,
        "visual_result": "PASS",
    },
    "topology": {
        "browser_dom_ids": 2759,
        "browser_dom_unique_ids": 2759,
        "internal_anchor_links": 1480,
        "missing_internal_anchor_targets": 0,
        "loaded_images": 94,
        "images_with_nonempty_alt": 94,
        "mathml_nodes": 10426,
        "unit_27_source_namespace_ids": 38,
        "unit_27_media_credit_ids": 1,
    },
    "boundary_inspection": {
        "desktop_frontmatter_reviewed": True,
        "mobile_frontmatter_reviewed": True,
        "desktop_unit_27_reviewed": True,
        "mobile_unit_27_reviewed": True,
        "unit_27_heading": "Kuliah 27: Ruang Proyektif",
        "unit_27_worksheet_target_present": True,
        "unit_27_zero_solution_closure_target_present": True,
        "unit_27_media_credits_target_present": True,
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
        "confines oversized mathematics to local auto-scrolling blocks, wraps long code "
        "and asset paths, loads all 94 embedded images with nonempty alternative text, "
        "closes all 1480 internal anchors, and produces no browser warning or error."
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
