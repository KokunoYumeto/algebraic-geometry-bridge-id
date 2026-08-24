---
title: "Solusi Publik Lembar Kerja 17"
stable_id: br-ak-2025-2026-w17-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-17/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: f329f9d1a6fc2e862009acd4761ed8289da2cf4c8b42e057db275642c05a700e
public_solution_count: 4
upstream_solution_revisions: "Soal 17.3=1068109; Soal 17.12=1090071; Soal 17.31=1090074; Soal 17.32=1090075"
solution_xml_sha256: "03=bf3b5ded9092bb12d4122ad46b5e37fd250bee2f36bc8709118fcfb128e59d2f; 12=d9cf94dfdb7f48983599c1ee8780ef83e2018e64b6a5146f30659534a33e5a41; 31=4ff966c557cc67bc3bd5292598370ec87b6f65f8d00e515b9a66118c33b7a878; 32=6ea35355e869b4f3eda794d1faf1e079b57d066a9b304b753d6ac8571f574b02"
license: "CC BY-SA 4.0"
translation_status: complete
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 17 {#br-ak-2025-2026-w17-solutions}

Pada batas revisi yang dibekukan, sumber hanya menyediakan solusi publik
untuk Soal 17.3, 17.12, 17.31, dan 17.32. Tidak ada solusi tambahan yang
dibuat untuk edisi ini.

<!-- upstream_solution: Z mod 3/Gruppenring/Rechenbeispiel/1/Aufgabe/Lösung; pageid=168445; revid=1068109 -->
<!-- upstream_solution_revid: 1068109 -->

## Solusi Soal 17.3 {#br-ak-2025-2026-w17-sol-03}

Di dalam $\mathbb Z/(7)[\mathbb Z/(3)]$, koefisien dihitung modulo $7$ dan
pangkat $T$ modulo $3$. Karena itu

$$
\begin{aligned}
&(3T^0-2T^1+5T^2)(4T^0-6T^1+5T^2)\\
&=(3T^0+5T^1+5T^2)(4T^0+T^1+5T^2)\\
&=5T^0+3T^1+T^2+6T^1+5T^2+4T^0
  +6T^2+5T^0+4T^1\\
&=6T+5T^2.
\end{aligned}
$$

[Kembali ke Soal 17.3](#br-ak-2025-2026-w17-ex-03).

<!-- upstream_solution: Monoid/Einheit/Ring/Umkehrung/Aufgabe/Lösung; pageid=95159; revid=1090071 -->
<!-- upstream_solution_revid: 1090071 -->

## Solusi Soal 17.12 {#br-ak-2025-2026-w17-sol-12}

Jika $m$ satuan di $M$, terdapat $n\in M$ dengan

$$
m+n=0.
$$

Maka

$$
T^mT^n=T^{m+n}=T^0=1,
$$

sehingga $T^m$ satuan di gelanggang monoid.

Sebaliknya, misalkan $T^m$ satuan di gelanggang monoid. Terdapat unsur

$$
P=\sum_{n\in E}a_nT^n
$$

dengan dukungan hingga $E\subseteq M$, semua koefisien yang dicantumkan
$a_n\in K$ tak nol, dan

$$
T^mP=\sum_{n\in E}a_nT^{m+n}=1.
$$

Koefisien $T^0$ pada ruas kiri sama dengan $1$, sehingga setidaknya terdapat
$n\in E$ dengan

$$
m+n=0.
$$

Jadi $m$ mempunyai invers di $M$.

**Catatan edisi:** sumber menyatakan bahwa semua eksponen $m+n$ harus sama
dengan nol. Pada monoid yang tidak memenuhi hukum pembatalan, suku-suku dengan
eksponen yang sama dapat bergabung dan saling meniadakan di luar nol. Argumen
yang diperlukan dan sah adalah bahwa koefisien tak nol dari $T^0$ menjamin
keberadaan setidaknya satu $n$ dengan $m+n=0$; itulah yang ditampilkan di
atas.

[Kembali ke Soal 17.12](#br-ak-2025-2026-w17-ex-12).

<!-- upstream_solution: Monoidring/Q geq 0/Über K/Teiler von X/Aufgabe/Lösung; pageid=72875; revid=1090074 -->
<!-- upstream_solution_revid: 1090074 -->

## Solusi Soal 17.31 {#br-ak-2025-2026-w17-sol-31}

Pembagi-pembagi $X$ tepat merupakan unsur berbentuk

$$
aX^q,
\qquad a\ne0,
\qquad q\in\mathbb Q_{\geq0},
\qquad q\leq1.
$$

Setiap unsur semacam itu memang pembagi, sebab

$$
(aX^q)(a^{-1}X^{1-q})
=X^qX^{1-q}
=X^{q+1-q}
=X.
$$

Sebaliknya, misalkan

$$
P=a_{q_1}X^{q_1}+a_{q_2}X^{q_2}+\cdots+a_{q_n}X^{q_n},
\qquad
0\leq q_1<q_2<\cdots<q_n,
$$

merupakan pembagi $X$. Maka terdapat

$$
Q=b_{r_1}X^{r_1}+b_{r_2}X^{r_2}+\cdots+b_{r_m}X^{r_m},
\qquad
0\leq r_1<r_2<\cdots<r_m,
$$

dengan semua koefisien yang dicantumkan tak nol dan $PQ=X$. Suku berpangkat
terendah dan tertinggi dalam hasil kali itu adalah

$$
a_{q_1}b_{r_1}X^{q_1+r_1}
\quad\text{dan}\quad
a_{q_n}b_{r_m}X^{q_n+r_m};
$$

keduanya tak nol. Agar $PQ=X$, harus berlaku

$$
q_1+r_1=q_n+r_m=1.
$$

Karena urutan eksponen ketat, ini hanya mungkin jika $n=m=1$. Jadi
$P=aX^q$ dengan $0\leq q\leq1$, seperti dinyatakan.

**Catatan edisi:** pada suku ekstrem terakhir, sumber mencetak
$a_{q_n}b_{r_n}$, padahal dukungan $Q$ mempunyai $m$ suku dan baris berikutnya
sendiri menggunakan $r_m$. Edisi ini menampilkan indeks terminal
$a_{q_n}b_{r_m}$.

[Kembali ke Soal 17.31](#br-ak-2025-2026-w17-ex-31).

<!-- upstream_solution: Monoidring/Q/Über K/Einheiten/Aufgabe/Lösung; pageid=72879; revid=1090075 -->
<!-- upstream_solution_revid: 1090075 -->

## Solusi Soal 17.32 {#br-ak-2025-2026-w17-sol-32}

Satuan-satuan tepat merupakan unsur berbentuk

$$
aX^q,
\qquad a\ne0,
\qquad q\in\mathbb Q.
$$

Unsur semacam itu satuan karena

$$
(aX^q)(a^{-1}X^{-q})
=X^qX^{-q}
=X^{q-q}
=X^0
=1.
$$

Sebaliknya, misalkan

$$
P=a_{q_1}X^{q_1}+a_{q_2}X^{q_2}+\cdots+a_{q_n}X^{q_n},
\qquad
q_1<q_2<\cdots<q_n,
$$

suatu satuan. Terdapat

$$
Q=b_{r_1}X^{r_1}+b_{r_2}X^{r_2}+\cdots+b_{r_m}X^{r_m},
\qquad
r_1<r_2<\cdots<r_m,
$$

dengan semua koefisien yang dicantumkan tak nol dan $PQ=1$. Suku berpangkat
terendah dan tertinggi dalam hasil kali adalah

$$
a_{q_1}b_{r_1}X^{q_1+r_1}
\quad\text{dan}\quad
a_{q_n}b_{r_m}X^{q_n+r_m},
$$

dan keduanya tak nol. Agar hasil kali sama dengan $1$, harus berlaku

$$
q_1+r_1=q_n+r_m=0.
$$

Ketatnya urutan eksponen memaksa $n=m=1$. Jadi $P=aX^q$.

[Kembali ke Soal 17.32](#br-ak-2025-2026-w17-ex-32).
