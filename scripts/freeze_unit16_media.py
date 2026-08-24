#!/usr/bin/env python3
"""Freeze Unit 16 Commons media and component-rights evidence.

The helper binds the three lecture images, the public Solution 16.12 sketch,
and both official PDF witnesses to Commons imageinfo and description
revisions. It stores a bounded reader image no wider than 500 pixels, a
component-rights ledger, Indonesian credits, and a closure receipt. It never
edits the frozen Wikiversity unit authority manifest.
"""

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
API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "Codex-authority-freezer/1.0 (independent edition preservation)"
UNIT = 16
UNIT_DIR = ROOT / "authority" / "wikiversity" / "unit-16"
MANIFEST = UNIT_DIR / "UNIT_AUTHORITY_MANIFEST.json"
META = ROOT / "authority" / "commons-imageinfo-unit-16.json"
ASSETS = ROOT / "authority" / "assets"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-16.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-16.json"
CREDITS = ROOT / "source" / "id-ID" / "media-credits-unit-16.md"

MEDIA = (
    {
        "resource_title": "File:Kaffeefilter.jpg",
        "caption": "Sebuah filter dapat diidentifikasi melalui apa yang tertahan di dalamnya",
        "alt": "Kertas penyaring berisi ampas kopi di dalam penyangga keramik putih",
        "local_name": "Kaffeefilter-500.jpg",
    },
    {
        "resource_title": "File:Cone_intersects_line.png",
        "caption": "Tidak setiap fungsi pada kerucut di luar sebuah garis dapat diperluas ke seluruh ruang afin tanpa garis tersebut",
        "alt": "Kerucut ganda dalam kotak koordinat x y z yang berpotongan dengan sebuah garis miring",
        "local_name": "Cone_intersects_line.png",
    },
    {
        "resource_title": "File:FiberBundle 2.png",
        "caption": "Serat-serat suatu pemetaan; M adalah kodomain dan domain merupakan gabungan semua serat",
        "alt": "Garis-garis serat vertikal di atas cakram U pada ruang dasar berbentuk oval yang diberi label M",
        "local_name": "FiberBundle_2.png",
    },
    {
        "resource_title": "File:Draft0.svg",
        "caption": "Sketsa gabungan tiga sumbu koordinat pada Solusi 16.12",
        "alt": "Tiga sumbu koordinat yang berpotongan di titik asal",
        "local_name": "Draft0-500.png",
    },
)


def digest(path: Path, algorithm: str = "sha256") -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def bytes_digest(value: bytes, algorithm: str = "sha256") -> str:
    return hashlib.new(algorithm, value).hexdigest()


def fetch(url: str, *, accept: str = "*/*", attempts: int = 8) -> bytes:
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": accept}
    )
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


def revision(page: dict[str, Any]) -> tuple[dict[str, Any], str]:
    revisions = page.get("revisions", [])
    if len(revisions) != 1:
        raise RuntimeError(f"No unique description revision for {page.get('title')!r}")
    item = revisions[0]
    content = item.get("slots", {}).get("main", {}).get("content")
    if not isinstance(content, str):
        raise RuntimeError(f"No description wikitext for {page.get('title')!r}")
    return item, content


def title_key(value: str) -> str:
    return value.replace("_", " ").casefold()


def commons_file_title(value: str) -> str:
    """Normalize a Wikiversity German file-namespace title for Commons."""
    for prefix in ("Datei:", "File:"):
        if value.startswith(prefix):
            return "File:" + value[len(prefix) :]
    return "File:" + value


def file_fact(path: Path) -> dict[str, Any]:
    return {
        "file": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }


def media_row(
    *, item: dict[str, str], page: dict[str, Any], order: int
) -> dict[str, Any]:
    infos = page.get("imageinfo", [])
    if len(infos) != 1:
        raise RuntimeError(f"No unique imageinfo for {page.get('title')!r}")
    info = infos[0]
    rev, content = revision(page)
    original_url = info["url"].split("?", 1)[0]
    original_width = int(info["width"])
    use_thumbnail = original_width > 500 or info.get("mime") == "image/svg+xml"
    selected_url = info.get("thumburl") if use_thumbnail else original_url
    if not selected_url:
        raise RuntimeError(f"Commons supplied no bounded reader URL for {page.get('title')!r}")
    local = ASSETS / item["local_name"]
    if not local.is_file():
        local.write_bytes(fetch(selected_url, accept=info.get("mime", "image/*")))
    if local.is_symlink():
        raise RuntimeError(f"Reader asset is not a regular file: {local}")
    with Image.open(local) as image:
        image.verify()
    with Image.open(local) as image:
        width, height = int(image.width), int(image.height)
    if width > 500:
        raise RuntimeError(f"Reader asset exceeds the bounded 500px width: {local}")
    if not use_thumbnail:
        if local.stat().st_size != int(info["size"]) or digest(local, "sha1") != info["sha1"]:
            raise RuntimeError(f"Original raster bytes disagree with Commons: {local}")
    else:
        reported_thumb = (int(info["thumbwidth"]), int(info["thumbheight"]))
        if width != reported_thumb[0] or abs(height - reported_thumb[1]) > 1:
            raise RuntimeError(f"Commons thumbnail dimensions disagree: {local}")

    licence = ext(info, "LicenseShortName") or ext(info, "UsageTerms")
    if not licence:
        raise RuntimeError(f"Commons supplied no licence witness for {page.get('title')!r}")
    return {
        "asset_id": f"br-ak-u16-media-{order:03d}",
        "reader_order": order,
        "reader_caption_id": item["caption"],
        "reader_alt_id": item["alt"],
        "resource_title": item["resource_title"],
        "metadata_title": page["title"],
        "repository": "commons",
        "description_url": info["descriptionurl"],
        "original_url": original_url,
        "selected_url": selected_url,
        "selected_form": "official Commons 500px PNG thumbnail" if use_thumbnail else "original Commons raster",
        "local_path": local.relative_to(ROOT).as_posix(),
        "local_bytes": local.stat().st_size,
        "local_sha256": digest(local),
        "local_width": width,
        "local_height": height,
        "reported_thumb_width": int(info["thumbwidth"]) if use_thumbnail else "",
        "reported_thumb_height": int(info["thumbheight"]) if use_thumbnail else "",
        "thumbnail_dimension_discrepancy": (
            f"decoded={width}x{height};reported={int(info['thumbwidth'])}x{int(info['thumbheight'])}"
            if use_thumbnail
            and (width, height) != (int(info["thumbwidth"]), int(info["thumbheight"]))
            else ""
        ),
        "frame_count": 1,
        "pdf_local_path": "",
        "pdf_local_bytes": "",
        "pdf_local_sha256": "",
        "pdf_width": "",
        "pdf_height": "",
        "pdf_companion_source": "",
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
        "description_pageid": page["pageid"],
        "description_revid": rev["revid"],
        "description_timestamp": rev["timestamp"],
        "description_mediawiki_sha1": rev["sha1"],
        "description_wikitext_bytes": len(content.encode("utf-8")),
        "description_wikitext_sha256": bytes_digest(content.encode("utf-8")),
        "html_animation_preserved": False,
    }


def pdf_rights(page: dict[str, Any], local: Path) -> dict[str, Any]:
    info_rows = page.get("imageinfo", [])
    if len(info_rows) != 1:
        raise RuntimeError(f"No unique PDF imageinfo for {page.get('title')!r}")
    info = info_rows[0]
    rev, content = revision(page)
    if not local.is_file() or local.is_symlink():
        raise RuntimeError(f"Missing/non-regular official PDF witness: {local}")
    if local.stat().st_size != int(info["size"]) or digest(local, "sha1") != info["sha1"]:
        raise RuntimeError(f"Official PDF bytes disagree with Commons: {page['title']}")
    if info.get("mime") != "application/pdf" or not local.read_bytes().startswith(b"%PDF-"):
        raise RuntimeError(f"Invalid official PDF witness: {page['title']}")
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
        "local_path": local.relative_to(ROOT).as_posix(),
        "local_bytes": local.stat().st_size,
        "local_sha256": digest(local),
        "source_bytes": int(info["size"]),
        "source_sha1": info["sha1"],
        "source_timestamp": info.get("timestamp", ""),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-metadata", action="store_true")
    args = parser.parse_args()
    if not MANIFEST.is_file():
        raise RuntimeError(f"Unit 16 authority manifest is absent: {MANIFEST}")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("unit_number") != UNIT:
        raise RuntimeError("Authority manifest is not Unit 16")
    image_names = set(manifest.get("images", {}).get("lecture", [])) | set(
        manifest.get("images", {}).get("worksheet", [])
    )
    substantive = sorted(name for name in image_names if not name.casefold().endswith(".pdf"))
    expected_substantive = sorted(
        item["resource_title"].removeprefix("File:") for item in MEDIA[:3]
    )
    if {title_key(value) for value in substantive} != {
        title_key(value) for value in expected_substantive
    }:
        raise RuntimeError(
            f"Unexpected Unit 16 substantive media closure: {substantive}; expected {expected_substantive}"
        )
    solution_html = UNIT_DIR / "solution-ex12.html"
    if "Draft0.svg" not in solution_html.read_text(encoding="utf-8"):
        raise RuntimeError("Public Solution 16.12 no longer binds File:Draft0.svg")

    pdf_titles = [
        commons_file_title(row["source_file_title"])
        for row in manifest["official_pdf_witnesses"]
    ]
    requested = [item["resource_title"] for item in MEDIA] + pdf_titles
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
    if len(pages) != len(requested) or any(page.get("missing") for page in pages):
        raise RuntimeError(f"Commons closure did not resolve all requested files: {pages}")
    by_key = {title_key(page["title"]): page for page in pages}
    if set(by_key) != {title_key(value) for value in requested}:
        raise RuntimeError(f"Commons title closure drift: {sorted(page['title'] for page in pages)}")

    ASSETS.mkdir(parents=True, exist_ok=True)
    rows = [
        media_row(item=item, page=by_key[title_key(item["resource_title"])], order=order)
        for order, item in enumerate(MEDIA, start=1)
    ]
    with RIGHTS.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    credit_lines = [
        "# Kredit media Unit 16 {#agc-media-credits-unit-16}",
        "",
        "Kredit mengikuti urutan gambar dalam Kuliah 16 dan Solusi Publik 16.12. Setiap komponen mempertahankan lisensi sumbernya sendiri.",
        "",
    ]
    for row in rows:
        creator = row["artist"] or row["uploader"] or "lihat metadata sumber"
        licence = row["license_short"] or row["usage_terms"] or "lihat halaman sumber"
        licence_text = (
            f"[{licence}]({row['license_url']})" if row["license_url"] else str(licence)
        )
        credit_lines.append(
            f"{row['reader_order']}. **{row['reader_caption_id']}** - "
            f"[{row['metadata_title']}]({row['description_url']}); "
            f"pencipta/atribusi: {creator}; lisensi/status hak: {licence_text}."
        )
        credit_lines.append("")
    CREDITS.write_text("\n".join(credit_lines), encoding="utf-8", newline="\n")

    pdf_records = []
    for witness in manifest["official_pdf_witnesses"]:
        title = commons_file_title(witness["source_file_title"])
        local = ROOT / witness["local_path"]
        pdf_records.append(pdf_rights(by_key[title_key(title)], local))

    closure = {
        "schema": "brenner-unit-media-closure-v2",
        "unit": UNIT,
        "authority_only_boundary": True,
        "reader_media_positions": len(rows),
        "animated_html_positions": 0,
        "unique_local_assets": len(rows),
        "metadata_file": file_fact(META),
        "rights_file": RIGHTS.relative_to(ROOT).as_posix(),
        "rights_bytes": RIGHTS.stat().st_size,
        "rights_sha256": digest(RIGHTS),
        "reader_credits_file": CREDITS.relative_to(ROOT).as_posix(),
        "reader_credits_bytes": CREDITS.stat().st_size,
        "reader_credits_sha256": digest(CREDITS),
        "official_pdf_witnesses_are_not_media_positions": True,
        "official_pdf_component_rights": sorted(pdf_records, key=lambda row: row["local_path"]),
        "assets": [
            {
                "asset_id": row["asset_id"],
                "repository": row["repository"],
                "metadata_title": row["metadata_title"],
                "local_path": row["local_path"],
                "local_bytes": row["local_bytes"],
                "local_sha256": row["local_sha256"],
                "license_short": row["license_short"],
                "license_url": row["license_url"],
                "html_animation_preserved": False,
            }
            for row in rows
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
                "unit": UNIT,
                "media_positions": len(rows),
                "binary_surfaces": len(rows),
                "pdf_witnesses": len(pdf_records),
                "rights_sha256": digest(RIGHTS),
                "closure_sha256": digest(CLOSURE),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
