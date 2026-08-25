---
title: "Kuliah 20 - Gelanggang Normal dan Normalisasi"
stable_id: br-ak-2025-2026-l20
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 20"
upstream_pageid: 165909
upstream_revid: 1112311
upstream_timestamp: "2026-08-21T09:10:26Z"
upstream_mediawiki_sha1: 74eb303dc659cb8131aaaee6948962210f063f4e
source_url: "https://de.wikiversity.org/w/index.php?oldid=1112311"
authority_manifest: authority/wikiversity/unit-20/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: b063e5edc556cd18598389083ea27ea7f255edfe2ae00e13ebf24de76e5b37d7
lecture_xml_sha256: 052aee339f49d9d2dfe7f71f50a17c5cc4f9f507eae70a2b8692a1dd5aa38e77
lecture_expanded_tex_sha256: 8d95abad821218ccc9a32b3b7d57f8696b57bb98991c707f4ef8e5a20a1bdecc
license: "CC BY-SA 4.0 for translated course text; the figure retains CC BY 2.5 component rights in authority/RIGHTS-unit-20.csv"
translation_status: complete
---

# Kuliah 20: Gelanggang Normal dan Normalisasi {#br-ak-2025-2026-l20}

## Gelanggang normal dan normalisasi {#br-ak-2025-2026-l20-s01}

<!-- upstream_entity: Kommutative Ringtheorie/Ganzheit/Normal (ganz-abgeschlossen)/Definition -->

### Definisi: domain integral normal {#br-ak-2025-2026-l20-def-01}

Suatu domain integral disebut *normal* jika tertutup secara integral di dalam
lapangan pecahannya.

Contoh penting gelanggang normal diberikan oleh domain faktorisasi tunggal.

<!-- upstream_entity: Kommutative Ringtheorie/Faktoriell/Normal/Fakt -->

### Teorema: domain faktorisasi tunggal bersifat normal {#br-ak-2025-2026-l20-thm-01}

Misalkan $R$ suatu domain faktorisasi tunggal. Maka $R$ normal.

#### Bukti {#br-ak-2025-2026-l20-thm-01-proof}

Misalkan

$$
K=Q(R)
$$

lapangan pecahan $R$, dan misalkan $q\in K$ memenuhi persamaan keintegralan

$$
q^n+r_{n-1}q^{n-1}+r_{n-2}q^{n-2}+\cdots+r_1q+r_0=0,
\qquad r_i\in R.
$$

Tuliskan

$$
q=\frac ab,
\qquad a,b\in R,
\qquad b\ne0,
$$

dalam bentuk yang telah disederhanakan, sehingga $a$ dan $b$ tidak mempunyai
pembagi prima bersama. Kita harus menunjukkan bahwa $b$ satuan di $R$, sebab
dalam hal itu

$$
q=ab^{-1}\in R.
$$

Kalikan persamaan keintegralan di atas dengan $b^n$. Di dalam $R$ diperoleh

$$
a^n+(r_{n-1}b)a^{n-1}+(r_{n-2}b^2)a^{n-2}
+\cdots+(r_1b^{n-1})a+r_0b^n=0.
$$

Jika $b$ bukan satuan, terdapat pembagi prima $p$ dari $b$. Unsur $p$ membagi
semua suku

$$
(r_{n-i}b^i)a^{n-i},
\qquad i\geq1,
$$

dan karena itu juga membagi suku pertama $a^n$. Maka $p$ membagi $a$, yang
bertentangan dengan asumsi bahwa $a$ dan $b$ tidak mempunyai pembagi prima
bersama.

<!-- upstream_entity: Kommutative Ringtheorie/Normal/Nenneraufnahme ist normal/Fakt -->

### Lema: pelokalan domain integral normal kembali normal {#br-ak-2025-2026-l20-lem-01}

Misalkan $R$ suatu domain integral normal dan $S\subseteq R$ suatu sistem
multiplikatif. Maka pelokalan $R_S$ juga normal.

#### Bukti {#br-ak-2025-2026-l20-lem-01-proof}

Lihat Soal 20.6.

<!-- upstream_entity: Kommutative Ringtheorie/Ganzheit/Normalisierung für Integritätsbereich/Definition -->

### Definisi: normalisasi domain integral {#br-ak-2025-2026-l20-def-02}

Misalkan $R$ suatu domain integral dan $Q(R)$ lapangan pecahannya. Penutupan
integral $R$ di dalam $Q(R)$ disebut *normalisasi* $R$.

Menurut Korolari 19.10, normalisasi merupakan subgelanggang lapangan pecahan.
Suatu fakta tak trivial menyatakan bahwa jika $R$ bertipe hingga di atas suatu
lapangan, normalisasinya juga bertipe hingga.

## Normalisasi gelanggang monoid {#br-ak-2025-2026-l20-s02}

Kita akan membahas kapan gelanggang monoid bersifat normal dan bagaimana
normalisasi gelanggang monoid dapat dideskripsikan. Mula-mula kita memerlukan
syarat-syarat yang menjamin bahwa gelanggang monoid di atas suatu domain
integral kembali merupakan domain integral.

<!-- upstream_entity: Kommutatives Monoid/Torsionsfrei/Definition -->

### Definisi: monoid bebas torsi {#br-ak-2025-2026-l20-def-03}

Suatu monoid komutatif $M$ disebut *bebas torsi* jika, untuk $m,n\in M$ dan
suatu bilangan positif $r\in\mathbb N_+$, dari

$$
rm=rn
$$

selalu mengikuti

$$
m=n.
$$

<!-- upstream_entity: Kommutative Monoidringe/Monoid mit Kürzungsregel und torsionsfrei/Grundring integer/Integer/Fakt -->

### Teorema: gelanggang monoid bebas torsi merupakan domain integral {#br-ak-2025-2026-l20-thm-02}

Misalkan $R$ suatu domain integral dan $M$ suatu monoid komutatif bebas torsi
yang memenuhi hukum pembatalan. Maka gelanggang monoid $R[M]$ merupakan
domain integral.

#### Bukti {#br-ak-2025-2026-l20-thm-02-proof}

Mula-mula,

$$
M\subseteq\Gamma(M),
$$

dengan $\Gamma(M)$ grup selisih $M$. Karena itu

$$
R[M]\subseteq R[\Gamma(M)]
$$

merupakan subgelanggang, sehingga cukup membuktikan pernyataan untuk
$R[\Gamma(M)]$. Karena $M$ bebas torsi, menurut Soal 20.10 grup
$\Gamma(M)$ juga bebas torsi. Jadi kita boleh menganggap bahwa $M$ sendiri
merupakan grup komutatif bebas torsi.

Misalkan

$$
\left(\sum_{m\in M}a_mX^m\right)
\left(\sum_{m\in M}b_mX^m\right)=0.
$$

Hampir semua koefisien dalam kedua jumlah itu nol. Oleh karena itu seluruh
perhitungan berlangsung di dalam suatu subgrup $U$ yang dibangkitkan secara
hingga dari grup bebas torsi $M$. Menurut teorema utama tentang grup komutatif
bebas torsi yang dibangkitkan secara hingga,

$$
U\cong\mathbb Z^n.
$$

Dengan demikian kita bahkan boleh menganggap $M=\mathbb Z^n$. Dalam hal ini
$R[M]$ adalah pelokalan suatu gelanggang polinom di atas domain integral, dan
karena itu merupakan domain integral.

Tanpa hukum pembatalan, gelanggang monoid di atas suatu domain integral dapat
mempunyai pembagi nol.

<!-- upstream_entity: Kommutative Monoidringe/Grundring integer/Monoidring nicht integer/Beispiel -->

### Contoh: pembagi nol tanpa hukum pembatalan {#br-ak-2025-2026-l20-exa-01}

Misalkan $M$ suatu monoid yang memuat dua unsur berbeda $m$ dan $n$ dengan

$$
m+n=n+n.
$$

Tanpa hukum pembatalan, persamaan ini tidak mengakibatkan $m=n$. Di dalam
gelanggang monoid di atas domain integral sebarang $R$ berlaku

$$
X^m-X^n\ne0
\qquad\text{dan}\qquad
X^n\ne0,
$$

tetapi

$$
(X^m-X^n)X^n
=X^{m+n}-X^{n+n}
=X^{2n}-X^{2n}
=0.
$$

<!-- upstream_entity: Kommutative Monoidtheorie/Normalisierung in Differenzengruppe und normal/Definition -->

### Definisi: normalisasi monoid {#br-ak-2025-2026-l20-def-04}

Misalkan $M$ suatu monoid komutatif bebas torsi yang memenuhi hukum
pembatalan, dengan grup selisih $\Gamma(M)$. Submonoid

$$
\widetilde M
=\{m\in\Gamma(M)\mid
\text{terdapat }r\in\mathbb N_+\text{ dengan }rm\in M\}
$$

disebut *normalisasi* $M$.

<!-- upstream_entity: Kommutative Monoidtheorie/Normalisierung/Monoid und Monoidring/Fakt -->

### Teorema: normalisasi gelanggang monoid {#br-ak-2025-2026-l20-thm-03}

Misalkan $M$ suatu monoid komutatif bebas torsi yang memenuhi hukum
pembatalan, dengan grup selisih $\Gamma(M)$ dan normalisasi

$$
M\subseteq\widetilde M\subseteq\Gamma(M).
$$

Misalkan pula $R$ suatu domain integral normal. Maka normalisasi gelanggang
monoid $R[M]$ ialah gelanggang monoid

$$
R[\widetilde M].
$$

Khususnya, gelanggang monoid dari suatu monoid normal di atas gelanggang
normal juga normal.

#### Bukti {#br-ak-2025-2026-l20-thm-03-proof}

Mula-mula,

$$
R[M]\subseteq R[\widetilde M]
\subseteq R[\Gamma(M)]
\subseteq Q(R)[\Gamma(M)]
\subseteq Q(R[M]).
$$

Ambil $m\in\widetilde M$ dengan

$$
m=n-k,
\qquad n,k\in M,
$$

dan dengan

$$
rm=\underbrace{m+\cdots+m}_{r\text{ kali}}\in M.
$$

Maka

$$
T^m=\frac{T^n}{T^k}
$$

merupakan unsur lapangan pecahan, sedangkan

$$
(T^m)^r\in R[M].
$$

Jadi $T^m$ memenuhi suatu persamaan keintegralan murni di atas $R[M]$ dan
berada dalam normalisasi $R[M]$. Dengan demikian,

$$
R[\widetilde M]\subseteq R[M]^{\operatorname{norm}}.
$$

**Catatan edisi:** pada dua rumus terakhir sumber mengganti gelanggang dasar
$R$ dengan $K$, meskipun teorema dan seluruh argumen menetapkan $R$. Edisi
ini mempertahankan $R$ secara konsisten. Sumber juga mencetak $rm=M$ pada
syarat definisi; sesuai definisi $\widetilde M$, relasi yang diperlukan dan
ditampilkan di sini ialah $rm\in M$.

Untuk inklusi sebaliknya, kita dapat mengganti $M$ dengan $\widetilde M$ dan
karena itu membatasi diri pada kasus ketika $M$ normal. Pertama-tama dibuktikan
bahwa, untuk grup komutatif bebas torsi $G$, gelanggang grup $R[G]$ normal.
Hal ini mengikuti dari fakta bahwa gelanggang polinom di atas suatu domain
normal kembali normal. Selanjutnya harus ditunjukkan bahwa $R[M]$ tertutup
secara integral di dalam $R[\Gamma(M)]$.

Suatu unsur

$$
q\in R(\Gamma(M))
$$

beserta persamaan keintegralannya berada di dalam gelanggang monoid dari suatu
subgrup yang dibangkitkan secara hingga

$$
U\subseteq\Gamma(M).
$$

Karena itu kita boleh menganggap

$$
\Gamma(M)=\mathbb Z^n.
$$

Pada titik ini masuk sedikit geometri konveks, yang tidak kita uraikan.
Bagaimanapun, suatu submonoid normal

$$
M\subseteq\mathbb Z^n
$$

dapat dinyatakan sebagai irisan $\mathbb Z^n$ dengan suatu kerucut polihedral
di dalam $\mathbb Q^n$ atau $\mathbb R^n$. Menurut lema Gordan, kerucut
tersebut pada gilirannya merupakan irisan berhingga dari setengah ruang
$H_i$. Suatu setengah ruang $H$ diberikan oleh pemetaan linear

$$
p:V=\mathbb R^n\longrightarrow\mathbb R
$$

melalui

$$
H=p^{-1}(\mathbb R_+).
$$

Karena itu $M$ merupakan irisan berhingga

$$
M=\bigcap_{i\in I}M_i,
\qquad
M_i=p_i^{-1}(\mathbb N),
$$

dengan

$$
M_i\cong\mathbb N\times\mathbb Z^{n-1}.
$$

Akibatnya,

$$
R[M]=\bigcap_{i\in I}R[M_i]
$$

normal menurut Soal 20.7, sebab setiap

$$
R[M_i]\cong R[\mathbb N\times\mathbb Z^{n-1}]
$$

normal.

<!-- upstream_entity: Monoidringe/Dimension zwei/Whitney Regenschirm/X^2Y-Z^2/Beispiel -->

### Contoh: payung Whitney {#br-ak-2025-2026-l20-exa-02}

![Permukaan abu-abu kebiruan berbentuk payung Whitney yang berpotongan sendiri di ruang tiga dimensi](authority/assets/Whitney_unbrella.png)

*Payung Whitney. Claudio Rocchini,
[CC BY 2.5](https://creativecommons.org/licenses/by/2.5/). Label lisensi
sebaris pada sumber berbeda dari opsi yang tersedia pada metadata Commons;
rincian pembekuan hak berada pada kredit media Unit 20.*

Tinjau permukaan aljabar yang diberikan oleh persamaan

$$
X^2Z=Y^2.
$$

Kita akan memahaminya sebagai permukaan yang terkait dengan suatu gelanggang
monoid. Tetapkan

$$
M=\langle(1,0),(1,1),(0,2)\rangle\subseteq\mathbb N^2.
$$

Karena

$$
(1,1)-(1,0)=(0,1),
$$

grup selisihnya ialah $\mathbb Z^2$. Selain itu,

$$
2(0,1)=(0,2)\in M,
$$

sehingga $\mathbb N^2$ merupakan normalisasi $M$. Ketiga pembangkit memberikan
homomorfisme monoid surjektif

$$
\begin{aligned}
\mathbb N^3&\longrightarrow M,\\
e_i&\longmapsto m_i.
\end{aligned}
$$

Secara geometris, pemetaan monomial

$$
\mathbb N^3\longrightarrow M\subseteq\mathbb N^2
$$

bersesuaian dengan pemetaan

$$
\begin{aligned}
\mathbb A_K^2&\longrightarrow
K\!-!\operatorname{Spek}(K[M])\hookrightarrow\mathbb A_K^3,\\
(s,t)&\longmapsto(s,st,t^2).
\end{aligned}
$$

Di bawah homomorfisme monoid tersebut,

$$
2e_1+e_3\longmapsto(2,2)
\qquad\text{dan}\qquad
2e_2\longmapsto(2,2).
$$

Hal ini menghasilkan persamaan

$$
X^2Z=Y^2,
$$

yang tentu juga dapat dibaca langsung dari parametrisasi.

**Catatan edisi:** sumber mencetak bahwa kedua unsur itu dipetakan ke
$(1,1)$. Dari pembangkit yang ditampilkan, keduanya dipetakan ke $(2,2)$.
Edisi memperbaiki koordinat ini secara transparan; relasi $X^2Z=Y^2$ tidak
berubah.

Persamaan pendefinisi juga dapat ditulis sebagai

$$
Z=\left(\frac YX\right)^2.
$$

Jadi, berangkat dari $K[X,Y]$, kita mengadjoin kuadrat dari $Y/X$.

<!-- upstream_entity: Monoidringe/Dimension zwei/Standardkegel/Z^2-XY/Monoid und Bewertungen/Beispiel -->

### Contoh: kerucut standar monomial {#br-ak-2025-2026-l20-exa-03}

Tinjau submonoid

$$
M=\langle(1,0),(-1,2),(0,1)\rangle\subseteq\mathbb Z^2.
$$

Untuk gelanggang monoid yang terkait berlaku

$$
K[M]\cong K[X,Y,Z]/(Z^2-XY).
$$

Kita klaim bahwa monoid tersebut normal, yakni sama dengan normalisasinya.
Dua pembangkit $(1,0)$ dan $(-1,2)$ masing-masing menentukan sebuah garis di
$\mathbb R^2$, dan monoid itu terdiri atas semua titik kisi di dalam kerucut
yang ditentukan oleh kedua garis tersebut. Titik-titik kisi dalam kerucut ini
diberikan oleh dua syarat

$$
\{(s,t)\in\mathbb Z^2\mid t\geq0\text{ dan }t\geq-2s\}.
$$

Suatu titik di dalam himpunan ini dengan $s\geq0$ jelas berada di $M$.
Sekarang misalkan $(s,t)$ suatu titik di dalam himpunan tersebut dengan
$s<0$. Berdasarkan syarat linear kedua, kita dapat menulis

$$
(s,t)=-s(-1,2)+(t+2s)(0,1),
$$

dan titik ini berada di $M$ karena $t+2s\geq0$.

Dengan kedua garis tersebut, $M$ juga langsung dapat dideskripsikan sebagai

$$
M=M_1\cap M_2,
$$

dengan

$$
M_1=\{(s,t)\in\mathbb Z^2\mid t\geq0\}
\cong\mathbb Z\times\mathbb N
$$

dan

$$
M_2=\{(s,t)\in\mathbb Z^2\mid t\geq-2s\}
\cong\mathbb Z\times\mathbb N.
$$

Identifikasi kedua berasal dari basis-$\mathbb Z$
$(-1,2),(0,1)$. Dari deskripsi eksplisit ini mengikuti bahwa gelanggang
monoid yang terkait normal.

## Kurva monomial dan normalisasi {#br-ak-2025-2026-l20-s03}

Kelak kita akan melihat bahwa suatu kurva aljabar normal jika dan hanya jika
kurva itu nonsingular. Dalam kasus kurva monomial, normalisasinya dapat
dideskripsikan dengan mudah.

<!-- upstream_entity: Affine Kurven/Monomiale Kurvenabbildung/Ist Normalisierung/Fakt -->

### Teorema: normalisasi kurva monomial {#br-ak-2025-2026-l20-thm-04}

Misalkan

$$
M\subseteq\mathbb N
$$

suatu submonoid yang dibangkitkan oleh bilangan-bilangan saling prima
$e_1,\ldots,e_n$, dan misalkan

$$
K[M]\subseteq K[T]
$$

perluasan gelanggang monoid yang terkait. Maka $K[T]$ merupakan normalisasi
$K[M]$.

Dengan kata lain, pemetaan monomial

$$
\mathbb A_K^1\longrightarrow K\!-!\operatorname{Spek}(K[M])
$$

merupakan suatu normalisasi.

#### Bukti {#br-ak-2025-2026-l20-thm-04-proof}

Kita mempunyai

$$
K[M]=K[T^{e_1},\ldots,T^{e_n}]\subseteq K[T].
$$

Karena eksponen-eksponennya saling prima, eksponen-eksponen itu membangkitkan
$1$. Jika dipandang secara multiplikatif, ini berarti bahwa terdapat suatu
monomial dalam pangkat-pangkat tersebut, dengan eksponen negatif juga
diizinkan, yang sama dengan $T$. Jadi $T$ merupakan hasil bagi unsur-unsur
$K[M]$, dan kedua lapangan pecahannya sama.

Di sisi lain, $T$ memenuhi persamaan keintegralan atas $K[M]$, misalnya

$$
X^{e_1}-T^{e_1}=0.
$$

Di sini $X$ adalah variabel polinom, sedangkan $T^{e_1}$ merupakan koefisien
di $K[M]$. Karena $K[T]$ normal—bahkan merupakan domain faktorisasi tunggal,
sebab ia domain ideal utama—maka $K[T]$ adalah normalisasi $K[M]$.

**Catatan edisi:** sumber memakai simbol $T$ untuk variabel polinom sekaligus
untuk unsur yang diuji, lalu menambahkan keterangan “dibaca dengan benar”.
Edisi membedakan keduanya dengan menamai variabel polinom $X$; isi matematis
tidak berubah.

Dengan demikian kurva-kurva monomial menyediakan banyak contoh ketika
normalisasi merupakan bijeksi pada tingkat spektrum-$K$. Pemetaan itu juga
merupakan homeomorfisme untuk topologi Zariski, yang pada kasus kurva memang
sangat sederhana. Namun, keliru jika kedua kurva dianggap identik. Jika
$e_i\ne1$ untuk semua $i$, normalisasi pada tingkat gelanggang bukanlah
bijeksi. Dalam geometri aljabar kita tidak boleh hanya memandang wujud
himpunan nol secara himpunan atau topologis; gelanggang dan persamaan yang
mendasarinya tidak boleh dilupakan. Perbedaannya juga tampak dalam situasi
terbenam, ketika parabola Neil mempunyai sebuah cusp.

Normalisasi memberi interpretasi baru bagi derajat singularitas kurva
monomial.

<!-- upstream_entity: Numerische Halbgruppe/Teilerfremde Erzeuger/Singularitätsgrad/Beziehung zur Normalisierung/Fakt -->

### Lema: derajat singularitas sebagai dimensi normalisasi {#br-ak-2025-2026-l20-lem-02}

Misalkan $M\subseteq\mathbb N$ suatu monoid numerik yang ditentukan oleh
pembangkit-pembangkit saling prima. Misalkan

$$
R=K[M]
$$

gelanggang monoid yang terkait dan

$$
R^{\operatorname{norm}}=K[T]
$$

normalisasinya. Maka

$$
\delta(M)=\dim_K\bigl(R^{\operatorname{norm}}/R\bigr).
$$

#### Bukti {#br-ak-2025-2026-l20-lem-02-proof}

Normalisasi mempunyai basis-$K$

$$
\{T^m\mid m\in\mathbb N\},
$$

sedangkan gelanggang monoid $K[M]$ mempunyai basis-$K$

$$
\{T^m\mid m\in M\}.
$$

Karena itu ruang faktor

$$
K[T]/K[M]
$$

mempunyai basis-$K$

$$
\{T^m\mid m\in\mathbb N\setminus M\}.
$$

Dimensi ruang faktor adalah banyak unsur suatu basis, yaitu banyak celah
$M$. Jumlah ini persis derajat singularitas $M$.

---

**Provenans edisi.** Terjemahan dan produksi pembaca: OpenAI Codex
gpt-5.6-sol, Ultra. Sumber, pengarang, dan lisensi komponen dipertahankan
seperti dinyatakan dalam metadata dan berkas hak edisi.
