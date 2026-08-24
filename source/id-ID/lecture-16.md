---
title: "Kuliah 16 - Filter Tak Tereduksi, Morfisme, dan Serat"
stable_id: br-ak-2025-2026-l16
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 16"
upstream_pageid: 165905
upstream_revid: 1060232
upstream_timestamp: "2025-11-29T13:15:50Z"
upstream_mediawiki_sha1: 59d50c0b858c5aa9b4a4be3b54c7336553e04482
source_url: "https://de.wikiversity.org/w/index.php?oldid=1060232"
authority_manifest: authority/wikiversity/unit-16/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 54c823b4aa99c6e37e1fd3f84754f290bb54500847800906569704c3b4d49da0
lecture_xml_sha256: 09f11700588ae9dd68416ee6d4ebca4910afe8ea87f37b532eaccaa0faa0259a
lecture_expanded_tex_sha256: 73e169f7b2f2fd447a150daa2f45edd213fd13c43b8fd5d151e28e89de82c72e
license: "CC BY-SA 4.0 for translated course text; media retain component rights in authority/RIGHTS-unit-16.csv"
translation_status: complete
---

# Kuliah 16: Filter Tak Tereduksi, Morfisme, dan Serat {#br-ak-2025-2026-l16}

## Filter tak tereduksi {#br-ak-2025-2026-l16-s01}

![Bubuk kopi tertahan di dalam kertas penyaring yang ditempatkan pada penyangga keramik putih](authority/assets/Kaffeefilter-500.jpg)

*Suatu filter dapat diidentifikasi dengan apa yang tertahan di dalamnya.
Elke Wetzig (Elya), [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).
Rincian sumber berada pada kredit media Unit 16.*

Pada kuliah sebelumnya kita melihat bahwa suatu titik $P$ di spektrum-$K$

$$
K\!-\!\operatorname{Spek}(R)
$$

menentukan filter lingkungannya, dan bahwa tangkai pada filter itu sama dengan
pelokalan $R$ pada ideal maksimal yang bersesuaian

$$
\mathfrak m_P\subseteq R.
$$

Kita juga melihat bahwa, jika $R$ integral, tangkai pada filter semua himpunan
terbuka tak kosong menghasilkan lapangan pecahan $R$, yang pada gilirannya
merupakan pelokalan pada ideal nol. Hubungan ini diperumum oleh konsep filter
tak tereduksi.

<!-- upstream_entity: Topologische Filter/Irreduzibler Filter/Definition -->

### Definisi: filter tak tereduksi {#br-ak-2025-2026-l16-def-01}

Suatu filter topologis $F$ disebut *tak tereduksi* jika

$$
\varnothing\notin F
$$

dan memenuhi syarat berikut: jika $U,V$ dua himpunan terbuka dengan

$$
U\cup V\in F,
$$

maka $U\in F$ atau $V\in F$.

Untuk filter Zariski, yakni filter topologis dalam topologi Zariski, berlaku
korespondensi berikut.

<!-- upstream_entity: K-Spektrum/Irreduzible Filter, Primideale, irreduzible Teilmengen/Fakt -->

### Teorema: ideal prima, himpunan tertutup tak tereduksi, dan filter tak tereduksi {#br-ak-2025-2026-l16-thm-01}

Misalkan $K$ lapangan tertutup secara aljabar, $R$ aljabar-$K$ komutatif
bertipe hingga, dan

$$
X=K\!-\!\operatorname{Spek}(R).
$$

Objek-objek berikut saling bersesuaian:

1. ideal prima di $R$;
2. subhimpunan tertutup tak tereduksi dari $X$;
3. filter tak tereduksi di $X$.

Subhimpunan tertutup tak tereduksi $Y\subseteq X$ bersesuaian dengan filter

$$
F(Y)=\{U\subseteq X\mid U\text{ terbuka dan }U\cap Y\ne\varnothing\}.
$$

Tangkai berkas struktur pada filter ini adalah pelokalan $R_{\mathfrak p}$,
dengan $\mathfrak p$ ideal prima yang bersesuaian.

#### Bukti {#br-ak-2025-2026-l16-thm-01-proof}

Korespondensi antara ideal prima dan subhimpunan tertutup tak tereduksi sudah
diketahui: ideal prima $\mathfrak p$ bersesuaian dengan subhimpunan tertutup
tak tereduksi $V(\mathfrak p)$; lihat Lema 4.3 dan Proposisi 11.7.

Konstruksi yang diberikan untuk suatu himpunan tertutup tak tereduksi $Y$
memang menghasilkan filter tak tereduksi. Ketaktereduksiannya langsung dari
definisi; yang perlu diperiksa hanyalah sifat irisan filter. Misalkan

$$
U,V\in F(Y),
$$

sehingga $Y\cap U$ dan $Y\cap V$ tak kosong. Karena $Y$ tak tereduksi,

$$
(Y\cap U)\cap(Y\cap V)=Y\cap(U\cap V)
$$

juga tak kosong. Jadi $U\cap V\in F(Y)$.

Sekarang misalkan $F$ suatu filter topologis tak tereduksi. Kita klaim bahwa
komplemen dari

$$
S=\{f\in R\mid D(f)\in F\}
$$

merupakan ideal prima. Himpunan $S$ langsung merupakan sistem multiplikatif
jenuh. Tinggal dibuktikan bahwa komplemennya tertutup terhadap penjumlahan.
Misalkan $g,h\in R$ dan $g+h\in S$. Maka $D(g+h)\in F$. Karena

$$
D(g)\cup D(h)=D(g,h)\supseteq D(g+h),
$$

himpunan $D(g)\cup D(h)$ juga berada dalam $F$. Ketaktereduksian $F$
memberikan $D(g)\in F$ atau $D(h)\in F$, sehingga $g\in S$ atau $h\in S$.
Dengan demikian komplemen $S$ tertutup terhadap penjumlahan dan merupakan
ideal prima.

Komposisi ketiga korespondensi selalu kembali ke objek semula. Untuk melihat
hal ini, cukup gunakan bahwa suatu filter Zariski tak tereduksi dibangkitkan
oleh himpunan-himpunan terbuka berbentuk $D(f)$; lihat Soal 16.1. Pernyataan
mengenai tangkai merupakan kasus khusus Soal 15.27.

Filter yang terkait dengan suatu himpunan tertutup tak tereduksi $Y$ juga
disebut *filter generik* $Y$, dan tangkainya disebut *tangkai generik* $Y$.
Kasus khusus korespondensi dalam Teorema 16.2 memberi hubungan antara ideal
prima minimal, komponen tak tereduksi, dan ultrafilter. Di sisi lain terdapat
korespondensi antara ideal maksimal, titik, dan filter lingkungan.

## Morfisme antarvarietas {#br-ak-2025-2026-l16-s02}

<!-- upstream_entity: Quasiaffine Varietäten/K-Spektrum/Morphismus/Definition -->

### Definisi: morfisme {#br-ak-2025-2026-l16-def-02}

Misalkan $X$ dan $Y$ varietas kuasiafin, dan misalkan

$$
\psi:Y\longrightarrow X
$$

suatu pemetaan kontinu. Pemetaan $\psi$ disebut *morfisme* varietas
kuasiafin jika untuk setiap himpunan terbuka $U\subseteq X$ dan setiap fungsi
aljabar

$$
f\in\Gamma(U,\mathcal O),
$$

fungsi komposisi

$$
f\circ\psi:\psi^{-1}(U)\longrightarrow U
\stackrel{f}{\longrightarrow}\mathbb A_K^1
$$

berada di $\Gamma(\psi^{-1}(U),\mathcal O)$.

<!-- upstream_entity: K-Spektrum/Morphismus/Ringhomomorphismen zu offenen Mengen/Diagramm/Bemerkung -->

### Catatan: homomorfisme tarik-balik {#br-ak-2025-2026-l16-rem-01}

Menurut definisi, untuk setiap himpunan terbuka $U\subseteq X$, suatu
morfisme $\psi:Y\to X$ menginduksi homomorfisme gelanggang

$$
\widetilde\psi:
\Gamma(U,\mathcal O)
\longrightarrow
\Gamma(\psi^{-1}(U),\mathcal O).
$$

Khususnya, terdapat homomorfisme gelanggang global

$$
\widetilde\psi:
\Gamma(X,\mathcal O)
\longrightarrow
\Gamma(Y,\mathcal O).
$$

Jika $U_1\subseteq U_2$ merupakan himpunan terbuka di $X$, kita mempunyai
diagram komutatif pemetaan kontinu

$$
\begin{matrix}
\psi^{-1}(U_1)&\longrightarrow&U_1\\
\downarrow&&\downarrow\\
\psi^{-1}(U_2)&\longrightarrow&U_2,
\end{matrix}
$$

dengan panah vertikal berupa inklusi terbuka. Diagram ini menghasilkan
diagram komutatif homomorfisme gelanggang

$$
\begin{matrix}
\Gamma(\psi^{-1}(U_1),\mathcal O)&\longleftarrow&\Gamma(U_1,\mathcal O)\\
\uparrow&&\uparrow\\
\Gamma(\psi^{-1}(U_2),\mathcal O)&\longleftarrow&\Gamma(U_2,\mathcal O).
\end{matrix}
$$

**Catatan edisi:** sumber menyebut $U_1,U_2$ sebagai himpunan terbuka di
$Y$. Akan tetapi, definisi sebelumnya, ekspresi $\psi^{-1}(U_i)$, dan kedua
diagram menuntut $U_i\subseteq X$. Edisi ini menampilkan domain yang
ditentukan oleh konteks tersebut.

<!-- upstream_entity: K-Spektrum/Morphismus/Verknüpfung/Offene Einbettung/Fakt -->

### Proposisi: inklusi terbuka dan komposisi {#br-ak-2025-2026-l16-prop-01}

Misalkan $K$ lapangan tertutup secara aljabar dan $U,X,Y,Z$ varietas
kuasiafin. Maka:

1. suatu inklusi terbuka $U\subseteq X$ merupakan morfisme;
2. jika $\theta:Z\to Y$ dan $\psi:Y\to X$ morfisme, maka
   $\psi\circ\theta$ juga morfisme.

Sifat-sifat berikut lebih penting.

<!-- upstream_entity: K-Spektrum/Ringhomomorphismus induziert Morphismus/Fakt -->

### Teorema: homomorfisme aljabar menginduksi morfisme {#br-ak-2025-2026-l16-thm-02}

Misalkan $K$ lapangan tertutup secara aljabar dan $R,S$ aljabar-$K$
komutatif bertipe hingga, dengan spektrum-$K$

$$
X=K\!-\!\operatorname{Spek}(R),
\qquad
Y=K\!-\!\operatorname{Spek}(S).
$$

Setiap homomorfisme aljabar-$K$

$$
\varphi:R\longrightarrow S
$$

menginduksi pemetaan spektrum

$$
\varphi^*:Y\longrightarrow X
$$

yang merupakan morfisme.

#### Bukti {#br-ak-2025-2026-l16-thm-02-proof}

Menurut Teorema 12.7, pemetaan $\varphi^*:Y\to X$ sudah diketahui kontinu.
Misalkan $U\subseteq X$ terbuka, tetapkan

$$
V=(\varphi^*)^{-1}(U),
$$

dan ambil fungsi aljabar $f:U\to K$. Kita harus menunjukkan bahwa
$f\circ\varphi^*:V\to K$ juga aljabar. Ambil $P\in V$, tetapkan
$Q=\varphi^*(P)$, dan pilih

$$
Q\in D(H)\subseteq U,
\qquad
f=G/H\quad\text{pada }D(H),
\qquad G,H\in R.
$$

Menurut Teorema 12.7,

$$
P\in(\varphi^*)^{-1}(D(H))=D(\varphi(H)).
$$

Pada himpunan terbuka ini berlaku

$$
f\circ\varphi^*=\frac{\varphi(G)}{\varphi(H)}.
$$

Memang, untuk $\widetilde P\in D(\varphi(H))$,

$$
\begin{aligned}
(f\circ\varphi^*)(\widetilde P)
&=f(\varphi^*(\widetilde P))\\
&=\frac{G(\varphi^*(\widetilde P))}
        {H(\varphi^*(\widetilde P))}\\
&=\frac{(\varphi(G))(\widetilde P)}
        {(\varphi(H))(\widetilde P)}.
\end{aligned}
$$

Jadi komposisi itu lokalnya merupakan fungsi rasional dengan penyebut tak
nol, sebagaimana diperlukan.

<!-- upstream_entity: K-Spektrum/Ringhomomorphismus induziert Morphismus/Auf D(F)/Bemerkung -->

### Catatan: tarik-balik pada himpunan terbuka utama {#br-ak-2025-2026-l16-rem-02}

Dalam situasi Teorema 16.6, homomorfisme gelanggang yang terkait dengan
$U=D(f)$ adalah pemetaan alami

$$
\Gamma(D(f),\mathcal O)\cong R_f
\longrightarrow
\Gamma(D(\varphi(f)),\mathcal O)=S_{\varphi(f)}.
$$

<!-- upstream_entity: Quasiaffine Varietät/Globale algebraische Funktion/Ist Morphismus nach affiner Geraden/Fakt -->

### Lema: fungsi aljabar global adalah morfisme ke garis afin {#br-ak-2025-2026-l16-lem-01}

Misalkan $U$ varietas kuasiafin di atas lapangan tertutup secara aljabar
$K$, dan misalkan

$$
f\in\Gamma(U,\mathcal O)
$$

suatu fungsi aljabar. Maka $f$ mendefinisikan morfisme

$$
f:U\longrightarrow\mathbb A_K^1\cong K.
$$

#### Bukti {#br-ak-2025-2026-l16-lem-01-proof}

Menurut Soal 14.4, pemetaan tersebut kontinu. Misalkan
$U\subseteq K\!-\!\operatorname{Spek}(R)$, ambil himpunan terbuka

$$
V=D(s)\subseteq\mathbb A_K^1,
\qquad
W=f^{-1}(V)\subseteq U,
$$

dan suatu fungsi aljabar pada $V$,

$$
q=\frac r{s^n}\in\Gamma(V,\mathcal O)=K[T]_s.
$$

Kita perlu menunjukkan bahwa $q\circ f$ aljabar pada $W$. Ambil $P\in W$
dan penyajian lokal

$$
f=G/H
$$

pada suatu lingkungan $D(H)\ni P$. Maka

$$
(q\circ f)(P)
=q(f(P))
=\frac r{s^n}\!\left(\frac GH(P)\right)
=\frac{r(G(P)/H(P))}{(s(G(P)/H(P)))^n}.
$$

Penyebutnya tidak nol karena $f(P)\in D(s)$; jadi ini merupakan penyajian
rasional yang diperlukan.

<!-- upstream_entity: Quasiaffine Varietät/Morphismus nach affiner Geraden/Fakt -->

### Teorema: morfisme ke garis afin adalah seksi global {#br-ak-2025-2026-l16-thm-03}

Misalkan $U\subseteq K\!-\!\operatorname{Spek}(R)$ varietas kuasiafin,
dengan $R$ aljabar-$K$ komutatif bertipe hingga di atas lapangan tertutup
secara aljabar $K$. Terdapat bijeksi alami

$$
\begin{aligned}
\operatorname{Mor}(U,\mathbb A_K^1)&\longrightarrow\Gamma(U,\mathcal O),\\
\psi&\longmapsto\widetilde\psi(T),
\end{aligned}
$$

dengan $T$ variabel dalam

$$
K[T]=\Gamma(\mathbb A_K^1,\mathcal O).
$$

Khususnya, morfisme dari $U$ ke garis afin ditentukan secara tunggal oleh
homomorfisme gelanggang global

$$
\widetilde\psi:K[T]\longrightarrow\Gamma(U,\mathcal O).
$$

#### Bukti {#br-ak-2025-2026-l16-thm-03-proof}

Pemetaan di atas terdefinisi baik dan surjektif. Jika diberikan fungsi
aljabar global $f\in\Gamma(U,\mathcal O)$, mula-mula kita memperoleh
pemetaan $f:U\to K$. Variabel $T$, yang bersesuaian dengan pemetaan identitas
pada $K=\mathbb A_K^1$, ditarik balik sepanjang $f$ menjadi unsur $f$ itu
sendiri. Menurut Lema 16.8, $f$ merupakan morfisme.

Injektivitas mengikuti karena baik morfisme maupun fungsi aljabar ditentukan
secara tunggal oleh pemetaan kontinu yang mendasarinya.

<!-- upstream_entity: Quasiaffine Varietät/Morphismus nach affiner Varietät/Fakt -->

### Teorema: morfisme ke varietas afin sebagai homomorfisme aljabar {#br-ak-2025-2026-l16-thm-04}

Misalkan $U\subseteq K\!-\!\operatorname{Spek}(R)$ varietas kuasiafin,
dengan $R$ aljabar-$K$ komutatif bertipe hingga di atas lapangan tertutup
secara aljabar $K$. Misalkan $S$ aljabar-$K$ komutatif bertipe hingga lainnya.
Terdapat bijeksi alami

$$
\begin{aligned}
\operatorname{Mor}\bigl(U,K\!-\!\operatorname{Spek}(S)\bigr)
&\longrightarrow
\operatorname{Hom}^{\mathrm{alg}}_K\bigl(S,\Gamma(U,\mathcal O)\bigr),\\
\psi&\longmapsto\widetilde\psi.
\end{aligned}
$$

#### Bukti {#br-ak-2025-2026-l16-thm-04-proof}

Pemetaan ini terdefinisi baik. Teorema 16.9 membuktikan pernyataan untuk
$S=K[T]$. Karena morfisme ke ruang afin $\mathbb A_K^n$ ditentukan oleh
komponennya dan homomorfisme aljabar-$K$ dari $K[T_1,\ldots,T_n]$ ditentukan
oleh substitusi bagi $T_i$, pernyataan itu juga berlaku bagi setiap
gelanggang polinomial $K[T_1,\ldots,T_n]$.

Sekarang tuliskan

$$
S=K[T_1,\ldots,T_n]/\mathfrak a,
\qquad
K\!-\!\operatorname{Spek}(S)\cong V(\mathfrak a)=V
\subseteq\mathbb A_K^n.
$$

Komposisi suatu morfisme $U\to K\!-\!\operatorname{Spek}(S)$ dengan
inklusi tertutup ke ruang afin juga merupakan morfisme. Karena itu terdapat
diagram komutatif

$$
\begin{matrix}
\operatorname{Mor}\bigl(U,K\!-\!\operatorname{Spek}(S)\bigr)
&\longrightarrow&
\operatorname{Hom}^{\mathrm{alg}}_K\bigl(S,\Gamma(U,\mathcal O)\bigr)\\
\downarrow&&\downarrow\\
\operatorname{Mor}(U,\mathbb A_K^n)
&\longrightarrow&
\operatorname{Hom}^{\mathrm{alg}}_K
\bigl(K[T_1,\ldots,T_n],\Gamma(U,\mathcal O)\bigr).
\end{matrix}
$$

Pemetaan bawah telah diketahui bijektif dan kedua pemetaan vertikal
injektif. Kita hanya perlu memeriksa bahwa pemetaan bawah membawa kedua
subhimpunan atas satu sama lain.

Suatu morfisme $U\to\mathbb A_K^n$ yang, sebagai pemetaan, memfaktor melalui
$V$ juga merupakan morfisme ke $V$. Sifat morfisme cukup diperiksa pada
himpunan terbuka utama $D(H)$ dengan $H\in S$. Jika
$\widetilde H\in K[T_1,\ldots,T_n]$ mewakili $H$, pemetaan

$$
K[T_1,\ldots,T_n]_{\widetilde H}\longrightarrow S_H
$$

surjektif. Karena itu setiap unsur $S_H$ ditarik balik menjadi fungsi
aljabar. Pada sisi kanan diagram, suatu homomorfisme aljabar berada dalam
subhimpunan atas tepat ketika $\mathfrak a$ berada dalam kernelnya.
Pernyataan sekarang mengikuti dari Soal 16.8.

![Kerucut ganda yang dipotong oleh sebuah garis miring, dengan sumbu koordinat x, y, dan z](authority/assets/Cone_intersects_line.png)

*Tidak setiap fungsi yang terdefinisi di luar garis pada kerucut dapat
diperluas ke ruang afin tanpa garis tersebut. Pmidden, domain publik.
Rincian sumber berada pada kredit media Unit 16.*

<!-- upstream_entity: K-Spektrum/Abgeschlossene Einbettung/Nicht überall ringsurjektiv/Kegel/Beispiel -->

### Contoh: restriksi yang tidak surjektif {#br-ak-2025-2026-l16-exa-01}

Tinjau kerucut standar sebagai subhimpunan tertutup

$$
V=V(X^2+Y^2-Z^2)\subseteq\mathbb A_K^3.
$$

Misalkan

$$
U=D(X,Z-Y)\subseteq\mathbb A_K^3.
$$

Irisan $U\cap V=D(X,Z-Y)$, kini dipandang di dalam $V$, merupakan himpunan
terbuka di $V$. Homomorfisme gelanggang yang terkait

$$
\Gamma(U,\mathcal O)\longrightarrow\Gamma(U\cap V,\mathcal O)
$$

tidak surjektif. Di ruas kiri hanya terdapat gelanggang polinomial dalam tiga
variabel; bandingkan Soal 14.24. Sebaliknya, dari

$$
X^2=Z^2-Y^2=(Z-Y)(Z+Y)
$$

diperoleh fungsi aljabar pada $U\cap V$

$$
\frac{X}{Z-Y}=\frac{Z+Y}{X}.
$$

Fungsi ini tidak berada dalam citra pemetaan tersebut karena tidak
memperluas menjadi fungsi pada seluruh kerucut.

![Garis-garis serat vertikal di atas daerah berbentuk oval M, dengan suatu daerah terbuka putus-putus U di dalam M](authority/assets/FiberBundle_2.png)

*Serat-serat suatu pemetaan: $M$ adalah kodomain, domain merupakan gabungan
semua serat, dan pemetaan bergerak dari atas ke bawah. １３２人目',
[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). Rincian
sumber berada pada kredit media Unit 16.*

<!-- upstream_entity: K-Spektrum/Morphismus/Faser/Definition -->

### Definisi: serat {#br-ak-2025-2026-l16-def-03}

Misalkan

$$
\psi:Y\longrightarrow X
$$

suatu morfisme antara varietas afin. Untuk suatu titik $P\in X$, pra-citra

$$
\psi^{-1}(P)\subseteq Y
$$

disebut *serat* di atas $P$. Sebagai subhimpunan tertutup dari $Y$, serat
tersebut juga merupakan varietas afin.

---

**Provenans edisi.** Terjemahan dan produksi pembaca: OpenAI Codex
gpt-5.6-sol, Ultra. Sumber, pengarang, dan lisensi komponen dipertahankan
seperti dinyatakan dalam metadata dan berkas hak edisi.
