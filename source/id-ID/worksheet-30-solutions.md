---
title: "Solusi Publik Lembar Kerja 30"
stable_id: br-ak-2012-w30-solutions
language: id-ID
source_course: "Algebraische Kurven (Osnabrück 2012)"
source_author: "Holger Brenner"
frozen_revision_contributors: "Soal 30.3: Bocardodarapti; Soal 30.4: Arbota"
upstream_map: authority/wikiversity/unit-30/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: 7b6ed646202784b0ae03782e76e751336516d2dda0ed17ecf70500ea2d7a491e
authority_manifest: authority/wikiversity/unit-30/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 756ec1f9ea386b8ad0fac38086b6c97f0b94d6dc7a139dc4663911d48655bbe1
candidate_evidence: authority/wikiversity/unit-30/worksheet-solution-candidates-api.json
public_solution_count: 2
negative_public_solution_count: 10
negative_solution_numbers: "1, 2, 5-12"
upstream_solution_revisions: "Soal 30.3=1112942; Soal 30.4=1106652"
solution_xml_sha256: "3=2657d734224c0681b15fd19b6dd1284f704e27b0eb3397e4cf7f91065f43ebcb; 4=1eb565f3f8ca6acd72b53a130427c18b1ca957b804b9ab7463d826396f8e9bd1"
license: "CC BY-SA 4.0 for the frozen semantic source; official 2012 PDF witnesses retain the component notices recorded in the Unit 30 rights ledger"
no_blanket_relicensing_claim: true
independent_derivative_non_endorsement: true
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra."
source_corrections: 2
correction_ids: "AGC-CORR-0134; AGC-CORR-0135"
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 30 {#br-ak-2012-w30-solutions}

Pada batas revisi yang dibekukan, sumber hanya menyediakan solusi publik
untuk Soal 30.3 dan 30.4. Sepuluh calon halaman solusi lainnya dinyatakan
tidak ada oleh kueri otoritas yang dibekukan. Tidak ada solusi tambahan yang
dibuat untuk edisi ini.

<!-- upstream_solution: Ebene Kurven/Schnitt und Schnittmultiplizität/Y ist X^3 und Y^2 ist X^3/Aufgabe/Lösung; pageid=21320; revid=1112942 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1112942 -->

## Solusi Soal 30.3 {#br-ak-2012-w30-sol-03}

Titik-titik perpotongan kedua kurva pada bidang afin kompleks diberikan oleh

$$
V(Y-X^3,\,Y^2-X^3).
$$

Jadi, untuk suatu titik perpotongan $(x,y)$ harus berlaku

$$
y=x^3
\qquad\text{dan}\qquad
y^2=x^3.
$$

Dengan menyubstitusikan persamaan pertama ke dalam persamaan kedua, kita
memperoleh

$$
y(y-1)=0.
$$

Maka $y=0$ atau $y=1$. Dengan demikian titik-titik perpotongannya adalah

$$
\{(0,0),(1,1),(\zeta,1),(\zeta^2,1)\},
$$

dengan $\zeta$ suatu akar satuan ketiga primitif. Pada titik asal, gelanggang
faktornya ialah

$$
\begin{aligned}
\mathbb C[X,Y]_{(X,Y)}/(Y-X^3,Y^2-X^3)
&\cong \mathbb C[X]_{(X)}/(X^3,X^6-X^3)\\
&\cong \mathbb C[X]/(X^3).
\end{aligned}
$$

Dimensinya sebagai ruang vektor kompleks adalah $3$, sehingga multiplisitas
perpotongan di titik asal sama dengan $3$.

Untuk menentukan multiplisitas pada tiga titik lainnya, hitung gradien dalam
urutan koordinat konvensional $(X,Y)$. Untuk

$$
F=Y-X^3,
\qquad
G=Y^2-X^3,
$$

kita memperoleh

$$
\nabla F=(-3x^2,1)
\qquad\text{dan}\qquad
\nabla G=(-3x^2,2y)=(-3x^2,2).
$$

Karena $x\ne0$, kedua arah ini bebas linear. Jadi kedua kurva mulus dan
berpotongan secara transversal pada ketiga titik tersebut; masing-masing
mempunyai multiplisitas perpotongan $1$.

> **Koreksi sumber AGC-CORR-0134 - urutan komponen gradien.** Sumber menulis
> komponen turunan dalam urutan implisit $(Y,X)$ pada satu bagian solusi,
> berbeda dari konvensi $(X,Y)$ yang dipakai di bagian lain. Edisi menulis
> kedua gradien secara konsisten dalam urutan $(X,Y)$; uji transversality dan
> hasilnya tidak berubah.

Dalam ruang proyektif, kedua ideal dihomogenkan. Jadi kita perhatikan

$$
V_+(YZ^2-X^3)
\qquad\text{dan}\qquad
V_+(Y^2Z-X^3).
$$

Dengan menetapkan $Z=0$, kita memperoleh $X=0$, sehingga titik
perpotongan di tak hingga adalah $(0,1,0)$. Lingkungan afin $D_+(Y)$
memberikan persamaan

$$
Z^2-X^3
\qquad\text{dan}\qquad
Z-X^3.
$$

Pada titik asal dalam chart ini, eliminasi $Z$ kembali menghasilkan faktor
lokal berdimensi $3$. Maka multiplisitas perpotongan di titik tak hingga itu
juga $3$. Jumlah semua multiplisitas perpotongan adalah

$$
3+3\cdot1+3=9,
$$

sesuai dengan hasil kali derajat kedua kurva, yaitu $3\cdot3=9$.

<!-- upstream_solution: Ebene Kurven/Schnitt und Schnittmultiplizität/Y ist X^2 und Y^2 ist X^5/Aufgabe/Lösung; pageid=21596; revid=1106652 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1106652 -->

## Solusi Soal 30.4 {#br-ak-2012-w30-sol-04}

Dengan menjumlahkan kedua persamaan, kita langsung memperoleh syarat

$$
0=X-X^5=X(1-X^4).
$$

Jadi koordinat $x$ suatu titik perpotongan adalah $0$ atau suatu akar satuan
keempat,

$$
x\in\{0,1,-1,i,-i\}.
$$

Jika $x=0$, langsung diperoleh $y=0$. Gelanggang faktor lokalnya dapat
ditulis sebagai

$$
\begin{aligned}
\mathbb C[X,Y]_{(X,Y)}/(X-Y^2,Y^2-X^5)
&\cong \mathbb C[Y]_{(Y)}/(Y^2-Y^{10})\\
&=\mathbb C[Y]_{(Y)}/\bigl(Y^2(1-Y^8)\bigr)\\
&\cong \mathbb C[Y]_{(Y)}/(Y^2).
\end{aligned}
$$

Karena $1-Y^8$ adalah unit dalam gelanggang lokal tersebut, multiplisitas
perpotongan di $(0,0)$ sama dengan $2$.

> **Koreksi sumber AGC-CORR-0135 - indeks pelokalan.** Pada baris tengah,
> sumber mencetak $\mathbb C[Y]_Y$, yang biasanya berarti membalik pangkat
> $Y$ dan tidak dapat menjadi gelanggang lokal di titik asal. Edisi
> mempertahankan pelokalan yang ditetapkan pada baris sebelumnya,
> $\mathbb C[Y]_{(Y)}$, sehingga argumen unit dan panjang lokalnya sah.

Sekarang misalkan $x$ suatu akar satuan keempat. Karena $y^2=x$, maka $y$
merupakan akar satuan kedelapan. Jika $\zeta$ adalah akar satuan kedelapan
primitif pertama, delapan titik perpotongan lainnya adalah

$$
\begin{gathered}
(1,1),(1,-1),(i,\zeta),(i,-\zeta),\\
(-1,i),(-1,-i),(-i,\zeta^3),(-i,-\zeta^3).
\end{gathered}
$$

Kita tunjukkan bahwa pada kedelapan titik itu perpotongannya transversal,
sehingga setiap multiplisitas perpotongannya sama dengan $1$. Untuk

$$
F=X-Y^2,
\qquad
G=Y^2-X^5,
$$

gradiennya adalah

$$
\nabla F=(1,-2Y)
\qquad\text{dan}\qquad
\nabla G=(-5X^4,2Y).
$$

Pada setiap titik $(x,y)$ di atas, $x\ne0$, sehingga kedua kurva mulus.
Karena $x^4=1$, gradien kedua berbentuk $(-5,2y)$. Kedua arah hanya dapat
bergantung linear jika $-2y=-10y$, yang mustahil karena $y\ne0$ di atas
$\mathbb C$. Jadi semua delapan perpotongan itu transversal.

Terakhir, perhatikan titik-titik di tak hingga. Homogenisasi persamaan
pertama adalah

$$
\widetilde F=XZ-Y^2,
$$

sehingga satu-satunya titik di tak hingga pada
$\overline C=V_+(\widetilde F)$ adalah $(1,0,0)$. Homogenisasi persamaan
kedua adalah

$$
\widetilde G=Y^2Z^3-X^5,
$$

sehingga satu-satunya titik di tak hingga pada
$\overline D=V_+(\widetilde G)$ adalah $(0,1,0)$. Kedua titik itu berbeda,
jadi tidak ada perpotongan tambahan di tak hingga.

Jumlah total multiplisitas perpotongan karena itu ialah

$$
2+8\cdot1=10.
$$

Karena kedua kurva berderajat $2$ dan $5$, jumlah tersebut sama dengan hasil
kali derajat $2\cdot5=10$, sebagaimana dinyatakan Teorema Bézout.
