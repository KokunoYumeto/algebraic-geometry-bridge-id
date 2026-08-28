---
title: "Kuliah 29 - Proyeksi dan Kurva Proyektif Terparametrisasi"
stable_id: br-ak-2012-l29
language: id-ID
source_author: "Holger Brenner"
frozen_revision_contributor: "Bocardodarapti"
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 29"
upstream_pageid: 51996
upstream_revid: 1069408
upstream_timestamp: "2026-02-05T19:18:37Z"
upstream_mediawiki_sha1: 6f0742211aeb307841634425937aad9037da51be
source_url: "https://de.wikiversity.org/w/index.php?oldid=1069408"
authority_manifest: authority/wikiversity/unit-29/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: ec3b34ad387ae827ecaa365c4def3b0550f74b629d0db3873a7cc28dc0831bc5
lecture_xml: authority/wikiversity/unit-29/lecture-29.xml
lecture_xml_sha256: e5055632a6aa8119540cb5acccc0ba86a82b6d2bc88192b9ddd5a77aaea31d70
lecture_expanded_tex: authority/wikiversity/unit-29/lecture-29-expanded.tex
lecture_expanded_tex_sha256: 7c06a1dbb12904bd5f89427955ef8bdae5781e402522cd70f09a0c6e1ef1e784
license: "Current semantic course text and this translation: CC BY-SA 4.0. Unit 29 reader media retain their component-specific public-domain status as recorded in authority/RIGHTS-unit-29.csv. No blanket relicensing claim is made."
source_component_license_route: "Semantic-site rights notice: CC BY-SA 4.0; media component rights remain item-specific; official-PDF notices remain component-specific; no blanket relicensing claim."
license_evidence: "authority/UNIT_29_AUTHORITY_FREEZE.md; authority/RIGHTS-unit-29.csv; authority/ASSET_CLOSURE-unit-29.json"
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_semantic_entities: 8
source_corrections: 4
correction_ids: "AGC-CORR-0126; AGC-CORR-0127; AGC-CORR-0128; AGC-CORR-0129"
reader_media_positions: 0
---

# Kuliah 29: Proyeksi dan Kurva Proyektif Terparametrisasi {#br-ak-2012-l29}

## Proyeksi dari sebuah titik {#br-ak-2012-l29-s01}

<!-- upstream_entity: Projektiver Raum/Projektion weg von einem Punkt/Definition -->

### Definisi 29.1: proyeksi dari sebuah titik {#br-ak-2012-l29-def-01}

Pemetaan

$$
\begin{aligned}
\mathbb P_K^n\setminus\{(1,0,\ldots,0)\}
&\longrightarrow \mathbb P_K^{n-1},\\
(x_0,x_1,\ldots,x_n)&\longmapsto(x_1,\ldots,x_n)
\end{aligned}
$$

disebut *proyeksi dari titik* $(1,0,\ldots,0)$.

Pemetaan ini merupakan morfisme yang terdefinisi dengan baik di luar
*pusat* proyeksi $(1,0,\ldots,0)$. Setiap titik lain dipetakan ke titik di
$\mathbb P_K^{n-1}$ yang bersesuaian dengan garis melalui titik itu dan
pusat proyeksi. Karena itu, pemetaan tersebut surjektif dan setiap serat
merupakan sebuah garis proyektif tanpa titik pusat, jadi sebuah garis afin.
Dengan kata lain, terdapat apa yang disebut *bundel garis* di atas
$\mathbb P_K^{n-1}$.

Pemetaan ini adalah perluasan pemetaan kerucut

$$
\mathbb A_K^n\setminus\{0\}\longrightarrow\mathbb P_K^{n-1}
$$

ke ruang proyektif tertusuk. Pemetaan yang bersesuaian dapat didefinisikan
untuk sembarang titik pusat; lihat Soal 29.7.

## Pemetaan ke $\mathbb P_K^1$ {#br-ak-2012-l29-s02}

Teorema berikut memberikan versi baru normalisasi Noether.

<!-- upstream_entity: Ebene projektive Kurve/Abbildung nach P^1 über Projektion von einem Punkt/Fakt -->

### Teorema 29.2: proyeksi kurva bidang ke $\mathbb P_K^1$ {#br-ak-2012-l29-thm-01}

Misalkan $K$ lapangan tertutup secara aljabar dan

$$
C\subseteq\mathbb P_K^2
$$

suatu kurva bidang proyektif berderajat $d$. Maka terdapat morfisme
surjektif

$$
C\longrightarrow\mathbb P_K^1
$$

sedemikian sehingga setiap serat terdiri atas paling banyak $d$ titik.

#### Bukti {#br-ak-2012-l29-thm-01-proof}

Pilih sebuah titik

$$
P\in\mathbb P_K^2
$$

yang tidak terletak pada kurva. Titik seperti itu ada karena, khususnya,
lapangan $K$ tak berhingga. Perhatikan proyeksi dari $P$; pembatasannya
menginduksi morfisme

$$
C\hookrightarrow\mathbb P_K^2\setminus\{P\}
\longrightarrow\mathbb P_K^1.
$$

Serat morfisme ini di atas suatu titik

$$
Q\in\mathbb P_K^1,
$$

yang merepresentasikan suatu arah di $P\in\mathbb P_K^2$, terdiri tepat atas
titik-titik kurva yang terletak pada garis yang ditentukan oleh $Q$,

$$
G=V_+(aX+bY+cZ)\cong\mathbb P_K^1\subseteq\mathbb P_K^2.
$$

Karena itu, serat di atas $Q$ dapat dideskripsikan pada $G$ dengan
mengeliminasi satu variabel dari persamaan kurva

$$
C=V_+(F)
$$

menggunakan persamaan garis tersebut. Hasilnya adalah polinom homogen tak
nol $\overline F$ dalam dua variabel dan berderajat $d$; polinom itu tidak
mungkin nol, sebab jika demikian maka $P$ akan menjadi titik kurva. Karena
kita bekerja di atas lapangan tertutup secara aljabar, polinom
$\overline F$ mempunyai sedikitnya satu dan paling banyak $d$ titik nol,
dan semuanya berbeda dari $P$. Hal ini membuktikan surjektivitas serta
batas banyaknya titik dalam setiap serat. $\square$

<!-- upstream_entity: Glatte projektive Kurven/Rationale Funktion als Morphismus nach P^1/Fakt -->

### Teorema 29.3: fungsi rasional sebagai morfisme ke $\mathbb P_K^1$ {#br-ak-2012-l29-thm-02}

Misalkan $K$ suatu lapangan dan

$$
C\subseteq\mathbb P_K^2
$$

suatu kurva bidang proyektif yang mulus dan tak tereduksi. Misalkan

$$
D=C\cap D_+(Z)\cong K\!-\!\operatorname{Spek}(R)
$$

suatu bagian afin kurva tersebut, dan misalkan

$$
q=\frac gh\in Q(R)
$$

suatu fungsi rasional, dengan $g,h\in R$ dan $h\ne0$. Maka terdapat tepat
satu morfisme

$$
\varphi:C\longrightarrow\mathbb P_K^1
$$

sedemikian sehingga diagram

$$
\begin{matrix}
D(h)&\stackrel{g/h}{\longrightarrow}&\mathbb A_K^1\cong D_+(s)\\
\downarrow&&\downarrow\\
C&\stackrel{\varphi}{\longrightarrow}&\mathbb P_K^1
\end{matrix}
$$

komutatif.

#### Bukti {#br-ak-2012-l29-thm-02-proof}

Pertama-tama kita mendefinisikan pada $D$ suatu perluasan

$$
\varphi:D\longrightarrow\mathbb P_K^1
$$

dari fungsi rasional $g/h$. Untuk itu, ambil sebuah titik $P\in D$ pada
kurva. Jika $P\in D(h)$, tidak ada yang perlu dilakukan. Jadi, misalkan
$h(P)=0$.

Karena kurva mulus, berdasarkan Teorema 23.6 gelanggang lokal $B$ kurva di
titik $P$ merupakan gelanggang valuasi diskret. Oleh sebab itu, pada titik
tersebut hasil bagi $g/h$ dapat ditulis sebagai

$$
\frac gh=u\pi^n,
$$

dengan $u\in B^\times$, $n\in\mathbb Z$, dan $\pi$ suatu uniformisator
(pembangkit ideal maksimal). Terdapat lingkungan terbuka

$$
P\in D(\psi)\subseteq D
$$

sedemikian sehingga $\pi$ dan $u$ terdefinisi pada $D(\psi)$ dan $u$ adalah
unit di sana. Jika $n\geq0$, maka

$$
\frac gh\in R_\psi,
$$

sehingga titik ketakterdefinisi itu bahkan dapat disingkirkan untuk pemetaan
ke $\mathbb A_K^1$. Jika $n\leq0$, hasil bagi terbalik

$$
\frac hg=u^{-1}\pi^{-n}
$$

terdefinisi pada $D(\psi)$ sebagai pemetaan ke $\mathbb A_K^1$. Melalui
"pembenaman dengan koordinat tertukar"

$$
\mathbb A_K^1\cong D_+(t)\hookrightarrow\mathbb P_K^1,
$$

kita memperoleh pemetaan ke $\mathbb P_K^1$.

Kita harus menunjukkan bahwa kedua morfisme ke garis proyektif ini berimpit
di tempat keduanya terdefinisi. Tempat itu terdiri atas titik-titik $P$ tempat
$g/h$ tidak bernilai nol dan tidak mempunyai kutub. Kompatibilitas
mengikuti dari kenyataan bahwa pada suatu lingkungan terbuka

$$
P\in U
$$

terdapat pemetaan

$$
\frac gh:U\longrightarrow
(\mathbb A_K^1)^\times=\mathbb A_K^1\setminus\{0\},
$$

dan diagram

$$
\begin{matrix}
(\mathbb A_K^1)^\times&\stackrel{i^{-1}}{\longrightarrow}&
\mathbb A_K^1\cong D_+(t)\\
\downarrow&&\downarrow\\
\mathbb A_K^1\cong D_+(s)&\longrightarrow&\mathbb P_K^1
\end{matrix}
$$

komutatif. Dengan demikian diperoleh morfisme yang terdefinisi dengan baik
pada bagian afin $D$.

> **Koreksi sumber AGC-CORR-0127 - objek yang memiliki nol dan kutub.**
> Sumber menyebut $\varphi$ pada kalimat ini, padahal nol dan kutub adalah
> sifat fungsi rasional $g/h$. Edisi menampilkan objek yang benar tanpa
> mengubah syarat tumpang-tindih atau diagram penempelannya.

Untuk sembarang titik pada kurva proyektif $C$ dan suatu lingkungan afin

$$
P\in D'\subseteq C,
$$

kita berada dalam situasi yang sama, karena

$$
D_+(h)\cap D'\ne\varnothing,
$$

sehingga fungsi rasional itu terdefinisi pada suatu himpunan terbuka tak
kosong, meskipun mungkin dengan pembilang dan penyebut yang berbeda. Dengan
demikian argumen sebelumnya dapat diterapkan dengan cara yang sama.

Ketunggalan mengikuti karena pada setiap himpunan terbuka afin

$$
P\in U
$$

irisan $U\cap D_+(h)$ tidak kosong. Suatu morfisme dari varietas integral ke
garis afin $\mathbb A_K^1$ ditentukan secara tunggal oleh fungsi rasionalnya.
$\square$

<!-- upstream_entity: Projektive Gerade/Rationale Funktion/z nach 1/z/Beispiel -->

### Contoh 29.4: inversi pada garis proyektif {#br-ak-2012-l29-ex-01}

Pemetaan inversi

$$
\begin{aligned}
\mathbb A_K^1\supset D(z)&\longrightarrow\mathbb A_K^1,\\
z&\longmapsto z^{-1}
\end{aligned}
$$

dapat diperluas menjadi morfisme bijektif

$$
\begin{aligned}
\mathbb P_K^1&\longrightarrow\mathbb P_K^1,\\
(x,y)&\longmapsto(y,x).
\end{aligned}
$$

Hal ini langsung mengikuti dari Teorema 29.3. Setiap titik $z\ne0$ dipetakan
ke $1/z$, sedangkan titik nol dipetakan ke titik di tak hingga $\infty$.

## Kurva bidang proyektif terparametrisasi {#br-ak-2012-l29-s03}

Misalkan diberikan kurva dengan parametrisasi rasional

$$
s\longmapsto
\left(\frac{\varphi_1(s)}{\psi(s)},
      \frac{\varphi_2(s)}{\psi(s)}\right).
$$

Dalam Teorema 6.11 kita telah melihat bahwa citranya memenuhi suatu persamaan
aljabar. Dalam bukti teorema tersebut kita sudah memakai parametrisasi yang
dihomogenkan; sekarang parametrisasi itu muncul kembali sebagai perluasan
proyektif.

<!-- upstream_entity: Rationale Kurvenparametrisierung/Fortsetzung auf projektive Gerade/Fakt -->

### Teorema 29.5: perluasan proyektif parametrisasi rasional {#br-ak-2012-l29-thm-03}

Misalkan

$$
\begin{aligned}
\mathbb A_K^1\supseteq D(\psi)&\longrightarrow\mathbb A_K^2,\\
s&\longmapsto
\left(\frac{\varphi_1(s)}{\psi(s)},
      \frac{\varphi_2(s)}{\psi(s)}\right)
\end{aligned}
$$

suatu parametrisasi rasional dalam bentuk tereduksi; yakni
$\varphi_1,\varphi_2,\psi$ tidak mempunyai pembagi bersama. Misalkan $d$
adalah derajat maksimum polinom-polinom yang terlibat dan

$$
\widehat{\varphi_1},\quad\widehat{\varphi_2},\quad\widehat\psi
$$

adalah homogenisasi polinom-polinom itu terhadap variabel baru $t$.
Masing-masing $H_1,H_2,H_3$ diperoleh dari ketiga homogenisasi dengan
mengalikannya dengan pangkat $t$ yang sesuai, sehingga ketiganya berderajat
$d$.

Maka $H_1,H_2,H_3$ mendefinisikan morfisme

$$
\begin{aligned}
H:\mathbb P_K^1&\longrightarrow\mathbb P_K^2,\\
(s,t)&\longmapsto\bigl(H_1(s,t),H_2(s,t),H_3(s,t)\bigr),
\end{aligned}
$$

sedemikian sehingga diagram

$$
\begin{matrix}
\mathbb A_K^1\supseteq D(\psi)&\longrightarrow&
\mathbb A_K^2\cong D_+(Z)\\
\downarrow&&\downarrow\\
\mathbb P_K^1&\stackrel{H}{\longrightarrow}&\mathbb P_K^2
\end{matrix}
$$

komutatif. Selain itu, citra $H$ terletak pada penutupan proyektif dari kurva
citra afin.

#### Bukti {#br-ak-2012-l29-thm-03-proof}

Menurut Soal 29.6, pemetaan $H$ terdefinisi dengan baik pada seluruh
$\mathbb P_K^1$, sebab $\varphi_1,\varphi_2,\psi$ tidak mempunyai pembagi
bersama. Untuk membuktikan komutativitas, cukup diperhatikan bahwa suatu

$$
s\in D(\psi)\subseteq\mathbb A_K^1
$$

di satu sisi dipetakan melalui $(s,1)$ ke

$$
\bigl(H_1(s,1),H_2(s,1),H_3(s,1)\bigr)
=\bigl(\varphi_1(s),\varphi_2(s),\psi(s)\bigr),
$$

sedangkan di sisi lain dipetakan ke

$$
\left(\frac{\varphi_1(s)}{\psi(s)},
      \frac{\varphi_2(s)}{\psi(s)},1\right)
=\bigl(\varphi_1(s),\varphi_2(s),\psi(s)\bigr)
$$

sebagai titik proyektif.

Untuk pernyataan tambahan, misalkan $C$ penutupan afin dari citra dan

$$
\overline C\subseteq\mathbb P_K^2
$$

penutupan proyektifnya. Perhatikan komplemen terbuka

$$
U=\mathbb P_K^2\setminus\overline C.
$$

Karena pemetaan tersebut kontinu, prapeta $H^{-1}(U)$ terbuka di
$\mathbb P_K^1$, dan hanya dapat memuat titik-titik dari
$\mathbb P_K^1\setminus D(\psi)$. Namun, suatu himpunan bagian berhingga yang
terbuka di garis proyektif harus kosong. $\square$

<!-- upstream_entity: Ebene projektive Kurve/Graph eines Polynoms in einer Variable/Singularität im Unendlichen/Fakt -->

### Teorema 29.6: penutupan proyektif grafik sebuah polinom {#br-ak-2012-l29-thm-04}

Misalkan $K$ lapangan tertutup secara aljabar dan

$$
F\in K[X]
$$

suatu polinom dalam satu variabel dan berderajat $d\geq1$. Penutupan
proyektif $C$ dari grafik

$$
V(Y-F(X))
$$

dideskripsikan oleh

$$
V_+\bigl(YZ^{d-1}-\widehat F(X,Z)\bigr),
$$

dengan $\widehat F(X,Z)$ homogenisasi $F$. Jika $d=1$ dan $F=aX+b$, maka
$C$ mempunyai satu titik tambahan, yaitu titik mulus $(1,a,0)$. Jika
$d\geq2$, titik tambahannya adalah $(0,1,0)$, yang singular bila $d\geq3$.
Untuk $d\geq2$, titik di tak hingga tersebut mempunyai multiplisitas $d-1$.

> **Koreksi sumber AGC-CORR-0128 - operator lokus nol proyektif.**
> Sumber mencetak $V$ untuk persamaan homogen di $\mathbb P_K^2$. Edisi
> memakai $V_+$, sesuai ruang ambien proyektif dan notasi bukti berikutnya.

#### Bukti {#br-ak-2012-l29-thm-04-proof}

Persamaan penutupan proyektif langsung mengikuti dari Korolari 28.10. Untuk
menentukan irisan $C$ dengan garis proyektif $V_+(Z)$ di tak hingga, tetapkan
$Z=0$ dalam persamaan.

Jika $d=1$, persamaan kurva adalah persamaan garis

$$
V_+(Y-aX-bZ),
$$

dan irisannya dengan $V_+(Z)$ menentukan satu-satunya titik $(1,a,0)$. Jika
$d\geq2$, persamaan kurvanya adalah

$$
V_+\bigl(
YZ^{d-1}-s_dX^d-s_{d-1}X^{d-1}Z-\cdots-s_0Z^d
\bigr),
$$

dengan $s_d\ne0$. Setelah menetapkan $Z=0$, yang tersisa adalah

$$
V_+(-s_dX^d),
$$

sehingga $X=0$. Ini memberikan satu-satunya titik di tak hingga $(0,1,0)$.

Untuk menghitung multiplisitas, perhatikan persamaan afin kurva pada
$D_+(Y)$. Dengan menetapkan $Y=1$, diperoleh persamaan afin

$$
V\bigl(
Z^{d-1}-s_dX^d-s_{d-1}X^{d-1}Z-\cdots-s_0Z^d
\bigr),
$$

dan dalam koordinat ini titik $(0,1,0)$ menjadi titik asal. Karena itu,
multiplisitasnya adalah $d-1$, dengan satu-satunya garis singgung diberikan
oleh $Z=0$. Jika $d\geq3$, multiplisitasnya sedikitnya $2$, sehingga titik
tersebut singular. $\square$

> **Koreksi sumber AGC-U29-SRC-001 / AGC-CORR-0126 - simbol bebas pada batas singularitas.**
> Pada kalimat terakhir bukti, sumber mencetak $g\geq3$, padahal tidak ada
> besaran $g$ yang didefinisikan dalam teorema ini. Derajat yang didefinisikan
> dan dipakai di seluruh perhitungan adalah $d$; edisi karena itu menampilkan
> batas yang dimaksud sebagai $d\geq3$ dan mempertahankan alasan
> multiplisitas $d-1\geq2$ secara eksplisit.

Teorema ini dapat dipahami sebagai berikut. Jika $d\geq2$, sumbu-$y$ -- yang
direpresentasikan oleh titik $(0,1,0)$ -- termasuk pada grafik secara
"asimtotik", dan sekaligus merupakan satu-satunya asimtot grafik. Garis di
tak hingga $V_+(Z)$ adalah satu-satunya garis singgung di titik tersebut.

Normalisasi $C$ adalah $\mathbb P_K^1$. Berdasarkan Teorema 29.5 yang
diterapkan pada parametrisasi afin grafik

$$
\begin{aligned}
\mathbb A_K^1&\longrightarrow
\mathbb A_K^1\times\mathbb A_K^1
=\mathbb A_K^2\cong D_+(Z)\subset\mathbb P_K^2,\\
x&\longmapsto(x,F(x))=(x,F(x),1),
\end{aligned}
$$

pemetaan normalisasinya diberikan oleh

$$
\begin{aligned}
\mathbb P_K^1&\longrightarrow C\subset\mathbb P_K^2,\\
(x,t)&\longmapsto\bigl(xt^{d-1},\widehat F(x,t),t^d\bigr).
\end{aligned}
$$

Titik di tak hingga $(1,0)$ dipetakan ke

$$
(0,s_d,0)=(0,1,0).
$$

<!-- upstream_entity: Ebene projektive Kurve/Graph einer rationalen Funktion in einer Variable/Singularität im Unendlichen/Fakt -->

### Teorema 29.7: penutupan proyektif grafik sebuah fungsi rasional {#br-ak-2012-l29-thm-05}

Misalkan $K$ lapangan tertutup secara aljabar, dan misalkan

$$
G,H\in K[X]
$$

polinom-polinom dalam satu variabel, masing-masing berderajat $d,e\geq1$,
tanpa akar bersama. Misalkan $H\ne0$ dan

$$
F(X)=\frac{G(X)}{H(X)}
$$

fungsi rasional yang bersesuaian. Misalkan $\widehat G(X,Z)$ dan
$\widehat H(X,Z)$ adalah homogenisasi masing-masing polinom. Jika $d>e$,
penutupan proyektif $C$ dari grafik $F(X)$ dideskripsikan oleh

$$
V_+\bigl(\widehat H(X,Z)YZ^{d-e-1}-\widehat G(X,Z)\bigr),
$$

sedangkan jika $d\leq e$, penutupan tersebut dideskripsikan oleh

$$
V_+\bigl(\widehat H(X,Z)Y-\widehat G(X,Z)Z^{e-d+1}\bigr).
$$

#### Bukti {#br-ak-2012-l29-thm-05-proof}

Deskripsi afin kurva adalah

$$
V(YH-G).
$$

Menurut Korolari 28.10, penutupan proyektif dideskripsikan oleh homogenisasi
$YH-G$. Untuk homogenisasi ini, yang menentukan adalah derajat maksimum di
antara suku $YH$ dan $G$; suku dengan derajat lebih kecil harus "dilengkapi"
dengan pangkat $Z$ yang sesuai. Hal ini menghasilkan kedua persamaan di atas.
$\square$

## Kurva proyektif monomial {#br-ak-2012-l29-s04}

Untuk kurva bidang monomial

$$
s\longmapsto(s^e,s^d)=(x,y)
$$

dengan eksponen saling prima $e>d$, berdasarkan Teorema 29.5 terdapat kurva
proyektif monomial

$$
(s,t)\longmapsto(s^e,s^dt^{e-d},t^e).
$$

Pada himpunan terbuka $D_+(t)$, pemetaan ini adalah pemetaan awal,
sedangkan pada $D_+(s)$ pemetaan tersebut menjadi pemetaan afin

$$
t\longmapsto(t^{e-d},t^e).
$$

<!-- upstream_entity: Ebene projektive monomiale Kurve/Singularität/Gesamtmultiplizität/Fakt -->

### Teorema 29.8: singularitas kurva proyektif monomial {#br-ak-2012-l29-thm-06}

Misalkan $e>d$ saling prima. Untuk kurva bidang proyektif monomial
berderajat $e$

$$
C:\quad(s,t)\longmapsto\bigl(s^e,s^dt^{e-d},t^e\bigr),
$$

berlaku pernyataan-pernyataan berikut.

1. Kurva dideskripsikan oleh persamaan homogen berderajat $e$

   $$
   Y^e=X^dZ^{e-d}.
   $$

2. Kurva mulus pada semua titik selain $(0,0,1)$ dan $(1,0,0)$.

3. Kurva mempunyai multiplisitas $d$ di titik $(0,0,1)$ dan
   multiplisitas $e-d$ di titik $(1,0,0)$.

4. Jika $e\geq3$, kurva tidak mulus.

#### Bukti {#br-ak-2012-l29-thm-06-proof}

1. Persamaan afinnya adalah $X^d-Y^e$. Menurut Korolari 28.10, penutupan
   proyektif dideskripsikan oleh homogenisasinya, yaitu

   $$
   V_+\bigl(X^dZ^{e-d}-Y^e\bigr).
   $$

   > **Koreksi sumber AGC-CORR-0129 - operator lokus nol proyektif.**
   > Sumber mencetak $V$ untuk homogenisasi yang mendefinisikan penutupan di
   > $\mathbb P_K^2$; edisi memakai $V_+$. Lokus-lokus afin di bawah tetap
   > memakai $V$.

2. Pada kurva afin

   $$
   V(X^d-Y^e)\subseteq\mathbb A_K^2\subseteq\mathbb P_K^2,
   $$

   menurut Teorema 20.12 hanya titik asal -- yang bersesuaian dengan titik
   proyektif $(0,0,1)$ -- yang mungkin tidak mulus. Titik-titik kurva di luar
   $D_+(Z)$ diperoleh dengan menetapkan $Z=0$ dalam persamaan. Hal ini
   memaksa $Y=0$, sehingga hanya tersisa titik $(1,0,0)$.

3. Multiplisitas pada suatu titik merupakan sifat lokal. Titik $(0,0,1)$
   bersesuaian dengan titik asal pada kurva monomial afin

   $$
   V(X^d-Y^e),
   $$

   yang menurut Korolari 23.8 mempunyai multiplisitas sebesar eksponen yang
   lebih kecil, yaitu $d$. Titik $(1,0,0)$ terletak pada $D_+(X)$, dan di
   sana persamaan afinnya adalah

   $$
   V(Y^e-Z^{e-d}).
   $$

   Multiplisitasnya kembali merupakan eksponen yang lebih kecil, yaitu
   $e-d$.

4. Pernyataan ini mengikuti dari butir 3. $\square$
