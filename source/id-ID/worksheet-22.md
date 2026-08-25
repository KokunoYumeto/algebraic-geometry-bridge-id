---
title: "Lembar Kerja 22 - Dimensi Penyematan, Singularitas, dan Garis Singgung"
stable_id: br-ak-2025-2026-w22
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Arbeitsblatt 22"
upstream_pageid: 165941
upstream_revid: 1062660
upstream_timestamp: "2025-12-19T12:06:58Z"
upstream_mediawiki_sha1: e82e91c94f0a39d73aa10913d6821f673925893e
source_url: "https://de.wikiversity.org/w/index.php?oldid=1062660"
authority_manifest: authority/wikiversity/unit-22/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: fefb7f6221a3e71b94649f03c75693f9eb34ec228cedf0af7d9e332aeda7d38a
worksheet_xml_sha256: 84114f9130aa04acd7db9ddd306a2c221a7fbd1f3dad29e51187c2211d015722
worksheet_expanded_tex_sha256: f72523eee3cc5d807be6435787581d95da6902348172780cad88423ab19f9e34
exercise_map: authority/wikiversity/unit-22/ORDERED_EXERCISE_MAP.json
exercise_map_sha256: d4b1d1f0a08de69d6fb7da513b8bce9ebaf697d5dad51632d0db063925d05f1e
license: "CC BY-SA 4.0"
component_rights:
  - path: authority/assets/Cercle_tangente_rayon.svg
    creator: "Christophe Dang Ngoc Chan (Cdang); karya turunan oleh Hagman"
    license: "CC BY-SA 3.0"
  - path: authority/assets/Cardioid.svg
    creator: "D.328"
    license: "CC BY-SA 3.0"
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_corrections: 2
---

# Lembar Kerja 22 {#br-ak-2025-2026-w22}

## Soal latihan {#br-ak-2025-2026-w22-practice}

<!-- upstream_entity: Achsenkreuz/3/Einbettungsdimension/Aufgabe -->

### Soal 22.1 {#br-ak-2025-2026-w22-ex-01}

Misalkan $R$ gelanggang lokal pada titik perpotongan ketiga sumbu koordinat
di ruang berdimensi tiga. Tentukan dimensi penyematannya.

<!-- upstream_entity: Raumkurve/Verschiedene Einbettungsdimensionen/Aufgabe -->

### Soal 22.2 {#br-ak-2025-2026-w22-ex-02}

Berikan contoh suatu kurva

$$
C\subseteq\mathbb A_K^n
$$

yang memiliki titik-titik $P_1,P_2,P_3\in C$ dengan dimensi penyematan
berturut-turut $1,2,3$.

<!-- upstream_entity: Ebene Kurve/Graph/Multiplizität/Tangente/Aufgabe -->

### Soal 22.3 {#br-ak-2025-2026-w22-ex-03}

Misalkan $H(X)\in K[X]$, $F=Y-H$, dan

$$
C=V(F)\subseteq\mathbb A_K^2
$$

grafik $H$ yang dipandang sebagai kurva aljabar bidang. Misalkan

$$
P=(a,b)=(a,H(a))
$$

suatu titik pada grafik tersebut.

1. Tunjukkan bahwa multiplisitas $C$ di $P$ sama dengan $1$.
2. Tunjukkan bahwa garis singgung pada $C$ di $P$ bertepatan dengan garis
   singgung biasa pada grafik di titik $a$.

<!-- upstream_entity: Polynomiale Abbildung/Kettenregel/Formal/Aufgabe -->

### Soal 22.4 {#br-ak-2025-2026-w22-ex-04}

Misalkan $K$ suatu lapangan dan

$$
F_1,\ldots,F_m\in K[X_1,\ldots,X_\ell]
$$

serta

$$
G_1,\ldots,G_n\in K[X_1,\ldots,X_m]
$$

polinom-polinom yang menghasilkan pemetaan polinomial

$$
\mathbb A_K^\ell\mathrel{\mathop{\longrightarrow}^{F}}
\mathbb A_K^m\mathrel{\mathop{\longrightarrow}^{G}}\mathbb A_K^n.
$$

Misalkan $J(F)_P$ dan $J(G)_Q$ matriks-matriks Jacobi yang didefinisikan
melalui pendiferensialan parsial formal. Buktikan aturan rantai formal

$$
J(G\circ F)_P=J(G)_{F(P)}\circ J(F)_P.
$$

<!-- upstream_entity: Homogenes Polynom/Partielle Ableitung/Dehomogenisierung/Aufgabe -->

### Soal 22.5 ★ {#br-ak-2025-2026-w22-ex-05}

1. Tunjukkan bahwa pendiferensialan parsial formal terhadap suatu variabel
   pada gelanggang polinomial $K[X_1,\ldots,X_n]$ komutatif dengan
   dehomogenisasi terhadap variabel lain.
2. Tunjukkan bahwa pernyataan tersebut tidak berlaku jika kedua operasi
   dilakukan terhadap variabel yang sama.

<!-- upstream_entity: Homogenes Polynom/Darstellung mit formalen partiellen Ableitungen/Aufgabe -->

### Soal 22.6 ★ {#br-ak-2025-2026-w22-ex-06}

Misalkan

$$
H\in K[X_1,\ldots,X_n]
$$

suatu polinom homogen berderajat $e$ dalam penggradasian standar. Tunjukkan
hubungan

$$
eH=X_1\frac{\partial H}{\partial X_1}+\cdots+
X_n\frac{\partial H}{\partial X_n}.
$$

<!-- upstream_entity: Affine Ebene/y ist 2x^4+3x^2-x+1/(1,5)/Transformation auf Nullpunkt, Tangente auf x-Achse/Aufgabe -->

### Soal 22.7 {#br-ak-2025-2026-w22-ex-07}

Tinjau kurva yang diberikan oleh

$$
y=2x^4+3x^2-x+1
$$

beserta titik

$$
P=(1, 5).
$$

Carilah suatu transformasi koordinat yang membawa $P$ ke titik $(0,0)$ dan
membawa garis singgung di $P$ ke sumbu-$x$.

<!-- upstream_entity: Ebene algebraische Kurve/Reduziert/Nur endlich viele singuläre Punkte/Aufgabe -->

### Soal 22.8 {#br-ak-2025-2026-w22-ex-08}

Misalkan $K$ suatu lapangan dan $F\in K[X,Y]$ suatu polinom tak konstan yang
faktor-faktor primanya semuanya sederhana. Misalkan

$$
C=V(F)
$$

kurva bidang yang terkait. Andaikan lebih lanjut bahwa $F$ tetap bebas faktor
berulang setelah perluasan skalar ke suatu ketertutupan aljabar dari $K$.
Tunjukkan bahwa
$C$ hanya memiliki berhingga banyak titik singular.

*Catatan edisi — koreksi hipotesis sumber:* Syarat bahwa faktor-faktor prima
$F$ sederhana hanya di $K[X,Y]$ tidak cukup jika $K$ tak sempurna. Misalnya,
di karakteristik $p>0$ sebuah polinom tereduksi di $K[X,Y]$ dapat menjadi
pangkat ke-$p$ setelah perluasan skalar, sehingga kedua turunan parsialnya nol
dan lokus singular geometrisnya berdimensi positif. Edisi ini menyatakan
syarat tepat yang diperlukan dalam argumen: $F$ tereduksi secara geometris.
Kondisi itu otomatis, misalnya, jika $K$ sempurna dan $F$ bebas faktor
berulang.

<!-- upstream_entity: Ebene algebraische Kurve/Glatter Punkt/Liegt nur auf einer Komponente/Fakt/Beweis/Aufgabe -->

### Soal 22.9 ★ {#br-ak-2025-2026-w22-ex-09}

Buktikan Lema 22.12.

![Diagram lingkaran dengan jari-jari menuju titik singgung dan garis singgung yang tegak lurus terhadap jari-jari tersebut](authority/assets/Cercle_tangente_rayon.svg)

*Gambar: Pada sebuah lingkaran, garis singgung di suatu titik tegak lurus
terhadap jari-jari yang menuju titik itu. Karya Christophe Dang Ngoc Chan
(Cdang), versi SVG turunan oleh Hagman; CC BY-SA 3.0.*

<!-- upstream_entity: Ebene algebraische Kurven/Einheitskreis/Bestimme Tangente/Aufgabe -->

### Soal 22.10 ★ {#br-ak-2025-2026-w22-ex-10}

Tunjukkan bahwa lingkaran satuan di atas suatu lapangan berkarakteristik
$\ne2$ adalah mulus, dan tentukan persamaan garis singgung di setiap
titiknya.

<!-- upstream_entity: Ebene algebraische Kurve/Glattheit/Graph von Polynom und rationaler Funktion/Aufgabe -->

### Soal 22.11 {#br-ak-2025-2026-w22-ex-11}

Misalkan $K$ suatu lapangan.

1. Tunjukkan bahwa grafik suatu polinom $F\in K[X]$ merupakan kurva aljabar
   mulus.
2. Misalkan $F,G\in K[X]$ polinom-polinom tanpa akar bersama. Tunjukkan bahwa
   grafik fungsi rasional $F/G$ juga merupakan kurva aljabar mulus.

<!-- upstream_entity: Ebene Kurve/-2x^3+3x^2y-y+2/3 \sqrt(1/3)/C/Singularitäten/Aufgabe -->

### Soal 22.12 ★ {#br-ak-2025-2026-w22-ex-12}

Tentukan titik-titik singular kurva aljabar bidang

$$
V\left(-2X^3+3X^2Y-Y+\frac{2}{3}\sqrt{\frac{1}{3}}\right)
\subseteq\mathbb A_{\mathbb C}^2.
$$

<!-- upstream_entity: Mechanisch definierte Kurven/Stangenkonfiguration/Kreis und tangentiale Gerade/Mittlere Trajektorie/Aufgabe -->

### Soal 22.13 {#br-ak-2025-2026-w22-ex-13}

Untuk lintasan yang dihitung dalam Contoh 8.5, tentukan koordinat titik-titik
tempat kurva tersebut singular.

<!-- upstream_entity: Ebene algebraische Kurve/x^3+xy^2/C/Singularitäten/Aufgabe -->

### Soal 22.14 ★ {#br-ak-2025-2026-w22-ex-14}

Tentukan faktorisasi prima polinom

$$
X^3+XY^2\in\mathbb C[X,Y],
$$

kemudian tentukan singularitas kurva afin yang terkait, beserta multiplisitas
dan garis-garis singgungnya.

<!-- upstream_entity: Ebene algebraische Kurve/y^4+x^3+3xy^2+2x^2y/C/Multiplizität und Tangenten/Aufgabe -->

### Soal 22.15 ★ {#br-ak-2025-2026-w22-ex-15}

Tentukan multiplisitas dan garis-garis singgung di titik asal $(0,0)$ dari
kurva aljabar bidang

$$
C=V\left(Y^4+X^3+3XY^2+2X^2Y\right)
\subseteq\mathbb A_{\mathbb C}^2.
$$

<!-- upstream_entity: Ebene Kurve/v^3+u^2v-2uv+2u^2-4u-2v/Bestimme Singularität/Aufgabe -->

### Soal 22.16 ★ {#br-ak-2025-2026-w22-ex-16}

Untuk lokus nol yang diberikan oleh polinom

$$
V^3+U^2V-2UV+2U^2-4U-2V,
$$

tentukan suatu titik singular dengan menggunakan turunan parsial. Lakukan
transformasi koordinat yang membawa titik tersebut ke titik asal. Tentukan
multiplisitas dan garis-garis singgung di titik itu.

*Catatan edisi — koreksi lingkup sumber:* Soal tidak menyebut lapangan dasar,
sedangkan solusi sumber membagi dengan $2$ dan $3$, lalu memfaktorkan dengan
$\sqrt3$. Untuk mengikuti solusi tersebut, andaikan
$\operatorname{char}(K)\notin\{2,3\}$ dan $\sqrt3\in K$ (misalnya
$K=\mathbb R$ atau $\mathbb C$). Di lapangan lain, titik yang ditemukan tetap
dapat diperiksa langsung, tetapi faktorisasi dan multiplisitas garis singgung
perlu dibaca di lapangan dasar yang bersangkutan; dalam karakteristik $2$,
kerucut tangennya mempunyai satu garis singgung ganda.

![Grafik kardioid simetris dengan titik runcing di sisi kiri dan lengkungan membulat di sisi kanan](authority/assets/Cardioid.svg)

*Gambar: Kardioid dengan persamaan polar $r=a(1+\cos\theta)$ untuk $a=1$.
Karya D.328; CC BY-SA 3.0.*

<!-- upstream_entity: Ebene algebraische Kurve/Kardioide/Singularitäten/Aufgabe -->

### Soal 22.17 {#br-ak-2025-2026-w22-ex-17}

Tentukan singularitas, termasuk multiplisitas dan garis-garis singgungnya,
dari kardioid yang diberikan oleh

$$
V\left(\left(X^2+Y^2\right)^2
-2X\left(X^2+Y^2\right)-Y^2\right).
$$

<!-- upstream_entity: Ebene Kurven/Lokale Diffeomorphie/Beispiel/1/Aufgabe -->

### Soal 22.18 ★ {#br-ak-2025-2026-w22-ex-18}

Tinjau dua kurva real

$$
V\left(X^5-X^3+2XY+7Y^2-9\right)
$$

di titik $(1,1)$ dan

$$
V\left(X^4+Y^4-3X^2Y^2+5X+7Y\right)
$$

di titik asal. Apakah kedua kurva ini secara lokal saling difeomorfik di
titik-titik yang diberikan tersebut?

## Soal untuk dikumpulkan {#br-ak-2025-2026-w22-submit}

<!-- upstream_entity: Formales Ableiten/Zwei Variablen/Positive Charakteristik/Eine partielle Ableitung und beide sind null/Charakterisiere/Aufgabe -->

### Soal 22.19 (3 poin) {#br-ak-2025-2026-w22-ex-19}

Misalkan $K$ suatu lapangan berkarakteristik $p\geq0$. Karakterisasikan
polinom-polinom $F\in K[X,Y]$ yang memenuhi masing-masing dari ketiga keadaan
berikut:

1. turunan parsial pertama sama dengan $0$;
2. turunan parsial kedua sama dengan $0$;
3. kedua turunan parsial sama dengan $0$.

<!-- upstream_entity: Ebene Kurve/x^3+y^3-3xy+1/Singularitäten und Tangenten über R und C/Aufgabe -->

### Soal 22.20 (4 poin) {#br-ak-2025-2026-w22-ex-20}

Untuk kurva

$$
V\left(X^3+Y^3-3XY+1\right),
$$

tentukan titik-titik singularnya di atas $\mathbb R$ dan di atas
$\mathbb C$. Dalam setiap kasus, berikan multiplisitas dan garis-garis
singgungnya.

<!-- upstream_entity: Ebene algebraische Kurve/Produkt/Einzelne Tangenten sind Tangenten/Aufgabe -->

### Soal 22.21 (3 poin) {#br-ak-2025-2026-w22-ex-21}

Misalkan $K$ suatu lapangan tertutup secara aljabar dan $G,H\in K[X,Y]$
polinom-polinom yang memenuhi

$$
G(P)=H(P)=0
$$

untuk suatu titik tertentu $P\in\mathbb A_K^2$. Misalkan $F=GH$. Tunjukkan
bahwa setiap garis singgung $G$ di $P$ dan setiap garis singgung $H$ di $P$
juga merupakan garis singgung $F$ di $P$.

<!-- upstream_entity: Ebene algebraische Kurve/x^3+5x^2y-6xy^2-x^2-xy+4y^2/Tangenten in (0,0) und (1,2)/Aufgabe -->

### Soal 22.22 (6 poin) {#br-ak-2025-2026-w22-ex-22}

Misalkan $K$ suatu lapangan tertutup secara aljabar. Tinjau kurva

$$
C=V\left(x^3+5x^2y-6xy^2-x^2-xy+4y^2\right).
$$

1. Tentukan garis-garis singgung di titik asal.
2. Tunjukkan bahwa

   $$
   P=(1,2)
   $$

   merupakan suatu titik pada kurva, dan hitung garis singgung (atau
   garis-garis singgung) $C$ di $P$ dengan menggunakan turunan.
3. Lakukan transformasi variabel sedemikian sehingga $P$ menjadi titik asal
   dalam variabel-variabel baru, lalu tentukan garis singgung (atau
   garis-garis singgung) di $P$ dari persamaan kurva yang telah
   ditransformasikan.

<!-- upstream_entity: Ebene algebraische Kurve/9y^4+10x^2y^2+x^4-12y^3-12x^2y+4y^2/Singularitäten und Multiplizität/Aufgabe -->

### Soal 22.23 (4 poin) {#br-ak-2025-2026-w22-ex-23}

Untuk kurva aljabar

$$
C=V\left(9y^4+10x^2y^2+x^4-12y^3-12x^2y+4y^2\right),
$$

tentukan singularitas-singularitasnya beserta multiplisitas dan garis-garis
singgungnya.

*Petunjuk sumber:* Bandingkan dengan Contoh 8.5.

---

**Provenans edisi.** Terjemahan dan produksi pembaca: OpenAI Codex
gpt-5.6-sol, Ultra. Sumber, pengarang, dan lisensi komponen dipertahankan
seperti dinyatakan dalam metadata dan berkas hak edisi.
