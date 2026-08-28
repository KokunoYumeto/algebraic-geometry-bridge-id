#!/usr/bin/env python3
"""Bind the completed in-app-browser responsive inspection through Unit 30."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "build" / "reader-id" / "index.html"
CSS = ROOT / "source" / "id-ID" / "reader.css"
MACHINE = ROOT / "qa" / "UNITS_01_30_MACHINE_QA.json"
OUT = ROOT / "qa" / "UNITS_01_30_RESPONSIVE_QA.json"
MODEL = "OpenAI Codex gpt-5.6-sol, Ultra."
EXPECTED = {
    HTML: (23805465, "1ca69127dbbf8aa86d8d3f238488686a145ad2dd99ee417c329a5bd9516ca677"),
    CSS: (1782, "51136e5adae36e8f2f51f834cd0fa43bf5902c3152406a05af4d4e7bbcd874cc"),
    MACHINE: (4526, "55e2044bc7423ba049adf9a1153c46c2dd957f5d147a85ee8ec1dfae3a850362"),
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def descriptor(path: Path) -> dict[str, object]:
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }


for path, expected in EXPECTED.items():
    actual = (path.stat().st_size, digest(path))
    if actual != expected:
        raise SystemExit(f"responsive input changed: {path.relative_to(ROOT)}: {actual}")

html = HTML.read_text(encoding="utf-8")
machine = json.loads(MACHINE.read_text(encoding="utf-8"))
measured = {
    "images": len(re.findall(r"<img\b", html)),
    "mathml_nodes": len(re.findall(r"<math\b", html)),
}
if measured != {"images": 101, "mathml_nodes": 11322}:
    raise SystemExit(f"unexpected responsive surface counts: {measured}")
if machine.get("status") != "PASS" or machine.get("through_unit") != 30:
    raise SystemExit("cumulative machine QA is not the Unit 30 PASS boundary")

receipt = {
    "schema": "ag-bridge-responsive-qa-v3",
    "checked_date": "2026-08-28",
    "status": "PASS",
    "through_unit": 30,
    "browser": "Codex In-app Browser",
    "served_url": "http://127.0.0.1:8765/build/reader-id/index.html",
    "artifact": {
        **descriptor(HTML),
        "title": "Kurva Aljabar - Unit 1-30",
        "language": "id-ID",
        "mathml_nodes": measured["mathml_nodes"],
        "images": measured["images"],
        "broken_images": 0,
        "images_with_empty_alt": 0,
        "browser_console_warnings_or_errors_after_final_reload": 0,
    },
    "responsive_source": {
        **descriptor(CSS),
        "display_math_overflow": "local horizontal auto-scroll",
        "long_code_and_asset_path_wrapping": "overflow-wrap:anywhere; word-break:break-word",
    },
    "machine_qa": descriptor(MACHINE),
    "desktop": {
        "viewport_width": 1440,
        "viewport_height": 1000,
        "document_client_width": 1425,
        "document_scroll_width": 1425,
        "body_width": 1224,
        "body_left": 100.44444274902344,
        "body_right": 1324.4444427490234,
        "centering_delta_px": -0.111114501953125,
        "toc_width": 972,
        "page_horizontal_overflow": False,
        "display_math_blocks": 2874,
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
        "display_math_blocks": 2874,
        "locally_scrollable_math_blocks": 181,
        "offscreen_descendants_inside_local_scrollers": 2014,
        "overflow_descendants_without_local_scroller": 0,
        "images_beyond_viewport": 0,
        "unit_30_heading_and_body_visually_legible": True,
        "visual_result": "PASS",
    },
    "topology": {
        "browser_dom_ids": 2974,
        "browser_dom_unique_ids": 2974,
        "machine_html_ids": machine["html"]["ids"],
        "internal_anchor_links": 1580,
        "missing_internal_anchor_targets": 0,
        "loaded_images": 101,
        "images_with_nonempty_alt": 101,
        "mathml_nodes": 11322,
        "unit_30_source_namespace_ids": 34,
        "unit_30_media_credit_ids": 1,
    },
    "boundary_inspection": {
        "final_build_reloaded_before_measurement": True,
        "desktop_frontmatter_reviewed": True,
        "desktop_terminal_unit_reviewed": True,
        "mobile_terminal_unit_reviewed": True,
        "unit_30_heading": "Kuliah 30: Teorema Bézout",
        "unit_30_worksheet_target_present": True,
        "unit_30_solution_target_present": True,
        "unit_30_media_credits_target_present": True,
    },
    "verification": {
        "all_images_embedded_loaded_and_have_alt_text": True,
        "desktop_body_centered_and_page_filling": True,
        "desktop_has_no_pagewide_overflow": True,
        "mobile_has_no_pagewide_overflow": True,
        "all_oversized_mobile_math_is_locally_contained": True,
        "internal_anchor_targets_complete": True,
        "fresh_browser_console_clean": True,
    },
    "conclusion": (
        "The final self-contained 30-unit reader is centered and page-filling at desktop width, "
        "reflows at phone width without document-level horizontal overflow, confines all 181 "
        "oversized mobile mathematics blocks to local scrolling, loads all 101 images with "
        "nonempty alternative text, closes all 1,580 internal anchors, and produces no browser warning or error."
    ),
    "provenance": MODEL,
}

OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"status": "PASS", "receipt": OUT.relative_to(ROOT).as_posix(),
                  "bytes": OUT.stat().st_size, "sha256": digest(OUT)}, ensure_ascii=False))
