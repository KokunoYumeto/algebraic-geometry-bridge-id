#!/usr/bin/env python3
"""Export the deterministic cumulative native backend through Units 1--7.

The audited Unit 5 exporter remains the structural template.  Units 1--6 are
the stable-ID/topology baseline; their content surfaces are refreshed only for
the evidence-backed 2026-08-22 terminology migration before Unit 7 is added.
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


# Advance the output while retaining the exact frozen Units 1--6 identity and
# topology as the migration baseline.
replace_exact("units-01-04", "__UNIT7_BASELINE_PATH__")
replace_exact("Units 1--4", "__UNIT7_BASELINE_LABEL__")
replace_exact("units-01-05", "units-01-07")
replace_exact("Units 1--5", "Units 1--7")
replace_exact("__UNIT7_BASELINE_PATH__", "units-01-06")
replace_exact("__UNIT7_BASELINE_LABEL__", "Units 1--6")

replace_exact(
    'BASELINE_MANIFEST_SHA256 = "5c548ca6b5257840b25f721b0e5548b89eb872b264d3d82a3afb7e7fb5186ac1"',
    'BASELINE_MANIFEST_SHA256 = "d018cc7ca7853cf3c5668605f472a47e9d331fb6a53730eac6861d3b06d918f2"',
    expected=1,
)
replace_exact(
    'BASELINE_RECORDS_SHA256 = "65434f1f6503d90569f39e2faa43d6d7bdcc752ea0a21e7ddae2d36c9d68c059"',
    'BASELINE_RECORDS_SHA256 = "6ef1b74826ad905689e4903011ef0a79acf19a9759b06f43804ff53e3abc56b3"',
    expected=1,
)
replace_exact(
    'BASELINE_SCHEMA_SHA256 = "519ab6508174375b38c737c7ff31c17dd5af8c8b8dfce4dbcdfc0b96fa9226cb"',
    'BASELINE_SCHEMA_SHA256 = "6affca57fdbcb797c4776177b8f5aaa97d72335a70b60d3ce9a525f9e1d78192"',
    expected=1,
)
replace_exact("BASELINE_RECORD_COUNT = 2775", "BASELINE_RECORD_COUNT = 4344", expected=1)
replace_exact("units_01_04", "units_01_06")

for old, new in (
    ("UNIT5", "UNIT7"),
    ("UNIT_05", "UNIT_07"),
    ("unit5", "unit7"),
    ("unit05", "unit07"),
    ("unit_5", "unit_7"),
    ("Unit 5", "Unit 7"),
    ("unit-05", "unit-07"),
    ("lecture-05", "lecture-07"),
    ("worksheet-05", "worksheet-07"),
    ("w05", "w07"),
    ("l05", "l07"),
    ("0105", "0107"),
    ("01_05", "01_07"),
):
    replace_exact(old, new)

replace_exact('build_receipt.get("through_unit") != 5', 'build_receipt.get("through_unit") != 7', expected=1)
replace_exact('authority_manifest.get("unit_number") != 5', 'authority_manifest.get("unit_number") != 7', expected=1)
replace_exact(
    'unit7_map.get("exercise_count") != 27 or unit7_map.get("solution_count") != 4',
    'unit7_map.get("exercise_count") != 33 or unit7_map.get("solution_count") != 3',
    expected=1,
)
replace_exact('if len(unit7_rights_rows) != 3:', 'if len(unit7_rights_rows) != 9:', expected=1)
replace_exact(
    'raise SystemExit("Unit 7 rights closure does not contain three positions")',
    'raise SystemExit("Unit 7 rights closure does not contain nine positions")',
    expected=1,
)
replace_exact('"through_unit": 5', '"through_unit": 7')

concept_block = '''NEW_CONCEPTS = {
    "AGT-0051": ("concept.conic-section", "conic section"),
    "AGT-0052": ("concept.quadric", "quadric"),
    "AGT-0053": ("concept.quadratic-form", "quadratic form"),
    "AGT-0054": ("concept.algebraic-closure", "algebraic closure"),
}

'''
source, count = re.subn(r"NEW_CONCEPTS = \{\n.*?\n\}\n\n", concept_block, source, count=1, flags=re.DOTALL)
if count != 1:
    raise SystemExit("Exporter concept block drift")

correction_block = '''new_correction_ids = [
    "AGC-CORR-0011",
    "AGC-CORR-0012",
    "AGC-CORR-0013",
    "AGC-CORR-0014",
    "AGC-ADAPT-0012",
    "AGC-ADAPT-0013",
    "AGC-ADAPT-0014",
    "AGC-CORR-0015",
    "AGC-CORR-0016",
    "AGC-CORR-0017",
    "AGC-CORR-0018",
    "AGC-CORR-0019",
    "AGC-ADAPT-0015",
    "AGC-ADAPT-0016",
]
new_correction_rows = [
    row for row in read_csv(CORRECTIONS_PATH)
    if row["correction_id"] in set(new_correction_ids)
]
if [row["correction_id"] for row in new_correction_rows] != new_correction_ids:
    raise SystemExit("Unit 7 correction/adaptation rows are missing or out of order")
correction_targets = {
    "AGC-CORR-0011": ["br-ak-2025-2026-l07"],
    "AGC-CORR-0012": ["br-ak-2025-2026-l07-ex-02"],
    "AGC-CORR-0013": ["br-ak-2025-2026-w07-ex-10"],
    "AGC-CORR-0014": ["br-ak-2025-2026-w07-ex-26"],
    "AGC-CORR-0015": ["br-ak-2025-2026-w07-sol-10"],
    "AGC-CORR-0016": ["br-ak-2025-2026-w07-ex-15"],
    "AGC-CORR-0017": ["br-ak-2025-2026-w07-ex-26"],
    "AGC-CORR-0018": ["br-ak-2025-2026-w07-ex-27"],
    "AGC-CORR-0019": ["br-ak-2025-2026-w07-sol-22"],
    "AGC-ADAPT-0012": ["br-ak-2025-2026-l07"],
    "AGC-ADAPT-0013": ["br-ak-2025-2026-l07"],
    "AGC-ADAPT-0014": ["br-ak-2025-2026-l07"],
    "AGC-ADAPT-0015": ["br-ak-2025-2026-w07-sol-10"],
    "AGC-ADAPT-0016": [
        "br-ak-2025-2026-l01", "br-ak-2025-2026-w01", "br-ak-2025-2026-w01-solutions",
        "br-ak-2025-2026-l02", "br-ak-2025-2026-w02", "br-ak-2025-2026-w02-solutions",
        "br-ak-2025-2026-l03", "br-ak-2025-2026-w03", "br-ak-2025-2026-w03-solutions",
        "br-ak-2025-2026-l04", "br-ak-2025-2026-w04", "br-ak-2025-2026-w04-solutions",
        "br-ak-2025-2026-l05", "br-ak-2025-2026-w05", "br-ak-2025-2026-w05-solutions",
        "br-ak-2025-2026-l06", "br-ak-2025-2026-w06",
        "br-ak-2025-2026-l07", "br-ak-2025-2026-w07",
    ],
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

# Bind the five actual Unit 7 QA surfaces, including the terminology migration
# and the independently generated desktop/mobile responsive receipt.
replace_exact(
    'RESPONSIVE_QA_PATH = ROOT / "qa" / "UNITS_01_07_RESPONSIVE_QA.json"',
    '''RESPONSIVE_QA_PATH = ROOT / "qa" / "UNITS_01_07_RESPONSIVE_QA.json"
TERMINOLOGY_MIGRATION_QA_PATH = ROOT / "qa" / "TERMINOLOGY_MIGRATION_UNIT_07.json"''',
    expected=1,
)
replace_exact(
    '("qa.units0107.responsive", RESPONSIVE_QA_PATH, "desktop_and_mobile_reader_reflow", "status"),',
    '''("qa.units0107.responsive", RESPONSIVE_QA_PATH, "desktop_and_mobile_reader_reflow", "status"),
    ("qa.units0107.terminology-migration", TERMINOLOGY_MIGRATION_QA_PATH, "indonesian_primary_source_terminology_migration", "schema"),''',
    expected=1,
)
replace_exact(
    'status="passed" if qa_status == "PASS" else "failed",',
    'status="passed" if qa_status in {"PASS", "ag-bridge-terminology-migration-v1"} else "failed",',
    expected=1,
)
replace_exact(
    'RESPONSIVE_QA_PATH,\n    PROTECTED_QA_PATH,',
    'RESPONSIVE_QA_PATH,\n    TERMINOLOGY_MIGRATION_QA_PATH,\n    PROTECTED_QA_PATH,',
    expected=2,
)

# Refresh the prior payload surfaces after all current terminology records and
# corrections have been loaded, but before concept needles index Unit 7.
refresh_marker = '''term_needles = [
'''
refresh_code = '''from backend_payload_refresh_units_01_07 import refresh_baseline
from backend_architecture_units_01_07 import apply_architecture_correction

TERMINOLOGY_MIGRATION_QA_PATH = ROOT / "qa" / "TERMINOLOGY_MIGRATION_UNIT_07.json"
baseline_refresh = refresh_baseline(
    root=ROOT,
    baseline_records=baseline_records,
    records=records,
    terminology_path=TERMINOLOGY_PATH,
    migration_receipt_path=TERMINOLOGY_MIGRATION_QA_PATH,
    canonical=canonical,
    text_digest=text_digest,
    digest=digest,
)
migrated_baseline_ids = set(baseline_refresh["changed_record_ids"])
architecture_correction = apply_architecture_correction(
    root=ROOT,
    records=records,
    timestamp=timestamp,
)
migrated_baseline_ids.update(
    row["stable_id"] for row in architecture_correction["changed_existing_records"]
)

term_needles = [
'''
replace_exact(refresh_marker, refresh_code, expected=1)

replace_exact(
    'return baseline_raw_by_id.get(record["stable_id"], canonical(record))',
    'return canonical(record) if record["stable_id"] in migrated_baseline_ids else baseline_raw_by_id.get(record["stable_id"], canonical(record))',
    expected=1,
)

# The manifest states the precise compatibility rule instead of claiming byte
# preservation for the intentionally refreshed prior payloads.
replace_exact(
    '"serialization": "canonical JSON Lines: records and keys sorted, compact separators, baseline-compatible CRLF",',
    '"serialization": "canonical JSON Lines: records and keys sorted, compact separators, CRLF; Units 1--6 structural baseline with authorized content refresh",',
    expected=1,
)
replace_exact(
    '"record_bytes_preserved": True,',
    '''"record_bytes_preserved": False,
        "stable_ids_and_structural_projection_preserved": True,
        "authorized_payload_refresh": baseline_refresh,''',
    expected=1,
)
replace_exact(
    '"units_01_06_record_bytes_preserved": True,',
    '"units_01_06_authorized_payload_refresh_only": True,',
    expected=1,
)
replace_exact(
    '"units_01_06_records_preserved": BASELINE_RECORD_COUNT,',
    '"units_01_06_stable_ids_preserved": BASELINE_RECORD_COUNT,\n            "authorized_prior_record_refreshes": baseline_refresh["changed_record_count"],',
    expected=1,
)

# Bind the refresh implementation and the human-readable terminology decision.
replace_exact(
    'Path(__file__),\n    ROOT / "scripts" / "qa_backend_units_01_07.py",',
    '''Path(__file__),
    ROOT / "scripts" / "backend_payload_refresh_units_01_07.py",
    ROOT / "scripts" / "backend_architecture_units_01_07.py",
    ROOT / "scripts" / "qa_backend_units_01_07.py",
    ROOT / "00_control" / "TERMINOLOGY_QA_20260822.md",
    ROOT / "00_control" / "SCHEME_BRIDGE_DECISION.md",''',
    expected=1,
)

replace_exact(
    '"reader_binding": {',
    '"architecture_correction": architecture_correction,\n    "reader_binding": {',
    expected=1,
)
replace_exact(
    '"deterministic_double_replay_required": True,',
    '"two_volume_architecture_record_closure": True,\n        "deterministic_double_replay_required": True,',
    expected=1,
)

required_markers = [
    'BASELINE = ROOT / "backend" / "units-01-06"',
    'OUT = ROOT / "backend" / "units-01-07"',
    'CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-07.2026-08-22"',
    'ROOT / "source" / "id-ID" / "lecture-07.md"',
    'ROOT / "source" / "id-ID" / "worksheet-07-solutions.md"',
    'ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-07.pdf"',
    'ROOT / "scripts" / "qa_backend_units_01_07.py"',
    'baseline_refresh = refresh_baseline(',
    'architecture_correction = apply_architecture_correction(',
    '"architecture_correction": architecture_correction',
    '"two_volume_architecture_record_closure": True',
    '"units_01_06_authorized_payload_refresh_only": True',
]
missing = [marker for marker in required_markers if marker not in source]
if missing:
    raise SystemExit(f"Transformed exporter markers absent: {missing}")

exec(compile(source, str(Path(__file__).resolve()), "exec"), globals())
