---
title: "Lembar Kerja 29 - Proyeksi dan Kurva Proyektif Terparametrisasi"
stable_id: br-ak-2012-w29
language: id-ID
source_course: "Kurs:Algebraische Kurven (Osnabrück 2012)"
source_author: "Holger Brenner"
frozen_revision_contributor: "Arbota"
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2012)/Arbeitsblatt 29"
upstream_pageid: 50924
upstream_revid: 1052757
upstream_timestamp: "2025-08-27T18:11:31Z"
upstream_mediawiki_sha1: 0e8dd5d1e5b9bf9552bdbd8f8c61c47ee2a0b726
source_url: "https://de.wikiversity.org/w/index.php?oldid=1052757"
authority_manifest: authority/wikiversity/unit-29/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: ec3b34ad387ae827ecaa365c4def3b0550f74b629d0db3873a7cc28dc0831bc5
worksheet_xml: authority/wikiversity/unit-29/worksheet-29.xml
worksheet_xml_sha256: d82d020fef6e0d4f604bda9807f1befa2b8e1392afd9fb9459dbe17461d34574
worksheet_expanded_tex: authority/wikiversity/unit-29/worksheet-29-expanded.tex
worksheet_expanded_tex_sha256: 53a54b5b7e59be71c94d41dc791021c0b2d6165bf0b489670800b09387d560d2
exercise_map: authority/wikiversity/unit-29/ORDERED_EXERCISE_MAP.json
exercise_map_sha256: 75b07cabcb83cc12a6fd1259017f7e169c0ded461e7b7c94e65f033b71d12bc9
license: "Current semantic course text and this translation: CC BY-SA 4.0. Official PDF and media components retain their recorded component routes."
component_rights:
  - path: authority/assets/Lemniscate_of_Bernoulli.svg
    creator: "Zorgit"
    license: "Public domain"
  - path: authority/assets/Tschirnhausen_cubic-500.png
    creator: "Oleg Alexandrov"
    license: "Public domain"
no_blanket_relicensing_claim: true
independent_derivative_non_endorsement: true
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
exercise_count: 10
warm_up_exercises: "1-5"
submitted_exercises: "6-10"
authored_points: "1:2; 2:4; 3:3; 4:3; 5:4; 6:3; 7:3; 8:3; 9:3; 10:5"
starred_exercises: "2, 3"
displayed_points: "6:3; 7:3; 8:3; 9:3; 10:5"
public_solution_count: 2
public_solution_exercises: "2, 3"
source_corrections: 0
source_discrepancies: 1
discrepancy_ids: "AGC-U29-SRC-002"
component_discrepancies: 1
reader_media_positions: 2
---

# Lembar Kerja 29 {#br-ak-2012-w29}

## Soal pemanasan {#br-ak-2012-w29-warmup}

<!-- upstream_entity: Projektive ebene Kurve/Schnitt mit projektiver Geraden/Algebraisch abgeschlossen/Nicht leer/Aufgabe -->

### Soal 29.1 {#br-ak-2012-w29-ex01}

Misalkan $K$ suatu lapangan tertutup secara aljabar. Tunjukkan bahwa setiap
kurva bidang proyektif mempunyai perpotongan tak kosong dengan setiap garis
proyektif di bidang proyektif.

<!-- upstream_entity: Ebene algebraische Kurven/Z mod 5/Einheitskreis und x^3-2y^2+3/Durchschnitt und unendlich ferne Punkte/Aufgabe -->

### Soal 29.2 * {#br-ak-2012-w29-ex02}

Misalkan

$$
K=\mathbb Z/(5),
$$

dan perhatikan dua kurva aljabar bidang afin

$$
C=V(X^2+Y^2-1)
\qquad\text{dan}\qquad
D=V(X^3-2Y^2+3).
$$

a. Tentukan perpotongan $C\cap D$.

b. Tentukan titik-titik dalam

$$
V_+(X^2+Y^2-Z^2)\setminus V(X^2+Y^2-1).
$$

c. Tentukan titik-titik dalam

$$
V_+(X^3-2Y^2Z+3Z^3)\setminus V(X^3-2Y^2+3).
$$

d. Apakah $V_+(X^2+Y^2-Z^2)$ merupakan penutupan proyektif dari
$V(X^2+Y^2-1)$?

<!-- upstream_entity: Projektive Gerade/K-Punkte/Lokale Ringe isomorph/Aufgabe -->

### Soal 29.3 * {#br-ak-2012-w29-ex03}

Misalkan $K$ suatu lapangan. Tunjukkan bahwa semua gelanggang lokal pada garis
proyektif $\mathbb P_K^1$ saling isomorfik. Berikan deskripsi sesederhana
mungkin untuk gelanggang tersebut.

![Lemniskat Bernoulli. Karya Zorgit, domain publik.](authority/assets/Lemniscate_of_Bernoulli.svg){fig-alt="Lemniskat Bernoulli berbentuk angka delapan mendatar"}

<!-- upstream_entity: Lemniskate/Projektive Punkte/Aufgabe -->

### Soal 29.4 {#br-ak-2012-w29-ex04}

Untuk lemniskat Bernoulli yang diberikan oleh

$$
V\!\left((X^2+Y^2)^2-X^2+Y^2\right),
$$

tentukan singularitas-singularitasnya serta titik-titiknya di tak hingga dalam
$\mathbb P_{\mathbb C}^2$. Pada semua titik tersebut, hitung multiplisitas dan
garis-garis singgungnya.

<!-- upstream_entity: Algebraische Kurve/ZX^2 ist Y^3/Charakteristik null/Singuläre Punkte und Parametrisierung/Aufgabe -->

### Soal 29.5 {#br-ak-2012-w29-ex05}

Perhatikan kurva proyektif

$$
C\subset\mathbb P_K^2
$$

di atas lapangan $K$ berkarakteristik $0$ yang diberikan oleh persamaan homogen

$$
ZX^2=Y^3.
$$

a. Tentukan titik-titik singular kurva tersebut.

b. Tunjukkan bahwa penetapan

$$
\varphi:(S,T)\longmapsto(T^3,ST^2,S^3)=(X,Y,Z)
$$

memberikan pemetaan yang terdefinisi dengan baik

$$
\varphi:\mathbb P^1\longrightarrow\mathbb P^2.
$$

c. Tunjukkan bahwa titik-titik bayangan $\varphi$ terletak pada kurva $C$.

d. Titik-titik mana dalam $\mathbb P^1$ yang bersesuaian dengan titik-titik
singular kurva $C$?

## Soal untuk dikumpulkan {#br-ak-2012-w29-submit}

<!-- upstream_entity: Projektive Abbildung/Morphismus durch homogenen Polynome vom gleichen Grad/Auf offener Menge/Aufgabe -->

### Soal 29.6 (3 poin) {#br-ak-2012-w29-ex06}

Misalkan diberikan $m+1$ polinom homogen

$$
F_0,\ldots,F_m
$$

dalam $n+1$ variabel, semuanya berderajat sama $d$. Tunjukkan bahwa terdapat
himpunan terbuka

$$
U\subseteq\mathbb P_K^n
$$

sedemikian sehingga polinom-polinom tersebut mendefinisikan suatu morfisme

$$
\mathbb P_K^n\supseteq U\longrightarrow\mathbb P_K^m.
$$

<!-- upstream_entity: Projektiver Raum/Projektion weg von beliebigem Punkt/Matrixbeschreibung/Aufgabe -->

### Soal 29.7 (3 poin) {#br-ak-2012-w29-ex07}

Misalkan

$$
P=(a_0,\ldots,a_n)\in\mathbb P_K^n
$$

suatu titik di ruang proyektif. Tunjukkan bahwa proyeksi
$\mathbb P_K^n$ ke $\mathbb P_K^{n-1}$ dengan pusat $P$ diberikan oleh sebuah
matriks. Sumber tidak mencantumkan matriks tersebut. Setelah itu, sumber
menuliskan pemetaan

$$
\begin{pmatrix}
x_0\\
x_1\\
\vdots\\
x_n
\end{pmatrix}
\longmapsto
\begin{pmatrix}
x_0\\
x_1\\
\vdots\\
x_n
\end{pmatrix}.
$$

> **Ketidaksesuaian sumber AGC-U29-SRC-002.** Blok matriks pada sumber kosong,
> dan vektor yang ditampilkan sesudahnya diulangi tanpa perubahan sehingga
> tidak mendeskripsikan proyeksi ke $\mathbb P_K^{n-1}$. Edisi mempertahankan
> kedua fakta itu dan tidak menebak matriks atau pemetaan yang dimaksud.

!["Kubik Tschirnhausen" menurut keterangan sebaris kursus. Karya Oleg Alexandrov, domain publik.](authority/assets/Tschirnhausen_cubic-500.png){fig-alt="Ilustrasi merah sebuah kurva kubik bidang dengan titik ganda"}

> **Catatan komponen media.** Halaman deskripsi Commons untuk berkas ini
> memperingatkan bahwa, meskipun judul berkasnya demikian, kurva pada gambar
> bukan kubik Tschirnhausen karena sudut perpotongan pada titik gandanya
> berbeda. Gambar yang benar-benar dipakai sumber tetap dipertahankan.

<!-- upstream_entity: Tschirnhausen Kubik/Projektive Punkte/Aufgabe -->

### Soal 29.8 (3 poin) {#br-ak-2012-w29-ex08}

Untuk kubik Tschirnhausen yang diberikan oleh

$$
V(X^3+3X^2-Y^2),
$$

tentukan singularitas-singularitasnya dengan turut memperhitungkan titik-titik
di tak hingga. Tentukan garis-garis singgung pada singularitas-singularitas dan
pada titik-titik di tak hingga tersebut.

<!-- upstream_entity: Kartesisches Blatt/Projektive Punkte/Aufgabe -->

### Soal 29.9 (3 poin) {#br-ak-2012-w29-ex09}

Untuk folium Descartes yang didefinisikan oleh

$$
V(X^3+Y^3-3XY),
$$

tentukan titik-titiknya di tak hingga dalam $\mathbb P_{\mathbb C}^2$, lalu
hitung multiplisitas dan garis-garis singgung pada titik-titik tersebut.

<!-- upstream_entity: Lemniskate von Bernoulli/Projektiv/Abbildung auf Quadrik/Aufgabe -->

### Soal 29.10 (5 poin) {#br-ak-2012-w29-ex10}

Untuk lemniskat Bernoulli proyektif

$$
V_+\!\left((X^2+Y^2)^2-Z^2X^2+Z^2Y^2\right)
\subset\mathbb P_K^2,
$$

berikan suatu morfisme surjektif ke sebuah kuadrik proyektif. Berapa banyak
titik lemniskat yang dipetakan ke satu titik kuadrik itu?
