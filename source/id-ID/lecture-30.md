---
title: "Kuliah 30 - Teorema Bézout"
stable_id: br-ak-2012-l30
language: id-ID
source_author: "Holger Brenner"
frozen_revision_contributor: "Bocardodarapti"
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 30"
upstream_pageid: 51997
upstream_revid: 1112650
upstream_timestamp: "2026-08-21T16:27:10Z"
upstream_mediawiki_sha1: e457ac9823425ad360cc32d095178e513f79ec94
source_url: "https://de.wikiversity.org/w/index.php?oldid=1112650"
authority_manifest: authority/wikiversity/unit-30/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 756ec1f9ea386b8ad0fac38086b6c97f0b94d6dc7a139dc4663911d48655bbe1
lecture_xml: authority/wikiversity/unit-30/lecture-30.xml
lecture_xml_sha256: 6b5118904f5cba97127372ccb52bb45a1c0e637202374c2d4842ff8246bd1cf0
lecture_expanded_tex: authority/wikiversity/unit-30/lecture-30-expanded.tex
lecture_expanded_tex_sha256: 0080d009a13829a4c0d75d4ce375090d76c5969b92a426635280c2c1d9af8d61
license: "Current semantic course text and this translation: CC BY-SA 4.0. Unit 30 reader media retain their component-specific public-domain status as recorded in authority/RIGHTS-unit-30.csv. No blanket relicensing claim is made."
source_component_license_route: "Semantic-site rights notice: CC BY-SA 4.0; media component rights remain item-specific; official-PDF notices remain component-specific; no blanket relicensing claim."
license_evidence: "authority/UNIT_30_AUTHORITY_FREEZE.md; authority/RIGHTS-unit-30.csv; authority/ASSET_CLOSURE-unit-30.json"
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra."
source_semantic_entities: 7
source_corrections: 3
correction_ids: "AGC-CORR-0130; AGC-CORR-0131; AGC-CORR-0132"
reader_media_positions: 1
---

# Kuliah 30: Teorema Bézout {#br-ak-2012-l30}

Dalam kuliah ini kita akan membuktikan Teorema Bézout untuk bidang
proyektif. Teorema ini menyatakan bahwa, bagi dua kurva proyektif di bidang
proyektif yang tidak mempunyai komponen bersama dan masing-masing berderajat
$m$ dan $n$, jumlah semua multiplisitas perpotongannya sama dengan $mn$.
Penyajian kita secara garis besar mengikuti susunan Fulton.

## Komponen homogen berderajat tertentu {#br-ak-2012-l30-s01}

<!-- upstream_entity: Projektive ebene Kurven/Satz von Bézout/Beweisaufbau/Textabschnitt -->

Untuk gelanggang polinom $P$ dan bilangan asli $\ell$, selanjutnya
$P_\ell$ menyatakan *komponen homogen berderajat $\ell$*, yaitu ruang yang
terdiri atas semua polinom homogen berderajat $\ell$. Notasi yang sama akan
kita gunakan untuk gelanggang faktor bergradasi dari gelanggang polinom,
yakni gelanggang faktor oleh suatu ideal homogen. Sebagai ruang vektor atas
lapangan dasar $K$, komponen ini dibangkitkan oleh semua monom berderajat
$\ell$. Khususnya, $P_\ell$ merupakan ruang vektor-$K$ berdimensi hingga.

<!-- upstream_entity: Schnitttheorie von Kurven/Satz von Bézout/Dimension von Stufe im homogenen Restklassenring/Fakt -->

### Lema 30.1: dimensi komponen homogen gelanggang faktor {#br-ak-2012-l30-lem-01}

Misalkan $K$ suatu lapangan, misalkan

$$
F,G\in K[X,Y,Z]=P
$$

polinom-polinom homogen berderajat $m$ dan $n$, dan andaikan $F$ serta $G$
tidak mempunyai pembagi bersama yang takkonstan. Maka

$$
\dim_K\bigl(P/(F,G)\bigr)_\ell=mn
$$

untuk $\ell$ yang cukup besar.

#### Bukti {#br-ak-2012-l30-lem-01-proof}

Perhatikan barisan eksak

$$
0\longrightarrow P
\stackrel{\begin{pmatrix}G\\-F\end{pmatrix}}{\longrightarrow}P\times P
\stackrel{(F,G)}{\longrightarrow}P
\longrightarrow P/(F,G)\longrightarrow0.
$$

Pemetaan pertama ialah

$$
H\longmapsto(GH,-FH),
$$

pemetaan berikutnya ialah

$$
(A,B)\longmapsto AF+BG,
$$

dan pemetaan terakhir ialah pembentukan kelas faktor. Semua pemetaan ini
merupakan homomorfisme modul-$P$. Injektivitas pada suku pertama jelas karena
$P$ merupakan domain integral. Barisan itu jelas eksak pada dua suku
terakhir; yang masih harus dibuktikan hanyalah bahwa barisan tersebut eksak
pada suku kedua.

Komposisi dua pemetaan pertama adalah pemetaan nol. Sebaliknya, misalkan

$$
AF+BG=0
$$

di $P$. Karena $P$ merupakan domain faktorisasi tunggal dan $F,G$ saling
prima, $A$ harus merupakan kelipatan $G$. Tuliskan $A=QG$. Persamaan di atas
kemudian menjadi

$$
G(QF+B)=0,
$$

sehingga $B=-QF$. Jadi

$$
(A,B)=Q(G,-F)
$$

berasal dari pemetaan di sebelah kiri.

> **Koreksi sumber AGC-CORR-0130 - tanda pada relasi.** Sumber mengatakan
> bahwa $B$ merupakan kelipatan $F$ "dengan faktor yang sama", tetapi tanda
> yang ditentukan oleh $AF+BG=0$ adalah $B=-QF$. Edisi menampilkan tanda
> minus ini secara eksplisit, sesuai dengan pemetaan $H\mapsto(GH,-FH)$ yang
> sudah tercetak dalam sumber.

Karena $F$ dan $G$ homogen dengan derajat tetap, barisan tersebut dapat
dibatasi pada komponen-komponen homogen. Hasilnya adalah barisan eksak

$$
0\longrightarrow P_{\ell-m-n}
\stackrel{\begin{pmatrix}G\\-F\end{pmatrix}}{\longrightarrow}
P_{\ell-m}\times P_{\ell-n}
\stackrel{(F,G)}{\longrightarrow}P_\ell
\longrightarrow\bigl(P/(F,G)\bigr)_\ell\longrightarrow0,
$$

dengan komponen berindeks negatif didefinisikan sebagai $0$. Barisan hasil
pembatasan tetap eksak karena komponen-komponen homogen suatu homomorfisme
homogen tidak saling bercampur. Semua komponen yang terlibat sekarang
merupakan ruang vektor berdimensi hingga.

Jika $\ell\geq m+n$, semua indeks tidak negatif dan

$$
\dim_K(P_\ell)=\frac{(\ell+1)(\ell+2)}2.
$$

Berdasarkan aditivitas dimensi ruang vektor dalam kompleks eksak (lihat Soal
14.7), diperoleh

$$
\begin{aligned}
\dim_K\bigl((P/(F,G))_\ell\bigr)
&=\frac{(\ell+1)(\ell+2)}2
-\frac{(\ell-m+1)(\ell-m+2)}2\\
&\quad-\frac{(\ell-n+1)(\ell-n+2)}2
+\frac{(\ell-m-n+1)(\ell-m-n+2)}2\\
&=\frac{2-(-m+1)(-m+2)-(-n+1)(-n+2)
+(-m-n+1)(-m-n+2)}2\\
&=\frac{2mn}{2}\\
&=mn.
\end{aligned}
$$

$\square$

## Injektivitas perkalian dengan $Z$ {#br-ak-2012-l30-s02}

<!-- upstream_entity: Schnitttheorie von Kurven/Satz von Bézout/Injektivität der Multiplikation mit Z im homogenen Restklassenring/Fakt -->

### Lema 30.2: perkalian dengan $Z$ pada gelanggang faktor {#br-ak-2012-l30-lem-02}

Misalkan $K$ lapangan tertutup secara aljabar dan misalkan

$$
F,G\in K[X,Y,Z]
$$

polinom-polinom homogen yang tidak mempunyai titik nol proyektif bersama pada

$$
V_+(Z)\subseteq\mathbb P_K^2.
$$

Tuliskan gelanggang faktor yang bersesuaian sebagai

$$
R=K[X,Y,Z]/(F,G).
$$

Maka pemetaan

$$
\begin{aligned}
R&\longrightarrow R,\\
H&\longmapsto ZH
\end{aligned}
$$

injektif.

#### Bukti {#br-ak-2012-l30-lem-02-proof}

Ambil $H\in K[X,Y,Z]$ dan andaikan kelasnya dipetakan ke $0$. Artinya,
terdapat $L,M\in K[X,Y,Z]$ sedemikian sehingga

$$
ZH=LF+MG.
$$

Substitusikan $Z=0$ ke dalam persamaan ini. Di $K[X,Y]$ kita memperoleh

$$
0=L(X,Y,0)F(X,Y,0)+M(X,Y,0)G(X,Y,0).
$$

Karena $F$ dan $G$ tidak mempunyai titik nol proyektif bersama pada
$V_+(Z)$, polinom $F(X,Y,0)$ dan $G(X,Y,0)$ hanya mempunyai titik nol
bersama $(0,0)$ di $\mathbb A_K^2$. Oleh sebab itu, keduanya saling prima di
$K[X,Y]$. Maka terdapat $Q\in K[X,Y]$ dengan

$$
L(X,Y,0)=QG(X,Y,0),
\qquad
M(X,Y,0)=-QF(X,Y,0).
$$

Jika diangkat kembali ke $K[X,Y,Z]$, persamaan ini berarti bahwa

$$
L=QG(X,Y,0)+Z\overline L,
\qquad
M=-QF(X,Y,0)+Z\overline M
$$

untuk suatu $\overline L,\overline M\in K[X,Y,Z]$. Dengan menuliskan

$$
F=F(X,Y,0)+Z\overline F,
\qquad
G=G(X,Y,0)+Z\overline G,
$$

persamaan awal memberikan

$$
\begin{aligned}
ZH
&=LF+MG\\
&=\bigl(QG(X,Y,0)+Z\overline L\bigr)F
+\bigl(-QF(X,Y,0)+Z\overline M\bigr)G\\
&=Q\bigl(G-Z\overline G\bigr)F
-Q\bigl(F-Z\overline F\bigr)G
+Z\overline L F+Z\overline M G\\
&=-QZ\overline G F+QZ\overline F G
+Z\overline L F+Z\overline M G\\
&=Z\bigl(-Q\overline G F+Q\overline F G
+\overline L F+\overline M G\bigr).
\end{aligned}
$$

Kita dapat mencoret $Z$ dari persamaan di gelanggang polinom tersebut dan
memperoleh suatu penyajian $H$ sebagai kombinasi linear $F$ dan $G$. Jadi
kelas $H$ di $R$ juga sama dengan $0$. $\square$

![Dua kurva kubik. Karya Hack, dibuat dengan Mathematica 6, domain publik.](authority/assets/Two_cubic_curves.png){fig-alt="Dua kurva kubik, satu merah dan satu biru, yang saling melintas pada bidang koordinat"}

## Teorema Bézout {#br-ak-2012-l30-s03}

Sekarang kita sampai pada Teorema Bézout.

<!-- upstream_entity: Schnitttheorie von Kurven/Satz von Bézout/Fakt -->

### Teorema 30.3: Teorema Bézout {#br-ak-2012-l30-thm-01}

Misalkan $K$ lapangan tertutup secara aljabar dan misalkan

$$
F,G\in K[X,Y,Z]
$$

polinom-polinom homogen berderajat $m$ dan $n$ tanpa komponen bersama, dengan
kurva-kurva yang bersesuaian

$$
C=V_+(F),\qquad D=V_+(G)\subseteq\mathbb P_K^2.
$$

Maka

$$
\sum_P\operatorname{mult}_P(C,D)=mn.
$$

#### Bukti {#br-ak-2012-l30-thm-01-proof}

Irisan $C\cap D$ hanya terdiri atas berhingga banyak titik. Berdasarkan Soal
27.10, setelah suatu perubahan koordinat proyektif kita dapat mengandaikan
bahwa semua titik perpotongan terletak di

$$
\mathbb A_K^2=D_+(Z)\subseteq\mathbb P_K^2.
$$

Misalkan $\widetilde F,\widetilde G\in K[X,Y]$ adalah dehomogenisasi yang
mendeskripsikan kurva afin $C\cap\mathbb A_K^2$ dan
$D\cap\mathbb A_K^2$. Maka

$$
\begin{aligned}
\sum_{P\in\mathbb P_K^2}\operatorname{mult}_P(F,G)
&=\sum_{P\in\mathbb A_K^2}
\operatorname{mult}_P(\widetilde F,\widetilde G)\\
&=\sum_{P\in\mathbb A_K^2}
\dim_K\!\left(
K[X,Y]_{\mathfrak m_P}/(\widetilde F,\widetilde G)
\right)\\
&=\dim_K\!\left(K[X,Y]/(\widetilde F,\widetilde G)\right).
\end{aligned}
$$

Kesamaan terakhir berdasarkan Teorema 26.11. Kita akan menghubungkan dimensi
$K$ gelanggang faktor takhomogen ini dengan dimensi suatu komponen homogen
dari gelanggang faktor

$$
\bigl(K[X,Y,Z]/(F,G)\bigr)_\ell.
$$

Berdasarkan Lema 30.1, untuk $\ell$ yang cukup besar dimensi komponen terakhir
ini sama dengan $mn$.

Pilih suatu basis

$$
V_1,\ldots,V_{mn}
$$

dari $\bigl(K[X,Y,Z]/(F,G)\bigr)_\ell$, dengan $\ell$ cukup besar dan
tetap. Kita mengklaim bahwa dehomogenisasi

$$
v_i=V_i(X,Y,1),\qquad i=1,\ldots,mn,
$$

membentuk suatu basis dari

$$
K[X,Y]/(\widetilde F,\widetilde G).
$$

Pertama kita membuktikan bahwa unsur-unsur ini membangkitkan. Ambil sembarang
$q\in K[X,Y]$ dan misalkan homogenisasinya

$$
Q\in K[X,Y,Z]
$$

berderajat $d$. Pilih bilangan bulat $e\geq0$ sehingga
$d+e\geq\ell$. Berdasarkan Lema 30.2,
untuk setiap $\lambda\geq1$ pemetaan

$$
\begin{aligned}
\bigl(K[X,Y,Z]/(F,G)\bigr)_\ell
&\longrightarrow
\bigl(K[X,Y,Z]/(F,G)\bigr)_{\ell+\lambda},\\
H&\longmapsto Z^\lambda H
\end{aligned}
$$

injektif. Karena kedua ruang mempunyai dimensi $mn$, pemetaan ini juga
bijektif. Dengan $\lambda=d+e-\ell$, unsur-unsur

$$
Z^\lambda V_i,\qquad i=1,\ldots,mn,
$$

membentuk suatu basis dari komponen berderajat $\ell+\lambda=d+e$.

> **Koreksi sumber AGC-CORR-0131 - kasus batas $\lambda=0$.** Sumber memilih
> $d+e\geq\ell$, tetapi pernyataan tentang perkalian dengan $Z^\lambda$
> ditulis hanya untuk $\lambda\geq1$. Jika $d+e=\ell$, maka $\lambda=0$ dan
> pemetaan yang diperlukan adalah identitas; jika $d+e>\ell$, argumen sumber
> berlaku dengan $\lambda\geq1$. Dengan pemisahan dua kasus ini, kesimpulan
> basis di atas berlaku untuk seluruh pilihan $d+e\geq\ell$.

Karena itu terdapat $a_1,\ldots,a_{mn}\in K$ sedemikian sehingga

$$
Z^eQ=\sum_{i=1}^{mn}a_iZ^{d+e-\ell}V_i.
$$

Dehomogenisasi persamaan ini langsung memberikan suatu penyajian $q$ sebagai
kombinasi linear $v_1,\ldots,v_{mn}$.

Untuk membuktikan bahwa unsur-unsur ini bebas linear, andaikan

$$
\sum_{i=1}^{mn}a_iv_i=0
$$

di gelanggang faktor. Maka di $K[X,Y]$ terdapat persamaan

$$
\sum_{i=1}^{mn}a_iv_i
=\widetilde A\widetilde F+\widetilde B\widetilde G.
$$

Ambil polinom homogen $A,B\in K[X,Y,Z]$ yang masing-masing berdehomogenisasi
$\widetilde A,\widetilde B$. Dengan demikian, kita mempunyai dua ungkapan
yang dehomogenisasinya sama: $\sum_i a_iV_i$, yang homogen berderajat
$\ell$, dan $AF+BG$, yang merupakan jumlah dua polinom homogen yang derajatnya
mungkin berbeda.

Dengan memilih bilangan-bilangan bulat taknegatif $r,s,t$ yang sesuai, kita
dapat membuat

$$
\sum_{i=1}^{mn}a_iZ^rV_i
\qquad\text{dan}\qquad
Z^sAF+Z^tBG
$$

homogen dengan derajat yang sama. Menurut Soal 6.9, kesamaan
dehomogenisasinya kemudian menyiratkan

$$
\sum_{i=1}^{mn}a_iZ^rV_i=Z^sAF+Z^tBG.
$$

Di $K[X,Y,Z]/(F,G)$, persamaan ini berarti

$$
\sum_{i=1}^{mn}a_iZ^rV_i=0.
$$

Perkalian dengan $Z^r$ bersifat injektif: untuk $r=0$ pemetaan itu adalah
identitas, sedangkan untuk $r>0$ hal ini mengikuti dengan menerapkan Lema
30.2 berulang kali. Karena $V_1,\ldots,V_{mn}$ merupakan basis, semua $a_i=0$.
Dengan demikian, $v_1,\ldots,v_{mn}$ benar-benar merupakan basis, sehingga

$$
\dim_K\!\left(K[X,Y]/(\widetilde F,\widetilde G)\right)=mn.
$$

Ini membuktikan rumus Teorema Bézout. $\square$

<!-- upstream_entity: Schnitttheorie von Kurven/Satz von Bézout/Es gibt Schnittpunkt/Fakt -->

### Korolari 30.4: adanya titik perpotongan {#br-ak-2012-l30-cor-01}

Misalkan $K$ lapangan tertutup secara aljabar dan misalkan

$$
C,D\subseteq\mathbb P_K^2
$$

kurva-kurva bidang proyektif. Maka

$$
C\cap D\ne\varnothing.
$$

#### Bukti {#br-ak-2012-l30-cor-01-proof}

Pernyataan ini jelas benar jika $C$ dan $D$ mempunyai komponen bersama. Jika
tidak, pernyataan tersebut mengikuti dari Teorema 30.3. $\square$

<!-- upstream_entity: Schnitttheorie von Kurven/Satz von Bézout/Maximal mn Schnittpunkte/Fakt -->

### Korolari 30.5: paling banyak $mn$ titik perpotongan {#br-ak-2012-l30-cor-02}

Misalkan $K$ lapangan tertutup secara aljabar dan misalkan

$$
F,G\in K[X,Y,Z]
$$

polinom-polinom homogen berderajat $m$ dan $n$ tanpa komponen bersama, dengan
kurva-kurva yang bersesuaian

$$
C=V_+(F),\qquad D=V_+(G)\subseteq\mathbb P_K^2.
$$

Maka $C$ dan $D$ mempunyai paling banyak $mn$ titik perpotongan.

#### Bukti {#br-ak-2012-l30-cor-02-proof}

Hal ini langsung mengikuti dari Teorema 30.3, karena setiap titik
perpotongan menyumbang sedikitnya $1$ pada jumlah multiplisitas perpotongan.
$\square$

## Contoh: parabola Neil dan sebuah lingkaran {#br-ak-2012-l30-s04}

<!-- upstream_entity: Satz von Bézout/ZY^2-X^3 und (X-Z)^2+Y^2-1/Beispiel -->

### Contoh 30.6: lima titik dengan jumlah multiplisitas enam {#br-ak-2012-l30-ex-01}

Dalam contoh ini kita bekerja di atas $\mathbb C$. Tinjau parabola Neil

$$
C=V_+(ZY^2-X^3)
$$

dan lingkaran berpusat di $(1,0,1)$,

$$
D=V_+\bigl((X-Z)^2+Y^2-Z^2\bigr).
$$

> **Koreksi sumber AGC-CORR-0132 - lapangan dasar contoh.** Sumber tidak
> menyebut lapangan dasar, tetapi perhitungannya memakai $\sqrt2\,\mathrm i$
> dan bentuk titik yang berbeda seperti tercetak hanya berlaku tanpa masalah
> karakteristik khusus. Edisi menetapkan $K=\mathbb C$, sehingga seluruh
> perhitungan, lima titik berbeda, dan penggunaan Teorema Bézout berada dalam
> cakupan yang sah. Persamaan sumber tidak diubah.

Menurut Teorema Bézout, kita mengharapkan jumlah total multiplisitas
perpotongan sebesar $6$. Mari kita hitung titik-titik perpotongannya. Jika
$Z=0$, persamaan pertama memberikan $X=0$, lalu persamaan kedua memberikan
$Y=0$. Ini tidak menentukan titik proyektif, sehingga tidak ada titik
perpotongan pada garis proyektif $V_+(Z)$.

Kita karena itu meninjau persamaan afin

$$
Y^2-X^3=0,
\qquad
(X-1)^2+Y^2-1=0.
$$

Substitusi

$$
Y^2=1-(X-1)^2
$$

ke persamaan pertama menghasilkan

$$
\begin{aligned}
1-(X-1)^2-X^3
&=-X^3-X^2+2X\\
&=X(-X^2-X+2)\\
&=-X(X-1)(X+2).
\end{aligned}
$$

Jadi titik-titik perpotongannya adalah

$$
(0,0),\quad(1,1),\quad(1,-1),\quad
(-2,2\sqrt2\,\mathrm i),\quad
(-2,-2\sqrt2\,\mathrm i).
$$

Dua titik terakhir juga memperlihatkan mengapa hipotesis lapangan tertutup
secara aljabar diperlukan: keduanya akan hilang jika kita hanya bekerja di
atas $\mathbb R$. Jadi terdapat lima titik perpotongan berbeda. Parabola Neil
mempunyai singularitas di titik asal, dan titik asal juga merupakan titik
perpotongan, sehingga multiplisitas perpotongannya di sana harus lebih besar
daripada $1$. Untuk menegaskannya, perhatikan

$$
\begin{aligned}
&K[X,Y]_{(X,Y)}/\bigl(Y^2-X^3,Y^2-1+(X-1)^2\bigr)\\
&\quad=K[X,Y]_{(X,Y)}/\bigl(Y^2-X^3,X(X-1)(X+2)\bigr)\\
&\quad=K[X,Y]_{(X,Y)}/\bigl(Y^2-X^3,X\bigr)\\
&\quad=K[X,Y]_{(X,Y)}/\bigl(Y^2,X\bigr)\\
&\quad=K[Y]/(Y^2).
\end{aligned}
$$

Di sini kita mengulangi eliminasi di atas dan kemudian memakai fakta bahwa
$X-1$ serta $X+2$ merupakan unit dalam gelanggang lokal
$K[X,Y]_{(X,Y)}$. Dimensinya adalah $2$. Dengan demikian, multiplisitas
perpotongan di titik asal sama dengan $2$, sedangkan pada masing-masing dari
empat titik lain sama dengan $1$, sebagaimana juga dapat diperiksa secara
langsung. Jumlahnya ialah

$$
2+1+1+1+1=6=3\cdot2,
$$

tepat seperti yang dinyatakan Teorema Bézout.
