# QA terminologi Indonesia — keputusan Unit 1–7

Tanggal: 2026-08-22  
Status: selesai; migrasi diterapkan; build kumulatif Unit 1–7 harus memakai hasil ini

## Batas pencarian dan sumber

Pencarian terbatas pada halaman pencarian resmi dan API resmi arXiv tidak
menemukan sumber TeX/e-print berbahasa Indonesia yang benar-benar mewakili
geometri aljabar. Hasil HTTP 429 tidak dihitung sebagai hasil nol. Karena itu,
sesuai instruksi, pemeriksaan beralih secara jujur ke dua PDF primer Indonesia:

1. S. Nurmalasari, S. Guritman, dan B. P. Silalahi, “Penyusunan Algoritme
   Operasi Grup yang Dibangkitkan oleh Kurva Hipereliptik ... atas Lapangan
   F_2^97,” DOI `10.29244/jmap.16.2.13-26`. Berkas lokal 408.458 byte,
   SHA-256 `c251f619bf97d0ab5f9a905ee2cc5b5038d2d7425d12d54aca606893e76c1150`.
2. Qharnida Khariani, Amir Kamal Amir, dan Nur Erawaty, “Ideal Prima dan Ideal
   Maksimal pada Gelanggang Polinomial,” DOI `10.20956/jmsk.v11i1.3431`.
   Berkas lokal 307.931 byte, SHA-256
   `18cfdbe1d8cad27eda19a6dab1e9d258ef4f7874407d3746a8cbd6bfbbdef16a`.

PDF pertama tidak menyatakan lisensi CC tertentu. Catatan OJS dan footer untuk
PDF kedua memberi pernyataan CC yang saling bertentangan. Keduanya disimpan
sebagai bukti QA lokal dan tidak dimasukkan ke payload edisi atau diterbitkan
ulang.

Laporan lengkap adalah
`authority/terminology-id-arxiv/TERMINOLOGY_QA_REPORT.md` (7.616 byte,
SHA-256 `379478bd8ad2cfb82a2df22208b51a63c438b1cc0d86bec46d43f7573ed6d1f9`).
Manifest sumber dan snapshot pramigrasi adalah
`authority/terminology-id-arxiv/SOURCE_MANIFEST.json` (10.227 byte, SHA-256
`ee90cac811cf13acb7db45fa067e404b8a474c12518a37d2b693edf8fc133a36`).

## Keputusan

- Ganti `medan` dengan `lapangan`. Sumber kurva aljabar memakai `lapangan` 34
  kali dan tidak memakai `medan`; sumber pendamping memakai `lapangan` 8 kali
  dan tidak memakai `medan`. Migrasi mengubah tepat 117 kemunculan dalam 18
  berkas, termasuk bentuk majemuk seperti `lapangan dasar`, `lapangan pecahan`,
  dan `lapangan fungsi rasional`.
- Ganti `gelanggang hasil bagi` dengan `gelanggang faktor`. Sumber aljabar
  komutatif secara eksplisit memakai `gelanggang faktor` untuk quotient ring.
  Migrasi mengubah tepat 22 kemunculan dalam 10 berkas, termasuk bentuk jamak,
  posesif, dan satu pemenggalan baris; makna matematis tidak berubah.
- Pertahankan `gelanggang`, `ideal prima`, `ideal maksimal`, `afin`, `kurva
  aljabar`, `lokus nol`/`himpunan nol`, `tak tereduksi`, `parametrisasi
  rasional`, `irisan kerucut`, `kuadrik`, serta pembedaan nomina `polinom` dan
  adjektiva `polinomial`.
- Masukkan `Kegelschnitt` → `irisan kerucut`, `Quadrik` → `kuadrik`, dan
  `quadratische Form` → `bentuk kuadratik` sebagai `AGT-0051`–`AGT-0053`.
  Masukkan `algebraischer Abschluss` → `ketertutupan aljabar` sebagai
  `AGT-0054` provisional sampai nomina itu pertama kali diperlukan.

`qa/TERMINOLOGY_MIGRATION_UNIT_07.json` mengikat seluruh hash sebelum/sesudah,
21 berkas yang diperiksa, 19 berkas yang berubah, dan hitungan residu nol;
berkas itu berukuran 8.933 byte dengan SHA-256
`d290dff2d248ece69202ac1ebbe7cb386c280e46ce8f2f868ec6bfdbfba27de3`.
`AGC-ADAPT-0016` merekam perubahan sebagai adaptasi terminologi tanpa perubahan
matematika. Gerbang berikutnya wajib membuktikan bahwa ID, rumus, tautan,
urutan, jumlah soal, dan hubungan solusi tidak berubah.

## Provenance alat

Frontmatter edisi dan README masing-masing memuat identifikasi tepat berikut,
tanpa menggantikan kredit penulis atau kontributor manusia:

**OpenAI Codex gpt-5.6-sol, Ultra.**

