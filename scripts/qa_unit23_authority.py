#!/usr/bin/env python3
"""Fail-closed independent replay of the frozen Unit 23 authority boundary."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "authority" / "wikiversity" / "unit-23"
MANIFEST = OUT / "UNIT_AUTHORITY_MANIFEST.json"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-23.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-23.json"
FREEZE = ROOT / "authority" / "UNIT_23_AUTHORITY_FREEZE.md"
RECEIPT = ROOT / "qa" / "UNIT_23_AUTHORITY_QA.json"


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
    require(path.is_file() and not path.is_symlink(), f"missing/non-regular bound file: {path}")
    require(path.stat().st_size == expected_bytes, f"byte mismatch: {path}")
    require(digest(path) == expected_sha256, f"SHA-256 mismatch: {path}")


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(manifest["schema"] == "brenner-unit-authority-freeze-v2", "schema")
    require(manifest["unit_number"] == 23, "unit")

    lecture = manifest["lecture"]
    worksheet = manifest["worksheet"]
    require(
        (
            lecture["pageid"],
            lecture["revid"],
            lecture["parentid"],
            lecture["timestamp"],
            lecture["mediawiki_sha1"],
            lecture["wikitext_bytes"],
            lecture["html_bytes"],
            lecture["html_sha256"],
        )
        == (
            165912,
            1112318,
            1051403,
            "2026-08-21T09:42:07Z",
            "a38160a106cf39298b3f2cb23f7880e05a5a86f7",
            3363,
            137610,
            "8ec4e80cb109e67aa9dba5b6c408760d77baa00c0e107409453eabe653ee5d43",
        ),
        "lecture identity",
    )
    require(
        (
            worksheet["pageid"],
            worksheet["revid"],
            worksheet["parentid"],
            worksheet["timestamp"],
            worksheet["mediawiki_sha1"],
            worksheet["wikitext_bytes"],
            worksheet["html_bytes"],
            worksheet["html_sha256"],
        )
        == (
            165942,
            1062659,
            1062658,
            "2025-12-19T12:06:03Z",
            "19554b41098b4f02ac6e558145036ca293e4bbc9",
            2059,
            53638,
            "77cd2292bea9b63d375ee75764d369bc543fb697f030cb8d6068ec3fbff6a2c6",
        ),
        "worksheet identity",
    )

    latex_expected = {
        "lecture": (
            165976,
            1033022,
            "3034e92c1843eab298fb5f6f859d2c89cf824d61",
            30809,
            "fe6c4e11e73c7449e98f396b9ae2ba23204cc28500bc4dd31352b3e9e03662f6",
            21754,
            "17aa88b5aa9a8d130f0995c036cb9ca332ef1b0feaef3b2d5ac5396e47b343a0",
        ),
        "worksheet": (
            166036,
            1033084,
            "3034e92c1843eab298fb5f6f859d2c89cf824d61",
            13695,
            "2c4229eeadf8d0b97de96e1fa3b85002c25aad436f4f4edd473c56a04f589e34",
            8243,
            "865905ee0d321006682c162fb2d9e272f1fc251e61b8dde9844981f6baba9c0f",
        ),
    }
    tex_records = {item["file"]: item for item in manifest["derived_expanded_tex"]}
    for kind, record in (
        ("lecture", manifest["lecture_latex_page"]),
        ("worksheet", manifest["worksheet_latex_page"]),
    ):
        expanded = tex_records[f"{kind}-23-expanded.tex"]
        expected = latex_expected[kind]
        require(
            (
                record["pageid"],
                record["revid"],
                record["mediawiki_sha1"],
                record["html_bytes"],
                record["html_sha256"],
                expanded["bytes"],
                expanded["sha256"],
            )
            == expected,
            f"{kind} /latex identity",
        )
        require(record["wikitext_bytes"] == 9, f"{kind} /latex launcher bytes")

    local_names: set[str] = set()
    local_bytes = 0
    for record in manifest["files"]:
        require(record["file"] not in local_names, "duplicate local manifest path")
        local_names.add(record["file"])
        verify_bound(OUT / record["file"], record["bytes"], record["sha256"])
        local_bytes += record["bytes"]
    observed_names = {
        path.name for path in OUT.iterdir() if path.is_file() and path.name != MANIFEST.name
    }
    require(observed_names == local_names, "local authority inventory differs from manifest")

    external_names: set[str] = set()
    external_bytes = 0
    for record in manifest["bounded_external_files"]:
        require(record["file"] not in external_names, "duplicate external manifest path")
        external_names.add(record["file"])
        verify_bound(ROOT / record["file"], record["bytes"], record["sha256"])
        external_bytes += record["bytes"]
    require(
        external_names
        == {
            "authority/ASSET_CLOSURE-unit-23.json",
            "authority/RIGHTS-unit-23.csv",
            "authority/artifacts/lecture-23-official.pdf",
            "authority/artifacts/worksheet-23-official.pdf",
        },
        "bounded external authority set",
    )

    lecture_closure = manifest["lecture_transclusion_closure"]
    worksheet_closure = manifest["worksheet_transclusion_closure"]
    require(lecture_closure["captured_page_count"] == 142, "lecture exact closure")
    require(worksheet_closure["captured_page_count"] == 102, "worksheet exact closure")
    require(lecture_closure["missing_page_count"] == worksheet_closure["missing_page_count"] == 0, "missing closure page")
    topology = manifest["transclusion_topology"]
    require(
        (
            topology["lecture"]["raw_parser_template_occurrences"],
            topology["lecture"]["unique_exact_parser_template_titles"],
            topology["lecture"]["unique_casefold_comparison_keys"],
        )
        == (142, 142, 141),
        "lecture title topology",
    )
    require(
        topology["lecture"]["casefold_title_collision_groups"]
        == [["MDLUL/Lineare Abbildung (Modul)", "MDLUL/lineare Abbildung (Modul)"]],
        "lecture case-sensitive title pair",
    )
    require(
        (
            topology["worksheet"]["raw_parser_template_occurrences"],
            topology["worksheet"]["unique_exact_parser_template_titles"],
            topology["worksheet"]["unique_casefold_comparison_keys"],
        )
        == (102, 102, 101),
        "worksheet title topology",
    )
    require(
        topology["worksheet"]["casefold_title_collision_groups"]
        == [["MDLUL/Kommutativer Ring", "MDLUL/kommutativer Ring"]],
        "worksheet case-sensitive title pair",
    )

    license_authority = manifest["source_course_license_authority"]
    require(license_authority["declared_license"] == "CC BY-SA 4.0", "course license")
    wrapper = license_authority["wrapper"]
    dependency = license_authority["validated_dependency"]
    require(
        (wrapper["pageid"], wrapper["revid"], wrapper["mediawiki_sha1"])
        == (166921, 1054579, "c914f4f47acd7cffab542e6ae29002aa9e5ced3e"),
        "license wrapper",
    )
    require(
        (dependency["pageid"], dependency["revid"], dependency["mediawiki_sha1"])
        == (102759, 1073083, "8e7f170511053c93b240f40db64466ea27a44116"),
        "license dependency",
    )
    require(
        license_authority["recursive_transclusion_closure"]["missing_page_count"] == 0,
        "license closure",
    )

    solutions = manifest["solutions"]
    require(solutions["exercise_count"] == 12 and solutions["solution_count"] == 2, "exercise/solution count")
    entries = solutions["entries"]
    require([entry["exercise_number"] for entry in entries] == list(range(1, 13)), "exercise order")
    expected_exercises = [
        (95498, 1083818, "1fa9d07f16a386ea4a61b06eae07ed375e787a3d"),
        (94471, 1083813, "3a73f507512c0371f00a7c4a49de17b760581377"),
        (21045, 1082164, "a82cf948adbb202df59623b987dcec60f7021b1d"),
        (95514, 1083785, "deba118f8b70dade2b19fb73c3355ec05c4ea2a2"),
        (95540, 1083673, "dde8354b1d96df83f9397a81d84a81dadf274054"),
        (20797, 1112488, "a791fbb7a7ecb784f1fa4755d30292a0defd3029"),
        (20892, 803939, "82e85f2d3228abd70c32c4f88a3129d4a2383563"),
        (20796, 1045806, "9a28148fc4843ac211fac6a81fdb3ae64b3a64e5"),
        (21046, 1083143, "904385c3accab6b410c6de90151c3b72e2bbb13d"),
        (20889, 985295, "6220fc907c1f38bf10778c7227d19b7abf8d4ebf"),
        (20893, 1106893, "edd275e7e969d1b4e186be3ea3efa1c194dc9868"),
        (20891, 1042655, "eb972c8766a92e15dd5e9023fc6d483a055ff9e4"),
    ]
    require(
        [(entry["exercise_pageid"], entry["exercise_revid"], entry["exercise_mediawiki_sha1"]) for entry in entries]
        == expected_exercises,
        "ordered exercise identities",
    )
    require([entry["role"] for entry in entries] == ["practice"] * 7 + ["submitted"] * 5, "role order")
    require([entry["authored_points"] for entry in entries] == [None, None, 2, 4, 4, 3, 2, 4, 3, 5, 5, 3], "authored points")
    require([entry["authored_subpoints"] for entry in entries] == [[], [], [], [], [2, 1, 1], [], [], [], [], [], [], []], "authored subpoints")
    require([entry["displayed_points"] for entry in entries] == [None] * 7 + [4, 3, 5, 5, 3], "displayed points")
    require(sum(entry["displayed_points"] or 0 for entry in entries) == 20, "displayed point total")
    public_numbers = [entry["exercise_number"] for entry in entries if entry["has_public_solution"]]
    require(public_numbers == [4, 5], "public solution set")
    require(
        [
            (entry["pageid"], entry["revid"], entry["mediawiki_sha1"], entry["wikitext_bytes"])
            for entry in entries
            if entry["has_public_solution"]
        ]
        == [
            (95515, 1090216, "ff517116601591c109925dcf590b9f084f006e99", 1680),
            (95541, 1096444, "b38570ced97626358cc493bfa56a140f114e1fdf", 1433),
        ],
        "solution identities",
    )
    solution_closures = manifest["solution_transclusion_closures"]
    require([item["exercise_number"] for item in solution_closures] == [4, 5], "solution closure order")
    require(
        [item["recursive_transclusion_closure"]["captured_page_count"] for item in solution_closures]
        == [19, 13],
        "solution closure sizes",
    )
    require(
        all(item["recursive_transclusion_closure"]["missing_page_count"] == 0 for item in solution_closures),
        "missing solution dependency",
    )
    require(all(not item["direct_wrapper_dependency_titles"] for item in solution_closures), "unexpected solution wrapper")

    expected_high_risk = [
        (20855, 1087697),
        (20860, 1086465),
        (18310, 1112317),
        (20801, 1101516),
        (20232, 1101012),
        (21026, 1101013),
        (50931, 1103183),
        (18360, 1101495),
        (20795, 978551),
        (95514, 1083785),
        (95515, 1090216),
        (95540, 1083673),
        (95541, 1096444),
        (20797, 1112488),
        (20893, 1106893),
    ]
    require(
        [(item["pageid"], item["revid"]) for item in manifest["high_risk_semantic_identity_bindings"]]
        == expected_high_risk,
        "high-risk identity bindings",
    )
    defects = manifest["source_defect_bindings"]
    require([item["id"] for item in defects] == [f"AGC-U23-SRC-{index:03d}" for index in range(1, 7)], "defect IDs")
    require([item["pageid"] for item in defects] == [20893, 95515, 95541, 20855, 20795, 18360], "defect pages")
    require("K × K" in defects[0]["counterexample"], "Ex11 counterexample")
    require("<n" in defects[1]["required_reader_repair"], "solution 4 repair")
    require("m_j" in defects[2]["required_reader_repair"], "solution 5 repair")
    require("m/m^2" in defects[3]["required_reader_repair"], "derivation quotient-class repair")
    require("monomial ideal" in defects[4]["required_reader_repair"], "monomial ideal interpretation")
    require("M_+" in defects[5]["required_reader_repair"], "summand-membership repair")

    with RIGHTS.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        rights_rows = list(reader)
        rights_header = reader.fieldnames
    require(rights_header is not None and len(rights_header) > 1 and rights_rows == [], "header-only rights ledger")
    closure = json.loads(CLOSURE.read_text(encoding="utf-8"))
    require(
        closure["unit"] == 23
        and closure["reader_media_positions"] == 0
        and closure["unique_local_assets"] == 0
        and closure["assets"] == [],
        "zero-media topology",
    )
    require(closure["rights_bytes"] == RIGHTS.stat().st_size and closure["rights_sha256"] == digest(RIGHTS), "rights binding")
    require(closure["component_discrepancies"]["worksheet_blank_page"]["page_number"] == 4, "blank worksheet page closure")

    pdfs = manifest["official_pdf_witnesses"]
    require([item["page_count"] for item in pdfs] == [7, 5], "PDF page counts")
    require(
        [item["local_sha256"] for item in pdfs]
        == [
            "96fc99009c2f4640ba99db6203c06bd59e03bdc2927c1bf81302625431302724",
            "6494630aba1d79f238c762b30cb382918444b19a82de3d96d66c4d6e3108d15b",
        ],
        "PDF byte identities",
    )
    require([item["commons_pageid"] for item in pdfs] == [182950524, 182948317], "Commons PDF page IDs")
    require([item["source_bytes"] for item in pdfs] == [191471, 159393], "Commons PDF sizes")
    require([item["mediawiki_sha1"] for item in pdfs] == ["49ac49a86f62182d8d9ca00310d16f7df4911d1e", "5fe6b3496a59f886e8779bb1d270977f86f4c4f0"], "Commons PDF SHA-1")
    require([item["blank_page_numbers"] for item in pdfs] == [[], [4]], "PDF blank-page topology")
    require([item["accessibility"]["extractable_text_characters"] for item in pdfs] == [10962, 4165], "PDF extractable text")
    require(all(not item["accessibility"]["tagged_pdf"] for item in pdfs), "PDF tagged state")
    require(all(not item["accessibility"]["structure_tree_present"] for item in pdfs), "PDF structure tree state")
    require([item["commons_description_revid"] for item in pdfs] == [1158248366, 1168719869], "Commons description revisions")
    require(
        [item["commons_description_mediawiki_sha1"] for item in pdfs]
        == ["ee06ff40e28a2a2d4a3d3e34ffbbf5a46c3d91cc", "43264b8f1626731b0598621f670b7fa4e74701ff"],
        "Commons description SHA-1",
    )
    expected_slots = [
        {
            "main": {"bytes": 321, "sha256": "c16cb0ecce8504d47c3503da380b9f0af05b18bf2dbfd82f7e81308680088559"},
            "mediainfo": {"bytes": 1706, "sha256": "e3182caa557e03ff020a17809f636f4b98e7b2f7e3bbb82fae96d0de7f14cc28"},
        },
        {
            "main": {"bytes": 327, "sha256": "9f5e5853adeaba6fa173a8a83d7fa2808dccaba300bed09428338f738b0935fe"},
            "mediainfo": {"bytes": 3143, "sha256": "50b945b267c15eb079b493c6cd91456b37a1bcf0dd20929ac0fe1bb8e57c1e16"},
        },
    ]
    require([item["commons_revision_slot_witnesses"] for item in pdfs] == expected_slots, "Commons slot witnesses")
    require(all(item["structured_license_claim"] == {"property": "P275", "item": "Q18199165", "meaning": "CC BY-SA 4.0"} for item in pdfs), "structured license claims")
    require(all(item["license_short"] == "CC BY-SA 4.0" for item in pdfs), "Commons PDF licenses")
    require(all(item["internal_pdf_boilerplate_label"] == "CC-by-sa 3.0" for item in pdfs), "stale PDF boilerplate evidence")
    require(any(page["pageid"] == 165912 for page in pdfs[0]["semantic_pages_newer_than_pdf"]), "lecture/PDF temporal discrepancy")
    require(any(page["pageid"] == 20797 for page in pdfs[1]["semantic_pages_newer_than_pdf"]), "worksheet/PDF temporal discrepancy")
    for item in pdfs:
        verify_bound(ROOT / item["local_path"], item["local_bytes"], item["local_sha256"])

    replay = manifest["final_live_identity_replay"]
    require(replay["result"] == "PASS", "final replay state")
    require(replay["wikiversity_identity_count"] == 208, "exact-title final replay count")
    require(sum(batch["title_count"] for batch in replay["wikiversity_batches"]) == 208, "final replay batches")
    require(replay["commons_pdf_identity_count"] == 2, "final Commons replay")

    freeze_text = FREEZE.read_text(encoding="utf-8")
    for needle in (
        "Exactly 12 exercises",
        "Only exercises 4 and 5",
        "page 4 is blank",
        "CC BY-SA 4.0",
        "208` unique Wikiversity",
        "AGC-U23-SRC-001",
        "AGC-U23-SRC-006",
    ):
        require(needle in freeze_text, f"freeze note missing: {needle}")

    receipt = {
        "schema": "ag-bridge-unit-authority-qa-v1",
        "result": "PASS",
        "unit": 23,
        "frozen_utc": manifest["frozen_utc"],
        "authority_manifest": {
            "path": MANIFEST.relative_to(ROOT).as_posix(),
            "bytes": MANIFEST.stat().st_size,
            "sha256": digest(MANIFEST),
        },
        "authority_freeze_note": {
            "path": FREEZE.relative_to(ROOT).as_posix(),
            "bytes": FREEZE.stat().st_size,
            "sha256": digest(FREEZE),
        },
        "qa_script": {
            "path": Path(__file__).resolve().relative_to(ROOT).as_posix(),
            "bytes": Path(__file__).stat().st_size,
            "sha256": digest(Path(__file__)),
        },
        "local_inventory": {"files": len(local_names), "bytes": local_bytes},
        "bounded_external_inventory": {"files": len(external_names), "bytes": external_bytes},
        "entry_revisions": {"lecture": lecture["revid"], "worksheet": worksheet["revid"]},
        "recursive_pages": {"lecture": 142, "worksheet": 102, "solutions": [19, 13], "missing": 0},
        "casefold_comparison_keys": {"lecture": 141, "worksheet": 101},
        "exercise_count": 12,
        "public_solution_numbers": public_numbers,
        "reader_media_positions": 0,
        "source_defect_ids": [item["id"] for item in defects],
        "official_pdf_pages": [7, 5],
        "worksheet_blank_page_numbers": [4],
        "final_live_identity_replay": {"wikiversity_exact_titles": 208, "commons_pdfs": 2},
        "checks": [
            "manifest_local_inventory_bytes_and_hashes",
            "bounded_external_inventory_bytes_and_hashes",
            "entry_latex_and_dynamic_tex_identities",
            "exact_case_sensitive_recursive_closure_identities",
            "course_cc_by_sa_4_license_closure",
            "ordered_exercise_roles_authored_and_displayed_points",
            "public_solution_identity_wrapper_and_dependency_closure",
            "high_risk_source_identity_and_defect_bindings",
            "header_only_rights_and_zero_media_closure",
            "official_pdf_bytes_pages_accessibility_slots_and_license_claims",
            "worksheet_blank_page_4_and_temporal_discrepancies",
            "captured_final_live_identity_replay",
            "durable_authority_freeze_note",
        ],
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "result": "PASS",
                "receipt": RECEIPT.relative_to(ROOT).as_posix(),
                "receipt_sha256": digest(RECEIPT),
                "manifest_sha256": digest(MANIFEST),
                "freeze_sha256": digest(FREEZE),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
