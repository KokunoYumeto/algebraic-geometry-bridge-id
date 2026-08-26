---
title: "Kuliah 26 - Multiplisitas Perpotongan"
stable_id: br-ak-2012-l26
language: id-ID
source_author: "Holger Brenner"
frozen_revision_contributor: "Arbota"
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2012)/Vorlesung 26"
upstream_pageid: 50732
upstream_revid: 793526
upstream_timestamp: "2022-08-25T06:09:17Z"
upstream_mediawiki_sha1: 57845c7bb535d0cccde6d289409a8dbbe684f2d8
source_url: "https://de.wikiversity.org/w/index.php?oldid=793526"
authority_manifest: authority/wikiversity/unit-26/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 981fa3c86534514215c722b6d4f6d711c040a7829465f20ae18940373f94763c
lecture_xml: authority/wikiversity/unit-26/lecture-26.xml
lecture_xml_sha256: cc6a483e01e22db4262c3e400325ec22c4cf8750e3a1a8c11043398368f40ff9
lecture_expanded_tex: authority/wikiversity/unit-26/lecture-26-expanded.tex
lecture_expanded_tex_sha256: 567968794b07d9e045813a62921dc8b527e99f500807bff843bd7cb498ea8ee7
lecture_dependency_identity_rows_sha256: f1a064c0531f9079633a57009c565f20a0520a0ef10cb2336ad3b52aa2d331b8
license: "Current semantic course text and this translation: CC BY-SA 4.0. Intersect3.png: CC BY-SA 3.0. The official 2012 PDF file-description surface also records the legacy CC BY-SA 2.0 Germany route. No blanket relicensing claim is made."
source_component_license_route: "Semantic-site rights notice: CC BY-SA 4.0; Intersect3.png: CC BY-SA 3.0; official-PDF legacy file-description notice: CC BY-SA 2.0 Germany; official-PDF current print-version notice: CC BY-SA 4.0; no blanket relicensing claim."
license_evidence: "authority/UNIT_26_AUTHORITY_FREEZE.md; authority/RIGHTS-unit-26.csv; authority/ASSET_CLOSURE-unit-26.json"
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_semantic_entities: 21
source_corrections: 6
correction_ids: "AGC-CORR-0097; AGC-CORR-0098; AGC-CORR-0099; AGC-CORR-0100; AGC-CORR-0104; AGC-CORR-0106"
reader_media_positions: 1
---

# Kuliah 26: Multiplisitas Perpotongan {#br-ak-2012-l26}

## Multiplisitas perpotongan {#br-ak-2012-l26-s01}

<!-- upstream_entity: Ebene algebraische Kurven/Schnittmultiplizität/Lokale und semilokale Beschreibung/Einführung/Textabschnitt -->

Misalkan diberikan dua kurva aljabar bidang

$$
C,D\subseteq\mathbb A_K^2
$$

yang tidak mempunyai komponen bersama. Menurut Teorema 4.8, irisan
$C\cap D$ hanya terdiri atas berhingga banyak titik. Kita hendak mengukur
perilaku perpotongan kedua kurva itu secara kuantitatif di suatu titik

$$
P\in C\cap D.
$$

Untuk itu, sebaiknya kita meninjau keadaan yang sedikit lebih umum. Kita
tulis

$$
C=V(F)
\qquad\text{dan}\qquad
D=V(G),
$$

lalu memperhitungkan bahwa faktor-faktor prima dapat muncul berulang kali
dalam $F$ maupun $G$. Dengan kata lain, mulai sekarang kita membedakan
$V(F)$ dari $V(F^n)$, walaupun keduanya merupakan objek geometris yang sama.

<!-- upstream_entity: Ebene algebraische Kurven/Schnittmultiplizität/Restdimension ist endlich/Fakt -->

### Lema 26.1: dimensi hasil bagi berhingga {#br-ak-2012-l26-lem-01}

Misalkan $K$ suatu lapangan dan

$$
F,G\in K[X,Y]
$$

dua polinom tanpa pembagi prima bersama. Misalkan

$$
P\in V(F,G)
$$

dan

$$
R=K[X,Y]_{\mathfrak m_P}
$$

pelokalan yang bersesuaian. Maka gelanggang hasil bagi

$$
R/(F,G)
$$

berdimensi hingga sebagai ruang vektor atas $K$.

<!-- upstream_entity: Ebene algebraische Kurven/Schnittmultiplizität/Restdimension ist endlich/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l26-lem-01-proof}

Misalkan $\mathfrak m$ ideal maksimal di $R$. Karena $F$ dan $G$ tidak
mempunyai pembagi bersama, tidak ada ideal prima lain di antara $(F,G)$ dan
$\mathfrak m$ di dalam $R$. Oleh karena itu, setiap unsur bukan-unit dalam
$R/(F,G)$ bersifat nilpoten. Jadi, untuk suatu $s$, berlaku

$$
\mathfrak m^s\subseteq(F,G)\subseteq\mathfrak m.
$$

Akibatnya terdapat surjeksi

$$
R/\mathfrak m^s\longrightarrow R/(F,G).
$$

Menurut Lema 23.3 dalam penomoran sumber, gelanggang di sebelah kiri
berdimensi hingga atas $K$. Karena itu gelanggang di sebelah kanan juga
berdimensi hingga atas $K$. $\square$

Berdasarkan lema ini, definisi berikut masuk akal.

<!-- upstream_entity: Ebene algebraische Kurven/Schnittmultiplizität/Restdimension/Definition -->

### Definisi 26.2: multiplisitas perpotongan {#br-ak-2012-l26-def-01}

Misalkan $K$ suatu lapangan dan

$$
F,G\in K[X,Y]
$$

dua polinom takkonstan tanpa komponen bersama, serta misalkan

$$
P\in V(F)\cap V(G)=V(F,G).
$$

Dimensi

$$
\dim_K\left(K[X,Y]_{\mathfrak m_P}/(F,G)\right)
$$

disebut *multiplisitas perpotongan* kurva $V(F)$ dan $V(G)$ di titik $P$.
Besaran ini dinotasikan dengan

$$
\operatorname{mult}_P(F,G)
\qquad\text{atau}\qquad
\operatorname{mult}_P\bigl(V(F),V(G)\bigr).
$$

<!-- upstream_entity: Ebene algebraische Kurven/Schnittmultiplizität/Restdimension/Schnitt mit Gerade/Beispiel -->

### Contoh 26.3: perpotongan sebuah kurva dengan sebuah garis {#br-ak-2012-l26-ex-01}

Misalkan

$$
C=V(F)
$$

dan sebuah garis

$$
L=V(cX+dY)
$$

di bidang afin $\mathbb A_K^2$ diberikan, dengan $L$ bukan komponen $C$.
Misalkan

$$
P=(a,b)\in C\cap L.
$$

Gelanggang hasil bagi

$$
K[X,Y]_{\mathfrak m_P}/(F,cX+dY)
$$

dapat dihitung dengan menyelesaikan suku linear tersebut terhadap salah satu
variabel. Jika $d\ne0$, kita substitusikan

$$
Y=-\frac cdX
$$

ke dalam $F$ dan memperoleh polinom satu variabel

$$
\widetilde F(X)=F\left(X,-\frac cdX\right).
$$

Dengan demikian,

$$
K[X,Y]_{\mathfrak m_P}/(F,cX+dY)
\cong K[X]_{(X-a)}/(\widetilde F).
$$

Jika $d=0$, maka $c\ne0$, sehingga kita menyelesaikan terhadap $X$ dan
memperoleh pernyataan analog dalam variabel $Y$, yang dilokalkan pada
$(Y-b)$. Secara ekuivalen, kita dapat membentuk gelanggang hasil bagi satu
variabel terlebih dahulu, kemudian melokalkannya pada titik yang sesuai.

Andaikan sekarang $K$ tertutup secara aljabar. Dalam cabang $d\ne0$, kita
mempunyai faktorisasi

$$
\widetilde F=(X-\lambda_1)^{\nu_1}\cdots
(X-\lambda_k)^{\nu_k}.
$$

Karena $P$ merupakan titik nol, haruslah $a=\lambda_i$ untuk suatu $i$.
Ketika kita melokalkan pada $(X-a)$, semua faktor linear yang lain menjadi
unit. Faktor yang tersisa menghasilkan gelanggang yang isomorfik dengan

$$
K[X]/(X-\lambda_i)^{\nu_i},
$$

yang berdimensi $\nu_i$ atas $K$.

> **Catatan edisi - cabang eliminasi dan pelokalan.** Sumber langsung
> mengganti $Y$ dengan $-(c/d)X$ tanpa menyatakan syarat $d\ne0$, lalu menulis
> $K[X]_P$. Edisi memisahkan cabang $d\ne0$ dan $c\ne0$ serta menuliskan
> ideal pelokalan satu variabel yang tepat, yaitu $(X-a)$ atau $(Y-b)$.

<!-- upstream_entity: Ebene algebraische Kurven/Schnittmultiplizität/Schnitt mit Gerade/Abschätzung zur Multiplizität/Fakt -->

### Lema 26.4: perpotongan dengan garis {#br-ak-2012-l26-lem-02}

Misalkan $K$ suatu lapangan tertutup secara aljabar,

$$
F=F_m+\cdots+F_d\in K[X,Y],
\qquad m\leq d,
$$

dekomposisi homogen suatu polinom, dan

$$
L=V(aX+bY)
$$

sebuah garis melalui titik asal $P$ yang bukan komponen $V(F)$. Maka

$$
\operatorname{mult}_P\bigl(L,V(F)\bigr)
\geq m_P(F)=m.
$$

Dengan kata lain, multiplisitas perpotongan sebuah kurva dengan sebuah garis
sekurang-kurangnya sama dengan multiplisitas kurva pada titik potong itu.
Jika $L$ bukan garis singgung kurva tersebut, berlaku kesamaan.

<!-- upstream_entity: Ebene algebraische Kurven/Schnittmultiplizität/Schnitt mit Gerade/Abschätzung zur Multiplizität/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l26-lem-02-proof}

Tetapkan

$$
R=K[X,Y]_{(X,Y)}
\qquad\text{dan}\qquad
H=aX+bY.
$$

Tanpa mengurangi keumuman, andaikan $b\ne0$, sehingga persamaan $H=0$ dapat
ditulis sebagai $Y=cX$ untuk suatu $c\in K$. Jika $b=0$, maka $a\ne0$ dan
argumen yang sama berlaku setelah menukar $X$ dengan $Y$.

Mula-mula andaikan $L$ bukan garis singgung $V(F)$ di $P$, sehingga $L$
bukan komponen $V(F_m)$. Maka

$$
R/(F,H)
\cong
K[X]_{(X)}/\bigl(F_m(X,cX)+\cdots+F_d(X,cX)\bigr).
$$

Karena $F_m(X,cX)\ne0$, polinom di dalam ideal dapat ditulis sebagai
$X^m u$ dengan $u$ suatu unit. Jadi gelanggang hasil bagi itu berdimensi $m$
atas $K$.

Dalam keadaan umum, terdapat indeks terkecil $i$, dengan $m\leq i\leq d$,
sedemikian sehingga

$$
F_i(X,cX)\ne0.
$$

Indeks seperti itu harus ada, sebab jika tidak, $L$ akan menjadi komponen
$V(F)$. Dengan argumen yang sama, dimensi gelanggang hasil bagi sama dengan
$i\geq m$. $\square$

> **Catatan edisi - pilihan koordinat dalam bukti.** Sumber mengandaikan
> $b\ne0$ tanpa menjelaskan kasus yang lain. Edisi menyatakan bahwa pilihan
> itu tanpa mengurangi keumuman, sebab untuk $b=0$ variabel $X$ dan $Y$ dapat
> dipertukarkan.

<!-- upstream_entity: Ebene algebraische Kurven/Schnittmultiplizität/Erste Eigenschaften/Fakt -->

### Lema 26.5: sifat-sifat dasar {#br-ak-2012-l26-lem-03}

Misalkan $K$ suatu lapangan tertutup secara aljabar,

$$
F,G\in K[X,Y]
$$

dua polinom tanpa komponen bersama, dan $P\in\mathbb A_K^2$. Maka berlaku:

1. $\operatorname{mult}_P(F,G)=0$ jika dan hanya jika
   $P\notin V(F,G)$.
2. $\operatorname{mult}_P(F,G)=\operatorname{mult}_P(G,F)$.
3. Multiplisitas perpotongan tidak berubah oleh transformasi afin pada
   variabel.
4. Jika $F=F_1F_2$ dan $F_2(P)\ne0$, maka
   $$
   \operatorname{mult}_P(F,G)=\operatorname{mult}_P(F_1,G).
   $$
5. Untuk setiap $H\in K[X,Y]$,
   $$
   \operatorname{mult}_P(F,G)
   =\operatorname{mult}_P(F,G+HF).
   $$

Pernyataan keempat juga dapat dirumuskan sebagai berikut: multiplisitas
perpotongan hanya bergantung pada komponen-komponen $F$ dan $G$ yang melalui
$P$.

![Sebuah lingkaran dan sebuah kurva yang bersinggungan di sebelah kiri serta berpotongan melintang di sebelah kanan](authority/assets/250px-Intersect3.png)

*Satu perpotongan transversal dan satu perpotongan nontransversal. Gambar
diciptakan oleh Michael Larsen dan diunggah ke Commons oleh Maksim;
[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/); berkas lokal:
`authority/assets/250px-Intersect3.png`.*

<!-- upstream_entity: Ebene algebraische Kurven/Schnittmultiplizität/Transversaler Schnitt/Definition -->

### Definisi 26.6: perpotongan transversal {#br-ak-2012-l26-def-02}

Misalkan

$$
F,G\in K[X,Y]
\qquad\text{dan}\qquad
P\in V(F,G).
$$

Kurva $V(F)$ dan $V(G)$ dikatakan *berpotongan secara transversal* di $P$
apabila $P$ merupakan titik mulus pada kedua kurva dan garis singgung kedua
kurva di $P$ berbeda.

<!-- upstream_entity: Ebene algebraische Kurven/Schnittmultiplizität/Charakterisierung Transversaler Schnitt/Fakt -->

### Lema 26.7: karakterisasi perpotongan transversal {#br-ak-2012-l26-lem-04}

Misalkan $K$ suatu lapangan dan

$$
F,G\in K[X,Y]
$$

dua polinom tanpa komponen bersama. Misalkan

$$
P\in V(F,G)\subseteq\mathbb A_K^2
$$

suatu titik potong. Maka $V(F)$ dan $V(G)$ berpotongan secara transversal di
$P$ jika dan hanya jika

$$
\operatorname{mult}_P\bigl(V(F),V(G)\bigr)=1.
$$

<!-- upstream_entity: Ebene algebraische Kurven/Schnittmultiplizität/Charakterisierung Transversaler Schnitt/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l26-lem-04-proof}

Misalkan

$$
R=K[X,Y]_{\mathfrak m_P}
$$

gelanggang lokal bidang di titik $P$. Mula-mula andaikan perpotongannya
transversal. Kedua kurva mulus di $P$, dan menurut Lema 23.2 dalam penomoran
sumber,

$$
B=R/(F)
$$

merupakan gelanggang valuasi diskret. Karena kedua garis singgung berbeda,
setelah suatu perubahan koordinat kita dapat mengandaikan bahwa garis singgung
$V(F)$ diberikan oleh $V(Y)$ dan garis singgung $V(G)$ diberikan oleh $V(X)$.
Dalam $B$, unsur $X$ merupakan uniformisator lokal. Karena

$$
G=X+H,
\qquad H\in\mathfrak m_P^2,
$$

unsur $G$ juga merupakan uniformisator lokal dalam $B$. Oleh karena itu,

$$
B/(G)=K,
$$

dan multiplisitas perpotongannya sama dengan satu.

Sebaliknya, andaikan

$$
\dim_K R/(F,G)=1.
$$

Karena $P$ adalah titik $K$-rasional, hasil bagi itu adalah medan residu $K$.
Jadi ideal maksimalnya lenyap, atau secara ekuivalen,

$$
(F,G)=\mathfrak m_P
$$

di $R$. Setelah mengambil hasil bagi modulo $\mathfrak m_P^2$, suku-suku
linear $F$ dan $G$ membangun ruang kotangen berdimensi dua
$\mathfrak m_P/\mathfrak m_P^2$. Maka kedua suku linear tersebut taknol dan
bebas linear. Dengan demikian kedua kurva mulus di $P$, dan kernel kedua
bentuk linear itu, yaitu garis singgungnya, berbeda. Jadi perpotongannya
transversal. $\square$

> **Catatan edisi - perbaikan bukti arah balik.** Sumber menyimpulkan
> kemulusan kedua kurva dengan mengutip Lema 26.4. Namun, lema tersebut hanya
> membahas perpotongan sebuah kurva dengan sebuah garis, sehingga tidak
> membenarkan kesimpulan yang dinyatakan untuk dua polinom sembarang. Selain
> itu, Lema 26.4 dinyatakan untuk lapangan tertutup secara aljabar, sedangkan
> Lema 26.7 dinyatakan untuk lapangan sembarang. Edisi mengganti langkah itu
> dengan argumen langsung pada $\mathfrak m_P/\mathfrak m_P^2$, yang berlaku
> untuk titik $K$-rasional sebagaimana dinyatakan.

<!-- upstream_entity: Ebene algebraische Kurven/Schnittmultiplizität/Summenformel für Schnittmultiplizität/Fakt -->

### Teorema 26.8: rumus aditivitas {#br-ak-2012-l26-thm-01}

Misalkan

$$
F,G\in K[X,Y]
$$

dua polinom tanpa pembagi prima bersama, dengan faktorisasi

$$
F=\prod_{i=1}^{m}F_i^{\nu_i}
\qquad\text{dan}\qquad
G=\prod_{j=1}^{n}G_j^{\mu_j}.
$$

Maka, untuk setiap $P\in\mathbb A_K^2$,

$$
\operatorname{mult}_P(F,G)
=\sum_{i,j}\nu_i\mu_j\operatorname{mult}_P(F_i,G_j).
$$

Di luar titik perpotongan, multiplisitas pada kedua ruas dipahami bernilai
nol sebagaimana dalam Lema 26.5.

> **Catatan edisi - pengikatan titik.** Sumber menampilkan $P$ pada rumus
> tanpa memperkenalkan atau menguantifikasikannya. Edisi menyatakan bahwa
> identitas berlaku untuk setiap $P\in\mathbb A_K^2$, dengan konvensi nol di
> luar himpunan perpotongan.

<!-- upstream_entity: Ebene algebraische Kurven/Schnittmultiplizität/Summenformel für Schnittmultiplizität/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l26-thm-01-proof}

Dengan induksi, cukup membuktikan kasus khusus $F=F_1F_2$. Tetapkan

$$
R=K[X,Y]_{\mathfrak m_P}.
$$

Karena

$$
(F_1F_2,G)\subseteq(F_2,G),
$$

terdapat pemetaan surjektif

$$
R/(F_1F_2,G)\longrightarrow R/(F_2,G).
$$

Di sisi lain, perkalian dengan $F_2$ menginduksi homomorfisme modul-$R$

$$
R/(F_1,G)\longrightarrow R/(F_1F_2,G).
$$

Kita klaim bahwa terdapat barisan eksak pendek

$$
0\longrightarrow R/(F_1,G)
\mathop{\longrightarrow}^{\cdot F_2}
R/(F_1F_2,G)
\longrightarrow R/(F_2,G)
\longrightarrow0.
$$

Surjektivitas pemetaan kanan jelas, demikian pula kenyataan bahwa komposisi
dua pemetaan itu nol. Misalkan kelas $z\in R/(F_1F_2,G)$ dipetakan ke nol di
sebelah kanan. Di dalam $R$ kita dapat menulis

$$
z=AF_2+BG.
$$

Jadi $AF_2$ mewakili kelas yang sama di $R/(F_1F_2,G)$, dan kelas itu berasal
dari sebelah kiri.

Sekarang misalkan kelas $w\in R/(F_1,G)$ dipetakan ke nol oleh perkalian
dengan $F_2$. Di dalam $R$ berarti

$$
wF_2=CF_1F_2+DG,
$$

atau

$$
(w-CF_1)F_2=DG.
$$

Karena $F$ dan $G$ tidak mempunyai pembagi prima bersama, demikian pula
$F_2$ dan $G$. Maka $F_2$ membagi $D$, sehingga

$$
w-CF_1=\widetilde D G.
$$

Jadi $w=0$ di $R/(F_1,G)$, dan pemetaan kiri injektif.

Sifat aditivitas dimensi pada barisan eksak pendek sekarang memberikan

$$
\begin{aligned}
\operatorname{mult}_P(F_1F_2,G)
&=\dim_K R/(F_1F_2,G)\\
&=\dim_K R/(F_1,G)+\dim_K R/(F_2,G)\\
&=\operatorname{mult}_P(F_1,G)+\operatorname{mult}_P(F_2,G).
\end{aligned}
$$

Induksi pada semua faktor $F$ dan $G$ membuktikan rumus tersebut. $\square$

<!-- upstream_entity: Noetherscher Nulldimensionaler Ring/Produktdarstellung/Fakt -->

### Teorema 26.9: dekomposisi produk gelanggang Noether berdimensi nol {#br-ak-2012-l26-thm-02}

Misalkan $R$ suatu gelanggang komutatif Noether yang hanya mempunyai berhingga
banyak ideal prima

$$
\mathfrak m_1,\ldots,\mathfrak m_n,
$$

dan semuanya maksimal. Maka terdapat isomorfisme kanonik

$$
R\cong R_{\mathfrak m_1}\times\cdots\times R_{\mathfrak m_n}.
$$

<!-- upstream_entity: Noetherscher Nulldimensionaler Ring/Produktdarstellung/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l26-thm-02-proof}

Ideal-ideal maksimal tersebut sekaligus merupakan ideal-ideal prima minimal.
Karena itu, irisan semua ideal maksimal,

$$
\mathfrak a=\bigcap_i\mathfrak m_i,
$$

hanya terdiri atas unsur-unsur nilpoten. Karena $R$ Noether, terdapat $s$
sedemikian sehingga

$$
\mathfrak a^s=0.
$$

Untuk setiap $i$, tinjau pelokalan

$$
R\longrightarrow R_{\mathfrak m_i}.
$$

Kita klaim bahwa pelokalan ini isomorfik dengan

$$
R/\mathfrak a_i,
\qquad
\mathfrak a_i:=\mathfrak m_i^s.
$$

Karena

$$
\prod_i\mathfrak m_i\subseteq\bigcap_i\mathfrak m_i,
$$

kita memperoleh

$$
\left(\prod_i\mathfrak m_i\right)^s
\subseteq
\left(\bigcap_i\mathfrak m_i\right)^s,
$$

dan dengan demikian

$$
\mathfrak a_1\cdots\mathfrak a_n=0.
$$

Ambil $i=1$. Untuk setiap $j\ne1$, terdapat

$$
g_j\in\mathfrak m_j
\qquad\text{dengan}\qquad
g_j\notin\mathfrak m_1.
$$

Untuk setiap $f\in\mathfrak a_1$ berlaku

$$
fg_2^s\cdots g_n^s=0.
$$

Karena $g_2^s\cdots g_n^s\notin\mathfrak m_1$, unsur tersebut menjadi unit
setelah pelokalan. Jadi $f$ dipetakan ke nol, dan kita memperoleh
homomorfisme gelanggang

$$
R/\mathfrak a_1\longrightarrow R_{\mathfrak m_1}.
$$

Ruas kanan juga merupakan pelokalan dari gelanggang hasil bagi di ruas kiri.
Ideal-ideal maksimal yang berbeda membangun ideal satuan secara berpasangan,
dan sifat ini tetap berlaku bagi pangkat-pangkatnya. Maka $\mathfrak a_1$
hanya termuat dalam $\mathfrak m_1$. Jadi $R/\mathfrak a_1$ sendiri merupakan
gelanggang lokal berdimensi nol, sehingga pemetaan di atas adalah
isomorfisme. Argumen yang sama berlaku untuk setiap $i$.

Pemetaan semula dengan demikian dapat ditulis sebagai

$$
R\longrightarrow\prod_{i=1}^{n}R/\mathfrak a_i.
$$

Karena ideal-ideal $\mathfrak a_i$ membangun ideal satuan secara berpasangan,
Teorema Sisa Cina menyatakan bahwa pemetaan ini merupakan isomorfisme.
$\square$

<!-- upstream_entity: Ebene algebraische Kurve/Schnitt von Kurven ohne gemeinsame Komponente/Beschreibung als Produktring/Fakt -->

### Korolari 26.10: hasil bagi global sebagai produk gelanggang lokal {#br-ak-2012-l26-cor-01}

Misalkan $K$ suatu lapangan tertutup secara aljabar dan

$$
F,G\in K[X,Y]
$$

dua polinom tanpa pembagi prima bersama. Misalkan

$$
P_1,\ldots,P_n\in\mathbb A_K^2
$$

merupakan semua titik dalam $V(F,G)$, dengan ideal maksimal yang bersesuaian
$\mathfrak m_1,\ldots,\mathfrak m_n$ di $K[X,Y]$. Maka terdapat isomorfisme
kanonik

$$
K[X,Y]/(F,G)
\cong
\prod_{i=1}^{n}\left(K[X,Y]_{\mathfrak m_i}/(F,G)\right).
$$

<!-- upstream_entity: Ebene algebraische Kurve/Schnitt von Kurven ohne gemeinsame Komponente/Beschreibung als Produktring/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l26-cor-01-proof}

Karena $F$ dan $G$ tidak mempunyai pembagi prima bersama, ideal $(F,G)$
hanya termuat dalam berhingga banyak ideal prima, dan semuanya maksimal. Oleh
karena itu, gelanggang hasil bagi

$$
K[X,Y]/(F,G)
$$

memenuhi syarat Teorema 26.9. Karena $K$ tertutup secara aljabar, ideal-ideal
maksimal tersebut bersesuaian secara bijektif dengan titik-titik perpotongan
$V(F)$ dan $V(G)$. Isomorfisme yang dinyatakan pun diperoleh. $\square$

> **Catatan edisi - simbol gelanggang dalam bukti.** Sumber menulis
> $R/(F,G)$ pada bukti ini tanpa pernah mendefinisikan $R$. Dari pernyataan
> korolari dan penerapan Teorema 26.9, gelanggang yang dimaksud adalah
> $K[X,Y]/(F,G)$; edisi menuliskannya secara eksplisit.

<!-- upstream_entity: Ebene algebraische Kurve/Schnittmultiplizität/Summe der Multiplizitäten ist Restklassendimension/Fakt -->

### Teorema 26.11: jumlah multiplisitas perpotongan {#br-ak-2012-l26-thm-03}

Misalkan $K$ suatu lapangan tertutup secara aljabar dan

$$
F,G\in K[X,Y]
$$

dua polinom tanpa pembagi prima bersama. Maka

$$
\dim_K\bigl(K[X,Y]/(F,G)\bigr)
=\sum_P\operatorname{mult}_P(F,G),
$$

dengan jumlah diambil atas semua titik $P\in V(F,G)$.

<!-- upstream_entity: Ebene algebraische Kurve/Schnittmultiplizität/Summe der Multiplizitäten ist Restklassendimension/Fakt/Beweis -->

#### Bukti {#br-ak-2012-l26-thm-03-proof}

Pernyataan ini langsung mengikuti isomorfisme yang dibuktikan dalam
Korolari 26.10, sebab dimensi suatu produk berhingga ruang vektor adalah
jumlah dimensi faktor-faktornya. $\square$

Sebagai penutup, kita catat tanpa bukti teorema berikut, yang memberi taksiran
antara multiplisitas perpotongan dan multiplisitas kedua kurva.

<!-- upstream_entity: Ebene algebraische Kurven/Schnittmultiplizität/Abschätzung von Schnittmultiplizität und Multiplizität/Fakt -->

### Teorema 26.12: batas bawah multiplisitas perpotongan {#br-ak-2012-l26-thm-04}

Misalkan

$$
F,G\in K[X,Y]
$$

dua polinom tanpa komponen bersama dan

$$
P\in V(F,G).
$$

Maka

$$
\operatorname{mult}_P(F,G)
\geq m_P(F)\,m_P(G).
$$

> **Catatan edisi - hipotesis keterhinggaan.** Sumber tidak menyatakan bahwa
> $F$ dan $G$ harus tanpa komponen bersama. Tanpa syarat itu, hasil bagi lokal
> pada definisi multiplisitas perpotongan dapat berdimensi tak hingga. Edisi
> menambahkan hipotesis yang sudah mengatur seluruh pembahasan dalam kuliah
> ini.

<!-- upstream_entity: Ebene algebraische Kurven/Schnittmultiplizität/Abschätzung von Schnittmultiplizität und Multiplizität/Fakt/Beweisverweis -->

#### Rujukan bukti {#br-ak-2012-l26-thm-04-proof-reference}

Lihat Fulton, *Algebraic Curves*, Bab III.3.
