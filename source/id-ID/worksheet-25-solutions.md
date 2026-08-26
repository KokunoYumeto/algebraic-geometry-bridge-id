---
title: "Solusi Publik Lembar Kerja 25"
stable_id: br-ak-2012-w25-solutions
language: id-ID
source_course: "Algebraische Kurven (Osnabrück 2012)"
source_author: "Holger Brenner"
frozen_revision_contributors: "Soal 25.1: Bocardodarapti; Soal 25.2: Arbota"
upstream_map: authority/wikiversity/unit-25/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: 1a887b81de9ccf9707e1e4835e477f9c9fb4a4358ab697242b17fd29873e8370
authority_manifest: authority/wikiversity/unit-25/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 7cafbca7b5fd080529c2019967647ef8ffa823539b2113caaf0ad65e56d6afc1
public_solution_count: 2
upstream_solution_revisions: "Soal 25.1=1112930; Soal 25.2=1022975"
solution_xml_sha256: "01=39ac23016a2014f255207ba743a8537d2e0744a7aa3d624e16cd2de1f5bf4ad5; 02=74a2d210868885487a9091acf5735ff97fb8a1809f697440bb87083584df6570"
license: "CC BY-SA 4.0 for the frozen semantic source; official 2012 PDF witnesses retain their recorded CC BY-SA 2.0 Germany notice"
no_blanket_relicensing_claim: true
independent_derivative_non_endorsement: true
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_corrections: 0
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 25 {#br-ak-2012-w25-solutions}

Pada batas revisi yang dibekukan, sumber hanya menyediakan solusi publik
untuk Soal 25.1 dan Soal 25.2. Sebelas calon halaman solusi lainnya
dinyatakan tidak ada oleh kueri otoritas yang dibekukan. Tidak ada solusi
tambahan yang dibuat untuk edisi ini.

<!-- upstream_solution: Ebene algebraische Kurve/Potenzreihenansatz/x^3+y^2-xy+x/Nullpunkt/Aufgabe/Lösung; pageid=21296; revid=1112930 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1112930 -->

## Solusi Soal 25.1 {#br-ak-2012-w25-sol-01}

Kita mengambil bentuk

$$
X=F(Y)=\sum_{i=0}^{\infty}a_iY^i
$$

lalu menentukan koefisien $a_0,\ldots,a_6$ berdasarkan syarat

$$
\left(\sum_{i=0}^{\infty}a_iY^i\right)^3
+Y^2
-\left(\sum_{i=0}^{\infty}a_iY^i\right)Y
+\left(\sum_{i=0}^{\infty}a_iY^i\right)
=0.
$$

Karena deret pangkat tersebut harus menghampiri kurva di titik asal, haruslah

$$
a_0=0.
$$

Untuk $Y^1$, syarat koefisiennya adalah

$$
a_1=0,
$$

sebab tiga suku pertama pada persamaan tidak memberi kontribusi. Untuk
$Y^2$, diperoleh

$$
1+a_2=0,
\qquad\text{sehingga}\qquad
a_2=-1.
$$

Dengan demikian, suku kedua $Y^2$ telah ditangani. Untuk $Y^3$, diperoleh

$$
-a_2+a_3=0,
\qquad\text{sehingga}\qquad
a_3=a_2=-1.
$$

Untuk $Y^4$, diperoleh

$$
-a_3+a_4=0,
\qquad\text{sehingga}\qquad
a_4=a_3=-1,
$$

dan untuk $Y^5$ diperoleh

$$
-a_4+a_5=0,
\qquad\text{sehingga}\qquad
a_5=a_4=-1.
$$

Pada $Y^6$, suku pertama harus diperhitungkan untuk pertama kalinya. Kita
memperoleh

$$
a_2^3-a_5+a_6=0,
\qquad\text{sehingga}\qquad
a_6=a_5-a_2^3=-1-(-1)^3=0.
$$

[Kembali ke Soal 25.1](#br-ak-2012-w25-ex-01)

<!-- upstream_solution: Ebene algebraische Kurve/Potenzreihenansatz/x^2y+x^2+y^2-5xy+y/Nullpunkt/Aufgabe/Lösung; pageid=21581; revid=1022975 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1022975 -->

## Solusi Soal 25.2 {#br-ak-2012-w25-sol-02}

Kita mengambil bentuk

$$
Y=F(X)=\sum_{n=0}^{\infty}a_nX^n
$$

(serta $X=X$), lalu menentukan koefisien secara berurutan dengan membandingkan
koefisien pangkat-pangkat $X$. Karena solusi tersebut harus melalui titik
asal, haruslah $a_0=0$.

$$
X^1:\qquad a_1=0.
$$

$$
X^2:\qquad 1+a_2=0,
\qquad\text{sehingga}\qquad a_2=-1.
$$

$$
X^3:\qquad -5a_2+a_3=0,
\qquad\text{sehingga}\qquad a_3=-5.
$$

$$
X^4:\qquad a_2+a_2^2-5a_3+a_4=0,
\qquad\text{sehingga}\qquad a_4=5a_3=-25.
$$

$$
\begin{aligned}
X^5:\qquad
a_3+2a_2a_3-5a_4+a_5&=0,\\
a_5&=-a_3-2a_2a_3+5a_4\\
&=5-10-125\\
&=-130.
\end{aligned}
$$

Jadi, suku-suku awal deret pangkat tersebut adalah

$$
F=-X^2-5X^3-25X^4-130X^5+\ldots.
$$

[Kembali ke Soal 25.2](#br-ak-2012-w25-ex-02)
