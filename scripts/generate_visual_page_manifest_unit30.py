#!/usr/bin/env python3
"""Bind every page raster of the complete 30-unit classical reader."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RENDER_DIR = ROOT / "tmp" / "pdfs" / "units-01-30-pages"
OUTPUT = ROOT / "qa" / "UNITS_01_30_VISUAL_PAGE_MANIFEST.json"
PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-30.pdf"
MACHINE = ROOT / "qa" / "UNITS_01_30_MACHINE_QA.json"
BASELINE = ROOT / "qa" / "UNITS_01_28_VISUAL_PAGE_MANIFEST.json"
BASELINE_FACT = (155125, "7cf4733ea8e74d5eb164cc0016ab11706542c76f4fcd1e13b91ae67c5bacb2b1")
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
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular: {path}")
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def main() -> int:
    baseline = file_fact(BASELINE)
    require((baseline["bytes"], baseline["sha256"]) == BASELINE_FACT,
            "Unit 28 visual-page baseline drift")
    baseline_payload = json.loads(BASELINE.read_text(encoding="utf-8"))
    require(baseline_payload.get("status") == "PASS" and
            baseline_payload.get("pdf", {}).get("pages") == 476,
            "Unit 28 visual-page baseline status/scope")

    machine = json.loads(MACHINE.read_text(encoding="utf-8"))
    require(machine.get("status") == "PASS" and machine.get("through_unit") == 30,
            "Units 1--30 machine QA mismatch")
    pdf_witness = machine.get("pdf", {})
    require((PDF.stat().st_size, sha256(PDF)) ==
            (pdf_witness.get("bytes"), pdf_witness.get("sha256")),
            "PDF/machine-QA identity mismatch")
    expected_pages = pdf_witness.get("pages")
    require(expected_pages == 504, "complete classical PDF page count")

    pages = sorted(RENDER_DIR.glob("page-*.png"))
    require(len(pages) == expected_pages, f"expected {expected_pages} rasters, found {len(pages)}")
    rows: list[dict[str, Any]] = []
    for number, path in enumerate(pages, start=1):
        require(path.name == f"page-{number:03d}.png", f"non-contiguous raster: {path.name}")
        require(path.is_file() and not path.is_symlink(), f"missing/nonregular raster: {path.name}")
        with Image.open(path) as image:
            width, height = image.size
            require((width, height) == EXPECTED_DIMENSIONS,
                    f"unexpected dimensions: {path.name}: {(width, height)}")
            histogram = image.convert("L").histogram()
        ink_pixels = sum(histogram[:INK_THRESHOLD])
        ink_fraction = ink_pixels / (width * height)
        require(ink_fraction > 0, f"blank raster: {path.name}")
        rows.append({
            "page": number,
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "width_px": width,
            "height_px": height,
            "visible_ink_fraction_gray_lt_248": ink_fraction,
        })

    payload = {
        "schema": "ag-bridge-visual-page-manifest-v2",
        "status": "PASS",
        "through_unit": 30,
        "baseline_unit_28": baseline,
        "machine_qa": file_fact(MACHINE),
        "pdf": {
            "path": PDF.relative_to(ROOT).as_posix(),
            "bytes": PDF.stat().st_size,
            "sha256": pdf_witness["sha256"],
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
        "provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "receipt": OUTPUT.relative_to(ROOT).as_posix(),
                      "bytes": OUTPUT.stat().st_size, "sha256": sha256(OUTPUT),
                      "pages": len(rows), "total_png_bytes": payload["render"]["total_bytes"]},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
