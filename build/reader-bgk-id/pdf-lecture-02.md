---
title: "Kuliah 2 - Seksi, Teorema Bola Berbulu, dan Data Pengeleman"
stable_id: br-bgk-2019-l02
language: id-ID
source_course: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)"
source_author: "Holger Brenner"
frozen_revision_contributor: "Arbota"
upstream_title: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)/Vorlesung 2"
upstream_pageid: 109004
upstream_revid: 1019972
upstream_timestamp: "2025-08-09T13:35:26Z"
upstream_mediawiki_sha1: d666b90510ef490f9a1d545df6394ebc55d5dcc5
source_url: "https://de.wikiversity.org/w/index.php?oldid=1019972"
authority_manifest: authority/wikiversity-bgk/unit-02/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: a348b56811fe98266feff9108a21a436a9b8f07a343321feab7d9fbb3b75e64d
lecture_xml: authority/wikiversity-bgk/unit-02/lecture-02.xml
lecture_xml_sha256: 9e5823b1031d2d8877147923324a95a78ff255d00a840745fe6a83dddb749670
lecture_expanded_tex: authority/wikiversity-bgk/unit-02/lecture-02-expanded.tex
lecture_expanded_tex_sha256: ae973e45a0aa3228ac31a61dd71b995d7872bfaaf8adca164bd97bd045f000b3
official_pdf: authority/artifacts/bgk-lecture-02-official.pdf
official_pdf_sha256: b898d226f1b680d4fe08873402847c9580d05aca8ca430ea8e6cca466cbbc391
license: "Frozen semantic course text and this translation: CC BY-SA 4.0. Official PDF and media retain their recorded component notices; no blanket relicensing claim is made."
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra."
---

# Kuliah 2: Seksi, Teorema Bola Berbulu, dan Data Pengeleman {#br-bgk-2019-l02}

## Seksi {#br-bgk-2019-l02-s01}

### Definisi 2.1: seksi kontinu {#br-bgk-2019-l02-def-01}

Misalkan $X$ dan $Y$ ruang-ruang topologis, dan misalkan

$$
p:Y\longrightarrow X
$$

suatu pemetaan kontinu. Sebuah *seksi kontinu* dari $p$ adalah pemetaan
kontinu

$$
s:X\longrightarrow Y
$$

sedemikian sehingga

$$
p\circ s=\operatorname{Id}_X.
$$

Sebagai contoh, kita dapat memikirkan $Y$ sebagai sebuah bundel vektor di
atas $X$. Seksi hanya dapat ada jika $p$ surjektif, dan sifat ini selalu
dipenuhi oleh sebuah bundel vektor. Kadang-kadang sebuah seksi diidentifikasi
dengan citranya. Hal ini tidak menimbulkan masalah karena setiap seksi
injektif. *Seksi nol* mempunyai peran khusus: kepada setiap titik basis $P$,
ia memasangkan titik nol di dalam ruang vektor $V_P$. Untuk bundel tangen,
seksi mempunyai nama tersendiri.

### Definisi 2.2: medan vektor {#br-bgk-2019-l02-def-02}

Misalkan $M$ sebuah manifold terdiferensial. Sebuah pemetaan

$$
F:M\longrightarrow TM
$$

yang memenuhi

$$
F(P)\in T_PM
$$

untuk setiap titik $P\in M$ disebut *medan vektor* (tak bergantung waktu).

## Teorema bola berbulu {#br-bgk-2019-l02-s02}

> **Ilustrasi sumber - `Hairy_ball_one_pole.jpg`.** Sebuah medan vektor
> kontinu pada sfera dua harus mempunyai setidaknya satu titik nol.

![Bola berbulu dengan satu pusaran di kutub, sebagai ilustrasi bahwa medan vektor tangen kontinu pada bola harus mempunyai titik nol](authority/assets/bgk-hairy-ball-one-pole-500.jpg)

### Teorema 2.3: teorema bola berbulu {#br-bgk-2019-l02-thm-01}

Pada sfera dua, setiap medan vektor kontinu

$$
f:S^2\longrightarrow TS^2
$$

mempunyai setidaknya satu titik nol.

Khususnya, bundel tangen sfera dua tidak trivial. Teorema ini mempunyai
berbagai penafsiran. Misalnya, pada permukaan bumi selalu ada suatu titik
tanpa angin, jika arah angin horizontal sesaat dipandang sebagai medan
vektor kontinu. Demikian pula, semua duri landak tidak mungkin direbahkan
rata pada tubuh landak tanpa membentuk satu titik yang tegak.

### Catatan 2.4: penerapan pada Contoh 1.2 {#br-bgk-2019-l02-rem-01}

Teorema bola berbulu menjelaskan mengapa bundel vektor $L$ dari Contoh 1.2,
yang terletak di atas

$$
\mathbb R^3\setminus\{(0,0,0)\},
$$

tidak mempunyai trivialisasi kontinu. Pertama,

$$
S^2\subset\mathbb R^3\setminus\{(0,0,0)\},
$$

sehingga $L$ dapat dibatasi pada $S^2$. Jika $L$ sendiri trivial, maka
pembatasan ini juga trivial. Akan tetapi, pembatasan $L$ pada sfera satuan
adalah bundel tangen sfera satuan. Memang, syarat

$$
ru+sv+tw=0
$$

dapat dipahami sebagai relasi ortogonalitas, dan ruang tangen ekstrinsik di
titik posisi $(r,s,t)$ pada sfera ditentukan oleh relasi tersebut. Jika
bundel tangen itu trivial, akan ada dua medan vektor kontinu $u$ dan $v$
yang membentuk basis ruang tangen pada setiap titik sfera. Namun, teorema
bola berbulu menyatakan bahwa setiap medan vektor bahkan mempunyai titik
nol, sedangkan $0$ tidak dapat menjadi anggota suatu basis.

## Data pengeleman untuk ruang topologis {#br-bgk-2019-l02-s03}

Sebuah bundel vektor $V\to X$ “tersusun” dari bundel-bundel vektor trivial
$V|_{U_i}\to U_i$ untuk suatu penutup terbuka dari $X$. Cara potongan-potongan
itu disusun justru menentukan bundel vektornya, dan susunan tersebut dapat
dideskripsikan secara ringkas dengan data pengeleman. Untuk itu, pertama-tama
kita memerlukan data pengeleman bagi ruang topologis secara umum.

Pertanyaan dasarnya ialah: apa yang harus diketahui dari sebuah penutup
terbuka

$$
X=\bigcup_{i\in I}U_i
$$

agar ruang $X$ dapat direkonstruksi? Jawaban singkatnya ialah bahwa kita
harus mengetahui $U_i$, irisan dua-dua $U_i\cap U_j$ sebagai himpunan bagian
baik dari $U_i$ maupun dari $U_j$, cara kedua salinan itu diidentifikasi, dan
sebuah syarat kompatibilitas bagi identifikasi tersebut pada setiap tiga
himpunan.

> **Ilustrasi sumber - `Inclusion-exclusion.svg`.** Tiga himpunan yang saling
> beririsan menggambarkan perlunya syarat kompatibilitas pada irisan rangkap
> tiga.

![Diagram tiga himpunan berbentuk lingkaran yang saling beririsan, dengan setiap daerah irisan dibedakan oleh warna](authority/assets/bgk-inclusion-exclusion-500.png)

### Definisi 2.5: data pengeleman ruang topologis {#br-bgk-2019-l02-def-03}

Sebuah *data pengeleman* untuk ruang-ruang topologis terdiri atas:

1. sebuah keluarga ruang topologis $(U_i)_{i\in I}$;
2. untuk setiap pasangan $(i,j)$, sebuah himpunan terbuka

   $$
   U_{ij}\subseteq U_i,
   $$

   dengan $U_{ii}=U_i$;
3. untuk setiap pasangan $(i,j)$, sebuah homeomorfisme

   $$
   \varphi_{ji}:U_{ij}\longrightarrow U_{ji},
   $$

   dengan $\varphi_{ii}=\operatorname{Id}_{U_i}$;
4. untuk semua $i,j,k\in I$, *syarat kokikel*

   $$
   \varphi_{kj}\circ\varphi_{ji}=\varphi_{ki}
   $$

   dipenuhi sebagai pemetaan dari $U_{ik}\cap U_{ij}$ ke $U_k$.

### Lema 2.6: merekonstruksi ruang dari data pengeleman {#br-bgk-2019-l02-lem-01}

Misalkan diberikan data pengeleman $(U_i)_{i\in I}$ untuk ruang-ruang
topologis. Maka terdapat ruang topologis $X$ yang ditentukan secara unik,
penutup terbuka

$$
X=\bigcup_{i\in I}V_i,
$$

dan homeomorfisme

$$
\psi_i:U_i\longrightarrow V_i
$$

sedemikian sehingga

$$
\psi_i(U_{ij})=V_i\cap V_j
$$

dan

$$
\psi_i|_{U_{ij}}
=\psi_j|_{U_{ji}}\circ\varphi_{ji}.
$$

#### Bukti {#br-bgk-2019-l02-lem-01-proof}

Misalkan $Y$ gabungan lepas semua $U_i$. Pada $Y$, definisikan relasi
ekuivalensi $\sim$ dengan menyatakan bahwa $x_i\in U_i$ dan $x_j\in U_j$
ekuivalen apabila

$$
x_i\in U_{ij},\qquad x_j\in U_{ji},\qquad
\varphi_{ji}(x_i)=x_j.
$$

Sifat-sifat relasi ekuivalensi dijamin oleh syarat kokikel; lihat Soal 2.14.
Tetapkan

$$
X:=Y/{\sim}
$$

dan beri $X$ topologi hasil bagi. Komposisi

$$
U_i\longrightarrow Y\longrightarrow X
$$

adalah pemetaan $\psi_i$, dan $V_i$ adalah citra pemetaan tersebut. Dengan
demikian, $\psi_i:U_i\to V_i$ adalah homeomorfisme. Untuk $x\in U_i$,

$$
\psi_i(x)\in V_j
$$

jika dan hanya jika $x\in U_{ij}$, karena tepat dalam kasus ini $x$
diidentifikasi dengan $\varphi_{ji}(x)$. Karena itu,

$$
\psi_i(U_{ij})=V_i\cap V_j.
$$

> **Catatan edisi - arah indeks dalam bukti.** Dengan konvensi pada
> Definisi 2.5, $\varphi_{ji}:U_{ij}\to U_{ji}$. Pada kalimat sebelumnya,
> sumber mencetak $\varphi_{ij}(x)$ untuk $x\in U_{ij}$, meskipun pemetaan
> yang bertipe benar adalah $\varphi_{ji}(x)$. Edisi menampilkan indeks yang
> bertipe benar di badan bukti dan mempertahankan bentuk sumber dalam catatan
> ini.

Komutativitas diagram

$$
\begin{array}{ccc}
U_{ij}&\stackrel{\varphi_{ji}}{\longrightarrow}&U_{ji}\\
&\searrow\psi_i&\downarrow\psi_j\\
&&V_i\cap V_j
\end{array}
$$

mengikuti dengan cara yang sama. $\square$

### Lema 2.7: mengelem pemetaan kontinu {#br-bgk-2019-l02-lem-02}

Misalkan diberikan data pengeleman $(U_i)_{i\in I}$ untuk ruang-ruang
topologis. Misalkan $Z$ ruang topologis lain dan diberikan pemetaan-pemetaan
kontinu

$$
\theta_i:U_i\longrightarrow Z
$$

yang memenuhi

$$
\theta_i|_{U_{ij}}
=\bigl(\theta_j|_{U_{ji}}\bigr)\circ\varphi_{ji}.
$$

Maka terdapat tepat satu pemetaan kontinu

$$
\theta:X\longrightarrow Z
$$

sedemikian sehingga

$$
\theta|_{V_i}\circ\psi_i=\theta_i,
$$

dengan $X$ ruang topologis yang ditentukan oleh data pengeleman seperti pada
Lema 2.6, termasuk notasinya.

> **Catatan edisi - identitas komposisi tidak bertipe.** Sumber mencetak
> $(\psi_i)^{-1}\circ\theta|_{V_i}=\theta_i$, yang tidak dapat
> dikomposisikan: $\theta|_{V_i}$ bernilai di $Z$, sedangkan
> $(\psi_i)^{-1}$ berdomain $V_i$. Edisi menampilkan identitas bertipe benar
> $\theta|_{V_i}\circ\psi_i=\theta_i$ di badan lema dan mempertahankan
> bentuk sumber dalam catatan ini.

#### Bukti {#br-bgk-2019-l02-lem-02-proof}

Lihat Soal 2.18.

## Data pengeleman untuk bundel vektor {#br-bgk-2019-l02-s04}

### Definisi 2.8: data pengeleman bundel vektor real {#br-bgk-2019-l02-def-04}

Sebuah *data pengeleman* untuk bundel vektor real dengan rank $r$ di atas ruang
topologis $X$ terdiri atas:

1. sebuah penutup terbuka

   $$
   X=\bigcup_{i\in I}U_i;
   $$

2. sebuah keluarga bundel vektor real dengan rank $r$,

   $$
   (E_i\longrightarrow U_i)_{i\in I};
   $$

3. untuk setiap pasangan $(i,j)$, sebuah isomorfisme bundel vektor

   $$
   \varphi_{ji}:E_i|_{U_i\cap U_j}
   \longrightarrow E_j|_{U_i\cap U_j}
   $$

   di atas $U_i\cap U_j$;
4. untuk semua $i,j,k\in I$, syarat kokikel

   $$
   \varphi_{kj}\circ\varphi_{ji}=\varphi_{ki}
   $$

   dipenuhi sebagai pemetaan dari $E_i|_{U_i\cap U_j\cap U_k}$ ke
   $E_k|_{U_i\cap U_j\cap U_k}$.

### Catatan 2.9: deskripsi matriks {#br-bgk-2019-l02-rem-02}

Biasanya, bundel-bundel vektor pada butir (2) Definisi 2.8 adalah bundel
trivial di atas $U_i$, yaitu

$$
E_i=\mathbb R^r\times U_i.
$$

Isomorfisme pada butir (3) kemudian hanya berupa pemetaan linear bijektif

$$
\varphi_{ji}:\mathbb R^r\longrightarrow\mathbb R^r
$$

yang bergantung secara kontinu pada titik basis di $U_i\cap U_j$. Pemetaan
tersebut dapat dideskripsikan secara ringkas sebagai pemetaan kontinu

$$
\varphi_{ji}:U_i\cap U_j\longrightarrow
\operatorname{GL}_r(\mathbb R)
$$

ke grup linear umum. Jadi, kepada setiap titik basis dipasangkan secara
kontinu suatu matriks $r\times r$ yang invertibel; kontinuitas berarti bahwa
setiap entri matriks merupakan fungsi kontinu. Ini disebut *deskripsi
matriks* bundel tersebut. Syarat kokikel tetap berlaku.

### Lema 2.10: mengelem bundel vektor {#br-bgk-2019-l02-lem-03}

Misalkan diberikan data pengeleman $(E_i)_{i\in I}$ di atas ruang topologis

$$
X=\bigcup_{i\in I}U_i.
$$

Maka terdapat bundel vektor real $E\to X$ yang ditentukan secara unik dan
isomorfisme

$$
\psi_i:E_i\longrightarrow E|_{U_i}
$$

sedemikian sehingga

$$
\psi_i|_{E_i|_{U_i\cap U_j}}
=\psi_j|_{E_j|_{U_i\cap U_j}}\circ\varphi_{ji}.
$$

#### Bukti {#br-bgk-2019-l02-lem-03-proof}

Keberadaan ruang topologis $E$ dengan sifat-sifat tersebut diperoleh dari
Lema 2.6. Himpunan terbuka yang harus dilem ialah

$$
W_{ij}:=E_i|_{U_i\cap U_j},
$$

sedangkan keberadaan pemetaan kontinu ke $X$ diperoleh dari Lema 2.7. Pada
setiap serat $E_x$ terdapat struktur ruang vektor yang terdefinisi dengan
baik dan berasal dari $E_i$ untuk sebarang lingkungan terbuka
$x\in U_i$. Ketidakbergantungannya pada pilihan $i$ mengikuti fakta bahwa,
untuk $x\in U_i\cap U_j$, hipotesis memberikan isomorfisme bundel vektor

$$
\varphi_{ji}:E_i|_{U_i\cap U_j}
\longrightarrow E_j|_{U_i\cap U_j},
$$

yang menginduksi isomorfisme ruang vektor

$$
(E_i)_x\longrightarrow(E_j)_x.
$$

> **Catatan edisi - arah indeks pada isomorfisme serat.** Definisi 2.8
> menetapkan $\varphi_{ji}:E_i|_{U_i\cap U_j}\to
> E_j|_{U_i\cap U_j}$. Sumber mencetak $\varphi_{ij}$ pada kalimat bukti
> yang mengarah dari $E_i$ ke $E_j$. Edisi menampilkan $\varphi_{ji}$ yang
> konsisten dengan domain dan kodomain di badan bukti serta mempertahankan
> bentuk sumber dalam catatan ini.

$\square$

> **Ilustrasi sumber - `Fiddler_crab_mobius_strip.gif`.** Sebuah pita
> Möbius, yang muncul dengan membalik satu serat ketika dua trivialisasi
> lokal dilem.

![Animasi seekor kepiting berjalan satu putaran mengelilingi pita Möbius dan kembali dengan orientasi terbalik](authority/assets/bgk-fiddler-crab-mobius-strip-frame-001.png)

### Contoh 2.11: pita Möbius dari data pengeleman {#br-bgk-2019-l02-exa-01}

Pada sfera satu dimensi

$$
S^1=\left\{(x,y)\in\mathbb R^2\mid x^2+y^2=1\right\},
$$

perhatikan penutup terbuka

$$
S^1=U\cup V,
$$

dengan

$$
U=S^1\setminus\{(0,1)\},
\qquad
V=S^1\setminus\{(0,-1)\}.
$$

Kita akan mendeskripsikan data pengeleman bagi sebuah bundel vektor real
dengan rank $1$. Kedua himpunan terbuka itu homeomorfik dengan garis real.
Irisannya ialah

$$
\begin{aligned}
U\cap V
&=S^1\setminus\{(0,1),(0,-1)\}\\
&=\left\{(x,y)\in S^1\mid x\ne0\right\}.
\end{aligned}
$$

Himpunan ini tidak terhubung, melainkan homeomorfik dengan dua sinar terbuka
real yang saling lepas (atau, masing-masing, dengan garis real). Tetapkan

$$
L=U\times\mathbb R,
\qquad
M=V\times\mathbb R.
$$

Definisikan isomorfisme

$$
\varphi:L|_{U\cap V}\longrightarrow M|_{U\cap V}
$$

dengan

$$
\varphi(x,y,t):=
\begin{cases}
(x,y,t),&x>0,\\
(x,y,-t),&x<0.
\end{cases}
$$

Pemetaan $\varphi$ kontinu karena kedua rumus berlaku pada himpunan-himpunan
terbuka yang saling lepas. Pada satu belahan, serat dipetakan secara identik;
pada belahan lain, serat dibalik. Dalam pengertian Catatan 2.9, deskripsi
matriks kontinu (dan konstan pada setiap komponen)

$$
\psi(x,y):=
\begin{cases}
(1),&x>0,\\
(-1),&x<0
\end{cases}
$$

berlaku pada $U\cap V$. Karena hanya ada dua himpunan terbuka, syarat kokikel
terpenuhi secara otomatis. Menurut Lema 2.10, data pengeleman ini menentukan
sebuah bundel vektor real dengan rank $1$ pada sfera. Bundel itu disebut *pita
Möbius*.

### Contoh 2.12: realisasi aljabar pita Möbius {#br-bgk-2019-l02-exa-02}

Kita berikan realisasi aljabar langsung dari pita Möbius di $\mathbb R^4$.
Perhatikan

$$
Y:=\left\{(x,y,z,w)\in\mathbb R^4\mathrel{\Big|}
x^2+y^2=1,\ (1-y)z=xw,\ xz=(1+y)w\right\}
$$

beserta proyeksi alaminya ke sfera satu dimensi

$$
S^1=\left\{(x,y)\in\mathbb R^2\mid x^2+y^2=1\right\}=U\cup V,
$$

dengan

$$
U=S^1\setminus\{(0,1)\},
\qquad
V=S^1\setminus\{(0,-1)\}.
$$

Kita klaim bahwa $Y$ adalah bundel vektor dengan rank $1$ yang isomorfik dengan
pita Möbius. Pada $U$, berlaku $y\ne1$, sehingga persamaan kedua dapat
diselesaikan terhadap $z$:

$$
z=\frac{x}{1-y}w.
$$

Persamaan ketiga kemudian dipenuhi secara otomatis karena

$$
xz=\frac{x}{1-y}xw
=\frac{x^2}{1-y}w
=\frac{1-y^2}{1-y}w
=(1+y)w.
$$

Dengan cara yang sama, pada $V$ berlaku

$$
w=\frac{x}{1+y}z,
$$

dan persamaan yang lain dipenuhi secara otomatis. Jadi, di atas $U$ dan $V$,
$Y$ merupakan bundel vektor trivial dengan rank $1$, masing-masing dengan
variabel serat $w$ dan $z$. Pemetaan transisinya pada $U\cap V$ diberikan
oleh

$$
\frac{x}{1-y}=\frac{1+y}{x},
$$

sehingga satu deskripsi matriks bundel ini ialah

$$
\left(\frac{x}{1-y}\right).
$$

Berbeda dari matriks konstan pada Contoh 2.11, matriks ini bergantung secara
eksplisit pada $(x,y)\in U\cap V$. Meskipun demikian, kedua bundel itu saling
isomorfik. Dengan menggunakan Soal 2.21, ambil fungsi-fungsi kontinu taknol
$\sqrt{1-y}$ pada $U$ dan $\sqrt{1+y}$ pada $V$. Kita memperoleh

> **Catatan edisi - variabel tak terdefinisi pada sumber.** Sumber mencetak
> $\sqrt{1-t}$ pada $U$ dan $\sqrt{1+t}$ pada $V$, tetapi tidak ada variabel
> $t$ dalam contoh ini. Perhitungan yang langsung menyusul memakai $y$ dan
> menetapkan kandidat koreksinya secara unik sebagai $\sqrt{1-y}$ dan
> $\sqrt{1+y}$. Edisi menampilkan bentuk bertipe benar itu di badan teks dan
> mengungkapkan normalisasi tersebut di sini.

$$
\begin{aligned}
\frac{1}{\sqrt{1+y}}\cdot
\frac{x}{1-y}\cdot\sqrt{1-y}
&=\frac{1}{\sqrt{1+y}}\cdot\frac{x}{\sqrt{1-y}}\\
&=\frac{x}{\sqrt{1-y^2}}\\
&=\frac{x}{\sqrt{x^2}}\\
&=\frac{x}{|x|}\\
&=\pm1,
\end{aligned}
$$

bergantung pada tanda $x$. Karena itu, kedua bundel tersebut isomorfik.
