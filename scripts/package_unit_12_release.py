#!/usr/bin/env python3
"""Build the fail-closed, reader-first cumulative Unit 12 release payload."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
U7_PATH = ROOT / "scripts" / "package_unit_07_release.py"
spec = importlib.util.spec_from_file_location("unit07_packaging_helpers", U7_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load bounded packaging helpers")
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)

helpers.OUT = ROOT / "release" / "unit-12"
helpers.PREFIX = "algebraic-geometry-bridge-id"
helpers.FIXED_ZIP_TIME = (2026, 8, 24, 0, 0, 0)
OUT = helpers.OUT

TITLE = "Kurva Aljabar — Edisi Bahasa Indonesia"
VERSION = "unit-12"
LANGUAGE = "id-ID"
MODEL_ID = "OpenAI Codex gpt-5.6-sol, Ultra"
PROVENANCE = f"{MODEL_ID}."
CONCEPT_DOI = "10.5281/zenodo.22059686"

EXPECTED_UNITS = 12
EXPECTED_PLANNED_UNITS = 30
EXPECTED_EXERCISES = 330
EXPECTED_PUBLIC_SOLUTIONS = 55
EXPECTED_MEDIA_POSITIONS = 65

PDF_SOURCE = "build/reader-id/algebraic-geometry-bridge-id-units-01-12.pdf"
HTML_SOURCE = "build/reader-id/index.html"
BUILD_RECEIPT_SOURCE = "build/reader-id/BUILD_RECEIPT.json"
BACKEND_DIRECTORY = "backend/units-01-12"
BACKEND_MANIFEST_SOURCE = f"{BACKEND_DIRECTORY}/MANIFEST.json"
BACKEND_RECORDS_SOURCE = f"{BACKEND_DIRECTORY}/records.jsonl"
MIGRATION_SOURCE = "backend/common-backend-v1/MIGRATION_RECEIPT.json"
MIGRATION_SCHEMA_SOURCE = (
    "backend/common-backend-v1-contract/upstream/"
    "backend-migration-receipt-v1.v0.42.0.schema.json"
)

PDF_NAME = "kurva-aljabar-id-unit-12.pdf"
HTML_NAME = "kurva-aljabar-id-unit-12.html"
SOURCE_ZIP_NAME = "kurva-aljabar-id-unit-12-source.zip"
AUTHORITY_ZIP_NAME = "kurva-aljabar-id-unit-12-authority-witnesses.zip"
BUILD_RECEIPT_NAME = "BUILD_RECEIPT-unit-12.json"
LICENSE_NAME = "LICENSE-unit-12.md"
MANIFEST_NAME = "ZENODO_FILE_MANIFEST-unit-12.json"
MIGRATION_NAME = "MIGRATION_RECEIPT.json"
RELEASE_FILES = [
    PDF_NAME,
    HTML_NAME,
    SOURCE_ZIP_NAME,
    AUTHORITY_ZIP_NAME,
    BUILD_RECEIPT_NAME,
    LICENSE_NAME,
    MANIFEST_NAME,
    MIGRATION_NAME,
]

MACHINE_QA = "qa/UNITS_01_12_MACHINE_QA.json"
VISUAL_QA = "qa/UNITS_01_12_VISUAL_QA.json"
RESPONSIVE_QA = "qa/UNITS_01_12_RESPONSIVE_QA.json"
BACKEND_QA = "qa/UNITS_01_12_BACKEND_QA.json"
PROTECTED_QA = "qa/UNIT_12_PROTECTED_SURFACES.json"
RELEASE_CANDIDATE = "qa/UNIT_12_RELEASE_CANDIDATE.json"
HANDOFF = "qa/UNITS_01_12_HANDOFF.md"


def exact(path: str) -> Path:
    return helpers.exact(path)


def tree(path: str) -> list[Path]:
    return helpers.tree(path)


def compact_tree(path: str) -> list[Path]:
    """Return a bounded tree without transient interpreter caches."""

    return [
        item
        for item in tree(path)
        if "__pycache__" not in item.parts and item.suffix.lower() not in {".pyc", ".pyo"}
    ]


def unique(paths: list[Path]) -> list[Path]:
    return helpers.unique(paths)


def descriptor(path: Path) -> dict:
    return helpers.descriptor(path)


def copy_exact(source: Path, name: str) -> Path:
    return helpers.copy_exact(source, name)


def zip_files(target: Path, paths: list[Path]) -> dict:
    return helpers.zip_files(target, paths)


def validate_release_inputs(paths: list[Path]) -> None:
    helpers.validate_release_inputs(paths)


def sha256(path: Path) -> str:
    return helpers.sha256(path)


def load_json(path: str) -> dict:
    source = exact(path)
    try:
        value = json.loads(source.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Invalid JSON prerequisite: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON prerequisite must contain an object: {path}")
    return value


def require_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise RuntimeError(f"{label} mismatch: expected {expected!r}, found {actual!r}")


def require_positive_int(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise RuntimeError(f"{label} must be a positive integer")
    return value


def verify_path_descriptor(
    value: object,
    label: str,
    expected_path: str | None = None,
) -> Path:
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} must be a descriptor object")
    relative = value.get("path")
    if not isinstance(relative, str) or not relative:
        raise RuntimeError(f"{label}.path is missing")
    normalized = Path(relative)
    if normalized.is_absolute() or ".." in normalized.parts:
        raise RuntimeError(f"{label}.path is not a bounded repository-relative path")
    if expected_path is not None:
        require_equal(relative.replace("\\", "/"), expected_path, f"{label}.path")
    path = exact(relative)
    require_equal(value.get("bytes"), path.stat().st_size, f"{label}.bytes")
    require_equal(value.get("sha256"), sha256(path), f"{label}.sha256")
    return path


def validate_build() -> tuple[dict, Path, Path]:
    receipt = load_json(BUILD_RECEIPT_SOURCE)
    require_equal(receipt.get("schema"), "ag-bridge-build-receipt-v2", "build schema")
    require_equal(receipt.get("language"), LANGUAGE, "build language")
    require_equal(receipt.get("through_unit"), EXPECTED_UNITS, "build through_unit")
    outputs = receipt.get("outputs")
    if not isinstance(outputs, list):
        raise RuntimeError("Build receipt outputs must be a list")
    by_path = {
        item.get("path"): item
        for item in outputs
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }
    require_equal(set(by_path), {PDF_SOURCE, HTML_SOURCE}, "build output inventory")
    pdf = verify_path_descriptor(by_path[PDF_SOURCE], "build PDF", PDF_SOURCE)
    html = verify_path_descriptor(by_path[HTML_SOURCE], "build HTML", HTML_SOURCE)
    return receipt, pdf, html


def sum_unit_field(table: object, field: str, label: str) -> int:
    if not isinstance(table, dict):
        raise RuntimeError(f"{label} must be an object")
    expected_keys = {f"unit_{number:02d}" for number in range(1, EXPECTED_UNITS + 1)}
    require_equal(set(table), expected_keys, f"{label} unit inventory")
    total = 0
    for key in sorted(expected_keys):
        entry = table[key]
        if not isinstance(entry, dict):
            raise RuntimeError(f"{label}.{key} must be an object")
        value = entry.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise RuntimeError(f"{label}.{key}.{field} must be a non-negative integer")
        total += value
    return total


def validate_reader_qa(pdf: Path, html: Path) -> int:
    machine = load_json(MACHINE_QA)
    require_equal(machine.get("status"), "PASS", "machine QA status")
    require_equal(machine.get("through_unit"), EXPECTED_UNITS, "machine QA through_unit")
    pages = require_positive_int((machine.get("pdf") or {}).get("pages"), "machine QA PDF pages")
    require_equal((machine.get("pdf") or {}).get("bytes"), pdf.stat().st_size, "machine QA PDF bytes")
    require_equal((machine.get("pdf") or {}).get("sha256"), sha256(pdf), "machine QA PDF sha256")
    require_equal((machine.get("html") or {}).get("bytes"), html.stat().st_size, "machine QA HTML bytes")
    require_equal((machine.get("html") or {}).get("sha256"), sha256(html), "machine QA HTML sha256")
    require_equal(
        (machine.get("html") or {}).get("images"),
        EXPECTED_MEDIA_POSITIONS,
        "machine QA reader media positions",
    )
    require_equal(
        sum_unit_field(machine.get("solutions"), "exercise_count", "machine QA solutions"),
        EXPECTED_EXERCISES,
        "machine QA exercise total",
    )
    require_equal(
        sum_unit_field(machine.get("solutions"), "solution_count", "machine QA solutions"),
        EXPECTED_PUBLIC_SOLUTIONS,
        "machine QA public-solution total",
    )
    require_equal(
        sum_unit_field(machine.get("rights"), "positions", "machine QA rights"),
        EXPECTED_MEDIA_POSITIONS,
        "machine QA rights-position total",
    )

    visual = load_json(VISUAL_QA)
    require_equal(visual.get("result"), "PASS", "visual QA result")
    require_equal(visual.get("through_unit"), EXPECTED_UNITS, "visual QA through_unit")
    require_equal((visual.get("pdf") or {}).get("pages"), pages, "visual QA PDF pages")
    require_equal((visual.get("pdf") or {}).get("bytes"), pdf.stat().st_size, "visual QA PDF bytes")
    require_equal((visual.get("pdf") or {}).get("sha256"), sha256(pdf), "visual QA PDF sha256")

    responsive = load_json(RESPONSIVE_QA)
    require_equal(responsive.get("status"), "PASS", "responsive QA status")
    require_equal(
        responsive.get("through_unit"),
        EXPECTED_UNITS,
        "responsive QA through_unit",
    )

    protected = load_json(PROTECTED_QA)
    require_equal(protected.get("status"), "PASS", "protected-surface QA status")
    require_equal(protected.get("unit"), EXPECTED_UNITS, "protected-surface QA unit")
    return pages


def validate_backend() -> tuple[dict, int]:
    manifest = load_json(BACKEND_MANIFEST_SOURCE)
    require_equal(
        manifest.get("schema"),
        "ag-bridge-backend-export-manifest-v2",
        "native backend schema",
    )
    require_equal(manifest.get("through_unit"), EXPECTED_UNITS, "native backend through_unit")
    record_count = require_positive_int(
        manifest.get("record_count"),
        "native backend record_count",
    )
    counts = manifest.get("counts")
    if not isinstance(counts, dict):
        raise RuntimeError("Native backend counts must be an object")
    require_equal(counts.get("exercise"), EXPECTED_EXERCISES, "native backend exercises")
    require_equal(counts.get("solution"), EXPECTED_PUBLIC_SOLUTIONS, "native backend solutions")
    require_equal(counts.get("asset"), EXPECTED_MEDIA_POSITIONS, "native backend assets")

    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        raise RuntimeError("Native backend file inventory is empty")
    seen: set[str] = set()
    for index, item in enumerate(files):
        path = verify_path_descriptor(item, f"native backend files[{index}]")
        relative = path.relative_to(ROOT).as_posix()
        if not relative.startswith(f"{BACKEND_DIRECTORY}/"):
            raise RuntimeError(f"Native backend descriptor escaped its bounded directory: {relative}")
        if relative in seen:
            raise RuntimeError(f"Duplicate native backend descriptor: {relative}")
        seen.add(relative)
    if BACKEND_RECORDS_SOURCE not in seen:
        raise RuntimeError("Native backend records.jsonl is absent from its manifest")

    qa = load_json(BACKEND_QA)
    require_equal(qa.get("result"), "PASS", "backend QA result")
    require_equal(qa.get("through_unit"), EXPECTED_UNITS, "backend QA through_unit")
    backend = qa.get("backend")
    if not isinstance(backend, dict):
        raise RuntimeError("Backend QA backend object is missing")
    require_equal(backend.get("record_count"), record_count, "backend QA record_count")
    require_equal(backend.get("counts"), counts, "backend QA table counts")
    require_equal(
        backend.get("manifest_path"),
        BACKEND_MANIFEST_SOURCE,
        "backend QA manifest path",
    )
    require_equal(
        backend.get("manifest_sha256"),
        sha256(exact(BACKEND_MANIFEST_SOURCE)),
        "backend QA manifest sha256",
    )
    require_equal(
        backend.get("records_path"),
        BACKEND_RECORDS_SOURCE,
        "backend QA records path",
    )
    require_equal(
        backend.get("records_sha256"),
        sha256(exact(BACKEND_RECORDS_SOURCE)),
        "backend QA records sha256",
    )
    return manifest, record_count


def validate_release_candidate(pages: int, backend_records: int) -> dict:
    candidate = load_json(RELEASE_CANDIDATE)
    if not str(candidate.get("status", "")).startswith("PASS"):
        raise RuntimeError("Unit 12 release candidate has not passed")
    require_equal(candidate.get("through_unit"), EXPECTED_UNITS, "release candidate through_unit")
    require_equal(candidate.get("language"), LANGUAGE, "release candidate language")
    require_equal(candidate.get("title"), TITLE, "release candidate title")
    require_equal(candidate.get("model_provenance"), PROVENANCE, "release candidate provenance")
    coverage = candidate.get("coverage")
    if not isinstance(coverage, dict):
        raise RuntimeError("Release candidate coverage is missing")
    require_equal(coverage.get("exercises"), EXPECTED_EXERCISES, "release candidate exercises")
    require_equal(
        coverage.get("public_source_solutions"),
        EXPECTED_PUBLIC_SOLUTIONS,
        "release candidate public solutions",
    )
    require_equal(
        coverage.get("reader_media_positions"),
        EXPECTED_MEDIA_POSITIONS,
        "release candidate media positions",
    )
    require_equal(
        coverage.get("native_backend_records"),
        backend_records,
        "release candidate backend records",
    )
    reader_pdf = ((candidate.get("reader") or {}).get("pdf") or {})
    require_equal(reader_pdf.get("pages"), pages, "release candidate PDF pages")
    return candidate


def validate_migration(backend_records: int) -> tuple[dict, dict]:
    receipt = load_json(MIGRATION_SOURCE)
    schema = load_json(MIGRATION_SCHEMA_SOURCE)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(receipt),
        key=lambda item: "/".join(str(part) for part in item.path),
    )
    if errors:
        rendered = "; ".join(error.message for error in errors[:5])
        raise RuntimeError(f"Common-backend migration receipt schema failure: {rendered}")

    require_equal(receipt.get("credentials_recorded"), False, "migration credential flag")
    require_equal(
        receipt.get("migration_mode"),
        "additive zero-copy adapter",
        "migration mode",
    )
    source = receipt.get("source")
    coverage = receipt.get("coverage")
    transformation = receipt.get("transformation")
    validation = receipt.get("validation")
    if not all(isinstance(value, dict) for value in (source, coverage, transformation, validation)):
        raise RuntimeError("Migration receipt lacks a required structured section")
    require_equal(source.get("through_unit"), EXPECTED_UNITS, "migration source through_unit")
    require_equal(source.get("record_count"), backend_records, "migration source record_count")
    require_equal(coverage.get("through_unit"), EXPECTED_UNITS, "migration coverage through_unit")
    require_equal(coverage.get("native_records"), backend_records, "migration native record count")
    require_equal(
        coverage.get("native_ids_preserved"),
        backend_records,
        "migration preserved native IDs",
    )
    require_equal(
        transformation.get("model_provenance"),
        PROVENANCE,
        "migration model provenance",
    )
    require_equal(validation.get("result"), "pass", "migration validation result")
    for key in (
        "strict_target_schema",
        "deterministic_double_replay",
        "global_id_uniqueness",
        "foreign_key_closure",
        "canonical_jsonl",
        "lossless_native_reverse",
    ):
        require_equal(validation.get(key), True, f"migration validation {key}")

    verify_path_descriptor(source.get("manifest"), "migration source manifest", BACKEND_MANIFEST_SOURCE)
    verify_path_descriptor(source.get("records_jsonl"), "migration source records", BACKEND_RECORDS_SOURCE)

    sanitized = copy.deepcopy(receipt)
    sanitized.pop("public_artifacts", None)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(sanitized),
        key=lambda item: "/".join(str(part) for part in item.path),
    )
    if errors:
        rendered = "; ".join(error.message for error in errors[:5])
        raise RuntimeError(f"Sanitized migration receipt schema failure: {rendered}")
    return receipt, sanitized


def validate_license() -> Path:
    path = exact("LICENSE.md")
    text = path.read_text(encoding="utf-8")
    normalized_text = " ".join(text.split())
    required = (
        "CC BY-SA 4.0",
        "RIGHTS-unit-12.csv",
        "independent edition",
        "does not imply endorsement",
        "Third-party media",
    )
    missing = [marker for marker in required if marker not in normalized_text]
    if missing:
        raise RuntimeError(f"Unit 12 mixed-rights licence notice is incomplete: {missing}")
    return path


def validate_prerequisites() -> dict:
    build_receipt, pdf, html = validate_build()
    pages = validate_reader_qa(pdf, html)
    backend_manifest, backend_records = validate_backend()
    validate_release_candidate(pages, backend_records)
    migration, sanitized_migration = validate_migration(backend_records)
    license_path = validate_license()
    exact(HANDOFF)
    return {
        "build_receipt": build_receipt,
        "pdf": pdf,
        "html": html,
        "pdf_pages": pages,
        "backend_manifest": backend_manifest,
        "backend_records": backend_records,
        "migration": migration,
        "sanitized_migration": sanitized_migration,
        "license": license_path,
    }


def source_inventory() -> list[Path]:
    files: list[Path] = [
        exact("README.md"),
        exact("CITATION.cff"),
        exact("LICENSE.md"),
        exact(BUILD_RECEIPT_SOURCE),
        exact(RELEASE_CANDIDATE),
        exact(HANDOFF),
        exact(MACHINE_QA),
        exact(VISUAL_QA),
        exact(RESPONSIVE_QA),
        exact(BACKEND_QA),
        exact(PROTECTED_QA),
        exact("qa/TERMINOLOGY_MIGRATION_UNIT_07.json"),
        exact("qa/TERMINOLOGY_QA_RECEIPT.json"),
        exact("qa/unit-10-translation-findings.md"),
        exact("qa/unit-11-translation-findings.md"),
        exact("qa/unit-12-translation-findings.md"),
        exact("authority/terminology-id-arxiv/TERMINOLOGY_QA_REPORT.md"),
        exact("authority/terminology-id-arxiv/SOURCE_MANIFEST.json"),
    ]
    for directory in (
        "source/id-ID",
        "authority/assets",
        BACKEND_DIRECTORY,
        "backend/common-backend-v1-contract",
        "scripts",
    ):
        files.extend(compact_tree(directory))
    for control_name in (
        "CORRECTIONS.csv",
        "CURRICULUM_SOURCE_RATIONALE.md",
        "CURSOR.json",
        "SCHEME_BRIDGE_DECISION.md",
        "TERMINOLOGY_QA_20260822.md",
        "TERMINOLOGY.csv",
        "UNIT_07_WORKLOG.md",
        "UNIT_08_WORKLOG.md",
        "UNIT_09_WORKLOG.md",
    ):
        files.append(exact(f"00_control/{control_name}"))

    files.extend(
        [
            exact("authority/AUTHORITY_FREEZE.md"),
            exact("authority/RIGHTS.csv"),
            exact("authority/ASSET_CLOSURE.json"),
            exact("authority/commons-imageinfo-lecture-01.json"),
        ]
    )
    for number in range(2, EXPECTED_UNITS + 1):
        files.extend(
            [
                exact(f"authority/UNIT_{number:02d}_AUTHORITY_FREEZE.md"),
                exact(f"authority/RIGHTS-unit-{number:02d}.csv"),
                exact(f"authority/ASSET_CLOSURE-unit-{number:02d}.json"),
            ]
        )
    for number in (*range(2, 10), 11, 12):
        files.append(exact(f"authority/commons-imageinfo-unit-{number:02d}.json"))
    files.extend(
        [
            exact("authority/commons-pdf-imageinfo-unit-10.json"),
            exact("authority/commons-description-unit-11.wikitext"),
            exact("authority/wikiversity-imageinfo-unit-08.json"),
            exact("authority/wikiversity-local-description-unit-08.wikitext"),
        ]
    )
    return unique(files)


def authority_inventory() -> list[Path]:
    files = compact_tree("authority/wikiversity")
    artifact_names = [
        "algebraische-kurven-osnabrueck-2025-2026-official.pdf",
        *[f"lecture-{number:02d}-official.pdf" for number in range(1, EXPECTED_UNITS + 1)],
        *[f"worksheet-{number:02d}-official.pdf" for number in range(1, EXPECTED_UNITS + 1)],
    ]
    files.extend(exact(f"authority/artifacts/{name}") for name in artifact_names)
    return unique(files)


def write_sanitized_migration(value: dict) -> Path:
    path = OUT / MIGRATION_NAME
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite {path}")
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    json.loads(path.read_text(encoding="utf-8"))
    validate_release_inputs([path])
    return path


def verify_final_inventory() -> list[dict]:
    entries = list(OUT.iterdir())
    if any(not item.is_file() for item in entries):
        raise RuntimeError("Unit 12 release directory contains a non-file entry")
    by_name = {item.name: item for item in entries}
    require_equal(set(by_name), set(RELEASE_FILES), "Unit 12 release inventory")
    if len(entries) != len(RELEASE_FILES):
        raise RuntimeError("Unit 12 release inventory contains duplicate or unexpected entries")
    return [descriptor(by_name[name]) for name in RELEASE_FILES]


def package() -> dict:
    state = validate_prerequisites()
    source_files = source_inventory()
    authority_files = authority_inventory()
    validate_release_inputs(source_files + authority_files)

    if OUT.exists():
        if not OUT.is_dir():
            raise RuntimeError(f"Release target is not a directory: {OUT}")
        if any(OUT.iterdir()):
            raise RuntimeError(f"Release directory must be empty: {OUT}")
    else:
        OUT.mkdir(parents=True)

    pdf = copy_exact(state["pdf"], PDF_NAME)
    html = copy_exact(state["html"], HTML_NAME)
    build_receipt = copy_exact(exact(BUILD_RECEIPT_SOURCE), BUILD_RECEIPT_NAME)
    license_copy = copy_exact(state["license"], LICENSE_NAME)
    source_zip_path = OUT / SOURCE_ZIP_NAME
    authority_zip_path = OUT / AUTHORITY_ZIP_NAME
    source_zip = zip_files(source_zip_path, source_files)
    authority_zip = zip_files(authority_zip_path, authority_files)
    migration_path = write_sanitized_migration(state["sanitized_migration"])

    manifest_bound_paths = [
        pdf,
        html,
        source_zip_path,
        authority_zip_path,
        build_receipt,
        license_copy,
        migration_path,
    ]
    manifest = {
        "schema": "ag-bridge-release-file-manifest-v2",
        # Bind the manifest timestamp to the frozen reader build.  This keeps
        # the package byte-reproducible when it is replayed after the public
        # artifact bindings are added to the (sanitized-on-release) migration
        # receipt.
        "generated_utc": state["build_receipt"]["built_utc"],
        "title": TITLE,
        "version": VERSION,
        "language": LANGUAGE,
        "tool_provenance": PROVENANCE,
        "coverage": {
            "through_unit": EXPECTED_UNITS,
            "planned_units": EXPECTED_PLANNED_UNITS,
            "full_edition_complete": False,
            "pdf_pages": state["pdf_pages"],
            "exercises": EXPECTED_EXERCISES,
            "public_source_solutions": EXPECTED_PUBLIC_SOLUTIONS,
            "reader_media_positions": EXPECTED_MEDIA_POSITIONS,
            "backend_records": state["backend_records"],
        },
        "rights": {
            "translated_text": "CC BY-SA 4.0",
            "media": "Per-component rights in RIGHTS files and reader credits",
            "build_and_qa_code": "MIT",
            "blanket_payload_license_claimed": False,
            "license_notice": f"{LICENSE_NAME} and LICENSE.md inside the source ZIP",
            "independent_non_endorsed_derivative": True,
        },
        "zenodo": {
            "concept_doi": CONCEPT_DOI,
            "reader_first": PDF_NAME,
            "files_excluding_this_manifest": [
                descriptor(path) for path in manifest_bound_paths
            ],
        },
        "archives": {
            "source": source_zip,
            "authority_witnesses": authority_zip,
        },
        "validated_inputs": {
            "build_receipt": descriptor(exact(BUILD_RECEIPT_SOURCE)),
            "machine_qa": descriptor(exact(MACHINE_QA)),
            "visual_qa": descriptor(exact(VISUAL_QA)),
            "responsive_qa": descriptor(exact(RESPONSIVE_QA)),
            "backend_qa": descriptor(exact(BACKEND_QA)),
            "protected_surfaces": descriptor(exact(PROTECTED_QA)),
            "release_candidate": descriptor(exact(RELEASE_CANDIDATE)),
            "native_backend_manifest": descriptor(exact(BACKEND_MANIFEST_SOURCE)),
            # Bind the sanitized receipt that is actually released.  The
            # source receipt additionally carries public-artifact hashes, so
            # hashing it here would create a manifest/receipt cycle.
            "released_sanitized_migration_receipt": descriptor(migration_path),
        },
    }
    manifest_path = OUT / MANIFEST_NAME
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    json.loads(manifest_path.read_text(encoding="utf-8"))

    files = verify_final_inventory()
    return {
        "status": "PASS",
        "output_directory": str(OUT),
        "reader_first": PDF_NAME,
        "coverage": manifest["coverage"],
        "files": files,
        "source_archive": source_zip,
        "authority_archive": authority_zip,
    }


def self_check() -> dict:
    state = validate_prerequisites()
    source_files = source_inventory()
    authority_files = authority_inventory()
    validate_release_inputs(source_files + authority_files)
    return {
        "status": "PASS",
        "mode": "offline_prerequisite_and_contract_check",
        "credential_read": False,
        "network_called": False,
        "release_written": False,
        "release_directory": str(OUT),
        "release_inventory": list(RELEASE_FILES),
        "coverage": {
            "through_unit": EXPECTED_UNITS,
            "planned_units": EXPECTED_PLANNED_UNITS,
            "full_edition_complete": False,
            "pdf_pages": state["pdf_pages"],
            "exercises": EXPECTED_EXERCISES,
            "public_source_solutions": EXPECTED_PUBLIC_SOLUTIONS,
            "reader_media_positions": EXPECTED_MEDIA_POSITIONS,
            "backend_records": state["backend_records"],
        },
        "source_archive_files": len(source_files),
        "authority_archive_files": len(authority_files),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--package", action="store_true")
    args = parser.parse_args()
    if sum((args.self_check, args.package)) != 1:
        raise SystemExit("Choose exactly one of --self-check or --package")
    result = self_check() if args.self_check else package()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
