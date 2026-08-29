#!/usr/bin/env python3
"""Publish BGK Units 01--06 as a new version of the existing Zenodo concept.

The script cannot create a new concept.  It accepts only the verified public
BGK Units 01--03 record as predecessor, preserves the eight complete-classical
files byte-for-byte, and replaces only the superseded BGK checkpoint files in
the *new unsubmitted draft*.  The immutable Units 01--03 public record remains
public and untouched.  Publication is complete only after anonymous streaming
readback of every final file matches local/predecessor bytes and SHA-256.

``--local-preflight`` performs no network, Git, credential, or public mutation.
Credentials are read only during ``--reserve`` or ``--publish`` and are never
placed in a URL, receipt, or diagnostic result.
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
RELEASE = ROOT / "release" / "bgk-units-01-06"
TOKEN_FILE = Path.home() / "Documents" / "Obsidian notes" / "New zenodo token.md"
RESERVATION = ROOT / "qa" / "BGK_UNITS_01_06_ZENODO_RESERVATION.json"
PUBLICATION_RECEIPT = ROOT / "qa" / "BGK_UNITS_01_06_ZENODO_PUBLICATION.json"
MIGRATION_RECEIPT = ROOT / "backend" / "bgk-common-backend-v1" / "MIGRATION_RECEIPT.json"
BASE = "https://zenodo.org"

PREVIOUS_RECORD_ID = 22160883
PREVIOUS_VERSION = "ak-unit-30+bgk-unit-03"
PREVIOUS_RECEIPT = ROOT / "qa" / "BGK_UNITS_01_03_ZENODO_PUBLICATION.json"
PREVIOUS_RECEIPT_SHA256 = "bdba910e1fda2c3f02d32d1addebf98facc5b36d8e09a6fac17e028c7bc8ca2a"
CLASSICAL_RECEIPT = ROOT / "qa" / "UNIT_30_ZENODO_PUBLICATION.json"
CLASSICAL_RECEIPT_SHA256 = "dcd2c4574081a4462627b5775480b27de4d5959e76442bc7d409979480e4bcea"
CONCEPT_DOI = "10.5281/zenodo.22059686"
CONCEPT_RECORD_ID = 22059686

TITLE = (
    "Kurva Aljabar (Unit 1–30, lengkap) + Bundel, Berkas, dan Kohomologi "
    "(Unit 1–6, parsial) — Edisi Bahasa Indonesia"
)
VERSION = "ak-unit-30+bgk-unit-06"
MODEL_ID = "OpenAI Codex gpt-5.6-sol, Ultra"
MODEL_PROVENANCE = MODEL_ID + "."
ORGANIZATION_HUB = "https://github.com/KokunoYumeto/program-matematika-indonesia"

BGK_FILES = (
    "01_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-06.pdf",
    "02_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-06.html",
    "03_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-06_source.zip",
    "04_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-06_native-backend.zip",
    "05_LICENSE_AND_COMPONENT_RIGHTS.md",
    "06_README.md",
    "07_RELEASE_MANIFEST.json",
    "08_SHA256SUMS.txt",
    "09_RELEASE_CANDIDATE_QA.json",
)
MIGRATION_PUBLIC_NAME = "10_BGK_MIGRATION_RECEIPT.json"
OLD_BGK_FILES = {
    "01_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-03.pdf",
    "02_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-03.html",
    "03_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-03_source.zip",
    "04_Bundel-Berkas-dan-Kohomologi_id-ID_Units-01-03_native-backend.zip",
    "05_LICENSE_AND_COMPONENT_RIGHTS.md",
    "06_README.md",
    "07_RELEASE_MANIFEST.json",
    "08_SHA256SUMS.txt",
    "09_RELEASE_CANDIDATE_QA.json",
    "10_BGK_MIGRATION_RECEIPT.json",
}


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_fact(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise RuntimeError(f"Required local file missing: {path}")
    return {"bytes": path.stat().st_size, "sha256": sha256_path(path)}


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"Invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"Expected JSON object: {path}")
    return value


def canonical_write(path: Path, value: dict) -> None:
    data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(data)
    temporary.replace(path)
    if path.read_bytes() != data:
        raise RuntimeError(f"Post-write verification failed: {path}")


def receipt_facts(path: Path, expected_hash: str, expected_count: int) -> tuple[dict, dict[str, dict]]:
    if sha256_path(path) != expected_hash:
        raise RuntimeError(f"Accepted predecessor receipt is absent or drifted: {path.name}")
    receipt = load_json(path)
    rows = ((receipt.get("anonymous_public_byte_readback") or {}).get("files") or [])
    facts = {
        row["name"]: {"bytes": int(row["bytes"]), "sha256": row["sha256"]}
        for row in rows
        if row.get("public_readback") is True
    }
    if len(facts) != expected_count:
        raise RuntimeError(f"Accepted receipt does not bind exactly {expected_count} files: {path.name}")
    return receipt, facts


def predecessor_facts() -> tuple[dict[str, dict], dict[str, dict]]:
    classical_receipt, classical = receipt_facts(CLASSICAL_RECEIPT, CLASSICAL_RECEIPT_SHA256, 8)
    previous_receipt, previous = receipt_facts(PREVIOUS_RECEIPT, PREVIOUS_RECEIPT_SHA256, 18)
    previous_record = previous_receipt.get("record") or {}
    if (
        int(previous_record.get("id", 0)) != PREVIOUS_RECORD_ID
        or previous_record.get("concept_doi") != CONCEPT_DOI
        or previous_record.get("version") != PREVIOUS_VERSION
    ):
        raise RuntimeError("Accepted BGK predecessor receipt has the wrong public identity")
    if set(previous) != set(classical) | OLD_BGK_FILES:
        raise RuntimeError("Accepted predecessor inventory is not classical-eight plus BGK-ten")
    if any(previous[name] != classical[name] for name in classical):
        raise RuntimeError("Classical files drifted between accepted Zenodo receipts")
    if (classical_receipt.get("record") or {}).get("concept_doi") != CONCEPT_DOI:
        raise RuntimeError("Classical baseline belongs to a different concept")
    return classical, {name: previous[name] for name in OLD_BGK_FILES}


def verify_checksums() -> None:
    checksum_path = RELEASE / "08_SHA256SUMS.txt"
    rows: dict[str, str] = {}
    for line in checksum_path.read_text(encoding="ascii").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\\/]+)", line)
        if not match or match.group(2) in rows:
            raise RuntimeError("Malformed or duplicate release checksum row")
        rows[match.group(2)] = match.group(1)
    expected_names = set(BGK_FILES) - {"08_SHA256SUMS.txt", "09_RELEASE_CANDIDATE_QA.json"}
    if set(rows) != expected_names:
        raise RuntimeError(f"Release checksum inventory mismatch: {sorted(rows)}")
    for name, expected in rows.items():
        if sha256_path(RELEASE / name) != expected:
            raise RuntimeError(f"Release checksum mismatch: {name}")


def release_contract() -> tuple[dict, dict, dict[str, dict]]:
    actual_names = {path.name for path in RELEASE.iterdir() if path.is_file()} if RELEASE.is_dir() else set()
    if actual_names != set(BGK_FILES):
        raise RuntimeError(f"Units 01--06 release inventory mismatch: {sorted(actual_names)}")
    manifest = load_json(RELEASE / "07_RELEASE_MANIFEST.json")
    qa = load_json(RELEASE / "09_RELEASE_CANDIDATE_QA.json")
    if (
        manifest.get("schema") != "ag-bridge-bgk-release-manifest-v1"
        or manifest.get("status") != "partial_coherent_checkpoint"
        or manifest.get("included_units") != list(range(1, 7))
        or manifest.get("included_unit_count") != 6
        or manifest.get("remaining_unit_count") != 24
        or manifest.get("model_provenance") != MODEL_PROVENANCE
        or qa.get("status") != "PASS"
        or (qa.get("scope_truth") or {}).get("bgk_units_complete") != 6
        or (qa.get("scope_truth") or {}).get("bgk_units_remaining") != 24
        or qa.get("model_provenance") != MODEL_PROVENANCE
        or (qa.get("reader_first") or {}).get("lexicographically_first_file") != BGK_FILES[0]
    ):
        raise RuntimeError("Release manifest/QA is not the exact Units 01--06 checkpoint")
    gates = qa.get("exact_gate_hashes") or {}
    for key in ("reader_qa", "visual_qa", "backend_qa", "common_adapter_qa"):
        item = gates.get(key) or {}
        path = ROOT / str(item.get("path", ""))
        if not path.is_file() or file_fact(path) != {"bytes": item.get("bytes"), "sha256": item.get("sha256")}:
            raise RuntimeError(f"Exact local QA gate hash is missing or drifted: {key}")
    facts = {name: file_fact(RELEASE / name) for name in BGK_FILES}
    declared = {item.get("path"): item for item in manifest.get("files", [])}
    expected_declared = set(BGK_FILES[:6])
    if set(declared) != expected_declared:
        raise RuntimeError("Release manifest payload inventory drifted")
    for name in expected_declared:
        if {"bytes": declared[name].get("bytes"), "sha256": declared[name].get("sha256")} != facts[name]:
            raise RuntimeError(f"Release manifest does not bind {name}")
    verify_checksums()
    return manifest, qa, facts


def migration_fact(reservation: dict) -> dict[str, object]:
    receipt = load_json(MIGRATION_RECEIPT)
    source = receipt.get("source") or {}
    coverage = receipt.get("coverage") or {}
    validation = receipt.get("validation") or {}
    transformation = receipt.get("transformation") or {}
    artifacts = receipt.get("public_artifacts") or []
    manifest_path = ROOT / "backend" / "bgk-units-01-06" / "MANIFEST.json"
    if (
        receipt.get("schema_name") != "interlanguage-math-modular-backend-migration-receipt"
        or coverage.get("through_unit") != 6
        or source.get("through_unit") != 6
        or source.get("manifest", {}).get("path") != "backend/bgk-units-01-06/MANIFEST.json"
        or source.get("manifest", {}).get("sha256") != sha256_path(manifest_path)
        or validation.get("result") != "pass"
        or validation.get("deterministic_double_replay") is not True
        or validation.get("lossless_native_reverse") is not True
        or transformation.get("model_provenance") != MODEL_PROVENANCE
        or receipt.get("credentials_recorded") is not False
        or len(artifacts) != 1
        or artifacts[0].get("repository") != "Zenodo"
        or artifacts[0].get("concept_doi") != CONCEPT_DOI
        or artifacts[0].get("doi") != reservation.get("doi")
        or artifacts[0].get("publication_uri") != reservation.get("record_url")
    ):
        raise RuntimeError("Final migration receipt does not bind the reserved Units 01--06 identity")
    return file_fact(MIGRATION_RECEIPT)


def metadata(manifest: dict) -> dict:
    reader = manifest.get("reader") or {}
    backend = manifest.get("backend") or {}
    pages = int(reader.get("pdf_pages", 0))
    exercises = int(reader.get("exercises", 0))
    public_solutions = int(reader.get("public_source_solutions", 0))
    missing = int(reader.get("documented_absent_source_solutions", -1))
    records = int(backend.get("native_records", 0))
    if min(pages, exercises, records) <= 0 or missing != exercises - public_solutions:
        raise RuntimeError("Release manifest exposes inconsistent reader/backend counts")
    payload = {
        "title": TITLE,
        "upload_type": "publication",
        "publication_type": "book",
        "description": (
            "<p><strong>Edisi Bahasa Indonesia (id-ID) dari dua kursus Holger Brenner.</strong> "
            "Volume <em>Kurva Aljabar</em> tetap lengkap pada 30 unit (504 halaman PDF, "
            "693 soal, dan seluruh 122 solusi publik yang dibekukan). Versi ini mengganti "
            "checkpoint BGK sebelumnya dengan checkpoint kumulatif enam kuliah dan enam "
            "lembar kerja (Unit 1–6) dari <em>Bundel, Berkas, dan Kohomologi</em>: "
            f"{pages} halaman PDF A4, HTML mandiri dengan MathML dan reflow seluler, "
            f"{exercises} soal, dan {public_solutions} solusi publik yang tersedia pada "
            f"revisi sumber. {missing} solusi lain memang tidak tersedia dalam sumber dan "
            "tidak diciptakan. Dua puluh empat unit kursus kedua masih tersisa; status "
            "parsial tersebut dinyatakan secara eksplisit.</p>"
            "<p>Delapan berkas volume klasik dari versi sebelumnya dipertahankan tanpa "
            "perubahan. Berkas checkpoint BGK Unit 1–3 diganti hanya di draf versi baru "
            "oleh checkpoint kumulatif Unit 1–6; versi publik sebelumnya tetap dapat "
            "diakses. Tambahan reader-first memuat PDF, HTML, sumber yang dapat "
            f"dilanjutkan, backend asli {records:,} rekaman, adapter backend umum "
            "tervalidasi, lisensi/hak komponen, manifest, checksum, dan bukti QA. Teks "
            "kursus dan terjemahannya berada di bawah CC BY-SA 4.0; media mempertahankan "
            "atribusi dan lisensi komponennya. Edisi independen ini disiapkan atas arahan "
            f"pengguna dengan {MODEL_PROVENANCE} Ini bukan terbitan resmi atau dukungan "
            "dari penulis sumber, Universitas Osnabrück, Wikiversity, Wikimedia Foundation, "
            "atau OpenAI.</p>"
            "<p><strong>English identification:</strong> Indonesian edition of Holger "
            "Brenner's two-course algebraic-geometry sequence. The complete 30-unit "
            "<em>Algebraische Kurven</em> volume is preserved unchanged; this version "
            "advances the cumulative partial checkpoint through Units 1–6 of "
            "<em>Bündel, Garben und Kohomologie</em>. Course text and translation are CC "
            "BY-SA 4.0, with component-specific media rights retained. Independent, "
            "non-endorsed derivative.</p>"
        ),
        "creators": [{"name": "Brenner, Holger"}],
        "contributors": [
            {"name": "TTP", "type": "Other", "affiliation": ORGANIZATION_HUB},
            {"name": MODEL_ID, "type": "Other"},
        ],
        "access_right": "open",
        "license": "other-open",
        "keywords": [
            "geometri aljabar", "algebraic geometry", "Bahasa Indonesia", "id-ID",
            "kurva aljabar", "berkas", "kohomologi", "open textbook",
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
    if serialized.count("TTP") != 1 or TITLE.startswith("TTP") or payload["description"].lstrip().startswith("TTP"):
        raise RuntimeError("Organization metadata convention violated")
    if MODEL_PROVENANCE not in payload["description"]:
        raise RuntimeError("Exact model provenance missing from metadata")
    return payload


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
        raise RuntimeError(f"Zenodo {method} failed with HTTP {response.status_code}: {response.text[:800]}")
    return response


def authenticated_session() -> tuple[requests.Session, str]:
    token = token_from_file()
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session, token


def public_latest() -> dict:
    response = requests.get(f"{BASE}/api/records/{PREVIOUS_RECORD_ID}/versions/latest", timeout=180)
    response.raise_for_status()
    return response.json()


def validate_latest(latest: dict) -> str:
    if latest.get("conceptdoi") != CONCEPT_DOI:
        raise RuntimeError("Zenodo concept DOI mismatch")
    version = (latest.get("metadata") or {}).get("version")
    if version == VERSION:
        return "target_public"
    if int(latest.get("id", 0)) != PREVIOUS_RECORD_ID or version != PREVIOUS_VERSION:
        raise RuntimeError("An unreviewed version is latest; refusing to branch or create a concept")
    return "predecessor_public"


def stream_public_files(record: dict, expected: dict[str, dict]) -> list[dict]:
    public = {row["key"]: row for row in record.get("files", [])}
    if set(public) != set(expected):
        raise RuntimeError(f"Public Zenodo inventory mismatch: {sorted(public)}")
    verified = []
    for name in sorted(expected):
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
        verified.append({"name": name, **actual, "public_readback": True, "credential_used": False})
    return verified


def verify_public(record_id: int, expected: dict[str, dict]) -> tuple[dict, list[dict]]:
    record = None
    for attempt in range(60):
        response = requests.get(f"{BASE}/api/records/{record_id}", timeout=180)
        if response.ok:
            candidate = response.json()
            if {row.get("key") for row in candidate.get("files", [])} == set(expected):
                record = candidate
                break
        if attempt < 59:
            time.sleep(2)
    if record is None:
        raise RuntimeError("Published version did not expose the expected inventory")
    return record, stream_public_files(record, expected)


def local_preflight() -> dict:
    classical, old_bgk = predecessor_facts()
    manifest, _, new = release_contract()
    metadata_value = metadata(manifest)
    return {
        "status": "PASS",
        "mode": "strict_local_only_no_network_no_credentials",
        "concept_doi": CONCEPT_DOI,
        "previous_record_id": PREVIOUS_RECORD_ID,
        "target_version": VERSION,
        "classical_files_preserved": len(classical),
        "superseded_bgk_files_identified": len(old_bgk),
        "new_release_files_verified": len(new),
        "new_release_bytes": sum(int(item["bytes"]) for item in new.values()),
        "final_migration_receipt": "required_after_reservation",
        "metadata_organization_occurrences": json.dumps(metadata_value, ensure_ascii=False).count("TTP"),
        "public_state_mutated": False,
        "credential_read": False,
    }


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
        "classical_files_preserved": sorted(predecessor_facts()[0]),
        "superseded_bgk_files_replaced_only_in_new_draft": sorted(OLD_BGK_FILES),
        "prior_public_record_remains_accessible": True,
        "target_files_planned": list(BGK_FILES) + [MIGRATION_PUBLIC_NAME],
        "credentials_recorded": False,
    }


def reserve() -> dict:
    classical, old_bgk = predecessor_facts()
    manifest, _, _ = release_contract()
    latest = public_latest()
    if validate_latest(latest) == "target_public":
        descriptor = reservation_descriptor(latest, "already_public")
        canonical_write(RESERVATION, descriptor)
        return descriptor

    session, token = authenticated_session()
    draft = None
    if RESERVATION.is_file():
        prior = load_json(RESERVATION)
        if prior.get("concept_doi") == CONCEPT_DOI and prior.get("version") == VERSION:
            response = session.get(f"{BASE}/api/deposit/depositions/{int(prior['record_id'])}", timeout=180)
            if response.ok and not response.json().get("submitted"):
                draft = response.json()
    if draft is None:
        drafts = request(
            session, "GET", f"{BASE}/api/deposit/depositions",
            params={"status": "draft", "sort": "mostrecent", "size": 100},
        ).json()
        candidates = [
            item for item in drafts
            if not item.get("submitted") and int(item.get("conceptrecid") or 0) == CONCEPT_RECORD_ID
        ]
        if len(candidates) > 1:
            raise RuntimeError("Multiple unsubmitted drafts exist in the target concept")
        if candidates:
            draft = candidates[0]
        else:
            response = request(
                session, "POST", f"{BASE}/api/deposit/depositions/{PREVIOUS_RECORD_ID}/actions/newversion"
            ).json()
            draft_url = (response.get("links") or {}).get("latest_draft")
            if not draft_url:
                raise RuntimeError("New-version response has no latest_draft link")
            draft = request(session, "GET", draft_url).json()

    names = {item.get("filename") or item.get("key") for item in draft.get("files", [])}
    allowed = set(classical) | set(old_bgk) | set(BGK_FILES) | {MIGRATION_PUBLIC_NAME}
    if not set(classical).issubset(names) or not names.issubset(allowed):
        raise RuntimeError(f"Zenodo draft inventory is unsafe: {sorted(names)}")
    draft = request(session, "PUT", draft["links"]["self"], json={"metadata": metadata(manifest)}).json()
    if draft.get("submitted"):
        raise RuntimeError("Reserved draft unexpectedly reports submitted=true")
    descriptor = reservation_descriptor(draft, "reserved_draft")
    canonical_write(RESERVATION, descriptor)
    del token
    session.close()
    return descriptor


def write_publication_receipt(record: dict, verified: list[dict], manifest: dict) -> None:
    metadata_value = record.get("metadata") or {}
    contributors = metadata_value.get("contributors") or []
    reader = manifest.get("reader") or {}
    backend = manifest.get("backend") or {}
    canonical_write(
        PUBLICATION_RECEIPT,
        {
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
                "bgk_units_complete": 6,
                "bgk_units_total": 30,
                "bgk_units_remaining": 24,
                "pdf_pages": reader.get("pdf_pages"),
                "exercises": reader.get("exercises"),
                "public_source_solutions": reader.get("public_source_solutions"),
                "native_backend_records": backend.get("native_records"),
                "classical_files_preserved": 8,
                "superseded_bgk_files_replaced_in_new_version": 10,
                "target_bgk_files": 10,
                "prior_public_record_remains_accessible": True,
            },
            "metadata_cleanliness": {
                "creator": "Brenner, Holger",
                "organization_contributor_count": sum(item.get("name") == "TTP" for item in contributors),
                "organization_hub": ORGANIZATION_HUB,
                "model_contributor_count": sum(item.get("name") == MODEL_ID for item in contributors),
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
        },
    )


def publish() -> dict:
    classical, old_bgk = predecessor_facts()
    manifest, _, new_release = release_contract()
    if not RESERVATION.is_file():
        raise RuntimeError("Reservation receipt missing; run --reserve first")
    reservation = load_json(RESERVATION)
    if (
        reservation.get("concept_doi") != CONCEPT_DOI
        or reservation.get("version") != VERSION
        or reservation.get("previous_record_id") != PREVIOUS_RECORD_ID
    ):
        raise RuntimeError("Reservation identity mismatch")
    migration = migration_fact(reservation)
    new = {**new_release, MIGRATION_PUBLIC_NAME: migration}
    expected = {**classical, **new}
    if len(expected) != 18:
        raise RuntimeError("Final Zenodo inventory must contain 18 collision-free files")

    latest = public_latest()
    if validate_latest(latest) == "target_public":
        record, verified = verify_public(int(latest["id"]), expected)
        write_publication_receipt(record, verified, manifest)
        return {"status": "PASS", "action": "verified_existing_units_01_06", "record_id": int(record["id"]), "files_verified": len(verified)}

    session, token = authenticated_session()
    draft_id = int(reservation["record_id"])
    draft = request(session, "GET", f"{BASE}/api/deposit/depositions/{draft_id}").json()
    if draft.get("submitted"):
        raise RuntimeError("Reserved draft is submitted but not public latest")
    names = {item.get("filename") or item.get("key") for item in draft.get("files", [])}
    allowed = set(classical) | set(old_bgk) | set(new)
    if not set(classical).issubset(names) or not names.issubset(allowed):
        raise RuntimeError(f"Zenodo draft inventory is unsafe: {sorted(names)}")

    # Remove only superseded/retry BGK files from this unsubmitted new-version
    # draft.  Never delete the eight classical files or touch the prior public
    # record, which remains immutable and accessible.
    replaceable = set(old_bgk) | set(new)
    for item in list(draft.get("files", [])):
        name = item.get("filename") or item.get("key")
        if name in replaceable and name not in classical:
            request(session, "DELETE", f"{BASE}/api/deposit/depositions/{draft_id}/files/{item['id']}")

    draft = request(session, "PUT", draft["links"]["self"], json={"metadata": metadata(manifest)}).json()
    bucket = draft["links"]["bucket"].rstrip("/")
    local_paths = {name: RELEASE / name for name in BGK_FILES}
    local_paths[MIGRATION_PUBLIC_NAME] = MIGRATION_RECEIPT
    for name in sorted(new):
        with local_paths[name].open("rb") as stream:
            request(session, "PUT", f"{bucket}/{quote(name, safe='')}", data=stream)

    refreshed = request(session, "GET", draft["links"]["self"]).json()
    refreshed_names = {item.get("filename") or item.get("key") for item in refreshed.get("files", [])}
    if refreshed_names != set(expected):
        raise RuntimeError(f"Pre-publication inventory mismatch: {sorted(refreshed_names)}")
    published = request(session, "POST", refreshed["links"]["publish"]).json()
    record_id = int(published.get("record_id") or published.get("id"))
    del token
    session.close()

    record, verified = verify_public(record_id, expected)
    public_metadata = record.get("metadata") or {}
    if record.get("conceptdoi") != CONCEPT_DOI or public_metadata.get("version") != VERSION or public_metadata.get("title") != TITLE:
        raise RuntimeError("Published metadata identity mismatch")
    write_publication_receipt(record, verified, manifest)
    return {
        "status": "PASS",
        "action": "published_new_version",
        "record_id": record_id,
        "doi": public_metadata["doi"],
        "files_verified": len(verified),
    }


def verify_existing() -> dict:
    classical, _ = predecessor_facts()
    manifest, _, new_release = release_contract()
    if not RESERVATION.is_file():
        raise RuntimeError("Reservation receipt missing")
    reservation = load_json(RESERVATION)
    migration = migration_fact(reservation)
    expected = {**classical, **new_release, MIGRATION_PUBLIC_NAME: migration}
    latest = public_latest()
    if validate_latest(latest) != "target_public":
        raise RuntimeError("Units 01--06 is not the public latest version")
    record, verified = verify_public(int(latest["id"]), expected)
    write_publication_receipt(record, verified, manifest)
    return {"status": "PASS", "record_id": int(record["id"]), "files_verified": len(verified)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--local-preflight", action="store_true")
    parser.add_argument("--reserve", action="store_true")
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--verify-public", action="store_true")
    args = parser.parse_args()
    modes = (args.local_preflight, args.reserve, args.publish, args.verify_public)
    if sum(modes) != 1:
        raise SystemExit("Choose exactly one mode")
    if args.local_preflight:
        result = local_preflight()
    elif args.reserve:
        result = reserve()
    elif args.publish:
        result = publish()
    else:
        result = verify_existing()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
