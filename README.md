# Kurva Aljabar — Edisi Bahasa Indonesia

Edisi Bahasa Indonesia independen dari *Algebraische Kurven (Osnabrück
2025–2026)* karya Holger Brenner. Repositori ini sengaja memakai akhiran
`-id`, metadata bahasa `id-ID`, dan judul Bahasa Indonesia agar edisi dan
bahasanya dapat ditemukan langsung.

Status saat ini: **Unit 1–2 lengkap** — dua kuliah, seluruh 55 soal dari dua
lembar kerja, 16 solusi publik yang tersedia pada revisi sumber, 25 posisi
media, atribusi per komponen, HTML mandiri, PDF A4 kumulatif 48 halaman, dan
backend ID stabil dengan 1.466 rekaman. Penerjemahan 30 kuliah dan 30 lembar
kerja tetap berlanjut dalam urutan sumber.

## Baca

- [Pembaca HTML](https://kokunoyumeto.github.io/algebraic-geometry-bridge-id/)
- [PDF kumulatif Unit 1–2](https://kokunoyumeto.github.io/algebraic-geometry-bridge-id/algebraic-geometry-bridge-id-units-01-02.pdf)
- [PDF historis Unit 1](https://kokunoyumeto.github.io/algebraic-geometry-bridge-id/algebraic-geometry-bridge-id-unit-01.pdf)
- [Sumber resmi di Wikiversity](https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026))

HTML adalah permukaan akses utama: dokumen menyatakan `id-ID`, memakai struktur
judul semantik, teks alternatif gambar, dan MathML, serta mempertahankan GIF
animasi. PDF adalah permukaan cetak dan tidak diklaim sebagai PDF bertag.

## Otoritas dan reproduksibilitas

- [`authority/AUTHORITY_FREEZE.md`](authority/AUTHORITY_FREEZE.md) mengikat
  revisi dan penutupan Unit 1; [`authority/UNIT_02_AUTHORITY_FREEZE.md`](authority/UNIT_02_AUTHORITY_FREEZE.md)
  mengikat revisi, transklusi, solusi, PDF resmi, media, dan hash Unit 2.
- [`authority/RIGHTS.csv`](authority/RIGHTS.csv) memisahkan hak setiap media.
- [`build/reader-id/BUILD_RECEIPT.json`](build/reader-id/BUILD_RECEIPT.json)
  mengikat semua input dan kedua keluaran pembaca.
- [`qa/UNITS_01_02_MACHINE_QA.json`](qa/UNITS_01_02_MACHINE_QA.json),
  [`qa/UNITS_01_02_VISUAL_QA.json`](qa/UNITS_01_02_VISUAL_QA.json),
  [`qa/UNIT_02_PROTECTED_SURFACES.json`](qa/UNIT_02_PROTECTED_SURFACES.json),
  dan [`qa/UNITS_01_02_BACKEND_QA.json`](qa/UNITS_01_02_BACKEND_QA.json)
  merekam gerbang QA kumulatif.
- [`backend/units-01-02/MANIFEST.json`](backend/units-01-02/MANIFEST.json)
  mengikat 1.466 rekaman deterministik untuk unit, segmen, latihan, solusi,
  konsep, istilah, aset, hak, koreksi, relasi, QA, dan artefak.

Bangun ulang dengan Python 3, Pandoc 3.9+, LuaLaTeX, dan dependensi Python
`pypandoc`, `pypdf`, serta `jsonschema`:

```powershell
python scripts/build_reader.py --through 2
python scripts/qa_reader_units_01_02.py
python scripts/export_backend_units_01_02.py
python scripts/qa_backend_units_01_02.py
```

Gerbang visual tetap memerlukan pemeriksaan manusia terhadap render halaman;
skrip tidak menggantikan pemeriksaan itu.

## Hubungan, perubahan, dan dukungan

Edisi ini menerjemahkan dan menata ulang materi sumber; edisi ini bukan terbitan
resmi Holger Brenner, Universitas Osnabrück, Wikiversity, Wikimedia Foundation,
atau pihak lain, dan tidak menyiratkan dukungan. Terjemahan disiapkan dengan
bantuan Codex atas arahan pengguna. Koreksi atau adaptasi dicatat terbuka dalam
[`00_control/CORRECTIONS.csv`](00_control/CORRECTIONS.csv); tidak ada koreksi
matematis yang disisipkan diam-diam.

Teks sumber dan terjemahan berada di bawah CC BY-SA 4.0. Media pihak ketiga
mempertahankan lisensi komponennya sendiri. Lihat [LICENSE.md](LICENSE.md) untuk
pemisahan hak yang mengikat.
