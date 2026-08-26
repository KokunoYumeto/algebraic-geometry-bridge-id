#!/usr/bin/env python3
"""Extend the byte-frozen Units 1--27 native backend through Unit 28.

This bounded specializer materializes the accepted Unit 27 exporter without
executing it, pins every accepted Unit 27 backend byte as the baseline, and
admits only Unit 28. Set AG_BRIDGE_SPECIALIZE_ONLY=1 to compile the final
exporter in memory without writing backend artifacts.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import os
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "export_backend_units_01_27.py"
TEMPLATE_SHA256 = "b09ae6121d7905c234026e9cb93af1101f56155c6732fdf40712bad16c3168e8"
BASELINE_MANIFEST_SHA256 = "b176a5ab161cc440ffae65fcd341828732970404bc22035b84eeb88edb0a781a"
BASELINE_RECORDS_SHA256 = "e12321f1c4724dac486ef7512462888647f2c3b30ae6a5d40022329dfa2a28f1"
BASELINE_RECORD_COUNT = 20570


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 28 exporter specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


def materialize_unit27() -> str:
    """Capture the accepted generated Unit 27 exporter without running it."""

    if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
        raise SystemExit("Accepted Unit 27 exporter template is absent or has drifted")
    previous = os.environ.get("AG_BRIDGE_SPECIALIZE_ONLY")
    os.environ["AG_BRIDGE_SPECIALIZE_ONLY"] = "1"
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            captured = runpy.run_path(str(TEMPLATE), run_name="unit27_exporter_capture")
    finally:
        if previous is None:
            os.environ.pop("AG_BRIDGE_SPECIALIZE_ONLY", None)
        else:
            os.environ["AG_BRIDGE_SPECIALIZE_ONLY"] = previous
    generated = captured.get("generated")
    if not isinstance(generated, str):
        raise SystemExit("Accepted Unit 27 exporter did not yield its generated implementation")
    return generated


generated = materialize_unit27()

# Advance cumulative output identities. The accepted Unit 27 baseline is
# restored explicitly below after these boundary-wide substitutions.
for old, new in (
    ("units-01-27", "units-01-28"),
    ("UNITS_01_27", "UNITS_01_28"),
    ("UNIT_27", "UNIT_28"),
    ("units0127", "units0128"),
    ("units_01_27", "units_01_28"),
    ("unit-27", "unit-28"),
    ("unit27", "unit28"),
    ("Unit 27", "Unit 28"),
    ("Units 1--27", "Units 1--28"),
    ("Units 25--27", "Unit 28"),
    ("Unit 25--27", "Unit 28"),
    ("units_25_27", "unit_28"),
    ("unit_25_27", "unit_28"),
):
    generated = generated.replace(old, new)

# Unit 28 is the sole additive source boundary.
generated = replace_once(
    generated,
    'UNIT_25_QA_PATH = ROOT / "qa" / "UNIT_25_TRANSLATION_QA.json"\n'
    'UNIT_26_QA_PATH = ROOT / "qa" / "UNIT_26_TRANSLATION_QA.json"\n',
    "",
)
generated = generated.replace("range(25, 28)", "range(28, 29)")
generated = replace_once(
    generated,
    "UNIT_QA_PATHS = {25: UNIT_25_QA_PATH, 26: UNIT_26_QA_PATH, 27: UNIT_28_QA_PATH}",
    "UNIT_QA_PATHS = {28: UNIT_28_QA_PATH}",
)
generated = replace_once(
    generated,
    "len(SOURCE_FILES) == 13 and len({rel(path) for path in SOURCE_FILES}) == 13",
    "len(SOURCE_FILES) == 5 and len({rel(path) for path in SOURCE_FILES}) == 5",
)
generated = replace_once(
    generated,
    "    UNIT_25_QA_PATH,\n    UNIT_26_QA_PATH,\n    UNIT_28_QA_PATH,",
    "    UNIT_28_QA_PATH,",
)
generated = generated.replace(
    "three independent translation workers froze their", "the Unit 28 translation boundary froze its"
)

# Unit 28's frozen worksheet identifiers use ``ex01`` ... ``ex14`` (while
# the solution keeps ``sol-10``). Accept both established spellings without
# rewriting a single source identifier.
generated = replace_once(
    generated,
    're.search(r"-w\\d{2}-ex-\\d+$", identifier)',
    're.search(r"-w\\d{2}-ex-?\\d+$", identifier)',
)
generated = replace_once(
    generated,
    're.search(rf"-w{unit:02d}-ex-(\\d+)$", row["stable_id"])',
    're.search(rf"-w{unit:02d}-ex-?(\\d+)$", row["stable_id"])',
)
generated = replace_once(
    generated,
    're.search(r"-(?:ex|sol)-(\\d+)$", unit_record["stable_id"])',
    're.search(r"-(?:ex-?|sol-)(\\d+)$", unit_record["stable_id"])',
)
generated = replace_once(
    generated,
    're.search(rf"-{family}{unit:02d}-{kind}-{number:02d}$", identifier)',
    're.search(rf"-{family}{unit:02d}-{kind}-?{number:02d}$", identifier)',
)

# Pin the complete accepted Unit 27 backend as the immutable byte baseline.
generated = replace_once(
    generated,
    'BASELINE = ROOT / "backend" / "units-01-24"',
    'BASELINE = ROOT / "backend" / "units-01-27"',
)
generated = replace_once(
    generated,
    'BASELINE_MANIFEST_SHA256 = "46ed6d1dc2629cd5303a38c972dff9fc885255fe3443374feafee8ecc07dd70a"',
    f'BASELINE_MANIFEST_SHA256 = "{BASELINE_MANIFEST_SHA256}"',
)
generated = replace_once(
    generated,
    'BASELINE_RECORDS_SHA256 = "b2550dc11285eec35e1e08eef58284fcf5d88ea9206eabac9fd4b921df43f0c7"',
    f'BASELINE_RECORDS_SHA256 = "{BASELINE_RECORDS_SHA256}"',
)
generated = replace_once(
    generated,
    "BASELINE_RECORD_COUNT = 18488",
    f"BASELINE_RECORD_COUNT = {BASELINE_RECORD_COUNT}",
)
generated = replace_once(
    generated,
    'PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-24.2026-08-25"',
    'PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-27.2026-08-26"',
)
generated = generated.replace("backend/units-01-24", "backend/units-01-27")
generated = generated.replace("Units 1--24", "Units 1--27")
generated = generated.replace("units_01_24", "units_01_27")

# Advance only cumulative runtime and emitted boundary fields.
if generated.count('get("through_unit") == 27') != 2:
    raise SystemExit("Unit 28 exporter expected two through_unit=27 runtime gates")
generated = generated.replace('get("through_unit") == 27', 'get("through_unit") == 28')
if generated.count('"through_unit": 27') != 3:
    raise SystemExit("Unit 28 exporter expected three emitted through_unit=27 fields")
generated = generated.replace('"through_unit": 27', '"through_unit": 28')

if "UNIT_25_QA_PATH" in generated or "UNIT_26_QA_PATH" in generated:
    raise SystemExit("Unit 28 exporter retained a prior-boundary translation-QA path")
if "2025-2026-l28" in generated or "2025-2026-w28" in generated:
    raise SystemExit("Unit 28 exporter retained the wrong source-edition namespace")

if os.environ.get("AG_BRIDGE_SPECIALIZE_ONLY") == "1":
    compile(generated, str(TEMPLATE), "exec")
    print("Unit 28 exporter specialization: COMPILE PASS")
else:
    namespace = {
        "__file__": str(Path(__file__).resolve()),
        "__name__": "__main__",
        "TEMPLATE_EXPORTER": TEMPLATE,
    }
    exec(compile(generated, str(TEMPLATE), "exec"), namespace)
