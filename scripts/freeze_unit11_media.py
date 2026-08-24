#!/usr/bin/env python3
"""Freeze Unit 11 Commons media and component-rights evidence.

This authority-only helper binds the one substantive reader image and the two
official PDF witnesses to Commons imageinfo, description revisions, local
bytes, dimensions, and per-component licence metadata.  It does not create or
modify Indonesian reader content.
"""

from __future__ import annotations

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
API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "Codex-authority-freezer/1.0 (independent edition preservation)"
UNIT_DIR = ROOT / "authority" / "wikiversity" / "unit-11"
MANIFEST = UNIT_DIR / "UNIT_AUTHORITY_MANIFEST.json"
META = ROOT / "authority" / "commons-imageinfo-unit-11.json"
DESCRIPTION = ROOT / "authority" / "commons-description-unit-11.wikitext"
ASSET = ROOT / "authority" / "assets" / "Disjoint_ellipses.png"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-11.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-11.json"

MEDIA_TITLE = "File:Disjoint ellipses.png"
MEDIA_THUMBNAIL_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/"
    "Disjoint_ellipses.png/250px-Disjoint_ellipses.png"
)
LECTURE_PDF_TITLE = "File:Algebraische Kurven (Osnabrück 2025-2026)Vorlesung11.pdf"
WORKSHEET_PDF_TITLE = "File:Algebraische Kurven (Osnabrück 2025-2026)Arbeitsblatt11.pdf"
EXPECTED_TITLES = (MEDIA_TITLE, LECTURE_PDF_TITLE, WORKSHEET_PDF_TITLE)
PDF_LOCAL = {
    LECTURE_PDF_TITLE: ROOT / "authority" / "artifacts" / "lecture-11-official.pdf",
    WORKSHEET_PDF_TITLE: ROOT / "authority" / "artifacts" / "worksheet-11-official.pdf",
}


def digest(path: Path, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def bytes_digest(value: bytes, algorithm: str = "sha256") -> str:
    return hashlib.new(algorithm, value).hexdigest()


def file_fact(path: Path) -> dict[str, Any]:
    return {
        "file": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }


def plain(value: object) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(html.unescape(text).split())


def ext(info: dict[str, Any], key: str) -> str:
    return plain(info.get("extmetadata", {}).get(key, {}).get("value", ""))


def fetch(url: str, *, accept: str, attempts: int = 6) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
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


def revision(page: dict[str, Any]) -> tuple[dict[str, Any], str]:
    revisions = page.get("revisions", [])
    if len(revisions) != 1:
        raise RuntimeError(f"No unique description revision for {page.get('title')!r}")
    item = revisions[0]
    content = item.get("slots", {}).get("main", {}).get("content")
    if not isinstance(content, str):
        raise RuntimeError(f"No description wikitext for {page.get('title')!r}")
    return item, content


def page_rights(page: dict[str, Any], info: dict[str, Any]) -> dict[str, Any]:
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
    if not MANIFEST.is_file():
        raise RuntimeError(f"Unit 11 authority manifest is absent: {MANIFEST}")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("unit_number") != 11:
        raise RuntimeError("Authority manifest is not Unit 11")
    image_names = set(manifest.get("images", {}).get("lecture", [])) | set(
        manifest.get("images", {}).get("worksheet", [])
    )
    substantive = sorted(name for name in image_names if not name.lower().endswith(".pdf"))
    if substantive != ["Disjoint_ellipses.png"]:
        raise RuntimeError(f"Unexpected Unit 11 substantive media closure: {substantive}")

    params = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "prop": "imageinfo|revisions",
        "iiprop": "url|size|mime|sha1|timestamp|user|mediatype|extmetadata",
        "rvprop": "ids|timestamp|sha1|content",
        "rvslots": "main",
        "titles": "|".join(EXPECTED_TITLES),
    }
    url = API + "?" + urllib.parse.urlencode(params)
    raw = META.read_bytes() if META.is_file() else fetch(url, accept="application/json")
    parsed = json.loads(raw.decode("utf-8"))
    if parsed.get("error"):
        raise RuntimeError(f"Commons API error: {parsed['error']}")
    META.write_bytes(raw)
    pages = parsed.get("query", {}).get("pages", [])
    if len(pages) != 3 or any(page.get("missing") for page in pages):
        raise RuntimeError(f"Commons closure did not resolve three files: {pages}")
    by_title = {page["title"].replace("_", " "): page for page in pages}
    if set(by_title) != set(EXPECTED_TITLES):
        raise RuntimeError(f"Commons title closure drift: {sorted(by_title)}")

    for title, local in PDF_LOCAL.items():
        page = by_title[title]
        infos = page.get("imageinfo", [])
        if len(infos) != 1:
            raise RuntimeError(f"No unique imageinfo for {title}")
        info = infos[0]
        if not local.is_file() or local.is_symlink():
            raise RuntimeError(f"Missing/non-regular official PDF witness: {local}")
        if local.stat().st_size != int(info["size"]) or digest(local, "sha1") != info["sha1"]:
            raise RuntimeError(f"Official PDF bytes disagree with Commons metadata: {title}")
        if not info.get("mime") == "application/pdf" or not local.read_bytes().startswith(b"%PDF-"):
            raise RuntimeError(f"Invalid official PDF witness: {title}")

    media_page = by_title[MEDIA_TITLE]
    media_infos = media_page.get("imageinfo", [])
    if len(media_infos) != 1:
        raise RuntimeError("No unique Commons imageinfo for Unit 11 reader media")
    info = media_infos[0]
    rev, content = revision(media_page)
    DESCRIPTION.write_text(content, encoding="utf-8", newline="\n")
    ASSET.parent.mkdir(parents=True, exist_ok=True)
    if not ASSET.is_file():
        ASSET.write_bytes(fetch(MEDIA_THUMBNAIL_URL, accept="image/png"))
    with Image.open(ASSET) as image:
        image.verify()
    with Image.open(ASSET) as image:
        width, height = int(image.width), int(image.height)
        frames = int(getattr(image, "n_frames", 1))
    if (width, height) != (int(info["width"]), int(info["height"])):
        raise RuntimeError("Local image dimensions disagree with Commons metadata")
    local_matches_original = (
        ASSET.stat().st_size == int(info["size"]) and digest(ASSET, "sha1") == info["sha1"]
    )
    selected_url = info["url"].split("?", 1)[0] if local_matches_original else MEDIA_THUMBNAIL_URL
    selected_form = "original" if local_matches_original else "commons-rendered-250px-thumbnail-at-source-native-width"

    license_short = ext(info, "LicenseShortName")
    usage_terms = ext(info, "UsageTerms")
    if not (license_short or usage_terms):
        raise RuntimeError("Commons did not provide an image licence witness")
    row = {
        "asset_id": "br-ak-u11-media-001",
        "reader_order": 1,
        "resource_title": MEDIA_TITLE,
        "metadata_title": media_page["title"],
        "repository": "commons",
        "description_url": info["descriptionurl"],
        "original_url": info["url"].split("?", 1)[0],
        "selected_url": selected_url,
        "selected_form": selected_form,
        "local_path": ASSET.relative_to(ROOT).as_posix(),
        "local_bytes": ASSET.stat().st_size,
        "local_sha256": digest(ASSET),
        "local_width": width,
        "local_height": height,
        "frame_count": frames,
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
        "artist": ext(info, "Artist"),
        "credit": ext(info, "Credit"),
        "license_short": license_short,
        "usage_terms": usage_terms,
        "license_url": ext(info, "LicenseUrl"),
        "attribution_required": ext(info, "AttributionRequired"),
        "source_course_creator": "Holger Brenner / Wikiversity course page",
        "source_course_license": "CC BY-SA 4.0",
        "description_pageid": media_page["pageid"],
        "description_revid": rev["revid"],
        "description_timestamp": rev["timestamp"],
        "description_mediawiki_sha1": rev["sha1"],
        "description_wikitext_bytes": DESCRIPTION.stat().st_size,
        "description_wikitext_sha256": digest(DESCRIPTION),
        "html_animation_preserved": False,
    }
    with RIGHTS.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(row), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)

    pdf_rights = []
    for title, local in PDF_LOCAL.items():
        page = by_title[title]
        pdf_info = page["imageinfo"][0]
        component = page_rights(page, pdf_info)
        component.update(
            {
                "local_path": local.relative_to(ROOT).as_posix(),
                "local_bytes": local.stat().st_size,
                "local_sha256": digest(local),
                "source_bytes": int(pdf_info["size"]),
                "source_sha1": pdf_info["sha1"],
                "source_timestamp": pdf_info.get("timestamp"),
            }
        )
        pdf_rights.append(component)

    closure = {
        "schema": "brenner-unit-media-closure-v2",
        "unit": 11,
        "authority_only_boundary": True,
        "reader_media_positions": 1,
        "animated_html_positions": 0,
        "unique_local_assets": 1,
        "metadata_files": [file_fact(META), file_fact(DESCRIPTION)],
        "rights_file": RIGHTS.relative_to(ROOT).as_posix(),
        "rights_bytes": RIGHTS.stat().st_size,
        "rights_sha256": digest(RIGHTS),
        "reader_credits_status": "deferred_to_translation_boundary",
        "official_pdf_witnesses_are_not_media_positions": True,
        "local_media_original_byte_match": local_matches_original,
        "local_media_selection_note": (
            "The selected Commons-rendered 250px PNG has the same 250 by 246 pixel dimensions as "
            "the source original; original size and SHA-1 remain independently frozen above."
            if not local_matches_original
            else "The selected local media is the byte-exact Commons original."
        ),
        "official_pdf_component_rights": sorted(pdf_rights, key=lambda item: item["local_path"]),
        "assets": [
            {
                "asset_id": row["asset_id"],
                "repository": row["repository"],
                "local_path": row["local_path"],
                "local_bytes": row["local_bytes"],
                "local_sha256": row["local_sha256"],
                "selected_form": row["selected_form"],
                "selected_url": row["selected_url"],
                "html_animation_preserved": False,
            }
        ],
    }
    CLOSURE.write_text(
        json.dumps(closure, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "media_positions": 1,
                "pdf_witnesses": 2,
                "rights_sha256": digest(RIGHTS),
                "closure_sha256": digest(CLOSURE),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
