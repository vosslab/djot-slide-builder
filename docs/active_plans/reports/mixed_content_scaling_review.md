# Mixed-content scaling implementation review

Date: 2026-10-26. Implements [the plan](../active/mixed_content_scaling.md).

## Result

The shared mixed image/text path now searches half-point font sizes above the existing body
floor, independently optimizes displayed image areas, and selects maximum total occupied
bounding-box area. Equal scores favor larger fonts and deterministic source order. Images
retain their aspect ratios. Text-only, image-only, table flow, and named layouts retain their
existing owners and behavior.

The image reduction bound is the theme's body-floor/ordinary-font ratio (20/28), applied to
an image's contain size when alone in the panel. The short-caption tall-image specimen passes:
a panel-width-only floor would incorrectly reject it. The bound prevents the reproduced severe
shrinkage but cannot determine whether embedded labels were readable in the original artwork.
Visual review remains necessary. No OCR, extra layout, author option, or dependency was added.

If the readable bounds cannot fit, the compiler emits the existing replacement watermark,
source-located `@replaceme`/split recommendation, and recommendation in speaker notes. It keeps
a degraded review preview, with independently optimized images and relaxed serializer-derived
reduction bounds. Such a preview is not a successful readable layout. Authored Djot is not
rewritten; source markers are applied during source review/conversion. Already marked slides
receive one watermark. Physically impossible previews fail with a replacement/split diagnostic.

## Measurements and rendering

Temporary evidence: `_temp/flow_sizing/implementation_results.json`, `implementation_build.log`,
`implementation_review.png`, and individual ODP/PDF/PNG specimens in the same directory.

| Specimen | Result |
| --- | --- |
| Slide 24, one-panel trial | 20 pt; PNG 99.7% width; SVG 100% width |
| Slide 24, existing stacked layout | 20.5 pt in top panel; PNG 99.9% of panel width |
| Slide 25 | 23.5 pt; PNG 100% width |
| Slide 25 with doubled text | Replacement watermark; split recommendation |
| Existing LECT07C three-image example | Replacement watermark; split recommendation |
| Existing LECT03C four-image example | Replacement watermark; split recommendation |
| Synthetic tall image and short caption | Fits at 28 pt; no replacement requirement |

These are temporary trial exports. Lecture sources, authored layout choices, source assets,
and published lecture artifacts were not changed by this implementation. The lower font on
slide 24 follows direct area maximization, rather than the earlier scale-sum objective.
The inspected renders retain prose, visibly larger figures on slides 24/25, and explicit review
marking on crowded examples.

Full representative decks compiled: LECT07B (51 slides), LECT07C (38), LECT03C (51),
LECT06C (53), and LECT08E (25). The first four yielded respectively 1, 2, 2, and 1 new mixed
readability diagnostics; LECT08E yielded four total capacity concerns. These are compile checks,
not a visual review of every page. A scan of Genetics/Biotechnology/Biostatistics sources found
mixed cells containing one to four images. Exact vertex enumeration is exponential in image
count, currently small; revisit the method if substantially larger mixed panels are introduced.

Warm median slide-25 compilation on this host was approximately 13.4 ms versus 2.1 ms with
the previous proportional/largest-font selector (ten measured pairs after two warm-up pairs).
The half-point search measures more font candidates than the previous descending fit search;
this is more meaningful than comparing only the objective's arithmetic cost.

## Verification

- `source source_me.sh && python3 -m pytest -q tests`: 1,273 passed.
- Temporary exhaustive integer-grid reference: 400 bounded cases with one to four images;
  objective values matched the vertex optimizer. Exploratory checks stay in `tests/_temp/`.
- Permanent regressions protect independent scaling, aspect/order/fit preservation,
  half-point output, determinism, replacement diagnostics/watermark/notes, marker deduplication,
  and unchanged authored source. The existing title-only topology test excludes the newly
  applicable replacement overlay from its body-object assertions.
- Seven editable ODP/PDF specimens rendered with repository exporters outside the sandbox;
  the contact sheet was visually inspected. Original teaching text remains unchanged.
- `git diff --check` passed.

Unrestricted `pytest` initially collected unrelated projects under `OTHER_REPOS` and failed
on their imports and duplicate module names. Restricting discovery to this repository's
`tests/` directory passes; no unrelated test configuration was changed.
