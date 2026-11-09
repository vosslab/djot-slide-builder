# Native table visual evaluation

Date: 2026-11-09\
Reviewer: Independent `image_evaluator` role\
Scope: Supplied LibreOffice-rendered samples; advisory visual assessment.

## Overall verdict

**The table styles look attractive, coherent with the course themes, and effective for visual teaching.** The strongest examples combine generous cell padding, clear headings, quiet rules, aligned numbers, and selective scientific color. They look like teaching materials belonging to these courses.

I support satisfaction with the **table design family**. I would not describe all sampled classroom slides as visually finished. Some dense tables need local sizing attention, and several slides retain material conversion gaps outside the table styling.

The missing pigeon reveals and Day 7/21 problems are real teaching limitations. Metadata identifies them as retained conversion blockers, so they are **not evidence that the new table styles caused regressions**.

## Basis and inventory

Read:

- `~/.codex/agents/image_evaluator.toml`
- Repository `AGENTS.md`
- `docs/REPO_STYLE.md` and `docs/MARKDOWN_STYLE.md`
- Slide visual review rubric and relevant color/pedagogy guidance

Directly inspected these **43 rendered classroom/demo pages individually**:

| Directory under `_temp/table_styles/` | Images inspected |
| --- | --- |
| `demo/` | `page-01.png` through `page-14.png` |
| `demo/` | `biotechnology-01.png`, `biotechnology-05.png`, `biotechnology-14.png` |
| `demo/` | `biostatistics-01.png`, `biostatistics-05.png`, `biostatistics-14.png` |
| `corpus_remaining/` | `biotechnology_page_002.png`, `biotechnology_page_028.png`, `biostatistics_page_001.png` |
| `corpus_remaining/` | `genetics_page_067.png`, `genetics_page_102.png`, `genetics_page_116.png`, `genetics_page_141.png` |
| `corpus_other_repairs/` | `review_002.png`, `review_003.png`, `review_024.png`, `review_025.png`, `review_028.png` |
| `corpus_other_repairs/` | `review_038.png` through `review_042.png` |
| `corpus_lect12/` | `lect12a-2026_announcements_table001.webp` |
| `corpus_lect12/` | `lect12b-gene_trees_table004.webp`, `lect12b-gene_trees_table024.webp` |
| `corpus_lect12/` | `lect12c-more_gene_trees_table002.webp`, `lect12c-more_gene_trees_table014.webp`, `lect12c-more_gene_trees_table028.webp` |

Also inspected `paired_sheet_01.webp` through `paired_sheet_05.webp` for overview and selecting comparisons. Their embedded status labels were not treated as visual evidence.

Rendered and inspected three original PDF pages separately at 1440-pixel width:

| Original | Comparison render under `_temp/table_styles/` |
| --- | --- |
| `genetics/LECT06/lect06d-x_linked_genes_1.pdf`, page 60 | `pigeon_original_60.png` |
| `genetics/LECT14/lect14c-hardy_weinberg_1.pdf`, page 52 | `blood_original_52.png` |
| `genetics/LECT14/lect14d-hardy_weinberg_conditions.pdf`, page 31 | `day7_original_31.png` |

Used metadata indexes to identify source slides and retained blocker context. This is a sample review, **not a review of the entire 424-table corpus**.

## Strongest successes

### Typography and rhythm

**Observed:** Ordinary tables use large, dark text, comfortable row height, and restrained horizontal rules. Working tables add a light grid without making every boundary compete with the values.

**Judgment:** The default and working styles are particularly successful. They feel deliberate and calm. The distinction between reading a comparison and working through a calculation is visible without introducing unrelated design languages.

### Course integration

**Observed:** Genetics blue, Biotechnology red, and Biostatistics green carry through heading fills and stronger separator rules. The same testcross recombinant rows retain their pale purple fill across all three themes.

**Judgment:** This is a convincing family. Course identity frames the table while scientific meaning remains independent. The red and green variants are brighter than Genetics, but neither looks disconnected from its slide theme.

### Scientific structure

**Observed:** Punnett examples distinguish both gamete axes; testcross alleles occupy stable columns; numbers generally align on the right; totals have stronger visual treatment. Scripts and the equation in demo page 02 are visibly differentiated.

**Judgment:** These are useful teaching choices, not merely decoration. Students can follow relationships and calculations without first decoding inconsistent alignment.

### Stable reveals

**Observed:** Demo pages 12 and 13 preserve table position and column widths. Answer cells gain a pale yellow fill. Blood-group pages 002/003 and pigeon pages 038/039 also preserve their table workspaces.

**Judgment:** These sequences support instructor-controlled explanation well. Attention can remain on the changed content.

### Meaningful color in real examples

**Observed:** The interference table preserves distinct allele-column fills. The tetrad workspace carries PD/NPD/TT colors into the instructions. LECT12 merge tables retain local outlines and scientific fills.

**Judgment:** These examples preserve course-specific instructional character. The table system accommodates meaningful exceptions successfully.

## Ranked findings

### 1. Pigeon sequence loses essential reveals

**Impact:** Material whole-slide concern; retained conversion gap.

**Evidence:** `corpus_other_repairs/review_040.png` through `review_042.png`; source `genetics/LECT06/djot/lect06d-x_linked_genes_1.djot`, local slides 58-60.

**Observed:** These pages show essentially the same completed genotype grid. In the separately inspected original PDF page 60, offspring cells have sex symbols, the lethal female cell has a large red X, and the conclusion reads "2 males for every 1 female." Those teaching cues are absent from `review_042.png`.

**Judgment:** The native grid itself is attractive and readable, but the final slide does not visually explain the survival-adjusted ratio. This is materially worse as a completed teaching sequence.

**Scope qualification:** Manifest entries retain `marker_after=true` and explicitly identify unreconstructed sex labels, lethal-cell X, and ratio answer. The manager reports that diagnostic renders suppress marker overlays. This finding concerns unfinished conversion content, not a newly introduced table-style regression.

**Recommendation:** Keep these slides marked incomplete until the source-grounded reveals are restored and the sequence is rendered again. Preserve the current grid geometry.

### 2. Day 7/21 data source is too small

**Impact:** Material whole-slide concern; retained conversion gap.

**Evidence:** `corpus_other_repairs/review_024.png` and `review_025.png`; source `genetics/LECT14/djot/lect14d-hardy_weinberg_conditions.djot`, local slides 32/33.

**Observed:** The native Day 7/21 tables are readable. The seedling source table above them is a small thumbnail, while the calculations occupy a much larger right-hand column. Non-table expressions visibly include flattened forms such as `p12` and `q12`. The original page 31 gives the seedling data substantially greater prominence and uses differentiated scripts.

**Judgment:** Students can read the derived results but would struggle to inspect the underlying counts during Zoom teaching. Flattened notation adds avoidable interpretation work.

**Scope qualification:** Metadata retains a blocker for inherited image/overlay relationships and flattened non-table calculation scripts.

**Recommendation:** Repair the source-data presentation and notation locally. The native Day table styling does not need redesign.

### 3. Assignment and date nearly run together

**Impact:** Local table-spacing concern.

**Evidence:** `corpus_remaining/biostatistics_page_001.png`; `biostats/LECT08/djot/lect08a-2026_biostats_announcements.djot`, source slide line 187.

**Observed:** In the Week 10 row, "regression feedback" extends almost to the adjacent "Nov 04." Other rows have clearer separation.

**Judgment:** The row remains decipherable, but this weakens the table's column grouping and looks less polished than the surrounding rows.

**Recommendation:** Give this assignment a controlled wrap or adjust its local column allocation so the date retains an obvious gutter. No global style change is warranted.

### 4. Dense real tables need local scale review

**Impact:** Repeated readability concern, especially over Zoom.

**Evidence:**

- `corpus_remaining/genetics_page_067.png`: `genetics/LECT05/djot/lect05h-epistasis.djot`, line 535.
- `corpus_remaining/biotechnology_page_028.png`: `biotech/LECT06/djot/set4_chapter_15.djot`, line 548.
- To a lesser extent, `corpus_remaining/genetics_page_116.png`: `genetics/LECT09/djot/lect09b1-interference_worked_example.djot`, line 37.

**Observed:** Squash genotypes and herbicide comparison text are substantially smaller than the surrounding explanatory prose. The interference table is dense but remains better supported by its simple columns and meaningful fills.

**Judgment:** Clean rules and padding cannot fully compensate for small instructional content. The squash Punnett outcomes and herbicide methods are central to their tasks and deserve greater visual weight.

**Recommendation:** Review local space allocation and type size, preserving all source content. Consider authorized emphasis or close-up treatment where appropriate; do not automatically split slides or remove rows.

### 5. Some demonstrations are intentionally less elegant

**Impact:** Minor; no product fix required.

**Evidence:** Demo pages 03, 10, 11, and 14.

**Observed:** Page 03 has tightly packed long column headings. Page 10 uses conspicuous empty space and heavy side rules to demonstrate vertical alignment. Page 11 is prose-heavy. Page 14 demonstrates mixed alignment beneath a merged heading.

**Judgment:** These are valid capability demonstrations, though some are less natural classroom compositions than the ordinary, working, and testcross examples.

**Recommendation:** Keep their demonstrative purpose explicit. Do not interpret their intentional overrides as defects in the defaults.

## Rubric scores

Scores describe the **whole rendered page**. R = Readability; O = Visual organization; H = Emphasis and hierarchy; S = Use of space; E = Overall effectiveness.

Bands: 18-20 generally strong; 15-17 contextual review; 0-14 advisory visual attention. One-point differences are not meaningful rankings. Any dimension of 2 merits follow-up even when the total is higher.

### Canonical demonstration

All filenames here are under `demo/`.

| Page | R | O | H | S | E | Total | Concern and reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: clear ordinary table. |
| 02 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: scripts and equation remain legible. |
| 03 | 3 | 4 | 4 | 3 | 4 | 18 | Minor concern: long headings feel tightly packed. |
| 04 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: strong calculation workspace. |
| 05 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: classification and count structure are immediate. |
| 06 | 4 | 4 | 4 | 3 | 4 | 19 | No concern: clear axes and selected outcome; ample lower space. |
| 07 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: active triangle is immediately distinguishable. |
| 08 | 4 | 4 | 4 | 3 | 4 | 19 | No concern: cropped matrix remains recognizable. |
| 09 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: intentional border demonstration is legible. |
| 10 | 4 | 4 | 3 | 3 | 4 | 18 | Minor concern: demonstrative geometry dominates the composition. |
| 11 | 3 | 4 | 4 | 3 | 4 | 18 | Minor concern: long prose requires sustained reading. |
| 12 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: clear question workspace. |
| 13 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: stable geometry and selective answer fill. |
| 14 | 4 | 4 | 3 | 3 | 4 | 18 | Minor concern: mixed alignment is a demonstration rather than a natural reading pattern. |

### Theme variants

| Image | R | O | H | S | E | Total | Concern and reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| biotechnology-01 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: readable course-themed structure. |
| biotechnology-05 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: scientific fill remains distinct from theme. |
| biotechnology-14 | 4 | 4 | 3 | 3 | 4 | 18 | Minor concern: same intentional mixed alignment as Genetics. |
| biostatistics-01 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: readable course-themed structure. |
| biostatistics-05 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: scientific fill remains distinct from theme. |
| biostatistics-14 | 4 | 4 | 3 | 3 | 4 | 18 | Minor concern: same intentional mixed alignment as Genetics. |

### Existing course slides

Filenames in the first seven rows are under `corpus_remaining/`; numbered review images are under `corpus_other_repairs/`.

| Image | R | O | H | S | E | Total | Concern and reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| biotechnology_page_002 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: balanced, readable rubric. |
| biotechnology_page_028 | 2 | 4 | 3 | 3 | 3 | 15 | Minor concern: central comparison text is small beside the bullets. |
| biostatistics_page_001 | 2 | 3 | 4 | 3 | 3 | 15 | Minor concern: Week 10 text nearly meets the date. |
| genetics_page_067 | 2 | 4 | 3 | 3 | 3 | 15 | Minor concern: Punnett outcomes are small for the teaching task. |
| genetics_page_102 | 4 | 4 | 4 | 3 | 4 | 19 | No concern: clear chi-square workspace and total. |
| genetics_page_116 | 3 | 4 | 4 | 3 | 3 | 17 | Minor concern: dense table and small supporting text warrant Zoom review. |
| genetics_page_141 | 3 | 4 | 4 | 4 | 4 | 19 | No concern: useful classifications connect directly to instructions. |
| review_002 | 3 | 4 | 4 | 3 | 4 | 18 | No concern: table is clear beneath a substantial problem statement. |
| review_003 | 3 | 4 | 4 | 3 | 4 | 18 | No concern: stable answer table with aligned frequencies. |
| review_024 | 2 | 3 | 2 | 2 | 3 | 12 | Material concern: tiny source data and flattened notation. |
| review_025 | 2 | 3 | 2 | 2 | 3 | 12 | Material concern: same source-data and notation limitations. |
| review_028 | 3 | 4 | 3 | 3 | 3 | 16 | Minor concern: crowded formulas and problem image compete for reading. |
| review_038 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: clear prompt and blank Punnett workspace. |
| review_039 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: stable, readable genotype reveal. |
| review_040 | 3 | 3 | 3 | 3 | 3 | 15 | Material sequence concern: later sex-label teaching step is absent. |
| review_041 | 3 | 3 | 2 | 3 | 2 | 13 | Material concern: lethality distinction is absent. |
| review_042 | 3 | 3 | 2 | 3 | 2 | 13 | Material concern: missing lethal-cell cue and final ratio conclusion. |

### LECT12 examples

All images are under `corpus_lect12/`.

| Image | R | O | H | S | E | Total | Concern and reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| lect12a-2026_announcements_table001 | 3 | 4 | 3 | 3 | 4 | 17 | Minor concern: wrapped URL is awkward; table itself is strong. |
| lect12b-gene_trees_table004 | 3 | 4 | 4 | 4 | 4 | 19 | No concern: symmetric entries and excluded diagonal are clear. |
| lect12b-gene_trees_table024 | 4 | 4 | 4 | 3 | 4 | 19 | No concern: large, immediately readable symmetry example. |
| lect12c-more_gene_trees_table002 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: active triangle and diagonal are unmistakable. |
| lect12c-more_gene_trees_table014 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: merge grouping and explanatory calculations connect clearly. |
| lect12c-more_gene_trees_table028 | 4 | 4 | 4 | 3 | 4 | 19 | No concern: merged column is visibly grouped and values remain clear. |

## Migration comparisons

These categorical calls use separately inspected original pages and final renders, not contact-sheet impressions alone.

| Original and final | Classification | Visible teaching reason |
| --- | --- | --- |
| Blood-group original page 52 -> `review_002` | Roughly equivalent | The themed header and lighter rules integrate better with the course; the original offers somewhat stronger row-group structure. Both preserve a readable genotype/frequency relationship. |
| Day 7 original page 31 -> `review_024` | Materially worse | The source seedling data becomes a thumbnail, and differentiated calculation scripts become flattened prose. The native result table remains usable. |
| Pigeon original page 60 -> `review_042` | Materially worse | Sex labels, the lethal-cell X, and the explicit surviving ratio disappear. The improved-looking grid cannot replace those instructional relationships. |

The latter two classifications describe retained conversion gaps. They do not establish a regression caused by this table-style change.

## Recommended disposition

- **Accept the table design family:** its defaults and specialized scientific treatments are visually successful.
- **Make the small local spacing correction** to the Biostatistics Week 10 row.
- **Review dense classroom instances locally**, especially the squash Punnett and herbicide comparison, before treating demo readability as proof of Zoom readability.
- **Retain explicit incomplete status** for the Day 7/21 and later pigeon slides until their non-table/source-reveal blockers are resolved.

No broader stylistic redesign is justified by this sample.

## Limitations

This was direct rendered-image review, not a live Zoom viewing test, numerical contrast audit, scientific-answer audit, native editability inspection, or complete corpus review. Contrast judgments are visual; no contrast ratios were measured.

No source, code, tests, or configuration changed. Three temporary original-page renders were created for comparison. Remaining risk: attractive tables can coexist with materially unfinished slide content.

## Provenance

Source: final report from the independent `image_evaluator` agent, event `amsg_01a1c25e-db86-78b0-aab7-89854ee6507a`, recorded 2026-11-09 22:12:38 UTC. Typographic quotation marks were normalized to ASCII. Two Markdown hard breaks use backslash markers to avoid trailing whitespace.
