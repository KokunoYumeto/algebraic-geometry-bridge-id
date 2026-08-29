#!/usr/bin/env python3
"""Build and verify the reader-first BGK Units 01--03 release candidate.

The operation is deliberately offline and confined to
``release/bgk-units-01-03``.  It packages, but never edits, the accepted
reader, translated source, authority pointers, ledgers, and native backend.
Two independent in-memory builds must be byte-identical before anything is
written.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import zipfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "release" / "bgk-units-01-03"
FIXED_ZIP_TIME = (2026, 8, 29, 0, 0, 0)
MODEL_PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."
TITLE = "Bundel, Berkas, dan Kohomologi — Unit 1–3, Bahasa Indonesia"

PDF_NAME = "01_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-03.pdf"
HTML_NAME = "02_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-03.html"
SOURCE_ZIP_NAME = "03_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-03_source.zip"
BACKEND_ZIP_NAME = "04_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-03_native-backend.zip"
LICENSE_NAME = "05_LICENSE_AND_COMPONENT_RIGHTS.md"
README_NAME = "06_README.md"
MANIFEST_NAME = "07_RELEASE_MANIFEST.json"
CHECKSUMS_NAME = "08_SHA256SUMS.txt"
QA_NAME = "09_RELEASE_CANDIDATE_QA.json"

PDF_PATH = "build/reader-bgk-id/bundel-berkas-dan-kohomologi-id-units-01-03.pdf"
HTML_PATH = "build/reader-bgk-id/index.html"
BUILD_RECEIPT_PATH = "build/reader-bgk-id/BUILD_RECEIPT.json"
BACKEND_MANIFEST_PATH = "backend/bgk-units-01-03/MANIFEST.json"

# Boundary-defining inputs are byte-pinned.  The reader build receipt and
# native-backend manifest bind every subordinate source/backend file.
PINS = {
    PDF_PATH: "01655c8ddb8056e03b06f09319f6f73b07daf55e709b2fffb6b83b7cf2a96800",
    HTML_PATH: "2cb348ee10366628742e12847a46d51ba9d58adeaa65187b067ce929ab2ca623",
    BUILD_RECEIPT_PATH: "6231b460e6de7db904f8056f4746e4c74def88fbeaf7764a4a45d8d774797f99",
    BACKEND_MANIFEST_PATH: "2ccea7a804737c7f7e5a65bb8398e836a36cd31f3aec1a4cf6a4d1117bed0c02",
    "qa/BGK_UNIT_01_AUTHORITY_QA.json": "2c42a091e5d9e12f8078839e8c520a0c258676548a392986e5452f521b2cb5a0",
    "qa/BGK_UNIT_01_TRANSLATION_QA.json": "c1b815046172ebe42c07d3e1780c1ea4ccc9b510bb5da5430f90c1445fc9612a",
    "qa/BGK_UNIT_02_AUTHORITY_QA.json": "56b4dec14089b86721ca8dfc7ec95c1593619d30433529f912e1f498aae0ef92",
    "qa/BGK_UNIT_02_TRANSLATION_QA.json": "285b29c9b4d9ebd938b1106f5b84e2fd6ad3509edbad79f66ebe10d29b42ffee",
    "qa/BGK_UNIT_03_AUTHORITY_QA.json": "fa6e5b308880eb09b8edce0c8ced383029748308dbe04698fefe051f9335b2bb",
    "qa/BGK_UNIT_03_TRANSLATION_QA.json": "8bde479b506421bddcdab21c9c0e3fb1c2027fc27d029dce87258cb29e30e6f0",
    "qa/BGK_UNITS_01_03_READER_QA.json": "b4c2962975f5cdeefd8ac3835b7f0eb34d510a24e223cdf3539ba316404aceea",
    "qa/BGK_UNITS_01_03_BACKEND_QA.json": "7308f881141cfaabb0f3f82e5f97a45ad2c2216386ad95252c71cfa50d38562d",
    "qa/BGK_UNITS_01_03_COMMON_ADAPTER_PREFLIGHT_QA.json": "873c2e35d90b6d397bf85b36403ff003badb081b34b2ea92b948fb73b92d671d",
    "scripts/build_bgk_reader.py": "10a96cc77ddb925a0e16fe7c368a60e83b38f46bf333a5588f5777c78d5a20c6",
    "scripts/export_backend_bgk_units_01_03.py": "66a2c50ef75fb4800257a6a3b6a49a11ef28a1cebfe365358cfcd5d450295b71",
    "scripts/qa_backend_bgk_units_01_03.py": "2f5f65811624298925afc4d3934a40c2df9ecaaf6b1dd90604476a1cfa08ee8e",
    "scripts/generate_common_backend_v1_receipts.py": "c058be10693c824339666cdf480e247851a2a0f3ca1f633824d40318be769568",
    "00_control/TERMINOLOGY.csv": "043a0370707a1f50b8af8ca3700d388a7e78bae53879919f40b7f5689e57ad19",
    "00_control/CORRECTIONS.csv": "8ddb2e4f54b80f3b825cbd630c73e3c90c3b617bb0caa21e7b4977e030975755",
    "00_control/BGK_UNIT_03_WORKLOG.md": "4a01f0e10d53fd94f3ccc3837e89d5571d37bcee5eb117869deb4eb293818f37",
}

SOURCE_FILE_PATHS = [
    "source/id-ID/bgk/frontmatter-bgk-units-01-03.md",
    "source/id-ID/bgk/lecture-01.md",
    "source/id-ID/bgk/worksheet-01.md",
    "source/id-ID/bgk/worksheet-01-solutions.md",
    "source/id-ID/bgk/lecture-02.md",
    "source/id-ID/bgk/worksheet-02.md",
    "source/id-ID/bgk/worksheet-02-solutions.md",
    "source/id-ID/bgk/lecture-03.md",
    "source/id-ID/bgk/worksheet-03.md",
    "source/id-ID/bgk/worksheet-03-solutions.md",
    "source/id-ID/media-credits-bgk-unit-01.md",
    "source/id-ID/media-credits-bgk-unit-02.md",
    "source/id-ID/media-credits-bgk-unit-03.md",
    "source/id-ID/reader.css",
    "source/id-ID/pdf-header.tex",
    "authority/wikiversity-bgk/course/COURSE_AUTHORITY_MANIFEST.json",
    "authority/wikiversity-bgk/unit-01/UNIT_AUTHORITY_MANIFEST.json",
    "authority/wikiversity-bgk/unit-02/UNIT_AUTHORITY_MANIFEST.json",
    "authority/wikiversity-bgk/unit-03/UNIT_AUTHORITY_MANIFEST.json",
    "authority/ASSET_CLOSURE-bgk-unit-01.json",
    "authority/ASSET_CLOSURE-bgk-unit-02.json",
    "authority/ASSET_CLOSURE-bgk-unit-03.json",
    "authority/RIGHTS-bgk-unit-01.csv",
    "authority/RIGHTS-bgk-unit-02.csv",
    "authority/RIGHTS-bgk-unit-03.csv",
    "authority/assets/bgk-tangent-bundle-500.png",
    "authority/assets/bgk-hairy-ball-one-pole-500.jpg",
    "authority/assets/bgk-inclusion-exclusion-500.png",
    "authority/assets/bgk-fiddler-crab-mobius-strip.gif",
    "authority/assets/bgk-fiddler-crab-mobius-strip-frame-001.png",
    "00_control/TERMINOLOGY.csv",
    "00_control/CORRECTIONS.csv",
    "00_control/BGK_UNIT_03_WORKLOG.md",
    "qa/BGK_UNIT_01_AUTHORITY_QA.json",
    "qa/BGK_UNIT_01_TRANSLATION_QA.json",
    "qa/BGK_UNIT_02_AUTHORITY_QA.json",
    "qa/BGK_UNIT_02_TRANSLATION_QA.json",
    "qa/BGK_UNIT_03_AUTHORITY_QA.json",
    "qa/BGK_UNIT_03_TRANSLATION_QA.json",
    "qa/BGK_UNITS_01_03_READER_QA.json",
    BUILD_RECEIPT_PATH,
    "scripts/build_bgk_reader.py",
]

BACKEND_EXTRA_PATHS = [
    "qa/BGK_UNITS_01_03_BACKEND_QA.json",
    "qa/BGK_UNITS_01_03_COMMON_ADAPTER_PREFLIGHT_QA.json",
    "scripts/export_backend_bgk_units_01_03.py",
    "scripts/qa_backend_bgk_units_01_03.py",
    "scripts/generate_common_backend_v1_receipts.py",
]

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

The source package points to frozen official PDF witnesses but does not include
those PDFs. Current Wikimedia Commons metadata records CC BY-SA 4.0, while the
visible notice in the complete official course PDF states CC BY-SA 3.0. Both
records are preserved in the authority manifests; this package makes no blanket
relicensing claim for those witnesses.

## Third-party media

No blanket package licence overrides component rights. Exact records are in
`authority/RIGHTS-bgk-unit-01.csv` through
`authority/RIGHTS-bgk-unit-03.csv` and in each reader's **Kredit media**
section:

- Tangent-bundle diagram by Oleg Alexandrov: public domain.
- Hairy-ball illustration by RokerHRO: CC BY-SA 3.0.
- Inclusion-exclusion diagram: public domain under the frozen Commons record.
- Fiddler-crab Möbius-strip animation by Hamishtodd1: CC BY-SA 4.0; the PDF
  uses its deterministically extracted first frame.

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

README_TEXT = f"""# {TITLE}

This is a **partial, coherent reader checkpoint** containing the first three
of the source course's 30 semantic units. It includes all three lectures and
worksheets, all 62 exercises, and exactly the two public source solutions found
within this boundary. It does not invent the 60 solutions absent from the
frozen source.

The separate Indonesian edition of Brenner's *Algebraische Kurven* is already
complete as its own 30-unit classical volume. That separate completed reader
is not duplicated in this BGK checkpoint. The two courses therefore comprise
60 source units in total; this package covers BGK Units 1–3 only.

## Start here

1. `{PDF_NAME}` — primary reader-first A4 PDF (50 pages).
2. `{HTML_NAME}` — semantic, responsive id-ID HTML with MathML, landmarks,
   alt text, and the original animation.
3. `{SOURCE_ZIP_NAME}` — compact translated source, frozen authority
   manifests/pointers, component-rights tables, assets, ledgers, QA, and the
   deterministic reader builder.
4. `{BACKEND_ZIP_NAME}` — complete 2,370-record cumulative native backend,
   schema, class projections, exporter/QA code, and common-backend preflight.

`{MANIFEST_NAME}` and `{CHECKSUMS_NAME}` bind the release bytes. The release
candidate QA receipt records deterministic double replay and a zero-hit secret
scan. No credential or raw provenance dump is included.

## Scope and quality

- Language: Bahasa Indonesia (`id-ID`).
- Status: partial, 3 of 30 BGK units; source order preserved.
- Source: Holger Brenner, *Bündel, Garben und Kohomologie (Osnabrück
  2019-2020)*, German Wikiversity.
- Reader QA: 50/50 PDF pages rendered and reviewed; responsive desktop/mobile
  HTML checked; no broken internal links, duplicate IDs, or missing alt text.
- Backend QA: 2,370 unique native records, 62 exercises, two public solutions,
  lossless common-backend preflight, and no collision with the separate
  completed classical namespace.
- Provenance: {MODEL_PROVENANCE}

See `{LICENSE_NAME}` before reuse. This independent edition is not endorsed by
the source author or upstream institutions.
"""

SOURCE_README = """# Resumable source checkpoint

This archive contains the translated Markdown for BGK Units 1–3, the exact
reader builder and style inputs, the cumulative terminology/corrections
ledgers, five admitted media files, component-rights tables, and compact frozen
course/unit authority manifests. `AUTHORITY_POINTERS.json` gives the six exact
semantic page/revision identities and official-PDF witness pointers without
duplicating the raw official PDFs or bulk API/HTML/XML dumps.

Run `scripts/build_bgk_reader.py` from the repository root after restoring the
paths in this archive. The included build and reader QA receipts bind the
accepted 50-page PDF and semantic HTML bytes.
"""

BACKEND_README = """# Native backend checkpoint

This archive contains the complete cumulative native backend for BGK Units
1–3: 2,370 canonical JSONL records, per-class projections, schema, manifest,
exporter, deterministic QA, and the common-backend-v1 preflight receipt and
adapter. The common projection itself is virtual and losslessly round-trips to
the native `records.jsonl`; a final migration receipt is intentionally deferred
until a public release identity exists.
"""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read_bytes(rel: str) -> bytes:
    path = ROOT / Path(rel)
    if not path.is_file():
        raise RuntimeError(f"Required input missing: {rel}")
    return path.read_bytes()


def read_pinned(rel: str) -> bytes:
    data = read_bytes(rel)
    expected = PINS.get(rel)
    if expected is not None and sha256(data) != expected:
        raise RuntimeError(f"Pinned input drifted: {rel}")
    return data


def json_from_bytes(data: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(data.decode("utf-8"))
    except Exception as exc:  # pragma: no cover - fail-closed diagnostic
        raise RuntimeError(f"Invalid JSON: {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"Expected JSON object: {label}")
    return value


def validate_reader_boundary() -> tuple[dict[str, Any], dict[str, Any]]:
    receipt_data = read_pinned(BUILD_RECEIPT_PATH)
    receipt = json_from_bytes(receipt_data, BUILD_RECEIPT_PATH)
    if receipt.get("through_unit") != 3 or receipt.get("language") != "id-ID":
        raise RuntimeError("Reader receipt scope drifted")
    outputs = {item["path"]: item for item in receipt.get("outputs", [])}
    for rel in (PDF_PATH, HTML_PATH):
        data = read_pinned(rel)
        item = outputs.get(rel)
        if not item or item.get("bytes") != len(data) or item.get("sha256") != sha256(data):
            raise RuntimeError(f"Reader receipt does not bind {rel}")
    inputs = {item["path"]: item for item in receipt.get("inputs", [])}
    return receipt, inputs


def validate_source_files(reader_inputs: dict[str, Any]) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    for rel in SOURCE_FILE_PATHS:
        data = read_pinned(rel)
        binding = reader_inputs.get(rel)
        if binding is not None:
            if binding.get("bytes") != len(data) or binding.get("sha256") != sha256(data):
                raise RuntimeError(f"Reader input binding drifted: {rel}")
        elif rel not in PINS:
            raise RuntimeError(f"Unbound source-package input: {rel}")
        result[rel] = data
    return result


def validate_backend_files() -> tuple[dict[str, Any], dict[str, bytes]]:
    manifest_data = read_pinned(BACKEND_MANIFEST_PATH)
    manifest = json_from_bytes(manifest_data, BACKEND_MANIFEST_PATH)
    if manifest.get("through_unit") != 3 or manifest.get("record_count") != 2370:
        raise RuntimeError("Native backend manifest scope drifted")
    result = {BACKEND_MANIFEST_PATH: manifest_data}
    for item in manifest.get("files", []):
        rel = item["path"]
        if not rel.startswith("backend/bgk-units-01-03/"):
            raise RuntimeError(f"Backend manifest escaped namespace: {rel}")
        data = read_bytes(rel)
        if item.get("bytes") != len(data) or item.get("sha256") != sha256(data):
            raise RuntimeError(f"Backend manifest file drifted: {rel}")
        result[rel] = data
    if len(result) != 19:
        raise RuntimeError(f"Expected manifest plus 18 backend files, found {len(result)}")
    for rel in BACKEND_EXTRA_PATHS:
        result[rel] = read_pinned(rel)
    return manifest, result


def authority_pointers(source_files: dict[str, bytes]) -> bytes:
    course_rel = "authority/wikiversity-bgk/course/COURSE_AUTHORITY_MANIFEST.json"
    course = json_from_bytes(source_files[course_rel], course_rel)
    rows: list[dict[str, Any]] = []
    for unit in range(1, 4):
        rel = f"authority/wikiversity-bgk/unit-{unit:02d}/UNIT_AUTHORITY_MANIFEST.json"
        manifest = json_from_bytes(source_files[rel], rel)
        entry: dict[str, Any] = {
            "unit": unit,
            "manifest": {
                "path": rel,
                "bytes": len(source_files[rel]),
                "sha256": sha256(source_files[rel]),
            },
        }
        for kind in ("lecture", "worksheet"):
            item = manifest[kind]
            entry[kind] = {
                key: item[key]
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
        entry["official_pdf_witnesses"] = [
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
        rows.append(entry)
    value = {
        "schema": "ag-bridge-bgk-release-authority-pointers-v1",
        "work": "Bündel, Garben und Kohomologie (Osnabrück 2019-2020)",
        "author": "Holger Brenner",
        "source_project": "German Wikiversity",
        "source_api": course.get("source_api"),
        "course_root": course.get("course_root"),
        "course_manifest": {
            "path": course_rel,
            "bytes": len(source_files[course_rel]),
            "sha256": sha256(source_files[course_rel]),
        },
        "complete_source_course_units": 30,
        "included_translation_units": [1, 2, 3],
        "rights_boundary": course.get("rights_boundary"),
        "units": rows,
        "model_provenance": MODEL_PROVENANCE,
    }
    return canonical_json(value)


def inventory(entries: dict[str, bytes], schema: str) -> bytes:
    value = {
        "schema": schema,
        "entry_count_excluding_inventory": len(entries),
        "uncompressed_bytes_excluding_inventory": sum(len(data) for data in entries.values()),
        "entries": [
            {"path": name, "bytes": len(entries[name]), "sha256": sha256(entries[name])}
            for name in sorted(entries)
        ],
    }
    return canonical_json(value)


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
            rows.append(
                {
                    "path": info.filename,
                    "bytes": len(payload),
                    "sha256": sha256(payload),
                    "timestamp": list(info.date_time),
                }
            )
        return {
            "entry_count": len(rows),
            "uncompressed_bytes": sum(row["bytes"] for row in rows),
            "entries": rows,
        }


def build_once() -> tuple[dict[str, bytes], dict[str, Any]]:
    _, reader_inputs = validate_reader_boundary()
    source_files = validate_source_files(reader_inputs)
    backend_manifest, backend_files = validate_backend_files()

    license_bytes = LICENSE_TEXT.encode("utf-8")
    source_root = "bundel-berkas-dan-kohomologi-id-ID-units-01-03-source"
    source_entries = {f"{source_root}/{rel}": data for rel, data in source_files.items()}
    source_entries[f"{source_root}/AUTHORITY_POINTERS.json"] = authority_pointers(source_files)
    source_entries[f"{source_root}/README.md"] = SOURCE_README.encode("utf-8")
    source_entries[f"{source_root}/LICENSE_AND_COMPONENT_RIGHTS.md"] = license_bytes
    source_entries[f"{source_root}/SOURCE_INVENTORY.json"] = inventory(
        source_entries, "ag-bridge-bgk-source-archive-inventory-v1"
    )

    backend_root = "bundel-berkas-dan-kohomologi-id-ID-units-01-03-native-backend"
    backend_entries = {f"{backend_root}/{rel}": data for rel, data in backend_files.items()}
    backend_entries[f"{backend_root}/README.md"] = BACKEND_README.encode("utf-8")
    backend_entries[f"{backend_root}/LICENSE_AND_COMPONENT_RIGHTS.md"] = license_bytes
    backend_entries[f"{backend_root}/BACKEND_INVENTORY.json"] = inventory(
        backend_entries, "ag-bridge-bgk-native-backend-archive-inventory-v1"
    )

    payload = {
        PDF_NAME: read_pinned(PDF_PATH),
        HTML_NAME: read_pinned(HTML_PATH),
        SOURCE_ZIP_NAME: deterministic_zip(source_entries),
        BACKEND_ZIP_NAME: deterministic_zip(backend_entries),
        LICENSE_NAME: license_bytes,
        README_NAME: README_TEXT.encode("utf-8"),
    }
    evidence = {
        "source_input_fingerprint": sha256(
            canonical_json(
                [
                    {"path": path, "bytes": len(data), "sha256": sha256(data)}
                    for path, data in sorted(source_files.items())
                ]
            )
        ),
        "backend_input_fingerprint": sha256(
            canonical_json(
                [
                    {"path": path, "bytes": len(data), "sha256": sha256(data)}
                    for path, data in sorted(backend_files.items())
                ]
            )
        ),
        "backend_manifest_sha256": sha256(canonical_json(backend_manifest)),
        "source_zip": zip_inventory(payload[SOURCE_ZIP_NAME]),
        "backend_zip": zip_inventory(payload[BACKEND_ZIP_NAME]),
    }
    return payload, evidence


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

    for name, data in payload.items():
        if name.endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(data), "r") as archive:
                for info in archive.infolist():
                    if Path(info.filename).suffix.lower() in {
                        ".css", ".csv", ".html", ".json", ".jsonl", ".md", ".py", ".tex", ".txt"
                    }:
                        scan(f"{name}!/{info.filename}", archive.read(info.filename))
        elif Path(name).suffix.lower() in {".html", ".json", ".md", ".txt"}:
            scan(name, data)
    return hits


def package_manifest(payload: dict[str, bytes], evidence: dict[str, Any]) -> bytes:
    value = {
        "schema": "ag-bridge-bgk-release-manifest-v1",
        "title": TITLE,
        "language": "id-ID",
        "status": "partial_coherent_checkpoint",
        "source_course_units": 30,
        "included_units": [1, 2, 3],
        "included_unit_count": 3,
        "remaining_unit_count": 27,
        "classical_course": {
            "work": "Algebraische Kurven",
            "status": "complete_separate_30_unit_volume",
            "included_in_this_payload": False,
        },
        "reader": {
            "primary_file": PDF_NAME,
            "pdf_pages": 50,
            "html_file": HTML_NAME,
            "exercises": 62,
            "public_source_solutions": 2,
            "documented_absent_source_solutions": 60,
        },
        "backend": {
            "native_records": 2370,
            "native_archive": BACKEND_ZIP_NAME,
            "common_backend_preflight": "PASS",
            "final_migration_receipt": "deferred_until_public_identity_exists",
        },
        "license": "CC BY-SA 4.0 for course text/translation; per-component media rights preserved",
        "model_provenance": MODEL_PROVENANCE,
        "deterministic_inputs": {
            "source_fingerprint": evidence["source_input_fingerprint"],
            "backend_fingerprint": evidence["backend_input_fingerprint"],
        },
        "files": [
            {"path": name, "bytes": len(payload[name]), "sha256": sha256(payload[name])}
            for name in sorted(payload)
        ],
        "qa_bindings": [
            {"path": path, "bytes": len(read_pinned(path)), "sha256": sha256(read_pinned(path))}
            for path in (
                "qa/BGK_UNITS_01_03_READER_QA.json",
                "qa/BGK_UNITS_01_03_BACKEND_QA.json",
                "qa/BGK_UNITS_01_03_COMMON_ADAPTER_PREFLIGHT_QA.json",
            )
        ],
    }
    return canonical_json(value)


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def main() -> None:
    first, first_evidence = build_once()
    second, second_evidence = build_once()
    if first.keys() != second.keys():
        raise RuntimeError("Deterministic replay file set differs")
    for name in first:
        if first[name] != second[name]:
            raise RuntimeError(f"Deterministic replay bytes differ: {name}")
    if first_evidence != second_evidence:
        raise RuntimeError("Deterministic replay evidence differs")

    hits = secret_hits(first)
    if hits:
        raise RuntimeError(f"Credential-like material detected: {hits}")
    forbidden = (b"Translation and Transcription Project", b"TTP")
    # The reader embeds binary media as data URLs, so arbitrary byte trigrams
    # inside that encoding are not prose.  Enforce the metadata convention on
    # the generated visible title/lead documents themselves.
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

    qa_value = {
        "schema": "ag-bridge-bgk-release-candidate-qa-v1",
        "status": "PASS",
        "title": TITLE,
        "language": "id-ID",
        "scope_truth": {
            "bgk_units_complete": 3,
            "bgk_units_total": 30,
            "bgk_units_remaining": 27,
            "classical_course_is_complete_and_separate": True,
            "classical_files_touched": False,
        },
        "reader_first": {
            "lexicographically_first_file": PDF_NAME,
            "pdf_pages": 50,
            "reader_qa_status": "PASS",
        },
        "deterministic_double_replay": {
            "status": "PASS",
            "payload_file_count": len(first),
            "all_payload_bytes_identical": True,
            "source_input_fingerprint": first_evidence["source_input_fingerprint"],
            "backend_input_fingerprint": first_evidence["backend_input_fingerprint"],
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
        "checks": {
            "reader_receipt_and_outputs_byte_bound": True,
            "native_manifest_and_all_18_backend_files_byte_bound": True,
            "source_archive_crc_and_entry_hashes_valid": True,
            "backend_archive_crc_and_entry_hashes_valid": True,
            "common_backend_preflight_included": True,
            "license_and_component_rights_included": True,
            "exact_model_provenance_included": True,
            "credential_pattern_hits": len(hits),
            "forbidden_visible_umbrella_label_hits": len(forbidden_hits),
            "raw_authority_dumps_included": False,
            "official_pdf_witnesses_included": False,
            "public_state_mutated": False,
        },
        "manifest": {"path": MANIFEST_NAME, "bytes": len(manifest), "sha256": sha256(manifest)},
        "checksums": {
            "path": CHECKSUMS_NAME,
            "bytes": len(checksums),
            "sha256": sha256(checksums),
        },
        "model_provenance": MODEL_PROVENANCE,
    }
    qa = canonical_json(qa_value)

    final = {
        **first,
        MANIFEST_NAME: manifest,
        CHECKSUMS_NAME: checksums,
        QA_NAME: qa,
    }
    expected_names = {
        PDF_NAME,
        HTML_NAME,
        SOURCE_ZIP_NAME,
        BACKEND_ZIP_NAME,
        LICENSE_NAME,
        README_NAME,
        MANIFEST_NAME,
        CHECKSUMS_NAME,
        QA_NAME,
    }
    if set(final) != expected_names or sorted(final)[0] != PDF_NAME:
        raise RuntimeError("Release candidate inventory or reader-first ordering drifted")

    OUT.mkdir(parents=True, exist_ok=True)
    existing = {path.name for path in OUT.iterdir() if path.is_file()}
    unexpected = existing - expected_names
    if unexpected:
        raise RuntimeError(f"Unexpected pre-existing candidate files: {sorted(unexpected)}")
    for name, data in sorted(final.items()):
        atomic_write(OUT / name, data)

    for name, data in final.items():
        written = (OUT / name).read_bytes()
        if written != data:
            raise RuntimeError(f"Post-write byte verification failed: {name}")
    if set(path.name for path in OUT.iterdir() if path.is_file()) != expected_names:
        raise RuntimeError("Post-write candidate inventory differs")

    result = {
        "status": "PASS",
        "directory": OUT.as_posix(),
        "file_count": len(final),
        "total_bytes": sum(len(data) for data in final.values()),
        "files": [
            {"path": name, "bytes": len(final[name]), "sha256": sha256(final[name])}
            for name in sorted(final)
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
