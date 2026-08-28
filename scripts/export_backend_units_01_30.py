#!/usr/bin/env python3
"""Extend the byte-frozen Units 1--28 native backend through Unit 30.

This bounded specializer materializes the accepted Unit 28 exporter without
executing it, pins every accepted Unit 28 backend byte as the baseline, and
admits only Units 29 and 30. Set AG_BRIDGE_SPECIALIZE_ONLY=1 to compile the
final exporter in memory without writing backend artifacts.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import os
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "export_backend_units_01_28.py"
TEMPLATE_SHA256 = "3fd09178c8ba92bdd6087ee321e41320760d8df4c12560000c94b1b954b2cee4"
BASELINE_MANIFEST_SHA256 = "52ce204f9f0843bb8c7598a66073699ba2a139d29cfa741d8dc6a0d509a9c4a2"
BASELINE_RECORDS_SHA256 = "94e9c9d0859fc30cfa46a9cc08ed2babb7db07b586a3b5985a91130b096261ef"
BASELINE_RECORD_COUNT = 21358


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 30 exporter specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


def materialize_unit28() -> str:
    """Capture the accepted generated Unit 28 exporter without running it."""

    if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
        raise SystemExit("Accepted Unit 28 exporter template is absent or has drifted")
    previous = os.environ.get("AG_BRIDGE_SPECIALIZE_ONLY")
    os.environ["AG_BRIDGE_SPECIALIZE_ONLY"] = "1"
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            captured = runpy.run_path(str(TEMPLATE), run_name="unit28_exporter_capture")
    finally:
        if previous is None:
            os.environ.pop("AG_BRIDGE_SPECIALIZE_ONLY", None)
        else:
            os.environ["AG_BRIDGE_SPECIALIZE_ONLY"] = previous
    generated = captured.get("generated")
    if not isinstance(generated, str):
        raise SystemExit("Accepted Unit 28 exporter did not yield its generated implementation")
    return generated


generated = materialize_unit28()

# Advance cumulative output identities. The accepted Unit 28 baseline is
# restored explicitly below after boundary-wide substitutions.
for old, new in (
    ("units-01-28", "units-01-30"),
    ("UNITS_01_28", "UNITS_01_30"),
    ("UNIT_28", "UNIT_30"),
    ("units0128", "units0130"),
    ("units_01_28", "units_01_30"),
    ("unit-28", "unit-30"),
    ("unit28", "unit30"),
    ("Unit 28", "Unit 30"),
    ("Units 1--28", "Units 1--30"),
):
    generated = generated.replace(old, new)

# Units 29 and 30 are the complete additive source boundary.
generated = replace_once(
    generated,
    'UNIT_30_QA_PATH = ROOT / "qa" / "UNIT_30_TRANSLATION_QA.json"\n',
    'UNIT_29_QA_PATH = ROOT / "qa" / "UNIT_29_TRANSLATION_QA.json"\n'
    'UNIT_30_QA_PATH = ROOT / "qa" / "UNIT_30_TRANSLATION_QA.json"\n',
)
if generated.count("range(28, 29)") != 6:
    raise SystemExit("Unit 30 exporter expected six Unit 28 source-range expressions")
generated = generated.replace("range(28, 29)", "range(29, 31)")
generated = replace_once(
    generated,
    "UNIT_QA_PATHS = {28: UNIT_30_QA_PATH}",
    "UNIT_QA_PATHS = {29: UNIT_29_QA_PATH, 30: UNIT_30_QA_PATH}",
)
generated = replace_once(
    generated,
    "len(SOURCE_FILES) == 5 and len({rel(path) for path in SOURCE_FILES}) == 5",
    "len(SOURCE_FILES) == 9 and len({rel(path) for path in SOURCE_FILES}) == 9",
)
generated = replace_once(
    generated,
    "    UNIT_30_QA_PATH,\n    *authority_paths,",
    "    UNIT_29_QA_PATH,\n    UNIT_30_QA_PATH,\n    *authority_paths,",
)

# Unit 30's authority freezer uses the newer compact closure schema. Normalize
# that read-only authority evidence in memory to the established native-backend
# projection; neither the authority files nor the source translation are
# rewritten.
generated = replace_once(
    generated,
    '    asset_closures[unit] = json.loads(spec["closure"].read_text(encoding="utf-8"))\n'
    '    manifest = authority_manifests[unit]\n',
    '    asset_closures[unit] = json.loads(spec["closure"].read_text(encoding="utf-8"))\n'
    '    closure_assets = {row["asset_id"]: row for row in asset_closures[unit].get("assets", [])}\n'
    '    for reader_order, rights_row in enumerate(rights_rows[unit], start=1):\n'
    '        authority_asset = closure_assets.get(rights_row["asset_id"])\n'
    '        require(authority_asset is not None, f"Unit {unit} rights asset is absent from the asset closure: {rights_row[\'asset_id\']}")\n'
    '        suffix = Path(rights_row["local_path"]).suffix.casefold()\n'
    '        derived_mime = {".png": "image/png", ".svg": "image/svg+xml", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif"}.get(suffix, "application/octet-stream")\n'
    '        defaults = {\n'
    '            "reader_order": reader_order,\n'
    '            "resource_title": authority_asset.get("source_title") or authority_asset.get("metadata_title"),\n'
    '            "metadata_title": authority_asset.get("source_title") or authority_asset.get("metadata_title"),\n'
    '            "original_url": authority_asset.get("source_url") or authority_asset.get("original_url"),\n'
    '            "selected_url": authority_asset.get("selected_url") or authority_asset.get("source_url"),\n'
    '            "selected_form": authority_asset.get("selected_form") or "original",\n'
    '            "local_width": authority_asset.get("width") or authority_asset.get("local_width"),\n'
    '            "local_height": authority_asset.get("height") or authority_asset.get("local_height"),\n'
    '            "frame_count": authority_asset.get("frame_count") or 1,\n'
    '            "mime": authority_asset.get("mime") or derived_mime,\n'
    '            "credit": authority_asset.get("source_credit") or authority_asset.get("credit") or "",\n'
    '            "usage_terms": authority_asset.get("license_evidence") or authority_asset.get("license_short") or "",\n'
    '            "license_url": authority_asset.get("license_url") or "",\n'
    '        }\n'
    '        for key, value in defaults.items():\n'
    '            if not rights_row.get(key):\n'
    '                rights_row[key] = str(value)\n'
    '    manifest = authority_manifests[unit]\n',
)
generated = replace_once(
    generated,
    '    require(manifest.get("unit_number") == unit, f"Unit {unit} authority manifest identity mismatch")',
    '    require((manifest.get("unit_number") or manifest.get("unit")) == unit, f"Unit {unit} authority manifest identity mismatch")',
)
# Pandoc figure attributes are part of the accessibility-preserving Unit 29-30
# source syntax; the accepted parser previously recognized only a bare image.
generated = replace_once(
    generated,
    '        image_match = re.fullmatch(r"!\\[[^\\]]*\\]\\(([^)]+)\\)", content)',
    '        image_match = re.fullmatch(r"!\\[[^\\]]*\\]\\(([^)]+)\\)(?:\\{[^}]*\\})?", content)',
)
generated = replace_once(
    generated,
    '    spec["media_count"] = closure_payload["reader_media_positions"]',
    '    spec["media_count"] = closure_payload.get("reader_media_positions", sum(int(row.get("reader_positions", 1)) for row in closure_payload.get("assets", [])))',
)
generated = replace_once(
    generated,
    '    spec["binary_surfaces"] = closure_payload["unique_local_assets"]',
    '    spec["binary_surfaces"] = closure_payload.get("unique_local_assets", len(closure_payload.get("assets", [])))',
)
generated = replace_once(
    generated,
    '    require(asset_closures[unit].get("reader_media_positions") == spec["media_count"], f"Unit {unit} media-position count mismatch")',
    '    require(asset_closures[unit].get("reader_media_positions", sum(int(row.get("reader_positions", 1)) for row in asset_closures[unit].get("assets", []))) == spec["media_count"], f"Unit {unit} media-position count mismatch")',
)
generated = replace_once(
    generated,
    '    require(asset_closures[unit].get("unique_local_assets") == spec["binary_surfaces"], f"Unit {unit} local-asset count mismatch")',
    '    require(asset_closures[unit].get("unique_local_assets", len(asset_closures[unit].get("assets", []))) == spec["binary_surfaces"], f"Unit {unit} local-asset count mismatch")',
)

# Pin the complete accepted Unit 28 backend as the immutable byte baseline.
generated = replace_once(
    generated,
    'BASELINE = ROOT / "backend" / "units-01-27"',
    'BASELINE = ROOT / "backend" / "units-01-28"',
)
generated = replace_once(
    generated,
    'BASELINE_MANIFEST_SHA256 = "b176a5ab161cc440ffae65fcd341828732970404bc22035b84eeb88edb0a781a"',
    f'BASELINE_MANIFEST_SHA256 = "{BASELINE_MANIFEST_SHA256}"',
)
generated = replace_once(
    generated,
    'BASELINE_RECORDS_SHA256 = "e12321f1c4724dac486ef7512462888647f2c3b30ae6a5d40022329dfa2a28f1"',
    f'BASELINE_RECORDS_SHA256 = "{BASELINE_RECORDS_SHA256}"',
)
generated = replace_once(
    generated,
    "BASELINE_RECORD_COUNT = 20570",
    f"BASELINE_RECORD_COUNT = {BASELINE_RECORD_COUNT}",
)
generated = replace_once(
    generated,
    'PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-27.2026-08-26"',
    'PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-28.2026-08-26"',
)
generated = replace_once(
    generated,
    'CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-30.2026-08-26"',
    'CUMULATIVE_EDITION = "edition.algebraic-geometry-bridge-id.units-01-30.2026-08-28"',
)
generated = generated.replace("backend/units-01-27", "backend/units-01-28")
generated = generated.replace("Units 1--27", "Units 1--28")
generated = generated.replace("units_01_27", "units_01_28")

# Correct inherited prose so the materialized implementation describes this
# two-unit boundary and the exact frozen baseline.
generated = generated.replace("Every one of its\n8,491 canonical JSONL records", "Every one of its\n21,358 canonical JSONL records")
generated = generated.replace("reader/source structures for Unit 30", "reader/source structures for Units 29--30")
generated = generated.replace("The script is intentionally fail-closed. It will not write the Unit 30", "The script is intentionally fail-closed. It will not write the Unit 30")
generated = generated.replace("identify the through-Unit-15 reader", "identify the through-Unit-30 reader")
generated = generated.replace("the Unit 30 translation boundary froze its", "the Units 29--30 translation boundary froze their")
generated = generated.replace("Unit 30 terminology bindings overlap", "Units 29--30 terminology bindings overlap")
generated = generated.replace("Unit 30 terminology ledger rows absent", "Units 29--30 terminology ledger rows absent")
generated = generated.replace("Unit 30 correction bindings overlap", "Units 29--30 correction bindings overlap")
generated = generated.replace("Unit 30 correction ledger rows absent", "Units 29--30 correction ledger rows absent")
generated = generated.replace("A Unit 30 correction target", "A Units 29--30 correction target")
generated = generated.replace("unit_28_authority_formula_exercise_solution_media_fidelity", "unit_30_authority_formula_exercise_solution_media_fidelity")
generated = generated.replace('"unit_28_source_hashes_match_reader_receipt"', '"units_29_30_source_hashes_match_reader_receipt"')
generated = generated.replace('"unit_28_terminology_and_correction_ledger_closure"', '"units_29_30_terminology_and_correction_ledger_closure"')

# Advance only cumulative runtime and emitted boundary fields.
if generated.count('get("through_unit") == 28') != 2:
    raise SystemExit("Unit 30 exporter expected two through_unit=28 runtime gates")
generated = generated.replace('get("through_unit") == 28', 'get("through_unit") == 30')
if generated.count('"through_unit": 28') != 3:
    raise SystemExit("Unit 30 exporter expected three emitted through_unit=28 fields")
generated = generated.replace('"through_unit": 28', '"through_unit": 30')

for residue in (
    "range(28, 29)",
    "UNIT_28_QA_PATH",
    "UNIT_28_TRANSLATION_QA.json",
    "2025-2026-l29",
    "2025-2026-w29",
    "2025-2026-l30",
    "2025-2026-w30",
):
    if residue in generated:
        raise SystemExit(f"Unit 30 exporter retained stale specialization residue: {residue}")

if os.environ.get("AG_BRIDGE_SPECIALIZE_ONLY") == "1":
    compile(generated, str(TEMPLATE), "exec")
    print("Unit 30 exporter specialization: COMPILE PASS")
else:
    namespace = {
        "__file__": str(Path(__file__).resolve()),
        "__name__": "__main__",
        "TEMPLATE_EXPORTER": TEMPLATE,
    }
    exec(compile(generated, str(TEMPLATE), "exec"), namespace)
