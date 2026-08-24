# Kurva Aljabar - Edisi Bahasa Indonesia

Edisi Bahasa Indonesia independen dari *Algebraische Kurven (Osnabrück
2025-2026)* karya Holger Brenner. Nama repositori berakhiran `-id`, dokumen
menyatakan bahasa `id-ID`, dan judul kerja dipertahankan agar edisi dan
bahasanya mudah ditemukan.

Status saat ini: **checkpoint kumulatif Unit 1-15 lengkap dan terverifikasi**.
Checkpoint ini memuat lima belas kuliah, lima belas lembar kerja dengan seluruh
423 soal, semua 75 solusi publik yang tersedia pada revisi sumber yang
dibekukan, 69 posisi media beserta atribusi per komponen, HTML mandiri, PDF A4
267 halaman, dan backend ID stabil dengan 10.938 rekaman. Edisi klasik yang
direncanakan terdiri atas 30 unit; produksi berikutnya dimulai pada Unit 16.

## Baca

- [Pembaca web di GitHub Pages](https://kokunoyumeto.github.io/algebraic-geometry-bridge-id/)
- [Repositori edisi dan bahasa ini](https://github.com/KokunoYumeto/algebraic-geometry-bridge-id)
- [Checkpoint Unit 15 di Zenodo](https://doi.org/10.5281/zenodo.22077441)
- [Konsep Zenodo yang memuat semua versi](https://doi.org/10.5281/zenodo.22059686)
- `build/reader-id/index.html`: pembaca HTML kumulatif mandiri
- `build/reader-id/algebraic-geometry-bridge-id-units-01-15.pdf`: PDF A4 kumulatif
- [Sumber resmi di Wikiversity](https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026))

HTML adalah permukaan akses utama: dokumen menyatakan `id-ID`, memakai struktur
judul semantik, teks alternatif pada semua 69 gambar, MathML, tautan internal
yang lengkap, dan reflow seluler tanpa luapan halaman. Rumus yang lebar dapat
digulir secara lokal. PDF adalah permukaan cetak dan tidak diklaim sebagai PDF
bertag.

## Otoritas dan reproduksibilitas

- `authority/wikiversity/unit-01` sampai `unit-15` mengikat revisi kuliah dan
  lembar kerja, seluruh transklusi, peta urutan soal, solusi publik, serta PDF
  resmi yang dipakai sebagai saksi build.
- `authority/RIGHTS.csv` dan `authority/RIGHTS-unit-02.csv` sampai
  `authority/RIGHTS-unit-15.csv` memisahkan hak setiap posisi media dan aset.
- [`build/reader-id/BUILD_RECEIPT.json`](build/reader-id/BUILD_RECEIPT.json)
  mengikat seluruh masukan dan keluaran pembaca.
- [`qa/UNITS_01_15_MACHINE_QA.json`](qa/UNITS_01_15_MACHINE_QA.json),
  [`qa/UNITS_01_15_VISUAL_QA.json`](qa/UNITS_01_15_VISUAL_QA.json),
  [`qa/UNITS_01_15_VISUAL_PAGE_MANIFEST.json`](qa/UNITS_01_15_VISUAL_PAGE_MANIFEST.json),
  [`qa/UNITS_01_15_RESPONSIVE_QA.json`](qa/UNITS_01_15_RESPONSIVE_QA.json), dan
  [`qa/UNIT_15_PROTECTED_SURFACES.json`](qa/UNIT_15_PROTECTED_SURFACES.json)
  merekam gerbang pembaca, semua 267 raster halaman, reflow desktop/seluler,
  matematika, struktur soal-solusi, hak, serta koreksi terlacak.
- [`backend/units-01-15/MANIFEST.json`](backend/units-01-15/MANIFEST.json)
  mengikat 10.938 rekaman deterministik; 8.491 rekaman baseline Unit 1-12
  dipertahankan tepat.
- [`qa/UNITS_01_15_BACKEND_QA.json`](qa/UNITS_01_15_BACKEND_QA.json) mengikat
  replay backend ganda, sedangkan
  [`backend/common-backend-v1/MIGRATION_RECEIPT.json`](backend/common-backend-v1/MIGRATION_RECEIPT.json)
  merekam adaptor virtual aditif tanpa mengganti backend asli atau pembaca.
- [`00_control/CORRECTIONS.csv`](00_control/CORRECTIONS.csv) dan
  [`00_control/TERMINOLOGY.csv`](00_control/TERMINOLOGY.csv) membuat adaptasi,
  koreksi, dan keputusan istilah dapat diaudit.

Bangun dan periksa ulang dengan Python 3, Pandoc 3.9+, LuaLaTeX, Poppler,
`pypdf`, `Pillow`, dan `jsonschema`:

```powershell
python scripts/build_reader.py --through 15
python scripts/qa_reader_units_01_15.py
python scripts/qa_protected_surfaces_units_13_15.py
python scripts/export_backend_units_01_15.py
python scripts/qa_backend_units_01_15.py
python scripts/generate_common_backend_v1_receipts.py --native-backend backend/units-01-15 --preflight
```

Gerbang visual merasterkan seluruh 267 halaman, mengikat setiap PNG menurut
ukuran dan SHA-256, lalu memeriksa lembar kontak semua halaman dan halaman yang
terpengaruh pada resolusi penuh. Gerbang browser menguji lebar desktop 1440 px
dan lebar telepon 390 px, 69/69 gambar, 5.989 simpul MathML, tautan internal,
luapan lokal rumus, serta log konsol.

## Hubungan, perubahan, dan hak

Edisi ini menerjemahkan dan menata ulang materi sumber. Ini bukan terbitan
resmi Holger Brenner, Universitas Osnabrück, Wikiversity, Wikimedia Foundation,
atau pihak lain, dan tidak menyiratkan dukungan mereka. Produksi dibantu oleh
**OpenAI Codex gpt-5.6-sol, Ultra.** Pekerjaan dilakukan atas arahan pengguna;
provenance alat tidak menggantikan kredit Holger Brenner, kontributor sumber,
atau kontributor manusia.

Teks sumber dan terjemahan berada di bawah CC BY-SA 4.0. Media pihak ketiga
mempertahankan pencipta, sumber, dan lisensi komponennya masing-masing. Lisensi
MIT untuk skrip tidak melisensikan ulang teks, saksi sumber, atau media. Lihat
[LICENSE.md](LICENSE.md) untuk pemisahan hak yang mengikat.
