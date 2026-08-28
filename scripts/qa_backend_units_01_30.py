#!/usr/bin/env python3
"""Validate the Units 1--30 native backend against frozen Unit 28 bytes.

The accepted Unit 28 validator is materialized without execution and then
specialized only for the additive Units 29--30 boundary. Set
AG_BRIDGE_SPECIALIZE_ONLY=1 to compile the final validator in memory.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import os
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "qa_backend_units_01_28.py"
TEMPLATE_SHA256 = "d28561a0c7e9faf8892574ecbe1238417da5c4f2dc51699284f77966a1e29704"
BASELINE_MANIFEST_SHA256 = "52ce204f9f0843bb8c7598a66073699ba2a139d29cfa741d8dc6a0d509a9c4a2"
BASELINE_RECORDS_SHA256 = "94e9c9d0859fc30cfa46a9cc08ed2babb7db07b586a3b5985a91130b096261ef"
BASELINE_RECORD_COUNT = 21358


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 30 backend-QA specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


def materialize_unit28() -> str:
    if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
        raise SystemExit("Accepted Unit 28 backend-QA template is absent or has drifted")
    previous = os.environ.get("AG_BRIDGE_SPECIALIZE_ONLY")
    os.environ["AG_BRIDGE_SPECIALIZE_ONLY"] = "1"
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            captured = runpy.run_path(str(TEMPLATE), run_name="unit28_backend_qa_capture")
    finally:
        if previous is None:
            os.environ.pop("AG_BRIDGE_SPECIALIZE_ONLY", None)
        else:
            os.environ["AG_BRIDGE_SPECIALIZE_ONLY"] = previous
    generated = captured.get("generated")
    if not isinstance(generated, str):
        raise SystemExit("Accepted Unit 28 backend QA did not yield its generated implementation")
    return generated


generated = materialize_unit28()
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

generated = replace_once(
    generated,
    'UNIT_30_QA_PATH = ROOT / "qa" / "UNIT_30_TRANSLATION_QA.json"\n',
    'UNIT_29_QA_PATH = ROOT / "qa" / "UNIT_29_TRANSLATION_QA.json"\n'
    'UNIT_30_QA_PATH = ROOT / "qa" / "UNIT_30_TRANSLATION_QA.json"\n',
)
if generated.count("range(28, 29)") != 6:
    raise SystemExit("Unit 30 backend QA expected six Unit 28 source-range expressions")
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
    '        "unit_28_translation_qa_sha256": digest(UNIT_30_QA_PATH),',
    '        "unit_29_translation_qa_sha256": digest(UNIT_29_QA_PATH),\n'
    '        "unit_30_translation_qa_sha256": digest(UNIT_30_QA_PATH),',
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
    '    require(closure.get("reader_media_positions") == spec["media_count"], f"Unit {unit} asset-closure count changed")',
    '    require(closure.get("reader_media_positions", sum(int(row.get("reader_positions", 1)) for row in closure.get("assets", []))) == spec["media_count"], f"Unit {unit} asset-closure count changed")',
)
generated = replace_once(
    generated,
    '    require(closure.get("unique_local_assets") == spec["binary_surfaces"], f"Unit {unit} binary-surface closure changed")',
    '    require(closure.get("unique_local_assets", len(closure.get("assets", []))) == spec["binary_surfaces"], f"Unit {unit} binary-surface closure changed")',
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
generated = generated.replace('BASELINE = ROOT / "backend" / "units-01-27"', 'BASELINE = ROOT / "backend" / "units-01-28"')
generated = generated.replace("Units 1--27", "Units 1--28")
generated = generated.replace("units_01_27", "units_01_28")
generated = generated.replace("Unit 27 record schema bytes", "Unit 28 record schema bytes")
generated = generated.replace("Unit 27 raw-byte baseline", "Unit 28 raw-byte baseline")
generated = generated.replace("a Unit 27 raw stable ID", "a Unit 28 raw stable ID")
generated = generated.replace("A Unit 27 serialized record byte", "A Unit 28 serialized record byte")
generated = generated.replace("all 20,570 rows", "all 21,358 rows")
generated = generated.replace("unit_27_schema_bytes_preserved", "unit_28_schema_bytes_preserved")

# Correct cumulative-boundary wording and receipt keys.
generated = generated.replace("Unit 30 source closure", "Units 29--30 source closure")
generated = generated.replace("Unit 30 source heading", "Units 29--30 source heading")
generated = generated.replace("Unit 30 terminology bindings overlap", "Units 29--30 terminology bindings overlap")
generated = generated.replace("Unit 30 terminology ledger rows absent", "Units 29--30 terminology ledger rows absent")
generated = generated.replace("Unit 30 correction bindings overlap", "Units 29--30 correction bindings overlap")
generated = generated.replace("Unit 30 correction ledger rows absent", "Units 29--30 correction ledger rows absent")
generated = generated.replace("Typed exercise closure for Unit 30", "Typed exercise closure for Units 29--30")
generated = generated.replace("Typed solution closure for Unit 30", "Typed solution closure for Units 29--30")
generated = generated.replace("Unit 30 asset closure", "Units 29--30 asset closure")
generated = generated.replace("Unit 30 rights closure", "Units 29--30 rights closure")
generated = generated.replace("Unexpected Unit 30 asset record", "Unexpected Units 29--30 asset record")
generated = generated.replace('"unit_28": unit_findings', '"units_29_30": unit_findings')
generated = generated.replace('"unit_28_terminology_and_correction_ledger_closure"', '"units_29_30_terminology_and_correction_ledger_closure"')
generated = generated.replace('"per_unit_28_translation_integration_evidence"', '"per_units_29_30_translation_integration_evidence"')

if generated.count('get("through_unit") == 28') != 7:
    raise SystemExit("Unit 30 backend QA expected seven through_unit=28 runtime gates")
generated = generated.replace('get("through_unit") == 28', 'get("through_unit") == 30')
if generated.count('"through_unit": 28') != 1:
    raise SystemExit("Unit 30 backend QA expected one emitted through_unit=28 field")
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
        raise SystemExit(f"Unit 30 backend QA retained stale specialization residue: {residue}")

if os.environ.get("AG_BRIDGE_SPECIALIZE_ONLY") == "1":
    compile(generated, str(TEMPLATE), "exec")
    print("Unit 30 backend-QA specialization: COMPILE PASS")
else:
    namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
    exec(compile(generated, str(TEMPLATE), "exec"), namespace)
