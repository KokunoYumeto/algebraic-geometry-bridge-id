---
title: "Solusi Publik Lembar Kerja 7"
stable_id: br-ak-2025-2026-w07-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-07/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: 8dfcc09854b47d83eaf9179462449a0a1fa307a3a72e5d1f252cfce35858e0e1
public_solution_count: 3
license: CC BY-SA 4.0
translation_status: complete
---

# Solusi Publik Lembar Kerja 7 {#br-ak-2025-2026-w07-solutions}

Sumber hanya menyediakan solusi publik bagi Soal 7.10, 7.11, dan 7.22 pada
batas revisi yang dibekukan. Tidak ada solusi tambahan yang dibuat untuk edisi
ini.

## Solusi Soal 7.10 {#br-ak-2025-2026-w07-sol-10}

<!-- upstream_solution_revid: 1113188 -->

Persamaan

$$
4X^2+3Y^2=9
$$

ekuivalen dengan

$$
\left(\frac{2}{3}X\right)^2
+\left(\frac{1}{\sqrt{3}}Y\right)^2
=1
=\widetilde X^2+\widetilde Y^2.
$$

Jadi, atas $\mathbb R$,

$$
\widetilde X=\frac{2}{3}X,
\qquad
\widetilde Y=\frac{1}{\sqrt{3}}Y
$$

merupakan transformasi afin-linear.

Untuk kasus $\mathbb Q$, kita mengambil

$$
\widetilde X=aX+bY+c
$$

dan

$$
\widetilde Y=dX+eY+f
$$

dengan koefisien $a,b,c,d,e,f\in\mathbb Q$. Diperoleh

$$
\begin{aligned}
\widetilde X^2+\widetilde Y^2
&=(aX+bY+c)^2+(dX+eY+f)^2\\
&=(a^2+d^2)X^2+(b^2+e^2)Y^2
  +2(ab+de)XY+H(X,Y),
\end{aligned}
$$

dengan $H\in\mathbb Q[X,Y]$ dan $\deg H\le 1$.

> **Catatan edisi:** Sumber langsung membandingkan koefisien pada langkah ini.
> Justifikasinya adalah bahwa ekuivalensi afin memetakan pusat unik kedua
> kuadrik ke pusat unik, sehingga $c=f=0$. Setelah persamaan penarikbalikan
> dinormalkan agar suku konstannya $-1$, kedua polinom kuadratik yang
> mendefinisikan lokus yang sama berimpit; perbandingan koefisien $Y^2$
> kemudian memberikan persamaan berikut.

Dengan justifikasi tersebut, harus berlaku

$$
b^2+e^2=\frac{1}{3}
\quad\Longleftrightarrow\quad
3(b^2+e^2)=1.
$$

Dengan mengalikan kedua ruas dengan penyebut bersama, persamaan tersebut dapat
dibawa ke bentuk

$$
3(r^2+s^2)=t^2,
$$

dengan $r,s,t\in\mathbb Z$. Kita akan menunjukkan bahwa persamaan ini tidak
mempunyai solusi bilangan bulat taktrivial. Karena ruas kiri persamaan merupakan
kelipatan $3$, diperoleh $3\mid t$, sehingga $9\mid t^2$. Akibatnya,
$3\mid(r^2+s^2)$. Dalam $\mathbb Z/(3)$, persamaan $r^2+s^2=0$ berlaku tepat
ketika $r=0$ dan $s=0$. Oleh karena itu, $9\mid(r^2+s^2)$ dan kedua ruas
persamaan dapat dibagi dengan $9$. Sekarang kita menetapkan

$$
r'=\frac r3,
\qquad
s'=\frac s3,
\qquad
t'=\frac t3.
$$

Argumen penurunan tak hingga menyelesaikan pembuktian.

[Kembali ke Soal 7.10](#br-ak-2025-2026-w07-ex-10).

## Solusi Soal 7.11 {#br-ak-2025-2026-w07-sol-11}

<!-- upstream_solution_revid: 1112940 -->

Jarak dari $P=(x,y)$ ke titik asal adalah $\sqrt{x^2+y^2}$, sedangkan jarak
tegak lurus ke garis $x=1$ adalah $\lvert x-1\rvert$. Proporsionalitas tersebut
dinyatakan oleh

$$
\frac{d(P,F)}{d(P,G)}=\sqrt e.
$$

Jadi,

$$
\sqrt{x^2+y^2}
=\sqrt e\,\lvert x-1\rvert
\quad\text{atau, secara ekuivalen,}\quad
x^2+y^2=e(x-1)^2.
$$

Dengan demikian,

$$
(1-e)x^2+y^2+2ex-e=0
$$

merupakan persamaan aljabar bagi suatu kurva yang memuat semua titik yang
memenuhi syarat tersebut. Jika $e=1$, persamaan itu menjadi

$$
y^2+2ex-e=0
\quad\text{atau}\quad
x=-\frac{1}{2e}y^2+\frac{1}{2},
$$

sehingga dalam kasus ini kurvanya merupakan sebuah parabola. Selanjutnya,
misalkan $e\ne1$. Persamaan umum dapat diubah menjadi

$$
x^2+\frac{1}{1-e}y^2+\frac{2e}{1-e}x-\frac{e}{1-e}=0
$$

dan, dengan melengkapkan kuadrat, dibawa ke bentuk

$$
\left(x+\frac{e}{1-e}\right)^2
+\frac{1}{1-e}y^2
-\frac{e^2}{(1-e)^2}
-\frac{e}{1-e}
=0.
$$

Kita menuliskannya sebagai

$$
\begin{aligned}
\left(x+\frac{e}{1-e}\right)^2+\frac{1}{1-e}y^2
&=\frac{e^2}{(1-e)^2}+\frac{e}{1-e}\\
&=\frac{e^2-e^2+e}{(1-e)^2}\\
&=:c>0.
\end{aligned}
$$

Faktor $\frac{1}{1-e}$ bernilai positif untuk $e<1$ dan negatif untuk $e>1$.
Dalam kasus pertama, setelah perubahan koordinat diperoleh persamaan berbentuk

$$
\widetilde x^2+\widetilde y^2=c,
$$

yaitu sebuah elips. Dalam kasus kedua, diperoleh

$$
\widetilde x^2-\widetilde y^2=c,
$$

yaitu sebuah hiperbola.

[Kembali ke Soal 7.11](#br-ak-2025-2026-w07-ex-11).

## Solusi Soal 7.22 {#br-ak-2025-2026-w07-sol-22}

<!-- upstream_solution_revid: 1095499 -->

Kita menggeser titik $(1,2)$ ke titik asal dengan memperkenalkan variabel baru

$$
U=X-1
$$

dan

$$
V=Y-2.
$$

Persamaan tersebut kemudian menjadi

$$
\begin{aligned}
X^2+Y^2-5
&=(U+1)^2+(V+2)^2-5\\
&=U^2+V^2+2U+4V.
\end{aligned}
$$

Tuliskan kurva hasil pergeseran itu sebagai

$$
\widetilde C=V\left(U^2+V^2+2U+4V\right).
$$

Rumus-rumus parametrisasi dengan garis $V=1$ menghasilkan

$$
P_1=-t(2t+4),
$$

$$
P_2=-(2t+4),
$$

dan

$$
Q=t^2+1.
$$

Jadi, parametrisasi diberikan oleh

$$
\mathbb Q\longrightarrow \widetilde C\subset\mathbb A^2_{\mathbb Q},
\qquad
t\longmapsto
\left(
\frac{-t(2t+4)}{t^2+1},
\frac{-(2t+4)}{t^2+1}
\right).
$$

> **Catatan edisi:** Sumber menamai kurva antara pada koordinat $(U,V)$ dengan
> simbol $C$ yang sama seperti kurva semula. Simbol $\widetilde C$ dipakai di
> sini agar langkah pergeseran dan rumus setelah digeser kembali tidak
> tertukar.

Dari sini diperoleh parametrisasi bagi persamaan semula:

$$
X
=-t\frac{2t+4}{t^2+1}+1
=\frac{-t^2-4t+1}{t^2+1}
$$

dan

$$
Y
=\frac{-(2t+4)}{t^2+1}+2
=\frac{2t^2-2t-2}{t^2+1}.
$$

[Kembali ke Soal 7.22](#br-ak-2025-2026-w07-ex-22).
