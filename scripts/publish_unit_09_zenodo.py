#!/usr/bin/env python3
"""Reserve/publish Unit 9 in the existing Zenodo concept and verify bytes.

The ``--self-check`` action is deliberately offline: it validates only the
static Unit 9 publication contract and does not inspect credentials, call
Zenodo, or require the release files to exist yet.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
U7_PATH = ROOT / "scripts" / "publish_unit_07_zenodo.py"
spec = importlib.util.spec_from_file_location("unit07_zenodo_helpers", U7_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load Zenodo publication helpers")
zenodo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(zenodo)

zenodo.ROOT = ROOT
zenodo.RELEASE = ROOT / "release" / "unit-09"
zenodo.TOKEN_FILE = Path.home() / "Documents" / "Obsidian notes" / "New zenodo token.md"
zenodo.RESERVATION = ROOT / "qa" / "UNIT_09_ZENODO_RESERVATION.json"
zenodo.RECEIPT = ROOT / "qa" / "UNIT_09_ZENODO_PUBLICATION.json"
zenodo.PREVIOUS_RECORD_ID = 22070936
zenodo.CONCEPT_DOI = "10.5281/zenodo.22059686"
zenodo.TITLE = "Kurva Aljabar — Edisi Bahasa Indonesia"
zenodo.VERSION = "unit-09"
zenodo.FILES = [
    "kurva-aljabar-id-unit-09.pdf",
    "kurva-aljabar-id-unit-09.html",
    "kurva-aljabar-id-unit-09-source.zip",
    "kurva-aljabar-id-unit-09-authority-witnesses.zip",
    "BUILD_RECEIPT-unit-09.json",
    "LICENSE-unit-09.md",
    "ZENODO_FILE_MANIFEST-unit-09.json",
    "MIGRATION_RECEIPT.json",
]

ORGANIZATION_HUB = "https://github.com/KokunoYumeto/program-matematika-indonesia"
PROVENANCE = "OpenAI Codex gpt-5.6-sol, Ultra."
AI_CONTRIBUTOR = PROVENANCE.removesuffix(".")

EXPECTED_UNITS = 9
EXPECTED_EXERCISES = 245
EXPECTED_PUBLIC_SOLUTIONS = 45
EXPECTED_PDF_PAGES = 174
EXPECTED_NATIVE_BACKEND_RECORDS = 6393


def _validate_metadata(payload: dict) -> None:
    """Fail closed if the static Unit 9 metadata contract drifts."""

    description = payload.get("description", "")
    title = payload.get("title", "")
    contributors = payload.get("contributors", [])
    ttp_entries = [item for item in contributors if item.get("name") == "TTP"]
    ai_entries = [item for item in contributors if item.get("name") == AI_CONTRIBUTOR]

    if title != "Kurva Aljabar — Edisi Bahasa Indonesia":
        raise RuntimeError("The work title drifted from the preserved Unit 9 title")
    if "TTP" in title or "TTP" in description:
        raise RuntimeError("TTP leaked into the title or description")
    if json.dumps(payload, ensure_ascii=False).count("TTP") != 1:
        raise RuntimeError("TTP must occur exactly once in Zenodo metadata")
    if ttp_entries != [
        {"name": "TTP", "type": "Other", "affiliation": ORGANIZATION_HUB}
    ]:
        raise RuntimeError("The sole TTP organization contributor is not exact")
    if ai_entries != [{"name": AI_CONTRIBUTOR, "type": "Other"}]:
        raise RuntimeError("The exact model contributor entry is missing or duplicated")
    if payload.get("creators") != [{"name": "Brenner, Holger"}]:
        raise RuntimeError("The source author must remain the sole creator")
    if payload.get("license") != "other-open":
        raise RuntimeError("Mixed-rights releases must use Zenodo license other-open")
    if payload.get("access_right") != "open":
        raise RuntimeError("Unit 9 must be an open-access checkpoint")
    if payload.get("language") != "ind" or payload.get("version") != "unit-09":
        raise RuntimeError("The Unit 9 language/version metadata drifted")
    if PROVENANCE not in description:
        raise RuntimeError("The exact model provenance sentence is missing")

    required_description_markers = (
        "Unit 1–9",
        "245 soal",
        "45 solusi publik",
        "174 halaman",
        "6.393 rekaman",
        "CC BY-SA 4.0",
        "lisensi komponennya sendiri",
        "belum merupakan edisi 30-unit yang lengkap",
        "tidak menyiratkan dukungan mereka",
        "Units 1–9",
        "independent, non-endorsed derivative",
    )
    missing = [marker for marker in required_description_markers if marker not in description]
    if missing:
        raise RuntimeError(f"Required Unit 9 description markers missing: {missing}")


def metadata() -> dict:
    payload = {
        "title": zenodo.TITLE,
        "upload_type": "publication",
        "publication_type": "book",
        "description": (
            "<p><strong>Rilis kumulatif kerja Bahasa Indonesia (id-ID), Unit 1–9</strong>, "
            "dari <em>Algebraische Kurven (Osnabrück 2025–2026)</em> karya Holger Brenner. "
            "Batas ini memuat sembilan kuliah, sembilan lembar kerja dengan 245 soal, dan "
            "45 solusi publik yang tersedia pada revisi sumber yang dibekukan. Ini belum "
            "merupakan edisi 30-unit yang lengkap; penerjemahan berlanjut dalam urutan sumber.</p>"
            "<p>Paket preservasi memuat pembaca PDF A4 174 halaman, pembaca HTML mandiri "
            "dengan MathML dan reflow seluler, snapshot sumber/backend asli 6.393 rekaman "
            "yang dapat dilanjutkan, adapter backend modular tervalidasi, manifest, build "
            "receipt, saksi otoritas, hak komponen, dan bukti QA. Terjemahan dan penataan "
            "ulang teks kursus berada di bawah CC BY-SA 4.0; setiap media pihak ketiga "
            "mempertahankan pencipta, sumber, dan lisensi komponennya sendiri. Edisi "
            f"independen ini disiapkan atas arahan pengguna dengan {PROVENANCE} Ini bukan "
            "terbitan resmi Holger Brenner, Universitas Osnabrück, Wikiversity, atau "
            "Wikimedia Foundation, dan tidak menyiratkan dukungan mereka.</p>"
            "<p><strong>English identification:</strong> Cumulative working Indonesian "
            "(id-ID) edition, Units 1–9, of Holger Brenner's <em>Algebraische Kurven "
            "(Osnabrück 2025–2026)</em>, with self-contained HTML, 174-page A4 PDF, "
            "editable source and 6,393-record native-backend snapshot, validated modular "
            "backend adapter, component-rights records, authority witnesses, and QA evidence. "
            "This is an independent, non-endorsed derivative and not yet the complete "
            "30-unit edition.</p>"
        ),
        "creators": [{"name": "Brenner, Holger"}],
        # This is intentionally the only occurrence of the organization label
        # in Zenodo metadata. Its affiliation provides the clickable hub.
        "contributors": [
            {"name": "TTP", "type": "Other", "affiliation": ORGANIZATION_HUB},
            {"name": AI_CONTRIBUTOR, "type": "Other"},
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
        "version": zenodo.VERSION,
        "related_identifiers": [
            {
                "identifier": "https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)",
                "relation": "isDerivedFrom",
                "resource_type": "publication-book",
            },
            {
                "identifier": ORGANIZATION_HUB,
                "relation": "isReferencedBy",
                "resource_type": "software",
            },
        ],
    }
    _validate_metadata(payload)
    return payload


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_receipt(record: dict, verified: list[dict]) -> None:
    public_metadata = record["metadata"]
    contributors = public_metadata.get("contributors", [])
    title = public_metadata["title"]
    description = public_metadata.get("description", "")
    ttp_entries = [item for item in contributors if item.get("name") == "TTP"]
    ai_entries = [item for item in contributors if item.get("name") == AI_CONTRIBUTOR]
    verified_names = [item.get("name") for item in verified]

    if "TTP" in title or "TTP" in description:
        raise RuntimeError("TTP leaked into the public title or description")
    if len(ttp_entries) != 1 or ttp_entries[0].get("affiliation") != ORGANIZATION_HUB:
        raise RuntimeError("The public TTP organization contributor is not exact")
    if len(ai_entries) != 1 or PROVENANCE not in description:
        raise RuntimeError("The exact public model provenance is missing or duplicated")
    if record.get("conceptdoi") != zenodo.CONCEPT_DOI:
        raise RuntimeError("The published record escaped the existing Zenodo concept")
    if title != zenodo.TITLE or public_metadata.get("version") != zenodo.VERSION:
        raise RuntimeError("The published title/version differs from the frozen Unit 9 contract")
    license_id = public_metadata.get("license", {}).get("id")
    if license_id != "other-open":
        raise RuntimeError("The public mixed-rights license field is not other-open")
    if verified_names != zenodo.FILES or len(set(verified_names)) != len(zenodo.FILES):
        raise RuntimeError("Anonymous public readback inventory differs from the frozen file order")

    receipt = {
        "schema": "ag-bridge-zenodo-publication-receipt-v2",
        "status": "PASS",
        "record": {
            "id": int(record["id"]),
            "url": record["links"]["self_html"],
            "api_url": record["links"]["self"],
            "doi": public_metadata["doi"],
            "concept_doi": record["conceptdoi"],
            "previous_record_id": zenodo.PREVIOUS_RECORD_ID,
            "title": title,
            "version": public_metadata["version"],
            "publication_date": public_metadata["publication_date"],
            "published_timestamp": record.get("created"),
            "zenodo_state": "done",
            "zenodo_status": "published",
        },
        "reader_boundary": {
            "through_unit": EXPECTED_UNITS,
            "planned_units": 30,
            "full_edition_complete": False,
            "incomplete_boundary_disclosed_in_description": True,
            "exercises": EXPECTED_EXERCISES,
            "public_source_solutions": EXPECTED_PUBLIC_SOLUTIONS,
            "pdf_pages": EXPECTED_PDF_PAGES,
            "native_backend_records": EXPECTED_NATIVE_BACKEND_RECORDS,
        },
        "metadata_cleanliness": {
            "creator": "Brenner, Holger",
            "organization_name": "TTP",
            "organization_contributor_count": len(ttp_entries),
            "organization_hub": ORGANIZATION_HUB,
            "ai_contributor": AI_CONTRIBUTOR,
            "ai_contributor_count": len(ai_entries),
            "exact_model_provenance": PROVENANCE,
            "work_title_preserved_without_organization_prefix": not title.startswith("TTP"),
            "description_lead_preserved_without_organization_prefix": not description.lstrip().startswith("TTP"),
            "non_endorsement_disclosed": True,
            "license_field": license_id,
            "license_field_rationale": "Avoids applying a false blanket licence to the mixed-rights file set.",
            "translated_course_text_license": "CC BY-SA 4.0",
            "third_party_media_license_policy": "Per-component rights and attribution are preserved in the source package.",
        },
        "anonymous_public_byte_readback": {
            "verified_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "credential_used": False,
            "files_expected": len(zenodo.FILES),
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
    zenodo.RECEIPT.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def self_check() -> dict:
    payload = metadata()
    if zenodo.PREVIOUS_RECORD_ID != 22070936:
        raise RuntimeError("Previous Zenodo record ID drifted")
    if zenodo.CONCEPT_DOI != "10.5281/zenodo.22059686":
        raise RuntimeError("Zenodo concept DOI drifted")
    if zenodo.RELEASE != ROOT / "release" / "unit-09":
        raise RuntimeError("Unit 9 release directory drifted")
    if len(zenodo.FILES) != 8 or len(set(zenodo.FILES)) != 8:
        raise RuntimeError("The frozen Unit 9 inventory must contain eight unique files")
    if any("unit-08" in name or "unit-07" in name for name in zenodo.FILES):
        raise RuntimeError("A prior-unit filename leaked into the Unit 9 inventory")
    if zenodo.FILES[-1] != "MIGRATION_RECEIPT.json":
        raise RuntimeError("The sanitized common-backend receipt is missing")
    return {
        "status": "PASS",
        "mode": "offline_static_contract_only",
        "credential_read": False,
        "network_called": False,
        "title": payload["title"],
        "version": payload["version"],
        "previous_record_id": zenodo.PREVIOUS_RECORD_ID,
        "concept_doi": zenodo.CONCEPT_DOI,
        "license": payload["license"],
        "metrics": {
            "through_unit": EXPECTED_UNITS,
            "exercises": EXPECTED_EXERCISES,
            "public_source_solutions": EXPECTED_PUBLIC_SOLUTIONS,
            "pdf_pages": EXPECTED_PDF_PAGES,
            "native_backend_records": EXPECTED_NATIVE_BACKEND_RECORDS,
        },
        "files": list(zenodo.FILES),
        "exact_provenance_present": PROVENANCE in payload["description"],
        "metadata_ttp_occurrences": json.dumps(payload, ensure_ascii=False).count("TTP"),
    }


zenodo.metadata = metadata
zenodo.write_receipt = write_receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--reserve", action="store_true")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    if sum((args.self_check, args.preflight, args.reserve, args.publish)) != 1:
        raise SystemExit("Choose exactly one of --self-check, --preflight, --reserve, or --publish")
    if args.self_check:
        result = self_check()
    elif args.preflight:
        result = zenodo.preflight()
    elif args.reserve:
        result = zenodo.reserve()
    else:
        result = zenodo.publish()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
