# TODO

Extended-Djot is the repository's sole authored deck source. [slide-specs/DJOT_SLIDE_SYNTAX.md](slide-specs/DJOT_SLIDE_SYNTAX.md)
defines its current authoring contract; [PIPELINE.md](PIPELINE.md) records the source-to-native
boundary.

- [ ] add a today is "national ice cream day" slide before the ice breaker, we will need a possible day for all 366
calendar days to pull from ideally with an image like I have used for Nov 11 singles day.
- [ ] clear out completed todo items to another file, this TODO file is hard to parse

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
  [wp_a1_animation_fidelity.md](archive/wp_a1_animation_fidelity.md) records the
  earlier OOXML design context.
- [x] Record native ODP package semantics, headless LibreOffice open/save preservation, and
  ODP-derived PDF final-state evidence.
- [ ] Attend and record Impress playback for object and top-level-list reveals.

## Compatibility and future language work

- [ ] Review Biotechnology Lecture 03A policies and links, and revise the dense legacy pages
  identified in [biotech_lecture_03_slide_review.md](active_plans/reports/biotech_lecture_03_slide_review.md).
- [ ] Independently check the Lecture 03C claims identified in
  [lect03c_topic_source_check.md](active_plans/reports/lect03c_topic_source_check.md).
- [ ] Complete the remaining formatter and editor-rule lanes of the strict-Djot compatibility suite.
- [x] Document authoring through [slide-specs/DJOT_SLIDE_SYNTAX.md](slide-specs/DJOT_SLIDE_SYNTAX.md),
  [USAGE.md](USAGE.md), and [COOKBOOK.md](COOKBOOK.md).
- [ ] Add native editable mappings for currently source-located unsupported content only when a
  teaching need and an acceptance path are defined.

## Deferred image investigation

- Automatic border trimming and further image-allocation remedies remain deferred. The audit is
  implemented; [image_area_regression_followup.md](archive/image_area_regression_followup.md)
  preserves its findings and constraints, including the instruction to use existing layouts.

## Deferred gene-tree SVG export

- [ ] Extend the existing Biology Problems Question tree library with the smallest self-contained,
  editable SVG output needed by Djot decks. This is deferred from
  [genetics_visual_renewal_plan.md](active_plans/active/genetics_visual_renewal_plan.md);
  all current gene-tree/phylogeny content, including cross-lecture great-ape examples, is excluded
  from that illustration delivery. Family pedigrees are not part of this deferral.
- Reuse tree models, rotations, taxa labels and topology from
  `~/nsh/PROBLEMS/biology-problems/problems/inheritance-problems/phylogenetic_trees/`.
  Existing question generators are `gene_tree_choice_plus.py` and `gene_tree_matches_plus.py`;
  `treelib/tl_output.py` currently emits HTML-table/ASCII representations, not SVG.
- Preserve current question behavior. Add one standalone SVG export path with editable geometry
  and live text; no separate tree framework. Existing output uses node-rank spacing, not numerical
  evolutionary distances. Do not imply time or distance from that spacing or expand this into
  UPGMA/NJ algorithm work.
- Prove topology/tip-label and rotation preservation on a representative existing tree, then embed
  its SVG in one Djot deck and inspect the actual ODP/PDF. Keep source counts and numerical models
  unchanged. Preserve the current working-tree tree code/art and historical evidence for reuse.
- Suggested implementation owner: the Biology Problems repository, whose existing backlog is
  `~/nsh/PROBLEMS/biology-problems/docs/TODO.md`; Djot integration proof belongs here. That external
  backlog has not been edited by this task.

## Stable exclusions

- [x] Keep Biotechnology source folders inside their lecture folders and delete obsolete duplicates.
- [x] Keep copyrighted assets local and ignored while validating their real paths with Djot lint.
- [x] Split large import and measurement modules into cohesive responsibilities.
- [x] Keep one canonical Djot source for each maintained deck.
- [x] Keep slide geometry in the layout registry rather than infer it from source order or images.
- [x] Keep source-only lint separate from native E2E and attended visual checks.
- [x] Use explicit layout directives and native Djot blocks for normal slide structure.
- [x] Keep permanent pytest fast, deterministic, offline, and behavior-focused; record corpus,
  rendering, and attended Office checks as one-time acceptance evidence.
