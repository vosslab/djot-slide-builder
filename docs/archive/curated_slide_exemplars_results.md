# Curated slide exemplars results

The approved collection is complete after independent INTEGRATION ACCEPT on November 9, 2026.
Start with [README.md](../../exemplars/README.md), the visual index and authoring entry
point for the seven curated decks at `exemplars/`. The full table-styles demo is the companion
eighth source selected by `./build_slides.sh exemplars`. The approved scope and decisions remain
in [curated_slide_exemplars_plan.md](curated_slide_exemplars_plan.md) and
[curated_slide_exemplars_progress.md](curated_slide_exemplars_progress.md).

## Delivered collection

Historical independent-review evidence and `_temp` manifests use the former `examples/exemplars/`
paths and predate relocation; those saved statements and hashes remain unchanged. The exact
`./build_slides.sh exemplars` relocation build passed (8 decks, 16 outputs, 44.7 seconds). Current
counts are 82 ODP/81 PDF overall, including 68/67 curated outputs and 14/14 table-styles outputs.
Relocation checks found 87 source/media/previews and 138 unrelated output hashes unchanged; the 16
rebuilt artifacts changed as expected. Detailed evidence is under `_temp/exemplars/relocation/`.

Seven short decks preserve course identity across Genetics, Biotechnology and Biostatistics:

| Deck | Teaching purpose | Authored / normal PDF pages |
| --- | --- | --- |
| 01 | Orientation and topic boundaries | 11 / 11 |
| 02 | Text explanations and notation | 8 / 8 |
| 03 | Figures and comparisons | 10 / 10 |
| 04 | Data and stable working tables | 10 / 10 |
| 05 | Equations and worked examples | 12 / 12 |
| 06 | Questions and explanation sequences | 7 / 7 |
| 07 | Logistics and study support | 10 / 9 |

The collection contains 68 authored/ODP pages, 67 normal PDF pages and 68 WebP previews at quality
90. Deck 07 authored slide 9 is hidden; its preview was reviewed through a separate diagnostic
export, while authored slide 10 maps to normal PDF page 9. Seven normal artifact pairs are in
`output/odp/exemplar_*.odp` and `output/pdf/exemplar_*.pdf`.

Eleven owned local SVG copies support 14 image uses. All seven sources compile after relocation,
and all picture dependencies resolve inside the collection. There are no symlinks, external SVG
resources, course-folder includes, private configuration dependencies or live media fetches.
Course paths provide credits only. The repository engine, fonts and shared template remain
required; portability here concerns the sources and their owned picture dependencies.

## Preservation and verification

Positive construction provenance supports all eleven figures. Nine copies match source bytes;
the two Microbes copies differ only in three documented text-fill attributes. Protected tracked
course files have empty diff/status. The `table_styles.djot` preservation check was made before
relocation; its bytes match `_temp/exemplars/relocation/baseline_hashes.json`, and its staged rename
from `examples/` to `exemplars/` is intentional. Curator candidate hashes remain unchanged. No
global pre-task byte baseline exists for every ignored course asset.

Native packages preserve selectable text, tables, notes and links; equations use the documented
MathJax vector-picture exception. Source/compiled/ODP visibility, SVG packaging, links, fonts,
scientific arithmetic and stable workspace geometry pass focused checks. Final contrast evidence
covers 1,526 native text runs and 112 SVG text leaves, with zero failures below 5.5:1 and a minimum
of 5.502686323:1. The earlier readability-stage count of 1,561 native runs is historical.

The final artifact manifest is `_temp/exemplars/verification/manifest.json`, SHA-256
`220e1beb9449887ac04c40d200e0db037870e10298d93ebe6875a90faa7d79c5`.
Detailed native, rendered, relocation and preservation evidence remains in
`_temp/exemplars/verification/REPORT.md`.

## Independent review outcome

Initial independent reviews accepted specification and quality:

- [curated_slide_exemplars_spec_review_2026-11-09.md](curated_slide_exemplars_spec_review_2026-11-09.md)
- [curated_slide_exemplars_quality_review_2026-11-09.md](curated_slide_exemplars_quality_review_2026-11-09.md)
- [curated_slide_exemplars_visual_evaluation_2026-11-09.md](curated_slide_exemplars_visual_evaluation_2026-11-09.md)

The retained all-68-page image evaluation recorded 59 generally strong, seven contextual review
and two advisory-attention pages. Its two material concerns were small figures on deck 03 slide 5
and equation prominence on deck 05 slide 7. Bounded composition corrections enlarged figure height
1.80 times and equation height 1.40 times. Scientific counts, answers and relationships remain
unchanged. All 20 unedited rebuilt PNG pages are pixel-identical; the other five decks and all SVG
bytes remain unchanged.

Fresh reviews accept the corrections and resolve both visual concerns:

- [curated_slide_exemplars_polish_spec_review_2026-11-09.md](curated_slide_exemplars_polish_spec_review_2026-11-09.md)
- [curated_slide_exemplars_polish_quality_review_2026-11-09.md](curated_slide_exemplars_polish_quality_review_2026-11-09.md)
- [curated_slide_exemplars_polish_visual_recheck_2026-11-09.md](curated_slide_exemplars_polish_visual_recheck_2026-11-09.md)

The configured image evaluator scores the two corrected pages 19/20 and 20/20 respectively.
This is a two-page recheck, not a new all-68-page score distribution. Minor contextual suggestions
remain advisory; no required scope work remains. Final independent integration acceptance and its
transcript provenance were saved before recording completion:
[curated_slide_exemplars_integration_review_2026-11-09.md](curated_slide_exemplars_integration_review_2026-11-09.md).
That reviewer independently passed 137 manifest/package checks, 100 current polish hashes,
72 unaffected hashes, 20 pixel comparisons, seven relocation compilations and 68-entry index coverage.

## Test result and limits

The captured final base suite collected 4,512 tests: **4,400 passed, three failed, 109 errors,
zero skipped and two warnings in 20.16 seconds**, exit code 1. All three failures concern preserved
Biotechnology LECT10 contracts/links; all 109 setup errors originate in the duplicate `left` slot
at `biotech/LECT10/djot/set5_cancer.djot:507`. No exemplar source is named in the failures/errors.
The full suite does not pass. The captured evidence is `_temp/exemplars/final_checks/REPORT.md`
and `full_suite.log` in that directory. Earlier pre-polish counts do not describe this final run.

The earlier documentation lane passed 827 cases; final direct checks passed ten new documentation
files. Completion bookkeeping receives its own ASCII, whitespace, link and hash checks under
`_temp/exemplars/closeout/`, without another full-suite or LibreOffice run.

Native animation trees and rendered pages establish static structure and containment, separately
from attended Impress click playback. Live Zoom, classroom outcomes and attended playback were
not tested. Integration acceptance does not assert human approval, merge or publication.
