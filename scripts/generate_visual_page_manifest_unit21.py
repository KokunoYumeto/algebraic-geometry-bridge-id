#!/usr/bin/env python3
"""Bind all final Units 1-21 PDF raster pages to a replayable QA manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RENDER_DIR = ROOT / "tmp" / "pdfs" / "units-01-21-pages"
OUTPUT = ROOT / "qa" / "UNITS_01_21_VISUAL_PAGE_MANIFEST.json"
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-21.pdf"
EXPECTED_PDF_SHA256 = "b95fd1ed0ea75294cd4562b7f2f36e920e247e2da5e1b039e99e975f9797a3e6"
EXPECTED_PAGES = 367
EXPECTED_DIMENSIONS = (745, 1053)
INK_THRESHOLD = 248


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    pages = sorted(RENDER_DIR.glob("page-*.png"))
    if len(pages) != EXPECTED_PAGES:
        raise RuntimeError(f"expected {EXPECTED_PAGES} page rasters, found {len(pages)}")
    if sha256(PDF) != EXPECTED_PDF_SHA256:
        raise RuntimeError("final PDF identity changed")

    rows = []
    for number, path in enumerate(pages, start=1):
        if path.name != f"page-{number:03d}.png":
            raise RuntimeError(f"non-contiguous page raster at {path.name}")
        with Image.open(path) as image:
            width, height = image.size
            if (width, height) != EXPECTED_DIMENSIONS:
                raise RuntimeError(f"unexpected dimensions for {path.name}: {(width, height)}")
            histogram = image.convert("L").histogram()
        ink_pixels = sum(histogram[:INK_THRESHOLD])
        ink_fraction = ink_pixels / (width * height)
        if ink_fraction <= 0:
            raise RuntimeError(f"blank page raster: {path.name}")
        rows.append(
            {
                "page": number,
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "width_px": width,
                "height_px": height,
                "visible_ink_fraction_gray_lt_248": ink_fraction,
            }
        )

    payload = {
        "schema": "ag-bridge-visual-page-manifest-v1",
        "status": "PASS",
        "pdf": {
            "path": PDF.relative_to(ROOT).as_posix(),
            "bytes": PDF.stat().st_size,
            "sha256": EXPECTED_PDF_SHA256,
            "pages": EXPECTED_PAGES,
        },
        "render": {
            "renderer": "pdftoppm",
            "resolution_dpi": 90,
            "page_count": len(rows),
            "total_bytes": sum(row["bytes"] for row in rows),
            "dimensions_px": list(EXPECTED_DIMENSIONS),
            "visible_ink_threshold_gray_lt": INK_THRESHOLD,
            "minimum_visible_ink_fraction": min(
                row["visible_ink_fraction_gray_lt_248"] for row in rows
            ),
            "minimum_visible_ink_page": min(
                rows, key=lambda row: row["visible_ink_fraction_gray_lt_248"]
            )["page"],
            "maximum_visible_ink_fraction": max(
                row["visible_ink_fraction_gray_lt_248"] for row in rows
            ),
            "maximum_visible_ink_page": max(
                rows, key=lambda row: row["visible_ink_fraction_gray_lt_248"]
            )["page"],
            "blank_pages_detected": 0,
            "dimension_mismatches": 0,
            "pages": rows,
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
