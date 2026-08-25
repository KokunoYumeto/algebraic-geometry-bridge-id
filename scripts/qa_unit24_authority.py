#!/usr/bin/env python3
"""Fail-closed independent replay of the frozen Unit 24 authority boundary."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "authority" / "wikiversity" / "unit-24"
MANIFEST = OUT / "UNIT_AUTHORITY_MANIFEST.json"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-24.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-24.json"
FREEZE_NOTE = ROOT / "authority" / "UNIT_24_AUTHORITY_FREEZE.md"
RECEIPT = ROOT / "qa" / "UNIT_24_AUTHORITY_QA.json"

CANONICAL_HASHES = {
    "lecture": "861c2d4566a137c9c3d791480bfa2f1f36a7885798f54f34c8e60557d34e75b2",
    "worksheet": "b02b815554f0c5dbb4e8f5aceb6b7cc7faa747d9c7c1aa136facd1f62d1831f1",
    "solution": "df98d341ed63b4cbd1b0051d725bfc8606937f489203941525b21bdfd54df7af",
}

PREFLIGHT_HASHES = {
    "lecture": "867955dfa799954da0c33d9b09625f7e194eda8ebfbdc23348c1c4ffbab83fa6",
    "worksheet": "baf26dd0e702bc9ebb4f0466b5c0e4e3c4daea3ab028a8964da4f7b7bc128b91",
    "solution": "978d772d44d664efcea08fb0de14e540f63bafeb2c1202552c4f209a8a3280a8",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def verify_bound(path: Path, expected_bytes: int, expected_sha256: str) -> None:
    require(path.is_file() and not path.is_symlink(), f"missing/non-regular bound file: {path}")
    require(path.stat().st_size == expected_bytes, f"byte mismatch: {path}")
    require(digest(path) == expected_sha256, f"SHA-256 mismatch: {path}")


def canonical_identity_hash(root: dict, closure: dict) -> str:
    fields = (
        "title",
        "pageid",
        "revid",
        "parentid",
        "timestamp",
        "mediawiki_sha1",
        "wikitext_bytes",
    )
    rows = [{field: record[field] for field in fields} for record in [root, *closure["pages"]]]
    rows.sort(key=lambda row: (row["title"], row["pageid"]))
    raw = json.dumps(
        rows,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(manifest["schema"] == "brenner-unit-authority-freeze-v2", "manifest schema")
    require(manifest["unit_number"] == 24, "unit number")
    require(manifest["source_course"] == "Kurs:Algebraische Kurven (Osnabrück 2012)", "source course")

    lecture = manifest["lecture"]
    worksheet = manifest["worksheet"]
    require(
        (lecture["pageid"], lecture["revid"], lecture["mediawiki_sha1"])
        == (50730, 933672, "af86fa9893c96376f910495b9a5d0c8be417b09e"),
        "lecture identity",
    )
    require(
        (worksheet["pageid"], worksheet["revid"], worksheet["mediawiki_sha1"])
        == (50759, 793492, "507a5966770c007e813734ca85da4e85f8a93b60"),
        "worksheet identity",
    )
    require(
        (
            manifest["lecture_latex_page"]["pageid"],
            manifest["lecture_latex_page"]["revid"],
            manifest["lecture_latex_page"]["mediawiki_sha1"],
        )
        == (51880, 806122, "1d092e4f15139d9908d36c4d64a1f4fde570e1ba"),
        "lecture /latex identity",
    )
    require(
        (
            manifest["worksheet_latex_page"]["pageid"],
            manifest["worksheet_latex_page"]["revid"],
            manifest["worksheet_latex_page"]["mediawiki_sha1"],
        )
        == (53017, 806090, "1d092e4f15139d9908d36c4d64a1f4fde570e1ba"),
        "worksheet /latex identity",
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
        path.name
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

    topologies = manifest["transclusion_topology"]
    expected_counts = {"lecture": (121, 122), "worksheet": (64, 65)}
    for kind, root, closure in (
        ("lecture", lecture, manifest["lecture_transclusion_closure"]),
        ("worksheet", worksheet, manifest["worksheet_transclusion_closure"]),
    ):
        dependencies, with_root = expected_counts[kind]
        require(closure["captured_page_count"] == dependencies, f"{kind} dependency count")
        require(closure["missing_page_count"] == 0, f"{kind} missing dependency")
        require(topologies[kind]["with_root"] == with_root, f"{kind} with-root count")
        observed = canonical_identity_hash(root, closure)
        require(observed == CANONICAL_HASHES[kind], f"{kind} canonical hash")
        require(topologies[kind]["canonical_identity_rows_sha256"] == observed, f"{kind} manifest canonical hash")
        require(topologies[kind]["preflight_reported_identity_sha256"] == PREFLIGHT_HASHES[kind], f"{kind} preflight hash record")
        require(topologies[kind]["preflight_hash_serialization_status"] == "ALGORITHM_NOT_YET_IDENTIFIED", f"{kind} preflight disposition")
        algorithm = topologies[kind]["canonical_identity_hash_algorithm"]
        require("title,pageid,revid,parentid,timestamp,mediawiki_sha1,wikitext_bytes" in algorithm, f"{kind} algorithm fields")
        require("ensure_ascii=false" in algorithm and "sort_keys=true" in algorithm, f"{kind} algorithm serialization")

    solutions = manifest["solutions"]
    require(solutions["exercise_count"] == 10, "exercise count")
    require(solutions["solution_count"] == 1, "solution count")
    entries = solutions["entries"]
    require([item["exercise_number"] for item in entries] == list(range(1, 11)), "exercise order")
    require([item["role"] for item in entries] == ["practice"] * 5 + ["submitted"] * 5, "exercise roles")
    require([item["authored_points"] for item in entries] == [2, 2, 2, 2, 3, 5, 3, 3, 3, 6], "authored points")
    require([item["exercise_number"] for item in entries if item["points_displayed_in_worksheet"]] == [6, 7, 8, 9, 10], "displayed point range")
    require([item["displayed_points"] for item in entries[5:]] == [5, 3, 3, 3, 6], "submitted points")
    require([item["exercise_number"] for item in entries if item["starred_in_worksheet"]] == [4], "starred exercise")
    require([item["exercise_number"] for item in entries if item["has_public_solution"]] == [4], "public solution set")

    solution = manifest["solution_transclusion_closure"]
    require(
        (
            solution["solution_pageid"],
            solution["solution_revid"],
            solution["solution_mediawiki_sha1"],
        )
        == (168447, 1068135, "c7d3afd4c8e56433e1d4b12c4ebb8e10b460bec0"),
        "solution identity",
    )
    require(not solution["direct_wrapper_dependency_titles"], "solution wrapper topology")
    require(solution["recursive_transclusion_closure"]["captured_page_count"] == 17, "solution dependency count")
    require(solution["recursive_transclusion_closure"]["missing_page_count"] == 0, "solution missing dependency")
    solution_root = {
        "title": solution["solution_title"],
        "pageid": solution["solution_pageid"],
        "revid": solution["solution_revid"],
        "parentid": 0,
        "timestamp": "2026-01-31T11:13:20Z",
        "mediawiki_sha1": solution["solution_mediawiki_sha1"],
        "wikitext_bytes": 882,
    }
    solution_hash = canonical_identity_hash(solution_root, solution["recursive_transclusion_closure"])
    require(solution_hash == CANONICAL_HASHES["solution"], "solution canonical hash")
    require(solution["topology"]["canonical_identity_rows_sha256"] == solution_hash, "solution manifest hash")
    require(solution["topology"]["preflight_reported_identity_sha256"] == PREFLIGHT_HASHES["solution"], "solution preflight hash")

    with RIGHTS.open(encoding="utf-8", newline="") as stream:
        rights_rows = list(csv.DictReader(stream))
    require(not rights_rows, "zero-media rights must be header-only")
    media = json.loads(CLOSURE.read_text(encoding="utf-8"))
    require(media["schema"] == "brenner-unit-media-closure-v2" and media["unit"] == 24, "media closure identity")
    require(media["reader_media_positions"] == 0 and media["unique_local_assets"] == 0, "zero-media topology")
    require(not media["assets"], "zero-media asset list")
    require(media["rights_bytes"] == RIGHTS.stat().st_size and media["rights_sha256"] == digest(RIGHTS), "rights binding")
    require(media["reader_credits_required"] is False, "reader credits topology")

    pdfs = {item["kind"]: item for item in manifest["official_pdf_witnesses"]}
    expected_pdfs = {
        "lecture": (90541, 6, "916b8d41a946cdf8ac978112a46e4f6d1dfb6c70fc0efc65a689cb8ff7205df1", 54026, 320347, "b19f86421aee262b9294058e2bc8d230e6de7fce"),
        "worksheet": (33474, 2, "733135d556513d01148333551693db2713915ee82ac8faa8ce745e966c073102", 54022, 325009, "fbd55561e353056ea6661f87be2c3263fd1cd373"),
    }
    for kind, expected in expected_pdfs.items():
        item = pdfs[kind]
        require(
            (
                item["local_bytes"],
                item["page_count"],
                item["local_sha256"],
                item["file_pageid"],
                item["file_revid"],
                item["source_sha1"],
            )
            == expected,
            f"{kind} PDF identity",
        )
        verify_bound(ROOT / item["local_path"], item["local_bytes"], item["local_sha256"])
        accessibility = item["accessibility"]
        require(accessibility == {
            "encrypted": False,
            "tagged_pdf": False,
            "structure_tree_present": False,
            "document_language": None,
            "outline_or_bookmark_count": 0,
        }, f"{kind} PDF accessibility")
        route = item["component_license_route"]
        require(route["current_print_version_notice"] == "CC BY-SA 4.0", f"{kind} current notice")
        require(route["legacy_file_notice"] == "CC BY-SA 2.0 Germany", f"{kind} legacy notice")
        require(route["embedded_pdf_label"] is None, f"{kind} no embedded license text")

    route = manifest["source_component_license_route"]
    require(route["semantic_site_rights"]["notice"] == "CC BY-SA 4.0", "site semantic license")
    require("creativecommons.org/licenses/by-sa/4.0" in route["semantic_site_rights"]["url"], "site rights URL")
    require(route["official_pdf_legacy_notice"] == "CC BY-SA 2.0 Germany", "legacy PDF/file notice")
    require(route["no_blanket_relicensing_claim"] is True, "no blanket claim")

    source_defects = manifest["source_defect_bindings"]
    require([item["id"] for item in source_defects] == ["AGC-U24-SRC-001"], "source defect set")
    source_defect = source_defects[0]
    require(source_defect["exercise_number"] == 7, "Exercise 7 defect number")
    require(source_defect["displayed_source"] == "X^2-Y^2-Y^3", "Exercise 7 displayed source")
    require(source_defect["cited_example_curve"] == "V(y^2-x^2-x^3)", "Exercise 7 cited curve")
    require("Y^2-X^2-X^3" in source_defect["required_reader_repair"], "Exercise 7 target")

    historical = manifest["historical_pdf_defect_bindings"]
    require([item["id"] for item in historical] == ["AGC-U24-PDF-001", "AGC-U24-PDF-002"], "historical defect set")
    require(historical[0]["live_identity"]["pageid"] == 18305, "G/y^2 live binding")
    require(historical[0]["historical_pdf_form"] == "G x^2", "G/x^2 historical form")
    require(historical[0]["live_semantic_form"] == "G y^2", "G/y^2 live form")
    require(historical[1]["live_identity"]["pageid"] == 20953, "coefficient live binding")
    require(historical[1]["mathematically_required_form"].endswith("b_{ell+1}T^{ell+1}+..."), "coefficient target")
    require("disproves" in historical[1]["preflight_claim_disposition"], "preflight claim disposition")

    replay = manifest["final_live_identity_replay"]
    require(replay["result"] == "PASS", "final replay state")
    require(replay["semantic_unique_identity_count"] == 159, "final semantic identity count")
    require(sum(batch["title_count"] for batch in replay["semantic_batches"]) == 159, "final replay batches")
    require(replay["local_wikiversity_pdf_identity_count"] == 2, "final PDF identity replay")

    note = FREEZE_NOTE.read_text(encoding="utf-8")
    require("CC BY-SA 2.0 Germany" in note and "CC BY-SA 4.0" in note, "freeze-note license routes")
    require("Y^2-X^2-X^3" in note and "a_{ell+1}" in note and "b_{ell+1}" in note, "freeze-note corrections")

    receipt = {
        "schema": "ag-bridge-unit-authority-qa-v1",
        "result": "PASS",
        "unit": 24,
        "frozen_utc": manifest["frozen_utc"],
        "authority_manifest": {
            "path": MANIFEST.relative_to(ROOT).as_posix(),
            "bytes": MANIFEST.stat().st_size,
            "sha256": digest(MANIFEST),
        },
        "authority_freeze_note": {
            "path": FREEZE_NOTE.relative_to(ROOT).as_posix(),
            "bytes": FREEZE_NOTE.stat().st_size,
            "sha256": digest(FREEZE_NOTE),
        },
        "qa_script": {
            "path": Path(__file__).resolve().relative_to(ROOT).as_posix(),
            "bytes": Path(__file__).stat().st_size,
            "sha256": digest(Path(__file__)),
        },
        "local_inventory": {"files": len(local_names), "bytes": local_bytes},
        "bounded_external_inventory": {"files": len(external_names), "bytes": external_bytes},
        "entry_revisions": {"lecture": 933672, "worksheet": 793492},
        "recursive_pages_with_roots": {"lecture": 122, "worksheet": 65, "solution": 18},
        "canonical_identity_rows_sha256": CANONICAL_HASHES,
        "noncontrolling_preflight_serialization_sha256": PREFLIGHT_HASHES,
        "exercise_count": 10,
        "practice_numbers": [1, 2, 3, 4, 5],
        "submitted_points": [5, 3, 3, 3, 6],
        "public_solution_numbers": [4],
        "reader_media_positions": 0,
        "official_pdf_pages": [6, 2],
        "final_live_identity_replay": {"semantic_wikiversity": 159, "local_wikiversity_pdfs": 2},
        "checks": [
            "manifest_local_inventory_bytes_and_hashes",
            "bounded_external_inventory_bytes_and_hashes",
            "entry_latex_and_recursive_closure_identities",
            "documented_canonical_identity_hash_recomputation",
            "noncontrolling_preflight_hash_serialization_mismatch_disclosed",
            "ordered_exercise_points_star_and_public_solution_topology",
            "complete_public_solution_dependency_closure",
            "zero_substantive_media_header_only_rights",
            "official_local_wikiversity_pdf_bytes_pages_and_accessibility",
            "dual_current_and_legacy_component_license_notices",
            "exercise_7_and_historical_pdf_math_defect_bindings",
            "captured_final_live_identity_replay",
        ],
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "result": "PASS",
                "receipt": RECEIPT.relative_to(ROOT).as_posix(),
                "receipt_sha256": digest(RECEIPT),
                "manifest_sha256": digest(MANIFEST),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
