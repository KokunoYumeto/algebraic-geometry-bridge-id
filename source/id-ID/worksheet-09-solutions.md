---
title: "Solusi Publik Lembar Kerja 9"
stable_id: br-ak-2025-2026-w09-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-09/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: c906ba0b1073a162f7f55289c0f60114063d011756f1eb907bcf342336729495
public_solution_count: 3
upstream_solution_revisions: "Soal 9.6=1107958; Soal 9.13=1059490; Soal 9.18=1112817"
solution_ex06_xml_sha256: f9e6a938ce01a3bd784f5d1a68bb1c0ab1790f9f8d78baebd319ec23e949a626
solution_ex13_xml_sha256: 382b85fe25d73ac31562c00ffdddbd030784a795c80b59425855b45fbc73edc6
solution_ex18_xml_sha256: 47b1095efe3e91a251c3f77a2ddaa93a51c821e335138a16849a90150368696b
license: "CC BY-SA 4.0"
translation_status: complete
---

# Solusi Publik Lembar Kerja 9 {#br-ak-2025-2026-w09-solutions}

Sumber hanya menyediakan solusi publik untuk Soal 9.6, 9.13, dan 9.18 pada
batas revisi yang dibekukan. Tidak ada solusi tambahan yang dibuat untuk edisi
ini.

<!-- upstream_solution: Noetherscher Ring/Unterring/Aufgabe/Lösung; pageid=100296; revid=1107958 -->
<!-- upstream_solution_revid: 1107958 -->

## Solusi Soal 9.6 {#br-ak-2025-2026-w09-sol-06}

Pandang

$$
S=K[X,Y]
$$

sebagai gelanggang polinomial dalam dua variabel atas suatu lapangan $K$.
Menurut Korolari 9.7, gelanggang ini Noether. Di dalamnya, pertimbangkan
subgelanggang

$$
R=\{Xg(X,Y)+c\mid g\in K[X,Y],\ c\in K\}
$$

dan di dalamnya rantai ideal

$$
\mathfrak a_n=(X,XY,\ldots,XY^n).
$$

Untuk setiap $n\in\mathbb N$ berlaku

$$
XY^{n+1}\in\mathfrak a_{n+1}\setminus\mathfrak a_n,
$$

sehingga rantai tersebut tidak stasioner. Jadi, menurut Proposisi 9.2, $R$
bukan gelanggang Noether.

[Kembali ke Soal 9.6](#br-ak-2025-2026-w09-ex-06).

<!-- upstream_solution: Endlich erzeugte Algebra/Endliches Teilsystem/Aufgabe/Lösung; pageid=167639; revid=1059490 -->
<!-- upstream_solution_revid: 1059490 -->

## Solusi Soal 9.13 {#br-ak-2025-2026-w09-sol-13}

Kita mempunyai

$$
A=R[f_1,\ldots,f_n]\subseteq R[a_i,\ i\in I].
$$

Setiap $f_j$ dapat ditulis sebagai ekspresi polinomial dalam unsur-unsur
keluarga $a_i$, dengan koefisien dari $R$. Untuk setiap $j$, hanya hingga
banyak unsur $a_i$ yang muncul. Karena itu semua pembangkit $f_j$ berada di

$$
R[a_i,\ i\in I']
$$

untuk suatu subkeluarga berhingga $I'\subseteq I$. Maka

$$
A=R[f_1,\ldots,f_n]\subseteq R[a_i,\ i\in I']
\subseteq A,
$$

dan jadi $A=R[a_i,\ i\in I']$.

[Kembali ke Soal 9.13](#br-ak-2025-2026-w09-ex-13).

<!-- upstream_solution: Modul/Kommutativer Ring/Allgemeines Distributivgesetz/Aufgabe/Lösung; pageid=94177; revid=1112817 -->
<!-- upstream_solution_revid: 1112817 -->

## Solusi Soal 9.18 {#br-ak-2025-2026-w09-sol-18}

Kita membuktikan pernyataan dengan induksi ganda pada $k,n\geq1$. Kasus

$$
(k,n)=(1,1),\qquad(1,2),\qquad(2,1)
$$

langsung jelas atau mengikuti langsung dari aksioma-aksioma modul.

Pernyataan untuk $k=1$ dan sembarang $n$ dibuktikan dengan induksi pada
$n$, dengan kasus awal dijamin oleh pengamatan sebelumnya. Andaikan
pernyataan sudah terbukti untuk suatu $n$, dan diberikan $n+1$ vektor
$v_1,\ldots,v_n,v_{n+1}\in V$. Dengan menggunakan kasus $(1,2)$ dan
hipotesis induksi, diperoleh

$$
\begin{aligned}
s\cdot\left(\sum_{j=1}^{n+1}v_j\right)
&=s\cdot\left(\sum_{j=1}^{n}v_j+v_{n+1}\right)\\
&=s\cdot\left(\sum_{j=1}^{n}v_j\right)+sv_{n+1}\\
&=\sum_{1\leq j\leq n}s\cdot v_j+sv_{n+1}\\
&=\sum_{1\leq j\leq n+1}s\cdot v_j.
\end{aligned}
$$

Sekarang kita tinjau pernyataan untuk $k$ tetap dan $n$ sembarang. Untuk
$k=1$, pernyataan itu sudah dibuktikan. Andaikan pernyataan sudah terbukti
untuk suatu $k$ tetap. Diberikan skalar

$$
s_1,\ldots,s_k,s_{k+1}\in R
$$

dan vektor

$$
v_1,\ldots,v_n\in V.
$$

Dengan menggunakan kasus $(2,1)$, kasus $(1,n)$, dan hipotesis induksi,
diperoleh

$$
\begin{aligned}
\left(\sum_{i=1}^{k+1}s_i\right)\!\cdot
 \left(\sum_{j=1}^{n}v_j\right)
&=\left(\sum_{i=1}^{k}s_i+s_{k+1}\right)\!\cdot
 \left(\sum_{j=1}^{n}v_j\right)\\
&=\left(\sum_{i=1}^{k}s_i\right)\!\cdot
 \left(\sum_{j=1}^{n}v_j\right)
 +s_{k+1}\cdot\left(\sum_{j=1}^{n}v_j\right)\\
&=\sum_{1\leq i\leq k,\,1\leq j\leq n}s_i\cdot v_j
 +\sum_{j=1}^{n}s_{k+1}\cdot v_j\\
&=\sum_{1\leq i\leq k+1,\,1\leq j\leq n}s_i\cdot v_j.
\end{aligned}
$$

[Kembali ke Soal 9.18](#br-ak-2025-2026-w09-ex-18).
