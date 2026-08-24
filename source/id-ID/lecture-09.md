---
title: "Kuliah 9 - Gelanggang Noether, Teorema Basis Hilbert, dan Modul"
stable_id: br-ak-2025-2026-l09
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 9"
upstream_pageid: 165898
upstream_revid: 1112241
upstream_timestamp: "2026-08-20T16:29:07Z"
upstream_mediawiki_sha1: 2a702891ae21267751c7900639ef3828faf949c2
source_url: "https://de.wikiversity.org/w/index.php?oldid=1112241"
authority_manifest: authority/wikiversity/unit-09/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 7cf7a956dffe854da9d021e3c74615573b91b5701d7e3b78a8f5f1aa45bfbc29
lecture_xml_sha256: 9094f97a84c8e4b46e42b993adfa31847aeb375536d16f4c39b6f35109e68e6a
lecture_expanded_tex_sha256: ae15977cb7189b8cdc2992d70193dd503725da41ad881ae1c68a681af3446e3d
license: "CC BY-SA 4.0 for translated course text; media retain component rights in authority/RIGHTS-unit-09.csv"
translation_status: complete
---

# Kuliah 9: Gelanggang Noether, Teorema Basis Hilbert, dan Modul {#br-ak-2025-2026-l09}

## Gelanggang Noether {#br-ak-2025-2026-l09-s01}

Pada kuliah-kuliah berikutnya kita akan mengembangkan lebih lanjut sisi
aljabar dari geometri aljabar. Tujuan pertama kita adalah menunjukkan bahwa,
jika $R$ merupakan gelanggang Noether, maka gelanggang polinomial $R[X]$ juga
merupakan gelanggang Noether (Teorema Basis Hilbert). Hal ini juga berlaku
untuk penambahan beberapa (hingga banyaknya) variabel, khususnya untuk
gelanggang polinomial dalam hingga banyak variabel di atas suatu lapangan.
Kita mengingat kembali pengertian gelanggang Noether.

<!-- upstream_entity: Kommutative Ringtheorie/Theorie der noetherschen kommutativen Ringe/Textabschnitt -->

### Definisi: gelanggang Noether {#br-ak-2025-2026-l09-def-01}

Suatu gelanggang komutatif $R$ disebut *Noether* jika setiap ideal di dalamnya
dibangkitkan secara hingga.

<!-- upstream_entity: Kommutative Ringtheorie/Noethersche Ringe/Äquivalente Formulierungen/Fakt -->

### Proposisi: karakterisasi gelanggang Noether {#br-ak-2025-2026-l09-prop-01}

Untuk gelanggang komutatif $R$, pernyataan-pernyataan berikut ekuivalen.

1. $R$ merupakan gelanggang Noether.
2. Setiap rantai ideal naik

   $$
   \mathfrak a_1\subseteq\mathfrak a_2\subseteq\mathfrak a_3\subseteq\cdots
   $$

   menjadi *stasioner*; artinya, terdapat $n$ sedemikian sehingga

   $$
   \mathfrak a_n=\mathfrak a_{n+1}=\cdots.
   $$

#### Bukti {#br-ak-2025-2026-l09-prop-01-proof}

**(1) $\Rightarrow$ (2).** Misalkan

$$
\mathfrak a_1\subseteq\mathfrak a_2\subseteq\mathfrak a_3\subseteq\cdots
$$

merupakan rantai ideal naik di $R$. Kita pertimbangkan gabungannya

$$
\mathfrak a=\bigcup_{n\in\mathbb N}\mathfrak a_n,
$$

yang kembali merupakan ideal di $R$. Karena $R$ Noether, $\mathfrak a$
dibangkitkan secara hingga, yaitu

$$
\mathfrak a=(f_1,\ldots,f_k).
$$

Semua $f_i$ berada dalam gabungan ideal-ideal $\mathfrak a_n$. Karena
ideal-ideal itu naik, terdapat $n$ sedemikian sehingga

$$
f_1,\ldots,f_k\in\mathfrak a_n.
$$

Maka, untuk setiap $m\geq0$,

$$
(f_1,\ldots,f_k)\subseteq\mathfrak a_n
\subseteq\mathfrak a_{n+m}
\subseteq\bigcup_{n\in\mathbb N}\mathfrak a_n
\subseteq(f_1,\ldots,f_k).
$$

Semua inklusi tersebut harus merupakan kesamaan; jadi rantai ideal stasioner
mulai dari $n$.

**(2) $\Rightarrow$ (1).** Misalkan $\mathfrak a$ suatu ideal di $R$.
Andaikan $\mathfrak a$ tidak dibangkitkan secara hingga. Kita dapat
membangun secara bertahap rantai ideal naik sejati tak berhingga

$$
\mathfrak a_1\subset\mathfrak a_2\subset\cdots\subseteq\mathfrak a,
$$

dengan setiap $\mathfrak a_n$ dibangkitkan secara hingga. Misalkan sudah
dibangun

$$
\mathfrak a_1\subset\mathfrak a_2\subset\cdots\subset\mathfrak a_n
\subseteq\mathfrak a.
$$

Karena $\mathfrak a_n$ dibangkitkan secara hingga sedangkan $\mathfrak a$
tidak, inklusi $\mathfrak a_n\subseteq\mathfrak a$ bersifat sejati. Jadi ada
unsur

$$
f_{n+1}\in\mathfrak a,\qquad f_{n+1}\notin\mathfrak a_n.
$$

Ideal

$$
\mathfrak a_{n+1}:=\mathfrak a_n+(f_{n+1})
$$

melanjutkan rantai itu secara sejati. Ini bertentangan dengan (2).

<!-- upstream_entity: Noetherscher Ring/Kommutativ/Restklassenring/Noethersch/Fakt -->

### Lema: gelanggang faktor dari gelanggang Noether {#br-ak-2025-2026-l09-lem-01}

Jika $R$ merupakan gelanggang Noether, maka setiap gelanggang faktor
$R/\mathfrak b$ juga Noether.

#### Bukti {#br-ak-2025-2026-l09-lem-01-proof}

Misalkan $\mathfrak a\subseteq R/\mathfrak b$ suatu ideal dan misalkan
$\widetilde{\mathfrak a}\subseteq R$ adalah ideal prapeta yang bersesuaian.
Menurut asumsi, ideal ini dibangkitkan secara hingga, sehingga

$$
\widetilde{\mathfrak a}=(f_1,\ldots,f_n).
$$

Kelas-kelas residu dari pembangkit-pembangkit tersebut,
$\bar f_1,\ldots,\bar f_n$, membentuk sistem pembangkit ideal untuk
$\mathfrak a$. Memang, untuk $\bar g\in\mathfrak a$ berlaku di $R$

$$
g=\sum_{i=1}^n r_i f_i,
$$

dan karena itu di $R/\mathfrak b$

$$
\bar g=\sum_{i=1}^n\bar r_i\,\bar f_i.
$$

## Teorema Basis Hilbert {#br-ak-2025-2026-l09-s02}

Seperti banyak pernyataan dasar dalam aljabar komutatif, Teorema Basis Hilbert
yang akan kita bahas berawal dari David Hilbert, lebih tepatnya dari karyanya
tahun 1890, *Ueber die Theorie der algebraischen Formen*.

![David Hilbert (1862–1943)](authority/assets/David_Hilbert_1886.jpg)

*David Hilbert (1862–1943); pencipta tidak diketahui (1886), Commons, domain
publik.*

<!-- upstream_entity: Kommutative Ringtheorie/Hilbertscher Basissatz/Fakt -->

### Teorema Basis Hilbert {#br-ak-2025-2026-l09-thm-01}

Jika $R$ merupakan gelanggang Noether, maka gelanggang polinomial $R[X]$ juga
Noether.

#### Bukti {#br-ak-2025-2026-l09-thm-01-proof}

Misalkan $\mathfrak b$ suatu ideal dalam gelanggang polinomial $R[X]$. Untuk
$n\in\mathbb N$, definisikan ideal $\mathfrak a_n$ di $R$ dengan

$$
\mathfrak a_n=\left\{c\in R\mid\text{ada }F\in\mathfrak b\text{ dengan }
F=cX^n+c_{n-1}X^{n-1}+\cdots+c_1X+c_0\right\}.
$$

Jadi, $\mathfrak a_n$ terdiri atas semua koefisien utama polinom berderajat
$n$ di $\mathfrak b$. Jelas bahwa $\mathfrak a_n$ adalah ideal di $R$
(di sini kita mengizinkan $0$ sebagai koefisien utama). Selain itu,

$$
\mathfrak a_n\subseteq\mathfrak a_{n+1},
$$

karena polinom $F$ berderajat $n$ dengan koefisien utama $c$ dapat dikalikan
dengan $X$ untuk memperoleh polinom berderajat $n+1$ yang masih berkoefisien
utama $c$. Karena $R$ Noether, rantai ideal naik ini stasioner; pilih $n$
sedemikian sehingga

$$
\mathfrak a_n=\mathfrak a_{n+1}=\cdots.
$$

Untuk setiap $i\leq n$, pilih suatu sistem pembangkit berhingga

$$
\mathfrak a_i=(c_{i1},\ldots,c_{ik_i}),
$$

dan pilih polinom yang bersesuaian

$$
F_{ij}=c_{ij}X^i+\text{ suku-suku berderajat lebih rendah}
$$

di $\mathfrak b$ (polinom-polinom itu ada menurut definisi $\mathfrak a_i$).

Kita klaim bahwa $\mathfrak b$ dibangkitkan oleh semua

$$
\left\{F_{ij}\mid 0\leq i\leq n,\ 1\leq j\leq k_i\right\}.
$$

Untuk setiap $G\in\mathfrak b$, kita buktikan dengan induksi pada derajat $G$
bahwa $G$ dapat ditulis sebagai kombinasi linear atas $R$ dari polinom-
polinom $F_{ij}$ tersebut. Jika $G$ konstan, yaitu $G\in R$, hal ini jelas.
Misalkan derajat $G$ sama dengan $d$ dan pernyataan sudah terbukti untuk
derajat yang lebih kecil. Tulis

$$
G=cX^d+c_{d-1}X^{d-1}+\cdots+c_1X+c_0.
$$

Kita memiliki $c\in\mathfrak a_d$. Jika $d\leq n$, maka $c$ dapat ditulis
sebagai kombinasi linear atas $R$ dari $c_{dj}$, katakanlah

$$
c=\sum_{j=1}^{k_d}r_jc_{dj}.
$$

Dengan demikian

$$
G-\sum_{j=1}^{k_d}r_jF_{dj}\in\mathfrak b
$$

dan derajatnya lebih kecil, sehingga hipotesis induksi dapat diterapkan. Jika
$d>n$, maka

$$
c=\sum_{i=0,\ldots,n,\,j=1,\ldots,k_i}r_{ij}c_{ij}.
$$

Karena itu

$$
G-\sum_{i=0,\ldots,n,\,j=1,\ldots,k_i}r_{ij}X^{d-i}F_{ij}
$$

juga berada di $\mathfrak b$ dan mempunyai derajat lebih kecil. Induksi
selesai, sehingga $\mathfrak b$ dibangkitkan secara hingga.

<!-- upstream_entity: Kommutative Ringtheorie/Hilbertscher Basissatz/Endliche viele Variablen/Fakt -->

### Korolari: hingga banyak variabel {#br-ak-2025-2026-l09-cor-01}

Jika $R$ gelanggang Noether, maka

$$
R[X_1,\ldots,X_n]
$$

juga Noether.

#### Bukti {#br-ak-2025-2026-l09-cor-01-proof}

Terapkan Teorema Basis Hilbert secara induktif pada rantai

$$
R\subset R[X_1]\subset (R[X_1])[X_2]=R[X_1,X_2]
\subset (R[X_1,X_2])[X_3]=R[X_1,X_2,X_3]
\subset\cdots\subset R[X_1,\ldots,X_n].
$$

<!-- upstream_entity: Kommutative Ringtheorie/Polynomring über Körper/Endliche viele Variablen/Noethersch/Fakt -->

### Korolari: gelanggang polinomial di atas lapangan {#br-ak-2025-2026-l09-cor-02}

Jika $K$ merupakan lapangan, maka $K[X_1,\ldots,X_n]$ Noether. Ini adalah
kasus khusus dari Korolari 9.5.

#### Bukti {#br-ak-2025-2026-l09-cor-02-proof}

Ini merupakan kasus khusus dari Korolari 9.5.

Teorema Basis Hilbert khususnya berarti bahwa setiap subvarietas tertutup

$$
V\subseteq\mathbb A_K^n
$$

dalam ruang afin dapat dideskripsikan oleh hingga banyak polinom. Jadi setiap
lokus nol aljabar sudah merupakan lokus nol dari hingga banyak polinom.

<!-- upstream_entity: Hilbertscher Basisatz/Affin-algebraische Menge als Faser über 0 einer Abbildung/Fakt -->

### Korolari: sebagai serat atas titik nol {#br-ak-2025-2026-l09-cor-03}

Misalkan $V\subseteq\mathbb A_K^n$ suatu himpunan aljabar afin. Maka ada suatu
pemetaan

$$
\varphi:\mathbb A_K^n\longrightarrow\mathbb A_K^m
$$

yang komponen-komponennya diberikan oleh polinom

$$
F_i\in K[X_1,\ldots,X_n],\qquad
\varphi=(F_1,\ldots,F_m),
$$

sedemikian sehingga $V$ merupakan prapeta titik nol

$$
0\in\mathbb A_K^m.
$$

#### Bukti {#br-ak-2025-2026-l09-cor-03-proof}

Misalkan $\mathfrak a$ merupakan ideal yang mendeskripsikan $V$, sehingga

$$
V=V(\mathfrak a).
$$

Menurut Teorema Basis Hilbert, terdapat

$$
F_1,\ldots,F_m\in K[X_1,\ldots,X_n]
$$

dengan $\mathfrak a=(F_1,\ldots,F_m)$. Maka

$$
V=V(\mathfrak a)=V(F_1)\cap\cdots\cap V(F_m).
$$

Gabungkan polinom-polinom ini menjadi pemetaan

$$
\varphi=(F_1,\ldots,F_m):\mathbb A_K^n\longrightarrow\mathbb A_K^m.
$$

Kita mempunyai $\varphi(P)=0$ tepat ketika semua fungsi komponennya nol,
yang terjadi tepat ketika $P\in V(F_i)$ untuk setiap $i$; jadi
$V=\varphi^{-1}(0)$.

<!-- upstream_entity: Kommutative Ringtheorie/Algebra von endlichem Typ/Definition -->

### Definisi: aljabar tipe hingga {#br-ak-2025-2026-l09-def-02}

Misalkan $R$ gelanggang komutatif. Suatu $R$-aljabar $A$ disebut *bertipe
hingga* (atau *dibangkitkan secara hingga*) jika berbentuk

$$
A=R[X_1,\ldots,X_n]/\mathfrak a.
$$

Dengan demikian, suatu $R$-aljabar yang dibangkitkan secara hingga memiliki
representasi sebagai gelanggang faktor dari aljabar polinomial atas $R$ dalam
hingga banyak variabel. Representasi seperti ini sama sekali tidak harus
unik.

<!-- upstream_entity: Kommutative Ringtheorie/Algebra von endlichem Typ/Körper/Noethersch/Fakt -->

### Korolari: aljabar tipe hingga dari gelanggang Noether {#br-ak-2025-2026-l09-cor-04}

Jika $R$ merupakan gelanggang Noether, maka setiap $R$-aljabar tipe hingga
juga Noether. Khususnya, jika $K$ suatu lapangan, setiap $K$-aljabar tipe
hingga adalah Noether.

#### Bukti {#br-ak-2025-2026-l09-cor-04-proof}

Hal ini mengikuti dari Korolari 9.5 dan Lema 9.3.

## Dekomposisi menjadi komponen tak tereduksi {#br-ak-2025-2026-l09-s03}

Dari Teorema Basis Hilbert kita memperoleh bahwa setiap rantai ideal naik

$$
\mathfrak a_1\subseteq\mathfrak a_2\subseteq\mathfrak a_3\subseteq\cdots
$$

dalam $K[X_1,\ldots,X_n]$ menjadi stasioner. Konsekuensinya untuk rantai
himpunan aljabar afin yang menurun di ruang afin adalah sebagai berikut.

<!-- upstream_entity: Affine Varietäten/Zariski-Topologie ist noethersch/Fakt -->

### Teorema: topologi Zariski bersifat Noether {#br-ak-2025-2026-l09-thm-02}

Dalam ruang afin $\mathbb A_K^n$, setiap barisan himpunan tertutup yang
menurun

$$
V_1\supseteq V_2\supseteq\cdots
$$

menjadi stasioner.

#### Bukti {#br-ak-2025-2026-l09-thm-02-proof}

Misalkan

$$
V_1\supseteq V_2\supseteq\cdots
$$

rantai menurun himpunan aljabar afin dalam $\mathbb A_K^n$. Dari Lema 3.7,
untuk ideal pelenyapan yang bersesuaian berlaku

$$
\operatorname{Id}(V_i)\subseteq\operatorname{Id}(V_{i+1}).
$$

Menurut Korolari 9.6, rantai ideal ini stasioner, misalnya untuk $i\geq i_0$.
Menurut bagian (3) Lema 3.8,

$$
V_i=V(\operatorname{Id}(V_i)).
$$

Maka, untuk $i\geq i_0$,

$$
V_i=V(\operatorname{Id}(V_i))
=V(\operatorname{Id}(V_{i+1}))=V_{i+1},
$$

sehingga rantai menurun tersebut stasioner.

Akibatnya, dengan beralih ke komplemen, setiap rantai naik himpunan terbuka
Zariski dalam ruang afin juga stasioner. Topologi seperti ini disebut
*Noether* (secara umum, suatu orde parsial yang setiap rantai naiknya
stasioner disebut Noether). Pada ruang Noether, setiap himpunan tak kosong
dari himpunan terbuka (atau himpunan tertutup) memiliki unsur maksimal
(atau minimal). Ini berguna sebagai prinsip pembuktian
*induksi Noether*: untuk membuktikan bahwa sifat $E$ berlaku bagi semua
himpunan tertutup, tinjau himpunan himpunan tertutup yang tidak memenuhi
$E$. Kita ingin menunjukkan bahwa himpunan ini kosong; andaikan tidak, ia
memiliki unsur minimal, dan kita dapat membawa unsur minimal itu ke
kontradiksi. Keabsahan prinsip ini bersandar pada fakta bahwa dari himpunan
tak kosong tanpa unsur minimal dapat dibangun rantai menurun tak berhingga.
Contoh khas prinsip ini adalah teorema berikut.

<!-- upstream_entity: Affin-algebraische Teilmengen/Zerlegung in irreduzible Komponenten/Fakt -->

### Teorema: dekomposisi komponen tak tereduksi {#br-ak-2025-2026-l09-thm-03}

Untuk setiap himpunan aljabar afin $V\subseteq\mathbb A_K^n$, terdapat
dekomposisi unik

$$
V=V_1\cup\cdots\cup V_k
$$

dengan himpunan-himpunan $V_i$ tak tereduksi dan

$$
V_i\not\subseteq V_j\qquad\text{untuk }i\ne j.
$$

#### Bukti keberadaan (induksi Noether) {#br-ak-2025-2026-l09-thm-03-existence}

Andaikan tidak setiap himpunan aljabar afin mempunyai dekomposisi demikian.
Maka ada himpunan minimal, sebut $V$, yang tidak mempunyai dekomposisi.
$V$ tidak mungkin tak tereduksi; jadi ada dekomposisi taktrivial

$$
V=V_1\cup V_2.
$$

Karena $V_1$ dan $V_2$ merupakan subhimpunan sejati dari $V$, masing-masing
memiliki representasi hingga sebagai gabungan himpunan-himpunan tak
tereduksi. Menggabungkan kedua representasi itu menghasilkan representasi
hingga untuk $V$, kontradiksi.

#### Bukti keunikan {#br-ak-2025-2026-l09-thm-03-uniqueness}

Misalkan

$$
V=V_1\cup\cdots\cup V_k=W_1\cup\cdots\cup W_m
$$

dua dekomposisi menjadi himpunan tak tereduksi (masing-masing tanpa hubungan
inklusi). Kita mempunyai

$$
V_1=V_1\cap V
=V_1\cap(W_1\cup\cdots\cup W_m)
=(V_1\cap W_1)\cup\cdots\cup(V_1\cap W_m).
$$

Karena $V_1$ tak tereduksi, haruslah $V_1\subseteq W_j$ untuk suatu $j$.
Dengan argumen yang sama, $W_j\subseteq V_i$ untuk suatu $i$; akibatnya
$i=1$ dan $V_1=W_j$. Dengan cara yang sama, $V_2$ dan seterusnya muncul
kembali dalam dekomposisi di sebelah kanan, sehingga dekomposisi itu unik.

Komponen-komponen $V_1,\ldots,V_k$ pada teorema di atas disebut
*komponen tak tereduksi* dari $V$.

## Modul {#br-ak-2025-2026-l09-s04}

<!-- upstream_entity: Modultheorie (kommutative Algebra)/Einführung/Textabschnitt -->

### Definisi: modul {#br-ak-2025-2026-l09-def-03}

Misalkan $R$ gelanggang komutatif dan

$$
M=(M,+,0)
$$

suatu grup komutatif yang ditulis secara aditif. Kita menyebut $M$ sebagai
*modul-$R$* jika ditetapkan suatu operasi

$$
R\times M\longrightarrow M,\qquad(r,v)\longmapsto rv=r\cdot v,
$$

yang disebut *perkalian skalar* dan memenuhi aksioma-aksioma berikut (untuk
sembarang $r,s\in R$ dan $u,v\in M$):

$$
\begin{aligned}
r(su)&=(rs)u,\\
r(u+v)&=(ru)+(rv),\\
(r+s)u&=(ru)+(su),\\
1u&=u.
\end{aligned}
$$

<!-- upstream_entity: Modultheorie (kommutative Algebra)/Untermodul/Definition -->

### Definisi: submodul {#br-ak-2025-2026-l09-def-04}

Misalkan $R$ gelanggang komutatif dan $M$ modul-$R$. Subhimpunan

$$
U\subseteq M
$$

disebut *submodul-$R$* jika $U$ merupakan subgrup dari $(M,0,+)$ dan untuk
setiap $u\in U$ serta $r\in R$ berlaku $ru\in U$.

<!-- upstream_entity: Modultheorie (kommutative Algebra)/Erzeugendensystem/Definition -->

### Definisi: sistem pembangkit modul {#br-ak-2025-2026-l09-def-05}

Misalkan $R$ gelanggang komutatif dan $M$ modul-$R$. Suatu keluarga

$$
v_i\in M\qquad(i\in I)
$$

disebut *sistem pembangkit* untuk $M$ jika untuk setiap $v\in M$ terdapat
representasi

$$
v=\sum_{i\in J}r_iv_i,
$$

dengan $J\subseteq I$ berhingga dan $r_i\in R$.

<!-- upstream_entity: Kommutative Algebra/Modultheorie/Endlicher Modul/Definition -->

### Definisi: modul dibangkitkan secara hingga {#br-ak-2025-2026-l09-def-06}

Modul-$M$ disebut *dibangkitkan secara hingga* (atau *hingga*) jika memiliki
sistem pembangkit berhingga $v_i$ ($i\in I$), yakni jika himpunan indeksnya
berhingga.

Sebuah gelanggang komutatif $R$ sendiri secara alami merupakan modul-$R$ jika
perkalian gelanggang ditafsirkan sebagai perkalian skalar. Ideal-ideal
tepat merupakan submodul-$R$ dari $R$. Untuk ideal, istilah *sistem pembangkit
ideal* dan *sistem pembangkit modul* bertepatan. Ruang vektor hanyalah modul
atas suatu lapangan.
