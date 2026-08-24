---
title: "Lembar Kerja 9 - Gelanggang Noether, Teorema Basis Hilbert, dan Modul"
stable_id: br-ak-2025-2026-w09
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Arbeitsblatt 9"
upstream_pageid: 165928
upstream_revid: 1059491
upstream_timestamp: "2025-11-21T13:53:14Z"
upstream_mediawiki_sha1: affd5b273368b8a02f7580671dc4b1431f7da9df
source_url: "https://de.wikiversity.org/w/index.php?oldid=1059491"
authority_manifest: authority/wikiversity/unit-09/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 7cf7a956dffe854da9d021e3c74615573b91b5701d7e3b78a8f5f1aa45bfbc29
worksheet_xml_sha256: f38a6617a6a4a10acfa6863eeb99d3ae806385dedb5b6aaa72ba419e9a957196
worksheet_expanded_tex_sha256: af54baf45f10cb1394ac10a2cbf6d9fbf9cb30c113c7166a3751acce8723c7e1
exercise_map: authority/wikiversity/unit-09/ORDERED_EXERCISE_MAP.json
exercise_map_sha256: c906ba0b1073a162f7f55289c0f60114063d011756f1eb907bcf342336729495
license: "CC BY-SA 4.0"
translation_status: complete
---

# Lembar Kerja 9 {#br-ak-2025-2026-w09}

## Soal latihan {#br-ak-2025-2026-w09-practice}

<!-- upstream_entity: Noethersche Ringe/Von endlichen Typ über Z/Beispiel/Aufgabe -->

### Soal 9.1 {#br-ak-2025-2026-w09-ex-01}

Jelaskan mengapa gelanggang

$$
\mathbb Z[X,Y,Z,W]/\left(XY-ZW,\,5X^8-YZ^3+2WXY\right)
$$

merupakan gelanggang Noether.

<!-- upstream_entity: Kommutative Ringe/Idealtheorie/Aufsteigende Kette ist Ideal/Aufgabe -->

### Soal 9.2 {#br-ak-2025-2026-w09-ex-02}

Misalkan $R$ gelanggang komutatif dan

$$
\mathfrak a_1\subseteq\mathfrak a_2\subseteq\mathfrak a_3\subseteq\cdots
$$

rantai naik ideal. Tunjukkan bahwa gabungan

$$
\bigcup_{n\in\mathbb N}\mathfrak a_n
$$

juga merupakan ideal. Berikan contoh sederhana yang menunjukkan bahwa
gabungan ideal-ideal pada umumnya bukan ideal.

<!-- upstream_entity: Noethersche Ringe/Produkt/Aufgabe -->

### Soal 9.3 {#br-ak-2025-2026-w09-ex-03}

Tunjukkan bahwa hasil kali $R\times S$ dari gelanggang Noether $R$ dan $S$
kembali merupakan gelanggang Noether.

<!-- upstream_entity: Polynomring/2 Variablen/Erzeugendensysteme/Aufgabe -->

### Soal 9.4 {#br-ak-2025-2026-w09-ex-04}

Misalkan $K$ suatu lapangan. Tunjukkan bahwa di $K[X,Y]$ tidak ada batas atas
untuk banyaknya pembangkit dalam suatu sistem pembangkit minimal dari ideal-
ideal.

**Petunjuk:** Pertimbangkan pangkat-pangkat $(X,Y)^m$.

<!-- upstream_entity: Polynomring in unendlich vielen Variablen/Nicht noethersch/Kette und Erzeugung/Aufgabe -->

### Soal 9.5 {#br-ak-2025-2026-w09-ex-05}

Misalkan $K$ suatu lapangan dan

$$
K[X_n,\,n\in\mathbb N]
$$

gelanggang polinomial atas $K$ dalam takhingga banyak variabel. Deskripsikan
suatu ideal yang tidak dibangkitkan secara hingga dan suatu rantai ideal naik
sejati tak berhingga di dalamnya.

<!-- upstream_entity: Noetherscher Ring/Unterring/Aufgabe -->

### Soal 9.6 {#br-ak-2025-2026-w09-ex-06}

Tunjukkan bahwa suatu subgelanggang

$$
R\subseteq S
$$

dari gelanggang Noether tidak harus merupakan gelanggang Noether.

<!-- upstream_entity: Nicht-noethersche Ringe/Beispiel/Reduktion ist Körper/Aufgabe -->

### Soal 9.7 {#br-ak-2025-2026-w09-ex-07}

Berikan contoh gelanggang yang bukan Noether tetapi reduksinya merupakan
lapangan.

<!-- upstream_entity: Noetherscher Ring/Ideal und Restklassenring/Aufgabe -->

### Soal 9.8 {#br-ak-2025-2026-w09-ex-08}

Misalkan $R$ gelanggang komutatif dan $\mathfrak a\subset R$ suatu ideal sejati
dengan gelanggang faktor $R/\mathfrak a$. Berikan contoh yang menunjukkan
bahwa $\mathfrak a$ dapat dibangkitkan secara hingga dan $R/\mathfrak a$ dapat
Noether, meskipun $R$ sendiri tidak Noether.

<!-- upstream_entity: Hilbertscher Basissatz/Normiertes Polynom/Idealkette/Aufgabe -->

### Soal 9.9 {#br-ak-2025-2026-w09-ex-09}

Misalkan $R$ gelanggang komutatif dan $\mathfrak b\subseteq R[X]$ suatu ideal
yang memuat setidaknya satu polinom monik. Apa konsekuensinya bagi rantai
ideal di $R$ yang dikonstruksi dalam bukti Teorema Basis Hilbert?

<!-- upstream_entity: Hilbertscher Basissatz/Konstante Idealkette/Aufgabe -->

### Soal 9.10 {#br-ak-2025-2026-w09-ex-10}

Misalkan $R$ gelanggang komutatif. Karakterisasikan ideal-ideal

$$
\mathfrak b\subseteq R[X]
$$

yang mempunyai sifat bahwa rantai ideal di $R$ yang dikonstruksi dalam bukti
Teorema Basis Hilbert bersifat konstan.

<!-- upstream_entity: Hilbertscher Basissatz/Maximales Ideal/Potenzen/Idealkette/Aufgabe -->

### Soal 9.11 {#br-ak-2025-2026-w09-ex-11}

Misalkan $K$ suatu lapangan dan $R=K[X]$ gelanggang polinomial atas $K$.
Untuk ideal-ideal

$$
\mathfrak b_m=(X,Y)^m\subseteq R[Y]=K[X,Y],
$$

tentukan rantai ideal di $R$ yang dikonstruksi dalam bukti Teorema Basis
Hilbert. Kapan rantai tersebut menjadi stasioner?

<!-- upstream_entity: Hilbertscher Basissatz/Z/(6,6x^2+2x+3,3x^3+5,2x^5+x-4,4x^7-3x)/Bestimme Idealkette/Aufgabe -->

### Soal 9.12 {#br-ak-2025-2026-w09-ex-12}

Untuk ideal

$$
I=\left(6,\,6x^2+2x+3,\,3x^3+5,\,2x^5+x-4,\,4x^7-3x\right)
$$

dalam $\mathbb Z[x]$, tentukan rantai ideal yang dikonstruksi dalam bukti
Teorema Basis Hilbert dan sistem pembangkit $I$ yang bersesuaian. Tuliskan
pembangkit-pembangkit di atas sebagai kombinasi linear dari sistem pembangkit
yang dikonstruksi.

<!-- upstream_entity: Endlich erzeugte Algebra/Endliches Teilsystem/Aufgabe -->

### Soal 9.13 {#br-ak-2025-2026-w09-ex-13}

Misalkan $R$ gelanggang komutatif dan $A$ suatu $R$-aljabar komutatif. Misalkan
$A$ dibangkitkan atas $R$ oleh keluarga $a_i\in A$ ($i\in I$). Buktikan bahwa
jika $A$ dibangkitkan secara hingga, maka $A$ juga dibangkitkan oleh suatu
subkeluarga berhingga dari keluarga $a_i$.

<!-- upstream_entity: Affiner Raum/Ab- und Aufsteigungseigenschaften/Endlicher Körper/Länge/Aufgabe -->

### Soal 9.14 {#br-ak-2025-2026-w09-ex-14}

Kita meninjau rantai naik dan turun himpunan aljabar afin di
$\mathbb A_K^n$ serta ideal-ideal di $K[X_1,\ldots,X_n]$. Tunjukkan pernyataan
berikut.

1. Untuk lapangan berhingga, setiap rantai naik

   $$
   V_0\subseteq V_1\subseteq V_2\subseteq\cdots
   $$

   himpunan aljabar afin menjadi stasioner.
2. Untuk lapangan tak berhingga dan $n\geq1$, tidak setiap rantai naik
   himpunan aljabar afin

   $$
   V_0\subseteq V_1\subseteq V_2\subseteq\cdots
   $$

   menjadi stasioner.
3. Untuk lapangan sembarang dan $n\geq1$, tidak setiap rantai turun ideal

   $$
   \mathfrak a_0\supseteq\mathfrak a_1\supseteq\mathfrak a_2\supseteq\cdots
   $$

   menjadi stasioner.
4. Untuk lapangan tak berhingga dan $n\geq1$, terdapat rantai turun sejati
   himpunan aljabar afin dengan panjang sembarang.

<!-- upstream_entity: Reelle Zahlen/Kein noetherscher Raum/Aufgabe -->

### Soal 9.15 {#br-ak-2025-2026-w09-ex-15}

Tunjukkan bahwa himpunan $\mathbb R$ bilangan real dengan topologi metriknya
bukan ruang topologis Noether.

<!-- upstream_entity: Kommutative Algebra/Abelsche Gruppe/Z-Modul/Aufgabe -->

### Soal 9.16 {#br-ak-2025-2026-w09-ex-16}

Misalkan $G$ suatu grup komutatif. Tunjukkan bahwa tepat ada satu cara untuk
memberikan struktur modul-$\mathbb Z$ pada $G$. Jadi grup komutatif dan
modul-$\mathbb Z$ merupakan objek yang ekuivalen.

<!-- upstream_entity: Kommutative Algebren/Moduldefinition und Ringhomomorphismus/Äquivalenz/Aufgabe -->

### Soal 9.17 {#br-ak-2025-2026-w09-ex-17}

Misalkan $R$ dan $A$ gelanggang komutatif. Tunjukkan bahwa $A$ merupakan
$R$-aljabar tepat ketika $A$ merupakan modul-$R$ yang selain itu memenuhi

$$
r(ab)=(ra)b\qquad\text{untuk semua }r\in R,\ a,b\in A.
$$

<!-- upstream_entity: Modul/Kommutativer Ring/Allgemeines Distributivgesetz/Aufgabe -->

### Soal 9.18 {#br-ak-2025-2026-w09-ex-18}

Misalkan $V$ suatu modul atas gelanggang komutatif $R$. Misalkan

$$
s_1,\ldots,s_k\in R\qquad\text{dan}\qquad v_1,\ldots,v_n\in V.
$$

Buktikan bahwa

$$
\left(\sum_{i=1}^k s_i\right)\!\cdot
\left(\sum_{j=1}^n v_j\right)
=\sum_{1\leq i\leq k,\,1\leq j\leq n}s_i\cdot v_j.
$$

<!-- upstream_entity: Lineare Abbildung/Moduln/Bild und Urbild/Untermoduln/Fakt/Beweis/Aufgabe -->

### Soal 9.19 {#br-ak-2025-2026-w09-ex-19}

Misalkan $R$ gelanggang komutatif, $M$ dan $N$ dua modul-$R$, serta
$\varphi:M\to N$ suatu homomorfisme modul. Buktikan pernyataan-pernyataan
berikut.

1. Jika $S\subseteq M$ suatu submodul-$R$, maka citra $\varphi(S)$ merupakan
   submodul dari $N$.
2. Khususnya, citra pemetaan

   $$
   \operatorname{im}\varphi=\varphi(M)
   $$

   merupakan submodul dari $N$.
3. Jika $T\subseteq N$ suatu submodul, maka prapeta

   $$
   \varphi^{-1}(T)
   $$

   merupakan submodul dari $M$.
4. Khususnya, kernel

   $$
   \varphi^{-1}(0)
   $$

   merupakan submodul dari $M$.

## Soal untuk dikumpulkan {#br-ak-2025-2026-w09-submit}

<!-- upstream_entity: Idealtheorie (kommutative Algebra)/Ideale im Restklassenring/Korrespondenz/Aufgabe -->

### Soal 9.20 (3 poin) {#br-ak-2025-2026-w09-ex-20}

Misalkan $R$ gelanggang komutatif dan $\mathfrak a$ suatu ideal dengan
gelanggang faktor

$$
S=R/\mathfrak a.
$$

Tunjukkan bahwa ideal-ideal di $S$ berkorespondensi secara unik dengan
ideal-ideal di $R$ yang memuat $\mathfrak a$. Tunjukkan bahwa pernyataan yang
sama berlaku untuk ideal prima, ideal radikal, dan ideal maksimal.

<!-- upstream_entity: Kommutative Ringtheorie/Noetherscher Bereich/Zerlegung in irreduzible Elemente/Aufgabe -->

### Soal 9.21 (4 poin) {#br-ak-2025-2026-w09-ex-21}

Misalkan $R$ suatu domain integral Noether. Tunjukkan bahwa setiap unsur dari
$R$ dapat ditulis sebagai hasil kali unsur-unsur tak tereduksi.

<!-- upstream_entity: Algebren von endlichem Typ/Q ist nicht über Z/Aufgabe -->

### Soal 9.22 (4 poin) {#br-ak-2025-2026-w09-ex-22}

Tunjukkan bahwa $\mathbb Q$ bukan aljabar tipe hingga atas $\mathbb Z$.

<!-- upstream_entity: Endlich erzeugte Algebra/Zwei Variablen über Körper/Nicht endlich erzeugte Unteralgebra/Finde/Aufgabe -->

### Soal 9.23 (4 poin) {#br-ak-2025-2026-w09-ex-23}

Misalkan $K$ lapangan dan $A=K[X,Y]$. Temukan subaljabar-$K$ dari $A$ yang
tidak dibangkitkan secara hingga.

<!-- upstream_entity: Hilbertscher Basissatz/Z/(10,6x^2+8,4x^3-12)/Bestimme Idealkette/Aufgabe -->

### Soal 9.24 (4 poin) {#br-ak-2025-2026-w09-ex-24}

Untuk ideal

$$
I=\left(10,\,6x^2+8,\,4x^3-12\right)
$$

dalam $\mathbb Z[x]$, tentukan rantai ideal yang dikonstruksi dalam bukti
Teorema Basis Hilbert dan sistem pembangkit $I$ yang bersesuaian. Tuliskan
pembangkit-pembangkit semula sebagai kombinasi linear dari sistem pembangkit
yang dikonstruksi.
