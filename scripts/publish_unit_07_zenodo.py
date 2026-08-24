#!/usr/bin/env python3
"""Reserve/publish Unit 7 in the existing Zenodo concept and verify public bytes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "release" / "unit-07"
TOKEN_FILE = Path.home() / "Documents" / "Obsidian notes" / "New zenodo token.md"
RESERVATION = ROOT / "qa" / "UNIT_07_ZENODO_RESERVATION.json"
RECEIPT = ROOT / "qa" / "UNIT_07_ZENODO_PUBLICATION.json"
BASE = "https://zenodo.org"
PREVIOUS_RECORD_ID = 22060388
CONCEPT_DOI = "10.5281/zenodo.22059686"
TITLE = "Kurva Aljabar — Edisi Bahasa Indonesia"
VERSION = "unit-07"
FILES = [
    "kurva-aljabar-id-unit-07.pdf",
    "kurva-aljabar-id-unit-07.html",
    "kurva-aljabar-id-unit-07-source.zip",
    "kurva-aljabar-id-unit-07-authority-witnesses.zip",
    "BUILD_RECEIPT-unit-07.json",
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
        raise RuntimeError("No Zenodo token candidate found in the designated credential file")
    return max(candidates, key=len)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def expected_files() -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for name in FILES:
        path = RELEASE / name
        if not path.is_file():
            raise FileNotFoundError(path)
        result[name] = {"bytes": path.stat().st_size, "sha256": sha256(path)}
    return result


def request(session: requests.Session, method: str, url: str, **kwargs) -> requests.Response:
    response = session.request(method, url, timeout=180, **kwargs)
    if not response.ok:
        body = response.text[:1000]
        raise RuntimeError(f"Zenodo {method} {url} failed with HTTP {response.status_code}: {body}")
    return response


def metadata() -> dict:
    return {
        "title": TITLE,
        "upload_type": "publication",
        "publication_type": "book",
        "description": (
            "<p><strong>Rilis kumulatif kerja Bahasa Indonesia (id-ID), Unit 1–7</strong>, "
            "dari <em>Algebraische Kurven (Osnabrück 2025–2026)</em> karya Holger Brenner. "
            "Batas ini memuat tujuh kuliah, tujuh lembar kerja dengan 197 soal, dan seluruh "
            "40 solusi publik yang tersedia pada revisi sumber yang dibekukan. Ini belum "
            "merupakan edisi 30-unit yang lengkap; penerjemahan berlanjut dalam urutan sumber.</p>"
            "<p>Paket preservasi memuat pembaca PDF A4 142 halaman, pembaca HTML mandiri "
            "dengan MathML dan reflow seluler, snapshot sumber/backend 5.182 rekaman yang dapat dilanjutkan, "
            "manifest, build receipt, saksi otoritas, hak komponen, dan bukti QA. Terjemahan "
            "dan penataan ulang teks kursus berada di bawah CC BY-SA 4.0; setiap media pihak "
            "ketiga mempertahankan pencipta, sumber, dan lisensi komponennya sendiri. Edisi "
            "independen ini disiapkan atas arahan pengguna dengan OpenAI Codex gpt-5.6-sol, Ultra. "
            "Ini bukan terbitan "
            "resmi Holger Brenner, Universitas Osnabrück, Wikiversity, atau Wikimedia Foundation, "
            "dan tidak menyiratkan dukungan mereka.</p>"
            "<p><strong>English identification:</strong> Cumulative working Indonesian (id-ID) "
            "edition, Units 1–7, of Holger Brenner's <em>Algebraische Kurven (Osnabrück "
            "2025–2026)</em>, with self-contained HTML, A4 PDF, editable source/backend snapshot, "
            "component-rights records, authority witnesses, and QA evidence. This is an "
            "independent, non-endorsed derivative and not yet the complete 30-unit edition.</p>"
        ),
        "creators": [{"name": "Brenner, Holger"}],
        "contributors": [
            {"name": "TTP", "type": "Other"},
            {"name": "OpenAI Codex gpt-5.6-sol, Ultra", "type": "Other"},
        ],
        "access_right": "open",
        "license": "other-open",
        "keywords": [
            "geometri aljabar",
            "algebraic geometry",
            "Bahasa Indonesia",
            "id-ID",
            "kurva aljabar",
            "open textbook",
        ],
        "language": "ind",
        "version": VERSION,
        "related_identifiers": [
            {
                "identifier": "https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)",
                "relation": "isDerivedFrom",
                "resource_type": "publication-book",
            }
        ],
    }


def public_latest() -> dict:
    response = requests.get(f"{BASE}/api/records/{PREVIOUS_RECORD_ID}/versions/latest", timeout=120)
    response.raise_for_status()
    return response.json()


def verify_public(record_id: int, expected: dict[str, dict[str, object]]) -> tuple[dict, list[dict]]:
    record = None
    for _ in range(60):
        response = requests.get(f"{BASE}/api/records/{record_id}", timeout=120)
        if response.ok:
            candidate = response.json()
            names = {item.get("key") for item in candidate.get("files", [])}
            if names == set(expected):
                record = candidate
                break
        time.sleep(2)
    if record is None:
        raise RuntimeError("Published Zenodo record did not become anonymously readable with the expected inventory")

    public_files = {item["key"]: item for item in record["files"]}
    verified: list[dict] = []
    for name in FILES:
        item = public_files[name]
        digest = hashlib.sha256()
        size = 0
        response = requests.get(item["links"]["self"], stream=True, timeout=180)
        response.raise_for_status()
        for chunk in response.iter_content(1024 * 1024):
            if chunk:
                size += len(chunk)
                digest.update(chunk)
        wanted = expected[name]
        if size != wanted["bytes"] or digest.hexdigest() != wanted["sha256"]:
            raise RuntimeError(f"Anonymous readback mismatch for {name}")
        verified.append(
            {"name": name, "bytes": size, "sha256": digest.hexdigest(), "public_readback": True}
        )
    return record, verified


def write_receipt(record: dict, verified: list[dict]) -> None:
    public_metadata = record["metadata"]
    contributors = public_metadata.get("contributors", [])
    receipt = {
        "schema": "ag-bridge-zenodo-publication-receipt-v1",
        "status": "PASS",
        "record": {
            "id": int(record["id"]),
            "url": record["links"]["self_html"],
            "api_url": record["links"]["self"],
            "doi": public_metadata["doi"],
            "concept_doi": record["conceptdoi"],
            "title": public_metadata["title"],
            "version": public_metadata["version"],
            "publication_date": public_metadata["publication_date"],
            "published_timestamp": record.get("created"),
            "zenodo_state": "done",
            "zenodo_status": "published",
        },
        "reader_boundary": {
            "through_unit": 7,
            "planned_units": 30,
            "full_edition_complete": False,
            "incomplete_boundary_disclosed_in_description": True,
        },
        "metadata_cleanliness": {
            "creator": "Brenner, Holger",
            "organization_contributor_count": sum(item.get("name") == "TTP" for item in contributors),
            "ai_contributor_count": sum(item.get("name", "").startswith("OpenAI Codex") for item in contributors),
            "work_title_preserved_without_organization_prefix": not public_metadata["title"].startswith("TTP"),
            "description_lead_preserved_without_organization_prefix": not public_metadata["description"].lstrip().startswith("TTP"),
            "non_endorsement_disclosed": True,
            "license_field": public_metadata["license"]["id"],
            "license_field_rationale": "Avoids applying a false blanket licence to the mixed-rights file set.",
            "translated_course_text_license": "CC BY-SA 4.0",
            "third_party_media_license_policy": "Per-component rights and attribution are preserved in the source package.",
        },
        "anonymous_public_byte_readback": {
            "verified_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "credential_used": False,
            "files_expected": len(FILES),
            "files_verified": len(verified),
            "all_size_and_sha256_matches": True,
            "files": verified,
        },
        "credential_handling": {
            "public_readback_used_anonymous_requests": True,
            "credential_value_logged_or_persisted": False,
        },
        "github": {
            "state": "publication_deferred_due_to_user_confirmed_account_suspension",
            "retry_attempted_after_suspension_notice": False,
            "support_ticket_filed_by_user": True,
        },
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def preflight() -> dict:
    expected = expected_files()
    current = public_latest()
    return {
        "status": "PASS",
        "current_latest_record": int(current["id"]),
        "current_latest_version": current["metadata"].get("version"),
        "concept_doi": current.get("conceptdoi"),
        "target_version": VERSION,
        "target_files": [{"name": name, **expected[name]} for name in FILES],
    }


def reservation_descriptor(draft: dict, state: str) -> dict:
    draft_id = int(draft["id"])
    reserved = (draft.get("metadata") or {}).get("prereserve_doi") or {}
    doi = reserved.get("doi") or (draft.get("metadata") or {}).get("doi")
    if not doi:
        raise RuntimeError("Zenodo draft does not expose a reserved DOI")
    return {
        "schema": "ag-bridge-zenodo-reservation-v1",
        "status": "PASS",
        "state": state,
        "record_id": draft_id,
        "record_url": f"{BASE}/records/{draft_id}",
        "doi": doi,
        "concept_doi": CONCEPT_DOI,
        "version": VERSION,
        "title": TITLE,
        "credentials_recorded": False,
    }


def reserve() -> dict:
    latest = public_latest()
    if latest.get("conceptdoi") != CONCEPT_DOI:
        raise RuntimeError("Zenodo concept DOI mismatch")
    if latest["metadata"].get("version") == VERSION:
        descriptor = reservation_descriptor(latest, "already_public")
        RESERVATION.write_text(json.dumps(descriptor, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return descriptor

    token = token_from_file()
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})

    draft = None
    if RESERVATION.is_file():
        prior = json.loads(RESERVATION.read_text(encoding="utf-8"))
        prior_id = int(prior.get("record_id", 0))
        if prior_id:
            response = session.get(f"{BASE}/api/deposit/depositions/{prior_id}", timeout=180)
            if response.ok:
                candidate = response.json()
                if not candidate.get("submitted") and (candidate.get("metadata") or {}).get("version") == VERSION:
                    draft = candidate

    if draft is None:
        response = request(
            session,
            "POST",
            f"{BASE}/api/deposit/depositions/{int(latest['id'])}/actions/newversion",
        )
        original = response.json()
        draft_url = original.get("links", {}).get("latest_draft")
        if not draft_url:
            raise RuntimeError("Zenodo new-version response did not expose latest_draft")
        draft = request(session, "GET", draft_url).json()

    draft_id = int(draft["id"])
    for item in list(draft.get("files", [])):
        request(session, "DELETE", f"{BASE}/api/deposit/depositions/{draft_id}/files/{item['id']}")
    draft = request(session, "PUT", draft["links"]["self"], json={"metadata": metadata()}).json()
    if draft.get("submitted"):
        raise RuntimeError("Reserved Zenodo boundary unexpectedly reports submitted=true")
    descriptor = reservation_descriptor(draft, "reserved_draft")
    RESERVATION.write_text(json.dumps(descriptor, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    del token
    return descriptor


def publish() -> dict:
    expected = expected_files()
    latest = public_latest()
    if latest.get("conceptdoi") != CONCEPT_DOI:
        raise RuntimeError("Zenodo concept DOI mismatch")
    if latest["metadata"].get("version") == VERSION:
        record, verified = verify_public(int(latest["id"]), expected)
        write_receipt(record, verified)
        return {"status": "PASS", "action": "verified_existing_unit_07", "record_id": int(record["id"])}

    token = token_from_file()
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})

    if not RESERVATION.is_file():
        raise RuntimeError("Unit 7 Zenodo reservation receipt is missing; run --reserve first")
    reservation = json.loads(RESERVATION.read_text(encoding="utf-8"))
    if reservation.get("concept_doi") != CONCEPT_DOI or reservation.get("version") != VERSION:
        raise RuntimeError("Zenodo reservation identity mismatch")
    draft_id = int(reservation["record_id"])
    draft = request(session, "GET", f"{BASE}/api/deposit/depositions/{draft_id}").json()
    if draft.get("submitted"):
        raise RuntimeError("Reserved Zenodo deposition is already submitted but not visible as latest")
    if (draft.get("metadata") or {}).get("version") != VERSION:
        raise RuntimeError("Reserved Zenodo draft version mismatch")

    for item in list(draft.get("files", [])):
        request(session, "DELETE", f"{BASE}/api/deposit/depositions/{draft_id}/files/{item['id']}")

    draft = request(session, "PUT", draft["links"]["self"], json={"metadata": metadata()}).json()
    bucket = draft["links"]["bucket"].rstrip("/")
    for name in FILES:
        path = RELEASE / name
        with path.open("rb") as stream:
            request(session, "PUT", f"{bucket}/{quote(name, safe='')}", data=stream)

    refreshed = request(session, "GET", draft["links"]["self"]).json()
    names = [item.get("filename") for item in refreshed.get("files", [])]
    if names != FILES:
        if set(names) != set(FILES):
            raise RuntimeError(f"Zenodo draft inventory mismatch: {names}")
    published = request(session, "POST", refreshed["links"]["publish"]).json()
    record_id = int(published.get("record_id") or published.get("id"))
    del token

    record, verified = verify_public(record_id, expected)
    if record.get("conceptdoi") != CONCEPT_DOI:
        raise RuntimeError("Published Zenodo concept DOI changed unexpectedly")
    if record["metadata"].get("version") != VERSION or record["metadata"].get("title") != TITLE:
        raise RuntimeError("Published Zenodo metadata mismatch")
    write_receipt(record, verified)
    return {
        "status": "PASS",
        "action": "published_new_version",
        "record_id": record_id,
        "doi": record["metadata"]["doi"],
        "files_verified": len(verified),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--reserve", action="store_true")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    if sum((args.preflight, args.reserve, args.publish)) != 1:
        raise SystemExit("Choose exactly one of --preflight, --reserve, or --publish")
    result = preflight() if args.preflight else reserve() if args.reserve else publish()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
