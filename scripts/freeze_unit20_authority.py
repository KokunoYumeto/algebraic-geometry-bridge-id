#!/usr/bin/env python3
"""Freeze the bounded official Unit 20 Wikiversity/Commons authority closure."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import freeze_unit12_authority as base


ROOT = Path(__file__).resolve().parents[1]
UNIT = 20

# Reuse the already exercised bounded capture machinery, but redirect every
# mutable/output and source-identity global before any request is made.
base.UNIT = UNIT
base.OUT = ROOT / "authority" / "wikiversity" / "unit-20"
base.ARTIFACTS = ROOT / "authority" / "artifacts"
base.ASSETS = ROOT / "authority" / "assets"
base.RIGHTS = ROOT / "authority" / "RIGHTS-unit-20.csv"
base.CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-20.json"
base.COMMONS_META = ROOT / "authority" / "commons-imageinfo-unit-20.json"
base.LECTURE_TITLE = f"{base.COURSE}/Vorlesung {UNIT}"
base.WORKSHEET_TITLE = f"{base.COURSE}/Arbeitsblatt {UNIT}"
base.USER_AGENT = "O016-unit20-authority-freeze/1.0 (bounded educational preservation)"
MEDIA_CREDITS = ROOT / "source" / "id-ID" / "media-credits-unit-20.md"
WHITNEY_URL = "https://upload.wikimedia.org/wikipedia/commons/7/79/Whitney_unbrella.png"
WHITNEY_BYTES = 35829
WHITNEY_SHA1 = "c2c21c52fde3d3c5c3939541dac74385e67a80c7"
WHITNEY_CAPTION = "Payung Whitney"
WHITNEY_ALT = "Permukaan abu-abu kebiruan berbentuk payung Whitney yang berpotongan sendiri di ruang tiga dimensi"


def ensure_whitney_original() -> None:
    """Prefer the tiny exact Commons original over a derived thumbnail."""
    data = base.fetch(WHITNEY_URL)
    if len(data) != WHITNEY_BYTES or base.digest_bytes(data, "sha1") != WHITNEY_SHA1:
        raise RuntimeError("Whitney original byte identity mismatch")
    path = base.ASSETS / "Whitney_unbrella.png"
    if path.exists() and path.read_bytes() != data:
        raise RuntimeError(f"refusing to overwrite a different asset: {path}")
    base.write_bytes(path, data)


def normalize_unit_asset_ids(asset_records: list[dict], pdf_records: list[dict]) -> None:
    """Replace the inherited Unit-12 ID prefix after the reusable capture."""
    original_path = base.ASSETS / "Whitney_unbrella.png"
    original_sha256 = base.digest(original_path)
    extra_fields = [
        "reader_caption_id",
        "reader_alt_id",
        "source_course_inline_license_label",
        "commons_description_license_templates",
        "license_discrepancy_note",
    ]
    with base.RIGHTS.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
        fieldnames = list(rows[0]) if rows else []
    if not rows:
        raise RuntimeError("Unit 20 substantive media closure unexpectedly empty")
    fieldnames.extend(name for name in extra_fields if name not in fieldnames)
    for row in rows:
        row["asset_id"] = row["asset_id"].replace("br-ak-u12-", "br-ak-u20-")
        row["selected_url"] = WHITNEY_URL
        row["selected_form"] = "exact Commons original"
        row["local_path"] = original_path.relative_to(ROOT).as_posix()
        row["local_bytes"] = str(WHITNEY_BYTES)
        row["local_sha256"] = original_sha256
        row["local_width"] = "267"
        row["local_height"] = "209"
        row["frame_count"] = "1"
        row["reader_caption_id"] = WHITNEY_CAPTION
        row["reader_alt_id"] = WHITNEY_ALT
        row["source_course_inline_license_label"] = "CC-BY-SA-2.5"
        row["commons_description_license_templates"] = "{{Self|GFDL|Cc-by-sa-3.0-migrated|Cc-by-2.5}}"
        row["license_discrepancy_note"] = (
            "Wikiversity and the lecture-PDF appendix label the image CC-BY-SA-2.5; "
            "frozen Commons metadata does not offer that combination and instead offers "
            "GFDL 1.2+, CC BY-SA 3.0, and CC BY 2.5. Reuse binds CC BY 2.5."
        )
    with base.RIGHTS.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    closure = json.loads(base.CLOSURE.read_text(encoding="utf-8"))
    closure["unit"] = UNIT
    closure["rights_bytes"] = base.RIGHTS.stat().st_size
    closure["rights_sha256"] = base.digest(base.RIGHTS)
    closure["reader_credits_file"] = MEDIA_CREDITS.relative_to(ROOT).as_posix()
    closure["reader_credits_bytes"] = MEDIA_CREDITS.stat().st_size
    closure["reader_credits_sha256"] = base.digest(MEDIA_CREDITS)
    closure["frozen_accessibility"] = {"caption_id": WHITNEY_CAPTION, "alt_id": WHITNEY_ALT}
    closure["source_inline_license_discrepancy"] = {
        "source_inline_label": "CC-BY-SA-2.5",
        "commons_license_short": "CC BY 2.5",
        "commons_description_license_templates": "{{Self|GFDL|Cc-by-sa-3.0-migrated|Cc-by-2.5}}",
        "reuse_option_bound": "CC BY 2.5",
        "note": "The source's CC-BY-SA-2.5 combination is not offered by frozen Commons metadata.",
    }
    closure["official_pdf_component_rights"] = []
    for record in pdf_records:
        item = dict(record)
        item["internal_pdf_boilerplate_label"] = "CC BY-SA 3.0"
        item["governing_current_course_and_commons_license"] = "CC BY-SA 4.0"
        item["license_discrepancy_note"] = (
            "The PDF's internal boilerplate retains CC BY-SA 3.0; the current course "
            "license surface and Commons description bind this component as CC BY-SA 4.0."
        )
        closure["official_pdf_component_rights"].append(item)
    for record in closure["assets"]:
        record["asset_id"] = record["asset_id"].replace("br-ak-u12-", "br-ak-u20-")
        record["selected_url"] = WHITNEY_URL
        record["selected_form"] = "exact Commons original"
        record["local_path"] = original_path.relative_to(ROOT).as_posix()
        record["local_bytes"] = WHITNEY_BYTES
        record["local_sha256"] = original_sha256
        record["local_width"] = 267
        record["local_height"] = 209
        record["frame_count"] = 1
    base.write_json(base.CLOSURE, closure)
    for record in asset_records:
        record["asset_id"] = record["asset_id"].replace("br-ak-u12-", "br-ak-u20-")
        record["selected_url"] = WHITNEY_URL
        record["selected_form"] = "exact Commons original"
        record["local_path"] = original_path.relative_to(ROOT).as_posix()
        record["local_bytes"] = WHITNEY_BYTES
        record["local_sha256"] = original_sha256
        record["local_width"] = 267
        record["local_height"] = 209
        record["frame_count"] = 1


def main() -> int:
    base.OUT.mkdir(parents=True, exist_ok=True)
    base.ARTIFACTS.mkdir(parents=True, exist_ok=True)
    base.ASSETS.mkdir(parents=True, exist_ok=True)
    if not MEDIA_CREDITS.is_file():
        raise RuntimeError(f"missing frozen Unit 20 media credits: {MEDIA_CREDITS}")
    ensure_whitney_original()

    lecture, lecture_parsed = base.entry_surface(base.LECTURE_TITLE, "lecture-20")
    worksheet, worksheet_parsed = base.entry_surface(base.WORKSHEET_TITLE, "worksheet-20")
    lecture_latex, lecture_tex = base.latex_surface(base.LECTURE_TITLE + "/latex", "lecture-20")
    worksheet_latex, worksheet_tex = base.latex_surface(base.WORKSHEET_TITLE + "/latex", "worksheet-20")
    lecture_closure = base.transclusion_closure(lecture_parsed, "lecture-20")
    worksheet_closure = base.transclusion_closure(worksheet_parsed, "worksheet-20")
    solutions = base.solution_map(worksheet, worksheet_parsed)
    solution_dependencies = []
    for exercise, title in (
        (1, "Quadratwurzel/2/Irrational/Fakt/Beweis"),
        (4, "Kommutative Ringtheorie/Z ist normal/Wurzeln aus ganzen Zahlen sind irrational/Fakt/Beweis"),
    ):
        stem = f"solution-ex{exercise:02d}-transcluded-proof"
        entry, parsed = base.entry_surface(title, stem)
        solution_dependencies.append(
            {
                "solution_exercise": exercise,
                "dependency_kind": "transcluded proof body",
                "entry": entry,
                "transclusion_closure": base.transclusion_closure(parsed, stem),
            }
        )
    official_pdfs, assets = base.shared_media(lecture_parsed, worksheet_parsed)
    normalize_unit_asset_ids(assets, official_pdfs)
    recheck = base.final_identity_recheck(lecture["revid"], worksheet["revid"])

    manifest = {
        "schema": "brenner-unit-authority-freeze-v2",
        "frozen_utc": datetime.now(timezone.utc).isoformat(),
        "unit_number": UNIT,
        "source_api": base.WIKI_API,
        "source_course_license": "CC BY-SA 4.0",
        "lecture": lecture,
        "worksheet": worksheet,
        "lecture_latex_page": lecture_latex,
        "worksheet_latex_page": worksheet_latex,
        "derived_expanded_tex": [lecture_tex, worksheet_tex],
        "lecture_transclusion_closure": lecture_closure,
        "worksheet_transclusion_closure": worksheet_closure,
        "solutions": solutions,
        "solution_transclusion_dependencies": solution_dependencies,
        "images": {
            "lecture": lecture_parsed.get("images", []),
            "worksheet": worksheet_parsed.get("images", []),
            "substantive_assets": assets,
        },
        "official_pdf_witnesses": official_pdfs,
        "entry_revision_recheck": recheck,
    }
    manifest["files"] = [
        {"file": path.name, "bytes": path.stat().st_size, "sha256": base.digest(path)}
        for path in sorted(base.OUT.iterdir(), key=lambda item: item.name)
        if path.is_file() and path.name != "UNIT_AUTHORITY_MANIFEST.json"
    ]
    manifest_path = base.OUT / "UNIT_AUTHORITY_MANIFEST.json"
    base.write_json(manifest_path, manifest)

    replay = json.loads(manifest_path.read_text(encoding="utf-8"))
    for record in replay["files"]:
        path = base.OUT / record["file"]
        if path.stat().st_size != record["bytes"] or base.digest(path) != record["sha256"]:
            raise RuntimeError(f"manifest replay failed: {path}")
    parsed_exercises = [
        item for item in worksheet_parsed["templates"]
        if item.get("ns") != 10 and item["title"].endswith("/Aufgabe")
    ]
    if replay["solutions"]["exercise_count"] != len(parsed_exercises):
        raise RuntimeError("exercise topology replay failed")
    result = {
        "result": "PASS",
        "unit": UNIT,
        "lecture_pageid": lecture["pageid"],
        "lecture_revid": lecture["revid"],
        "worksheet_pageid": worksheet["pageid"],
        "worksheet_revid": worksheet["revid"],
        "lecture_transclusions": lecture_closure["captured_page_count"],
        "worksheet_transclusions": worksheet_closure["captured_page_count"],
        "exercises": solutions["exercise_count"],
        "public_solutions": solutions["solution_count"],
        "media_positions": len(assets),
        "official_pdf_pages": [item["page_count"] for item in official_pdfs],
        "manifest_bytes": manifest_path.stat().st_size,
        "manifest_sha256": base.digest(manifest_path),
        "rights_bytes": base.RIGHTS.stat().st_size,
        "rights_sha256": base.digest(base.RIGHTS),
        "closure_bytes": base.CLOSURE.stat().st_size,
        "closure_sha256": base.digest(base.CLOSURE),
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
