#!/usr/bin/env python3
"""Export the deterministic cumulative native backend through Unit 9.

This is a narrow replay adapter over the audited Unit 8 exporter.  The Unit 8
JSONL is the frozen baseline; only Unit 9 source, authority, QA, and reader
artifacts are added here.  The two-stage source replay keeps the exporter
logic in one place while making the Unit 8 byte-preservation boundary explicit.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "export_backend_units_01_08.py"


def _replay_unit8_source() -> str:
    """Materialize the Unit 8 transform without executing its file writes."""

    wrapper_marker = 'exec(compile(outer, str(Path(__file__).resolve()), "exec"), globals())'
    inner_marker = 'exec(compile(source, str(Path(__file__).resolve()), "exec"), globals())'
    wrapper = TEMPLATE.read_text(encoding="utf-8")
    if wrapper.count(wrapper_marker) != 1:
        raise SystemExit("Unit 8 wrapper final marker drift")
    wrapper = wrapper.replace(wrapper_marker, "generated_wrapper = outer", 1)
    namespace: dict[str, object] = {"__file__": str(TEMPLATE), "__name__": "__unit8_wrapper__"}
    exec(compile(wrapper, str(TEMPLATE), "exec"), namespace)
    generated_wrapper = namespace.get("generated_wrapper")
    if not isinstance(generated_wrapper, str) or generated_wrapper.count(inner_marker) != 1:
        raise SystemExit("Unit 8 inner exporter final marker drift")
    generated_wrapper = generated_wrapper.replace(inner_marker, "generated_inner = source", 1)
    inner_namespace: dict[str, object] = {
        "__file__": str(TEMPLATE),
        "__name__": "__unit8_inner_exporter__",
    }
    exec(compile(generated_wrapper, str(TEMPLATE), "exec"), inner_namespace)
    source = inner_namespace.get("generated_inner")
    if not isinstance(source, str):
        raise SystemExit("Unit 8 inner exporter was not materialized")
    return source


source = _replay_unit8_source()


def _replace(old: str, new: str, expected: int = 1) -> None:
    global source
    count = source.count(old)
    if count != expected:
        raise SystemExit(f"Unit 9 exporter template drift for {old!r}: expected {expected}, found {count}")
    source = source.replace(old, new)


# Carry the complete Unit 8 export forward as an exact baseline.
_replace('BASELINE = ROOT / "backend" / "units-01-07"', 'BASELINE = ROOT / "backend" / "units-01-08"')
_replace('OUT = ROOT / "backend" / "units-01-08"', 'OUT = ROOT / "backend" / "units-01-09"')
_replace(
    'BASELINE_MANIFEST_SHA256 = "8b482971c444a4e5d90695f084234924a873b671885428d98e9db447e4924967"',
    'BASELINE_MANIFEST_SHA256 = "__UNIT8_MANIFEST_SHA256__"',
)
_replace(
    'BASELINE_RECORDS_SHA256 = "663713a128a0e673a4daf9edd67f9c3dd10ebae02039f8e0c2044c0ca0fa14be"',
    'BASELINE_RECORDS_SHA256 = "7ac2d40a553741648ef3e5136802247cd3004ea41e3733496aabb0d7c273f973"',
)
_replace(
    'BASELINE_SCHEMA_SHA256 = "fed2bc176f438e9ab2053b21c67f9ac3feac391ccd83f5c70107a1f86f994b8b"',
    'BASELINE_SCHEMA_SHA256 = "8c98c4999faabe8356129f6b5de0a8482022ebd04c315b673e2a7cbfbacbb917"',
)
_replace('BASELINE_RECORD_COUNT = 5182', 'BASELINE_RECORD_COUNT = 5787')
_replace(
    'PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-07.2026-08-22"',
    'PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-08.2026-08-23"',
)
_replace(
    'CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-08.2026-08-23"',
    'CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-09.2026-08-23"',
)
_replace('source_local_id="units-01-08"', 'source_local_id="units-01-09"')
_replace('build_receipt.get("through_unit") != 8', 'build_receipt.get("through_unit") != 9')
_replace('"through_unit": 8', '"through_unit": 9', expected=2)
_replace('"algebraic-geometry-bridge-id-units-01-08.pdf"', '"algebraic-geometry-bridge-id-units-01-09.pdf"')
_replace('"cumulative Units 1--8"', '"cumulative Units 1--9"', expected=1)
_replace('through Units 1--8', 'through Units 1--9')
_replace('qa.units0108', 'qa.units0109', expected=4)
_replace('qa.unit08.protected', 'qa.unit09.protected')
_replace('UNITS_01_08_MACHINE_QA.json', 'UNITS_01_09_MACHINE_QA.json')
_replace('UNITS_01_08_VISUAL_QA.json', 'UNITS_01_09_VISUAL_QA.json')
_replace('UNITS_01_08_RESPONSIVE_QA.json', 'UNITS_01_09_RESPONSIVE_QA.json')
_replace('UNIT_08_PROTECTED_SURFACES.json', 'UNIT_09_PROTECTED_SURFACES.json')
_replace('"units_01_07_baseline_manifest_sha256"', '"units_01_08_baseline_manifest_sha256"')
_replace('"units_01_07_baseline": {', '"units_01_08_baseline": {')
_replace('"backend/units-01-07/MANIFEST.json"', '"backend/units-01-08/MANIFEST.json"')
_replace('"backend/units-01-07/records.jsonl"', '"backend/units-01-08/records.jsonl"')
_replace('"unit_01_07_baseline_carried_forward"', '"unit_01_08_baseline_carried_forward"')

# Unit 8's source/authority additions are already in BASELINE.  Suppress those
# replay additions and replace them with the five Unit 9 reader files.
source, _count = re.subn(
    r"NEW_SOURCE_FILES = \[.*?\n\]",
    'NEW_SOURCE_FILES = [\n'
    '    ROOT / "source" / "id-ID" / "frontmatter-units-01-09.md",\n'
    '    ROOT / "source" / "id-ID" / "lecture-09.md",\n'
    '    ROOT / "source" / "id-ID" / "worksheet-09.md",\n'
    '    ROOT / "source" / "id-ID" / "worksheet-09-solutions.md",\n'
    '    ROOT / "source" / "id-ID" / "media-credits-unit-09.md",\n'
    "]",
    source,
    count=1,
    flags=re.DOTALL,
)
if _count != 1:
    raise SystemExit("Unit 9 source-file closure transformation drift")

source, _count = re.subn(
    r'new_correction_ids = \[.*?\nfor row in new_correction_rows:',
    'new_correction_ids = []\n'
    'new_correction_rows = []\n'
    'correction_targets = {}\n'
    'for row in new_correction_rows:',
    source,
    count=1,
    flags=re.DOTALL,
)
if _count != 1:
    raise SystemExit("Unit 8 correction suppression transformation drift")

source, _count = re.subn(
    r'unit8_solution_entries = \{.*?\n\}\n',
    'unit8_solution_entries = {}\n\n'
    'unit9_solution_entries = {\n'
    '    int(row["exercise_number"]): row\n'
    '    for row in unit9_map["entries"]\n'
    '    if row.get("has_public_solution")\n'
    '}\n',
    source,
    count=1,
    flags=re.DOTALL,
)
if _count != 1:
    raise SystemExit("Unit 8 solution suppression transformation drift")

source, _count = re.subn(
    r'unit8_rights_rows = read_csv\(UNIT8_RIGHTS_PATH\).*?\nall_unit_records =',
    'unit8_rights_rows = []\n\n'
    'unit9_rights_rows = read_csv(UNIT9_RIGHTS_PATH)\n'
    'if len(unit9_rights_rows) != 1:\n'
    '    raise SystemExit("Unit 9 rights closure does not contain one position")\n'
    'for row in unit9_rights_rows:\n'
    '    component_rights_id = f"rights.{row[\'asset_id\']}"\n'
    '    add(make_record("rights", component_rights_id, source_local_id=row["metadata_title"], resource_id=BRENNER_RESOURCE, edition_id=CUMULATIVE_EDITION, source_locator=row["description_url"], content_sha256=row["local_sha256"], payload={"license": row["license_short"], "license_url": row["license_url"] or None, "usage_terms": row["usage_terms"] or None, "creator_or_artist": row["artist"] or row["uploader"], "uploader": row["uploader"], "attribution_required": row["attribution_required"].lower() == "true", "scope": row["asset_id"]}))\n'
    '    add(make_record("asset", row["asset_id"], source_local_id=row["resource_title"], parent_id=image_parent_by_path.get(row["local_path"], "br-ak-2025-2026-l09"), order=int(row["reader_order"]), path=row["local_path"], resource_id=BRENNER_RESOURCE, edition_id=CUMULATIVE_EDITION, source_locator=row["description_url"], content_sha256=row["local_sha256"], translation_state="built", rights_id=component_rights_id, payload={"caption_id": row.get("reader_caption_id") or row["asset_id"], "selected_form": row["selected_form"], "bytes": int(row["local_bytes"]), "width": int(row["local_width"]), "height": int(row["local_height"]), "mime": row["mime"], "source_original_url": row["original_url"], "selected_url": row["selected_url"], "pdf_companion": ({"path": row["pdf_local_path"], "bytes": int(row["pdf_local_bytes"]), "sha256": row["pdf_local_sha256"]} if row["pdf_local_path"] else None)}))\n'
    'all_unit_records =',
    source,
    count=1,
    flags=re.DOTALL,
)
if _count != 1:
    raise SystemExit("Unit 8 rights suppression transformation drift")

# Add Unit 9 authority witnesses before the inherited Unit 7 validation.
authority9_block = '''AUTHORITY_MANIFEST9_PATH = ROOT / "authority" / "wikiversity" / "unit-09" / "UNIT_AUTHORITY_MANIFEST.json"
UNIT9_MAP_PATH = ROOT / "authority" / "wikiversity" / "unit-09" / "ORDERED_EXERCISE_MAP.json"
UNIT9_RIGHTS_PATH = ROOT / "authority" / "RIGHTS-unit-09.csv"
UNIT9_ASSET_CLOSURE_PATH = ROOT / "authority" / "ASSET_CLOSURE-unit-09.json"
authority_manifest9 = json.loads(AUTHORITY_MANIFEST9_PATH.read_text(encoding="utf-8"))
unit9_map = json.loads(UNIT9_MAP_PATH.read_text(encoding="utf-8"))
if authority_manifest9.get("unit_number") != 9 or unit9_map.get("exercise_count") != 24 or unit9_map.get("solution_count") != 3:
    raise SystemExit("Unit 9 authority closure mismatch")
'''
marker = 'if authority_manifest.get("unit_number") != 7:\n'
if source.count(marker) != 1:
    raise SystemExit("Unit 9 authority insertion marker drift")
source = source.replace(marker, authority9_block + marker, 1)

# The inherited source-provenance dispatch remains available for old records;
# Unit 9 gets an explicit manifest/map witness and public-solution mapping.
unit9_provenance = '''\n\ndef source_provenance_unit9(source_path: Path, metadata: dict[str, str], identifier: str) -> dict[str, Any]:
    editorial = source_path.name in {"frontmatter-units-01-09.md", "media-credits-unit-09.md"}
    result: dict[str, Any] = {
        "source_edition_id": None if editorial else BRENNER_EDITION,
        "unit_9_authority_manifest": {"path": rel(AUTHORITY_MANIFEST9_PATH), "sha256": digest(AUTHORITY_MANIFEST9_PATH)},
    }
    if source_path.name == "lecture-09.md":
        result["upstream"] = compact_upstream(authority_manifest9["lecture"])
    elif source_path.name == "worksheet-09.md":
        result["upstream"] = compact_upstream(authority_manifest9["worksheet"])
    elif source_path.name == "worksheet-09-solutions.md":
        match = re.search(r"-sol-(\\d+)$", identifier)
        result["exercise_solution_map"] = {"path": rel(UNIT9_MAP_PATH), "sha256": digest(UNIT9_MAP_PATH), "worksheet_revid": unit9_map["worksheet"]["revid"]}
        result["upstream"] = compact_upstream(unit9_solution_entries[int(match.group(1))]) if match else compact_upstream(unit9_map["worksheet"])
    else:
        result["upstream"] = {key: metadata[key] for key in ("upstream_title", "upstream_pageid", "upstream_revid", "upstream_timestamp", "upstream_mediawiki_sha1", "source_url") if key in metadata}
    return result
'''
marker = 'all_new_units: list[dict[str, Any]] = []\n'
if source.count(marker) != 1:
    raise SystemExit("Unit 9 provenance insertion marker drift")
source = source.replace(marker, unit9_provenance + "\n" + marker, 1)

old_dispatch = 'provenance=(source_provenance_unit8(source_path, metadata, identifier) if source_path.name in {"frontmatter-units-01-08.md", "lecture-08.md", "worksheet-08.md", "worksheet-08-solutions.md", "media-credits-unit-08.md"} else source_provenance(source_path, metadata, identifier)),'
new_dispatch = 'provenance=(source_provenance_unit9(source_path, metadata, identifier) if source_path.name in {"frontmatter-units-01-09.md", "lecture-09.md", "worksheet-09.md", "worksheet-09-solutions.md", "media-credits-unit-09.md"} else source_provenance_unit8(source_path, metadata, identifier) if source_path.name in {"frontmatter-units-01-08.md", "lecture-08.md", "worksheet-08.md", "worksheet-08-solutions.md", "media-credits-unit-08.md"} else source_provenance(source_path, metadata, identifier)), '
_replace(old_dispatch, new_dispatch.rstrip(), expected=1)
old_dispatch_active = 'provenance=(source_provenance_unit8(source_path, metadata, active_id) if source_path.name in {"frontmatter-units-01-08.md", "lecture-08.md", "worksheet-08.md", "worksheet-08-solutions.md", "media-credits-unit-08.md"} else source_provenance(source_path, metadata, active_id)),'
new_dispatch_active = 'provenance=(source_provenance_unit9(source_path, metadata, active_id) if source_path.name in {"frontmatter-units-01-09.md", "lecture-09.md", "worksheet-09.md", "worksheet-09-solutions.md", "media-credits-unit-09.md"} else source_provenance_unit8(source_path, metadata, active_id) if source_path.name in {"frontmatter-units-01-08.md", "lecture-08.md", "worksheet-08.md", "worksheet-08-solutions.md", "media-credits-unit-08.md"} else source_provenance(source_path, metadata, active_id)),'
_replace(old_dispatch_active, new_dispatch_active, expected=1)

# Select the Unit 9 map for its typed solution projection.
old_solution_branch = '''        if "-w08-sol-" in unit["stable_id"]:
            solution_map_path, solution_entries = UNIT8_MAP_PATH, unit8_solution_entries
        else:
            solution_map_path, solution_entries = UNIT7_MAP_PATH, unit7_solution_entries
'''
new_solution_branch = '''        if "-w09-sol-" in unit["stable_id"]:
            solution_map_path, solution_entries = UNIT9_MAP_PATH, unit9_solution_entries
        elif "-w08-sol-" in unit["stable_id"]:
            solution_map_path, solution_entries = UNIT8_MAP_PATH, unit8_solution_entries
        else:
            solution_map_path, solution_entries = UNIT7_MAP_PATH, unit7_solution_entries
'''
_replace(old_solution_branch, new_solution_branch, expected=1)

# Bind Unit 9 artifacts and authority files while retaining the inherited
# Unit 7/8 witnesses in the new manifest for reproducibility.
_replace(
    '    ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-09.pdf",\n'
    '    BUILD_RECEIPT_PATH,',
    '    ROOT / "build" / "reader-id" / "algebraic-geometry-bridge-id-units-01-09.pdf",\n'
    '    BUILD_RECEIPT_PATH,',
    expected=1,
)
artifact_marker = '    UNIT8_ASSET_CLOSURE_PATH,\n]'
if source.count(artifact_marker) != 1:
    raise SystemExit("Unit 9 artifact insertion marker drift")
source = source.replace(
    artifact_marker,
    '    UNIT8_ASSET_CLOSURE_PATH,\n'
    '    AUTHORITY_MANIFEST9_PATH,\n'
    '    UNIT9_MAP_PATH,\n'
    '    UNIT9_RIGHTS_PATH,\n'
    '    UNIT9_ASSET_CLOSURE_PATH,\n]',
    1,
)

# The source-binding list has the same authority additions as artifact_paths;
# include the Unit 9 QA script in place of the inherited reader-QA wrapper.
_replace('ROOT / "scripts" / "qa_reader_units_01_08.py",', 'ROOT / "scripts" / "qa_reader_units_01_09.py",')
source_binding_marker = '    UNIT8_ASSET_CLOSURE_PATH,\n    CORRECTIONS_PATH,'
if source.count(source_binding_marker) != 1:
    raise SystemExit("Unit 9 source-binding insertion marker drift")
source = source.replace(
    source_binding_marker,
    '    UNIT8_ASSET_CLOSURE_PATH,\n'
    '    AUTHORITY_MANIFEST9_PATH,\n'
    '    UNIT9_MAP_PATH,\n'
    '    UNIT9_RIGHTS_PATH,\n'
    '    UNIT9_ASSET_CLOSURE_PATH,\n'
    '    CORRECTIONS_PATH,',
    1,
)

# Add Unit 9 solution/media relations.  The inherited Unit 8 loops are empty
# because Unit 8 is already part of the frozen baseline.
relation_marker = 'for typed in typed_records:\n'
if source.count(relation_marker) != 1:
    raise SystemExit("Unit 9 relation insertion marker drift")
unit9_relations = '''for exercise_number in sorted(unit9_solution_entries):
    add_relation("solves", f"br-ak-2025-2026-w09-sol-{exercise_number:02d}", f"br-ak-2025-2026-w09-ex-{exercise_number:02d}", source_locator=rel(UNIT9_MAP_PATH))
for row in unit9_rights_rows:
    add_relation("illustrates", row["asset_id"], image_parent_by_path.get(row["local_path"], "br-ak-2025-2026-l09"), source_locator=row["description_url"])
for exercise_number in sorted(unit9_solution_entries):
    add_relation("solves", f"solution.br-ak-2025-2026-w09-sol-{exercise_number:02d}", f"exercise.br-ak-2025-2026-w09-ex-{exercise_number:02d}", source_locator=rel(UNIT9_MAP_PATH), payload={"typed_family_projection": True})
'''
source = source.replace(relation_marker, unit9_relations + relation_marker, 1)

_replace('artifact.units0108.', 'artifact.units0109.')
_replace('relation.units0108.', 'relation.units0109.')
_replace(
    '"unit_8_asset_closure": {"path": rel(UNIT8_ASSET_CLOSURE_PATH), "sha256": digest(UNIT8_ASSET_CLOSURE_PATH)},\n',
    '"unit_8_asset_closure": {"path": rel(UNIT8_ASSET_CLOSURE_PATH), "sha256": digest(UNIT8_ASSET_CLOSURE_PATH)},\n'
    '        "unit_9_manifest": {"path": rel(AUTHORITY_MANIFEST9_PATH), "sha256": digest(AUTHORITY_MANIFEST9_PATH)},\n'
    '        "unit_9_exercise_map": {"path": rel(UNIT9_MAP_PATH), "sha256": digest(UNIT9_MAP_PATH)},\n'
    '        "unit_9_rights": {"path": rel(UNIT9_RIGHTS_PATH), "sha256": digest(UNIT9_RIGHTS_PATH)},\n'
    '        "unit_9_asset_closure": {"path": rel(UNIT9_ASSET_CLOSURE_PATH), "sha256": digest(UNIT9_ASSET_CLOSURE_PATH)},\n',
    expected=1,
)
_replace(
    'frozen Unit 7 cumulative baseline carried forward',
    'frozen Unit 8 cumulative baseline carried forward',
    expected=1,
)
_replace('"units_01_07_stable_ids_preserved": BASELINE_RECORD_COUNT', '"units_01_08_stable_ids_preserved": BASELINE_RECORD_COUNT')

source = source.replace('__UNIT8_MANIFEST_SHA256__', 'PLACEHOLDER_UNIT8_MANIFEST_SHA256')

# Execute the transformed inner exporter.  The placeholder is replaced at
# runtime below after a bounded hash read, so a stale baseline cannot pass.
unit8_manifest_path = ROOT / "backend" / "units-01-08" / "MANIFEST.json"
import hashlib

baseline_hash = hashlib.sha256(unit8_manifest_path.read_bytes()).hexdigest()
source = source.replace('PLACEHOLDER_UNIT8_MANIFEST_SHA256', baseline_hash)
exec(compile(source, str(Path(__file__).resolve()), "exec"), globals())
