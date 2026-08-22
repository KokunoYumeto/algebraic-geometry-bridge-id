#!/usr/bin/env python3
"""Freeze Unit 3 Commons media and emit component-level rights records."""

from __future__ import annotations

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
META = ROOT / "authority" / "commons-imageinfo-unit-03.json"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-03.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-03.json"
CREDITS = ROOT / "source" / "id-ID" / "media-credits-unit-03.md"
API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "Codex algebraic-geometry-bridge-id media freeze (at user's direction)"

MEDIA = (
    {
        "metadata_title": "File:Oscar Zariski.jpg",
        "caption": "Oscar Zariski (1899-1986)",
        "selected_url": "https://upload.wikimedia.org/wikipedia/commons/e/e5/Oscar_Zariski.jpg",
        "local_name": "Oscar_Zariski.jpg",
    },
    {
        "metadata_title": "File:Lineline.jpg",
        "caption": "Sebuah garis di bidang",
        "selected_url": "https://upload.wikimedia.org/wikipedia/commons/7/76/Lineline.jpg",
        "local_name": "Lineline.jpg",
    },
    {
        "metadata_title": "File:IntersectingPlanes.png",
        "caption": "Irisan dua bidang",
        "selected_url": "https://upload.wikimedia.org/wikipedia/commons/b/b3/IntersectingPlanes.png",
        "local_name": "IntersectingPlanes.png",
    },
    {
        "metadata_title": "File:Secretsharing-3-point.png",
        "caption": "Irisan tiga bidang",
        "selected_url": "https://upload.wikimedia.org/wikipedia/commons/c/cd/Secretsharing-3-point.png",
        "local_name": "Secretsharing-3-point.png",
    },
)


def fetch(url: str, data: bytes | None = None) -> bytes:
    for attempt in range(1, 7):
        try:
            request = Request(url, data=data, headers={"User-Agent": USER_AGENT})
            with urlopen(request, timeout=90) as response:
                result = response.read()
            time.sleep(0.5)
            return result
        except HTTPError as exc:
            if exc.code != 429 or attempt == 6:
                raise
            retry = exc.headers.get("Retry-After")
            time.sleep(min(20, int(retry) if retry and retry.isdigit() else 4 * attempt))
    raise RuntimeError("unreachable retry state")


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


def dimensions(path: Path) -> tuple[int, int]:
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        return int(image.width), int(image.height)


def main() -> int:
    ASSETS.mkdir(parents=True, exist_ok=True)
    params = {
        "action": "query",
        "prop": "imageinfo",
        "titles": "|".join(item["metadata_title"] for item in MEDIA),
        "iiprop": "url|sha1|size|mime|mediatype|timestamp|user|extmetadata",
        "format": "json",
        "formatversion": "2",
    }
    raw = fetch(API, urlencode(params).encode("utf-8"))
    META.write_bytes(raw)
    data = json.loads(raw)
    pages = {page["title"]: page for page in data["query"]["pages"]}
    rows = []
    for order, item in enumerate(MEDIA, start=1):
        page = pages[item["metadata_title"]]
        info = page["imageinfo"][0]
        local = ASSETS / item["local_name"]
        local.write_bytes(fetch(item["selected_url"]))
        width, height = dimensions(local)
        if local.stat().st_size != int(info["size"]) or digest(local, "sha1") != info["sha1"]:
            raise RuntimeError(f"Original validation failed: {local.name}")
        if width != int(info["width"]) or height != int(info["height"]):
            raise RuntimeError(f"Dimension validation failed: {local.name}")
        metadata = info.get("extmetadata", {})
        rows.append(
            {
                "asset_id": f"br-ak-u03-media-{order:03d}",
                "reader_order": order,
                "reader_caption_id": item["caption"],
                "resource_title": item["metadata_title"],
                "commons_metadata_title": item["metadata_title"],
                "description_url": info["descriptionurl"],
                "original_url": info["url"].split("?", 1)[0],
                "selected_url": item["selected_url"],
                "selected_form": "original",
                "local_path": f"authority/assets/{local.name}",
                "local_bytes": local.stat().st_size,
                "local_sha256": digest(local),
                "local_width": width,
                "local_height": height,
                "pdf_local_path": "",
                "pdf_local_bytes": "",
                "pdf_local_sha256": "",
                "pdf_companion_source_url": "",
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
        "# Kredit media Unit 3 {#agc-media-credits-unit-03}",
        "",
        "Kredit mengikuti urutan gambar dalam Kuliah 3. Setiap komponen mempertahankan lisensi sumbernya sendiri.",
        "",
    ]
    for row in rows:
        creator = row["artist"] or row["uploader"] or "tidak dinyatakan dalam metadata"
        licence = row["license_short"] or row["usage_terms"] or "lihat halaman sumber"
        if row["license_url"]:
            licence = f"[{licence}]({row['license_url']})"
        credit_lines.append(
            f"{row['reader_order']}. **{row['reader_caption_id']}** — "
            f"[{row['resource_title']}]({row['description_url']}); pencipta/atribusi: {creator}; lisensi: {licence}."
        )
    CREDITS.write_text("\n".join(credit_lines) + "\n", encoding="utf-8")

    closure = {
        "schema": "brenner-unit-media-closure-v1",
        "unit": 3,
        "reader_media_positions": len(rows),
        "unique_local_assets": len(rows),
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
                "pdf_local_path": "",
                "pdf_local_bytes": "",
                "pdf_local_sha256": "",
            }
            for row in rows
        ],
    }
    CLOSURE.write_text(json.dumps(closure, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
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
