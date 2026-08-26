# Kurva Aljabar - Edisi Bahasa Indonesia

Edisi Bahasa Indonesia independen dari *Algebraische Kurven* karya Holger
Brenner. Unit 1–23 mengikuti kursus resmi *Osnabrück 2025–2026*, sedangkan
Unit 24–27 mengikuti kuliah dan lembar kerja resmi *Osnabrück 2012*. Kedua
batas sumber dibekukan dan dilabeli secara terpisah. Nama repositori berakhiran
`-id`, dokumen menyatakan bahasa `id-ID`, dan judul kerja dipertahankan agar
edisi serta bahasanya mudah ditemukan.

Status saat ini: **edisi parsial 27 dari 30 unit; checkpoint kumulatif Unit
1–27 lengkap untuk batas ini dan terverifikasi**. Checkpoint ini memuat 27
kuliah, 27 lembar kerja dengan seluruh 657 soal, semua 117 solusi publik yang
tersedia pada revisi sumber yang dibekukan, 94 posisi media beserta atribusi
per komponen, HTML mandiri, PDF A4 464 halaman, dan backend ID stabil dengan
20.570 rekaman. Tiga unit klasik masih tersisa; Unit 28 adalah batas produksi
berikutnya.

## Baca

- [Pembaca web di GitHub Pages](https://kokunoyumeto.github.io/algebraic-geometry-bridge-id/)
- [Repositori edisi dan bahasa ini](https://github.com/KokunoYumeto/algebraic-geometry-bridge-id)
- [Checkpoint Unit 27 di Zenodo](https://doi.org/10.5281/zenodo.22104692)
- [Konsep Zenodo yang memuat semua versi](https://doi.org/10.5281/zenodo.22059686)
- `build/reader-id/index.html`: pembaca HTML kumulatif mandiri
- `build/reader-id/algebraic-geometry-bridge-id-units-01-27.pdf`: PDF A4 kumulatif
- [Sumber resmi 2025-2026 di Wikiversity](https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026))
- [Sumber resmi 2012 di Wikiversity](https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2012))

HTML adalah permukaan akses utama: dokumen menyatakan `id-ID`, memakai struktur
judul semantik, teks alternatif pada semua 94 gambar, 10.426 simpul MathML,
1.480 tautan internal yang lengkap, dan reflow seluler tanpa luapan halaman.
Semua 170 blok matematika yang lebar pada lebar telepon dapat digulir secara
lokal. PDF adalah permukaan cetak dan tidak diklaim sebagai PDF bertag.

## Otoritas dan reproduksibilitas

- `authority/wikiversity/unit-01` sampai `unit-27` mengikat revisi kuliah dan
  lembar kerja, seluruh transklusi, peta urutan soal, solusi publik, serta PDF
  resmi yang dipakai sebagai saksi build.
- `authority/RIGHTS.csv` dan `authority/RIGHTS-unit-02.csv` sampai
  `authority/RIGHTS-unit-27.csv` memisahkan hak setiap posisi media dan aset.
- [`build/reader-id/BUILD_RECEIPT.json`](build/reader-id/BUILD_RECEIPT.json)
  mengikat seluruh masukan dan keluaran pembaca.
- [`qa/UNITS_01_27_MACHINE_QA.json`](qa/UNITS_01_27_MACHINE_QA.json),
  [`qa/UNITS_01_27_VISUAL_QA.json`](qa/UNITS_01_27_VISUAL_QA.json),
  [`qa/UNITS_01_27_VISUAL_PAGE_MANIFEST.json`](qa/UNITS_01_27_VISUAL_PAGE_MANIFEST.json),
  [`qa/UNITS_01_27_RESPONSIVE_QA.json`](qa/UNITS_01_27_RESPONSIVE_QA.json), dan
  [`qa/UNIT_27_PROTECTED_SURFACES.json`](qa/UNIT_27_PROTECTED_SURFACES.json)
  merekam gerbang pembaca, semua 464 raster halaman, reflow desktop/seluler,
  matematika, struktur soal-solusi, hak, serta koreksi terlacak.
- [`backend/units-01-27/MANIFEST.json`](backend/units-01-27/MANIFEST.json)
  mengikat 20.570 rekaman deterministik; seluruh 18.488 rekaman baseline Unit
  1–24 dipertahankan byte demi byte.
- [`qa/UNITS_01_27_BACKEND_QA.json`](qa/UNITS_01_27_BACKEND_QA.json) mengikat
  replay backend ganda, sedangkan
  [`backend/common-backend-v1/MIGRATION_RECEIPT.json`](backend/common-backend-v1/MIGRATION_RECEIPT.json)
  merekam adaptor virtual aditif tanpa mengganti backend asli atau pembaca.
- [`00_control/CORRECTIONS.csv`](00_control/CORRECTIONS.csv) dan
  [`00_control/TERMINOLOGY.csv`](00_control/TERMINOLOGY.csv) membuat adaptasi,
  koreksi, dan keputusan istilah dapat diaudit.

Bangun dan periksa ulang dengan Python 3, Pandoc 3.9+, LuaLaTeX, Poppler,
ImageMagick, `pypdf`, `Pillow`, dan `jsonschema`:

```powershell
python scripts/build_reader.py --through 27
python scripts/qa_reader_units_01_27.py
python scripts/qa_protected_surfaces_units_25_27.py
python scripts/export_backend_units_01_27.py
python scripts/qa_backend_units_01_27.py
python scripts/generate_common_backend_v1_receipts.py --native-backend backend/units-01-27 --preflight
```

Gerbang visual merasterkan seluruh 464 halaman, mengikat setiap PNG menurut
ukuran dan SHA-256, lalu memeriksa 24 lembar kontak dan halaman berisiko pada
resolusi penuh. Gerbang browser menguji lebar desktop 1.440 px dan telepon 390
px, 94/94 gambar, 10.426 simpul MathML, 1.480 tautan internal, 170 blok
matematika yang dapat digulir secara lokal, jalur aset panjang, serta log konsol.

## Hubungan, perubahan, dan hak

Edisi ini menerjemahkan dan menata ulang materi sumber. Ini bukan terbitan
resmi Holger Brenner, Universitas Osnabrück, Wikiversity, Wikimedia Foundation,
atau pihak lain, dan tidak menyiratkan dukungan mereka. Produksi dibantu oleh
**OpenAI Codex gpt-5.6-sol, Ultra.** Pekerjaan dilakukan atas arahan pengguna;
provenance alat tidak menggantikan kredit Holger Brenner, kontributor sumber,
atau kontributor manusia.

Teks sumber dan terjemahan berada di bawah CC BY-SA 4.0. Saksi PDF resmi Unit
24–27 mempertahankan pemberitahuan komponen jalur kursus CC BY-SA 4.0 dan
berkas CC BY-SA 2.0 Germany. Media pihak ketiga mempertahankan pencipta, sumber, dan
lisensi komponennya masing-masing; tidak ada klaim lisensi tunggal untuk
seluruh payload campuran. Lisensi MIT untuk skrip tidak melisensikan ulang
teks, saksi sumber, atau media. Lihat [LICENSE.md](LICENSE.md) untuk pemisahan
hak yang mengikat.
