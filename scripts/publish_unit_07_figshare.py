#!/usr/bin/env python3
"""Publish the lawful Figshare work-level metadata record for Unit 7."""

from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
TOKEN_FILE = Path.home() / "Documents" / "TOKENS" / "Figshare Token.md"
RECEIPT = ROOT / "qa" / "UNIT_07_FIGSHARE_PUBLICATION.json"
BASE = "https://api.figshare.com/v2"
PROJECT_ID = 280296
COLLECTION_ID = 8668413
TITLE = "Kurva Aljabar — Edisi Bahasa Indonesia"
AUTHOR_ID = 24614067
CC0_ID = 2
ZENODO_CONCEPT = "10.5281/zenodo.22059686"
ZENODO_VERSION = "10.5281/zenodo.22062319"
SOURCE_URL = "https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)"
INVENTORY_DOI = "10.6084/m9.figshare.33314676.v1"
COLLECTION_REQUESTED_DOI = "10.6084/m9.figshare.c.8668413.v1"
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://figshare.com",
    "Referer": "https://figshare.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/140 Safari/537.36",
}


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


def call(session: requests.Session, method: str, endpoint: str, **kwargs) -> requests.Response:
    url = endpoint if endpoint.startswith("http") else f"{BASE}/{endpoint.lstrip('/')}"
    response = None
    for attempt in range(12):
        response = session.request(method, url, timeout=180, **kwargs)
        if response.ok:
            return response
        if response.status_code not in {403, 429, 500, 502, 503, 504}:
            break
        time.sleep(min(2 + attempt, 10))
    assert response is not None
    raise RuntimeError(f"Figshare {method} {url} failed with HTTP {response.status_code}: {response.text[:1000]}")


def description() -> str:
    return (
        "<p><strong>Catatan metadata saja; tidak ada byte edisi yang diunggah ke item Figshare ini.</strong> "
        "Berkas pembaca dan sumber terverifikasi tersedia pada DOI konsep Zenodo "
        f"<a href=\"https://doi.org/{ZENODO_CONCEPT}\">{ZENODO_CONCEPT}</a>; versi Unit 7 saat ini ialah "
        f"<a href=\"https://doi.org/{ZENODO_VERSION}\">{ZENODO_VERSION}</a>.</p>"
        "<p><strong>Status:</strong> <code>active_partial</code> — Unit 1–7 dari 30 unit <em>Algebraische "
        "Kurven (Osnabrück 2025–2026)</em> telah diterjemahkan dan diverifikasi. Batas kumulatif ini "
        "memuat tujuh kuliah, tujuh lembar kerja, seluruh 197 soal, seluruh 40 solusi publik yang "
        "tersedia pada revisi sumber yang dibekukan, 53 posisi media, pembaca HTML mandiri dengan "
        "MathML/reflow seluler, PDF A4 142 halaman, serta backend ID stabil dengan 5.182 rekaman. "
        "Ini belum merupakan edisi 30-unit yang lengkap; produksi berlanjut dalam urutan sumber.</p>"
        "<p><strong>Lisensi:</strong> CC0 hanya berlaku pada catatan metadata Figshare ini. Berkas "
        "edisi yang ditautkan tidak berlisensi CC0. Teks sumber dan adaptasi Indonesia berada di "
        "bawah CC BY-SA 4.0; media mempertahankan pencipta, sumber, dan lisensi komponennya "
        "masing-masing. Karena akun Figshare ini tidak menawarkan CC BY-SA atau lisensi campuran "
        "yang dapat menyatakan hak berkas dengan tepat, tidak ada byte edisi yang diunggah di sini.</p>"
        "<p>HTML adalah permukaan akses utama dan semantik; PDF tidak diklaim sebagai PDF bertag. "
        "Edisi ini merupakan adaptasi independen dan tidak disahkan oleh Holger Brenner, Universitas "
        "Osnabrück, Wikiversity, Wikimedia Commons, atau Wikimedia Foundation. Terjemahan, reflow, "
        "backend, dan QA dibuat atas arahan pengguna dengan OpenAI Codex gpt-5.6-sol, Ultra. Model "
        "bukan penulis karya.</p>"
    )


def metadata() -> dict:
    return {
        "title": TITLE,
        "description": description(),
        "defined_type": "book",
        "authors": [{"id": AUTHOR_ID}],
        "categories": [29830, 26095],
        "keywords": [
            "geometri aljabar",
            "algebraic geometry",
            "Bahasa Indonesia",
            "id-ID",
            "kurva aljabar",
            "open textbook",
            "active_partial",
        ],
        "license": CC0_ID,
        "references": [
            f"https://doi.org/{ZENODO_CONCEPT}",
            f"https://doi.org/{ZENODO_VERSION}",
            SOURCE_URL,
            f"https://doi.org/{INVENTORY_DOI}",
            f"https://doi.org/{COLLECTION_REQUESTED_DOI}",
        ],
        "timeline": {"online_publication": "2026-08-22"},
    }


def project_details(session: requests.Session) -> tuple[list[dict], int]:
    articles = call(session, "GET", f"account/projects/{PROJECT_ID}/articles?limit=1000").json()
    details = []
    total_bytes = 0
    for summary in articles:
        detail = call(session, "GET", f"account/articles/{int(summary['id'])}").json()
        files = detail.get("files", [])
        file_bytes = sum(int(item.get("size", 0)) for item in files)
        total_bytes += file_bytes
        details.append(detail)
    return details, total_bytes


def match_items(details: list[dict]) -> list[dict]:
    matches = []
    for item in details:
        refs = item.get("references") or []
        if item.get("title") == TITLE or any(ZENODO_CONCEPT in ref for ref in refs):
            matches.append(item)
    return matches


def public_get(endpoint: str) -> dict | list:
    url = f"{BASE}/{endpoint.lstrip('/')}"
    response = None
    for attempt in range(12):
        response = requests.get(url, headers=HEADERS, timeout=120)
        if response.ok:
            return response.json()
        if response.status_code not in {403, 429, 500, 502, 503, 504}:
            break
        time.sleep(min(2 + attempt, 10))
    assert response is not None
    response.raise_for_status()
    raise AssertionError("unreachable")


def wait_public_membership(endpoint: str, article_id: int) -> list[dict]:
    last: list[dict] = []
    for _ in range(60):
        payload = public_get(endpoint)
        if not isinstance(payload, list):
            raise RuntimeError(f"Unexpected Figshare membership response for {endpoint}")
        last = payload
        if article_id in {int(item["id"]) for item in payload}:
            return payload
        time.sleep(2)
    return last


def verify_public(article_id: int) -> dict:
    public = None
    for _ in range(60):
        response = requests.get(f"{BASE}/articles/{article_id}", headers=HEADERS, timeout=120)
        if response.ok:
            candidate = response.json()
            if candidate.get("is_public") and candidate.get("title") == TITLE:
                public = candidate
                break
        time.sleep(2)
    if public is None:
        raise RuntimeError("Figshare article did not become anonymously readable")
    if public.get("files"):
        raise RuntimeError("Metadata-only Figshare item unexpectedly exposes edition files")
    if public.get("license", {}).get("value") != CC0_ID:
        raise RuntimeError("Figshare metadata-record license mismatch")
    authors = public.get("authors", [])
    if [int(item["id"]) for item in authors] != [AUTHOR_ID]:
        raise RuntimeError(f"Figshare author list mismatch: {authors}")
    if "CC0 hanya berlaku pada catatan metadata Figshare ini" not in public.get("description", ""):
        raise RuntimeError("Figshare license-scope warning missing")
    return public


def main() -> None:
    token = token_from_file()
    session = requests.Session()
    session.headers.update({**HEADERS, "Authorization": f"token {token}"})

    licenses = call(session, "GET", "account/licenses").json()
    exact_by_sa = [item for item in licenses if "BY-SA 4.0" in item.get("name", "").upper()]
    if exact_by_sa:
        raise RuntimeError("Exact CC BY-SA became available; use the reader-file route instead of metadata-only fallback")
    cc0 = [item for item in licenses if int(item.get("value", -1)) == CC0_ID and item.get("name") == "CC0"]
    if len(cc0) != 1:
        raise RuntimeError("Could not prove the metadata-only CC0 license option")

    before_details, before_bytes = project_details(session)
    if before_bytes >= 20_000_000_000:
        raise RuntimeError("Figshare project is already at or above the 20GB cap")
    matches = match_items(before_details)
    if len(matches) > 1:
        raise RuntimeError("Multiple matching Figshare items exist; refusing to create or choose a duplicate")

    action = "updated_existing"
    publish_needed = True
    if matches:
        existing = matches[0]
        article_id = int(existing["id"])
        author_ids = [int(item["id"]) for item in existing.get("authors", [])]
        existing_complete = (
            existing.get("is_public")
            and existing.get("title") == TITLE
            and ZENODO_VERSION in existing.get("description", "")
            and "CC0 hanya berlaku pada catatan metadata Figshare ini" in existing.get("description", "")
            and existing.get("defined_type_name") == "book"
            and existing.get("license", {}).get("value") == CC0_ID
            and author_ids == [AUTHOR_ID]
            and not existing.get("files")
        )
        if existing_complete:
            action = "verified_existing"
            publish_needed = False
        else:
            call(session, "PUT", f"account/articles/{article_id}", json=metadata())
    else:
        response = call(session, "POST", f"account/projects/{PROJECT_ID}/articles", json=metadata())
        payload = response.json() if response.content else {}
        location = payload.get("location") or response.headers.get("Location")
        if payload.get("id"):
            article_id = int(payload["id"])
        elif location:
            article_id = int(str(location).rstrip("/").split("/")[-1])
        else:
            raise RuntimeError("Figshare creation response did not identify the new article")
        action = "created_new"

    if publish_needed:
        call(session, "PUT", f"account/articles/{article_id}/authors", json={"authors": [{"id": AUTHOR_ID}]})
    draft = call(session, "GET", f"account/articles/{article_id}").json()
    if draft.get("files"):
        raise RuntimeError("Refusing to publish an unexpected file-bearing Figshare draft")
    if draft.get("license", {}).get("value") != CC0_ID:
        raise RuntimeError("Figshare draft license mismatch")
    if draft.get("title") != TITLE:
        raise RuntimeError("Figshare draft title mismatch")

    if publish_needed:
        call(session, "POST", f"account/articles/{article_id}/publish")

    public = verify_public(article_id)
    public_project = wait_public_membership(f"projects/{PROJECT_ID}/articles?limit=1000", article_id)
    if article_id not in {int(item["id"]) for item in public_project}:
        raise RuntimeError("Published article missing from public project")

    collection_updated = False
    collection = None
    public_collection: list[dict] = []
    for _ in range(8):
        private_collection = call(
            session, "GET", f"account/collections/{COLLECTION_ID}/articles?limit=1000"
        ).json()
        private_ids = {int(item["id"]) for item in private_collection}
        if article_id not in private_ids:
            call(
                session,
                "POST",
                f"account/collections/{COLLECTION_ID}/articles",
                json={"articles": [article_id]},
            )
        call(session, "POST", f"account/collections/{COLLECTION_ID}/publish")
        collection_updated = True
        for _ in range(15):
            collection = public_get(f"collections/{COLLECTION_ID}")
            payload = public_get(f"collections/{COLLECTION_ID}/articles?limit=1000")
            if not isinstance(payload, list):
                raise RuntimeError("Unexpected public collection article response")
            public_collection = payload
            if article_id in {int(item["id"]) for item in public_collection}:
                break
            time.sleep(2)
        if article_id in {int(item["id"]) for item in public_collection}:
            break
    if article_id not in {int(item["id"]) for item in public_collection}:
        raise RuntimeError("Published article missing from public Indonesian collection after bounded republish attempts")
    assert isinstance(collection, dict)
    collection_version = int(collection["version"])
    version_snapshot = public_get(f"collections/{COLLECTION_ID}/versions/{collection_version}")
    if not isinstance(version_snapshot, dict) or int(version_snapshot.get("version", -1)) != collection_version:
        raise RuntimeError("Could not anonymously read the exact collection version snapshot")

    after_details, after_bytes = project_details(session)
    if after_bytes >= 20_000_000_000:
        raise RuntimeError("Figshare project exceeds the 20GB cap after publication")
    after_matches = match_items(after_details)
    if [int(item["id"]) for item in after_matches] != [article_id]:
        raise RuntimeError("Figshare duplicate check failed after publication")

    receipt = {
        "schema": "ag-bridge-figshare-publication-receipt-v1",
        "status": "PASS",
        "action": action,
        "article": {
            "id": article_id,
            "title": public["title"],
            "doi": public.get("doi"),
            "url": public.get("url_public_html"),
            "version": public.get("version"),
            "defined_type": public.get("defined_type_name"),
            "authors": [{"id": int(item["id"])} for item in public.get("authors", [])],
            "license": public.get("license"),
            "files": [],
            "metadata_only": True,
        },
        "reader_boundary": {
            "through_unit": 7,
            "planned_units": 30,
            "full_edition_complete": False,
            "zenodo_concept_doi": ZENODO_CONCEPT,
            "zenodo_version_doi": ZENODO_VERSION,
        },
        "license_gate": {
            "exact_cc_by_sa_or_mixed_license_available": False,
            "available_license_names": [item.get("name") for item in licenses],
            "edition_bytes_uploaded": False,
            "reason": "The platform license list cannot truthfully represent CC BY-SA 4.0 text plus per-component media rights; CC0 is explicitly limited to this metadata record.",
        },
        "project": {
            "id": PROJECT_ID,
            "url": f"https://figshare.com/projects/Open_and_Share-Alike_Educational_Materials_Translations/{PROJECT_ID}",
            "file_bytes_before": before_bytes,
            "file_bytes_after": after_bytes,
            "cap_bytes": 20_000_000_000,
            "duplicate_matches_after": 1,
        },
        "collection": {
            "id": COLLECTION_ID,
            "requested_doi": COLLECTION_REQUESTED_DOI,
            "current_public_doi": collection.get("doi"),
            "current_public_version": collection.get("version"),
            "version_snapshot_url": f"https://api.figshare.com/v2/collections/{COLLECTION_ID}/versions/{collection_version}",
            "article_membership_verified": True,
            "new_version_published": collection_updated,
        },
        "anonymous_public_readback": {
            "verified_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "credential_used": False,
            "article": True,
            "project_membership": True,
            "collection_membership": True,
            "public_file_count": 0,
        },
        "credential_handling": {
            "credential_value_logged_or_persisted": False,
            "anonymous_readback_used_no_credential": True,
        },
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    del token
    print(json.dumps({
        "status": "PASS",
        "article_id": article_id,
        "doi": public.get("doi"),
        "url": public.get("url_public_html"),
        "collection_doi": collection.get("doi"),
        "metadata_only": True,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
