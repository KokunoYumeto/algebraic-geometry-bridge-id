#!/usr/bin/env python3
"""Freeze one-image Brenner unit media, credits, rights, and official-PDF rights."""

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
            time.sleep(0.4)
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
    for prefix in ("Datei:", "File:"):
        if value.startswith(prefix):
            return "File:" + value[len(prefix) :]
    return "File:" + value


def pdf_rights(page: dict[str, Any], local: Path) -> dict[str, Any]:
    infos = page.get("imageinfo", [])
    if len(infos) != 1:
        raise RuntimeError(f"No unique PDF imageinfo for {page.get('title')!r}")
    info = infos[0]
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
    parser.add_argument("--unit", required=True, type=int)
    parser.add_argument("--resource-title", required=True)
    parser.add_argument("--local-name", required=True)
    parser.add_argument("--caption", required=True)
    parser.add_argument("--alt", required=True)
    parser.add_argument("--source-inline-license-label", default="")
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
    resource_title = commons_file_title(args.resource_title)
    expected_name = resource_title.removeprefix("File:")
    if {title_key(value) for value in substantive} != {title_key(expected_name)}:
        raise RuntimeError(f"Unexpected Unit {unit} media closure: {substantive}")

    pdf_titles = [commons_file_title(row["source_file_title"]) for row in manifest["official_pdf_witnesses"]]
    requested = [resource_title] + pdf_titles
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
    raw = fetch(API + "?" + urllib.parse.urlencode(params), accept="application/json")
    metadata_path = ROOT / "authority" / f"commons-imageinfo-unit-{unit_label}.json"
    metadata_path.write_bytes(raw)
    payload = json.loads(raw.decode("utf-8"))
    if payload.get("error"):
        raise RuntimeError(f"Commons API error: {payload['error']}")
    pages = payload.get("query", {}).get("pages", [])
    if len(pages) != len(requested) or any(page.get("missing") for page in pages):
        raise RuntimeError("Commons closure did not resolve every requested file")
    by_key = {title_key(page["title"]): page for page in pages}
    if set(by_key) != {title_key(value) for value in requested}:
        raise RuntimeError("Commons title closure drift")

    page = by_key[title_key(resource_title)]
    infos = page.get("imageinfo", [])
    if len(infos) != 1:
        raise RuntimeError("No unique substantive imageinfo")
    info = infos[0]
    rev, content = revision(page)
    original_url = info["url"].split("?", 1)[0]
    use_thumbnail = int(info["width"]) > 500 or info.get("mime") == "image/svg+xml"
    selected_url = info.get("thumburl") if use_thumbnail else original_url
    if not selected_url:
        raise RuntimeError("Commons supplied no bounded reader URL")
    assets = ROOT / "authority" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    local = assets / args.local_name
    if not local.is_file():
        local.write_bytes(fetch(selected_url, accept=info.get("mime", "image/*")))
    if local.is_symlink():
        raise RuntimeError(f"Reader asset is not a regular file: {local}")
    with Image.open(local) as image:
        image.verify()
    with Image.open(local) as image:
        width, height = int(image.width), int(image.height)
    if width > 500:
        raise RuntimeError("Reader asset exceeds 500 pixels in width")
    if use_thumbnail:
        if width != int(info["thumbwidth"]) or abs(height - int(info["thumbheight"])) > 1:
            raise RuntimeError("Commons thumbnail dimensions disagree")
    elif local.stat().st_size != int(info["size"]) or digest(local, "sha1") != info["sha1"]:
        raise RuntimeError("Original raster bytes disagree with Commons")
    licence = ext(info, "LicenseShortName") or ext(info, "UsageTerms")
    if not licence:
        raise RuntimeError("Commons supplied no image licence witness")
    license_template_lines = [
        line.strip()
        for line in content.splitlines()
        if re.search(r"\{\{(?:self|cc-|gfdl)", line, flags=re.I)
    ]

    row = {
        "asset_id": f"br-ak-u{unit_label}-media-001",
        "reader_order": 1,
        "reader_caption_id": args.caption,
        "reader_alt_id": args.alt,
        "resource_title": resource_title,
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
            if use_thumbnail and (width, height) != (int(info["thumbwidth"]), int(info["thumbheight"]))
            else ""
        ),
        "frame_count": 1,
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
        "license_short": ext(info, "LicenseShortName"),
        "usage_terms": ext(info, "UsageTerms"),
        "license_url": ext(info, "LicenseUrl"),
        "attribution_required": ext(info, "AttributionRequired"),
        "source_course_inline_license_label": args.source_inline_license_label,
        "commons_description_license_templates": " | ".join(license_template_lines),
        "license_discrepancy_note": (
            f"Wikiversity inline label {args.source_inline_license_label}; frozen Commons metadata offers {licence}. Reuse binds the Commons option."
            if args.source_inline_license_label
            and args.source_inline_license_label.casefold() != licence.casefold()
            else ""
        ),
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
    rights = ROOT / "authority" / f"RIGHTS-unit-{unit_label}.csv"
    with rights.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(row), lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)
    credits = ROOT / "source" / "id-ID" / f"media-credits-unit-{unit_label}.md"
    creator = row["artist"] or row["uploader"] or "lihat metadata sumber"
    licence_text = f"[{licence}]({row['license_url']})" if row["license_url"] else licence
    discrepancy_lines = []
    if row["license_discrepancy_note"]:
        discrepancy_lines = [
            "",
            f"Catatan hak: label sebaris pada halaman kuliah adalah `{args.source_inline_license_label}`, sedangkan deskripsi Commons yang dibekukan memuat `{row['commons_description_license_templates']}` dan metadata Commons menawarkan {licence_text}. Edisi mengikat opsi Commons tersebut, bukan label sebaris yang berbeda.",
        ]
    credits.write_text(
        "\n".join(
            [
                f"# Kredit media Unit {unit} {{#agc-media-credits-unit-{unit_label}}}",
                "",
                f"Satu posisi media substantif pada Kuliah {unit} mempertahankan identitas Commons dan lisensi sumbernya. Dua PDF resmi adalah saksi authority, bukan posisi media pembaca tambahan.",
                "",
                f"1. **{args.caption}** - [{row['metadata_title']}]({row['description_url']}); pencipta/atribusi: {creator}; lisensi/status hak: {licence_text}.",
                *discrepancy_lines,
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )
    pdf_records = [
        pdf_rights(by_key[title_key(title)], ROOT / witness["local_path"])
        for title, witness in zip(pdf_titles, manifest["official_pdf_witnesses"], strict=True)
    ]
    closure = {
        "schema": "brenner-unit-media-closure-v2",
        "unit": unit,
        "authority_only_boundary": True,
        "reader_media_positions": 1,
        "animated_html_positions": 0,
        "unique_local_assets": 1,
        "metadata_file": metadata_path.relative_to(ROOT).as_posix(),
        "metadata_bytes": metadata_path.stat().st_size,
        "metadata_sha256": digest(metadata_path),
        "rights_file": rights.relative_to(ROOT).as_posix(),
        "rights_bytes": rights.stat().st_size,
        "rights_sha256": digest(rights),
        "reader_credits_file": credits.relative_to(ROOT).as_posix(),
        "reader_credits_bytes": credits.stat().st_size,
        "reader_credits_sha256": digest(credits),
        "official_pdf_witnesses_are_not_media_positions": True,
        "source_inline_license_discrepancy": {
            "source_inline_label": args.source_inline_license_label,
            "commons_license_short": row["license_short"],
            "commons_usage_terms": row["usage_terms"],
            "commons_description_license_templates": row["commons_description_license_templates"],
            "reuse_option_bound": row["license_short"] or row["usage_terms"],
            "note": row["license_discrepancy_note"],
        },
        "official_pdf_component_rights": sorted(pdf_records, key=lambda item: item["local_path"]),
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
        ],
    }
    closure_path = ROOT / "authority" / f"ASSET_CLOSURE-unit-{unit_label}.json"
    closure_path.write_text(json.dumps(closure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": "PASS",
                "unit": unit,
                "media_positions": 1,
                "pdf_witnesses": 2,
                "rights_sha256": digest(rights),
                "closure_sha256": digest(closure_path),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
