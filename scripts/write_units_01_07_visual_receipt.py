#!/usr/bin/env python3
"""Write the replayable all-page and Unit 7 visual-QA receipt."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "write_units_01_06_visual_receipt.py"
source = TEMPLATE.read_text(encoding="utf-8")


def replace_exact(old: str, new: str, *, expected: int | None = None) -> None:
    global source
    count = source.count(old)
    if expected is not None and count != expected:
        raise SystemExit(f"Visual-QA template drift for {old!r}: expected {expected}, found {count}")
    if count == 0:
        raise SystemExit(f"Visual-QA template marker absent: {old!r}")
    source = source.replace(old, new)


for old, new in (
    ("units-01-06", "units-01-07"),
    ("unit-06", "unit-07"),
    ("UNITS_01_06", "UNITS_01_07"),
    ("Unit 6", "Unit 7"),
    ("unit_06", "unit_07"),
):
    replace_exact(old, new)

replace_exact(
    'EXPECTED_PDF_SHA256 = "27b459e5277c2baddcf849978d0ef720ed72bda60cd4c360b8d53ae765b9462e"',
    'EXPECTED_PDF_SHA256 = "729d1b4f5593d2695091fd72379df9df69cc3dccb3e6ca404fce705d3d834f56"',
    expected=1,
)
replace_exact("EXPECTED_PAGE_COUNT = 117", "EXPECTED_PAGE_COUNT = 142", expected=1)

contacts_block = '''EXPECTED_CONTACTS = {
    "contact-01.png": "a3b780ea827ac4f62fbb7304808a6be7114418baf8f9b76c0ab26bb2c0cd95f2",
    "contact-02.png": "cfb81123080eca6388176bfb30393845d650ca10947d98655ee56b1bd8ec226a",
    "contact-03.png": "41a3a2746a69dd5dfa3618de40bebd7cf3e8f6205b7339d4471128dc7e3ee761",
    "contact-04.png": "f182412d2faa8808ed11aa58dfea1beaf66e244d2483a3ade940ad978b305fe0",
    "contact-05.png": "1f685dcf2fcd3cdfe1e73b335b8f3f85886a041f2d6f4bdab6a85e1782d4efea",
    "contact-06.png": "301f132ba41624b46396432ff7afda3ca335748157dcc5f3878543c5dd062c34",
    "unit-07-contact.png": "dd767075a094f050e35979522ee5b611d482a9bd071b6d5ba1638b7a24011743",
}
'''
source, count = re.subn(
    r"EXPECTED_CONTACTS = \{\n.*?\n\}\n",
    contacts_block,
    source,
    count=1,
    flags=re.DOTALL,
)
if count != 1:
    raise SystemExit("Visual-QA contact block drift")

replace_exact("page-001..page-117", "page-001..page-142", expected=1)
replace_exact("range(95, 118)", "range(116, 143)")
replace_exact('"through_unit": 6', '"through_unit": 7', expected=1)
replace_exact('"contact_sheets_reviewed_all_117_pages": True', '"contact_sheets_reviewed_all_142_pages": True', expected=1)
replace_exact('"reviewed_full_size_pages": [95, 98, 103, 104, 109, 117]', '"reviewed_full_size_pages": [116, 117, 118, 124, 128, 129, 130, 137, 142]', expected=1)
replace_exact(
    '"unit_07_lecture_worksheet_solution_and_credit_transitions": "PASS"',
    '"unit_07_lecture_worksheet_solution_and_credit_transitions": "PASS"',
    expected=1,
)
replace_exact(
    '"diocles_figure_and_caption_clear_footer": "PASS",\n            "cubic_svg_pdf_companion_renders_without_clipping": "PASS",',
    '"unit_07_portrait_and_caption_clear_footer": "PASS",\n            "conic_svg_pdf_companion_renders_without_clipping": "PASS",\n            "three_orbit_first_frame_pdf_companions_render": "PASS",',
    expected=1,
)

required_markers = [
    'algebraic-geometry-bridge-id-units-01-07.pdf',
    'EXPECTED_PAGE_COUNT = 142',
    'range(116, 143)',
    '"through_unit": 7',
    '"contact_sheets_reviewed_all_142_pages": True',
]
missing = [marker for marker in required_markers if marker not in source]
if missing:
    raise SystemExit(f"Transformed visual-QA markers absent: {missing}")

exec(compile(source, str(Path(__file__).resolve()), "exec"), globals())
