---
title: "Kuliah 4 - Berkas dan Morfisme Berkas"
stable_id: br-bgk-2019-l04
language: id-ID
source_course: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)"
source_author: "Holger Brenner"
frozen_revision_contributor: "Bocardodarapti"
upstream_title: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)/Vorlesung 4"
upstream_pageid: 109008
upstream_revid: 1003714
upstream_timestamp: "2025-06-08T15:26:17Z"
upstream_mediawiki_sha1: 8eceb7ac307706e0858ffa278bd9d1235574a596
source_url: "https://de.wikiversity.org/w/index.php?oldid=1003714"
authority_manifest: authority/wikiversity-bgk/unit-04/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 3f26616ff7e9f4ac0d5bb0e64ad8435fefc18e32e4c91b16d780d4346498f680
lecture_xml: authority/wikiversity-bgk/unit-04/lecture-04.xml
lecture_xml_sha256: 008241be410fe252da296e8332fa11c1db08960ff84eaac3c073564007d5845a
lecture_expanded_tex: authority/wikiversity-bgk/unit-04/lecture-04-expanded.tex
lecture_expanded_tex_sha256: 4dc55e0810888863946316396cff73ce5ef1a1bb9b46864b64b3ed80ba3a8ea1
official_pdf: authority/artifacts/bgk-lecture-04-official.pdf
official_pdf_sha256: 9e6dd93da57ae35f96568fc717442ac4c6fb209733527143068c34f32248d222
license: "Frozen semantic course text and this translation: CC BY-SA 4.0. Official PDF and media retain their recorded component notices; no blanket relicensing claim is made."
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra."
---

# Kuliah 4: Berkas dan Morfisme Berkas {#br-bgk-2019-l04}

![Berkas-berkas gandum spelta yang berdiri tegak di sebuah ladang](authority/assets/bgk-u04-triticum-spelta.jpg)

*Berkas gandum spelta. André Karwath aka Aka, CC BY-SA 2.5; lihat kredit
media Unit 4.*

## Berkas {#br-bgk-2019-l04-s01}

### Definisi 4.1: berkas {#br-bgk-2019-l04-def-01}

Misalkan $X$ sebuah ruang topologis. Sebuah *berkas* $\mathcal F$ pada $X$
adalah praberkas $\mathcal F$ pada $X$ yang memenuhi kedua sifat berikut.

1. Untuk setiap penutup terbuka

   $$
   U=\bigcup_{i\in I}U_i
   $$

   dan setiap $s,t\in\mathcal F(U)$ dengan

   $$
   \rho_{U,U_i}(s)=\rho_{U,U_i}(t)
   $$

   bagi semua $i\in I$, berlaku $s=t$.

2. Untuk setiap penutup terbuka

   $$
   U=\bigcup_{i\in I}U_i
   $$

   dan setiap keluarga $s_i\in\mathcal F(U_i)$ yang kompatibel, yakni

   $$
   \rho_{U_i,U_i\cap U_j}(s_i)
   =\rho_{U_j,U_i\cap U_j}(s_j)
   $$

   bagi semua $i,j\in I$, terdapat suatu $s\in\mathcal F(U)$ dengan

   $$
   s_i=\rho_{U,U_i}(s)
   $$

   bagi semua $i\in I$.

Kedua sifat ini disebut *syarat-syarat Serre*. Syarat pertama menyatakan
bahwa kesamaan seksi dapat diperiksa secara lokal pada suatu penutup terbuka.
Syarat kedua menyatakan bahwa seksi-seksi lokal yang saling cocok berasal
dari sebuah seksi global. Seksi global itu tunggal menurut syarat pertama.

Nilai $\mathcal F(\varnothing)$ terdiri atas tepat satu unsur. Secara teori
himpunan, hal ini mengikuti dengan menerapkan kedua syarat tersebut pada
penutup himpunan kosong yang mempunyai himpunan indeks kosong.

Sebagai wakil dari banyak contoh serupa, kita tunjukkan bahwa praberkas
seksi dari suatu pemetaan kontinu merupakan berkas.

### Contoh 4.2: berkas seksi kontinu {#br-bgk-2019-l04-exa-01}

Kita lanjutkan Contoh 3.12. Misalkan $X$ dan $Y$ ruang topologis dan

$$
p:Y\longrightarrow X
$$

sebuah pemetaan kontinu tetap. Praberkas seksi kontinu di $Y$ diberikan
oleh

$$
U\longmapsto S(U,Y)
=\{s:U\to p^{-1}(U)\mid s\text{ seksi kontinu bagi }p\}.
$$

Praberkas ini merupakan berkas. Syarat Serre pertama berlaku karena dua
seksi sama apabila nilainya sama di setiap titik $P\in U$, dan kesamaan
tersebut dapat diperiksa secara lokal pada penutup terbuka. Untuk syarat
kedua, sebuah keluarga seksi kontinu yang kompatibel

$$
s_i:U_i\longrightarrow Y|_{U_i}
$$

secara langsung mendefinisikan sebuah seksi

$$
s:U\longrightarrow Y|_U
$$

yang sekaligus memperluas semua $s_i$. Pemetaan $s$ kontinu karena
kontinuitas dapat diperiksa secara lokal.

### Contoh 4.3: berkas pemetaan kontinu bernilai grup {#br-bgk-2019-l04-exa-02}

Misalkan $G$ sebuah grup topologis dan $X$ sebuah ruang topologis. Penetapan

$$
U\longmapsto C^0(U,G)
$$

merupakan berkas, yaitu berkas grup pemetaan kontinu bernilai di $G$.
Sifat berkas mengikuti dari dua fakta: kesamaan pemetaan kontinu dapat
diperiksa titik demi titik, dan pemetaan-pemetaan kontinu pada himpunan
terbuka yang berimpit pada setiap irisan dapat dilem menjadi sebuah pemetaan
kontinu global.

### Lema 4.4: uji lokal kesamaan seksi {#br-bgk-2019-l04-lem-01}

Misalkan $\mathcal F$ sebuah berkas pada ruang topologis $X$, dan misalkan

$$
s,t\in\mathcal F(X).
$$

Jika

$$
s_P=t_P
$$

di tangkai $\mathcal F_P$ untuk setiap $P\in X$, maka $s=t$.

#### Bukti {#br-bgk-2019-l04-lem-01-proof}

Menurut hipotesis, untuk setiap $P\in X$ terdapat lingkungan terbuka

$$
P\in U_P\subseteq X
$$

sedemikian sehingga

$$
\rho_{X,U_P}(s)=\rho_{X,U_P}(t).
$$

Karena

$$
X=\bigcup_{P\in X}U_P,
$$

syarat berkas pertama memberikan $s=t$.

## Morfisme berkas {#br-bgk-2019-l04-s02}

Morfisme berkas hanyalah morfisme praberkas antara dua berkas. Meskipun
demikian, ada beberapa kekhususan penting yang berkaitan dengan
injektivitas, surjektivitas, citra, dan uji isomorfisme lokal.

> **Catatan edisi - salah ketik pada judul sumber.** Sumber mencetak
> *Garbenmorpismen*; kata Jerman yang dimaksud ialah *Garbenmorphismen*.
> Edisi memakai istilah matematis yang benar, "morfisme berkas".

### Lema 4.5: injektivitas dapat diuji pada tangkai {#br-bgk-2019-l04-lem-02}

Misalkan $X$ sebuah ruang topologis dan

$$
\varphi:\mathcal F\longrightarrow\mathcal G
$$

sebuah morfisme berkas. Pernyataan berikut ekuivalen.

1. Pemetaan

   $$
   \varphi_U:\mathcal F(U)\longrightarrow\mathcal G(U)
   $$

   injektif untuk setiap himpunan terbuka $U\subseteq X$.

2. Pemetaan tangkai

   $$
   \varphi_P:\mathcal F_P\longrightarrow\mathcal G_P
   $$

   injektif untuk setiap $P\in X$.

#### Bukti {#br-bgk-2019-l04-lem-02-proof}

Pertama, andaikan semua pemetaan pada seksi di atas himpunan terbuka
injektif. Misalkan $s_P,t_P\in\mathcal F_P$ dan

$$
\varphi_P(s_P)=\varphi_P(t_P).
$$

Kita dapat mewakili keduanya oleh seksi $s,t\in\mathcal F(U)$ pada suatu
lingkungan terbuka $U$ dari $P$. Kesamaan di tangkai $\mathcal G_P$
memberikan lingkungan terbuka yang lebih kecil

$$
P\in U'\subseteq U
$$

dengan

$$
\varphi_{U'}(s|_{U'})=\varphi_{U'}(t|_{U'}).
$$

Injektivitas $\varphi_{U'}$ memberi $s|_{U'}=t|_{U'}$, sehingga
$s_P=t_P$.

Sebaliknya, andaikan semua pemetaan tangkai injektif. Misalkan
$s,t\in\mathcal F(U)$ dan $\varphi_U(s)=\varphi_U(t)$. Untuk setiap
$P\in U$ kita memperoleh

$$
\varphi_P(s_P)=\varphi_P(t_P),
$$

maka $s_P=t_P$. Dengan menerapkan Lema 4.4 pada pembatasan berkas ke $U$,
kita memperoleh $s=t$.

### Lema 4.6: uji isomorfisme pada tangkai {#br-bgk-2019-l04-lem-03}

Misalkan $X$ sebuah ruang topologis dan

$$
\varphi:\mathcal F\longrightarrow\mathcal G
$$

sebuah morfisme berkas. Morfisme $\varphi$ merupakan isomorfisme berkas
jika dan hanya jika, untuk setiap $P\in X$, pemetaan tangkai

$$
\varphi_P:\mathcal F_P\longrightarrow\mathcal G_P
$$

merupakan isomorfisme.

#### Bukti {#br-bgk-2019-l04-lem-03-proof}

Arah maju langsung. Untuk arah sebaliknya, kita harus menunjukkan bahwa

$$
\varphi_U:\mathcal F(U)\longrightarrow\mathcal G(U)
$$

bijektif untuk setiap himpunan terbuka $U\subseteq X$. Dengan membatasi
kedua berkas, cukup membahas kasus $U=X$. Injektivitas mengikuti dari
Lema 4.5.

Untuk surjektivitas, ambil $t\in\mathcal G(X)$. Bagi setiap $P\in X$,
terdapat tepat satu $s_P\in\mathcal F_P$ dengan

$$
\varphi_P(s_P)=t_P.
$$

Pilih wakil $r_P\in\mathcal F(U_P)$ pada suatu lingkungan terbuka $U_P$
dari $P$. Karena $\varphi(r_P)$ dan $t$ mempunyai germ yang sama di $P$,
setelah memperkecil $U_P$ bila perlu kita memperoleh

$$
\varphi_{U_P}(r_P)=t|_{U_P}.
$$

Himpunan-himpunan $U_P$ menutupi $X$. Pada $U_P\cap U_Q$ dan untuk setiap
$Z\in U_P\cap U_Q$, kedua germ $(r_P)_Z$ dan $(r_Q)_Z$ dipetakan oleh
isomorfisme $\varphi_Z$ ke $t_Z$. Jadi

$$
(r_P)_Z=(r_Q)_Z.
$$

Menurut Lema 4.4,

$$
r_P|_{U_P\cap U_Q}=r_Q|_{U_P\cap U_Q}.
$$

Syarat berkas kedua kemudian mengelem semua $r_P$ menjadi
$r\in\mathcal F(X)$. Pada setiap $U_P$ berlaku
$\varphi(r)|_{U_P}=t|_{U_P}$, sehingga syarat berkas pertama memberikan
$\varphi(r)=t$.

Pernyataan ini tidak berlaku untuk praberkas - pertimbangkan, misalnya,
berkasisasi suatu praberkas - dan juga tidak berlaku tanpa adanya sebuah
morfisme di antara kedua berkas. Dua berkas yang isomorfik pada setiap
tangkai belum tentu isomorfik sebagai berkas. Contoh pentingnya ialah berkas
bebas lokal: secara lokal berkas semacam ini isomorfik dengan berkas bebas,
tetapi secara umum tidak bebas secara global.

Sekilas mungkin mengejutkan bahwa, untuk morfisme berkas, surjektivitas pada
seksi di atas himpunan terbuka berbeda dari surjektivitas pada tangkai.
Perbedaan ini justru merupakan kekuatan teori berkas: kegagalan
surjektivitas global dari morfisme yang surjektif pada setiap tangkai dapat
mencerminkan sifat topologis ruang dasarnya.

### Definisi 4.7: morfisme berkas surjektif {#br-bgk-2019-l04-def-02}

Sebuah morfisme berkas

$$
\varphi:\mathcal F\longrightarrow\mathcal G
$$

pada ruang topologis $X$ disebut *surjektif* jika, untuk setiap titik
$P\in X$, pemetaan tangkai

$$
\varphi_P:\mathcal F_P\longrightarrow\mathcal G_P
$$

surjektif. Sifat ini jauh lebih lemah daripada surjektivitas pemetaan seksi
di atas setiap himpunan terbuka.

### Contoh 4.8: surjektif pada tangkai, tidak selalu pada seksi {#br-bgk-2019-l04-exa-03}

Perhatikan homomorfisme grup kontinu

$$
\varphi:\mathbb R\longrightarrow S^1,
\qquad
t\longmapsto(\cos t,\sin t),
$$

yaitu parametrisasi trigonometrik periodik lingkaran satuan. Pada setiap
ruang topologis $X$, pemetaan ini menginduksi morfisme berkas

$$
C^0(-,\mathbb R)\longrightarrow C^0(-,S^1),
$$

yang mengirim fungsi kontinu $f:U\to\mathbb R$ ke komposisi

$$
\varphi\circ f:U\longrightarrow S^1.
$$

Morfisme ini surjektif karena $\varphi$ dapat dibalik secara lokal. Namun,
pemetaan pada seksi tidak selalu surjektif. Jika $X=S^1$, misalnya,
identitas pada $S^1$ tidak mempunyai pengangkatan kontinu ke $\mathbb R$.

### Lema 4.9: berkas morfisme {#br-bgk-2019-l04-lem-04}

Untuk dua berkas $\mathcal F$ dan $\mathcal G$ pada ruang topologis $X$,
penetapan

$$
U\longmapsto
\operatorname{Mor}(\mathcal F|_U,\mathcal G|_U)
$$

merupakan sebuah berkas.

#### Bukti {#br-bgk-2019-l04-lem-04-proof}

Restriksi sebuah morfisme berkas

$$
\varphi:\mathcal F|_U\longrightarrow\mathcal G|_U
$$

ke setiap himpunan terbuka $V\subseteq U$ memberikan morfisme

$$
\varphi|_V:\mathcal F|_V\longrightarrow\mathcal G|_V.
$$

Jadi penetapan di atas mula-mula merupakan praberkas.

Misalkan $U=\bigcup_{i\in I}U_i$. Untuk syarat kesamaan, misalkan
$\varphi$ dan $\psi$ dua morfisme pada $U$ yang restriksinya sama pada
setiap $U_i$. Bagi setiap himpunan terbuka $V\subseteq U$ dan setiap
$s\in\mathcal F(V)$, seksi $\varphi_V(s)$ dan $\psi_V(s)$ pada
$\mathcal G(V)$ sama setelah direstriksi ke setiap $V\cap U_i$. Syarat
berkas pertama untuk $\mathcal G$ memberikan
$\varphi_V(s)=\psi_V(s)$. Karena ini berlaku untuk semua $V$ dan $s$,
kita memperoleh $\varphi=\psi$.

Untuk syarat pengeleman, misalkan diberikan morfisme

$$
\varphi_i:\mathcal F|_{U_i}\longrightarrow\mathcal G|_{U_i}
$$

yang memenuhi

$$
\varphi_i|_{U_i\cap U_j}=\varphi_j|_{U_i\cap U_j}.
$$

Untuk setiap himpunan terbuka $V\subseteq U$ dan setiap
$s\in\mathcal F(V)$, tetapkan pada $V\cap U_i$

$$
t_i=(\varphi_i)_{V\cap U_i}(s|_{V\cap U_i}).
$$

Keluarga $(t_i)$ kompatibel pada semua irisan, sehingga terdapat tepat satu
$t\in\mathcal G(V)$ dengan $t|_{V\cap U_i}=t_i$. Tetapkan

$$
\varphi_V(s):=t.
$$

Jika $W\subseteq V$, maka $\varphi_V(s)|_W$ dan
$\varphi_W(s|_W)$ mempunyai restriksi lokal yang sama pada setiap
$W\cap U_i$; ketunggalan pengeleman menunjukkan bahwa keduanya sama.
Jadi keluarga $\varphi_V$ kompatibel dengan semua pemetaan restriksi dan
benar-benar mendefinisikan morfisme berkas

$$
\varphi:\mathcal F|_U\longrightarrow\mathcal G|_U.
$$

Restriksinya pada setiap $U_i$ adalah $\varphi_i$, juga menurut ketunggalan
pengeleman.

> **Catatan edisi - pelengkapan pembuktian sumber.** Pembuktian sumber
> melakukan pemeriksaan kesamaan dan konstruksi pengeleman hanya pada seksi
> di atas $U$. Sebuah morfisme berkas harus mempunyai komponen pada setiap
> himpunan terbuka $V\subseteq U$ dan harus komutatif dengan restriksi.
> Pembuktian di atas menampilkan langkah standar yang hilang, menggunakan
> penutup $(V\cap U_i)_i$ dan ketunggalan pengeleman. Bentuk ringkas sumber
> tetap dipertahankan dalam batas otoritas Unit 4.

### Korolari 4.10: mengeleman morfisme berkas {#br-bgk-2019-l04-cor-01}

Misalkan

$$
X=\bigcup_{i\in I}U_i
$$

sebuah penutup terbuka ruang topologis $X$, dan misalkan $\mathcal F$ dan
$\mathcal G$ berkas pada $X$. Untuk setiap $i\in I$, misalkan diberikan
morfisme berkas

$$
\alpha_i:\mathcal F|_{U_i}\longrightarrow\mathcal G|_{U_i}
$$

dengan

$$
\alpha_i|_{U_i\cap U_j}=\alpha_j|_{U_i\cap U_j}
$$

bagi semua $i,j$. Maka terdapat tepat satu morfisme berkas

$$
\alpha:\mathcal F\longrightarrow\mathcal G
$$

yang memenuhi $\alpha|_{U_i}=\alpha_i$ untuk setiap $i$.

#### Bukti {#br-bgk-2019-l04-cor-01-proof}

Pernyataan ini langsung mengikuti Lema 4.9.

### Korolari 4.11: uji kesamaan pada tangkai {#br-bgk-2019-l04-cor-02}

Misalkan $\mathcal F$ dan $\mathcal G$ berkas pada ruang topologis $X$,
dan misalkan

$$
\alpha,\beta:\mathcal F\longrightarrow\mathcal G
$$

morfisme berkas. Maka

$$
\alpha=\beta
$$

jika dan hanya jika

$$
\alpha_P=\beta_P
$$

untuk setiap $P\in X$.

> **Catatan edisi - indeks sumber tidak konsisten.** Sumber menulis
> $\alpha_p=\beta_P$ setelah mengkuantifikasi titik $P$. Edisi memakai
> indeks yang konsisten, $\alpha_P=\beta_P$.

#### Bukti {#br-bgk-2019-l04-cor-02-proof}

Pernyataan ini langsung mengikuti Lema 4.9 dan Lema 4.4.
