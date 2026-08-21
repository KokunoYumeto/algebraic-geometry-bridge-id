---
title: "Kuliah 1 — Kurva Aljabar Bidang"
stable_id: br-ak-2025-2026-l01
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 1"
upstream_pageid: 165889
upstream_revid: 1108084
upstream_timestamp: "2026-07-20T08:57:22Z"
upstream_mediawiki_sha1: sbohlbklicv2bb3w2dxf1d2h6qa1ogt
source_url: "https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)/Vorlesung_1?oldid=1108084"
license: "CC BY-SA 4.0 for translated course text; media retain component licences in authority/RIGHTS.csv"
translation_status: complete
---

# Kuliah 1: Kurva Aljabar Bidang {#br-ak-2025-2026-l01}

## Kurva aljabar bidang {#br-ak-2025-2026-l01-s01}

Apakah kurva aljabar itu? Misalnya, objek-objek yang tampak pada gambar-gambar indah berikut.

![Grafik fungsi linear](authority/assets/Linear_function-250.png)

![Grafik polinom berderajat empat](authority/assets/Polynomialdeg4.png)

![Grafik fungsi rasional](authority/assets/RationalDegree2byXedi.gif)

![Lingkaran satuan](authority/assets/Disk_1-250.png)

![Elips](authority/assets/Ellipse.svg)

![Kurva dengan kuspa](authority/assets/Cusp-250.png)

![Contoh kurva eliptik](authority/assets/Elliptic_curve_simple-250.png)

![Kubik Tschirnhausen](authority/assets/Tschirnhausen_cubic-250.png)

![Kampyle Eudoxus](authority/assets/Kampyle_Eudoxus-250.png)

![Konkoid Pascal](authority/assets/Conchoid_of_Pascal.png)

![Bifolium](authority/assets/Bifolium.png)

![Limaçon](authority/assets/Limacon.png)

![Quadrifolium](authority/assets/Quadrifolium-250.png)

![Lemniskat Bernoulli](authority/assets/Lemniscate_of_Bernoulli-250.png)

Tentu saja kita dapat menggambar banyak hal. Kurva-kurva berikut juga indah, tetapi bukan kurva aljabar.

![Sikloid](authority/assets/Cicloide-250.png)

![Spiral logaritmik](authority/assets/Logarithmic_spiral-250.png)

![Grafik sinus](authority/assets/Sin-250.png)

![Kurva Koch kuadratik](authority/assets/Quadratic_Koch.png)

Kata “aljabar” dalam *kurva aljabar* berasal dari pembatasan bahwa definisinya hanya boleh menggunakan operasi aljabar, yakni penjumlahan dan perkalian, bukan proses analitis seperti mengambil limit, membentuk jumlah tak hingga, melakukan hampiran, mendiferensialkan, atau mengintegralkan. Pemetaan yang diizinkan dalam konteks kita diberikan oleh polinom dalam beberapa variabel. Gambar-gambar di atas menampilkan kurva aljabar bidang yang didefinisikan oleh sebuah polinom dalam dua variabel. Dua gambar pertama adalah *grafik* suatu fungsi polinomial dalam satu variabel; keduanya dideskripsikan oleh

$$
Y=P(X).
$$

Pada gambar pertama, $P(X)=X$ (jadi polinomnya linear), sedangkan pada gambar kedua bentuknya kurang lebih

$$
P(X)=a_4X^4+a_3X^3+a_2X^2+a_1X+a_0,
$$

dengan koefisien-koefisien $a_i$ dalam suatu medan $K$. Dalam geometri aljabar kita menetapkan sebuah *medan dasar* $K$. Medan penting bagi kita adalah bilangan real (gambar-gambar tadi terutama harus dipahami dalam arti ini) dan bilangan kompleks $\mathbb C$. Grafik semacam itu merupakan objek yang sederhana dalam arti bahwa setiap nilai $X$ memiliki tepat satu nilai $Y$, yaitu nilai fungsi, dan nilai itu mudah dihitung apabila kita dapat berhitung di medan yang diberikan. Dalam arti tertentu, grafik tersebut adalah salinan “melengkung” dari garis dasar, yakni sumbu $X$.

Sekarang perhatikan gambar ketiga. Gambar itu adalah grafik suatu *fungsi rasional*: kita mengambil dua polinom $P,Q$ dalam variabel $X$, lalu meninjau hasil bagi $P(X)/Q(X)$. Ungkapan ini hanya bermakna ketika penyebutnya tidak nol. Pada akar-akar polinom penyebut, fungsi rasional tidak terdefinisi. Jika pembilang dan penyebut sama-sama nol di suatu titik, kadang-kadang penyederhanaan pecahan membuat hasil bagi itu dapat diberi makna di titik tersebut. Jika penyebut nol tetapi pembilang tidak, titik ketakterdefinisian itu merupakan sebuah *kutub*: grafik real mendekati $+\infty$ atau $-\infty$. Memang menggoda untuk mengatakan bahwa nilai fungsi rasional pada titik-titik itu adalah “tak hingga”; dalam geometri projektif gagasan ini benar-benar bermakna, sebagaimana akan kita lihat nanti.

Namun, “persamaan grafik” $Y=P(X)/Q(X)$ bukan deskripsi yang ideal karena adanya titik-titik ketakterdefinisian. Jika persamaan itu dikalikan dengan penyebutnya, kita memperoleh syarat, atau *persamaan*,

$$
YQ(X)=P(X),
\qquad\text{atau lebih tepatnya}\qquad
\{(x,y)\in K^2\mid yQ(x)=P(x)\},
$$

yang kedua ruasnya berupa polinom yang terdefinisi dengan baik. *Himpunan pemenuh* (atau *himpunan solusi*) terdefinisi secara tunggal. Untuk suatu $x$ dengan $Q(x)=0$, ruas kiri bernilai nol. Jika $P(x)\ne0$, tidak ada solusi pada $x$ itu, seperti pada gambar; jika $P(x)=0$, setiap nilai $Y$ diperbolehkan. Dalam kasus terakhir, objek tersebut memuat garis melalui $(x,0)$ yang tegak lurus terhadap sumbu $X$.

### Contoh: hiperbola {#br-ak-2025-2026-l01-ex-01}

Contoh khas dan penting dari fungsi rasional adalah $Y=1/X$. Grafik yang bersesuaian disebut *hiperbola* $H$. Tanpa penyebut, persamaannya menjadi

$$
XY=1,
\qquad\text{atau}\qquad
H=\{(x,y)\mid xy=1\}.
$$

Pada $K^\times=K\setminus\{0\}$, fungsi rasional ini merupakan fungsi sejati, dengan $H$ sebagai grafiknya, dan memberikan bijeksi “alami”

$$
K^\times\longrightarrow H,
\qquad x\longmapsto\left(x,\frac1x\right).
$$

Jadi, dalam pengertian yang akan dibuat presisi nanti, $K^\times$ dan $H$ “ekuivalen” atau “isomorfik”.

Kedua deskripsi tersebut memiliki kelebihan masing-masing. Deskripsi sebagai $K^\times\subset K$ berlangsung pada sebuah garis (jika kita membayangkan $K=\mathbb R$), tetapi titik $0$, yang merupakan *titik limit* dari $K^\times$, tidak termasuk dalam $K^\times$. Dengan kata lain, $K^\times$ tidak *tertutup*. Sebaliknya, hiperbola tertutup di $\mathbb R^2$; jadi, untuk mewujudkannya sebagai himpunan tertutup, kita harus berpindah ke dimensi yang lebih tinggi. Pertanyaan mengenai deskripsi yang baik bagi sebuah objek geometri aljabar akan terus muncul.

![Hiperbola siku-siku](authority/assets/Rectangular_hyperbola-250.png)

Dalam kasus real, yakni $K=\mathbb R$, himpunan $\mathbb R^\times$ (dan demikian pula $H_{\mathbb R}$) terdiri atas dua “cabang” yang saling lepas, sehingga tidak *terhubung*. Dalam kasus kompleks, yakni $K=\mathbb C$, himpunan $\mathbb C^\times$ (dan demikian pula $H_{\mathbb C}$) adalah bidang real dengan satu titik dihilangkan, sehingga terhubung. Ini adalah fenomena khas geometri aljabar: sifat-sifat penting dapat bergantung pada medan dasar. Meskipun demikian, sifat-sifat yang hanya bergantung pada persamaan yang mendeskripsikan objek—dan berlaku bagi himpunan solusi di atas semua medan—mempunyai arti yang sangat khusus.

Gambar keempat adalah sebuah *lingkaran*, dengan persamaan

$$
K=\{(x,y)\mid x^2+y^2=r^2\},
$$

di mana $r$ menyatakan jari-jari lingkaran. Gambar itu sendiri sudah menunjukkan bahwa objek ini tidak mungkin merupakan grafik sebuah fungsi, sebab pada suatu grafik setiap nilai $x$ selalu berpasangan dengan tepat satu nilai $y$. Tidak ada fungsi $y=\varphi(x)$ yang memenuhi

$$
K=\{(x,\varphi(x))\mid x\in\mathbb R\}.
$$

Pertanyaan apakah suatu objek solusi aljabar dapat diwujudkan sebagai grafik ekuivalen dengan pertanyaan apakah persamaan pendefinisinya dapat “diselesaikan” terhadap $y$. Pada contoh ini kita dapat menulis

$$
y^2=r^2-x^2,
\qquad
y=\sqrt{r^2-x^2}=\sqrt{(r-x)(r+x)}.
$$

Jadi, apakah lingkaran itu ternyata sebuah grafik? Ada dua penafsiran.

1. Jika kita membatasi diri pada bilangan real dan akar positif, langkah terakhir bukan transformasi yang ekuivalen: kita telah “menambahkan” informasi yang tidak ada dalam persamaan semula. Mengambil akar positif berarti membatasi diri pada setengah lingkaran atas. Menambahkan informasi atau syarat memperkecil himpunan solusi.

2. Jika sebaliknya $\sqrt{\phantom{x}}$ dipahami sebagai semua solusi—dalam bilangan real, akar kuadrat positif dan negatif, yang sering ditulis $\pm\sqrt{\phantom{x}}$—kita tidak menambahkan informasi, tetapi juga belum menyelesaikan persamaan menjadi sebuah fungsi; kita baru memperoleh apa yang kadang disebut “fungsi bernilai banyak”.

Kedua sudut pandang itu berguna. Upaya mencari deskripsi sederhana sebagai grafik bagi suatu bagian objek geometri, seperti busur atas, muncul kembali dalam teorema fungsi implisit, pendekatan deret pangkat, parametrisasi, dan teori lokal.

## Persamaan berbentuk $Y^2=G(X)$ {#br-ak-2025-2026-l01-s02}

![Kurva-kurva kubik yang dikaji Newton](authority/assets/Newtonbig.gif)

![Isaac Newton (1643–1727)](authority/assets/GodfreyKneller-IsaacNewton-1689.jpg)

Persamaan lingkaran dapat dipandang sebagai persamaan berbentuk

$$
Y^2=G(X),
$$

dengan $G$ sebuah polinom dalam satu variabel $X$; untuk lingkaran, $G=-X^2+1$. Objek ini bukan grafik, melainkan “akar” dari sebuah grafik. Secara umum, izinkan $G(X)$ lebih rumit. Himpunan nol (*lokus nol*) tersebut merepresentasikan akar kuadrat $\sqrt{G(X)}$. Jika kita menetapkan sebarang nilai $x$ bagi $X$, maka dalam bilangan real ada tiga kemungkinan bagi solusi $y$ yang bersesuaian.

1. Jika $G(x)<0$, tidak ada solusi.
2. Jika $G(x)=0$, terdapat tepat satu solusi, yaitu $y=0$.
3. Jika $G(x)>0$, terdapat dua solusi, yaitu $y=\pm\sqrt{G(x)}$.

Ini juga memberi cara untuk membayangkan gambar realnya: untuk setiap $x$, hitung $G(x)$, lalu—jika radikannya taknegatif—tandai titik-titik $(x,\pm\sqrt{G(x)})$.

Di atas bilangan kompleks, kita hanya perlu membedakan kasus $G(x)=0$ dan $G(x)\ne0$. Jika $G$ berderajat dua, kurva yang diperoleh merupakan sebuah *irisan kerucut*, yang telah dipelajari sejak zaman kuno (lihat Kuliah 7).

Isaac Newton mempelajari secara intensif kasus ketika $G(X)$ adalah polinom kubik real, yaitu berderajat tiga. Bahkan bahan contoh ini saja sudah sangat kaya.

![Contoh-contoh kurva eliptik real](authority/assets/ECexamples01-330.png)

Perhatikan kasus $G(X)=X^3$, yaitu objek yang dideskripsikan oleh

$$
\{(x,y)\mid y^2=x^3\}.
$$

Objek ini disebut *parabola Neil*. Di sini muncul fenomena baru: titik asal berbeda dari semua titik lainnya. Kita menyebutnya sebuah *singularitas*; sebaliknya, titik-titik lain disebut *mulus* atau *nonsingular*. Memberikan definisi yang tepat merupakan bagian dari mata kuliah ini. Sebagai rumusan awal yang belum presisi, sebuah kurva di sekitar titik mulus, setelah memilih koordinat yang sesuai, tampak seperti grafik—yang mungkin telah diputar—dari suatu fungsi terdiferensialkan. Singularitas pada parabola Neil juga disebut *titik runcing* atau *kuspa* (kata *cusp* sendiri berarti titik runcing). Sebaliknya, singularitas pada gambar ke-8 adalah *titik perpotongan* atau *titik ganda*.

Pada gambar ke-7 di bagian awal, dan juga pada gambar di atas, kita melihat himpunan nol berbentuk $Y^2=G(X)$ dengan $G(X)$ berderajat tiga. Seperti apakah $G(X)$ agar menghasilkan kurva semacam itu? Contoh-contoh terakhir juga menunjukkan bahwa keberadaan singularitas bergantung pada bentuk tepat $G(X)$.

Mari kita tetap meninjau parabola Neil $C$. Jika $t$ adalah sebarang bilangan real atau kompleks, titik dengan koordinat

$$
(x,y)=(t^2,t^3)
$$

selalu terletak pada parabola Neil, karena $(t^2)^3=t^6=(t^3)^2$. Sebaliknya, dapat pula dibuktikan (lihat [Soal 1.6](https://de.wikiversity.org/wiki/Neilsche_Parabel/Bildbeschreibung_durch_Gleichung/Aufgabe)) bahwa setiap titik pada parabola Neil berbentuk demikian: untuk setiap $(x,y)$ dengan $y^2=x^3$, ada tepat satu $t$ dengan $(x,y)=(t^2,t^3)$. Pemetaan

$$
\mathbb R\longrightarrow C,
\qquad t\longmapsto(t^2,t^3),
$$

disebut *parametrisasi* (polinomial bijektif) dari parabola Neil. Menentukan kurva aljabar mana yang mempunyai parametrisasi polinomial merupakan pertanyaan taktrivial. Kurva mulus berbentuk $Y^2=G(X)$ dengan $\deg G=3$ tidak mempunyai parametrisasi semacam itu. Dalam teori bilangan elementer, kita mempelajari bahwa semua *tripel Pythagoras* dapat ditulis dalam bentuk sederhana yang seragam; lihat [Teorema 10.6 (Teori Bilangan, Osnabrück 2025)](https://de.wikiversity.org/wiki/Pythagoreische_Tripel/Parametrische_Charakterisierung/Fakt). Pernyataan yang ekuivalen adalah adanya parametrisasi rasional lingkaran satuan rasional; lihat [Teorema 10.4](https://de.wikiversity.org/wiki/Einheitskreis/Rationale_Parametrisierung/Fakt). Kita akan membahas hal ini dengan generalitas yang lebih besar dalam [Teorema 7.6](https://de.wikiversity.org/wiki/Quadrik_in_zwei_Variablen/Rationale_Parametrisierung/Fakt).

Sekarang kita sampai pada definisi umum pertama.

### Definisi: kurva aljabar bidang afin {#br-ak-2025-2026-l01-def-01}

Misalkan $K$ suatu medan. Sebuah *kurva aljabar bidang afin* di atas $K$ adalah himpunan nol (*lokus nol*) $V(F)\subseteq K^2$ dari suatu polinom takkonstan $F$ dalam dua variabel, yaitu

$$
F=\sum_{0\le i,j\le m}a_{ij}X^iY^j
\qquad (a_{ij}\in K).
$$

Dengan kata lain,

$$
V(F)=\left\{(x,y)\in K^2\;\middle|\;
F(x,y)=\sum_{0\le i,j\le m}a_{ij}x^iy^j=0\right\}.
$$

Polinom-polinom favorit dalam variabel $X$ dan $Y$ yang disebutkan di kelas adalah:

1. $X^2-Y^2$;
2. $2X+4Y+3$;
3. $X^2+Y^2-3$;
4. $X^2+Y^2$;
5. $5X^2+12Y^2-26$;
6. $3X^2-15Y^2-3$;
7. $X^3+Y^3+XY$;
8. $X^3-4Y^2-XY$;
9. $X^4$;
10. $X^2Y^2-X^2$.

Tingkat kesulitan memahami himpunan nol $V(F)$ yang bersesuaian berbeda-beda. Dengan identitas selisih dua kuadrat,

$$
X^2-Y^2=(X+Y)(X-Y),
$$

dan karena hasil kali dua unsur dalam suatu medan sama dengan nol tepat ketika salah satu faktornya nol, lokus nol ini hanyalah gabungan diagonal utama dan diagonal lainnya: gabungan dua garis afin. Lokus nol $2X+4Y+3$ adalah himpunan solusi persamaan linear itu, yakni sebuah garis afin. Lokus nol real $X^2+Y^2-3$ adalah lingkaran berpusat di titik asal dengan jari-jari $\sqrt3$. Sebaliknya, lokus nol real $X^2+Y^2$ hanya terdiri atas titik asal $(0,0)$; di atas $\mathbb C$ keadaannya berbeda. Lokus nol $5X^2+12Y^2-26$ adalah elips yang sumbunya sejajar sumbu koordinat, sedangkan lokus nol $3X^2-15Y^2-3$ adalah hiperbola yang dimampatkan.

Kita akan membahas dan mengklasifikasikan secara rinci himpunan nol polinom kuadratik pada Kuliah 7. Dua polinom $X^3+Y^3+XY$ dan $X^3-4Y^2-XY$ berderajat $3$ dan jauh lebih sulit dipahami. Pertanyaan pertama adalah apakah kurvanya mulus atau memiliki singularitas. Himpunan nol $V(X^4)$ sama dengan $V(X)$, sehingga merupakan sumbu $y$. Polinom terakhir dapat difaktorkan sebagai

$$
X^2Y^2-X^2=X^2(Y^2-1)=X^2(Y-1)(Y+1),
$$

dan karena itu mudah dipahami. Himpunan nolnya adalah gabungan tiga garis: sumbu $y$ dan dua garis yang sejajar dengan sumbu $x$.

Kita akan membuktikan sebuah lema yang langsung menunjukkan bahwa empat kurva terakhir yang digambarkan di atas bukan kurva aljabar.

### Lema: perpotongan dengan garis {#br-ak-2025-2026-l01-lem-01}

Misalkan $C$ suatu kurva aljabar bidang afin dan $L$ suatu garis di $K^2$.

**Maka $C\cap L$ adalah seluruh garis $L$, atau hanya terdiri atas berhingga banyak titik.**

#### Bukti {#br-ak-2025-2026-l01-lem-01-proof}

Menurut definisi, sebuah kurva aljabar bidang $C=V(F)$ selalu merupakan himpunan nol suatu polinom $F$ dalam dua variabel. Misalkan garis $L$ diberikan oleh persamaan

$$
aX+bY+c=0.
$$

Tanpa mengurangi keumuman, anggap $a\ne0$. Kita dapat menyelesaikan persamaan tersebut terhadap $X$ dan memperoleh $X=\alpha Y+\beta$. Sebuah titik perpotongan $P\in C\cap L$ harus memenuhi $F(P)=0$ sekaligus persamaan garis. Dengan persamaan garis itu, kita dapat mengganti $X$ dalam $F$ dengan $\alpha Y+\beta$. Dengan demikian $F$ menjadi polinom dalam satu variabel $Y$, yang kita namai $\widetilde F$.

Sekarang, $P\in C\cap L$ ekuivalen dengan $P\in L$ dan $\widetilde F(P)=0$. Jadi, himpunan perpotongan dideskripsikan oleh polinom $\widetilde F$. Jika $\widetilde F=0$, seluruh garis merupakan perpotongan. Jika $\widetilde F\ne0$, [Korolari 19.9 (Aljabar Linear, Osnabrück 2024–2025)](https://de.wikiversity.org/wiki/Polynomring_(K%C3%B6rper)/Nullstellen/Anzahl/Fakt) menyatakan bahwa polinom tersebut hanya mempunyai berhingga banyak akar. $\square$

Pada empat contoh nonaljabar di atas, terdapat garis yang memotong kurvanya di tak berhingga banyak titik. Karena itu, kurva-kurva tersebut bukan kurva aljabar.

## Gelanggang polinomial {#br-ak-2025-2026-l01-s03}

Sesudah contoh-contoh pengantar ini, kita menetapkan beberapa istilah yang barangkali sudah dikenal.

### Definisi: gelanggang polinomial dalam satu variabel {#br-ak-2025-2026-l01-def-02}

*Gelanggang polinomial* di atas suatu gelanggang komutatif $R$ terdiri atas semua *polinom*

$$
P=a_0+a_1X+a_2X^2+\cdots+a_nX^n,
$$

dengan $a_i\in R$ untuk $i=0,\ldots,n$ dan $n\in\mathbb N$, dilengkapi penjumlahan per komponen dan perkalian yang didefinisikan dengan memperluas secara distributif aturan

$$
X^n\cdot X^m:=X^{n+m}.
$$

Berdasarkan definisi ini kita juga dapat mendefinisikan gelanggang polinomial dalam beberapa variabel. Kita menetapkan

$$
K[X,Y]:=(K[X])[Y],
\qquad
K[X,Y,Z]:=(K[X,Y])[Z],
$$

dan seterusnya. Sebuah polinom dalam $n$ variabel berbentuk

$$
F=\sum_{(\nu_1,\ldots,\nu_n)}
a_{(\nu_1,\ldots,\nu_n)}X_1^{\nu_1}\cdots X_n^{\nu_n}.
$$

Penjumlahan diambil atas suatu keluarga hingga dari *tupel eksponen* $(\nu_1,\ldots,\nu_n)$. Ungkapan $X_1^{\nu_1}\cdots X_n^{\nu_n}$ juga disebut *monomial*. Biasanya sebuah polinom ditulis ringkas sebagai $F=\sum_\nu a_\nu X^\nu$. Perkalian dua monomial berarti menjumlahkan tupel eksponennya:

$$
\left(X_1^{\nu_1}\cdots X_n^{\nu_n}\right)
\left(X_1^{\mu_1}\cdots X_n^{\mu_n}\right)
:=X_1^{\nu_1+\mu_1}\cdots X_n^{\nu_n+\mu_n}.
$$

Dalam konteks geometri aljabar, kasus yang terutama menarik bagi kita adalah ketika gelanggang dasar $R$ merupakan medan. Geometri aljabar mempelajari bentuk lokus nol polinom dalam beberapa variabel. Kelak kita akan melihat bahwa hubungan antara sifat aljabar dan sifat geometri menjadi sangat kuat apabila medan dasarnya tertutup secara aljabar.

### Definisi: medan tertutup secara aljabar {#br-ak-2025-2026-l01-def-03}

Sebuah medan $K$ disebut *tertutup secara aljabar* jika setiap polinom takkonstan $F\in K[X]$ mempunyai sebuah akar di $K$.

![Carl Friedrich Gauss (1777–1855)](authority/assets/Carl_Friedrich_Gauss.jpg)

Apa yang disebut *teorema dasar aljabar* pertama kali dibuktikan oleh Gauss.

### Teorema: teorema dasar aljabar {#br-ak-2025-2026-l01-thm-01}

Medan bilangan kompleks $\mathbb C$ **tertutup secara aljabar**.

#### Bukti {#br-ak-2025-2026-l01-thm-01-proof}

Kita tidak akan membuktikan teorema ini di sini. Bukti-buktinya menggunakan metode topologis atau analitis. $\square$

---

**Navigasi sumber:** [mata kuliah](https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)) · [Kuliah 2](https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)/Vorlesung_2) · [lembar kerja untuk kuliah ini](https://de.wikiversity.org/wiki/Kurs:Algebraische_Kurven_(Osnabr%C3%BCck_2025-2026)/Arbeitsblatt_1)
