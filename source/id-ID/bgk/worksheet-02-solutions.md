---
title: "Solusi Publik Lembar Kerja 2"
stable_id: br-bgk-2019-w02-solutions
language: id-ID
source_course: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)"
source_author: "Holger Brenner"
upstream_map: authority/wikiversity-bgk/unit-02/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: 4e0633e8c35ea5a2fddd0b63a0bb67fdd6af93f11a55f3a2eae10eae0d25a10a
authority_manifest: authority/wikiversity-bgk/unit-02/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: a348b56811fe98266feff9108a21a436a9b8f07a343321feab7d9fbb3b75e64d
candidate_evidence: authority/wikiversity-bgk/unit-02/worksheet-solution-candidates-api.json
candidate_evidence_sha256: 5051d800bed72fe432757012033319ca30c14503254f16d0d385f9a0a3c82ad2
solution_ex04_xml: authority/wikiversity-bgk/unit-02/solution-ex04.xml
solution_ex04_xml_sha256: 6f326a59a4289d17ac6aee485706faa81d641d994ddda72bd463053eec4b71b1
solution_ex04_html: authority/wikiversity-bgk/unit-02/solution-ex04.html
solution_ex04_html_sha256: 8cf7b19c9693b1817e5699b32703545716fb35dfa713b9f6129758dbe0bf0e7f
solution_ex04_upstream_title: "Stetiges Vektorfeld/S^2/Nur eine Nullstelle/Aufgabe/Lösung"
solution_ex04_upstream_pageid: 77727
solution_ex04_upstream_revid: 1096699
solution_ex04_upstream_timestamp: "2026-06-15T09:32:35Z"
solution_ex04_upstream_mediawiki_sha1: 64a726dc965e322b03e5eb0797f109cb45ab5125
solution_ex04_source_url: "https://de.wikiversity.org/w/index.php?oldid=1096699"
solution_ex04_frozen_revision_contributor: "Arbota"
exercise_count: 27
public_solution_count: 1
public_solution_numbers: "4"
negative_public_solution_count: 26
negative_solution_numbers: "1-3, 5-27"
license: "Frozen semantic course text and this translation: CC BY-SA 4.0."
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: source_scope_complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra."
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 2 {#br-bgk-2019-w02-solutions}

Pada batas otoritas yang dibekukan, sumber menyediakan tepat satu solusi
publik di antara 27 soal pada Lembar Kerja 2, yaitu solusi Soal 2.4. Peta
soal yang dibekukan mencatat hasil negatif untuk Soal 2.1-2.3 dan 2.5-2.27.
Tidak ada solusi baru yang dibuat untuk edisi ini.

## Solusi sumber untuk Soal 2.4 {#br-bgk-2019-w02-ex04-solution}

Pada $\mathbb R^2$, perhatikan medan vektor kontinu $F$ yang diberikan oleh

$$
F(x,y)=\frac{1}{1+x^2+y^2}e_1.
$$

Medan ini tidak mempunyai titik nol dan kontinu. Kita pindahkan medan vektor
ini melalui proyeksi stereografis ke

$$
\mathbb R^2\cong S^2\setminus\{N\}
$$

dan melengkapinya di kutub utara dengan nilai

$$
0\in T_NS^2.
$$

Kita klaim bahwa medan vektor tersebut kontinu. Untuk itu, misalkan $(P_n)$
sebuah barisan pada $S^2$ yang konvergen ke $N$. Kita dapat langsung
mengasumsikan bahwa $P_n\ne N$ untuk semua $n$. Citra barisan itu dalam
bagan ialah

$$
P_n'=(x_n,y_n).
$$

Karena $P_n$ konvergen ke kutub utara, $\lVert P_n'\rVert$ divergen ke
$\infty$. Karena itu, barisan

$$
F(P_n')=F(x_n,y_n)
=\frac{1}{1+x_n^2+y_n^2}e_1
$$

konvergen ke $0$.

> **Catatan edisi - formula sumber tidak terdefinisi di titik asal.**
> Sumber membentuk $F$ pada seluruh $\mathbb R^2$ dengan
> $F(x,y)=(x^2+y^2)^{-1}e_1$, tetapi rumus ini tidak terdefinisi pada
> $(0,0)$. Jadi klaim bahwa $F$ kontinu dan taknol pada seluruh bidang tidak
> benar sebagaimana tercetak. Edisi menampilkan perbaikan minimal
> $F(x,y)=(1+x^2+y^2)^{-1}e_1$: fungsi ini kontinu dan taknol pada seluruh
> $\mathbb R^2$, menuju $0$ ketika $\lVert(x,y)\rVert\to\infty$, dan
> setelah didorong maju oleh invers proyeksi stereografis juga menuju vektor
> nol di kutub utara (diferensial invers proyeksi itu tetap terbatas dan
> bahkan meluruh di tak berhingga). Dengan demikian, perubahan tersebut
> memperbaiki cacat lokal tanpa mengubah struktur argumen sumber; bentuk
> sumber dipertahankan di catatan ini. Pada baris limit, sumber juga mencetak
> $x,y$ tanpa subskrip; edisi menampilkan $x_n,y_n$ sesuai barisan yang baru
> saja didefinisikan. Sumber juga menggandakan kata kerja *sei* dalam kalimat
> yang memperkenalkan barisan $(P_n)$; pengulangan tipografis itu dihilangkan
> dalam terjemahan dan dicatat di sini.
