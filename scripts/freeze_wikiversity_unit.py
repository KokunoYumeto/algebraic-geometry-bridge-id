#!/usr/bin/env python3
"""Freeze one Brenner lecture/worksheet pair and its rendered source closure."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
API = "https://de.wikiversity.org/w/api.php"
REST_HTML = "https://de.wikiversity.org/api/rest_v1/page/html"
EXPORT = "https://de.wikiversity.org/wiki/Spezial:Exportieren"
USER_AGENT = "Codex algebraic-geometry-bridge-id source freeze (at user's direction)"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def fetch(url: str, data: bytes | None = None) -> bytes:
    for attempt in range(1, 7):
        request = Request(url, data=data, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(request, timeout=90) as response:
                result = response.read()
            time.sleep(0.5)
            return result
        except HTTPError as exc:
            if exc.code != 429 or attempt == 6:
                raise
            retry_after = exc.headers.get("Retry-After")
            delay = min(20, int(retry_after) if retry_after and retry_after.isdigit() else 4 * attempt)
            time.sleep(delay)
    raise RuntimeError("unreachable retry state")


def api(params: dict[str, str]) -> bytes:
    complete = {"format": "json", "formatversion": "2", **params}
    return fetch(API, urlencode(complete).encode("utf-8"))


def write_raw(path: Path, data: bytes) -> None:
    path.write_bytes(data)


def revision_payload(title: str, path: Path) -> tuple[dict, str]:
    raw = api(
        {
            "action": "query",
            "prop": "revisions",
            "titles": title,
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "main",
        }
    )
    write_raw(path, raw)
    data = json.loads(raw)
    page = data["query"]["pages"][0]
    if page.get("missing"):
        raise RuntimeError(f"Missing page: {title}")
    revision = page["revisions"][0]
    content = revision["slots"]["main"]["content"]
    return {
        "title": page["title"],
        "pageid": page["pageid"],
        "revid": revision["revid"],
        "parentid": revision.get("parentid", 0),
        "timestamp": revision["timestamp"],
        "mediawiki_sha1": revision["sha1"],
        "wikitext_bytes": len(content.encode("utf-8")),
        "api_file": path.name,
        "api_bytes": path.stat().st_size,
        "api_sha256": digest(path),
    }, content


def freeze_page(title: str, stem: str, out: Path, include_parse: bool = True) -> tuple[dict, str, dict | None]:
    metadata, content = revision_payload(title, out / f"{stem}-api.json")
    encoded = quote(title, safe="")
    xml_path = out / f"{stem}.xml"
    html_path = out / f"{stem}.html"
    write_raw(xml_path, fetch(f"{EXPORT}/{encoded}"))
    write_raw(html_path, fetch(f"{REST_HTML}/{encoded}/{metadata['revid']}"))
    metadata.update(
        {
            "oldid_url": f"https://de.wikiversity.org/w/index.php?oldid={metadata['revid']}",
            "xml_file": xml_path.name,
            "xml_bytes": xml_path.stat().st_size,
            "xml_sha256": digest(xml_path),
            "html_file": html_path.name,
            "html_bytes": html_path.stat().st_size,
            "html_sha256": digest(html_path),
        }
    )
    parse_data = None
    if include_parse:
        raw_parse = api(
            {
                "action": "parse",
                "oldid": str(metadata["revid"]),
                "prop": "templates|images|links|externallinks|sections|displaytitle",
            }
        )
        parse_path = out / f"{stem}-parse-api.json"
        write_raw(parse_path, raw_parse)
        parse_data = json.loads(raw_parse)["parse"]
        metadata.update(
            {
                "parse_api_file": parse_path.name,
                "parse_api_bytes": parse_path.stat().st_size,
                "parse_api_sha256": digest(parse_path),
                "template_count": len(parse_data.get("templates", [])),
                "image_count": len(parse_data.get("images", [])),
                "link_count": len(parse_data.get("links", [])),
                "external_link_count": len(parse_data.get("externallinks", [])),
            }
        )
    return metadata, content, parse_data


def freeze_template_closure(parse_data: dict, stem: str, out: Path) -> dict:
    titles = sorted({row["title"] for row in parse_data.get("templates", [])})
    batch_rows = []
    closure_pages = []
    for batch_number, start in enumerate(range(0, len(titles), 25), start=1):
        batch_titles = titles[start : start + 25]
        raw = api(
            {
                "action": "query",
                "prop": "revisions",
                "titles": "|".join(batch_titles),
                "rvprop": "ids|timestamp|sha1|content",
                "rvslots": "main",
            }
        )
        path = out / f"{stem}-transclusions-{batch_number:02d}.json"
        write_raw(path, raw)
        data = json.loads(raw)
        for page in data["query"]["pages"]:
            if page.get("missing"):
                closure_pages.append({"title": page["title"], "missing": True})
                continue
            revision = page["revisions"][0]
            content = revision["slots"]["main"]["content"]
            closure_pages.append(
                {
                    "title": page["title"],
                    "pageid": page["pageid"],
                    "revid": revision["revid"],
                    "parentid": revision.get("parentid", 0),
                    "timestamp": revision["timestamp"],
                    "mediawiki_sha1": revision["sha1"],
                    "wikitext_bytes": len(content.encode("utf-8")),
                }
            )
        batch_rows.append(
            {
                "file": path.name,
                "bytes": path.stat().st_size,
                "sha256": digest(path),
                "requested_titles": batch_titles,
            }
        )
    closure_pages.sort(key=lambda row: row["title"])
    return {
        "requested_template_count": len(titles),
        "captured_page_count": len(closure_pages),
        "missing_page_count": sum(1 for row in closure_pages if row.get("missing")),
        "batches": batch_rows,
        "pages": closure_pages,
    }


def expanded_tex(html_path: Path, output_path: Path) -> None:
    soup = BeautifulSoup(html_path.read_bytes(), "html.parser")
    body = soup.body
    if body is None:
        raise RuntimeError(f"No body in {html_path}")
    for br in body.find_all("br"):
        br.replace_with("\n")
    value = html.unescape(body.get_text("\n"))
    value = value.replace("\u00a0", " ")
    value = re.sub(r"[ \t]+\n", "\n", value)
    value = re.sub(r"\n{4,}", "\n\n\n", value).strip() + "\n"
    output_path.write_text(value, encoding="utf-8")


def exercise_titles(wikitext: str) -> list[str]:
    found = re.findall(r"\{\{\s*inputaufgabe\s*\|\s*([^|\n}]+)", wikitext, flags=re.IGNORECASE)
    return [html.unescape(title.strip()) for title in found]


def freeze_solutions(exercises: list[str], out: Path, worksheet_metadata: dict) -> dict:
    candidate_titles = [f"{title}/Lösung" for title in exercises]
    raw = api(
        {
            "action": "query",
            "prop": "revisions",
            "titles": "|".join(candidate_titles),
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "main",
        }
    )
    candidates_path = out / "worksheet-solution-candidates-api.json"
    write_raw(candidates_path, raw)
    data = json.loads(raw)
    by_title = {page["title"]: page for page in data["query"]["pages"]}
    entries = []
    solution_number = 0
    for exercise_number, (exercise_title, candidate_title) in enumerate(zip(exercises, candidate_titles), start=1):
        page = by_title.get(candidate_title)
        if not page or page.get("missing"):
            entries.append(
                {
                    "exercise_number": exercise_number,
                    "exercise_title": exercise_title,
                    "solution_title": candidate_title,
                    "has_public_solution": False,
                }
            )
            continue
        solution_number += 1
        revision = page["revisions"][0]
        stem = f"solution-ex{exercise_number:02d}"
        encoded = quote(page["title"], safe="")
        xml_path = out / f"{stem}.xml"
        html_path = out / f"{stem}.html"
        write_raw(xml_path, fetch(f"{EXPORT}/{encoded}"))
        write_raw(html_path, fetch(f"{REST_HTML}/{encoded}/{revision['revid']}"))
        entries.append(
            {
                "exercise_number": exercise_number,
                "exercise_title": exercise_title,
                "solution_title": page["title"],
                "has_public_solution": True,
                "pageid": page["pageid"],
                "revid": revision["revid"],
                "parentid": revision.get("parentid", 0),
                "timestamp": revision["timestamp"],
                "mediawiki_sha1": revision["sha1"],
                "oldid_url": f"https://de.wikiversity.org/w/index.php?oldid={revision['revid']}",
                "xml_file": xml_path.name,
                "xml_bytes": xml_path.stat().st_size,
                "xml_sha256": digest(xml_path),
                "html_file": html_path.name,
                "html_bytes": html_path.stat().st_size,
                "html_sha256": digest(html_path),
            }
        )
    result = {
        "schema": "brenner-worksheet-solution-map-v2",
        "worksheet": worksheet_metadata,
        "exercise_count": len(exercises),
        "solution_count": solution_number,
        "candidate_api_file": candidates_path.name,
        "candidate_api_bytes": candidates_path.stat().st_size,
        "candidate_api_sha256": digest(candidates_path),
        "entries": entries,
    }
    map_path = out / "ORDERED_EXERCISE_MAP.json"
    map_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result["map_file"] = map_path.name
    result["map_bytes"] = map_path.stat().st_size
    result["map_sha256"] = digest(map_path)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--number", type=int, required=True)
    args = parser.parse_args()
    number = args.number
    out = ROOT / "authority" / "wikiversity" / f"unit-{number:02d}"
    out.mkdir(parents=True, exist_ok=True)

    prefix = "Kurs:Algebraische Kurven (Osnabrück 2025-2026)"
    lecture_title = f"{prefix}/Vorlesung {number}"
    worksheet_title = f"{prefix}/Arbeitsblatt {number}"
    lecture, lecture_wikitext, lecture_parse = freeze_page(lecture_title, f"lecture-{number:02d}", out)
    worksheet, worksheet_wikitext, worksheet_parse = freeze_page(worksheet_title, f"worksheet-{number:02d}", out)
    lecture_latex, _, _ = freeze_page(f"{lecture_title}/latex", f"lecture-{number:02d}-latex-page", out, False)
    worksheet_latex, _, _ = freeze_page(f"{worksheet_title}/latex", f"worksheet-{number:02d}-latex-page", out, False)

    lecture_tex_path = out / f"lecture-{number:02d}-expanded.tex"
    worksheet_tex_path = out / f"worksheet-{number:02d}-expanded.tex"
    expanded_tex(out / lecture_latex["html_file"], lecture_tex_path)
    expanded_tex(out / worksheet_latex["html_file"], worksheet_tex_path)

    lecture_closure = freeze_template_closure(lecture_parse or {}, f"lecture-{number:02d}", out)
    worksheet_closure = freeze_template_closure(worksheet_parse or {}, f"worksheet-{number:02d}", out)
    exercises = exercise_titles(worksheet_wikitext)
    solutions = freeze_solutions(exercises, out, worksheet)

    manifest = {
        "schema": "brenner-unit-authority-freeze-v1",
        "unit_number": number,
        "source_api": API,
        "lecture": lecture,
        "worksheet": worksheet,
        "lecture_latex_page": lecture_latex,
        "worksheet_latex_page": worksheet_latex,
        "derived_expanded_tex": [
            {"file": lecture_tex_path.name, "bytes": lecture_tex_path.stat().st_size, "sha256": digest(lecture_tex_path)},
            {"file": worksheet_tex_path.name, "bytes": worksheet_tex_path.stat().st_size, "sha256": digest(worksheet_tex_path)},
        ],
        "lecture_transclusion_closure": lecture_closure,
        "worksheet_transclusion_closure": worksheet_closure,
        "solutions": solutions,
        "images": {
            "lecture": lecture_parse.get("images", []) if lecture_parse else [],
            "worksheet": worksheet_parse.get("images", []) if worksheet_parse else [],
        },
        "files": [],
    }
    manifest_path = out / "UNIT_AUTHORITY_MANIFEST.json"
    for path in sorted(out.iterdir(), key=lambda item: item.name):
        if path.is_file() and path != manifest_path:
            manifest["files"].append({"file": path.name, "bytes": path.stat().st_size, "sha256": digest(path)})
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "result": "PASS",
                "unit": number,
                "lecture_revid": lecture["revid"],
                "worksheet_revid": worksheet["revid"],
                "exercises": len(exercises),
                "solutions": solutions["solution_count"],
                "lecture_templates": lecture_closure["requested_template_count"],
                "worksheet_templates": worksheet_closure["requested_template_count"],
                "manifest": manifest_path.relative_to(ROOT).as_posix(),
                "manifest_sha256": digest(manifest_path),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
