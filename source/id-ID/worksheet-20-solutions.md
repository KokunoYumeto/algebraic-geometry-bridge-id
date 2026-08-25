---
title: "Solusi Publik Lembar Kerja 20"
stable_id: br-ak-2025-2026-w20-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-20/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: c74da7b0627cf8c8c694c0a9f20e94b0c7dc00ecd6c95b72ad21ae4a6c5c07ea
public_solution_count: 8
upstream_solution_revisions: "Soal 20.1=612937; Soal 20.3=1113196; Soal 20.4=1054377; Soal 20.5=1090115; Soal 20.12=1112402; Soal 20.13=1095226; Soal 20.14=1096447; Soal 20.17=1096446"
solution_xml_sha256: "01=adde79e2be2fd065988d87a4679d4b1da19c7adc757b2a3359a8d724c6b013b0; 03=94c1fde92ccb9f23400663f673eafa555e7194c89a9427f11c3c9cfed923df66; 04=804783e2895604f6748c0e47fa40799d384a5c5c3eea9488557c93954acf6a54; 05=32953ecdbf24d53fdd469f25c78110aee88485b4b3f7877429e30097a6139b9a; 12=96f81c667ecc03e7e8685821049a66aa24146255456d281e92d8ffe6a0b85b76; 13=801eb06d552df3563f8e70d53fa673fad0e0e88ee2c35b959c366c25fbf14af4; 14=fd17e6d973a3b495694a25b252368ebffd43cf66cdb4d236707638f658c53b9b; 17=116baccffca81eab52df1ee1a543d4d982c63359f24de407a13cbbd4a7fb318c"
transcluded_proof_revisions: "Soal 20.1=1108353; Soal 20.4=1101325"
transcluded_proof_xml_sha256: "01=2af64ad5502d186551fbe405a788f7ac04384bc68a8e0652f6675f92311918e9; 04=045c7318d21d5469bf7ab7f4b368fbcb469292746db573f737bf00b65b2f2a4d"
license: "CC BY-SA 4.0"
translation_status: complete
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 20 {#br-ak-2025-2026-w20-solutions}

Pada batas revisi yang dibekukan, sumber hanya menyediakan solusi publik
untuk Soal 20.1, 20.3, 20.4, 20.5, 20.12, 20.13, 20.14, dan 20.17. Solusi
untuk Soal 20.1 dan 20.4 berupa halaman pembungkus yang mentransklusikan
tubuh bukti terpisah; edisi ini memuat tubuh bukti beku tersebut secara
lengkap. Tidak ada solusi tambahan yang dibuat untuk edisi ini.

<!-- upstream_solution: Quadratwurzel/2/Irrational/Fakt/Beweis/Aufgabe/Lösung; pageid=114792; revid=612937 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=612937 -->
<!-- upstream_transcluded_proof: Quadratwurzel/2/Irrational/Fakt/Beweis; pageid=111327; revid=1108353 -->
<!-- upstream_transcluded_proof_url: https://de.wikiversity.org/w/index.php?oldid=1108353 -->

## Solusi Soal 20.1 {#br-ak-2025-2026-w20-sol-01}

Kita andaikan bahwa ada bilangan rasional yang kuadratnya sama dengan $2$,
lalu menurunkan suatu kontradiksi. Jadi, misalkan

$$
x\in\mathbb Q
$$

dan

$$
x^2=2.
$$

Setiap bilangan rasional dapat ditulis sebagai pecahan dengan pembilang dan
penyebut bilangan bulat. Karena itu, kita dapat menulis

$$
x=\frac ab.
$$

Kita juga dapat mengandaikan bahwa pecahan ini telah disederhanakan, sehingga
$a$ dan $b$ tidak mempunyai pembagi bersama selain satu. Pilihan ini hanya
menyederhanakan penyajian dan bukan asumsi yang hendak dibantah. Sebenarnya,
kita hanya memerlukan bahwa sekurang-kurangnya salah satu dari $a$ dan $b$
ganjil; jika keduanya genap, kita dapat membagi keduanya dengan $2$, dan
melanjutkan demikian bila perlu.

Persamaan $x^2=2$ berarti

$$
x^2=\left(\frac ab\right)^2=\frac{a^2}{b^2}=2.
$$

Dengan mengalikan persamaan ini dengan $b^2$, kita memperoleh persamaan dalam
$\mathbb Z$,

$$
2b^2=a^2.
$$

Jadi $a^2$ genap, karena merupakan kelipatan $2$. Akibatnya, $a$ sendiri
genap, sebab kuadrat bilangan ganjil tetap ganjil. Maka kita dapat menulis

$$
a=2c
$$

untuk suatu $c\in\mathbb Z$. Substitusi ke persamaan di atas memberikan

$$
2b^2=(2c)^2=2^2c^2.
$$

Setelah membagi dengan $2$, kita memperoleh

$$
b^2=2c^2.
$$

Dengan alasan yang sama, $b^2$, dan karenanya $b$, juga genap. Hal ini
bertentangan dengan pilihan bahwa $a$ dan $b$ tidak keduanya genap.

[Kembali ke Soal 20.1](#br-ak-2025-2026-w20-ex-01).

<!-- upstream_solution: Primfaktorzerlegung/3 Wurzel 9/Irrational/Aufgabe/Lösung; pageid=25178; revid=1113196 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1113196 -->

## Solusi Soal 20.3 {#br-ak-2025-2026-w20-sol-03}

Andaikan terdapat penyajian

$$
9^{1/3}=\frac ab
$$

dengan $a,b\in\mathbb N_+$. Jika $a$ dan $b$ mempunyai pembagi bersama yang
sekurang-kurangnya $2$, kita dapat menyederhanakan pecahan itu. Karena itu,
kita boleh mengandaikan bahwa $a$ dan $b$ saling prima. Dengan mengambil
pangkat tiga dari persamaan awal, kita memperoleh

$$
9=\frac{a^3}{b^3},
$$

atau

$$
3^2b^3=a^3.
$$

Bilangan ini mempunyai faktorisasi prima yang unik. Karena $3$ muncul di
dalamnya, berlaku $3\mid a^3$, dan karena $3$ prima, juga $3\mid a$. Jadi
eksponen $3$ pada faktorisasi prima ruas kanan sekurang-kurangnya $3$.
Sebaliknya, karena $a$ dan $b$ saling prima, $b$ tidak habis dibagi $3$;
eksponen $3$ pada ruas kiri tepat $2$. Ini merupakan kontradiksi.

[Kembali ke Soal 20.3](#br-ak-2025-2026-w20-ex-03).

<!-- upstream_solution: Kommutative Ringtheorie/Z ist normal/Wurzeln aus ganzen Zahlen sind irrational/Fakt/Beweis/Aufgabe/Lösung; pageid=166918; revid=1054377 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1054377 -->
<!-- upstream_transcluded_proof: Kommutative Ringtheorie/Z ist normal/Wurzeln aus ganzen Zahlen sind irrational/Fakt/Beweis; pageid=14442; revid=1101325 -->
<!-- upstream_transcluded_proof_url: https://de.wikiversity.org/w/index.php?oldid=1101325 -->

## Solusi Soal 20.4 {#br-ak-2025-2026-w20-sol-04}

Bilangan

$$
n=p_1^{\alpha_1}\cdots p_r^{\alpha_r}
$$

tidak dapat mempunyai akar pangkat $k$ di $\mathbb Z$, sebab dalam suatu
pangkat ke-$k$ semua eksponen pada faktor-faktor prima merupakan kelipatan
$k$, sedangkan menurut asumsi hal itu tidak berlaku bagi semua $\alpha_i$.

Karena $\mathbb Z$ merupakan domain faktorisasi tunggal, ia normal. Oleh
karena itu, tidak mungkin pula ada

$$
x\in Q(\mathbb Z)=\mathbb Q
$$

dengan

$$
x^k=n.
$$

Jadi bilangan real $n^{1/k}$ irasional.

[Kembali ke Soal 20.4](#br-ak-2025-2026-w20-ex-04).

<!-- upstream_solution: Normaler integrer Ring/Nenneraufnahme an einem Element ist normal/Aufgabe/Lösung; pageid=21367; revid=1090115 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1090115 -->

## Solusi Soal 20.5 {#br-ak-2025-2026-w20-sol-05}

Misalkan

$$
q\in Q(R)=Q(R_f)
$$

merupakan unsur dalam lapangan pecahan dan memenuhi suatu persamaan
keintegralan atas $R_f$. Jadi terdapat persamaan

$$
q^n+g_{n-1}q^{n-1}+\cdots+g_1q+g_0=0,
\qquad g_i\in R_f.
$$

Setiap $g_i$ dapat ditulis sebagai pecahan yang penyebutnya merupakan suatu
pangkat dari $f$. Kita dapat memilih satu pangkat tetap $f^k$ sebagai
penyebut bersama. Dengan memperbesar $k$ bila perlu, kita juga boleh
mengandaikan bahwa $k$ merupakan kelipatan $n$.

Kita kalikan persamaan tersebut dengan $f^{kn}$ dan memperoleh

$$
(f^kq)^n
+g_{n-1}f^k(f^kq)^{n-1}
+\cdots
+g_1f^{k(n-1)}(f^kq)
+f^{kn}g_0=0.
$$

Semua koefisien dalam persamaan ini berada di $R$. Jadi persamaan tersebut
merupakan persamaan keintegralan untuk $f^kq$ atas $R$. Karena $R$ normal,
kita memperoleh $f^kq\in R$, dan dengan demikian

$$
q=\frac b{f^k}\in R_f
$$

untuk suatu $b\in R$. Jadi pelokalan $R_f$ juga normal.

[Kembali ke Soal 20.5](#br-ak-2025-2026-w20-ex-05).

<!-- upstream_solution: Y^2-X^4/Monoidring/Aufgabe/Lösung; pageid=95141; revid=1112402 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1112402 -->

## Solusi Soal 20.12 {#br-ak-2025-2026-w20-sol-12}

1. Kita mempunyai

   $$
   Y^2-X^4=(Y-X^2)(Y+X^2),
   $$

   sehingga kurva tersebut tereduksi.

2. Tinjau monoid $M$ dengan dua pembangkit $e,f$ dan satu-satunya relasi

   $$
   2f=4e.
   $$

   Maka

   $$
   \mathbb C[M]\cong\mathbb C[X,Y]/(Y^2-X^4).
   $$

3. Ambil

   $$
   e=(1,1)\in\mathbb N\times\mathbb Z/(2)
   $$

   dan

   $$
   f=(2,1)\in\mathbb N\times\mathbb Z/(2).
   $$

   Berlaku $2f=4e$. Semua relasi lain merupakan kelipatan relasi ini. Memang,
   jika

   $$
   af=be,
   \qquad a,b\in\mathbb N,
   $$

   maka perbandingan koordinat pertama memberikan $b=2a$, sedangkan
   perbandingan koordinat kedua mengharuskan $a$ genap.

[Kembali ke Soal 20.12](#br-ak-2025-2026-w20-ex-12).

<!-- upstream_solution: Monoid/Einheit/Teilmenge von NxZ mod n/Aufgabe/Lösung; pageid=95147; revid=1095226 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1095226 -->

## Solusi Soal 20.13 {#br-ak-2025-2026-w20-sol-13}

Misalkan

$$
m=(r,s)\in M.
$$

Jika $m$ merupakan satuan di $M$, maka tentu ia juga merupakan satuan di
$\mathbb N\times\mathbb Z/(n)$, sebab inversnya di $M$ juga berada di monoid
yang lebih besar itu.

Sebaliknya, misalkan $m$ merupakan satuan di
$\mathbb N\times\mathbb Z/(n)$. Pertama-tama harus berlaku $r=0$. Untuk

$$
m=(0,s),
\qquad 0\leq s<n,
$$

inversnya di $\mathbb N\times\mathbb Z/(n)$ adalah

$$
(0,n-s)=(0,-s).
$$

Namun

$$
(n-1)(0,s)=(0,(n-1)s)=(0,-s).
$$

Karena $(0,s)\in M$ dan $M$ tertutup terhadap penjumlahan, unsur invers ini
juga berada di $M$. Jadi $m$ merupakan satuan di $M$.

[Kembali ke Soal 20.13](#br-ak-2025-2026-w20-ex-13).

<!-- upstream_solution: NxZ mod n/C/Komponenten/Aufgabe/Lösung; pageid=95161; revid=1096447 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1096447 -->

## Solusi Soal 20.14 {#br-ak-2025-2026-w20-sol-14}

Kita mempunyai

$$
\begin{aligned}
\mathbb C[M]
&\cong \mathbb C[S,T]/(S^n-1)\\
&\cong \mathbb C[T][S]/(S^n-1)\\
&\cong \mathbb C[T][S]\Big/\left(\prod_{\zeta^n=1}(S-\zeta)\right)\\
&\cong \left(\mathbb C[S]\Big/\left(\prod_{\zeta^n=1}(S-\zeta)\right)\right)[T],
\end{aligned}
$$

dengan $\zeta$ menjelajahi semua $n$ akar satuan kompleks. Selanjutnya,

$$
\mathbb C[S]\Big/\left(\prod_{\zeta^n=1}(S-\zeta)\right)
\cong\mathbb C^n,
$$

dengan isomorfisme yang diberikan oleh

$$
S\longmapsto(\zeta_0,\zeta_1,\ldots,\zeta_{n-1}).
$$

Akibatnya,

$$
\left(\mathbb C[S]\Big/\left(\prod_{\zeta^n=1}(S-\zeta)\right)\right)[T]
\cong\mathbb C^n[T]
\cong(\mathbb C[T])^n
$$

merupakan gelanggang produk dari $n$ gelanggang polinomial $\mathbb C[T]$.
Oleh karena itu, spektrum-$\mathbb C$ gelanggang ini merupakan gabungan
terpisah dari $n$ salinan

$$
\operatorname{Spec}_{\mathbb C}(\mathbb C[T])
\cong\mathbb A^1_{\mathbb C}.
$$

Setiap garis afin tersebut tak tereduksi.

**Catatan edisi:** dalam ketiga hasil kali, sumber memakai indeks dummy
$\eta$ pada $\prod_\eta(S-\zeta)$, sedangkan faktor dan kalimat penjelas
memakai $\zeta$. Edisi ini menyeragamkan indeksnya secara transparan menjadi
$\prod_{\zeta^n=1}(S-\zeta)$.

[Kembali ke Soal 20.14](#br-ak-2025-2026-w20-ex-14).

<!-- upstream_solution: Numerisches Monoid/Singularitätsgrad/Ringkette/Aufgabe/Lösung; pageid=95576; revid=1096446 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1096446 -->

## Solusi Soal 20.17 {#br-ak-2025-2026-w20-sol-17}

Derajat singularitas $\delta$ adalah banyaknya celah $M$ di dalam
$\mathbb N$. Nilai ini sama dengan

$$
\dim_K(R^{\mathrm{norm}}/R)
=\dim_K(K[T]/K[M]).
$$

1. Dalam suatu rantai monoid

   $$
   M=M_0\subsetneq M_1\subsetneq M_2\subsetneq\cdots
   \subsetneq M_n=\mathbb N,
   $$

   sekurang-kurangnya satu unsur harus ditambahkan pada setiap langkah.
   Karena itu, $n\leq\delta$. Sebaliknya, definisikan $M_{i+1}$ secara
   berturut-turut dengan menambahkan ke $M_i$ unsur terbesar yang belum
   berada di $M_i$. Hasilnya tetap sebuah monoid dan mempunyai tepat satu
   unsur lebih banyak daripada $M_i$. Prosedur ini menghasilkan rantai
   sepanjang $\delta$, seperti yang diinginkan.

2. Rantai sepanjang $\delta$ tersebut menghasilkan rantai aljabar-$K$

   $$
   K[M]=K[M_0]\subsetneq K[M_1]\subsetneq K[M_2]\subsetneq\cdots
   \subsetneq K[M_\delta]=K[\mathbb N].
   $$

   Semua inklusi itu ketat: jika
   $m\in M_{i+1}\setminus M_i$, maka

   $$
   T^m\in K[M_{i+1}]\setminus K[M_i].
   $$

   Bagian berikut memberikan alasan umum bahwa tidak ada rantai yang lebih
   panjang.

3. Rantai aljabar pada bagian 2 khususnya merupakan rantai subruang vektor
   atas $K$. Karena

   $$
   \dim_K(K[\mathbb N]/K[M])=\delta,
   $$

   tidak mungkin ada rantai subruang vektor yang lebih panjang: rantai
   tersebut berkorespondensi dengan rantai di ruang faktor
   $K[\mathbb N]/K[M]$, sedangkan dalam ruang vektor berdimensi $\delta$,
   panjang maksimum rantai inklusi ketat adalah $\delta$.

**Catatan edisi:** pada langkah 2, sumber menulis
$T^m\in M_{i+1}\setminus M_i$. Karena $M_i$ terdiri atas eksponen, hubungan
yang bertipe benar adalah $m\in M_{i+1}\setminus M_i$, yang kemudian
menghasilkan $T^m\in K[M_{i+1}]\setminus K[M_i]$. Edisi ini menuliskan
implikasi tersebut secara eksplisit.

[Kembali ke Soal 20.17](#br-ak-2025-2026-w20-ex-17).

---

**Provenans edisi.** Terjemahan dan produksi pembaca: OpenAI Codex
gpt-5.6-sol, Ultra. Sumber, pengarang, dan lisensi komponen dipertahankan
seperti dinyatakan dalam metadata dan berkas hak edisi.
