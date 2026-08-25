#!/usr/bin/env python3
"""Publish the verified Unit 21 checkpoint in the existing Zenodo lineage.

This specialization reuses the byte-frozen, fail-closed Unit 15 publisher and
changes only the predecessor identity, bounded coverage, versioned filenames,
and truthful checkpoint prose. Credentials remain runtime-only in the helper.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "publish_unit_15_zenodo.py"
TEMPLATE_SHA256 = "45fc082dfa54eb2c8ef1e246eefc4df12294f7b97cf9c8471ff8c744e21670b4"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Zenodo specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
    raise SystemExit("Frozen Unit 15 Zenodo publisher template is absent or has drifted")

generated = TEMPLATE.read_text(encoding="utf-8")
for old, new in (
    ("units-01-15", "units-01-21"),
    ("UNITS_01_15", "UNITS_01_21"),
    ("UNIT_15", "UNIT_21"),
    ("unit-15", "unit-21"),
    ("unit_15", "unit_21"),
    ("unit15", "unit21"),
    ("Unit 1–15", "Unit 1–21"),
    ("Units 1–15", "Units 1–21"),
    ("Unit 15", "Unit 21"),
    ("lima belas", "dua puluh satu"),
    ("fifteen", "twenty-one"),
):
    generated = generated.replace(old, new)

generated = generated.replace("22074716", "22087566")
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

# Coverage numerals in bilingual metadata and required-marker checks are
# checkpoint facts, not record identifiers.
generated = generated.replace("423 soal", "577 soal")
generated = generated.replace("75 solusi publik", "102 solusi publik")
generated = generated.replace("69 posisi media pembaca", "76 posisi media pembaca")
generated = generated.replace("423 exercises", "577 exercises")
generated = generated.replace("75 frozen public-source", "102 frozen public-source")
generated = generated.replace("69 credited reader-media", "76 credited reader-media")

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
