#!/usr/bin/env python3
"""Freeze BGK Unit 4 media using an official Commons redirect fallback.

The generic one-image freezer's direct 500 px upload URL is intermittently
throttled.  For Unit 4's sole substantive image, Commons' official
``Special:Redirect/file`` surface resolves to the same generated thumbnail.
All authority, rights, dimension, and hash checks remain those of the generic
freezer.
"""

from __future__ import annotations

import sys
import urllib.parse
import contextlib
import csv
import hashlib
import io
import json

import freeze_bgk_single_image_unit_media as core


UNIT = "4"
RESOURCE = "Triticum_spelta_-_shock_(aka).jpg"
REDIRECT = (
    "https://commons.wikimedia.org/wiki/Special:Redirect/file/"
    + urllib.parse.quote(RESOURCE, safe="()_-.")
    + "?width=500"
)
ORIGINAL_FETCH = core.fetch


def fetch(url: str, *, accept: str = "*/*", attempts: int = 8) -> bytes:
    decoded = urllib.parse.unquote(url)
    if "/thumb/" in decoded and RESOURCE in decoded:
        return ORIGINAL_FETCH(REDIRECT, accept=accept, attempts=attempts)
    return ORIGINAL_FETCH(url, accept=accept, attempts=attempts)


def normalized_license(value: str) -> str:
    return "".join(character for character in value.casefold() if character.isalnum())


def correct_label_only_variation() -> dict[str, object]:
    """Do not misclassify typography as a component-license discrepancy."""
    rights_path = core.ROOT / "authority" / "RIGHTS-bgk-unit-04.csv"
    closure_path = core.ROOT / "authority" / "ASSET_CLOSURE-bgk-unit-04.json"
    credits_path = core.ROOT / "source" / "id-ID" / "media-credits-bgk-unit-04.md"
    with rights_path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
    if len(rows) != 1:
        raise RuntimeError("BGK Unit 4 must have exactly one component-rights row")
    row = rows[0]
    inline = row["source_course_inline_license_label"]
    commons = row["license_short"] or row["usage_terms"]
    if normalized_license(inline) != normalized_license(commons):
        raise RuntimeError(
            "BGK Unit 4 source and Commons licenses are not semantically identical"
        )
    row["license_discrepancy_present"] = "False"
    row["license_discrepancy_note"] = ""
    rights_raw = core.csv_bytes(row)
    creator = row["artist"] or row["uploader"] or "lihat metadata sumber"
    licence_text = (
        f"[{commons}]({row['license_url']})" if row["license_url"] else commons
    )
    credits_raw = (
        "\n".join(
            [
                "# Kredit media BGK Unit 4 {#agc-bgk-media-credits-unit-04}",
                "",
                f"Sumber kursus: **{row['source_course_title']}**, {row['source_course_lecture_title']}. Satu posisi media substantif mempertahankan identitas Commons dan lisensi komponennya. Dua PDF resmi adalah saksi authority, bukan posisi media pembaca tambahan.",
                "",
                f"1. **{row['reader_caption_id']}** - [{row['metadata_title']}]({row['description_url']}); pencipta/atribusi: {creator}; lisensi/status hak: {licence_text}.",
                "",
            ]
        )
    ).encode("utf-8")
    closure = json.loads(closure_path.read_text(encoding="utf-8"))
    closure["rights_bytes"] = len(rights_raw)
    closure["rights_sha256"] = hashlib.sha256(rights_raw).hexdigest()
    closure["reader_credits_bytes"] = len(credits_raw)
    closure["reader_credits_sha256"] = hashlib.sha256(credits_raw).hexdigest()
    discrepancy = closure["source_inline_license_discrepancy"]
    discrepancy["present"] = False
    discrepancy["note"] = ""
    discrepancy["label_format_variation_only"] = True
    discrepancy["semantic_equivalence_checked"] = True
    closure_raw = (json.dumps(closure, ensure_ascii=False, indent=2) + "\n").encode(
        "utf-8"
    )
    rights_path.write_bytes(rights_raw)
    credits_path.write_bytes(credits_raw)
    closure_path.write_bytes(closure_raw)
    return {
        "status": "PASS",
        "unit": 4,
        "media_positions": 1,
        "pdf_witnesses": 2,
        "license_discrepancy_present": False,
        "label_format_variation_only": True,
        "rights_sha256": hashlib.sha256(rights_raw).hexdigest(),
        "credits_sha256": hashlib.sha256(credits_raw).hexdigest(),
        "closure_sha256": hashlib.sha256(closure_raw).hexdigest(),
    }


def main() -> int:
    try:
        position = sys.argv.index("--unit")
        requested_unit = sys.argv[position + 1]
    except (ValueError, IndexError) as error:
        raise SystemExit("This bounded wrapper requires --unit 4") from error
    if requested_unit != UNIT:
        raise SystemExit("This bounded wrapper may freeze only BGK Unit 4")
    core.fetch = fetch
    with contextlib.redirect_stdout(io.StringIO()):
        result = core.main()
    print(json.dumps(correct_label_only_variation(), ensure_ascii=False))
    return result


if __name__ == "__main__":
    raise SystemExit(main())
