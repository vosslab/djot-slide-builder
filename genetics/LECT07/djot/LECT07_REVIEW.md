# Lecture 07 source fidelity revision

This review supersedes the earlier conversion report. The revision uses the repository
`deck_tools.py import` and `deck_tools.py build` commands. Original ODP/PDF files remain
unchanged one directory above. The source import reports are retained under
`assets/source_fidelity/`. No new converter or math renderer was added.

## Scope and sequence

All five Genetics LECT07 decks were compared with their original sources. The four teaching
decks now retain source slide order. Removed conversion-authored objectives, closing summaries,
prompts, slogans, new explanatory prose, and split reference slides. Original presenter notes
are restored. Each slide records its source slide number in notes.

| Deck | Authored | Visible | Review markers |
| --- | ---: | ---: | ---: |
| lect07a-2026_announcements | 36 | 25 | 0 |
| lect07a2-genetic_probability | 8 | 8 | 3 |
| lect07b-prob_of_progeny | 51 | 51 | 13 |
| lect07c-prob_of_progeny_2 | 38 | 38 | 1 |
| lect07d-chi_square | 60 | 57 | 13 |

The instructor subsequently approved splitting D source slides 3 and 4 into four slides,
with scientific corrections that preserve his voice. Later D slide positions shift by two;
source slide numbers in notes and the historical review references below remain unchanged.

## LECT07C second layout pass

Compared all 38 source PDF pages with the rebuilt deck. Restored 35 formula previews
through the existing GDI converter after fixing detection of extensionless SVM members.
Restored the single Punnett-square progression and lethal-TT crosses on slides 4-6.
Used dedicated panels and source-derived vector equation groups for the probability
tables, three-sex derivation, and dihybrid calculations. Wording and slide sequence remain
source-based. Formula SVGs preserve typesetting; ordinary slide text remains native.

Cleared 19 of the previous 20 review markers after rendered comparison. Slide 8 retains
its marker: its six calculations are complete, but the figure remains too small for
confident classroom acceptance. Comparison renders are under `_temp/lect07c-layout/`.
The historical notes below describe the earlier pass, not the current C equation recovery.

A2 retains the requested universal cover before its seven original slides. Announcements
retain the requested podcast slide and current dates, schedule colors, public/private links,
YouTube wording, and evergreen Discord information. B, C, and D map one-to-one to the 51, 38,
and 58 source slides respectively. Native factorial and progressive chi-square tables remain.
The approved multiple-choice answers, emphasis, and seven-child separation remain.

## Remaining representation gaps

`@replaceme` means unresolved source representation, not a completed slide. The importer
identifies missing native equations, unsupported annotations/animations, and layouts needing
review. Reasons and source slide references are in notes. Existing source pictures remain
pictures; they are not described as editable native equations. The former plain-text equation
rewrites do not count as faithful mathematical rendering.

- lect07a2-genetic_probability: authored slides 2, 5, 8.
- lect07b-prob_of_progeny: authored slides 9, 17, 19, 20, 23, 26, 31, 36, 37, 43, 44, 45, 46.
- lect07c-prob_of_progeny_2: authored slides 4, 5, 6, 7, 8, 9, 10, 14, 18, 19, 20, 21, 22, 23, 24, 27, 28, 32, 33, 34.
- lect07d-chi_square: authored slides 16, 17, 18, 20, 23, 24, 25, 26, 27, 28, 29, 38, 56.

## Source issues kept separate

This is a fidelity revision, not permission to rewrite the teaching material. Source claims
about pea pod versus seed color, accepting the null hypothesis, and the fruit-fly p-value
need instructor review. They have not been silently replaced with new explanations.

## Verification

- All sources parse; the universal cover/parser/include check passes (150 tests).
- All 61 initially flagged pages were compared side by side against original PDFs;
  original ODP XML was also checked for unsupported empty-frame warnings.
- Eight markers cleared: A2 3, 4; B 22, 30; C 17; D 22, 32, 50.
- Remaining 49 markers are intentional. A2 animation behavior remains unresolved;
  B/C primarily lose native equations and some correction annotations. C4-6 duplicate
  the Punnett square and C5-6 lose the lethal-genotype cross. D23-26/28-29 have
  unreadably small image rows; D16/20/27/38/56 lose table annotations. D3/4/53/54
  were subsequently accepted by the instructor and cleared after H subscript 0 repair.
- B9 now strikes through the source incorrect calculation; its animation flag remains.
- Original/rebuilt comparison images are in _temp/lect07-review/.
- Unresolved review markers prevent a claim that every slide is classroom-ready.

### Final output checks

All five decks rebuilt through `build_slides.sh` outside the sandbox. The eight cleared
pages were inspected again after rebuilding. The announcements homework page restores
its source two-column organization and original schedule guidance. The YouTube channel
page uses big-image with a single-line caption and visible channel URL; a stacked-panels
comparison was inspected and retained in the temporary review folder. Biotech remains
unchanged. Titleless one-panel bodies now reclaim the top margin, with focused layout
coverage protecting expansion and absence of a title slot.
