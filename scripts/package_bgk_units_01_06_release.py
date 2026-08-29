#!/usr/bin/env python3
"""Build the deterministic reader-first BGK Units 01--06 release candidate.

This operation is offline and confined to ``release/bgk-units-01-06``.  It
fails closed until the cumulative reader, native backend, and common-backend
preflight receipts exist, carry the exact Units 01--06 scope, bind their local
artifacts by bytes and SHA-256, and report successful deterministic QA.

The source archive is intentionally resumable but compact: translated source,
component media, compact authority identities/maps/rights, ledgers, worklogs,
QA receipts, and deterministic build code are included.  Raw API/HTML/XML
dumps and official PDF witnesses remain in the local authority store and are
not duplicated in the public package.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import zipfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "release" / "bgk-units-01-06"
UNITS = tuple(range(1, 7))
FIXED_ZIP_TIME = (2026, 8, 29, 0, 0, 0)
MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."
TITLE = "Bundel, Berkas, dan Kohomologi — Unit 1–6, Bahasa Indonesia"

PDF_NAME = "01_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-06.pdf"
HTML_NAME = "02_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-06.html"
SOURCE_ZIP_NAME = "03_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-06_source.zip"
BACKEND_ZIP_NAME = "04_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-06_native-backend.zip"
LICENSE_NAME = "05_LICENSE_AND_COMPONENT_RIGHTS.md"
README_NAME = "06_README.md"
MANIFEST_NAME = "07_RELEASE_MANIFEST.json"
CHECKSUMS_NAME = "08_SHA256SUMS.txt"
QA_NAME = "09_RELEASE_CANDIDATE_QA.json"

PDF_PATH = "build/reader-bgk-id/bundel-berkas-dan-kohomologi-id-units-01-06.pdf"
HTML_PATH = "build/reader-bgk-id/index.html"
BUILD_RECEIPT_PATH = "build/reader-bgk-id/BUILD_RECEIPT.json"
READER_QA_PATH = "qa/BGK_UNITS_01_06_READER_QA.json"
BACKEND_ROOT = "backend/bgk-units-01-06"
BACKEND_MANIFEST_PATH = f"{BACKEND_ROOT}/MANIFEST.json"
BACKEND_QA_PATH = "qa/BGK_UNITS_01_06_BACKEND_QA.json"
COMMON_QA_PATH = "qa/BGK_UNITS_01_06_COMMON_ADAPTER_PREFLIGHT_QA.json"

BACKEND_TOOL_PATHS = (
    "scripts/export_backend_bgk_units_01_06.py",
    "scripts/qa_backend_bgk_units_01_06.py",
    "scripts/generate_common_backend_v1_receipts.py",
)
COMMON_CONTRACT_PATHS = (
    "backend/common-backend-v1-contract/README.md",
    "backend/common-backend-v1-contract/UPSTREAM_MANIFEST.json",
    "backend/common-backend-v1-contract/upstream/backend-migration-receipt-v1.v0.42.0.schema.json",
    "backend/common-backend-v1-contract/upstream/backend-v1.v0.41.0.schema.json",
    "backend/common-backend-v1-contract/upstream/MIGRATION_HANDOFF_V1.v0.42.0.md",
    "backend/common-backend-v1-contract/upstream/source-format-profile-v1.v0.41.0.schema.json",
)

LICENSE_TEXT = """# Licence and component-rights notice

## Course text and Indonesian derivative

The source course is Holger Brenner's *Bündel, Garben und Kohomologie
(Osnabrück 2019-2020)* on German Wikiversity. The frozen semantic course text
and this independent Indonesian translation and re-typesetting are distributed
under the **Creative Commons Attribution-ShareAlike 4.0 International licence
(CC BY-SA 4.0)**:

<https://creativecommons.org/licenses/by-sa/4.0/>

Required attribution is to Holger Brenner for the source work. The change
notice is: **Indonesian translation and re-typesetting, 2026**. Reuse must
preserve attribution, indicate changes, link the licence, and satisfy
ShareAlike. Backend records that reproduce or adapt course text follow the same
licence.

This is an independent edition. It is not an official publication of, and does
not imply endorsement by, Holger Brenner, the University of Osnabrück,
Wikiversity, Wikimedia Foundation, OpenAI, or any other upstream party.

## Official PDF witnesses

The source archive points to frozen official PDF witnesses but does not include
those PDFs. Current Wikimedia Commons metadata records CC BY-SA 4.0, while the
visible notices in the official PDFs record CC BY-SA 3.0. Both surfaces remain
bound in the authority manifests; this package makes no blanket relicensing
claim for those witnesses.

## Third-party media

No blanket package licence overrides component rights. Exact records are in
`authority/RIGHTS-bgk-unit-01.csv` through
`authority/RIGHTS-bgk-unit-06.csv` and in the reader's **Kredit media**
sections:

- Tangent-bundle diagram by Oleg Alexandrov: public domain.
- Hairy-ball illustration by RokerHRO: CC BY-SA 3.0.
- Inclusion-exclusion diagram: public domain under the frozen Commons record.
- Fiddler-crab Möbius-strip animation by Hamishtodd1: CC BY-SA 4.0; the PDF
  uses its deterministically extracted first frame.
- *Triticum spelta* photograph by André Karwath (Aka): CC BY-SA 2.5.

## Build and QA code

Repository-authored build, export, QA, and packaging code is available under
the MIT License unless the file itself states otherwise. That code licence does
not relicense course text, translated text, source witnesses, backend content,
or third-party media.

Copyright (c) 2026 Indonesian-edition contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def local_path(rel: str) -> Path:
    relative = Path(rel)
    if relative.is_absolute() or ".." in relative.parts:
        raise RuntimeError(f"Unsafe relative path: {rel}")
    path = ROOT / relative
    try:
        path.resolve().relative_to(ROOT.resolve())
    except ValueError as exc:
        raise RuntimeError(f"Path escaped release lane: {rel}") from exc
    return path


def read_bytes(rel: str) -> bytes:
    path = local_path(rel)
    if not path.is_file():
        raise RuntimeError(f"Required input missing: {rel}")
    return path.read_bytes()


def fact(rel: str, data: bytes | None = None) -> dict[str, Any]:
    payload = read_bytes(rel) if data is None else data
    return {"path": rel, "bytes": len(payload), "sha256": sha256(payload)}


def load_json(rel: str) -> tuple[dict[str, Any], bytes]:
    data = read_bytes(rel)
    try:
        value = json.loads(data.decode("utf-8"))
    except Exception as exc:
        raise RuntimeError(f"Invalid JSON: {rel}: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"Expected JSON object: {rel}")
    return value, data


def require_binding(binding: dict[str, Any], rel: str, data: bytes | None = None) -> None:
    payload = read_bytes(rel) if data is None else data
    if (
        binding.get("path") != rel
        or binding.get("bytes") != len(payload)
        or binding.get("sha256") != sha256(payload)
    ):
        raise RuntimeError(f"Receipt binding drifted: {rel}")


def require_pass(value: dict[str, Any], rel: str) -> None:
    status = value.get("status")
    if not isinstance(status, str) or not status.startswith("PASS"):
        raise RuntimeError(f"Required QA is not PASS: {rel}: {status!r}")


def validate_reader(visual_qa_rel: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, bytes]]:
    qa, qa_data = load_json(READER_QA_PATH)
    require_pass(qa, READER_QA_PATH)
    if (
        qa.get("schema") not in {
            "ag-bridge-bgk-cumulative-reader-qa-v1",
            "ag-bridge-bgk-cumulative-reader-machine-qa-v1",
        }
        or qa.get("through_unit") != 6
        or qa.get("language") != "id-ID"
        or qa.get("model_provenance") != MODEL_PROVENANCE
    ):
        raise RuntimeError("Cumulative reader QA is not the exact Units 01--06 contract")

    receipt, receipt_data = load_json(BUILD_RECEIPT_PATH)
    if (
        receipt.get("schema") != "ag-bridge-bgk-build-receipt-v1"
        or receipt.get("through_unit") != 6
        or receipt.get("language") != "id-ID"
    ):
        raise RuntimeError("Build receipt scope drifted from Units 01--06")
    require_binding(qa.get("build_receipt") or {}, BUILD_RECEIPT_PATH, receipt_data)

    outputs = {item.get("path"): item for item in receipt.get("outputs", [])}
    reader_files: dict[str, bytes] = {}
    for rel, qa_key in ((PDF_PATH, "pdf"), (HTML_PATH, "html")):
        data = read_bytes(rel)
        require_binding(outputs.get(rel) or {}, rel, data)
        require_binding(qa.get(qa_key) or {}, rel, data)
        reader_files[rel] = data

    pdf = qa.get("pdf") or {}
    html = qa.get("html") or {}
    pages = int(pdf.get("pages_pypdf") or pdf.get("pages_poppler") or 0)
    if (
        pages <= 0
        or int(pdf.get("pages_poppler") or 0) != pages
        or int(pdf.get("extractable_text_pages") or pages) != pages
        or int(pdf.get("out_of_bounds_link_annotations") or 0) != 0
        or pdf.get("encrypted") is not False
        or int(pdf.get("type_3_fonts") or 0) != 0
        or html.get("self_contained") is not True
        or html.get("duplicate_ids") != 0
        or html.get("broken_internal_anchors") != 0
        or html.get("images_missing_alt") != 0
    ):
        raise RuntimeError("Reader machine QA lacks deterministic/accessibility closure")

    if not visual_qa_rel.startswith("qa/") or not visual_qa_rel.endswith(".json"):
        raise RuntimeError("--visual-qa must name a task-local qa/*.json receipt")
    visual, visual_data = load_json(visual_qa_rel)
    require_pass(visual, visual_qa_rel)
    visual_pdf = visual.get("pdf") or {}
    pdf_data = reader_files[PDF_PATH]
    if (
        visual.get("through_unit") != 6
        or visual.get("model_provenance") != MODEL_PROVENANCE
        or visual_pdf.get("path") != PDF_PATH
        or visual_pdf.get("bytes") != len(pdf_data)
        or visual_pdf.get("sha256") != sha256(pdf_data)
        or int(visual_pdf.get("pages_rendered") or 0) != pages
        or int(visual_pdf.get("pages_visually_reviewed") or 0) != pages
        or visual_pdf.get("unintended_blank_pages") != 0
        or visual_pdf.get("clipping_overlap_bad_glyph_or_broken_equation_observed") is not False
    ):
        raise RuntimeError("Separate visual QA does not bind review of all Units 01--06 PDF pages")

    reader_inputs = {item.get("path"): item for item in receipt.get("inputs", [])}
    if len(reader_inputs) != len(receipt.get("inputs", [])):
        raise RuntimeError("Duplicate input path in build receipt")
    qa_script = qa.get("qa_script") or {}
    qa_script_rel = qa_script.get("path")
    if not isinstance(qa_script_rel, str):
        raise RuntimeError("Reader QA does not identify its QA script")
    qa_script_data = read_bytes(qa_script_rel)
    require_binding(qa_script, qa_script_rel, qa_script_data)
    return qa, receipt, {
        READER_QA_PATH: qa_data,
        visual_qa_rel: visual_data,
        BUILD_RECEIPT_PATH: receipt_data,
        qa_script_rel: qa_script_data,
        **reader_files,
    }


def validate_units() -> tuple[dict[int, dict[str, Any]], dict[int, dict[str, Any]], dict[str, bytes]]:
    authority: dict[int, dict[str, Any]] = {}
    translation: dict[int, dict[str, Any]] = {}
    data: dict[str, bytes] = {}
    for unit in UNITS:
        authority_rel = f"qa/BGK_UNIT_{unit:02d}_AUTHORITY_QA.json"
        translation_rel = f"qa/BGK_UNIT_{unit:02d}_TRANSLATION_QA.json"
        authority_qa, authority_data = load_json(authority_rel)
        translation_qa, translation_data = load_json(translation_rel)
        require_pass(authority_qa, authority_rel)
        require_pass(translation_qa, translation_rel)
        if authority_qa.get("unit") != unit or translation_qa.get("unit") != unit:
            raise RuntimeError(f"Unit QA identity drifted for Unit {unit}")
        if translation_qa.get("language") != "id-ID":
            raise RuntimeError(f"Translation QA language drifted for Unit {unit}")
        if int((translation_qa.get("counts") or {}).get("invented_solutions", 0)) != 0:
            raise RuntimeError(f"Invented-solution count is nonzero for Unit {unit}")
        authority[unit] = authority_qa
        translation[unit] = translation_qa
        data[authority_rel] = authority_data
        data[translation_rel] = translation_data
    return authority, translation, data


def validate_backend() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, bytes]]:
    manifest, manifest_data = load_json(BACKEND_MANIFEST_PATH)
    backend_qa, backend_qa_data = load_json(BACKEND_QA_PATH)
    common_qa, common_qa_data = load_json(COMMON_QA_PATH)
    require_pass(backend_qa, BACKEND_QA_PATH)
    require_pass(common_qa, COMMON_QA_PATH)

    if (
        manifest.get("schema") != "ag-bridge-bgk-native-backend-export-manifest-v1"
        or manifest.get("through_unit") != 6
        or int(manifest.get("record_count", 0)) <= 0
        or backend_qa.get("through_unit") != 6
        or backend_qa.get("model_provenance") != MODEL_PROVENANCE
    ):
        raise RuntimeError("Native backend is not the exact Units 01--06 contract")
    require_binding(
        {
            "path": backend_qa.get("manifest_path"),
            "bytes": backend_qa.get("manifest_bytes"),
            "sha256": backend_qa.get("manifest_sha256"),
        },
        BACKEND_MANIFEST_PATH,
        manifest_data,
    )

    files: dict[str, bytes] = {BACKEND_MANIFEST_PATH: manifest_data}
    declared = manifest.get("files") or []
    declared_paths = [item.get("path") for item in declared]
    if len(declared_paths) != len(set(declared_paths)) or len(declared_paths) < 2:
        raise RuntimeError("Backend manifest file inventory is empty or duplicated")
    for item in declared:
        rel = item.get("path")
        if not isinstance(rel, str) or not rel.startswith(BACKEND_ROOT + "/"):
            raise RuntimeError(f"Backend manifest escaped namespace: {rel!r}")
        data = read_bytes(rel)
        require_binding(item, rel, data)
        files[rel] = data

    records_rel = f"{BACKEND_ROOT}/records.jsonl"
    records_data = files.get(records_rel)
    if records_data is None:
        raise RuntimeError("Backend manifest does not bind records.jsonl")
    if (
        backend_qa.get("records_path") != records_rel
        or backend_qa.get("records_bytes") != len(records_data)
        or backend_qa.get("records_sha256") != sha256(records_data)
        or backend_qa.get("record_count") != manifest.get("record_count")
        or backend_qa.get("deterministic_double_replay") is not True
        or backend_qa.get("all_export_file_hashes_stable") is not True
        or backend_qa.get("unique_stable_ids") is not True
        or int(
            backend_qa.get(
                "bgk_classical_stable_id_intersection_count",
                (backend_qa.get("classical_collision_baseline") or {}).get("intersection_count", -1),
            )
        ) != 0
    ):
        raise RuntimeError("Native backend QA does not close the cumulative backend")

    native = common_qa.get("native_backend") or {}
    projection = common_qa.get("common_projection") or {}
    checks = common_qa.get("checks") or {}
    if (
        common_qa.get("schema") != "ag-bridge-common-backend-v1-preflight-qa-v1"
        or "01-06" not in str(common_qa.get("scope"))
        or common_qa.get("language") != "id-ID"
        or common_qa.get("model_provenance") != MODEL_PROVENANCE
        or native.get("path") != BACKEND_ROOT
        or native.get("manifest_sha256") != sha256(manifest_data)
        or native.get("native_qa_sha256") != sha256(backend_qa_data)
        or native.get("records_sha256") != sha256(records_data)
        or projection.get("lossless_reverse_sha256") != sha256(records_data)
        or projection.get("double_preflight_stdout_identical") is not True
        or not checks
        or any(value is not True for value in checks.values())
        or not str((common_qa.get("classical_regression") or {}).get("status", "")).startswith("PASS")
    ):
        raise RuntimeError("Common-backend preflight does not losslessly bind Units 01--06")

    files[BACKEND_QA_PATH] = backend_qa_data
    files[COMMON_QA_PATH] = common_qa_data
    for rel in BACKEND_TOOL_PATHS + COMMON_CONTRACT_PATHS:
        files[rel] = read_bytes(rel)
    return manifest, backend_qa, common_qa, files


def source_file_inventory(
    build_receipt: dict[str, Any], unit_qa_data: dict[str, bytes]
) -> dict[str, bytes]:
    inputs = {item.get("path"): item for item in build_receipt.get("inputs", [])}
    required = {
        "source/id-ID/bgk/frontmatter-bgk-units-01-06.md",
        "source/id-ID/reader.css",
        "source/id-ID/pdf-header.tex",
        "authority/wikiversity-bgk/course/COURSE_AUTHORITY_MANIFEST.json",
        "00_control/TERMINOLOGY.csv",
        "00_control/CORRECTIONS.csv",
        "scripts/build_bgk_reader.py",
    }
    for unit in UNITS:
        required.update(
            {
                f"source/id-ID/bgk/lecture-{unit:02d}.md",
                f"source/id-ID/bgk/worksheet-{unit:02d}.md",
                f"source/id-ID/bgk/worksheet-{unit:02d}-solutions.md",
                f"source/id-ID/media-credits-bgk-unit-{unit:02d}.md",
                f"authority/wikiversity-bgk/unit-{unit:02d}/UNIT_AUTHORITY_MANIFEST.json",
                f"authority/wikiversity-bgk/unit-{unit:02d}/ORDERED_EXERCISE_MAP.json",
                f"authority/wikiversity-bgk/unit-{unit:02d}/worksheet-solution-candidates-api.json",
                f"authority/BGK_UNIT_{unit:02d}_AUTHORITY_FREEZE.md",
                f"authority/ASSET_CLOSURE-bgk-unit-{unit:02d}.json",
                f"authority/RIGHTS-bgk-unit-{unit:02d}.csv",
                f"00_control/BGK_UNIT_{unit:02d}_WORKLOG.md",
                f"qa/BGK_UNIT_{unit:02d}_AUTHORITY_QA.json",
                f"qa/BGK_UNIT_{unit:02d}_TRANSLATION_QA.json",
                f"scripts/qa_bgk_unit_{unit:02d}_translation.py",
            }
        )

    files: dict[str, bytes] = {}
    for rel in sorted(required):
        data = unit_qa_data.get(rel, read_bytes(rel))
        binding = inputs.get(rel)
        if binding is not None:
            require_binding(binding, rel, data)
        elif rel.startswith("source/id-ID/bgk/") or rel in {
            "source/id-ID/reader.css",
            "source/id-ID/pdf-header.tex",
            "authority/wikiversity-bgk/course/COURSE_AUTHORITY_MANIFEST.json",
        }:
            raise RuntimeError(f"Build-critical source is not bound by the reader receipt: {rel}")
        files[rel] = data

    for unit in UNITS:
        closure_rel = f"authority/ASSET_CLOSURE-bgk-unit-{unit:02d}.json"
        closure = json.loads(files[closure_rel].decode("utf-8"))
        for asset in closure.get("assets", []):
            for key, bytes_key, hash_key in (
                ("local_path", "local_bytes", "local_sha256"),
                ("pdf_local_path", "pdf_local_bytes", "pdf_local_sha256"),
            ):
                rel = asset.get(key)
                if not rel:
                    continue
                if not isinstance(rel, str) or not rel.startswith("authority/assets/bgk-"):
                    raise RuntimeError(f"Unsafe BGK component-asset path: {rel!r}")
                data = read_bytes(rel)
                if asset.get(bytes_key) != len(data) or asset.get(hash_key) != sha256(data):
                    raise RuntimeError(f"Asset closure drifted: {rel}")
                files[rel] = data
    return files


def authority_pointers(source_files: dict[str, bytes]) -> bytes:
    course_rel = "authority/wikiversity-bgk/course/COURSE_AUTHORITY_MANIFEST.json"
    course = json.loads(source_files[course_rel].decode("utf-8"))
    units: list[dict[str, Any]] = []
    for unit in UNITS:
        rel = f"authority/wikiversity-bgk/unit-{unit:02d}/UNIT_AUTHORITY_MANIFEST.json"
        manifest = json.loads(source_files[rel].decode("utf-8"))
        row: dict[str, Any] = {
            "unit": unit,
            "manifest": fact(rel, source_files[rel]),
        }
        for kind in ("lecture", "worksheet"):
            item = manifest.get(kind) or {}
            row[kind] = {
                key: item.get(key)
                for key in (
                    "title",
                    "pageid",
                    "revid",
                    "timestamp",
                    "mediawiki_sha1",
                    "wikitext_bytes",
                    "oldid_url",
                )
            }
        row["official_pdf_witnesses"] = [
            {
                key: item.get(key)
                for key in (
                    "kind",
                    "source_file_title",
                    "source_url",
                    "description_url",
                    "source_bytes",
                    "mediawiki_sha1",
                    "local_bytes",
                    "local_sha256",
                )
            }
            for item in manifest.get("official_pdf_witnesses", [])
        ]
        units.append(row)
    return canonical_json(
        {
            "schema": "ag-bridge-bgk-release-authority-pointers-v1",
            "work": "Bündel, Garben und Kohomologie (Osnabrück 2019-2020)",
            "author": "Holger Brenner",
            "source_project": "German Wikiversity",
            "source_api": course.get("source_api"),
            "course_root": course.get("course_root"),
            "course_manifest": fact(course_rel, source_files[course_rel]),
            "complete_source_course_units": 30,
            "included_translation_units": list(UNITS),
            "rights_boundary": course.get("rights_boundary"),
            "units": units,
            "model_provenance": MODEL_PROVENANCE,
        }
    )


def inventory(entries: dict[str, bytes], schema: str) -> bytes:
    return canonical_json(
        {
            "schema": schema,
            "entry_count_excluding_inventory": len(entries),
            "uncompressed_bytes_excluding_inventory": sum(map(len, entries.values())),
            "entries": [
                {"path": name, "bytes": len(entries[name]), "sha256": sha256(entries[name])}
                for name in sorted(entries)
            ],
        }
    )


def deterministic_zip(entries: dict[str, bytes]) -> bytes:
    stream = io.BytesIO()
    with zipfile.ZipFile(
        stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9, strict_timestamps=True
    ) as archive:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.flag_bits |= 0x800
            archive.writestr(info, entries[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return stream.getvalue()


def zip_inventory(data: bytes) -> dict[str, Any]:
    with zipfile.ZipFile(io.BytesIO(data), "r") as archive:
        bad = archive.testzip()
        if bad is not None:
            raise RuntimeError(f"ZIP CRC failure: {bad}")
        rows = []
        for info in archive.infolist():
            payload = archive.read(info.filename)
            rows.append({"path": info.filename, "bytes": len(payload), "sha256": sha256(payload)})
        return {
            "entry_count": len(rows),
            "uncompressed_bytes": sum(row["bytes"] for row in rows),
            "entries": rows,
        }


def release_texts(pages: int, exercises: int, public_solutions: int, records: int) -> tuple[bytes, bytes]:
    missing = exercises - public_solutions
    if missing < 0:
        raise RuntimeError("Public-solution count exceeds exercise count")
    readme = f"""# {TITLE}

This is a **partial, coherent reader checkpoint** containing the first six of
the source course's 30 semantic units. It includes all six lectures and
worksheets, all {exercises} exercises, and exactly the {public_solutions}
public source solutions found within this boundary. It does not invent the
{missing} solutions absent from the frozen source.

The separate Indonesian edition of Brenner's *Algebraische Kurven* is already
complete as its own 30-unit classical volume and is not duplicated in this BGK
payload. The two courses comprise 60 source units; this package covers BGK
Units 1–6.

## Start here

1. `{PDF_NAME}` — primary reader-first A4 PDF ({pages} pages).
2. `{HTML_NAME}` — semantic, responsive id-ID HTML with MathML, landmarks,
   alternative text, and the source animation.
3. `{SOURCE_ZIP_NAME}` — compact resumable translated source, frozen authority
   identities/maps, component-rights tables, assets, ledgers, QA, and builder.
4. `{BACKEND_ZIP_NAME}` — complete {records:,}-record cumulative native
   backend, schema, class projections, exporter/QA code, and lossless
   common-backend preflight.

`{MANIFEST_NAME}` and `{CHECKSUMS_NAME}` bind the release bytes. The release
candidate QA records deterministic double replay and a zero-hit secret scan.
No credential, raw provenance dump, or official source PDF is included.

## Scope and quality

- Language: Bahasa Indonesia (`id-ID`).
- Status: partial, 6 of 30 BGK units; source order preserved.
- Source: Holger Brenner, *Bündel, Garben und Kohomologie (Osnabrück
  2019-2020)*, German Wikiversity.
- Reader QA: all {pages} PDF pages rendered and visually reviewed; responsive
  desktop/mobile HTML checked; internal links, stable IDs, media, and alt text
  closed deterministically.
- Backend QA: {records:,} unique native records; lossless common-backend
  preflight; no collision with the completed classical namespace.
- Provenance: {MODEL_PROVENANCE}

See `{LICENSE_NAME}` before reuse. This independent edition is not endorsed by
the source author or upstream institutions.
"""
    source_readme = f"""# Resumable source checkpoint

This archive contains the translated Markdown for BGK Units 1–6, the exact
reader builder/style inputs, cumulative terminology and correction ledgers,
the admitted component media, rights tables, unit worklogs and QA, and compact
frozen course/unit authority identities. `AUTHORITY_POINTERS.json` binds all
twelve semantic page/revision identities and official-PDF witness pointers
without duplicating raw API/HTML/XML dumps or the official PDFs.

Run `scripts/build_bgk_reader.py --through 6` from the restored repository
root. The included build and cumulative reader QA receipts bind the accepted
{pages}-page PDF and semantic HTML bytes.
"""
    return readme.encode("utf-8"), source_readme.encode("utf-8")


def backend_readme(records: int) -> bytes:
    return f"""# Native backend checkpoint

This archive contains the complete cumulative native backend for BGK Units
1–6: {records:,} canonical JSONL records, per-class projections, schema,
manifest, exporter, deterministic native QA, the frozen common-backend
contract, and the lossless common-backend-v1 preflight. The final migration
receipt is generated only after the existing Zenodo lineage reserves the exact
public identity; it is therefore a separate release asset.
""".encode("utf-8")


SECRET_PATTERNS = {
    "private_key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github_classic_token": re.compile(rb"gh[pousr]_[A-Za-z0-9]{20,}"),
    "github_fine_grained_token": re.compile(rb"github_pat_[A-Za-z0-9_]{20,}"),
    "bearer_token": re.compile(rb"(?i)authorization\s*:\s*bearer\s+[A-Za-z0-9._~-]{20,}"),
    "assigned_secret": re.compile(
        rb"(?i)(?:access[_-]?token|api[_-]?key|password)\s*[:=]\s*[\"']?[A-Za-z0-9._~-]{16,}"
    ),
}


def secret_hits(payload: dict[str, bytes]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []

    def scan(label: str, data: bytes) -> None:
        for pattern_name, pattern in SECRET_PATTERNS.items():
            if pattern.search(data):
                hits.append({"path": label, "pattern": pattern_name})

    text_suffixes = {".css", ".csv", ".html", ".json", ".jsonl", ".md", ".py", ".tex", ".txt"}
    for name, data in payload.items():
        if name.endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(data), "r") as archive:
                for info in archive.infolist():
                    if Path(info.filename).suffix.lower() in text_suffixes:
                        scan(f"{name}!/{info.filename}", archive.read(info.filename))
        elif Path(name).suffix.lower() in text_suffixes:
            scan(name, data)
    return hits


def build_once(visual_qa_rel: str) -> tuple[dict[str, bytes], dict[str, Any]]:
    reader_qa, build_receipt, reader_data = validate_reader(visual_qa_rel)
    authority_qas, translation_qas, unit_qa_data = validate_units()
    backend_manifest, backend_qa, common_qa, backend_files = validate_backend()
    source_files = source_file_inventory(build_receipt, unit_qa_data)
    source_files[READER_QA_PATH] = reader_data[READER_QA_PATH]
    source_files[visual_qa_rel] = reader_data[visual_qa_rel]
    source_files[BUILD_RECEIPT_PATH] = reader_data[BUILD_RECEIPT_PATH]
    reader_qa_script_rel = (reader_qa.get("qa_script") or {})["path"]
    source_files[reader_qa_script_rel] = reader_data[reader_qa_script_rel]

    exercises = sum(int((translation_qas[unit].get("counts") or {}).get("source_exercises", 0)) for unit in UNITS)
    public_solutions = sum(int((translation_qas[unit].get("counts") or {}).get("source_public_solutions", 0)) for unit in UNITS)
    reader_scope = reader_qa.get("exercise_solution_closure") or {}
    if (
        exercises <= 0
        or reader_scope.get("total_exercises") != exercises
        or reader_scope.get("public_solutions") != public_solutions
        or reader_scope.get("negative_solution_checks") != exercises - public_solutions
        or reader_scope.get("invented_solutions") != 0
        or backend_qa.get("exercise_count") != exercises
        or backend_qa.get("public_solution_count") != public_solutions
    ):
        raise RuntimeError("Reader/unit/backend exercise-and-solution closure disagrees")
    pages = int((reader_qa.get("pdf") or {}).get("pages_pypdf") or 0)
    records = int(backend_manifest["record_count"])
    readme, source_readme = release_texts(pages, exercises, public_solutions, records)
    license_bytes = LICENSE_TEXT.encode("utf-8")

    source_root = "bundel-berkas-dan-kohomologi-id-ID-units-01-06-source"
    source_entries = {f"{source_root}/{rel}": data for rel, data in source_files.items()}
    source_entries[f"{source_root}/AUTHORITY_POINTERS.json"] = authority_pointers(source_files)
    source_entries[f"{source_root}/README.md"] = source_readme
    source_entries[f"{source_root}/LICENSE_AND_COMPONENT_RIGHTS.md"] = license_bytes
    source_entries[f"{source_root}/SOURCE_INVENTORY.json"] = inventory(
        source_entries, "ag-bridge-bgk-source-archive-inventory-v1"
    )

    backend_root = "bundel-berkas-dan-kohomologi-id-ID-units-01-06-native-backend"
    backend_entries = {f"{backend_root}/{rel}": data for rel, data in backend_files.items()}
    backend_entries[f"{backend_root}/README.md"] = backend_readme(records)
    backend_entries[f"{backend_root}/LICENSE_AND_COMPONENT_RIGHTS.md"] = license_bytes
    backend_entries[f"{backend_root}/BACKEND_INVENTORY.json"] = inventory(
        backend_entries, "ag-bridge-bgk-native-backend-archive-inventory-v1"
    )

    payload = {
        PDF_NAME: reader_data[PDF_PATH],
        HTML_NAME: reader_data[HTML_PATH],
        SOURCE_ZIP_NAME: deterministic_zip(source_entries),
        BACKEND_ZIP_NAME: deterministic_zip(backend_entries),
        LICENSE_NAME: license_bytes,
        README_NAME: readme,
    }
    evidence = {
        "reader_qa": fact(READER_QA_PATH, reader_data[READER_QA_PATH]),
        "visual_qa": fact(visual_qa_rel, reader_data[visual_qa_rel]),
        "build_receipt": fact(BUILD_RECEIPT_PATH, reader_data[BUILD_RECEIPT_PATH]),
        "backend_manifest": fact(BACKEND_MANIFEST_PATH, read_bytes(BACKEND_MANIFEST_PATH)),
        "backend_qa": fact(BACKEND_QA_PATH, read_bytes(BACKEND_QA_PATH)),
        "common_qa": fact(COMMON_QA_PATH, read_bytes(COMMON_QA_PATH)),
        "unit_authority_qa": [
            fact(f"qa/BGK_UNIT_{unit:02d}_AUTHORITY_QA.json", unit_qa_data[f"qa/BGK_UNIT_{unit:02d}_AUTHORITY_QA.json"])
            for unit in UNITS
        ],
        "unit_translation_qa": [
            fact(f"qa/BGK_UNIT_{unit:02d}_TRANSLATION_QA.json", unit_qa_data[f"qa/BGK_UNIT_{unit:02d}_TRANSLATION_QA.json"])
            for unit in UNITS
        ],
        "source_fingerprint": sha256(canonical_json([fact(rel, data) for rel, data in sorted(source_files.items())])),
        "backend_fingerprint": sha256(canonical_json([fact(rel, data) for rel, data in sorted(backend_files.items())])),
        "source_zip": zip_inventory(payload[SOURCE_ZIP_NAME]),
        "backend_zip": zip_inventory(payload[BACKEND_ZIP_NAME]),
        "pages": pages,
        "exercises": exercises,
        "public_solutions": public_solutions,
        "records": records,
        "backend_status": backend_qa["status"],
        "common_status": common_qa["status"],
        "all_unit_authority_qas_pass": all(str(authority_qas[u]["status"]).startswith("PASS") for u in UNITS),
    }
    return payload, evidence


def package_manifest(payload: dict[str, bytes], evidence: dict[str, Any]) -> bytes:
    return canonical_json(
        {
            "schema": "ag-bridge-bgk-release-manifest-v1",
            "title": TITLE,
            "language": "id-ID",
            "status": "partial_coherent_checkpoint",
            "source_course_units": 30,
            "included_units": list(UNITS),
            "included_unit_count": 6,
            "remaining_unit_count": 24,
            "classical_course": {
                "work": "Algebraische Kurven",
                "status": "complete_separate_30_unit_volume",
                "included_in_this_payload": False,
            },
            "reader": {
                "primary_file": PDF_NAME,
                "pdf_pages": evidence["pages"],
                "html_file": HTML_NAME,
                "exercises": evidence["exercises"],
                "public_source_solutions": evidence["public_solutions"],
                "documented_absent_source_solutions": evidence["exercises"] - evidence["public_solutions"],
            },
            "backend": {
                "native_records": evidence["records"],
                "native_archive": BACKEND_ZIP_NAME,
                "common_backend_preflight": evidence["common_status"],
                "final_migration_receipt": "separate_asset_after_existing_lineage_reservation",
            },
            "license": "CC BY-SA 4.0 for course text/translation; per-component media rights preserved",
            "model_provenance": MODEL_PROVENANCE,
            "deterministic_inputs": {
                "source_fingerprint": evidence["source_fingerprint"],
                "backend_fingerprint": evidence["backend_fingerprint"],
            },
            "files": [
                {"path": name, "bytes": len(payload[name]), "sha256": sha256(payload[name])}
                for name in sorted(payload)
            ],
            "qa_bindings": [
                evidence["reader_qa"],
                evidence["visual_qa"],
                evidence["backend_qa"],
                evidence["common_qa"],
                *evidence["unit_authority_qa"],
                *evidence["unit_translation_qa"],
            ],
        }
    )


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--visual-qa",
        required=True,
        help=(
            "task-relative JSON receipt whose pdf object binds path/bytes/SHA-256, "
            "all pages rendered/reviewed, zero unintended blanks, and zero visual defects"
        ),
    )
    args = parser.parse_args()
    visual_qa_rel = Path(args.visual_qa).as_posix()
    first, first_evidence = build_once(visual_qa_rel)
    second, second_evidence = build_once(visual_qa_rel)
    if first.keys() != second.keys() or first_evidence != second_evidence:
        raise RuntimeError("Deterministic replay inventory/evidence differs")
    for name in first:
        if first[name] != second[name]:
            raise RuntimeError(f"Deterministic replay bytes differ: {name}")

    hits = secret_hits(first)
    if hits:
        raise RuntimeError(f"Credential-like material detected: {hits}")
    forbidden = (b"Translation and Transcription Project", b"TTP")
    forbidden_hits = [
        {"path": name, "label": label.decode("ascii")}
        for name, data in first.items()
        if name in {README_NAME, LICENSE_NAME}
        for label in forbidden
        if label in data
    ]
    if forbidden_hits:
        raise RuntimeError(f"Forbidden umbrella label in visible release prose: {forbidden_hits}")

    manifest = package_manifest(first, first_evidence)
    checksums = "".join(
        f"{sha256(data)}  {name}\n"
        for name, data in sorted({**first, MANIFEST_NAME: manifest}.items())
    ).encode("ascii")
    qa = canonical_json(
        {
            "schema": "ag-bridge-bgk-release-candidate-qa-v1",
            "status": "PASS",
            "title": TITLE,
            "language": "id-ID",
            "scope_truth": {
                "bgk_units_complete": 6,
                "bgk_units_total": 30,
                "bgk_units_remaining": 24,
                "classical_course_is_complete_and_separate": True,
                "classical_files_touched": False,
            },
            "reader_first": {
                "lexicographically_first_file": PDF_NAME,
                "pdf_pages": first_evidence["pages"],
                "reader_qa_status": "PASS",
            },
            "deterministic_double_replay": {
                "status": "PASS",
                "payload_file_count": len(first),
                "all_payload_bytes_identical": True,
                "source_input_fingerprint": first_evidence["source_fingerprint"],
                "backend_input_fingerprint": first_evidence["backend_fingerprint"],
                "source_zip_sha256_first": sha256(first[SOURCE_ZIP_NAME]),
                "source_zip_sha256_second": sha256(second[SOURCE_ZIP_NAME]),
                "backend_zip_sha256_first": sha256(first[BACKEND_ZIP_NAME]),
                "backend_zip_sha256_second": sha256(second[BACKEND_ZIP_NAME]),
            },
            "source_archive": {
                "file": SOURCE_ZIP_NAME,
                "bytes": len(first[SOURCE_ZIP_NAME]),
                "sha256": sha256(first[SOURCE_ZIP_NAME]),
                **first_evidence["source_zip"],
            },
            "backend_archive": {
                "file": BACKEND_ZIP_NAME,
                "bytes": len(first[BACKEND_ZIP_NAME]),
                "sha256": sha256(first[BACKEND_ZIP_NAME]),
                **first_evidence["backend_zip"],
            },
            "exact_gate_hashes": {
                "reader_qa": first_evidence["reader_qa"],
                "visual_qa": first_evidence["visual_qa"],
                "backend_qa": first_evidence["backend_qa"],
                "common_adapter_qa": first_evidence["common_qa"],
            },
            "checks": {
                "reader_receipt_outputs_and_all_page_visual_qa_bound": True,
                "all_six_unit_authority_and_translation_qas_pass": first_evidence["all_unit_authority_qas_pass"],
                "native_manifest_and_declared_backend_files_byte_bound": True,
                "common_backend_lossless_preflight_bound": True,
                "source_archive_crc_and_entry_hashes_valid": True,
                "backend_archive_crc_and_entry_hashes_valid": True,
                "license_and_component_rights_included": True,
                "exact_model_provenance_included": True,
                "credential_pattern_hits": len(hits),
                "forbidden_visible_umbrella_label_hits": len(forbidden_hits),
                "raw_authority_dumps_included": False,
                "official_pdf_witnesses_included": False,
                "public_state_mutated": False,
            },
            "manifest": {"path": MANIFEST_NAME, "bytes": len(manifest), "sha256": sha256(manifest)},
            "checksums": {"path": CHECKSUMS_NAME, "bytes": len(checksums), "sha256": sha256(checksums)},
            "model_provenance": MODEL_PROVENANCE,
        }
    )

    final = {**first, MANIFEST_NAME: manifest, CHECKSUMS_NAME: checksums, QA_NAME: qa}
    expected_names = {
        PDF_NAME, HTML_NAME, SOURCE_ZIP_NAME, BACKEND_ZIP_NAME, LICENSE_NAME,
        README_NAME, MANIFEST_NAME, CHECKSUMS_NAME, QA_NAME,
    }
    if set(final) != expected_names or sorted(final)[0] != PDF_NAME:
        raise RuntimeError("Release inventory or reader-first ordering drifted")

    OUT.mkdir(parents=True, exist_ok=True)
    existing = {path.name for path in OUT.iterdir() if path.is_file()}
    unexpected = existing - expected_names
    if unexpected:
        raise RuntimeError(f"Unexpected pre-existing candidate files: {sorted(unexpected)}")
    for name, data in sorted(final.items()):
        atomic_write(OUT / name, data)
    for name, data in final.items():
        if (OUT / name).read_bytes() != data:
            raise RuntimeError(f"Post-write byte verification failed: {name}")
    if set(path.name for path in OUT.iterdir() if path.is_file()) != expected_names:
        raise RuntimeError("Post-write candidate inventory differs")

    print(
        json.dumps(
            {
                "status": "PASS",
                "directory": OUT.as_posix(),
                "file_count": len(final),
                "total_bytes": sum(map(len, final.values())),
                "files": [
                    {"path": name, "bytes": len(final[name]), "sha256": sha256(final[name])}
                    for name in sorted(final)
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
