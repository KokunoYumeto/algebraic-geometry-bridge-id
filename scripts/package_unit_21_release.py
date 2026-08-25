#!/usr/bin/env python3
"""Build the deterministic reader-first cumulative Unit 21 release payload."""

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
        raise SystemExit(
            f"Release specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
    raise SystemExit("Frozen Unit 15 release packager template is absent or has drifted")

generated = TEMPLATE.read_text(encoding="utf-8")
for old, new in (
    ("units-01-15", "units-01-21"),
    ("UNITS_01_15", "UNITS_01_21"),
    ("UNIT_15", "UNIT_21"),
    ("unit-15", "unit-21"),
    ("unit_15", "unit_21"),
    ("unit15", "unit21"),
    ("Unit 15", "Unit 21"),
):
    generated = generated.replace(old, new)

generated = replace_once(generated, "EXPECTED_UNITS = 15", "EXPECTED_UNITS = 21")
generated = replace_once(generated, "EXPECTED_EXERCISES = 423", "EXPECTED_EXERCISES = 577")
generated = replace_once(
    generated,
    "EXPECTED_PUBLIC_SOLUTIONS = 75",
    "EXPECTED_PUBLIC_SOLUTIONS = 102",
)
generated = replace_once(
    generated,
    "EXPECTED_MEDIA_POSITIONS = 69",
    "EXPECTED_MEDIA_POSITIONS = 76",
)
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

# Preserve the complete contiguous QA/worklog closure. Unit 19's owner gate is
# named INTEGRATION_QA because its source arrived through the bounded helper
# packet and was independently three-way reviewed before admission.
generated = replace_once(
    generated,
    '        exact("qa/UNIT_13_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_14_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_21_TRANSLATION_QA.json"),',
    '        exact("qa/UNIT_13_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_14_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_15_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_16_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_17_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_18_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_19_RELEASE_QA.json"),\n'
    '        exact("qa/UNIT_20_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_21_TRANSLATION_QA.json"),',
)
generated = replace_once(
    generated,
    '        "UNIT_13_WORKLOG.md",\n'
    '        "UNIT_14_WORKLOG.md",\n'
    '        "UNIT_21_WORKLOG.md",',
    '        "UNIT_13_WORKLOG.md",\n'
    '        "UNIT_14_WORKLOG.md",\n'
    '        "UNIT_15_WORKLOG.md",\n'
    '        "UNIT_16_WORKLOG.md",\n'
    '        "UNIT_17_WORKLOG.md",\n'
    '        "UNIT_18_WORKLOG.md",\n'
    '        "UNIT_19_WORKLOG.md",\n'
    '        "UNIT_20_WORKLOG.md",\n'
    '        "UNIT_21_WORKLOG.md",',
)
generated = replace_once(
    generated,
    '''    for directory in (
        "source/id-ID",
        "authority/assets",
        BACKEND_DIRECTORY,
        "backend/common-backend-v1-contract",
        "scripts",
    ):
        files.extend(compact_tree(directory))
    for control_name in (''',
    '''    for directory in (
        "source/id-ID",
        "authority/assets",
        BACKEND_DIRECTORY,
        "backend/common-backend-v1-contract",
        "scripts",
    ):
        files.extend(compact_tree(directory))
    # The private integration harness embeds a machine-local helper-packet path.
    # Its public, path-free QA derivative is selected explicitly above.
    files = [
        path
        for path in files
        if path.relative_to(ROOT).as_posix() != "scripts/qa_unit19_integration.py"
    ]
    for control_name in (''',
)
generated = replace_once(
    generated,
    "    for number in (*range(2, 10), 11, 12, 13, 14, 15):",
    "    for number in (*range(2, 10), *range(11, 22)):",
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
