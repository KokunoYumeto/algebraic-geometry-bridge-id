---
title: "Lembar Kerja 11 - Nullstellensatz Hilbert dan Gelanggang Koordinat"
stable_id: br-ak-2025-2026-w11
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Arbeitsblatt 11"
upstream_pageid: 165930
upstream_revid: 1062657
upstream_timestamp: "2025-12-19T12:03:06Z"
upstream_mediawiki_sha1: 1b95cc02cb9d0260971c1fa369afc8969fa13262
source_url: "https://de.wikiversity.org/w/index.php?oldid=1062657"
authority_manifest: authority/wikiversity/unit-11/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: ea2d4936bb27e88b2863f8fecbddd5570992c432aee66c72066597709da65a47
worksheet_xml_sha256: 89a6af1d88b9e07bf99fc5dc6a97d739aab9bc8094a7d9feb70cd3ab681841c4
worksheet_expanded_tex_sha256: abfaeecd8c9dcb591c8757dca4d28a5f91e1ab1595889380903dc8858dd81eac
exercise_map: authority/wikiversity/unit-11/ORDERED_EXERCISE_MAP.json
exercise_map_sha256: 6298bafd7656e4653b504706b437e89de7faa92a75fac10c31d51ad9644a20cf
license: "CC BY-SA 4.0"
translation_status: complete
---

# Lembar Kerja 11 {#br-ak-2025-2026-w11}

## Soal latihan {#br-ak-2025-2026-w11-practice}

<!-- upstream_entity: Hilbertscher Nullstellensatz/Eindimensional/Direkt/Aufgabe -->

### Soal 11.1 {#br-ak-2025-2026-w11-ex-01}

Misalkan $K$ suatu lapangan yang tertutup secara aljabar. Buktikan
Nullstellensatz Hilbert secara langsung untuk gelanggang polinomial dalam satu
variabel.

<!-- upstream_entity: Hilbertscher Nullstellensatz/Einzelne Funktionen/Radikal/Aufgabe -->

### Soal 11.2 {#br-ak-2025-2026-w11-ex-02}

Misalkan $K$ suatu lapangan yang tertutup secara aljabar dan

$$
f,g\in K[X_1,\ldots,X_n].
$$

Tunjukkan bahwa

$$
V(f)\subseteq V(g)
$$

tepat ketika terdapat bilangan asli $r$ dan
$h\in K[X_1,\ldots,X_n]$ dengan

$$
fh=g^r.
$$

Tinjau juga kasus-kasus khusus ketika $f$, atau ketika $g$, merupakan polinom
konstan.

<!-- upstream_entity: Hilbertscher Nullstellensatz/Korrespondenz/Maximales Ideal/Aufgabe -->

### Soal 11.3 {#br-ak-2025-2026-w11-ex-03}

Tunjukkan bahwa dalam korespondensi yang diberikan oleh Nullstellensatz
Hilbert, titik-titik berkorespondensi dengan ideal-ideal maksimal.

<!-- upstream_entity: Hilbertscher Nullstellensatz/Korrespondenz/Primideal/Fakt/Beweis/Aufgabe -->

### Soal 11.4 {#br-ak-2025-2026-w11-ex-04}

Tunjukkan bahwa dalam korespondensi yang diberikan oleh Nullstellensatz
Hilbert, varietas-varietas tak tereduksi berkorespondensi dengan ideal-ideal
prima.

<!-- upstream_entity: Hilbertscher Nullstellensatz/Nullstellenfrei/Einheit/Aufgabe -->

### Soal 11.5 {#br-ak-2025-2026-w11-ex-05}

Misalkan $K$ suatu lapangan yang tertutup secara aljabar. Buktikan secara
langsung kasus khusus Nullstellensatz Hilbert berikut: jika

$$
f\in K[X_1,\ldots,X_n]
$$

tidak mempunyai akar dalam $K^n$, maka $f$ merupakan polinom konstan yang
tidak nol.

<!-- upstream_entity: Hilbertscher Nullstellensatz/Ebene algebraische Kurven/R und C/1/Aufgabe -->

### Soal 11.6 ★ {#br-ak-2025-2026-w11-ex-06}

Tinjau kedua polinom $X^2+Y^2$ dan $X^2-Y^3$, beserta kurva aljabar yang
bersesuaian di atas lapangan $\mathbb R$ dan $\mathbb C$.

1. Apakah

   $$
   V(X^2+Y^2)\subseteq V(X^2-Y^3)
   $$

   berlaku dalam $\mathbb A_{\mathbb R}^2$?
2. Apakah inklusi yang sama berlaku dalam $\mathbb A_{\mathbb C}^2$?
3. Apakah $X^2-Y^3$ termasuk dalam radikal $(X^2+Y^2)$ di
   $\mathbb R[X,Y]$?
4. Apakah $X^2-Y^3$ termasuk dalam radikal $(X^2+Y^2)$ di
   $\mathbb C[X,Y]$?

<!-- upstream_entity: Hilbertscher Nullstellensatz/C/Linearkombination mit Funktionen/Aufgabe -->

### Soal 11.7 ★ {#br-ak-2025-2026-w11-ex-07}

Misalkan diberikan polinom-polinom

$$
f_1,\ldots,f_k\in\mathbb C[X_1,\ldots,X_n],
$$

yang dipandang sebagai fungsi

$$
f_i:\mathbb C^n\longrightarrow\mathbb C.
$$

Misalkan $f\in\mathbb C[X_1,\ldots,X_n]$ suatu polinom lain, dan misalkan

$$
g_1,\ldots,g_k:\mathbb C^n\longrightarrow\mathbb C
$$

fungsi-fungsi yang tidak harus polinomial. Andaikan berlaku kesamaan fungsi

$$
f=g_1f_1+\cdots+g_kf_k.
$$

Tunjukkan bahwa $f$ termasuk dalam radikal $(f_1,\ldots,f_k)$.

<!-- upstream_entity: Rationale Funktionen/Nullstellenfrei/Ring/Aufgabe -->

### Soal 11.8 {#br-ak-2025-2026-w11-ex-08}

Misalkan $K$ suatu lapangan dan $n\in\mathbb N_+$. Tunjukkan bahwa semua
fungsi $\varphi:K^n\to K$ yang berbentuk

$$
\varphi=\frac{P}{Q},
$$

dengan $P,Q\in K[X_1,\ldots,X_n]$ dan $Q$ tidak mempunyai akar pada $K^n$,
membentuk suatu gelanggang komutatif. Tunjukkan bahwa jika $K$ tertutup secara
aljabar, gelanggang ini sama dengan gelanggang polinomial.

<!-- upstream_entity: Hilbertscher Nullstellensatz/Endlicher Körper/Nullstellen und Radikale/Aufgabe -->

### Soal 11.9 {#br-ak-2025-2026-w11-ex-09}

Misalkan $K$ suatu lapangan berhingga. Tunjukkan bahwa hanya terdapat hingga
banyak lokus nol dalam $\mathbb A_K^n$, tetapi terdapat takhingga banyak ideal
radikal dalam $K[X_1,\ldots,X_n]$.

<!-- upstream_entity: Kommutative Ringtheorie/Einheitsideal/Endlich viele Erzeuger/Aufgabe -->

### Soal 11.10 {#br-ak-2025-2026-w11-ex-10}

Misalkan $R$ suatu gelanggang komutatif dan $f_j$, $j\in J$, suatu keluarga
unsur dalam $R$. Andaikan semua $f_j$ bersama-sama membangkitkan ideal satuan.
Tunjukkan bahwa terdapat subkeluarga berhingga

$$
f_j,\qquad j\in J_0\subseteq J,
$$

yang juga membangkitkan ideal satuan.

<!-- upstream_entity: Affine Varietäten/Affine Äquivalenz/Radikal und Nullstellenmenge/Aufgabe -->

### Soal 11.11 {#br-ak-2025-2026-w11-ex-11}

Misalkan $K$ suatu lapangan yang tertutup secara aljabar dan

$$
\mathfrak a,\mathfrak b\subseteq K[X_1,\ldots,X_n]
$$

ideal-ideal radikal. Tunjukkan bahwa lokus-lokus nol $V(\mathfrak a)$ dan
$V(\mathfrak b)$ ekuivalen secara afin-linear tepat ketika terdapat
transformasi variabel afin-linear yang membawa kedua ideal itu satu ke yang
lain.

### Sisipan: ideal perluasan {#br-ak-2025-2026-w11-note-01}

Misalkan

$$
\varphi:A\longrightarrow B
$$

suatu homomorfisme gelanggang antara gelanggang komutatif $A$ dan $B$. Untuk
suatu ideal $\mathfrak a\subseteq A$, ideal dalam $B$ yang dibangkitkan oleh
$\varphi(\mathfrak a)$ disebut *ideal perluasan* dari $\mathfrak a$ di bawah
$\varphi$. Ideal itu ditulis $\mathfrak aB$. Jika $\varphi$ surjektif, ideal
ini hanyalah ideal citra.

<!-- upstream_entity: Idealzugehörigkeit/Reell/Komplex/Aufgabe -->

### Soal 11.12 {#br-ak-2025-2026-w11-ex-12}

Misalkan

$$
\mathfrak a\subseteq\mathbb R[X_1,\ldots,X_n]
$$

suatu ideal dan $f\in\mathbb R[X_1,\ldots,X_n]$. Tunjukkan bahwa
$f\in\mathfrak a$ tepat ketika

$$
f\in\mathfrak a\mathbb C[X_1,\ldots,X_n]
$$

untuk ideal perluasan tersebut.

<!-- upstream_entity: Ebene algebraische Kurven/Graph von x auf V(xy)/Skizziere/Aufgabe -->

### Soal 11.13 {#br-ak-2025-2026-w11-ex-13}

Buat sketsa grafik fungsi $x$ dan $y$ pada $V(xy)$. Yakinkan diri Anda bahwa
hasil kali $xy$ merupakan fungsi nol.

<!-- upstream_entity: Endliche Punktmenge/Koordinatenring/Aufgabe -->

### Soal 11.14 {#br-ak-2025-2026-w11-ex-14}

Tentukan gelanggang koordinat suatu himpunan aljabar afin
$V\subseteq\mathbb A_K^n$ yang terdiri atas $d$ titik.

<!-- upstream_entity: Affine Ebene/Gerade/Koordinatenring/1/Aufgabe -->

### Soal 11.15 {#br-ak-2025-2026-w11-ex-15}

Tentukan gelanggang koordinat himpunan aljabar afin

$$
V=V(5X-8Y+3)\subseteq\mathbb A_K^2.
$$

<!-- upstream_entity: Affin-algebraische Mengen/Hyperbel/Koordinatenring über Z mod 11/Inverses von 4x^3/Aufgabe -->

### Soal 11.16 {#br-ak-2025-2026-w11-ex-16}

Tinjau hiperbola $V(xy-1)$ di atas lapangan $K=\mathbb Z/(11)$. Tentukan
invers dari $4x^3$ dalam gelanggang koordinat yang bersesuaian.

<!-- upstream_entity: Affin-algebraische Mengen/Inklusion und Koordinatenring/Aufgabe -->

### Soal 11.17 {#br-ak-2025-2026-w11-ex-17}

Misalkan $K$ suatu lapangan dan

$$
V,W\subseteq\mathbb A_K^n
$$

himpunan-himpunan aljabar afin dengan $V\subseteq W$. Definisikan suatu
homomorfisme $K$-aljabar antara kedua gelanggang koordinat $R(V)$ dan $R(W)$,
lalu deskripsikan sifat-sifat terpentingnya. Berikan contoh dua himpunan
aljabar afin yang tidak saling termuat, tetapi gelanggang koordinatnya
isomorfik.

<!-- upstream_entity: Polynomring/Restklassenring/Radikalgleich/Gleiche Radikale/Aufgabe -->

### Soal 11.18 {#br-ak-2025-2026-w11-ex-18}

Misalkan $K$ suatu lapangan dan

$$
\mathfrak a,\mathfrak b\subseteq K[X_1,\ldots,X_n]
$$

ideal-ideal dengan radikal yang sama. Tunjukkan bahwa terdapat bijeksi alami
antara ideal-ideal radikal dalam gelanggang-gelanggang faktor

$$
K[X_1,\ldots,X_n]/\mathfrak a
\qquad\text{dan}\qquad
K[X_1,\ldots,X_n]/\mathfrak b.
$$

<!-- upstream_entity: Koordinatenring/Endlicher Körper/Nicht nur Frobenius Gleichung/Beispiel/Aufgabe -->

### Soal 11.19 {#br-ak-2025-2026-w11-ex-19}

Misalkan $K$ suatu lapangan dengan $q$ unsur dan
$V=V(\mathfrak a)\subseteq\mathbb A_K^n$ suatu himpunan aljabar afin.
Tunjukkan bahwa gelanggang koordinat $V$ tidak harus sama dengan

$$
K[x_1,\ldots,x_n]\big/
\big((x_1^q-x_1,\ldots,x_n^q-x_n)+\mathfrak a\big).
$$

> **Catatan edisi:** Sumber menempatkan $+\mathfrak a$ secara tipografis di
> luar penyebut gelanggang faktor. Tanda kurung di atas membuat pembacaan
> matematis yang dimaksud menjadi eksplisit.

<!-- upstream_entity: Algebraische Raumkurven/Schnitt/Zylinder und Kugel/(x-3)^2+y^2+z^2-7/Realisierung in zwei Variablen/Aufgabe -->

### Soal 11.20 {#br-ak-2025-2026-w11-ex-20}

Misalkan $K$ suatu lapangan berkarakteristik $0$. Tinjau irisan sebuah
silinder dan sebuah bola,

$$
C=V(X^2+Y^2-1)\cap
V((X-3)^2+Y^2+Z^2-7)\subseteq\mathbb A_K^3.
$$

Tunjukkan bahwa gelanggang koordinat $C$ dapat ditulis sebagai gelanggang
faktor dari suatu gelanggang polinomial dalam dua variabel.

## Soal untuk dikumpulkan {#br-ak-2025-2026-w11-submit}

<!-- upstream_entity: Identitätssatz für Polynome/Komplex-analytisch/Aufgabe -->

### Soal 11.21 (4 poin) {#br-ak-2025-2026-w11-ex-21}

Misalkan $F\in\mathbb C[X_1,\ldots,X_n]$ dan
$U\subseteq\mathbb A_{\mathbb C}^n$ suatu subhimpunan yang terbuka dan tak
kosong dalam topologi metrik. Jika $F|_U=0$ sebagai fungsi nol, tunjukkan bahwa
$F$ merupakan polinom nol.

<!-- upstream_entity: Hilberts Nullstellensatz/Algebraisch abgeschlossen/Keine gemeinsame Nullstelle/Dann Einheitsideal/Aufgabe -->

### Soal 11.22 (3 poin) {#br-ak-2025-2026-w11-ex-22}

Buktikan Korolari 11.3 secara langsung dari Teorema 10.10.

<!-- upstream_entity: Hilberts Nullstellensatz/Rabinowich-Trick/Aufgabe -->

### Soal 11.23 (7 poin) {#br-ak-2025-2026-w11-ex-23}

Misalkan $K$ suatu lapangan yang tertutup secara aljabar dan $R$ gelanggang
polinomial dalam $n$ variabel di atas $K$. Kita akan melihat bukti alternatif,
berdasarkan Korolari 11.3, bahwa

$$
\operatorname{Id}(V(J))=\operatorname{rad}(J)
$$

untuk setiap ideal $J$ dalam $R$. Misalkan
$f\in\operatorname{Id}(V(J))$. Tinjau gelanggang $R[T]$ dan tunjukkan bahwa
ideal

$$
J'=(J,1-f\cdot T)
$$

adalah ideal satuan. Simpulkan bahwa $f$ termasuk dalam radikal $J$.

<!-- upstream_entity: Affin-algebraische Mengen/Vergleich von Mengen und ihr Bild im Graph/Aufgabe -->

### Soal 11.24 (3 poin) {#br-ak-2025-2026-w11-ex-24}

Misalkan $F\in K[X_1,\ldots,X_n]$ dan tinjau pemetaan polinomial

$$
\begin{aligned}
\varphi:\mathbb A_K^n&\longrightarrow\mathbb A_K^{n+1},\\
(x_1,\ldots,x_n)&\longmapsto
(x_1,\ldots,x_n,F(x_1,\ldots,x_n)),
\end{aligned}
$$

yang mendefinisikan bijeksi antara ruang afin dan grafik $F$. Untuk suatu
himpunan aljabar afin $V(\mathfrak a)\subseteq\mathbb A_K^n$, tinjau citra
$V'=\varphi(V)$. Tunjukkan bahwa $V'$ juga aljabar afin dan berikan ideal yang
mendeskripsikannya. Tunjukkan bahwa $V$ tak tereduksi tepat ketika $V'$ tak
tereduksi.

<!-- upstream_entity: Ebene algebraische Kurven/Schnitt/x^2+y^2-2 und x^2+2y^2-1/Über Z mod 7/Punkte in Erweiterungskörper/Aufgabe -->

### Soal 11.25 (5 poin) {#br-ak-2025-2026-w11-ex-25}

Tinjau dua kurva aljabar

$$
V(x^2+y^2-2)
\qquad\text{dan}\qquad
V(x^2+2y^2-1)
$$

di atas lapangan $\mathbb Z/(7)$. Tunjukkan bahwa irisannya kosong, lalu
temukan suatu lapangan perluasan $K\supseteq\mathbb Z/(7)$ yang membuat
irisannya tak kosong. Hitung semua titik irisan di atas $K$ dan di atas setiap
lapangan perluasan lainnya. Deskripsikan juga gelanggang koordinat irisan itu.

<!-- upstream_entity: Affine Ebene/Endlich viele Punkte/Beliebige Wertvorgabe/Funktion/Aufgabe -->

### Soal 11.26 (4 poin) {#br-ak-2025-2026-w11-ex-26}

Misalkan $K$ suatu lapangan, dan $P_1,\ldots,P_n$ hingga banyak titik dalam
bidang afin $\mathbb A_K^2$. Misalkan
$a_1,\ldots,a_n\in K$ nilai-nilai sebarang yang telah ditentukan. Tunjukkan
bahwa terdapat polinom $F\in K[X,Y]$ dengan

$$
F(P_i)=a_i\qquad\text{untuk setiap }i=1,\ldots,n.
$$
