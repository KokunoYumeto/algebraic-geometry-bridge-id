#!/usr/bin/env python3
"""Publish the verified Unit 28 checkpoint in the existing Zenodo lineage.

This bounded adapter specializes the byte-pinned, accepted Unit 27 publisher.
Credentials remain runtime-only; ``--self-check`` and ``--preflight`` do not
read them, and publication receipts contain only sanitized handling flags.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "publish_unit_27_zenodo.py"
TEMPLATE_SHA256 = "6a0eb4807f8ebb8dd03f526eeac8a74dccc802fb925afd70e2b84f5f09db243d"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 28 Zenodo specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


def materialize_unit27_implementation() -> str:
    if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
        raise SystemExit("Accepted Unit 27 Zenodo publisher is absent or has drifted")
    source = TEMPLATE.read_text(encoding="utf-8")
    marker = '\nnamespace = {"__file__":'
    if source.count(marker) != 1:
        raise SystemExit("Could not isolate the accepted Unit 27 Zenodo builder")
    builder = source[: source.index(marker)]
    namespace = {"__file__": str(TEMPLATE), "__name__": "unit27_builder_capture"}
    exec(compile(builder, str(TEMPLATE), "exec"), namespace)
    generated = namespace.get("generated")
    if not isinstance(generated, str):
        raise SystemExit("Accepted Unit 27 Zenodo builder yielded no implementation")
    return generated


generated = materialize_unit27_implementation()
for old, new in (
    ("Units 1–27", "Units 1–28"),
    ("Unit 1–27", "Unit 1–28"),
    ("Units 24–27", "Units 24–28"),
    ("Unit 24–27", "Unit 24–28"),
    ("units_24_27", "units_24_28"),
):
    generated = generated.replace(old, new)

for old, new in (
    ("units-01-27", "units-01-28"),
    ("UNITS_01_27", "UNITS_01_28"),
    ("UNIT_27", "UNIT_28"),
    ("unit-27", "unit-28"),
    ("unit_27", "unit_28"),
    ("unit27", "unit28"),
    ("Unit 27", "Unit 28"),
):
    generated = generated.replace(old, new)

generated = replace_once(generated, "EXPECTED_UNITS = 27", "EXPECTED_UNITS = 28")
if generated.count("22102097") != 3:
    raise SystemExit("Accepted Unit 27 Zenodo predecessor bindings have drifted")
generated = generated.replace("22102097", "22104692")

for old, new in (
    ('f"{prefix}source/id-ID/lecture-27.md"', 'f"{prefix}source/id-ID/lecture-28.md"'),
    ('f"{prefix}source/id-ID/worksheet-27.md"', 'f"{prefix}source/id-ID/worksheet-28.md"'),
    (
        'f"{prefix}source/id-ID/worksheet-27-solutions.md"',
        'f"{prefix}source/id-ID/worksheet-28-solutions.md"',
    ),
    (
        'f"Checkpoint parsial ini memuat 27 kuliah, 27 lembar kerja, {exercises} soal, "',
        'f"Checkpoint parsial ini memuat 28 kuliah, 28 lembar kerja, {exercises} soal, "',
    ),
):
    generated = replace_once(generated, old, new)

# Keep the source archive validation contiguous after the latest-unit token
# substitution; Unit 27 remains accepted evidence and must not disappear.
generated = replace_once(
    generated,
    '            f"{prefix}qa/UNIT_26_TRANSLATION_QA.json",\n'
    '            f"{prefix}qa/UNIT_28_TRANSLATION_QA.json",',
    '            f"{prefix}qa/UNIT_26_TRANSLATION_QA.json",\n'
    '            f"{prefix}qa/UNIT_27_TRANSLATION_QA.json",\n'
    '            f"{prefix}qa/UNIT_28_TRANSLATION_QA.json",',
)
generated = replace_once(
    generated,
    '            f"{prefix}00_control/UNIT_26_WORKLOG.md",\n'
    '            f"{prefix}00_control/UNIT_28_WORKLOG.md",',
    '            f"{prefix}00_control/UNIT_26_WORKLOG.md",\n'
    '            f"{prefix}00_control/UNIT_27_WORKLOG.md",\n'
    '            f"{prefix}00_control/UNIT_28_WORKLOG.md",',
)

# A reserved Unit 28 draft must be a new version after the public Unit 27
# record.  The inherited implementation already verifies the live concept and
# latest-record relationship before it reserves or publishes.
generated = generated.replace(
    "A different Zenodo version became latest after record 22104692",
    "A different Zenodo version became latest after the Unit 27 record 22104692",
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
