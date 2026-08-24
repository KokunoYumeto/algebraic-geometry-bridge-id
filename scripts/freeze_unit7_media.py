#!/usr/bin/env python3
"""Freeze Unit 7 Commons media and emit component-level rights records."""

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
META = ROOT / "authority" / "commons-imageinfo-unit-07.json"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-07.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-07.json"
CREDITS = ROOT / "source" / "id-ID" / "media-credits-unit-07.md"
API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "Codex algebraic-geometry-bridge-id media freeze (at user's direction)"

# Order is the exact order of the nine substantive image positions in the
# frozen Lecture 7 expanded TeX. The two PDF icons returned by the parse API
# are official build witnesses, not reader-image positions.
MEDIA = (
    {
        "resource_title": "File:DoubleCone.png",
        "metadata_title": "File:DoubleCone.png",
        "caption": "Kerucut standar",
        "source_creator": "Lars H. Rohwedder (RokerHRO)",
        "source_license": "domain publik",
        "local_name": "DoubleCone.png",
        "pdf_name": "",
    },
    {
        "resource_title": "File:Conic sections.svg",
        "metadata_title": "File:Conic sections.svg",
        "caption": "Irisan-irisan kerucut standar dengan bidang-bidang afin",
        "source_creator": "Anuskafm",
        "source_license": "CC BY-SA 3.0",
        "local_name": "Conic_sections.svg",
        "pdf_name": "Conic_sections-500.png",
    },
    {
        "resource_title": "File:Hauptachsentransformation1.png",
        "metadata_title": "File:Hauptachsentransformation1.png",
        "caption": "Tahap pertama transformasi sumbu utama suatu kuadrik",
        "source_creator": "Rdb",
        "source_license": "domain publik",
        "local_name": "Hauptachsentransformation1.png",
        "pdf_name": "",
    },
    {
        "resource_title": "File:Hauptachsentransformation2.png",
        "metadata_title": "File:Hauptachsentransformation2.png",
        "caption": "Tahap kedua transformasi sumbu utama suatu kuadrik",
        "source_creator": "Rdb",
        "source_license": "domain publik",
        "local_name": "Hauptachsentransformation2.png",
        "pdf_name": "",
    },
    {
        "resource_title": "File:Hauptachsentransformation3.png",
        "metadata_title": "File:Hauptachsentransformation3.png",
        "caption": "Tahap ketiga transformasi sumbu utama suatu kuadrik",
        "source_creator": "Rdb",
        "source_license": "domain publik",
        "local_name": "Hauptachsentransformation3.png",
        "pdf_name": "",
    },
    {
        "resource_title": "File:Johannes Kepler 1610.jpg",
        "metadata_title": "File:Portrait Confused With Johannes Kepler 1610.jpg",
        "caption": "Potret seorang pria tak dikenal, dahulu disalahidentifikasi sebagai Johannes Kepler",
        "source_creator": "pelukis tidak diketahui; sumber kuliah menyebutnya tidak diketahui (1610)",
        "source_license": "domain publik",
        "local_name": "Portrait_Confused_With_Johannes_Kepler_1610.jpg",
        "pdf_name": "",
    },
    {
        "resource_title": "File:Elliptic orbit.gif",
        "metadata_title": "File:Elliptic orbit.gif",
        "caption": "Orbit eliptik",
        "source_creator": "Brandir",
        "source_license": "CC BY-SA 2.5",
        "local_name": "Elliptic_orbit.gif",
        "pdf_name": "Elliptic_orbit-frame-1.png",
        "selected_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Elliptic_orbit.gif/250px-Elliptic_orbit.gif",
    },
    {
        "resource_title": "File:Parabolic orbit.gif",
        "metadata_title": "File:Parabolic orbit.gif",
        "caption": "Orbit parabola",
        "source_creator": "Brandir",
        "source_license": "CC BY-SA 2.5",
        "local_name": "Parabolic_orbit.gif",
        "pdf_name": "Parabolic_orbit-frame-1.png",
        "selected_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Parabolic_orbit.gif/250px-Parabolic_orbit.gif",
    },
    {
        "resource_title": "File:Hyperbolic orbit.gif",
        "metadata_title": "File:Hyperbolic orbit.gif",
        "caption": "Orbit hiperbola",
        "source_creator": "Brandir",
        "source_license": "CC BY-SA 2.5",
        "local_name": "Hyperbolic_orbit.gif",
        "pdf_name": "Hyperbolic_orbit-frame-1.png",
        "selected_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Hyperbolic_orbit.gif/250px-Hyperbolic_orbit.gif",
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


def title_key(title: str) -> str:
    return " ".join(title.replace("_", " ").split()).casefold()


def dimensions(path: Path, fallback_width: int, fallback_height: int) -> tuple[int, int]:
    if path.suffix.casefold() == ".svg":
        return fallback_width, fallback_height
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
    pages = {title_key(page["title"]): page for page in data["query"]["pages"]}

    rows: list[dict[str, object]] = []
    for order, item in enumerate(MEDIA, start=1):
        page = pages.get(title_key(item["metadata_title"]))
        if page is None or "missing" in page or not page.get("imageinfo"):
            raise RuntimeError(f"Commons metadata did not resolve: {item['metadata_title']}")
        info = page["imageinfo"][0]
        local = ASSETS / item["local_name"]
        # Commons explicitly asks automated clients to use its standard
        # thumbnail sizes. The animated source GIFs therefore use official
        # 250-pixel Commons thumbnails; original metadata remains frozen in
        # the same row for provenance.
        selected_url = item.get("selected_url", info["url"])
        selected_form = "commons_250px_thumbnail" if item.get("selected_url") else "original"
        if not local.is_file():
            local.write_bytes(fetch(selected_url))
        width, height = dimensions(local, int(info["width"]), int(info["height"]))
        if selected_form == "original":
            if local.stat().st_size != int(info["size"]) or digest(local, "sha1") != info["sha1"]:
                raise RuntimeError(f"Original validation failed: {local.name}")
            if width != int(info["width"]) or height != int(info["height"]):
                raise RuntimeError(f"Dimension validation failed: {local.name}")
        elif width != 250 or frame_count(local) < 2:
            raise RuntimeError(f"Animated thumbnail validation failed: {local.name}")

        pdf_local = ASSETS / item["pdf_name"] if item["pdf_name"] else None
        pdf_source = ""
        if pdf_local:
            if local.suffix.casefold() == ".svg":
                pdf_source = info.get("thumburl", "")
                if not pdf_source:
                    raise RuntimeError(f"No Commons PNG companion URL for {local.name}")
                if not pdf_local.is_file():
                    pdf_local.write_bytes(fetch(pdf_source))
            elif local.suffix.casefold() == ".gif":
                make_first_frame(local, pdf_local)
                pdf_source = "locally derived first frame from byte-exact Commons GIF"
            else:
                raise RuntimeError(f"Unexpected companion source: {local.name}")
            dimensions(pdf_local, 0, 0)

        metadata = info.get("extmetadata", {})
        rows.append(
            {
                "asset_id": f"br-ak-u07-media-{order:03d}",
                "reader_order": order,
                "reader_caption_id": item["caption"],
                "resource_title": item["resource_title"],
                "commons_metadata_title": page["title"],
                "description_url": info["descriptionurl"],
                "original_url": info["url"].split("?", 1)[0],
                "selected_url": selected_url,
                "selected_form": selected_form,
                "local_path": f"authority/assets/{local.name}",
                "local_bytes": local.stat().st_size,
                "local_sha256": digest(local),
                "local_width": width,
                "local_height": height,
                "pdf_local_path": f"authority/assets/{pdf_local.name}" if pdf_local else "",
                "pdf_local_bytes": pdf_local.stat().st_size if pdf_local else "",
                "pdf_local_sha256": digest(pdf_local) if pdf_local else "",
                "pdf_companion_source_url": pdf_source,
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
                "source_course_creator": item["source_creator"],
                "source_course_license": item["source_license"],
                "html_animation_preserved": frame_count(local) > 1,
            }
        )

    with RIGHTS.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    credit_lines = [
        "# Kredit media Unit 7 {#agc-media-credits-unit-07}",
        "",
        "Kredit mengikuti sembilan posisi gambar dalam Kuliah 7. Setiap komponen mempertahankan status hak atau lisensi sumbernya sendiri. Tiga GIF orbit tetap beranimasi dalam pembaca HTML; PDF memakai bingkai pertamanya yang diturunkan secara lokal.",
        "",
    ]
    for row, item in zip(rows, MEDIA, strict=True):
        creator = row["artist"] or item["source_creator"] or row["uploader"]
        licence = row["license_short"] or row["usage_terms"] or item["source_license"]
        if row["license_url"]:
            licence_text = f"[{licence}]({row['license_url']})"
        else:
            licence_text = str(licence)
        credit_lines.append(
            f"{row['reader_order']}. **{row['reader_caption_id']}** - "
            f"[{row['commons_metadata_title']}]({row['description_url']}); "
            f"pencipta/atribusi: {creator}; status hak/lisensi: {licence_text}."
        )
    CREDITS.write_bytes(("\n".join(credit_lines) + "\n").encode("utf-8"))

    closure = {
        "schema": "brenner-unit-media-closure-v1",
        "unit": 7,
        "reader_media_positions": len(rows),
        "animated_html_positions": sum(1 for row in rows if row["html_animation_preserved"]),
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
                "rights_sha256": closure["rights_sha256"],
                "closure_sha256": digest(CLOSURE),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
