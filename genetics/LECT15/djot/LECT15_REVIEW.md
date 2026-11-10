# LECT15 conversion review

Four canonical content decks: Evolution, Selection, Drift, and Inbreeding.
Renumbered from LECT1X on November 9, 2026, at the instructor's request.
Preserves 184 original content slides and 11 previously added bookends/dividers.
69 explicit `@replaceme` slides remain reconstruction tasks.

[LECT15_SOURCE_MAP.md](LECT15_SOURCE_MAP.md) maps every original and final slide.

## November 10 agenda addition

Add `lect15a-agenda.djot`, a one-slide agenda using the B-E titles: Genetics and Evolution,
Natural Selection, Genetic Drift, and Inbreeding, plus the drift activity. It retains Chapter 10.
This is an undated
agenda-only deck; the course schedule supplies no Lecture 15 teaching date. No full announcement
deck was supplied. Rebuilt ODP/PDF, passed strict native lint, and inspected the agenda.
The wording correction passes 213 documentation/guidance checks. Evidence: `_temp/genetics_agendas_09_15/`.
The wording correction is verified separately in `_temp/genetics_agenda_voice/`.
The existing B-E conversion limitations below are unchanged.

## Outputs and counts

Canonical Djot and local assets are in this directory. Editable ODP and ODP-derived PDF
use the same deck stem under `output/odp/` and `output/pdf/` at the repository root.

| Canonical deck | Authored ODP | Hidden | PDF pages | Replacements |
| --- | --- | --- | --- | --- |
| lect15a-agenda | 1 | 0 | 1 | 0 |
| lect15b-genetic_evolution | 22 | 0 | 22 | 7 |
| lect15c-natural_selection | 77 | 1 | 76 | 29 |
| lect15d-genetic_drift | 35 | 0 | 35 | 12 |
| lect15e-inbreeding | 61 | 0 | 61 | 21 |

Total including the new agenda: 196 authored, 1 hidden, 195 visible PDF pages.

## Organization and source files

Whole content decks were assigned to the two lectures; no teaching slide was split, merged,
or reordered within a deck. Content filenames and covers now use letters B-E, reserving A
for announcements. No original announcement source or teaching date was supplied for these numbers;
the new A source supplies only the agenda.
Original ODP/PDF inputs and extracted assets moved with their corresponding content.
Original input files retain identical bytes; their old filenames remain provenance below.
Import reports retain their original input labels. Includes and live asset references use
the new paths. LECT1X no longer contains a separate copy of these decks.

| Former input filename | Retained input location | Canonical Djot |
| --- | --- | --- |
| lect1Xe-genetic_evolution.odp | ../lect15b-genetic_evolution.odp | lect15b-genetic_evolution.djot |
| lect1Xf-natural_selection.odp | ../lect15c-natural_selection.odp | lect15c-natural_selection.djot |
| lect1Xg-genetic_drift.odp | ../lect15d-genetic_drift.odp | lect15d-genetic_drift.djot |
| lect1Xg-inbreeding.odp | ../lect15e-inbreeding.odp | lect15e-inbreeding.djot |

Original authored/hidden/animation inventory:

- `lect1Xe-genetic_evolution.odp`: 20 authored; hidden none; source animation elements none.
- `lect1Xf-natural_selection.odp`: 74 authored; hidden 2; source animation elements none.
- `lect1Xg-genetic_drift.odp`: 32 authored; hidden none; source animation elements none.
- `lect1Xg-inbreeding.odp`: 58 authored; hidden none; source animation elements none.

Source section order, `lect15b-genetic_evolution`: 2 From this point forward, no more equations will appear on the exam. Only definitions. -> 11 Irreversible Mutation A&#8594;a -> 14 Reversible Mutations and Equilibrium A&#8594;a and a&#8594;A -> 20 THE END.

Source section order, `lect15c-natural_selection`: 3 Natural Selection -> 11 Selection in a Laboratory Experiment -> 14 Individual Fitness, w, Relative Fitness, W, and  Selection Coefficient -> 20 Selection in Diploid Organisms -> 23 True or False: Saving lives of persons with rare recessive disorders (e.g. cystic fibrosis) will cause a deterioration of gene pool. -> 25 Dark-light Insect selection example -> 41 Directionality of Natural Selection -> 45 Selection-Mutation Balance -> 53 Heterozygote Superiority -> 74 THE END.

Source section order, `lect15d-genetic_drift`: 7 The Bottleneck Effect -> 12 Case Study: the Greater Prairie Chicken -> 16 Heterozygosity -> 22 Genetic Drift Activity -> 32 THE END.

Source section order, `lect15e-inbreeding`: 4 How can you tell if an animal is inbread? -> 6 Effects of Inbreeding -> 14 Inbreeding Coefficient -> 17 The inbreeding coefficient of individual is the probability that the individual carries alleles that are identical by descent. -> 22 Calculate the Inbreeding Coefficient of Individual (COI) -> 24 What percent DNA do you share with your aunt? 50% offspring (mother to son) &#215; 50% sisters (mother to aunt) = 25% DNA shared -> 25 What percent DNA do you share with your grandfather&#8217;s sister&#8217;s kids? -> 26 What percent DNA do you share with your grandfather&#8217;s sister&#8217;s kids? 25% grandfather &#215; 50% sibling (gpa to sister) &#215; 50% offspring (sister to kid) = 0.25&#215;0.5&#215;0.5 = 6.25% -> 32 My Family Story -> 37 The Closed Loop Method for Calculating the Coefficient of Inbreeding (COI) -> 58 THE END.


Sibling include fragments remain parts of their master deck, keeping source files below
the repository line limit. Original closing slides, appendices, and added closing bookends
keep their existing positions. Existing definitions, objectives, and summaries are retained.

## Cover dates and course schedule

Cover numbers now identify Lecture 15B-E. Chapter 10 and the existing December 8, 2026
cover date were retained. The local schedule at
`/Users/vosslab/nsh/syllabus/site_docs/fall_2026/genetics/SCHEDULE.md` ends with Lecture 13
on December 8 and the final exam on December 15. It supplies no Lecture 14/15 dates.
**The retained cover date is not a newly scheduled Lecture 14/15 class. Update it when the
teaching dates are chosen.** No assessment deadline or announcement was invented.

## Preserved conversion findings

The initial conversion compared all visible original content pages with watermark-free
diagnostic renders in `_temp/lect12_13_1x/review/`. That history uses former deck names.
This reorganization changes covers and file/asset references only. All 353 non-cover PDF
pages across Lectures 14 and 15 have identical native text; 243 also have identical pixels.
The remaining 110 pages show small font/glyph rendering variations. The largest measured
character-origin shift is 0.222 pt; selected paired differences preserve the layout.
Hidden and replacement flags are identical to the preceding authored sources.
All eight new covers were rendered and visually inspected. Evidence and current slide maps
are under `_temp/lect14_15/`. Original input/media hashes also reconcile after the moves.

Preserved tasks below use original ODP slide numbers. The source map gives current Djot/PDF
positions. Replacement watermarks remain until the native repair is rendered and compared
with the original. Selectable prose/bookends remain native; scanned source text stays raster.

Natural-selection, drift, and pedigree geometry remains incomplete on marked slides.
Colored definitions retain the verified white-background repair. The ancillary drift ODG,
ODS, and their two PDFs moved here as `lect15x-*` with identical bytes.
The evolution deck's old exam-policy statement remains historical source content. Dated
medical prevalence, legal-map claims, and terminology in scanned problems were preserved
without a new scientific, medical, or legal fact-check.

### lect15b-genetic_evolution

Cleared after paired/rendered verification: source 11, 14.

- Source 3 -> Djot 4: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 9 -> Djot 10: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 10 -> Djot 11: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 12 -> Djot 13: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 13 -> Djot 14: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 15 -> Djot 16: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 16 -> Djot 17: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.

### lect15c-natural_selection

Cleared after paired/rendered verification: source 4, 9-10, 14-15, 17, 31-39, 42.

- Source 5 -> Djot 7: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 6 -> Djot 8: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 7 -> Djot 9: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 12 -> Djot 14: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 13 -> Djot 15: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 18 -> Djot 20: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 21 -> Djot 23: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 22 -> Djot 24: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 24 -> Djot 26: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 30 -> Djot 32: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 40 -> Djot 42: figure or notation remains too small or loses source emphasis; rework the native layout/figure and compare with the original.
- Source 44 -> Djot 46: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 47 -> Djot 49: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 49 -> Djot 51: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 50 -> Djot 52: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 51 -> Djot 53: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 52 -> Djot 54: figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 54 -> Djot 56: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 56 -> Djot 58: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 58 -> Djot 60: figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 63 -> Djot 65: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 64 -> Djot 66: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 65 -> Djot 67: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 66 -> Djot 68: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 67 -> Djot 69: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 68 -> Djot 70: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 69 -> Djot 71: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 70 -> Djot 72: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 72 -> Djot 74: figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.

### lect15d-genetic_drift

Cleared after paired/rendered verification: source 18-19, 28.

- Source 3 -> Djot 5: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 4 -> Djot 6: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 5 -> Djot 7: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 9 -> Djot 11: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 10 -> Djot 12: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 11 -> Djot 13: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 14 -> Djot 16: prairie-chicken table labels/values missing from the converted figure; reconstruct the complete labeled table and map.
- Source 20 -> Djot 22: figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 24 -> Djot 26: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 25 -> Djot 27: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 27 -> Djot 29: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 30 -> Djot 32: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.

### lect15e-inbreeding

Cleared after paired/rendered verification: source 8-9, 12, 17.

- Source 13 -> Djot 15: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 15 -> Djot 17: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 16 -> Djot 18: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 18 -> Djot 20: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 20 -> Djot 22: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 21 -> Djot 23: table spans, highlights, or native/bitmap duplication unresolved; source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 23 -> Djot 25: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 29 -> Djot 31: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 33 -> Djot 35: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 34 -> Djot 36: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 36 -> Djot 38: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 38 -> Djot 40: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 39 -> Djot 41: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 40 -> Djot 42: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 41 -> Djot 43: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 42 -> Djot 44: source geometry, labels, or spatial grouping unresolved; rework the native layout/figure and compare with the original.
- Source 48 -> Djot 50: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 49 -> Djot 51: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 54 -> Djot 56: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 55 -> Djot 57: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.
- Source 56 -> Djot 58: source geometry, labels, or spatial grouping unresolved; figure/text allocation or readable fit unresolved; rework the native layout/figure and compare with the original.

## Capacity and typography

Capacity and typography audits were rerun for the new folders. Existing warnings remain
advisory; every mixed-readability failure retains its explicit replacement marker.
Existing source wording and shorter-title suggestions from the initial review are retained.

| Deck / Djot | Slot | Cause | Required / floor pt | Review outcome |
| --- | --- | --- | --- | --- |
| lect15c-natural_selection / 9 | body | mixed-readability | 14.5 / 20.0 | Retain replacement marker. |
| lect15c-natural_selection / 15 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect15c-natural_selection / 46 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect15c-natural_selection / 51 | top-left | paragraph/list | 11.25 / 20.0 | Retain replacement marker. |
| lect15c-natural_selection / 52 | left | paragraph/list | 16.75 / 20.0 | Retain replacement marker. |
| lect15c-natural_selection / 53 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect15c-natural_selection / 58 | bottom-left | paragraph/list | 15.0 / 20.0 | Retain replacement marker. |
| lect15c-natural_selection / 60 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect15c-natural_selection / 66 | top | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect15c-natural_selection / 67 | top | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect15c-natural_selection / 68 | top | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect15c-natural_selection / 70 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect15c-natural_selection / 72 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect15c-natural_selection / 74 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect15d-genetic_drift / 5 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect15d-genetic_drift / 11 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect15d-genetic_drift / 12 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect15d-genetic_drift / 13 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect15d-genetic_drift / 30 | top-left | paragraph/list | 18.0 / 20.0 | Below-floor advisory retained; inspect at teaching distance. |
| lect15e-inbreeding / 5 | top-left | paragraph/list | 14.5 / 20.0 | Below-floor advisory retained; inspect at teaching distance. |
| lect15e-inbreeding / 15 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect15e-inbreeding / 17 | body | paragraph/list | 18.5 / 20.0 | Retain replacement marker. |
| lect15e-inbreeding / 20 | bottom-right | table | 15.25 / 20.0 | Retain replacement marker. |
| lect15e-inbreeding / 22 | top-right | table | 11.0 / 20.0 | Retain replacement marker. |
| lect15e-inbreeding / 23 | top-right | table | 11.0 / 20.0 | Retain replacement marker. |
| lect15e-inbreeding / 38 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect15e-inbreeding / 47 | left | paragraph/list | 17.75 / 20.0 | Below-floor advisory retained; inspect at teaching distance. |
| lect15e-inbreeding / 48 | right | paragraph/list | 17.0 / 20.0 | Below-floor advisory retained; inspect at teaching distance. |
| lect15e-inbreeding / 57 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect15e-inbreeding / 58 | body | mixed-readability | 20.0 / 20.0 | Retain replacement marker. |
| lect15e-inbreeding / 59 | top-right | paragraph/list | 13.25 / 20.0 | Below-floor advisory retained; inspect at teaching distance. |

Typography summary: {'runt': 5, 'title-wrap': 14}. Skipped coverage: {'special-layout-titles': 8, 'final-paragraph-runts-at-max-size': 3, 'hidden-slides': 1}.

| Deck / Djot | Finding | Review or possible shorter title |
| --- | --- | --- |
| lect15c-natural_selection / 12 | runt in body, paragraph 1 | Existing wording retained; advisory line fit. |
| lect15c-natural_selection / 15 | Title wraps | Selection for Allele A in E. coli |
| lect15c-natural_selection / 21 | Title wraps | Selection for Allele A in E. coli |
| lect15c-natural_selection / 30 | Title wraps | Light and Dark Peppered Moths |
| lect15c-natural_selection / 33 | runt in body, paragraph 1 | Existing wording retained; advisory line fit. |
| lect15c-natural_selection / 39 | runt in body, paragraph 7 | Existing wording retained; advisory line fit. |
| lect15c-natural_selection / 48 | Title wraps | Population Size and Mutation-Drift Balance |
| lect15c-natural_selection / 53 | Title wraps | Dominance of a Recessive Lethal Allele |
| lect15c-natural_selection / 54 | Title wraps | Heterozygosity and Mutation-Drift Balance |
| lect15c-natural_selection / 59 | runt in body, paragraph 1 | Existing wording retained; advisory line fit. |
| lect15c-natural_selection / 60 | Title wraps | Sickle-Cell Anemia and Malaria Distribution |
| lect15d-genetic_drift / 26 | Title wraps | Drift in 12 Populations |
| lect15d-genetic_drift / 27 | Title wraps | Drift in 12 Populations |
| lect15d-genetic_drift / 28 | Title wraps | Pooled Allele Frequency Stays Constant |
| lect15d-genetic_drift / 30 | Title wraps | Drift in 107 Drosophila Populations |
| lect15e-inbreeding / 13 | Title wraps | Inbreeding and Rare Recessive Homozygotes |
| lect15e-inbreeding / 15 | Title wraps | Inbreeding Reduces Heterozygosity |
| lect15e-inbreeding / 20 | runt in left, paragraph 4 | Existing wording retained; advisory line fit. |
| lect15e-inbreeding / 32 | Title wraps | First-Cousin Marriage in Illinois |

## Validation and limits

- Strict native Djot lint and all-format LibreOffice builds passed for all eight masters.
  Source includes/assets resolve; ODP authored/hidden counts, PDF pages, and every visible
  replacement watermark reconcile. Rebuild logs are `_temp/lect14_15/lect*_build.log`.
- Each non-cover PDF page was compared with its previous exported page, including exact
  native text and rendered pixels. The eight changed covers retain native selectable text.
- Base suite: 4,051 passed, 3 failed, 87 errors. The failures/errors are the pre-existing
  Biotechnology LECT10 problems. Log: `_temp/lect14_15/pytest_final.log`.
  Existing Biotechnology LECT10 working-tree conflicts remain outside this task.
- Attended Impress click playback, classroom/Zoom testing, and independent scientific
  fact-checks remain unperformed. Initial conversion warnings/tasks still apply.
- Source images/import reports and generated ODP/PDF remain ignored by Git. They exist
  in this checkout; a source-only Git handoff does not contain all teaching media.

## Conversion checklist

The completed initial-conversion checklist is retained below. This follow-up repeated
the affected inventory, source links, cover, lint, audit, build, comparison, and count checks.
Announcement/date items remain inapplicable or unresolved as described above.

Copied from the repository conversion checklist. Checked review items can retain documented
replacement outcomes. N/A and unperformed checks are annotated explicitly.

### Inventory the inputs

- [x] List every source ODP and existing Djot deck in the review report; identify the version
  being converted and the canonical announcement deck before copying or importing anything.
- [x] Record each source deck's authored slide count, hidden slide numbers, section order,
  and slides with animations or answer reveals.
- [x] Generate or locate a source PDF for visual comparison. Map source slide numbers to
  visible PDF pages, explicitly accounting for hidden slides.
- [x] Content cover date recorded above; announcement format example N/A. Record the lecture date and the schedule/spreadsheet used for weekly updates, including
  its path or URL. Identify the instructor-cleaned announcement deck used as a format example.

### Initial conversion and assembly

- [ ] N/A: no announcement deck. Follow the instructor-edited announcement formatting: put very long URLs in `@citation`,
  keeping their complete clickable destinations.
- [ ] N/A: no announcement deck. Show the quiz-guidance group if a quiz is this week or next week; hide it otherwise.
  Control the included group's visibility with one `hidden` setting.
- [ ] N/A: no announcement deck. Reference course-wide evergreen groups for recurring opening slides and quiz/exam guidance.
  Keep the agenda, selected icebreaker/podcast, assessment colors, and dated deadlines weekly.
- [ ] N/A: no announcement deck. Retain first-week assignments and future course-evaluation slides as hidden reusable
  groups. Verify their inventory survives the weekly update; refresh dates before showing them.

- [x] Keep source filenames, source slide numbers, and conversion provenance out of Djot files,
  including `@notes` and comments. Use separate import reports, slide maps, or review files for
  traceability; reserve `@notes` for presentation note cards used while lecturing. Exclude selection history,
  publication metadata, refresh commands, repair details, and verification logs from Djot files.

- [x] Import each source with the repository importer documented in [USAGE.md](../../../docs/USAGE.md).
  Save the generated Djot, component assets, and import report; list their paths in the review.
  For an existing conversion, locate these artifacts instead of overwriting reviewed source.
- [x] Build a source-to-Djot slide map. Account for every source slide, its relative order,
  and hidden status; verify one-to-one correspondence through existing content and list added
  slides separately so counts reconcile. Record human approval for any source-slide splitting.
- [x] Update each cover's course, lecture number, date, and topic. Check the rendered cover
  against the cover requirements in the pedagogical guide.
- [x] Verify each cover's chapter number against the relevant BPW course index linked from
  [HUMAN_GUIDANCE.md](../../../docs/HUMAN_GUIDANCE.md). Do not infer it from the lecture number;
  announcements have no chapter.
- [x] Locate the learning objectives in each content deck. If absent, add content-derived
  objectives on slide 2; record the resulting slide number.
- [x] Inspect generated objectives for runts. Shorten generated wording to one line where practical;
  otherwise avoid a single-word final line and aim for a final line at least one-third of the text
  width. Recheck the render. Preserve instructor-authored wording unless edits are authorized.
- [x] Run `python3 deck_tools.py audit <djot-file-or-folder>` using the repository Python
  environment. The audit exempts final-paragraph runts at maximum body size.
  Review title-wrap and runt findings against the rendered slides; record skipped
  coverage and unresolved warnings. Findings are advisory, not automatic wording changes.
- [x] Verify condensed URLs remain intact after independent sizing down to 12 pt. Review
  `url-too-wide` audit warnings; preserve complete displayed addresses and clickable destinations.
- [x] Compare important terminology with previous lectures and locate existing definitions.
  If useful, add a definitions slide near the beginning for important terms new to the lecture
  sequence. Keep definitions concise and limited to terms used in the lecture; list the added
  slide in the slide map.
- [x] Locate the closing summary in each content deck. If absent, add content-derived
  takeaways immediately before THE END; verify the closing slide order in the PDF.
- [x] Check section boundaries against the existing lecture outline. Insert missing dividers
  only to label existing topic boundaries, without reorganizing the teaching sequence;
  list any inserted dividers in the slide map.

### Recurring lecture announcement updates

Use [../../../docs/slide-specs/ANNOUNCEMENT_DECK_GUIDE.md](../../../docs/slide-specs/ANNOUNCEMENT_DECK_GUIDE.md) for the announcement order,
section hierarchy, seasonal groups, and signup/profile deadlines.

- [x] Add an undated agenda-only source with this lecture's topics and activities; compare each agenda
  item with the content decks and current course schedule.
- [ ] N/A: no announcement source supplied. Check every assessment and assignment date against the schedule/spreadsheet. Update
  relative wording, deadline/status colors, and expired assignment entries for the lecture date.
- [ ] N/A: no announcement source supplied. Compare announcement visibility with this week's plan. Record every changed hidden flag;
  confirm evergreen Discord information remains even when its signup assignment expires.
- [ ] N/A: no announcement source supplied. Select the week's icebreaker explicitly from `evergreen/icebreakers.yaml` or an instructor selection.
  Copy its prompt/examples and remove any stale week/date label; record the selected catalog key.
- [ ] N/A: no announcement source supplied. Preview the StVC refresh with
  `source source_me.sh && python3 -m slide_lib.refresh_podcast DECK.djot`.
  Inspect the selected episode before applying `--write`.
- [ ] N/A: no announcement source supplied. Confirm the latest published regular StVC episode available on the lecture date, excluding
  specials, and use it as the default. Record its number; if another episode is more appropriate,
  select it and document why.
- [ ] N/A: no announcement source supplied. Verify the saved StVC episode number/title, video URL, thumbnail, and playable game/tool
  URL all refer to the selected episode. Open both links and inspect the downloaded image.
- [ ] N/A: no announcement source supplied. Inspect the rendered StVC slide: confirm three caption lines, visible clickable video
  and game/tool URLs, and placement immediately after the YouTube channel slide.
- [ ] N/A: no announcement source supplied. Check the YouTube channel, anonymous-message, Discord, and applicable Zoom slides.
  Verify their images/QR codes and visible clickable URLs; keep private course URLs in
  `course_links.local.yaml` through `{{course_url:key}}` references.

### Repair individual slides

- [ ] Visible pages compared; hidden content checked as text/XML only. Compare every source slide with its rendered conversion, including slides without importer
  warnings. Record missing text, labels, objects, emphasis, and changed reading order by slide.
- [x] Inspect the content underneath existing replacement watermarks using separate diagnostic
  copies. Reassess the actual failure rather than inheriting an old import warning. Keep diagnostic
  copies clearly labeled; removing a watermark for inspection does not clear the canonical marker.
- [x] Copy colored text and emphasis faithfully from the source: match colors, colored spans,
  bold, underline, and cross-references in the Djot and rendered PDF. Do not flatten colored text
  during conversion. Check repeated procedure slides against the same canonical colored version.
- [ ] N/A: no new three-point testcross problem. Before a new three-point testcross problem, repeat the matching colored roadmap: the
  pairwise-distance checklist for full mapping, or the DCO checklist for quick gene-order exercises.
  Keep the two methods' step numbering distinct. Use the fixed [COLOR_PALETTE.md](../../../docs/COLOR_PALETTE.md)
  colors in rainbow order, with matching colored step cross-references.
- [x] Remove textbook figure-number artifacts from titles, captions, citations, and editable
  diagram labels. Keep meaningful explanatory captions and all diagram content.
- [x] Wrapped titles retained; shorter wording proposed above for review. Inspect every rendered title for single-line fit, following the preference in
  [HUMAN_GUIDANCE.md](../../../docs/HUMAN_GUIDANCE.md). Flag wrapping titles and record proposed shorter
  wording for review; permission to rewrite titles remains separate from checking their length.
- [x] For textbook diagrams assembled from artwork and positioned labels, compare label placement,
  arrows, and diagram relationships with the source. Record whether a labeled image reconstruction
  is a suitable repair; retain the replacement marker until the rendered result is verified.
- [ ] N/A: no new labeled-image reconstruction. Where suitable, use one quality-90 WebP inside SVG with live overlapping labels. Keep titles,
  captions, surrounding prose, and native tables outside the asset. Verify the LibreOffice render
  and review any source reveals separately; a static figure does not certify animation fidelity.
- [x] Preserve source vector figures as vectors with live labels. Restore static diagram highlights
  and masks within their figure, and preserve paint order so hidden answers do not reappear above
  opaque masks. Verify both masked and unmasked regions against the source.
- [x] Check each figure's identity against the source render, including orientation and cropping;
  a plausible diagram or matching subject is insufficient evidence that it is the right asset.
- [x] Static-mask losses retained as replacement tasks; no new click masks authored. Distinguish static masks from actual reveal targets using the source ODP. Use an image-relative
  native cover for an explicitly intended click-to-remove image mask; check bounds against the final
  displayed image. Test native targets/order and record unperformed click playback separately.
- [x] Confirm local headings and all other content share region sizing, and subsection backgrounds
  follow the course accent. Do not compensate for allocation defects by rewriting source prose.
- [x] For sequential text/image content split across panels, try the existing one-panel mixed
  flow and compare the render. Keep the grouping with readable labels and correct reading order;
  record unresolved fit failures rather than adding a special layout.
- [x] Inspect images for excess borders and composite panels. Trim empty margins and cut,
  split, or crop images where this improves their fit and associations with nearby text.
  Use derived assets or cropped views so the original remains recoverable. Compare against
  the source to preserve labels, arrows, scale bars, legends, and meaningful spacing; update
  overlapping label coordinates when cropping labeled images. Image splitting is authorized;
  splitting slides still requires human approval.
- [x] Run the [image-area audit](../../../docs/USAGE.md#audit-image-shrinkage) for matching source/conversion
  slides. Inspect flagged shrinkage and record the chosen repair or retained review reason;
  after slide insertions, use the source map rather than assuming page numbers still align.
- [x] Compare every table's headers, values, totals, blank calculation cells, and progressive
  steps with the source. Rebuild representable tables as native tables and inspect their PDF.
- [x] Inspect rendered equations and genetic notation against the source: fractions, chi-square,
  allele superscripts, generation subscripts, and H~0~. Correct misplaced or baseline characters.
- [ ] Static states/source animation inventory checked; attended playback unperformed. Compare source animation targets/order with the converted reveals. Inspect final PDF states
  and test click playback in Impress for affected slides, or explicitly record playback as untested.
- [x] For each unresolved slide, add or retain `@replaceme` and record its source number, specific
  missing feature, and next action. When readable sizing cannot fit, retain the source slide with
  `@replaceme`, the preferred outcome over splitting. Do not make splitting the default repair;
  any split requires human approval.
- [x] Before clearing any replacement marker, compare the repaired render with the original and
  verify the previously missing content or behavior; record the evidence in the review report.

### Build and hand off

- [x] Run `source source_me.sh && python3 deck_tools.py lint --require-native
  --native-executable "$(command -v jotdown)" LECTURE_DIR` as one command.
  Save its result and resolve parser/semantic errors.
- [x] Run `source source_me.sh && python3 deck_tools.py capacity LECTURE_DIR`.
  Inspect each diagnostic and record a repair or slide-specific unresolved finding.
- [x] Run `source source_me.sh && python3 deck_tools.py build LECTURE_DIR --format all`
  outside the sandbox. Confirm an editable ODP and ODP-derived PDF exist for every deck.
- [x] Inspect every visible PDF page against the source using
  [the visual review rubric](../../../docs/slide-specs/SLIDE_VISUAL_REVIEW_RUBRIC.md) as assessment guidance. Inspect dense
  text, small diagram labels, tables, and repaired slides at readable size; record problems and
  repairs, then rerender and recheck subsequent edits. Routine conversion review does not require
  per-slide numerical scores; the separate scored review is advisory and runs on demand.
- [x] Reconcile final ODP authored counts and PDF visible counts with the slide map, hidden flags,
  and added slides. Count remaining replacement markers per deck and list their source numbers.
- [x] Finish the lecture review report with output paths, validation results, repaired slides,
  unresolved slides, and unperformed checks. Distinguish reviewed draft completion from
  classroom readiness when replacement slides remain.
- [x] Add a concise conversion/review entry to [CHANGELOG.md](../../../docs/CHANGELOG.md), naming the lecture
  and resulting artifacts; report the review and output paths to the instructor.
