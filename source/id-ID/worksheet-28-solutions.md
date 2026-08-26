---
title: "Solusi Publik Lembar Kerja 28"
stable_id: br-ak-2012-w28-solutions
language: id-ID
source_course: "Algebraische Kurven (Osnabrück 2012)"
source_author: "Holger Brenner"
frozen_revision_contributors: "Soal 28.10: Bocardodarapti"
upstream_map: authority/wikiversity/unit-28/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: c5aed5500f44a39bbe0a7a079792e0da11781a24a69c274d7170b0e2cdc1df40
authority_manifest: authority/wikiversity/unit-28/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: f2e34fc420c4beec300ea9e0accc52598e12c27f46c9022611996b1b43e29a99
public_solution_count: 1
negative_public_solution_count: 13
upstream_solution_revisions: "Soal 28.10=1112869"
solution_xml_sha256: "10=b0ed23c137883f7304b18304e06b5fa5e02cce5ae81b966a5e23c428d84497be"
license: "CC BY-SA 4.0 for the frozen semantic source; official 2012 PDF witnesses retain their recorded CC BY-SA 2.0 Germany notice"
no_blanket_relicensing_claim: true
independent_derivative_non_endorsement: true
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_corrections: 1
correction_ids: "AGC-CORR-0122"
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 28 {#br-ak-2012-w28-solutions}

Pada batas revisi yang dibekukan, sumber hanya menyediakan solusi publik
untuk Soal 28.10. Tiga belas calon halaman solusi lainnya dinyatakan tidak
ada oleh kueri otoritas yang dibekukan. Tidak ada solusi tambahan yang dibuat
untuk edisi ini.

<!-- upstream_solution: Ebene Kurve/y-x^3+x+2/Rationale Parametrisierung/Fortsetzung auf P^1/Aufgabe/Lösung; pageid=21591; revid=1112869 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1112869 -->

## Solusi Soal 28.10 {#br-ak-2012-w28-sol-10}

Suatu isomorfisme diberikan oleh

$$
x\longmapsto(x,x^3-x-2)=(x,y).
$$

Pada tingkat gelanggang, pemetaan ini bersesuaian dengan homomorfisme
substitusi

$$
\begin{aligned}
K[X,Y]/(Y-X^3+X+2)&\longrightarrow K[X],\\
X&\longmapsto X,\\
Y&\longmapsto X^3-X-2.
\end{aligned}
$$

Homomorfisme itu terdefinisi dengan baik dan surjektif. Karena $Y$ dapat
dieliminasi langsung di ruas kiri, gelanggang sumber isomorfik dengan
$K[X]$. Jadi pemetaan tersebut memang suatu isomorfisme kurva afin.

Isomorfisme ini tidak dapat diperluas menjadi isomorfisme dengan garis
proyektif. Penutupan proyektif kurva adalah

$$
\overline C
=
V_+(YZ^2-X^3+XZ^2+2Z^3).
$$

Tepat satu titik di tak hingga ditambahkan, yaitu $(0,1,0)$. Pada lingkungan
afin $D_+(Y)$, titik itu menjadi titik asal kurva afin

$$
V(Z^2-X^3+XZ^2+2Z^3).
$$

Titik asal mempunyai multiplisitas dua dan karena itu tidak mulus.

> **Jembatan edisi.** Suku berderajat terendah $Z^2$ menjelaskan
> multiplisitas dua tersebut. Karena garis proyektif mulus, $\overline C$
> tidak isomorfik dengan $\mathbb P_K^1$.

> **Catatan edisi - kesesuaian tunggal-jamak.** Sumber menulis bentuk
> gramatikal yang menyebut "titik-titik" tetapi kemudian memberikan tepat
> satu titik $(0,1,0)$. Persamaan homogen juga menunjukkan hanya titik itu.
> Edisi menerjemahkan makna matematis yang konsisten: tepat satu titik di tak
> hingga.
