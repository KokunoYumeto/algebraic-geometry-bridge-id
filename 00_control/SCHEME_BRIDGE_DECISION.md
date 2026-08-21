# Compact schemes bridge — bounded source decision

Decision date: 2026-08-21  
Decision: conditional GO — Napkin Part XX as donor/core, not as the whole bridge

## Comparison boundary

The comparison was deliberately stopped after three viable primary-source
leads.  More searching would not add enough value to justify delaying reader
production.

| Candidate | Editable/buildable authority | Rights | Relevant closure | Disposition |
|---|---|---|---|---|
| Evan Chen, *An Infinitely Large Napkin*, Part XX | Official GitHub LaTeX; whole-tree Nix/`latexmk`/Asymptote routes | Text/PDF CC BY-SA 4.0; build source GPLv3; two media files unresolved | Sheaves, localization, `Spec`, Zariski topology, affine structure sheaf, stalks, residue fields, locally ringed spaces, scheme morphisms, affine anti-equivalence | Admit as the compact affine-schemes core, subject to exact archive/build freeze and media exclusion |
| MIT OCW 18.726, Algebraic Geometry (Spring 2009) | Official downloadable HTML/PDF course, but no public editable mathematical source/build closure | CC BY-NC-SA | 39 lectures and 12 problem sets, broad graduate sequence, no solutions | Reject for this role: editable-source/build gates fail and scope is too broad |
| Andreas Gathmann, *Algebraic Geometry* | Official current 138-page PDF; no editable source exposed | Site states all rights reserved | Excellent classical-to-schemes course with exercises | Reject: no lawful translation/adaptation basis and no editable build closure |

## Exact admitted Napkin authority

- Repository: <https://github.com/vEnhance/napkin>
- Commit: `e50be9a0b2b12d080c273619424d0ee13372cc91`
- Tree: `023467410bdf924c8fd38ac04009b4c887cbfb5e`
- Commit timestamp: `2026-08-20T18:59:08Z`
- Immutable archive:
  <https://github.com/vEnhance/napkin/archive/e50be9a0b2b12d080c273619424d0ee13372cc91.zip>
- Official Part XX PDF:
  <https://venhance.github.io/napkin/Parts/part-20-napkin-algebraic-geometry-ii.pdf>
- Part XX authored files: `sheaves.tex`, `localization.tex`,
  `spec-zariski.tex`, `spec-sheaf.tex`, `spec-examples.tex`, and
  `mor-scheme.tex`.

These six files are not a standalone build.  They depend on the whole-book
`Napkin.tex` preamble, shared macros, bibliography, media, and earlier
cross-references.  The hosted 74-page part is a comparison witness, not a
substitute for an exact-commit build replay.

## Why supplementation is mandatory

Part XX does not actually construct schemes by gluing affine charts.  Its
projective material following `\endinput` in `mor-scheme.tex` is inactive and
does not count.  The exercise surface is also incomplete: approximately 21
problems, 10 exercises, and 14 questions, but only 10 hints and 7 inline
solutions.  The separately maintained community solutions are not admitted
without their own source-and-license freeze.

The original supplement will therefore contain:

1. the transition from Brenner's classical affine varieties/curves to affine
   schemes;
2. affine gluing data and the cocycle condition;
3. `P^1` from two affine lines;
4. the doubled-origin line as a nonseparated warning;
5. one Brenner projective curve expressed in scheme charts; and
6. a compact original exercise set with complete original solutions.

Permanent Stacks tags `01HR`, `01HW`, `01JA`, `01JB`, `01JC`, and `01JE` are
downstream definition/proof checks only.  They do not become the first reader.

## Rights boundary

- Translated Napkin prose and mathematical exposition: CC BY-SA 4.0, with
  attribution, license link, translation/change notice, and ShareAlike.
- Distributed modified LaTeX/build source: GPLv3.
- New bridge supplement: independently worded, licensed CC BY-SA 4.0.
- `calvin-hobbes-fly.png` and `mumforddrawing.jpg`: omit or replace unless an
  independent component-rights audit proves their use.

Acquisition and exact-head build status are recorded separately in the
authority freeze and QA receipts; admission is not final until those byte-level
checks pass or a precise build blocker is documented.
