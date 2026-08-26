#!/usr/bin/env python3
"""Validate the Units 1--27 native backend against frozen Unit 24 bytes.

The accepted Unit 24 validator is materialized without execution and then
specialized only for the additive Units 25--27 boundary. Set
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
TEMPLATE = ROOT / "scripts" / "qa_backend_units_01_24.py"
TEMPLATE_SHA256 = "e186fc1d496227044ae21cf89f3371be1f26eef0d5e4974378cc90f5fcaa76c2"
BASELINE_MANIFEST_SHA256 = "46ed6d1dc2629cd5303a38c972dff9fc885255fe3443374feafee8ecc07dd70a"
BASELINE_RECORDS_SHA256 = "b2550dc11285eec35e1e08eef58284fcf5d88ea9206eabac9fd4b921df43f0c7"
BASELINE_RECORD_COUNT = 18488


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 27 backend-QA specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


def materialize_unit24() -> str:
    if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
        raise SystemExit("Accepted Unit 24 backend-QA template is absent or has drifted")
    previous = os.environ.get("AG_BRIDGE_SPECIALIZE_ONLY")
    os.environ["AG_BRIDGE_SPECIALIZE_ONLY"] = "1"
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            captured = runpy.run_path(str(TEMPLATE), run_name="unit24_backend_qa_capture")
    finally:
        if previous is None:
            os.environ.pop("AG_BRIDGE_SPECIALIZE_ONLY", None)
        else:
            os.environ["AG_BRIDGE_SPECIALIZE_ONLY"] = previous
    namespace = captured.get("namespace")
    generated = namespace.get("generated") if isinstance(namespace, dict) else None
    if not isinstance(generated, str):
        raise SystemExit("Accepted Unit 24 backend QA did not yield its generated implementation")
    return generated


generated = materialize_unit24()
for old, new in (
    ("units-01-24", "units-01-27"),
    ("UNITS_01_24", "UNITS_01_27"),
    ("UNIT_24", "UNIT_27"),
    ("units0124", "units0127"),
    ("units_01_24", "units_01_27"),
    ("unit-24", "unit-27"),
    ("unit24", "unit27"),
    ("Unit 24", "Unit 27"),
    ("Units 1--24", "Units 1--27"),
    ("Units 22--24", "Units 25--27"),
    ("Unit 22--24", "Unit 25--27"),
    ("units_22_24", "units_25_27"),
    ("unit_22_24", "unit_25_27"),
):
    generated = generated.replace(old, new)

generated = generated.replace("UNIT_22_QA_PATH", "UNIT_25_QA_PATH")
generated = generated.replace("UNIT_23_QA_PATH", "UNIT_26_QA_PATH")
generated = generated.replace("UNIT_22_TRANSLATION_QA.json", "UNIT_25_TRANSLATION_QA.json")
generated = generated.replace("UNIT_23_TRANSLATION_QA.json", "UNIT_26_TRANSLATION_QA.json")
generated = generated.replace("unit_22_translation", "unit_25_translation")
generated = generated.replace("unit_23_translation", "unit_26_translation")
generated = generated.replace("unit_24_translation", "unit_27_translation")
generated = generated.replace("range(22, 25)", "range(25, 28)")
generated = replace_once(
    generated,
    "UNIT_QA_PATHS = {22: UNIT_25_QA_PATH, 23: UNIT_26_QA_PATH, 24: UNIT_27_QA_PATH}",
    "UNIT_QA_PATHS = {25: UNIT_25_QA_PATH, 26: UNIT_26_QA_PATH, 27: UNIT_27_QA_PATH}",
)
generated = replace_once(
    generated,
    'edition_slug = "2012" if unit == 24 else "2025-2026"',
    'edition_slug = "2012"',
)
generated = replace_once(
    generated,
    'wrong_slug = "2025-2026" if unit == 24 else "2012"',
    'wrong_slug = "2025-2026"',
)

generated = replace_once(
    generated,
    'BASELINE = ROOT / "backend" / "units-01-21"',
    'BASELINE = ROOT / "backend" / "units-01-24"',
)
generated = replace_once(
    generated,
    'BASELINE_MANIFEST_SHA256 = "d2afc26b3c81c8b57e585c2a7bc4ac683a740403a527e9bfd203a88e45a3363d"',
    f'BASELINE_MANIFEST_SHA256 = "{BASELINE_MANIFEST_SHA256}"',
)
generated = replace_once(
    generated,
    'BASELINE_RECORDS_SHA256 = "ac9e40ad50e6dfdef977036999cebc5bc443d1064283c86eb30999b461a8872f"',
    f'BASELINE_RECORDS_SHA256 = "{BASELINE_RECORDS_SHA256}"',
)
generated = replace_once(
    generated,
    "BASELINE_RECORD_COUNT = 16114",
    f"BASELINE_RECORD_COUNT = {BASELINE_RECORD_COUNT}",
)
generated = replace_once(
    generated,
    'PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-21.2026-08-25"',
    'PREVIOUS_EDITION = "edition.algebraic-geometry-bridge-id.units-01-24.2026-08-25"',
)
generated = generated.replace("Units 1--21", "Units 1--24")
generated = generated.replace("Unit 21", "Unit 24")
generated = generated.replace("units_01_21", "units_01_24")
generated = generated.replace("backend/units-01-21", "backend/units-01-24")
generated = generated.replace('get("through_unit") == 24', 'get("through_unit") == 27')
generated = generated.replace('"through_unit": 24', '"through_unit": 27')
generated = generated.replace(
    "edition.algebraic-geometry-bridge-id.units-01-27.2026-08-25",
    "edition.algebraic-geometry-bridge-id.units-01-27.2026-08-26",
)
generated = generated.replace('"verified_date": "2026-08-25"', '"verified_date": "2026-08-26"')

if os.environ.get("AG_BRIDGE_SPECIALIZE_ONLY") == "1":
    compile(generated, str(TEMPLATE), "exec")
    print("Unit 27 backend-QA specialization: COMPILE PASS")
else:
    namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
    exec(compile(generated, str(TEMPLATE), "exec"), namespace)
