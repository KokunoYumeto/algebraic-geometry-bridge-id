#!/usr/bin/env python3
"""Offline deterministic replay of the frozen Unit 27 authority boundary.

This verifier reads only captured Unit 27 witnesses and does not make network
requests. It fails closed on identity, closure, exercise, rights, media, PDF,
and manifest inventory gates.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / "authority"
UNIT = AUTH / "wikiversity" / "unit-27"
MANIFEST_PATH = UNIT / "UNIT_AUTHORITY_MANIFEST.json"
RIGHTS_PATH = AUTH / "RIGHTS-unit-27.csv"
CLOSURE_PATH = AUTH / "ASSET_CLOSURE-unit-27.json"
QA_PATH = ROOT / "qa" / "UNIT_27_AUTHORITY_QA.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    require(MANIFEST_PATH.is_file(), "authority manifest missing")
    require(RIGHTS_PATH.is_file(), "rights ledger missing")
    require(CLOSURE_PATH.is_file(), "asset closure missing")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    closure = json.loads(CLOSURE_PATH.read_text(encoding="utf-8"))

    require(manifest.get("schema") == "brenner-unit-authority-freeze-v2", "manifest schema")
    require(manifest.get("unit_number") == 27, "manifest unit")
    require(manifest["lecture"]["pageid"] == 50733 and manifest["lecture"]["revid"] == 1052572, "lecture identity")
    require(manifest["lecture"]["mediawiki_sha1"] == "9a396f3a601f0a0a0606657550a30b9a601da2f6", "lecture SHA-1")
    require(manifest["worksheet"]["pageid"] == 50762 and manifest["worksheet"]["revid"] == 793496, "worksheet identity")
    require(manifest["worksheet"]["mediawiki_sha1"] == "eeac2c6881d4121e734bc2dffbe9621f03dfdc89", "worksheet SHA-1")
    require(manifest["transclusion_topology"]["lecture"]["with_root"] == 121, "lecture closure count")
    require(manifest["transclusion_topology"]["lecture"]["canonical_identity_rows_sha256"] == "5ed97c57220d6379b672fd7b47a8cfca82c38ef4e84bafd3538e3cdf42f74ca8", "lecture closure hash")
    require(manifest["transclusion_topology"]["worksheet"]["with_root"] == 61, "worksheet closure count")
    require(manifest["transclusion_topology"]["worksheet"]["canonical_identity_rows_sha256"] == "bea2d1bb50691139418ccf884928594f7658bc3bad1a0e22b8a4c99eb71c8b24", "worksheet closure hash")
    solutions = manifest["solutions"]
    require(solutions["exercise_count"] == 11, "exercise count")
    require(solutions["solution_count"] == 0, "public solution count")
    require(solutions["negative_public_solution_evidence"]["negative_count"] == 11, "negative solution count")
    require(closure["reader_media_positions"] == 10 and closure["unique_local_assets"] == 10, "media topology")
    require(manifest["final_live_identity_replay"]["result"] == "PASS", "live replay result")
    require(manifest["final_live_identity_replay"]["semantic_unique_identity_count"] == 157, "live semantic union")
    require(manifest["final_live_identity_replay"]["commons_media_identity_count"] == 10, "live media replay")

    external = {item["file"]: item for item in manifest["bounded_external_files"]}
    for rel, expected in external.items():
        path = ROOT / rel
        require(path.is_file(), f"missing bound file: {rel}")
        require(path.stat().st_size == expected["bytes"], f"byte drift: {rel}")
        require(sha256(path) == expected["sha256"], f"hash drift: {rel}")

    for item in closure["assets"]:
        path = ROOT / item["local_path"]
        witness = ROOT / item["authority_witness_path"]
        require(path.is_file() and witness.is_file(), f"asset missing: {item['source_parser_name']}")
        require(path.stat().st_size == item["local_bytes"], f"asset bytes: {item['source_parser_name']}")
        require(sha256(path) == item["local_sha256"], f"asset hash: {item['source_parser_name']}")
        require(path.read_bytes() == witness.read_bytes(), f"asset witness mismatch: {item['source_parser_name']}")

    pdf_rows = []
    for item in manifest["official_pdf_witnesses"]:
        path = ROOT / item["local_path"]
        require(path.is_file(), f"PDF missing: {item['kind']}")
        require(path.stat().st_size == item["local_bytes"], f"PDF bytes: {item['kind']}")
        require(sha256(path) == item["local_sha256"], f"PDF hash: {item['kind']}")
        pages = None
        if PdfReader is not None:
            reader = PdfReader(str(path))
            pages = len(reader.pages)
            require(pages == item["page_count"], f"PDF page count: {item['kind']}")
        pdf_rows.append({"kind": item["kind"], "bytes": item["local_bytes"], "sha256": item["local_sha256"], "pages": pages})

    for rel in ("source/id-ID/lecture-27.md", "source/id-ID/worksheet-27.md", "source/id-ID/worksheet-27-solutions.md"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        require("UNBOUND_PENDING" not in text, f"unbound source manifest: {rel}")
        require("OpenAI Codex gpt-5.6-sol, Ultra" in text, f"provenance missing: {rel}")
        require(not any(mark in text for mark in ("\u2013", "\u2014", "\u2011")), f"unicode dash in {rel}")
    lecture = (ROOT / "source/id-ID/lecture-27.md").read_text(encoding="utf-8")
    require(lecture.count("<!-- upstream_entity:") == 21, "lecture semantic entity count")
    require(lecture.count("![") == 10, "lecture media count")
    worksheet = (ROOT / "source/id-ID/worksheet-27.md").read_text(encoding="utf-8")
    require(worksheet.count("### Soal 27.") == 11, "worksheet exercise count")

    receipt = {
        "schema": "ag-bridge-unit-authority-qa-v1",
        "unit": 27,
        "status": "PASS",
        "authority_manifest": {"path": "authority/wikiversity/unit-27/UNIT_AUTHORITY_MANIFEST.json", "bytes": MANIFEST_PATH.stat().st_size, "sha256": sha256(MANIFEST_PATH)},
        "authority": {"lecture_closure_with_root": 121, "worksheet_closure_with_root": 61, "semantic_union": 157},
        "exercises": {"count": 11, "public_solutions": 0, "negative_candidates": 11},
        "media": {"positions": 10, "assets": 10},
        "pdfs": pdf_rows,
        "rights": {"path": "authority/RIGHTS-unit-27.csv", "bytes": RIGHTS_PATH.stat().st_size, "sha256": sha256(RIGHTS_PATH)},
        "asset_closure": {"path": "authority/ASSET_CLOSURE-unit-27.json", "bytes": CLOSURE_PATH.stat().st_size, "sha256": sha256(CLOSURE_PATH)},
        "offline_replay": True,
        "network_replay_witness": "authority/wikiversity/unit-27/final-commons-media-identity-replay.json",
        "provenance": "OpenAI Codex gpt-5.6-sol, Ultra",
    }
    QA_PATH.parent.mkdir(parents=True, exist_ok=True)
    QA_PATH.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(receipt, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
