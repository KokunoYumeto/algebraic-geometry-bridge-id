#!/usr/bin/env python3
"""Build the deterministic reader-first cumulative Unit 30 release payload.

This bounded adapter specializes the byte-pinned, accepted Unit 28 packager.
It preserves the existing GitHub and Zenodo lineages, records the completed
classical volume without claiming the full two-volume edition, and keeps
--self-check offline and non-writing.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "package_unit_28_release.py"
TEMPLATE_SHA256 = "048da93eafc6ecb814f3db8cf185c7f5d3e115f2cf9781fc62e9b90e43bd44d1"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 30 release specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


def materialize_unit28_implementation() -> str:
    if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
        raise SystemExit("Accepted Unit 28 release packager is absent or has drifted")
    source = TEMPLATE.read_text(encoding="utf-8")
    marker = '\nnamespace = {"__file__":'
    if source.count(marker) != 1:
        raise SystemExit("Could not isolate the accepted Unit 28 packager builder")
    builder = source[: source.index(marker)]
    namespace = {"__file__": str(TEMPLATE), "__name__": "unit28_builder_capture"}
    exec(compile(builder, str(TEMPLATE), "exec"), namespace)
    generated = namespace.get("generated")
    if not isinstance(generated, str):
        raise SystemExit("Accepted Unit 28 packager did not yield an implementation")
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
generated = replace_once(
    generated,
    "helpers.FIXED_ZIP_TIME = (2026, 8, 26, 0, 0, 0)",
    "helpers.FIXED_ZIP_TIME = (2026, 8, 28, 0, 0, 0)",
)
generated = replace_once(
    generated,
    '        "date-released": "2026-08-26",',
    '        "date-released": "2026-08-28",',
)
if generated.count("22104692") != 4:
    raise SystemExit("Accepted Unit 28 packager predecessor bindings have drifted")
generated = generated.replace("22104692", "22105836")
generated = generated.replace("Unit 27 predecessor DOI", "Unit 28 predecessor DOI")

# The Unit 28 implementation already carries Units 25–28.  Its latest-unit
# substitution turns Unit 28 into Unit 30, so restore both intervening units.
for stem in ("TRANSLATION_QA", "AUTHORITY_QA"):
    generated = replace_once(
        generated,
        f'        exact("qa/UNIT_27_{stem}.json"),\n'
        f'        exact("qa/UNIT_30_{stem}.json"),',
        f'        exact("qa/UNIT_27_{stem}.json"),\n'
        f'        exact("qa/UNIT_28_{stem}.json"),\n'
        f'        exact("qa/UNIT_29_{stem}.json"),\n'
        f'        exact("qa/UNIT_30_{stem}.json"),',
    )
generated = replace_once(
    generated,
    '        "UNIT_27_WORKLOG.md",\n'
    '        "UNIT_30_WORKLOG.md",',
    '        "UNIT_27_WORKLOG.md",\n'
    '        "UNIT_28_WORKLOG.md",\n'
    '        "UNIT_29_WORKLOG.md",\n'
    '        "UNIT_30_WORKLOG.md",',
)
generated = replace_once(
    generated,
    "    for number in (25, 26, 27, 28):",
    "    for number in (25, 26, 27, 28, 29, 30):",
)

generated = replace_once(
    generated,
    '    require_equal(backend.get("unit_27_records_preserved"), 20570, "release candidate Unit 27 baseline")',
    '    require_equal(backend.get("unit_28_records_preserved"), 21358, "release candidate Unit 28 baseline")\n'
    '    require_equal(candidate.get("classical_volume_complete"), True, "release candidate classical completion")\n'
    '    require_equal(candidate.get("full_two_volume_edition_complete"), False, "release candidate two-volume truth")',
)

for old, new in (
    ('        "28 dari 30 unit",', '        "30 dari 30 unit",'),
    ('        "671 soal",', '        "693 soal",'),
    ('        "118 solusi publik",', '        "122 solusi publik",'),
    ('        "98 posisi media",', '        "101 posisi media",'),
    ('        "PDF A4 476 halaman",', '        "PDF A4 504 halaman",'),
):
    generated = replace_once(generated, old, new)

generated = replace_once(
    generated,
    '        "RIGHTS-unit-27.csv",\n'
    '        "RIGHTS-unit-30.csv",',
    '        "RIGHTS-unit-27.csv",\n'
    '        "RIGHTS-unit-28.csv",\n'
    '        "RIGHTS-unit-29.csv",\n'
    '        "RIGHTS-unit-30.csv",',
)

# The release manifest keeps the broader two-volume edition incomplete while
# making the completed classical-volume boundary explicit.
if generated.count('            "full_edition_complete": False,') != 2:
    raise SystemExit("Accepted Unit 28 packager completion fields have drifted")
generated = generated.replace(
    '            "full_edition_complete": False,',
    '            "classical_volume_complete": True,\n'
    '            "full_edition_complete": False,',
)

# Unit 30's official 2012 PDF endpoints returned HTTP 429 during the bounded
# authority capture.  Their exact page/byte/source-SHA1 metadata is frozen in
# the Unit 30 manifest, but no local binary or SHA-256 was invented.  Package
# all extant Unit 1–29 PDF witnesses and the complete Unit 30 semantic closure.
generated = replace_once(
    generated,
    '*[f"lecture-{number:02d}-official.pdf" for number in range(1, EXPECTED_UNITS + 1)],',
    '*[f"lecture-{number:02d}-official.pdf" for number in range(1, EXPECTED_UNITS)],',
)
generated = replace_once(
    generated,
    '*[f"worksheet-{number:02d}-official.pdf" for number in range(1, EXPECTED_UNITS + 1)],',
    '*[f"worksheet-{number:02d}-official.pdf" for number in range(1, EXPECTED_UNITS)],',
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
