---
title: "Solusi Publik Lembar Kerja 14"
stable_id: br-ak-2025-2026-w14-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-14/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: 0d223f7f3c56c4714736dfc6eb3dbd40dc8cd3cb30a05f66281a6f2b1b875dbe
public_solution_count: 2
upstream_solution_revisions: "Soal 14.2=1068085; Soal 14.7=1095255"
solution_xml_sha256: "02=1f46f16de8715afb59c5f3ac7ec9c47968093ba3ca322e8bbeb63098b63cd96d; 07=34fd3f0291c291b74dd0b6fcd35aa6bac54d56f2d3aabecdb2f25ff9d2d181f4"
license: "CC BY-SA 4.0"
translation_status: complete
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 14 {#br-ak-2025-2026-w14-solutions}

Pada batas revisi yang dibekukan, sumber hanya menyediakan solusi publik
untuk Soal 14.2 dan 14.7. Tidak ada solusi tambahan yang dibuat untuk edisi
ini.

<!-- upstream_solution: Integritätsbereich/Faktoriell/K-Spektrum/Algebraische Abbildung/Eindeutige Darstellung/Aufgabe/Lösung; pageid=168430; revid=1068085 -->
<!-- upstream_solution_revid: 1068085 -->

## Solusi Soal 14.2 {#br-ak-2025-2026-w14-sol-02}

Misalkan

$$
U=\bigcup_{i\in I}D(H_i)
$$

dengan $I$ berhingga, dan pada setiap $D(H_i)$ fungsi $f$ mempunyai
penyajian

$$
f=\frac{F_i}{H_i},
$$

yakni

$$
f(Q)=\frac{F_i(Q)}{H_i(Q)}
\qquad\text{untuk setiap }Q\in D(H_i).
$$

Pada irisan $D(H_i)\cap D(H_j)$ berlaku

$$
\frac{F_i(Q)}{H_i(Q)}
=f(Q)
=\frac{F_j(Q)}{H_j(Q)}.
$$

Jadi

$$
H_j(Q)F_i(Q)-H_i(Q)F_j(Q)=0
$$

untuk setiap $Q\in D(H_i)\cap D(H_j)$. Oleh karena itu unsur

$$
H_iH_j(H_jF_i-H_iF_j)
$$

menginduksi fungsi nol pada seluruh $K\!-\!\operatorname{Spek}(R)$. Karena
$R$ integral dan $K$ tertutup secara aljabar, teorema identitas memberikan

$$
H_iH_j(H_jF_i-H_iF_j)=0
$$

di $R$. Setelah mengabaikan anggota penutup yang kosong, $H_i$ dan $H_j$
tidak nol; karena $R$ suatu daerah integral, diperoleh

$$
H_jF_i=H_iF_j.
$$

Berdasarkan ketunggalan faktorisasi prima, terdapat unsur $A,B,C,D$ dan
suatu satuan $u$ dengan

$$
H_jF_i=(AB)(CD)=(u^{-1}AD)(uBC)=H_iF_j.
$$

Akibatnya

$$
\frac{F_i}{H_i}
=\frac{uCD}{AD}
=\frac{uC}{A}
=\frac{uBC}{AB}
=\frac{F_j}{H_j}.
$$

Penyajian pecahan $uC/A$ berlaku pada $D(H_i)\cup D(H_j)$. Dengan cara ini,
kita dapat menggabungkan dua anggota penutup dan memperkecil himpunan indeks
$I$. Karena $I$ berhingga, pengulangan proses tersebut akhirnya menghasilkan
satu pecahan $G/H$ yang berlaku pada seluruh $U$. Dengan membatalkan faktor
persekutuan, $G$ dan $H$ dapat dipilih tidak dapat disederhanakan, dan tentu
$U\subseteq D(H)$.

[Kembali ke Soal 14.2](#br-ak-2025-2026-w14-ex-02).

<!-- upstream_solution: Neilsche Parabel/Rationale Funktion mit Pol in (1,1)/Aufgabe/Lösung; pageid=94830; revid=1095255 -->
<!-- upstream_solution_revid: 1095255 -->

## Solusi Soal 14.7 {#br-ak-2025-2026-w14-sol-07}

Ideal maksimal yang bersesuaian dengan titik $P$ diberikan oleh
$(X-1,Y-1)$. Di dalam gelanggang koordinat

$$
R=K[X,Y]/(Y^2-X^3)
$$

berlaku

$$
X^2(X-1)=X^3-X^2=Y^2-X^2=(Y-X)(Y+X).
$$

Karena itu, di dalam lapangan pecahan kita dapat menetapkan

$$
f:=\frac{X^2}{Y-X}=\frac{X+Y}{X-1}.
$$

Penyajian-penyajian ini mendefinisikan fungsi aljabar pada

$$
D(Y-X,X-1)=D(Y-1,X-1)=C\setminus\{P\}.
$$

Untuk menunjukkan bahwa fungsi tersebut tidak terdefinisi pada seluruh
$C$, tinjau pemetaan

$$
\begin{aligned}
\varphi:\mathbb A_K^1&\longrightarrow C,\\
t&\longmapsto(t^2,t^3).
\end{aligned}
$$

Kita mempunyai

$$
\varphi^{-1}(C\setminus\{P\})=\mathbb A_K^1\setminus\{1\}.
$$

Praimaj fungsi $f$ melalui pemetaan ini adalah

$$
\frac{t^2+t^3}{t^2-1}
=\frac{t^2(1+t)}{(t+1)(t-1)}
=\frac{t^2}{t-1}.
$$

Fungsi ini mempunyai kutub di $t=1$ dan tidak dapat diperluas menjadi
fungsi aljabar pada seluruh garis afin. Maka $f$ juga tidak dapat diperluas
secara aljabar ke seluruh $C$.

**Catatan edisi:** pada langkah pembatalan terakhir, sumber menampilkan
$-t^2/(t-1)$. Faktorisasi yang ditampilkan pada baris sebelumnya memberikan
$t^2/(t-1)$ tanpa tanda minus. Kutub di $t=1$ dan kesimpulan pembuktian tidak
berubah.

[Kembali ke Soal 14.7](#br-ak-2025-2026-w14-ex-07).
