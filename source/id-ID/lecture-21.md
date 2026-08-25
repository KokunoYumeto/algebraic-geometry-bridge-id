---
title: "Kuliah 21 - Gelanggang Valuasi Diskret dan Lema Nakayama"
stable_id: br-ak-2025-2026-l21
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 21"
upstream_pageid: 165910
upstream_revid: 1112312
upstream_timestamp: "2026-08-21T09:27:05Z"
upstream_mediawiki_sha1: 05c51f6e29f6ec12aef400195396ca517924b094
source_url: "https://de.wikiversity.org/w/index.php?oldid=1112312"
authority_manifest: authority/wikiversity/unit-21/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: d85444ddfc66c8e77d52db3f3abc0a186e5dd598789edaaf890b3c09cf00f923
lecture_xml_sha256: 65c9dc086c930a46e53957102e7f742d3ea04fac707dae3595ac3983b54f75b8
lecture_expanded_tex_sha256: 0a6fc74c8d01069d327fe25c5203bf4587b4564c8409ad57f625c3ac16ceb62f
license: "CC BY-SA 4.0 for translated course text; Unit 21 contains no substantive reader media"
translation_status: complete
source_semantic_entities: 13
edition_bridges: 3
source_corrections: 2
---

# Kuliah 21: Gelanggang Valuasi Diskret dan Lema Nakayama {#br-ak-2025-2026-l21}

## Gelanggang valuasi diskret {#br-ak-2025-2026-l21-s01}

<!-- upstream_entity: Diskreter Bewertungsring/Beispiele/Charakterisierung/2/Einführung/Textabschnitt -->

Kita sekarang melanjutkan kajian lokal kurva aljabar. Dalam pembahasan
berikutnya kita akan memperoleh berbagai karakterisasi bagi suatu titik pada
kurva agar nonsingular—atau mulus. Untuk sebuah titik $P$ pada kurva, terdapat
gelanggang lokal di $P$, yaitu pelokalan gelanggang koordinat afin kurva pada
ideal maksimal yang bersesuaian dengan $P$. Jika

$$
P=(a,b)\in C=V(F)\subseteq\mathbb A_K^2,
$$

gelanggang lokal itu dapat dideskripsikan dengan dua cara:

$$
K[X,Y]_{(X-a,Y-b)}/(F)
\cong
(K[X,Y]/(F))_{\mathfrak m},
$$

dengan $\mathfrak m$ ideal maksimal yang kini dipandang di dalam gelanggang
faktor. Gelanggang ini memuat sifat-sifat aljabar pokok titik tersebut. Konsep
pertama yang penting adalah gelanggang valuasi diskret.

<!-- upstream_entity: Kommutative Ringtheorie/Diskreter Bewertungsring/Definition -->

### Definisi: gelanggang valuasi diskret {#br-ak-2025-2026-l21-def-01}

Suatu *gelanggang valuasi diskret* adalah domain ideal utama $R$ yang, hingga
asosiasi, mempunyai tepat satu unsur prima.

Pembangkit ideal maksimal pada gelanggang valuasi diskret juga disebut
*uniformisator lokal*.

<!-- upstream_entity: Diskreter Bewertungsring/Erste Eigenschaften/Fakt -->

### Lema: sifat-sifat pertama gelanggang valuasi diskret {#br-ak-2025-2026-l21-lem-01}

Suatu gelanggang valuasi diskret merupakan domain ideal utama lokal dan
Noether yang mempunyai tepat dua ideal prima, yaitu

$$
(0)\subset\mathfrak m,
$$

dengan $\mathfrak m$ ideal maksimalnya.

#### Bukti {#br-ak-2025-2026-l21-lem-01-proof}

Suatu gelanggang valuasi diskret bukan lapangan. Dalam domain ideal utama yang
bukan lapangan, setiap ideal maksimal dibangkitkan oleh suatu unsur prima,
sedangkan pembangkit prima dari dua ideal maksimal yang berbeda tidak dapat
saling berasosiasi. Karena dalam gelanggang valuasi diskret hanya ada satu
unsur prima hingga asosiasi, hanya ada satu ideal maksimal.

Demikian pula, setiap ideal prima tak nol di dalam domain ideal utama
dibangkitkan oleh suatu unsur prima. Karena itu satu-satunya ideal prima tak
nol ialah $\mathfrak m$; bersama ideal nol, diperoleh tepat dua ideal prima.

<!-- upstream_entity: Polynomring/Eine Variable/Lokalisiert/Diskreter Bewertungsring/Beispiel -->

### Contoh: pelokalan $K[X]$ pada $(X)$ {#br-ak-2025-2026-l21-exa-01}

Misalkan $K$ suatu lapangan, $K[X]$ gelanggang polinomial, dan

$$
R=K[X]_{(X)}
$$

pelokalan pada ideal maksimal

$$
\mathfrak m=(X).
$$

Maka $R$ merupakan gelanggang valuasi diskret. Kedua ideal primanya ialah

$$
(0)\subset(X).
$$

Gelanggang $R$ merupakan domain ideal utama karena $K[X]$ adalah domain ideal
utama. Karena hanya terdapat satu ideal maksimal, hingga asosiasi hanya
terdapat satu unsur prima, yaitu $X$.

<!-- upstream_entity: Z/Lokalisiert/Diskreter Bewertungsring/Beispiel -->

### Contoh: pelokalan $\mathbb Z$ pada $(p)$ {#br-ak-2025-2026-l21-exa-02}

Misalkan $p$ suatu bilangan prima dan

$$
R=\mathbb Z_{(p)}
$$

pelokalan pada ideal maksimal

$$
\mathfrak m=(p).
$$

Maka $R$ merupakan gelanggang valuasi diskret. Kedua ideal primanya ialah

$$
(0)\subset(p).
$$

Gelanggang $R$ merupakan domain ideal utama karena $\mathbb Z$ adalah domain
ideal utama. Karena hanya terdapat satu ideal maksimal, hingga asosiasi hanya
terdapat satu unsur prima, yaitu $p$.

<!-- upstream_entity: Diskreter Bewertungsring/Ordnung/Definition -->

### Definisi: orde pada gelanggang valuasi diskret {#br-ak-2025-2026-l21-def-02}

Misalkan $R$ suatu gelanggang valuasi diskret dengan unsur prima $p$. Untuk
setiap unsur tak nol $f\in R$, terdapat suatu $n\in\mathbb N$ dan suatu satuan
$u\in R^\times$ sehingga

$$
f=up^n.
$$

Bilangan $n$ disebut *orde* $f$ dan ditulis

$$
\operatorname{ord}(f)=n.
$$

Jadi orde tidak lain adalah eksponen dari unsur prima tunggal—hingga
asosiasi—dalam faktorisasi prima $f$.

<!-- upstream_entity: Diskreter Bewertungsring/Ordnungsfunktion/Erste Eigenschaften/Fakt -->

### Lema: sifat-sifat orde {#br-ak-2025-2026-l21-lem-02}

Misalkan $R$ suatu gelanggang valuasi diskret dengan ideal maksimal

$$
\mathfrak m=(p).
$$

Pemetaan orde

$$
\begin{aligned}
R\setminus\{0\}&\longrightarrow\mathbb N,\\
f&\longmapsto\operatorname{ord}(f)
\end{aligned}
$$

mempunyai sifat-sifat berikut. Untuk $f,g\in R\setminus\{0\}$,

1. berlaku

   $$
   \operatorname{ord}(fg)
   =\operatorname{ord}(f)+\operatorname{ord}(g);
   $$

2. jika $f+g\ne0$, berlaku

   $$
   \operatorname{ord}(f+g)
   \geq
   \min\{\operatorname{ord}(f),\operatorname{ord}(g)\};
   $$

3. berlaku $f\in\mathfrak m$ jika dan hanya jika

   $$
   \operatorname{ord}(f)\geq1;
   $$

4. berlaku $f\in R^\times$ jika dan hanya jika

   $$
   \operatorname{ord}(f)=0.
   $$

**Bukti.** Lihat Soal 21.2.

**Catatan edisi — koreksi sumber.** Sumber mendefinisikan
$\operatorname{ord}$ hanya pada $R\setminus\{0\}$, tetapi mencetak
ketaksamaan pada jumlah tanpa mengecualikan $f+g=0$. Edisi ini menambahkan
syarat $f+g\ne0$, sehingga setiap kemunculan $\operatorname{ord}$ berada di
dalam domain definisinya.

Kita sekarang akan membuktikan suatu karakterisasi penting bagi gelanggang
valuasi diskret. Secara khusus, karakterisasi itu menunjukkan bahwa domain
integral lokal normal yang Noether dan mempunyai tepat dua ideal prima sudah
merupakan gelanggang valuasi diskret. Mula-mula kita memerlukan sebuah lema.

<!-- upstream_entity: Kommutative Ringtheorie/Noethersch lokal nulldimensional/Potenz ist null/Fakt -->

### Lema 21.7: nilpotensi ideal maksimal {#br-ak-2025-2026-l21-lem-03}

Misalkan $S$ suatu gelanggang komutatif lokal dan Noether. Andaikan ideal
maksimal $\mathfrak m$ merupakan satu-satunya ideal prima $S$. Maka terdapat
suatu $n\in\mathbb N$ sehingga

$$
\mathfrak m^n=0.
$$

<!-- upstream_entity: Kommutative Ringtheorie/Noethersch lokal nulldimensional/Potenz ist null/Fakt/Beweis -->

#### Bukti {#br-ak-2025-2026-l21-lem-03-proof}

Pertama kita klaim bahwa setiap unsur $S$ merupakan satuan atau nilpoten.
Ambil suatu unsur $f\in S$ yang bukan satuan. Karena $S$ lokal,

$$
f\in\mathfrak m.
$$

Andaikan $f$ tidak nilpoten.

<!-- upstream_cross_reference: Lemma 22.15 (Zahlentheorie (Osnabrück 2025)); replaced by the self-contained edition bridge below -->

> **Jembatan edisi 21.A — lema ideal prima.** Jika suatu unsur $f$ dalam
> gelanggang komutatif tidak nilpoten, terdapat ideal prima $\mathfrak p$
> yang tidak memuat $f$. Memang, himpunan multiplikatif
> $T=\{1,f,f^2,\ldots\}$ tidak memuat nol. Dengan lema Zorn, pilih ideal
> $\mathfrak p$ yang maksimal di antara ideal-ideal yang tidak beririsan
> dengan $T$. Jika $ab\in\mathfrak p$ tetapi $a,b\notin\mathfrak p$, maka
> $\mathfrak p+(a)$ dan $\mathfrak p+(b)$ masing-masing beririsan dengan
> $T$. Mengalikan satu unsur dari setiap irisan menghasilkan unsur
> $T\cap\mathfrak p$, suatu kontradiksi. Jadi $\mathfrak p$ prima dan,
> karena $\mathfrak p\cap T=\varnothing$, berlaku $f\notin\mathfrak p$.
> Sumber merujuk fakta ini melalui penomoran kursus lain; edisi menyertakan
> pernyataan dan buktinya agar argumen mandiri.

Ideal prima $\mathfrak p$ tersebut berbeda dari $\mathfrak m$, sebab
$f\in\mathfrak m$ tetapi $f\notin\mathfrak p$. Ini bertentangan dengan asumsi
bahwa $\mathfrak m$ satu-satunya ideal prima. Jadi setiap unsur ideal maksimal
bersifat nilpoten.

Karena $S$ Noether, ideal $\mathfrak m$ mempunyai sistem pembangkit berhingga

$$
\mathfrak m=(f_1,\ldots,f_k).
$$

Jika $\mathfrak m=0$, cukup ambil $n=1$. Karena itu selanjutnya kita boleh
menganggap $k\geq1$.

Pilih $m\in\mathbb N$ sehingga

$$
f_i^m=0
\qquad\text{untuk semua }i=1,\ldots,k,
$$

dan tetapkan $n=km$. Setiap unsur $\mathfrak m^n$ merupakan kombinasi linear
dari produk-produk berbentuk

$$
\left(\sum_{i=1}^k a_{i1}f_i\right)
\left(\sum_{i=1}^k a_{i2}f_i\right)
\cdots
\left(\sum_{i=1}^k a_{in}f_i\right).
$$

Setelah dikembangkan, setiap suku merupakan monomial

$$
f_1^{r_1}\cdots f_k^{r_k}
\qquad\text{dengan}\qquad
\sum_{i=1}^k r_i=n.
$$

Untuk paling sedikit satu indeks $i$ berlaku

$$
r_i\geq\frac nk=m.
$$

Karena $f_i^m=0$, setiap monomial itu nol. Maka $\mathfrak m^n=0$.

<!-- upstream_entity: Diskrete Bewertungsringe/Charakterisierung/1/Fakt -->

### Teorema: karakterisasi gelanggang valuasi diskret {#br-ak-2025-2026-l21-thm-01}

Misalkan $R$ suatu domain integral lokal dan Noether yang mempunyai tepat dua
ideal prima

$$
(0)\subset\mathfrak m.
$$

Pernyataan-pernyataan berikut ekuivalen.

1. $R$ merupakan gelanggang valuasi diskret.
2. $R$ merupakan domain ideal utama.
3. $R$ merupakan domain faktorisasi tunggal.
4. $R$ normal.
5. Ideal maksimal $\mathfrak m$ merupakan ideal utama.

<!-- upstream_entity: Diskrete Bewertungsringe/Charakterisierung/1/Fakt/Beweis -->

#### Bukti {#br-ak-2025-2026-l21-thm-01-proof}

Implikasi $(1)\Rightarrow(2)$ langsung mengikuti Definisi 21.1.

Implikasi $(2)\Rightarrow(3)$ mengikuti Teorema 9.3 dalam Aljabar Komutatif.

Implikasi $(3)\Rightarrow(4)$ mengikuti Teorema 20.2.

Untuk membuktikan $(4)\Rightarrow(5)$, ambil

$$
f\in\mathfrak m,
\qquad f\ne0.
$$

> **Jembatan edisi 21.B — penerapan pada $R/(f)$.** Tetapkan
> $S=R/(f)$. Gelanggang $S$ tetap Noether dan lokal, dengan ideal maksimal
> $\widetilde{\mathfrak m}=\mathfrak m/(f)$. Ideal-ideal prima $S$
> bersesuaian dengan ideal prima $R$ yang memuat $(f)$. Karena ideal prima
> $R$ hanya $(0)$ dan $\mathfrak m$, sedangkan $f\ne0$, satu-satunya ideal
> prima yang memuat $(f)$ ialah $\mathfrak m$. Jadi
> $\widetilde{\mathfrak m}$ satu-satunya ideal prima $S$. Lema 21.7 memberi
> $\widetilde{\mathfrak m}^{\,n}=0$ untuk suatu $n$, yang setelah ditarik
> kembali ke $R$ tepat berarti $\mathfrak m^n\subseteq(f)$.

Pilih $n$ minimal sehingga

$$
\mathfrak m^n\subseteq(f)
\qquad\text{dan}\qquad
\mathfrak m^{n-1}\nsubseteq(f).
$$

Pilih

$$
g\in\mathfrak m^{n-1}\setminus(f)
$$

dan tinjau

$$
h:=\frac fg\in Q(R).
$$

Di sini $g\ne0$. Inversnya,

$$
h^{-1}=\frac gf,
$$

tidak berada di $R$, sebab jika berada di $R$ maka $g\in(f)$. Karena $R$
normal, $h^{-1}$ juga tidak integral atas $R$. Menurut kriteria modul bagi
keintegralan pada Lema 19.9, khususnya untuk ideal maksimal
$\mathfrak m\subset R$, berlaku

$$
h^{-1}\mathfrak m\nsubseteq\mathfrak m.
$$

Di sisi lain, berdasarkan pilihan $g$,

$$
h^{-1}\mathfrak m
=\frac gf\mathfrak m
\subseteq\frac{\mathfrak m^n}{f}
\subseteq R.
$$

Dengan demikian $h^{-1}\mathfrak m$ adalah suatu ideal $R$ yang tidak termuat
dalam ideal maksimal. Jadi

$$
h^{-1}\mathfrak m=R.
$$

Dari persamaan ini diperoleh $h\in\mathfrak m$. Selain itu, untuk setiap
$x\in\mathfrak m$ berlaku $h^{-1}x\in R$, sehingga

$$
x=h(h^{-1}x)\in(h).
$$

Maka

$$
(h)=\mathfrak m,
$$

dan ideal maksimal itu utama.

Sekarang buktikan $(5)\Rightarrow(1)$. Misalkan

$$
\mathfrak m=(\pi).
$$

Unsur $\pi$ prima dan, hingga asosiasi, merupakan satu-satunya unsur prima.
Ambil suatu $f\in R$, $f\ne0$, yang bukan satuan. Maka

$$
f\in\mathfrak m,
$$

sehingga $f=\pi g_1$. Unsur $g_1$ merupakan satuan atau kembali berada di
$\mathfrak m$. Dalam kasus kedua,

$$
g_1=\pi g_2
\qquad\text{dan}\qquad
f=\pi^2g_2.
$$

Kita klaim bahwa proses ini berhenti, sehingga

$$
f=\pi^ku
$$

untuk suatu $k\in\mathbb N$ dan satuan $u$. Jika tidak, untuk setiap
$n$ yang sebesar apa pun dapat ditulis

$$
f=\pi^ng_n.
$$

Dengan penerapan Lema 21.7 pada $R/(f)$ seperti dalam Jembatan 21.B, terdapat
$m\in\mathbb N$ sehingga

$$
(\pi^m)=\mathfrak m^m\subseteq(f).
$$

Jika $n\geq m+1$, maka untuk beberapa $a,b\in R$ diperoleh

$$
\pi^m=af=a\pi^{m+1}b,
$$

dan karena $R$ domain integral, pembatalan $\pi^m$ menghasilkan kontradiksi

$$
1=ab\pi.
$$

Jadi setiap unsur tak nol yang bukan satuan merupakan hasil kali suatu
pangkat $\pi$ dengan sebuah satuan. Khususnya, $R$ merupakan domain
faktorisasi tunggal. Karena $R$ Noether, setiap ideal dapat ditulis

$$
\mathfrak a=(f_1,\ldots,f_s).
$$

Ideal nol sudah utama. Untuk $\mathfrak a\ne0$, hapus pembangkit yang nol dan
tuliskan setiap pembangkit yang tersisa sebagai

$$
f_i=\pi^{n_i}u_i
$$

dengan $u_i$ satuan. Jika

$$
n=\min_i n_i,
$$

maka

$$
\mathfrak a=(\pi^n).
$$

Jadi $R$ adalah domain ideal utama dengan tepat satu unsur prima hingga
asosiasi; menurut definisi, $R$ merupakan gelanggang valuasi diskret.

## Lema Nakayama {#br-ak-2025-2026-l21-s02}

Di dalam kelas domain integral lokal Noether yang mempunyai tepat dua ideal
prima $(0)\subset\mathfrak m$—dan karena itu bukan lapangan—teorema di atas
menunjukkan bahwa $R$ merupakan gelanggang valuasi diskret jika dan hanya jika
ideal maksimal $\mathfrak m$ dibangkitkan oleh satu unsur. Karena itu wajar
untuk menanyakan, secara lebih umum, berapa banyak pembangkit yang diperlukan
oleh ideal maksimal gelanggang lokal pada suatu titik kurva aljabar. Pertanyaan
ini mengarah pada dimensi penyematan, yang telah muncul pada kurva monomial.
Dimensi tersebut juga merupakan dimensi ruang vektor atas $R/\mathfrak m$

$$
\mathfrak m/\mathfrak m^2.
$$

Untuk menjelaskan hubungan ini, kita memerlukan beberapa persiapan, terutama
Lema Nakayama.

**Catatan edisi — koreksi lingkup sumber.** Kalimat peralihan sumber menyatakan
ekuivalensi antara “gelanggang valuasi diskret” dan “ideal maksimal utama”
tanpa mengulang hipotesis. Edisi ini secara eksplisit mempertahankan lingkup
teorema: domain integral lokal Noether dengan tepat dua ideal prima.

Konstruksi berikut dipakai dalam Lema Nakayama. Misalkan $V$ suatu modul-$R$,
$U\subseteq V$ suatu submodul, dan $I\subseteq R$ suatu ideal. Notasi $IU$
menyatakan submodul-$R$ dari $V$ yang dibangkitkan oleh semua unsur

$$
fv,
\qquad f\in I,
\qquad v\in U.
$$

Submodul ini juga merupakan submodul dari $U$. Jika $U$ sendiri sebuah ideal—
jadi submodul-$R$ dari $R$—konstruksi tersebut sama dengan hasil kali ideal.
Modul faktor $V/IV$ secara alami bukan hanya modul-$R$, melainkan juga
modul-$(R/I)$. Jika $I$ maksimal, modul faktor itu bahkan merupakan ruang
vektor atas lapangan residu $R/I$.

<!-- upstream_entity: Lokaler Ring/Lemma von Nakayama/Fakt -->

### Lema Nakayama {#br-ak-2025-2026-l21-lem-04}

Misalkan $(R,\mathfrak m)$ suatu gelanggang lokal dan $V$ suatu modul-$R$ yang
dibangkitkan secara hingga. Jika

$$
\mathfrak mV=V,
$$

maka

$$
V=0.
$$

<!-- upstream_entity: Lokaler Ring/Lemma von Nakayama/Fakt/Beweis -->

#### Bukti {#br-ak-2025-2026-l21-lem-04-proof}

Misalkan $v_1,\ldots,v_n$ suatu sistem pembangkit $V$. Karena
$v_i\in\mathfrak mV$, untuk setiap $v_i$ terdapat penyajian

$$
v_i=a_{i1}v_1+\cdots+a_{in}v_n,
\qquad a_{ij}\in\mathfrak m.
$$

Jadi, untuk setiap $i$,

$$
(1-a_{ii})v_i
=a_{i1}v_1+\cdots+a_{i,i-1}v_{i-1}
+a_{i,i+1}v_{i+1}+\cdots+a_{in}v_n.
$$

Karena $a_{ii}\in\mathfrak m$, koefisien $1-a_{ii}$ merupakan satuan dalam
gelanggang lokal $R$. Kita dapat menyelesaikan persamaan itu terhadap $v_i$;
artinya, $v_i$ berlebih dalam sistem pembangkit. Dengan menghapus pembangkit
satu demi satu, pada akhirnya tidak tersisa pembangkit. Maka $V$ adalah modul
nol.

> **Jembatan edisi 21.C — korolari pembangkit minimal.** Misalkan
> $(R,\mathfrak m)$ gelanggang lokal, $k=R/\mathfrak m$ lapangan residunya,
> dan $V$ modul-$R$ yang dibangkitkan secara hingga. Unsur
> $v_1,\ldots,v_r$ membangkitkan $V$ jika dan hanya jika kelas-kelasnya
> membangkitkan ruang vektor $V/\mathfrak mV$ atas $k$. Arah maju langsung.
> Untuk arah balik, tetapkan $N=Rv_1+\cdots+Rv_r$. Hipotesis pada kelas-kelas
> memberi $V=N+\mathfrak mV$, sehingga
> $V/N=\mathfrak m(V/N)$. Lema Nakayama memberikan $V/N=0$, jadi $V=N$.
> Akibatnya, jumlah minimal pembangkit $V$ ialah
> $\dim_k(V/\mathfrak mV)$. Jika $\mathfrak m$ dibangkitkan secara hingga—
> khususnya dalam konteks Noether di atas—maka
> $\mu_R(\mathfrak m)=\dim_k(\mathfrak m/\mathfrak m^2)$, yaitu dimensi
> penyematan. Korolari ini menyediakan alat yang diperlukan untuk menilai
> banyaknya pembangkit ideal pada Soal 21.25–21.26, tanpa memberikan solusi
> bagi soal-soal tersebut.

---

**Provenans edisi.** Terjemahan dan produksi pembaca: OpenAI Codex
gpt-5.6-sol, Ultra. Sumber, pengarang, dan lisensi komponen dipertahankan
seperti dinyatakan dalam metadata dan berkas hak edisi.
