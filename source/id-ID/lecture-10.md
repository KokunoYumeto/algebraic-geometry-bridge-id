---
title: "Kuliah 10 - Modul Noether dan Nullstellensatz Hilbert"
stable_id: br-ak-2025-2026-l10
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 10"
upstream_pageid: 165899
upstream_revid: 1051326
upstream_timestamp: "2025-08-18T07:56:09Z"
upstream_mediawiki_sha1: 2635c363f022af1e0603447bbac65bfe71e87a46
source_url: "https://de.wikiversity.org/w/index.php?oldid=1051326"
authority_manifest: authority/wikiversity/unit-10/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: f8b4f8bf12a0613f774352df31941d79a35d9eed10f2d8fb5570f9ffe07bfb43
lecture_xml_sha256: 05e042175d3a11fe60926739c4b4fa4d4f092a6b086c2ce6e6b5f2031087f2c9
lecture_expanded_tex_sha256: db404d16cbcaee5bc0cdd879ab39d288ea7696d9c1de1915090669c794ae5263
license: "CC BY-SA 4.0"
translation_status: complete
---

# Kuliah 10: Modul Noether dan Nullstellensatz Hilbert {#br-ak-2025-2026-l10}

## Modul Noether {#br-ak-2025-2026-l10-s01}

Kita hendak menunjukkan bahwa, untuk gelanggang Noether $R$ dan modul-$R$
yang dibangkitkan secara hingga, setiap submodul-$R$ kembali dibangkitkan
secara hingga. Modul dengan sifat ini disebut Noether.

<!-- upstream_entity: Modultheorie (kommutative Algebra)/Noetherscher Modul/Definition -->

### Definisi: modul Noether {#br-ak-2025-2026-l10-def-01}

Misalkan $R$ suatu gelanggang komutatif dan $M$ suatu modul-$R$. Modul $M$
disebut *Noether* jika setiap submodul-$R$ dari $M$ dibangkitkan secara
hingga.

Untuk $M=R$, definisi ini sama dengan definisi gelanggang Noether, sebab
submodul-$R$ dari $R$ tepat merupakan ideal-idealnya.

Dalam pernyataan-pernyataan berikut, kita menggunakan istilah dan notasi
berikut.

<!-- upstream_entity: Modultheorie (kommutative Algebra)/Kurze exakte Sequenz/Definition -->

### Definisi: barisan eksak pendek {#br-ak-2025-2026-l10-def-02}

Misalkan $R$ suatu gelanggang komutatif dan $M_1,M_2,M_3$ modul-$R$. Diagram
berbentuk

$$
0\longrightarrow M_1\longrightarrow M_2\longrightarrow M_3\longrightarrow0
$$

disebut *barisan eksak pendek* modul-$R$ jika $M_1$ merupakan submodul-$R$
dari $M_2$ dan $M_3$ merupakan modul faktor dari $M_2$ yang isomorfik dengan
$M_2/M_1$.

Keeksakan berarti bahwa pada setiap posisi berlaku

$$
\operatorname{ker}\varphi_{i+1}=\operatorname{im}\varphi_i,
$$

dengan $\varphi_i$ menyatakan homomorfisme-homomorfisme modul-$R$ dalam
barisan tersebut.

<!-- upstream_entity: Modultheorie (kommutative Algebra)/Noethersche Moduln/Kurze exakte Sequenz/Äquivalentes Kriterium/Fakt -->

### Lema: sifat Noether dalam barisan eksak pendek {#br-ak-2025-2026-l10-lem-01}

Misalkan $R$ suatu gelanggang komutatif dan

$$
0\longrightarrow M_1\longrightarrow M\longrightarrow M_3\longrightarrow0
$$

suatu barisan eksak pendek modul-$R$. Maka $M$ Noether tepat ketika $M_1$
dan $M_3$ keduanya Noether.

#### Bukti {#br-ak-2025-2026-l10-lem-01-proof}

Pertama, misalkan $M$ Noether dan $U\subseteq M_1$ suatu submodul. Karena
$U$ juga langsung merupakan submodul dari $M$, menurut asumsi ia dibangkitkan
secara hingga. Sekarang misalkan $V\subseteq M_3$ suatu submodul dari modul
faktor tersebut. Misalkan $\widetilde V$ adalah prapeta $V$ di $M$ terhadap
pemetaan faktor. Menurut asumsi, $\widetilde V$ dibangkitkan secara hingga,
dan citra dari suatu sistem pembangkitnya juga membangkitkan modul citra $V$.

Sebaliknya, misalkan kedua modul luar $M_1$ dan $M_3$ Noether, serta
$U\subseteq M$ suatu submodul. Misalkan $U_3\subseteq M_3$ adalah submodul
citra dari $U$. Modul $U_3$ dibangkitkan oleh hingga banyak unsur
$s_1,\ldots,s_n$, dan kita dapat menganggap bahwa

$$
s_i=\overline r_i
$$

merupakan citra unsur-unsur $r_i\in U$. Tinjau $U\cap M_1$. Ini merupakan
submodul dari $M_1$, sehingga dibangkitkan secara hingga, katakanlah oleh
$t_1,\ldots,t_k$, yang kita pandang sebagai unsur-unsur $U$. Kita klaim bahwa

$$
r_1,\ldots,r_n,t_1,\ldots,t_k
$$

membentuk sistem pembangkit untuk $U$. Ambil sembarang $m\in U$. Maka

$$
\overline m=\sum_{i=1}^n a_i s_i.
$$

Karena itu unsur $m-\sum_{i=1}^n a_i r_i$ dipetakan ke $0$ di sebelah kanan.
Unsur tersebut berada dalam kernel pemetaan faktor, jadi berada dalam $M_1$.
Di sisi lain, unsur ini juga berada dalam $U$, sehingga berada dalam irisan
$M_1\cap U$, yang dibangkitkan oleh $t_1,\ldots,t_k$. Jadi kita dapat menulis

$$
m-\sum_{i=1}^n a_i r_i=\sum_{j=1}^k b_jt_j,
$$

atau, secara ekuivalen,

$$
m=\sum_{i=1}^n a_i r_i+\sum_{j=1}^k b_jt_j.
$$

<!-- upstream_entity: Kommutative Ringtheorie/Noethersche Ringe/Endlich erzeugte Moduln sind noethersch/Fakt -->

### Teorema: modul hingga atas gelanggang Noether {#br-ak-2025-2026-l10-thm-01}

Misalkan $R$ suatu gelanggang komutatif Noether dan $M$ suatu modul-$R$ yang
dibangkitkan secara hingga. Maka $M$ merupakan modul Noether.

#### Bukti {#br-ak-2025-2026-l10-thm-01-proof}

Kita membuktikan pernyataan ini dengan induksi pada banyaknya $n$ pembangkit
modul $M$. Untuk $n=0$, kita memperoleh modul nol. Misalkan $n=1$. Maka ada
pemetaan surjektif

$$
R\longrightarrow M\cong R/\mathfrak a.
$$

Menurut Lema 10.3, modul faktor dari modul Noether kembali Noether. Karena
gelanggang $R$ sendiri Noether menurut asumsi, $M$ juga Noether.

Sekarang misalkan $n\geq2$ dan pernyataan telah terbukti untuk nilai yang
lebih kecil. Misalkan $m_1,\ldots,m_n$ suatu sistem pembangkit $M$. Nyatakan
dengan $M_1$ submodul-$R$ yang dibangkitkan oleh
$m_1,\ldots,m_{n-1}$. Submodul ini memberikan barisan eksak pendek

$$
0\longrightarrow M_1\longrightarrow M
\longrightarrow M/M_1=:M_3\longrightarrow0.
$$

Modul di sebelah kiri dibangkitkan oleh $n-1$ unsur dan Noether menurut
hipotesis induksi. Modul di sebelah kanan dibangkitkan oleh kelas residu
$m_n$, jadi oleh satu unsur, dan karena itu juga Noether. Menurut Lema 10.3,
$M$ pun Noether.

## Nullstellensatz Hilbert — versi aljabar {#br-ak-2025-2026-l10-s02}

Untuk suatu aljabar-$R$ $A$, istilah *hingga* dan *dibangkitkan secara
hingga* akan sama-sama penting. Istilah pertama berarti bahwa $A$, jika
dipandang sebagai modul-$R$, dibangkitkan secara hingga; istilah kedua berarti
bahwa $A$ dibangkitkan secara hingga sebagai aljabar. Gelanggang polinomial
$R[X_1,\ldots,X_n]$ dibangkitkan secara hingga dalam arti kedua: variabel-
variabelnya membentuk sistem pembangkit aljabar berhingga. Namun, gelanggang
polinomial itu tidak dibangkitkan secara hingga sebagai modul; sistem
pembangkit modul yang paling sederhana terdiri atas semua monomial.

Kita hendak membuktikan versi aljabar dari Nullstellensatz Hilbert. Untuk itu
kita memerlukan dua lema berikut.

<!-- upstream_entity: Endlich erzeugte kommutative Algebren/R noethersch/A über R endlich erzeugt/A endlich über B/B ist endlich erzeugt/Fakt -->

### Lema: subaljabar di bawah perluasan hingga {#br-ak-2025-2026-l10-lem-02}

Misalkan $R$ suatu gelanggang komutatif Noether dan $A$ suatu aljabar-$R$
yang dibangkitkan secara hingga. Misalkan $B\subseteq A$ suatu subaljabar-$R$
sedemikian sehingga $A$ hingga di atas $B$ (sebagai modul-$B$). Maka $B$ juga
merupakan aljabar-$R$ yang dibangkitkan secara hingga.

#### Bukti {#br-ak-2025-2026-l10-lem-02-proof}

Kita tulis

$$
A=R[x_1,\ldots,x_n]
$$

dan

$$
A=Ba_1+\cdots+Ba_m,
$$

dengan $a_i\in A$. Tetapkan

$$
x_i=\sum_{j=1}^m b_{ij}a_j
\qquad\text{dan}\qquad
a_i a_j=\sum_{k=1}^m b_{ijk}a_k,
$$

dengan koefisien $b_{ij},b_{ijk}\in B$. Tinjau subaljabar-$R$ $S$ dari $B$
yang dibangkitkan oleh koefisien-koefisien tersebut dan submodul-$S$

$$
\widetilde A=Sa_1+\cdots+Sa_m\subseteq A.
$$

Hasil kali $a_i a_j$ kembali berada dalam modul ini, sehingga
$\widetilde A$ bahkan merupakan aljabar-$S$. Karena semua $x_i$ juga berada
dalam $\widetilde A$, kita memperoleh $A=\widetilde A$. Ini berarti bahwa
$A$ adalah modul-$S$ hingga. Menurut Korolari 9.9, $S$ merupakan gelanggang
Noether; menurut Teorema 10.4, submodul-$S$

$$
B\subseteq A
$$

juga merupakan modul-$S$ hingga. Rantai

$$
R\subseteq S\subseteq B
$$

akhirnya menunjukkan bahwa $B$ adalah aljabar-$R$ yang dibangkitkan secara
hingga.

<!-- upstream_entity: Endlich erzeugte kommutative Algebren/Rationaler Funktionenkörper ist nicht endlich erzeugt/Fakt -->

### Lema: lapangan fungsi rasional tidak dibangkitkan secara hingga {#br-ak-2025-2026-l10-lem-03}

Misalkan $K$ suatu lapangan dan $R=K(X)$ lapangan fungsi rasional yang
bersesuaian. Maka $R$ bukan aljabar-$K$ yang dibangkitkan secara hingga.

#### Bukti {#br-ak-2025-2026-l10-lem-03-proof}

Andaikan fungsi-fungsi rasional

$$
F_i=\frac{P_i}{Q_i},\qquad i=1,\ldots,n,
$$

dengan $P_i,Q_i\in K[X]$ dan $Q_i\ne0$, membentuk suatu sistem pembangkit
berhingga bagi $K(X)$. Dengan beralih ke penyebut bersama, kita dapat
menganggap semua penyebutnya sama, yakni $Q_i=Q$. Jadi asumsi tersebut
khususnya mengatakan bahwa lapangan fungsi rasional dapat diperoleh dengan
melokalkan pada satu unsur saja. Karena $Q$ bukan konstanta (jika tidak,
$K[X]=K(X)$, yang tidak benar), kita mempunyai $Q-1\ne0$, sehingga

$$
\frac1{Q-1}\in K(X).
$$

Maka terdapat representasi

$$
\frac1{Q-1}=\frac{P}{Q^s}
$$

untuk suatu $s$ yang sesuai. Akibatnya,

$$
Q^s=(Q-1)P.
$$

Karena $Q^s$ dan $Q-1$ membangkitkan ideal satuan dalam $K[X]$, kesamaan ini
menyiratkan bahwa $Q-1$ sendiri sudah membangkitkan ideal satuan, jadi
$Q-1$ merupakan satuan. Namun, itu berarti $Q$ adalah konstanta, suatu
kontradiksi.

Pernyataan berikut merupakan versi aljabar dari Nullstellensatz Hilbert.

<!-- upstream_entity: Hilbertscher Nullstellensatz (algebraisch)/Endlich erzeugte Körpererweiterung ist endlich/Fakt -->

### Teorema: Nullstellensatz Hilbert, versi aljabar {#br-ak-2025-2026-l10-thm-02}

Misalkan $K$ suatu lapangan dan $K\subseteq L$ suatu perluasan lapangan yang
dibangkitkan secara hingga sebagai aljabar-$K$. Maka $L$ hingga di atas $K$.

#### Bukti {#br-ak-2025-2026-l10-thm-02-proof}

Tetapkan

$$
L=K[x_1,\ldots,x_n].
$$

Misalkan $K_i$ adalah lapangan pecahan dari $K[x_1,\ldots,x_i]$ di dalam
$L$. Dengan demikian kita mempunyai rantai lapangan

$$
K=K_0\subseteq K_1\subseteq\cdots\subseteq K_n=L.
$$

Kita hendak menunjukkan bahwa $L$ hingga di atas $K$. Menurut Teorema 2.8
dari kuliah Teori Lapangan dan Galois (Osnabrück 2018–2019), cukup ditunjukkan
bahwa setiap tahap dalam rantai lapangan tersebut hingga. Andaikan
$K_i\subseteq K_{i+1}$ tidak hingga, tetapi semua tahap sesudahnya hingga.
Terapkan Lema 10.5 pada

$$
K\subseteq K_{i+1}\subset L.
$$

Kita memperoleh bahwa $K_{i+1}$ dibangkitkan secara hingga di atas $K$.
Secara khusus, $K_{i+1}$ juga dibangkitkan secara hingga di atas $K_i$.
Di sisi lain, $K_{i+1}$ merupakan lapangan pecahan dari
$K_i[x_{i+1}]$. Jadi kita mempunyai rantai

$$
K_i\subseteq K_i[x_{i+1}]
\subseteq Q\bigl(K_i[x_{i+1}]\bigr)=K_{i+1},
$$

di mana $K_{i+1}$ dibangkitkan secara hingga di atas $K_i$, tetapi tidak
hingga. Seandainya $x_{i+1}$ aljabar atas $K_i$, maka ia juga hingga, dan
menurut Soal 10.1, $K_i[x_{i+1}]$ sudah merupakan lapangan. Seluruh rantai
terakhir itu lantas hingga, bertentangan dengan pemilihan $i$. Jadi
$x_{i+1}$ transenden atas $K_i$. Namun, $K_i[x_{i+1}]$ kemudian isomorfik
dengan gelanggang polinomial dalam satu variabel, dan
$Q(K_i[x_{i+1}])$ isomorfik dengan lapangan fungsi rasional di atas $K_i$.
Menurut Lema 10.6, lapangan ini tidak dibangkitkan secara hingga, sekali lagi
suatu kontradiksi.

<!-- upstream_entity: Algebren von endlichem Typ über Körper/Homomorphismen/Urbild von maximalem Ideal ist maximal/Fakt -->

### Teorema: prapeta ideal maksimal {#br-ak-2025-2026-l10-thm-03}

Misalkan $K$ suatu lapangan dan $A,B$ dua aljabar-$K$ bertipe hingga.
Misalkan

$$
\varphi:A\longrightarrow B
$$

suatu homomorfisme aljabar-$K$. Maka, untuk setiap ideal maksimal
$\mathfrak m$ di $B$, prapetanya $\varphi^{-1}(\mathfrak m)$ juga merupakan
ideal maksimal.

#### Bukti {#br-ak-2025-2026-l10-thm-03-proof}

Misalkan $\mathfrak m$ suatu ideal maksimal di $B$. Dari Soal 4.19 kita tahu
bahwa prapeta ideal prima di bawah setiap homomorfisme gelanggang kembali
prima. Jadi $\varphi^{-1}(\mathfrak m)$ mula-mula merupakan ideal prima;
sebut ideal ini $\mathfrak p$. Kita memperoleh homomorfisme gelanggang
terinduksi

$$
K\longrightarrow A/\mathfrak p\longrightarrow B/\mathfrak m=L,
$$

di mana $L$ merupakan lapangan dan kedua homomorfisme bersifat injektif serta
bertipe hingga. Karena pemetaan komposit bertipe hingga dan $K,L$ keduanya
lapangan, Teorema 10.7 menyatakan bahwa pemetaan tersebut hingga. Kita hendak
menunjukkan bahwa gelanggang antara $A/\mathfrak p$ merupakan lapangan. Hal
ini mengikuti dari Soal 10.2.

<!-- upstream_entity: Algebren von endlichem Typ über Körper/Radikal ist Durchschnitt von maximalen Idealen/Fakt -->

### Teorema: radikal sebagai irisan ideal maksimal {#br-ak-2025-2026-l10-thm-04}

Misalkan $K$ suatu lapangan dan $A$ suatu aljabar-$K$ bertipe hingga. Maka
setiap ideal radikal dalam $A$ merupakan irisan ideal-ideal maksimal.

#### Bukti {#br-ak-2025-2026-l10-thm-04-proof}

Menurut Soal 10.17, setiap ideal radikal merupakan irisan ideal-ideal prima.
Karena itu cukup ditunjukkan bahwa setiap ideal prima dalam aljabar yang
dibangkitkan secara hingga merupakan irisan ideal-ideal maksimal. Misalkan
$\mathfrak p$ suatu ideal prima dan $f\notin\mathfrak p$. Ideal
$\mathfrak p$ tetap merupakan ideal prima di dalam pelokalan

$$
B:=A_f.
$$

Di $A_f$ terdapat ideal maksimal $\mathfrak m\subset A_f$ yang memuat
$\mathfrak pA_f$. Pandang $A_f$ sebagai aljabar-$K$ yang dibangkitkan secara
hingga dan tinjau

$$
\varphi:A\longrightarrow A_f.
$$

Kita mempunyai

$$
\mathfrak p\subseteq\varphi^{-1}(\mathfrak m)
\qquad\text{dan}\qquad
f\notin\varphi^{-1}(\mathfrak m).
$$

Menurut Teorema 10.8, $\varphi^{-1}(\mathfrak m)$ maksimal.

<!-- upstream_entity: Algebren von endlichem Typ über Körper/Algebraisch abgeschlossen/Maximale Ideale sind Punktideal/Fakt -->

### Teorema: ideal maksimal adalah ideal titik {#br-ak-2025-2026-l10-thm-05}

Misalkan $K$ suatu lapangan yang tertutup secara aljabar dan $A$ suatu
aljabar-$K$ yang dibangkitkan secara hingga. Maka setiap lapangan residu dari
$A$ isomorfik dengan $K$. Dengan kata lain, setiap ideal maksimal di $A$
merupakan ideal titik.

#### Bukti {#br-ak-2025-2026-l10-thm-05-proof}

Misalkan $\mathfrak m$ suatu ideal maksimal dari aljabar-$K$ yang
dibangkitkan secara hingga $A$, dan tinjau

$$
K\longrightarrow A\longrightarrow A/\mathfrak m=:L.
$$

Di sini $L$ merupakan lapangan dan sekaligus aljabar-$K$ yang dibangkitkan
secara hingga. Menurut Teorema 10.7, $L$ harus merupakan aljabar-$K$ hingga.
Karena $K$ tertutup secara aljabar, harus berlaku $K=L$.
