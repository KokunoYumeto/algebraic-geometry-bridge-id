---
title: "Kuliah 5 - Komponen Homogen, Normalisasi Noether, dan Pemetaan Polinomial"
stable_id: br-ak-2025-2026-l05
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 5"
upstream_pageid: 165894
upstream_revid: 1051269
upstream_timestamp: "2025-08-18T07:26:27Z"
upstream_mediawiki_sha1: 31f879dfdf7a47a2387eb3fa1200ae7918cc205e
source_url: "https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)/Vorlesung_5?oldid=1051269"
license: "CC BY-SA 4.0 for translated course text; media retain component rights in authority/RIGHTS-unit-05.csv"
translation_status: complete
---

# Kuliah 5: Komponen Homogen, Normalisasi Noether, dan Pemetaan Polinomial {#br-ak-2025-2026-l05}

## Komponen homogen {#br-ak-2025-2026-l05-s01}

Kita membahas derajat dan dekomposisi polinom dalam beberapa variabel menjadi
komponen-komponen homogen.

### Definisi: derajat {#br-ak-2025-2026-l05-def-01}

Misalkan $S$ suatu gelanggang komutatif dan

$$
R=S[X_1,\ldots,X_n]
$$

gelanggang polinomial dalam $n$ variabel di atas $S$. Untuk suatu monomial

$$
G=X^\nu=X_1^{\nu_1}\cdots X_n^{\nu_n},
$$

bilangan

$$
|\nu|=\sum_{j=1}^n\nu_j
$$

disebut *derajat* $G$. Untuk polinom taknol

$$
F=\sum_\nu a_\nu X^\nu,
$$

bilangan

$$
\max\{|\nu|:a_\nu\ne0\}
$$

disebut *derajat* $F$.

### Definisi: dekomposisi homogen {#br-ak-2025-2026-l05-def-02}

Misalkan $S$ dan $R=S[X_1,\ldots,X_n]$ seperti di atas. Untuk suatu polinom

$$
F=\sum_\nu a_\nu X^\nu\in R,
$$

dekomposisi

$$
F=\sum_{i=0}^d F_i,
$$

dengan

$$
F_i=\sum_{\substack{\nu\\|\nu|=i}}a_\nu X^\nu,
$$

disebut *dekomposisi homogen* dari $F$. Polinom $F_i$ disebut *komponen
homogen* dari $F$ yang berderajat $i$. Polinom $F$ sendiri disebut *homogen*
apabila dekomposisi homogennya hanya mempunyai satu komponen taknol.

![Sebuah kerucut (himpunan nol dari polinom homogen)](authority/assets/Kuzel_obecny.svg)

Himpunan nol suatu polinom homogen $F$ merupakan kerucut garis melalui titik
asal: jika suatu titik $P$ berada dalam $V(F)$, maka seluruh garis melalui
$P$ dan $0$ juga berada dalam $V(F)$.

### Contoh: derajat total dan derajat terhadap satu variabel {#br-ak-2025-2026-l05-ex-01}

Polinom

$$
F=4X^3YZ^2+2X^2Y^5+5XYZ^7-3X^4YZ^4+X^8-Y^7+2Y^6Z^3+X+5
$$

berderajat $9$, dengan komponen-komponen homogen

$$
F_9=5XYZ^7-3X^4YZ^4+2Y^6Z^3,
$$

$$
F_8=X^8,
$$

$$
F_7=2X^2Y^5-Y^7,
$$

$$
F_6=4X^3YZ^2,
$$

$$
F_5=F_4=F_3=F_2=0,
$$

serta

$$
F_1=X,
\qquad
F_0=5.
$$

Jika $F$ dipandang sebagai polinom dalam
$(K[Y,Z])[X]$ dan kita hanya memperhatikan pangkat $X$, kita berbicara tentang
*derajat-$X$*. Derajat-$X$ dari $F$ adalah $8$. Ada pula dekomposisi homogen
terhadap gradasi-$X$: komponen berderajat-$X$ nol adalah

$$
-Y^7+2Y^6Z^3+5,
$$

sedangkan komponen berderajat-$X$ satu adalah

$$
5XYZ^7+X.
$$

## Banyaknya titik pada kurva II {#br-ak-2025-2026-l05-s02}

![Emmy Noether (1882-1935)](authority/assets/Noether.jpg)

Teorema berikut disebut teorema *normalisasi Noether* dalam kasus kurva
bidang.

### Teorema: normalisasi Noether untuk kurva bidang {#br-ak-2025-2026-l05-thm-01}

Misalkan $K$ suatu medan tertutup secara aljabar dan
$F\in K[X,Y]$ suatu polinom takkonstan berderajat $d$ yang mendefinisikan
kurva aljabar

$$
C=V(F).
$$

Terdapat suatu transformasi koordinat linear sedemikian sehingga, dalam
koordinat baru $\widetilde X,\widetilde Y$, polinom yang ditransformasikan
mempunyai bentuk

$$
\widetilde F=\widetilde X^d+\text{suku-suku berderajat lebih rendah dalam }\widetilde X.
$$

#### Bukti {#br-ak-2025-2026-l05-thm-01-proof}

Tuliskan dekomposisi homogen

$$
F=F_d+F_{d-1}+\cdots+F_1+F_0,
$$

dengan

$$
F_i=\sum_{a+b=i}c_{a,b}X^aY^b.
$$

Polinom homogen dalam dua variabel mempunyai sifat faktorisasi yang sama
dengan polinom dalam satu variabel. Karena $K$ tertutup secara aljabar,
terdapat faktorisasi

$$
F_d=c(Y-e_1X)\cdots(Y-e_kX)X^{d-k}.
$$

Karena $c$ mempunyai akar ke-$d$, dengan menskalakan variabel kita dapat
mengandaikan $c=1$. Medan $K$ khususnya takhingga, sehingga kita dapat memilih
$e\in K$ yang berbeda dari semua $e_j$. Gunakan koordinat baru

$$
\widetilde Y=Y-eX,
\qquad
\widetilde X=X.
$$

Dalam koordinat ini, setiap faktor linear menjadi

$$
\begin{aligned}
Y-e_jX
&=Y-eX+eX-e_jX\\
&=\widetilde Y-(e_j-e)X\\
&=\widetilde Y-(e_j-e)\widetilde X,
\end{aligned}
$$

dengan $e_j-e\ne0$, sedangkan faktor $X$ menjadi $\widetilde X$. Setelah
dikalikan, $\widetilde X^d$ muncul dengan koefisien taknol di $K$, yang sekali
lagi dapat dibuat sama dengan $1$ melalui penskalaan. Karena komponen homogen
berderajat lebih rendah tetap mempertahankan derajatnya, semua monomial lain
mempunyai derajat-$\widetilde X$ paling tinggi $d-1$. $\square$

### Korolari: kurva bidang mempunyai takhingga banyak titik {#br-ak-2025-2026-l05-cor-01}

Misalkan $K$ suatu medan tertutup secara aljabar dan
$F\in K[X,Y]$ suatu polinom takkonstan yang mendefinisikan kurva aljabar
$C=V(F)$. Maka $C$ mempunyai takhingga banyak elemen.

#### Bukti {#br-ak-2025-2026-l05-cor-01-proof}

Menurut teorema normalisasi Noether, kita dapat mengandaikan

$$
F=X^d+P_{d-1}(Y)X^{d-1}+\cdots+P_1(Y)X+P_0(Y),
$$

dengan $P_i(Y)\in K[Y]$. Untuk setiap nilai $a\in K$ yang diberikan bagi
$Y$, substitusi $Y=a$ menghasilkan polinom monik berderajat $d$ dalam $X$.
Karena $K$ tertutup secara aljabar, polinom itu mempunyai sedikitnya satu
akar $b\in K$. Jadi titik dengan koordinat $X=b$ dan $Y=a$ berada pada
$C$. Karena $K$ takhingga, kurva tersebut mempunyai takhingga banyak titik.
$\square$

**Catatan edisi:** setelah menetapkan $Y=a$ dan memilih akar $X=b$, sumber
menulis pasangan titik sebagai $(a,b)$. Edisi ini menyebut kedua koordinat
secara eksplisit agar urutannya tetap $X=b$, $Y=a$.

## Pemetaan polinomial antara ruang-ruang afin {#br-ak-2025-2026-l05-s03}

Pertimbangkan pemetaan

$$
\begin{aligned}
\varphi:\mathbb A_K^r&\longrightarrow\mathbb A_K^n,\\
(t_1,\ldots,t_r)&\longmapsto
(\varphi_1(t_1,\ldots,t_r),\ldots,\varphi_n(t_1,\ldots,t_r))
=(x_1,\ldots,x_n),
\end{aligned}
$$

dengan setiap fungsi komponen
$\varphi_i\in K[T_1,\ldots,T_r]$. Jadi, setiap komponen pemetaan diberikan oleh
suatu polinom dalam $r$ variabel. Kasus $n=1$ adalah sebuah polinom dalam $r$
variabel; kasus $r=1$ dan $n=2$ adalah parametrisasi kurva aljabar. Kelak kita
akan mendefinisikan morfisme antara himpunan-himpunan aljabar afin dengan
generalisasi yang lebih luas.

**Catatan edisi:** sumber mencetak gelanggang fungsi komponen sebagai
$K[X_1,\ldots,X_r]$, walaupun parameter pemetaan dan gelanggang sasaran
homomorfisme substitusinya memakai $T_1,\ldots,T_r$. Edisi ini menggunakan
$K[T_1,\ldots,T_r]$ secara konsisten.

Suatu pemetaan polinomial
$\varphi:\mathbb A_K^r\to\mathbb A_K^n$ menginduksi homomorfisme aljabar-$K$
antara gelanggang polinomial dalam arah berlawanan. Homomorfisme substitusi
itu ditentukan oleh $X_i\mapsto\varphi_i$ dan ditulis

$$
\begin{aligned}
\widetilde\varphi:
K[X_1,\ldots,X_n]&\longrightarrow K[T_1,\ldots,T_r],\\
F&\longmapsto F\circ\varphi
=F(\varphi_i/X_i).
\end{aligned}
$$

Notasi $\varphi_i/X_i$ berarti mengganti variabel $X_i$ dengan
$\varphi_i$. Dipandang sebagai fungsi, $F\circ\varphi$ adalah komposisi

$$
\mathbb A_K^r\xrightarrow{\varphi}\mathbb A_K^n
\xrightarrow{F}\mathbb A_K^1.
$$

Untuk lokus nol $V(F)\subseteq\mathbb A_K^n$ berlaku

$$
\varphi^{-1}(V(F))=V(\widetilde\varphi(F)).
$$

Selain pemetaan konstan, pemetaan polinomial yang paling sederhana adalah
pemetaan afin-linear, yaitu pemetaan yang fungsi-fungsi komponennya merupakan
polinom afin-linear:

$$
\varphi_i=a_{i1}T_1+\cdots+a_{ir}T_r+c_i.
$$

Pemetaan ini tidak harus linear karena titik asal tidak harus dipetakan ke
titik asal; translasi diperbolehkan. Pemetaan afin-linear merupakan komposisi
pemetaan linear dan translasi. Untuk $r=n$, suatu pemetaan afin-linear yang
bijektif dipandang sebagai transformasi koordinat atau transformasi variabel.

### Definisi: transformasi variabel afin-linear {#br-ak-2025-2026-l05-def-03}

Misalkan $K$ suatu medan. Suatu pemetaan
$\varphi:\mathbb A_K^n\to\mathbb A_K^n$ berbentuk

$$
\varphi(x_1,\ldots,x_n)
=M
\begin{pmatrix}
x_1\\
\vdots\\
x_n
\end{pmatrix}
+(v_1,\ldots,v_n),
$$

dengan $M$ suatu matriks invertibel, disebut *transformasi variabel
afin-linear*.

Orang dapat memperdebatkan apakah transformasi variabel linear benar-benar
memindahkan sesuatu di ruang atau hanya mengubah koordinat. Bagaimanapun,
transformasi demikian merupakan alat penting untuk membawa polinom, sistem
persamaan aljabar, atau himpunan aljabar afin ke bentuk yang lebih sederhana.
Di bawah transformasi variabel, himpunan

$$
V=V(F_1,\ldots,F_m)
$$

berubah menjadi

$$
\widetilde V=V(\widetilde F_1,\ldots,\widetilde F_m),
\qquad
\widetilde F_i=\widetilde\varphi(F_i),
$$

dan $\widetilde V$ adalah prapeta $V$ di bawah $\varphi$.

### Definisi: ekuivalensi afin-linear {#br-ak-2025-2026-l05-def-04}

Dua himpunan aljabar afin

$$
V,\widetilde V\subseteq\mathbb A_K^n
$$

disebut *ekuivalen afin-linear* apabila terdapat transformasi variabel
afin-linear $\varphi:\mathbb A_K^n\to\mathbb A_K^n$ sedemikian sehingga

$$
\varphi^{-1}(V)=\widetilde V.
$$

Konsep ini bergantung pada bagaimana situasi tersebut tertanam. Kelak kita
akan melihat bahwa parabola dan garis di bidang saling isomorfik karena
keduanya isomorfik dengan garis afin, tetapi keduanya tidak ekuivalen secara
afin-linear.

Sifat-sifat aljabar dan topologis yang esensial dari suatu himpunan aljabar
afin tetap terpelihara di bawah transformasi variabel afin-linear, termasuk
ketaktereduksian, singularitas, perpotongan, keterhubungan, dan kekompakan.
Sebaliknya, sifat-sifat khas geometri metrik real dapat berubah: sudut,
panjang dan perbandingan panjang, volume, serta bentuk. Konsep-konsep terakhir
itu tidak relevan bagi geometri aljabar. Karena itu, mulai sekarang kita akan
mengubah suatu situasi ke bentuk yang diinginkan tanpa banyak penekanan jika
transformasi semacam itu tersedia.

### Teorema: gelanggang hasil bagi di bawah ekuivalensi afin-linear {#br-ak-2025-2026-l05-thm-02}

Misalkan $K$ suatu medan dan
$V,\widetilde V\subseteq\mathbb A_K^n$ dua himpunan aljabar afin yang ekuivalen
afin-linear. Misalkan $\operatorname{Id}(V)$ dan
$\operatorname{Id}(\widetilde V)$ ideal-ideal pelenyapan yang bersesuaian.
Maka terdapat isomorfisme aljabar-$K$

$$
K[X_1,\ldots,X_n]/\operatorname{Id}(V)
\cong
K[X_1,\ldots,X_n]/\operatorname{Id}(\widetilde V).
$$

#### Bukti {#br-ak-2025-2026-l05-thm-02-proof}

Menurut definisi, terdapat transformasi variabel afin-linear

$$
\mathbb A_K^n\longrightarrow\mathbb A_K^n,
\qquad
P\longmapsto\varphi(P),
$$

dengan $\varphi^{-1}(V)=\widetilde V$. Misalkan $\widetilde\varphi$
automorfisme yang bersesuaian dari $K[X_1,\ldots,X_n]$. Maka

$$
\widetilde\varphi^{-1}\bigl(\operatorname{Id}(\widetilde V)\bigr)
=\operatorname{Id}(V).
$$

Teorema isomorfisme menghasilkan isomorfisme kedua gelanggang hasil bagi.
$\square$

### Catatan: gelanggang koordinat sebagai invarian intrinsik {#br-ak-2025-2026-l05-rem-01}

Teorema sebelumnya mengungkapkan suatu prinsip penting dalam geometri
aljabar: objek aljabar yang melekat pada suatu lokus nol adalah gelanggang
hasil bagi gelanggang polinomial oleh ideal pelenyapannya. Objek ini merupakan
*invarian intrinsik* dari lokus nol, yaitu tidak bergantung pada penanamannya.

Dari sudut pandang ini, normalisasi Noether untuk kurva bidang memperoleh
makna baru. Kita dapat mengandaikan persamaan kurva berbentuk

$$
F=X^d+P_{d-1}(Y)X^{d-1}+\cdots+P_1(Y)X+P_0(Y).
$$

Persamaan $F=0$ merupakan persamaan integral bagi kelas residu $X$. Lebih
tepatnya, kelas residu $X$ dalam $K[X,Y]/(F)$ integral atas $K[Y]$. Karena
$X$ membangkitkan gelanggang itu sebagai aljabar atas $K[Y]$, terdapat
perluasan gelanggang integral, bahkan hingga,

$$
K[Y]\longrightarrow
K[X,Y]/\bigl(X^d+P_{d-1}(Y)X^{d-1}+\cdots+P_1(Y)X+P_0(Y)\bigr).
$$

Dengan demikian, teorema normalisasi Noether juga mengatakan bahwa, untuk
setiap kurva aljabar di atas medan tertutup secara aljabar, gelanggang
koordinatnya dapat direalisasikan sebagai perluasan hingga dari domain ideal
utama $K[Y]$. Ini merupakan analogi langsung dengan gelanggang bilangan bulat
dalam teori bilangan, yang juga merupakan perluasan hingga di atas domain
ideal utama $\mathbb Z$.

Pemetaan polinomial umum antara ruang-ruang afin, berbeda dengan transformasi
afin-linear, dapat mengubah banyak sifat aljabar: dimensi dapat berubah,
singularitas dapat muncul, dan sebagainya. Namun, ketaktereduksian berpindah ke
penutupan Zariski dari citra pemetaan.

### Teorema: penutupan citra pemetaan polinomial tak tereduksi {#br-ak-2025-2026-l05-thm-03}

Misalkan $K$ suatu medan takhingga dan

$$
\varphi:\mathbb A_K^r\longrightarrow\mathbb A_K^n
$$

suatu pemetaan yang diberikan oleh $n$ polinom dalam $r$ variabel. Maka
penutupan Zariski dari citra $\varphi$ tak tereduksi.

#### Bukti {#br-ak-2025-2026-l05-thm-03-proof}

Misalkan

$$
B=\varphi(\mathbb A_K^r)
$$

citra pemetaan. Menurut Lema 3.10,

$$
\overline B=V(\operatorname{Id}(B)).
$$

Untuk $P=\varphi(Q)$ dengan $Q\in\mathbb A_K^r$ dan
$F\in K[X_1,\ldots,X_n]$ berlaku

$$
F(P)=F(\varphi(Q))=(F\circ\varphi)(Q),
$$

dengan $F\circ\varphi\in K[T_1,\ldots,T_r]$ diperoleh dengan mengganti
$X_i$ oleh fungsi komponen ke-$i$, yaitu
$\varphi_i\in K[T_1,\ldots,T_r]$. Karena itu, $F$ lenyap di seluruh $B$
tepat ketika $F\circ\varphi$ lenyap di seluruh $\mathbb A_K^r$. Karena $K$
takhingga, kondisi terakhir berarti bahwa $F\circ\varphi$ adalah polinom nol.

Jadi,

$$
F\in\operatorname{Id}(B)
$$

tepat ketika $F$ dipetakan ke nol oleh homomorfisme

$$
\widetilde\varphi:
K[X_1,\ldots,X_n]\longrightarrow K[T_1,\ldots,T_r].
$$

Dengan demikian, $\operatorname{Id}(B)$ adalah prapeta ideal prima, yakni
ideal nol di $K[T_1,\ldots,T_r]$, dan karena itu sendiri merupakan ideal
prima menurut Soal 4.19. Lema 4.3 kemudian menunjukkan bahwa
$V(\operatorname{Id}(B))$ tak tereduksi. $\square$
