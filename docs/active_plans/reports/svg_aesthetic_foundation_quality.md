# SVG foundation quality review

**Verdict: FAIL for the reviewed candidate set, with one required M3 correction.**
M1, M2, M11 and M12 pass this scoped source and SVG-render review. The diagrams and
plots show a useful visible upgrade. The large composed cell still has an excessively
heavy outer contour. A fixed 3-unit cap is sufficient; no redesign or style framework is
needed. The manager accepted that correction during this review. Its implementation and
regenerated artifacts require the separate fresh re-review.

## Required correction

The reviewed `composition/gallery/organelles.drawn.svg` uses a 6.8-unit contour for its
440 by 340 composed cell, while small internal organelles use approximately 1-unit lines.
The border dominates the cell and makes the contents look insubstantial. This is visible
in the complete 1200-pixel gallery image, not just in a magnified detail.

The cause is the uncapped `0.02 * min(width, height)` in
[svg_tools/_style.py](../../../svg_tools/_style.py), used by the cell envelope in
[svg_tools/examples/organelles.py](../../../svg_tools/examples/organelles.py).
Cap the shared outer contour at 3 drawing units while retaining the proportional behavior
for smaller parts. Keep the existing baked geometry, colors, anchors and internal anatomy.
Re-render the composed cell and representative large/small users of the helper. Update the
helper explanation and extend its existing focused check; a new test framework is unnecessary.

A scratch-only comparison changed stroke widths above 3 to 3 in the same composed SVG.
It produces a clearer hierarchy: the cell remains enclosed, while the nucleus and internal
structures receive appropriate attention. This is direct evidence for the cap rather than
an arbitrary style threshold. The comparison also capped three 3.3-unit strokes, so it is
a controlled visual diagnostic rather than an exact simulation of the shared helper change.

Evidence under `_temp/svg_aesthetic/foundation_quality/`:

- `organelles_current.webp`: preserved candidate before the cap.
- `organelles_cap3.svg` and `organelles_cap3.webp`: same geometry, capped stroke diagnostic.
- `foundation_before.webp` and `foundation_after.webp`: nine matched foundation examples.
- Individual `*_before_600.webp` and `*_after_600.webp`: fresh SVG renders at 600 pixels wide.

## Accepted scoped results

**M1: baseline and visual contract.** All 51 snapshot hashes match the baseline manifest;
all seven live protected originals match their stored hashes. The guide makes biological
identity, original local geometry, semantic color, editable labels and slide-size inspection
explicit. Source inspection found locally authored contours and no Servier asset ingestion
in the reviewed implementation. Existing Lucide icons remain an explicitly licensed import;
they are not evidence of newly imported biological geometry. This is a source/provenance
check, not a claim that visual similarity can prove independent authorship.

**M2: local state and serialization.** The final writer's local namespace map is a small,
appropriate correction for the demonstrated prefix collisions. It preserves foreign
metadata, comments and literal XLink references without changing ElementTree's registry.
The gallery uses an explicit output argument for curves and plots, and restores its caller's
working directory in `finally`. The scoped implementation earns its complexity; I found no
reason to replace it with a serializer framework or add configuration.

**M3: geometry mechanism.** Baked path dimensions remove anisotropic outline distortion.
The helper is deliberately limited to current normalized paths and independent closed
subpaths. Existing checks exercise closure and transposed aspect ratios. The remaining
failure is composition line weight, addressed above; it does not invalidate the geometry
mechanism.

**M11: diagrams, text and icons.** I inspected current placement, text labels, styled text,
curves, imported composition, icons and annotations at full preview size and in fresh
600-pixel renders beside the original baseline. All are unclipped and understandable.
The imported pattern now recedes behind its label. Styled text wraps into three balanced
lines instead of leaving a solitary last word. Aligned sequence rows demonstrate the mono
font. Bold branch labels improve annotation reading order while preserving arrow and
inhibition meanings. Placement and curve geometry remain clear without unnecessary redraw.
The icon and diagram contours need not be forced to identical numerical weights; their
different optical roles are intentional and coherent.

**M12: plots.** The four-chart gallery improves materially beyond recoloring: line markers
show observations, error-bar caps expose uncertainty, open frames reduce clutter, and title
weight creates a clearer reading order. Both allele series remain identifiable by shape
and color, including their common point. The genome plot has readable category and value
labels, an explicit approximate intron value, and a clear percentage axis. Its source data
remain 1.5, 5, 20, 15, 44 and 14; their 99.5 total is not normalized. Full previews and the
600-pixel plot renders show no clipped labels, collisions or hidden data marks. A four-panel
gallery still needs a substantial slide footprint; the tiny index thumbnail is navigation,
not a teaching-sized chart.

## Verification and limits

Fresh focused command:

```sh
PYTHONPATH="$PWD:$PWD/tests" MPLCONFIGDIR="$PWD/_temp/mplconfig" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest --basetemp="$PWD/_temp/svg_aesthetic/foundation_quality/pytest" -q tests/test_svg_import.py tests/test_svg_drawing.py tests/test_svg_gallery_state.py tests/test_svg_style.py tests/test_svg_plots.py
```

Result: **30 passed in 1.49 seconds**. The cap owner changed the source during this run;
the result includes the updated helper check, but it does not establish acceptance of its
regenerated composed artwork. Rendering used `rsvg-convert` on white and final review
images use WebP quality 90. An initial rendering command used `.drawn.svg` for plot files;
the corrected command selected their actual `.plot.svg` names and completed successfully.

I read the visual guide, active plan, foundation re-specification, namespace correction,
diagram and plot reports, and relevant implementation/tests. Current biological candidate
images informed only the shared stroke finding. Their anatomy, contact corrections, and
trial biology are explicitly outside this acceptance. The new-signaling trial was inspected
for broad typography and spacing only; its biological review remains separate.

No production source was changed by this reviewer. No Git commands, `source_me.sh`,
LibreOffice, full-suite run, or native slide review was performed. Final classroom-scale
readability and native import/export remain pending with their assigned owners.
