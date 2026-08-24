#!/usr/bin/env python3
"""Fail-closed replay and closure QA for the cumulative Units 1--7 backend."""

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


replace_exact("units-01-04", "__UNIT7_BASELINE_PATH__")
replace_exact("Units 1--4", "__UNIT7_BASELINE_LABEL__")
replace_exact("units-01-05", "units-01-07")
replace_exact("Units 1--5", "Units 1--7")
replace_exact("__UNIT7_BASELINE_PATH__", "units-01-06")
replace_exact("__UNIT7_BASELINE_LABEL__", "Units 1--6")
replace_exact(
    'BASELINE_RECORDS_SHA256 = "65434f1f6503d90569f39e2faa43d6d7bdcc752ea0a21e7ddae2d36c9d68c059"',
    'BASELINE_RECORDS_SHA256 = "6ef1b74826ad905689e4903011ef0a79acf19a9759b06f43804ff53e3abc56b3"',
    expected=1,
)
replace_exact("BASELINE_RECORD_COUNT = 2775", "BASELINE_RECORD_COUNT = 4344", expected=1)
replace_exact("units_01_04", "units_01_06")
replace_exact("units0104", "units0106", expected=1)

for old, new in (
    ("UNIT5", "UNIT7"),
    ("UNIT_05", "UNIT_07"),
    ("unit5", "unit7"),
    ("unit_05", "unit_07"),
    ("unit_5", "unit_7"),
    ("Unit 5", "Unit 7"),
    ("unit-05", "unit-07"),
    ("lecture-05", "lecture-07"),
    ("worksheet-05", "worksheet-07"),
    ("w05", "w07"),
    ("0105", "0107"),
    ("01_05", "01_07"),
):
    replace_exact(old, new)

replace_exact('manifest["through_unit"] == 5', 'manifest["through_unit"] == 7', expected=1)
replace_exact('build_receipt["through_unit"] == 5', 'build_receipt["through_unit"] == 7', expected=1)
replace_exact('authority_manifest["unit_number"] == 5', 'authority_manifest["unit_number"] == 7', expected=1)
replace_exact('"through_unit": 5', '"through_unit": 7', expected=1)
replace_exact('len(exercises) == 27', 'len(exercises) == 33', expected=1)
replace_exact('len(solutions) == 4', 'len(solutions) == 3', expected=1)
replace_exact(
    'source_solution_numbers == mapped_numbers == [3, 15, 19, 20]',
    'source_solution_numbers == mapped_numbers == [10, 11, 22]',
    expected=1,
)
replace_exact('len(class_ids["exercise"]) == 134', 'len(class_ids["exercise"]) == 197', expected=1)
replace_exact('len(class_ids["solution"]) == 28', 'len(class_ids["solution"]) == 40', expected=1)
replace_exact('len(rights_rows) == 3', 'len(rights_rows) == 9', expected=1)
replace_exact('closure["reader_media_positions"] == 3', 'closure["reader_media_positions"] == 9', expected=1)
replace_exact(
    'len(unique_local_paths) == closure["unique_local_assets"] == 4',
    'len(unique_local_paths) == closure["unique_local_assets"] == 13',
    expected=1,
)
replace_exact('len(class_ids["asset"]) == 41', 'len(class_ids["asset"]) == 53', expected=1)
replace_exact(
    'len(class_ids["concept"]) == 42 and len(class_ids["term"]) == 42',
    'len(class_ids["concept"]) == 54 and len(class_ids["term"]) == 54',
    expected=1,
)
replace_exact('len(correction_rows) == 16', 'len(correction_rows) == 35', expected=1)
replace_exact('len(class_ids["correction"]) == 16', 'len(class_ids["correction"]) == 35', expected=1)
replace_exact("does not contain sixteen rows", "does not contain thirty-five rows", expected=1)
replace_exact('"unit_07_additions": 7', '"unit_07_additions": 14', expected=1)
replace_exact('"sixteen_row_correction_ledger_hash_closure"', '"thirty_five_row_correction_ledger_hash_closure"', expected=1)

term_block = '''NEW_TERM_BINDINGS = {
    "AGT-0051": ("concept.conic-section", "irisan kerucut"),
    "AGT-0052": ("concept.quadric", "kuadrik"),
    "AGT-0053": ("concept.quadratic-form", "bentuk kuadratik"),
    "AGT-0054": ("concept.algebraic-closure", "ketertutupan aljabar"),
}

'''
source, count = re.subn(r"NEW_TERM_BINDINGS = \{\n.*?\n\}\n\n", term_block, source, count=1, flags=re.DOTALL)
if count != 1:
    raise SystemExit("Backend-QA terminology block drift")

# Replace byte-identical baseline checking with an independent reconstruction
# of the authorized payload refresh and an exact structural projection audit.
baseline_block = '''require(digest(BASELINE / "records.jsonl") == BASELINE_RECORDS_SHA256, "Units 1--6 baseline hash changed")
baseline_records: list[dict[str, Any]] = [
    json.loads(line)
    for line in (BASELINE / "records.jsonl").read_text(encoding="utf-8").splitlines()
]
cumulative_raw_by_id = {json.loads(line)["stable_id"]: line for line in combined_lines}
require(len(baseline_records) == BASELINE_RECORD_COUNT, "Frozen Units 1--6 baseline record count changed")
from backend_payload_refresh_units_01_07 import refresh_baseline
from backend_architecture_units_01_07 import (
    BGK_RELATION_ID,
    BGK_RESOURCE_ID,
    BGK_RIGHTS_ID,
    COURSE_ID,
    HANDOFF_BYTES,
    HANDOFF_SHA256,
    HANDOFF_WORKSPACE_RELATIVE,
    NAPKIN_RELATION_ID,
    NAPKIN_RESOURCE_ID,
    audit_architecture_export,
)

TERMINOLOGY_MIGRATION_PATH = ROOT / "qa" / "TERMINOLOGY_MIGRATION_UNIT_07.json"
terminology_refreshed_baseline = json.loads(json.dumps(baseline_records, ensure_ascii=False))
baseline_refresh = refresh_baseline(
    root=ROOT,
    baseline_records=terminology_refreshed_baseline,
    records=list(terminology_refreshed_baseline),
    terminology_path=TERMINOLOGY_PATH,
    migration_receipt_path=TERMINOLOGY_MIGRATION_PATH,
)
architecture_correction = audit_architecture_export(
    root=ROOT,
    terminology_refreshed_baseline=terminology_refreshed_baseline,
    cumulative_records=combined_records,
    timestamp=manifest["generated_from_build_utc"],
)
require(
    manifest["units_01_06_baseline"]["authorized_payload_refresh"] == baseline_refresh,
    "Manifest authorized baseline-refresh inventory does not replay",
)
require(
    manifest["architecture_correction"] == architecture_correction,
    "Manifest two-volume architecture correction does not replay",
)
require(
    manifest["units_01_06_baseline"]["stable_ids_and_structural_projection_preserved"] is True,
    "Manifest does not assert prior stable-ID/topology preservation",
)
'''
source, count = re.subn(
    r'require\(digest\(BASELINE / "records\.jsonl"\).*?\n\s*require\(cumulative_raw_by_id\.get\(stable_id\) == baseline_line, f"Units 1--6 record bytes changed: \{stable_id\}"\)\n',
    lambda _: baseline_block,
    source,
    count=1,
    flags=re.DOTALL,
)
if count != 1:
    raise SystemExit("Backend-QA baseline comparison block drift")

# Assert the exact three-record correction and three-record BGK closure without
# weakening any pre-existing family or endpoint checks.
replace_exact(
    'counts = Counter(record["entity_class"] for record in combined_records)',
    '''expected_architecture_changed_ids = {
    COURSE_ID,
    NAPKIN_RESOURCE_ID,
    NAPKIN_RELATION_ID,
}
expected_architecture_added_ids = {
    BGK_RESOURCE_ID,
    BGK_RIGHTS_ID,
    BGK_RELATION_ID,
}
require(
    {row["stable_id"] for row in architecture_correction["changed_existing_records"]}
    == expected_architecture_changed_ids,
    "Architecture correction changed an unexpected existing stable ID",
)
require(
    {row["stable_id"] for row in architecture_correction["added_records"]}
    == expected_architecture_added_ids,
    "Architecture correction added an unexpected stable ID",
)
require(expected_architecture_added_ids <= id_set, "BGK architecture records are incomplete")
require(len(class_ids["resource"]) == 4, "Cumulative resource-family count mismatch")
require(len(class_ids["rights"]) == 58, "Cumulative rights-family count mismatch")
require(len(class_ids["relation"]) == 2134, "Cumulative relation-family count mismatch")
course = by_id[COURSE_ID]
napkin = by_id[NAPKIN_RESOURCE_ID]
napkin_relation = by_id[NAPKIN_RELATION_ID]
bgk_resource = by_id[BGK_RESOURCE_ID]
bgk_rights = by_id[BGK_RIGHTS_ID]
bgk_relation = by_id[BGK_RELATION_ID]
require(course["payload"]["required_second_volume_resource_id"] == BGK_RESOURCE_ID, "Course does not require BGK")
require(course["payload"]["concentrated_bgk_route_units"] == [*range(2, 16), *range(23, 28)], "BGK concentrated route mismatch")
require(course["payload"]["napkin_disposition"].startswith("optional reference evidence only"), "Napkin course disposition is not optional")
require(napkin["payload"]["required_course_material"] is False, "Napkin remains required course material")
require(napkin["payload"]["required_donor"] is False, "Napkin remains a required donor")
require(napkin["payload"]["required_dependency"] is False, "Napkin remains a required dependency")
require(napkin_relation["payload"]["relation_type"] == "optional_reference", "Napkin relation is not optional")
require(bgk_relation["payload"]["relation_type"] == "requires_complete_volume", "BGK relation is not required")
require(bgk_relation["payload"]["subject_id"] == COURSE_ID and bgk_relation["payload"]["object_id"] == BGK_RESOURCE_ID, "BGK relation endpoints mismatch")
require(bgk_resource["status"] == "required_second_volume_pending_complete_authority_freeze", "BGK resource authority state is overstated")
require(bgk_resource["content_sha256"] is None, "Unfrozen BGK resource has a content hash")
require(bgk_rights["status"] == "pending_complete_authority_freeze", "BGK rights authority state is overstated")
require(bgk_rights["content_sha256"] is None, "Unfrozen BGK rights has a content hash")
require(
    not any(
        row["payload"].get("subject_id") == COURSE_ID
        and row["payload"].get("object_id") == NAPKIN_RESOURCE_ID
        and row["payload"].get("relation_type") != "optional_reference"
        for row in combined_records
        if row["entity_class"] == "relation"
    ),
    "A required course-to-Napkin relation survives",
)
architecture_text = canonical({
    stable_id: by_id[stable_id]
    for stable_id in sorted(expected_architecture_changed_ids | expected_architecture_added_ids)
})
require("compact schemes transition" not in architecture_text.lower(), "Stale compact-transition wording survives")
require("bounded donor" not in architecture_text.lower(), "Stale required-donor wording survives")
require(manifest["validation"]["two_volume_architecture_record_closure"] is True, "Manifest architecture validation flag absent")

external_handoff_path = ROOT.parents[2] / HANDOFF_WORKSPACE_RELATIVE
external_handoff_present = external_handoff_path.is_file()
if external_handoff_present:
    require(external_handoff_path.stat().st_size == HANDOFF_BYTES, "External controlling handoff byte count changed")
    require(digest(external_handoff_path) == HANDOFF_SHA256, "External controlling handoff SHA-256 changed")
external_handoff_verification = {
    "workspace_relative_path": HANDOFF_WORKSPACE_RELATIVE,
    "expected_bytes": HANDOFF_BYTES,
    "expected_sha256": HANDOFF_SHA256,
    "present_and_verified_in_this_workspace": external_handoff_present,
    "required_for_extracted_package_replay": False,
}

counts = Counter(record["entity_class"] for record in combined_records)''',
    expected=1,
)

# The terminology receipt is an additional current artifact alongside the
# responsive receipt; it is not a replacement for responsive layout QA.
replace_exact(
    '"qa/UNITS_01_07_RESPONSIVE_QA.json",\n    "qa/UNIT_07_PROTECTED_SURFACES.json",',
    '"qa/UNITS_01_07_RESPONSIVE_QA.json",\n    "qa/TERMINOLOGY_MIGRATION_UNIT_07.json",\n    "qa/UNIT_07_PROTECTED_SURFACES.json",',
    expected=1,
)

# Report the protected payload refresh instead of a false byte-preservation
# claim, retaining the same stable-ID count as the baseline.
replace_exact(
    '"units_01_06_record_bytes_preserved": len(baseline_raw_by_id),',
    '''"units_01_06_stable_ids_preserved": len(baseline_records),
    "units_01_06_authorized_payload_refresh": baseline_refresh,
    "two_volume_architecture": architecture_correction,
    "external_controlling_handoff_verification": external_handoff_verification,''',
    expected=1,
)
replace_exact(
    '"stable_id_uniqueness_format_and_units0106_byte_preservation"',
    '"stable_id_uniqueness_and_units0106_authorized_payload_refresh_with_structural_projection_preservation"',
    expected=1,
)
replace_exact(
    '"parent_relation_resource_edition_rights_and_concept_closure",',
    '"parent_relation_resource_edition_rights_and_concept_closure",\n        "two_volume_brenner_architecture_and_optional_napkin_closure",',
    expected=1,
)
replace_exact(
    '''"replay_command": f'"{sys.executable}" "{Path(__file__).relative_to(ROOT).as_posix()}"',''',
    '''"replay_command": "python scripts/qa_backend_units_01_07.py",''',
    expected=1,
)

required_markers = [
    'EXPORTER = ROOT / "scripts" / "export_backend_units_01_07.py"',
    'BACKEND = ROOT / "backend" / "units-01-07"',
    'BASELINE = ROOT / "backend" / "units-01-06"',
    'CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-07.2026-08-22"',
    'ROOT / "source" / "id-ID" / "worksheet-07.md"',
    'qa/UNITS_01_07_MACHINE_QA.json',
    '"qa/UNITS_01_07_RESPONSIVE_QA.json"',
    '"qa/TERMINOLOGY_MIGRATION_UNIT_07.json"',
    '"qa/UNIT_07_PROTECTED_SURFACES.json"',
    'baseline_refresh = refresh_baseline(',
    'architecture_correction = audit_architecture_export(',
    '"two_volume_architecture": architecture_correction',
    '"present_and_verified_in_this_workspace": external_handoff_present',
]
missing = [marker for marker in required_markers if marker not in source]
if missing:
    raise SystemExit(f"Transformed backend-QA markers absent: {missing}")

exec(compile(source, str(Path(__file__).resolve()), "exec"), globals())
