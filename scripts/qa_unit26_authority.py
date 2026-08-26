#!/usr/bin/env python3
"""Fail-closed independent replay of the frozen Unit 26 authority boundary."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "authority" / "wikiversity" / "unit-26"
MANIFEST = OUT / "UNIT_AUTHORITY_MANIFEST.json"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-26.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-26.json"
FREEZE_NOTE = ROOT / "authority" / "UNIT_26_AUTHORITY_FREEZE.md"
RECEIPT = ROOT / "qa" / "UNIT_26_AUTHORITY_QA.json"

COURSE = "Kurs:Algebraische Kurven (Osnabrück 2012)"
TOPIC = "Die Schnittmultiplizität"
CANONICAL_HASHES = {
    "lecture": "f1a064c0531f9079633a57009c565f20a0520a0ef10cb2336ad3b52aa2d331b8",
    "worksheet": "158fd9f6495ee9763d9e01cc1c0969a6be7c8b194dd88c4f8b12edbad900211f",
    "solution-04": "8fd91e101676ccbe314c5905bb2ac8ccbf457c5d629962206124b6878c212d30",
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
    require(manifest["unit_number"] == 26, "unit number")
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
            50732, 793526, 538867, "2022-08-25T06:09:17Z",
            "57845c7bb535d0cccde6d289409a8dbbe684f2d8", 558,
        ),
        "lecture identity",
    )
    require(
        (
            worksheet["pageid"], worksheet["revid"], worksheet["parentid"],
            worksheet["timestamp"], worksheet["mediawiki_sha1"], worksheet["wikitext_bytes"],
        )
        == (
            50761, 793494, 324706, "2022-08-25T06:04:07Z",
            "10aad7862403732dbaa5a05ae637a084c2758751", 1666,
        ),
        "worksheet identity",
    )
    require(TOPIC in api_content(lecture), "lecture topic source")

    latex_expected = {
        "lecture": (51878, 806124, 796343, "2022-09-18T07:14:52Z"),
        "worksheet": (53019, 806092, 796311, "2022-09-18T07:09:42Z"),
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
            "authority/ASSET_CLOSURE-unit-26.json",
            "authority/RIGHTS-unit-26.csv",
            "authority/assets/250px-Intersect3.png",
            "authority/artifacts/lecture-26-official.pdf",
            "authority/artifacts/worksheet-26-official.pdf",
        },
        "bounded external inventory",
    )

    expected_counts = {"lecture": (118, 119), "worksheet": (57, 58)}
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
    require(solutions["exercise_count"] == 11 and solutions["solution_count"] == 1, "exercise/solution count")
    require([item["exercise_number"] for item in entries] == list(range(1, 12)), "exercise order")
    require([item["role"] for item in entries] == ["warm-up"] * 4 + ["submitted"] * 7, "exercise roles")
    require(
        [item["authored_points"] for item in entries]
        == [2, 2, 3, 4, 4, 4, 4, 4, 4, 3, 8],
        "authored points",
    )
    require(
        [item["displayed_points"] for item in entries]
        == [None, None, 3, None, 4, 4, 4, 4, 4, 3, 8],
        "worksheet-displayed points",
    )
    require([item["exercise_number"] for item in entries if item["starred_in_worksheet"]] == [4], "star topology")
    require([item["exercise_number"] for item in entries if item["has_public_solution"]] == [4], "solution set")
    topology = solutions["ordered_role_point_and_star_topology"]
    require(topology["submitted_displayed_point_total"] == 31, "submitted points total")
    require(topology["warm_up_numbers"] == [1, 2, 3, 4], "warm-up role")
    require(topology["submitted_numbers"] == [5, 6, 7, 8, 9, 10, 11], "submitted role")
    require(topology["upload_numbers"] == [], "no upload role")

    negative = solutions["negative_public_solution_evidence"]
    require(negative["exact_candidate_title_count"] == 11, "candidate title count")
    require(negative["positive_numbers"] == [4], "candidate positives")
    require(
        negative["negative_numbers"] == [1, 2, 3, 5, 6, 7, 8, 9, 10, 11]
        and negative["negative_count"] == 10,
        "full negative set",
    )
    require(all(item["api_missing"] is True for item in negative["entries"]), "negative API flags")
    candidate_payload = json.loads((OUT / negative["candidate_query_file"]).read_text(encoding="utf-8"))
    candidate_pages = candidate_payload["query"]["pages"]
    require(len(candidate_pages) == 11, "candidate response count")
    require(sum(bool(page.get("missing")) for page in candidate_pages) == 10, "candidate response missing count")
    require(sum(not bool(page.get("missing")) for page in candidate_pages) == 1, "candidate response positive count")

    expected_solution_identities = {
        4: (21344, 1112503, 1011285, "2026-08-21T15:27:54Z", "82d108d8f5b167d377b1f0a2ec03fa72073786d2", 1365, 9, 10),
    }
    solution_records = manifest["public_solution_transclusion_closures"]
    require([item["exercise_number"] for item in solution_records] == [4], "solution closure order")
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

    require(manifest["source_discrepancy_bindings"] == [], "no source discrepancy binding")
    require(manifest["source_defect_bindings"] == [], "no invented source defect binding")

    lecture_parse = json.loads((OUT / lecture["parse_api_file"]).read_text(encoding="utf-8"))["parse"]
    worksheet_parse = json.loads((OUT / worksheet["parse_api_file"]).read_text(encoding="utf-8"))["parse"]
    expected_images = {
        "Intersect3.png",
        "Algebraische_Kurven_(Osnabrück_2012)Vorlesung26.pdf",
        "Algebraische_Kurven_(Osnabrück_2012)Arbeitsblatt26.pdf",
    }
    require(set(lecture_parse["images"] + worksheet_parse["images"]) == expected_images, "exact parser image set")
    require(lecture_parse["externallinks"] == [] and worksheet_parse["externallinks"] == [], "entry external links")

    with RIGHTS.open(encoding="utf-8", newline="") as stream:
        rights_rows = list(csv.DictReader(stream))
    require(len(rights_rows) == 1, "single-media rights row")
    rights = rights_rows[0]
    require(rights["asset_id"] == "br-ak-u26-media-001" and rights["reader_order"] == "1", "media rights identity")
    require(rights["resource_title"] == "File:Intersect3.png" and rights["metadata_title"] == "File:Intersect3.png", "media title")
    require(rights["local_path"] == "authority/assets/250px-Intersect3.png", "media local path")
    require(rights["local_bytes"] == "5922" and rights["local_sha256"] == "b29c15edf6619632fe033e0b6064c1826226abce0be6219262ca028a2a157818", "media local bytes")
    require(rights["original_bytes"] == "5018" and rights["original_sha1"] == "26fef135fcc9d950958068778e5805830ffa8b8e", "media original bytes")
    require(rights["license_short"] == "CC BY-SA 3.0", "media license")
    require(rights["license_url"] == "http://creativecommons.org/licenses/by-sa/3.0/", "media license URL")
    require(rights["reader_caption_id"] == "br-ak-u26-media-001-caption", "media caption ID")
    require(rights["reader_alt_id"] == "br-ak-u26-media-001-alt", "media alt ID")
    media = json.loads(CLOSURE.read_text(encoding="utf-8"))
    require(media["schema"] == "brenner-unit-media-closure-v2" and media["unit"] == 26, "media closure identity")
    require(media["reader_media_positions"] == 1 and media["unique_local_assets"] == 1 and len(media["assets"]) == 1, "single-media topology")
    require(media["rights_bytes"] == RIGHTS.stat().st_size and media["rights_sha256"] == digest(RIGHTS), "rights binding")
    require(media["reader_credits_required"] is True, "reader credits topology")
    asset = media["assets"][0]
    require(
        (
            asset["description_pageid"], asset["description_revid"], asset["description_parentid"],
            asset["description_timestamp"], asset["description_mediawiki_sha1"], asset["description_wikitext_bytes"],
        )
        == (
            641346, 475878038, 178377620, "2020-09-29T22:17:08Z",
            "03e63ff3aa8d32cce178f10ce577b131f8f2b1c1", 1356,
        ),
        "Commons description identity",
    )
    require(asset["local_sha256"] == "b29c15edf6619632fe033e0b6064c1826226abce0be6219262ca028a2a157818", "asset closure bytes")
    require((asset["width"], asset["height"], asset["frame_count"]) == (250, 249, 1), "asset decoded topology")
    require(asset["license_short"] == "CC BY-SA 3.0" and asset["attribution_required"] is True, "asset rights")
    verify_bound(ROOT / asset["local_path"], asset["local_bytes"], asset["local_sha256"])
    require(media["component_discrepancies"]["exercise_point_discrepancies"] == [], "point discrepancies")

    expected_pdfs = {
        "lecture": (89958, 7, "9ec109463f2fe8f00ca9d3f6edb6f3a604d8c5c6f79ed5dd6584d41456da10c7", 53374, 321257, "c2d188d5f445c7dedd05ac35a3e290b0307647e1", "1b27e2c5d0bf430250d722751382ee3fdb129c6b"),
        "worksheet": (34715, 2, "4b1dc786752f41daa80031e8563ba0446e2d1a6c039798779fd0681f617f1c92", 54209, 325013, "471acc9bf6c2431bacf49ef70dbdd3ac5a9cd28e", "5b91dec48ec4ae9a1fae3a8e227c570ff3361e3f"),
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
    require(replay["result"] == "PASS" and replay["semantic_unique_identity_count"] == 157, "final semantic replay")
    require(sum(batch["title_count"] for batch in replay["semantic_batches"]) == 157, "final replay batches")
    require(replay["local_wikiversity_pdf_identity_count"] == 2, "final PDF replay")
    require(replay["commons_media_identity_count"] == 1, "final Commons replay")
    require(replay["latest_solution_identity_replayed"] == {
        "exercise_number": 4,
        "revid": 1112503,
        "timestamp": "2026-08-21T15:27:54Z",
        "mediawiki_sha1": "82d108d8f5b167d377b1f0a2ec03fa72073786d2",
    }, "latest solution replay")

    note = FREEZE_NOTE.read_text(encoding="utf-8")
    for needle in (
        TOPIC, "warm-up 1-4", "submitted 5-11", "other 10 solution pages absent",
        "CC BY-SA 3.0", "CC BY-SA 4.0", "CC BY-SA 2.0 Germany",
        "157 unique semantic identities",
    ):
        require(needle in note, f"freeze-note evidence: {needle}")

    receipt = {
        "schema": "ag-bridge-unit-authority-qa-v1",
        "result": "PASS",
        "unit": 26,
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
        "entry_revisions": {"course": 658236, "lecture": 793526, "worksheet": 793494},
        "recursive_pages_with_roots": {"lecture": 119, "worksheet": 58, "solution_04": 10},
        "canonical_identity_rows_sha256": CANONICAL_HASHES,
        "exercise_count": 11,
        "roles": {"warm_up": [1, 2, 3, 4], "submitted": [5, 6, 7, 8, 9, 10, 11], "upload": []},
        "submitted_displayed_points": [4, 4, 4, 4, 4, 3, 8],
        "starred_numbers": [4],
        "public_solution_numbers": [4],
        "negative_solution_numbers": [1, 2, 3, 5, 6, 7, 8, 9, 10, 11],
        "reader_media_positions": 1,
        "official_pdf_pages": [7, 2],
        "final_live_identity_replay": {
            "semantic_wikiversity": 157,
            "local_wikiversity_pdfs": 2,
            "commons_media": 1,
        },
        "checks": [
            "course_entry_latex_and_recursive_closure_identities",
            "manifest_local_and_bounded_external_inventory",
            "canonical_identity_hash_recomputation",
            "ordered_roles_authored_and_displayed_points_and_stars",
            "sole_complete_public_solution_closure",
            "exact_11_candidate_positive_and_negative_solution_evidence",
            "single_static_commons_media_bytes_rights_and_accessibility_ids",
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
