# Lecture 09E/F/G visual revision

The instructor requested larger classification answers, colored definition terms and formulas,
normal SVG lettering, homework-style tetrads in the crossover figures, and consistent treatment
of material already covered in class. Review 09F and 09G for the same issues.

## Changes and page ownership

| Deck | Pages | Changes |
| --- | ---: | --- |
| 09E | 30 | Static classification question/answer pair; term colors; repaired SVG text; homework-shaped outcomes; colored derivation; unlinked TT taught on the later slide. |
| 09F | 24 | Larger classification labels in both examples and working tables; class colors through formulas, substitutions, and intermediate sums. |
| 09G | 42 | Larger cumulative homework-table answers; prominent matching answers; class colors through substitutions and intermediate sums. |

Former E6 becomes E6-7: a question followed by an answer with approximately 50.5 pt class labels,
up from 17.3 pt. These are separate static slides. Other former E7-29 pages shift forward by one;
their topic order is retained. The two-gene examples already have separate question/answer pages.
Their answer galleries now use the same large labels. Three-gene answers retain the full homework
table and earlier pair classifications, with unused-gene covers in the later 09G revision below.

E3 uses gold PD, green NPD, and magenta TT terms. E4 uses course blue for NCO, SCO, and DCO;
a DCO can produce multiple classes, so it does not receive a single class's color.

Former E8, now E9, contained per-character x coordinates tied to an older font and an inherited
20% horizontal bitmap stretch. Restore natural proportions and reflow all labels with normal
text shaping in Atkinson Hyperlegible Next. Join the split Metaphase I/II labels.
Apply the same repair to the crossover-summary SVG's live labels. Original artwork remains.

Former E10-13, now E11-14, retain the chromosome mechanisms and starting PD question, with the
homework's colored ascus replacing the old yellow outcome. Explain that chromosome A/B means
the homework's +, while lowercase alleles retain their meaning. Preserve the original four-spore
multisets and chromosome participation; spore position is unordered and colors are schematic.
Original source images remain recoverable. E28 retains both unlinked TT mechanisms and now uses
the matching homework asci. It stays later in the deck, with an earlier forward reference.

E28 is an ordinary teaching slide. The already-taught mapping recaps at E26/F22 and the complete
classification recap at G37 also use ordinary layouts. Their misleading "not covered in class"
footers are removed. Optional estimates, prior-year practice, and video references keep their
reference treatment. No shared renderer behavior changes.

## Color and data contracts

- PD: `#935D00`, pale fill `#FFE3A3`.
- TT: `#A719DB`, pale fill `#E8CCE6`.
- NPD: `#007A00`, pale fill `#BFE6C0`.
- Use the same class color for its formula symbol, substituted count, and separate contribution.
  Combined totals, coefficients, operators, N, and final results keep their existing colors.
- Keep gene/pair colors distinct in meaning from class colors. Preserve all spore labels,
  counts, rows, phenotype colors, parent crosses, procedure steps, and gene-order answers.
- Keep every original equation's numbers and operations. Classes are upright named counts in
  MathJax, with explicit colors; equations remain authored in Djot.

The linked two-gene example remains 20 cM with 18% observed RF. The unlinked example remains
49.8% RF. The three-gene answers remain 10/15/24 cM and B-A-C/C-A-B; adjacent intervals sum to
25 cM. The six-step procedure is unchanged.

Figure inputs, hashes, transformations, genotype multisets, font sizes, and construction
references are in [figure_sources.json](assets/lect09e-tetrad_visuals/figure_sources.json).
The existing `slide_lib/render_tetrad_tables.py` reproduces the
larger Type-column labels. Ordinary builds read saved assets and need no generator or browser.

## Verification and limits

- [x] Check every equation against its earlier form after removing color/upright styling.
- [x] Independently verify the fixed class counts, distances, and genotype multisets.
- [x] Preserve the embedded chromosome artwork and the three-gene homework capture bytes.
- [x] Check SVG validity, unique IDs, normal lettering, and image proportions through export.
- [x] Verify larger class labels fit their cells; preserve every cumulative classification state.
- [x] Confirm source/ODP/PDF counts agree at 30/24/42 with no replacement markers.
- [x] Pass strict native lint, typography/capacity audits, existing covers, and relevant table,
  definition, SVG, and equation tests. Introduce no new permanent tests.
- [x] Review all 96 exported pages and inspect affected figures, answers, and equations at full size.
- [x] Preserve all other lecture sources and original problem data; refresh current documentation.

Evidence is in `_temp/tetrad_visuals/`: source/PDF baselines, authoring scripts, equation/data
checks, build/test/audit logs, page inventory, and quality-90 WebP reviews. The actual image
scale is preserved; minor PDF conversion rounding is checked against the export precision.
Physical classroom projection/pacing and Impress click playback remain untested.

## 09G pair-focus and handout follow-up

Keep the 42-slide inventory and every fixed genotype, count, classification, equation, and map
result. Add figure-local static covers, not animation: C on G9-10, B on G18-19, A on G27-28.
Each view has four header covers and 24 allele covers, measured from the saved homework HTML
using the original font mapping. Covers stay inside their own allele cells; the underlying
capture bytes, spore borders, table geometry, counts, and earlier answers remain intact.
G37 is the uncovered complete reference.

Set 6 contains only a++ and +bc. Its 702 tetrads contribute PD to every pair. Keep this row
outlined in gold in all figure states, highlight it in G11/20/29's native summaries, and color
the same 702 contribution in G12/21/30's sums. Explain the invariant in G6 and G41, alongside
the existing reminder to classify by genotypes rather than counts.

G38 retains all four activity instructions beside a full-page preview of page 2 from the
instructor-edited `tetrad_handout.odt` in the 2026 course folder. This page contains the three-gene
exercises. Export through the repository's LibreOffice runner with the Writer PDF filter;
capture the entire Letter page at 2x resolution as quality-90 WebP. Preserve the handout itself.
Source and export hashes, page size, covers, and drawing references are recorded in
[three_gene_homework_sources.json](assets/lect09c-tetrad_worked_examples_bpw/three_gene_homework_sources.json).

The shared roadmap now says "With three genes, focus on one pair at a time" rather than
requiring every locus to remain visible. G7/16/25 and F5/16 use the same
updated source. No shared renderer or generator changes are needed.

- [x] Independently classify the original tetrads and verify that only Set 6 is PD for all pairs.
- [x] Preserve image bytes, every cumulative class state, equation, native table value, and other decks.
- [x] Validate all covers and SVG IDs, and check native image proportions through export.
- [x] Reconcile source/ODP/PDF counts: G42 and F24; no replacement markers.
- [x] Pass strict native lint, zero typography/capacity findings, and the existing G cover test.
- [x] Inspect all 42 G pages, affected figures at full size, and the revised F roadmaps.

Evidence: `_temp/tetrad_g_focus/`, including the before sources/PDFs, measured cell bounds,
handout export, authoring/verification scripts, build/audit logs, and quality-90 WebP reviews.
The full-page handout is a visual preview; students use the actual handout for reading and work.
Classroom projection and pacing remain untested.
