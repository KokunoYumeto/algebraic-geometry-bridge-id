#!/usr/bin/env python3
"""Freeze Unit 9 image metadata and component-rights evidence.

The lecture/worksheet parse surfaces also reference the two official PDF
witnesses.  Those PDFs are build witnesses, not reader media positions; this
script records the one substantive image position separately and preserves
its Commons identity and rights metadata.
"""

from __future__ import annotations

import csv
import hashlib
import html
import json
import re
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "authority" / "commons-imageinfo-unit-09.json"
ASSETS = ROOT / "authority" / "assets"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-09.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-09.json"
CREDITS = ROOT / "source" / "id-ID" / "media-credits-unit-09.md"


def digest(path: Path, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def plain(value: object) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(html.unescape(text).split())


def ext(metadata: dict, key: str) -> str:
    return plain(metadata.get(key, {}).get("value", ""))


def main() -> int:
    data = json.loads(META.read_text(encoding="utf-8"))
    pages = data.get("query", {}).get("pages", [])
    if len(pages) != 1 or not pages[0].get("imageinfo"):
        raise RuntimeError("Unit 9 Commons metadata must resolve exactly one image")
    page = pages[0]
    info = page["imageinfo"][0]
    asset = ASSETS / "David_Hilbert_1886.jpg"
    if not asset.is_file() or asset.is_symlink():
        raise RuntimeError(f"missing/non-regular asset: {asset}")
    if asset.stat().st_size != int(info["size"]):
        raise RuntimeError("local byte size does not match frozen Commons metadata")
    if digest(asset, "sha1") != info["sha1"]:
        raise RuntimeError("local SHA-1 does not match frozen Commons metadata")
    with Image.open(asset) as image:
        image.verify()
    with Image.open(asset) as image:
        width, height = int(image.width), int(image.height)
    if (width, height) != (int(info["width"]), int(info["height"])):
        raise RuntimeError("local dimensions do not match frozen Commons metadata")

    metadata = info.get("extmetadata", {})
    license_short = ext(metadata, "LicenseShortName")
    usage_terms = ext(metadata, "UsageTerms")
    if "Public domain" not in license_short and "Public domain" not in usage_terms:
        raise RuntimeError(f"unexpected Unit 9 image licence: {license_short!r} / {usage_terms!r}")

    row = {
        "asset_id": "br-ak-u09-media-001",
        "reader_order": 1,
        "resource_title": "File:David Hilbert 1886.jpg",
        "metadata_title": page["title"],
        "repository": "commons",
        "description_url": info["descriptionurl"],
        "original_url": info["url"].split("?", 1)[0],
        "selected_url": info["url"],
        "selected_form": "original",
        "local_path": "authority/assets/David_Hilbert_1886.jpg",
        "local_bytes": asset.stat().st_size,
        "local_sha256": digest(asset),
        "local_width": width,
        "local_height": height,
        "frame_count": 1,
        "pdf_local_path": "",
        "pdf_local_bytes": "",
        "pdf_local_sha256": "",
        "pdf_companion_source": "",
        "original_bytes": int(info["size"]),
        "original_sha1": info["sha1"],
        "original_width": int(info["width"]),
        "original_height": int(info["height"]),
        "mime": info["mime"],
        "media_type": info.get("mediatype", "BITMAP"),
        "source_timestamp": info.get("timestamp", ""),
        "uploader": info.get("user", ""),
        "artist": ext(metadata, "Artist"),
        "credit": ext(metadata, "Credit"),
        "license_short": license_short,
        "usage_terms": usage_terms,
        "license_url": ext(metadata, "LicenseUrl"),
        "attribution_required": ext(metadata, "AttributionRequired") or "false",
        "source_course_creator": "Holger Brenner / Wikiversity course page",
        "source_course_license": "CC BY-SA 4.0",
        "description_pageid": page.get("pageid", ""),
        "description_revid": "",
        "description_timestamp": "",
        "description_mediawiki_sha1": "",
        "description_wikitext_bytes": "",
        "description_wikitext_sha256": "",
        "html_animation_preserved": False,
    }

    RIGHTS.parent.mkdir(parents=True, exist_ok=True)
    with RIGHTS.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(row), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)

    CREDITS.parent.mkdir(parents=True, exist_ok=True)
    license_text = row["license_short"] or row["usage_terms"] or "lihat halaman sumber"
    if row["license_url"]:
        license_text = f"[{license_text}]({row['license_url']})"
    CREDITS.write_text(
        "\n".join(
            [
                "# Kredit media Unit 9 {#agc-media-credits-unit-09}",
                "",
                "Satu posisi media substantif pada Kuliah 9 mempertahankan identitas Commons dan status hak sumbernya. Dua PDF yang dirujuk halaman adalah saksi build resmi dan dicatat dalam manifest authority, bukan media pembaca terpisah.",
                "",
                f"1. **David Hilbert (1886)** - [{row['metadata_title']}]({row['description_url']}); pencipta/atribusi: {row['artist'] or row['uploader']}; status hak/lisensi: {license_text}.",
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )

    closure = {
        "schema": "brenner-unit-media-closure-v2",
        "unit": 9,
        "reader_media_positions": 1,
        "animated_html_positions": 0,
        "unique_local_assets": 1,
        "metadata_file": META.relative_to(ROOT).as_posix(),
        "metadata_bytes": META.stat().st_size,
        "metadata_sha256": digest(META),
        "rights_file": RIGHTS.relative_to(ROOT).as_posix(),
        "rights_bytes": RIGHTS.stat().st_size,
        "rights_sha256": digest(RIGHTS),
        "reader_credits_file": CREDITS.relative_to(ROOT).as_posix(),
        "reader_credits_bytes": CREDITS.stat().st_size,
        "reader_credits_sha256": digest(CREDITS),
        "official_pdf_witnesses_are_not_media_positions": True,
        "assets": [
            {
                "asset_id": row["asset_id"],
                "repository": row["repository"],
                "local_path": row["local_path"],
                "local_bytes": row["local_bytes"],
                "local_sha256": row["local_sha256"],
                "html_animation_preserved": False,
            }
        ],
    }
    CLOSURE.write_text(json.dumps(closure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"result": "PASS", "media_positions": 1, "rights_sha256": closure["rights_sha256"], "closure_sha256": digest(CLOSURE)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
