#!/usr/bin/env python3
"""Freeze one Brenner lecture/worksheet unit from official Wikiversity APIs.

The output is immutable authority evidence, not reader prose.  The script
captures entry revisions, XML, rendered HTML, semantic parse surfaces,
transclusion revisions, ordered exercises, every public solution, the /latex
surfaces, derived LaTeX witnesses, and the official lecture/worksheet PDFs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
API = "https://de.wikiversity.org/w/api.php"
REST_HTML = "https://de.wikiversity.org/api/rest_v1/page/html"
COURSE = "Kurs:Algebraische Kurven (Osnabrück 2025-2026)"
USER_AGENT = "Codex-authority-freezer/1.0 (independent edition preservation)"
REVISION_PROPS = "ids|timestamp|sha1|content"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_fact(path: Path, base: Path) -> dict[str, Any]:
    return {
        "file": path.relative_to(base).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def write_json(path: Path, value: Any) -> None:
    payload = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    path.write_bytes(payload.encode("utf-8"))


def fetch(url: str, *, accept: str = "*/*", attempts: int = 6) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": accept},
    )
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            if error.code not in {429, 500, 502, 503, 504} or attempt + 1 == attempts:
                raise
            retry_after = error.headers.get("Retry-After", "")
            delay = int(retry_after) if retry_after.isdigit() else min(2 ** attempt, 30)
            time.sleep(max(delay, 1))
        except (TimeoutError, urllib.error.URLError):
            if attempt + 1 == attempts:
                raise
            time.sleep(min(2 ** attempt, 30))
    raise RuntimeError(f"unreachable fetch failure: {url}")


def api_url(params: dict[str, Any]) -> str:
    enriched = {"format": "json", "formatversion": 2, "maxlag": 5, **params}
    return API + "?" + urllib.parse.urlencode(enriched)


def fetch_api(params: dict[str, Any]) -> tuple[bytes, dict[str, Any]]:
    raw = fetch(api_url(params), accept="application/json")
    parsed = json.loads(raw.decode("utf-8"))
    if "error" in parsed:
        raise RuntimeError(f"MediaWiki API error: {parsed['error']}")
    return raw, parsed


def fetch_or_reuse(path: Path, url: str, *, resume: bool, accept: str = "*/*") -> bytes:
    if resume and path.is_file():
        return path.read_bytes()
    raw = fetch(url, accept=accept)
    path.write_bytes(raw)
    return raw


def api_or_reuse(
    path: Path,
    params: dict[str, Any],
    *,
    resume: bool,
) -> tuple[bytes, dict[str, Any]]:
    if resume and path.is_file():
        raw = path.read_bytes()
        return raw, json.loads(raw.decode("utf-8"))
    raw, parsed = fetch_api(params)
    path.write_bytes(raw)
    return raw, parsed


def revision_page(parsed: dict[str, Any], expected_title: str) -> tuple[dict[str, Any], dict[str, Any], str]:
    pages = parsed.get("query", {}).get("pages", [])
    if len(pages) != 1 or pages[0].get("missing"):
        raise RuntimeError(f"Page is missing or ambiguous: {expected_title!r}")
    page = pages[0]
    revisions = page.get("revisions", [])
    if len(revisions) != 1:
        raise RuntimeError(f"Expected exactly one current revision: {expected_title!r}")
    revision = revisions[0]
    content = revision.get("slots", {}).get("main", {}).get("content")
    if not isinstance(content, str):
        raise RuntimeError(f"Missing main-slot wikitext: {expected_title!r}")
    return page, revision, content


def page_metadata(page: dict[str, Any], revision: dict[str, Any], content: str) -> dict[str, Any]:
    return {
        "title": page["title"],
        "pageid": page["pageid"],
        "revid": revision["revid"],
        "parentid": revision.get("parentid", 0),
        "timestamp": revision["timestamp"],
        "mediawiki_sha1": revision["sha1"],
        "wikitext_bytes": len(content.encode("utf-8")),
    }


def rest_title(title: str) -> str:
    return urllib.parse.quote(title.replace(" ", "_"), safe="/:()_-")


def exact_html(
    title: str,
    revid: int,
    *,
    html_path: Path,
    resume: bool,
) -> tuple[bytes, str]:
    if resume and html_path.is_file():
        return html_path.read_bytes(), "reused_frozen_file"
    url = f"{REST_HTML}/{rest_title(title)}/{revid}"
    try:
        raw = fetch(url, accept="text/html", attempts=4)
        source = "rest_revision_html"
    except urllib.error.HTTPError as error:
        if error.code not in {404, 429}:
            raise
        raw_api, parsed = fetch_api(
            {"action": "parse", "oldid": revid, "prop": "text"}
        )
        del raw_api
        text = parsed.get("parse", {}).get("text")
        if not isinstance(text, str):
            raise RuntimeError(f"No rendered HTML fallback for revision {revid}")
        raw = text.encode("utf-8")
        source = "action_parse_text_fallback"
    html_path.write_bytes(raw)
    return raw, source


def exact_xml(revid: int, *, xml_path: Path, resume: bool) -> bytes:
    params = {
        "action": "query",
        "format": "xml",
        "export": 1,
        "exportnowrap": 1,
        "revids": revid,
    }
    url = API + "?" + urllib.parse.urlencode(params)
    raw = fetch_or_reuse(xml_path, url, resume=resume, accept="application/xml")
    if f"<id>{revid}</id>".encode() not in raw:
        raise RuntimeError(f"XML export did not bind revision {revid}")
    return raw


def freeze_entry(
    *,
    title: str,
    stem: str,
    target: Path,
    resume: bool,
    parse_surface: bool,
) -> tuple[dict[str, Any], str, dict[str, Any] | None]:
    api_path = target / f"{stem}-api.json"
    api_raw, api_data = api_or_reuse(
        api_path,
        {
            "action": "query",
            "prop": "revisions",
            "rvprop": REVISION_PROPS,
            "rvslots": "main",
            "titles": title,
        },
        resume=resume,
    )
    page, revision, content = revision_page(api_data, title)
    record = page_metadata(page, revision, content)
    record.update(
        {
            "api_file": api_path.name,
            "api_bytes": len(api_raw),
            "api_sha256": sha256(api_path),
            "oldid_url": f"https://de.wikiversity.org/w/index.php?oldid={revision['revid']}",
        }
    )

    xml_path = target / f"{stem}.xml"
    xml_raw = exact_xml(revision["revid"], xml_path=xml_path, resume=resume)
    record.update(
        {
            "xml_file": xml_path.name,
            "xml_bytes": len(xml_raw),
            "xml_sha256": sha256(xml_path),
        }
    )

    html_path = target / f"{stem}.html"
    html_raw, html_source = exact_html(
        page["title"], revision["revid"], html_path=html_path, resume=resume
    )
    record.update(
        {
            "html_file": html_path.name,
            "html_bytes": len(html_raw),
            "html_sha256": sha256(html_path),
            "html_source": html_source,
        }
    )

    parse_data: dict[str, Any] | None = None
    if parse_surface:
        parse_path = target / f"{stem}-parse-api.json"
        parse_raw, parse_data = api_or_reuse(
            parse_path,
            {
                "action": "parse",
                "oldid": revision["revid"],
                "prop": "links|templates|images|externallinks|sections|displaytitle",
            },
            resume=resume,
        )
        parse_root = parse_data.get("parse", {})
        record.update(
            {
                "parse_api_file": parse_path.name,
                "parse_api_bytes": len(parse_raw),
                "parse_api_sha256": sha256(parse_path),
                "template_count": len(parse_root.get("templates", [])),
                "image_count": len(parse_root.get("images", [])),
                "link_count": len(parse_root.get("links", [])),
                "external_link_count": len(parse_root.get("externallinks", [])),
            }
        )
    return record, content, parse_data


def transclusion_closure(
    *,
    prefix: str,
    template_titles: list[str],
    target: Path,
    resume: bool,
) -> dict[str, Any]:
    requested = sorted(set(template_titles), key=str.casefold)
    batches: list[dict[str, Any]] = []
    pages_by_title: dict[str, dict[str, Any]] = {}
    for start in range(0, len(requested), 25):
        titles = requested[start : start + 25]
        path = target / f"{prefix}-transclusions-{start // 25 + 1:02d}.json"
        raw, parsed = api_or_reuse(
            path,
            {
                "action": "query",
                "prop": "revisions",
                "rvprop": REVISION_PROPS,
                "rvslots": "main",
                "titles": "|".join(titles),
            },
            resume=resume,
        )
        batch_pages = parsed.get("query", {}).get("pages", [])
        missing = [page.get("title") for page in batch_pages if page.get("missing")]
        if missing:
            raise RuntimeError(f"Missing transclusions for {prefix}: {missing}")
        for page in batch_pages:
            revisions = page.get("revisions", [])
            if len(revisions) != 1:
                raise RuntimeError(f"No unique revision for transclusion {page.get('title')!r}")
            revision = revisions[0]
            content = revision.get("slots", {}).get("main", {}).get("content")
            if not isinstance(content, str):
                raise RuntimeError(f"No main-slot content for {page.get('title')!r}")
            pages_by_title[page["title"]] = page_metadata(page, revision, content)
        batches.append(
            {
                "file": path.name,
                "bytes": len(raw),
                "sha256": sha256(path),
                "requested_titles": titles,
            }
        )
    if len(pages_by_title) != len(requested):
        raise RuntimeError(
            f"Transclusion closure mismatch for {prefix}: requested {len(requested)}, captured {len(pages_by_title)}"
        )
    return {
        "requested_template_count": len(requested),
        "captured_page_count": len(pages_by_title),
        "missing_page_count": 0,
        "batches": batches,
        "pages": [pages_by_title[title] for title in sorted(pages_by_title, key=str.casefold)],
    }


INPUT_EXERCISE = re.compile(
    r"\{\{\s*inputaufgabe\s*\|\s*([^|}\r\n]+?)\s*(?=\||\}\})",
    re.IGNORECASE,
)


def exercise_titles(wikitext: str) -> list[str]:
    titles = [match.group(1).strip() for match in INPUT_EXERCISE.finditer(wikitext)]
    if not titles or len(titles) != len(set(titles)):
        raise RuntimeError(f"Exercise extraction failed or produced duplicates: {len(titles)}")
    return titles


def freeze_solutions(
    *,
    unit: int,
    worksheet_record: dict[str, Any],
    worksheet_wikitext: str,
    target: Path,
    resume: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    exercises = exercise_titles(worksheet_wikitext)
    solution_titles = [title + "/Lösung" for title in exercises]
    candidate_path = target / "worksheet-solution-candidates-api.json"
    raw, parsed = api_or_reuse(
        candidate_path,
        {
            "action": "query",
            "prop": "revisions",
            "rvprop": REVISION_PROPS,
            "rvslots": "main",
            "titles": "|".join(solution_titles),
        },
        resume=resume,
    )
    candidates = {
        page["title"]: page for page in parsed.get("query", {}).get("pages", [])
    }
    normalized = {
        item["from"]: item["to"]
        for item in parsed.get("query", {}).get("normalized", [])
    }
    redirects = {
        item["from"]: item["to"]
        for item in parsed.get("query", {}).get("redirects", [])
    }
    entries: list[dict[str, Any]] = []
    solution_records: list[dict[str, Any]] = []
    for number, (exercise, requested_solution) in enumerate(
        zip(exercises, solution_titles, strict=True), start=1
    ):
        resolved_solution = requested_solution
        visited: set[str] = set()
        while resolved_solution not in visited:
            visited.add(resolved_solution)
            next_title = normalized.get(resolved_solution) or redirects.get(resolved_solution)
            if next_title is None:
                break
            resolved_solution = next_title
        page = candidates.get(resolved_solution)
        if page is None:
            raise RuntimeError(f"Solution candidate absent from API response: {requested_solution}")
        entry: dict[str, Any] = {
            "exercise_number": number,
            "exercise_title": exercise,
            "solution_title": requested_solution,
            "has_public_solution": not bool(page.get("missing")),
        }
        if page.get("missing"):
            entries.append(entry)
            continue
        revisions = page.get("revisions", [])
        if len(revisions) != 1:
            raise RuntimeError(f"No unique public solution revision: {requested_solution}")
        revision = revisions[0]
        content = revision.get("slots", {}).get("main", {}).get("content")
        if not isinstance(content, str):
            raise RuntimeError(f"No public solution wikitext: {requested_solution}")
        meta = page_metadata(page, revision, content)
        xml_path = target / f"solution-ex{number:02d}.xml"
        xml_raw = exact_xml(revision["revid"], xml_path=xml_path, resume=resume)
        html_path = target / f"solution-ex{number:02d}.html"
        html_raw, html_source = exact_html(
            page["title"], revision["revid"], html_path=html_path, resume=resume
        )
        entry.update(
            {
                "pageid": meta["pageid"],
                "revid": meta["revid"],
                "parentid": meta["parentid"],
                "timestamp": meta["timestamp"],
                "mediawiki_sha1": meta["mediawiki_sha1"],
                "oldid_url": f"https://de.wikiversity.org/w/index.php?oldid={meta['revid']}",
                "xml_file": xml_path.name,
                "xml_bytes": len(xml_raw),
                "xml_sha256": sha256(xml_path),
                "html_file": html_path.name,
                "html_bytes": len(html_raw),
                "html_sha256": sha256(html_path),
                "html_source": html_source,
            }
        )
        entries.append(entry)
        solution_records.append({**entry, "wikitext_bytes": meta["wikitext_bytes"]})

    ordered_map = {
        "schema": "brenner-worksheet-solution-map-v2",
        "unit": unit,
        "worksheet": worksheet_record,
        "exercise_count": len(entries),
        "solution_count": len(solution_records),
        "candidate_api_file": candidate_path.name,
        "candidate_api_bytes": len(raw),
        "candidate_api_sha256": sha256(candidate_path),
        "entries": entries,
    }
    map_path = target / "ORDERED_EXERCISE_MAP.json"
    write_json(map_path, ordered_map)
    solutions_manifest = {
        "worksheet": worksheet_record,
        "exercise_count": len(entries),
        "solution_count": len(solution_records),
        "candidate_api_file": candidate_path.name,
        "candidate_api_bytes": len(raw),
        "candidate_api_sha256": sha256(candidate_path),
        "entries": entries,
        "map_file": map_path.name,
        "map_bytes": map_path.stat().st_size,
        "map_sha256": sha256(map_path),
    }
    return ordered_map, solutions_manifest


def derive_tex(html_path: Path, tex_path: Path) -> None:
    soup = BeautifulSoup(html_path.read_bytes(), "html.parser")
    text = soup.get_text(separator="\n").replace("\xa0", " ")
    lines = [line.rstrip() for line in text.splitlines()]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    tex_path.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def freeze_official_pdfs(
    *,
    unit: int,
    image_names: list[str],
    target: Path,
    resume: bool,
) -> list[dict[str, Any]]:
    pdf_names = sorted({name for name in image_names if name.lower().endswith(".pdf")})
    if not pdf_names:
        raise RuntimeError("No official PDF file surfaces found in parse images")
    metadata_path = target / "official-pdfs-api.json"
    raw, parsed = api_or_reuse(
        metadata_path,
        {
            "action": "query",
            "prop": "imageinfo",
            "iiprop": "url|size|mime|sha1|timestamp",
            "titles": "|".join("File:" + name for name in pdf_names),
        },
        resume=resume,
    )
    del raw
    artifact_root = ROOT / "authority" / "artifacts"
    artifact_root.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    for page in parsed.get("query", {}).get("pages", []):
        info_rows = page.get("imageinfo", [])
        if len(info_rows) != 1:
            raise RuntimeError(f"No unique official PDF imageinfo for {page.get('title')}")
        info = info_rows[0]
        title = page["title"].removeprefix("File:")
        kind = "lecture" if "Vorlesung" in title else "worksheet" if "Arbeitsblatt" in title else "other"
        output = artifact_root / f"{kind}-{unit:02d}-official.pdf"
        pdf_raw = fetch_or_reuse(output, info["url"], resume=resume, accept="application/pdf")
        if not pdf_raw.startswith(b"%PDF-"):
            raise RuntimeError(f"Official PDF does not have a PDF signature: {title}")
        records.append(
            {
                "source_file_title": title,
                "pageid": page.get("pageid"),
                "image_timestamp": info.get("timestamp"),
                "mediawiki_sha1": info.get("sha1"),
                "source_bytes": info.get("size"),
                "mime": info.get("mime"),
                "source_url": info["url"],
                "description_url": info.get("descriptionurl"),
                "local_path": output.relative_to(ROOT).as_posix(),
                "local_bytes": len(pdf_raw),
                "local_sha256": sha256(output),
            }
        )
    if not {record["kind"] if "kind" in record else record["local_path"].split("/")[-1].split("-")[0] for record in records} >= {"lecture", "worksheet"}:
        raise RuntimeError(f"Official PDF closure lacks lecture or worksheet witness: {records}")
    return sorted(records, key=lambda record: record["local_path"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", type=int, required=True)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    unit = args.unit
    if not 1 <= unit <= 30:
        raise SystemExit("--unit must be between 1 and 30")
    target = ROOT / "authority" / "wikiversity" / f"unit-{unit:02d}"
    if target.exists() and any(target.iterdir()) and not args.resume:
        raise SystemExit(f"Refusing to overwrite non-empty authority directory: {target}")
    target.mkdir(parents=True, exist_ok=True)

    lecture_title = f"{COURSE}/Vorlesung {unit}"
    worksheet_title = f"{COURSE}/Arbeitsblatt {unit}"
    lecture, lecture_wikitext, lecture_parse = freeze_entry(
        title=lecture_title,
        stem=f"lecture-{unit:02d}",
        target=target,
        resume=args.resume,
        parse_surface=True,
    )
    worksheet, worksheet_wikitext, worksheet_parse = freeze_entry(
        title=worksheet_title,
        stem=f"worksheet-{unit:02d}",
        target=target,
        resume=args.resume,
        parse_surface=True,
    )
    assert lecture_parse is not None and worksheet_parse is not None

    lecture_latex, _, _ = freeze_entry(
        title=lecture_title + "/latex",
        stem=f"lecture-{unit:02d}-latex-page",
        target=target,
        resume=args.resume,
        parse_surface=False,
    )
    worksheet_latex, _, _ = freeze_entry(
        title=worksheet_title + "/latex",
        stem=f"worksheet-{unit:02d}-latex-page",
        target=target,
        resume=args.resume,
        parse_surface=False,
    )
    lecture_tex = target / f"lecture-{unit:02d}-expanded.tex"
    worksheet_tex = target / f"worksheet-{unit:02d}-expanded.tex"
    derive_tex(target / lecture_latex["html_file"], lecture_tex)
    derive_tex(target / worksheet_latex["html_file"], worksheet_tex)

    lecture_templates = [row["title"] for row in lecture_parse["parse"].get("templates", [])]
    worksheet_templates = [row["title"] for row in worksheet_parse["parse"].get("templates", [])]
    lecture_closure = transclusion_closure(
        prefix=f"lecture-{unit:02d}",
        template_titles=lecture_templates,
        target=target,
        resume=args.resume,
    )
    worksheet_closure = transclusion_closure(
        prefix=f"worksheet-{unit:02d}",
        template_titles=worksheet_templates,
        target=target,
        resume=args.resume,
    )
    ordered_map, solutions = freeze_solutions(
        unit=unit,
        worksheet_record=worksheet,
        worksheet_wikitext=worksheet_wikitext,
        target=target,
        resume=args.resume,
    )
    del ordered_map

    lecture_images = lecture_parse["parse"].get("images", [])
    worksheet_images = worksheet_parse["parse"].get("images", [])
    official_pdfs = freeze_official_pdfs(
        unit=unit,
        image_names=lecture_images + worksheet_images,
        target=target,
        resume=args.resume,
    )

    manifest_path = target / "UNIT_AUTHORITY_MANIFEST.json"
    files = [file_fact(path, target) for path in sorted(target.iterdir()) if path.is_file() and path != manifest_path]
    manifest = {
        "schema": "brenner-unit-authority-freeze-v2",
        "frozen_utc": datetime.now(timezone.utc).isoformat(),
        "unit_number": unit,
        "source_api": API,
        "lecture": lecture,
        "worksheet": worksheet,
        "lecture_latex_page": lecture_latex,
        "worksheet_latex_page": worksheet_latex,
        "derived_expanded_tex": [file_fact(lecture_tex, target), file_fact(worksheet_tex, target)],
        "lecture_transclusion_closure": lecture_closure,
        "worksheet_transclusion_closure": worksheet_closure,
        "solutions": solutions,
        "images": {"lecture": lecture_images, "worksheet": worksheet_images},
        "official_pdf_witnesses": official_pdfs,
        "files": files,
    }
    write_json(manifest_path, manifest)

    print(
        json.dumps(
            {
                "status": "PASS",
                "unit": unit,
                "lecture_revid": lecture["revid"],
                "worksheet_revid": worksheet["revid"],
                "lecture_transclusions": lecture_closure["captured_page_count"],
                "worksheet_transclusions": worksheet_closure["captured_page_count"],
                "exercises": solutions["exercise_count"],
                "public_solutions": solutions["solution_count"],
                "images": len(set(lecture_images + worksheet_images)),
                "manifest_files": len(files),
                "manifest": manifest_path.relative_to(ROOT).as_posix(),
                "manifest_bytes": manifest_path.stat().st_size,
                "manifest_sha256": sha256(manifest_path),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise
