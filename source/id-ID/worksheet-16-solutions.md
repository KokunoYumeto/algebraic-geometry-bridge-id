---
title: "Solusi Publik Lembar Kerja 16"
stable_id: br-ak-2025-2026-w16-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-16/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: 835029f5f5f46dea23486bd62edec6f4ab64667192c44504fee3af259e5b5266
public_solution_count: 6
upstream_solution_revisions: "Soal 16.1=1068100; Soal 16.10=1067953; Soal 16.11=1094645; Soal 16.12=1112750; Soal 16.13=1089809; Soal 16.15=1096228"
solution_xml_sha256: "01=420fa066280c15a83372541ece706d0e5ec995f1aa1c0266510da72582beda97; 10=730f7926be80a253bc8167f3f349a66e788ac8d689437791490bf93d68c8d797; 11=98d614f4acfbf8dcaea8e637ad6a18375546274f6d4ee20df9163ebe46e7de0a; 12=4cbfdb0498bda3335528ebd078b592eea736da509ed6f0be8e6ce4f4b8b9cc61; 13=b5e3335a35c26d85b544cd4a755256ba1696af3f1d766495f4239d1a7c739a62; 15=41008ef3351d2d28fb88f1c1c2fb3e1b3580ddc40884547a7bb4ddaf0995d248"
license: "CC BY-SA 4.0; the image in Solution 16.12 remains CC BY-SA 3.0"
translation_status: complete
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 16 {#br-ak-2025-2026-w16-solutions}

Pada batas revisi yang dibekukan, sumber hanya menyediakan solusi publik
untuk Soal 16.1, 16.10, 16.11, 16.12, 16.13, dan 16.15. Tidak ada solusi
tambahan yang dibuat untuk edisi ini. Solusi 16.13 dipertahankan sampai batas
yang benar-benar tersedia di sumber; batas itu dijelaskan pada tempatnya.

<!-- upstream_solution: Zariski-Filter/Irreduzibler Filter ist durch D(f) bestimmt/Aufgabe/Lösung; pageid=168442; revid=1068100 -->
<!-- upstream_solution_revid: 1068100 -->

## Solusi Soal 16.1 {#br-ak-2025-2026-w16-sol-01}

Misalkan $F$ filter tak tereduksi. Untuk setiap $U\in F$, tuliskan

$$
U=D(f_1)\cup\cdots\cup D(f_k).
$$

Karena $F$ tak tereduksi, setidaknya satu $D(f_i)$ berada di $F$. Karena

$$
D(f_i)\subseteq U,
$$

himpunan-himpunan terbuka berbentuk $D(f)$ yang berada di $F$ membangkitkan
filter tersebut.

[Kembali ke Soal 16.1](#br-ak-2025-2026-w16-ex-01).

<!-- upstream_solution: K-Spektrum/Bijektiv stetig, nicht homöomorph/Aufgabe/Lösung; pageid=168403; revid=1067953 -->
<!-- upstream_solution_revid: 1067953 -->

## Solusi Soal 16.10 {#br-ak-2025-2026-w16-sol-10}

Tinjau garis afin $\mathbb A_K^1$ dan garis tertusuk

$$
Y=\mathbb A_K^1\setminus\{0\},
$$

yang merupakan varietas afin karena dapat direalisasikan sebagai hiperbola.
Tinjau gabungan saling lepas

$$
Z=Y\uplus\{P\}
$$

dengan satu titik tambahan. Terdapat morfisme alami

$$
Z\longrightarrow\mathbb A_K^1
$$

yang pada $Y$ merupakan inklusi terbuka dan memetakan $P$ ke titik nol.
Pemetaan ini bijektif. Akan tetapi, $\{P\}$ terbuka di sisi kiri dan tidak
terbuka di sisi kanan. Jadi pemetaan inversnya tidak kontinu.

[Kembali ke Soal 16.10](#br-ak-2025-2026-w16-ex-10).

<!-- upstream_solution: Einheitskreis/Punktepaar/Automorphismus/Aufgabe/Lösung; pageid=95397; revid=1094645 -->
<!-- upstream_solution_revid: 1094645 -->

## Solusi Soal 16.11 {#br-ak-2025-2026-w16-sol-11}

Cukup diberikan, bagi titik $(1,0)$ dan $P=(a,b)\in V$, suatu automorfisme
lingkaran yang membawa $(1,0)$ ke $P$. Automorfisme yang diminta dari $P$ ke
$Q$ kemudian diperoleh sebagai komposisi pemetaan-pemetaan semacam itu dan,
bila perlu, inversnya.

Tinjau pemetaan linear bijektif

$$
\varphi:K^2\longrightarrow K^2
$$

yang diberikan oleh matriks

$$
\begin{pmatrix}
a&-b\\
b&a
\end{pmatrix}.
$$

Pemetaan ini membawa $(1,0)$ ke $(a,b)$. Suatu titik $(x,y)\in V$ dipetakan
ke

$$
(ax-by,bx+ay).
$$

Untuk titik citra berlaku

$$
\begin{aligned}
(ax-by)^2+(bx+ay)^2
&=a^2x^2-2abxy+b^2y^2+b^2x^2+2abxy+a^2y^2\\
&=(a^2+b^2)x^2+(a^2+b^2)y^2\\
&=x^2+y^2\\
&=1.
\end{aligned}
$$

Jadi titik citra kembali berada pada lingkaran dan $\varphi$ menginduksi
pemetaan aljabar $V\to V$. Pemetaan linear dengan matriks

$$
\begin{pmatrix}
a&b\\
-b&a
\end{pmatrix}
$$

memberikan morfisme invers. Dengan demikian diperoleh automorfisme.

**Catatan edisi:** pada suku kedua ruas pertama perhitungan, sumber menulis
$(bx+ax)^2$. Pemetaan yang baru saja didefinisikan dan ekspansi pada baris
berikutnya sama-sama menuntut $(bx+ay)^2$, yang ditampilkan di sini.

[Kembali ke Soal 16.11](#br-ak-2025-2026-w16-ex-11).

<!-- upstream_solution: Achsenkreuz/Drei Geraden in Ebene/Beziehung/Aufgabe/Lösung; pageid=95122; revid=1112750 -->
<!-- upstream_solution_revid: 1112750 -->

## Solusi Soal 16.12 {#br-ak-2025-2026-w16-sol-12}

1. Kita mempunyai

   $$
   V=V(XY,XZ,YZ)
   =V(X,Y)\cup V(X,Z)\cup V(Y,Z),
   $$

   yakni gabungan ketiga sumbu koordinat di ruang afin tiga dimensi.

   ![Tiga sumbu koordinat yang berpotongan di titik asal](authority/assets/Draft0-500.png)

   *Sketsa gabungan ketiga sumbu koordinat. Kalan,
   [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). Rincian
   sumber berada pada kredit media Unit 16.*

   **Catatan edisi:** sumber menampilkan
   $V(XY)\cup V(XZ)\cup V(YZ)$ pada ruas kanan. Gabungan itu bukan himpunan
   nol bersama ketiga polinomial dan bukan hanya ketiga sumbu. Edisi ini
   menampilkan dekomposisi komponen yang sesuai dengan ruas kiri dan dengan
   kalimat sumber sesudahnya.

2. Pemetaan linear

   $$
   K^3\longrightarrow K^2
   $$

   yang, terhadap basis standar, diberikan oleh matriks

   $$
   \begin{pmatrix}
   1&0&1\\
   0&1&1
   \end{pmatrix}
   $$

   adalah identitas pada bidang $XY$ dan membawa sumbu $Z$ ke diagonal utama
   bidang tersebut. Karena itu citra gabungan sumbu seluruhnya berada dalam

   $$
   W=V(ST(S-T)),
   $$

   sehingga diperoleh morfisme

   $$
   \varphi:V\longrightarrow W.
   $$

   Morfisme ini bijektif karena setiap garis yang terlibat dipetakan secara
   bijektif ke salah satu garis.

3. Secara aljabar terdapat homomorfisme aljabar-$K$

   $$
   K[S,T]/(ST(S-T))
   \longrightarrow
   K[X,Y,Z]/(XY,XZ,YZ),
   $$

   dengan

   $$
   S\longmapsto X+Z,
   \qquad
   T\longmapsto Y+Z.
   $$

   Homomorfisme ini menginduksi homomorfisme pelokalan

   $$
   \bigl(K[S,T]/(ST(S-T))\bigr)_{S+T}
   \longrightarrow
   \bigl(K[X,Y,Z]/(XY,XZ,YZ)\bigr)_{X+Y+2Z}.
   $$

   Irisan $V(S+T)$, maupun $V(X+Y+2Z)$, dengan masing-masing dari ketiga
   garis hanya terdiri atas titik asal, dengan menggunakan bahwa
   $\operatorname{char}(K)\ne2$. Karena itu kedua pelokalan menggambarkan
   komplemen titik asal.

   Dengan variabel

   $$
   A=X+Z,
   \qquad
   B=Y+Z,
   $$

   gelanggang di ruas kanan dapat ditulis

   $$
   K[A,B,Z,(A+B)^{-1}]
   \big/
   \bigl((A-Z)Z,(B-Z)Z,(A-Z)(B-Z)\bigr).
   $$

   Di dalam gelanggang ini,

   $$
   \begin{aligned}
   2AB
   &=2Z(A+B)-2Z^2\\
   &=2Z(A+B)-AZ-BZ\\
   &=Z(A+B),
   \end{aligned}
   $$

   sehingga

   $$
   Z=\frac{2AB}{A+B}.
   $$

   Jadi $Z$ dapat dieliminasi. Karena

   $$
   A-Z
   =A-\frac{2AB}{A+B}
   =\frac{A^2-AB}{A+B},
   $$

   pembangkit-pembangkit ideal berubah menjadi

   $$
   (A-Z)Z
   =\frac{2A^2B(A-B)}{(A+B)^2},
   $$

   $$
   (B-Z)Z
   =-\frac{2AB^2(A-B)}{(A+B)^2},
   $$

   dan

   $$
   \begin{aligned}
   (A-Z)(B-Z)
   &=\frac{A^2-AB}{A+B}\,
     \frac{B^2-AB}{A+B}\\
   &=\frac{2A^2B^2-AB^3-A^3B}{(A+B)^2}.
   \end{aligned}
   $$

   **Catatan edisi:** sumber mencetak tanda positif di depan pecahan untuk
   $(B-Z)Z$. Substitusi yang ditampilkan memberi tanda negatif. Perubahan
   tanda tidak mengubah ideal yang dibangkitkan, tetapi kesamaan aljabarnya
   ditampilkan dengan tanda yang benar di sini.

   Karena $A+B$ dan $2$ merupakan satuan, kedua pembangkit pertama memberikan

   $$
   A^3B=A^2B^2=AB^3,
   $$

   sehingga pembangkit ketiga berlebihan. Selain itu,

   $$
   AB(A-B)(A+B)=AB(A^2-B^2)
   $$

   berada dalam ideal. Karena $A+B$ satuan, $AB(A-B)$ juga berada dalam
   ideal; sebaliknya unsur itu membangkitkan ideal yang sama. Jadi pemetaan
   yang diberikan oleh $S\mapsto A$ dan $T\mapsto B$ merupakan isomorfisme
   pada komplemen titik asal.

[Kembali ke Soal 16.12](#br-ak-2025-2026-w16-ex-12).

<!-- upstream_solution: Kreisgleichung/Morphismus/2 zu 1/Aufgabe/Lösung; pageid=95083; revid=1089809 -->
<!-- upstream_solution_revid: 1089809 -->

## Solusi Soal 16.13 {#br-ak-2025-2026-w16-sol-13}

Terdapat morfisme

$$
V(Z^2+W^2-1)\longrightarrow\mathbb A_K^2.
$$

Jadi cukup diperiksa bahwa citranya memenuhi persamaan lingkaran. Memang,

$$
\begin{aligned}
X^2+Y^2
&=(Z^2-W^2)^2+4Z^2W^2\\
&=(Z^2-(1-Z^2))^2+4Z^2(1-Z^2)\\
&=(2Z^2-1)^2+4Z^2(1-Z^2)\\
&=4Z^4-4Z^2+1+4Z^2-4Z^4\\
&=1.
\end{aligned}
$$

**Batas solusi sumber:** solusi publik yang dibekukan berhenti setelah
membuktikan bahwa citra memenuhi persamaan lingkaran. Ia tidak membuktikan
pernyataan kedua soal bahwa setiap serat terdiri atas dua titik. Edisi ini
tidak mengarang kelanjutan yang tidak tersedia di sumber.

[Kembali ke Soal 16.13](#br-ak-2025-2026-w16-ex-13).

<!-- upstream_solution: Gruppenvarietät/K-Algebra Homomorphismus für Addition/Aufgabe/Lösung; pageid=21349; revid=1096228 -->
<!-- upstream_solution_revid: 1096228 -->

## Solusi Soal 16.15 {#br-ak-2025-2026-w16-sol-15}

Tinjau homomorfisme substitusi

$$
\begin{aligned}
K[X]&\longrightarrow K[Y,Z],\\
X&\longmapsto Y+Z.
\end{aligned}
$$

Pemetaan spektrum yang diinduksi adalah

$$
\begin{aligned}
\mathbb A_K^2\cong K^2&\longrightarrow\mathbb A_K^1\cong K,\\
(y,z)&\longmapsto y+z.
\end{aligned}
$$

Ini tepat merupakan operasi penjumlahan pada $K$.

[Kembali ke Soal 16.15](#br-ak-2025-2026-w16-ex-15).
