---
title: "Kuliah 7 - Irisan Kerucut dan Kuadrik"
stable_id: br-ak-2025-2026-l07
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 7"
upstream_pageid: 165896
upstream_revid: 1057689
upstream_timestamp: "2025-11-04T10:20:33Z"
upstream_mediawiki_sha1: 482eacab21b84870389c23a5faac8493768fd522
source_url: "https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)/Vorlesung_7?oldid=1057689"
license: "CC BY-SA 4.0 for translated course text; media retain component rights in authority/RIGHTS-unit-07.csv"
translation_status: complete
---

# Kuliah 7: Irisan Kerucut dan Kuadrik {#br-ak-2025-2026-l07}

## Irisan kerucut dan kuadrik {#br-ak-2025-2026-l07-s01}

![Kerucut standar](authority/assets/DoubleCone.png)

*Kerucut standar* dalam ruang afin berdimensi tiga diberikan oleh persamaan
homogen

$$
Z^2=X^2+Y^2.
$$

Hal ini dapat dibayangkan dengan menganggap bahwa $z$ menentukan jari-jari
suatu lingkaran yang terletak pada bidang sejajar bidang $x$-$y$ dan melalui
titik $(0,0,z)$. Setiap irisan kerucut ini dengan suatu bidang afin $E$
disebut *irisan kerucut*.

![Irisan-irisan kerucut standar dengan bidang-bidang afin](authority/assets/Conic_sections.svg)

### [Definisi: irisan kerucut](https://de.wikiversity.org/wiki/Algebraische_Kurven/Kegelschnitt_mit_Standardkegel/Definition) {#br-ak-2025-2026-l07-def-01}

Suatu *irisan kerucut* $C$ adalah irisan kerucut standar
$V(Z^2-X^2-Y^2)$ dengan suatu bidang afin
$V(aX+bY+cZ+d)$, dengan $a,b,c$ tidak semuanya nol; jadi,

$$
C=V(Z^2-X^2-Y^2)\cap V(aX+bY+cZ+d).
$$

Teori irisan kerucut merupakan topik klasik yang telah dibahas dalam sebuah
karya oleh [Apollonios dari Perga](https://de.wikipedia.org/wiki/Apollonios_von_Perge).
Karena bidang itu diberikan oleh persamaan

$$
aX+bY+cZ+d=0,
$$

kita dapat menyelesaikannya secara linear terhadap salah satu variabel dan
memperoleh persamaan baru dalam dua variabel bagi irisan kerucut tersebut.
Ini merupakan substitusi variabel afin-linear, sehingga persamaan baru itu
juga berderajat dua.

Oleh karena itu, kita meninjau *kuadrik afin* dalam dua variabel secara umum.

### [Definisi: kuadrik dalam dua variabel](https://de.wikiversity.org/wiki/Ebene_algebraische_Kurven/Quadrik_in_zwei_Variablen/Polynom_und_Nullstelle/Definition) {#br-ak-2025-2026-l07-def-02}

Suatu polinom berbentuk

$$
F=\alpha X^2+\beta XY+\gamma Y^2+\delta X+\epsilon Y+\eta,
\qquad
\alpha,\beta,\gamma,\delta,\epsilon,\eta\in K,
$$

dengan sekurang-kurangnya satu di antara koefisien
$\alpha,\beta,\gamma$ tidak nol, disebut *bentuk kuadratik dalam dua variabel*
(di atas $K$), atau *kuadrik dalam dua variabel*. Lokus nol yang bersesuaian

$$
V(F)\subseteq\mathbb A_K^2
$$

juga disebut *kuadrik*.

Kita ingin mengetahui berapa banyak tipe kuadrik yang berbeda. Jawabannya
bergantung pada lapangan dasar. Selain itu, kita harus menentukan konsep
ekuivalensi mana yang hendak digunakan. Untuk dua kuadrik

$$
F,G\in K[X,Y],
$$

konsep-konsep ekuivalensi berikut layak dipelajari.

1. $F$ dan $G$, sebagai polinom, *ekuivalen secara afin*: terdapat suatu
   transformasi variabel afin-linear (bijektif)

   $$
   \begin{aligned}
   \varphi:K[X,Y]&\longrightarrow K[X,Y],\\
   X&\longmapsto rX+sY+t,\\
   Y&\longmapsto \widetilde rX+\widetilde sY+\widetilde t,
   \end{aligned}
   $$

   sedemikian sehingga $G=\varphi(F)$.

2. Ideal-ideal utama $(F)$ dan $(G)$ *ekuivalen secara afin*: terdapat suatu
   transformasi variabel afin-linear (bijektif) $\varphi$ sedemikian sehingga

   $$
   (G)=(\varphi(F)).
   $$

3. Gelanggang-gelanggang faktor

   $$
   K[X,Y]/(F)\qquad\text{dan}\qquad K[X,Y]/(G)
   $$

   isomorfik sebagai
   [$K$-aljabar](https://de.wikiversity.org/wiki/Kommutative_Ringtheorie/Algebra/Ringhomomorphismus/Definition).

4. Lokus-lokus nol $V(F)$ dan $V(G)$
   [ekuivalen secara afin-linear](https://de.wikiversity.org/wiki/Affin-algebraische_Mengen/Affin-linear_%C3%A4quivalent/Definition).

Konsep ekuivalensi pertama lebih kuat daripada yang kedua, dan yang kedua
lebih kuat daripada kedua konsep terakhir. Perbedaan penting antara (1) dan
(2) ialah bahwa pada (2) kita selalu boleh mengalikan dengan suatu satuan
(hal ini juga tidak mengubah lokus nol). Di atas lapangan yang tidak tertutup
secara aljabar, ekuivalensi dalam (4) dapat menjadi sangat kasar, sebab semua
$F$ dengan lokus nol kosong ekuivalen dalam pengertian (4).

Untuk $K=\mathbb R$ dan $K=\mathbb C$, kita juga tertarik pada kesesuaian
sifat-sifat topologis dari lokus-lokus nol yang bersesuaian. Di sini kita akan
meninjau berbagai konsep ekuivalensi bagi dua kuadrik $F$ dan $G$ secara
paralel, tetapi perhatian utama kita tertuju pada (2).

### [Lema: reduksi pertama kuadrik afin](https://de.wikiversity.org/wiki/Affine_Quadriken_in_zwei_Variablen/Erste_Reduktion/Fakt) {#br-ak-2025-2026-l07-lem-01}

Misalkan $K$ suatu
[lapangan](https://de.wikiversity.org/wiki/K%C3%B6rpertheorie_%28Algebra%29/K%C3%B6rper/Direkt/Definition)
dengan
[karakteristik](https://de.wikiversity.org/wiki/K%C3%B6rpertheorie_%28Algebra%29/Charakteristik/1/Definition)
$\ne2$, dan misalkan

$$
F=\alpha X^2+\beta XY+\gamma Y^2+\delta X+\epsilon Y+\eta
$$

suatu kuadrik. Maka terdapat suatu
[transformasi variabel](https://de.wikiversity.org/wiki/Affiner_Raum/Lineare_Variablentransformation/Definition)
pada bidang afin sedemikian sehingga polinom yang ditransformasikan, dalam
variabel-variabel baru, berbentuk

$$
G=\gamma Y^2+H(X),
\qquad
H(X)=aX^2+bX+c,
$$

dengan $\gamma\ne0$. Jika $a\ne0$, kita dapat mencapai $b=0$.

Di atas suatu
[lapangan tertutup secara aljabar](https://de.wikiversity.org/wiki/K%C3%B6rpertheorie_%28Algebra%29/Algebraisch_abgeschlossen/Definition),
kita dapat mencapai $\gamma=1$ melalui suatu transformasi variabel.

Jika yang diperhatikan adalah ideal yang dibangkitkan atau lokus nolnya, kita
juga dapat mencapai $\gamma=1$ melalui pembagian.

#### [Bukti](https://de.wikiversity.org/wiki/Affine_Quadriken_in_zwei_Variablen/Erste_Reduktion/Fakt/Beweis) {#br-ak-2025-2026-l07-lem-01-proof}

Pertama-tama kita mereduksi ke kasus $\gamma\ne0$. Jika $\gamma=0$ dan
$\alpha\ne0$, kita dapat mempertukarkan $X$ dan $Y$. Jika
$\alpha=\gamma=0$, haruslah $\beta\ne0$. Dalam hal ini, melalui

$$
X\longmapsto X+Y,
\qquad
Y\longmapsto Y,
$$

kita dapat membuat koefisien $Y^2$ menjadi tidak nol. Jadi, selanjutnya kita
mengandaikan bahwa $\gamma\ne0$.

Kita menulis polinom itu sebagai

$$
\gamma Y^2+(\beta X+\epsilon)Y+\widetilde H(X),
$$

dengan $\widetilde H$ suatu polinom dalam $X$ berderajat $\le2$. Dengan
melengkapkan kuadrat, ungkapan ini dapat ditulis sebagai

$$
\gamma\left(Y+\frac{\beta X+\epsilon}{2\gamma}\right)^2
+\widetilde H(X)-\frac{(\beta X+\epsilon)^2}{4\gamma}.
$$

Dalam variabel-variabel baru

$$
Y+\frac{\beta X+\epsilon}{2\gamma}
\qquad\text{dan}\qquad
X,
$$

persamaan tersebut berbentuk

$$
G=\gamma Y^2+H(X),
\qquad
H(X)=aX^2+bX+c.
$$

Jika $K$ tertutup secara aljabar, $\gamma$ mempunyai akar kuadrat, sehingga
melalui $Y\mapsto Y/\sqrt\gamma$ koefisien itu dapat dibuat menjadi $1$.
Pernyataan tambahan yang lain jelas. $\square$

## Klasifikasi kuadrik real dan kompleks {#br-ak-2025-2026-l07-s02}

### [Contoh: klasifikasi kuadrik real](https://de.wikiversity.org/wiki/Affine_Quadriken_in_zwei_Variablen/Reell/Klassifizierung/Beispiel) {#br-ak-2025-2026-l07-ex-01}

Misalkan $K=\mathbb R$. Kita ingin mengklasifikasikan kuadrik-kuadrik real,
terutama berkenaan dengan ekuivalensi afin-linear dari ideal-ideal utama yang
dibangkitkannya. Dengan kata lain, kita boleh melakukan transformasi variabel
afin dan membagi dengan $-1$. Berdasarkan [Lema 7.3](#br-ak-2025-2026-l07-lem-01),
kita dapat mengandaikan bahwa persamaan yang mendeskripsikannya berbentuk

$$
Y^2=aX^2+bX+c.
$$

Jika $a=b=0$, melalui transformasi $Y\mapsto\sqrt cY$ untuk $c>0$, atau
$Y\mapsto\sqrt{-c}Y$ untuk $c<0$, lalu membagi dengan $\pm c$, kita dapat
membuat ruas kanan menjadi $1$, $-1$, atau $0$.

Jika $a=0$ dan $b\ne0$, kita dapat mengambil $bX+c$ sebagai variabel baru dan
memperoleh persamaan

$$
Y^2=X.
$$

Sekarang misalkan $a\ne0$. Melalui transformasi
$X\mapsto X/\sqrt a$ atau $X\mapsto X/\sqrt{-a}$, kita dapat mencapai
$a=\pm1$. Dengan melengkapkan kuadrat, kita dapat membuat $b=0$. Jika $c=0$,
kita dapat mentransformasikan persamaan itu menjadi

$$
Y^2=\pm X^2.
$$

Jadi, misalkan $c\ne0$. Melalui transformasi serentak

$$
X\longmapsto uX,
\qquad
Y\longmapsto uY,
\qquad
u=\sqrt{\pm c},
$$

dan pembagian setelahnya, kita dapat mencapai $c=\pm1$. Dengan demikian,
kemungkinan yang masih harus ditinjau adalah

$$
Y^2=\pm X^2\pm1,
$$

dengan kedua persamaan

$$
Y^2-X^2=\pm1
$$

saling ekuivalen.

Jadi, kita mengetahui bahwa setiap kuadrik real dapat dibawa ke salah satu
dari sembilan bentuk berikut.

I. $Y^2=0$. Ini adalah suatu *garis rangkap*.

II. $Y^2=1$. Ini berarti $Y=\pm1$, jadi merupakan *dua garis sejajar*.

III. $Y^2=-1$. Lokus ini *kosong*.

IV. $Y^2=X$. Ini adalah suatu *parabola*.

V. $Y^2=X^2$. Ini berarti $(Y-X)(Y+X)=0$, jadi merupakan *dua garis yang
berpotongan*.

VI. $Y^2=-X^2$. Satu-satunya solusi adalah *titik* $(0,0)$.

VII. $Y^2=X^2+1$. Ini berarti $(Y-X)(Y+X)=1$, jadi merupakan suatu
*hiperbola*.

VIII. $Y^2=-X^2+1$. Ini adalah suatu *lingkaran satuan*.

IX. $Y^2=-X^2-1$. Lokus ini kembali *kosong*.

Apakah kesembilan tipe ini semuanya saling berbeda? Jawabannya bergantung pada
konsep ekuivalensi yang digunakan. Tipe III dan IX keduanya kosong, sehingga
mempunyai lokus nol yang identik. Di sisi lain, gelanggang-gelanggang hasil
bagi yang bersesuaian

$$
\mathbb R[X,Y]/(Y^2+1)
\qquad\text{dan}\qquad
\mathbb R[X,Y]/(X^2+Y^2+1)
$$

tidak isomorfik, dan di atas bilangan kompleks lokus-lokus nolnya tidak sama.
Karena itu, di sini keduanya juga dipandang berbeda. Selain itu, lokus-lokus
nol tersebut pada umumnya sudah berbeda karena alasan topologis. Sebagai
contoh, lingkaran satuan
[kompak](https://de.wikiversity.org/wiki/Topologie/Grundbegriffe/Kompaktheit/%C3%9Cberdeckungskompakt/Definition),
hiperbola tidak kompak dan mempunyai dua komponen terhubung, sedangkan
parabola tidak kompak dan mempunyai satu komponen terhubung, dan seterusnya.

Namun, garis rangkap dan parabola sama secara topologis-real, demikian pula
hiperbola dan kedua garis sejajar. Dalam tiap pasangan ini, gelanggang hasil
baginya berbeda; pada pasangan kedua, versi kompleksnya juga berbeda. Sebagai
contoh, $K[X,Y]/(Y^2)$ bukan gelanggang tereduksi, sedangkan

$$
K[X,Y]/(Y^2-X)\cong K[Y]
$$

merupakan domain integral. Hiperbola kompleks terhubung karena isomorfik
dengan

$$
\mathbb C^\times=\mathbb C\setminus\{0\},
$$

yakni dengan garis kompleks tertusuk
$\mathbb A_{\mathbb C}^1\setminus\{0\}$.

Gambar-gambar berikut menunjukkan rotasi dan translasi suatu kuadrik.

![Tahap pertama transformasi sumbu utama suatu kuadrik](authority/assets/Hauptachsentransformation1.png)

![Tahap kedua transformasi sumbu utama suatu kuadrik](authority/assets/Hauptachsentransformation2.png)

![Tahap ketiga transformasi sumbu utama suatu kuadrik](authority/assets/Hauptachsentransformation3.png)

### [Contoh: klasifikasi kuadrik kompleks](https://de.wikiversity.org/wiki/Affine_Quadriken_in_zwei_Variablen/Komplex/Klassifizierung/Beispiel) {#br-ak-2025-2026-l07-ex-02}

Misalkan $K=\mathbb C$. Kita ingin mengklasifikasikan kuadrik-kuadrik kompleks.
Berdasarkan [Lema 7.3](#br-ak-2025-2026-l07-lem-01), kita dapat mengandaikan
bahwa persamaan yang mendeskripsikannya berbentuk

$$
Y^2=aX^2+bX+c.
$$

Jika $a=b=0$ dan $c=0$, kita mempertahankan persamaan $Y^2=0$. Jika
$a=b=0$ dan $c\ne0$, melalui penskalaan variabel $Y$ dan pembagian dengan
konstanta tak nol, kita dapat membuat persamaannya menjadi $Y^2=1$.

Jika $a=0$ dan $b\ne0$, kita dapat mengambil $bX+c$ sebagai variabel baru dan
memperoleh persamaan

$$
Y^2=X.
$$

Sekarang misalkan $a\ne0$. Melalui transformasi
$X\mapsto X/\sqrt a$, kita dapat mencapai $a=1$. Dengan melengkapkan kuadrat,
kita dapat membuat $b=0$. Akhirnya, melalui transformasi serentak
$X\mapsto uX$, $Y\mapsto uY$, lalu melakukan pembagian, kita dapat mencapai
$c=1$ apabila $c\ne0$; apabila $c=0$, bentuk $Y^2=X^2$ dipertahankan.

> **Catatan edisi:** Pada kedua langkah normalisasi di atas, sumber memakai
> penskalaan atau pembagian yang memerlukan $c\ne0$ tanpa memisahkan kasus
> $c=0$. Edisi ini memisahkannya secara eksplisit: $c=0$ menghasilkan bentuk I
> ketika $a=b=0$, dan bentuk IV, $Y^2=X^2$, ketika $a\ne0$.

Jadi, kita mengetahui bahwa setiap kuadrik kompleks dapat dibawa ke salah satu
dari lima bentuk berikut.

I. $Y^2=0$. Ini adalah suatu *garis rangkap*.

II. $Y^2=1$. Ini berarti $Y=\pm1$, jadi merupakan *dua garis kompleks
sejajar*.

III. $Y^2=X$. Ini adalah suatu *parabola kompleks*.

IV. $Y^2=X^2$. Ini berarti $(Y-X)(Y+X)=0$, jadi merupakan *dua garis
kompleks* yang berpotongan di satu titik.

V. $Y^2=X^2+1$. Ini berarti $(Y-X)(Y+X)=1$, jadi merupakan suatu *hiperbola
kompleks*.

Ditinjau secara topologis-kompleks, Tipe I dan Tipe III merupakan suatu garis
afin kompleks, jadi suatu bidang real, dan dengan demikian keduanya sama
secara topologis. Menyebutnya “bidang kompleks” berbahaya dalam konteks
geometri aljabar, sebab istilah itu dapat berarti $\mathbb C$ atau
$\mathbb C^2$. Akan tetapi, gelanggang-gelanggang faktornya berbeda,
sehingga keduanya dicantumkan sebagai tipe yang berbeda. Selain itu, semua
tipe saling berbeda secara topologis-kompleks. Di samping bidang real, kita
mempunyai garis afin kompleks tertusuk (hiperbola, yang secara topologis
merupakan bidang real tertusuk), dua garis yang saling lepas, dan dua garis
yang berpotongan di satu titik.

Klasifikasi kuadrik kompleks yang disajikan dalam contoh terakhir berlaku di
atas setiap lapangan tertutup secara aljabar yang berkarakteristik $\ne2$.

## Parametrisasi kuadrik {#br-ak-2025-2026-l07-s03}

Dalam teori bilangan elementer, kita mempelajari cara mendapatkan semua tripel
Pythagoras secara sistematis. Alasannya adalah bahwa lingkaran satuan mempunyai
parametrisasi oleh fungsi-fungsi rasional. Sekarang, sebagai generalisasi dari
[Soal 1.28](https://de.wikiversity.org/wiki/Einheitskreis/Rationale_Parametrisierung/Funktionaler_Ausdruck/Aufgabe),
kita menunjukkan bahwa setiap kuadrik tak tereduksi dapat diparameterkan
secara rasional.

### [Teorema: parametrisasi rasional kuadrik](https://de.wikiversity.org/wiki/Quadrik_in_zwei_Variablen/Rationale_Parametrisierung/Fakt) {#br-ak-2025-2026-l07-thm-01}

Misalkan

$$
C=V(F)
$$

suatu kuadrik dalam dua variabel, yakni

$$
F=\alpha X^2+\beta XY+\gamma Y^2+\delta X+\epsilon Y+\eta,
$$

dengan $\alpha,\beta,\gamma$ tidak semuanya nol. Andaikan sekurang-kurangnya
terdapat satu titik pada kuadrik tersebut. Maka terdapat polinom-polinom

$$
P_1,P_2,Q\in K[T],
\qquad
Q\ne0,
$$

sedemikian sehingga citra pemetaan rasional

$$
\begin{aligned}
\mathbb A_K^1\supseteq D(Q)&\longrightarrow\mathbb A_K^2,\\
t&\longmapsto
\left(\frac{P_1(t)}{Q(t)},\frac{P_2(t)}{Q(t)}\right)
\end{aligned}
$$

terletak dalam $C$.

Jika $C$ mempunyai sekurang-kurangnya dua titik, pemetaan tersebut tidak
konstan dan injektif kecuali untuk berhingga banyak pengecualian.

Jika, selain itu, $C$
[tak tereduksi](https://de.wikiversity.org/wiki/Affine_Variet%C3%A4ten/Affin-algebraische_Mengen/Irreduzibel/Definition),
pemetaan tersebut surjektif kecuali untuk berhingga banyak pengecualian.
Khususnya, suatu kuadrik tak tereduksi dengan sekurang-kurangnya dua titik
merupakan suatu
[kurva rasional](https://de.wikiversity.org/wiki/Ebene_algebraische_Kurven/Rationale_Kurve/Definition).

#### [Bukti](https://de.wikiversity.org/wiki/Quadrik_in_zwei_Variablen/Rationale_Parametrisierung/Fakt/Beweis) {#br-ak-2025-2026-l07-thm-01-proof}

Melalui suatu transformasi variabel, kita dapat mencapai $\alpha\ne0$. Lalu
kita dapat membagi dengan $\alpha$ dan mengandaikan bahwa $\alpha=1$. Melalui
translasi, kita dapat mengandaikan bahwa titik asal $0=(0,0)$ terletak pada
kurva. Maka $\eta=0$. Jika kuadrik itu terdiri atas dua garis yang berpotongan,
kita dapat melakukan translasi agar titik asal bukan titik perpotongannya
(tetapi tetap terletak pada salah satu garis).

Gagasannya adalah, untuk suatu titik

$$
H=(t,1),
$$

kita meninjau garis yang melalui $0$ dan $H$, lalu meninjau irisan garis ini
dengan $C$. Irisan tersebut terdiri atas paling banyak dua titik (kecuali jika
irisannya adalah seluruh garis). Karena $0$ merupakan salah satu titik itu,
titik lain yang harus ada ditentukan secara tunggal.

Jadi, misalkan $H=(t,1)$ diberikan. Garis melalui $H$ dan $0$ terdiri atas
semua titik

$$
(at,a),
\qquad
a\in K.
$$

Titik-titik irisannya dengan $C$ diperoleh dengan menyubstitusikan
$(x,y)=(at,a)$ ke dalam $F$ dan mencari solusi-solusinya terhadap $a$.
Substitusi memberikan syarat

$$
F(at,a)=(at)^2+\beta(at\,a)+\gamma a^2+\delta at+\epsilon a.
$$

Solusi $a=0$ bersesuaian dengan titik asal yang sudah kita ketahui. Solusi
kedua adalah

$$
a_2=\frac{-\delta t-\epsilon}{t^2+\beta t+\gamma}.
$$

Ungkapan ini terdefinisi jika

$$
Q(t)=t^2+\beta t+\gamma\ne0,
$$

yang mengecualikan paling banyak dua nilai $t$. Titik pada $C$ yang
bersesuaian dengan $a_2$ adalah

$$
\begin{aligned}
a_2(t,1)
&=(a_2t,a_2)\\
&=\left(
t\frac{-\delta t-\epsilon}{t^2+\beta t+\gamma},
\frac{-\delta t-\epsilon}{t^2+\beta t+\gamma}
\right).
\end{aligned}
$$

Karena itu, kita harus menetapkan

$$
P_1=-t(\delta t+\epsilon),
\qquad
P_2=-\delta t-\epsilon.
$$

Pemetaan ini terdefinisi dengan baik pada himpunan terbuka Zariski $D(Q)$
(dan himpunan ini tidak kosong segera setelah lapangan tersebut mempunyai
sekurang-kurangnya tiga elemen).

Mulai sekarang, andaikan $C$ mempunyai sekurang-kurangnya dua titik. Jika
$\delta=\epsilon=0$, maka $F$ berbentuk

$$
F=X^2+\beta XY+\gamma Y^2.
$$

Karena kita mengandaikan bahwa terdapat sekurang-kurangnya dua titik pada
$C$, maka $F$ merupakan hasil kali dua bentuk linear homogen (yang ternormalkan
terhadap $X$). Jika $F$ merupakan kuadrat suatu bentuk linear, secara
geometris kita hanya mempunyai suatu “garis rangkap”, yang dapat langsung
diparameterkan secara bijektif. Jika tidak, $F$ merupakan hasil kali dua
bentuk linear homogen yang berbeda dan kedua garis yang bersesuaian melalui
titik asal, sesuatu yang telah kita kecualikan. Jadi, dalam kasus ini
$\delta$ dan $\epsilon$ tidak mungkin keduanya sama dengan $0$.

Dengan demikian, kita hanya perlu meninjau situasi ketika
$\delta t+\epsilon$ bukan polinom nol. Dari sini, pemetaan pada domain
definisinya injektif kecuali untuk berhingga banyak pengecualian, sebab jika
$\delta t+\epsilon\ne0$, prapeta $t$ dapat direkonstruksi dari citranya
melalui

$$
t=\frac{P_1}{Q}\cdot\frac{Q}{P_2}.
$$

Untuk menunjukkan bahwa pemetaan tersebut surjektif kecuali untuk berhingga
banyak pengecualian, kita memerlukan asumsi bahwa $C$ tak tereduksi. Secara
khusus, ini berarti bahwa $C$ bukan gabungan dua garis. Misalkan $P\in C$ dan
koordinat-$y$ dari $P$ tidak nol (paling banyak terdapat dua titik dengan
koordinat-$y$ nol). Maka garis melalui $P$ dan $0$ mempunyai titik potong

$$
H=(t,1)
$$

dengan garis parametrisasi $V(Y-1)$. Kecuali untuk berhingga banyak nilai $t$,
pemetaan tersebut terdefinisi di titik $H$ ini dan $P$ kemudian merupakan
titik citra pemetaan. Karena ketaktereduksian, hanya berhingga banyak titik
$C$ yang terletak pada garis-garis pengecualian; karena itu, hampir semua
titik tercapai. $\square$

![Potret seorang pria tak dikenal, dahulu disalahidentifikasi sebagai Johannes Kepler](authority/assets/Portrait_Confused_With_Johannes_Kepler_1610.jpg)

> **Catatan penerjemah:** Sumber beku menampilkan berkas
> `Johannes Kepler 1610.jpg` dengan keterangan bahwa sosoknya adalah Kepler.
> Berkas Commons yang tersedia kini berjudul
> `Portrait Confused With Johannes Kepler 1610.jpg` dan mengidentifikasi
> sosok tersebut sebagai seorang pria tak dikenal yang dahulu
> disalahidentifikasi sebagai Kepler. Nama dan keterangan aset lokal telah
> disesuaikan secara transparan.

Irisan-irisan kerucut (yang bebas singularitas) juga merupakan lintasan gerak
benda-benda langit. Kemungkinan lintasan benda langit pertama kali
dideskripsikan oleh [Johannes Kepler](https://de.wikipedia.org/wiki/Johannes_Kepler).
Hukum yang mendasarinya menyatakan bahwa pada setiap saat, percepatan
sebanding dengan gaya gravitasi antara titik massa pusat (bintang, Matahari)
dan titik massa yang bergerak (planet, komet). Gaya tarik itu sendiri
bergantung pada kedua massa dan kuadrat jarak di antara keduanya. Terdapat
lintasan “terikat” (elips) dan lintasan “tak terikat” (parabola, hiperbola).

Lingkaran dan elips dapat saling diubah melalui suatu transformasi variabel
linear. Perhatikan bahwa parametrisasi rasional bukanlah “parametrisasi
fisika”. Parametrisasi fisika benar-benar mendeskripsikan proses gerak: di
sana parameternya adalah waktu dan turunan pada suatu saat merupakan kecepatan
sesaat. Parametrisasi rasional “hanya” mendeskripsikan lintasan. Seperti
diketahui, lingkaran dilintasi secara seragam (dengan besar kecepatan konstan)
oleh

$$
(x,y)=(\cos t,\sin t).
$$

![Orbit eliptik](authority/assets/Elliptic_orbit.gif)

![Orbit parabola](authority/assets/Parabolic_orbit.gif)

![Orbit hiperbola](authority/assets/Hyperbolic_orbit.gif)

### [Catatan: domain parametrisasi kuadrik](https://de.wikiversity.org/wiki/Quadrik_in_zwei_Variablen/Rationale_Parametrisierung/Bemerkung) {#br-ak-2025-2026-l07-rem-01}

Parametrisasi suatu kuadrik tidak bergantung pada lapangan dasar, sebab suku-suku
yang mendefinisikan pemetaan selalu sama. Akan tetapi, di atas lapangan berhingga,
domain definisi suatu pemetaan rasional dapat kosong. Namun, jika kita beralih
ke suatu lapangan berhingga yang lebih besar $\mathbb F_q$, pemetaan tersebut
selalu mempunyai domain definisi yang tidak kosong.

Secara geometris, lubang-lubang definisi dalam parametrisasi timbul karena
garis-garis penghubung yang dikonstruksi dalam bukti
[Teorema 7.6](#br-ak-2025-2026-l07-thm-01), selain titik asal, tidak mempunyai
titik potong lain dengan kuadrik; atau sebaliknya, seluruh garis itu terletak
pada kuadrik (hal ini hanya mungkin dalam kasus tereduksi atau pada suatu garis
rangkap). Himpunan pengecualian berupa titik-titik kuadrik yang tidak berada
dalam citra pemetaan adalah titik-titik pada sumbu $x$ (khususnya titik asal),
dan, dalam kasus tereduksi, titik-titik pada garis yang seluruhnya terletak
pada kuadrik dan melalui titik asal.
