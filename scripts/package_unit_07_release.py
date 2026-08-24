#!/usr/bin/env python3
"""Create and verify the bounded cumulative Unit 7 preservation payload."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "release" / "unit-07"
PREFIX = "algebraic-geometry-bridge-id"
FIXED_ZIP_TIME = (2026, 8, 22, 0, 0, 0)
TEXT_SUFFIXES = {".cff", ".csv", ".html", ".json", ".jsonl", ".md", ".py", ".tex", ".txt", ".xml"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact(path: str) -> Path:
    candidate = ROOT / path
    if not candidate.is_file():
        raise FileNotFoundError(path)
    return candidate


def tree(path: str) -> list[Path]:
    base = ROOT / path
    if not base.is_dir():
        raise FileNotFoundError(path)
    return sorted((item for item in base.rglob("*") if item.is_file()), key=lambda p: p.as_posix())


def unique(paths: list[Path]) -> list[Path]:
    table = {path.relative_to(ROOT).as_posix(): path for path in paths}
    return [table[key] for key in sorted(table)]


def zip_files(target: Path, paths: list[Path]) -> dict:
    if target.exists():
        raise FileExistsError(f"Refusing to overwrite {target}")
    expected: dict[str, dict[str, object]] = {}
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source in unique(paths):
            relative = source.relative_to(ROOT).as_posix()
            archive_name = f"{PREFIX}/{relative}"
            data = source.read_bytes()
            info = zipfile.ZipInfo(archive_name, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
            expected[archive_name] = {
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }

    with zipfile.ZipFile(target, "r") as archive:
        names = archive.namelist()
        if names != sorted(expected):
            raise RuntimeError(f"Archive order/inventory mismatch: {target.name}")
        if archive.testzip() is not None:
            raise RuntimeError(f"CRC failure: {target.name}")
        for name in names:
            data = archive.read(name)
            wanted = expected[name]
            if len(data) != wanted["bytes"] or hashlib.sha256(data).hexdigest() != wanted["sha256"]:
                raise RuntimeError(f"Archive entry mismatch: {target.name}:{name}")

    return {
        "name": target.name,
        "bytes": target.stat().st_size,
        "sha256": sha256(target),
        "entries": len(expected),
        "uncompressed_bytes": sum(int(item["bytes"]) for item in expected.values()),
        "verified": True,
    }


def copy_exact(source: Path, name: str) -> Path:
    target = OUT / name
    if target.exists():
        raise FileExistsError(f"Refusing to overwrite {target}")
    shutil.copyfile(source, target)
    if target.stat().st_size != source.stat().st_size or sha256(target) != sha256(source):
        raise RuntimeError(f"Copy mismatch: {name}")
    return target


def descriptor(path: Path) -> dict:
    return {"name": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}


def validate_release_inputs(paths: list[Path]) -> None:
    """Reject profile-local paths, personal-name residue, or credential files."""
    local_profile_marker = Path.home().name.encode("utf-8")
    forbidden_bytes = (
        b"C:" + b"\\" + b"Users" + b"\\",
        b"/" + b"Users" + b"/",
        b"-----BEGIN " + b"PRIVATE KEY-----",
    )
    for path in unique(paths):
        relative = path.relative_to(ROOT).as_posix()
        lower = relative.lower()
        if lower.endswith("token.md") or "/tokens/" in lower or "/credentials/" in lower:
            raise RuntimeError(f"Credential-bearing path selected for release: {relative}")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        data = path.read_bytes()
        if any(marker in data for marker in forbidden_bytes) or (
            len(local_profile_marker) >= 3 and local_profile_marker in data
        ):
            raise RuntimeError(f"Unsanitized release input: {relative}")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    if any(OUT.iterdir()):
        raise RuntimeError(f"Release directory must be empty: {OUT}")

    source_files: list[Path] = [
        exact("README.md"),
        exact("CITATION.cff"),
        exact("LICENSE.md"),
        exact("build/reader-id/BUILD_RECEIPT.json"),
        exact("qa/UNIT_07_RELEASE_CANDIDATE.json"),
        exact("qa/UNITS_01_07_HANDOFF.md"),
        exact("qa/UNITS_01_07_MACHINE_QA.json"),
        exact("qa/UNITS_01_07_VISUAL_QA.json"),
        exact("qa/UNITS_01_07_RESPONSIVE_QA.json"),
        exact("qa/UNIT_07_PROTECTED_SURFACES.json"),
        exact("qa/UNITS_01_07_BACKEND_QA.json"),
        exact("qa/TERMINOLOGY_MIGRATION_UNIT_07.json"),
        exact("qa/TERMINOLOGY_QA_RECEIPT.json"),
        exact("backend/common-backend-v1/MIGRATION_RECEIPT.json"),
        exact("qa/UNIT_07_ZENODO_RESERVATION.json"),
        exact("qa/UNIT_06_ZENODO_PUBLICATION.json"),
        exact("qa/UNIT_06_FIGSHARE_PUBLICATION.json"),
        exact("authority/terminology-id-arxiv/TERMINOLOGY_QA_REPORT.md"),
        exact("authority/terminology-id-arxiv/SOURCE_MANIFEST.json"),
    ]
    for directory in (
        "source/id-ID",
        "authority/assets",
        "backend/units-01-07",
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
        "RIGHTS.csv",
        "RIGHTS-unit-02.csv",
        "RIGHTS-unit-03.csv",
        "RIGHTS-unit-04.csv",
        "RIGHTS-unit-05.csv",
        "RIGHTS-unit-06.csv",
        "RIGHTS-unit-07.csv",
        "ASSET_CLOSURE.json",
        "ASSET_CLOSURE-unit-02.json",
        "ASSET_CLOSURE-unit-03.json",
        "ASSET_CLOSURE-unit-04.json",
        "ASSET_CLOSURE-unit-05.json",
        "ASSET_CLOSURE-unit-06.json",
        "ASSET_CLOSURE-unit-07.json",
        "commons-imageinfo-lecture-01.json",
        "commons-imageinfo-unit-02.json",
        "commons-imageinfo-unit-03.json",
        "commons-imageinfo-unit-04.json",
        "commons-imageinfo-unit-05.json",
        "commons-imageinfo-unit-06.json",
        "commons-imageinfo-unit-07.json",
    ):
        source_files.append(exact(f"authority/{name}"))

    authority_files = tree("authority/wikiversity")
    for name in (
        "algebraische-kurven-osnabrueck-2025-2026-official.pdf",
        "lecture-01-official.pdf",
        "lecture-02-official.pdf",
        "lecture-03-official.pdf",
        "lecture-04-official.pdf",
        "lecture-05-official.pdf",
        "lecture-06-official.pdf",
        "lecture-07-official.pdf",
        "worksheet-01-official.pdf",
        "worksheet-02-official.pdf",
        "worksheet-03-official.pdf",
        "worksheet-04-official.pdf",
        "worksheet-05-official.pdf",
        "worksheet-06-official.pdf",
        "worksheet-07-official.pdf",
    ):
        authority_files.append(exact(f"authority/artifacts/{name}"))

    validate_release_inputs(source_files)

    pdf = copy_exact(
        exact("build/reader-id/algebraic-geometry-bridge-id-units-01-07.pdf"),
        "kurva-aljabar-id-unit-07.pdf",
    )
    html = copy_exact(exact("build/reader-id/index.html"), "kurva-aljabar-id-unit-07.html")
    receipt = copy_exact(exact("build/reader-id/BUILD_RECEIPT.json"), "BUILD_RECEIPT-unit-07.json")
    license_copy = copy_exact(exact("LICENSE.md"), "LICENSE-unit-07.md")

    source_zip_path = OUT / "kurva-aljabar-id-unit-07-source.zip"
    authority_zip_path = OUT / "kurva-aljabar-id-unit-07-authority-witnesses.zip"
    source_zip = zip_files(source_zip_path, source_files)
    authority_zip = zip_files(authority_zip_path, authority_files)

    zenodo_files = [pdf, html, source_zip_path, authority_zip_path, receipt, license_copy]
    figshare_files = [pdf, html, source_zip_path, license_copy]
    manifest = {
        "schema": "ag-bridge-release-file-manifest-v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "title": "Kurva Aljabar — Edisi Bahasa Indonesia",
        "version": "unit-07",
        "language": "id-ID",
        "tool_provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
        "coverage": {
            "through_unit": 7,
            "planned_units": 30,
            "full_edition_complete": False,
            "pdf_pages": 142,
            "exercises": 197,
            "public_source_solutions": 40,
            "backend_records": 5182,
        },
        "rights": {
            "translated_text": "CC BY-SA 4.0",
            "media": "Per-component rights in RIGHTS files and reader credits",
            "blanket_payload_license_claimed": False,
            "license_notice": "LICENSE-unit-07.md and LICENSE.md inside the source ZIP",
        },
        "zenodo": {
            "concept_doi": "10.5281/zenodo.22059686",
            "files_excluding_this_manifest": [descriptor(path) for path in zenodo_files],
        },
        "figshare": {
            "project_id": 280296,
            "collection_id": 8668413,
            "collection_doi": "10.6084/m9.figshare.c.8668413.v1",
            "reader_first": pdf.name,
            "files_excluding_this_manifest": [descriptor(path) for path in figshare_files],
            "payload_bytes_excluding_this_manifest": sum(path.stat().st_size for path in figshare_files),
            "payload_cap_bytes": 500000000,
        },
        "archives": {"source": source_zip, "authority_witnesses": authority_zip},
    }
    manifest_path = OUT / "ZENODO_FILE_MANIFEST-unit-07.json"
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
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
