---
title: "Solusi Publik Lembar Kerja 22"
stable_id: br-ak-2025-2026-w22-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-22/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: d4b1d1f0a08de69d6fb7da513b8bce9ebaf697d5dad51632d0db063925d05f1e
public_solution_count: 9
upstream_solution_revisions: "Soal 22.5=971273; Soal 22.6=1067646; Soal 22.9=1067974; Soal 22.10=1067981; Soal 22.12=1096085; Soal 22.14=958122; Soal 22.15=1089314; Soal 22.16=1089323; Soal 22.18=1094625"
solution_xml_sha256: "05=87338c889aad1ab68dc84d26c1d1d3e87786e3a856b2336ad88214e3fc24865d; 06=2f2912b1c2a934f58904cc198db011f2a981322f5858f95376c677cfffabca3a; 09=5d141458a1d3e0c8ee28730993263299cc7e82d7ce6a2287c4c1ee745840c1ca; 10=739b5ce54439877c6f8bced7ee413374eadb8df77f1df2f0b92180e2e5beb926; 12=7c112582720b0695d98642cb498502a99159e33fb53b718e3233a7cf10e4c5c7; 14=68bcfe6fe279f0a5f0e41a138ddaab9e29a95271f66d8591e570d0263fd93af7; 15=a09ce8c91da266cdf44ff73fbdde6710965c2b39c82531d6e473e65bfe034e82; 16=5de4d530da5eec27a612859cd8bfe4c9f714fcd0e1dd9fbdb53555532e9c9da7; 18=946fd900982637115aaf775bb264bc1a30838342f03ef5c73c0ac0376379edd8"
solution_ex09_transclusion: "proof pageid=84110; proof revid=1101009; json_sha256=6fdee6cc2b0b469aad230fc3094543e94c09bba93f3211986f7705c90e672aaa"
license: "CC BY-SA 4.0"
translation_status: complete
source_corrections: 2
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 22 {#br-ak-2025-2026-w22-solutions}

Pada batas revisi yang dibekukan, sumber hanya menyediakan solusi publik
untuk Soal 22.5, 22.6, 22.9, 22.10, 22.12, 22.14, 22.15, 22.16, dan 22.18.
Tidak ada solusi tambahan yang dibuat untuk edisi ini. Solusi Soal 22.9
mentransklusikan sebuah halaman bukti; teks di bawah menerjemahkan tubuh bukti
yang sebenarnya dari penutupan transklusi rekursif yang dibekukan.

<!-- upstream_solution: Homogenes Polynom/Partielle Ableitung/Dehomogenisierung/Aufgabe/Lösung; pageid=96914; revid=971273 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=971273 -->

## Solusi Soal 22.5 {#br-ak-2025-2026-w22-sol-05}

1. Karena kedua proses bersifat linear, cukup meninjaunya pada monom

   $$
   X_1^{\nu_1}X_2^{\nu_2}X_3^{\nu_3}\cdots X_n^{\nu_n},
   $$

   lalu mempertimbangkan keadaan ketika turunan diambil terhadap $X_1$ dan
   dehomogenisasi dilakukan terhadap $X_2$. Turunan parsialnya adalah

   $$
   \nu_1X_1^{\nu_1-1}X_2^{\nu_2}X_3^{\nu_3}\cdots X_n^{\nu_n},
   $$

   dan dehomogenisasi menghasilkan

   $$
   \nu_1X_1^{\nu_1-1}X_3^{\nu_3}\cdots X_n^{\nu_n}.
   $$

   Jika dehomogenisasi dilakukan terlebih dahulu, diperoleh

   $$
   X_1^{\nu_1}X_3^{\nu_3}\cdots X_n^{\nu_n},
   $$

   dan turunan parsialnya juga menghasilkan

   $$
   \nu_1X_1^{\nu_1-1}X_3^{\nu_3}\cdots X_n^{\nu_n}.
   $$

2. Tinjau $X_1$. Pendiferensialan terhadap $X_1$ menghasilkan $1$, yang tetap
   sama setelah dehomogenisasi. Jika dehomogenisasi terhadap $X_1$ dilakukan
   terlebih dahulu, diperoleh $1$, dan turunannya adalah $0$.

[Kembali ke Soal 22.5](#br-ak-2025-2026-w22-ex-05).

<!-- upstream_solution: Homogenes Polynom/Darstellung mit formalen partiellen Ableitungen/Aufgabe/Lösung; pageid=168373; revid=1067646 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1067646 -->

## Solusi Soal 22.6 {#br-ak-2025-2026-w22-sol-06}

Karena turunan parsial dan perkalian dengan suatu variabel bersifat linear,
cukup membuktikan pernyataan tersebut untuk sebuah monom. Jadi, misalkan

$$
H=X_1^{\nu_1}\cdot X_2^{\nu_2}\cdots X_n^{\nu_n}.
$$

Maka

$$
\begin{aligned}
X_1\frac{\partial H}{\partial X_1}+\cdots+
X_n\frac{\partial H}{\partial X_n}
&=\nu_1X_1\cdot X_1^{\nu_1-1}\cdot X_2^{\nu_2}\cdots X_n^{\nu_n} \\
&\quad+\nu_2X_2\cdot X_1^{\nu_1}\cdot X_2^{\nu_2-1}\cdots X_n^{\nu_n}
+\cdots \\
&\quad+\nu_nX_n\cdot X_1^{\nu_1}\cdot X_2^{\nu_2}\cdots X_n^{\nu_n-1} \\
&=\nu_1X_1^{\nu_1}\cdot X_2^{\nu_2}\cdots X_n^{\nu_n}
+\nu_2X_1^{\nu_1}\cdot X_2^{\nu_2}\cdots X_n^{\nu_n}
+\cdots \\
&\quad+\nu_nX_1^{\nu_1}\cdot X_2^{\nu_2}\cdots X_n^{\nu_n} \\
&=(\nu_1+\nu_2+\cdots+\nu_n)
X_1^{\nu_1}\cdot X_2^{\nu_2}\cdots X_n^{\nu_n}.
\end{aligned}
$$

Inilah pernyataan yang hendak dibuktikan, karena jumlah eksponen adalah
derajat monom tersebut.

[Kembali ke Soal 22.6](#br-ak-2025-2026-w22-ex-06).

<!-- upstream_solution: Ebene algebraische Kurve/Glatter Punkt/Liegt nur auf einer Komponente/Fakt/Beweis/Aufgabe/Lösung; pageid=168407; revid=1067974 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1067974 -->
<!-- frozen_transclusion: Ebene algebraische Kurve/Glatter Punkt/Liegt nur auf einer Komponente/Fakt/Beweis; pageid=84110; revid=1101009 -->

## Solusi Soal 22.9 {#br-ak-2025-2026-w22-sol-09}

Karena $P$ merupakan titik mulus pada kurva, tanpa mengurangi keumuman kita
dapat mengasumsikan bahwa

$$
\frac{\partial F}{\partial X}(P)\neq0.
$$

Menurut aturan hasil kali,

$$
\begin{aligned}
\frac{\partial F}{\partial X}(P)
&=\frac{\partial(F_1\cdots F_n)}{\partial X}(P) \\
&=\sum_{k=1}^n
F_1(P)\cdots F_{k-1}(P)\cdot
\frac{\partial F_k}{\partial X}(P)\cdot
F_{k+1}(P)\cdots F_n(P).
\end{aligned}
$$

Sekarang andaikan

$$
P\in C_i\cap C_j
$$

untuk $i\neq j$, yakni

$$
F_i(P)=F_j(P)=0.
$$

Setiap hasil kali dalam jumlah di atas akan mempunyai sebuah faktor nol,
sehingga

$$
\frac{\partial F}{\partial X}(P)=0,
$$

yang bertentangan dengan kemulusan $P$.

[Kembali ke Soal 22.9](#br-ak-2025-2026-w22-ex-09).

<!-- upstream_solution: Ebene algebraische Kurven/Einheitskreis/Bestimme Tangente/Aufgabe/Lösung; pageid=168408; revid=1067981 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1067981 -->

## Solusi Soal 22.10 {#br-ak-2025-2026-w22-sol-10}

Polinom yang mendeskripsikan kurva adalah

$$
X^2+Y^2-1,
$$

dan turunan-turunan parsialnya adalah $2X$ dan $2Y$. Karena diasumsikan
bahwa karakteristiknya bukan $2$, dan karena titik asal tidak terletak pada
lingkaran, kurva tersebut mulus. Di titik $(a,b)$ pada lingkaran, persamaan
garis singgungnya adalah

$$
2a(X-a)+2b(Y-b)=0.
$$

Setelah dibagi dengan $2$, persamaan ini dapat ditulis sebagai

$$
aX+bY-a^2-b^2=aX+bY-1=0.
$$

**Catatan edisi — koreksi sumber.** Sumber mencetak hanya ruas kiri kedua
ungkapan sambil menyebutnya “persamaan garis singgung”. Edisi ini memulihkan
syarat sama dengan nol yang membuatnya benar-benar sebuah persamaan.

[Kembali ke Soal 22.10](#br-ak-2025-2026-w22-ex-10).

<!-- upstream_solution: Ebene Kurve/-2x^3+3x^2y-y+2/3 \sqrt(1/3)/C/Singularitäten/Aufgabe/Lösung; pageid=21571; revid=1096085 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1096085 -->

## Solusi Soal 22.12 {#br-ak-2025-2026-w22-sol-12}

Misalkan $F$ adalah polinom yang mendeskripsikan kurva. Turunan-turunan
parsialnya adalah

$$
\frac{\partial F}{\partial X}=-6X^2+6XY
\quad\text{dan}\quad
\frac{\partial F}{\partial Y}=3X^2-1.
$$

Kita samakan kedua polinom dengan nol. Persamaan kedua memberikan
$x^2=\frac13$, sehingga

$$
x=\pm\sqrt{\frac13}.
$$

Pada persamaan pertama, kita dapat mengeluarkan faktor $6X$, yang tidak nol,
sehingga harus berlaku $x=y$. Jadi,

$$
y=\pm\sqrt{\frac13}.
$$

Untuk $x=y$, persamaan kurva menjadi

$$
x^3-x+\frac23\sqrt{\frac13}=0.
$$

Pada $x=\sqrt{\frac13}$, ruas kirinya bernilai

$$
\frac13\sqrt{\frac13}-\sqrt{\frac13}
+\frac23\sqrt{\frac13}=0,
$$

sehingga

$$
\left(\sqrt{\frac13},\sqrt{\frac13}\right)
$$

merupakan titik pada kurva. Sebaliknya, pada
$x=y=-\sqrt{\frac13}$ diperoleh

$$
-\frac13\sqrt{\frac13}+\sqrt{\frac13}
+\frac23\sqrt{\frac13}
=\frac43\sqrt{\frac13}\neq0,
$$

sehingga titik tersebut bukan titik pada kurva. Jadi, satu-satunya
singularitas kurva adalah

$$
\left(\sqrt{\frac13},\sqrt{\frac13}\right).
$$

[Kembali ke Soal 22.12](#br-ak-2025-2026-w22-ex-12).

<!-- upstream_solution: Ebene algebraische Kurve/x^3+xy^2/C/Singularitäten/Aufgabe/Lösung; pageid=21319; revid=958122 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=958122 -->

## Solusi Soal 22.14 {#br-ak-2025-2026-w22-sol-14}

Jelas bahwa

$$
X(X+\mathrm iY)(X-\mathrm iY)
$$

merupakan faktorisasi polinom tersebut menjadi faktor-faktor prima. Untuk
menentukan titik-titik singular, kita periksa turunan-turunan parsialnya:

$$
\frac{\partial F}{\partial X}=3X^2+Y^2
\quad\text{dan}\quad
\frac{\partial F}{\partial Y}=2XY.
$$

Kedua persamaan ini dipenuhi tepat ketika $(x,y)=(0,0)$. Karena titik ini
juga memenuhi persamaan kurva, titik tersebut merupakan titik singular
kurva. Polinom yang mendeskripsikan kurva sudah homogen berderajat $3$,
sehingga multiplisitasnya adalah $3$. Dengan demikian, garis-garis
singgungnya diberikan oleh

$$
V(X),\qquad V(X+\mathrm iY),\qquad V(X-\mathrm iY).
$$

[Kembali ke Soal 22.14](#br-ak-2025-2026-w22-ex-14).

<!-- upstream_solution: Ebene algebraische Kurve/y^4+x^3+3xy^2+2x^2y/C/Multiplizität und Tangenten/Aufgabe/Lösung; pageid=21569; revid=1089314 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1089314 -->

## Solusi Soal 22.15 {#br-ak-2025-2026-w22-sol-15}

Multiplisitasnya adalah derajat komponen homogen yang berderajat paling
rendah, yaitu $3$. Untuk menentukan garis-garis singgung, kita harus
memfaktorkan $X^3+3XY^2+2X^2Y$ menjadi faktor-faktor linear. Kita mempunyai

$$
X^3+3XY^2+2X^2Y=X(X^2+3Y^2+2XY).
$$

Selanjutnya,

$$
\begin{aligned}
X^2+3Y^2+2XY
&=(X+Y)^2-Y^2+3Y^2 \\
&=(X+Y)^2+2Y^2 \\
&=(X+Y+\sqrt2\,\mathrm iY)(X+Y-\sqrt2\,\mathrm iY).
\end{aligned}
$$

Jadi, garis-garis singgungnya adalah

$$
X=0
$$

(sumbu $Y$), serta

$$
X=-(1+\sqrt2\,\mathrm i)Y
\quad\text{dan}\quad
X=(-1+\sqrt2\,\mathrm i)Y.
$$

[Kembali ke Soal 22.15](#br-ak-2025-2026-w22-ex-15).

<!-- upstream_solution: Ebene Kurve/v^3+u^2v-2uv+2u^2-4u-2v/Bestimme Singularität/Aufgabe/Lösung; pageid=21307; revid=1089323 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1089323 -->

## Solusi Soal 22.16 {#br-ak-2025-2026-w22-sol-16}

Perhitungan sumber berikut menggunakan hipotesis edisi pada Soal 22.16,
yaitu $\operatorname{char}(K)\notin\{2,3\}$ dan $\sqrt3\in K$.

Misalkan

$$
F=V^3+U^2V-2UV+2U^2-4U-2V.
$$

Maka

$$
\frac{\partial F}{\partial U}=2UV-2V+4U-4
\quad\text{dan}\quad
\frac{\partial F}{\partial V}=3V^2+U^2-2U-2.
$$

Dari persamaan pertama, untuk suatu titik singular diperoleh syarat

$$
V(U-1)=-2U+2,
\qquad\text{atau}\qquad
V=\frac{-2U+2}{U-1},
$$

dengan syarat pada bentuk terakhir bahwa $U\neq1$. Jadi, pertama-tama kita
tinjau kasus $U=1$. Turunan parsial pertama kemudian sama dengan nol tanpa
bergantung pada $V$, sedangkan turunan kedua memberikan syarat

$$
3V^2+1-2-2=0,
\qquad V^2=1,
\qquad V=\pm1.
$$

Persamaan kurva memberikan

$$
V^3+V-2V-2V-2=V^3-3V-2=0,
$$

yang dipenuhi oleh $V=-1$. Oleh karena itu,

$$
P=(1,-1)
$$

merupakan titik singular kurva.

Dengan variabel baru $X=U-1$ dan $Y=V+1$, titik $P$ menjadi titik asal.
Melalui substitusi $U=X+1$ dan $V=Y-1$, persamaan kurva berubah menjadi

$$
\begin{aligned}
&(Y-1)^3+(X+1)^2(Y-1)-2(X+1)(Y-1) \\
&\qquad+2(X+1)^2-4(X+1)-2(Y-1) \\
&=Y^3-3Y^2+3Y-1+(X^2+2X+1)(Y-1) \\
&\qquad-2XY+2X-2Y+2+2X^2+4X+2-4X-4-2Y+2 \\
&=Y^3-3Y^2+3Y-1+X^2Y+2XY+Y-X^2-2X-1 \\
&\qquad-2XY+2X-2Y+2+2X^2+4X+2-4X-4-2Y+2 \\
&=Y^3+X^2Y-3Y^2+X^2.
\end{aligned}
$$

Jadi, komponen homogen berderajat paling rendah adalah

$$
X^2-3Y^2=(X-\sqrt3Y)(X+\sqrt3Y).
$$

Oleh karena itu, multiplisitasnya adalah dua dan kedua garis singgung melalui
titik singular tersebut dideskripsikan oleh

$$
X=\pm\sqrt3Y.
$$

[Kembali ke Soal 22.16](#br-ak-2025-2026-w22-ex-16).

<!-- upstream_solution: Ebene Kurven/Lokale Diffeomorphie/Beispiel/1/Aufgabe/Lösung; pageid=95189; revid=1094625 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1094625 -->

## Solusi Soal 22.18 {#br-ak-2025-2026-w22-sol-18}

Turunan parsial polinom pertama terhadap $X$ adalah

$$
5X^4-3X^2+2Y,
$$

yang pada titik yang diberikan bernilai

$$
4\neq0.
$$

Turunan parsial polinom kedua terhadap $X$ adalah

$$
4X^3-6XY^2+5,
$$

yang pada titik yang diberikan bernilai

$$
5\neq0.
$$

Jadi, kedua kurva mulus pada titik-titik tersebut. Menurut teorema fungsi
implisit, masing-masing kurva dengan demikian secara lokal difeomorfik
dengan suatu interval riil terbuka, sehingga keduanya juga saling
difeomorfik.

[Kembali ke Soal 22.18](#br-ak-2025-2026-w22-ex-18).

---

**Provenans edisi.** Terjemahan dan produksi pembaca: OpenAI Codex
gpt-5.6-sol, Ultra. Sumber, pengarang, dan lisensi komponen dipertahankan
seperti dinyatakan dalam metadata dan berkas hak edisi.
