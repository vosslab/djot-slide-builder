# Lecture 08 conversion review

Converted October 26, 2026. Originals remain unchanged one directory above.
The six Djot sources use existing layouts; no teaching prose was rewritten.
Content covers use the October 27, 2026 lecture date and Chapter 8, verified
against the [BPW Genetics index](https://biologyproblems.org/genetics/).

## Source selection

- B-F come from the corresponding original ODPs, retaining all 210 slides and
  the one hidden C slide. Per-slide import evidence is under `assets/<deck>/import_report.json`.
- A reuses the maintained LECT07 2026 Djot announcements and its local assets,
  following HG rather than converting the obsolete 2025 announcements.
- Only announcement cover metadata and Quiz 3/Weeks 07-08 deadline colors change.
  Dates were checked against the instructor schedule spreadsheet on October 26.
  The inherited Lecture 07 agenda, pets question, podcast episode 36, and historical
  notes remain verbatim under the conversion-only instruction. They are not current-week revisions.

## Verification

- Strict Jotdown parsing and semantic lint pass for all six sources.
- All six covers pass the existing HG cover checker.
- Repository builds produce six editable ODPs and six LibreOffice-derived PDFs.
  LibreOffice runs outside the sandbox.
- ODP slide counts and PDF visible-page counts match Djot: 248 authored,
  234 visible, 14 hidden. Original content-deck PDFs match the 209 visible B-F pages.
- Original/generated B-F contact sheets were compared for all visible pages;
  repaired pages were rendered again. Hidden C2 retains the original internal note.
- Eight native chi-square tables retain the source numeric values and blank cells.
  Their headers use stacked equation fractions; the total has a separate final row.
- F27-29 source XML identifies the answer paragraphs as on-click appear targets.
  Existing three-panel layouts now carry corresponding native appear reveals.
  Their ODP timing metadata was checked; attended Impress playback was not performed.
- One-time checks, build logs, and reviewed contact sheets are in `_temp/lect08/`;
  no new permanent tests or compiler changes were added.

## Remaining limitations

Replacement markers denote representation failures, not requests to rewrite content.
Source table highlights, column masks, connected chromosome diagrams, and unsupported
animations remain visibly flagged. The flagged drafts are not ready for classroom use.
Some retain only partial native content; use their original ODP and import evidence
when reconstructing them. No whole-slide screenshots replace editable slide content.

C6 and image-heavy F5 retain smaller figures than the originals. Dense text slides
retain their authored wording and can require smaller type. Capacity warnings remain
in the build log; unresolved low-capacity diagram slides retain their replacement marks.

## Deck inventory

| Deck | Authored | Visible | Replacement marks |
| --- | --- | --- | --- |
| [lect08a-2026_announcements.djot](lect08a-2026_announcements.djot) | 38 | 25 | 0 |
| [lect08b-chap8-linked_genes.djot](lect08b-chap8-linked_genes.djot) | 41 | 41 | 19 |
| [lect08c-gene_mapping.djot](lect08c-gene_mapping.djot) | 46 | 45 | 19 |
| [lect08d-3_point_testcross_voss.djot](lect08d-3_point_testcross_voss.djot) | 44 | 44 | 32 |
| [lect08e-linked_gene_chi_square.djot](lect08e-linked_gene_chi_square.djot) | 25 | 25 | 6 |
| [lect08f-3_point_testcross_textbook.djot](lect08f-3_point_testcross_textbook.djot) | 54 | 54 | 33 |

## LECT08B findings

| Source slide | Comparison | Finding |
| --- | --- | --- |
| 1 | improved | Standard title layout; same topic, canonical chapter and current lecture metadata. |
| 2 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 3 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 4 | materially worse; flagged | Positioned labels and their diagram relationships need reconstruction. |
| 5 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 6 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 7 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 8 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 9 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 10 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 11 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 12 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 13 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 14 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 15 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 16 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 17 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 18 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 19 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 20 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 21 | materially worse; flagged | Source grid lost its row/column relationships. |
| 22 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 23 | materially worse; flagged | Source grid lost its row/column relationships. |
| 24 | materially worse; flagged | Positioned labels and their diagram relationships need reconstruction. |
| 25 | materially worse; flagged | Source grid lost its row/column relationships. |
| 26 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 27 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 28 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 29 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 30 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 31 | materially worse; flagged | Positioned labels and their diagram relationships need reconstruction. |
| 32 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 33 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 34 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 35 | materially worse; flagged | Positioned labels and their diagram relationships need reconstruction. |
| 36 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 37 | materially worse; flagged | Positioned labels and their diagram relationships need reconstruction. |
| 38 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 39 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 40 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 41 | roughly equivalent | Existing theend layout preserves the authored closer and native star. |

## LECT08C findings

| Source slide | Comparison | Finding |
| --- | --- | --- |
| 1 | improved | Standard title layout; same topic, canonical chapter and current lecture metadata. |
| 2 | hidden; structural review | Original internal note and hidden status retained; no source PDF page. |
| 3 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 4 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 5 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 6 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. Figures are smaller; inspect at presentation scale. |
| 7 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 8 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 9 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 10 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 11 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 12 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 13 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 14 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 15 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 16 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 17 | materially worse; flagged | Positioned labels and their diagram relationships need reconstruction. |
| 18 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 19 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 20 | materially worse; flagged | Source reveal/mask sequence is unresolved; static PDF is insufficient. |
| 21 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 22 | materially worse; flagged | Positioned labels and their diagram relationships need reconstruction. |
| 23 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 24 | materially worse; flagged | Positioned labels and their diagram relationships need reconstruction. |
| 25 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 26 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 27 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 28 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 29 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 30 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 31 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 32 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 33 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 34 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 35 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 36 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 37 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 38 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 39 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 40 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 41 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 42 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 43 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 44 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 45 | materially worse; flagged | Source reveal/mask sequence is unresolved; static PDF is insufficient. |
| 46 | roughly equivalent | Existing theend layout preserves the authored closer and native star. |

## LECT08D findings

| Source slide | Comparison | Finding |
| --- | --- | --- |
| 1 | improved | Standard title layout; same topic, canonical chapter and current lecture metadata. |
| 2 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 3 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 4 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 5 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 6 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 7 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 8 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 9 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 10 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 11 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 12 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 13 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 14 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 15 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 16 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 17 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 18 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 19 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 20 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 21 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 22 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 23 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 24 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 25 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 26 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 27 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 28 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 29 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 30 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 31 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 32 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 33 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 34 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 35 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 36 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 37 | materially worse; flagged | Source grid lost its row/column relationships. |
| 38 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 39 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 40 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 41 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 42 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 43 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 44 | roughly equivalent | Existing theend layout preserves the authored closer and native star. |

## LECT08E findings

| Source slide | Comparison | Finding |
| --- | --- | --- |
| 1 | improved | Standard title layout; same topic, canonical chapter and current lecture metadata. |
| 2 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 3 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 4 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 5 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 6 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 7 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 8 | materially worse; flagged | Source grid lost its row/column relationships. |
| 9 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 10 | materially worse; flagged | Source grid lost its row/column relationships. |
| 11 | improved | Editable native table preserves source numbers, blanks, incremental completion and total. |
| 12 | improved | Editable native table preserves source numbers, blanks, incremental completion and total. |
| 13 | improved | Editable native table preserves source numbers, blanks, incremental completion and total. |
| 14 | improved | Editable native table preserves source numbers, blanks, incremental completion and total. |
| 15 | improved | Editable native table preserves source numbers, blanks, incremental completion and total. |
| 16 | improved | Editable native table preserves source numbers, blanks, incremental completion and total. |
| 17 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 18 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 19 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 20 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 21 | improved | Editable native table preserves source numbers, blanks, incremental completion and total. |
| 22 | materially worse; flagged | Positioned labels and their diagram relationships need reconstruction. |
| 23 | improved | Editable native table preserves source numbers, blanks, incremental completion and total. |
| 24 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 25 | roughly equivalent | Existing theend layout preserves the authored closer and native star. |

## LECT08F findings

| Source slide | Comparison | Finding |
| --- | --- | --- |
| 1 | improved | Standard title layout; same topic, canonical chapter and current lecture metadata. |
| 2 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 3 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 4 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 5 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. Figures are smaller; inspect at presentation scale. |
| 6 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 7 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 8 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 9 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 10 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 11 | roughly equivalent | Comparison resolves importer warning; teaching content survives without the legacy decoration. |
| 12 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 13 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 14 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 15 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 16 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 17 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 18 | materially worse; flagged | Source grid lost its row/column relationships. |
| 19 | materially worse; flagged | Source grid lost its row/column relationships. |
| 20 | materially worse; flagged | Source reveal/mask sequence is unresolved; static PDF is insufficient. |
| 21 | materially worse; flagged | Source grid lost its row/column relationships. |
| 22 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 23 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 24 | materially worse; flagged | Source grid lost its row/column relationships. |
| 25 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 26 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 27 | roughly equivalent | Existing two-over-one layout; source answer restored as an on-click appear reveal. |
| 28 | roughly equivalent | Existing two-over-one layout; source answer restored as an on-click appear reveal. |
| 29 | roughly equivalent | Existing two-over-one layout; source answer restored as an on-click appear reveal. |
| 30 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 31 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 32 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 33 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 34 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 35 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 36 | roughly equivalent | Source text/image sequence and meaningful emphasis retained in an existing layout. |
| 37 | materially worse; flagged | Column mask is missing; the censored gene remains visible. |
| 38 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 39 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 40 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 41 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 42 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 43 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 44 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 45 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 46 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 47 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 48 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 49 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 50 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 51 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 52 | materially worse; flagged | Source shapes, highlights, masks, or connected geometry are not faithfully represented. |
| 53 | materially worse; flagged | Source reveal/mask sequence is unresolved; static PDF is insufficient. |
| 54 | roughly equivalent | Existing theend layout preserves the authored closer and native star. |
