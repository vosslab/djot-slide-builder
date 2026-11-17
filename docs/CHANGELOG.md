## 2026-11-17

### Behavior or Interface Changes

- Unify C03/C36 with C03's banded chromosome-fusion construction. Concatenate the
  ancestral material into one dicentric body, remove internal telomere caps, and
  preserve its full length and bands through centromere inactivation. Retire the
  separate C36 generator and its outdated circle legend; regenerate only prototype artwork.
- Correct shared chromosome surfaces at segment joins: retain each arm's tangent
  instead of rotating the surface along the next arm. Remove C62's tapered wedges,
  smooth the repeated chromosome shapes in C18/C19/C40/C50, and give C66's fused
  arms and centromere one common root. Retain BPQ layers, chromosome identities,
  counts and labels; preserve Drosophila Y material lengths and the C50 micrograph.
- Move C58's "When the centromere..." explanation from the SVG into native Djot
  text. Preserve all diagram geometry and labels, crop the unused paragraph area,
  and retain the separation when regenerating the review prototype.
- Redraw C51/C52 as BPQ deletion maps: textured gray retained material, narrow
  magenta deletion markers, and visible breakpoint edges. C52 uses equal gene slots;
  C51 preserves every original breakpoint and unequal gene spacing, including the
  distinct V and VI deletion lengths. Generate both in the review prototype.
- Keep extended chromatin and early synapsis strands as simple paths; reserve BPQ
  surface polish for condensed chromosomes. Remove redundant surface coordinates
  from curved chromosome bodies while retaining their shading, bands, and outlines.
  Regenerate the chromosome review prototype without changing lecture artwork.
  C11 falls from 72.6 MiB to 5.5 KiB; the 67 review SVGs fall from 337.8 to 57.7 MiB.

## 2026-11-16

### Additions and New Features

- Replace the chromosome corpus prototype illustrations with prototype-owned SVGs built from the
  shared chromosome renderer. The renderer now uses constant-width curved chromatids,
  independently modeled sisters, local banding, compact Barr-body states, and large rectangular
  centromeres. Preserve all original lecture artwork and instructional content.

- Inventory `_temp/` and prepare a compact rescue under `prototype/temp_cleanup/`: 12 browsable
  SVG samples, the unique Biotechnology drawing generator, final evidence receipts, three PDF
  snapshots, and a local-only source/reference archive. Original scratch remains intact pending
  the removal decision; see the rescue index for the keep list and cleanup recommendation.

- Add `prototype/chromosome_review.djot`: one 70-slide corpus collection with 68 current figures
  from 24 Genetics decks across 10 lecture folders. Stable C01-C68 labels, source-slide captions,
  speaker-note prompts, source hashes, and a feedback CSV support instructor critique.

### Behavior or Interface Changes

- Center C18 centromere collars on their chromosome paths by removing obsolete
  manual marker coordinates from the X-linked figure generator and its source data.
- Survey all C01-C68 figures for sister-chromatid clarity using C16 as the reference.
  Correct C17's squat pairs and length drift, separate independent C37 ploidy copies,
  and join confirmed sisters with foreground belts in C56-C59 and C67. Preserve
  single homologs, separated products, and genuinely short chromosomes.
- Redraw C01 with BPQ chromosome bodies, gene letters, and labeled before/after
  comparisons for insertional and reciprocal translocations. Preserve each gene
  block's identity and length while replacing the opaque numbered textbook layout.
- Correct C06's vertical chromosome paths: an extra x coordinate was interpreted as
  another y position, producing long spikes beneath the nuclei.
- Lengthen C07/C08 chromosomes from 62 to 80 units, preserving chromatid thickness,
  replication scale, and centromere label alignment in the review prototype.
- Reproduce BPQ chromosome surface layers with scalable reference proportions: texture,
  sheen, inset highlights/shadows, black outlines, and integrated gray telomeres. Extend the
  same layers around curved centerlines. Foreground centromere belts span paired chromatids.
- Make chromosome thickness per chromatid, including replication; remove the unused decorative
  band-index field from `Segment` and update callers. Correct C03 overpainting, C08 scale,
  C16 cubic shoulders, C20 gene intervals, and C28 belt coverage in the review prototype.
- Correct five LECT08 prototype generator destinations that left the deck pointing to stale
  files. Shared renderer changes are evaluated in prototype outputs; lecture artwork is retained.


- Reserve `exemplars/` for instructor-approved models. Keep corpus collections awaiting critique
  in `prototype/`, with the reviewed PDF and ODP beside their sources.

### Developer Tests and Notes

- Verify 68 original source hashes, 67 replacement provenance rows plus the C04 empirical
  reference, focused shared chromosome tests, Djot lint, and a 70-page native ODP/PDF export.
  Inspect all PDF contact sheets and full-size C32, C55, and C57 pages.

- Verify all 1,496 archived source hashes, ZIP integrity, and all ten regenerated Biotechnology
  drawings. Parse 121 current decks and 2,949 image placements with no scratch input dependencies
  or missing images; match all 519 extracted Biotechnology images to original slide-file members.

- Build the prototype through the native ODP/PDF workflow; verify 70 exported pages, all 68 native
  review labels, unchanged source hashes, and exact embedded image bytes. Inspect rendered pages;
  this is collection validation, not approval of the artwork's style or science.

## 2026-11-15

### Completed

- Complete the all-course chromosome-theme migration: shared v2 rods, open-X sisters,
  source-faithful curves/rings/terminal loci, and reviewed course-specific figures now cover every
  classified active placement. Preserve empirical images and measured maps, baseline source records,
  and LECT13D's semantic composition mapping. Native acceptance covers 26 masters, 234 changed PDF
  pages, and 255 changed placements; focused SVG checks and independent integration pass. See
  [CHROMOSOME_THEME_MIGRATION_REPORT.md](CHROMOSOME_THEME_MIGRATION_REPORT.md).

### Fixes and Maintenance

- Rotate older whole-day history into CHANGELOG-2026-11b/c/d.md with the existing rotation
  helper and explicit repository root; preserve every day block and leave existing archives intact.

## 2026-11-14

### Fixes and Maintenance

- Remove the obsolete Lecture 11 deletion-mechanisms copy left after chromosome topics moved
  to Lecture 12. It duplicated the renumbered Lecture 12 source but referenced moved assets,
  causing `./build_slides.sh genetics/LECT11/` to fail on a missing figure.

- Clear completed items from TODO and roadmap documents into
  [archive/DONE_TODO.md](archive/DONE_TODO.md), retaining open work and current SVG toolkit links.

- Refresh Genetics Lecture 11 gene-tree teaching examples and move chromosome topics to
  Lecture 12. Native exports and independent specification, quality, and integration reviews pass. See [GENETICS_GENE_TREE_REFRESH_REPORT.md](GENETICS_GENE_TREE_REFRESH_REPORT.md).


- Complete the SVG toolkit aesthetic upgrade and document its visual direction and anchor-based
  composition. Code, standalone art, 32 native proof pages and integration passed review; scoped
  cleanup is complete. See [SVG_AESTHETIC_UPGRADE_REPORT.md](SVG_AESTHETIC_UPGRADE_REPORT.md).

- Correct the curve example's temporary output location and remove an uncalled chromosome helper.

### Removals and Deprecations

- Prune duplicate and implementation-specific tests, removing 32 test definitions and two modules.

### Developer Tests and Notes

- Rebuild all five Genetics Lecture 11 decks as ODP/PDF after removing the obsolete source;
  Lecture 11/12 structure and image checks pass. Base suite: 7,926 pass, 76 failures in
  unrelated hygiene checks; automatic text-fixer side effects were verified and undone.

- Complete six audit passes and the retained 476-case test lane. Record remaining coverage gaps
  and limits in [svg_toolkit_post_aesthetic_audit.md](active_plans/audits/svg_toolkit_post_aesthetic_audit.md).
