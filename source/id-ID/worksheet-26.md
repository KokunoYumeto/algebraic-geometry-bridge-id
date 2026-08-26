---
title: "Lembar Kerja 26 - Multiplisitas Perpotongan"
stable_id: br-ak-2012-w26
language: id-ID
source_course: "Kurs:Algebraische Kurven (Osnabrück 2012)"
source_author: "Holger Brenner"
frozen_revision_contributor: "Arbota"
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2012)/Arbeitsblatt 26"
upstream_pageid: 50761
upstream_revid: 793494
upstream_timestamp: "2022-08-25T06:04:07Z"
upstream_mediawiki_sha1: 10aad7862403732dbaa5a05ae637a084c2758751
source_url: "https://de.wikiversity.org/w/index.php?oldid=793494"
authority_manifest: authority/wikiversity/unit-26/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 981fa3c86534514215c722b6d4f6d711c040a7829465f20ae18940373f94763c
worksheet_xml_sha256: b5cc1634fba66dca202dec1947c17adf55182effecb80e3f298bf597e1535e78
worksheet_expanded_tex_sha256: 2959064d81372593e3a7c619b0753d0be90dde49318262a5995e2b4abccfce71
exercise_map: authority/wikiversity/unit-26/ORDERED_EXERCISE_MAP.json
exercise_map_sha256: efa1d77d8b594a24078097f3595c0ae8078d9735dfe7d2b3abb05392d7340423
license: "CC BY-SA 4.0"
source_component_license_route: "Sumber semantik: CC BY-SA 4.0; PDF historis resmi mempertahankan pemberitahuan CC BY-SA 2.0 Jerman dan CC BY-SA 4.0"
no_blanket_relicensing_claim: true
independent_derivative_non_endorsement: true
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_corrections: 4
correction_ids: "AGC-CORR-0101; AGC-CORR-0103; AGC-CORR-0105; AGC-CORR-0107"
source_discrepancies: 0
reader_media_positions: 0
---

# Lembar Kerja 26 {#br-ak-2012-w26}

## Soal latihan {#br-ak-2012-w26-practice}

<!-- upstream_entity: Ebene algebraische Kurven/Schnittmultiplizität/Schulbeispiel/Aufgabe -->

### Soal 26.1 {#br-ak-2012-w26-ex-01}

Untuk setiap $n$, berikan contoh dua kurva aljabar bidang yang dikenal dari
sekolah dan berpotongan tepat di satu titik dengan multiplisitas perpotongan
$n$.

<!-- upstream_entity: Affine Ebene/y ist 2x^4+3x^2-x+1/(1,5)/Transformation auf Nullpunkt, Tangente auf x-Achse/Aufgabe -->

### Soal 26.2 {#br-ak-2012-w26-ex-02}

Tinjau kurva yang diberikan oleh

$$
y=2x^4+3x^2-x+1
$$

beserta titik

$$
P=(1,5).
$$

Carilah suatu transformasi koordinat sedemikian sehingga $P$ dipetakan ke
$(0,0)$ dan garis singgung di $P$ dipetakan ke sumbu $x$.

<!-- upstream_entity: Ebene monomiale Kurve/Schnittmultiplizität mit Gerade durch Nullpunkt/Aufgabe -->

### Soal 26.3 (3 poin) {#br-ak-2012-w26-ex-03}

Misalkan diberikan kurva monomial bidang

$$
C=V\left(X^d-Y^e\right),
$$

dengan $d$ dan $e$ relatif prima. Hitung multiplisitas perpotongan kurva
tersebut dengan setiap garis $G$ yang melalui titik asal dan bukan komponen
$C$.

> **Catatan edisi - kasus komponen bersama.** Sumber meminta setiap garis
> melalui titik asal. Jika $d=e=1$, kurva $C=V(X-Y)$ sendiri merupakan salah
> satu garis tersebut, dan multiplisitas perpotongan hingga yang didefinisikan
> dalam kuliah tidak tersedia bagi sebuah kurva dengan dirinya sendiri.
> Edisi mengecualikan garis yang merupakan komponen $C$.

<!-- upstream_entity: Kartesisches Blatt/Schnittmultiplizität im Nullpunkt/Mit jeder Geraden/Aufgabe -->

### Soal 26.4 ★ {#br-ak-2012-w26-ex-04}

Tentukan multiplisitas perpotongan di titik asal antara folium Descartes

$$
C=V\left(X^3+Y^3-3XY\right)
$$

dan setiap garis afin di bidang afin. Andaikan karakteristik lapangan bukan
$3$.

## Soal untuk dikumpulkan {#br-ak-2012-w26-submitted}

<!-- upstream_entity: Ebene Kurven/Schnittmultiplizität von x^5-y^2 und x^7-y^3 im Nullpunkt/Aufgabe -->

### Soal 26.5 (4 poin) {#br-ak-2012-w26-ex-05}

Hitung multiplisitas perpotongan kedua kurva monomial

$$
C=V\left(X^5-Y^2\right)
\qquad\text{dan}\qquad
D=V\left(X^7-Y^3\right)
$$

di titik asal.

<!-- upstream_entity: Ebene algebraische Kurven/Schnittmultiplizität/Glatter Punkt auf C/Ordnung von G im Bewertungsring/Aufgabe -->

### Soal 26.6 (4 poin) {#br-ak-2012-w26-ex-06}

Misalkan $K$ suatu lapangan, dan misalkan

$$
C=V(F)
\qquad\text{dan}\qquad
D=V(G)
$$

dua kurva aljabar bidang tanpa komponen bersama. Misalkan

$$
P\in C
$$

suatu titik mulus, sehingga gelanggang lokal

$$
R=K[X,Y]_{\mathfrak m_P}/(F)
$$

merupakan gelanggang valuasi diskret. Tunjukkan bahwa

$$
\operatorname{mult}_P(F,G)=\operatorname{ord}(G),
$$

dengan $\operatorname{ord}$ menyatakan orde citra taknol $G$ di dalam
gelanggang valuasi $R$.

> **Catatan edisi - syarat keterhinggaan.** Sumber tidak menyatakan bahwa
> kedua kurva harus tanpa komponen bersama. Syarat ini, atau secara lokal
> syarat bahwa citra $G$ dalam $R$ taknol, diperlukan agar kedua ruas
> merupakan bilangan berhingga. Edisi menyatakannya secara eksplisit.

<!-- upstream_entity: Ebene Kurven/Parabel und Kreis um (0,r) mit Radius r/Schnitt und Schnittmultiplizität/Aufgabe -->

### Soal 26.7 (4 poin) {#br-ak-2012-w26-ex-07}

Di bidang real, misalkan $r>0$. Tinjau parabola

$$
C=V\left(Y-X^2\right)
$$

dan lingkaran $D$ yang berpusat di $(0,r)$ dan berjari-jari $r$, yaitu

$$
D=V\left(X^2+(Y-r)^2-r^2\right).
$$

Tentukan titik-titik perpotongan $C$ dan $D$ beserta multiplisitas
perpotongannya masing-masing.

> **Catatan edisi - lingkup geometris.** Sumber menyebut pusat dan jari-jari
> tanpa menetapkan lapangan dasar atau syarat pada $r$. Agar "lingkaran
> berjari-jari $r$" mempunyai arti geometris biasa dan tidak merosot menjadi
> sebuah titik, edisi menafsirkan soal ini di atas $\mathbb R$ dengan $r>0$
> serta menuliskan persamaan lingkarannya.

<!-- upstream_entity: Schnittmultiplizität/Einheitshyperbel und Kreis/Restklassenring als Produktring/Aufgabe -->

### Soal 26.8 (4 poin) {#br-ak-2012-w26-ex-08}

Untuk setiap $a\in\mathbb C$, deskripsikan gelanggang hasil bagi

$$
\mathbb C[X,Y]/\left(XY-1,X^2+Y^2-a\right)
$$

sebagai gelanggang produk dari gelanggang-gelanggang lokal. Nyatakan pula
dimensi setiap gelanggang faktor sebagai ruang vektor atas $\mathbb C$.

<!-- upstream_entity: Ebene Kurve/x^3+y^3-3xy+1/Singularitäten und Tangenten über R und C/Aufgabe -->

### Soal 26.9 (4 poin) {#br-ak-2012-w26-ex-09}

Untuk kurva

$$
V\left(X^3+Y^3-3XY+1\right),
$$

tentukan titik-titik singularnya di atas $\mathbb R$ dan di atas
$\mathbb C$. Untuk setiap titik, berikan multiplisitas dan garis-garis
singgungnya.

<!-- upstream_entity: Ebene Kurven/y ist 2x^4+3x^2-x+1/(1,5)/Transformiere und Potenzreihenansatz bis 5/Aufgabe -->

### Soal 26.10 (3 poin) {#br-ak-2012-w26-ex-10}

Tinjau kurva

$$
y=2x^4+3x^2-x+1
$$

di titik

$$
P=(1,5),
$$

dengan koordinat yang ditemukan dalam Soal 26.2. Tentukan deret pangkat bagi
kurva di $P$ sepanjang garis singgung, sampai dengan suku kelima.

Soal berikut tampaknya lebih sulit.

<!-- upstream_entity: Zwei ebene monomiale Kurven/Schnittmultiplizität/Aufgabe -->

### Soal 26.11 (8 poin) {#br-ak-2012-w26-ex-11}

Misalkan diberikan dua kurva monomial bidang yang berbeda,

$$
C=V\left(X^d-Y^e\right)
\qquad\text{dan}\qquad
D=V\left(X^r-Y^s\right),
$$

dengan $d,e$ relatif prima dan $r,s$ relatif prima. Hitung multiplisitas
perpotongan kedua kurva itu di titik asal.

> **Catatan edisi - simbol himpunan nol.** Pada persamaan kedua, sumber
> menulis $D=(X^r-Y^s)$ dan menghilangkan simbol $V$, walaupun teks menyebut
> $D$ sebagai kurva. Edisi memulihkan bentuk yang dimaksud,
> $D=V(X^r-Y^s)$.
