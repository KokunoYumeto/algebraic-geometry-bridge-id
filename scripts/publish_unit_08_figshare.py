#!/usr/bin/env python3
"""Update the existing lawful Figshare metadata pointer for Unit 8."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
U7_PATH = ROOT / "scripts" / "publish_unit_07_figshare.py"
spec = importlib.util.spec_from_file_location("unit07_figshare_helpers", U7_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load Figshare publication helpers")
figshare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(figshare)

figshare.ROOT = ROOT
figshare.TOKEN_FILE = Path.home() / "Documents" / "TOKENS" / "Figshare Token.md"
figshare.RECEIPT = ROOT / "qa" / "UNIT_08_FIGSHARE_PUBLICATION.json"
figshare.TITLE = "Kurva Aljabar — Edisi Bahasa Indonesia"
figshare.ZENODO_CONCEPT = "10.5281/zenodo.22059686"
figshare.ZENODO_VERSION = "10.5281/zenodo.22070936"
figshare.SOURCE_URL = "https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)"


def description() -> str:
    return (
        "<p><strong>Catatan metadata saja; tidak ada byte edisi yang diunggah ke item Figshare ini.</strong> "
        "Berkas pembaca dan sumber terverifikasi tersedia pada DOI konsep Zenodo "
        f"<a href=\"https://doi.org/{figshare.ZENODO_CONCEPT}\">{figshare.ZENODO_CONCEPT}</a>; "
        f"versi Unit 8 saat ini ialah <a href=\"https://doi.org/{figshare.ZENODO_VERSION}\">{figshare.ZENODO_VERSION}</a>.</p>"
        "<p><strong>Status:</strong> <code>active_partial</code> — Unit 1–8 dari 30 unit "
        "<em>Algebraische Kurven (Osnabrück 2025–2026)</em> telah diterjemahkan dan diverifikasi. "
        "Batas kumulatif ini memuat delapan kuliah, delapan lembar kerja, 221 soal, 42 solusi publik, "
        "59 posisi media, pembaca HTML mandiri dengan MathML/reflow seluler, PDF A4 161 halaman, "
        "dan backend ID stabil dengan 5.787 rekaman. Ini belum merupakan edisi 30-unit yang lengkap; "
        "produksi berlanjut dalam urutan sumber.</p>"
        "<p><strong>Lisensi:</strong> CC0 hanya berlaku pada catatan metadata Figshare ini. Berkas "
        "edisi yang ditautkan tidak berlisensi CC0. Teks sumber dan adaptasi Indonesia berada di bawah "
        "CC BY-SA 4.0; media mempertahankan pencipta, sumber, dan lisensi komponennya masing-masing. "
        "Karena akun Figshare ini tidak menawarkan CC BY-SA atau lisensi campuran yang dapat menyatakan "
        "hak berkas dengan tepat, tidak ada byte edisi yang diunggah di sini.</p>"
        "<p>HTML adalah permukaan akses utama dan semantik; PDF tidak diklaim sebagai PDF bertag. Edisi "
        "ini merupakan adaptasi independen dan tidak disahkan oleh Holger Brenner, Universitas Osnabrück, "
        "Wikiversity, Wikimedia Commons, atau Wikimedia Foundation. Terjemahan, reflow, backend, dan QA "
        "dibuat atas arahan pengguna dengan OpenAI Codex gpt-5.6-sol, Ultra. Model bukan penulis karya.</p>"
    )


_original_metadata = figshare.metadata


def metadata() -> dict:
    value = dict(_original_metadata())
    value["description"] = description()
    return value


figshare.description = description
figshare.metadata = metadata


def main() -> None:
    figshare.main()
    # The inherited helper writes a structurally valid receipt; normalize its
    # boundary fields to the Unit 8 transaction and re-read the exact JSON.
    receipt_path = figshare.RECEIPT
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["reader_boundary"]["through_unit"] = 8
    receipt["reader_boundary"]["zenodo_version_doi"] = figshare.ZENODO_VERSION
    receipt["reader_boundary"]["zenodo_concept_doi"] = figshare.ZENODO_CONCEPT
    receipt["provenance"] = "OpenAI Codex gpt-5.6-sol, Ultra."
    receipt["metadata_cleanliness"] = {
        "title_has_organization_prefix": False,
        "description_has_organization_prefix": False,
        "organization_token_count": 0,
        "ai_provenance_disclosed": True,
    }
    text = json.dumps(receipt, ensure_ascii=False, indent=2) + "\n"
    if "TTP" in text:
        raise RuntimeError("TTP leaked into Figshare metadata receipt")
    receipt_path.write_text(text, encoding="utf-8")
    json.loads(receipt_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
