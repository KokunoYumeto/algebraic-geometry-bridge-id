#!/usr/bin/env python3
"""Bind every final Unit 12 QA raster page to a replayable manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RENDER_DIR = ROOT / "tmp" / "pdfs" / "unit-12-release-render"
OUTPUT = ROOT / "qa" / "UNITS_01_12_VISUAL_PAGE_MANIFEST.json"
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-12.pdf"
EXPECTED_PDF_SHA256 = "3213bee4e472c11c480bb2241077ffad4fb62d95ac590f3448a6fbd188c9159d"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    pages = sorted(RENDER_DIR.glob("page-*.png"))
    if len(pages) != 215:
        raise RuntimeError(f"expected 215 page rasters, found {len(pages)}")
    if sha256(PDF) != EXPECTED_PDF_SHA256:
        raise RuntimeError("final PDF identity changed")

    rows = []
    for number, path in enumerate(pages, start=1):
        if path.name != f"page-{number:03d}.png":
            raise RuntimeError(f"non-contiguous page raster at {path.name}")
        with Image.open(path) as image:
            width, height = image.size
        if (width, height) != (794, 1123):
            raise RuntimeError(f"unexpected dimensions for {path.name}: {(width, height)}")
        rows.append(
            {
                "page": number,
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "width_px": width,
                "height_px": height,
            }
        )

    payload = {
        "schema": "ag-bridge-visual-page-manifest-v1",
        "status": "PASS",
        "pdf": {
            "path": PDF.relative_to(ROOT).as_posix(),
            "bytes": PDF.stat().st_size,
            "sha256": EXPECTED_PDF_SHA256,
            "pages": 215,
        },
        "render": {
            "renderer": "pdftoppm",
            "resolution_dpi": 96,
            "page_count": len(rows),
            "total_bytes": sum(row["bytes"] for row in rows),
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
