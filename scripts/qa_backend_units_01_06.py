#!/usr/bin/env python3
"""Fail-closed replay and closure QA for the cumulative Units 1--6 backend."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "qa_backend_units_01_05.py"
source = TEMPLATE.read_text(encoding="utf-8")


def replace_exact(old: str, new: str, *, expected: int | None = None) -> None:
    global source
    count = source.count(old)
    if expected is not None and count != expected:
        raise SystemExit(f"Backend-QA template drift for {old!r}: expected {expected}, found {count}")
    if count == 0:
        raise SystemExit(f"Backend-QA template marker absent: {old!r}")
    source = source.replace(old, new)


# Preserve Unit 5 as the byte-identical baseline while advancing the output.
replace_exact("units-01-04", "__UNIT6_BASELINE_PATH__")
replace_exact("Units 1--4", "__UNIT6_BASELINE_LABEL__")
replace_exact("units-01-05", "units-01-06")
replace_exact("Units 1--5", "Units 1--6")
replace_exact("__UNIT6_BASELINE_PATH__", "units-01-05")
replace_exact("__UNIT6_BASELINE_LABEL__", "Units 1--5")
replace_exact(
    'BASELINE_RECORDS_SHA256 = "65434f1f6503d90569f39e2faa43d6d7bdcc752ea0a21e7ddae2d36c9d68c059"',
    'BASELINE_RECORDS_SHA256 = "6fd038ef29dd5fc7c7fdbf956e4e20d53e35f851feb16459f05c634ce240cb0d"',
    expected=1,
)
replace_exact("BASELINE_RECORD_COUNT = 2775", "BASELINE_RECORD_COUNT = 3471", expected=1)
replace_exact("units_01_04", "units_01_05")
replace_exact("units0104", "units0105", expected=1)

for old, new in (
    ("UNIT5", "UNIT6"),
    ("UNIT_05", "UNIT_06"),
    ("unit5", "unit6"),
    ("unit_05", "unit_06"),
    ("unit_5", "unit_6"),
    ("Unit 5", "Unit 6"),
    ("unit-05", "unit-06"),
    ("lecture-05", "lecture-06"),
    ("worksheet-05", "worksheet-06"),
    ("w05", "w06"),
    ("0105", "0106"),
    ("01_05", "01_06"),
):
    replace_exact(old, new)

# This receipt key reports the preserved Unit 5 baseline.
replace_exact("units_01_06_record_bytes_preserved", "units_01_05_record_bytes_preserved")
replace_exact("units0106_byte_preservation", "units0105_byte_preservation")

replace_exact('manifest["through_unit"] == 5', 'manifest["through_unit"] == 6', expected=1)
replace_exact('build_receipt["through_unit"] == 5', 'build_receipt["through_unit"] == 6', expected=1)
replace_exact('authority_manifest["unit_number"] == 5', 'authority_manifest["unit_number"] == 6', expected=1)
replace_exact('"through_unit": 5', '"through_unit": 6', expected=1)
replace_exact('len(exercises) == 27', 'len(exercises) == 30', expected=1)
replace_exact('len(solutions) == 4', 'len(solutions) == 9', expected=1)
replace_exact(
    'source_solution_numbers == mapped_numbers == [3, 15, 19, 20]',
    'source_solution_numbers == mapped_numbers == [3, 4, 8, 9, 17, 18, 21, 22, 25]',
    expected=1,
)
replace_exact('len(class_ids["exercise"]) == 134', 'len(class_ids["exercise"]) == 164', expected=1)
replace_exact('len(class_ids["solution"]) == 28', 'len(class_ids["solution"]) == 37', expected=1)
replace_exact('len(class_ids["asset"]) == 41', 'len(class_ids["asset"]) == 44', expected=1)
replace_exact(
    'len(class_ids["concept"]) == 42 and len(class_ids["term"]) == 42',
    'len(class_ids["concept"]) == 50 and len(class_ids["term"]) == 50',
    expected=1,
)
replace_exact('len(correction_rows) == 16', 'len(correction_rows) == 21', expected=1)
replace_exact('len(class_ids["correction"]) == 16', 'len(class_ids["correction"]) == 21', expected=1)
replace_exact("does not contain sixteen rows", "does not contain twenty-one rows", expected=1)
replace_exact('"unit_06_additions": 7', '"unit_06_additions": 5', expected=1)
replace_exact('"sixteen_row_correction_ledger_hash_closure"', '"twenty_one_row_correction_ledger_hash_closure"', expected=1)

term_block = '''NEW_TERM_BINDINGS = {
    "AGT-0043": ("concept.polynomial-parametrization", "parametrisasi polinomial"),
    "AGT-0044": ("concept.rational-parametrization", "parametrisasi rasional"),
    "AGT-0045": ("concept.rational-curve", "kurva rasional"),
    "AGT-0046": ("concept.homogenization", "homogenisasi"),
    "AGT-0047": ("concept.dehomogenization", "dehomogenisasi"),
    "AGT-0048": ("concept.differentiable-curve", "kurva terdiferensial"),
    "AGT-0049": ("concept.domain-of-definition", "domain definisi"),
    "AGT-0050": ("concept.implicit-function-theorem", "teorema fungsi implisit"),
}

'''
source, count = re.subn(r"NEW_TERM_BINDINGS = \{\n.*?\n\}\n\n", term_block, source, count=1, flags=re.DOTALL)
if count != 1:
    raise SystemExit("Backend-QA terminology block drift")

required_markers = [
    'EXPORTER = ROOT / "scripts" / "export_backend_units_01_06.py"',
    'BACKEND = ROOT / "backend" / "units-01-06"',
    'BASELINE = ROOT / "backend" / "units-01-05"',
    'CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-06.2026-08-22"',
    'ROOT / "source" / "id-ID" / "worksheet-06.md"',
    'qa/UNITS_01_06_MACHINE_QA.json',
    '"qa/UNIT_06_PROTECTED_SURFACES.json"',
]
missing = [marker for marker in required_markers if marker not in source]
if missing:
    raise SystemExit(f"Transformed backend-QA markers absent: {missing}")

exec(compile(source, str(Path(__file__).resolve()), "exec"), globals())
