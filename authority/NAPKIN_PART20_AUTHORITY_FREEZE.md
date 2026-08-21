# Napkin Part XX authority freeze and build baseline

Freeze date: 2026-08-21 (Europe/Berlin)

## Authority

- Work: Evan Chen, *An Infinitely Large Napkin*, Part XX, “Algebraic Geometry II: Affine Schemes”.
- Official repository: <https://github.com/vEnhance/napkin>
- Frozen commit: `e50be9a0b2b12d080c273619424d0ee13372cc91`
- Frozen tree: `023467410bdf924c8fd38ac04009b4c887cbfb5e`
- Upstream commit timestamp: `2026-08-20T18:59:08Z`
- Immutable archive URL: <https://github.com/vEnhance/napkin/archive/e50be9a0b2b12d080c273619424d0ee13372cc91.zip>
- Official generated Part XX PDF: <https://venhance.github.io/napkin/Parts/part-20-napkin-algebraic-geometry-ii.pdf>

The immutable ZIP is the canonical source witness. The extracted tree was pristine when validated, then acquired normal LaTeX build products during the documented baseline attempt. The selected source, licence, and build-control files were rehashed afterward and all still match this manifest.

## Frozen artifacts

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `authority/artifacts/napkin-e50be9a0b2b12d080c273619424d0ee13372cc91.zip` | 6,438,632 | `A88CDF86CBB749CD9528074BD1789224725CDBF4439B1E580457DD1DB06008D7` |
| `authority/artifacts/part-20-napkin-algebraic-geometry-ii-official.pdf` | 1,352,150 | `4B2AAD5DAC158B84A934CF57BAE37B7D055004134D4B738C452041F24975B69D` |

ZIP validation found 207 entries, 180 files, 26 directory entries, 8,490,743 uncompressed file bytes, one expected top-level directory, no duplicate names, no absolute/traversing paths, and no symbolic-link entries. It was extracted, with the single archive root stripped, to `authority/napkin-e50be9a`.

The official Part XX PDF reports `v1.6.20260820`, 74 A4 pages, pdfTeX 1.40.25, creation/modification time 2026-08-20 21:01:06 local time, and no encryption. `pdfinfo` reports `Tagged: no`; therefore this PDF is not a tagged semantic-accessibility surface.

## Exact Part XX source closure

These are the six files selected by the Part XX block in `Napkin.tex`. None contains another `\input` or `\include`.

| Relative path | Bytes | SHA-256 |
|---|---:|---|
| `tex/alg-geom/sheaves.tex` | 31,229 | `9F5F2E3B73B1AED24C344273BD8E652DE855699AFD58F03A28E2579D06BEBFBB` |
| `tex/alg-geom/localization.tex` | 24,030 | `54DC95BAFE5F63584CD0BC38F687D3E6F56126688F9A84E8111199726924CE2D` |
| `tex/alg-geom/spec-zariski.tex` | 22,434 | `742162581A6DE852DF6D2530DE5F7066D9CD54A6B1679D795BF21C53FD69713A` |
| `tex/alg-geom/spec-sheaf.tex` | 22,075 | `D1F9C786A21C24726F9B061B689DAE5B7E95155E3C4FF161A6D21FE5B318A181` |
| `tex/alg-geom/spec-examples.tex` | 35,181 | `A84E7D392D801107DA2D759C48964DC23BCC443E4E428AC465E53E27F85A5A4B` |
| `tex/alg-geom/mor-scheme.tex` | 35,177 | `A9525F8020DACEB0873A63C85BE8D87B819E6A0A246B92C9B9AC111163457B76` |

## Shared build closure

Part XX is not an independent subdocument. `Napkin.tex` unconditionally includes every book part and the back matter, while Part XX relies on whole-book macros, counters, cross-references, bibliographies, solution files, and generated Asymptote figures. Consequently the immutable archive—not merely the six files—is the reproducible whole-tree build closure.

Primary shared controllers and direct Part XX dependencies are frozen below.

| Relative path | Role | SHA-256 |
|---|---|---|
| `Napkin.tex` | whole-book controller and Part XX selection | `3CCBB71A66047754FEC45B0C0609222AD85443E3822778C244751D90F90D8A3F` |
| `tex/preamble.tex` | packages, document configuration, bibliography resources | `6834D248988A948D891F1E3A53B5E8671CD82C595C89E163D6ED206A0E1489C9` |
| `tex/macros.tex` | shared semantic and mathematical macros | `6AD582E6BC320141BF9B16ADA02A935A76EC28A780101652071578FF48A7F24E` |
| `tex/Qcircuit.tex` | root-level shared input | `1F1AEBBA56BF5525739ADEB561FC3840DB8895E79B331D01933DFAA27E943EF1` |
| `references.bib` | citations used by Part XX and book | `FCF30A81D7ACA295B052786ACD7E297C5F9B2F0AA4762E31529941B0DC19145A` |
| `images.bib` | image attribution data | `C400013EC9BBDD272161C04BAE2DD543692833BD446980B37F5A46D58F47CFFC` |
| `.latexmkrc` | documented LaTeX/Asymptote orchestration | `04D700E7160D8A94E4ACFB30DA39BEBA648A4B72E27B7E9D22F94F9C4E9E0D65` |
| `flake.nix` | official Nix build expression | `CA43F8B48C155F95374F1704A281669F833576A792D7C583B10185693C77AFA8` |
| `flake.lock` | pinned Nix inputs | `DF3663344E3ED7C65B554BA351D46D5BEE784BDAFDD03FFF7190D3216F93A8F4` |
| `.github/workflows/napkin.yml` | demonstrated CI commands and part extraction | `06CEFF45900DFD239686CC7A10309F276130F627EA7300259FDCABC4985FBE11` |
| `print-toc.py` | qpdf per-part extraction commands | `E68F381827FDE9F60BF0454D5B9611662A76B5CF750EF0C58D20ECF5FFEE363C` |
| `README.md` | official build directions | `91B8660CA944BAA152E8E71E9223918C029735F0D24A40F4564612B84652594E` |
| `LICENSE.md` | upstream rights statement | `E77286D2A0FF092119ADA1C1B3E239707B86D81AED00917C5E22ADE5F19F02A4` |

The six files contain 23 inline Asymptote figures. Their generated `.asy` inputs depend on the preamble and full-document numbering. They also directly use two raster files:

| Relative path | Bytes | SHA-256 | Component-rights finding |
|---|---:|---|---|
| `media/calvin-hobbes-fly.png` | 20,541 | `79F70D71EE5AED3F929C07399CCEF9DE769963BC41293C64F111E6BC246C748F` | `images.bib` credits Bill Watterson and says only “I think this is fair use”; no reusable component licence is established. Replace or omit in a derivative. |
| `media/mumforddrawing.jpg` | 28,887 | `1CB853868026BFE898E544CFB2C491C3E9D004018AE1D48E2D5FE24E43FB5435` | `spec-examples.tex` identifies it as the famous picture from Mumford's *Red Book* and reproduces it for “culture-preservation”; no component licence is recorded. Replace or omit in a derivative. |

## Rights separation

`LICENSE.md` states that the Napkin text/PDF is CC BY-SA 4.0 and its source files are GNU GPL v3; it also states that there is no contributor licence agreement. A translated textual adaptation must carry CC BY-SA attribution, change notice, licence link, and ShareAlike. Distributed modified TeX/build source must separately satisfy GPLv3. Do not make one blanket rights claim across both layers or across third-party media. The two raster exceptions above are not cleared by the repository statement and are excluded from the planned derivative unless replaced with independently created or separately licensed material.

## Whole-tree build result: BLOCKED

Official documented routes:

1. `nix build` using `flake.nix` and `flake.lock`.
2. `latexmk`, with a recent TeX distribution and Asymptote. CI uses `latexmk -pdflatex -interaction=nonstopmode -file-line-error Napkin.tex`.

Nix is not installed on this machine, so route 1 was unavailable. The available route used Latexmk 4.88, MiKTeX-pdfTeX 4.27 / MiKTeX 26.5, Asymptote 3.06, and Biber 2.21. Package installation was disabled with `MIKTEX_ENABLE_INSTALLER=0` and `pdflatex --disable-installer`.

Exact attempted command:

```text
latexmk "-pdflatex=pdflatex --disable-installer %O %S" -interaction=nonstopmode -file-line-error Napkin.tex
```

The first pdflatex pass completed a provisional 988-page `Napkin.pdf` (9,621,088 bytes; SHA-256 `AE068581B436380C2DBA0DA36FCE3AF89D376A8D21C47FBD35596BAB47E66C86`) and emitted 213 `.asy` inputs, but no Asymptote PDFs. Latexmk then called `.latexmkrc`'s custom dependency:

```perl
system("cd '$dir' && asy -tex pdflatex '$base'")
```

On Windows, that string is dispatched through `cmd.exe`; its single-quoted directory is treated literally. The command reports `The system cannot find the path specified`, the Asymptote rule returns 256, and Latexmk exits 12. Thus the provisional PDF is not a successful baseline and must not be used as one. An installed POSIX shell was not available: the Windows `bash.exe` shim has no registered WSL distribution. `qpdf`, needed only after a successful build for official part extraction, is also absent.

No package was installed, no frozen source/controller was edited, and no failure was forced past with Latexmk's `-f` option. A successful baseline requires either the already-pinned Nix route on a Nix-capable host or an upstream-equivalent POSIX TeX environment. This Windows-host failure is the bounded blocker.

## QA evidence

- `qa/run-napkin-baseline-build.ps1`: exact route-selection and safety wrapper.
- `qa/napkin-baseline-build.log`: command, environment paths, timestamps, and exit code.
- `qa/napkin-pdflatex-first-pass.log`: copied native TeX log from the provisional first pass.
- `qa/napkin-baseline-replay-v2.stdout.log` and `.stderr.log`: concise native Latexmk/Asymptote failure reproduction, exit 12.
- `qa/capture-napkin-build-failure.ps1` and the non-v2 replay logs are a superseded capture attempt whose argument quoting failed before the build; they are not build evidence. The v2 pair is authoritative.
- `qa/NAPKIN_BASELINE_HASHES.sha256`: artifact, source-closure, controller, and QA-evidence hashes.

`Napkin.tex` embeds the wall-clock build date in `\napkinversion`; even after the build blocker is removed, byte-identical reproduction requires controlling or recording that date.
