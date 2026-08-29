---
title: "Kuliah 6 - Eksak, Evaluasi Global, serta Tarik dan Dorong Berkas"
stable_id: br-bgk-2019-l06
language: id-ID
source_course: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)"
source_author: "Holger Brenner"
frozen_revision_contributor: "Bocardodarapti"
upstream_title: "Kurs:Bündel, Garben und Kohomologie (Osnabrück 2019-2020)/Vorlesung 6"
upstream_pageid: 109010
upstream_revid: 1003728
upstream_timestamp: "2025-06-08T15:29:32Z"
upstream_mediawiki_sha1: 0dfea13421076e8f6486836e9fc799822bf52053
source_url: "https://de.wikiversity.org/w/index.php?oldid=1003728"
authority_manifest: authority/wikiversity-bgk/unit-06/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: 69a10e682e853c6f386afbc68438605846e5096220b21bd1e827c07633a79244
lecture_xml: authority/wikiversity-bgk/unit-06/lecture-06.xml
lecture_xml_sha256: 8d60efeb0563ba0268a61940d94a71c8fd489c2e3d6e83cc61c785e75cdb1d54
lecture_expanded_tex: authority/wikiversity-bgk/unit-06/lecture-06-expanded.tex
lecture_expanded_tex_sha256: 0bdf28cb69d063b1782b7b42eb2212241e109f66ba382368dcd8e782d5ae829d
official_pdf: authority/artifacts/bgk-lecture-06-official.pdf
official_pdf_sha256: 55fbef2b5d9eae950ac7ab064a8029f2e2932c49280a98a4a7ec6ed16262c75d
license: "Frozen semantic course text and this translation: CC BY-SA 4.0. Official PDF witnesses retain their recorded component notices; no blanket relicensing claim is made."
non_endorsement: "Edisi Indonesia independen ini tidak menyiratkan dukungan dari penulis, Wikiversity, Wikimedia Foundation, atau lembaga sumber mana pun."
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra."
---

# Kuliah 6: Eksak, Evaluasi Global, serta Tarik dan Dorong Berkas {#br-bgk-2019-l06}

## Eksak {#br-bgk-2019-l06-s01}

### Definisi 6.1: kompleks berkas {#br-bgk-2019-l06-def-01}

Misalkan $X$ sebuah ruang topologis, $\mathcal F_n$ berkas grup komutatif
pada $X$, dan

$$
\varphi_n:\mathcal F_{n-1}\longrightarrow\mathcal F_n
$$

homomorfisme-homomorfisme berkas. Kita mengatakan bahwa terbentuk sebuah
*kompleks berkas* apabila

$$
\operatorname{im}\varphi_n\subseteq\ker\varphi_{n+1}
$$

berlaku.

### Definisi 6.2: eksak {#br-bgk-2019-l06-def-02}

Misalkan $X$ sebuah ruang topologis dan $\mathcal F_\bullet$ sebuah kompleks
berkas grup komutatif pada $X$. Kompleks tersebut disebut *eksak* apabila

$$
\operatorname{im}\varphi_n=\ker\varphi_{n+1}
$$

untuk semua $n\in\mathbb Z$.

### Lema 6.3: karakterisasi eksak pada tangkai {#br-bgk-2019-l06-lem-01}

Misalkan $X$ sebuah ruang topologis dan

$$
\mathcal F\longrightarrow\mathcal G\longrightarrow\mathcal H
$$

sebuah kompleks berkas grup komutatif pada $X$. Kompleks ini eksak tepat
ketika, untuk setiap titik $P\in X$, kompleks tangkainya

$$
\mathcal F_P\longrightarrow\mathcal G_P\longrightarrow\mathcal H_P
$$

eksak.

#### Bukti {#br-bgk-2019-l06-lem-01-proof}

Kita beri nama situasi tersebut

$$
\mathcal F\xrightarrow{\alpha}\mathcal G\xrightarrow{\beta}\mathcal H.
$$

Menurut Korolari 4.11, ini merupakan kompleks berkas tepat ketika semua
pemetaan pada tangkai merupakan kompleks. Anggap kompleksnya eksak, jadi

$$
\operatorname{im}\alpha=\ker\beta.
$$

Pilih $P\in X$ dan ambil $s\in\mathcal G_P$ dengan
$\beta_P(s)=0$. Ada lingkungan terbuka $U$ dari $P$ tempat $s$ diwakili oleh
sebuah seksi $s$, dan ada lingkungan terbuka yang lebih kecil

$$
P\in V\subseteq U
$$

sedemikian sehingga

$$
\beta_V(s|_V)=0.
$$

Unsur $s\in\mathcal G(V)$ (restriksi ini tetap kita sebut $s$) berada di
kernel $\beta_V$, dan karena itu berada di citra berkas dari $\alpha$. Jadi
ada lingkungan terbuka

$$
P\in W\subseteq V
$$

sedemikian sehingga $s$ berada di citra pemetaan

$$
\alpha_W:\mathcal F(W)\longrightarrow\mathcal G(W).
$$

Maka germ $s$ berada di citra $\alpha_P$. Ini membuktikan bahwa kompleks
tangkai eksak. Arah sebaliknya diperoleh dengan menerapkan kesamaan citra dan
kernel pada setiap tangkai (dan fakta bahwa kesamaan seksi berkas dapat diuji
secara lokal).

### Definisi 6.4: barisan eksak pendek {#br-bgk-2019-l06-def-03}

Sebuah kompleks eksak

$$
0\longrightarrow\mathcal F\longrightarrow\mathcal G\longrightarrow
\mathcal H\longrightarrow0
$$

berkas grup komutatif pada ruang topologis $X$ disebut *barisan eksak pendek*.

Dengan demikian, pemetaan pertama khususnya injektif dan pemetaan terakhir
surjektif sebagai pemetaan berkas (yakni surjektif secara lokal pada setiap
titik).

### Lema 6.5: barisan berkas dari barisan grup topologis {#br-bgk-2019-l06-lem-02}

Misalkan

$$
0\longrightarrow F\longrightarrow G\longrightarrow H\longrightarrow0
$$

sebuah barisan eksak pendek grup topologis komutatif (dengan homomorfisme
grup kontinu). Anggap $F$ memakai topologi terinduksi dari $G$, dan
surjeksi

$$
p:G\longrightarrow H
$$

memiliki sifat berikut: untuk setiap $h\in H$ terdapat lingkungan terbuka

$$
h\in W\subseteq H
$$

dan seksi kontinu terhadap $p$ di atas $W$. Maka, untuk setiap ruang
topologis $X$, barisan berkas pemetaan kontinu yang bersesuaian

$$
0\longrightarrow C^0(-,F)\longrightarrow C^0(-,G)\longrightarrow
C^0(-,H)\longrightarrow0
$$

juga eksak.

#### Bukti {#br-bgk-2019-l06-lem-02-proof}

Jelas bahwa ini merupakan kompleks berkas grup komutatif pada $X$. Injektivitas
di kiri juga jelas. Untuk eksak di tengah, misalkan $U\subseteq X$ terbuka
dan $\varphi:U\to G$ kontinu dengan $p\circ\varphi$ pemetaan nol. Citra
$\varphi$ berada di $F$; karena $F$ memakai topologi terinduksi dari $G$,
fungsi $\varphi:U\to F$ juga kontinu.

Untuk surjektivitas berkas di kanan, ambil titik $P\in X$ dan pemetaan
kontinu $\psi:V\to H$ yang didefinisikan pada lingkungan terbuka $V$ dari
$P$. Tuliskan $\psi(P)=h$. Menurut hipotesis ada lingkungan terbuka

$$
h\in W\subseteq H
$$

dan seksi $s:W\to G$ dengan

$$
p\circ s=\operatorname{Id}_W.
$$

Ambil

$$
U:=V\cap\psi^{-1}(W).
$$

Maka $s\circ\psi$, dibatasi ke $U$, merupakan seksi kontinu bernilai di $G$
yang dipetakan oleh $p$ ke $\psi$.

### Contoh 6.6: barisan eksponensial {#br-bgk-2019-l06-exa-01}

Pertimbangkan barisan eksak pendek

$$
0\longrightarrow2\pi\mathrm i\,\mathbb Z\longrightarrow\mathbb C
\xrightarrow{\operatorname{exp}}\mathbb C^{\times}
\longrightarrow0
$$

dari grup-grup topologis. Eksak di tengah mengikuti Satz 21.5 (Analysis
(Osnabrück 2021--2023), bagian (2)); sifat homomorfismenya mengikuti persamaan fungsional
fungsi eksponensial. Menurut Satz 21.6 (Analysis (Osnabrück 2021--2023)),
fungsi eksponensial kompleks surjektif ke $\mathbb C\setminus\{0\}$ dan
merupakan sebuah pemetaan ruang penutup (lihat Contoh 21.3, Funktionentheorie
(Osnabrück 2023--2024)). Karena logaritma tersedia secara lokal, hipotesis
Lema 6.5 terpenuhi. Jadi, untuk setiap ruang topologis $X$, diperoleh barisan
eksak pendek berkas

$$
0\longrightarrow C^0(-,\mathbb Z)\longrightarrow C^0(-,\mathbb C)
\longrightarrow C^0(-,\mathbb C^{\times})\longrightarrow0.
$$

Barisan ini disebut *barisan eksponensial kontinu kompleks*. Di kiri terdapat
berkas konstan lokal dengan nilai di $\mathbb Z$; di tengah, berkas fungsi
kontinu bernilai kompleks; dan di kanan, berkas fungsi kontinu bernilai
kompleks yang tidak memiliki titik nol. Jika $X=\mathbb C^{\times}$, evaluasi
global pemetaan terakhir tidak surjektif karena fungsi identitas tidak berada
di dalam citranya.

> **Catatan edisi - tahun pada rujukan sumber.** Walaupun kursus ini berjudul
> 2019--2020, dua permukaan sumber berbeda: PDF terminal mencetak rujukan
> Analysis (Osnabrück 2014--2016), sedangkan saksi TeX semantik saat ini
> menyebut Analysis 2021--2023 dan Funktionentheorie 2023--2024. Semua tahun
> dipertahankan sebagai identitas sumber masing-masing, tanpa menyimpulkan
> adanya penyelarasan edisi.

## Evaluasi global {#br-bgk-2019-l06-s02}

### Lema 6.7: evaluasi global mempertahankan kompleks {#br-bgk-2019-l06-lem-03}

Misalkan $X$ sebuah ruang topologis dan

$$
\mathcal F\xrightarrow{d}\mathcal G\xrightarrow{d'}\mathcal H
$$

sebuah kompleks homomorfisme berkas grup komutatif pada $X$. Maka

$$
\Gamma(X,\mathcal F)\longrightarrow\Gamma(X,\mathcal G)
\longrightarrow\Gamma(X,\mathcal H)
$$

juga merupakan sebuah kompleks.

#### Bukti {#br-bgk-2019-l06-lem-03-proof}

Hipotesisnya berarti tepat bahwa $d'\circ d$ merupakan pemetaan nol. Karena
itu, evaluasi globalnya juga merupakan pemetaan nol.

### Lema 6.8: evaluasi global eksak-kiri {#br-bgk-2019-l06-lem-04}

Misalkan $X$ sebuah ruang topologis dan

$$
0\longrightarrow\mathcal F\xrightarrow{d}\mathcal G
\xrightarrow{d'}\mathcal H
$$

sebuah kompleks eksak homomorfisme berkas grup komutatif pada $X$. Maka

$$
0\longrightarrow\Gamma(X,\mathcal F)\longrightarrow\Gamma(X,\mathcal G)
\longrightarrow\Gamma(X,\mathcal H)
$$

juga eksak.

#### Bukti {#br-bgk-2019-l06-lem-04-proof}

Menurut Lema 6.7, barisan seksi global tersebut merupakan kompleks. Eksak
berarti bahwa, pada setiap titik $P\in X$,

$$
0\longrightarrow\mathcal F_P\longrightarrow\mathcal G_P
\longrightarrow\mathcal H_P
$$

eksak pada tangkai.

Ambil $s\in\Gamma(X,\mathcal F)$ dengan $d(s)=0$ di
$\Gamma(X,\mathcal G)$. Maka $d(s)_P=0$ pada setiap titik. Oleh karena itu
$s_P=0$ untuk setiap $P$, dan Lema 4.4 memberi $s=0$. Pemetaan di kiri
injektif.

Selanjutnya, ambil $t\in\Gamma(X,\mathcal G)$ dengan
$d'(t)=0$ di $\Gamma(X,\mathcal H)$. Eksak pada tangkai berarti bahwa untuk
setiap $P$, germ $t_P$ berada di $\mathcal F_P$. Dengan Soal 5.5, ini
menyiratkan bahwa $t$ sendiri merupakan seksi di $\mathcal F$.

Jadi evaluasi global pada berkas grup abelian merupakan sebuah *funktor
eksak-kiri kovarian aditif*.

## Tarik dan dorong {#br-bgk-2019-l06-s03}

Sampai sekarang kita hanya membahas berkas dan hubungan di antaranya pada
sebuah ruang topologis tetap. Sekarang kita mempertimbangkan ruang-ruang
topologis yang dihubungkan oleh sebuah pemetaan kontinu.

### Definisi 6.9: praberkas dorong maju {#br-bgk-2019-l06-def-04}

Untuk pemetaan kontinu

$$
\varphi:X\longrightarrow Y
$$

dan praberkas $\mathcal F$ pada $X$, praberkas pada $Y$ yang pada setiap
himpunan terbuka $U\subseteq Y$ diberikan oleh

$$
(\varphi_*\mathcal F)(U):=\mathcal F\bigl(\varphi^{-1}(U)\bigr)
$$

disebut *praberkas dorong maju* dari $\mathcal F$ melalui $\varphi$.

Jika $V\subseteq W$ terbuka, maka

$$
\varphi^{-1}(V)\subseteq\varphi^{-1}(W),
$$

sehingga tersedia pemetaan restriksi alami dan memang diperoleh sebuah
praberkas.

### Lema 6.10: dorong maju berkas adalah berkas {#br-bgk-2019-l06-lem-05}

Untuk pemetaan kontinu $\varphi:X\to Y$ dan berkas $\mathcal F$ pada $X$,
praberkas dorong maju $\varphi_*\mathcal F$ merupakan sebuah berkas.

#### Bukti {#br-bgk-2019-l06-lem-05-proof}

Misalkan

$$
V=\bigcup_{i\in I}V_i
$$

sebuah penutup terbuka dari himpunan terbuka $V\subseteq Y$. Maka
$\varphi^{-1}(V_i)$, untuk $i\in I$, merupakan penutup terbuka dari
$\varphi^{-1}(V)$. Jika $s,t\in(\varphi_*\mathcal F)(V)$ memenuhi

$$
s|_{V_i\cap V_j}=t|_{V_i\cap V_j},
$$

maka, setelah dibaca di $X$,

$$
s|_{\varphi^{-1}(V_i)\cap\varphi^{-1}(V_j)}
=t|_{\varphi^{-1}(V_i)\cap\varphi^{-1}(V_j)}.
$$

Sifat berkas pertama untuk $\mathcal F$ memberi $s=t$ di
$\mathcal F(\varphi^{-1}(V))$, dan karenanya di $(\varphi_*\mathcal F)(V)$.

Sebaliknya, ambil seksi-seksi $s_i\in\mathcal F(\varphi^{-1}(V_i))$ yang
kompatibel pada semua irisan. Dengan menerjemahkannya kembali ke $X$, sifat
pengeleman berkas $\mathcal F$ menghasilkan sebuah seksi di

$$
\mathcal F(\varphi^{-1}(V))=(\varphi_*\mathcal F)(V).
$$

> **Catatan edisi - jenis seksi pada bukti Lema 6.10.** Sumber menulis
> $s_i\in\mathcal F(V_i)$, walaupun $\mathcal F$ adalah praberkas pada $X$
> dan $V_i\subseteq Y$. Bentuk yang berjenis adalah
> $s_i\in\mathcal F(\varphi^{-1}(V_i))$; bentuk ini dipakai di atas dan
> penyimpangan sumber dicatat, bukan disamarkan.

### Lema 6.11: tangkai praberkas dorong maju {#br-bgk-2019-l06-lem-06}

Untuk pemetaan kontinu $\varphi:X\to Y$, titik $Q\in Y$, dan praberkas
$\mathcal F$ pada $X$, tangkai praberkas dorong maju $\varphi_*\mathcal F$ di
$Q$ adalah

$$
\operatorname*{colim}_{\substack{V\subseteq Y,\;V\text{ terbuka}\\Q\in V}}
\mathcal F(\varphi^{-1}(V))
=
\operatorname*{colim}_{\substack{U\subseteq X\\
\exists\text{ lingkungan terbuka }V\ni Q:\,\varphi^{-1}(V)\subseteq U}}
\mathcal F(U).
$$

> **Catatan edisi - indeks lingkungan pada sumber.** Notasi sumber menulis
> “ada lingkungan terbuka $Q\in V$” di dalam indeks kolimit kedua; ini dibaca
> sebagai “ada lingkungan terbuka $V\ni Q$”. Terjemahan menampilkan bentuk
> yang eksplisit dan bertipe.

Lihat Soal 6.5. Jadi tangkai praberkas dorong maju adalah tangkai praberkas
asal pada suatu filter (yakni filter praimaj dari filter lingkungan
$\mathcal U(Q)$), tetapi secara umum bukan tangkai pada satu titik.

### Definisi 6.12: praberkas tarik balik {#br-bgk-2019-l06-def-05}

Untuk pemetaan kontinu $\varphi:X\to Y$ dan praberkas $\mathcal G$ pada $Y$,
praberkas pada $X$ yang pada himpunan terbuka $U\subseteq X$ diberikan oleh

$$
U\longmapsto
\operatorname*{colim}_{\substack{V\subseteq Y\\U\subseteq\varphi^{-1}(V)}}
\mathcal G(V)
$$

disebut *praberkas tarik balik* dari $\mathcal G$ melalui $\varphi$.

### Definisi 6.13: berkas tarik balik {#br-bgk-2019-l06-def-06}

Untuk pemetaan kontinu $\varphi:X\to Y$ dan berkas $\mathcal G$ pada $Y$,
*berkas tarik balik* adalah berkasisasi dari praberkas tarik balik tersebut.
Berkas ini ditulis

$$
\varphi^{-1}\mathcal G.
$$

### Lema 6.14: tangkai berkas tarik balik {#br-bgk-2019-l06-lem-07}

Untuk pemetaan kontinu $\varphi:X\to Y$ dan berkas $\mathcal G$ pada $Y$,
tangkai berkas tarik balik di titik $P\in X$ sama dengan tangkai $\mathcal G$
di $\varphi(P)$.

Lihat Soal 6.6.
