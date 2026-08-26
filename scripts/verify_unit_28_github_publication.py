#!/usr/bin/env python3
"""Anonymously verify and receipt the cumulative Unit 28 GitHub publication.

The accepted Unit 27 verifier is specialized from a pinned byte identity.
``--self-check`` validates only local release bytes and contracts; the normal
mode performs anonymous public readback and never reads an account credential.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "verify_unit_27_github_publication.py"
TEMPLATE_SHA256 = "379a85ec2dc36797652114b4a3f6c0ab61aaafa0de97e7d57208424e14aa1e2d"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 28 GitHub specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


def materialize_unit27_implementation() -> str:
    if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
        raise SystemExit("Accepted Unit 27 GitHub verifier is absent or has drifted")
    source = TEMPLATE.read_text(encoding="utf-8")
    marker = '\nnamespace = {"__file__":'
    if source.count(marker) != 1:
        raise SystemExit("Could not isolate the accepted Unit 27 GitHub builder")
    builder = source[: source.index(marker)]
    namespace = {"__file__": str(TEMPLATE), "__name__": "unit27_builder_capture"}
    exec(compile(builder, str(TEMPLATE), "exec"), namespace)
    generated = namespace.get("generated")
    if not isinstance(generated, str):
        raise SystemExit("Accepted Unit 27 GitHub builder yielded no implementation")
    return generated


generated = materialize_unit27_implementation()
for old, new in (
    ("Units 1–27", "Units 1–28"),
    ("Unit 1–27", "Unit 1–28"),
    ("Units 24–27", "Units 24–28"),
    ("Unit 24–27", "Unit 24–28"),
    ("units_24_27", "units_24_28"),
):
    generated = generated.replace(old, new)

generated = replace_once(
    generated,
    '    if not isinstance(coverage, dict) or coverage.get("through_unit") != 27:',
    '    if not isinstance(coverage, dict) or coverage.get("through_unit") != 28:',
)
generated = replace_once(
    generated,
    '        raise RuntimeError("Unit 27 release must remain a truthful partial 27/30 checkpoint")',
    '        raise RuntimeError("Unit 28 release must remain a truthful partial 28/30 checkpoint")',
)

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

# Bind all changing coverage to the frozen local candidate.  Reader facts are
# independently pinned here; the backend count is measured only after its
# deterministic export instead of being guessed in advance.
generated = replace_once(
    generated,
    '''    exact_coverage = {
        "pdf_pages": 464,
        "exercises": 657,
        "public_source_solutions": 117,
        "reader_media_positions": 94,
        "backend_records": 20570,
    }
    for key, wanted in exact_coverage.items():
        if coverage.get(key) != wanted:
            raise RuntimeError(
                f"Unit 28 release coverage {key} mismatch: {coverage.get(key)!r} != {wanted!r}"
            )
    candidate_path = ROOT / "qa" / "UNIT_28_RELEASE_CANDIDATE.json"
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
        raise RuntimeError("Unit 28 release manifest is not bound to the frozen candidate")''',
    '''    candidate_path = ROOT / "qa" / "UNIT_28_RELEASE_CANDIDATE.json"
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    if not isinstance(candidate, dict) or candidate.get("status") != "PASS_RELEASE_READY":
        raise RuntimeError("Unit 28 frozen release candidate is unavailable or not ready")
    candidate_coverage = candidate.get("coverage") or {}
    backend_records = candidate_coverage.get("native_backend_records")
    if not isinstance(backend_records, int) or isinstance(backend_records, bool) or backend_records <= 20570:
        raise RuntimeError("Unit 28 candidate does not extend the 20,570-record Unit 27 backend")
    exact_coverage = {
        "pdf_pages": 476,
        "exercises": 671,
        "public_source_solutions": 118,
        "reader_media_positions": 98,
        "backend_records": backend_records,
    }
    for key, wanted in exact_coverage.items():
        if coverage.get(key) != wanted:
            raise RuntimeError(
                f"Unit 28 release coverage {key} mismatch: {coverage.get(key)!r} != {wanted!r}"
            )
    candidate_map = {
        "pdf_pages": ((candidate.get("reader") or {}).get("pdf") or {}).get("pages"),
        "exercises": candidate_coverage.get("exercises"),
        "public_source_solutions": candidate_coverage.get("public_source_solutions"),
        "reader_media_positions": candidate_coverage.get("reader_media_positions"),
        "backend_records": candidate_coverage.get("native_backend_records"),
    }
    if candidate_map != exact_coverage:
        raise RuntimeError("Unit 28 release manifest is not bound to the frozen candidate")''',
)

# The Unit 28 DOI does not exist until Zenodo reserves the new version.  Bind
# GitHub metadata to the sanitized public Zenodo receipt rather than hard-code
# or predict that identity.
generated = replace_once(
    generated,
    '''    citation_text = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    if 'doi: "10.5281/zenodo.22104692"' not in citation_text:
        raise RuntimeError("Public citation does not bind the Unit 28 Zenodo DOI")''',
    '''    zenodo_receipt_path = ROOT / "qa" / "UNIT_28_ZENODO_PUBLICATION.json"
    zenodo_receipt = json.loads(zenodo_receipt_path.read_text(encoding="utf-8"))
    if not isinstance(zenodo_receipt, dict) or zenodo_receipt.get("status") != "PASS":
        raise RuntimeError("Unit 28 Zenodo publication receipt is unavailable or not PASS")
    zenodo_record = zenodo_receipt.get("record")
    if not isinstance(zenodo_record, dict):
        raise RuntimeError("Unit 28 Zenodo record identity is missing")
    if zenodo_record.get("previous_record_id") != 22104692:
        raise RuntimeError("Unit 28 Zenodo receipt is not the successor of record 22104692")
    publication_doi = zenodo_record.get("doi")
    if not isinstance(publication_doi, str) or not publication_doi.startswith("10.5281/zenodo."):
        raise RuntimeError("Unit 28 Zenodo DOI is invalid")
    if publication_doi == "10.5281/zenodo.22104692":
        raise RuntimeError("Unit 28 Zenodo receipt reuses the Unit 27 DOI")
    citation_text = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    if f'doi: "{publication_doi}"' not in citation_text:
        raise RuntimeError("Public citation does not bind the Unit 28 Zenodo DOI")''',
)

# Add a truly offline contract check.  It validates the exact eight local
# release files and the frozen lineage/tag facts, and does not instantiate an
# HTTP session.
generated = replace_once(
    generated,
    "def main() -> None:",
    '''def self_check() -> dict:
    expected, manifest = load_release_contract()
    candidate = json.loads(
        (ROOT / "qa" / "UNIT_28_RELEASE_CANDIDATE.json").read_text(encoding="utf-8")
    )
    publication = candidate.get("publication") or {}
    if ((publication.get("github") or {}).get("target_tag")) != TAG:
        raise RuntimeError("Unit 28 candidate GitHub tag mismatch")
    if ((publication.get("zenodo") or {}).get("previous_record_id")) != 22104692:
        raise RuntimeError("Unit 28 candidate Zenodo predecessor mismatch")
    if list(expected) != FILES or len(expected) != 8:
        raise RuntimeError("Unit 28 release is not the exact eight-file inventory")
    for relative in ("CITATION.cff", "README.md", "LICENSE.md", "docs/index.html", "docs/algebraic-geometry-bridge-id-units-01-28.pdf"):
        repository_descriptor(relative)
    return {
        "status": "PASS",
        "mode": "offline_local_contract_check",
        "version": manifest.get("version"),
        "tag": TAG,
        "files": len(expected),
        "credential_read": False,
        "network_called": False,
        "receipt_written": False,
    }


def main() -> None:''',
)
generated = replace_once(
    generated,
    '''    parser = argparse.ArgumentParser()
    parser.add_argument("--wait-seconds", type=int, default=300)
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    result = verify(args.wait_seconds, args.expected_commit)''',
    '''    parser = argparse.ArgumentParser()
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--wait-seconds", type=int, default=300)
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    if args.self_check:
        print(json.dumps(self_check(), indent=2))
        return
    result = verify(args.wait_seconds, args.expected_commit)''',
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
