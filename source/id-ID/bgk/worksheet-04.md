---
title: "Lembar Kerja 4 - Berkas dan Morfisme Berkas"
stable_id: br-bgk-2019-w04
language: id-ID
source_course: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)"
source_author: "Holger Brenner"
frozen_revision_contributor: "Bocardodarapti"
upstream_title: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)/Arbeitsblatt 4"
upstream_pageid: 110209
upstream_revid: 1003857
upstream_timestamp: "2025-06-10T09:15:51Z"
upstream_mediawiki_sha1: 879b20dfad7b078a205c00bf5e341035b8307f8e
source_url: "https://de.wikiversity.org/w/index.php?oldid=1003857"
authority_manifest: authority/wikiversity-bgk/unit-04/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 3f26616ff7e9f4ac0d5bb0e64ad8435fefc18e32e4c91b16d780d4346498f680
worksheet_xml: authority/wikiversity-bgk/unit-04/worksheet-04.xml
worksheet_xml_sha256: 3e205caf77b5388ff6a0aa2bb1fa3643e354ce4ccc7e5e19d2dc7f6e29daca8a
worksheet_expanded_tex: authority/wikiversity-bgk/unit-04/worksheet-04-expanded.tex
worksheet_expanded_tex_sha256: 7af2dce83605791269ba4fc1d5351100411b0a8081920cce8f1241724249f974
exercise_map: authority/wikiversity-bgk/unit-04/ORDERED_EXERCISE_MAP.json
exercise_map_sha256: a53d958595d6fd0aac34f8ea6562204dda96b44a375e68b33d93d92e63485dcf
official_pdf: authority/artifacts/bgk-worksheet-04-official.pdf
official_pdf_sha256: 082b49c71d075c7bd137ff66ce20d1ec3a76fe2368e1a2c2f0141e774e270ed9
license: "Frozen semantic course text and this translation: CC BY-SA 4.0. Official PDF witnesses retain their recorded component notices; no blanket relicensing claim is made."
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra."
exercise_count: 9
public_solution_count: 0
---

# Lembar Kerja 4: Berkas dan Morfisme Berkas {#br-bgk-2019-w04}

<!-- upstream_entity: Garbe/Produkt/Aufgabe -->

## Soal 4.1 {#br-bgk-2019-w04-ex01}

Misalkan $\mathcal F$ dan $\mathcal G$ berkas pada ruang topologis $X$.
Tunjukkan bahwa penetapan

$$
U\longmapsto\mathcal F(U)\times\mathcal G(U),
$$

bersama pemetaan produk alami sebagai pemetaan restriksi, mendefinisikan
sebuah berkas pada $X$.

<!-- upstream_entity: Garbe/Unzusammenhängender Raum/Produkt/Aufgabe -->

## Soal 4.2 {#br-bgk-2019-w04-ex02}

Misalkan $\mathcal G$ sebuah berkas pada ruang tak terhubung $X$ yang
mempunyai dekomposisi

$$
X=U\mathbin{\uplus}V
$$

menjadi dua himpunan terbuka tak kosong yang saling lepas. Tunjukkan bahwa

$$
\mathcal G(X)=\mathcal G(U)\times\mathcal G(V).
$$

<!-- upstream_entity: Topologischer Raum/Disjunkte offene Vereinigung/Garben/Aufgabe -->

## Soal 4.3 {#br-bgk-2019-w04-ex03}

Misalkan $X$ sebuah ruang topologis dengan dekomposisi

$$
X=Y\mathbin{\uplus}Z
$$

menjadi dua subhimpunan terbuka tak kosong yang saling lepas. Misalkan
$\mathcal G$ sebuah berkas pada $Y$ dan $\mathcal H$ sebuah berkas pada
$Z$. Tunjukkan bahwa, untuk setiap himpunan terbuka $U\subseteq X$,
penetapan

$$
\mathcal F(U)
=\mathcal G(U\cap Y)\times\mathcal H(U\cap Z)
$$

mendefinisikan sebuah berkas $\mathcal F$ pada $X$.

<!-- upstream_entity: Hausdorffraum/Konstante Prägarbe/Keine Garbe/Aufgabe -->

## Soal 4.4 {#br-bgk-2019-w04-ex04}

Misalkan $X$ sebuah ruang Hausdorff dengan sekurang-kurangnya dua titik dan
misalkan $M$ sebuah himpunan dengan sekurang-kurangnya dua unsur. Tunjukkan
bahwa praberkas konstan yang bernilai $M$ bukan sebuah berkas.

> **Catatan edisi - hipotesis sumber tidak cukup kuat.** Sumber hanya
> mengasumsikan $M\ne\varnothing$. Kesimpulannya salah jika $M$ berunsur
> tunggal, sebab praberkas konstan bernilai satu unsur memenuhi kedua syarat
> berkas. Edisi menyatakan hipotesis yang dimaksud, yaitu bahwa $M$
> mempunyai sekurang-kurangnya dua unsur.

<!-- upstream_entity: Garbe/Einschränkung/Garbe/Aufgabe -->

## Soal 4.5 {#br-bgk-2019-w04-ex05}

Tunjukkan bahwa pembatasan sebuah berkas ke suatu subhimpunan terbuka

$$
U\subseteq X
$$

merupakan sebuah berkas.

<!-- upstream_entity: C/Holomorphe Funktion/Keim/Potenzreihe/Aufgabe -->

## Soal 4.6 {#br-bgk-2019-w04-ex06}

Tunjukkan bahwa tangkai di $0\in\mathbb C$ dari berkas fungsi holomorfik
isomorfik dengan gelanggang deret pangkat konvergen dalam satu variabel.

<!-- upstream_entity: Garbenmorphismus/Surjektiv/Halmweise surjektiv/Aufgabe -->

## Soal 4.7 {#br-bgk-2019-w04-ex07}

Misalkan

$$
\varphi:\mathcal F\longrightarrow\mathcal G
$$

sebuah morfisme berkas pada ruang topologis $X$. Andaikan

$$
\varphi_U:\mathcal F(U)\longrightarrow\mathcal G(U)
$$

surjektif untuk setiap himpunan terbuka $U\subseteq X$. Tunjukkan bahwa
setiap pemetaan tangkai

$$
\varphi_P:\mathcal F_P\longrightarrow\mathcal G_P
$$

juga surjektif.

<!-- upstream_entity: Garbe/Kommutative Gruppen/Leere Menge/Aufgabe -->

## Soal 4.8 {#br-bgk-2019-w04-ex08}

Misalkan $\mathcal G$ sebuah berkas grup komutatif pada ruang topologis $X$.
Tunjukkan bahwa

$$
\mathcal G(\varnothing)=0,
$$

yakni bahwa nilai berkas pada himpunan kosong adalah grup trivial.

<!-- upstream_entity: Wolkenkratzergarbe/Gruppe/Garbeneigenschaft/Aufgabe -->

## Soal 4.9 {#br-bgk-2019-w04-ex09}

Misalkan $X$ sebuah ruang topologis, $P\in X$ sebuah titik, dan $G$ sebuah
grup komutatif. Pertimbangkan penetapan

$$
U\longmapsto
\mathcal G(U):=
\begin{cases}
G,&\text{jika }P\in U,\\
0,&\text{jika }P\notin U,
\end{cases}
$$

dengan pemetaan restriksi yang wajar untuk setiap inklusi himpunan terbuka
$V\subseteq U$.

1. Tunjukkan bahwa $\mathcal G$ merupakan sebuah berkas grup komutatif.
2. Tentukan tangkai $\mathcal G_P$.
3. Sekarang andaikan $P$ sebuah titik tertutup. Tentukan tangkai
   $\mathcal G_Q$ untuk setiap titik $Q\ne P$.

> **Catatan edisi - dua salah ketik sumber.** Perintah terakhir pada sumber
> berbunyi *Besitmme die Halm*. Bentuk yang dimaksud ialah
> *Bestimme die Halme*, yaitu menentukan tangkai-tangkai pada semua titik
> $Q\ne P$.

Berkas yang dikonstruksi dalam soal di atas disebut *berkas pencakar
langit* dengan nilai $G$ di titik $P$.
