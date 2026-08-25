#!/usr/bin/env python3
"""Freeze the bounded official Unit 23 Wikiversity/Commons authority closure.

This is an authority-only capture.  It preserves the exact live semantic
surfaces, dynamic /latex renderings, exercise/solution topology, component
rights, and official PDF witnesses without translating or correcting upstream.
Known source defects are bound explicitly so the Indonesian production lane can
repair them transparently instead of reproducing them as mathematical claims.
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
from freeze_single_image_unit_media import commons_file_title, pdf_rights, title_key


ROOT = Path(__file__).resolve().parents[1]
UNIT = 23
UNIT_LABEL = f"{UNIT:02d}"

# Redirect every imported capture primitive before the first request.
base.UNIT = UNIT
base.OUT = ROOT / "authority" / "wikiversity" / f"unit-{UNIT_LABEL}"
base.ARTIFACTS = ROOT / "authority" / "artifacts"
base.ASSETS = ROOT / "authority" / "assets"
base.RIGHTS = ROOT / "authority" / f"RIGHTS-unit-{UNIT_LABEL}.csv"
base.CLOSURE = ROOT / "authority" / f"ASSET_CLOSURE-unit-{UNIT_LABEL}.json"
# Keep the complete raw Commons response inside the explicitly owned Unit 23 tree.
base.COMMONS_META = base.OUT / "commons-pdf-metadata.json"
base.LECTURE_TITLE = f"{base.COURSE}/Vorlesung {UNIT}"
base.WORKSHEET_TITLE = f"{base.COURSE}/Arbeitsblatt {UNIT}"
base.USER_AGENT = "O016-unit23-authority-freeze/1.0 (bounded educational preservation)"

COURSE_LICENSE_TITLE = f"{base.COURSE}/Lizenzerklärung"
COURSE_LICENSE_DEPENDENCY = "Holger Brenner/Lizenzerklärung"
CURRENT_LICENSE = "CC BY-SA 4.0"
PDF_INTERNAL_LABEL = "CC-by-sa 3.0"
FREEZE_NOTE = ROOT / "authority" / "UNIT_23_AUTHORITY_FREEZE.md"

EXPECTED_ENTRIES = {
    "lecture": {
        "pageid": 165912,
        "revid": 1112318,
        "parentid": 1051403,
        "timestamp": "2026-08-21T09:42:07Z",
        "sha1": "a38160a106cf39298b3f2cb23f7880e05a5a86f7",
        "wikitext_bytes": 3363,
        "html_bytes": 137610,
        "html_sha256": "8ec4e80cb109e67aa9dba5b6c408760d77baa00c0e107409453eabe653ee5d43",
    },
    "worksheet": {
        "pageid": 165942,
        "revid": 1062659,
        "parentid": 1062658,
        "timestamp": "2025-12-19T12:06:03Z",
        "sha1": "19554b41098b4f02ac6e558145036ca293e4bbc9",
        "wikitext_bytes": 2059,
        "html_bytes": 53638,
        "html_sha256": "77cd2292bea9b63d375ee75764d369bc543fb697f030cb8d6068ec3fbff6a2c6",
    },
}

EXPECTED_LATEX = {
    "lecture": {
        "pageid": 165976,
        "revid": 1033022,
        "sha1": "3034e92c1843eab298fb5f6f859d2c89cf824d61",
        "launcher_bytes": 9,
        "html_bytes": 30809,
        "html_sha256": "fe6c4e11e73c7449e98f396b9ae2ba23204cc28500bc4dd31352b3e9e03662f6",
        "tex_bytes": 21754,
        "tex_sha256": "17aa88b5aa9a8d130f0995c036cb9ca332ef1b0feaef3b2d5ac5396e47b343a0",
    },
    "worksheet": {
        "pageid": 166036,
        "revid": 1033084,
        "sha1": "3034e92c1843eab298fb5f6f859d2c89cf824d61",
        "launcher_bytes": 9,
        "html_bytes": 13695,
        "html_sha256": "2c4229eeadf8d0b97de96e1fa3b85002c25aad436f4f4edd473c56a04f589e34",
        "tex_bytes": 8243,
        "tex_sha256": "865905ee0d321006682c162fb2d9e272f1fc251e61b8dde9844981f6baba9c0f",
    },
}

EXPECTED_SOLUTIONS = {
    4: {
        "pageid": 95515,
        "revid": 1090216,
        "sha1": "ff517116601591c109925dcf590b9f084f006e99",
        "wikitext_bytes": 1680,
        "closure_pages": 19,
    },
    5: {
        "pageid": 95541,
        "revid": 1096444,
        "sha1": "b38570ced97626358cc493bfa56a140f114e1fdf",
        "wikitext_bytes": 1433,
        "closure_pages": 13,
    },
}

HIGH_RISK_IDENTITIES = [
    ("direct derivation", 20855, 1087697),
    ("direct derivation proof", 20860, 1086465),
    ("smooth point/DVR proof", 18310, 1112317),
    ("finite jets proof", 20801, 1101516),
    ("Hilbert-Samuel proof", 20232, 1101012),
    ("smooth/DVR/multiplicity equivalence proof", 21026, 1101013),
    ("monomial-curve multiplicity section", 50931, 1103183),
    ("difference-set estimate proof", 18360, 1101495),
    ("numerical/Hilbert-Samuel equality proof", 20795, 978551),
    ("exercise 4", 95514, 1083785),
    ("solution 4", 95515, 1090216),
    ("exercise 5", 95540, 1083673),
    ("solution 5", 95541, 1096444),
    ("exercise 6 updated after official PDF", 20797, 1112488),
    ("exercise 11", 20893, 1106893),
]

EXPECTED_PDFS = {
    "lecture": {
        "commons_pageid": 182950524,
        "image_timestamp": "2026-02-02T14:29:53Z",
        "source_bytes": 191471,
        "source_sha1": "49ac49a86f62182d8d9ca00310d16f7df4911d1e",
        "local_sha256": "96fc99009c2f4640ba99db6203c06bd59e03bdc2927c1bf81302625431302724",
        "page_count": 7,
        "text_characters": 10962,
        "description_revid": 1158248366,
        "description_sha1": "ee06ff40e28a2a2d4a3d3e34ffbbf5a46c3d91cc",
        "slots": {
            "main": (321, "c16cb0ecce8504d47c3503da380b9f0af05b18bf2dbfd82f7e81308680088559"),
            "mediainfo": (1706, "e3182caa557e03ff020a17809f636f4b98e7b2f7e3bbb82fae96d0de7f14cc28"),
        },
    },
    "worksheet": {
        "commons_pageid": 182948317,
        "image_timestamp": "2026-02-02T13:34:54Z",
        "source_bytes": 159393,
        "source_sha1": "5fe6b3496a59f886e8779bb1d270977f86f4c4f0",
        "local_sha256": "6494630aba1d79f238c762b30cb382918444b19a82de3d96d66c4d6e3108d15b",
        "page_count": 5,
        "text_characters": 4165,
        "description_revid": 1168719869,
        "description_sha1": "43264b8f1626731b0598621f670b7fa4e74701ff",
        "slots": {
            "main": (327, "9f5e5853adeaba6fa173a8a83d7fa2808dccaba300bed09428338f738b0935fe"),
            "mediainfo": (3143, "50b945b267c15eb079b493c6cd91456b37a1bcf0dd20929ac0fe1bb8e57c1e16"),
        },
    },
}

EXPECTED_LICENSE = {
    "wrapper_pageid": 166921,
    "wrapper_revid": 1054579,
    "wrapper_sha1": "c914f4f47acd7cffab542e6ae29002aa9e5ced3e",
    "dependency_pageid": 102759,
    "dependency_revid": 1073083,
    "dependency_sha1": "8e7f170511053c93b240f40db64466ea27a44116",
}


def key(value: str) -> str:
    return value.replace("_", " ")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def content_from_page(page: dict) -> str:
    return base.revision(page)["slots"]["main"]["content"]


def assert_primary_surface(kind: str, record: dict) -> None:
    expected = EXPECTED_ENTRIES[kind]
    actual = {
        "pageid": record["pageid"],
        "revid": record["revid"],
        "parentid": record["parentid"],
        "timestamp": record["timestamp"],
        "sha1": record["mediawiki_sha1"],
        "wikitext_bytes": record["wikitext_bytes"],
        "html_bytes": record["html_bytes"],
        "html_sha256": record["html_sha256"],
    }
    require(actual == expected, f"{kind} primary identity drift: {actual}")


def assert_latex_surface(kind: str, record: dict, expanded: dict) -> None:
    expected = EXPECTED_LATEX[kind]
    actual = {
        "pageid": record["pageid"],
        "revid": record["revid"],
        "sha1": record["mediawiki_sha1"],
        "launcher_bytes": record["wikitext_bytes"],
        "html_bytes": record["html_bytes"],
        "html_sha256": record["html_sha256"],
        "tex_bytes": expanded["bytes"],
        "tex_sha256": expanded["sha256"],
    }
    require(actual == expected, f"{kind} /latex authority drift: {actual}")
    payload = json.loads((base.OUT / record["api_file"]).read_text(encoding="utf-8"))
    require(content_from_page(base.one_page(payload)).strip() == "{{latex}}", f"{kind} launcher")


def identity_rows_hash(closure: dict) -> str:
    rows = sorted(closure["pages"], key=lambda item: (item["title"], item["pageid"]))
    raw = json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(raw)


def closure_topology(
    parsed: dict,
    closure: dict,
    *,
    expected_raw: int,
    expected_exact: int,
    expected_casefold: int,
) -> dict:
    raw_titles = [item["title"] for item in parsed.get("templates", [])]
    exact_duplicates = sorted(title for title, count in Counter(raw_titles).items() if count > 1)
    comparison_groups: dict[str, list[str]] = {}
    for title in raw_titles:
        comparison_groups.setdefault(title.replace("_", " ").casefold(), []).append(title)
    casefold_collisions = sorted(
        sorted(group) for group in comparison_groups.values() if len(group) > 1
    )
    require(len(raw_titles) == expected_raw, f"raw transclusion count drift: {len(raw_titles)}")
    require(len(set(raw_titles)) == expected_exact, "exact-title transclusion count drift")
    require(len(comparison_groups) == expected_casefold, "casefold comparison topology drift")
    require(closure["captured_page_count"] == expected_exact, "captured closure count drift")
    require(closure["missing_page_count"] == 0, "missing recursive transclusion")
    require(not exact_duplicates, f"unexpected exact duplicate topology: {exact_duplicates}")
    require(len(casefold_collisions) == 1, f"unexpected casefold topology: {casefold_collisions}")
    return {
        "raw_parser_template_occurrences": len(raw_titles),
        "unique_exact_parser_template_titles": len(set(raw_titles)),
        "unique_casefold_comparison_keys": len(comparison_groups),
        "casefold_title_collision_groups": casefold_collisions,
        "note": (
            "MediaWiki titles remain case-sensitive after the first character. The two titles "
            "in the collision group resolve to distinct page identities and are both preserved; "
            "the lower comparison count is diagnostic only."
        ),
        "canonical_identity_rows_sha256": identity_rows_hash(closure),
    }


def course_license_surface() -> dict:
    entry, parsed = base.entry_surface(COURSE_LICENSE_TITLE, "course-license")
    require(
        (entry["pageid"], entry["revid"], entry["mediawiki_sha1"])
        == (
            EXPECTED_LICENSE["wrapper_pageid"],
            EXPECTED_LICENSE["wrapper_revid"],
            EXPECTED_LICENSE["wrapper_sha1"],
        ),
        "course license wrapper drift",
    )
    closure = base.transclusion_closure(parsed, "course-license")
    dependencies = {key(item["title"]): item for item in closure["pages"]}
    dependency = dependencies.get(key(COURSE_LICENSE_DEPENDENCY))
    require(dependency is not None, "course license dependency absent")
    require(
        (dependency["pageid"], dependency["revid"], dependency["mediawiki_sha1"])
        == (
            EXPECTED_LICENSE["dependency_pageid"],
            EXPECTED_LICENSE["dependency_revid"],
            EXPECTED_LICENSE["dependency_sha1"],
        ),
        "course license dependency drift",
    )
    declaration = ""
    for batch in closure["batches"]:
        payload = json.loads((base.OUT / batch["file"]).read_text(encoding="utf-8"))
        for page in payload.get("query", {}).get("pages", []):
            if key(page.get("title", "")) == key(COURSE_LICENSE_DEPENDENCY):
                declaration = content_from_page(page)
    require("CC-by-sa 4.0" in declaration, "course declaration no longer states CC BY-SA 4.0")
    return {
        "declared_license": CURRENT_LICENSE,
        "wrapper": entry,
        "recursive_transclusion_closure": closure,
        "validated_dependency_title": COURSE_LICENSE_DEPENDENCY,
        "validated_dependency": dependency,
    }


def enrich_exercise_map(solutions: dict, worksheet_parsed: dict) -> dict:
    entries = solutions["entries"]
    require(len(entries) == 12, "Unit 23 must retain exactly 12 ordered exercises")
    titles = [entry["exercise_title"] for entry in entries]
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
    source_path = base.OUT / "ordered-exercise-source-api.json"
    base.write_bytes(source_path, raw)
    query = payload.get("query", {})
    mapping = base.canonical_map(query)
    pages = {page["title"]: page for page in query.get("pages", [])}
    hidden_points = {3: 2, 4: 4, 5: 4, 6: 3, 7: 2}
    hidden_subpoints = {5: [2, 1, 1]}
    displayed_points = {8: 4, 9: 3, 10: 5, 11: 5, 12: 3}
    enriched: list[dict] = []
    for number, (entry, title) in enumerate(zip(entries, titles, strict=True), start=1):
        resolved = base.resolve_title(title, mapping)
        page = pages.get(resolved) or pages.get(title)
        require(page is not None and not page.get("missing"), f"exercise source missing: {title}")
        rev = base.revision(page)
        content = rev["slots"]["main"]["content"]
        point_match = re.search(r"(?m)^\|Punkte[ \t]*=[ \t]*([^\r\n}]*)", content)
        authored_points = int(point_match.group(1).strip()) if point_match and point_match.group(1).strip() else None
        subpoints = [
            int(value)
            for _, value in re.findall(r"(?m)^\|p(\d+)\s*=\s*(\d+)\s*$", content)
        ]
        expected_authored = hidden_points.get(number, displayed_points.get(number))
        if expected_authored is None:
            require(authored_points is None, f"unexpected authored points on exercise {number}")
        else:
            require(authored_points == expected_authored, f"authored points drift on exercise {number}")
        require(subpoints == hidden_subpoints.get(number, []), f"subpoint topology drift on exercise {number}")
        role = "practice" if number <= 7 else "submitted"
        entry.update(
            {
                "role": role,
                "authored_points": authored_points,
                "authored_subpoints": subpoints,
                "displayed_points": displayed_points.get(number),
                "points_displayed_in_worksheet": number >= 8,
                "exercise_pageid": int(page["pageid"]),
                "exercise_revid": int(rev["revid"]),
                "exercise_mediawiki_sha1": rev["sha1"],
                "exercise_wikitext_bytes": base.content_bytes(rev),
            }
        )
        enriched.append(entry)

    raw_template_titles = [item["title"] for item in worksheet_parsed.get("templates", [])]
    ordered_from_parse = [
        item["title"]
        for item in worksheet_parsed.get("templates", [])
        if int(item.get("ns", -1)) != 10 and item["title"].endswith("/Aufgabe")
    ]
    require(ordered_from_parse == titles, "ordered exercise parser extraction changed")
    require(sum(item["displayed_points"] or 0 for item in enriched) == 20, "displayed point total")
    solutions["ordered_role_and_point_topology"] = {
        "practice_numbers": list(range(1, 8)),
        "submitted_numbers": list(range(8, 13)),
        "practice_authored_hidden_points": hidden_points,
        "practice_authored_hidden_subpoints": hidden_subpoints,
        "submitted_displayed_points": displayed_points,
        "submitted_displayed_point_total": 20,
        "source_api_file": source_path.name,
        "source_api_bytes": source_path.stat().st_size,
        "source_api_sha256": base.digest(source_path),
    }
    map_path = base.OUT / "ORDERED_EXERCISE_MAP.json"
    for field in ("map_file", "map_bytes", "map_sha256"):
        solutions.pop(field, None)
    base.write_json(map_path, solutions)
    solutions["map_file"] = map_path.name
    solutions["map_bytes"] = map_path.stat().st_size
    solutions["map_sha256"] = base.digest(map_path)
    return solutions


def solution_transclusion_closures(solutions: dict) -> list[dict]:
    candidate_payload = json.loads(
        (base.OUT / solutions["candidate_api_file"]).read_text(encoding="utf-8")
    )
    pages = {
        key(page["title"]): page
        for page in candidate_payload.get("query", {}).get("pages", [])
        if not page.get("missing")
    }
    records: list[dict] = []
    for item in solutions["entries"]:
        if not item["has_public_solution"]:
            continue
        number = int(item["exercise_number"])
        expected = EXPECTED_SOLUTIONS.get(number)
        require(expected is not None, f"unexpected public solution {number}")
        page = pages.get(key(str(item["resolved_title"])))
        require(page is not None, f"solution content absent: {item['resolved_title']}")
        rev = base.revision(page)
        require(
            (int(page["pageid"]), int(rev["revid"]), rev["sha1"], base.content_bytes(rev))
            == (expected["pageid"], expected["revid"], expected["sha1"], expected["wikitext_bytes"]),
            f"solution {number} identity drift",
        )
        wikitext = rev["slots"]["main"]["content"]
        wrappers = [
            value.strip()
            for value in re.findall(r"\{\{\s*:\s*([^|}\n]+)", wikitext)
            if value.strip()
        ]
        require(not wrappers, f"solution {number} unexpectedly became a wrapper")
        parse_raw, parse_payload = base.api_raw(
            base.WIKI_API,
            {
                "action": "parse",
                "oldid": int(item["revid"]),
                "prop": "links|templates|images|externallinks|tocdata",
            },
        )
        parse_path = base.OUT / f"solution-ex{number:02d}-parse-api.json"
        base.write_bytes(parse_path, parse_raw)
        parsed = parse_payload["parse"]
        closure = base.transclusion_closure(parsed, f"solution-ex{number:02d}")
        require(closure["captured_page_count"] == expected["closure_pages"], f"solution {number} closure")
        require(closure["missing_page_count"] == 0, f"solution {number} missing dependency")
        records.append(
            {
                "exercise_number": number,
                "solution_title": item["resolved_title"],
                "solution_revid": int(item["revid"]),
                "parse_api_file": parse_path.name,
                "parse_api_bytes": parse_path.stat().st_size,
                "parse_api_sha256": base.digest(parse_path),
                "direct_wrapper_dependency_titles": wrappers,
                "recursive_transclusion_closure": closure,
                "canonical_identity_rows_sha256": identity_rows_hash(closure),
            }
        )
    require([item["exercise_number"] for item in records] == [4, 5], "public solution set")
    return records


def freeze_high_risk_bindings(
    lecture_closure: dict, worksheet_closure: dict, solutions: dict, solution_closures: list[dict]
) -> tuple[list[dict], list[dict]]:
    pageids = [str(pageid) for _, pageid, _ in HIGH_RISK_IDENTITIES]
    raw, payload = base.api_raw(
        base.WIKI_API,
        {
            "action": "query",
            "prop": "revisions",
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "main",
            "pageids": "|".join(pageids),
        },
    )
    path = base.OUT / "high-risk-source-api.json"
    base.write_bytes(path, raw)
    pages = {int(page["pageid"]): page for page in payload.get("query", {}).get("pages", [])}
    closure_ids = {
        int(page["pageid"])
        for closure in (lecture_closure, worksheet_closure, *[item["recursive_transclusion_closure"] for item in solution_closures])
        for page in closure["pages"]
    }
    closure_ids.update(int(entry["pageid"]) for entry in solutions["entries"] if entry["has_public_solution"])
    bindings: list[dict] = []
    content_by_id: dict[int, str] = {}
    for label, pageid, revid in HIGH_RISK_IDENTITIES:
        page = pages.get(pageid)
        require(page is not None and not page.get("missing"), f"high-risk page missing: {pageid}")
        rev = base.revision(page)
        require(int(rev["revid"]) == revid, f"high-risk revision drift: {label}")
        require(pageid in closure_ids, f"high-risk page is outside frozen semantic closure: {label}")
        content = rev["slots"]["main"]["content"]
        content_by_id[pageid] = content
        bindings.append(
            {
                "label": label,
                "title": page["title"],
                "pageid": pageid,
                "revid": revid,
                "parentid": int(rev.get("parentid", 0)),
                "timestamp": rev["timestamp"],
                "mediawiki_sha1": rev["sha1"],
                "wikitext_bytes": base.content_bytes(rev),
                "capture_file": path.name,
            }
        )

    defects = [
        {
            "id": "AGC-U23-SRC-001",
            "pageid": 20893,
            "kind": "false universal statement",
            "source_needle": "für jedes maximale Ideal",
            "required_reader_repair": (
                "Do not reproduce universal maximal-ideal nilpotence. State the valid localized "
                "form (mR_m)^n=0 with a uniform exponent, or a correct proper Jacobson-radical formulation."
            ),
            "counterexample": "K × K has dimension zero but neither maximal ideal is nilpotent.",
        },
        {
            "id": "AGC-U23-SRC-002",
            "pageid": 95515,
            "kind": "degree-bound typo and proof gap",
            "source_needle": "vom Grad {{mathl|term= < m",
            "required_reader_repair": (
                "Replace <m by <n and use the lowest nonzero homogeneous component of G, "
                "whose product with F_m cannot cancel."
            ),
        },
        {
            "id": "AGC-U23-SRC-003",
            "pageid": 95541,
            "kind": "index typo",
            "source_needle": "|n_j\n| \\geq | e",
            "required_reader_repair": "Replace n_j by m_j, matching the preceding summands m_1,...,m_n.",
        },
        {
            "id": "AGC-U23-SRC-004",
            "pageid": 20855,
            "kind": "quotient-class notation must remain explicit",
            "source_needle": "df {{defeq}}\\overline {f-f(P)}",
            "required_reader_repair": (
                "Render d(f) as the class [f-f(P)] in m/m^2; all Leibniz equalities in the proof "
                "are congruences/classes modulo m^2, not equalities in R."
            ),
        },
        {
            "id": "AGC-U23-SRC-005",
            "pageid": 20795,
            "kind": "monomial-ideal shorthand",
            "source_needle": "K[M]/(n M_+)",
            "required_reader_repair": (
                "Explain (nM_+) as the monomial ideal spanned/generated by T^m for m in nM_+, "
                "not scalar multiplication of a subset."
            ),
        },
        {
            "id": "AGC-U23-SRC-006",
            "pageid": 18360,
            "kind": "summand-membership omission",
            "source_needle": "Summanden aus {{math|term= M }}",
            "required_reader_repair": "The n summands must lie in M_+, not merely M.",
        },
    ]
    for defect in defects:
        require(defect["source_needle"] in content_by_id[defect["pageid"]], f"source defect evidence drift: {defect['id']}")
    return bindings, defects


def revision_slot_witnesses(page: dict) -> dict[str, dict]:
    revisions = page.get("revisions", [])
    require(len(revisions) == 1, f"non-unique Commons description revision: {page.get('title')}")
    slots = revisions[0].get("slots", {})
    result: dict[str, dict] = {}
    for name, slot in sorted(slots.items()):
        content = slot.get("content")
        require(isinstance(content, str), f"missing Commons slot content: {page.get('title')} {name}")
        raw = content.encode("utf-8")
        result[name] = {"bytes": len(raw), "sha256": sha256_bytes(raw)}
    return result


def official_pdfs_no_assets(
    lecture_parsed: dict,
    worksheet_parsed: dict,
    lecture: dict,
    worksheet: dict,
    lecture_closure: dict,
    worksheet_closure: dict,
) -> tuple[list[dict], list[dict]]:
    image_names = list(dict.fromkeys(lecture_parsed.get("images", []) + worksheet_parsed.get("images", [])))
    pdf_names = [name for name in image_names if name.casefold().endswith(".pdf")]
    substantive = [name for name in image_names if not name.casefold().endswith(".pdf")]
    require(not substantive, f"Unit 23 media topology changed: {substantive}")
    lecture_pdf = [name for name in pdf_names if "Vorlesung23.pdf" in name.replace("_", "")]
    worksheet_pdf = [name for name in pdf_names if "Arbeitsblatt23.pdf" in name.replace("_", "")]
    require(len(lecture_pdf) == len(worksheet_pdf) == 1 and len(pdf_names) == 2, f"PDF topology: {pdf_names}")

    ordered_names = [lecture_pdf[0], worksheet_pdf[0]]
    wiki_raw, wiki_payload = base.api_raw(
        base.WIKI_API,
        {
            "action": "query",
            "prop": "imageinfo",
            "iiprop": "timestamp|url|size|sha1|mime|mediatype",
            "titles": "|".join("File:" + name for name in ordered_names),
        },
    )
    official_path = base.OUT / "official-pdfs-api.json"
    base.write_bytes(official_path, wiki_raw)
    commons_raw, commons_payload = base.api_raw(
        base.COMMONS_API,
        {
            "action": "query",
            "prop": "imageinfo|revisions",
            "iiprop": "timestamp|user|url|size|sha1|mime|mediatype|extmetadata",
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "*",
            "titles": "|".join("File:" + name for name in ordered_names),
        },
    )
    base.write_bytes(base.COMMONS_META, commons_raw)
    wiki_pages = {base.file_key(page["title"]): page for page in wiki_payload.get("query", {}).get("pages", [])}
    commons_pages = {base.file_key(page["title"]): page for page in commons_payload.get("query", {}).get("pages", [])}

    records: list[dict] = []
    semantic_by_kind = {
        "lecture": [lecture, *lecture_closure["pages"]],
        "worksheet": [worksheet, *worksheet_closure["pages"]],
    }
    for kind, name in (("lecture", lecture_pdf[0]), ("worksheet", worksheet_pdf[0])):
        expected = EXPECTED_PDFS[kind]
        page = wiki_pages.get(base.file_key(name))
        commons_page = commons_pages.get(base.file_key(name))
        require(page is not None and page.get("imageinfo"), f"Wikiversity PDF missing: {name}")
        require(commons_page is not None and commons_page.get("imageinfo"), f"Commons PDF missing: {name}")
        info = page["imageinfo"][0]
        commons_info = commons_page["imageinfo"][0]
        data = base.fetch(info["url"])
        require(len(data) == int(info["size"]), f"PDF byte mismatch: {name}")
        require(base.digest_bytes(data, "sha1") == info["sha1"], f"PDF SHA-1 mismatch: {name}")
        local = base.ARTIFACTS / f"{kind}-{UNIT_LABEL}-official.pdf"
        base.write_bytes(local, data)
        require(base.digest(local) == expected["local_sha256"], f"PDF SHA-256 drift: {kind}")

        reader = base.PdfReader(str(local))
        require(not reader.is_encrypted, f"encrypted official PDF: {name}")
        page_text = [(pdf_page.extract_text() or "") for pdf_page in reader.pages]
        extracted = "\n".join(page_text)
        extracted_character_total = sum(len(text) for text in page_text)
        normalized_text = " ".join(extracted.split()).casefold()
        require(PDF_INTERNAL_LABEL.casefold() in normalized_text, f"legacy PDF license label absent: {name}")
        root = reader.trailer["/Root"]
        mark_info = root.get("/MarkInfo")
        if hasattr(mark_info, "get_object"):
            mark_info = mark_info.get_object()
        tagged = bool(mark_info and mark_info.get("/Marked", False))
        has_structure_tree = root.get("/StructTreeRoot") is not None
        blank_pages = [index for index, text in enumerate(page_text, start=1) if not text.strip()]
        if kind == "worksheet":
            require(blank_pages == [4], f"worksheet blank-page topology changed: {blank_pages}")
        else:
            require(not blank_pages, f"unexpected blank lecture page: {blank_pages}")

        metadata = commons_info.get("extmetadata", {})
        license_short = base.ext(metadata, "LicenseShortName") or base.ext(metadata, "UsageTerms")
        require(license_short == CURRENT_LICENSE, f"unexpected Commons PDF license: {license_short}")
        slots = revision_slot_witnesses(commons_page)
        expected_slots = {
            slot: {"bytes": values[0], "sha256": values[1]}
            for slot, values in expected["slots"].items()
        }
        require(slots == expected_slots, f"Commons slot drift: {kind} {slots}")
        media_content = commons_page["revisions"][0]["slots"]["mediainfo"]["content"]
        require("Q18199165" in media_content, f"CC BY-SA 4.0 P275 claim absent: {name}")
        description_rev = commons_page["revisions"][0]
        actual = {
            "commons_pageid": int(commons_page["pageid"]),
            "image_timestamp": info["timestamp"],
            "source_bytes": int(info["size"]),
            "source_sha1": info["sha1"],
            "local_sha256": base.digest(local),
            "page_count": len(reader.pages),
            "text_characters": extracted_character_total,
            "description_revid": int(description_rev["revid"]),
            "description_sha1": description_rev["sha1"],
            "slots": expected["slots"],
        }
        require(actual == expected, f"official PDF identity/accessibility drift: {kind} {actual}")
        later_semantic_pages = sorted(
            [
                {"title": item["title"], "pageid": item["pageid"], "revid": item["revid"], "timestamp": item["timestamp"]}
                for item in semantic_by_kind[kind]
                if item["timestamp"] > info["timestamp"]
            ],
            key=lambda item: (item["timestamp"], item["title"]),
        )
        if kind == "lecture":
            require(any(item["pageid"] == 165912 for item in later_semantic_pages), "lecture/PDF temporal discrepancy missing")
        else:
            require(any(item["pageid"] == 20797 for item in later_semantic_pages), "worksheet Ex6/PDF discrepancy missing")

        records.append(
            {
                "source_file_title": page["title"],
                "commons_pageid": int(commons_page["pageid"]),
                "image_timestamp": info["timestamp"],
                "mediawiki_sha1": info["sha1"],
                "source_bytes": int(info["size"]),
                "mime": info["mime"],
                "source_url": info["url"],
                "description_url": info["descriptionurl"],
                "local_path": local.relative_to(ROOT).as_posix(),
                "local_bytes": local.stat().st_size,
                "local_sha256": base.digest(local),
                "page_count": len(reader.pages),
                "page_text_characters": [len(text) for text in page_text],
                "extractable_text_characters_joined_with_page_separators": len(extracted),
                "blank_page_numbers": blank_pages,
                "license_short": license_short,
                "license_url": base.ext(metadata, "LicenseUrl"),
                "artist": base.ext(metadata, "Artist"),
                "credit": base.ext(metadata, "Credit"),
                "commons_description_revid": int(description_rev["revid"]),
                "commons_description_mediawiki_sha1": description_rev["sha1"],
                "commons_revision_slot_witnesses": slots,
                "structured_license_claim": {"property": "P275", "item": "Q18199165", "meaning": CURRENT_LICENSE},
                "accessibility": {
                    "encrypted": False,
                    "extractable_text_characters": extracted_character_total,
                    "tagged_pdf": tagged,
                    "structure_tree_present": has_structure_tree,
                    "blank_page_numbers": blank_pages,
                },
                "semantic_pages_newer_than_pdf": later_semantic_pages,
                "internal_pdf_boilerplate_label": PDF_INTERNAL_LABEL,
                "governing_current_course_and_commons_license": CURRENT_LICENSE,
                "license_discrepancy_note": (
                    "The generated PDF retains a CC-by-sa 3.0 boilerplate, while the frozen "
                    "course declaration and Commons description/structured data bind CC BY-SA 4.0."
                ),
                "temporal_discrepancy_note": (
                    "This official PDF is an authority witness, not a byte-equivalent rendering "
                    "of the current semantic entry/transclusion closure."
                ),
            }
        )
    return records, list(commons_pages.values())


def write_zero_media_rights(pdf_records: list[dict], commons_pages: list[dict]) -> dict:
    by_key = {title_key(page["title"]): page for page in commons_pages}
    rights_records: list[dict] = []
    for witness in pdf_records:
        title = commons_file_title(witness["source_file_title"])
        page = by_key.get(title_key(title))
        require(page is not None, f"Commons rights page missing: {title}")
        record = pdf_rights(page, ROOT / witness["local_path"])
        require(record["license_short"] == CURRENT_LICENSE, f"PDF component license drift: {title}")
        for field in (
            "accessibility",
            "commons_revision_slot_witnesses",
            "structured_license_claim",
            "semantic_pages_newer_than_pdf",
            "internal_pdf_boilerplate_label",
            "governing_current_course_and_commons_license",
            "license_discrepancy_note",
            "temporal_discrepancy_note",
        ):
            record[field] = witness[field]
        rights_records.append(record)

    base.RIGHTS.parent.mkdir(parents=True, exist_ok=True)
    with base.RIGHTS.open("w", encoding="utf-8", newline="") as stream:
        csv.DictWriter(stream, fieldnames=EMPTY_RIGHTS_FIELDS, lineterminator="\n").writeheader()

    closure = {
        "schema": "brenner-unit-media-closure-v2",
        "unit": UNIT,
        "authority_only_boundary": True,
        "reader_media_positions": 0,
        "animated_html_positions": 0,
        "unique_local_assets": 0,
        "metadata_file": base.COMMONS_META.relative_to(ROOT).as_posix(),
        "metadata_bytes": base.COMMONS_META.stat().st_size,
        "metadata_sha256": base.digest(base.COMMONS_META),
        "rights_file": base.RIGHTS.relative_to(ROOT).as_posix(),
        "rights_bytes": base.RIGHTS.stat().st_size,
        "rights_sha256": base.digest(base.RIGHTS),
        "reader_credits_file": None,
        "reader_credits_required": False,
        "accessibility": {
            "reader_media_alt_or_caption_required": False,
            "reason": "The parsed Unit 23 entry surfaces contain no substantive reader media.",
            "official_pdf_surfaces": [
                {"local_path": item["local_path"], **item["accessibility"]} for item in pdf_records
            ],
        },
        "official_pdf_witnesses_are_not_media_positions": True,
        "official_pdf_component_rights": sorted(rights_records, key=lambda item: item["local_path"]),
        "component_discrepancies": {
            "official_pdf_license_boilerplate": [
                {
                    "local_path": item["local_path"],
                    "embedded_label": item["internal_pdf_boilerplate_label"],
                    "current_commons_and_course_license": CURRENT_LICENSE,
                    "note": item["license_discrepancy_note"],
                }
                for item in pdf_records
            ],
            "temporal_scope": [
                {
                    "local_path": item["local_path"],
                    "pdf_timestamp": item["image_timestamp"],
                    "newer_semantic_pages": item["semantic_pages_newer_than_pdf"],
                    "note": item["temporal_discrepancy_note"],
                }
                for item in pdf_records
            ],
            "worksheet_blank_page": {
                "local_path": next(item["local_path"] for item in pdf_records if "worksheet-23" in item["local_path"]),
                "page_number": 4,
                "classification": "blank in the official five-page PDF; preserved as source evidence",
            },
        },
        "assets": [],
    }
    base.write_json(base.CLOSURE, closure)
    return closure


def add_expected(expected: dict[str, dict], record: dict) -> None:
    title = str(record["title"])
    candidate = {"title": title, "revid": int(record["revid"]), "sha1": record["mediawiki_sha1"]}
    previous = expected.get(key(title))
    require(previous is None or previous == candidate, f"inconsistent repeated identity: {title}")
    expected[key(title)] = candidate


def final_live_identity_replay(
    primary_records: list[dict],
    closures: list[dict],
    solutions: dict,
    pdf_records: list[dict],
    pdf_rights_records: list[dict],
) -> dict:
    expected: dict[str, dict] = {}
    for record in primary_records:
        add_expected(expected, record)
    for closure in closures:
        for page in closure["pages"]:
            add_expected(expected, page)
    for item in solutions["entries"]:
        if item["has_public_solution"]:
            add_expected(expected, {"title": item["resolved_title"], "revid": item["revid"], "mediawiki_sha1": item["mediawiki_sha1"]})

    requested = [item["title"] for item in sorted(expected.values(), key=lambda row: row["title"])]
    require(len(requested) == 208, f"final replay identity topology changed: {len(requested)}")
    batches: list[dict] = []
    for offset in range(0, len(requested), 25):
        titles = requested[offset : offset + 25]
        raw, payload = base.api_raw(
            base.WIKI_API,
            {"action": "query", "prop": "revisions", "rvprop": "ids|timestamp|sha1", "titles": "|".join(titles)},
        )
        path = base.OUT / f"final-identity-replay-{offset // 25 + 1:02d}.json"
        base.write_bytes(path, raw)
        pages = payload.get("query", {}).get("pages", [])
        require(len(pages) == len(titles) and not any(page.get("missing") for page in pages), f"final replay batch: {path.name}")
        for page in pages:
            rev = base.revision(page)
            frozen = expected.get(key(page["title"]))
            require(frozen is not None, f"unexpected final replay title: {page['title']}")
            require(int(rev["revid"]) == frozen["revid"] and rev["sha1"] == frozen["sha1"], f"live revision drift: {page['title']}")
        batches.append({"file": path.name, "bytes": path.stat().st_size, "sha256": base.digest(path), "title_count": len(titles)})

    commons_raw, commons_payload = base.api_raw(
        base.COMMONS_API,
        {
            "action": "query",
            "prop": "imageinfo|revisions",
            "iiprop": "timestamp|url|size|sha1|mime|mediatype",
            "rvprop": "ids|timestamp|sha1",
            "titles": "|".join(commons_file_title(item["source_file_title"]) for item in pdf_records),
        },
    )
    commons_path = base.OUT / "final-commons-pdf-identity-replay.json"
    base.write_bytes(commons_path, commons_raw)
    commons_pages = {title_key(page["title"]): page for page in commons_payload.get("query", {}).get("pages", [])}
    rights_by_title = {title_key(item["title"]): item for item in pdf_rights_records}
    for witness in pdf_records:
        title = commons_file_title(witness["source_file_title"])
        page = commons_pages.get(title_key(title))
        rights = rights_by_title.get(title_key(title))
        require(page is not None and rights is not None and not page.get("missing"), f"final Commons replay missing: {title}")
        info = page["imageinfo"][0]
        rev = base.revision(page)
        require(int(info["size"]) == witness["source_bytes"] and info["sha1"] == witness["mediawiki_sha1"], f"final PDF byte drift: {title}")
        require(int(rev["revid"]) == rights["revid"] and rev["sha1"] == rights["mediawiki_sha1"], f"final PDF description drift: {title}")
    return {
        "result": "PASS",
        "wikiversity_identity_count": len(expected),
        "wikiversity_batches": batches,
        "commons_pdf_identity_count": len(pdf_records),
        "commons_replay_file": commons_path.name,
        "commons_replay_bytes": commons_path.stat().st_size,
        "commons_replay_sha256": base.digest(commons_path),
    }


def write_freeze_note(manifest_path: Path, manifest: dict) -> None:
    lecture = manifest["lecture"]
    worksheet = manifest["worksheet"]
    pdfs = {"lecture" if "lecture-23" in item["local_path"] else "worksheet": item for item in manifest["official_pdf_witnesses"]}
    source_defects = manifest["source_defect_bindings"]
    lines = [
        "# Unit 23 authority freeze",
        "",
        f"Frozen at `{manifest['frozen_utc']}` from the official German Wikiversity course `{base.COURSE}`. This is an authority boundary, not an Indonesian translation checkpoint.",
        "",
        "## Exact primary entry and editable surfaces",
        "",
        f"- Lecture: pageid `{lecture['pageid']}`, revid `{lecture['revid']}`, MediaWiki SHA-1 `{lecture['mediawiki_sha1']}`, immutable oldid `{lecture['oldid_url']}`.",
        f"- Worksheet: pageid `{worksheet['pageid']}`, revid `{worksheet['revid']}`, MediaWiki SHA-1 `{worksheet['mediawiki_sha1']}`, immutable oldid `{worksheet['oldid_url']}`.",
        f"- `/latex` launchers: lecture revid `{manifest['lecture_latex_page']['revid']}` and worksheet revid `{manifest['worksheet_latex_page']['revid']}`; each launcher is exactly `{{{{latex}}}}`. Their expanded `.tex` files are captures of dynamic Parsoid output, not immutable source revisions.",
        f"- Recursive closure: lecture `{manifest['lecture_transclusion_closure']['captured_page_count']}` exact page identities from `{manifest['transclusion_topology']['lecture']['raw_parser_template_occurrences']}` parser occurrences (`{manifest['transclusion_topology']['lecture']['unique_casefold_comparison_keys']}` case-folded comparison keys); worksheet `{manifest['worksheet_transclusion_closure']['captured_page_count']}` exact page identities from `{manifest['transclusion_topology']['worksheet']['raw_parser_template_occurrences']}` occurrences (`{manifest['transclusion_topology']['worksheet']['unique_casefold_comparison_keys']}` case-folded keys); missing pages `0`. Each apparent case-only collision is retained because it resolves to two distinct MediaWiki pages.",
        "",
        "## Exercise and solution closure",
        "",
        "Exactly 12 exercises are ordered as practice 1-7 and submitted 8-12. Displayed submitted points are 4, 3, 5, 5, 3 (total 20). Practice source pages retain hidden authored points on exercises 3-7: 2, 4, 4 (subparts 2+1+1), 3, 2. Only exercises 4 and 5 have public solutions; both are complete content pages rather than transclusion wrappers, with recursive closures of 19 and 13 pages.",
        "",
        "## Rights, media, PDFs, and accessibility",
        "",
        f"The course-specific license wrapper and its `Holger Brenner/Lizenzerklärung` dependency bind the semantic closure under `{CURRENT_LICENSE}`. The reader-media closure is exactly zero positions, so `RIGHTS-unit-23.csv` is intentionally header-only.",
        f"- Official lecture PDF: `{pdfs['lecture']['local_bytes']}` bytes, SHA-256 `{pdfs['lecture']['local_sha256']}`, `{pdfs['lecture']['page_count']}` pages, unencrypted, extractable text, untagged, no structure tree.",
        f"- Official worksheet PDF: `{pdfs['worksheet']['local_bytes']}` bytes, SHA-256 `{pdfs['worksheet']['local_sha256']}`, `{pdfs['worksheet']['page_count']}` pages; page 4 is blank; unencrypted, extractable text, untagged, no structure tree.",
        "Both PDF binaries retain stale internal CC-by-sa 3.0 boilerplate while current Commons descriptions, structured P275 claims, and the course license state CC BY-SA 4.0. Both are preserved as official witnesses, not asserted as current semantic clones: the lecture entry is newer than its PDF, and worksheet exercise 6 is newer than the worksheet PDF.",
        "",
        "## Bound source defects and translation requirements",
        "",
    ]
    for defect in source_defects:
        lines.append(f"- `{defect['id']}` (pageid `{defect['pageid']}`): {defect['kind']}. Required reader handling: {defect['required_reader_repair']}")
    lines.extend(
        [
            "",
            "Upstream authority bytes remain unchanged. These defects must be corrected transparently in the Indonesian derivative and entered in its corrections ledger.",
            "",
            "## Replay boundary",
            "",
            f"Final live replay passed for `{manifest['final_live_identity_replay']['wikiversity_identity_count']}` unique Wikiversity revision identities and both Commons PDF components.",
            f"Manifest: `{manifest_path.relative_to(ROOT).as_posix()}`; `{manifest_path.stat().st_size}` bytes; SHA-256 `{base.digest(manifest_path)}`.",
            "",
        ]
    )
    FREEZE_NOTE.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    base.OUT.mkdir(parents=True, exist_ok=True)
    base.ARTIFACTS.mkdir(parents=True, exist_ok=True)

    lecture, lecture_parsed = base.entry_surface(base.LECTURE_TITLE, "lecture-23")
    worksheet, worksheet_parsed = base.entry_surface(base.WORKSHEET_TITLE, "worksheet-23")
    assert_primary_surface("lecture", lecture)
    assert_primary_surface("worksheet", worksheet)
    lecture_latex, lecture_tex = base.latex_surface(base.LECTURE_TITLE + "/latex", "lecture-23")
    worksheet_latex, worksheet_tex = base.latex_surface(base.WORKSHEET_TITLE + "/latex", "worksheet-23")
    assert_latex_surface("lecture", lecture_latex, lecture_tex)
    assert_latex_surface("worksheet", worksheet_latex, worksheet_tex)

    lecture_closure = base.transclusion_closure(lecture_parsed, "lecture-23")
    worksheet_closure = base.transclusion_closure(worksheet_parsed, "worksheet-23")
    transclusion_topology = {
        "lecture": closure_topology(
            lecture_parsed,
            lecture_closure,
            expected_raw=142,
            expected_exact=142,
            expected_casefold=141,
        ),
        "worksheet": closure_topology(
            worksheet_parsed,
            worksheet_closure,
            expected_raw=102,
            expected_exact=102,
            expected_casefold=101,
        ),
    }

    solutions = base.solution_map(worksheet, worksheet_parsed)
    require(solutions["exercise_count"] == 12 and solutions["solution_count"] == 2, "exercise/solution topology")
    solutions = enrich_exercise_map(solutions, worksheet_parsed)
    public_numbers = [entry["exercise_number"] for entry in solutions["entries"] if entry["has_public_solution"]]
    require(public_numbers == [4, 5], f"public solution set drift: {public_numbers}")
    solution_closures = solution_transclusion_closures(solutions)
    high_risk_bindings, source_defects = freeze_high_risk_bindings(
        lecture_closure, worksheet_closure, solutions, solution_closures
    )

    license_surface = course_license_surface()
    pdf_records, commons_pages = official_pdfs_no_assets(
        lecture_parsed, worksheet_parsed, lecture, worksheet, lecture_closure, worksheet_closure
    )
    media_closure = write_zero_media_rights(pdf_records, commons_pages)
    entry_recheck = base.final_identity_recheck(lecture["revid"], worksheet["revid"])

    all_closures = [
        lecture_closure,
        worksheet_closure,
        license_surface["recursive_transclusion_closure"],
        *[item["recursive_transclusion_closure"] for item in solution_closures],
    ]
    primary_records = [lecture, worksheet, lecture_latex, worksheet_latex, license_surface["wrapper"]]
    identity_replay = final_live_identity_replay(
        primary_records,
        all_closures,
        solutions,
        pdf_records,
        media_closure["official_pdf_component_rights"],
    )

    manifest = {
        "schema": "brenner-unit-authority-freeze-v2",
        "frozen_utc": datetime.now(timezone.utc).isoformat(),
        "unit_number": UNIT,
        "source_api": base.WIKI_API,
        "source_course_license": CURRENT_LICENSE,
        "source_course_license_authority": license_surface,
        "lecture": lecture,
        "worksheet": worksheet,
        "lecture_latex_page": lecture_latex,
        "worksheet_latex_page": worksheet_latex,
        "latex_capture_semantics": (
            "Each /latex page is a frozen launcher revision containing exactly {{latex}}; expanded "
            "TeX is a byte-bound capture of its dynamic Parsoid rendering at freeze time."
        ),
        "derived_expanded_tex": [lecture_tex, worksheet_tex],
        "lecture_transclusion_closure": lecture_closure,
        "worksheet_transclusion_closure": worksheet_closure,
        "transclusion_topology": transclusion_topology,
        "high_risk_semantic_identity_bindings": high_risk_bindings,
        "source_defect_bindings": source_defects,
        "solutions": solutions,
        "solution_transclusion_closures": solution_closures,
        "images": {
            "lecture": lecture_parsed.get("images", []),
            "worksheet": worksheet_parsed.get("images", []),
            "substantive_assets": [],
            "reader_media_positions": 0,
        },
        "official_pdf_witnesses": pdf_records,
        "media_rights_accessibility_and_discrepancies": {
            "closure_file": base.CLOSURE.relative_to(ROOT).as_posix(),
            "closure_bytes": base.CLOSURE.stat().st_size,
            "closure_sha256": base.digest(base.CLOSURE),
            "rights_file": base.RIGHTS.relative_to(ROOT).as_posix(),
            "rights_bytes": base.RIGHTS.stat().st_size,
            "rights_sha256": base.digest(base.RIGHTS),
        },
        "entry_revision_recheck": entry_recheck,
        "final_live_identity_replay": identity_replay,
    }
    manifest["files"] = [
        {"file": path.name, "bytes": path.stat().st_size, "sha256": base.digest(path)}
        for path in sorted(base.OUT.iterdir(), key=lambda item: item.name)
        if path.is_file() and path.name != "UNIT_AUTHORITY_MANIFEST.json"
    ]
    external_paths = [*(ROOT / item["local_path"] for item in pdf_records), base.RIGHTS, base.CLOSURE]
    manifest["bounded_external_files"] = [
        {"file": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": base.digest(path)}
        for path in sorted(external_paths, key=lambda item: item.as_posix())
    ]
    manifest_path = base.OUT / "UNIT_AUTHORITY_MANIFEST.json"
    base.write_json(manifest_path, manifest)

    replay = json.loads(manifest_path.read_text(encoding="utf-8"))
    actual_names = {path.name for path in base.OUT.iterdir() if path.is_file() and path.name != manifest_path.name}
    bound_names = {item["file"] for item in replay["files"]}
    require(actual_names == bound_names, "manifest-local inventory replay")
    for record in replay["files"]:
        path = base.OUT / record["file"]
        require(path.stat().st_size == record["bytes"] and base.digest(path) == record["sha256"], f"manifest replay: {path}")
    for record in replay["bounded_external_files"]:
        path = ROOT / record["file"]
        require(path.stat().st_size == record["bytes"] and base.digest(path) == record["sha256"], f"external replay: {path}")
    require(media_closure["reader_media_positions"] == 0 and not media_closure["assets"], "zero-media replay")
    require(identity_replay["result"] == "PASS" and identity_replay["wikiversity_identity_count"] == 208, "live replay")

    write_freeze_note(manifest_path, manifest)
    result = {
        "result": "PASS",
        "unit": UNIT,
        "lecture_pageid": lecture["pageid"],
        "lecture_revid": lecture["revid"],
        "worksheet_pageid": worksheet["pageid"],
        "worksheet_revid": worksheet["revid"],
        "lecture_transclusions": lecture_closure["captured_page_count"],
        "worksheet_transclusions": worksheet_closure["captured_page_count"],
        "solution_transclusions": [item["recursive_transclusion_closure"]["captured_page_count"] for item in solution_closures],
        "exercises": solutions["exercise_count"],
        "public_solutions": solutions["solution_count"],
        "media_positions": 0,
        "official_pdf_pages": [item["page_count"] for item in pdf_records],
        "live_replay_identities": identity_replay["wikiversity_identity_count"],
        "manifest_bytes": manifest_path.stat().st_size,
        "manifest_sha256": base.digest(manifest_path),
        "freeze_note_bytes": FREEZE_NOTE.stat().st_size,
        "freeze_note_sha256": base.digest(FREEZE_NOTE),
        "rights_bytes": base.RIGHTS.stat().st_size,
        "rights_sha256": base.digest(base.RIGHTS),
        "closure_bytes": base.CLOSURE.stat().st_size,
        "closure_sha256": base.digest(base.CLOSURE),
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
