---
title: "Lembar Kerja 21 - Gelanggang Valuasi Diskret dan Turunan Formal"
stable_id: br-ak-2025-2026-w21
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Arbeitsblatt 21"
upstream_pageid: 165940
upstream_revid: 1062605
upstream_timestamp: "2025-12-18T11:05:07Z"
upstream_mediawiki_sha1: 38a7856a5df3695eb80874194bc043dda3377f90
source_url: "https://de.wikiversity.org/w/index.php?oldid=1062605"
authority_manifest: authority/wikiversity/unit-21/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: d85444ddfc66c8e77d52db3f3abc0a186e5dd598789edaaf890b3c09cf00f923
worksheet_xml_sha256: 4989d4150db14646ebd04d3e029ff8bb2e51600fef64a00ff279d9cf48dab4b3
worksheet_expanded_tex_sha256: d49d171f1e6dea766ba1ff7bca9fce1a44ef38fff87fc3064b4071cdfb1ce9a4
exercise_map: authority/wikiversity/unit-21/ORDERED_EXERCISE_MAP.json
exercise_map_sha256: 9329621bbdd62df63f01d7298dc2a4a65a296211db131f8d8730b7d308fd5f47
license: "CC BY-SA 4.0"
translation_status: complete
---

# Lembar Kerja 21 {#br-ak-2025-2026-w21}

## Soal latihan {#br-ak-2025-2026-w21-practice}

<!-- upstream_entity: Monomiale Kurve/Lokalisiert/Kein diskreter Bewertungsring/Aufgabe -->

### Soal 21.1 {#br-ak-2025-2026-w21-ex-01}

Misalkan

$$
M\subseteq\mathbb N
$$

suatu monoid numerik yang dibangkitkan oleh pembangkit-pembangkit yang saling
prima, dan misalkan $K[M]$ gelanggang monoid $M$ di atas suatu lapangan $K$.
Tuliskan $M_+=M\setminus\{0\}$ dan misalkan

$$
R=K[M]_{\mathfrak m}
$$

pelokalan pada ideal maksimal

$$
\mathfrak m=K[M_+]
=\left\langle T^m\mathrel{\Big|}m\in M_+\right\rangle.
$$

Tunjukkan bahwa $R$ merupakan gelanggang valuasi diskret hanya dalam kasus
$M=\mathbb N$.

*Catatan koreksi sumber:* Pada penyajian terakhir untuk $\mathfrak m$, sumber
mengindeks pembangkit dengan semua $m\in M$, yang akan memasukkan
$T^0=1$ dan menghasilkan seluruh gelanggang. Indeks tersebut dikoreksi menjadi
$m\in M_+$ agar menyatakan ideal monomial positif yang dimaksud.

<!-- upstream_entity: Diskreter Bewertungsring/Ordnungsfunktion/Erste Eigenschaften/Fakt/Beweis/Aufgabe -->

### Soal 21.2 {#br-ak-2025-2026-w21-ex-02}

Misalkan $R$ suatu gelanggang valuasi diskret dengan ideal maksimal
$\mathfrak m=(p)$. Tunjukkan bahwa fungsi orde

$$
\operatorname{ord}:R\setminus\{0\}\longrightarrow\mathbb N
$$

memiliki sifat-sifat berikut.

1. Untuk setiap $f,g\in R\setminus\{0\}$,

   $$
   \operatorname{ord}(fg)
   =\operatorname{ord}(f)+\operatorname{ord}(g).
   $$

2. Untuk setiap $f,g\in R\setminus\{0\}$ dengan $f+g\ne0$,

   $$
   \operatorname{ord}(f+g)
   \geq\min\{\operatorname{ord}(f),\operatorname{ord}(g)\}.
   $$

3. Untuk setiap $f\in R\setminus\{0\}$, berlaku
   $f\in\mathfrak m$ jika dan hanya jika
   $\operatorname{ord}(f)\geq1$.
4. Untuk setiap $f\in R\setminus\{0\}$, berlaku
   $f\in R^\times$ jika dan hanya jika $\operatorname{ord}(f)=0$.

*Catatan koreksi sumber:* Syarat $f+g\ne0$ ditambahkan pada bagian 2 karena
domain fungsi $\operatorname{ord}$ yang diberikan di sini tidak memuat $0$.

<!-- upstream_entity: Diskreter Bewertungsring/Zwischenringe im Quotientenkörper/Aufgabe -->

### Soal 21.3 ★ {#br-ak-2025-2026-w21-ex-03}

Misalkan $R$ suatu gelanggang valuasi diskret dengan lapangan pecahan $Q$.
Tunjukkan bahwa tidak ada gelanggang perantara sejati antara $R$ dan $Q$.

<!-- upstream_entity: Diskreter Bewertungsring/Endlich erzeugte Untermodul im Quotientenkörper/Charakterisiere/Aufgabe -->

### Soal 21.4 {#br-ak-2025-2026-w21-ex-04}

Misalkan $R$ suatu gelanggang valuasi diskret dengan lapangan pecahan $Q$.
Karakterisasikan submodul-$R$ yang dibangkitkan secara hingga dari $Q$. Ke
bentuk apakah suatu sistem pembangkitnya dapat dibawa?

<!-- upstream_entity: Diskreter Bewertungsring/Ordnung/Fortsetzung auf Quotientenkörper/Aufgabe -->

### Soal 21.5 {#br-ak-2025-2026-w21-ex-05}

Misalkan $R$ suatu gelanggang valuasi diskret. Untuk setiap
$q\in Q(R)\setminus\{0\}$, definisikan

$$
\operatorname{ord}(q)\in\mathbb Z
$$

sedemikian sehingga definisi tersebut bertepatan dengan orde unsur-unsur $R$
dan mendefinisikan suatu homomorfisme grup

$$
Q(R)\setminus\{0\}\longrightarrow\mathbb Z.
$$

Apakah kernel homomorfisme ini?

<!-- upstream_entity: Einheitskreis/Lokalisierung/Diskreter Bewertungsring/Aufgabe -->

### Soal 21.6 {#br-ak-2025-2026-w21-ex-06}

Misalkan $K$ suatu lapangan dengan $\operatorname{char}(K)\ne2$, dan misalkan

$$
V=V(x^2+y^2-1)\subseteq\mathbb A_K^2
$$

lingkaran satuan di atas $K$. Misalkan pula $P=(a,b)\in V$ suatu titik.

1. Tunjukkan bahwa gelanggang lokal $R$ dari $V$ di titik $P$ merupakan
   gelanggang valuasi diskret.
2. Simpulkan bahwa gelanggang koordinat

   $$
   K[X,Y]/(X^2+Y^2-1)
   $$

   normal.
3. Untuk bagian ini, andaikan selain itu bahwa $-1$ bukan kuadrat di $K$.
   Tunjukkan bahwa

   $$
   K[X,Y]/(X^2+Y^2-1)
   $$

   bukan domain faktorisasi tunggal.
4. Tentukan orde $X$ dan $Y-1$ di dalam gelanggang lokal pada titik $(0,1)$.

*Catatan koreksi sumber:* Sumber tidak membatasi karakteristik dan menyatakan
gelanggang pada bagian 3 selalu tidak faktorial. Dalam karakteristik $2$,
persamaan kurva merupakan kuadrat dan gelanggang koordinatnya tidak tereduksi.
Jika $\operatorname{char}(K)\ne2$, gelanggang itu faktorial tepat ketika $-1$
merupakan kuadrat di $K$; pernyataan di atas menambahkan hipotesis minimum
yang membuat keempat bagian benar. Izin dalam sumber untuk mengandaikan $K$
tertutup secara aljabar juga dihapus karena bertentangan dengan bagian 3.

<!-- upstream_entity: Diskreter Bewertungsring/Hauptideal/Potenzen/Restklassenmodul/Aufgabe -->

### Soal 21.7 {#br-ak-2025-2026-w21-ex-07}

Misalkan $R$ suatu gelanggang valuasi diskret dengan ideal maksimal
$\mathfrak m=(\pi)$, dan misalkan $K=R/(\pi)$ lapangan residunya. Tunjukkan
bahwa untuk setiap $n\in\mathbb N$ terdapat suatu isomorfisme modul-$R$

$$
(\pi^n)/(\pi^{n+1})\longrightarrow K.
$$

<!-- upstream_entity: Bewertungstheorie/Körper mit diskreter Bewertung/Diskreter Bewertungsring/Aufgabe -->

### Soal 21.8 ★ {#br-ak-2025-2026-w21-ex-08}

Misalkan $K$ suatu lapangan dan

$$
\nu:(K^\times,\cdot,1)\longrightarrow(\mathbb Z,+,0)
$$

suatu homomorfisme grup surjektif yang memenuhi

$$
\nu(f+g)\geq\min\{\nu(f),\nu(g)\}
$$

untuk setiap $f,g\in K^\times$ dengan $f+g\ne0$. Tunjukkan bahwa

$$
R=\{f\in K^\times\mid\nu(f)\geq0\}\cup\{0\}
$$

merupakan gelanggang valuasi diskret.

*Catatan koreksi sumber:* Syarat $f+g\ne0$ ditambahkan karena $\nu$ hanya
didefinisikan pada $K^\times$.

<!-- upstream_entity: Polynomring/Verschwindungsordnung/Analogie zu Zahlbereich/Aufgabe -->

### Soal 21.9 {#br-ak-2025-2026-w21-ex-09}

Misalkan $f\in\mathbb C[X]$ dengan $f\ne0$ dan $a\in\mathbb C$. Tunjukkan
bahwa ketiga "orde" $f$ di titik $a$ berikut bertepatan.

1. Orde pelenyapan $f$ di titik $a$, yaitu orde minimum suatu turunan yang
   memenuhi

   $$
   f^{(k)}(a)\ne0.
   $$

2. Eksponen faktor linear $X-a$ dalam faktorisasi $f$ menjadi
   polinom-polinom tak tereduksi.
3. Orde $f$ di dalam pelokalan
   $\mathbb C[X]_{(X-a)}$ dari $\mathbb C[X]$ pada ideal maksimal $(X-a)$.

Soal sebelumnya dapat diperluas ke lapangan dasar lain melalui konsep
pendiferensialan formal. Misalkan $K$ suatu lapangan dan $K[X]$ gelanggang
polinomial di atas $K$. Untuk suatu polinom

$$
F=\sum_{i=0}^n a_iX^i\in K[X],
$$

polinom

$$
F'=na_nX^{n-1}+(n-1)a_{n-1}X^{n-2}+\cdots
   +3a_3X^2+2a_2X+a_1
$$

disebut **turunan formal** dari $F$.

<!-- upstream_entity: Formale Ableitung/Z mod 3/2x^7+x^6+2x^5+x^4+x^3+x^2+2/Aufgabe -->

### Soal 21.10 {#br-ak-2025-2026-w21-ex-10}

Tentukan turunan formal dari

$$
2X^7+X^6+2X^5+X^4+X^3+X^2+2
\in(\mathbb Z/(3))[X].
$$

<!-- upstream_entity: Formales Ableiten/Rechenregeln/Aufgabe -->

### Soal 21.11 {#br-ak-2025-2026-w21-ex-11}

Misalkan $K$ suatu lapangan dan $K[X]$ gelanggang polinomial di atas $K$.
Buktikan aturan-aturan perhitungan berikut untuk pendiferensialan formal
$F\mapsto F'$.

1. Turunan polinom konstan adalah $0$.
2. Operasi turunan bersifat linear atas $K$.
3. Berlaku aturan hasil kali

   $$
   (FG)'=FG'+F'G.
   $$

<!-- upstream_entity: Formales Ableiten/Mehrfache Nullstelle/Aufgabe -->

### Soal 21.12 {#br-ak-2025-2026-w21-ex-12}

Misalkan $K$ suatu lapangan, $F\in K[X]$, dan misalkan $a\in K$ sudah
merupakan akar dari $F$. Tunjukkan bahwa $a$ merupakan akar multipel dari $F$
jika dan hanya jika

$$
F'(a)=0,
$$

dengan $F'$ menyatakan turunan formal dari $F$.

*Catatan koreksi sumber:* Hipotesis $F(a)=0$ ditambahkan. Tanpanya,
$F'(a)=0$ juga dapat berlaku ketika $a$ sama sekali bukan akar $F$.

<!-- upstream_entity: Formales Ableiten/Eine Variable/Positive Charakteristik/F' ist 0/Aufgabe -->

### Soal 21.13 {#br-ak-2025-2026-w21-ex-13}

Misalkan $K$ suatu lapangan berkarakteristik positif $p>0$. Tentukan himpunan
semua polinom $F\in K[T]$ yang turunan formalnya memenuhi $F'=0$.

<!-- upstream_entity: Formales Ableiten/Potenz/Binomialbeziehung/Aufgabe -->

### Soal 21.14 {#br-ak-2025-2026-w21-ex-14}

Tunjukkan bahwa, di atas suatu lapangan $K$ berkarakteristik $0$, untuk
$i\leq n$ berlaku hubungan

$$
\frac{1}{i!}\left(X^n\right)^{(i)}
=\binom ni X^{n-i}.
$$

<!-- upstream_entity: Polynomring/1/K/Verschwindungsordnung/Aufgabe -->

### Soal 21.15 {#br-ak-2025-2026-w21-ex-15}

Misalkan $K$ suatu lapangan berkarakteristik $0$, $f\in K[X]$ dengan
$f\ne0$, dan $a\in K$. Tunjukkan bahwa ketiga "orde" $f$ di titik $a$
berikut bertepatan.

1. Orde pelenyapan $f$ di titik $a$, yaitu orde minimum suatu turunan formal
   yang memenuhi

   $$
   f^{(k)}(a)\ne0.
   $$

2. Eksponen faktor linear $X-a$ dalam faktorisasi $f$.
3. Orde $f$ di dalam pelokalan $K[X]_{(X-a)}$ dari $K[X]$ pada ideal
   maksimal $(X-a)$.

Untuk soal-soal berikut, gunakan definisi ini. Misalkan $R$ suatu gelanggang
komutatif, $\mathfrak a\subseteq R$ suatu ideal, dan $U\subseteq V$ suatu
submodul dari modul-$R$ $V$. Dengan $\mathfrak aU$ kita maksud submodul yang
dibangkitkan oleh semua hasil kali

$$
fv\quad\text{dengan }f\in\mathfrak a\text{ dan }v\in U.
$$

<!-- upstream_entity: Modul/Ideal/Produkt/Verträglich/Aufgabe -->

### Soal 21.16 {#br-ak-2025-2026-w21-ex-16}

Misalkan $\mathfrak a,\mathfrak b\subseteq R$ ideal-ideal dalam suatu
gelanggang komutatif. Tunjukkan bahwa hasil kali ideal
$\mathfrak a\mathfrak b$ bertepatan dengan hasil kali $\mathfrak a\mathfrak b$
yang dibentuk dari ideal $\mathfrak a$ dan submodul-$R$
$\mathfrak b\subseteq R$ menurut definisi di atas.

<!-- upstream_entity: Modul/Ideal/Produkt/Assoziativität/Aufgabe -->

### Soal 21.17 {#br-ak-2025-2026-w21-ex-17}

Misalkan $\mathfrak a,\mathfrak b\subseteq R$ ideal-ideal dalam suatu
gelanggang komutatif dan $U\subseteq V$ suatu submodul dari modul-$R$ $V$.
Tunjukkan bahwa

$$
(\mathfrak a\cdot\mathfrak b)\cdot U
=\mathfrak a\cdot(\mathfrak b\cdot U).
$$

<!-- upstream_entity: Modul/Ideal/Produkt/Distributivität im Ideal/Aufgabe -->

### Soal 21.18 {#br-ak-2025-2026-w21-ex-18}

Misalkan $\mathfrak a,\mathfrak b\subseteq R$ ideal-ideal dalam suatu
gelanggang komutatif dan $U\subseteq V$ suatu submodul dari modul-$R$ $V$.
Tunjukkan bahwa

$$
(\mathfrak a+\mathfrak b)\cdot U
=\mathfrak a\cdot U+\mathfrak b\cdot U.
$$

<!-- upstream_entity: Modul/Ideal/Produkt/Distributivität im Untermodul/Aufgabe -->

### Soal 21.19 {#br-ak-2025-2026-w21-ex-19}

Misalkan $\mathfrak a\subseteq R$ suatu ideal dalam gelanggang komutatif dan
$U,W\subseteq V$ submodul-submodul dari modul-$R$ $V$. Tunjukkan bahwa

$$
\mathfrak a\cdot(U+W)=\mathfrak a\cdot U+\mathfrak a\cdot W.
$$

<!-- upstream_entity: Lokaler Ring/Nakayama/Maximales Ideal/Potenzen/Aufgabe -->

### Soal 21.20 {#br-ak-2025-2026-w21-ex-20}

Misalkan $(R,\mathfrak m)$ suatu gelanggang lokal Noether dan
$n\in\mathbb N$. Tunjukkan bahwa

$$
\mathfrak m^{n+1}=\mathfrak m^n
$$

menyiratkan

$$
\mathfrak m^n=0.
$$

*Catatan koreksi sumber:* Kuantifikasi $n\in\mathbb N$ ditambahkan secara
eksplisit; sumber menggunakan $n$ tanpa memperkenalkannya.

<!-- upstream_entity: Lokaler Ring/Quotientenkörper/Nakayama/Aufgabe -->

### Soal 21.21 {#br-ak-2025-2026-w21-ex-21}

Misalkan $(R,\mathfrak m)$ suatu domain integral lokal yang bukan lapangan,
dan misalkan $Q$ lapangan pecahan $R$. Tunjukkan bahwa

$$
\mathfrak mQ=Q.
$$

## Soal untuk dikumpulkan {#br-ak-2025-2026-w21-submit}

<!-- upstream_entity: Diskreter Bewertungsring/In K(T)/Schnitt mit K T ist K/Aufgabe -->

### Soal 21.22 (4 poin) {#br-ak-2025-2026-w21-ex-22}

Misalkan $K$ suatu lapangan dan $K(T)$ lapangan fungsi rasional di atas $K$.
Carilah suatu gelanggang valuasi diskret

$$
R\subseteq K(T)
$$

yang memenuhi

$$
Q(R)=K(T)
\qquad\text{dan}\qquad
R\cap K[T]=K.
$$

<!-- upstream_entity: Diskreter Bewertungsring/Potenzreihenring in einer Variablen/Grundlegender Nachweis/Aufgabe -->

### Soal 21.23 (4 poin) {#br-ak-2025-2026-w21-ex-23}

Misalkan $K$ suatu lapangan. Suatu **deret pangkat dalam satu variabel** di
atas $K$ adalah suatu ekspresi formal berbentuk

$$
a_0+a_1T+a_2T^2+a_3T^3+\cdots,
\qquad a_i\in K.
$$

Jadi, di sini dapat terdapat tak hingga banyak koefisien $a_i$ yang tidak
nol. Definisikan struktur gelanggang pada himpunan semua deret pangkat yang
memperluas struktur gelanggang pada gelanggang polinomial dalam satu variabel.
Tunjukkan bahwa gelanggang ini merupakan gelanggang valuasi diskret.

<!-- upstream_entity: Noetherscher Integritätsbereich/Totale Teilbarkeitsbeziehung/Ist diskreter Bewertungsring/Aufgabe -->

### Soal 21.24 (4 poin) {#br-ak-2025-2026-w21-ex-24}

Misalkan $R$ suatu domain integral dengan sifat berikut: untuk setiap dua
unsur $f,g\in R$, salah satu dari $f$ membagi $g$ atau $g$ membagi $f$.
Andaikan $R$ Noether, tetapi bukan lapangan. Tunjukkan bahwa $R$ merupakan
gelanggang valuasi diskret.

<!-- upstream_entity: Monoidringe/Idealerzeuger für Neilsche Parabel/Aufgabe -->

### Soal 21.25 (3 poin) {#br-ak-2025-2026-w21-ex-25}

Tunjukkan bahwa setiap ideal dalam

$$
K[X,Y]_{(X,Y)}/(X^2-Y^3)
$$

dapat dibangkitkan oleh paling banyak dua unsur.

<!-- upstream_entity: Monoidringe/Ebene monomiale Kurve/Beispiel für Ideal mit mehr als zwei Erzeugern/Aufgabe -->

### Soal 21.26 (3 poin) {#br-ak-2025-2026-w21-ex-26}

Berikan contoh suatu kurva monomial bidang dan suatu ideal dalam gelanggang
lokal terkait pada singularitasnya yang tidak dapat dibangkitkan oleh dua
unsur.

---

**Provenans edisi.** Terjemahan dan produksi pembaca: OpenAI Codex
gpt-5.6-sol, Ultra. Sumber, pengarang, dan lisensi komponen dipertahankan
seperti dinyatakan dalam metadata dan berkas hak edisi.
