---
title: "Kuliah 27 - Ruang Proyektif"
stable_id: br-ak-2012-l27
language: id-ID
source_author: "Holger Brenner"
frozen_revision_contributor: "Arbota"
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 27"
upstream_pageid: 50733
upstream_revid: 1052572
upstream_timestamp: "2025-08-27T14:01:03Z"
upstream_mediawiki_sha1: 9a396f3a601f0a0a0606657550a30b9a601da2f6
source_url: "https://de.wikiversity.org/w/index.php?oldid=1052572"
authority_manifest: authority/wikiversity/unit-27/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 98f9ebcc0d3b41bb0b955c5190d416b9ebfc07433015732faaf7f38366a1d9b2
lecture_xml: authority/wikiversity/unit-27/lecture-27.xml
lecture_xml_sha256: 9e1a4f687ca1faf008e9864460dc036f7849e2a3203f7d30dd509c7876b69ea6
lecture_expanded_tex: authority/wikiversity/unit-27/lecture-27-expanded.tex
lecture_expanded_tex_sha256: 2b75b62d96c149f8344de2060fcbc96a4d2061140dd6c509b2b11ad2e95dc8b4
license: "Current semantic course text and this translation: CC BY-SA 4.0. Unit 27 reader media retain their component-specific licenses and public-domain status as recorded in authority/RIGHTS-unit-27.csv. No blanket relicensing claim is made."
source_component_license_route: "Semantic-site rights notice: CC BY-SA 4.0; media component rights remain item-specific; official-PDF notices remain component-specific; no blanket relicensing claim."
license_evidence: "authority/UNIT_27_AUTHORITY_FREEZE.md; authority/RIGHTS-unit-27.csv; authority/ASSET_CLOSURE-unit-27.json"
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_semantic_entities: 21
source_corrections: 7
correction_ids: "AGC-CORR-0108; AGC-CORR-0109; AGC-CORR-0110; AGC-CORR-0111; AGC-CORR-0112; AGC-CORR-0113; AGC-CORR-0114"
reader_media_positions: 10
---

# Kuliah 27: Ruang Proyektif {#br-ak-2012-l27}

## Ruang proyektif {#br-ak-2012-l27-s01}

![Bunga dandelion dengan banyak garis dan tangkai yang memancar dari satu pusat](authority/assets/Loewenzahn_20.jpg)

*Garis-garis melalui satu titik. Waugsberg, CC BY-SA 2.5; berkas lokal:
`authority/assets/Loewenzahn_20.jpg`.*

<!-- upstream_entity: Projektiver Raum/Geradenmenge/Tafelbilder/Einführung/Textabschnitt -->

<!-- upstream_entity: Der projektive Raum/Als Geradenmenge/Homogene Koordinaten/Ohne Topologie/Definition -->

### Definisi 27.1: ruang proyektif {#br-ak-2012-l27-def-01}

Misalkan $K$ suatu lapangan. *Ruang proyektif berdimensi $n$*

$$
\mathbb P_K^n
$$

terdiri atas semua garis dalam ruang afin $\mathbb A_K^{n+1}$ yang melalui
titik asal, dengan setiap garis tersebut dipandang sebagai satu titik. Titik
proyektif seperti itu direpresentasikan oleh *koordinat homogen*

$$
(a_0,a_1,\ldots,a_n),
$$

dengan tidak semua $a_i$ sama dengan nol. Dua tupel koordinat tersebut
merepresentasikan titik yang sama tepat ketika yang satu diperoleh dari yang
lain melalui perkalian dengan suatu skalar

$$
\lambda\in K^\times.
$$

Secara bertahap kita akan melengkapi ruang proyektif dengan struktur-struktur
tambahan.

<!-- upstream_entity: Der projektive Raum/Offene Standardüberdeckung mit affinen Räumen/Fakt -->

### Teorema 27.2: penutup terbuka standar oleh ruang afin {#br-ak-2012-l27-thm-01}

Misalkan $K$ suatu lapangan, $\mathbb P_K^n$ suatu ruang proyektif, dan

$$
i\in\{0,1,\ldots,n\}.
$$

Dengan mengindeks koordinat sumber oleh semua $j\ne i$, terdapat pemetaan
alami

$$
\begin{aligned}
\varphi_i:\mathbb A_K^n&\longrightarrow\mathbb P_K^n,\\
(u_0,\ldots,\widehat{u_i},\ldots,u_n)
&\longmapsto
[u_0:\cdots:u_{i-1}:1:u_{i+1}:\cdots:u_n].
\end{aligned}
$$

Pemetaan ini injektif dan menginduksi bijeksi dengan himpunan titik
proyektif yang koordinat homogen ke-$i$-nya tidak nol, yaitu

$$
D_+(X_i)
:=
\{[x_0:\cdots:x_n]\in\mathbb P_K^n\mid x_i\ne0\}.
$$

Pemetaan baliknya diberikan oleh

$$
[x_0:\cdots:x_n]
\longmapsto
\left(
\frac{x_0}{x_i},\ldots,
\frac{x_{i-1}}{x_i},
\frac{x_{i+1}}{x_i},\ldots,
\frac{x_n}{x_i}
\right).
$$

Ruang proyektif ditutupi oleh $n+1$ ruang afin tersebut. Komplemen bagan
afin

$$
\mathbb A_K^n\cong D_+(X_i)\subseteq\mathbb P_K^n
$$

adalah ruang proyektif berdimensi $n-1$.

> **Catatan edisi - indeks penyisipan bagan.** Sumber menulis koordinat
> sumber sebagai $(u_1,\ldots,u_n)$ lalu menyisipkan $1$ "pada posisi $i$"
> untuk $i\in\{0,\ldots,n\}$. Notasi itu ambigu pada batas indeks dan tidak
> menampilkan koordinat $u_0$. Edisi mengindeks koordinat oleh
> $\{0,\ldots,n\}\setminus\{i\}$ dan memakai tanda topi untuk koordinat yang
> dihilangkan.

<!-- upstream_entity: Der projektive Raum/Offene Standardüberdeckung mit affinen Räumen/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l27-thm-01-proof}

Pemetaan tersebut terdefinisi dengan baik karena koordinat $1$ memastikan
bahwa sekurang-kurangnya satu koordinat homogen tidak nol. Jika

$$
[u_0:\cdots:u_{i-1}:1:u_{i+1}:\cdots:u_n]
=
[v_0:\cdots:v_{i-1}:1:v_{i+1}:\cdots:v_n],
$$

maka terdapat $\lambda\in K^\times$ yang mengalikan semua koordinat di ruas
kanan. Perbandingan koordinat ke-$i$ memberikan $1=\lambda$, sehingga semua
koordinat lainnya sama dan pemetaan itu injektif.

Pada $D_+(X_i)$, setiap titik mempunyai tepat satu wakil dengan koordinat
ke-$i$ sama dengan $1$, yang diperoleh dengan membagi semua koordinat oleh
$x_i$. Hal ini membuktikan rumus pemetaan balik. Setiap titik proyektif
mempunyai sekurang-kurangnya satu koordinat tak nol, sehingga bagan-bagan
$D_+(X_i)$ menutupi $\mathbb P_K^n$.

Komplemen $D_+(X_i)$ ialah

$$
V_+(X_i)
=
\{[x_0:\cdots:x_{i-1}:0:x_{i+1}:\cdots:x_n]
\mid \text{sekurang-kurangnya satu }x_j\ne0\}.
$$

Setelah tetap mengidentifikasi tupel yang berbeda dengan suatu faktor skalar,
himpunan ini adalah $\mathbb P_K^{n-1}$. $\square$

![Diagram pertama dari tiga ilustrasi bagan afin pada garis proyektif](authority/assets/Projektiveline1bb.jpg)

*Ilustrasi garis proyektif, bagian 1. Darapti, CC BY-SA 3.0; berkas lokal:
`authority/assets/Projektiveline1bb.jpg`.*

![Diagram kedua dari tiga ilustrasi bagan afin pada garis proyektif](authority/assets/Projektiveline2bb.jpg)

*Ilustrasi garis proyektif, bagian 2. Darapti, CC BY-SA 3.0; berkas lokal:
`authority/assets/Projektiveline2bb.jpg`.*

![Diagram ketiga dari tiga ilustrasi bagan afin pada garis proyektif](authority/assets/Projektiveline3bb.jpg)

*Ilustrasi garis proyektif, bagian 3. Darapti, CC BY-SA 3.0; berkas lokal:
`authority/assets/Projektiveline3bb.jpg`.*

<!-- upstream_entity: Die projektive Gerade/Einführende Beschreibung/Beispiel -->

### Contoh 27.3: garis proyektif {#br-ak-2012-l27-ex-01}

Garis proyektif $\mathbb P_K^1$ adalah himpunan garis-garis melalui titik asal
di bidang afin $\mathbb A_K^2$. Garis seperti itu adalah sumbu $x$, atau
memotong garis

$$
V(y-1)
$$

tepat di satu titik. Garis $V(y-1)$ sejajar dengan sumbu $x$ dan melalui
$(0,1)$. Sebaliknya, setiap titik

$$
P\in V(y-1)\cong\mathbb A_K^1
$$

menentukan secara tunggal sebuah garis melalui titik asal. Jadi garis
proyektif terdiri atas sebuah garis afin beserta satu titik tambahan, yang
disebut titik "di tak hingga".

Titik tersebut tidak berbeda secara hakiki dari titik proyektif lainnya.
Ambil sembarang garis $G$ melalui titik asal dan suatu garis $L\ne G$ yang
sejajar dengannya. Garis $L$ dapat mengambil peran sebagai garis afin,
sedangkan $G$ merepresentasikan titik di tak hingga jika dilihat dari bagan
afin tersebut.

![Diagram pertama dari empat ilustrasi bagan afin dan titik-titik di tak hingga pada bidang proyektif](authority/assets/Projektiveplane1bb.jpg)

*Ilustrasi bidang proyektif, bagian 1. Darapti, CC BY-SA 3.0; berkas lokal:
`authority/assets/Projektiveplane1bb.jpg`.*

![Diagram kedua dari empat ilustrasi bagan afin dan titik-titik di tak hingga pada bidang proyektif](authority/assets/Projektiveplane2bb.jpg)

*Ilustrasi bidang proyektif, bagian 2. Darapti, CC BY-SA 3.0; berkas lokal:
`authority/assets/Projektiveplane2bb.jpg`.*

![Diagram ketiga dari empat ilustrasi bagan afin dan titik-titik di tak hingga pada bidang proyektif](authority/assets/Projektiveplane3bb.jpg)

*Ilustrasi bidang proyektif, bagian 3. Darapti, CC BY-SA 3.0; berkas lokal:
`authority/assets/Projektiveplane3bb.jpg`.*

![Diagram keempat dari empat ilustrasi bagan afin dan titik-titik di tak hingga pada bidang proyektif](authority/assets/Projektiveplane4bb.jpg)

*Ilustrasi bidang proyektif, bagian 4. Darapti, CC BY-SA 3.0; berkas lokal:
`authority/assets/Projektiveplane4bb.jpg`.*

<!-- upstream_entity: Die projektive Ebene/Einführende Beschreibung/Beispiel -->

### Contoh 27.4: bidang proyektif {#br-ak-2012-l27-ex-02}

Titik-titik di bidang proyektif $\mathbb P_K^2$ bersesuaian dengan garis-garis
melalui titik asal di ruang afin $\mathbb A_K^3$. Setiap titik bidang
proyektif direpresentasikan oleh suatu tupel

$$
(x,y,z),
$$

dengan $x,y,z$ tidak semuanya nol. Dua tupel diidentifikasi jika yang satu
diperoleh dari yang lain melalui perkalian dengan suatu skalar tak nol.
Bidang proyektif ditutupi oleh tiga bidang afin

$$
D_+(X),\qquad D_+(Y),\qquad D_+(Z).
$$

Bagan $D_+(Z)$ terdiri atas semua titik dengan koordinat ketiga tidak nol.
Dengan mengalikan koordinat dengan $z^{-1}$, titik tersebut mempunyai wakil

$$
\left(\frac{x}{z},\frac{y}{z},\frac{z}{z}\right)
=(u,v,1),
$$

sehingga bagan itu benar-benar sebuah bidang afin. Komplemennya ialah
$V_+(Z)$, yaitu titik-titik dengan koordinat ketiga nol. Setelah identifikasi
skalar tetap diberlakukan, $V_+(Z)$ merupakan sebuah garis proyektif.

Sebuah titik $(x,y,0)$ pada garis itu, bersama titik asal $(0,0,1)$ pada
$D_+(Z)$, menentukan arah $(x,y)$ dari sebuah garis melalui titik asal di
bidang afin. Persamaan homogen garis tersebut adalah

$$
yX-xY=0,
$$

atau $V_+(yX-xY)$. Karena itu, bidang proyektif dapat dibayangkan sebagai
bidang afin yang dilengkapi dengan satu titik tambahan di tak hingga untuk
setiap arah garis melalui titik asal.

![Diagram perspektif dengan sinar-sinar proyeksi yang menghubungkan objek, pusat proyeksi, dan bidang gambar](authority/assets/Perspective_Projection_Principle.jpg)

*Prinsip proyeksi perspektif. Fantagu, CC BY-SA 3.0; berkas lokal:
`authority/assets/Perspective_Projection_Principle.jpg`.*

## Titik nol polinom homogen {#br-ak-2012-l27-s02}

<!-- upstream_entity: Homogene Polynome/Projektive Nullstellengebilde/Zariski-Topologie/Einführung/Textabschnitt -->

Untuk polinom sembarang

$$
F\in K[X_0,\ldots,X_n],
$$

pernyataan bahwa suatu titik $P\in\mathbb P_K^n$ adalah titik nol $F$ pada
umumnya tidak terdefinisi dengan baik. Nilai itu dapat berubah ketika wakil
koordinat $P$ dikalikan dengan skalar. Untuk polinom homogen, keadaan ini
berbeda.

<!-- upstream_entity: Der projektive Raum/Homogenes Polynom/Nullsein ist wohldefiniert/Fakt -->

### Lema 27.5: lenyapnya polinom homogen terdefinisi dengan baik {#br-ak-2012-l27-lem-01}

Misalkan $K$ suatu lapangan dan

$$
F\in K[X_0,\ldots,X_n]
$$

suatu polinom homogen berderajat $d$. Untuk setiap
$(x_0,\ldots,x_n)\in K^{n+1}$ dan $\lambda\in K$ berlaku

$$
F(\lambda x_0,\ldots,\lambda x_n)
=
\lambda^d F(x_0,\ldots,x_n).
$$

Khususnya, $F$ lenyap pada $(x_0,\ldots,x_n)$ jika dan hanya jika ia lenyap
pada $\lambda(x_0,\ldots,x_n)$ untuk setiap $\lambda\ne0$.

<!-- upstream_entity: Der projektive Raum/Homogenes Polynom/Nullsein ist wohldefiniert/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l27-lem-01-proof}

Cukup periksa setiap monom homogen. Untuk

$$
X_0^{d_0}\cdots X_n^{d_n},
\qquad
\sum_{i=0}^{n}d_i=d,
$$

kita memperoleh

$$
\begin{aligned}
(\lambda X_0)^{d_0}\cdots(\lambda X_n)^{d_n}
&=(\lambda^{d_0}X_0^{d_0})\cdots
  (\lambda^{d_n}X_n^{d_n})\\
&=\lambda^d X_0^{d_0}\cdots X_n^{d_n}.
\end{aligned}
$$

Linearitas kemudian memberikan pernyataan untuk $F$. $\square$

Lema tersebut membuat sifat "lenyap atau tidak" terdefinisi dengan baik pada
titik proyektif. Namun, nilai numerik sebuah polinom homogen pada titik
proyektif tetap tidak terdefinisi secara intrinsik. Polinom homogen bukanlah
fungsi pada ruang proyektif.

<!-- upstream_entity: Der projektive Raum/Nullstellengebilde zu einem homogenen Polynom/Definition -->

### Definisi 27.6: himpunan titik nol proyektif {#br-ak-2012-l27-def-02}

Misalkan $K$ suatu lapangan dan

$$
F\in K[X_0,\ldots,X_n]
$$

suatu polinom homogen. Himpunan

$$
V_+(F)
=
\{P=[x_0:\cdots:x_n]\in\mathbb P_K^n
\mid F(x_0,\ldots,x_n)=0\}
$$

disebut *himpunan titik nol proyektif* dari $F$.

Untuk menentukan $V_+(F)$, kita dapat memakai dekomposisi disjung

$$
\mathbb P_K^n=D_+(X_0)\mathbin{\uplus}V_+(X_0),
$$

dan demikian pula untuk setiap variabel lain. Pada bagan
$D_+(X_0)\cong\mathbb A_K^n$, kita menetapkan $X_0=1$ dan menyelesaikan

$$
F(1,X_1,\ldots,X_n)=0.
$$

Polinom tersebut mungkin menjadi takhomogen, satu variabel dieliminasi, dan
dimensi lingkungan tetap sama, tetapi persoalannya menjadi afin. Pada
$V_+(X_0)\cong\mathbb P_K^{n-1}$, kita menetapkan $X_0=0$ dan menyelesaikan

$$
F(0,X_1,\ldots,X_n)=0.
$$

Di sini satu variabel kembali dieliminasi, polinom tetap homogen, dan
dimensi ruang proyektif berkurang satu.

> **Catatan edisi - dehomogenisasi.** Sumber menampilkan ekspresi cacat
> $F\{1/X_0\}$ dan $F\{0/X_0\}$. Uraian tepat sebelum kedua ekspresi itu
> menyatakan substitusi $X_0=1$ dan $X_0=0$. Edisi menuliskan polinom yang
> dimaksud secara eksplisit sebagai $F(1,X_1,\ldots,X_n)$ dan
> $F(0,X_1,\ldots,X_n)$.

<!-- upstream_entity: Der Projektive Raum/Homogenes lineares Polynom/Nullstellenmenge/Beispiel -->

### Contoh 27.7: polinom linear homogen {#br-ak-2012-l27-ex-03}

Polinom homogen yang paling sederhana dalam $K[X_0,\ldots,X_n]$ ialah
polinom berderajat satu,

$$
F=a_0X_0+a_1X_1+\cdots+a_nX_n,
$$

dengan koefisien-koefisien yang tidak semuanya nol. Himpunan titik nol afin
$V(F)$ di $\mathbb A_K^{n+1}$ adalah ruang afin berdimensi $n$ yang melalui
titik asal. Himpunan titik nol proyektif $V_+(F)$ di $\mathbb P_K^n$
isomorfik dengan ruang proyektif berdimensi $n-1$.

> **Catatan edisi - indeks suku linear.** Sumber menulis
> $a_0X_0+a_1X_0+\cdots+a_nX_n$. Suku kedua harus memakai $X_1$ agar bentuk
> itu merupakan bentuk linear umum dalam variabel $X_0,\ldots,X_n$.

<!-- upstream_entity: Polynomring/Homogenes Ideal/Definition -->

### Definisi 27.8: ideal homogen {#br-ak-2012-l27-def-03}

Misalkan $K$ suatu lapangan dan

$$
\mathfrak a\subseteq K[X_1,\ldots,X_n]
$$

suatu ideal. Ideal $\mathfrak a$ disebut *homogen* jika, untuk setiap
$H\in\mathfrak a$ dengan dekomposisi homogen

$$
H=\sum_i H_i,
$$

setiap komponen homogen $H_i$ juga berada dalam $\mathfrak a$.

<!-- upstream_entity: Der projektive Raum/Nullstellengebilde zu einem homogenen Ideal/Definition -->

### Definisi 27.9: varietas proyektif {#br-ak-2012-l27-def-04}

Untuk suatu ideal homogen

$$
\mathfrak a\subseteq K[X_0,\ldots,X_n],
$$

himpunan

$$
V_+(\mathfrak a)
=
\{P\in\mathbb P_K^n
\mid F(P)=0\text{ untuk setiap }F\in\mathfrak a
   \text{ yang homogen}\}
$$

disebut *himpunan titik nol proyektif* atau *varietas proyektif* dari
$\mathfrak a$.

<!-- upstream_entity: Der projektive Raum/Mit Zariski-Topologie/Definition -->

### Definisi 27.10: topologi Zariski pada ruang proyektif {#br-ak-2012-l27-def-05}

Ruang proyektif $\mathbb P_K^n$ dilengkapi dengan *topologi Zariski* dengan
menetapkan himpunan

$$
V_+(\mathfrak a)\subseteq\mathbb P_K^n,
$$

untuk setiap ideal homogen

$$
\mathfrak a\subseteq K[X_0,\ldots,X_n],
$$

sebagai himpunan-himpunan tertutup.

Dengan demikian, himpunan terbuka ruang proyektif berbentuk

$$
D_+(\mathfrak a)
:=
\mathbb P_K^n\setminus V_+(\mathfrak a).
$$

Khususnya, setiap himpunan terbuka standar $D_+(X_i)$ isomorfik dengan ruang
afin berdimensi $n$.

<!-- upstream_entity: Der projektive Raum/Punkt ist abgeschlossen/Beschreibung/Bemerkung -->

### Catatan 27.11: titik proyektif bersifat tertutup {#br-ak-2012-l27-rem-01}

Misalkan

$$
P=[a_0:\cdots:a_n]\in\mathbb P_K^n.
$$

Titik $P$ tertutup. Lebih tepatnya,

$$
P=V_+(\mathfrak a_P),
\qquad
\mathfrak a_P
=
(a_iX_j-a_jX_i\mid 0\leq i,j\leq n).
$$

Jika $a_0\ne0$, ideal itu juga dapat ditulis sebagai

$$
\mathfrak a_P
=
\left(X_j-\frac{a_j}{a_0}X_0\ \middle|\ j\ne0\right);
$$

pembangun $a_iX_j-a_jX_i$ dengan $i\ne0$ kemudian berlebihan. Ideal ini
jelas homogen dan $P\in V_+(\mathfrak a_P)$. Jika

$$
Q=[b_0:\cdots:b_n]\in V_+(\mathfrak a_P),
$$

maka, karena $a_0\ne0$,

$$
b_j-\frac{a_j}{a_0}b_0=0
$$

untuk setiap $j$. Oleh karena itu,

$$
(b_0,\ldots,b_n)
=
\frac{b_0}{a_0}(a_0,\ldots,a_n),
$$

sehingga $Q=P$ sebagai titik proyektif.

Ideal $\mathfrak a_P$ bukan ideal maksimal dalam gelanggang polinom. Ia
merupakan ideal prima homogen: hasil bagi terhadapnya isomorfik dengan
gelanggang polinom satu variabel. Di $\mathbb A_K^{n+1}$, ideal tersebut
mendefinisikan garis melalui titik asal yang bersesuaian dengan titik
proyektif $P$.

> **Catatan edisi - klaim maksimalitas.** Sumber menyatakan bahwa
> $\mathfrak a_P$ maksimal di antara semua ideal homogen selain ideal
> irelevan $(X_0,\ldots,X_n)$. Klaim itu salah tanpa syarat tambahan. Sebagai
> contoh, setelah memilih $a_0\ne0$, ideal homogen
> $\mathfrak a_P+(X_0^2)$ berada secara ketat di antara $\mathfrak a_P$ dan
> ideal irelevan. Edisi mempertahankan pernyataan yang benar dan diperlukan:
> $\mathfrak a_P$ adalah ideal prima homogen dan mendefinisikan tepat titik
> proyektif $P$.

Tidak ada pemetaan alami dari seluruh $\mathbb A_K^{n+1}$ ke
$\mathbb P_K^n$, sebab titik asal tidak menentukan sebuah garis. Namun,
terdapat pemetaan alami

$$
\begin{aligned}
\mathbb A_K^{n+1}\setminus\{0\}&\longrightarrow\mathbb P_K^n,\\
(x_0,\ldots,x_n)&\longmapsto[x_0:\cdots:x_n].
\end{aligned}
$$

Pemetaan ini mengirimkan titik tak nol ke garis melalui titik itu dan titik
asal. Pemetaan tersebut disebut *pemetaan kanonik* atau *pemetaan kerucut*.
Prapeta $D_+(X_i)$ di bawah pemetaan ini ialah $D(X_i)$.

## Ruang proyektif di atas $\mathbb R$ dan $\mathbb C$ {#br-ak-2012-l27-s03}

Kita sekarang membangun gambaran topologis ruang proyektif untuk
$\mathbb K=\mathbb R$ dan $\mathbb K=\mathbb C$. Sfera real berdimensi $n$
adalah

$$
S^n
=
\{x\in\mathbb R^{n+1}\mid\lVert x\rVert=1\},
$$

dengan

$$
\lVert x\rVert=\sqrt{x_0^2+\cdots+x_n^2}
$$

norma Euklides.

<!-- upstream_entity: Projektiver Raum/R oder C/Repräsentiert durch Sphäre/Fakt -->

### Teorema 27.12: representasi oleh sfera {#br-ak-2012-l27-thm-02}

Ruang proyektif real $\mathbb P_{\mathbb R}^n$ dapat direpresentasikan oleh
sfera $S^n\subseteq\mathbb R^{n+1}$ modulo relasi ekuivalensi yang
mengidentifikasi setiap pasangan titik antipodal.

Ruang proyektif kompleks $\mathbb P_{\mathbb C}^n$ dapat direpresentasikan
oleh sfera

$$
S^{2n+1}\subseteq\mathbb R^{2n+2}\cong\mathbb C^{n+1}
$$

modulo relasi ekuivalensi yang mengidentifikasi $z,w\in S^{2n+1}$ jika

$$
z=\lambda w
$$

untuk suatu $\lambda\in S^1\subseteq\mathbb C$.

<!-- upstream_entity: Projektiver Raum/R oder C/Repräsentiert durch Sphäre/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l27-thm-02-proof}

Kita menangani kasus real dan kompleks secara bersamaan. Setiap titik pada
sfera $S$ menentukan suatu garis real atau kompleks melalui titik asal di
ruang ambien, sehingga menentukan sebuah titik proyektif. Dua titik
$z,w\in S$ menentukan garis yang sama tepat ketika

$$
z=\lambda w
$$

untuk suatu $\lambda\in\mathbb K$. Multiplikativitas norma memberikan

$$
\lVert z\rVert=|\lambda|\lVert w\rVert.
$$

Karena kedua norma sama dengan satu, $|\lambda|=1$. Dalam kasus real, ini
berarti $\lambda=\pm1$, sehingga titik-titik yang diidentifikasi adalah
pasangan antipodal. Dalam kasus kompleks, ini berarti
$\lambda\in S^1\subseteq\mathbb C$. $\square$

Secara keseluruhan terdapat pemetaan surjektif

$$
S^n\subseteq\mathbb R^{n+1}\setminus\{0\}
\longrightarrow\mathbb P_{\mathbb R}^n
$$

dalam kasus real, serta

$$
S^{2n+1}\subseteq\mathbb R^{2n+2}\setminus\{0\}
\cong\mathbb C^{n+1}\setminus\{0\}
\longrightarrow\mathbb P_{\mathbb C}^n
$$

dalam kasus kompleks. Ruang proyektif real dan kompleks dilengkapi dengan
topologi hasil bagi dari topologi metrik ruang vektor real tersebut. Jadi,
$U\subseteq\mathbb P_{\mathbb K}^n$ dinyatakan terbuka jika prapetanya di
$\mathbb A_{\mathbb K}^{n+1}\setminus\{0\}$ terbuka. Hal ini ekuivalen
dengan keterbukaan prapetanya pada sfera yang bersesuaian. Dengan topologi
metrik atau topologi alami ini, pemetaan-pemetaan di atas kontinu.

<!-- upstream_entity: Projektiver Raum/R oder C/Offen überdeckt und Mannigfaltigkeit/Fakt -->

### Lema 27.13: bagan terbuka dan struktur manifold {#br-ak-2012-l27-lem-02}

Untuk ruang proyektif real dan kompleks, himpunan $D_+(X_i)$ terbuka dalam
topologi alami dan homeomorfik, masing-masing, dengan $\mathbb R^n$ atau
$\mathbb C^n$. Khususnya, ruang proyektif real dan kompleks merupakan
manifold topologis.

<!-- upstream_entity: Projektiver Raum/R oder C/Offen überdeckt und Mannigfaltigkeit/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l27-lem-02-proof}

Prapeta $D_+(X_i)$ di bawah pemetaan kanonik

$$
\mathbb A_{\mathbb K}^{n+1}\setminus\{0\}
\longrightarrow\mathbb P_{\mathbb K}^n
$$

ialah $D(X_i)$, komplemen suatu subruang vektor berdimensi $n$, sehingga
terbuka dalam topologi alami. Tinjau pemetaan kontinu

$$
\mathbb K^n
\cong V(X_i-1)
\subset D(X_i)
\longrightarrow D_+(X_i).
$$

Pemetaan ini bijektif. Untuk menunjukkan bahwa ia homeomorfisme, cukup
menunjukkan bahwa ia terbuka. Misalkan

$$
U\subseteq V(X_i-1)\cong\mathbb K^n
$$

terbuka dan $U'$ citranya dalam $D_+(X_i)$. Prapeta $U'$ di $D(X_i)$ ialah
kerucut

$$
U''=\{\lambda P\mid \lambda\in\mathbb K^\times, P\in U\}.
$$

Pemetaan

$$
\begin{aligned}
\mathbb K^\times\times V(X_i-1)&\longrightarrow D(X_i),\\
(\lambda,P)&\longmapsto\lambda P
\end{aligned}
$$

adalah homeomorfisme, dengan pemetaan balik

$$
Q\longmapsto\left(Q_i,\frac{Q}{Q_i}\right).
$$

Karena itu,

$$
U''\cong\mathbb K^\times\times U
$$

terbuka dalam $D(X_i)$. Menurut definisi topologi hasil bagi, $U'$ terbuka.
Jadi bijeksi tersebut adalah homeomorfisme. $\square$

> **Catatan edisi - lingkungan dalam kerucut.** Sumber memilih sebuah bola
> terbuka $B$ di sekitar $P$, lalu menyatakan tanpa syarat bahwa kerucutnya
> termuat dalam $U''$. Agar kesimpulan itu benar, bola harus dipilih dengan
> $P\in B\subseteq U$. Edisi memberikan argumen global yang ekuivalen melalui
> homeomorfisme $\mathbb K^\times\times V(X_i-1)\cong D(X_i)$, yang sekaligus
> menutup celah tersebut.

![Sfera biru tiga dimensi yang merepresentasikan garis proyektif kompleks](authority/assets/Blue-sphere.png)

*Garis proyektif di atas $\mathbb C$ adalah sebuah sfera. Kieff, domain
publik; berkas lokal: `authority/assets/Blue-sphere.png`.*

<!-- upstream_entity: Projektiver Raum/R oder C/Kompakt/Fakt -->

### Korolari 27.14: kekompakan dan sifat Hausdorff {#br-ak-2012-l27-cor-01}

Dalam topologi alaminya, ruang proyektif real dan kompleks bersifat kompak
dan Hausdorff.

<!-- upstream_entity: Projektiver Raum/R oder C/Kompakt/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l27-cor-01-proof}

Untuk setiap ruang proyektif tersebut terdapat pemetaan kontinu surjektif
dari sfera yang bersesuaian. Sfera itu tertutup dan terbatas dalam ruang
vektor real berdimensi hingga, sehingga kompak menurut Teorema Heine-Borel.
Citra kontinu suatu ruang kompak bersifat kompak. Oleh karena itu, ruang
proyektif real dan kompleks bersifat kompak.

Sekarang ambil dua titik berbeda

$$
P,Q\in\mathbb P_{\mathbb K}^n,
\qquad
\mathbb K\in\{\mathbb R,\mathbb C\}.
$$

Karena $\mathbb K$ tak hingga, terdapat bentuk linear homogen $L$ yang tidak
lenyap pada $P$ maupun $Q$. Memang, di ruang dual, bentuk-bentuk yang lenyap
pada $P$ dan yang lenyap pada $Q$ masing-masing membentuk hiperbidang sejati,
dan gabungan dua hiperbidang tersebut tidak memenuhi seluruh ruang dual.

Dengan suatu perubahan koordinat linear, $L$ dapat dijadikan salah satu
koordinat homogen. Maka

$$
P,Q\in D_+(L)\cong\mathbb K^n.
$$

Menurut Lema 27.13, bagan ini homeomorfik dengan ruang Euklides real atau
kompleks dan karena itu Hausdorff. Jadi terdapat lingkungan terbuka yang
saling lepas bagi $P$ dan $Q$. Dengan demikian seluruh ruang proyektif
bersifat Hausdorff. $\square$

> **Catatan edisi - dua titik dalam satu bagan.** Sumber mengandaikan bahwa
> dua titik proyektif sembarang terletak bersama-sama dalam salah satu bagan
> standar $D_+(X_i)$. Hal itu salah, misalnya bagi $[1:0]$ dan $[0:1]$ dalam
> $\mathbb P^1$. Edisi memilih bentuk linear $L$ yang tidak lenyap pada kedua
> titik, lalu memakai perubahan koordinat untuk memperoleh bagan afin
> $D_+(L)$ yang memuat keduanya.

> **Catatan edisi - rujukan yang terputus.** Pada bagian kekompakan, sumber
> merujuk ke "Fakt *****". Edisi mengganti penanda yang terputus itu dengan
> pernyataan standar yang benar-benar digunakan: citra kontinu ruang kompak
> bersifat kompak.
