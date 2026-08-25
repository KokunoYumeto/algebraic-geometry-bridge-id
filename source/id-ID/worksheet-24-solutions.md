---
title: "Solusi Publik Lembar Kerja 24"
stable_id: br-ak-2012-w24-solutions
language: id-ID
source_course: "Algebraische Kurven (Osnabrück 2012)"
upstream_map: authority/wikiversity/unit-24/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: 250744d177bc2d5cf2a1cc506a99e05f1250c771de88b214a0e8d5cabfe7b9b8
authority_manifest: authority/wikiversity/unit-24/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 3731896a5980c565d9d69a2e01eee497f13b6f449f2f9c701fce726271c026a5
public_solution_count: 1
upstream_solution_revisions: "Soal 24.4=1068135"
solution_xml_sha256: "04=7904b98444817d81659d24fafd37e9009c39547c891bce705b0ae4b37f0ec527"
license: "CC BY-SA 4.0 for the frozen semantic source; official 2012 PDF witnesses retain their recorded CC BY-SA 2.0 Germany notice"
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_corrections: 1
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 24 {#br-ak-2012-w24-solutions}

Pada batas revisi yang dibekukan, sumber hanya menyediakan solusi publik
untuk Soal 24.4. Tidak ada solusi tambahan yang dibuat untuk edisi ini.

<!-- upstream_solution: Potenzreihenring eine Variable/Abbildung der Lokalisierung an maximalen Ideal/Aufgabe/Lösung; pageid=168447; revid=1068135 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1068135 -->

## Solusi Soal 24.4 {#br-ak-2012-w24-sol-04}

Kita mulai dengan homomorfisme aljabar-$K$

$$
\begin{aligned}
K[T]&\longrightarrow K[[T]],\\
T&\longmapsto T.
\end{aligned}
$$

Setiap polinom $P\in K[T]\setminus (T)$ mempunyai suku konstan

$$
P(0)\ne 0.
$$

Oleh kriteria satuan untuk gelanggang deret pangkat formal, $P$ merupakan
satuan di $K[[T]]$. Karena semua unsur himpunan penyebut
$K[T]\setminus (T)$ dipetakan ke satuan, sifat universal pelokalan memberikan
homomorfisme aljabar-$K$ yang tunggal

$$
K[T]_{(T)}\longrightarrow K[[T]].
$$

Secara eksplisit, pemetaan itu diberikan oleh

$$
\frac{f}{P}\longmapsto fP^{-1}.
$$

*Catatan edisi -- koreksi solusi sumber:* Setelah menyatakan
$P\notin (T)$, sumber hanya menampilkan simbol $\ne 0$ tanpa ruas kiri.
Edisi memulihkan pernyataan yang diperlukan, yaitu $P(0)\ne0$; kesalahan
ejaan Jerman yang tidak memengaruhi matematika juga diperbaiki secara alami
dalam terjemahan.

[Kembali ke Soal 24.4](#br-ak-2012-w24-ex-04)
