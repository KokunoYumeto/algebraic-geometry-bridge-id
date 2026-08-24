#!/usr/bin/env python3
"""Build the deterministic reader-first cumulative Unit 18 release payload."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "package_unit_15_release.py"
TEMPLATE_SHA256 = "90dbe56a4c0c0d4bc2086c1146a32493bb904940260840a9da7848dbff435168"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Release specialization expected one occurrence, found {count}: {old!r}")
    return text.replace(old, new, 1)


if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
    raise SystemExit("Frozen Unit 15 release packager template is absent or has drifted")

generated = TEMPLATE.read_text(encoding="utf-8")
for old, new in (
    ("units-01-15", "units-01-18"),
    ("UNITS_01_15", "UNITS_01_18"),
    ("UNIT_15", "UNIT_18"),
    ("unit-15", "unit-18"),
    ("unit_15", "unit_18"),
    ("unit15", "unit18"),
    ("Unit 15", "Unit 18"),
):
    generated = generated.replace(old, new)

generated = replace_once(generated, "EXPECTED_UNITS = 15", "EXPECTED_UNITS = 18")
generated = replace_once(generated, "EXPECTED_EXERCISES = 423", "EXPECTED_EXERCISES = 513")
generated = replace_once(generated, "EXPECTED_PUBLIC_SOLUTIONS = 75", "EXPECTED_PUBLIC_SOLUTIONS = 90")
generated = replace_once(generated, "EXPECTED_MEDIA_POSITIONS = 69", "EXPECTED_MEDIA_POSITIONS = 74")
generated = replace_once(
    generated,
    "helpers.FIXED_ZIP_TIME = (2026, 8, 24, 0, 0, 0)",
    "helpers.FIXED_ZIP_TIME = (2026, 8, 25, 0, 0, 0)",
)
generated = replace_once(
    generated,
    'require_equal(protected.get("unit"), EXPECTED_UNITS, "protected-surface QA unit")',
    'require_equal(protected.get("through_unit"), EXPECTED_UNITS, "protected-surface QA through_unit")',
)
generated = replace_once(
    generated,
    '''    require_equal(
        sum_unit_field(machine.get("solutions"), "exercise_count", "machine QA solutions"),
        EXPECTED_EXERCISES,
        "machine QA exercise total",
    )''',
    '''    require_equal(
        (machine.get("coverage") or {}).get("exercises"),
        EXPECTED_EXERCISES,
        "machine QA exercise total",
    )''',
)
generated = replace_once(
    generated,
    '''    require_equal(
        sum_unit_field(machine.get("solutions"), "solution_count", "machine QA solutions"),
        EXPECTED_PUBLIC_SOLUTIONS,
        "machine QA public-solution total",
    )''',
    '''    require_equal(
        (machine.get("coverage") or {}).get("public_source_solutions"),
        EXPECTED_PUBLIC_SOLUTIONS,
        "machine QA public-solution total",
    )''',
)
generated = replace_once(
    generated,
    '''    require_equal(
        sum_unit_field(machine.get("rights"), "positions", "machine QA rights"),
        EXPECTED_MEDIA_POSITIONS,
        "machine QA rights-position total",
    )''',
    '''    require_equal(
        (machine.get("coverage") or {}).get("reader_media_positions"),
        EXPECTED_MEDIA_POSITIONS,
        "machine QA rights-position total",
    )''',
)

# Keep the complete contiguous checkpoint QA/worklog closure, not only the
# terminal unit introduced by the mechanical version-name replacement.
generated = replace_once(
    generated,
    '        exact("qa/UNIT_14_TRANSLATION_QA.json"),\n        exact("qa/UNIT_18_TRANSLATION_QA.json"),',
    '        exact("qa/UNIT_14_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_15_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_16_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_17_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_18_TRANSLATION_QA.json"),',
)
generated = replace_once(
    generated,
    '        "UNIT_14_WORKLOG.md",\n        "UNIT_18_WORKLOG.md",',
    '        "UNIT_14_WORKLOG.md",\n'
    '        "UNIT_15_WORKLOG.md",\n'
    '        "UNIT_16_WORKLOG.md",\n'
    '        "UNIT_17_WORKLOG.md",\n'
    '        "UNIT_18_WORKLOG.md",',
)
generated = replace_once(
    generated,
    "    for number in (*range(2, 10), 11, 12, 13, 14, 15):",
    "    for number in (*range(2, 10), 11, 12, 13, 14, 15, 16, 17, 18):",
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
