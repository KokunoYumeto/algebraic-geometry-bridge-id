#!/usr/bin/env python3
"""Freeze the bounded official Unit 22 Wikiversity/Commons authority closure."""

from __future__ import annotations

import csv
import json
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

import freeze_unit12_authority as base
import freeze_unit21_authority as strong
from freeze_single_image_unit_media import commons_file_title, pdf_rights, title_key


ROOT = Path(__file__).resolve().parents[1]
UNIT = 22
UNIT_LABEL = f"{UNIT:02d}"
EXPECTED_EXERCISES = 23
EXPECTED_SOLUTIONS = 9


def configure() -> None:
    """Redirect every inherited mutable surface before the first request."""
    base.UNIT = UNIT
    base.OUT = ROOT / "authority" / "wikiversity" / f"unit-{UNIT_LABEL}"
    base.ARTIFACTS = ROOT / "authority" / "artifacts"
    base.ASSETS = ROOT / "authority" / "assets"
    base.RIGHTS = ROOT / "authority" / f"RIGHTS-unit-{UNIT_LABEL}.csv"
    base.CLOSURE = ROOT / "authority" / f"ASSET_CLOSURE-unit-{UNIT_LABEL}.json"
    base.COMMONS_META = ROOT / "authority" / f"commons-imageinfo-unit-{UNIT_LABEL}.json"
    base.LECTURE_TITLE = f"{base.COURSE}/Vorlesung {UNIT}"
    base.WORKSHEET_TITLE = f"{base.COURSE}/Arbeitsblatt {UNIT}"
    base.USER_AGENT = "O016-unit22-authority-freeze/1.0 (bounded educational preservation)"
    strong.UNIT = UNIT
    strong.UNIT_LABEL = UNIT_LABEL
    strong.AUDIT_SEMANTIC_IDENTITIES = []


def normalize_asset_ids(assets: list[dict]) -> dict:
    """Replace every inherited Unit 12 asset ID and rebind closure hashes."""
    with base.RIGHTS.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    if not rows or not fieldnames:
        raise RuntimeError("Unit 22 media-rights ledger is empty")
    old_prefix = "br-ak-u12-media-"
    new_prefix = f"br-ak-u{UNIT_LABEL}-media-"

    if len(assets) != len(rows):
        raise RuntimeError("Unit 22 in-memory asset topology mismatch")
    for asset in assets:
        asset_id = asset.get("asset_id", "")
        if not asset_id.startswith(old_prefix):
            raise RuntimeError(f"unexpected inherited in-memory asset ID: {asset_id}")
        asset["asset_id"] = new_prefix + asset_id[len(old_prefix) :]

    for row in rows:
        asset_id = row.get("asset_id", "")
        if not asset_id.startswith(old_prefix):
            raise RuntimeError(f"unexpected inherited asset ID: {asset_id}")
        row["asset_id"] = new_prefix + asset_id[len(old_prefix) :]
    with base.RIGHTS.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    closure = json.loads(base.CLOSURE.read_text(encoding="utf-8"))
    if closure.get("unit") != UNIT or len(closure.get("assets", [])) != len(rows):
        raise RuntimeError("Unit 22 media closure topology mismatch")
    for record in closure["assets"]:
        asset_id = record.get("asset_id", "")
        if not asset_id.startswith(old_prefix):
            raise RuntimeError(f"unexpected inherited closure asset ID: {asset_id}")
        record["asset_id"] = new_prefix + asset_id[len(old_prefix) :]
    closure["rights_bytes"] = base.RIGHTS.stat().st_size
    closure["rights_sha256"] = base.digest(base.RIGHTS)
    closure["reader_credits_required"] = True
    closure["reader_credits_path_planned"] = f"source/id-ID/media-credits-unit-{UNIT_LABEL}.md"
    base.write_json(base.CLOSURE, closure)
    return closure


def official_pdf_rights(pdf_records: list[dict]) -> list[dict]:
    """Bind current Commons description revisions and component licenses."""
    payload = json.loads(base.COMMONS_META.read_text(encoding="utf-8"))
    pages = {
        title_key(page["title"]): page
        for page in payload.get("query", {}).get("pages", [])
        if not page.get("missing")
    }
    records: list[dict] = []
    for witness in pdf_records:
        title = commons_file_title(witness["source_file_title"])
        page = pages.get(title_key(title))
        if page is None:
            raise RuntimeError(f"Commons PDF description is absent: {title}")
        local = ROOT / witness["local_path"]
        record = pdf_rights(page, local)
        records.append(record)
    return records


def ensure_vector_originals(lecture_parsed: dict, worksheet_parsed: dict) -> list[Path]:
    """Bind original SVG bytes when a raster thumbnail would upscale its nominal canvas."""
    names = list(
        dict.fromkeys(lecture_parsed.get("images", []) + worksheet_parsed.get("images", []))
    )
    vector_names = [name for name in names if name.casefold().endswith(".svg")]
    raw, payload = base.api_raw(
        base.COMMONS_API,
        {
            "action": "query",
            "prop": "imageinfo",
            "iiprop": "timestamp|url|size|sha1|mime|mediatype",
            "titles": "|".join("File:" + name for name in vector_names),
        },
    )
    base.write_bytes(base.OUT / "vector-originals-api.json", raw)
    pages = {
        base.file_key(page["title"]): page
        for page in payload.get("query", {}).get("pages", [])
    }
    locals_: list[Path] = []
    for name in vector_names:
        page = pages.get(base.file_key(name))
        if page is None or page.get("missing") or len(page.get("imageinfo", [])) != 1:
            raise RuntimeError(f"vector original did not resolve uniquely: {name}")
        info = page["imageinfo"][0]
        if info.get("mime") != "image/svg+xml" or info.get("mediatype") != "DRAWING":
            raise RuntimeError(f"unexpected vector component type: {name}")
        data = base.fetch(info["url"])
        if len(data) != int(info["size"]) or base.digest_bytes(data, "sha1") != info["sha1"]:
            raise RuntimeError(f"vector original byte identity mismatch: {name}")
        original_url = info["url"].split("?", 1)[0]
        local_name = urllib.parse.unquote(Path(urllib.parse.urlparse(original_url).path).name)
        local = base.ASSETS / local_name
        if local.exists() and local.read_bytes() != data:
            raise RuntimeError(f"refusing to overwrite a different vector original: {local}")
        base.write_bytes(local, data)
        locals_.append(local)
    return locals_


def main() -> int:
    configure()
    base.OUT.mkdir(parents=True, exist_ok=True)
    base.ARTIFACTS.mkdir(parents=True, exist_ok=True)
    base.ASSETS.mkdir(parents=True, exist_ok=True)

    lecture, lecture_parsed = base.entry_surface(base.LECTURE_TITLE, "lecture-22")
    worksheet, worksheet_parsed = base.entry_surface(base.WORKSHEET_TITLE, "worksheet-22")
    lecture_latex, lecture_tex = base.latex_surface(base.LECTURE_TITLE + "/latex", "lecture-22")
    worksheet_latex, worksheet_tex = base.latex_surface(
        base.WORKSHEET_TITLE + "/latex", "worksheet-22"
    )
    lecture_closure = base.transclusion_closure(lecture_parsed, "lecture-22")
    worksheet_closure = base.transclusion_closure(worksheet_parsed, "worksheet-22")
    solutions = base.solution_map(worksheet, worksheet_parsed)
    if (
        int(solutions["exercise_count"]) != EXPECTED_EXERCISES
        or int(solutions["solution_count"]) != EXPECTED_SOLUTIONS
    ):
        raise RuntimeError(
            "Unit 22 exercise/solution topology differs from bounded preflight: "
            f"{solutions['exercise_count']}/{solutions['solution_count']}"
        )
    solution_closures = strong.solution_transclusion_closures(solutions)
    license_surface = strong.course_license_surface()
    ensure_vector_originals(lecture_parsed, worksheet_parsed)
    pdf_records, assets = base.shared_media(lecture_parsed, worksheet_parsed)
    media_closure = normalize_asset_ids(assets)
    pdf_rights_records = official_pdf_rights(pdf_records)
    entry_recheck = base.final_identity_recheck(lecture["revid"], worksheet["revid"])

    solution_recursive_closures = [
        item["recursive_transclusion_closure"] for item in solution_closures
    ]
    all_recursive_closures = [
        lecture_closure,
        worksheet_closure,
        license_surface["recursive_transclusion_closure"],
        *solution_recursive_closures,
    ]
    primary_records = [
        lecture,
        worksheet,
        lecture_latex,
        worksheet_latex,
        license_surface["wrapper"],
    ]
    identity_replay = strong.final_live_identity_replay(
        primary_records,
        all_recursive_closures,
        solutions,
        pdf_records,
        pdf_rights_records,
    )

    manifest = {
        "schema": "brenner-unit-authority-freeze-v2",
        "frozen_utc": datetime.now(timezone.utc).isoformat(),
        "unit_number": UNIT,
        "source_api": base.WIKI_API,
        "source_course_license": strong.CURRENT_LICENSE,
        "source_course_license_authority": license_surface,
        "lecture": lecture,
        "worksheet": worksheet,
        "lecture_latex_page": lecture_latex,
        "worksheet_latex_page": worksheet_latex,
        "latex_capture_semantics": (
            "Each /latex page is a frozen launcher revision; expanded TeX is a byte-bound "
            "capture of its dynamic Parsoid rendering at freeze time."
        ),
        "derived_expanded_tex": [lecture_tex, worksheet_tex],
        "lecture_transclusion_closure": lecture_closure,
        "worksheet_transclusion_closure": worksheet_closure,
        "semantic_audit_identity_bindings": [],
        "solutions": solutions,
        "solution_transclusion_closures": solution_closures,
        "images": {
            "lecture": lecture_parsed.get("images", []),
            "worksheet": worksheet_parsed.get("images", []),
            "substantive_assets": assets,
            "reader_media_positions": media_closure["reader_media_positions"],
        },
        "official_pdf_witnesses": pdf_records,
        "media_rights_accessibility_and_discrepancies": {
            "closure_file": base.CLOSURE.relative_to(ROOT).as_posix(),
            "closure_bytes": base.CLOSURE.stat().st_size,
            "closure_sha256": base.digest(base.CLOSURE),
            "rights_file": base.RIGHTS.relative_to(ROOT).as_posix(),
            "rights_bytes": base.RIGHTS.stat().st_size,
            "rights_sha256": base.digest(base.RIGHTS),
            "official_pdf_component_rights": pdf_rights_records,
            "reader_credits_required": True,
        },
        "entry_revision_recheck": entry_recheck,
        "final_live_identity_replay": identity_replay,
    }
    manifest["files"] = [
        {"file": path.name, "bytes": path.stat().st_size, "sha256": base.digest(path)}
        for path in sorted(base.OUT.iterdir(), key=lambda item: item.name)
        if path.is_file() and path.name != "UNIT_AUTHORITY_MANIFEST.json"
    ]
    external_paths = [
        *(ROOT / item["local_path"] for item in pdf_records),
        *(ROOT / item["local_path"] for item in assets),
        base.RIGHTS,
        base.CLOSURE,
        base.COMMONS_META,
    ]
    manifest["bounded_external_files"] = [
        {
            "file": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": base.digest(path),
        }
        for path in sorted(set(external_paths), key=lambda item: item.as_posix())
    ]
    manifest_path = base.OUT / "UNIT_AUTHORITY_MANIFEST.json"
    base.write_json(manifest_path, manifest)

    replay = json.loads(manifest_path.read_text(encoding="utf-8"))
    actual_names = {
        path.name
        for path in base.OUT.iterdir()
        if path.is_file() and path.name != manifest_path.name
    }
    bound_names = {item["file"] for item in replay["files"]}
    if actual_names != bound_names:
        raise RuntimeError("manifest-local file inventory replay failed")
    for record in replay["files"]:
        path = base.OUT / record["file"]
        if path.stat().st_size != record["bytes"] or base.digest(path) != record["sha256"]:
            raise RuntimeError(f"manifest replay failed: {path}")
    for record in replay["bounded_external_files"]:
        path = ROOT / record["file"]
        if path.stat().st_size != record["bytes"] or base.digest(path) != record["sha256"]:
            raise RuntimeError(f"external-file replay failed: {path}")
    if replay["solutions"]["exercise_count"] != EXPECTED_EXERCISES:
        raise RuntimeError("exercise topology replay failed")
    if replay["solutions"]["solution_count"] != EXPECTED_SOLUTIONS:
        raise RuntimeError("solution topology replay failed")
    if media_closure["reader_media_positions"] != 7 or len(assets) != 7:
        raise RuntimeError("Unit 22 seven-position media topology replay failed")
    if replay["final_live_identity_replay"]["result"] != "PASS":
        raise RuntimeError("final live identity replay did not pass")

    result = {
        "result": "PASS",
        "unit": UNIT,
        "lecture_pageid": lecture["pageid"],
        "lecture_revid": lecture["revid"],
        "worksheet_pageid": worksheet["pageid"],
        "worksheet_revid": worksheet["revid"],
        "lecture_transclusions": lecture_closure["captured_page_count"],
        "worksheet_transclusions": worksheet_closure["captured_page_count"],
        "solution_transclusions": [
            item["recursive_transclusion_closure"]["captured_page_count"]
            for item in solution_closures
        ],
        "exercises": solutions["exercise_count"],
        "public_solutions": solutions["solution_count"],
        "media_positions": media_closure["reader_media_positions"],
        "official_pdf_pages": [item["page_count"] for item in pdf_records],
        "live_replay_identities": identity_replay["wikiversity_identity_count"],
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
