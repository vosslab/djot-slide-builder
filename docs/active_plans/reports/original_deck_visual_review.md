# Original deck visual review

## Scope and method

This is the WP-S3 advisory review of the eight final LibreOffice-derived PDFs in
`output/pdf/` against the corresponding originals in `genetics/`. It covers 336
generated pages and the same 336 original/generated page pairs. `pdfinfo` reported
matching counts for every deck. All pages were rendered to 90 dpi contact sheets;
the flagged pairs below were also rendered at 180 dpi and inspected at readable size.

This report applies [SLIDE_VISUAL_REVIEW_RUBRIC.md](../../SLIDE_VISUAL_REVIEW_RUBRIC.md).
Its scores and comparison calls are advisory evidence, not deterministic gates.

## Standalone quality

The generated corpus is visually consistent: the theme is applied throughout, titles
and section dividers are clear, images generally retain their useful framing, and no
whole-slide raster fallback was observed. The main exception is the 16 pages listed
under material findings, which visibly announce missing positioned diagram labels.

| Total band | Pages | Review call |
| --- | ---: | --- |
| 18-20 | 208 | Generally strong |
| 15-17 | 108 | Contextual review; no material concern |
| 0-14 | 16 | Advisory attention required |

The per-dimension distributions are below. No page scored 0 or 2 in an individual
dimension; the 16 attention pages score 1 in every dimension because the missing
labels remove the diagram's instructional relationship.

| Dimension | 4 | 3 | 1 |
| --- | ---: | ---: | ---: |
| Readability | 158 | 162 | 16 |
| Visual organization | 183 | 137 | 16 |
| Emphasis and hierarchy | 174 | 146 | 16 |
| Use of space | 163 | 157 | 16 |
| Overall effectiveness | 180 | 140 | 16 |

The page-level scoring worksheet was deliberately disposable implementation evidence.
This retained baseline records its distributions and every advisory outlier rather
than adding a fragile permanent test or a 336-row artifact.

## Migration comparison

The generated slides are roughly equivalent on 272 pages and improved on 48 pages.
The improvement calls chiefly reflect clearer, consistent hierarchy on headings,
questions, and standardized answer treatment without losing the instructional order.
Sixteen pages are materially worse because the original's positioned diagram labels
are not present in the generated slide.

| Deck | Improved | Roughly equivalent | Materially worse |
| --- | ---: | ---: | ---: |
| `lect01a-course_intro` | 6 | 25 | 0 |
| `lect01b-genetic_disorders` | 4 | 19 | 0 |
| `lect02a-2025_announcements` | 5 | 38 | 0 |
| `lect02b-genes_dogma` | 7 | 31 | 11 |
| `lect02c-genome_sizes` | 12 | 47 | 0 |
| `lect02d-dna_structure_overview` | 6 | 37 | 0 |
| `lect02e-restriction_enzymes` | 7 | 51 | 4 |
| `lect02f-dna_electrophoresis` | 1 | 24 | 1 |
| Total | 48 | 272 | 16 |

## Material findings

These are observed visual failures, not inferred structural warnings. At readable
resolution, each generated page retains part of the source drawing but replaces the
labels that explain it with `Native reconstruction needed: ... positioned diagram
labels.` The result removes a necessary teaching relationship and warrants a
`material concern` and `materially worse` comparison call.

| Deck/page | Visible teaching effect |
| --- | --- |
| `lect02b-genes_dogma` pp. 12, 19-27, 41 | Mendelian and biochemical diagrams lose their positioned explanatory labels. |
| `lect02e-restriction_enzymes` pp. 53-56 | Restriction-enzyme figures lose labels for cuts, sticky ends, and outcomes. |
| `lect02f-dna_electrophoresis` p. 11 | The electrophoresis apparatus loses its directional and component labels. |

No other page was judged materially worse. Dense source-derived reference material
and long URLs remain small on some pages, but their generated counterparts preserve
the original instructional role and are no worse than the originals; they are
contextual, not material, concerns.

### Closeout disposition

The 16 findings are accepted explicit source-migration limitations for this closeout.
Their source pages already state `Native reconstruction needed`; the approved plan
forbids Djot prose and image edits, and the rejected canonical-SVG diagram
abstraction is not reintroduced to address them. They remain material visual findings
in this baseline, but they do not leave a required implementation action.

## Evidence and limits

The review used `pdfinfo` for page counts and `pdftoppm` contact sheets for all 672
rendered pages. It then compared the 16 flagged original/generated pairs at 180 dpi.
The temporary render bundle was generated outside the repository at
`/private/tmp/djot_visual_review/` and removed after this report was recorded;
no source, generated deck, test, or permanent image artifact was changed by this
review.

The rubric is intentionally non-gating. It cannot establish editability, XML
structure, image aspect ratio, chrome absence, or page identity; those remain the
deterministic verification lanes. The material findings do establish that the present
PDF corpus has the documented, accepted diagram-label limitations above.
