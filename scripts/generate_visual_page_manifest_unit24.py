#!/usr/bin/env python3
"""Bind every Units 1--24 PDF raster page to a replayable QA manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RENDER_DIR = ROOT / "tmp" / "pdfs" / "units-01-24-pages"
OUTPUT = ROOT / "qa" / "UNITS_01_24_VISUAL_PAGE_MANIFEST.json"
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-24.pdf"
MACHINE = ROOT / "qa" / "UNITS_01_24_MACHINE_QA.json"
BASELINE = ROOT / "qa" / "UNITS_01_21_VISUAL_PAGE_MANIFEST.json"
BASELINE_FACT = (119494, "bc8d6ba08961db685d9b9d33cd8899f050b483722c7a523940f6f150e7a7e211")
EXPECTED_DIMENSIONS = (745, 1053)
INK_THRESHOLD = 248


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def file_fact(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular file: {path}")
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def main() -> int:
    baseline = file_fact(BASELINE)
    require((baseline["bytes"], baseline["sha256"]) == BASELINE_FACT, "Unit 21 visual-page baseline drift")
    baseline_payload = json.loads(BASELINE.read_text(encoding="utf-8"))
    require(baseline_payload.get("status") == "PASS", "Unit 21 visual-page baseline did not pass")
    require(baseline_payload.get("pdf", {}).get("pages") == 367, "Unit 21 visual-page count drift")

    machine = json.loads(MACHINE.read_text(encoding="utf-8"))
    require(machine.get("status") == "PASS" and machine.get("through_unit") == 24, "Units 1--24 machine QA mismatch")
    pdf_witness = machine.get("pdf", {})
    expected_pdf = (pdf_witness.get("bytes"), pdf_witness.get("sha256"))
    require(PDF.is_file() and not PDF.is_symlink(), "Units 1--24 PDF missing/nonregular")
    require((PDF.stat().st_size, sha256(PDF)) == expected_pdf, "PDF/machine-QA identity mismatch")
    expected_pages = pdf_witness.get("pages")
    require(isinstance(expected_pages, int) and expected_pages > 367, "Units 1--24 PDF did not advance beyond Unit 21")

    pages = sorted(RENDER_DIR.glob("page-*.png"))
    require(len(pages) == expected_pages, f"expected {expected_pages} page rasters, found {len(pages)}")
    rows: list[dict[str, Any]] = []
    for number, path in enumerate(pages, start=1):
        require(path.name == f"page-{number:03d}.png", f"non-contiguous page raster at {path.name}")
        require(path.is_file() and not path.is_symlink(), f"page raster missing/nonregular: {path.name}")
        with Image.open(path) as image:
            width, height = image.size
            require((width, height) == EXPECTED_DIMENSIONS, f"unexpected dimensions for {path.name}: {(width, height)}")
            histogram = image.convert("L").histogram()
        ink_pixels = sum(histogram[:INK_THRESHOLD])
        ink_fraction = ink_pixels / (width * height)
        require(ink_fraction > 0, f"blank page raster: {path.name}")
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
        "through_unit": 24,
        "baseline_unit_21": baseline,
        "machine_qa": file_fact(MACHINE),
        "pdf": {
            "path": PDF.relative_to(ROOT).as_posix(),
            "bytes": PDF.stat().st_size,
            "sha256": expected_pdf[1],
            "pages": expected_pages,
        },
        "render": {
            "renderer": "pdftoppm",
            "resolution_dpi": 90,
            "page_count": len(rows),
            "total_bytes": sum(row["bytes"] for row in rows),
            "dimensions_px": list(EXPECTED_DIMENSIONS),
            "visible_ink_threshold_gray_lt": INK_THRESHOLD,
            "minimum_visible_ink_fraction": min(row["visible_ink_fraction_gray_lt_248"] for row in rows),
            "minimum_visible_ink_page": min(rows, key=lambda row: row["visible_ink_fraction_gray_lt_248"])["page"],
            "maximum_visible_ink_fraction": max(row["visible_ink_fraction_gray_lt_248"] for row in rows),
            "maximum_visible_ink_page": max(rows, key=lambda row: row["visible_ink_fraction_gray_lt_248"])["page"],
            "blank_pages_detected": 0,
            "dimension_mismatches": 0,
            "pages": rows,
        },
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
