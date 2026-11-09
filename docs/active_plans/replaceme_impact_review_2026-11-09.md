# Replacement-slide impact review

Reviewed November 9, 2026. This is a prioritization review, not an implementation plan.
All 460 current `@replaceme` slides remain marked.

## Recommended single improvement

Finish the existing native-table import path: emit each source table once, with the cell
formatting and spans supported by the native table model. This is the largest clearly bounded
importer repair identified here: 96 affected slides, including 57 in LECT12 and 25 in LECT14.
The target is the importer-to-native-table handoff, using the existing layouts and exporter.

Every one of those 96 source slides has an ODF frame containing both a real table and its
image preview. The importer currently admits both. Many current renders consequently show the
same table twice, shrinking the useful content. Other examples need merged cells, source fills,
or table emphasis restored. The existing backend already supports editable cell fills and
horizontal spans; the importer does not carry those facts through.

The source establishes a 96-slide affected set, not 96 guaranteed removals. Ten of these slides
also need native sequence alignment, eight also need a branch/map drawing, and four have source
animations. Those sets are disjoint here. The remaining 74 have no separate major blocker noted
in this review; their markers still require a rebuilt-slide comparison after any repair.

## Useful table features

A follow-up census of the 96 marked native-table source slides distinguishes existing features
from useful additions. These counts overlap within the same 96 slides; they are not extra
replacement-slide opportunities.

| Capability | Current support | Evidence and value |
| --- | --- | --- |
| Selective cell borders | Missing from authored tables; exporter uses one uniform border | 61 source slides have explicit mixed or suppressed cell borders. This is the strongest new feature for distance matrices and partial working tables. |
| Cell fills | Supported in authored Djot; absent from imported table facts | 40 source slides have explicitly colored cells. Carry the existing feature through import. |
| Horizontal merges | Supported as `colspan`; import still flags source spans | Nine source slides have merged cells, all spanning four columns. Preserve these through import. |
| Column proportions and shared sizing | Supported as `column-widths` and `table-group` | Reuse for repeated question/answer tables. Shared groups stabilize columns; row heights still follow each slide's content. |
| Vertical merges | No authored `rowspan` | None occurs in these 96 source slides, so it has lower immediate value. |
| Artwork in cells | No authored native image-in-cell support | Potentially useful for tetrad/chromosome tables; existing tetrad work uses whole-table SVGs. This census does not establish a replacement-count benefit. |

The smallest valuable new capability is selective borders, alongside fixing the existing import
handoff. Border control can retain an unused triangle, a partial grid, or an instructional separator
without drawing a full grid everywhere. No new table feature is implemented by this review.
The census resolves explicit cell-style inheritance in the original ODP XML; it is not a new
rendered acceptance test. Current table authoring is documented in
[../slide-specs/DJOT_SLIDE_SYNTAX.md](../slide-specs/DJOT_SLIDE_SYNTAX.md).

## Existing figure composition

The artwork-plus-labels workflow already exists and has successful LECT06/LECT08 repairs.
The instructor's clarified boundary is one artwork image per composed SVG, with associated
labels allowed outside the image rectangle. Titles, captions, and explanatory prose stay native.
The SVG viewport can include the artwork, labels, and leaders together.

This review identifies 69 artwork-composition candidates. Two also have source animations.
Some slides contain a separate question or matrix picture: compose only the relevant artwork,
or make separate one-image SVGs, while leaving the other component outside that SVG.
Reusing this workflow is valuable; a second SVG packaging system is unnecessary.

A separate 52-slide group loses native vector drawings, such as the LECT13D chromosomes.
There is no bitmap to label in the clearest examples. Another 44 slides involve relationships
among several distinct pictures. These are different repair problems; adding all three groups
together would overstate what a one-image labeling pass can clear.

The 130 native-fit/review cases are also not a promise of 130 easy removals. They include
crowded native calculations, small figures, notation, comparison prose, and conservative or
possibly stale warnings. For example, LECT12D source 12/16/20/28 has no active highlight shape;
LECT08C source 31/35/39 already has composed figure repairs. Review the actual remaining issue
before commissioning another tool for those slides.

## Evidence and coverage

- Rendered all 460 marked slides in temporary diagnostic decks and inspected 39 paired sheets.
  Compared 455 with their mapped original visible PDF pages; the five Biotechnology cases
  are manual content/placeholder decisions without a mapped source page. Two marked Genetics
  slides are hidden in their canonical decks and were made visible only in diagnostics.
- Cross-checked the inventory against physical source markers and expanded canonical decks.
  One unrelated Biotechnology LECT10 root fails parsing on an existing duplicate slot; scanning
  its physical sources finds no additional replacement markers.
- Refreshed the working-tree view after the Synology warning. The reviewed Djot, Python, and
  Markdown snapshot remained unchanged. This review does not revert concurrent edits.
- No slide content, markers, importer behavior, or canonical ODP/PDF products change here.
  Temporary diagnostic products and the machine-readable inventory are under
  `_temp/replaceme_impact/` and are not durable source artifacts.
- Documentation checks: 801 pass; two fail on missing links in the separate question
  pedagogy/voice guides, which remain untouched. The changed documentation passes its checks.
  The full base suite and attended Impress playback are not rerun for this review.

Counts describe the reviewed snapshot. Categories below are mutually exclusive primary repair
families. Source animation is an additional condition where noted, not a second counted slide.
Source correspondence cases remain unresolved and are excluded from the tool opportunity sets.

### Primary repair families

| Primary repair family | Slides | Interpretation |
| --- | ---: | --- |
| Native fit/review | 130 | Native text/notation, figure sizing, or warning review; no single shared repair established. |
| Native table | 96 | Complete the existing native-table import handoff; source table and preview share one frame. |
| Artwork composition | 69 | Use the existing one-artwork SVG workflow for labels, leaders, highlights, or static masks. |
| Vector figure | 52 | Restore source vector geometry and its attached labels. |
| Multiple artwork | 44 | Preserve relationships among separate pictures while keeping one artwork per SVG. |
| Reveal/media | 23 | Restore staged presentation or source media behavior. |
| Math/media | 17 | Restore equations, source image media, or mathematical spatial notation. |
| Native cards/reveal | 14 | Rebuild native genotype/answer cards and source staging. |
| Table reconstruction | 6 | Rebuild tabular positioned text; these are not ODF native tables. |
| Manual content | 5 | Instructor content or placeholder decision. |
| Source correspondence | 2 | Resolve source-to-current mapping/content before choosing a repair. |
| Sequence alignment | 2 | Keep sequence/dot columns aligned in native monospaced text. |
| **Total** | **460** | |

### Lecture coverage

| Folder | Marked slides |
| --- | ---: |
| `biotech/LECT05` | 1 |
| `biotech/LECT06` | 4 |
| `genetics/LECT06` | 22 |
| `genetics/LECT07` | 30 |
| `genetics/LECT08` | 34 |
| `genetics/LECT11` | 62 |
| `genetics/LECT12` | 101 |
| `genetics/LECT13` | 70 |
| `genetics/LECT14` | 67 |
| `genetics/LECT15` | 69 |

### Code and prior repairs

- [../../slide_lib/importers/odp_page_objects.py](../../slide_lib/importers/odp_page_objects.py):
  `read_frame()` independently calls `add_table()` and `add_picture()` for the same frame.
  `read_vector()` preserves text from text-bearing shapes but generally omits their geometry;
  only a limited set of arrows/outlines gets native overlay records.
- [../../slide_lib/importers/odp_tables.py](../../slide_lib/importers/odp_tables.py):
  `read_table()` retains rectangular text runs, flags merged/covered cells, and does not emit
  source cell fills or span metadata.
- [../../slide_lib/native_model.py](../../slide_lib/native_model.py): `TableCell` already has
  whole-cell fill, horizontal span, and alignment fields. This supports completing an existing
  contract rather than introducing another table renderer.
- [../../slide_lib/importers/native_normalization.py](../../slide_lib/importers/native_normalization.py):
  source-ordered native flow does not retain the spatial attachment of distributed figure labels.
- [../../slide_lib/importers/figure_regions.py](../../slide_lib/importers/figure_regions.py):
  image/label-region recognition exists, including nearby external labels. Recognition alone
  does not create a composed figure.
- [../slide-specs/SVG_DIAGRAMS.md](../slide-specs/SVG_DIAGRAMS.md) documents composed SVG assets and native captions.
  [../../slide_lib/svg_images.py](../../slide_lib/svg_images.py) validates/packages SVG assets.
  The supported CLI has no general figure-composition command in the reviewed tree; existing
  repair assets demonstrate the authoring workflow, not an automatic group-extraction command.
- [../../genetics/LECT06/djot/LECT06_REVIEW.md](../../genetics/LECT06/djot/LECT06_REVIEW.md) and
  [../../genetics/LECT08/djot/LECT08_REVIEW.md](../../genetics/LECT08/djot/LECT08_REVIEW.md)
  record previous successful figure repairs and remaining fit/reveal work. LECT08 local asset
  receipts include `labeled_figures.json` and `static_figure_repairs.json`.

## Per-slide findings

Source numbers are original ODP slide indices; Djot numbers include authored covers and dividers.
Each deck link identifies the canonical root, including slides supplied by its fragment files.
An animation suffix records actual animation actions in the source ODP, not every historical
import warning. Figures already repaired are identified in the relevant finding.

### lect05a-2026_biotech_announcements

[lect05a-2026_biotech_announcements.djot](../../biotech/LECT05/djot/lect05a-2026_biotech_announcements.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| manual | 20 | Manual content | Manual content/placeholder decision; no mapped original ODP page. Canonical slide hidden. |

### lect06a-2026_biotech_announcements

[lect06a-2026_biotech_announcements.djot](../../biotech/LECT06/djot/lect06a-2026_biotech_announcements.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| manual | 20 | Manual content | Manual content/placeholder decision; no mapped original ODP page. Canonical slide hidden. |

### lect06c-set_4_tp_chapter_12_16_material

[lect06c-set_4_tp_chapter_12_16_material.djot](../../biotech/LECT06/djot/lect06c-set_4_tp_chapter_12_16_material.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| manual | 216 | Manual content | Manual content/placeholder decision; no mapped original ODP page. |
| manual | 227 | Manual content | Manual content/placeholder decision; no mapped original ODP page. |
| manual | 233 | Manual content | Manual content/placeholder decision; no mapped original ODP page. |

### lect06c-meiosis

[lect06c-meiosis.djot](../../genetics/LECT06/djot/lect06c-meiosis.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 14 | 14 | Vector figure | Restore the warning symbol beside the figure; source also contains an animation. Source animation also present. |
| 37 | 37 | Multiple artwork | Retain the relationships and readable size of three separate source pictures. |
| 48 | 48 | Table reconstruction | Rebuild the summary grid from positioned text; it is not an ODF native table. |
| 52 | 52 | Artwork composition | Compose the single artwork with its detached identifying labels. |

### lect06d-x_linked_genes_1

[lect06d-x_linked_genes_1.djot](../../genetics/LECT06/djot/lect06d-x_linked_genes_1.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 50 | 50 | Native fit/review | Keep scanned question fragments readable and in their source reading order. |
| 56 | 56 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 57 | 57 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 58 | 58 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 59 | 59 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 60 | 60 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |

### lect06e-x_linked_genes_2

[lect06e-x_linked_genes_2.djot](../../genetics/LECT06/djot/lect06e-x_linked_genes_2.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 4 | 4 | Artwork composition | Restore the static opaque mask over one artwork; do not expose the covered answer. |
| 5 | 5 | Artwork composition | Restore the static opaque mask over one artwork; do not expose the covered answer. |
| 9 | 9 | Native fit/review | Check sex-determination question/answer presentation; source 11 additionally has an animation. |
| 10 | 10 | Native fit/review | Check sex-determination question/answer presentation; source 11 additionally has an animation. |
| 11 | 11 | Native fit/review | Check sex-determination question/answer presentation; source 11 additionally has an animation. Source animation also present. |
| 15 | 15 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 16 | 16 | Vector figure | Restore the drawn ratio axis and the placement of its labels. |
| 21 | 21 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 22 | 22 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 23 | 23 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 24 | 24 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 25 | 25 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |

### lect07a2-genetic_probability

[lect07a2-genetic_probability.djot](../../genetics/LECT07/djot/lect07a2-genetic_probability.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 1 | 2 | Reveal/media | Preserve the source animation or staged question/answer behavior. Source animation also present. |
| 4 | 5 | Reveal/media | Preserve the source animation or staged question/answer behavior. Source animation also present. |
| 7 | 8 | Reveal/media | Preserve the source animation or staged question/answer behavior. Source animation also present. |

### lect07b-prob_of_progeny

[lect07b-prob_of_progeny.djot](../../genetics/LECT07/djot/lect07b-prob_of_progeny.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 9 | 9 | Reveal/media | Restore the correction/reveal sequence, including its crossed-out answer. Source animation also present. |
| 17 | 17 | Math/media | Restore missing mathematical formula media using the existing equation/metafile workflow. |
| 19 | 19 | Math/media | Restore missing mathematical formula media using the existing equation/metafile workflow. |
| 20 | 20 | Math/media | Restore missing mathematical formula media using the existing equation/metafile workflow. |
| 23 | 23 | Math/media | Restore missing mathematical formula media using the existing equation/metafile workflow. |
| 26 | 26 | Math/media | Restore missing mathematical formula media using the existing equation/metafile workflow. |
| 31 | 31 | Math/media | Restore missing mathematical formula media using the existing equation/metafile workflow. |
| 36 | 36 | Math/media | Restore missing mathematical formula media using the existing equation/metafile workflow. |
| 37 | 37 | Math/media | Restore missing mathematical formula media using the existing equation/metafile workflow. |
| 43 | 43 | Math/media | Restore missing mathematical formula media using the existing equation/metafile workflow. |
| 44 | 44 | Math/media | Restore missing mathematical formula media using the existing equation/metafile workflow. |
| 45 | 45 | Math/media | Restore missing mathematical formula media using the existing equation/metafile workflow. |
| 46 | 46 | Math/media | Restore missing mathematical formula media using the existing equation/metafile workflow. |

### lect07c-prob_of_progeny_2

[lect07c-prob_of_progeny_2.djot](../../genetics/LECT07/djot/lect07c-prob_of_progeny_2.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 8 | 8 | Native fit/review | Formula artwork is present; make the six worked calculations readable. |

### lect07d-chi_square

[lect07d-chi_square.djot](../../genetics/LECT07/djot/lect07d-chi_square.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 16 | 18 | Artwork composition | Preserve the selected-row/column highlights and guide lines over the distribution-table artwork. |
| 17 | 19 | Math/media | Restore the missing equation or probability notation beside the table explanation. |
| 18 | 20 | Math/media | Restore the missing equation or probability notation beside the table explanation. |
| 20 | 22 | Artwork composition | Preserve the selected-row/column highlights and guide lines over the distribution-table artwork. |
| 23 | 25 | Multiple artwork | Rebuild the relationships among question, equation, and reference-table fragments without combining their bitmaps. |
| 24 | 26 | Multiple artwork | Rebuild the relationships among question, equation, and reference-table fragments without combining their bitmaps. |
| 25 | 27 | Multiple artwork | Rebuild the relationships among question, equation, and reference-table fragments without combining their bitmaps. |
| 26 | 28 | Multiple artwork | Rebuild the relationships among question, equation, and reference-table fragments without combining their bitmaps. |
| 27 | 29 | Artwork composition | Preserve the selected-row/column highlights and guide lines over the distribution-table artwork. |
| 28 | 30 | Multiple artwork | Rebuild the relationships among question, equation, and reference-table fragments without combining their bitmaps. |
| 29 | 31 | Multiple artwork | Rebuild the relationships among question, equation, and reference-table fragments without combining their bitmaps. |
| 38 | 40 | Artwork composition | Preserve the selected-row/column highlights and guide lines over the distribution-table artwork. |
| 57 | 59 | Source correspondence | Resolve the source-to-current table correspondence before repairing or clearing this marker. |

### lect08b-chap8-linked_genes

[lect08b-chap8-linked_genes.djot](../../genetics/LECT08/djot/lect08b-chap8-linked_genes.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 2 | 4 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 7 | 9 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 15 | 17 | Artwork composition | Keep the chromosome/gamete identifiers attached to the single source artwork; check source guide lines. |
| 16 | 18 | Artwork composition | Keep the chromosome/gamete identifiers attached to the single source artwork; check source guide lines. |
| 17 | 19 | Artwork composition | Keep the chromosome/gamete identifiers attached to the single source artwork; check source guide lines. |
| 18 | 20 | Artwork composition | Keep the chromosome/gamete identifiers attached to the single source artwork; check source guide lines. |
| 30 | 32 | Multiple artwork | Preserve crossover labels and their relationship to the separate source artwork components. |
| 35 | 37 | Reveal/media | A composed SVG already preserves the static figure; the remaining source reveal still needs review. Source animation also present. |
| 36 | 38 | Artwork composition | Keep the product identifiers attached to the artwork; leave explanatory sentences native. |
| 40 | 42 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |

### lect08c-gene_mapping

[lect08c-gene_mapping.djot](../../genetics/LECT08/djot/lect08c-gene_mapping.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 6 | 8 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 17 | 19 | Reveal/media | A composed SVG already preserves the static figure; the remaining source reveal still needs review. Source animation also present. |
| 31 | 34 | Native fit/review | Existing composed SVG preserves labels/masks; remaining issue is readable native calculations and sizing. |
| 35 | 38 | Native fit/review | Existing composed SVG preserves labels/masks; remaining issue is readable native calculations and sizing. |
| 39 | 42 | Native fit/review | Existing composed SVG preserves labels/masks; remaining issue is readable native calculations and sizing. |

### lect08d-3_point_testcross_voss

[lect08d-3_point_testcross_voss.djot](../../genetics/LECT08/djot/lect08d-3_point_testcross_voss.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 10 | 12 | Native fit/review | Existing repaired figure is present; review native calculation fit and teaching sequence. |
| 16 | 19 | Native fit/review | Existing repaired figure is present; review native calculation fit and teaching sequence. |
| 22 | 26 | Native fit/review | Existing repaired figure is present; review native calculation fit and teaching sequence. |
| 24 | 28 | Vector figure | Restore the gene-map bars, connectors, labels, and their source spatial relationships. |
| 25 | 29 | Vector figure | Restore the gene-map bars, connectors, labels, and their source spatial relationships. |
| 26 | 30 | Vector figure | Restore the gene-map bars, connectors, labels, and their source spatial relationships. |
| 27 | 31 | Vector figure | Restore the gene-map bars, connectors, labels, and their source spatial relationships. |
| 28 | 32 | Vector figure | Restore the gene-map bars, connectors, labels, and their source spatial relationships. |
| 29 | 33 | Vector figure | Restore the gene-map bars, connectors, labels, and their source spatial relationships. |
| 30 | 34 | Vector figure | Restore the gene-map bars, connectors, labels, and their source spatial relationships. |
| 31 | 35 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Branch/map drawing also needs repair. |
| 32 | 36 | Vector figure | Restore the gene-map bars, connectors, labels, and their source spatial relationships. |
| 33 | 37 | Vector figure | Restore the gene-map bars, connectors, labels, and their source spatial relationships. |
| 34 | 38 | Vector figure | Restore the gene-map bars, connectors, labels, and their source spatial relationships. |
| 35 | 39 | Vector figure | Restore the gene-map bars, connectors, labels, and their source spatial relationships. |
| 36 | 40 | Vector figure | Restore the gene-map bars, connectors, labels, and their source spatial relationships. |
| 37 | 41 | Vector figure | Restore the gene-map bars, connectors, labels, and their source spatial relationships. |

### lect08e-linked_gene_chi_square

[lect08e-linked_gene_chi_square.djot](../../genetics/LECT08/djot/lect08e-linked_gene_chi_square.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 18 | 20 | Native fit/review | Check highlighted distribution-table emphasis against the source; not a missing label-group conversion. |
| 23 | 25 | Source correspondence | Resolve the source-to-current table correspondence before repairing or clearing this marker. |

### lect11b-polyploidy

[lect11b-polyploidy.djot](../../genetics/LECT11/djot/lect11b-polyploidy.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 8 | 10 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 12 | 14 | Reveal/media | Restore staged presentation of the native question and answer. Source animation also present. |
| 23 | 25 | Artwork composition | Compose one original artwork with its detached species, ploidy, or chromosome identifiers and guide geometry. |
| 27 | 29 | Multiple artwork | Preserve separate artwork components and cross-component relationships; do not put several bitmaps into one SVG. |
| 30 | 32 | Multiple artwork | Preserve separate artwork components and cross-component relationships; do not put several bitmaps into one SVG. |
| 31 | 33 | Artwork composition | Compose one original artwork with its detached species, ploidy, or chromosome identifiers and guide geometry. |
| 32 | 34 | Artwork composition | Compose one original artwork with its detached species, ploidy, or chromosome identifiers and guide geometry. |
| 33 | 35 | Artwork composition | Compose one original artwork with its detached species, ploidy, or chromosome identifiers and guide geometry. |
| 34 | 36 | Multiple artwork | Preserve separate artwork components and cross-component relationships; do not put several bitmaps into one SVG. |
| 36 | 38 | Artwork composition | Compose one original artwork with its detached species, ploidy, or chromosome identifiers and guide geometry. |
| 37 | 39 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 38 | 40 | Artwork composition | Compose one original artwork with its detached species, ploidy, or chromosome identifiers and guide geometry. |
| 43 | 45 | Multiple artwork | Preserve separate artwork components and cross-component relationships; do not put several bitmaps into one SVG. |

### lect11c-sex_dosage

[lect11c-sex_dosage.djot](../../genetics/LECT11/djot/lect11c-sex_dosage.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 4 | 5 | Reveal/media | Native teaching text is present; restore its staged question/answer presentation. Source animation also present. |
| 5 | 6 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 6 | 7 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 17 | 18 | Artwork composition | Keep short genotype, chromosome, or regulatory labels positioned with their single artwork. |
| 28 | 29 | Artwork composition | Keep short genotype, chromosome, or regulatory labels positioned with their single artwork. |
| 29 | 30 | Artwork composition | Keep short genotype, chromosome, or regulatory labels positioned with their single artwork. |
| 41 | 42 | Reveal/media | Native teaching text is present; restore its staged question/answer presentation. Source animation also present. |
| 44 | 45 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 45 | 46 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 46 | 47 | Native fit/review | Keep the native comparison prose and restore its relationship arrow outside ordinary figure composition. |
| 47 | 48 | Artwork composition | Keep short genotype, chromosome, or regulatory labels positioned with their single artwork. |
| 49 | 50 | Native cards/reveal | Rebuild native genotype/answer cards and the source reveal; these are not labeled bitmap figures. Source animation also present. |
| 50 | 51 | Native cards/reveal | Rebuild native genotype/answer cards and the source reveal; these are not labeled bitmap figures. Source animation also present. |
| 51 | 52 | Native cards/reveal | Rebuild native genotype/answer cards and the source reveal; these are not labeled bitmap figures. Source animation also present. |
| 52 | 53 | Native cards/reveal | Rebuild native genotype/answer cards and the source reveal; these are not labeled bitmap figures. Source animation also present. |
| 53 | 54 | Native cards/reveal | Rebuild native genotype/answer cards and the source reveal; these are not labeled bitmap figures. Source animation also present. |
| 54 | 55 | Native cards/reveal | Rebuild native genotype/answer cards and the source reveal; these are not labeled bitmap figures. Source animation also present. |
| 55 | 56 | Native cards/reveal | Rebuild native genotype/answer cards and the source reveal; these are not labeled bitmap figures. Source animation also present. |
| 56 | 57 | Native cards/reveal | Rebuild native genotype/answer cards and the source reveal; these are not labeled bitmap figures. Source animation also present. |
| 57 | 58 | Native cards/reveal | Rebuild native genotype/answer cards and the source reveal; these are not labeled bitmap figures. Source animation also present. |
| 58 | 59 | Native cards/reveal | Rebuild native genotype/answer cards and the source reveal; these are not labeled bitmap figures. Source animation also present. |
| 59 | 60 | Native cards/reveal | Rebuild native genotype/answer cards and the source reveal; these are not labeled bitmap figures. Source animation also present. |
| 60 | 61 | Native cards/reveal | Rebuild native genotype/answer cards and the source reveal; these are not labeled bitmap figures. Source animation also present. |
| 61 | 62 | Native cards/reveal | Rebuild native genotype/answer cards and the source reveal; these are not labeled bitmap figures. Source animation also present. |
| 62 | 63 | Native cards/reveal | Rebuild native genotype/answer cards and the source reveal; these are not labeled bitmap figures. Source animation also present. |
| 64 | 65 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |

### lect11d-chromo_alter_1-deletions

[lect11d-chromo_alter_1-deletions.djot](../../genetics/LECT11/djot/lect11d-chromo_alter_1-deletions.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 14 | 15 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 19 | 20 | Artwork composition | Keep the short genotype identifiers positioned around the single figure; recheck readable figure size. |
| 29 | 30 | Multiple artwork | Preserve deletion-mapping chromosome/table artwork and cross-component masks, arrows, and labels without a multi-bitmap SVG. |
| 30 | 31 | Multiple artwork | Preserve deletion-mapping chromosome/table artwork and cross-component masks, arrows, and labels without a multi-bitmap SVG. |
| 31 | 32 | Multiple artwork | Preserve deletion-mapping chromosome/table artwork and cross-component masks, arrows, and labels without a multi-bitmap SVG. |
| 32 | 33 | Multiple artwork | Preserve deletion-mapping chromosome/table artwork and cross-component masks, arrows, and labels without a multi-bitmap SVG. |
| 33 | 34 | Multiple artwork | Preserve deletion-mapping chromosome/table artwork and cross-component masks, arrows, and labels without a multi-bitmap SVG. |
| 34 | 35 | Multiple artwork | Preserve deletion-mapping chromosome/table artwork and cross-component masks, arrows, and labels without a multi-bitmap SVG. |
| 35 | 36 | Multiple artwork | Preserve deletion-mapping chromosome/table artwork and cross-component masks, arrows, and labels without a multi-bitmap SVG. |
| 36 | 37 | Multiple artwork | Preserve deletion-mapping chromosome/table artwork and cross-component masks, arrows, and labels without a multi-bitmap SVG. |
| 37 | 38 | Multiple artwork | Preserve deletion-mapping chromosome/table artwork and cross-component masks, arrows, and labels without a multi-bitmap SVG. |
| 38 | 39 | Multiple artwork | Preserve deletion-mapping chromosome/table artwork and cross-component masks, arrows, and labels without a multi-bitmap SVG. |
| 39 | 40 | Multiple artwork | Preserve deletion-mapping chromosome/table artwork and cross-component masks, arrows, and labels without a multi-bitmap SVG. |
| 40 | 41 | Multiple artwork | Preserve deletion-mapping chromosome/table artwork and cross-component masks, arrows, and labels without a multi-bitmap SVG. |
| 41 | 42 | Multiple artwork | Preserve deletion-mapping chromosome/table artwork and cross-component masks, arrows, and labels without a multi-bitmap SVG. |
| 91 | 92 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 92 | 93 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 94 | 95 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 99 | 101 | Table reconstruction | Rebuild the gene-order answer grid natively beside the scanned question. |
| 108 | 110 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |

### lect11e-chromo_alter_2-duplications

[lect11e-chromo_alter_2-duplications.djot](../../genetics/LECT11/djot/lect11e-chromo_alter_2-duplications.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 14 | 16 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 20 | 22 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 26 | 28 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |

### lect12b-gene_trees

[lect12b-gene_trees.djot](../../genetics/LECT12/djot/lect12b-gene_trees.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 10 | 12 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 11 | 13 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 12 | 14 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 13 | 15 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 14 | 16 | Artwork composition | Restore distance guides on the tree artwork; leave the separate scanned question outside this figure. |
| 15 | 17 | Artwork composition | Restore distance guides on the tree artwork; leave the separate scanned question outside this figure. |
| 16 | 18 | Artwork composition | Restore distance guides on the tree artwork; leave the separate scanned question outside this figure. |
| 19 | 21 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 20 | 22 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 24 | 26 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 27 | 29 | Artwork composition | Restore the selection outline over the sequence-alignment artwork. |
| 42 | 44 | Sequence alignment | Preserve monospaced sequence/dot columns in native text. |
| 43 | 45 | Sequence alignment | Preserve monospaced sequence/dot columns in native text. |
| 44 | 46 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Sequence alignment also needs repair. |
| 45 | 47 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Sequence alignment also needs repair. |
| 46 | 48 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Sequence alignment also needs repair. |
| 47 | 49 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Sequence alignment also needs repair. |
| 48 | 50 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Sequence alignment also needs repair. |
| 49 | 51 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Sequence alignment also needs repair. |
| 50 | 52 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Sequence alignment also needs repair. |
| 51 | 53 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Sequence alignment also needs repair. |
| 52 | 54 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Sequence alignment also needs repair. |
| 53 | 55 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Sequence alignment also needs repair. |
| 55 | 57 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 56 | 58 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 57 | 59 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 58 | 60 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 59 | 61 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Branch/map drawing also needs repair. |
| 60 | 62 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Branch/map drawing also needs repair. |
| 61 | 63 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Branch/map drawing also needs repair. |
| 62 | 64 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Branch/map drawing also needs repair. |
| 63 | 65 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Branch/map drawing also needs repair. |
| 64 | 66 | Vector figure | Restore the completed native vector gene tree and its branch labels. |
| 67 | 69 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 68 | 70 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 69 | 71 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 70 | 72 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 71 | 73 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 72 | 74 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |

### lect12c-more_gene_trees

[lect12c-more_gene_trees.djot](../../genetics/LECT12/djot/lect12c-more_gene_trees.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 3 | 4 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 5 | 6 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 6 | 7 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 7 | 8 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 8 | 9 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 9 | 10 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 10 | 11 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 11 | 12 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 12 | 13 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 13 | 14 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 14 | 15 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 15 | 16 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 16 | 17 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 17 | 18 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 18 | 19 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 19 | 20 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 20 | 21 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 21 | 22 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 22 | 23 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 23 | 24 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 24 | 25 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 26 | 27 | Artwork composition | Restore figure paths around one tree artwork; source animation is an additional blocker. Source animation also present. |
| 29 | 30 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 30 | 31 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 31 | 32 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 32 | 33 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 33 | 34 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 34 | 35 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 35 | 36 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 36 | 37 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 37 | 38 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 38 | 39 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Branch/map drawing also needs repair. |
| 39 | 40 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Branch/map drawing also needs repair. |
| 40 | 41 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 44 | 46 | Multiple artwork | Preserve the readable relationship among five separate matrix/equation/sequence pictures. |
| 45 | 47 | Artwork composition | Restore opaque masks on the tree artwork; keep the matrix bitmap separate and arithmetic/caption native. |
| 46 | 48 | Artwork composition | Restore opaque masks on the tree artwork; keep the matrix bitmap separate and arithmetic/caption native. |
| 47 | 49 | Artwork composition | Restore opaque masks on the tree artwork; keep the matrix bitmap separate and arithmetic/caption native. |
| 48 | 50 | Artwork composition | Restore opaque masks on the tree artwork; keep the matrix bitmap separate and arithmetic/caption native. |
| 49 | 51 | Artwork composition | Restore opaque masks on the tree artwork; keep the matrix bitmap separate and arithmetic/caption native. |
| 50 | 52 | Artwork composition | Restore opaque masks on the tree artwork; keep the matrix bitmap separate and arithmetic/caption native. |
| 51 | 53 | Artwork composition | Restore opaque masks on the tree artwork; keep the matrix bitmap separate and arithmetic/caption native. |
| 52 | 54 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |

### lect12d-gene_tree_activity

[lect12d-gene_tree_activity.djot](../../genetics/LECT12/djot/lect12d-gene_tree_activity.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 3 | 5 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 8 | 10 | Artwork composition | Restore matrix highlight overlays, with one artwork per composed SVG and any calculation caption native. |
| 9 | 11 | Artwork composition | Restore matrix highlight overlays, with one artwork per composed SVG and any calculation caption native. |
| 10 | 12 | Artwork composition | Restore matrix highlight overlays, with one artwork per composed SVG and any calculation caption native. |
| 12 | 14 | Native fit/review | No active source highlight shape is present; recheck figure size before retaining the old highlight warning. |
| 13 | 15 | Artwork composition | Restore matrix highlight overlays, with one artwork per composed SVG and any calculation caption native. |
| 14 | 16 | Artwork composition | Restore matrix highlight overlays, with one artwork per composed SVG and any calculation caption native. |
| 16 | 18 | Native fit/review | No active source highlight shape is present; recheck figure size before retaining the old highlight warning. |
| 17 | 19 | Artwork composition | Restore matrix highlight overlays, with one artwork per composed SVG and any calculation caption native. |
| 18 | 20 | Artwork composition | Restore matrix highlight overlays, with one artwork per composed SVG and any calculation caption native. |
| 20 | 22 | Native fit/review | No active source highlight shape is present; recheck figure size before retaining the old highlight warning. |
| 21 | 23 | Artwork composition | Restore matrix highlight overlays, with one artwork per composed SVG and any calculation caption native. |
| 22 | 24 | Artwork composition | Restore matrix highlight overlays, with one artwork per composed SVG and any calculation caption native. |
| 24 | 26 | Artwork composition | Restore matrix highlight overlays, with one artwork per composed SVG and any calculation caption native. |
| 25 | 27 | Artwork composition | Restore matrix highlight overlays, with one artwork per composed SVG and any calculation caption native. |
| 26 | 28 | Artwork composition | Restore matrix highlight overlays, with one artwork per composed SVG and any calculation caption native. |
| 27 | 29 | Artwork composition | Restore matrix highlight overlays, with one artwork per composed SVG and any calculation caption native. |
| 28 | 30 | Native fit/review | No active source highlight shape is present; recheck figure size before retaining the old highlight warning. |

### lect12e-evol_time

[lect12e-evol_time.djot](../../genetics/LECT12/djot/lect12e-evol_time.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 5 | 7 | Multiple artwork | Rebuild the molecule/sequence figure relationships while preserving separate source pictures. |

### lect13b-chromo_alter_3-inversion

[lect13b-chromo_alter_3-inversion.djot](../../genetics/LECT13/djot/lect13b-chromo_alter_3-inversion.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 8 | 10 | Artwork composition | Restore source vector crossover annotations around the artwork; source animation is an additional blocker. Source animation also present. |
| 12 | 14 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 14 | 16 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 21 | 23 | Artwork composition | Restore crossover arrows or selected-region outlines on the chromosome/problem artwork, keeping question prose separate. |
| 22 | 24 | Artwork composition | Restore crossover arrows or selected-region outlines on the chromosome/problem artwork, keeping question prose separate. |
| 25 | 27 | Artwork composition | Restore crossover arrows or selected-region outlines on the chromosome/problem artwork, keeping question prose separate. |
| 28 | 30 | Artwork composition | Restore crossover arrows or selected-region outlines on the chromosome/problem artwork, keeping question prose separate. |
| 29 | 31 | Artwork composition | Restore crossover arrows or selected-region outlines on the chromosome/problem artwork, keeping question prose separate. |
| 30 | 32 | Artwork composition | Restore crossover arrows or selected-region outlines on the chromosome/problem artwork, keeping question prose separate. |
| 31 | 33 | Artwork composition | Restore crossover arrows or selected-region outlines on the chromosome/problem artwork, keeping question prose separate. |
| 34 | 36 | Multiple artwork | Preserve relationships among eye and chromosome artwork and their external identifiers. |

### lect13c-chromo_alter_4-translocation

[lect13c-chromo_alter_4-translocation.djot](../../genetics/LECT13/djot/lect13c-chromo_alter_4-translocation.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 6 | 8 | Multiple artwork | Preserve the three source components and their association with the native explanation. |
| 7 | 9 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 8 | 10 | Artwork composition | Restore the chromosome identifiers around the single artwork. |
| 10 | 12 | Reveal/media | Restore the staged native question, choices, and answer presentation. Source animation also present. |
| 13 | 15 | Vector figure | Restore the native gene-string diagram, curved arrows, and numbered relationships; keep the scanned question separate. |
| 14 | 16 | Vector figure | Restore the native gene-string diagram, curved arrows, and numbered relationships; keep the scanned question separate. |
| 15 | 17 | Vector figure | Restore the native gene-string diagram, curved arrows, and numbered relationships; keep the scanned question separate. |
| 16 | 18 | Vector figure | Restore the native gene-string diagram, curved arrows, and numbered relationships; keep the scanned question separate. |
| 17 | 19 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 18 | 20 | Vector figure | Restore the native gene-string diagram, curved arrows, and numbered relationships; keep the scanned question separate. |
| 19 | 21 | Reveal/media | Restore the staged native question, choices, and answer presentation. Source animation also present. |
| 21 | 23 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 25 | 27 | Reveal/media | Restore the staged native question, choices, and answer presentation. Source animation also present. |
| 27 | 29 | Reveal/media | Restore the staged native question, choices, and answer presentation. Source animation also present. |

### lect13d-meiosis_translocation

[lect13d-meiosis_translocation.djot](../../genetics/LECT13/djot/lect13d-meiosis_translocation.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 4 | 6 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 7 | 9 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 8 | 10 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 9 | 11 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 10 | 12 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 11 | 13 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 12 | 14 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 13 | 15 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 14 | 16 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 15 | 17 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 16 | 18 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 17 | 19 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 18 | 20 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 19 | 21 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 20 | 22 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 21 | 23 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 22 | 24 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 23 | 25 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 24 | 26 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 25 | 27 | Vector figure | Restore the entirely missing native vector chromosome drawing; no source bitmap exists to label. |
| 27 | 29 | Artwork composition | Attach short chromosome identifiers to the appropriate artwork; keep setup and pairing-rule prose native. |
| 28 | 30 | Artwork composition | Attach short chromosome identifiers to the appropriate artwork; keep setup and pairing-rule prose native. |
| 29 | 31 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 30 | 32 | Multiple artwork | Recover the spatial relationship among separate chromosome/gamete panels, guide lines, masks, and identifiers. |
| 32 | 34 | Artwork composition | Attach short chromosome identifiers to the appropriate artwork; keep setup and pairing-rule prose native. |
| 33 | 35 | Multiple artwork | Recover the spatial relationship among separate chromosome/gamete panels, guide lines, masks, and identifiers. |
| 34 | 36 | Multiple artwork | Recover the spatial relationship among separate chromosome/gamete panels, guide lines, masks, and identifiers. |
| 37 | 39 | Artwork composition | Attach short chromosome identifiers to the appropriate artwork; keep setup and pairing-rule prose native. |
| 38 | 40 | Multiple artwork | Recover the spatial relationship among separate chromosome/gamete panels, guide lines, masks, and identifiers. |
| 39 | 41 | Multiple artwork | Recover the spatial relationship among separate chromosome/gamete panels, guide lines, masks, and identifiers. |
| 40 | 42 | Multiple artwork | Recover the spatial relationship among separate chromosome/gamete panels, guide lines, masks, and identifiers. |
| 41 | 43 | Multiple artwork | Recover the spatial relationship among separate chromosome/gamete panels, guide lines, masks, and identifiers. |
| 42 | 44 | Multiple artwork | Recover the spatial relationship among separate chromosome/gamete panels, guide lines, masks, and identifiers. |
| 43 | 45 | Vector figure | Restore the native vector chromosome/translocation diagram; some slides also need masks or native question cards. Source animation also present. |
| 44 | 46 | Vector figure | Restore the native vector chromosome/translocation diagram; some slides also need masks or native question cards. |
| 45 | 47 | Vector figure | Restore the native vector chromosome/translocation diagram; some slides also need masks or native question cards. |
| 46 | 48 | Vector figure | Restore the native vector chromosome/translocation diagram; some slides also need masks or native question cards. |
| 47 | 49 | Vector figure | Restore the native vector chromosome/translocation diagram; some slides also need masks or native question cards. |
| 48 | 50 | Vector figure | Restore the native vector chromosome/translocation diagram; some slides also need masks or native question cards. |
| 49 | 51 | Vector figure | Restore the native vector chromosome/translocation diagram; some slides also need masks or native question cards. |
| 50 | 52 | Vector figure | Restore the native vector chromosome/translocation diagram; some slides also need masks or native question cards. |
| 53 | 55 | Artwork composition | Attach short species/chromosome identifiers to the fusion artwork; keep the explanatory conclusion native. |
| 54 | 56 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 55 | 57 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 58 | 60 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |

### lect14b-allele_freq

[lect14b-allele_freq.djot](../../genetics/LECT14/djot/lect14b-allele_freq.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 11 | 13 | Artwork composition | Restore the static cover over allele-count artwork; keep the question text outside the SVG. |
| 12 | 14 | Artwork composition | Restore the static cover over allele-count artwork; keep the question text outside the SVG. |
| 14 | 16 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 15 | 17 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 16 | 18 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 25 | 27 | Reveal/media | Native allele-frequency calculation is present; preserve its source reveal sequence. Source animation also present. |

### lect14c-hardy_weinberg_1

[lect14c-hardy_weinberg_1.djot](../../genetics/LECT14/djot/lect14c-hardy_weinberg_1.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 2 | 4 | Vector figure | Restore the allele/genotype frequency boxes and the connecting relationship arrow; keep definition prose native. |
| 3 | 5 | Vector figure | Restore the allele/genotype frequency boxes and the connecting relationship arrow; keep definition prose native. |
| 8 | 10 | Vector figure | Restore the allele/genotype frequency boxes and the connecting relationship arrow; keep definition prose native. |
| 18 | 20 | Math/media | Preserve the spatial genotype-frequency equation/label alignment and readable mathematical notation. |
| 19 | 21 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 20 | 22 | Multiple artwork | Restore the wildflower/genotype diagram with multiple distinct source artwork components. |
| 21 | 23 | Math/media | Restore the missing source equation/metafile and genotype-flow relationships. |
| 22 | 24 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 27 | 29 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 38 | 40 | Reveal/media | Native worked answer is present; preserve the source staged problem solution. Source animation also present. |
| 40 | 42 | Reveal/media | Native worked answer is present; preserve the source staged problem solution. Source animation also present. |
| 41 | 43 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 42 | 44 | Reveal/media | Native worked answer is present; preserve the source staged problem solution. Source animation also present. |
| 44 | 46 | Reveal/media | Native worked answer is present; preserve the source staged problem solution. Source animation also present. |
| 47 | 49 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 49 | 51 | Table reconstruction | Rebuild the blood-group/genotype/frequency columns as a native table; the source uses positioned text. |
| 50 | 52 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 52 | 54 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 53 | 55 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 56 | 58 | Artwork composition | Attach the short male/female genotype/frequency identifiers to the single artwork; keep explanatory prose native. |
| 57 | 59 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 58 | 60 | Table reconstruction | Rebuild the blood-group/genotype/frequency columns as a native table; the source uses positioned text. |
| 59 | 61 | Table reconstruction | Rebuild the blood-group/genotype/frequency columns as a native table; the source uses positioned text. |
| 60 | 62 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |

### lect14d-hardy_weinberg_conditions

[lect14d-hardy_weinberg_conditions.djot](../../genetics/LECT14/djot/lect14d-hardy_weinberg_conditions.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 4 | 5 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 6 | 7 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 11 | 12 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Source animation also present. |
| 12 | 13 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 13 | 14 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 14 | 15 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 15 | 16 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 16 | 17 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 17 | 18 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Source animation also present. |
| 19 | 20 | Reveal/media | Preserve the source staged allele-frequency solution. Source animation also present. |
| 20 | 21 | Reveal/media | Preserve the source staged allele-frequency solution. Source animation also present. |
| 26 | 27 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 29 | 30 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 30 | 31 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 31 | 32 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 32 | 33 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |

### lect14e-hardy_weinberg_chi_square

[lect14e-hardy_weinberg_chi_square.djot](../../genetics/LECT14/djot/lect14e-hardy_weinberg_chi_square.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 3 | 4 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 5 | 6 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 6 | 7 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 7 | 8 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 8 | 9 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 9 | 10 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 10 | 11 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 13 | 14 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 15 | 16 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Source animation also present. |
| 16 | 17 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 17 | 18 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 18 | 19 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. Source animation also present. |
| 19 | 20 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 20 | 21 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 25 | 27 | Reveal/media | Preserve the source staged allele/genotype-frequency solution. Source animation also present. |
| 26 | 28 | Reveal/media | Preserve the source staged allele/genotype-frequency solution. Source animation also present. |
| 27 | 29 | Reveal/media | Preserve the source staged allele/genotype-frequency solution. Source animation also present. |
| 28 | 30 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 29 | 31 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 31 | 33 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 32 | 34 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |

### lect15b-genetic_evolution

[lect15b-genetic_evolution.djot](../../genetics/LECT15/djot/lect15b-genetic_evolution.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 3 | 4 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 9 | 10 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 10 | 11 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 12 | 13 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 13 | 14 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 15 | 16 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 16 | 17 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |

### lect15c-natural_selection

[lect15c-natural_selection.djot](../../genetics/LECT15/djot/lect15c-natural_selection.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 5 | 7 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 6 | 8 | Artwork composition | Keep the short spore-cloud identifier and leader attached to the photograph. |
| 7 | 9 | Vector figure | Restore the lost observation/inference flowchart boxes and connectors; keep its text editable. |
| 12 | 14 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 13 | 15 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 18 | 20 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 21 | 23 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 22 | 24 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 24 | 26 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 30 | 32 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 40 | 42 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 44 | 46 | Multiple artwork | Restore the three selection-mode plots and their labels without merging separate source pictures into one SVG. |
| 47 | 49 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 49 | 51 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 50 | 52 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 51 | 53 | Artwork composition | Restore bounded short parameter/fitness labels around the single graph; keep ordinary explanatory prose native. |
| 52 | 54 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 54 | 56 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 56 | 58 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 58 | 60 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 63 | 65 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 64 | 66 | Native fit/review | Rebuild readable native worked-problem panels; keep scanned question and equation artwork separate from explanatory prose. |
| 65 | 67 | Native fit/review | Rebuild readable native worked-problem panels; keep scanned question and equation artwork separate from explanatory prose. |
| 66 | 68 | Native fit/review | Rebuild readable native worked-problem panels; keep scanned question and equation artwork separate from explanatory prose. |
| 67 | 69 | Native fit/review | Rebuild readable native worked-problem panels; keep scanned question and equation artwork separate from explanatory prose. |
| 68 | 70 | Native fit/review | Rebuild readable native worked-problem panels; keep scanned question and equation artwork separate from explanatory prose. |
| 69 | 71 | Native fit/review | Rebuild readable native worked-problem panels; keep scanned question and equation artwork separate from explanatory prose. |
| 70 | 72 | Native fit/review | Rebuild readable native worked-problem panels; keep scanned question and equation artwork separate from explanatory prose. |
| 72 | 74 | Native fit/review | Rebuild readable native worked-problem panels; keep scanned question and equation artwork separate from explanatory prose. |

### lect15d-genetic_drift

[lect15d-genetic_drift.djot](../../genetics/LECT15/djot/lect15d-genetic_drift.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 3 | 5 | Multiple artwork | Restore population/bottleneck figures and their component-specific labels without combining separate pictures into one SVG. |
| 4 | 6 | Multiple artwork | Restore population/bottleneck figures and their component-specific labels without combining separate pictures into one SVG. |
| 5 | 7 | Multiple artwork | Restore population/bottleneck figures and their component-specific labels without combining separate pictures into one SVG. |
| 9 | 11 | Artwork composition | Keep the original-population identifier attached to its single bottle artwork. |
| 10 | 12 | Multiple artwork | Restore population/bottleneck figures and their component-specific labels without combining separate pictures into one SVG. |
| 11 | 13 | Multiple artwork | Restore population/bottleneck figures and their component-specific labels without combining separate pictures into one SVG. |
| 14 | 16 | Table reconstruction | Rebuild the missing positioned-text table and keep the prairie-chicken/map artwork separate. |
| 20 | 22 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 24 | 26 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 25 | 27 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 27 | 29 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 30 | 32 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |

### lect15e-inbreeding

[lect15e-inbreeding.djot](../../genetics/LECT15/djot/lect15e-inbreeding.djot)

| Source | Djot | Primary repair | Finding |
| ---: | ---: | --- | --- |
| 13 | 15 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 15 | 17 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 16 | 18 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 18 | 20 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 20 | 22 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 21 | 23 | Native table | Repair native table duplication, cell styling/spans, or table-associated highlights; preserve editable cells. |
| 23 | 25 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 29 | 31 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 33 | 35 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 34 | 36 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 36 | 38 | Math/media | Restore the missing calculator-window image; the surviving dialog alone is incomplete. |
| 38 | 40 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 39 | 41 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 40 | 42 | Artwork composition | Restore the two crossed-out founders over the pedigree artwork. |
| 41 | 43 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 42 | 44 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 48 | 50 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 49 | 51 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 54 | 56 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
| 55 | 57 | Native fit/review | Retain pedigree prominence and native common-ancestor/path answer text; keep prose outside the SVG. |
| 56 | 58 | Native fit/review | Recheck native text, notation, figure prominence, and source relationships; no missing bounded figure established. |
