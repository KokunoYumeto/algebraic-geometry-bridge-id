---
title: "Kuliah 23 - Ruang Kotangen dan Multiplisitas Hilbert-Samuel"
stable_id: br-ak-2025-2026-l23
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 23"
upstream_pageid: 165912
upstream_revid: 1112318
upstream_timestamp: "2026-08-21T09:42:07Z"
upstream_mediawiki_sha1: a38160a106cf39298b3f2cb23f7880e05a5a86f7
source_url: "https://de.wikiversity.org/w/index.php?oldid=1112318"
authority_manifest: authority/wikiversity/unit-23/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: f7ee49a4bfa589b831c1fdb69e6f091ac1762d9da019a133670e4e0d723d34ae
lecture_xml_sha256: e03f37dab14063c982dec993e0da4dd94e9e4cbdf9b73b38ad4c77a63dd83116
lecture_expanded_tex_sha256: 17aa88b5aa9a8d130f0995c036cb9ca332ef1b0feaef3b2d5ac5396e47b343a0
license: "CC BY-SA 4.0"
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_semantic_entities: 17
source_corrections: 3
reader_media_positions: 0
---

# Kuliah 23: Ruang Kotangen dan Multiplisitas Hilbert-Samuel {#br-ak-2025-2026-l23}

## Interpretasi sebagai ruang kotangen {#br-ak-2025-2026-l23-s01}

Kita tambahkan alasan mengapa $\mathfrak m/\mathfrak m^2$ layak disebut
*ruang kotangen*. Dari analisis diketahui bahwa, untuk suatu titik
$P\in M$ pada manifold $M$ dan suatu fungsi terdiferensialkan
$f:M\longrightarrow\mathbb R$, diferensial

$$
df:T_PM\longrightarrow\mathbb R
$$

bersifat linear. Jadi, $df$ merupakan unsur ruang kotangen $T_P^*M$.
Pemetaan keseluruhan

$$
C^1(M,\mathbb R)\longrightarrow T_P^*M,
\qquad f\longmapsto df,
$$

merupakan suatu derivasi: ia memenuhi aturan Leibniz

$$
d(fg)=f\,dg+g\,df.
$$

Kita sekarang memperkenalkan konsep aljabarnya.

<!-- upstream_entity: Algebraische Derivation/Definition -->

### Definisi: derivasi aljabar {#br-ak-2025-2026-l23-def-01}

Misalkan $R$ suatu gelanggang komutatif, $A$ suatu aljabar komutatif atas
$R$, dan $M$ suatu modul-$A$. Suatu pemetaan linear-$R$

$$
\delta:A\longrightarrow M
$$

disebut *derivasi-$R$* dengan nilai di $M$ jika

$$
\delta(ab)=a\delta(b)+b\delta(a)
$$

untuk semua $a,b\in A$.

<!-- upstream_entity: K-Algebra/Algebraischer Kotangentialraum an K-Punkt/Direkte Derivation/Fakt -->

### Teorema: derivasi kanonik menuju ruang kotangen {#br-ak-2025-2026-l23-thm-01}

Misalkan $K$ suatu lapangan, $R$ suatu aljabar bertipe hingga atas $K$, dan

$$
P\in K\!-\!\operatorname{Spek}(R)
$$

suatu titik dengan ideal maksimal terkait $\mathfrak m$. Maka pemetaan

$$
\begin{aligned}
d:R&\longrightarrow\mathfrak m/\mathfrak m^2,\\
f&\longmapsto d f:=\overline{f-f(P)}
\end{aligned}
$$

merupakan suatu derivasi-$K$.

<!-- upstream_entity: K-Algebra/Algebraischer Kotangentialraum an K-Punkt/Direkte Derivation/Fakt/Beweis -->

### Bukti {#br-ak-2025-2026-l23-prf-01}

Terdapat isomorfisme kanonik $K\longrightarrow R/\mathfrak m$ antara
lapangan dasar dan lapangan residu. Pemetaan $d$ terdefinisi dengan baik
karena

$$
(f-f(P))(P)=0,
$$

sehingga $f-f(P)\in\mathfrak m$. Linearitas-$K$ langsung diperoleh. Untuk
aturan hasil kali, semua kesamaan berikut dipahami di dalam
$\mathfrak m/\mathfrak m^2$:

$$
\begin{aligned}
d(fg)
&=\overline{fg-f(P)g(P)}\\
&=\overline{fg-f(P)g(P)+(f-f(P))(g-g(P))}\\
&=\overline{f(g-g(P))+g(f-f(P))}\\
&=f\,dg+g\,df.
\end{aligned}
$$

Pada langkah kedua ditambahkan suatu unsur $\mathfrak m^2$, yang kelasnya
nol dalam hasil bagi. Ini membuktikan aturan Leibniz. $\square$

*Catatan edisi -- penjelasan notasi sumber:* Sumber menuliskan rantai di atas
tanpa garis kelas pada setiap suku. Kesamaan tersebut adalah kesamaan modulo
$\mathfrak m^2$, bukan kesamaan polinom di $R$.

## Titik mulus dan titik normal {#br-ak-2025-2026-l23-s02}

Kita akan menunjukkan bahwa suatu titik pada kurva aljabar bidang bersifat
mulus tepat ketika gelanggang lokal terkait merupakan gelanggang valuasi
diskret. Kemulusan di suatu titik mula-mula didefinisikan secara ekstrinsik
dengan merujuk pada bidang ambien, sedangkan sifat menjadi gelanggang valuasi
diskret hanya bergantung pada gelanggang koordinat kurva. Lema berikut
menangani satu arah. Untuk arah lainnya, kita terlebih dahulu mengembangkan
multiplisitas intrinsik bagi gelanggang lokal.

<!-- upstream_entity: Ebene algebraische Kurve/Glatter Punkt/Lokaler Ring ist diskreter Bewertungsring/Fakt -->

### Lema: titik mulus menghasilkan gelanggang valuasi diskret {#br-ak-2025-2026-l23-lem-01}

Misalkan $K$ suatu lapangan, $F\in K[X,Y]$ suatu polinom tak nol tanpa faktor
berulang, dan

$$
P\in C=V(F)
$$

suatu titik mulus pada kurva tersebut. Jika $R$ adalah gelanggang lokal kurva
di $P$, maka $R$ merupakan gelanggang valuasi diskret.

<!-- upstream_entity: Ebene algebraische Kurve/Glatter Punkt/Lokaler Ring ist diskreter Bewertungsring/Fakt/Beweis -->

### Bukti {#br-ak-2025-2026-l23-prf-02}

Mula-mula, $R$ adalah gelanggang lokal Noether dan, menurut Lema 22.12,
merupakan domain integral. Karena itu, satu-satunya ideal prima $R$ ialah
ideal nol dan ideal maksimal $\mathfrak m_P$. Kita akan menunjukkan bahwa
ideal maksimal tersebut merupakan ideal utama.

Kita boleh menganggap $P$ sebagai titik asal dan menulis

$$
F=F_d+\cdots+F_1,
\qquad F_1\ne0,
$$

dengan setiap $F_i$ homogen berderajat $i$. Karena $P$ mulus, bentuk ini
memiliki suku linear tak nol. Melalui perubahan variabel linear, kita dapat
mengatur agar $F_1=Y$. Kumpulkan semua pangkat $X$ yang berdiri sendiri,
yaitu monom yang tidak mengandung $Y$, lalu keluarkan faktor $Y$ dari
suku-suku lainnya. Persamaan $F=0$ dapat ditulis sebagai

$$
Y(1+G)=XH(X),
\qquad G\in(X,Y).
$$

Unsur $1+G$ merupakan satuan dalam $K[X,Y]_{(X,Y)}$, dan karenanya juga
dalam gelanggang lokal kurva di titik asal,

$$
R=K[X,Y]_{(X,Y)}/(F).
$$

Di dalam $R$ berlaku

$$
Y=\frac{H}{1+G}X.
$$

Jadi ideal maksimal $R$ dibangkitkan oleh $X$ saja. Berdasarkan Teorema
21.8, $R$ merupakan gelanggang valuasi diskret. $\square$

## Multiplisitas Hilbert-Samuel {#br-ak-2025-2026-l23-s03}

<!-- upstream_entity: Noetherscher lokaler Ring/Potenzen vom maximalen Ideal/Restklassenring und Jets sind endlich-dimensional/Fakt -->

### Lema: hasil bagi oleh pangkat ideal maksimal berdimensi hingga {#br-ak-2025-2026-l23-lem-02}

Misalkan $R$ suatu gelanggang lokal Noether dengan ideal maksimal
$\mathfrak m$ dan lapangan residu

$$
K=R/\mathfrak m.
$$

Maka modul faktor $\mathfrak m^n/\mathfrak m^{n+1}$ berdimensi hingga atas
$K$. Jika $R$ memuat suatu lapangan $K$ yang dipetakan secara isomorfik ke
lapangan residu, gelanggang faktor $R/\mathfrak m^n$ juga berdimensi hingga
atas $K$.

<!-- upstream_entity: Noetherscher lokaler Ring/Potenzen vom maximalen Ideal/Restklassenring und Jets sind endlich-dimensional/Fakt/Beweis -->

### Bukti {#br-ak-2025-2026-l23-prf-03}

Kita menulis

$$
\mathfrak m^n/\mathfrak m^{n+1}
\cong
\mathfrak m^n/(\mathfrak m^n)\mathfrak m.
$$

Ini adalah situasi Lema 22.2. Karena $\mathfrak m^n$ merupakan ideal yang
dibangkitkan secara hingga, modul faktor tersebut berdimensi hingga atas
lapangan residu.

Untuk gelanggang faktor, tinjau barisan eksak pendek modul-$R$

$$
0\longrightarrow
\mathfrak m^n/\mathfrak m^{n+1}
\longrightarrow R/\mathfrak m^{n+1}
\longrightarrow R/\mathfrak m^n
\longrightarrow0.
$$

Berdasarkan hipotesis tambahan, ini juga merupakan barisan eksak pendek
ruang vektor-$K$, sehingga dimensi-dimensinya dapat dijumlahkan. Ruang di
kiri berdimensi hingga menurut bagian yang baru dibuktikan. Induksi atas $n$
sekarang memberi hasil yang diinginkan, dengan kasus awal
$R/\mathfrak m=K$. $\square$

Untuk suatu kurva aljabar bidang

$$
V=V(F)\subseteq\mathbb A_K^2
$$

dan titik $P=(a,b)\in V$, gelanggang lokalnya ialah

$$
K[X,Y]_{(X-a,Y-b)}/(F).
$$

Lapangan residunya adalah $K$ sendiri. Dengan demikian, semua hipotesis Lema
23.4 terpenuhi dan semua dimensi berikut adalah dimensi atas lapangan dasar.

<!-- upstream_entity: Ebene algebraische Kurve/Multiplizität über Hilbert-Samuel Polynom/Fakt -->

### Teorema: multiplisitas melalui fungsi Hilbert-Samuel {#br-ak-2025-2026-l23-thm-02}

Misalkan

$$
P\in V=V(F)\subseteq\mathbb A_K^2
$$

suatu titik pada kurva afin bidang. Misalkan

$$
R=\mathcal O_{V,P}
$$

gelanggang lokal terkait, dengan ideal maksimal $\mathfrak m$. Maka
multiplisitas $m_P$ dari $P$ memenuhi

$$
m_P=\dim_K\left(\mathfrak m^n/\mathfrak m^{n+1}\right)
$$

untuk semua $n$ yang cukup besar.

<!-- upstream_entity: Ebene algebraische Kurve/Multiplizität über Hilbert-Samuel Polynom/Fakt/Beweis -->

### Bukti {#br-ak-2025-2026-l23-prf-04}

Tinjau barisan eksak pendek ruang vektor-$K$

$$
0\longrightarrow
\mathfrak m^n/\mathfrak m^{n+1}
\longrightarrow R/\mathfrak m^{n+1}
\longrightarrow R/\mathfrak m^n
\longrightarrow0.
$$

Menurut Lema 23.4, semua dimensinya hingga. Pernyataan bahwa dimensi
$\mathfrak m^n/\mathfrak m^{n+1}$ akhirnya konstan dan sama dengan
multiplisitas ekuivalen dengan pernyataan bahwa selisih

$$
\dim_K(R/\mathfrak m^{n+1})-\dim_K(R/\mathfrak m^n)
$$

akhirnya konstan dan sama dengan multiplisitas. Melalui induksi, hal itu
ekuivalen dengan adanya suatu konstanta $c$ sehingga

$$
\dim_K(R/\mathfrak m^n)=m_Pn+c
$$

untuk $n$ yang cukup besar.

Setelah melakukan translasi, kita boleh menganggap $P$ sebagai titik asal.
Tetapkan

$$
\mathfrak a=(X,Y)\subseteq S=K[X,Y].
$$

Kemudian

$$
K[X,Y]/(\mathfrak a^n+(F))=R/\mathfrak m^n,
$$

sehingga cukup membuktikan pernyataan bagi hasil bagi di kiri. Berdasarkan
hipotesis, $F$ mempunyai bentuk

$$
F=F_m+F_{m+1}+\cdots,
\qquad m=m_P,
$$

dan khususnya $F\in\mathfrak a^m$. Jika
$G\in\mathfrak a^{n-m}$ dengan $n\ge m$, maka
$GF\in\mathfrak a^n$. Karena itu terdapat barisan eksak pendek

$$
0\longrightarrow
S/\mathfrak a^{n-m}
\xrightarrow{\,\cdot F\,}
S/\mathfrak a^n
\longrightarrow
S/(\mathfrak a^n,F)=R/\mathfrak m^n
\longrightarrow0.
$$

Injektivitas di kiri diperoleh dari perbandingan derajat langsung; lihat
Soal 23.4. Diketahui bahwa

$$
\dim_K(S/\mathfrak a^n)=\frac{n(n+1)}2.
$$

Oleh sebab itu, untuk $n\ge m$,

$$
\begin{aligned}
\dim_K(R/\mathfrak m^n)
&=\frac{n(n+1)}2-\frac{(n-m)(n-m+1)}2\\
&=\frac{n^2+n-(n-m)^2-n+m}{2}\\
&=\frac{2nm-m^2+m}{2}\\
&=mn-\frac{m(m-1)}2.
\end{aligned}
$$

Inilah bentuk linear yang diperlukan. $\square$

<!-- upstream_entity: Ebene algebraische Kurve/Multiplizität über Hilbert-Samuel Polynom/Bemerkung -->

### Catatan: multiplisitas sebagai invarian intrinsik {#br-ak-2025-2026-l23-rem-01}

Teorema 23.5 khususnya menyatakan bahwa multiplisitas suatu titik pada kurva
bidang merupakan invarian gelanggang lokal kurva di titik tersebut. Jadi,
multiplisitas hanya bergantung pada sifat intrinsik kurva, bukan pada
realisasinya di dalam bidang ambien.

Setiap gelanggang lokal Noether mempunyai *multiplisitas Hilbert-Samuel*,
yang didefinisikan melalui dimensi atas $R/\mathfrak m$ dari modul faktor
$\mathfrak m^n/\mathfrak m^{n+1}$. Dalam kasus berdimensi satu,
multiplisitas ini adalah

$$
\lim_{n\to\infty}
\dim_{R/\mathfrak m}
\left(\mathfrak m^n/\mathfrak m^{n+1}\right),
$$

karena fungsi tersebut akhirnya menjadi konstan--sebuah fakta yang tidak
sepele. Jika $R$ memuat suatu lapangan $K$ yang isomorfik dengan lapangan
residunya, seperti pada gelanggang lokal kurva yang dibahas di sini, bilangan
yang sama juga diberikan oleh

$$
\lim_{n\to\infty}
\frac{\dim_K(R/\mathfrak m^n)}{n}.
$$

<!-- upstream_entity: Ebene algebraische Kurve/Punkt/Glatt,diskreter Bewertungsring, Multiplizität/Fakt -->

### Teorema: kemulusan, multiplisitas, valuasi diskret, dan normalitas {#br-ak-2025-2026-l23-thm-03}

Misalkan $K$ suatu lapangan dan $F\in K[X,Y]$ suatu polinom tak konstan tanpa
faktor berulang, dengan kurva aljabar terkait

$$
C=V(F).
$$

Misalkan $P=(a,b)\in C$, dengan ideal maksimal

$$
\mathfrak m=(X-a,Y-b)
$$

dan gelanggang lokal

$$
R=K[X,Y]_{\mathfrak m}/(F).
$$

Pernyataan berikut ekuivalen.

1. $P$ merupakan titik mulus pada kurva.
2. Multiplisitas $P$ sama dengan satu.
3. $R$ merupakan gelanggang valuasi diskret.
4. $R$ merupakan domain integral normal.

<!-- upstream_entity: Ebene algebraische Kurve/Punkt/Glatt,diskreter Bewertungsring, Multiplizität/Fakt/Beweis -->

### Bukti {#br-ak-2025-2026-l23-prf-05}

Ekuivalensi (1) $\Leftrightarrow$ (2) mengikuti Definisi 22.7 tentang
multiplisitas. Ekuivalensi (3) $\Leftrightarrow$ (4) dibuktikan dalam
Teorema 21.8, sedangkan implikasi (1) $\Rightarrow$ (3) dibuktikan dalam
Lema 23.3. Jadi tinggal membuktikan (3) $\Rightarrow$ (2), dan berdasarkan
Teorema 23.5 kita boleh menggunakan multiplisitas Hilbert-Samuel.

Cukup ditunjukkan bahwa, untuk gelanggang lokal kurva bidang yang merupakan
gelanggang valuasi diskret, semua modul faktor

$$
\mathfrak m^n/\mathfrak m^{n+1}
\cong
\mathfrak m^n/\mathfrak m^n\mathfrak m
$$

berdimensi satu atas lapangan residu $R/\mathfrak m\cong K$. Karena
$\mathfrak m^n=(\pi^n)$, hal ini langsung mengikuti lema Nakayama. $\square$

## Kurva monomial dan multiplisitas {#br-ak-2025-2026-l23-s04}

<!-- upstream_entity: Monomiale Kurve/Multiplizität/Numerisch und Hilbert-Samuel/Textabschnitt -->

Misalkan $M\subseteq\mathbb N$ suatu monoid numerik yang dibangkitkan oleh
bilangan-bilangan asli saling prima

$$
e_1<e_2<\cdots<e_r.
$$

Pembangkit minimal $e_1$ juga disebut *multiplisitas numerik* $M$. Kita akan
menunjukkan bahwa bilangan ini benar-benar menghasilkan multiplisitas
gelanggang yang tepat. Tetapkan

$$
M_+=\{m\in M\mid m\ge1\}
$$

dan

$$
nM_+=
\left\{
m\in M\ \middle|\
m=m_1+\cdots+m_n\text{ untuk suatu }m_i\in M_+
\right\}.
$$

Keduanya merupakan ideal monoid pada $M$. Jadi ruang monom

$$
K[nM_+]=\bigoplus_{m\in nM_+}KT^m
$$

merupakan ideal di dalam gelanggang monoid. Secara khusus,

$$
\mathfrak m=K[M_+]
$$

merupakan ideal maksimal, dan pangkat-pangkatnya ialah

$$
\mathfrak m^n=K[nM_+].
$$

<!-- upstream_entity: Monomiale Kurven/Multiplizität/Abschätzungen für Anzahl in Differenzmengen/Fakt -->

### Lema: taksiran himpunan selisih monoid {#br-ak-2025-2026-l23-lem-03}

Misalkan $M\subseteq\mathbb N$ suatu monoid numerik dengan multiplisitas
numerik $e_1$. Pilih bilangan $\ell\ge1$ sedemikian sehingga
$\mathbb N_{\ge\ell}\subseteq M$. Maka

$$
ne_1-\ell
\le
\#(M\setminus nM_+)
\le
(n-1)e_1+\ell.
$$

<!-- upstream_entity: Monomiale Kurven/Multiplizität/Abschätzungen für Anzahl in Differenzmengen/Fakt/Beweis -->

### Bukti {#br-ak-2025-2026-l23-prf-06}

Taksiran bawah mengikuti fakta bahwa bilangan terkecil dalam $nM_+$ adalah
$ne_1$. Jadi bilangan $0,1,\ldots,ne_1-1$ berada di luarnya. Semua bilangan
yang sedikitnya $\ell$ berada dalam $M$, sehingga di antara $ne_1$ bilangan
tersebut setidaknya $ne_1-\ell$ berada dalam $M$ tetapi tidak dalam $nM_+$.

Untuk taksiran atas, kita klaim bahwa setiap bilangan yang sedikitnya
$(n-1)e_1+\ell$ berada dalam $nM_+$. Misalkan

$$
x\ge(n-1)e_1+\ell.
$$

Tulislah

$$
x=(n-1)e_1+\ell',
\qquad \ell'\ge\ell.
$$

Karena $\ell'\in M_+$, ruas kanan adalah jumlah $n$ unsur $M_+$: sebanyak
$n-1$ suku sama dengan $e_1$ dan satu suku sama dengan $\ell'$. Jadi
$x\in nM_+$, dan taksiran atas terbukti. $\square$

*Catatan edisi -- koreksi batas sumber:* Sumber hanya menyebut $\ell$ sebagai
“suatu bilangan” dan pada langkah terakhir mengatakan bahwa suku-sukunya
berada di $M$. Hipotesis $\ell\ge1$, yang selalu dapat dipenuhi dengan
memperbesar ambang, memastikan bahwa semua $n$ suku benar-benar berada di
$M_+$ sebagaimana dituntut oleh definisi $nM_+$.

<!-- upstream_entity: Monomiale Kurve/Hilbert-Samuel Multiplizität ist numerische Multiplizität/Fakt -->

### Korolari: multiplisitas numerik sama dengan multiplisitas Hilbert-Samuel {#br-ak-2025-2026-l23-cor-01}

Misalkan $M\subseteq\mathbb N$ suatu monoid numerik yang dibangkitkan oleh
bilangan-bilangan saling prima dan mempunyai multiplisitas numerik $e_1$.
Misalkan

$$
\mathfrak m=K[M_+]
$$

ideal maksimal pada gelanggang monoid $K[M]$ yang bersesuaian dengan titik
asal. Maka

$$
\lim_{n\to\infty}
\frac{\dim_K\left(K[M]/\mathfrak m^n\right)}{n}
=e_1.
$$

Dengan kata lain, multiplisitas numerik sama dengan multiplisitas
Hilbert-Samuel.

<!-- upstream_entity: Monomiale Kurve/Hilbert-Samuel Multiplizität ist numerische Multiplizität/Fakt/Beweis -->

### Bukti {#br-ak-2025-2026-l23-prf-07}

Karena $\mathfrak m^n=K[nM_+]$, gelanggang faktor

$$
K[M]/\mathfrak m^n
=K[M]/K[nM_+]
$$

mempunyai monom-monom $T^m$ dengan $m\in M\setminus nM_+$ sebagai basis
atas $K$. Dimensinya dengan demikian sama dengan
$\#(M\setminus nM_+)$. Menurut taksiran Lema 23.8,

$$
\frac{\#(M\setminus nM_+)}{n}\longrightarrow e_1.
$$

Konvergensi yang sama berlaku bagi dimensi-dimensi tersebut. $\square$

*Catatan edisi -- penjelasan notasi sumber:* Bentuk sumber
$K[M]/(nM_+)$ berarti hasil bagi oleh ideal monom
$K[nM_+]$; tanda kurung itu bukan perkalian skalar himpunan dengan $n$.
