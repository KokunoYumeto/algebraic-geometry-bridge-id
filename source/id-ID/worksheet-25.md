---
title: "Lembar Kerja 25 - Solusi Deret Pangkat bagi Kurva Aljabar"
stable_id: br-ak-2012-w25
language: id-ID
source_course: "Kurs:Algebraische Kurven (Osnabrück 2012)"
source_author: "Holger Brenner"
frozen_revision_contributor: "Arbota"
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2012)/Arbeitsblatt 25"
upstream_pageid: 50760
upstream_revid: 793493
upstream_timestamp: "2022-08-25T06:03:57Z"
upstream_mediawiki_sha1: 1418cec6171ff8fd056dda7e6461f5ca4d91d910
source_url: "https://de.wikiversity.org/w/index.php?oldid=793493"
authority_manifest: authority/wikiversity/unit-25/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 7cafbca7b5fd080529c2019967647ef8ffa823539b2113caaf0ad65e56d6afc1
worksheet_xml_sha256: f682934e1b3b2cc74a078af4611c56de2aa73b41cfa5d61edf406ff7b13601f7
worksheet_expanded_tex_sha256: 40661bb4202b74ed245da30306df0456c3b60d17ee62e054871386a70300514e
exercise_map: authority/wikiversity/unit-25/ORDERED_EXERCISE_MAP.json
exercise_map_sha256: 1a887b81de9ccf9707e1e4835e477f9c9fb4a4358ab697242b17fd29873e8370
license: "CC BY-SA 4.0"
source_component_license_route: "Sumber semantik: CC BY-SA 4.0; PDF historis resmi mempertahankan pemberitahuan CC BY-SA 2.0 Jerman dan CC BY-SA 4.0"
no_blanket_relicensing_claim: true
independent_derivative_non_endorsement: true
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_corrections: 2
correction_ids: "AGC-CORR-0094; AGC-CORR-0095"
source_discrepancies: 1
source_discrepancy_ids: "AGC-CORR-0096; AGC-U25-POINT-001"
reader_media_positions: 0
---

# Lembar Kerja 25 {#br-ak-2012-w25}

## Soal latihan {#br-ak-2012-w25-practice}

<!-- upstream_entity: Ebene algebraische Kurve/Potenzreihenansatz/x^3+y^2-xy+x/Nullpunkt/Aufgabe -->

### Soal 25.1 ★ {#br-ak-2012-w25-ex-01}

Untuk kurva aljabar bidang

$$
V\left(X^3+Y^2-XY+X\right),
$$

tentukan suatu solusi deret pangkat tak konstan

$$
X=F(Y)
$$

di titik asal sampai dengan suku keenam.

<!-- upstream_entity: Ebene algebraische Kurve/Potenzreihenansatz/x^2y+x^2+y^2-5xy+y/Nullpunkt/Aufgabe -->

### Soal 25.2 ★ {#br-ak-2012-w25-ex-02}

Untuk kurva aljabar bidang

$$
V\left(X^2Y+X^2+Y^2-5XY+Y\right),
$$

tentukan suatu solusi deret pangkat tak konstan

$$
Y=F(X)
$$

di titik asal sampai dengan orde kelima.

Soal-soal berikut membahas kompletasi suatu gelanggang lokal.

<!-- upstream_entity: Komplettierung eines lokalen Ringes/Begriff und kanonische Abbildung/Aufgabe -->

### Soal 25.3 {#br-ak-2012-w25-ex-03}

Misalkan $R$ suatu gelanggang lokal dengan ideal maksimal $\mathfrak m$.
Tinjau diagram

$$
\longrightarrow R/\mathfrak m^4
\longrightarrow R/\mathfrak m^3
\longrightarrow R/\mathfrak m^2
\longrightarrow R/\mathfrak m.
$$

Pemetaan-pemetaan tersebut adalah proyeksi kanonik

$$
\varphi_n:R/\mathfrak m^{n+1}\longrightarrow R/\mathfrak m^n
$$

yang diinduksi oleh inklusi ideal
$\mathfrak m^{n+1}\subseteq\mathfrak m^n$. Suatu barisan unsur

$$
a_n\in R/\mathfrak m^n
$$

disebut *kompatibel* apabila

$$
\varphi_n(a_{n+1})=a_n
$$

untuk setiap $n$. Definisikan struktur gelanggang pada himpunan semua
barisan kompatibel tersebut. Gelanggang ini disebut *kompletasi* $R$.
Tunjukkan pula bahwa terdapat suatu homomorfisme gelanggang kanonik dari
$R$ ke kompletasinya.

<!-- upstream_entity: Komplettierung eines lokalen Ringes/Eindimensional/Injektivität der kanonischen Abbildung/Aufgabe -->

### Soal 25.4 {#br-ak-2012-w25-ex-04}

Misalkan $R$ suatu gelanggang komutatif lokal Noether berdimensi satu.
Tunjukkan bahwa pemetaan kanonik dari $R$ ke kompletasi $R$ bersifat
injektif.

> **Catatan.** Injektivitas tersebut berlaku untuk setiap gelanggang lokal
> Noether, tetapi pembuktiannya lebih sulit.

<!-- upstream_entity: Kommutative Ringtheorie/Ideal-adische Topologie eines Rings/Aufgabe -->

### Soal 25.5 {#br-ak-2012-w25-ex-05}

Misalkan $R$ suatu gelanggang komutatif dan $I$ suatu ideal. Tunjukkan bahwa,
untuk setiap $x\in R$, keluarga

$$
\left\{x+I^n\mid n\in\mathbb N\right\}
$$

mendefinisikan suatu basis lingkungan di $x$. Keluarga-keluarga ini
mendefinisikan topologi $I$-adik pada $R$. Tunjukkan pula bahwa topologi
tersebut bersifat Hausdorff jika dan hanya jika

$$
\bigcap_n I^n=\{0\}.
$$

> **Catatan.** Kompletasi suatu gelanggang lokal terhadap ideal maksimalnya
> tepat sama dengan kompletasi topologis terhadap topologi
> ini.

## Soal untuk dikumpulkan {#br-ak-2012-w25-submitted}

<!-- upstream_entity: Ebene algebraische Kurve/Kardioide/Potenzreihe in (2,0) bis Term c4/Aufgabe -->

### Soal 25.6 (4 poin) {#br-ak-2012-w25-ex-06}

Tinjau kardioid

$$
V\left(\left(X^2+Y^2\right)^2
-2X\left(X^2+Y^2\right)-Y^2\right)
$$

di titik $(2,0)$. Tentukan suatu parametrisasi formal kurva di titik ini,
sampai dengan suku kelima, dalam suatu parameter garis singgung.

> **Catatan edisi - lingkup lapangan.** Sumber tidak menyebut lapangan dasar.
> Untuk interpretasi geometris kardioid dan parameter garis singgung pada soal
> ini, edisi memakai lapangan dasar $\mathbb R$; khususnya, lapangan tersebut
> berkarakteristik nol.

<!-- upstream_entity: Potenzreihe/Lösung für Einheitskreis/Aufgabe -->

### Soal 25.7 (4 poin) {#br-ak-2012-w25-ex-07}

Misalkan $K$ suatu lapangan dengan $\operatorname{char}(K)\ne2$. Tinjau
lingkaran satuan

$$
X^2+Y^2=1
$$

di titik $(1,0)$. Tentukan deret pangkat

$$
G,H\in K[[T]]
$$

dengan syarat awal

$$
a_0=1,\qquad a_1=0,\qquad b_0=0,\qquad b_1=1,
$$

dan yang memenuhi

$$
G(T)^2+H(T)^2=1.
$$

> **Catatan edisi - karakteristik.** Sumber tidak membatasi karakteristik
> $K$. Syarat $\operatorname{char}(K)\ne2$ ditambahkan karena, dalam
> karakteristik $2$, koefisien $T^2$ pada persamaan yang diminta akan memaksa
> $1=0$, sehingga deret dengan syarat awal tersebut tidak mungkin ada.

<!-- upstream_entity: Potenzreihe/Neilsche Parabel in (1,1)/Lösung als Graph/Aufgabe -->

### Soal 25.8 (4 poin) {#br-ak-2012-w25-ex-08}

Tinjau parabola Neil

$$
C=V\left(Y^3-X^2\right)
$$

di titik $(1,1)$. Tentukan suatu parametrisasi kurva di titik ini dengan
deret pangkat sampai dengan suku kelima, sedemikian sehingga salah satu
deret pangkat tersebut merupakan polinom linear.

<!-- upstream_entity: Potenzreihenring/Eine Variable/Quotientenkörper/Formale Laurentreihen/Aufgabe -->

### Soal 25.9 (3 poin) {#br-ak-2012-w25-ex-09}

Misalkan $K$ suatu lapangan. Suatu *deret Laurent formal dengan bagian utama
berhingga* adalah jumlah tak berhingga berbentuk

$$
F=\sum_{n=k}^{\infty}a_nT^n,
\qquad a_n\in K,\quad k\in\mathbb Z.
$$

Tunjukkan bahwa gelanggang semua deret formal tersebut, dengan operasi
gelanggang yang sesuai, isomorfik dengan lapangan pecahan dari gelanggang
deret pangkat $K[[T]]$.

<!-- upstream_entity: Polynomring in einer Variablen über Körper/Komplettierung ist Potenzreihenring/Aufgabe -->

### Soal 25.10 (4 poin) {#br-ak-2012-w25-ex-10}

Misalkan $K$ suatu lapangan dan $K[T]$ gelanggang polinom dalam satu
variabel. Misalkan $R$ adalah pelokalan $K[T]$ pada ideal maksimal

$$
\mathfrak m=(T).
$$

Tunjukkan bahwa kompletasi $R$ isomorfik dengan gelanggang deret pangkat
$K[[T]]$.

<!-- upstream_entity: Potenzreihenring eine Variable/Keine Quadratwurzel aus T/Quadratwurzel aus T+2 über Z mod 7/Aufgabe -->

### Soal 25.11 (4 poin) {#br-ak-2012-w25-ex-11}

Misalkan $K$ suatu lapangan dan

$$
R=K[[T]]
$$

gelanggang deret pangkat. Tunjukkan bahwa tidak ada akar kuadrat dari $T$
di dalam $R$. Tunjukkan pula bahwa, apabila $K=\mathbb Z/(7)$, unsur $T+2$
memiliki akar kuadrat di dalam $R$, lalu tentukan lima koefisien pertama
dari salah satu akar kuadrat tersebut.

<!-- upstream_entity: Ebene integrale Kurve/Potenzreihenlösung/Lift in die Normalisierung/Aufgabe -->

### Soal 25.12 (5 poin) {#br-ak-2012-w25-ex-12}

Misalkan

$$
F\in K[X,Y]
$$

suatu polinom tak tereduksi dan

$$
R=K[X,Y]/(F)
$$

gelanggang koordinat integral dari kurva bidang

$$
C=V(F).
$$

Misalkan

$$
R\longrightarrow S=R^{\operatorname{norm}}
$$

adalah normalisasi $R$, dan misalkan

$$
R\longrightarrow K[[T]]
$$

adalah homomorfisme gelanggang yang bersesuaian dengan suatu solusi deret
pangkat formal tak konstan dari kurva tersebut. Tunjukkan bahwa terdapat tepat satu
homomorfisme gelanggang

$$
S\longrightarrow K[[T]]
$$

yang membuat diagram

$$
\begin{array}{ccc}
R & \longrightarrow & S \\
& \searrow & \downarrow \\
& & K[[T]]
\end{array}
$$

komutatif.

## Soal untuk diunggah {#br-ak-2012-w25-upload}

<!-- upstream_entity: Ebene Kurven/Tangenten und Potenzreihen/Bilder für Beispiele/Zeichne/Aufgabe -->

### Soal 25.13 (4 poin) {#br-ak-2012-w25-ex-13}

Dengan menggunakan program yang sesuai, gambarkan salah satu kurva contoh
dari kuliah beserta berbagai aproksimasi polinomial yang dihitung di sana.

> **Catatan edisi - ketidaksesuaian poin sumber.** Lembar kerja resmi
> menampilkan 4 poin untuk soal ini, sedangkan halaman tugas semantik yang
> ditransklusikan mencatat 3 poin. Edisi mempertahankan nilai 4 yang tampil
> pada lembar kerja dan mencatat nilai 3 dari halaman tugas tanpa
> menyelaraskannya secara diam-diam.
