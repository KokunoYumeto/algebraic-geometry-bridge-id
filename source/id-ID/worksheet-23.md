---
title: "Lembar Kerja 23 - Derivasi, Multiplisitas Hilbert-Samuel, dan Dimensi Krull"
stable_id: br-ak-2025-2026-w23
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Arbeitsblatt 23"
upstream_pageid: 165942
upstream_revid: 1062659
upstream_timestamp: "2025-12-19T12:06:03Z"
upstream_mediawiki_sha1: 19554b41098b4f02ac6e558145036ca293e4bbc9
source_url: "https://de.wikiversity.org/w/index.php?oldid=1062659"
authority_manifest: authority/wikiversity/unit-23/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: f7ee49a4bfa589b831c1fdb69e6f091ac1762d9da019a133670e4e0d723d34ae
worksheet_xml_sha256: 98b40a9acd3a8da5e5b743b8245b2690007abdbbc6d7fa7b2106e2871560dabc
worksheet_expanded_tex_sha256: 865905ee0d321006682c162fb2d9e272f1fc251e61b8dde9844981f6baba9c0f
exercise_map: authority/wikiversity/unit-23/ORDERED_EXERCISE_MAP.json
exercise_map_sha256: fdfec83fe1ef4f0d87eca194f2991805cd69ff2af070b73ef83c0ba1c9d1e4c4
license: "CC BY-SA 4.0"
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_corrections: 1
reader_media_positions: 0
---

# Lembar Kerja 23 {#br-ak-2025-2026-w23}

## Soal latihan {#br-ak-2025-2026-w23-practice}

<!-- upstream_entity: Polynomring/Partielle Ableitung/Derivation/Aufgabe -->

### Soal 23.1 {#br-ak-2025-2026-w23-ex-01}

Misalkan $K$ suatu lapangan, $K[X_1,\ldots,X_n]$ gelanggang polinom atas
$K$, dan

$$
\frac{\partial}{\partial X_1}
$$

turunan parsial formal terhadap $X_1$, yaitu pemetaan

$$
\begin{aligned}
K[X_1,\ldots,X_n]&\longrightarrow K[X_1,\ldots,X_n],\\
f&\longmapsto\frac{\partial f}{\partial X_1}.
\end{aligned}
$$

Tunjukkan bahwa pemetaan ini merupakan derivasi-$K$.

<!-- upstream_entity: Polynomring/Maximales Ideal/Potenzen/Restklassenbasis/Aufgabe -->

### Soal 23.2 {#br-ak-2025-2026-w23-ex-02}

Tinjau ideal maksimal

$$
\mathfrak m=(X_1,\ldots,X_n)
\subseteq K[X_1,\ldots,X_n]
$$

dalam gelanggang polinom atas suatu lapangan $K$, beserta pangkat-pangkat
$\mathfrak m^d$. Tunjukkan bahwa monom-monom

$$
X_1^{\nu_1}\cdots X_n^{\nu_n},
\qquad \sum_{i=1}^n\nu_i<d,
$$

membentuk suatu basis atas $K$ bagi gelanggang faktor

$$
K[X_1,\ldots,X_n]/\mathfrak m^d.
$$

<!-- upstream_entity: Achsenkreuz/R mod m^n/Basis und Hilbert Funktion/Berechne/Aufgabe -->

### Soal 23.3 {#br-ak-2025-2026-w23-ex-03}

Tinjau perpotongan sumbu

$$
V(xy)\subseteq\mathbb A_K^2
$$

dan gelanggang lokal $R$ yang bersesuaian dengan titik asal, dengan ideal
maksimal $\mathfrak m$. Deskripsikan secara eksplisit suatu basis atas $K$
bagi gelanggang faktor $R/\mathfrak m^n$, lalu tentukan dimensinya.

<!-- upstream_entity: Polynomring/2/Multiplizität/Multiplikation/Aufgabe -->

### Soal 23.4 ★ {#br-ak-2025-2026-w23-ex-04}

Misalkan

$$
F=F_m+\cdots+F_d\in K[X,Y]
$$

dekomposisi homogen suatu polinom, dengan $m\le d$, dan misalkan
$\mathfrak m=(X,Y)$. Tunjukkan bahwa, untuk setiap $n\ge m$, pemetaan
perkalian

$$
\begin{aligned}
K[X,Y]&\longrightarrow K[X,Y],\\
G&\longmapsto FG
\end{aligned}
$$

menginduksi homomorfisme modul-$K[X,Y]$ yang terdefinisi dengan baik dan
injektif

$$
K[X,Y]/\mathfrak m^{n-m}
\longrightarrow
K[X,Y]/\mathfrak m^n.
$$

<!-- upstream_entity: Numerisches Monoid/N ab e/Hilbert-Funktion/Aufgabe -->

### Soal 23.5 ★ {#br-ak-2025-2026-w23-ex-05}

Misalkan $e\in\mathbb N_+$ dan

$$
M:=\{0\}\cup\mathbb N_{\ge e}\subseteq\mathbb N.
$$

1. Tentukan $nM_+$ untuk $n\in\mathbb N_+$.
2. Tentukan $\#(M\setminus nM_+)$.
3. Misalkan $K$ suatu lapangan dan tetapkan

   $$
   R=K[M]_{\mathfrak m},
   \qquad
   \mathfrak m=K[M_+]\subseteq K[M].
   $$

   Tentukan $\dim_K(R/\mathfrak m^n)$.

<!-- upstream_entity: Numerisches Monoid/Abschätzungen für Multiplizität und Differenzanzahl/4,9/bis n ist 6/Aufgabe -->

### Soal 23.6 {#br-ak-2025-2026-w23-ex-06}

Untuk monoid numerik $M\subseteq\mathbb N$ yang dibangkitkan oleh $4$ dan
$9$, hitunglah besaran-besaran yang muncul dalam taksiran Lema 23.8 hingga
$n\le6$.

## Dimensi Krull {#br-ak-2025-2026-w23-krull}

Beberapa soal berikut menggunakan dimensi Krull suatu gelanggang komutatif.
Karena perhatian utama kita adalah kurva, yang bersesuaian dengan gelanggang
berdimensi satu, kita tidak akan mengembangkan teori dimensi secara
sistematis.

<!-- upstream_entity: Kommutative Ringtheorie/Primidealkette/Krulldimension/Definition -->

### Definisi: rantai ideal prima dan dimensi Krull {#br-ak-2025-2026-w23-def-01}

Misalkan $R$ suatu gelanggang komutatif. Suatu rantai ideal prima

$$
\mathfrak p_0
\subset
\mathfrak p_1
\subset
\cdots
\subset
\mathfrak p_n
$$

disebut *rantai ideal prima dengan panjang $n$*. Jadi yang dihitung adalah
banyaknya inklusi, bukan banyaknya ideal prima dalam rantai. *Dimensi* atau
*dimensi Krull* $R$ adalah supremum semua panjang rantai ideal prima dan
ditulis

$$
\dim(R).
$$

<!-- upstream_entity: Krulldimension/Hauptidealbereich, kein Körper/Krulldimension 1/Aufgabe -->

### Soal 23.7 {#br-ak-2025-2026-w23-ex-07}

Misalkan $R$ suatu domain ideal utama yang bukan lapangan. Tunjukkan bahwa
dimensi Krull $R$ sama dengan satu.

## Soal untuk dikumpulkan {#br-ak-2025-2026-w23-submitted}

<!-- upstream_entity: Numerisches Monoid/Abschätzungen für Multiplizität und Differenzanzahl/5,8,11/bis n ist 5/Aufgabe -->

### Soal 23.8 (4 poin) {#br-ak-2025-2026-w23-ex-08}

Untuk monoid $M\subseteq\mathbb N$ yang dibangkitkan oleh $5,8,11$, hitunglah
besaran-besaran yang muncul dalam taksiran Lema 23.8 hingga $n\le5$.

<!-- upstream_entity: Kommutative Ringtheorie/Ideal mit nur einem einzigen maximalen Oberideal/Restklassenring direkt und nach Lokalisierung/Aufgabe -->

### Soal 23.9 (3 poin) {#br-ak-2025-2026-w23-ex-09}

Misalkan $\mathfrak a\subseteq R$ suatu ideal dalam gelanggang komutatif,
dan andaikan satu-satunya ideal prima yang memuat $\mathfrak a$ adalah suatu
ideal maksimal $\mathfrak m$. Tunjukkan bahwa

$$
R/\mathfrak a
\cong
R_{\mathfrak m}/\mathfrak aR_{\mathfrak m}.
$$

Simpulkan bahwa, bagi suatu ideal maksimal $\mathfrak m$ dalam gelanggang
komutatif Noether, berlaku isomorfisme

$$
R/\mathfrak m^n
\cong
R_{\mathfrak m}/\mathfrak m^nR_{\mathfrak m}
$$

untuk setiap $n$.

<!-- upstream_entity: Krulldimension/Algebraisch abgeschlossener Körper/Affine Ebene ist zweidimensional/Aufgabe -->

### Soal 23.10 (5 poin) {#br-ak-2025-2026-w23-ex-10}

Misalkan $K$ suatu lapangan tertutup secara aljabar dan
$R=K[X,Y]$ gelanggang polinom dalam dua variabel. Tunjukkan bahwa $R$
mempunyai dimensi Krull dua.

<!-- upstream_entity: Krulldimension/Noethersch/Charakterisierung von nulldimensional/Fakt/Beweis/Aufgabe -->

### Soal 23.11 (5 poin) {#br-ak-2025-2026-w23-ex-11}

Misalkan $R$ suatu gelanggang komutatif Noether. Tunjukkan bahwa pernyataan
berikut ekuivalen.

1. $R$ mempunyai dimensi Krull $0$.
2. $R$ merupakan gelanggang Artin.
3. $R$ mempunyai berhingga banyak ideal prima dan semuanya maksimal.
4. Terdapat $n\in\mathbb N$ sehingga

   $$
   (\mathfrak mR_{\mathfrak m})^n=0
   $$

   untuk setiap ideal maksimal $\mathfrak m$.
5. Reduksi $R_{\mathrm{red}}=R/\sqrt{(0)}$ merupakan hasil kali hingga
   lapangan-lapangan.

*Catatan edisi -- koreksi pernyataan sumber:* Butir (4) pada sumber menuliskan
$\mathfrak m^n=0$ di $R$ untuk setiap ideal maksimal. Pernyataan itu tidak
ekuivalen dengan empat butir lainnya; misalnya, pada $R=K\times K$ kedua
ideal maksimal bersifat idempoten, bukan nilpoten, meskipun $R$ berdimensi
nol dan Artin. Edisi menggantinya dengan formulasi lokal seragam di atas,
yang merupakan karakterisasi yang benar bagi gelanggang Noether berdimensi
nol. Kata “hasil kali” pada butir (5) juga dinyatakan sebagai hasil kali
*hingga*, sebagaimana dipaksakan oleh kondisi Noether/Artin.

<!-- upstream_entity: Krulldimension/Dimension des Polynomringes ist mindestens eins größer/Aufgabe -->

### Soal 23.12 (3 poin) {#br-ak-2025-2026-w23-ex-12}

Misalkan $R$ suatu gelanggang komutatif dengan dimensi Krull hingga $d$.
Tunjukkan bahwa dimensi Krull gelanggang polinom $R[X]$ sedikitnya $d+1$.

*Catatan sumber:* Jika gelanggang dasar Noether, peralihan ke gelanggang
polinom menaikkan dimensi tepat satu; membuktikan hasil yang lebih kuat itu
lebih sulit.
