---
title: "Lembar Kerja 30 - Teorema Bézout"
stable_id: br-ak-2012-w30
language: id-ID
source_course: "Kurs:Algebraische Kurven (Osnabrück 2012)"
source_author: "Holger Brenner"
frozen_revision_contributor: "Bocardodarapti"
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2012)/Arbeitsblatt 30"
upstream_pageid: 50925
upstream_revid: 1112597
upstream_timestamp: "2026-08-21T16:19:24Z"
upstream_mediawiki_sha1: 2111599a8a79cbd491a5f334baf54bb39e9af931
source_url: "https://de.wikiversity.org/w/index.php?oldid=1112597"
authority_manifest: authority/wikiversity/unit-30/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 756ec1f9ea386b8ad0fac38086b6c97f0b94d6dc7a139dc4663911d48655bbe1
worksheet_xml: authority/wikiversity/unit-30/worksheet-30.xml
worksheet_xml_sha256: 0525c13b64a201759a6982c6f8885cc3fe456fb23abbd1be9ad1e1e6cc780382
worksheet_expanded_tex: authority/wikiversity/unit-30/worksheet-30-expanded.tex
worksheet_expanded_tex_sha256: c32bea5c89b6606a5171f79958a1dccded6575c4cca1ff4ca154fe5961800966
exercise_map: authority/wikiversity/unit-30/ORDERED_EXERCISE_MAP.json
exercise_map_sha256: 7b6ed646202784b0ae03782e76e751336516d2dda0ed17ecf70500ea2d7a491e
license: "Current semantic course text and this translation: CC BY-SA 4.0. Official PDF components retain their recorded component routes."
no_blanket_relicensing_claim: true
independent_derivative_non_endorsement: true
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra."
exercise_count: 12
warm_up_exercises: "1-4"
submitted_exercises: "5-12"
authored_points: "1:3; 2:3; 3:4; 4:7; 5:6; 6:5; 7:5; 8:4; 9:4; 10:4; 11:4; 12:5"
starred_exercises: "3, 4"
displayed_points: "5:6; 6:5; 7:5; 8:4; 9:4; 10:4; 11:4; 12:5"
displayed_points_total: 37
public_solution_count: 2
public_solution_exercises: "3, 4"
source_corrections: 1
correction_ids: "AGC-CORR-0133"
source_discrepancies: 1
discrepancy_ids: "AGC-U30-SRC-001"
reader_media_positions: 0
---

# Lembar Kerja 30: Teorema Bézout {#br-ak-2012-w30}

## Soal pemanasan {#br-ak-2012-w30-warmup}

<!-- upstream_entity: Schnitttheorie von Kurven/Satz von Bézout/Injektivität der Multiplikation mit Z im homogenen Restklassenring/Beispiel bei nicht algebraisch abgeschlossen/Aufgabe -->

### Soal 30.1 {#br-ak-2012-w30-ex01}

Berikan sebuah contoh yang menunjukkan bahwa Lemma 30.2 tidak berlaku jika
syarat bahwa lapangan dasarnya tertutup secara aljabar dihilangkan.

<!-- upstream_entity: Satz von Bézout/ZY^2-X^3 und (X-Z)^2+Y^2-1/Beispiel/Transversaler Schnitt/Aufgabe -->

### Soal 30.2 {#br-ak-2012-w30-ex02}

Tunjukkan bahwa kedua kurva pada Contoh 30.6 berpotongan secara transversal
di setiap titik perpotongan yang telah dihitung selain $(0,0)$.

<!-- upstream_entity: Ebene Kurven/Schnitt und Schnittmultiplizität/Y ist X^3 und Y^2 ist X^3/Aufgabe -->

### Soal 30.3 * {#br-ak-2012-w30-ex03}

Misalkan $K=\mathbb C$. Untuk dua kurva afin

$$
V(Y-X^3)
\qquad\text{dan}\qquad
V(Y^2-X^3),
$$

tentukan semua titik perpotongannya beserta multiplisitas perpotongan pada
setiap titik. Periksa pula titik-titik perpotongan dalam
$\mathbb P_{\mathbb C}^2$ dan konfirmasikan Teorema Bézout pada contoh ini.

<!-- upstream_entity: Ebene Kurven/Schnitt und Schnittmultiplizität/Y ist X^2 und Y^2 ist X^5/Aufgabe -->

### Soal 30.4 * {#br-ak-2012-w30-ex04}

Misalkan $K=\mathbb C$. Perhatikan dua kurva aljabar bidang

$$
C=V(X-Y^2)
\qquad\text{dan}\qquad
D=V(Y^2-X^5).
$$

Tentukan semua titik perpotongan kedua kurva pada bidang afin dan hitung
multiplisitas perpotongan pada setiap titik. Tentukan pula titik-titik di tak
hingga pada kedua kurva, yakni titik-titik tambahan pada penutupan proyektif
$\overline C$ dan $\overline D$, lalu periksa perpotongan di tak hingga.
Terakhir, konfirmasikan Teorema Bézout pada contoh ini.

> **Ketidaksesuaian sumber AGC-U30-SRC-001.** Judul halaman semantik sumber
> menyebut kurva pertama sebagai "$Y=X^2$", sedangkan rumus yang ditampilkan
> dalam soal dan solusi sumber sama-sama memakai $X=Y^2$. Edisi mengikuti
> rumus yang benar-benar ditampilkan dan tidak mengubah identitas halaman
> sumber yang dibekukan.

## Soal untuk dikumpulkan {#br-ak-2012-w30-submit}

<!-- upstream_entity: Projektive Kurve/Parametrisierung einer glatten Quadrik/Aufgabe -->

### Soal 30.5 (6 poin) {#br-ak-2012-w30-ex05}

Misalkan

$$
C\subseteq\mathbb P_K^2
$$

suatu kuadrik mulus, yakni kurva berderajat dua, di atas lapangan tertutup
secara aljabar. Tunjukkan bahwa $C$ isomorfik dengan garis proyektif
$\mathbb P_K^1$.

<!-- upstream_entity: Projektive ebene glatte Kurve/Grad d/Morphismus mit d-1 Faserpunkte/Aufgabe -->

### Soal 30.6 (5 poin) {#br-ak-2012-w30-ex06}

Misalkan $K$ suatu lapangan tertutup secara aljabar dan

$$
C\subset\mathbb P_K^2
$$

suatu kurva mulus berderajat $d\geq2$. Tunjukkan bahwa terdapat morfisme

$$
C\longrightarrow\mathbb P_K^1
$$

sedemikian sehingga setiap serat terdiri atas paling banyak $d-1$ titik.

<!-- upstream_entity: Ebene projektive Kurven/Fermat-Kubik auf P^1/2 zu 1/Aufgabe -->

### Soal 30.7 (5 poin) {#br-ak-2012-w30-ex07}

Misalkan

$$
C=V_+(X^3+Y^3+Z^3)\subseteq\mathbb P_K^2
$$

adalah kubik Fermat di atas lapangan tertutup secara aljabar dengan
karakteristik bukan $3$. Deskripsikan secara eksplisit suatu morfisme

$$
C\longrightarrow\mathbb P_K^1
$$

yang setiap seratnya memuat paling banyak dua titik.

<!-- upstream_entity: Der komplex-projektive Einheitskreis/Explizite bijektive Parametrisierung/Aufgabe -->

### Soal 30.8 (4 poin) {#br-ak-2012-w30-ex08}

Misalkan

$$
C\subseteq\mathbb P_{\mathbb C}^2
$$

adalah penutupan kompleks-proyektif dari lingkaran satuan. Tentukan suatu
parametrisasi bijektif yang eksplisit

$$
\mathbb P_{\mathbb C}^1\longrightarrow C.
$$

<!-- upstream_entity: Satz von Bézout/Bestätige für ZY^2-X^3 und X^2+(Y-Z)^2-Z^2/Aufgabe -->

### Soal 30.9 (4 poin) {#br-ak-2012-w30-ex09}

Di atas $\mathbb C$, konfirmasikan Teorema Bézout untuk dua kurva bidang
proyektif

$$
C=V_+(ZY^2-X^3)
$$

dan

$$
D=V_+\!\left(X^2+(Y-Z)^2-Z^2\right).
$$

Buat sketsa situasinya.

<!-- upstream_entity: Satz von Bézout/Bestätige für ZY-X^2 und X^2+(Y-Z)^2-Z^2/Aufgabe -->

### Soal 30.10 (4 poin) {#br-ak-2012-w30-ex10}

Di atas $\mathbb C$, konfirmasikan Teorema Bézout untuk dua kurva bidang
proyektif

$$
C=V_+(ZY-X^2)
$$

dan

$$
D=V_+\!\left(X^2+(Y-Z)^2-Z^2\right).
$$

Buat sketsa situasinya.

> **Catatan cakupan AGC-CORR-0133.** Sumber Soal 30.9 dan 30.10 tidak
> menyatakan lapangan dasar. Edisi menyatakan $\mathbb C$ secara eksplisit,
> sesuai pembacaan geometris dan perintah membuat sketsa; pada karakteristik
> $2$, bentuk kuadratik kedua merosot menjadi kuadrat sebuah garis sehingga
> perhitungan yang dimaksud tidak lagi sama.

<!-- upstream_entity: Satz von Bézout/Bestätige für X^2-Y^3 und X^5-Y^4/Aufgabe -->

### Soal 30.11 (4 poin) {#br-ak-2012-w30-ex11}

Konfirmasikan Teorema Bézout untuk dua kurva monomial yang secara afin
diberikan oleh

$$
C=V(X^2-Y^3)
$$

dan

$$
D=V(X^5-Y^4).
$$

<!-- upstream_entity: Modultheorie/Exakte Komplexe/Kurze exakte Sequenzen/Hom-Funktoren/Aufgabe -->

### Soal 30.12 (5 poin) {#br-ak-2012-w30-ex12}

Misalkan $R$ suatu gelanggang komutatif dan $M,N$ modul-$R$. Jika

$$
f:M\longrightarrow N
$$

suatu homomorfisme modul-$R$, maka pemetaan

$$
\begin{aligned}
f^*:\operatorname{Hom}(N,R)&\longrightarrow\operatorname{Hom}(M,R),\\
\varphi&\longmapsto\varphi\circ f
\end{aligned}
$$

juga merupakan homomorfisme modul-$R$.

Sekarang misalkan

$$
0\longrightarrow M\longrightarrow N\longrightarrow P\longrightarrow0
$$

suatu barisan eksak pendek modul-$R$. Tunjukkan bahwa barisan terinduksi

$$
0\longrightarrow\operatorname{Hom}(P,R)
\longrightarrow\operatorname{Hom}(N,R)
\longrightarrow\operatorname{Hom}(M,R)
$$

eksak. Berikan pula sebuah contoh dengan $R=\mathbb Z$ yang menunjukkan bahwa
panah terakhir pada umumnya tidak surjektif.
