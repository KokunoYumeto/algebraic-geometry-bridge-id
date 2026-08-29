---
title: "Kuliah 3 - Konstruksi Linear Bundel Vektor dan Praberkas"
stable_id: br-bgk-2019-l03
language: id-ID
source_course: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)"
source_author: "Holger Brenner"
frozen_revision_contributor: "Arbota"
upstream_title: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)/Vorlesung 3"
upstream_pageid: 109005
upstream_revid: 793623
upstream_timestamp: "2022-08-25T06:25:18Z"
upstream_mediawiki_sha1: 065d606279906a405645b5b97abf2e3c027e2b4c
source_url: "https://de.wikiversity.org/w/index.php?oldid=793623"
authority_manifest: authority/wikiversity-bgk/unit-03/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 60270cc7ba74a4ed744687ae18c3887eca8a2fff6bce48a819be102d4a619a5a
lecture_xml: authority/wikiversity-bgk/unit-03/lecture-03.xml
lecture_xml_sha256: 7c048b329215669e01d8068cd150f5a1bee11bc00c2466e2d9b63e3d7abfa258
lecture_expanded_tex: authority/wikiversity-bgk/unit-03/lecture-03-expanded.tex
lecture_expanded_tex_sha256: 04989737d12bf8ac77127e60f193e6ac2c19201d4f5d66221f8c5e1de85a87eb
official_pdf: authority/artifacts/bgk-lecture-03-official.pdf
official_pdf_sha256: f418f7acb52670e0d274528450101c93f7dacdef880f99d4aa0e80ac920da884
license: "Frozen semantic course text and this translation: CC BY-SA 4.0. Official PDF witnesses retain their recorded component notices; no blanket relicensing claim is made."
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra."
---

# Kuliah 3: Konstruksi Linear Bundel Vektor dan Praberkas {#br-bgk-2019-l03}

## Konstruksi linear bundel vektor {#br-bgk-2019-l03-s01}

Untuk ruang vektor terdapat berbagai konstruksi, seperti jumlah langsung,
hasil kali tensor, dan ruang dual. Kita ingin memperkenalkan konstruksi yang
bersesuaian untuk bundel vektor. Pada setiap serat, konstruksi itu harus sama
dengan konstruksi dalam aljabar linear, tetapi juga harus memperhitungkan
ketergantungan serat pada ruang basis. Kita akan bekerja dengan data
pengeleman bundel vektor dan menggunakan fakta bahwa, untuk dua bundel
vektor di atas ruang topologis $X$, selalu terdapat penutup terbuka yang
cukup halus dari $X$ sehingga kedua bundel mempunyai trivialisasi terhadap
penutup itu. Secara khusus, kita dapat mereduksi pembahasan pada kasus ketika
kedua bundel diberikan oleh deskripsi matriks. Konstruksinya kemudian
berlangsung pada tingkat manipulasi matriks.

### Definisi 3.1: jumlah langsung {#br-bgk-2019-l03-def-01}

Misalkan $E$ dan $F$ bundel vektor real di atas ruang topologis $X$, dengan
trivialisasi

$$
\alpha_i:E|_{U_i}\longrightarrow U_i\times\mathbb R^m
$$

dan

$$
\beta_i:F|_{U_i}\longrightarrow U_i\times\mathbb R^n.
$$

Bundel vektor yang diperoleh dari data pengeleman

$$
G_i=U_i\times\mathbb R^m\times\mathbb R^n
$$

dan

$$
\varphi_{ij}:G_i|_{U_i\cap U_j}\longrightarrow G_j|_{U_i\cap U_j},
$$

dengan

$$
\varphi_{ij}(x,v,w)
=\bigl(x,\alpha_j(\alpha_i^{-1}(x,v)),
          \beta_j(\beta_i^{-1}(x,w))\bigr),
$$

disebut *jumlah langsung* dari $E$ dan $F$, dan dinotasikan dengan
$E\oplus F$.

Jika $E$ diberikan oleh deskripsi matriks

$$
\varphi_{ij}:U_i\cap U_j\longrightarrow\operatorname{GL}_m(\mathbb R)
$$

dan $F$ oleh

$$
\psi_{ij}:U_i\cap U_j\longrightarrow\operatorname{GL}_n(\mathbb R),
$$

maka deskripsi matriks $E\oplus F$ diperoleh dengan menempatkan kedua
matriks pada blok diagonal sebuah matriks berukuran
$(m+n)\times(m+n)$ dan mengisi blok lainnya dengan nol.

### Definisi 3.2: hasil kali tensor {#br-bgk-2019-l03-def-02}

Misalkan $E$ dan $F$ bundel vektor real di atas $X$, dengan trivialisasi
$\alpha_i$ dan $\beta_i$ seperti di atas. Bundel vektor yang diperoleh dari
data pengeleman

$$
G_i=U_i\times(\mathbb R^m\otimes\mathbb R^n)
$$

dan

$$
\varphi_{ij}:G_i|_{U_i\cap U_j}\longrightarrow G_j|_{U_i\cap U_j},
\qquad
\varphi_{ij}
=\bigl(\alpha_j\circ\alpha_i^{-1}\bigr)
 \otimes
 \bigl(\beta_j\circ\beta_i^{-1}\bigr),
$$

disebut *hasil kali tensor* dari $E$ dan $F$, dan dinotasikan dengan
$E\otimes F$. Di sini, pada setiap titik basis diambil hasil kali tensor dari
pemetaan-pemetaan linearnya.

Jika deskripsi matriks kedua bundel diberikan, deskripsi matriks hasil kali
tensornya diperoleh melalui *hasil kali Kronecker*: setiap entri pada salah
satu matriks dikalikan dengan setiap entri pada matriks lainnya.

### Definisi 3.3: hasil kali eksterior {#br-bgk-2019-l03-def-03}

Misalkan $E$ sebuah bundel vektor real berank $m$ di atas ruang topologis
$X$, dengan trivialisasi

$$
\alpha_i:E|_{U_i}\longrightarrow U_i\times\mathbb R^m,
$$

dan misalkan $r\in\mathbb N$. Bundel vektor yang diperoleh dari data
pengeleman

$$
G_i=U_i\times\bigwedge^r\mathbb R^m
$$

dan

$$
\varphi_{ij}:G_i|_{U_i\cap U_j}\longrightarrow G_j|_{U_i\cap U_j},
\qquad
\varphi_{ij}=\bigwedge^r\bigl(\alpha_j\circ\alpha_i^{-1}\bigr),
$$

disebut *hasil kali eksterior ke-$r$* dari $E$, dan dinotasikan dengan
$\bigwedge^rE$. Pada setiap titik basis, yang diambil adalah hasil kali
eksterior ke-$r$ dari pemetaan linear yang bersangkutan.

Untuk suatu deskripsi matriks $E$, deskripsi matriks
$\bigwedge^rE$ diperoleh dengan menyusun semua determinan submatriks
$r\times r$ menjadi sebuah matriks.

### Definisi 3.4: bundel determinan {#br-bgk-2019-l03-def-04}

Misalkan $E$ sebuah bundel vektor real berank $m$ di atas ruang topologis
$X$. Hasil kali eksterior ke-$m$

$$
\bigwedge^mE
$$

disebut *bundel determinan* dari $E$, dan dinotasikan dengan $\det E$.

Bundel determinan merupakan bundel garis. Deskripsi matriksnya diberikan
oleh determinan.

### Definisi 3.5: bundel homomorfisme {#br-bgk-2019-l03-def-05}

Misalkan $E$ dan $F$ bundel vektor real di atas ruang topologis $X$, dengan
trivialisasi

$$
\alpha_i:E|_{U_i}\longrightarrow U_i\times\mathbb R^m,
\qquad
\beta_i:F|_{U_i}\longrightarrow U_i\times\mathbb R^n.
$$

Bundel vektor yang diperoleh dari data pengeleman

$$
G_i=U_i\times\operatorname{Hom}_{\mathbb R}
       (\mathbb R^m,\mathbb R^n)
$$

dan

$$
\varphi_{ij}:G_i|_{U_i\cap U_j}\longrightarrow G_j|_{U_i\cap U_j},
$$

dengan

$$
\varphi_{ij}(\theta)
=\bigl(\beta_j\circ\beta_i^{-1}\bigr)
 \circ\theta\circ
 \bigl(\alpha_i\circ\alpha_j^{-1}\bigr),
$$

disebut *bundel homomorfisme* dari $E$ ke $F$, dan dinotasikan dengan
$\operatorname{Hom}(E,F)$.

### Definisi 3.6: bundel dual {#br-bgk-2019-l03-def-06}

Untuk sebuah bundel vektor real $E$ di atas ruang topologis $X$, bundel
homomorfisme

$$
\operatorname{Hom}(E,X\times\mathbb R)
$$

disebut *bundel dual* dari $E$, dan dinotasikan dengan $E^*$.

Pada suatu manifold, bundel dual dari bundel tangen disebut *bundel
kotangen*.

## Praberkas {#br-bgk-2019-l03-s02}

### Definisi 3.7: praberkas {#br-bgk-2019-l03-def-07}

Misalkan $X$ sebuah ruang topologis. Sebuah *praberkas* $\mathcal F$ pada
$X$ adalah suatu penetapan yang memasangkan kepada setiap himpunan terbuka
$U\subseteq X$ sebuah himpunan $\mathcal F(U)$, dan kepada setiap pasangan
himpunan terbuka $U\subseteq V$ sebuah pemetaan

$$
\rho_{V,U}:\mathcal F(V)\longrightarrow\mathcal F(U),
$$

sedemikian sehingga kedua syarat berikut dipenuhi.

1. Untuk $U=V$,

   $$
   \rho_{U,U}=\operatorname{Id}_{\mathcal F(U)}.
   $$

2. Untuk himpunan terbuka $U\subseteq V\subseteq W$,

   $$
   \rho_{W,U}=\rho_{V,U}\circ\rho_{W,V}.
   $$

Pemetaan $\rho_{V,U}$ disebut *pemetaan restriksi*. Himpunan
$\mathcal F(U)$ juga disebut nilai praberkas pada himpunan terbuka $U$.

Contoh-contoh dasar praberkas, dan kelak berkas, adalah konstruksi berikut.

### Contoh 3.8: pemetaan kontinu {#br-bgk-2019-l03-exa-01}

Misalkan $X$ dan $Z$ ruang topologis. Kepada setiap himpunan terbuka
$U\subseteq X$ kita pasangkan himpunan pemetaan kontinu dari $U$ ke $Z$,
yaitu

$$
C^0(U,Z)=\{\varphi:U\to Z\mid\varphi\text{ kontinu}\}.
$$

Setiap pemetaan kontinu $\varphi:U\to Z$ dapat direstriksi ke himpunan
terbuka $V\subseteq U$. Selain itu, untuk $U\subseteq V\subseteq W$,
restriksi dari $W$ ke $U$ dapat dilakukan sekaligus ataupun dalam dua
langkah. Karena itu, konstruksi ini merupakan sebuah praberkas.

Kasus khusus berikut mempunyai struktur tambahan, yakni struktur ruang
bergelanggang.

### Contoh 3.9: fungsi kontinu bernilai real {#br-bgk-2019-l03-exa-02}

Misalkan $X$ sebuah ruang topologis. Kepada setiap himpunan terbuka
$U\subseteq X$ kita pasangkan himpunan fungsi kontinu bernilai real pada
$U$,

$$
\mathcal C(U)=C^0(U,\mathbb R)
=\{f:U\to\mathbb R\mid f\text{ kontinu}\}.
$$

Karena setiap fungsi kontinu pada $U$ dapat direstriksi ke setiap himpunan
terbuka $V\subseteq U$, konstruksi ini merupakan sebuah praberkas.

### Contoh 3.10: fungsi terdiferensial {#br-bgk-2019-l03-exa-03}

Misalkan $X$ sebuah manifold terdiferensial. Kepada setiap himpunan terbuka
$U\subseteq X$ kita pasangkan himpunan fungsi terdiferensial bernilai real
pada $U$,

$$
\mathcal C(U)=C^1(U,\mathbb R)
=\{f:U\to\mathbb R\mid f\text{ terdiferensial kontinu}\}.
$$

Karena setiap fungsi terdiferensial pada $U$ dapat direstriksi ke setiap
himpunan terbuka $V\subseteq U$, konstruksi ini merupakan sebuah
praberkas.

### Contoh 3.11: praberkas konstan {#br-bgk-2019-l03-exa-04}

Pada ruang topologis $X$, untuk suatu himpunan tetap $M$, penetapan yang
memasangkan $M$ kepada setiap himpunan terbuka $U\subseteq X$ dan
identitas pada $M$ kepada setiap inklusi merupakan sebuah praberkas. Ia
disebut *praberkas konstan*.

Untuk contoh berikut, bayangkan sebuah bundel vektor di atas basis $X$.

### Contoh 3.12: praberkas seksi kontinu {#br-bgk-2019-l03-exa-05}

Misalkan $X$ dan $Y$ ruang topologis, dan misalkan

$$
p:Y\longrightarrow X
$$

sebuah pemetaan kontinu tetap. Untuk setiap himpunan terbuka
$U\subseteq X$, situasi ini menginduksi pemetaan kontinu

$$
Y|_U=p^{-1}(U)\longrightarrow U.
$$

Kepada $U$ kita pasangkan himpunan seksi kontinu pada $U$ dari pemetaan
tersebut,

$$
S(U,Y)=\{s:U\to p^{-1}(U)\mid s\text{ seksi kontinu dari }p\}.
$$

Sebuah seksi kontinu dapat direstriksi ke setiap himpunan terbuka
$V\subseteq U$, dengan kodomain sekaligus direstriksi menjadi
$p^{-1}(V)$. Jadi konstruksi ini merupakan sebuah praberkas.

Karena contoh penting ini, sebuah unsur
$s\in\mathcal F(U)$ juga disebut *seksi* dari praberkas $\mathcal F$ di
atas $U$. Untuk restriksi seksi itu ke himpunan terbuka yang lebih kecil
$V\subseteq U$, kita juga menulis

$$
s|_V=\rho_{U,V}(s).
$$

### Definisi 3.13: subpraberkas {#br-bgk-2019-l03-def-08}

Misalkan $\mathcal F$ sebuah praberkas pada ruang topologis $X$. Sebuah
praberkas $\mathcal G$ disebut *subpraberkas* dari $\mathcal F$ jika, untuk
setiap himpunan terbuka $U\subseteq X$,

$$
\mathcal G(U)\subseteq\mathcal F(U),
$$

dan, untuk setiap $U\subseteq V$, pemetaan restriksinya kompatibel:

$$
\rho^{\mathcal G}_{V,U}
=\rho^{\mathcal F}_{V,U}|_{\mathcal G(V)}.
$$

> **Catatan edisi - syarat restriksi yang hilang pada sumber.** Definisi
> sumber hanya menyatakan $\mathcal G(U)\subseteq\mathcal F(U)$ untuk setiap
> $U$ dan tidak menyatakan kompatibilitas pemetaan restriksi. Edisi
> menampilkan syarat restriksi di atas agar objek yang didefinisikan benar
> merupakan subpraberkas; bentuk sumber yang lebih pendek dipertahankan
> dalam catatan ini.

Karena fungsi terdiferensial pada suatu manifold khususnya kontinu,
praberkas fungsi terdiferensial membentuk subberkas dari praberkas fungsi
kontinu bernilai real.

## Praberkas dengan struktur {#br-bgk-2019-l03-s03}

### Definisi 3.14: praberkas grup {#br-bgk-2019-l03-def-09}

Sebuah praberkas $\mathcal F$ pada ruang topologis $X$ disebut
*praberkas grup* jika $\mathcal F(U)$ merupakan sebuah grup untuk setiap
himpunan terbuka $U\subseteq X$, dan, untuk setiap inklusi
$U\subseteq V$, pemetaan restriksi

$$
\rho_{V,U}:\mathcal F(V)\longrightarrow\mathcal F(U)
$$

merupakan homomorfisme grup.

### Definisi 3.15: praberkas gelanggang komutatif {#br-bgk-2019-l03-def-10}

Sebuah praberkas $\mathcal F$ pada ruang topologis $X$ disebut
*praberkas gelanggang komutatif* jika $\mathcal F(U)$ merupakan sebuah
gelanggang komutatif untuk setiap himpunan terbuka $U\subseteq X$, dan,
untuk setiap inklusi $U\subseteq V$, pemetaan restriksi

$$
\rho_{V,U}:\mathcal F(V)\longrightarrow\mathcal F(U)
$$

merupakan homomorfisme gelanggang.

### Catatan 3.16: praberkas sebagai funktor {#br-bgk-2019-l03-rem-01}

Sebuah praberkas $\mathcal F$ pada ruang topologis $(X,\mathcal T)$ dapat
dipandang sebagai funktor kontravarian

$$
\mathcal F:\mathcal T\longrightarrow\operatorname{MEN},
$$

dengan $\mathcal T$ dipandang sebagai kategori sebagaimana pada Contoh
Lampiran 1.11. Demikian pula, sebuah praberkas grup komutatif merupakan
funktor kontravarian ke kategori grup komutatif, dan sebuah praberkas
gelanggang komutatif merupakan funktor kontravarian ke kategori gelanggang
komutatif, dan seterusnya.

### Definisi 3.17: grup topologis {#br-bgk-2019-l03-def-11}

Sebuah *grup topologis* adalah grup $G$ yang sekaligus merupakan ruang
topologis, sedemikian sehingga operasi grup

$$
G\times G\longrightarrow G,
\qquad (g,h)\longmapsto g\circ h,
$$

dan operasi invers

$$
G\longrightarrow G,
\qquad g\longmapsto g^{-1},
$$

merupakan pemetaan kontinu.

Contoh grup topologis adalah

$$
(\mathbb R,+),\quad
(\mathbb R\setminus\{0\},\cdot),\quad
(\mathbb C,+),\quad
(\mathbb C\setminus\{0\},\cdot),\quad
(\mathbb R^n,+),
$$

lingkaran $S^1$ dengan penjumlahan sudut, grup linear umum
$\operatorname{GL}_n(\mathbb R)$ dan $\operatorname{GL}_n(\mathbb C)$,
serta torus kompleks $\mathbb C/\Gamma$ untuk suatu kisi
$\Gamma\subseteq\mathbb C$. Setiap grup dapat dijadikan grup topologis
dengan topologi diskret.

Untuk ruang topologis $X$, himpunan pemetaan kontinu dari $X$ ke grup
topologis $G$ sendiri merupakan grup dengan operasi alami. Restriksi ke
himpunan terbuka merupakan homomorfisme grup. Karena itu, penetapan

$$
U\longmapsto C^0(U,G)
$$

merupakan praberkas grup pada $X$.

## Tangkai praberkas {#br-bgk-2019-l03-s04}

Salah satu gagasan dasar bundel vektor dan praberkas adalah memisahkan
secara bermakna sifat lokal dan global objek geometris, lalu memahami
interaksi keduanya. Sifat lokal, misalnya, ialah sifat yang berlaku pada
himpunan terbuka yang “kecil”. Sering kali kita ingin mengganti himpunan
terbuka kecil dengan himpunan yang lebih kecil lagi, khususnya untuk
memahami perilaku di lingkungan sekecil apa pun dari sebuah titik. Untuk
itu, kita perkenalkan konsep-konsep berikut.

### Definisi 3.18: filter topologis {#br-bgk-2019-l03-def-12}

Misalkan $X$ sebuah ruang topologis. Sebuah sistem $F$ yang terdiri atas
himpunan-himpunan terbuka dari $X$ disebut *filter* jika, untuk himpunan
terbuka $U$ dan $V$, berlaku:

1. $X\in F$;
2. jika $U\in F$ dan $U\subseteq V$, maka $V\in F$;
3. jika $U\in F$ dan $V\in F$, maka $U\cap V\in F$.

Contoh terpenting di sini ialah filter lingkungan suatu titik: filter itu
terdiri atas semua lingkungan terbuka dari titik tetap tersebut.

> **Catatan edisi - kalimat sumber yang rusak.** Sumber mencetak kalimat
> “Die wichtigsten Filter sind für und die Umgebungsfilter zu einer Punkt,
> der aus allen offenen Mengen eines fixierten Punktes besteht.” Kalimat itu
> rusak secara gramatikal. Berdasarkan definisi yang baru diberikan dan
> pemakaian filter pada definisi tangkai di bawah, edisi menampilkan bacaan
> kontekstual yang lengkap tentang filter lingkungan, tanpa mengatribusikan
> rekonstruksi ini kepada penulis sumber.

### Definisi 3.19: himpunan terarah {#br-bgk-2019-l03-def-13}

Sebuah himpunan terurut $(I,\preccurlyeq)$ disebut *terarah* jika untuk
setiap $i,j\in I$ terdapat $k\in I$ sedemikian sehingga

$$
i,j\preccurlyeq k.
$$

Kita memandang filter topologis sebagai himpunan yang diurutkan oleh
inklusi. Sifat irisan filter menjadikannya himpunan terarah; konvensi
arahnya ialah $\preccurlyeq\,=\,\supseteq$.

### Definisi 3.20: sistem terurut dan sistem terarah {#br-bgk-2019-l03-def-14}

Misalkan $(I,\preccurlyeq)$ sebuah himpunan indeks terurut. Sebuah keluarga

$$
M_i,\qquad i\in I,
$$

disebut *sistem terurut himpunan* jika:

1. untuk $i\preccurlyeq j$ terdapat pemetaan
   $\varphi_{ij}:M_i\to M_j$;
2. untuk $i\preccurlyeq j\preccurlyeq k$ berlaku
   $\varphi_{ik}=\varphi_{jk}\circ\varphi_{ij}$.

Jika himpunan indeksnya juga terarah, keluarga tersebut disebut *sistem
terarah himpunan*.

Jika semua $M_i$ merupakan grup, masing-masing gelanggang, dan semua
pemetaan di antaranya merupakan homomorfisme grup, masing-masing
homomorfisme gelanggang, kita berbicara tentang sistem terurut atau terarah
grup, masing-masing gelanggang.

### Definisi 3.21: kolimit {#br-bgk-2019-l03-def-15}

Misalkan $(M_i)_{i\in I}$ sebuah sistem terarah himpunan. *Kolimit*, yang
juga disebut limit langsung atau limit induktif, dari sistem itu ialah

$$
\operatorname{colim}_{i\in I}M_i
=\left(\biguplus_{i\in I}M_i\right)\big/\!\sim.
$$

Di sini, $\sim$ adalah relasi ekuivalensi yang menyatakan dua unsur
$m\in M_i$ dan $n\in M_j$ ekuivalen jika terdapat $k\in I$ dengan
$i,j\preccurlyeq k$ dan

$$
\varphi_{ik}(m)=\varphi_{jk}(n).
$$

Khususnya, $s_i\in M_i$ ekuivalen dengan citranya
$\varphi_{ik}(s_i)\in M_k$ untuk semua $i\preccurlyeq k$. Jika sistemnya
merupakan sistem terarah grup atau gelanggang, kolimit himpunan tersebut
juga dapat diberi struktur grup atau gelanggang. Alasannya, dua unsur
kolimit yang diwakili oleh $s_i\in M_i$ dan $s_j\in M_j$ dapat
diidentifikasi dengan citra mereka dalam suatu $M_k$ dengan
$i,j\preccurlyeq k$; operasi lalu dilakukan di sana. Lihat Soal 3.13.

Contoh utama kita ialah sistem terarah yang ditentukan oleh filter topologis
untuk sebuah praberkas $\mathcal F$ pada $X$, yakni

$$
\mathcal F(U),\qquad U\in F.
$$

### Definisi 3.22: tangkai pada suatu titik {#br-bgk-2019-l03-def-16}

Untuk praberkas $\mathcal F$ pada ruang topologis $X$ dan titik $P\in X$,

$$
\mathcal F_P
:=\operatorname{colim}_{P\in U}\Gamma(U,\mathcal F)
$$

disebut *tangkai* praberkas di titik $P$.

Khususnya, setiap seksi $s\in\mathcal F(U)$ dan setiap titik $P\in U$
menentukan unsur tunggal

$$
s_P\in\mathcal F_P,
$$

yang disebut *germ* dari $s$ di $P$. Pemetaan

$$
\mathcal F(U)\longrightarrow\mathcal F_P,
\qquad s\longmapsto s_P,
$$

disebut pemetaan restriksi dan dinotasikan dengan $\rho_{U,P}$. Untuk
$P\in V\subseteq U$, diagram berikut komutatif:

$$
\begin{array}{ccc}
\mathcal F(U)&\xrightarrow{\rho_{U,V}}&\mathcal F(V)\\
&\searrow\scriptstyle\rho_{U,P}&\downarrow\scriptstyle\rho_{V,P}\\
&&\mathcal F_P.
\end{array}
$$

### Definisi 3.23: tangkai pada suatu filter {#br-bgk-2019-l03-def-17}

Untuk praberkas $\mathcal G$ pada ruang topologis $X$ dan filter topologis
$F$,

$$
\mathcal G_F
:=\operatorname{colim}_{U\in F}\Gamma(U,\mathcal G)
$$

disebut *tangkai* praberkas pada filter $F$.

## Morfisme praberkas {#br-bgk-2019-l03-s05}

### Definisi 3.24: morfisme praberkas {#br-bgk-2019-l03-def-18}

Misalkan $\mathcal F$ dan $\mathcal G$ praberkas pada ruang topologis $X$.
Sebuah *morfisme praberkas*

$$
\varphi:\mathcal F\longrightarrow\mathcal G
$$

adalah keluarga pemetaan

$$
\varphi_U:\mathcal F(U)\longrightarrow\mathcal G(U)
$$

untuk setiap himpunan terbuka $U\subseteq X$, sedemikian sehingga untuk
setiap inklusi terbuka $U\subseteq V$ diagram berikut komutatif:

$$
\begin{array}{ccc}
\mathcal F(V)&\xrightarrow{\varphi_V}&\mathcal G(V)\\
\downarrow\scriptstyle\rho^{\mathcal F}_{V,U}&&
\downarrow\scriptstyle\rho^{\mathcal G}_{V,U}\\
\mathcal F(U)&\xrightarrow{\varphi_U}&\mathcal G(U).
\end{array}
$$

> **Catatan edisi - diagram sumber berlawanan arah.** Untuk
> $U\subseteq V$, diagram sumber menempatkan $\mathcal F(U)$ dan
> $\mathcal G(U)$ pada baris atas, $\mathcal F(V)$ dan $\mathcal G(V)$ pada
> baris bawah, lalu memberi panah vertikal ke bawah label $\rho_{U,V}$.
> Praberkas bersifat kontravarian, sehingga pemetaan restriksinya justru
> berjalan dari nilai pada $V$ ke nilai pada $U$. Edisi menampilkan diagram
> bertipe benar di atas, dengan superskrip yang membedakan kedua praberkas;
> tata letak sumber dipertahankan dalam catatan ini.

### Definisi 3.25: isomorfisme praberkas {#br-bgk-2019-l03-def-19}

Sebuah morfisme praberkas
$\varphi:\mathcal F\to\mathcal G$ pada $X$ disebut *isomorfisme* jika,
untuk setiap himpunan terbuka $U\subseteq X$, pemetaan

$$
\varphi_U:\mathcal F(U)\longrightarrow\mathcal G(U)
$$

merupakan bijeksi.

### Lema 3.26: identitas, komposisi, dan inklusi {#br-bgk-2019-l03-lem-01}

Misalkan $X$ sebuah ruang topologis dan
$\mathcal F,\mathcal G,\mathcal H$ praberkas pada $X$. Pernyataan berikut
berlaku.

1. Identitas $\mathcal F\to\mathcal F$ merupakan morfisme praberkas.
2. Jika $\varphi:\mathcal F\to\mathcal G$ dan
   $\psi:\mathcal G\to\mathcal H$ merupakan morfisme praberkas, maka
   $\psi\circ\varphi$ juga merupakan morfisme praberkas.
3. Untuk subpraberkas $\mathcal F\subseteq\mathcal G$, inklusi alaminya
   merupakan morfisme praberkas.

> **Catatan edisi - salah ketik sumber.** Pada butir ketiga, sumber dan
> Soal 3.17 mencetak *Prägraben*, yang jelas merupakan salah ketik untuk
> *Prägarben* (praberkas). Edisi memakai bentuk matematis yang benar.

#### Bukti {#br-bgk-2019-l03-lem-01-proof}

Lihat Soal 3.17.

### Lema 3.27: morfisme pada tangkai {#br-bgk-2019-l03-lem-02}

Sebuah morfisme praberkas

$$
\varphi:\mathcal F\longrightarrow\mathcal G
$$

pada ruang topologis $X$ mendefinisikan, untuk setiap titik $P\in X$,
sebuah pemetaan antar-tangkai

$$
\varphi_P:\mathcal F_P\longrightarrow\mathcal G_P
$$

yang kompatibel dengan pemetaan restriksi. Artinya, untuk $P\in U$, diagram

$$
\begin{array}{ccc}
\mathcal F(U)&\xrightarrow{\varphi_U}&\mathcal G(U)\\
\downarrow\scriptstyle\rho_{U,P}&&\downarrow\scriptstyle\rho_{U,P}\\
\mathcal F_P&\xrightarrow{\varphi_P}&\mathcal G_P
\end{array}
$$

komutatif.

#### Bukti {#br-bgk-2019-l03-lem-02-proof}

Misalkan $s_P\in\mathcal F_P$. Berarti terdapat lingkungan terbuka
$P\in U\subseteq X$ dan suatu $s\in\mathcal F(U)$ dengan
$\rho_{U,P}(s)=s_P$. Tetapkan

$$
\varphi_P(s_P):=\rho_{U,P}\bigl(\varphi_U(s)\bigr).
$$

Kita harus menunjukkan bahwa definisi ini bebas dari wakil $s$ dan dari
$U$. Misalkan $t\in\mathcal F(V)$ adalah wakil lain. Karena $s_P=t_P$,
terdapat lingkungan terbuka

$$
P\in W\subseteq U\cap V
$$

sedemikian sehingga $s|_W=t|_W$. Maka

$$
\varphi_U(s)|_W
=\varphi_W(s|_W)
=\varphi_W(t|_W)
=\varphi_V(t)|_W,
$$

dan oleh karena itu

$$
\rho_{U,P}\bigl(\varphi_U(s)\bigr)
=\rho_{V,P}\bigl(\varphi_V(t)\bigr).
$$

Jadi pemetaan $\varphi_P$ terdefinisi dengan baik dan diagram di atas
komutatif.
