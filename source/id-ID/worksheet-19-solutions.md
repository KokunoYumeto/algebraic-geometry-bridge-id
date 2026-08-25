---
title: "Solusi Publik Lembar Kerja 19"
stable_id: br-ak-2025-2026-w19-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-19/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: f75bcc8e564cef327687b486bb074fa8c799b065994f4a1d79e7abf2b78b30dd
public_solution_count: 2
upstream_solution_revisions: "Soal 19.4=1089525; Soal 19.12=1089395"
solution_xml_sha256: "04=d7bb006cf095c0f6bd86d7690802bf62956452bc2d6f739b1c3005325828981a; 12=c1f14a69bfcc5cc33d7f2b50a07abf49163fa04631cfcd5cd083cea81a62f3c5"
license: "CC BY-SA 4.0"
translation_status: complete
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 19 {#br-ak-2025-2026-w19-solutions}

Pada batas revisi yang dibekukan, sumber hanya menyediakan solusi publik
untuk Soal 19.4 dan 19.12. Tidak ada solusi tambahan yang dibuat untuk edisi
ini.

<!-- upstream_solution: Ganze Erweiterung/Integritätsbereich/Nichteinheit bleibt Nichteinheit/Aufgabe/Lösung; pageid=17225; revid=1089525 -->
<!-- upstream_solution_revid: 1089525 -->

## Solusi Soal 19.4 {#br-ak-2025-2026-w19-sol-04}

Misalkan $s\in S$ invers dari $f$, sehingga $fs=1$. Karena $S$ integral atas
$R$, terdapat suatu persamaan keintegralan untuk $s$, katakanlah

$$
s^n+a_{n-1}s^{n-1}+\cdots+a_1s+a_0=0,
\qquad a_i\in R.
$$

Kita kalikan persamaan ini dengan $f^n$ dan memperoleh

$$
(fs)^n+a_{n-1}f(fs)^{n-1}+\cdots+a_1f^{n-1}(fs)+a_0f^n=0,
$$

atau, karena $fs=1$,

$$
1+a_{n-1}f+\cdots+a_1f^{n-1}+a_0f^n=0.
$$

Dengan memfaktorkan $f$, kita memperoleh

$$
1+f\left(a_{n-1}+\cdots+a_1f^{n-2}+a_0f^{n-1}\right)=0,
$$

dan dengan demikian

$$
f\left(-a_{n-1}-\cdots-a_1f^{n-2}-a_0f^{n-1}\right)=1.
$$

Ekspresi di dalam tanda kurung berada di $R$. Jadi $f$ juga mempunyai invers
di $R$.

[Kembali ke Soal 19.4](#br-ak-2025-2026-w19-ex-04).

<!-- upstream_solution: Endliche Erweiterung/KX/Explizit/Relation über X invers/Aufgabe/Lösung; pageid=134951; revid=1089395 -->
<!-- upstream_solution_revid: 1089395 -->

## Solusi Soal 19.12 {#br-ak-2025-2026-w19-sol-12}

Kita kalikan persamaan keintegralan yang diberikan dengan $X^{-kn}$. Di
dalam lapangan pecahan $Q$ dari gelanggang faktor yang mendefinisikan $R$,
kita memperoleh

$$
Y^nX^{-kn}+\sum_{i=0}^{n-1}P_iY^iX^{-kn}=0.
$$

Di sini

$$
Y^nX^{-kn}=(YX^{-k})^n
$$

dan

$$
\begin{aligned}
P_iY^iX^{-kn}
&=P_iY^iX^{-ki}X^{-k(n-i)}\\
&=(YX^{-k})^iP_iX^{-k(n-i)}.
\end{aligned}
$$

Syarat pada $k$ memastikan bahwa

$$
P_iX^{-k(n-i)}
$$

merupakan polinom dalam $X^{-1}$. Jadi persamaan yang dihasilkan merupakan
persamaan keintegralan monik berderajat $n$ untuk $YX^{-k}$ atas
$K[X^{-1}]$.

Karena $R$ merupakan domain integral, polinom pendefinisi asal tak
tereduksi. Setelah perubahan variabel yang dapat dibalik di $K(X)$, polinom
monik hasil di atas tak tereduksi di $K[X^{-1}][Z]$, dengan $Z$ suatu
variabel formal yang kemudian dipetakan ke $YX^{-k}$.

**Catatan edisi:** sumber menyebut persamaan itu tak tereduksi “di
$K[X^{-1},YX^{-k}]$”. Di dalam aljabar faktor tersebut, relasinya bernilai
nol; gelanggang polinomial yang tepat untuk menyatakan ketaktereduksian adalah
$K[X^{-1}][Z]$. Edisi memperjelas gelanggang tempat polinom itu dipandang dan
variabel formalnya; klaim ini tidak diperlukan untuk dua kesimpulan yang
diminta.

Kita mempunyai

$$
K[X^{-1}][YX^{-k}]\subseteq Q.
$$

Lapangan pecahan ruas kiri memuat $X$ sebagai invers dari $X^{-1}$, lalu
memuat

$$
Y=(YX^{-k})X^k.
$$

Karena itu lapangan pecahannya memuat $K(X,Y)=Q$. Inklusi sebaliknya sudah
jelas dari inklusi di atas, sehingga kedua lapangan pecahan sama.

[Kembali ke Soal 19.12](#br-ak-2025-2026-w19-ex-12).

---

**Provenans edisi.** Terjemahan dan produksi pembaca: OpenAI Codex
gpt-5.6-sol, Ultra. Sumber, pengarang, dan lisensi komponen dipertahankan
seperti dinyatakan dalam metadata dan berkas hak edisi.
