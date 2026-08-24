#!/usr/bin/env python3
"""Create the bounded, reader-first cumulative Unit 9 release payload."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "package_unit_08_release.py"
source = TEMPLATE.read_text(encoding="utf-8")


def replace(old: str, new: str, expected: int | None = None) -> None:
    global source
    count = source.count(old)
    if expected is not None and count != expected:
        raise SystemExit(
            f"Unit 9 packaging template drift for {old!r}: expected {expected}, found {count}"
        )
    if count == 0:
        raise SystemExit(f"Unit 9 packaging template marker absent: {old!r}")
    source = source.replace(old, new)


# Identity/path changes are intentionally explicit and fail closed.
replace("Unit 8", "Unit 9", expected=1)
replace("unit-08", "unit-09")
replace("01_08", "01_09")
replace("UNIT_08", "UNIT_09")
replace("units-01-08", "units-01-09")
replace("lecture-08", "lecture-09")
replace("worksheet-08", "worksheet-09")
replace("media-credits-unit-08", "media-credits-unit-09")
replace("range(1, 9)", "range(1, 10)", expected=2)
replace('"through_unit": 8', '"through_unit": 9', expected=1)
replace('"version": "unit-08"', '"version": "unit-09"', expected=1)
replace('"pdf_pages": 161', '"pdf_pages": 174', expected=1)
replace('"exercises": 221', '"exercises": 245', expected=1)
replace('"public_source_solutions": 42', '"public_source_solutions": 45', expected=1)
replace('"reader_media_positions": 59', '"reader_media_positions": 60', expected=1)
replace('"backend_records": 5787', '"backend_records": BACKEND_RECORDS', expected=1)

# The global Unit 8 -> Unit 9 substitutions above advance the current-boundary
# paths, but the cumulative source archive must still retain the preceding Unit
# 8 authority/rights witnesses.  Restore those four entries explicitly before
# the new Unit 9 entries; otherwise a superficially valid archive would omit
# part of the cumulative component-rights chain.
for current_marker, previous_entry in (
    ('        "UNIT_09_AUTHORITY_FREEZE.md",\n', '        "UNIT_08_AUTHORITY_FREEZE.md",\n'),
    ('        "RIGHTS-unit-09.csv",\n', '        "RIGHTS-unit-08.csv",\n'),
    ('        "ASSET_CLOSURE-unit-09.json",\n', '        "ASSET_CLOSURE-unit-08.json",\n'),
    ('        "commons-imageinfo-unit-09.json",\n', '        "commons-imageinfo-unit-08.json",\n'),
):
    replace(current_marker, previous_entry + current_marker, expected=1)

# Preserve the earlier terminology evidence and include the cumulative Unit 9
# receipt emitted by the additive common-backend adapter.
replace(
    '        exact("qa/TERMINOLOGY_QA_RECEIPT.json"),\n',
    '        exact("qa/TERMINOLOGY_QA_RECEIPT.json"),\n'
    '        exact("qa/TERMINOLOGY_QA_RECEIPT_UNIT_09.json"),\n',
    expected=1,
)

# Bind the Unit 9 native count at runtime, keeping this wrapper independent of
# a guessed count while still requiring the exported manifest to agree.
replace(
    'OUT = helpers.OUT\n',
    'OUT = helpers.OUT\n'
    'BACKEND_RECORDS = __import__("json").loads((ROOT / "backend" / "units-01-09" / "MANIFEST.json").read_text(encoding="utf-8"))["record_count"]\n',
    expected=1,
)

# The source package is resumable and includes the new cumulative handoff.
replace(
    '        exact("qa/UNITS_01_09_BACKEND_QA.json"),\n',
    '        exact("qa/UNITS_01_09_BACKEND_QA.json"),\n'
    '        exact("qa/UNITS_01_09_HANDOFF.md"),\n',
    expected=2,
)

# Keep the migration receipt as a separate Zenodo file to avoid a
# self-referential source-archive hash cycle.
source = source.replace(
    '    "MIGRATION_RECEIPT.json",\n',
    '    "MIGRATION_RECEIPT.json",\n',
    1,
)

required = [
    'ROOT / "release" / "unit-09"',
    'qa/UNITS_01_09_HANDOFF.md',
    'authority/UNIT_09_AUTHORITY_FREEZE.md',
    'authority/RIGHTS-unit-09.csv',
    'backend/units-01-09',
    '"through_unit": 9',
    '"pdf_pages": 174',
    '"reader_media_positions": 60',
]
missing = [marker for marker in required if marker not in source]
if missing:
    raise SystemExit(f"Unit 9 packaging markers absent: {missing}")

exec(compile(source, str(Path(__file__).resolve()), "exec"), globals())
