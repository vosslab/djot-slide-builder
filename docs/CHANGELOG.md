## 2026-11-19

### Additions and New Features

- Expand the [Set 7 bioethics lecture](../biotech/LECT12/djot/SET7_TOPIC_GUIDE.md)
  to 303 slides across 41 topics. Add 14 editable SVG diagrams, slide-level sources,
  and worked comparisons using the 2024 SART IVF data and March 2026 KFF survey.

## 2026-11-18

### Additions and New Features

- Add the November 19 BIOL 480 [Lecture 12 decks](../biotech/LECT12/djot/LECT12_REVIEW.md).
  Update the announcements and Company Vision Report guide, make both project rubrics
  available, and assemble Set #7 Bioethics in Biotechnology in current topic order.
- Add [Biostatistics Lecture 12A](../biostats/LECT12/djot/lect12a-2026_biostats_announcements.djot)
  as one deck for announcements, class plans, and group tutorial work. Groups start from their
  submitted proposals, submit one working activity with Google Doc and Sheet links by Dec 2 at
  11:59 p.m., try another group's activity in class on Dec 9, and submit the revision on Dec 16
  asynchronously. Let each testing group give feedback on Dec 9 through a form or short video.
  Have each group check its own revised tutorial before submitting the final Doc and Sheet.
  Give the Quiz 3 cancellation its own slide in the Quizzes section.
- Add a [ten-slide chromosome deck](../prototype/chromosome_engine_mini2.djot) for reviewing
  chromosome transfers, wheat genomes, crossovers, banding, inversions, and gamete products.
  The renderer's keyword-only `texture=True` controls the decorative pattern. Setting it to
  `False` removes the texture and keeps the sheen.
- Add a [four-slide chromosome deck](../prototype/chromosome_engine_mini.djot) for reviewing
  the Drosophila complements, cis/trans alleles, sister chromatids and Robertsonian fusion.
- Give C18 BPQ-style centromere collars with pale fills and upright chromosome IDs.
  The shared renderer accepts centromere styles for individual chromatids and sister belts.

### Behavior or Interface Changes

- Use the course palette's extra-light center band on subsection dividers, with medium bands
  above and below and centered black text.
- Support a one-line Djot comment at the start of a source file. Add a reminder to include
  evergreen fragments directly and edit them in place. Header comments stay out of exports
  and preserve source line numbers in diagnostics.
- Migrate the 73-slide [chromosome review](../prototype/chromosome_review.djot) to shared chromosome
  models and rendering. Promote seven Mini2 models and generate 68 SVGs for 70 placements. C04
  continues to use the original local course JPEG. Preserve the source images in mixed figures
  and keep the recipes and their frozen source components in the prototype.
- Add `render_sisters()` with gentle mirrored curves for C02, C38, and C67. Use straight sisters
  in C39 to align with the cohesin drawing. Support independently authored sister paths for C57
  and a closed path for the excised ring in C48. Existing explicit-path calls keep their geometry.
- Rename the Djot speaker note directive to `@speaker-notes`. Keep lecture cues in ODP speaker
  notes and move slide development rationale and provenance into `SLIDE_DEVELOPMENT_NOTES.md`
  beside the decks. Document figure-specific choices in Python recipe docstrings.

### Fixes and Maintenance

- Move Stump the Vibe Coder episode slides and quality-90 thumbnails to
  [shared/README.md](../shared/README.md). Announcement masters now pin an explicit shared episode
  include, preserving historical choices while refresh can migrate a legacy inlined managed slide.
- Use the canonical evergreen sources in
  [Genetics 11A announcements](../genetics/LECT11/djot/lect11a-2026_announcements.djot).
  Move shared contact and registration corrections and
  Genetics-specific assessment wording into the owning fragments. Apply Red Dark to the
  shared announcement emphasis so courses using those fragments render the same red.
- Add native explanations for the C24 crossover, C63 example frequencies, and C68 trisomy 21
  outcome. Improve map contrast in C49 and the figure layout in C68. Clarify C59's problem cue.
- Track reviewed image-containing SVGs with the `.image.svg` suffix. Rename the 17 assets
  covered by individual SVG exceptions and update their deck and generator references.
- Label the centromeres in C23 and C61 to track their origin after exchange. Add one
  centromere callout to the C31 reference chromosome.
- Keep C22's crossover curved, with straight terminal runs and shared centromere collars.
- Lengthen the C01 chromosomes and give gene groups distinct extra-light card colors.
  Reserve space beside visible splices and reject cramped cards unless external labels are
  enabled. Validate source material conservation across Mini2 translocation products.
- Scale C63 to estimated Drosophila chromosome lengths and label the centromeres.
  Use fixed palette colors to track X, Y, and chromosome 2 through the exchange.
- Shape the blue C55 homolog like an omega and guide matching loci across the loop and flanks.
- Lengthen the C31 chromosomes and align 25 bands across all four views. Use one neutral gray,
  stain-colored labels, and one opaque band-color strip per chromatid to avoid PDF hairlines.
- Paint consecutive same-color bands as one stroke while retaining their source boundaries.
- Bring C28 sister chromatids together under their shared centromere collars while preserving
  both crossover points.
- Reserve body color between gene cards and centromeres. Refine Mini2 chromosome proportions,
  telomere alignment, inversion curves, staining colors, and C28 gene-label font fallback.
- Share the C22 and C23 crossover SVGs and the four-panel C31 staining comparison between
  both chromosome review decks. Reuse the byte-identical C13 artwork for C21 while keeping
  each slide's citation, and retire the superseded prototype copies and staining recipe.
- Restore numeric character references in the ASCII fixer for SVG and XML so cleanup preserves
  scientific labels and existing XML escapes.
- Guard the shared lxml object model with a pytest that catches `defusedxml` and `xml.etree` imports.
- Prune retired Djot syntax cases, simplify speaker-note fixtures, and wrap Python test lines
  to fit the 120-character ceiling documented in [DEVELOPMENT.md](DEVELOPMENT.md).
- Standardize ODP, SVG recipes, and XML tests on lxml objects with document-local namespaces.
  Store retained vector artwork in SVG files and build both C20 layouts from structured data.
- Record lecture and course color assignments in [REPO_COLOR_PALETTE.md](REPO_COLOR_PALETTE.md),
  with links from the slide guides and existing values for reproduction.
- Use lxml across `svg_tools` for XML construction and safe parsing. Keep local SVG and
  `xlink` namespaces in the writer for LibreOffice. Use the repository bootstrap in the SVG cookbook.
- Lower the X chromosomes in C18 to bring the X and Y centromeres nearly level. Turn the
  Y so that its short arm still faces the proximal X heterochromatin.
- Use fixed palette hues with five shared lightness grades for authored SVG fills.
  Apply them to C18, C20, C29, and C66 with the same Sky blue `#076DAD` on all four.
- Move gene-locus drawing into `svg_tools/chromosome_loci.py` and put slide-writing,
  conversion review, and teaching voice in [HUMAN_SLIDE_GUIDANCE.md](HUMAN_SLIDE_GUIDANCE.md).
- Group matching chromosome texture marks into compound SVG paths. Regenerate C18,
  C20, C29 and C66. The four-slide PDF shrinks by half with pixel-identical figures.
- Pose the C18 Y with its short arm facing the X heterochromatin, as at the rDNA
  pairing region in male metaphase I.
- Move source records and citations out of the chromosome review decks' speaker notes.
  The [figure sources](../prototype/chromosome_review_sources.md) link the original lecture
  inventory and the studies behind C18.
- Leave a visible stretch of chromosome color between an internal gene block and each
  telomere cap. Extend the four C20 homologs past the last locus to show this spacing
  while keeping the cis and trans allele labels inside their chromosomes.
- Draw all 16 C18 chromosomes and the legend with a common centromere size. Lengthen
  the chromosome bodies together so chromosome 4 shows both its collar and its arm.
  Use mitotic chromosome maps for the heterochromatin blocks
  and the unequal arms of the Y in the [chromosome mini deck](../prototype/chromosome_engine_mini.djot).
- Allow rounding at equal material positions when drawing rearranged sisters. Give the C66
  fusion recipe an explicit output directory for independent generation. Document the limits
  of automatic sister placement on deep bends in the [chromosome engine audit](active_plans/audits/chromosome_engine_audit.md).
- Synchronized shared style guides, tests, and repository support files from the starter template.

### Developer Tests and Notes

- Prune one-off test matrices, exact diagram and layout assertions, and obsolete test helpers.
  Use one representative LibreOffice round trip to check editable objects, answer reveals,
  and selectable PDF captions.

## 2026-11-17

- Use actual Q&A slides for Genetics 11B with visible choices and a separate answer popup.
  Keep component diagrams larger when readable text still fits; wrap answer text explicitly.
- Remove the misplaced construction divider from 11C; restore colored merge bands and
  matching original-pair averaging cues in 11D/11E. Use varied distances in the four-gene
  example and center distance-matrix cells throughout LECT11.

### Additions and New Features

- Add a general-purpose linear chromosome model with immutable source intervals,
  source genes, copy-specific centromere activity, and operations for cutting, reversing,
  copying, joining, and making homologs or sisters. The renderer uses numeric pose points
  and a separate color palette to map material along an open spline. It returns composable
  parts with feature anchors and ink bounds. See [CHROMOSOME_ENGINE.md](CHROMOSOME_ENGINE.md).

- Establish [CHROMOSOME_GENE_LABELS.md](CHROMOSOME_GENE_LABELS.md) as the chromosome
  gene-label convention and pipeline. Add one shared source-locus adapter using existing
  Segment data and final chromosome geometry.

### Behavior or Interface Changes

- Publish four prototype review figures on the chromosome engine. C18 draws the XX and XY Drosophila
  complements, C20 shows cis and trans locus ownership in the wide layout, C29 draws
  sisters with one shared belt and the schematic locus A, and C66 joins the long arms
  into one Robertsonian fusion product alongside the short-arm product.

- Draw telomere caps at true ends and centromere collars at active sites in the new
  renderer. Use the shared gene-letter pipeline and supply an external label when the
  body lacks space. Compose the selected branches from engine parts and structured
  Python or JSON data, generating SVG markup through the drawing helpers.

- Give C31 irregular, matching sister-chromatid bands in C36's purple/pale-yellow palette.
  Preserve reversed G/R patterns and pericentromeric C-bands; identify the colors and widths
  as schematic in the prototype's native caption.

- Default SVG canvases to transparency through the shared writer and inherited recipe trees,
  preserving white structures, panels, and definition paint. Remove 40 canvas rectangles from
  the chromosome review and tighten C31/C44-C46 around their visible content. Export vector
  plots with transparent, content-fitted canvases and a small margin.

- Color-code each merge stage in Genetics 11E across headings, selected matrix cells,
  cluster labels, and tree branches, retaining previous stages in the growing trees.

- Route chromosome gene text through measured upright labels with local fit, contrast,
  centered ink and multi-letter allele superscripts. Embed C25/C26/C60/C63 loci while
  preserving chromosome identities, genotypes, source positions and C25's schematic distal
  locus order. Reuse the same helper in the inversion recipes and regenerate the prototype.
- Widen C60/C63's schematic rods for readable internal symbols. Keep C63 strip backgrounds
  transparent and pad their viewports so neighboring components preserve full centromere
  collars. Add two C63 detail views alongside the dense three-column overview.

- Split Genetics 11C into sequence/method concepts and distance-to-tree construction.
  Separate the class and extension activity into their own decks, and renumber C-H
  with distinct titles, objectives, summaries, and updated artifact links.

- Pair Genetics 11B primate questions with on-click answers while preserving diagram size;
  restore a saturated orange tree using the course palette.

- Expand Genetics 11F into a 49-slide explanation of gene choice, substitution rates,
  calibrated clocks, and gene versus species dates. Preserve the original figures, repair
  the Adh map, correct inherited definitions, and add worked steps and speaking notes.

- Give Genetics 11B-F distinct topic-based cover titles and matching canonical
  filenames, including Five Sequences and Weighted Averages for the former More Gene Trees.

- Replace muted brown with saturated palette blue in the original Genetics 11B
  primate tree, preserving its vector geometry, labels, scale, and displayed proportions.

- Use palette Blue #003FFF and Purple #A719DB for Genetics 11B Tree Terms and
  matching branch-point/MRCA references.

- Consolidate all Genetics 11A native reds to #D40000, including reminders and the
  icebreaker, preserving its original typeface and 38.75 pt size.

- Include the second gene-tree handout as the early-finisher extension, add its
  complete UPGMA answers to Genetics 11E, and supply a two-page printable bundle.

- Add subsection dividers at teaching transitions in Genetics 11C/D/E, preserving
  calculation and question/answer sequences and consistent matrix sizes.

- Simplify Genetics 11B wording, add an early Tree Terms slide, clarify MRCA and
  polytomy explanations, and defer UPGMA vocabulary to construction deck 11C.

- Restore the three-rhino sequence-to-UPGMA introduction before the four-sequence
  example in Genetics 11C. Correct one source sequence typo to match its dotted
  representation and original 4/12/8 distances.

- Split Genetics 11B interpretation from new 11C tree construction and four-sequence
  UPGMA. Shift the five-gene example, group activity, and evolutionary time to D/E/F.

- Update Genetics 11A to StVC 39, Red Dead Cell Counter, with its current thumbnail,
  video link, and primary tool link.

- Keep Genetics 11C/11D distance matrices at matching dimensions for each row/column
  count, using fixed 22 pt cell text and equal-width grid/answer borders.

- Restore Genetics 11B's original illustrated conceptual sequence, including Khan
  Academy tree rotations, annotated ancestry diagrams, primate questions, alignments,
  and methods figures. Retain its checked four-sequence example with colored clades.

- Make condensed chromosome centerlines tangent-continuous in the shared renderer, preserving
  already smooth paths such as C28. Align source bands, centromeres, gene regions and crossing
  gutters with the final spine. Smooth C18 and C30, and widen C57's two too-tight approaches.
- Record C28 as an instructor-approved curved-chromosome reference and add the existing four
  white zigzags at its crossover-source boundaries, preserving its geometry and allele products.

- Present LECT11 movie-advisory content ratings in an editable two-column table.

- Apply course-identity colors to shared upcoming-course titles, summary entries, and
  key labels: biochemistry purple, lab red, cellular biology blue, and film dark purple.

- Restore LECT11 movie-score highlighting and add tomato/popcorn ratings. Follow the
  movie overview with an editable IMDb Parents Guide content-advisory slide.

- Restore the original red extension-policy emphasis on LECT11 Illness Policy.

- Mark LECT11 Quiz 4 dark red because it is at the next class meeting; define schedule
  emphasis by next class rather than next calendar week across breaks.

- Format LECT11 anonymous-message instructions as three bullets, retaining the original
  wording, form image, and URL.

- Automatically size visible URLs at 80% of surrounding text, retaining condensed type
  and the 12 pt floor. Put LECT11 syllabus URLs on bullets below plain labels, and outline
  its next-class topics, quiz, and homework status separately.

- Pair each LECT11 syllabus-link label with its complete URL in one bullet. Verify
  condensed PDF fonts, independent URL sizing, and all four clickable destinations.

- Give LECT11 Office Hours compact weekday/time labels and bold green schedule text
  ahead of the room and Zoom details, preserving its illustration and links.

- Group Genetics LECT11 agenda content under Chapter 11 and require chapter/unit
  grouping in the agenda preparation guidance. Focus its lookahead on the next class
  after Thanksgiving break, omitting later December deadlines from that slide. Keep
  homework off the agenda while retaining the moved-quiz status reminder.

- Require the manager to check the whole course semester for icebreaker reuse, including
  reworded repeats. Use a visible REPLACEME prompt and `@replaceme` when freshness cannot
  be established. Replace Genetics LECT11's repeated animal-modification question with
  an animal-roommate movie tie-in.

- Standardize illustration definitions with `_recipe.py` and `_recipes.py`, and asset
  orchestration with `make_`. Move five lecture-owned generators from `devel/` into their
  lectures, updating callers and current documentation while preserving asset destinations.
  Use the shared SVG document and text writers for LECT10B's chromosome-form recipe.
- Replace `lucide-static` with Font Awesome Free for general SVG icons. Read individual solid
  SVG assets during figure generation, retain their attribution comments, and remove the
  stroke-width option and repeated full-license metadata. Update the icon example and guides.
- Standardize chromosome loci around colored gene regions and upright, contrast-aware
  labels. Replace floating recipe labels where the chromosome has room, while retaining
  readable external labels for dense diagrams and whole-chromosome identifiers.
  Rename the shared decorative `bands` switch to `texture`; explicit biological bands,
  ancestry colors and gene intervals remain independent. Remove C01's local text-outline fix.
- Move C13/C21's numbered explanations and C25/C56/C59's bottom prose into native
  Djot text. Split C55 into two SVG panels with native captions; reuse C13's working
  diagram for the duplicate C21, restoring its micrograph and cell backdrop.
- Reduce rendering timestamps to 12 pt IBM Plex Sans Condensed and place them below
  the THE END outline with more clearance. Retain subdued, readable theme colors.
- Stamp slide 1 and the last visible THE END slide with the same local rendering date
  and time on each native build. Use subdued, selectable text on light
  and dark backgrounds; ODP and its exported PDF share the timestamp automatically.
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

### Fixes and Maintenance

- Keep regenerated chromosome SVGs ASCII through character references and retain LF inventory
  line endings, preserving artwork and avoiding serialization-only rebuild differences.
- Replace unsafe XML parsing calls with the existing safe parser while retaining XML builders
  and serialization. Correct annotations, indentation, executable modes, generator entrypoints,
  source character references, and broken documentation links. Align the frozen meiosis-input
  checksum with its newline-terminated JSON without changing the chromosome records.
- Align SVG runtime guidance with the master repository rules: use the Python bootstrap,
  `pyflakes` and focused pytest checks. Keep task briefs positive and specific.
- Correct the C24 prototype destination so the review uses the regenerated locus diagram.

### Removals and Deprecations

- Remove the special `allele_labels` option, superseded raw C25/C26 template labels and
  duplicated LECT13 gene-patch/text construction. Recipes supply locus data to shared tools.

- Prune 73 repository-owned test functions and 10 low-value test modules, removing 1,562 lines
  of artwork snapshots, tuning assertions and duplicate implementation checks. Retain scientific
  geometry, source preservation, native text, XML safety, fonts, atomic output and authoring checks.

### Decisions and Failures

- Two explicit bytecode-compilation commands created eight `.pyc` files despite the
  environment's import-cache suppression. Validation now uses the documented bootstrap,
  `pyflakes` and focused tests; the cache scan is clean.

### Developer Tests and Notes

- Chromosome engine authoring passed a standalone exercise using the public guide.
  The example renders alternate poses, a homolog, a one-pose sister pair, and a
  terminal exchange that conserves 448 units of source material. The 73-slide review
  embeds all four replacements with native titles and captions. The base suite passed
  9,515 checks with two source-line advisories.

- C31 banding: 18 focused chromosome tests and pyflakes pass. Inspect the updated native
  PDF slide 32, verify its SVG is embedded unchanged, and compare all review/source asset
  hashes to confirm that only C31 artwork changed. The base suite was not rerun for this
  recipe-only styling change.

- SVG transparency: 24 focused checks pass. All 70 review SVGs render with transparent
  space, and foreground comparison permits only 40 canvas removals and the four authored
  crops. Preserve all 68 original lecture SVGs, verify all 70 current inputs in the native
  ODP, and inspect C31/C44-C46 in the exported PDF. Base suite: 9,398 passes, with the two
  existing LECT11 fragment-cover and review-document-length failures remaining.

- Gene labeling: 22 focused SVG tests pass. Verify all C25/C26/C60/C63 alleles, C28/C53's
  preserved geometry, unchanged original chromosome lecture outputs, and all 70 current SVG
  inputs embedded in the 73-slide native review. C63's two detail views partition the same
  overview components without changing their content; both pass final native slide inspection.
  Base suite: 9,401 passes and two separate
  LECT11 failures (the unused four-step fragment cover and the overlong review document).

- Chromosome smoothness: 17 focused geometry tests pass. Verify 835 regenerated body
  centerlines, C28's unchanged geometry apart from its new joins, C30's 15 band heights,
  C57's 16 loci, and unchanged original lecture SVGs. Rebuild the 71-slide prototype,
  verify all 68 current SVG inputs are embedded unchanged, and accept 12 native review pages.

- Illustration naming and ownership: 24 source moves, 9,285 passing base-suite tests, and a
  successful prototype rebuild. Check 1,304 SVG hashes and all seven mixed LECT06 outputs;
  preserve original lecture artwork. C35 renders identically after adopting the shared writer
  and passes the focused native ODP/PDF check. Retain the reciprocal-cross SVG's content while
  encoding its symbols as character references. LECT04's PNG conversion was not rerun.
- Font Awesome migration: 9,281 base-suite tests pass; npm reports no known vulnerabilities.
  Export the 18-slide toolkit showcase and inspect its icon page, verifying that the current
  icon SVG is embedded unchanged. The four-icon SVG falls from 15,827 to 4,060 bytes.
- Complete six independent cleanup audit passes: Plan, Test, Style, Docs, Legacy and Comment.
  Regenerate all 68 chromosome review assets with identical output bytes and preserve all 1,040
  original lecture SVGs. Restore C53's heading spaces after source indentation cleanup.
  Keep the ASCII checks active and validation bytecode-free.
- Chromosome labels: 22 focused SVG tests, source-label preservation, continuous-chromatid
  product tracing, SVG references, native slide export and visual review. Original lecture
  SVGs remain unchanged; 71 review slides retain native explanations and the build timestamp.

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
