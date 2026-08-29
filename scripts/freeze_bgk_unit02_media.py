#!/usr/bin/env python3
"""Freeze BGK Unit 2 reader media and component-rights evidence.

This deterministic, unit-scoped authority helper binds the three substantive
Commons media positions and the two already-frozen official PDF witnesses.  It
preserves the animated GIF for HTML and derives a reproducible first-frame PNG
for PDF output.  It never edits reader translation, controls, builds, backend,
Git state, or publication state.
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
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "Codex-BGK-authority-freezer/1.0 (independent edition preservation)"
COURSE_PROJECT = "German Wikiversity"
COURSE_TITLE = "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)"
COURSE_API = "https://de.wikiversity.org/w/api.php"
AUTHORITY_NAMESPACE = "authority/wikiversity-bgk"
MANIFEST_SCHEMA = "brenner-bgk-unit-authority-freeze-v1"
UNIT = 2
UNIT_LABEL = "02"
EXPECTED_MANIFEST_SHA256 = (
    "a348b56811fe98266feff9108a21a436a9b8f07a343321feab7d9fbb3b75e64d"
)

MEDIA_SPECS = (
    {
        "resource_name": "Hairy_ball_one_pole.jpg",
        "local_name": "bgk-hairy-ball-one-pole-500.jpg",
        "selection": "commons-500px-thumbnail",
        "caption_id": "Ilustrasi teorema bola berbulu",
        "alt_id": (
            "Bola berbulu dengan satu pusaran di kutub, sebagai ilustrasi bahwa "
            "medan vektor tangen kontinu pada bola harus mempunyai titik nol"
        ),
        "source_inline_creator": "RokerHRO",
        "source_inline_license": "CC-by-sa 3.0",
    },
    {
        "resource_name": "Inclusion-exclusion.svg",
        "local_name": "bgk-inclusion-exclusion-500.png",
        "selection": "commons-500px-png-thumbnail",
        "caption_id": "Diagram inklusi–eksklusi untuk tiga himpunan",
        "alt_id": (
            "Diagram tiga himpunan berbentuk lingkaran yang saling beririsan, "
            "dengan setiap daerah irisan dibedakan oleh warna"
        ),
        "source_inline_creator": "Burn~commonswiki",
        "source_inline_license": "CC-by-sa 3.0",
    },
    {
        "resource_name": "Fiddler_crab_mobius_strip.gif",
        "local_name": "bgk-fiddler-crab-mobius-strip.gif",
        "selection": "byte-exact-original-animation",
        "caption_id": "Animasi kepiting pada pita Möbius",
        "alt_id": (
            "Animasi seekor kepiting berjalan satu putaran mengelilingi pita "
            "Möbius dan kembali dengan orientasi terbalik"
        ),
        "source_inline_creator": "Hamishtodd1",
        "source_inline_license": "CC-by-sa 4.0",
        "pdf_companion_name": "bgk-fiddler-crab-mobius-strip-frame-001.png",
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


def normalized_license(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def authority_identity(manifest: dict[str, Any]) -> dict[str, Any]:
    source = manifest.get("source_identity", {})
    storage = manifest.get("storage_identity", {})
    expected = {
        "project": COURSE_PROJECT,
        "course_title": COURSE_TITLE,
        "source_api": COURSE_API,
    }
    if {key: source.get(key) for key in expected} != expected:
        raise RuntimeError("Refusing mismatched BGK course identity")
    if manifest.get("schema") != MANIFEST_SCHEMA or manifest.get("unit_number") != UNIT:
        raise RuntimeError("Authority manifest is not the admitted BGK Unit 2 schema")
    if storage.get("authority_namespace") != AUTHORITY_NAMESPACE:
        raise RuntimeError("Refusing non-BGK authority namespace")
    if storage.get("artifact_prefix") != "bgk":
        raise RuntimeError("Refusing authority without BGK artifact prefix")
    lecture = f"{COURSE_TITLE}/Vorlesung {UNIT}"
    worksheet = f"{COURSE_TITLE}/Arbeitsblatt {UNIT}"
    if source.get("lecture_title") != lecture or source.get("worksheet_title") != worksheet:
        raise RuntimeError("Authority source titles do not identify BGK Unit 2")
    return {
        **expected,
        "source_namespace_label": source.get("source_namespace_label"),
        "lecture_title": lecture,
        "worksheet_title": worksheet,
        "authority_namespace": AUTHORITY_NAMESPACE,
        "artifact_prefix": "bgk",
    }


def refuse_unless_resume(paths: list[Path], resume: bool) -> None:
    if len(paths) != len(set(paths)):
        raise RuntimeError("Output path collision")
    symlinks = [path for path in paths if path.is_symlink()]
    if symlinks:
        raise RuntimeError(f"Refusing symlink output target(s): {symlinks}")
    existing = [path for path in paths if path.exists()]
    if existing and not resume:
        rendered = ", ".join(path.relative_to(ROOT).as_posix() for path in existing)
        raise RuntimeError(f"Refusing to overwrite without --resume: {rendered}")
    nonfiles = [path for path in existing if not path.is_file()]
    if nonfiles:
        raise RuntimeError(f"Refusing non-file output target(s): {nonfiles}")


def decode_raster(value: bytes) -> tuple[int, int, int, str, dict[str, Any]]:
    with Image.open(io.BytesIO(value)) as image:
        image.verify()
    with Image.open(io.BytesIO(value)) as image:
        width = int(image.width)
        height = int(image.height)
        frames = int(getattr(image, "n_frames", 1))
        fmt = str(image.format or "")
        animation = {
            "loop": image.info.get("loop"),
            "first_frame_duration_ms": image.info.get("duration"),
        }
    return width, height, frames, fmt, animation


def first_frame_png(value: bytes) -> bytes:
    target = io.BytesIO()
    with Image.open(io.BytesIO(value)) as image:
        image.seek(0)
        rgba = image.convert("RGBA")
        rgba.save(target, format="PNG", optimize=False, compress_level=9)
    return target.getvalue()


def license_templates(content: str) -> list[str]:
    return [
        line.strip()
        for line in content.splitlines()
        if re.search(r"\{\{\s*(?:self\b|cc[- _]|gfdl\b|pd(?:\b|[- _]))", line, re.I)
    ]


def pdf_rights(
    page: dict[str, Any], witness: dict[str, Any], manifest_path: Path
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
        raise RuntimeError(f"Official PDF bytes disagree with manifest: {local}")
    if digest(local) != witness["local_sha256"]:
        raise RuntimeError(f"Official PDF SHA-256 disagrees with manifest: {local}")
    if int(info["size"]) != int(witness["source_bytes"]):
        raise RuntimeError(f"Commons PDF size drift: {page['title']}")
    if info["sha1"] != witness["mediawiki_sha1"]:
        raise RuntimeError(f"Commons PDF SHA-1 drift: {page['title']}")
    if local.stat().st_size != int(info["size"]) or digest(local, "sha1") != info["sha1"]:
        raise RuntimeError(f"Official PDF bytes disagree with Commons: {page['title']}")
    if info.get("mime") != "application/pdf" or not local.read_bytes().startswith(b"%PDF-"):
        raise RuntimeError(f"Invalid official PDF witness: {page['title']}")
    kind = str(witness.get("kind"))
    expected_pages = {"lecture": 9, "worksheet": 7}.get(kind)
    if expected_pages is None:
        raise RuntimeError(f"Unexpected PDF-witness kind: {kind!r}")
    reader = PdfReader(str(local))
    if len(reader.pages) != expected_pages:
        raise RuntimeError(
            f"Official {kind} PDF page count drift: {len(reader.pages)} != {expected_pages}"
        )
    last_page_text = reader.pages[-1].extract_text() or ""
    compact_text = re.sub(r"\s+", "", last_page_text).casefold()
    for expected_text in ("HolgerBrenner", "CC-by-sa3.0"):
        if expected_text.casefold() not in compact_text:
            raise RuntimeError(f"Missing embedded PDF rights witness {expected_text!r}: {local}")
    embedded_media_inventory: list[dict[str, str]] = []
    if kind == "lecture":
        embedded_media_inventory = [
            {
                "resource_name": "Hairy ball one pole.jpg",
                "creator_label": "RokerHRO",
                "license_label": "CC-by-sa 3.0",
            },
            {
                "resource_name": "Inclusion-exclusion.svg",
                "creator_label": "Burn commonswiki",
                "license_label": "CC-by-sa 3.0",
            },
            {
                "resource_name": "Fiddler crab mobius strip.gif",
                "creator_label": "Hamishtodd1",
                "license_label": "CC-by-sa 4.0",
            },
        ]
        for embedded in embedded_media_inventory:
            for expected_text in (
                embedded["resource_name"],
                embedded["creator_label"],
                embedded["license_label"],
            ):
                if re.sub(r"\s+", "", expected_text).casefold() not in compact_text:
                    raise RuntimeError(
                        f"Missing embedded lecture-PDF media-rights witness {expected_text!r}"
                    )
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
        "manifest_kind": kind,
        "pdf_pages": len(reader.pages),
        "embedded_rights_page": len(reader.pages),
        "embedded_rights_page_text_bytes": len(last_page_text.encode("utf-8")),
        "embedded_rights_page_text_sha256": bytes_digest(last_page_text.encode("utf-8")),
        "embedded_course_creator_label": "Holger Brenner alias Bocardodarapti",
        "embedded_course_text_license_label": "CC-by-sa 3.0",
        "embedded_media_inventory": embedded_media_inventory,
        "commons_vs_embedded_course_license_discrepancy": (
            normalized_license(ext(info, "LicenseShortName") or ext(info, "UsageTerms"))
            != normalized_license("CC-by-sa 3.0")
        ),
        "reuse_scope_note": (
            "The PDF is an authority witness, not a reader-media position. Its embedded CC BY-SA 3.0 notice and the current Commons description's CC BY-SA 4.0 metadata are both preserved; semantic course reuse remains bound to the separately frozen current course authority and component ledger."
        ),
    }


def csv_bytes(rows: list[dict[str, Any]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--resume",
        action="store_true",
        help="explicitly replace the same Unit 2 outputs after complete validation",
    )
    args = parser.parse_args()

    manifest_path = (
        ROOT
        / "authority"
        / "wikiversity-bgk"
        / "unit-02"
        / "UNIT_AUTHORITY_MANIFEST.json"
    )
    if not manifest_path.is_file() or manifest_path.is_symlink():
        raise RuntimeError(f"Missing/non-regular BGK manifest: {manifest_path}")
    if digest(manifest_path) != EXPECTED_MANIFEST_SHA256:
        raise RuntimeError("BGK Unit 2 authority-manifest SHA-256 does not match admission")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    identity = authority_identity(manifest)

    image_names = set(manifest.get("images", {}).get("lecture", [])) | set(
        manifest.get("images", {}).get("worksheet", [])
    )
    substantive = sorted(name for name in image_names if not name.casefold().endswith(".pdf"))
    expected_substantive = sorted(str(spec["resource_name"]) for spec in MEDIA_SPECS)
    if substantive != expected_substantive:
        raise RuntimeError(f"Unexpected BGK Unit 2 media closure: {substantive}")

    witnesses = manifest.get("official_pdf_witnesses", [])
    if len(witnesses) != 2 or {row.get("kind") for row in witnesses} != {
        "lecture",
        "worksheet",
    }:
        raise RuntimeError("Authority manifest lacks exactly both official PDF witnesses")

    metadata_path = ROOT / "authority" / "commons-imageinfo-bgk-unit-02.json"
    rights_path = ROOT / "authority" / "RIGHTS-bgk-unit-02.csv"
    closure_path = ROOT / "authority" / "ASSET_CLOSURE-bgk-unit-02.json"
    credits_path = ROOT / "source" / "id-ID" / "media-credits-bgk-unit-02.md"
    asset_paths = [ROOT / "authority" / "assets" / str(spec["local_name"]) for spec in MEDIA_SPECS]
    companion_paths = [
        ROOT / "authority" / "assets" / str(spec["pdf_companion_name"])
        for spec in MEDIA_SPECS
        if spec.get("pdf_companion_name")
    ]
    outputs = [metadata_path, rights_path, closure_path, credits_path, *asset_paths, *companion_paths]
    refuse_unless_resume(outputs, args.resume)

    media_titles = [commons_file_title(str(spec["resource_name"])) for spec in MEDIA_SPECS]
    pdf_titles = [commons_file_title(str(row["source_file_title"])) for row in witnesses]
    requested = [*media_titles, *pdf_titles]
    if len({title_key(value) for value in requested}) != 5:
        raise RuntimeError("The three media and two PDFs are not five distinct Commons files")
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
    api_url = COMMONS_API + "?" + urllib.parse.urlencode(params)
    api_raw = fetch(api_url, accept="application/json")
    payload = json.loads(api_raw.decode("utf-8"))
    if payload.get("error"):
        raise RuntimeError(f"Commons API error: {payload['error']}")
    pages = payload.get("query", {}).get("pages", [])
    if len(pages) != 5 or any(page.get("missing") for page in pages):
        raise RuntimeError("Commons closure did not resolve all five Unit 2 files")
    by_key = {title_key(page["title"]): page for page in pages}
    if set(by_key) != {title_key(value) for value in requested}:
        raise RuntimeError("Commons title closure drift")

    rows: list[dict[str, Any]] = []
    metadata_records: list[dict[str, Any]] = []
    asset_bytes: dict[Path, bytes] = {}
    for order, (spec, title) in enumerate(zip(MEDIA_SPECS, media_titles, strict=True), 1):
        page = by_key[title_key(title)]
        infos = page.get("imageinfo", [])
        if len(infos) != 1:
            raise RuntimeError(f"No unique imageinfo for {title}")
        info = infos[0]
        rev, content = revision(page)
        original_url = info["url"].split("?", 1)[0]
        selection = str(spec["selection"])
        if selection == "byte-exact-original-animation":
            selected_url = original_url
            selected_raw = fetch(selected_url, accept="image/gif")
            if len(selected_raw) != int(info["size"]) or bytes_digest(selected_raw, "sha1") != info["sha1"]:
                raise RuntimeError(f"Original GIF bytes disagree with Commons: {title}")
            selected_form = "byte-exact Commons original GIF"
        else:
            selected_url = info.get("thumburl")
            if not selected_url:
                raise RuntimeError(f"Commons supplied no 500px thumbnail: {title}")
            selected_raw = fetch(selected_url, accept="image/*")
            selected_form = (
                "official Commons 500px JPEG thumbnail"
                if selection == "commons-500px-thumbnail"
                else "official Commons 500px PNG rendering of SVG"
            )

        width, height, frames, image_format, animation = decode_raster(selected_raw)
        if selection != "byte-exact-original-animation" and width != 500:
            raise RuntimeError(f"Bounded thumbnail is not 500px wide: {title}: {width}")
        if selection == "byte-exact-original-animation" and frames <= 1:
            raise RuntimeError("The admitted animated GIF unexpectedly has one frame")
        if selection == "commons-500px-thumbnail" and image_format.upper() not in {"JPEG", "JPG"}:
            raise RuntimeError(f"Unexpected hairy-ball thumbnail format: {image_format}")
        if selection == "commons-500px-png-thumbnail" and image_format.upper() != "PNG":
            raise RuntimeError(f"Unexpected SVG rendering format: {image_format}")
        if selection == "byte-exact-original-animation" and image_format.upper() != "GIF":
            raise RuntimeError(f"Unexpected animation format: {image_format}")

        asset_path = ROOT / "authority" / "assets" / str(spec["local_name"])
        asset_bytes[asset_path] = selected_raw
        companion_path: Path | None = None
        companion_raw = b""
        if spec.get("pdf_companion_name"):
            companion_path = ROOT / "authority" / "assets" / str(spec["pdf_companion_name"])
            companion_raw = first_frame_png(selected_raw)
            c_width, c_height, c_frames, c_format, _ = decode_raster(companion_raw)
            if (c_width, c_height, c_frames, c_format.upper()) != (width, height, 1, "PNG"):
                raise RuntimeError("Deterministic GIF first-frame companion failed validation")
            if companion_raw != first_frame_png(selected_raw):
                raise RuntimeError("GIF first-frame derivation is not byte-deterministic")
            asset_bytes[companion_path] = companion_raw

        extmetadata = info.get("extmetadata", {})
        extmetadata_bytes = json.dumps(
            extmetadata, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        templates = license_templates(content)
        license_short = ext(info, "LicenseShortName")
        usage_terms = ext(info, "UsageTerms")
        bound_license = license_short or usage_terms
        if not bound_license:
            raise RuntimeError(f"Commons supplied no license witness: {title}")
        discrepancy = normalized_license(str(spec["source_inline_license"])) != normalized_license(
            bound_license
        )
        local_name = str(spec["local_name"])
        row = {
            "asset_id": f"br-bgk-u02-media-{order:03d}",
            "reader_order": order,
            "reader_caption_id": spec["caption_id"],
            "reader_alt_id": spec["alt_id"],
            "resource_title": title,
            "metadata_title": page["title"],
            "repository": "Wikimedia Commons",
            "description_url": info.get("descriptionurl", ""),
            "original_url": original_url,
            "selected_url": selected_url,
            "selected_form": selected_form,
            "local_path": asset_path.relative_to(ROOT).as_posix(),
            "local_bytes": len(selected_raw),
            "local_sha256": bytes_digest(selected_raw),
            "local_width": width,
            "local_height": height,
            "reported_thumb_width": int(info["thumbwidth"]) if "thumbwidth" in info else "",
            "reported_thumb_height": int(info["thumbheight"]) if "thumbheight" in info else "",
            "thumbnail_dimension_discrepancy": (
                f"decoded={width}x{height};reported={int(info['thumbwidth'])}x{int(info['thumbheight'])}"
                if "thumbwidth" in info
                and (width, height) != (int(info["thumbwidth"]), int(info["thumbheight"]))
                else ""
            ),
            "frame_count": frames,
            "animation_loop": "" if animation["loop"] is None else animation["loop"],
            "first_frame_duration_ms": (
                "" if animation["first_frame_duration_ms"] is None else animation["first_frame_duration_ms"]
            ),
            "pdf_local_path": companion_path.relative_to(ROOT).as_posix() if companion_path else "",
            "pdf_local_bytes": len(companion_raw) if companion_path else "",
            "pdf_local_sha256": bytes_digest(companion_raw) if companion_path else "",
            "pdf_companion_source": "locally derived deterministic first frame" if companion_path else "",
            "original_bytes": int(info["size"]),
            "original_sha1": info["sha1"],
            "original_width": int(info["width"]),
            "original_height": int(info["height"]),
            "mime": info["mime"],
            "media_type": info.get("mediatype", ""),
            "source_timestamp": info.get("timestamp", ""),
            "uploader": info.get("user", ""),
            "artist": ext(info, "Artist"),
            "credit": ext(info, "Credit"),
            "license_short": license_short,
            "usage_terms": usage_terms,
            "license_url": ext(info, "LicenseUrl"),
            "attribution_required": ext(info, "AttributionRequired"),
            "extmetadata_canonical_json_sha256": bytes_digest(extmetadata_bytes),
            "source_course_inline_creator": spec["source_inline_creator"],
            "source_course_inline_license_label": spec["source_inline_license"],
            "commons_description_license_templates": " | ".join(templates),
            "license_discrepancy_present": discrepancy,
            "license_discrepancy_note": (
                f"Label sebaris Wikiversity adalah {spec['source_inline_license']}; metadata Commons yang dibekukan menawarkan {bound_license}. Penggunaan ulang edisi ini mengikat opsi Commons tersebut."
                if discrepancy
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
            "html_animation_preserved": bool(companion_path),
        }
        rows.append(row)
        metadata_records.append(
            {
                "resource_title": title,
                "metadata_title": page["title"],
                "pageid": page.get("pageid"),
                "description_revision": {
                    "revid": rev["revid"],
                    "timestamp": rev["timestamp"],
                    "mediawiki_sha1": rev["sha1"],
                    "wikitext_bytes": len(content.encode("utf-8")),
                    "wikitext_sha256": bytes_digest(content.encode("utf-8")),
                    "wikitext": content,
                },
                "imageinfo": {
                    "description_url": info.get("descriptionurl", ""),
                    "original_url": original_url,
                    "original_bytes": int(info["size"]),
                    "original_sha1": info["sha1"],
                    "original_width": int(info["width"]),
                    "original_height": int(info["height"]),
                    "mime": info["mime"],
                    "media_type": info.get("mediatype", ""),
                    "timestamp": info.get("timestamp", ""),
                    "uploader": info.get("user", ""),
                    "artist": row["artist"],
                    "credit": row["credit"],
                    "license_short": license_short,
                    "usage_terms": usage_terms,
                    "license_url": row["license_url"],
                    "attribution_required": row["attribution_required"],
                    "extmetadata": extmetadata,
                    "extmetadata_canonical_json_sha256": bytes_digest(extmetadata_bytes),
                },
                "selection": {
                    "selected_url": selected_url,
                    "selected_form": selected_form,
                    "local_path": row["local_path"],
                    "local_bytes": row["local_bytes"],
                    "local_sha256": row["local_sha256"],
                    "local_width": width,
                    "local_height": height,
                    "frame_count": frames,
                    "pdf_local_path": row["pdf_local_path"],
                    "pdf_local_bytes": row["pdf_local_bytes"],
                    "pdf_local_sha256": row["pdf_local_sha256"],
                },
            }
        )

    pdf_records = [
        pdf_rights(by_key[title_key(title)], witness, manifest_path)
        for title, witness in zip(pdf_titles, witnesses, strict=True)
    ]
    metadata = {
        "schema": "brenner-bgk-unit-commons-media-metadata-v1",
        "unit": UNIT,
        "source_api": COMMONS_API,
        "request_parameters": params,
        "source_api_response_bytes": len(api_raw),
        "source_api_response_sha256": bytes_digest(api_raw),
        "records": metadata_records,
    }
    metadata_raw = (json.dumps(metadata, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    rights_raw = csv_bytes(rows)

    credit_lines = [
        "# Kredit media BGK Unit 2 {#agc-bgk-media-credits-unit-02}",
        "",
        f"Sumber kursus: **{COURSE_TITLE}**, {identity['lecture_title']}. Tiga posisi media substantif mempertahankan identitas Commons dan lisensi komponennya. Dua PDF resmi adalah saksi authority, bukan posisi media pembaca tambahan.",
        "",
    ]
    for row in rows:
        commons_artist = str(row["artist"] or "")
        inline_creator = str(row["source_course_inline_creator"] or "")
        if commons_artist.casefold() in {"", "unknown", "unknown unknown"} and inline_creator:
            creator = (
                f"{inline_creator} (disebut pada sumber kursus; metadata Commons "
                f"mencatat pencipta sebagai '{commons_artist or 'tidak diketahui'}' "
                f"dan pengunggah sebagai {row['uploader']})"
            )
        else:
            creator = commons_artist or str(row["uploader"]) or inline_creator
        license_name = row["license_short"] or row["usage_terms"] or "lihat halaman sumber"
        license_text = (
            f"[{license_name}]({row['license_url']})" if row["license_url"] else str(license_name)
        )
        animation_note = (
            " Animasi asli dipertahankan untuk HTML; bingkai pertama deterministik digunakan untuk PDF."
            if row["html_animation_preserved"]
            else ""
        )
        credit_lines.extend(
            [
                f"{row['reader_order']}. **{row['reader_caption_id']}** — [{row['metadata_title']}]({row['description_url']}); pencipta/atribusi: {creator}; lisensi/status hak: {license_text}.{animation_note}",
                f"   Teks alternatif: {row['reader_alt_id']}.",
            ]
        )
        if row["license_discrepancy_note"]:
            credit_lines.append(f"   Catatan hak: {row['license_discrepancy_note']}")
        credit_lines.append("")
    credits_raw = "\n".join(credit_lines).encode("utf-8")

    asset_manifest = []
    for path, value in sorted(asset_bytes.items(), key=lambda item: item[0].name.casefold()):
        asset_manifest.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": len(value),
                "sha256": bytes_digest(value),
                "derived": path in companion_paths,
            }
        )
    closure = {
        "schema": "brenner-bgk-unit-media-closure-v1",
        "unit": UNIT,
        "source_identity": identity,
        "authority_manifest": {
            "path": manifest_path.relative_to(ROOT).as_posix(),
            "bytes": manifest_path.stat().st_size,
            "sha256": digest(manifest_path),
            "schema": manifest["schema"],
        },
        "authority_only_boundary": True,
        "reader_media_positions": len(rows),
        "animated_html_positions": sum(bool(row["html_animation_preserved"]) for row in rows),
        "unique_primary_local_assets": len(rows),
        "unique_pdf_companion_assets": len(companion_paths),
        "unique_local_assets": len(asset_manifest),
        "metadata_file": metadata_path.relative_to(ROOT).as_posix(),
        "metadata_bytes": len(metadata_raw),
        "metadata_sha256": bytes_digest(metadata_raw),
        "metadata_preserves_commons_description_wikitext": True,
        "rights_file": rights_path.relative_to(ROOT).as_posix(),
        "rights_bytes": len(rights_raw),
        "rights_sha256": bytes_digest(rights_raw),
        "reader_credits_file": credits_path.relative_to(ROOT).as_posix(),
        "reader_credits_bytes": len(credits_raw),
        "reader_credits_sha256": bytes_digest(credits_raw),
        "official_pdf_witnesses_are_not_media_positions": True,
        "official_pdf_component_rights": sorted(pdf_records, key=lambda item: item["local_path"]),
        "license_discrepancies": [
            {
                "asset_id": row["asset_id"],
                "present": row["license_discrepancy_present"],
                "source_inline_label": row["source_course_inline_license_label"],
                "commons_license_short": row["license_short"],
                "commons_usage_terms": row["usage_terms"],
                "commons_description_license_templates": row[
                    "commons_description_license_templates"
                ],
                "reuse_option_bound": row["license_short"] or row["usage_terms"],
                "note": row["license_discrepancy_note"],
            }
            for row in rows
        ],
        "assets": [
            {
                "asset_id": row["asset_id"],
                "reader_order": row["reader_order"],
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
                "local_width": row["local_width"],
                "local_height": row["local_height"],
                "frame_count": row["frame_count"],
                "pdf_local_path": row["pdf_local_path"],
                "pdf_local_bytes": row["pdf_local_bytes"],
                "pdf_local_sha256": row["pdf_local_sha256"],
                "license_short": row["license_short"],
                "usage_terms": row["usage_terms"],
                "license_url": row["license_url"],
                "html_animation_preserved": row["html_animation_preserved"],
                "reader_alt_id": row["reader_alt_id"],
            }
            for row in rows
        ],
        "asset_manifest": asset_manifest,
    }
    closure_raw = (json.dumps(closure, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

    # Every source, identity, rights, format, dimension, and derivation check is
    # complete before the first output mutation.
    writes = [
        (metadata_path, metadata_raw),
        (rights_path, rights_raw),
        (credits_path, credits_raw),
        *sorted(asset_bytes.items(), key=lambda item: item[0].as_posix().casefold()),
        (closure_path, closure_raw),
    ]
    for path, value in writes:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(value)

    print(
        json.dumps(
            {
                "status": "PASS",
                "unit": UNIT,
                "reader_media_positions": len(rows),
                "animated_html_positions": 1,
                "local_assets": len(asset_manifest),
                "pdf_witnesses": len(pdf_records),
                "metadata_sha256": bytes_digest(metadata_raw),
                "rights_sha256": bytes_digest(rights_raw),
                "credits_sha256": bytes_digest(credits_raw),
                "closure_sha256": bytes_digest(closure_raw),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
