---
title: "Solusi Publik Lembar Kerja 21"
stable_id: br-ak-2025-2026-w21-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-21/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: 9329621bbdd62df63f01d7298dc2a4a65a296211db131f8d8730b7d308fd5f47
public_solution_count: 2
upstream_solution_revisions: "Soal 21.3=1068126; Soal 21.8=1113184"
solution_xml_sha256: "03=70d121ea8136ceefbc726198671bd03643ba84382f694a5aafa66272c522bdf9; 08=5821567b75632728c65045870c4aede0d84d7a39c0901c8320cfded033259b71"
license: "CC BY-SA 4.0"
translation_status: complete
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 21 {#br-ak-2025-2026-w21-solutions}

Pada batas revisi yang dibekukan, sumber hanya menyediakan solusi publik
untuk Soal 21.3 dan 21.8. Kedua solusi berupa tubuh sumber lengkap tanpa
transklusi pembungkus. Tidak ada solusi tambahan yang dibuat untuk edisi ini.

<!-- upstream_solution: Diskreter Bewertungsring/Zwischenringe im Quotientenkörper/Aufgabe/Lösung; pageid=168446; revid=1068126 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1068126 -->

## Solusi Soal 21.3 {#br-ak-2025-2026-w21-sol-03}

Misalkan ideal maksimal di $R$ adalah

$$
\mathfrak m=(\pi).
$$

Lapangan pecahan $R$ adalah

$$
Q(R)=R_\pi,
$$

dan di dalam lapangan ini setiap unsur tak nol berbentuk

$$
u\pi^n,
\qquad u\in R^\times,\quad n\in\mathbb Z.
$$

Misalkan

$$
R\subsetneq T\subseteq Q(R).
$$

Karena inklusi pertama ketat, terdapat suatu unsur

$$
u\pi^n\in T
$$

dengan $n<0$. Karena $u$ merupakan satuan di $R\subseteq T$, kita juga
mempunyai $\pi^n\in T$. Selanjutnya, $-n-1\geq0$, sehingga

$$
\pi^{-1}=\pi^{-n-1}\pi^n\in T.
$$

Jadi $R_\pi\subseteq T$. Bersama dengan $T\subseteq Q(R)=R_\pi$, hal ini
memberikan

$$
T=Q(R).
$$

Dengan demikian, tidak ada gelanggang perantara sejati antara $R$ dan
lapangan pecahannya.

[Kembali ke Soal 21.3](#br-ak-2025-2026-w21-ex-03).

<!-- upstream_solution: Bewertungstheorie/Körper mit diskreter Bewertung/Diskreter Bewertungsring/Aufgabe/Lösung; pageid=16847; revid=1113184 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1113184 -->

## Solusi Soal 21.8 {#br-ak-2025-2026-w21-sol-08}

Pertama-tama kita tunjukkan bahwa $R$ merupakan subgelanggang dari lapangan
$K$. Menurut definisi, $0\in R$. Karena $\nu$ homomorfisme grup, berlaku

$$
\nu(1)=0,
$$

sehingga $1\in R$. Untuk $f,g\in R$, kasus yang melibatkan unsur nol
langsung memenuhi ketertutupan terhadap perkalian. Jika $f$ dan $g$ tak nol,
maka

$$
\nu(fg)=\nu(f)+\nu(g)\geq0,
$$

sehingga $fg\in R$. Untuk penjumlahan, jika salah satu dari $f,g$ sama
dengan nol atau jika $f+g=0$, ketertutupan juga langsung berlaku. Dalam
kasus selebihnya, $f,g,f+g$ semuanya tak nol dan asumsi memberikan

$$
\nu(f+g)\geq\min\{\nu(f),\nu(g)\}\geq0.
$$

Jadi $f+g\in R$. Selain itu,

$$
\nu(-1)+\nu(-1)
=\nu((-1)^2)
=\nu(1)
=0,
$$

sehingga $\nu(-1)=0$ dan $-1\in R$. Dengan demikian, $R$ juga tertutup
terhadap pengambilan negatif dan merupakan gelanggang komutatif.

Selanjutnya kita tunjukkan bahwa $R$ merupakan gelanggang lokal. Tetapkan

$$
\mathfrak m
:=
\{f\in K^\times\mid \nu(f)\geq1\}\cup\{0\}
\subseteq R.
$$

Himpunan ini memuat $0$. Jika $f,g\in\mathfrak m$, kasus yang melibatkan
unsur nol atau memenuhi $f+g=0$ bersifat langsung. Dalam kasus selebihnya,

$$
\nu(f+g)\geq\min\{\nu(f),\nu(g)\}\geq1,
$$

sehingga $f+g\in\mathfrak m$. Untuk $f\in\mathfrak m$ dan $g\in R$, kasus
$f=0$ atau $g=0$ juga langsung. Jika keduanya tak nol, maka

$$
\nu(gf)=\nu(g)+\nu(f)\geq1,
$$

sehingga $gf\in\mathfrak m$. Jadi $\mathfrak m$ merupakan ideal.

Komplemen $R\setminus\mathfrak m$ terdiri tepat atas unsur
$h\in K^\times$ dengan

$$
\nu(h)=0.
$$

Untuk unsur seperti itu,

$$
\nu(h^{-1})=-\nu(h)=0,
$$

sehingga $h^{-1}\in R$. Jadi semua unsur dalam
$R\setminus\mathfrak m$ merupakan satuan. Oleh karena itu,
$\mathfrak m$ adalah satu-satunya ideal maksimal, dan $R$ merupakan
gelanggang lokal.

Masih harus ditunjukkan bahwa $R$ merupakan gelanggang valuasi diskret.
Karena $\nu$ surjektif, terdapat $p\in K^\times$ dengan

$$
\nu(p)=1.
$$

Khususnya, $p\in R$. Kita tunjukkan bahwa $p$ merupakan unsur prima. Untuk
unsur tak nol $x,y\in R$, unsur $y$ merupakan kelipatan $x$ tepat ketika

$$
\nu(y)\geq\nu(x),
$$

sebab kondisi itu ekuivalen dengan $y/x\in R$. Sekarang misalkan
$p\mid xy$ untuk $x,y\in R$. Jika $xy=0$, salah satu faktor sama dengan nol
dan tentu merupakan kelipatan $p$. Jika $xy\ne0$, maka

$$
1=\nu(p)\leq\nu(xy)=\nu(x)+\nu(y).
$$

Karena $\nu(x)$ dan $\nu(y)$ bilangan bulat tak negatif, berlaku
$\nu(x)\geq1$ atau $\nu(y)\geq1$. Dengan karakterisasi keterbagian di atas,
$p$ membagi salah satu dari $x$ atau $y$. Jadi $p$ merupakan unsur prima.

Dengan argumen yang sama, setiap unsur tak nol $x\in R$ dengan

$$
n=\nu(x)
$$

berasosiasi dengan $p^n$. Memang, $\nu(x/p^n)=0$, sehingga $x/p^n$ merupakan
satuan di $R$. Jadi $R$ merupakan domain ideal utama dengan tepat ideal-ideal
$0$ dan

$$
(p^n),
\qquad n\in\mathbb N.
$$

Dengan demikian, $R$ merupakan gelanggang valuasi diskret.

**Catatan edisi:** sumber mendefinisikan $\nu$ hanya pada $K^\times$, tetapi
menyatakan pertaksamaan untuk $\nu(f+g)$ tanpa syarat $f+g\ne0$. Karena
$\nu(0)$ tidak terdefinisi, edisi ini memakai pertaksamaan tersebut hanya
ketika $f+g\ne0$ dan menangani kasus jumlah nol secara terpisah; edisi ini
tidak memperluas $\nu$ ke $0$.

[Kembali ke Soal 21.8](#br-ak-2025-2026-w21-ex-08).

---

**Provenans edisi.** Terjemahan dan produksi pembaca: OpenAI Codex
gpt-5.6-sol, Ultra. Sumber, pengarang, dan lisensi komponen dipertahankan
seperti dinyatakan dalam metadata dan berkas hak edisi.
