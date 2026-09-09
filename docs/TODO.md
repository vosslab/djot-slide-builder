# TODO

Extended-Djot is the repository's sole authored deck source. [DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md)
defines its current authoring contract; [PIPELINE.md](PIPELINE.md) records the source-to-native
boundary.

## Completed implementation boundary

- [x] Publish one normative syntax reference for the supported Djot presentation surface.
- [x] Route canonical `.djot` source through the native export pipeline.
- [x] Generate and one-time accept the eight-deck Djot corpus on short layout names, including
  strict validation, bounded-region review, asset integrity, and independent private regeneration.
- [x] Run the native-layout Djot E2E through editable ODP and LibreOffice-derived PDF.

## Verification and evidence

- [x] Complete one-time native acceptance, then remove its disposable runners after proof: strict
  lint, `build_slides.sh genetics`, two explicit native E2Es, and eight sequential matching
  ODP/PDF exports with editable text/direct images and the Lecture 02e native table.
- [x] Build the bounded ODF/SMIL reveal model; the dated
  [wp_a1_animation_fidelity.md](active_plans/reports/wp_a1_animation_fidelity.md) records the
  earlier OOXML design context.
- [x] Record native ODP package semantics, headless LibreOffice open/save preservation, and
  ODP-derived PDF final-state evidence.
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
- [x] Use explicit layout directives and native Djot blocks for normal slide structure.
- [x] Keep permanent pytest fast, deterministic, offline, and behavior-focused; record corpus,
  rendering, and attended Office checks as one-time acceptance evidence.
