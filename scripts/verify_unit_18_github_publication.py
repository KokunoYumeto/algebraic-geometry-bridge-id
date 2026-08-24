#!/usr/bin/env python3
"""Anonymously verify and receipt the cumulative Unit 18 GitHub publication."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "verify_unit_15_github_publication.py"
TEMPLATE_SHA256 = "543d8e2f3efc1637f95a9a41a27b44a448641afa1a425837a47a4090adc70e8f"
CONTENT_COMMIT = "fb99904c2dce760fdb67ffff5f561b6ffa30541b"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"GitHub verifier specialization expected one occurrence, found {count}: {old!r}")
    return text.replace(old, new, 1)


if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
    raise SystemExit("Frozen Unit 15 GitHub verifier template is absent or has drifted")

generated = TEMPLATE.read_text(encoding="utf-8")
for old, new in (
    ("units-01-15", "units-01-18"),
    ("UNIT_15", "UNIT_18"),
    ("unit-15", "unit-18"),
    ("unit_15", "unit_18"),
    ("unit15", "unit18"),
    ("Unit 15", "Unit 18"),
):
    generated = generated.replace(old, new)
generated = replace_once(
    generated,
    'EXPECTED_COMMIT = "aada4c2320a79e5dcdce0d7fa767c67dd0b24a9e"',
    f'EXPECTED_COMMIT = "{CONTENT_COMMIT}"',
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
