# QA terminologi Indonesia: geometri aljabar dan aljabar komutatif

Tanggal pemeriksaan: 2026-08-22  
Cakupan terjemahan: `source/id-ID` Unit 1-7 dan `00_control/TERMINOLOGY.csv` pada snapshot yang dicatat di `SOURCE_MANIFEST.json`.

## Hasil singkat

Pemeriksaan ini menemukan satu koreksi yang cukup kuat untuk diterapkan ke edisi: istilah **field** sebaiknya diubah dari **medan** menjadi **lapangan**. Artikel Indonesia yang paling dekat dengan bidang buku ini memakai *lapangan* 34 kali dan tidak memakai *medan*; artikel pendamping tentang gelanggang polinomial juga memakai *lapangan* 8 kali dan tidak memakai *medan*. Snapshot terjemahan memakai *medan* 117 kali dalam 18 berkas dan tidak memakai *lapangan*.

Istilah lain yang diperiksa pada umumnya sudah baik: **gelanggang**, **ideal prima**, **afin**, **kurva aljabar**, **lokus nol** (dengan alias *himpunan nol*), **tak tereduksi**, **parametrisasi rasional**, **irisan kerucut**, dan **kuadrik**. Bukti dan batas evidensinya dijelaskan di bawah. Saya tidak mengubah berkas terjemahan atau glosarium karena subtask ini hanya diberi batas tulis pada direktori bukti ini.

## Pencarian arXiv yang dibatasi

Pencarian dilakukan pada halaman pencarian resmi arXiv dan API resmi arXiv, bukan pada salinan pihak ketiga. Ini adalah pencarian terbatas, bukan klaim bahwa arXiv sama sekali tidak memiliki teks Indonesia.

- `all: aljabar`: 7 hasil; semuanya merupakan kecocokan tidak relevan, terutama nama keluarga **Aljabar**, dengan judul dan abstrak bukan bahasa Indonesia.
- `all: gelanggang`: 0 hasil.
- Frasa tepat `"kurva aljabar"`, `"kurva hipereliptik"`, `"ideal prima"`, dan `"varietas afin"`: masing-masing 0 hasil.
- `all: polinomial`: 48 hasil luas, tetapi halaman hasil tidak memuat `Indonesia`, `Bahasa`, atau `Kurva`; pemeriksaan metadata menunjukkan kecocokan non-Indonesia dan pemakaian ejaan tersebut dalam bahasa lain/abstrak Inggris.
- Permintaan `lapangan` dan `"geometri aljabar"`, serta endpoint API, berulang kali mendapat HTTP 429 dan karena itu tidak dihitung sebagai hasil nol.

Tidak ditemukan kandidat Indonesia yang layak dan mempunyai paket sumber/e-print TeX dalam batas pencarian tersebut. Karena tidak ada kandidat, tidak ada paket TeX arXiv yang dapat diunduh tanpa mengarang bukti. Pemeriksaan beralih secara jujur ke PDF primer Indonesia.

## Sumber fallback primer

### Sumber utama: kurva aljabar

S. Nurmalasari, S. Guritman, dan B. P. Silalahi, “Penyusunan Algoritme Operasi Grup yang Dibangkitkan oleh Kurva Hipereliptik ... atas Lapangan F2^97,” *Journal of Mathematics and Its Applications* 16(2), 2017, hlm. 13-26, DOI `10.29244/jmap.16.2.13-26`.

Ini merupakan sumber yang paling representatif karena membahas langsung kurva hipereliptik sebagai kurva aljabar di atas lapangan hingga. PDF 14 halaman diperiksa seluruhnya melalui render dan ekstraksi teks. Catatan artikel/PDF tidak menyatakan lisensi Creative Commons tertentu. Kebijakan jurnal saat ini menyatakan akses terbuka dan hak baca/unduh/salin/distribusi/cetak/cari/taut, tetapi laporan ini tidak menganggap kebijakan saat ini sebagai lisensi CC retroaktif.

### Sumber pendamping: aljabar komutatif

Qharnida Khariani, Amir Kamal Amir, dan Nur Erawaty, “Ideal Prima dan Ideal Maksimal pada Gelanggang Polinomial,” *Jurnal Matematika, Statistika dan Komputasi* 11(1), hlm. 71-76, DOI `10.20956/jmsk.v11i1.3431`. PDF/nomor jurnal bertanggal Juli 2014; catatan OJS menampilkan tanggal publikasi 2018-02-01.

PDF 6 halaman diperiksa seluruhnya. Catatan artikel OJS secara spesifik menyebut CC BY 4.0, sedangkan footer situs yang sama menyebut CC BY-NC 4.0. Konflik metadata lisensi tersebut dicatat apa adanya; tidak ada isi sumber yang diterbitkan ulang di sini selain istilah pendek untuk analisis terminologi.

## Perbandingan istilah

Hitungan di kolom “edisi” berasal dari seluruh 21 berkas Unit 1-7; hitungan sumber berasal dari hasil ekstraksi PDF yang tersimpan berdampingan.

| Konsep | Edisi sekarang | IPB | Unhas | Keputusan |
|---|---:|---:|---:|---|
| field: `medan` | 117 | 0 | 0 | Ganti dengan `lapangan`. |
| field: `lapangan` | 0 | 34 | 8 | Bentuk pilihan yang didukung langsung. |
| ring: `gelanggang` | 116 | 0 | 30 | Pertahankan; sumber pendamping tidak memakai `cincin`. |
| prime ideal: `ideal prima` | 21 | 0 | 24 | Pertahankan. |
| maximal ideal: `ideal maksimal` | 4 | 0 | 38 | Pertahankan. |
| algebraic curve: `kurva aljabar` | 39 | 1 | 0 | Pertahankan; cocok tepat dengan sumber utama. |
| irreducible: `tak tereduksi` | 51 | 0 | 16 | Pertahankan; IPB memakai varian `tak teruraikan` sekali, tetapi Unhas memberi dukungan jauh lebih kuat dan bentuk sekarang konsisten dengan `tereduksi`. |
| polynomial adjective: `polinomial` | 80 | 7 | 9 | Pertahankan, khususnya `gelanggang polinomial`. |
| polynomial noun: `polinom` | 225 | 0 | 0 | Pertahankan sebagai pembedaan nomina/adjektiva yang konsisten; kedua artikel memakai `polinomial` lebih luas, tetapi itu tidak membuat bentuk sekarang salah. |
| affine: `afin` | 167 | 0 | 0 | Pertahankan secara provisional; kedua PDF tidak menguji istilah ini dan arXiv exact-phrase search tidak menghasilkan sumber. |
| zero locus: `lokus nol` / `himpunan nol` | 55 / 18 | 0 / 0 | 0 / 0 | Pertahankan; tidak ada bukti baru yang membenarkan penggantian dengan `himpunan akar`. |
| rational parametrization: `parametrisasi rasional` | 12 | 0 | 0 | Pertahankan secara provisional untuk konsistensi matematis dan morfologis. |
| conic: `irisan kerucut` | 21 | 0 | 0 | Pertahankan; jangan ganti dengan `konik` tanpa bukti bidang yang lebih kuat. |
| quadric: `kuadrik` | 58 | 0 | 0 | Pertahankan dan bedakan dari `bentuk kuadratik`. |

Sumber IPB juga memakai **ketertutupan aljabar** untuk objek algebraic closure, sedangkan edisi sejauh ini hanya memerlukan sifat **tertutup secara aljabar**. Jika nomina itu muncul kelak, `ketertutupan aljabar` layak dimasukkan ke glosarium sebagai bentuk berbukti, tanpa mengubah sifat `tertutup secara aljabar`.

## Perubahan yang direkomendasikan untuk lane induk

1. Ubah entri glosarium `Grundkörper` dari `medan dasar` menjadi `lapangan dasar`, dan ubah seluruh pemakaian mandiri `medan` menjadi `lapangan` pada Unit 1-7.
2. Propagasikan perubahan majemuk secara sadar: `medan pecahan` -> `lapangan pecahan`, `medan fungsi rasional` -> `lapangan fungsi rasional`, dan `perluasan medan` -> `perluasan lapangan`; jangan melakukan penggantian buta di URL atau penanda sumber.
3. Tambahkan entri glosarium Unit 7: `Kegelschnitt` -> `irisan kerucut`, `Quadrik` -> `kuadrik`, dan `quadratische Form` -> `bentuk kuadratik`.
4. Tambahkan entri provisional `algebraic closure` -> `ketertutupan aljabar` ketika konsep nomina pertama kali muncul.
5. Setelah propagasi, jalankan kembali QA istilah, build PDF/HTML, pemeriksaan tautan/ID, dan QA visual sebelum checkpoint publik berikutnya.
6. Catatan provenance edisi/release harus memuat tepat: **OpenAI Codex gpt-5.6-sol, Ultra.** Semua kredit sumber, penulis, dan kontributor manusia tetap dipertahankan.

## Berkas terdampak oleh `medan`

`lecture-01.md`, `lecture-02.md`, `lecture-03.md`, `lecture-04.md`, `lecture-05.md`, `lecture-06.md`, `lecture-07.md`, `worksheet-01.md`, `worksheet-01-solutions.md`, `worksheet-02.md`, `worksheet-02-solutions.md`, `worksheet-03.md`, `worksheet-04.md`, `worksheet-04-solutions.md`, `worksheet-05.md`, `worksheet-05-solutions.md`, `worksheet-06.md`, dan `worksheet-07.md`.

Jumlah snapshot: 117 kemunculan pada 18 berkas. `worksheet-03-solutions.md`, `worksheet-06-solutions.md`, dan `worksheet-07-solutions.md` tidak memuat istilah tersebut pada snapshot.
