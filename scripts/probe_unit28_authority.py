#!/usr/bin/env python3
"""Bounded primary-source probe for the official 2012 Unit 28 authority.

This is a discovery pass, not the final freeze. It uses the established
MediaWiki witness primitives to capture the exact entry, editable/HTML/TeX,
recursive-transclusion, exercise/solution-candidate, and image-list surfaces
needed to specialize the fail-closed Unit 28 freeze.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import freeze_unit12_authority as base


ROOT = Path(__file__).resolve().parents[1]
UNIT = 28
COURSE = "Kurs:Algebraische Kurven (Osnabrück 2012)"
LECTURE_TITLE = f"{COURSE}/Vorlesung {UNIT}"
WORKSHEET_TITLE = f"{COURSE}/Arbeitsblatt {UNIT}"
OUT = ROOT / "authority" / "wikiversity" / "unit-28"

base.UNIT = UNIT
base.COURSE = COURSE
base.LECTURE_TITLE = LECTURE_TITLE
base.WORKSHEET_TITLE = WORKSHEET_TITLE
base.OUT = OUT
base.ARTIFACTS = ROOT / "authority" / "artifacts"
base.ASSETS = ROOT / "authority" / "assets"
base.RIGHTS = ROOT / "authority" / "RIGHTS-unit-28.csv"
base.CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-28.json"
base.COMMONS_META = OUT / "local-pdf-file-metadata-api.json"
base.USER_AGENT = "O016-unit28-authority-probe/1.0 (bounded educational preservation)"


def normalized(record: dict) -> dict:
    return {
        key: record[key]
        for key in (
            "title",
            "pageid",
            "revid",
            "parentid",
            "timestamp",
            "mediawiki_sha1",
            "wikitext_bytes",
        )
    }


def closure_summary(root: dict, parsed: dict, closure: dict) -> dict:
    records = [normalized(root), *(normalized(item) for item in closure["pages"])]
    records.sort(key=lambda item: item["title"].casefold())
    payload = json.dumps(
        records,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return {
        "parser_occurrences": len(parsed.get("templates", [])),
        "unique_exact_titles": len({item["title"] for item in parsed.get("templates", [])}),
        "dependencies": len(closure["pages"]),
        "with_root": len(records),
        "canonical_identity_rows_sha256": hashlib.sha256(payload).hexdigest(),
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    if sys.argv[1:] == ["--media-only"]:
        lecture_parsed = json.loads(
            (OUT / "lecture-28-parse-api.json").read_text(encoding="utf-8")
        )["parse"]
        worksheet_parsed = json.loads(
            (OUT / "worksheet-28-parse-api.json").read_text(encoding="utf-8")
        )["parse"]
        pdfs, assets = base.shared_media(lecture_parsed, worksheet_parsed)
        result = {"unit": UNIT, "official_pdfs": pdfs, "media_assets": assets}
        base.write_json(OUT / "PROBE_MEDIA_SUMMARY.json", result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    if sys.argv[1:] == ["--solution-only"]:
        title = (
            "Ebene Kurve/y-x^3+x+2/Rationale Parametrisierung/"
            "Fortsetzung auf P^1/Aufgabe/Lösung"
        )
        solution, parsed = base.entry_surface(title, "solution-ex10")
        closure = base.transclusion_closure(parsed, "solution-ex10")
        result = {
            "unit": UNIT,
            "exercise_number": 10,
            "solution": solution,
            "transclusion_topology": closure_summary(solution, parsed, closure),
        }
        base.write_json(OUT / "PROBE_SOLUTION_SUMMARY.json", result)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    if sys.argv[1:]:
        raise SystemExit(
            "Usage: probe_unit28_authority.py [--media-only|--solution-only]"
        )
    course, course_parsed = base.entry_surface(COURSE, "course-2012")
    lecture, lecture_parsed = base.entry_surface(LECTURE_TITLE, "lecture-28")
    worksheet, worksheet_parsed = base.entry_surface(WORKSHEET_TITLE, "worksheet-28")
    lecture_latex, lecture_tex = base.latex_surface(LECTURE_TITLE + "/latex", "lecture-28")
    worksheet_latex, worksheet_tex = base.latex_surface(WORKSHEET_TITLE + "/latex", "worksheet-28")
    lecture_closure = base.transclusion_closure(lecture_parsed, "lecture-28")
    worksheet_closure = base.transclusion_closure(worksheet_parsed, "worksheet-28")
    solutions = base.solution_map(worksheet, worksheet_parsed)

    summary = {
        "schema": "ag-bridge-unit-authority-probe-v1",
        "unit": UNIT,
        "source_api": base.WIKI_API,
        "course": course,
        "lecture": lecture,
        "worksheet": worksheet,
        "latex": {
            "lecture_page": lecture_latex,
            "lecture_expanded": lecture_tex,
            "worksheet_page": worksheet_latex,
            "worksheet_expanded": worksheet_tex,
        },
        "parse": {
            "course_templates": len(course_parsed.get("templates", [])),
            "lecture_templates": len(lecture_parsed.get("templates", [])),
            "worksheet_templates": len(worksheet_parsed.get("templates", [])),
            "lecture_images": lecture_parsed.get("images", []),
            "worksheet_images": worksheet_parsed.get("images", []),
        },
        "transclusion_topology": {
            "lecture": closure_summary(lecture, lecture_parsed, lecture_closure),
            "worksheet": closure_summary(worksheet, worksheet_parsed, worksheet_closure),
        },
        "solutions": solutions,
    }
    base.write_json(OUT / "PROBE_SUMMARY.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
