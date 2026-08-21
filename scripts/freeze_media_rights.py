#!/usr/bin/env python3
"""Validate Unit 1 media and emit deterministic component-rights receipts."""

from __future__ import annotations

import csv
import hashlib
import html
import json
from pathlib import Path
import re

from PIL import Image


LANE = Path(__file__).resolve().parents[1]
META = LANE / "authority" / "commons-imageinfo-lecture-01.json"
ASSETS = LANE / "authority" / "assets"
RIGHTS = LANE / "authority" / "RIGHTS.csv"
CLOSURE = LANE / "authority" / "ASSET_CLOSURE.json"
CREDITS = LANE / "source" / "id-ID" / "media-credits.md"

# Lecture order is part of the reader contract.  The resource title is the
# Parsoid/Wikiversity identity; metadata_title selects its frozen Commons row.
MEDIA = (
    ("File:Linear_function.svg", "File:Linear function.svg", "Linear_function-250.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Linear_function.svg/250px-Linear_function.svg.png", "thumbnail"),
    ("File:Polynomialdeg4.png", "File:Polynomialdeg4.png", "Polynomialdeg4.png", "https://upload.wikimedia.org/wikipedia/commons/a/a1/Polynomialdeg4.png", "original"),
    ("File:RationalDegree2byXedi.gif", "File:RationalDegree2byXedi.gif", "RationalDegree2byXedi.gif", "https://upload.wikimedia.org/wikipedia/commons/0/09/RationalDegree2byXedi.gif", "original"),
    ("File:Disk_1.svg", "File:Disk 1.svg", "Disk_1-250.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Disk_1.svg/250px-Disk_1.svg.png", "thumbnail"),
    ("File:Ellipse.svg", "File:Ellipse.svg", "Ellipse.svg", "https://upload.wikimedia.org/wikipedia/commons/2/2e/Ellipse.svg", "original"),
    ("File:Cusp.png", "File:Cusp.png", "Cusp-250.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Cusp.png/250px-Cusp.png", "thumbnail"),
    ("File:Elliptic_curve_simple.svg", "File:Elliptic curve simple.svg", "Elliptic_curve_simple-250.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Elliptic_curve_simple.svg/250px-Elliptic_curve_simple.svg.png", "thumbnail"),
    ("File:Tschirnhausen_cubic.svg", "File:Tschirnhausen cubic.svg", "Tschirnhausen_cubic-250.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Tschirnhausen_cubic.svg/250px-Tschirnhausen_cubic.svg.png", "thumbnail"),
    ("File:Eudoxus.png", "File:Eudoxus.png", "Kampyle_Eudoxus-250.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Kampyle_Eudoxus.png/250px-Kampyle_Eudoxus.png", "thumbnail"),
    ("File:Conchoid_of_Pascal.png", "File:Conchoid of Pascal.png", "Conchoid_of_Pascal.png", "https://upload.wikimedia.org/wikipedia/commons/e/e9/Conchoid_of_Pascal.png", "original"),
    ("File:Bifolium.png", "File:Bifolium.png", "Bifolium.png", "https://upload.wikimedia.org/wikipedia/commons/2/2d/Bifolium.png", "original"),
    ("File:Limacon.png", "File:Limacon.png", "Limacon.png", "https://upload.wikimedia.org/wikipedia/commons/0/0e/Limacon.png", "original"),
    ("File:Quadrifolium.svg", "File:Quadrifolium.svg", "Quadrifolium-250.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Quadrifolium.svg/250px-Quadrifolium.svg.png", "thumbnail"),
    ("File:Lemniscate_of_Bernoulli.svg", "File:Lemniscate of Bernoulli.svg", "Lemniscate_of_Bernoulli-250.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Lemniscate_of_Bernoulli.svg/250px-Lemniscate_of_Bernoulli.svg.png", "thumbnail"),
    ("File:Cicloide.svg", "File:Cicloide.svg", "Cicloide-250.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Cicloide.svg/250px-Cicloide.svg.png", "thumbnail"),
    ("File:Logarithmic_spiral.png", "File:Logarithmic spiral.png", "Logarithmic_spiral-250.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Logarithmic_spiral.png/250px-Logarithmic_spiral.png", "thumbnail"),
    ("File:Sin.svg", "File:Sin.svg", "Sin-250.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Sin.svg/250px-Sin.svg.png", "thumbnail"),
    ("File:Quadratic_Koch.png", "File:Quadratic Koch.png", "Quadratic_Koch.png", "https://upload.wikimedia.org/wikipedia/commons/1/1b/Quadratic_Koch.png", "original"),
    ("File:Rectangular_hyperbola.svg", "File:Rectangular hyperbola.svg", "Rectangular_hyperbola-250.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Rectangular_hyperbola.svg/250px-Rectangular_hyperbola.svg.png", "thumbnail"),
    ("File:Newtonbig.gif", "File:Newtonbig.gif", "Newtonbig.gif", "https://upload.wikimedia.org/wikipedia/commons/0/0e/Newtonbig.gif", "original"),
    ("File:GodfreyKneller-IsaacNewton-1689.jpg", "File:GodfreyKneller-IsaacNewton-1689.jpg", "GodfreyKneller-IsaacNewton-1689.jpg", "https://upload.wikimedia.org/wikipedia/commons/3/39/GodfreyKneller-IsaacNewton-1689.jpg", "original"),
    ("File:ECexamples01.png", "File:ECexamples01.png", "ECexamples01-330.png", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/ECexamples01.png/330px-ECexamples01.png", "thumbnail"),
    ("File:Carl_Friedrich_Gauss.jpg", "File:Carl Friedrich Gauss.jpg", "Carl_Friedrich_Gauss.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/9b/Carl_Friedrich_Gauss.jpg", "original"),
)

CAPTIONS = (
    "Grafik fungsi linear",
    "Grafik polinom berderajat empat",
    "Grafik fungsi rasional",
    "Lingkaran satuan",
    "Elips",
    "Kurva dengan kuspa",
    "Contoh kurva eliptik",
    "Kubik Tschirnhausen",
    "Kampyle Eudoxus",
    "Konkoid Pascal",
    "Bifolium",
    "Limaçon",
    "Quadrifolium",
    "Lemniskat Bernoulli",
    "Sikloid",
    "Spiral logaritmik",
    "Grafik sinus",
    "Kurva Koch kuadratik",
    "Hiperbola siku-siku",
    "Kurva-kurva kubik yang dikaji Newton",
    "Isaac Newton",
    "Contoh-contoh kurva eliptik real",
    "Carl Friedrich Gauss",
)

PDF_COMPANIONS = {
    "RationalDegree2byXedi.gif": "RationalDegree2byXedi-frame-1.png",
    "Ellipse.svg": "Ellipse-250.png",
    "Newtonbig.gif": "Newtonbig-frame-1.png",
}

PDF_COMPANION_URLS = {
    "Ellipse.svg": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Ellipse.svg/250px-Ellipse.svg.png",
}


def digest(path: Path, algorithm: str = "sha256") -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def plain(value: object) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(html.unescape(text).split())


def ext(meta: dict, key: str) -> str:
    return plain(meta.get(key, {}).get("value", ""))


def image_size(path: Path, original_width: int, original_height: int) -> tuple[int, int]:
    if path.suffix.casefold() == ".svg":
        # The selected SVG is the byte-exact Commons original, whose dimensions
        # are already frozen in imageinfo.
        return original_width, original_height
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        return int(image.width), int(image.height)


def make_pdf_companion(source: Path, target: Path) -> None:
    if source.suffix.casefold() == ".svg":
        if not target.is_file() or target.is_symlink():
            raise RuntimeError(f"missing frozen SVG thumbnail companion: {target}")
        with Image.open(target) as image:
            image.verify()
        return
    with Image.open(source) as image:
        image.seek(0)
        image.convert("RGBA").save(
            target,
            format="PNG",
            optimize=False,
            compress_level=9,
        )


def main() -> int:
    data = json.loads(META.read_text(encoding="utf-8"))
    pages = {page["title"]: page for page in data["pages"]}
    if len(MEDIA) != 23 or len(CAPTIONS) != 23 or len({row[2] for row in MEDIA}) != 23:
        raise RuntimeError("media selection must contain 23 unique local files")

    rows: list[dict[str, object]] = []
    total_bytes = 0
    for order, (resource, metadata_title, local_name, selected_url, form) in enumerate(MEDIA, 1):
        caption = CAPTIONS[order - 1]
        page = pages.get(metadata_title)
        if page is None:
            raise RuntimeError(f"missing frozen metadata row: {metadata_title}")
        info = page["imageinfo"][0]
        path = ASSETS / local_name
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"missing/nonregular selected asset: {path}")
        if form == "original":
            if path.stat().st_size != int(info["size"]):
                raise RuntimeError(f"original size mismatch: {local_name}")
            if digest(path, "sha1") != info["sha1"]:
                raise RuntimeError(f"original SHA-1 mismatch: {local_name}")
        local_width, local_height = image_size(
            path, int(info["width"]), int(info["height"])
        )
        pdf_name = PDF_COMPANIONS.get(local_name, "")
        pdf_path = ASSETS / pdf_name if pdf_name else None
        if pdf_path is not None:
            make_pdf_companion(path, pdf_path)
        metadata = info.get("extmetadata", {})
        total_bytes += path.stat().st_size
        rows.append(
            {
                "asset_id": f"br-ak-media-{order:03d}",
                "reader_order": order,
                "reader_caption_id": caption,
                "resource_title": resource,
                "commons_metadata_title": metadata_title,
                "description_url": info["descriptionurl"],
                "original_url": info["url"].split("?", 1)[0],
                "selected_url": selected_url,
                "selected_form": form,
                "local_path": f"authority/assets/{local_name}",
                "local_bytes": path.stat().st_size,
                "local_sha256": digest(path),
                "local_width": local_width,
                "local_height": local_height,
                "pdf_local_path": f"authority/assets/{pdf_name}" if pdf_name else "",
                "pdf_local_bytes": pdf_path.stat().st_size if pdf_path else "",
                "pdf_local_sha256": digest(pdf_path) if pdf_path else "",
                "pdf_companion_source_url": PDF_COMPANION_URLS.get(local_name, "locally derived first frame" if pdf_name else ""),
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

    fieldnames = list(rows[0])
    with RIGHTS.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    credit_lines = [
        "# Kredit media {#agc-media-credits}",
        "",
        "Kredit berikut mengikuti urutan kemunculan gambar dalam Kuliah 1. ",
        "Setiap komponen mempertahankan lisensi sumbernya sendiri; lisensi teks ",
        "kuliah tidak menggantikan lisensi komponen media.",
        "",
        "\\begingroup\\small",
        "",
    ]
    for row in rows:
        creator = row["artist"] or row["uploader"] or "tidak dinyatakan dalam metadata"
        license_name = row["license_short"] or row["usage_terms"] or "lihat halaman sumber"
        if row["license_url"]:
            license_text = f"[{license_name}]({row['license_url']})"
        else:
            license_text = str(license_name)
        credit_lines.extend(
            [
                f"{row['reader_order']}. **{row['reader_caption_id']}** — "
                f"[{row['commons_metadata_title']}]({row['description_url']}); "
                f"pencipta/atribusi: {creator}; lisensi: {license_text}.",
                "",
            ]
        )
    credit_lines.extend(["\\endgroup", ""])
    CREDITS.write_text("\n".join(credit_lines), encoding="utf-8", newline="\n")

    asset_manifest = [
        {
            "path": row["local_path"],
            "bytes": row["local_bytes"],
            "sha256": row["local_sha256"],
        }
        for row in rows
    ]
    asset_manifest.extend(
        {
            "path": row["pdf_local_path"],
            "bytes": row["pdf_local_bytes"],
            "sha256": row["pdf_local_sha256"],
        }
        for row in rows
        if row["pdf_local_path"]
    )
    asset_manifest.sort(key=lambda row: str(row["path"]).casefold())

    closure = {
        "schema": "brenner-unit-media-closure-v1",
        "language": "id-ID",
        "authority_metadata_file": "authority/commons-imageinfo-lecture-01.json",
        "authority_metadata_sha256": digest(META),
        "authority_page_records": len(data["pages"]),
        "reader_media_positions": len(rows),
        "unique_local_assets": len(asset_manifest),
        "local_asset_bytes": sum(int(row["bytes"]) for row in asset_manifest),
        "rights_file": "authority/RIGHTS.csv",
        "rights_sha256": digest(RIGHTS),
        "reader_credits_file": "source/id-ID/media-credits.md",
        "reader_credits_sha256": digest(CREDITS),
        "asset_manifest": asset_manifest,
    }
    CLOSURE.write_text(
        json.dumps(closure, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"assets": len(rows), "bytes": total_bytes, "rights_sha256": digest(RIGHTS)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
