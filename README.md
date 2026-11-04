# Kurva Aljabar dan Bundel, Berkas, dan Kohomologi: terjemahan Bahasa Indonesia kursus Holger Brenner

Terjemahan Bahasa Indonesia yang lengkap dari dua kursus Wikiversity Jerman karya Holger Brenner: *Algebraische
Kurven* (30 unit; Unit 1–23 dari kursus Osnabrück 2025–2026, Unit 24–30 dari kuliah dan lembar kerja Osnabrück 2012)
dan *Bündel, Garben und Kohomologie* (30 unit, Osnabrück 2019–2020), sebagai pembaca HTML, PDF A4, sumber, dan backend
stabil. Repositori ini juga memuat edisi bahasa Inggris kedua kursus.

[Baca Kurva Aljabar](https://kokunoyumeto.github.io/algebraic-geometry-bridge-id/) · [Baca Bundel, Berkas, dan Kohomologi](https://kokunoyumeto.github.io/algebraic-geometry-bridge-id/bgk/) · [English edition](https://kokunoyumeto.github.io/algebraic-geometry-bridge-id/en/)

## Cara pembuatan

Terjemahan dan penataan ulang dikerjakan oleh AI: OpenAI Codex gpt-5.6-sol, Ultra. Revisi kuliah dan lembar kerja,
transklusi, urutan soal, solusi publik, dan PDF resmi sumber dibekukan di `authority/wikiversity/` dan
`authority/wikiversity-bgk/`; hak setiap posisi media dicatat di `authority/RIGHTS*.csv`, sedangkan adaptasi, koreksi,
dan keputusan istilah dicatat di [`00_control/CORRECTIONS.csv`](00_control/CORRECTIONS.csv) dan
[`00_control/TERMINOLOGY.csv`](00_control/TERMINOLOGY.csv). Pemeriksaan merasterkan seluruh 504 halaman Kurva Aljabar
dan 380 halaman BGK, menguji kedua pembaca di desktop dan telepon (matematika, tautan internal, teks alternatif, jalur
aset, log konsol), dan memutar ulang backend secara ganda; hasilnya ada di [`qa/`](qa/).

## Status

Kedua volume lengkap. Kurva Aljabar: 30/30 unit, seluruh 693 soal, 122 solusi publik, 101 posisi media, PDF 504 halaman,
backend 22.752 rekaman. Bundel, Berkas, dan Kohomologi: 30/30 unit, seluruh 495 soal, 25 solusi publik yang tersedia di
sumber (solusi yang tidak tersedia tidak diciptakan), PDF 380 halaman, backend 21.686 rekaman. Lapisan pendamping
orisinal (jembatan skema dan kohomologi, latihan penguasaan, masalah integratif, dan tugas akhir) belum ada dalam
Bahasa Indonesia; edisi bahasa Inggris memuat pendamping orisinal *From Varieties to Schemes*. PDF tidak bertag; HTML
adalah permukaan akses utama. Masih mungkin ada kesalahan.

## Isi

- Rilis [unit-30](https://github.com/KokunoYumeto/algebraic-geometry-bridge-id/releases/tag/unit-30) (Kurva Aljabar lengkap: PDF, HTML, sumber, saksi sumber),
  [bgk-unit-30](https://github.com/KokunoYumeto/algebraic-geometry-bridge-id/releases/tag/bgk-unit-30) (Bundel, Berkas, dan Kohomologi lengkap: PDF, HTML, sumber, backend), dan
  [en-v1.0.0](https://github.com/KokunoYumeto/algebraic-geometry-bridge-id/releases/tag/en-v1.0.0) (edisi bahasa Inggris: kedua volume, pendamping *From Varieties to Schemes*, sumber,
  backend); checkpoint yang lebih awal tetap tersedia di [rilis GitHub](https://github.com/KokunoYumeto/algebraic-geometry-bridge-id/releases).
- `build/reader-id/` dan `build/reader-bgk-id/`: pembaca HTML mandiri dan PDF A4 kedua volume; `docs/`: situs Pages.
- `authority/`, `backend/`, `qa/`, `00_control/`, `scripts/`, `source/`: sumber yang dibekukan, backend, pemeriksaan,
  kontrol, skrip, dan sumber terjemahan.

Bangun dan periksa ulang dengan Python 3, Pandoc 3.9+, LuaLaTeX, Poppler, ImageMagick, `pypdf`, `Pillow`, dan
`jsonschema`:

```powershell
python scripts/build_reader.py --through 30
python scripts/qa_reader_units_01_30.py
python scripts/qa_protected_surfaces_unit_30.py
python scripts/export_backend_units_01_30.py
python scripts/qa_backend_units_01_30.py
python scripts/generate_common_backend_v1_receipts.py --native-backend backend/units-01-30 --preflight
python scripts/build_bgk_reader.py --through 30
python scripts/qa_bgk_reader_general.py --through 30
python scripts/export_backend_bgk_units_01_30.py
python scripts/qa_backend_bgk_units_01_30.py
python scripts/qa_common_backend_bgk_units_01_30.py
python scripts/generate_common_backend_v1_receipts.py --native-backend backend/bgk-units-01-30 --preflight
python scripts/apply_federated_reader_navigation.py --apply --report qa/FEDERATED_NAVIGATION_QA.json
python scripts/apply_federated_reader_navigation.py --check
```

Setelah setiap penyegaran `docs/**/*.html`, jalankan gerbang navigasi
(`scripts/apply_federated_reader_navigation.py --check`); berkas HTML yang belum terdaftar di
`source/federated-navigation/d100-reader-navigation-v1.json` membuat pemeriksaan gagal.

## Sumber dan atribusi

- Holger Brenner, [*Algebraische Kurven (Osnabrück 2025-2026)*](https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_%28Osnabr%C3%BCck_2025-2026%29),
  [*Algebraische Kurven (Osnabrück 2012)*](https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_%28Osnabr%C3%BCck_2012%29)
  dan [*Bündel, Garben und Kohomologie (Osnabrück 2019-2020)*](https://de.wikiversity.org/wiki/Kurs:B%C3%BCndel,_Garben_und_Kohomologie_%28Osnabr%C3%BCck_2019-2020%29),
  Wikiversity Jerman, beserta kontributor sumber dan pencipta media yang dicatat di `authority/`.
- Edisi ini bukan terbitan resmi Holger Brenner, Universitas Osnabrück, Wikiversity, atau Wikimedia Foundation dan tidak
  menyiratkan dukungan mereka.

## Lisensi

Teks sumber dan terjemahannya tersedia menurut CC BY-SA 4.0. Saksi PDF resmi Unit 24–30 mempertahankan pemberitahuan
CC BY-SA 4.0 dan CC BY-SA 2.0 Germany; media pihak ketiga mempertahankan pencipta, sumber, dan lisensinya masing-masing;
skrip berlisensi MIT. Lihat [LICENSE.md](LICENSE.md).
