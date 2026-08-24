---
title: "Kuliah 8 - Kurva Aljabar yang Didefinisikan Secara Mekanis"
stable_id: br-ak-2025-2026-l08
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 8"
upstream_pageid: 165897
upstream_revid: 1051293
upstream_timestamp: "2025-08-18T07:32:25Z"
upstream_mediawiki_sha1: f84804863234f9cbcd9f9c06f334e60a8bde42fa
source_url: "https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)/Vorlesung_8?oldid=1051293"
license: "CC BY-SA 4.0 for translated course text; media retain component rights in authority/RIGHTS-unit-08.csv"
translation_status: complete
---

# Kuliah 8: Kurva Aljabar yang Didefinisikan Secara Mekanis {#br-ak-2025-2026-l08}

## Kurva aljabar yang didefinisikan secara mekanis {#br-ak-2025-2026-l08-s01}

![Gedung berbentuk lemniskata](authority/assets/Lemniscate_Building.gif)

Misalkan $S$ sebuah batang kaku
(bayangkan sebuah komponen mesin mekanis)
dengan dua titik tetap

$$
P_1,P_2\in S
$$

(bayangkan sendi-sendi).
Batang ini dapat bergerak dalam bidang (yakni $\mathbb R^2$), dengan syarat
bahwa kedua titik tersebut masing-masing harus berada pada dua lintasan
tertentu $B_1$ dan $B_2$ (bayangkan rel). Lintasan-lintasan itu dapat diberikan
dengan cukup sederhana, misalnya oleh garis atau lingkaran. Pada mesin uap,
sebuah roda yang dapat berputar dan sebuah rel lurus dihubungkan oleh suatu
batang. Bagaimana proses gerak yang bersesuaian dideskripsikan? Apa saja
*konfigurasi sistem yang diizinkan*? Karena konfigurasi semacam itu ditentukan
oleh posisi kedua titik, dan masing-masing posisi diberikan oleh dua koordinat
bidang, secara keseluruhan kita menghadapi situasi berdimensi empat.

Jika kita menetapkan sebuah titik $P$ pada batang (misalnya dengan memberinya
warna), seperti apakah *lintasan gerak* (atau *trajektori*) titik ini dalam
bidang?

Untuk kasus-kasus ekstrem

$$
P=P_1
\qquad\text{dan}\qquad
P=P_2,
$$

lintasan-lintasan geraknya merupakan (biasanya) subhimpunan sejati dari
$B_1$ dan $B_2$. Untuk titik-titik di antaranya, kita mengharapkan suatu
*deformasi kontinu* dari lintasan yang satu ke lintasan yang lain.

### [Situasi: sistem mekanis batang penghubung](https://de.wikiversity.org/wiki/Mechanische_ebene_Kurven/Stangenkoppelung/Bemerkung) {#br-ak-2025-2026-l08-sit-01}

Misalkan $B_1$ dan $B_2$ dua kurva aljabar bidang yang dideskripsikan oleh
persamaan $F_1=0$ dan $F_2=0$, dengan

$$
F_1,F_2\in K[X,Y].
$$

Misalkan $S$ suatu “garis bergerak” (sebuah batang) dengan dua titik

$$
P_1,P_2\in S,
\qquad
P_1\ne P_2,
$$

yang berjarak $d$ satu sama lain. *Sistem mekanis* yang diberikan oleh semua
posisi $S$ dalam bidang yang sekaligus memenuhi

$$
P_1\in B_1
\qquad\text{dan}\qquad
P_2\in B_2
$$

dideskripsikan sebagai berikut.

Posisi batang dalam bidang ditentukan secara tunggal apabila posisi kedua
titiknya telah ditentukan (ini belum memperhitungkan syarat jarak), jadi oleh
empat variabel

$$
(P_1,P_2)=(x_1,y_1,x_2,y_2).
$$

Suatu *konfigurasi yang diizinkan* harus memenuhi tiga syarat aljabar berikut.

1. $F_1(x_1,y_1)=0$.

2. $F_2(x_2,y_2)=0$.

3. $(x_2-x_1)^2+(y_2-y_1)^2=d^2$ (syarat jarak).

Jadi, terdapat tiga persamaan aljabar dalam empat variabel; karena itu, sebagai
himpunan solusi kita mengharapkan sebuah kurva dalam $\mathbb A_K^4$.
Sebuah titik

$$
P\in S
$$

dideskripsikan melalui jaraknya dari $P_1$ atau $P_2$. Karena titik-titik ini
bergerak dalam sistem mekanis, kita menetapkan koordinat *titik yang ikut
bergerak* $P$ sebagai

$$
P=P_1+u(P_2-P_1)
$$

(jadi, jarak $P$ dari $P_1$ adalah
$\lVert u(P_2-P_1)\rVert=\lvert ud\rvert$), dan menuliskan koordinatnya sebagai

$$
\begin{aligned}
(x,y)
&=(x_1,y_1)+u(x_2-x_1,y_2-y_1)\\
&=(ux_2+(1-u)x_1,uy_2+(1-u)y_1).
\end{aligned}
$$

Seluruh sistem mekanis kemudian dapat dinyatakan (melalui suatu transformasi
linear) dalam empat variabel $x_1,y_1,x,y$. Untuk $u\ne0$, kita menyubstitusikan

$$
x_2=\frac{x-(1-u)x_1}{u}
\qquad\text{dan}\qquad
y_2=\frac{y-(1-u)y_1}{u}
$$

ke dalam persamaan-persamaannya. Dalam variabel-variabel baru diperoleh tiga
persamaan

$$
\begin{aligned}
F_1(x_1,y_1)&=0,\\
F_2\left(
\frac{x-(1-u)x_1}{u},
\frac{y-(1-u)y_1}{u}
\right)&=0,\\
(x-x_1)^2+(y-y_1)^2&=u^2d^2.
\end{aligned}
$$

Pada prinsipnya, trajektori yang bersesuaian dengan $P$ dapat diperoleh dengan
“mengeliminasi” variabel $x_1$ dan $y_1$ dari sistem persamaan ini, sehingga
diperoleh suatu persamaan aljabar bagi $x$ dan $y$. Akan tetapi, hal ini lebih
mudah dikatakan daripada dilakukan; sering kali lebih berguna untuk
menyederhanakan sistem persamaan melalui manipulasi yang cerdik.

### [Catatan: bidang yang ikut bergerak](https://de.wikiversity.org/wiki/Mechanische_ebene_Kurven/Stangenkoppelung/Mitbewegte_Ebene/Bemerkung) {#br-ak-2025-2026-l08-rem-01}

Kadang-kadang kita juga tertarik pada situasi ketika seluruh bidang ikut
bergerak bersama batang, serta pada trajektori titik-titik dalam bidang itu.
Hal ini terjadi, misalnya, apabila komponen-komponen mesin lain dipasang pada
batang. Dalam kasus ini, setiap titik bidang dapat dinyatakan relatif terhadap
$P_1$ dan $P_2$ sebagai

$$
(x,y)
=(x_1,y_1)
+u(x_2-x_1,y_2-y_1)
+v(y_2-y_1,-x_2+x_1).
$$

Jadi, titik $P_1$ diambil sebagai titik asal bidang bergerak, garis penghubung
ke $P_2$ sebagai sumbu koordinat pertama, dan sumbu yang tegak lurus terhadapnya
sebagai sumbu koordinat kedua.

Dengan demikian, seluruh sistem mekanis (batang) dideskripsikan oleh empat
variabel dengan tiga persamaan. Namun, cara kerjanya yang terlihat, yaitu
proses gerak suatu titik tetap $P$ pada $S$, menghasilkan sebuah trajektori
dalam bidang afin.

Kita meninjau beberapa contoh.

## Dua garis sebagai lintasan {#br-ak-2025-2026-l08-s02}

### [Contoh: dua garis sebagai lintasan](https://de.wikiversity.org/wiki/Mechanische_ebene_Kurven/Stangenkoppelung/Zwei_Geraden/Beispiel) {#br-ak-2025-2026-l08-ex-01}

Misalkan $L_1$ dan $L_2$ dua garis dalam bidang real $\mathbb R^2$, dan
misalkan $S$ sebuah garis bergerak (sebuah batang) dengan dua titik $P_1,P_2$
yang berjarak $d$ satu sama lain. Konfigurasi sistem yang diizinkan adalah
posisi-posisi $S$ yang sekaligus memenuhi

$$
P_1\in L_1
\qquad\text{dan}\qquad
P_2\in L_2.
$$

Garis-garis tersebut ditetapkan oleh

$$
L_1=\{(x,y)\mid a_1x+b_1y=c_1\}
$$

dan

$$
L_2=\{(x,y)\mid a_2x+b_2y=c_2\}.
$$

Menurut [Situasi 8.1](#br-ak-2025-2026-l08-sit-01), konfigurasi yang diizinkan
ditetapkan oleh tiga syarat

$$
\begin{aligned}
a_1x_1+b_1y_1&=c_1,\\
a_2x_2+b_2y_2&=c_2,\\
(x_2-x_1)^2+(y_2-y_1)^2&=d^2.
\end{aligned}
$$

Himpunan solusi dari masing-masing persamaan linear merupakan subruang
berdimensi tiga. Himpunan solusi persamaan ketiga dapat dipandang sebagai
hasil kali sebuah lingkaran (dalam variabel $x_2-x_1$ dan $y_2-y_1$) dengan
suatu bidang afin. Ini merupakan sejenis silinder, meskipun serat-seratnya
berdimensi dua. Bagaimana lokus nol bersamanya dapat dideskripsikan, dan seperti
apakah trajektori sistem mekanis yang dihasilkan oleh suatu titik

$$
P\in S?
$$

Melalui suatu transformasi variabel, kita dapat mengandaikan bahwa garis
pertama adalah sumbu $x$, jadi didefinisikan oleh persamaan

$$
y=0,
$$

sedangkan garis yang lain didefinisikan oleh

$$
ax+by=c.
$$

Untuk sistem tersebut, ini memberikan syarat $y_1=0$, sehingga variabel
$y_1$ dapat dieliminasi. Kita lalu memperoleh suatu sistem dengan tiga
variabel $x_1,x_2,y_2$ dan dua syarat

$$
\begin{aligned}
(x_2-x_1)^2+y_2^2&=d^2,\\
ax_2+by_2&=c.
\end{aligned}
$$

**Garis-garis sejajar.**

![Garis-garis sejajar](authority/assets/Parallelle_lijnen.png)

Jika garis kedua sejajar dengan garis pertama, maka $a=0$, dan persamaan
kedua dapat diselesaikan terhadap $y_2$, sehingga diperoleh

$$
y_2=\frac cb=e
$$

(dengan $b\ne0$; jika tidak, persamaan itu tidak mendefinisikan sebuah garis).
Bilangan $e$ adalah jarak antara kedua garis sejajar. Sekarang $y_2$ juga dapat
dieliminasi, dan yang tersisa hanyalah persamaan

$$
(x_2-x_1)^2+e^2=d^2,
$$

atau

$$
(x_2-x_1)^2=d^2-e^2=(d-e)(d+e).
$$

Jika $e>d$, persamaan ini tidak mempunyai solusi (jarak konstan antara
garis-garis sejajar lebih besar daripada jarak kopling pada batang).

Jika $e=d$, diperoleh syarat

$$
x_1=x_2.
$$

Ini bersesuaian dengan situasi ketika jarak antara garis-garis sejajar sama
dengan jarak kopling. Konfigurasi yang diizinkan hanyalah konfigurasi ketika
batang tegak lurus terhadap kedua garis. Jadi, himpunan solusinya adalah sebuah
garis. Bagi setiap titik pada batang, trajektorinya hanyalah sebuah garis
sejajar lain.

Sekarang, misalkan $e<d$. Maka

$$
x_2-x_1=\pm\sqrt{(d-e)(d+e)}.
$$

Himpunan solusinya terdiri atas dua garis yang saling lepas. Ini bersesuaian
dengan dua pemasangan berbeda yang tidak dapat diubah menjadi satu sama lain.
Jadi, sistem mekanis tersebut terdiri atas dua komponen terhubung. Akan tetapi,
untuk suatu titik pada batang, kedua pemasangan menghasilkan trajektori yang
sama, yaitu sebuah garis sejajar yang, dalam pengertian tertentu, dilintasi
dua kali. Dengan demikian, himpunan solusi sistem mekanis lengkap terdiri atas
dua garis afin (sejajar) dalam ruang afin berdimensi empat, sedangkan
trajektori-trajektorinya bagi suatu titik tetap hanya membentuk satu garis.

**Garis-garis tidak sejajar.**

Sekarang kita meninjau kasus ketika kedua garis tidak sejajar. Maka keduanya
berpotongan dan himpunan solusi tidak mungkin kosong. Melalui suatu
transformasi linear lebih lanjut, kita dapat mengandaikan bahwa titik
perpotongannya adalah titik nol $(0,0)$. Persamaan kedua kemudian dideskripsikan
oleh

$$
x_2=ey_2.
$$

Dengan demikian, $x_2$ dapat dieliminasi dan, dalam dua variabel $x_1,y_2$,
kita memperoleh satu-satunya persamaan

$$
(ey_2-x_1)^2+y_2^2=d^2.
$$

Jadi, ruang konfigurasi sistem mekanis berlangsung dalam suatu bidang (yang
didefinisikan oleh $y_1=0$ dan $x_2=ey_2$) dan dideskripsikan oleh sebuah
kuadrik. Jika $ey_2-x_1$ dipandang sebagai variabel baru, terlihat bahwa
kuadrik itu adalah sebuah elips (dalam koordinat $x_1,y_2$; dalam koordinat
$ey_2-x_1,y_2$, kuadrik itu merupakan sebuah lingkaran).

![Elips](authority/assets/Ellipse_tri.png)

Seperti apakah trajektorinya? Misalkan $P$ titik pada batang yang diberikan
oleh

$$
P_1+t(P_2-P_1).
$$

Menurut [deskripsi Situasi 8.1](#br-ak-2025-2026-l08-sit-01), titik $P$
mempunyai koordinat

$$
((1-t)x_1+tey_2,ty_2),
$$

dengan syarat

$$
(ey_2-x_1)^2+y_2^2=d^2.
$$

Dalam kasus-kasus ekstrem $t=0$ dan $t=1$, himpunan solusi yang diperoleh
masing-masing adalah $(x_1,0)$ (dengan $x_1$ sembarang) dan $(ey_2,y_2)$
(dengan $y_2$ sembarang). Di sini, syarat

$$
(ey_2-x_1)^2+y_2^2=d^2
$$

tetap harus dipenuhi; artinya, untuk $x_1$ (atau $y_2$) yang diberikan, harus
ada solusi persamaan dalam variabel yang lain. Solusi seperti itu ada apabila
$x_1$ (atau $y_2$) cukup kecil. Secara keseluruhan, kita memperoleh ruas-ruas
tertentu pada garis-garis semula. Titik-titik $P_1$ dan $P_2$ harus tetap
berada pada lintasannya dan tidak dapat menjauh tanpa batas dari garis yang
lain.

> **Catatan edisi:** Ungkapan “cukup kecil” pada sumber berarti kecil dalam
> nilai mutlak. Untuk $t=0$, peminimuman ruas kiri terhadap $y_2$ memberi
> syarat tepat $|x_1|\le d\sqrt{1+e^2}$; untuk $t=1$, peminimuman terhadap
> $x_1$ memberi syarat tepat $|y_2|\le d$.

Jadi, misalkan

$$
t\ne0,1.
$$

Dari ansatz

$$
(x,y)=((1-t)x_1+tey_2,ty_2)
$$

diperoleh

$$
y_2=\frac yt
$$

dan

$$
x_1=\frac{x-tey_2}{1-t}=\frac{x-ey}{1-t}
$$

(jadi, prapetanya ditentukan secara tunggal). Persamaannya lalu menjadi

$$
\left(\frac{ey}{t}-\frac{x-ey}{1-t}\right)^2+\frac{y^2}{t^2}=d^2,
$$

yang kembali merupakan persamaan sebuah elips.

## Garis dan lingkaran sebagai lintasan {#br-ak-2025-2026-l08-s03}

Sekarang kita meninjau kasus suatu kurva mekanis ketika lintasan yang satu
adalah sebuah garis dan lintasan kedua sebuah lingkaran. Inilah situasi pada
mesin uap (khususnya apabila garis melalui pusat lingkaran).

![Mesin uap sedang bekerja](authority/assets/Steam_engine_in_action.gif)

Tanpa mengurangi keumuman, kita dapat mengandaikan bahwa garis diberikan oleh

$$
y=0.
$$

Koordinat titik pada garis kemudian adalah

$$
P_1=(x_1,y_1)=(x_1,0).
$$

Untuk lingkarannya, kita dapat mengandaikan bahwa pusatnya $(0,b)$ dan
jari-jarinya $r$. Titik lintasan lingkaran

$$
P_2=(x_2,y_2)
$$

memenuhi syarat

$$
x_2^2+(y_2-b)^2=r^2.
$$

Jadi, seluruh sistem mekanis dideskripsikan oleh dua syarat

$$
\begin{aligned}
x_2^2+(y_2-b)^2&=r^2,\\
(x_2-x_1)^2+y_2^2&=d^2,
\end{aligned}
$$

dengan $d$ kembali menyatakan jarak kopling. Jika kedua persamaan ini ditinjau
dalam koordinat $x_2,y_2$ dan $x_2-x_1$, terlihat bahwa keduanya mendeskripsikan
irisan dua silinder, serupa dengan
[Contoh 4.6](https://de.wikiversity.org/wiki/Affine_Variet%C3%A4ten/Irreduzible_Teilmengen/Schnitt_von_zwei_gleichgro%C3%9Fen_Zylindern/Zwei_Kreise/Beispiel).
Jadi, konfigurasi batang yang diizinkan dalam sistem mekanis dapat ditafsirkan,
dalam tiga koordinat yang sesuai, sebagai irisan dua silinder. Namun,
jari-jarinya tidak harus sama dan sumbu-sumbu dalam silindernya juga tidak
harus berpotongan. Irisan semacam itu beserta trajektori-trajektori yang
bersesuaian dapat menjadi cukup rumit.

Dalam contoh-contoh berikut, kita memerlukan sebuah lema yang mendeskripsikan
suatu *situasi eliminasi* sederhana.

### [Lema: eliminasi dua persamaan kuadratik](https://de.wikiversity.org/wiki/Elimination/Zwei_quadratische_Gleichungen/Direkt/Fakt) {#br-ak-2025-2026-l08-lem-01}

Misalkan $R$ suatu
[domain integral](https://de.wikiversity.org/wiki/Kommutative_Ringtheorie/Integrit%C3%A4tsbereich/Definition),
dan misalkan

$$
F_1=a_1X^2+b_1X+c_1
\qquad\text{dan}\qquad
F_2=a_2X^2+b_2X+c_2
$$

dua polinom kuadratik dalam satu variabel di atas $R$, dengan

$$
a_1\ne0,
$$

serta $(a_1,b_1)$ dan $(a_2,b_2)$ bebas linear. Maka ideal

$$
(F_1,F_2)\cap R
$$

memuat unsur

$$
\begin{aligned}
&(a_2c_1-a_1c_2)^2\\
&\quad-b_1(-a_2c_1b_2-c_2a_2b_1+a_1b_2c_2)\\
&\quad+c_1(a_1b_2^2-2a_2b_1b_2).
\end{aligned}
$$

#### [Bukti](https://de.wikiversity.org/wiki/Elimination/Zwei_quadratische_Gleichungen/Direkt/Fakt/Beweis2) {#br-ak-2025-2026-l08-lem-01-proof}

Pertama-tama, kita mempunyai

$$
a_2F_1-a_1F_2
=(a_2b_1-a_1b_2)X+a_2c_1-a_1c_2.
$$

Dari sini diperoleh ungkapan (argumen ini tidak sepenuhnya benar, tetapi juga
dapat dilaksanakan secara lebih ketat)

$$
X=-\frac{a_2c_1-a_1c_2}{a_2b_1-a_1b_2}.
$$

Kita menyubstitusikannya ke dalam $F_1$, lalu mengalikan dengan kuadrat
penyebut, dan memperoleh

$$
\begin{aligned}
&a_1(a_2c_1-a_1c_2)^2\\
&\quad-b_1(a_2c_1-a_1c_2)(a_2b_1-a_1b_2)\\
&\quad+c_1(a_2b_1-a_1b_2)^2.
\end{aligned}
$$

Dalam suku kedua muncul $-b_1a_2c_1a_2b_1$, dan dalam suku ketiga muncul
$c_1a_2^2b_1^2$; kedua suku ini saling meniadakan. Setiap monom yang tersisa
memuat $a_1$. Jadi, kita dapat mencoret $a_1$, dan yang tersisa adalah

$$
\begin{aligned}
&(a_2c_1-a_1c_2)^2\\
&\quad-b_1(-a_2c_1b_2-c_2a_2b_1+a_1b_2c_2)\\
&\quad+c_1(a_1b_2^2-2a_2b_1b_2).
\end{aligned}
$$

$\square$

### [Contoh: lingkaran satuan dan garis singgung](https://de.wikiversity.org/wiki/Mechanisch_definierte_Kurven/Stangenkonfiguration/Kreis_und_tangentiale_Gerade/Beispiel) {#br-ak-2025-2026-l08-ex-02}

Kita meninjau sistem kopling mekanis yang didefinisikan oleh lingkaran satuan
dan garis yang menyinggungnya di $(0,1)$, dengan jarak kopling

$$
d=2.
$$

Jadi, titik lintasan garis dan titik lintasan lingkaran adalah

$$
P_1=(x_1,1)
\qquad\text{dan}\qquad
P_2=(x_2,y_2),
$$

dengan dua syarat

$$
\begin{aligned}
x_2^2+y_2^2&=1,\\
(x_2-x_1)^2+(y_2-1)^2&=4.
\end{aligned}
$$

Jadi, sistem ini merupakan irisan dua silinder, tetapi dengan jari-jari yang
berbeda dan sumbu-sumbu dalam yang tidak berpotongan. Selisih kedua
persamaannya adalah

$$
x_1^2-2x_1x_2-2y_2-2=0,
$$

dan salah satu persamaan dapat diganti dengannya. Dari sini juga terlihat
bahwa variabel $y_2$ dapat dieliminasi, sehingga diperoleh suatu sistem dengan
satu persamaan dalam dua variabel; lihat
[Soal 8.9](https://de.wikiversity.org/wiki/Mechanisch_definierte_Kurven/Stangenkonfiguration/Kreis_und_tangentiale_Gerade/Zweidimensionale_Interpretation/Aufgabe).
Sistem ini tak tereduksi; lihat
[Soal 8.10](https://de.wikiversity.org/wiki/Mechanisch_definierte_Kurven/Stangenkonfiguration/Kreis_und_tangentiale_Gerade/Irreduzibel/Aufgabe).

Dua garis berikut menarik:

$$
G_1=V(x_2,y_2+1)
$$

dan

$$
G_2=V(x_2-x_1,y_2+1).
$$

Keduanya berpotongan di titik

$$
P=(0,0,-1).
$$

Garis $G_1$ terletak pada salah satu silinder dan menyinggung silinder yang
lain, demikian pula sebaliknya. Gambaran geometrisnya adalah bahwa silinder
yang lebih kecil melubangi silinder yang lebih besar dan menghasilkan suatu
“angka delapan melengkung”, dengan $P$ sebagai titik persilangan angka delapan
itu.

![Irisan dua silinder](authority/assets/Intersection_of_cylinders.jpg)

Konfigurasi batang yang diizinkan dapat diperoleh sebagai berikut. Untuk
setiap titik lingkaran, terdapat dua kemungkinan posisi batang, kecuali untuk
titik lintasan lingkaran $(0,-1)$, ketika titik lintasan garis haruslah
$(0,1)$.

Kita mulai dengan situasi ketika $(0,1)$ adalah titik lintasan lingkaran dan
$(-2,1)$ adalah titik lintasan garis (jadi, batang terletak ke kiri pada
garis), lalu membiarkan titik lintasan lingkaran bergerak mengelilingi
lingkaran searah jarum jam. Titik lintasan lingkaran kemudian menarik titik
lintasan garis di belakangnya sampai tiba di bawah, pada $(0,-1)$. Batang
kemudian menjadi diameter vertikal lingkaran (titik lintasan garis berada di
$(0,1)$ dan titik lintasan lingkaran tepat di bawah). Sesudah itu, titik
lintasan lingkaran bergerak naik pada busur kiri lingkaran sambil mendorong
batang lebih jauh ke kanan, sampai titik lintasan garis tiba di $(2,1)$.

Kemungkinan lain ketika $(0,1)$ adalah titik lintasan lingkaran ialah batang
terletak ke kanan pada garis (dengan $(2,1)$ sebagai titik lintasan garis).
Titik lintasan lingkaran kembali bergerak searah jarum jam. Mula-mula, titik
itu mendorong titik lintasan garis ke kanan sampai suatu posisi ekstrem,
ketika batang tegak lurus terhadap lingkaran di titik lintasan lingkaran.
Sesudah itu, titik lintasan lingkaran menarik titik lintasan garis kembali ke
kiri, sementara batang menegak, sampai batang menempati diameter vertikal
lingkaran. Selanjutnya, titik lintasan lingkaran kembali bergerak naik pada
busur kiri lingkaran, sambil mendorong titik lintasan garis ke kiri sampai
posisi ekstrem, lalu pada bagian terakhir kembali menariknya ke $(-2,1)$.

Khususnya, diameter vertikal lingkaran ditempati dua kali oleh batang; jadi,
konfigurasi batang ini bersesuaian dengan titik persilangan angka delapan.

Sekarang kita hendak menghitung trajektori titik tengah batang, yaitu

$$
\begin{aligned}
P
&=P_1+\frac12(P_2-P_1)\\
&=(x_1,1)+\frac12(x_2-x_1,y_2-1)\\
&=\left(\frac12x_1+\frac12x_2,\frac12y_2+\frac12\right)\\
&\mathrel{:=}(x,y).
\end{aligned}
$$

Kita mencari suatu persamaan bagi $x$ dan $y$, dan memperkenalkan variabel

$$
z=\frac12x_1-\frac12x_2.
$$

Maka

$$
x_1=x+z,\qquad x_2=x-z,\qquad y_2=2y-1,
$$

dan sistem persamaan dalam variabel-variabel baru menjadi

$$
(x-z)^2+(2y-1)^2=1
\qquad\text{dan}\qquad
(-2z)^2+(2y-2)^2=4.
$$

Persamaan kedua dapat ditulis sebagai

$$
z^2+(y-1)^2=1,
$$

atau sebagai

$$
z^2+y^2-2y=0.
$$

Setelah dikembangkan, persamaan pertama menjadi

$$
z^2-2zx+x^2+4y^2-4y=0.
$$

Menurut [Lema 8.4](#br-ak-2025-2026-l08-lem-01), dengan

$$
R=\mathbb R[x,y]
$$

dan variabel tambahan $z$ (jadi, $a_1=a_2=1$ dan $b_1=0$), diperoleh
persamaan

$$
\begin{aligned}
(c_1-c_2)^2+c_1b_2^2
&=(y^2-2y-x^2-4y^2+4y)^2+(y^2-2y)(2x)^2\\
&=(-3y^2+2y-x^2)^2+(y^2-2y)(2x)^2\\
&=9y^4+x^4+4y^2-12y^3+6x^2y^2-4x^2y\\
&\qquad+4x^2y^2-8x^2y\\
&=9y^4+10x^2y^2+x^4-12y^3-12x^2y+4y^2.
\end{aligned}
$$

Ini adalah suatu kuartik (kurva berderajat empat) dengan dua singularitas.

![Gambar untuk latihan](authority/assets/Alg_Kurven_OS2008_Lsg8.10_v2.png)

### [Contoh: jari-jari sama dengan jarak kopling](https://de.wikiversity.org/wiki/Mechanische_ebene_Kurven/Stangenkoppelung/Gerade_und_Kreis/Radius_ist_Koppelungsabstand/Beispiel) {#br-ak-2025-2026-l08-ex-03}

Kita meninjau sistem mekanis yang terdiri atas lingkaran satuan dan sumbu
$x$, dengan jarak kopling

$$
d=1.
$$

Sistem mekanis itu dideskripsikan oleh dua persamaan

$$
\begin{aligned}
x_2^2+y_2^2&=1,\\
(x_2-x_1)^2+y_2^2&=1.
\end{aligned}
$$

Ini merupakan irisan dua silinder dengan jari-jari yang sama dan sumbu-sumbu
dalam yang berpotongan; jadi, kita dapat menggunakan hasil
[Contoh 4.6](https://de.wikiversity.org/wiki/Affine_Variet%C3%A4ten/Irreduzible_Teilmengen/Schnitt_von_zwei_gleichgro%C3%9Fen_Zylindern/Zwei_Kreise/Beispiel).
Di sana telah ditunjukkan bahwa irisan tersebut diberikan oleh dua elips yang
berpotongan di dua titik. Deskripsi ini juga harus muncul kembali dalam
konteks sistem mekanis. Konfigurasi batang manakah yang bersesuaian dengan
elips pertama, konfigurasi manakah yang bersesuaian dengan elips kedua, dan
konfigurasi manakah yang terletak pada keduanya?

Mari kita tinjau seluruh konfigurasi yang diizinkan. Jika titik garis (yakni
titik pada lintasan garis) adalah pusat lingkaran, setiap titik lingkaran
diizinkan sebagai titik lintasan lingkaran. Jadi, sinar-sinar radial lingkaran
membentuk suatu keluarga konfigurasi batang yang diizinkan, dan bersama-sama
mereka membentuk salah satu elips. Elips yang lain bersesuaian dengan himpunan
konfigurasi batang ketika titik lintasan garis bergerak dari $-2$ ke $+2$,
sambil mendorong titik lintasan lingkaran di depannya atau menariknya di
belakangnya pada busur atas atau busur bawah lingkaran. Ada dua konfigurasi
batang yang termasuk dalam kedua keluarga, yaitu konfigurasi dengan pusat
lingkaran sebagai titik lintasan garis dan $(0,1)$ atau $(0,-1)$ sebagai titik
lintasan lingkaran. Dalam konfigurasi batang seperti itu, sistem mekanis tidak
hanya dapat bergerak maju dan mundur, tetapi juga dapat mengubah arah secara
esensial.

Seperti apakah trajektori suatu titik pada batang bergerak? Trajektori totalnya
adalah gabungan kedua trajektori yang bersesuaian dengan kedua komponen tak
tereduksi sistem. Berapa banyak titik penembusan diri yang ada?

Untuk suatu titik

$$
P=P_1+u(P_2-P_1)
$$

pada batang kopling, koordinatnya adalah

$$
(z_1,z_2)=(x_1+u(x_2-x_1),uy_2).
$$

Untuk $u=0$, trajektorinya adalah interval real $[-2,2]$, dan untuk $u=1$,
trajektorinya adalah lingkaran satuan. Jadi, sekarang misalkan

$$
u\ne0,1.
$$

Proyeksi komponen-komponen radial sistem hanyalah lingkaran berjari-jari $u$.
Proyeksi elips yang lain kembali merupakan sebuah elips yang dapat memotong
lingkaran tersebut dengan berbagai cara. Lihat juga
[Soal 8.23](https://de.wikiversity.org/wiki/Schnitt_von_zwei_Zylindern/Projektion_auf_Fl%C3%A4chen/Charakterisierung_der_Bilder/Aufgabe).
