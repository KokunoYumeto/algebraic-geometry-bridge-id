---
title: "Solusi Publik dan Cakupan Lembar Kerja 5"
stable_id: br-bgk-2019-w05-solutions
language: id-ID
source_course: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)"
source_author: "Holger Brenner"
upstream_map: authority/wikiversity-bgk/unit-05/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: b6bf28ef883ac91c07d0c50526ff655b2bcf7fc1b0d45773f0543092d463cadf
authority_manifest: authority/wikiversity-bgk/unit-05/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 328774ffd66341ba8841b86935037a043067202dd10916d3e0be5082faeac35e
candidate_evidence: authority/wikiversity-bgk/unit-05/worksheet-solution-candidates-api.json
candidate_evidence_sha256: 8b7b0d65fa6670632c96c8ab95b48b732576ebc3db80007ce281c78fb9875d51
solution_ex05_xml: authority/wikiversity-bgk/unit-05/solution-ex05.xml
solution_ex05_xml_sha256: 95fa2f0799fb9bfbfe0d9475a42c061ea805618e25e31560a6004da4672c5c86
solution_ex05_html: authority/wikiversity-bgk/unit-05/solution-ex05.html
solution_ex05_html_sha256: 04c72e340da0acd5220449d60b5bc1d18e30d2808f549600b5288910de26d406
solution_ex05_upstream_title: "Garbe/Untergarbe/Halmweise Zugehörigkeit/Aufgabe/Lösung"
solution_ex05_upstream_pageid: 116432
solution_ex05_upstream_revid: 1112696
solution_ex05_upstream_timestamp: "2026-08-21T16:35:52Z"
solution_ex05_mediawiki_sha1: 0d2b14ff95268801b6ec1fdea9771b8e505725c8
solution_ex05_source_url: "https://de.wikiversity.org/w/index.php?oldid=1112696"
solution_ex05_frozen_revision_contributor: "Bocardodarapti"
exercise_count: 11
public_solution_count: 1
public_solution_numbers: "5"
negative_public_solution_count: 10
negative_solution_numbers: "1-4, 6-11"
license: "Frozen semantic course text and this translation: CC BY-SA 4.0."
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra."
---

```{=latex}
\clearpage
```

# Solusi Publik dan Cakupan Lembar Kerja 5 {#br-bgk-2019-w05-solutions}

Pada batas revisi yang dibekukan, sumber menyediakan tepat satu solusi
publik di antara sebelas soal pada Lembar Kerja 5, yaitu solusi Soal 5.5.
Peta soal dan bukti kandidat yang dibekukan mencatat hasil negatif untuk
Soal 5.1-5.4 dan 5.6-5.11. Tidak ada solusi baru yang dibuat untuk edisi ini.

## Solusi sumber untuk Soal 5.5 {#br-bgk-2019-w05-ex05-solution}

Keanggotaan pada tangkai

$$
t_P\in\mathcal F_P
$$

berarti bahwa terdapat lingkungan terbuka

$$
P\in U_P
$$

dan sebuah seksi

$$
s_P\in\mathcal F(U_P)\subseteq\mathcal G(U_P)
$$

yang germnya di $P$ sama dengan $t_P$. Dengan demikian, terdapat lingkungan
terbuka yang lebih kecil

$$
P\in V_P\subseteq U_P
$$

sedemikian sehingga restriksi $t$ dan $s_P$, dipandang sebagai seksi-seksi
$\mathcal G$, berimpit pada $V_P$.

Jadi terdapat penutup terbuka

$$
X=\bigcup_{i\in I}V_i
$$

sedemikian sehingga

$$
t|_{V_i}\in\mathcal F(V_i)\subseteq\mathcal G(V_i).
$$

Seksi-seksi ini kompatibel, baik sebagai seksi $\mathcal G$ maupun sebagai
seksi $\mathcal F$. Oleh karena itu, terdapat sebuah seksi

$$
s\in\mathcal F(X)
$$

yang restriksinya pada setiap $V_i$ adalah $t|_{V_i}$. Karena sebuah
keluarga kompatibel dalam suatu berkas mempunyai tepat satu realisasi
global, berlaku

$$
s=t
$$

di $\mathcal G(X)$. Dengan demikian,

$$
t\in\mathcal F(X).
$$

> **Catatan edisi - seksi dan germ.** Sumber menyatakan bahwa seksi lokal
> “membatasi ke” germ $t_P$. Secara tepat, germ $s_{P}$ dari seksi lokal
> $s_P$ di titik $P$ sama dengan $t_P$; terjemahan memakai hubungan berjenis
> ini tanpa mengubah argumen.

[Kembali ke Soal 5.5](#br-bgk-2019-w05-ex05).
