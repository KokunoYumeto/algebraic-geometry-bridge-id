---
title: "Lembar Kerja 5 - Komponen Homogen, Normalisasi Noether, dan Pemetaan Polinomial"
stable_id: br-ak-2025-2026-w05
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Arbeitsblatt 5"
upstream_pageid: 165924
upstream_revid: 1062652
upstream_timestamp: "2025-12-19T11:50:54Z"
upstream_mediawiki_sha1: 23ae014ac445f9189e80c6d48007971cd596c227
source_url: "https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)/Arbeitsblatt_5?oldid=1062652"
license: CC BY-SA 4.0
translation_status: complete
---

# Lembar Kerja 5 {#br-ak-2025-2026-w05}

## Soal latihan {#br-ak-2025-2026-w05-practice}

### Soal 5.1 {#br-ak-2025-2026-w05-ex-01}

<!-- upstream_entity: Homogenes Polynom/Skalarmultiplikation auf Nullstellenmenge/Abgeschlossen/Aufgabe -->

Misalkan $F\in K[X_1,\ldots,X_n]$ suatu polinom homogen dengan lokus nol
$V(F)$. Buktikan bahwa bagi setiap titik $P\in V(F)$ dan setiap skalar
$\lambda\in K$, berlaku pula $\lambda P\in V(F)$.

### Soal 5.2 {#br-ak-2025-2026-w05-ex-02}

<!-- upstream_entity: Homogene Polynome in zwei Variablen/C/X^n-Y^n/Aufgabe -->

Tentukan faktorisasi polinom

$$
X^n-Y^n\in\mathbb C[X,Y]
$$

untuk $n\in\mathbb N_+$.

### Soal 5.3 ★ {#br-ak-2025-2026-w05-ex-03}

<!-- upstream_entity: Homogene Polynome in zwei Variablen/Algebraisch abgeschlossener Körper/Zerfällt/Aufgabe -->

Misalkan $K$ suatu lapangan tertutup secara aljabar dan
$F\in K[X,Y]$ suatu polinom homogen. Buktikan bahwa $F$ terurai menjadi
faktor-faktor linear.

### Soal 5.4 {#br-ak-2025-2026-w05-ex-04}

<!-- upstream_entity: Homogenes Polynom/Körper/Faktoren/Homogen/Aufgabe -->

Misalkan $K$ suatu lapangan, $F\in K[X_1,\ldots,X_n]$ suatu polinom homogen,
dan $F=GH$ suatu faktorisasi. Buktikan bahwa $G$ dan $H$ juga homogen.

### Soal 5.5 {#br-ak-2025-2026-w05-ex-05}

<!-- upstream_entity: Polynomring/Mehrere Variablen/Potenzen des maximalen Ideals/Gradabschnitt/Aufgabe -->

Misalkan $R$ suatu gelanggang komutatif dan

$$
P=R[X_1,\ldots,X_m]
$$

gelanggang polinomial di atas $R$ dalam $m$ variabel. Misalkan

$$
\mathfrak m=(X_1,\ldots,X_m)
$$

ideal yang dibangkitkan oleh variabel-variabel tersebut. Buktikan bahwa

$$
\mathfrak m^n=P_{\ge n},
$$

dengan $P_{\ge n}$ menyatakan ideal dalam $P$ yang dibangkitkan oleh semua
polinom homogen berderajat $\ge n$.

### Soal 5.6 {#br-ak-2025-2026-w05-ex-06}

<!-- upstream_entity: Homogene Polynome/Unter linearer Transformation/Bleibt homogen/Aufgabe -->

Buktikan bahwa suatu polinom homogen tetap homogen dengan derajat yang sama
di bawah transformasi variabel linear, sedangkan hal ini tidak harus berlaku
di bawah transformasi variabel afin-linear.

### Soal 5.7 {#br-ak-2025-2026-w05-ex-07}

<!-- upstream_entity: Affine Varietäten/Affin-linear äquivalente Nullstellengebilde/Ist Äquivalenzrelation/Aufgabe -->

Buktikan bahwa relasi ekuivalensi afin-linear merupakan suatu relasi
ekuivalensi pada himpunan-himpunan aljabar afin
$V,V'\subseteq\mathbb A_K^n$.

### Soal 5.8 {#br-ak-2025-2026-w05-ex-08}

<!-- upstream_entity: Affine Ebene/Punkt und verschiedene Geraden/Transformation auf Achsenkreuz/Aufgabe -->

Misalkan $P=(a,b)$ suatu titik di bidang afin, dan $L$ serta $L'$ dua garis
berbeda yang melalui $P$. Misalkan $C=V(F)$, dengan $F\in K[X,Y]$, suatu
kurva aljabar bidang. Deskripsikan secara eksplisit suatu transformasi
variabel (perubahan koordinat) sedemikian sehingga dalam koordinat baru $P$
menjadi titik asal dan kedua garis menjadi kedua sumbu koordinat. Bagaimana
persamaan kurva tersebut dalam koordinat baru?

### Soal 5.9 {#br-ak-2025-2026-w05-ex-09}

<!-- upstream_entity: Affine Ebene/Drei verschiedene Geraden/Affin-linear äquivalent/Aufgabe -->

Misalkan $C$ dan $D$ masing-masing merupakan kurva aljabar afin bidang yang
terdiri atas gabungan tiga garis berbeda, dan ketiga garis pada masing-masing
kurva berpotongan di satu titik. Buktikan bahwa terdapat perubahan koordinat
afin-linear yang memetakan $C$ ke $D$.

### Soal 5.10 {#br-ak-2025-2026-w05-ex-10}

<!-- upstream_entity: Affine Ebene/Vier verschiedene Geraden/Nicht affin-linear äquivalent/Aufgabe -->

Misalkan $C$ dan $D$ masing-masing merupakan kurva aljabar afin bidang yang
terdiri atas gabungan empat garis berbeda, dan keempat garis pada
masing-masing kurva berpotongan di satu titik. Buktikan bahwa pada umumnya
tidak terdapat perubahan koordinat afin-linear yang memetakan $C$ ke $D$.

Dua soal berikut dimaksudkan untuk memahami Teorema 5.4 dan Korolari 5.5.

### Soal 5.11 {#br-ak-2025-2026-w05-ex-11}

<!-- upstream_entity: Ebene Kurven/Algebraisch abgeschlossener Körper/Noethersche Normalisierung/Anwendung auf Y/Aufgabe -->

Terapkan bukti Teorema 5.4 pada polinom $Y$.

### Soal 5.12 {#br-ak-2025-2026-w05-ex-12}

<!-- upstream_entity: Noethersche Normalisierung/Ebene/Hyperbel/Aufgabe -->

Terapkan bukti Teorema 5.4 pada hiperbola $XY-1$.

### Soal 5.13 {#br-ak-2025-2026-w05-ex-13}

<!-- upstream_entity: Noethersche Normalisierung/Ebene/2/Aufgabe -->

Terapkan bukti Teorema 5.4 pada polinom

$$
X^2Y^3+5X^3Y^2-X^2Y^2+3Y+7\in\mathbb C[X,Y].
$$

### Soal 5.14 {#br-ak-2025-2026-w05-ex-14}

<!-- upstream_entity: Ebene Kurven/C/Überabzählbar viele Elemente/Aufgabe -->

Misalkan $F\in\mathbb C[X,Y]$ suatu polinom takkonstan. Buktikan bahwa kurva
aljabar $C=V(F)$ yang bersesuaian mempunyai takterhitung banyak elemen.

### Soal 5.15 ★ {#br-ak-2025-2026-w05-ex-15}

<!-- upstream_entity: Affine Ebene/Unendlicher Körper/Endliche Punktmenge/Irreduzibler Kurvenschnitt/Aufgabe -->

Misalkan

$$
M=\{P_1,\ldots,P_n\}\subseteq K^2
$$

suatu himpunan titik berhingga di bidang di atas lapangan takhingga $K$.

1. Buktikan bahwa $M$ dapat diperoleh sebagai irisan dua kurva aljabar.
2. Buktikan bahwa $M$ dapat diperoleh sebagai irisan dua kurva aljabar yang
   tak tereduksi.

### Soal 5.16 {#br-ak-2025-2026-w05-ex-16}

<!-- upstream_entity: Polynomiale Abbildungen der Ebene/x nach t^2+s-3, y nach 3ts+s^2-t/Bild von x^2y+3xy-y^3/Aufgabe -->

Hitung citra $\widetilde F$ dari polinom

$$
F=X^2Y+3XY-Y^3
$$

di bawah homomorfisme substitusi

$$
K[X,Y]\longrightarrow K[S,T]
$$

yang ditentukan oleh

$$
X\longmapsto T^2+S-3,
\qquad
Y\longmapsto 3TS+S^2-T.
$$

### Soal 5.17 {#br-ak-2025-2026-w05-ex-17}

<!-- upstream_entity: K unendlich/Polynom/Bild unendlich oder konstant/Zwei Beweise/Aufgabe -->

Misalkan $K$ suatu lapangan takhingga dan
$F\in K[X_1,\ldots,X_n]$ suatu polinom dengan pemetaan yang bersesuaian

$$
F:\mathbb A_K^n\longrightarrow\mathbb A_K^1.
$$

Buktikan, dengan dan tanpa menggunakan Teorema 5.10, bahwa citra $F$ terdiri
atas satu titik atau takhingga banyak titik.

### Soal 5.18 {#br-ak-2025-2026-w05-ex-18}

<!-- upstream_entity: Endlicher Körper/Endlich viele Punkte in Ebene/Parametrisierung und Anzahl/Aufgabe -->

Misalkan $K$ suatu lapangan berhingga dengan $q$ elemen, dan

$$
P_1,\ldots,P_n\in\mathbb A_K^2
$$

merupakan $n$ titik di bidang afin. Buktikan bahwa terdapat pemetaan
polinomial

$$
\varphi:\mathbb A_K^1\longrightarrow\mathbb A_K^2
$$

dengan

$$
\operatorname{im}\varphi=\{P_1,\ldots,P_n\}
$$

tepat ketika $1\le n\le q$.

### Soal 5.19 ★ {#br-ak-2025-2026-w05-ex-19}

<!-- upstream_entity: Polynomiale Abbildung/A^2 nach A^1/Eine Faser reduzibel, sonst irreduzibel/Aufgabe -->

Berikan sebuah contoh pemetaan polinomial

$$
\mathbb A_K^2\longrightarrow\mathbb A_K^1
$$

sedemikian sehingga praimaj satu titik tereduksi, sedangkan praimaj setiap
titik lainnya tak tereduksi.

### Soal 5.20 ★ {#br-ak-2025-2026-w05-ex-20}

<!-- upstream_entity: Körper/Nullstellen auf Polynomkoeffizienten/Eigenschaften/Aufgabe -->

Misalkan $K$ suatu lapangan. Untuk setiap $n\in\mathbb N_+$, pertimbangkan
pemetaan

$$
\begin{aligned}
\varphi:K^n&\longrightarrow K^n,\\
(\lambda_1,\lambda_2,\ldots,\lambda_n)
&\longmapsto(c_0,c_1,\ldots,c_{n-1}),
\end{aligned}
$$

yang memetakan tupel akar $(\lambda_1,\ldots,\lambda_n)$ ke tupel koefisien
$(c_0,\ldots,c_{n-1})$ (tanpa koefisien $1$) dari polinom monik

$$
(X-\lambda_1)(X-\lambda_2)\cdots(X-\lambda_n)
=P=c_0+c_1X+\cdots+c_{n-1}X^{n-1}+X^n.
$$

1. Deskripsikan $\varphi$ secara eksplisit untuk $n=2$.
2. Deskripsikan $\varphi$ secara eksplisit untuk $n=3$.
3. Jelaskan mengapa pemetaan-pemetaan $\varphi$ tersebut polinomial.
4. Buktikan bahwa serat-serat $\varphi$ berhingga.
5. Kapan serat di atas suatu tupel $(c_0,c_1,\ldots,c_{n-1})$ kosong?
6. Berapakah banyak elemen maksimum dalam suatu serat? Berikan contoh yang
   menunjukkan bahwa maksimum tersebut dicapai untuk $K=\mathbb R$.
7. Sekarang misalkan $K$ tertutup secara aljabar. Buktikan bahwa $\varphi$
   surjektif.

### Soal 5.21 {#br-ak-2025-2026-w05-ex-21}

<!-- upstream_entity: Zariski-Topologie/Polynomiale Abbildung/Abschluss von Bild/Aufgabe -->

Misalkan

$$
\varphi:\mathbb A_K^r\longrightarrow\mathbb A_K^n
$$

suatu pemetaan polinomial dan $T\subseteq\mathbb A_K^r$ suatu subhimpunan.
Buktikan bahwa

$$
\overline{\varphi(T)}=\overline{\varphi(\overline T)}.
$$

### Soal 5.22 {#br-ak-2025-2026-w05-ex-22}

<!-- upstream_entity: Zariski-Topologie/Beispiel für Abbildung/Abschluss vom Bild/Ist nicht Abschluss vom Bild vom Abschluss/Aufgabe -->

Buktikan bahwa pernyataan Soal 5.21 tidak berlaku tanpa asumsi bahwa
pemetaan tersebut polinomial.

## Soal untuk dikumpulkan {#br-ak-2025-2026-w05-submission}

### Soal 5.23 - 3 poin {#br-ak-2025-2026-w05-ex-23}

<!-- upstream_entity: Homogene Polynome/Bis zu drei Variablen/Wie viele Monome/Aufgabe -->

Berapa banyak monomial berderajat $d$ yang terdapat dalam gelanggang
polinomial dalam satu, dua, dan tiga variabel?

### Soal 5.24 - 3 poin {#br-ak-2025-2026-w05-ex-24}

<!-- upstream_entity: Ebene Kurven/Algebraisch abgeschlossener Körper/Noethersche Normalisierung/Anwendung auf Y ist X^2-2X durch X^2-1/Aufgabe -->

Terapkan bukti Teorema 5.4 pada kurva aljabar yang bersesuaian dengan fungsi
rasional

$$
Y=\frac{X^2-2X}{X^2-1}.
$$

### Soal 5.25 - 3 poin {#br-ak-2025-2026-w05-ex-25}

<!-- upstream_entity: Polynomiale Abbildungen auf Ebene/x,y nach x,xy/Bestimme Fasern/Aufgabe -->

Pertimbangkan pemetaan

$$
\mathbb A_K^2\longrightarrow\mathbb A_K^2,
\qquad
(x,y)\longmapsto(x,xy).
$$

Tentukan citra dan serat-serat pemetaan ini.

### Soal 5.26 - 3 poin {#br-ak-2025-2026-w05-ex-26}

<!-- upstream_entity: Quadriken in drei Variablen/2x^2+3y^2+4z^2-5/Transformiere auf Standardkugel/Aufgabe -->

Pertimbangkan elipsoid

$$
E=V(2x^2+3y^2+4z^2-5)
=\{(x,y,z):2x^2+3y^2+4z^2=5\}.
$$

Temukan suatu transformasi variabel afin-linear di atas $\mathbb R$
sedemikian sehingga citra $E$ di bawah pemetaan tersebut adalah bola satuan
standar

$$
V(x^2+y^2+z^2-1).
$$

![Sebuah elipsoid; dalam geometri aljabar yang dimaksud adalah permukaannya](authority/assets/Elipsoid_trojosy321.png)

### Soal 5.27 - 4 poin {#br-ak-2025-2026-w05-ex-27}

<!-- upstream_entity: Affine ebene Kurven/über Z mod 2/Affin-linear äquivalent und gleiche Anzahl/Aufgabe -->

Misalkan $V$ dan $\widetilde V$ himpunan-himpunan aljabar afin dalam
$\mathbb A_K^2$ untuk $K=\mathbb Z/(2)$. Buktikan bahwa kedua himpunan itu
ekuivalen afin-linear tepat ketika keduanya mempunyai kardinalitas yang sama.

Buktikan pula bahwa pernyataan ini tidak berlaku untuk
$K=\mathbb Z/(p)$ dengan $p\ge3$, dan juga tidak berlaku di
$\mathbb A_{\mathbb Z/(2)}^n$ untuk $n\ge3$.

---

**Navigasi sumber:** [Kuliah 5](#br-ak-2025-2026-l05) - [solusi publik Unit 5](#br-ak-2025-2026-w05-solutions) - [Lembar Kerja 4](#br-ak-2025-2026-w04) - [Lembar Kerja 6 (sumber)](https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)/Arbeitsblatt_6)
