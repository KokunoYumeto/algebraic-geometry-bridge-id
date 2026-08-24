---
title: "Kuliah 18 - Kurva Monomial dan Monoid Numerik"
stable_id: br-ak-2025-2026-l18
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 18"
upstream_pageid: 165907
upstream_revid: 1051383
upstream_timestamp: "2025-08-18T08:13:31Z"
upstream_mediawiki_sha1: a30ad183e1e879bf7fec6ce414cbfad149b89bb1
source_url: "https://de.wikiversity.org/w/index.php?oldid=1051383"
authority_manifest: authority/wikiversity/unit-18/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 26a56a0ccad60414bf09320dc008d438ccf84b3dd11c12c31e80fa6088437033
lecture_xml_sha256: 442e5b76c1d65a58fd5fe03f327cb07b5649dd183c932a5ef3512a3876925c03
lecture_expanded_tex_sha256: 4625196e696979389e6e4bd06182249a09fbe04dfdf7928ff1cc4a50a841ea03
license: "CC BY-SA 4.0 for translated course text; the figure retains component rights in authority/RIGHTS-unit-18.csv"
translation_status: complete
---

# Kuliah 18: Kurva Monomial dan Monoid Numerik {#br-ak-2025-2026-l18}

## Kurva monomial {#br-ak-2025-2026-l18-s01}

Sekarang kita mengkhususkan teori gelanggang monoid pada kasus satu dimensi
dan memperoleh gelanggang-gelanggang yang mendeskripsikan kurva monomial.

<!-- upstream_entity: Affine Kurven/Monomiale Kurve/Definition -->

### Definisi: kurva monomial {#br-ak-2025-2026-l18-def-01}

Suatu *kurva monomial* adalah citra garis afin $\mathbb A_K^1$ di bawah
pemetaan berbentuk

$$
\begin{aligned}
\mathbb A_K^1&\longrightarrow\mathbb A_K^n,\\
t&\longmapsto(t^{e_1},\ldots,t^{e_n}),
\end{aligned}
$$

dengan $e_i\geq1$ untuk semua $i$.

Kita akan segera melihat bahwa citra pemetaan monomial semacam itu tertutup
secara Zariski. Jadi kurva monomial benar-benar merupakan kurva aljabar.
Karena terparametrisasi, kurva monomial merupakan kurva rasional, tetapi pada
umumnya bukan kurva bidang. Kadang-kadang pemetaannya sendiri juga disebut
kurva monomial.

Sering kali kita membatasi perhatian pada eksponen $e_i$ yang secara bersama
saling prima. Ini bukan pembatasan penting. Jika $m$ adalah faktor persekutuan
terbesar semua $e_i$, kita dapat menulis

$$
e_i=mf_i
$$

dengan $f_1,\ldots,f_n$ saling prima, lalu memfaktorkan pemetaan sebagai

$$
\mathbb A_K^1\longrightarrow\mathbb A_K^1\longrightarrow\mathbb A_K^n,
\qquad
t\longmapsto t^m=s,
\qquad
s\longmapsto(s^{f_1},\ldots,s^{f_n}).
$$

Pemetaan pertama hanyalah pemangkatan, sedangkan pemetaan kedua adalah
pemetaan kurva monomial dengan eksponen saling prima.

**Catatan edisi:** meskipun domain pemetaan kedua adalah garis afin dengan
koordinat tunggal $s$, sumber mencetak koordinat citranya sebagai
$(s_1^{f_1},\ldots,s_n^{f_n})$. Edisi ini menampilkan pangkat dari input
skalar yang telah didefinisikan, yakni $(s^{f_1},\ldots,s^{f_n})$.

<!-- upstream_entity: Monomiale Kurvenabbildung/Monoidhomomorphismus/Bemerkung -->

### Catatan: pemetaan monoid yang mendasari {#br-ak-2025-2026-l18-rem-01}

Pemetaan monomial

$$
t\longmapsto(t^{e_1},\ldots,t^{e_n})
$$

tidak lain adalah pemetaan spektrum-$K$ yang bersesuaian dengan homomorfisme
monoid

$$
\mathbb N^n\longrightarrow\mathbb N
$$

yang membawa vektor basis ke-$i$ ke $e_i$; bandingkan Catatan 17.9.

**Catatan edisi:** sumber mencetak koordinat sebagai
$(t_1^{e_1},\ldots,t_n^{e_n})$, padahal inputnya adalah skalar tunggal $t$.
Edisi ini menampilkan koordinat yang bertipe benar.

Homomorfisme monoid tersebut memfaktor sebagai

$$
\mathbb N^n\longrightarrow M\longrightarrow\mathbb N,
$$

dengan $M$ submonoid $\mathbb N$ yang dibangkitkan oleh $e_1,\ldots,e_n$.
Submonoid semacam itu disebut *monoid numerik*. Pemetaan pertama surjektif.
Pada taraf gelanggang kita memperoleh

$$
K[\mathbb N^n]=K[X_1,\ldots,X_n]
\longrightarrow K[M]
\longrightarrow K[\mathbb N]=K[T],
$$

sedangkan secara geometris kita memperoleh pemetaan spektrum

$$
\mathbb A_K^1
\longrightarrow
K\!-\!\operatorname{Spek}(K[M])
\subseteq\mathbb A_K^n.
$$

Jadi citra garis afin berada di dalam spektrum-$K$ gelanggang monoid $K[M]$.
Teorema 18.10 akan menunjukkan bahwa

$$
\mathbb A_K^1\longrightarrow K\!-\!\operatorname{Spek}(K[M])
$$

selalu surjektif dan, jika eksponen-eksponennya saling prima, juga injektif.

<!-- upstream_entity: Ebene monomiale Kurven/Neilsche Parabel/Beispiel -->

### Contoh: parabola Neil {#br-ak-2025-2026-l18-exa-01}

![Kurva berbentuk cusp dengan dua cabang halus yang bertemu runcing di titik asal](authority/assets/Cusp-500.png)

*Parabola Neil dengan titik singular kuspidal di titik asal. Georg-Johann,
[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). Rincian
sumber dan perbedaan label hak berada pada kredit media Unit 18.*

*Parabola Neil* $C$ adalah citra pemetaan monomial

$$
\begin{aligned}
\mathbb A_K^1&\longrightarrow\mathbb A_K^2,\\
t&\longmapsto(t^2,t^3)=(x,y).
\end{aligned}
$$

Persamaan yang terkait adalah

$$
y^2=x^3,
$$

sehingga

$$
C=V(Y^2-X^3).
$$

Kurva monomial hanya ditentukan oleh tuple eksponen
$(e_1,\ldots,e_n)$, atau ekuivalen oleh monoid numerik yang dibangkitkannya.
Jadi data kombinatorial yang diperlukan sangat sedikit. Walaupun demikian,
kurva-kurva ini menyediakan banyak contoh yang kaya dalam teori kurva
aljabar. Fenomena serupa berlaku lebih umum untuk gelanggang monoid dan
varietas aljabar yang didefinisikannya.

## Invarian monoid numerik {#br-ak-2025-2026-l18-s02}

<!-- upstream_entity: Numerische Halbgruppe/Teilerfremde Erzeuger/Ab n alles/Fakt -->

### Lema: semua bilangan yang cukup besar berada di dalam monoid {#br-ak-2025-2026-l18-lem-01}

Misalkan $M\subseteq\mathbb N$ monoid numerik yang dibangkitkan oleh bilangan
asli saling prima $e_1,\ldots,e_n$. Untuk setiap $m\in\mathbb N$ terdapat
penyajian

$$
m=a_1e_1+\cdots+a_ne_n
$$

dengan

$$
0\leq a_i<e_{i+1},
\qquad 1\leq i\leq n-1.
$$

Jika $m$ cukup besar, kita juga dapat memilih $a_n\geq0$, sehingga semua
koefisien dalam penyajian tersebut tak negatif.

#### Bukti {#br-ak-2025-2026-l18-lem-01-proof}

Karena $e_1,\ldots,e_n$ saling prima, mula-mula terdapat penyajian

$$
m=b_1e_1+\cdots+b_ne_n
$$

dengan koefisien bilangan bulat. Kita ubah penyajian ini langkah demi langkah.
Dengan pembagian bersisa, tuliskan

$$
b_1=c_1e_2+a_1,
\qquad
0\leq a_1<e_2.
$$

Substitusikan ke penyajian $m$ dan gabungkan suku $c_1e_2e_1$ dengan
$b_2e_2$. Koefisien kedua yang baru kemudian diproses bersama pembangkit
ketiga dengan cara yang sama. Dengan melanjutkan proses ini, semua koefisien
pertama sampai ke-$(n-1)$ memperoleh bentuk yang diinginkan.

Dalam bentuk tersebut, jumlah $n-1$ suku pertama terbatas oleh suatu konstanta
yang hanya bergantung pada para pembangkit. Jika $m$ melampaui batas itu,
suku terakhir, dan karenanya koefisien terakhir $a_n$, harus tak negatif.

Jadi, mulai dari suatu ambang tertentu, setiap bilangan asli berada di dalam
monoid yang dibangkitkan oleh eksponen-eksponen saling prima itu. Ambang
minimal tersebut memperoleh nama khusus.

<!-- upstream_entity: Numerische Halbgruppe/Teilerfremde Erzeuger/Führungszahl/Definition -->

### Definisi: bilangan konduktor {#br-ak-2025-2026-l18-def-02}

Misalkan $M\subseteq\mathbb N$ monoid numerik yang dibangkitkan oleh
pembangkit-pembangkit saling prima. Bilangan terkecil $f$ yang memenuhi

$$
\mathbb N_{\geq f}\subseteq M
$$

disebut *bilangan konduktor* $M$.

Invarian-invarian berikut juga dapat dihitung secara diskret pada taraf monoid
numerik. Kelak kita akan mendefinisikannya untuk kurva aljabar sebarang; pada
keumuman itu, penghitungannya biasanya lebih sulit.

<!-- upstream_entity: Numerische Halbgruppe/Teilerfremde Erzeuger/Numerische Einbettungsdimension/Definition -->

### Definisi: dimensi penyematan {#br-ak-2025-2026-l18-def-03}

Misalkan $M\subseteq\mathbb N$ monoid numerik dengan pembangkit-pembangkit
saling prima. Jumlah unsur terkecil di antara semua sistem pembangkit $M$
disebut *dimensi penyematan* $M$.

<!-- upstream_entity: Numerische Monoide/Teilerfremde Erzeuger/Numerische Multiplizität/Definition -->

### Definisi: multiplisitas {#br-ak-2025-2026-l18-def-04}

Misalkan $M\subseteq\mathbb N$ monoid numerik dengan pembangkit-pembangkit
saling prima. Unsur positif terkecil

$$
e\in M,
\qquad e\geq1,
$$

disebut *multiplisitas* $M$ dan ditulis $e(M)$.

<!-- upstream_entity: Numerische Halbgruppe/Teilerfremde Erzeuger/Singularitätsgrad/Definition -->

### Definisi: derajat singularitas {#br-ak-2025-2026-l18-def-05}

Misalkan $M\subseteq\mathbb N$ monoid numerik dengan pembangkit-pembangkit
saling prima. Banyak celah, yakni banyak unsur dalam

$$
\mathbb N\setminus M,
$$

disebut *derajat singularitas* $M$ dan ditulis $\delta(M)$.

<!-- upstream_entity: Numerisches Monoid/5,8,11/Invarianten/Beispiel -->

### Contoh: monoid yang dibangkitkan oleh 5, 8, dan 11 {#br-ak-2025-2026-l18-exa-02}

Tinjau monoid numerik $M$ yang dibangkitkan oleh $5,8,11$. Jadi $M$ terdiri
atas semua jumlah

$$
5a_1+8a_2+11a_3,
\qquad a_1,a_2,a_3\geq0.
$$

Unsur-unsurnya mencakup

$$
0,5,8,10,11,13,15,16,18,19,20,21,22,23,24,25,\ldots.
$$

Karena $18,19,20,21,22$ merupakan lima bilangan berurutan di $M$ dan
$5\in M$, semua bilangan setelahnya juga berada di $M$. Karena itu bilangan
konduktornya $18$, multiplisitasnya $5$, derajat singularitasnya $10$, dan
dimensi penyematannya $3$.

## Parametrisasi dan sistem pembangkit kanonik {#br-ak-2025-2026-l18-s03}

<!-- upstream_entity: Monomiale Kurvenabbildung/Bijektiv/Fakt -->

### Teorema: parametrisasi monomial adalah bijeksi {#br-ak-2025-2026-l18-thm-01}

Misalkan $M\subseteq\mathbb N$ submonoid yang dibangkitkan oleh bilangan asli
saling prima $e_1,\ldots,e_n$. Pemetaan monomial

$$
\mathbb A_K^1\longrightarrow K\!-\!\operatorname{Spek}(K[M])
$$

merupakan bijeksi.

#### Bukti {#br-ak-2025-2026-l18-thm-01-proof}

Menurut Catatan 17.9, pemetaan ini dapat dipandang sebagai pemetaan alami

$$
\mathbb A_K^1
=\operatorname{Mor}_{\mathrm{mon}}(\mathbb N,K)
\longrightarrow
\operatorname{Mor}_{\mathrm{mon}}(M,K)
$$

yang diinduksi oleh inklusi $M\subseteq\mathbb N$.

Untuk membuktikan injektivitas, misalkan $a,b\in K$ dan

$$
a^m=b^m
$$

untuk semua $m\in M$. Jika $b=0$, segera diperoleh $a=0$. Jadi anggap
$b\ne0$; dengan cara yang sama $a\ne0$. Menurut Lema 18.4, mulai dari suatu
$f$, semua bilangan asli berada di $M$. Khususnya,

$$
a^f=b^f,
\qquad
a^{f+1}=b^{f+1}.
$$

Maka

$$
a=\frac{a^{f+1}}{a^f}
=\frac{b^{f+1}}{b^f}
=b.
$$

Untuk surjektivitas, berikan homomorfisme monoid

$$
\varphi:M\longrightarrow K.
$$

Kita harus memperluasnya ke seluruh $\mathbb N$. Tuliskan

$$
\varphi(e_i)=a_i\in K.
$$

Nilai-nilai ini memenuhi

$$
a_j^{e_i}
=\varphi(e_j)^{e_i}
=\varphi(e_ie_j)
=\varphi(e_i)^{e_j}
=a_i^{e_j}.
$$

Jika salah satu $a_i=0$, semua $a_i=0$, dan pemetaan yang membawa setiap
bilangan positif ke $0$ (serta $0$ ke $1$) memberi perluasan. Jadi kita dapat
menganggap semua $a_i$ satuan.

Karena $e_i$ saling prima, terdapat $m_1,\ldots,m_n\in\mathbb Z$ dengan

$$
m_1e_1+\cdots+m_ne_n=1.
$$

Tetapkan

$$
a=a_1^{m_1}\cdots a_n^{m_n}.
$$

Kita klaim bahwa homomorfisme $\mathbb N\to K$ yang ditentukan oleh
$1\mapsto a$, yakni $k\mapsto a^k$, memperluas $\varphi$. Cukup memeriksanya
pada semua $e_i$. Untuk $e_1$,

$$
\begin{aligned}
a^{e_1}
&=(a_1^{m_1}\cdots a_n^{m_n})^{e_1}\\
&=a_1^{e_1m_1}a_2^{e_1m_2}\cdots a_n^{e_1m_n}\\
&=a_1^{1-\sum_{i=2}^nm_ie_i}
  (a_2^{e_1m_2}\cdots a_n^{e_1m_n})\\
&=a_1(a_1^{-e_2}a_2^{e_1})^{m_2}
  \cdots(a_1^{-e_n}a_n^{e_1})^{m_n}\\
&=a_1,
\end{aligned}
$$

karena setiap faktor dalam baris kedua terakhir sama dengan $1$ menurut
relasi $a_j^{e_i}=a_i^{e_j}$. Argumen yang sama berlaku untuk setiap $e_i$.

<!-- upstream_entity: Monomiale Kurven/Affin/Über Monoidringe/Einführung/Textabschnitt -->

### Catatan: bukti melalui grup selisih {#br-ak-2025-2026-l18-rem-02}

Surjektivitas teorema di atas juga dapat dilihat melalui sifat universal grup
selisih. Grup selisih monoid numerik dengan pembangkit saling prima adalah
$\mathbb Z$. Kasus ketika suatu pembangkit dipetakan ke nol ditangani seperti
dalam bukti. Jika semua citra bukan nol, kita memperoleh homomorfisme monoid

$$
\varphi:M\longrightarrow K^\times.
$$

Sifat universal grup selisih memberikan perluasan tunggal

$$
\widetilde\varphi:\mathbb Z\longrightarrow K^\times,
$$

yang menghasilkan pra-citra yang diperlukan.

**Catatan edisi:** pada langkah ini sumber menyebut sifat universal gelanggang
monoid. Konstruksi yang benar-benar digunakan adalah perluasan dari $M$ ke
grup selisihnya $\mathbb Z$, sehingga edisi ini menampilkan sifat universal
grup selisih.

Dua pernyataan berikut menunjukkan bahwa monoid numerik mempunyai sistem
pembangkit kanonik. Dengan demikian dimensi penyematan memperoleh interpretasi
yang kelak dapat dialihkan ke gelanggang lokal Noether sebarang. Gelanggang
monoid itu sendiri tentu tidak lokal, tetapi pelokalannya pada singularitas
monoid numerik bersifat lokal.

<!-- upstream_entity: Numerische Halbgruppe/Teilerfremde Erzeuger/Minimales Standard-Erzeugendensystem/Fakt -->

### Lema: sistem pembangkit minimal kanonik {#br-ak-2025-2026-l18-lem-02}

Misalkan $M\subseteq\mathbb N$ monoid numerik dengan pembangkit-pembangkit
saling prima. Tetapkan

$$
M_+=\{m\in M\mid m\geq1\}
$$

dan

$$
M_++M_+=\{m+m'\mid m,m'\in M_+\}.
$$

Maka

$$
M_+\setminus(M_++M_+)
$$

merupakan sistem pembangkit $M$, dan setiap sistem pembangkit lain memuat
himpunan ini.

#### Bukti {#br-ak-2025-2026-l18-lem-02-proof}

Suatu unsur

$$
m\in M_+\setminus(M_++M_+)
$$

tidak dapat ditulis sebagai jumlah dua unsur positif lain dari $M$. Karena itu
ia harus berada dalam setiap sistem pembangkit.

Sebaliknya, himpunan tersebut sudah membangkitkan $M$. Jika tidak, pilih unsur
terkecil $x\in M$ yang tidak dibangkitkannya. Karena $x$ bukan anggota
$M_+\setminus(M_++M_+)$, terdapat

$$
x=x_1+x_2,
\qquad x_1,x_2\in M_+.
$$

Kedua suku lebih kecil daripada $x$, sehingga masing-masing dapat ditulis
sebagai jumlah unsur-unsur dari himpunan kanonik. Ini langsung memberi
kontradiksi.

**Catatan edisi:** sumber mencetak $x_1,x_2\in M_++M_+$. Dari
$x\in M_++M_+$, definisi himpunan jumlah hanya memberikan
$x_1,x_2\in M_+$, dan keanggotaan inilah yang diperlukan untuk argumen
descent minimal.

<!-- upstream_entity: Numerische Halbgruppe/Teilerfremde Erzeuger/Numerische Einbettungsdimension/Charakterisierung mit M+ ohne M+^2/Fakt -->

### Korolari: dimensi penyematan dari pembangkit kanonik {#br-ak-2025-2026-l18-cor-01}

Dalam situasi lema di atas, dimensi penyematan $M$ sama dengan banyak unsur
dalam

$$
M_+\setminus(M_++M_+).
$$

#### Bukti {#br-ak-2025-2026-l18-cor-01-proof}

Pernyataan ini langsung mengikuti dari Lema 18.12.

---

**Provenans edisi.** Terjemahan dan produksi pembaca: OpenAI Codex
gpt-5.6-sol, Ultra. Sumber, pengarang, dan lisensi komponen dipertahankan
seperti dinyatakan dalam metadata dan berkas hak edisi.
