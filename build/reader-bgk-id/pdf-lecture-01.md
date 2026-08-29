---
title: "Kuliah 1 - Sistem Persamaan Linear yang Bergantung pada Parameter dan Bundel Vektor"
stable_id: br-bgk-2019-l01
language: id-ID
source_course: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)"
source_author: "Holger Brenner"
frozen_revision_contributor: "Arbota"
upstream_title: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)/Vorlesung 1"
upstream_pageid: 109003
upstream_revid: 1069568
upstream_timestamp: "2026-02-06T07:06:14Z"
upstream_mediawiki_sha1: 6e619f166a640629f33e73ac518faff6daff2810
source_url: "https://de.wikiversity.org/w/index.php?oldid=1069568"
authority_manifest: authority/wikiversity-bgk/unit-01/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: ad271f5ad69f9990dbe3082c22f8c52b7a4c58494c8f6614350078535d4f2ba1
lecture_xml: authority/wikiversity-bgk/unit-01/lecture-01.xml
lecture_xml_sha256: 68d7783afc1c1353c3298638f150095dad79c2424c356bc09bc50c023ab86392
lecture_expanded_tex: authority/wikiversity-bgk/unit-01/lecture-01-expanded.tex
lecture_expanded_tex_sha256: 7b22065d36d75d01385aabd97edd6e5416f817e1ebf96af9543023242135c77d
official_pdf: authority/artifacts/bgk-lecture-01-official.pdf
official_pdf_sha256: be4103eb7f4631f300c8f5f895de82094d0cd5ffac603eff9d5c7b77aef3d3ce
license: "Frozen semantic course text and this translation: CC BY-SA 4.0. Official PDF and media retain their recorded component notices; no blanket relicensing claim is made."
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra."
---

# Kuliah 1: Sistem Persamaan Linear yang Bergantung pada Parameter dan Bundel Vektor {#br-bgk-2019-l01}

## Sistem persamaan linear yang bergantung pada parameter {#br-bgk-2019-l01-s01}

Kita perhatikan persamaan linear real

$$
7u-5v+2w=0.
$$

Himpunan penyelesaiannya

$$
L=\left\{(u,v,w)\in\mathbb R^3\mid 7u-5v+2w=0\right\}
\subset\mathbb R^3
$$

merupakan subruang vektor real berdimensi dua dari $\mathbb R^3$.
Menyelesaikan persamaan linear semacam itu antara lain berarti menentukan
suatu basis bagi $L$. Dalam kasus ini, misalnya,

$$
L=\left\langle
\begin{pmatrix}5\\7\\0\end{pmatrix},
\begin{pmatrix}2\\0\\-7\end{pmatrix}
\right\rangle.
$$

Metode penyelesaiannya pada umumnya tidak bergantung pada koefisien konkret
persamaan linear itu, meskipun nanti akan kita lihat batas dari pernyataan
ini. Jika angka-angka konkret diganti dengan koefisien yang secara fungsional
bergantung pada parameter, kita dapat bertanya bagaimana ruang penyelesaian
berubah bersama parameter tersebut. Sebagai contoh, perhatikan persamaan
linear yang bergantung pada parameter $s$,

$$
7u-5v+(s^2-3s-10)w=0.
$$

Untuk setiap $s$, ruang penyelesaian $L_s$ bergantung pada $s$, tetapi tetap
merupakan subruang berdimensi dua,

$$
L_s\subset\mathbb R^3.
$$

Dengan kata lain, ruang penyelesaian itu adalah sebuah bidang yang bergerak
di dalam ruang ketika $s$ berubah. Kita dapat menanyakan untuk nilai $s$ mana
vektor

$$
\begin{pmatrix}5\\-3\\8\end{pmatrix}
$$

merupakan penyelesaian, yakni termasuk dalam $L_s$. Kita juga dapat bertanya
apakah terdapat parameter berbeda $s,t$ dengan

$$
L_s=L_t
$$

sebagai subruang dari $\mathbb R^3$; apakah selalu ada basis ruang
penyelesaian berbentuk

$$
\left\langle
\begin{pmatrix}a\\b\\0\end{pmatrix},
\begin{pmatrix}c\\0\\d\end{pmatrix}
\right\rangle;
$$

atau apakah selalu ada vektor penyelesaian berbentuk

$$
\begin{pmatrix}1\\0\\e\end{pmatrix}.
$$

Ingatlah bahwa algoritme untuk menyelesaikan sistem persamaan linear, yaitu
eliminasi Gauss, bercabang ketika koefisien tertentu bernilai $0$ atau
menjadi $0$ selama algoritme berlangsung. Persamaan

$$
7u-5v+0w=0
$$

mempunyai ruang penyelesaian

$$
\left\langle
\begin{pmatrix}5\\7\\0\end{pmatrix},
\begin{pmatrix}0\\0\\1\end{pmatrix}
\right\rangle
$$

dan tidak memuat vektor berbentuk
$\begin{pmatrix}1&0&e\end{pmatrix}^{\mathsf T}$. Karena $s=-2$ dan $s=5$
adalah akar-akar polinom kuadrat $s^2-3s-10$, untuk kedua nilai parameter
itu persamaan berparameter di atas berubah menjadi

$$
7u-5v+0w=0.
$$

Jadi, untuk kedua nilai tersebut, $L_s$ tidak mempunyai vektor berbentuk
$\begin{pmatrix}1&0&e\end{pmatrix}^{\mathsf T}$. Untuk semua nilai parameter
lainnya, ruang penyelesaiannya memuat vektor

$$
\begin{pmatrix}
1\\[2pt]0\\[2pt]-\dfrac{7}{s^2-3s-10}
\end{pmatrix}.
$$

Dengan demikian, aspek tertentu dari ruang penyelesaian itu sendiri
bergantung secara fungsional pada parameter.

Wajar jika ketergantungan sebuah persamaan linear atau sistem persamaan
linear pada parameter dipelajari dalam dua tahap. Pada tahap pertama,
koefisien-koefisien persamaan diperlakukan sebagai variabel, yaitu sebagai
*parameter universal*, lalu dipelajari bagaimana ruang penyelesaian berubah
bersamanya. Secara khusus, kita ingin memahami lompatan kualitatif dalam
perilaku ruang penyelesaian. Pada tahap kedua, kita memberikan syarat
tambahan yang lebih atau kurang membatasi parameter universal itu, atau
membiarkannya bergantung secara fungsional pada parameter lain.

### Contoh 1.1: satu persamaan dalam dua variabel {#br-bgk-2019-l01-exa-01}

Kita perhatikan persamaan linear real umum

$$
su+tv=0
$$

dalam variabel $u,v$ dan parameter $s,t$, yang berperan sebagai koefisien
tak tentu. Kita ingin memahami ruang penyelesaian

$$
L_{(s,t)}=\left\{(u,v)\mid su+tv=0\right\}\subseteq\mathbb R^2
$$

sebagai fungsi dari parameter $(s,t)$. Kasus ekstrem terjadi pada
$(s,t)=(0,0)$: persamaan dipenuhi oleh setiap $(u,v)$, sehingga ruang
penyelesaiannya adalah seluruh $\mathbb R^2$, yang berdimensi dua. Jika
$(s,t)\ne(0,0)$, ruang penyelesaiannya berdimensi satu, dan sebuah vektor
basis bagi garis penyelesaian itu adalah

$$
\begin{pmatrix}t\\-s\end{pmatrix}.
$$

Jadi, di atas ruang parameter $\mathbb R^2\setminus\{(0,0)\}$, ruang
penyelesaiannya dapat ditulis seragam sebagai

$$
L_{(s,t)}=
\left\{c\begin{pmatrix}t\\-s\end{pmatrix}\mathrel{\Big|}c\in\mathbb R\right\}.
$$

Penafsiran yang lebih ringkas diperoleh dengan memandang ruang penyelesaian
total

$$
L=\left\{(s,t,u,v)\mid su+tv=0\right\}\subseteq\mathbb R^4.
$$

Perhatikan bahwa $L$ bukan subruang vektor linear dari $\mathbb R^4$.
Ruang penyelesaian untuk nilai parameter khusus $(s,t)$ diperoleh dengan
memotong $L$ dengan bidang afin $(s,t)\times\mathbb R^2$. Di bawah proyeksi
total

$$
L\longrightarrow\mathbb R^2\times\mathbb R^2
\stackrel{p_{s,t}}{\longrightarrow}\mathbb R^2,
\qquad (s,t,u,v)\longmapsto(s,t),
$$

$L_{(s,t)}$ adalah serat di atas $(s,t)$. Di dalam ruang penyelesaian total,
terlihat baik perubahan garis penyelesaian terhadap parameter maupun
degenerasinya menjadi bidang penyelesaian di atas titik nol. Perilaku di luar
titik parameter nol dideskripsikan oleh pembatasan

$$
L'=L\setminus\bigl(\{(0,0)\}\times\mathbb R^2\bigr)
=p^{-1}\!\left(\mathbb R^2\setminus\{(0,0)\}\right)
\longrightarrow\mathbb R^2\setminus\{(0,0)\}.
$$

Setiap serat proyeksi terbatas ini adalah ruang penyelesaian berdimensi satu.
Selain itu, terdapat bijeksi

$$
\begin{aligned}
\left(\mathbb R^2\setminus\{(0,0)\}\right)\times\mathbb R
&\longrightarrow L',\\
(s,t;c)&\longmapsto(s,t,ct,-cs),
\end{aligned}
$$

yang linear pada setiap parameter $(s,t)$. Di ruas kiri terdapat hasil kali
langsung ruang basis $\mathbb R^2\setminus\{(0,0)\}$ dan serat $\mathbb R$,
yang tidak bergantung pada titik basis. Di ruas kanan terdapat keluarga garis
yang berubah-ubah di $\mathbb R^2$, tetapi bijeksi tersebut menerjemahkan
satu gambaran ke gambaran yang lain.

> **Catatan edisi - urutan faktor dan ruang basis.** Pada definisi $L'$,
> sumber mencetak $\mathbb R^2\times(0,0)$, padahal kesamaan dengan
> $p^{-1}(\mathbb R^2\setminus\{(0,0)\})$ mengharuskan serat di atas titik
> nol yang dibuang, yaitu $\{(0,0)\}\times\mathbb R^2$. Prosa sumber kemudian
> mencetak $\mathbb R^2\times(0,0)$ sekali lagi sebagai ruang basis, sedangkan
> domain bijeksi yang langsung mendahuluinya adalah
> $\mathbb R^2\setminus\{(0,0)\}$. Edisi mengikuti kedua pemetaan yang
> ditampilkan dan mencatat ketidaksesuaian ini secara terbuka.

### Contoh 1.2: satu persamaan dalam tiga variabel {#br-bgk-2019-l01-exa-02}

Kita perhatikan persamaan linear real umum

$$
ru+sv+tw=0
$$

dalam variabel $u,v,w$ dan parameter $r,s,t$, yang berperan sebagai
koefisien tak tentu. Kita ingin memahami ruang penyelesaian

$$
L_{(r,s,t)}=
\left\{(u,v,w)\mid ru+sv+tw=0\right\}\subseteq\mathbb R^3
$$

sebagai fungsi dari parameter $(r,s,t)$. Pada $(r,s,t)=(0,0,0)$, ruang
penyelesaiannya adalah seluruh $\mathbb R^3$. Jika
$(r,s,t)\ne(0,0,0)$, ruang penyelesaiannya berdimensi dua. Kita keluarkan
titik nol dari ruang parameter dan perhatikan ruang penyelesaian total

$$
\begin{aligned}
L={}&\left\{(r,s,t,u,v,w)\mathrel{\Big|}
ru+sv+tw=0, (r,s,t)\ne(0,0,0)\right\}\\
&\subseteq\left(\mathbb R^3\setminus\{(0,0,0)\}\right)\times\mathbb R^3,
\end{aligned}
$$

bersama proyeksi $p$ ke $\mathbb R^3\setminus\{(0,0,0)\}$. Serat $p$ di
atas parameter khusus $(r,s,t)$ adalah ruang penyelesaian $L_{(r,s,t)}$
untuk persamaan yang ditentukan oleh tupel parameter itu.

> **Catatan edisi - notasi titik nol dan cakupan hasil kali.** Sumber
> mencetak $\mathbb R^3\setminus\{0,0,0\}\times\mathbb R^3$ pada inklusi
> ini, tanpa menuliskan titik nol sebagai tupel dan tanpa tanda kurung yang
> memisahkan ruang basis dari faktor serat. Proyeksi pada kalimat berikutnya
> menetapkan maksudnya secara unik. Edisi menuliskannya sebagai
> $(\mathbb R^3\setminus\{(0,0,0)\})\times\mathbb R^3$.

Dapatkah kita memberikan basis bagi setiap ruang penyelesaian yang
bergantung pada parameter dengan cara aljabar dan komputasional yang jelas?
Karena titik nol telah dikeluarkan,

$$
\mathbb R^3\setminus\{(0,0,0)\}
=\{(r,s,t)\mid r\ne0\}\cup
\{(r,s,t)\mid s\ne0\}\cup
\{(r,s,t)\mid t\ne0\}.
$$

Jadi ruang basis dapat ditulis sebagai gabungan tiga himpunan terbuka. Di
atas himpunan terbuka $r\ne0$, misalnya, suatu basis diberikan oleh

$$
(s,-r,0)\quad\text{dan}\quad(t,0,-r).
$$

Syarat $r\ne0$ menjamin bahwa kedua vektor itu bebas linear. Kedua vektor
tersebut bahkan merupakan penyelesaian yang terdefinisi di mana-mana, tetapi
ketika $r=0$ keduanya kehilangan kebebasan linear sehingga tidak membentuk
basis di mana-mana. Bagaimanapun, pemetaan

$$
\begin{aligned}
\{(r,s,t)\mid r\ne0\}\times\mathbb R^2
&\longrightarrow L|_{\{(r,s,t)\mid r\ne0\}},\\
(r,s,t;c,d)&\longmapsto c(s,-r,0)+d(t,0,-r)
\end{aligned}
$$

adalah bijeksi yang sederhana secara komputasional antara hasil kali ruang
basis dengan $\mathbb R^2$ dan ruang penyelesaian di atas
$\{(r,s,t)\mid r\ne0\}$.

Sekarang kita bertanya apakah mungkin memberikan secara global, di seluruh
$\mathbb R^3\setminus\{(0,0,0)\}$, sebuah basis ruang penyelesaian yang
berubah bersama titik basis. Yang ditanyakan ialah keberadaan dua fungsi
$u(r,s,t)$ dan $v(r,s,t)$ bernilai di $\mathbb R^3$ yang selalu membentuk
basis serat terkait, dan khususnya selalu termasuk dalam serat itu. Tanpa
syarat lebih lanjut pada $u$ dan $v$, hal ini mungkin dilakukan dengan
definisi kasus per kasus. Akan tetapi, hal itu tidak lagi mungkin jika kedua
fungsi tersebut disyaratkan kontinu. Karena kontinuitas, fungsi global
$u$ dan $v$ sudah ditentukan oleh nilainya pada himpunan terbuka rapat

$$
U=\{(r,s,t)\mid r\ne0\}
\subseteq\mathbb R^3\setminus\{(0,0,0)\}.
$$

Dengan basis di atas $U$ yang telah diberikan, kita dapat menulis

$$
u=\alpha(r,s,t)\begin{pmatrix}s\\-r\\0\end{pmatrix}
+\beta(r,s,t)\begin{pmatrix}t\\0\\-r\end{pmatrix}
$$

dan

$$
v=\gamma(r,s,t)\begin{pmatrix}s\\-r\\0\end{pmatrix}
+\delta(r,s,t)\begin{pmatrix}t\\0\\-r\end{pmatrix},
$$

dengan $\alpha,\beta,\gamma,\delta$ fungsi real kontinu pada $U$. Kita tidak
dapat mengharapkan fungsi-fungsi koefisien itu terdefinisi di seluruh
$\mathbb R^3$, sehingga argumen dalam kasus kontinu menjadi lebih rumit.
Hasilnya akan mengikuti dari Teorema 2.3; lihat Catatan 2.4.

Karena itu, untuk saat ini kita batasi perhatian pada fungsi rasional yang
penyebutnya boleh memuat suatu pangkat $r$, yakni fungsi rasional pada $U$.
Perhatikan

$$
\begin{aligned}
u
&=\alpha\begin{pmatrix}s\\-r\\0\end{pmatrix}
+\beta\begin{pmatrix}t\\0\\-r\end{pmatrix}\\
&=\frac{P}{r^m}\begin{pmatrix}s\\-r\\0\end{pmatrix}
+\frac{Q}{r^n}\begin{pmatrix}t\\0\\-r\end{pmatrix},
\end{aligned}
$$

dengan $P,Q$ polinom dan faktor $r$ telah dicoret jika mungkin. Karena
$u$ secara keseluruhan terdefinisi pada seluruh $\mathbb R^3$, pangkat $m$
dan, dengan alasan yang sama, $n$, paling besar $1$; jika tidak, $u$ akan
mempunyai sebuah kutub. Untuk $m=n=1$, komponen pertama menghasilkan
persamaan polinomial berbentuk

$$
rN+sP+tQ=0,
\qquad N,P,Q\in\mathbb R[r,s,t].
$$

Dalam hal ini, dengan kata kunci resolusi Koszul,

$$
(N,P,Q)=A(-s,r,0)+B(t,0,-r)+C(0,t,-s)
$$

untuk polinom $A,B,C\in\mathbb R[r,s,t]$. Dengan cara yang sama, $v$
mempunyai representasi melalui $(N',P',Q')$ dan $(A',B',C')$. Tuliskan

$$
X=\mathbb R^3\setminus\{(0,0,0)\}
$$

dan perhatikan pemetaan

$$
\begin{aligned}
\varphi:X\times\mathbb R^3&\longrightarrow L\subseteq X\times\mathbb R^3,\\
(r,s,t;a,b,c)&\longmapsto
(r,s,t;\,a(-s,r,0)+b(t,0,-r)+c(0,t,-s)).
\end{aligned}
$$

Di bawah pemetaan ini, tupel polinom $(A,B,C)$ dan $(A',B',C')$, yang kita
pandang sebagai pemetaan $X\to X\times\mathbb R^3$, dipetakan ke $u$ dan
$v$. Menurut asumsi, $u$ dan $v$ membentuk basis setiap serat $L$, sehingga
$(A,B,C)$ dan $(A',B',C')$ bebas linear pada setiap titik. Tupel
$(t,s,-r)$ dipetakan oleh $\varphi$ ke $0$ pada setiap serat. Oleh karena
itu,

$$
(A,B,C),\qquad(A',B',C'),\qquad(t,s,-r)
$$

membentuk basis $\mathbb R^3$ pada setiap titik: $(t,s,-r)$ tidak mungkin
merupakan kombinasi linear dari dua tupel pertama, sebab setelah menerapkan
$\varphi$ akan diperoleh relasi taktrivial antara $u$ dan $v$. Akan tetapi,
determinan matriks

$$
\begin{pmatrix}
A&B&C\\
A'&B'&C'\\
t&s&-r
\end{pmatrix}
$$

merupakan kombinasi polinomial dari variabel $r,s,t$, sehingga bukan unit
di dalam gelanggang polinom. Dalam kasus real, dari sini belum dapat
disimpulkan bahwa determinan itu mempunyai titik nol real di $X$; misalnya,
bentuknya mungkin $r^2+s^2+t^2$. Namun, jika $\mathbb R$ diganti dengan
$\mathbb C$, argumen aljabarnya tidak berubah, dan dapat disimpulkan bahwa
determinan itu mempunyai titik nol pada

$$
X_{\mathbb C}=\mathbb C^3\setminus\{(0,0,0)\}.
$$

Jadi basis global seperti itu tidak dapat ada di semua titik.

### Contoh 1.3: dua persamaan dalam tiga variabel {#br-bgk-2019-l01-exa-03}

Kita perhatikan sistem persamaan linear real umum

$$
au+bv+cw=0
$$

dan

$$
du+ev+fw=0
$$

dalam variabel $u,v,w$ dan parameter $a,b,c,d,e,f$. Jika parameternya cukup
umum, lebih tepatnya jika kedua persamaan tidak berelasi linear, maka ruang
penyelesaian

$$
L_{(a,b,c,d,e,f)}=
\left\{(u,v,w)\mathrel{\Big|}
au+bv+cw=0\ \text{dan}\ du+ev+fw=0\right\}
\subseteq\mathbb R^3
$$

adalah sebuah garis. Jadi, di bawah syarat ini, parameter menentukan suatu
keluarga garis yang berubah-ubah di $\mathbb R^3$. Ruang parameter yang
relevan bagi keluarga garis tersebut adalah

$$
P=\left\{(a,b,c,d,e,f)\mathrel{\Big|}
(a,b,c)\ \text{dan}\ (d,e,f)\ \text{bebas linear}\right\}.
$$

Secara keseluruhan, kita memperoleh ruang penyelesaian total

$$
\begin{aligned}
L=\{&(a,b,c,d,e,f,u,v,w)\mid
au+bv+cw=0\ \text{dan}\ du+ev+fw=0\}\\
&\subseteq P\times\mathbb R^3,
\end{aligned}
$$

beserta proyeksinya ke $P$.

Dapatkah garis ini, atau sebuah elemen basisnya, diberikan secara global
sebagai fungsi parameter? Jika kedua persamaan dipandang sebagai relasi
ortogonalitas, kita mencari vektor taknol yang tegak lurus terhadap kedua
vektor syarat

$$
\begin{pmatrix}a\\b\\c\end{pmatrix}
\quad\text{dan}\quad
\begin{pmatrix}d\\e\\f\end{pmatrix}.
$$

Vektor hasil kali silang keduanya mempunyai sifat tersebut, yakni

$$
\begin{pmatrix}
bf-ce\\
-af+cd\\
ae-bd
\end{pmatrix}.
$$

Untuk sifat-sifat hasil kali silang yang digunakan di sini, sumber merujuk
ke Lema 33.3 dalam *Lineare Algebra (Osnabrück 2024-2025)*.

Jadi terdapat bijeksi

$$
\begin{aligned}
P\times\mathbb R&\longrightarrow L,\\
(a,b,c,d,e,f;s)&\longmapsto
(a,b,c,d,e,f;s(bf-ce),s(-af+cd),s(ae-bd)).
\end{aligned}
$$

> **Catatan edisi - dua nama koordinat pada sumber.** Sumber menampilkan
> vektor syarat kedua sebagai $(e,f,g)$ meskipun sistem dan ruang parameter
> mendefinisikannya sebagai $(d,e,f)$. Pada pemetaan terakhir, sumber juga
> mencetak komponen tengah $-af+ce$, padahal hasil kali silang yang dicetak
> tepat sebelumnya memberi $-af+cd$. Edisi memakai $(d,e,f)$ dan
> $-af+cd$, yang dapat diverifikasi langsung dari dua persamaan, sambil
> mencatat kedua salah ketik sumber tersebut.

Pada Contoh 1.1 dan Contoh 1.3 terdapat *trivialisasi polinomial global*:
dengan fungsi-fungsi polinomial, objek geometris yang rumit diterjemahkan ke
objek sederhana $P\times\mathbb R$, dengan $P$ ruang basis. Sebaliknya,
trivialisasi global semacam itu tidak mungkin pada Contoh 1.2, walaupun
trivialisasi lokal tersedia di atas tiga himpunan terbuka yang diberikan.
Objek geometris semacam inilah yang disebut bundel vektor.

## Bundel vektor real {#br-bgk-2019-l01-s02}

### Definisi 1.4: bundel vektor real {#br-bgk-2019-l01-def-01}

Misalkan $X$ suatu ruang topologis dan $r\in\mathbb N$. Sebuah *bundel
vektor real dengan rank $r$* adalah sebuah ruang topologis $V$ beserta
pemetaan kontinu

$$
p:V\longrightarrow X
$$

sedemikian sehingga setiap serat $p^{-1}(x)$ merupakan ruang vektor real
berdimensi $r$, dan terdapat suatu penutup terbuka

$$
X=\bigcup_{i\in I}U_i
$$

beserta homeomorfisme-homeomorfisme di atas $U_i$,

$$
\varphi_i:p^{-1}(U_i)\longrightarrow U_i\times\mathbb R^r,
$$

yang pada setiap serat menginduksi isomorfisme linear

$$
(\varphi_i)_x:p^{-1}(x)\longrightarrow\mathbb R^r.
$$

Ruang $V$ juga disebut *ruang total*, sedangkan $X$ disebut *ruang basis*
bundel vektor. Serat di atas $x$ sering ditulis

$$
V_x=p^{-1}(x).
$$

Dalam contoh-contoh di atas, $X$ adalah ruang parameter yang relevan, yaitu
tempat parameter-parameter yang ruang penyelesaiannya berdimensi minimum.
Dimensi ini adalah rank $r$ pada definisi tadi, berturut-turut
$1,2,1$. Pada contoh pertama dan ketiga, penutup terbukanya hanya terdiri
atas ruang basis sendiri; kedua bundel itu mempunyai trivialisasi global.
Pada contoh kedua, terdapat penutup oleh tiga himpunan terbuka yang di
atasnya trivialisasi telah diberikan.

Dalam homeomorfisme

$$
p^{-1}(U)\longrightarrow U\times\mathbb R^r,
$$

ruas kanan diberi topologi produk, $\mathbb R^r$ diberi topologi Euklides
alaminya, dan $p^{-1}(U)$ diberi topologi terinduksi dari $V$. Jadi setiap
serat $V_x$ membawa topologi alami ruang vektor real berdimensi hingga.
Yang dimaksud dengan homeomorfisme *di atas $U$* ialah bahwa diagram

$$
\begin{array}{ccc}
p^{-1}(U)&\stackrel{\varphi}{\longrightarrow}&U\times\mathbb R^r\\
&\searrow p&\downarrow\operatorname{pr}_1\\
&&U
\end{array}
$$

komutatif.

> **Catatan edisi - simbol rank pada diagram.** Diagram sumber mencetak
> $U\times\mathbb R^n$, sedangkan definisi dan semua rumus yang mengapitnya
> menetapkan rank sebagai $r$. Edisi menampilkan $\mathbb R^r$.

Hasil kali $X\times\mathbb R^r$ adalah sebuah bundel vektor yang disebut
*bundel vektor trivial*.

### Lema 1.5: pembatasan bundel vektor {#br-bgk-2019-l01-lem-01}

Misalkan

$$
p:V\longrightarrow X
$$

suatu bundel vektor real di atas ruang topologis $X$. Untuk setiap himpunan
terbuka $W\subseteq X$, pembatasan

$$
p^{-1}(W)\longrightarrow W
$$

juga merupakan bundel vektor.

#### Bukti {#br-bgk-2019-l01-lem-01-proof}

Cukup batasi homeomorfisme-homeomorfisme linear serat demi serat

$$
\varphi_i:p^{-1}(U_i)\longrightarrow U_i\times\mathbb R^r
$$

menjadi

$$
\varphi_i|_{W\cap U_i}:
p^{-1}(W\cap U_i)\longrightarrow(W\cap U_i)\times\mathbb R^r.
$$

$\square$

Pembatasan sebuah bundel vektor pada setiap $U_i$ bersifat trivial. Jadi,
secara lokal setiap bundel vektor bersifat trivial.

### Definisi 1.6: homomorfisme bundel vektor {#br-bgk-2019-l01-def-02}

Misalkan $E$ dan $F$ bundel vektor real di atas ruang topologis $X$.
Sebuah *homomorfisme bundel vektor*

$$
\varphi:E\longrightarrow F
$$

adalah pemetaan kontinu di atas $X$ sedemikian sehingga, untuk setiap
$x\in X$, pemetaan terinduksi

$$
\varphi_x:E_x\longrightarrow F_x
$$

bersifat linear atas $\mathbb R$.

### Definisi 1.7: isomorfisme bundel vektor {#br-bgk-2019-l01-def-03}

Misalkan $E$ dan $F$ bundel vektor real di atas ruang topologis $X$.
Homomorfisme bundel vektor

$$
\varphi:E\longrightarrow F
$$

disebut *isomorfisme* jika terdapat homomorfisme

$$
\psi:F\longrightarrow E
$$

yang, jika dikomposisikan dengan $\varphi$ dalam kedua urutan, menghasilkan
pemetaan identitas.

## Bundel tangen pada manifold {#br-bgk-2019-l01-s03}

Sekarang kita bahas sebuah bundel vektor sangat penting yang terdapat pada
setiap manifold, yaitu bundel tangen.

Untuk setiap titik $P\in M$ pada sebuah manifold terdapat ruang tangen
$T_PM$. Ruang tangen adalah ruang vektor berdimensi $n$, dengan $n$ dimensi
manifold tersebut. Elemen-elemennya adalah vektor tangen, yakni “arah
infinitesimal” di titik itu. Pada awalnya, arah tangen di dua titik yang
berbeda tidak berhubungan: definisinya hanya bergantung pada lingkungan
terbuka sekecil apa pun di sekitar masing-masing titik, dan berkat sifat
Hausdorff lingkungan-lingkungan itu dapat dipilih saling lepas.

Gambaran ini sangat berbeda untuk sebuah himpunan terbuka
$V\subseteq\mathbb R^n$. Untuk setiap $Q\in V$, ruang tangen $T_QV$ dapat
diidentifikasi secara alami dengan ruang vektor ambien $\mathbb R^n$.
Sebuah vektor $v\in\mathbb R^n$ dipasangkan dengan vektor tangen yang
ditentukan oleh kurva linear $t\mapsto Q+tv$. Karena identifikasi ini berlaku
untuk setiap titik, terdapat kesejajaran langsung antara ruang-ruang tangen
untuk

$$
Q\in V\subseteq\mathbb R^n.
$$

Sebuah manifold ditutupi oleh himpunan-himpunan terbuka yang difeomorfik
dengan himpunan terbuka dalam ruang Euklides. Karena itu, masuk akal untuk
menduga bahwa berbagai ruang tangennya tidak sepenuhnya terisolasi. Konsep
bundel tangen menggabungkan semua ruang tangen dan mencerminkan keterkaitan
lokal di antara ruang-ruang tersebut.

> **Ilustrasi sumber - `Tangent_bundle.svg`.** Dua visualisasi bundel tangen
> sebuah lingkaran. Pada gambar atas, ruang tangen di setiap titik $P$ pada
> lingkaran diletakkan menyinggung lingkaran dan direalisasikan sebagai
> subruang afin berdimensi satu di $\mathbb R^2$. Pembenaman ini menimbulkan
> perpotongan yang sebenarnya tidak ada dalam bundel tangen, karena titik
> basis $P$ juga harus diperhitungkan. Pada gambar bawah, ruang-ruang tangen
> disusun sejajar di atas titik-titik lingkaran dan menghasilkan sebuah
> silinder.

![Diagram bundel tangen dengan ruang tangen sebagai serat di atas setiap titik manifold](authority/assets/bgk-tangent-bundle-500.png){height=70%}

### Definisi 1.8: bundel tangen sebagai gabungan lepas {#br-bgk-2019-l01-def-04}

Misalkan $M$ suatu manifold terdiferensial. Himpunan

$$
TM=\biguplus_{P\in M}T_PM,
$$

beserta pemetaan proyeksi

$$
\begin{aligned}
\pi:TM&\longrightarrow M,\\
(P,v)&\longmapsto P,
\end{aligned}
$$

disebut *bundel tangen* dari $M$.

Sebuah titik $u\in TM$ selalu mempunyai titik basis $P\in M$ dan merupakan
elemen ruang tangen $T_PM$. Titik itu biasanya ditulis $(P,v)$ dengan
$P\in M$ dan $v\in T_PM$. Untuk suatu himpunan terbuka
$V\subseteq\mathbb R^n$,

$$
TV=V\times\mathbb R^n,
$$

jadi ia merupakan ruang hasil kali. Hal ini tidak berlaku pada manifold
sebarang. Mula-mula bundel tangen hanya menggabungkan secara lepas berbagai
ruang tangen, tanpa mengidentifikasi ruang tangen yang berbeda satu sama
lain. Namun, topologi yang akan segera diberikan pada bundel tangen
menambahkan suatu “struktur ketetanggaan” di antara ruang-ruang tangen.

### Definisi 1.9: pemetaan tangen {#br-bgk-2019-l01-def-05}

Misalkan $M$ dan $N$ manifold terdiferensial dan

$$
\varphi:M\longrightarrow N
$$

suatu pemetaan terdiferensial. Misalkan $TM$ dan $TN$ bundel tangen yang
bersesuaian. *Pemetaan tangen*

$$
T(\varphi):TM\longrightarrow TN
$$

adalah gabungan lepas pemetaan-pemetaan tangen pada setiap titik, yakni

$$
T(\varphi)=\biguplus_{P\in M}T_P(\varphi).
$$

### Contoh 1.10: trivialisasi lokal dari sebuah bagan {#br-bgk-2019-l01-exa-04}

Misalkan $M$ suatu manifold terdiferensial dan

$$
\alpha:U\longrightarrow V
$$

sebuah bagan, dengan $V\subseteq\mathbb R^n$ terbuka. Bagan itu menginduksi
bijeksi alami

$$
\begin{aligned}
T(\alpha^{-1}):TV=V\times\mathbb R^n&\longrightarrow TU,\\
(Q,v)&\longmapsto
\left(\alpha^{-1}(Q),[s\mapsto\alpha^{-1}(Q+sv)]\right).
\end{aligned}
$$

Di sini $s$ bergerak dalam suatu interval real $I$ yang dipilih sehingga
$Q+sv\in V$ (bandingkan Lema 77.5 pada *Analysis (Osnabrück 2014-2016)*).
Karena $V\times\mathbb R^n$ merupakan hasil kali ruang-ruang topologis,

$$
TV=V\times\mathbb R^n
$$

sendiri merupakan ruang topologis. Wajar untuk memindahkan topologi ini ke
$TU$, lalu membangun topologi pada seluruh bundel tangen $TM$.

### Definisi 1.11: topologi bundel tangen {#br-bgk-2019-l01-def-06}

Misalkan $M$ suatu manifold terdiferensial berdimensi $n$ dan

$$
TM=\biguplus_{P\in M}T_PM
$$

bundel tangennya, dengan proyeksi

$$
\begin{aligned}
\pi:TM&\longrightarrow M,\\
(P,v)&\longmapsto P.
\end{aligned}
$$

Bundel tangen diberi topologi yang didefinisikan sebagai berikut: suatu
himpunan bagian $W\subseteq TM$ terbuka jika dan hanya jika, untuk setiap
bagan

$$
\alpha:U\longrightarrow V,
$$

himpunan

$$
T(\alpha)\left(W\cap\pi^{-1}(U)\right)
$$

terbuka di $V\times\mathbb R^n$.

Khususnya, untuk setiap himpunan terbuka $U\subseteq M$, prabayang

$$
\pi^{-1}(U)=TU\subseteq TM
$$

terbuka; dengan kata lain, proyeksi $\pi$ kontinu. Dengan ketetapan ini,
bundel tangen manifold terdiferensial merupakan bundel vektor real. Jika

$$
M=\bigcup_{i\in I}U_i
$$

adalah suatu penutup terbuka oleh himpunan-himpunan $U_i$ yang homeomorfik
dengan himpunan terbuka $V_i\subseteq\mathbb R^n$, maka bagan-bagan

$$
\alpha_i:U_i\longrightarrow V_i
$$

langsung memberikan trivialisasi

$$
TM|_{U_i}=TU_i
\stackrel{T(\alpha_i)}{\longrightarrow}
TV_i=V_i\times\mathbb R^n.
$$

Sangat banyak sifat manifold tercermin pada sifat bundel tangennya. Bundel
tangen dapat bersifat trivial sekalipun $M$ tidak homeomorfik dengan suatu
himpunan terbuka di $\mathbb R^n$.
