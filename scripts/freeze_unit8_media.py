#!/usr/bin/env python3
"""Freeze Unit 8 media, mixed-repository metadata, and component rights."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "authority" / "assets"
COMMONS_META = ROOT / "authority" / "commons-imageinfo-unit-08.json"
WIKIVERSITY_META = ROOT / "authority" / "wikiversity-imageinfo-unit-08.json"
LOCAL_DESCRIPTION = ROOT / "authority" / "wikiversity-local-description-unit-08.wikitext"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-08.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-08.json"
CREDITS = ROOT / "source" / "id-ID" / "media-credits-unit-08.md"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
WIKIVERSITY_API = "https://de.wikiversity.org/w/api.php"
USER_AGENT = "Codex algebraic-geometry-bridge-id media freeze (at user's direction)"

# Exact order of the six substantive image positions returned by the frozen
# Lecture 8 parse surface. The two parse-surface PDFs are official build
# witnesses and are frozen separately by freeze_brenner_unit.py.
MEDIA = (
    {
        "resource_title": "File:Lemniscate Building.gif",
        "metadata_title": "File:Lemniscate Building.gif",
        "repository": "commons",
        "source_creator": "Zorgit",
        "source_license": "CC BY-SA 3.0",
        "local_name": "Lemniscate_Building.gif",
        "pdf_name": "Lemniscate_Building-frame-1.png",
    },
    {
        "resource_title": "File:Parallelle lijnen.png",
        "metadata_title": "File:Parallelle lijnen.png",
        "repository": "commons",
        "source_creator": "Ellywa",
        "source_license": "CC BY-SA 3.0",
        "local_name": "Parallelle_lijnen.png",
        "pdf_name": "",
    },
    {
        "resource_title": "File:Ellipse tri.png",
        "metadata_title": "File:Ellipse tri.png",
        "repository": "commons",
        "source_creator": "David Shay (original uploader at Hebrew Wikipedia)",
        "source_license": "CC BY-SA 3.0",
        "local_name": "Ellipse_tri.png",
        "pdf_name": "",
    },
    {
        "resource_title": "File:Steam engine in action.gif",
        "metadata_title": "File:Steam engine in action.gif",
        "repository": "commons",
        "source_creator": "Panther",
        "source_license": "CC BY-SA 3.0",
        "local_name": "Steam_engine_in_action.gif",
        "pdf_name": "Steam_engine_in_action-frame-1.png",
    },
    {
        "resource_title": "File:Intersection of cylinders.jpg",
        "metadata_title": "File:Intersection of cylinders.jpg",
        "repository": "commons",
        "source_creator": "Jan Schoenke",
        "source_license": "CC BY-SA 3.0",
        "local_name": "Intersection_of_cylinders.jpg",
        "pdf_name": "",
    },
    {
        "resource_title": "File:Alg Kurven OS2008 Lsg8.10 v2.png",
        "metadata_title": "File:Alg Kurven OS2008 Lsg8.10 v2.png",
        "repository": "wikiversity-local",
        "source_creator": "Christian Boberg",
        "source_license": "CC BY-SA 3.0",
        "local_name": "Alg_Kurven_OS2008_Lsg8.10_v2.png",
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
            if error.code not in {429, 500, 502, 503, 504} or attempt == 6:
                raise
            retry_after = error.headers.get("Retry-After", "")
            delay = int(retry_after) if retry_after.isdigit() else 3 * attempt
            time.sleep(min(delay, 25))
        except (TimeoutError, URLError):
            if attempt == 6:
                raise
            time.sleep(min(2**attempt, 25))
    raise RuntimeError("unreachable retry state")


def fetch_api(api: str, params: dict[str, str]) -> bytes:
    payload = urlencode({"format": "json", "formatversion": "2", **params}).encode("utf-8")
    raw = fetch(api, payload)
    parsed = json.loads(raw)
    if "error" in parsed:
        raise RuntimeError(f"MediaWiki API error: {parsed['error']}")
    return raw


def digest(path: Path, algorithm: str = "sha256") -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def bytes_digest(value: bytes, algorithm: str = "sha256") -> str:
    return hashlib.new(algorithm, value).hexdigest()


def plain(value: object) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(html.unescape(text).split())


def ext(metadata: dict, key: str) -> str:
    return plain(metadata.get(key, {}).get("value", ""))


def title_key(title: str) -> str:
    value = " ".join(title.replace("_", " ").split()).casefold()
    return re.sub(r"^(file|datei):", "file:", value)


def dimensions(path: Path) -> tuple[int, int]:
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        return int(image.width), int(image.height)


def frame_count(path: Path) -> int:
    if path.suffix.casefold() != ".gif":
        return 1
    with Image.open(path) as image:
        return int(getattr(image, "n_frames", 1))


def make_first_frame(source: Path, target: Path) -> None:
    with Image.open(source) as image:
        image.seek(0)
        image.convert("RGBA").save(
            target,
            format="PNG",
            optimize=False,
            compress_level=9,
        )


def image_page(page: dict, expected_title: str) -> tuple[dict, dict]:
    if not page.get("imageinfo"):
        raise RuntimeError(f"Image metadata did not resolve: {expected_title}")
    return page, page["imageinfo"][0]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-metadata", action="store_true")
    args = parser.parse_args()
    ASSETS.mkdir(parents=True, exist_ok=True)
    CREDITS.parent.mkdir(parents=True, exist_ok=True)

    commons_titles = [
        item["metadata_title"] for item in MEDIA if item["repository"] == "commons"
    ]
    if COMMONS_META.is_file() and not args.refresh_metadata:
        commons_raw = COMMONS_META.read_bytes()
    else:
        commons_raw = fetch_api(
            COMMONS_API,
            {
                "action": "query",
                "prop": "imageinfo",
                "titles": "|".join(commons_titles),
                "iiprop": "url|sha1|size|mime|mediatype|timestamp|user|extmetadata",
            },
        )
        COMMONS_META.write_bytes(commons_raw)
    commons_data = json.loads(commons_raw)
    commons_pages = {
        title_key(page["title"]): page for page in commons_data["query"]["pages"]
    }

    local_item = next(item for item in MEDIA if item["repository"] == "wikiversity-local")
    if WIKIVERSITY_META.is_file() and not args.refresh_metadata:
        local_raw = WIKIVERSITY_META.read_bytes()
    else:
        local_raw = fetch_api(
            WIKIVERSITY_API,
            {
                "action": "query",
                "prop": "revisions|imageinfo",
                "titles": local_item["metadata_title"],
                "rvprop": "ids|timestamp|sha1|content",
                "rvslots": "main",
                "iiprop": "url|sha1|size|mime|mediatype|timestamp|user|extmetadata",
            },
        )
        WIKIVERSITY_META.write_bytes(local_raw)
    local_data = json.loads(local_raw)
    local_pages = local_data.get("query", {}).get("pages", [])
    if len(local_pages) != 1:
        raise RuntimeError(f"Local file page did not resolve uniquely: {local_item['metadata_title']}")
    local_page, local_info = image_page(local_pages[0], local_item["metadata_title"])
    local_revisions = local_page.get("revisions", [])
    if len(local_revisions) != 1:
        raise RuntimeError("Local file description has no unique current revision")
    local_revision = local_revisions[0]
    local_description = local_revision.get("slots", {}).get("main", {}).get("content")
    if not isinstance(local_description, str):
        raise RuntimeError("Local file description wikitext is absent")
    if "Bild-CC-by-sa-3.0" not in local_description:
        raise RuntimeError("Local file description no longer contains its CC BY-SA 3.0 declaration")
    LOCAL_DESCRIPTION.write_bytes(local_description.encode("utf-8"))

    rows: list[dict[str, object]] = []
    for order, item in enumerate(MEDIA, start=1):
        if item["repository"] == "commons":
            page = commons_pages.get(title_key(item["metadata_title"]))
            if page is None:
                raise RuntimeError(f"Commons metadata did not resolve: {item['metadata_title']}")
            page, info = image_page(page, item["metadata_title"])
            description_pageid: int | str = ""
            description_revid: int | str = ""
            description_timestamp = ""
            description_sha1 = ""
            description_bytes: int | str = ""
            description_content_sha256 = ""
        else:
            page, info = local_page, local_info
            description_pageid = int(local_page["pageid"])
            description_revid = int(local_revision["revid"])
            description_timestamp = local_revision["timestamp"]
            description_sha1 = local_revision["sha1"]
            description_raw = local_description.encode("utf-8")
            description_bytes = len(description_raw)
            description_content_sha256 = bytes_digest(description_raw)

        local = ASSETS / item["local_name"]
        selected_url = info["url"]
        if not local.is_file():
            local.write_bytes(fetch(selected_url))
        width, height = dimensions(local)
        if local.stat().st_size != int(info["size"]) or digest(local, "sha1") != info["sha1"]:
            raise RuntimeError(f"Original byte validation failed: {local.name}")
        if width != int(info["width"]) or height != int(info["height"]):
            raise RuntimeError(f"Original dimension validation failed: {local.name}")

        pdf_local = ASSETS / item["pdf_name"] if item["pdf_name"] else None
        pdf_source = ""
        if pdf_local:
            if local.suffix.casefold() != ".gif" or frame_count(local) < 2:
                raise RuntimeError(f"Expected animated GIF for PDF companion: {local.name}")
            make_first_frame(local, pdf_local)
            dimensions(pdf_local)
            pdf_source = "locally derived deterministic first frame from byte-exact source GIF"

        metadata = info.get("extmetadata", {})
        licence = ext(metadata, "LicenseShortName") or item["source_license"]
        if "CC BY-SA 3.0" not in licence:
            raise RuntimeError(f"Unexpected current licence for {page['title']}: {licence!r}")
        rows.append(
            {
                "asset_id": f"br-ak-u08-media-{order:03d}",
                "reader_order": order,
                "resource_title": item["resource_title"],
                "metadata_title": page["title"],
                "repository": item["repository"],
                "description_url": info["descriptionurl"],
                "original_url": info["url"].split("?", 1)[0],
                "selected_url": selected_url,
                "selected_form": "original",
                "local_path": f"authority/assets/{local.name}",
                "local_bytes": local.stat().st_size,
                "local_sha256": digest(local),
                "local_width": width,
                "local_height": height,
                "frame_count": frame_count(local),
                "pdf_local_path": f"authority/assets/{pdf_local.name}" if pdf_local else "",
                "pdf_local_bytes": pdf_local.stat().st_size if pdf_local else "",
                "pdf_local_sha256": digest(pdf_local) if pdf_local else "",
                "pdf_companion_source": pdf_source,
                "original_bytes": int(info["size"]),
                "original_sha1": info["sha1"],
                "original_width": int(info["width"]),
                "original_height": int(info["height"]),
                "mime": info["mime"],
                "media_type": info["mediatype"],
                "source_timestamp": info["timestamp"],
                "uploader": info["user"],
                "artist": ext(metadata, "Artist") or item["source_creator"],
                "credit": ext(metadata, "Credit"),
                "license_short": licence,
                "usage_terms": ext(metadata, "UsageTerms") or item["source_license"],
                "license_url": ext(metadata, "LicenseUrl"),
                "attribution_required": ext(metadata, "AttributionRequired") or "true",
                "source_course_creator": item["source_creator"],
                "source_course_license": item["source_license"],
                "description_pageid": description_pageid,
                "description_revid": description_revid,
                "description_timestamp": description_timestamp,
                "description_mediawiki_sha1": description_sha1,
                "description_wikitext_bytes": description_bytes,
                "description_wikitext_sha256": description_content_sha256,
                "html_animation_preserved": frame_count(local) > 1,
            }
        )

    with RIGHTS.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    credit_lines = [
        "# Kredit media Unit 8 {#agc-media-credits-unit-08}",
        "",
        "Enam posisi media Kuliah 8 mempertahankan atribusi dan lisensi komponennya masing-masing. Dua GIF tetap beranimasi dalam pembaca HTML; PDF memakai bingkai pertama deterministik.",
        "",
    ]
    for row in rows:
        licence = str(row["license_short"])
        if row["license_url"]:
            licence = f"[{licence}]({row['license_url']})"
        credit_lines.append(
            f"{row['reader_order']}. **{row['resource_title']}** - "
            f"[{row['metadata_title']}]({row['description_url']}); "
            f"pencipta/atribusi: {plain(row['artist'])}; lisensi: {licence}."
        )
    CREDITS.write_bytes(("\n".join(credit_lines) + "\n").encode("utf-8"))

    metadata_files = []
    for path, role in (
        (COMMONS_META, "commons_imageinfo_and_extmetadata"),
        (WIKIVERSITY_META, "local_imageinfo_and_description_revision"),
        (LOCAL_DESCRIPTION, "local_description_wikitext"),
    ):
        metadata_files.append(
            {
                "role": role,
                "file": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": digest(path),
            }
        )
    closure = {
        "schema": "brenner-unit-media-closure-v2",
        "unit": 8,
        "reader_media_positions": len(rows),
        "animated_html_positions": sum(1 for row in rows if row["html_animation_preserved"]),
        "unique_local_assets": len(rows) + sum(1 for row in rows if row["pdf_local_path"]),
        "metadata_files": metadata_files,
        "local_description_revision": {
            "title": local_page["title"],
            "pageid": local_page["pageid"],
            "revid": local_revision["revid"],
            "timestamp": local_revision["timestamp"],
            "mediawiki_sha1": local_revision["sha1"],
            "license_evidence": "{{Bild-CC-by-sa-3.0}} in frozen description wikitext",
        },
        "rights_file": RIGHTS.relative_to(ROOT).as_posix(),
        "rights_bytes": RIGHTS.stat().st_size,
        "rights_sha256": digest(RIGHTS),
        "reader_credits_file": CREDITS.relative_to(ROOT).as_posix(),
        "reader_credits_bytes": CREDITS.stat().st_size,
        "reader_credits_sha256": digest(CREDITS),
        "assets": [
            {
                "asset_id": row["asset_id"],
                "repository": row["repository"],
                "local_path": row["local_path"],
                "local_bytes": row["local_bytes"],
                "local_sha256": row["local_sha256"],
                "pdf_local_path": row["pdf_local_path"],
                "pdf_local_bytes": row["pdf_local_bytes"],
                "pdf_local_sha256": row["pdf_local_sha256"],
                "html_animation_preserved": row["html_animation_preserved"],
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
                "animated_html_positions": closure["animated_html_positions"],
                "binary_surfaces": closure["unique_local_assets"],
                "metadata_sources": len(metadata_files),
                "local_description_revid": local_revision["revid"],
                "rights_sha256": closure["rights_sha256"],
                "closure_sha256": digest(CLOSURE),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
