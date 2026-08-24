---
title: "Kuliah 15 - Varietas Afin dan Kuasiafin, Gelanggang Lokal, dan Tangkai"
stable_id: br-ak-2025-2026-l15
language: id-ID
upstream_title: "Kurs:Algebraische Kurven (Osnabrück 2025-2026)/Vorlesung 15"
upstream_pageid: 165904
upstream_revid: 1051357
upstream_timestamp: "2025-08-18T08:08:44Z"
upstream_mediawiki_sha1: 72949885b4a089a2f30ea68019ce98ea55d1939d
source_url: "https://de.wikiversity.org/w/index.php?oldid=1051357"
authority_manifest: authority/wikiversity/unit-15/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 86e394725e766838f01eb035ca53044c4d3b85ff20eb99f8fecda9c2a0156425
lecture_xml_sha256: 303749263b928e32c699cae0f7ebbccd419ec3455ec79eee6afb137a8a0887ca
lecture_expanded_tex_sha256: f369a5fb5de001525bb9fd50bf62df84c33fd02a3bc329dfc55874bb8a89d4e2
license: "CC BY-SA 4.0 for translated course text; media retain component rights in authority/RIGHTS-unit-15.csv"
translation_status: complete
---

# Kuliah 15: Varietas Afin dan Kuasiafin, Gelanggang Lokal, dan Tangkai {#br-ak-2025-2026-l15}

## Varietas afin dan kuasiafin {#br-ak-2025-2026-l15-s01}

<!-- upstream_entity: Affine Varietät/Algebraisch abgeschlossener Körper/K-Punkte/Definition -->

### Definisi: varietas afin {#br-ak-2025-2026-l15-def-01}

Misalkan $K$ lapangan tertutup secara aljabar dan $R$ aljabar-$K$ bertipe
hingga. Spektrum-$K$

$$
V=K\!-\!\operatorname{Spek}(R),
$$

dengan setiap himpunan terbuka Zariski $U\subseteq V$ dilengkapi gelanggang
fungsi aljabar $\Gamma(U,\mathcal O)$, disebut *varietas afin*.

Suatu subhimpunan terbuka dari varietas afin, dengan setiap himpunan
terbukanya juga dilengkapi gelanggang struktur, disebut *varietas kuasiafin*.
Varietas kuasiafin dapat ditutupi oleh berhingga banyak himpunan terbuka
berbentuk $D(f)$, yang masing-masing merupakan varietas afin. Sebagian
pengarang hanya menyebut spektrum-$K$ yang tak tereduksi sebagai varietas.

Teorema 14.9 menjamin bahwa tidak ada informasi yang hilang ketika kita
beralih dari $R$ ke

$$
V=K\!-\!\operatorname{Spek}(R),
$$

karena gelanggang $R$ dapat diperoleh kembali sebagai
$\Gamma(V,\mathcal O)$. Hal ini tidak dapat dilakukan hanya dari ruang
topologisnya.

## Gelanggang lokal {#br-ak-2025-2026-l15-s02}

Untuk suatu titik $P$ dalam spektrum-$K$, kita tertarik pada semua fungsi
aljabar yang terdefinisi di $P$ dan mempunyai penyajian rasional pada suatu
lingkungan $P$. Fungsi-fungsi tersebut terdefinisi pada lingkungan yang
berbeda, dan tidak ada lingkungan terkecil tempat semua fungsi aljabar yang
terdefinisi di $P$ sekaligus terdefinisi. Kita mempunyai sistem gelanggang

$$
\bigl(\Gamma(U,\mathcal O)\bigr)_{P\in U}
$$

yang hendak dipahami secara geometris dan aljabar. Sistem ini ternyata
mempunyai limit yang bermakna - disebut *limit langsung* atau *kolimit* - dan
limit tersebut sama dengan pelokalan $R_{\mathfrak m}$ pada ideal maksimal
$\mathfrak m$ yang bersesuaian dengan $P$. Kita mulai dengan istilah
aljabarnya.

<!-- upstream_entity: Kommutative Ringtheorie/Lokaler Ring/Definition -->

### Definisi: gelanggang lokal {#br-ak-2025-2026-l15-def-02}

Suatu gelanggang komutatif $R$ disebut *lokal* jika $R$ mempunyai tepat satu
ideal maksimal.

Syarat ini ekuivalen dengan tertutupnya komplemen grup satuan $R$ terhadap
penjumlahan. Gelanggang lokal yang paling sederhana adalah lapangan. Kepada
setiap gelanggang lokal $R$ dengan ideal maksimal $\mathfrak m$ dikaitkan
lapangan faktor $R/\mathfrak m$, yang disebut *lapangan residu* $R$. Kita
akan segera melihat bahwa setiap titik spektrum-$K$ mempunyai gelanggang
lokal yang secara aljabar menggambarkan "rupa lokal" varietas di titik itu.

<!-- upstream_entity: Kommutative Ringtheorie/Lokalisierung für Primideal/Definition -->

### Definisi: pelokalan pada ideal prima {#br-ak-2025-2026-l15-def-03}

Misalkan $R$ gelanggang komutatif dan $\mathfrak p$ ideal prima. Pelokalan
terhadap sistem multiplikatif

$$
S=R\setminus\mathfrak p
$$

disebut *pelokalan* $R$ pada $\mathfrak p$ dan ditulis $R_{\mathfrak p}$.
Dengan demikian,

$$
R_{\mathfrak p}
=\left\{\frac fg\mathrel{\Big|}f\in R,\ g\notin\mathfrak p\right\}.
$$

Teorema berikut menjelaskan alasan penamaan itu.

<!-- upstream_entity: Kommutative Ringtheorie/Lokalisierung/Lokaler Ring/Fakt -->

### Teorema: pelokalan pada ideal prima bersifat lokal {#br-ak-2025-2026-l15-thm-01}

Misalkan $R$ gelanggang komutatif dan $\mathfrak p$ ideal prima di $R$.
Maka $R_{\mathfrak p}$ merupakan gelanggang lokal dengan ideal maksimal

$$
\mathfrak pR_{\mathfrak p}
=\left\{\frac fg\mathrel{\Big|}f\in\mathfrak p,\ g\notin\mathfrak p\right\}.
$$

#### Bukti {#br-ak-2025-2026-l15-thm-01-proof}

Himpunan yang ditampilkan memang suatu ideal di dalam

$$
R_{\mathfrak p}
=\left\{\frac fg\mathrel{\Big|}f\in R,\ g\notin\mathfrak p\right\}.
$$

Kita tunjukkan bahwa komplemen $\mathfrak pR_{\mathfrak p}$ hanya terdiri
atas satuan, sehingga ideal itu harus maksimal. Misalkan

$$
q=\frac fg\in R_{\mathfrak p}
$$

tetapi $q\notin\mathfrak pR_{\mathfrak p}$. Maka $f,g\notin\mathfrak p$,
sehingga pecahan kebalikannya $g/f$ juga terletak di dalam pelokalan.

## Lapangan pecahan dan lapangan fungsi {#br-ak-2025-2026-l15-s03}

Jika $R$ suatu daerah integral, lapangan pecahannya merupakan pelokalan pada
ideal prima nol. Sekarang kita tunjukkan bahwa untuk varietas afin tak
tereduksi $K\!-\!\operatorname{Spek}(R)$, setiap fungsi aljabar secara alami
terletak di dalam lapangan pecahan.

<!-- upstream_entity: K-Spektrum/Integritätsbereich/Algebraische Funktion ist Element im Quotientenkörper/Fakt -->

### Lema: fungsi aljabar sebagai unsur lapangan pecahan {#br-ak-2025-2026-l15-lem-01}

Misalkan $K$ lapangan tertutup secara aljabar, $R$ aljabar-$K$ integral
bertipe hingga, dan

$$
\varnothing\ne U\subseteq K\!-\!\operatorname{Spek}(R)
$$

suatu subhimpunan terbuka. Terdapat homomorfisme aljabar-$R$ injektif yang
ditentukan secara tunggal

$$
\Gamma(U,\mathcal O)\longrightarrow Q(R).
$$

Khususnya, setiap fungsi aljabar yang terdefinisi pada himpunan terbuka tak
kosong $U$ merupakan suatu unsur lapangan pecahan $Q(R)$.

#### Bukti {#br-ak-2025-2026-l15-lem-01-proof}

Ambil $P\in U$ dan misalkan pada suatu lingkungan $P$ fungsi aljabar $f$
diberikan oleh

$$
f=G/H,
\qquad G,H\in R,
\qquad H\ne0.
$$

Pecahan $G/H$ langsung dapat dipandang sebagai unsur lapangan pecahan.
Misalkan $Q\in U$ titik lain dengan penyajian

$$
f=G'/H'.
$$

Menurut Lema 14.8 dan karena $R$ merupakan daerah integral,

$$
GH'=G'H
$$

di $R$. Jadi unsur lapangan pecahan tersebut terdefinisi dengan baik.
Pemetaan yang diperoleh jelas suatu homomorfisme gelanggang dan membuat
diagram

$$
\begin{matrix}
R &&\\
\downarrow & \searrow &\\
\Gamma(U,\mathcal O)&\longrightarrow&Q(R)
\end{matrix}
$$

komutatif. Sifat-sifat ini juga menentukan pemetaan tersebut secara tunggal:
fungsi aljabar yang berasal dari unsur $R$ harus dipetakan ke unsur yang sama
di lapangan pecahan, sehingga citra setiap pecahan sudah ditentukan.

Untuk injektivitas, jika $G/H=0$ di lapangan pecahan, maka $G=0$ dan fungsi
yang bersesuaian adalah fungsi nol pada $D(H)$. Untuk penyajian lain
$G'/H'$ bagi fungsi yang sama, hubungan di atas kembali memberikan $G'=0$;
jadi fungsi itu nol pada seluruh $U$.

Ketunggalan juga langsung menunjukkan bahwa untuk dua himpunan terbuka
$U\subseteq U'$, diagram

$$
\begin{matrix}
\Gamma(U',\mathcal O)&&\\
\downarrow&\searrow&\\
\Gamma(U,\mathcal O)&\longrightarrow&Q(R)
\end{matrix}
$$

komutatif, dengan homomorfisme restriksi di sebelah kiri. Mulai sekarang,
dalam kasus integral kita mengidentifikasi fungsi aljabar dengan unsur
lapangan pecahan yang bersesuaian.

## Filter topologis dan tangkainya {#br-ak-2025-2026-l15-s04}

Hasil bagian sebelumnya mengatakan bahwa lapangan pecahan dapat diperoleh
sebagai gabungan terurut dari semua gelanggang seksi
$\Gamma(U,\mathcal O)$ ketika $U$ menjelajahi semua himpunan terbuka tak
kosong. Konstruksi serupa dapat dilakukan untuk sistem himpunan terbuka yang
terstruktur dengan sesuai. Untuk itu kita memerlukan konsep filter.

<!-- upstream_entity: Topologie/Topologischer Filter/Definition -->

### Definisi: filter topologis {#br-ak-2025-2026-l15-def-04}

Misalkan $X$ ruang topologis. Suatu sistem $F$ yang terdiri atas
subhimpunan-subhimpunan terbuka $X$ disebut *filter topologis* jika, untuk
himpunan terbuka $U,V$, berlaku:

1. $X\in F$;
2. jika $U\in F$ dan $U\subseteq V$, maka $V\in F$;
3. jika $U,V\in F$, maka $U\cap V\in F$.

![Empat lingkaran abu-abu konsentris pada latar transparan](authority/assets/Concentric_Circles.svg)

*Representasi skematis suatu filter lingkungan; Andreas Pietzowski,
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0). Rincian
sumber berada pada kredit media Unit 15.*

<!-- upstream_entity: Topologische Filter/Umgebungsfilter/Definition -->

### Definisi: filter lingkungan {#br-ak-2025-2026-l15-def-05}

Misalkan $X$ ruang topologis dan $M\subseteq X$. Sistem

$$
\mathcal U(M)
=\{U\subseteq X\mid U\text{ terbuka dan }M\subseteq U\}
$$

disebut *filter lingkungan* $M$.

Sistem ini jelas suatu filter topologis. Khususnya, untuk satu titik $P\in X$
terdapat filter lingkungan $\mathcal U(P)$ yang menghimpun semua lingkungan
terbuka titik itu.

Misalkan diberikan dua lingkungan terbuka $U_1,U_2$ dari $P$ dan dua fungsi
aljabar

$$
f_1\in\Gamma(U_1,\mathcal O),
\qquad
f_2\in\Gamma(U_2,\mathcal O).
$$

Pada mulanya jumlah $f_1+f_2$ - demikian pula hasil kalinya - belum
bermakna karena domain definisinya berbeda. Dalam kasus integral, keduanya
dapat dipandang sebagai unsur lapangan pecahan dan dijumlahkan di sana.
Sebagai alternatif, kita dapat beralih ke irisan $U_1\cap U_2$, yang juga
merupakan lingkungan terbuka $P$, lalu menjumlahkan restriksi kedua fungsi
di sana. Sifat penting filter adalah bahwa bersama setiap dua himpunan
terbukanya, filter juga memuat irisannya, dengan inklusi

$$
U_1\cap U_2\subseteq U_1,U_2
$$

dan pemetaan restriksi yang bersesuaian

$$
\Gamma(U_1,\mathcal O),\Gamma(U_2,\mathcal O)
\longrightarrow\Gamma(U_1\cap U_2,\mathcal O).
$$

Pengamatan ini dirumuskan secara tepat melalui himpunan terarah dan sistem
terarah.

<!-- upstream_entity: Ordnungstheorie/Gerichtete Menge/Definition -->

### Definisi: himpunan terarah {#br-ak-2025-2026-l15-def-06}

Suatu himpunan terurut $(I,\preccurlyeq)$ disebut *terurut secara terarah*
atau singkatnya *terarah* jika untuk setiap $i,j\in I$ terdapat $k\in I$
dengan

$$
i,j\preccurlyeq k.
$$

Kita memandang filter topologis sebagai himpunan yang diurutkan oleh inklusi.
Sifat irisan filter membuatnya terarah; arah urutannya adalah

$$
\preccurlyeq\;=\;\supseteq.
$$

<!-- upstream_entity: Geordnetes und gerichtetes System/Von Mengen/Definition -->

### Definisi: sistem terurut dan sistem terarah {#br-ak-2025-2026-l15-def-07}

Misalkan $(I,\preccurlyeq)$ suatu himpunan indeks terurut. Keluarga himpunan

$$
M_i,\qquad i\in I,
$$

disebut *sistem terurut himpunan* jika:

1. untuk $i\preccurlyeq j$ terdapat pemetaan
   $\varphi_{ij}:M_i\to M_j$;
2. untuk $i\preccurlyeq j\preccurlyeq k$ berlaku

   $$
   \varphi_{ik}=\varphi_{jk}\circ\varphi_{ij}.
   $$

Jika himpunan indeksnya juga terarah, keluarga tersebut disebut *sistem
terarah himpunan*.

Jika semua $M_i$ merupakan grup (atau gelanggang) dan semua pemetaan di
antaranya homomorfisme grup (atau homomorfisme gelanggang), kita berbicara
tentang sistem terurut atau terarah grup (atau gelanggang).

<!-- upstream_entity: Geordnetes System/Von Mengen/Kolimes/Definition -->

### Definisi: kolimit {#br-ak-2025-2026-l15-def-08}

Misalkan $(M_i)_{i\in I}$ suatu sistem terarah himpunan. Himpunan

$$
\operatorname{colim}_{i\in I}M_i
=\left(\biguplus_{i\in I}M_i\right)\!\big/\!\sim
$$

disebut *kolimit* (juga *limit langsung* atau *limit induktif*) sistem
tersebut. Di sini $\sim$ adalah relasi ekuivalensi yang menyatakan dua unsur
$m\in M_i$ dan $n\in M_j$ ekuivalen jika terdapat $k\in I$ dengan
$i,j\preccurlyeq k$ dan

$$
\varphi_{ik}(m)=\varphi_{jk}(n).
$$

Secara khusus, $s_i\in M_i$ ekuivalen dengan citranya
$\varphi_{ik}(s_i)\in M_k$ untuk setiap $i\preccurlyeq k$.

**Catatan edisi:** pada kalimat terakhir, sumber menulis $s_i\in M$, padahal
sistem hanya mendefinisikan himpunan-himpunan $M_i$. Edisi ini menampilkan
indeks yang diperlukan, $s_i\in M_i$.

Jika kita mempunyai sistem terarah grup (atau gelanggang), kolimit himpunan
di atas juga dapat diberi struktur grup (atau gelanggang). Dua unsur kolimit
yang diwakili oleh $s_i\in M_i$ dan $s_j\in M_j$ dapat diganti dengan
citranya di suatu $M_k$ dengan $i,j\preccurlyeq k$, lalu operasinya
didefinisikan di $M_k$; lihat Soal 15.23.

Contoh utama kita adalah sistem terarah gelanggang

$$
\Gamma(U,\mathcal O),\qquad U\in F,
$$

yang diarahkan oleh suatu filter topologis. Kolimit sistem ini mendapat nama
tersendiri.

<!-- upstream_entity: Quasiaffine Varietät/Topologischer Filter/Halm der Strukturgarbe/Definition -->

### Definisi: tangkai pada filter {#br-ak-2025-2026-l15-def-09}

Misalkan $(V,\mathcal O)$ varietas kuasiafin dan $F$ filter topologis di
$V$. Kolimit

$$
\mathcal O_F
=\operatorname{colim}_{U\in F}\Gamma(U,\mathcal O)
$$

disebut *tangkai* $\mathcal O$ pada $F$.

Tangkai pada filter lingkungan suatu titik $P$ juga disebut tangkai di $P$
dan ditulis $\mathcal O_P$.

<!-- upstream_entity: K-Spektrum/Algebraisch abgeschlossen/Punkt/Halm ist Lokalisierung/Fakt -->

### Teorema: tangkai di suatu titik adalah pelokalan {#br-ak-2025-2026-l15-thm-02}

Misalkan $R$ aljabar komutatif tereduksi bertipe hingga di atas lapangan
tertutup secara aljabar $K$. Misalkan

$$
P\in K\!-\!\operatorname{Spek}(R)
$$

suatu titik dengan ideal maksimal $\mathfrak m\subseteq R$ yang
bersesuaian. Terdapat isomorfisme alami aljabar-$R$

$$
R_{\mathfrak m}\longrightarrow\mathcal O_P.
$$

#### Bukti {#br-ak-2025-2026-l15-thm-02-proof}

Tangkai $\mathcal O_P$ mempunyai struktur aljabar-$R$ yang tunggal karena
seluruh ruang termasuk dalam filter. Jika $F\in R$ dan
$F\notin\mathfrak m$, fungsi $1/F$ terdefinisi pada lingkungan terbuka
$D(F)$ dari $P$. Di sana berlaku $F\cdot(1/F)=1$, sehingga $F$ menjadi
satuan di dalam kolimit. Berdasarkan sifat universal pelokalan, terdapat
homomorfisme aljabar-$R$

$$
R_{\mathfrak m}\longrightarrow\mathcal O_P.
$$

Kita buktikan bahwa pemetaan ini bijektif. Mula-mula ambil
$f\in\mathcal O_P$. Unsur ini diwakili oleh suatu fungsi aljabar

$$
f\in\Gamma(U,\mathcal O),
\qquad P\in U.
$$

Khususnya, $f$ mempunyai penyajian rasional di $P$: pada $D(H)$ berlaku

$$
f=G/H,
\qquad P\in D(H).
$$

Syarat terakhir berarti $H(P)\ne0$, atau ekuivalen
$H\notin\mathfrak m$. Jadi $G/H\in R_{\mathfrak m}$ dan dipetakan ke $f$.
Ini membuktikan surjektivitas.

Untuk injektivitas, ambil $G/H$ dengan $H\notin\mathfrak m$ dan andaikan
citranya di dalam tangkai adalah nol. Artinya terdapat lingkungan terbuka
$U$ dari $P$ tempat $G/H$ merupakan fungsi nol. Kita boleh memilih

$$
P\in D(H')\subseteq D(H)
$$

dan, berdasarkan Korolari 14.10, menuliskan pada himpunan itu

$$
G/H=G'/H'=0.
$$

Menurut Lema 14.8,

$$
H(H')^2G=0
$$

di $R$. Karena $H$ dan $H'$ menjadi satuan di $R_{\mathfrak m}$, diperoleh
$G/H=0$ di dalam pelokalan.

<!-- upstream_entity: K-Spektrum/Integritätsbereich/Durchschnitt von lokalen Ringen/Fakt -->

### Lema: seksi sebagai irisan gelanggang lokal {#br-ak-2025-2026-l15-lem-02}

Misalkan $K$ lapangan tertutup secara aljabar, $R$ aljabar-$K$ integral
bertipe hingga, dan

$$
U\subseteq K\!-\!\operatorname{Spek}(R)
$$

suatu himpunan terbuka. Maka

$$
\Gamma(U,\mathcal O)=\bigcap_{P\in U}\mathcal O_P,
$$

dengan irisan diambil di dalam lapangan pecahan $Q(R)$.

#### Bukti {#br-ak-2025-2026-l15-lem-02-proof}

Untuk setiap $P\in U$ terdapat homomorfisme gelanggang injektif

$$
\Gamma(U,\mathcal O)\longrightarrow\mathcal O_P
\longrightarrow Q(R).
$$

Karena itu terdapat homomorfisme gelanggang injektif

$$
\Gamma(U,\mathcal O)
\longrightarrow\bigcap_{P\in U}\mathcal O_P.
$$

Sebaliknya, misalkan $f\in Q(R)$ berada di dalam irisan di sebelah kanan.
Untuk setiap $P\in U$, terdapat penyajian $f=G/H$ dengan

$$
P\in D(H)\subseteq U.
$$

Ini langsung berarti bahwa $f$ merupakan fungsi aljabar pada $U$.

<!-- upstream_entity: Quasiaffine Varietäten/Irreduzibel/Funktionenkörper/Definition -->

### Definisi: lapangan fungsi {#br-ak-2025-2026-l15-def-10}

Misalkan $V$ varietas kuasiafin tak tereduksi. Tangkai $\mathcal O_V$ pada
filter semua himpunan terbuka tak kosong di $V$ merupakan suatu lapangan,
yang disebut *lapangan fungsi* $V$.

---

**Provenans edisi.** Terjemahan dan produksi pembaca: OpenAI Codex
gpt-5.6-sol, Ultra. Sumber, pengarang, dan lisensi komponen dipertahankan
seperti dinyatakan dalam metadata dan berkas hak edisi.
