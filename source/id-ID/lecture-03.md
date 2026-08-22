---
title: "Kuliah 3 — Topologi Zariski, Ideal Pelenyapan, dan Radikal"
stable_id: br-ak-2025-2026-l03
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 3"
upstream_pageid: 165892
upstream_revid: 1052207
upstream_timestamp: "2025-08-27T11:33:02Z"
upstream_mediawiki_sha1: 9ce92720a5f22f16453faa79345392063318ee86
source_url: "https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)/Vorlesung_3?oldid=1052207"
license: "CC BY-SA 4.0 for translated course text; media retain component licences in authority/RIGHTS-unit-03.csv"
translation_status: complete
---

# Kuliah 3: Topologi Zariski, Ideal Pelenyapan, dan Radikal {#br-ak-2025-2026-l03}

## Topologi Zariski {#br-ak-2025-2026-l03-s01}

![Oscar Zariski (1899-1986)](authority/assets/Oscar_Zariski.jpg)

Dalam Proposisi 2.8 kita telah menunjukkan bahwa subhimpunan aljabar afin dari
suatu ruang afin memenuhi aksioma-aksioma bagi himpunan tertutup suatu topologi.
Topologi ini disebut *topologi Zariski*.

### Definisi: topologi Zariski {#br-ak-2025-2026-l03-def-01}

Pada ruang afin $\mathbb A_K^n$, *topologi Zariski* adalah topologi yang
mendeklarasikan himpunan-himpunan aljabar afin sebagai himpunan tertutup.

Dengan demikian, himpunan terbuka dalam topologi Zariski adalah komplemen
himpunan aljabar afin. Untuk suatu ideal $\mathfrak a$, komplemen ini ditulis

$$
D(\mathfrak a)=\mathbb A_K^n\setminus V(\mathfrak a).
$$

Topologi Zariski sangat berbeda dari topologi-topologi lain, terutama dari
topologi yang diberikan oleh suatu metrik. Secara khusus, topologi Zariski
bukan topologi Hausdorff. Secara umum, himpunan-himpunan terbuka yang takkosong
dalam topologi Zariski sangat besar (lihat Soal 3.20), sedangkan
himpunan-himpunan tertutup—yakni himpunan aljabar afin—sangat tipis, kecuali
seluruh ruang itu sendiri.

### Contoh: topologi Zariski pada garis afin {#br-ak-2025-2026-l03-ex-01}

Topologi Zariski pada garis afin $\mathbb A_K^1$ di atas suatu medan $K$ mudah
dideskripsikan. Seluruh garis afin adalah himpunan tertutup yang diberikan oleh
$V(0)$. Semua subhimpunan tertutup lainnya diberikan oleh $V(\mathfrak a)$
dengan $\mathfrak a\ne0$. Karena $K[X]$ adalah domain ideal utama, kita bahkan
dapat menulis

$$
\mathfrak a=(f),\qquad f\ne0.
$$

Lokus nol yang bersesuaian hanya terdiri atas berhingga banyak titik.
Sebaliknya, setiap titik tunggal $P$ berkoordinat $a$ adalah satu-satunya akar
polinom linear $X-a$, sehingga

$$
\{P\}=V(X-a)
$$

tertutup dalam topologi Zariski. Kumpulan berhingga titik
$P_1,\ldots,P_k$ dengan koordinat $a_1,\ldots,a_k$ adalah lokus nol polinom

$$
(X-a_1)\cdots(X-a_k).
$$

Jadi, himpunan-himpunan tertutup Zariski pada garis afin adalah semua
subhimpunan berhingga—termasuk himpunan kosong—beserta seluruh garis afin.

![Sebuah garis di bidang](authority/assets/Lineline.jpg)

### Contoh: titik adalah tertutup {#br-ak-2025-2026-l03-ex-02}

Setiap titik

$$
P=(a_1,\ldots,a_n)\in\mathbb A_K^n
$$

tertutup dalam topologi Zariski; tepatnya,

$$
P=V(X_1-a_1,X_2-a_2,\ldots,X_n-a_n).
$$

Selain himpunan kosong dan seluruh ruang, titik-titik adalah himpunan aljabar
afin yang paling sederhana. Ideal

$$
(X_1-a_1,X_2-a_2,\ldots,X_n-a_n),
$$

yang disebut *ideal titik*, adalah ideal maksimal; lihat Soal 2.12.

![Irisan dua bidang](authority/assets/IntersectingPlanes.png)

![Irisan tiga bidang](authority/assets/Secretsharing-3-point.png)

Menurut Proposisi 2.8(3), setiap subhimpunan berhingga ruang afin tertutup dalam
topologi Zariski. Karena itu, jika $E$ suatu himpunan titik berhingga, maka
komplemennya

$$
\mathbb A_K^n\setminus E
$$

terbuka dalam topologi Zariski. Demikian pula, untuk fungsi rasional $P/Q$
dengan

$$
P,Q\in K[X_1,\ldots,X_n],\qquad Q\ne0,
$$

domain definisinya, yaitu $D(Q)$, terbuka.

## Ideal pelenyapan {#br-ak-2025-2026-l03-s02}

### Definisi: ideal pelenyapan {#br-ak-2025-2026-l03-def-02}

Misalkan $T\subseteq\mathbb A_K^n$ suatu subhimpunan. Himpunan

$$
\operatorname{Id}(T)
=\{F\in K[X_1,\ldots,X_n]\mid F(P)=0
\text{ untuk setiap }P\in T\}
$$

disebut *ideal pelenyapan* dari $T$.

Himpunan ini memang sebuah ideal. Jika $F(P)=0$ dan $G(P)=0$ untuk setiap
$P\in T$, maka hal yang sama berlaku bagi jumlah $F+G$ dan bagi setiap kelipatan
$HF$.

Jadi, kita mempunyai dua pemetaan dengan arah berlawanan: suatu subhimpunan
ruang afin dipetakan ke ideal pelenyapannya, sedangkan suatu ideal dalam
gelanggang polinomial dipetakan ke lokus nolnya. Kita ingin memahami sejauh mana
ideal dan lokus nol saling bersesuaian.

### Contoh: himpunan kosong dan seluruh ruang {#br-ak-2025-2026-l03-ex-03}

Ideal pelenyapan himpunan kosong adalah ideal satuan, sebab tidak ada titik
tempat syarat pelenyapan perlu diperiksa.

Ideal pelenyapan seluruh ruang $\mathbb A_K^n$ bergantung pada medannya. Jika
$K$ takhingga, hanya polinom nol yang lenyap di mana-mana, sehingga ideal
pelenyapannya adalah ideal nol. Pernyataan ini mengikuti dari Soal 3.18.

Sebaliknya, jika $K$ adalah medan berhingga dengan $q$ unsur, maka

$$
x^q-x=0
$$

untuk setiap $x\in K$. Karena itu, polinom $X^q-X$ lenyap di setiap titik garis
afin dan termasuk dalam ideal pelenyapan garis afin tersebut. Pada dimensi yang
lebih tinggi,

$$
\operatorname{Id}(\mathbb A_K^n)
=(X_1^q-X_1,X_2^q-X_2,\ldots,X_n^q-X_n).
$$

### Contoh: ideal pelenyapan sebuah titik {#br-ak-2025-2026-l03-ex-04}

Misalkan

$$
P=(a_1,\ldots,a_n)\in\mathbb A_K^n.
$$

Maka

$$
\operatorname{Id}(P)=(X_1-a_1,\ldots,X_n-a_n).
$$

Mula-mula, polinom linear $X_i-a_i$ jelas lenyap di $P$, sebab
$(X_i-a_i)(P)=a_i-a_i=0$. Dengan demikian, ideal yang dibangkitkan oleh
polinom-polinom tersebut termuat dalam ideal pelenyapan.

Sebaliknya, misalkan $F$ suatu polinom dengan $F(P)=0$. Tulis $F$ dalam
“variabel baru”

$$
\widetilde X_1=X_1-a_1,\ldots,
\widetilde X_n=X_n-a_n
$$

dengan mengganti $X_i$ oleh $X_i-a_i+a_i$. Dalam variabel baru itu, tulis

$$
F=\sum_\nu b_\nu\widetilde X^\nu.
$$

Polinom ini terdiri atas suku konstan $b_0$, sedangkan setiap monom lainnya
memuat sekurang-kurangnya satu variabel. Jadi, untuk polinom-polinom tertentu
$F_i$, kita dapat menulis

$$
F=F_1\widetilde X_1+\cdots+F_n\widetilde X_n+c.
$$

Karena $F(P)=c=0$, kita memperoleh

$$
F\in(\widetilde X_1,\ldots,\widetilde X_n)
=(X_1-a_1,\ldots,X_n-a_n).
$$

### Lema: inklusi subhimpunan membalik inklusi ideal pelenyapan {#br-ak-2025-2026-l03-lem-01}

Misalkan $V\subseteq W\subseteq\mathbb A_K^n$. Maka

$$
\operatorname{Id}(W)\subseteq\operatorname{Id}(V).
$$

#### Bukti {#br-ak-2025-2026-l03-lem-01-proof}

Ambil $F\in\operatorname{Id}(W)$. Dengan kata lain, $F(P)=0$ untuk setiap
$P\in W$. Karena $V\subseteq W$, khususnya $F(P)=0$ untuk setiap $P\in V$.
Jadi, $F\in\operatorname{Id}(V)$. $\square$

### Lema: hubungan antara lokus nol dan ideal pelenyapan {#br-ak-2025-2026-l03-lem-02}

Misalkan $I\subseteq K[X_1,\ldots,X_n]$ suatu ideal dan
$T\subseteq\mathbb A_K^n$ suatu subhimpunan. Pernyataan-pernyataan berikut
berlaku.

1. $T\subseteq V(\operatorname{Id}(T))$.
2. $I\subseteq\operatorname{Id}(V(I))$.
3. $V(I)=V(\operatorname{Id}(V(I)))$.
4. $\operatorname{Id}(T)=\operatorname{Id}(V(\operatorname{Id}(T)))$.

#### Bukti {#br-ak-2025-2026-l03-lem-02-proof}

Untuk (1), ambil $P\in T$. Menurut definisi, setiap polinom
$F\in\operatorname{Id}(T)$ lenyap pada $T$, sehingga
$P\in V(\operatorname{Id}(T))$.

Untuk (2), ambil $F\in I$. Polinom $F$ lenyap pada seluruh $V(I)$, sehingga
$F\in\operatorname{Id}(V(I))$.

Untuk (3), terapkan (1) pada $T=V(I)$ untuk memperoleh inklusi
$V(I)\subseteq V(\operatorname{Id}(V(I)))$. Menurut (2),
$I\subseteq\operatorname{Id}(V(I))$; penerapan $V(-)$ dan Lema 2.7 memberikan
inklusi sebaliknya.

Pernyataan (4) dibuktikan dengan cara yang sama. $\square$

### Contoh: inklusi yang tegas {#br-ak-2025-2026-l03-ex-05}

Kedua inklusi pada Lema 3.8(1) dan (2) dapat bersifat tegas. Sebagai contoh,
misalkan $T\subsetneq\mathbb A_K^1$ suatu subhimpunan takhingga yang proper;
ini mensyaratkan bahwa $K$ takhingga. Maka

$$
\operatorname{Id}(T)=0,
$$

sehingga $V(0)=\mathbb A_K^1$ benar-benar lebih besar daripada $T$.

Untuk inklusi pada (2), ambil $R=K[X]$ dan $I=(X^2)$. Maka

$$
V(I)=\{0\},\qquad \operatorname{Id}(\{0\})=(X),
$$

tetapi $X\notin(X^2)$. Contoh yang lebih ekstrem dalam
$R=\mathbb R[X,Y]$ ialah $I=(X^2+Y^2)$, dengan
$V(I)=\{(0,0)\}$. Ideal pelenyapan titik tersebut adalah $(X,Y)$.

### Lema: penutupan Zariski {#br-ak-2025-2026-l03-lem-03}

Misalkan $T\subseteq\mathbb A_K^n$. Penutupan Zariski dari $T$ adalah

$$
\overline T=V(\operatorname{Id}(T)).
$$

#### Bukti {#br-ak-2025-2026-l03-lem-03-proof}

Inklusi $T\subseteq V(\operatorname{Id}(T))$ telah dibuktikan dalam Lema
3.8(1). Karena $V(\operatorname{Id}(T))$ tertutup menurut definisi, kita
memperoleh

$$
\overline T\subseteq V(\operatorname{Id}(T)).
$$

Sebaliknya, ambil $P\in V(\operatorname{Id}(T))$ dan andaikan
$P\notin\overline T$. Maka terdapat himpunan terbuka Zariski $U$ sedemikian
rupa sehingga

$$
P\in U,
\qquad
U\cap T=\varnothing.
$$

Tuliskan $U=D(\mathfrak a)$. Syarat $P\in U$ berarti terdapat
$G\in\mathfrak a$ dengan $G(P)\ne0$. Maka

$$
P\in D(G)\subseteq U,
$$

sehingga $T\cap D(G)=\varnothing$. Jadi, $T\subseteq V(G)$ dan
$G\in\operatorname{Id}(T)$. Namun, $G(P)\ne0$ bertentangan dengan
$P\in V(\operatorname{Id}(T))$. $\square$

## Radikal {#br-ak-2025-2026-l03-s03}

### Definisi: ideal radikal {#br-ak-2025-2026-l03-def-03}

Suatu ideal $\mathfrak a$ dalam gelanggang komutatif $R$ disebut *ideal
radikal* apabila berlaku: jika $f^n\in\mathfrak a$ untuk suatu
$n\in\mathbb N$, maka sudah pasti $f\in\mathfrak a$.

### Definisi: radikal suatu ideal {#br-ak-2025-2026-l03-def-04}

Misalkan $R$ suatu gelanggang komutatif dan $\mathfrak a\subseteq R$ suatu
ideal. Himpunan

$$
\operatorname{rad}(\mathfrak a)
=\{f\in R\mid\text{terdapat }r\text{ dengan }f^r\in\mathfrak a\}
$$

disebut *radikal* dari $\mathfrak a$.

Radikal suatu ideal sendiri merupakan ideal radikal.

### Lema: radikal suatu ideal adalah ideal radikal {#br-ak-2025-2026-l03-lem-04}

Misalkan $R$ suatu gelanggang komutatif dan $\mathfrak a\subseteq R$ suatu
ideal. Maka $\operatorname{rad}(\mathfrak a)$ adalah ideal radikal.

#### Bukti {#br-ak-2025-2026-l03-lem-04-proof}

Mula-mula kita buktikan bahwa himpunan tersebut merupakan ideal. Jelas bahwa
$0$ berada dalam radikal. Jika $f\in\operatorname{rad}(\mathfrak a)$, katakan
$f^r\in\mathfrak a$, maka

$$
(af)^r=a^rf^r\in\mathfrak a,
$$

sehingga $af$ berada dalam radikal. Untuk sifat penjumlahan, misalkan
$f,g\in\operatorname{rad}(\mathfrak a)$ dengan
$f^r\in\mathfrak a$ dan $g^s\in\mathfrak a$. Maka

$$
\begin{aligned}
(f+g)^{r+s}
&=\sum_{i+j=r+s}\binom{r+s}{i}f^ig^j\\
&=\sum_{\substack{i+j=r+s\\i<r}}\binom{r+s}{i}f^ig^j
 +\sum_{\substack{i+j=r+s\\i\ge r}}\binom{r+s}{i}f^ig^j
\in\mathfrak a.
\end{aligned}
$$

Sekarang andaikan $f^k\in\operatorname{rad}(\mathfrak a)$. Maka untuk suatu
$r$ berlaku

$$
(f^k)^r=f^{kr}\in\mathfrak a,
$$

sehingga $f\in\operatorname{rad}(\mathfrak a)$. $\square$

### Lema: ideal pelenyapan adalah ideal radikal {#br-ak-2025-2026-l03-lem-05}

Misalkan $T\subseteq\mathbb A_K^n$. Maka ideal pelenyapan
$\operatorname{Id}(T)$ adalah ideal radikal.

#### Bukti {#br-ak-2025-2026-l03-lem-05-proof}

Misalkan $F\in K[X_1,\ldots,X_n]$ dan
$F^s\in\operatorname{Id}(T)$. Maka

$$
F^s(P)=0
$$

untuk setiap $P\in T$. Karena itu, $F(P)=0$ untuk setiap $P\in T$, sehingga
$F\in\operatorname{Id}(T)$. $\square$

Kelak kita akan melihat bahwa di atas medan tertutup secara aljabar, ideal
radikal dan lokus nol aljabar saling bersesuaian. Inilah isi teorema
Nullstellensatz Hilbert.

---

**Navigasi sumber:** [mata kuliah](https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)) · [Kuliah 2](#br-ak-2025-2026-l02) · [Kuliah 4 (sumber)](https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)/Vorlesung_4) · [Lembar Kerja 3](#br-ak-2025-2026-w03)
