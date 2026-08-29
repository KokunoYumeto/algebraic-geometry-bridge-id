#!/usr/bin/env python3
"""Freeze BGK component rights for a unit with no substantive reader media.

The script validates the isolated BGK authority manifest, binds both official
PDF witnesses to current Commons description metadata, records their embedded
rights notices, and emits an explicit zero-reader-media ledger and Indonesian
credits note.  ``--resume`` reuses the frozen Commons response so the receipt
replays deterministically rather than silently following later metadata edits.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import urllib.parse
from typing import Any

from pypdf import PdfReader

from freeze_bgk_single_image_unit_media import (
    COMMONS_API,
    COURSE_TITLE,
    ROOT,
    commons_file_title,
    course_identity,
    digest,
    fetch,
    pdf_rights,
    refuse_unless_resume,
    title_key,
)


EMPTY_RIGHTS_FIELDS = [
    "asset_id",
    "reader_order",
    "reader_caption_id",
    "reader_alt_id",
    "resource_title",
    "metadata_title",
    "repository",
    "description_url",
    "original_url",
    "selected_url",
    "selected_form",
    "local_path",
    "local_bytes",
    "local_sha256",
    "local_width",
    "local_height",
    "reported_thumb_width",
    "reported_thumb_height",
    "thumbnail_dimension_discrepancy",
    "frame_count",
    "animation_loop",
    "first_frame_duration_ms",
    "pdf_local_path",
    "pdf_local_bytes",
    "pdf_local_sha256",
    "pdf_companion_source",
    "original_bytes",
    "original_sha1",
    "original_width",
    "original_height",
    "mime",
    "media_type",
    "source_timestamp",
    "uploader",
    "artist",
    "credit",
    "license_short",
    "usage_terms",
    "license_url",
    "attribution_required",
    "extmetadata_canonical_json_sha256",
    "source_course_inline_creator",
    "source_course_inline_license_label",
    "commons_description_license_templates",
    "license_discrepancy_present",
    "license_discrepancy_note",
    "source_course_project",
    "source_course_title",
    "source_course_lecture_title",
    "source_course_creator",
    "source_course_license",
    "description_pageid",
    "description_revid",
    "description_timestamp",
    "description_mediawiki_sha1",
    "description_wikitext_bytes",
    "description_wikitext_sha256",
    "html_animation_preserved",
]


def normalized_license(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def empty_rights_bytes() -> bytes:
    stream = io.StringIO(newline="")
    csv.DictWriter(stream, fieldnames=EMPTY_RIGHTS_FIELDS, lineterminator="\n").writeheader()
    return stream.getvalue().encode("utf-8")


def embedded_pdf_rights(record: dict[str, Any]) -> dict[str, Any]:
    path = ROOT / record["local_path"]
    reader = PdfReader(str(path))
    if not reader.pages:
        raise RuntimeError(f"Official PDF has no pages: {path}")
    last_text = reader.pages[-1].extract_text() or ""
    compact = re.sub(r"\s+", "", last_text).casefold()
    for expected in ("HolgerBrenner", "Bocardodarapti", "CC-by-sa3.0"):
        if expected.casefold() not in compact:
            raise RuntimeError(f"Missing embedded rights witness {expected!r}: {path}")
    commons_license = str(record.get("license_short") or record.get("usage_terms") or "")
    if not commons_license:
        raise RuntimeError(f"Commons supplied no PDF license metadata: {path}")
    return {
        **record,
        "pdf_pages": len(reader.pages),
        "embedded_rights_page": len(reader.pages),
        "embedded_rights_page_text_bytes": len(last_text.encode("utf-8")),
        "embedded_rights_page_text_sha256": hashlib.sha256(last_text.encode("utf-8")).hexdigest(),
        "embedded_course_creator_label": "Holger Brenner alias Bocardodarapti",
        "embedded_course_text_license_label": "CC-by-sa 3.0",
        "commons_vs_embedded_course_license_discrepancy": (
            normalized_license(commons_license) != normalized_license("CC-by-sa 3.0")
        ),
        "reuse_scope_note": (
            "The PDF is an authority witness, not a reader-media position. Its embedded rights notice and current Commons description metadata are both preserved; semantic reuse remains bound to the separately frozen current course authority."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--unit", required=True, type=int)
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument(
        "--resume",
        action="store_true",
        help="replace the same outputs while reusing the already-frozen Commons response",
    )
    args = parser.parse_args()
    if not 1 <= args.unit <= 30:
        raise SystemExit("--unit must be between 1 and 30")
    expected_manifest_sha = args.manifest_sha256.casefold()
    if not re.fullmatch(r"[0-9a-f]{64}", expected_manifest_sha):
        raise SystemExit("--manifest-sha256 must be 64 lowercase or uppercase hex digits")
    unit_label = f"{args.unit:02d}"
    unit_dir = ROOT / "authority" / "wikiversity-bgk" / f"unit-{unit_label}"
    manifest_path = unit_dir / "UNIT_AUTHORITY_MANIFEST.json"
    if not manifest_path.is_file() or manifest_path.is_symlink():
        raise RuntimeError(f"Missing/non-regular BGK authority manifest: {manifest_path}")
    if digest(manifest_path) != expected_manifest_sha:
        raise RuntimeError("BGK authority-manifest SHA-256 does not match the admitted boundary")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    identity = course_identity(manifest, args.unit)

    image_names = set(manifest.get("images", {}).get("lecture", [])) | set(
        manifest.get("images", {}).get("worksheet", [])
    )
    substantive = sorted(name for name in image_names if not name.casefold().endswith(".pdf"))
    if substantive:
        raise RuntimeError(f"BGK Unit {args.unit} has substantive reader media: {substantive}")
    witnesses = manifest.get("official_pdf_witnesses", [])
    if len(witnesses) != 2 or {row.get("kind") for row in witnesses} != {
        "lecture",
        "worksheet",
    }:
        raise RuntimeError("BGK authority lacks exactly both official PDF witnesses")
    pdf_titles = [commons_file_title(row["source_file_title"]) for row in witnesses]
    if len({title_key(value) for value in pdf_titles}) != 2:
        raise RuntimeError("Official PDF titles are not distinct")

    metadata_path = ROOT / "authority" / f"commons-imageinfo-bgk-unit-{unit_label}.json"
    rights_path = ROOT / "authority" / f"RIGHTS-bgk-unit-{unit_label}.csv"
    closure_path = ROOT / "authority" / f"ASSET_CLOSURE-bgk-unit-{unit_label}.json"
    credits_path = ROOT / "source" / "id-ID" / f"media-credits-bgk-unit-{unit_label}.md"
    refuse_unless_resume(
        [metadata_path, rights_path, closure_path, credits_path], args.resume
    )
    params = {
        "action": "query",
        "format": "json",
        "formatversion": 2,
        "prop": "imageinfo|revisions",
        "iiprop": "url|size|mime|sha1|timestamp|user|mediatype|extmetadata",
        "rvprop": "ids|timestamp|sha1|content",
        "rvslots": "main",
        "titles": "|".join(pdf_titles),
    }
    if args.resume and metadata_path.is_file():
        metadata_raw = metadata_path.read_bytes()
    else:
        metadata_raw = fetch(
            COMMONS_API + "?" + urllib.parse.urlencode(params),
            accept="application/json",
        )
    payload = json.loads(metadata_raw.decode("utf-8"))
    if payload.get("error"):
        raise RuntimeError(f"Commons API error: {payload['error']}")
    pages = payload.get("query", {}).get("pages", [])
    if len(pages) != 2 or any(page.get("missing") for page in pages):
        raise RuntimeError("Commons did not resolve both official PDFs")
    by_key = {title_key(page["title"]): page for page in pages}
    if set(by_key) != {title_key(title) for title in pdf_titles}:
        raise RuntimeError("Commons PDF title closure drift")
    pdf_records = [
        embedded_pdf_rights(
            pdf_rights(by_key[title_key(title)], witness, manifest_path)
        )
        for title, witness in zip(pdf_titles, witnesses, strict=True)
    ]

    rights_raw = empty_rights_bytes()
    credits_raw = (
        "\n".join(
            [
                f"# Kredit media BGK Unit {args.unit} {{#agc-bgk-media-credits-unit-{unit_label}}}",
                "",
                f"Sumber kursus: **{COURSE_TITLE}**, {identity['lecture_title']} dan {identity['worksheet_title']}.",
                "",
                "Unit ini tidak memiliki posisi media substantif untuk pembaca, sehingga tidak ada keterangan gambar atau teks alternatif komponen yang perlu ditambahkan. Dua berkas PDF resmi yang muncul pada permukaan parse dibekukan hanya sebagai saksi authority; identitas, atribusi, lisensi, revisi, ukuran, dan hash keduanya tercatat dalam penutupan aset, bukan sebagai media pembaca.",
                "",
            ]
        )
    ).encode("utf-8")
    closure = {
        "schema": "brenner-bgk-unit-media-closure-v1",
        "unit": args.unit,
        "source_identity": identity,
        "authority_manifest": {
            "path": manifest_path.relative_to(ROOT).as_posix(),
            "bytes": manifest_path.stat().st_size,
            "sha256": digest(manifest_path),
            "schema": manifest["schema"],
        },
        "authority_only_boundary": True,
        "reader_media_positions": 0,
        "animated_html_positions": 0,
        "unique_primary_local_assets": 0,
        "unique_pdf_companion_assets": 0,
        "unique_local_assets": 0,
        "reader_caption_and_alt_status": "not applicable: zero substantive reader-media positions",
        "metadata_file": metadata_path.relative_to(ROOT).as_posix(),
        "metadata_bytes": len(metadata_raw),
        "metadata_sha256": hashlib.sha256(metadata_raw).hexdigest(),
        "metadata_preserves_raw_commons_response": True,
        "rights_file": rights_path.relative_to(ROOT).as_posix(),
        "rights_bytes": len(rights_raw),
        "rights_sha256": hashlib.sha256(rights_raw).hexdigest(),
        "reader_credits_file": credits_path.relative_to(ROOT).as_posix(),
        "reader_credits_bytes": len(credits_raw),
        "reader_credits_sha256": hashlib.sha256(credits_raw).hexdigest(),
        "reader_credits_required": True,
        "official_pdf_witnesses_are_not_media_positions": True,
        "official_pdf_component_rights": sorted(
            pdf_records, key=lambda item: item["local_path"]
        ),
        "assets": [],
    }
    closure_raw = (json.dumps(closure, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

    # All authority, rights, PDF, and zero-media checks complete before writes.
    for path, raw in (
        (metadata_path, metadata_raw),
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
                "unit": args.unit,
                "media_positions": 0,
                "pdf_witnesses": len(pdf_records),
                "metadata_sha256": digest(metadata_path),
                "rights_sha256": digest(rights_path),
                "credits_sha256": digest(credits_path),
                "closure_sha256": digest(closure_path),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
