---
title: "Solusi Publik Lembar Kerja 5"
stable_id: br-ak-2025-2026-w05-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-05/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: d7b9b302ea2a57199d9ff7940f6a8440d50abdc7e4fe1ccdfdd96f27686d84d5
public_solution_count: 4
license: CC BY-SA 4.0
translation_status: complete
---

# Solusi Publik Lembar Kerja 5 {#br-ak-2025-2026-w05-solutions}

Sumber hanya menyediakan solusi publik bagi Soal 5.3, 5.15, 5.19, dan 5.20
pada batas revisi yang dibekukan. Tidak ada solusi tambahan yang dibuat untuk
edisi ini.

## Solusi Soal 5.3 {#br-ak-2025-2026-w05-sol-03}

<!-- upstream_solution_revid: 1068012 -->

Misalkan

$$
F=\sum_{i=0}^n a_iX^iY^{n-i}.
$$

Dehomogenisasinya adalah polinom satu variabel

$$
\widetilde F=\sum_{i=0}^n a_iX^i.
$$

Karena lapangan tersebut tertutup secara aljabar, polinom ini mempunyai
faktorisasi

$$
\widetilde F=a_n\prod_{i=1}^n(X-c_i).
$$

Dengan menghomogenkan kembali, diperoleh faktorisasi

$$
F=a_n\prod_{i=1}^n(X-c_iY).
$$

**Catatan edisi:** rumus sumber menempatkan $a_n$ di dalam tanda hasil kali,
yang akan menghasilkan faktor $a_n^n$. Di sini $a_n$ ditempatkan satu kali di
luar hasil kali, sesuai faktorisasi polinom berkoefisien utama $a_n$.

[Kembali ke Soal 5.3](#br-ak-2025-2026-w05-ex-03).

## Solusi Soal 5.15 {#br-ak-2025-2026-w05-sol-15}

<!-- upstream_solution_revid: 1028148 -->

1. Pilih suatu bentuk linear yang cukup umum sehingga nilainya berbeda pada
   titik-titik yang diberikan. Dengan demikian, kita dapat mengandaikan bahwa
   koordinat telah dipilih sedemikian sehingga bagi

   $$
   P_i=(a_i,b_i),
   $$

   semua koordinat pertama $a_i$ saling berbeda. Misalkan

   $$
   F=(X-a_1)\cdots(X-a_n).
   $$

   Menurut teorema interpolasi, pilih suatu polinom satu variabel $H$ dengan

   $$
   H(a_i)=b_i
   $$

   untuk $i=1,\ldots,n$. Dengan $G=Y-H$, kita memperoleh

   $$
   M=V(F)\cap V(G),
   $$

   sehingga $M$ merupakan irisan dua kurva.

2. Ganti $F$ dengan

   $$
   F'=Y-H+F.
   $$

   Maka

   $$
   V(G)\cap V(F')=V(G)\cap V(F)=M.
   $$

   Kedua kurva tersebut merupakan grafik, sehingga tak tereduksi.

[Kembali ke Soal 5.15](#br-ak-2025-2026-w05-ex-15).

## Solusi Soal 5.19 {#br-ak-2025-2026-w05-sol-19}

<!-- upstream_solution_revid: 1096503 -->

Misalkan $K$ suatu lapangan tertutup secara aljabar. Pertimbangkan pemetaan

$$
\mathbb A_K^2\longrightarrow\mathbb A_K^1,
\qquad
(x,y)\longmapsto xy.
$$

Serat di atas titik nol adalah pasangan sumbu

$$
V(xy)=V(x)\cup V(y),
$$

yang tereduksi. Serat di atas suatu titik $\lambda\in K$ dengan
$\lambda\ne0$ adalah $V(xy-\lambda)$. Cukup dibuktikan bahwa
$xy-\lambda$ merupakan polinom prima. Hal ini mengikuti dari isomorfisme

$$
K[x,y]/(xy-\lambda)\longrightarrow K[u]_u,
\qquad
x\longmapsto u,
\qquad
y\longmapsto\lambda u^{-1},
$$

dengan pemetaan balik $u\mapsto x$. Sifat universal gelanggang faktor dan
lokalisasi memastikan bahwa pemetaan-pemetaan tersebut memang saling
berbalikan.

[Kembali ke Soal 5.19](#br-ak-2025-2026-w05-ex-19).

## Solusi Soal 5.20 {#br-ak-2025-2026-w05-sol-20}

<!-- upstream_solution_revid: 1096346 -->

1. Untuk $n=2$, karena

   $$
   (X-\lambda_1)(X-\lambda_2)
   =X^2-(\lambda_1+\lambda_2)X+\lambda_1\lambda_2,
   $$

   pemetaannya adalah

   $$
   \begin{aligned}
   \varphi:K^2&\longrightarrow K^2,\\
   (\lambda_1,\lambda_2)
   &\longmapsto(\lambda_1\lambda_2,-(\lambda_1+\lambda_2)).
   \end{aligned}
   $$

2. Untuk $n=3$, karena

   $$
   \begin{aligned}
   &(X-\lambda_1)(X-\lambda_2)(X-\lambda_3)\\
   &\quad=X^3-(\lambda_1+\lambda_2+\lambda_3)X^2
   +(\lambda_1\lambda_2+\lambda_1\lambda_3
   +\lambda_2\lambda_3)X-\lambda_1\lambda_2\lambda_3,
   \end{aligned}
   $$

   pemetaannya adalah

   $$
   \begin{aligned}
   \varphi:K^3&\longrightarrow K^3,\\
   (\lambda_1,\lambda_2,\lambda_3)
   &\longmapsto\bigl(-\lambda_1\lambda_2\lambda_3,
   \lambda_1\lambda_2+\lambda_1\lambda_3+\lambda_2\lambda_3,
   -(\lambda_1+\lambda_2+\lambda_3)\bigr).
   \end{aligned}
   $$

3. Tetapkan $n\in\mathbb N_+$ dan $k$ di antara $0$ dan $n-1$. Berdasarkan
   hukum distributif, koefisien $c_k$ dari
   $\prod_{i=1}^n(X-\lambda_i)$ adalah

   $$
   \mathord{\pm}
   \sum_{1\le i_1<i_2<\cdots<i_{n-k}\le n}
   \lambda_{i_1}\lambda_{i_2}\cdots\lambda_{i_{n-k}},
   $$

   dengan tanda yang ditentukan oleh paritas $n-k$. Jadi setiap fungsi
   komponen merupakan polinom.

4. Tupel $(\lambda_1,\ldots,\lambda_n)$ termasuk dalam serat di atas tupel
   koefisien $(c_0,\ldots,c_{n-1})$ tepat ketika

   $$
   \prod_{i=1}^n(X-\lambda_i)
   =\sum_{j=0}^{n-1}c_jX^j+X^n=P.
   $$

   Secara khusus, semua $\lambda_i$ harus merupakan akar $P$. Karena suatu
   polinom hanya mempunyai berhingga banyak akar, hanya ada berhingga banyak
   permutasi yang mungkin.

5. Serat di atas tupel $(c_0,\ldots,c_{n-1})$ kosong tepat ketika polinom

   $$
   \sum_{j=0}^{n-1}c_jX^j+X^n
   $$

   tidak terurai sepenuhnya menjadi faktor-faktor linear.

6. Banyak elemen maksimum dalam suatu serat adalah $n!$. Jika polinom yang
   diberikan oleh tupel koefisien terurai sepenuhnya, seratnya terdiri atas
   tupel-tupel akar terurut; jika tidak, seratnya kosong. Karena terdapat
   paling banyak $n$ akar, paling banyak $n!$ tupel terurut dapat dibentuk.
   Jika terdapat $n$ akar berbeda, seluruh permutasinya menghasilkan tepat
   $n!$ tupel. Sebagai contoh, tupel akar

   $$
   (1,2,3,\ldots,n)
   $$

   dipetakan ke suatu tupel koefisien yang seratnya terdiri atas semua
   permutasi tupel tersebut.

7. Jika $K$ tertutup secara aljabar, setiap polinom monik terurai menjadi
   faktor-faktor linear monik. Menurut bagian 5, setiap serat yang
   bersesuaian tidak kosong. Jadi, $\varphi$ surjektif.

[Kembali ke Soal 5.20](#br-ak-2025-2026-w05-ex-20).
