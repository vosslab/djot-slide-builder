# TODO

Extended-Djot is the repository's sole authored deck source. [slide-specs/DJOT_SLIDE_SYNTAX.md](slide-specs/DJOT_SLIDE_SYNTAX.md)
defines its current authoring contract; [PIPELINE.md](PIPELINE.md) records the source-to-native
boundary. Completed work is recorded in
[archive/DONE_TODO.md](archive/DONE_TODO.md).

- [ ] Add a "Today is National Ice Cream Day" slide before the icebreaker. Cover all 366
  calendar days, ideally with an image like the November 11 Singles Day slide.

## Playback verification

- [ ] Attend and record Impress playback for object and top-level-list reveals.

## Compatibility and future language work

- [ ] Review Biotechnology Lecture 03A policies and links, and revise the dense legacy pages
  identified in [biotech_lecture_03_slide_review.md](active_plans/reports/biotech_lecture_03_slide_review.md).
- [ ] Independently check the Lecture 03C claims identified in
  [lect03c_topic_source_check.md](active_plans/reports/lect03c_topic_source_check.md).
- [ ] Complete the remaining formatter and editor-rule lanes of the strict-Djot compatibility suite.
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
  the separate cross-lecture great-ape examples remain excluded from that illustration delivery.
  The Lecture 11 refresh supplies its own fixed teaching examples; it does not implement this API. Family pedigrees are not part of this deferral.
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
