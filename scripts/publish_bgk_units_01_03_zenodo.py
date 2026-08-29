#!/usr/bin/env python3
"""Publish the BGK Units 01--03 checkpoint in the existing Zenodo concept.

The new version deliberately preserves the eight byte-verified files from the
complete classical volume and adds the reader-first BGK checkpoint.  It never
deletes inherited files.  Credentials are read only for reserve/publish and are
never placed in URLs, receipts, or diagnostic output; public verification is
anonymous and streams every file through SHA-256.
"""

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
RELEASE = ROOT / "release" / "bgk-units-01-03"
TOKEN_FILE = Path.home() / "Documents" / "Obsidian notes" / "New zenodo token.md"
RESERVATION = ROOT / "qa" / "BGK_UNITS_01_03_ZENODO_RESERVATION.json"
PUBLICATION_RECEIPT = ROOT / "qa" / "BGK_UNITS_01_03_ZENODO_PUBLICATION.json"
MIGRATION_RECEIPT = ROOT / "backend" / "bgk-common-backend-v1" / "MIGRATION_RECEIPT.json"
BASE = "https://zenodo.org"
PREVIOUS_RECORD_ID = 22150273
CONCEPT_DOI = "10.5281/zenodo.22059686"
CONCEPT_RECORD_ID = 22059686
TITLE = (
    "Kurva Aljabar (Unit 1–30, lengkap) + Bundel, Berkas, dan Kohomologi "
    "(Unit 1–3, parsial) — Edisi Bahasa Indonesia"
)
VERSION = "ak-unit-30+bgk-unit-03"
MODEL_ID = "OpenAI Codex gpt-5.6-sol, Ultra"
MODEL_PROVENANCE = MODEL_ID + "."
ORGANIZATION_HUB = "https://github.com/KokunoYumeto/program-matematika-indonesia"
PRIOR_RECEIPT = ROOT / "qa" / "UNIT_30_ZENODO_PUBLICATION.json"
PRIOR_RECEIPT_SHA256 = "dcd2c4574081a4462627b5775480b27de4d5959e76442bc7d409979480e4bcea"

BGK_FILES = [
    "01_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-03.pdf",
    "02_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-03.html",
    "03_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-03_source.zip",
    "04_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-03_native-backend.zip",
    "05_LICENSE_AND_COMPONENT_RIGHTS.md",
    "06_README.md",
    "07_RELEASE_MANIFEST.json",
    "08_SHA256SUMS.txt",
    "09_RELEASE_CANDIDATE_QA.json",
]
MIGRATION_PUBLIC_NAME = "10_BGK_MIGRATION_RECEIPT.json"


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_write(path: Path, value: dict) -> None:
    data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(data)
    temporary.replace(path)
    if path.read_bytes() != data:
        raise RuntimeError(f"Post-write verification failed: {path}")


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"Expected a JSON object: {path}")
    return value


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


def request(session: requests.Session, method: str, url: str, **kwargs) -> requests.Response:
    response = session.request(method, url, timeout=240, **kwargs)
    if not response.ok:
        raise RuntimeError(
            f"Zenodo {method} {url} failed with HTTP {response.status_code}: "
            f"{response.text[:800]}"
        )
    return response


def file_fact(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    return {"bytes": path.stat().st_size, "sha256": sha256_path(path)}


def prior_file_facts() -> dict[str, dict]:
    if sha256_path(PRIOR_RECEIPT) != PRIOR_RECEIPT_SHA256:
        raise RuntimeError("Accepted Unit 30 Zenodo receipt is absent or has drifted")
    receipt = load_json(PRIOR_RECEIPT)
    record = receipt.get("record") or {}
    if (
        int(record.get("id", 0)) != PREVIOUS_RECORD_ID
        or record.get("concept_doi") != CONCEPT_DOI
        or record.get("version") != "unit-30"
    ):
        raise RuntimeError("Accepted predecessor receipt has the wrong public identity")
    rows = ((receipt.get("anonymous_public_byte_readback") or {}).get("files") or [])
    facts = {
        row["name"]: {"bytes": int(row["bytes"]), "sha256": row["sha256"]}
        for row in rows
        if row.get("public_readback") is True
    }
    if len(facts) != 8:
        raise RuntimeError("Accepted predecessor receipt does not bind exactly eight files")
    return facts


def bgk_file_facts(include_migration: bool) -> dict[str, dict]:
    facts = {name: file_fact(RELEASE / name) for name in BGK_FILES}
    manifest = load_json(RELEASE / "07_RELEASE_MANIFEST.json")
    qa = load_json(RELEASE / "09_RELEASE_CANDIDATE_QA.json")
    if (
        manifest.get("status") != "partial_coherent_checkpoint"
        or manifest.get("included_units") != [1, 2, 3]
        or manifest.get("remaining_unit_count") != 27
        or qa.get("status") != "PASS"
    ):
        raise RuntimeError("BGK release contract is not the verified Units 01--03 boundary")
    if include_migration:
        receipt = load_json(MIGRATION_RECEIPT)
        if receipt.get("schema_name") != "interlanguage-math-modular-backend-migration-receipt":
            raise RuntimeError("BGK migration receipt has the wrong schema identity")
        facts[MIGRATION_PUBLIC_NAME] = file_fact(MIGRATION_RECEIPT)
    return facts


def metadata() -> dict:
    payload = {
        "title": TITLE,
        "upload_type": "publication",
        "publication_type": "book",
        "description": (
            "<p><strong>Edisi Bahasa Indonesia (id-ID) dari dua kursus Holger Brenner.</strong> "
            "Volume <em>Kurva Aljabar</em> tetap lengkap pada 30 unit (504 halaman PDF, "
            "693 soal, dan seluruh 122 solusi publik yang dibekukan). Versi ini menambahkan "
            "checkpoint koheren tiga kuliah dan tiga lembar kerja (Unit 1–3) dari "
            "<em>Bundel, Berkas, dan Kohomologi</em>: 50 halaman PDF A4, HTML mandiri "
            "dengan MathML dan reflow seluler, 62 soal, dan kedua solusi publik yang "
            "tersedia pada revisi sumber. Enam puluh solusi lain memang tidak tersedia "
            "dalam sumber dan tidak diciptakan. Dua puluh tujuh unit kursus kedua masih "
            "tersisa; status parsial tersebut dinyatakan secara eksplisit.</p>"
            "<p>Berkas lengkap volume klasik dari versi sebelumnya dipertahankan tanpa "
            "pengurangan akses. Tambahan BGK bersifat reader-first dan memuat PDF, HTML, "
            "sumber yang dapat dilanjutkan, backend asli 2.370 rekaman, adapter backend umum "
            "tervalidasi, lisensi/hak komponen, manifest, checksum, dan bukti QA. Teks kursus "
            "dan terjemahannya berada di bawah CC BY-SA 4.0; media mempertahankan atribusi "
            "dan lisensi komponennya masing-masing. Edisi independen ini disiapkan atas "
            f"arahan pengguna dengan {MODEL_PROVENANCE} Ini bukan terbitan resmi Holger "
            "Brenner, Universitas Osnabrück, Wikiversity, Wikimedia Foundation, atau OpenAI, "
            "dan tidak menyiratkan dukungan mereka.</p>"
            "<p><strong>English identification:</strong> Indonesian edition of Holger "
            "Brenner's two-course algebraic-geometry sequence. The complete 30-unit "
            "<em>Algebraische Kurven</em> volume is preserved unchanged; this version adds "
            "a coherent partial checkpoint through Units 1–3 of <em>Bündel, Garben und "
            "Kohomologie</em>. Course text and translation are CC BY-SA 4.0, with "
            "component-specific media rights retained. Independent, non-endorsed derivative.</p>"
        ),
        "creators": [{"name": "Brenner, Holger"}],
        "contributors": [
            {"name": "TTP", "type": "Other", "affiliation": ORGANIZATION_HUB},
            {"name": MODEL_ID, "type": "Other"},
        ],
        "access_right": "open",
        "license": "other-open",
        "keywords": [
            "geometri aljabar",
            "algebraic geometry",
            "Bahasa Indonesia",
            "id-ID",
            "kurva aljabar",
            "berkas",
            "kohomologi",
            "open textbook",
        ],
        "language": "ind",
        "version": VERSION,
        "related_identifiers": [
            {
                "identifier": "https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)",
                "relation": "isDerivedFrom",
                "resource_type": "publication-book",
            },
            {
                "identifier": "https://de.wikiversity.org/w/index.php?oldid=1052895",
                "relation": "isDerivedFrom",
                "resource_type": "publication-book",
            },
        ],
    }
    serialized = json.dumps(payload, ensure_ascii=False)
    if serialized.count("TTP") != 1:
        raise RuntimeError("Organization label must occur exactly once in Zenodo metadata")
    if TITLE.startswith("TTP") or payload["description"].lstrip().startswith("TTP"):
        raise RuntimeError("Organization label may not prefix title or description")
    if MODEL_PROVENANCE not in payload["description"]:
        raise RuntimeError("Exact model provenance is missing from Zenodo metadata")
    return payload


def public_latest() -> dict:
    response = requests.get(
        f"{BASE}/api/records/{PREVIOUS_RECORD_ID}/versions/latest", timeout=180
    )
    response.raise_for_status()
    return response.json()


def stream_public_files(record: dict, expected: dict[str, dict]) -> list[dict]:
    public = {row["key"]: row for row in record.get("files", [])}
    if set(public) != set(expected):
        raise RuntimeError(
            f"Public Zenodo inventory mismatch: expected {sorted(expected)}, got {sorted(public)}"
        )
    verified: list[dict] = []
    for name in expected:
        response = requests.get(public[name]["links"]["self"], stream=True, timeout=240)
        response.raise_for_status()
        digest = hashlib.sha256()
        size = 0
        for chunk in response.iter_content(1024 * 1024):
            if chunk:
                size += len(chunk)
                digest.update(chunk)
        actual = {"bytes": size, "sha256": digest.hexdigest()}
        if actual != expected[name]:
            raise RuntimeError(f"Anonymous public-byte mismatch for {name}: {actual}")
        verified.append(
            {"name": name, **actual, "public_readback": True, "credential_used": False}
        )
    return verified


def verify_public(record_id: int, expected: dict[str, dict]) -> tuple[dict, list[dict]]:
    record = None
    for _ in range(60):
        response = requests.get(f"{BASE}/api/records/{record_id}", timeout=180)
        if response.ok:
            candidate = response.json()
            if {row.get("key") for row in candidate.get("files", [])} == set(expected):
                record = candidate
                break
        time.sleep(2)
    if record is None:
        raise RuntimeError("Published Zenodo version did not expose the expected public inventory")
    return record, stream_public_files(record, expected)


def validate_latest_predecessor(latest: dict) -> str:
    if latest.get("conceptdoi") != CONCEPT_DOI:
        raise RuntimeError("Zenodo concept DOI mismatch")
    version = (latest.get("metadata") or {}).get("version")
    if version == VERSION:
        return "target_public"
    if int(latest.get("id", 0)) != PREVIOUS_RECORD_ID or version != "unit-30":
        raise RuntimeError("An unreviewed Zenodo version became latest; refusing to branch")
    return "predecessor_public"


def reservation_descriptor(draft: dict, state: str) -> dict:
    reserved = (draft.get("metadata") or {}).get("prereserve_doi") or {}
    doi = reserved.get("doi") or (draft.get("metadata") or {}).get("doi")
    if not doi:
        raise RuntimeError("Zenodo draft exposes no reserved DOI")
    return {
        "schema": "ag-bridge-bgk-zenodo-reservation-v1",
        "status": "PASS",
        "state": state,
        "record_id": int(draft["id"]),
        "record_url": f"{BASE}/records/{int(draft['id'])}",
        "doi": doi,
        "concept_doi": CONCEPT_DOI,
        "previous_record_id": PREVIOUS_RECORD_ID,
        "title": TITLE,
        "version": VERSION,
        "inherited_files_preserved": sorted(prior_file_facts()),
        "bgk_files_planned": BGK_FILES + [MIGRATION_PUBLIC_NAME],
        "credentials_recorded": False,
    }


def preflight() -> dict:
    old = prior_file_facts()
    new = bgk_file_facts(include_migration=False)
    latest = public_latest()
    state = validate_latest_predecessor(latest)
    if state == "predecessor_public":
        public_old = stream_public_files(latest, old)
        old_verified = len(public_old)
    else:
        old_verified = len(old)
    metadata_value = metadata()
    return {
        "status": "PASS",
        "mode": "anonymous_predecessor_and_local_release_preflight",
        "credential_read": False,
        "current_latest_record": int(latest["id"]),
        "current_latest_version": (latest.get("metadata") or {}).get("version"),
        "concept_doi": latest.get("conceptdoi"),
        "target_version": VERSION,
        "title": metadata_value["title"],
        "license": metadata_value["license"],
        "inherited_files_verified": old_verified,
        "new_files_verified": len(new),
        "new_bytes": sum(row["bytes"] for row in new.values()),
        "final_migration_receipt": "generated_after_reserved_public_identity",
        "metadata_organization_occurrences": json.dumps(metadata_value, ensure_ascii=False).count("TTP"),
    }


def authenticated_session() -> tuple[requests.Session, str]:
    token = token_from_file()
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session, token


def reserve() -> dict:
    bgk_file_facts(include_migration=False)
    latest = public_latest()
    if validate_latest_predecessor(latest) == "target_public":
        descriptor = reservation_descriptor(latest, "already_public")
        canonical_write(RESERVATION, descriptor)
        return descriptor

    session, token = authenticated_session()
    draft = None
    if RESERVATION.is_file():
        prior = load_json(RESERVATION)
        if (
            prior.get("concept_doi") == CONCEPT_DOI
            and prior.get("version") == VERSION
            and int(prior.get("record_id", 0))
        ):
            response = session.get(
                f"{BASE}/api/deposit/depositions/{int(prior['record_id'])}", timeout=180
            )
            if response.ok and not response.json().get("submitted"):
                draft = response.json()

    if draft is None:
        drafts = request(
            session,
            "GET",
            f"{BASE}/api/deposit/depositions",
            params={"status": "draft", "sort": "mostrecent", "size": 100},
        ).json()
        candidates = [
            item
            for item in drafts
            if not item.get("submitted")
            and int(item.get("conceptrecid") or 0) == CONCEPT_RECORD_ID
        ]
        if len(candidates) > 1:
            raise RuntimeError("Multiple unsubmitted drafts exist in the target Zenodo concept")
        if candidates:
            draft = candidates[0]
        else:
            response = request(
                session,
                "POST",
                f"{BASE}/api/deposit/depositions/{PREVIOUS_RECORD_ID}/actions/newversion",
            ).json()
            draft_url = (response.get("links") or {}).get("latest_draft")
            if not draft_url:
                raise RuntimeError("Zenodo new-version response has no latest_draft link")
            draft = request(session, "GET", draft_url).json()

    inherited_names = {
        item.get("filename") or item.get("key") for item in draft.get("files", [])
    }
    if inherited_names != set(prior_file_facts()):
        raise RuntimeError(
            f"Zenodo draft did not preserve the eight inherited files: {sorted(inherited_names)}"
        )
    draft = request(
        session, "PUT", draft["links"]["self"], json={"metadata": metadata()}
    ).json()
    if draft.get("submitted"):
        raise RuntimeError("Reserved Zenodo draft unexpectedly reports submitted=true")
    descriptor = reservation_descriptor(draft, "reserved_draft")
    canonical_write(RESERVATION, descriptor)
    del token
    session.close()
    return descriptor


def write_publication_receipt(record: dict, verified: list[dict]) -> None:
    metadata_value = record.get("metadata") or {}
    contributors = metadata_value.get("contributors") or []
    receipt = {
        "schema": "ag-bridge-bgk-zenodo-publication-receipt-v1",
        "status": "PASS",
        "record": {
            "id": int(record["id"]),
            "url": record["links"]["self_html"],
            "api_url": record["links"]["self"],
            "doi": metadata_value["doi"],
            "concept_doi": record["conceptdoi"],
            "previous_record_id": PREVIOUS_RECORD_ID,
            "title": metadata_value["title"],
            "version": metadata_value["version"],
            "publication_date": metadata_value["publication_date"],
            "published_timestamp": record.get("created"),
        },
        "coverage": {
            "classical_units_complete": 30,
            "bgk_units_complete": 3,
            "bgk_units_total": 30,
            "bgk_units_remaining": 27,
            "classical_files_preserved": 8,
            "bgk_files_added": 10,
        },
        "metadata_cleanliness": {
            "creator": "Brenner, Holger",
            "organization_contributor_count": sum(
                item.get("name") == "TTP" for item in contributors
            ),
            "organization_hub": ORGANIZATION_HUB,
            "model_contributor_count": sum(
                item.get("name") == MODEL_ID for item in contributors
            ),
            "exact_model_provenance": MODEL_PROVENANCE,
            "license_field": "other-open",
            "translated_course_text_license": "CC BY-SA 4.0",
            "non_endorsement_disclosed": True,
        },
        "anonymous_public_byte_readback": {
            "verified_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "credential_used": False,
            "files_expected": 18,
            "files_verified": len(verified),
            "all_size_and_sha256_matches": True,
            "files": verified,
        },
        "credential_handling": {
            "credential_value_logged_or_persisted": False,
            "credential_file_path_recorded": False,
            "public_readback_used_anonymous_requests": True,
        },
    }
    canonical_write(PUBLICATION_RECEIPT, receipt)


def publish() -> dict:
    old = prior_file_facts()
    new = bgk_file_facts(include_migration=True)
    expected = {**old, **new}
    if len(expected) != 18:
        raise RuntimeError("Final Zenodo inventory must contain 18 collision-free files")
    latest = public_latest()
    if validate_latest_predecessor(latest) == "target_public":
        record, verified = verify_public(int(latest["id"]), expected)
        write_publication_receipt(record, verified)
        return {
            "status": "PASS",
            "action": "verified_existing_bgk_units_01_03",
            "record_id": int(record["id"]),
            "files_verified": len(verified),
        }
    if not RESERVATION.is_file():
        raise RuntimeError("Zenodo reservation receipt is missing; run --reserve first")
    reservation = load_json(RESERVATION)
    if (
        reservation.get("concept_doi") != CONCEPT_DOI
        or reservation.get("version") != VERSION
        or reservation.get("previous_record_id") != PREVIOUS_RECORD_ID
    ):
        raise RuntimeError("Zenodo reservation identity mismatch")

    session, token = authenticated_session()
    draft_id = int(reservation["record_id"])
    draft = request(
        session, "GET", f"{BASE}/api/deposit/depositions/{draft_id}"
    ).json()
    if draft.get("submitted"):
        raise RuntimeError("Reserved Zenodo draft is already submitted but not public latest")
    draft_names = {
        item.get("filename") or item.get("key") for item in draft.get("files", [])
    }
    unexpected = draft_names - set(expected)
    missing_inherited = set(old) - draft_names
    if unexpected or missing_inherited:
        raise RuntimeError(
            f"Zenodo draft inventory is unsafe: unexpected={sorted(unexpected)}, "
            f"missing_inherited={sorted(missing_inherited)}"
        )
    # A retry may have uploaded part of the BGK set.  Delete only those exact
    # unsubmitted additions, never the inherited public-volume files.
    for item in list(draft.get("files", [])):
        name = item.get("filename") or item.get("key")
        if name in new:
            request(
                session,
                "DELETE",
                f"{BASE}/api/deposit/depositions/{draft_id}/files/{item['id']}",
            )
    draft = request(
        session, "PUT", draft["links"]["self"], json={"metadata": metadata()}
    ).json()
    bucket = draft["links"]["bucket"].rstrip("/")
    local_paths = {name: RELEASE / name for name in BGK_FILES}
    local_paths[MIGRATION_PUBLIC_NAME] = MIGRATION_RECEIPT
    for name in new:
        with local_paths[name].open("rb") as stream:
            request(session, "PUT", f"{bucket}/{quote(name, safe='')}", data=stream)

    refreshed = request(session, "GET", draft["links"]["self"]).json()
    refreshed_names = {
        item.get("filename") or item.get("key") for item in refreshed.get("files", [])
    }
    if refreshed_names != set(expected):
        raise RuntimeError(f"Zenodo pre-publication inventory mismatch: {sorted(refreshed_names)}")
    published = request(session, "POST", refreshed["links"]["publish"]).json()
    record_id = int(published.get("record_id") or published.get("id"))
    del token
    session.close()

    record, verified = verify_public(record_id, expected)
    public_metadata = record.get("metadata") or {}
    if (
        record.get("conceptdoi") != CONCEPT_DOI
        or public_metadata.get("version") != VERSION
        or public_metadata.get("title") != TITLE
    ):
        raise RuntimeError("Published Zenodo metadata identity mismatch")
    write_publication_receipt(record, verified)
    return {
        "status": "PASS",
        "action": "published_new_version",
        "record_id": record_id,
        "doi": public_metadata["doi"],
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
