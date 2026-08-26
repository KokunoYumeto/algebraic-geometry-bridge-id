#!/usr/bin/env python3
"""Build the deterministic reader-first cumulative Unit 28 release payload.

This bounded adapter specializes the byte-pinned, accepted Unit 27 packager.
All reader, backend, QA, reservation, and DOI facts are checked from the live
frozen receipts.  ``--self-check`` is offline and does not write a release.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "package_unit_27_release.py"
TEMPLATE_SHA256 = "28ff9a31d5cbd117b63cf666529d0728726acd247ea8c9aebcc120541fcd0bd5"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 28 release specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


def materialize_unit27_implementation() -> str:
    if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
        raise SystemExit("Accepted Unit 27 release packager is absent or has drifted")
    source = TEMPLATE.read_text(encoding="utf-8")
    marker = '\nnamespace = {"__file__":'
    if source.count(marker) != 1:
        raise SystemExit("Could not isolate the accepted Unit 27 packager builder")
    builder = source[: source.index(marker)]
    namespace = {"__file__": str(TEMPLATE), "__name__": "unit27_builder_capture"}
    exec(compile(builder, str(TEMPLATE), "exec"), namespace)
    generated = namespace.get("generated")
    if not isinstance(generated, str):
        raise SystemExit("Accepted Unit 27 packager did not yield an implementation")
    return generated


generated = materialize_unit27_implementation()

# Boundary phrases which are not covered by the filename/token substitutions.
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
    raise SystemExit("Accepted Unit 27 packager predecessor bindings have drifted")
generated = generated.replace("22102097", "22104692")

# Preserve the complete cumulative evidence closure after the mechanical latest-
# unit substitution, which would otherwise skip Unit 27.
generated = replace_once(
    generated,
    '        exact("qa/UNIT_26_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_28_TRANSLATION_QA.json"),',
    '        exact("qa/UNIT_26_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_27_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_28_TRANSLATION_QA.json"),',
)
generated = replace_once(
    generated,
    '        exact("qa/UNIT_26_AUTHORITY_QA.json"),\n'
    '        exact("qa/UNIT_28_AUTHORITY_QA.json"),',
    '        exact("qa/UNIT_26_AUTHORITY_QA.json"),\n'
    '        exact("qa/UNIT_27_AUTHORITY_QA.json"),\n'
    '        exact("qa/UNIT_28_AUTHORITY_QA.json"),',
)
generated = replace_once(
    generated,
    '        "UNIT_26_WORKLOG.md",\n'
    '        "UNIT_28_WORKLOG.md",',
    '        "UNIT_26_WORKLOG.md",\n'
    '        "UNIT_27_WORKLOG.md",\n'
    '        "UNIT_28_WORKLOG.md",',
)
generated = replace_once(
    generated,
    "    for number in (25, 26, 27):",
    "    for number in (25, 26, 27, 28):",
)

# The new backend must preserve the entire accepted Unit 27 dataset byte-for-
# byte, rather than falling back to the older Unit 24 baseline check.
generated = replace_once(
    generated,
    '    require_equal(backend.get("unit_24_records_preserved"), 18488, "release candidate Unit 24 baseline")',
    '    require_equal(backend.get("unit_27_records_preserved"), 20570, "release candidate Unit 27 baseline")',
)

# Public documentation is validated against the measured Unit 28 boundary and
# the reserved DOI at runtime.  The backend record count is intentionally not
# guessed before export.
generated = replace_once(
    generated,
    "def validate_public_docs() -> None:\n"
    '    readme = " ".join(exact("README.md").read_text(encoding="utf-8").split())',
    "def validate_public_docs(backend_records: int) -> None:\n"
    '    reservation_doi = load_json("qa/UNIT_28_ZENODO_RESERVATION.json").get("doi")\n'
    '    if not isinstance(reservation_doi, str) or not reservation_doi.startswith("10.5281/zenodo."):\n'
    '        raise RuntimeError("Unit 28 README cannot be checked without a valid reserved DOI")\n'
    '    if reservation_doi == "10.5281/zenodo.22104692":\n'
    '        raise RuntimeError("Unit 28 README reservation reuses the Unit 27 predecessor DOI")\n'
    '    readme = " ".join(exact("README.md").read_text(encoding="utf-8").split())',
)
for old, new in (
    ('        "27 dari 30 unit",', '        "28 dari 30 unit",'),
    ('        "657 soal",', '        "671 soal",'),
    ('        "117 solusi publik",', '        "118 solusi publik",'),
    ('        "94 posisi media",', '        "98 posisi media",'),
    ('        "PDF A4 464 halaman",', '        "PDF A4 476 halaman",'),
    ('        "20.570 rekaman",', '        f"{backend_records:,}".replace(",", ".") + " rekaman",'),
    ('        "10.5281/zenodo.22104692",', "        reservation_doi,"),
    ("    validate_public_docs()", "    validate_public_docs(backend_records)"),
):
    generated = replace_once(generated, old, new)

generated = replace_once(
    generated,
    '        "RIGHTS-unit-26.csv",\n'
    '        "RIGHTS-unit-28.csv",',
    '        "RIGHTS-unit-26.csv",\n'
    '        "RIGHTS-unit-27.csv",\n'
    '        "RIGHTS-unit-28.csv",',
)
generated = replace_once(
    generated,
    '        "RIGHTS-unit-28.csv",\n'
    '        "CC BY-SA 4.0 course route",\n'
    '        "CC BY-SA 2.0 Germany file notice",',
    '        "RIGHTS-unit-28.csv",\n'
    '        "CC BY-SA 4.0 print/course route",\n'
    '        "CC BY-SA 2.0 Germany file notice",',
)
generated = generated.replace(
    "Unit 28 citation reuses the Unit 24 predecessor DOI",
    "Unit 28 citation reuses the Unit 27 predecessor DOI",
)

# The source freeze proves which official 2012 route was frozen; the release
# licence notice, not that freeze note, is the authority for the cumulative
# payload's exact mixed-rights wording.  Keep both checks path-specific.
generated = replace_once(
    generated,
    '''    authority_path = exact("authority/UNIT_28_AUTHORITY_FREEZE.md")
    authority_text = " ".join(authority_path.read_text(encoding="utf-8").split())
    authority_markers = (
        "Kurs:Algebraische Kurven (Osnabrück 2012)",
        "CC BY-SA 4.0 print/course route",
        "CC BY-SA 2.0 Germany file notice",
        "make no blanket relicensing claim",
    )
    missing_authority = [
        marker for marker in authority_markers if marker not in authority_text
    ]
    if missing_authority:
        raise RuntimeError(
            f"Unit 28 source/licence transition is incomplete: {missing_authority}"
        )
    return path''',
    '''    authority_path = exact("authority/UNIT_28_AUTHORITY_FREEZE.md")
    authority_text = " ".join(authority_path.read_text(encoding="utf-8").split())
    authority_markers = ("Kurs:Algebraische Kurven (Osnabrück 2012)",)
    missing_authority = [
        marker for marker in authority_markers if marker not in authority_text
    ]
    if missing_authority:
        raise RuntimeError(
            f"Unit 28 frozen source-route evidence is incomplete: {missing_authority}"
        )

    release_rights_markers = (
        "CC BY-SA 4.0 print/course route",
        "CC BY-SA 2.0 Germany file notice",
        "make no blanket relicensing claim",
    )
    missing_release_rights = [
        marker for marker in release_rights_markers if marker not in normalized_text
    ]
    if missing_release_rights:
        raise RuntimeError(
            f"Unit 28 root LICENSE mixed-rights transition is incomplete: {missing_release_rights}"
        )
    return path''',
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
