# Lecture 11 review

Current deck names and page counts are in [LECT11_SOURCE_MAP.md](LECT11_SOURCE_MAP.md).
Earlier conversion and classroom-refresh records are in the [review archive](../../../docs/archive/genetics_lect11_review_early_20261117.md).
Dated entries below retain history; later entries supersede earlier deck letters and counts.

## November 17: distinct deck titles and filenames

Rename the canonical masters and generated outputs to match their teaching roles:
- 11B Interpreting Gene Trees: `lect11b-interpreting_gene_trees`.
- 11C Building Gene Trees: Three- and Four-Sequence Examples: `lect11c-building_gene_trees`.
- 11D UPGMA: Five Sequences and Weighted Averages: `lect11d-upgma_weighted_averages`.
- 11E UPGMA Practice: Class and Extension Problems: `lect11e-upgma_group_activity`.
- 11F Molecular Clocks and Evolutionary Time: `lect11f-molecular_clocks`.

Only the cover titles change within the decks; all teaching blocks and included fragments
remain unchanged. Update Markdown links to canonical sources and generated outputs;
original archived ODP/PDF and asset names remain intact. Move superseded generated
filenames into `_temp/lect11_names_before/` to avoid stale duplicates. Handout filenames
remain unchanged. Rebuild all five ODP/PDF pairs, verify cover titles and page counts
30/59/38/64/19, and visually inspect the covers. Native lint passes for 210 slides.
The prior 11C character-methods font advisory and 11F figure marker remain.
Evidence: `_temp/lect11_names_review/`. Live Impress playback untested.

## November 17: color-code the five joins in 11E

Use the documented five-stage rainbow selection: Red #D40000, Dark yellow #6C6C00,
Teal #00775F, Navy #0067CC, Pink #CC0066. Numbered colored Join headings repeat across
each merge's question, answer, and distance updates. Match selected matrix cells and
new cluster labels to each join. Newly created tree branches, their height labels,
and joined tip labels receive the join color; previous branches retain their colors.
Color final node labels in the branch-length summary. Keep ordinary prose neutral.
Add Follow the Join Colors at PDF 7; the extension restarts the same color sequence.
11E now has 65 pages; the extension begins PDF 36, answers PDF 39-63.

The existing recipe owns this behavior for the two six-gene examples. Regenerating
four/five examples with before/after recipe versions gives byte-identical Djot and
SVG output; those canonical artifacts were not regenerated or rebuilt. The two
six-gene histories, all numeric values, SVG path geometry, and text positions match
before/after. Before an answer reveal, the matrix does not highlight the selected
cell. All 30 native tables preserve exact widths/heights and row/column dimensions
against the pre-change export. No new capacity advisories. Native lint and pyflakes
pass. Visually review all changed teaching pages and both completed trees after the
ODP/PDF rebuild. Print handouts remain unchanged. Evidence and assertions:
`_temp/lect11e_stage_colors_review/`, `_temp/check_lect11e_stage_colors.py`.
Live Impress playback untested.

## 11F teaching expansion, November 17

Rebuilt the former 19-page evolutionary-time sequence as 49 bite-size teaching slides.
The central message is that sequence differences need a calibrated rate to become a time
estimate. Four sections follow gene choice, sequence change, calibration, and interpretation.
All nine substantive original figures remain, including a repaired Adh map; the former
replacement marker is resolved. Added 41 speaking notes, early definitions, paired questions
and answers, a two-lineage diagram, a numerical calibration and dating example, and a formula
reference. Corrected the inherited ortholog/paralog definitions and mutation/rate claims.
The beta-globin numbers are explicitly historical teaching assumptions.

See [LECT11H_TEACHING_GUIDE.md](LECT11H_TEACHING_GUIDE.md) for the teaching route, cognitive
walkthrough, scientific corrections, sources, and evidence limits. Strict native lint and
343 focused checks passed. All 49 pages were rendered and reviewed, arithmetic recomputed,
source-image bytes preserved, new diagram contrast measured, and no out-of-page words found.
No student study or attended playback was performed. This supersedes the earlier 11F
figure-placeholder limitation.

## 11A Episode 39 thumbnail refresh, November 17

Downloaded the updated 1280 x 720 YouTube thumbnail for `Iyz6WX2r8Rg` using a
cache-busting request. The revised image gives the hosts Western clothing and hats.
Replaced the local WebP and rebuilt the 11A ODP/PDF; the episode title and links remain.

## 11B primate question/answer pairs and orange tree, November 17

Former PDF slides 13-18 are now three paired questions with native on-click answer reveals,
on current slides 13-15. Kept the two-column layout because the standard multiple-choice
layout limits its top figure to 30 percent of content height. The existing diagram frame
is exactly unchanged on all three questions (12.228125 x 8.220862 cm). Each answer includes
a short explanation. The PDF shows the complete answers for studying. Total deck: 27 pages.

Replaced all 52 saturated-blue tree paint attributes with palette dark orange #B74300
(5.50:1 against white). SVG geometry, labels, time scale, and positions are unchanged.
The introductory tree uses the same orange asset. Strict native lint passes; exported
question pages were visually inspected, and all three reveal objects are present in ODP.
Live click-through in Impress was not tested.

## Second deck split, November 17

Split former 11C at "From Distances to a Tree": current 11C covers sequences and methods
(18 pages), and current 11D contains the complete three-rhino and four-sequence construction
examples (45 pages). Former 11D becomes 11E (38 pages). Split former 11E into current
11F class activity (37 pages) and 11G extension activity (35 pages); each has its own
objectives, procedure, five-color key, complete answers, summary, and end. Former 11F
becomes 11H (49 pages). The molecular-clock teaching guide is now LECT11H_TEACHING_GUIDE.md.

All moved teaching pages were compared against the pre-split exports. Matrices, tree
figures, source assets, and handouts retain their geometry or byte hashes. The H source
is identical to the prior F source except its cover letter; its new export reflects
pre-existing ASCII arrow/multiplication/approximation spellings already in the source.
Current links and source map are updated. Old generated filenames were backed up under
_temp/lect11_second_split_before and removed from the output folders. Original archived
lecture-root sources and printable handout filenames remain unchanged.

Strict native lint passes for all six decks (222 slides). 343 focused link/guidance
checks pass. Covers, summaries, and split boundaries were visually reviewed; all moved
teaching text and table/image-frame geometry were checked. The existing 17.5 pt advisory
on Character-Based Methods remains in C. No attended Impress playback was performed.

## Q&A repair, merge cues, varied distances, and table alignment

- 11B slides 13-15 now use `multiple-choice` with separate `@question` and `@answer`
  slots. The previous generic paragraph reveal hid its whole choices/answer text frame.
  The actual Q&A layout keeps choices visible and animates only the answer rectangle.
  Component images can use half the question area when both text sizes remain at least
  20 pt; otherwise the original smaller allocation remains. Answer shapes receive explicit
  measured line breaks, preventing overflow without changing ordinary text serialization.
- Removed the misplaced "Constructing a Gene Tree from Sequences" divider from 11C.
  C now has 17 pages; construction begins in 11D.
- Restored merge row/column bands in D/E. Purple identifies the merged rows/columns.
  Matching teal, blue, orange, or purple cells connect original gene pairs with their
  average calculation. Calculation pages display the original matrix beside the arithmetic;
  weighted examples still count every original gene equally.
- Four-gene input distances are now ab=16, ac=6, ad=18, bc=20, bd=10, cd=22. Joins remain
  ac, bd, then abcd. First averages are (16+20)/2=18 and (18+22)/2=20; the final average is
  (16+20+18+22)/4=19. Root height is 19/2; root branches are 13/2 and 9/2. Tree figures,
  branch summaries, and the explanation that some fitted distances differ were regenerated.
  The three-rhino, five-gene, class-handout, and extension-handout input data are unchanged.
- Distance matrix values and labels use explicit center alignment, including question marks
  in the rhino comparison tables and highlighted cells. Numeric branch-height cells are
  centered as well. The local four-step fragment now includes the canonical generated
  fragment, so future recipe runs retain the revised data, cues, and colored tree.

Verification: strict native lint passes for all eight current masters (305 authored slides,
including hidden A slides). The audit finds 62 centered distance matrices and 396 centered
numeric cells; 20 repeated table-layout groups retain their dimensions within each deck.
The full PDF set has 284 visible pages and no extracted words outside page bounds. Rendered
question/answer states and colored averaging pages were inspected. Native ODP animation targets
only each answer shape. No attended Impress click-through was performed.

Evidence is under `_temp/lect11_table_refinement/` and `_temp/lect11b_actual_qa/`.
The full-suite chromosome-review caption failure belongs to the separate chromosome work;
no chromosome files were changed for this task.

Final regression result: 485 focused checks passed. The full base suite returned
9,414 passed and one failure in `prototype/chromosome_review_part_01.djot` (a big-image
caption with more than two paragraphs); that unrelated chromosome source was left untouched.
