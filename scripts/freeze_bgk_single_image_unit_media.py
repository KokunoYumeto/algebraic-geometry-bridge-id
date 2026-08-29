#!/usr/bin/env python3
"""Freeze one-image BGK unit media, credits, rights, and official-PDF rights.

The freezer is deliberately isolated from the classical ``Algebraische Kurven``
outputs.  It consumes only the already-frozen BGK unit manifest and writes only
BGK-prefixed authority, reader-credit, and asset artifacts.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import io
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
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "Codex-BGK-authority-freezer/1.0 (independent edition preservation)"
COURSE_PROJECT = "German Wikiversity"
COURSE_TITLE = "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)"
COURSE_API = "https://de.wikiversity.org/w/api.php"
AUTHORITY_NAMESPACE = "authority/wikiversity-bgk"
MANIFEST_SCHEMA = "brenner-bgk-unit-authority-freeze-v1"
UNIT_MIN = 1
UNIT_MAX = 30


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
        url,
        headers={"User-Agent": USER_AGENT, "Accept": accept},
    )
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


def course_identity(manifest: dict[str, Any], unit: int) -> dict[str, Any]:
    source = manifest.get("source_identity", {})
    storage = manifest.get("storage_identity", {})
    expected = {
        "project": COURSE_PROJECT,
        "course_title": COURSE_TITLE,
        "source_api": COURSE_API,
    }
    observed = {key: source.get(key) for key in expected}
    if observed != expected:
        raise RuntimeError(
            f"Refusing mismatched BGK course identity: expected {expected}, got {observed}"
        )
    if manifest.get("schema") != MANIFEST_SCHEMA:
        raise RuntimeError(f"Unexpected BGK manifest schema: {manifest.get('schema')!r}")
    if manifest.get("unit_number") != unit:
        raise RuntimeError(f"Authority manifest is not BGK Unit {unit}")
    if storage.get("authority_namespace") != AUTHORITY_NAMESPACE:
        raise RuntimeError(
            "Refusing non-BGK authority namespace: "
            f"expected {AUTHORITY_NAMESPACE!r}, got {storage.get('authority_namespace')!r}"
        )
    if storage.get("artifact_prefix") != "bgk":
        raise RuntimeError("Refusing authority manifest without BGK artifact prefix")
    expected_lecture = f"{COURSE_TITLE}/Vorlesung {unit}"
    expected_worksheet = f"{COURSE_TITLE}/Arbeitsblatt {unit}"
    if source.get("lecture_title") != expected_lecture:
        raise RuntimeError("BGK lecture identity does not match the requested unit")
    if source.get("worksheet_title") != expected_worksheet:
        raise RuntimeError("BGK worksheet identity does not match the requested unit")
    return {
        **expected,
        "source_namespace_label": source.get("source_namespace_label"),
        "lecture_title": expected_lecture,
        "worksheet_title": expected_worksheet,
        "authority_namespace": AUTHORITY_NAMESPACE,
        "artifact_prefix": "bgk",
    }


def validate_local_name(value: str) -> str:
    candidate = Path(value)
    if candidate.name != value or candidate.is_absolute() or value in {".", ".."}:
        raise argparse.ArgumentTypeError("--local-name must be one safe filename")
    if not value.casefold().startswith("bgk-"):
        raise argparse.ArgumentTypeError("--local-name must begin with 'bgk-'")
    if candidate.suffix.casefold() not in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
        raise argparse.ArgumentTypeError("--local-name must name a supported raster asset")
    return value


def refuse_unless_resume(paths: list[Path], resume: bool) -> None:
    symlinks = [path for path in paths if path.is_symlink()]
    if symlinks:
        raise RuntimeError(f"Refusing symlink output target(s): {symlinks}")
    existing = [path for path in paths if path.exists()]
    if existing and not resume:
        rendered = ", ".join(path.relative_to(ROOT).as_posix() for path in existing)
        raise RuntimeError(
            f"Refusing to overwrite existing BGK output(s) without --resume: {rendered}"
        )
    nonfiles = [path for path in existing if not path.is_file()]
    if nonfiles:
        raise RuntimeError(f"Refusing non-file output target(s): {nonfiles}")


def pdf_rights(
    page: dict[str, Any],
    witness: dict[str, Any],
    manifest_path: Path,
) -> dict[str, Any]:
    infos = page.get("imageinfo", [])
    if len(infos) != 1:
        raise RuntimeError(f"No unique PDF imageinfo for {page.get('title')!r}")
    info = infos[0]
    rev, content = revision(page)
    local = ROOT / witness["local_path"]
    if not local.is_file() or local.is_symlink():
        raise RuntimeError(f"Missing/non-regular official PDF witness: {local}")
    if local.stat().st_size != int(witness["local_bytes"]):
        raise RuntimeError(f"Official PDF bytes disagree with BGK manifest: {local}")
    if digest(local) != witness["local_sha256"]:
        raise RuntimeError(f"Official PDF SHA-256 disagrees with BGK manifest: {local}")
    if int(witness["source_bytes"]) != int(info["size"]):
        raise RuntimeError(f"Commons PDF size drift: {page['title']}")
    if witness["mediawiki_sha1"] != info["sha1"]:
        raise RuntimeError(f"Commons PDF SHA-1 drift: {page['title']}")
    if local.stat().st_size != int(info["size"]) or digest(local, "sha1") != info["sha1"]:
        raise RuntimeError(f"Official PDF bytes disagree with Commons: {page['title']}")
    if info.get("mime") != "application/pdf" or not local.read_bytes().startswith(b"%PDF-"):
        raise RuntimeError(f"Invalid official PDF witness: {page['title']}")
    extmetadata_bytes = json.dumps(
        info.get("extmetadata", {}), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return {
        "title": page["title"],
        "pageid": page.get("pageid"),
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
        "extmetadata_canonical_json_sha256": bytes_digest(extmetadata_bytes),
        "local_path": local.relative_to(ROOT).as_posix(),
        "local_bytes": local.stat().st_size,
        "local_sha256": digest(local),
        "source_bytes": int(info["size"]),
        "source_sha1": info["sha1"],
        "source_timestamp": info.get("timestamp", ""),
        "manifest_file": manifest_path.relative_to(ROOT).as_posix(),
        "manifest_kind": witness.get("kind"),
    }


def csv_bytes(row: dict[str, Any]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(row), lineterminator="\n")
    writer.writeheader()
    writer.writerow(row)
    return stream.getvalue().encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--unit", required=True, type=int)
    parser.add_argument("--resource-title", required=True)
    parser.add_argument("--local-name", required=True, type=validate_local_name)
    parser.add_argument("--caption", required=True)
    parser.add_argument("--alt", required=True)
    parser.add_argument(
        "--source-inline-license-label",
        required=True,
        help="exact license label embedded beside the image in the frozen BGK source",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="explicitly permit replacement of the same BGK output filenames",
    )
    args = parser.parse_args()
    unit = args.unit
    if not UNIT_MIN <= unit <= UNIT_MAX:
        raise SystemExit(f"--unit must be between {UNIT_MIN} and {UNIT_MAX}")
    unit_label = f"{unit:02d}"
    manifest_path = (
        ROOT
        / "authority"
        / "wikiversity-bgk"
        / f"unit-{unit_label}"
        / "UNIT_AUTHORITY_MANIFEST.json"
    )
    if not manifest_path.is_file() or manifest_path.is_symlink():
        raise RuntimeError(f"Missing/non-regular BGK authority manifest: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    identity = course_identity(manifest, unit)

    image_names = set(manifest.get("images", {}).get("lecture", [])) | set(
        manifest.get("images", {}).get("worksheet", [])
    )
    substantive = sorted(name for name in image_names if not name.casefold().endswith(".pdf"))
    resource_title = commons_file_title(args.resource_title)
    expected_name = resource_title.removeprefix("File:")
    if len(substantive) != 1 or title_key(substantive[0]) != title_key(expected_name):
        raise RuntimeError(f"Unexpected BGK Unit {unit} media closure: {substantive}")

    witnesses = manifest.get("official_pdf_witnesses", [])
    if len(witnesses) != 2 or {row.get("kind") for row in witnesses} != {"lecture", "worksheet"}:
        raise RuntimeError("BGK authority manifest does not contain exactly both official PDF witnesses")
    pdf_titles = [commons_file_title(row["source_file_title"]) for row in witnesses]
    requested = [resource_title, *pdf_titles]
    if len({title_key(value) for value in requested}) != 3:
        raise RuntimeError("BGK Unit media and PDF titles are not three distinct Commons files")

    metadata_path = ROOT / "authority" / f"commons-imageinfo-bgk-unit-{unit_label}.json"
    rights_path = ROOT / "authority" / f"RIGHTS-bgk-unit-{unit_label}.csv"
    closure_path = ROOT / "authority" / f"ASSET_CLOSURE-bgk-unit-{unit_label}.json"
    credits_path = ROOT / "source" / "id-ID" / f"media-credits-bgk-unit-{unit_label}.md"
    asset_path = ROOT / "authority" / "assets" / args.local_name
    outputs = [metadata_path, rights_path, closure_path, credits_path, asset_path]
    refuse_unless_resume(outputs, args.resume)

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
    metadata_raw = fetch(
        COMMONS_API + "?" + urllib.parse.urlencode(params),
        accept="application/json",
    )
    payload = json.loads(metadata_raw.decode("utf-8"))
    if payload.get("error"):
        raise RuntimeError(f"Commons API error: {payload['error']}")
    pages = payload.get("query", {}).get("pages", [])
    if len(pages) != len(requested) or any(page.get("missing") for page in pages):
        raise RuntimeError("Commons closure did not resolve every requested BGK file")
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
    asset_raw = fetch(selected_url, accept=info.get("mime", "image/*"))
    with Image.open(io.BytesIO(asset_raw)) as image:
        image.verify()
    with Image.open(io.BytesIO(asset_raw)) as image:
        width, height = int(image.width), int(image.height)
    if width > 500:
        raise RuntimeError("Reader asset exceeds 500 pixels in width")
    if use_thumbnail:
        if width != int(info["thumbwidth"]):
            raise RuntimeError("Commons thumbnail width disagrees")
        # Commons currently reports Tangent_bundle.svg's 500px thumbnail as
        # 500x1204, while the exact returned PNG decodes as 500x1284.  Preserve
        # that witnessed height discrepancy in the rights row instead of
        # rejecting otherwise valid byte-identical response content.
    elif len(asset_raw) != int(info["size"]) or bytes_digest(asset_raw, "sha1") != info["sha1"]:
        raise RuntimeError("Original raster bytes disagree with Commons")

    licence = ext(info, "LicenseShortName") or ext(info, "UsageTerms")
    if not licence:
        raise RuntimeError("Commons supplied no image licence witness")
    license_template_lines = [
        line.strip()
        for line in content.splitlines()
        if re.search(r"\{\{\s*(?:self\b|cc[- _]|gfdl\b|pd(?:\b|[- _]))", line, flags=re.I)
    ]
    licence_discrepancy = (
        args.source_inline_license_label.casefold() != licence.casefold()
    )
    extmetadata_bytes = json.dumps(
        info.get("extmetadata", {}), ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    row = {
        "asset_id": f"br-bgk-u{unit_label}-media-001",
        "reader_order": 1,
        "reader_caption_id": args.caption,
        "reader_alt_id": args.alt,
        "resource_title": resource_title,
        "metadata_title": page["title"],
        "repository": "Wikimedia Commons",
        "description_url": info["descriptionurl"],
        "original_url": original_url,
        "selected_url": selected_url,
        "selected_form": (
            "official Commons 500px PNG thumbnail" if use_thumbnail else "original Commons raster"
        ),
        "local_path": asset_path.relative_to(ROOT).as_posix(),
        "local_bytes": len(asset_raw),
        "local_sha256": bytes_digest(asset_raw),
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
        "extmetadata_canonical_json_sha256": bytes_digest(extmetadata_bytes),
        "source_course_inline_license_label": args.source_inline_license_label,
        "commons_description_license_templates": " | ".join(license_template_lines),
        "license_discrepancy_present": licence_discrepancy,
        "license_discrepancy_note": (
            f"Wikiversity inline label {args.source_inline_license_label}; frozen Commons metadata offers {licence}. Reuse binds the Commons option."
            if licence_discrepancy
            else ""
        ),
        "source_course_project": COURSE_PROJECT,
        "source_course_title": COURSE_TITLE,
        "source_course_lecture_title": identity["lecture_title"],
        "source_course_creator": "Holger Brenner / Wikiversity course page",
        "source_course_license": "CC BY-SA 4.0",
        "description_pageid": page.get("pageid"),
        "description_revid": rev["revid"],
        "description_timestamp": rev["timestamp"],
        "description_mediawiki_sha1": rev["sha1"],
        "description_wikitext_bytes": len(content.encode("utf-8")),
        "description_wikitext_sha256": bytes_digest(content.encode("utf-8")),
        "html_animation_preserved": False,
    }
    rights_raw = csv_bytes(row)
    creator = row["artist"] or row["uploader"] or "lihat metadata sumber"
    licence_text = f"[{licence}]({row['license_url']})" if row["license_url"] else licence
    discrepancy_lines: list[str] = []
    if row["license_discrepancy_note"]:
        discrepancy_lines = [
            "",
            f"Catatan hak: label sebaris pada sumber BGK adalah `{args.source_inline_license_label}`, sedangkan revisi deskripsi Commons yang dibekukan memuat `{row['commons_description_license_templates']}` dan metadata Commons menawarkan {licence_text}. Edisi mengikat opsi Commons tersebut, bukan label sebaris yang berbeda.",
        ]
    credits_raw = (
        "\n".join(
            [
                f"# Kredit media BGK Unit {unit} {{#agc-bgk-media-credits-unit-{unit_label}}}",
                "",
                f"Sumber kursus: **{COURSE_TITLE}**, {identity['lecture_title']}. Satu posisi media substantif mempertahankan identitas Commons dan lisensi komponennya. Dua PDF resmi adalah saksi authority, bukan posisi media pembaca tambahan.",
                "",
                f"1. **{args.caption}** - [{row['metadata_title']}]({row['description_url']}); pencipta/atribusi: {creator}; lisensi/status hak: {licence_text}.",
                *discrepancy_lines,
                "",
            ]
        )
    ).encode("utf-8")
    pdf_records = [
        pdf_rights(by_key[title_key(title)], witness, manifest_path)
        for title, witness in zip(pdf_titles, witnesses, strict=True)
    ]
    closure = {
        "schema": "brenner-bgk-unit-media-closure-v1",
        "unit": unit,
        "source_identity": identity,
        "authority_manifest": {
            "path": manifest_path.relative_to(ROOT).as_posix(),
            "bytes": manifest_path.stat().st_size,
            "sha256": digest(manifest_path),
            "schema": manifest["schema"],
        },
        "authority_only_boundary": True,
        "reader_media_positions": 1,
        "animated_html_positions": 0,
        "unique_local_assets": 1,
        "metadata_file": metadata_path.relative_to(ROOT).as_posix(),
        "metadata_bytes": len(metadata_raw),
        "metadata_sha256": bytes_digest(metadata_raw),
        "metadata_preserves_raw_commons_response": True,
        "rights_file": rights_path.relative_to(ROOT).as_posix(),
        "rights_bytes": len(rights_raw),
        "rights_sha256": bytes_digest(rights_raw),
        "reader_credits_file": credits_path.relative_to(ROOT).as_posix(),
        "reader_credits_bytes": len(credits_raw),
        "reader_credits_sha256": bytes_digest(credits_raw),
        "official_pdf_witnesses_are_not_media_positions": True,
        "source_inline_license_discrepancy": {
            "present": licence_discrepancy,
            "source_inline_label": args.source_inline_license_label,
            "commons_license_short": row["license_short"],
            "commons_usage_terms": row["usage_terms"],
            "commons_description_license_templates": row[
                "commons_description_license_templates"
            ],
            "reuse_option_bound": row["license_short"] or row["usage_terms"],
            "note": row["license_discrepancy_note"],
        },
        "official_pdf_component_rights": sorted(
            pdf_records, key=lambda item: item["local_path"]
        ),
        "assets": [
            {
                "asset_id": row["asset_id"],
                "repository": row["repository"],
                "metadata_title": row["metadata_title"],
                "description_revid": row["description_revid"],
                "description_mediawiki_sha1": row["description_mediawiki_sha1"],
                "description_wikitext_sha256": row["description_wikitext_sha256"],
                "extmetadata_canonical_json_sha256": row[
                    "extmetadata_canonical_json_sha256"
                ],
                "local_path": row["local_path"],
                "local_bytes": row["local_bytes"],
                "local_sha256": row["local_sha256"],
                "license_short": row["license_short"],
                "usage_terms": row["usage_terms"],
                "license_url": row["license_url"],
                "html_animation_preserved": False,
            }
        ],
    }
    closure_raw = (json.dumps(closure, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

    # All source/rights checks above complete before the first output mutation.
    for path, raw in (
        (metadata_path, metadata_raw),
        (asset_path, asset_raw),
        (rights_path, rights_raw),
        (credits_path, credits_raw),
        (closure_path, closure_raw),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)

    print(
        json.dumps(
            {
                "status": "PASS",
                "course_title": COURSE_TITLE,
                "unit": unit,
                "media_positions": 1,
                "pdf_witnesses": 2,
                "license_discrepancy_present": licence_discrepancy,
                "rights_sha256": bytes_digest(rights_raw),
                "closure_sha256": bytes_digest(closure_raw),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
