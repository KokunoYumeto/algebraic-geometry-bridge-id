#!/usr/bin/env python3
"""Export the deterministic cumulative backend through reader Units 1--6.

The Unit 5 exporter is the audited structural template. This wrapper performs
an explicit, fail-closed specialization against the frozen 3,471-record Unit 5
backend so those canonical record bytes remain unchanged.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "export_backend_units_01_05.py"
source = TEMPLATE.read_text(encoding="utf-8")


def replace_exact(old: str, new: str, *, expected: int | None = None) -> None:
    global source
    count = source.count(old)
    if expected is not None and count != expected:
        raise SystemExit(f"Exporter template drift for {old!r}: expected {expected}, found {count}")
    if count == 0:
        raise SystemExit(f"Exporter template marker absent: {old!r}")
    source = source.replace(old, new)


# Protect the intended Unit 5 baseline while advancing cumulative paths.
replace_exact("units-01-04", "__UNIT6_BASELINE_PATH__")
replace_exact("Units 1--4", "__UNIT6_BASELINE_LABEL__")
replace_exact("units-01-05", "units-01-06")
replace_exact("Units 1--5", "Units 1--6")
replace_exact("__UNIT6_BASELINE_PATH__", "units-01-05")
replace_exact("__UNIT6_BASELINE_LABEL__", "Units 1--5")

# Frozen baseline identity and cumulative semantic names.
replace_exact(
    'BASELINE_MANIFEST_SHA256 = "5c548ca6b5257840b25f721b0e5548b89eb872b264d3d82a3afb7e7fb5186ac1"',
    'BASELINE_MANIFEST_SHA256 = "325958e8350b5a179dbad96d9a7bda71adfc82ef8b4abf78d0dc34d51ac2eadf"',
    expected=1,
)
replace_exact(
    'BASELINE_RECORDS_SHA256 = "65434f1f6503d90569f39e2faa43d6d7bdcc752ea0a21e7ddae2d36c9d68c059"',
    'BASELINE_RECORDS_SHA256 = "6fd038ef29dd5fc7c7fdbf956e4e20d53e35f851feb16459f05c634ce240cb0d"',
    expected=1,
)
replace_exact(
    'BASELINE_SCHEMA_SHA256 = "519ab6508174375b38c737c7ff31c17dd5af8c8b8dfce4dbcdfc0b96fa9226cb"',
    'BASELINE_SCHEMA_SHA256 = "0553c75a81cecd08ba39a5e67e1aa39ed0c90e9697d8deefb84f7eea09b42eef"',
    expected=1,
)
replace_exact("BASELINE_RECORD_COUNT = 2775", "BASELINE_RECORD_COUNT = 3471", expected=1)
replace_exact("units_01_04", "units_01_05")

# Advance Unit-specific identifiers, files, bindings, and reader scope.
for old, new in (
    ("UNIT5", "UNIT6"),
    ("UNIT_05", "UNIT_06"),
    ("unit5", "unit6"),
    ("unit05", "unit06"),
    ("unit_5", "unit_6"),
    ("Unit 5", "Unit 6"),
    ("unit-05", "unit-06"),
    ("lecture-05", "lecture-06"),
    ("worksheet-05", "worksheet-06"),
    ("w05", "w06"),
    ("l05", "l06"),
    ("0105", "0106"),
    ("01_05", "01_06"),
):
    replace_exact(old, new)

# These keys describe the preserved baseline, not the new cumulative output.
replace_exact("units_01_06_baseline", "units_01_05_baseline")
replace_exact("units_01_06_record_bytes_preserved", "units_01_05_record_bytes_preserved")
replace_exact("units_01_06_records_preserved", "units_01_05_records_preserved")

replace_exact('build_receipt.get("through_unit") != 5', 'build_receipt.get("through_unit") != 6', expected=1)
replace_exact('authority_manifest.get("unit_number") != 5', 'authority_manifest.get("unit_number") != 6', expected=1)
replace_exact(
    'unit6_map.get("exercise_count") != 27 or unit6_map.get("solution_count") != 4',
    'unit6_map.get("exercise_count") != 30 or unit6_map.get("solution_count") != 9',
    expected=1,
)
replace_exact('"through_unit": 5', '"through_unit": 6')

concept_block = '''NEW_CONCEPTS = {
    "AGT-0043": ("concept.polynomial-parametrization", "polynomial parametrization"),
    "AGT-0044": ("concept.rational-parametrization", "rational parametrization"),
    "AGT-0045": ("concept.rational-curve", "rational curve"),
    "AGT-0046": ("concept.homogenization", "homogenization"),
    "AGT-0047": ("concept.dehomogenization", "dehomogenization"),
    "AGT-0048": ("concept.differentiable-curve", "differentiable curve"),
    "AGT-0049": ("concept.domain-of-definition", "domain of definition"),
    "AGT-0050": ("concept.implicit-function-theorem", "implicit function theorem"),
}

'''
source, count = re.subn(r"NEW_CONCEPTS = \{\n.*?\n\}\n\n", concept_block, source, count=1, flags=re.DOTALL)
if count != 1:
    raise SystemExit("Exporter concept block drift")

correction_block = '''new_correction_ids = [
    "AGC-CORR-0010",
    "AGC-ADAPT-0008",
    "AGC-ADAPT-0009",
    "AGC-ADAPT-0010",
    "AGC-ADAPT-0011",
]
new_correction_rows = [
    row for row in read_csv(CORRECTIONS_PATH)
    if row["correction_id"] in set(new_correction_ids)
]
if [row["correction_id"] for row in new_correction_rows] != new_correction_ids:
    raise SystemExit("Unit 6 correction/adaptation rows are missing or out of order")
correction_targets = {
    "AGC-CORR-0010": ["br-ak-2025-2026-l06-thm-02-proof"],
    "AGC-ADAPT-0008": ["br-ak-2025-2026-l06-ex-02"],
    "AGC-ADAPT-0009": ["br-ak-2025-2026-l06", "br-ak-2025-2026-w06"],
    "AGC-ADAPT-0010": ["br-ak-2025-2026-l06-ex-02"],
    "AGC-ADAPT-0011": ["br-ak-2025-2026-l06-thm-02-proof"],
}
'''
source, count = re.subn(
    r"new_correction_ids = \[\n.*?\n\}\n(?=for row in new_correction_rows:)",
    correction_block,
    source,
    count=1,
    flags=re.DOTALL,
)
if count != 1:
    raise SystemExit("Exporter correction block drift")

# The transformed exporter must bind this wrapper and the Unit 6 QA script.
required_markers = [
    'BASELINE = ROOT / "backend" / "units-01-05"',
    'OUT = ROOT / "backend" / "units-01-06"',
    'CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-06.2026-08-22"',
    'ROOT / "source" / "id-ID" / "lecture-06.md"',
    'ROOT / "source" / "id-ID" / "worksheet-06-solutions.md"',
    'ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-06.pdf"',
    'ROOT / "scripts" / "qa_backend_units_01_06.py"',
]
missing = [marker for marker in required_markers if marker not in source]
if missing:
    raise SystemExit(f"Transformed exporter markers absent: {missing}")

exec(compile(source, str(Path(__file__).resolve()), "exec"), globals())
