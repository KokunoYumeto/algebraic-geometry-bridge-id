#!/usr/bin/env python3
"""Anonymously verify and receipt the cumulative Unit 27 GitHub publication.

This bounded adapter specializes the byte-pinned accepted Unit 24 verifier and
binds the public main commit, annotated tag, release assets, raw reader bytes,
and live Pages bytes without embedding a not-yet-created commit hash.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "verify_unit_24_github_publication.py"
TEMPLATE_SHA256 = "e5e9280c3a6e8d5a5eaf39d0e3c2568320a7a4e427aa47d4d511687eaf5e346b"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def materialize_unit24_implementation() -> str:
    if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
        raise SystemExit("Accepted Unit 24 GitHub verifier is absent or has drifted")
    source = TEMPLATE.read_text(encoding="utf-8")
    marker = '\nnamespace = {"__file__":'
    if source.count(marker) != 1:
        raise SystemExit("Could not isolate the accepted Unit 24 GitHub builder")
    builder = source[: source.index(marker)]
    namespace = {"__file__": str(TEMPLATE), "__name__": "unit24_builder_capture"}
    exec(compile(builder, str(TEMPLATE), "exec"), namespace)
    generated = namespace.get("generated")
    if not isinstance(generated, str):
        raise SystemExit("Accepted Unit 24 GitHub builder yielded no implementation")
    return generated


generated = materialize_unit24_implementation()
for old, new in (
    ("units-01-24", "units-01-27"),
    ("UNIT_24", "UNIT_27"),
    ("unit-24", "unit-27"),
    ("unit_24", "unit_27"),
    ("unit24", "unit27"),
    ("Unit 24", "Unit 27"),
):
    generated = generated.replace(old, new)

generated = generated.replace(
    '"unit_27": "Algebraische Kurven (Osnabrück 2012)"',
    '"units_24_27": "Algebraische Kurven (Osnabrück 2012)"',
)
generated = generated.replace(
    '"unit_27_pdf_component_notices"',
    '"units_24_27_pdf_component_notices"',
)
generated = generated.replace(
    'coverage.get("through_unit") != 24',
    'coverage.get("through_unit") != 27',
)
generated = generated.replace(
    "truthful partial 24/30 checkpoint",
    "truthful partial 27/30 checkpoint",
)

generated = generated.replace(
    '''def load_release_contract() -> tuple[dict[str, dict[str, object]], dict]:''',
    '''def repository_descriptor(relative: str) -> dict[str, object]:
    path = ROOT / relative
    if not path.is_file():
        raise FileNotFoundError(path)
    return {
        "path": relative,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def load_release_contract() -> tuple[dict[str, dict[str, object]], dict]:''',
    1,
)
generated = generated.replace(
    '''    if manifest.get("version") != "unit-27" or manifest.get("language") != "id-ID":
        raise RuntimeError("Unit 27 release-manifest identity mismatch")
    coverage = manifest.get("coverage")''',
    '''    if manifest.get("version") != "unit-27" or manifest.get("language") != "id-ID":
        raise RuntimeError("Unit 27 release-manifest identity mismatch")
    if manifest.get("title") != "Kurva Aljabar — Edisi Bahasa Indonesia":
        raise RuntimeError("Unit 27 release-manifest title mismatch")
    if manifest.get("tool_provenance") != "OpenAI Codex gpt-5.6-sol, Ultra.":
        raise RuntimeError("Unit 27 release-manifest provenance mismatch")
    coverage = manifest.get("coverage")''',
    1,
)
generated = generated.replace(
    '''    if coverage.get("planned_units") != 30 or coverage.get("full_edition_complete") is not False:
        raise RuntimeError("Unit 27 release must remain a truthful partial 27/30 checkpoint")
    rights = manifest.get("rights")''',
    '''    if coverage.get("planned_units") != 30 or coverage.get("full_edition_complete") is not False:
        raise RuntimeError("Unit 27 release must remain a truthful partial 27/30 checkpoint")
    exact_coverage = {
        "pdf_pages": 464,
        "exercises": 657,
        "public_source_solutions": 117,
        "reader_media_positions": 94,
        "backend_records": 20570,
    }
    for key, wanted in exact_coverage.items():
        if coverage.get(key) != wanted:
            raise RuntimeError(
                f"Unit 27 release coverage {key} mismatch: {coverage.get(key)!r} != {wanted!r}"
            )
    candidate_path = ROOT / "qa" / "UNIT_27_RELEASE_CANDIDATE.json"
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    candidate_coverage = candidate.get("coverage") or {}
    candidate_map = {
        "pdf_pages": ((candidate.get("reader") or {}).get("pdf") or {}).get("pages"),
        "exercises": candidate_coverage.get("exercises"),
        "public_source_solutions": candidate_coverage.get("public_source_solutions"),
        "reader_media_positions": candidate_coverage.get("reader_media_positions"),
        "backend_records": candidate_coverage.get("native_backend_records"),
    }
    if candidate_map != exact_coverage:
        raise RuntimeError("Unit 27 release manifest is not bound to the frozen candidate")
    rights = manifest.get("rights")''',
    1,
)
generated = generated.replace(
    '''    if zenodo_section.get("reader_first") != FILES[0]:
        raise RuntimeError("Unit 27 release manifest is not reader-first")''',
    '''    if zenodo_section.get("concept_doi") != "10.5281/zenodo.22059686":
        raise RuntimeError("Unit 27 release manifest concept DOI mismatch")
    if zenodo_section.get("reader_first") != FILES[0]:
        raise RuntimeError("Unit 27 release manifest is not reader-first")''',
    1,
)

# Verify the public repository metadata bytes as well as reader bytes.
generated = generated.replace(
    '''    verify_equal(raw_html, expected["kurva-aljabar-id-unit-27.html"], "raw commit HTML")
    verify_equal(raw_pdf, expected["kurva-aljabar-id-unit-27.pdf"], "raw commit PDF")''',
    '''    verify_equal(raw_html, expected["kurva-aljabar-id-unit-27.html"], "raw commit HTML")
    verify_equal(raw_pdf, expected["kurva-aljabar-id-unit-27.pdf"], "raw commit PDF")
    raw_metadata: dict[str, dict[str, object]] = {}
    for relative in ("CITATION.cff", "README.md", "LICENSE.md"):
        local = repository_descriptor(relative)
        actual = readback(
            session,
            f"https://raw.githubusercontent.com/{OWNER}/{REPOSITORY}/{branch_commit}/{relative}",
        )
        verify_equal(actual, local, f"raw commit {relative}")
        raw_metadata[relative] = {**actual, "match": True}
    citation_text = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    if 'doi: "10.5281/zenodo.22104692"' not in citation_text:
        raise RuntimeError("Public citation does not bind the Unit 27 Zenodo DOI")''',
    1,
)
generated = generated.replace(
    '''        "raw_commit_readback": {
            "credential_used": False,
            "html": {**raw_html, "match": True},
            "pdf": {**raw_pdf, "match": True},
        },''',
    '''        "raw_commit_readback": {
            "credential_used": False,
            "html": {**raw_html, "match": True},
            "pdf": {**raw_pdf, "match": True},
            "metadata": raw_metadata,
        },''',
    1,
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
