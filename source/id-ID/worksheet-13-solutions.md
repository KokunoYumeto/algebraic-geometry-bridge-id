---
title: "Solusi Publik Lembar Kerja 13"
stable_id: br-ak-2025-2026-w13-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-13/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: f954f09c996c8aa22f94ec826a1503b135a7b4fb9f9e0d5d6ff21f36a519e52a
public_solution_count: 14
upstream_solution_revisions: "Soal 13.3=1023890; 13.6=663088; 13.8=1112836; 13.9=1060069; 13.11=1023327; 13.14=1089391; 13.15=1029221; 13.17=1113410; 13.20=1095814; 13.21=1096486; 13.24=1060010; 13.27=1094892; 13.28=1089663; 13.31=1065090"
solution_xml_sha256: "03=71a4c039de6111f019e2580e0c9af5382450aee092e9e50f34e90368089b1f89; 06=f07fb1df932f9dadf9849fb8a656783d820cb343e5580bd003382cef9788ccac; 08=a2b47f3a63b65b38ae83c5d806aa60fb32a48e8e1d3f083e4f8896e42e61461d; 09=b8ff1918b646eff1d77c8a29cb6b97b6478294e35e0459dc952d3d49a8f7ea6e; 11=752330f95561989915091de492b4cda2fc75710d6b4ee121cef24d62771037a6; 14=d51c295e8174e7ce572b632aee9af39582111d2aa826878d71e420da65da33b0; 15=6e2790855ccbb62268be031dcfbe059c36b0cf4a13a5ad5e129de073975b06ed; 17=59ade099fbf3e862db3d7d0793152278471f697a80a04150e162768452d56e8d; 20=16e9149ead068dc694c59b8ceda85e798cdb480d013ec52bde116005a8581836; 21=34216c74192341aa62c099d3818cd5083057a4a407223dcee4157f894d352639; 24=a369cb91ccbce5c9c5854d7305b2fc8928e73fbfaafd6b5b0dc9f03b970c0c91; 27=f90da5c3fc81eb9c2eebd43131a6d432986c3bb1e0cd363dac6100343b7b3525; 28=7b2e1d5c6d658b72921d28bafef2757bc90683beefcc60091a8028dce3ccbfbd; 31=c1823799d3e16c30f8c13c9ae3ae79ac0ff88c0d89d223d751f1b6c8900bd30d"
license: "CC BY-SA 4.0"
translation_status: complete
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 13 {#br-ak-2025-2026-w13-solutions}

Sumber hanya menyediakan solusi publik untuk Soal 13.3, 13.6, 13.8, 13.9,
13.11, 13.14, 13.15, 13.17, 13.20, 13.21, 13.24, 13.27, 13.28, dan 13.31
pada batas revisi yang dibekukan. Tidak ada solusi tambahan yang dibuat untuk
edisi ini.

<!-- upstream_solution: Rationale Zahlen/Unterringe/Überabzählbar/Aufgabe/Lösung; pageid=86264; revid=1023890 -->
<!-- upstream_solution_revid: 1023890 -->

## Solusi Soal 13.3 {#br-ak-2025-2026-w13-sol-03}

Misalkan $T$ suatu subhimpunan dari himpunan bilangan prima. Karena terdapat
tak hingga banyak bilangan prima, terdapat tak terhitung banyak pilihan
subhimpunan $T$. Kepada $T$ kaitkan sistem multiplikatif $M(T)$ yang terdiri
atas semua bilangan bulat yang dalam faktorisasi primanya hanya mengandung
bilangan prima dari $T$. Pelokalan

$$
\mathbb Z_{M(T)}\subseteq\mathbb Q
$$

terdiri atas semua bilangan rasional yang dapat ditulis dengan penyebut yang
faktorisasi primanya hanya memakai bilangan prima dari $T$. Ketunggalan
faktorisasi prima di $\mathbb Z$ menunjukkan bahwa subgelanggang-subgelanggang
ini berbeda untuk pilihan $T$ yang berbeda.

[Kembali ke Soal 13.3](#br-ak-2025-2026-w13-ex-03).

<!-- upstream_solution: Nenneraufnahme/Universelle Eigenschaft/Fakt/Beweis/Aufgabe/Lösung; pageid=126003; revid=663088 -->
<!-- upstream_solution_revid: 663088 -->

## Solusi Soal 13.6 {#br-ak-2025-2026-w13-sol-06}

Agar diagram homomorfisme gelanggang komutatif, harus berlaku

$$
\widetilde\varphi(1/s)=\varphi(s)^{-1}
$$

untuk $s\in S$, dan karena itu

$$
\widetilde\varphi(a/s)=\varphi(a)\varphi(s)^{-1}.
$$

Jadi paling banyak terdapat satu homomorfisme gelanggang seperti itu, dan
homomorfisme tersebut harus diberikan oleh rumus terakhir.

Kita perlu menunjukkan bahwa rumus ini terdefinisi dengan baik. Misalkan
$a/s=b/t$ dengan $s,t\in S$. Ini berarti terdapat $r\in S$ sehingga
$rta=rsb$. Maka

$$
\varphi(r)\varphi(t)\varphi(a)
=\varphi(r)\varphi(s)\varphi(b).
$$

Dengan mengalikan kedua ruas dengan satuan
$\varphi(r)^{-1}\varphi(t)^{-1}\varphi(s)^{-1}$, diperoleh

$$
\varphi(a)\varphi(s)^{-1}
=\varphi(b)\varphi(t)^{-1}.
$$

Sebagai contoh verifikasi sifat homomorfisme, untuk penjumlahan kita peroleh

$$
\begin{aligned}
\widetilde\varphi\!\left(\frac as+\frac bt\right)
&=\widetilde\varphi\!\left(\frac{at+bs}{st}\right)\\
&=\varphi(at+bs)\varphi(st)^{-1}\\
&=(\varphi(a)\varphi(t)+\varphi(s)\varphi(b))
  \varphi(s)^{-1}\varphi(t)^{-1}\\
&=\varphi(a)\varphi(s)^{-1}+\varphi(b)\varphi(t)^{-1}\\
&=\widetilde\varphi\!\left(\frac as\right)
 +\widetilde\varphi\!\left(\frac bt\right).
\end{aligned}
$$

[Kembali ke Soal 13.6](#br-ak-2025-2026-w13-ex-06).

<!-- upstream_solution: Polynomring zwei Variablen/Multiplikatives System/Eine Gleichung/Verträglichkeit/Aufgabe/Lösung; pageid=21362; revid=1112836 -->
<!-- upstream_solution_revid: 1112836 -->

## Solusi Soal 13.8 {#br-ak-2025-2026-w13-sol-08}

Semua homomorfisme berikut merupakan homomorfisme aljabar-$R$ dan ditentukan
secara tunggal oleh sifat yang dinyatakan. Homomorfisme $R\to R_S$ mula-mula
menginduksi

$$
R/(F)\longrightarrow R_S/(F).
$$

Karena citra $S$ di $R/(F)$ menjadi satuan di $R_S/(F)$, sifat universal
pelokalan memberikan homomorfisme

$$
(R/(F))_S\longrightarrow R_S/(F),
\qquad
\frac{\bar r}{\bar s}\longmapsto\overline{\left(\frac rs\right)}.
$$

Pemetaan ini surjektif: setiap unsur di ruas kanan direpresentasikan oleh
$r/s$ dengan $s\in S$ dan berasal dari $\bar r/\bar s$.

Untuk injektivitas, misalkan $\bar r/\bar s$ dipetakan ke $0$. Maka
$r/s\in(F)R_S$, sehingga $r/s=Fa/t$ untuk suatu $a\in R$ dan $t\in S$.
Dengan menerjemahkan persamaan itu kembali ke $R$, diperoleh

$$
tr=sFa.
$$

Jadi $tr=0$ di $R/(F)$. Karena $t\in S$, hal ini memberikan
$\bar r/\bar s=0$ di $(R/(F))_S$.

[Kembali ke Soal 13.8](#br-ak-2025-2026-w13-ex-08).

<!-- upstream_solution: Nenneraufnahme/Restklassenbildung/Vertauschbarkeit/Fakt/Beweis/Aufgabe/Lösung; pageid=167737; revid=1060069 -->
<!-- upstream_solution_revid: 1060069 -->

## Solusi Soal 13.9 {#br-ak-2025-2026-w13-sol-09}

Homomorfisme gelanggang

$$
R\longrightarrow R_S/\mathfrak aR_S
$$

memetakan $\mathfrak a$ ke $0$ dan karena itu menginduksi homomorfisme

$$
R/\mathfrak a\longrightarrow R_S/\mathfrak aR_S.
$$

Sifat universal pelokalan kemudian menginduksi

$$
(R/\mathfrak a)_S\longrightarrow R_S/\mathfrak aR_S,
\qquad
\frac{[r]}s\longmapsto\left[\frac rs\right].
$$

Rumus ini langsung menunjukkan surjektivitas. Jika
$[r/s]\in\mathfrak aR_S$, maka $r\in\mathfrak aR_S$. Jadi terdapat
$t\in S$ dengan $tr\in\mathfrak a$. Dengan demikian $[tr]=0$ di
$R/\mathfrak a$ dan karenanya $[r]/s=0$ di $(R/\mathfrak a)_S$.
Pemetaan tersebut juga injektif.

[Kembali ke Soal 13.9](#br-ak-2025-2026-w13-ex-09).

<!-- upstream_solution: Hilbertscher Nullstellensatz/Äquivalent/D(f) in D(g)/R g nach R f/Aufgabe/Lösung; pageid=21347; revid=1023327 -->
<!-- upstream_solution_revid: 1023327 -->

## Solusi Soal 13.11 {#br-ak-2025-2026-w13-sol-11}

Jika (2) berlaku, khususnya kita dapat menulis

$$
\frac1g=\frac r{f^n},
\qquad\text{atau setara dengan}\qquad
f^n=rg.
$$

Jadi $g$ membagi suatu pangkat $f$, yakni
$f\in\operatorname{rad}(g)$. Sebaliknya, jika
$f\in\operatorname{rad}(g)$, maka $g$ merupakan satuan di $R_f$ dan sifat
universal pelokalan memberikan homomorfisme aljabar-$R$ $R_g\to R_f$.

Dari $f\in\operatorname{rad}(g)$ langsung diperoleh bahwa $f$ lenyap pada
$V(g)$, sehingga $V(g)\subseteq V(f)$. Jika $K$ tertutup secara aljabar,
implikasi sebaliknya mengikuti dari Nullstellensatz Hilbert. Karena
$D(f)\subseteq D(g)$ ekuivalen dengan $V(g)\subseteq V(f)$, kedua pernyataan
dalam soal ekuivalen.

Untuk $K=\mathbb R$, ambil $R=K[X]$, $f=1$, dan $g=X^2+1$. Polinom $g$
tidak mempunyai akar real, sehingga

$$
V(g)=\varnothing=V(1)
$$

dan $D(f)\subseteq D(g)$, tetapi $g$ bukan satuan di $R_f=R$.

**Catatan edisi:** pada kalimat contoh terakhir, sumber menampilkan
$V(g)=\mathbb A_{\mathbb R}^1=V(1)$. Kedua himpunan nol yang dimaksud adalah
himpunan kosong; relasi himpunan terbukanya tetap seperti di atas.

[Kembali ke Soal 13.11](#br-ak-2025-2026-w13-ex-11).

<!-- upstream_solution: Endlich erzeugte integre K-Algebra/C/Nenneraufnahme/Kein maximales Ideal überlebt/Aufgabe/Lösung; pageid=21586; revid=1089391 -->
<!-- upstream_solution_revid: 1089391 -->

## Solusi Soal 13.14 {#br-ak-2025-2026-w13-sol-14}

Ambil

$$
R=\mathbb C[X,Y]
$$

dan misalkan $S$ sistem multiplikatif yang terdiri atas semua produk unsur
berbentuk $X-a$, $a\in\mathbb C$. Ideal-ideal maksimal di $R$ berbentuk

$$
(X-a,Y-b).
$$

Karena itu setiap ideal maksimal mengandung unsur $S$ dan menjadi ideal
satuan di $R_S$. Namun $R_S$ bukan lapangan: tepat unsur-unsur prima $X-a$
yang dibuat menjadi satuan, sedangkan unsur prima lain, misalnya $Y$, tidak.

[Kembali ke Soal 13.14](#br-ak-2025-2026-w13-ex-14).

<!-- upstream_solution: Integritätsbereich/Zusammenhängend/Aufgabe/Lösung; pageid=126687; revid=1029221 -->
<!-- upstream_solution_revid: 1029221 -->

## Solusi Soal 13.15 {#br-ak-2025-2026-w13-sol-15}

Suatu unsur idempoten $e$ memenuhi

$$
e(1-e)=e-e^2=0.
$$

Di gelanggang tanpa pembagi nol, hal ini mengakibatkan $e=1$ atau $e=0$.

[Kembali ke Soal 13.15](#br-ak-2025-2026-w13-ex-15).

<!-- upstream_solution: Kommutativer Ring/nx und x^n ist 0/Aufgabe/Lösung; pageid=73634; revid=1113410 -->
<!-- upstream_solution_revid: 1113410 -->

## Solusi Soal 13.17 {#br-ak-2025-2026-w13-sol-17}

Tinjau gelanggang kelas residu

$$
R=(\mathbb Z/n\mathbb Z)[X]/(X^n)
$$

dan tuliskan $x$ untuk kelas residu $X$. Unsur $x$ tidak nol, sebab di
gelanggang polinomial $X$ tidak mungkin merupakan kelipatan $X^n$ ketika
$n\ge2$. Di $R$ berlaku $n=0$, sehingga $ny=0$ untuk setiap $y\in R$,
khususnya $nx=0$. Selain itu $x^n=0$ karena seluruh ideal $(X^n)$ dibuat nol
dalam pembentukan gelanggang kelas residu.

[Kembali ke Soal 13.17](#br-ak-2025-2026-w13-ex-17).

<!-- upstream_solution: Z/Restklassenring nach Primelementpotenz/Ist zusammenhängend/Aufgabe/Lösung; pageid=73535; revid=1095814 -->
<!-- upstream_solution_revid: 1095814 -->

## Solusi Soal 13.20 {#br-ak-2025-2026-w13-sol-20}

Misalkan $e\in\mathbb Z/(p^n)$ idempoten. Dengan memilih wakil bilangan
bulatnya, persamaan $e^2=e$ berarti

$$
p^n\mid e(e-1).
$$

Bilangan bulat $e$ dan $e-1$ saling prima, sehingga keduanya tidak mungkin
sama-sama habis dibagi $p$. Karena $p^n$ membagi produknya, seluruh faktor
$p^n$ harus membagi salah satu dari $e$ atau $e-1$. Maka

$$
e=0\quad\text{atau}\quad e=1
$$

di $\mathbb Z/(p^n)$.

**Catatan edisi:** sumber menuliskan faktorisasi $e=bp^i$ dan
$e-1=cp^j$ dengan $i+j=n$. Argumen saling prima di atas menyatakan langkah
yang sama tanpa mengandaikan bahwa valuasi hasil kali tepat $n$.

[Kembali ke Soal 13.20](#br-ak-2025-2026-w13-ex-20).

<!-- upstream_solution: Polynom/Q X modulo X^4-1/Produkt von Körpern/Restklasse von X^3+X/Aufgabe/Lösung; pageid=25988; revid=1096486 -->
<!-- upstream_solution_revid: 1096486 -->

## Solusi Soal 13.21 {#br-ak-2025-2026-w13-sol-21}

Kita mempunyai

$$
X^4-1=(X^2-1)(X^2+1)=(X+1)(X-1)(X^2+1).
$$

Polinom $X^2+1\in\mathbb Q[X]$ tak tereduksi karena tidak mempunyai akar
rasional. Faktor-faktor monik di atas saling tidak berasosiasi. Teorema Sisa
Cina untuk daerah ideal utama memberikan

$$
\begin{aligned}
\mathbb Q[X]/(X^4-1)
&\cong \mathbb Q[X]/(X+1)
\times\mathbb Q[X]/(X-1)
\times\mathbb Q[X]/(X^2+1)\\
&\cong\mathbb Q\times\mathbb Q\times\mathbb Q[\mathrm i].
\end{aligned}
$$

Isomorfisme terakhir memakai substitusi $X\mapsto-1$, $X\mapsto1$, dan
$\mathbb Q[X]/(X^2+1)\cong\mathbb Q[\mathrm i]$. Unsur
$X^3+X=X(X^2+1)$ dipetakan oleh ketiga proyeksi ke $-2$, $2$, dan $0$.
Jadi tupelnya ialah

$$
(-2,2,0).
$$

[Kembali ke Soal 13.21](#br-ak-2025-2026-w13-ex-21).

<!-- upstream_solution: K-Algebren/K-Spektren/Disjunkte Realisierung/Aufgabe/Lösung; pageid=167734; revid=1060010 -->
<!-- upstream_solution_revid: 1060010 -->

## Solusi Soal 13.24 {#br-ak-2025-2026-w13-sol-24}

Tanpa mengurangi keumuman, misalkan $m\ge n$. Kita dapat menulis

$$
B\cong
K[X_1,\ldots,X_m]/
\bigl(\mathfrak b+(X_{n+1},\ldots,X_m)\bigr).
$$

Nyatakan ideal yang diperluas itu dengan $\mathfrak b'$. Dengan demikian
kedua spektrum-$K$ telah direalisasikan sebagai subhimpunan tertutup dari
ruang afin yang sama. Gunakan satu variabel tambahan $Z$ untuk memisahkan
keduanya, dan tinjau

$$
C=
K[X_1,\ldots,X_m,Z]/
\bigl(Z(Z-1),\,Z\mathfrak a,\,(Z-1)\mathfrak b'\bigr).
$$

Spektrum-$K$ dari $C$ merupakan gabungan disjung kedua spektrum yang
diberikan. Memang, himpunan

$$
V=V\bigl(Z(Z-1),\,Z\mathfrak a,\,(Z-1)\mathfrak b'\bigr)
\subseteq\mathbb A_K^{m+1}
$$

memenuhi $Z=0$ atau $Z=1$. Bagian $Z=0$ adalah

$$
\begin{aligned}
V_0
&=V\bigl(Z,\mathfrak b'\bigr)\\
&\cong
K\!-\!\operatorname{Spek}
\left(K[X_1,\ldots,X_m,Z]/(Z,\mathfrak b')\right)\\
&\cong K\!-\!\operatorname{Spek}(B),
\end{aligned}
$$

sedangkan bagian $Z=1$ adalah

$$
\begin{aligned}
V_1
&=V\bigl(Z-1,\mathfrak a\bigr)\\
&\cong
K\!-\!\operatorname{Spek}
\left(K[X_1,\ldots,X_m,Z]/(Z-1,\mathfrak a)\right)\\
&\cong K\!-\!\operatorname{Spek}(A).
\end{aligned}
$$

[Kembali ke Soal 13.24](#br-ak-2025-2026-w13-ex-24).

<!-- upstream_solution: Idempotente Elemente/Reduktion/Injektiv/Aufgabe/Lösung; pageid=94590; revid=1094892 -->
<!-- upstream_solution_revid: 1094892 -->

## Solusi Soal 13.27 {#br-ak-2025-2026-w13-sol-27}

Misalkan $e,f\in R$ idempoten dan citranya di dalam reduksi sama. Maka
$e-f$ nilpoten di $R$. Jadi terdapat $n\in\mathbb N$ dengan

$$
(e-f)^n=0.
$$

Kita boleh mengambil $n$ ganjil. Dengan teorema binomial, simetri koefisien
binomial, dan sifat idempoten, diperoleh

$$
\begin{aligned}
0=(e-f)^n
&=e^n-f^n+
\sum_{k=1}^{n-1}\binom nk e^kf^{n-k}\\
&=e-f+
\sum_{k=1}^{(n-1)/2}\binom nk
\left(e^kf^{n-k}-e^{n-k}f^k\right)\\
&=e-f+
\sum_{k=1}^{(n-1)/2}\binom nk(ef-ef)\\
&=e-f.
\end{aligned}
$$

Maka $e=f$.

[Kembali ke Soal 13.27](#br-ak-2025-2026-w13-ex-27).

<!-- upstream_solution: Idempotente Elemente/Modulo nilpotentes Element/Surjektiv/Aufgabe/Lösung; pageid=94592; revid=1089663 -->
<!-- upstream_solution_revid: 1089663 -->

## Solusi Soal 13.28 {#br-ak-2025-2026-w13-sol-28}

Ambil praimaj $f\in R$ dari $e$. Karena $e$ idempoten, unsur

$$
c=f^2-f
$$

terletak di $(n)$, sehingga $c^2=0$. Tinjau

$$
g=f+c-2cf.
$$

Unsur ini juga dipetakan ke $e$. Selain itu,

$$
\begin{aligned}
g^2
&=(f+c-2cf)^2\\
&=f^2+c^2+4c^2f^2+2cf-4cf^2-4c^2f\\
&=f^2+2cf-4cf^2\\
&=f+c+2cf-4c(f+c)\\
&=f+c+2cf-4cf\\
&=f+c-2cf\\
&=g.
\end{aligned}
$$

Jadi $g$ adalah praimaj idempoten dari $e$.

[Kembali ke Soal 13.28](#br-ak-2025-2026-w13-ex-28).

<!-- upstream_solution: Kommutativer Ring/Ideal/Teilerfremd/Chinesischer Restsatz/Fakt/Beweis/Aufgabe/Lösung; pageid=168189; revid=1065090 -->
<!-- upstream_solution_revid: 1065090 -->

## Solusi Soal 13.31 {#br-ak-2025-2026-w13-sol-31}

Kasus umum mengikuti dari kasus $n=2$, jadi cukup tinjau dua ideal
$\mathfrak a$ dan $\mathfrak b$. Pemetaan alami

$$
R\longrightarrow R/\mathfrak a\times R/\mathfrak b
$$

mempunyai kernel $\mathfrak a\cap\mathfrak b$. Untuk ideal yang saling
komaksimal, irisan ini sama dengan hasil kali
$\mathfrak a\mathfrak b$. Maka kita memperoleh homomorfisme gelanggang
injektif

$$
R/(\mathfrak a\mathfrak b)
\longrightarrow R/\mathfrak a\times R/\mathfrak b.
$$

Untuk membuktikan surjektivitas, ambil $(r,s)$ di ruas kanan. Pilih
$a\in\mathfrak a$ dan $b\in\mathfrak b$ dengan $a+b=1$. Unsur

$$
r-ar+s-sb
$$

merupakan praimaj $(r,s)$. Modulo $\mathfrak a$, unsur itu menjadi

$$
r-ar+s-sb=r+s-s(1-a)=r,
$$

dan secara serupa modulo $\mathfrak b$ ia menjadi $s$.

[Kembali ke Soal 13.31](#br-ak-2025-2026-w13-ex-31).
