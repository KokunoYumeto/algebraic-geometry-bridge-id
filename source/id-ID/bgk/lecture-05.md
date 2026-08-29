---
title: "Kuliah 5 - Berkasisasi, Homomorfisme, dan Berkas Hasil Bagi"
stable_id: br-bgk-2019-l05
language: id-ID
source_course: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)"
source_author: "Holger Brenner"
frozen_revision_contributor: "Bocardodarapti"
upstream_title: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)/Vorlesung 5"
upstream_pageid: 109009
upstream_revid: 1003725
upstream_timestamp: "2025-06-08T15:27:50Z"
upstream_mediawiki_sha1: 1697741995f2c7537d0b38edc16fe8df38024e13
source_url: "https://de.wikiversity.org/w/index.php?oldid=1003725"
authority_manifest: authority/wikiversity-bgk/unit-05/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 328774ffd66341ba8841b86935037a043067202dd10916d3e0be5082faeac35e
lecture_xml: authority/wikiversity-bgk/unit-05/lecture-05.xml
lecture_xml_sha256: edc881b76f88954eeceb7fa0a1902791218e064b947adee9e01119969c21c237
lecture_expanded_tex: authority/wikiversity-bgk/unit-05/lecture-05-expanded.tex
lecture_expanded_tex_sha256: d5d29f43c3209ccf8c8f80290ba3e44e800552807d4975ae0e78cb2dcd73735f
official_pdf: authority/artifacts/bgk-lecture-05-official.pdf
official_pdf_sha256: 85be007896876a0717ef5eddfe64ed919aeb6559dce44ec2828ffe2b1d755085
license: "Frozen semantic course text and this translation: CC BY-SA 4.0. Official PDF witnesses retain their recorded component notices; no blanket relicensing claim is made."
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra."
---

# Kuliah 5: Berkasisasi, Homomorfisme, dan Berkas Hasil Bagi {#br-bgk-2019-l05}

## Berkasisasi {#br-bgk-2019-l05-s01}

Sebuah praberkas dapat secara kanonik dikaitkan dengan sebuah berkas.
Konstruksi ini disebut *berkasisasi*.

### Definisi 5.1: berkasisasi {#br-bgk-2019-l05-def-01}

Misalkan $\mathcal F$ sebuah praberkas pada ruang topologis $X$. Praberkas
yang diberikan oleh

$$
\widetilde{\mathcal F}(U)
:=
\left\{
(s_P)_{P\in U}\in\prod_{P\in U}\mathcal F_P
\ \middle|\
\begin{array}{l}
\text{untuk setiap }P\in U\text{ terdapat himpunan terbuka }V\\
\text{dengan }P\in V\subseteq U\text{ dan }t\in\mathcal F(V)\\
\text{sedemikian sehingga }s_Q=t_Q\text{ di }\mathcal F_Q
\text{ bagi setiap }Q\in V
\end{array}
\right\},
$$

bersama pemetaan restriksi alami, disebut *berkasisasi* dari $\mathcal F$.

Syarat dalam definisi ini, yakni bahwa seksi-seksi lokal mendefinisikan
germ yang sama di setiap tangkai, juga disebut *syarat kompatibilitas*.

> **Catatan edisi - sifat terbuka lingkungan lokal.** Rumus sumber hanya
> menulis $P\in V\subseteq U$ tanpa menyebutkan bahwa $V$ terbuka. Karena
> $\mathcal F(V)$ dan konstruksi lokal ini menggunakan objek praberkas,
> $V$ harus berupa lingkungan terbuka. Edisi menyatakan syarat tersebut
> secara eksplisit.

### Lema 5.2: sifat-sifat berkasisasi {#br-bgk-2019-l05-lem-01}

Misalkan $\mathcal F$ sebuah praberkas pada ruang topologis $X$, dan
misalkan $\widetilde{\mathcal F}$ berkasisasinya. Sifat-sifat berikut
berlaku.

1. Terdapat morfisme praberkas alami

   $$
   \eta:\mathcal F\longrightarrow\widetilde{\mathcal F},
   $$

   yang pada setiap himpunan terbuka $U$ diberikan oleh

   $$
   \begin{aligned}
   \eta_U:\mathcal F(U)&\longrightarrow\widetilde{\mathcal F}(U),\\
   s&\longmapsto(s_P)_{P\in U}.
   \end{aligned}
   $$

2. Untuk setiap $P\in X$, terdapat isomorfisme alami

   $$
   \widetilde{\mathcal F}_P\cong\mathcal F_P.
   $$

3. Berkasisasi $\widetilde{\mathcal F}$ merupakan sebuah berkas.

4. Jika $\mathcal F$ sudah merupakan sebuah berkas, maka morfisme alami

   $$
   \mathcal F\longrightarrow\widetilde{\mathcal F}
   $$

   merupakan isomorfisme.

5. Untuk setiap morfisme praberkas

   $$
   \psi:\mathcal F\longrightarrow\mathcal G
   $$

   ke sebuah berkas $\mathcal G$, terdapat tepat satu faktorisasi

   $$
   \widetilde\psi:
   \widetilde{\mathcal F}\longrightarrow\mathcal G.
   $$

#### Bukti {#br-bgk-2019-l05-lem-01-proof}

1. Sebuah unsur $s\in\mathcal F(U)$ mendefinisikan tupel

   $$
   (s_P)_{P\in U},
   $$

   yang langsung memenuhi syarat kompatibilitas. Jadi terdapat pemetaan
   yang terdefinisi dengan baik

   $$
   \eta_U:\mathcal F(U)\longrightarrow\widetilde{\mathcal F}(U).
   $$

   Jika $V\subseteq U$, terdapat diagram komutatif

   $$
   \begin{array}{ccc}
   \mathcal F(U)
   &\xrightarrow{\ \eta_U\ }&
   \displaystyle\prod_{P\in U}\mathcal F_P\\[2mm]
   {\scriptstyle\rho_{U,V}}\downarrow
   &&
   \downarrow\\[2mm]
   \mathcal F(V)
   &\xrightarrow{\ \eta_V\ }&
   \displaystyle\prod_{P\in V}\mathcal F_P.
   \end{array}
   $$

   Komutativitasnya mengikuti dari fakta bahwa germ suatu seksi pada
   tangkai di sebuah titik hanya bergantung pada lingkungan-lingkungan
   terbuka titik tersebut.

2. Menurut bagian (1) dan Lema 3.27, terdapat pemetaan alami

   $$
   \mathcal F_P\longrightarrow\widetilde{\mathcal F}_P.
   $$

   Untuk membuktikan surjektivitasnya, ambil
   $s\in\widetilde{\mathcal F}_P$, yang diwakili oleh suatu

   $$
   s'\in\widetilde{\mathcal F}(U).
   $$

   Pada suatu lingkungan terbuka $V\subseteq U$ dari $P$, seksi tersebut
   diwakili oleh sebuah unsur

   $$
   s''\in\mathcal F(V).
   $$

   Germ $s''_P\in\mathcal F_P$ langsung merupakan praimaj dari $s$.

   Untuk membuktikan injektivitasnya, misalkan
   $s,t\in\mathcal F_P$ mempunyai citra yang sama dalam
   $\widetilde{\mathcal F}_P$. Kita dapat menganggap $s$ dan $t$ diwakili
   oleh seksi-seksi pada himpunan terbuka yang sama, katakanlah $U$.
   Kesamaan di tangkai berkasisasi berarti bahwa terdapat lingkungan
   terbuka $P\in V\subseteq U$ dengan

   $$
   (s_Q)_{Q\in V}=(t_Q)_{Q\in V}.
   $$

   Khususnya, germ kedua seksi di $P$ sama, sehingga $s=t$ dalam
   $\mathcal F_P$.

3. Misalkan

   $$
   U=\bigcup_{i\in I}U_i
   $$

   sebuah penutup terbuka, dan misalkan

   $$
   s,t\in\Gamma(U,\widetilde{\mathcal F})
   $$

   memenuhi

   $$
   s|_{U_i}=t|_{U_i}
   $$

   bagi setiap $i$. Setiap titik $P\in U$ terletak di suatu $U_i$, sehingga

   $$
   s_P=t_P
   $$

   bagi setiap $P\in U$. Jadi kedua tupel di dalam produk tangkai sama,
   dan karenanya $s=t$ dalam berkasisasi.

   Sekarang misalkan diberikan seksi-seksi

   $$
   s_i\in\widetilde{\mathcal F}(U_i)
   $$

   dengan

   $$
   s_i|_{U_i\cap U_j}=s_j|_{U_i\cap U_j}.
   $$

   Untuk setiap $P\in U$, salah satu $s_i$ dengan $P\in U_i$ menentukan
   sebuah germ $s_P$. Germ ini tunggal karena syarat kompatibilitas pada
   irisan. Tupel

   $$
   (s_P)_{P\in U}
   $$

   langsung memenuhi syarat kompatibilitas dalam definisi berkasisasi.
   Dengan demikian, $\widetilde{\mathcal F}$ memenuhi kedua syarat berkas.

4. Menurut bagian (1), terdapat morfisme praberkas

   $$
   \mathcal F\longrightarrow\widetilde{\mathcal F}.
   $$

   Menurut bagian (2), morfisme ini bijektif pada setiap tangkai. Sisi kiri
   merupakan berkas menurut hipotesis, dan sisi kanan merupakan berkas
   menurut bagian (3). Lema 4.6 menunjukkan bahwa morfisme tersebut
   merupakan isomorfisme.

5. Lihat Soal 5.2. $\square$

> **Catatan edisi - salah artikel pada sumber.** Pada butir (4), sumber
> mencetak *die natürliche Morphismus*. Bentuk Jerman yang benar ialah
> *der natürliche Morphismus*. Terjemahan memakai bentuk matematis yang
> dimaksud, yaitu "morfisme alami". (Salah ketik judul *Garbenmorpismen*
> pada sumber juga dipertahankan sebagai bagian dari catatan otoritas Unit 4;
> istilah yang dipakai di sini tetap "morfisme berkas".)

## Homomorfisme berkas grup {#br-bgk-2019-l05-s02}

### Definisi 5.3: homomorfisme berkas grup komutatif {#br-bgk-2019-l05-def-02}

Misalkan $X$ sebuah ruang topologis, dan misalkan $\mathcal F$ serta
$\mathcal G$ berkas grup komutatif pada $X$. Sebuah morfisme berkas

$$
\varphi:\mathcal F\longrightarrow\mathcal G
$$

disebut *homomorfisme berkas grup komutatif* jika, untuk setiap himpunan
terbuka $U\subseteq X$, pemetaan

$$
\varphi_U:\mathcal F(U)\longrightarrow\mathcal G(U)
$$

merupakan homomorfisme grup.

### Contoh 5.4: homomorfisme yang diinduksi oleh grup topologis {#br-bgk-2019-l05-exa-01}

Sebuah homomorfisme grup kontinu

$$
\varphi:F\longrightarrow G
$$

di antara grup-grup topologis $F$ dan $G$ menentukan, pada setiap ruang
topologis $X$, sebuah homomorfisme berkas grup. Pada setiap himpunan terbuka
$U$, homomorfisme itu diberikan oleh

$$
\begin{aligned}
C^0(U,F)&\longrightarrow C^0(U,G),\\
f&\longmapsto\varphi\circ f.
\end{aligned}
$$

> **Catatan lingkup.** Definisi 5.3 dirumuskan untuk berkas grup komutatif,
> sedangkan contoh sumber ini memakai grup topologis umum. Konstruksi
> komposisi di atas memang tidak memerlukan komutativitas; karena itu edisi
> menyebutnya homomorfisme berkas grup pada tingkat umum.

### Definisi 5.5: berkas kernel {#br-bgk-2019-l05-def-03}

Misalkan $X$ sebuah ruang topologis dan

$$
\varphi:\mathcal F\longrightarrow\mathcal G
$$

sebuah homomorfisme berkas grup komutatif. Subberkas dari $\mathcal F$ yang
didefinisikan oleh

$$
(\ker\varphi)(U):=\ker\varphi_U
$$

disebut *berkas kernel* dari $\varphi$.

Lebih tepatnya, berkas tersebut merupakan subberkas grup komutatif: bagi
setiap himpunan terbuka $U$, nilainya adalah sebuah subgrup dari
$\mathcal F(U)$; lihat Soal 5.6.

### Definisi 5.6: berkas citra {#br-bgk-2019-l05-def-04}

Misalkan $X$ sebuah ruang topologis dan

$$
\varphi:\mathcal F\longrightarrow\mathcal G
$$

sebuah homomorfisme berkas grup komutatif. Berkasisasi dari praberkas yang
diberikan oleh

$$
(\operatorname{im}\varphi)(U):=\operatorname{im}\varphi_U
$$

disebut *berkas citra* dari $\varphi$.

Menurut Lema 5.2(5), berkas citra secara alami merupakan subberkas
$\mathcal G$, dan lebih tepatnya subberkas grup komutatif. Berkas ini
ditulis $\operatorname{im}\varphi$.

### Contoh 5.7: homomorfisme bundel vektor trivial {#br-bgk-2019-l05-exa-02}

Misalkan $X$ sebuah ruang topologis dan

$$
\varphi:X\times\mathbb R^n\longrightarrow X\times\mathbb R^m
$$

sebuah homomorfisme di antara bundel-bundel vektor trivial. Homomorfisme ini
dideskripsikan oleh sebuah pemetaan kontinu

$$
M:X\longrightarrow
\operatorname{Mat}_{m\times n}\bigl(C^0(X,\mathbb R)\bigr),
$$

yakni setiap titik secara kontinu dipasangkan dengan sebuah matriks yang
pada titik tersebut mendeskripsikan pemetaan linear
$\mathbb R^n\to\mathbb R^m$. Hal ini langsung dapat dipandang sebagai
homomorfisme berkas grup pada $X$:

$$
\begin{aligned}
C^0(-,\mathbb R)^n&\longrightarrow C^0(-,\mathbb R)^m,\\
\begin{pmatrix}
f_1\\
\vdots\\
f_n
\end{pmatrix}
&\longmapsto
M
\begin{pmatrix}
f_1\\
\vdots\\
f_n
\end{pmatrix}.
\end{aligned}
$$

Dalam Contoh 1.2, untuk $X=\mathbb R^3$, terdapat pemetaan

$$
\begin{aligned}
\varphi:\mathbb R^3\times\mathbb R^3
&\longrightarrow\mathbb R^3\times\mathbb R,\\
(r,s,t;u,v,w)&\longmapsto(r,s,t;ru+sv+tw),
\end{aligned}
$$

atau, secara ekuivalen,

$$
\begin{aligned}
M:\mathbb R^3&\longrightarrow
\operatorname{Mat}_{1\times3}(K),\\
(r,s,t)&\longmapsto(r,s,t).
\end{aligned}
$$

> **Catatan edisi - dua ketidakcocokan jenis pada notasi matriks sumber.**
> Sumber menulis
> $M:X\to\operatorname{Mat}_{m\times n}(C^0(X,\mathbb R))$, sedangkan
> uraian sesudahnya memperlakukan $M$ sebagai fungsi matriks bernilai titik.
> Bentuk berjenis yang lazim ialah
> $M:X\to\operatorname{Mat}_{m\times n}(\mathbb R)$, atau secara ekuivalen
> $M\in\operatorname{Mat}_{m\times n}(C^0(X,\mathbb R))$. Pada contoh real
> konkret, sumber juga menulis $\operatorname{Mat}_{1\times3}(K)$ meskipun
> $K$ tidak didefinisikan dan konteksnya menggunakan $\mathbb R$. Kedua
> rumus sumber dipertahankan di atas agar penyimpangan tersebut tetap
> terlihat.

Berkas kernel di atas $U$ adalah

$$
\begin{aligned}
(\ker\varphi)(U)
&=
\left\{
\begin{pmatrix}
f_1\\
\vdots\\
f_n
\end{pmatrix}
\in C^0(U,\mathbb R)^n
\ \middle|\
M
\begin{pmatrix}
f_1\\
\vdots\\
f_n
\end{pmatrix}
=0
\right\}\\
&\subseteq C^0(U,\mathbb R)^n.
\end{aligned}
$$

## Berkas hasil bagi {#br-bgk-2019-l05-s03}

### Definisi 5.8: berkas hasil bagi {#br-bgk-2019-l05-def-05}

Misalkan $\mathcal G$ sebuah berkas grup komutatif dan

$$
\mathcal F\subseteq\mathcal G
$$

sebuah subberkas grup. Berkasisasi dari praberkas

$$
U\longmapsto\mathcal G(U)/\mathcal F(U)
$$

disebut *berkas hasil bagi* dari $\mathcal G$ oleh $\mathcal F$.

Berkas hasil bagi ditulis $\mathcal G/\mathcal F$. Karena konstruksinya
memakai berkasisasi, secara umum tidak harus berlaku

$$
(\mathcal G/\mathcal F)(U)
=
\mathcal G(U)/\mathcal F(U).
$$

Namun, untuk setiap titik $P\in X$, berlaku

$$
(\mathcal G/\mathcal F)_P
=
\mathcal G_P/\mathcal F_P;
$$

lihat Soal 5.11.

### Lema 5.9: deskripsi eksplisit berkas hasil bagi {#br-bgk-2019-l05-lem-02}

Misalkan $\mathcal G$ sebuah berkas grup komutatif dan

$$
\mathcal F\subseteq\mathcal G
$$

sebuah subberkas grup, dengan berkas hasil bagi
$\mathcal G/\mathcal F$. Pernyataan berikut berlaku.

1. Setiap unsur

   $$
   s\in\Gamma(X,\mathcal G/\mathcal F)
   $$

   diwakili oleh suatu keluarga

   $$
   (U_i,g_i)_{i\in I},
   $$

   dengan

   $$
   X=\bigcup_{i\in I}U_i
   $$

   sebuah penutup terbuka dan

   $$
   g_i\in\Gamma(U_i,\mathcal G),
   $$

   sedemikian sehingga

   $$
   g_i|_{U_i\cap U_j}-g_j|_{U_i\cap U_j}
   \in\Gamma(U_i\cap U_j,\mathcal F).
   $$

   Setiap keluarga semacam itu menentukan sebuah unsur
   $\Gamma(X,\mathcal G/\mathcal F)$.

2. Dua keluarga

   $$
   (U_i,g_i)_{i\in I}
   \qquad\text{dan}\qquad
   (U_i,h_i)_{i\in I}
   $$

   pada penutup terbuka yang sama menentukan unsur yang sama dalam

   $$
   \Gamma(X,\mathcal G/\mathcal F)
   $$

   tepat ketika

   $$
   g_i-h_i\in\Gamma(U_i,\mathcal F)
   $$

   bagi setiap $i$.

3. Dua keluarga

   $$
   (U_i,g_i)_{i\in I}
   \qquad\text{dan}\qquad
   (V_j,h_j)_{j\in J}
   $$

   menentukan unsur yang sama tepat ketika, pada suatu - dan karenanya
   pada setiap - penghalusan bersama kedua penutup, selisih seksi-seksinya
   termasuk dalam $\mathcal F$.

#### Bukti {#br-bgk-2019-l05-lem-02-proof}

1. Homomorfisme berkas kanonik

   $$
   \mathcal G\longrightarrow\mathcal G/\mathcal F
   $$

   bersifat surjektif. Oleh karena itu, setiap seksi

   $$
   s\in\Gamma(X,\mathcal G/\mathcal F)
   $$

   mempunyai praimaj secara lokal. Dengan demikian, terdapat penutup
   terbuka

   $$
   X=\bigcup_{i\in I}U_i
   $$

   dan unsur-unsur

   $$
   g_i\in\Gamma(U_i,\mathcal G)
   $$

   yang dipetakan ke $s|_{U_i}$. Maka

   $$
   g_i|_{U_i\cap U_j}-g_j|_{U_i\cap U_j}
   \in\Gamma(U_i\cap U_j,\mathcal G)
   $$

   dipetakan ke nol, sehingga selisih ini termasuk dalam kernel, yakni
   $\mathcal F$.

   Sebaliknya, sebuah keluarga yang memenuhi syarat tersebut menentukan
   kelas-kelas

   $$
   [g_i]\in\Gamma(U_i,\mathcal G/\mathcal F).
   $$

   Pada setiap irisan berlaku

   $$
   \begin{aligned}
   [g_i]|_{U_i\cap U_j}-[g_j]|_{U_i\cap U_j}
   &=
   [g_i|_{U_i\cap U_j}-g_j|_{U_i\cap U_j}]\\
   &=0.
   \end{aligned}
   $$

   Jadi kelas-kelas tersebut kompatibel dan menentukan sebuah seksi global
   berkas hasil bagi.

2. Dengan mengganti kedua keluarga oleh keluarga selisihnya, cukup dibahas
   kasus $h_i=0$. Kita harus menunjukkan bahwa $(U_i,g_i)$ menentukan
   unsur nol dalam berkas hasil bagi tepat ketika setiap

   $$
   g_i\in\Gamma(U_i,\mathcal F).
   $$

   Jika keluarga tersebut menentukan unsur nol, citranya pada setiap
   tangkai juga nol. Jadi, untuk setiap $P\in U_i$, germnya memenuhi

   $$
   (g_i)_P\in\mathcal F_P.
   $$

   Keanggotaan pada sebuah subberkas dapat diuji pada tangkai, sehingga

   $$
   g_i\in\Gamma(U_i,\mathcal F).
   $$

   Arah sebaliknya langsung.

3. Kesamaan seksi sebuah berkas dapat diuji secara lokal pada sebarang
   penutup terbuka. Pernyataan mengikuti dari bagian (2) serta fakta bahwa
   keanggotaan pada sebuah subberkas juga dapat diuji secara lokal.
   $\square$

> **Catatan edisi - seksi dan germ pada pembuktian sumber.** Pada butir (2),
> sumber menulis $g_i\in\mathcal F_P$, padahal $g_i$ adalah seksi di
> $U_i$, sedangkan $\mathcal F_P$ adalah tangkai. Pernyataan berjenis yang
> dipakai di atas ialah $(g_i)_P\in\mathcal F_P$.
