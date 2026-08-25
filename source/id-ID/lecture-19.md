---
title: "Kuliah 19 - Penyajian sebagai Gelanggang Faktor dan Keintegralan"
stable_id: br-ak-2025-2026-l19
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 19"
upstream_pageid: 165908
upstream_revid: 1051386
upstream_timestamp: "2025-08-18T08:16:13Z"
upstream_mediawiki_sha1: d256e22d3ab01cb721aa6dd2162e54aebd5789c1
source_url: "https://de.wikiversity.org/w/index.php?oldid=1051386"
authority_manifest: authority/wikiversity/unit-19/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 52245060a54f973b4fba19878eec234904430b9e5058defdbd9feaa7a868080e
lecture_xml_sha256: 850f012e21ac7a2045dfe0ae1e4c77878ca6aab9f42b02ea3a48564f0c808430
lecture_expanded_tex_sha256: 8d6d6bad20f9d4e6a5321a4add51b32416bf1d04c7ed857c080fb2439628974d
license: "CC BY-SA 4.0 for translated course text; the figure retains CC BY 3.0 component rights in authority/RIGHTS-unit-19.csv"
translation_status: complete
---

# Kuliah 19: Penyajian sebagai Gelanggang Faktor dan Keintegralan {#br-ak-2025-2026-l19}

## Penyajian gelanggang koordinat kurva monomial sebagai gelanggang faktor {#br-ak-2025-2026-l19-s01}

Misalkan

$$
M\subseteq\mathbb N
$$

monoid numerik yang dibangkitkan oleh bilangan-bilangan asli
$e_1,\ldots,e_n$ dengan $\gcd(e_1,\ldots,e_n)=1$. Surjeksi yang terkait

$$
\mathbb N^n\longrightarrow M\subseteq\mathbb N
$$

menghasilkan surjeksi

$$
\begin{aligned}
K[X_1,\ldots,X_n]&\longrightarrow K[M],\\
X_i&\longmapsto T^{e_i},
\end{aligned}
$$

dan pembenaman tertutup

$$
C=K\!-\!\operatorname{Spek}(K[M])\hookrightarrow\mathbb A_K^n.
$$

Dengan persamaan apa kurva $C$ dapat dideskripsikan?

<!-- upstream_entity: Affine Kurven/Monomiale Kurven/Beschreibende binomiale Gleichungen/Fakt -->

### Teorema: persamaan binomial yang mendeskripsikan kurva {#br-ak-2025-2026-l19-thm-01}

Misalkan $M\subseteq\mathbb N$ submonoid yang dibangkitkan oleh
$e_1,\ldots,e_n$ dengan $\gcd(e_1,\ldots,e_n)=1$, dan misalkan

$$
\mathbb N^n\longrightarrow M
$$

pemetaan surjektif yang terkait, dengan homomorfisme faktor

$$
\varphi:K[X_1,\ldots,X_n]\longrightarrow K[M].
$$

Maka ideal kernel dideskripsikan oleh

$$
\ker\varphi=
\left(
\prod_{i\in I_1}X_i^{r_i}-\prod_{i\in I_2}X_i^{s_i}
\mathrel{\Bigg|}
\begin{array}{l}
I_1,I_2\subseteq\{1,\ldots,n\}\text{ saling lepas},\\
\displaystyle\sum_{i\in I_1}r_ie_i=
\sum_{i\in I_2}s_ie_i,\\
r_i,s_i\geq1
\end{array}
\right).
$$

#### Bukti {#br-ak-2025-2026-l19-thm-01-proof}

Bahwa unsur-unsur yang ditampilkan berada dalam ideal kernel langsung
mengikuti dari

$$
\begin{aligned}
\varphi\left(\prod_{i\in I_1}X_i^{r_i}\right)
&=\prod_{i\in I_1}\left(T^{e_i}\right)^{r_i}\\
&=T^{\sum_{i\in I_1}r_ie_i}.
\end{aligned}
$$

**Catatan edisi:** pada baris ini sumber beralih dari variabel $T$ yang
ditetapkan dalam homomorfisme ke huruf kecil $t$. Edisi ini mempertahankan
satu variabel $T$ secara konsisten; tidak ada isi matematis yang berubah.

Untuk arah sebaliknya, misalkan

$$
F\in K[X_1,\ldots,X_n]
$$

suatu polinom dengan $\varphi(F)=0$. Tuliskan

$$
F=\sum_\nu a_\nu X^\nu,
\qquad
\nu=(\nu_1,\ldots,\nu_n).
$$

Maka

$$
\begin{aligned}
\varphi(F)
&=\sum_\nu a_\nu T^{\sum_{i=1}^n\nu_ie_i}\\
&=\sum_{k\geq0}
\left(
\sum_{\nu:\,\sum_{i=1}^n\nu_ie_i=k}a_\nu
\right)T^k.
\end{aligned}
$$

**Catatan edisi:** sumber menulis batas penjumlahan `\sum_{k=0}` tanpa
batas atas. Karena $F$ adalah polinom dan baris ini mengelompokkan suku menurut bobot tak
negatif $k$, edisi menulis $\sum_{k\geq0}$; hanya notasi yang dilengkapi.

Karena polinom ini sama dengan nol, semua koefisiennya nol. Jadi, untuk
setiap $k$, polinom

$$
F_k=
\sum_{\nu:\,\sum_{i=1}^n\nu_ie_i=k}a_\nu X^\nu
$$

juga berada dalam kernel. Karena itu kita boleh menganggap bahwa $F$ hanya
memuat monomial-monomial $X^\nu$ dengan nilai yang sama

$$
\sum_{i=1}^n\nu_ie_i=k.
$$

Ambil salah satu monomial $X^\nu$ yang muncul dalam $F$, dengan $a_\nu\ne0$.
Setidaknya satu monomial lain, katakanlah $X^\mu$, juga harus muncul, karena
satu monomial saja tidak dipetakan ke nol. Kita tulis

$$
F=a_\nu(X^\nu-X^\mu)
+\left(F-a_\nu X^\nu+a_\nu X^\mu\right).
$$

Monomial $X^\nu$ tidak lagi muncul dalam suku di sebelah kanan, dan tidak ada
monomial baru yang ditambahkan. Dari $X^\nu-X^\mu$ kita dapat memfaktorkan
semua variabel yang muncul pada kedua sisi sejauh mungkin, sehingga diperoleh

$$
X^\nu-X^\mu
=X_1^{b_1}\cdots X_n^{b_n}
\left(
\prod_{i\in I_1}X_i^{r_i}
-\prod_{i\in I_2}X_i^{s_i}
\right),
$$

dengan $I_1$ dan $I_2$ saling lepas serta

$$
\sum_{i\in I_1}e_ir_i=\sum_{i\in I_2}e_is_i.
$$

Jadi suku pertama dalam penyajian $F$ di atas berada dalam ideal yang
dibangkitkan oleh binomial-binomial yang dinyatakan. Kita dapat melanjutkan
dengan suku kedua, yang memuat satu monomial lebih sedikit. Proses ini berakhir
dan membuktikan klaim.

Persamaan-persamaan dalam teorema di atas disebut *persamaan binomial*.
Persamaan binomial yang paling sederhana berbentuk

$$
X_i^{e_j/\gcd(e_i,e_j)}
=X_j^{e_i/\gcd(e_i,e_j)},
\qquad i\ne j.
$$

Untuk kurva monomial bidang, ini juga merupakan satu-satunya persamaan.

<!-- upstream_entity: Ebene affine Kurven/Monomiale Kurve/Beschreibende Gleichung/Fakt -->

### Korolari: persamaan kurva monomial bidang {#br-ak-2025-2026-l19-cor-01}

Misalkan $C$ kurva monomial bidang yang diberikan oleh

$$
t\longmapsto(t^{e_1},t^{e_2})=(x,y),
$$

dengan $e_1$ dan $e_2$ saling prima. Maka

$$
C=V(X^{e_2}-Y^{e_1}).
$$

#### Bukti {#br-ak-2025-2026-l19-cor-01-proof}

Pernyataan ini langsung mengikuti dari Teorema 19.1.

Untuk kurva monomial ruang, persamaan-persamaan yang mendeskripsikannya juga
masih dapat ditentukan dengan cukup mudah, karena selalu mungkin mengisolasi
satu variabel.

<!-- upstream_entity: Algebraische Raumkurven/Gedrehte Kubik/Projektionen auf Ebenen/Beispiel -->

### Contoh: kurva kubik terpilin {#br-ak-2025-2026-l19-exa-01}

![Kurva ruang hijau yang berpilin pada dua permukaan tembus pandang di dalam kotak tiga dimensi](authority/assets/Twisted_cubic_curve.png)

*Kurva kubik terpilin. Claudio Rocchini,
[CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). Sumber kuliah
memberi label sebaris CC BY-SA 3.0, sedangkan metadata Commons yang dibekukan
menyediakan opsi CC BY 3.0 yang digunakan untuk komponen ini.*

Misalkan

$$
C\subset\mathbb A_K^3
$$

adalah *kurva kubik terpilin*, yaitu citra pemetaan monomial

$$
t\longmapsto(t,t^2,t^3).
$$

Kurva ini isomorfik dengan garis afin dan, khususnya, mulus. Menurut Teorema
19.1, ideal yang mendeskripsikannya ialah

$$
\begin{aligned}
\mathfrak a
&=(Y-X^2,Z-X^3,Y^3-Z^2,Z-XY)\\
&=(Y-X^2,Z-X^3).
\end{aligned}
$$

Dua pembangkit ideal terakhir berlebih, sebab keduanya dapat dinyatakan
melalui dua pembangkit lainnya. Jadi

$$
C=V(Y-X^2,Z-X^3).
$$

Citra $C$ di bawah tiga proyeksi yang berbeda adalah

$$
C_1=V(Z^2-Y^3),\qquad
C_2=V(Z-X^3),\qquad
C_3=V(Y-X^2).
$$

Kurva $C_2$ dan $C_3$ isomorfik dengan garis afin, sebagai grafik suatu
pemetaan, sedangkan $C_1$ adalah parabola Neil yang singular.

<!-- upstream_entity: Affine monomiale Raumkurve/3 4 5/Beschreibung mit Gleichungen/Beispiel -->

### Contoh: kurva monomial dengan eksponen 3, 4, dan 5 {#br-ak-2025-2026-l19-exa-02}

Misalkan $C$ kurva monomial yang diberikan oleh

$$
t\longmapsto(t^3,t^4,t^5)=(x,y,z).
$$

Untuk masing-masing dari ketiga variabel, menurut Teorema 19.1 kita harus
menentukan pangkat yang, setelah pangkat-pangkat $t$ disubstitusikan, juga
dapat dinyatakan sebagai monomial dalam dua variabel lainnya.

Pertama-tama, persamaan-persamaan yang hanya melibatkan dua variabel adalah

$$
Y^3=X^4,\qquad Z^3=X^5,\qquad Z^4=Y^5.
$$

Seperti dalam kasus bidang, untuk setiap pasangan variabel hanya mungkin ada
satu relasi dasar.

Dalam relasi yang melibatkan ketiga variabel, salah satu variabel muncul
sendiri pada satu sisi. Mulailah dengan $X$. Pangkat $X$ dan $X^2$ belum
dapat dinyatakan melalui variabel lain, tetapi

$$
X^3=T^9=YZ.
$$

Tidak mungkin ada kombinasi lain yang bebas dari relasi ini. Secara umum,
suatu penyajian ganda

$$
X^k=Y^iZ^j=Y^aZ^b
$$

menghasilkan relasi antara pangkat $Y$ dan pangkat $Z$, setelah pangkat yang
lebih kecil dicoret. Karena semua relasi yang hanya melibatkan dua variabel
sudah dicantumkan, setiap pangkat $X$ menghasilkan paling banyak satu relasi
baru.

Kita sudah selesai untuk relasi dengan $X$ sendirian. Memang, jika

$$
X^k=Y^iZ^j,
$$

maka $k\geq3$. Jika $i=0$ atau $j=0$, relasinya sudah tercantum. Jadi anggap
$i,j\geq1$. Dengan persamaan $X^3=YZ$, eksponen-eksponen dalam persamaan itu
dapat diperkecil: kurangi eksponen $X$ sebesar $3$ dan masing-masing eksponen
$Y$ dan $Z$ sebesar $1$.

Untuk $Y$ kita langsung memperoleh

$$
Y^2=ZX,
$$

yang kembali mereduksi semua persamaan lainnya. Untuk $Z$ kita memperoleh

$$
Z^2=X^2Y
$$

dan

$$
Z^3=XY^3.
$$

Tidak ada monomial yang lebih kecil dalam $X$ dan $Y$ yang dapat dinyatakan
sebagai pangkat $Z$. Karena itu setiap relasi lain dapat dikembalikan pada
salah satu relasi sebelumnya.

Secara keseluruhan, kurva $C$ mempunyai penyajian

$$
C=V(Y^3-X^4,\ Z^3-X^5,\ Z^4-Y^5,\ X^3-YZ,\ Y^2-XZ,\ Z^2-X^2Y,\ Z^3-XY^3).
$$

**Catatan edisi:** dalam daftar terakhir ini sumber memasukkan
`\mathdisplaybruch X^3-YZ`, yaitu pemanggilan makro pecahan tanpa argumen
berkurung. Edisi menampilkan relasi yang sudah dinyatakan dan dibuktikan tepat
sebelumnya, $X^3-YZ$.

## Keintegralan {#br-ak-2025-2026-l19-s02}

<!-- upstream_entity: Kommutative Ringtheorie/Ganzheit/Ganzheitsgleichung/Definition -->

### Definisi: persamaan keintegralan {#br-ak-2025-2026-l19-def-01}

Misalkan $R$ dan $S$ gelanggang-gelanggang komutatif dan

$$
R\subseteq S
$$

suatu perluasan gelanggang. Untuk $x\in S$, persamaan berbentuk

$$
x^n+r_{n-1}x^{n-1}+r_{n-2}x^{n-2}+\cdots+r_1x+r_0=0,
$$

dengan $r_i\in R$ untuk $i=0,\ldots,n-1$, disebut *persamaan keintegralan*
untuk $x$.

<!-- upstream_entity: Kommutative Ringtheorie/Ganzheit/Ganzes Element/Definition -->

### Definisi: unsur integral {#br-ak-2025-2026-l19-def-02}

Misalkan $R\subseteq S$ suatu perluasan gelanggang komutatif. Unsur $x\in S$
disebut *integral atas $R$* jika $x$ memenuhi suatu persamaan keintegralan
dengan koefisien dalam $R$.

<!-- upstream_entity: Kommutative Ringtheorie/Ganzheit/Ganzer Abschluss/Definition -->

### Definisi: penutupan integral {#br-ak-2025-2026-l19-def-03}

Misalkan $R\subseteq S$ suatu perluasan gelanggang komutatif. Himpunan semua
unsur $x\in S$ yang integral atas $R$ disebut *penutupan integral* $R$ di
dalam $S$.

<!-- upstream_entity: Kommutative Ringtheorie/Ganzheit/Ganze Algebra/Definition -->

### Definisi: perluasan integral {#br-ak-2025-2026-l19-def-04}

Misalkan $R\subseteq S$ suatu perluasan gelanggang komutatif. Gelanggang $S$
disebut *integral atas $R$*, dan $R\subseteq S$ disebut *perluasan gelanggang
integral*, jika setiap $x\in S$ integral atas $R$.

Gelanggang $S$ integral atas $R$ jika dan hanya jika penutupan integral $R$
di dalam $S$ sama dengan $S$.

<!-- upstream_entity: Kommutative Ringtheorie/Ganzheit/Ganzes Element/Charakterisierung/Fakt -->

### Lema: karakterisasi unsur integral {#br-ak-2025-2026-l19-lem-01}

Misalkan $R\subseteq S$ suatu perluasan gelanggang komutatif. Untuk suatu
unsur $x\in S$, pernyataan-pernyataan berikut ekuivalen.

1. Unsur $x$ integral atas $R$.
2. Terdapat subaljabar-$R$ $T$ dari $S$ yang memuat $x$ dan dibangkitkan
   secara hingga sebagai modul-$R$.
3. Terdapat submodul-$R$ $M$ dari $S$ yang dibangkitkan secara hingga,
   memuat suatu unsur bukan pembagi nol di $S$, dan memenuhi $xM\subseteq M$.

#### Bukti {#br-ak-2025-2026-l19-lem-01-proof}

**(1) $\Rightarrow$ (2).** Tinjau subaljabar-$R$ dari $S$ yang dibangkitkan
oleh pangkat-pangkat $x$,

$$
R[x].
$$

Subaljabar ini terdiri atas semua ekspresi polinomial dalam $x$ dengan
koefisien di $R$. Dari suatu persamaan keintegralan

$$
x^n+r_{n-1}x^{n-1}+r_{n-2}x^{n-2}+\cdots+r_1x+r_0=0
$$

diperoleh

$$
x^n=-r_{n-1}x^{n-1}-r_{n-2}x^{n-2}-\cdots-r_1x-r_0.
$$

Jadi $x^n$ dapat dinyatakan sebagai ekspresi polinomial berderajat lebih
kecil. Dengan mengalikan persamaan terakhir ini dengan $x^i$, setiap pangkat
$x$ dengan eksponen sekurang-kurangnya $n$ dapat diganti oleh ekspresi
polinomial berderajat lebih kecil. Akhirnya semua pangkat tersebut dapat
dinyatakan dengan derajat paling besar $n-1$. Dengan demikian

$$
R[x]=R+Rx+Rx^2+\cdots+Rx^{n-2}+Rx^{n-1},
$$

dan $x^0=1,x,x^2,\ldots,x^{n-1}$ merupakan sistem pembangkit berhingga untuk
modul-$R$ $T=R[x]$.

**(2) $\Rightarrow$ (3).** Misalkan

$$
x\in T\subseteq S,
$$

dengan $T$ subaljabar-$R$ yang dibangkitkan secara hingga sebagai
modul-$R$. Maka $xT\subseteq T$, dan $T$ memuat unsur bukan pembagi nol $1$.

**(3) $\Rightarrow$ (1).** Misalkan $M\subseteq S$ submodul-$R$ yang
dibangkitkan secara hingga dan memenuhi $xM\subseteq M$, lalu pilih
pembangkit $y_1,\ldots,y_n$ bagi $M$. Untuk setiap $i$, unsur $xy_i$ merupakan
kombinasi linear-$R$ dari $y_j$, sehingga

$$
xy_i=\sum_{j=1}^n r_{ij}y_j,
\qquad r_{ij}\in R.
$$

Dalam bentuk matriks,

$$
x
\begin{pmatrix}
y_1\\y_2\\\vdots\\y_n
\end{pmatrix}
=
\begin{pmatrix}
r_{1,1}&r_{1,2}&\cdots&r_{1,n}\\
r_{2,1}&r_{2,2}&\cdots&r_{2,n}\\
\vdots&\vdots&\ddots&\vdots\\
r_{n,1}&r_{n,2}&\cdots&r_{n,n}
\end{pmatrix}
\begin{pmatrix}
y_1\\y_2\\\vdots\\y_n
\end{pmatrix}.
$$

Jadi

$$
0=
\underbrace{
\begin{pmatrix}
x-r_{1,1}&-r_{1,2}&\cdots&-r_{1,n}\\
-r_{2,1}&x-r_{2,2}&\cdots&-r_{2,n}\\
\vdots&\vdots&\ddots&\vdots\\
-r_{n,1}&-r_{n,2}&\cdots&x-r_{n,n}
\end{pmatrix}}_{A}
\begin{pmatrix}
y_1\\y_2\\\vdots\\y_n
\end{pmatrix}.
$$

Entri-entri matriks $A$ berada di $S$. Jika $A^{\operatorname{adj}}$ adalah matriks adjugat (adjoin klasik) dari
$A$, maka

$$
A^{\operatorname{adj}}Ay=0,
$$

dengan $y=(y_1,\ldots,y_n)^{\mathsf T}$. Menurut identitas adjugat,

$$
A^{\operatorname{adj}}A=(\det A)I_n,
$$

sehingga

$$
((\det A)I_n)y=0.
$$

Jadi $(\det A)y_j=0$ untuk setiap $j$, dan karena itu

$$
(\det A)z=0
$$

untuk setiap $z\in M$. Menurut asumsi, $M$ memuat suatu unsur bukan pembagi
nol di $S$; akibatnya $\det A=0$. Akan tetapi, determinan ini merupakan
ekspresi polinomial monik dalam $x$ berderajat $n$. Jadi $x$ memenuhi suatu
persamaan keintegralan.

<!-- upstream_entity: Kommutative Ringtheorie/Ganzheit/Ganzer Abschluss/Ring/Fakt -->

### Korolari: penutupan integral merupakan subaljabar {#br-ak-2025-2026-l19-cor-02}

Misalkan $R\subseteq S$ suatu perluasan gelanggang komutatif. Penutupan
integral $R$ di dalam $S$ merupakan subaljabar-$R$ dari $S$.

#### Bukti {#br-ak-2025-2026-l19-cor-02-proof}

Persamaan keintegralan $X-r=0$, untuk $r\in R$, menunjukkan bahwa setiap unsur
$R$ integral atas $R$. Misalkan $x_1,x_2\in S$ integral atas $R$. Menurut
karakterisasi keintegralan, terdapat subaljabar-subaljabar-$R$

$$
T_1,T_2\subseteq S
$$

dengan $x_1\in T_1$ dan $x_2\in T_2$ yang masing-masing dibangkitkan secara hingga sebagai modul-$R$. Misalkan $y_1,\ldots,y_n$ sistem
pembangkit-$R$ bagi $T_1$, dan $z_1,\ldots,z_m$ sistem pembangkit-$R$ bagi
$T_2$. Kita dapat menganggap $y_1=z_1=1$.

Tinjau modul-$R$ yang dibangkitkan secara hingga

$$
T=T_1T_2
=\left\langle y_iz_j\mathrel{\Big|}
i=1,\ldots,n,\ j=1,\ldots,m\right\rangle.
$$

Modul ini jelas memuat $x_1+x_2$, $x_1x_2$, dan $1$. Modul-$R$ $T$ juga
merupakan aljabar-$R$. Memang, untuk dua unsur sebarang,

$$
\left(\sum r_{ij}y_iz_j\right)
\left(\sum s_{k\ell}y_kz_\ell\right)
=\sum r_{ij}s_{k\ell}y_iy_kz_jz_\ell,
$$

dan $y_iy_k\in T_1$ serta $z_jz_\ell\in T_2$, sehingga kombinasi linear ini
berada dalam $T$.

Karena itu jumlah dan hasil kali dua unsur integral kembali integral. Jadi
penutupan integral adalah subgelanggang $S$ yang memuat $R$, yaitu suatu
subaljabar-$R$.

<!-- upstream_entity: Kommutative Ringtheorie/Ganzheit/Ganz-abgeschlossen/Definition -->

### Definisi: tertutup secara integral {#br-ak-2025-2026-l19-def-05}

Misalkan $R\subseteq S$ suatu perluasan gelanggang komutatif. Gelanggang $R$
disebut *tertutup secara integral di dalam $S$* jika penutupan integral $R$ di
dalam $S$ sama dengan $R$.

---

**Provenans edisi.** Terjemahan dan produksi pembaca: OpenAI Codex
gpt-5.6-sol, Ultra. Sumber, pengarang, dan lisensi komponen dipertahankan
seperti dinyatakan dalam metadata dan berkas hak edisi.
