#!/usr/bin/env python3
"""Record the bounded in-app-browser desktop/mobile responsive gate for Unit 9."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "build" / "reader-id" / "index.html"
CSS = ROOT / "source" / "id-ID" / "reader.css"
RECEIPT = ROOT / "qa" / "UNITS_01_09_RESPONSIVE_QA.json"
EXPECTED_HTML_SHA256 = "19f5612e4f5b102c61cfc63d6a51ea47062af6a66a22261cc4eef0af904ae777"
EXPECTED_CSS_SHA256 = "3242ba1d6d1ebb6abf4a321377fcdef3e67a02c7dbc986b502f2363719f76efa"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


if digest(HTML) != EXPECTED_HTML_SHA256 or digest(CSS) != EXPECTED_CSS_SHA256:
    raise SystemExit("Unit 9 responsive inputs changed after browser measurement")
html = HTML.read_text(encoding="utf-8")
image_count = len(re.findall(r"<img\b", html))
mathml_count = len(re.findall(r"<math\b", html))
if (image_count, mathml_count) != (60, 3262):
    raise SystemExit(f"unexpected Unit 9 HTML surface counts: images={image_count}, mathml={mathml_count}")

receipt = {
    "schema": "ag-bridge-responsive-html-qa-v3",
    "audited_utc": datetime.now(timezone.utc).isoformat(),
    "status": "PASS",
    "through_unit": 9,
    "browser_surface": "Codex In-app Browser",
    "artifact": {
        "path": HTML.relative_to(ROOT).as_posix(),
        "bytes": HTML.stat().st_size,
        "sha256": EXPECTED_HTML_SHA256,
        "title": "Kurva Aljabar - Unit 1-9",
        "language": "id-ID",
        "mathml_nodes": mathml_count,
        "images": image_count,
        "broken_images": 0,
        "browser_console_warnings_or_errors": 0,
    },
    "responsive_source": {
        "path": CSS.relative_to(ROOT).as_posix(),
        "bytes": CSS.stat().st_size,
        "sha256": EXPECTED_CSS_SHA256,
        "display_math_overflow": "local horizontal auto-scroll",
        "long_link_wrapping": "anywhere",
    },
    "desktop": {
        "viewport_css_pixels": {"width": 1440, "height": 1000},
        "document_client_width": 1425,
        "document_scroll_width": 1425,
        "body_left": 100.44444274902344,
        "body_right": 1324.4444427490234,
        "body_width": 1224,
        "page_horizontal_overflow": False,
        "centered_reader": True,
        "rendered_elements_outside_viewport": 0,
        "visual_result": "PASS",
    },
    "mobile": {
        "viewport_css_pixels": {"width": 390, "height": 844},
        "document_client_width": 375,
        "document_scroll_width": 375,
        "body_left": 0,
        "body_right": 375.1111145019531,
        "body_width": 375.1111145019531,
        "page_horizontal_overflow": False,
        "images_over_content": 0,
        "display_math_blocks": 889,
        "display_math_overflow_blocks": 73,
        "overflow_blocks_without_auto": 0,
        "visual_result": "PASS",
    },
    "verification": {
        "all_images_local_and_loaded": True,
        "all_image_alt_text_nonempty": True,
        "desktop_and_mobile_title_and_language_match": True,
        "desktop_body_centered": True,
        "mobile_math_overflow_is_contained": True,
        "local_server": "http://127.0.0.1:8879/build/reader-id/index.html",
        "desktop_screenshot_reviewed": True,
        "mobile_screenshot_reviewed": True,
    },
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"receipt": RECEIPT.relative_to(ROOT).as_posix(), "bytes": RECEIPT.stat().st_size, "sha256": digest(RECEIPT), "result": "PASS"}, ensure_ascii=False))
