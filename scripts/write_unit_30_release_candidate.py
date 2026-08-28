#!/usr/bin/env python3
"""Freeze the fail-closed cumulative Unit 30 release candidate.

This bounded adapter specializes the byte-pinned Unit 28 candidate writer for
the completed 30-unit classical volume.  --self-check remains offline and
--write is the only mode that mutates the candidate receipt.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "write_unit_28_release_candidate.py"
TEMPLATE_SHA256 = "bb40a8daf595f6a8489ca8ffd632c817911ee9bc17628512db4e36e43092ca7f"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 30 candidate specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
    raise SystemExit("Accepted Unit 28 release-candidate writer is absent or has drifted")

generated = TEMPLATE.read_text(encoding="utf-8")

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

for old, new in (
    ("THROUGH_UNIT = 28", "THROUGH_UNIT = 30"),
    ("PREVIOUS_ZENODO_RECORD = 22104692", "PREVIOUS_ZENODO_RECORD = 22105836"),
    ('    "pdf_pages": 476,', '    "pdf_pages": 504,'),
    ('    "exercises": 671,', '    "exercises": 693,'),
    ('    "public_source_solutions": 118,', '    "public_source_solutions": 122,'),
    ('    "reader_media_positions": 98,', '    "reader_media_positions": 101,'),
    ('    "stable_source_ids": 1483,', '    "stable_source_ids": 1554,'),
    ('    "mathml_nodes": 10717,', '    "mathml_nodes": 11322,'),
    ('    "bytes": 15820212,', '    "bytes": 16019237,'),
    (
        '    "sha256": "181b6fba2b5441fb7a5ab76a512e9d9ee2300e4201fd4632cac20a70bc703df6",',
        '    "sha256": "6383d3b9804a059e76dc643da5974b8809649707e177ba191a69220fa7ea0e5d",',
    ),
    ('    "bytes": 23412216,', '    "bytes": 23805465,'),
    (
        '    "sha256": "b7cef9e6c08b696bde2f875a4766e6c35e975d4fd0901e414c3896014bbd9c10",',
        '    "sha256": "1ca69127dbbf8aa86d8d3f238488686a145ad2dd99ee417c329a5bd9516ca677",',
    ),
    ('    "bytes": 43674,', '    "bytes": 45373,'),
    (
        '    "sha256": "5a843fdc6cb79ab3329e1f316027968e14ab2a0b765ff3505ad2af85003df5c3",',
        '    "sha256": "1e90f2791e813319f95095b8be40b698e7dacd548f0e5e51c39be413d7846c19",',
    ),
    (
        'COMMON_GENERATOR_SHA256 = "cd868864d84479238ef27b8475ada68bcf20cac0cd2c154dabadcd68f6089574"',
        'COMMON_GENERATOR_SHA256 = "8ca2498eae90a365e63997f50e48b80d070d252be8b946d38570b46ac7c40092"',
    ),
    ("UNIT_27_BASELINE_RECORDS = 20570", "UNIT_28_BASELINE_RECORDS = 21358"),
    ("    for number in (25, 26, 27, 28)", "    for number in (25, 26, 27, 28, 29, 30)"),
    ('        "frozen_date": "2026-08-26",', '        "frozen_date": "2026-08-28",'),
    (
        '        "release_state": "verified_cumulative_checkpoint_ready_for_existing_github_and_zenodo_lineages",',
        '        "release_state": "verified_complete_classical_volume_ready_for_existing_github_and_zenodo_lineages",',
    ),
    ('        "classical_volume_complete": False,', '        "classical_volume_complete": True,'),
    (
        '    require_equal(inspection.get("contact_sheet_count"), 24, "visual contact-sheet count")',
        '    require_equal(inspection.get("contact_sheet_count"), 26, "visual contact-sheet count")',
    ),
    ("len(sheets) != 24", "len(sheets) != 26"),
    (
        '        raise RuntimeError("Visual QA must bind all 24 contact sheets")',
        '        raise RuntimeError("Visual QA must bind all 26 contact sheets")',
    ),
):
    generated = replace_once(generated, old, new)

# Units 29–30 were exported together from the accepted Unit 28 backend.  Keep
# the actual byte-preserved baseline rather than inventing a Unit 29 baseline.
generated = generated.replace("UNIT_27_BASELINE_RECORDS", "UNIT_28_BASELINE_RECORDS")
generated = generated.replace("units_01_27_baseline", "units_01_28_baseline")
generated = generated.replace("unit_27_records_preserved", "unit_28_records_preserved")
generated = generated.replace("Unit 27 backend", "Unit 28 backend")
generated = generated.replace("Unit 27 baseline", "Unit 28 baseline")

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(Path(__file__).resolve()), "exec"), namespace)
