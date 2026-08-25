---
title: "Kuliah 22 - Dimensi Penyematan serta Titik Mulus dan Singular"
stable_id: br-ak-2025-2026-l22
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 22"
upstream_pageid: 165911
upstream_revid: 1051397
upstream_timestamp: "2025-08-18T08:21:20Z"
upstream_mediawiki_sha1: 907644dc696a39dc2462e100fe3dd1f8a452fd8a
source_url: "https://de.wikiversity.org/w/index.php?oldid=1051397"
authority_manifest: authority/wikiversity/unit-22/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: fefb7f6221a3e71b94649f03c75693f9eb34ec228cedf0af7d9e332aeda7d38a
lecture_xml_sha256: dd79b2c081285203f10fd0eaa0b612d39f6a3ea945a5afb1c9cf5243dd4f588f
lecture_expanded_tex_sha256: ba8f39ddc1cd90388fe9962dd6aabff5aa1b9e37432362e69676b383fe337130
license: "CC BY-SA 4.0 for translated course text; reader media retain component-specific rights: Tangent_to_a_curve.svg, 3 equations -5.JPG, and the René Descartes portrait are public domain; Kartesisches-Blatt.svg and Intersect3.png are CC BY-SA 3.0; see authority/RIGHTS-unit-22.csv"
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_semantic_entities: 20
edition_bridges: 1
source_corrections: 1
source_credit_notes: 1
reader_media_positions: 5
---

# Kuliah 22: Dimensi Penyematan serta Titik Mulus dan Singular {#br-ak-2025-2026-l22}

## Dimensi penyematan {#br-ak-2025-2026-l22-s01}

<!-- upstream_entity: Lokale kommutative noethersche Ringe/Minimale Erzeugendenzahl des maximalen Ideals/Definition -->

### Definisi: dimensi penyematan {#br-ak-2025-2026-l22-def-01}

Misalkan $R$ suatu gelanggang komutatif lokal dan Noether dengan ideal
maksimal $\mathfrak m$. Banyaknya unsur dalam suatu sistem pembangkit minimal
bagi ideal $\mathfrak m$ disebut *dimensi penyematan* $R$, dan ditulis

$$
\operatorname{embdim}(R).
$$

<!-- upstream_entity: Einbettungsdimension/Numerische Situation/Einführung/Textabschnitt -->

Suatu domain integral lokal Noether berdimensi satu—artinya, satu-satunya
ideal primanya ialah ideal nol dan ideal maksimal—merupakan gelanggang
valuasi diskret jika dan hanya jika dimensi penyematannya $1$, menurut
Teorema 21.8. Dimensi penyematan selalu paling sedikit sebesar dimensi suatu
gelanggang lokal. Gelanggang-gelanggang yang mencapai kesamaan memainkan
peranan khusus dan disebut *gelanggang reguler*. Kita telah menjumpai dimensi
penyematan dalam kasus kurva monomial dan harus menunjukkan bahwa definisi di
sana (Definisi 18.6) selaras dengan definisi yang baru ini.

Pertama-tama kita buktikan karakterisasi lain yang merupakan akibat Lema
Nakayama.

<!-- upstream_entity: Lokaler Ring/Modulerzeuger und Erzeuger mod m/Fakt -->

### Lema: pembangkit modul dan pembangkit modulo $\mathfrak m$ {#br-ak-2025-2026-l22-lem-01}

Misalkan $(R,\mathfrak m,K)$ suatu gelanggang lokal dan $V$ suatu modul-$R$
yang dibangkitkan secara hingga. Maka banyak pembangkit minimal

$$
\mu(V)
$$

sama dengan dimensi ruang vektor-$K$

$$
V/\mathfrak mV.
$$

<!-- upstream_entity: Lokaler Ring/Modulerzeuger und Erzeuger mod m/Fakt/Beweis -->

#### Bukti {#br-ak-2025-2026-l22-lem-01-proof}

Kita buktikan pernyataan yang sedikit lebih umum: unsur-unsur

$$
v_1,\ldots,v_n\in V
$$

membentuk sistem pembangkit-$R$ bagi $V$ jika dan hanya jika kelas-kelas
residunya di $V/\mathfrak mV$ membentuk sistem pembangkit atas
$R/\mathfrak m$. Salah satu arahnya langsung. Jadi misalkan
$v_1,\ldots,v_n\in V$ diberikan dan kelas-kelasnya modulo $\mathfrak m$
membentuk suatu sistem pembangkit. Misalkan

$$
U\subseteq V
$$

submodul-$R$ yang dibangkitkan oleh $v_i$. Hipotesis tersebut berarti

$$
V=U+\mathfrak mV.
$$

Tinjau modul faktor $V/U$. Di sana berlaku

$$
(V/U)\mathfrak m=V/U.
$$

Lema Nakayama memberikan

$$
V/U=0,
$$

dan karena itu

$$
V=U.
$$

<!-- upstream_entity: Lokaler Ring/Einbettungsdimension ist Dimension des Kotangentialraumes/Fakt -->

### Korolari: dimensi penyematan sebagai dimensi ruang kotangen {#br-ak-2025-2026-l22-cor-01}

Misalkan $(R,\mathfrak m,K)$ suatu gelanggang lokal dan Noether. Maka dimensi
penyematannya sama dengan

$$
\mu(\mathfrak m)
=
\dim_K\left(\mathfrak m/\mathfrak m^2\right).
$$

<!-- upstream_entity: Lokaler Ring/Einbettungsdimension ist Dimension des Kotangentialraumes/Fakt/Beweis -->

#### Bukti {#br-ak-2025-2026-l22-cor-01-proof}

Pernyataan ini langsung mengikuti Lema Nakayama yang diterapkan pada ideal
$\mathfrak m$ dan modul-$R$ yang dibangkitkan secara hingga $\mathfrak m$.

Modul-$R$

$$
\mathfrak m/\mathfrak m^2,
$$

yang muncul dalam pernyataan di atas dan merupakan ruang vektor atas
$R/\mathfrak m$, juga disebut *ruang kotangen* gelanggang lokal tersebut.

<!-- upstream_entity: Noetherscher Ring/Maximales Ideal/Kotangentialraum direkt und über lokalen Ring/Fakt -->

### Lema: ruang kotangen sebelum dan sesudah pelokalan {#br-ak-2025-2026-l22-lem-02}

Misalkan $R$ suatu gelanggang komutatif dan Noether serta $\mathfrak n$ suatu
ideal maksimal. Misalkan

$$
S=R_{\mathfrak n}
$$

pelokalan pada $\mathfrak n$, dengan ideal maksimal

$$
\mathfrak m=\mathfrak nR_{\mathfrak n}.
$$

Maka

$$
\mathfrak m/\mathfrak m^2
\cong
\mathfrak n/\mathfrak n^2.
$$

Secara khusus, dimensi penyematan pelokalan tersebut sama dengan

$$
\dim_{R/\mathfrak n}\left(\mathfrak n/\mathfrak n^2\right).
$$

<!-- upstream_entity: Noetherscher Ring/Maximales Ideal/Kotangentialraum direkt und über lokalen Ring/Fakt/Beweis -->

#### Bukti {#br-ak-2025-2026-l22-lem-02-proof}

Menurut Soal 15.5,

$$
R/\mathfrak n
\cong
R_{\mathfrak n}/\mathfrak m,
$$

sehingga lapangan residunya sama; tuliskan lapangan residu bersama ini sebagai
$K$. Homomorfisme modul-$R$ alami

$$
\mathfrak n\longrightarrow\mathfrak m
$$

menginduksi homomorfisme ruang vektor-$K$

$$
\mathfrak n/\mathfrak n^2
\longrightarrow
\mathfrak m/\mathfrak m^2.
$$

Pemetaan ini surjektif, sebab pembangkit modul-$R$ bagi $\mathfrak n$
dipetakan ke pembangkit modul-$R_{\mathfrak n}$ bagi $\mathfrak m$, dan
kelas-kelas pembangkit ini modulo $\mathfrak m^2$ membentuk sistem pembangkit
ruang vektor-$K$.

Untuk membuktikan injektivitas, ambil

$$
f\in\mathfrak n
$$

yang dipetakan ke $0$ di ruas kanan. Artinya,

$$
f\in\mathfrak m^2
$$

di dalam pelokalan $R_{\mathfrak n}$. Jadi terdapat unsur-unsur

$$
g_1,\ldots,g_n\in\mathfrak n,
\qquad
h_1,\ldots,h_n\in\mathfrak n,
$$

serta unsur-unsur

$$
q_i=\frac{a_i}{s_i}\in R_{\mathfrak n},
\qquad
s_i\notin\mathfrak n,
\qquad
a_i\in R,
$$

sedemikian sehingga

$$
f=\frac{a_1}{s_1}g_1h_1+\cdots+\frac{a_n}{s_n}g_nh_n.
$$

Jika diterjemahkan kembali ke $R$, ini berarti bahwa terdapat suatu

$$
s\notin\mathfrak n
$$

dengan

$$
sf=b_1g_1h_1+\cdots+b_ng_nh_n
$$

untuk beberapa $b_i\in R$. Karena $s$ tidak termasuk ideal maksimal
$\mathfrak n$, terdapat $r\in R$ dan $g\in\mathfrak n$ sehingga

$$
g+rs=1.
$$

Kalikan persamaan sebelumnya dengan $r$. Kita memperoleh

$$
(1-g)f
=
r\left(b_1g_1h_1+\cdots+b_ng_nh_n\right),
$$

atau, ekuivalen,

$$
f
=
r\left(b_1g_1h_1+\cdots+b_ng_nh_n\right)+gf.
$$

Ruas kanan jelas termasuk $\mathfrak n^2$. Jadi $f$ menentukan unsur nol di
$\mathfrak n/\mathfrak n^2$, dan injektivitas pun terbukti.

<!-- upstream_entity: Numerisches Monoid/Lokale kommutative noethersche Ringe/Numerische und algebraische Einbettungsdimension/Äquivalenz/Fakt -->

### Lema: kesamaan dimensi penyematan numerik dan aljabar {#br-ak-2025-2026-l22-lem-03}

Misalkan $K$ suatu lapangan dan $M$ suatu monoid numerik yang dibangkitkan
oleh bilangan-bilangan asli yang saling prima. Misalkan

$$
R=K[M]
$$

gelanggang monoid yang terkait, dengan ideal maksimal

$$
\mathfrak n=(M_+),
$$

dan misalkan $R_{\mathfrak n}$ pelokalannya. Maka dimensi penyematan numerik
$M$—atau $K[M]$—sama dengan dimensi penyematan gelanggang lokal
$R_{\mathfrak n}$.

<!-- upstream_entity: Numerisches Monoid/Lokale kommutative noethersche Ringe/Numerische und algebraische Einbettungsdimension/Äquivalenz/Fakt/Beweis -->

#### Bukti {#br-ak-2025-2026-l22-lem-03-proof}

Berlaku

$$
\mathfrak n
=(M_+)
=\bigoplus_{m\in M_+}K\,T^m
$$

dan

$$
\mathfrak n^2
=(2M_+)
=\bigoplus_{m\in2M_+}K\,T^m.
$$

Karena itu ruang residunya ialah

$$
\mathfrak n/\mathfrak n^2
=
\bigoplus_{m\in M_+\setminus2M_+}K\,T^m.
$$

Dimensi-$K$ ruang ini sama dengan banyaknya unsur
$M_+\setminus2M_+$. Menurut Korolari 18.13, himpunan
$M_+\setminus2M_+$ merupakan sistem pembangkit monoid minimal $M$. Jadi
dimensi-$K$ tersebut sama dengan dimensi penyematan numerik.

Di sisi lain, menurut Lema 22.4, dimensi-$K$
$\mathfrak n/\mathfrak n^2$ sama dengan dimensi penyematan gelanggang lokal
$R_{\mathfrak n}$ yang terkait.

## Titik mulus dan singular {#br-ak-2025-2026-l22-s02}

![Kurva hitam dengan sebuah titik merah dan garis singgung merah yang menyentuh kurva di titik tersebut](authority/assets/Tangent_to_a_curve.svg)

*Garis singgung pada sebuah kurva. Karya Jacj di Wikipedia bahasa Inggris;
versi-versi berikutnya diunggah oleh Oleg Alexandrov. Domain publik; berkas
lokal: `authority/assets/Tangent_to_a_curve.svg`.*

**Catatan edisi — kredit media.** Baris kredit sumber menamai AxelBoldt dan
CC BY-SA 3.0. Metadata Commons beku untuk berkas ini menyatakan domain publik
serta mencatat riwayat karya Jacj/Oleg Alexandrov; metadata Commons tersebut
mengatur kredit komponen pada edisi ini.

<!-- upstream_entity: Algebraische ebene Kurve/Multiplizität/Glatte und singuläre Punkte/Partielle Ableitungen/Kartesisches Blatt/Einführung/Textabschnitt -->

Misalkan $K$ suatu lapangan dan

$$
F\in K[X,Y],
\qquad
F\ne0,
$$

suatu polinom tanpa faktor berulang. Karena yang kita perhatikan hanya kurva
yang terkait, apabila lapangan itu tertutup secara aljabar, hipotesis ini
bukanlah pembatasan berkat Nullstellensatz Hilbert. Untuk setiap titik

$$
(a,b)\in\mathbb A_K^2,
$$

kita dapat beralih ke variabel $X-a$ dan $Y-b$. Artinya, titik tersebut
digeser ke titik asal. Karena itu, untuk mengkaji perilaku suatu polinom pada
sebuah titik, kita selalu dapat membatasi perhatian pada titik asal.

Misalkan sekarang

$$
P=(0,0).
$$

Tuliskan $F$ melalui komponen-komponen homogennya sebagai

$$
F=F_d+F_{d-1}+\cdots+F_1+F_0,
$$

dengan $F_i$ homogen berderajat $i$. Apa yang dapat dibaca dari masing-masing
komponen homogen itu? Pertama-tama, secara langsung berlaku

$$
P\in V(F)
\quad\Longleftrightarrow\quad
F_0=0.
$$

Jika koordinat $P$, yaitu $(0,0)$, disubstitusikan ke $F$, semua komponen
berderajat lebih tinggi menjadi $0$ dan hanya komponen konstan $F_0$ yang
tersisa. Karena kita terutama tertarik pada perilaku kurva di sebuah titik
kurva, kita akan sering membatasi perhatian pada situasi

$$
F_0=0.
$$

Komponen homogen $F_i$ manakah yang pertama kali tidak nol? Peranan apa yang
dimainkan indeks $i$ itu, dan peranan apa yang dimainkan faktor-faktor
linearnya?

Mula-mula andaikan

$$
F_0=0
\qquad\text{dan}\qquad
F_1=aX+bY.
$$

Bentuk linear ini, yang mungkin saja nol, juga dapat dicirikan dengan turunan
parsial:

$$
\frac{\partial F}{\partial X}(P)=a
\qquad\text{dan}\qquad
\frac{\partial F}{\partial Y}(P)=b.
$$

Di sini dan selanjutnya polinom diturunkan secara formal. Dengan demikian,

$$
F_1=0
\quad\Longleftrightarrow\quad
\frac{\partial F}{\partial X}(P)
=
\frac{\partial F}{\partial Y}(P)
=0.
$$

Jika hal ini tidak terjadi, wajar untuk memandang garis yang didefinisikan
oleh

$$
F_1(X,Y)=0
$$

sebagai garis singgung kurva di titik $P$. Petunjuk pertamanya ialah bahwa
dalam kasus linear

$$
F=F_1,
$$

garis tersebut seharusnya berimpit dengan garis singgungnya.

<!-- upstream_entity: Ebene algebraische Kurven/Punkt/Glatt mit partiellen Ableitungen/Definition -->

### Definisi: titik mulus dan titik singular {#br-ak-2025-2026-l22-def-02}

Misalkan $K$ suatu lapangan dan $F\in K[X,Y]$ suatu polinom tak nol. Misalkan

$$
P\in C=V(F)\subseteq\mathbb A_K^2
$$

suatu titik pada kurva bidang afin yang terkait. Titik $P$ disebut *titik
mulus* $C$ jika

$$
\frac{\partial F}{\partial X}(P)\ne0
\qquad\text{atau}\qquad
\frac{\partial F}{\partial Y}(P)\ne0.
$$

Jika tidak, titik tersebut disebut *singular*.

Kurva itu disebut *mulus* apabila mulus di setiap titiknya.

> **Jembatan edisi 22.A — lingkup istilah.** Kuliah ini bekerja dengan
> presentasi kurva bidang oleh polinom $F$ tanpa faktor berulang sebagaimana
> ditetapkan di atas, dan “mulus” dalam definisi ini berarti kriteria turunan
> formal yang baru saja dinyatakan untuk presentasi tersebut. Edisi tidak
> memperluas pernyataan itu menjadi identifikasi tanpa syarat dengan
> kemulusan skema di atas lapangan sembarang, khususnya lapangan tak sempurna.

<!-- upstream_entity: Ebene algebraische Kurven/Singularitäten/Multiplizität und Tangenten über kleinste homogene Komponente/Definition -->

### Definisi: multiplisitas dan garis singgung {#br-ak-2025-2026-l22-def-03}

Misalkan $K$ suatu lapangan tertutup secara aljabar dan $F\in K[X,Y]$ suatu
polinom tak nol. Misalkan

$$
P\in C=V(F)\subseteq\mathbb A_K^2
$$

suatu titik pada kurva bidang afin yang terkait dan, setelah perubahan
koordinat afin berupa translasi, anggap $P$ sebagai titik asal. Misalkan

$$
F=F_d+F_{d-1}+\cdots+F_m
$$

dekomposisi homogen $F$, dengan

$$
F_d\ne0,
\qquad
F_m\ne0,
\qquad
d\geq m.
$$

Bilangan $m$ disebut *multiplisitas* kurva di titik $P$. Misalkan

$$
F_m=G_1\cdots G_m
$$

dekomposisi menjadi faktor-faktor linear. Setiap garis

$$
V(G_i),
\qquad i=1,\ldots,m,
$$

disebut *garis singgung* pada $C$ di titik $P$. Banyaknya kemunculan $G_i$
di dalam $F_m$ juga disebut *multiplisitas* garis singgung tersebut.

**Catatan edisi — koreksi sumber.** Sumber menyebut perpindahan titik umum
$P$ ke titik asal sebagai “transformasi linear variabel”. Translasi
$(X,Y)\mapsto(X-a,Y-b)$ adalah perubahan koordinat afin, bukan transformasi
linear kecuali $P=(0,0)$. Edisi menggunakan istilah yang tepat tanpa mengubah
dekomposisi homogen dalam koordinat baru.

Titik itu mulus jika dan hanya jika multiplisitasnya $1$. Dalam hal ini
terdapat tepat satu garis singgung melalui titik tersebut, dan kemiringannya
dapat dihitung melalui turunan-turunan parsial.

![Tiga garis lurus berwarna merah, hijau, dan biru yang berpotongan di titik koordinat nol-koma-satu](authority/assets/250px-3_equations_-5.JPG)

*Garis-garis yang berpotongan di titik $(0,1)$. Cronholm144, domain publik;
berkas lokal: `authority/assets/250px-3_equations_-5.JPG`.*

<!-- upstream_entity: Ebene algebraische Kurven/Mehrere Geraden durch Ursprung/Gleichung/Beispiel -->

### Contoh: beberapa garis melalui titik asal {#br-ak-2025-2026-l22-exa-01}

Misalkan diberikan $d$ garis berbeda

$$
L_1,\ldots,L_d
$$

di bidang afin, semuanya melalui titik asal. Misalkan

$$
a_iX+b_iY=0,
\qquad i=1,\ldots,d,
$$

persamaan-persamaan garis yang terkait, yang hanya ditentukan hingga suatu
skalar. Gabungan garis-garis tersebut dideskripsikan oleh produk

$$
F=(a_1X+b_1Y)\cdots(a_dX+b_dY).
$$

Secara khusus,

$$
F=F_d
$$

homogen berderajat $d$. Di sini setiap faktor linear mendefinisikan sebuah
garis singgung melalui titik asal. Multiplisitasnya ialah $d$.

<!-- upstream_entity: Ebene algebraische Kurven/Kartesisches Blatt/Beispiel -->

### Contoh: folium Descartes {#br-ak-2025-2026-l22-exa-02}

![Potret René Descartes dengan rambut sebahu, kerah putih, dan pakaian hitam pada latar gelap](authority/assets/250px-Frans_Hals_-_Portret_van_René_Descartes.jpg)

*René Descartes (1596–1650). Potret menurut Frans Hals; diunggah ke Commons
oleh Dedden; domain publik; berkas lokal:
`authority/assets/250px-Frans_Hals_-_Portret_van_René_Descartes.jpg`.*

![Grafik folium Descartes berwarna hijau dengan gelung di kuadran pertama, simpul di titik asal, dan asimtot biru putus-putus](authority/assets/Kartesisches-Blatt.svg)

*Folium Descartes $x^3+y^3-3xy=0$, beserta sumbu, kisi, dan asimtotnya.
Georg-Johann, [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/);
berkas lokal: `authority/assets/Kartesisches-Blatt.svg`.*

*Folium Descartes* dideskripsikan oleh persamaan

$$
F=X^3+Y^3-3XY=0.
$$

Angka $3$ di sini tidak penting dan dapat diganti dengan bilangan lain yang
tidak sama dengan $0$. Komponen-komponen homogen persamaan kurva tersebut
ialah

$$
F_3=X^3+Y^3
$$

dan

$$
F_2=-3XY.
$$

Jadi titik asal folium Descartes mempunyai multiplisitas dua dan bersifat
singular. Sumbu $X$ dan sumbu $Y$ keduanya merupakan garis singgung, masing-
masing dengan multiplisitas satu. Pada semua titik lainnya kurva itu mulus,
dengan syarat lapangan dasarnya tidak berkarakteristik $3$. Dari

$$
\frac{\partial F}{\partial X}=3X^2-3Y=0
\qquad\text{dan}\qquad
\frac{\partial F}{\partial Y}=3Y^2-3X=0
$$

diperoleh

$$
Y=X^2
\qquad\text{dan}\qquad
X=Y^2,
$$

sehingga juga

$$
Y=Y^4,
$$

dan demikian pula untuk $X$. Jadi

$$
Y=X=0,
$$

atau $X$ dan $Y$ keduanya merupakan akar satuan ketiga: keduanya $1$, atau
$X$ dan $Y$ adalah dua akar satuan ketiga lainnya, dalam salah satu urutan.
Akan tetapi, pada titik-titik lain tempat kedua turunan parsial itu nol, $F$
bernilai $-1$. Karena itu titik-titik ini bukanlah titik kurva.

<!-- upstream_entity: Ebene algebraische Kurven/Tangente in einem glatten Punkt/Bemerkung -->

### Catatan: persamaan garis singgung di titik mulus {#br-ak-2025-2026-l22-rem-01}

Untuk suatu titik mulus

$$
P\in C=V(F)
$$

pada kurva aljabar bidang, multiplisitasnya ialah

$$
m=1.
$$

Jika $P=(0,0)$, suku linear persamaan kurvanya ialah

$$
F_1=uX+vY=0,
$$

dan

$$
\frac{\partial F}{\partial X}(P)=u
\qquad\text{serta}\qquad
\frac{\partial F}{\partial Y}(P)=v,
$$

sebab komponen-komponen homogen $F$ yang berderajat lebih tinggi tidak
memberikan sumbangan pada turunan parsial di titik asal. Jadi persamaan
linear tersebut merupakan persamaan garis singgung.

Untuk titik mulus sembarang

$$
P=(a,b)\in C,
$$

persamaan garis singgung juga dapat langsung dibaca dari turunan-turunan
parsial $F$ di $P$. Garis singgung itu diberikan oleh

$$
\frac{\partial F}{\partial X}(P)(X-a)
+
\frac{\partial F}{\partial Y}(P)(Y-b)
=0.
$$

<!-- upstream_entity: Ebene algebraische Kurven/Tangentialabbildung und Tangente in einem glatten Punkt als Kern/Bemerkung -->

### Catatan: pemetaan tangen dan arah garis singgung {#br-ak-2025-2026-l22-rem-02}

Misalkan $F\in K[X,Y]$ dengan kurva aljabar bidang terkait $C$, dan misalkan

$$
P\in C=V(F)
$$

suatu titik mulus kurva. Pemetaan

$$
F:\mathbb A_K^2\longrightarrow\mathbb A_K^1
$$

dan titik $P$ menentukan *pemetaan tangen* linear, yang juga disebut
*diferensial total*, di antara ruang-ruang tangen terkait:

$$
\begin{aligned}
T_PF
=
\left(
\frac{\partial F}{\partial X}(P),
\frac{\partial F}{\partial Y}(P)
\right):
T_P\mathbb A_K^2\cong\mathbb A_K^2
&\longrightarrow
T_{F(P)}\mathbb A_K^1
=T_0\mathbb A_K^1
\cong\mathbb A_K^1,\\
(s,t)
&\longmapsto
\frac{\partial F}{\partial X}(P)s
+
\frac{\partial F}{\partial Y}(P)t.
\end{aligned}
$$

Karena $P$ titik mulus, pemetaan linear ini bukan pemetaan nol. Arah garis
singgung $C$ di $P$ merupakan kernel pemetaan tangen ini. Ketika bidang
tangen di $P$ diidentifikasi dengan bidang afin sekelilingnya, titik $P$
harus diidentifikasi dengan titik asal: garis singgung harus melalui titik
tersebut, sedangkan kernel hanya menentukan suatu arah linear.

![Dua kurva hitam—sebuah lingkaran dan sebuah cabang melengkung—yang berpotongan di dua titik, ditampilkan pada sumbu koordinat abu-abu](authority/assets/250px-Intersect3.png)

*Pada kurva aljabar, titik potong komponen-komponen tak tereduksi tidak pernah
mulus. Sumber kuliah mengkreditkan Michael Larsen; metadata Commons mencatat
pengunggah Maksim dan lisensi
[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/); berkas lokal:
`authority/assets/250px-Intersect3.png`.*

Pernyataan berikut menunjukkan bahwa titik perpotongan dua komponen tak
tereduksi tidak pernah dapat mulus.

<!-- upstream_entity: Ebene algebraische Kurve/Glatter Punkt/Liegt nur auf einer Komponente/Fakt -->

### Lema: titik mulus terletak pada hanya satu komponen {#br-ak-2025-2026-l22-lem-04}

Misalkan

$$
C=V(F)
$$

suatu kurva aljabar bidang dan

$$
F=F_1\cdots F_n
$$

dekomposisinya menjadi faktor-faktor prima yang berbeda. Misalkan $P\in C$
suatu titik mulus kurva. Maka $P$ terletak pada hanya satu komponen

$$
C_i=V(F_i)
$$

kurva tersebut.

**Bukti.** Lihat Soal 22.9.

<!-- upstream_entity: Ebene algebraische Kurve/Glatte zusammenhängende Kurve/Ist irreduzibel/Fakt -->

### Korolari: kurva mulus dan terhubung bersifat tak tereduksi {#br-ak-2025-2026-l22-cor-02}

Misalkan

$$
C\subseteq\mathbb A_K^2
$$

suatu kurva aljabar bidang mulus yang terhubung dalam topologi Zariski di
atas lapangan tertutup secara aljabar $K$. Maka $C$ tak tereduksi.

<!-- upstream_entity: Ebene algebraische Kurve/Glatte zusammenhängende Kurve/Ist irreduzibel/Fakt/Beweis -->

#### Bukti {#br-ak-2025-2026-l22-cor-02-proof}

Menurut Lema 22.12, komponen-komponen tak tereduksi kurva tersebut saling
lepas. Akan tetapi, komponen-komponen itu juga merupakan komponen-komponen
terhubung kurva. Jadi hanya terdapat satu komponen tak tereduksi, dan karena
itu kurva tersebut tak tereduksi.

---

**Provenans edisi.** Terjemahan dan produksi pembaca: OpenAI Codex
gpt-5.6-sol, Ultra. Sumber, pengarang, dan lisensi komponen dipertahankan
seperti dinyatakan dalam metadata dan berkas hak edisi.
