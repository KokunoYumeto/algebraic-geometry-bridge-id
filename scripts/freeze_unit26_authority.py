#!/usr/bin/env python3
"""Freeze the complete bounded official Unit 26 Wikiversity authority closure.

Unit 26 is the second admitted unit from Brenner's complete 2012 course.  This
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
from datetime import datetime, timezone
from pathlib import Path

import freeze_unit12_authority as base
from freeze_no_image_unit_rights import EMPTY_RIGHTS_FIELDS


ROOT = Path(__file__).resolve().parents[1]
UNIT = 26
COURSE = "Kurs:Algebraische Kurven (Osnabrück 2012)"
LECTURE_TITLE = f"{COURSE}/Vorlesung 26"
WORKSHEET_TITLE = f"{COURSE}/Arbeitsblatt 26"
OUT = ROOT / "authority" / "wikiversity" / "unit-26"
ARTIFACTS = ROOT / "authority" / "artifacts"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-26.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-26.json"
FREEZE_NOTE = ROOT / "authority" / "UNIT_26_AUTHORITY_FREEZE.md"

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
base.USER_AGENT = "O016-unit26-authority-freeze/1.0 (bounded educational preservation)"

CURRENT_SEMANTIC_LICENSE = "CC BY-SA 4.0"
LEGACY_FILE_LICENSE = "CC BY-SA 2.0 Germany"
TOPIC_HEADING = "Die Schnittmultiplizität"

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
        "pageid": 50732,
        "revid": 793526,
        "parentid": 538867,
        "timestamp": "2022-08-25T06:09:17Z",
        "sha1": "57845c7bb535d0cccde6d289409a8dbbe684f2d8",
        "wikitext_bytes": 558,
    },
    "worksheet": {
        "pageid": 50761,
        "revid": 793494,
        "parentid": 324706,
        "timestamp": "2022-08-25T06:04:07Z",
        "sha1": "10aad7862403732dbaa5a05ae637a084c2758751",
        "wikitext_bytes": 1666,
    },
}
EXPECTED_LATEX = {
    "lecture": {
        "pageid": 51878,
        "revid": 806124,
        "parentid": 796343,
        "timestamp": "2022-09-18T07:14:52Z",
        "sha1": "1d092e4f15139d9908d36c4d64a1f4fde570e1ba",
        "wikitext_bytes": 9,
    },
    "worksheet": {
        "pageid": 53019,
        "revid": 806092,
        "parentid": 796311,
        "timestamp": "2022-09-18T07:09:42Z",
        "sha1": "1d092e4f15139d9908d36c4d64a1f4fde570e1ba",
        "wikitext_bytes": 9,
    },
}
EXPECTED_CLOSURES = {
    "lecture": {
        "dependencies": 118,
        "with_root": 119,
        "canonical_sha256": "f1a064c0531f9079633a57009c565f20a0520a0ef10cb2336ad3b52aa2d331b8",
    },
    "worksheet": {
        "dependencies": 57,
        "with_root": 58,
        "canonical_sha256": "158fd9f6495ee9763d9e01cc1c0969a6be7c8b194dd88c4f8b12edbad900211f",
    },
    "solution-04": {
        "dependencies": 9,
        "with_root": 10,
        "canonical_sha256": "8fd91e101676ccbe314c5905bb2ac8ccbf457c5d629962206124b6878c212d30",
    },
}
EXPECTED_SOLUTIONS = {
    4: {
        "pageid": 21344,
        "revid": 1112503,
        "parentid": 1011285,
        "timestamp": "2026-08-21T15:27:54Z",
        "sha1": "82d108d8f5b167d377b1f0a2ec03fa72073786d2",
        "wikitext_bytes": 1365,
    },
}
EXPECTED_AUTHORED_POINTS = [2, 2, 3, 4, 4, 4, 4, 4, 4, 3, 8]
EXPECTED_DISPLAYED_POINTS = {3: 3, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 10: 3, 11: 8}
EXPECTED_PDFS = {
    "lecture": {
        "file_title": "Datei:Algebraische Kurven (Osnabrück 2012)Vorlesung26.pdf",
        "file_pageid": 53374,
        "file_revid": 321257,
        "file_parentid": 314271,
        "file_timestamp": "2012-07-10T12:59:55Z",
        "file_sha1": "c2d188d5f445c7dedd05ac35a3e290b0307647e1",
        "source_timestamp": "2012-07-10T12:59:55Z",
        "source_bytes": 89958,
        "source_sha1": "1b27e2c5d0bf430250d722751382ee3fdb129c6b",
        "local_sha256": "9ec109463f2fe8f00ca9d3f6edb6f3a604d8c5c6f79ed5dd6584d41456da10c7",
        "page_count": 7,
    },
    "worksheet": {
        "file_title": "Datei:Algebraische Kurven (Osnabrück 2012)Arbeitsblatt26.pdf",
        "file_pageid": 54209,
        "file_revid": 325013,
        "file_parentid": 321062,
        "file_timestamp": "2012-07-31T14:00:34Z",
        "file_sha1": "471acc9bf6c2431bacf49ef70dbdd3ac5a9cd28e",
        "source_timestamp": "2012-07-31T14:00:34Z",
        "source_bytes": 34715,
        "source_sha1": "5b91dec48ec4ae9a1fae3a8e227c570ff3361e3f",
        "local_sha256": "4b1dc786752f41daa80031e8563ba0446e2d1a6c039798779fd0681f617f1c92",
        "page_count": 2,
    },
}
EXPECTED_MEDIA = {
    "resource_title": "File:Intersect3.png",
    "metadata_title": "File:Intersect3.png",
    "pageid": 641346,
    "revid": 475878038,
    "parentid": 178377620,
    "timestamp": "2020-09-29T22:17:08Z",
    "mediawiki_sha1": "03e63ff3aa8d32cce178f10ce577b131f8f2b1c1",
    "wikitext_bytes": 1356,
    "source_timestamp": "2006-03-18T17:21:17Z",
    "source_bytes": 5018,
    "source_sha1": "26fef135fcc9d950958068778e5805830ffa8b8e",
    "source_width": 400,
    "source_height": 399,
    "selected_width": 250,
    "selected_height": 249,
    "local_path": "authority/assets/250px-Intersect3.png",
    "local_bytes": 5922,
    "local_sha256": "b29c15edf6619632fe033e0b6064c1826226abce0be6219262ca028a2a157818",
    "license_short": "CC BY-SA 3.0",
    "usage_terms": "Creative Commons Attribution-Share Alike 3.0",
    "license_url": "http://creativecommons.org/licenses/by-sa/3.0/",
}
EXPECTED_LIVE_UNION = 157


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
    expected = EXPECTED_CLOSURES[kind]
    titles = [item["title"] for item in parsed.get("templates", [])]
    require(len(titles) == len(set(titles)), f"{kind} exact-title uniqueness")
    if expected["dependencies"]:
        require(len(titles) == expected["dependencies"], f"{kind} parser occurrence count")
        require(closure["captured_page_count"] == expected["dependencies"], f"{kind} captured closure")
    require(closure["missing_page_count"] == 0, f"{kind} missing dependency")
    records = [root, *closure["pages"]]
    observed = identity_hash(records)
    if expected["with_root"]:
        require(len(records) == expected["with_root"], f"{kind} root-plus-dependency count")
    if expected["canonical_sha256"] != "PENDING":
        require(observed == expected["canonical_sha256"], f"{kind} canonical identity hash drift: {observed}")
    return {
        "parser_template_occurrences": len(titles),
        "unique_exact_titles": len(set(titles)),
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


def enrich_exercise_map(solutions: dict, worksheet_parsed: dict) -> dict:
    entries = solutions["entries"]
    require(len(entries) == 11, "Unit 26 must retain exactly eleven ordered exercises")
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
    for number, (entry, title, expected_points) in enumerate(
        zip(entries, titles, EXPECTED_AUTHORED_POINTS, strict=True), start=1
    ):
        resolved = base.resolve_title(title, mapping)
        page = pages.get(resolved) or pages.get(title)
        require(page is not None and not page.get("missing"), f"exercise source absent: {title}")
        rev = base.revision(page)
        content = rev["slots"]["main"]["content"]
        match = re.search(r"(?m)^\|Punkte\s*=\s*([^\r\n}]*)", content)
        require(match is not None and match.group(1).strip().isdigit(), f"exercise {number} authored points")
        authored_points = int(match.group(1).strip())
        require(authored_points == expected_points, f"exercise {number} authored point drift")
        role = "warm-up" if number <= 4 else "submitted"
        entry.update(
            {
                "role": role,
                "authored_points": authored_points,
                "displayed_points": EXPECTED_DISPLAYED_POINTS.get(number),
                "points_displayed_in_worksheet": number in EXPECTED_DISPLAYED_POINTS,
                "starred_in_worksheet": number == 4,
                "exercise_pageid": int(page["pageid"]),
                "exercise_revid": int(rev["revid"]),
                "exercise_parentid": int(rev.get("parentid", 0)),
                "exercise_timestamp": rev["timestamp"],
                "exercise_mediawiki_sha1": rev["sha1"],
                "exercise_wikitext_bytes": base.content_bytes(rev),
            }
        )

    parsed_order = [
        item["title"]
        for item in worksheet_parsed.get("templates", [])
        if int(item.get("ns", -1)) != 10 and item["title"].endswith("/Aufgabe")
    ]
    require(parsed_order == titles, "worksheet parser exercise order")
    toc_lines = [section["line"] for section in worksheet_parsed["tocdata"]["sections"]]
    require(len(toc_lines) == 11, "worksheet TOC exercise count")
    require([index for index, line in enumerate(toc_lines, start=1) if "*" in line] == [4], "star topology")
    for number, points in EXPECTED_DISPLAYED_POINTS.items():
        require(f"({points} Punkte)" in toc_lines[number - 1], f"exercise {number} displayed points")
    require([item["exercise_number"] for item in entries if item["has_public_solution"]] == [4], "public solution set")

    candidate = json.loads((OUT / solutions["candidate_api_file"]).read_text(encoding="utf-8"))
    candidate_pages = candidate.get("query", {}).get("pages", [])
    require(len(candidate_pages) == 11, "candidate query must return exactly eleven page records")
    negatives = []
    for item in entries:
        if item["exercise_number"] == 4:
            continue
        require(not item["has_public_solution"], f"unexpected public solution for Exercise {item['exercise_number']}")
        negatives.append({
            "exercise_number": item["exercise_number"],
            "attempted_solution_title": item["solution_title"],
            "api_missing": True,
        })
    require(len(negatives) == 10, "complete negative solution evidence")
    solutions["ordered_role_point_and_star_topology"] = {
        "warm_up_numbers": [1, 2, 3, 4],
        "submitted_numbers": [5, 6, 7, 8, 9, 10, 11],
        "upload_numbers": [],
        "authored_points": {str(i): value for i, value in enumerate(EXPECTED_AUTHORED_POINTS, start=1)},
        "displayed_points": {str(k): v for k, v in EXPECTED_DISPLAYED_POINTS.items()},
        "submitted_displayed_point_total": sum(EXPECTED_DISPLAYED_POINTS[i] for i in range(5, 12)),
        "starred_numbers": [4],
        "source_api_file": source_path.name,
        "source_api_bytes": source_path.stat().st_size,
        "source_api_sha256": base.digest(source_path),
    }
    solutions["negative_public_solution_evidence"] = {
        "candidate_query_file": solutions["candidate_api_file"],
        "candidate_query_bytes": solutions["candidate_api_bytes"],
        "candidate_query_sha256": solutions["candidate_api_sha256"],
        "exact_candidate_title_count": 11,
        "positive_numbers": [4],
        "negative_numbers": [1, 2, 3, 5, 6, 7, 8, 9, 10, 11],
        "negative_count": 10,
        "entries": negatives,
    }
    solutions["point_discrepancies"] = []
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
    require([item["exercise_number"] for item in public] == [4], "sole public solution root")
    for item in public:
        number = item["exercise_number"]
        page = pages.get(key(item["resolved_title"]))
        require(page is not None, f"public solution {number} body absent")
        rev = base.revision(page)
        expected = EXPECTED_SOLUTIONS[number]
        actual = {
            "pageid": int(page["pageid"]),
            "revid": int(rev["revid"]),
            "parentid": int(rev.get("parentid", 0)),
            "timestamp": rev["timestamp"],
            "sha1": rev["sha1"],
            "wikitext_bytes": base.content_bytes(rev),
        }
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
    record, parsed = base.entry_surface(title, f"{kind}-26-file-description")
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
    closure = base.transclusion_closure(parsed, f"{kind}-26-file-description")
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


def official_pdfs_and_media(lecture_parsed: dict, worksheet_parsed: dict) -> tuple[list[dict], list[dict], dict]:
    image_names = list(dict.fromkeys(lecture_parsed.get("images", []) + worksheet_parsed.get("images", [])))
    pdf_names = [name for name in image_names if name.casefold().endswith(".pdf")]
    substantive = [name for name in image_names if not name.casefold().endswith(".pdf")]
    require(substantive == ["Intersect3.png"], f"Unit 26 substantive media topology: {substantive}")
    require(len(pdf_names) == 2, f"Unit 26 official PDF topology: {pdf_names}")
    expected_names = {
        value["file_title"].split(":", 1)[1].replace(" ", "_").casefold()
        for value in EXPECTED_PDFS.values()
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
    surfaces, records = [], []
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
        data = base.fetch(info["url"])
        require(len(data) == expected["source_bytes"], f"{kind} PDF byte count")
        require(base.digest_bytes(data, "sha1") == expected["source_sha1"], f"{kind} PDF SHA-1")
        local = ARTIFACTS / f"{kind}-26-official.pdf"
        base.write_bytes(local, data)
        require(base.digest(local) == expected["local_sha256"], f"{kind} PDF SHA-256")
        reader = base.PdfReader(str(local))
        require(not reader.is_encrypted and len(reader.pages) == expected["page_count"], f"{kind} PDF structure")
        page_text = [(pdf_page.extract_text() or "") for pdf_page in reader.pages]
        root = reader.trailer["/Root"]
        mark_info = root.get("/MarkInfo")
        if hasattr(mark_info, "get_object"):
            mark_info = mark_info.get_object()
        tagged = bool(mark_info and mark_info.get("/Marked", False))
        structure = root.get("/StructTreeRoot") is not None
        language = root.get("/Lang")
        outlines = pdf_outline_count(reader)
        require(not tagged and not structure and language is None and outlines == 0, f"{kind} PDF accessibility topology")
        surface, surface_closure = file_description_surface(kind, expected["file_title"], expected)
        surfaces.append({"kind": kind, "entry": surface, "recursive_transclusion_closure": surface_closure})
        records.append(
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
                        "Preserve both notices: the current print-version/course route is CC BY-SA 4.0, "
                        "while the unchanged 2012 file page retains CC BY-SA 2.0 Germany."
                    ),
                },
            }
        )

    media_raw, media_payload = base.api_raw(
        base.COMMONS_API,
        {
            "action": "query",
            "prop": "imageinfo|revisions",
            "iiprop": "timestamp|user|url|size|sha1|mime|mediatype|extmetadata",
            "iiurlwidth": 250,
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "main",
            "titles": EXPECTED_MEDIA["metadata_title"],
        },
    )
    media_metadata_path = OUT / "commons-intersect3-metadata-api.json"
    base.write_bytes(media_metadata_path, media_raw)
    media_page = base.one_page(media_payload)
    media_rev = base.revision(media_page)
    media_info = media_page["imageinfo"][0]
    media_actual = {
        "pageid": int(media_page["pageid"]),
        "revid": int(media_rev["revid"]),
        "parentid": int(media_rev.get("parentid", 0)),
        "timestamp": media_rev["timestamp"],
        "mediawiki_sha1": media_rev["sha1"],
        "wikitext_bytes": base.content_bytes(media_rev),
        "source_timestamp": media_info["timestamp"],
        "source_bytes": int(media_info["size"]),
        "source_sha1": media_info["sha1"],
        "source_width": int(media_info["width"]),
        "source_height": int(media_info["height"]),
        "selected_width": int(media_info["thumbwidth"]),
        "selected_height": int(media_info["thumbheight"]),
    }
    require(
        media_actual
        == {name: EXPECTED_MEDIA[name] for name in media_actual},
        f"Intersect3 Commons identity drift: {media_actual}",
    )
    require(media_info["mime"] == "image/png" and media_info.get("mediatype") == "BITMAP", "Intersect3 media type")
    metadata = media_info.get("extmetadata", {})
    require(base.ext(metadata, "LicenseShortName") == EXPECTED_MEDIA["license_short"], "Intersect3 license short name")
    require(base.ext(metadata, "UsageTerms") == EXPECTED_MEDIA["usage_terms"], "Intersect3 usage terms")
    require(base.ext(metadata, "LicenseUrl") == EXPECTED_MEDIA["license_url"], "Intersect3 license URL")

    local_media = ROOT / EXPECTED_MEDIA["local_path"]
    require(local_media.is_file() and not local_media.is_symlink(), "Intersect3 local reader asset")
    require(
        local_media.stat().st_size == EXPECTED_MEDIA["local_bytes"]
        and base.digest(local_media) == EXPECTED_MEDIA["local_sha256"],
        "Intersect3 local reader bytes",
    )
    selected_bytes = base.fetch(media_info["thumburl"])
    require(
        len(selected_bytes) == EXPECTED_MEDIA["local_bytes"]
        and hashlib.sha256(selected_bytes).hexdigest() == EXPECTED_MEDIA["local_sha256"]
        and selected_bytes == local_media.read_bytes(),
        "Intersect3 live thumbnail bytes",
    )
    with base.Image.open(local_media) as image:
        require(
            (int(image.width), int(image.height), int(getattr(image, "n_frames", 1)))
            == (EXPECTED_MEDIA["selected_width"], EXPECTED_MEDIA["selected_height"], 1),
            "Intersect3 decoded image topology",
        )
    description_content = media_rev["slots"]["main"]["content"]
    rights_row = {field: "" for field in EMPTY_RIGHTS_FIELDS}
    rights_row.update(
        {
            "asset_id": "br-ak-u26-media-001",
            "reader_order": 1,
            "reader_caption_id": "br-ak-u26-media-001-caption",
            "reader_alt_id": "br-ak-u26-media-001-alt",
            "resource_title": EXPECTED_MEDIA["resource_title"],
            "metadata_title": media_page["title"],
            "repository": "commons",
            "description_url": media_info["descriptionurl"],
            "original_url": media_info["url"].split("?", 1)[0],
            "selected_url": media_info["thumburl"],
            "selected_form": "official Commons thumbnail (250px)",
            "local_path": EXPECTED_MEDIA["local_path"],
            "local_bytes": local_media.stat().st_size,
            "local_sha256": base.digest(local_media),
            "local_width": EXPECTED_MEDIA["selected_width"],
            "local_height": EXPECTED_MEDIA["selected_height"],
            "frame_count": 1,
            "original_bytes": EXPECTED_MEDIA["source_bytes"],
            "original_sha1": EXPECTED_MEDIA["source_sha1"],
            "original_width": EXPECTED_MEDIA["source_width"],
            "original_height": EXPECTED_MEDIA["source_height"],
            "mime": media_info["mime"],
            "media_type": media_info.get("mediatype", ""),
            "source_timestamp": media_info["timestamp"],
            "uploader": media_info.get("user", ""),
            "artist": base.ext(metadata, "Artist"),
            "credit": base.ext(metadata, "Credit"),
            "license_short": EXPECTED_MEDIA["license_short"],
            "usage_terms": EXPECTED_MEDIA["usage_terms"],
            "license_url": EXPECTED_MEDIA["license_url"],
            "attribution_required": base.ext(metadata, "AttributionRequired") or "true",
            "source_course_creator": "Holger Brenner / Wikiversity course page",
            "source_course_license": CURRENT_SEMANTIC_LICENSE,
        }
    )
    with RIGHTS.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=EMPTY_RIGHTS_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerow(rights_row)
    asset_record = {
        "asset_id": rights_row["asset_id"],
        "reader_order": 1,
        "reader_caption_id": rights_row["reader_caption_id"],
        "reader_alt_id": rights_row["reader_alt_id"],
        "repository": "commons",
        "resource_title": EXPECTED_MEDIA["resource_title"],
        "metadata_title": media_page["title"],
        "description_pageid": int(media_page["pageid"]),
        "description_revid": int(media_rev["revid"]),
        "description_parentid": int(media_rev.get("parentid", 0)),
        "description_timestamp": media_rev["timestamp"],
        "description_mediawiki_sha1": media_rev["sha1"],
        "description_wikitext_bytes": base.content_bytes(media_rev),
        "description_wikitext_sha256": hashlib.sha256(description_content.encode("utf-8")).hexdigest(),
        "source_timestamp": media_info["timestamp"],
        "original_bytes": int(media_info["size"]),
        "original_sha1": media_info["sha1"],
        "original_width": int(media_info["width"]),
        "original_height": int(media_info["height"]),
        "selected_url": media_info["thumburl"],
        "selected_form": "official Commons thumbnail (250px)",
        "local_path": EXPECTED_MEDIA["local_path"],
        "local_bytes": local_media.stat().st_size,
        "local_sha256": base.digest(local_media),
        "width": EXPECTED_MEDIA["selected_width"],
        "height": EXPECTED_MEDIA["selected_height"],
        "frame_count": 1,
        "license_short": EXPECTED_MEDIA["license_short"],
        "usage_terms": EXPECTED_MEDIA["usage_terms"],
        "license_url": EXPECTED_MEDIA["license_url"],
        "attribution_required": True,
        "html_animation_preserved": False,
    }
    closure = {
        "schema": "brenner-unit-media-closure-v2",
        "unit": 26,
        "authority_only_boundary": True,
        "reader_media_positions": 1,
        "animated_html_positions": 0,
        "unique_local_assets": 1,
        "metadata_file": media_metadata_path.relative_to(ROOT).as_posix(),
        "metadata_bytes": media_metadata_path.stat().st_size,
        "metadata_sha256": base.digest(media_metadata_path),
        "local_pdf_metadata_file": metadata_path.relative_to(ROOT).as_posix(),
        "local_pdf_metadata_bytes": metadata_path.stat().st_size,
        "local_pdf_metadata_sha256": base.digest(metadata_path),
        "rights_file": RIGHTS.relative_to(ROOT).as_posix(),
        "rights_bytes": RIGHTS.stat().st_size,
        "rights_sha256": base.digest(RIGHTS),
        "reader_credits_file": None,
        "reader_credits_required": True,
        "official_pdf_witnesses_are_not_media_positions": True,
        "accessibility": {
            "reader_media_alt_or_caption_required": True,
            "planned_caption_id": rights_row["reader_caption_id"],
            "planned_alt_id": rights_row["reader_alt_id"],
            "reason": "The Unit 26 lecture has one static Commons intersection diagram.",
            "official_pdf_surfaces": [{"local_path": item["local_path"], **item["accessibility"]} for item in records],
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
            for item in records
        ],
        "component_discrepancies": {
            "dual_license_notices": (
                "Each local file page identifies the generated print version with the current "
                "CC BY-SA 4.0 route while retaining the legacy CC BY-SA 2.0 Germany file notice."
            ),
            "exercise_point_discrepancies": [],
        },
        "assets": [asset_record],
    }
    base.write_json(CLOSURE, closure)
    return records, surfaces, closure


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
            "titles": EXPECTED_MEDIA["metadata_title"],
        },
    )
    commons_path = OUT / "final-commons-media-identity-replay.json"
    base.write_bytes(commons_path, commons_raw)
    commons_page = base.one_page(commons_payload)
    commons_rev = base.revision(commons_page)
    commons_info = commons_page["imageinfo"][0]
    require(
        int(commons_page["pageid"]) == EXPECTED_MEDIA["pageid"]
        and int(commons_rev["revid"]) == EXPECTED_MEDIA["revid"]
        and commons_rev["sha1"] == EXPECTED_MEDIA["mediawiki_sha1"],
        "final Intersect3 description drift",
    )
    require(
        int(commons_info["size"]) == EXPECTED_MEDIA["source_bytes"]
        and commons_info["sha1"] == EXPECTED_MEDIA["source_sha1"],
        "final Intersect3 source bytes drift",
    )
    return {
        "result": "PASS",
        "semantic_unique_identity_count": len(expected),
        "semantic_batches": batches,
        "local_wikiversity_pdf_identity_count": 2,
        "local_pdf_replay_file": file_path.name,
        "local_pdf_replay_bytes": file_path.stat().st_size,
        "local_pdf_replay_sha256": base.digest(file_path),
        "commons_media_identity_count": 1,
        "commons_media_replay_file": commons_path.name,
        "commons_media_replay_bytes": commons_path.stat().st_size,
        "commons_media_replay_sha256": base.digest(commons_path),
        "latest_solution_identity_replayed": {
            "exercise_number": 4,
            "revid": EXPECTED_SOLUTIONS[4]["revid"],
            "timestamp": EXPECTED_SOLUTIONS[4]["timestamp"],
            "mediawiki_sha1": EXPECTED_SOLUTIONS[4]["sha1"],
        },
    }


def write_freeze_note(manifest_path: Path, manifest: dict) -> None:
    pdfs = {item["kind"]: item for item in manifest["official_pdf_witnesses"]}
    solutions = manifest["public_solution_transclusion_closures"]
    lines = [
        "# Unit 26 authority freeze",
        "",
        f"Frozen at {manifest['frozen_utc']} from the official German Wikiversity course {COURSE}. This is an authority boundary, not an Indonesian translation checkpoint.",
        "",
        "## Exact source boundary",
        "",
        f"- Course route: pageid {manifest['source_course_surface']['pageid']}, revid {manifest['source_course_surface']['revid']}.",
        f"- Lecture: pageid {manifest['lecture']['pageid']}, revid {manifest['lecture']['revid']}, MediaWiki SHA-1 {manifest['lecture']['mediawiki_sha1']}.",
        f"- Worksheet: pageid {manifest['worksheet']['pageid']}, revid {manifest['worksheet']['revid']}, MediaWiki SHA-1 {manifest['worksheet']['mediawiki_sha1']}.",
        f"- Topic heading: {TOPIC_HEADING}.",
        f"- Lecture closure: {manifest['transclusion_topology']['lecture']['dependencies']} dependencies plus root = {manifest['transclusion_topology']['lecture']['with_root']} identities; SHA-256 {manifest['transclusion_topology']['lecture']['canonical_identity_rows_sha256']}.",
        f"- Worksheet closure: {manifest['transclusion_topology']['worksheet']['dependencies']} dependencies plus root = {manifest['transclusion_topology']['worksheet']['with_root']} identities; SHA-256 {manifest['transclusion_topology']['worksheet']['canonical_identity_rows_sha256']}.",
        "- Both /latex revisions contain only {{Latex}}. Their expanded TeX files are byte-bound dynamic captures, not immutable standalone source revisions.",
        "",
        "## Exercises and solutions",
        "",
        "Exactly 11 exercises are preserved in order: warm-up 1-4 and submitted 5-11. Exercise 3 is a displayed three-point warm-up. The submitted displayed points are 4, 4, 4, 4, 4, 3, and 8 (31 total). Exercise 4 is starred and is the only public solution.",
        f"- Solution 4: root plus {solutions[0]['topology']['dependencies']} dependencies = {solutions[0]['topology']['with_root']} identities; SHA-256 {solutions[0]['topology']['canonical_identity_rows_sha256']}.",
        "The exact 11-title candidate API batch proves the other 10 solution pages absent. The live Exercise 4 solution identity is included in the final replay.",
        "All worksheet-displayed point values agree with their frozen task-page authored values; no point discrepancy is recorded.",
        "",
        "## PDFs, accessibility, and component rights",
        "",
        "The lecture exposes one substantive static reader image, Intersect3.png, in addition to the two official PDFs. The reader reuses the already frozen 250px Commons thumbnail, while RIGHTS-unit-26.csv and ASSET_CLOSURE-unit-26.json bind its exact CC BY-SA 3.0 component route and accessibility identifiers.",
        f"- Lecture PDF: {pdfs['lecture']['local_bytes']} bytes, {pdfs['lecture']['page_count']} pages, SHA-256 {pdfs['lecture']['local_sha256']}.",
        f"- Worksheet PDF: {pdfs['worksheet']['local_bytes']} bytes, {pdfs['worksheet']['page_count']} pages, SHA-256 {pdfs['worksheet']['local_sha256']}.",
        "Both PDFs are unencrypted and text-extractable but untagged, with no structure tree, document language, or outline. Each file page carries the current CC BY-SA 4.0 print/course route alongside the legacy CC BY-SA 2.0 Germany file notice. Preserve both notices; make no blanket relicensing claim.",
        "",
        "## Replay boundary",
        "",
        f"Final live replay passed for {manifest['final_live_identity_replay']['semantic_unique_identity_count']} unique semantic identities and both local Wikiversity PDF identities.",
        f"Manifest: {manifest_path.relative_to(ROOT).as_posix()}; {manifest_path.stat().st_size} bytes; SHA-256 {base.digest(manifest_path)}.",
        "",
    ]
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
    lecture, lecture_parsed = base.entry_surface(LECTURE_TITLE, "lecture-26")
    worksheet, worksheet_parsed = base.entry_surface(WORKSHEET_TITLE, "worksheet-26")
    assert_surface("lecture", lecture, EXPECTED_ENTRIES["lecture"])
    assert_surface("worksheet", worksheet, EXPECTED_ENTRIES["worksheet"])
    require(TOPIC_HEADING in read_api_content(lecture), "Unit 26 topic-heading drift")

    lecture_latex, lecture_tex = base.latex_surface(LECTURE_TITLE + "/latex", "lecture-26")
    worksheet_latex, worksheet_tex = base.latex_surface(WORKSHEET_TITLE + "/latex", "worksheet-26")
    assert_surface("lecture /latex", lecture_latex, EXPECTED_LATEX["lecture"])
    assert_surface("worksheet /latex", worksheet_latex, EXPECTED_LATEX["worksheet"])
    require(read_api_content(lecture_latex).strip().casefold() == "{{latex}}", "lecture /latex launcher")
    require(read_api_content(worksheet_latex).strip().casefold() == "{{latex}}", "worksheet /latex launcher")
    require(lecture_tex["bytes"] > 1000 and worksheet_tex["bytes"] > 1000, "expanded TeX captures")

    lecture_closure = base.transclusion_closure(lecture_parsed, "lecture-26")
    worksheet_closure = base.transclusion_closure(worksheet_parsed, "worksheet-26")
    topology = {
        "lecture": closure_topology("lecture", lecture, lecture_parsed, lecture_closure),
        "worksheet": closure_topology("worksheet", worksheet, worksheet_parsed, worksheet_closure),
    }

    solutions = base.solution_map(worksheet, worksheet_parsed)
    require(solutions["exercise_count"] == 11 and solutions["solution_count"] == 1, "exercise/solution count")
    solutions = enrich_exercise_map(solutions, worksheet_parsed)
    solution_records = public_solution_closures(solutions)
    require(len(solution_records) == 1, "complete public solution closure")

    rights_surface = site_rights_surface()
    pdf_records, file_surfaces, media_closure = official_pdfs_and_media(lecture_parsed, worksheet_parsed)
    entry_recheck = base.final_identity_recheck(lecture["revid"], worksheet["revid"])
    live_replay = final_live_replay(
        course, lecture, lecture_closure, worksheet, worksheet_closure, solution_records, pdf_records
    )

    manifest = {
        "schema": "brenner-unit-authority-freeze-v2",
        "frozen_utc": frozen_utc,
        "unit_number": 26,
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
        "source_defect_bindings": [],
        "source_discrepancy_bindings": solutions["point_discrepancies"],
        "images": {
            "lecture": lecture_parsed.get("images", []),
            "worksheet": worksheet_parsed.get("images", []),
            "substantive_assets": ["Intersect3.png"],
            "reader_media_positions": 1,
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
    external_paths = [
        *(ROOT / item["local_path"] for item in pdf_records),
        ROOT / EXPECTED_MEDIA["local_path"],
        RIGHTS,
        CLOSURE,
    ]
    manifest["bounded_external_files"] = [
        {"file": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": base.digest(path)}
        for path in sorted(external_paths, key=lambda item: item.as_posix())
    ]
    base.write_json(manifest_path, manifest)

    replay = json.loads(manifest_path.read_text(encoding="utf-8"))
    actual_names = {path.name for path in OUT.iterdir() if path.is_file() and path.name != manifest_path.name}
    require(actual_names == {item["file"] for item in replay["files"]}, "manifest local inventory replay")
    for record in replay["files"]:
        path = OUT / record["file"]
        require(path.stat().st_size == record["bytes"] and base.digest(path) == record["sha256"], f"manifest replay: {path}")
    for record in replay["bounded_external_files"]:
        path = ROOT / record["file"]
        require(path.stat().st_size == record["bytes"] and base.digest(path) == record["sha256"], f"external replay: {path}")
    require(
        media_closure["reader_media_positions"] == 1
        and len(media_closure["assets"]) == 1
        and media_closure["assets"][0]["local_sha256"] == EXPECTED_MEDIA["local_sha256"],
        "single-media replay",
    )
    require(live_replay["result"] == "PASS", "live replay")
    write_freeze_note(manifest_path, manifest)

    observed_topologies = {
        "lecture": topology["lecture"],
        "worksheet": topology["worksheet"],
        "solution-04": solution_records[0]["topology"],
    }
    pending = {
        kind: {
            "dependencies": record["dependencies"],
            "with_root": record["with_root"],
            "canonical_sha256": record["canonical_identity_rows_sha256"],
        }
        for kind, record in observed_topologies.items()
        if EXPECTED_CLOSURES[kind]["canonical_sha256"] == "PENDING"
    }
    result = {
        "result": "PASS" if not pending and EXPECTED_LIVE_UNION else "PREFLIGHT_VALUES_REQUIRED",
        "unit": 26,
        "pending_topologies": pending,
        "observed_live_union": live_replay["semantic_unique_identity_count"],
        "lecture_closure_with_root": topology["lecture"]["with_root"],
        "worksheet_closure_with_root": topology["worksheet"]["with_root"],
        "solution_closures_with_root": [item["topology"]["with_root"] for item in solution_records],
        "exercises": solutions["exercise_count"],
        "public_solutions": solutions["solution_count"],
        "negative_solution_candidates": solutions["negative_public_solution_evidence"]["negative_count"],
        "media_positions": 1,
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
