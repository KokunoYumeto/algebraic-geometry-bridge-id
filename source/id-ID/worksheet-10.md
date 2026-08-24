---
title: "Lembar Kerja 10 - Modul Noether dan Nullstellensatz Hilbert"
stable_id: br-ak-2025-2026-w10
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Arbeitsblatt 10"
upstream_pageid: 165929
upstream_revid: 1058833
upstream_timestamp: "2025-11-13T14:59:04Z"
upstream_mediawiki_sha1: 48ce873997cecbd45efdceb3a7caa19ae7844876
source_url: "https://de.wikiversity.org/w/index.php?oldid=1058833"
authority_manifest: authority/wikiversity/unit-10/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: f8b4f8bf12a0613f774352df31941d79a35d9eed10f2d8fb5570f9ffe07bfb43
worksheet_xml_sha256: 9a52bae904d62f5f15dbf7f7f8ba2a5470bdb4f706773be0b0419f8096511a00
worksheet_expanded_tex_sha256: 1631c95c639e523ea8d4daa7b4aac9460280f2f7c2a13dab49230980675442d3
exercise_map: authority/wikiversity/unit-10/ORDERED_EXERCISE_MAP.json
exercise_map_sha256: 972e36256d128916533a33be1d2feedfdecbd133a0dbba96193a85477cf7e92c
license: "CC BY-SA 4.0"
translation_status: complete
---

# Lembar Kerja 10 {#br-ak-2025-2026-w10}

## Soal latihan {#br-ak-2025-2026-w10-practice}

<!-- upstream_entity: Endliche Algebra über Körper/Kommutativ/Einheit und Nichtnullteiler/Aufgabe -->

### Soal 10.1 ★ {#br-ak-2025-2026-w10-ex-01}

Misalkan $K$ suatu lapangan dan $A$ suatu aljabar-$K$ komutatif yang hingga
sebagai modul-$K$. Tunjukkan bahwa suatu unsur $f\in A$ merupakan satuan tepat
ketika ia bukan pembagi nol.

<!-- upstream_entity: Endliche Körpererweiterung/Zwischenring/Körper/Aufgabe -->

### Soal 10.2 {#br-ak-2025-2026-w10-ex-02}

Misalkan $K$ dan $L$ lapangan, $K\subseteq L$ suatu perluasan lapangan hingga,
dan $A$ suatu gelanggang antara,

$$
K\subseteq A\subseteq L.
$$

Tunjukkan bahwa $A$ juga merupakan lapangan.

<!-- upstream_entity: Kommutative Ringtheorie/Endliche Erweiterung/Nichteinheit bleibt Nichteinheit/Aufgabe -->

### Soal 10.3 {#br-ak-2025-2026-w10-ex-03}

Misalkan $R\subseteq S$ suatu perluasan gelanggang hingga dan $f\in R$.
Tunjukkan: jika $f$, ketika dipandang sebagai unsur $S$, merupakan satuan,
maka $f$ merupakan satuan di $R$.

<!-- upstream_entity: Kommutativer Ring/Modul/Noethersch und Aufstiegsbedingung/Aufgabe -->

### Soal 10.4 {#br-ak-2025-2026-w10-ex-04}

Misalkan $R$ suatu gelanggang komutatif dan $M$ suatu modul-$R$. Tunjukkan
bahwa $M$ Noether tepat ketika setiap rantai naik submodul-$R$

$$
M_0\subseteq M_1\subseteq M_2\subseteq\cdots
$$

menjadi stasioner.

<!-- upstream_entity: Nichtnullteiler/Kurze exakte Sequenz/Aufgabe -->

### Soal 10.5 {#br-ak-2025-2026-w10-ex-05}

Misalkan $f\in R$ bukan pembagi nol dalam suatu gelanggang komutatif $R$.
Tunjukkan bahwa ini menghasilkan barisan eksak pendek modul-$R$

$$
0\longrightarrow R\xrightarrow{\cdot f}R
\longrightarrow R/(f)\longrightarrow0.
$$

<!-- upstream_entity: Kommutativer Ring/Ideale/Chinesischer Restsatz/Kurze exakte Sequenz/Aufgabe -->

### Soal 10.6 ★ {#br-ak-2025-2026-w10-ex-06}

Misalkan $R$ suatu gelanggang komutatif dan $I,J\subseteq R$ ideal. Tunjukkan
bahwa barisan

$$
0\longrightarrow R/(I\cap J)\longrightarrow R/I\times R/J
\longrightarrow R/(I+J)\longrightarrow0
$$

dengan pemetaan $r\mapsto(r,r)$ dan $(s,t)\mapsto s-t$ adalah eksak.

<!-- upstream_entity: Moduln (kommutative Algebra)/L in M in N/Kurze exakte Sequenz/Aufgabe -->

### Soal 10.7 {#br-ak-2025-2026-w10-ex-07}

Misalkan $R$ suatu gelanggang komutatif dan $N$ suatu modul-$R$ dengan
submodul-submodul-$R$

$$
L\subseteq M\subseteq N.
$$

Tunjukkan bahwa modul-modul faktor tersebut dihubungkan oleh barisan eksak
pendek

$$
0\longrightarrow M/L\longrightarrow N/L
\longrightarrow N/M\longrightarrow0.
$$

<!-- upstream_entity: Modul-Homomorphismus/Exakte Sequenz/Aufgabe -->

### Soal 10.8 {#br-ak-2025-2026-w10-ex-08}

Misalkan $R$ suatu gelanggang komutatif dan

$$
\varphi:M\longrightarrow N
$$

suatu homomorfisme modul-$R$ antara modul-$R$ $M$ dan $N$. Tunjukkan bahwa
ini menghasilkan barisan eksak pendek

$$
0\longrightarrow\operatorname{ker}\varphi\longrightarrow M
\longrightarrow\operatorname{im}\varphi\longrightarrow0.
$$

Misalkan $R$ suatu gelanggang komutatif dan $M$ suatu modul-$R$. Modul-$R$

$$
M^*=\operatorname{Hom}_R(M,R)
$$

disebut *modul dual* dari $M$.

<!-- upstream_entity: Kurze exakte Sequenz/Modul/Duale Sequenz/Aufgabe -->

### Soal 10.9 ★ {#br-ak-2025-2026-w10-ex-09}

Misalkan $R$ suatu gelanggang komutatif dan

$$
0\longrightarrow L\longrightarrow M\longrightarrow N\longrightarrow0
$$

suatu barisan eksak pendek modul-$R$ $L,M,N$. Tunjukkan bahwa ini menghasilkan
barisan eksak modul dual

$$
0\longrightarrow N^*\longrightarrow M^*\longrightarrow L^*.
$$

<!-- upstream_entity: Kurze exakte Sequenz/Vektorraum/Duale Sequenz/Aufgabe -->

### Soal 10.10 {#br-ak-2025-2026-w10-ex-10}

Misalkan $K$ suatu lapangan dan

$$
0\longrightarrow L\longrightarrow M\longrightarrow N\longrightarrow0
$$

suatu barisan eksak pendek ruang vektor-$K$ $L,M,N$. Tunjukkan bahwa ini
menghasilkan barisan eksak pendek ruang dual

$$
0\longrightarrow N^*\longrightarrow M^*\longrightarrow L^*
\longrightarrow0.
$$

<!-- upstream_entity: Kurze exakte Sequenz/Z/Duale Sequenz/Nicht exakt/Aufgabe -->

### Soal 10.11 {#br-ak-2025-2026-w10-ex-11}

Misalkan $a\ne0$ suatu bilangan bulat. Kita meninjau barisan eksak pendek
modul-$\mathbb Z$

$$
0\longrightarrow\mathbb Z\xrightarrow{\cdot a}\mathbb Z
\longrightarrow\mathbb Z/(a)\longrightarrow0.
$$

Tunjukkan bahwa, untuk $a\geq2$, barisan yang eksak menurut Soal 10.9,

$$
0\longrightarrow(\mathbb Z/(a))^*\longrightarrow\mathbb Z^*
\longrightarrow\mathbb Z^*,
$$

tidak dapat diperpanjang secara eksak ke kanan dengan $\longrightarrow0$.

<!-- upstream_entity: Kurze exakte Sequenz/Modul/Erzeugendenzahl/Aufgabe -->

### Soal 10.12 {#br-ak-2025-2026-w10-ex-12}

Misalkan $R$ suatu gelanggang komutatif dan

$$
0\longrightarrow L\longrightarrow M\longrightarrow N\longrightarrow0
$$

suatu barisan eksak pendek modul-$R$. Misalkan $L$ memiliki sistem pembangkit
modul-$R$ dengan $k$ unsur dan $N$ memiliki sistem pembangkit modul-$R$ dengan
$n$ unsur. Tunjukkan bahwa $M$ memiliki sistem pembangkit modul-$R$ dengan
$k+n$ unsur.

<!-- upstream_entity: Endlicher Modul/Endliche Algebra/Endlich/Aufgabe -->

### Soal 10.13 {#br-ak-2025-2026-w10-ex-13}

Misalkan $R$ suatu gelanggang komutatif, $A$ suatu aljabar-$R$ komutatif yang
hingga, dan $M$ suatu modul-$A$ hingga. Tunjukkan bahwa $M$ juga merupakan
modul-$R$ hingga.

Soal-soal berikut menggunakan pengertian modul Artin, yang “dual” terhadap
pengertian modul Noether.

Misalkan $R$ suatu gelanggang komutatif. Modul-$R$ $M$ disebut *Artin* jika
setiap rantai turun submodul-$R$

$$
M_1\supseteq M_2\supseteq M_3\supseteq\cdots
$$

menjadi stasioner. Gelanggang komutatif $R$ disebut *Artin* jika ia Artin
sebagai modul-$R$.

<!-- upstream_entity: Artinsche Ringe/Artinsche Integritätsbereiche sind Körper/Aufgabe -->

### Soal 10.14 {#br-ak-2025-2026-w10-ex-14}

Misalkan $A$ suatu domain integral Artin. Tunjukkan bahwa $A$ merupakan
lapangan. Berikan contoh gelanggang komutatif Artin yang bukan lapangan.

<!-- upstream_entity: Kommutative Algebra/Noethersche bzw. artinsche Moduln/Endomorphismen/Aufgabe -->

### Soal 10.15 {#br-ak-2025-2026-w10-ex-15}

Misalkan $R$ suatu gelanggang komutatif dan $M$ suatu modul-$R$. Tunjukkan:
jika $M$ Artin dan

$$
\phi:M\longrightarrow M
$$

bersifat linear-$R$ dan injektif, maka $\phi$ merupakan isomorfisme.
Rumuskan dan buktikan pula pernyataan analog untuk kasus ketika $M$ Noether.

<!-- upstream_entity: Kommutative Ringtheorie/f nicht nilpotent/Existenz von Primidealen/Fakt/Beweis/Aufgabe -->

### Soal 10.16 ★ {#br-ak-2025-2026-w10-ex-16}

Misalkan $R$ suatu gelanggang komutatif dan $f\in R$ tidak nilpoten. Tunjukkan
bahwa terdapat ideal prima $\mathfrak p$ dengan $f\notin\mathfrak p$.

<!-- upstream_entity: Kommutative Ringtheorie/Ideale/Radikal ist Durchschnitt von Primidealen/Aufgabe -->

### Soal 10.17 ★ {#br-ak-2025-2026-w10-ex-17}

Misalkan $\mathfrak a$ suatu ideal radikal dalam sebuah gelanggang komutatif.
Tunjukkan bahwa $\mathfrak a$ merupakan irisan ideal-ideal prima.

Salah satu cara diperoleh dari soal sebelumnya; cara lain diperoleh dari
Soal 13.5 di bagian berikutnya.

<!-- upstream_entity: Polynom/1/Nicht konstant/Nicht algebraisch/Aufgabe -->

### Soal 10.18 {#br-ak-2025-2026-w10-ex-18}

Misalkan $K$ suatu lapangan dan $P\in K[X]$ suatu polinom takkonstan.
Tunjukkan bahwa $P$ tidak aljabar atas $K$.

<!-- upstream_entity: Rationaler Funktionenkörper/Echter Zwischenkörper/Darüber endlich/Aufgabe -->

### Soal 10.19 {#br-ak-2025-2026-w10-ex-19}

Misalkan $K$ suatu lapangan dan $L=K(X)$ lapangan pecahan dari gelanggang
polinomial $K[X]$. Misalkan $M$ suatu lapangan antara dengan

$$
K\subseteq M\subseteq L,
\qquad M\ne K.
$$

Tunjukkan bahwa $M\subseteq L$ merupakan perluasan lapangan hingga.

<!-- upstream_entity: Hilbertscher Nullstellensatz/Algebraisch/Z/Endlicher Körper/Aufgabe -->

### Soal 10.20 ★ {#br-ak-2025-2026-w10-ex-20}

Misalkan $A$ suatu aljabar-$\mathbb Z$ yang dibangkitkan secara hingga dan
$\mathfrak m\subseteq A$ suatu ideal maksimal. Tunjukkan bahwa gelanggang
faktor $A/\mathfrak m$ merupakan lapangan berhingga.

Misalkan $K$ suatu lapangan dan $A$ suatu aljabar-$K$ komutatif. Unsur-unsur
$f_1,\ldots,f_n\in A$ disebut *bergantung secara aljabar* jika terdapat
polinom taknol $P\in K[X_1,\ldots,X_n]$ sedemikian sehingga

$$
P(f_1,\ldots,f_n)=0.
$$

<!-- upstream_entity: Polynome/n Variablen/Variablen/Algebraisch unabhängig/Aufgabe -->

### Soal 10.21 {#br-ak-2025-2026-w10-ex-21}

Misalkan $K[X_1,\ldots,X_n]$ gelanggang polinomial atas suatu lapangan $K$.
Tunjukkan bahwa variabel-variabel $X_1,\ldots,X_n$ bebas secara aljabar.

<!-- upstream_entity: Polynome/n Variablen/Algebraisch abhängig/Aufgabe -->

### Soal 10.22 {#br-ak-2025-2026-w10-ex-22}

Misalkan $K[X_1,\ldots,X_n]$ gelanggang polinomial atas suatu lapangan $K$
dan diberikan $n+1$ polinom

$$
f_1,\ldots,f_{n+1}\in K[X_1,\ldots,X_n].
$$

Tunjukkan bahwa polinom-polinom ini bergantung secara aljabar.

<!-- upstream_entity: Affiner Raum/Polynomiale Abbildung/Höhere Dimension/Nicht surjektiv/Aufgabe -->

### Soal 10.23 {#br-ak-2025-2026-w10-ex-23}

Misalkan

$$
\varphi:\mathbb A_K^m\longrightarrow\mathbb A_K^n
$$

suatu pemetaan polinomial antara ruang-ruang afin dengan $m<n$. Tunjukkan
bahwa $\varphi$ tidak surjektif.

<!-- upstream_entity: Algebra/K/Algebraisch unabhängig/Isomorphie/Aufgabe -->

### Soal 10.24 {#br-ak-2025-2026-w10-ex-24}

Misalkan $A$ suatu aljabar-$K$ komutatif atas lapangan $K$ dan diberikan $n$
unsur $f_1,\ldots,f_n\in A$. Tunjukkan bahwa unsur-unsur ini bebas secara
aljabar tepat ketika aljabar-$K$ yang dibangkitkannya,
$K[f_1,\ldots,f_n]$, isomorfik dengan gelanggang polinomial
$K[X_1,\ldots,X_n]$.

## Soal untuk dikumpulkan {#br-ak-2025-2026-w10-submit}

<!-- upstream_entity: Ebene algebraische Kurve/Restklassenring/Algebraisch abgeschlossen/Endlich über Polynomring in einer Variablen/Aufgabe -->

### Soal 10.25 - 3 poin {#br-ak-2025-2026-w10-ex-25}

Misalkan $K$ suatu lapangan yang tertutup secara aljabar dan
$F\in K[X,Y]$ suatu polinom takkonstan. Tunjukkan bahwa gelanggang faktor

$$
K[X,Y]/(F)
$$

dapat dipandang sebagai aljabar-$K[T]$ hingga.

<!-- upstream_entity: Kommutative Ringtheorie/Transitivität der Endlichkeit (Algebren)/Aufgabe -->

### Soal 10.26 - 3 poin {#br-ak-2025-2026-w10-ex-26}

Misalkan $R,S,T$ gelanggang komutatif, serta
$\varphi:R\to S$ dan $\psi:S\to T$ homomorfisme gelanggang sedemikian sehingga
$S$ hingga di atas $R$ dan $T$ hingga di atas $S$. Tunjukkan bahwa $T$ juga
hingga di atas $R$.

<!-- upstream_entity: Artinscher Modul/Kurze exakte Sequenz/Aufgabe -->

### Soal 10.27 - 5 poin {#br-ak-2025-2026-w10-ex-27}

Misalkan $A$ suatu gelanggang komutatif dan

$$
0\longrightarrow M\longrightarrow N\longrightarrow P\longrightarrow0
$$

suatu barisan eksak pendek modul-$A$. Tunjukkan bahwa $N$ Artin tepat ketika
$M$ dan $P$ keduanya Artin.

<!-- upstream_entity: Modultheorie/Exakte Komplexe/Kurze exakte Sequenzen/Aufgabe -->

### Soal 10.28 - 4 poin (1+3) {#br-ak-2025-2026-w10-ex-28}

Misalkan $R$ suatu gelanggang komutatif dan $M_i$, $i\in\mathbb N$, adalah
modul-$R$ dengan homomorfisme modul-$R$ tetap

$$
\varphi_i:M_i\longrightarrow M_{i+1}.
$$

Barisan

$$
\cdots\longrightarrow M_i\longrightarrow M_{i+1}
\longrightarrow M_{i+2}\longrightarrow M_{i+3}\longrightarrow\cdots
$$

disebut *eksak* jika, untuk setiap $i$,

$$
\operatorname{ker}(\varphi_i)=\operatorname{im}(\varphi_{i-1}).
$$

1. Tunjukkan bahwa, dalam kasus barisan eksak pendek, definisi ini sama dengan
   Definisi 10.2 dalam kuliah.
2. Sekarang misalkan $R=K$ suatu lapangan, semua $M_i$ dibangkitkan secara
   hingga, $M_0=0$, dan $M_i=0$ untuk semua $i\geq n$ bagi suatu $n$.
   Tunjukkan bahwa

   $$
   \sum_{i=0}^{n}(-1)^i\operatorname{dim}_K M_i=0.
   $$

<!-- upstream_entity: Körpertheorie/Endliche Erweiterung von Körper/Ist artinsch/Aufgabe -->

### Soal 10.29 - 3 poin {#br-ak-2025-2026-w10-ex-29}

Misalkan $K$ suatu lapangan dan $A$ suatu aljabar-$K$ hingga. Tunjukkan bahwa
$A$ Artin.
