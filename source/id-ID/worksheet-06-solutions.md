---
title: "Solusi Publik Lembar Kerja 6"
stable_id: br-ak-2025-2026-w06-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-06/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: 24ad08b1cbd215a1142d66d4297a5ce177b610aaaadd4329d464b1febb8c4c2c
public_solution_count: 9
license: CC BY-SA 4.0
translation_status: complete
---

# Solusi Publik Lembar Kerja 6 {#br-ak-2025-2026-w06-solutions}

Sumber hanya menyediakan solusi publik bagi Soal 6.3, 6.4, 6.8, 6.9,
6.17, 6.18, 6.21, 6.22, dan 6.25 pada batas revisi yang dibekukan. Tidak ada
solusi tambahan yang dibuat untuk edisi ini.

## Solusi Soal 6.3 {#br-ak-2025-2026-w06-sol-03}

<!-- upstream_solution_revid: 1112350 -->

Kita menghitung beberapa monomial pertama dalam $X$ dan $Y$:

$$
X^0Y^0=1,
$$

$$
X=t^2+t,
$$

$$
Y=t^3,
$$

$$
XY=t^5+t^4,
$$

$$
X^2=t^4+2t^3+t^2,
$$

$$
Y^2=t^6,
$$

dan

$$
X^3=t^6+3t^5+3t^4+t^3.
$$

Kita mencari relasi taktrivial di antara polinom-polinom ini dalam $K[t]$.
Karena

$$
X^3-Y^2-Y=3t^5+3t^4=3XY,
$$

suatu relasi aljabar bagi kurva citra adalah

$$
X^3-Y^2-Y-3XY=0.
$$

Sebagai contoh, titik $(1,0)$ di bidang afin tidak terletak pada kurva citra,
sebab

$$
1^3-0^2-0-3\cdot1\cdot0=1\ne0.
$$

[Kembali ke Soal 6.3](#br-ak-2025-2026-w06-ex-03).

## Solusi Soal 6.4 {#br-ak-2025-2026-w06-sol-04}

<!-- upstream_solution_revid: 958133 -->

Kita menghitung beberapa monomial dalam $X$ dan $Y$:

$$
X^0Y^0=1,
$$

$$
X=t^2+1,
$$

$$
X^2=t^4+2t^2+1,
$$

$$
X^3=t^6+3t^4+3t^2+1,
$$

dan

$$
Y^2=t^6-2t^4+t^2.
$$

Ini adalah lima polinom yang hanya memuat pangkat $t^0,t^2,t^4,t^6$,
sehingga polinom-polinom tersebut harus bergantung linear. Salah satu relasi
linearnya adalah

$$
-Y^2+X^3-5X^2+8X-4=0.
$$

[Kembali ke Soal 6.4](#br-ak-2025-2026-w06-ex-04).

## Solusi Soal 6.8 {#br-ak-2025-2026-w06-sol-08}

<!-- upstream_solution_revid: 1057120 -->

Polinom semacam itu tidak ada. Andaikan

$$
F=\sum_{\alpha+\beta+\gamma=d}
a_{(\alpha,\beta,\gamma)}X^\alpha Y^\beta Z^\gamma
$$

suatu polinom homogen berderajat $d$. Persamaan yang diminta akan menjadi

$$
F(S,T,ST)
=\sum_{\alpha+\beta+\gamma=d}
a_{(\alpha,\beta,\gamma)}
S^{\alpha+\gamma}T^{\beta+\gamma}
=0.
$$

Andaikan dua monomial dalam jumlah itu sama:

$$
S^{\alpha_1+\gamma_1}T^{\beta_1+\gamma_1}
=S^{\alpha_2+\gamma_2}T^{\beta_2+\gamma_2}.
$$

Maka

$$
\alpha_1+\gamma_1=\alpha_2+\gamma_2
$$

dan

$$
\beta_1+\gamma_1=\beta_2+\gamma_2.
$$

Dengan menjumlahkan kedua persamaan, diperoleh

$$
\alpha_1+\beta_1+2\gamma_1
=\alpha_2+\beta_2+2\gamma_2.
$$

Karena

$$
\alpha_1+\beta_1+\gamma_1
=\alpha_2+\beta_2+\gamma_2=d,
$$

berlaku $\gamma_1=\gamma_2$, lalu $\alpha_1=\alpha_2$ dan
$\beta_1=\beta_2$. Jadi, semua monomial
$S^{\alpha+\gamma}T^{\beta+\gamma}$ dalam jumlah di atas berbeda berpasangan.
Agar $F(S,T,ST)=0$, setiap koefisien
$a_{(\alpha,\beta,\gamma)}$ harus nol. Dengan demikian, $F=0$, bertentangan
dengan syarat soal.

[Kembali ke Soal 6.8](#br-ak-2025-2026-w06-ex-08).

## Solusi Soal 6.9 {#br-ak-2025-2026-w06-sol-09}

<!-- upstream_solution_revid: 1112838 -->

Kita memakai homogenisasi berderajat sama

$$
H_1=T^2+S^2,
\qquad
H_2=S(T+S)=ST+S^2,
\qquad
H_3=ST.
$$

Dari ketiganya diperoleh enam monomial berderajat $4$ terhadap $S,T$.
Karena hanya terdapat lima monomial berderajat $4$ dalam dua variabel, harus
ada ketergantungan linear. Secara eksplisit,

$$
F_1=H_1^2=T^4+2S^2T^2+S^4,
$$

$$
F_2=H_2^2=S^2T^2+2S^3T+S^4,
$$

$$
F_3=H_3^2=S^2T^2,
$$

$$
F_4=H_1H_2=ST^3+S^2T^2+S^3T+S^4,
$$

$$
F_5=H_1H_3=ST^3+S^3T,
$$

dan

$$
F_6=H_2H_3=S^2T^2+S^3T.
$$

Karena $T^4$ hanya muncul dalam $F_1$, relasi linear harus dapat dicari di
antara $F_2,F_3,F_4,F_5,F_6$. Kita mempunyai

$$
F_2-F_4+F_5-2F_6=-2S^2T^2.
$$

Jadi,

$$
F_2+2F_3-F_4+F_5-2F_6=0.
$$

Dengan demikian,

$$
F(U,V,W)=V^2+2W^2-UV+UW-2VW
$$

merupakan polinom homogen berderajat $2$ yang bernilai nol setelah
$U,V,W$ masing-masing diganti dengan $H_1,H_2,H_3$. Pembagian oleh $W^2$
memberikan

$$
\left(\frac VW\right)^2+2
-\frac UW\frac VW+\frac UW-2\frac VW=0.
$$

Setelah $H_1,H_2,H_3$ disubstitusikan dan kemudian $S=1$ ditetapkan, rasio
$U/W$ dan $V/W$ menjadi kedua fungsi rasional semula. Jadi, suatu polinom
pelenyap adalah

$$
Y^2-XY+X-2Y+2.
$$

Sebagai pemeriksaan langsung,

$$
\begin{aligned}
&\left(\frac{t+1}{t}\right)^2
-\frac{t^2+1}{t}\frac{t+1}{t}
+\frac{t^2+1}{t}
-2\frac{t+1}{t}+2\\
&=\frac{t^2+2t+1-(t^3+t^2+t+1)
+t^3+t-2t^2-2t+2t^2}{t^2}\\
&=0.
\end{aligned}
$$

[Kembali ke Soal 6.9](#br-ak-2025-2026-w06-ex-09).

## Solusi Soal 6.17 {#br-ak-2025-2026-w06-sol-17}

<!-- upstream_solution_revid: 1096769 -->

1. Dari

   $$
   (x,y,z,w)
   =\bigl(p^2,p(1-p),(1-p)p,(1-p)^2\bigr)
   =\bigl(p^2,p-p^2,p-p^2,p^2-2p+1\bigr),
   $$

   langsung diperoleh

   $$
   p=p^2+(p-p^2)=x+y.
   $$

   Jadi, variabel masukan dapat direkonstruksi dari polinom-polinom
   komponen, yang membuktikan keinjektifan.

2. Jelas bahwa $y=z$, yang memberikan persamaan pertama dan memungkinkan
   eliminasi $z$. Dengan memakai

   $$
   u=p=x+y,
   $$

   kita memperoleh

   $$
   y=u-u^2
   $$

   dan

   $$
   w=u^2-2u+1.
   $$

   Jadi, citra dideskripsikan secara lengkap oleh ketiga persamaan

   $$
   y-z=0,
   $$

   $$
   y-(x+y)+(x+y)^2=0,
   $$

   dan

   $$
   w-(x+y)^2+2(x+y)-1=0.
   $$

[Kembali ke Soal 6.17](#br-ak-2025-2026-w06-ex-17).

## Solusi Soal 6.18 {#br-ak-2025-2026-w06-sol-18}

<!-- upstream_solution_revid: 1024155 -->

1. Dari

   $$
   (x,y,z,w)
   =\bigl(pq,p(1-q),(1-p)q,(1-p)(1-q)\bigr)
   =\bigl(pq,p-pq,q-pq,pq-p-q+1\bigr),
   $$

   langsung diperoleh

   $$
   p=pq+(p-pq)=x+y
   $$

   dan

   $$
   q=pq+(q-pq)=x+z.
   $$

   Jadi, kedua variabel masukan dapat direkonstruksi, yang membuktikan
   keinjektifan.

2. Dengan memakai

   $$
   u=p=x+y,
   \qquad
   v=q=x+z,
   $$

   kita memperoleh

   $$
   x=uv
   $$

   dan

   $$
   w=uv-u-v+1.
   $$

   Jadi, citra dideskripsikan secara lengkap oleh kedua persamaan

   $$
   x-(x+y)(x+z)=0
   $$

   dan

   $$
   w-(x+y)(x+z)+(x+y)+(x+z)-1=0.
   $$

[Kembali ke Soal 6.18](#br-ak-2025-2026-w06-ex-18).

## Solusi Soal 6.21 {#br-ak-2025-2026-w06-sol-21}

<!-- upstream_solution_revid: 1067921 -->

Misalkan $d$ derajat bersama $G$ dan $H$, dan tuliskan

$$
G=\sum_{\nu\in\mathbb N^n}
a_\nu X^\nu Z^{d-|\nu|}
$$

serta

$$
H=\sum_{\nu\in\mathbb N^n}
b_\nu X^\nu Z^{d-|\nu|}.
$$

Dehomogenisasinya adalah

$$
\sum_{\nu\in\mathbb N^n}a_\nu X^\nu
\qquad\text{dan}\qquad
\sum_{\nu\in\mathbb N^n}b_\nu X^\nu,
$$

yang sama menurut asumsi. Jadi, $a_\nu=b_\nu$ bagi setiap $\nu$, dan karena
itu kedua polinom asal juga sama.

[Kembali ke Soal 6.21](#br-ak-2025-2026-w06-ex-21).

## Solusi Soal 6.22 {#br-ak-2025-2026-w06-sol-22}

<!-- upstream_solution_revid: 1096509 -->

Misalkan

$$
F=F_d+F_{d-1}+\cdots+F_1+F_0
$$

dan

$$
G=G_e+G_{e-1}+\cdots+G_1+G_0
$$

polinom berderajat $d$ dan $e$, ditulis menurut dekomposisi homogennya.
Homogenisasinya adalah

$$
\widehat F
=F_d+F_{d-1}Z+\cdots+F_1Z^{d-1}+F_0Z^d
$$

dan

$$
\widehat G
=G_e+G_{e-1}Z+\cdots+G_1Z^{e-1}+G_0Z^e.
$$

Hasil kalinya berbentuk

$$
\widehat F\,\widehat G
=\sum_{k=0}^{d+e}P_kZ^{d+e-k},
$$

dengan

$$
P_k=\sum_{i=0}^dF_iG_{k-i},
$$

di mana komponen dengan indeks di luar rentang dipahami bernilai nol.
Di sisi lain,

$$
FG=\sum_{k=0}^{d+e}H_k
$$

mempunyai komponen homogen

$$
H_k=\sum_{i=0}^dF_iG_{k-i}.
$$

Karena itu,

$$
\begin{aligned}
\widehat{FG}
&=\sum_{k=0}^{d+e}H_kZ^{d+e-k}\\
&=\sum_{k=0}^{d+e}
\left(\sum_{i=0}^dF_iG_{k-i}\right)Z^{d+e-k}\\
&=\sum_{k=0}^{d+e}P_kZ^{d+e-k}\\
&=\widehat F\,\widehat G.
\end{aligned}
$$

[Kembali ke Soal 6.22](#br-ak-2025-2026-w06-ex-22).

## Solusi Soal 6.25 {#br-ak-2025-2026-w06-sol-25}

<!-- upstream_solution_revid: 1089645 -->

Pembagian dengan sisa dalam kasus homogen memberikan

$$
\begin{aligned}
&X^4+9X^3Y+7X^2Y^2+XY^3+8Y^4\\
&\quad=(X^3+5X^2Y)(X+4Y)
-13X^2Y^2+XY^3+8Y^4.
\end{aligned}
$$

Jadi,

$$
Q=X+4Y
$$

dan

$$
R=-13X^2Y^2+XY^3+8Y^4.
$$

[Kembali ke Soal 6.25](#br-ak-2025-2026-w06-ex-25).
