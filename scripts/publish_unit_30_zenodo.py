#!/usr/bin/env python3
"""Publish the verified Unit 30 classical volume in the existing Zenodo lineage.

This bounded adapter specializes the byte-pinned, accepted Unit 28 publisher.
Credentials remain runtime-only; --self-check and --preflight do not read
them, and publication receipts contain only sanitized handling flags.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "publish_unit_28_zenodo.py"
TEMPLATE_SHA256 = "afcdc99fdac78294e2c6e7b0d4736d41833b869e98d343f3874ee61ceb90f7a7"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 30 Zenodo specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


def materialize_unit28_implementation() -> str:
    if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
        raise SystemExit("Accepted Unit 28 Zenodo publisher is absent or has drifted")
    source = TEMPLATE.read_text(encoding="utf-8")
    marker = '\nnamespace = {"__file__":'
    if source.count(marker) != 1:
        raise SystemExit("Could not isolate the accepted Unit 28 Zenodo builder")
    builder = source[: source.index(marker)]
    namespace = {"__file__": str(TEMPLATE), "__name__": "unit28_builder_capture"}
    exec(compile(builder, str(TEMPLATE), "exec"), namespace)
    generated = namespace.get("generated")
    if not isinstance(generated, str):
        raise SystemExit("Accepted Unit 28 Zenodo builder yielded no implementation")
    return generated


generated = materialize_unit28_implementation()
for old, new in (
    ("Units 1–28", "Units 1–30"),
    ("Unit 1–28", "Unit 1–30"),
    ("Units 24–28", "Units 24–30"),
    ("Unit 24–28", "Unit 24–30"),
    ("units_24_28", "units_24_30"),
):
    generated = generated.replace(old, new)

for old, new in (
    ("units-01-28", "units-01-30"),
    ("UNITS_01_28", "UNITS_01_30"),
    ("UNIT_28", "UNIT_30"),
    ("unit-28", "unit-30"),
    ("unit_28", "unit_30"),
    ("unit28", "unit30"),
    ("Unit 28", "Unit 30"),
):
    generated = generated.replace(old, new)

generated = replace_once(generated, "EXPECTED_UNITS = 28", "EXPECTED_UNITS = 30")
if generated.count("22104692") != 3:
    raise SystemExit("Accepted Unit 28 Zenodo predecessor bindings have drifted")
generated = generated.replace("22104692", "22105836")
generated = generated.replace("Unit 27 record 22105836", "Unit 28 record 22105836")

# The completed release advances directly from the public Unit 28 record and
# therefore must explicitly retain Unit 29 as well as Unit 28 in its archive
# contract after the mechanical latest-unit substitution.
for suffix in ("lecture-29.md", "worksheet-29.md", "worksheet-29-solutions.md"):
    unit28_suffix = suffix.replace("-29", "-28")
    unit30_suffix = suffix.replace("-29", "-30")
    generated = replace_once(
        generated,
        f'f"{{prefix}}source/id-ID/{unit28_suffix}"',
        f'f"{{prefix}}source/id-ID/{suffix}",\n'
        f'            f"{{prefix}}source/id-ID/{unit30_suffix}"',
    )
generated = replace_once(
    generated,
    '            f"{prefix}qa/UNIT_27_TRANSLATION_QA.json",\n'
    '            f"{prefix}qa/UNIT_30_TRANSLATION_QA.json",',
    '            f"{prefix}qa/UNIT_27_TRANSLATION_QA.json",\n'
    '            f"{prefix}qa/UNIT_28_TRANSLATION_QA.json",\n'
    '            f"{prefix}qa/UNIT_29_TRANSLATION_QA.json",\n'
    '            f"{prefix}qa/UNIT_30_TRANSLATION_QA.json",',
)
generated = replace_once(
    generated,
    '            f"{prefix}00_control/UNIT_27_WORKLOG.md",\n'
    '            f"{prefix}00_control/UNIT_30_WORKLOG.md",',
    '            f"{prefix}00_control/UNIT_27_WORKLOG.md",\n'
    '            f"{prefix}00_control/UNIT_28_WORKLOG.md",\n'
    '            f"{prefix}00_control/UNIT_29_WORKLOG.md",\n'
    '            f"{prefix}00_control/UNIT_30_WORKLOG.md",',
)
generated = replace_once(
    generated,
    'f"Checkpoint parsial ini memuat 28 kuliah, 28 lembar kerja, {exercises} soal, "',
    'f"Edisi klasik lengkap ini memuat 30 kuliah, 30 lembar kerja, {exercises} soal, "',
)

generated = replace_once(
    generated,
    '    require_equal(coverage.get("full_edition_complete"), False, "coverage completion flag")',
    '    require_equal(coverage.get("classical_volume_complete"), True, "classical completion flag")\n'
    '    require_equal(coverage.get("full_edition_complete"), False, "two-volume completion flag")',
)
if generated.count('            "full_edition_complete": False,') != 2:
    raise SystemExit("Accepted Unit 28 publisher completion fields have drifted")
generated = generated.replace(
    '            "full_edition_complete": False,',
    '            "classical_volume_complete": True,\n'
    '            "full_edition_complete": False,',
)

# Unit 30's official PDF endpoints returned HTTP 429; the semantic closure and
# exact PDF metadata are frozen, but no nonexistent binary is required from the
# authority ZIP.  Units 1–29 retain their complete local PDF witnesses.
pdf_range = 'for number in range(1, EXPECTED_UNITS + 1)\n    )'
if generated.count(pdf_range) != 2:
    raise SystemExit("Accepted Unit 28 publisher PDF-witness loops have drifted")
generated = generated.replace(
    pdf_range,
    'for number in range(1, EXPECTED_UNITS)\n    )',
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
