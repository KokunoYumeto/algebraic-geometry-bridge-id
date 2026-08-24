---
title: "Solusi Publik Lembar Kerja 15"
stable_id: br-ak-2025-2026-w15-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-15/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: 3c8c41458f5418ff858a58748ba4b23bc0a8cb34d9c386c155806b4482760470
public_solution_count: 4
upstream_solution_revisions: "Soal 15.6=663110; Soal 15.9=1095144; Soal 15.19=1112864; Soal 15.22=1089392"
solution_xml_sha256: "06=20af89ec50341df835441e3b0c06a80ca6ad7c015bbcd31a3c25e0567476ca7c; 09=b11c0433de7913559f0081546f223982afc420b66da100fd2c1da072ef9488ba; 19=7a9835691cd557c0cb97717e3ad86be45cb2ffd9ee20e6da501446f964b07d0b; 22=926741a153722186dfd4e1c4e99ef24f2021a8e10e242fb8224083cb0628cec5"
license: "CC BY-SA 4.0"
translation_status: complete
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 15 {#br-ak-2025-2026-w15-solutions}

Pada batas revisi yang dibekukan, sumber hanya menyediakan solusi publik
untuk Soal 15.6, 15.9, 15.19, dan 15.22. Tidak ada solusi tambahan yang
dibuat untuk edisi ini.

<!-- upstream_solution: Kommutative Ringtheorie/Primideal/Restekörper als Quotientenring/Fakt/Beweis/Aufgabe/Lösung; pageid=126006; revid=663110 -->
<!-- upstream_solution_revid: 663110 -->

## Solusi Soal 15.6 {#br-ak-2025-2026-w15-sol-06}

Tinjau diagram komutatif homomorfisme gelanggang

$$
\begin{array}{ccccc}
R&\longrightarrow&R/\mathfrak p&\longrightarrow&Q(R/\mathfrak p)\\
\downarrow&&\downarrow_{\varphi}&&\downarrow_{\psi}\\
R_{\mathfrak p}&\longrightarrow&R_{\mathfrak p}/\mathfrak pR_{\mathfrak p}
&=&R_{\mathfrak p}/\mathfrak pR_{\mathfrak p}.
\end{array}
$$

Di bawah homomorfisme gelanggang

$$
R\longrightarrow R_{\mathfrak p}/\mathfrak pR_{\mathfrak p},
$$

ideal prima $\mathfrak p$ dipetakan ke nol, sehingga diperoleh
homomorfisme terinduksi $\varphi$. Homomorfisme $\varphi$ memetakan setiap
unsur tak nol

$$
[r]\in R/\mathfrak p,
\qquad [r]\ne0,
$$

yang diwakili oleh $r\notin\mathfrak p$, ke suatu satuan. Berdasarkan sifat
universal pelokalan, $\varphi$ karena itu dapat diperluas ke lapangan
pecahan:

$$
\psi:Q(R/\mathfrak p)
\longrightarrow R_{\mathfrak p}/\mathfrak pR_{\mathfrak p}.
$$

Sebagai homomorfisme gelanggang antara lapangan, $\psi$ injektif. Setiap
unsur lapangan residu di ruas kanan dapat diwakili oleh pecahan $r/s$ di
$R_{\mathfrak p}$ dengan $s\notin\mathfrak p$. Unsur itu merupakan citra

$$
\frac{[r]}{[s]}\in Q(R/\mathfrak p),
$$

karena $[s]\ne0$. Jadi $\psi$ juga surjektif dan merupakan isomorfisme.

[Kembali ke Soal 15.6](#br-ak-2025-2026-w15-ex-06).

<!-- upstream_solution: Lokaler Ring/Restklassenring/Einheiten surjektiv/Aufgabe/Lösung; pageid=95358; revid=1095144 -->
<!-- upstream_solution_revid: 1095144 -->

## Solusi Soal 15.9 {#br-ak-2025-2026-w15-sol-09}

Jika $\mathfrak a=R$, gelanggang faktornya adalah gelanggang nol dan
pernyataannya jelas. Jadi andaikan

$$
\mathfrak a\subseteq\mathfrak m,
$$

dengan $\mathfrak m$ ideal maksimal tunggal $R$.

Misalkan $r\in R$ mewakili suatu satuan di $R/\mathfrak a$, dan pilih
$s\in R$ sedemikian sehingga

$$
rs=1\quad\text{di }R/\mathfrak a.
$$

Ini berarti

$$
rs-1\in\mathfrak a\subseteq\mathfrak m.
$$

Jika $r$ bukan satuan, maka $r\in\mathfrak m$, sehingga
$rs\in\mathfrak m$. Akan tetapi, ini memberikan kontradiksi

$$
1=(1-rs)+rs\in\mathfrak m.
$$

Jadi $r$ sendiri merupakan satuan. Dengan demikian setiap satuan di
$R/\mathfrak a$ mempunyai pra-citra satuan di $R$.

[Kembali ke Soal 15.9](#br-ak-2025-2026-w15-ex-09).

<!-- upstream_solution: Integre endlich erzeugte Algebren/Lokaler Isomorphismus/In Umgebung/Aufgabe/Lösung; pageid=21576; revid=1112864 -->
<!-- upstream_solution_revid: 1112864 -->

## Solusi Soal 15.19 {#br-ak-2025-2026-w15-sol-19}

Kita buktikan terlebih dahulu bahwa pemetaan

$$
R_f\longrightarrow S_{\varphi(f)}
$$

surjektif untuk suatu $f\in R$ yang sesuai. Pilih suatu sistem pembangkit
aljabar-$K$, katakanlah $x_1,\ldots,x_n$, bagi $S$. Berdasarkan
surjektivitas pemetaan lokal, terdapat unsur

$$
y_i=\frac{r_i}{g_i}\in R_{\mathfrak m},
\qquad g_i\notin\mathfrak m,
$$

dengan $\varphi(y_i)=x_i$ di $S_{\mathfrak n}$. Kesamaan terakhir berarti
bahwa untuk suatu $h_i\notin\mathfrak n$ berlaku

$$
h_i\bigl(\varphi(r_i)-\varphi(g_i)x_i\bigr)=0
$$

di $S$. Karena $S$ integral dan $h_i\ne0$, diperoleh

$$
\varphi(r_i)=\varphi(g_i)x_i
$$

di $S$.

Tetapkan

$$
f=g_1\cdots g_n.
$$

Karena setiap $g_i\notin\mathfrak m$ dan $\mathfrak m$ prima, kita mempunyai
$f\notin\mathfrak m$. Semua $y_i$ dapat dituliskan dengan penyebut utama
bersama $f$, sehingga $y_i\in R_f$. Dengan demikian setiap pembangkit $x_i$
berada di dalam citra $R_f\to S_{\varphi(f)}$. Pangkat-pangkat penyebut
$\varphi(f)^k$ juga merupakan citra pangkat-pangkat $f^k$. Maka pemetaan itu
surjektif.

**Catatan edisi:** sumber langsung menyimpulkan surjektivitas dari kesamaan
di $S_{\mathfrak n}$ tanpa menuliskan langkah pembatalan $h_i$ di atas.
Langkah tersebut sah tepat karena hipotesis menyatakan bahwa $S$ integral;
edisi ini membuat ketergantungan itu eksplisit tanpa mengubah argumen.

Sekarang kita buktikan injektivitas. Andaikan $q\in R_f$ dipetakan ke nol.
Maka citranya tentu juga nol di $S_{\mathfrak n}$, dan $q$ berasal dari
unsur di $R_{\mathfrak m}$. Karena pemetaan lokal merupakan isomorfisme,
$q=0$ di $R_{\mathfrak m}$. Karena $R$ integral, hal ini juga memberikan
$q=0$ di $R_f$. Jadi pemetaan tersebut injektif dan, bersama
surjektivitasnya, merupakan isomorfisme.

[Kembali ke Soal 15.19](#br-ak-2025-2026-w15-ex-19).

<!-- upstream_solution: Endlich erzeugte integre K-Algebra/Definitionsort im K-Spektrum ist offen/Aufgabe/Lösung; pageid=21588; revid=1089392 -->
<!-- upstream_solution_revid: 1089392 -->

## Solusi Soal 15.22 {#br-ak-2025-2026-w15-sol-22}

Kita tunjukkan bahwa untuk setiap titik $P$ dengan $q\in\mathcal O_P$,
terdapat lingkungan terbuka $P$ tempat sifat yang sama berlaku di setiap
titik. Himpunan dalam soal lalu merupakan gabungan lingkungan-lingkungan
terbuka tersebut dan karena itu terbuka.

Gelanggang lokal di $P$ berbentuk

$$
\mathcal O_P=R_{\mathfrak m}
$$

untuk suatu ideal maksimal $\mathfrak m$ di $R$. Keanggotaan
$q\in R_{\mathfrak m}$ berarti bahwa

$$
q=\frac rf
$$

dengan $f\notin\mathfrak m$. Maka $P\in D(f)$, sehingga $D(f)$ merupakan
lingkungan terbuka $P$. Untuk setiap $P'\in D(f)$, unsur $f$ juga merupakan
penyebut yang diizinkan. Jadi $q\in\mathcal O_{P'}$ bagi setiap
$P'\in D(f)$, seperti yang diperlukan.

[Kembali ke Soal 15.22](#br-ak-2025-2026-w15-ex-22).
