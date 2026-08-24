#!/usr/bin/env python3
"""Freeze the official Unit 12 Wikiversity/Commons authority closure.

This helper is deliberately bounded to Unit 12.  It captures immutable entry
surfaces, parser-recursive transclusions, ordered exercises and every extant
public solution, /latex witnesses, official PDFs, substantive media, and
component-rights metadata.  It does not read or modify translated units,
builds, publication state, Git, or Units 1--11.
"""

from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
UNIT = 12
OUT = ROOT / "authority" / "wikiversity" / "unit-12"
ARTIFACTS = ROOT / "authority" / "artifacts"
ASSETS = ROOT / "authority" / "assets"
RIGHTS = ROOT / "authority" / "RIGHTS-unit-12.csv"
CLOSURE = ROOT / "authority" / "ASSET_CLOSURE-unit-12.json"
COMMONS_META = ROOT / "authority" / "commons-imageinfo-unit-12.json"
WIKI_API = "https://de.wikiversity.org/w/api.php"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
REST_HTML = "https://de.wikiversity.org/api/rest_v1/page/html"
COURSE = "Kurs:Algebraische Kurven (Osnabrück 2025-2026)"
LECTURE_TITLE = f"{COURSE}/Vorlesung {UNIT}"
WORKSHEET_TITLE = f"{COURSE}/Arbeitsblatt {UNIT}"
USER_AGENT = "O016-unit12-authority-freeze/1.0 (bounded educational preservation)"
MIN_REQUEST_INTERVAL = 3.0
_last_request = 0.0


def digest_bytes(data: bytes, algorithm: str = "sha256") -> str:
    return hashlib.new(algorithm, data).hexdigest()


def digest(path: Path, algorithm: str = "sha256") -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def write_json(path: Path, payload: object) -> None:
    write_bytes(path, (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def fetch(url: str, attempts: int = 12) -> bytes:
    global _last_request
    parsed_url = urllib.parse.urlsplit(url)
    if parsed_url.hostname == "upload.wikimedia.org" and parsed_url.query:
        url = urllib.parse.urlunsplit((parsed_url.scheme, parsed_url.netloc, parsed_url.path, "", ""))
    for attempt in range(1, attempts + 1):
        pause = MIN_REQUEST_INTERVAL - (time.monotonic() - _last_request)
        if pause > 0:
            time.sleep(pause)
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                data = response.read()
            _last_request = time.monotonic()
            if not data:
                raise RuntimeError(f"empty HTTP response: {url}")
            return data
        except urllib.error.HTTPError as exc:
            _last_request = time.monotonic()
            if exc.code not in {429, 500, 502, 503, 504} or attempt == attempts:
                raise
            retry_after = exc.headers.get("Retry-After")
            delay = min(30, int(retry_after)) if retry_after and retry_after.isdigit() else min(30, 4 + attempt * 3)
            time.sleep(delay)
        except urllib.error.URLError:
            _last_request = time.monotonic()
            if attempt == attempts:
                raise
            time.sleep(min(30, 4 + attempt * 3))
    raise AssertionError("unreachable")


def api_raw(api: str, params: dict[str, object]) -> tuple[bytes, dict]:
    query = dict(params)
    query.setdefault("format", "json")
    query.setdefault("formatversion", 2)
    query.setdefault("maxlag", 5)
    url = api + "?" + urllib.parse.urlencode(query)
    for _ in range(12):
        raw = fetch(url)
        payload = json.loads(raw.decode("utf-8"))
        error = payload.get("error")
        if not error:
            return raw, payload
        if error.get("code") not in {"maxlag", "ratelimited"}:
            raise RuntimeError(f"MediaWiki API error: {error}")
        time.sleep(10)
    raise RuntimeError(f"MediaWiki API remained unavailable: {url}")


def one_page(payload: dict, *, allow_shared_missing: bool = False) -> dict:
    pages = payload.get("query", {}).get("pages", [])
    if len(pages) != 1:
        raise RuntimeError(f"expected exactly one page, got {len(pages)}")
    page = pages[0]
    if page.get("missing") and not (allow_shared_missing and page.get("known")):
        raise RuntimeError(f"missing page: {page.get('title')}")
    return page


def revision(page: dict) -> dict:
    revisions = page.get("revisions", [])
    if len(revisions) != 1:
        raise RuntimeError(f"expected one revision for {page.get('title')}")
    return revisions[0]


def content_bytes(rev: dict) -> int:
    return len(rev["slots"]["main"]["content"].encode("utf-8"))


def export_xml(revid: int) -> bytes:
    params = {
        "action": "query",
        "revids": revid,
        "export": 1,
        "exportnowrap": 1,
        "format": "json",
        "formatversion": 2,
        "maxlag": 5,
    }
    data = fetch(WIKI_API + "?" + urllib.parse.urlencode(params))
    if not data.lstrip().startswith(b"<"):
        payload = json.loads(data.decode("utf-8"))
        export = payload.get("query", {}).get("export")
        if isinstance(export, dict):
            xml = export.get("*") or export.get("content")
        else:
            xml = export
        if not isinstance(xml, str):
            raise RuntimeError(f"API export did not return XML for revision {revid}")
        data = xml.encode("utf-8")
    if not re.search(rb"<revision>.*?<id>\s*" + str(revid).encode("ascii") + rb"\s*</id>", data, re.S):
        raise RuntimeError(f"XML export does not bind revision {revid}")
    return data


def exact_html(title: str, revid: int) -> bytes:
    encoded = urllib.parse.quote(title.replace(" ", "_"), safe="")
    data = fetch(f"{REST_HTML}/{encoded}/{revid}")
    needle = f"revision/{revid}".encode("ascii")
    if needle not in data and f'content="{revid}"'.encode("ascii") not in data:
        raise RuntimeError(f"Parsoid HTML does not identify revision {revid}: {title}")
    return data


def entry_surface(title: str, stem: str) -> tuple[dict, dict]:
    raw, payload = api_raw(
        WIKI_API,
        {
            "action": "query",
            "prop": "revisions",
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "main",
            "titles": title,
        },
    )
    api_path = OUT / f"{stem}-api.json"
    write_bytes(api_path, raw)
    page = one_page(payload)
    rev = revision(page)
    revid = int(rev["revid"])

    xml_path = OUT / f"{stem}.xml"
    html_path = OUT / f"{stem}.html"
    write_bytes(xml_path, export_xml(revid))
    write_bytes(html_path, exact_html(title, revid))

    parse_raw, parse_payload = api_raw(
        WIKI_API,
        {
            "action": "parse",
            "oldid": revid,
            "prop": "links|templates|images|externallinks|tocdata",
        },
    )
    parse_path = OUT / f"{stem}-parse-api.json"
    write_bytes(parse_path, parse_raw)
    parsed = parse_payload["parse"]
    if int(parsed["pageid"]) != int(page["pageid"]) or int(parsed["revid"]) != revid:
        raise RuntimeError(f"parse identity drift: {title}")

    record = {
        "title": page["title"],
        "pageid": int(page["pageid"]),
        "revid": revid,
        "parentid": int(rev.get("parentid", 0)),
        "timestamp": rev["timestamp"],
        "mediawiki_sha1": rev["sha1"],
        "wikitext_bytes": content_bytes(rev),
        "api_file": api_path.name,
        "api_bytes": api_path.stat().st_size,
        "api_sha256": digest(api_path),
        "oldid_url": f"https://de.wikiversity.org/w/index.php?oldid={revid}",
        "xml_file": xml_path.name,
        "xml_bytes": xml_path.stat().st_size,
        "xml_sha256": digest(xml_path),
        "html_file": html_path.name,
        "html_bytes": html_path.stat().st_size,
        "html_sha256": digest(html_path),
        "html_source": "immutable Parsoid revision endpoint",
        "parse_api_file": parse_path.name,
        "parse_api_bytes": parse_path.stat().st_size,
        "parse_api_sha256": digest(parse_path),
        "template_count": len(parsed.get("templates", [])),
        "image_count": len(parsed.get("images", [])),
        "link_count": len(parsed.get("links", [])),
        "external_link_count": len(parsed.get("externallinks", [])),
    }
    return record, parsed


class TeXText(HTMLParser):
    BREAKS = {"br", "p", "div", "section", "li", "h1", "h2", "h3", "h4"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.BREAKS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.BREAKS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        value = "".join(self.parts).replace("\r", "")
        value = re.sub(r"[ \t]+\n", "\n", value)
        value = re.sub(r"\n{4,}", "\n\n\n", value)
        return value.strip() + "\n"


def latex_surface(title: str, stem: str) -> tuple[dict, dict]:
    raw, payload = api_raw(
        WIKI_API,
        {
            "action": "query",
            "prop": "revisions",
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "main",
            "titles": title,
        },
    )
    api_path = OUT / f"{stem}-latex-page-api.json"
    write_bytes(api_path, raw)
    page = one_page(payload)
    rev = revision(page)
    revid = int(rev["revid"])
    xml_path = OUT / f"{stem}-latex-page.xml"
    html_path = OUT / f"{stem}-latex-page.html"
    write_bytes(xml_path, export_xml(revid))
    html_bytes = exact_html(title, revid)
    write_bytes(html_path, html_bytes)
    parser = TeXText()
    parser.feed(html_bytes.decode("utf-8"))
    expanded_path = OUT / f"{stem}-expanded.tex"
    expanded_path.write_text(title + "\n" + parser.text(), encoding="utf-8", newline="\n")
    return (
        {
            "title": page["title"],
            "pageid": int(page["pageid"]),
            "revid": revid,
            "parentid": int(rev.get("parentid", 0)),
            "timestamp": rev["timestamp"],
            "mediawiki_sha1": rev["sha1"],
            "wikitext_bytes": content_bytes(rev),
            "api_file": api_path.name,
            "api_bytes": api_path.stat().st_size,
            "api_sha256": digest(api_path),
            "oldid_url": f"https://de.wikiversity.org/w/index.php?oldid={revid}",
            "xml_file": xml_path.name,
            "xml_bytes": xml_path.stat().st_size,
            "xml_sha256": digest(xml_path),
            "html_file": html_path.name,
            "html_bytes": html_path.stat().st_size,
            "html_sha256": digest(html_path),
            "html_source": "immutable Parsoid revision endpoint",
        },
        {
            "file": expanded_path.name,
            "bytes": expanded_path.stat().st_size,
            "sha256": digest(expanded_path),
        },
    )


def transclusion_closure(parsed: dict, stem: str) -> dict:
    titles = sorted({item["title"] for item in parsed.get("templates", [])})
    pages_out: list[dict] = []
    batches: list[dict] = []
    for index in range(0, len(titles), 25):
        requested = titles[index : index + 25]
        raw, payload = api_raw(
            WIKI_API,
            {
                "action": "query",
                "prop": "revisions",
                "rvprop": "ids|timestamp|sha1|content",
                "rvslots": "main",
                "titles": "|".join(requested),
            },
        )
        path = OUT / f"{stem}-transclusions-{index // 25 + 1:02d}.json"
        write_bytes(path, raw)
        batch_pages = payload.get("query", {}).get("pages", [])
        if len(batch_pages) != len(requested):
            raise RuntimeError(f"transclusion count mismatch in {path.name}")
        for page in batch_pages:
            if page.get("missing"):
                raise RuntimeError(f"missing recursive transclusion: {page.get('title')}")
            rev = revision(page)
            pages_out.append(
                {
                    "title": page["title"],
                    "pageid": int(page["pageid"]),
                    "revid": int(rev["revid"]),
                    "parentid": int(rev.get("parentid", 0)),
                    "timestamp": rev["timestamp"],
                    "mediawiki_sha1": rev["sha1"],
                    "wikitext_bytes": content_bytes(rev),
                }
            )
        batches.append(
            {
                "file": path.name,
                "bytes": path.stat().st_size,
                "sha256": digest(path),
                "requested_titles": requested,
            }
        )
    if len(pages_out) != len(titles) or len({p["title"] for p in pages_out}) != len(titles):
        raise RuntimeError(f"recursive transclusion closure failed for {stem}")
    return {
        "source": "action=parse template list after recursive parser expansion",
        "requested_template_count": len(titles),
        "captured_page_count": len(pages_out),
        "missing_page_count": 0,
        "batches": batches,
        "pages": sorted(pages_out, key=lambda item: item["title"]),
    }


def canonical_map(query: dict) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for item in query.get("normalized", []):
        mapping[item["from"]] = item["to"]
    for item in query.get("redirects", []):
        mapping[item["from"]] = item["to"]
    return mapping


def resolve_title(title: str, mapping: dict[str, str]) -> str:
    seen: set[str] = set()
    while title in mapping and title not in seen:
        seen.add(title)
        title = mapping[title]
    return title


def solution_map(worksheet: dict, parsed: dict) -> dict:
    exercises = [
        item["title"]
        for item in parsed.get("templates", [])
        if int(item.get("ns", -1)) != 10 and item["title"].endswith("/Aufgabe")
    ]
    if not exercises or len(exercises) != len(set(exercises)):
        raise RuntimeError("ordered exercise extraction is empty or duplicated")
    solution_titles = [title + "/Lösung" for title in exercises]
    raw, payload = api_raw(
        WIKI_API,
        {
            "action": "query",
            "prop": "revisions",
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "main",
            "redirects": 1,
            "titles": "|".join(solution_titles),
        },
    )
    candidates_path = OUT / "worksheet-solution-candidates-api.json"
    write_bytes(candidates_path, raw)
    query = payload.get("query", {})
    mapping = canonical_map(query)
    pages = {page["title"]: page for page in query.get("pages", [])}
    entries: list[dict] = []
    solution_count = 0
    for number, (exercise_title, solution_title) in enumerate(zip(exercises, solution_titles), start=1):
        resolved = resolve_title(solution_title, mapping)
        page = pages.get(resolved) or pages.get(solution_title)
        if page is None:
            raise RuntimeError(f"solution candidate missing from API response: {solution_title}")
        entry: dict[str, object] = {
            "exercise_number": number,
            "exercise_title": exercise_title,
            "solution_title": solution_title,
            "has_public_solution": not bool(page.get("missing")),
        }
        if not page.get("missing"):
            rev = revision(page)
            revid = int(rev["revid"])
            xml_path = OUT / f"solution-ex{number:02d}.xml"
            html_path = OUT / f"solution-ex{number:02d}.html"
            write_bytes(xml_path, export_xml(revid))
            write_bytes(html_path, exact_html(page["title"], revid))
            entry.update(
                {
                    "resolved_title": page["title"],
                    "pageid": int(page["pageid"]),
                    "revid": revid,
                    "parentid": int(rev.get("parentid", 0)),
                    "timestamp": rev["timestamp"],
                    "mediawiki_sha1": rev["sha1"],
                    "wikitext_bytes": content_bytes(rev),
                    "oldid_url": f"https://de.wikiversity.org/w/index.php?oldid={revid}",
                    "xml_file": xml_path.name,
                    "xml_bytes": xml_path.stat().st_size,
                    "xml_sha256": digest(xml_path),
                    "html_file": html_path.name,
                    "html_bytes": html_path.stat().st_size,
                    "html_sha256": digest(html_path),
                    "html_source": "immutable Parsoid revision endpoint",
                }
            )
            solution_count += 1
        entries.append(entry)
    result = {
        "schema": "brenner-worksheet-solution-map-v2",
        "unit": UNIT,
        "worksheet": worksheet,
        "exercise_count": len(exercises),
        "solution_count": solution_count,
        "candidate_api_file": candidates_path.name,
        "candidate_api_bytes": candidates_path.stat().st_size,
        "candidate_api_sha256": digest(candidates_path),
        "entries": entries,
    }
    path = OUT / "ORDERED_EXERCISE_MAP.json"
    write_json(path, result)
    result["map_file"] = path.name
    result["map_bytes"] = path.stat().st_size
    result["map_sha256"] = digest(path)
    return result


def file_key(title_or_name: str) -> str:
    value = title_or_name.split(":", 1)[-1]
    return value.replace(" ", "_").lower()


def plain(value: object) -> str:
    text = "" if value is None else str(value)
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(html.unescape(text).split())


def ext(metadata: dict, key: str) -> str:
    return plain(metadata.get(key, {}).get("value", ""))


def shared_media(lecture_parsed: dict, worksheet_parsed: dict) -> tuple[list[dict], list[dict]]:
    image_names = list(dict.fromkeys(lecture_parsed.get("images", []) + worksheet_parsed.get("images", [])))
    pdf_names = [name for name in image_names if name.lower().endswith(".pdf")]
    media_names = [name for name in image_names if not name.lower().endswith(".pdf")]
    lecture_pdf = [name for name in pdf_names if f"Vorlesung{UNIT}.pdf" in name.replace("_", "")]
    worksheet_pdf = [name for name in pdf_names if f"Arbeitsblatt{UNIT}.pdf" in name.replace("_", "")]
    if len(lecture_pdf) != 1 or len(worksheet_pdf) != 1:
        raise RuntimeError(f"official Unit {UNIT} PDF identity is not unique: {pdf_names}")

    wiki_raw, wiki_payload = api_raw(
        WIKI_API,
        {
            "action": "query",
            "prop": "imageinfo",
            "iiprop": "timestamp|url|size|sha1|mime|mediatype",
            "titles": "|".join("File:" + name for name in [lecture_pdf[0], worksheet_pdf[0]]),
        },
    )
    official_api_path = OUT / "official-pdfs-api.json"
    write_bytes(official_api_path, wiki_raw)

    all_names = media_names + [lecture_pdf[0], worksheet_pdf[0]]
    commons_raw, commons_payload = api_raw(
        COMMONS_API,
        {
            "action": "query",
            "prop": "imageinfo|revisions",
            "iiprop": "timestamp|user|url|size|sha1|mime|mediatype|extmetadata",
            "iiurlwidth": 200,
            "rvprop": "ids|timestamp|sha1|content",
            "rvslots": "main",
            "titles": "|".join("File:" + name for name in all_names),
        },
    )
    write_bytes(COMMONS_META, commons_raw)
    commons_pages = {
        file_key(page["title"]): page for page in commons_payload.get("query", {}).get("pages", [])
    }
    wiki_pages = {
        file_key(page["title"]): page for page in wiki_payload.get("query", {}).get("pages", [])
    }

    pdf_records: list[dict] = []
    for kind, name in (("lecture", lecture_pdf[0]), ("worksheet", worksheet_pdf[0])):
        page = wiki_pages.get(file_key(name))
        commons_page = commons_pages.get(file_key(name))
        if page is None or not page.get("imageinfo") or commons_page is None:
            raise RuntimeError(f"official PDF did not resolve: {name}")
        info = page["imageinfo"][0]
        commons_info = commons_page["imageinfo"][0]
        data = fetch(info["url"])
        if len(data) != int(info["size"]) or digest_bytes(data, "sha1") != info["sha1"]:
            raise RuntimeError(f"official PDF byte identity mismatch: {name}")
        local = ARTIFACTS / f"{kind}-{UNIT:02d}-official.pdf"
        write_bytes(local, data)
        reader = PdfReader(str(local))
        if reader.is_encrypted:
            raise RuntimeError(f"encrypted official PDF: {name}")
        metadata = commons_info.get("extmetadata", {})
        pdf_records.append(
            {
                "source_file_title": page["title"],
                "commons_pageid": commons_page.get("pageid"),
                "image_timestamp": info["timestamp"],
                "mediawiki_sha1": info["sha1"],
                "source_bytes": int(info["size"]),
                "mime": info["mime"],
                "source_url": info["url"],
                "description_url": info["descriptionurl"],
                "local_path": local.relative_to(ROOT).as_posix(),
                "local_bytes": local.stat().st_size,
                "local_sha256": digest(local),
                "page_count": len(reader.pages),
                "license_short": ext(metadata, "LicenseShortName") or ext(metadata, "UsageTerms"),
                "license_url": ext(metadata, "LicenseUrl"),
                "artist": ext(metadata, "Artist"),
                "credit": ext(metadata, "Credit"),
            }
        )

    rows: list[dict[str, object]] = []
    asset_records: list[dict] = []
    for order, name in enumerate(media_names, start=1):
        page = commons_pages.get(file_key(name))
        if page is None or page.get("missing") or not page.get("imageinfo"):
            raise RuntimeError(f"substantive media did not resolve on Commons: {name}")
        info = page["imageinfo"][0]
        original_name = urllib.parse.unquote(Path(urllib.parse.urlparse(info["url"]).path).name)
        original_local = ASSETS / original_name
        selected_form = "original"
        selected_url = info["url"]
        if (
            original_local.is_file()
            and original_local.stat().st_size == int(info["size"])
            and digest(original_local, "sha1") == info["sha1"]
        ):
            local = original_local
            data = local.read_bytes()
            expected_width, expected_height = int(info["width"]), int(info["height"])
        else:
            selected_url = info.get("thumburl", "")
            if not selected_url or not info.get("thumbwidth") or not info.get("thumbheight"):
                raise RuntimeError(f"Commons thumbnail fallback is absent: {name}")
            if "/thumb/" not in urllib.parse.urlparse(selected_url).path:
                original = urllib.parse.urlsplit(info["url"].split("?", 1)[0])
                parts = original.path.rsplit("/", 3)
                if len(parts) != 4:
                    raise RuntimeError(f"cannot derive allowed Commons thumbnail URL: {name}")
                base, shard_a, shard_b, filename = parts
                selected_url = urllib.parse.urlunsplit(
                    (
                        original.scheme,
                        original.netloc,
                        f"{base}/thumb/{shard_a}/{shard_b}/{filename}/120px-{filename}",
                        "",
                        "",
                    )
                )
            data = fetch(selected_url)
            local_name = urllib.parse.unquote(Path(urllib.parse.urlparse(selected_url).path).name)
            local = ASSETS / local_name
            if local.exists() and local.read_bytes() != data:
                raise RuntimeError(f"refusing to overwrite a different pre-existing asset: {local}")
            if not local.exists():
                write_bytes(local, data)
            expected_width, expected_height = int(info["thumbwidth"]), int(info["thumbheight"])
            selected_form = "official Commons thumbnail"
        frames = 1
        width, height = expected_width, expected_height
        if info.get("mediatype") == "BITMAP":
            with Image.open(local) as image:
                image.verify()
            with Image.open(local) as image:
                width, height = int(image.width), int(image.height)
                frames = int(getattr(image, "n_frames", 1))
        if selected_form == "original":
            if (width, height) != (int(info["width"]), int(info["height"])):
                raise RuntimeError(f"Commons original dimensions mismatch: {name}")
        else:
            if width <= 0 or height <= 0 or width > int(info["width"]) or height > int(info["height"]):
                raise RuntimeError(f"Commons thumbnail dimensions are invalid: {name}")
            if abs(width * int(info["height"]) - height * int(info["width"])) > max(width, int(info["width"])) * 2:
                raise RuntimeError(f"Commons thumbnail aspect ratio mismatch: {name}")
            selected_form = f"official Commons thumbnail ({width}px)"
        metadata = info.get("extmetadata", {})
        revs = page.get("revisions", [])
        desc_rev = revs[0] if len(revs) == 1 else None
        desc_content = desc_rev["slots"]["main"]["content"] if desc_rev else ""
        license_short = ext(metadata, "LicenseShortName") or ext(metadata, "UsageTerms")
        if not license_short:
            raise RuntimeError(f"Commons component license is absent: {name}")
        row = {
            "asset_id": f"br-ak-u12-media-{order:03d}",
            "reader_order": order,
            "resource_title": "File:" + name,
            "metadata_title": page["title"],
            "repository": "commons",
            "description_url": info["descriptionurl"],
            "original_url": info["url"].split("?", 1)[0],
            "selected_url": selected_url,
            "selected_form": selected_form,
            "local_path": local.relative_to(ROOT).as_posix(),
            "local_bytes": local.stat().st_size,
            "local_sha256": digest(local),
            "local_width": width,
            "local_height": height,
            "frame_count": frames,
            "pdf_local_path": "",
            "pdf_local_bytes": "",
            "pdf_local_sha256": "",
            "pdf_companion_source": "",
            "original_bytes": int(info["size"]),
            "original_sha1": info["sha1"],
            "original_width": int(info["width"]),
            "original_height": int(info["height"]),
            "mime": info["mime"],
            "media_type": info.get("mediatype", ""),
            "source_timestamp": info.get("timestamp", ""),
            "uploader": info.get("user", ""),
            "artist": ext(metadata, "Artist"),
            "credit": ext(metadata, "Credit"),
            "license_short": license_short,
            "usage_terms": ext(metadata, "UsageTerms"),
            "license_url": ext(metadata, "LicenseUrl"),
            "attribution_required": ext(metadata, "AttributionRequired"),
            "source_course_creator": "Holger Brenner / Wikiversity course page",
            "source_course_license": "CC BY-SA 4.0",
            "description_pageid": page.get("pageid", ""),
            "description_revid": desc_rev.get("revid", "") if desc_rev else "",
            "description_timestamp": desc_rev.get("timestamp", "") if desc_rev else "",
            "description_mediawiki_sha1": desc_rev.get("sha1", "") if desc_rev else "",
            "description_wikitext_bytes": len(desc_content.encode("utf-8")) if desc_content else "",
            "description_wikitext_sha256": digest_bytes(desc_content.encode("utf-8")) if desc_content else "",
            "html_animation_preserved": frames > 1,
        }
        rows.append(row)
        asset_records.append(
            {
                "asset_id": row["asset_id"],
                "repository": "commons",
                "metadata_title": page["title"],
                "local_path": row["local_path"],
                "local_bytes": row["local_bytes"],
                "local_sha256": row["local_sha256"],
                "width": width,
                "height": height,
                "frame_count": frames,
                "license_short": license_short,
                "license_url": row["license_url"],
                "html_animation_preserved": frames > 1,
            }
        )

    RIGHTS.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise RuntimeError("Unit 12 must contain at least one substantive media position")
    with RIGHTS.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    closure = {
        "schema": "brenner-unit-media-closure-v2",
        "unit": UNIT,
        "reader_media_positions": len(rows),
        "animated_html_positions": sum(1 for row in rows if row["html_animation_preserved"]),
        "unique_local_assets": len(asset_records),
        "metadata_file": COMMONS_META.relative_to(ROOT).as_posix(),
        "metadata_bytes": COMMONS_META.stat().st_size,
        "metadata_sha256": digest(COMMONS_META),
        "rights_file": RIGHTS.relative_to(ROOT).as_posix(),
        "rights_bytes": RIGHTS.stat().st_size,
        "rights_sha256": digest(RIGHTS),
        "official_pdf_witnesses_are_not_media_positions": True,
        "assets": asset_records,
    }
    write_json(CLOSURE, closure)
    return pdf_records, asset_records


def final_identity_recheck(lecture_revid: int, worksheet_revid: int) -> dict:
    raw, payload = api_raw(
        WIKI_API,
        {
            "action": "query",
            "prop": "revisions",
            "rvprop": "ids|timestamp|sha1",
            "titles": LECTURE_TITLE + "|" + WORKSHEET_TITLE,
        },
    )
    path = OUT / "final-entry-recheck-api.json"
    write_bytes(path, raw)
    got = {page["title"]: int(revision(page)["revid"]) for page in payload["query"]["pages"]}
    expected = {LECTURE_TITLE: lecture_revid, WORKSHEET_TITLE: worksheet_revid}
    if got != expected:
        raise RuntimeError(f"entry revision drift during freeze: expected {expected}, got {got}")
    return {"file": path.name, "bytes": path.stat().st_size, "sha256": digest(path), "result": "PASS"}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)

    lecture, lecture_parsed = entry_surface(LECTURE_TITLE, "lecture-12")
    worksheet, worksheet_parsed = entry_surface(WORKSHEET_TITLE, "worksheet-12")
    lecture_latex, lecture_tex = latex_surface(LECTURE_TITLE + "/latex", "lecture-12")
    worksheet_latex, worksheet_tex = latex_surface(WORKSHEET_TITLE + "/latex", "worksheet-12")
    lecture_closure = transclusion_closure(lecture_parsed, "lecture-12")
    worksheet_closure = transclusion_closure(worksheet_parsed, "worksheet-12")
    solutions = solution_map(worksheet, worksheet_parsed)
    official_pdfs, assets = shared_media(lecture_parsed, worksheet_parsed)
    recheck = final_identity_recheck(lecture["revid"], worksheet["revid"])

    manifest = {
        "schema": "brenner-unit-authority-freeze-v2",
        "frozen_utc": datetime.now(timezone.utc).isoformat(),
        "unit_number": UNIT,
        "source_api": WIKI_API,
        "source_course_license": "CC BY-SA 4.0",
        "lecture": lecture,
        "worksheet": worksheet,
        "lecture_latex_page": lecture_latex,
        "worksheet_latex_page": worksheet_latex,
        "derived_expanded_tex": [lecture_tex, worksheet_tex],
        "lecture_transclusion_closure": lecture_closure,
        "worksheet_transclusion_closure": worksheet_closure,
        "solutions": solutions,
        "images": {
            "lecture": lecture_parsed.get("images", []),
            "worksheet": worksheet_parsed.get("images", []),
            "substantive_assets": assets,
        },
        "official_pdf_witnesses": official_pdfs,
        "entry_revision_recheck": recheck,
    }
    manifest["files"] = [
        {"file": path.name, "bytes": path.stat().st_size, "sha256": digest(path)}
        for path in sorted(OUT.iterdir(), key=lambda item: item.name)
        if path.is_file() and path.name != "UNIT_AUTHORITY_MANIFEST.json"
    ]
    manifest_path = OUT / "UNIT_AUTHORITY_MANIFEST.json"
    write_json(manifest_path, manifest)

    # Fail closed by replaying every locally bound file and all topology counts.
    replay = json.loads(manifest_path.read_text(encoding="utf-8"))
    for record in replay["files"]:
        path = OUT / record["file"]
        if path.stat().st_size != record["bytes"] or digest(path) != record["sha256"]:
            raise RuntimeError(f"manifest replay failed: {path}")
    if replay["solutions"]["exercise_count"] != len(
        [item for item in worksheet_parsed["templates"] if item.get("ns") != 10 and item["title"].endswith("/Aufgabe")]
    ):
        raise RuntimeError("exercise topology replay failed")
    result = {
        "result": "PASS",
        "unit": UNIT,
        "lecture_pageid": lecture["pageid"],
        "lecture_revid": lecture["revid"],
        "worksheet_pageid": worksheet["pageid"],
        "worksheet_revid": worksheet["revid"],
        "lecture_transclusions": lecture_closure["captured_page_count"],
        "worksheet_transclusions": worksheet_closure["captured_page_count"],
        "exercises": solutions["exercise_count"],
        "public_solutions": solutions["solution_count"],
        "media_positions": len(assets),
        "official_pdf_pages": [item["page_count"] for item in official_pdfs],
        "manifest_bytes": manifest_path.stat().st_size,
        "manifest_sha256": digest(manifest_path),
        "rights_bytes": RIGHTS.stat().st_size,
        "rights_sha256": digest(RIGHTS),
        "closure_bytes": CLOSURE.stat().st_size,
        "closure_sha256": digest(CLOSURE),
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
