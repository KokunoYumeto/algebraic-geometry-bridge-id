# Kurva Aljabar - Edisi Bahasa Indonesia

Edisi Bahasa Indonesia independen dari *Algebraische Kurven* karya Holger
Brenner. Unit 1-23 mengikuti kursus resmi *Osnabrück 2025-2026*. Karena kursus
itu berakhir pada Unit 23, Unit 24 mengikuti kuliah dan lembar kerja resmi
*Osnabrück 2012*. Nama repositori berakhiran `-id`, dokumen menyatakan bahasa
`id-ID`, dan judul kerja dipertahankan agar edisi serta bahasanya mudah
ditemukan.

Status saat ini: **checkpoint kumulatif Unit 1-24 lengkap dan terverifikasi**.
Checkpoint ini memuat 24 kuliah, 24 lembar kerja dengan seluruh 622 soal, semua
114 solusi publik yang tersedia pada revisi sumber yang dibekukan, 83 posisi
media beserta atribusi per komponen, HTML mandiri, PDF A4 417 halaman, dan
backend ID stabil dengan 18.488 rekaman. Edisi klasik yang direncanakan terdiri
atas 30 unit; Unit 25 adalah batas produksi berikutnya.

## Baca

- [Pembaca web di GitHub Pages](https://kokunoyumeto.github.io/algebraic-geometry-bridge-id/)
- [Repositori edisi dan bahasa ini](https://github.com/KokunoYumeto/algebraic-geometry-bridge-id)
- [Checkpoint Unit 24 di Zenodo](https://doi.org/10.5281/zenodo.22102097)
- [Konsep Zenodo yang memuat semua versi](https://doi.org/10.5281/zenodo.22059686)
- `build/reader-id/index.html`: pembaca HTML kumulatif mandiri
- `build/reader-id/algebraic-geometry-bridge-id-units-01-24.pdf`: PDF A4 kumulatif
- [Sumber resmi 2025-2026 di Wikiversity](https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026))
- [Sumber resmi 2012 di Wikiversity](https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2012))

HTML adalah permukaan akses utama: dokumen menyatakan `id-ID`, memakai struktur
judul semantik, teks alternatif pada semua 83 gambar, 9.514 simpul MathML,
tautan internal yang lengkap, dan reflow seluler tanpa luapan halaman. Semua
153 rumus yang lebar pada lebar telepon dapat digulir secara lokal. PDF adalah
permukaan cetak dan tidak diklaim sebagai PDF bertag.

## Otoritas dan reproduksibilitas

- `authority/wikiversity/unit-01` sampai `unit-24` mengikat revisi kuliah dan
  lembar kerja, seluruh transklusi, peta urutan soal, solusi publik, serta PDF
  resmi yang dipakai sebagai saksi build.
- `authority/RIGHTS.csv` dan `authority/RIGHTS-unit-02.csv` sampai
  `authority/RIGHTS-unit-24.csv` memisahkan hak setiap posisi media dan aset.
- [`build/reader-id/BUILD_RECEIPT.json`](build/reader-id/BUILD_RECEIPT.json)
  mengikat seluruh masukan dan keluaran pembaca.
- [`qa/UNITS_01_24_MACHINE_QA.json`](qa/UNITS_01_24_MACHINE_QA.json),
  [`qa/UNITS_01_24_VISUAL_QA.json`](qa/UNITS_01_24_VISUAL_QA.json),
  [`qa/UNITS_01_24_VISUAL_PAGE_MANIFEST.json`](qa/UNITS_01_24_VISUAL_PAGE_MANIFEST.json),
  [`qa/UNITS_01_24_RESPONSIVE_QA.json`](qa/UNITS_01_24_RESPONSIVE_QA.json), dan
  [`qa/UNIT_24_PROTECTED_SURFACES.json`](qa/UNIT_24_PROTECTED_SURFACES.json)
  merekam gerbang pembaca, semua 417 raster halaman, reflow desktop/seluler,
  matematika, struktur soal-solusi, hak, serta koreksi terlacak.
- [`backend/units-01-24/MANIFEST.json`](backend/units-01-24/MANIFEST.json)
  mengikat 18.488 rekaman deterministik; seluruh 16.114 rekaman baseline Unit
  1-21 dipertahankan byte demi byte.
- [`qa/UNITS_01_24_BACKEND_QA.json`](qa/UNITS_01_24_BACKEND_QA.json) mengikat
  replay backend ganda, sedangkan
  [`backend/common-backend-v1/MIGRATION_RECEIPT.json`](backend/common-backend-v1/MIGRATION_RECEIPT.json)
  merekam adaptor virtual aditif tanpa mengganti backend asli atau pembaca.
- [`00_control/CORRECTIONS.csv`](00_control/CORRECTIONS.csv) dan
  [`00_control/TERMINOLOGY.csv`](00_control/TERMINOLOGY.csv) membuat adaptasi,
  koreksi, dan keputusan istilah dapat diaudit.

Bangun dan periksa ulang dengan Python 3, Pandoc 3.9+, LuaLaTeX, Poppler,
ImageMagick, `pypdf`, `Pillow`, dan `jsonschema`:

```powershell
python scripts/build_reader.py --through 24
python scripts/qa_reader_units_01_24.py
python scripts/qa_protected_surfaces_units_22_24.py
python scripts/export_backend_units_01_24.py
python scripts/qa_backend_units_01_24.py
python scripts/generate_common_backend_v1_receipts.py --native-backend backend/units-01-24 --preflight
```

Gerbang visual merasterkan seluruh 417 halaman, mengikat setiap PNG menurut
ukuran dan SHA-256, lalu memeriksa 21 lembar kontak dan halaman berisiko pada
resolusi penuh. Gerbang browser menguji lebar desktop 1.440 px dan telepon 390
px, 83/83 gambar, 9.514 simpul MathML, 1.380 tautan internal, luapan lokal
rumus, jalur aset panjang, serta log konsol.

## Hubungan, perubahan, dan hak

Edisi ini menerjemahkan dan menata ulang materi sumber. Ini bukan terbitan
resmi Holger Brenner, Universitas Osnabrück, Wikiversity, Wikimedia Foundation,
atau pihak lain, dan tidak menyiratkan dukungan mereka. Produksi dibantu oleh
**OpenAI Codex gpt-5.6-sol, Ultra.** Pekerjaan dilakukan atas arahan pengguna;
provenance alat tidak menggantikan kredit Holger Brenner, kontributor sumber,
atau kontributor manusia.

Teks sumber dan terjemahan berada di bawah CC BY-SA 4.0. Saksi PDF resmi Unit
24 mempertahankan pemberitahuan komponen jalur kursus CC BY-SA 4.0 dan berkas
CC BY-SA 2.0 Germany. Media pihak ketiga mempertahankan pencipta, sumber, dan
lisensi komponennya masing-masing; tidak ada klaim lisensi tunggal untuk
seluruh payload campuran. Lisensi MIT untuk skrip tidak melisensikan ulang
teks, saksi sumber, atau media. Lihat [LICENSE.md](LICENSE.md) untuk pemisahan
hak yang mengikat.
