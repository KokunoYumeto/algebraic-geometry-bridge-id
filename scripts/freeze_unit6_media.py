#!/usr/bin/env python3
"""Freeze Unit 6 Commons media and emit component-level rights records."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "authority" / "assets"
META = ROOT / "authority" / "commons-imageinfo-unit-06.json"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-06.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-06.json"
CREDITS = ROOT / "source" / "id-ID" / "media-credits-unit-06.md"
API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "Codex algebraic-geometry-bridge-id media freeze (at user's direction)"

MEDIA = (
    {
        "resource_title": "File:Krivka parametricky.png",
        "metadata_title": "File:Krivka parametricky.png",
        "caption": "Kurva berparameter dapat dibayangkan sebagai suatu lintasan gerak",
        "credit_creator": "Beny di Wikipedia bahasa Ceko",
        "credit_status": "domain publik",
        "local_name": "Krivka_parametricky.png",
        "pdf_name": "",
    },
    {
        "resource_title": "File:Cubic with double point.svg",
        "metadata_title": "File:Cubic with double point.svg",
        "caption": "Kurva kubik dengan titik ganda",
        "credit_creator": "Gunther di Wikipedia bahasa Jerman",
        "credit_status": "domain publik",
        "local_name": "Cubic_with_double_point.svg",
        "pdf_name": "Cubic_with_double_point-500.png",
    },
    {
        "resource_title": "File:Dioklova kisoida.png",
        "metadata_title": "File:Dioklova kisoida.png",
        "caption": "Sissoid Diokles (hitam pada gambar) dapat diparameterkan secara rasional",
        "credit_creator": "Pajs di Wikipedia bahasa Ceko",
        "credit_status": "domain publik",
        "local_name": "Dioklova_kisoida.png",
        "pdf_name": "",
    },
)


def fetch(url: str, data: bytes | None = None) -> bytes:
    for attempt in range(1, 7):
        try:
            request = Request(url, data=data, headers={"User-Agent": USER_AGENT})
            with urlopen(request, timeout=90) as response:
                result = response.read()
            time.sleep(1.0)
            return result
        except HTTPError as error:
            if error.code != 429 or attempt == 6:
                raise
            retry_after = error.headers.get("Retry-After", "")
            delay = int(retry_after) if retry_after.isdigit() else 3 * attempt
            time.sleep(min(delay, 25))
    raise RuntimeError("unreachable retry state")


def digest(path: Path, algorithm: str = "sha256") -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def plain(value: object) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(html.unescape(text).split())


def ext(metadata: dict, key: str) -> str:
    return plain(metadata.get(key, {}).get("value", ""))


def dimensions(path: Path, fallback_width: int, fallback_height: int) -> tuple[int, int]:
    if path.suffix.casefold() == ".svg":
        return fallback_width, fallback_height
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        return int(image.width), int(image.height)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-metadata", action="store_true")
    args = parser.parse_args()
    ASSETS.mkdir(parents=True, exist_ok=True)
    params = {
        "action": "query",
        "prop": "imageinfo",
        "titles": "|".join(item["metadata_title"] for item in MEDIA),
        "iiprop": "url|sha1|size|mime|mediatype|timestamp|user|extmetadata",
        "iiurlwidth": 500,
        "format": "json",
        "formatversion": "2",
    }
    if META.is_file() and not args.refresh_metadata:
        raw = META.read_bytes()
    else:
        raw = fetch(API, urlencode(params).encode("utf-8"))
        META.write_bytes(raw)
    data = json.loads(raw)
    pages = {page["title"]: page for page in data["query"]["pages"]}

    rows: list[dict[str, object]] = []
    for order, item in enumerate(MEDIA, start=1):
        page = pages[item["metadata_title"]]
        info = page["imageinfo"][0]
        local = ASSETS / item["local_name"]
        if not local.is_file():
            local.write_bytes(fetch(info["url"]))
        width, height = dimensions(local, int(info["width"]), int(info["height"]))
        if local.stat().st_size != int(info["size"]) or digest(local, "sha1") != info["sha1"]:
            raise RuntimeError(f"Original validation failed: {local.name}")
        if width != int(info["width"]) or height != int(info["height"]):
            raise RuntimeError(f"Dimension validation failed: {local.name}")

        pdf_local = ASSETS / item["pdf_name"] if item["pdf_name"] else None
        pdf_url = info.get("thumburl", "") if pdf_local else ""
        if pdf_local:
            if not pdf_url:
                raise RuntimeError(f"No Commons PNG companion URL for {local.name}")
            if not pdf_local.is_file():
                pdf_local.write_bytes(fetch(pdf_url))
            dimensions(pdf_local, 0, 0)

        metadata = info.get("extmetadata", {})
        rows.append(
            {
                "asset_id": f"br-ak-u06-media-{order:03d}",
                "reader_order": order,
                "reader_caption_id": item["caption"],
                "resource_title": item["resource_title"],
                "commons_metadata_title": item["metadata_title"],
                "description_url": info["descriptionurl"],
                "original_url": info["url"].split("?", 1)[0],
                "selected_url": info["url"],
                "selected_form": "original",
                "local_path": f"authority/assets/{local.name}",
                "local_bytes": local.stat().st_size,
                "local_sha256": digest(local),
                "local_width": width,
                "local_height": height,
                "pdf_local_path": f"authority/assets/{pdf_local.name}" if pdf_local else "",
                "pdf_local_bytes": pdf_local.stat().st_size if pdf_local else "",
                "pdf_local_sha256": digest(pdf_local) if pdf_local else "",
                "pdf_companion_source_url": pdf_url,
                "original_bytes": int(info["size"]),
                "original_sha1": info["sha1"],
                "original_width": int(info["width"]),
                "original_height": int(info["height"]),
                "mime": info["mime"],
                "commons_timestamp": info["timestamp"],
                "uploader": info["user"],
                "artist": ext(metadata, "Artist"),
                "license_short": ext(metadata, "LicenseShortName"),
                "usage_terms": ext(metadata, "UsageTerms"),
                "license_url": ext(metadata, "LicenseUrl"),
                "attribution_required": ext(metadata, "AttributionRequired"),
            }
        )

    with RIGHTS.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    credit_lines = [
        "# Kredit media Unit 6 {#agc-media-credits-unit-06}",
        "",
        "Kredit mengikuti urutan gambar dalam Kuliah 6 dan Lembar Kerja 6. Setiap komponen mempertahankan status hak sumbernya sendiri.",
        "",
    ]
    for row, item in zip(rows, MEDIA, strict=True):
        creator = item["credit_creator"]
        licence = item["credit_status"]
        credit_lines.append(
            f"{row['reader_order']}. **{row['reader_caption_id']}** - "
            f"[{row['resource_title']}]({row['description_url']}); pencipta/atribusi: {creator}; status hak/lisensi: {licence}."
        )
    CREDITS.write_bytes(("\n".join(credit_lines) + "\n").encode("utf-8"))

    closure = {
        "schema": "brenner-unit-media-closure-v1",
        "unit": 6,
        "reader_media_positions": len(rows),
        "unique_local_assets": len(rows) + sum(1 for row in rows if row["pdf_local_path"]),
        "metadata_file": META.relative_to(ROOT).as_posix(),
        "metadata_bytes": META.stat().st_size,
        "metadata_sha256": digest(META),
        "rights_file": RIGHTS.relative_to(ROOT).as_posix(),
        "rights_bytes": RIGHTS.stat().st_size,
        "rights_sha256": digest(RIGHTS),
        "reader_credits_file": CREDITS.relative_to(ROOT).as_posix(),
        "reader_credits_bytes": CREDITS.stat().st_size,
        "reader_credits_sha256": digest(CREDITS),
        "assets": [
            {
                "asset_id": row["asset_id"],
                "local_path": row["local_path"],
                "local_bytes": row["local_bytes"],
                "local_sha256": row["local_sha256"],
                "pdf_local_path": row["pdf_local_path"],
                "pdf_local_bytes": row["pdf_local_bytes"],
                "pdf_local_sha256": row["pdf_local_sha256"],
            }
            for row in rows
        ],
    }
    CLOSURE.write_bytes((json.dumps(closure, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(
        json.dumps(
            {
                "result": "PASS",
                "assets": len(rows),
                "binary_surfaces": closure["unique_local_assets"],
                "rights_sha256": closure["rights_sha256"],
                "closure_sha256": digest(CLOSURE),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
