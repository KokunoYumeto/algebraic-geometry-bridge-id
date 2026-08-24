#!/usr/bin/env python3
"""Reserve/publish Unit 8 in the existing Zenodo concept and verify bytes."""

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
zenodo.RELEASE = ROOT / "release" / "unit-08"
zenodo.TOKEN_FILE = Path.home() / "Documents" / "Obsidian notes" / "New zenodo token.md"
zenodo.RESERVATION = ROOT / "qa" / "UNIT_08_ZENODO_RESERVATION.json"
zenodo.RECEIPT = ROOT / "qa" / "UNIT_08_ZENODO_PUBLICATION.json"
zenodo.PREVIOUS_RECORD_ID = 22062319
zenodo.CONCEPT_DOI = "10.5281/zenodo.22059686"
zenodo.TITLE = "Kurva Aljabar — Edisi Bahasa Indonesia"
zenodo.VERSION = "unit-08"
zenodo.FILES = [
    "kurva-aljabar-id-unit-08.pdf",
    "kurva-aljabar-id-unit-08.html",
    "kurva-aljabar-id-unit-08-source.zip",
    "kurva-aljabar-id-unit-08-authority-witnesses.zip",
    "BUILD_RECEIPT-unit-08.json",
    "LICENSE-unit-08.md",
    "ZENODO_FILE_MANIFEST-unit-08.json",
    "MIGRATION_RECEIPT.json",
]


def metadata() -> dict:
    return {
        "title": zenodo.TITLE,
        "upload_type": "publication",
        "publication_type": "book",
        "description": (
            "<p><strong>Rilis kumulatif kerja Bahasa Indonesia (id-ID), Unit 1–8</strong>, "
            "dari <em>Algebraische Kurven (Osnabrück 2025–2026)</em> karya Holger Brenner. "
            "Batas ini memuat delapan kuliah, delapan lembar kerja dengan 221 soal, dan "
            "42 solusi publik yang tersedia pada revisi sumber yang dibekukan. Ini belum "
            "merupakan edisi 30-unit yang lengkap; penerjemahan berlanjut dalam urutan sumber.</p>"
            "<p>Paket preservasi memuat pembaca PDF A4 161 halaman, pembaca HTML mandiri "
            "dengan MathML dan reflow seluler, snapshot sumber/backend 5.787 rekaman yang "
            "dapat dilanjutkan, adapter backend modular tervalidasi, manifest, build receipt, "
            "saksi otoritas, hak komponen, dan bukti QA. Terjemahan dan penataan ulang teks "
            "kursus berada di bawah CC BY-SA 4.0; setiap media pihak ketiga mempertahankan "
            "pencipta, sumber, dan lisensi komponennya sendiri. Edisi independen ini disiapkan "
            "atas arahan pengguna dengan OpenAI Codex gpt-5.6-sol, Ultra. Ini bukan terbitan "
            "resmi Holger Brenner, Universitas Osnabrück, Wikiversity, atau Wikimedia Foundation, "
            "dan tidak menyiratkan dukungan mereka.</p>"
            "<p><strong>English identification:</strong> Cumulative working Indonesian (id-ID) "
            "edition, Units 1–8, of Holger Brenner's <em>Algebraische Kurven (Osnabrück "
            "2025–2026)</em>, with self-contained HTML, A4 PDF, editable source/backend snapshot, "
            "component-rights records, authority witnesses, and QA evidence. This is an "
            "independent, non-endorsed derivative and not yet the complete 30-unit edition.</p>"
        ),
        "creators": [{"name": "Brenner, Holger"}],
        # The single organization entry is intentionally the only TTP token in
        # Zenodo metadata; the affiliation is the canonical project hub link.
        "contributors": [
            {"name": "TTP", "type": "Other", "affiliation": "https://github.com/KokunoYumeto/program-matematika-indonesia"},
            {"name": "OpenAI Codex gpt-5.6-sol, Ultra", "type": "Other"},
        ],
        "access_right": "open",
        "license": "other-open",
        "keywords": [
            "geometri aljabar", "algebraic geometry", "Bahasa Indonesia", "id-ID",
            "kurva aljabar", "open textbook",
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
                "identifier": "https://github.com/KokunoYumeto/program-matematika-indonesia",
                "relation": "isReferencedBy",
                "resource_type": "software",
            },
        ],
    }


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_receipt(record: dict, verified: list[dict]) -> None:
    public_metadata = record["metadata"]
    contributors = public_metadata.get("contributors", [])
    title = public_metadata["title"]
    description = public_metadata.get("description", "")
    if "TTP" in title or "TTP" in description:
        raise RuntimeError("TTP leaked into title or description")
    if sum(item.get("name") == "TTP" for item in contributors) != 1:
        raise RuntimeError("Zenodo organization entry count is not exactly one")
    receipt = {
        "schema": "ag-bridge-zenodo-publication-receipt-v2",
        "status": "PASS",
        "record": {
            "id": int(record["id"]),
            "url": record["links"]["self_html"],
            "api_url": record["links"]["self"],
            "doi": public_metadata["doi"],
            "concept_doi": record["conceptdoi"],
            "title": title,
            "version": public_metadata["version"],
            "publication_date": public_metadata["publication_date"],
            "published_timestamp": record.get("created"),
            "zenodo_state": "done",
            "zenodo_status": "published",
        },
        "reader_boundary": {
            "through_unit": 8,
            "planned_units": 30,
            "full_edition_complete": False,
            "incomplete_boundary_disclosed_in_description": True,
        },
        "metadata_cleanliness": {
            "creator": "Brenner, Holger",
            "organization_name": "TTP",
            "organization_contributor_count": sum(item.get("name") == "TTP" for item in contributors),
            "organization_hub": "https://github.com/KokunoYumeto/program-matematika-indonesia",
            "ai_contributor_count": sum(item.get("name", "").startswith("OpenAI Codex") for item in contributors),
            "work_title_preserved_without_organization_prefix": not title.startswith("TTP"),
            "description_lead_preserved_without_organization_prefix": not description.lstrip().startswith("TTP"),
            "non_endorsement_disclosed": True,
            "license_field": public_metadata["license"]["id"],
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
    zenodo.RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


zenodo.metadata = metadata
zenodo.write_receipt = write_receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--reserve", action="store_true")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    if sum((args.preflight, args.reserve, args.publish)) != 1:
        raise SystemExit("Choose exactly one of --preflight, --reserve, or --publish")
    result = zenodo.preflight() if args.preflight else zenodo.reserve() if args.reserve else zenodo.publish()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

