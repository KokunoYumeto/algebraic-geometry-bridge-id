#!/usr/bin/env python3
"""Create bounded contact sheets for visual review of all Units 1--28 pages."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "make_unit24_contact_sheets.py"
TEMPLATE_SHA256 = "99019cfaa26e01e5343c9c4c8a139753f64562dfacef83e6b18f56610bdf5c64"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Unit 28 contact-sheet specialization expected one occurrence, found {count}: {old!r}")
    return text.replace(old, new, 1)


if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
    raise SystemExit("Accepted Unit 24 contact-sheet template is absent or has drifted")

generated = TEMPLATE.read_text(encoding="utf-8")
for old, new in (
    ('RENDER_DIR = ROOT / "tmp" / "pdfs" / "units-01-24-pages"', 'RENDER_DIR = ROOT / "tmp" / "pdfs" / "units-01-28-pages"'),
    ('OUTPUT_DIR = ROOT / "tmp" / "pdfs" / "units-01-24-contact"', 'OUTPUT_DIR = ROOT / "tmp" / "pdfs" / "units-01-28-contact"'),
    ('EXPECTED_PAGES = 417', 'EXPECTED_PAGES = 476'),
    ('page-001..page-417', 'page-001..page-476'),
):
    generated = replace_once(generated, old, new)
generated = generated.replace("Units 1--24", "Units 1--28")

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
