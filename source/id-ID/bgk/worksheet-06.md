---
title: "Lembar Kerja 6 - Ruang Penutup, Eksak, serta Tarik dan Dorong Berkas"
stable_id: br-bgk-2019-w06
language: id-ID
source_course: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)"
source_author: "Holger Brenner"
frozen_revision_contributor: "Bocardodarapti"
upstream_title: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)/Arbeitsblatt 6"
upstream_pageid: 110211
upstream_revid: 900086
upstream_timestamp: "2023-06-27T11:07:09Z"
upstream_mediawiki_sha1: 619536dcd80063470e12de7a3ebb3fc9fe1aa5e5
source_url: "https://de.wikiversity.org/w/index.php?oldid=900086"
authority_manifest: authority/wikiversity-bgk/unit-06/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 69a10e682e853c6f386afbc68438605846e5096220b21bd1e827c07633a79244
worksheet_xml: authority/wikiversity-bgk/unit-06/worksheet-06.xml
worksheet_xml_sha256: b82d2ac0f8a0420a53e44be87c0b5a0f8237daac39ef86cf3be365a3b8fe37bd
worksheet_expanded_tex: authority/wikiversity-bgk/unit-06/worksheet-06-expanded.tex
worksheet_expanded_tex_sha256: 0de1911162df14c38fa00755cf67583fbdd9b101134314e6d47a546922e875c1
exercise_map: authority/wikiversity-bgk/unit-06/ORDERED_EXERCISE_MAP.json
exercise_map_sha256: ea15e1f79b4dfc0928fe132eb83e8d20d10fbc84837de153da2b4e345e5a04a0
official_pdf: authority/artifacts/bgk-worksheet-06-official.pdf
official_pdf_sha256: 7b4f4569e7ab749a9e6affac715592316c109507d91971fd1c7b82cefaa825b5
license: "Frozen semantic course text and this translation: CC BY-SA 4.0. Official PDF witnesses retain their recorded component notices; no blanket relicensing claim is made."
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra."
exercise_count: 19
public_solution_count: 0
---

# Lembar Kerja 6: Ruang Penutup, Eksak, serta Tarik dan Dorong Berkas {#br-bgk-2019-w06}

<!-- upstream_entity: Überlagerung/Diskret/Definition -->

### Definisi: ruang penutup {#br-bgk-2019-w06-def-01}

Misalkan $X$ dan $Y$ ruang topologis. Sebuah pemetaan kontinu

$$
p:Y\longrightarrow X
$$

disebut *pemetaan ruang penutup* apabila terdapat penutup terbuka

$$
X=\bigcup_{i\in I}U_i
$$

dan keluarga ruang topologis diskret $F_i$, untuk $i\in I$, sedemikian
sehingga $p^{-1}(U_i)$ homeomorfik dengan $U_i\times F_i$ (dengan topologi
produk), dan homeomorfisme-homeomorfisme tersebut kompatibel dengan pemetaan
ke $U_i$.

<!-- upstream_entity: R und S^1/Überlagerung/Aufgabe -->

## Soal 6.1 {#br-bgk-2019-w06-ex01}

Tunjukkan bahwa pemetaan

$$
\begin{aligned}
\mathbb R&\longrightarrow S^1,\\
t&\longmapsto(\cos t,\sin t)
\end{aligned}
$$

merupakan pemetaan ruang penutup.

<!-- upstream_entity: C und C^x/Überlagerung/Aufgabe -->

## Soal 6.2 {#br-bgk-2019-w06-ex02}

Tunjukkan bahwa pemetaan

$$
\begin{aligned}
\mathbb C&\longrightarrow\mathbb C^{\times}=\mathbb C\setminus\{0\},\\
z&\longmapsto\exp z
\end{aligned}
$$

merupakan pemetaan ruang penutup.

<!-- upstream_entity: Überlagerung/Lokaler Schnitt/Aufgabe -->

## Soal 6.3 {#br-bgk-2019-w06-ex03}

Buktikan bahwa, untuk setiap pemetaan ruang penutup

$$
p:Y\longrightarrow X,
$$

dan setiap titik $x\in X$, terdapat lingkungan terbuka

$$
x\in U\subseteq X
$$

serta seksi kontinu

$$
s:U\longrightarrow p^{-1}(U)
$$

dengan $p\circ s=\operatorname{Id}_U$.

<!-- upstream_entity: Topologische Gruppen/Spaltende Sequenz/Garbenversion/Aufgabe -->

## Soal 6.4 {#br-bgk-2019-w06-ex04}

Misalkan $F$ dan $H$ grup topologis komutatif, dan misalkan

$$
G=F\times H
$$

adalah grup produk mereka dengan topologi produk. Misalkan

$$
0\longrightarrow F\longrightarrow G\longrightarrow H\longrightarrow0
$$

barisan eksak pendek yang bersesuaian. Tunjukkan bahwa, untuk setiap ruang
topologis $X$, terdapat barisan eksak pendek berkas

$$
0\longrightarrow C^0(-,F)\longrightarrow C^0(-,G)\longrightarrow
C^0(-,H)\longrightarrow0
$$

yang evaluasi globalnya pada bagian paling kanan selalu surjektif.

<!-- upstream_entity: Stetige Abbildung/Prägarbe/Vorschub/Halme/Fakt/Beweis/Aufgabe -->

## Soal 6.5 {#br-bgk-2019-w06-ex05}

Misalkan $\varphi:X\to Y$ sebuah pemetaan kontinu, $Q\in Y$ sebuah titik,
dan $\mathcal F$ sebuah praberkas pada $X$. Tunjukkan bahwa tangkai praberkas
dorong maju $\varphi_*\mathcal F$ di $Q$ sama dengan

$$
\operatorname*{colim}_{Q\in V}\mathcal F(\varphi^{-1}(V))
=
\operatorname*{colim}_{\substack{U\subseteq X\mid
\text{ada }V\text{ terbuka dengan }Q\in V\text{ dan }\varphi^{-1}(V)\subseteq U}}
\mathcal F(U).
$$

> **Catatan edisi - indeks kolimit pada sumber.** Sumber menulis syarat
> lingkungan dengan bentuk ringkas “ada $Q\in V$”; yang dimaksud ialah ada
> himpunan terbuka $V\ni Q$. Bentuk eksplisit tersebut dipakai di atas.

<!-- upstream_entity: Stetige Abbildung/Garbe/Rückzug/Halme/Fakt/Beweis/Aufgabe -->

## Soal 6.6 {#br-bgk-2019-w06-ex06}

Misalkan $\varphi:X\to Y$ sebuah pemetaan kontinu dan $\mathcal G$ sebuah
berkas pada $Y$. Tunjukkan bahwa tangkai berkas tarik balik di titik
$P\in X$ sama dengan tangkai $\mathcal G$ di $\varphi(P)$.

> **Catatan edisi - tata bahasa sumber.** Sumber mencetak frasa Jerman
> *einer stetige Abbildung* (artikel dan adjektiva tidak selaras). Terjemahan
> memakai bentuk Indonesia yang bertipe tanpa mengubah isi matematis.

<!-- upstream_entity: Menge/Topologien/Vorschub und Rückzug/Aufgabe -->

## Soal 6.7 {#br-bgk-2019-w06-ex07}

Misalkan $X$ sebuah himpunan dengan dua topologi $\tau_1$ dan $\tau_2$,
sedemikian sehingga identitas

$$
\varphi:X_1=(X,\tau_1)\longrightarrow X_2=(X,\tau_2)
$$

kontinu; jadi topologi pertama lebih halus daripada topologi kedua.
Misalkan $\mathcal F_1$ sebuah berkas pada $X_1$ dan $\mathcal F_2$ sebuah
berkas pada $X_2$. Tentukan $\varphi_*\mathcal F_1$ dan
$\varphi^{-1}\mathcal F_2$. Bagaimana bentuknya jika $\tau_1$ adalah topologi
diskret dan $\tau_2$ adalah topologi indiscret?

<!-- upstream_entity: Topologischer Raum/Konstante Abbildung/Vorschub/Aufgabe -->

## Soal 6.8 {#br-bgk-2019-w06-ex08}

Misalkan $X$ sebuah ruang topologis dan $\varphi:X\to\{P\}$ pemetaan
konstan. Jika $\mathcal F$ sebuah berkas pada $X$, tentukan
$\varphi_*\mathcal F$.

<!-- upstream_entity: Topologischer Raum/Punkt/Vorschub/Wolkenkratzergarbe/Aufgabe -->

## Soal 6.9 {#br-bgk-2019-w06-ex09}

Misalkan $X$ sebuah ruang topologis, $P\in X$, dan

$$
i:\{P\}\longrightarrow X
$$

inklusi terkait. Misalkan $\mathcal F$ sebuah berkas grup
komutatif pada $\{P\}$. Deskripsikan berkas $i_*\mathcal F$ pada himpunan-
himpunan terbuka di $X$. Bagaimana bentuk tangkai-tangkai $i_*\mathcal F$
apabila $P$ merupakan titik tertutup?

Bandingkan juga Soal 4.9.

<!-- upstream_entity: Topologischer Raum/Konstante Abbildung/Rückzug/Aufgabe -->

## Soal 6.10 {#br-bgk-2019-w06-ex10}

Misalkan $X$ sebuah ruang topologis dan $\varphi:X\to\{P\}$ pemetaan
konstan. Jika $\mathcal G$ sebuah berkas pada $\{P\}$, tentukan
$\varphi^{-1}\mathcal G$.

<!-- upstream_entity: Topologische Räume/Stetige Abbildung/Garbe vorne/Vorschub und Rückzug/Morphismus/Aufgabe -->

## Soal 6.11 {#br-bgk-2019-w06-ex11}

Misalkan $\varphi:X\to Y$ sebuah pemetaan kontinu di antara ruang topologis
$X$ dan $Y$, dan misalkan $\mathcal F$ sebuah berkas pada $X$. Buktikan bahwa
terdapat morfisme berkas alami pada $X$,

$$
\varphi^{-1}(\varphi_*\mathcal F)\longrightarrow\mathcal F.
$$

<!-- upstream_entity: Topologische Räume/Stetige Abbildung/Garbe hinten/Rückzug und Vorschub/Morphismus/Aufgabe -->

## Soal 6.12 {#br-bgk-2019-w06-ex12}

Misalkan $\varphi:X\to Y$ sebuah pemetaan kontinu di antara ruang topologis
$X$ dan $Y$, dan misalkan $\mathcal G$ sebuah berkas pada $Y$. Buktikan bahwa
terdapat morfisme berkas alami pada $Y$,

$$
\mathcal G\longrightarrow\varphi_*\bigl(\varphi^{-1}\mathcal G\bigr).
$$

<!-- upstream_entity: Topologische Räume/Stetige Abbildung/Rückzug und Vorschub/Morphismen/Aufgabe -->

## Soal 6.13 {#br-bgk-2019-w06-ex13}

Misalkan $\varphi:X\to Y$ sebuah pemetaan kontinu di antara ruang topologis
$X$ dan $Y$. Misalkan $\mathcal F$ sebuah berkas pada $X$ dan $\mathcal G$
sebuah berkas pada $Y$. Buktikan bahwa terdapat bijeksi alami antara
morfisme-morfisme berkas pada $X$

$$
\psi:\varphi^{-1}\mathcal G\longrightarrow\mathcal F
$$

dan morfisme-morfisme berkas pada $Y$

$$
\theta:\mathcal G\longrightarrow\varphi_*\mathcal F.
$$

<!-- upstream_entity: Mengen/Relatives Produkt/Aufgabe -->

## Soal 6.14 {#br-bgk-2019-w06-ex14}

Misalkan $L_1,L_2,M$ himpunan, serta $p_1:L_1\to M$ dan $p_2:L_2\to M$
pemetaan. Definisikan

$$
L_1\times_M L_2
:=\{(x_1,x_2)\mid p_1(x_1)=p_2(x_2)\}
\subseteq L_1\times L_2.
$$

1. Tunjukkan bahwa terdapat diagram komutatif

$$
\begin{matrix}
L_1\times_M L_2&\longrightarrow&L_1\\
\downarrow&&\downarrow\\
L_2&\longrightarrow&M
\end{matrix}
$$

2. Misalkan $T$ sebuah himpunan lain dan $\psi_1:T\to L_1$ serta
   $\psi_2:T\to L_2$ pemetaan dengan

   $$
   p_1\circ\psi_1=p_2\circ\psi_2.
   $$

   Tunjukkan bahwa terdapat tepat satu pemetaan $\psi:T\to L_1\times_M L_2$
   yang proyeksinya ke $L_1$ dan $L_2$ masing-masing sama dengan
   $\psi_1$ dan $\psi_2$.

<!-- upstream_entity: Topologische Räume/Relatives Produkt/Aufgabe -->

## Soal 6.15 {#br-bgk-2019-w06-ex15}

Misalkan $L_1,L_2,M$ ruang topologis dan $p_1:L_1\to M$ serta
$p_2:L_2\to M$ pemetaan kontinu. Definisikan

$$
L_1\times_M L_2
:=\{(x_1,x_2)\mid p_1(x_1)=p_2(x_2)\}
\subseteq L_1\times L_2
$$

dengan topologi terinduksi.

1. Tunjukkan bahwa terdapat diagram komutatif dengan pemetaan-pemetaan
   kontinu,

   $$
   \begin{matrix}
   L_1\times_M L_2&\longrightarrow&L_1\\
   \downarrow&&\downarrow\\
   L_2&\longrightarrow&M
   \end{matrix}
   $$

2. Misalkan $T$ sebuah ruang topologis lain dan $\psi_1:T\to L_1$ serta
   $\psi_2:T\to L_2$ pemetaan kontinu dengan

   $$
   p_1\circ\psi_1=p_2\circ\psi_2.
   $$

   Tunjukkan bahwa terdapat tepat satu pemetaan kontinu
   $\psi:T\to L_1\times_M L_2$ yang proyeksinya ke $L_1$ dan $L_2$ masing-masing
   sama dengan $\psi_1$ dan $\psi_2$.

> **Catatan edisi - tata bahasa sumber.** Sumber mencetak frasa Jerman
> *eine weiterer topologischer Raum* (artikel dan adjektiva tidak selaras).
> Terjemahan memakai bentuk Indonesia “ruang topologis lain” tanpa mengubah
> isi matematis.

> **Catatan edisi - notasi produk serat pada sumber.** Pada beberapa
> tampilan sumber, syarat kesamaan ditulis dengan simbol $\varphi_1,\varphi_2$
> walaupun pemetaan yang baru saja didefinisikan bernama $p_1,p_2$. Terjemahan
> memakai $p_1,p_2$ secara konsisten dan mempertahankan objek matematis yang
> dimaksud.

<!-- upstream_entity: Topologische Räume/Vektorbündel/Rückzug/Aufgabe -->

## Soal 6.16 {#br-bgk-2019-w06-ex16}

Misalkan $X$ dan $Y$ ruang topologis, $\varphi:Y\to X$ pemetaan kontinu, dan
$p:V\to X$ sebuah bundel vektor di atas $X$. Buktikan bahwa

$$
Y\times_XV
$$

(lihat Soal 6.15) merupakan bundel vektor di atas $Y$.

<!-- upstream_entity: Topologischer Raum/Vektorbündel/Summe/Produktrealisierung/Aufgabe -->

## Soal 6.17 {#br-bgk-2019-w06-ex17}

Misalkan $X$ sebuah ruang topologis dan $p:V\to X$, $q:W\to X$ bundel-bundel
vektor di atas $X$. Buktikan bahwa

$$
V\times_XW
$$

(lihat Soal 6.15) merupakan bundel vektor di atas $X$ yang sama dengan jumlah
langsung bundel-bundel vektor di atas $X$.

<!-- upstream_entity: Topologische Räume/Relatives Produkt/Schnitt/Charakterisierung/Aufgabe -->

## Soal 6.18 {#br-bgk-2019-w06-ex18}

Misalkan $X,Y,Z$ ruang topologis, serta $\varphi:Y\to X$ dan $p:Z\to X$
pemetaan kontinu. Misalkan

$$
p_Y:Y\times_XZ\longrightarrow Y
$$

proyeksi alami. Tunjukkan bahwa seksi kontinu

$$
s:Y\longrightarrow Y\times_XZ
$$

sama dengan pemetaan kontinu $t:Y\to Z$ yang memenuhi

$$
p\circ t=\varphi.
$$

<!-- upstream_entity: Topologische Räume/Relatives Produkt/Rückzug/Schnitte/Aufgabe -->

## Soal 6.19 {#br-bgk-2019-w06-ex19}

Misalkan $X,Y,Z$ ruang topologis, serta $\varphi:Y\to X$ dan $p:Z\to X$
pemetaan kontinu. Misalkan $p_Y:Y\times_XZ\to Y$ proyeksi alami. Misalkan
$\mathcal G$ berkas seksi kontinu yang bersesuaian dengan $p$ di atas $X$.
Tunjukkan bahwa tarik balik $\varphi^*\mathcal G$ sama dengan berkas seksi
yang bersesuaian dengan $p_Y$.
