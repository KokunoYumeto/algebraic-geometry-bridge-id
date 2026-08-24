#!/usr/bin/env python3
"""Freeze the explicit zero-reader-media rights closure for Brenner Unit 10.

The Unit 10 lecture and worksheet parse surfaces contain only the two official
PDF build witnesses. They are authority artifacts, not reader-media positions.
This helper fails closed if another image appears or if either PDF no longer
matches the official Commons imageinfo witness.
"""

from __future__ import annotations

import csv
import hashlib
import html
import json
import re
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "authority" / "wikiversity" / "unit-10"
LECTURE_PARSE = UNIT / "lecture-10-parse-api.json"
WORKSHEET_PARSE = UNIT / "worksheet-10-parse-api.json"
PDF_METADATA = UNIT / "official-pdfs-api.json"
COMMONS_METADATA = ROOT / "authority" / "commons-pdf-imageinfo-unit-10.json"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-10.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-10.json"
COURSE_LICENSE_API = ROOT / "authority" / "wikiversity" / "course-license-api.json"
COURSE_LICENSE_HTML = ROOT / "authority" / "wikiversity" / "course-license.html"

EXPECTED_IMAGE_NAMES = {
    "Algebraische_Kurven_(Osnabrück_2025-2026)Vorlesung10.pdf",
    "Algebraische_Kurven_(Osnabrück_2025-2026)Arbeitsblatt10.pdf",
}
EXPECTED_PDFS = {
    "Algebraische Kurven (Osnabrück 2025-2026)Vorlesung10.pdf":
        ROOT / "authority" / "artifacts" / "lecture-10-official.pdf",
    "Algebraische Kurven (Osnabrück 2025-2026)Arbeitsblatt10.pdf":
        ROOT / "authority" / "artifacts" / "worksheet-10-official.pdf",
}

RIGHTS_FIELDS = [
    "asset_id", "reader_order", "resource_title", "metadata_title",
    "repository", "description_url", "original_url", "selected_url",
    "selected_form", "local_path", "local_bytes", "local_sha256",
    "local_width", "local_height", "frame_count", "pdf_local_path",
    "pdf_local_bytes", "pdf_local_sha256", "pdf_companion_source",
    "original_bytes", "original_sha1", "original_width", "original_height",
    "mime", "media_type", "source_timestamp", "uploader", "artist",
    "credit", "license_short", "usage_terms", "license_url",
    "attribution_required", "source_course_creator", "source_course_license",
    "description_pageid", "description_revid", "description_timestamp",
    "description_mediawiki_sha1", "description_wikitext_bytes",
    "description_wikitext_sha256", "html_animation_preserved",
]


def digest(path: Path, algorithm: str = "sha256") -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def read_json(path: Path) -> dict:
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"Missing/non-regular frozen witness: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def plain(value: object) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(html.unescape(text).split())


def parse_images(path: Path) -> set[str]:
    data = read_json(path)
    images = data.get("parse", {}).get("images")
    if not isinstance(images, list) or not all(isinstance(item, str) for item in images):
        raise RuntimeError(f"Malformed parse image surface: {path}")
    return set(images)


def main() -> int:
    expected_titles = EXPECTED_IMAGE_NAMES
    lecture_images = parse_images(LECTURE_PARSE)
    worksheet_images = parse_images(WORKSHEET_PARSE)
    if lecture_images != expected_titles or worksheet_images != expected_titles:
        raise RuntimeError(
            "Unit 10 image surfaces are not exactly the two official PDF witnesses: "
            f"lecture={sorted(lecture_images)!r}, worksheet={sorted(worksheet_images)!r}"
        )

    pdf_data = read_json(PDF_METADATA)
    pages = pdf_data.get("query", {}).get("pages", [])
    if len(pages) != 2:
        raise RuntimeError("Official Unit 10 PDF metadata must resolve exactly two pages")
    pdf_facts: list[dict] = []
    seen: set[str] = set()
    for page in pages:
        title = page.get("title", "").removeprefix("Datei:").removeprefix("File:")
        if title not in EXPECTED_PDFS or title in seen:
            raise RuntimeError(f"Unexpected/duplicate official PDF metadata title: {title!r}")
        seen.add(title)
        rows = page.get("imageinfo", [])
        if len(rows) != 1:
            raise RuntimeError(f"Official PDF metadata is not unique: {title!r}")
        info = rows[0]
        local = EXPECTED_PDFS[title]
        if not local.is_file() or local.is_symlink():
            raise RuntimeError(f"Missing/non-regular official PDF: {local}")
        raw_prefix = local.read_bytes()[:5]
        if raw_prefix != b"%PDF-":
            raise RuntimeError(f"Invalid PDF signature: {local}")
        if local.stat().st_size != int(info["size"]):
            raise RuntimeError(f"Official PDF byte-size mismatch: {title!r}")
        if digest(local, "sha1") != info["sha1"]:
            raise RuntimeError(f"Official PDF SHA-1 mismatch: {title!r}")
        pdf_facts.append(
            {
                "source_file_title": title,
                "local_path": local.relative_to(ROOT).as_posix(),
                "bytes": local.stat().st_size,
                "sha1": info["sha1"],
                "sha256": digest(local),
                "mime": info.get("mime"),
                "source_timestamp": info.get("timestamp"),
                "source_url": info.get("url"),
                "description_url": info.get("descriptionurl"),
            }
        )
    if seen != set(EXPECTED_PDFS):
        raise RuntimeError("Official Unit 10 PDF metadata closure is incomplete")

    commons_data = read_json(COMMONS_METADATA)
    commons_pages = commons_data.get("query", {}).get("pages", [])
    if len(commons_pages) != 2:
        raise RuntimeError("Commons component-rights metadata must resolve exactly two file pages")
    component_rights: list[dict] = []
    rights_by_title: dict[str, dict] = {}
    for page in commons_pages:
        title = page.get("title", "").removeprefix("File:").removeprefix("Datei:")
        if title not in EXPECTED_PDFS or title in rights_by_title:
            raise RuntimeError(f"Unexpected/duplicate Commons rights page: {title!r}")
        revisions = page.get("revisions", [])
        info_rows = page.get("imageinfo", [])
        if len(revisions) != 1 or len(info_rows) != 1:
            raise RuntimeError(f"Non-unique Commons rights witness: {title!r}")
        revision = revisions[0]
        content = revision.get("slots", {}).get("main", {}).get("content")
        if not isinstance(content, str):
            raise RuntimeError(f"Missing Commons description wikitext: {title!r}")
        info = info_rows[0]
        metadata = info.get("extmetadata", {})
        license_short = plain(metadata.get("LicenseShortName", {}).get("value"))
        license_url = plain(metadata.get("LicenseUrl", {}).get("value"))
        usage_terms = plain(metadata.get("UsageTerms", {}).get("value"))
        attribution_required = plain(metadata.get("AttributionRequired", {}).get("value"))
        artist = plain(metadata.get("Artist", {}).get("value"))
        if license_short != "CC BY-SA 4.0" or license_url != "https://creativecommons.org/licenses/by-sa/4.0":
            raise RuntimeError(f"Unexpected Commons PDF component licence: {title!r}")
        if attribution_required.lower() != "true" or "Bocardodarapti" not in artist:
            raise RuntimeError(f"Unexpected Commons PDF attribution metadata: {title!r}")
        local = EXPECTED_PDFS[title]
        if int(info["size"]) != local.stat().st_size or info["sha1"] != digest(local, "sha1"):
            raise RuntimeError(f"Commons component-rights bytes differ from the local PDF: {title!r}")
        last_page_text = PdfReader(local).pages[-1].extract_text() or ""
        if "CC-by-sa 3.0" not in last_page_text:
            raise RuntimeError(f"Expected stale printed 3.0 footer was not found: {title!r}")
        row = {
            "source_file_title": title,
            "description_pageid": page.get("pageid"),
            "description_revid": revision.get("revid"),
            "description_timestamp": revision.get("timestamp"),
            "description_mediawiki_sha1": revision.get("sha1"),
            "description_wikitext_bytes": len(content.encode("utf-8")),
            "description_wikitext_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            "file_timestamp": info.get("timestamp"),
            "file_bytes": int(info["size"]),
            "file_sha1": info["sha1"],
            "artist": artist,
            "license_short": license_short,
            "usage_terms": usage_terms,
            "license_url": license_url,
            "attribution_required": True,
            "printed_pdf_footer_license_text": "CC-by-sa 3.0",
            "printed_pdf_footer_is_stale_against_course_and_file_page": True,
        }
        rights_by_title[title] = row
        component_rights.append(row)
    if set(rights_by_title) != set(EXPECTED_PDFS):
        raise RuntimeError("Commons Unit 10 PDF rights closure is incomplete")

    course_license_html = COURSE_LICENSE_HTML.read_text(encoding="utf-8")
    if "CC-by-sa 4.0" not in course_license_html:
        raise RuntimeError("Frozen course licence witness does not state CC BY-SA 4.0")

    RIGHTS.parent.mkdir(parents=True, exist_ok=True)
    with RIGHTS.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=RIGHTS_FIELDS, lineterminator="\n")
        writer.writeheader()

    closure = {
        "schema": "brenner-unit-media-closure-v2",
        "unit": 10,
        "reader_media_positions": 0,
        "animated_html_positions": 0,
        "unique_local_assets": 0,
        "rights_rows": 0,
        "course_prose_license": "CC BY-SA 4.0",
        "course_license_witnesses": [
            {
                "file": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": digest(path),
            }
            for path in (COURSE_LICENSE_API, COURSE_LICENSE_HTML)
        ],
        "rights_file": RIGHTS.relative_to(ROOT).as_posix(),
        "rights_bytes": RIGHTS.stat().st_size,
        "rights_sha256": digest(RIGHTS),
        "parse_witnesses": [
            {
                "file": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": digest(path),
            }
            for path in (LECTURE_PARSE, WORKSHEET_PARSE)
        ],
        "official_pdf_metadata_file": PDF_METADATA.relative_to(ROOT).as_posix(),
        "official_pdf_metadata_bytes": PDF_METADATA.stat().st_size,
        "official_pdf_metadata_sha256": digest(PDF_METADATA),
        "commons_component_rights_metadata_file": COMMONS_METADATA.relative_to(ROOT).as_posix(),
        "commons_component_rights_metadata_bytes": COMMONS_METADATA.stat().st_size,
        "commons_component_rights_metadata_sha256": digest(COMMONS_METADATA),
        "official_pdf_witnesses_are_not_media_positions": True,
        "official_pdf_witnesses": sorted(pdf_facts, key=lambda row: row["local_path"]),
        "official_pdf_component_rights": sorted(component_rights, key=lambda row: row["source_file_title"]),
        "license_discrepancy": {
            "status": "RECORDED",
            "printed_pdf_footer": "CC-by-sa 3.0",
            "course_license_page": "CC-by-sa 4.0",
            "commons_file_description_and_structured_metadata": "CC BY-SA 4.0",
            "downstream_component_license": "CC BY-SA 4.0",
            "resolution": "Preserve the stale printed footer as source evidence; use the current course and Commons file-page grant for downstream rights metadata.",
        },
        "assets": [],
    }
    CLOSURE.write_text(
        json.dumps(closure, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "result": "PASS",
                "unit": 10,
                "reader_media_positions": 0,
                "official_pdf_witnesses": 2,
                "rights_sha256": closure["rights_sha256"],
                "closure_sha256": digest(CLOSURE),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
