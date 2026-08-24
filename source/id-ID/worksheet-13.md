---
title: "Lembar Kerja 13 - Pelokalan, Keterhubungan, dan Unsur Idempoten"
stable_id: br-ak-2025-2026-w13
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Arbeitsblatt 13"
upstream_pageid: 165932
upstream_revid: 1065092
upstream_timestamp: "2026-01-15T10:23:01Z"
upstream_mediawiki_sha1: 20d30f0f2a09974c436262bbe20c0fab3fa34faa
source_url: "https://de.wikiversity.org/w/index.php?oldid=1065092"
authority_manifest: authority/wikiversity/unit-13/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: dc86b4d124c7e775fb635a1f9672a8b8faadc4ff2259b0779f7bac6302d18848
worksheet_xml_sha256: 1882e3d182183429492f2a2d942797e85a5c970c160c7fae461ba14d51e1f0aa
worksheet_expanded_tex_sha256: 353bf5a5b4742d09274f33b3865f70714982be04fc32e22f4d484fa9aa64ba7b
exercise_map: authority/wikiversity/unit-13/ORDERED_EXERCISE_MAP.json
exercise_map_sha256: f954f09c996c8aa22f94ec826a1503b135a7b4fb9f9e0d5d6ff21f36a519e52a
license: "CC BY-SA 4.0"
translation_status: complete
---

# Lembar Kerja 13 {#br-ak-2025-2026-w13}

## Soal latihan {#br-ak-2025-2026-w13-practice}

<!-- upstream_entity: Nenneraufnahme/Mit Nullteilern/Begriff/Aufgabe -->

### Soal 13.1 {#br-ak-2025-2026-w13-ex-01}

Misalkan $R$ suatu gelanggang komutatif dan $S\subseteq R$ suatu sistem
multiplikatif. Pelokalan $R_S$ didefinisikan langkah demi langkah sebagai
berikut. Mula-mula, misalkan $M$ himpunan pecahan formal dengan penyebut di
$S$, yaitu

$$
M=\left\{\frac rs\mathrel{\Big|}r\in R,\ s\in S\right\}.
$$

Tunjukkan bahwa

$$
\frac rs\sim\frac{r'}{s'}
\quad\Longleftrightarrow\quad
\text{terdapat }t\in S\text{ dengan }trs'=tr's
$$

mendefinisikan relasi ekuivalensi pada $M$. Nyatakan dengan $R_S$ himpunan
kelas ekuivalensinya. Definisikan struktur gelanggang pada $R_S$ dan suatu
homomorfisme gelanggang $R\to R_S$.

<!-- upstream_entity: Nenneraufnahme/Ist Unterring/Umkehrung/Aufgabe -->

### Soal 13.2 {#br-ak-2025-2026-w13-ex-02}

Misalkan $R$ suatu daerah integral dan $S\subseteq R$ suatu sistem
multiplikatif dengan $0\notin S$.

1. Tunjukkan bahwa pelokalan

   $$
   R_S:=\left\{\frac fg\mathrel{\Big|}f\in R,\ g\in S\right\}
   \subseteq Q(R)
   $$

   merupakan subgelanggang dari $Q(R)$.
2. Tunjukkan bahwa tidak setiap subgelanggang dari $Q(R)$ merupakan suatu
   pelokalan.

<!-- upstream_entity: Rationale Zahlen/Unterringe/Überabzählbar/Aufgabe -->

### Soal 13.3 ★ {#br-ak-2025-2026-w13-ex-03}

Tunjukkan bahwa lapangan bilangan rasional $\mathbb Q$ mempunyai tak
terhitung banyak subgelanggang.

<!-- upstream_entity: Kommutative Ringtheorie/Nenneraufnahme/Ein Element/Restklassendarstellung/Aufgabe -->

### Soal 13.4 {#br-ak-2025-2026-w13-ex-04}

Misalkan $R$ suatu gelanggang komutatif dan $f\in R$, dengan pelokalan
$R_f$. Buktikan isomorfisme aljabar-$R$

$$
R_f\cong R[T]/(Tf-1).
$$

<!-- upstream_entity: Nenneraufnahme/f/Nilpotent/Aufgabe -->

### Soal 13.5 {#br-ak-2025-2026-w13-ex-05}

Misalkan $R$ suatu gelanggang komutatif, $f\in R$, dan $R_f$ pelokalan yang
bersesuaian. Tunjukkan bahwa $f$ nilpoten jika dan hanya jika $R_f$ merupakan
gelanggang nol.

Dalam soal-soal berikut tentang pelokalan, Anda boleh menganggap gelanggang
yang muncul sebagai daerah integral jika menginginkannya.

<!-- upstream_entity: Nenneraufnahme/Universelle Eigenschaft/Fakt/Beweis/Aufgabe -->

### Soal 13.6 ★ {#br-ak-2025-2026-w13-ex-06}

Misalkan $R,A$ gelanggang komutatif, $S\subseteq R$ suatu sistem
multiplikatif, dan

$$
\varphi:R\longrightarrow A
$$

suatu homomorfisme gelanggang sedemikian sehingga $\varphi(s)$ adalah satuan
di $A$ untuk setiap $s\in S$. Tunjukkan bahwa terdapat tepat satu
homomorfisme gelanggang

$$
\widetilde\varphi:R_S\longrightarrow A
$$

yang memperluas $\varphi$.

<!-- upstream_entity: Nenneraufnahme/Verhalten von Primidealen/Aufgabe -->

### Soal 13.7 {#br-ak-2025-2026-w13-ex-07}

Misalkan $R$ suatu gelanggang komutatif dan $S\subseteq R$ suatu sistem
multiplikatif. Tunjukkan bahwa ideal-ideal prima di $R_S$ tepat
berkorespondensi dengan ideal-ideal prima di $R$ yang tidak beririsan dengan
$S$.

<!-- upstream_entity: Polynomring zwei Variablen/Multiplikatives System/Eine Gleichung/Verträglichkeit/Aufgabe -->

### Soal 13.8 ★ {#br-ak-2025-2026-w13-ex-08}

Misalkan $K$ suatu lapangan, $R=K[X,Y]$, $S\subseteq R$ suatu sistem
multiplikatif, dan $F\in R$. Tunjukkan bahwa terdapat tepat satu isomorfisme
aljabar-$R$

$$
(R/(F))_S\cong (R_S)/(F),
$$

di mana pada ruas kiri pelokalan diambil terhadap citra $S$ di $R/(F)$.

<!-- upstream_entity: Nenneraufnahme/Restklassenbildung/Vertauschbarkeit/Fakt/Beweis/Aufgabe -->

### Soal 13.9 ★ {#br-ak-2025-2026-w13-ex-09}

Misalkan $R$ suatu gelanggang komutatif, $\mathfrak a\subseteq R$ suatu ideal,
dan $S\subseteq R$ suatu sistem multiplikatif. Tunjukkan bahwa terdapat
isomorfisme gelanggang alami

$$
(R/\mathfrak a)_S\cong R_S/\mathfrak aR_S,
$$

di mana pelokalan pada ruas kiri diambil terhadap citra $S$ di
$R/\mathfrak a$.

<!-- upstream_entity: Kommutative Ringtheorie/K-Spektren/Algebraisch abgeschlossen/Nenneraufnahme zu einem Element/Faktorisierungsverhalten/Aufgabe -->

### Soal 13.10 {#br-ak-2025-2026-w13-ex-10}

Misalkan $K$ lapangan tertutup secara aljabar, $R,S$ aljabar-$K$ komutatif
bertipe hingga, $f\in R$, dan

$$
\varphi:R\longrightarrow S
$$

suatu homomorfisme aljabar-$K$. Tunjukkan bahwa pemetaan spektrum
$\varphi^*$ memfaktor melalui $D(f)$ jika dan hanya jika $\varphi(f)$ adalah
satuan di $S$.

<!-- upstream_entity: Hilbertscher Nullstellensatz/Äquivalent/D(f) in D(g)/R g nach R f/Aufgabe -->

### Soal 13.11 ★ {#br-ak-2025-2026-w13-ex-11}

Misalkan $K$ lapangan tertutup secara aljabar dan $R$ aljabar-$K$ integral
bertipe hingga. Untuk $f,g\in R$, tunjukkan bahwa pernyataan berikut
ekuivalen:

1. $D(f)\subseteq D(g)$;
2. terdapat homomorfisme aljabar-$R$ $R_g\to R_f$.

Tunjukkan pula bahwa ekuivalensi ini tidak berlaku untuk $K=\mathbb R$.

Soal berikut menggunakan konsep sistem multiplikatif jenuh. Suatu sistem
multiplikatif $S$ di dalam gelanggang komutatif $R$ disebut *jenuh* jika:
bila $g\in R$ dan terdapat $f\in S$ yang habis dibagi oleh $g$, maka
$g\in S$.

<!-- upstream_entity: Multiplikatives System/Saturiert/Urbild der Einheitengruppe/Aufgabe -->

### Soal 13.12 {#br-ak-2025-2026-w13-ex-12}

Misalkan $A,B$ gelanggang komutatif dan
$\varphi:A\to B$ suatu homomorfisme gelanggang. Tunjukkan bahwa praimaj

$$
\varphi^{-1}(B^\times)
$$

dari grup satuan merupakan sistem multiplikatif jenuh di $A$.

<!-- upstream_entity: Kommutative Ringtheorie/Nichtnullteiler/Sind saturiertes multiplikatives System/Aufgabe -->

### Soal 13.13 {#br-ak-2025-2026-w13-ex-13}

Misalkan $R$ suatu gelanggang komutatif. Tunjukkan bahwa himpunan semua unsur
bukan pembagi nol di $R$ membentuk sistem multiplikatif jenuh.

<!-- upstream_entity: Endlich erzeugte integre K-Algebra/C/Nenneraufnahme/Kein maximales Ideal überlebt/Aufgabe -->

### Soal 13.14 ★ {#br-ak-2025-2026-w13-ex-14}

Berikan contoh aljabar-$\mathbb C$ integral bertipe hingga $R$ dan sistem
multiplikatif $S\subseteq R$, $0\notin S$, sedemikian sehingga $R_S$ bukan
lapangan, tetapi setiap ideal maksimal di $R$ menjadi ideal satuan di $R_S$.

<!-- upstream_entity: Integritätsbereich/Zusammenhängend/Aufgabe -->

### Soal 13.15 ★ {#br-ak-2025-2026-w13-ex-15}

Tunjukkan bahwa setiap daerah integral merupakan gelanggang terhubung.

<!-- upstream_entity: Kommutative Ringtheorie/Idempotent und nilpotent/Ist null/Aufgabe -->

### Soal 13.16 {#br-ak-2025-2026-w13-ex-16}

Misalkan $R$ suatu gelanggang komutatif dan $f\in R$. Jika $f$ sekaligus
nilpoten dan idempoten, tunjukkan bahwa $f=0$.

<!-- upstream_entity: Kommutativer Ring/nx und x^n ist 0/Aufgabe -->

### Soal 13.17 ★ {#br-ak-2025-2026-w13-ex-17}

Untuk setiap $n\ge2$, berikan gelanggang komutatif $R$ dan unsur
$x\in R$, $x\ne0$, yang memenuhi

$$
nx=0
\qquad\text{dan}\qquad
x^n=0.
$$

<!-- upstream_entity: Kommutativer Ring/Idempotentes Element/Nenneraufnahme und Restklassenring/Aufgabe -->

### Soal 13.18 {#br-ak-2025-2026-w13-ex-18}

Misalkan $R$ suatu gelanggang komutatif dan $e\in R$ suatu unsur idempoten.
Tunjukkan bahwa terdapat isomorfisme gelanggang alami

$$
R_e\cong R/(1-e).
$$

Ini menunjukkan sekali lagi bahwa $D(e)$ sekaligus terbuka dan tertutup.

<!-- upstream_entity: Kommutative Ringtheorie/Produktring/R_1 x 0 ist Hauptideal/Aufgabe -->

### Soal 13.19 {#br-ak-2025-2026-w13-ex-19}

Misalkan $R,S$ gelanggang komutatif. Tunjukkan bahwa subhimpunan
$R\times0$ dari gelanggang produk $R\times S$ merupakan ideal utama.

<!-- upstream_entity: Z/Restklassenring nach Primelementpotenz/Ist zusammenhängend/Aufgabe -->

### Soal 13.20 ★ {#br-ak-2025-2026-w13-ex-20}

Misalkan $p\in\mathbb Z$ suatu bilangan prima dan $n\in\mathbb N$. Tunjukkan
bahwa gelanggang kelas residu $\mathbb Z/(p^n)$ hanya mempunyai dua unsur
idempoten trivial, $0$ dan $1$.

<!-- upstream_entity: Polynom/Q X modulo X^4-1/Produkt von Körpern/Restklasse von X^3+X/Aufgabe -->

### Soal 13.21 ★ {#br-ak-2025-2026-w13-ex-21}

Tuliskan gelanggang kelas residu

$$
\mathbb Q[X]/(X^4-1)
$$

sebagai produk lapangan yang hanya melibatkan $\mathbb Q$ dan
$\mathbb Q[\mathrm i]$. Tuliskan kelas residu $X^3+X$ sebagai suatu tupel
dalam dekomposisi produk tersebut.

<!-- upstream_entity: Polynomring K X/Produkt von Linearfaktoren/Restklassenring/Aufgabe -->

### Soal 13.22 {#br-ak-2025-2026-w13-ex-22}

Misalkan $K$ suatu lapangan, $a_1,\ldots,a_n\in K$ unsur-unsur yang berbeda,
dan

$$
F=(X-a_1)\cdots(X-a_n)\in K[X].
$$

Tunjukkan bahwa gelanggang kelas residu $K[X]/(F)$ isomorfik dengan
gelanggang produk $K^n$.

<!-- upstream_entity: Polynomring K X/Algebraisch abgeschlossen/Restklassenring/Struktur/Aufgabe -->

### Soal 13.23 {#br-ak-2025-2026-w13-ex-23}

Misalkan $K$ suatu lapangan tertutup secara aljabar. Tunjukkan bahwa untuk
setiap polinom tak nol $F\in K[X]$, gelanggang kelas residunya mempunyai
struktur

$$
K[X]/(F)
\cong
K[T]/(T^{n_1})\times\cdots\times K[T]/(T^{n_r}).
$$

Tunjukkan pula bahwa

$$
\deg(F)=n_1+\cdots+n_r.
$$

<!-- upstream_entity: K-Algebren/K-Spektren/Disjunkte Realisierung/Aufgabe -->

### Soal 13.24 ★ {#br-ak-2025-2026-w13-ex-24}

Misalkan $K$ suatu lapangan dan

$$
A=K[X_1,\ldots,X_m]/\mathfrak a,
\qquad
B=K[Y_1,\ldots,Y_n]/\mathfrak b
$$

aljabar-$K$ bertipe hingga. Tetapkan

$$
\ell=\max(m,n).
$$

Tunjukkan bahwa spektrum-$K$ dari gelanggang produk $A\times B$ dapat
direalisasikan sebagai himpunan tertutup dalam $\mathbb A_K^{\ell+1}$.

<!-- upstream_entity: Topologie/Zusammenhang/Nicht zusammenhängend/Nichttriviale stetige idempotente Abbildungen/Aufgabe -->

### Soal 13.25 {#br-ak-2025-2026-w13-ex-25}

Misalkan $X$ suatu ruang topologis yang tak kosong dan tidak terhubung.
Tunjukkan bahwa terdapat fungsi kontinu

$$
f:X\longrightarrow\mathbb R,
\qquad f\ne0,1,
$$

dengan $\mathbb R$ diberi topologi metrik, yang idempoten di dalam gelanggang
fungsi kontinu pada $X$.

<!-- upstream_entity: Funktionenring/Disjunkte Zerlegung/Produktring/Aufgabe -->

### Soal 13.26 {#br-ak-2025-2026-w13-ex-26}

Misalkan $X$ suatu ruang topologis dengan dekomposisi disjung

$$
X=U\mathbin{\uplus}V
$$

menjadi subhimpunan terbuka $U,V\subseteq X$. Tunjukkan bahwa pemetaan alami

$$
\begin{aligned}
C(X,\mathbb R)&\longrightarrow C(U,\mathbb R)\times C(V,\mathbb R),\\
f&\longmapsto(f|_U,f|_V)
\end{aligned}
$$

bijektif.

<!-- upstream_entity: Idempotente Elemente/Reduktion/Injektiv/Aufgabe -->

### Soal 13.27 ★ {#br-ak-2025-2026-w13-ex-27}

Misalkan $R$ suatu gelanggang komutatif dengan reduksi $S$. Tunjukkan bahwa
pemetaan yang mengirim setiap unsur idempoten di $R$ ke kelas residunya di
$S$ bersifat injektif.

<!-- upstream_entity: Idempotente Elemente/Modulo nilpotentes Element/Surjektiv/Aufgabe -->

### Soal 13.28 ★ {#br-ak-2025-2026-w13-ex-28}

Misalkan $R$ suatu gelanggang komutatif yang mempunyai unsur $n\in R$ dengan
$n^2=0$, dan misalkan

$$
S=R/(n).
$$

Tunjukkan bahwa setiap unsur idempoten $e$ di $S$ mempunyai praimaj idempoten
di $R$.

<!-- upstream_entity: Reduktion/Noetherscher Ring/Induktionsschritt/Aufgabe -->

### Soal 13.29 {#br-ak-2025-2026-w13-ex-29}

Misalkan $R$ suatu gelanggang komutatif Noether dengan reduksi $S$. Tunjukkan
bahwa terdapat barisan gelanggang komutatif $R_i$, $1\le i\le n$, dan
homomorfisme gelanggang surjektif

$$
\varphi_i:R_i\longrightarrow R_{i+1}
$$

sedemikian sehingga pemetaan komposit

$$
R=R_0\longrightarrow R_1\longrightarrow\cdots
\longrightarrow R_{n-1}\longrightarrow R_n=S
$$

merupakan pemetaan reduksi, dan setiap $\varphi_i$ adalah homomorfisme kelas
residu $R_i\to R_i/(x_i)$ untuk suatu $x_i\in R_i$ dengan $x_i^2=0$.

**Catatan edisi:** sumber menuliskan domain dan kodomain homomorfisme kelas
residu terakhir sebagai $R\to R/(x_i)$; notasi $R_i\to R_i/(x_i)$ di atas
mengikuti konteks barisan dan unsur $x_i\in R_i$.

<!-- upstream_entity: Idempotente Elemente/Reduktion/Surjektiv/Aufgabe -->

### Soal 13.30 {#br-ak-2025-2026-w13-ex-30}

Misalkan $R$ suatu gelanggang komutatif dengan reduksi $S$. Tunjukkan bahwa
pemetaan yang mengirim setiap unsur idempoten di $R$ ke kelas residunya di
$S$ bersifat surjektif.

Pernyataan berikut merupakan salah satu versi Teorema Sisa Cina.

<!-- upstream_entity: Kommutativer Ring/Ideal/Teilerfremd/Chinesischer Restsatz/Fakt/Beweis/Aufgabe -->

### Soal 13.31 ★ {#br-ak-2025-2026-w13-ex-31}

Misalkan $R$ suatu gelanggang komutatif dan
$\mathfrak a_j$, $j=1,\ldots,n$, ideal-ideal yang memenuhi

$$
\mathfrak a_i+\mathfrak a_j=R
$$

untuk semua $i\ne j$. Tunjukkan bahwa

$$
R/(\mathfrak a_1\cdots\mathfrak a_n)
\cong
R/\mathfrak a_1\times\cdots\times R/\mathfrak a_n.
$$

## Soal untuk dikumpulkan {#br-ak-2025-2026-w13-submit}

<!-- upstream_entity: Hauptidealbereich/Zwischenring in Quotientenkörper/Ist Nenneraufnahme/Aufgabe -->

### Soal 13.32 (4 poin) {#br-ak-2025-2026-w13-ex-32}

Misalkan $R$ suatu daerah ideal utama dengan lapangan pecahan $Q=Q(R)$.
Tunjukkan bahwa setiap gelanggang perantara

$$
R\subseteq S\subseteq Q
$$

merupakan suatu pelokalan.

<!-- upstream_entity: Algebraische Kurve/y^2 ist x^3+x^2/D(x)/Abgeschlossene Realisierungen/Aufgabe -->

### Soal 13.33 (5 poin: 1+2+1+1) {#br-ak-2025-2026-w13-ex-33}

Tinjau kurva $C$ yang diberikan oleh

$$
Y^2=X^3+X^2
$$

(lihat Contoh 6.3) dan himpunan terbuka $U=D(X)\subseteq C$.

1. Temukan suatu realisasi tertutup dari $U$ di $\mathbb A_K^3$.
2. Tunjukkan bahwa realisasi tertutup juga ada di $\mathbb A_K^2$.
3. Apakah $U$ isomorfik dengan suatu himpunan terbuka dari garis afin?
4. Sketsakan kurva citra di bawah pemetaan

   $$
   \begin{aligned}
   U&\longrightarrow\mathbb A_{\mathbb R}^2,\\
   (x,y)&\longmapsto\left(\frac1x,y\right).
   \end{aligned}
   $$

<!-- upstream_entity: Ebene algebraische Kurven/Parallele Geraden und Achsenkreuz/Abbildung geometrisch und algebraisch/Aufgabe -->

### Soal 13.34 (4 poin) {#br-ak-2025-2026-w13-ex-34}

Tinjau gabungan dua garis sejajar $V$ dan silang sumbu $W$. Deskripsikan
suatu pemetaan surjektif yang sealami mungkin antara $V$ dan $W$ - tentukan
arahnya - baik secara geometris maupun aljabar. Apakah terdapat pula pemetaan
polinomial surjektif ke arah sebaliknya?

<!-- upstream_entity: Restklassenringe (Z)/Z/175/nilpotent idempotent/Aufgabe -->

### Soal 13.35 (3 poin) {#br-ak-2025-2026-w13-ex-35}

Tentukan semua unsur nilpoten dan semua unsur idempoten di
$\mathbb Z/(175)$.

<!-- upstream_entity: Ebene algebraische Kurven/x^2+y^2-1 und y-x^2/Schnitt als Produktring/Aufgabe -->

### Soal 13.36 (4 poin) {#br-ak-2025-2026-w13-ex-36}

Misalkan $K$ lapangan tertutup secara aljabar. Tinjau irisan dua kurva
aljabar

$$
V(X^2+Y^2-1)
\qquad\text{dan}\qquad
V(Y-X^2).
$$

Identifikasikan gelanggang kelas residu

$$
R=K[X,Y]/(X^2+Y^2-1,\,Y-X^2)
$$

dengan suatu gelanggang produk dan deskripsikan pemetaan kelas residu
$K[X,Y]\to R$ melalui identifikasi tersebut. Tentukan praimaj di $K[X,Y]$
untuk semua unsur idempoten dari gelanggang produk itu.

<!-- upstream_entity: Kommutative Ringtheorie/Nulldimensionale Algebra/Reduziert/Aufgabe -->

### Soal 13.37 (6 poin) {#br-ak-2025-2026-w13-ex-37}

Misalkan $K$ suatu lapangan dan $A$ suatu aljabar-$K$ berdimensi hingga yang
tereduksi. Tunjukkan bahwa $A$ merupakan produk langsung berhingga dari
perluasan-perluasan lapangan hingga atas $K$.

**Petunjuk.** Anda boleh menggunakan tanpa bukti bahwa $A$ hanya mempunyai
berhingga banyak ideal prima.
