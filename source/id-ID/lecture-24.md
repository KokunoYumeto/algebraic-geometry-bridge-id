---
title: "Kuliah 24 - Garis Singgung dan Gelanggang Deret Pangkat Formal"
stable_id: br-ak-2012-l24
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 24"
upstream_pageid: 50730
upstream_revid: 933672
upstream_timestamp: "2024-05-06T16:57:23Z"
upstream_mediawiki_sha1: af86fa9893c96376f910495b9a5d0c8be417b09e
source_url: "https://de.wikiversity.org/w/index.php?oldid=933672"
authority_manifest: authority/wikiversity/unit-24/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 3731896a5980c565d9d69a2e01eee497f13b6f449f2f9c701fce726271c026a5
lecture_xml: authority/wikiversity/unit-24/lecture-24.xml
lecture_xml_sha256: 0dd11d94f88e81036d00c2662c6377e13e25d749bed7721902ec75c737251bd3
lecture_expanded_tex: authority/wikiversity/unit-24/lecture-24-expanded.tex
lecture_expanded_tex_sha256: b391d18cc0cea33afedfff5e6db46842d2ef6504843336b71f44eda448f12f5e
lecture_dependency_identity_rows_sha256: 861c2d4566a137c9c3d791480bfa2f1f36a7885798f54f34c8e60557d34e75b2
license: "Current semantic course text and this translation: CC BY-SA 4.0. The official 2012 PDF file-description surface also records the legacy CC BY-SA 2.0 Germany route. Unit 24 contains no substantive media; no blanket relicensing claim is made."
source_component_license_route: "Semantic-site rights notice: CC BY-SA 4.0; official-PDF legacy file-description notice: CC BY-SA 2.0 Germany; official-PDF current print-version notice: CC BY-SA 4.0; no blanket relicensing claim."
license_evidence: "authority/UNIT_24_AUTHORITY_FREEZE.md; authority/RIGHTS-unit-24.csv; authority/ASSET_CLOSURE-unit-24.json"
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_semantic_entities: 22
source_corrections: 6
reader_media_positions: 0
---

# Kuliah 24: Garis Singgung dan Gelanggang Deret Pangkat Formal {#br-ak-2012-l24}

<!-- upstream_entity: Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 24#Tangenten bei Parametrisierungen -->

## Garis singgung pada parametrisasi {#br-ak-2012-l24-s01}

<!-- upstream_entity: Algebraische Kurven/Rationale Parametrisierung/Verhältnis Tangenten/Fakt -->

### Teorema 24.1: vektor turunan suatu parametrisasi {#br-ak-2012-l24-thm-01}

Misalkan $K$ lapangan tak hingga dan

$$
\varphi\colon \mathbb A_K^1\longrightarrow \mathbb A_K^n
$$

suatu pemetaan yang diberikan oleh $n$ polinom dalam satu variabel,

$$
\varphi=\bigl(\varphi_1(t),\ldots,\varphi_n(t)\bigr),
$$

dan misalkan citranya termuat dalam kurva

$$
C=V(F_1,\ldots,F_m).
$$

Ambil $Q\in\mathbb A_K^1$ dan

$$
P=\varphi(Q)\in C.
$$

Maka vektor turunan

$$
\left(
  \frac{\partial\varphi_1}{\partial t}(Q),\ldots,
  \frac{\partial\varphi_n}{\partial t}(Q)
\right)
$$

terletak dalam kernel pemetaan tangen linear

$$
(TF)_P\colon\mathbb A_K^n\longrightarrow\mathbb A_K^m
$$

yang didefinisikan oleh matriks Jacobi

$$
\left(
  \frac{\partial F_i}{\partial X_j}(P)
\right)_{ij}.
$$

Jika $n=2$, kedua turunan $\varphi_1'(Q)$ dan $\varphi_2'(Q)$ tidak
sekaligus nol, dan $P$ merupakan titik mulus pada $C$, maka

$$
\left(
  \frac{\partial\varphi_1}{\partial t}(Q),
  \frac{\partial\varphi_2}{\partial t}(Q)
\right)
$$

menentukan arah garis singgung $C$ di $P$.

<!-- upstream_entity: Algebraische Kurven/Rationale Parametrisierung/Verhältnis Tangenten/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l24-thm-01-proof}

Tuliskan $F=(F_1,\ldots,F_m)$. Karena

$$
\varphi\bigl(\mathbb A_K^1\bigr)\subseteq V(F_1,\ldots,F_m),
$$

komposisi $F\circ\varphi$ adalah pemetaan konstan ke titik nol. Karena
$K$ tak hingga, setiap polinom komponen yang menyatakan
$F_i\circ\varphi$ merupakan polinom nol. Aturan rantai formal untuk
polinom karena itu memberikan

$$
0=(T(F\circ\varphi))_Q=(TF)_P\circ(T\varphi)_Q.
$$

Jadi citra $(T\varphi)_Q$, yang dibentang oleh vektor turunan di atas,
termuat dalam kernel $(TF)_P$.

Dalam kasus bidang yang dinyatakan pada bagian terakhir teorema, kernel
matriks Jacobi berdimensi satu. Citra $(T\varphi)_Q$ juga berdimensi satu
karena vektor turunannya tidak nol. Inklusi tersebut dengan demikian
merupakan kesamaan, sehingga vektor itu menentukan arah garis singgung.
$\square$

<!-- upstream_entity: Endlicher Körper/(t^q-t,t^q-t)/Gerade/Ableitung ist keine Tangente/Beispiel -->

### Contoh 24.2: mengapa lapangan harus tak hingga {#br-ak-2012-l24-ex-01}

Misalkan $K$ lapangan hingga dengan

$$
q=p^e
$$

unsur, dengan $p$ prima dan $e\geq1$. Pemetaan

$$
\begin{aligned}
\mathbb A_K^1&\longrightarrow\mathbb A_K^2,\\
t&\longmapsto(t^q-t,t^q-t)
\end{aligned}
$$

mengirim setiap titik $K$-rasional ke satu-satunya titik citra
$(0,0)$, sebab $t^q=t$ untuk setiap $t\in K$. Akan tetapi, vektor turunan
formal parametrisasi polinomial tersebut ialah

$$
(-1,-1).
$$

Jadi pemetaan pada titik-titik $K$-rasional dapat bersifat konstan dalam
karakteristik positif walaupun turunan formal polinom yang
mendefinisikannya tidak nol. Titik asal merupakan titik mulus pada setiap
garis

$$
C=V(aX+bY),
$$

dengan $(a,b)\ne(0,0)$.

Arah garis singgungnya adalah kernel bentuk linear $aX+bY$, sedangkan bentuk itu
menganulir $(-1,-1)$ hanya apabila $a=-b$. Dengan demikian, asumsi bahwa
$K$ tak hingga dalam Teorema 24.1 tidak dapat dihapus.

> **Catatan edisi.** Pernyataan kekonstanan di sini secara eksplisit
> menyangkut fungsi pada titik-titik $K$-rasional. Morfisme yang
> didefinisikan oleh pasangan polinom $(t^q-t,t^q-t)$ bukan morfisme
> konstan. Pembedaan ini mencegah kata “konstan” disalahartikan sebagai
> pernyataan tentang polinom atau morfisme itu sendiri.

<!-- upstream_entity: Ebene algebraische Kurve/x^2-y^2+y^3/Tangente unter Parametrisierung/t ist 2/Beispiel -->

### Contoh 24.3: garis singgung dari sebuah parametrisasi {#br-ak-2012-l24-ex-02}

Dalam contoh ini kita bekerja di atas lapangan $K$ berkarakteristik nol.
Pertimbangkan kurva

$$
V(y^2-x^2-x^3)
$$

dengan parametrisasi

$$
(\varphi(t),\psi(t))
=\bigl(t^2-1,t(t^2-1)\bigr)
=(x,y).
$$

Untuk

$$
F=y^2-x^2-x^3,
$$

turunan parsialnya adalah

$$
\frac{\partial F}{\partial x}=-2x-3x^2
\qquad\text{dan}\qquad
\frac{\partial F}{\partial y}=2y.
$$

Matriks Jacobi parametrisasi, dipandang sebagai vektor baris, ialah

$$
\left(
  \frac{\partial\varphi}{\partial t},
  \frac{\partial\psi}{\partial t}
\right)
=(2t,3t^2-1).
$$

Dengan $P=(\varphi(t),\psi(t))$, perhitungan aturan rantai polinomial
formal memang memberikan

$$
\begin{aligned}
&\left(
  \frac{\partial F}{\partial x}(P),
  \frac{\partial F}{\partial y}(P)
\right)
\begin{pmatrix}2t\\3t^2-1\end{pmatrix}\\
&=\left(
  -2(t^2-1)-3(t^2-1)^2,
  2(t^3-t)
\right)
\begin{pmatrix}2t\\3t^2-1\end{pmatrix}\\
&=-4t(t^2-1)-6t(t^2-1)^2
  +2(t^3-t)(3t^2-1)\\
&=-4t^3+4t-6t^5+12t^3-6t
  +6t^5-2t^3-6t^3+2t\\
&=0.
\end{aligned}
$$

Untuk $t=2$, misalnya, diperoleh titik citra

$$
P=(3,6).
$$

Vektor turunannya adalah $(4,11)$, sedangkan turunan parsial di $P$
memberikan gradien $(-33,12)$, yang ortogonal terhadap vektor arah garis
singgung. Garis singgungnya dapat ditulis sebagai

$$
\bigl\{(3,6)+s(4,11)\mid s\in K\bigr\}
$$

atau sebagai

$$
V(-11x+4y+9).
$$

> **Catatan edisi.** Sumber tidak menyatakan batasan karakteristik pada
> contoh numerik ini. Edisi ini membatasinya pada karakteristik nol karena
> koefisien $2$, $3$, dan $11$, serta nilai khusus $t=2$, dapat berubah
> atau lenyap setelah direduksi dalam karakteristik positif kecil. Dalam
> karakteristik positif, kemulusan dan arah garis singgung harus diperiksa kembali
> di lapangan yang bersangkutan.

<!-- upstream_entity: Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 24#Tangenten bei Raumkurven -->

## Garis singgung pada kurva ruang {#br-ak-2012-l24-s02}

<!-- upstream_entity: Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 24#Tangenten bei Raumkurven/Jacobi-Absatz -->

Walaupun pembahasan kita terutama dibatasi pada kurva bidang, turunan juga
dapat dipakai untuk mendefinisikan titik mulus dan singular pada kurva di
ruang berdimensi lebih tinggi, bahkan pada varietas sembarang. Sebagai
ilustrasi, misalkan sebuah kurva ruang diberikan oleh dua polinom tanpa
komponen bersama,

$$
F,G\in K[X,Y,Z].
$$

Tidak setiap kurva ruang dapat dideskripsikan dengan cara ini. Untuk
$P\in C=V(F,G)$, pertimbangkan kembali pemetaan yang diberikan oleh matriks
Jacobi

$$
\left(
\begin{array}{ccc}
\dfrac{\partial F}{\partial x}&
\dfrac{\partial F}{\partial y}&
\dfrac{\partial F}{\partial z}\\[4pt]
\dfrac{\partial G}{\partial x}&
\dfrac{\partial G}{\partial y}&
\dfrac{\partial G}{\partial z}
\end{array}
\right)_P
\colon\mathbb A_K^3\longrightarrow\mathbb A_K^2.
$$

Titik $P$ mulus pada kurva tepat apabila matriks tersebut memiliki rank
dua. Dalam keadaan itu, kernelnya berdimensi satu dan mendefinisikan garis
singgung.

<!-- upstream_entity: Algebraische Raumkurven/Schnitt von zwei gleichgroßen Zylindern/Singuläre Punkte/Beispiel -->

### Contoh 24.4: irisan dua silinder {#br-ak-2012-l24-ex-03}

Anggap $\operatorname{char}(K)\ne2$. Pertimbangkan irisan $C$ dari dua
silinder

$$
F=x^2+y^2-1
\qquad\text{dan}\qquad
G=y^2+z^2-1.
$$

Vektor-vektor turunan parsialnya ialah

$$
\partial F=(2x,2y,0)
\qquad\text{dan}\qquad
\partial G=(0,2y,2z).
$$

Suatu titik singular terjadi apabila pemetaan yang didefinisikan oleh
matriks Jacobi ini memiliki rank paling banyak satu, yakni apabila kedua
vektor turunan parsial bergantung linear dan titik tersebut memang terletak
pada varietas terkait. Ketergantungan linear mengharuskan

$$
xy=xz=yz=0.
$$

Pada kurva dengan kedua parameter sama dengan $1$, persamaan kurva
menyingkirkan kasus $x=y=0$ dan $y=z=0$. Jadi kandidat yang tersisa memenuhi

$$
x=z=0,
$$

dan untuk nilai itu kedua vektor memang bergantung linear bagi setiap $y$.
Ketika $x=z=0$, hanya

$$
y=\pm1
$$

yang memberikan titik pada kurva. Jadi, kedua titik itulah tepatnya titik
singular $C$. Keduanya juga merupakan dua titik potong dua lingkaran yang
menjadi komponen-komponen tak tereduksi $C$.

Untuk versi berjari-jari berbeda, tuliskan $r_1,r_2\in K^\times$ sebagai
*kuadrat jari-jari tak nol* dan gunakan

$$
F=x^2+y^2-r_1,
\qquad
G=y^2+z^2-r_2.
$$

Jika besaran yang diberikan adalah jari-jari $\rho_1$ dan $\rho_2$
sendiri, maka $r_i=\rho_i^2$. Syarat ketergantungan
$xy=xz=yz=0$ sekarang harus diselesaikan bersama kedua persamaan kurva.
Pada cabang $x=z=0$, persamaan itu menjadi

$$
y^2=r_1
\qquad\text{dan}\qquad
y^2=r_2.
$$

Jadi cabang ini memaksa $r_1=r_2$. Cabang $x=y=0$ memaksa $r_1=0$,
sedangkan cabang $y=z=0$ memaksa $r_2=0$. Ketiganya mustahil
untuk $r_1,r_2\ne0$ dan $r_1\ne r_2$. Jadi kurva irisan tersebut mulus
apabila kuadrat jari-jarinya tak nol dan berbeda. Untuk silinder real
dengan jari-jari positif, ketaknolannya otomatis.

> **Catatan edisi.** Teks semantik hidup yang dibekukan memakai
> $G=y^2+z^2-1$; PDF historis resmi salah mencetak $G=x^2+z^2-1$. Edisi
> ini mengikuti teks semantik hidup. Sumber juga menyebut $r_1,r_2$
> “jari-jari” tetapi kemudian memakai persamaan $y^2=r_i$; di sini
> parameter itu dijelaskan sebagai kuadrat jari-jari. Syarat ketaknolannya
> juga dibuat eksplisit karena jika $r_1=0$ atau $r_2=0$, peringkat matriks
> Jacobi dapat turun walaupun $r_1\ne r_2$. Asumsi
> $\operatorname{char}(K)\ne2$ dibuat tampak karena semua turunan yang
> ditampilkan akan lenyap dalam karakteristik $2$.

<!-- upstream_entity: Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 24#Potenzreihenringe -->

## Gelanggang deret pangkat {#br-ak-2012-l24-s03}

<!-- upstream_entity: Potenzreihenring/Allgemein und eine Variable/Einführung/Textabschnitt -->

<!-- upstream_entity: Potenzreihenring/Endlich viele Variablen/Formale Potenzreihe/Definition -->

### Definisi 24.5: deret pangkat formal {#br-ak-2012-l24-def-01}

Misalkan $R$ suatu gelanggang komutatif dan $T_1,\ldots,T_n$ sekumpulan
variabel. Suatu *deret pangkat formal* adalah ekspresi berbentuk

$$
F=\sum_\nu a_\nu T^\nu
 =\sum_\nu a_\nu T_1^{\nu_1}\cdots T_n^{\nu_n},
$$

dengan

$$
a_\nu\in R
$$

untuk setiap multiindeks

$$
\nu=(\nu_1,\ldots,\nu_n)\in\mathbb N^n.
$$

Dua deret pangkat dijumlahkan komponen demi komponen dan dikalikan dengan
cara yang sama seperti polinom. Dalam satu variabel,

$$
\begin{aligned}
F\cdot G
&=\left(\sum_{i=0}^{\infty}a_iT^i\right)
  \left(\sum_{j=0}^{\infty}b_jT^j\right)\\
&=\sum_{k=0}^{\infty}c_kT^k,
\end{aligned}
$$

dengan

$$
c_k=\sum_{i=0}^k a_i b_{k-i}.
$$

<!-- upstream_entity: Potenzreihenring/Endlich viele Variablen/Definition -->

### Definisi 24.6: gelanggang deret pangkat {#br-ak-2012-l24-def-02}

Misalkan $R$ suatu gelanggang komutatif. Notasi

$$
R[\![X_1,\ldots,X_n]\!]
$$

menyatakan *gelanggang deret pangkat dalam $n$ variabel*, yang juga disebut
*gelanggang deret pangkat formal dalam $n$ variabel*.

<!-- upstream_entity: Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 24#Potenzreihenringe/zusatz1 -->

Kita terutama akan memakai gelanggang deret pangkat satu variabel
$K[\![T]\!]$ di atas suatu lapangan $K$. Dengan gelanggang ini, kita dapat
menemukan “parametrisasi formal” bagi kurva aljabar sembarang di setiap
titik; hal itu akan dibahas pada kuliah berikutnya. Mula-mula kita perlu
memahami beberapa sifat dasar gelanggang deret pangkat.

<!-- upstream_entity: Formaler Potenzreihenring/Eine Variable/Konstante nicht null, dann Einheit/Fakt -->

### Teorema 24.7: kriteria unit {#br-ak-2012-l24-thm-02}

Misalkan $K$ suatu lapangan. Deret pangkat formal

$$
F=\sum_{n=0}^{\infty}a_nT^n\in K[\![T]\!]
$$

merupakan unit tepat apabila suku konstannya memenuhi $a_0\ne0$.

<!-- upstream_entity: Formaler Potenzreihenring/Eine Variable/Konstante nicht null, dann Einheit/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l24-thm-02-proof}

Syarat tersebut perlu karena evaluasi formal di $T=0$,

$$
\begin{aligned}
\operatorname{ev}_0\colon K[\![T]\!]&\longrightarrow K,\\
F&\longmapsto F(0)=a_0,
\end{aligned}
$$

merupakan homomorfisme gelanggang. Jadi unit harus dikirim ke unsur tak nol
di $K$.

Sebaliknya, andaikan $a_0\ne0$. Kita akan membangun

$$
G=\sum_{j=0}^{\infty}b_jT^j
$$

sedemikian sehingga

$$
FG=\left(\sum_{i=0}^{\infty}a_iT^i\right)
   \left(\sum_{j=0}^{\infty}b_jT^j\right)=1.
$$

Untuk koefisien konstan, kita memerlukan

$$
a_0b_0=1,
$$

yang mempunyai solusi tunggal $b_0=a_0^{-1}$. Secara induktif, andaikan
$b_j$ telah dibangun untuk $j<n$ sehingga semua koefisien $c_k$ dari $FG$
dengan $1\leq k<n$ sama dengan nol. Untuk koefisien ke-$n$, syaratnya ialah

$$
0=c_n=a_0b_n+a_1b_{n-1}+\cdots+a_{n-1}b_1+a_nb_0.
$$

Semua nilai kecuali $b_n$ sudah ditentukan. Karena $a_0\ne0$, persamaan
tersebut mempunyai tepat satu solusi untuk $b_n$. Induksi ini membangun
invers $G$ bagi $F$. $\square$

> **Catatan edisi.** Teks semantik hidup mengakhiri alasan tentang
> homomorfisme suku konstan dengan penanda latihan yang belum terisi.
> Edisi ini tidak mempertahankan rujukan gantung itu;
> evaluasi di $T=0$ dinyatakan dan dipakai secara langsung.

<!-- upstream_entity: Formaler Potenzreihenring/Eine Variable/Diskreter Bewertungsring/Fakt -->

### Korolari 24.8: gelanggang valuasi diskret {#br-ak-2012-l24-cor-01}

Jika $K$ suatu lapangan, maka gelanggang deret pangkat satu variabel

$$
R=K[\![T]\!]
$$

merupakan gelanggang valuasi diskret.

<!-- upstream_entity: Formaler Potenzreihenring/Eine Variable/Diskreter Bewertungsring/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l24-cor-01-proof}

Mula-mula, $R$ adalah gelanggang lokal dengan ideal maksimal

$$
\mathfrak m=(T).
$$

Memang, jika deret pangkat $F$ bukan unit, Teorema 24.7 menyatakan bahwa
suku konstannya nol. Karena itu,

$$
F=T\widetilde F
$$

untuk deret pangkat $\widetilde F$ yang diperoleh dengan menggeser indeks.

Ketiadaan pembagi nol terlihat dari suku awal. Jika $F$ dan $G$ merupakan
deret pangkat tak nol, tuliskan

$$
F=a_kT^k+a_{k+1}T^{k+1}+\cdots
$$

dan

$$
G=b_\ell T^\ell+b_{\ell+1}T^{\ell+1}+\cdots,
$$

dengan $a_k\ne0$ dan $b_\ell\ne0$. Karena semua koefisien sebelumnya nol,
koefisien derajat $k+\ell$ pada hasil kali adalah

$$
c_{k+\ell}=a_kb_\ell\ne0.
$$

Terakhir, $R$ bahkan merupakan domain ideal utama. Untuk ideal tak nol
$I\subseteq R$, ambil $j$ sebagai indeks terkecil dari koefisien tak nol
di antara semua deret dalam $I$. Pilih $H\in I$ dengan suku awal berderajat
$j$. Maka $H=T^jU$ dengan $U$ sebuah unit menurut Teorema 24.7, sehingga
$T^j\in I$. Minimalitas $j$ juga memberi $I\subseteq(T^j)$, jadi

$$
I=(T^j).
$$

Dengan demikian $R$ adalah domain ideal utama lokal dengan ideal maksimal
$(T)$, dan karenanya gelanggang valuasi diskret. $\square$

> **Catatan edisi.** Baik teks semantik hidup maupun PDF historis menulis
> suku kedua $G$ sebagai $a_{\ell+1}T^{\ell+1}$. Indeks keluarga
> koefisien yang benar ialah $b_{\ell+1}$, sebagaimana ditampilkan di atas.

Deret pangkat tidak hanya dapat dijumlahkan dan dikalikan. Dengan syarat
tambahan tertentu, suatu deret pangkat juga dapat disubstitusikan ke dalam
deret pangkat lain. Operasi ini bersesuaian dengan komposisi pemetaan.

<!-- upstream_entity: Formaler Potenzreihenring/Eine Variable/Einsetzen von Potenzreihen mit Konstante null/Definition -->

### Definisi 24.9: substitusi deret pangkat {#br-ak-2012-l24-def-03}

Misalkan $K$ suatu lapangan dan

$$
F=\sum_{i=0}^{\infty}a_iT^i\in K[\![T]\!].
$$

Misalkan pula

$$
G=\sum_{j=0}^{\infty}b_jT^j
$$

suatu deret pangkat dengan suku konstan $b_0=0$. Deret

$$
\begin{aligned}
F(G)
&=a_0+a_1\left(\sum_{j=0}^{\infty}b_jT^j\right)
 +a_2\left(\sum_{j=0}^{\infty}b_jT^j\right)^2\\
&\quad
 +a_3\left(\sum_{j=0}^{\infty}b_jT^j\right)^3+\cdots\\
&=\sum_{k=0}^{\infty}c_kT^k
\end{aligned}
$$

disebut *deret pangkat hasil substitusi*. Koefisiennya ditentukan oleh

$$
c_0=a_0
$$

dan, untuk $k\geq1$,

$$
c_k=\sum_{s=0}^k a_s
\left(
  \sum_{j_1+\cdots+j_s=k}b_{j_1}\cdots b_{j_s}
\right),
$$

dengan jumlah dalam diambil atas semua $s$-tupel terurut

$$
(j_1,\ldots,j_s)\in\mathbb N_+^s.
$$

Karena $b_0=0$, hanya indeks $j\geq1$ yang muncul, sehingga setiap jumlah
yang menentukan suatu koefisien bersifat hingga. Rumus ini berimpit dengan
substitusi polinom biasa ketika $F$ dan $G$ adalah polinom. Substitusi deret
pangkat ke dalam deret pangkat menghasilkan homomorfisme substitusi antara
gelanggang-gelanggang deret pangkat.

<!-- upstream_entity: Formaler Potenzreihenring/Eine Variable/Einsetzen ergibt Ringhomomorphismus/Fakt -->

### Lema 24.10: substitusi adalah homomorfisme {#br-ak-2012-l24-lem-01}

Misalkan $K$ suatu lapangan dan $G\in K[\![S]\!]$ suatu deret pangkat
dengan suku konstan nol. Substitusi oleh $G$ mendefinisikan homomorfisme
$K$-aljabar

$$
\begin{aligned}
K[\![T]\!]&\longrightarrow K[\![S]\!],\\
F&\longmapsto F(G).
\end{aligned}
$$

<!-- upstream_entity: Formaler Potenzreihenring/Eine Variable/Einsetzen ergibt Ringhomomorphismus/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l24-lem-01-proof}

Pemetaan itu terdefinisi dengan baik. Untuk membuktikan bahwa ia merupakan
homomorfisme gelanggang, cukup bandingkan koefisien-koefisien yang sesuai.
Setiap koefisien tersebut hanya bergantung pada sejumlah hingga koefisien
deret-deret yang terlibat. Oleh sebab itu, identitas yang diperlukan
mengikuti dari kasus polinomial. Pemetaan ini juga mempertahankan skalar
$K$, sehingga merupakan homomorfisme $K$-aljabar. $\square$

<!-- upstream_entity: Formaler Potenzreihenring/Eine Variable/T+../Transformierbar auf T/Fakt -->

### Lema 24.11: perubahan parameter formal {#br-ak-2012-l24-lem-02}

Misalkan $K$ suatu lapangan dan

$$
G=\sum_{j=0}^{\infty}b_jT^j\in K[\![T]\!]
$$

dengan $b_0=0$ dan $b_1\ne0$. Maka homomorfisme substitusi yang ditentukan
oleh

$$
T\longmapsto G
$$

merupakan automorfisme $K$-aljabar pada $K[\![T]\!]$.

<!-- upstream_entity: Formaler Potenzreihenring/Eine Variable/T+../Transformierbar auf T/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l24-lem-02-proof}

Pertama-tama kita membangun deret pangkat

$$
F=\sum_{i=0}^{\infty}a_iT^i
$$

dengan

$$
F(G)=T.
$$

Haruslah $a_0=0$ dan $a_1=b_1^{-1}$. Untuk $k\geq2$, andaikan secara induktif bahwa
koefisien-koefisien $F$ sampai $a_{k-1}$ telah dibangun agar koefisien
yang diinginkan terpenuhi. Menurut Definisi 24.9, syarat untuk koefisien
$c_k$ ialah

$$
\begin{aligned}
0=c_k
&=\sum_{s=0}^k a_s
  \left(
    \sum_{j_1+\cdots+j_s=k}b_{j_1}\cdots b_{j_s}
  \right)\\
&=\sum_{s=0}^{k-1}a_s
  \left(
    \sum_{j_1+\cdots+j_s=k}b_{j_1}\cdots b_{j_s}
  \right)
  +a_kb_1^k.
\end{aligned}
$$

Karena $b_1\ne0$, persamaan ini menentukan $a_k$ secara tunggal.

Sekarang pertimbangkan komposisi

$$
K[\![T]\!]
\xrightarrow{\ T\mapsto F\ }
K[\![T]\!]
\xrightarrow{\ T\mapsto G\ }
K[\![T]\!].
$$

Komposisi totalnya ialah homomorfisme substitusi $T\mapsto T$, yaitu
identitas. Karena itu, pemetaan kedua, yang ditentukan oleh $T\mapsto G$,
surjektif. Menurut Korolari 24.8, $K[\![T]\!]$ merupakan gelanggang valuasi
diskret, dan ideal-idealnya telah diketahui. Jika kernel pemetaan kedua
tak nol, kernel itu memuat suatu $T^j$; tetapi citranya adalah $G^j\ne0$.
Maka hanya ideal nol yang mungkin menjadi kernel. Pemetaan tersebut juga
injektif, sehingga bijektif dan merupakan automorfisme $K$-aljabar.
$\square$
