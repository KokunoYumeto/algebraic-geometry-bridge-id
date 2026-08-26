#!/usr/bin/env python3
"""Freeze the complete bounded official Unit 27 Wikiversity authority closure.

Unit 27 is a bounded source-order unit from Brenner's complete 2012 course. This
script captures immutable semantic/editable witnesses, ordered exercises,
complete positive and negative public-solution evidence, both official PDFs,
component rights, accessibility facts, and a final live-identity replay.  It
does not translate or publish anything.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

import freeze_unit12_authority as base
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
UNIT = 27
COURSE = "Kurs:Algebraische Kurven (Osnabrück 2012)"
LECTURE_TITLE = f"{COURSE}/Vorlesung 27"
WORKSHEET_TITLE = f"{COURSE}/Arbeitsblatt 27"
OUT = ROOT / "authority" / "wikiversity" / "unit-27"
ARTIFACTS = ROOT / "authority" / "artifacts"
SHARED_ASSETS = ROOT / "authority" / "assets"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-27.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-27.json"
FREEZE_NOTE = ROOT / "authority" / "UNIT_27_AUTHORITY_FREEZE.md"

# Route the proven bounded capture primitives to this unit before any request.
base.UNIT = UNIT
base.COURSE = COURSE
base.OUT = OUT
base.ARTIFACTS = ARTIFACTS
base.RIGHTS = RIGHTS
base.CLOSURE = CLOSURE
base.COMMONS_META = OUT / "local-pdf-file-metadata-api.json"
base.LECTURE_TITLE = LECTURE_TITLE
base.WORKSHEET_TITLE = WORKSHEET_TITLE
base.USER_AGENT = "O016-unit27-authority-freeze/1.0 (bounded educational preservation)"

CURRENT_SEMANTIC_LICENSE = "CC BY-SA 4.0"
LEGACY_FILE_LICENSE = "CC BY-SA 2.0 Germany"
TOPIC_HEADING = "Der projektive Raum"
ADDITIONAL_TOPIC_HEADINGS = [
    "Nullstellen von homogenen Polynomen",
    "Der projektive Raum über {{math|term=\\R|SZ=}} und über {{math|term={{CC}}|SZ=}}",
]

EXPECTED_COURSE = {
    "pageid": 50687,
    "revid": 658236,
    "parentid": 439529,
    "timestamp": "2020-09-24T11:56:43Z",
    "sha1": "2f2ede7249fcaa55ba17d9cd0e3d9ee9d4941f0c",
    "wikitext_bytes": 619,
}
EXPECTED_ENTRIES = {
    "lecture": {
        "pageid": 50733,
        "revid": 1052572,
        "parentid": 1020208,
        "timestamp": "2025-08-27T14:01:03Z",
        "sha1": "9a396f3a601f0a0a0606657550a30b9a601da2f6",
        "wikitext_bytes": 3935,
    },
    "worksheet": {
        "pageid": 50762,
        "revid": 793496,
        "parentid": 324687,
        "timestamp": "2022-08-25T06:04:17Z",
        "sha1": "eeac2c6881d4121e734bc2dffbe9621f03dfdc89",
        "wikitext_bytes": 1742,
    },
}
EXPECTED_LATEX = {
    "lecture": {
        "pageid": 51877,
        "revid": 806125,
        "parentid": 796345,
        "timestamp": "2022-09-18T07:15:02Z",
        "sha1": "1d092e4f15139d9908d36c4d64a1f4fde570e1ba",
        "wikitext_bytes": 9,
    },
    "worksheet": {
        "pageid": 53020,
        "revid": 806093,
        "parentid": 796312,
        "timestamp": "2022-09-18T07:09:52Z",
        "sha1": "1d092e4f15139d9908d36c4d64a1f4fde570e1ba",
        "wikitext_bytes": 9,
    },
}
EXPECTED_CLOSURES = {
    "lecture": {
        "parser_occurrences": 120,
        "unique_exact_titles": 120,
        "dependencies": 120,
        "with_root": 121,
        "canonical_sha256": "5ed97c57220d6379b672fd7b47a8cfca82c38ef4e84bafd3538e3cdf42f74ca8",
    },
    "worksheet": {
        "parser_occurrences": 60,
        "unique_exact_titles": 60,
        "dependencies": 60,
        "with_root": 61,
        "canonical_sha256": "bea2d1bb50691139418ccf884928594f7658bc3bad1a0e22b8a4c99eb71c8b24",
    },
}
EXPECTED_SOLUTIONS: dict[int, dict] = {}
EXPECTED_PUBLIC_SOLUTION_NUMBERS: list[int] | None = []
EXPECTED_AUTHORED_POINTS: list[int] | None = [2, 2, 2, 3, 2, 2, 2, 3, 3, 3, 3]
EXPECTED_DISPLAYED_POINTS = {8: 3, 9: 3, 10: 3, 11: 3}
EXPECTED_MEDIA_NAMES = [
    "Loewenzahn_20.jpg",
    "Projektiveline1bb.jpg",
    "Projektiveline2bb.jpg",
    "Projektiveline3bb.jpg",
    "Projektiveplane1bb.jpg",
    "Projektiveplane2bb.jpg",
    "Projektiveplane3bb.jpg",
    "Projektiveplane4bb.jpg",
    "Perspective_Projection_Principle.jpg",
    "Blue-sphere.png",
]
EXPECTED_COURSE_CREDITS = {
    "Loewenzahn_20.jpg": {"author": "Waugsberg", "user": "", "repository": "Commons", "license_label": "CC-BY-SA-2.5"},
    "Projektiveline1bb.jpg": {"author": "Darapti", "user": "", "repository": "Commons", "license_label": "CC-BY-SA-3.0"},
    "Projektiveline2bb.jpg": {"author": "Darapti", "user": "", "repository": "Commons", "license_label": "CC-BY-SA-3.0"},
    "Projektiveline3bb.jpg": {"author": "Darapti", "user": "", "repository": "Commons", "license_label": "CC-BY-SA-3.0"},
    "Projektiveplane1bb.jpg": {"author": "Darapti", "user": "", "repository": "Commons", "license_label": "CC-BY-SA-3.0"},
    "Projektiveplane2bb.jpg": {"author": "Darapti", "user": "", "repository": "Commons", "license_label": "CC-BY-SA-3.0"},
    "Projektiveplane3bb.jpg": {"author": "Darapti", "user": "", "repository": "Commons", "license_label": "CC-BY-SA-3.0"},
    "Projektiveplane4bb.jpg": {"author": "Darapti", "user": "", "repository": "Commons", "license_label": "CC-BY-SA-3.0"},
    "Perspective_Projection_Principle.jpg": {"author": "", "user": "Fantagu", "repository": "Commons", "license_label": "CC-BY-SA-3.0"},
    "Blue-sphere.png": {"author": "", "user": "Kieff", "repository": "Commons", "license_label": "PD"},
}
EXPECTED_MEDIA: dict[str, dict] = {
    "Loewenzahn_20.jpg": {
        "pageid": 2016480, "revid": 1247205786, "parentid": 1145516218,
        "timestamp": "2026-07-13T06:22:34Z", "sha1": "580150be0321eb5c5306677d51f457ac92222489",
        "wikitext_bytes": 320, "source_timestamp": "2007-04-28T22:16:58Z", "source_bytes": 840757,
        "source_sha1": "5f0f9dcad9abd11a27b28b77847226c65785e42a", "width": 2288, "height": 1712,
    },
    "Projektiveline1bb.jpg": {
        "pageid": 5909039, "revid": 1252904590, "parentid": 1243185432,
        "timestamp": "2026-07-27T20:23:29Z", "sha1": "21bb191b5ea1963f0185fbc05d9a2b7c924080f8",
        "wikitext_bytes": 355, "source_timestamp": "2009-02-09T18:56:39Z", "source_bytes": 723518,
        "source_sha1": "6cdf4d9ba1caac42c678b0de7fb8f91be1d3bd00", "width": 1920, "height": 1080,
    },
    "Projektiveline2bb.jpg": {
        "pageid": 5909093, "revid": 1252904648, "parentid": 1100106079,
        "timestamp": "2026-07-27T20:23:34Z", "sha1": "5c611c6e3b996af11ec8d4e77ff3dcbe022a312f",
        "wikitext_bytes": 386, "source_timestamp": "2009-02-09T19:05:59Z", "source_bytes": 777323,
        "source_sha1": "7a8ca057dc79e8d902c9ab59a60dd653efc7bb53", "width": 1920, "height": 1080,
    },
    "Projektiveline3bb.jpg": {
        "pageid": 5909079, "revid": 1252904680, "parentid": 1243373728,
        "timestamp": "2026-07-27T20:23:37Z", "sha1": "7ad396573b84177606bc4dd11eab321c7922267e",
        "wikitext_bytes": 387, "source_timestamp": "2009-02-09T19:03:08Z", "source_bytes": 808222,
        "source_sha1": "64cffcd438c46cf135088bea91e4fd0dfe1ae379", "width": 1920, "height": 1080,
    },
    "Projektiveplane1bb.jpg": {
        "pageid": 5909161, "revid": 1252904952, "parentid": 1072444930,
        "timestamp": "2026-07-27T20:24:00Z", "sha1": "b05c8806e704797c56344d477f74fa7015da228a",
        "wikitext_bytes": 387, "source_timestamp": "2009-02-09T19:16:23Z", "source_bytes": 737889,
        "source_sha1": "371aa3d8b9a7c429563c80c624764897dfb01787", "width": 1920, "height": 1080,
    },
    "Projektiveplane2bb.jpg": {
        "pageid": 5909182, "revid": 1252905099, "parentid": 1243372688,
        "timestamp": "2026-07-27T20:24:16Z", "sha1": "f25b67bdcf431d8b6febb87d4647d0717b5a5892",
        "wikitext_bytes": 387, "source_timestamp": "2009-02-09T19:19:41Z", "source_bytes": 789468,
        "source_sha1": "6a959ba6bac06b673a4252bb0e5ce8b1eaab5d82", "width": 1920, "height": 1080,
    },
    "Projektiveplane3bb.jpg": {
        "pageid": 5909193, "revid": 1252905074, "parentid": 1243372961,
        "timestamp": "2026-07-27T20:24:13Z", "sha1": "0208b8a7cc57da42ede1e43ee36b54fae900ae65",
        "wikitext_bytes": 387, "source_timestamp": "2009-02-09T19:21:41Z", "source_bytes": 801410,
        "source_sha1": "c0471b85d6e56d547f0976b6c7dee7a24ca49547", "width": 1920, "height": 1080,
    },
    "Projektiveplane4bb.jpg": {
        "pageid": 5909201, "revid": 1252905141, "parentid": 1185953024,
        "timestamp": "2026-07-27T20:24:21Z", "sha1": "16ae02d6a109c7913e6e4a47bf4be7346c5ff503",
        "wikitext_bytes": 407, "source_timestamp": "2009-02-09T19:23:02Z", "source_bytes": 839639,
        "source_sha1": "4606cf629f10e387a589d03597f85fa991902068", "width": 1920, "height": 1080,
    },
    "Perspective_Projection_Principle.jpg": {
        "pageid": 337435, "revid": 488715640, "parentid": 142246843,
        "timestamp": "2020-10-13T14:33:49Z", "sha1": "833c5f24aef7a02e7b86022ec941b7126ebec155",
        "wikitext_bytes": 273, "source_timestamp": "2005-09-24T09:59:43Z", "source_bytes": 53956,
        "source_sha1": "0f33c6c4dc3f95ba2723e6c777deab3ecdb37e0a", "width": 800, "height": 368,
    },
    "Blue-sphere.png": {
        "pageid": 1243724, "revid": 1041208370, "parentid": 826671531,
        "timestamp": "2025-06-07T16:42:42Z", "sha1": "daf418a13ef72190e6ecab86e2a481aac01d66ee",
        "wikitext_bytes": 382, "source_timestamp": "2006-10-04T01:59:44Z", "source_bytes": 123336,
        "source_sha1": "c86a035254ed60c637f822c1357973878b860763", "width": 960, "height": 960,
    },
}
EXPECTED_PDFS = {
    "lecture": {
        "file_title": "Datei:Algebraische Kurven (Osnabrück 2012)Vorlesung27.pdf",
        "file_pageid": 53376,
        "file_revid": 333482,
        "file_parentid": 321269,
        "file_timestamp": "2012-10-19T12:00:13Z",
        "file_sha1": "dc3d5fc4d36d5b5b1ed5d39f30a29647f4ceb3e8",
        "source_timestamp": "2012-10-19T12:00:13Z",
        "source_bytes": 171996,
        "source_sha1": "957128b0f0008de76432a4fdf88d56283d229559",
        "local_sha256": "0d4402bfae46abd09cb4719110a006287b03de31b0e620e0157a4ef9a07817f2",
        "page_count": 9,
    },
    "worksheet": {
        "file_title": "Datei:Algebraische Kurven (Osnabrück 2012)Arbeitsblatt27.pdf",
        "file_pageid": 54238,
        "file_revid": 325015,
        "file_parentid": 321244,
        "file_timestamp": "2012-07-31T14:02:33Z",
        "file_sha1": "0891524b106887dc0eb9afa0c5ff655a26ed45ba",
        "source_timestamp": "2012-07-31T14:02:33Z",
        "source_bytes": 41952,
        "source_sha1": "6fed5295a1e7141f0cc640c951938be23522f031",
        "local_sha256": "e1fa608c2b54c988f16d0c0b2119f1d21440b37debbf87d89b7bbf228c6bdf9d",
        "page_count": 2,
    },
}
EXPECTED_LIVE_UNION = 157
EXPECTED_ROOT_CONTRIBUTOR = "Arbota"
SOURCE_DEFECT_BINDINGS = [
    {
        "id": "AGC-U27-SRC-001",
        "surface": "lecture current semantic source / expanded TeX",
        "source_text": "F\\frac{1}{X_0}=0 and F\\frac{0}{X_0}=0",
        "issue": "The rendered formulas look like multiplication by fractions, although the prose requires substitution X_0=1 and X_0=0.",
        "reader_handling": "Disclose the source notation and render the intended substitutions explicitly as F(1,X_1,...,X_n)=0 and F(0,X_1,...,X_n)=0.",
    },
    {
        "id": "AGC-U27-SRC-002",
        "surface": "lecture current semantic source / expanded TeX",
        "source_text": "F=a_0X_0+a_1X_0+\\cdots+a_nX_n",
        "issue": "The second variable is repeated; the degree-one form requires a_1X_1.",
        "reader_handling": "Correct the second term to a_1X_1 and disclose the correction.",
    },
    {
        "id": "AGC-U27-SRC-003",
        "surface": "lecture current semantic source / expanded TeX",
        "source_text": "nach Fakt *****",
        "issue": "The compactness proof contains an unresolved internal cross-reference placeholder.",
        "reader_handling": "State the standard continuous-image-of-a-compact-space result without inventing a source identifier; disclose the unresolved source reference.",
    },
    {
        "id": "AGC-U27-SRC-004",
        "surface": "lecture current semantic source / expanded TeX",
        "source_text": "Man kann annehmen, dass sie beide auf einem der affinen ueberdeckenden Raeume D_+(X_i) liegen.",
        "issue": "Two projective points need not share one of the fixed standard charts; for example [1:0] and [0:1] in P^1 share neither D_+(X_0) nor D_+(X_1).",
        "reader_handling": "For K=R or C, choose a linear form nonzero on both points and use its affine chart (equivalently make a projective coordinate change), then separate them there; disclose the repair.",
    },
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def key(value: str) -> str:
    return value.replace("_", " ")


def normalized_identity(record: dict) -> dict:
    return {
        "title": record["title"],
        "pageid": int(record["pageid"]),
        "revid": int(record["revid"]),
        "parentid": int(record.get("parentid", 0)),
        "timestamp": record["timestamp"],
        "mediawiki_sha1": record["mediawiki_sha1"],
        "wikitext_bytes": int(record["wikitext_bytes"]),
    }


def identity_hash(records: list[dict]) -> str:
    rows = sorted((normalized_identity(item) for item in records), key=lambda row: (row["title"], row["pageid"]))
    raw = json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def assert_surface(kind: str, record: dict, expected: dict) -> None:
    actual = {
        "pageid": record["pageid"],
        "revid": record["revid"],
        "parentid": record["parentid"],
        "timestamp": record["timestamp"],
        "sha1": record["mediawiki_sha1"],
        "wikitext_bytes": record["wikitext_bytes"],
    }
    require(actual == expected, f"{kind} identity drift: {actual}")


def read_api_content(record: dict) -> str:
    payload = json.loads((OUT / record["api_file"]).read_text(encoding="utf-8"))
    return base.revision(base.one_page(payload))["slots"]["main"]["content"]


def closure_topology(kind: str, root: dict, parsed: dict, closure: dict) -> dict:
    expected = EXPECTED_CLOSURES.get(kind)
    titles = [item["title"] for item in parsed.get("templates", [])]
    if expected is None:
        expected = {
            "parser_occurrences": len(titles),
            "unique_exact_titles": len(set(titles)),
            "dependencies": len(set(titles)),
            "with_root": len(set(titles)) + 1,
            "canonical_sha256": "PENDING",
        }
    require(len(titles) == expected["parser_occurrences"], f"{kind} parser occurrence count")
    require(len(set(titles)) == expected["unique_exact_titles"], f"{kind} exact-title uniqueness")
    require(closure["captured_page_count"] == expected["dependencies"], f"{kind} captured closure")
    require(closure["missing_page_count"] == 0, f"{kind} missing dependency")
    records = [root, *closure["pages"]]
    observed = identity_hash(records)
    require(len(records) == expected["with_root"], f"{kind} root-plus-dependency count")
    if expected["canonical_sha256"] != "PENDING":
        require(observed == expected["canonical_sha256"], f"{kind} canonical identity hash drift: {observed}")
    return {
        "parser_template_occurrences": len(titles),
        "unique_exact_titles": len(set(titles)),
        "duplicate_exact_titles": [
            {"title": title, "occurrences": titles.count(title)}
            for title in sorted(set(titles))
            if titles.count(title) > 1
        ],
        "dependencies": closure["captured_page_count"],
        "with_root": len(records),
        "canonical_identity_rows_sha256": observed,
        "canonical_identity_hash_algorithm": (
            "SHA-256 of UTF-8 JSON rows reduced to title,pageid,revid,parentid,timestamp,"
            "mediawiki_sha1,wikitext_bytes; rows sorted by (title,pageid); ensure_ascii=false; "
            "sort_keys=true; separators=(',',':')"
        ),
    }


def site_rights_surface() -> dict:
    raw, payload = base.api_raw(base.WIKI_API, {"action": "query", "meta": "siteinfo", "siprop": "rightsinfo"})
    path = OUT / "site-rightsinfo-api.json"
    base.write_bytes(path, raw)
    info = payload["query"]["rightsinfo"]
    require("creativecommons.org/licenses/by-sa/4.0" in info["url"], f"site rights route drift: {info}")
    return {
        "source": "de.wikiversity.org action=query meta=siteinfo rightsinfo",
        "notice": CURRENT_SEMANTIC_LICENSE,
        "text": info["text"],
        "url": info["url"],
        "file": path.name,
        "bytes": path.stat().st_size,
        "sha256": base.digest(path),
    }


def root_revision_contributors(lecture: dict, worksheet: dict) -> dict:
    raw, payload = base.api_raw(
        base.WIKI_API,
        {
            "action": "query",
            "prop": "revisions",
            "revids": f"{lecture['revid']}|{worksheet['revid']}",
            "rvprop": "ids|user|timestamp|sha1",
        },
    )
    path = OUT / "root-revision-contributors-api.json"
    base.write_bytes(path, raw)
    pages = payload.get("query", {}).get("pages", [])
    require(len(pages) == 2, "root contributor response count")
    expected = {
        int(lecture["revid"]): ("lecture", lecture),
        int(worksheet["revid"]): ("worksheet", worksheet),
    }
    records = []
    for page in pages:
        rev = base.revision(page)
        kind, frozen = expected[int(rev["revid"])]
        require(
            int(page["pageid"]) == int(frozen["pageid"])
            and rev["timestamp"] == frozen["timestamp"]
            and rev["sha1"] == frozen["mediawiki_sha1"],
            f"{kind} contributor identity drift",
        )
        require(rev["user"] == EXPECTED_ROOT_CONTRIBUTOR, f"{kind} root contributor drift")
        records.append({
            "kind": kind,
            "title": page["title"],
            "pageid": int(page["pageid"]),
            "revid": int(rev["revid"]),
            "timestamp": rev["timestamp"],
            "mediawiki_sha1": rev["sha1"],
            "revision_contributor": rev["user"],
        })
    records.sort(key=lambda item: item["kind"])
    return {
        "source": "de.wikiversity.org action=query prop=revisions rvprop=ids|user|timestamp|sha1",
        "course_author": "Holger Brenner",
        "revision_contributor_is_not_course_authorship": True,
        "records": records,
        "file": path.name,
        "bytes": path.stat().st_size,
        "sha256": base.digest(path),
    }


def enrich_exercise_map(solutions: dict, worksheet_parsed: dict) -> dict:
    entries = solutions["entries"]
    require(len(entries) == 11, "Unit 27 must retain exactly eleven ordered exercises")
    require([item["exercise_number"] for item in entries] == list(range(1, 12)), "exercise order")
    titles = [item["exercise_title"] for item in entries]
    raw, payload = base.api_raw(
        base.WIKI_API,
        {
            "action": "query",
            "prop": "revisions",
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "main",
            "redirects": 1,
            "titles": "|".join(titles),
        },
    )
    source_path = OUT / "ordered-exercise-source-api.json"
    base.write_bytes(source_path, raw)
    query = payload.get("query", {})
    mapping = base.canonical_map(query)
    pages = {page["title"]: page for page in query.get("pages", [])}
    observed_authored: list[int] = []
    for number, (entry, title) in enumerate(zip(entries, titles, strict=True), start=1):
        resolved = base.resolve_title(title, mapping)
        page = pages.get(resolved) or pages.get(title)
        require(page is not None and not page.get("missing"), f"exercise source absent: {title}")
        rev = base.revision(page)
        content = rev["slots"]["main"]["content"]
        match = re.search(r"(?m)^\|Punkte\s*=\s*([^\r\n}]*)", content)
        require(match is not None and match.group(1).strip().isdigit(), f"exercise {number} authored points")
        authored_points = int(match.group(1).strip())
        observed_authored.append(authored_points)
        role = "warm-up" if number <= 7 else "submitted"
        entry.update(
            {
                "role": role,
                "authored_points": authored_points,
                "displayed_points": EXPECTED_DISPLAYED_POINTS.get(number),
                "points_displayed_in_worksheet": number >= 8,
                "starred_in_worksheet": False,
                "exercise_pageid": int(page["pageid"]),
                "exercise_revid": int(rev["revid"]),
                "exercise_parentid": int(rev.get("parentid", 0)),
                "exercise_timestamp": rev["timestamp"],
                "exercise_mediawiki_sha1": rev["sha1"],
                "exercise_wikitext_bytes": base.content_bytes(rev),
            }
        )
    if EXPECTED_AUTHORED_POINTS is not None:
        require(observed_authored == EXPECTED_AUTHORED_POINTS, f"authored point drift: {observed_authored}")

    parsed_order = [
        item["title"]
        for item in worksheet_parsed.get("templates", [])
        if int(item.get("ns", -1)) != 10 and item["title"].endswith("/Aufgabe")
    ]
    require(parsed_order == titles, "worksheet parser exercise order")
    toc_lines = [section["line"] for section in worksheet_parsed["tocdata"]["sections"]]
    require(len(toc_lines) == 11, "worksheet TOC exercise count")
    require(not any("*" in line for line in toc_lines), "unexpected star topology")
    for number, points in EXPECTED_DISPLAYED_POINTS.items():
        require(f"({points} Punkte)" in toc_lines[number - 1], f"exercise {number} displayed points")

    public_numbers = [item["exercise_number"] for item in entries if item["has_public_solution"]]
    if EXPECTED_PUBLIC_SOLUTION_NUMBERS is not None:
        require(public_numbers == EXPECTED_PUBLIC_SOLUTION_NUMBERS, f"public solution drift: {public_numbers}")
    candidate = json.loads((OUT / solutions["candidate_api_file"]).read_text(encoding="utf-8"))
    candidate_pages = candidate.get("query", {}).get("pages", [])
    require(len(candidate_pages) == 11, "candidate query must return exactly eleven page records")
    negatives = [
        {
            "exercise_number": item["exercise_number"],
            "attempted_solution_title": item["solution_title"],
            "api_missing": True,
        }
        for item in entries
        if not item["has_public_solution"]
    ]
    solutions["ordered_role_point_and_star_topology"] = {
        "warm_up_numbers": list(range(1, 8)),
        "submitted_numbers": list(range(8, 12)),
        "upload_numbers": [],
        "authored_points": {str(i): value for i, value in enumerate(observed_authored, start=1)},
        "displayed_points": {str(k): v for k, v in EXPECTED_DISPLAYED_POINTS.items()},
        "submitted_displayed_point_total": sum(EXPECTED_DISPLAYED_POINTS.values()),
        "starred_numbers": [],
        "source_api_file": source_path.name,
        "source_api_bytes": source_path.stat().st_size,
        "source_api_sha256": base.digest(source_path),
    }
    solutions["negative_public_solution_evidence"] = {
        "candidate_query_file": solutions["candidate_api_file"],
        "candidate_query_bytes": solutions["candidate_api_bytes"],
        "candidate_query_sha256": solutions["candidate_api_sha256"],
        "exact_candidate_title_count": 11,
        "positive_numbers": public_numbers,
        "negative_numbers": [item["exercise_number"] for item in entries if not item["has_public_solution"]],
        "negative_count": len(negatives),
        "entries": negatives,
    }
    solutions["point_discrepancies"] = [
        {
            "id": f"AGC-U27-POINT-{number:03d}",
            "exercise_number": number,
            "exercise_page_authored_points": observed_authored[number - 1],
            "worksheet_displayed_points": displayed,
            "handling": "Preserve and disclose both source values; do not silently reconcile them.",
        }
        for number, displayed in EXPECTED_DISPLAYED_POINTS.items()
        if observed_authored[number - 1] != displayed
    ]
    map_path = OUT / "ORDERED_EXERCISE_MAP.json"
    for field in ("map_file", "map_bytes", "map_sha256"):
        solutions.pop(field, None)
    base.write_json(map_path, solutions)
    solutions["map_file"] = map_path.name
    solutions["map_bytes"] = map_path.stat().st_size
    solutions["map_sha256"] = base.digest(map_path)
    return solutions
def public_solution_closures(solutions: dict) -> list[dict]:
    candidates = json.loads((OUT / solutions["candidate_api_file"]).read_text(encoding="utf-8"))
    pages = {
        key(page["title"]): page
        for page in candidates.get("query", {}).get("pages", [])
        if not page.get("missing")
    }
    records: list[dict] = []
    public = [item for item in solutions["entries"] if item["has_public_solution"]]
    public_numbers = [item["exercise_number"] for item in public]
    if EXPECTED_PUBLIC_SOLUTION_NUMBERS is not None:
        require(public_numbers == EXPECTED_PUBLIC_SOLUTION_NUMBERS, "public solution roots")
    for item in public:
        number = item["exercise_number"]
        page = pages.get(key(item["resolved_title"]))
        require(page is not None, f"public solution {number} body absent")
        rev = base.revision(page)
        actual = {
            "pageid": int(page["pageid"]),
            "revid": int(rev["revid"]),
            "parentid": int(rev.get("parentid", 0)),
            "timestamp": rev["timestamp"],
            "sha1": rev["sha1"],
            "wikitext_bytes": base.content_bytes(rev),
        }
        expected = EXPECTED_SOLUTIONS.get(number)
        if expected is not None:
            require(actual == expected, f"solution {number} identity drift: {actual}")
        content = rev["slots"]["main"]["content"]
        require(not re.findall(r"\{\{\s*:\s*([^|}\n]+)", content), f"solution {number} became a wrapper")
        raw, payload = base.api_raw(
            base.WIKI_API,
            {
                "action": "parse",
                "oldid": int(rev["revid"]),
                "prop": "links|templates|images|externallinks|tocdata",
            },
        )
        parse_path = OUT / f"solution-ex{number:02d}-parse-api.json"
        base.write_bytes(parse_path, raw)
        parsed = payload["parse"]
        closure = base.transclusion_closure(parsed, f"solution-ex{number:02d}")
        root = {
            "title": page["title"],
            "pageid": page["pageid"],
            "revid": rev["revid"],
            "parentid": rev.get("parentid", 0),
            "timestamp": rev["timestamp"],
            "mediawiki_sha1": rev["sha1"],
            "wikitext_bytes": base.content_bytes(rev),
        }
        topology = closure_topology(f"solution-{number:02d}", root, parsed, closure)
        records.append(
            {
                "exercise_number": number,
                "solution_title": page["title"],
                "solution_pageid": int(page["pageid"]),
                "solution_revid": int(rev["revid"]),
                "solution_parentid": int(rev.get("parentid", 0)),
                "solution_timestamp": rev["timestamp"],
                "solution_mediawiki_sha1": rev["sha1"],
                "solution_wikitext_bytes": base.content_bytes(rev),
                "direct_wrapper_dependency_titles": [],
                "parse_api_file": parse_path.name,
                "parse_api_bytes": parse_path.stat().st_size,
                "parse_api_sha256": base.digest(parse_path),
                "recursive_transclusion_closure": closure,
                "topology": topology,
            }
        )
    return records


def file_description_surface(kind: str, title: str, expected: dict) -> tuple[dict, dict]:
    record, parsed = base.entry_surface(title, f"{kind}-27-file-description")
    assert_surface(
        f"{kind} file-description",
        record,
        {
            "pageid": expected["file_pageid"],
            "revid": expected["file_revid"],
            "parentid": expected["file_parentid"],
            "timestamp": expected["file_timestamp"],
            "sha1": expected["file_sha1"],
            "wikitext_bytes": len(read_api_content(record).encode("utf-8")),
        },
    )
    closure = base.transclusion_closure(parsed, f"{kind}-27-file-description")
    require(closure["missing_page_count"] == 0, f"{kind} file-description dependency")
    html = (OUT / record["html_file"]).read_text(encoding="utf-8").casefold()
    require("creativecommons.org/licenses/by-sa/4.0" in html, f"{kind} current 4.0 notice")
    require("creativecommons.org/licenses/by-sa/2.0/de" in html, f"{kind} legacy 2.0-DE notice")
    return record, closure


def pdf_outline_count(reader: base.PdfReader) -> int:
    try:
        outline = reader.outline
    except Exception:
        return 0
    stack = list(outline if isinstance(outline, list) else ([outline] if outline else []))
    count = 0
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(item)
        else:
            count += 1
    return count


def embedded_course_credit_labels() -> dict[str, dict]:
    text = (OUT / "lecture-27-expanded.tex").read_text(encoding="utf-8")
    pattern = re.compile(
        r"\\bildlizenz\s*\{\s*([^{}]*?)\s*\}\s*"
        r"\{\s*([^{}]*?)\s*\}\s*\{\s*([^{}]*?)\s*\}\s*"
        r"\{\s*([^{}]*?)\s*\}\s*\{\s*([^{}]*?)\s*\}\s*"
        r"\{\s*([^{}]*?)\s*\}"
    )
    observed: dict[str, dict] = {}
    for filename, author, user, repository, license_label, trailing in pattern.findall(text):
        parser_name = filename.strip().replace(" ", "_")
        require(parser_name not in observed, f"duplicate embedded credit label: {parser_name}")
        observed[parser_name] = {
            "source_filename_label": filename.strip(),
            "author": author.strip(),
            "user": user.strip(),
            "repository": repository.strip(),
            "license_label": license_label.strip(),
            "trailing_field": trailing.strip(),
        }
    require(list(observed) == EXPECTED_MEDIA_NAMES, f"embedded credit order drift: {list(observed)}")
    for name, expected in EXPECTED_COURSE_CREDITS.items():
        actual = {field: observed[name][field] for field in expected}
        require(actual == expected, f"embedded course credit drift: {name}: {actual}")
        require(observed[name]["trailing_field"] == "", f"embedded course credit trailing field: {name}")
    return observed


def verify_source_defects() -> list[dict]:
    tex = (OUT / "lecture-27-expanded.tex").read_text(encoding="utf-8")
    html = (OUT / "lecture-27.html").read_text(encoding="utf-8")
    require("F { \\frac{   1 }{ X_0 } }" in tex and "F { \\frac{   0 }{ X_0 } }" in tex, "substitution-notation defect evidence")
    require("a_0X_0 + a_1X_0 + \\cdots + a_nX_n" in tex, "linear-form defect evidence")
    require("nach Fakt *****" in tex, "unresolved-reference defect evidence")
    require("beide auf einem der affinen überdeckenden Räume" in tex, "fixed-chart defect evidence")
    for needle in (">*****</a>", "a_1X_0", "affinen überdeckenden Räume"):
        require(needle in html, f"rendered source-defect evidence: {needle}")
    return SOURCE_DEFECT_BINDINGS


def official_pdfs_and_media(
    lecture_parsed: dict, worksheet_parsed: dict
) -> tuple[list[dict], list[dict], dict, list[dict]]:
    image_names = list(dict.fromkeys(lecture_parsed.get("images", []) + worksheet_parsed.get("images", [])))
    pdf_names = [name for name in image_names if name.casefold().endswith(".pdf")]
    substantive = [name for name in image_names if not name.casefold().endswith(".pdf")]
    require(substantive == EXPECTED_MEDIA_NAMES, f"Unit 27 substantive media order: {substantive}")
    require(len(pdf_names) == 2, f"Unit 27 official PDF topology: {pdf_names}")
    expected_names = {
        value["file_title"].split(":", 1)[1].replace(" ", "_").casefold()
        for value in EXPECTED_PDFS.values()
    }
    require({name.replace(" ", "_").casefold() for name in pdf_names} == expected_names, "official PDF names")

    pdf_titles = [EXPECTED_PDFS["lecture"]["file_title"], EXPECTED_PDFS["worksheet"]["file_title"]]
    raw, payload = base.api_raw(
        base.WIKI_API,
        {
            "action": "query",
            "prop": "imageinfo|revisions",
            "iiprop": "timestamp|user|url|size|sha1|mime|mediatype|extmetadata",
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "main",
            "titles": "|".join(pdf_titles),
        },
    )
    metadata_path = OUT / "local-pdf-file-metadata-api.json"
    base.write_bytes(metadata_path, raw)
    pages = {key(page["title"]): page for page in payload.get("query", {}).get("pages", [])}
    require(len(pages) == 2 and not any(page.get("missing") for page in pages.values()), "local file pages")
    surfaces, pdf_records = [], []
    for kind in ("lecture", "worksheet"):
        expected = EXPECTED_PDFS[kind]
        page = pages.get(key(expected["file_title"]))
        require(page is not None and len(page.get("imageinfo", [])) == 1, f"{kind} PDF imageinfo")
        info, rev = page["imageinfo"][0], base.revision(page)
        actual = {
            "file_pageid": int(page["pageid"]),
            "file_revid": int(rev["revid"]),
            "file_parentid": int(rev.get("parentid", 0)),
            "file_timestamp": rev["timestamp"],
            "file_sha1": rev["sha1"],
            "source_timestamp": info["timestamp"],
            "source_bytes": int(info["size"]),
            "source_sha1": info["sha1"],
        }
        require(actual == {name: expected[name] for name in actual}, f"{kind} PDF/file identity drift: {actual}")
        local = ARTIFACTS / f"{kind}-27-official.pdf"
        if (
            local.is_file()
            and local.stat().st_size == expected["source_bytes"]
            and base.digest(local, "sha1") == expected["source_sha1"]
        ):
            data = local.read_bytes()
        else:
            data = base.fetch(info["url"])
            base.write_bytes(local, data)
        require(len(data) == expected["source_bytes"], f"{kind} PDF byte count")
        require(base.digest_bytes(data, "sha1") == expected["source_sha1"], f"{kind} PDF SHA-1")
        if expected["local_sha256"] != "PENDING":
            require(base.digest(local) == expected["local_sha256"], f"{kind} PDF SHA-256")
        reader = base.PdfReader(str(local))
        if expected["page_count"]:
            require(len(reader.pages) == expected["page_count"], f"{kind} PDF page count")
        require(not reader.is_encrypted, f"{kind} PDF encryption")
        page_text = [(pdf_page.extract_text() or "") for pdf_page in reader.pages]
        root = reader.trailer["/Root"]
        mark_info = root.get("/MarkInfo")
        if hasattr(mark_info, "get_object"):
            mark_info = mark_info.get_object()
        tagged = bool(mark_info and mark_info.get("/Marked", False))
        structure = root.get("/StructTreeRoot") is not None
        language = root.get("/Lang")
        outlines = pdf_outline_count(reader)
        surface, surface_closure = file_description_surface(kind, expected["file_title"], expected)
        surfaces.append({"kind": kind, "entry": surface, "recursive_transclusion_closure": surface_closure})
        pdf_records.append(
            {
                "kind": kind,
                "source_file_title": page["title"],
                "file_pageid": int(page["pageid"]),
                "file_revid": int(rev["revid"]),
                "file_parentid": int(rev.get("parentid", 0)),
                "file_timestamp": rev["timestamp"],
                "file_mediawiki_sha1": rev["sha1"],
                "file_wikitext_bytes": base.content_bytes(rev),
                "source_timestamp": info["timestamp"],
                "uploader": info.get("user", ""),
                "source_bytes": int(info["size"]),
                "source_sha1": info["sha1"],
                "source_url": info["url"].split("?", 1)[0],
                "description_url": info["descriptionurl"],
                "mime": info["mime"],
                "media_type": info.get("mediatype", ""),
                "local_path": local.relative_to(ROOT).as_posix(),
                "local_bytes": local.stat().st_size,
                "local_sha256": base.digest(local),
                "page_count": len(reader.pages),
                "page_text_characters": [len(text) for text in page_text],
                "extractable_text_characters": sum(len(text) for text in page_text),
                "blank_page_numbers": [index for index, text in enumerate(page_text, start=1) if not text.strip()],
                "accessibility": {
                    "encrypted": False,
                    "tagged_pdf": tagged,
                    "structure_tree_present": structure,
                    "document_language": str(language) if language is not None else None,
                    "outline_or_bookmark_count": outlines,
                },
                "component_license_route": {
                    "current_print_version_notice": CURRENT_SEMANTIC_LICENSE,
                    "current_notice_evidence": surface["html_file"],
                    "legacy_file_notice": LEGACY_FILE_LICENSE,
                    "legacy_notice_evidence": surface["html_file"],
                    "embedded_pdf_label": None,
                    "interpretation": (
                        "Preserve both notices: the current print-version/course route is CC BY-SA 4.0, "
                        "while the unchanged 2012 file page retains CC BY-SA 2.0 Germany."
                    ),
                },
            }
        )

    commons_raw, commons_payload = base.api_raw(
        base.COMMONS_API,
        {
            "action": "query",
            "prop": "imageinfo|revisions",
            "iiprop": "timestamp|user|url|size|sha1|mime|mediatype|extmetadata",
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "main",
            "titles": "|".join("File:" + name for name in substantive),
        },
    )
    commons_path = OUT / "commons-media-metadata-api.json"
    base.write_bytes(commons_path, commons_raw)
    commons_pages = {
        base.file_key(page["title"]): page
        for page in commons_payload.get("query", {}).get("pages", [])
    }
    require(
        set(commons_pages) == {base.file_key(name) for name in substantive}
        and not any(page.get("missing") for page in commons_pages.values()),
        "Commons substantive media title closure",
    )
    asset_dir = OUT / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    SHARED_ASSETS.mkdir(parents=True, exist_ok=True)
    course_credits = embedded_course_credit_labels()
    rows: list[dict] = []
    asset_records: list[dict] = []
    for order, name in enumerate(substantive, start=1):
        page = commons_pages[base.file_key(name)]
        require(len(page.get("imageinfo", [])) == 1 and len(page.get("revisions", [])) == 1, f"Commons metadata: {name}")
        info, desc_rev = page["imageinfo"][0], base.revision(page)
        desc_content = desc_rev["slots"]["main"]["content"]
        local_name = urllib.parse.unquote(Path(urllib.parse.urlparse(info["url"]).path).name)
        local = asset_dir / local_name
        if (
            local.is_file()
            and local.stat().st_size == int(info["size"])
            and base.digest(local, "sha1") == info["sha1"]
        ):
            data = local.read_bytes()
        else:
            data = base.fetch(info["url"])
            base.write_bytes(local, data)
        require(len(data) == int(info["size"]), f"Commons byte count: {name}")
        require(base.digest_bytes(data, "sha1") == info["sha1"], f"Commons SHA-1: {name}")
        with Image.open(local) as image:
            image.verify()
        with Image.open(local) as image:
            width, height = int(image.width), int(image.height)
            frames = int(getattr(image, "n_frames", 1))
        require((width, height) == (int(info["width"]), int(info["height"])), f"Commons dimensions: {name}")
        shared = SHARED_ASSETS / local_name
        if shared.is_file():
            require(
                shared.stat().st_size == local.stat().st_size and base.digest(shared) == base.digest(local),
                f"shared reader asset collision: {shared}",
            )
        else:
            base.write_bytes(shared, data)
        metadata = info.get("extmetadata", {})
        license_short = base.ext(metadata, "LicenseShortName") or base.ext(metadata, "UsageTerms")
        license_url = base.ext(metadata, "LicenseUrl")
        require(license_short, f"Commons component license absent: {name}")
        identity = {
            "pageid": int(page["pageid"]),
            "revid": int(desc_rev["revid"]),
            "parentid": int(desc_rev.get("parentid", 0)),
            "timestamp": desc_rev["timestamp"],
            "sha1": desc_rev["sha1"],
            "wikitext_bytes": base.content_bytes(desc_rev),
            "source_timestamp": info["timestamp"],
            "source_bytes": int(info["size"]),
            "source_sha1": info["sha1"],
            "width": int(info["width"]),
            "height": int(info["height"]),
        }
        expected_media = EXPECTED_MEDIA.get(name)
        if expected_media is not None:
            require(identity == expected_media, f"Commons identity drift: {name}: {identity}")
        artist = base.ext(metadata, "Artist")
        credit = base.ext(metadata, "Credit")
        if name == "Perspective_Projection_Principle.jpg":
            require("Drawing by Joachim Baecker 2005/09/23" in desc_content, "Perspective creator credit")
            artist = artist or "Joachim Baecker"
            credit = credit or "Drawing by Joachim Baecker 2005/09/23 (Commons description page)"
        course_credit = course_credits[name]
        row = {
            "asset_id": f"br-ak-u27-media-{order:03d}",
            "reader_order": order,
            "resource_title": "File:" + name,
            "metadata_title": page["title"],
            "repository": "Wikimedia Commons",
            "description_url": info["descriptionurl"],
            "original_url": info["url"].split("?", 1)[0],
            "selected_url": info["url"].split("?", 1)[0],
            "selected_form": "original",
            "local_path": shared.relative_to(ROOT).as_posix(),
            "local_bytes": shared.stat().st_size,
            "local_sha256": base.digest(shared),
            "authority_witness_path": local.relative_to(ROOT).as_posix(),
            "authority_witness_bytes": local.stat().st_size,
            "authority_witness_sha256": base.digest(local),
            "local_width": width,
            "local_height": height,
            "frame_count": frames,
            "original_bytes": int(info["size"]),
            "original_sha1": info["sha1"],
            "original_width": int(info["width"]),
            "original_height": int(info["height"]),
            "mime": info["mime"],
            "media_type": info.get("mediatype", ""),
            "source_timestamp": info["timestamp"],
            "uploader": info.get("user", ""),
            "artist": artist,
            "credit": credit,
            "license_short": license_short,
            "usage_terms": base.ext(metadata, "UsageTerms"),
            "license_url": license_url,
            "attribution_required": base.ext(metadata, "AttributionRequired"),
            "course_credit_author": course_credit["author"],
            "course_credit_user": course_credit["user"],
            "course_credit_repository": course_credit["repository"],
            "course_credit_license_label": course_credit["license_label"],
            "course_credit_source_filename_label": course_credit["source_filename_label"],
            "source_course_creator": "Holger Brenner / Wikiversity course page",
            "source_course_license": CURRENT_SEMANTIC_LICENSE,
            "description_pageid": int(page["pageid"]),
            "description_revid": int(desc_rev["revid"]),
            "description_parentid": int(desc_rev.get("parentid", 0)),
            "description_timestamp": desc_rev["timestamp"],
            "description_mediawiki_sha1": desc_rev["sha1"],
            "description_wikitext_bytes": base.content_bytes(desc_rev),
            "description_wikitext_sha256": base.digest_bytes(desc_content.encode("utf-8")),
            "html_animation_preserved": frames > 1,
        }
        rows.append(row)
        asset_records.append(
            {
                "asset_id": row["asset_id"],
                "reader_order": order,
                "source_parser_name": name,
                "metadata_title": page["title"],
                "description_pageid": row["description_pageid"],
                "description_revid": row["description_revid"],
                "description_parentid": row["description_parentid"],
                "description_timestamp": row["description_timestamp"],
                "description_mediawiki_sha1": row["description_mediawiki_sha1"],
                "description_wikitext_bytes": row["description_wikitext_bytes"],
                "source_timestamp": info["timestamp"],
                "source_bytes": int(info["size"]),
                "source_sha1": info["sha1"],
                "source_url": row["original_url"],
                "local_path": row["local_path"],
                "local_bytes": row["local_bytes"],
                "local_sha256": row["local_sha256"],
                "authority_witness_path": row["authority_witness_path"],
                "authority_witness_bytes": row["authority_witness_bytes"],
                "authority_witness_sha256": row["authority_witness_sha256"],
                "width": width,
                "height": height,
                "frame_count": frames,
                "mime": info["mime"],
                "license_short": license_short,
                "license_url": license_url,
                "artist": row["artist"],
                "credit": row["credit"],
                "attribution_required": row["attribution_required"],
                "course_credit_author": row["course_credit_author"],
                "course_credit_user": row["course_credit_user"],
                "course_credit_repository": row["course_credit_repository"],
                "course_credit_license_label": row["course_credit_license_label"],
                "course_credit_source_filename_label": row["course_credit_source_filename_label"],
                "html_animation_preserved": frames > 1,
            }
        )
    with RIGHTS.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    closure = {
        "schema": "brenner-unit-media-closure-v2",
        "unit": 27,
        "authority_only_boundary": True,
        "reader_media_positions": len(rows),
        "animated_html_positions": sum(1 for row in rows if row["html_animation_preserved"]),
        "unique_local_assets": len(asset_records),
        "reader_media_order": substantive,
        "metadata_file": commons_path.relative_to(ROOT).as_posix(),
        "metadata_bytes": commons_path.stat().st_size,
        "metadata_sha256": base.digest(commons_path),
        "local_pdf_metadata_file": metadata_path.relative_to(ROOT).as_posix(),
        "local_pdf_metadata_bytes": metadata_path.stat().st_size,
        "local_pdf_metadata_sha256": base.digest(metadata_path),
        "rights_file": RIGHTS.relative_to(ROOT).as_posix(),
        "rights_bytes": RIGHTS.stat().st_size,
        "rights_sha256": base.digest(RIGHTS),
        "reader_credits_required": True,
        "official_pdf_witnesses_are_not_media_positions": True,
        "accessibility": {
            "reader_media_alt_or_caption_required": True,
            "reader_media_source_names": substantive,
            "animated_assets": [item["metadata_title"] for item in asset_records if item["html_animation_preserved"]],
            "official_pdf_surfaces": [{"local_path": item["local_path"], **item["accessibility"]} for item in pdf_records],
        },
        "official_pdf_component_rights": [
            {
                key_name: item[key_name]
                for key_name in (
                    "source_file_title", "file_pageid", "file_revid", "file_mediawiki_sha1",
                    "source_timestamp", "source_bytes", "source_sha1", "local_path",
                    "local_bytes", "local_sha256", "component_license_route"
                )
            }
            for item in pdf_records
        ],
        "course_embedded_credit_labels": [
            {"source_parser_name": name, **course_credits[name]}
            for name in substantive
        ],
        "component_discrepancies": {
            "static_pdf_versus_semantic_revision_boundary": (
                "The official PDFs are unchanged 2012 static witnesses. They are not asserted to be renders "
                "of the frozen 2025 lecture or 2022 worksheet semantic revisions; the expanded TeX captures "
                "are separately byte-bound dynamic surfaces."
            ),
            "dual_pdf_file_page_license_notices": (
                "Each local file page identifies the generated print version with the current "
                "CC BY-SA 4.0 route while retaining the legacy CC BY-SA 2.0 Germany file notice."
            ),
            "media_credit_labels": [
                {
                    "source_parser_name": "Loewenzahn_20.jpg",
                    "kind": "license-version-label",
                    "course_embedded_label": "CC-BY-SA-2.5",
                    "current_commons_label": "CC BY-SA 3.0",
                    "handling": "Preserve and disclose both captured labels; follow the current Commons component route for reuse.",
                },
                {
                    "source_parser_name": "Perspective_Projection_Principle.jpg",
                    "kind": "creator-versus-course-user-credit",
                    "course_embedded_user": "Fantagu",
                    "commons_description_creator": "Joachim Baecker",
                    "current_commons_uploader": "Fantagu",
                    "handling": "Credit Joachim Baecker as the drawing creator and retain Fantagu as the course/user-uploader label.",
                },
                {
                    "source_parser_name": "Blue-sphere.png",
                    "kind": "historical-versus-current-user-credit",
                    "course_embedded_user": "Kieff",
                    "current_commons_artist": "Lucas Vieira",
                    "current_commons_uploader": "LucasVB",
                    "license_label": "Public domain",
                    "handling": "Preserve the historical course credit and the current Commons creator/uploader metadata.",
                },
            ],
        },
        "assets": asset_records,
    }
    base.write_json(CLOSURE, closure)
    return pdf_records, surfaces, closure, asset_records
def add_identity(target: dict[str, dict], record: dict) -> None:
    item = normalized_identity(record)
    previous = target.get(key(item["title"]))
    require(previous is None or previous == item, f"inconsistent repeated identity: {item['title']}")
    target[key(item["title"])] = item


def final_live_replay(
    course: dict,
    lecture: dict,
    lecture_closure: dict,
    worksheet: dict,
    worksheet_closure: dict,
    solution_records: list[dict],
    pdf_records: list[dict],
    media_records: list[dict],
) -> dict:
    expected: dict[str, dict] = {}
    add_identity(expected, course)
    for root, closure in ((lecture, lecture_closure), (worksheet, worksheet_closure)):
        add_identity(expected, root)
        for item in closure["pages"]:
            add_identity(expected, item)
    for solution in solution_records:
        root = {
            "title": solution["solution_title"],
            "pageid": solution["solution_pageid"],
            "revid": solution["solution_revid"],
            "parentid": solution["solution_parentid"],
            "timestamp": solution["solution_timestamp"],
            "mediawiki_sha1": solution["solution_mediawiki_sha1"],
            "wikitext_bytes": solution["solution_wikitext_bytes"],
        }
        add_identity(expected, root)
        for item in solution["recursive_transclusion_closure"]["pages"]:
            add_identity(expected, item)
    if EXPECTED_LIVE_UNION:
        require(len(expected) == EXPECTED_LIVE_UNION, f"semantic union identity count drift: {len(expected)}")
    requested = [item["title"] for item in sorted(expected.values(), key=lambda row: row["title"])]
    batches = []
    for offset in range(0, len(requested), 25):
        titles = requested[offset:offset + 25]
        raw, payload = base.api_raw(
            base.WIKI_API,
            {"action": "query", "prop": "revisions", "rvprop": "ids|timestamp|sha1", "titles": "|".join(titles)},
        )
        path = OUT / f"final-semantic-identity-replay-{offset // 25 + 1:02d}.json"
        base.write_bytes(path, raw)
        pages = payload.get("query", {}).get("pages", [])
        require(len(pages) == len(titles) and not any(page.get("missing") for page in pages), f"final semantic replay {path.name}")
        for page in pages:
            rev = base.revision(page)
            frozen = expected.get(key(page["title"]))
            require(frozen is not None, f"unexpected replay title: {page['title']}")
            require(
                int(page["pageid"]) == frozen["pageid"]
                and int(rev["revid"]) == frozen["revid"]
                and rev["sha1"] == frozen["mediawiki_sha1"],
                f"live semantic drift: {page['title']}",
            )
        batches.append({"file": path.name, "bytes": path.stat().st_size, "sha256": base.digest(path), "title_count": len(titles)})

    raw, payload = base.api_raw(
        base.WIKI_API,
        {
            "action": "query",
            "prop": "imageinfo|revisions",
            "iiprop": "timestamp|size|sha1",
            "rvprop": "ids|timestamp|sha1",
            "titles": "|".join(item["source_file_title"] for item in pdf_records),
        },
    )
    file_path = OUT / "final-local-pdf-identity-replay.json"
    base.write_bytes(file_path, raw)
    by_title = {key(page["title"]): page for page in payload.get("query", {}).get("pages", [])}
    for item in pdf_records:
        page = by_title.get(key(item["source_file_title"]))
        require(page is not None and not page.get("missing"), f"final PDF missing: {item['source_file_title']}")
        rev, info = base.revision(page), page["imageinfo"][0]
        require(int(rev["revid"]) == item["file_revid"] and rev["sha1"] == item["file_mediawiki_sha1"], "final PDF page drift")
        require(int(info["size"]) == item["source_bytes"] and info["sha1"] == item["source_sha1"], "final PDF bytes drift")
    commons_raw, commons_payload = base.api_raw(
        base.COMMONS_API,
        {
            "action": "query",
            "prop": "imageinfo|revisions",
            "iiprop": "timestamp|size|sha1",
            "rvprop": "ids|timestamp|sha1",
            "titles": "|".join(item["metadata_title"] for item in media_records),
        },
    )
    commons_replay_path = OUT / "final-commons-media-identity-replay.json"
    base.write_bytes(commons_replay_path, commons_raw)
    commons_pages = {
        base.file_key(page["title"]): page
        for page in commons_payload.get("query", {}).get("pages", [])
    }
    require(len(commons_pages) == len(media_records), "final Commons media count")
    for item in media_records:
        page = commons_pages.get(base.file_key(item["metadata_title"]))
        require(page is not None and not page.get("missing"), f"final Commons media missing: {item['metadata_title']}")
        rev, info = base.revision(page), page["imageinfo"][0]
        require(
            int(page["pageid"]) == item["description_pageid"]
            and int(rev["revid"]) == item["description_revid"]
            and rev["sha1"] == item["description_mediawiki_sha1"],
            f"final Commons description drift: {item['metadata_title']}",
        )
        require(
            info["timestamp"] == item["source_timestamp"]
            and int(info["size"]) == item["source_bytes"]
            and info["sha1"] == item["source_sha1"],
            f"final Commons bytes drift: {item['metadata_title']}",
        )
    latest_solution = max(solution_records, key=lambda item: item["solution_timestamp"], default=None)
    return {
        "result": "PASS",
        "semantic_unique_identity_count": len(expected),
        "semantic_batches": batches,
        "local_wikiversity_pdf_identity_count": 2,
        "local_pdf_replay_file": file_path.name,
        "local_pdf_replay_bytes": file_path.stat().st_size,
        "local_pdf_replay_sha256": base.digest(file_path),
        "commons_media_identity_count": len(media_records),
        "commons_media_replay_file": commons_replay_path.name,
        "commons_media_replay_bytes": commons_replay_path.stat().st_size,
        "commons_media_replay_sha256": base.digest(commons_replay_path),
        "latest_solution_identity_replayed": None if latest_solution is None else {
            "exercise_number": latest_solution["exercise_number"],
            "revid": latest_solution["solution_revid"],
            "timestamp": latest_solution["solution_timestamp"],
            "mediawiki_sha1": latest_solution["solution_mediawiki_sha1"],
        },
    }


def write_freeze_note(manifest_path: Path, manifest: dict) -> None:
    pdfs = {item["kind"]: item for item in manifest["official_pdf_witnesses"]}
    solutions = manifest["public_solution_transclusion_closures"]
    solution_numbers = [item["exercise_number"] for item in solutions]
    negative_numbers = manifest["solutions"]["negative_public_solution_evidence"]["negative_numbers"]
    roles = manifest["solutions"]["ordered_role_point_and_star_topology"]
    lecture_topology = manifest["transclusion_topology"]["lecture"]
    worksheet_topology = manifest["transclusion_topology"]["worksheet"]
    lines = [
        "# Unit 27 authority freeze",
        "",
        f"Frozen at {manifest['frozen_utc']} from the official German Wikiversity course {COURSE}. This is an authority boundary, not an Indonesian translation checkpoint.",
        "",
        "## Exact source boundary",
        "",
        f"- Course route: pageid {manifest['source_course_surface']['pageid']}, revid {manifest['source_course_surface']['revid']}.",
        f"- Lecture: pageid {manifest['lecture']['pageid']}, revid {manifest['lecture']['revid']}, MediaWiki SHA-1 {manifest['lecture']['mediawiki_sha1']}.",
        f"- Worksheet: pageid {manifest['worksheet']['pageid']}, revid {manifest['worksheet']['revid']}, MediaWiki SHA-1 {manifest['worksheet']['mediawiki_sha1']}.",
        f"- Topic boundary: {TOPIC_HEADING}; {', '.join(ADDITIONAL_TOPIC_HEADINGS)}.",
        f"- Lecture parser: {lecture_topology['parser_template_occurrences']} occurrences, {lecture_topology['unique_exact_titles']} exact unique dependencies plus root = {lecture_topology['with_root']} identities; SHA-256 {lecture_topology['canonical_identity_rows_sha256']}.",
        f"- Worksheet parser: {worksheet_topology['parser_template_occurrences']} occurrences, {worksheet_topology['unique_exact_titles']} exact unique dependencies plus root = {worksheet_topology['with_root']} identities; SHA-256 {worksheet_topology['canonical_identity_rows_sha256']}.",
        f"- Lecture dependency titles are exact-unique; duplicate list: {lecture_topology['duplicate_exact_titles']}.",
        f"- Course author: Holger Brenner. Exact lecture and worksheet root-revision contributor: {manifest['root_revision_contributors']['records'][0]['revision_contributor']} (recorded as revision provenance, not course authorship).",
        "- Both /latex revisions contain only {{Latex}}. Their expanded TeX files are byte-bound dynamic captures, not immutable standalone source revisions.",
        "",
        "## Exercises and solutions",
        "",
        f"Exactly 11 exercises are preserved in order: warm-up 1-7 and submitted 8-11. The submitted displayed points are 3, 3, 3, 3 ({roles['submitted_displayed_point_total']} total); there is no upload exercise and no starred exercise.",
        f"All and only public solution numbers are {solution_numbers}; exact negative API evidence covers {negative_numbers}.",
    ]
    for item in solutions:
        lines.append(
            f"- Solution {item['exercise_number']}: root plus {item['topology']['dependencies']} dependencies = "
            f"{item['topology']['with_root']} identities; SHA-256 {item['topology']['canonical_identity_rows_sha256']}."
        )
    if manifest["source_discrepancy_bindings"]:
        lines.append(f"Point-source discrepancies are preserved without reconciliation: {manifest['source_discrepancy_bindings']}.")
    else:
        lines.append("No authored-versus-displayed point discrepancy was found.")
    lines.extend(["", "## Bound source defects", ""])
    for item in manifest["source_defect_bindings"]:
        lines.append(f"- {item['id']}: {item['issue']} Reader handling: {item['reader_handling']}")
    lines.extend(
        [
            "",
            "## Media, PDFs, accessibility, and component rights",
            "",
            f"The parser exposes {manifest['images']['reader_media_positions']} substantive reader-media positions and exactly two official PDFs. All ten media originals, their exact Commons description revisions, source bytes, dimensions, authorship, and component licenses are bound in RIGHTS-unit-27.csv and ASSET_CLOSURE-unit-27.json.",
            "Each verified original is retained inside the immutable Unit 27 witness directory and admitted byte-identically at its shared authority/assets reader path; both paths and hashes are bound.",
            "The course-embedded media credit labels are also preserved. Three historical/current metadata differences are explicit: Loewenzahn carries CC-BY-SA-2.5 in the course but CC BY-SA 3.0 on current Commons; Perspective credits course user Fantagu while the Commons description names drawing creator Joachim Baecker; Blue-sphere credits historical course user Kieff while current Commons identifies Lucas Vieira / LucasVB. Preserve both sides of each record.",
            f"- Lecture PDF: {pdfs['lecture']['local_bytes']} bytes, {pdfs['lecture']['page_count']} pages, SHA-256 {pdfs['lecture']['local_sha256']}.",
            f"- Worksheet PDF: {pdfs['worksheet']['local_bytes']} bytes, {pdfs['worksheet']['page_count']} pages, SHA-256 {pdfs['worksheet']['local_sha256']}.",
            "The official PDFs are 2012 static witnesses and are not asserted to render the frozen 2025 lecture or 2022 worksheet semantic revisions; the dynamic expanded-TeX captures are separately bound.",
            "The PDF accessibility structures and extractable-text counts are recorded exactly. Each local file page carries the current CC BY-SA 4.0 print/course route alongside the legacy CC BY-SA 2.0 Germany file notice. Preserve both notices; make no blanket relicensing claim.",
            "",
            "## Replay boundary",
            "",
            f"Final live replay passed for {manifest['final_live_identity_replay']['semantic_unique_identity_count']} unique Wikiversity semantic identities, both local Wikiversity PDF identities, and {manifest['final_live_identity_replay']['commons_media_identity_count']} Commons media identities.",
            f"Manifest: {manifest_path.relative_to(ROOT).as_posix()}; {manifest_path.stat().st_size} bytes; SHA-256 {base.digest(manifest_path)}.",
            "",
        ]
    )
    FREEZE_NOTE.write_text("\n".join(lines), encoding="utf-8", newline="\n")
def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT / "UNIT_AUTHORITY_MANIFEST.json"
    if manifest_path.is_file():
        prior_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        frozen_utc = prior_manifest.get("frozen_utc")
        require(isinstance(frozen_utc, str) and frozen_utc, "prior frozen_utc")
    else:
        frozen_utc = datetime.now(timezone.utc).isoformat()

    course, _ = base.entry_surface(COURSE, "course-2012")
    assert_surface("course", course, EXPECTED_COURSE)
    lecture, lecture_parsed = base.entry_surface(LECTURE_TITLE, "lecture-27")
    worksheet, worksheet_parsed = base.entry_surface(WORKSHEET_TITLE, "worksheet-27")
    assert_surface("lecture", lecture, EXPECTED_ENTRIES["lecture"])
    assert_surface("worksheet", worksheet, EXPECTED_ENTRIES["worksheet"])
    require(TOPIC_HEADING in read_api_content(lecture), "Unit 27 topic-heading drift")
    require(all(heading in read_api_content(lecture) for heading in ADDITIONAL_TOPIC_HEADINGS), "Unit 27 additional topic-heading drift")

    lecture_latex, lecture_tex = base.latex_surface(LECTURE_TITLE + "/latex", "lecture-27")
    worksheet_latex, worksheet_tex = base.latex_surface(WORKSHEET_TITLE + "/latex", "worksheet-27")
    assert_surface("lecture /latex", lecture_latex, EXPECTED_LATEX["lecture"])
    assert_surface("worksheet /latex", worksheet_latex, EXPECTED_LATEX["worksheet"])
    require(read_api_content(lecture_latex).strip().casefold() == "{{latex}}", "lecture /latex launcher")
    require(read_api_content(worksheet_latex).strip().casefold() == "{{latex}}", "worksheet /latex launcher")
    require(lecture_tex["bytes"] > 1000 and worksheet_tex["bytes"] > 1000, "expanded TeX captures")

    lecture_closure = base.transclusion_closure(lecture_parsed, "lecture-27")
    worksheet_closure = base.transclusion_closure(worksheet_parsed, "worksheet-27")
    topology = {
        "lecture": closure_topology("lecture", lecture, lecture_parsed, lecture_closure),
        "worksheet": closure_topology("worksheet", worksheet, worksheet_parsed, worksheet_closure),
    }

    solutions = base.solution_map(worksheet, worksheet_parsed)
    require(solutions["exercise_count"] == 11, "exercise count")
    solutions = enrich_exercise_map(solutions, worksheet_parsed)
    solution_records = public_solution_closures(solutions)
    require(len(solution_records) == solutions["solution_count"], "complete public solution closure")

    rights_surface = site_rights_surface()
    contributors = root_revision_contributors(lecture, worksheet)
    source_defects = verify_source_defects()
    pdf_records, file_surfaces, media_closure, media_records = official_pdfs_and_media(lecture_parsed, worksheet_parsed)
    entry_recheck = base.final_identity_recheck(lecture["revid"], worksheet["revid"])
    live_replay = final_live_replay(
        course, lecture, lecture_closure, worksheet, worksheet_closure, solution_records, pdf_records, media_records
    )

    manifest = {
        "schema": "brenner-unit-authority-freeze-v2",
        "frozen_utc": frozen_utc,
        "unit_number": 27,
        "source_api": base.WIKI_API,
        "source_course": COURSE,
        "source_course_surface": course,
        "source_course_license": CURRENT_SEMANTIC_LICENSE,
        "source_component_license_route": {
            "semantic_site_rights": rights_surface,
            "official_pdf_legacy_notice": LEGACY_FILE_LICENSE,
            "official_pdf_current_print_version_notice": CURRENT_SEMANTIC_LICENSE,
            "no_blanket_relicensing_claim": True,
        },
        "topic_heading": TOPIC_HEADING,
        "lecture": lecture,
        "worksheet": worksheet,
        "root_revision_contributors": contributors,
        "lecture_latex_page": lecture_latex,
        "worksheet_latex_page": worksheet_latex,
        "latex_capture_semantics": (
            "Each /latex revision contains only {{Latex}}. Expanded TeX is a byte-bound "
            "dynamic capture, not an immutable standalone source revision."
        ),
        "derived_expanded_tex": [lecture_tex, worksheet_tex],
        "lecture_transclusion_closure": lecture_closure,
        "worksheet_transclusion_closure": worksheet_closure,
        "transclusion_topology": topology,
        "solutions": solutions,
        "public_solution_transclusion_closures": solution_records,
        "source_defect_bindings": source_defects,
        "source_discrepancy_bindings": solutions["point_discrepancies"],
        "images": {
            "lecture": lecture_parsed.get("images", []),
            "worksheet": worksheet_parsed.get("images", []),
            "substantive_assets": media_records,
            "reader_media_positions": len(media_records),
        },
        "official_pdf_witnesses": pdf_records,
        "official_pdf_file_description_surfaces": file_surfaces,
        "media_rights_accessibility_and_discrepancies": {
            "closure_file": CLOSURE.relative_to(ROOT).as_posix(),
            "closure_bytes": CLOSURE.stat().st_size,
            "closure_sha256": base.digest(CLOSURE),
            "rights_file": RIGHTS.relative_to(ROOT).as_posix(),
            "rights_bytes": RIGHTS.stat().st_size,
            "rights_sha256": base.digest(RIGHTS),
        },
        "entry_revision_recheck": entry_recheck,
        "final_live_identity_replay": live_replay,
    }
    manifest["files"] = [
        {"file": path.relative_to(OUT).as_posix(), "bytes": path.stat().st_size, "sha256": base.digest(path)}
        for path in sorted(OUT.rglob("*"), key=lambda item: item.as_posix())
        if path.is_file() and path.name != "UNIT_AUTHORITY_MANIFEST.json"
    ]
    external_paths = [
        *(ROOT / item["local_path"] for item in pdf_records),
        *(ROOT / item["local_path"] for item in media_records),
        RIGHTS,
        CLOSURE,
    ]
    manifest["bounded_external_files"] = [
        {"file": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": base.digest(path)}
        for path in sorted(external_paths, key=lambda item: item.as_posix())
    ]
    manifest_path = OUT / "UNIT_AUTHORITY_MANIFEST.json"
    base.write_json(manifest_path, manifest)

    replay = json.loads(manifest_path.read_text(encoding="utf-8"))
    actual_names = {
        path.relative_to(OUT).as_posix()
        for path in OUT.rglob("*")
        if path.is_file() and path.name != manifest_path.name
    }
    require(actual_names == {item["file"] for item in replay["files"]}, "manifest local inventory replay")
    for record in replay["files"]:
        path = OUT / record["file"]
        require(path.stat().st_size == record["bytes"] and base.digest(path) == record["sha256"], f"manifest replay: {path}")
    for record in replay["bounded_external_files"]:
        path = ROOT / record["file"]
        require(path.stat().st_size == record["bytes"] and base.digest(path) == record["sha256"], f"external replay: {path}")
    require(media_closure["reader_media_positions"] == 10 and len(media_closure["assets"]) == 10, "media replay")
    require(live_replay["result"] == "PASS", "live replay")
    write_freeze_note(manifest_path, manifest)

    all_topology = {**topology, **{f"solution-{item['exercise_number']:02d}": item["topology"] for item in solution_records}}
    pending = {
        kind: topology_record["canonical_identity_rows_sha256"]
        for kind, topology_record in all_topology.items()
        if EXPECTED_CLOSURES.get(kind, {}).get("canonical_sha256", "PENDING") == "PENDING"
    }
    preflight_pending = bool(
        pending
        or not EXPECTED_LIVE_UNION
        or EXPECTED_AUTHORED_POINTS is None
        or EXPECTED_PUBLIC_SOLUTION_NUMBERS is None
        or len(EXPECTED_MEDIA) != len(EXPECTED_MEDIA_NAMES)
        or any(item["local_sha256"] == "PENDING" or not item["page_count"] for item in EXPECTED_PDFS.values())
    )
    result = {
        "result": "PREFLIGHT_VALUES_REQUIRED" if preflight_pending else "PASS",
        "unit": 27,
        "pending_solution_hashes": pending,
        "observed_live_union": live_replay["semantic_unique_identity_count"],
        "lecture_closure_with_root": topology["lecture"]["with_root"],
        "worksheet_closure_with_root": topology["worksheet"]["with_root"],
        "solution_closures_with_root": [item["topology"]["with_root"] for item in solution_records],
        "exercises": solutions["exercise_count"],
        "public_solutions": solutions["solution_count"],
        "negative_solution_candidates": solutions["negative_public_solution_evidence"]["negative_count"],
        "authored_points": [item["authored_points"] for item in solutions["entries"]],
        "public_solution_numbers": [item["exercise_number"] for item in solution_records],
        "media_positions": len(media_records),
        "observed_media_identities": {
            item["source_parser_name"]: {
                "pageid": item["description_pageid"],
                "revid": item["description_revid"],
                "parentid": item["description_parentid"],
                "timestamp": item["description_timestamp"],
                "sha1": item["description_mediawiki_sha1"],
                "wikitext_bytes": item["description_wikitext_bytes"],
                "source_timestamp": item["source_timestamp"],
                "source_bytes": item["source_bytes"],
                "source_sha1": item["source_sha1"],
                "width": item["width"],
                "height": item["height"],
            }
            for item in media_records
        },
        "observed_pdf_values": {
            item["kind"]: {
                "local_sha256": item["local_sha256"],
                "page_count": item["page_count"],
                "accessibility": item["accessibility"],
            }
            for item in pdf_records
        },
        "official_pdf_pages": [item["page_count"] for item in pdf_records],
        "manifest_bytes": manifest_path.stat().st_size,
        "manifest_sha256": base.digest(manifest_path),
        "freeze_note_bytes": FREEZE_NOTE.stat().st_size,
        "freeze_note_sha256": base.digest(FREEZE_NOTE),
        "rights_bytes": RIGHTS.stat().st_size,
        "rights_sha256": base.digest(RIGHTS),
        "closure_bytes": CLOSURE.stat().st_size,
        "closure_sha256": base.digest(CLOSURE),
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["result"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
