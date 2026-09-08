# TODO

Extended-Djot is the repository's sole authored deck source. The historical language exploration is
recorded in [djot_slide_extension_exploration.md](active_plans/decisions/djot_slide_extension_exploration.md);
the current source-to-native boundary is [PIPELINE.md](PIPELINE.md).

## Completed implementation boundary

- [x] Adopt exact `=== layout: <name>` and `@<slot>` source directives.
- [x] Derive legal layouts and slots from the native layout registry.
- [x] Parse supported Djot blocks and inline content into the presentation-neutral IR.
- [x] Route `.djot` files directly through native export.
- [x] Rename the layout vocabulary to canonical short names without aliases.
- [x] Add `multiple-choice` with required `@question` and `@answer` slots.
- [x] Generate and one-time accept the eight-deck Djot corpus on short layout names, including
  strict validation, bounded-region review, asset integrity, and independent private regeneration.
- [x] Keep `<= blue overlay` recognized and source-located as deferred work.
- [x] Run the native-layout Djot E2E through editable PPTX, ODP, and PDF.

## Verification and evidence

- [x] Complete one-time native acceptance: strict lint, `build_slides.sh genetics`, both explicit native
  E2Es, and eight sequential matching PPTX/ODP/PDF exports with editable text/direct images and the
  Lecture 02e native table.
- [x] Build the bounded OOXML animation model described in
  [wp_a1_animation_fidelity.md](active_plans/reports/wp_a1_animation_fidelity.md).
- [x] Record one-time headless PPTX-to-ODP/package semantics and ODP-derived PDF final-state evidence.
- [ ] Attend and record Impress playback for object and top-level-list reveals.

## Compatibility and future language work

- [ ] Pin the remaining formatter and editor-rule lanes of the strict-Djot compatibility suite.
- [ ] Write a standalone extended-Djot authoring guide when that broader documentation task is
  approved.
- [ ] Add native editable mappings for currently source-located unsupported content only when a
  teaching need and an acceptance path are defined.

## Stable exclusions

- [x] Keep one canonical Djot source for each maintained deck.
- [x] Keep slide geometry in the layout registry rather than infer it from source order or images.
- [x] Keep source-only lint separate from native E2E and attended visual checks.
- [x] Do not use comment-based `_cell` markers, raw HTML, or raw XML for normal slide structure.
- [x] Keep permanent pytest fast, deterministic, offline, and behavior-focused; record corpus,
  rendering, and attended Office checks as one-time acceptance evidence.
