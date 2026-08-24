---
title: "Kuliah 2 — Himpunan Aljabar Afin"
stable_id: br-ak-2025-2026-l02
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 2"
upstream_pageid: 165891
upstream_revid: 1055217
upstream_timestamp: "2025-10-10T09:51:04Z"
upstream_mediawiki_sha1: be3bd8706fc4945584860560ee832690f17184ab
source_url: "https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)/Vorlesung_2?oldid=1055217"
license: "CC BY-SA 4.0 for translated course text; media retain component licences in authority/RIGHTS-unit-02.csv"
translation_status: complete
---

# Kuliah 2: Himpunan Aljabar Afin {#br-ak-2025-2026-l02}

## Himpunan aljabar afin {#br-ak-2025-2026-l02-s01}

### Definisi: ruang afin {#br-ak-2025-2026-l02-def-01}

Misalkan $K$ suatu lapangan. Ruang

$$
\mathbb A_K^n=K^n
$$

disebut *ruang afin* berdimensi $n$ di atas $K$.

Jadi, mula-mula ruang afin hanyalah suatu himpunan titik. Sebuah titik dalam
ruang afin adalah sebuah $n$-tupel $(a_1,\ldots,a_n)$ yang koordinatnya berasal
dari $K$. Mengapa kita memerlukan istilah baru? Istilah “ruang afin” menunjukkan
bahwa kita ingin memandang $K^n$ sebagai objek geometri aljabar. Artinya, kita
memandang ruang afin berdimensi $n$ sebagai objek geometri alami tempat
polinom-polinom dalam $n$ variabel bekerja sebagai fungsi. Secara bertahap kita
akan memperkaya ruang afin dengan struktur lain—topologi Zariski dan berkas
struktur—yang memperlihatkan bahwa ruang ini “lebih” daripada “sekadar” $K^n$.
Untuk $n=1$ kita menyebutnya *garis afin*, dan untuk $n=2$ kita menyebutnya
*bidang afin*.

Suatu polinom $F\in K[X_1,\ldots,X_n]$ secara alami dapat dipandang sebagai
fungsi pada ruang afin. Untuk titik

$$
P=(a_1,\ldots,a_n)\in\mathbb A_K^n,
$$

kita menetapkan nilai

$$
F(P)=F(a_1,\ldots,a_n)
$$

dengan mengganti variabel $X_i$ oleh $a_i$ dan menghitung semuanya di dalam
$K$. Untuk suatu polinom $F\in K[X_1,\ldots,X_n]$, kita dapat menanyakan apakah
$F(P)=0$. Karena itu, salah satu objek utama yang dikaitkan dengan $F$ ialah
lokus nol yang didefinisikannya,

$$
V(F)=\{P\in\mathbb A_K^n\mid F(P)=0\}.
$$

Kita sudah menjumpai beberapa contoh dalam kuliah pertama. Namun, kita juga
perlu mempelajari lokus nol simultan dari beberapa polinom. Lokus ini adalah
irisan lokus-lokus nol setiap polinom yang terlibat—misalnya, pada irisan
kerucut, ketika sebuah kerucut dalam ruang tiga dimensi dipotong oleh berbagai
bidang.

![Irisan kerucut](authority/assets/Conic_sections_2n-330.png)

Karena itu, kita membuat definisi umum berikut.

### Definisi: lokus nol suatu keluarga polinom {#br-ak-2025-2026-l02-def-02}

Misalkan $K$ suatu lapangan dan

$$
F_j\in K[X_1,\ldots,X_n],\qquad j\in J,
$$

suatu keluarga polinom dalam $n$ variabel. Himpunan

$$
\{P\in\mathbb A_K^n\mid F_j(P)=0\text{ untuk setiap }j\in J\}
$$

disebut *lokus nol* (atau *himpunan nol*) yang didefinisikan oleh keluarga
tersebut. Himpunan ini ditulis $V(F_j,j\in J)$.

Subhimpunan ruang afin yang dapat muncul sebagai himpunan nol layak diberi nama
tersendiri.

### Definisi: himpunan aljabar afin {#br-ak-2025-2026-l02-def-03}

Misalkan $K$ suatu lapangan dan $K[X_1,\ldots,X_n]$ gelanggang polinomial dalam
$n$ variabel. Suatu subhimpunan $V\subseteq\mathbb A_K^n$ disebut *aljabar
afin* apabila merupakan himpunan nol suatu keluarga polinom $F_j$, $j\in J$,
dengan $F_j\in K[X_1,\ldots,X_n]$; yaitu, apabila

$$
V=V(F_j,j\in J).
$$

Contoh-contoh paling sederhana ialah himpunan titik berhingga pada garis afin
$\mathbb A_K^1$, yang diberikan oleh sebuah polinom tunggal, serta subruang
linear afin dalam $\mathbb A_K^n$, yang merupakan himpunan solusi suatu sistem
persamaan linear takhomogen di atas $K$.

### Contoh: sumbu dan titik asal {#br-ak-2025-2026-l02-ex-01}

Kita meninjau bidang afin $\mathbb A_K^2$ dan beberapa subhimpunan aljabar afin
di dalamnya yang didefinisikan oleh variabel $X$ dan $Y$.

- Lokus nol $V(X,Y)$ hanya terdiri atas *titik asal* $(0,0)$, sebab kedua
  variabel harus bernilai nol.
- Himpunan $V(X)$ adalah *sumbu $Y$*, yakni semua titik berbentuk $(0,y)$.
- Himpunan $V(Y)$ adalah *sumbu $X$*.
- Himpunan $V(X+Y)$ terdiri atas semua titik $(x,y)$ dengan $y=-x$; ini adalah
  *antidiagonal*.
- Himpunan $V(XY)$ terdiri atas titik-titik $(x,y)$ dengan $xy=0$. Karena $K$
  suatu lapangan, sebuah hasil kali hanya dapat bernilai nol jika salah satu
  faktornya nol. Jadi,

  $$
  V(XY)=V(X)\cup V(Y),
  $$

  yakni gabungan kedua sumbu koordinat.

Titik-titik dalam ruang afin atau pada suatu himpunan aljabar afin sering
ditafsirkan sebagai representasi objek matematika lain yang lebih rumit.
Sifat-sifat objek itu tercermin pada apakah titik yang merepresentasikannya
memenuhi persamaan aljabar tertentu; dengan kata lain, pada apakah titik tersebut
terletak pada himpunan aljabar afin tertentu. Contoh berikut menggambarkan
gagasan ini.

### Contoh: matriks sebagai titik ruang afin {#br-ak-2025-2026-l02-ex-02}

Sebuah matriks $2\times2$

$$
\begin{pmatrix}
a_{11}&a_{21}\\
a_{12}&a_{22}
\end{pmatrix}
$$

ditentukan secara unik oleh empat bilangan $a_{11},a_{21},a_{12},a_{22}\in K$.
Karena itu, matriks tersebut dapat diidentifikasi dengan sebuah titik dalam
$\mathbb A_K^4$. Dalam penafsiran ini, wajar jika variabel-variabelnya kita
tulis $X_{11},X_{21},X_{12},X_{22}$. Sekarang kita dapat menanyakan sifat
matriks mana yang dapat dideskripsikan oleh persamaan aljabar.

Sebuah matriks merupakan matriks segitiga atas tepat ketika $a_{12}=0$. Jadi,
himpunan matriks segitiga atas adalah lokus nol $X_{12}$.

Sebuah matriks dapat dibalik apabila

$$
a_{11}a_{22}-a_{12}a_{21}\ne0.
$$

Karena itu, himpunan matriks yang tidak dapat dibalik dideskripsikan oleh syarat
determinan aljabar

$$
X_{11}X_{22}-X_{12}X_{21}=0.
$$

Sebuah matriks mendeskripsikan perkalian oleh suatu skalar apabila matriks itu
diagonal dengan entri diagonal yang sama. Himpunan ini dideskripsikan oleh tiga
persamaan

$$
X_{12}=0,\qquad X_{21}=0,\qquad X_{11}-X_{22}=0.
$$

Suatu unsur $\lambda\in K$ adalah nilai eigen suatu matriks tepat ketika
$\lambda$ merupakan akar polinom karakteristik matriks itu, yakni ketika

$$
\det\begin{pmatrix}
\lambda-a_{11}&-a_{21}\\
-a_{12}&\lambda-a_{22}
\end{pmatrix}
=\lambda^2-\lambda(a_{11}+a_{22})+a_{11}a_{22}-a_{12}a_{21}=0.
$$

Dalam aljabar linear, biasanya matriks diberikan dan kita mencari akar
$\lambda$ dari polinom satu variabel ini. Kita juga dapat membalik sudut
pandang: tetapkan $\lambda$, lalu pelajari lokus nol

$$
\lambda^2-\lambda(X_{11}+X_{22})
+X_{11}X_{22}-X_{12}X_{21}=0
$$

dalam empat variabel. Persamaan ini mendeskripsikan semua matriks yang mempunyai
$\lambda$ sebagai nilai eigen.

Demikian pula, suatu matriks mempunyai dua nilai eigen berbeda
$\lambda\ne\delta$ tepat ketika

$$
\lambda^2-\lambda(X_{11}+X_{22})
+X_{11}X_{22}-X_{12}X_{21}=0
$$

dan

$$
\delta^2-\delta(X_{11}+X_{22})
+X_{11}X_{22}-X_{12}X_{21}=0.
$$

Selisih kedua persamaan itu ialah

$$
\lambda^2-\delta^2-(\lambda-\delta)(X_{11}+X_{22})=0.
$$

Karena $\lambda\ne\delta$, kita dapat menulisnya sebagai

$$
X_{11}+X_{22}=\lambda+\delta.
$$

Jumlah entri diagonal sebuah matriks disebut *jejak* matriks. Persamaan terakhir
menyatakan bahwa jejak matriks yang mempunyai nilai eigen
$\lambda\ne\delta$ harus sama dengan jumlah kedua nilai eigen itu.

Polinom karakteristik matriks juga dapat ditulis

$$
\lambda^2-\lambda\operatorname{Jejak}(M)+\det(M),
$$

dengan

$$
\operatorname{Jejak}(M)=X_{11}+X_{22},\qquad
\det(M)=X_{11}X_{22}-X_{12}X_{21}.
$$

Jadi, dua matriks mempunyai polinom karakteristik yang sama tepat ketika jejak
dan determinannya sama. Dengan demikian, himpunan matriks dengan polinom
karakteristik tertentu dapat dipandang sebagai serat pemetaan

$$
\mathbb A_K^4\longrightarrow\mathbb A_K^2,
\qquad M\longmapsto(\operatorname{Jejak}(M),\det(M)).
$$

Pemetaan ini diberikan oleh ungkapan polinomial sederhana. Apakah pemetaan ini
surjektif? Apakah semua seratnya mempunyai bentuk yang sama—apakah himpunan
matriks dengan jejak dan determinan tertentu selalu mempunyai struktur yang
sama—atau terdapat perbedaan?

Tetapkan $s$ dan $d$. Kita harus mempelajari himpunan solusi sistem

$$
X_{11}+X_{22}=s,
\qquad
X_{11}X_{22}-X_{12}X_{21}=d.
$$

Variabel $X_{11}$ ditentukan secara unik oleh $X_{22}$, dan sebaliknya. Karena
itu, kita dapat *mengeliminasi* satu variabel dengan menetapkan
$X_{22}=s-X_{11}$. Kita memperoleh sistem “ekuivalen” dalam tiga variabel
$X_{11},X_{12},X_{21}$ dengan persamaan tunggal

$$
X_{11}(s-X_{11})-X_{12}X_{21}=d,
$$

atau

$$
X_{11}^2-sX_{11}+X_{12}X_{21}+d=0.
$$

Di sini “ekuivalen” berarti bahwa himpunan solusi kedua sistem saling berbijeksi
melalui pemetaan yang diberikan oleh polinom. Bentuk terakhir menunjukkan bahwa
solusi selalu ada: kita dapat menetapkan sebarang nilai bagi $X_{11}$ lalu
memperoleh persamaan berbentuk $X_{12}X_{21}=a$, yang mempunyai solusi.

Dengan transformasi variabel linear, persamaan itu dapat disederhanakan lagi.
Andaikan $2$ dapat dibalik dalam $K$—jadi karakteristik $K$ bukan $2$. Dengan

$$
X=X_{11}-\frac{s}{2},\qquad Y=X_{12},\qquad Z=X_{21},
$$

kita memperoleh

$$
X^2+YZ+c=0,
\qquad
c=-\frac{s^2}{4}+d.
$$

Karena itu, bentuk himpunan matriks dengan jejak dan determinan tertentu hanya
bergantung pada $-s^2/4+d$. Bahkan, lokus nolnya berbeda menurut apakah suku ini
nol atau tidak. Dalam kasus pertama lokus itu mempunyai singularitas; dalam
kasus kedua tidak, sebagaimana akan kita lihat nanti.

## Ideal dan lokus nol {#br-ak-2025-2026-l02-s02}

Karena untuk sementara kita mengizinkan keluarga polinom sebarang untuk
mendefinisikan lokus nol dan himpunan aljabar afin, objek-objek itu pada awalnya
tampak sulit dikendalikan. Namun, tiga pernyataan penting berlaku; kita akan
membuktikannya secara bertahap.

1. Lokus nol suatu keluarga polinom sama dengan lokus nol ideal yang dibangkitkan
   oleh keluarga tersebut.
2. Setiap ideal mempunyai sistem pembangkit berhingga. Jadi, setiap lokus nol
   dapat dideskripsikan oleh berhingga banyak polinom (teorema basis Hilbert).
3. Di atas lapangan tertutup secara aljabar, lokus-lokus nol berkorespondensi
   secara bijektif dengan ideal-ideal radikal (teorema Nullstellensatz Hilbert).

Pernyataan pertama dapat segera kita buktikan. Dua pernyataan lainnya memerlukan
persiapan aljabar yang akan kita kembangkan dalam kuliah-kuliah berikutnya.

### Lema: keluarga polinom dan ideal yang dibangkitkannya {#br-ak-2025-2026-l02-lem-01}

Misalkan $K$ suatu lapangan dan $F_j\in K[X_1,\ldots,X_n]$, $j\in J$, suatu
keluarga polinom dalam $n$ variabel. Misalkan $\mathfrak a$ adalah ideal dalam
$K[X_1,\ldots,X_n]$ yang dibangkitkan oleh semua $F_j$. Maka

$$
V(F_j,j\in J)=V(\mathfrak a).
$$

#### Bukti {#br-ak-2025-2026-l02-lem-01-proof}

Ideal $\mathfrak a$ terdiri atas semua kombinasi linear berhingga dari
polinom-polinom $F_j$ dan, khususnya, memuat setiap $F_j$. Karena itu, inklusi

$$
V(F_j,j\in J)\supseteq V(\mathfrak a)
$$

jelas. Untuk inklusi sebaliknya, ambil
$P\in V(F_j,j\in J)$ dan $H\in\mathfrak a$. Terdapat polinom-polinom
$A_i\in K[X_1,\ldots,X_n]$ dan indeks $j_1,\ldots,j_k$ sedemikian rupa sehingga

$$
H=\sum_{i=1}^k A_iF_{j_i}.
$$

Maka

$$
H(P)=\sum_{i=1}^k A_i(P)F_{j_i}(P)=0.
$$

Jadi, setiap unsur ideal tersebut lenyap di $P$, sehingga
$P\in V(\mathfrak a)$. $\square$

Dengan demikian, selanjutnya kita dapat menganggap bahwa setiap himpunan nol
diberikan oleh sebuah ideal.

### Lema: inklusi ideal membalik inklusi lokus nol {#br-ak-2025-2026-l02-lem-02}

Untuk ideal-ideal $\mathfrak a\subseteq\mathfrak b$ dalam
$K[X_1,\ldots,X_n]$, lokus-lokus nol yang bersesuaian memenuhi

$$
V(\mathfrak a)\supseteq V(\mathfrak b).
$$

#### Bukti {#br-ak-2025-2026-l02-lem-02-proof}

Ambil $P\in V(\mathfrak b)$. Artinya, $F(P)=0$ bagi setiap
$F\in\mathfrak b$. Karena $\mathfrak a\subseteq\mathfrak b$, tentu
$F(P)=0$ bagi setiap $F\in\mathfrak a$. Jadi,
$P\in V(\mathfrak a)$. $\square$

Subhimpunan aljabar afin dari ruang afin memenuhi sifat-sifat struktural penting
berikut.

### Proposisi: gabungan dan irisan himpunan aljabar afin {#br-ak-2025-2026-l02-prop-01}

Misalkan $K$ suatu lapangan, $K[X_1,\ldots,X_n]$ gelanggang polinomial dalam
$n$ variabel, dan $\mathbb A_K^n$ ruang afin yang bersesuaian. Sifat-sifat
berikut berlaku.

1. $V(0)=\mathbb A_K^n$; jadi, seluruh ruang afin adalah himpunan aljabar afin.
2. $V(1)=\varnothing$; jadi, himpunan kosong adalah himpunan aljabar afin.
3. Jika $V_1,\ldots,V_k$ adalah himpunan aljabar afin dengan
   $V_i=V(\mathfrak a_i)$, maka

   $$
   V_1\cup V_2\cup\cdots\cup V_k
   =V(\mathfrak a_1\mathfrak a_2\cdots\mathfrak a_k).
   $$

   Khususnya, gabungan berhingga himpunan-himpunan aljabar afin juga merupakan
   himpunan aljabar afin.
4. Jika $V_i$, $i\in I$, adalah himpunan aljabar afin dengan
   $V_i=V(\mathfrak a_i)$, maka

   $$
   \bigcap_{i\in I}V_i=V\left(\sum_{i\in I}\mathfrak a_i\right).
   $$

   Khususnya, irisan sebarang banyak himpunan aljabar afin juga merupakan
   himpunan aljabar afin.

#### Bukti {#br-ak-2025-2026-l02-prop-01-proof}

Pernyataan (1) dan (2) jelas: polinom konstan $0$ lenyap di setiap titik,
sedangkan polinom konstan $1$ tidak lenyap di titik mana pun.

Untuk (3), ambil titik dalam gabungan tersebut, katakanlah
$P\in V(\mathfrak a_1)$. Maka $f(P)=0$ bagi setiap
$f\in\mathfrak a_1$. Setiap unsur ideal hasil kali
$\mathfrak a_1\cdots\mathfrak a_k$ berbentuk

$$
h=\sum_{j=1}^m r_j f_{1j}f_{2j}\cdots f_{kj},
$$

dengan $f_{ij}\in\mathfrak a_i$. Karena selalu $f_{1j}(P)=0$, kita memperoleh
$h(P)=0$. Jadi, $P$ berada pada lokus nol di ruas kanan.

Sebaliknya, andaikan $P$ tidak berada dalam gabungan di ruas kiri. Maka
$P\notin V(\mathfrak a_i)$ untuk setiap $i=1,\ldots,k$. Untuk setiap $i$,
terdapat $f_i\in\mathfrak a_i$ dengan $f_i(P)\ne0$. Karena $K$ lapangan,

$$
(f_1f_2\cdots f_k)(P)\ne0,
$$

padahal $f_1f_2\cdots f_k\in\mathfrak a_1\cdots\mathfrak a_k$. Jadi, $P$
tidak mungkin berada pada lokus nol di ruas kanan.

Untuk (4), ambil $P\in\mathbb A_K^n$. Titik $P$ berada dalam
$V(\mathfrak a_i)$ untuk setiap $i\in I$ tepat ketika $f(P)=0$ bagi setiap
$f\in\mathfrak a_i$ dan setiap $i\in I$. Hal ini terjadi tepat ketika $f(P)=0$
bagi setiap $f$ dalam jumlah ideal-ideal tersebut. $\square$

![Contoh himpunan aljabar](authority/assets/Conjuntos_algebraicos_2.svg)

---

**Navigasi sumber:** [mata kuliah](https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)) · [Kuliah 1](#br-ak-2025-2026-l01) · [Kuliah 3 (sumber)](https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)/Vorlesung_3) · [Lembar Kerja 2](#br-ak-2025-2026-w02)
