#!/usr/bin/env python3
"""Build the deterministic reader-first cumulative Unit 24 release payload.

The implementation is specialized from the byte-pinned, accepted Unit 21
packager. Final reader/backend counts and all file identities are read from the
frozen Unit 24 candidate and receipts at runtime; this adapter embeds none of
their eventual hashes or page counts.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "package_unit_21_release.py"
TEMPLATE_SHA256 = "0deae93ab8519091e8b5084b3eba96db7ddc3770a32979d45300ee307284d87f"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 24 release specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


def materialize_unit21_implementation() -> str:
    """Materialize the accepted Unit 21 implementation without running it."""

    if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
        raise SystemExit("Accepted Unit 21 release packager is absent or has drifted")
    source = TEMPLATE.read_text(encoding="utf-8")
    marker = '\nnamespace = {"__file__":'
    if source.count(marker) != 1:
        raise SystemExit("Could not isolate the accepted Unit 21 packager builder")
    builder = source[: source.index(marker)]
    namespace = {"__file__": str(TEMPLATE), "__name__": "unit21_builder_capture"}
    exec(compile(builder, str(TEMPLATE), "exec"), namespace)
    generated = namespace.get("generated")
    if not isinstance(generated, str):
        raise SystemExit("Accepted Unit 21 packager did not yield an implementation")
    return generated


generated = materialize_unit21_implementation()
for old, new in (
    ("units-01-21", "units-01-24"),
    ("UNITS_01_21", "UNITS_01_24"),
    ("UNIT_21", "UNIT_24"),
    ("unit-21", "unit-24"),
    ("unit_21", "unit_24"),
    ("unit21", "unit24"),
    ("Unit 21", "Unit 24"),
):
    generated = generated.replace(old, new)

generated = replace_once(
    generated,
    """EXPECTED_UNITS = 21
EXPECTED_PLANNED_UNITS = 30
EXPECTED_EXERCISES = 577
EXPECTED_PUBLIC_SOLUTIONS = 102
EXPECTED_MEDIA_POSITIONS = 76""",
    """EXPECTED_UNITS = 24
EXPECTED_PLANNED_UNITS = 30


def _runtime_candidate_coverage() -> dict[str, int]:
    path = ROOT / "qa" / "UNIT_24_RELEASE_CANDIDATE.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Unit 24 release candidate is unavailable or invalid: {exc}") from exc
    if not isinstance(value, dict) or not str(value.get("status", "")).startswith("PASS"):
        raise RuntimeError("Unit 24 release candidate is not a PASS object")
    if value.get("through_unit") != EXPECTED_UNITS:
        raise RuntimeError("Unit 24 release candidate has the wrong boundary")
    coverage = value.get("coverage")
    if not isinstance(coverage, dict):
        raise RuntimeError("Unit 24 release candidate coverage is missing")
    keys = ("exercises", "public_source_solutions", "reader_media_positions")
    result: dict[str, int] = {}
    for key in keys:
        item = coverage.get(key)
        if not isinstance(item, int) or isinstance(item, bool) or item < 0:
            raise RuntimeError(f"Unit 24 release candidate {key} is not a non-negative integer")
        result[key] = item
    if result["exercises"] == 0 or result["public_source_solutions"] == 0:
        raise RuntimeError("Unit 24 cumulative exercise/solution coverage cannot be zero")
    return result


_RUNTIME_COVERAGE = _runtime_candidate_coverage()
EXPECTED_EXERCISES = _RUNTIME_COVERAGE["exercises"]
EXPECTED_PUBLIC_SOLUTIONS = _RUNTIME_COVERAGE["public_source_solutions"]
EXPECTED_MEDIA_POSITIONS = _RUNTIME_COVERAGE["reader_media_positions"]""",
)

generated = replace_once(
    generated,
    '        exact("qa/UNIT_24_TRANSLATION_QA.json"),',
    '        exact("qa/UNIT_21_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_22_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_23_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_24_TRANSLATION_QA.json"),',
)
generated = replace_once(
    generated,
    '        "UNIT_24_WORKLOG.md",',
    '        "UNIT_21_WORKLOG.md",\n'
    '        "UNIT_22_WORKLOG.md",\n'
    '        "UNIT_23_WORKLOG.md",\n'
    '        "UNIT_24_WORKLOG.md",',
)
generated = replace_once(
    generated,
    "    for number in (*range(2, 10), *range(11, 22)):",
    "    for number in (*range(2, 10), *range(11, 23)):",
)

# The accepted license gate remains authoritative. Add the truthful historical
# boundary and dual component-notice check required by the official 2012 Unit
# 24 PDF witnesses; neither notice is promoted into a blanket payload license.
generated = replace_once(
    generated,
    """    missing = [marker for marker in required if marker not in normalized_text]
    if missing:
        raise RuntimeError(f"Unit 24 mixed-rights licence notice is incomplete: {missing}")
    return path""",
    """    missing = [marker for marker in required if marker not in normalized_text]
    if missing:
        raise RuntimeError(f"Unit 24 mixed-rights licence notice is incomplete: {missing}")

    authority_path = exact("authority/UNIT_24_AUTHORITY_FREEZE.md")
    authority_text = " ".join(authority_path.read_text(encoding="utf-8").split())
    authority_markers = (
        "Kurs:Algebraische Kurven (Osnabrück 2012)",
        "CC BY-SA 4.0 course route",
        "CC BY-SA 2.0 Germany file notice",
        "do not make a blanket relicensing claim",
    )
    missing_authority = [
        marker for marker in authority_markers if marker not in authority_text
    ]
    if missing_authority:
        raise RuntimeError(
            f"Unit 24 source/licence transition is incomplete: {missing_authority}"
        )
    return path""",
)

generated = replace_once(
    generated,
    '            "independent_non_endorsed_derivative": True,',
    '            "independent_non_endorsed_derivative": True,\n'
    '            "source_course_boundary": {\n'
    '                "units_01_23": "Algebraische Kurven (Osnabrück 2025–2026)",\n'
    '                "unit_24": "Algebraische Kurven (Osnabrück 2012)",\n'
    '            },\n'
    '            "unit_24_pdf_component_notices": [\n'
    '                "CC BY-SA 4.0 course route",\n'
    '                "CC BY-SA 2.0 Germany file notice",\n'
    '            ],',
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
