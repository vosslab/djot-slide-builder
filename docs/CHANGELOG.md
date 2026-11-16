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
