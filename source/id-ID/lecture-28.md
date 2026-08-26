---
title: "Kuliah 28 - Varietas Proyektif dan Kurva Bidang Proyektif"
stable_id: br-ak-2012-l28
language: id-ID
source_author: "Holger Brenner"
frozen_revision_contributor: "Arbota"
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 28"
upstream_pageid: 50734
upstream_revid: 1052516
upstream_timestamp: "2025-08-27T13:52:03Z"
upstream_mediawiki_sha1: d037d0173bca4c443e06c7991d830568fa8dc0ea
source_url: "https://de.wikiversity.org/w/index.php?oldid=1052516"
authority_manifest: authority/wikiversity/unit-28/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: f2e34fc420c4beec300ea9e0accc52598e12c27f46c9022611996b1b43e29a99
lecture_xml: authority/wikiversity/unit-28/lecture-28.xml
lecture_xml_sha256: 3dc1abff96585199774b74910d1fc93102d0baf31e09ffa432a6e3966ddb5423
lecture_expanded_tex: authority/wikiversity/unit-28/lecture-28-expanded.tex
lecture_expanded_tex_sha256: ed9054224eb4f1d8d5849d9e44c88f82107866c8f0944ee7cb047e27ad337709
license: "Current semantic course text and this translation: CC BY-SA 4.0. Unit 28 reader media retain their component-specific CC0 or public-domain status as recorded in authority/RIGHTS-unit-28.csv. No blanket relicensing claim is made."
source_component_license_route: "Semantic-site rights notice: CC BY-SA 4.0; media component rights remain item-specific; official-PDF notices remain component-specific; no blanket relicensing claim."
license_evidence: "authority/UNIT_28_AUTHORITY_FREEZE.md; authority/RIGHTS-unit-28.csv; authority/ASSET_CLOSURE-unit-28.json"
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_semantic_entities: 19
source_corrections: 9
correction_ids: "AGC-CORR-0115; AGC-CORR-0116; AGC-CORR-0117; AGC-CORR-0118; AGC-CORR-0119; AGC-CORR-0120; AGC-CORR-0123; AGC-CORR-0124; AGC-CORR-0125"
reader_media_positions: 4
---

# Kuliah 28: Varietas Proyektif dan Kurva Bidang Proyektif {#br-ak-2012-l28}

## Varietas proyektif {#br-ak-2012-l28-s01}

<!-- upstream_entity: Projektive Varietäten/Über Körper/Nullstellengebilde zu homogenen Polynomen/Definition -->

### Definisi 28.1: varietas proyektif {#br-ak-2012-l28-def-01}

Suatu *varietas proyektif* adalah sebuah himpunan bagian tertutup Zariski

$$
V_+(\mathfrak a)\subseteq\mathbb P_K^n,
$$

dengan $\mathfrak a$ suatu ideal homogen di
$K[X_0,X_1,\ldots,X_n]$. Jadi, suatu varietas proyektif $Y$ merupakan
himpunan titik nol di ruang proyektif dari suatu himpunan berhingga polinom
homogen.

Dengan topologi terinduksi, varietas proyektif kembali dilengkapi dengan
topologi Zariski. Himpunan terbukanya berbentuk $D_+(\mathfrak b)$ untuk
suatu ideal homogen $\mathfrak b$, baik di $K[X_0,\ldots,X_n]$ maupun di
gelanggang hasil bagi

$$
K[X_0,\ldots,X_n]/\mathfrak a,
$$

yang juga disebut *gelanggang koordinat homogen* dari
$V_+(\mathfrak a)$. Khususnya, setiap elemen homogen
$F\in K[X_0,\ldots,X_n]$ mendefinisikan himpunan terbuka

$$
D_+(F)\subseteq Y.
$$

<!-- upstream_entity: Projektive Varietät/Wird überdeckt von affinen Varietäten/Fakt -->

### Lema 28.2: penutup oleh varietas afin {#br-ak-2012-l28-lem-01}

Misalkan $Y\subseteq\mathbb P_K^n$ suatu varietas proyektif. Ruang-ruang
afin

$$
D_+(X_i)\cong\mathbb A_K^n\subset\mathbb P_K^n
$$

memberikan varietas-varietas afin

$$
D_+(X_i)\cap Y
$$

yang menutupi $Y$. Khususnya, untuk setiap titik $P\in Y$ dan setiap
lingkungan terbuka $P\in U$, terdapat lingkungan terbuka afin dari $P$ yang
termuat di dalam $U$.

<!-- upstream_entity: Projektive Varietät/Wird überdeckt von affinen Varietäten/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l28-lem-01-proof}

Di dalam $Y$ kita mempunyai

$$
D_+^Y(X_i):=Y\cap D_+^{\mathbb P_K^n}(X_i)
\cong Y\cap\mathbb A_K^n,
$$

dengan $D_+^Y(X_i)$ menyatakan himpunan terbuka relatif di $Y$, sedangkan
$D_+^{\mathbb P_K^n}(X_i)$ adalah bagan standar di ruang proyektif ambien.
Karena itu, $D_+^Y(X_i)$ merupakan himpunan bagian tertutup (lihat Soal 28.2)
dari ruang afin $D_+^{\mathbb P_K^n}(X_i)\cong\mathbb A_K^n$, dan dengan
demikian merupakan varietas afin. Karena semua
$D_+^{\mathbb P_K^n}(X_i)$ menutupi ruang proyektif, himpunan-himpunan
$D_+^Y(X_i)$ menutupi $Y$.

> **Jembatan edisi.** Untuk memperoleh klaim tentang lingkungan terbuka
> sembarang $U$, pilih bagan afin di atas yang memuat $P$, lalu perkecil
> irisannya dengan suatu himpunan terbuka utama yang memuat $P$ dan termuat di
> dalam $U$. Himpunan terbuka utama itu afin, sehingga merupakan lingkungan
> afin yang dicari. $\square$

> **Catatan edisi - notasi relatif dan ambien.** Sumber memakai
> $D_+(X_i)$ sekaligus untuk himpunan terbuka relatif di $Y$ dan untuk bagan
> standar di $\mathbb P_K^n$. Edisi menampilkan irisan dengan $Y$ agar kedua
> makna itu tidak tertukar.

Akibat langsungnya adalah bahwa konsep-konsep lokal yang telah dikembangkan
untuk varietas afin berlaku juga pada varietas proyektif. Untuk memeriksa
suatu sifat pada sebuah titik, kita dapat segera berpindah ke lingkungan
terbuka afin titik itu. Hal ini berlaku, misalnya, untuk kemulusan,
normalitas, dan fungsi reguler.

## Fungsi aljabar dan morfisme {#br-ak-2012-l28-s02}

Dengan hasil yang baru saja dibuktikan, kita dapat kembali mendefinisikan apa
yang dimaksud dengan fungsi reguler atau aljabar pada suatu varietas
proyektif.

<!-- upstream_entity: Projektive Varietät/Als abgeschlossene Teilmenge/Algebraische Funktion/Definition -->

### Definisi 28.3: fungsi reguler {#br-ak-2012-l28-def-02}

Misalkan $K$ lapangan tertutup secara aljabar,
$Y\subseteq\mathbb P_K^n$ suatu varietas proyektif, $U\subseteq Y$ suatu
himpunan terbuka, dan $P\in U$. Suatu fungsi

$$
f:U\longrightarrow\mathbb A_K^1=K
$$

disebut *aljabar*, *reguler*, atau *polinomial* di $P$ jika terdapat
lingkungan terbuka afin

$$
P\in V\subseteq U
$$

sedemikian sehingga $f|_V$ aljabar di $P$. Fungsi $f$ disebut aljabar pada
$U$ jika ia aljabar di setiap titik dalam $U$.

Untuk suatu himpunan terbuka $U$, himpunan semua fungsi reguler pada $U$
kembali membentuk aljabar-$K$ komutatif yang ditulis
$\Gamma(U,\mathcal O)$. Mulai sekarang, sebuah varietas proyektif dipahami
sebagai himpunan titik nol proyektif dengan topologi Zariski terinduksi dan
dengan *berkas struktur* $\mathcal O$ fungsi-fungsi reguler.

Konsep-konsep ini segera berlaku pula pada himpunan-himpunan terbuka, sehingga
mengarah pada pengertian varietas kuasiprojektif.

<!-- upstream_entity: Varietäten/K/Quasiprojektive Varietät/Definition -->

### Definisi 28.4: varietas kuasiprojektif {#br-ak-2012-l28-def-03}

Suatu himpunan bagian terbuka dari sebuah varietas proyektif, dengan topologi
Zariski terinduksi dan berkas struktur fungsi-fungsi aljabar, disebut
*varietas kuasiprojektif*.

Khususnya, varietas proyektif maupun varietas afin bersifat
kuasiprojektif. Untuk yang terakhir, suatu varietas afin
$Y\subseteq\mathbb A_K^n$ dapat diperluas menjadi varietas proyektif
$\widetilde Y\subseteq\mathbb P_K^n$ yang memuat $Y$ sebagai himpunan
terbuka.

Definisi morfisme juga dapat diterapkan kata demi kata pada situasi yang lebih
umum ini.

<!-- upstream_entity: Quasiprojektive Varietäten/K/Morphismus/Definition -->

### Definisi 28.5: morfisme varietas kuasiprojektif {#br-ak-2012-l28-def-04}

Misalkan $X$ dan $Y$ varietas kuasiprojektif di atas suatu lapangan tertutup
secara aljabar, dan misalkan

$$
\psi:Y\longrightarrow X
$$

suatu pemetaan kontinu. Pemetaan $\psi$ disebut *morfisme* jika, untuk setiap
himpunan terbuka $U\subseteq X$ dan setiap fungsi aljabar
$f\in\Gamma(U,\mathcal O_X)$, komposisi

$$
f\circ\psi:
\psi^{-1}(U)\longrightarrow U\stackrel{f}{\longrightarrow}\mathbb A_K^1
$$

berada di $\Gamma(\psi^{-1}(U),\mathcal O_Y)$.

## Homogenisasi dan penutupan proyektif {#br-ak-2012-l28-s03}

Perhatikan hiperbola

$$
V(XY-1)\subset\mathbb A_K^2\subset\mathbb P_K^2.
$$

Hiperbola itu tertutup di bidang afin, tetapi tidak tertutup di bidang
proyektif. Benamkan bidang afin sebagai $V(Z-1)$ di ruang berdimensi tiga,
lalu perhatikan garis-garis melalui titik asal dan titik-titik hiperbola.
Secara geometris garis-garis itu semakin miring dan, dalam gambaran real atau
kompleks, mendekati sumbu $x$ dan sumbu $y$. Perhitungan aljabar berikut
memberikan pernyataan yang berlaku atas lapangan dasar yang ditetapkan.

> **Catatan edisi - lingkup intuisi topologis.** Ungkapan "mendekati" pada
> sumber merupakan intuisi Euclidean untuk $\mathbb R$ atau $\mathbb C$,
> bukan pernyataan topologis atas lapangan sembarang.

<!-- upstream_entity: Polynomring/Homogenisierung zu einem Ideal/Definition -->

### Definisi 28.6: homogenisasi suatu ideal {#br-ak-2012-l28-def-05}

Untuk suatu ideal

$$
\mathfrak a\subseteq K[X_1,\ldots,X_n],
$$

ideal di $K[X_1,\ldots,X_n,Z]$ yang dibangkitkan oleh homogenisasi semua
elemen $\mathfrak a$ disebut *homogenisasi* $\mathfrak a^h$ dari
$\mathfrak a$.

Pada umumnya tidak cukup hanya menghomogenkan suatu sistem pembangkit ideal
$\mathfrak a$.

<!-- upstream_entity: Affine Varietät/Projektiver Abschluss/Definition -->

### Definisi 28.7: penutupan proyektif {#br-ak-2012-l28-def-06}

Untuk suatu varietas afin

$$
V(\mathfrak a)\subseteq\mathbb A_K^n\subseteq\mathbb P_K^n,
$$

penutupan Zariski dari $V(\mathfrak a)$ di $\mathbb P_K^n$ disebut
*penutupan proyektif* dari $V(\mathfrak a)$.

<!-- upstream_entity: Affine Varietät/Projektiver Abschluss/Beschreibung mit Homogenisierung/Fakt -->

### Teorema 28.8: penutupan proyektif melalui homogenisasi {#br-ak-2012-l28-thm-01}

Misalkan $K$ lapangan tertutup secara aljabar dan

$$
V=V(\mathfrak a)\subseteq\mathbb A_K^n\cong D_+(X_0)
$$

suatu varietas afin. Penutupan proyektif $V(\mathfrak a)$ di
$\mathbb P_K^n$ adalah $V_+(\mathfrak b)$, dengan $\mathfrak b$ homogenisasi
$\mathfrak a$ di $K[X_0,X_1,\ldots,X_n]$.

<!-- upstream_entity: Affine Varietät/Projektiver Abschluss/Beschreibung mit Homogenisierung/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l28-thm-01-proof}

Titik $P=(x_1,\ldots,x_n)$ di $\mathbb A_K^n$ menentukan titik
$\widehat P=(1,x_1,\ldots,x_n)$ di $\mathbb P_K^n$. Untuk
$F\in K[X_1,\ldots,X_n]$ dan homogenisasinya $\widehat F$, berlaku

$$
F(P)=\widehat F(\widehat P).
$$

Karena itu, semua polinom homogen dalam $\mathfrak b$ lenyap pada
$V(\mathfrak a)$, sehingga

$$
V(\mathfrak a)\subseteq V_+(\mathfrak b).
$$

Kita memperoleh diagram komutatif dengan semua panah injektif,

$$
\begin{matrix}
V(\mathfrak a)&\longrightarrow&V_+(\mathfrak b)\\
\downarrow&&\downarrow\\
\mathbb A_K^n&\longrightarrow&\mathbb P_K^n.
\end{matrix}
$$

Misalkan penutupan proyektif $V(\mathfrak a)$ ditulis
$V_+(\mathfrak c)$ untuk suatu ideal homogen $\mathfrak c$. Dari minimalitas
penutupan diperoleh $V_+(\mathfrak c)\subseteq V_+(\mathfrak b)$. Untuk
membuktikan inklusi sebaliknya cukup menunjukkan

$$
\mathfrak c\subseteq\operatorname{rad}(\mathfrak b).
$$

Kita boleh mengambil $F\in\mathfrak c$ homogen. Tulislah
$F=X_0^rG$, dengan $G$ bukan kelipatan $X_0$. Karena $F$ lenyap pada
$V(\mathfrak a)$ dan $X_0$ tidak lenyap pada
$V(\mathfrak a)\subseteq D_+(X_0)$, polinom $G$ juga lenyap di sana. Maka
kita dapat menganggap $F$ bukan kelipatan $X_0$.

Dehomogenisasi

$$
\widetilde F=F(1,X_1,\ldots,X_n)
$$

lenyap pada $V(\mathfrak a)$ dan mempunyai derajat yang sama dengan $F$.
Dengan Teorema Titik Nol Hilbert, setelah mengganti $\mathfrak a$ oleh
radikalnya tanpa mengubah varietas, diperoleh
$\widetilde F\in\mathfrak a$. Menghomogenkan kembali menunjukkan
$F\in\mathfrak b$. Jadi kedua inklusi berlaku dan penutupan itu tepat
$V_+(\mathfrak b)$. $\square$

## Kurva bidang proyektif {#br-ak-2012-l28-s04}

<!-- upstream_entity: Algebraische Kurve/Projektive ebene Kurve/Definition -->

### Definisi 28.9: kurva bidang proyektif {#br-ak-2012-l28-def-07}

Suatu *kurva bidang proyektif* adalah himpunan titik nol

$$
C=V_+(F)\subset\mathbb P_K^2
$$

dari suatu polinom homogen tak konstan $F\in K[X,Y,Z]$.

Untuk kurva bidang afin $V=V(G)\subset\mathbb A_K^2\subset\mathbb P_K^2$,
penutupan Zariski dari $V$ di $\mathbb P_K^2$ disebut penutupan proyektif
kurva tersebut.

<!-- upstream_entity: Ebene projektive Kurve/Gleichung für projektiven Abschluss mit Homogenisierung/Fakt -->

### Korolari 28.10: persamaan penutupan proyektif kurva {#br-ak-2012-l28-cor-01}

Misalkan $K$ lapangan tertutup secara aljabar dan

$$
V=V(G)\subseteq\mathbb A_K^2\subseteq\mathbb P_K^2,
\qquad G\in K[X,Y].
$$

Penutupan Zariski $V$ di $\mathbb P_K^2$ adalah

$$
C=V_+(H),
$$

dengan $H$ homogenisasi $G$ di $K[X,Y,Z]$.

<!-- upstream_entity: Ebene projektive Kurve/Gleichung für projektiven Abschluss mit Homogenisierung/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l28-cor-01-proof}

Pernyataan ini mengikuti langsung dari Teorema 28.8 dan fakta bahwa
homogenisasi suatu ideal utama dibangkitkan oleh homogenisasi pembangkitnya.
$\square$

> **Catatan edisi - dua rujukan sumber yang belum terselesaikan.** Pada
> langkah sebelumnya sumber mencetak `nach Aufgabe *****` sambil menaut ke
> soal tentang homogenisasi ideal utama. Sesudah korolari, sumber juga
> mencetak `siehe Aufgabe *****` sambil menaut ke soal tentang persamaan
> homogen penutupan proyektif atas lapangan yang tidak tertutup secara
> aljabar. Nomor kedua soal tidak diberikan; edisi mempertahankan isi tautan
> tanpa menebak nomornya.

Tanpa hipotesis bahwa lapangan tertutup secara aljabar, pernyataan tersebut
tidak selalu berlaku.

<!-- upstream_entity: Ebene projektive Kurve/Verschiedene affine Ausschnitte/Glattheit/Bemerkung -->

### Catatan 28.11: bagan afin dan titik di tak hingga {#br-ak-2012-l28-rem-01}

Misalkan $G\in K[X,Y]$ dan $F\in K[X,Y,Z]$ homogenisasinya. Kita memperoleh
kembali $G$ dari $F$ dengan menetapkan $Z=1$. Polinom $G$ mendeskripsikan
irisan $D_+(Z)\cap V_+(F)$. Dua bagian afin lainnya,

$$
D_+(X)\cap V_+(F)
\quad\text{dan}\quad
D_+(Y)\cap V_+(F),
$$

berperan setara dan memberikan lingkungan afin bagi titik-titik
$C=V_+(F)$ yang tidak terletak di $D_+(Z)$.

Untuk memeriksa kemulusan di $P\in C$, pilih lingkungan terbuka afin,
sebaiknya salah satu $D_+(L)\cap C$ dengan $L=X,Y,Z$, lalu gunakan kriteria
turunan pada persamaan afin di bagan itu. Hasilnya tidak bergantung pada
bagan yang dipilih, walaupun suatu bagan mungkin lebih mudah secara
komputasional.

Dari sudut pandang kurva afin $V(G)$, titik-titik di tak hingga adalah

$$
V_+(F)\cap V_+(Z).
$$

Ini adalah irisan kurva proyektif dengan suatu garis proyektif.

Irisan ini berhingga kecuali garis $V_+(Z)$ merupakan komponen kurva. Hal
itu tidak terjadi jika kita mulai dari kurva afin, sebab $Z$ bukan pembagi
homogenisasi $F$. Tulislah dekomposisi homogen

$$
G=G_d+\cdots+G_m,\qquad m\leq d,
$$

sehingga

$$
F=G_d+G_{d-1}Z+\cdots+G_mZ^{d-m}.
$$

Menetapkan $Z=0$ menunjukkan bahwa titik-titik di tak hingga diperoleh dari
titik nol proyektif polinom homogen $G_d(X,Y)$. Jadi derajat $d$ segera
memberi batas atas bagi banyaknya titik di tak hingga kurva.

<!-- upstream_entity: Ebene projektive Kurven/Kegelschnitt als affine Ausschnitte/Beispiel -->

### Contoh 28.12: irisan kerucut sebagai bagan afin {#br-ak-2012-l28-ex-01}

Anggap $\operatorname{char}(K)\ne2$, dan perhatikan kerucut standar

$$
V(X^2+Y^2-Z^2)\subset\mathbb A_K^3.
$$

Karena persamaannya homogen, kerucut itu sekaligus dapat dipandang sebagai
kurva bidang proyektif berderajat dua

$$
V_+(X^2+Y^2-Z^2)\subset\mathbb P_K^2.
$$

Irisan kerucut dengan sembarang bidang $E\subset\mathbb A_K^3$ disebut
*irisan kerucut*. Jika $E$ tidak melalui titik asal, bidang itu secara alami
dapat diidentifikasi dengan suatu bidang afin terbuka
$D_+(L)\subseteq\mathbb P_K^2$, dengan $L$ bentuk linear homogen yang
mendeskripsikan subruang vektor sejajar dengan $E$. Irisan kerucut dengan
$E$ merupakan berbagai bagian afin dari kurva proyektif yang sama. Karena
itu, lingkaran, hiperbola, dan parabola adalah bagian-bagian afin semacam
ini.

Sebaliknya, irisan dengan bidang yang melalui titik asal, bila dipandang
secara proyektif, merupakan himpunan berhingga

$$
V_+(X^2+Y^2-Z^2)\cap V_+(L).
$$

> **Catatan edisi - karakteristik dua.** Sumber tidak membatasi
> karakteristik. Dalam karakteristik $2$, polinom di atas menjadi
> $(X+Y+Z)^2$; jika $L=X+Y+Z$, irisan proyektifnya adalah seluruh garis dan
> bukan himpunan berhingga. Batasan karakteristik di atas memastikan koniknya
> tak singular dan tidak mempunyai garis sebagai komponen.

<!-- upstream_entity: Projektive Kurve/Fermat-Kurve vom Grad d/Definition -->

### Definisi 28.13: kurva Fermat {#br-ak-2012-l28-def-08}

Misalkan $K$ suatu lapangan dan $d\geq1$. Kurva bidang proyektif

$$
V_+(X^d+Y^d+Z^d)\subseteq\mathbb P_K^2
$$

disebut *kurva Fermat* berderajat $d$. Untuk $d=1$, kurva itu hanyalah
sebuah garis proyektif.

> **Catatan edisi - operator titik nol proyektif.** Pada definisi ini sumber
> menulis $V(X^d+Y^d+Z^d)$ walaupun objek berada di $\mathbb P_K^2$; lema
> berikutnya menulis $V_+$ dengan benar. Edisi memakai $V_+$ secara konsisten.

<!-- upstream_entity: Projektive Kurve/Fermat-Kurve vom Grad d/Glattheit/Fakt -->

### Lema 28.14: kemulusan kurva Fermat {#br-ak-2012-l28-lem-02}

Misalkan $K$ lapangan tertutup secara aljabar dengan karakteristik
$p\geq0$, dan misalkan

$$
C=V_+(X^d+Y^d+Z^d)\subset\mathbb P_K^2
$$

kurva Fermat berderajat $d$. Jika karakteristik $K$ tidak membagi $d$, maka
$C$ merupakan kurva mulus.

<!-- upstream_entity: Projektive Kurve/Fermat-Kurve vom Grad d/Glattheit/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l28-lem-02-proof}

Kemulusan adalah sifat lokal, sehingga cukup bekerja pada sembarang bagian
afin. Karena situasinya simetris, perhatikan

$$
V(X^d+Y^d+1)\subset\mathbb A_K^2.
$$

Turunan parsialnya adalah $dX^{d-1}$ dan $dY^{d-1}$. Hipotesis
karakteristik memberi $d\ne0$. Jika $d=1$, kedua turunan merupakan konstanta
tak nol, sehingga tidak pernah lenyap. Jika $d>1$, kedua turunan hanya lenyap
bersama di $x=y=0$, dan titik itu tidak berada pada kurva. $\square$

> **Catatan edisi - kasus derajat satu.** Sumber menyatakan langsung bahwa
> kedua turunan hanya lenyap bersama di $(0,0)$; pernyataan itu tidak berlaku
> untuk $d=1$, ketika kedua turunan justru konstan dan tak nol. Pemisahan kasus
> di atas mempertahankan kesimpulan kemulusan untuk semua $d$ yang diizinkan.

![Pola bola sepak yang menggambarkan permukaan genus nol](authority/assets/Soccerball.svg)

*Sfera atau permukaan genus nol. Berkas OpenClipart, unggahan Commons saat
ini oleh MapGrid, CC0 1.0; label historis kursus mencatat Ranveig/PD.*

![Ilustrasi torus sebagai permukaan dengan satu gagang](authority/assets/Torus_illustration.png)

*Torus, permukaan genus satu. Oleg Alexandrov, domain publik.*

![Ilustrasi torus ganda sebagai permukaan dengan dua gagang](authority/assets/Double_torus_illustration.png)

*Torus ganda, permukaan genus dua. Oleg Alexandrov, domain publik.*

![Ilustrasi sfera dengan tiga gagang](authority/assets/Sphere_with_three_handles.png)

*Sfera dengan tiga gagang, permukaan genus tiga. Oleg Alexandrov, domain
publik.*

<!-- upstream_entity: Glatte projektive Kurven/C/Kurzübersicht zur topologischen Gestalt/Bemerkung -->

### Catatan 28.15: bentuk topologis dan genus {#br-ak-2012-l28-rem-02}

Jika lapangan dasar adalah $\mathbb C$, kurva proyektif mulus dapat dipandang
sebagai manifold real berdimensi dua yang kompak dan berorientasi. Secara topologis,
manifold seperti itu homeomorfik dengan permukaan sfera yang diberi $g$
gagang. Bilangan $g$ disebut *genus* permukaan real tersebut, dan juga genus
kurvanya.

Garis proyektif kompleks adalah sfera berdimensi dua dan tidak memiliki
gagang, sehingga genusnya $0$. Permukaan genus $1$ adalah torus (seperti ban
mobil), yang homeomorfik dengan $S^1\times S^1$. Dalam eksposisi sumber,
kurva proyektif yang sebagai manifold topologis bergenus satu disebut kurva
eliptik.

> **Catatan edisi - konvensi kurva eliptik.** Dalam terminologi modern,
> kurva eliptik biasanya berarti kurva proyektif mulus bergenus satu
> bersama satu titik dasar. Pernyataan sumber mendeskripsikan kurva genus
> satu tanpa data titik dasar; edisi mempertahankan paparannya dan mencatat
> perbedaan konvensi ini.

Genus juga mempunyai definisi aljabar dan karena itu terdefinisi untuk kurva
proyektif mulus di atas setiap lapangan tertutup secara aljabar. Genus sama
dengan dimensi-$K$ grup kohomologi pertama berkas struktur dan juga sama
dengan dimensi-$K$ ruang bentuk diferensial global pada kurva.

Untuk setiap $g$ terdapat kurva proyektif bergenus $g$. Secara khusus,
setiap permukaan real berdimensi dua yang kompak dan berorientasi dapat direalisasikan
sebagai kurva proyektif kompleks. Objek semacam ini juga disebut *permukaan
Riemann*.

Untuk kurva bidang mulus

$$
C=V_+(F)\subset\mathbb P_K^2
$$

berderajat $d=\deg(F)$, genusnya adalah

$$
g=\frac{(d-1)(d-2)}{2}.
$$

Kurva bidang proyektif mulus berderajat satu atau dua, yakni garis dan
kuadrik, mempunyai genus $0$ dan isomorfik dengan garis proyektif. Untuk
$d=3$ diperoleh genus $1$, yakni kurva eliptik dalam konvensi sumber,
sedangkan untuk $d=4$ diperoleh genus $3$. Jadi, tidak setiap genus dapat
direalisasikan oleh kurva bidang mulus. Sebagai contoh, sama sekali tidak
mudah memberikan persamaan eksplisit untuk kurva genus $2$.
