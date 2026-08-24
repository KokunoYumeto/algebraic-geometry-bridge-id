---
title: "Solusi Publik Lembar Kerja 10"
stable_id: br-ak-2025-2026-w10-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-10/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: 972e36256d128916533a33be1d2feedfdecbd133a0dbba96193a85477cf7e92c
public_solution_count: 6
upstream_solution_revisions: "Soal 10.1=1028855; Soal 10.6=1068028; Soal 10.9=1068729; Soal 10.16=536882; Soal 10.17=743216; Soal 10.20=1112824"
solution_ex01_xml_sha256: 31c3ede05c3c48f6874d9438be3268fb23fb82e34d86e86019b7d88943b35860
solution_ex06_xml_sha256: 876565809f57d44a1c7721ec1ca3a591f1236a4dad869558c871c14d7602a97f
solution_ex09_xml_sha256: 7f2d29f86b768f7b953873e092ab3da83f6c4cc7c7a87a343fa574463d6591c8
solution_ex16_xml_sha256: 20633a9d709de29027a543a08d402f7daaa76326cc624dcce6d14763bb0b620d
solution_ex17_xml_sha256: b7db71351f962f7a6621fd23a555ce07f7afbb07cc81a34aed96368acf885ca1
solution_ex20_xml_sha256: 8969cca31d81d18bf98bb7ea9b008e8e15d169caf0037312a45c9c91f13d9557
license: "CC BY-SA 4.0"
translation_status: complete
---

# Solusi Publik Lembar Kerja 10 {#br-ak-2025-2026-w10-solutions}

Sumber hanya menyediakan solusi publik untuk Soal 10.1, 10.6, 10.9, 10.16,
10.17, dan 10.20 pada batas revisi yang dibekukan. Tidak ada solusi tambahan
yang dibuat untuk edisi ini.

<!-- upstream_solution: Endliche Algebra über Körper/Kommutativ/Einheit und Nichtnullteiler/Aufgabe/Lösung; pageid=94256; revid=1028855 -->
<!-- upstream_solution_revid: 1028855 -->

## Solusi Soal 10.1 {#br-ak-2025-2026-w10-sol-01}

Jika $f$ suatu satuan, maka ada $g\in A$ dengan $gf=1$. Dari $fh=0$ langsung
diperoleh

$$
h=gfh=g0=0.
$$

Jadi $f$ bukan pembagi nol.

Sebaliknya, jika $f$ bukan pembagi nol, tinjau pemetaan perkalian linear-$K$

$$
\mu_f:A\longrightarrow A,
\qquad h\longmapsto fh.
$$

Pemetaan ini injektif. Karena $A$ hingga sebagai modul atas lapangan $K$,
$A$ merupakan ruang vektor-$K$ berdimensi hingga. Suatu endomorfisme injektif
pada ruang vektor berdimensi hingga juga surjektif. Secara khusus, terdapat
$g\in A$ dengan $fg=1$. Ini berarti bahwa $f$ suatu satuan.

[Kembali ke Soal 10.1](#br-ak-2025-2026-w10-ex-01).

<!-- upstream_solution: Kommutativer Ring/Ideale/Chinesischer Restsatz/Kurze exakte Sequenz/Aufgabe/Lösung; pageid=168416; revid=1068028 -->
<!-- upstream_solution_revid: 1068028 -->

## Solusi Soal 10.6 {#br-ak-2025-2026-w10-sol-06}

Misalkan diberikan $r\in R/(I\cap J)$ yang dipetakan ke $(r,r)=0$ dalam
$R/I\times R/J$. Kedua komponennya sama dengan $0$, sehingga $r\in I$ dan
$r\in J$. Jadi $r\in I\cap J$, sehingga kelas $r$ di sebelah kiri adalah
$0$. Dengan demikian, pemetaan di sebelah kiri injektif.

Pemetaan komposit diberikan oleh

$$
r\longmapsto(r,r)\longmapsto r-r,
$$

jadi merupakan pemetaan nol. Sebaliknya, jika $(s,t)$ dipetakan ke $0$ di
sebelah kanan, maka $s-t\in I+J$. Katakanlah

$$
s-t=a+b,
\qquad a\in I,\quad b\in J.
$$

Maka

$$
s-a=t+b
$$

di $R$. Unsur ini juga merepresentasikan $(s,t)$, jadi $(s,t)$ berasal dari
sebelah kiri. Kesurjektifan pemetaan terakhir diperoleh langsung dengan
memilih $t=0$.

[Kembali ke Soal 10.6](#br-ak-2025-2026-w10-ex-06).

<!-- upstream_solution: Kurze exakte Sequenz/Modul/Duale Sequenz/Aufgabe/Lösung; pageid=168494; revid=1068729 -->
<!-- upstream_solution_revid: 1068729 -->

## Solusi Soal 10.9 {#br-ak-2025-2026-w10-sol-09}

Dari kesurjektifan pemetaan $M\to N$ langsung diperoleh bahwa pemetaan

$$
N^*\longrightarrow M^*
$$

injektif: pemetaan linear-$R$ $N\to R$ yang kompositnya dengan $M\to N$
adalah pemetaan nol haruslah merupakan pemetaan nol.

Karena komposit $L\to M\to N$ adalah pemetaan nol, hal yang sama berlaku
untuk pemetaan dual yang bersesuaian.

Tinggal ditunjukkan bahwa suatu bentuk linear $f\in M^*$ yang dipetakan ke
$0$ dalam $L^*$ berasal dari suatu bentuk dual dalam $N^*$. Syarat tersebut
berarti bahwa pembatasan $f$ pada submodul $L\subseteq M$ adalah pemetaan nol.
Dengan kata lain, $L$ termuat dalam kernel $f$. Menurut teorema homomorfisme,
terdapat homomorfisme terinduksi

$$
\widetilde f:M/L\longrightarrow R
$$

yang kompositnya dengan $M\to M/L$ sama dengan $f$. Karena $M/L\cong N$,
inilah pernyataan yang dikehendaki.

[Kembali ke Soal 10.9](#br-ak-2025-2026-w10-ex-09).

<!-- upstream_solution: Kommutative Ringtheorie/f nicht nilpotent/Existenz von Primidealen/Fakt/Beweis/Aufgabe/Lösung; pageid=95372; revid=536882 -->
<!-- upstream_solution_revid: 536882 -->

## Solusi Soal 10.16 {#br-ak-2025-2026-w10-sol-16}

Tinjau himpunan ideal

$$
\mathcal M=
\left\{\mathfrak a\text{ ideal}\mid
f^r\notin\mathfrak a\text{ untuk setiap }r\right\}.
$$

Himpunan ini tidak kosong karena memuat ideal nol. Selain itu,
$\mathcal M$ terurut secara induktif terhadap inklusi. Memang, jika
$\mathfrak a_i$, $i\in I$, merupakan subhimpunan terurut total dari
$\mathcal M$, maka gabungannya juga suatu ideal yang tidak memuat pangkat
mana pun dari $f$. Menurut Lema Zorn, $\mathcal M$ mempunyai unsur maksimal.

Kita klaim bahwa setiap unsur maksimal seperti itu, katakanlah
$\mathfrak p$, merupakan ideal prima. Ambil $g,h\in R$ dengan
$gh\in\mathfrak p$, dan andaikan $g,h\notin\mathfrak p$. Maka terdapat
inklusi sejati

$$
\mathfrak p\subsetneq\mathfrak p+(g),
\qquad
\mathfrak p\subsetneq\mathfrak p+(h).
$$

Karena $\mathfrak p$ maksimal dalam $\mathcal M$, kedua ideal di sebelah
kanan tidak berada dalam $\mathcal M$. Jadi terdapat $r,s\in\mathbb N$
sedemikian sehingga

$$
f^r\in\mathfrak p+(g)
\qquad\text{dan}\qquad
f^s\in\mathfrak p+(h).
$$

Namun, dengan mengalikan kedua hubungan itu kita memperoleh kontradiksi

$$
f^{r+s}\in\mathfrak p+(gh)\subseteq\mathfrak p.
$$

Jadi $\mathfrak p$ prima dan, menurut definisi $\mathcal M$,
$f\notin\mathfrak p$.

[Kembali ke Soal 10.16](#br-ak-2025-2026-w10-ex-16).

<!-- upstream_solution: Kommutative Ringtheorie/Ideale/Radikal ist Durchschnitt von Primidealen/Aufgabe/Lösung; pageid=140640; revid=743216 -->
<!-- upstream_solution_revid: 743216 -->

## Solusi Soal 10.17 {#br-ak-2025-2026-w10-sol-17}

Misalkan $\mathfrak a\subseteq R$ suatu ideal radikal. Maka
$\mathfrak a=\sqrt{\mathfrak a}$. Ideal nilradikal dari $R/\mathfrak a$
adalah irisan semua ideal prima dalam gelanggang faktor itu. Di bawah
korespondensi antara ideal-ideal $R/\mathfrak a$ dan ideal-ideal $R$ yang
memuat $\mathfrak a$, hal ini memberikan

$$
\sqrt{\mathfrak a}
=\bigcap_{\substack{\mathfrak p\supseteq\mathfrak a\\
                    \mathfrak p\text{ prima}}}\mathfrak p.
$$

Karena $\mathfrak a=\sqrt{\mathfrak a}$, diperoleh

$$
\mathfrak a
=\bigcap_{\substack{\mathfrak p\supseteq\mathfrak a\\
                    \mathfrak p\text{ prima}}}\mathfrak p.
$$

[Kembali ke Soal 10.17](#br-ak-2025-2026-w10-ex-17).

<!-- upstream_solution: Hilbertscher Nullstellensatz/Algebraisch/Z/Endlicher Körper/Aufgabe/Lösung; pageid=94501; revid=1112824 -->
<!-- upstream_solution_revid: 1112824 -->

## Solusi Soal 10.20 {#br-ak-2025-2026-w10-sol-20}

Tinjau pemetaan komposit

$$
\mathbb Z\xrightarrow{\varphi}A\longrightarrow A/\mathfrak m=L,
$$

yang juga bertipe hingga. Prapeta $\varphi^{-1}(\mathfrak m)$ merupakan ideal
prima dalam $\mathbb Z$, jadi sama dengan $(0)$ atau $(p)$ untuk suatu
bilangan prima $p$.

Dalam kasus pertama terdapat faktorisasi

$$
\mathbb Z\longrightarrow\mathbb Q\longrightarrow L.
$$

Menurut Nullstellensatz Hilbert, $L$ hingga di atas $\mathbb Q$, dan menurut
Lema 10.5, $\mathbb Q$ kemudian harus dibangkitkan secara hingga di atas
$\mathbb Z$, padahal hal ini tidak benar. Jadi kasus pertama mustahil.

Karena itu berlaku kasus kedua dan terdapat faktorisasi

$$
\mathbb Z\longrightarrow\mathbb Z/(p)\longrightarrow L.
$$

Menurut Nullstellensatz Hilbert, $L$ hingga di atas lapangan berhingga
$\mathbb Z/(p)$, sehingga $L$ sendiri berhingga.

[Kembali ke Soal 10.20](#br-ak-2025-2026-w10-ex-20).
