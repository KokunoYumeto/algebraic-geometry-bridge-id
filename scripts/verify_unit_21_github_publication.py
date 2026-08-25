#!/usr/bin/env python3
"""Anonymously verify and receipt the cumulative Unit 21 GitHub publication."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "verify_unit_15_github_publication.py"
TEMPLATE_SHA256 = "543d8e2f3efc1637f95a9a41a27b44a448641afa1a425837a47a4090adc70e8f"
CONTENT_COMMIT = "5304877a495b39bba9f9d681b086139ba3bd2f4e"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"GitHub verifier specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
    raise SystemExit("Frozen Unit 15 GitHub verifier template is absent or has drifted")

generated = TEMPLATE.read_text(encoding="utf-8")
for old, new in (
    ("units-01-15", "units-01-21"),
    ("UNIT_15", "UNIT_21"),
    ("unit-15", "unit-21"),
    ("unit_15", "unit_21"),
    ("unit15", "unit21"),
    ("Unit 15", "Unit 21"),
):
    generated = generated.replace(old, new)
generated = replace_once(
    generated,
    'EXPECTED_COMMIT = "aada4c2320a79e5dcdce0d7fa767c67dd0b24a9e"',
    f'EXPECTED_COMMIT = "{CONTENT_COMMIT}"',
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
