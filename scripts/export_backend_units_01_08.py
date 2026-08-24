#!/usr/bin/env python3
"""Export the deterministic cumulative native backend through Unit 8."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "export_backend_units_01_07.py"
outer = TEMPLATE.read_text(encoding="utf-8")
marker = 'exec(compile(source, str(Path(__file__).resolve()), "exec"), globals())'
if outer.count(marker) != 1:
    raise SystemExit("Unit 7 exporter template final exec marker drift")

post = r'''

def _replace(old: str, new: str, expected: int = 1) -> None:
    global source
    count = source.count(old)
    if count != expected:
        raise SystemExit(f"Unit 8 exporter template drift for {old!r}: expected {expected}, found {count}")
    source = source.replace(old, new)


_replace('OUT = ROOT / "backend" / "units-01-07"', 'OUT = ROOT / "backend" / "units-01-08"')
_replace('BASELINE = ROOT / "backend" / "units-01-06"', 'BASELINE = ROOT / "backend" / "units-01-07"')
_replace('BASELINE_MANIFEST_SHA256 = "d018cc7ca7853cf3c5668605f472a47e9d331fb6a53730eac6861d3b06d918f2"', 'BASELINE_MANIFEST_SHA256 = "8b482971c444a4e5d90695f084234924a873b671885428d98e9db447e4924967"')
_replace('BASELINE_RECORDS_SHA256 = "6ef1b74826ad905689e4903011ef0a79acf19a9759b06f43804ff53e3abc56b3"', 'BASELINE_RECORDS_SHA256 = "663713a128a0e673a4daf9edd67f9c3dd10ebae02039f8e0c2044c0ca0fa14be"')
_replace('BASELINE_SCHEMA_SHA256 = "6affca57fdbcb797c4776177b8f5aaa97d72335a70b60d3ce9a525f9e1d78192"', 'BASELINE_SCHEMA_SHA256 = "fed2bc176f438e9ab2053b21c67f9ac3feac391ccd83f5c70107a1f86f994b8b"')
_replace('BASELINE_RECORD_COUNT = 4344', 'BASELINE_RECORD_COUNT = 5182')
_replace('"units_01_06_baseline_manifest_sha256"', '"units_01_07_baseline_manifest_sha256"')
_replace('"units_01_06_baseline": {', '"units_01_07_baseline": {')
_replace('"manifest_path": "backend/units-01-06/MANIFEST.json"', '"manifest_path": "backend/units-01-07/MANIFEST.json"')
_replace('"records_path": "backend/units-01-06/records.jsonl"', '"records_path": "backend/units-01-07/records.jsonl"')
_replace('"record_bytes_preserved": False', '"record_bytes_preserved": True')
_replace('"units_01_06_authorized_payload_refresh_only": True', '"unit_01_07_baseline_carried_forward": True')
_replace('"units_01_06_stable_ids_preserved": BASELINE_RECORD_COUNT', '"units_01_07_stable_ids_preserved": BASELINE_RECORD_COUNT')
_replace('"serialization": "canonical JSON Lines: records and keys sorted, compact separators, CRLF; Units 1--6 structural baseline with authorized content refresh"', '"serialization": "canonical JSON Lines: records and keys sorted, compact separators, CRLF; frozen Unit 7 cumulative baseline carried forward"')
_replace('MACHINE_QA_PATH = ROOT / "qa" / "UNITS_01_07_MACHINE_QA.json"', 'MACHINE_QA_PATH = ROOT / "qa" / "UNITS_01_08_MACHINE_QA.json"')
_replace('VISUAL_QA_PATH = ROOT / "qa" / "UNITS_01_07_VISUAL_QA.json"', 'VISUAL_QA_PATH = ROOT / "qa" / "UNITS_01_08_VISUAL_QA.json"')
_replace('RESPONSIVE_QA_PATH = ROOT / "qa" / "UNITS_01_07_RESPONSIVE_QA.json"', 'RESPONSIVE_QA_PATH = ROOT / "qa" / "UNITS_01_08_RESPONSIVE_QA.json"')
_replace('PROTECTED_QA_PATH = ROOT / "qa" / "UNIT_07_PROTECTED_SURFACES.json"', 'PROTECTED_QA_PATH = ROOT / "qa" / "UNIT_08_PROTECTED_SURFACES.json"')
_replace('CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-07.2026-08-22"', 'CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-08.2026-08-23"')
_replace('PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-06.2026-08-22"', 'PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-07.2026-08-22"')
_replace('source_local_id="units-01-07"', 'source_local_id="units-01-08"')
_replace('"through_unit": 7', '"through_unit": 8', expected=2)
_replace('build_receipt.get("through_unit") != 7', 'build_receipt.get("through_unit") != 8')
_replace('authority_manifest.get("unit_number") != 7', 'authority_manifest.get("unit_number") != 7')
_replace('"algebraic-geometry-bridge-id-units-01-07.pdf"', '"algebraic-geometry-bridge-id-units-01-08.pdf"')
_replace('units0107', 'units0108', expected=6)
_replace('backend-record-units-01-07-v1.schema.json', 'backend-record-units-01-08-v1.schema.json')
_replace('"Algebraic Geometry Bridge cumulative backend record through Units 1--7"', '"Algebraic Geometry Bridge cumulative backend record through Units 1--8"')
_replace('"cumulative Units 1--7"', '"cumulative Units 1--8"')

# Bind the Unit 8 authority closure alongside the retained Unit 7 authority.
_replace(
    'unit7_map = json.loads(UNIT7_MAP_PATH.read_text(encoding="utf-8"))\n',
    'unit7_map = json.loads(UNIT7_MAP_PATH.read_text(encoding="utf-8"))\n'
    'AUTHORITY_MANIFEST8_PATH = ROOT / "authority" / "wikiversity" / "unit-08" / "UNIT_AUTHORITY_MANIFEST.json"\n'
    'UNIT8_MAP_PATH = ROOT / "authority" / "wikiversity" / "unit-08" / "ORDERED_EXERCISE_MAP.json"\n'
    'UNIT8_RIGHTS_PATH = ROOT / "authority" / "RIGHTS-unit-08.csv"\n'
    'UNIT8_ASSET_CLOSURE_PATH = ROOT / "authority" / "ASSET_CLOSURE-unit-08.json"\n'
    'authority_manifest8 = json.loads(AUTHORITY_MANIFEST8_PATH.read_text(encoding="utf-8"))\n'
    'unit8_map = json.loads(UNIT8_MAP_PATH.read_text(encoding="utf-8"))\n'
    'if authority_manifest8.get("unit_number") != 8 or unit8_map.get("exercise_count") != 24 or unit8_map.get("solution_count") != 2:\n'
    '    raise SystemExit("Unit 8 authority closure mismatch")\n',
)
_replace(
    '    ROOT / "source" / "id-ID" / "media-credits-unit-07.md",\n]',
    '    ROOT / "source" / "id-ID" / "media-credits-unit-07.md",\n'
    '    ROOT / "source" / "id-ID" / "frontmatter-units-01-08.md",\n'
    '    ROOT / "source" / "id-ID" / "lecture-08.md",\n'
    '    ROOT / "source" / "id-ID" / "worksheet-08.md",\n'
    '    ROOT / "source" / "id-ID" / "worksheet-08-solutions.md",\n'
    '    ROOT / "source" / "id-ID" / "media-credits-unit-08.md",\n]',
)
_replace('"unit_7_authority_manifest"', '"unit_7_authority_manifest"', expected=1)
_replace(
    '            "unit_7_exercise_map_sha256": digest(UNIT7_MAP_PATH),\n',
    '            "unit_7_exercise_map_sha256": digest(UNIT7_MAP_PATH),\n'
    '            "unit_8_authority_manifest_sha256": digest(AUTHORITY_MANIFEST8_PATH),\n'
    '            "unit_8_exercise_map_sha256": digest(UNIT8_MAP_PATH),\n',
)
_replace(
    'unit7_solution_entries = {\n    int(row["exercise_number"]): row\n    for row in unit7_map["entries"]\n    if row.get("has_public_solution")\n}\n',
    'unit7_solution_entries = {\n    int(row["exercise_number"]): row\n    for row in unit7_map["entries"]\n    if row.get("has_public_solution")\n}\n\n'
    'unit8_solution_entries = {\n    int(row["exercise_number"]): row\n    for row in unit8_map["entries"]\n    if row.get("has_public_solution")\n}\n',
)
unit8_provenance = "\n".join(
    [
        "def source_provenance_unit8(source_path: Path, metadata: dict[str, str], identifier: str) -> dict[str, Any]:",
        '    editorial = source_path.name in {"frontmatter-units-01-08.md", "media-credits-unit-08.md"}',
        '    result: dict[str, Any] = {',
        '        "source_edition_id": None if editorial else BRENNER_EDITION,',
        '        "unit_8_authority_manifest": {"path": rel(AUTHORITY_MANIFEST8_PATH), "sha256": digest(AUTHORITY_MANIFEST8_PATH)},',
        '    }',
        '    if source_path.name == "lecture-08.md":',
        '        result["upstream"] = compact_upstream(authority_manifest8["lecture"])',
        '    elif source_path.name == "worksheet-08.md":',
        '        result["upstream"] = compact_upstream(authority_manifest8["worksheet"])',
        '    elif source_path.name == "worksheet-08-solutions.md":',
        '        match = re.search(r"-sol-(\\d+)$", identifier)',
        '        result["exercise_solution_map"] = {"path": rel(UNIT8_MAP_PATH), "sha256": digest(UNIT8_MAP_PATH), "worksheet_revid": unit8_map["worksheet"]["revid"]}',
        '        result["upstream"] = compact_upstream(unit8_solution_entries[int(match.group(1))]) if match else compact_upstream(unit8_map["worksheet"])',
        '    else:',
        '        result["upstream"] = {key: metadata[key] for key in ("upstream_title", "upstream_pageid", "upstream_revid", "upstream_timestamp", "upstream_mediawiki_sha1", "source_url") if key in metadata}',
        '    return result',
        "",
        "",
    ]
)
_replace("all_new_units: list[dict[str, Any]] = []\n", unit8_provenance + "all_new_units: list[dict[str, Any]] = []\n")
_replace(
    'provenance=source_provenance(source_path, metadata, identifier),',
    'provenance=(source_provenance_unit8(source_path, metadata, identifier) if source_path.name in {"frontmatter-units-01-08.md", "lecture-08.md", "worksheet-08.md", "worksheet-08-solutions.md", "media-credits-unit-08.md"} else source_provenance(source_path, metadata, identifier)),',
    expected=1,
)
_replace(
    'provenance=source_provenance(source_path, metadata, active_id),',
    'provenance=(source_provenance_unit8(source_path, metadata, active_id) if source_path.name in {"frontmatter-units-01-08.md", "lecture-08.md", "worksheet-08.md", "worksheet-08-solutions.md", "media-credits-unit-08.md"} else source_provenance(source_path, metadata, active_id)),',
    expected=1,
)
_replace(
    '    "AGC-ADAPT-0016",\n]',
    '    "AGC-ADAPT-0016",\n'
    '    "AGC-CORR-0020",\n'
    '    "AGC-CORR-0021",\n'
    '    "AGC-ADAPT-0017",\n'
    '    "AGC-ADAPT-0018",\n'
    '    "AGC-ADAPT-0019",\n'
    '    "AGC-ADAPT-0020",\n]',
)
_replace(
    '    "AGC-ADAPT-0016": [\n        "br-ak-2025-2026-l01", "br-ak-2025-2026-w01", "br-ak-2025-2026-w01-solutions",\n        "br-ak-2025-2026-l02", "br-ak-2025-2026-w02", "br-ak-2025-2026-w02-solutions",\n        "br-ak-2025-2026-l03", "br-ak-2025-2026-w03", "br-ak-2025-2026-w03-solutions",\n        "br-ak-2025-2026-l04", "br-ak-2025-2026-w04", "br-ak-2025-2026-w04-solutions",\n        "br-ak-2025-2026-l05", "br-ak-2025-2025-2026-w05", "br-ak-2025-2026-w05-solutions",\n        "br-ak-2025-2026-l06", "br-ak-2025-2026-w06",\n        "br-ak-2025-2026-l07", "br-ak-2025-2026-w07",\n    ],\n}',
    '    "AGC-ADAPT-0016": [\n        "br-ak-2025-2026-l01", "br-ak-2025-2026-w01", "br-ak-2025-2026-w01-solutions",\n        "br-ak-2025-2026-l02", "br-ak-2025-2026-w02", "br-ak-2025-2026-w02-solutions",\n        "br-ak-2025-2026-l03", "br-ak-2025-2026-w03", "br-ak-2025-2026-w03-solutions",\n        "br-ak-2025-2026-l04", "br-ak-2025-2026-w04", "br-ak-2025-2026-w04-solutions",\n        "br-ak-2025-2026-l05", "br-ak-2025-2026-w05", "br-ak-2025-2026-w05-solutions",\n        "br-ak-2025-2026-l06", "br-ak-2025-2026-w06",\n        "br-ak-2025-2026-l07", "br-ak-2025-2026-w07",\n    ],\n'
    '    "AGC-CORR-0020": ["br-ak-2025-2026-l08"],\n'
    '    "AGC-CORR-0021": ["br-ak-2025-2026-l08-lem-01-proof"],\n'
    '    "AGC-ADAPT-0017": ["br-ak-2025-2026-l08"],\n'
    '    "AGC-ADAPT-0018": ["br-ak-2025-2026-l08"],\n'
    '    "AGC-ADAPT-0019": ["br-ak-2025-2026-l08"],\n'
    '    "AGC-ADAPT-0020": ["agc-media-credits-unit-08"],\n'
    '}',
    expected=0,
)
source, _correction_target_count = re.subn(
    r'(    "AGC-ADAPT-0016": \[.*?\n    \],)\n}',
    r'\1\n'
    '    "AGC-CORR-0020": ["br-ak-2025-2026-l08"],\n'
    '    "AGC-CORR-0021": ["br-ak-2025-2026-l08-lem-01-proof"],\n'
    '    "AGC-ADAPT-0017": ["br-ak-2025-2026-l08"],\n'
    '    "AGC-ADAPT-0018": ["br-ak-2025-2026-l08"],\n'
    '    "AGC-ADAPT-0019": ["br-ak-2025-2026-l08"],\n'
    '    "AGC-ADAPT-0020": ["agc-media-credits-unit-08"],\n}',
    source,
    count=1,
    flags=re.DOTALL,
)
if _correction_target_count != 1:
    raise SystemExit("Unit 8 correction target extension drift")
unit8_rights_block = "\n".join(
    [
        'unit8_rights_rows = read_csv(UNIT8_RIGHTS_PATH)',
        'if len(unit8_rights_rows) != 6:',
        '    raise SystemExit("Unit 8 rights closure does not contain six positions")',
        'for row in unit8_rights_rows:',
        '    component_rights_id = f"rights.{row[\'asset_id\']}"',
        '    add(make_record("rights", component_rights_id, source_local_id=row["metadata_title"], resource_id=BRENNER_RESOURCE, edition_id=CUMULATIVE_EDITION, source_locator=row["description_url"], content_sha256=row["local_sha256"], payload={"license": row["license_short"], "license_url": row["license_url"] or None, "usage_terms": row["usage_terms"] or None, "creator_or_artist": row["artist"] or row["uploader"], "uploader": row["uploader"], "attribution_required": row["attribution_required"].lower() == "true", "scope": row["asset_id"]}))',
        '    add(make_record("asset", row["asset_id"], source_local_id=row["resource_title"], parent_id=image_parent_by_path.get(row["local_path"], "br-ak-2025-2026-l08"), order=int(row["reader_order"]), path=row["local_path"], resource_id=BRENNER_RESOURCE, edition_id=CUMULATIVE_EDITION, source_locator=row["description_url"], content_sha256=row["local_sha256"], translation_state="built", rights_id=component_rights_id, payload={"caption_id": row.get("reader_caption_id") or row["asset_id"], "selected_form": row["selected_form"], "bytes": int(row["local_bytes"]), "width": int(row["local_width"]), "height": int(row["local_height"]), "mime": row["mime"], "source_original_url": row["original_url"], "selected_url": row["selected_url"], "pdf_companion": ({"path": row["pdf_local_path"], "bytes": int(row["pdf_local_bytes"]), "sha256": row["pdf_local_sha256"]} if row["pdf_local_path"] else None)}))',
        "",
    ]
)
_replace("\nall_unit_records = [record for record in records if record[\"entity_class\"] == \"unit\"]", "\n" + unit8_rights_block + "all_unit_records = [record for record in records if record[\"entity_class\"] == \"unit\"]")
_replace(
    '    if unit_type == "solution" and exercise_number is not None:\n        provenance["exercise_solution_authority"] = {\n            "map_path": rel(UNIT7_MAP_PATH),\n            "map_sha256": digest(UNIT7_MAP_PATH),\n            "upstream": compact_upstream(unit7_solution_entries[exercise_number]),\n        }\n',
    '    if unit_type == "solution" and exercise_number is not None:\n'
    '        if "-w08-sol-" in unit["stable_id"]:\n'
    '            solution_map_path, solution_entries = UNIT8_MAP_PATH, unit8_solution_entries\n'
    '        else:\n'
    '            solution_map_path, solution_entries = UNIT7_MAP_PATH, unit7_solution_entries\n'
    '        provenance["exercise_solution_authority"] = {\n'
    '            "map_path": rel(solution_map_path),\n'
    '            "map_sha256": digest(solution_map_path),\n'
    '            "upstream": compact_upstream(solution_entries[exercise_number]),\n'
    '        }\n',
)
_replace('qa.unit07.protected', 'qa.unit08.protected')
_replace(
    '    UNIT7_ASSET_CLOSURE_PATH,\n]',
    '    UNIT7_ASSET_CLOSURE_PATH,\n'
    '    AUTHORITY_MANIFEST8_PATH,\n'
    '    UNIT8_MAP_PATH,\n'
    '    UNIT8_RIGHTS_PATH,\n'
    '    UNIT8_ASSET_CLOSURE_PATH,\n]',
)
_replace(
    '    UNIT7_ASSET_CLOSURE_PATH,\n    CORRECTIONS_PATH,',
    '    UNIT7_ASSET_CLOSURE_PATH,\n'
    '    AUTHORITY_MANIFEST8_PATH,\n'
    '    UNIT8_MAP_PATH,\n'
    '    UNIT8_RIGHTS_PATH,\n'
    '    UNIT8_ASSET_CLOSURE_PATH,\n'
    '    CORRECTIONS_PATH,',
)
unit8_relation_block = "\n".join(
    [
        'for exercise_number in sorted(unit8_solution_entries):',
        '    add_relation("solves", f"br-ak-2025-2026-w08-sol-{exercise_number:02d}", f"br-ak-2025-2026-w08-ex-{exercise_number:02d}", source_locator=rel(UNIT8_MAP_PATH))',
        'for row in unit8_rights_rows:',
        '    add_relation("illustrates", row["asset_id"], image_parent_by_path.get(row["local_path"], "br-ak-2025-2026-l08"), source_locator=row["description_url"])',
        'for exercise_number in sorted(unit8_solution_entries):',
        '    add_relation("solves", f"solution.br-ak-2025-2026-w08-sol-{exercise_number:02d}", f"exercise.br-ak-2025-2026-w08-ex-{exercise_number:02d}", source_locator=rel(UNIT8_MAP_PATH), payload={"typed_family_projection": True})',
        "",
    ]
)
_replace("for typed in typed_records:\n", unit8_relation_block + "for typed in typed_records:\n")
_replace(
    '    ROOT / "scripts" / "qa_backend_units_01_07.py",\n',
    '    ROOT / "scripts" / "qa_backend_units_01_07.py",\n'
    '    ROOT / "scripts" / "qa_reader_units_01_08.py",\n'
    '    ROOT / "scripts" / "write_units_01_08_visual_receipt.py",\n',
)
_replace(
    '        "unit_7_asset_closure": {"path": rel(UNIT7_ASSET_CLOSURE_PATH), "sha256": digest(UNIT7_ASSET_CLOSURE_PATH)},\n',
    '        "unit_7_asset_closure": {"path": rel(UNIT7_ASSET_CLOSURE_PATH), "sha256": digest(UNIT7_ASSET_CLOSURE_PATH)},\n'
    '        "unit_8_manifest": {"path": rel(AUTHORITY_MANIFEST8_PATH), "sha256": digest(AUTHORITY_MANIFEST8_PATH)},\n'
    '        "unit_8_exercise_map": {"path": rel(UNIT8_MAP_PATH), "sha256": digest(UNIT8_MAP_PATH)},\n'
    '        "unit_8_rights": {"path": rel(UNIT8_RIGHTS_PATH), "sha256": digest(UNIT8_RIGHTS_PATH)},\n'
    '        "unit_8_asset_closure": {"path": rel(UNIT8_ASSET_CLOSURE_PATH), "sha256": digest(UNIT8_ASSET_CLOSURE_PATH)},\n',
)

# Unit 7 is now the frozen cumulative baseline.  Apply these suppressions only
# after the inherited template has been transformed, so its Unit 8 additions
# and authority bindings above remain intact while no Unit 7 stable ID is
# emitted a second time.
source, _source_file_count = re.subn(
    r'NEW_SOURCE_FILES = \[.*?\n\]\n\nREQUIRED_CLASSES',
    'NEW_SOURCE_FILES = [\n'
    '    ROOT / "source" / "id-ID" / "frontmatter-units-01-08.md",\n'
    '    ROOT / "source" / "id-ID" / "lecture-08.md",\n'
    '    ROOT / "source" / "id-ID" / "worksheet-08.md",\n'
    '    ROOT / "source" / "id-ID" / "worksheet-08-solutions.md",\n'
    '    ROOT / "source" / "id-ID" / "media-credits-unit-08.md",\n'
    ']\n\nREQUIRED_CLASSES',
    source,
    count=1,
    flags=re.DOTALL,
)
if _source_file_count != 1:
    raise SystemExit("Unit 8 source-file closure transformation drift")
source, _concept_count = re.subn(
    r'NEW_CONCEPTS = \{.*?\n\}\n\n',
    'NEW_CONCEPTS = {}\n\n',
    source,
    count=1,
    flags=re.DOTALL,
)
if _concept_count != 1:
    raise SystemExit("Unit 8 concept closure transformation drift")

unit8_correction_block = """new_correction_ids = [
    "AGC-CORR-0020",
    "AGC-CORR-0021",
    "AGC-ADAPT-0017",
    "AGC-ADAPT-0018",
    "AGC-ADAPT-0019",
    "AGC-ADAPT-0020",
]
new_correction_rows = [
    row for row in read_csv(CORRECTIONS_PATH)
    if row["correction_id"] in set(new_correction_ids)
]
if [row["correction_id"] for row in new_correction_rows] != new_correction_ids:
    raise SystemExit("Unit 8 correction/adaptation rows are missing or out of order")
correction_targets = {
    "AGC-CORR-0020": ["br-ak-2025-2026-l08"],
    "AGC-CORR-0021": ["br-ak-2025-2026-l08-lem-01-proof"],
    "AGC-ADAPT-0017": ["br-ak-2025-2026-l08"],
    "AGC-ADAPT-0018": ["br-ak-2025-2026-l08"],
    "AGC-ADAPT-0019": ["br-ak-2025-2026-l08"],
    "AGC-ADAPT-0020": ["agc-media-credits-unit-08"],
}
"""
source, _correction_block_count = re.subn(
    r'new_correction_ids = \[.*?\nfor row in new_correction_rows:',
    unit8_correction_block + 'for row in new_correction_rows:',
    source,
    count=1,
    flags=re.DOTALL,
)
if _correction_block_count != 1:
    raise SystemExit("Unit 8 correction block transformation drift")
source, _solution_block_count = re.subn(
    r'unit7_solution_entries = \{.*?\n\}\n',
    'unit7_solution_entries = {}\n',
    source,
    count=1,
    flags=re.DOTALL,
)
if _solution_block_count != 1:
    raise SystemExit("Unit 7 solution suppression transformation drift")
source, _rights_block_count = re.subn(
    r'unit7_rights_rows = read_csv\(UNIT7_RIGHTS_PATH\).*?\n\nunit8_rights_rows = read_csv\(UNIT8_RIGHTS_PATH\)',
    'unit7_rights_rows = []\n\nunit8_rights_rows = read_csv(UNIT8_RIGHTS_PATH)',
    source,
    count=1,
    flags=re.DOTALL,
)
if _rights_block_count != 1:
    raise SystemExit("Unit 7 rights suppression transformation drift")
source, _architecture_block_count = re.subn(
    r'architecture_correction = apply_architecture_correction\(\n'
    r'    root=ROOT,\n'
    r'    records=records,\n'
    r'    timestamp=timestamp,\n'
    r'\)\n'
    r'migrated_baseline_ids\.update\(\n'
    r'    row\["stable_id"\] for row in architecture_correction\["changed_existing_records"\]\n'
    r'\)',
    'architecture_correction = json.loads((BASELINE / "MANIFEST.json").read_text(encoding="utf-8")).get("architecture_correction", {})\n'
    'if architecture_correction.get("required_bgk_relation_id") != "relation.units0107.architecture-bgk-required":\n'
    '    raise SystemExit("Unit 7 architecture correction witness is absent from the frozen baseline")\n'
    'migrated_baseline_ids.update(\n'
    '    row["stable_id"] for row in architecture_correction.get("changed_existing_records", [])\n'
    ')',
    source,
    count=1,
    flags=re.DOTALL,
)
if _architecture_block_count != 1:
    raise SystemExit("Unit 7 architecture carry-forward transformation drift")
'''
outer = outer.replace(marker, post + "\n" + marker, 1)
exec(compile(outer, str(Path(__file__).resolve()), "exec"), globals())
