#!/usr/bin/env python3
"""Freeze the bounded official Unit 24 Wikiversity authority closure.

Unit 24 comes from the complete 2012 course rather than the later 2025-2026
surface.  This authority-only capture preserves the exact semantic entries,
their recursively expanded dependencies, the dynamic /latex witnesses, the
ordered exercise/public-solution topology, and both official local-Wikiversity
PDF files.  It records the old PDF/file CC BY-SA 2.0 Germany notice separately
from the current CC BY-SA 4.0 course/site notice and does not translate source
text or silently absorb known source defects.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import freeze_unit12_authority as base
from freeze_no_image_unit_rights import EMPTY_RIGHTS_FIELDS


ROOT = Path(__file__).resolve().parents[1]
UNIT = 24
UNIT_LABEL = "24"
COURSE = "Kurs:Algebraische Kurven (Osnabrück 2012)"
OUT = ROOT / "authority" / "wikiversity" / "unit-24"
ARTIFACTS = ROOT / "authority" / "artifacts"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-24.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-24.json"
FREEZE_NOTE = ROOT / "authority" / "UNIT_24_AUTHORITY_FREEZE.md"

# Redirect every imported capture primitive before its first network request.
base.UNIT = UNIT
base.COURSE = COURSE
base.OUT = OUT
base.ARTIFACTS = ARTIFACTS
base.RIGHTS = RIGHTS
base.CLOSURE = CLOSURE
base.COMMONS_META = OUT / "local-pdf-file-metadata-api.json"
base.LECTURE_TITLE = f"{COURSE}/Vorlesung 24"
base.WORKSHEET_TITLE = f"{COURSE}/Arbeitsblatt 24"
base.USER_AGENT = "O016-unit24-authority-freeze/1.0 (bounded educational preservation)"

CURRENT_SEMANTIC_LICENSE = "CC BY-SA 4.0"
LEGACY_FILE_LICENSE = "CC BY-SA 2.0 Germany"

EXPECTED_ENTRIES = {
    "lecture": {
        "pageid": 50730,
        "revid": 933672,
        "parentid": 833962,
        "timestamp": "2024-05-06T16:57:23Z",
        "sha1": "af86fa9893c96376f910495b9a5d0c8be417b09e",
        "wikitext_bytes": 2141,
    },
    "worksheet": {
        "pageid": 50759,
        "revid": 793492,
        "parentid": 324701,
        "timestamp": "2022-08-25T06:03:47Z",
        "sha1": "507a5966770c007e813734ca85da4e85f8a93b60",
        "wikitext_bytes": 1332,
    },
}

EXPECTED_LATEX = {
    "lecture": {
        "pageid": 51880,
        "revid": 806122,
        "parentid": 796341,
        "timestamp": "2022-09-18T07:14:32Z",
        "sha1": "1d092e4f15139d9908d36c4d64a1f4fde570e1ba",
        "wikitext_bytes": 9,
    },
    "worksheet": {
        "pageid": 53017,
        "revid": 806090,
        "parentid": 796309,
        "timestamp": "2022-09-18T07:09:22Z",
        "sha1": "1d092e4f15139d9908d36c4d64a1f4fde570e1ba",
        "wikitext_bytes": 9,
    },
}

EXPECTED_CLOSURES = {
    "lecture": {
        "dependencies": 121,
        "with_root": 122,
        "identity_sha256": "867955dfa799954da0c33d9b09625f7e194eda8ebfbdc23348c1c4ffbab83fa6",
    },
    "worksheet": {
        "dependencies": 64,
        "with_root": 65,
        "identity_sha256": "baf26dd0e702bc9ebb4f0466b5c0e4e3c4daea3ab028a8964da4f7b7bc128b91",
    },
    "solution": {
        "dependencies": 17,
        "with_root": 18,
        "identity_sha256": "978d772d44d664efcea08fb0de14e540f63bafeb2c1202552c4f209a8a3280a8",
    },
}

# Locally recomputed with the documented algorithm in identity_hash(): each
# root/dependency is reduced to the seven normalized identity fields, sorted by
# (title, pageid), serialized as UTF-8 canonical JSON (ensure_ascii=False,
# sort_keys=True, separators=(",", ":")), then SHA-256 hashed.
CANONICAL_IDENTITY_HASHES = {
    "lecture": "861c2d4566a137c9c3d791480bfa2f1f36a7885798f54f34c8e60557d34e75b2",
    "worksheet": "b02b815554f0c5dbb4e8f5aceb6b7cc7faa747d9c7c1aa136facd1f62d1831f1",
    "solution": "df98d341ed63b4cbd1b0051d725bfc8606937f489203941525b21bdfd54df7af",
}

EXPECTED_SOLUTION = {
    "exercise_number": 4,
    "pageid": 168447,
    "revid": 1068135,
    "parentid": 0,
    "timestamp": "2026-01-31T11:13:20Z",
    "sha1": "c7d3afd4c8e56433e1d4b12c4ebb8e10b460bec0",
    "wikitext_bytes": 882,
}

EXPECTED_EXERCISE_POINTS = [2, 2, 2, 2, 3, 5, 3, 3, 3, 6]
EXPECTED_SUBMITTED_POINTS = {6: 5, 7: 3, 8: 3, 9: 3, 10: 6}

EXPECTED_PDFS = {
    "lecture": {
        "file_title": "Datei:Algebraische Kurven (Osnabrück 2012)Vorlesung24.pdf",
        "file_pageid": 54026,
        "file_revid": 320347,
        "file_sha1": "fd0f1e2b1704cc237af58defc8c10d5aacbb2c35",
        "source_timestamp": "2012-07-03T13:50:14Z",
        "source_bytes": 90541,
        "source_sha1": "b19f86421aee262b9294058e2bc8d230e6de7fce",
        "local_sha256": "916b8d41a946cdf8ac978112a46e4f6d1dfb6c70fc0efc65a689cb8ff7205df1",
        "page_count": 6,
    },
    "worksheet": {
        "file_title": "Datei:Algebraische Kurven (Osnabrück 2012)Arbeitsblatt24.pdf",
        "file_pageid": 54022,
        "file_revid": 325009,
        "file_sha1": "fd2370fa785f842740c240da38acdead15b233c8",
        "source_timestamp": "2012-07-31T13:55:16Z",
        "source_bytes": 33474,
        "source_sha1": "fbd55561e353056ea6661f87be2c3263fd1cd373",
        "local_sha256": "733135d556513d01148333551693db2713915ee82ac8faa8ce745e966c073102",
        "page_count": 2,
    },
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


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
    return sha256_bytes(raw)


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


def assert_latex(kind: str, record: dict, expanded: dict) -> None:
    assert_surface(f"{kind} /latex", record, EXPECTED_LATEX[kind])
    payload = json.loads((OUT / record["api_file"]).read_text(encoding="utf-8"))
    content = base.revision(base.one_page(payload))["slots"]["main"]["content"]
    require(content.strip().casefold() == "{{latex}}", f"{kind} /latex launcher content")
    require(expanded["bytes"] > 1000 and len(expanded["sha256"]) == 64, f"{kind} expanded TeX")


def closure_topology(kind: str, root: dict, parsed: dict, closure: dict) -> dict:
    expected = EXPECTED_CLOSURES[kind]
    titles = [item["title"] for item in parsed.get("templates", [])]
    require(len(titles) == expected["dependencies"], f"{kind} parser occurrence count")
    require(len(set(titles)) == expected["dependencies"], f"{kind} exact-title uniqueness")
    require(len({title.replace('_', ' ').casefold() for title in titles}) == expected["dependencies"], f"{kind} casefold uniqueness")
    require(closure["captured_page_count"] == expected["dependencies"], f"{kind} captured closure")
    require(closure["missing_page_count"] == 0, f"{kind} missing dependency")
    records = [root, *closure["pages"]]
    observed_hash = identity_hash(records)
    require(len(records) == expected["with_root"], f"{kind} root-plus-dependency count")
    require(observed_hash == CANONICAL_IDENTITY_HASHES[kind], f"{kind} canonical identity hash drift: {observed_hash}")
    return {
        "parser_template_occurrences": len(titles),
        "unique_exact_titles": len(set(titles)),
        "unique_casefold_keys": len({title.replace('_', ' ').casefold() for title in titles}),
        "dependencies": closure["captured_page_count"],
        "with_root": len(records),
        "canonical_identity_rows_sha256": observed_hash,
        "canonical_identity_hash_algorithm": (
            "SHA-256 of UTF-8 JSON rows reduced to title,pageid,revid,parentid,timestamp,"
            "mediawiki_sha1,wikitext_bytes; rows sorted by (title,pageid); ensure_ascii=false; "
            "sort_keys=true; separators=(',',':')"
        ),
        "preflight_reported_identity_sha256": expected["identity_sha256"],
        "preflight_hash_serialization_status": (
            "MATCH" if observed_hash == expected["identity_sha256"] else "ALGORITHM_NOT_YET_IDENTIFIED"
        ),
    }


def site_rights_surface() -> dict:
    raw, payload = base.api_raw(
        base.WIKI_API,
        {"action": "query", "meta": "siteinfo", "siprop": "rightsinfo"},
    )
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


def enrich_exercise_map(solutions: dict, worksheet_parsed: dict) -> tuple[dict, dict[int, str]]:
    entries = solutions["entries"]
    require(len(entries) == 10, "Unit 24 must retain exactly ten ordered exercises")
    require([item["exercise_number"] for item in entries] == list(range(1, 11)), "exercise order")
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
    contents: dict[int, str] = {}
    for number, (entry, title, expected_points) in enumerate(
        zip(entries, titles, EXPECTED_EXERCISE_POINTS, strict=True), start=1
    ):
        resolved = base.resolve_title(title, mapping)
        page = pages.get(resolved) or pages.get(title)
        require(page is not None and not page.get("missing"), f"exercise source absent: {title}")
        rev = base.revision(page)
        content = rev["slots"]["main"]["content"]
        point_match = re.search(r"(?m)^\|Punkte\s*=\s*([^\r\n}]*)", content)
        require(point_match is not None and point_match.group(1).strip().isdigit(), f"exercise {number} point source")
        authored_points = int(point_match.group(1).strip())
        require(authored_points == expected_points, f"exercise {number} authored points")
        entry.update(
            {
                "role": "practice" if number <= 5 else "submitted",
                "authored_points": authored_points,
                "displayed_points": EXPECTED_SUBMITTED_POINTS.get(number),
                "points_displayed_in_worksheet": number >= 6,
                "starred_in_worksheet": number == 4,
                "exercise_pageid": int(page["pageid"]),
                "exercise_revid": int(rev["revid"]),
                "exercise_parentid": int(rev.get("parentid", 0)),
                "exercise_timestamp": rev["timestamp"],
                "exercise_mediawiki_sha1": rev["sha1"],
                "exercise_wikitext_bytes": base.content_bytes(rev),
            }
        )
        contents[number] = content

    parsed_order = [
        item["title"]
        for item in worksheet_parsed.get("templates", [])
        if int(item.get("ns", -1)) != 10 and item["title"].endswith("/Aufgabe")
    ]
    require(parsed_order == titles, "worksheet parser exercise order")
    public = [item["exercise_number"] for item in entries if item["has_public_solution"]]
    require(public == [4], f"public solution/star topology drift: {public}")
    require(sum(EXPECTED_SUBMITTED_POINTS.values()) == 20, "submitted point total")
    solutions["ordered_role_point_and_star_topology"] = {
        "practice_numbers": [1, 2, 3, 4, 5],
        "submitted_numbers": [6, 7, 8, 9, 10],
        "authored_points": {str(index): value for index, value in enumerate(EXPECTED_EXERCISE_POINTS, start=1)},
        "submitted_displayed_points": {str(key): value for key, value in EXPECTED_SUBMITTED_POINTS.items()},
        "submitted_displayed_point_total": 20,
        "starred_numbers": [4],
        "source_api_file": source_path.name,
        "source_api_bytes": source_path.stat().st_size,
        "source_api_sha256": base.digest(source_path),
    }
    map_path = OUT / "ORDERED_EXERCISE_MAP.json"
    for field in ("map_file", "map_bytes", "map_sha256"):
        solutions.pop(field, None)
    base.write_json(map_path, solutions)
    solutions["map_file"] = map_path.name
    solutions["map_bytes"] = map_path.stat().st_size
    solutions["map_sha256"] = base.digest(map_path)
    return solutions, contents


def solution_closure(solutions: dict) -> tuple[dict, str]:
    candidates = json.loads((OUT / solutions["candidate_api_file"]).read_text(encoding="utf-8"))
    pages = {
        key(page["title"]): page
        for page in candidates.get("query", {}).get("pages", [])
        if not page.get("missing")
    }
    public = [item for item in solutions["entries"] if item["has_public_solution"]]
    require(len(public) == 1 and public[0]["exercise_number"] == 4, "sole public solution")
    item = public[0]
    page = pages.get(key(item["resolved_title"]))
    require(page is not None, "public solution body absent")
    rev = base.revision(page)
    actual = {
        "exercise_number": 4,
        "pageid": int(page["pageid"]),
        "revid": int(rev["revid"]),
        "parentid": int(rev.get("parentid", 0)),
        "timestamp": rev["timestamp"],
        "sha1": rev["sha1"],
        "wikitext_bytes": base.content_bytes(rev),
    }
    require(actual == EXPECTED_SOLUTION, f"solution identity drift: {actual}")
    content = rev["slots"]["main"]["content"]
    require(not re.findall(r"\{\{\s*:\s*([^|}\n]+)", content), "solution became a wrapper")

    parse_raw, parse_payload = base.api_raw(
        base.WIKI_API,
        {
            "action": "parse",
            "oldid": int(rev["revid"]),
            "prop": "links|templates|images|externallinks|tocdata",
        },
    )
    parse_path = OUT / "solution-ex04-parse-api.json"
    base.write_bytes(parse_path, parse_raw)
    parsed = parse_payload["parse"]
    closure = base.transclusion_closure(parsed, "solution-ex04")
    root = {
        "title": page["title"],
        "pageid": page["pageid"],
        "revid": rev["revid"],
        "parentid": rev.get("parentid", 0),
        "timestamp": rev["timestamp"],
        "mediawiki_sha1": rev["sha1"],
        "wikitext_bytes": base.content_bytes(rev),
    }
    topology = closure_topology("solution", root, parsed, closure)
    return (
        {
            "exercise_number": 4,
            "solution_title": page["title"],
            "solution_pageid": int(page["pageid"]),
            "solution_revid": int(rev["revid"]),
            "solution_mediawiki_sha1": rev["sha1"],
            "direct_wrapper_dependency_titles": [],
            "parse_api_file": parse_path.name,
            "parse_api_bytes": parse_path.stat().st_size,
            "parse_api_sha256": base.digest(parse_path),
            "recursive_transclusion_closure": closure,
            "topology": topology,
        },
        content,
    )


def captured_contents(closures: list[dict]) -> dict[int, tuple[dict, str]]:
    result: dict[int, tuple[dict, str]] = {}
    for closure in closures:
        identities = {int(item["pageid"]): item for item in closure["pages"]}
        for batch in closure["batches"]:
            payload = json.loads((OUT / batch["file"]).read_text(encoding="utf-8"))
            for page in payload.get("query", {}).get("pages", []):
                rev = base.revision(page)
                result[int(page["pageid"])] = (identities[int(page["pageid"])], rev["slots"]["main"]["content"])
    return result


def source_defect_bindings(
    lecture_closure: dict,
    worksheet_closure: dict,
    solution_record: dict,
    exercise_contents: dict[int, str],
) -> list[dict]:
    all_content = captured_contents(
        [lecture_closure, worksheet_closure, solution_record["recursive_transclusion_closure"]]
    )
    exercise = next(item for item in json.loads((OUT / "ORDERED_EXERCISE_MAP.json").read_text(encoding="utf-8"))["entries"] if item["exercise_number"] == 7)
    example_pageid = 21057
    example_identity, example_content = all_content[example_pageid]
    ex7 = exercise_contents[7]
    require("X^2-Y^2-Y^3" in ex7, "Exercise 7 displayed polynomial evidence")
    require("Objektkategorie=Das Polynom Y^2-X^3-X^2" in ex7, "Exercise 7 object-category evidence")
    require("Ebene algebraische Kurve/x^2-y^2+y^3/Tangente unter Parametrisierung/t ist 2/Beispiel" in ex7, "Exercise 7 cited example evidence")
    require("V(y^2-x^2-x^3)" in example_content, "cited parametrized curve evidence")
    require("t^2-1" in example_content and "t^3-t" in example_content, "cited parametrization evidence")
    return [
        {
            "id": "AGC-U24-SRC-001",
            "exercise_number": 7,
            "kind": "displayed defining-polynomial mismatch",
            "exercise_identity": {
                "title": exercise["exercise_title"],
                "pageid": exercise["exercise_pageid"],
                "revid": exercise["exercise_revid"],
                "mediawiki_sha1": exercise["exercise_mediawiki_sha1"],
            },
            "displayed_source": "X^2-Y^2-Y^3",
            "conflicting_object_category": "Das Polynom Y^2-X^3-X^2",
            "cited_example_identity": normalized_identity(example_identity),
            "cited_example_curve": "V(y^2-x^2-x^3)",
            "cited_parametrization": "(t^2-1, t(t^2-1))",
            "required_reader_repair": (
                "Use Y^2-X^2-X^3 (equivalently y^2-x^2-x^3) so the exercise agrees with "
                "its cited parametrization and object category; disclose the repair."
            ),
        }
    ]


def file_description_surface(kind: str, title: str, expected: dict) -> tuple[dict, dict, dict]:
    record, parsed = base.entry_surface(title, f"{kind}-24-file-description")
    require(
        (record["pageid"], record["revid"], record["mediawiki_sha1"])
        == (expected["file_pageid"], expected["file_revid"], expected["file_sha1"]),
        f"{kind} file-description identity",
    )
    closure = base.transclusion_closure(parsed, f"{kind}-24-file-description")
    require(closure["missing_page_count"] == 0, f"{kind} file-description dependency")
    html_text = (OUT / record["html_file"]).read_text(encoding="utf-8").casefold()
    require("creativecommons.org/licenses/by-sa/4.0" in html_text, f"{kind} current 4.0 notice")
    require("creativecommons.org/licenses/by-sa/2.0/de" in html_text, f"{kind} legacy 2.0-DE notice")
    return record, parsed, closure


def pdf_outline_count(reader: base.PdfReader) -> int:
    try:
        outline = reader.outline
    except Exception:
        return 0
    if not outline:
        return 0
    stack = list(outline if isinstance(outline, list) else [outline])
    count = 0
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(item)
        else:
            count += 1
    return count


def official_pdfs_zero_media(
    lecture_parsed: dict,
    worksheet_parsed: dict,
) -> tuple[list[dict], list[dict], dict]:
    image_names = list(dict.fromkeys(lecture_parsed.get("images", []) + worksheet_parsed.get("images", [])))
    pdf_names = [name for name in image_names if name.casefold().endswith(".pdf")]
    substantive = [name for name in image_names if not name.casefold().endswith(".pdf")]
    require(not substantive, f"Unit 24 substantive media topology: {substantive}")
    require(len(pdf_names) == 2, f"Unit 24 official PDF topology: {pdf_names}")

    expected_names = {
        expected["file_title"].split(":", 1)[1].replace(" ", "_").casefold()
        for expected in EXPECTED_PDFS.values()
    }
    require({name.replace(" ", "_").casefold() for name in pdf_names} == expected_names, "official PDF names")
    titles = [EXPECTED_PDFS["lecture"]["file_title"], EXPECTED_PDFS["worksheet"]["file_title"]]
    raw, payload = base.api_raw(
        base.WIKI_API,
        {
            "action": "query",
            "prop": "imageinfo|revisions",
            "iiprop": "timestamp|user|url|size|sha1|mime|mediatype|extmetadata",
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "main",
            "titles": "|".join(titles),
        },
    )
    metadata_path = OUT / "local-pdf-file-metadata-api.json"
    base.write_bytes(metadata_path, raw)
    pages = {key(page["title"]): page for page in payload.get("query", {}).get("pages", [])}
    require(len(pages) == 2 and not any(page.get("missing") for page in pages.values()), "local file pages")

    file_surfaces: list[dict] = []
    records: list[dict] = []
    for kind in ("lecture", "worksheet"):
        expected = EXPECTED_PDFS[kind]
        page = pages.get(key(expected["file_title"]))
        require(page is not None and len(page.get("imageinfo", [])) == 1, f"{kind} PDF imageinfo")
        info = page["imageinfo"][0]
        rev = base.revision(page)
        actual = {
            "file_pageid": int(page["pageid"]),
            "file_revid": int(rev["revid"]),
            "file_sha1": rev["sha1"],
            "source_timestamp": info["timestamp"],
            "source_bytes": int(info["size"]),
            "source_sha1": info["sha1"],
        }
        require(actual == {name: expected[name] for name in actual}, f"{kind} PDF/file identity drift: {actual}")
        data = base.fetch(info["url"])
        require(len(data) == expected["source_bytes"], f"{kind} PDF byte count")
        require(base.digest_bytes(data, "sha1") == expected["source_sha1"], f"{kind} PDF SHA-1")
        local = ARTIFACTS / f"{kind}-24-official.pdf"
        base.write_bytes(local, data)
        require(base.digest(local) == expected["local_sha256"], f"{kind} PDF SHA-256")

        reader = base.PdfReader(str(local))
        require(not reader.is_encrypted, f"{kind} PDF encryption")
        require(len(reader.pages) == expected["page_count"], f"{kind} PDF page count")
        page_text = [(pdf_page.extract_text() or "") for pdf_page in reader.pages]
        extracted = "\n".join(page_text)
        normalized = " ".join(extracted.split()).casefold()
        root = reader.trailer["/Root"]
        mark_info = root.get("/MarkInfo")
        if hasattr(mark_info, "get_object"):
            mark_info = mark_info.get_object()
        tagged = bool(mark_info and mark_info.get("/Marked", False))
        structure = root.get("/StructTreeRoot") is not None
        lang = root.get("/Lang")
        outlines = pdf_outline_count(reader)
        require(not tagged and not structure and lang is None and outlines == 0, f"{kind} PDF accessibility topology")

        surface, _, surface_closure = file_description_surface(kind, expected["file_title"], expected)
        file_surfaces.append({"kind": kind, "entry": surface, "recursive_transclusion_closure": surface_closure})
        records.append(
            {
                "kind": kind,
                "source_file_title": page["title"],
                "file_pageid": int(page["pageid"]),
                "file_revid": int(rev["revid"]),
                "file_mediawiki_sha1": rev["sha1"],
                "file_wikitext_bytes": base.content_bytes(rev),
                "source_timestamp": info["timestamp"],
                "uploader": info.get("user", ""),
                "source_bytes": int(info["size"]),
                "source_sha1": info["sha1"],
                "source_url": info["url"],
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
                    "document_language": None,
                    "outline_or_bookmark_count": outlines,
                },
                "component_license_route": {
                    "current_print_version_notice": CURRENT_SEMANTIC_LICENSE,
                    "current_notice_evidence": surface["html_file"],
                    "legacy_file_notice": LEGACY_FILE_LICENSE,
                    "legacy_notice_evidence": surface["html_file"],
                    "embedded_pdf_label": None,
                    "interpretation": (
                        "Preserve both notices. The current print-version/course reuse route is CC BY-SA 4.0; "
                        "the unchanged 2012 file-description surface retains its CC BY-SA 2.0 Germany notice. "
                        "The PDF text itself contains no extracted license boilerplate."
                    ),
                },
                "extracted_text": extracted,
            }
        )

    with RIGHTS.open("w", encoding="utf-8", newline="") as stream:
        csv.DictWriter(stream, fieldnames=EMPTY_RIGHTS_FIELDS, lineterminator="\n").writeheader()
    closure = {
        "schema": "brenner-unit-media-closure-v2",
        "unit": 24,
        "authority_only_boundary": True,
        "reader_media_positions": 0,
        "animated_html_positions": 0,
        "unique_local_assets": 0,
        "metadata_file": metadata_path.relative_to(ROOT).as_posix(),
        "metadata_bytes": metadata_path.stat().st_size,
        "metadata_sha256": base.digest(metadata_path),
        "rights_file": RIGHTS.relative_to(ROOT).as_posix(),
        "rights_bytes": RIGHTS.stat().st_size,
        "rights_sha256": base.digest(RIGHTS),
        "reader_credits_file": None,
        "reader_credits_required": False,
        "official_pdf_witnesses_are_not_media_positions": True,
        "accessibility": {
            "reader_media_alt_or_caption_required": False,
            "reason": "The parsed Unit 24 entry surfaces contain no substantive reader media.",
            "official_pdf_surfaces": [
                {"local_path": item["local_path"], **item["accessibility"]} for item in records
            ],
        },
        "official_pdf_component_rights": [
            {
                "source_file_title": item["source_file_title"],
                "file_pageid": item["file_pageid"],
                "file_revid": item["file_revid"],
                "file_mediawiki_sha1": item["file_mediawiki_sha1"],
                "source_timestamp": item["source_timestamp"],
                "source_bytes": item["source_bytes"],
                "source_sha1": item["source_sha1"],
                "local_path": item["local_path"],
                "local_bytes": item["local_bytes"],
                "local_sha256": item["local_sha256"],
                "component_license_route": item["component_license_route"],
            }
            for item in records
        ],
        "component_discrepancies": {
            "dual_license_notices": (
                "Each local Wikiversity file page simultaneously identifies the generated print version "
                "with the current CC BY-SA 4.0 course route and retains the legacy CC BY-SA 2.0 Germany "
                "file notice. No blanket replacement or relicensing claim is made."
            ),
            "historical_pdf_math": [],
        },
        "assets": [],
    }
    base.write_json(CLOSURE, closure)
    return records, file_surfaces, closure


def bind_historical_pdf_defects(
    pdf_records: list[dict],
    lecture_closure: dict,
    media_closure: dict,
) -> list[dict]:
    lecture_pdf = next(item for item in pdf_records if item["kind"] == "lecture")
    pdf_text = lecture_pdf["extracted_text"]
    content = captured_contents([lecture_closure])

    # The two current semantic repairs are searched in the fully captured live
    # closure, while the preserved 2012 PDF provides the historical forms.
    gy_candidates = [
        (identity, text)
        for identity, text in content.values()
        if re.search(r"G[^\n]{0,100}y\^2", text, flags=re.IGNORECASE)
    ]
    bell_candidates = [
        (identity, text)
        for identity, text in content.values()
        if "a_{\\ell+1}T^{\\ell+1}" in text
    ]
    require(gy_candidates, "live G/y^2 repair evidence absent")
    require(bell_candidates, "live a_{ell+1} coefficient-symbol evidence absent")

    normalized_pdf = " ".join(pdf_text.split())
    require(re.search(r"G\s*=\s*x\s*2\s*\+\s*z\s*2", normalized_pdf, flags=re.IGNORECASE), "historical PDF G x^2 evidence absent")
    require(re.search(r"G\s*=\s*b[ℓl].{0,30}a[ℓl]\+1", normalized_pdf, flags=re.IGNORECASE), "historical PDF a_{ell+1} evidence absent")

    defects = [
        {
            "id": "AGC-U24-PDF-001",
            "kind": "historical official-PDF variable typo",
            "historical_pdf_form": "G x^2",
            "live_semantic_form": "G y^2",
            "live_identity": normalized_identity(gy_candidates[0][0]),
            "required_reader_handling": "Use the frozen live semantic y^2 form; retain the PDF only as historical evidence.",
        },
        {
            "id": "AGC-U24-PDF-002",
            "kind": "historical-PDF and current-live coefficient-symbol typo",
            "historical_pdf_form": "G=b_ell T^ell+a_{ell+1}T^{ell+1}+...",
            "live_semantic_form": "G=b_ell T^ell+a_{ell+1}T^{ell+1}+...",
            "mathematically_required_form": "G=b_ell T^ell+b_{ell+1}T^{ell+1}+...",
            "live_identity": normalized_identity(bell_candidates[0][0]),
            "preflight_claim_disposition": (
                "The supplied preflight wording claimed that the live page already had b_{ell+1}; "
                "exact pageid 20953/revid 1043192 disproves that claim."
            ),
            "required_reader_handling": "Correct a_{ell+1} to b_{ell+1} and disclose this live-source repair.",
        },
    ]
    media_closure["component_discrepancies"]["historical_pdf_math"] = defects
    base.write_json(CLOSURE, media_closure)
    return defects


def add_identity(target: dict[str, dict], record: dict) -> None:
    item = normalized_identity(record)
    previous = target.get(key(item["title"]))
    require(previous is None or previous == item, f"inconsistent repeated identity: {item['title']}")
    target[key(item["title"])] = item


def final_live_replay(
    lecture: dict,
    lecture_closure: dict,
    worksheet: dict,
    worksheet_closure: dict,
    solution_record: dict,
    pdf_records: list[dict],
) -> dict:
    expected: dict[str, dict] = {}
    for root, closure in (
        (lecture, lecture_closure),
        (worksheet, worksheet_closure),
    ):
        add_identity(expected, root)
        for item in closure["pages"]:
            add_identity(expected, item)

    solution_root = {
        "title": solution_record["solution_title"],
        "pageid": solution_record["solution_pageid"],
        "revid": solution_record["solution_revid"],
        "parentid": EXPECTED_SOLUTION["parentid"],
        "timestamp": EXPECTED_SOLUTION["timestamp"],
        "mediawiki_sha1": solution_record["solution_mediawiki_sha1"],
        "wikitext_bytes": EXPECTED_SOLUTION["wikitext_bytes"],
    }
    add_identity(expected, solution_root)
    for item in solution_record["recursive_transclusion_closure"]["pages"]:
        add_identity(expected, item)
    require(len(expected) == 159, f"semantic union identity count drift: {len(expected)}")

    requested = [item["title"] for item in sorted(expected.values(), key=lambda row: row["title"])]
    batches: list[dict] = []
    for offset in range(0, len(requested), 25):
        titles = requested[offset : offset + 25]
        raw, payload = base.api_raw(
            base.WIKI_API,
            {
                "action": "query",
                "prop": "revisions",
                "rvprop": "ids|timestamp|sha1",
                "titles": "|".join(titles),
            },
        )
        path = OUT / f"final-semantic-identity-replay-{offset // 25 + 1:02d}.json"
        base.write_bytes(path, raw)
        pages = payload.get("query", {}).get("pages", [])
        require(len(pages) == len(titles) and not any(page.get("missing") for page in pages), f"final semantic replay {path.name}")
        for page in pages:
            rev = base.revision(page)
            frozen = expected.get(key(page["title"]))
            require(frozen is not None, f"unexpected replay title: {page['title']}")
            require(int(rev["revid"]) == frozen["revid"] and rev["sha1"] == frozen["mediawiki_sha1"], f"live semantic drift: {page['title']}")
        batches.append(
            {
                "file": path.name,
                "bytes": path.stat().st_size,
                "sha256": base.digest(path),
                "title_count": len(titles),
            }
        )

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
        require(page is not None and not page.get("missing"), f"final local PDF missing: {item['source_file_title']}")
        rev = base.revision(page)
        info = page["imageinfo"][0]
        require(int(rev["revid"]) == item["file_revid"] and rev["sha1"] == item["file_mediawiki_sha1"], "final file description drift")
        require(int(info["size"]) == item["source_bytes"] and info["sha1"] == item["source_sha1"], "final PDF bytes drift")
    return {
        "result": "PASS",
        "semantic_unique_identity_count": len(expected),
        "semantic_batches": batches,
        "local_wikiversity_pdf_identity_count": 2,
        "local_pdf_replay_file": file_path.name,
        "local_pdf_replay_bytes": file_path.stat().st_size,
        "local_pdf_replay_sha256": base.digest(file_path),
    }


def write_freeze_note(manifest_path: Path, manifest: dict) -> None:
    lecture = manifest["lecture"]
    worksheet = manifest["worksheet"]
    solution = manifest["solution_transclusion_closure"]
    pdfs = {item["kind"]: item for item in manifest["official_pdf_witnesses"]}
    lines = [
        "# Unit 24 authority freeze",
        "",
        f"Frozen at `{manifest['frozen_utc']}` from the official German Wikiversity course `{COURSE}`. This is an authority boundary, not an Indonesian translation checkpoint.",
        "",
        "## Exact semantic and editable surfaces",
        "",
        f"- Lecture: pageid `{lecture['pageid']}`, revid `{lecture['revid']}`, MediaWiki SHA-1 `{lecture['mediawiki_sha1']}`, immutable oldid `{lecture['oldid_url']}`.",
        f"- Worksheet: pageid `{worksheet['pageid']}`, revid `{worksheet['revid']}`, MediaWiki SHA-1 `{worksheet['mediawiki_sha1']}`, immutable oldid `{worksheet['oldid_url']}`.",
        f"- `/latex` launchers: lecture pageid/revid `{manifest['lecture_latex_page']['pageid']}/{manifest['lecture_latex_page']['revid']}` and worksheet `{manifest['worksheet_latex_page']['pageid']}/{manifest['worksheet_latex_page']['revid']}`. Both contain exactly `{{{{Latex}}}}`; expanded TeX files are byte-bound dynamic captures, not immutable standalone source revisions.",
        f"- Lecture closure: root plus `{manifest['transclusion_topology']['lecture']['dependencies']}` exact dependencies = `{manifest['transclusion_topology']['lecture']['with_root']}` identities, SHA-256 `{manifest['transclusion_topology']['lecture']['canonical_identity_rows_sha256']}`.",
        f"- Worksheet closure: root plus `{manifest['transclusion_topology']['worksheet']['dependencies']}` exact dependencies = `{manifest['transclusion_topology']['worksheet']['with_root']}` identities, SHA-256 `{manifest['transclusion_topology']['worksheet']['canonical_identity_rows_sha256']}`.",
        "",
        "## Exercises and solution closure",
        "",
        f"The worksheet has exactly ten exercises: practice 1-5 and submitted 6-10. Submitted points are 5, 3, 3, 3, and 6 (20 total). Only Exercise 4 is starred and has a public solution. Its root plus `{solution['topology']['dependencies']}` dependencies = `{solution['topology']['with_root']}` exact identities, SHA-256 `{solution['topology']['canonical_identity_rows_sha256']}`; no dependency is missing and the solution is a direct body, not a wrapper.",
        "",
        "## Zero-media, PDFs, accessibility, and component rights",
        "",
        "The lecture and worksheet parser surfaces contain exactly the two official PDF links and no substantive reader media. `RIGHTS-unit-24.csv` is therefore intentionally header-only; `ASSET_CLOSURE-unit-24.json` records zero reader positions.",
        f"- Lecture PDF: `{pdfs['lecture']['local_bytes']}` bytes, `{pdfs['lecture']['page_count']}` pages, SHA-256 `{pdfs['lecture']['local_sha256']}`.",
        f"- Worksheet PDF: `{pdfs['worksheet']['local_bytes']}` bytes, `{pdfs['worksheet']['page_count']}` pages, SHA-256 `{pdfs['worksheet']['local_sha256']}`.",
        "Both are unencrypted and text-extractable but untagged, have no structure tree, no document language, and no outline/bookmarks. Each local Wikiversity file page simultaneously says the generated print version follows the current CC BY-SA 4.0 course route and retains a CC BY-SA 2.0 Germany file notice; the PDF text itself contains no extracted license boilerplate. Preserve both component notices and do not make a blanket relicensing claim.",
        "",
        "## Bound source and historical-PDF defects",
        "",
    ]
    for defect in manifest["source_defect_bindings"] + manifest["historical_pdf_defect_bindings"]:
        handling = defect.get("required_reader_repair") or defect.get("required_reader_handling")
        lines.append(f"- `{defect['id']}`: {defect['kind']}. Required reader handling: {handling}")
    lines.extend(
        [
            "",
            "Exercise 7's displayed `X^2-Y^2-Y^3` conflicts with both its cited parametrized curve and its object category. The derivative must use `Y^2-X^2-X^3`. The 2012 PDF's `G=x^2+z^2-1` was repaired on the live semantic page to `G=y^2+z^2-1`, so the live identity controls. By contrast, both the PDF and exact live page 20953/revision 1043192 still print `a_{ell+1}` as the second coefficient of `G`; the mathematically required and transparently disclosed derivative repair is `b_{ell+1}`.",
            "",
            "## Replay boundary",
            "",
            f"Final live replay passed for `{manifest['final_live_identity_replay']['semantic_unique_identity_count']}` unique semantic Wikiversity identities and both local Wikiversity PDF identities.",
            f"Manifest: `{manifest_path.relative_to(ROOT).as_posix()}`; `{manifest_path.stat().st_size}` bytes; SHA-256 `{base.digest(manifest_path)}`.",
            "",
        ]
    )
    FREEZE_NOTE.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    lecture, lecture_parsed = base.entry_surface(base.LECTURE_TITLE, "lecture-24")
    worksheet, worksheet_parsed = base.entry_surface(base.WORKSHEET_TITLE, "worksheet-24")
    assert_surface("lecture", lecture, EXPECTED_ENTRIES["lecture"])
    assert_surface("worksheet", worksheet, EXPECTED_ENTRIES["worksheet"])

    lecture_latex, lecture_tex = base.latex_surface(base.LECTURE_TITLE + "/latex", "lecture-24")
    worksheet_latex, worksheet_tex = base.latex_surface(base.WORKSHEET_TITLE + "/latex", "worksheet-24")
    assert_latex("lecture", lecture_latex, lecture_tex)
    assert_latex("worksheet", worksheet_latex, worksheet_tex)

    lecture_closure = base.transclusion_closure(lecture_parsed, "lecture-24")
    worksheet_closure = base.transclusion_closure(worksheet_parsed, "worksheet-24")
    topology = {
        "lecture": closure_topology("lecture", lecture, lecture_parsed, lecture_closure),
        "worksheet": closure_topology("worksheet", worksheet, worksheet_parsed, worksheet_closure),
    }

    solutions = base.solution_map(worksheet, worksheet_parsed)
    require(solutions["exercise_count"] == 10 and solutions["solution_count"] == 1, "exercise/solution count")
    solutions, exercise_contents = enrich_exercise_map(solutions, worksheet_parsed)
    solution_record, _ = solution_closure(solutions)
    source_defects = source_defect_bindings(
        lecture_closure, worksheet_closure, solution_record, exercise_contents
    )

    rights_surface = site_rights_surface()
    pdf_records, file_surfaces, media_closure = official_pdfs_zero_media(lecture_parsed, worksheet_parsed)
    historical_pdf_defects = bind_historical_pdf_defects(pdf_records, lecture_closure, media_closure)
    entry_recheck = base.final_identity_recheck(lecture["revid"], worksheet["revid"])
    live_replay = final_live_replay(
        lecture, lecture_closure, worksheet, worksheet_closure, solution_record, pdf_records
    )

    # Extracted text is evidence used for checks but would unnecessarily bloat
    # the manifest; the exact PDFs themselves remain bound external files.
    for item in pdf_records:
        item.pop("extracted_text")

    manifest = {
        "schema": "brenner-unit-authority-freeze-v2",
        "frozen_utc": datetime.now(timezone.utc).isoformat(),
        "unit_number": 24,
        "source_api": base.WIKI_API,
        "source_course": COURSE,
        "source_course_license": CURRENT_SEMANTIC_LICENSE,
        "source_component_license_route": {
            "semantic_site_rights": rights_surface,
            "official_pdf_legacy_notice": LEGACY_FILE_LICENSE,
            "official_pdf_current_print_version_notice": CURRENT_SEMANTIC_LICENSE,
            "no_blanket_relicensing_claim": True,
        },
        "lecture": lecture,
        "worksheet": worksheet,
        "lecture_latex_page": lecture_latex,
        "worksheet_latex_page": worksheet_latex,
        "latex_capture_semantics": (
            "Each /latex revision contains only {{Latex}}. Expanded TeX is a byte-bound "
            "capture of dynamic Parsoid rendering at freeze time, not immutable source closure."
        ),
        "derived_expanded_tex": [lecture_tex, worksheet_tex],
        "lecture_transclusion_closure": lecture_closure,
        "worksheet_transclusion_closure": worksheet_closure,
        "transclusion_topology": topology,
        "solutions": solutions,
        "solution_transclusion_closure": solution_record,
        "source_defect_bindings": source_defects,
        "historical_pdf_defect_bindings": historical_pdf_defects,
        "images": {
            "lecture": lecture_parsed.get("images", []),
            "worksheet": worksheet_parsed.get("images", []),
            "substantive_assets": [],
            "reader_media_positions": 0,
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
        {"file": path.name, "bytes": path.stat().st_size, "sha256": base.digest(path)}
        for path in sorted(OUT.iterdir(), key=lambda item: item.name)
        if path.is_file() and path.name != "UNIT_AUTHORITY_MANIFEST.json"
    ]
    external_paths = [*(ROOT / item["local_path"] for item in pdf_records), RIGHTS, CLOSURE]
    manifest["bounded_external_files"] = [
        {"file": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": base.digest(path)}
        for path in sorted(external_paths, key=lambda item: item.as_posix())
    ]
    manifest_path = OUT / "UNIT_AUTHORITY_MANIFEST.json"
    base.write_json(manifest_path, manifest)

    replay = json.loads(manifest_path.read_text(encoding="utf-8"))
    actual_names = {path.name for path in OUT.iterdir() if path.is_file() and path.name != manifest_path.name}
    bound_names = {item["file"] for item in replay["files"]}
    require(actual_names == bound_names, "manifest local inventory replay")
    for record in replay["files"]:
        path = OUT / record["file"]
        require(path.stat().st_size == record["bytes"] and base.digest(path) == record["sha256"], f"manifest replay: {path}")
    for record in replay["bounded_external_files"]:
        path = ROOT / record["file"]
        require(path.stat().st_size == record["bytes"] and base.digest(path) == record["sha256"], f"external replay: {path}")
    require(media_closure["reader_media_positions"] == 0 and not media_closure["assets"], "zero-media replay")
    require(live_replay["result"] == "PASS" and live_replay["semantic_unique_identity_count"] == 159, "live replay")

    write_freeze_note(manifest_path, manifest)
    result = {
        "result": "PASS",
        "unit": 24,
        "lecture_pageid": lecture["pageid"],
        "lecture_revid": lecture["revid"],
        "worksheet_pageid": worksheet["pageid"],
        "worksheet_revid": worksheet["revid"],
        "lecture_closure_with_root": topology["lecture"]["with_root"],
        "worksheet_closure_with_root": topology["worksheet"]["with_root"],
        "solution_closure_with_root": solution_record["topology"]["with_root"],
        "exercises": solutions["exercise_count"],
        "public_solutions": solutions["solution_count"],
        "media_positions": 0,
        "official_pdf_pages": [item["page_count"] for item in pdf_records],
        "live_replay_identities": live_replay["semantic_unique_identity_count"],
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
