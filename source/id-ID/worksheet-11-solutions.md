---
title: "Solusi Publik Lembar Kerja 11"
stable_id: br-ak-2025-2026-w11-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-11/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: 6298bafd7656e4653b504706b437e89de7faa92a75fac10c31d51ad9644a20cf
public_solution_count: 2
upstream_solution_revisions: "Soal 11.6=1094883; Soal 11.7=1112854"
solution_ex06_xml_sha256: 51f80c3d46d2a7fd2637618a6e762f0ec0398a6010a0e0e9733796277b2e652d
solution_ex07_xml_sha256: aaa033e15eaf2c7115bd7f6c301b8646a96d1be86fc046da40e77ad21bca97c9
license: "CC BY-SA 4.0"
translation_status: complete
---

# Solusi Publik Lembar Kerja 11 {#br-ak-2025-2026-w11-solutions}

Sumber hanya menyediakan solusi publik untuk Soal 11.6 dan 11.7 pada batas
revisi yang dibekukan. Tidak ada solusi tambahan yang dibuat untuk edisi ini.

<!-- upstream_solution: Hilbertscher Nullstellensatz/Ebene algebraische Kurven/R und C/1/Aufgabe/Lösung; pageid=94452; revid=1094883 -->
<!-- upstream_solution_revid: 1094883 -->

## Solusi Soal 11.6 {#br-ak-2025-2026-w11-sol-06}

1. Satu-satunya titik real pada $V(X^2+Y^2)$ adalah titik asal $(0,0)$, dan
   titik ini berada pada $V(X^2-Y^3)$. Jadi,

   $$
   V(X^2+Y^2)\subseteq V(X^2-Y^3)
   \subseteq\mathbb A_{\mathbb R}^2.
   $$

2. Inklusi yang bersesuaian tidak berlaku di atas bilangan kompleks. Sebagai
   contoh,

   $$
   (1,\mathrm i)\in V(X^2+Y^2),
   $$

   tetapi karena $1\ne\mathrm i^3$, titik itu tidak berada pada
   $V(X^2-Y^3)$.

3. Andaikan $X^2-Y^3$ termasuk dalam radikal $(X^2+Y^2)$ di
   $\mathbb R[X,Y]$. Setelah perluasan skalar, hal yang sama akan langsung
   berlaku di $\mathbb C[X,Y]$. Namun, menurut butir berikut, hal itu tidak
   berlaku.

4. Dari butir (2) dan arah mudah Nullstellensatz Hilbert, diperoleh bahwa
   $X^2-Y^3$ tidak termasuk dalam radikal $(X^2+Y^2)$ di
   $\mathbb C[X,Y]$.

[Kembali ke Soal 11.6](#br-ak-2025-2026-w11-ex-06).

<!-- upstream_solution: Hilbertscher Nullstellensatz/C/Linearkombination mit Funktionen/Aufgabe/Lösung; pageid=168417; revid=1112854 -->
<!-- upstream_solution_revid: 1112854 -->

## Solusi Soal 11.7 {#br-ak-2025-2026-w11-sol-07}

Kita klaim bahwa

$$
V(f_1,\ldots,f_k)\subseteq V(f).
$$

Setelah klaim ini terbukti, Nullstellensatz Hilbert menyatakan bahwa $f$
termasuk dalam radikal $(f_1,\ldots,f_k)$.

Misalkan

$$
P=(x_1,\ldots,x_n)\in\mathbb C^n
$$

dan $P\in V(f_1,\ldots,f_k)$. Ini berarti $f_i(P)=0$ untuk setiap $i$. Maka

$$
\begin{aligned}
f(P)
&=(g_1f_1+\cdots+g_kf_k)(P)\\
&=g_1(P)f_1(P)+\cdots+g_k(P)f_k(P)\\
&=0.
\end{aligned}
$$

Jadi $P\in V(f)$, yang membuktikan klaim.

[Kembali ke Soal 11.7](#br-ak-2025-2026-w11-ex-07).
