#!/usr/bin/env python3
"""Freeze official-PDF component rights for a Brenner unit with no reader images."""

from __future__ import annotations

import argparse
import csv
import json
import urllib.parse

from freeze_single_image_unit_media import (
    API,
    ROOT,
    commons_file_title,
    digest,
    fetch,
    pdf_rights,
    title_key,
)


EMPTY_RIGHTS_FIELDS = [
    "asset_id",
    "reader_order",
    "reader_caption_id",
    "reader_alt_id",
    "resource_title",
    "metadata_title",
    "repository",
    "description_url",
    "original_url",
    "selected_url",
    "selected_form",
    "local_path",
    "local_bytes",
    "local_sha256",
    "local_width",
    "local_height",
    "frame_count",
    "original_bytes",
    "original_sha1",
    "original_width",
    "original_height",
    "mime",
    "media_type",
    "source_timestamp",
    "uploader",
    "artist",
    "credit",
    "license_short",
    "usage_terms",
    "license_url",
    "attribution_required",
    "source_course_creator",
    "source_course_license",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--unit", required=True, type=int)
    args = parser.parse_args()
    unit = args.unit
    unit_label = f"{unit:02d}"
    unit_dir = ROOT / "authority" / "wikiversity" / f"unit-{unit_label}"
    manifest_path = unit_dir / "UNIT_AUTHORITY_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("unit_number") != unit:
        raise RuntimeError(f"Authority manifest is not Unit {unit}")
    image_names = set(manifest.get("images", {}).get("lecture", [])) | set(
        manifest.get("images", {}).get("worksheet", [])
    )
    substantive = sorted(name for name in image_names if not name.casefold().endswith(".pdf"))
    if substantive:
        raise RuntimeError(f"Unit {unit} has substantive reader media: {substantive}")

    pdf_titles = [
        commons_file_title(row["source_file_title"])
        for row in manifest["official_pdf_witnesses"]
    ]
    params = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "prop": "imageinfo|revisions",
        "iiprop": "url|size|mime|sha1|timestamp|user|mediatype|extmetadata",
        "rvprop": "ids|timestamp|sha1|content",
        "rvslots": "main",
        "titles": "|".join(pdf_titles),
    }
    raw = fetch(API + "?" + urllib.parse.urlencode(params), accept="application/json")
    metadata_path = ROOT / "authority" / f"commons-imageinfo-unit-{unit_label}.json"
    metadata_path.write_bytes(raw)
    payload = json.loads(raw.decode("utf-8"))
    if payload.get("error"):
        raise RuntimeError(f"Commons API error: {payload['error']}")
    pages = payload.get("query", {}).get("pages", [])
    if len(pages) != len(pdf_titles) or any(page.get("missing") for page in pages):
        raise RuntimeError("Commons did not resolve both official PDFs")
    by_key = {title_key(page["title"]): page for page in pages}
    if set(by_key) != {title_key(title) for title in pdf_titles}:
        raise RuntimeError("Commons PDF title closure drift")
    pdf_records = [
        pdf_rights(by_key[title_key(title)], ROOT / witness["local_path"])
        for title, witness in zip(pdf_titles, manifest["official_pdf_witnesses"], strict=True)
    ]

    rights = ROOT / "authority" / f"RIGHTS-unit-{unit_label}.csv"
    with rights.open("w", encoding="utf-8", newline="") as stream:
        csv.DictWriter(stream, fieldnames=EMPTY_RIGHTS_FIELDS, lineterminator="\n").writeheader()
    closure = {
        "schema": "brenner-unit-media-closure-v2",
        "unit": unit,
        "authority_only_boundary": True,
        "reader_media_positions": 0,
        "animated_html_positions": 0,
        "unique_local_assets": 0,
        "metadata_file": metadata_path.relative_to(ROOT).as_posix(),
        "metadata_bytes": metadata_path.stat().st_size,
        "metadata_sha256": digest(metadata_path),
        "rights_file": rights.relative_to(ROOT).as_posix(),
        "rights_bytes": rights.stat().st_size,
        "rights_sha256": digest(rights),
        "reader_credits_file": None,
        "reader_credits_required": False,
        "official_pdf_witnesses_are_not_media_positions": True,
        "official_pdf_component_rights": sorted(pdf_records, key=lambda item: item["local_path"]),
        "assets": [],
    }
    closure_path = ROOT / "authority" / f"ASSET_CLOSURE-unit-{unit_label}.json"
    closure_path.write_text(
        json.dumps(closure, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "unit": unit,
                "media_positions": 0,
                "pdf_witnesses": len(pdf_records),
                "rights_sha256": digest(rights),
                "closure_sha256": digest(closure_path),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
