#!/usr/bin/env python3
"""Bind every Units 1--27 PDF raster page to a replayable QA manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "generate_visual_page_manifest_unit24.py"
TEMPLATE_SHA256 = "be8f0d388bc50007da8e10973ce513eb704debb97c4c857cc5e060f40d11b4f7"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Unit 27 visual-manifest specialization expected one occurrence, found {count}: {old!r}")
    return text.replace(old, new, 1)


if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
    raise SystemExit("Accepted Unit 24 visual-manifest template is absent or has drifted")

generated = TEMPLATE.read_text(encoding="utf-8")
for old, new in (
    ('RENDER_DIR = ROOT / "tmp" / "pdfs" / "units-01-24-pages"', 'RENDER_DIR = ROOT / "tmp" / "pdfs" / "units-01-27-pages"'),
    ('OUTPUT = ROOT / "qa" / "UNITS_01_24_VISUAL_PAGE_MANIFEST.json"', 'OUTPUT = ROOT / "qa" / "UNITS_01_27_VISUAL_PAGE_MANIFEST.json"'),
    ('PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-24.pdf"', 'PDF = ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-27.pdf"'),
    ('MACHINE = ROOT / "qa" / "UNITS_01_24_MACHINE_QA.json"', 'MACHINE = ROOT / "qa" / "UNITS_01_27_MACHINE_QA.json"'),
    ('BASELINE = ROOT / "qa" / "UNITS_01_21_VISUAL_PAGE_MANIFEST.json"', 'BASELINE = ROOT / "qa" / "UNITS_01_24_VISUAL_PAGE_MANIFEST.json"'),
    ('BASELINE_FACT = (119494, "bc8d6ba08961db685d9b9d33cd8899f050b483722c7a523940f6f150e7a7e211")', 'BASELINE_FACT = (136053, "b68bcdad06e95f4f95d2b13926f2ac63d09a3c4b49282c5a7acd7b944ef60054")'),
):
    generated = replace_once(generated, old, new)

generated = generated.replace("Unit 21 visual-page", "Unit 24 visual-page")
generated = generated.replace('get("pdf", {}).get("pages") == 367', 'get("pdf", {}).get("pages") == 417')
generated = generated.replace("Unit 21 visual-page count drift", "Unit 24 visual-page count drift")
generated = generated.replace('machine.get("through_unit") == 24', 'machine.get("through_unit") == 27')
generated = generated.replace("Units 1--24", "Units 1--27")
generated = generated.replace('expected_pages > 367', 'expected_pages > 417')
generated = generated.replace('"through_unit": 24', '"through_unit": 27')
generated = generated.replace('"baseline_unit_21": baseline', '"baseline_unit_24": baseline')

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
