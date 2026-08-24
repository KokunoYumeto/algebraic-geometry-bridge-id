---
title: "Kuliah 11 - Nullstellensatz Hilbert dan Gelanggang Koordinat"
stable_id: br-ak-2025-2026-l11
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 11"
upstream_pageid: 165900
upstream_revid: 1051329
upstream_timestamp: "2025-08-18T07:58:01Z"
upstream_mediawiki_sha1: 33f81e0bf65b5b23de1c5798adf4a93282354d82
source_url: "https://de.wikiversity.org/w/index.php?oldid=1051329"
authority_manifest: authority/wikiversity/unit-11/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: ea2d4936bb27e88b2863f8fecbddd5570992c432aee66c72066597709da65a47
lecture_xml_sha256: b449e7c7370ea9e057046ca2a3b203cd8f66ef72da94f604e321c37b0e14481a
lecture_expanded_tex_sha256: 4bb7299a66d59560540d764f4ea6449bf4b4e19e230957748d66b421fea7857d
license: "CC BY-SA 4.0 for translated course text; media retain component rights in authority/RIGHTS-unit-11.csv"
translation_status: complete
---

# Kuliah 11: Nullstellensatz Hilbert dan Gelanggang Koordinat {#br-ak-2025-2026-l11}

## Nullstellensatz Hilbert - versi geometris {#br-ak-2025-2026-l11-s01}

Sekarang kita akan membuktikan versi geometris Nullstellensatz Hilbert. Untuk
lapangan yang tertutup secara aljabar, teorema ini memberikan hubungan tunggal
antara himpunan aljabar afin dalam ruang afin
$\mathbb A_K^n$ dan ideal-ideal radikal dalam gelanggang polinomial.

<!-- upstream_entity: Affiner Raum/Hilbertscher Nullstellensatz (geometrisch)/Algebraisch abgeschlossen/Fakt -->

### Teorema: Nullstellensatz Hilbert geometris {#br-ak-2025-2026-l11-thm-01}

Misalkan $K$ lapangan yang tertutup secara aljabar dan

$$
V=V(\mathfrak a)\subseteq\mathbb A_K^n
$$

suatu himpunan aljabar afin yang dideskripsikan oleh ideal $\mathfrak a$.
Misalkan

$$
F\in K[X_1,\ldots,X_n]
$$

suatu polinom yang lenyap pada $V$. Maka $F$ termasuk dalam radikal
$\mathfrak a$; artinya, terdapat $r\in\mathbb N$ dengan

$$
F^r\in\mathfrak a.
$$

#### Bukti {#br-ak-2025-2026-l11-thm-01-proof}

Andaikan $F$ tidak termasuk dalam radikal $\mathfrak a$. Menurut Teorema 10.9,
terdapat ideal maksimal

$$
\mathfrak m\subset K[X_1,\ldots,X_n]
$$

dengan $\mathfrak a\subseteq\mathfrak m$ dan $F\notin\mathfrak m$. Menurut
Teorema 10.10,

$$
K[X_1,\ldots,X_n]/\mathfrak m=K,
$$

sehingga

$$
\mathfrak m=(X_1-a_1,\ldots,X_n-a_n)
$$

untuk beberapa $a_1,\ldots,a_n\in K$. Sifat $F\notin\mathfrak m$ berarti
bahwa $F$ tidak sama dengan nol dalam lapangan residu yang bersesuaian, yakni

$$
F(a_1,\ldots,a_n)\ne0.
$$

Namun, karena $\mathfrak a\subseteq\mathfrak m$, titik
$(a_1,\ldots,a_n)$ berada dalam $V$. Menurut asumsi, $F$ harus lenyap di titik
itu. Ini suatu kontradiksi.

<!-- upstream_entity: Affiner Raum/Algebraisch abgeschlossen/Korrespondenz zwischen affin algebraischen Mengen und Radikalen/Fakt -->

### Teorema: korespondensi himpunan aljabar dan ideal radikal {#br-ak-2025-2026-l11-thm-02}

Misalkan $K$ lapangan yang tertutup secara aljabar, dengan gelanggang
polinomial $K[X_1,\ldots,X_n]$ dan ruang afin $\mathbb A_K^n$. Terdapat
korespondensi alami antara himpunan-himpunan aljabar afin dalam
$\mathbb A_K^n$ dan ideal-ideal radikal dalam $K[X_1,\ldots,X_n]$.

Dalam korespondensi ini, ideal radikal dipetakan ke lokus nolnya, sedangkan
himpunan aljabar afin dipetakan ke ideal pelenyapannya.

#### Bukti {#br-ak-2025-2026-l11-thm-02-proof}

Misalkan $V\subseteq\mathbb A_K^n$ aljabar afin. Menurut bagian (3) Lema 3.8,

$$
V=V(\operatorname{Id}(V)).
$$

Untuk suatu ideal radikal $I\subseteq K[X_1,\ldots,X_n]$, bagian (2) lema
yang sama memberikan inklusi

$$
I\subseteq\operatorname{Id}(V(I)).
$$

Inklusi sebaliknya,

$$
\operatorname{Id}(V(I))\subseteq I,
$$

merupakan isi Nullstellensatz Hilbert.

<!-- upstream_entity: Affiner Raum/Algebraisch abgeschlossener Körper/D(f i) überdeckt/Erzeugt Einheitsideal/Fakt -->

### Korolari: penutup oleh himpunan terbuka utama {#br-ak-2025-2026-l11-cor-01}

Misalkan $K$ lapangan yang tertutup secara aljabar dan

$$
F_i\in K[X_1,\ldots,X_n],\qquad i\in I,
$$

polinom-polinom sedemikian sehingga

$$
\mathbb A_K^n=\bigcup_{i\in I}D(F_i).
$$

Maka semua $F_i$ membangkitkan ideal satuan dalam
$K[X_1,\ldots,X_n]$.

#### Bukti {#br-ak-2025-2026-l11-cor-01-proof}

Misalkan $\mathfrak b$ ideal yang dibangkitkan oleh semua $F_i$. Asumsi
menyatakan bahwa

$$
\bigcap_{i\in I}V(F_i)=V(\mathfrak b)
$$

kosong. Dengan demikian, $V(\mathfrak b)\subseteq V(1)$. Menurut
Nullstellensatz Hilbert, suatu pangkat dari $1$, jadi $1$ sendiri, termasuk
dalam $\mathfrak b$. Maka $\mathfrak b$ adalah ideal satuan.

<!-- upstream_entity: Affine Varietäten/Algebraisch abgeschlossener Körper/Verschwindungsideal vom Durchschnitt/Fakt -->

### Korolari: ideal pelenyapan suatu irisan {#br-ak-2025-2026-l11-cor-02}

Misalkan $K$ lapangan yang tertutup secara aljabar dan $V_1,V_2$ dua himpunan
aljabar afin dalam $\mathbb A_K^n$. Maka

$$
\operatorname{Id}(V_1\cap V_2)
=\operatorname{rad}\!\left(\operatorname{Id}(V_1)+
\operatorname{Id}(V_2)\right).
$$

#### Bukti {#br-ak-2025-2026-l11-cor-02-proof}

Misalkan

$$
\mathfrak a_1=\operatorname{Id}(V_1),\qquad
\mathfrak a_2=\operatorname{Id}(V_2).
$$

Pernyataan itu mengikuti dari

$$
\begin{aligned}
\operatorname{rad}(\mathfrak a_1+\mathfrak a_2)
&=\operatorname{Id}\!\left(V(\operatorname{rad}(\mathfrak a_1+
\mathfrak a_2))\right)\\
&=\operatorname{Id}(V(\mathfrak a_1+\mathfrak a_2))\\
&=\operatorname{Id}(V(\mathfrak a_1)\cap V(\mathfrak a_2)),
\end{aligned}
$$

dengan kesamaan pertama berasal dari Teorema 11.1.

Sifat-sifat ini juga tidak berlaku tanpa asumsi bahwa lapangan tertutup secara
aljabar, sebagaimana ditunjukkan oleh contoh berikut.

![Dua elips yang tidak berpotongan](authority/assets/Disjoint_ellipses.png)

*Dua elips yang tidak berpotongan; Pmidden, dibuat dengan Mathematica; domain
publik.*

<!-- upstream_entity: Ebene algebraische Kurven/Reell/X^2+Y^2-2 und X^2+2Y^2-1/Durchschnitt und Einheit/Beispiel -->

### Contoh: dua kuadrik real yang tidak berpotongan {#br-ak-2025-2026-l11-ex-01}

Kita tinjau dua kurva aljabar

$$
V_1=V(X^2+Y^2-2),\qquad
V_2=V(X^2+2Y^2-1)\subseteq\mathbb A_K^2.
$$

Untuk $K=\mathbb R$, keduanya merupakan kuadrik tak tereduksi. Irisannya
dideskripsikan oleh ideal

$$
(X^2+Y^2-2,X^2+2Y^2-1)=(Y^2+1,X^2-3).
$$

Karena polinom $Y^2+1$ tidak memiliki akar real,

$$
V_1\cap V_2=\varnothing.
$$

Ideal pelenyapan irisan yang kosong tentu merupakan ideal satuan, sedangkan
jumlah kedua ideal pelenyapan tersebut bukan ideal satuan.

## Gelanggang koordinat suatu himpunan aljabar afin {#br-ak-2025-2026-l11-s02}

Misalkan $V\subseteq\mathbb A_K^n$ suatu himpunan aljabar afin dengan ideal
pelenyapan $\operatorname{Id}(V)$. Setiap polinom

$$
F\in K[X_1,\ldots,X_n]
$$

mendefinisikan fungsi pada ruang afin, dan dengan demikian menginduksi fungsi
pada subhimpunan $V$:

$$
\begin{matrix}
\mathbb A_K^n&\xrightarrow{F}&K\\
\uparrow&\nearrow&\\
V&&
\end{matrix}
$$

Menurut Definisi 3.4, unsur ideal pelenyapan menginduksi fungsi nol pada $V$.
Dua polinom $G,H\in K[X_1,\ldots,X_n]$ yang selisihnya termasuk dalam ideal
pelenyapan menginduksi fungsi yang sama pada $V$. Oleh karena itu, wajar untuk
memandang gelanggang faktor

$$
K[X_1,\ldots,X_n]/\operatorname{Id}(V)
$$

sebagai gelanggang fungsi polinomial (atau fungsi aljabar) pada $V$.

<!-- upstream_entity: Affine-algebraische Mengen/Koordinatenring/Definition -->

### Definisi: gelanggang koordinat {#br-ak-2025-2026-l11-def-01}

Untuk suatu himpunan aljabar afin

$$
V\subseteq\mathbb A_K^n
$$

dengan ideal pelenyapan $\operatorname{Id}(V)$, gelanggang

$$
R(V)=K[X_1,\ldots,X_n]/\operatorname{Id}(V)
$$

disebut *gelanggang koordinat* dari $V$.

Pengertian ini tidak sepenuhnya tanpa masalah, terutama apabila $K$ tidak
tertutup secara aljabar; lihat contoh-contoh di bawah. Mula-mula kita catat
beberapa sifat elementer.

<!-- upstream_entity: Affine-algebraische Mengen/Koordinatenring/Grundeigenschaften/Fakt -->

### Proposisi: sifat-sifat dasar gelanggang koordinat {#br-ak-2025-2026-l11-prop-01}

Misalkan $V\subseteq\mathbb A_K^n$ suatu himpunan aljabar afin dan

$$
R=K[X_1,\ldots,X_n]/\operatorname{Id}(V)
$$

gelanggang koordinatnya. Maka berlaku pernyataan-pernyataan berikut.

1. $R$ tereduksi.
2. $V=\varnothing$ tepat ketika $R$ merupakan gelanggang nol.
3. $V$ tak tereduksi tepat ketika $R$ merupakan domain integral.
4. $V$ terdiri atas tepat satu titik ketika $R=K$.
5. Jika $K$ tertutup secara aljabar dan $V=V(\mathfrak a)$, maka

   $$
   R=K[X_1,\ldots,X_n]/\operatorname{rad}(\mathfrak a).
   $$

#### Bukti {#br-ak-2025-2026-l11-prop-01-proof}

Misalkan $I=\operatorname{Id}(V)$ ideal pelenyapan $V$.

1. Pernyataan ini mengikuti dari Lema 3.14 dan Soal 3.13.
2. Kesamaan $V=\varnothing$ ekuivalen dengan $1\in I$, dan ini ekuivalen
   dengan $R=0$.
3. Pernyataan ini mengikuti dari Lema 4.3 dan Soal 4.17.
4. Misalkan $V=\{P\}$ dengan $P=(a_1,\ldots,a_n)$. Maka

   $$
   I=(X_1-a_1,\ldots,X_n-a_n)
   $$

   dan gelanggang koordinatnya ialah

   $$
   K[X_1,\ldots,X_n]/(X_1-a_1,\ldots,X_n-a_n)\cong K.
   $$

   Sebaliknya, jika gelanggang koordinatnya adalah $K$, homomorfisme faktor
   yang bersesuaian harus merupakan homomorfisme evaluasi $X_i\mapsto a_i$.
   Ideal pelenyapan $V$ harus merupakan ideal titik, dan
   $P=(a_1,\ldots,a_n)\in V$. Jika ada titik lain $Q\in V$, $Q\ne P$, kita
   memperoleh kontradiksi karena tidak semua $X_i-a_i$ lenyap di $Q$.
5. Jika $K$ tertutup secara aljabar, Nullstellensatz Hilbert memberikan

   $$
   \operatorname{Id}(V)=\operatorname{rad}(\mathfrak a).
   $$

<!-- upstream_entity: Affin-algebraische Mengen/Affiner Raum/Unendlicher Körper/Koordinatenring ist Polynomring/Fakt -->

### Teorema: gelanggang koordinat ruang afin di atas lapangan tak berhingga {#br-ak-2025-2026-l11-thm-03}

Misalkan $K$ lapangan tak berhingga. Ideal pelenyapan ruang afin
$\mathbb A_K^n$ adalah ideal nol, dan gelanggang koordinatnya merupakan
gelanggang polinomial $K[X_1,\ldots,X_n]$.

#### Bukti {#br-ak-2025-2026-l11-thm-03-proof}

Kita membuktikan pernyataan dengan induksi pada banyaknya variabel. Untuk
$n=1$, pernyataan mengikuti dari fakta bahwa polinom berderajat $d$ mempunyai
paling banyak $d$ akar.

Untuk langkah induksi, misalkan

$$
F\in K[X_1,\ldots,X_n]
$$

suatu polinom yang lenyap pada setiap titik
$\mathbb A_K^n=K^n$. Tulis $F$ sebagai

$$
F=P_dX_n^d+P_{d-1}X_n^{d-1}+\cdots+P_1X_n+P_0,
$$

dengan

$$
P_d,\ldots,P_0\in K[X_1,\ldots,X_{n-1}].
$$

Kita harus menunjukkan bahwa $F=0$, yang ekuivalen dengan $P_i=0$ untuk
setiap $i=0,\ldots,d$. Andaikan, tanpa mengurangi keumuman, $P_d$ bukan
polinom nol. Menurut hipotesis induksi, $P_d$ juga bukan fungsi nol. Jadi,
terdapat titik $(a_1,\ldots,a_{n-1})$ dengan

$$
P_d(a_1,\ldots,a_{n-1})\ne0.
$$

Dengan demikian, $F(a_1,\ldots,a_{n-1})$ merupakan polinom tak nol berderajat
$d$ dalam satu variabel $X_n$. Menurut kasus satu variabel, polinom itu tidak
dapat menjadi fungsi nol, suatu kontradiksi.

> **Catatan edisi:** Saksi TeX sumber menuliskan suku linear sebagai
> $P_1X_0$. Konteks ekspansi menurut variabel $X_n$ mengharuskan $P_1X_n$;
> edisi ini menggunakan indeks yang konsisten dan mempertahankan salah cetak
> sumber dalam catatan ini.

<!-- upstream_entity: Affin-algebraische Mengen/Affiner Raum/Endlicher Körper/Großes Verschwindungsideal/Beispiel -->

### Contoh: lapangan berhingga {#br-ak-2025-2026-l11-ex-02}

Teorema 11.8 tidak benar untuk lapangan berhingga. Di atas lapangan berhingga,
ruang afin hanya terdiri atas hingga banyak titik dan terdapat banyak polinom
yang lenyap pada semua titik itu. Contoh khas diberikan oleh polinom

$$
X_i^q-X_i,
$$

dengan $q$ banyaknya unsur lapangan.

<!-- upstream_entity: Affin-algebraische Mengen/Reelle affine Ebene/X^2+Y^2/Verschwindungsideal und Koordinatenring/Beispiel -->

### Contoh: gelanggang faktor dan gelanggang koordinat dapat berbeda {#br-ak-2025-2026-l11-ex-03}

Misalkan

$$
R=\mathbb R[X,Y]/(X^2+Y^2).
$$

Karena kuadrat bilangan real tidak pernah negatif, lokus nol
$X^2+Y^2$ hanya terdiri atas titik asal:

$$
V(X^2+Y^2)=\{(0,0)\}.
$$

Ideal pelenyapannya adalah ideal maksimal $(X,Y)$, sehingga gelanggang
koordinat yang bersesuaian ialah

$$
\mathbb R[X,Y]/(X,Y)\cong\mathbb R.
$$

Jadi, gelanggang koordinat dapat sangat berbeda dari gelanggang faktor awal
yang idealnya digunakan untuk mendefinisikan lokus nol.

## Nullstellensatz Hilbert untuk himpunan aljabar afin {#br-ak-2025-2026-l11-s03}

Nullstellensatz Hilbert yang telah dirumuskan untuk ruang afin dan gelanggang
polinomial berlaku secara bersesuaian bagi setiap $V(\mathfrak a)$ dan
gelanggang faktor $K[X_1,\ldots,X_n]/\mathfrak a$.

<!-- upstream_entity: Affine Varietäten/Hilbertscher Nullstellensatz (geometrisch)/Algebraisch abgeschlossen/Fakt -->

### Korolari: Nullstellensatz pada suatu himpunan aljabar afin {#br-ak-2025-2026-l11-cor-03}

Misalkan $K$ lapangan yang tertutup secara aljabar dan

$$
R=K[X_1,\ldots,X_n]/\mathfrak a
$$

suatu $K$-aljabar tipe hingga dengan lokus nol

$$
V=V(\mathfrak a)\subseteq\mathbb A_K^n.
$$

Misalkan $\mathfrak b$ suatu ideal dalam $R$, dan $F\in R$ suatu unsur yang
lenyap pada $V(\mathfrak b)\subseteq V$. Maka terdapat $r\in\mathbb N$ dengan

$$
F^r\in\mathfrak b
$$

dalam $R$.

#### Bukti {#br-ak-2025-2026-l11-cor-03-proof}

Syarat pelenyapan $V(\mathfrak b)\subseteq V(F)$ di dalam
$V=V(\mathfrak a)$, jika diterjemahkan kembali ke ruang afin, menyatakan

$$
V(\mathfrak a+\mathfrak b)
=V(\mathfrak a)\cap V(\mathfrak b)
\subseteq V(F),
$$

dengan $F$ sekarang suatu polinom wakil dalam $K[X_1,\ldots,X_n]$ dan
$\mathfrak b$ ideal prapeta di gelanggang itu. Menurut Nullstellensatz Hilbert
untuk ruang afin, terdapat $r\in\mathbb N$ dengan

$$
F^r\in\mathfrak a+\mathfrak b.
$$

Modulo $\mathfrak a$, ini tepat berarti $F^r\in\mathfrak b$ dalam $R$.

<!-- upstream_entity: Affine Varietäten/Algebraisch abgeschlossener Körper/D(f i) überdeckt/Erzeugt Einheitsideal/Fakt -->

### Korolari: penutup utama pada suatu himpunan aljabar afin {#br-ak-2025-2026-l11-cor-04}

Misalkan $K$ lapangan yang tertutup secara aljabar dan
$V=V(\mathfrak a)\subseteq\mathbb A_K^n$ suatu himpunan aljabar afin yang
dideskripsikan oleh ideal $\mathfrak a$. Misalkan

$$
F_i\in K[X_1,\ldots,X_n],\qquad i\in I,
$$

sedemikian sehingga

$$
V=\bigcup_{i\in I}D(F_i).
$$

Maka kelas semua $F_i$ membangkitkan ideal satuan dalam
$K[X_1,\ldots,X_n]/\mathfrak a$.

#### Bukti {#br-ak-2025-2026-l11-cor-04-proof}

Misalkan $\mathfrak b$ ideal dalam
$K[X_1,\ldots,X_n]/\mathfrak a$ yang dibangkitkan oleh semua $F_i$,
$i\in I$. Asumsi menyatakan bahwa

$$
V(\mathfrak b)=\bigcap_{i\in I}V(F_i)
$$

kosong pada $V$. Karena $V(1)$ juga kosong, $V(1)\subseteq V(\mathfrak b)$.
Menurut Nullstellensatz Hilbert, suatu pangkat dari $1$, jadi $1$ sendiri,
termasuk dalam $\mathfrak b$.

<!-- upstream_entity: Affine Varietäten/Algebraisch abgeschlossener Körper/Einheit auf Nullstellenmenge und im Restklassenring/Fakt -->

### Korolari: polinom tanpa akar merupakan unit {#br-ak-2025-2026-l11-cor-05}

Misalkan $K$ lapangan yang tertutup secara aljabar dan
$V=V(\mathfrak a)\subseteq\mathbb A_K^n$ suatu himpunan aljabar afin yang
dideskripsikan oleh ideal $\mathfrak a$. Jika
$F\in K[X_1,\ldots,X_n]$ tidak mempunyai akar pada $V$, maka kelas $F$
merupakan unit dalam gelanggang faktor

$$
K[X_1,\ldots,X_n]/\mathfrak a.
$$

#### Bukti {#br-ak-2025-2026-l11-cor-05-proof}

Ini merupakan kasus khusus Korolari 11.12.

Dalam Contoh 11.5, fungsi $X^2+2Y^2-1$ tidak mempunyai akar pada lokus nol real
$V(X^2+Y^2-2)$, sehingga fungsi itu bernilai unit di setiap titik lokus
tersebut. Namun, fungsi itu bukan unit dalam gelanggang koordinat

$$
\mathbb R[X,Y]/(X^2+Y^2-2).
$$
