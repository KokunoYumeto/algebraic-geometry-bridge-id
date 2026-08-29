#!/usr/bin/env python3
"""Bind the completed all-page visual review for the final BGK Units 1--6 reader."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "build" / "reader-bgk-id" / "bundel-berkas-dan-kohomologi-id-units-01-06.pdf"
RENDER = ROOT / "tmp" / "pdfs" / "bgk-units-01-06-20260829"
RESPONSIVE = ROOT / "qa" / "BGK_UNITS_01_06_RESPONSIVE_QA.json"
MACHINE = ROOT / "qa" / "BGK_UNITS_01_06_READER_QA.json"
OUT = ROOT / "qa" / "BGK_UNITS_01_06_VISUAL_QA.json"
PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."

EXPECTED = {
    PDF: (896_202, "f89a622f15acab90f683fb2a0b72a150363fc71d0f41f971c48b8c8ee43c2c9b"),
    RESPONSIVE: (16_164, "755494a526f1d23e81ec797859a12dd9fb6bcea639b5dc53fada4136d7a5b0f0"),
    MACHINE: (6_369, "8c40f147451888e3ab4c2da95d164388c4f5725d37e121f020842da9488e250c"),
}
CONTACT_RANGES = ((1, 20), (21, 40), (41, 60), (61, 80), (81, 82))
FULL_SIZE_REVIEWED = (5, 6, 76, 77, 81, 82)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fact(path: Path) -> dict[str, object]:
    require(path.is_file() and not path.is_symlink(), f"missing regular file: {path}")
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def require_expected(path: Path) -> dict[str, object]:
    observed = fact(path)
    expected_bytes, expected_hash = EXPECTED[path]
    require(observed["bytes"] == expected_bytes, f"byte drift: {path}")
    require(observed["sha256"] == expected_hash, f"hash drift: {path}")
    return observed


def main() -> int:
    pdf = require_expected(PDF)
    responsive = require_expected(RESPONSIVE)
    machine = require_expected(MACHINE)
    require(len(PdfReader(str(PDF)).pages) == 82, "PDF page count drifted")

    page_rows: list[dict[str, object]] = []
    for number in range(1, 83):
        path = RENDER / f"page-{number:02d}.png"
        row = fact(path)
        with Image.open(path) as image:
            require(image.size == (910, 1287), f"raster dimensions drifted on page {number}")
            gray = image.convert("L")
            histogram = gray.histogram()
            visible_fraction = sum(histogram[:248]) / (gray.width * gray.height)
        require(visible_fraction > 0.001, f"apparently blank page: {number}")
        row.update({
            "page": number,
            "width_px": 910,
            "height_px": 1287,
            "visible_ink_fraction_gray_lt_248": round(visible_fraction, 8),
        })
        page_rows.append(row)

    contact_rows: list[dict[str, object]] = []
    covered: list[int] = []
    for start, end in CONTACT_RANGES:
        path = RENDER / f"contact-{start:02d}-{end:02d}.png"
        row = fact(path)
        row.update({"pages": [start, end]})
        contact_rows.append(row)
        covered.extend(range(start, end + 1))
    require(covered == list(range(1, 83)), "contact-sheet coverage is not exact")

    result = {
        "schema": "ag-bridge-bgk-visual-qa-v1",
        "through_unit": 6,
        "status": "PASS",
        "model_provenance": PROVENANCE,
        "pdf": {
            **pdf,
            "pages_rendered": 82,
            "pages_visually_reviewed": 82,
            "unintended_blank_pages": 0,
            "clipping_overlap_bad_glyph_or_broken_equation_observed": False,
            "paper": "A4",
            "render_dpi": 110,
            "page_pixel_dimensions": {"width": 910, "height": 1287},
        },
        "bound_machine_qa": machine,
        "bound_responsive_qa": responsive,
        "page_rasters": page_rows,
        "contact_sheets": contact_rows,
        "review": {
            "contact_sheets_reviewed_in_full": [f"pages {start}-{end}" for start, end in CONTACT_RANGES],
            "full_size_pages_reviewed": list(FULL_SIZE_REVIEWED),
            "frontmatter_scope_correction_pages_rechecked": [5, 6],
            "unit_06_terminology_correction_page_rechecked": 76,
            "final_unit_06_formula_and_source_note_pages_rechecked": [77, 81, 82],
            "checks": {
                "all_pages_present_and_legible": "PASS",
                "page_sequence_and_transitions": "PASS",
                "headings_paragraphs_math_and_notes_not_clipped": "PASS",
                "figures_and_captions_visible": "PASS",
                "no_overlap_or_broken_glyphs": "PASS",
                "corrected_three_solution_and_ninety_eight_negative_scope_visible": "PASS",
                "corrected_functor_spelling_visible": "PASS",
                "desktop_centering_mobile_reflow_and_local_math_scroll": "PASS",
            },
        },
        "defect_counts": {
            "visible_clipping": 0,
            "visible_overlap": 0,
            "visible_broken_glyph": 0,
            "visible_broken_equation": 0,
            "unintended_blank_page": 0,
            "document_level_mobile_overflow": 0,
            "total": 0,
        },
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"receipt": fact(OUT), "pages": len(page_rows), "contacts": len(contact_rows)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
