---
title: "Lembar Kerja 28 - Varietas Proyektif dan Penutupan Proyektif"
stable_id: br-ak-2012-w28
language: id-ID
source_author: "Holger Brenner"
frozen_revision_contributor: "Arbota"
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2012)/Arbeitsblatt 28"
upstream_pageid: 50763
upstream_revid: 793497
upstream_timestamp: "2022-08-25T06:04:27Z"
upstream_mediawiki_sha1: 7ee8f07ea803541b23e8e1fa686c7b2c17e6f67a
source_url: "https://de.wikiversity.org/w/index.php?oldid=793497"
authority_manifest: authority/wikiversity/unit-28/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: f2e34fc420c4beec300ea9e0accc52598e12c27f46c9022611996b1b43e29a99
worksheet_xml: authority/wikiversity/unit-28/worksheet-28.xml
worksheet_xml_sha256: dc1af11088dac5f3ae3597a94af6bdba91afe35de35d8c2aecf4d26edd00f4fa
worksheet_expanded_tex: authority/wikiversity/unit-28/worksheet-28-expanded.tex
worksheet_expanded_tex_sha256: 9505f42a5a87139ca3e3dae694dc90b1692b38e0a9e312efa3b9159bbf2bab94
license: "Current semantic course text and this translation: CC BY-SA 4.0. Official PDF and media components retain their recorded component routes."
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
exercise_count: 14
warm_up_exercises: "1-10"
submitted_exercises: "11-14"
starred_exercises: "10"
displayed_points: "11:3; 12:4; 13:3; 14:3"
public_solution_count: 1
public_solution_exercises: "10"
source_corrections: 1
correction_ids: "AGC-CORR-0121"
---

# Lembar Kerja 28 {#br-ak-2012-w28}

## Soal pemanasan {#br-ak-2012-w28-warmup}

<!-- upstream_entity: Projektiver Raum/Für jeden Punkt affine Umgebung, wo Nullpunkt/Aufgabe -->

### Soal 28.1 {#br-ak-2012-w28-ex01}

Misalkan

$$
P=(a_0,\ldots,a_n)\in\mathbb P_K^n
$$

suatu titik di ruang proyektif. Tunjukkan bahwa terdapat lingkungan terbuka
afin

$$
U\cong\mathbb A_K^n\subset\mathbb P_K^n
$$

sedemikian sehingga $P$ bersesuaian dengan titik asal dalam ruang afin itu.

<!-- upstream_entity: Projektiver Raum/Zariski Topologie/Einschränkung auf affinen Raum/Aufgabe -->

### Soal 28.2 {#br-ak-2012-w28-ex02}

Misalkan

$$
D_+(L)\cong\mathbb A_K^n\subseteq\mathbb P_K^n,
$$

dengan $L$ suatu bentuk linear homogen di $K[X_0,\ldots,X_n]$. Tunjukkan
bahwa topologi Zariski pada ruang proyektif menginduksi topologi Zariski pada
ruang afin tersebut.

<!-- upstream_entity: Projektive Gerade/Morphismus durch beliebige Potenzen/Aufgabe -->

### Soal 28.3 {#br-ak-2012-w28-ex03}

Untuk setiap $n\in\mathbb Z$, definisikan pemangkatan

$$
x\longmapsto x^n
$$

sebagai morfisme dari garis proyektif ke dirinya sendiri. Bagaimanakah
serat-serat morfisme ini?

> **Catatan edisi - semua eksponen bulat.** Kuantor sumber
> $n\in\mathbb Z$ dipertahankan. Kasus $n=0$, $n<0$, dan karakteristik yang
> membagi $|n|$ perlu dibedakan; edisi tidak diam-diam menggantinya dengan
> asumsi $n>0$ atau karakteristik nol.

<!-- upstream_entity: Ebene algebraische Kurve/Kardioide/Projektiver Abschluss/Aufgabe -->

### Soal 28.4 {#br-ak-2012-w28-ex04}

Tentukan penutupan proyektif kardioid kompleks

$$
V\!\left((X^2+Y^2)^2-2X(X^2+Y^2)-Y^2\right),
$$

khususnya titik-titiknya di tak hingga.

<!-- upstream_entity: Projektiver Raum/Kegelabbildung/Ist Morphismus/Aufgabe -->

### Soal 28.5 {#br-ak-2012-w28-ex05}

Tunjukkan bahwa pemetaan kerucut

$$
\mathbb A_K^{n+1}\setminus\{0\}\longrightarrow\mathbb P_K^n
$$

merupakan morfisme varietas kuasiprojektif.

<!-- upstream_entity: Projektiver Raum/Kegelabbildung/Ist nicht abgeschlossen/Aufgabe -->

### Soal 28.6 {#br-ak-2012-w28-ex06}

Berikan contoh yang menunjukkan bahwa pemetaan kerucut

$$
\mathbb A_K^{n+1}\setminus\{0\}\longrightarrow\mathbb P_K^n
$$

tidak harus merupakan pemetaan tertutup.

<!-- upstream_entity: Quasiprojektive Varietäten/Offene Überdeckung des Ziels/Kriterium für Morphismus/Aufgabe -->

### Soal 28.7 {#br-ak-2012-w28-ex07}

Misalkan $X$ dan $Y$ varietas kuasiprojektif dan
$\varphi:X\to Y$ suatu pemetaan kontinu. Misalkan

$$
Y=\bigcup_{i\in I}U_i
$$

suatu penutup terbuka. Tunjukkan bahwa $\varphi$ merupakan morfisme jika dan
hanya jika, untuk setiap $i$, pembatasan

$$
\varphi_i:\varphi^{-1}(U_i)\longrightarrow U_i
$$

merupakan morfisme.

<!-- upstream_entity: Die projektive Gerade/Globaler Schnittring/Aufgabe -->

### Soal 28.8 {#br-ak-2012-w28-ex08}

Misalkan $K$ suatu lapangan. Tentukan gelanggang seksi global

$$
\Gamma\!\left(\mathbb P_K^1,\mathcal O_{\mathbb P_K^1}\right).
$$

Apa akibatnya bagi suatu morfisme

$$
\mathbb P_K^1\longrightarrow\mathbb A_K^1?
$$

<!-- upstream_entity: Quasiprojektive Varietät/Normal/Definiere/Aufgabe -->

### Soal 28.9 {#br-ak-2012-w28-ex09}

Definisikan dan cirikan kapan suatu varietas kuasiprojektif tak tereduksi
disebut *normal*.

<!-- upstream_entity: Ebene Kurve/y-x^3+x+2/Rationale Parametrisierung/Fortsetzung auf P^1/Aufgabe -->

### Soal 28.10 * {#br-ak-2012-w28-ex10}

Misalkan $K$ suatu lapangan. Perhatikan kurva bidang afin

$$
C=V(Y-X^3+X+2).
$$

Definisikan suatu isomorfisme antara $C$ dan garis afin $\mathbb A_K^1$.
Dapatkah isomorfisme semacam itu diperluas menjadi isomorfisme antara
$\mathbb P_K^1$ dan penutupan proyektif

$$
\overline C\subset\mathbb P_K^2?
$$

## Soal untuk dikumpulkan {#br-ak-2012-w28-submit}

<!-- upstream_entity: Affiner Raum/K ist R oder C/Offene Menge auf Hyperebene und zugehöriger Kegel/Ist offen/Aufgabe -->

### Soal 28.11 (3 poin) {#br-ak-2012-w28-ex11}

Misalkan $\mathbb K=\mathbb R$ atau $\mathbb K=\mathbb C$. Misalkan
$H\subset\mathbb K^{n+1}$ suatu subruang afin berdimensi $n$ yang tidak
memuat titik asal, dan misalkan $\widetilde H$ subruang yang sejajar dengan
$H$ dan melalui titik asal. Misalkan $U\subseteq H$ terbuka dalam topologi
metrik pada $H\cong\mathbb K^n$, dan misalkan $V$ gabungan semua garis yang
melalui titik asal dan suatu titik dari $U$. Tunjukkan bahwa

$$
V\cap(\mathbb K^{n+1}\setminus\widetilde H)
$$

terbuka.

<!-- upstream_entity: Projektiver Raum/Kegelabbildung/Abschluss des Bildes einer abgeschlossenen Menge/Aufgabe -->

### Soal 28.12 (4 poin) {#br-ak-2012-w28-ex12}

Untuk pemetaan kerucut

$$
\mathbb A_K^{n+1}\setminus\{0\}\longrightarrow\mathbb P_K^n,
$$

tentukan penutupan Zariski di $\mathbb P_K^n$ dari bayangan himpunan
tertutup

$$
V(\mathfrak a)\cap(\mathbb A_K^{n+1}\setminus\{0\}).
$$

<!-- upstream_entity: Quasiprojektive Varietät/Integer/Durchschnitt/Aufgabe -->

### Soal 28.13 (3 poin) {#br-ak-2012-w28-ex13}

Misalkan $X$ suatu varietas kuasiprojektif tak tereduksi dengan lapangan
fungsi $L=K(X)$. Misalkan $U$ dan $U_i$ untuk $i\in I$ himpunan-himpunan
terbuka dengan

$$
U=\bigcup_{i\in I}U_i.
$$

Tunjukkan bahwa

$$
\Gamma(U,\mathcal O)
=
\bigcap_{i\in I}\Gamma(U_i,\mathcal O),
$$

dengan irisan diambil di dalam $L$.

<!-- upstream_entity: Projektiver Raum/Globale algebraische Funktionen/Sind K/Aufgabe -->

### Soal 28.14 (3 poin) {#br-ak-2012-w28-ex14}

Misalkan $K$ suatu lapangan dan $\mathbb P_K^n$ ruang proyektif di atas
$K$. Tunjukkan bahwa konstanta adalah satu-satunya fungsi aljabar global,
yakni

$$
\Gamma\!\left(\mathbb P_K^n,\mathcal O_{\mathbb P_K^n}\right)=K.
$$

> **Catatan sumber.** Pernyataan ini berlaku untuk setiap varietas
> proyektif terhubung di atas lapangan tertutup secara aljabar.
