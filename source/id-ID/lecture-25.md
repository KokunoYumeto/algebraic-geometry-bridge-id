---
title: "Kuliah 25 - Solusi Deret Pangkat untuk Kurva Aljabar"
stable_id: br-ak-2012-l25
language: id-ID
source_author: "Holger Brenner"
frozen_revision_contributor: "Arbota"
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 25"
upstream_pageid: 50731
upstream_revid: 793525
upstream_timestamp: "2022-08-25T06:09:07Z"
upstream_mediawiki_sha1: c589c3b9586e551eb81d7d941d79a9bc1461fe06
source_url: "https://de.wikiversity.org/w/index.php?oldid=793525"
authority_manifest: authority/wikiversity/unit-25/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 7cafbca7b5fd080529c2019967647ef8ffa823539b2113caaf0ad65e56d6afc1
lecture_xml: authority/wikiversity/unit-25/lecture-25.xml
lecture_xml_sha256: 4063269fa3a4e919790799935760600f5df9fecb1c8a677554188f059b316aa1
lecture_expanded_tex: authority/wikiversity/unit-25/lecture-25-expanded.tex
lecture_expanded_tex_sha256: 47cd10c4b01ead8e51b1fa6e1e020900032bae6517030efd4cc116ef0ba1fe5e
lecture_dependency_identity_rows_sha256: aa14c07698e5e2911790457bee99f6e58a47b68fd5e75520c175ecc2756df8b1
license: "Current semantic course text and this translation: CC BY-SA 4.0. The official 2012 PDF file-description surface also records the legacy CC BY-SA 2.0 Germany route. Unit 25 contains no substantive media; no blanket relicensing claim is made."
source_component_license_route: "Semantic-site rights notice: CC BY-SA 4.0; official-PDF legacy file-description notice: CC BY-SA 2.0 Germany; official-PDF current print-version notice: CC BY-SA 4.0; no blanket relicensing claim."
license_evidence: "authority/UNIT_25_AUTHORITY_FREEZE.md; authority/RIGHTS-unit-25.csv; authority/ASSET_CLOSURE-unit-25.json"
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_semantic_entities: 9
source_corrections: 3
correction_ids: "AGC-CORR-0091; AGC-CORR-0092; AGC-CORR-0093"
reader_media_positions: 0
---

# Kuliah 25: Solusi Deret Pangkat untuk Kurva Aljabar {#br-ak-2012-l25}

## Solusi deret pangkat untuk kurva aljabar {#br-ak-2012-l25-s01}

<!-- upstream_entity: Ebene algebraische Kurve/Potenzreihenansatz/Einführung und Beispiele/Textabschnitt -->

Misalkan $F\ne 0$ suatu polinom yang mendeskripsikan kurva aljabar bidang
$C$, dan andaikan

$$
P=(0,0)\in C.
$$

Andaian ini tidak membatasi keumuman, sebab keadaan tersebut selalu dapat
dicapai melalui suatu translasi. Bagaimana kita dapat mendeskripsikan kurva
di sekitar titik asal dengan memakai deret pangkat? Dengan kata lain, kapan
terdapat homomorfisme gelanggang yang ditentukan oleh deret pangkat takkonstan
$G$ dan $H$ dengan suku konstan nol,

$$
\begin{aligned}
K[X,Y]&\longrightarrow K[[T]],\\
X&\longmapsto G,\\
Y&\longmapsto H,
\end{aligned}
$$

sedemikian sehingga

$$
F(G,H)=0?
$$

Secara ekuivalen, kita mencari homomorfisme gelanggang

$$
K[X,Y]/(F)\longrightarrow K[[T]].
$$

Jadi persoalannya ialah mencari solusi deret pangkat bagi persamaan

$$
F(X,Y)=0
$$

yang mendeskripsikan perilaku kurva di sekitar solusi titik $(0,0)$ dengan
lebih teliti.

Pendekatan dasarnya adalah pendekatan deret pangkat, seperti yang juga dipakai
dalam teori persamaan diferensial. Kita mulai dengan

$$
G=\sum_{k=0}^{\infty}a_kT^k
\qquad\text{dan}\qquad
H=\sum_{\ell=0}^{\infty}b_\ell T^\ell,
$$

dengan koefisien $a_k$ dan $b_\ell$ yang mula-mula belum diketahui. Substitusi
langsung ke dalam persamaan $F=0$, lalu pengembangan hasil kalinya,
menghasilkan suatu ungkapan yang pada prinsipnya tak hingga. Akan tetapi,
untuk setiap pangkat $T^k$, ungkapan bagi koefisien yang bersesuaian hanya
ditentukan oleh sejumlah data berhingga: cukup mengetahui koefisien-koefisien
$F$, $G$, dan $H$ hingga derajat yang relevan di bawah $k$. Karena harus berlaku

$$
F(G,H)=0,
$$

koefisien-koefisien $F$, $G$, dan $H$ harus membuat koefisien setiap $T^k$
sama dengan nol.

Kita kemudian mencari syarat bagi keberadaan solusi, bentuknya, dan
ketunggalannya. Syarat

$$
a_0=b_0=0
$$

adalah syarat awal yang menyatakan bahwa solusi deret pangkat tersebut melalui
titik asal.

Syarat bagi suku-suku linear deret pangkat, yaitu bagi $a_1$ dan $b_1$, segera
muncul. Syarat ini memberi pembenaran tambahan bagi penafsiran faktor-faktor
linear dari komponen homogen berderajat terendah $F_m$ dalam dekomposisi
homogen $F$ sebagai persamaan-persamaan garis singgung.

<!-- upstream_entity: Ebene algebraische Kurven/Potenzreihenlösung für Punkt/Linearer Term liegt auf Tangente/Fakt -->

### Lema 25.1: suku linear terletak pada suatu garis singgung {#br-ak-2012-l25-lem-01}

Misalkan $K$ suatu lapangan yang tertutup secara aljabar dan

$$
F\in K[X,Y]
$$

suatu polinom dengan dekomposisi homogen

$$
F=F_m+\cdots+F_d,
\qquad d\geq m\geq1,
\qquad F_m\ne0.
$$

Misalkan

$$
F_m=\prod_{\lambda=1}^{m}(u_\lambda X+v_\lambda Y)
$$

faktorisasi $F_m$ menjadi faktor-faktor linear. Faktor-faktor linear ini
mendefinisikan garis-garis singgung kurva

$$
C=V(F)
$$

di titik $P=(0,0)$. Misalkan pula

$$
G=\sum_{n=0}^{\infty}a_nT^n
\qquad\text{dan}\qquad
H=\sum_{\ell=0}^{\infty}b_\ell T^\ell
$$

merupakan unsur $K[[T]]$ yang memberi suatu solusi persamaan kurva melalui
titik asal, yakni

$$
a_0=b_0=0
\qquad\text{dan}\qquad
F(G,H)=0.
$$

Maka, untuk suatu $\lambda$, berlaku

$$
u_\lambda a_1+v_\lambda b_1=0.
$$

Dengan kata lain, pasangan suku linear dari kedua deret pangkat tersebut
ditentukan oleh salah satu garis singgung.

<!-- upstream_entity: Ebene algebraische Kurven/Potenzreihenlösung für Punkt/Linearer Term liegt auf Tangente/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l25-lem-01-proof}

Substitusikan

$$
G=a_1T+a_2T^2+\cdots
\qquad\text{dan}\qquad
H=b_1T+b_2T^2+\cdots
$$

ke dalam $F$. Suatu komponen homogen $F_k$ merupakan jumlah suku-suku
$c_{ij}X^iY^j$ dengan $i+j=k$. Kita dapat langsung memfaktorkan $T^k$ dan
memperoleh ungkapan berbentuk

$$
\begin{aligned}
F_k(G,H)
={}&\left(\sum_{i+j=k}c_{ij}a_1^ib_1^j\right)T^k\\
&+\left(\sum_{i+j=k}c_{ij}
\left(ia_1^{i-1}a_2b_1^j
+ja_1^ib_1^{j-1}b_2\right)\right)T^{k+1}
+\cdots.
\end{aligned}
$$

Jadi $a_1$ dan $b_1$ masuk secara langsung ke koefisien $T^k$ melalui
$F_k$; koefisien itu pada umumnya juga menerima sumbangan yang lebih rumit
dari $F_\ell$ dengan $\ell<k$. Untuk $F_m$ tidak ada komponen homogen yang
lebih rendah. Karena itu persamaan penentu bagi $a_1$ dan $b_1$ ialah

$$
\sum_{i+j=m}c_{ij}a_1^ib_1^j=0,
$$

atau, secara ekuivalen,

$$
F_m(a_1,b_1)=0.
$$

Karena $F_m$ merupakan hasil kali faktor-faktor linear, vektor baris
$(a_1,b_1)$ harus menolkan salah satu faktor tersebut. Inilah pernyataan yang
hendak dibuktikan. $\square$

Perhatikan bahwa Lema 25.1 tidak menyingkirkan kemungkinan

$$
a_1=b_1=0.
$$

Memang, realisasi suatu kurva dengan deret pangkat sepanjang sebuah garis
singgung yang telah ditentukan hanya tersedia di bawah syarat tambahan; lihat
[Teorema 25.2](#br-ak-2012-l25-thm-01) dan contoh-contoh di bawah.

Beban perhitungan untuk menentukan solusi deret pangkat dapat dikurangi secara
berarti apabila kita membatasi perhatian pada “solusi berbentuk grafik”, yaitu
salah satu deret pangkatnya hanyalah sebuah polinom linear yang diberikan oleh
suatu garis singgung, sedangkan deret yang lain harus ditentukan. Pembatasan ini
sering kali tidak hakiki, sebagaimana mengikuti dari
[Lema 24.11](#br-ak-2012-l24-lem-02). Dengan lema tersebut, kita dapat
mereparametrisasi

$$
G,H\in K[[T]]
$$

dengan mudah apabila kedua suku linearnya tidak sekaligus lenyap. Andaikan

$$
G=a_1T+\cdots,
\qquad a_1\ne0.
$$

Pilih deret pangkat $U(T)$ yang merupakan invers komposisional $G$. Maka

$$
G(U(T))=T
\qquad\text{dan}\qquad
H(U(T))=\widetilde H(T).
$$

Dengan menempatkan automorfisme gelanggang deret pangkat sesudah pemetaan
semula, kita memperoleh komposisi

$$
K[X,Y]
\mathop{\longrightarrow}^{X\mapsto G,\,Y\mapsto H}
K[[T]]
\mathop{\longrightarrow}^{T\mapsto U(T)}
K[[T]],
$$

yang berbentuk sangat sederhana,

$$
X\longmapsto T,
\qquad
Y\longmapsto\widetilde H.
$$

Artinya, kita hendak merealisasikan kurva sebagai grafik suatu fungsi formal
dalam satu variabel.

> **Catatan edisi - koreksi orientasi komposisi sumber.** Sumber menulis
> $U(G(T))=T$ dan $U(H(T))=\widetilde H(T)$. Akan tetapi, anak panah yang
> ditampilkan adalah substitusi $T\mapsto U(T)$ sesudah pemetaan pertama,
> sehingga citra yang dihasilkan adalah $G(U(T))$ dan $H(U(T))$. Edisi memakai
> orientasi komposisi yang sesuai dengan anak panah tersebut.

<!-- upstream_entity: Ebene algebraische Kurven/Tangenten mit Kontaktordnung eins/Formal-analytische Realisierung als Graph/Fakt -->

### Teorema 25.2: garis singgung berorde kontak satu menghasilkan solusi berbentuk grafik {#br-ak-2012-l25-thm-01}

Misalkan $K$ suatu lapangan dan

$$
F\in K[X,Y]
$$

suatu polinom taknol dengan

$$
(0,0)\in C=V(F).
$$

Misalkan

$$
F=F_d+\cdots+F_m,
\qquad d\geq m,
\qquad F_m\ne0,
$$

dekomposisi homogen $F$, dan misalkan $uX+vY$ suatu faktor linear sederhana
dari $F_m$, yaitu suatu polinom linear yang mendefinisikan garis singgung
berorde kontak satu, atau bermultiplisitas $1$. Maka terdapat deret pangkat

$$
G=\sum_{n=0}^{\infty}a_nT^n,
\qquad
H=\sum_{\ell=0}^{\infty}b_\ell T^\ell
\in K[[T]]
$$

sedemikian sehingga

$$
F(G,H)=0,
\qquad
a_0=b_0=0,
\qquad
a_1u+b_1v=0.
$$

Selain itu, salah satu dari kedua deret pangkat tersebut dapat dipilih sebagai
polinom linear.

> **Catatan edisi - penegasan syarat awal.** Sumber menulis
> “$a_0,b_0=0$”. Edisi menuliskan kesamaan yang dimaksud tanpa ambiguitas
> sebagai $a_0=b_0=0$.

<!-- upstream_entity: Ebene algebraische Kurven/Tangenten mit Kontaktordnung eins/Formal-analytische Realisierung als Graph/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l25-thm-01-proof}

Melalui transformasi linear pada variabel, kita boleh mengandaikan

$$
uX+vY=Y.
$$

Kita akan membangun solusi deret pangkat dengan

$$
G=T
$$

dan

$$
H=b_2T^2+b_3T^3+\cdots.
$$

Karena $a_1=1$ dan $b_1=0$, solusi ini memenuhi syarat linear yang diberikan
oleh garis singgung tersebut.

Tuliskan

$$
F=\sum_{i,j}c_{ij}X^iY^j.
$$

Kita mempunyai

$$
c_{m,0}=0,
$$

sebab jika tidak demikian, $Y$ tidak mungkin menjadi faktor linear $F_m$.
Selain itu,

$$
c_{m-1,1}\ne0,
$$

sebab jika koefisien ini nol, $Y$ akan menjadi faktor linear dengan
multiplisitas sekurang-kurangnya $2$.

Sekarang kita tunjukkan bahwa syarat awal tersebut menentukan tepat satu deret
pangkat

$$
H=b_2T^2+b_3T^3+\cdots.
$$

Substitusi $G$ dan $H$ ke dalam $F$ memberi satu syarat untuk setiap $k$,
karena koefisien $T^k$ pada hasilnya harus sama dengan nol. Koefisien ke-$k$
merupakan jumlah ungkapan berbentuk

$$
c_{ij}b_{\ell_1}\cdots b_{\ell_j},
\qquad
i+\sum_{\rho=1}^{j}\ell_\rho=k.
$$

Ungkapan-ungkapan ini dapat muncul beberapa kali, dengan suatu koefisien
multinomial. Karena $\ell_\rho\geq2$, suku $b_\ell$ belum muncul apabila

$$
k<m+\ell-1.
$$

Suku $b_\ell$ pertama kali muncul pada koefisien dengan

$$
k=m+\ell-1,
$$

dan satu-satunya kemunculannya di sana ialah

$$
c_{m-1,1}b_\ell.
$$

Suku-suku lain dalam koefisien itu hanya melibatkan $c_{ij}$ dan $b_r$ dengan
$r<\ell$. Karena $c_{m-1,1}\ne0$, nilai $b_\ell$ ditentukan secara tunggal.
Dengan demikian koefisien-koefisien $b_\ell$ dapat dibangun secara induktif,
dan pada setiap tahap nilainya ditentukan secara tunggal oleh persamaan
koefisien yang bersesuaian. $\square$

<!-- upstream_entity: Potenzreihe für ebene Kurven/Graph einer rationalen Funktion/X^3+XY+Y ist 0/Beispiel -->

### Contoh 25.3: grafik suatu fungsi rasional {#br-ak-2012-l25-ex-01}

Tinjau kurva afin bidang berderajat tiga yang diberikan oleh

$$
F=X^3+XY+Y=0.
$$

Turunan parsialnya ialah

$$
\frac{\partial F}{\partial X}=3X^2+Y
\qquad\text{dan}\qquad
\frac{\partial F}{\partial Y}=X+1.
$$

Turunan parsial yang kedua hanya nol ketika $X=-1$; tetapi pada garis itu
$F$ bernilai $-1$. Jadi kurva tersebut mulus. Di titik asal, kedua turunan
parsial bernilai $(0,1)$. Garis singgungnya dengan demikian adalah sumbu
$X$, sesuai dengan kenyataan bahwa suku linear persamaan kurva ialah $Y$.

Kita hitung deret pangkat

$$
Y=H(T)=\sum_{\ell=0}^{\infty}b_\ell T^\ell
$$

yang mendeskripsikan kurva sebagai grafik di titik asal, dengan $X=T$. Syarat
awalnya ialah

$$
b_0=b_1=0.
$$

Koefisien-koefisien berikutnya harus memenuhi

$$
F(T,H)=T^3+TH+H=0,
$$

atau

$$
T^3+T(b_2T^2+b_3T^3+\cdots)
+(b_2T^2+b_3T^3+\cdots)=0.
$$

Untuk $b_2$, koefisien kedua persamaan langsung memberi

$$
b_2=0.
$$

Untuk $b_3$, koefisien ketiga memberi

$$
1+b_3=0,
$$

sehingga $b_3=-1$. Koefisien-koefisien selanjutnya memberi relasi

$$
b_{\ell-1}+b_\ell=0.
$$

Jadi koefisien-koefisien berikutnya berganti-ganti antara $1$ dan $-1$, dan

$$
H=-T^3+T^4-T^5+T^6-T^7+\cdots.
$$

Menulis ulang persamaan kurva sebagai

$$
Y=\frac{-X^3}{1+X}
$$

menunjukkan bahwa kurva ini merupakan grafik fungsi rasional yang mempunyai
kutub di $X=-1$. Deret pangkat di atas mendeskripsikan grafik fungsi rasional
tersebut sebagai grafik suatu fungsi analitik formal.

<!-- upstream_entity: Potenzreihe für ebene Kurven/Kartesisches Blatt/Graph/Beispiel -->

### Contoh 25.4: folium Descartes sebagai grafik formal {#br-ak-2012-l25-ex-02}

Tinjau folium Descartes

$$
X^3+Y^3-3XY=0
$$

di titik asal, dengan garis singgung $Y=0$. Kita hendak menentukan deret
pangkat yang mendeskripsikan cabang kurva yang ditentukan oleh garis singgung
tersebut sebagai sebuah grafik. Ambil

$$
X=T
$$

dan

$$
H=b_2T^2+b_3T^3+b_4T^4+\cdots,
$$

dengan asumsi bahwa karakteristik $K$ bukan $3$. Koefisien-koefisien $b_\ell$
ditentukan oleh

$$
\begin{aligned}
0
&=T^3+H^3-3TH\\
&=T^3+(b_2T^2+b_3T^3+\cdots)^3
-3T(b_2T^2+b_3T^3+\cdots).
\end{aligned}
$$

Substitusi dan pengembangan ini pertama kali memberi syarat pada $k=3$.
Suku $X^3$, atau $T^3$, hanya perlu diperhitungkan sekali, yakni ketika
$k=3$. Suku $Y^3$ baru memberi sumbangan mulai $k\geq6$, sebab $Y=H$
merupakan kelipatan $T^2$. Suku $XY$ harus diperhitungkan mulai $k=3$.

Untuk $b_2$ kita memperoleh

$$
1-3b_2=0,
$$

sehingga

$$
b_2=\frac13.
$$

Koefisien $b_3$ pertama kali muncul dalam syarat bagi koefisien keempat dan
berdiri sendiri di sana, sehingga

$$
b_3=0.
$$

Dengan alasan yang sama,

$$
b_4=0.
$$

Untuk $b_5$, koefisien keenam menjadi penentu, dan sekarang suku $Y^3$ juga
harus diperhitungkan. Syaratnya ialah

$$
b_2^3-3b_5=0,
$$

jadi

$$
b_5=\frac1{81}.
$$

Untuk $b_6,b_7,b_8$, perhatikan bahwa suku

$$
Y^3=(b_2T^2+b_5T^5+\cdots)
(b_2T^2+b_5T^5+\cdots)
(b_2T^2+b_5T^5+\cdots)
$$

baru memberi sumbangan lagi pada koefisien kesembilan, yaitu
$3b_2^2b_5$. Karena itu $b_6$ dan $b_7$ berdiri sendiri dan harus nol. Untuk
$b_8$ kita memperoleh

$$
3b_2^2b_5-3b_8=0,
$$

sehingga

$$
b_8=\frac1{729}.
$$

Jadi bagian awal deret pangkat yang mendeskripsikan cabang kurva tersebut
sebagai grafik ialah

$$
H=\frac13T^2+\frac1{81}T^5+\frac1{729}T^8+\cdots.
$$

<!-- upstream_entity: Potenzreihe für ebene Kurven/Neilsche Parabel/Keine tangentiale Potenzreihe/Beispiel -->

### Contoh 25.5: parabola Neil tanpa suku linear taknol {#br-ak-2012-l25-ex-03}

Tinjau parabola Neil yang diberikan oleh

$$
X^3-Y^2=0.
$$

Titik asalnya singular dan hanya mempunyai satu garis singgung, yaitu

$$
Y=0.
$$

Namun, garis singgung ini mempunyai multiplisitas dua, sehingga
[Teorema 25.2](#br-ak-2012-l25-thm-01) tidak dapat diterapkan. Bahkan, tidak
ada solusi deret pangkat di titik asal dengan suku linear taknol.

Untuk melihatnya, misalkan

$$
X=G=a_1T+a_2T^2+\cdots
$$

dan

$$
Y=H=b_1T+b_2T^2+\cdots
$$

memenuhi persamaan kurva. Setelah disubstitusikan, koefisien kedua memberi

$$
-b_1^2=0,
$$

sehingga $b_1=0$. Sebaliknya, koefisien ketiga memberi

$$
a_1^3=0,
$$

sehingga $a_1=0$ pula.

Walaupun demikian, terdapat solusi deret pangkat bagi parabola Neil melalui
titik asal. Kita dapat mengambil solusi monomial

$$
G=T^2
\qquad\text{dan}\qquad
H=T^3.
$$

Solusi ini bahkan memberi bijeksi antara garis afin dan parabola Neil, tetapi
suku linearnya memang sama dengan nol.

<!-- upstream_entity: Satz über implizite Funktionen/Ebene Kurven/Bemerkung -->

### Catatan 25.6: perbandingan dengan teorema fungsi implisit {#br-ak-2012-l25-rem-01}

Misalkan

$$
K=\mathbb R
\qquad\text{atau}\qquad
K=\mathbb C,
$$

dan $F\in K[X,Y]$. Jika

$$
\left(
\frac{\partial F}{\partial x}(P),
\frac{\partial F}{\partial y}(P)
\right)\ne(0,0),
$$

yakni jika $P$ merupakan titik reguler bagi fungsi $F$, atau secara
ekuivalen, titik mulus pada

$$
C=V(F-F(P)),
$$

maka teorema fungsi implisit menjamin bahwa, dalam suatu lingkungan metrik
dari $P$, kurva tersebut dapat dinyatakan sebagai grafik suatu fungsi
terdiferensialkan.

> **Catatan edisi - perbaikan redaksional sumber.** Sumber menulis
> “$K=\mathbb R$ atau $=\mathbb C$”. Edisi melengkapi subjek pada alternatif
> kedua dan menulis $K=\mathbb R$ atau $K=\mathbb C$.
