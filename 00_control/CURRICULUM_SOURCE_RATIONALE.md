# O016/D100 corpus rationale — bounded checkpoint

Date: 2026-08-22  
Scope: evidence for curriculum selection; not a curriculum-admission decision

## Disposition

**GO for the present corpus design.** Brenner plus the bounded schemes bridge
remains the strongest lawful, buildable, self-study-oriented design found for
O016/D100. This conclusion is independent of the Indonesian work already
completed: sunk production is not selection evidence, and the edition remains
worth completing even if the curriculum root later chooses another spine.

## Exact boundary

1. Translate all 30 lectures and all 30 worksheets of Holger Brenner's
   *Algebraische Kurven (Osnabrück 2025–2026)* in source order, including every
   frozen public solution and component-rights closure. The authority is the
   semantic Wikiversity course and transcluded-page closure; HTML, generated
   LaTeX, and official PDFs are independent reader/build witnesses.
2. Use only Part XX, “Algebraic Geometry II: Affine Schemes,” of Evan Chen's
   *An Infinitely Large Napkin* at commit
   `e50be9a0b2b12d080c273619424d0ee13372cc91`, tree
   `023467410bdf924c8fd38ac04009b4c887cbfb5e`, and its exact six authored files:
   `sheaves.tex`, `localization.tex`, `spec-zariski.tex`, `spec-sheaf.tex`,
   `spec-examples.tex`, and `mor-scheme.tex`.
3. Add an independently worded connector, with complete original exercises and
   solutions, covering affine gluing and cocycles, `P^1` from two affine lines,
   the doubled-origin line, and one Brenner projective curve in charts. Check
   it downstream against permanent Stacks tags `01HR`, `01HW`, `01JA`, `01JB`,
   `01JC`, and `01JE`.

## Why this combination is strongest

Brenner supplies a coherent classical course rather than isolated notes: a
fixed 30-lecture/30-worksheet sequence, substantial exercise density, public
solutions where the course exposes them, and an unusually rich editable
closure (semantic wiki source, rendered HTML, generated LaTeX, and PDF
witnesses). Its CC BY-SA 4.0 authority permits a clearly attributed Indonesian
derivative and continued correction. Napkin Part XX is compact, readable, and
legally adaptable; its official LaTeX gives a modern affine-schemes transition
without replacing the classical course. The custom connector fills the exact
gap between them instead of forcing an encyclopedic reference to act as an
introductory textbook.

## Serious alternatives and why they lose here

- **Stacks Project:** the correct permanent technical reference, with source
  and stable tags, but far too large and reference-shaped to be the first
  self-study reader for this bridge. It is used for downstream verification,
  not as the narrative spine.
- **MIT OCW 18.726 (Spring 2009):** a broad 39-lecture graduate course with 12
  problem sets under CC BY-NC-SA, but the official surface does not provide a
  complete editable mathematical source/build closure and supplies no
  solutions. It is weaker for translation maintenance and independent study.
- **Andreas Gathmann, *Algebraic Geometry*:** pedagogically excellent and
  compact, but the official site exposes a PDF rather than an editable build
  closure and reserves rights; it is not a lawful translation basis.

## Remaining gaps, overlap, and self-study limits

Brenner does not expose public solutions for every worksheet problem; those
must remain unsolved rather than be silently invented. Napkin Part XX likewise
has an incomplete exercise-support surface (about 21 problems, 10 exercises,
and 14 questions, but only 10 hints and seven inline solutions), and its
inactive post-`endinput` projective material does not count. The original
connector therefore needs complete solutions and explicit prerequisite links.
Some repetition of affine varieties, ideals, `Spec`, and Zariski language is
intentional transition scaffolding; duplicative exposition beyond that should
be removed. Advanced scheme theory, cohomology, and the full Stacks dependency
graph remain downstream subjects rather than hidden requirements of this
bridge.

The primary evidence is frozen in `authority/AUTHORITY_FREEZE.md`,
`authority/NAPKIN_PART20_AUTHORITY_FREEZE.md`, and
`00_control/SCHEME_BRIDGE_DECISION.md`.
