---
title: "Lembar Kerja 5 - Berkasisasi dan Berkas Hasil Bagi"
stable_id: br-bgk-2019-w05
language: id-ID
source_course: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)"
source_author: "Holger Brenner"
frozen_revision_contributor: "Bocardodarapti"
upstream_title: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)/Arbeitsblatt 5"
upstream_pageid: 110210
upstream_revid: 619386
upstream_timestamp: "2020-02-17T12:38:11Z"
upstream_mediawiki_sha1: 7ea9208cb3444aa48e23d1acbe66e27672d28d27
source_url: "https://de.wikiversity.org/w/index.php?oldid=619386"
authority_manifest: authority/wikiversity-bgk/unit-05/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 328774ffd66341ba8841b86935037a043067202dd10916d3e0be5082faeac35e
worksheet_xml: authority/wikiversity-bgk/unit-05/worksheet-05.xml
worksheet_xml_sha256: 89e545b88502d4e9f4bd19c8ca79a68cf86a480aca360f4d0c3740589366a7f5
worksheet_expanded_tex: authority/wikiversity-bgk/unit-05/worksheet-05-expanded.tex
worksheet_expanded_tex_sha256: af4235ab3c393b02ad8f081f8f8fb17c24067fa07af63ec7f9bb3f17e1526b86
exercise_map: authority/wikiversity-bgk/unit-05/ORDERED_EXERCISE_MAP.json
exercise_map_sha256: b6bf28ef883ac91c07d0c50526ff655b2bcf7fc1b0d45773f0543092d463cadf
official_pdf: authority/artifacts/bgk-worksheet-05-official.pdf
official_pdf_sha256: 206418f092c563128b3dbf893b8547dc6db727773d4e4ec88e07140886d79113
license: "Frozen semantic course text and this translation: CC BY-SA 4.0. Official PDF witnesses retain their recorded component notices; no blanket relicensing claim is made."
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra."
exercise_count: 11
public_solution_count: 1
---

# Lembar Kerja 5: Berkasisasi dan Berkas Hasil Bagi {#br-bgk-2019-w05}

<!-- upstream_entity: Prägarbe/Diskretisierung/Aufgabe -->

## Soal 5.1 {#br-bgk-2019-w05-ex01}

Misalkan $X$ sebuah ruang topologis dan $\mathcal F$ sebuah praberkas pada
$X$. Tunjukkan bahwa penetapan

$$
U\longmapsto\prod_{P\in U}\mathcal F_P,
$$

yakni himpunan produk semua tangkai di titik-titik $U$, bersama proyeksi
alami sebagai pemetaan restriksi, mendefinisikan sebuah praberkas.
Tunjukkan pula bahwa terdapat morfisme praberkas alami dari $\mathcal F$
ke praberkas tersebut.

<!-- upstream_entity: Prägarbe/Vergarbung/Universelle Eigenschaft/Aufgabe -->

## Soal 5.2 {#br-bgk-2019-w05-ex02}

Misalkan $\mathcal F$ sebuah praberkas pada ruang topologis $X$, dan
misalkan $\widetilde{\mathcal F}$ berkasisasinya. Tunjukkan bahwa, untuk
setiap morfisme praberkas

$$
\psi:\mathcal F\longrightarrow\mathcal G
$$

ke sebuah berkas $\mathcal G$, terdapat tepat satu faktorisasi

$$
\widetilde\psi:
\widetilde{\mathcal F}\longrightarrow\mathcal G.
$$

Berkasisasi sebuah praberkas konstan disebut *berkas konstan lokal*, dan
kadang-kadang juga disebut cukup sebagai *berkas konstan*.

<!-- upstream_entity: Konstante Prägarbe/Vergarbung/Halm/Aufgabe -->

## Soal 5.3 {#br-bgk-2019-w05-ex03}

Misalkan $\mathcal F$ praberkas konstan bernilai suatu himpunan $M$ pada
ruang topologis $X$. Tunjukkan bahwa tangkai berkasisasi $\mathcal F$ di
setiap titik

$$
P\in X
$$

sama dengan $M$.

<!-- upstream_entity: Konstante Prägarbe/Diskrete Gruppe/Vergarbung/Aufgabe -->

## Soal 5.4 {#br-bgk-2019-w05-ex04}

Misalkan $G$ sebuah grup topologis diskret dan $X$ sebuah ruang topologis.
Misalkan $\mathcal G$ praberkas konstan bernilai $G$ pada $X$. Tunjukkan
bahwa berkasisasi $\mathcal G$ sama dengan

$$
C^0(-,G).
$$

<!-- upstream_entity: Garbe/Untergarbe/Halmweise Zugehörigkeit/Aufgabe -->

## Soal 5.5* {#br-bgk-2019-w05-ex05}

Misalkan $X$ sebuah ruang topologis, $\mathcal G$ sebuah berkas pada $X$,
dan

$$
\mathcal F\subseteq\mathcal G
$$

sebuah subberkas. Misalkan

$$
t\in\Gamma(X,\mathcal G)
$$

memenuhi

$$
t_P\in\mathcal F_P
$$

untuk setiap

$$
P\in X.
$$

Tunjukkan bahwa

$$
t\in\Gamma(X,\mathcal F).
$$

<!-- upstream_entity: Garben von Gruppen/Homomorphismus/Kern/Garbe/Aufgabe -->

## Soal 5.6 {#br-bgk-2019-w05-ex06}

Misalkan $X$ sebuah ruang topologis dan

$$
\varphi:\mathcal F\longrightarrow\mathcal G
$$

sebuah homomorfisme berkas grup komutatif. Tunjukkan bahwa penetapan

$$
(\ker\varphi)(U):=\ker\varphi_U
$$

mendefinisikan sebuah berkas grup pada $X$.

<!-- upstream_entity: Garben von Gruppen/Homomorphismus/Injektiv und Kern/Aufgabe -->

## Soal 5.7 {#br-bgk-2019-w05-ex07}

Misalkan $X$ sebuah ruang topologis dan

$$
\varphi:\mathcal F\longrightarrow\mathcal G
$$

sebuah homomorfisme berkas grup komutatif. Tunjukkan bahwa $\varphi$
injektif tepat ketika

$$
\ker\varphi
$$

merupakan berkas nol.

<!-- upstream_entity: Garben von Gruppen/Homomorphismus/Surjektiv und Bild/Aufgabe -->

## Soal 5.8 {#br-bgk-2019-w05-ex08}

Misalkan $X$ sebuah ruang topologis dan

$$
\varphi:\mathcal F\longrightarrow\mathcal G
$$

sebuah homomorfisme berkas grup komutatif. Tunjukkan bahwa $\varphi$
surjektif tepat ketika

$$
\operatorname{im}\varphi=\mathcal G.
$$

<!-- upstream_entity: Garben von Gruppen/Homomorphismus/Bild/Halm/Aufgabe -->

## Soal 5.9 {#br-bgk-2019-w05-ex09}

Misalkan $X$ sebuah ruang topologis dan

$$
\varphi:\mathcal F\longrightarrow\mathcal G
$$

sebuah homomorfisme berkas grup komutatif. Tunjukkan bahwa, untuk setiap

$$
P\in X,
$$

berlaku

$$
(\operatorname{im}\varphi)_P
=
\operatorname{im}(\varphi_P).
$$

<!-- upstream_entity: Garben von Gruppen/Untergarbe/Quotientengarbe/Surjektiv/Aufgabe -->

## Soal 5.10 {#br-bgk-2019-w05-ex10}

Misalkan $\mathcal G$ sebuah berkas grup komutatif dan

$$
\mathcal F\subseteq\mathcal G
$$

sebuah subberkas grup. Tunjukkan bahwa terdapat homomorfisme berkas grup
komutatif yang kanonik dan surjektif

$$
\mathcal G\longrightarrow\mathcal G/\mathcal F.
$$

<!-- upstream_entity: Garben von Gruppen/Untergarbe/Quotientengarbe/Halm/Aufgabe -->

## Soal 5.11 {#br-bgk-2019-w05-ex11}

Misalkan $\mathcal G$ sebuah berkas grup komutatif dan

$$
\mathcal F\subseteq\mathcal G
$$

sebuah subberkas grup, dan misalkan $\mathcal G/\mathcal F$ berkas hasil
baginya. Tunjukkan bahwa

$$
(\mathcal G/\mathcal F)_P
=
\mathcal G_P/\mathcal F_P
$$

untuk setiap titik

$$
P\in X.
$$
