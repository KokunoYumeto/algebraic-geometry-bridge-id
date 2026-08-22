---
title: "Solusi Publik Lembar Kerja 4"
stable_id: br-ak-2025-2026-w04-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-04/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: a6e2631e9b4156d5f32bf5f55c1a201987f9da9c41d247d51755fb8727079420
public_solution_count: 6
license: CC BY-SA 4.0
translation_status: complete
---

# Solusi Publik Lembar Kerja 4 {#br-ak-2025-2026-w04-solutions}

Sumber hanya menyediakan solusi publik bagi Soal 4.10, 4.11, 4.12, 4.14,
4.15, dan 4.17 pada batas revisi yang dibekukan. Tidak ada solusi tambahan
yang dibuat untuk edisi ini.

## Solusi Soal 4.10 {#br-ak-2025-2026-w04-sol-10}

<!-- upstream_solution_revid: 1067858 -->

Kita akan membuktikan isomorfisme

$$
K[X,Y]/(Y-F,Y-G)\cong K[X]/(F-G).
$$

Pertimbangkan homomorfisme aljabar-$K$

$$
\varphi:K[X,Y]\longrightarrow K[X]/(F-G)
$$

yang memetakan $X\mapsto X$ dan $Y\mapsto F$. Berlaku

$$
\varphi(Y-F)=F-F=0
$$

dan

$$
\varphi(Y-G)=F-G=0.
$$

Menurut teorema homomorfisme bagi gelanggang, diperoleh homomorfisme
aljabar-$K$ terinduksi

$$
\overline\varphi:
K[X,Y]/(Y-F,Y-G)\longrightarrow K[X]/(F-G).
$$

Sekarang pertimbangkan homomorfisme aljabar-$K$

$$
\psi:K[X]\longrightarrow K[X,Y]/(Y-F,Y-G)
$$

dengan $X\mapsto X$. Di gelanggang sasaran,

$$
\psi(F-G)=F-G=(Y-G)-(Y-F)=0.
$$

Karena itu diperoleh homomorfisme terinduksi

$$
\overline\psi:
K[X]/(F-G)\longrightarrow K[X,Y]/(Y-F,Y-G).
$$

Kedua komposisi $\overline\psi\circ\overline\varphi$ dan
$\overline\varphi\circ\overline\psi$ masing-masing merupakan identitas.

[Kembali ke Soal 4.10](#br-ak-2025-2026-w04-ex-10).

## Solusi Soal 4.11 {#br-ak-2025-2026-w04-sol-11}

<!-- upstream_solution_revid: 1067949 -->

1. Persamaan sebuah lingkaran berbentuk

   $$
   (X-a)^2+(Y-b)^2-c=0.
   $$

   Setelah dikembangkan, tulis

   $$
   F=X^2+Y^2+rX+sY+t
   $$

   dan, dengan cara yang sama,

   $$
   G=X^2+Y^2+\widetilde rX+\widetilde sY+\widetilde t.
   $$

   Maka

   $$
   H=F-G=(r-\widetilde r)X+(s-\widetilde s)Y
   +(t-\widetilde t).
   $$

   Karena kedua lingkaran berbeda, $H$ berderajat $1$ atau $0$. Selain itu,

   $$
   (F,G)=(F,H),
   $$

   sehingga gelanggang hasil baginya isomorfik.

2. Gunakan deskripsi pada bagian pertama:

   $$
   R=K[X,Y]/(F,H).
   $$

   Jika $H$ suatu konstanta taknol, $R$ adalah gelanggang nol. Selain itu,
   $H$ linear, sehingga salah satu variabel dapat dinyatakan dalam variabel
   lainnya; katakan

   $$
   Y=\alpha X+\beta.
   $$

   Dengan demikian,

   $$
   \begin{aligned}
   K[X,Y]/(F,H)
   &\cong K[X,Y]/(X^2+Y^2+rX+sY+t,\,Y-\alpha X-\beta)\\
   &\cong K[X]/\bigl(X^2+(\alpha X+\beta)^2+rX
     +s(\alpha X+\beta)+t\bigr)\\
   &\cong K[X]/(uX^2+vX+w).
   \end{aligned}
   $$

[Kembali ke Soal 4.11](#br-ak-2025-2026-w04-ex-11).

## Solusi Soal 4.12 {#br-ak-2025-2026-w04-sol-12}

<!-- upstream_solution_revid: 1110006 -->

Pertimbangkan homomorfisme evaluasi yang surjektif

$$
R[X]\longrightarrow R/(G_1,\ldots,G_n),
\qquad
X\longmapsto[r].
$$

Pembangkit $F_0=X-r$ dipetakan ke $0$, dan untuk $i\ge1$, pembangkit $F_i$
dipetakan ke $G_i=0$. Teorema homomorfisme memberikan homomorfisme gelanggang
surjektif

$$
\varphi:R[X]/\mathfrak a\longrightarrow R/(G_1,\ldots,G_n).
$$

Kita tinggal membuktikan bahwa homomorfisme ini injektif. Misalkan

$$
P=a_0+a_1X+\cdots+a_mX^m\in R[X]
$$

dipetakan oleh $\varphi$ ke $0$. Ini berarti

$$
P(r)=a_0+a_1r+\cdots+a_mr^m
\in(G_1,\ldots,G_n)
$$

di dalam $R$. Selanjutnya,

$$
\begin{aligned}
P-P(r)
&=\sum_{i=0}^m a_iX^i-\sum_{i=0}^m a_ir^i\\
&=\sum_{i=0}^m a_i(X^i-r^i)\\
&=\sum_{i=1}^m a_i(X^i-r^i)\\
&=\sum_{i=1}^m (X-r)H_i,
\end{aligned}
$$

sebab $X^i-r^i$ selalu habis dibagi $X-r$. Maka

$$
P-P(r)\in(X-r),
$$

dan secara keseluruhan

$$
P\in(X-r,G_1,\ldots,G_n).
$$

Untuk unsur-unsur tertentu $B_i$ juga berlaku

$$
F_i-G_i=F_i-F_i(r)=(X-r)B_i.
$$

Karena itu,

$$
\begin{aligned}
P&\in(X-r,G_1,\ldots,G_n)\\
&=(X-r,F_1,\ldots,F_n)\\
&=\mathfrak a.
\end{aligned}
$$

Jadi, $\varphi$ injektif dan merupakan isomorfisme yang diminta.

[Kembali ke Soal 4.12](#br-ak-2025-2026-w04-ex-12).

## Solusi Soal 4.14 {#br-ak-2025-2026-w04-sol-14}

<!-- upstream_solution_revid: 1075363 -->

Untuk $p=2$, pernyataan dapat diperiksa langsung. Andaikan $p\ge3$. Tulis
persamaan sebagai

$$
aX^2=-bY^2-c.
$$

Karena $a$ dan $b$ merupakan unit, teorema tentang banyaknya residu kuadrat
menunjukkan bahwa himpunan nilai di ruas kiri maupun himpunan nilai di ruas
kanan masing-masing mempunyai $(p+1)/2$ unsur. Medan $\mathbb Z/(p)$ hanya
mempunyai $p$ unsur, sehingga kedua himpunan itu tidak mungkin saling lepas.
Jadi, terdapat $d\in\mathbb Z/(p)$ yang dapat ditulis sebagai

$$
d=aX^2=-bY^2-c
$$

untuk unsur-unsur tertentu $X,Y\in\mathbb Z/(p)$. Pasangan tersebut merupakan
solusi persamaan semula.

[Kembali ke Soal 4.14](#br-ak-2025-2026-w04-ex-14).

## Solusi Soal 4.15 {#br-ak-2025-2026-w04-sol-15}

<!-- upstream_solution_revid: 1072981 -->

Mula-mula misalkan $\mathfrak a$ suatu ideal prima. Maka gelanggang hasil bagi
$R/\mathfrak a$ merupakan domain integral, sehingga mempunyai medan pecahan
$Q(R/\mathfrak a)$. Komposisi proyeksi kanonik dengan inklusi ke medan
pecahan,

$$
\varphi:R\longrightarrow Q(R/\mathfrak a),
\qquad
x\longmapsto[x],
$$

merupakan homomorfisme gelanggang ke suatu medan dengan

$$
\ker\varphi=\mathfrak a.
$$

Sebaliknya, kernel suatu homomorfisme gelanggang

$$
\varphi:R\longrightarrow K
$$

selalu merupakan ideal. Jika $ab\in\ker\varphi$, maka

$$
0=\varphi(ab)=\varphi(a)\varphi(b).
$$

Karena medan $K$ tidak mempunyai pembagi nol, berlaku $\varphi(a)=0$ atau
$\varphi(b)=0$. Ini setara dengan $a\in\ker\varphi$ atau
$b\in\ker\varphi$. Jadi, $\ker\varphi$ merupakan ideal prima.

[Kembali ke Soal 4.15](#br-ak-2025-2026-w04-ex-15).

## Solusi Soal 4.17 {#br-ak-2025-2026-w04-sol-17}

<!-- upstream_solution_revid: 485196 -->

Mula-mula misalkan $\mathfrak p$ suatu ideal prima. Khususnya,
$\mathfrak p\subsetneq R$, sehingga $R/\mathfrak p$ bukan gelanggang nol.
Andaikan $fg=0$ dalam $R/\mathfrak p$, dengan $f$ dan $g$ diwakili oleh unsur
dalam $R$. Maka $fg\in\mathfrak p$, sehingga $f\in\mathfrak p$ atau
$g\in\mathfrak p$. Dalam $R/\mathfrak p$, ini tepat berarti $f=0$ atau
$g=0$. Jadi, $R/\mathfrak p$ merupakan domain integral.

Sebaliknya, andaikan $R/\mathfrak p$ suatu domain integral. Gelanggang hasil
bagi ini bukan gelanggang nol, sehingga $\mathfrak p\ne R$. Jika
$f,g\notin\mathfrak p$, maka kelas $f$ dan $g$ keduanya tidak nol dalam
$R/\mathfrak p$. Karena gelanggang itu merupakan domain integral, hasil
kalinya tidak nol. Jadi,

$$
fg\notin\mathfrak p.
$$

Kontraposisi menyatakan bahwa $fg\in\mathfrak p$ memaksa
$f\in\mathfrak p$ atau $g\in\mathfrak p$. Maka $\mathfrak p$ merupakan ideal
prima.

[Kembali ke Soal 4.17](#br-ak-2025-2026-w04-ex-17).
