#!/usr/bin/env python3
"""Read-only authenticated Figshare preflight for the Unit 7 work item."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release" / "unit-07"
TOKEN_FILE = Path.home() / "Documents" / "TOKENS" / "Figshare Token.md"
BASE = "https://api.figshare.com/v2"
PROJECT_ID = 280296
COLLECTION_ID = 8668413
TITLE = "Kurva Aljabar — Edisi Bahasa Indonesia"
CONCEPT_DOI = "10.5281/zenodo.22059686"
FILES = [
    "kurva-aljabar-id-unit-07.pdf",
    "kurva-aljabar-id-unit-07.html",
    "kurva-aljabar-id-unit-07-source.zip",
    "LICENSE-unit-07.md",
    "ZENODO_FILE_MANIFEST-unit-07.json",
]


def token_from_file() -> str:
    text = TOKEN_FILE.read_text(encoding="utf-8-sig")
    candidates: list[str] = []
    for line in text.splitlines():
        cleaned = line.strip().strip("`'\"")
        if not cleaned:
            continue
        if ":" in cleaned and "token" in cleaned.lower():
            cleaned = cleaned.split(":", 1)[1].strip().strip("`'\"")
        candidates.extend(re.findall(r"[A-Za-z0-9._-]{32,}", cleaned))
    if not candidates:
        raise RuntimeError("No Figshare token candidate found in the designated credential file")
    return max(candidates, key=len)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def get(session: requests.Session, endpoint: str):
    url = endpoint if endpoint.startswith("http") else f"{BASE}/{endpoint.lstrip('/')}"
    response = session.get(url, timeout=120)
    if not response.ok:
        raise RuntimeError(f"Figshare GET {url} failed with HTTP {response.status_code}: {response.text[:1000]}")
    return response.json()


def main() -> None:
    token = token_from_file()
    session = requests.Session()
    session.headers.update({
        "Authorization": f"token {token}",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://figshare.com",
        "Referer": "https://figshare.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140 Safari/537.36",
    })

    licenses = get(session, "account/licenses")
    articles = get(session, f"account/projects/{PROJECT_ID}/articles?limit=1000")
    collection_articles = get(session, f"account/collections/{COLLECTION_ID}/articles?limit=1000")
    collection_detail = get(session, f"account/collections/{COLLECTION_ID}")

    detailed = []
    for item in articles:
        article_id = int(item["id"])
        detail = get(session, f"account/articles/{article_id}")
        files = detail.get("files", [])
        detailed.append(
            {
                "id": article_id,
                "title": detail.get("title"),
                "doi": detail.get("doi"),
                "url_public_html": detail.get("url_public_html"),
                "file_bytes": sum(int(file.get("size", 0)) for file in files),
                "file_count": len(files),
            }
        )

    matches = [
        item for item in detailed
        if item.get("title") == TITLE or item.get("doi") == CONCEPT_DOI
    ]
    local_files = []
    for name in FILES:
        path = RELEASE / name
        if not path.is_file():
            raise FileNotFoundError(path)
        local_files.append({"name": name, "bytes": path.stat().st_size, "sha256": sha256(path)})

    result = {
        "status": "PASS",
        "project_id": PROJECT_ID,
        "project_article_count": len(detailed),
        "project_current_file_bytes": sum(item["file_bytes"] for item in detailed),
        "project_cap_bytes": 20000000000,
        "existing_work_matches": matches,
        "collection_id": COLLECTION_ID,
        "collection_article_count": len(collection_articles),
        "collection_contains_work": any(int(item["id"]) == 33314856 for item in collection_articles),
        "collection_state": {
            "doi": collection_detail.get("doi"),
            "version": collection_detail.get("version"),
            "is_public": collection_detail.get("is_public"),
            "url_public_html": collection_detail.get("url_public_html"),
            "links": collection_detail.get("links"),
        },
        "available_licenses": [
            {
                "id": item.get("id") or item.get("value"),
                "raw_keys": sorted(item),
                "name": item.get("name"),
                "url": item.get("url"),
            }
            for item in licenses
        ],
        "local_payload": local_files,
        "local_payload_bytes": sum(item["bytes"] for item in local_files),
        "work_cap_bytes": 500000000,
        "credential_value_logged_or_persisted": False,
    }
    del token
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
