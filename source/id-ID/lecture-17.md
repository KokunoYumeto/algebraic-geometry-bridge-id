---
title: "Kuliah 17 - Gelanggang Monoid dan Grup Selisih"
stable_id: br-ak-2025-2026-l17
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 17"
upstream_pageid: 165906
upstream_revid: 1112301
upstream_timestamp: "2026-08-21T08:52:16Z"
upstream_mediawiki_sha1: da4e92351c0197e66d117d85306d1578900dc81b
source_url: "https://de.wikiversity.org/w/index.php?oldid=1112301"
authority_manifest: authority/wikiversity/unit-17/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: c6747335c58fb3b4303cf3095705df7f991143f79d2d3598582a1cc8c99bef1a
lecture_xml_sha256: 27edcd8d46ff9a0d3b04e3b7996caec8b5b73076a7717499b6219d2e65edb09d
lecture_expanded_tex_sha256: 6afb4b6a5e3db0455481dcb68af9b8ecdff5d42d979f53399b41830108c00084
license: "CC BY-SA 4.0 for translated course text; official PDF rights are recorded in authority/ASSET_CLOSURE-unit-17.json"
translation_status: complete
---

# Kuliah 17: Gelanggang Monoid dan Grup Selisih {#br-ak-2025-2026-l17}

Setelah mengembangkan teori cukup jauh, kini kita beralih kepada suatu kelas
contoh yang luas, yaitu gelanggang monoid.

## Gelanggang monoid {#br-ak-2025-2026-l17-s01}

<!-- upstream_entity: Kommutative Ringtheorie/Monoidringe/Definition -->

### Definisi: gelanggang monoid {#br-ak-2025-2026-l17-def-01}

Misalkan $M$ suatu monoid komutatif yang ditulis secara aditif dan $R$ suatu
gelanggang komutatif. *Gelanggang monoid* $R[M]$ dibangun sebagai berikut.
Sebagai modul-$R$,

$$
R[M]=\bigoplus_{m\in M}Re_m,
$$

yakni $R[M]$ adalah modul bebas dengan basis

$$
(e_m)_{m\in M}.
$$

Perkalian pada unsur-unsur basis didefinisikan oleh

$$
e_m\cdot e_k:=e_{m+k}
$$

dan diperluas secara distributif ke seluruh $R[M]$. Unsur netral
$0\in M$ menentukan unsur netral perkalian

$$
1=e_0.
$$

<!-- upstream_entity: Kommutative Ringtheorie/Monoidringe/Grundeigenschaften/Bemerkung -->

### Catatan: bentuk unsur dan perkalian {#br-ak-2025-2026-l17-rem-01}

Setiap unsur gelanggang monoid mempunyai bentuk tunggal

$$
f=\sum_{m\in\widetilde M}a_me_m,
$$

dengan $\widetilde M\subseteq M$ hingga dan $a_m\in R$. Penjumlahan dilakukan
per komponen, sedangkan perkalian diberikan secara eksplisit oleh

$$
\begin{aligned}
fg
&=\left(\sum_{m\in\widetilde M}a_me_m\right)
  \left(\sum_{k\in\overline M}b_ke_k\right)\\
&=\sum_{\ell\in M}
  \left(\sum_{\substack{m+k=\ell\\m\in\widetilde M,\ k\in\overline M}}
  a_mb_k\right)e_\ell.
\end{aligned}
$$

Hanya berhingga banyak $\ell$ yang muncul, dan setiap jumlah di bagian dalam
juga hingga. Inilah arti perluasan distributif pada definisi di atas.

Lazimnya $e_m$ ditulis dengan notasi yang lebih sugestif, yaitu $X^m$, dengan
$X$ suatu simbol yang mengingatkan kita pada variabel. Aturan

$$
X^mX^k=X^{m+k}
$$

menyerupai aturan pada gelanggang polinomial. Memang, gelanggang polinomial
merupakan kasus khusus gelanggang monoid. Biasanya kita menulis

$$
\sum_{m\in M}a_mX^m,
$$

dengan hampir semua $a_m=0$. Unsur berbentuk $X^m$ disebut *monomial*.
Pemetaan

$$
\begin{aligned}
M&\longrightarrow R[M],\\
m&\longmapsto X^m
\end{aligned}
$$

adalah homomorfisme monoid, dengan struktur monoid perkalian pada ruas kanan.

Secara alami, gelanggang monoid merupakan aljabar-$R$: unsur $f\in R$ di dalam
$R[M]$ dipahami sebagai

$$
f=f\cdot1=fX^0.
$$

Karena itu $R$ juga disebut *gelanggang dasar* gelanggang monoid tersebut.
Gelanggang monoid sudah menarik bahkan ketika gelanggang dasarnya suatu
lapangan.

<!-- upstream_entity: Kommutative Monoidringe/Polynomring als Monoidring (mehrere Variablen)/Beispiel -->

### Contoh: gelanggang polinomial {#br-ak-2025-2026-l17-exa-01}

Misalkan $n$ bilangan asli dan

$$
M=\mathbb N^n.
$$

Setiap $k\in\mathbb N^n$ merupakan suatu $n$-tuple
$k=(k_1,\ldots,k_n)$ dengan $k_i\in\mathbb N$, dan dapat ditulis sebagai

$$
(k_1,\ldots,k_n)
=k_1(1,0,\ldots,0)+\cdots+k_n(0,\ldots,0,1).
$$

Dengan menulis $X_i=X^{e_i}$ untuk monomial yang bersesuaian dengan unsur
basis ke-$i$, kita memperoleh

$$
X^k=X_1^{k_1}X_2^{k_2}\cdots X_n^{k_n}.
$$

Jadi gelanggang monoid dari $\mathbb N^n$ di atas $R$ tepat merupakan
gelanggang polinomial dalam $n$ variabel. Khususnya,

$$
R[\mathbb N]=R[X].
$$

Gelanggang monoid dari monoid trivial $\{0\}$ adalah gelanggang dasar itu
sendiri.

<!-- upstream_entity: Kommutative Monoidringe/Laurentring als Monoidring (mehrere Variablen)/Beispiel -->

### Contoh: gelanggang Laurent {#br-ak-2025-2026-l17-exa-02}

Misalkan $n$ bilangan asli dan

$$
M=\mathbb Z^n.
$$

Monoid $M$ adalah grup komutatif bebas berperingkat $n$. Setiap
$k\in\mathbb Z^n$ merupakan suatu $n$-tuple
$k=(k_1,\ldots,k_n)$ dengan $k_i\in\mathbb Z$, yang dapat ditulis sebagai

$$
(k_1,\ldots,k_n)
=k_1(1,0,\ldots,0)+\cdots+k_n(0,\ldots,0,1).
$$

Unsur tersebut menghasilkan monomial

$$
X^k=X_1^{k_1}X_2^{k_2}\cdots X_n^{k_n},
\qquad X_i=X^{e_i}.
$$

Karena itu

$$
R[M]
=R[X_1,\ldots,X_n,X_1^{-1},\ldots,X_n^{-1}].
$$

Gelanggang ini isomorfik dengan pelokalan gelanggang polinomial pada hasil
kali semua variabel:

$$
R[M]
=R[X_1,\ldots,X_n,X_1^{-1},\ldots,X_n^{-1}]
=R[X_1,\ldots,X_n]_{X_1\cdots X_n}.
$$

Gelanggang tersebut disebut *gelanggang Laurent* dalam $n$ variabel di atas
$R$.

## Sifat universal gelanggang monoid {#br-ak-2025-2026-l17-s02}

<!-- upstream_entity: Kommutative Monoidringe/Universelle Eigenschaft für R-Algebren mit Monoidabbildung/Fakt -->

### Teorema: sifat universal {#br-ak-2025-2026-l17-thm-01}

Misalkan $R$ gelanggang komutatif, $M$ monoid komutatif, $B$ aljabar-$R$
komutatif, dan

$$
\varphi:M\longrightarrow(B,\cdot,1)
$$

homomorfisme monoid. Maka terdapat tepat satu homomorfisme aljabar-$R$

$$
\widetilde\varphi:R[M]\longrightarrow B
$$

yang membuat diagram berikut komutatif:

$$
\begin{matrix}
M&\longrightarrow&R[M]\\
&\searrow&\downarrow\widetilde\varphi\\
&&B.
\end{matrix}
$$

#### Bukti {#br-ak-2025-2026-l17-thm-01-proof}

Suatu homomorfisme modul-$R$

$$
\widetilde\varphi:R[M]\longrightarrow B
$$

ditentukan oleh citra unsur-unsur basis $(X^m)_{m\in M}$. Diagram komutatif
tepat ketika

$$
\widetilde\varphi(X^m)=\varphi(m).
$$

Syarat ini menentukan pemetaan secara tunggal dan langsung memberinya sifat
homomorfisme modul-$R$. Kita tinggal memeriksa perkalian. Pertama,

$$
\widetilde\varphi(1)
=\widetilde\varphi(X^0)
=\varphi(0)
=1.
$$

Selanjutnya,

$$
\begin{aligned}
\widetilde\varphi(X^mX^k)
&=\widetilde\varphi(X^{m+k})\\
&=\varphi(m+k)\\
&=\varphi(m)\varphi(k)\\
&=\widetilde\varphi(X^m)\widetilde\varphi(X^k).
\end{aligned}
$$

Jadi pemetaan menghormati perkalian pada monomial. Untuk

$$
f=\sum_{m\in M}a_mX^m,
\qquad
g=\sum_{k\in M}b_kX^k,
$$

dengan dukungan hingga, diperoleh

$$
\begin{aligned}
\widetilde\varphi(fg)
&=\widetilde\varphi\!\left(
  \sum_{\ell\in M}\left(\sum_{m+k=\ell}a_mb_k\right)X^\ell
  \right)\\
&=\sum_{\ell\in M}\left(\sum_{m+k=\ell}a_mb_k\right)
  \varphi(\ell)\\
&=\sum_{m,k\in M}a_mb_k\varphi(m)\varphi(k)\\
&=\left(\sum_{m\in M}a_m\varphi(m)\right)
  \left(\sum_{k\in M}b_k\varphi(k)\right)\\
&=\widetilde\varphi(f)\widetilde\varphi(g).
\end{aligned}
$$

Dengan demikian $\widetilde\varphi$ adalah homomorfisme gelanggang.

<!-- upstream_entity: Kommutative Monoidringe/Funktorialität im Monoid/Fakt -->

### Korolari: funktorialitas terhadap monoid {#br-ak-2025-2026-l17-cor-01}

Misalkan $R$ gelanggang komutatif, $M,N$ monoid komutatif, dan

$$
\varphi:M\longrightarrow N
$$

homomorfisme monoid. Pemetaan ini menginduksi homomorfisme aljabar-$R$

$$
\begin{aligned}
\widetilde\varphi:R[M]&\longrightarrow R[N],\\
X^m&\longmapsto X^{\varphi(m)}.
\end{aligned}
$$

#### Bukti {#br-ak-2025-2026-l17-cor-01-proof}

Terapkan Teorema 17.5 pada aljabar-$R$ $B=R[N]$ dan komposisi homomorfisme
monoid

$$
M\stackrel{\varphi}{\longrightarrow}N\longrightarrow R[N].
$$

<!-- upstream_entity: Kommutative Monoidringe/Universelle Eigenschaft für R-Algebren mit Monoidabbildung/Polynomring als Spezialfall/Bemerkung -->

### Catatan: substitusi dari aljabar polinomial {#br-ak-2025-2026-l17-rem-02}

Suatu keluarga $(m_i)_{i\in I}$ di dalam monoid $M$ menentukan homomorfisme
monoid

$$
\mathbb N^{(I)}\longrightarrow M
$$

yang memetakan unsur basis ke-$i$, $e_i$, ke $m_i$. Jika
$I=\{1,\ldots,n\}$ hingga, Korolari 17.6 menghasilkan homomorfisme
aljabar-$R$

$$
R[\mathbb N^n]=R[X_1,\ldots,X_n]\longrightarrow R[M].
$$

Ini adalah homomorfisme substitusi yang diberikan oleh

$$
X_i\longmapsto X^{m_i}.
$$

<!-- upstream_entity: Kommutative Monoidringe/R-wertige Punkte/Definition -->

### Definisi: titik bernilai gelanggang {#br-ak-2025-2026-l17-def-02}

Untuk monoid komutatif $M$ dan gelanggang komutatif $R$, suatu homomorfisme
monoid

$$
M\longrightarrow(R,\cdot,1)
$$

disebut *titik bernilai $R$* dari $M$.

<!-- upstream_entity: Kommutative Monoidringe/R-wertige Punkte/Bemerkung -->

### Catatan: titik monoid dan spektrum-$K$ {#br-ak-2025-2026-l17-rem-03}

Menurut Teorema 17.5, suatu titik bernilai $R$ dari $M$ ekuivalen dengan
homomorfisme aljabar-$R$ dari $R[M]$ ke $R$. Untuk lapangan dasar $K$,

$$
\begin{aligned}
K\!-\!\operatorname{Spek}(K[M])
&=\operatorname{Hom}^{\mathrm{alg}}_K(K[M],K)\\
&=\operatorname{Mor}_{\mathrm{mon}}(M,K)\\
&=\{\text{titik bernilai }K\text{ dari }M\}.
\end{aligned}
$$

Jadi spektrum-$K$ sudah memiliki deskripsi sederhana pada taraf monoid yang
murni bersifat multiplikatif. Akan tetapi, gelanggang monoid tetap mutlak
diperlukan untuk mendefinisikan topologi Zariski dan berkas fungsi aljabar
pada $K\!-\!\operatorname{Spek}(K[M])$.

<!-- upstream_entity: Kommutative Monoidringe/K-wertige Punkte/Gleichungen/Bemerkung -->

### Catatan: pembangkit dan relasi binomial {#br-ak-2025-2026-l17-rem-04}

Monoid komutatif sering dideskripsikan oleh berhingga banyak pembangkit
$e_1,\ldots,e_r$ beserta relasi-relasi binomial berbentuk

$$
n_1e_1+\cdots+n_re_r=m_1e_1+\cdots+m_re_r,
\qquad n_i,m_i\in\mathbb N.
$$

Suatu titik bernilai $K$

$$
\varphi:M\longrightarrow K
$$

ditentukan secara tunggal oleh $a_i=\varphi(e_i)$. Untuk setiap relasi
binomial yang berlaku di $M$, nilai-nilai tersebut harus memenuhi

$$
a_1^{n_1}\cdots a_r^{n_r}
=a_1^{m_1}\cdots a_r^{m_r}.
$$

<!-- upstream_entity: Kommutative Monoidringe/Funktorialität im Monoid/Surjektivität/Fakt -->

### Lema: injektivitas dan surjektivitas {#br-ak-2025-2026-l17-lem-01}

Misalkan $R$ gelanggang komutatif tak nol, $M,N$ monoid komutatif, dan

$$
\varphi:M\longrightarrow N
$$

homomorfisme monoid. Pemetaan $\varphi$ injektif (berturut-turut, surjektif)
jika dan hanya jika homomorfisme aljabar-$R$ terkait

$$
\widetilde\varphi:R[M]\longrightarrow R[N]
$$

injektif (berturut-turut, surjektif).

#### Bukti {#br-ak-2025-2026-l17-lem-01-proof}

Misalkan $\varphi$ injektif dan

$$
\widetilde\varphi\!\left(\sum_{m\in M}a_mX^m\right)
=\sum_{m\in M}a_mX^{\varphi(m)}=0.
$$

Karena semua $\varphi(m)$ berbeda, setiap $a_m=0$. Sebaliknya, jika
$\varphi$ tidak injektif, ambil $m\ne k$ dengan
$\varphi(m)=\varphi(k)$. Maka

$$
\widetilde\varphi(X^m)=\widetilde\varphi(X^k),
\qquad X^m\ne X^k,
$$

sehingga $\widetilde\varphi$ tidak injektif.

Jika $\varphi$ surjektif, untuk setiap unsur
$\sum_{n\in N}a_nX^n\in R[N]$ pilih pra-citra $m_n\in M$ dari $n$. Unsur
$\sum_{n\in N}a_nX^{m_n}$ merupakan pra-citranya. Sebaliknya, jika
$n\in N$ tidak berada dalam citra $\varphi$, monomial tak nol $X^n$ tidak
dapat berada dalam citra $\widetilde\varphi$.

<!-- upstream_entity: Kommutative Monoidringe/Erzeugendensystem für Monoid und Polynomring/Fakt -->

### Korolari: sistem pembangkit {#br-ak-2025-2026-l17-cor-02}

Misalkan $R$ gelanggang komutatif tak nol, $M$ monoid komutatif, dan
$(m_i)_{i\in I}$ suatu keluarga unsur $M$. Keluarga $(m_i)_{i\in I}$
membangkitkan $M$ sebagai monoid jika dan hanya jika
$(X^{m_i})_{i\in I}$ membangkitkan $R[M]$ sebagai aljabar-$R$.

#### Bukti {#br-ak-2025-2026-l17-cor-02-proof}

Keluarga $(m_i)_{i\in I}$ membangkitkan $M$ tepat ketika homomorfisme monoid

$$
\mathbb N^{(I)}\longrightarrow M
$$

surjektif. Menurut Lema 17.11, ini ekuivalen dengan surjektivitas

$$
\begin{aligned}
R[X_i\mid i\in I]&\longrightarrow R[M],\\
X_i&\longmapsto X^{m_i},
\end{aligned}
$$

yang tepat berarti bahwa $X^{m_i}$ membangkitkan $R[M]$ sebagai aljabar-$R$.

<!-- upstream_entity: Kommutative Monoidringe/Funktorialität im Ring/Fakt -->

### Korolari: funktorialitas terhadap gelanggang dasar {#br-ak-2025-2026-l17-cor-03}

Misalkan $R$ gelanggang komutatif, $S$ aljabar-$R$, dan $M$ monoid
komutatif. Terdapat homomorfisme aljabar-$R$ alami

$$
\begin{aligned}
R[M]&\longrightarrow S[M],\\
\sum_{m\in M}a_mX^m&\longmapsto\sum_{m\in M}a_mX^m,
\end{aligned}
$$

dengan koefisien dari $R$ dipandang melalui pemetaan struktur $R\to S$.

#### Bukti {#br-ak-2025-2026-l17-cor-03-proof}

Terapkan Teorema 17.5 pada aljabar-$R$ $S[M]$ dan homomorfisme monoid alami
$M\to S[M]$.

## Grup selisih suatu monoid {#br-ak-2025-2026-l17-s03}

Kita ingin mengetahui kapan gelanggang monoid merupakan domain integral
(yang hanya mungkin jika gelanggang dasarnya integral) dan bagaimana lapangan
pecahannya dapat dideskripsikan. Di dalam lapangan pecahan, setiap unsur tak
nol harus dapat dibalik; khususnya, demikian pula monomial-monomial $X^m$.
Karena itu wajar untuk mencari suatu grup aditif yang memuat $M$.

**Catatan edisi:** setelah menggunakan $X^m$ secara konsisten sebagai notasi
monomial, sumber mencetak $T^m$ pada kalimat terakhir. Edisi ini mempertahankan
notasi $X^m$ yang telah ditetapkan dalam kuliah ini.

<!-- upstream_entity: Kommutative Monoidtheorie/Differenzengruppe zu Monoid/Definition -->

### Definisi: grup selisih {#br-ak-2025-2026-l17-def-03}

Misalkan $M$ monoid komutatif. Himpunan *selisih formal*

$$
\Gamma(M)=\{m-n\mid m,n\in M\}
$$

dilengkapi dengan penjumlahan

$$
(m_1-n_1)+(m_2-n_2)
:=(m_1+m_2)-(n_1+n_2)
$$

dan identifikasi

$$
m_1-n_1=m_2-n_2
$$

jika terdapat $u\in M$ sehingga

$$
u+m_1+n_2=u+m_2+n_1.
$$

Objek $\Gamma(M)$ disebut *grup selisih* dari $M$.

Soal 17.13 meminta pembaca membuktikan bahwa objek tersebut benar-benar
suatu grup. Konstruksinya meniru pembentukan lapangan pecahan, dengan notasi
perkalian diganti oleh notasi penjumlahan. Sebagai contoh,

$$
\Gamma(\mathbb N)=\mathbb Z.
$$

Terdapat homomorfisme monoid alami

$$
\begin{aligned}
M&\longrightarrow\Gamma(M),\\
m&\longmapsto m-0.
\end{aligned}
$$

Biasanya kita menulis $m$ saja untuk $m-0$. Pemetaan ini tidak selalu
injektif, karena pada relasi identifikasi di atas boleh muncul unsur tambahan
$u$. Kita sekarang mengkarakterisasi monoid yang tidak memerlukan unsur
tambahan tersebut.

<!-- upstream_entity: Kommutative Monoidtheorie/Monoid mit Kürzungsregel/Definition -->

### Definisi: hukum pembatalan {#br-ak-2025-2026-l17-def-04}

Suatu monoid komutatif $M$ dikatakan memenuhi *hukum pembatalan* (atau
disebut monoid kanselatif) jika, dari

$$
m+n=m+k,
\qquad m,n,k\in M,
$$

selalu mengikuti $n=k$.

Untuk monoid semacam itu, pemetaan $M\to\Gamma(M)$ bersifat injektif; lihat
Soal 17.16.

---

**Provenans edisi.** Terjemahan dan produksi pembaca: OpenAI Codex
gpt-5.6-sol, Ultra. Sumber, pengarang, dan lisensi komponen dipertahankan
seperti dinyatakan dalam metadata dan berkas hak edisi.
