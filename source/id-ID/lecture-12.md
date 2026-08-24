---
title: "Kuliah 12 - Spektrum-K dan Funktorialitasnya"
stable_id: br-ak-2025-2026-l12
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 12"
upstream_pageid: 165901
upstream_revid: 1112280
upstream_timestamp: "2026-08-21T08:02:32Z"
upstream_mediawiki_sha1: 7273d05cc557ce9421f7cc42b6f70b8b28ba57e2
source_url: "https://de.wikiversity.org/w/index.php?oldid=1112280"
authority_manifest: authority/wikiversity/unit-12/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 181ce377bd68639b12511a9b1402ca03fd76c6107325195d3aa51a81b7286559
lecture_xml_sha256: 5c7011a57a38a83222a6f5ea0001d00a5a811000510bea8ebcf00754457ec81d
lecture_expanded_tex_sha256: 1cbd13d735c9eade611094b6ab0eb7b3d1678abe589bb9b1e8b5a7d25d218b07
license: "CC BY-SA 4.0 for translated course text; media retain component rights in authority/RIGHTS-unit-12.csv"
translation_status: complete
---

# Kuliah 12: Spektrum-$K$ dan Funktorialitasnya {#br-ak-2025-2026-l12}

> “Terlahir untuk melihat, ditugaskan untuk memandang.”
>
> — Johann Wolfgang von Goethe

## Spektrum-$K$ {#br-ak-2025-2026-l12-s01}

![Potret hitam-putih Alexander Grothendieck yang sedang duduk](authority/assets/Alexander_Grothendieck.jpg)

*Alexander Grothendieck (1928–2014); foto: Konrad Jacobs, Oberwolfach Photo
Collection/MFO; [CC BY-SA 2.0 de](https://creativecommons.org/licenses/by-sa/2.0/de/deed.en).*

Bagaimana himpunan aljabar afin dan gelanggang koordinatnya saling
berhubungan? Jawaban yang bermakna hanya dapat diharapkan untuk lapangan dasar
yang tak hingga, karena dalam kasus berhingga jumlah titiknya terlalu sedikit.
Teori yang memuaskan bahkan mengharuskan kita membatasi diri pada lapangan yang
tertutup secara aljabar, atau—dan inilah sudut pandang teori skema yang
dikembangkan Alexander Grothendieck—tidak hanya meninjau titik-$K$, tetapi juga
memasukkan ideal maksimal dan ideal prima sebagai titik.

Pertanyaan penting pertama ialah sebagai berikut. Suatu aljabar-$K$ $R$ bertipe
hingga mempunyai beberapa representasi, yang pada umumnya berkedudukan sama,
sebagai gelanggang faktor dari suatu aljabar polinomial; misalnya,

$$
K[X_1,\ldots,X_n]/\mathfrak a
\cong R
\cong K[X_1,\ldots,X_m]/\mathfrak b.
$$

Kedua representasi ini menghasilkan lokus nol

$$
V(\mathfrak a)\subseteq\mathbb A_K^n
\qquad\text{dan}\qquad
V(\mathfrak b)\subseteq\mathbb A_K^m.
$$

Bagaimana kedua lokus nol tersebut saling berhubungan?

<!-- upstream_entity: Affin-algebraische Mengen/Isomorphe Algebren und Nullstellengebilde/Polynomring in einer Variablen als Gerade, eingebettete Gerade und Graph/Beispiel -->

### Contoh: tiga representasi garis afin {#br-ak-2025-2026-l12-exm-01}

Tinjau gelanggang polinomial satu variabel

$$
R=K[T].
$$

Objek yang pertama-tama bersesuaian dengannya ialah garis afin
$\mathbb A_K^1$. Akan tetapi, $R$ juga dapat diperoleh dengan berbagai cara
sebagai gelanggang faktor dari aljabar polinomial dalam lebih dari satu
variabel. Misalkan, sebagai contoh,

$$
a\in K,\qquad a\ne0,
$$

dan tinjau gelanggang faktor $K[X,Y]/(aY+bX)$. Gelanggang ini, sebagai
aljabar-$K$, isomorfik dengan $R$, seperti ditunjukkan oleh pemetaan

$$
\begin{aligned}
K[X,Y]/(aY+bX)&\longrightarrow K[T],\\
X&\longmapsto T,\\
Y&\longmapsto-\frac baT.
\end{aligned}
$$

Lokus nol yang bersesuaian,

$$
V(aY+bX)\subset\mathbb A_K^2,
$$

hanyalah garis di bidang afin yang dideskripsikan oleh persamaan

$$
Y=-\frac baX.
$$

Cara lain untuk merepresentasikan gelanggang polinomial satu variabel sebagai
gelanggang faktor ialah

$$
K[X,Y]/(Y-P(X)),
$$

dengan $P(X)$ suatu polinom sembarang dalam satu variabel $X$. Homomorfisme
gelanggang

$$
\begin{aligned}
K[X,Y]/(Y-P(X))&\longrightarrow K[T],\\
X&\longmapsto T,\\
Y&\longmapsto P(T)
\end{aligned}
$$

kembali menunjukkan adanya isomorfisme dengan gelanggang polinomial satu
variabel. Lokus nol yang bersesuaian hanyalah grafik polinom $P(X)$.

![Garis horizontal hitam](authority/assets/Lineline.jpg)

*Garis horizontal; Astur1, domain publik.*

![Grafik garis lurus merah pada sistem koordinat Kartesius](authority/assets/250px-Lineair-cartesiaans.png)

*Grafik fungsi linear pada koordinat Kartesius; MADe, [CC BY-SA
3.0](http://creativecommons.org/licenses/by-sa/3.0/).*

![Grafik merah suatu polinom berderajat lima](authority/assets/120px-Polynomialdeg5.png)

*Grafik polinom berderajat lima; Derbeth, [CC BY-SA
3.0](http://creativecommons.org/licenses/by-sa/3.0/).*

Inti contoh ini ialah bahwa ketiga objek geometris tersebut merupakan himpunan
nol bagi representasi gelanggang faktor yang berbeda dari $K[T]$. Dari sudut
pandang geometri aljabar, ketiganya adalah representasi yang berkedudukan sama
dari garis afin, walaupun “penampilan” mereka berbeda. Dalam geometri aljabar
kita harus memandangnya dengan cara yang membuat mereka tampak sama. Yang
terlihat hanyalah pembenaman berbeda dari objek geometris “sejati” yang secara
intrinsik bersesuaian dengan suatu aljabar-$K$, yaitu spektrum-$K$.

<!-- upstream_entity: Endlich erzeugte K-Algebren/K-Spektrum mit Zariski-Topologie/Definition -->

### Definisi: spektrum-$K$ {#br-ak-2025-2026-l12-def-01}

Untuk suatu aljabar-$K$ komutatif $R$ bertipe hingga, himpunan semua
homomorfisme aljabar-$K$

$$
\operatorname{Hom}_K(R,K)
$$

disebut *spektrum-$K$* dari $R$ dan dinotasikan dengan

$$
K\!-\!\operatorname{Spek}(R).
$$

Unsur-unsur dalam spektrum-$K$
$K\!-\!\operatorname{Spek}(R)$ kita pandang sebagai titik dan biasanya
kita lambangkan dengan $P$, walaupun menurut definisi unsur-unsur itu adalah
pemetaan, yakni homomorfisme aljabar-$K$ dari $R$ ke $K$. Untuk suatu unsur
gelanggang $f\in R$, kita kemudian menulis $f(P)$, bukan $P(f)$, untuk nilai
$f$ di bawah homomorfisme gelanggang yang dilambangkan dengan $P$. Memang,
lazim pula untuk memandang sebuah titik sebagai evaluasi fungsi-fungsi yang
terdefinisi di suatu lingkungan titik tersebut.

Spektrum-$K$ kembali dilengkapi dengan topologi Zariski. Untuk suatu ideal
$\mathfrak a\subseteq R$—atau bahkan untuk sembarang subhimpunan dari $R$—kita
menetapkan subhimpunan

$$
V(\mathfrak a)
=\left\{P\in K\!-\!\operatorname{Spek}(R)
\mid f(P)=0\ \text{untuk semua }f\in\mathfrak a\right\}
$$

sebagai himpunan tertutup. Penetapan ini benar-benar mendefinisikan suatu
topologi; lihat Soal 12.8. Komplemen terbukanya dilambangkan dengan
$D(\mathfrak a)$.

<!-- upstream_entity: Polynomring über Körper/Punkte im affinen Raum und K-Algebra-Homomorphismen/Identifizierung/Fakt -->

### Lema: titik ruang afin sebagai homomorfisme {#br-ak-2025-2026-l12-lem-01}

Misalkan $K$ suatu lapangan dan $K[X_1,\ldots,X_n]$ gelanggang polinomial
dalam $n$ variabel. Homomorfisme aljabar-$K$ dari
$K[X_1,\ldots,X_n]$ ke $K$ berkorespondensi secara bijektif dan alami dengan
titik-titik ruang afin

$$
\mathbb A_K^n=K^n.
$$

Titik $(a_1,\ldots,a_n)$ bersesuaian dengan homomorfisme substitusi
$X_i\mapsto a_i$. Dengan kata lain,

$$
K\!-\!\operatorname{Spek}\bigl(K[X_1,\ldots,X_n]\bigr)
=\mathbb A_K^n.
$$

#### Bukti {#br-ak-2025-2026-l12-lem-01-proof}

Suatu homomorfisme aljabar-$K$ selalu ditentukan oleh sebuah sistem pembangkit
aljabar-$K$. Jadi nilai-nilai pada variabel $X_i$ menentukan homomorfisme
aljabar-$K$ dari $K[X_1,\ldots,X_n]$ ke $K$. Homomorfisme substitusi demikian
ditentukan oleh $X_i\mapsto a_i$, dan di sini setiap pilihan nilai
$(a_1,\ldots,a_n)$ diperbolehkan.

<!-- upstream_entity: Endlich erzeugte K-Algebren/K-Spektrum/von K ist Punkt/Beispiel -->

### Contoh: spektrum-$K$ dari $K$ {#br-ak-2025-2026-l12-exm-02}

Spektrum-$K$ dari aljabar-$K$ $K$ hanya terdiri atas satu titik: identitas

$$
\operatorname{id}:K\longrightarrow K
$$

adalah satu-satunya homomorfisme aljabar-$K$ dari $K$ ke $K$. Secara umum
mungkin ada automorfisme lapangan lain pada $K$, tetapi automorfisme itu bukan
homomorfisme aljabar-$K$.

Teorema berikut sangat penting karena memberikan hubungan bijektif antara
spektrum-$K$ dari $R$ dan lokus nol yang berasal dari suatu representasi
gelanggang faktor dari $R$.

<!-- upstream_entity: Endlich erzeugte K-Algebren/K-Spektrum/Isomorph zu Einbettung/Fakt -->

### Teorema: spektrum-$K$ dan lokus nol {#br-ak-2025-2026-l12-thm-01}

Misalkan $K$ suatu lapangan dan $R$ aljabar-$K$ komutatif yang dibangkitkan
secara hingga, dengan spektrum-$K$
$K\!-\!\operatorname{Spek}(R)$. Misalkan

$$
R=K[X_1,\ldots,X_n]/\mathfrak a
$$

suatu representasi gelanggang faktor dari $R$, dengan homomorfisme faktor

$$
\varphi:K[X_1,\ldots,X_n]\longrightarrow R
$$

dan lokus nol yang bersesuaian
$V(\mathfrak a)\subseteq\mathbb A_K^n$. Pemetaan

$$
\begin{aligned}
K\!-\!\operatorname{Spek}(R)&\longrightarrow\mathbb A_K^n,\\
P&\longmapsto P\circ\varphi
\end{aligned}
$$

memberikan bijeksi antara $K\!-\!\operatorname{Spek}(R)$ dan
$V(\mathfrak a)$, dan bijeksi tersebut merupakan homeomorfisme terhadap
topologi Zariski.

#### Bukti {#br-ak-2025-2026-l12-thm-01-proof}

Mula-mula, pemetaan di atas terdefinisi dengan baik karena komposisi

$$
P\circ\varphi:
K[X_1,\ldots,X_n]
\xrightarrow{\varphi}K[X_1,\ldots,X_n]/\mathfrak a
\cong R\xrightarrow{P}K
$$

mendefinisikan homomorfisme aljabar-$K$ dari gelanggang polinomial ke $K$.
Menurut Lema 12.3, homomorfisme ini adalah homomorfisme substitusi pada suatu
$(a_1,\ldots,a_n)$ dan dapat diidentifikasi dengan titik yang bersesuaian di
ruang afin; secara tepat,

$$
a_i=P\bigl(\varphi(X_i)\bigr).
$$

Karena $P\circ\varphi$ memfaktor melalui $R$, ideal $\mathfrak a$ dipetakan ke
$0$. Jadi titik citra

$$
P\circ\varphi=(a_1,\ldots,a_n)
$$

terletak di $V(\mathfrak a)$. Dengan demikian kita memperoleh pemetaan

$$
\begin{aligned}
K\!-\!\operatorname{Spek}(R)&\longrightarrow
V(\mathfrak a)\subseteq\mathbb A_K^n,\\
P&\longmapsto P\circ\varphi,
\end{aligned}
$$

yang tinggal dibuktikan bijektif.

Misalkan $P_1,P_2\in K\!-\!\operatorname{Spek}(R)$ dua titik berbeda.
Keduanya adalah homomorfisme aljabar-$K$ yang berbeda. Karena homomorfisme
aljabar-$K$ ditentukan oleh nilainya pada suatu sistem pembangkit
aljabar-$K$, keduanya harus berbeda pada setidaknya satu citra variabel. Maka
koordinat yang bersesuaian juga berbeda, sehingga
$P_1\circ\varphi\ne P_2\circ\varphi$. Jadi pemetaan tersebut injektif.

Untuk surjektivitas, misalkan
$(a_1,\ldots,a_n)\in V(\mathfrak a)$. Homomorfisme aljabar-$K$ yang
bersesuaian,

$$
\begin{aligned}
K[X_1,\ldots,X_n]&\longrightarrow K,\\
X_i&\longmapsto a_i,
\end{aligned}
$$

melenyapkan setiap $F\in\mathfrak a$. Oleh sebab itu homomorfisme gelanggang
ini memfaktor melalui $K[X_1,\ldots,X_n]/\mathfrak a$. Homomorfisme hasil
faktorisasi itulah prapeta yang dicari di
$K\!-\!\operatorname{Spek}(R)$.

Untuk bagian topologi, ambil $G\in R$, suatu prapeta
$\widetilde G\in K[X_1,\ldots,X_n]$, dan titik
$P\in K\!-\!\operatorname{Spek}(R)$ dengan titik citra
$\widetilde P=P\circ\varphi\in V(\mathfrak a)$. Maka

$$
G(P)=P(G)=P\bigl(\varphi(\widetilde G)\bigr)
=(P\circ\varphi)(\widetilde G)
=\widetilde G(\widetilde P),
$$

sehingga lokus nol pada kedua sisi juga berkorespondensi. Dengan demikian
bijeksi tersebut merupakan homeomorfisme.

Teorema ini mengatakan bahwa setiap spektrum-$K$ dari suatu aljabar-$K$
bertipe hingga $R$ dapat diidentifikasi dengan himpunan tertutup Zariski dalam
suatu $\mathbb A_K^n$. Identifikasi demikian disebut *pembenaman tertutup*.

<!-- upstream_entity: Endlich erzeugte K-Algebren/Nullenstellengebilde zu verschiedenen Restklassendarstellungen sind isomorph/über K-Spektrum/Fakt -->

### Korolari: independensi topologis dari representasi {#br-ak-2025-2026-l12-cor-01}

Misalkan $K$ suatu lapangan dan $R$ aljabar-$K$ komutatif yang dibangkitkan
secara hingga dengan dua representasi gelanggang faktor

$$
R\cong K[X_1,\ldots,X_n]/\mathfrak a
\qquad\text{dan}\qquad
R\cong K[X_1,\ldots,X_m]/\mathfrak b,
$$

beserta lokus nol yang bersesuaian

$$
V(\mathfrak a)\subseteq\mathbb A_K^n
\qquad\text{dan}\qquad
V(\mathfrak b)\subseteq\mathbb A_K^m.
$$

Dengan topologi Zariski terinduksinya, kedua lokus nol tersebut homeomorfik.

#### Bukti {#br-ak-2025-2026-l12-cor-01-proof}

Menurut Teorema 12.5, kedua lokus nol homeomorfik dengan
$K\!-\!\operatorname{Spek}(R)$, sehingga keduanya juga homeomorfik satu
sama lain.

Jika $R$ adalah gelanggang nol, spektrum-$K$-nya kosong. Jika $K$ tidak
tertutup secara aljabar, spektrum gelanggang lain pun dapat kosong. Akan
tetapi, jika $K$ tertutup secara aljabar dan $R\ne0$, spektrumnya tidak kosong.
Dalam keadaan ini berlaku lagi suatu Nullstellensatz Hilbert; lihat
Soal 12.10.

## Spektrum-$K$ sebagai funktor {#br-ak-2025-2026-l12-s02}

<!-- upstream_entity: Affine Varietäten/K-Spektren als Funktor/Fakt -->

### Teorema: pemetaan spektrum {#br-ak-2025-2026-l12-thm-02}

Misalkan $K$ suatu lapangan, $R$ dan $S$ aljabar-$K$ komutatif bertipe hingga,
serta

$$
\varphi:R\longrightarrow S
$$

suatu homomorfisme aljabar-$K$. Homomorfisme ini menginduksi pemetaan

$$
\begin{aligned}
\varphi^*:K\!-\!\operatorname{Spek}(S)&\longrightarrow
K\!-\!\operatorname{Spek}(R),\\
P&\longmapsto P\circ\varphi.
\end{aligned}
$$

Pemetaan ini kontinu terhadap topologi Zariski.

#### Bukti {#br-ak-2025-2026-l12-thm-02-proof}

Keberadaan pemetaan tersebut jelas: kepada homomorfisme aljabar-$K$
$P:S\to K$ kita pasangkan komposisi

$$
R\xrightarrow{\varphi}S\xrightarrow{P}K.
$$

Prapeta himpunan terbuka
$D(f)\subseteq K\!-\!\operatorname{Spek}(R)$ ialah

$$
\begin{aligned}
(\varphi^*)^{-1}(D(f))
&=\{P\in K\!-\!\operatorname{Spek}(S)
       \mid\varphi^*(P)\in D(f)\}\\
&=\{P\in K\!-\!\operatorname{Spek}(S)
       \mid P\circ\varphi\in D(f)\}\\
&=\{P\in K\!-\!\operatorname{Spek}(S)
       \mid(P\circ\varphi)(f)\ne0\}\\
&=\{P\in K\!-\!\operatorname{Spek}(S)
       \mid P(\varphi(f))\ne0\}\\
&=D(\varphi(f)).
\end{aligned}
$$

Jadi prapeta himpunan terbuka kembali terbuka, dan pemetaan tersebut kontinu.

Pemetaan $\varphi^*$ yang diperkenalkan dalam Teorema 12.7 disebut *pemetaan
spektrum* yang bersesuaian dengan $\varphi$.

<!-- upstream_entity: Endlich erzeugte K-Algebren/K-Spektren als Funktor/Verschiedene Homomorphismen/Fakt -->

### Proposisi: beberapa bentuk pemetaan spektrum {#br-ak-2025-2026-l12-prop-01}

Misalkan $K$ suatu lapangan dan
$\varphi:R\to S$ homomorfisme aljabar-$K$ antara aljabar-$K$ bertipe hingga,
dengan $\varphi^*$ pemetaan spektrum yang bersesuaian. Pernyataan-pernyataan
berikut berlaku.

1. Untuk suatu homomorfisme aljabar-$K$ $P:R\to K$, pemetaan spektrum
   terinduksi $P^*$ adalah pemetaan yang membawa satu-satunya titik

   $$
   \{\operatorname{id}\}=K\!-\!\operatorname{Spek}(K)
   $$

   ke titik $P\in K\!-\!\operatorname{Spek}(R)$.
2. Homomorfisme substitusi yang ditentukan oleh $F\in R$,

   $$
   \begin{aligned}
   \varphi:K[T]&\longrightarrow R,\\
   T&\longmapsto F,
   \end{aligned}
   $$

   menginduksi pemetaan spektrum

   $$
   \begin{aligned}
   \varphi^*:K\!-\!\operatorname{Spek}(R)&\longrightarrow
   K\!-\!\operatorname{Spek}(K[T])=\mathbb A_K^1,\\
   P&\longmapsto F(P).
   \end{aligned}
   $$
3. Jika $\varphi:R\to S$ surjektif, maka pemetaan spektrum

   $$
   \varphi^*:K\!-\!\operatorname{Spek}(S)\longrightarrow
   K\!-\!\operatorname{Spek}(R)
   $$

   merupakan pembenaman tertutup dengan citra $V(\ker\varphi)$.
4. Pemetaan spektrum yang bersesuaian dengan pemetaan surjektif

   $$
   K[X_1,\ldots,X_n]\longrightarrow S
   $$

   sama dengan pemetaan

   $$
   \varphi^*:K\!-\!\operatorname{Spek}(S)\longrightarrow
   K\!-\!\operatorname{Spek}(K[X_1,\ldots,X_n])
   \cong\mathbb A_K^n
   $$

   yang didefinisikan dalam Teorema 12.5.
5. Misalkan $F_i\in K[X_1,\ldots,X_n]$ untuk $i=1,\ldots,m$, dan

   $$
   \begin{aligned}
   \varphi:K[Y_1,\ldots,Y_m]&\longrightarrow K[X_1,\ldots,X_n],\\
   Y_i&\longmapsto F_i
   \end{aligned}
   $$

   homomorfisme substitusi yang bersesuaian. Dengan identifikasi pada Lema
   12.3, pemetaan spektrum

   $$
   \varphi^*:\mathbb A_K^n
   =K\!-\!\operatorname{Spek}(K[X_1,\ldots,X_n])
   \longrightarrow
   \mathbb A_K^m
   =K\!-\!\operatorname{Spek}(K[Y_1,\ldots,Y_m])
   $$

   sama dengan pemetaan polinomial langsung

   $$
   (x_1,\ldots,x_n)\longmapsto
   \bigl(F_1(x_1,\ldots,x_n),\ldots,F_m(x_1,\ldots,x_n)\bigr).
   $$

#### Bukti {#br-ak-2025-2026-l12-prop-01-proof}

(1) mengikuti dari $\operatorname{id}\circ P=P$.

Untuk (2), pada komposisi

$$
K[T]\xrightarrow{\varphi}R\xrightarrow{P}K,
$$

$T$ dipetakan ke $P(F)=F(P)$.

(3) didasarkan pada pertimbangan serupa dengan yang digunakan dalam bukti
Teorema 12.5; pertimbangan itu juga membuktikan (4). Untuk (5), lihat Soal
12.18.

Pernyataan (2) khususnya mengatakan bahwa unsur-unsur gelanggang $R$ dapat
dipandang sebagai fungsi dari spektrum-$K$
$K\!-\!\operatorname{Spek}(R)$ ke $\mathbb A_K^1$. Jadi kita telah
memperkenalkan suatu objek geometris yang merealisasikan unsur gelanggang
sebagai fungsi.

## Sifat lain spektrum-$K$ {#br-ak-2025-2026-l12-s03}

<!-- upstream_entity: Affine Varietäten/K-Spektren/Polynomring und affine Gerade/Fakt -->

### Lema: menambahkan satu variabel {#br-ak-2025-2026-l12-lem-02}

Misalkan $K$ suatu lapangan dan $R$ aljabar-$K$ komutatif yang dibangkitkan
secara hingga. Maka terdapat bijeksi alami

$$
K\!-\!\operatorname{Spek}(R[X])
\cong K\!-\!\operatorname{Spek}(R)\times\mathbb A_K^1.
$$

#### Bukti {#br-ak-2025-2026-l12-lem-02-proof}

Suatu homomorfisme aljabar-$K$ $R[T]\to K$ menginduksi homomorfisme
aljabar-$K$ $R\to K$, sementara $T$ dipetakan ke suatu unsur tertentu
$a\in K$. Sebaliknya, kedua data tersebut menentukan sebuah homomorfisme
aljabar-$K$ $R[T]\to K$ secara unik.

Peringatan: pernyataan di atas hanya memberikan bijeksi alami pada tingkat
titik. Jika himpunan produk di sebelah kanan diberi topologi produk, bijeksi
ini bukan homeomorfisme dengan topologi Zariski di sebelah kiri. Secara
khusus,

$$
\mathbb A_K^2=\mathbb A_K^1\times\mathbb A_K^1,
$$

tetapi topologi Zariski pada bidang afin bukan topologi produk dari topologi
Zariski pada garis afin dengan dirinya sendiri.

### Catatan: produk melalui hasil kali tensor {#br-ak-2025-2026-l12-rem-01}

Jika

$$
X=K\!-\!\operatorname{Spek}(R)
\qquad\text{dan}\qquad
Y=K\!-\!\operatorname{Spek}(S),
$$

maka himpunan produk $X\times Y$ juga dapat direpresentasikan sebagai
spektrum-$K$ suatu aljabar-$K$, yaitu

$$
X\times Y\cong
K\!-\!\operatorname{Spek}(R\otimes_K S),
$$

dengan $\otimes$ menyatakan hasil kali tensor. Kita tidak akan membahasnya
secara terperinci. Untuk memperoleh gambaran, ambil

$$
R=K[X_1,\ldots,X_n]/\mathfrak a
\qquad\text{dan}\qquad
S=K[Y_1,\ldots,Y_m]/\mathfrak b.
$$

Maka

$$
R\otimes_K S
\cong
K[X_1,\ldots,X_n,Y_1,\ldots,Y_m]/(\mathfrak a+\mathfrak b).
$$

Untuk definisi *ad hoc* ini, belum jelas bahwa hasilnya tidak bergantung pada
pilihan representasi gelanggang faktor.
