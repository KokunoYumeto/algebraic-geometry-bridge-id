---
title: "Solusi Publik Lembar Kerja 29"
stable_id: br-ak-2012-w29-solutions
language: id-ID
source_course: "Algebraische Kurven (Osnabrück 2012)"
source_author: "Holger Brenner"
frozen_revision_contributors: "Soal 29.2: Arbota; Soal 29.3: Arbota"
upstream_map: authority/wikiversity/unit-29/ORDERED_EXERCISE_MAP.json
upstream_map_sha256: 75b07cabcb83cc12a6fd1259017f7e169c0ded461e7b7c94e65f033b71d12bc9
authority_manifest: authority/wikiversity/unit-29/UNIT_AUTHORITY_MANIFEST.json
authority_manifest_sha256: ec3b34ad387ae827ecaa365c4def3b0550f74b629d0db3873a7cc28dc0831bc5
candidate_evidence: authority/wikiversity/unit-29/worksheet-solution-candidates-api.json
public_solution_count: 2
negative_public_solution_count: 8
negative_solution_numbers: "1, 4-10"
upstream_solution_revisions: "Soal 29.2=1094621; Soal 29.3=1090273"
solution_xml_sha256: "2=2b468a1f7d9bebff884c001c3a475a212601b022896953c97e6a55026cf38f66; 3=50771bcf86505ee8429426f3488ef46af450a258629d4403a2bc16aa74abcaff"
license: "CC BY-SA 4.0 for the frozen semantic source; official 2012 PDF witnesses retain their component notices recorded in the Unit 29 rights ledger"
no_blanket_relicensing_claim: true
independent_derivative_non_endorsement: true
translation_status: complete
translation_provenance: "OpenAI Codex gpt-5.6-sol, Ultra"
source_corrections: 0
---

```{=latex}
\clearpage
```

# Solusi Publik Lembar Kerja 29 {#br-ak-2012-w29-solutions}

Pada batas revisi yang dibekukan, sumber hanya menyediakan solusi publik
untuk Soal 29.2 dan 29.3. Delapan calon halaman solusi lainnya dinyatakan
tidak ada oleh kueri otoritas yang dibekukan. Tidak ada solusi tambahan yang
dibuat untuk edisi ini.

<!-- upstream_solution: Ebene algebraische Kurven/Z mod 5/Einheitskreis und x^3-2y^2+3/Durchschnitt und unendlich ferne Punkte/Aufgabe/Lösung; pageid=21303; revid=1094621 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1094621 -->

## Solusi Soal 29.2 {#br-ak-2012-w29-sol-02}

a. Kita jumlahkan kedua persamaan

$$
2X^2+2Y^2-2=0
\qquad\text{dan}\qquad
X^3-2Y^2+3=0
$$

dan memperoleh syarat

$$
X^3+2X^2+1=0.
$$

Untuk nilai-nilai yang mungkin, yaitu $x=0,1,2,3,4$, hasil substitusinya
berturut-turut ialah $1,4,2,1,2$. Jadi syarat itu tidak dapat dipenuhi, dan
karena itu perpotongan kedua kurva di $\mathbb A_K^2$ kosong.

b. Yang dicari adalah titik-titik dalam $\mathbb P_K^2$ yang secara bersamaan
memenuhi

$$
X^2+Y^2-Z^2=0
\qquad\text{dan}\qquad
Z=0.
$$

Hal ini menghasilkan syarat

$$
X^2+Y^2=0.
$$

Kuadrat-kuadrat dalam $\mathbb Z/(5)$ adalah $0,1,4$. Solusi $(0,0,0)$ tidak
diizinkan karena tidak merepresentasikan suatu titik proyektif, dan kita
memperoleh solusi-solusi $(\pm1,\pm2)$ dan $(\pm2,\pm1)$. Karena yang dicari
adalah titik proyektif, komponen pertama dapat dinormalkan menjadi $1$, dan
komponen kedua harus bernilai $2$ atau $-2=3$. Jadi terdapat dua titik di tak
hingga,

$$
(1,2,0)
\qquad\text{dan}\qquad
(1,3,0).
$$

c. Kedua persamaan

$$
X^3-2Y^2Z+3Z^3=0
\qquad\text{dan}\qquad
Z=0
$$

langsung menghasilkan $X^3=0$, sehingga $X=0$. Dengan demikian, satu-satunya
titik di tak hingga adalah $(0,1,0)$.

d. Menurut definisi, penutupan proyektif adalah penutupan Zariski. Karena
$V(X^2+Y^2-1)$ merupakan himpunan titik berhingga, himpunan itu sudah tertutup
dan sama dengan penutupannya. Namun, menurut bagian b,
$V_+(X^2+Y^2-Z^2)$ memuat titik-titik tambahan. Jadi himpunan terakhir itu
bukan penutupan proyektifnya.

<!-- upstream_solution: Projektive Gerade/K-Punkte/Lokale Ringe isomorph/Aufgabe/Lösung; pageid=21573; revid=1090273 -->
<!-- upstream_solution_url: https://de.wikiversity.org/w/index.php?oldid=1090273 -->

## Solusi Soal 29.3 {#br-ak-2012-w29-sol-03}

Setiap titik $P\in\mathbb P_K^1$ terletak pada sebuah garis afin

$$
P\in\mathbb A_K^1=D_+(L)\subset\mathbb P_K^1,
$$

dengan $L$ suatu bentuk linear homogen. Selanjutnya, dengan melakukan
translasi pada garis afin itu, kita dapat mengandaikan bahwa titik yang
bersangkutan adalah titik asal. Hal tersebut dapat dilakukan untuk setiap
titik dan tidak mengubah gelanggang lokalnya. Oleh karena itu, semua gelanggang
lokal itu saling isomorfik. Gelanggang lokal di titik asal pada garis afin
adalah pelokalan

$$
K[X]_{(X)}.
$$
