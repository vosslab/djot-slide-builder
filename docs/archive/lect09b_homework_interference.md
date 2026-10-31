# Plan: Homework interference in 09B

## Goal and context

Teach crossover interference through one fixed problem from
`three-point_test_cross-find_interence.py`, keeping the homework's recognizable table and
breaking the reasoning into small pieces in the instructor's voice.

The current 23-slide 09B deck contains three older numerical examples, repeated calculations,
and nine replacement markers. Known source errors include `11.648.5`, calling 48.5%
interference "no interference," and chromatin claims already flagged for review.
The generator supplies gene order and all three pairwise distances; students need to calculate
interference rather than solve an entire three-point map again.

Use item 1 from the existing numeric homework bank in the website's `site_docs/genetics/topic08/`:
F/P/W allele columns, F-W-P gene order, 1,800 offspring, adjacent intervals 25 and 15 cM.
The double-crossover rows are `f+w` (23) and `+p+` (31), so observed DCO = 54,
expected DCO = 0.25 x 0.15 x 1,800 = 67.5, coincidence = 0.8, and interference = 20%.
This is the proposed fixed example; preserve the actual homework row order and phenotype names.

## Approach

1. Freeze that homework item with its eight counts, phenotype information, given distances,
   question, answer, and original HTML. Record the bank filename/item/hash and generator
   revision. Build slides from saved inputs; ordinary builds need no problem-generation step.
2. Introduce interference with a short conceptual contrast: what independence predicts versus
   what the data show. Retain the existing outer-gene/hidden-double-crossover motivation.
   Explain that crossover suppression alone does not establish crossover interference.
3. Present the homework problem before showing a solution. Reconstruct its simple table in
   native Djot: phenotype column, three separate colored allele cells, counts, and total.
   Keep all genes visible and table geometry stable. Make the distinction between alphabetical
   F/P/W table columns and physical F-W-P gene order explicit. Show the supplied map separately.
4. Use the generator's five-step procedure, with a lecture-local colored roadmap and small
   question/answer stages:
   - Identify the parents, then compare them with the reciprocal DCO types. Explain the middle
     gene's change; do not rely only on choosing the two smallest counts. Add 23 + 31.
   - Convert 25% and 15% to 0.25 and 0.15. Explain why independence lets us multiply them.
   - Multiply by 1,800. Explain why an expected count of 67.5 is meaningful.
   - Divide 54 by 67.5. Interpret 0.8 as 80% of the predicted doubles being observed.
   - Subtract from one. Interpret 20% as the reduction relative to the independent expectation,
     rather than 20% of all offspring. Close with 1/5 = 0.20 = 20% and numeric entry `20`.
   Keep equations and explanations visible in the student PDF. Repeat the compact table or
   a readable count summary when needed to connect each calculation to its source.
5. Make this the main worked example. Keep the Lz/Su/Gl, zero-interference A-C-B, and F-G-H
   examples as verified reference/practice material, consolidating repeated calculation slides
   while preserving distinct results and question/answer stages. Retain useful mapping-function
   and chromatin context; check its flagged definitions/inferences against local textbooks.
   Correct arithmetic and interpretation errors. Account for every current slide in the source map.
6. Update objectives/takeaways and build only 09B. Review the exported ODP/PDF, including
   homework-table readability, staged answers, and the bridge between each equation and its meaning.

## File scope

- `genetics/LECT09/djot/lect09b-crossover_interference.djot`: concept sequence and main deck.
- `genetics/LECT09/djot/lect09b1-interference_worked_example.djot`: locally included example.
- `genetics/LECT09/djot/interference_steps.djot`: five-step roadmap, locally included wherever
  repeated in 09B. Keep both supporting Djot files out of evergreen.
- `genetics/LECT09/djot/assets/lect09b-crossover_interference/`: frozen problem data/HTML and
  any necessary figure repairs. Existing lecture folders already provide ownership; no `deps/`
  folder, new compiler feature, or automatic problem-to-slide pipeline is needed.
- `genetics/LECT09/djot/LECT09_SOURCE_MAP.md`, `LECT09_REVIEW.md`, `genetics/README.md`, and
  `docs/CHANGELOG.md`: coverage, rationale, inventory, and verification evidence.
- `output/odp/lect09b-crossover_interference.odp` and matching `output/pdf/` export: generated
  from the updated source. Other decks, original presentations, and BPW repositories stay unchanged.

## Completion checks

- Independently verify all eight counts, parents/DCO identities, both interval frequencies,
  exact expected count, coincidence, and interference against the saved bank answer.
- Distinguish the given 34% outer-pair recombination from the 40 cM adjacent-interval sum.
  Do not multiply the outer-pair value into the independent-DCO calculation. Adapt the numeric
  bank's misleading distance/cM answer tips to interference percentage in the slides.
- Run strict native lint and the existing focused include/09B cover checks. Use one-time
  arithmetic/coverage checks; this content change needs no new permanent test framework.
- Inspect every exported page; keep titles/prose native, tables legible, and colors consistent.
  Build with the repository CLI and run LibreOffice outside the sandbox. Use `_temp/` for review.
- Give all 23 prior slides an explicit disposition. Resolve markers within the revised teaching
  sequence, documenting any remaining source-figure limitations without claiming playback testing.

Completed October 31, 2026: 44 visible slides with matching ODP/PDF exports. All four datasets
were independently checked; strict lint and 13 focused tests pass. The source map accounts for
all 23 previous slides. Classroom projection/pacing and Impress click playback remain untested.
