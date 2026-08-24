---
title: "Solusi Publik Lembar Kerja 12"
stable_id: br-ak-2025-2026-w12-solutions
language: id-ID
upstream_map: authority/wikiversity/unit-12/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: a37f874ffa17dd35ed4375f2956786793e475fcd5e2ded0333207c546e7e91db
public_solution_count: 2
upstream_solution_revisions: "Soal 12.6=1068040; Soal 12.12=1089724"
solution_ex06_xml_sha256: 501ac61733a2cb317b0195407b74729e5f09beace36a9da8764708e036ea11c6
solution_ex12_xml_sha256: e59d798d41b83bf59e9fb4931a5f122ffb538ee3f8341669ab8b07db9a632894
license: "CC BY-SA 4.0"
translation_status: complete
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 12 {#br-ak-2025-2026-w12-solutions}

Sumber hanya menyediakan solusi publik untuk Soal 12.6 dan 12.12 pada batas
revisi yang dibekukan. Tidak ada solusi tambahan yang dibuat untuk edisi ini.

<!-- upstream_solution: K-Spektrum/Algebraisch abgeschlossen/K-Punkt und maximales Ideal/Aufgabe/Lösung; pageid=168418; revid=1068040 -->
<!-- upstream_solution_revid: 1068040 -->

## Solusi Soal 12.6 {#br-ak-2025-2026-w12-sol-06}

Suatu titik-$K$ adalah homomorfisme aljabar-$K$

$$
\varphi:A\longrightarrow K.
$$

Karena $A$ merupakan aljabar-$K$, homomorfisme ini surjektif. Kernelnya
merupakan ideal maksimal di $A$. Karena $A$ bertipe hingga di atas lapangan
yang tertutup secara aljabar, teorema bahwa ideal maksimal pada aljabar bertipe
hingga di atas lapangan tertutup secara aljabar adalah ideal titik dapat
diterapkan. Oleh sebab itu lapangan residu pada setiap ideal maksimal sama
dengan $K$.

**Catatan edisi:** soal menamai aljabar dengan $R$, sedangkan sumber solusi
memakai $A$. Notasi $A$ dari sumber solusi dipertahankan di sini.

[Kembali ke Soal 12.6](#br-ak-2025-2026-w12-ex-06).

<!-- upstream_solution: K-Spektrum/Einheitsideal und leere Nullstellenmenge/Nilpotent und ganze Nullstellenmenge/Aufgabe/Lösung; pageid=21584; revid=1089724 -->
<!-- upstream_solution_revid: 1089724 -->

## Solusi Soal 12.12 {#br-ak-2025-2026-w12-sol-12}

Jika $\mathfrak a$ adalah ideal satuan, maka
$V(\mathfrak a)=\varnothing$, karena $1$ tidak lenyap di titik mana pun.
Kebalikannya berlaku jika $K$ tertutup secara aljabar. Memang, dari

$$
V(1)\subseteq V(\mathfrak a)
$$

—karena kedua himpunan itu kosong—Nullstellensatz Hilbert langsung
memberikan

$$
1=1^n\in\mathfrak a.
$$

Untuk $K=\mathbb R$, kebalikan tersebut tidak berlaku. Polinom

$$
F=X^2+1
$$

bukan satuan, tetapi lokus nolnya kosong.

Jika $\mathfrak a$ nilpoten, maka setiap unsurnya nilpoten dan karena itu
lenyap di bawah setiap homomorfisme gelanggang ke suatu lapangan, sebab
lapangan tereduksi. Untuk lapangan dasar yang tertutup secara aljabar,
kebalikannya kembali berlaku. Jika $V(\mathfrak a)=X$, maka untuk setiap
$f\in\mathfrak a$ berlaku

$$
V(\mathfrak a)\subseteq V(f)=X=V(0).
$$

Menurut Nullstellensatz Hilbert, ini mengakibatkan

$$
f^n=0,
$$

sehingga $f$ nilpoten. Dalam gelanggang Noether, hal ini juga mengakibatkan
ideal $\mathfrak a$ sendiri nilpoten.

Di atas lapangan berhingga, kebalikan ini tidak berlaku. Untuk
$K=\mathbb F_2$, polinom

$$
X^2-X\in K[X]
$$

tidak nilpoten, tetapi lenyap pada kedua titik—yakni pada semua titik—dari
$K$.

[Kembali ke Soal 12.12](#br-ak-2025-2026-w12-ex-12).
