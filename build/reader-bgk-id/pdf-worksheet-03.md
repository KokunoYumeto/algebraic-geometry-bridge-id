---
title: "Lembar Kerja 3 - Konstruksi Linear, Praberkas, dan Tangkai"
stable_id: br-bgk-2019-w03
language: id-ID
source_course: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)"
source_author: "Holger Brenner"
frozen_revision_contributor: "Bocardodarapti"
upstream_title: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)/Arbeitsblatt 3"
upstream_pageid: 109057
upstream_revid: 619301
upstream_timestamp: "2020-02-17T10:29:54Z"
upstream_mediawiki_sha1: a6abf3d53e491ec12c798e96f3dfeec8b84de8c7
source_url: "https://de.wikiversity.org/w/index.php?oldid=619301"
authority_manifest: authority/wikiversity-bgk/unit-03/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 60270cc7ba74a4ed744687ae18c3887eca8a2fff6bce48a819be102d4a619a5a
worksheet_xml: authority/wikiversity-bgk/unit-03/worksheet-03.xml
worksheet_xml_sha256: a34ac6428f6d2074e4bc01f3d3d6064c38625eea36fa4b5c48e18a524e583c15
worksheet_expanded_tex: authority/wikiversity-bgk/unit-03/worksheet-03-expanded.tex
worksheet_expanded_tex_sha256: 08f9268af226916ef212041a50d430ca5fcf71df2c5a57ab5adb36183e2a4b2a
exercise_map: authority/wikiversity-bgk/unit-03/ORDERED_EXERCISE_MAP.json
exercise_map_sha256: 5242db043a773e412806fd066ed831fe6ebbdc7d16a35af8070ff1ce7398901f
official_pdf: authority/artifacts/bgk-worksheet-03-official.pdf
official_pdf_sha256: 615cfac501c1397cab86e7a4a000adae7587161b7cf7b2fd28f9bd6df7c7993c
license: "Frozen semantic course text and this translation: CC BY-SA 4.0. Official PDF witnesses retain their recorded component notices; no blanket relicensing claim is made."
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra."
exercise_count: 18
public_solution_count: 1
---

# Lembar Kerja 3: Konstruksi Linear, Praberkas, dan Tangkai {#br-bgk-2019-w03}

Hasil kali Kronecker dari matriks

$$
A=(a_{ij})_{1\le i\le m,\,1\le j\le n}
$$

dan

$$
B=(b_{k\ell})_{1\le k\le p,\,1\le\ell\le r}
$$

adalah matriks

$$
(a_{ij}b_{k\ell})_{
  1\le i\le m,\,1\le k\le p;\,
  1\le j\le n,\,1\le\ell\le r}.
$$

<!-- upstream_entity: Kroneckerprodukt/2x2/Berechnung/Aufgabe -->

## Soal 3.1 {#br-bgk-2019-w03-ex01}

Hitung hasil kali Kronecker kedua matriks

$$
\begin{pmatrix}3&-4\\5&-2\end{pmatrix}
\quad\text{dan}\quad
\begin{pmatrix}-2&7\\6&3\end{pmatrix}.
$$

<!-- upstream_entity: Matrizen/Tensorprodukt/Kroneckerprodukt/Aufgabe -->

## Soal 3.2 {#br-bgk-2019-w03-ex02}

Misalkan $K$ sebuah lapangan, dan misalkan

$$
A=(a_{ij})_{1\le i\le m,\,1\le j\le n},
\qquad
B=(b_{k\ell})_{1\le k\le p,\,1\le\ell\le r}
$$

matriks-matriks dengan pemetaan linear yang bersesuaian

$$
A:K^n\longrightarrow K^m,
\qquad
B:K^r\longrightarrow K^p.
$$

Tunjukkan bahwa hasil kali tensor kedua pemetaan linear tersebut, terhadap
basis

$$
(e_j\otimes e_\ell)_{1\le j\le n,\,1\le\ell\le r}
$$

dari $K^n\otimes K^r$ dan basis

$$
(e_i\otimes e_k)_{1\le i\le m,\,1\le k\le p}
$$

dari $K^m\otimes K^p$, dideskripsikan oleh hasil kali Kronecker $A$ dan
$B$.

<!-- upstream_entity: Möbiusband/Tensorprodukt/Trivial/Aufgabe -->

## Soal 3.3 {#br-bgk-2019-w03-ex03}

Tunjukkan bahwa hasil kali tensor pita Möbius dengan dirinya sendiri
merupakan bundel garis trivial.

<!-- upstream_entity: Prägarbe/Produkt/Aufgabe -->

## Soal 3.4 {#br-bgk-2019-w03-ex04}

Misalkan $\mathcal F$ dan $\mathcal G$ praberkas pada ruang topologis $X$.
Tunjukkan bahwa penetapan

$$
U\longmapsto\mathcal F(U)\times\mathcal G(U),
$$

bersama pemetaan produk alami sebagai pemetaan restriksi, mendefinisikan
sebuah praberkas pada $X$.

<!-- upstream_entity: Prägarbe/Produkt/Beliebige Indexmenge/Aufgabe -->

## Soal 3.5 {#br-bgk-2019-w03-ex05}

Misalkan $I$ sebuah himpunan indeks dan
$(\mathcal F_i)_{i\in I}$ sebuah keluarga praberkas pada ruang topologis
$X$. Tunjukkan bahwa penetapan

$$
U\longmapsto\prod_{i\in I}\mathcal F_i(U),
$$

bersama pemetaan produk alami sebagai pemetaan restriksi, mendefinisikan
sebuah praberkas pada $X$.

<!-- upstream_entity: Prägarbe/Stetige Abbildungen/Schnitte/Aufgabe -->

## Soal 3.6 {#br-bgk-2019-w03-ex06}

Tafsirkan Contoh 3.8 menurut kerangka Contoh 3.12.

<!-- upstream_entity: Reelles Vektorbündel/Trivialisierung/Stetige Schnitte/Aufgabe -->

## Soal 3.7 {#br-bgk-2019-w03-ex07}

Misalkan

$$
p:V\longrightarrow X
$$

sebuah bundel vektor real berank $m$ pada ruang topologis $X$. Tunjukkan
bahwa untuk setiap himpunan terbuka $U\subseteq X$ tempat $V$ trivial,
praberkas seksi kontinu yang bersesuaian isomorfik dengan

$$
C^0(U,\mathbb R)^m.
$$

Jelaskan pula dalam pengertian apa isomorfisme tersebut dimaksud.

<!-- upstream_entity: Topologische Gruppe/Nachweis/Aufgabe -->

## Soal 3.8 {#br-bgk-2019-w03-ex08}

Tunjukkan bahwa grup-grup

$$
(\mathbb R,+),\quad
(\mathbb R\setminus\{0\},\cdot),\quad
(\mathbb C,+),\quad
(\mathbb C\setminus\{0\},\cdot),\quad
(\mathbb R^n,+),
$$

lingkaran $S^1$ dengan penjumlahan sudut, serta grup linear umum
$\operatorname{GL}_n(\mathbb R)$ dan $\operatorname{GL}_n(\mathbb C)$
merupakan grup topologis.

<!-- upstream_entity: Topologische Gruppe/Untergruppe/Unterprägarbe/Aufgabe -->

## Soal 3.9 {#br-bgk-2019-w03-ex09}

Misalkan $G$ sebuah grup topologis dan $H\subseteq G$ sebuah subgrup.
Tunjukkan bahwa, pada setiap ruang topologis $X$, praberkas
$C^0(-,H)$ merupakan subpraberkas dari $C^0(-,G)$.

Sebuah manifold terdiferensial $G$ yang sekaligus merupakan grup, dengan
operasi invers dan operasi grup berupa pemetaan terdiferensial, disebut
*grup Lie real*.

<!-- upstream_entity: Lie-Gruppe/Nachweis/Aufgabe -->

## Soal 3.10 {#br-bgk-2019-w03-ex10}

Tunjukkan bahwa grup-grup

$$
(\mathbb R,+),\quad
(\mathbb R\setminus\{0\},\cdot),\quad
(\mathbb C,+),\quad
(\mathbb C\setminus\{0\},\cdot),\quad
(\mathbb R^n,+),
$$

lingkaran $S^1$ dengan penjumlahan sudut, serta
$\operatorname{GL}_n(\mathbb R)$ dan $\operatorname{GL}_n(\mathbb C)$
merupakan grup Lie.

<!-- upstream_entity: Reelle Lie-Gruppe/Tangentialbündel/Trivial/Aufgabe -->

## Soal 3.11 {#br-bgk-2019-w03-ex11}

Tunjukkan bahwa bundel tangen pada suatu grup Lie trivial.

> **Petunjuk.** Tunjukkan bahwa ruang tangen pada unsur identitas dapat
> dipindahkan secara alami ke ruang-ruang tangen lainnya.

<!-- upstream_entity: Gerichtetes System/Kolimes/Universelle Eigenschaft/Mengen und Gruppen/Aufgabe -->

## Soal 3.12 {#br-bgk-2019-w03-ex12}

Misalkan $I$ sebuah himpunan indeks terarah dan $(M_i)_{i\in I}$ sebuah
sistem terarah himpunan, dengan pemetaan sistem
$\varphi_{ij}:M_i\to M_j$. Misalkan $N$ sebuah himpunan lain, dan untuk
setiap $i\in I$ diberikan pemetaan

$$
\psi_i:M_i\longrightarrow N
$$

sedemikian sehingga

$$
\psi_i=\psi_j\circ\varphi_{ij}
$$

untuk semua $i\preccurlyeq j$. Buktikan sifat universal kolimit: terdapat
tepat satu pemetaan

$$
\psi:\operatorname{colim}_{i\in I}M_i\longrightarrow N
$$

sedemikian sehingga

$$
\psi_i=\psi\circ j_i,
$$

dengan $j_i:M_i\to\operatorname{colim}_{i\in I}M_i$ pemetaan alami.

Tunjukkan pula bahwa jika $(M_i)$ merupakan sistem terarah grup, $N$ juga
sebuah grup, dan semua $\psi_i$ homomorfisme grup, maka $\psi$ juga
merupakan homomorfisme grup.

<!-- upstream_entity: Gerichtetes System/Von kommutativen Gruppen/Kolimes ist kommutative Gruppe/Aufgabe -->

## Soal 3.13 {#br-bgk-2019-w03-ex13}

Misalkan $I$ sebuah himpunan indeks terarah dan $(G_i)_{i\in I}$ sebuah
sistem terarah grup komutatif. Tunjukkan bahwa kolimitnya merupakan grup
komutatif.

<!-- upstream_entity: Kommutative Ringtheorie/Nenneraufnahme/Als gerichtetes System/Aufgabe -->

## Soal 3.14 {#br-bgk-2019-w03-ex14}

Misalkan $R$ sebuah gelanggang komutatif dan $S\subseteq R$ sebuah sistem
multiplikatif. Pada $S$, perhatikan urutan parsial berikut: nyatakan
$f\preccurlyeq g$ jika $f$ membagi suatu pangkat dari $g$; identifikasikan
dua unsur jika relasi tersebut berlaku dalam kedua arah.

Tunjukkan bahwa gelanggang-gelanggang komutatif

$$
R_f,\qquad f\in S,
$$

membentuk sebuah sistem terarah, dan bahwa

$$
\operatorname{colim}_{f\in S}R_f=R_S.
$$

<!-- upstream_entity: Mannigfaltigkeit/Tangentialbündel/Halm/Gleich/Aufgabe -->

## Soal 3.15 {#br-bgk-2019-w03-ex15}

Misalkan $M$ sebuah manifold terdiferensial dan $P\in M$. Tunjukkan bahwa
tangkai di $P$ dari praberkas seksi kontinu bundel tangen $TM\to M$ hanya
bergantung pada dimensi manifold di titik $P$.

> **Catatan edisi - objek tangkai diperjelas.** Sumber meminta pembuktian
> tentang “tangkai bundel tangen”. Tangkai melekat pada praberkas, bukan
> langsung pada bundel. Konteks Kuliah 3 dan Contoh 3.12 menentukan objek
> yang dimaksud sebagai praberkas seksi kontinu dari bundel tangen. Edisi
> menyatakan objek tersebut secara eksplisit dan mempertahankan bentuk
> singkat sumber dalam catatan ini.

<!-- upstream_entity: Prägarbe/Produkt/Halm/Aufgabe -->

## Soal 3.16 {#br-bgk-2019-w03-ex16}

Misalkan $\mathcal F$ dan $\mathcal G$ praberkas pada ruang topologis $X$,
dan misalkan $\mathcal F\times\mathcal G$ praberkas produknya. Tunjukkan
bahwa untuk setiap titik $P\in X$ berlaku

$$
(\mathcal F\times\mathcal G)_P
=\mathcal F_P\times\mathcal G_P.
$$

<!-- upstream_entity: Prägarbe/Homomorphismus/Verknüpfung/Fakt/Beweis/Aufgabe -->

## Soal 3.17 {#br-bgk-2019-w03-ex17}

Misalkan $X$ sebuah ruang topologis dan
$\mathcal F,\mathcal G,\mathcal H$ praberkas pada $X$. Tunjukkan
pernyataan-pernyataan berikut.

1. Identitas $\mathcal F\to\mathcal F$ merupakan morfisme praberkas.
2. Jika $\varphi:\mathcal F\to\mathcal G$ dan
   $\psi:\mathcal G\to\mathcal H$ merupakan morfisme praberkas, maka
   $\psi\circ\varphi$ juga merupakan morfisme praberkas.
3. Jika $\mathcal F\subseteq\mathcal G$ sebuah subpraberkas, inklusi
   alaminya merupakan morfisme praberkas.

> **Catatan edisi - salah ketik sumber.** Pada butir ketiga, sumber
> mencetak *Prägraben*, yang jelas merupakan salah ketik untuk
> *Prägarben* (praberkas). Bentuk yang benar dipakai di atas; cacat yang
> sama juga dicatat pada Lema 3.26.

<!-- upstream_entity: Prägarbe/Produkt/Beliebige Indexmenge/Morphismus/Aufgabe -->

## Soal 3.18 {#br-bgk-2019-w03-ex18}

Misalkan $I$ sebuah himpunan indeks,
$(\mathcal F_i)_{i\in I}$ sebuah keluarga praberkas pada ruang topologis
$X$, dan $\prod_{i\in I}\mathcal F_i$ praberkas produknya. Misalkan
$\mathcal G$ sebuah praberkas lain pada $X$. Tunjukkan bahwa sebuah morfisme
praberkas

$$
\psi:\mathcal G\longrightarrow\prod_{i\in I}\mathcal F_i
$$

sama artinya dengan suatu keluarga morfisme praberkas

$$
\psi_i:\mathcal G\longrightarrow\mathcal F_i,
\qquad i\in I.
$$
