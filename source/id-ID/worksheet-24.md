---
title: "Lembar Kerja 24 - Deret Pangkat Formal dan Garis Singgung"
stable_id: br-ak-2012-w24
language: id-ID
source_course: "Kurs:Algebraische Kurven (Osnabrück 2012)"
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2012)/Arbeitsblatt 24"
upstream_pageid: 50759
upstream_revid: 793492
upstream_timestamp: "2022-08-25T06:03:47Z"
upstream_mediawiki_sha1: 507a5966770c007e813734ca85da4e85f8a93b60
source_url: "https://de.wikiversity.org/w/index.php?oldid=793492"
authority_manifest: authority/wikiversity/unit-24/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 3731896a5980c565d9d69a2e01eee497f13b6f449f2f9c701fce726271c026a5
worksheet_xml_sha256: c6b2e329dc1326aef1b0372702a03fba7fc7106c9e866498df92e1fc9508d4b2
worksheet_expanded_tex_sha256: 37b53c3b6049ba45ff4aa1f4b7b4c4f0666e8a97248ba3c6c34a38061b758a4f
exercise_map: authority/wikiversity/unit-24/ORDERED_EXERCISE_MAP.json
exercise_map_sha256: 250744d177bc2d5cf2a1cc506a99e05f1250c771de88b214a0e8d5cabfe7b9b8
license: "CC BY-SA 4.0"
source_component_license_route: "Sumber semantik: CC BY-SA 4.0; PDF historis resmi mempertahankan pemberitahuan CC BY-SA 2.0 Jerman dan CC BY-SA 4.0"
no_blanket_relicensing_claim: true
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_corrections: 1
reader_media_positions: 0
---

# Lembar Kerja 24 {#br-ak-2012-w24}

## Soal latihan {#br-ak-2012-w24-practice}

<!-- upstream_entity: Ebene algebraische Kurve/Glatt/Parametrisierung ist singulär/Aufgabe -->

### Soal 24.1 {#br-ak-2012-w24-ex-01}

Berikan sebuah contoh kurva mulus

$$
C\subseteq\mathbb A_K^2
$$

yang memiliki suatu parametrisasi dengan diferensial yang bernilai nol pada
setidaknya satu titik.

<!-- upstream_entity: Achsenkreuz/R mod m^n/Basis und Hilbert Funktion/Berechne/Aufgabe -->

### Soal 24.2 {#br-ak-2012-w24-ex-02}

Tinjau perpotongan sumbu

$$
V(xy)\subseteq\mathbb A_K^2
$$

dan gelanggang lokal $R$ yang bersesuaian dengan titik asal, dengan ideal
maksimal $\mathfrak m$. Deskripsikan secara eksplisit suatu basis atas $K$
bagi gelanggang faktor $R/\mathfrak m^n$, lalu tentukan dimensinya.

<!-- upstream_entity: Formale Potenzreihe/Inverses von 1-T/Aufgabe -->

### Soal 24.3 {#br-ak-2012-w24-ex-03}

Misalkan $K$ suatu lapangan dan $K[[T]]$ gelanggang deret pangkat formal.
Tentukan deret pangkat yang merupakan invers dari $1-T$.

<!-- upstream_entity: Potenzreihenring eine Variable/Abbildung der Lokalisierung an maximalen Ideal/Aufgabe -->

### Soal 24.4 ★ {#br-ak-2012-w24-ex-04}

Misalkan $K$ suatu lapangan dan

$$
\mathfrak m=(T)\subseteq K[T]
$$

ideal maksimal yang bersesuaian dengan titik asal, dengan pelokalan

$$
R=K[T]_{\mathfrak m}.
$$

Definisikan suatu homomorfisme aljabar-$K$

$$
\varphi:R\longrightarrow K[[T]]
$$

yang memenuhi $\varphi(T)=T$, dengan $K[[T]]$ menyatakan gelanggang deret
pangkat formal.

<!-- upstream_entity: Potenzreihe/Eine Variable/Einsetzen/Erste vier Glieder/Aufgabe -->

### Soal 24.5 {#br-ak-2012-w24-ex-05}

Hitung lima koefisien pertama, sampai dengan dan termasuk $c_4$, dari deret
pangkat hasil substitusi $F(G)$ dalam pengertian Definisi 24.9.

## Soal untuk dikumpulkan {#br-ak-2012-w24-submitted}

<!-- upstream_entity: Polynom in zwei Variablen/Identische partielle Ableitungen/über R und C/Aufgabe -->

### Soal 24.6 (5 poin) {#br-ak-2012-w24-ex-06}

Berikan contoh suatu polinom real tak tereduksi

$$
F\in\mathbb R[X,Y]
$$

sedemikian sehingga kedua turunan parsialnya sama dan tidak konstan.
Tunjukkan bahwa hal ini tidak mungkin terjadi di atas $\mathbb C$.

<!-- upstream_entity: Ebene algebraische Kurve/x^2 ist y^2+y^3/Singulärer Punkt, Tangenten/Parametrisierung t ist 1,0,-1 /Aufgabe -->

### Soal 24.7 (3 poin) {#br-ak-2012-w24-ex-07}

Tinjau kurva

$$
C=V\left(Y^2-X^2-X^3\right)
$$

dengan parametrisasi yang dibahas dalam Contoh 24.3. Tentukan titik-titik
singular kurva beserta multiplisitas dan garis singgungnya. Hitung pula
titik-titik citra dan garis-garis singgung untuk nilai parameter

$$
t=-1,0,1.
$$

Untuk kesimpulan geometris tentang garis singgung dan nilai parameter di
atas, ambil lapangan dasar $\mathbb R$; khususnya, lapangan tersebut
berkarakteristik nol.

*Catatan edisi - koreksi persamaan sumber:* Sumber menampilkan
$C=V(X^2-Y^2-Y^3)$, tetapi parametrisasi yang dirujuk adalah

$$
(x,y)=\left(t^2-1,t(t^2-1)\right).
$$

Substitusi langsung memberi

$$
y^2-x^2-x^3
=(t^2-1)^2\left(t^2-1-(t^2-1)\right)=0.
$$

Karena itu edisi memakai $C=V(Y^2-X^2-X^3)$, sesuai dengan parametrisasi
dan kategori objek sumber.

<!-- upstream_entity: Potenzreihe über C, die nirgendwo konvergiert/Aufgabe -->

### Soal 24.8 (3 poin) {#br-ak-2012-w24-ex-08}

Deskripsikan suatu deret pangkat formal di atas $\mathbb C$ yang tidak
konvergen pada lingkungan mana pun dari titik asal.

<!-- upstream_entity: Potenzreihenring und Polynomring/Reihenfolge/Vergleiche/Aufgabe -->

### Soal 24.9 (3 poin) {#br-ak-2012-w24-ex-09}

Misalkan $K$ suatu lapangan. Bandingkan kedua gelanggang

$$
(K[X])[[Y]]
\qquad\text{dan}\qquad
(K[[Y]])[X].
$$

Secara khusus, tentukan apakah salah satunya termuat dalam yang lain dan,
jika demikian, tentukan arah inklusinya.

<!-- upstream_entity: Hilberts Basissatz/Erweiterung auf Potenzreihenringe/Aufgabe -->

### Soal 24.10 (6 poin) {#br-ak-2012-w24-ex-10}

Misalkan $R$ suatu gelanggang komutatif Noether. Tunjukkan bahwa

$$
R[[T_1,\ldots,T_n]]
$$

bersifat Noether.

> **Petunjuk.** Ambillah inspirasi dari bukti Teorema Basis Hilbert.

