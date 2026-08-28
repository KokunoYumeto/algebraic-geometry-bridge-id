#!/usr/bin/env python3
"""Fail-closed offline replay of the frozen Unit 29 authority boundary."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "authority"
UNIT = AUTH / "wikiversity" / "unit-29"
MANIFEST_PATH = UNIT / "UNIT_AUTHORITY_MANIFEST.json"
RIGHTS_PATH = AUTH / "RIGHTS-unit-29.csv"
CLOSURE_PATH = AUTH / "ASSET_CLOSURE-unit-29.json"
FREEZE_PATH = AUTH / "UNIT_29_AUTHORITY_FREEZE.md"
QA_PATH = ROOT / "qa" / "UNIT_29_AUTHORITY_QA.json"

PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."
SEMANTIC_LICENSE = "CC BY-SA 4.0"
LEGACY_PDF_LICENSE = "CC BY-SA 2.0 Germany"
COURSE_TITLE = "Kurs:Algebraische Kurven (Osnabrück 2012)"
LECTURE_TITLE = f"{COURSE_TITLE}/Vorlesung 29"
WORKSHEET_TITLE = f"{COURSE_TITLE}/Arbeitsblatt 29"
IDENTITY_FIELDS = (
    "title",
    "pageid",
    "revid",
    "parentid",
    "timestamp",
    "mediawiki_sha1",
    "wikitext_bytes",
)

EXPECTED_ROOTS = {
    "course": {
        "title": COURSE_TITLE,
        "pageid": 50687,
        "revid": 658236,
        "parentid": 439529,
        "timestamp": "2020-09-24T11:56:43Z",
        "mediawiki_sha1": "2f2ede7249fcaa55ba17d9cd0e3d9ee9d4941f0c",
        "wikitext_bytes": 619,
    },
    "lecture": {
        "title": LECTURE_TITLE,
        "pageid": 51996,
        "revid": 1069408,
        "parentid": 833971,
        "timestamp": "2026-02-05T19:18:37Z",
        "mediawiki_sha1": "6f0742211aeb307841634425937aad9037da51be",
        "wikitext_bytes": 3224,
    },
    "worksheet": {
        "title": WORKSHEET_TITLE,
        "pageid": 50924,
        "revid": 1052757,
        "parentid": 793498,
        "timestamp": "2025-08-27T18:11:31Z",
        "mediawiki_sha1": "0e8dd5d1e5b9bf9552bdbd8f8c61c47ee2a0b726",
        "wikitext_bytes": 1692,
    },
    "lecture_latex": {
        "title": f"{LECTURE_TITLE}/latex",
        "pageid": 53378,
        "revid": 806127,
        "parentid": 796347,
        "timestamp": "2022-09-18T07:15:22Z",
        "mediawiki_sha1": "1d092e4f15139d9908d36c4d64a1f4fde570e1ba",
        "wikitext_bytes": 9,
    },
    "worksheet_latex": {
        "title": f"{WORKSHEET_TITLE}/latex",
        "pageid": 53022,
        "revid": 806095,
        "parentid": 796314,
        "timestamp": "2022-09-18T07:10:12Z",
        "mediawiki_sha1": "1d092e4f15139d9908d36c4d64a1f4fde570e1ba",
        "wikitext_bytes": 9,
    },
}

EXPECTED_EXPANDED_TEX = {
    "lecture-29-expanded.tex": (
        23292,
        "7c06a1dbb12904bd5f89427955ef8bdae5781e402522cd70f09a0c6e1ef1e784",
    ),
    "worksheet-29-expanded.tex": (
        5439,
        "53a54b5b7e59be71c94d41dc791021c0b2d6165bf0b489670800b09387d560d2",
    ),
}

EXPECTED_CLOSURES = {
    "lecture": (
        106,
        107,
        "87f4ba1e8fb06c51346d5d8fbb105bf2c48e7242a9de2e387906f9608380308b",
    ),
    "worksheet": (
        61,
        62,
        "4b6d796d4888b94cfaa1c29811b60ea012118af4af993efd3fd4f23bc5f1229a",
    ),
    "solution-02": (
        16,
        17,
        "baafc7ca56b87391f988b7f9b03bf7a4098109451b94b2cec1817fdf0fdb0f86",
    ),
    "solution-03": (
        7,
        8,
        "efe168f6a9cec88cc0a21f4e31656747feff0f79c1d6cb30552e615ea9400cd8",
    ),
}

EXPECTED_EXERCISES = [
    (
        1,
        "Projektive ebene Kurve/Schnitt mit projektiver Geraden/Algebraisch abgeschlossen/Nicht leer/Aufgabe",
        False,
        "warm-up",
        2,
        None,
        False,
        21282,
        847242,
        785422,
        "2022-09-25T21:02:14Z",
        "af4eee45b9d06c71f8780f99e66cf7c9a806030b",
        510,
    ),
    (
        2,
        "Ebene algebraische Kurven/Z mod 5/Einheitskreis und x^3-2y^2+3/Durchschnitt und unendlich ferne Punkte/Aufgabe",
        True,
        "warm-up",
        4,
        None,
        True,
        21302,
        1072843,
        1041212,
        "2026-02-21T09:35:16Z",
        "a2878affd52e5e91234fe225d14e384d74e5d85c",
        1072,
    ),
    (
        3,
        "Projektive Gerade/K-Punkte/Lokale Ringe isomorph/Aufgabe",
        True,
        "warm-up",
        3,
        None,
        True,
        21572,
        1083904,
        1047305,
        "2026-05-29T22:23:43Z",
        "a313e73f4e0c6bcfdfbfb354200ed967160a5c53",
        480,
    ),
    (
        4,
        "Lemniskate/Projektive Punkte/Aufgabe",
        False,
        "warm-up",
        3,
        None,
        False,
        21168,
        1083303,
        1043132,
        "2026-05-29T20:45:53Z",
        "2df5915eb9529a40d7a8aa6716ecdb1bb1122124",
        571,
    ),
    (
        5,
        "Algebraische Kurve/ZX^2 ist Y^3/Charakteristik null/Singuläre Punkte und Parametrisierung/Aufgabe",
        False,
        "warm-up",
        4,
        None,
        False,
        16956,
        1043872,
        1022886,
        "2025-08-12T20:33:28Z",
        "c6fc454f13201cf6105865fd19ba7c5dfa16f691",
        1166,
    ),
    (
        6,
        "Projektive Abbildung/Morphismus durch homogenen Polynome vom gleichen Grad/Auf offener Menge/Aufgabe",
        False,
        "submitted",
        3,
        3,
        False,
        21333,
        1098945,
        1083901,
        "2026-06-15T17:15:54Z",
        "82739289f53a2c98c6b0319410e4ebeb0a290857",
        858,
    ),
    (
        7,
        "Projektiver Raum/Projektion weg von beliebigem Punkt/Matrixbeschreibung/Aufgabe",
        False,
        "submitted",
        3,
        3,
        False,
        21223,
        1098952,
        1083918,
        "2026-06-15T17:17:04Z",
        "c5f5ce2e9115bc6919c8370da4f87b5dc7da7c74",
        871,
    ),
    (
        8,
        "Tschirnhausen Kubik/Projektive Punkte/Aufgabe",
        False,
        "submitted",
        3,
        3,
        False,
        21164,
        787111,
        541421,
        "2022-08-22T13:17:34Z",
        "853a82feb307c59ab807f3d94996a00263c6ca62",
        542,
    ),
    (
        9,
        "Kartesisches Blatt/Projektive Punkte/Aufgabe",
        False,
        "submitted",
        3,
        3,
        False,
        21166,
        1042321,
        858058,
        "2025-08-12T16:21:05Z",
        "4d38e5aa034cb507a72e9c5ed210448dd6d205bf",
        636,
    ),
    (
        10,
        "Lemniskate von Bernoulli/Projektiv/Abbildung auf Quadrik/Aufgabe",
        False,
        "submitted",
        5,
        5,
        False,
        21170,
        1043128,
        985607,
        "2025-08-12T18:29:36Z",
        "ea825e7dfce478fe6a6c17380060ee7a0bca3771",
        598,
    ),
]

EXPECTED_SOLUTION_ROOTS = {
    2: {
        "title": EXPECTED_EXERCISES[1][1] + "/Lösung",
        "pageid": 21303,
        "revid": 1094621,
        "parentid": 1089317,
        "timestamp": "2026-06-14T16:25:59Z",
        "mediawiki_sha1": "859801fc5d0e4bb16dd1ec72b7af1873ab2f2a4a",
        "wikitext_bytes": 2307,
    },
    3: {
        "title": EXPECTED_EXERCISES[2][1] + "/Lösung",
        "pageid": 21573,
        "revid": 1090273,
        "parentid": 959539,
        "timestamp": "2026-05-31T12:45:13Z",
        "mediawiki_sha1": "f0359ee4a15f70916cf5443ab14890f3ac8207dc",
        "wikitext_bytes": 812,
    },
}

EXPECTED_MEDIA = [
    {
        "source_parser_name": "Lemniscate_of_Bernoulli.svg",
        "metadata_title": "File:Lemniscate of Bernoulli.svg",
        "description_pageid": 4285176,
        "description_revid": 512182780,
        "description_parentid": 141013849,
        "description_timestamp": "2020-11-12T15:39:26Z",
        "description_mediawiki_sha1": "f8b8f0465e1f7c5ef3e88ad85e99456ce3d01b24",
        "description_wikitext_bytes": 368,
        "source_timestamp": "2010-09-18T22:36:31Z",
        "source_bytes": 1087,
        "source_sha1": "9c474e2a9ed86aaa7d5a700d311c13b4a05866de",
        "source_url": "https://upload.wikimedia.org/wikipedia/commons/e/ef/Lemniscate_of_Bernoulli.svg",
        "selected_url": "https://upload.wikimedia.org/wikipedia/commons/e/ef/Lemniscate_of_Bernoulli.svg",
        "selected_form": "original",
        "original_locally_archived": True,
        "original_bytes": 1087,
        "original_sha1": "9c474e2a9ed86aaa7d5a700d311c13b4a05866de",
        "original_width": 800,
        "original_height": 300,
        "local_path": "authority/assets/Lemniscate_of_Bernoulli.svg",
        "local_bytes": 1087,
        "local_sha256": "3e1753bdbf9a9e0068892d1c10c445c104033e2a100d2d0b68f349fc8e1324f4",
        "authority_witness_path": "authority/wikiversity/unit-29/assets/Lemniscate_of_Bernoulli.svg",
        "authority_witness_bytes": 1087,
        "authority_witness_sha256": "3e1753bdbf9a9e0068892d1c10c445c104033e2a100d2d0b68f349fc8e1324f4",
        "width": 800,
        "height": 300,
        "frame_count": 1,
        "mime": "image/svg+xml",
        "license_short": "Public domain",
        "course_credit_user": "Zorgit",
        "course_credit_repository": "Commons",
        "course_credit_license_label": "PD",
    },
    {
        "source_parser_name": "Tschirnhausen_cubic.png",
        "metadata_title": "File:Tschirnhausen cubic.png",
        "description_pageid": 2408689,
        "description_revid": 1134413486,
        "description_parentid": 1124033583,
        "description_timestamp": "2025-12-21T08:02:34Z",
        "description_mediawiki_sha1": "457e538f54b1164ad87f7b6db252b1c4541edfee",
        "description_wikitext_bytes": 2240,
        "source_timestamp": "2007-07-14T16:31:30Z",
        "source_bytes": 64767,
        "source_sha1": "44a9bbaa597b2fce69ca491335199890546cfb3d",
        "source_url": "https://upload.wikimedia.org/wikipedia/commons/2/26/Tschirnhausen_cubic.png",
        "selected_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Tschirnhausen_cubic.png/500px-Tschirnhausen_cubic.png",
        "selected_form": "thumbnail_500px",
        "original_locally_archived": False,
        "original_bytes": 64767,
        "original_sha1": "44a9bbaa597b2fce69ca491335199890546cfb3d",
        "original_width": 1100,
        "original_height": 1638,
        "local_path": "authority/assets/Tschirnhausen_cubic-500.png",
        "local_bytes": 83502,
        "local_sha256": "f3dda9da65db9e431f25ea77eb83f51aed2eff1c191dc1206e0759561ee613c7",
        "authority_witness_path": "authority/wikiversity/unit-29/assets/Tschirnhausen_cubic-500.png",
        "authority_witness_bytes": 83502,
        "authority_witness_sha256": "f3dda9da65db9e431f25ea77eb83f51aed2eff1c191dc1206e0759561ee613c7",
        "width": 500,
        "height": 745,
        "frame_count": 1,
        "mime": "image/png",
        "license_short": "Public domain",
        "course_credit_user": "Oleg Alexandrov",
        "course_credit_repository": "Commons",
        "course_credit_license_label": "PD",
    },
]

EXPECTED_PDFS = {
    "lecture": {
        "source_file_title": "Datei:Algebraische Kurven (Osnabrück 2012)Vorlesung29.pdf",
        "file_pageid": 53379,
        "file_revid": 325148,
        "file_parentid": 322248,
        "file_timestamp": "2012-08-02T10:21:15Z",
        "file_mediawiki_sha1": "dc79a72b6f301293f130cdeb82cbbd60b6debe51",
        "file_wikitext_bytes": 72,
        "source_timestamp": "2012-08-02T10:21:15Z",
        "source_bytes": 84904,
        "source_sha1": "23eed466fa4d6473efd9143cd72f2eb319eeac31",
        "mime": "application/pdf",
        "media_type": "OFFICE",
        "local_path": "authority/artifacts/lecture-29-official.pdf",
        "local_bytes": 84904,
        "local_sha256": "9f7082c66d493cd02a6e4f0579493ad1ba74ddec4b3777517c9ab6daa9610c6d",
        "page_count": 6,
    },
    "worksheet": {
        "source_file_title": "Datei:Algebraische Kurven (Osnabrück 2012)Arbeitsblatt29.pdf",
        "file_pageid": 54374,
        "file_revid": 325018,
        "file_parentid": 322184,
        "file_timestamp": "2012-07-31T14:08:29Z",
        "file_mediawiki_sha1": "290ec63705242e2b8dccf596ed48a8d1adac9880",
        "file_wikitext_bytes": 75,
        "source_timestamp": "2012-07-31T14:08:29Z",
        "source_bytes": 81522,
        "source_sha1": "6a783df1c478e4644df12cbbe8db164d9f84076a",
        "mime": "application/pdf",
        "media_type": "OFFICE",
        "local_path": "authority/artifacts/worksheet-29-official.pdf",
        "local_bytes": 81522,
        "local_sha256": "83986d2a9928c6e61ad7afa6d5a890e2b296c15a8706931c8c6da485b05079d2",
        "page_count": 3,
    },
}

EXPECTED_SOURCE_DEFECTS = [
    {
        "id": "AGC-U29-SRC-001",
        "surface": "lecture current semantic source / expanded TeX",
        "source_text": "Bei g >= 3 ist die Multiplizität >= 2",
        "issue": (
            "The proof of the degree-d graph theorem switches from d to an "
            "undefined g in its final singularity criterion."
        ),
        "reader_handling": (
            "Render d >= 3, label the correction visibly, and retain this exact source binding."
        ),
    },
    {
        "id": "AGC-U29-SRC-002",
        "surface": "worksheet Exercise 7 current semantic source / expanded TeX",
        "source_text": (
            "durch die Matrix [blank] ... (x_0,...,x_n) maps to (x_0,...,x_n)"
        ),
        "issue": (
            "The requested projection matrix is blank and the displayed map repeats "
            "the input vector instead of giving the projection."
        ),
        "reader_handling": (
            "Preserve the unresolved source surface and disclose it; do not invent a "
            "matrix or silently repair the exercise."
        ),
    },
]

EXPECTED_EXTERNAL_PATHS = {
    "authority/ASSET_CLOSURE-unit-29.json",
    "authority/RIGHTS-unit-29.csv",
    "authority/artifacts/lecture-29-official.pdf",
    "authority/artifacts/worksheet-29-official.pdf",
    "authority/assets/Lemniscate_of_Bernoulli.svg",
    "authority/assets/Tschirnhausen_cubic-500.png",
}


def digest(path: Path, algorithm: str = "sha256") -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def safe_relative(value: object, label: str) -> PurePosixPath:
    require(isinstance(value, str) and value != "", f"invalid path value: {label}")
    require("\\" not in value and "\x00" not in value and ":" not in value, f"unsafe path spelling: {label}")
    relative = PurePosixPath(value)
    require(not relative.is_absolute(), f"absolute path rejected: {label}")
    require(relative.parts and all(part not in ("", ".", "..") for part in relative.parts), f"path traversal rejected: {label}")
    require(relative.as_posix() == value, f"noncanonical path rejected: {label}")
    return relative


def regular_path(base: Path, value: object, label: str) -> Path:
    relative = safe_relative(value, label)
    path = base.joinpath(*relative.parts)
    current = base
    for part in relative.parts:
        current = current / part
        require(not current.is_symlink(), f"symlink rejected: {label}")
    require(path.is_file(), f"missing/nonregular file: {label}")
    return path


def verify_bound(path: Path, expected: dict, label: str) -> None:
    require(path.is_file() and not path.is_symlink(), f"missing/nonregular: {label}")
    require(path.stat().st_size == int(expected["bytes"]), f"byte drift: {label}")
    require(digest(path) == expected["sha256"], f"hash drift: {label}")


def identity(record: dict) -> dict:
    return {
        "title": record["title"],
        "pageid": int(record["pageid"]),
        "revid": int(record["revid"]),
        "parentid": int(record.get("parentid", 0)),
        "timestamp": record["timestamp"],
        "mediawiki_sha1": record["mediawiki_sha1"],
        "wikitext_bytes": int(record["wikitext_bytes"]),
    }


def require_identity(record: dict, expected: dict, label: str) -> None:
    require(identity(record) == expected, f"identity drift: {label}")


def identity_hash(records: list[dict]) -> str:
    rows = sorted((identity(item) for item in records), key=lambda row: (row["title"], row["pageid"]))
    raw = json.dumps(
        rows,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def solution_root(record: dict) -> dict:
    return {
        "title": record["solution_title"],
        "pageid": record["solution_pageid"],
        "revid": record["solution_revid"],
        "parentid": record["solution_parentid"],
        "timestamp": record["solution_timestamp"],
        "mediawiki_sha1": record["solution_mediawiki_sha1"],
        "wikitext_bytes": record["solution_wikitext_bytes"],
    }


def verify_closure(
    label: str,
    root: dict,
    closure: dict,
    topology: dict,
) -> list[dict]:
    dependencies, with_root, expected_hash = EXPECTED_CLOSURES[label]
    pages = closure["pages"]
    require(closure["captured_page_count"] == dependencies, f"captured closure count: {label}")
    require(closure["missing_page_count"] == 0, f"missing closure page: {label}")
    require(len(pages) == dependencies, f"closure list count: {label}")
    require(len({(row["title"], int(row["pageid"])) for row in pages}) == len(pages), f"duplicate closure identity: {label}")
    records = [root, *pages]
    observed_hash = identity_hash(records)
    require(len(records) == with_root, f"root-plus-closure count: {label}")
    require(observed_hash == expected_hash, f"case-sensitive canonical closure hash: {label}")
    require(topology["dependencies"] == dependencies, f"manifest dependency topology: {label}")
    require(topology["with_root"] == with_root, f"manifest closure topology: {label}")
    require(topology["unique_exact_titles"] == dependencies, f"manifest unique title topology: {label}")
    require(topology["parser_template_occurrences"] == dependencies, f"manifest parser topology: {label}")
    require(topology["duplicate_exact_titles"] == [], f"manifest duplicate title topology: {label}")
    require(topology["canonical_identity_rows_sha256"] == expected_hash, f"manifest closure hash: {label}")
    algorithm = topology["canonical_identity_hash_algorithm"]
    require("rows sorted by (title,pageid)" in algorithm and "ensure_ascii=false" in algorithm, f"canonical closure algorithm: {label}")
    return records


def verify_inventory(manifest: dict) -> int:
    rows = manifest["files"]
    require(isinstance(rows, list), "manifest local inventory type")
    paths = [row.get("file") for row in rows]
    require(len(paths) == len(set(paths)), "duplicate manifest local inventory path")
    for path in UNIT.rglob("*"):
        require(not path.is_symlink(), f"symlink inside Unit 29 authority tree: {path.relative_to(UNIT)}")
    actual = {
        path.relative_to(UNIT).as_posix()
        for path in UNIT.rglob("*")
        if path.is_file() and path.name != MANIFEST_PATH.name
    }
    require(set(paths) == actual, "missing/extra local authority inventory")
    for row in rows:
        path = regular_path(UNIT, row["file"], f"local inventory {row['file']}")
        verify_bound(path, row, row["file"])

    external_rows = manifest["bounded_external_files"]
    require(isinstance(external_rows, list), "manifest external inventory type")
    external_paths = [row.get("file") for row in external_rows]
    require(len(external_paths) == len(set(external_paths)), "duplicate manifest external inventory path")
    require(set(external_paths) == EXPECTED_EXTERNAL_PATHS, "missing/extra bounded external inventory")
    for row in external_rows:
        path = regular_path(ROOT, row["file"], f"external inventory {row['file']}")
        verify_bound(path, row, row["file"])
    return len(rows) + len(external_rows)


def verify_exercises(manifest: dict) -> tuple[list[dict], list[dict]]:
    solutions = manifest["solutions"]
    require(solutions["schema"] == "brenner-worksheet-solution-map-v2", "solution-map schema")
    require(solutions["unit"] == 29, "solution-map unit")
    require(solutions["exercise_count"] == 10 and solutions["solution_count"] == 2, "exercise/solution counts")
    entries = solutions["entries"]
    require(len(entries) == len(EXPECTED_EXERCISES), "ordered exercise count")
    for entry, expected in zip(entries, EXPECTED_EXERCISES, strict=True):
        (
            number,
            title,
            has_solution,
            role,
            authored_points,
            displayed_points,
            starred,
            pageid,
            revid,
            parentid,
            timestamp,
            mediawiki_sha1,
            wikitext_bytes,
        ) = expected
        observed = (
            entry["exercise_number"],
            entry["exercise_title"],
            entry["has_public_solution"],
            entry["role"],
            entry["authored_points"],
            entry["displayed_points"],
            entry["starred_in_worksheet"],
            entry["exercise_pageid"],
            entry["exercise_revid"],
            entry["exercise_parentid"],
            entry["exercise_timestamp"],
            entry["exercise_mediawiki_sha1"],
            entry["exercise_wikitext_bytes"],
        )
        require(observed == expected, f"ordered exercise identity/topology: {number}")
        require(entry["solution_title"] == title + "/Lösung", f"solution candidate title: {number}")
        require(entry["points_displayed_in_worksheet"] == (number >= 6), f"displayed-point flag: {number}")
        if has_solution:
            expected_solution = EXPECTED_SOLUTION_ROOTS[number]
            observed_solution = {
                "title": entry["solution_title"],
                "pageid": entry["pageid"],
                "revid": entry["revid"],
                "parentid": entry["parentid"],
                "timestamp": entry["timestamp"],
                "mediawiki_sha1": entry["mediawiki_sha1"],
                "wikitext_bytes": entry["wikitext_bytes"],
            }
            require(observed_solution == expected_solution, f"solution map positive identity: {number}")

    roles = solutions["ordered_role_point_and_star_topology"]
    require(roles["warm_up_numbers"] == [1, 2, 3, 4, 5], "warm-up topology")
    require(roles["submitted_numbers"] == [6, 7, 8, 9, 10], "submitted topology")
    require(roles["upload_numbers"] == [], "upload topology")
    require(roles["authored_points"] == {str(number): points for number, points in enumerate([2, 4, 3, 3, 4, 3, 3, 3, 3, 5], start=1)}, "authored-point topology")
    require(roles["displayed_points"] == {"6": 3, "7": 3, "8": 3, "9": 3, "10": 5}, "displayed-point topology")
    require(roles["submitted_displayed_point_total"] == 17, "displayed-point total")
    require(roles["starred_numbers"] == [2, 3], "star topology")

    negative = solutions["negative_public_solution_evidence"]
    require(negative["exact_candidate_title_count"] == 10, "solution-candidate topology")
    require(negative["positive_numbers"] == [2, 3], "positive solution topology")
    require(negative["negative_numbers"] == [1, 4, 5, 6, 7, 8, 9, 10], "negative solution topology")
    require(negative["negative_count"] == 8 and len(negative["entries"]) == 8, "negative solution count")
    require([row["exercise_number"] for row in negative["entries"]] == negative["negative_numbers"], "ordered negative solution evidence")
    require(all(row["api_missing"] is True for row in negative["entries"]), "negative solution missing flags")

    public = manifest["public_solution_transclusion_closures"]
    require([row["exercise_number"] for row in public] == [2, 3], "public solution closure order")
    solution_records: list[dict] = []
    for record in public:
        number = record["exercise_number"]
        root = solution_root(record)
        require(root == EXPECTED_SOLUTION_ROOTS[number], f"public solution root: {number}")
        records = verify_closure(
            f"solution-{number:02d}",
            root,
            record["recursive_transclusion_closure"],
            record["topology"],
        )
        solution_records.extend(records)
    return entries, solution_records


def verify_media(manifest: dict, closure: dict) -> list[dict]:
    require(closure["schema"] == "brenner-unit-media-closure-v2" and closure["unit"] == 29, "media closure identity")
    require(closure["authority_only_boundary"] is True, "media authority-only boundary")
    require(closure["reader_media_positions"] == 2 and closure["unique_local_assets"] == 2, "media topology")
    require(closure["animated_html_positions"] == 0, "animated-media topology")
    expected_names = [row["source_parser_name"] for row in EXPECTED_MEDIA]
    require(closure["reader_media_order"] == expected_names, "closure media order")
    require(closure["accessibility"]["reader_media_alt_or_caption_required"] is True, "media accessibility contract")
    require(closure["accessibility"]["reader_media_source_names"] == expected_names, "media accessibility order")
    require(closure["official_pdf_witnesses_are_not_media_positions"] is True, "PDF/media position separation")

    assets = closure["assets"]
    manifest_assets = manifest["images"]["substantive_assets"]
    require(manifest["images"]["reader_media_positions"] == 2, "manifest media positions")
    require(len(assets) == len(manifest_assets) == 2, "media asset count")
    require([row["source_parser_name"] for row in assets] == expected_names, "media order")
    require(len({row["source_parser_name"] for row in assets}) == 2, "duplicate media name")
    require(len({row["local_path"] for row in assets}) == 2, "duplicate media local path")

    for order, (row, manifest_row, expected) in enumerate(zip(assets, manifest_assets, EXPECTED_MEDIA, strict=True), start=1):
        require(row == manifest_row, f"manifest/closure media disagreement: {expected['source_parser_name']}")
        require(row["reader_order"] == order and row["asset_id"] == f"br-ak-u29-media-{order:03d}", f"media stable ID/order: {order}")
        for key, value in expected.items():
            require(row[key] == value, f"media identity/rights drift: {expected['source_parser_name']}:{key}")
        shared = regular_path(ROOT, row["local_path"], f"media shared path {row['source_parser_name']}")
        witness = regular_path(ROOT, row["authority_witness_path"], f"media witness path {row['source_parser_name']}")
        require(shared.read_bytes() == witness.read_bytes(), f"media witness byte identity: {row['source_parser_name']}")
        require((shared.stat().st_size, digest(shared)) == (expected["local_bytes"], expected["local_sha256"]), f"media local bytes: {row['source_parser_name']}")
        if expected["original_locally_archived"]:
            require(digest(shared, "sha1") == expected["source_sha1"], f"archived original SHA-1: {row['source_parser_name']}")
        else:
            require(shared.stat().st_size != expected["source_bytes"], f"thumbnail/original byte separation: {row['source_parser_name']}")
        if row["mime"] == "image/svg+xml":
            require(ET.parse(shared).getroot().tag.endswith("svg"), "Lemniscate SVG validity")
        else:
            with Image.open(shared) as image:
                require((image.width, image.height) == (expected["width"], expected["height"]), f"media dimensions: {row['source_parser_name']}")
                image.verify()

    with RIGHTS_PATH.open(encoding="utf-8", newline="") as stream:
        rights = list(csv.DictReader(stream))
    require(len(rights) == 2, "rights row count")
    require([row["resource_title"].removeprefix("File:") for row in rights] == expected_names, "rights media order")
    require(all(row["license_short"] == "Public domain" for row in rights), "public-domain rights route")
    for rights_row, expected in zip(rights, EXPECTED_MEDIA, strict=True):
        require(rights_row["local_path"] == expected["local_path"], f"rights local path: {expected['source_parser_name']}")
        require(int(rights_row["local_bytes"]) == expected["local_bytes"], f"rights byte count: {expected['source_parser_name']}")
        require(rights_row["local_sha256"] == expected["local_sha256"], f"rights SHA-256: {expected['source_parser_name']}")
        require(rights_row["original_url"] == expected["source_url"], f"rights original URL: {expected['source_parser_name']}")
        require(rights_row["selected_url"] == expected["selected_url"], f"rights selected URL: {expected['source_parser_name']}")
        require(rights_row["selected_form"] == expected["selected_form"], f"rights selected form: {expected['source_parser_name']}")
        require(rights_row["original_locally_archived"].casefold() == str(expected["original_locally_archived"]).casefold(), f"rights original archive state: {expected['source_parser_name']}")
        require(int(rights_row["original_bytes"]) == expected["original_bytes"], f"rights original bytes: {expected['source_parser_name']}")
        require(rights_row["original_sha1"] == expected["original_sha1"], f"rights original SHA-1: {expected['source_parser_name']}")
        require((int(rights_row["original_width"]), int(rights_row["original_height"])) == (expected["original_width"], expected["original_height"]), f"rights original dimensions: {expected['source_parser_name']}")
        require((int(rights_row["local_width"]), int(rights_row["local_height"])) == (expected["width"], expected["height"]), f"rights selected dimensions: {expected['source_parser_name']}")
        require(int(rights_row["description_pageid"]) == expected["description_pageid"], f"rights description page: {expected['source_parser_name']}")
        require(int(rights_row["description_revid"]) == expected["description_revid"], f"rights description revision: {expected['source_parser_name']}")
        require(rights_row["description_mediawiki_sha1"] == expected["description_mediawiki_sha1"], f"rights description SHA-1: {expected['source_parser_name']}")
        require(rights_row["source_course_license"] == SEMANTIC_LICENSE, f"rights semantic route: {expected['source_parser_name']}")

    discrepancies = closure["component_discrepancies"]["media_semantic_description"]
    require([row["source_parser_name"] for row in discrepancies] == ["Tschirnhausen_cubic.png", "Lemniscate_of_Bernoulli.svg"], "media discrepancy topology")
    require("not the Tschirnhausen cubic" in discrepancies[0]["current_commons_description"], "Tschirnhausen identification warning")
    require(discrepancies[1]["current_commons_artist"] == "Zorgit", "Lemniscate artist provenance")
    require(discrepancies[1]["current_file_uploader"] == "Georg-Johann", "Lemniscate uploader provenance")
    retrieval = closure["component_discrepancies"]["original_media_retrieval"]
    require(retrieval["source_parser_name"] == "Tschirnhausen_cubic.png", "thumbnail fallback component")
    require(retrieval["original_identity_status"] == "metadata-bound from the frozen Commons description/imageinfo revision", "thumbnail fallback original identity")
    require(retrieval["original_local_archive_status"] == "not archived at this boundary after the canonical original endpoint returned HTTP 429", "thumbnail fallback archive disclosure")
    require(retrieval["selected_reader_derivative"] == "official Wikimedia 500px thumbnail, byte-bound in the asset records", "thumbnail fallback selected derivative")
    return assets


def verify_pdfs(manifest: dict, closure: dict) -> list[dict]:
    rows = manifest["official_pdf_witnesses"]
    require([row["kind"] for row in rows] == ["lecture", "worksheet"], "exact PDF kinds/order")
    require(len({row["kind"] for row in rows}) == 2, "duplicate PDF kind")
    closure_rights = {row["source_file_title"]: row for row in closure["official_pdf_component_rights"]}
    require(len(closure_rights) == 2, "PDF closure rights count")
    receipt_rows = []
    for row in rows:
        kind = row["kind"]
        expected = EXPECTED_PDFS[kind]
        for key, value in expected.items():
            require(row[key] == value, f"PDF identity drift: {kind}:{key}")
        path = regular_path(ROOT, row["local_path"], f"official PDF {kind}")
        require((path.stat().st_size, digest(path), digest(path, "sha1")) == (expected["local_bytes"], expected["local_sha256"], expected["source_sha1"]), f"PDF bytes/hashes: {kind}")
        reader = PdfReader(str(path))
        require(not reader.is_encrypted and len(reader.pages) == expected["page_count"], f"PDF validity/page count: {kind}")
        route = row["component_license_route"]
        require(route["current_print_version_notice"] == SEMANTIC_LICENSE, f"PDF current license: {kind}")
        require(route["legacy_file_notice"] == LEGACY_PDF_LICENSE, f"PDF legacy license: {kind}")
        require(route["current_notice_evidence"] == f"{kind}-29-file-description.html", f"PDF current-license evidence: {kind}")
        require(route["legacy_notice_evidence"] == f"{kind}-29-file-description.html", f"PDF legacy-license evidence: {kind}")
        require(closure_rights[row["source_file_title"]]["component_license_route"] == route, f"PDF closure rights route: {kind}")
        receipt_rows.append({"kind": kind, "bytes": expected["local_bytes"], "sha256": expected["local_sha256"], "pages": expected["page_count"]})
    require(manifest["final_live_identity_replay"]["local_wikiversity_pdf_identity_count"] == 2, "PDF replay count")
    return receipt_rows


def verify_source_defects(manifest: dict) -> None:
    require(manifest["source_defect_bindings"] == EXPECTED_SOURCE_DEFECTS, "source-defect binding drift")
    lecture_tex = (UNIT / "lecture-29-expanded.tex").read_text(encoding="utf-8")
    worksheet_tex = (UNIT / "worksheet-29-expanded.tex").read_text(encoding="utf-8")
    require(re.search(r"\{\s*g\s*\}\s*\{\s*\\geq\s*\}\{\s*3", lecture_tex) is not None, "degree-variable defect evidence")
    require("durch die Matrix" in worksheet_tex and r"\mathdisp {} {  }" in worksheet_tex, "blank-matrix defect evidence")
    require(worksheet_tex.count(r"\begin{pmatrix}  x_0") >= 2, "repeated-vector defect evidence")


def verify_replay(
    manifest: dict,
    semantic_records: list[dict],
) -> None:
    union: dict[str, dict] = {}
    for record in semantic_records:
        row = identity(record)
        key = row["title"].replace("_", " ")
        previous = union.get(key)
        require(previous is None or previous == row, f"inconsistent semantic union identity: {row['title']}")
        union[key] = row
    require(len(union) == 150, "semantic union count")
    replay = manifest["final_live_identity_replay"]
    require(replay["result"] == "PASS" and replay["semantic_unique_identity_count"] == 150, "semantic replay result/count")
    require([row["title_count"] for row in replay["semantic_batches"]] == [25, 25, 25, 25, 25, 25], "semantic replay batch topology")
    require([row["file"] for row in replay["semantic_batches"]] == [f"final-semantic-identity-replay-{index:02d}.json" for index in range(1, 7)], "semantic replay file topology")
    require(replay["local_wikiversity_pdf_identity_count"] == 2, "local PDF replay count")
    require(replay["commons_media_identity_count"] == 2, "Commons replay count")
    require(replay["latest_solution_identity_replayed"] == {"exercise_number": 2, "revid": 1094621, "timestamp": "2026-06-14T16:25:59Z", "mediawiki_sha1": "859801fc5d0e4bb16dd1ec72b7af1873ab2f2a4a"}, "latest solution replay identity")


def main() -> int:
    QA_PATH.unlink(missing_ok=True)
    for path in (MANIFEST_PATH, RIGHTS_PATH, CLOSURE_PATH, FREEZE_PATH):
        require(path.is_file() and not path.is_symlink(), f"missing authority file: {path}")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    closure = json.loads(CLOSURE_PATH.read_text(encoding="utf-8"))

    require(manifest["schema"] == "brenner-unit-authority-freeze-v2", "manifest schema")
    require(manifest["unit_number"] == 29, "manifest unit")
    require(manifest["source_course"] == COURSE_TITLE, "course title")
    require(manifest["source_course_license"] == SEMANTIC_LICENSE, "semantic course license")
    component_route = manifest["source_component_license_route"]
    require(component_route["official_pdf_legacy_notice"] == LEGACY_PDF_LICENSE, "legacy PDF route")
    require(component_route["official_pdf_current_print_version_notice"] == SEMANTIC_LICENSE, "current PDF route")
    require(component_route["no_blanket_relicensing_claim"] is True, "component no-relicensing claim")

    require_identity(manifest["source_course_surface"], EXPECTED_ROOTS["course"], "course")
    require_identity(manifest["lecture"], EXPECTED_ROOTS["lecture"], "lecture")
    require_identity(manifest["worksheet"], EXPECTED_ROOTS["worksheet"], "worksheet")
    require_identity(manifest["lecture_latex_page"], EXPECTED_ROOTS["lecture_latex"], "lecture /latex")
    require_identity(manifest["worksheet_latex_page"], EXPECTED_ROOTS["worksheet_latex"], "worksheet /latex")
    require(manifest["topic_heading"] == "Projektion weg von einem Punkt", "topic heading")

    contributors = manifest["root_revision_contributors"]
    require(contributors["course_author"] == "Holger Brenner", "course author")
    require(contributors["revision_contributor_is_not_course_authorship"] is True, "contributor/authorship distinction")
    require(
        [(row["kind"], row["pageid"], row["revid"], row["revision_contributor"]) for row in contributors["records"]]
        == [("lecture", 51996, 1069408, "Bocardodarapti"), ("worksheet", 50924, 1052757, "Arbota")],
        "root contributor identities",
    )

    expanded_rows = manifest["derived_expanded_tex"]
    require([row["file"] for row in expanded_rows] == list(EXPECTED_EXPANDED_TEX), "expanded-TeX order")
    for row in expanded_rows:
        expected_bytes, expected_sha256 = EXPECTED_EXPANDED_TEX[row["file"]]
        require((row["bytes"], row["sha256"]) == (expected_bytes, expected_sha256), f"expanded-TeX manifest identity: {row['file']}")
        path = regular_path(UNIT, row["file"], f"expanded TeX {row['file']}")
        require((path.stat().st_size, digest(path)) == (expected_bytes, expected_sha256), f"expanded-TeX bytes: {row['file']}")

    lecture_records = verify_closure(
        "lecture",
        manifest["lecture"],
        manifest["lecture_transclusion_closure"],
        manifest["transclusion_topology"]["lecture"],
    )
    worksheet_records = verify_closure(
        "worksheet",
        manifest["worksheet"],
        manifest["worksheet_transclusion_closure"],
        manifest["transclusion_topology"]["worksheet"],
    )
    _, solution_records = verify_exercises(manifest)
    verify_source_defects(manifest)

    inventory_count = verify_inventory(manifest)
    media_records = verify_media(manifest, closure)
    pdf_rows = verify_pdfs(manifest, closure)
    verify_replay(
        manifest,
        [manifest["source_course_surface"], *lecture_records, *worksheet_records, *solution_records],
    )

    receipt = {
        "schema": "ag-bridge-unit-authority-qa-v1",
        "unit": 29,
        "status": "PASS",
        "authority_manifest": {
            "path": MANIFEST_PATH.relative_to(ROOT).as_posix(),
            "bytes": MANIFEST_PATH.stat().st_size,
            "sha256": digest(MANIFEST_PATH),
        },
        "freeze_note": {
            "path": FREEZE_PATH.relative_to(ROOT).as_posix(),
            "bytes": FREEZE_PATH.stat().st_size,
            "sha256": digest(FREEZE_PATH),
        },
        "authority": {
            "course_pageid": 50687,
            "lecture_closure_with_root": 107,
            "worksheet_closure_with_root": 62,
            "solution_closures_with_root": {"2": 17, "3": 8},
            "semantic_union": 150,
            "canonical_sort": "case-sensitive (title,pageid)",
        },
        "exercises": {
            "count": 10,
            "public_solution_numbers": [2, 3],
            "negative_candidate_numbers": [1, 4, 5, 6, 7, 8, 9, 10],
            "starred": [2, 3],
            "submitted_displayed_point_total": 17,
        },
        "source_defects": [row["id"] for row in EXPECTED_SOURCE_DEFECTS],
        "media": {
            "positions": 2,
            "assets": 2,
            "public_domain": 2,
            "tschirnhausen_identification_warning_preserved": True,
            "tschirnhausen_selected_form": "thumbnail_500px",
            "tschirnhausen_selected_bytes": 83502,
            "tschirnhausen_selected_sha256": "f3dda9da65db9e431f25ea77eb83f51aed2eff1c191dc1206e0759561ee613c7",
            "tschirnhausen_original_locally_archived": False,
            "tschirnhausen_original_identity_metadata_bound": True,
        },
        "pdfs": pdf_rows,
        "rights": {
            "path": RIGHTS_PATH.relative_to(ROOT).as_posix(),
            "bytes": RIGHTS_PATH.stat().st_size,
            "sha256": digest(RIGHTS_PATH),
        },
        "asset_closure": {
            "path": CLOSURE_PATH.relative_to(ROOT).as_posix(),
            "bytes": CLOSURE_PATH.stat().st_size,
            "sha256": digest(CLOSURE_PATH),
        },
        "offline_inventory_files_verified": inventory_count,
        "unsafe_or_duplicate_inventory_paths_accepted": 0,
        "live_replay_witnesses_preserved": True,
        "provenance": PROVENANCE,
    }
    QA_PATH.parent.mkdir(parents=True, exist_ok=True)
    QA_PATH.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "receipt": QA_PATH.relative_to(ROOT).as_posix(),
                "bytes": QA_PATH.stat().st_size,
                "sha256": digest(QA_PATH),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
