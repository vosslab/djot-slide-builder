# Mixed text and image scaling

Status: implemented and verified on 2026-10-26. The approach below records the original plan;
the settled bounds and outcomes are in [the review](../reports/mixed_content_scaling_review.md)
and [design decisions](../../DESIGN_DECISIONS.md#mixed-text-and-image-area-optimization).

## Goal and evidence

Replace the shared mixed-flow rule that maximizes font size while allowing images to
collapse. Preserve authored prose, source order, image aspect ratios, and existing layouts.
Use 0.5 pt font candidates and let every image scale independently.

Current ownership: `layout_builders._select_mixed_flow_allocation` selects the font;
`layout_measurement.mixed_flow_allocation` measures text and divides the remaining height.
The latter currently forces a common image scale. Picture projection already preserves
aspect ratio and must continue using the same measured allocation during export.

Measured evidence in `_temp/flow_sizing/`: doubling slide 25's text produces a 2.3%-width
image without a capacity warning. For one-panel slide 24, independent scale-sum optimization
selects 23 pt with PNG 100% and SVG 97.9%, occupying 95.0% of panel bounding-box area.
Max-min selects 25 pt and 89.0% image widths, occupying 87.3%. Neither proves a universal
quality metric or that the sum gives the greatest possible occupied area.

## Proposed approach

1. **Establish one shared optimization contract.** For each font candidate, measure text once
   at the panel width; reserve text height, existing clearance, and existing gaps. Each image
   has its own scale between a readability bound and 100% of panel width. Use the exact
   displayed rectangles, not full-width allocation rectangles, to calculate image area.
   Retain the existing body-font readability floor. Failure to satisfy readability requires
   `@replaceme` with a recommendation to split the slide.

2. **Resolve the image-readability constraint with a bounded experiment before implementation.**
   Compare slide 24, slide 25, the demonstrated long-text failure, and existing mixed-flow
   examples with tall, wide, and multiple images. Compare occupied-area, scale-sum, and
   max-min winners. Include a case where unconstrained area maximization sacrifices an image.
   Recommend occupied-area maximization subject to readability constraints, rather than
   area alone. Select and document the smallest defensible common image constraint from
   those renders; distinguish mathematical nonzero size from readable teaching content.
   A width percentage alone does not establish readability of embedded labels. If no common
   constraint works across these examples, record that result and resolve the policy before
   changing production selection; do not add lecture-specific rules or claim a solved metric.

3. **Implement the selected policy at the shared owner.** Search font sizes in 0.5 pt steps
   from the theme's ordinary size through its readability floor. For each font, optimize
   independent image sizes under the available-height constraint and established bounds.
   Use occupied area as the objective, then larger font and deterministic source order for
   exact ties. Text-box area is constant within a font candidate but changes between fonts;
   measure and report image area separately so wrapping cannot conceal a regression.
   If nothing meets the readability bounds, classify the slide as requiring `@replaceme`
   and recommend splitting it, naming the offending content and violated bound. Use the
   existing marker syntax and reporting path; a warning alone is not a successful fit.
   Keep recommendations outside teaching prose. Compilation must not silently rewrite
   authored Djot: report the required marker and actionable split recommendation; apply
   the marker during an authorized source-edit/conversion workflow. An already marked
   slide remains a review artifact rather than a readable-layout success.

4. **Keep the search small and verify the actual projection.** For two images, evaluate the
   feasible endpoints at each font: image area is convex along the fixed-height constraint.
   For more images, examine existing deck cardinalities and choose the smallest exact bounded
   allocation method that handles them; verify it against a temporary exhaustive reference.
   Do not introduce an optimizer dependency or dense pixel grid. Reuse the selected allocation
   in object placement and export rather than independently recomputing it.

5. **Validate and document.** Render the comparison set through editable ODP and PDF, inspect
   wrapping and diagram labels, and report font sizes, independent image scales, image area,
   and total bounding-box coverage. Inspect changed mixed-flow slides across representative
   decks. Record the settled policy in design decisions and describe user-visible behavior.
   Changing lecture 24's authored layout remains a separate edit from the compiler fix.

## File scope

- `slide_lib/layout_measurement.py`: measured candidates, independent image allocation, scoring.
- `slide_lib/layout_builders.py`: selection and projection of the chosen allocation.
- Existing capacity-reporting and replacement-marker reporting owners: unreadable content
  requires replacement, with an actionable recommendation to split.
- `tests/test_layout_engine.py`: minimal durable regressions for image starvation, independent
  image allocation, fit/aspect preservation, and deterministic output. Avoid locking in exact
  slide-specific font sizes or scores. Put exploratory enumeration in `tests/_temp/`.
- `_temp/flow_sizing/`: experiments, score curves, rendered comparisons, timing evidence.
- `docs/DESIGN_DECISIONS.md`, `docs/USAGE.md`, `docs/CHANGELOG.md`: settled behavior and evidence.
  No new layout names, author controls, dependencies, or lecture prose changes.

## Completion checks

- The reproduced starvation case receives a readable allocation or is classified as requiring
  `@replaceme` with a recommendation to split. A capacity warning alone does not satisfy this check.
- Independently sized images are permitted; equality may emerge but is never imposed.
- Font selection uses 0.5 pt candidates; source order and image aspect ratios survive export.
- Shared mixed-flow callers are inspected; image-only and text-only behavior stays intact.
- Focused existing layout tests and justified new regressions pass using `source source_me.sh &&
  python3 -m pytest -q tests/test_layout_engine.py tests/test_svg_and_definition_contracts.py`.
- Candidate selection agrees with a temporary exhaustive reference on small bounded cases.
- ODP/PDF comparisons are visually reviewed using repository export scripts outside the sandbox.
  Compare selection time with the current path; text measurement should remain the dominant work.

Implementation followed the instructor's explicit request. The geometric image bound reuses the
theme's existing font-reduction budget relative to each image's solo contain size. Embedded-label
readability remains a visual-review responsibility; no automatic semantic readability claim is made.
