#!/usr/bin/env python3
"""Build the deterministic reader-first cumulative Unit 27 release payload.

This bounded adapter specializes the byte-pinned accepted Unit 24 packager.
All reader/backend counts and file identities are loaded from the frozen Unit
27 candidate and receipts at runtime.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "scripts" / "package_unit_24_release.py"
TEMPLATE_SHA256 = "435a64ab075688930fa0f24ca4c864e303b9386c506706e29390db1fcac0002c"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Unit 27 release specialization expected one occurrence, found {count}: {old!r}"
        )
    return text.replace(old, new, 1)


def materialize_unit24_implementation() -> str:
    if not TEMPLATE.is_file() or digest(TEMPLATE) != TEMPLATE_SHA256:
        raise SystemExit("Accepted Unit 24 release packager is absent or has drifted")
    source = TEMPLATE.read_text(encoding="utf-8")
    marker = '\nnamespace = {"__file__":'
    if source.count(marker) != 1:
        raise SystemExit("Could not isolate the accepted Unit 24 packager builder")
    builder = source[: source.index(marker)]
    namespace = {"__file__": str(TEMPLATE), "__name__": "unit24_builder_capture"}
    exec(compile(builder, str(TEMPLATE), "exec"), namespace)
    generated = namespace.get("generated")
    if not isinstance(generated, str):
        raise SystemExit("Accepted Unit 24 packager did not yield an implementation")
    return generated


generated = materialize_unit24_implementation()
for old, new in (
    ("units-01-24", "units-01-27"),
    ("UNITS_01_24", "UNITS_01_27"),
    ("UNIT_24", "UNIT_27"),
    ("unit-24", "unit-27"),
    ("unit_24", "unit_27"),
    ("unit24", "unit27"),
    ("Unit 24", "Unit 27"),
):
    generated = generated.replace(old, new)

generated = replace_once(generated, "EXPECTED_UNITS = 24", "EXPECTED_UNITS = 27")
generated = replace_once(
    generated,
    "helpers.FIXED_ZIP_TIME = (2026, 8, 25, 0, 0, 0)",
    "helpers.FIXED_ZIP_TIME = (2026, 8, 26, 0, 0, 0)",
)

# Preserve the complete contiguous QA/worklog closure rather than jumping from
# the previous cumulative boundary directly to Unit 27.
generated = replace_once(
    generated,
    '        exact("qa/UNIT_21_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_22_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_23_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_27_TRANSLATION_QA.json"),',
    '        exact("qa/UNIT_21_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_22_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_23_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_24_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_25_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_26_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_27_TRANSLATION_QA.json"),',
)
generated = replace_once(
    generated,
    '        exact("qa/UNIT_27_TRANSLATION_QA.json"),\n'
    '        exact("authority/terminology-id-arxiv/TERMINOLOGY_QA_REPORT.md"),',
    '        exact("qa/UNIT_27_TRANSLATION_QA.json"),\n'
    '        exact("qa/UNIT_25_AUTHORITY_QA.json"),\n'
    '        exact("qa/UNIT_26_AUTHORITY_QA.json"),\n'
    '        exact("qa/UNIT_27_AUTHORITY_QA.json"),\n'
    '        exact("qa/UNIT_27_TERMINOLOGY_QA.md"),\n'
    '        exact("authority/terminology-id-arxiv/TERMINOLOGY_QA_REPORT.md"),',
)
generated = replace_once(
    generated,
    '        "UNIT_21_WORKLOG.md",\n'
    '        "UNIT_22_WORKLOG.md",\n'
    '        "UNIT_23_WORKLOG.md",\n'
    '        "UNIT_27_WORKLOG.md",',
    '        "UNIT_21_WORKLOG.md",\n'
    '        "UNIT_22_WORKLOG.md",\n'
    '        "UNIT_23_WORKLOG.md",\n'
    '        "UNIT_24_WORKLOG.md",\n'
    '        "UNIT_25_WORKLOG.md",\n'
    '        "UNIT_26_WORKLOG.md",\n'
    '        "UNIT_27_WORKLOG.md",',
)

# Bind the release candidate to its actual authority, reader, QA, backend,
# rights, and publication identities instead of accepting coverage numerals
# alone.
generated = replace_once(
    generated,
    '''    require_equal(reader_pdf.get("pages"), pages, "release candidate PDF pages")
    return candidate''',
    '''    require_equal(reader_pdf.get("pages"), pages, "release candidate PDF pages")
    require_equal(
        candidate.get("source_course_boundary"),
        {
            "units_01_23": "Algebraische Kurven (Osnabrück 2025–2026)",
            "units_24_27": "Algebraische Kurven (Osnabrück 2012)",
        },
        "release candidate source-course boundary",
    )
    reader = candidate.get("reader")
    if not isinstance(reader, dict):
        raise RuntimeError("Release candidate reader section is missing")
    verify_path_descriptor(reader.get("html"), "release candidate HTML", HTML_SOURCE)
    verify_path_descriptor(reader.get("pdf"), "release candidate PDF", PDF_SOURCE)
    verify_path_descriptor(
        reader.get("build_receipt"),
        "release candidate build receipt",
        BUILD_RECEIPT_SOURCE,
    )

    qa = candidate.get("qa")
    if not isinstance(qa, dict):
        raise RuntimeError("Release candidate QA section is missing")
    qa_paths = {
        "machine": MACHINE_QA,
        "visual": VISUAL_QA,
        "responsive": RESPONSIVE_QA,
        "protected_surfaces": PROTECTED_QA,
        "backend": BACKEND_QA,
        "translation": "qa/UNIT_27_TRANSLATION_QA.json",
    }
    for key, expected_path in qa_paths.items():
        item = qa.get(key)
        if not isinstance(item, dict):
            raise RuntimeError(f"Release candidate QA descriptor is missing: {key}")
        require_equal(item.get("path"), expected_path, f"release candidate QA {key} path")
        require_equal(item.get("status"), "PASS", f"release candidate QA {key} status")
        require_equal(item.get("sha256"), sha256(exact(expected_path)), f"release candidate QA {key} sha256")

    authority = candidate.get("authority")
    if not isinstance(authority, dict):
        raise RuntimeError("Release candidate authority section is missing")
    for number in (25, 26, 27):
        key = f"unit_{number:02d}"
        item = authority.get(key)
        if not isinstance(item, dict):
            raise RuntimeError(f"Release candidate authority descriptor is missing: {key}")
        manifest_path = f"authority/wikiversity/unit-{number:02d}/UNIT_AUTHORITY_MANIFEST.json"
        manifest_descriptor = item.get("manifest")
        if not isinstance(manifest_descriptor, dict):
            raise RuntimeError(f"Release candidate authority manifest is missing: {key}")
        require_equal(manifest_descriptor.get("path"), manifest_path, f"{key} manifest path")
        require_equal(manifest_descriptor.get("sha256"), sha256(exact(manifest_path)), f"{key} manifest sha256")
        manifest_value = load_json(manifest_path)
        require_equal(manifest_descriptor.get("lecture_revid"), manifest_value["lecture"]["revid"], f"{key} lecture revid")
        require_equal(manifest_descriptor.get("worksheet_revid"), manifest_value["worksheet"]["revid"], f"{key} worksheet revid")
        require_equal(item.get("exercise_map_sha256"), sha256(exact(f"authority/wikiversity/unit-{number:02d}/ORDERED_EXERCISE_MAP.json")), f"{key} exercise-map sha256")
        require_equal(item.get("rights_sha256"), sha256(exact(f"authority/RIGHTS-unit-{number:02d}.csv")), f"{key} rights sha256")
        require_equal(item.get("asset_closure_sha256"), sha256(exact(f"authority/ASSET_CLOSURE-unit-{number:02d}.json")), f"{key} asset-closure sha256")

    backend = candidate.get("backend")
    if not isinstance(backend, dict):
        raise RuntimeError("Release candidate backend section is missing")
    verify_path_descriptor(backend.get("native_manifest"), "release candidate backend manifest", BACKEND_MANIFEST_SOURCE)
    verify_path_descriptor(backend.get("native_records"), "release candidate backend records", BACKEND_RECORDS_SOURCE)
    require_equal(backend.get("unit_24_records_preserved"), 18488, "release candidate Unit 24 baseline")
    require_equal(backend.get("deterministic_double_replay"), True, "release candidate backend replay")

    rights = candidate.get("rights")
    require_equal((rights or {}).get("translated_text"), "CC BY-SA 4.0", "release candidate translated-text licence")
    require_equal((rights or {}).get("blanket_file_set_license_claimed"), False, "release candidate blanket-licence flag")
    require_equal((rights or {}).get("non_endorsed_independent_derivative"), True, "release candidate non-endorsement")
    publication = candidate.get("publication") or {}
    require_equal(((publication.get("zenodo") or {}).get("previous_record_id")), 22102097, "release candidate Zenodo predecessor")
    require_equal(((publication.get("github") or {}).get("target_tag")), "unit-27", "release candidate GitHub tag")
    return candidate''',
)

# The historical-source boundary spans all four admitted 2012 units.
generated = generated.replace(
    '"unit_27": "Algebraische Kurven (Osnabrück 2012)"',
    '"units_24_27": "Algebraische Kurven (Osnabrück 2012)"',
)
generated = generated.replace(
    '"unit_27_pdf_component_notices"',
    '"units_24_27_pdf_component_notices"',
)
generated = replace_once(
    generated,
    '''    authority_markers = (
        "Kurs:Algebraische Kurven (Osnabrück 2012)",
        "CC BY-SA 4.0 course route",
        "CC BY-SA 2.0 Germany file notice",
        "do not make a blanket relicensing claim",
    )''',
    '''    authority_markers = (
        "Kurs:Algebraische Kurven (Osnabrück 2012)",
        "CC BY-SA 4.0 print/course route",
        "CC BY-SA 2.0 Germany file notice",
        "make no blanket relicensing claim",
    )''',
)

# Bind the citation metadata to the already-reserved version identity. The
# reservation is deliberately created before packaging to avoid inventing a
# DOI and to keep the public concept lineage single.
generated = replace_once(
    generated,
    "def validate_prerequisites() -> dict:",
    '''def validate_citation() -> Path:
    path = exact("CITATION.cff")
    reservation = load_json("qa/UNIT_27_ZENODO_RESERVATION.json")
    require_equal(reservation.get("status"), "PASS", "citation reservation status")
    require_equal(reservation.get("version"), "unit-27", "citation reservation version")
    require_equal(
        reservation.get("previous_record_id"),
        22102097,
        "citation reservation predecessor",
    )
    require_equal(
        reservation.get("concept_doi"),
        CONCEPT_DOI,
        "citation reservation concept DOI",
    )
    doi = reservation.get("doi")
    if not isinstance(doi, str) or not doi.startswith("10.5281/zenodo."):
        raise RuntimeError("Citation reservation DOI is invalid")
    record_id = reservation.get("record_id")
    require_equal(doi, f"10.5281/zenodo.{record_id}", "citation reservation DOI identity")
    if doi == "10.5281/zenodo.22102097":
        raise RuntimeError("Unit 27 citation reuses the Unit 24 predecessor DOI")

    text = path.read_text(encoding="utf-8")
    top_level: dict[str, str] = {}
    for line in text.splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        top_level[key.strip()] = value.strip().strip('"')
    expected = {
        "cff-version": "1.2.0",
        "title": "Kurva Aljabar — Edisi Bahasa Indonesia",
        "type": "book",
        "version": "unit-27",
        "doi": doi,
        "date-released": "2026-08-26",
        "repository-code": "https://github.com/KokunoYumeto/algebraic-geometry-bridge-id",
        "url": f"https://doi.org/{doi}",
    }
    for key, wanted in expected.items():
        require_equal(top_level.get(key), wanted, f"CITATION.cff {key}")

    normalized = " ".join(text.split())
    required = (
        "family-names: Brenner",
        "given-names: Holger",
        "Unit 1–27",
        "Unit 24–27",
        "OpenAI Codex gpt-5.6-sol, Ultra.",
    )
    missing = [marker for marker in required if marker not in normalized]
    if missing:
        raise RuntimeError(f"Unit 27 citation metadata is stale: {missing}")
    return path


def validate_public_docs() -> None:
    readme = " ".join(exact("README.md").read_text(encoding="utf-8").split())
    readme_required = (
        "Unit 1–23",
        "Unit 24–27",
        "27 dari 30 unit",
        "657 soal",
        "117 solusi publik",
        "94 posisi media",
        "PDF A4 464 halaman",
        "20.570 rekaman",
        "algebraic-geometry-bridge-id-units-01-27.pdf",
        "qa/UNITS_01_27_MACHINE_QA.json",
        "qa/UNITS_01_27_BACKEND_QA.json",
        "10.5281/zenodo.22104692",
    )
    missing_readme = [marker for marker in readme_required if marker not in readme]
    if missing_readme:
        raise RuntimeError(f"Unit 27 README is stale: {missing_readme}")

    license_text = " ".join(exact("LICENSE.md").read_text(encoding="utf-8").split())
    license_required = (
        "Units 24–27",
        "RIGHTS-unit-25.csv",
        "RIGHTS-unit-26.csv",
        "RIGHTS-unit-27.csv",
        "CC BY-SA 4.0 course route",
        "CC BY-SA 2.0 Germany file notice",
        "blanket relicensing claim",
    )
    missing_license = [marker for marker in license_required if marker not in license_text]
    if missing_license:
        raise RuntimeError(f"Unit 27 LICENSE is stale: {missing_license}")


def validate_prerequisites() -> dict:''',
)
generated = replace_once(
    generated,
    "    license_path = validate_license()\n    exact(HANDOFF)",
    "    license_path = validate_license()\n    validate_citation()\n    validate_public_docs()\n    exact(HANDOFF)",
)

namespace = {"__file__": str(Path(__file__).resolve()), "__name__": "__main__"}
exec(compile(generated, str(TEMPLATE), "exec"), namespace)
