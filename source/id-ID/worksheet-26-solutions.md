---
title: "Solusi Publik Lembar Kerja 26"
stable_id: br-ak-2012-w26-solutions
language: id-ID
source_course: "Algebraische Kurven (Osnabrück 2012)"
source_author: "Holger Brenner"
frozen_revision_contributors: "Soal 26.4: Bocardodarapti"
upstream_map: authority/wikiversity/unit-26/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: efa1d77d8b594a24078097f3595c0ae8078d9735dfe7d2b3abb05392d7340423
authority_manifest: authority/wikiversity/unit-26/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 981fa3c86534514215c722b6d4f6d711c040a7829465f20ae18940373f94763c
public_solution_count: 1
upstream_solution_revisions: "Soal 26.4=1112503"
solution_xml_sha256: "04=d80e1ff03f562cdde8bfc9776ff56a7d1dfd364cf2c819d9d3187a5e91528ec0"
license: "CC BY-SA 4.0 for the frozen semantic source; official 2012 PDF witnesses retain their recorded CC BY-SA 2.0 Germany notice"
no_blanket_relicensing_claim: true
independent_derivative_non_endorsement: true
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_corrections: 1
correction_ids: "AGC-CORR-0102"
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 26 {#br-ak-2012-w26-solutions}

Pada batas revisi yang dibekukan, sumber hanya menyediakan solusi publik
untuk Soal 26.4. Sepuluh calon halaman solusi lainnya dinyatakan tidak ada
oleh kueri otoritas yang dibekukan. Tidak ada solusi tambahan yang dibuat
untuk edisi ini.

<!-- upstream_solution: Kartesisches Blatt/Schnittmultiplizität im Nullpunkt/Mit jeder Geraden/Aufgabe/Lösung; pageid=21344; revid=1112503 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1112503 -->

## Solusi Soal 26.4 {#br-ak-2012-w26-sol-04}

Jika sebuah garis tidak melalui titik asal, multiplisitas perpotongannya
dengan folium di titik asal adalah nol. Jadi cukup tinjau garis-garis melalui
titik asal. Semua garis itu dapat ditulis sebagai

$$
V(Y-aX),\qquad a\in K,
$$

atau sebagai garis vertikal $V(X)$.

Untuk $a=0$, yaitu garis $V(Y)$, gelanggang hasil baginya adalah

$$
\begin{aligned}
K[X,Y]_{(X,Y)}/(Y,X^3+Y^3-3XY)
&\cong K[X]_{(X)}/(X^3).
\end{aligned}
$$

Gelanggang ini berdimensi $3$ atas $K$, sehingga multiplisitas
perpotongannya adalah $3$. Karena persamaan folium simetris dalam $X$ dan
$Y$, hasil yang sama berlaku bagi garis $V(X)$.

Sekarang ambil garis $V(Y-aX)$ dengan $a\ne0$. Maka

$$
\begin{aligned}
K[X,Y]_{(X,Y)}/(Y-aX,X^3+Y^3-3XY)
&\cong K[X]_{(X)}/(X^3+a^3X^3-3aX^2)\\
&=K[X]_{(X)}/\left(X^2\bigl(-3a+(1+a^3)X\bigr)\right).
\end{aligned}
$$

Karena $\operatorname{char}(K)\ne3$ dan $a\ne0$, faktor

$$
-3a+(1+a^3)X
$$

merupakan unit di $K[X]_{(X)}$. Jadi gelanggang hasil bagi tersebut isomorfik
dengan

$$
K[X]_{(X)}/(X^2),
$$

yang berdimensi $2$. Dengan demikian, garis $V(X)$ dan $V(Y)$ mempunyai
multiplisitas perpotongan $3$ di titik asal, sedangkan setiap garis lain yang
melalui titik asal mempunyai multiplisitas perpotongan $2$.

> **Catatan edisi - daftar garis melalui titik asal.** Sumber menyatakan
> bahwa garis-garis tersebut berbentuk $V(Y-aX)$ atau $V(Y)$, sehingga
> $V(Y)$ disebut dua kali dan garis vertikal $V(X)$ tidak tercakup. Langkah
> berikutnya dalam sumber sendiri menangani $V(X)$ dengan simetri. Edisi
> memulihkan daftar yang dimaksud: $V(Y-aX)$ untuk $a\in K$, ditambah
> $V(X)$.

[Kembali ke Soal 26.4](#br-ak-2012-w26-ex-04)
