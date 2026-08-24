#!/usr/bin/env python3
"""Publish the verified Unit 15 checkpoint in the existing Zenodo concept.

The self-check is offline and fail-closed. It requires the complete packaged
release, but never reads credentials or calls Zenodo.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
U7_PATH = ROOT / "scripts" / "publish_unit_07_zenodo.py"
spec = importlib.util.spec_from_file_location("unit07_zenodo_helpers", U7_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load Zenodo publication helpers")
zenodo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(zenodo)

zenodo.ROOT = ROOT
zenodo.RELEASE = ROOT / "release" / "unit-15"
zenodo.TOKEN_FILE = Path.home() / "Documents" / "Obsidian notes" / "New zenodo token.md"
zenodo.RESERVATION = ROOT / "qa" / "UNIT_15_ZENODO_RESERVATION.json"
zenodo.RECEIPT = ROOT / "qa" / "UNIT_15_ZENODO_PUBLICATION.json"
zenodo.PREVIOUS_RECORD_ID = 22074716
zenodo.CONCEPT_DOI = "10.5281/zenodo.22059686"
zenodo.TITLE = "Kurva Aljabar — Edisi Bahasa Indonesia"
zenodo.VERSION = "unit-15"
zenodo.FILES = [
    "kurva-aljabar-id-unit-15.pdf",
    "kurva-aljabar-id-unit-15.html",
    "kurva-aljabar-id-unit-15-source.zip",
    "kurva-aljabar-id-unit-15-authority-witnesses.zip",
    "BUILD_RECEIPT-unit-15.json",
    "LICENSE-unit-15.md",
    "ZENODO_FILE_MANIFEST-unit-15.json",
    "MIGRATION_RECEIPT.json",
]

TITLE = zenodo.TITLE
VERSION = zenodo.VERSION
CONCEPT_DOI = zenodo.CONCEPT_DOI
PREVIOUS_RECORD_ID = zenodo.PREVIOUS_RECORD_ID
RELEASE = zenodo.RELEASE
RESERVATION = zenodo.RESERVATION
PUBLICATION_RECEIPT = zenodo.RECEIPT

ORGANIZATION_HUB = "https://github.com/KokunoYumeto/program-matematika-indonesia"
MODEL_ID = "OpenAI Codex gpt-5.6-sol, Ultra"
PROVENANCE = f"{MODEL_ID}."

EXPECTED_UNITS = 15
EXPECTED_PLANNED_UNITS = 30
EXPECTED_EXERCISES = 423
EXPECTED_PUBLIC_SOLUTIONS = 75
EXPECTED_MEDIA_POSITIONS = 69

PDF_NAME = zenodo.FILES[0]
HTML_NAME = zenodo.FILES[1]
SOURCE_ZIP_NAME = zenodo.FILES[2]
AUTHORITY_ZIP_NAME = zenodo.FILES[3]
BUILD_RECEIPT_NAME = zenodo.FILES[4]
LICENSE_NAME = zenodo.FILES[5]
MANIFEST_NAME = zenodo.FILES[6]
MIGRATION_NAME = zenodo.FILES[7]

PDF_SOURCE = "build/reader-id/algebraic-geometry-bridge-id-units-01-15.pdf"
HTML_SOURCE = "build/reader-id/index.html"
MIGRATION_SCHEMA_SOURCE = (
    "backend/common-backend-v1-contract/upstream/"
    "backend-migration-receipt-v1.v0.42.0.schema.json"
)


def sha256(path: Path) -> str:
    return zenodo.sha256(path)


def load_json(path: Path, label: str) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Invalid {label} JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} must contain a JSON object")
    return value


def require_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise RuntimeError(f"{label} mismatch: expected {expected!r}, found {actual!r}")


def require_positive_int(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise RuntimeError(f"{label} must be a positive integer")
    return value


def file_descriptor(name: str) -> dict:
    path = RELEASE / name
    if not path.is_file():
        raise FileNotFoundError(path)
    return {"name": name, "bytes": path.stat().st_size, "sha256": sha256(path)}


def validate_named_descriptor(value: object, name: str, label: str) -> dict:
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} must be a descriptor object")
    wanted = file_descriptor(name)
    require_equal(value.get("name"), name, f"{label}.name")
    require_equal(value.get("bytes"), wanted["bytes"], f"{label}.bytes")
    require_equal(value.get("sha256"), wanted["sha256"], f"{label}.sha256")
    return wanted


def validate_build_descriptor(
    value: object,
    expected_path: str,
    release_name: str,
    label: str,
) -> None:
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} must be a descriptor object")
    require_equal(value.get("path"), expected_path, f"{label}.path")
    release_descriptor = file_descriptor(release_name)
    require_equal(value.get("bytes"), release_descriptor["bytes"], f"{label}.bytes")
    require_equal(value.get("sha256"), release_descriptor["sha256"], f"{label}.sha256")


def validate_zip(path: Path, required_entries: set[str], label: str) -> dict:
    prefix = "algebraic-geometry-bridge-id/"
    try:
        with zipfile.ZipFile(path, "r") as archive:
            names = archive.namelist()
            if not names or names != sorted(names) or len(names) != len(set(names)):
                raise RuntimeError(f"{label} inventory is empty, unsorted, or duplicated")
            if any(not name.startswith(prefix) or ".." in Path(name).parts for name in names):
                raise RuntimeError(f"{label} contains an unbounded entry")
            missing = sorted(required_entries - set(names))
            if missing:
                raise RuntimeError(f"{label} lacks required entries: {missing}")
            corrupt = archive.testzip()
            if corrupt is not None:
                raise RuntimeError(f"{label} CRC failure: {corrupt}")
            uncompressed = sum(item.file_size for item in archive.infolist())
    except zipfile.BadZipFile as exc:
        raise RuntimeError(f"{label} is not a valid ZIP archive") from exc
    return {
        "entries": len(names),
        "uncompressed_bytes": uncompressed,
        "crc_verified": True,
    }


def validate_release_contract() -> dict:
    if not RELEASE.is_dir():
        raise FileNotFoundError(RELEASE)
    entries = list(RELEASE.iterdir())
    if any(not item.is_file() for item in entries):
        raise RuntimeError("Unit 15 release directory contains a non-file entry")
    actual_names = {item.name for item in entries}
    require_equal(actual_names, set(zenodo.FILES), "Unit 15 release inventory")
    if len(entries) != len(zenodo.FILES) or len(set(zenodo.FILES)) != 8:
        raise RuntimeError("Unit 15 release must contain exactly eight unique files")

    manifest = load_json(RELEASE / MANIFEST_NAME, "release manifest")
    require_equal(
        manifest.get("schema"),
        "ag-bridge-release-file-manifest-v2",
        "release manifest schema",
    )
    require_equal(manifest.get("title"), TITLE, "release manifest title")
    require_equal(manifest.get("version"), VERSION, "release manifest version")
    require_equal(manifest.get("language"), "id-ID", "release manifest language")
    require_equal(manifest.get("tool_provenance"), PROVENANCE, "release manifest provenance")

    coverage = manifest.get("coverage")
    if not isinstance(coverage, dict):
        raise RuntimeError("Release manifest coverage is missing")
    require_equal(coverage.get("through_unit"), EXPECTED_UNITS, "coverage through_unit")
    require_equal(coverage.get("planned_units"), EXPECTED_PLANNED_UNITS, "coverage planned_units")
    require_equal(coverage.get("full_edition_complete"), False, "coverage completion flag")
    require_equal(coverage.get("exercises"), EXPECTED_EXERCISES, "coverage exercises")
    require_equal(
        coverage.get("public_source_solutions"),
        EXPECTED_PUBLIC_SOLUTIONS,
        "coverage public solutions",
    )
    require_equal(
        coverage.get("reader_media_positions"),
        EXPECTED_MEDIA_POSITIONS,
        "coverage media positions",
    )
    pages = require_positive_int(coverage.get("pdf_pages"), "coverage PDF pages")
    backend_records = require_positive_int(
        coverage.get("backend_records"),
        "coverage backend records",
    )

    rights = manifest.get("rights")
    if not isinstance(rights, dict):
        raise RuntimeError("Release manifest rights are missing")
    require_equal(rights.get("translated_text"), "CC BY-SA 4.0", "translated-text licence")
    require_equal(
        rights.get("blanket_payload_license_claimed"),
        False,
        "blanket payload licence flag",
    )
    require_equal(
        rights.get("independent_non_endorsed_derivative"),
        True,
        "non-endorsement flag",
    )

    zenodo_section = manifest.get("zenodo")
    if not isinstance(zenodo_section, dict):
        raise RuntimeError("Release manifest Zenodo section is missing")
    require_equal(zenodo_section.get("concept_doi"), CONCEPT_DOI, "manifest concept DOI")
    require_equal(zenodo_section.get("reader_first"), PDF_NAME, "reader-first file")
    bound = zenodo_section.get("files_excluding_this_manifest")
    if not isinstance(bound, list):
        raise RuntimeError("Release manifest file descriptors are missing")
    bound_names = [item.get("name") for item in bound if isinstance(item, dict)]
    expected_bound_names = [name for name in zenodo.FILES if name != MANIFEST_NAME]
    require_equal(bound_names, expected_bound_names, "manifest-bound file order")
    for index, name in enumerate(expected_bound_names):
        validate_named_descriptor(bound[index], name, f"manifest files[{index}]")

    build = load_json(RELEASE / BUILD_RECEIPT_NAME, "build receipt")
    require_equal(build.get("schema"), "ag-bridge-build-receipt-v2", "build receipt schema")
    require_equal(build.get("language"), "id-ID", "build receipt language")
    require_equal(build.get("through_unit"), EXPECTED_UNITS, "build receipt through_unit")
    outputs = build.get("outputs")
    if not isinstance(outputs, list):
        raise RuntimeError("Build receipt outputs must be a list")
    by_path = {
        item.get("path"): item
        for item in outputs
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }
    require_equal(set(by_path), {PDF_SOURCE, HTML_SOURCE}, "build receipt output inventory")
    validate_build_descriptor(by_path[PDF_SOURCE], PDF_SOURCE, PDF_NAME, "build PDF")
    validate_build_descriptor(by_path[HTML_SOURCE], HTML_SOURCE, HTML_NAME, "build HTML")

    migration = load_json(RELEASE / MIGRATION_NAME, "sanitized migration receipt")
    if "public_artifacts" in migration:
        raise RuntimeError("Sanitized migration receipt retains stale public-artifact data")
    require_equal(migration.get("credentials_recorded"), False, "migration credential flag")
    require_equal(
        migration.get("migration_mode"),
        "additive zero-copy adapter",
        "migration mode",
    )
    source = migration.get("source")
    migration_coverage = migration.get("coverage")
    transformation = migration.get("transformation")
    validation = migration.get("validation")
    if not all(
        isinstance(value, dict)
        for value in (source, migration_coverage, transformation, validation)
    ):
        raise RuntimeError("Sanitized migration receipt lacks a required structured section")
    require_equal(source.get("through_unit"), EXPECTED_UNITS, "migration source through_unit")
    require_equal(source.get("record_count"), backend_records, "migration source records")
    require_equal(
        migration_coverage.get("through_unit"),
        EXPECTED_UNITS,
        "migration coverage through_unit",
    )
    require_equal(
        migration_coverage.get("native_records"),
        backend_records,
        "migration native records",
    )
    require_equal(
        migration_coverage.get("native_ids_preserved"),
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
    schema = load_json(ROOT / MIGRATION_SCHEMA_SOURCE, "migration receipt schema")
    errors = sorted(
        Draft202012Validator(schema).iter_errors(migration),
        key=lambda item: "/".join(str(part) for part in item.path),
    )
    if errors:
        rendered = "; ".join(error.message for error in errors[:5])
        raise RuntimeError(f"Sanitized migration receipt schema failure: {rendered}")

    license_text = (RELEASE / LICENSE_NAME).read_text(encoding="utf-8")
    normalized_license_text = " ".join(license_text.split())
    required_license_markers = (
        "CC BY-SA 4.0",
        "RIGHTS-unit-15.csv",
        "independent edition",
        "does not imply endorsement",
        "Third-party media",
    )
    missing_license = [
        marker for marker in required_license_markers if marker not in normalized_license_text
    ]
    if missing_license:
        raise RuntimeError(f"Published mixed-rights notice is incomplete: {missing_license}")

    prefix = "algebraic-geometry-bridge-id/"
    source_zip = validate_zip(
        RELEASE / SOURCE_ZIP_NAME,
        {
            f"{prefix}source/id-ID/lecture-15.md",
            f"{prefix}source/id-ID/worksheet-15.md",
            f"{prefix}source/id-ID/worksheet-15-solutions.md",
            f"{prefix}source/id-ID/media-credits-unit-15.md",
            f"{prefix}backend/units-01-15/MANIFEST.json",
            f"{prefix}backend/units-01-15/records.jsonl",
            f"{prefix}backend/common-backend-v1-contract/upstream/"
            "backend-migration-receipt-v1.v0.42.0.schema.json",
            f"{prefix}qa/UNITS_01_15_MACHINE_QA.json",
            f"{prefix}qa/UNITS_01_15_BACKEND_QA.json",
            f"{prefix}qa/UNIT_15_RELEASE_CANDIDATE.json",
            f"{prefix}LICENSE.md",
        },
        "source ZIP",
    )
    authority_required = {
        f"{prefix}authority/wikiversity/unit-15/UNIT_AUTHORITY_MANIFEST.json",
        f"{prefix}authority/artifacts/"
        "algebraische-kurven-osnabrueck-2025-2026-official.pdf",
    }
    authority_required.update(
        f"{prefix}authority/artifacts/lecture-{number:02d}-official.pdf"
        for number in range(1, EXPECTED_UNITS + 1)
    )
    authority_required.update(
        f"{prefix}authority/artifacts/worksheet-{number:02d}-official.pdf"
        for number in range(1, EXPECTED_UNITS + 1)
    )
    authority_zip = validate_zip(
        RELEASE / AUTHORITY_ZIP_NAME,
        authority_required,
        "authority-witness ZIP",
    )

    files = [file_descriptor(name) for name in zenodo.FILES]
    return {
        "manifest": manifest,
        "coverage": {
            "through_unit": EXPECTED_UNITS,
            "planned_units": EXPECTED_PLANNED_UNITS,
            "full_edition_complete": False,
            "pdf_pages": pages,
            "exercises": EXPECTED_EXERCISES,
            "public_source_solutions": EXPECTED_PUBLIC_SOLUTIONS,
            "reader_media_positions": EXPECTED_MEDIA_POSITIONS,
            "backend_records": backend_records,
        },
        "files": files,
        "source_zip": source_zip,
        "authority_zip": authority_zip,
    }


def format_id_number(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def current_boundary_contract() -> dict:
    """Return the frozen QA/backend coverage before release packaging exists."""
    machine = load_json(ROOT / "qa" / "UNITS_01_15_MACHINE_QA.json", "machine QA")
    backend = load_json(
        ROOT / "backend" / "units-01-15" / "MANIFEST.json",
        "native backend manifest",
    )
    require_equal(machine.get("status"), "PASS", "machine QA status")
    require_equal(machine.get("through_unit"), EXPECTED_UNITS, "machine QA boundary")
    require_equal(backend.get("through_unit"), EXPECTED_UNITS, "backend boundary")
    require_equal((backend.get("counts") or {}).get("exercise"), EXPECTED_EXERCISES, "backend exercises")
    require_equal((backend.get("counts") or {}).get("solution"), EXPECTED_PUBLIC_SOLUTIONS, "backend solutions")
    require_equal((backend.get("counts") or {}).get("asset"), EXPECTED_MEDIA_POSITIONS, "backend assets")
    return {
        "coverage": {
            "through_unit": EXPECTED_UNITS,
            "planned_units": EXPECTED_PLANNED_UNITS,
            "full_edition_complete": False,
            "pdf_pages": require_positive_int((machine.get("pdf") or {}).get("pages"), "machine QA PDF pages"),
            "exercises": EXPECTED_EXERCISES,
            "public_source_solutions": EXPECTED_PUBLIC_SOLUTIONS,
            "reader_media_positions": EXPECTED_MEDIA_POSITIONS,
            "backend_records": require_positive_int(backend.get("record_count"), "backend record count"),
        }
    }


def metadata(contract: dict | None = None) -> dict:
    if contract is None:
        manifest_path = RELEASE / MANIFEST_NAME
        contract = validate_release_contract() if manifest_path.is_file() else current_boundary_contract()
    coverage = contract["coverage"]
    pages = coverage["pdf_pages"]
    backend_records = coverage["backend_records"]
    pages_id = format_id_number(pages)
    records_id = format_id_number(backend_records)
    payload = {
        "title": TITLE,
        "upload_type": "publication",
        "publication_type": "book",
        "description": (
            "<p><strong>Rilis kumulatif kerja Bahasa Indonesia (id-ID), Unit 1–15</strong>, "
            "dari <em>Algebraische Kurven (Osnabrück 2025–2026)</em> karya Holger Brenner. "
            "Checkpoint parsial ini memuat lima belas kuliah, lima belas lembar kerja dengan "
            "423 soal, seluruh 75 solusi publik yang tersedia pada revisi sumber yang "
            "dibekukan, dan 69 posisi media pembaca yang dilengkapi kredit. Ini belum "
            "merupakan edisi 30-unit yang lengkap; penerjemahan berlanjut dalam urutan sumber.</p>"
            f"<p>Paket preservasi memuat pembaca PDF A4 {pages_id} halaman, pembaca HTML "
            "mandiri dengan MathML dan reflow seluler, snapshot sumber/backend asli "
            f"{records_id} rekaman yang dapat dilanjutkan, adapter backend modular "
            "tervalidasi, manifest, build receipt, saksi otoritas, hak komponen, dan bukti "
            "QA. Terjemahan dan penataan ulang teks kursus berada di bawah CC BY-SA 4.0; "
            "setiap media pihak ketiga mempertahankan pencipta, sumber, dan lisensi "
            "komponennya sendiri. Edisi independen ini disiapkan atas arahan pengguna "
            f"dengan {PROVENANCE} Ini bukan terbitan resmi Holger Brenner, Universitas "
            "Osnabrück, Wikiversity, atau Wikimedia Foundation, dan tidak menyiratkan "
            "dukungan mereka.</p>"
            "<p><strong>English identification:</strong> Cumulative working Indonesian "
            "(id-ID) edition, Units 1–15, of Holger Brenner's <em>Algebraische Kurven "
            "(Osnabrück 2025–2026)</em>, with 423 exercises, all 75 frozen public-source "
            f"solutions, 69 credited reader-media positions, self-contained HTML, a "
            f"{pages}-page A4 PDF, and an editable {backend_records:,}-record native-backend "
            "snapshot with a validated modular adapter, component-rights records, authority "
            "witnesses, and QA evidence. This is an independent, non-endorsed derivative "
            "and not yet the complete 30-unit edition.</p>"
        ),
        "creators": [{"name": "Brenner, Holger"}],
        "contributors": [
            {"name": "TTP", "type": "Other", "affiliation": ORGANIZATION_HUB},
            {"name": MODEL_ID, "type": "Other"},
        ],
        "access_right": "open",
        "license": "other-open",
        "keywords": [
            "geometri aljabar",
            "algebraic geometry",
            "Bahasa Indonesia",
            "id-ID",
            "kurva aljabar",
            "open textbook",
        ],
        "language": "ind",
        "version": VERSION,
        "related_identifiers": [
            {
                "identifier": (
                    "https://de.wikiversity.org/wiki/"
                    "Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)"
                ),
                "relation": "isDerivedFrom",
                "resource_type": "publication-book",
            },
            {
                "identifier": ORGANIZATION_HUB,
                "relation": "isReferencedBy",
                "resource_type": "software",
            },
        ],
    }
    validate_metadata(payload, contract)
    return payload


def validate_metadata(payload: dict, contract: dict) -> None:
    coverage = contract["coverage"]
    description = payload.get("description", "")
    title = payload.get("title", "")
    contributors = payload.get("contributors", [])
    creators = payload.get("creators", [])
    ttp_entries = [item for item in contributors if item.get("name") == "TTP"]
    model_entries = [item for item in contributors if item.get("name") == MODEL_ID]
    normalized_model_entries = [
        {key: value for key, value in item.items() if value is not None}
        for item in model_entries
    ]
    normalized_creators = [
        {key: value for key, value in item.items() if value is not None}
        for item in creators
    ]

    require_equal(title, TITLE, "Zenodo title")
    if "TTP" in title or "TTP" in description:
        raise RuntimeError("TTP leaked into the title or description")
    require_equal(
        json.dumps(payload, ensure_ascii=False).count("TTP"),
        1,
        "Zenodo metadata TTP occurrence count",
    )
    require_equal(
        ttp_entries,
        [{"name": "TTP", "type": "Other", "affiliation": ORGANIZATION_HUB}],
        "Zenodo organization contributor",
    )
    require_equal(
        normalized_model_entries,
        [{"name": MODEL_ID, "type": "Other"}],
        "Zenodo model contributor",
    )
    require_equal(normalized_creators, [{"name": "Brenner, Holger"}], "Zenodo creators")
    require_equal(payload.get("access_right"), "open", "Zenodo access right")
    require_equal(
        license_id(payload.get("license")),
        "other-open",
        "Zenodo mixed-rights licence",
    )
    require_equal(payload.get("language"), "ind", "Zenodo language")
    require_equal(payload.get("version"), VERSION, "Zenodo version")
    if PROVENANCE not in description:
        raise RuntimeError("Exact model provenance is absent from the Zenodo description")

    markers = (
        "Unit 1–15",
        "423 soal",
        "75 solusi publik",
        "69 posisi media pembaca",
        f"{format_id_number(coverage['pdf_pages'])} halaman",
        f"{format_id_number(coverage['backend_records'])} rekaman",
        "CC BY-SA 4.0",
        "lisensi komponennya sendiri",
        "belum merupakan edisi 30-unit yang lengkap",
        "tidak menyiratkan dukungan mereka",
        "Units 1–15",
        "independent, non-endorsed derivative",
    )
    missing = [marker for marker in markers if marker not in description]
    if missing:
        raise RuntimeError(f"Required Unit 15 description markers are missing: {missing}")


def expected_files() -> dict[str, dict[str, object]]:
    contract = validate_release_contract()
    return {
        item["name"]: {"bytes": item["bytes"], "sha256": item["sha256"]}
        for item in contract["files"]
    }


base_public_latest = zenodo.public_latest


def public_latest() -> dict:
    record = base_public_latest()
    if record.get("conceptdoi") != CONCEPT_DOI:
        raise RuntimeError("Zenodo concept DOI mismatch")
    record_id = int(record["id"])
    public_metadata = record.get("metadata") or {}
    public_version = public_metadata.get("version")
    if public_version == VERSION:
        require_equal(public_metadata.get("title"), TITLE, "existing Unit 15 public title")
        if record_id == PREVIOUS_RECORD_ID:
            raise RuntimeError("Unit 15 cannot reuse the previous public record identity")
        return record
    if record_id != PREVIOUS_RECORD_ID:
        raise RuntimeError(
            "A different Zenodo version became latest after record 22074716; "
            "refusing to create Unit 15 from an unreviewed predecessor"
        )
    require_equal(public_metadata.get("title"), TITLE, "previous Zenodo record title")
    return record


base_reservation_descriptor = zenodo.reservation_descriptor


def reservation_descriptor(draft: dict, state: str) -> dict:
    receipt = base_reservation_descriptor(draft, state)
    require_equal(receipt.get("concept_doi"), CONCEPT_DOI, "reservation concept DOI")
    require_equal(receipt.get("version"), VERSION, "reservation version")
    require_equal(receipt.get("title"), TITLE, "reservation title")
    receipt["previous_record_id"] = PREVIOUS_RECORD_ID
    receipt["reader_boundary"] = {
        "units": EXPECTED_UNITS,
        "planned_units": EXPECTED_PLANNED_UNITS,
        "exercises": EXPECTED_EXERCISES,
        "public_solutions": EXPECTED_PUBLIC_SOLUTIONS,
        "media_positions": EXPECTED_MEDIA_POSITIONS,
    }
    receipt["declared_files"] = list(zenodo.FILES)
    manifest_path = RELEASE / MANIFEST_NAME
    if manifest_path.is_file():
        contract = validate_release_contract()
        receipt["reader_boundary"] = dict(contract["coverage"])
        receipt["files"] = list(contract["files"])
        receipt["release_contract_state"] = "verified"
    else:
        receipt["release_contract_state"] = "awaiting_package"
    receipt["credential_handling"] = {
        "credential_value_logged_or_persisted": False,
        "credential_file_path_recorded": False,
    }
    return receipt


def license_id(metadata_value: object) -> str | None:
    if isinstance(metadata_value, dict):
        value = metadata_value.get("id")
        return value if isinstance(value, str) else None
    return metadata_value if isinstance(metadata_value, str) else None


def write_receipt(record: dict, verified: list[dict]) -> None:
    contract = validate_release_contract()
    public_metadata = record.get("metadata") or {}
    validate_metadata(public_metadata, contract)
    require_equal(record.get("conceptdoi"), CONCEPT_DOI, "public concept DOI")
    require_equal(public_metadata.get("version"), VERSION, "public version")
    require_equal(public_metadata.get("title"), TITLE, "public title")
    if int(record["id"]) == PREVIOUS_RECORD_ID:
        raise RuntimeError("Published Unit 15 record reused the predecessor record ID")
    require_equal(
        license_id(public_metadata.get("license")),
        "other-open",
        "public mixed-rights licence",
    )

    expected = {item["name"]: item for item in contract["files"]}
    verified_names = [item.get("name") for item in verified]
    require_equal(verified_names, zenodo.FILES, "anonymous readback file order")
    if len(set(verified_names)) != 8:
        raise RuntimeError("Anonymous readback did not verify eight unique files")
    for item in verified:
        name = item["name"]
        wanted = expected[name]
        require_equal(item.get("bytes"), wanted["bytes"], f"public {name} bytes")
        require_equal(item.get("sha256"), wanted["sha256"], f"public {name} sha256")
        require_equal(item.get("public_readback"), True, f"public {name} readback flag")

    contributors = public_metadata.get("contributors", [])
    receipt = {
        "schema": "ag-bridge-zenodo-publication-receipt-v3",
        "status": "PASS",
        "record": {
            "id": int(record["id"]),
            "url": record["links"]["self_html"],
            "api_url": record["links"]["self"],
            "doi": public_metadata["doi"],
            "concept_doi": record["conceptdoi"],
            "previous_record_id": PREVIOUS_RECORD_ID,
            "title": public_metadata["title"],
            "version": public_metadata["version"],
            "publication_date": public_metadata["publication_date"],
            "published_timestamp": record.get("created"),
            "zenodo_state": "done",
            "zenodo_status": "published",
        },
        "reader_boundary": dict(contract["coverage"]),
        "metadata_cleanliness": {
            "creator": "Brenner, Holger",
            "creator_count": len(public_metadata.get("creators", [])),
            "organization_name": "TTP",
            "organization_contributor_count": sum(
                item.get("name") == "TTP" for item in contributors
            ),
            "organization_hub": ORGANIZATION_HUB,
            "model_contributor": MODEL_ID,
            "model_contributor_count": sum(
                item.get("name") == MODEL_ID for item in contributors
            ),
            "exact_model_provenance": PROVENANCE,
            "work_title_preserved_without_organization_prefix": not TITLE.startswith("TTP"),
            "description_lead_preserved_without_organization_prefix": not public_metadata[
                "description"
            ].lstrip().startswith("TTP"),
            "non_endorsement_disclosed": True,
            "license_field": "other-open",
            "license_field_rationale": (
                "Avoids applying a false blanket licence to the mixed-rights file set."
            ),
            "translated_course_text_license": "CC BY-SA 4.0",
            "third_party_media_license_policy": (
                "Per-component rights and attribution are preserved in the source package."
            ),
        },
        "anonymous_public_byte_readback": {
            "verified_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "credential_used": False,
            "files_expected": 8,
            "files_verified": len(verified),
            "all_size_and_sha256_matches": True,
            "files": verified,
        },
        "credential_handling": {
            "public_readback_used_anonymous_requests": True,
            "credential_value_logged_or_persisted": False,
            "credential_file_path_recorded": False,
        },
    }
    PUBLICATION_RECEIPT.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


zenodo.metadata = metadata
zenodo.expected_files = expected_files
zenodo.public_latest = public_latest
zenodo.reservation_descriptor = reservation_descriptor
zenodo.write_receipt = write_receipt

base_preflight = zenodo.preflight
base_reserve = zenodo.reserve
base_publish = zenodo.publish


def self_check() -> dict:
    contract = validate_release_contract()
    payload = metadata(contract)
    require_equal(PREVIOUS_RECORD_ID, 22074716, "previous Zenodo record ID")
    require_equal(CONCEPT_DOI, "10.5281/zenodo.22059686", "Zenodo concept DOI")
    require_equal(RELEASE, ROOT / "release" / "unit-15", "Unit 15 release directory")
    require_equal(len(zenodo.FILES), 8, "Zenodo file count")
    require_equal(len(set(zenodo.FILES)), 8, "Zenodo unique file count")
    return {
        "status": "PASS",
        "mode": "offline_release_and_metadata_contract",
        "credential_read": False,
        "network_called": False,
        "title": payload["title"],
        "version": payload["version"],
        "previous_record_id": PREVIOUS_RECORD_ID,
        "concept_doi": CONCEPT_DOI,
        "license": payload["license"],
        "reader_first": PDF_NAME,
        "coverage": contract["coverage"],
        "files": contract["files"],
        "source_zip": contract["source_zip"],
        "authority_zip": contract["authority_zip"],
        "exact_provenance_present": PROVENANCE in payload["description"],
        "metadata_ttp_occurrences": json.dumps(payload, ensure_ascii=False).count("TTP"),
    }


def preflight() -> dict:
    contract = validate_release_contract()
    result = base_preflight()
    result["reader_boundary"] = dict(contract["coverage"])
    result["release_contract_verified"] = True
    return result


def validate_existing_reservation() -> None:
    if not RESERVATION.is_file():
        return
    receipt = load_json(RESERVATION, "existing reservation receipt")
    require_equal(receipt.get("status"), "PASS", "existing reservation status")
    require_equal(receipt.get("concept_doi"), CONCEPT_DOI, "existing reservation concept DOI")
    require_equal(receipt.get("version"), VERSION, "existing reservation version")
    require_equal(receipt.get("title"), TITLE, "existing reservation title")
    require_equal(
        receipt.get("previous_record_id"),
        PREVIOUS_RECORD_ID,
        "existing reservation predecessor",
    )
    if receipt.get("credentials_recorded") is not False:
        raise RuntimeError("Existing reservation receipt is not sanitized")


def recover_unreceipted_draft() -> dict | None:
    """Recover a new-version draft created before its local receipt was written."""
    if RESERVATION.is_file():
        return None
    token = zenodo.token_from_file()
    session = zenodo.requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})
    response = zenodo.request(
        session,
        "GET",
        f"{zenodo.BASE}/api/deposit/depositions",
        params={"status": "draft", "sort": "mostrecent", "size": 100},
    )
    candidates = [
        item
        for item in response.json()
        if not item.get("submitted")
        and str(item.get("conceptrecid")) == CONCEPT_DOI.rsplit(".", 1)[-1]
    ]
    if not candidates:
        del token
        return None
    if len(candidates) != 1:
        raise RuntimeError(
            f"Expected one unsubmitted draft in concept {CONCEPT_DOI}, found {len(candidates)}"
        )
    draft = candidates[0]
    draft = zenodo.request(
        session,
        "PUT",
        draft["links"]["self"],
        json={"metadata": metadata()},
    ).json()
    if draft.get("submitted"):
        raise RuntimeError("Recovered Zenodo draft unexpectedly reports submitted=true")
    descriptor = reservation_descriptor(draft, "recovered_reserved_draft")
    RESERVATION.write_text(
        json.dumps(descriptor, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    del token
    return descriptor


def reserve() -> dict:
    validate_existing_reservation()
    recovered = recover_unreceipted_draft()
    if recovered is not None:
        return recovered
    return base_reserve()


def publish() -> dict:
    validate_release_contract()
    validate_existing_reservation()
    result = base_publish()
    if result.get("action") == "verified_existing_unit_07":
        result["action"] = "verified_existing_unit_15"
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--reserve", action="store_true")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    if sum((args.self_check, args.preflight, args.reserve, args.publish)) != 1:
        raise SystemExit(
            "Choose exactly one of --self-check, --preflight, --reserve, or --publish"
        )
    if args.self_check:
        result = self_check()
    elif args.preflight:
        result = preflight()
    elif args.reserve:
        result = reserve()
    else:
        result = publish()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
