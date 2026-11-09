# Curated slide exemplars progress

Tracks the approved [curated slide exemplars plan](curated_slide_exemplars_plan.md). Curator
handoffs, readability fixes, final artifact checks, and independent specification, quality, and
visual reviews are complete. Independent INTEGRATION ACCEPT closes the approved implementation.
See [curated_slide_exemplars_results.md](curated_slide_exemplars_results.md) for delivery and limits.

## Work status

| Task | Owner | Status | Evidence or next action |
| --- | --- | --- | --- |
| Root-folder correction | `/root/flatten_exemplar_folder` | Complete; SPEC, QUALITY, and INTEGRATION ACCEPT | User-directed `exemplars/` layout; maintained teaching/authoring showcase, not fixture data. Exact `./build_slides.sh exemplars` passed (8 decks, 16 outputs, 44.7 seconds); current counts are 82 ODP/81 PDF, with 68/67 curated and 14/14 table-styles outputs. Path/hash checks confirm 87 source/media/previews and 138 unrelated outputs unchanged; 16 rebuilt artifacts intentionally changed. Evidence: `_temp/exemplars/relocation/REPORT.md`, `build.log`, `build_report.md`, and `direct_evidence.json`.
| C1: Orientation and text | `/root/exemplar_foundations` | Handoff complete | Decks 01-02: 19 authored slides; source-preservation and structural checks passed. Handoff: `_temp/exemplars/foundations/handoff.json`. |
| C2: Figures and data | `/root/exemplar_visuals_data` | Handoff complete | Decks 03-04: 20 slides; strict lint and capacity checks passed; 11 image uses. Original-source ownership and construction checked. Handoff: `_temp/exemplars/visuals_data/handoff.json`. |
| C3: Worked examples and questions | `/root/exemplar_reasoning_sequences` | Handoff complete | Decks 05-06: 19 slides; strict lint, native capacity, arithmetic and source-preservation checks passed. D9 compacts a redundant phenotype column while preserving all eight genotype/count relations and setup definitions. Handoff: `_temp/exemplars/reasoning_sequences/handoff.json`. |
| C4: Logistics and study support | `/root/exemplar_logistics` | Handoff complete | Deck 07: 10 authored slides, one hidden; two owned SVGs and historical context documented. Handoff: `_temp/exemplars/logistics/handoff.json`. |
| D: Index and discovery docs | `/root/exemplar_index_docs` | Complete | Index covers all 68 examples and credits all 11 local artwork copies; README, authoring guide and changelog are updated. Colors, popup wording, notes references, links, ASCII, and hashes were reconciled after repairs. Report: `_temp/exemplars/docs/REPORT.md`. |
| V: Build and rendered review | `/root/exemplar_build_verify` | Final verification complete | Current manifest records seven ODP/PDF pairs and 68 previews; all seven decks compile after relocation. Current manifest SHA-256: `220e1beb9449887ac04c40d200e0db037870e10298d93ebe6875a90faa7d79c5`. Report: `_temp/exemplars/verification/REPORT.md`. |
| Readability fixes | `/root/exemplar_readability_fixes` | Complete | D10 repairs copied text contrast while preserving hue and semantic fills; D11 shortens deck 06 slide 2 feedback and clarifies deck 03 notes. Handoff: `_temp/exemplars/readability_fixes/handoff.json`. |
| Visual polish | `/root/exemplar_visual_polish` | Complete | Applied the approved two-page corrections to deck 03 slide 5 and deck 05 slide 7. Current manifest and polish evidence are under `_temp/exemplars/visual_polish/`. |
| Initial specification review | `/root/exemplar_spec_review` | SPEC ACCEPT | Initial review found no open specification gaps or architectural drift. Report: [curated_slide_exemplars_spec_review_2026-11-09.md](curated_slide_exemplars_spec_review_2026-11-09.md). |
| Initial quality review | `/root/exemplar_quality_review` | QUALITY ACCEPT | Initial review found no actionable quality findings or architectural drift. Report: [curated_slide_exemplars_quality_review_2026-11-09.md](curated_slide_exemplars_quality_review_2026-11-09.md). |
| Initial image evaluation | `/root/exemplar_image_evaluation` | Two material concerns | The all-68-page report flags deck 03 slide 5 figure scale and deck 05 slide 7 equation prominence. Its distribution (59 generally strong, 7 contextual review, 2 advisory attention) applies to the initial review only. Report: [curated_slide_exemplars_visual_evaluation_2026-11-09.md](curated_slide_exemplars_visual_evaluation_2026-11-09.md). |
| Fresh specification re-review | `/root/exemplar_polish_spec_recheck` | SPEC ACCEPT | No remaining specification gaps or plan drift in the two-page correction. Report: [curated_slide_exemplars_polish_spec_review_2026-11-09.md](curated_slide_exemplars_polish_spec_review_2026-11-09.md). |
| Fresh quality re-review | `/root/exemplar_polish_quality_recheck` | QUALITY ACCEPT | No actionable quality issues or drift from the approved plan. Report: [curated_slide_exemplars_polish_quality_review_2026-11-09.md](curated_slide_exemplars_polish_quality_review_2026-11-09.md). |
| Fresh visual recheck | `/root/exemplar_image_recheck` | Both concerns resolved | Deck 03 slide 5 scored 19/20 and deck 05 slide 7 scored 20/20; no further fix recommended. These scores cover only the two corrected pages, not all 68. Report: [curated_slide_exemplars_polish_visual_recheck_2026-11-09.md](curated_slide_exemplars_polish_visual_recheck_2026-11-09.md). |
| Final integration review | `/root/exemplar_final_integration` | INTEGRATION ACCEPT | No remaining actionable integration findings or architectural drift. Actual review saved before completion was recorded: [curated_slide_exemplars_integration_review_2026-11-09.md](curated_slide_exemplars_integration_review_2026-11-09.md). |

## Baseline evidence

The paths recorded in the saved independent reports and pre-relocation `_temp` evidence refer to the
original `examples/exemplars/` layout and predate the user-directed move. Their review statements
and hashes remain historical.

- 68 authored slides across seven curated decks; 67 normal PDF pages because deck 07 slide 9 is hidden.
  Seven normal ODP/PDF pairs built. Deck 07's hidden slide was separately exported for review.
- Strict native lint passed for all seven decks, with 14 component image uses. All local artwork
  copies are regular files; packaged SVG bytes match the source files. Relocated copies of all
  decks and assets compiled successfully.
- Source, compiled and ODP visibility counts agree. All 67 normal PDF pages and the hidden slide
  were rendered to 90-quality WebP previews and individually inspected. Native MC/popup structure
  was inspected statically; click playback was not tested.
- Focused arithmetic and workspace geometry checks passed. The four curator handoffs report source
  preservation; original courses and `exemplars/table_styles.djot` remain unchanged.
- The baseline render exposed one material clipping defect: deck 06 slide 2's feedback popup
  crosses the page edge. Contrast measurement found four label pairs below 3:1: deck 03 `#00FF33`
  on white (2.929:1); deck 04 `#D40000` on `#FF8F8F` (2.521:1), `#003FFF` on `#8FABFF`
  (2.991:1), and `#A719DB` on `#DC9AF4` (2.621:1). These drive D10-D11; no final visual
  approval is implied by the baseline review.
- Detailed logs, manifests, renders and the baseline copy are under `_temp/exemplars/verification/`.

## Final verification evidence

- The current manifest SHA-256 is `220e1beb9449887ac04c40d200e0db037870e10298d93ebe6875a90faa7d79c5`.
  Source, ODP and PDF visibility counts agree: 68 authored slides and 67 normal PDF pages, with
  authored slide 07:9 hidden. All 68 previews are present.
- All seven decks compile after relocation; all local artwork is contained in the collection.
  Eleven SVGs have positive construction provenance: nine byte-identical copies and two Microbes
  copies with documented text-fill adaptations. Original course files and `table_styles.djot` were
  checked for changes; this is not a global ignored-asset baseline.
- Current contrast checks cover 1,526 native text runs and 112 SVG text leaves, with zero contrast failures.
  Minimum measured contrast is 5.502686323:1 against the 5.5 target. Nine copied SVGs retain exact
  bytes; the two Microbes copies differ only in three documented text-fill attributes.
- The captured latest base-suite run collected 4,512 tests: 4,400 passed, 3 failed, 109 errors,
  0 skipped, and 2 warnings in 20.16 seconds. The failures and errors come from inherited Biotechnology
  LECT10 parse/link conflicts; no exemplar source is named. This is not a full-suite pass. Details:
  `_temp/exemplars/final_checks/REPORT.md`. The earlier pre-polish run
  reported 4,506 collected, 4,394 passed, and the same failure/error counts.
- Documentation checks passed 827 cases with one upstream warning. Full-page review reopened all
  48 rebuilt preview states; the repaired popup is contained. Native animation structure does not
  establish attended click playback.

## Decisions

- **D1-D4 - Scope confirmed:** Curators preserve content and course identity in lightly polished
  copies; the seven purpose decks target about 50-70 slides in total; asset ownership and
  provenance are checked; originals and `exemplars/table_styles.djot` stay unchanged.
- **D5 - Mixed-source C1 pair:** Genetics and Biotech examples may share a deck when scientific
  meaning is preserved; the theme follows the cohesive deck.
- **D6 - Exact filenames:** All four curators used the plan's exact long filenames.
- **D7 - Optional C2 diagram treatment:** Not used. Existing image-comparison and native
  multiple-choice examples provide the selected coverage without adding that treatment.
- **D8 - Notes and provenance:** Teaching cues stay in `@notes`; source and asset provenance and
  design rationale stay in the index.
- **D9 - Compact genetics table:** Approved and applied in C3; all eight genotype/count relations
  and setup definitions remain.
- **D10 - Contrast repair:** Applied. Preserve the deck's color meaning while making actual
  foreground/background pairs readable; keep the source palette unchanged.
- **D11 - Popup repair:** Applied. Shorten deck 06 slide 2 popup text to fit while preserving its
  meaning; clarify deck 03 notes references that do not appear in the sample.
- **D12 - Visual polish:** Applied to the two initial material findings. On deck 03 slide 5,
  shorten native captions and enlarge owned figures to 1.80x height. On deck 05 slide 7, keep the
  equation and explanation together at full width and enlarge the formula to 1.40x height. The
  fresh visual recheck reports both concerns resolved.

## Handoff sequence

Curator source handoffs, D10-D12, index work, build/render verification, and the initial and fresh
specification, quality, and visual reviews are recorded. D12 applies the approved corrections to
deck 03 slide 5 and deck 05 slide 7; the fresh visual recheck resolves both initial material
findings within its two-page scope. The original all-68 score distribution remains historical and
is not a post-polish all-page score. The independent final integration review accepts the current
collection, with 137 manifest/package checks, 100 polish hash checks, 72 unaffected hash checks,
20 pixel-identical page comparisons, seven relocation checks and all 68 index entries verified.
Its actual report and transcript provenance were saved and read back before this completion status
was recorded. Implementation, verification and required reviews are complete; no human approval,
merge authorization, publication or live classroom outcome is asserted.
