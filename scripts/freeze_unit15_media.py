#!/usr/bin/env python3
"""Freeze Unit 15 Commons media and component-rights evidence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
UNIT = 15
API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "Codex-authority-freezer/1.0 (independent edition preservation)"
MANIFEST = ROOT / "authority" / "wikiversity" / "unit-15" / "UNIT_AUTHORITY_MANIFEST.json"
META = ROOT / "authority" / "commons-imageinfo-unit-15.json"
SVG = ROOT / "authority" / "assets" / "Concentric_Circles.svg"
PNG = ROOT / "authority" / "assets" / "Concentric_Circles-500.png"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-15.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-15.json"
CREDITS = ROOT / "source" / "id-ID" / "media-credits-unit-15.md"
RESOURCE_TITLE = "File:Concentric_Circles.svg"
CAPTION = "Representasi skematis suatu filter lingkungan"
ALT = "Empat lingkaran abu-abu konsentris pada latar transparan"


def digest(path: Path, algorithm: str = "sha256") -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def bytes_digest(value: bytes, algorithm: str = "sha256") -> str:
    return hashlib.new(algorithm, value).hexdigest()


def fetch(url: str, *, accept: str = "*/*", attempts: int = 8) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                result = response.read()
            time.sleep(0.5)
            return result
        except urllib.error.HTTPError as error:
            if error.code not in {429, 500, 502, 503, 504} or attempt + 1 == attempts:
                raise
            retry_after = error.headers.get("Retry-After", "")
            delay = int(retry_after) if retry_after.isdigit() else min(2**attempt, 30)
            time.sleep(max(delay, 1))
        except (TimeoutError, urllib.error.URLError):
            if attempt + 1 == attempts:
                raise
            time.sleep(min(2**attempt, 30))
    raise RuntimeError(f"unreachable fetch failure: {url}")


def plain(value: object) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(html.unescape(text).split())


def ext(info: dict[str, Any], key: str) -> str:
    return plain(info.get("extmetadata", {}).get(key, {}).get("value", ""))


def title_key(value: str) -> str:
    return value.replace("_", " ").casefold()


def commons_file_title(value: str) -> str:
    for prefix in ("Datei:", "File:"):
        if value.startswith(prefix):
            return "File:" + value[len(prefix) :]
    return "File:" + value


def revision(page: dict[str, Any]) -> tuple[dict[str, Any], str]:
    revisions = page.get("revisions", [])
    if len(revisions) != 1:
        raise RuntimeError(f"No unique description revision for {page.get('title')!r}")
    item = revisions[0]
    content = item.get("slots", {}).get("main", {}).get("content")
    if not isinstance(content, str):
        raise RuntimeError(f"No description wikitext for {page.get('title')!r}")
    return item, content


def file_fact(path: Path) -> dict[str, Any]:
    return {
        "file": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }


def component_rights(page: dict[str, Any], info: dict[str, Any]) -> dict[str, Any]:
    rev, content = revision(page)
    return {
        "title": page["title"],
        "pageid": page["pageid"],
        "revid": rev["revid"],
        "timestamp": rev["timestamp"],
        "mediawiki_sha1": rev["sha1"],
        "description_wikitext_bytes": len(content.encode("utf-8")),
        "description_wikitext_sha256": bytes_digest(content.encode("utf-8")),
        "description_url": info.get("descriptionurl"),
        "artist": ext(info, "Artist"),
        "credit": ext(info, "Credit"),
        "license_short": ext(info, "LicenseShortName"),
        "usage_terms": ext(info, "UsageTerms"),
        "license_url": ext(info, "LicenseUrl"),
        "attribution_required": ext(info, "AttributionRequired"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-metadata", action="store_true")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("unit_number") != UNIT:
        raise RuntimeError("Authority manifest is not Unit 15")
    names = set(manifest["images"]["lecture"]) | set(manifest["images"]["worksheet"])
    substantive = sorted(name for name in names if not name.casefold().endswith(".pdf"))
    if substantive != [RESOURCE_TITLE.removeprefix("File:")]:
        raise RuntimeError(f"Unexpected Unit 15 substantive media closure: {substantive}")

    pdf_titles = [commons_file_title(row["source_file_title"]) for row in manifest["official_pdf_witnesses"]]
    requested = [RESOURCE_TITLE, *pdf_titles]
    params = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "prop": "imageinfo|revisions",
        "iiprop": "url|size|mime|sha1|timestamp|user|mediatype|extmetadata",
        "iiurlwidth": 500,
        "rvprop": "ids|timestamp|sha1|content",
        "rvslots": "main",
        "titles": "|".join(requested),
    }
    url = API + "?" + urllib.parse.urlencode(params)
    if META.is_file() and not args.refresh_metadata:
        raw = META.read_bytes()
    else:
        raw = fetch(url, accept="application/json")
        META.write_bytes(raw)
    payload = json.loads(raw.decode("utf-8"))
    if payload.get("error"):
        raise RuntimeError(f"Commons API error: {payload['error']}")
    pages = payload.get("query", {}).get("pages", [])
    if len(pages) != 3 or any(page.get("missing") for page in pages):
        raise RuntimeError(f"Commons closure did not resolve all three files: {pages}")
    by_key = {title_key(page["title"]): page for page in pages}
    if set(by_key) != {title_key(value) for value in requested}:
        raise RuntimeError(f"Commons title closure drift: {sorted(page['title'] for page in pages)}")

    media_page = by_key[title_key(RESOURCE_TITLE)]
    infos = media_page.get("imageinfo", [])
    if len(infos) != 1:
        raise RuntimeError("No unique Commons imageinfo for Unit 15 media")
    info = infos[0]
    thumb_url = info.get("thumburl")
    if not thumb_url:
        raise RuntimeError("Commons supplied no 500px thumbnail")
    SVG.parent.mkdir(parents=True, exist_ok=True)
    if not SVG.is_file():
        SVG.write_bytes(fetch(info["url"].split("?", 1)[0], accept="image/svg+xml"))
    if not PNG.is_file():
        PNG.write_bytes(fetch(thumb_url, accept="image/png"))
    if SVG.is_symlink() or PNG.is_symlink():
        raise RuntimeError("Unit 15 media assets must be regular files")
    svg_head = SVG.read_bytes()[:1024].lower()
    if b"<svg" not in svg_head:
        raise RuntimeError("Local original is not recognizable SVG")
    with Image.open(PNG) as image:
        image.verify()
    with Image.open(PNG) as image:
        thumb_width, thumb_height = int(image.width), int(image.height)
    reported_thumb = (int(info["thumbwidth"]), int(info["thumbheight"]))
    if thumb_width != reported_thumb[0] or abs(thumb_height - reported_thumb[1]) > 1:
        raise RuntimeError("Local thumbnail dimensions disagree materially with Commons")
    if SVG.stat().st_size != int(info["size"]) or digest(SVG, "sha1") != info["sha1"]:
        raise RuntimeError("Local SVG bytes disagree with Commons original")

    rev, content = revision(media_page)
    licence = ext(info, "LicenseShortName") or ext(info, "UsageTerms")
    if not licence:
        raise RuntimeError("Commons supplied no media licence witness")
    row = {
        "asset_id": "br-ak-u15-media-001",
        "reader_order": 1,
        "reader_caption_id": CAPTION,
        "reader_alt_id": ALT,
        "resource_title": RESOURCE_TITLE,
        "metadata_title": media_page["title"],
        "repository": "commons",
        "description_url": info["descriptionurl"],
        "original_url": info["url"].split("?", 1)[0],
        "selected_url": info["url"].split("?", 1)[0],
        "selected_form": "original Commons SVG",
        "local_path": SVG.relative_to(ROOT).as_posix(),
        "local_bytes": SVG.stat().st_size,
        "local_sha256": digest(SVG),
        "local_width": int(info["width"]),
        "local_height": int(info["height"]),
        "frame_count": 1,
        "pdf_local_path": PNG.relative_to(ROOT).as_posix(),
        "pdf_local_bytes": PNG.stat().st_size,
        "pdf_local_sha256": digest(PNG),
        "pdf_companion_source": thumb_url,
        "original_bytes": int(info["size"]),
        "original_sha1": info["sha1"],
        "original_width": int(info["width"]),
        "original_height": int(info["height"]),
        "mime": info["mime"],
        "media_type": info.get("mediatype", "DRAWING"),
        "source_timestamp": info.get("timestamp", ""),
        "uploader": info.get("user", ""),
        "artist": ext(info, "Artist"),
        "credit": ext(info, "Credit"),
        "license_short": ext(info, "LicenseShortName"),
        "usage_terms": ext(info, "UsageTerms"),
        "license_url": ext(info, "LicenseUrl"),
        "attribution_required": ext(info, "AttributionRequired"),
        "source_course_creator": "Holger Brenner / Wikiversity course page",
        "source_course_license": "CC BY-SA 4.0",
        "description_pageid": media_page["pageid"],
        "description_revid": rev["revid"],
        "description_timestamp": rev["timestamp"],
        "description_mediawiki_sha1": rev["sha1"],
        "description_wikitext_bytes": len(content.encode("utf-8")),
        "description_wikitext_sha256": bytes_digest(content.encode("utf-8")),
        "html_animation_preserved": False,
    }
    with RIGHTS.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(row), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)

    creator = row["artist"] or row["uploader"] or "lihat metadata sumber"
    licence_text = f"[{licence}]({row['license_url']})" if row["license_url"] else licence
    CREDITS.write_text(
        "\n".join(
            [
                "# Kredit media Unit 15 {#agc-media-credits-unit-15}",
                "",
                "Kredit mengikuti satu gambar dalam Kuliah 15. Komponen mempertahankan lisensi sumbernya sendiri.",
                "",
                f"1. **{CAPTION}** - [{row['metadata_title']}]({row['description_url']}); pencipta/atribusi: {creator}; lisensi/status hak: {licence_text}.",
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )

    pdf_records = []
    for witness in manifest["official_pdf_witnesses"]:
        title = commons_file_title(witness["source_file_title"])
        page = by_key[title_key(title)]
        pdf_info = page["imageinfo"][0]
        local = ROOT / witness["local_path"]
        if not local.is_file() or local.is_symlink():
            raise RuntimeError(f"Missing official PDF witness: {local}")
        if local.stat().st_size != int(pdf_info["size"]) or digest(local, "sha1") != pdf_info["sha1"]:
            raise RuntimeError(f"Official PDF bytes disagree with Commons: {title}")
        if not local.read_bytes().startswith(b"%PDF-"):
            raise RuntimeError(f"Invalid official PDF signature: {title}")
        component = component_rights(page, pdf_info)
        component.update(
            {
                "local_path": local.relative_to(ROOT).as_posix(),
                "local_bytes": local.stat().st_size,
                "local_sha256": digest(local),
                "source_bytes": int(pdf_info["size"]),
                "source_sha1": pdf_info["sha1"],
                "source_timestamp": pdf_info.get("timestamp", ""),
            }
        )
        pdf_records.append(component)

    closure = {
        "schema": "brenner-unit-media-closure-v2",
        "unit": UNIT,
        "authority_only_boundary": True,
        "reader_media_positions": 1,
        "animated_html_positions": 0,
        "unique_local_assets": 2,
        "metadata_file": file_fact(META),
        "commons_reported_thumbnail_dimensions": [reported_thumb[0], reported_thumb[1]],
        "decoded_thumbnail_dimensions": [thumb_width, thumb_height],
        "thumbnail_dimension_note": "Commons reports 500x500; the returned PNG decodes as 500x501, retained byte-exactly.",
        "rights_file": RIGHTS.relative_to(ROOT).as_posix(),
        "rights_bytes": RIGHTS.stat().st_size,
        "rights_sha256": digest(RIGHTS),
        "reader_credits_file": CREDITS.relative_to(ROOT).as_posix(),
        "reader_credits_bytes": CREDITS.stat().st_size,
        "reader_credits_sha256": digest(CREDITS),
        "official_pdf_witnesses_are_not_media_positions": True,
        "official_pdf_component_rights": sorted(pdf_records, key=lambda item: item["local_path"]),
        "assets": [
            {
                "asset_id": row["asset_id"],
                "repository": "commons",
                "metadata_title": row["metadata_title"],
                "local_path": row["local_path"],
                "local_bytes": row["local_bytes"],
                "local_sha256": row["local_sha256"],
                "pdf_local_path": row["pdf_local_path"],
                "pdf_local_bytes": row["pdf_local_bytes"],
                "pdf_local_sha256": row["pdf_local_sha256"],
                "selected_form": row["selected_form"],
                "license_short": row["license_short"],
                "license_url": row["license_url"],
                "html_animation_preserved": False,
            }
        ],
    }
    CLOSURE.write_text(json.dumps(closure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "unit": UNIT, "media_positions": 1, "binary_surfaces": 2, "pdf_witnesses": 2, "rights_sha256": digest(RIGHTS), "closure_sha256": digest(CLOSURE)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
