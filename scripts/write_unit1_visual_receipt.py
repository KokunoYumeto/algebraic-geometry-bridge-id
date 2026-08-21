from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-unit-01.pdf"
RENDER_DIR = ROOT / "qa" / "unit-01-pdf-visual-8666aa74"
MANIFEST = RENDER_DIR / "MANIFEST.json"
RECEIPT = ROOT / "qa" / "UNIT_01_VISUAL_QA.json"
EXPECTED_PDF_SHA256 = "8666aa744b6200ff89043c801420ead551d02bcb922599238e101ec8aaf1a79f"
EXPECTED_CONTACT_SHEET_SHA256 = "3d52933ab693beb49c0ee6cfab212e4a7021dc89dc99348bcc9f56cf0d1c6bf4"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


pdf_sha256 = digest(PDF)
if pdf_sha256 != EXPECTED_PDF_SHA256:
    raise SystemExit(f"Unexpected PDF digest: {pdf_sha256}")

reader = PdfReader(str(PDF), strict=True)
if len(reader.pages) != 27:
    raise SystemExit(f"Unexpected PDF page count: {len(reader.pages)}")

pages = sorted(RENDER_DIR.glob("page-*.png"))
if [path.name for path in pages] != [f"page-{number:02d}.png" for number in range(1, 28)]:
    raise SystemExit("Render set is not the exact contiguous page-01..page-27 sequence")

contact_sheet = RENDER_DIR / "contact-sheet.png"
contact_sheet_sha256 = digest(contact_sheet)
if contact_sheet_sha256 != EXPECTED_CONTACT_SHEET_SHA256:
    raise SystemExit(f"Unexpected contact-sheet digest: {contact_sheet_sha256}")

entries = []
for path in [*pages, contact_sheet]:
    entries.append(
        {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": digest(path),
        }
    )

manifest = {
    "schema": "algebraic-geometry-bridge-render-manifest-v1",
    "pdf": {
        "path": PDF.relative_to(ROOT).as_posix(),
        "bytes": PDF.stat().st_size,
        "sha256": pdf_sha256,
        "pages": len(reader.pages),
    },
    "renders": entries,
    "render_count": len(entries),
    "render_bytes": sum(entry["bytes"] for entry in entries),
}
MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

receipt = {
    "schema": "algebraic-geometry-bridge-visual-qa-v1",
    "review_date": date.today().isoformat(),
    "pdf": manifest["pdf"],
    "render_manifest": {
        "path": MANIFEST.relative_to(ROOT).as_posix(),
        "bytes": MANIFEST.stat().st_size,
        "sha256": digest(MANIFEST),
    },
    "contact_sheet": entries[-1],
    "review": {
        "contact_sheet_reviewed_all_pages": True,
        "full_resolution_pages_reviewed": [1, 3, 14, 20, 24, 26, 27],
        "title_and_contents_checked": True,
        "image_scale_and_captions_checked": True,
        "worksheet_math_checked": True,
        "solution_math_checked": True,
        "media_credits_checked": True,
        "visible_clipping_count": 0,
        "visible_overlap_count": 0,
        "visible_broken_glyph_count": 0,
        "visible_unresolved_source_marker_count": 0,
    },
    "result": "PASS",
}
RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(json.dumps({"manifest": str(MANIFEST), "receipt": str(RECEIPT), "result": "PASS"}))
