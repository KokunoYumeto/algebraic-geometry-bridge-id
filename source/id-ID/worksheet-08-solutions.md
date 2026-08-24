---
title: "Solusi Publik Lembar Kerja 8"
stable_id: br-ak-2025-2026-w08-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-08/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: 000ee8da757d92c581bb49a4d0e5a23b06393d5af3028f2f97c979fabcf4553d
public_solution_count: 2
license: CC BY-SA 4.0
translation_status: complete
---

# Solusi Publik Lembar Kerja 8 {#br-ak-2025-2026-w08-solutions}

Sumber hanya menyediakan solusi publik bagi Soal 8.9 dan 8.17 pada batas
revisi yang dibekukan. Tidak ada solusi tambahan yang dibuat untuk edisi ini.

## Solusi Soal 8.9 {#br-ak-2025-2026-w08-sol-09}

<!-- upstream_solution_revid: 1096407 -->

Dengan

$$
P_1=(x_1,1)
\qquad\text{dan}\qquad
P_2=(x_2,y_2),
$$

kita memperoleh kedua syarat

$$
x_2^2+y_2^2=1
$$

dan

$$
(x_2-x_1)^2+(y_2-1)^2=4.
$$

Kita kurangkan persamaan pertama dari persamaan kedua dan memperoleh

$$
\begin{aligned}
0
&=(x_2-x_1)^2+(y_2-1)^2-4-(x_2^2+y_2^2-1)\\
&=x_2^2+x_1^2-2x_1x_2+y_2^2-2y_2+1-4-x_2^2-y_2^2+1\\
&=x_1^2-2x_1x_2-2y_2-2.
\end{aligned}
$$

Persamaan ini, bersama dengan persamaan lingkaran satuan, ekuivalen dengan
sistem semula. Dari persamaan kedua yang baru tersebut, $y_2$ dapat
dieliminasikan melalui

$$
y_2=\frac12x_1^2-x_1x_2-1.
$$

Jadi, sistem dapat dideskripsikan hanya dengan variabel $x_1$ dan $x_2$,
yaitu sebagai himpunan nol polinom

$$
\begin{aligned}
x_2^2+y_2^2-1
&=x_2^2+\left(\frac12x_1^2-x_1x_2-1\right)^2-1\\
&=x_2^2+\frac14x_1^4+x_1^2x_2^2+1-x_1^3x_2-x_1^2+2x_1x_2-1\\
&=\frac14x_1^4-x_1^3x_2+x_1^2x_2^2-x_1^2+2x_1x_2+x_2^2.
\end{aligned}
$$

[Kembali ke Soal 8.9](#br-ak-2025-2026-w08-ex-09).

## Solusi Soal 8.17 {#br-ak-2025-2026-w08-sol-17}

<!-- upstream_solution_revid: 1096408 -->

1. Misalkan

   $$
   P_1=(x_1,y_1)
   $$

   adalah titik pada lingkaran dan

   $$
   P_2=(x_2,0)
   $$

   adalah titik pada sumbu $x$. Persamaan-persamaannya ialah

   $$
   x_1^2+(y_1-2)^2=1
   $$

   dan

   $$
   (x_1-x_2)^2+y_1^2=d^2.
   $$

2. Tuliskan

   $$
   f_1=x_1^2+(y_1-2)^2-1
      =x_1^2+y_1^2-4y_1+3
   $$

   dan

   $$
   f_2=(x_1-x_2)^2+y_1^2-d^2
      =x_1^2+x_2^2-2x_1x_2+y_1^2-d^2.
   $$

   Matriks Jacobi terhadap variabel $(x_1,x_2,y_1)$ adalah

   $$
   \begin{pmatrix}
   2x_1 & 0 & 2y_1-4\\
   2x_1-2x_2 & 2x_2-2x_1 & 2y_1
   \end{pmatrix}.
   $$

   Kita harus memeriksa, bergantung pada $d$, pada titik mana pemetaan linear
   $\mathbb R^3\to\mathbb R^2$ yang diberikan oleh matriks ini surjektif,
   yakni mempunyai rank $2$. Rank-nya bukan $2$ tepat ketika semua kolom
   bergantung linear, atau secara ekuivalen ketika semua minor $2\times2$
   sama dengan nol. Setelah faktor bersama $4$ dikeluarkan, ketiga polinomnya
   adalah

   $$
   x_1(x_2-x_1),
   \qquad
   (y_1-2)(x_2-x_1),
   \qquad
   x_1y_1-(x_1-x_2)(y_1-2).
   $$

   Jika $x_1\ne0$, maka harus berlaku $x_1=x_2$ dan $y_1=0$. Namun, ini bukan
   titik sistem. Jadi, harus berlaku $x_1=0$. Jika $x_2\ne0$, maka harus
   berlaku $y_1=2$, tetapi ini tidak memenuhi persamaan pertama sistem. Maka
   $x_2=0$. Selanjutnya, persamaan-persamaan sistem memberikan

   $$
   (y_1-2)^2=1
   \qquad\text{dan}\qquad
   y_1^2=d^2.
   $$

   Persamaan pertama memaksa $y_1=1$ atau $y_1=3$, sehingga $d=1$ atau $d=3$.
   Dengan demikian, tepat untuk $d\ne1,3$ sistem ini reguler di setiap titik.

3. Untuk $d=1$, berdasarkan perhitungan di atas, $(0,0,1)$ adalah satu-satunya
   titik kritis; bahkan titik ini merupakan satu-satunya titik sistem, yang
   menjelaskan singularitas tersebut.

   Untuk $d=3$, titik $(0,0,3)$ adalah satu-satunya titik kritis sistem. Di
   sana terdapat titik perpotongan karena batang dapat bergerak dalam empat
   arah: kedua koordinat $(x_1,x_2)$ ke arah positif, keduanya ke arah negatif,
   atau dalam dua arah campuran.

[Kembali ke Soal 8.17](#br-ak-2025-2026-w08-ex-17).

---

**Navigasi sumber:** [Lembar Kerja 8](#br-ak-2025-2026-w08) - [Kuliah 8](#br-ak-2025-2026-l08)
