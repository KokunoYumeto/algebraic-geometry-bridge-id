#!/usr/bin/env python3
"""Anonymously verify and receipt the cumulative Unit 30 GitHub publication.

The accepted Unit 28 verifier is specialized from a pinned byte identity.
--self-check validates only local release bytes and contracts; normal mode
performs anonymous public readback and never reads an account credential.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "verify_unit_28_github_publication.py"
TEMPLATE_SHA256 = "e11a7dc169229109cf5ff0b7d8bbb0241df4b1a99b52226d423adbeca0af8639"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 30 GitHub specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


def materialize_unit28_implementation() -> str:
    if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
        raise SystemExit("Accepted Unit 28 GitHub verifier is absent or has drifted")
    source = TEMPLATE.read_text(encoding="utf-8")
    marker = '\nnamespace = {"__file__":'
    if source.count(marker) != 1:
        raise SystemExit("Could not isolate the accepted Unit 28 GitHub builder")
    builder = source[: source.index(marker)]
    namespace = {"__file__": str(TEMPLATE), "__name__": "unit28_builder_capture"}
    exec(compile(builder, str(TEMPLATE), "exec"), namespace)
    generated = namespace.get("generated")
    if not isinstance(generated, str):
        raise SystemExit("Accepted Unit 28 GitHub builder yielded no implementation")
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

generated = replace_once(
    generated,
    '    if not isinstance(coverage, dict) or coverage.get("through_unit") != 28:',
    '    if not isinstance(coverage, dict) or coverage.get("through_unit") != 30:',
)
generated = replace_once(
    generated,
    '    if coverage.get("planned_units") != 30 or coverage.get("full_edition_complete") is not False:\n'
    '        raise RuntimeError("Unit 30 release must remain a truthful partial 28/30 checkpoint")',
    '    if (\n'
    '        coverage.get("planned_units") != 30\n'
    '        or coverage.get("classical_volume_complete") is not True\n'
    '        or coverage.get("full_edition_complete") is not False\n'
    '    ):\n'
    '        raise RuntimeError(\n'
    '            "Unit 30 release must be a complete 30/30 classical volume without "\n'
    '            "claiming completion of the broader two-volume edition"\n'
    '        )',
)

for old, new in (
    ('        "pdf_pages": 476,', '        "pdf_pages": 504,'),
    ('        "exercises": 671,', '        "exercises": 693,'),
    ('        "public_source_solutions": 118,', '        "public_source_solutions": 122,'),
    ('        "reader_media_positions": 98,', '        "reader_media_positions": 101,'),
    ("backend_records <= 20570", "backend_records <= 21358"),
    (
        '        raise RuntimeError("Unit 30 candidate does not extend the 20,570-record Unit 27 backend")',
        '        raise RuntimeError("Unit 30 candidate does not extend the 21,358-record Unit 28 backend")',
    ),
):
    generated = replace_once(generated, old, new)

generated = generated.replace("22104692", "22105836")
generated = generated.replace("Unit 27 DOI", "Unit 28 DOI")

generated = replace_once(
    generated,
    '            "full_edition_complete": release_manifest["coverage"]["full_edition_complete"],',
    '            "classical_volume_complete": release_manifest["coverage"]["classical_volume_complete"],\n'
    '            "full_edition_complete": release_manifest["coverage"]["full_edition_complete"],',
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
