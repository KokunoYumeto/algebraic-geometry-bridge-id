---
title: "Solusi Lembar Kerja 1 — Kurva Aljabar"
stable_id: br-ak-2025-2026-w01-solutions
language: id-ID
upstream_solution_count: 7
upstream_solution_map: "authority/wikiversity/worksheet-01-solutions/ORDERED_EXERCISE_MAP.json"
license: CC BY-SA 4.0
translation_status: complete
---

# Solusi Lembar Kerja 1 {#br-ak-2025-2026-w01-solutions}

Bagian ini menerjemahkan ketujuh solusi publik yang terhubung dari Lembar
Kerja 1. Nomor dan urutannya mengikuti soal sumber. Soal yang tidak mempunyai
solusi publik pada revisi sumber yang dibekukan tidak diberi solusi tambahan.

## Solusi Soal 1.4 {#br-ak-2025-2026-w01-sol-04}

<!-- upstream_solution_revid: 1094618 -->

1. $(5,3)$ adalah suatu solusi bilangan bulat.

2. Kita mempunyai

   $$
   \begin{aligned}
   \left(\frac{383}{1000}\right)^2
   -\left(\frac{129}{100}\right)^3+2
   &=\frac{146\,689}{1\,000\,000}
     -\frac{2\,146\,689}{1\,000\,000}+2\\
   &=\frac{146\,689-2\,146\,689}{1\,000\,000}+2\\
   &=\frac{-2\,000\,000}{1\,000\,000}+2\\
   &=-2+2\\
   &=0.
   \end{aligned}
   $$

[Kembali ke Soal 1.4](#br-ak-2025-2026-w01-ex-04).

## Solusi Soal 1.5 {#br-ak-2025-2026-w01-sol-05}

<!-- upstream_solution_revid: 1096326 -->

Kita meninjau irisan kurva dengan garis $V(X-Y)$, yakni dengan syarat tambahan
$X=Y$. Dengan menyubstitusikan $Y=X$ ke persamaan kurva, kita memperoleh

$$
X^3-X^3+4X^2-2X^2+X+3=2X^2+X+3=0.
$$

Rumus kuadrat memberikan

$$
X=-\frac14\pm\sqrt{-\frac{23}{16}}
  =-\frac14\pm\frac{\sqrt{23}}4i.
$$

Karena itu,

$$
\left(\frac{-1+\sqrt{23}\,i}{4},
      \frac{-1+\sqrt{23}\,i}{4}\right)
$$

adalah sebuah titik pada kurva.

[Kembali ke Soal 1.5](#br-ak-2025-2026-w01-ex-05).

## Solusi Soal 1.12 {#br-ak-2025-2026-w01-sol-12}

<!-- upstream_solution_revid: 1094741 -->

Kita pilih garis

$$
G=V(Y+1).
$$

Titik-titik irisan $C\cap G$ dapat dihitung dengan menyubstitusikan persamaan
$Y=-1$, yang berlaku pada $G$, ke persamaan kurva. Kita memperoleh

$$
0=X^3+(-1)^3+1=X^3.
$$

Satu-satunya solusi ialah $X=0$. Jadi, $(0,-1)$ adalah satu-satunya titik
irisan $G$ dan $C$.

[Kembali ke Soal 1.12](#br-ak-2025-2026-w01-ex-12).

## Solusi Soal 1.13 {#br-ak-2025-2026-w01-sol-13}

<!-- upstream_solution_revid: 1096436 -->

Setiap garis pada bidang dideskripsikan oleh persamaan

$$
ax+by=c,
$$

dengan $a$ dan $b$ tidak sekaligus nol. Jika garis itu melalui titik $(1,1)$,
maka $a+b=c$.

Jika $b=0$, garis tersebut diberikan oleh $x=1$ dan mempunyai titik irisan lain
$(1,-1)$ dengan kurva. Karena itu, sekarang misalkan $b\ne0$. Persamaan garis
dapat diselesaikan terhadap $y$ sehingga berbentuk

$$
y=rx+s,
\qquad s=1-r.
$$

Pada garis ini, persamaan kurva menjadi

$$
\begin{aligned}
0
&=y^2-x^3\\
&=(rx+(1-r))^2-x^3\\
&=-x^3+r^2x^2+2r(1-r)x+(1-r)^2.
\end{aligned}
$$

Karena $x=1$ adalah salah satu akarnya, kita dapat mengeluarkan faktor $x-1$:

$$
-x^3+r^2x^2+2r(1-r)x+(1-r)^2
=(x-1)\bigl(-x^2-(1-r^2)x-(1-r)^2\bigr).
$$

Setelah dikalikan dengan $-1$, faktor kuadratik di sebelah kanan merupakan
polinom monik berderajat $2$, sehingga mempunyai akar-akar di $\mathbb C$.
Kita harus menunjukkan bahwa sekurang-kurangnya salah satu akar tambahan itu
bukan $1$. Nilai faktor kuadratik yang ditampilkan di atas pada $x=1$ adalah

$$
-1-(1-r^2)-(1-r)^2=2r-3.
$$

Jika $r\ne\frac32$, maka $1$ bukan akar faktor kuadratik tersebut. Tinggal
kasus $r=\frac32$. Dalam kasus ini,

$$
x^2+(1-r^2)x+(1-r)^2
=x^2-\frac54x+\frac14
=(x-1)\left(x-\frac14\right),
$$

sehingga terdapat akar lain, yaitu $x=\frac14$. Jadi, setiap garis melalui
$(1,1)$ memotong parabola Neil di sekurang-kurangnya satu titik lain.

[Kembali ke Soal 1.13](#br-ak-2025-2026-w01-ex-13).

## Solusi Soal 1.14 {#br-ak-2025-2026-w01-sol-14}

<!-- upstream_solution_revid: 1096438 -->

Kita substitusikan $y^2=x^3$ ke persamaan lingkaran dan memperoleh

$$
x^3+x^2-1=0.
$$

Pada $x=1$ polinom ini bernilai $1$, sedangkan pada $x=0{,}5$ nilainya negatif.
Menurut teorema nilai antara, polinom tersebut mempunyai sebuah akar $x_0$
dalam interval $[0{,}5,1]$. Karena $x_0^3$ positif, akar kuadrat real

$$
y_0=\sqrt{x_0^3}
$$

ada, dan $(x_0,y_0)$ merupakan titik potong real.

Untuk menghampiri $x_0$ secara numerik, kita hitung

$$
(0{,}7)^3+(0{,}7)^2-1
<0{,}49+0{,}49-1<0
$$

dan

$$
\begin{aligned}
(0{,}8)^3+(0{,}8)^2-1
&=0{,}64\cdot0{,}8+0{,}64-1\\
&>0{,}48+0{,}64-1>0.
\end{aligned}
$$

Jadi, ada titik potong yang koordinat $x$-nya berada dalam interval
$[0{,}7,0{,}8]$.

[Kembali ke Soal 1.14](#br-ak-2025-2026-w01-ex-14).

## Solusi Soal 1.20 {#br-ak-2025-2026-w01-sol-20}

<!-- upstream_solution_revid: 1089682 -->

Misalkan $a\in R$ suatu unsur satuan. Ada $b\in R$ dengan $ab=1$, dan
identitas yang sama juga berlaku dalam gelanggang polinomial. Jadi,

$$
R^\times\subseteq R[X]^\times.
$$

Sebaliknya, misalkan

$$
P=\sum_{i=0}^d a_iX^i,
\qquad a_d\ne0,
$$

suatu unsur satuan dalam $R[X]$. Maka terdapat polinom

$$
Q=\sum_{j=0}^e b_jX^j,
\qquad b_e\ne0,
$$

dengan $PQ=1$. Karena $R$ suatu daerah integral, $a_db_e\ne0$, dan suku
berderajat tertinggi dalam hasil kali itu adalah

$$
a_db_eX^{d+e}+\text{suku-suku berderajat lebih rendah}.
$$

Karena $PQ=1$, kita harus mempunyai $d+e=0$ dan $a_db_e=1$. Jadi, $P$ adalah
suatu unsur satuan konstan. Dengan demikian, unsur-unsur satuan dalam $R[X]$
tepat sama dengan unsur-unsur satuan dalam $R$.

[Kembali ke Soal 1.20](#br-ak-2025-2026-w01-ex-20).

## Solusi Soal 1.21 {#br-ak-2025-2026-w01-sol-21}

<!-- upstream_solution_revid: 1054755 -->

Misalkan $K$ tertutup secara aljabar dan $F\in K[X]$ takkonstan. Kita buktikan
dengan induksi pada $n=\deg F$ bahwa $F$ terurai menjadi faktor-faktor linear.

Untuk $n=1$, kita mempunyai $F=a_1X+a_0$, sehingga $F$ sendiri sudah merupakan
satu faktor linear. Misalkan setiap polinom $G\in K[X]$ berderajat $n-1$
terurai menjadi faktor-faktor linear. Karena $K$ tertutup secara aljabar, $F$
mempunyai suatu akar $x_0$. Karena itu, kita dapat menulis

$$
F=G(X-x_0)
$$

untuk suatu $G\in K[X]$ berderajat $n-1$. Fakta tentang derajat ini mengikuti
langsung dari kenyataan bahwa setiap medan juga merupakan daerah integral dan
dari sedikit penyesuaian terhadap bukti pada Soal 8. Menurut hipotesis induksi,
$G$ terurai menjadi faktor-faktor linear; karena itu $G(X-x_0)$ juga demikian.
Jadi, setiap polinom takkonstan $F\in K[X]$ terurai menjadi faktor-faktor linear.

Sebaliknya, jika setiap polinom takkonstan terurai menjadi faktor-faktor linear,
setiap polinom tersebut mempunyai akar yang direpresentasikan oleh salah satu
faktor linearnya. Maka $K$ tertutup secara aljabar.

[Kembali ke Soal 1.21](#br-ak-2025-2026-w01-ex-21).
