---
title: "Kuliah 6 - Parametrisasi Polinomial dan Rasional"
stable_id: br-ak-2025-2026-l06
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 6"
upstream_pageid: 165895
upstream_revid: 1112253
upstream_timestamp: "2026-08-20T16:51:19Z"
upstream_mediawiki_sha1: 5b0f6515a3cd3c8079cef3862b8d182c6549dcf9
source_url: "https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)/Vorlesung_6?oldid=1112253"
license: "CC BY-SA 4.0 for translated course text; media retain component rights in authority/RIGHTS-unit-06.csv"
translation_status: complete
---

# Kuliah 6: Parametrisasi Polinomial dan Rasional {#br-ak-2025-2026-l06}

## Parametrisasi polinomial bidang {#br-ak-2025-2026-l06-s01}

![Kurva berparameter dapat dibayangkan sebagai suatu lintasan gerak](authority/assets/Krivka_parametricky.png)

Sekarang kita meninjau pemetaan

$$
\varphi:\mathbb A_K^1\longrightarrow\mathbb A_K^2
$$

yang diberikan oleh dua polinom satu variabel

$$
P,Q\in K[T].
$$

Citra pemetaan semacam ini terletak pada suatu kurva aljabar afin, seperti
ditunjukkan oleh teorema berikut. Kita juga berbicara tentang *kurva
berparameter*, atau lebih tepatnya *kurva yang diparameterkan secara
polinomial*.

Di sini ada dua sudut pandang yang bersaing tentang cara mendeskripsikan
kurva aljabar. Titik-titik pada kurva yang diberikan oleh persamaan kurva
hanya ditentukan secara implisit. Untuk setiap titik bidang, mudah diperiksa
apakah titik itu terletak pada kurva, tetapi secara umum sulit menemukan atau
menuliskan titik-titik kurva secara eksplisit. Sebaliknya, kurva
berparameter diberikan secara eksplisit: bagi setiap titik garis afin, titik
citranya dapat dihitung dengan mudah, sehingga titik-titik kurva diperoleh
secara eksplisit. Namun, tidak setiap kurva aljabar dapat diparameterkan oleh
polinom.

### Teorema: persamaan bagi kurva yang diparameterkan secara polinomial {#br-ak-2025-2026-l06-thm-01}

Misalkan $K$ suatu lapangan dan $P,Q\in K[T]$ polinom. Maka terdapat polinom

$$
F\in K[X,Y],\qquad F\ne0,
$$

dengan

$$
F(P,Q)=0.
$$

Dengan kata lain, citra suatu kurva yang diparameterkan secara polinomial
terletak pada kurva aljabar bidang

$$
C=V(F).
$$

Jika $K$ takhingga dan $P,Q$ tidak keduanya konstan, penutupan Zariski citra
tersebut merupakan kurva tak tereduksi $C$.

#### Bukti {#br-ak-2025-2026-l06-thm-01-proof}

Misalkan $d$ dan $e$ masing-masing derajat $P$ dan $Q$. Kita meninjau
monomial-monomial

$$
P^iQ^j.
$$

Ini merupakan polinom dalam $T$ berderajat $di+ej$. Untuk $i\le n$ dan
$j\le m$, terdapat $(n+1)(m+1)$ monomial semacam itu. Semuanya terletak dalam
ruang vektor-$K$ berdimensi $dn+em+1$ yang dibangkitkan oleh

$$
1=T^0,T^1,T^2,\ldots,T^{dn+em}.
$$

Jika

$$
(n+1)(m+1)>dn+em+1,
$$

harus ada ketergantungan linear taktrivial di antara $P^iQ^j$. Ketergantungan
ini memberikan polinom $F(X,Y)\ne0$ dengan $F(P,Q)=0$. Syarat numerik di atas
dapat dipenuhi dengan memilih $n,m$ cukup besar.

Mulai sekarang, misalkan $K$ takhingga. Menurut Lema 3.10, penutupan Zariski
dari citra

$$
B=\varphi(\mathbb A_K^1)
$$

adalah $V(\operatorname{Id}(B))$, dan menurut Teorema 5.10 himpunan ini tak
tereduksi. Karena $K$ takhingga dan pemetaan tersebut tidak konstan,
ketaktereduksian juga memaksa $V(\operatorname{Id}(B))$ mempunyai takhingga
banyak titik. Menurut Lema 4.3, $\operatorname{Id}(B)$ merupakan ideal prima;
menurut bagian pertama, ideal ini memuat suatu

$$
F\in\operatorname{Id}(B),\qquad F\ne0.
$$

Karena $K[X,Y]$ merupakan domain faktorisasi unik, suatu faktor prima dari
$F$ juga termasuk dalam ideal tersebut. Jadi, kita dapat mengandaikan bahwa
$F$ merupakan polinom prima. Kita mempunyai inklusi

$$
B\subseteq\overline B
=V(\operatorname{Id}(B))
\subseteq V(F).
$$

Untuk $H\in\operatorname{Id}(B)$, himpunan

$$
V(\operatorname{Id}(B))\subseteq V(H)\cap V(F)
$$

takhingga. Menurut Teorema 4.8, $H$ dan $F$ harus mempunyai faktor
takkonstan yang sama. Karena $F$ prima, $H$ harus merupakan kelipatan $F$.
Dengan demikian,

$$
\operatorname{Id}(B)=(F).
$$

$\square$

### Contoh: mengeliminasi parameter {#br-ak-2025-2026-l06-ex-01}

Pertimbangkan kurva yang diberikan oleh parametrisasi

$$
x=t^2+t+1,
\qquad
y=2t^2+3t-1.
$$

Kita mempunyai

$$
x-1=t^2+t,
\qquad
y+1=2t^2+3t.
$$

Pengurangan sederhana menghasilkan

$$
(y+1)-2(x-1)=3t-2t=t.
$$

Jadi,

$$
x-1=t^2+t=(y-2x+3)^2+(y-2x+3).
$$

Setelah dikembangkan, persamaan kurvanya adalah

$$
y^2+4x^2-4xy-15x+7y+13=0.
$$

### Contoh: kurva dengan satu perpotongan-diri {#br-ak-2025-2026-l06-ex-02}

![Kurva kubik dengan titik ganda](authority/assets/Cubic_with_double_point.svg)

Pertimbangkan pemetaan $\mathbb A_K^1\to\mathbb A_K^2$ yang diberikan oleh

$$
P=t^2-1,
\qquad
Q=t^3-t=t(t^2-1).
$$

Kedua nilai parameter $t=\pm1$ menghasilkan titik $(0,0)$. Untuk setiap nilai
lain $t\ne\pm1$, kita dapat menulis

$$
t=\frac{t^3-t}{t^2-1}=\frac{Q(t)}{P(t)}.
$$

Jadi, parameter $t$ dapat direkonstruksi dari nilai citranya, yang berarti
pemetaan tersebut injektif di luar kedua nilai itu. Dengan demikian, kurva
citranya berpotongan dengan dirinya sendiri tepat di satu tempat.

Untuk menentukan persamaan kurva, tuliskan $x=t^2-1$ dan $y=t^3-t$. Maka

$$
t^2=x+1
$$

dan

$$
\begin{aligned}
y^2
&=t^2(t^2-1)^2\\
&=t^2x^2\\
&=(x+1)x^2\\
&=x^3+x^2.
\end{aligned}
$$

Jadi, polinom yang mendeskripsikan kurva tersebut adalah

$$
Y^2-X^3-X^2.
$$

## Parametrisasi rasional {#br-ak-2025-2026-l06-s02}

Pertimbangkan fungsi rasional

$$
Y=\frac{P}{Q},
\qquad
P,Q\in K[T].
$$

Fungsi ini segera memberikan bentuk parametrisasi baru melalui pemetaan

$$
\begin{aligned}
\mathbb A_K^1\supseteq D(Q)&\longrightarrow\mathbb A_K^2,\\
t&\longmapsto\left(t,\frac{P(t)}{Q(t)}\right).
\end{aligned}
$$

Di sini $D(Q)$ adalah domain definisi pemetaan, yakni

$$
D(Q)=\mathbb A_K^1\setminus V(Q),
$$

yang terdiri atas semua titik tempat polinom penyebut $Q$ tidak bernilai nol.
Pemetaan ini jelas mencakup semua titik grafik fungsi rasional, sehingga,
seperti parametrisasi polinomial, ia memberikan deskripsi eksplisit bagi
kurva. Oleh karena itu, untuk mendeskripsikan kurva, wajar pula mengizinkan
parametrisasi yang fungsi-fungsi komponennya rasional.

### Definisi: parametrisasi rasional {#br-ak-2025-2026-l06-def-01}

Dua fungsi rasional

$$
\varphi_1=\frac{P_1}{Q_1},
\qquad
\varphi_2=\frac{P_2}{Q_2},
$$

dengan

$$
P_1,P_2,Q_1,Q_2\in K[T],
\qquad
Q_1,Q_2\ne0,
$$

disebut suatu *parametrisasi rasional* bagi kurva aljabar

$$
C=V(F),
\qquad
F\in K[X,Y]\text{ takkonstan},
$$

apabila

$$
F(\varphi_1(T),\varphi_2(T))=0
$$

dan pasangan $(\varphi_1,\varphi_2)$ tidak konstan.

Kesamaan dalam definisi ini dipahami dalam lapangan fungsi rasional $K(T)$. Jika
$K$ takhingga, hal ini ekuivalen dengan kesamaan tersebut berlaku untuk semua
$t\in K$ tempat polinom-polinom penyebut terdefinisi.

### Definisi: kurva rasional {#br-ak-2025-2026-l06-def-02}

Kurva aljabar bidang

$$
C=V(F)
$$

disebut *rasional* apabila kurva itu tak tereduksi dan mempunyai suatu
parametrisasi rasional.

Contoh sederhana berikut menunjukkan bahwa fungsi rasional dapat
memarameterkan lebih banyak kurva daripada polinom. Namun, perlu disebutkan
sejak sekarang bahwa perbedaan ini menghilang lagi dalam konteks geometri
projektif.

### Contoh: hiperbola {#br-ak-2025-2026-l06-ex-03}

Pertimbangkan hiperbola

$$
H=V(XY-1).
$$

Kita menyatakan bahwa hiperbola ini tidak mempunyai parametrisasi
polinomial. Bagi dua polinom $P(t)$ dan $Q(t)$, syarat agar citranya selalu
berada pada $H$ adalah

$$
P(t)Q(t)=1
\quad\text{untuk setiap }t\in\mathbb A_K^1,
$$

atau bahwa $P(t)Q(t)=1$ dalam gelanggang polinomial $K[t]$. Kedua syarat ini
ekuivalen jika lapangan tersebut takhingga; untuk lapangan berhingga, identitas
kedualah syarat yang tepat. Identitas itu berarti $P$ dan $Q$ saling invers,
sehingga keduanya satuan. Satuan-satuan dalam gelanggang polinomial hanyalah
konstanta taknol. Jadi, kedua polinom itu konstan, pemetaan yang didefinisikan
olehnya konstan, dan tidak ada parametrisasi polinomial.

Sebaliknya,

$$
\begin{aligned}
\mathbb A_K^1\setminus\{0\}&\longrightarrow\mathbb A_K^2,\\
t&\longmapsto\left(t,\frac1t\right)
\end{aligned}
$$

merupakan parametrisasi rasional bagi hiperbola tersebut.

Kita ingin menunjukkan bahwa citra pemetaan rasional takkonstan selalu
memenuhi suatu persamaan aljabar, sehingga selalu memberikan parametrisasi
rasional bagi suatu kurva aljabar. Dalam kasus polinomial, persamaan aljabar
diperoleh melalui argumen pencacahan: jumlah monomial dalam dua variabel
bertumbuh lebih cepat bersama derajat daripada jumlah monomial dalam satu
variabel. Kita akan memakai argumen serupa bersama sebuah trik tambahan,
yaitu *homogenisasi*. Trik ini membuat suatu situasi takhomogen menjadi
homogen dengan menambahkan satu variabel lagi. Di sini proses tersebut kita
gunakan secara aljabar murni, tetapi di baliknya terdapat hubungan antara
geometri afin dan geometri projektif.

### Definisi: homogenisasi {#br-ak-2025-2026-l06-def-03}

Misalkan

$$
F\in K[X_1,\ldots,X_n],
\qquad
F\ne0,
$$

suatu polinom dengan dekomposisi homogen

$$
F=\sum_{i=0}^dF_i,
$$

dan misalkan $Z$ suatu variabel tambahan. Polinom homogen berderajat $d$

$$
\widehat F
=\sum_{i=0}^dF_iZ^{d-i}
\in K[X_1,\ldots,X_n,Z]
$$

disebut *homogenisasi* dari $F$.

Polinom asal dapat diperoleh kembali dari homogenisasinya dengan menetapkan
variabel tambahan $Z=1$. Proses ini disebut *dehomogenisasi*.

### Lema: relasi homogen bagi tiga polinom homogen {#br-ak-2025-2026-l06-lem-01}

Misalkan

$$
P_1,P_2,P_3\in K[S,T]
$$

tiga polinom homogen dengan derajat yang sama. Maka terdapat polinom homogen

$$
F\in K[X,Y,Z],
\qquad
F\ne0,
$$

dengan

$$
F(P_1,P_2,P_3)=0.
$$

#### Bukti {#br-ak-2025-2026-l06-lem-01-proof}

Pernyataan ini mengikuti dari argumen pencacahan yang serupa dengan bukti
Teorema 6.1; lihat Soal 6.7. $\square$

### Contoh: suatu relasi monomial {#br-ak-2025-2026-l06-ex-04}

Pertimbangkan pemetaan

$$
(S,T)\longmapsto(S^2,T^2,ST)=(X,Y,Z),
$$

yang diberikan oleh polinom-polinom homogen, bahkan oleh monomial. Relasi
aljabar bagi citranya mudah ditemukan:

$$
Z^2=(ST)^2=S^2T^2=XY.
$$

Jadi, citra pemetaan tersebut terletak pada $V(Z^2-XY)$. Lihat juga Soal
6.29.

### Teorema: citra pemetaan rasional memenuhi persamaan aljabar {#br-ak-2025-2026-l06-thm-02}

Misalkan diberikan dua fungsi rasional

$$
\varphi_1=\frac{P_1}{Q_1},
\qquad
\varphi_2=\frac{P_2}{Q_2},
$$

dengan $P_1,P_2,Q_1,Q_2\in K[T]$, $Q_1,Q_2\ne0$, yang tidak keduanya
konstan. Maka terdapat polinom takkonstan $F\in K[X,Y]$ dengan

$$
F(\varphi_1(T),\varphi_2(T))=0.
$$

Dengan demikian, $\varphi_1$ dan $\varphi_2$ mendefinisikan suatu
parametrisasi rasional.

#### Bukti {#br-ak-2025-2026-l06-thm-02-proof}

Dengan memakai penyebut bersama, kita dapat mengandaikan bahwa pemetaan
rasional tersebut diberikan oleh

$$
\varphi_1=\frac{P_1}{Q},
\qquad
\varphi_2=\frac{P_2}{Q},
$$

dengan $P_1,P_2,Q\in K[T]$ dan $Q\ne0$. Misalkan

$$
H'_1,H'_2,H'_3\in K[T,S]
$$

homogenisasi ketiga polinom itu dengan variabel baru $S$, dan misalkan $e$
derajat terbesar di antara ketiganya. Tetapkan

$$
H_i=S^{e-\deg(H'_i)}H'_i.
$$

Polinom $H_1,H_2,H_3$ semuanya berderajat $e$, sedangkan dehomogenisasinya
pada $S=1$ tetap $P_1,P_2,Q$. Menurut Lema 6.8, terdapat polinom homogen

$$
F\in K[U,V,W],
\qquad
F\ne0,
$$

berderajat $d$ dalam $U,V,W$, dengan

$$
F(H_1,H_2,H_3)=0.
$$

Sekarang tinjau

$$
\frac1{W^d}F(U,V,W)
=F\left(\frac UW,\frac VW,\frac WW\right),
$$

yang merupakan polinom dalam kedua fungsi rasional $U/W$ dan $V/W$.
Homogenitas $F$ sangat penting bagi langkah ini. Substitusi ketiga polinom
homogen menghasilkan

$$
0=F\left(\frac{H_1}{H_3},\frac{H_2}{H_3},1\right).
$$

Ini merupakan kesamaan dalam lapangan hasil bagi $K[S,T]$. Dengan menetapkan
$S=1$, yaitu melakukan dehomogenisasi, dan menuliskan

$$
G(X,Y)=F(X,Y,1),
$$

kita memperoleh polinom taknol $G\in K[X,Y]$ dengan

$$
0=G\left(\frac{P_1}{Q},\frac{P_2}{Q}\right),
$$

yang merupakan suatu persamaan bagi kedua fungsi rasional asal. $\square$

![Sissoid Diokles (hitam pada gambar) dapat diparameterkan secara rasional](authority/assets/Dioklova_kisoida.png)

### Catatan: parametrisasi terdiferensial lokal {#br-ak-2025-2026-l06-rem-01}

Kita dapat melangkah lebih jauh dan bertanya apakah ada cara lain untuk
mendeskripsikan kurva aljabar

$$
C=V(F)
$$

melalui suatu pemetaan $\varphi:K\to K^2$ jika $\varphi$ boleh berasal dari
kelas fungsi yang lebih luas. Salah satu hasil penting adalah teorema fungsi
implisit. Untuk $K=\mathbb R$ atau $K=\mathbb C$, teorema ini menyatakan bahwa
jika kedua turunan parsial $F$ tidak sekaligus nol di suatu titik kurva, maka
terdapat suatu pemetaan terdiferensial takhingga kali, bahkan analitik, yang
mendeskripsikan kurva dalam suatu lingkungan terbuka kecil di sekitar titik
tersebut. Versi aljabar dari teorema fungsi implisit muncul kembali dalam
pendekatan deret pangkat yang akan kita bahas kemudian.
