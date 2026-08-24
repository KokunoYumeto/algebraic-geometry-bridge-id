---
title: "Kuliah 13 - Himpunan Terbuka D(f), Keterhubungan, dan Unsur Idempoten"
stable_id: br-ak-2025-2026-l13
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 13"
upstream_pageid: 165902
upstream_revid: 1112285
upstream_timestamp: "2026-08-21T08:10:43Z"
upstream_mediawiki_sha1: 21738279d828654cee2399253d3c1763db6476a6
source_url: "https://de.wikiversity.org/w/index.php?oldid=1112285"
authority_manifest: authority/wikiversity/unit-13/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: dc86b4d124c7e775fb635a1f9672a8b8faadc4ff2259b0779f7bac6302d18848
lecture_xml_sha256: 400ee9f6816ba759171c717de302bced04a0445ce67afd2e0519f68c67f4559d
lecture_expanded_tex_sha256: f974398ce33ffc1b49b68dd15fdd2db5f701dcf8ecef893285e4d18d432a4e90
license: "CC BY-SA 4.0 for translated course text; media retain component rights in authority/RIGHTS-unit-13.csv"
translation_status: complete
---

# Kuliah 13: Himpunan Terbuka $D(f)$, Keterhubungan, dan Unsur Idempoten {#br-ak-2025-2026-l13}

## Himpunan terbuka $D(f)$ {#br-ak-2025-2026-l13-s01}

Kita akan menunjukkan bahwa subhimpunan terbuka Zariski

$$
D(f)\subseteq K\!-\!\operatorname{Spek}(R)
$$

sendiri homeomorfik dengan spektrum-$K$ suatu aljabar-$K$ bertipe hingga.
Untuk itu kita memerlukan konsep sistem multiplikatif dan pelokalan.

<!-- upstream_entity: Kommutative Ringtheorie/Multiplikatives System/Definition -->

### Definisi: sistem multiplikatif {#br-ak-2025-2026-l13-def-01}

Misalkan $R$ suatu gelanggang komutatif. Suatu subhimpunan
$S\subseteq R$ disebut *sistem multiplikatif* jika memenuhi kedua sifat
berikut:

1. $1\in S$;
2. jika $f,g\in S$, maka $fg\in S$.

<!-- upstream_entity: Kommutative Ringtheorie/Multiplikative Systeme/Potenzen eines Elementes/Beispiel -->

### Contoh: pangkat suatu unsur {#br-ak-2025-2026-l13-exm-01}

Misalkan $R$ suatu gelanggang komutatif dan $f\in R$. Pangkat-pangkat

$$
\{f^n\mid n\in\mathbb N\}
$$

membentuk suatu sistem multiplikatif.

<!-- upstream_entity: Kommutative Ringtheorie/Nenneraufnahme für multiplikative Systeme in Integritätsbereiche/In Quotientenkörper/Definition -->

### Definisi: pelokalan di dalam lapangan pecahan {#br-ak-2025-2026-l13-def-02}

Misalkan $R$ suatu daerah integral dan $S\subseteq R$ suatu sistem
multiplikatif dengan $0\notin S$. Subgelanggang

$$
R_S:=\left\{\frac fg\mathrel{\Big|} f\in R,\ g\in S\right\}
\subseteq Q(R)
$$

disebut *pelokalan* $R$ terhadap $S$.

Untuk pelokalan pada satu unsur $f$, kita cukup menulis $R_f$, bukan
$R_{\{f^n\mid n\in\mathbb N\}}$. Untuk definisi pelokalan pada gelanggang
komutatif sembarang, lihat Soal 13.1.

<!-- upstream_entity: Affine Varietäten/K-Spektrum/D(f) als K-Spek von R_f/Fakt -->

### Teorema: $D(f)$ sebagai spektrum-$K$ dari $R_f$ {#br-ak-2025-2026-l13-thm-01}

Misalkan $K$ suatu lapangan, $R$ suatu aljabar-$K$ bertipe hingga, dan
$f\in R$. Himpunan terbuka Zariski

$$
D(f)\subseteq K\!-\!\operatorname{Spek}(R)
$$

secara alami homeomorfik dengan
$K\!-\!\operatorname{Spek}(R_f)$.

#### Bukti {#br-ak-2025-2026-l13-thm-01-proof}

Tinjau homomorfisme aljabar-$K$ kanonik

$$
\varphi:R\longrightarrow R_f
$$

beserta pemetaan spektrum

$$
\begin{aligned}
\varphi^*:K\!-\!\operatorname{Spek}(R_f)&\longrightarrow
K\!-\!\operatorname{Spek}(R),\\
P&\longmapsto P\circ\varphi.
\end{aligned}
$$

Menurut Teorema 12.7 pemetaan ini kontinu. Karena $f$ menjadi satuan di
$R_f$, untuk setiap $P$ berlaku

$$
f(P\circ\varphi)=P(\varphi(f))\ne0.
$$

Jadi citra $\varphi^*$ terletak di $D(f)$.

Sebaliknya, ambil $Q\in D(f)$. Jadi $Q:R\to K$ merupakan homomorfisme
aljabar-$K$ dengan $Q(f)\ne0$. Unsur $Q(f)$ adalah satuan di $K$. Menurut
sifat universal pelokalan (lihat Soal 13.6), $Q$ mempunyai perluasan
$R_f\to K$. Perluasan ini merupakan praimaj yang dicari, sehingga
$\varphi^*$ surjektif sebagai pemetaan ke $D(f)$.

Untuk membuktikan injektivitas, misalkan $P_1,P_2:R_f\to K$ adalah dua
homomorfisme aljabar-$K$ yang komposisinya dengan $R\to R_f$ sama. Untuk
$r\in R$ dan $s\in\mathbb N$ berlaku

$$
P_1\!\left(\frac r{f^s}\right)
=P_1(rf^{-s})
=P_1(r)P_1(f^s)^{-1},
$$

dan rumus yang sama berlaku untuk $P_2$. Karena nilai keduanya pada $R$ sama,
diperoleh $P_1=P_2$.

Terakhir, himpunan terbuka Zariski pada
$K\!-\!\operatorname{Spek}(R_f)$ ditutupi oleh himpunan-himpunan $D(g)$
dengan $g\in R_f$. Karena $f$ satuan di $R_f$, kita dapat mengambil
$g\in R$. Himpunan $D(g)$ itu sama dengan

$$
(\varphi^*)^{-1}(D(gf)),
$$

di mana $D(gf)$ di ruas kanan merupakan himpunan terbuka di
$K\!-\!\operatorname{Spek}(R)$. Maka bijeksi di atas adalah homeomorfisme.

<!-- upstream_entity: Affine Varietäten/K-Spektrum/D(f) als K-Spek von R_f/Bemerkung -->

### Catatan: realisasi tertutup dari $D(f)$ {#br-ak-2025-2026-l13-rem-01}

Teorema 13.4 khususnya menyatakan bahwa himpunan terbuka

$$
D(f)\subseteq K\!-\!\operatorname{Spek}(R)
$$

sendiri merupakan spektrum-$K$ suatu aljabar-$K$ bertipe hingga, yakni
$R_f$, yang dibangkitkan di atas $R$ oleh $1/f$. Karena

$$
R_f\cong R[T]/(Tf-1)
$$

(lihat Soal 13.4), himpunan itu dapat direalisasikan sebagai himpunan tertutup
dalam suatu ruang afin. Jika

$$
R=K[X_1,\ldots,X_n]/\mathfrak a,
$$

maka homomorfisme gelanggang surjektif

$$
K[X_1,\ldots,X_n,T]
\longrightarrow
\bigl(K[X_1,\ldots,X_n]/\mathfrak a\bigr)[T]
\longrightarrow
\frac{\bigl(K[X_1,\ldots,X_n]/\mathfrak a\bigr)[T]}{(Tf-1)}
\cong R_f
$$

memberikan pembenaman tertutup $D(f)$ ke $\mathbb A_K^{n+1}$ menurut
Proposisi 12.8(3). Jika $\psi$ adalah inklusi komposit

$$
D(f)\subseteq K\!-\!\operatorname{Spek}(R)\subseteq\mathbb A_K^n,
$$

pembenaman tertutup itu juga dapat dipandang sebagai

$$
\psi\times\frac1f:
D(f)\longrightarrow\mathbb A_K^n\times\mathbb A_K^1.
$$

Di sini produk varietas kembali muncul.

<!-- upstream_entity: Affine Varietäten/K-Spektrum/Punktierte affine Gerade als Hyperbel/Beispiel -->

### Contoh: garis afin berlubang sebagai hiperbola {#br-ak-2025-2026-l13-exm-02}

Melanjutkan Catatan 13.5, tinjau himpunan terbuka

$$
D(X)=\{P\in\mathbb A_K^1\mid P\ne0\}\subset\mathbb A_K^1.
$$

Himpunan ini disebut *garis afin berlubang*. Di atasnya $X$ dapat dibalik,
sehingga fungsi rasional $1/X$ terdefinisi. Bersama dengan inklusi terbuka
$D(X)\subseteq\mathbb A_K^1$, fungsi ini memberikan inklusi tertutup

$$
\begin{aligned}
D(X)&\longrightarrow V(XY-1)\subseteq\mathbb A_K^2,\\
x&\longmapsto\left(x,\frac1x\right).
\end{aligned}
$$

Citranya ialah sebuah hiperbola yang tertutup di bidang afin. Jadi garis afin
berlubang dan hiperbola itu homeomorfik; gelanggang yang bersesuaian,

$$
K[X]_X=K[X,X^{-1}]
\qquad\text{dan}\qquad
K[X,Y]/(XY-1),
$$

juga isomorfik.

![Dua cabang hiperbola y sama dengan satu per x pada bidang koordinat](authority/assets/Hyperbola_one_over_x.svg)

*Grafik hiperbola $y=1/x$; Ktims, [CC BY-SA
3.0](http://creativecommons.org/licenses/by-sa/3.0/).*

## Keterhubungan dan unsur idempoten {#br-ak-2025-2026-l13-s02}

Kita ingin memahami bagaimana keterhubungan suatu himpunan aljabar afin
tercermin pada gelanggang koordinatnya dan bagaimana komponen-komponen
terhubung dapat dicirikan. Contoh berikut menunjukkan bahwa teori yang
memuaskan tidak dapat diharapkan di atas lapangan yang tidak tertutup secara
aljabar.

<!-- upstream_entity: Ebene algebraische Kurven/Reell/X^2+Y^2-2 und X^2+2Y^2-1/Zusammenhangseigenschaft/Beispiel -->

### Contoh: keterhubungan dapat berubah setelah perluasan lapangan {#br-ak-2025-2026-l13-exm-03}

Seperti pada Contoh 11.5, tinjau dua kurva aljabar

$$
V_1=V(X^2+Y^2-2)
\quad\text{dan}\quad
V_2=V(X^2+2Y^2-1)\subseteq\mathbb A_K^2.
$$

Irisannya dideskripsikan oleh ideal

$$
(X^2+Y^2-2,\,X^2+2Y^2-1)
=(Y^2+1,\,X^2-3).
$$

Untuk $K=\mathbb R$ kita mempunyai $V_1\cap V_2=\varnothing$. Karena itu

$$
V=V_1\cup V_2
$$

tidak terhubung; $V_1$ dan $V_2$ sekaligus merupakan komponen tak tereduksi
dan komponen terhubungnya. Gelanggang koordinat $V$ ialah

$$
\mathbb R[X,Y]/\bigl((X^2+Y^2-2)(X^2+2Y^2-1)\bigr).
$$

Kita mungkin menduga bahwa fungsi pada $V$ yang konstan $1$ di $V_1$ dan
konstan $0$ di $V_2$ muncul di dalam gelanggang koordinat. Namun tidak
demikian. Penyebabnya ialah bahwa setelah memperluas skalar ke bilangan
kompleks, $V_{\mathbb C}$ terhubung. Oleh karena itu gelanggang koordinat
kompleks hanya mempunyai unsur idempoten trivial, dan hal ini turun ke
gelanggang koordinat real.

<!-- upstream_entity: Kommutative Ringtheorie/Idempotentes Element/Definition -->

### Definisi: unsur idempoten {#br-ak-2025-2026-l13-def-03}

Suatu unsur $e$ dari gelanggang komutatif disebut *idempoten* jika

$$
e^2=e.
$$

Unsur $0$ dan $1$ adalah idempoten.

<!-- upstream_entity: Kommutative Ringtheorie/Produktring/Definition -->

### Definisi: gelanggang produk {#br-ak-2025-2026-l13-def-04}

Misalkan $R_1,\ldots,R_n$ gelanggang-gelanggang komutatif. Produk

$$
R_1\times\cdots\times R_n,
$$

dengan penjumlahan dan perkalian per komponen, disebut *gelanggang produk*
dari $R_i$, $i=1,\ldots,n$.

Dalam gelanggang produk terdapat banyak unsur idempoten, yaitu unsur-unsur
yang setiap komponennya bernilai $0$ atau $1$.

<!-- upstream_entity: Kommutative Ringtheorie/Zusammenhängender Ring/Definition -->

### Definisi: gelanggang terhubung {#br-ak-2025-2026-l13-def-05}

Suatu gelanggang komutatif $R$ disebut *terhubung* jika tepat mempunyai dua
unsur idempoten, yakni $0\ne1$.

![Satu bentuk merah yang utuh dan dua bentuk hijau yang terpisah](authority/assets/Connected_and_disconnected_spaces2.svg)

*Ruang topologis terhubung (merah) dan ruang tak terhubung (hijau); Dbc334,
domain publik.*

<!-- upstream_entity: Topologische Grundbegriffe/Zusammenhängender Raum/Definition -->

### Definisi: ruang topologis terhubung {#br-ak-2025-2026-l13-def-06}

Suatu ruang topologis $X$ disebut *terhubung* jika di dalam $X$ tepat terdapat
dua subhimpunan - yaitu $\varnothing$ dan seluruh ruang
$X\ne\varnothing$ - yang sekaligus terbuka dan tertutup.

Himpunan kosong dan seluruh ruang selalu sekaligus terbuka dan tertutup.
Himpunan semacam itu juga disebut *clopen*. Ruang topologis kosong tidak
dianggap terhubung karena hanya mempunyai satu subhimpunan yang sekaligus
terbuka dan tertutup.

<!-- upstream_entity: Kommutative Ringtheorie/K-Spektrum/Produktring/Fakt -->

### Lema: spektrum-$K$ dari gelanggang produk {#br-ak-2025-2026-l13-lem-01}

Misalkan $K$ suatu lapangan dan $R_1,R_2$ aljabar-$K$ bertipe hingga. Untuk
$R=R_1\times R_2$ terdapat homeomorfisme alami

$$
K\!-\!\operatorname{Spek}(R_1\times R_2)
\cong
K\!-\!\operatorname{Spek}(R_1)
\mathbin{\uplus}
K\!-\!\operatorname{Spek}(R_2).
$$

Pembenaman dari ruas kanan ke ruas kiri diinduksi oleh proyeksi
$R\to R_i$, $i=1,2$.

#### Bukti {#br-ak-2025-2026-l13-lem-01-proof}

Proyeksi $R_1\times R_2\to R_1$ merupakan homomorfisme aljabar-$K$ dan
menurut Proposisi 12.8(3) menginduksi pemetaan kontinu - bahkan pembenaman
tertutup -

$$
K\!-\!\operatorname{Spek}(R_1)
\longrightarrow K\!-\!\operatorname{Spek}(R_1\times R_2).
$$

Hal yang sama berlaku bagi $R_2$. Kedua pemetaan bersama-sama memberikan
pemetaan kontinu dari gabungan disjung ruas kanan ke ruas kiri.

Ambil $P\in K\!-\!\operatorname{Spek}(R_1\times R_2)$, yakni homomorfisme
aljabar-$K$ $P:R_1\times R_2\to K$. Misalkan

$$
e_1=(1,0),\qquad e_2=(0,1).
$$

Karena $e_1+e_2=1$ dan $e_1e_2=0$, tepat satu dari kedua unsur itu dipetakan
oleh $P$ ke $0$ dan yang lain ke $1$. Dengan demikian $P$ memfaktor melalui
salah satu proyeksi. Ini membuktikan surjektivitas.

Untuk injektivitas, ambil dua titik berbeda dalam gabungan disjung. Jika
keduanya terletak pada komponen yang sama, citranya tetap berbeda karena
pemetaan pada komponen itu merupakan pembenaman tertutup. Jika keduanya
terletak pada komponen berbeda, nilai mereka pada $e_1$ masing-masing $0$ dan
$1$, sehingga mereka juga berbeda sebagai titik spektrum produk.

Pemetaan bijektif ini adalah homeomorfisme karena kedua pembenaman tertutup
tersebut bergabung menjadi pemetaan tertutup.

<!-- upstream_entity: Kommutative Ringtheorie/K-Spektrum/Algebraisch abgeschlossen/Idempotente Elemente und randlose Mengen/Fakt -->

### Teorema: unsur idempoten dan subhimpunan clopen {#br-ak-2025-2026-l13-thm-02}

Misalkan $K$ lapangan tertutup secara aljabar dan $R$ aljabar-$K$ komutatif
bertipe hingga yang tereduksi. Pemetaan

$$
e\longmapsto D(e)
$$

memberikan bijeksi antara unsur-unsur idempoten di $R$ dan subhimpunan dari
$K\!-\!\operatorname{Spek}(R)$ yang sekaligus terbuka dan tertutup.

#### Bukti {#br-ak-2025-2026-l13-thm-02-proof}

Pertama,

$$
D(e)=V(1-e)
$$

sekaligus terbuka dan tertutup. Hal ini mengikuti dari

$$
D(e)\cup D(1-e)=D(1)=K\!-\!\operatorname{Spek}(R)
$$

dan

$$
D(e)\cap D(1-e)=D(e(1-e))=D(e-e^2)=D(0)=\varnothing.
$$

Jadi pemetaan tersebut terdefinisi dengan baik.

Misalkan $e_1,e_2$ idempoten dan

$$
U=D(e_1)=D(e_2).
$$

Unsur idempoten di suatu lapangan hanya dapat bernilai $0$ atau $1$. Karena
itu $e_1$ dan $e_2$ sama-sama bernilai $1$ pada $U$ dan $0$ di luar $U$.
Keduanya mempunyai nilai yang sama di setiap titik. Teorema identitas untuk
aljabar tereduksi di atas lapangan tertutup secara aljabar memberikan
$e_1=e_2$. Ini membuktikan injektivitas.

Sekarang misalkan $U=D(\mathfrak a)$ sekaligus terbuka dan tertutup. Ada ideal
lain $\mathfrak b$ dengan

$$
D(\mathfrak a)\cup D(\mathfrak b)
=K\!-\!\operatorname{Spek}(R),
\qquad
D(\mathfrak a)\cap D(\mathfrak b)=\varnothing.
$$

Menurut Korolari 11.12, $\mathfrak a$ dan $\mathfrak b$ bersama-sama
membangkitkan ideal satuan. Jadi terdapat $a\in\mathfrak a$ dan
$b\in\mathfrak b$ dengan $a+b=1$. Karena

$$
D(a)\cap D(b)=D(ab)=\varnothing,
$$

Soal 12.11 menyatakan bahwa $ab$ nilpoten. Gelanggang $R$ tereduksi, sehingga
$ab=0$. Akibatnya

$$
a=a\cdot1=a(a+b)=a^2+ab=a^2,
$$

jadi $a$ idempoten. Karena $D(a)\subseteq D(\mathfrak a)$,
$D(b)\subseteq D(\mathfrak b)$, dan
$D(a)\cup D(b)=K\!-\!\operatorname{Spek}(R)$, diperoleh

$$
U=D(\mathfrak a)=D(a).
$$

Ini membuktikan surjektivitas.

Sebagai akibat, di atas lapangan yang tertutup secara aljabar, suatu
aljabar-$K$ tereduksi bertipe hingga $R$ terhubung jika dan hanya jika
$K\!-\!\operatorname{Spek}(R)$ terhubung.

Pernyataan terakhir juga berlaku tanpa asumsi tereduksi karena unsur-unsur
idempoten berkorespondensi secara bijektif setelah mengambil reduksi; lihat
Soal 13.27 dan 13.30.
