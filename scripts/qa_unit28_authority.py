#!/usr/bin/env python3
"""Fail-closed offline replay of the frozen Unit 28 authority boundary."""

from __future__ import annotations

import csv
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "authority"
UNIT = AUTH / "wikiversity" / "unit-28"
MANIFEST_PATH = UNIT / "UNIT_AUTHORITY_MANIFEST.json"
RIGHTS_PATH = AUTH / "RIGHTS-unit-28.csv"
CLOSURE_PATH = AUTH / "ASSET_CLOSURE-unit-28.json"
FREEZE_PATH = AUTH / "UNIT_28_AUTHORITY_FREEZE.md"
QA_PATH = ROOT / "qa" / "UNIT_28_AUTHORITY_QA.json"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def verify_bound(path: Path, expected: dict, label: str) -> None:
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular: {label}")
    require(path.stat().st_size == expected["bytes"], f"byte drift: {label}")
    require(digest(path) == expected["sha256"], f"hash drift: {label}")


def main() -> int:
    for path in (MANIFEST_PATH, RIGHTS_PATH, CLOSURE_PATH, FREEZE_PATH):
        require(path.is_file() and not path.is_symlink(), f"missing authority file: {path}")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    closure = json.loads(CLOSURE_PATH.read_text(encoding="utf-8"))

    require(manifest["schema"] == "brenner-unit-authority-freeze-v2", "manifest schema")
    require(manifest["unit_number"] == 28, "manifest unit")
    require(manifest["lecture"]["pageid"] == 50734 and manifest["lecture"]["revid"] == 1052516, "lecture identity")
    require(manifest["lecture"]["mediawiki_sha1"] == "d037d0173bca4c443e06c7991d830568fa8dc0ea", "lecture SHA-1")
    require(manifest["worksheet"]["pageid"] == 50763 and manifest["worksheet"]["revid"] == 793497, "worksheet identity")
    require(manifest["worksheet"]["mediawiki_sha1"] == "7ee8f07ea803541b23e8e1fa686c7b2c17e6f67a", "worksheet SHA-1")

    topology = manifest["transclusion_topology"]
    require(topology["lecture"]["with_root"] == 120, "lecture closure count")
    require(topology["lecture"]["canonical_identity_rows_sha256"] == "e5f7a370f948b4e1ab9cc663820569cfad9811bf7c9da88546995084059120cc", "lecture closure hash")
    require(topology["worksheet"]["with_root"] == 75, "worksheet closure count")
    require(topology["worksheet"]["canonical_identity_rows_sha256"] == "394da195ee18a8413830d80e0552ed4d71d69f04a83e952c594de3ab799249f5", "worksheet closure hash")

    solutions = manifest["solutions"]
    roles = solutions["ordered_role_point_and_star_topology"]
    require(solutions["exercise_count"] == 14 and solutions["solution_count"] == 1, "exercise/solution counts")
    require(solutions["negative_public_solution_evidence"]["negative_numbers"] == list(range(1, 10)) + list(range(11, 15)), "negative solution closure")
    require(roles["warm_up_numbers"] == list(range(1, 11)), "warm-up topology")
    require(roles["submitted_numbers"] == list(range(11, 15)), "submitted topology")
    require(roles["upload_numbers"] == [] and roles["starred_numbers"] == [10], "upload/star topology")
    require(roles["displayed_points"] == {"11": 3, "12": 4, "13": 3, "14": 3}, "displayed points")
    require(roles["submitted_displayed_point_total"] == 13, "displayed total")
    solution = manifest["public_solution_transclusion_closures"]
    require(len(solution) == 1 and solution[0]["exercise_number"] == 10, "public solution identity")
    require(solution[0]["solution_revid"] == 1112869 and solution[0]["solution_mediawiki_sha1"] == "85608d2ad2ee8515d39df596af6407dc0270b7f0", "solution root")
    require(solution[0]["topology"]["with_root"] == 8, "solution closure count")
    require(solution[0]["topology"]["canonical_identity_rows_sha256"] == "54c8c9c86a9e42371574b63eb8b25cfc84e0848f25a46e9fd81f48839ce0a619", "solution closure hash")

    replay = manifest["final_live_identity_replay"]
    require(replay["result"] == "PASS" and replay["semantic_unique_identity_count"] == 164, "semantic live replay")
    require(len(replay["semantic_batches"]) == 7 and sum(row["title_count"] for row in replay["semantic_batches"]) == 164, "semantic replay batches")
    require(replay["local_wikiversity_pdf_identity_count"] == 2 and replay["commons_media_identity_count"] == 4, "external live replay counts")

    local_inventory = {row["file"]: row for row in manifest["files"]}
    actual_local = {
        path.relative_to(UNIT).as_posix()
        for path in UNIT.rglob("*")
        if path.is_file() and path.name != MANIFEST_PATH.name
    }
    require(set(local_inventory) == actual_local, "manifest local inventory set")
    for relative, expected in local_inventory.items():
        verify_bound(UNIT / relative, expected, relative)
    for expected in manifest["bounded_external_files"]:
        verify_bound(ROOT / expected["file"], expected, expected["file"])

    require(closure["unit"] == 28 and closure["reader_media_positions"] == 4 and closure["unique_local_assets"] == 4, "media topology")
    expected_media = {
        "Soccerball.svg": (1311, "0405cfe3c75353882ffeecdbd4c8514bba49954482109c5f06f760d6a93b70e7", "image/svg+xml", "CC0"),
        "Torus_illustration.png": (150645, "f5c22545e3dbdf4e056c4439d63bdd41f029589893e178502d460576c44d78b7", "image/png", "Public domain"),
        "Double_torus_illustration.png": (266030, "1a7664a61899dd83245760b2842c6f1b8c2f18887bb507fdbc5405acd1d8a038", "image/png", "Public domain"),
        "Sphere_with_three_handles.png": (398740, "49398059697841332186226bccf87e46032289c1a8a02063fc2600070c51a311", "image/png", "Public domain"),
    }
    require([row["source_parser_name"] for row in closure["assets"]] == list(expected_media), "media order")
    for row in closure["assets"]:
        expected = expected_media[row["source_parser_name"]]
        path = ROOT / row["local_path"]
        witness = ROOT / row["authority_witness_path"]
        require(path.is_file() and witness.is_file() and path.read_bytes() == witness.read_bytes(), f"media witness: {row['source_parser_name']}")
        require((path.stat().st_size, digest(path), row["mime"], row["license_short"]) == expected, f"media identity/rights: {row['source_parser_name']}")
        if row["mime"] == "image/svg+xml":
            require(ET.parse(path).getroot().tag.endswith("svg") and row["frame_count"] == 1, "SVG validity")
        else:
            with Image.open(path) as image:
                image.verify()

    with RIGHTS_PATH.open(encoding="utf-8", newline="") as stream:
        rights = list(csv.DictReader(stream))
    require(len(rights) == 4, "rights row count")
    require(sum(row["license_short"] == "CC0" for row in rights) == 1, "CC0 rights route")
    require(sum(row["license_short"] == "Public domain" for row in rights) == 3, "public-domain rights route")

    pdf_rows = []
    expected_pdfs = {
        "lecture": (106537, "0d040f9a5663e6d0d7451f4de864a0712e35e08e961afc66d6742dfbee065609", 9),
        "worksheet": (45643, "579b29f1250b346549522aadc465f7afa0c67b012b5d7ba76b4c6eb0c94a5d12", 3),
    }
    for row in manifest["official_pdf_witnesses"]:
        path = ROOT / row["local_path"]
        expected = expected_pdfs[row["kind"]]
        require(path.is_file() and (path.stat().st_size, digest(path), len(PdfReader(str(path)).pages)) == expected, f"PDF identity: {row['kind']}")
        route = row["component_license_route"]
        require(route["current_print_version_notice"] == "CC BY-SA 4.0" and route["legacy_file_notice"] == "CC BY-SA 2.0 Germany", f"PDF rights: {row['kind']}")
        pdf_rows.append({"kind": row["kind"], "bytes": expected[0], "sha256": expected[1], "pages": expected[2]})

    receipt = {
        "schema": "ag-bridge-unit-authority-qa-v1",
        "unit": 28,
        "status": "PASS",
        "authority_manifest": {"path": MANIFEST_PATH.relative_to(ROOT).as_posix(), "bytes": MANIFEST_PATH.stat().st_size, "sha256": digest(MANIFEST_PATH)},
        "freeze_note": {"path": FREEZE_PATH.relative_to(ROOT).as_posix(), "bytes": FREEZE_PATH.stat().st_size, "sha256": digest(FREEZE_PATH)},
        "authority": {"lecture_closure_with_root": 120, "worksheet_closure_with_root": 75, "solution_closure_with_root": 8, "semantic_union": 164},
        "exercises": {"count": 14, "public_solutions": 1, "negative_candidates": 13, "starred": [10]},
        "media": {"positions": 4, "assets": 4, "cc0": 1, "public_domain": 3},
        "pdfs": pdf_rows,
        "rights": {"path": RIGHTS_PATH.relative_to(ROOT).as_posix(), "bytes": RIGHTS_PATH.stat().st_size, "sha256": digest(RIGHTS_PATH)},
        "asset_closure": {"path": CLOSURE_PATH.relative_to(ROOT).as_posix(), "bytes": CLOSURE_PATH.stat().st_size, "sha256": digest(CLOSURE_PATH)},
        "offline_inventory_files_verified": len(local_inventory) + len(manifest["bounded_external_files"]),
        "live_replay_witnesses_preserved": True,
        "provenance": "OpenAI Codex gpt-5.6-sol, Ultra.",
    }
    QA_PATH.parent.mkdir(parents=True, exist_ok=True)
    QA_PATH.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "receipt": QA_PATH.relative_to(ROOT).as_posix(), "bytes": QA_PATH.stat().st_size, "sha256": digest(QA_PATH)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
