"""Fail-closed independent replay of the frozen Unit 22 authority boundary."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "authority" / "wikiversity" / "unit-22"
MANIFEST = OUT / "UNIT_AUTHORITY_MANIFEST.json"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-22.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-22.json"
RECEIPT = ROOT / "qa" / "UNIT_22_AUTHORITY_QA.json"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def verify_bound(path: Path, expected_bytes: int, expected_sha256: str) -> None:
    require(path.is_file(), f"missing bound file: {path}")
    require(path.stat().st_size == expected_bytes, f"byte mismatch: {path}")
    require(digest(path) == expected_sha256, f"SHA-256 mismatch: {path}")


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(manifest["schema"] == "brenner-unit-authority-freeze-v2", "schema")
    require(manifest["unit_number"] == 22, "unit")

    lecture = manifest["lecture"]
    worksheet = manifest["worksheet"]
    require(
        (lecture["pageid"], lecture["revid"], lecture["mediawiki_sha1"])
        == (165911, 1051397, "907644dc696a39dc2462e100fe3dd1f8a452fd8a"),
        "lecture identity",
    )
    require(
        (worksheet["pageid"], worksheet["revid"], worksheet["mediawiki_sha1"])
        == (165941, 1062660, "e82e91c94f0a39d73aa10913d6821f673925893e"),
        "worksheet identity",
    )

    local_names: set[str] = set()
    local_bytes = 0
    for record in manifest["files"]:
        require(record["file"] not in local_names, "duplicate local manifest path")
        local_names.add(record["file"])
        path = OUT / record["file"]
        verify_bound(path, record["bytes"], record["sha256"])
        local_bytes += record["bytes"]
    observed_names = {
        path.relative_to(OUT).as_posix()
        for path in OUT.iterdir()
        if path.is_file() and path.name != MANIFEST.name
    }
    require(observed_names == local_names, "local authority inventory differs from manifest")

    external_names: set[str] = set()
    external_bytes = 0
    for record in manifest["bounded_external_files"]:
        require(record["file"] not in external_names, "duplicate external manifest path")
        external_names.add(record["file"])
        path = ROOT / record["file"]
        verify_bound(path, record["bytes"], record["sha256"])
        external_bytes += record["bytes"]

    require(manifest["lecture_transclusion_closure"]["captured_page_count"] == 131, "lecture closure")
    require(manifest["lecture_transclusion_closure"]["missing_page_count"] == 0, "lecture missing")
    require(manifest["worksheet_transclusion_closure"]["captured_page_count"] == 118, "worksheet closure")
    require(manifest["worksheet_transclusion_closure"]["missing_page_count"] == 0, "worksheet missing")
    license_authority = manifest["source_course_license_authority"]
    require(license_authority["declared_license"] == "CC BY-SA 4.0", "course license")
    require(
        license_authority["recursive_transclusion_closure"]["missing_page_count"] == 0,
        "license closure",
    )

    solutions = manifest["solutions"]
    require(solutions["exercise_count"] == 23, "exercise count")
    require(solutions["solution_count"] == 9, "solution count")
    require([entry["exercise_number"] for entry in solutions["entries"]] == list(range(1, 24)), "exercise order")
    public_numbers = [entry["exercise_number"] for entry in solutions["entries"] if entry["has_public_solution"]]
    require(public_numbers == [5, 6, 9, 10, 12, 14, 15, 16, 18], "public solution set")
    solution_closures = manifest["solution_transclusion_closures"]
    require([item["exercise_number"] for item in solution_closures] == public_numbers, "solution closure order")
    require(
        [item["recursive_transclusion_closure"]["captured_page_count"] for item in solution_closures]
        == [7, 10, 13, 10, 10, 7, 9, 11, 13],
        "solution closure sizes",
    )
    require(
        all(item["recursive_transclusion_closure"]["missing_page_count"] == 0 for item in solution_closures),
        "missing solution dependency",
    )
    wrappers = {item["exercise_number"]: item["direct_wrapper_dependency_titles"] for item in solution_closures}
    require(wrappers[9] == ["Ebene algebraische Kurve/Glatter Punkt/Liegt nur auf einer Komponente/Fakt/Beweis"], "Exercise 9 wrapper")
    require(all(not titles for number, titles in wrappers.items() if number != 9), "unexpected solution wrapper")

    with RIGHTS.open(encoding="utf-8", newline="") as stream:
        rights_rows = list(csv.DictReader(stream))
    closure = json.loads(CLOSURE.read_text(encoding="utf-8"))
    expected_ids = [f"br-ak-u22-media-{index:03d}" for index in range(1, 8)]
    require([row["asset_id"] for row in rights_rows] == expected_ids, "rights asset IDs")
    require([record["asset_id"] for record in closure["assets"]] == expected_ids, "closure asset IDs")
    require(closure["unit"] == 22 and closure["reader_media_positions"] == 7, "media topology")
    require(closure["rights_bytes"] == RIGHTS.stat().st_size, "closure rights bytes")
    require(closure["rights_sha256"] == digest(RIGHTS), "closure rights hash")

    manifest_assets = manifest["images"]["substantive_assets"]
    require([record["asset_id"] for record in manifest_assets] == expected_ids, "manifest asset IDs")
    require(manifest["images"]["reader_media_positions"] == 7, "manifest media positions")
    for row, closure_record, manifest_record in zip(rights_rows, closure["assets"], manifest_assets, strict=True):
        local = ROOT / row["local_path"]
        verify_bound(local, int(row["local_bytes"]), row["local_sha256"])
        require(closure_record["local_path"] == row["local_path"], "closure path")
        require(closure_record["local_sha256"] == row["local_sha256"], "closure asset hash")
        require(manifest_record["local_path"] == row["local_path"], "manifest path")
        require(manifest_record["local_sha256"] == row["local_sha256"], "manifest asset hash")

    expected_originals = {
        "File:Tangent to a curve.svg": (669, "7c9883519afcaa315116654e4a5b9e653c3b9069"),
        "File:3 equations -5.JPG": (28887, "2c7da50d20fd763dd6347ea205b47e7b65cc1860"),
        "File:Frans Hals - Portret van René Descartes.jpg": (155042, "1edcb2775f3fe8f0e8a76eb9a7127afe597d2259"),
        "File:Kartesisches-Blatt.svg": (4895, "f27ef84850014c7b8fed8187927483b8116b2362"),
        "File:Intersect3.png": (5018, "26fef135fcc9d950958068778e5805830ffa8b8e"),
        "File:Cercle tangente rayon.svg": (778, "0324054d23c963b33c2cc483db82f6325312aef8"),
        "File:Cardioid.svg": (214237, "94a988489019f8b39a2b9ca445cb1adf66ca56f9"),
    }
    require(
        {row["metadata_title"]: (int(row["original_bytes"]), row["original_sha1"]) for row in rights_rows}
        == expected_originals,
        "Commons original identities",
    )
    require(sum(row["attribution_required"].casefold() == "true" for row in rights_rows) == 4, "attribution topology")

    pdfs = manifest["official_pdf_witnesses"]
    require([item["page_count"] for item in pdfs] == [9, 7], "PDF pages")
    require(
        [item["local_sha256"] for item in pdfs]
        == [
            "ae0905f5a2fc3faf2d52902abd85d79cbc50faf15d0067ed2b368c997e843401",
            "0806b21d473557628ddf3315700756a25bfe5736e33db1e54927e05cf2b2efeb",
        ],
        "PDF identities",
    )
    for item in pdfs:
        verify_bound(ROOT / item["local_path"], item["local_bytes"], item["local_sha256"])

    replay = manifest["final_live_identity_replay"]
    require(replay["result"] == "PASS", "final replay state")
    require(replay["wikiversity_identity_count"] == 242, "final Wikiversity replay count")
    require(sum(batch["title_count"] for batch in replay["wikiversity_batches"]) == 242, "replay batches")
    require(replay["commons_pdf_identity_count"] == 2, "final Commons replay count")

    serialized_manifest = MANIFEST.read_text(encoding="utf-8")
    require("br-ak-u12-media-" not in serialized_manifest, "stale Unit 12 asset ID in manifest")
    require("br-ak-u12-media-" not in RIGHTS.read_text(encoding="utf-8"), "stale Unit 12 asset ID in rights")
    require("br-ak-u12-media-" not in CLOSURE.read_text(encoding="utf-8"), "stale Unit 12 asset ID in closure")

    receipt = {
        "schema": "ag-bridge-unit-authority-qa-v1",
        "result": "PASS",
        "unit": 22,
        "frozen_utc": manifest["frozen_utc"],
        "authority_manifest": {
            "path": MANIFEST.relative_to(ROOT).as_posix(),
            "bytes": MANIFEST.stat().st_size,
            "sha256": digest(MANIFEST),
        },
        "qa_script": {
            "path": Path(__file__).resolve().relative_to(ROOT).as_posix(),
            "bytes": Path(__file__).stat().st_size,
            "sha256": digest(Path(__file__)),
        },
        "local_inventory": {"files": len(local_names), "bytes": local_bytes},
        "bounded_external_inventory": {"files": len(external_names), "bytes": external_bytes},
        "entry_revisions": {"lecture": lecture["revid"], "worksheet": worksheet["revid"]},
        "recursive_pages": {
            "lecture": 131,
            "worksheet": 118,
            "solutions": [7, 10, 13, 10, 10, 7, 9, 11, 13],
            "missing": 0,
        },
        "exercise_count": 23,
        "public_solution_numbers": public_numbers,
        "reader_media_positions": 7,
        "asset_ids": expected_ids,
        "official_pdf_pages": [9, 7],
        "final_live_identity_replay": {"wikiversity": 242, "commons_pdfs": 2},
        "checks": [
            "manifest_local_inventory_bytes_and_hashes",
            "bounded_external_inventory_bytes_and_hashes",
            "entry_and_recursive_closure_identities",
            "ordered_exercise_and_public_solution_topology",
            "complete_solution_wrapper_and_dependency_closure",
            "unit_scoped_media_ids_rights_assets_and_original_identities",
            "official_pdf_component_identities",
            "captured_final_live_identity_replay",
            "no_stale_unit12_asset_identifiers",
        ],
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "receipt": RECEIPT.relative_to(ROOT).as_posix(), "receipt_sha256": digest(RECEIPT), "manifest_sha256": digest(MANIFEST)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
