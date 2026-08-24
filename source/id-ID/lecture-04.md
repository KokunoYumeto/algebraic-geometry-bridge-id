---
title: "Kuliah 4 - Ketaktereduksian, Komponen, dan Irisan Kurva"
stable_id: br-ak-2025-2026-l04
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 4"
upstream_pageid: 165893
upstream_revid: 1112250
upstream_timestamp: "2026-08-20T16:46:15Z"
upstream_mediawiki_sha1: 5931f665f4ab4e6180050ddde5164d5edc94e37a
source_url: "https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)/Vorlesung_4?oldid=1112250"
license: "CC BY-SA 4.0 for translated course text; media retain component licences in authority/RIGHTS-unit-04.csv"
translation_status: complete
---

# Kuliah 4: Ketaktereduksian, Komponen, dan Irisan Kurva {#br-ak-2025-2026-l04}

## Himpunan aljabar afin yang tak tereduksi {#br-ak-2025-2026-l04-s01}

### Definisi: himpunan tak tereduksi {#br-ak-2025-2026-l04-def-01}

Suatu himpunan aljabar afin

$$
V\subseteq\mathbb A_K^n
$$

disebut *tak tereduksi* apabila $V\ne\varnothing$ dan tidak ada dekomposisi

$$
V=Y\cup Z
$$

dengan himpunan-himpunan aljabar afin $Y,Z\subsetneq V$.

Jadi, himpunan tertutup Zariski $V$ tak tereduksi tepat ketika
$V\ne\varnothing$ dan setiap dekomposisi $V=Y\cup Z$ memaksa $V=Y$ atau
$V=Z$. Pernyataan yang sama segera berlaku bagi setiap penyajian berhingga
sebagai gabungan himpunan tertutup.

Ketaktereduksian adalah sifat yang sepenuhnya topologis. Dalam ruang topologis
umum, definisi di atas dirumuskan dengan himpunan tertutup sebagai pengganti
himpunan aljabar afin, yang memang merupakan himpunan tertutup dalam topologi
Zariski.

Gambar-gambar berikut menunjukkan beberapa subhimpunan aljabar afin yang tak
tereduksi maupun yang tereduksi. Apa komponen-komponen tak tereduksinya (lihat
definisi di bawah)?

![Titik-titik untuk triangulasi Delaunay](authority/assets/Delaunay_points.png)

![Sebuah garis](authority/assets/Gerade.svg)

![Beberapa garis lurus](authority/assets/Straight_lines.svg)

![Sebuah ruang linear](authority/assets/Linear_space2.png)

### Contoh: ruang afin {#br-ak-2025-2026-l04-ex-01}

Pertimbangkan ruang afin $\mathbb A_K^n$. Jika $K$ berhingga, ruang ini hanya
terdiri atas berhingga banyak titik dan hanya subhimpunan satu titik yang tak
tereduksi. Khususnya, kecuali untuk $n=0$, ruang afin tersebut tidak tak
tereduksi.

Sebaliknya, jika $K$ takhingga, ruang afin $\mathbb A_K^n$ tak tereduksi.
Andaikan

$$
\mathbb A_K^n=Y\cup Z
$$

dengan $Y$ dan $Z$ subhimpunan aljabar afin yang keduanya proper. Untuk
komplemen terbukanya,

$$
U=\mathbb A_K^n\setminus Y,
\qquad
W=\mathbb A_K^n\setminus Z,
$$

berlaku $U,W\ne\varnothing$, tetapi $U\cap W=\varnothing$. Hal ini
bertentangan dengan Soal 3.20.

### Lema: ketaktereduksian dan ideal prima {#br-ak-2025-2026-l04-lem-01}

Misalkan $V\subseteq\mathbb A_K^n$ suatu himpunan aljabar afin dengan ideal
pelenyapan $\operatorname{Id}(V)$. Maka $V$ tak tereduksi tepat ketika
$\operatorname{Id}(V)$ merupakan ideal prima.

#### Bukti {#br-ak-2025-2026-l04-lem-01-proof}

Mula-mula andaikan $\operatorname{Id}(V)$ bukan ideal prima. Jika

$$
\operatorname{Id}(V)=K[X_1,\ldots,X_n],
$$

maka $V=\varnothing$, sehingga $V$ tidak tak tereduksi menurut definisi.
Selain kasus itu, terdapat polinom

$$
F,G\in K[X_1,\ldots,X_n]
$$

dengan

$$
FG\in\operatorname{Id}(V),
\qquad
F,G\notin\operatorname{Id}(V).
$$

Karena itu terdapat $P,Q\in V$ dengan $F(P)\ne0$ dan $G(Q)\ne0$. Bentuk dua
ideal

$$
\mathfrak a_1=\operatorname{Id}(V)+(F),
\qquad
\mathfrak a_2=\operatorname{Id}(V)+(G).
$$

Menurut Lema 3.8(3),

$$
V(\mathfrak a_1),V(\mathfrak a_2)
\subseteq V(\operatorname{Id}(V))=V.
$$

Kedua inklusi ini proper karena $P\notin V(\mathfrak a_1)$ dan
$Q\notin V(\mathfrak a_2)$. Di sisi lain,

$$
V(\mathfrak a_1)\cup V(\mathfrak a_2)
=V(\mathfrak a_1\mathfrak a_2)
=V(\operatorname{Id}(V))
=V.
$$

Jadi, $V$ mempunyai dekomposisi taktrivial dan tidak tak tereduksi.

Sekarang andaikan $V$ tidak tak tereduksi. Jika $V=\varnothing$, maka
$\operatorname{Id}(V)$ adalah seluruh gelanggang dan bukan ideal prima.
Andaikan selanjutnya $V\ne\varnothing$ dan

$$
V=Y\cup Z
$$

merupakan dekomposisi taktrivial. Tuliskan

$$
Y=V(\mathfrak a_1),
\qquad
Z=V(\mathfrak a_2).
$$

Karena $Y\subsetneq V$, ada titik

$$
P\in V=V(\operatorname{Id}(V)),
\qquad
P\notin V(\mathfrak a_1).
$$

Maka ada $F\in\mathfrak a_1$ dengan $F(P)\ne0$, sehingga
$F\notin\operatorname{Id}(V)$. Dengan cara yang sama, ada
$G\in\mathfrak a_2$ dengan $G\notin\operatorname{Id}(V)$. Untuk setiap
$Q\in V=Y\cup Z$, berlaku $(FG)(Q)=0$, sebab $F$ lenyap pada $Y$ dan $G$
lenyap pada $Z$. Jadi,

$$
FG\in\operatorname{Id}(V),
$$

meskipun kedua faktornya tidak berada dalam ideal tersebut. Dengan demikian,
$\operatorname{Id}(V)$ bukan ideal prima. $\square$

### Definisi: komponen tak tereduksi {#br-ak-2025-2026-l04-def-02}

Misalkan $V$ suatu himpunan aljabar afin. Suatu subhimpunan aljabar afin
$W\subseteq V$ disebut *komponen tak tereduksi* dari $V$ apabila $W$ tak
tereduksi dan tidak ada subhimpunan tak tereduksi $W'$ dengan

$$
W\subsetneq W'\subseteq V.
$$

Jika $V$ tak tereduksi, maka $V$ sendiri merupakan satu-satunya komponen tak
tereduksi dari $V$. Dalam Teorema 9.11 kelak akan dibuktikan bahwa setiap
himpunan aljabar afin dapat ditulis sebagai gabungan berhingga komponen tak
tereduksi.

### Contoh: perilaku di atas bilangan real dan kompleks {#br-ak-2025-2026-l04-ex-02}

Pertimbangkan persamaan

$$
F=Y^2+X^2(X+1)^2=0.
$$

Di atas bilangan real, persamaan ini mempunyai dua solusi. Karena kuadrat real
tidak pernah negatif, $F$ hanya dapat bernilai nol jika kedua sukunya nol.
Akibatnya, $Y=0$ dan $X=0$ atau $X=-1$. Khususnya, himpunan solusi realnya
tidak terhubung dan tidak tak tereduksi; ideal pelenyapannya dalam situasi real
ini juga sangat besar.

Di atas bilangan kompleks terdapat faktorisasi

$$
F=(Y+iX(X+1))(Y-iX(X+1))
$$

menjadi polinom-polinom tak tereduksi. Hal ini sekaligus menunjukkan bahwa
$F$, sebagai polinom dalam $\mathbb R[X,Y]$, tak tereduksi, meskipun lokus nol
realnya tidak tak tereduksi. Lokus nol kompleksnya terdiri atas kedua grafik

$$
Y=\pm iX(X+1),
$$

yang beririsan di $(0,0)$ dan $(-1,0)$.

Untuk persamaan

$$
Y^2+Z^2+X^2(X+1)^2=0
$$

kembali hanya ada dua titik solusi real, sedangkan polinomnya tak tereduksi
baik di atas bilangan real maupun kompleks.

![Hidran di Pulau Krk, Kroasia](authority/assets/Hydrant_Insel_Krk_Kroatien-500.jpg)

### Contoh: irisan dua silinder yang sama besar {#br-ak-2025-2026-l04-ex-03}

Di ruang afin $\mathbb A_K^3$ dengan $K=\mathbb R$, pertimbangkan kedua
silinder

$$
S_1=\{(x,y,z)\mid x^2+y^2=1\},
\qquad
S_2=\{(x,y,z)\mid y^2+z^2=1\}.
$$

Keduanya merupakan himpunan tak tereduksi, sebagaimana akan kita lihat kelak
untuk $K$ takhingga. Seperti apakah irisannya? Irisan tersebut dideskripsikan
oleh ideal $\mathfrak a$ yang dibangkitkan oleh $X^2+Y^2-1$ dan
$Y^2+Z^2-1$. Mengurangkan satu persamaan dari persamaan lainnya memberikan

$$
X^2-Z^2=(X-Z)(X+Z)\in\mathfrak a.
$$

Namun, kedua faktor tersebut sendiri tidak berada dalam $\mathfrak a$.
Sebagai contoh, $(1,0,-1)$ merupakan titik irisan tempat $X-Z$ tidak lenyap
(untuk karakteristik $\ne2$), sedangkan $(1,0,1)$ merupakan titik irisan
tempat $X+Z$ tidak lenyap. Komponen-komponen irisan justru dideskripsikan oleh

$$
\mathfrak b_1=\mathfrak a+(X-Z),
\qquad
\mathfrak b_2=\mathfrak a+(X+Z).
$$

Keduanya ideal prima, dan gelanggang faktor yang pertama adalah

$$
\begin{aligned}
K[X,Y,Z]/\mathfrak b_1
&=K[X,Y,Z]/(\mathfrak a+(X-Z))\\
&\cong K[X,Y]/(X^2+Y^2-1).
\end{aligned}
$$

Untuk melihat isomorfisme terakhir, eliminasi $Z$ dengan persamaan $X-Z=0$;
kedua persamaan silinder lalu menjadi identik. Argumen bagi ideal lainnya
sama. Secara geometris, setiap titik $S_1\cap S_2$ terletak pada bidang

$$
E_1=V(Z-X)
\qquad\text{atau}\qquad
E_2=V(Z+X).
$$

Selain itu,

$$
E_1\cap S_1=E_1\cap S_1\cap S_2=E_1\cap S_2,
$$

dan demikian pula untuk $E_2$, sebab kedua persamaan silinder menjadi identik
pada masing-masing bidang tersebut.

Seperti apakah irisan-irisan itu jika dilihat di dalam bidangnya? Pada
$E_1$, gunakan koordinat $Y$ dan $U=Z+X$. Karena

$$
X=\frac12((Z+X)-(Z-X)),
$$

persamaan silinder pertama dapat ditulis

$$
\left(\frac12((Z+X)-(Z-X))\right)^2+Y^2=1.
$$

Di bidang $E_1$, tempat $Z=X$, persamaan ini menjadi

$$
\left(\frac12U\right)^2+Y^2=1,
$$

atau

$$
\frac14U^2+Y^2=1.
$$

Ini merupakan persamaan elips. Sebelumnya, perhitungan gelanggang faktor
$K[X,Y,Z]/\mathfrak b_1$ menghasilkan persamaan lingkaran. Tidak ada
pertentangan: lingkaran dan elips dapat diubah satu sama lain dengan
transformasi linear, sehingga gelanggang faktornya isomorfik. Sebagai
objek metrik, keduanya berbeda, dan irisan dua silinder ini terdiri atas dua
elips. Transformasi variabel ortonormal mempertahankan struktur metrik, tetapi
variabel $Y$, $X+Z$, dan $X-Z$ tidak mendefinisikan transformasi ortonormal.

Jadi,

$$
S_1\cap S_2=V(\mathfrak b_1)\cup V(\mathfrak b_2),
$$

dengan

$$
\mathfrak b_1=(X^2+Y^2-1,X-Z),
\qquad
\mathfrak b_2=(X^2+Y^2-1,X+Z),
$$

yang mendeskripsikan dua elips. Untuk menentukan bagaimana kedua elips ini
beririsan, hitung jumlah idealnya:

$$
\begin{aligned}
\mathfrak b_1+\mathfrak b_2
&=(X^2+Y^2-1,X-Z,X+Z)\\
&=(Y^2-1,X,Z).
\end{aligned}
$$

Lokus nolnya terdiri atas dua titik $(0,1,0)$ dan $(0,-1,0)$.

![Arah utama pada sebuah silinder](authority/assets/Cylinder_principal_directions-250.png)

## Banyaknya titik pada kurva {#br-ak-2025-2026-l04-s02}

Kita telah melihat bahwa irisan sebuah kurva dengan sebuah garis hanya terdiri
atas berhingga banyak titik, kecuali garis itu sendiri merupakan komponen
kurva; lihat Lema 1.3. Sekarang kita akan memperluas hasil ini ke irisan dua
kurva bidang sebarang. Kita memerlukan definisi berikut.

### Definisi: lapangan fungsi rasional {#br-ak-2025-2026-l04-def-03}

Misalkan $K$ suatu lapangan dan $K[X]$ gelanggang polinomial satu variabel di atas
$K$. Lapangan pecahan $Q(K[X])$ disebut *lapangan fungsi rasional* di atas $K$ dan
ditulis

$$
K(X).
$$

### Teorema: irisan kurva tanpa komponen bersama {#br-ak-2025-2026-l04-thm-01}

Misalkan $K$ suatu lapangan dan

$$
F,G\in K[X,Y]
$$

dua polinom tanpa faktor persekutuan yang takkonstan. Maka hanya ada berhingga
banyak titik $P_1,\ldots,P_n$ dalam $V(F,G)$.

#### Bukti {#br-ak-2025-2026-l04-thm-01-proof}

Pandang $F,G\in K[X,Y]$ sebagai unsur $K(X)[Y]$, dengan $K(X)$ lapangan fungsi
rasional dalam $X$. Menurut Soal 4.27, $F$ dan $G$ juga tidak mempunyai faktor
persekutuan dalam $K(X)[Y]$. Karena gelanggang ini merupakan domain ideal
utama, keduanya bersama-sama membangkitkan ideal satuan. Jadi, terdapat

$$
A,B\in K(X)[Y]
$$

dengan

$$
AF+BG=1.
$$

Kalikan dengan penyebut persekutuan $A$ dan $B$. Di dalam $K[X,Y]$ diperoleh

$$
\widetilde A F+\widetilde B G=H,
\qquad
0\ne H\in K[X].
$$

Setiap akar bersama $F$ dan $G$ dalam $\mathbb A_K^2$ harus menjadi akar
$H$. Dengan demikian, hanya ada berhingga banyak nilai $X$ yang mungkin muncul
dalam akar bersama. Dengan menukar peran $X$ dan $Y$, diperoleh bahwa hanya
ada berhingga banyak nilai $Y$ yang mungkin. Karena itu, jumlah akar bersama
seluruhnya berhingga. $\square$

![Dua kurva kubik](authority/assets/Two_cubic_curves.png)

### Korolari: kurva prima dengan takhingga banyak titik {#br-ak-2025-2026-l04-cor-01}

Misalkan $K$ suatu lapangan dan $F\in K[X,Y]$ suatu polinom prima. Andaikan kurva
$V(F)$ mempunyai takhingga banyak titik. Maka ideal pelenyapan $V(F)$ sama
dengan ideal utama $(F)$, dan $V(F)$ tak tereduksi.

#### Bukti {#br-ak-2025-2026-l04-cor-01-proof}

Jelas bahwa

$$
(F)\subseteq\operatorname{Id}(V(F)).
$$

Ambil $G\in\operatorname{Id}(V(F))$. Menurut Lema 3.8(3),

$$
V(F)=V(\operatorname{Id}(V(F)))\subseteq V(F,G).
$$

Jika $G$ bukan kelipatan $F$, Teorema 4.8 langsung memberikan pertentangan
dengan asumsi bahwa $V(F)$ mempunyai takhingga banyak titik. Jadi,

$$
\operatorname{Id}(V(F))=(F).
$$

Ideal ini prima, dan oleh Lema 4.3, $V(F)$ tak tereduksi. $\square$

---

**Navigasi sumber:** [mata kuliah](https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)) - [Kuliah 3](#br-ak-2025-2026-l03) - [Kuliah 5 (sumber)](https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)/Vorlesung_5) - [Lembar Kerja 4](#br-ak-2025-2026-w04)
