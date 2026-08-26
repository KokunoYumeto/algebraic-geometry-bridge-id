#!/usr/bin/env python3
"""Publish the verified Unit 27 checkpoint in the existing Zenodo lineage.

This bounded adapter specializes the byte-pinned accepted Unit 24 publisher,
keeps credentials runtime-only, and preserves anonymous full-byte readback.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "publish_unit_24_zenodo.py"
TEMPLATE_SHA256 = "33baeed5c76373309bb676ce002fe9a36ce9265e987565b30f9d3d224af7357b"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 27 Zenodo specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


def materialize_unit24_implementation() -> str:
    if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
        raise SystemExit("Accepted Unit 24 Zenodo publisher is absent or has drifted")
    source = TEMPLATE.read_text(encoding="utf-8")
    marker = '\nnamespace = {"__file__":'
    if source.count(marker) != 1:
        raise SystemExit("Could not isolate the accepted Unit 24 Zenodo builder")
    builder = source[: source.index(marker)]
    namespace = {"__file__": str(TEMPLATE), "__name__": "unit24_builder_capture"}
    exec(compile(builder, str(TEMPLATE), "exec"), namespace)
    generated = namespace.get("generated")
    if not isinstance(generated, str):
        raise SystemExit("Accepted Unit 24 Zenodo builder yielded no implementation")
    return generated


generated = materialize_unit24_implementation()
for old, new in (
    ("units-01-24", "units-01-27"),
    ("UNITS_01_24", "UNITS_01_27"),
    ("UNIT_24", "UNIT_27"),
    ("unit-24", "unit-27"),
    ("unit_24", "unit_27"),
    ("unit24", "unit27"),
    ("Unit 1–24", "Unit 1–27"),
    ("Units 1–24", "Units 1–27"),
    ("Unit 24", "Unit 27"),
):
    generated = generated.replace(old, new)

generated = generated.replace("22088753", "22102097")
generated = replace_once(generated, "EXPECTED_UNITS = 24", "EXPECTED_UNITS = 27")

# The Unit 24 specialization used literal boundary sentinels and counts which
# are not covered by the token substitutions above.
for old, new in (
    ('f"{prefix}source/id-ID/lecture-24.md"', 'f"{prefix}source/id-ID/lecture-27.md"'),
    ('f"{prefix}source/id-ID/worksheet-24.md"', 'f"{prefix}source/id-ID/worksheet-27.md"'),
    (
        'f"{prefix}source/id-ID/worksheet-24-solutions.md"',
        'f"{prefix}source/id-ID/worksheet-27-solutions.md"',
    ),
    ('f"Checkpoint parsial ini memuat 24 kuliah, 24 lembar kerja, {exercises} soal, "',
     'f"Checkpoint parsial ini memuat 27 kuliah, 27 lembar kerja, {exercises} soal, "'),
):
    generated = replace_once(generated, old, new)

# Correct the historical-source scope after the mechanical boundary change.
generated = generated.replace(
    '"unit_27": "Algebraische Kurven (Osnabrück 2012)"',
    '"units_24_27": "Algebraische Kurven (Osnabrück 2012)"',
)
generated = generated.replace(
    '"unit_27_pdf_component_notices"',
    '"units_24_27_pdf_component_notices"',
)
generated = generated.replace(
    "Unit 27 mengikuti kuliah dan ",
    "Unit 24–27 mengikuti kuliah dan ",
)
generated = generated.replace(
    "Saksi PDF resmi Unit 27 mempertahankan",
    "Saksi PDF resmi Unit 24–27 mempertahankan",
)
generated = replace_once(
    generated,
    '            "Units 1–23 follow the official Osnabrück 2025–2026 course; Unit 27 follows "\n'
    '            "the official Osnabrück 2012 lecture and worksheet because the 2025–2026 "',
    '            "Units 1–23 follow the official Osnabrück 2025–2026 course; Units 24–27 follow "\n'
    '            "the official Osnabrück 2012 lectures and worksheets because the 2025–2026 "',
)
generated = replace_once(
    generated,
    '            "adapter, component-rights records, authority witnesses, and QA evidence. The "\n'
    '            "Unit 27 official PDF witnesses retain both the CC BY-SA 4.0 course-route and "',
    '            "adapter, component-rights records, authority witnesses, and QA evidence. The "\n'
    '            "official PDF witnesses for Units 24–27 retain both the CC BY-SA 4.0 course-route and "',
)
generated = generated.replace(
    '        "Unit 27",\n        "Osnabrück 2025–2026",',
    '        "Unit 24–27",\n        "Osnabrück 2025–2026",',
)
generated = replace_once(
    generated,
    '        "Units 1–27",\n        "independent, non-endorsed derivative",',
    '        "Units 1–27",\n        "Units 24–27",\n        "independent, non-endorsed derivative",',
)

# Require the whole new three-unit evidence closure inside the resumable
# source ZIP, not merely a single boundary sentinel.
generated = replace_once(
    generated,
    '            f"{prefix}qa/UNIT_27_RELEASE_CANDIDATE.json",\n'
    '            f"{prefix}LICENSE.md",',
    '            f"{prefix}qa/UNIT_25_TRANSLATION_QA.json",\n'
    '            f"{prefix}qa/UNIT_26_TRANSLATION_QA.json",\n'
    '            f"{prefix}qa/UNIT_27_TRANSLATION_QA.json",\n'
    '            f"{prefix}qa/UNIT_27_RELEASE_CANDIDATE.json",\n'
    '            f"{prefix}00_control/UNIT_25_WORKLOG.md",\n'
    '            f"{prefix}00_control/UNIT_26_WORKLOG.md",\n'
    '            f"{prefix}00_control/UNIT_27_WORKLOG.md",\n'
    '            f"{prefix}README.md",\n'
    '            f"{prefix}CITATION.cff",\n'
    '            f"{prefix}LICENSE.md",',
)

# The public record must be the exact reserved identity in this concept.
generated = replace_once(
    generated,
    '''def write_receipt(record: dict, verified: list[dict]) -> None:
    contract = validate_release_contract()
    public_metadata = record.get("metadata") or {}''',
    '''def write_receipt(record: dict, verified: list[dict]) -> None:
    contract = validate_release_contract()
    reservation = load_json(RESERVATION, "Zenodo reservation receipt")
    require_equal(int(record["id"]), reservation.get("record_id"), "public/reserved record ID")
    public_metadata = record.get("metadata") or {}
    require_equal(public_metadata.get("doi"), reservation.get("doi"), "public/reserved DOI")''',
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
