# Lecture 05 conversion

Eight decks were converted on 2026-09-28 from the ODPs in `../old/`. The supplied
2026 announcements are authoritative; the 2025 announcements remain historical evidence.
The canonical sources retain all 325 source slides in order. None of these inputs has hidden pages.

| Source | Authored | Visible | Hidden |
| --- | ---: | ---: | ---: |
| [lect05a-2026_announcements.djot](lect05a-2026_announcements.djot) | 35 | 35 | 0 |
| [lect05b-unknown_genotype_problems.djot](lect05b-unknown_genotype_problems.djot) | 16 | 16 | 0 |
| [lect05c-pedigree.djot](lect05c-pedigree.djot) | 49 | 49 | 0 |
| [lect05d-probability_concepts.djot](lect05d-probability_concepts.djot) | 31 | 31 | 0 |
| [lect05e-probability_problems.djot](lect05e-probability_problems.djot) | 36 | 36 | 0 |
| [lect05f-degrees_of_dominance.djot](lect05f-degrees_of_dominance.djot) | 52 | 52 | 0 |
| [lect05g-more_probability_problems.djot](lect05g-more_probability_problems.djot) | 19 | 19 | 0 |
| [lect05h-epistasis.djot](lect05h-epistasis.djot) | 87 | 87 | 0 |
| Total | 325 | 325 | 0 |

## Teaching-layout repairs

- Covers identify Lecture 05A--05H and September 29, 2026. The copied Lecture 04A cover and
  agenda now identify Lecture 05 topics. The announcement cover uses Chapter 5 from the updated
  course schedule; the content-deck chapter labels follow the supplied teaching decks.
- The assessment dates edited in the supplied 2026 announcements remain unchanged: Quiz 2 on
  October 6 and the midterm on October 13. The source's later quiz schedule remains provisional.
- Covers, informational dividers, and final `theend` pages use explicit native layouts.
- Genuine source images remain local component assets. Figure explanations use separate native
  text regions; repeated teaching steps remain separate source slides.
- The incomplete-dominance cross, ABO genotypes, codominant donor/recipient results, and
  recessive-epistasis Punnett square replace four importer placeholders with editable content.
  The pea-pigment pathway, squash genotype classes, AB x AB answer, and F2/testcross ratio
  sequences also replace missing vector relationships with explicit editable teaching structure.
  The donor directions were checked against original 05F PDF page 33.
- Probability examples group detached alleles into their cross and event definitions. The
  selected-round-seed solution retains its cross, conditional proportions, and final 1/3 result
  in short phrases. Bateson/Punnett figures retain their parental cross and F1/F2 outcomes.
- A zero-width polyline on original 05H slide 60 remains an unsupported-object review reason
  rather than preventing import. Bounded finite lengths and rejection of negative dimensions
  remain enforced. No original ODP was changed.

## Lecture 04 comparison

The teaching edits in `../../LECT04/2026/` were compared with the available generated ODPs and
canonical Lecture 04 sources. This comparison informs Lecture 05; Lecture 04 sources are unchanged.

- 04A removes the Zoom and purchased-textbook pages, revises assessment and homework dates, and
  drops the "Assignment 3 is due tonight" reminder. Lecture 05 uses the supplied 2026 material.
- 04C breaks long question stems into shorter lines. Several content decks regroup figure labels
  and captions; some imported labels were previously disconnected from their illustrations.
- 04G restores the dependent-versus-independent assortment diagram where generated content had
  only a reconstruction placeholder. Punnett-square sequences in 04F/04G also contain edited
  label positions and teaching steps. This is why Lecture 05's reconstruction placeholders were
  replaced with explicit crosses, tables, or donor-direction results.
- 04B's extracted text is unchanged. Equal text does not establish equal visual layout; this
  comparison does not claim that every manual geometry adjustment has been cataloged.

## Verification boundary

Import provenance and original presenter notes remain in each local
`assets/<deck>/import_report.json`. These reports describe initial extraction, before the repairs
above. Generated ODPs and PDFs live under `output/odp/` and `output/pdf/` at repository root.

Strict Jotdown and semantic lint pass for eight sources, 325 slides, and 206 image references.
The focused importer tests pass (22 tests). The final build produces eight editable ODPs and eight
ODP-derived PDFs; each output has the same page count as its source. Contact sheets covered all
325 pages, followed by larger checks of repaired teaching figures. This is a bounded visual review,
not an attended Impress playback test.

Capacity inspection reports two remaining regions below the 20 pt body floor: 05B page 15 at
19.5 pt and 05D page 27 at 14.5 pt. The latter retains the inherited conditional-probability issue
below and needs instructor revision. The other reported dense regions were shortened or regrouped
without adding or removing slides.

Broader repository checks found existing failures in nine archived Biotechnology text files, an
oversized [DESIGN_DECISIONS.md](../../../docs/DESIGN_DECISIONS.md), and a stale Biotechnology review link. The test auto-fixes to
previously clean archived inputs were restored; those unrelated files are unchanged.

One inherited content issue needs instructor review: 05D's final Huntington-disease conditional
probability example gives inconsistent values for P(A|B) and P(B). Its original arithmetic is
retained; the conversion does not silently choose a different question or disease assumption.

Rebuild the lecture with:

```bash
source source_me.sh && python3 deck_tools.py build genetics/LECT05 --format all
```

## Selected visual checks

Final ODP-derived pages were inspected at larger size after the contact-sheet sweep. Scores use
[SLIDE_VISUAL_REVIEW_RUBRIC.md](../../../docs/SLIDE_VISUAL_REVIEW_RUBRIC.md): readability,
organization, hierarchy, space, and effectiveness, each out of four. These are advisory checks.

| Page | Read | Organize | Hierarchy | Space | Effective | Total | Concern |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 05A 26 | 4 | 4 | 4 | 3 | 4 | 19 | No concern: grouped quiz instructions are readable. |
| 05F 6 | 3 | 4 | 4 | 3 | 3 | 17 | Minor: flower image small; native cross carries the teaching point. |
| 05F 15 | 4 | 4 | 4 | 3 | 4 | 19 | No concern: allele legend and genotype table stay separate. |
| 05F 21 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: native AB cross replaces a missing answer diagram. |
| 05F 33 | 3 | 4 | 4 | 3 | 4 | 18 | Minor: source mouse figure small; editable table states donor directions. |
| 05H 54 | 3 | 4 | 4 | 3 | 4 | 18 | Minor: dense Punnett square remains legible alongside phenotype classes. |
| 05D 27 | 2 | 2 | 2 | 2 | 1 | 9 | Material: dense inherited explanation and contradictory equations need revision. |

The final epistasis source escapes unknown-allele underscores explicitly; these must remain
visible allele notation rather than being interpreted as Djot emphasis.

## Automatic GDI preservation

The importer now preserves embedded SVM/EMF/WMF figures as component images. It selects a
package-local raster alternative when supplied, otherwise converts the individual figure through
LibreOffice to PNG. A component-sized Draw page prevents default-page padding and clipping.

Complete trial imports under `/private/tmp/lect05_gdi_import/` preserved all 325 slides. These
inputs contain 47 SVM frame references: 42 have raster alternatives and five require conversion.
The five converted components were checked visually; 141 importer, geometry, and Python lint
checks pass. The trial imports validate the new importer behavior; the authored sources above
retain their reviewed teaching edits.

## Announcement corrections

Instructor screenshot review prompted restored contact-method colors, red assessment labels,
bold grade-percentage names, clearer grade-book wording, and short clickable link labels. The
anonymous-message screenshot comes from the supplied 2025 announcement ODP (the edited 2026
source had replaced it with duplicate prose). It remains a historical Blackboard navigation image.
Named and numeric entities now decode in native text, including the apostrophe in "Don't Panic"
and schedule dashes; verbatim text stays literal.

The [instructor's schedule spreadsheet](https://docs.google.com/spreadsheets/d/1XLZcg8PnW4GyMxFctAKCTvzN9qImIb5S3bK6hyeDz0Q/edit)
was read on September 28, 2026. Quiz dates are September 22, October 6, November 3, November 17,
and December 8; the midterm is October 13 (Chapters 1-4), and the cumulative final is December 15.
Homework dates were updated from the same sheet. The announcement deck remains 35 slides.

Static and weekly content are still in one authored file. Reusable source inclusion remains
specified by the [deck-includes plan](../../../docs/active_plans/active/djot_deck_includes_plan.md)
and is not implemented by these corrections.

## Pedigree color corrections

- Restored 46 missing colored text spans from the source ODP: inheritance answer choices,
  autosomal answer headings, recessive labels, and male/female emphasis.
- Strict native validation passes all 49 slides. Rebuilt ODP/PDF and visually checked slides
  13, 17, 24, and 29 for the restored colors.

## Remaining deck color audit

- Checked A/B/D/E/F/G/H against the original ODP text styles. A retains the announcement
  corrections; restored missing color emphasis in B/D/E/F/G/H on 35 pages.
- B: band exclusion clues and same-gene conclusions. D/E/G: blue general-rule formulas,
  event labels, red probability terms, and green/blue worked-example factors.
- F: restored red parent/F1 genotypes and F2 ratios in donor/recipient slides, blood-type
  emphasis, and the green/blue/red dominance choices.
- H: orange experiment labels, red/blue experiment authors, and missing answer/ratio emphasis.
  Yellow/brown use readable orange; the teal band clue and mustard conditional factor use blue
  within the supported semantic palette. Original figure colors remain in local image assets.
- Strict native validation passes 325 slides. Rebuilt all eight ODP/PDF pairs and reviewed all
  35 changed pages. No new capacity concerns; D slide 27 remains the documented dense example
  with source mathematical contradictions requiring instructor review.

## Probability allele subscripts

- Converted all 68 editable A1-A4 occurrences in D to numeric references for subscript digits,
  including colored labels, crosses, and Punnett-table headers/cells.
- Strict native validation passes 31 slides. Rebuilt ODP/PDF and visually checked slides 11
  and 14 for subscript glyphs and retained colors.

## Epistasis deep revision

A [dedicated Lecture 05H review](LECT05H_REVIEW.md) supersedes the earlier selected 05H score.
Sixty slides were improved while preserving all 87 source positions. Missing pea, squash, and
Labrador Punnett squares are restored as native tables; pathway stages now show blocked reactions
and their consequences. Native phenotype-group tables distinguish F2 counts from testcross counts.
Cat gene labels, the flower-count normalization, and genotype-versus-phenotype prompts were corrected.
Strict native validation passes; capacity inspection has no 05H concerns. The rebuilt ODP/PDF
received a full contact-sheet sweep and larger checks of the repaired teaching objects.

## Lecture 05F notation repair

Restored 28 ABO allele superscripts, 50 C-locus allele superscripts (preserving uppercase
and lowercase source letters), and 52 F/P generation subscripts across 14 slides.
Numeric character references keep the Djot sources ASCII and the native text editable.
Strict native validation and capacity checks pass for all 52 slides. Rebuilt both ODP
and PDF and visually reviewed every changed page, including the ABO Punnett square,
flower crosses, donor/recipient table, and dominance-game genotypes.
