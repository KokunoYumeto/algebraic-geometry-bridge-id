#!/usr/bin/env python3
"""Fail-closed independent replay of the frozen Unit 25 authority boundary."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "authority" / "wikiversity" / "unit-25"
MANIFEST = OUT / "UNIT_AUTHORITY_MANIFEST.json"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-25.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-25.json"
FREEZE_NOTE = ROOT / "authority" / "UNIT_25_AUTHORITY_FREEZE.md"
RECEIPT = ROOT / "qa" / "UNIT_25_AUTHORITY_QA.json"

COURSE = "Kurs:Algebraische Kurven (Osnabrück 2012)"
TOPIC = "Lösung in Potenzreihen für algebraische Kurven"
CANONICAL_HASHES = {
    "lecture": "aa14c07698e5e2911790457bee99f6e58a47b68fd5e75520c175ecc2756df8b1",
    "worksheet": "92727348e69deb229c952710318393751f99b09fea0b41b4c855daeadcb62828",
    "solution-01": "cf8713fe21f8f85b327439235147d91ea4be82422f56750a3e70d51fd17e22fe",
    "solution-02": "9c6d058cb3adb20f94624e47caaf62847655243262aeda7d497cceae5a079e51",
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
    fields = ("title", "pageid", "revid", "parentid", "timestamp", "mediawiki_sha1", "wikitext_bytes")
    rows = [{field: record[field] for field in fields} for record in [root, *closure["pages"]]]
    rows.sort(key=lambda row: (row["title"], row["pageid"]))
    raw = json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def api_content(record: dict) -> str:
    payload = json.loads((OUT / record["api_file"]).read_text(encoding="utf-8"))
    page = payload["query"]["pages"][0]
    return page["revisions"][0]["slots"]["main"]["content"]


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(manifest["schema"] == "brenner-unit-authority-freeze-v2", "manifest schema")
    require(manifest["unit_number"] == 25, "unit number")
    require(manifest["source_course"] == COURSE, "source course")
    require(manifest["topic_heading"] == TOPIC, "topic heading")

    course = manifest["source_course_surface"]
    require(
        (course["pageid"], course["revid"], course["parentid"], course["mediawiki_sha1"])
        == (50687, 658236, 439529, "2f2ede7249fcaa55ba17d9cd0e3d9ee9d4941f0c"),
        "course route identity",
    )
    lecture, worksheet = manifest["lecture"], manifest["worksheet"]
    require(
        (
            lecture["pageid"], lecture["revid"], lecture["parentid"],
            lecture["timestamp"], lecture["mediawiki_sha1"], lecture["wikitext_bytes"],
        )
        == (
            50731, 793525, 305024, "2022-08-25T06:09:07Z",
            "c589c3b9586e551eb81d7d941d79a9bc1461fe06", 238,
        ),
        "lecture identity",
    )
    require(
        (
            worksheet["pageid"], worksheet["revid"], worksheet["parentid"],
            worksheet["timestamp"], worksheet["mediawiki_sha1"], worksheet["wikitext_bytes"],
        )
        == (
            50760, 793493, 324710, "2022-08-25T06:03:57Z",
            "1418cec6171ff8fd056dda7e6461f5ca4d91d910", 2077,
        ),
        "worksheet identity",
    )
    require(TOPIC in api_content(lecture), "lecture topic source")

    latex_expected = {
        "lecture": (51879, 806123, 796342, "2022-09-18T07:14:42Z"),
        "worksheet": (53018, 806091, 796310, "2022-09-18T07:09:32Z"),
    }
    for kind, record in (
        ("lecture", manifest["lecture_latex_page"]),
        ("worksheet", manifest["worksheet_latex_page"]),
    ):
        require(
            (record["pageid"], record["revid"], record["parentid"], record["timestamp"])
            == latex_expected[kind],
            f"{kind} /latex identity",
        )
        require(record["mediawiki_sha1"] == "1d092e4f15139d9908d36c4d64a1f4fde570e1ba", f"{kind} /latex SHA-1")
        require(record["wikitext_bytes"] == 9 and api_content(record).strip().casefold() == "{{latex}}", f"{kind} /latex launcher")
    require(all(item["bytes"] > 1000 and len(item["sha256"]) == 64 for item in manifest["derived_expanded_tex"]), "expanded TeX")

    local_names, local_bytes = set(), 0
    for record in manifest["files"]:
        require(record["file"] not in local_names, "duplicate local manifest path")
        local_names.add(record["file"])
        verify_bound(OUT / record["file"], record["bytes"], record["sha256"])
        local_bytes += record["bytes"]
    observed_names = {path.name for path in OUT.iterdir() if path.is_file() and path.name != MANIFEST.name}
    require(observed_names == local_names, "local authority inventory differs from manifest")

    external_names, external_bytes = set(), 0
    for record in manifest["bounded_external_files"]:
        require(record["file"] not in external_names, "duplicate external manifest path")
        external_names.add(record["file"])
        verify_bound(ROOT / record["file"], record["bytes"], record["sha256"])
        external_bytes += record["bytes"]
    require(
        external_names
        == {
            "authority/ASSET_CLOSURE-unit-25.json",
            "authority/RIGHTS-unit-25.csv",
            "authority/artifacts/lecture-25-official.pdf",
            "authority/artifacts/worksheet-25-official.pdf",
        },
        "bounded external inventory",
    )

    expected_counts = {"lecture": (69, 70), "worksheet": (61, 62)}
    for kind, root, closure in (
        ("lecture", lecture, manifest["lecture_transclusion_closure"]),
        ("worksheet", worksheet, manifest["worksheet_transclusion_closure"]),
    ):
        dependencies, with_root = expected_counts[kind]
        topology = manifest["transclusion_topology"][kind]
        require(closure["captured_page_count"] == dependencies and closure["missing_page_count"] == 0, f"{kind} closure")
        require(topology["dependencies"] == dependencies and topology["with_root"] == with_root, f"{kind} topology")
        observed = canonical_identity_hash(root, closure)
        require(observed == CANONICAL_HASHES[kind], f"{kind} canonical hash")
        require(topology["canonical_identity_rows_sha256"] == observed, f"{kind} manifest hash")

    solutions = manifest["solutions"]
    entries = solutions["entries"]
    require(solutions["exercise_count"] == 13 and solutions["solution_count"] == 2, "exercise/solution count")
    require([item["exercise_number"] for item in entries] == list(range(1, 14)), "exercise order")
    require([item["role"] for item in entries] == ["warm-up"] * 5 + ["submitted"] * 7 + ["upload"], "exercise roles")
    require(
        [item["authored_points"] for item in entries]
        == [4, 4, 3, 3, 3, 4, 4, 4, 3, 4, 4, 5, 3],
        "authored points",
    )
    require(
        [item["displayed_points"] for item in entries]
        == [None, None, None, None, None, 4, 4, 4, 3, 4, 4, 5, 4],
        "worksheet-displayed points",
    )
    require([item["exercise_number"] for item in entries if item["starred_in_worksheet"]] == [1, 2], "star topology")
    require([item["exercise_number"] for item in entries if item["has_public_solution"]] == [1, 2], "solution set")
    topology = solutions["ordered_role_point_and_star_topology"]
    require(topology["submitted_displayed_point_total"] == 28, "submitted points total")
    require(topology["upload_numbers"] == [13], "upload role")

    negative = solutions["negative_public_solution_evidence"]
    require(negative["exact_candidate_title_count"] == 13, "candidate title count")
    require(negative["positive_numbers"] == [1, 2], "candidate positives")
    require(negative["negative_numbers"] == list(range(3, 14)) and negative["negative_count"] == 11, "full negative set")
    require(all(item["api_missing"] is True for item in negative["entries"]), "negative API flags")
    candidate_payload = json.loads((OUT / negative["candidate_query_file"]).read_text(encoding="utf-8"))
    candidate_pages = candidate_payload["query"]["pages"]
    require(len(candidate_pages) == 13, "candidate response count")
    require(sum(bool(page.get("missing")) for page in candidate_pages) == 11, "candidate response missing count")
    require(sum(not bool(page.get("missing")) for page in candidate_pages) == 2, "candidate response positive count")

    expected_solution_identities = {
        1: (21296, 1112930, 1022977, "2026-08-22T08:48:42Z", "a388a7f91dd1a2c6759186a6c63de83eb93ba8e9", 1537, 11, 12),
        2: (21581, 1022975, 983076, "2025-08-09T22:30:58Z", "4e9bc137ff33d63de0728b6b9c40093ba7e95e46", 1004, 8, 9),
    }
    solution_records = manifest["public_solution_transclusion_closures"]
    require([item["exercise_number"] for item in solution_records] == [1, 2], "solution closure order")
    for item in solution_records:
        number = item["exercise_number"]
        pageid, revid, parentid, timestamp, sha1, size, deps, with_root = expected_solution_identities[number]
        require(
            (
                item["solution_pageid"], item["solution_revid"], item["solution_parentid"],
                item["solution_timestamp"], item["solution_mediawiki_sha1"], item["solution_wikitext_bytes"],
            )
            == (pageid, revid, parentid, timestamp, sha1, size),
            f"solution {number} identity",
        )
        require(not item["direct_wrapper_dependency_titles"], f"solution {number} wrapper")
        closure = item["recursive_transclusion_closure"]
        require(closure["captured_page_count"] == deps and closure["missing_page_count"] == 0, f"solution {number} closure")
        root = {
            "title": item["solution_title"],
            "pageid": pageid,
            "revid": revid,
            "parentid": parentid,
            "timestamp": timestamp,
            "mediawiki_sha1": sha1,
            "wikitext_bytes": size,
        }
        observed = canonical_identity_hash(root, closure)
        require(observed == CANONICAL_HASHES[f"solution-{number:02d}"], f"solution {number} canonical hash")
        require(item["topology"]["with_root"] == with_root and item["topology"]["canonical_identity_rows_sha256"] == observed, f"solution {number} topology")

    discrepancy = manifest["source_discrepancy_bindings"]
    require(len(discrepancy) == 1 and discrepancy[0]["id"] == "AGC-U25-POINT-001", "source discrepancy set")
    require(
        discrepancy[0]["exercise_page_authored_points"] == 3
        and discrepancy[0]["worksheet_displayed_points"] == 4,
        "Exercise 13 point mismatch",
    )
    require(manifest["source_defect_bindings"] == [], "no invented source defect binding")

    lecture_parse = json.loads((OUT / lecture["parse_api_file"]).read_text(encoding="utf-8"))["parse"]
    worksheet_parse = json.loads((OUT / worksheet["parse_api_file"]).read_text(encoding="utf-8"))["parse"]
    expected_images = {
        "Algebraische_Kurven_(Osnabrück_2012)Vorlesung25.pdf",
        "Algebraische_Kurven_(Osnabrück_2012)Arbeitsblatt25.pdf",
    }
    require(set(lecture_parse["images"] + worksheet_parse["images"]) == expected_images, "exact parser PDF set")
    require(lecture_parse["externallinks"] == [] and worksheet_parse["externallinks"] == [], "entry external links")

    with RIGHTS.open(encoding="utf-8", newline="") as stream:
        rights_rows = list(csv.DictReader(stream))
    require(not rights_rows, "zero-media rights must be header-only")
    media = json.loads(CLOSURE.read_text(encoding="utf-8"))
    require(media["schema"] == "brenner-unit-media-closure-v2" and media["unit"] == 25, "media closure identity")
    require(media["reader_media_positions"] == 0 and media["unique_local_assets"] == 0 and not media["assets"], "zero-media topology")
    require(media["rights_bytes"] == RIGHTS.stat().st_size and media["rights_sha256"] == digest(RIGHTS), "rights binding")
    require(media["reader_credits_required"] is False, "reader credits topology")
    require(media["component_discrepancies"]["exercise_13_point_mismatch"] == {
        "exercise_page_authored_points": 3,
        "worksheet_displayed_points": 4,
    }, "media discrepancy binding")

    expected_pdfs = {
        "lecture": (83406, 7, "2543659400dcdeae70e7b088ebd2acc3298444af944812a10e1ae87cc939c449", 53373, 321060, "d0d7141c0525cc5ca6f46dbced1440e5810c7181", "f456dc49f8f4c1f1d67c921124496871f54f5c0b"),
        "worksheet": (47791, 3, "e111513289034c75da657a778b7ca699e1a5fda55749477e5696aa5afa00a8d5", 54066, 325012, "ec33bc155eff7d14d09400537869a151a38446b0", "3d854595c241715a34b1f003440b2171d2e4b7e8"),
    }
    pdfs = {item["kind"]: item for item in manifest["official_pdf_witnesses"]}
    for kind, expected in expected_pdfs.items():
        item = pdfs[kind]
        require(
            (
                item["local_bytes"], item["page_count"], item["local_sha256"], item["file_pageid"],
                item["file_revid"], item["file_mediawiki_sha1"], item["source_sha1"],
            )
            == expected,
            f"{kind} PDF identity",
        )
        verify_bound(ROOT / item["local_path"], item["local_bytes"], item["local_sha256"])
        require(item["blank_page_numbers"] == [] and item["extractable_text_characters"] > 0, f"{kind} PDF text")
        require(item["accessibility"] == {
            "encrypted": False,
            "tagged_pdf": False,
            "structure_tree_present": False,
            "document_language": None,
            "outline_or_bookmark_count": 0,
        }, f"{kind} PDF accessibility")
        route = item["component_license_route"]
        require(route["current_print_version_notice"] == "CC BY-SA 4.0", f"{kind} current notice")
        require(route["legacy_file_notice"] == "CC BY-SA 2.0 Germany", f"{kind} legacy notice")
        require(route["embedded_pdf_label"] is None, f"{kind} no embedded label")
        html = (OUT / route["current_notice_evidence"]).read_text(encoding="utf-8").casefold()
        require("creativecommons.org/licenses/by-sa/4.0" in html, f"{kind} 4.0 evidence")
        require("creativecommons.org/licenses/by-sa/2.0/de" in html, f"{kind} 2.0-DE evidence")

    route = manifest["source_component_license_route"]
    require(route["semantic_site_rights"]["notice"] == "CC BY-SA 4.0", "semantic license")
    require("creativecommons.org/licenses/by-sa/4.0" in route["semantic_site_rights"]["url"], "rights URL")
    require(route["official_pdf_legacy_notice"] == "CC BY-SA 2.0 Germany", "legacy route")
    require(route["no_blanket_relicensing_claim"] is True, "no blanket relicensing")

    replay = manifest["final_live_identity_replay"]
    require(replay["result"] == "PASS" and replay["semantic_unique_identity_count"] == 120, "final semantic replay")
    require(sum(batch["title_count"] for batch in replay["semantic_batches"]) == 120, "final replay batches")
    require(replay["local_wikiversity_pdf_identity_count"] == 2, "final PDF replay")
    require(replay["latest_solution_identity_replayed"] == {
        "exercise_number": 1,
        "revid": 1112930,
        "timestamp": "2026-08-22T08:48:42Z",
        "mediawiki_sha1": "a388a7f91dd1a2c6759186a6c63de83eb93ba8e9",
    }, "latest solution replay")

    note = FREEZE_NOTE.read_text(encoding="utf-8")
    for needle in (
        TOPIC, "warm-up 1-5", "submitted 6-12", "upload 13", "other 11 solution pages absent",
        "authored points while the worksheet displays", "CC BY-SA 4.0", "CC BY-SA 2.0 Germany",
        "120 unique semantic identities",
    ):
        require(needle in note, f"freeze-note evidence: {needle}")

    receipt = {
        "schema": "ag-bridge-unit-authority-qa-v1",
        "result": "PASS",
        "unit": 25,
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
        "entry_revisions": {"course": 658236, "lecture": 793525, "worksheet": 793493},
        "recursive_pages_with_roots": {"lecture": 70, "worksheet": 62, "solution_01": 12, "solution_02": 9},
        "canonical_identity_rows_sha256": CANONICAL_HASHES,
        "exercise_count": 13,
        "roles": {"warm_up": [1, 2, 3, 4, 5], "submitted": [6, 7, 8, 9, 10, 11, 12], "upload": [13]},
        "submitted_displayed_points": [4, 4, 4, 3, 4, 4, 5],
        "upload_displayed_points": 4,
        "upload_authored_points": 3,
        "starred_numbers": [1, 2],
        "public_solution_numbers": [1, 2],
        "negative_solution_numbers": list(range(3, 14)),
        "reader_media_positions": 0,
        "official_pdf_pages": [7, 3],
        "final_live_identity_replay": {"semantic_wikiversity": 120, "local_wikiversity_pdfs": 2},
        "checks": [
            "course_entry_latex_and_recursive_closure_identities",
            "manifest_local_and_bounded_external_inventory",
            "canonical_identity_hash_recomputation",
            "ordered_roles_authored_and_displayed_points_and_stars",
            "two_complete_public_solution_closures",
            "exact_13_candidate_positive_and_negative_solution_evidence",
            "exercise_13_authored_vs_displayed_point_discrepancy",
            "zero_substantive_media_and_header_only_rights",
            "official_local_pdf_bytes_pages_text_and_accessibility",
            "dual_current_and_legacy_component_license_notices",
            "captured_final_live_identity_replay_including_latest_solution",
        ],
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({
        "result": "PASS",
        "receipt": RECEIPT.relative_to(ROOT).as_posix(),
        "receipt_sha256": digest(RECEIPT),
        "manifest_sha256": digest(MANIFEST),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
