---
title: "Solusi Publik Lembar Kerja 18"
stable_id: br-ak-2025-2026-w18-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-18/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: 8b55ef14cccbcab93ba99882d16e0f9888780353f7290eff8e1d2d6cd6bc4cd9
public_solution_count: 5
upstream_solution_revisions: "Soal 18.3=959312; Soal 18.4=959372; Soal 18.10=1112399; Soal 18.11=1111901; Soal 18.15=1090073"
solution_xml_sha256: "03=d2aa3b5c46f63dbdecb3a62db121a935570696bd7c0dc1f34152eba4102fb44d; 04=b9cd383fbd20439b01122bc90b52acaa0ed68198299f74573e1c1511803ff512; 10=814e4ec7eba6c9095bd791de8e09ce91ed76cdd6bc7420478db4e6cf143b5b0b; 11=5732eddb9ae123354f8c3899aa1e88daa89e684432601e1e311c9e350f3f8a59; 15=34642c05983708afb0e21ce5072b5179ddb09a7bb70930ff1f74fb137a7fdf5d"
license: "CC BY-SA 4.0"
translation_status: complete
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 18 {#br-ak-2025-2026-w18-solutions}

Pada batas revisi yang dibekukan, sumber hanya menyediakan solusi publik
untuk Soal 18.3, 18.4, 18.10, 18.11, dan 18.15. Tidak ada solusi tambahan
yang dibuat untuk edisi ini.

<!-- upstream_solution: Monomiale Kurve/7,11,13,37/Geldfälscher/Aufgabe/Lösung; pageid=21336; revid=959312 -->
<!-- upstream_solution_revid: 959312 -->

## Solusi Soal 18.3 {#br-ak-2025-2026-w18-sol-03}

Kita hitung jumlah-jumlah yang dapat dibentuk dari keempat bilangan tersebut.
Caranya ialah menambahkan kelipatan $7$ pada jumlah yang dibentuk dari
bilangan-bilangan yang lebih besar. Kelipatan $7$ ialah

$$
7,14,21,28,35,42,\ldots.
$$

Mulai dari $11$ diperoleh

$$
11,18,25,32,39,46,\ldots.
$$

Mulai dari $13$ diperoleh

$$
13,20,27,34,41,\ldots.
$$

Mulai dari $22=11+11$ diperoleh

$$
22,29,36,43,\ldots,
$$

dan mulai dari $24=11+13$ diperoleh

$$
24,31,38,45,\ldots.
$$

Tambahkan pula

$$
26=13+13,\qquad
33=11+11+11,\qquad
35=11+11+13,\qquad
37=11+13+13.
$$

Persamaan terakhir juga menunjukkan bahwa pembangkit $37$ berlebih. Kini
terdapat urutan tanpa celah dari $31$ sampai $37$, yang panjangnya $7$;
karena itu semua bilangan yang lebih besar juga berada di dalam monoid.
Bilangan $30$ tidak berada di dalamnya. Jadi bilangan konduktornya $31$, dan
$30$ merupakan jumlah terbesar yang tidak dapat dibayarkan.

Multiplisitasnya adalah bilangan positif terkecil, yaitu $7$, dan dimensi
penyematannya $3$ karena $37$ berlebih. Celah-celahnya ialah

$$
1,2,3,4,5,6,8,9,10,12,15,16,17,19,23,30.
$$

Jadi derajat singularitasnya $16$; tepat sebanyak itulah jumlah yang tidak
dapat dibayarkan.

[Kembali ke Soal 18.3](#br-ak-2025-2026-w18-ex-03).

<!-- upstream_solution: Numerisches Monoid/4,7,17/Invarianten/Aufgabe/Lösung; pageid=21594; revid=959372 -->
<!-- upstream_solution_revid: 959372 -->

## Solusi Soal 18.4 {#br-ak-2025-2026-w18-sol-04}

Monoid memuat semua kelipatan $4$, yakni

$$
4,8,12,16,20,24,\ldots.
$$

Ia juga memuat semua jumlah $7$ dengan kelipatan $4$,

$$
7,11,15,19,23,\ldots,
$$

semua jumlah $2\cdot7=14$ dengan kelipatan $4$,

$$
14,18,22,26,\ldots,
$$

dan semua jumlah $3\cdot7=21$ dengan kelipatan $4$,

$$
21,25,\ldots.
$$

Dengan demikian semua bilangan mulai dari $18$ telah tercakup, sebab setiap
kelas sisa modulo $4$ mempunyai wakil di dalam monoid. Karena pembangkit $17$
juga tersedia, semua bilangan mulai dari $14$ berada di dalam monoid. Jadi
bilangan konduktornya $14$.

Multiplisitasnya adalah bilangan positif terkecil di dalam monoid, yaitu $4$.
Dimensi penyematannya $3$, sebab pembangkit $17$ tidak dapat dibuang. Celahnya
ialah

$$
1,2,3,5,6,9,10,13,
$$

sehingga derajat singularitasnya $8$.

[Kembali ke Soal 18.4](#br-ak-2025-2026-w18-ex-04).

<!-- upstream_solution: Neilsche Parabel/(1,1)/Radikalbeschreibung/Aufgabe/Lösung; pageid=94833; revid=1112399 -->
<!-- upstream_solution_revid: 1112399 -->

## Solusi Soal 18.10 {#br-ak-2025-2026-w18-sol-10}

Tinjau homomorfisme gelanggang injektif

$$
\begin{aligned}
\varphi:R&\longrightarrow\mathbb C[T],\\
X&\longmapsto T^2,\\
Y&\longmapsto T^3.
\end{aligned}
$$

Perluasan ideal $(X-1,Y-1)$ adalah

$$
(T^2-1,T^3-1)
=((T-1)(T+1),(T-1)(T^2+T+1)).
$$

Radikal ideal ini ialah $(T-1)$, sebab $1$ merupakan satu-satunya akar
bersama kedua polinomial itu. Hal ini juga mengikuti dari Nullstellensatz;
dalam kasus ini bahkan berlaku kesamaan ideal yang bersesuaian.

Andaikan $(X-1,Y-1)=\sqrt{(f)}$ untuk suatu $f\in R$. Setelah diperluas ke
$\mathbb C[T]$, harus berlaku

$$
\varphi(f)=c(T-1)^n
$$

untuk suatu $n\in\mathbb N_+$ dan $c\in\mathbb C^\times$. Koefisien $T$ dalam
polinomial ini tak nol. Akan tetapi, setiap unsur dalam citra $R$ mempunyai
bentuk

$$
\varphi(f)=a_0+a_2T^2+a_3T^3+\cdots+a_dT^d,
$$

dan karenanya tidak mempunyai suku linear. Ini kontradiksi.

**Catatan edisi:** sumber menulis langsung
$\varphi(f)=(T-1)^n$. Dari kesamaan radikal hanya diperoleh kelipatan skalar
tak nol $c(T-1)^n$. Edisi ini mempertahankan argumen dengan faktor $c$ yang
diperlukan; koefisien linearnya tetap tak nol.

[Kembali ke Soal 18.10](#br-ak-2025-2026-w18-ex-10).

<!-- upstream_solution: Neilsches Monoid/Werte in Z mod 9/Aufgabe/Lösung; pageid=167325; revid=1111901 -->
<!-- upstream_solution_revid: 1111901 -->

## Solusi Soal 18.11 {#br-ak-2025-2026-w18-sol-11}

1. Unsur-unsur

   $$
   1,2,4,5,7,8
   $$

   adalah satuan, sebab semuanya relatif prima dengan $9$. Unsur-unsur
   $0,3,6$ nilpoten, sebab kuadratnya sama dengan $0$ dalam $R$.

2. Untuk homomorfisme monoid

   $$
   \pi:\mathbb N\longrightarrow R
   $$

   harus berlaku $\pi(0)=1$. Homomorfisme itu ditentukan secara tunggal oleh
   nilai $\pi(1)$, dan setiap unsur $R$ dapat dipilih sebagai nilai tersebut.
   Jadi

   $$
   \left|\operatorname{Mor}_{\mathrm{mon}}(\mathbb N,R)\right|=9.
   $$

3. Misalkan $\rho(2)$ satuan. Satu-satunya pilihan yang mungkin ialah

   $$
   \pi(1)=\rho(3)\rho(2)^{-1},
   $$

   sebab harus berlaku

   $$
   \rho(3)=\pi(3)=\pi(2)\pi(1)=\rho(2)\pi(1).
   $$

   Kita periksa bahwa ini benar-benar menentukan homomorfisme dari
   $\mathbb N$ ke $R$. Kasus ketika salah satu penjumlah adalah $0$, atau
   ketika kedua penjumlah sekurang-kurangnya $2$, langsung mengikuti dari
   sifat homomorfisme $\rho$. Untuk $i=j=1$,

   $$
   \begin{aligned}
   \pi(1)\pi(1)
   &=\rho(3)\rho(2)^{-1}\rho(3)\rho(2)^{-1}\\
   &=\rho(3+3)\rho(2+2)^{-1}\rho(2)^{-1}\rho(2)\\
   &=\rho(6)\rho(6)^{-1}\rho(2)\\
   &=\rho(2)=\pi(2).
   \end{aligned}
   $$

   Untuk $j\geq2$,

   $$
   \begin{aligned}
   \pi(1)\pi(j)
   &=\pi(1)\rho(j)\\
   &=\rho(3)\rho(2)^{-1}\rho(j)\\
   &=\rho(3+j)\rho(2)^{-1}\\
   &=\rho(1+j)\rho(2)\rho(2)^{-1}\\
   &=\rho(1+j)=\pi(1+j).
   \end{aligned}
   $$

4. Jika $\pi(1)$ satuan, seluruh citranya terdiri atas satuan, sehingga
   pembatasan pada $M\setminus\{0\}$ bukan fungsi nol. Jika

   $$
   \pi(1)\in\{0,3,6\},
   $$

   maka $\pi(2)=0$, lalu $\pi(i)=0$ untuk setiap $i\geq2$. Jadi tepat ketiga
   pilihan nilai tersebut memberikan pembatasan nol yang diminta.

5. Menurut bagian 3, hanya $\rho$ dengan $\rho(2)$ nilpoten yang mungkin tidak
   mempunyai perluasan. Dalam hal itu $\rho(3)$ juga nilpoten. Jika
   $\rho(3)$ satuan, maka

   $$
   \rho(3+3)=\rho(6)=\rho(2+2+2)
   $$

   akan menjadi satuan, dan karenanya $\rho(2)$ juga satuan, suatu
   kontradiksi.

   Sebaliknya, pilih sebarang unsur nilpoten untuk $\rho(2)$ dan $\rho(3)$.
   Maka harus berlaku $\rho(n)=0$ untuk setiap $n\geq4$, sebab setiap bilangan
   semacam itu dapat ditulis $n=2i+3j$ dengan $i+j\geq2$. Setiap pilihan
   demikian benar-benar memberi homomorfisme monoid $M\to R$. Homomorfisme
   tersebut hanya mempunyai perluasan ke $\mathbb N$ ketika

   $$
   \rho(2)=\rho(3)=0.
   $$

   Delapan pasangan nilpoten lainnya tidak mempunyai perluasan.

6. Enam homomorfisme dengan $\rho(2)$ satuan, delapan homomorfisme tanpa
   perluasan dari bagian 5, dan satu homomorfisme nol pada
   $M\setminus\{0\}$ menghasilkan

   $$
   6+8+1=15
   $$

   unsur dalam $\operatorname{Mor}_{\mathrm{mon}}(M,R)$.

[Kembali ke Soal 18.11](#br-ak-2025-2026-w18-ex-11).

<!-- upstream_solution: Monoidring/Homomorphismus/Spektrumsabbildung nicht surjektiv/Aufgabe/Lösung; pageid=94911; revid=1090073 -->
<!-- upstream_solution_revid: 1090073 -->

## Solusi Soal 18.15 {#br-ak-2025-2026-w18-sol-15}

Tinjau inklusi

$$
\mathbb N\subset\mathbb Z.
$$

Untuk sebarang lapangan $K$, pemetaan

$$
\varphi:\mathbb N\longrightarrow(K,\cdot,1)
$$

yang membawa $0$ ke $1$ dan setiap bilangan positif ke $0$ merupakan
homomorfisme monoid, dan karenanya suatu titik dalam
$K\!-!\operatorname{Spek}(K[\mathbb N])$. Homomorfisme ini tidak dapat
diperluas menjadi homomorfisme monoid pada seluruh $\mathbb Z$, sebab $1$
dapat dibalik di $\mathbb Z$ dan karena itu harus dipetakan ke suatu satuan.
Jadi pemetaan spektrum yang diinduksi oleh inklusi di atas tidak surjektif.

[Kembali ke Soal 18.15](#br-ak-2025-2026-w18-ex-15).

---

**Provenans edisi.** Terjemahan dan produksi pembaca: OpenAI Codex
gpt-5.6-sol, Ultra. Sumber, pengarang, dan lisensi komponen dipertahankan
seperti dinyatakan dalam metadata dan berkas hak edisi.
