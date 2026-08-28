#!/usr/bin/env python3
"""Bounded primary-source discovery for official 2012 Unit 29 authority."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import freeze_unit12_authority as base


ROOT = Path(__file__).resolve().parents[1]
UNIT = 29
COURSE = "Kurs:Algebraische Kurven (Osnabrück 2012)"
LECTURE_TITLE = f"{COURSE}/Vorlesung {UNIT}"
WORKSHEET_TITLE = f"{COURSE}/Arbeitsblatt {UNIT}"
OUT = ROOT / "authority" / "wikiversity" / "unit-29"

base.UNIT = UNIT
base.COURSE = COURSE
base.LECTURE_TITLE = LECTURE_TITLE
base.WORKSHEET_TITLE = WORKSHEET_TITLE
base.OUT = OUT
base.ARTIFACTS = ROOT / "authority" / "artifacts"
base.ASSETS = ROOT / "authority" / "assets"
base.RIGHTS = ROOT / "authority" / "RIGHTS-unit-29.csv"
base.CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-29.json"
base.COMMONS_META = OUT / "local-pdf-file-metadata-api.json"
base.USER_AGENT = "O016-unit29-authority-probe/1.0 (bounded educational preservation)"


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


def probe_main() -> dict:
    course, course_parsed = base.entry_surface(COURSE, "course-2012")
    lecture, lecture_parsed = base.entry_surface(LECTURE_TITLE, "lecture-29")
    worksheet, worksheet_parsed = base.entry_surface(WORKSHEET_TITLE, "worksheet-29")
    lecture_latex, lecture_tex = base.latex_surface(
        LECTURE_TITLE + "/latex", "lecture-29"
    )
    worksheet_latex, worksheet_tex = base.latex_surface(
        WORKSHEET_TITLE + "/latex", "worksheet-29"
    )
    lecture_closure = base.transclusion_closure(lecture_parsed, "lecture-29")
    worksheet_closure = base.transclusion_closure(worksheet_parsed, "worksheet-29")
    solutions = base.solution_map(worksheet, worksheet_parsed)
    return {
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


def probe_media() -> dict:
    lecture_parsed = json.loads(
        (OUT / "lecture-29-parse-api.json").read_text(encoding="utf-8")
    )["parse"]
    worksheet_parsed = json.loads(
        (OUT / "worksheet-29-parse-api.json").read_text(encoding="utf-8")
    )["parse"]
    pdfs, assets = base.shared_media(lecture_parsed, worksheet_parsed)
    return {"unit": UNIT, "official_pdfs": pdfs, "media_assets": assets}


def probe_solution(number: int, title: str) -> dict:
    solution, parsed = base.entry_surface(title, f"solution-ex{number}")
    closure = base.transclusion_closure(parsed, f"solution-ex{number}")
    return {
        "unit": UNIT,
        "exercise_number": number,
        "solution": solution,
        "transclusion_topology": closure_summary(solution, parsed, closure),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--media-only", action="store_true")
    parser.add_argument("--all-positive-solutions", action="store_true")
    parser.add_argument("--solution-number", type=int)
    parser.add_argument("--solution-title")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.media_only:
        if args.solution_number is not None or args.solution_title is not None:
            raise SystemExit("--media-only cannot be combined with solution arguments")
        result = probe_media()
        output = OUT / "PROBE_MEDIA_SUMMARY.json"
    elif args.all_positive_solutions:
        if args.solution_number is not None or args.solution_title is not None:
            raise SystemExit(
                "--all-positive-solutions cannot be combined with solution arguments"
            )
        summary = json.loads((OUT / "PROBE_SUMMARY.json").read_text(encoding="utf-8"))
        result = {"unit": UNIT, "solutions": []}
        for entry in summary["solutions"]["entries"]:
            if not entry["has_public_solution"]:
                continue
            item = probe_solution(entry["exercise_number"], entry["resolved_title"])
            result["solutions"].append(item)
            base.write_json(
                OUT / f"PROBE_SOLUTION_EX{entry['exercise_number']}_SUMMARY.json",
                item,
            )
        output = OUT / "PROBE_POSITIVE_SOLUTIONS_SUMMARY.json"
    elif args.solution_number is not None or args.solution_title is not None:
        if args.solution_number is None or not args.solution_title:
            raise SystemExit("both --solution-number and --solution-title are required")
        result = probe_solution(args.solution_number, args.solution_title)
        output = OUT / f"PROBE_SOLUTION_EX{args.solution_number}_SUMMARY.json"
    else:
        result = probe_main()
        output = OUT / "PROBE_SUMMARY.json"
    base.write_json(output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
