---
title: "Lembar Kerja 1 - Bundel Vektor dan Bundel Tangen"
stable_id: br-bgk-2019-w01
language: id-ID
source_course: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)"
source_author: "Holger Brenner"
frozen_revision_contributor: "Bocardodarapti"
upstream_title: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)/Arbeitsblatt 1"
upstream_pageid: 110204
upstream_revid: 1069465
upstream_timestamp: "2026-02-05T20:48:01Z"
upstream_mediawiki_sha1: a2c9deb62e10eb9942aac56cde2e33aed04823fd
source_url: "https://de.wikiversity.org/w/index.php?oldid=1069465"
authority_manifest: authority/wikiversity-bgk/unit-01/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: ad271f5ad69f9990dbe3082c22f8c52b7a4c58494c8f6614350078535d4f2ba1
worksheet_xml: authority/wikiversity-bgk/unit-01/worksheet-01.xml
worksheet_xml_sha256: 95e392e04115c0dcfc94eebc28bfdbdbdfc1cda3c46d6f008d7d1324b3e81095
worksheet_expanded_tex: authority/wikiversity-bgk/unit-01/worksheet-01-expanded.tex
worksheet_expanded_tex_sha256: 566b4211d5b25be90256a24567f0c448a6cc9fe23aec74c4fde8c6922cba2d97
exercise_map: authority/wikiversity-bgk/unit-01/ORDERED_EXERCISE_MAP.json
exercise_map_sha256: 21244128b357d5fc35d5a8dc7129c27e091a781594516c4f6db87e9202b162ba
official_pdf: authority/artifacts/bgk-worksheet-01-official.pdf
official_pdf_sha256: 0f65dad0173f0ad40d22cf5f255f9379aca90a090d0c54cc268379f8628ee70a
license: "Frozen semantic course text and this translation: CC BY-SA 4.0. Official PDF and media retain their recorded component notices; no blanket relicensing claim is made."
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra."
exercise_count: 17
public_solution_count: 0
---

# Lembar Kerja 1: Bundel Vektor dan Bundel Tangen {#br-bgk-2019-w01}

Dalam soal-soal berikut, kita menggunakan notasi

$$
D(r)=\left\{(r,s,t)\in\mathbb R^3\mid r\ne0\right\}.
$$

<!-- upstream_entity: Lineare Gleichung/Drei Variablen/Parameter/Trivialisierungen/Übergangsabbildungen/Aufgabe -->

## Soal 1.1 {#br-bgk-2019-w01-ex01}

Untuk bundel vektor

$$
\begin{aligned}
L={}&\left\{(r,s,t,u,v,w)\mathrel{\Big|}
ru+sv+tw=0,\ (r,s,t)\ne(0,0,0)\right\}\\
&\subseteq
\left(\mathbb R^3\setminus\{(0,0,0)\}\right)\times\mathbb R^3
\longrightarrow\mathbb R^3\setminus\{(0,0,0)\},
\end{aligned}
$$

tentukan trivialisasi linear di atas $D(r)$, $D(s)$, dan $D(t)$, yaitu
basis-basis yang bergantung pada $r,s,t$ di atas $D(r)$ dan seterusnya.
Tentukan pemetaan perubahan basis pada

$$
D(rs)=D(r)\cap D(s).
$$

<!-- upstream_entity: Lineare Gleichung/Drei Variablen/Parameter/Trivialisierungen/Vektorzugehörigkeit/Aufgabe -->

## Soal 1.2 {#br-bgk-2019-w01-ex02}

Untuk bundel vektor

$$
\begin{aligned}
L={}&\left\{(r,s,t,u,v,w)\mathrel{\Big|}
ru+sv+tw=0,\ (r,s,t)\ne(0,0,0)\right\}\\
&\subseteq
\left(\mathbb R^3\setminus\{(0,0,0)\}\right)\times\mathbb R^3
\longrightarrow\mathbb R^3\setminus\{(0,0,0)\},
\end{aligned}
$$

tentukan semua parameter $(r,s,t)$ yang membuat vektor $(3,7,4)$ termasuk
dalam serat $L_{(r,s,t)}$.

<!-- upstream_entity: Lineare Gleichung/Drei Variablen/Parameter/Trivialisierungen/Fortsetzungsfunktion/Aufgabe -->

## Soal 1.3 {#br-bgk-2019-w01-ex03}

Tunjukkan bahwa, pada Contoh 1.2 dan di atas $D(r)$, rumus

$$
u(r,s,t)=
\frac{t}{r}\begin{pmatrix}s\\-r\\0\end{pmatrix}
-\frac{s}{r}\begin{pmatrix}t\\0\\-r\end{pmatrix}
$$

mendefinisikan sebuah vektor dalam ruang penyelesaian yang bergantung pada
parameter dan dapat diperluas secara polinomial ke seluruh $\mathbb R^3$,
meskipun fungsi koefisien $t/r$ dan $-s/r$ hanya terdefinisi pada $D(r)$ dan
tidak dapat diperluas. Apakah $u(r,s,t)$ merupakan bagian dari suatu basis di
setiap titik?

<!-- upstream_entity: Zwei lineare Gleichungen/Drei Variablen/Parameter/Trivialisierung/Stratifizierung/Aufgabe -->

## Soal 1.4 {#br-bgk-2019-w01-ex04}

Pada Contoh 1.3, tentukan parameter-parameter yang membuat ruang
penyelesaian $L_{(a,b,c,d,e,f)}$ berdimensi satu, dua, atau tiga. Apakah
himpunan-himpunan parameter tersebut terbuka atau tertutup?

<!-- upstream_entity: Körper/Kreuzprodukt/Keine Basis/Aufgabe -->

## Soal 1.5 {#br-bgk-2019-w01-ex05}

Tunjukkan bahwa, di atas lapangan sebarang $K$, untuk dua vektor bebas
linear

$$
u=\begin{pmatrix}a\\b\\c\end{pmatrix}
\quad\text{dan}\quad
v=\begin{pmatrix}d\\e\\f\end{pmatrix},
$$

keluarga yang terdiri atas $u$, $v$, dan hasil kali silangnya

$$
\begin{pmatrix}a\\b\\c\end{pmatrix}
\times
\begin{pmatrix}d\\e\\f\end{pmatrix}
$$

tidak harus membentuk basis bagi $K^3$.

<!-- upstream_entity: Affin-lineares Bündel/R^2/Fasern/Aufgabe -->

## Soal 1.6 {#br-bgk-2019-w01-ex06}

Perhatikan ruang topologis

$$
Y:=\left\{(s,t,u,v)\in\mathbb R^4\mid su+tv=1\right\}
$$

dengan proyeksi

$$
\begin{aligned}
p:Y&\longrightarrow\mathbb R^2\setminus\{(0,0)\}=X,\\
(s,t,u,v)&\longmapsto(s,t).
\end{aligned}
$$

1. Tunjukkan bahwa setiap serat $p$ homeomorfik dengan sebuah garis real.
2. Tunjukkan bahwa

   $$
   \varphi(s,t)=(s,t,u(s,t),v(s,t))
   =\left(s,t,\frac{s}{s^2+t^2},\frac{t}{s^2+t^2}\right)
   $$

   mendefinisikan pemetaan kontinu $\varphi:X\to Y$ dengan

   $$
   p\circ\varphi=\operatorname{Id}_X.
   $$

3. Definisikan suatu homeomorfisme antara $Y$ dan $X\times\mathbb R$.
4. Tunjukkan bahwa tidak terdapat pemetaan polinomial $\psi:X\to Y$ dengan

   $$
   p\circ\psi=\operatorname{Id}_X.
   $$

<!-- upstream_entity: Reelles Vektorbündel/Ein Punkt/Aufgabe -->

## Soal 1.7 {#br-bgk-2019-w01-ex07}

Tunjukkan bahwa sebuah bundel vektor real di atas satu titik, yakni di atas
ruang topologis bertitik tunggal, sama dengan sebuah ruang vektor real
berdimensi hingga.

<!-- upstream_entity: Reelles Vektorbündel/Hausdorff/Aufgabe -->

## Soal 1.8 {#br-bgk-2019-w01-ex08}

Misalkan $p:V\to X$ suatu bundel vektor real di atas ruang topologis $X$.
Tunjukkan bahwa $V$ merupakan ruang Hausdorff jika dan hanya jika $X$
merupakan ruang Hausdorff.

<!-- upstream_entity: Reelles Vektorbündel/Identität/Aufgabe -->

## Soal 1.9 {#br-bgk-2019-w01-ex09}

Misalkan $X$ suatu ruang topologis. Tunjukkan bahwa pemetaan identitas

$$
\operatorname{Id}_X:X\longrightarrow X
$$

dapat dipandang sebagai bundel vektor real dengan rank $0$.

<!-- upstream_entity: Triviale Bündel/Homomorphismus/Matrixbeschreibung/Aufgabe -->

## Soal 1.10 {#br-bgk-2019-w01-ex10}

Misalkan $X$ suatu ruang topologis. Tunjukkan bahwa sebuah homomorfisme
bundel vektor trivial

$$
\varphi:X\times\mathbb R^n\longrightarrow X\times\mathbb R^m
$$

sama dengan sebuah matriks $m\times n$ yang entri-entrinya adalah fungsi
kontinu dari $X$ ke $\mathbb R$.

<!-- upstream_entity: Stetige differenzierbare Abbildung/Totales Differential/Vektorbündelhomomorphismus/Aufgabe -->

## Soal 1.11 {#br-bgk-2019-w01-ex11}

Misalkan $U\subseteq\mathbb R^n$ terbuka dan
$f:U\to\mathbb R^m$ suatu pemetaan terdiferensial secara kontinu.
Tunjukkan
bahwa diferensial total, dalam bentuk

$$
\begin{aligned}
U\times\mathbb R^n&\longrightarrow U\times\mathbb R^m,\\
(x,v)&\longmapsto\bigl(x,(Df)_x(v)\bigr),
\end{aligned}
$$

mendefinisikan homomorfisme dari bundel vektor $U\times\mathbb R^n$ ke
bundel vektor $U\times\mathbb R^m$.

<!-- upstream_entity: Tangentialbündel/S^1/Trivial/Aufgabe -->

## Soal 1.12 {#br-bgk-2019-w01-ex12}

Tunjukkan bahwa bundel tangen $TS^1$ dari sfera satu $S^1$ homeomorfik
dengan hasil kali $S^1\times\mathbb R$.

Apa hubungan soal ini dengan Contoh 1.1?

<!-- upstream_entity: S^1/Weg/Tangentialbündel/Basiskonvergenz/Beispiel/Aufgabe -->

## Soal 1.13 {#br-bgk-2019-w01-ex13}

Berikan sebuah contoh kurva terdiferensial

$$
\gamma:[0,1)\longrightarrow S^1
$$

sedemikian sehingga limit

$$
\lim_{t\to1}\gamma(t)
$$

ada, tetapi limit

$$
\lim_{t\to1}\bigl(\gamma(t),T_t(\gamma)(1)\bigr)
$$

tidak ada di $TS^1$.

<!-- upstream_entity: Einheitssphäre/Untermannigfaltigkeit/Tangentialabbildung/Aufgabe -->

## Soal 1.14 {#br-bgk-2019-w01-ex14}

Tunjukkan bahwa pemetaan

$$
\begin{aligned}
TS^1&\longrightarrow\mathbb R^2,\\
((a,b),t(-b,a))&\longmapsto(a,b)+t(-b,a)
\end{aligned}
$$

mempunyai dua prabayang untuk setiap titik $(x,y)\in\mathbb R^2$ di luar
cakram satuan, satu prabayang untuk setiap titik pada lingkaran satuan, dan
tidak mempunyai prabayang untuk setiap titik di dalam cakram satuan terbuka.
Tafsirkan hasil ini secara geometris.

<!-- upstream_entity: Mannigfaltigkeit/Differenzierbare Abbildung/Injektiv/Tangentialabbildung nicht injektiv/Beispiel/Aufgabe -->

## Soal 1.15 {#br-bgk-2019-w01-ex15}

Berikan sebuah contoh pemetaan terdiferensial injektif

$$
\varphi:M\longrightarrow N
$$

antara dua manifold terdiferensial $M$ dan $N$ sedemikian sehingga
pemetaan tangen terkait

$$
T(\varphi):TM\longrightarrow TN
$$

tidak injektif.

<!-- upstream_entity: Mannigfaltigkeit/Differenzierbare Abbildung/Surjektiv/Tangentialabbildung nicht surjektiv/Beispiel/Aufgabe -->

## Soal 1.16 {#br-bgk-2019-w01-ex16}

Berikan sebuah contoh pemetaan terdiferensial surjektif

$$
\varphi:M\longrightarrow N
$$

antara dua manifold terdiferensial $M$ dan $N$ sedemikian sehingga
pemetaan tangen terkait

$$
T(\varphi):TM\longrightarrow TN
$$

tidak surjektif.

<!-- upstream_entity: Mannigfaltigkeit/Tangentialabbildung/Stetig/Aufgabe -->

## Soal 1.17 {#br-bgk-2019-w01-ex17}

Misalkan $M$ dan $N$ manifold terdiferensial dan
$\varphi:M\to N$ suatu pemetaan terdiferensial. Tunjukkan bahwa pemetaan
tangen terkait

$$
T(\varphi):TM\longrightarrow TN
$$

bersifat kontinu.
