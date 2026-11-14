# SVG aesthetic upgrade report

The SVG toolkit now has a cohesive family of locally authored semi-flat scientific
illustrations. This report records the 2026-11-14 upgrade and the evidence available at this
completion. Code specification, standalone artwork, native specification, native quality and
integration reviews passed, and scoped cleanup is complete. The current milestone status is
in [svg_aesthetic_progress.md](active_plans/active/svg_aesthetic_progress.md).
The subsequent pruning and six-pass review are recorded in
[svg_toolkit_post_aesthetic_audit.md](active_plans/audits/svg_toolkit_post_aesthetic_audit.md).

See [index.webp](slide-specs/illustration_examples/svg_toolkit/index.webp) for the gallery,
[before_after_details.webp](slide-specs/illustration_examples/svg_toolkit/before_after_details.webp)
for comparisons, [SVG_VISUAL_STYLE.md](SVG_VISUAL_STYLE.md) for the visual contract, and
[native_proof_index.webp](slide-specs/illustration_examples/svg_toolkit_native/native_proof_index.webp)
for the 32 native proof pages. The earlier toolkit delivery and its historical checks are in
[SVG_TOOLKIT_IMPLEMENTATION_REPORT.md](SVG_TOOLKIT_IMPLEMENTATION_REPORT.md).

## What changed

Broad color masses, controlled contours and a few contained tone planes give cells, organelles,
proteins and binding illustrations shallow depth while keeping their teaching features visible.
Membranes, gene tracks, chromosome bands and plots stay direct diagrams. The illustrations are
schematic: organelle fold and sac counts do not represent measurements. The original LECT02
B-DNA illustration and the six original pre-toolkit pilots remain byte-identical; no quantitative
DNA pitch claim was added. This is the scoped toolkit upgrade, not a migration of all repository
SVGs.

The mitochondrial inner membrane now forms connected folds with open lumens; chloroplasts have
flattened thylakoid stacks and connecting lamellae. Membrane insertion leaves a deliberate gap,
protein contact anchors meet their contours, and activity and phosphorylation remain independent.
Antibody binding topology, chromosome bands and locus ordering, phenotype classes, and seed-cross
ratios are preserved. Plot markers, error bars and quieter frames improve reading without changing
the underlying data. Labels remain live SVG text: Atkinson Hyperlegible Next serves ordinary
labels and Mono aligned sequences; the fonts are installed renderer dependencies.

The implementation uses small shared geometry and stroke helpers and locally authored tone planes, preserving existing APIs and
caller colors. The outer stroke scales with the shorter dimension up to a 3-unit cap. Corrections
also contain molecule shading, restore gallery caller state, isolate XML namespace serialization,
and pass the plot output path explicitly so gallery arguments do not redirect the plot recipe.
Servier Medical Art informs the style only: no Servier artwork, tracing or geometry was reused.

## Verification

- The [code re-review](active_plans/reports/svg_aesthetic_code_respec.md) passed after the
  shading correction; 125 focused SVG and Djot-include tests passed. Numerical sampling checked
  tone containment at two aspect ratios; it is not a proof for every possible dimension.
- [Composition evidence](active_plans/reports/svg_aesthetic_composition.md) records 48
  deliverables: 17 gallery SVG/WebP pairs and an index, chromosome v2, six toolkit
  pilots, two trial SVG/WebP pairs, and two before/after comparison images.
  All 26 SVGs parse as ASCII XML with positive viewBoxes. Text-element sequences match baseline
  for the 17 gallery figures, six pilots and two trials; all seven protected originals match their
  baseline hashes. The [regeneration manifest](active_plans/reports/svg_toolkit_regeneration.json)
  records commands and hashes.
- [Standalone art review](active_plans/reports/svg_aesthetic_final_art_quality.md) passed all
  26 illustrations individually at 1200 and 600 pixels, including the corrected large cell contour.
  Dense chromosome, Sxl, organelle and signaling compositions need enough slide area; reduction
  is not a universal Zoom-legibility guarantee.
- The fresh [native rebuild](active_plans/reports/svg_aesthetic_native.md) covers eight ODP/PDF
  pairs and 32 pages: 18 showcase pages, 12 whole-slide excerpts from five consumer decks, and
  two trial pages. Referenced SVG bytes match their ODP embeddings, with SVG MIME entries;
  PDF page counts, extractable sample text, and embedded Atkinson Hyperlegible Next were checked.
  The [native manifest](active_plans/reports/svg_aesthetic_native.json) records proof hashes and
  details, including 59 artifact hashes. [Native specification review](active_plans/reports/svg_aesthetic_native_spec.md)
  independently verified those hashes, 48 regeneration hashes and 28 source-to-ODP matches. These checks do not establish editing of every object or every glyph's font.

The Western excerpts on pages 5 and 7 produced 18.5 pt left-panel capacity warnings against
the 20 pt floor. Some Western and array figure labels are small in their existing contexts.
The [native quality review](active_plans/reports/svg_aesthetic_native_quality.md) passed all
32 pages, and the [integration review](active_plans/reports/svg_aesthetic_integration.md) passed
after [scoped cleanup](active_plans/reports/svg_aesthetic_cleanup.md). Cleanup removed 625 files,
295 directories and 90 symlinks (25,507,074 file bytes), with all guarded hashes unchanged.
Post-cleanup integration verified 103 unique durable hashes, seven protected originals, 26 SVGs
and five consumer source hashes. The complete 351-slide consumer-deck build is historical and
was not rerun; the full base suite, live Zoom display and interactive Impress editing were not
checked in this pass.
