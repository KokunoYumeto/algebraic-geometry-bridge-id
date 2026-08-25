---
title: "Solusi Publik Lembar Kerja 23"
stable_id: br-ak-2025-2026-w23-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-23/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: fdfec83fe1ef4f0d87eca194f2991805cd69ff2af070b73ef83c0ba1c9d1e4c4
authority_manifest: authority/wikiversity/unit-23/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: f7ee49a4bfa589b831c1fdb69e6f091ac1762d9da019a133670e4e0d723d34ae
public_solution_count: 2
upstream_solution_revisions: "Soal 23.4=1090216; Soal 23.5=1096444"
solution_xml_sha256: "04=56b03cddd25d14146c8934076599108a3cbf927f6696e7aaed9612b3fed40bea; 05=549cbd738a19c67071ca964c1bfa55e472c8ae592b01e8ce88b2a62114924300"
license: "CC BY-SA 4.0"
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_corrections: 2
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 23 {#br-ak-2025-2026-w23-solutions}

Pada batas revisi yang dibekukan, sumber hanya menyediakan solusi publik
untuk Soal 23.4 dan 23.5. Tidak ada solusi tambahan yang dibuat untuk edisi
ini.

<!-- upstream_solution: Polynomring/2/Multiplizität/Multiplikation/Aufgabe/Lösung; pageid=95515; revid=1090216 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1090216 -->

## Solusi Soal 23.4 {#br-ak-2025-2026-w23-sol-04}

Tulislah $S=K[X,Y]$. Karena suku homogen terendah $F$ berderajat $m$, kita
mempunyai $F\in\mathfrak m^m$. Untuk keterdefinisian yang baik, misalkan
$G\in\mathfrak m^{n-m}$. Maka

$$
FG\in\mathfrak m^m\mathfrak m^{n-m}=\mathfrak m^n.
$$

Jadi pemetaan modul-$S$

$$
S\xrightarrow{\,\cdot F\,}S
\longrightarrow S/\mathfrak m^n
$$

bernilai nol pada $\mathfrak m^{n-m}$. Berdasarkan sifat universal modul
faktor, pemetaan tersebut menginduksi homomorfisme modul-$S$

$$
S/\mathfrak m^{n-m}
\xrightarrow{\,\cdot F\,}
S/\mathfrak m^n.
$$

Untuk membuktikan injektivitas, misalkan kelas $G$ dipetakan ke nol, sehingga
$FG\in\mathfrak m^n$. Andaikan $G\notin\mathfrak m^{n-m}$. Jika $q$ adalah
derajat suku homogen tak nol terendah $G_q$ dari $G$, maka

$$
q<n-m.
$$

Suku homogen terendah dari $FG$ adalah $F_mG_q$. Karena $K[X,Y]$ merupakan
domain integral dan $F_m,G_q\ne0$, berlaku

$$
F_mG_q\ne0,
\qquad
\deg(F_mG_q)=m+q<n.
$$

Dengan demikian $FG\notin\mathfrak m^n$, bertentangan dengan asumsi. Jadi
$G\in\mathfrak m^{n-m}$ dan kelasnya nol. Homomorfisme yang diinduksi
tersebut injektif. $\square$

*Catatan edisi -- koreksi solusi sumber:* Sumber mengatakan bahwa $FG$
mempunyai monom berderajat “kurang dari $m$”; batas yang diperlukan adalah
kurang dari $n$. Argumen melalui suku homogen terendah $F_mG_q$ di atas juga
menutup kemungkinan pembatalan. Karena perkalian dengan $F$ umumnya bukan
homomorfisme gelanggang, faktorisasi yang digunakan adalah sifat universal
*modul* faktor.

[Kembali ke Soal 23.4](#br-ak-2025-2026-w23-ex-04)

<!-- upstream_solution: Numerisches Monoid/N ab e/Hilbert-Funktion/Aufgabe/Lösung; pageid=95541; revid=1096444 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1096444 -->

## Solusi Soal 23.5 {#br-ak-2025-2026-w23-sol-05}

1. Kita klaim bahwa

   $$
   nM_+=\mathbb N_{\ge ne}.
   $$

   Keanggotaan $k\in nM_+$ berarti bahwa terdapat
   $m_1,\ldots,m_n\in M_+=\mathbb N_{\ge e}$ dengan

   $$
   k=m_1+\cdots+m_n.
   $$

   Karena $m_j\ge e$ untuk setiap $j$, diperoleh $k\ge ne$. Sebaliknya,
   jika $k\ge ne$, maka

   $$
   k=(n-1)e+m,
   \qquad m:=k-(n-1)e\ge e.
   $$

   Jadi ruas kanan adalah jumlah $n$ unsur $M_+$ dan $k\in nM_+$.

2. Diperoleh

   $$
   M\setminus nM_+
   =M\setminus\mathbb N_{\ge ne}
   =\{0,e,e+1,\ldots,ne-1\}.
   $$

   Karena itu,

   $$
   \#(M\setminus nM_+)=ne-e+1=(n-1)e+1.
   $$

3. Ideal $\mathfrak m^n$ adalah ideal monom $K[nM_+]$. Pelokalan tidak
   mengubah hasil bagi berdimensi hingga ini, dan terdapat isomorfisme ruang
   vektor-$K$

   $$
   \begin{aligned}
   R/\mathfrak m^n
   &\cong K[M]/K[nM_+]\\
   &\cong
   \operatorname{span}_K
   \{T^m\mid m\in M\setminus nM_+\}.
   \end{aligned}
   $$

   Maka

   $$
   \dim_K(R/\mathfrak m^n)=(n-1)e+1.
   $$

*Catatan edisi -- koreksi solusi sumber:* Pada bagian pertama, sumber
menuliskan $n_j\ge e$ setelah memperkenalkan $m_1,\ldots,m_n$; indeks yang
benar ialah $m_j\ge e$. Pada bagian ketiga, notasi sumber menyamakan hasil
bagi dengan $K[M\setminus nM_+]$ seolah-olah komplemen itu gelanggang
monoid. Edisi menyatakan objek yang tepat: hasil bagi oleh ideal monom
$K[nM_+]$ dan ruang linear dengan basis monom dari komplemennya.

[Kembali ke Soal 23.5](#br-ak-2025-2026-w23-ex-05)
