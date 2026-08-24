#!/usr/bin/env python3
"""Create the bounded, reader-first cumulative Unit 8 release payload."""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
U7_PATH = ROOT / "scripts" / "package_unit_07_release.py"
spec = importlib.util.spec_from_file_location("unit07_packaging_helpers", U7_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load bounded packaging helpers")
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)

helpers.OUT = ROOT / "release" / "unit-08"
helpers.PREFIX = "algebraic-geometry-bridge-id"
helpers.FIXED_ZIP_TIME = (2026, 8, 23, 0, 0, 0)
OUT = helpers.OUT


def exact(path: str) -> Path:
    return helpers.exact(path)


def tree(path: str) -> list[Path]:
    return helpers.tree(path)


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


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    if any(OUT.iterdir()):
        raise RuntimeError(f"Release directory must be empty: {OUT}")

    source_files: list[Path] = [
        exact("README.md"),
        exact("CITATION.cff"),
        exact("LICENSE.md"),
        exact("build/reader-id/BUILD_RECEIPT.json"),
        exact("qa/UNIT_08_RELEASE_CANDIDATE.json"),
        exact("qa/UNITS_01_08_HANDOFF.md"),
        exact("qa/UNITS_01_08_MACHINE_QA.json"),
        exact("qa/UNITS_01_08_VISUAL_QA.json"),
        exact("qa/UNITS_01_08_RESPONSIVE_QA.json"),
        exact("qa/UNITS_01_08_BACKEND_QA.json"),
        exact("qa/UNIT_08_PROTECTED_SURFACES.json"),
        exact("qa/TERMINOLOGY_MIGRATION_UNIT_07.json"),
        exact("qa/TERMINOLOGY_QA_RECEIPT.json"),
        exact("qa/UNITS_01_08_BACKEND_QA.json"),
        exact("authority/terminology-id-arxiv/TERMINOLOGY_QA_REPORT.md"),
        exact("authority/terminology-id-arxiv/SOURCE_MANIFEST.json"),
    ]
    for directory in (
        "source/id-ID",
        "authority/assets",
        "backend/units-01-08",
        "backend/common-backend-v1-contract",
        "scripts",
        "00_control",
    ):
        source_files.extend(tree(directory))
    for name in (
        "AUTHORITY_FREEZE.md",
        "UNIT_02_AUTHORITY_FREEZE.md",
        "UNIT_03_AUTHORITY_FREEZE.md",
        "UNIT_04_AUTHORITY_FREEZE.md",
        "UNIT_05_AUTHORITY_FREEZE.md",
        "UNIT_06_AUTHORITY_FREEZE.md",
        "UNIT_07_AUTHORITY_FREEZE.md",
        "UNIT_08_AUTHORITY_FREEZE.md",
        "RIGHTS.csv",
        "RIGHTS-unit-02.csv",
        "RIGHTS-unit-03.csv",
        "RIGHTS-unit-04.csv",
        "RIGHTS-unit-05.csv",
        "RIGHTS-unit-06.csv",
        "RIGHTS-unit-07.csv",
        "RIGHTS-unit-08.csv",
        "ASSET_CLOSURE.json",
        "ASSET_CLOSURE-unit-02.json",
        "ASSET_CLOSURE-unit-03.json",
        "ASSET_CLOSURE-unit-04.json",
        "ASSET_CLOSURE-unit-05.json",
        "ASSET_CLOSURE-unit-06.json",
        "ASSET_CLOSURE-unit-07.json",
        "ASSET_CLOSURE-unit-08.json",
        "commons-imageinfo-lecture-01.json",
        "commons-imageinfo-unit-02.json",
        "commons-imageinfo-unit-03.json",
        "commons-imageinfo-unit-04.json",
        "commons-imageinfo-unit-05.json",
        "commons-imageinfo-unit-06.json",
        "commons-imageinfo-unit-07.json",
        "commons-imageinfo-unit-08.json",
    ):
        source_files.append(exact(f"authority/{name}"))

    authority_files = tree("authority/wikiversity")
    for name in (
        "algebraische-kurven-osnabrueck-2025-2026-official.pdf",
        *[f"lecture-{n:02d}-official.pdf" for n in range(1, 9)],
        *[f"worksheet-{n:02d}-official.pdf" for n in range(1, 9)],
    ):
        authority_files.append(exact(f"authority/artifacts/{name}"))

    # The migration receipt is emitted after this archive is frozen and is
    # uploaded as a separate standalone release file; keeping it out of the
    # source archive avoids a self-referential hash cycle.
    validate_release_inputs(source_files)

    pdf = copy_exact(
        exact("build/reader-id/algebraic-geometry-bridge-id-units-01-08.pdf"),
        "kurva-aljabar-id-unit-08.pdf",
    )
    html = copy_exact(exact("build/reader-id/index.html"), "kurva-aljabar-id-unit-08.html")
    receipt = copy_exact(exact("build/reader-id/BUILD_RECEIPT.json"), "BUILD_RECEIPT-unit-08.json")
    license_copy = copy_exact(exact("LICENSE.md"), "LICENSE-unit-08.md")

    source_zip_path = OUT / "kurva-aljabar-id-unit-08-source.zip"
    authority_zip_path = OUT / "kurva-aljabar-id-unit-08-authority-witnesses.zip"
    source_zip = zip_files(source_zip_path, source_files)
    authority_zip = zip_files(authority_zip_path, authority_files)

    manifest = {
        "schema": "ag-bridge-release-file-manifest-v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "title": "Kurva Aljabar — Edisi Bahasa Indonesia",
        "version": "unit-08",
        "language": "id-ID",
        "tool_provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
        "coverage": {
            "through_unit": 8,
            "planned_units": 30,
            "full_edition_complete": False,
            "pdf_pages": 161,
            "exercises": 221,
            "public_source_solutions": 42,
            "reader_media_positions": 59,
            "backend_records": 5787,
        },
        "rights": {
            "translated_text": "CC BY-SA 4.0",
            "media": "Per-component rights in RIGHTS files and reader credits",
            "blanket_payload_license_claimed": False,
            "license_notice": "LICENSE-unit-08.md and LICENSE.md inside the source ZIP",
        },
        "zenodo": {
            "concept_doi": "10.5281/zenodo.22059686",
            "files_excluding_this_manifest_and_migration_receipt": [descriptor(path) for path in (pdf, html, source_zip_path, authority_zip_path, receipt, license_copy)],
        },
        "figshare": {
            "project_id": 280296,
            "collection_id": 8668413,
            "collection_doi": "10.6084/m9.figshare.c.8668413.v1",
            "reader_first": pdf.name,
            "files_excluding_this_manifest": [descriptor(path) for path in (pdf, html, source_zip_path, license_copy)],
            "payload_bytes_excluding_this_manifest": sum(path.stat().st_size for path in (pdf, html, source_zip_path, license_copy)),
            "payload_cap_bytes": 500000000,
        },
        "archives": {"source": source_zip, "authority_witnesses": authority_zip},
    }
    manifest_path = OUT / "ZENODO_FILE_MANIFEST-unit-08.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["figshare"]["payload_bytes_excluding_this_manifest"] + manifest_path.stat().st_size > 500000000:
        raise RuntimeError("Figshare work payload cap exceeded")

    result = {
        "status": "PASS",
        "output_directory": str(OUT),
        "files": [descriptor(path) for path in sorted(OUT.iterdir(), key=lambda p: p.name)],
        "source_archive": source_zip,
        "authority_archive": authority_zip,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

