---
title: "Kuliah 14 - Fungsi Aljabar pada Varietas"
stable_id: br-ak-2025-2026-l14
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 14"
upstream_pageid: 165903
upstream_revid: 1051343
upstream_timestamp: "2025-08-18T08:06:49Z"
upstream_mediawiki_sha1: 5bc2e2c3db815edeb4f10640564c8cd793de74a8
source_url: "https://de.wikiversity.org/w/index.php?oldid=1051343"
authority_manifest: authority/wikiversity/unit-14/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: a63c3481d0a9cfa9b960f12c9bf0eec9a5d39cecfb61eddb8f9d96190e52e83e
lecture_xml_sha256: 779422f6a20c9462db83e79f38450073da2b0653a239b1028795cc6b49cf7a32
lecture_expanded_tex_sha256: 26347a8614ea18ca719d548ea3d58d9e8d419bf5adc469c19e757d48e53c3f55
license: "CC BY-SA 4.0 for translated course text; media retain component rights in authority/RIGHTS-unit-14.csv"
translation_status: complete
---

# Kuliah 14: Fungsi Aljabar pada Varietas {#br-ak-2025-2026-l14}

## Fungsi aljabar {#br-ak-2025-2026-l14-s01}

Apakah yang dimaksud dengan morfisme antara dua himpunan aljabar afin $V$
dan $W$? Mula-mula kita meninjau kasus ketika

$$
W=\mathbb A_K^1
$$

adalah garis afin. Misalkan

$$
V=V(\mathfrak a)\subseteq\mathbb A_K^n
$$

diberikan sebagai subhimpunan tertutup suatu ruang afin. Setiap polinom

$$
F\in K[X_1,\ldots,X_n]
$$

memberikan pemetaan

$$
F:\mathbb A_K^n\longrightarrow\mathbb A_K^1=K
$$

dan, dengan restriksi, juga suatu pemetaan pada $V$. Hal ini telah kita
tinjau ketika mendefinisikan gelanggang koordinat. Demikian pula, suatu unsur
$F$ dari aljabar-$K$ bertipe hingga $R$ memberikan fungsi

$$
\begin{aligned}
K\!-\!\operatorname{Spek}(R)&\longrightarrow\mathbb A_K^1,\\
P&\longmapsto F(P).
\end{aligned}
$$

Ini adalah pemetaan spektrum yang, menurut Proposisi 12.8(2), bersesuaian
dengan homomorfisme substitusi

$$
K[T]\longrightarrow R,
\qquad T\longmapsto F.
$$

Pada himpunan terbuka

$$
D(F)\cong K\!-\!\operatorname{Spek}(R_F),
$$

fungsi $1/F$ terdefinisi dengan baik menurut Teorema 13.4. Sekarang kita akan
menjelaskan fungsi aljabar pada suatu himpunan terbuka Zariski sembarang
$U\subseteq V$. Definisi berikut disusun agar syarat "aljabar" merupakan
sifat lokal.

<!-- upstream_entity: K-Spektrum/Algebraisch abgeschlossener Körper/Algebraische (reguläre) Funktion auf offener Menge/Punktweise und global/Definition -->

### Definisi: fungsi aljabar pada himpunan terbuka {#br-ak-2025-2026-l14-def-01}

Misalkan $K$ lapangan tertutup secara aljabar, $R$ aljabar-$K$ bertipe
hingga, dan

$$
V=K\!-\!\operatorname{Spek}(R).
$$

Misalkan $P\in V$, $U\subseteq V$ suatu himpunan terbuka Zariski dengan
$P\in U$, dan

$$
f:U\longrightarrow\mathbb A_K^1=K
$$

suatu fungsi. Fungsi $f$ disebut *aljabar* (juga *reguler* atau
*polinomial*) di titik $P$ jika terdapat $G,H\in R$ dengan

$$
P\in D(H)\subseteq U
$$

dan

$$
f(Q)=\frac{G(Q)}{H(Q)}
\qquad\text{untuk setiap }Q\in D(H).
$$

Fungsi $f$ disebut *aljabar pada $U$* jika $f$ aljabar di setiap titik
$U$.

Setiap unsur $f\in R$ tentu mendefinisikan fungsi aljabar pada setiap
subhimpunan terbuka dari spektrum-$K$. Namun, pada umumnya tidak mudah
memberikan deskripsi yang ringkas bagi semua fungsi aljabar.

<!-- upstream_entity: K-Spektrum/Algebraisch abgeschlossener Körper/Algebraische Funktion auf offener Menge/Bemerkung -->

### Catatan: sifat lokal dan penyajian pecahan {#br-ak-2025-2026-l14-rem-01}

Dalam Definisi 14.1, syarat $D(H)\subseteq U$ tidak esensial. Jika terdapat
penyajian $f=G/H$ pada $D(H)$ dengan $P\in D(H)$, pilih $H'$ sedemikian
sehingga

$$
P\in D(H')\subseteq U.
$$

Pada

$$
D(H)\cap D(H')=D(HH')
$$

kita dapat memakai penyajian

$$
f=\frac{GH'}{HH'}.
$$

Jika $f=G/H$ merupakan penyajian pecahan di titik $P$, penyajian yang sama
berlaku bagi semua titik di $D(H)$. Jadi $f$ aljabar pada seluruh himpunan
terbuka $D(H)$. Karena itu kita tidak perlu bekerja dengan tak berhingga
banyak penyajian berbeda: cukup memakai berhingga banyak pecahan
$G_i/H_i$ untuk suatu penutup

$$
U=\bigcup_{i\in I}D(H_i).
$$

Untuk $K=\mathbb C$, setiap fungsi aljabar juga kontinu terhadap topologi
metrik; jika $R=\mathbb C[X_1,\ldots,X_n]$, fungsi itu holomorfik.

<!-- upstream_entity: Affine Varietäten/Algebraische Funktionen/ux-vy/Funktion auf D(x,y)/Beispiel -->

### Contoh: fungsi yang direkatkan dari dua pecahan {#br-ak-2025-2026-l14-exm-01}

Misalkan

$$
V=V(WX-ZY)\subseteq\mathbb A_K^4
$$

dan

$$
U=D(X,Y)=D(X)\cup D(Y)\subset V.
$$

Pada $U$, fungsi yang didefinisikan oleh

$$
f=\frac ZX=\frac WY
$$

adalah fungsi aljabar. Kedua pecahan tersebut jelas memberikan fungsi
aljabar masing-masing pada $D(X)$ dan $D(Y)$. Agar keduanya mendefinisikan
satu fungsi pada $U$, nilainya harus sama pada irisan
$D(X)\cap D(Y)=D(XY)$. Ambil

$$
Q=(w,x,y,z)\in D(XY)\cap V.
$$

Kita mempunyai $x,y\ne0$ dan $wx=zy$, sehingga

$$
\frac ZX(Q)=\frac zx=\frac wy=\frac WY(Q).
$$

<!-- upstream_entity: K-Spektrum/Algebraisch abgeschlossener Körper/Algebraische Funktion auf offener Menge/Ring/Fakt -->

### Lema: fungsi aljabar membentuk aljabar {#br-ak-2025-2026-l14-lem-01}

Misalkan $K$ lapangan tertutup secara aljabar, $R$ aljabar-$K$ bertipe
hingga, $V=K\!-\!\operatorname{Spek}(R)$, dan $U\subseteq V$ terbuka
Zariski. Himpunan fungsi aljabar pada $U$ merupakan subgelanggang - bahkan
subaljabar-$K$ - dari gelanggang semua fungsi $U\to K$, dengan operasi
dilakukan di $K$.

#### Bukti {#br-ak-2025-2026-l14-lem-01-proof}

Kita harus memeriksa fungsi konstan nol dan satu, negatif suatu fungsi
aljabar, serta jumlah dan hasil kali dua fungsi aljabar. Cukup kita tuliskan
kasus jumlah. Misalkan $f_1,f_2$ aljabar dan $P\in U$. Terdapat
$G_1,H_1,G_2,H_2\in R$ dengan

$$
f_1(Q)=\frac{G_1(Q)}{H_1(Q)}
\quad(Q\in D(H_1)\subseteq U),
\qquad P\in D(H_1),
$$

dan

$$
f_2(Q)=\frac{G_2(Q)}{H_2(Q)}
\quad(Q\in D(H_2)\subseteq U),
\qquad P\in D(H_2).
$$

Tetapkan $H=H_1H_2$. Maka

$$
P\in D(H)=D(H_1)\cap D(H_2)\subseteq U.
$$

Untuk $Q\in D(H)$ berlaku

$$
\begin{aligned}
(f_1+f_2)(Q)
&=f_1(Q)+f_2(Q)\\
&=\frac{G_1(Q)}{H_1(Q)}+\frac{G_2(Q)}{H_2(Q)}\\
&=\frac{G_1(Q)H_2(Q)+G_2(Q)H_1(Q)}{H_1(Q)H_2(Q)}\\
&=\frac{(G_1H_2+G_2H_1)(Q)}{(H_1H_2)(Q)}.
\end{aligned}
$$

Jadi fungsi jumlah mempunyai penyajian pecahan pada lingkungan terbuka
Zariski $D(H)$ dari $P$. Kasus-kasus lainnya serupa.

<!-- upstream_entity: K-Spektrum/Algebraisch abgeschlossener Körper/Algebraische (reguläre) Funktion auf offener Menge/Schnittring/Definition -->

### Definisi: gelanggang seksi aljabar {#br-ak-2025-2026-l14-def-02}

Dalam situasi di atas, gelanggang

$$
\Gamma(U,\mathcal O)
=\{f:U\longrightarrow K\mid f\text{ aljabar}\}
$$

disebut *gelanggang fungsi aljabar* pada $U$. Gelanggang ini juga disebut
*gelanggang struktur* atau *gelanggang seksi* pada $U$. Simbol $\mathcal O$
(dibaca "O") menyatakan apa yang disebut *berkas struktur*.

<!-- upstream_entity: K-Spektrum/Ring der algebraischen Funktionen/Restriktion/Fakt -->

### Lema: pemetaan restriksi {#br-ak-2025-2026-l14-lem-02}

Misalkan $U_1\subseteq U_2$ subhimpunan terbuka dari
$V=K\!-\!\operatorname{Spek}(R)$. Terdapat homomorfisme aljabar-$K$ alami

$$
\Gamma(U_2,\mathcal O)\longrightarrow\Gamma(U_1,\mathcal O).
$$

#### Bukti {#br-ak-2025-2026-l14-lem-02-proof}

Suatu fungsi $f:U_2\to K$ langsung memberikan fungsi pada $U_1$ dengan
restriksi. Deskripsi lokal-aljabar yang berlaku bagi $f$ di setiap titik
$P\in U_2$ juga berlaku pada subhimpunan yang lebih kecil $U_1$.

Pemetaan pada lema ini disebut *pemetaan restriksi*.

<!-- upstream_entity: K-Spektrum/Ring der algebraischen Funktionen/U subseteq D(f)/Unabhängigkeit/Fakt -->

### Lema: kebebasan dari ruang ambien terbuka utama {#br-ak-2025-2026-l14-lem-03}

Misalkan $F\in R$ dan

$$
U\subseteq D(F)\subseteq V=K\!-\!\operatorname{Spek}(R)
$$

terbuka. Definisi $\Gamma(U,\mathcal O)$ memberikan gelanggang yang sama,
baik jika ruang ambiennya diambil sebagai $V$ maupun sebagai

$$
D(F)=K\!-\!\operatorname{Spek}(R_F).
$$

#### Bukti {#br-ak-2025-2026-l14-lem-03-proof}

Fungsi-fungsi pada $U$ tentu hanya bergantung pada $U$, bukan pada suatu
ruang ambien. Kita tinggal membuktikan bahwa syarat lokal-aljabarnya juga
hanya bergantung pada $U$.

Ambil $P\in U$. Penyajian

$$
\varphi=\frac GH\text{ pada }D(H),
\qquad P\in D(H),\quad G,H\in R,
$$

langsung memberikan penyajian pecahan pada $D(HF)$ jika $G,H$ dipandang
sebagai unsur $R_F$.

Sebaliknya, misalkan dalam $R_F$ terdapat penyajian

$$
\varphi=\frac{\widetilde G}{\widetilde H}
\text{ pada }D(\widetilde H),
\qquad P\in D(\widetilde H),
$$

dengan

$$
\widetilde G=\frac G{F^r},
\qquad
\widetilde H=\frac H{F^s}.
$$

Untuk $Q\in D(HF)$ berlaku

$$
\varphi(Q)
=\frac{\widetilde G(Q)}{\widetilde H(Q)}
=\frac{G(Q)/F^r(Q)}{H(Q)/F^s(Q)}
=\frac{G(Q)F^s(Q)}{H(Q)F^r(Q)}.
$$

Pembilang dan penyebut terakhir terletak di $R$, dan
$HF^r(P)\ne0$. Jadi $D(HF^r)$ merupakan lingkungan terbuka dari $P$ yang
memberikan penyajian terhadap $V$.

<!-- upstream_entity: K-Spektrum/Algebraisch abgeschlossener Körper/Verschiedene rationale Darstellungen einer aIgebraischen Funktion/Beziehung im Koordinatenring/Fakt -->

### Lema: hubungan antara dua penyajian rasional {#br-ak-2025-2026-l14-lem-04}

Misalkan $f:U\to K$ fungsi aljabar pada himpunan terbuka Zariski
$U\subseteq V=K\!-\!\operatorname{Spek}(R)$. Misalkan di sekitar
$P\in U$ fungsi itu mempunyai dua penyajian

$$
\frac{G_1}{H_1}
\qquad\text{dan}\qquad
\frac{G_2}{H_2},
$$

dengan $G_1,H_1,G_2,H_2\in R$ dan
$P\in D(H_1),D(H_2)\subseteq U$. Maka terdapat $r\in\mathbb N$ sehingga

$$
H_1^rH_2^r(G_1H_2-G_2H_1)^r=0
\quad\text{di }R.
$$

Jika $R$ tereduksi, bahkan berlaku

$$
H_1H_2(G_1H_2-G_2H_1)=0.
$$

#### Bukti {#br-ak-2025-2026-l14-lem-04-proof}

Tinjau unsur

$$
F=H_1H_2(G_1H_2-G_2H_1)
$$

pada $V$. Kita tunjukkan bahwa unsur ini menginduksi fungsi nol. Ambil
$Q\in V$. Jika $H_1(Q)=0$ atau $H_2(Q)=0$, maka langsung $F(Q)=0$.
Jika keduanya tidak nol, maka $Q\in D(H_1)\cap D(H_2)$ dan

$$
\frac{G_1(Q)}{H_1(Q)}=f(Q)=\frac{G_2(Q)}{H_2(Q)}.
$$

Jadi $G_1(Q)H_2(Q)=G_2(Q)H_1(Q)$ dan kembali $F(Q)=0$. Dengan
Nullstellensatz Hilbert, terdapat $r$ sehingga $F^r=0$ di $R$. Jika $R$
tereduksi, $F=0$.

![Permukaan pelana monyet berwarna tembaga dengan tiga lembah dan tiga punggung](authority/assets/Monkey_Saddle_Surface_Shaded-500.png)

*Grafik suatu fungsi global pada ruang afin dua dimensi; Inductiveload,
domain publik. Rincian sumber berada pada kredit media Unit 14.*

<!-- upstream_entity: K-Spektrum/Algebraisch abgeschlossener Körper/Algebraische (reguläre) Funktion auf offener Menge/Globaler Schnittring ist Koordinatenring/Fakt -->

### Teorema: seksi global pada spektrum afin {#br-ak-2025-2026-l14-thm-01}

Misalkan $K$ lapangan tertutup secara aljabar, $R$ aljabar-$K$ bertipe
hingga yang tereduksi, dan $V=K\!-\!\operatorname{Spek}(R)$. Maka

$$
\Gamma(V,\mathcal O)=R.
$$

#### Bukti {#br-ak-2025-2026-l14-thm-01-proof}

Setiap $F\in R$ langsung memberikan fungsi aljabar pada seluruh $V$, jadi
terdapat homomorfisme aljabar-$K$

$$
R\longrightarrow\Gamma(V,\mathcal O).
$$

Jika $F$ menginduksi fungsi nol di setiap titik, Teorema 11.1 dan sifat
tereduksi memberikan $F=0$. Jadi pemetaan itu injektif.

Sekarang misalkan $f:V\to K$ suatu fungsi aljabar. Untuk setiap $P\in V$
terdapat $G_P,H_P\in R$ dengan $P\in D(H_P)$ dan

$$
f=\frac{G_P}{H_P}\quad\text{pada }D(H_P).
$$

Himpunan-himpunan $D(H_P)$ menutupi $V$. Menurut Korolari 11.12, unsur-unsur
$H_P$ membangkitkan ideal satuan, sehingga berhingga banyak di antaranya
sudah membangkitkan ideal satuan. Nyatakan unsur-unsur itu dengan

$$
H_i=H_{P_i},\qquad i=1,\ldots,m.
$$

Maka $D(H_i)$ menutupi seluruh $V$. Pada setiap irisan
$D(H_iH_j)=D(H_i)\cap D(H_j)$ berlaku

$$
f(Q)=\frac{G_i(Q)}{H_i(Q)}=\frac{G_j(Q)}{H_j(Q)}.
$$

Menurut Lema 14.8 dan sifat tereduksi,

$$
H_iH_jG_iH_j=H_iH_jG_jH_i
$$

di $R$. Ganti $H_i$ dengan $H_i^2$ dan $G_i$ dengan $G_iH_i$. Penyajian
$G_i/H_i$ tetap sama, sedangkan hubungan terakhir menyederhana menjadi

$$
H_iG_j=H_jG_i.
$$

Karena $H_i$ membangkitkan ideal satuan, terdapat $A_i\in R$ dengan

$$
\sum_{i=1}^m A_iH_i=1.
$$

Tetapkan

$$
F=\sum_{i=1}^m A_iG_i.
$$

Kita klaim bahwa $F$ menginduksi $f$ pada seluruh $V$. Ambil $Q\in V$;
tanpa mengurangi keumuman, misalkan $Q\in D(H_1)$. Maka

$$
\begin{aligned}
f(Q)
&=\frac{G_1(Q)}{H_1(Q)}\\
&=\frac{G_1(Q)}{H_1(Q)}
  \left(\sum_{i=1}^m A_iH_i\right)(Q)\\
&=\sum_{i=1}^m A_i(Q)\frac{G_1(Q)H_i(Q)}{H_1(Q)}\\
&=\sum_{i=1}^m A_i(Q)G_i(Q)\\
&=F(Q).
\end{aligned}
$$

Jadi homomorfisme di atas juga surjektif.

<!-- upstream_entity: K-Spektrum/Algebraisch abgeschlossener Körper/Algebraische (reguläre) Funktion auf D(f)/Ist R f/Fakt -->

### Korolari: seksi pada himpunan terbuka utama {#br-ak-2025-2026-l14-cor-01}

Misalkan $F\in R$ dalam situasi teorema sebelumnya. Maka

$$
\Gamma(D(F),\mathcal O)=R_F.
$$

#### Bukti {#br-ak-2025-2026-l14-cor-01-proof}

Pernyataan ini langsung mengikuti dari Lema 14.7 dan Teorema 14.9.

<!-- upstream_entity: Hilbertsches Problem/14/Schnittring/Bemerkung -->

### Catatan: masalah Hilbert ke-14 {#br-ak-2025-2026-l14-rem-02}

Salah satu varian masalah Hilbert ke-14 menanyakan apakah gelanggang fungsi
aljabar $\Gamma(U,\mathcal O)$ dibangkitkan secara hingga untuk setiap
himpunan terbuka $U$. Jawabannya benar untuk himpunan terbuka berbentuk
$U=D(f)$, juga ketika $R$ reguler atau faktorial, dan pada dimensi kecil.
Namun, secara umum jawabannya tidak benar.

---

**Provenans edisi.** Terjemahan dan produksi pembaca: OpenAI Codex
gpt-5.6-sol, Ultra. Sumber, pengarang, dan lisensi komponen dipertahankan
seperti dinyatakan dalam metadata dan berkas hak edisi.
