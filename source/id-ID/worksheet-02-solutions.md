---
title: "Solusi Lembar Kerja 2 — Himpunan Aljabar Afin dan Ideal"
stable_id: br-ak-2025-2026-w02-solutions
language: id-ID
upstream_solution_count: 9
upstream_solution_map: "authority/wikiversity/unit-02/ORDERED_EXERCISE_MAP.json"
license: CC BY-SA 4.0
translation_status: complete
---

# Solusi Lembar Kerja 2 {#br-ak-2025-2026-w02-solutions}

Bagian ini menerjemahkan kesembilan solusi publik yang terhubung dari Lembar
Kerja 2 pada pembekuan sumber. Nomor dan urutannya mengikuti soal sumber. Soal
yang tidak mempunyai solusi publik pada batas tersebut tidak diberi solusi
tambahan.

## Solusi Soal 2.2 {#br-ak-2025-2026-w02-sol-02}

<!-- upstream_solution_revid: 1096652 -->

Vektor arah garis tersebut ialah

$$
\begin{pmatrix}5\\-3\end{pmatrix}.
$$

Jadi, persamaan garisnya berbentuk

$$
3x+5y=c.
$$

Substitusi salah satu titik memberikan $c=2$. Dengan demikian,

$$
y=\frac{2-3x}{5}.
$$

Kita substitusikan ungkapan ini ke dalam persamaan lingkaran

$$
x^2+y^2=1
$$

dan memperoleh

$$
x^2+\left(\frac{2-3x}{5}\right)^2=1,
$$

atau

$$
x^2+\frac{4-12x+9x^2}{25}-1
=\frac{34}{25}x^2-\frac{12}{25}x-\frac{21}{25}=0.
$$

Setelah dinormalkan, persamaan itu menjadi

$$
x^2-\frac6{17}x-\frac{21}{34}=0.
$$

Karena itu,

$$
\begin{aligned}
x_{1,2}
&=\frac{\frac6{17}\pm
\sqrt{\left(\frac6{17}\right)^2+4\cdot\frac{21}{34}}}{2}\\
&=\frac{\frac6{17}\pm
\sqrt{\left(\frac6{17}\right)^2+\frac{42}{17}}}{2}\\
&=\frac{6\pm\sqrt{6^2+714}}{34}\\
&=\frac{6\pm\sqrt{750}}{34}\\
&=\frac{6\pm5\sqrt{30}}{34},
\end{aligned}
$$

dan

$$
\begin{aligned}
y_{1,2}
&=\frac{2-3x_{1,2}}5\\
&=\frac{2-3\left(\frac{6\pm5\sqrt{30}}{34}\right)}5\\
&=\frac{68-3(6\pm5\sqrt{30})}{170}\\
&=\frac{50\mp15\sqrt{30}}{170}\\
&=\frac{10\mp3\sqrt{30}}{34}.
\end{aligned}
$$

Jadi, titik-titik potongnya adalah

$$
\left(\frac{6+5\sqrt{30}}{34},\frac{10-3\sqrt{30}}{34}\right)
\quad\text{dan}\quad
\left(\frac{6-5\sqrt{30}}{34},\frac{10+3\sqrt{30}}{34}\right).
$$

[Kembali ke Soal 2.2](#br-ak-2025-2026-w02-ex-02).

## Solusi Soal 2.6 {#br-ak-2025-2026-w02-sol-06}

<!-- upstream_solution_revid: 1096317 -->

Lingkaran satuan adalah himpunan solusi persamaan

$$
x^2+y^2=1,
$$

sedangkan $K$ adalah himpunan solusi persamaan

$$
(x-1)^2+y^2=x^2-2x+1+y^2=4.
$$

Dengan mengurangkan persamaan pertama dari persamaan kedua, kita memperoleh

$$
-2x+1=3,
$$

sehingga $x=-1$. Persamaan lingkaran satuan lalu memberikan $y=0$. Jadi,
satu-satunya titik potong ialah $(-1,0)$, yang memang memenuhi kedua persamaan.

[Kembali ke Soal 2.6](#br-ak-2025-2026-w02-ex-06).

## Solusi Soal 2.7 {#br-ak-2025-2026-w02-sol-07}

<!-- upstream_solution_revid: 1096561 -->

Kita mencari solusi sistem

$$
x^2+xy+3y^2=3
$$

dan

$$
2x^2-xy+y^2=4.
$$

Jumlah kedua persamaan tersebut adalah

$$
3x^2+4y^2=7,
$$

sedangkan dua kali persamaan pertama dikurangi persamaan kedua memberikan

$$
3xy+5y^2=2.
$$

Dari persamaan terakhir,

$$
x=\frac{2-5y^2}{3y};
$$

nilai $y=0$ jelas tidak menghasilkan solusi. Substitusi ungkapan bagi $x$ ke
persamaan sebelumnya memberikan

$$
3\left(\frac{2-5y^2}{3y}\right)^2+4y^2=7.
$$

Setelah dikalikan dengan $3y^2$, kita memperoleh

$$
\begin{aligned}
0
&=(2-5y^2)^2+12y^4-21y^2\\
&=4-20y^2+25y^4+12y^4-21y^2\\
&=37y^4-41y^2+4.
\end{aligned}
$$

Ini adalah persamaan bikuadrat.

[Kembali ke Soal 2.7](#br-ak-2025-2026-w02-ex-07).

## Solusi Soal 2.8 {#br-ak-2025-2026-w02-sol-08}

<!-- upstream_solution_revid: 1096094 -->

Parabola standar diberikan oleh persamaan

$$
y=x^2,
$$

sedangkan lingkaran satuan diberikan oleh

$$
x^2+y^2=1.
$$

Titik-titik potong harus memenuhi kedua persamaan secara simultan. Dengan
mengganti $x^2$ pada persamaan kedua menggunakan persamaan pertama, kita
memperoleh

$$
y^2+y-1=0.
$$

Jadi,

$$
y=\frac{-1\pm\sqrt{1+4}}2=\frac{-1\pm\sqrt5}{2}.
$$

Tanda negatif tidak memberikan nilai $x$ real, sehingga

$$
y=\frac{-1+\sqrt5}{2},
\qquad
x=\pm\sqrt{\frac{-1+\sqrt5}{2}}.
$$

Kedua titik potongnya adalah

$$
\left(-\sqrt{\frac{-1+\sqrt5}{2}},\frac{-1+\sqrt5}{2}\right)
$$

dan

$$
\left(\sqrt{\frac{-1+\sqrt5}{2}},\frac{-1+\sqrt5}{2}\right).
$$

[Kembali ke Soal 2.8](#br-ak-2025-2026-w02-ex-08).

## Solusi Soal 2.9 {#br-ak-2025-2026-w02-sol-09}

<!-- upstream_solution_revid: 1096689 -->

1. Buat sketsa sesuai perintah soal.

2. Kita mempunyai

   $$
   \begin{aligned}
   K
   &=\{(x,y)\in\mathbb R^2\mid(y-1)^2+x^2=1\}\\
   &=\{(x,y)\in\mathbb R^2\mid y^2-2y+1+x^2=1\}\\
   &=\{(x,y)\in\mathbb R^2\mid y^2-2y+x^2=0\}.
   \end{aligned}
   $$

3. Kita mencari himpunan solusi bersama kedua persamaan

   $$
   y=x^2
   $$

   dan

   $$
   y^2-2y+x^2=0.
   $$

   Ganti $x^2$ dalam persamaan kedua dengan $y$. Kita memperoleh

   $$
   0=y^2-2y+y=y^2-y=y(y-1).
   $$

   Jadi, $y=0$ atau $y=1$. Ini memberikan tiga titik potong
   $(0,0)$, $(1,1)$, dan $(-1,1)$.

4. Persamaan lingkaran

   $$
   y^2-2y+x^2=0
   $$

   ekuivalen dengan

   $$
   y^2-2y=-x^2,
   $$

   dan dengan

   $$
   (y-1)^2=1-x^2.
   $$

   Karena itu,

   $$
   y=1\pm\sqrt{1-x^2}.
   $$

   Busur bawah lingkaran adalah grafik fungsi

   $$
   [-1,1]\longrightarrow\mathbb R,
   \qquad x\longmapsto1-\sqrt{1-x^2}.
   $$

5. Kita menyatakan bahwa pada $[-1,1]$ parabola berada di atas busur bawah
   lingkaran. Kita harus menunjukkan

   $$
   x^2\ge1-\sqrt{1-x^2}.
   $$

   Ini ekuivalen dengan

   $$
   \sqrt{1-x^2}\ge1-x^2.
   $$

   Karena kedua ruas taknegatif pada interval tersebut, hal ini ekuivalen
   dengan

   $$
   1-x^2\ge(1-x^2)^2=1+x^4-2x^2.
   $$

   Persamaan terakhir ekuivalen dengan $x^4-x^2\le0$, dan kemudian dengan
   $x^2-1\le0$, yang benar karena $x\in[-1,1]$.

[Kembali ke Soal 2.9](#br-ak-2025-2026-w02-ex-09).

## Solusi Soal 2.11 {#br-ak-2025-2026-w02-sol-11}

<!-- upstream_solution_revid: 1094978 -->

1. Misalkan

   $$
   A=\begin{pmatrix}X_1&X_2\\X_3&X_4\end{pmatrix}
   \qquad\text{dan}\qquad
   B=\begin{pmatrix}Y_1&Y_2\\Y_3&Y_4\end{pmatrix}.
   $$

   Maka

   $$
   AB=
   \begin{pmatrix}
   X_1Y_1+X_2Y_3&X_1Y_2+X_2Y_4\\
   X_3Y_1+X_4Y_3&X_3Y_2+X_4Y_4
   \end{pmatrix}
   $$

   dan

   $$
   BA=
   \begin{pmatrix}
   X_1Y_1+X_3Y_2&X_2Y_1+X_4Y_2\\
   X_1Y_3+X_3Y_4&X_2Y_3+X_4Y_4
   \end{pmatrix}.
   $$

   Kedua matriks hasil kali ini sama tepat ketika keempat entri yang
   bersesuaian sama, yaitu ketika

   $$
   X_1Y_1+X_2Y_3=X_1Y_1+X_3Y_2,
   $$

   $$
   X_1Y_2+X_2Y_4=X_2Y_1+X_4Y_2,
   $$

   $$
   X_3Y_1+X_4Y_3=X_1Y_3+X_3Y_4,
   $$

   dan

   $$
   X_3Y_2+X_4Y_4=X_2Y_3+X_4Y_4.
   $$

   Karena itu, himpunannya adalah varietas afin. Persamaan pertama dan keempat
   saling ekuivalen dan keduanya ekuivalen dengan

   $$
   X_2Y_3=X_3Y_2.
   $$

   Jadi, matriks-matriks yang saling komutatif dideskripsikan oleh sistem

   $$
   X_2Y_3=X_3Y_2,
   $$

   $$
   X_1Y_2+X_2Y_4=X_2Y_1+X_4Y_2,
   $$

   $$
   X_3Y_1+X_4Y_3=X_1Y_3+X_3Y_4.
   $$

2. Matriks identitas $E_2$ komutatif dengan setiap matriks. Jadi, $(A,E_2)$
   adalah salah satu praimaj dari $A$.

3. Kita mencari matriks

   $$
   B=\begin{pmatrix}Y_1&Y_2\\Y_3&Y_4\end{pmatrix}
   $$

   yang memenuhi sistem di atas untuk

   $$
   A=\begin{pmatrix}X_1&X_2\\X_3&X_4\end{pmatrix}
   =\begin{pmatrix}1&1\\0&0\end{pmatrix}.
   $$

   Syarat-syaratnya menjadi

   $$
   Y_3=0,
   \qquad
   Y_2+Y_4=Y_1,
   \qquad
   0=Y_3,
   $$

   dan syarat ketiga dapat dibuang. Jadi, praimaj matriks tersebut adalah

   $$
   \left\{
   \left(
   \begin{pmatrix}1&1\\0&0\end{pmatrix},
   \begin{pmatrix}Y_2+Y_4&Y_2\\0&Y_4\end{pmatrix}
   \right)
   \;\middle|\;Y_2,Y_4\in K
   \right\}.
   $$

[Kembali ke Soal 2.11](#br-ak-2025-2026-w02-ex-11).

## Solusi Soal 2.15 {#br-ak-2025-2026-w02-sol-15}

<!-- upstream_solution_revid: 1089351 -->

Pertama-tama kita buktikan $\mathfrak b\subseteq\mathfrak a$ dengan menunjukkan
bahwa setiap pembangkit $\mathfrak b$ bernilai $0$ dalam gelanggang faktor
oleh $\mathfrak a$. Dalam gelanggang itu,

$$
\begin{aligned}
X^2+Y^2
&=(2Z^2-1)^2+4Z^2W^2\\
&=(2Z^2-1)^2+4Z^2(1-Z^2)\\
&=4Z^4-4Z^2+1+4Z^2-4Z^4\\
&=1.
\end{aligned}
$$

Selain itu,

$$
\begin{aligned}
YW
&=2ZW^2\\
&=2Z(1-Z^2)\\
&=Z(2-2Z^2)\\
&=Z(1-2Z^2+1)\\
&=Z(1-X),
\end{aligned}
$$

dan

$$
\begin{aligned}
W(1+X)
&=W(2Z^2)\\
&=2WZ^2\\
&=ZY.
\end{aligned}
$$

Inklusi $\mathfrak c\subseteq\mathfrak b$ jelas karena satu pembangkit
dihilangkan.

Terakhir, kita buktikan $\mathfrak a\subseteq\mathfrak c$ dengan menunjukkan
bahwa pembangkit-pembangkit $\mathfrak a$ bernilai $0$ dalam gelanggang hasil
bagi oleh $\mathfrak c$. Dalam gelanggang itu berlaku

$$
ZX=Z-YW
\qquad\text{dan}\qquad
WX=YZ-W.
$$

Karena itu,

$$
\begin{aligned}
X
&=X\cdot1\\
&=X(Z^2+W^2)\\
&=Z^2-ZYW+YZW-W^2\\
&=Z^2-W^2\\
&=2Z^2-1,
\end{aligned}
$$

dan

$$
\begin{aligned}
Y
&=Y\cdot1\\
&=Y(Z^2+W^2)\\
&=WXZ+WZ+ZW-ZXW\\
&=2ZW.
\end{aligned}
$$

[Kembali ke Soal 2.15](#br-ak-2025-2026-w02-ex-15).

## Solusi Soal 2.16 {#br-ak-2025-2026-w02-sol-16}

<!-- upstream_solution_revid: 1112335 -->

1. Jelas bahwa $(1,1)$ adalah suatu akar $F$.

2. Kita mempunyai

   $$
   \begin{aligned}
   F\cdot(X^2+Y^2+1)
   ={}&(X^4Y^2+X^2Y^4-3X^2Y^2+1)(X^2+Y^2+1)\\
   ={}&X^6Y^2+X^4Y^4-3X^4Y^2+X^2
   +X^4Y^4+X^2Y^6-3X^2Y^4+Y^2\\
   &+X^4Y^2+X^2Y^4-3X^2Y^2+1\\
   ={}&2X^4Y^4+X^6Y^2+X^2Y^6-2X^4Y^2-2X^2Y^4
   -3X^2Y^2+X^2+Y^2+1.
   \end{aligned}
   $$

   Untuk ruas lainnya,

   $$
   (X^2Y-Y)^2+(XY^2-X)^2+(X^2Y^2-1)^2
   +\frac14(XY^3-X^3Y)^2
   +\frac34(XY^3+X^3Y-2XY)^2,
   $$

   kita hitung koefisien setiap monom. Hanya derajat genap yang muncul dan
   derajat tertingginya $8$. Pada derajat itu hanya tiga suku terakhir yang
   berkontribusi, dan hanya monom $X^6Y^2$, $X^4Y^4$, dan $X^2Y^6$ yang muncul:

   $$
   X^6Y^2:\quad\frac14+\frac34=1,
   $$

   $$
   X^4Y^4:\quad1+\frac14(-2)+\frac34(2)=2,
   $$

   $$
   X^2Y^6:\quad\frac14+\frac34=1.
   $$

   Pada derajat $6$, hanya $X^4Y^2$ dan $X^2Y^4$ yang muncul:

   $$
   X^4Y^2:\quad1+\frac34(-4)=-2,
   $$

   $$
   X^2Y^4:\quad1+\frac34(-4)=-2.
   $$

   Pada derajat $4$, hanya $X^2Y^2$ yang muncul:

   $$
   X^2Y^2:\quad-2-2-2+\frac34(4)=-3.
   $$

   Pada derajat $2$, koefisien $X^2$ dan $Y^2$ masing-masing adalah $1$.
   Pada derajat $0$, koefisien $1$ juga $1$. Jadi, kedua ruas identik.

3. Dengan membagi identitas pada bagian (2) oleh $X^2+Y^2+1$ dalam lapangan hasil
   bagi $K[X,Y]$, kita memperoleh

   $$
   \begin{aligned}
   F=\frac{1}{X^2+Y^2+1}\Big(& (X^2Y-Y)^2+(XY^2-X)^2
   +(X^2Y^2-1)^2\\
   &+\frac14(XY^3-X^3Y)^2
   +\frac34(XY^3+X^3Y-2XY)^2\Big).
   \end{aligned}
   $$

   Karena $X^2+Y^2+1$ tidak mempunyai akar real, identitas ini juga berlaku
   sebagai identitas fungsional bagi fungsi-fungsi $\mathbb R^2\to\mathbb R$.
   Kuadrat tidak pernah negatif dan koefisien semua kuadrat yang terlibat
   positif. Jadi, fungsi tersebut taknegatif di setiap titik.

[Kembali ke Soal 2.16](#br-ak-2025-2026-w02-ex-16).

## Solusi Soal 2.20 {#br-ak-2025-2026-w02-sol-20}

<!-- upstream_solution_revid: 1096251 -->

Untuk membuktikan inklusi $\subseteq$, ambil $f\in(I+J)^n$. Karena hasil kali
ideal terdiri atas semua jumlah hasil kali, kita dapat menulis

$$
f=f_1+f_2+\cdots+f_k,
$$

dengan

$$
f_\ell=c_{\ell1}c_{\ell2}\cdots c_{\ell n},
$$

di mana $c_{\ell r}\in I+J$. Selanjutnya,

$$
c_{\ell r}=a_{\ell r}+b_{\ell r}
$$

dengan $a_{\ell r}\in I$ dan $b_{\ell r}\in J$. Jadi,

$$
f_\ell=(a_{\ell1}+b_{\ell1})(a_{\ell2}+b_{\ell2})
\cdots(a_{\ell n}+b_{\ell n}).
$$

Jika hasil kali ini dijabarkan secara distributif, kita memperoleh jumlah
hasil-hasil kali yang masing-masing mempunyai $n$ faktor: $s$ faktor berasal
dari $I$ dan $n-s$ faktor berasal dari $J$. Karena itu, setiap suku berada pada
ruas kanan; demikian pula setiap $f_\ell$ dan akhirnya $f$.

Untuk membuktikan inklusi $\supseteq$, cukup ditunjukkan

$$
I^sJ^{n-s}\subseteq(I+J)^n
$$

bagi setiap $s$. Karena $I,J\subseteq I+J$, langsung diperoleh

$$
I^sJ^{n-s}
\subseteq(I+J)^s(I+J)^{n-s}
=(I+J)^n.
$$

[Kembali ke Soal 2.20](#br-ak-2025-2026-w02-ex-20).
