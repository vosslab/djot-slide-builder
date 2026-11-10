## 2026-11-10

### Additions and New Features

- Add `movie-panel` with editable text on the left and a narrower 2:3 poster slot on the right.
  Import the four supplied movie choices into Genetics 10A with their ODP wording and original
  posters, followed by a vote recap showing all titles/posters. Reuse the existing layout compiler
  and image containment; add one layout-contract regression and extend the existing native-layout
  acceptance specimen. Keep movie-specific import and rendered verification temporary.
  All 5,880 base tests pass; source/export checks preserve the four ODP text sets and poster bytes.
  Visually review the movie/vote pages and their surrounding 10A context. The complete descriptions
  fit at 15.5-16.75 pt, below the ordinary body target.

- Review Genetics Lecture 10's visible text for the instructor's voice, short teaching phrases,
  and meaningful color. Inspect 112 text-rich or changed pages; revise wording or emphasis on
  96 pages while preserving problem assumptions, all eight answers/reveals, and figure references.
  Rebuild all four decks and check the exports. Improve the newborn reference table's widths
  and announcement text fit; keep lecture-specific verification temporary.

- Improve Genetics 10D slide 26 readability with a shorter meiosis-II question and parallel
  choices stated as counts out of four gametes. The existing layout now fits four full-width,
  single-line choices at 28 pt above the answer reveal. Rebuild and visually verify the PDF;
  keep this slide-specific check temporary.

- Distinguish the sparingly used `question-ask` card from the icebreaker `prompt` layout.
  Put one editable centered question in the reference's ultra light hexagon with dark corners;
  keep icebreaker prompts and required examples on a pale rounded card. Apply `question-ask` to
  Genetics 04H slide 5, 06D slide 43, and the two existing question-only Lecture 10D dividers.
  Move the three question-layout recipes into a dedicated authoring guide so the main syntax
  reference has room to grow. Review all four course proofs and the affected classroom cards;
  all 5,878 base tests pass. Keep rendered implementation proof under `_temp/`.

- Implement the instructor's section-header ODP/PDF reference with native editable master shapes:
  framed dark sections, light center bands with medium edges for subsections, dark inset panels
  with light edges for the new `subsubsection`, and ultra light hexagons with dark corners for
  `question-ask`. Preserve measured course hues/saturations, add ultra light colors, lighten the header
  gradient from medium to white, and use ultra light closer text on dark backgrounds. Update the
  existing behavior/export checks and authoring guidance; keep reference-specific proofs temporary.
  Explicit dark list markers and bundled marker fonts preserve readable examples over the pale
  prompt center. All 44 measured color pairs pass; the minimum text contrast is 6.81:1.
  Clarify that editable text is required and decorative shapes are an implementation choice.

- Revise Genetics Lecture 09-15 agendas using the instructor's original short deck titles and
  topic labels, preserving chapter groupings and class activities. Add undated agenda-only sources
  for Lectures 14 and 15,
  correct remaining November 17 Quiz 4 references to December 1, and keep Quiz 5 conditional on
  the class vote. Document brief agenda wording and calendar checks in the announcement-deck guide.

- Restore Lecture 10's agenda with chapter grouping and brief topic labels from the original,
  including karyotypes, chromosome nomenclature, aneuploidy, and polyploidy. Include the movie choice
  and Quiz 5 vote; check the rendered agenda against the original and current content decks.

- Compare all 149 original Lecture 10 pages with all 184 current visible pages. Record the
  improvement in teaching structure, questions, and explanations alongside remaining dense
  reference figures. Repair answer leakage in CFTR/polyploidy questions, restore the original
  CFTR band-location illustration, enlarge ultrasound and screening visuals, replace graph-
  inconsistent risk prose with interpretation prompts, and correct the chromosome-2 centromere
  claim against primary evidence. Refresh the current review and source-map counts; keep the
  lecture-specific verification as temporary evidence.

- Restore the original three-stage nondisjunction comparison in Lecture 10D slides 21-23.
  The replacement lineages omitted original segregation details, and the products replacement
  rendered blank in LibreOffice. Rebuild the current 65-slide ODP/PDF and visually verify both
  branches and all eight illustrated gametes. Review the two remaining prenatal replacement
  figures in 10D and retain their complete anatomy/workflow diagrams.

- Add the native editable `prompt` layout for icebreakers and open discussions. Required
  question/examples slots supply automatic red emphasis and dark supporting text on a pale card.
  Migrate Lecture 10's food-classification icebreaker and all 14 catalog entries to plain-text
  slots. Keep two behavior tests for default styling/readability and required supporting examples.

- Make Lecture 10B-D hierarchy consistent: retain broad opening and Summary sections, use
  subsections for teaching topics, and split the long chromosome-shape, address, and trisomy
  runs at existing conceptual boundaries. Clarify the roughly ten-slide divider target in the
  teaching guide and conversion checklist. Use automatic answer colors throughout Lecture 10
  by removing three local answer-block overrides.

- Complete the Lecture 10 question-layout audit: give Recognizing Homologs and Follow the X
  Chromosome the native question/answer layout and answer popup, retaining their fuller follow-up
  explanations. Label the homolog question select-all-that-apply. All eight choice-based problems
  now use the dedicated layout; clarify this requirement in the teaching guidance.

- Replace Lecture 10's unfinished pop-culture fallback with the instructor's hot-dog/sandwich
  and ice-cream/soup classification debate, with a colored prompt and dark examples and suggestions.
  Add six varied, ready-to-use catalog options spanning debate, recognition, missing pairs,
  directions, traditions, and movie perspectives. Compare the previous two lectures when selecting
  prompts so premises and examples vary. Complete older entries' examples and prompt colors.

- Replace nearly white subsection tints with saturated course-color divider pairs. Keep the
  original course hue and saturation, with dark framed sections and brighter striped
  subsections. Use the instructor's revised 2:1 minimum for all background comparisons:
  between levels and from each to black and white. Define all three background colors for
  each course, reserving the third for a future subsubsection layout. Every adjacent step
  from black through the three backgrounds to white measures 2.10-2.17:1. Genetics uses
  #1C4470 / #3177C3 / #8CB5E2; black subsection headings
  exceed 4.5:1 and white section headings exceed 9.7:1. Update the existing native-export
  regression and measured palette audit; ordinary accents and decorative tints retain their
  existing colors. The initial pale treatment lost recognizable course color, while the proposed
  simultaneous 3:1 background limits exceeded the available black-to-white range.

- Integrate sixteen original pea, Four-o-clock, snapdragon, cattle, Western and ELISA SVGs
  through 60 image URLs in three sources, preserving native teaching content and original art.
  Independent actual-context reviews cover 78 authored contexts per variant: all 150 ordinary
  and six hidden page images are individually inspected. Preserve 306 native paragraph/style
  instances and 1,082 SVG text instances: 1,060 selectable plus 22 decorative book-cover words
  outlined in PDF but live in SVG. Recompile all six proofs under current R1 runtime; every
  reviewed R0 ODP ZIP payload is byte-exact, with only container timestamps changed. This
  qualifies the existing proof PDFs without claiming unchanged tables throughout the course.
  Retain the corrected ELISA plate well, useful captions and credits, and the narrow authorized
  textbook-ID omissions. Add one pea/Four-o-clock paragraph to the provisional botanical guide.
  Preserve four available prior Genetics outputs; the two absent Biotechnology outputs have
  historical hashes only. Canonical full-root builds and a fresh exact base suite are pending;
  the earlier 5791-test result belongs to the preceding batch. See
  [genetics_visual_renewal_progress.md](active_plans/reports/genetics_visual_renewal_progress.md).

- Give the reusable prompt catalog neutral Icebreaker titles and use Icebreaker in Genetics
  Lecture 10. Document the in-person format in announcement guidance and the conversion checklist;
  keep Zoom-specific discussion naming with the Zoom guidance.

- Split layout regression tests into compiler, table, text, and media modules. Apply the
  permanent-test checklist to remove incidental style/identity assertions and duplicate native
  export checks; reduce redundant parameter sweeps. Keep one-time rebuild and rendered-review
  checks as task evidence. The former 916-line module is now below the advisory band.

- Align ordinary table bodies by column: numeric-only columns use their preset's numeric
  alignment, while mixed notation keeps consistent preset alignment. Ignore headers, blanks,
  and merged cells when classifying columns; preserve merged-cell defaults, matrix rules,
  and explicit table/cell overrides. Add a mixed-notation example to the native table showcase.

- Accept and integrate five original mouse-graft, strawberry, MALDI, electrospray and magnetic
  sector drawings through 24 image URLs in three ASCII sources. Independent source/art and
  actual-context reviews accept 34 paired contexts across 68 inspected PDF pages, preserving
  131 selectable SVG text instances and 140 native paragraph/style instances. Complete URL
  reversal restores source bytes/models; native voice, layouts and original assets stay intact.
  Add one reviewed botanical construction example to the provisional illustration guide.
  Archive six prior canonical outputs byte-exact before authorized supersession; freeze 906
  integration entries and the delivery docs. All three canonical builds exit zero with
  source/ODP/hidden/PDF counts of 55/55/0/55, 49/49/1/48 and 390/390/6/384. Individually inspect
  all 34 contexts and 24 exact placements; all 131 SVG text and 140 native paragraph/style
  instances match accepted proofs. Thirty-one render hashes match; the three strawberry pairs
  pass direct visual and content/style comparison. Retain the initial generated-style-ID check
  failure and its complete-definition correction; no source/export change or rebuild is needed.
  The exact base suite runs once: 5791 passed, 2 existing warnings in 26.79s, exit 0, with zero
  tracked build/test mutations. All 906 integration and four frozen document/archive entries
  stay intact. Only five accepted SVG additions enter the index; prior entries and thirteen
  cached EOF warnings stay unchanged. Prior output archives and unrelated LECT06 references
  remain intact. LibreOffice is released. Delivery is DONE_WITH_CONCERNS for the inherited tiny
  mouse overlay, fine-label reading limits and unchanged TOF neighbor's clipped final two words.
  The earlier 5781-test receipt retains its prior-batch scope. This documentation-only closeout
  follows the suite; guide/example and archive stay unchanged. No tests, exports or index actions
  run for this receipt. This batch is complete; the broader all-lecture goal remains open. See
  [genetics_visual_renewal_progress.md](active_plans/reports/genetics_visual_renewal_progress.md).

- Accept seven original mitosis-stage, division-comparison, plant-wall and organelle drawings
  after independent source/art and actual-context review. Seventeen paired contexts retain
  119 selectable SVG text elements and 52 native paragraph/style instances across 34 PDF pages.
  Integrate seven exact accepted SVGs through seven image URLs in three ASCII Djot files;
  URL reversal restores complete source bytes and parsed models. Preserve all 210 preexisting
  assets, seven other source dependencies and 96 runtime files. No production code or source
  cleanup changes are needed. Add one reviewed wall example to the provisional illustration
  guide, separating its retained 50 nm fibril-scale cue from schematic exploded layer spacing.
  Preserve the prior Biotechnology ODP/PDF byte-exact before authorized output supersession.
  All three canonical builds pass with source/ODP/hidden/PDF counts of 24/24/0/24, 53/53/0/53
  and 281/281/0/281. Individually inspect all seventeen unique contexts and all seven placements;
  all 119 SVG text elements and 52 native paragraph/style instances match accepted proofs.
  Thirteen of seventeen renders match bytes; all seventeen content signatures and text streams
  match. The exact base suite runs once: 5781 passed, 2 warnings in 23.70s, exit 0, with zero
  tracked build/test mutations. All 837 integration entries and four frozen document/archive
  entries remain intact. Only seven exact SVG additions enter the index; other entries and
  thirteen existing cached EOF warnings remain unchanged. LibreOffice is released. Delivery is
  DONE_WITH_CONCERNS for fine labels, chemistry and chromosome tips needing the full lecture
  view, schematic wall spacing, the inherited division-neighbor overlay and capacity advisories.
  The previous 5767-test receipt retains its earlier eight-drawing scope. This final
  documentation-only receipt follows the suite; guide/example and archive stay unchanged.
  No tests, exports or index actions run for this receipt. This batch is complete;
  the broader all-lecture artwork goal remains open. See
  [genetics_visual_renewal_progress.md](active_plans/reports/genetics_visual_renewal_progress.md).

- Accept eight fly, Morgan, sexual-cycle and industrial drawings after independent source/art
  and actual-context review. Correct only the cycle sporophyte leader to reach its exposed
  capsule; preserve the rejected parent and first-pass proofs. The initial paired proofs cover
  twenty contexts per variant, forty inspected PDF pages, 213 selectable SVG text elements and
  46 preserved native paragraphs; the corrected three-page cycle proof retains all 52 labels.
  Integrate eight exact SVGs through eight URLs in four Djot files. All 222 original assets and
  six other source dependencies remain unchanged. Separately escape one inherited degree sign
  as `&#176;`; complete models and rendered wording remain identical. URL/entity reversal
  restores original source bytes. Add two reviewed Morgan/ethanol composition examples to the
  provisional guide. Preserve the tiny assembly panel's 6.92-8.36 pt label limits, with no large
  repeat, and other full-view reading limits. Canonical source/ODP/hidden/PDF counts are
  62/62/0/62, 53/53/0/53 and 281/281/0/281. Inspect all nineteen unique canonical contexts
  covering twenty proof instances and all eight changed placements. All 213 SVG text elements
  remain selectable; all 46 native paragraph/style instances match. Preserve the whole mixed
  GIF, corrected cycle leader and rendered degree sign. Thirteen of twenty proof-instance
  renders match bytes; all twenty content signatures match. The exact base suite runs once:
  5767 passed, 2 warnings in 23.43s, exit 0. Builds and tests have zero tracked-file mutations.
  Stage only eight exact SVG additions; preserve other index entries and thirteen existing
  cached EOF warnings. Save two old canonical PDFs byte-exact before explicit supersession;
  the other 682 frozen integration entries, three documents, archive and helper remain intact.
  Retain the corrected scratch degree-sign page-map check and its initial failed log; no
  source/export change was needed. LibreOffice is released. This final documentation-only
  receipt follows the successful suite; guide and archive remain unchanged. Delivery is
  DONE_WITH_CONCERNS for accepted fine-detail limits and inherited margins/capacity advisories.
  The earlier 5751-test receipt remains specific to the prior batch. This batch is complete;
  the broader all-lecture artwork goal remains open. See
  [genetics_visual_renewal_progress.md](active_plans/reports/genetics_visual_renewal_progress.md).

- Accept an Ames apparatus drawing, five checkpoint-gate drawings and one Neurospora cycle
  after independent source/art and actual-context review of seven placements across twelve
  paired contexts. Integrate eight exact accepted SVGs through seven URL spans in three source
  files; URL reversal restores complete bytes and parsed models. All 89 original assets and
  eleven other source dependencies remain unchanged. Add one demonstrated organic-cycle/photo
  composition example to the provisional illustration guide. Canonical source/ODP/hidden/PDF
  counts are 244/244/0/244, 24/24/0/24 and 31/31/0/31. All twelve contexts preserve native text,
  notes, frames, non-target images and selectable text; all 99 SVG text elements and 32 native
  paragraphs with referenced styles match. Inspect every changed and neighboring context.
  Nine of twelve renders match accepted proof bytes; three Neurospora pages differ without
  meaningful visual or signature changes. The mixed Neurospora SVG/ODP retains exact empirical
  photo pixels and PNG bytes; normal PDF export uses a 141 x 144 JPEG with alpha mask, so exact
  PDF pixels are not claimed. The first exact base suite reports 1 failed, 5750 passed,
  2 warnings in 23.34s: fourteen new Markdown links target ignored temporary evidence. Convert
  only those links to inline paths; the focused ledger check passes (1 passed, 1 warning in
  0.44s), then the exact base suite passes (5751 passed, 2 warnings in 24.59s, exit 0).
  Preserve the failed logs and original/corrected documentation freezes. Builds and both suite
  runs have zero tracked-file mutations. All 313 integration-frozen files and four corrected
  frozen documents remain intact. Only eight exact accepted SVGs enter the index; other index
  entries and thirteen preexisting cached EOF warnings remain unchanged. LibreOffice is
  released. Delivery is DONE_WITH_CONCERNS for minor connector/caption spacing, fine-detail
  viewing limits, PDF photo resampling and unchanged capacity advisories. Rotate the changelog
  with the existing script: keep November 10/9 active and preserve all older content verbatim
  in [CHANGELOG-2026-11a.md](CHANGELOG-2026-11a.md), leaving existing archives unchanged. This
  documentation-only receipt follows the successful suite. The earlier 5734-test receipt
  remains specific to the completed bottle/algae/liposome batch. This batch is complete; the
  broader all-lecture artwork goal remains open. See
  [genetics_visual_renewal_progress.md](active_plans/reports/genetics_visual_renewal_progress.md).

- Accept five original bottle, algae-fuel and liposome drawings after independent source and
  actual-context review of eight uses across fourteen paired contexts. Correct only the therapy
  plasmid-label leader so it reaches the core plasmid above the shell; preserve parent art and
  the other four accepted drawings. Verify native text, notes, geometry, non-target images and
  selectable SVG labels. Preserve the reviewed adjacent big-image views for fine liposome labels
  and the inherited bottle-neighbor overlay. Integrate five exact SVGs through eight URL spans
  in three source files; URL reversal restores complete source bytes and parsed models. All 151
  preexisting assets and eighteen other source dependencies remain unchanged. Canonical
  source/ODP/hidden/PDF counts are 77/77/1/76, 281/281/0/281 and 244/244/0/244. All fourteen
  contexts match accepted proof content, notes, geometry, payloads and selectable text; all 123
  SVG text-line instances remain selectable. Inspect all eight changed placements, including the
  corrected therapy leader in both views. Twelve of fourteen renders match proof bytes; two
  bottle renders differ without meaningful visual or signature changes. Exact base suite runs
  once: 5734 passed, 2 warnings in 28.49s, exit 0, with zero tracked build/test mutations. Only
  five accepted SVGs are staged; other index entries and frozen inputs remain intact. LibreOffice
  is released. This documentation-only receipt follows the suite. Delivery is DONE_WITH_CONCERNS
  for inherited fine-print viewing limits, bottle-neighbor overlay, low algae-neighbor margin
  and unchanged capacity advisories. The earlier 5724-test receipt remains specific to the prior
  animal/gamete batch. This batch is complete; the broader artwork goal remains open. See
  [genetics_visual_renewal_progress.md](active_plans/reports/genetics_visual_renewal_progress.md).

- Accept four original animal/human life-cycle and gametogenesis drawings after independent
  source and six-page actual-context review, preserving native content, frames and all 49
  selectable SVG text elements. Correct human export banding with exactly four skin fills
  changed to existing palette solids; preserve every other artwork byte. Retain the initial
  striped proof and unsuccessful percentage-gradient probe as evidence. This scoped workaround
  establishes no general gradient policy or renderer-cause diagnosis. Integrate exactly four
  accepted SVGs through four image URLs; all 70 original assets remain unchanged, and URL
  reversal restores source bytes and the complete parsed model. Add a human-cycle composition
  example to the illustration guide. Canonical source/ODP/hidden/PDF counts are 53/53/0/53;
  verify all four exact payloads, six final-proof context signatures and 49 selectable labels.
  View all six canonical pages: human skin remains smooth and half-width labels fit. Five of
  six renders match proof bytes; the human raster differs without meaningful visual or signature
  change. Fresh base suite runs once: 5724 passed, 2 warnings in 23.46s, with zero tracked-file
  mutations. All 70 old assets and frozen receipts remain intact; only four accepted SVGs are
  staged and other index entries are preserved. This documentation-only receipt follows that
  run. Delivery is DONE_WITH_CONCERNS for the inherited unchanged slide 37 capacity advisory.
  The batch is complete; the broader all-lecture artwork goal remains open. See
  [genetics_visual_renewal_progress.md](active_plans/reports/genetics_visual_renewal_progress.md).

- Accept five original inversion drawings and two fuel-cell cutaways after independent source
  and actual-context review: forty paired proof pages, seven placements and 156 selectable
  SVG text elements. Preserve native voice, layouts, markers and microscopy. Final fuel copies
  fix blank LibreOffice import by changing only the XML declaration from ASCII to UTF-8;
  source bytes remain ASCII and parsed artwork is unchanged. Retain failed proofs as evidence.
  Integrate exactly seven SVGs and seven image URLs; URL reversal restores original source bytes
  and all 132 preexisting assets remain unchanged. Canonical source/ODP/hidden/PDF counts are
  48/48/0/48 and 281/281/0/281. Verify all seven placements, twenty accepted new-proof context
  signatures and 156 selectable SVG text elements; inspect all changed pages individually.
  Nine of twenty canonical renders match proof bytes; eleven inversion renders have small
  documented differences without visible fit regression. Fresh base suite: 5716 passed,
  2 warnings in 23.16s, with zero tracked mutations and only seven accepted SVGs added to the
  index. This documentation-only receipt follows that run. Batch delivery is DONE_WITH_CONCERNS
  for protected inversion overlays, fine labels and inherited capacity advisories. The broader
  all-lecture artwork goal remains open; see
  [genetics_visual_renewal_progress.md](active_plans/reports/genetics_visual_renewal_progress.md).

- Integrate five accepted Genetics SVGs through five image URLs: three ordered-tetrad drawings
  in LECT09H and landscape amniocentesis/CVS drawings in LECT10D. Preserve native wording,
  alt text, layouts, original assets and accepted portrait candidates. Fresh source and
  actual-context reviews accept ten ordered and four selected prenatal pages. The landscape proof
  enlarges main labels from 8.529/8.204 pt to 13.394 pt while retaining anatomy and workflows.
  Add one practical composition example to the provisional
  [slide-specs/GENETICS_ILLUSTRATION_GUIDE.md](slide-specs/GENETICS_ILLUSTRATION_GUIDE.md).
  Canonical source/ODP/hidden/PDF counts are 31/31/0/31 and 63/63/0/63. Verify all five placements,
  all fourteen accepted proof contexts and 172 selectable SVG labels; open all five changed
  pages and four neighbors. Fresh base suite: 5702 passed, 2 warnings in 22.94s, with zero
  mutations across 1190 tracked files. Only the five authorized SVGs were staged. This
  documentation-only receipt follows that run. Delivery is DONE_WITH_CONCERNS for dense
  ordered-mitosis fine text at reduced viewing sizes; the broader artwork goal remains open. See
  [genetics_visual_renewal_progress.md](active_plans/reports/genetics_visual_renewal_progress.md).

### Fixes and Maintenance

- Correct the overreaching Lecture 10 voice pass: restore established instructor wording and
  emphasis on 39 B-D pages, plus 10A's shared announcements, policies, and homework instructions.
  Restore the full-width contact prose and plain anonymous-message instructions. Clarify that
  voice edits target LLM-authored additions and that color marks meaningful distinctions.
  Preserve the existing scientific corrections, current dates, question layouts, and reveals.

- Omit the XML declaration from `write_svg()` output to avoid the observed blank LibreOffice
  imports associated with `encoding="ASCII"`. Preserve ASCII bytes, numeric character
  references, safe parsing and metadata validation before writing. Caller inspection finds no
  declaration dependency; both existing SVG drawing tests and disposable XML/Unicode/ASCII/
  invalid-metadata preservation checks pass. No artwork is regenerated and no new dependency
  or permanent test is added. No fresh live LibreOffice check of this helper is claimed;
  the subsequent exact base suite passes with 5767 tests and two warnings. Evidence:
  `_temp/svg_writer_declaration_fix/HANDOFF.md`.

## 2026-11-09

### Additions and New Features

- Integrate seven independently accepted Genetics SVGs through eight image URLs: three
  unequal-crossing artworks in LECT11E and four meiosis stages in LECT06C. Preserve native
  wording, alt text, layouts, reveal markers and all original assets. Fresh source and
  actual-context reviews accept all seven drawings and 22 candidate pages, with fine anatomy
  labels requiring the large view. Add one canonical meiosis example to the provisional
  [slide-specs/GENETICS_ILLUSTRATION_GUIDE.md](slide-specs/GENETICS_ILLUSTRATION_GUIDE.md).
  Both canonical builds pass at 53/53/0/53 and 37/37/0/37 source/ODP/hidden/PDF pages.
  Verify all eight SVG placements and all 22 accepted proof contexts; inspect eight changed
  and two adjacent canonical pages. Fresh base suite: 5692 passed, 2 warnings in 24.98s,
  with no tracked-file mutations. This documentation-only receipt follows that run.
  Delivery is DONE_WITH_CONCERNS for fine-detail display limits and inherited density;
  the broader artwork goal remains open. See
  [genetics_visual_renewal_progress.md](active_plans/reports/genetics_visual_renewal_progress.md).

- Integrate nine independently accepted original Biotechnology artworks as ten SVG files through
  45 image URLs, plus the second Genetics challenge OCR quote card through one image URL.
  Preserve original rasters, native prose, alt text, questions, answers and layouts; the quote
  retains the source typo. All 34 Biotechnology actual-source proof contexts pass visual review,
  with inherited small-panel label limits retained. Add two canonical equipment examples to
  [slide-specs/GENETICS_ILLUSTRATION_GUIDE.md](slide-specs/GENETICS_ILLUSTRATION_GUIDE.md).
  Complete all three canonical builds: source/ODP/hidden/PDF counts are 11/11/0/11,
  390/390/6/384 and 281/281/0/281. Verify all 46 SVG placements and proof equivalence for
  35 changed plus two adjacent contexts; inspect 22 canonical pages. The exact base suite
  passes 5678 tests with 2 warnings in 22.39s, with zero changes across 1054 monitored files.
  This documentation-only receipt follows that run. Delivery is DONE_WITH_CONCERNS because
  inherited tiny labels and capacity advisories remain; the broader art goal stays open. See
  [genetics_visual_renewal_progress.md](active_plans/reports/genetics_visual_renewal_progress.md).

- Complete independent review, seven-URL canonical integration and export review for six yeast
  drawings and one mouse-selection SVG; the inherited mouse placement remains tiny. Integrate an
  independently reviewed, faithful DNA polarity OCR quote card through one image URL, retaining
  the original PNG and native source text. The card has editable SVG text, not a native Djot
  blockquote; its canonical export passes at 47 source/ODP/PDF pages, with three changed/adjacent
  pages reviewed. Repair the prior
  copied-tool/archive suite failures, preserve twelve historical source files byte-for-byte, and
  document MIT/LGPL notices in `svg_tools/README.md`. The subsequent base suite passed 5973 tests
  with 2 warnings before quote integration. Prioritize further art by visual gain and difficulty;
  see [genetics_visual_renewal_progress.md](active_plans/reports/genetics_visual_renewal_progress.md).
  Subsequently remove 36 unused copied SVG tool files and three unused dependencies, retaining
  the original six drawing helpers; two focused tests pass. Integrate three independently accepted
  first-cousin pedigree SVGs through exactly five image URLs on slides 45-48, preserving all
  native source bytes after URL reversal and all original rasters. The four-page placement proof
  passes; canonical source/ODP/PDF counts are 61/61/61. The 5973-test run predates tool pruning,
  quote integration and pedigree integration; the final suite passed 5656 tests with 2 warnings
  in 22.99s and zero mutations across 1167 tracked files. Strict checks passed for 118 Genetics
  Djot files and 275 authored SVGs. Eight SVGs had 17 characters encoded as XML references
  with parsed content unchanged. Existing display advisories remain; see the progress ledger.

- Accept the chromosome-complement, folded-hemoglobin, CCR5 and corn drawings and their
  ten-page original-voice proof. Integrate four artwork files and exactly two image URLs;
  canonical source/ODP/PDF counts match at 112, 51, 31 and 53 pages with no hidden slides.
  Ten changed/adjacent pages pass visual review; 128 image references preserve exact bytes and
  18 native paragraphs match the accepted original-voice proof. Fresh verification passes
  5324 tests with 2 warnings in 25.68s and no source/doc mutations across 1,434 files, before
  this documentation-only receipt. Record the instructor's raster-image replacement
  scope and preserve native slide voice, prose, titles, alt text, examples, layouts and sequence.
  Keep CCR5 prose byte-identical; the cancelled scratch variant is not delivered. The broader
  all-lecture art goal stays open, with Genetics first. Details and
  accepted source links are in
  [genetics_visual_renewal_progress.md](active_plans/reports/genetics_visual_renewal_progress.md).

- Accept the provisional [slide-specs/GENETICS_ILLUSTRATION_GUIDE.md](slide-specs/GENETICS_ILLUSTRATION_GUIDE.md)
  and three durable examples, plus small projected cuboid/cylinder construction helpers.
  Specification and quality reviews accept standalone ABO and bottleneck refinements; their
  eight-page contextual proof passes independent review. Integrate the four accepted SVGs and
  remove three drift review markers plus three invisible-image references, preserving source
  text, slide counts and original assets. Canonical ABO/drift source/ODP/PDF counts match at
  44/44/44 and 35/35/35; eight changed/adjacent pages pass review. The final batch suite passes
  5324 tests with 2 warnings; unrelated slide-capacity advisories remain recorded in the
  [genetics_visual_renewal_progress.md](active_plans/reports/genetics_visual_renewal_progress.md). Preserve
  source-supported XX/XY chromosome findings and remaining limits in
  [genetics_illustration_reassessment.md](active_plans/reports/genetics_illustration_reassessment.md).
  Release the reassessment hold for this bounded original-art batch under existing authorization;
  remaining course artwork and final delivery checks stay open.

- Add seven short curated teaching-purpose decks and a visual authoring index in
  [../exemplars/README.md](../exemplars/README.md). Preserve course context in
  lightly polished copies, keep verified original artwork in deck-owned local folders, and document
  source headings, teaching rationale, alternatives, adaptations, and historical logistics.
  Link the collection from the root README and authoring overview; retain the canonical table-style
  demonstration. Independent rendered review and integration are tracked separately.

- Add themed native table presets, whole-cell and table formatting overrides, measured padding,
  selective borders, and coordinated question/answer column sizing. Publish
  [slide-specs/TABLE_AUTHORING_GUIDE.md](slide-specs/TABLE_AUTHORING_GUIDE.md) and the maintained
  [../exemplars/table_styles.djot](../exemplars/table_styles.djot) demonstration for editable ODP
  and ODP-derived PDF output. Reconcile 424 physical teaching tables (421 existing plus three
  restored), separately from the 14-table demo; preserve all 96 repaired source tables and clear
  59 target markers while retaining 37 non-table blockers. Record native edit/save/reopen,
  rendered comparison, source/hash evidence, and verification limits in the dated
  [native table results](archive/native_table_styles_results.md). Verify 53 normal course ODP/PDF pairs plus the separate 14-page demo; retain 16
  table-only fallback contexts in two blocked consumers. Final integration review is pending.
  Raw ODP import now preserves every supplied valid source column proportion,
  including equal and near-equal widths; curated course tables and accepted outputs
  were unchanged. All 93 changed raw snippets preserve source facts, cell lines,
  scripts, and spans, with maximum ratio error 1.039e-6. Two regressions, 50 importer
  checks, and six selected security/typing/style gates pass. The final base suite
  reports 4,380 passed, three failed, two warnings, and 109 errors in 24.86s; the
  failures and setup errors trace to inherited Biotechnology LECT10 parse conflicts,
  and no new table-code tests failed.

- Consolidate authoritative slide guidance into `docs/slide-specs/COLOR_GUIDE.md`, `VOICE_GUIDE.md`, and
  `PEDAGOGY_GUIDE.md`. Preserve recorded preferences and useful teaching examples, distinguish
  instructor instructions from observed habits and inherited recommendations, and adapt the BPQ
  material to slide teaching. Keep the older style guide as a layout/typography overview, remove
  the superseded methods guide, and link authoring and review docs directly to the specifications.
- Convert Genetics LECT12, LECT13, and LECT1X into 17 canonical Djot decks with local assets,
  per-folder source maps, and conversion reviews. Preserve all 642 original content slides
  and their hidden status; add 45 opening/closing slides. Build 796 editable ODP slides and
  760 visible PDF pages, retaining 307 explicit `@replaceme` slides for difficult conversions.
- Convert Genetics LECT11 into five canonical Djot decks with local assets, source maps,
  and a completed conversion review. Retain all 253 original B-E content slides and their
  hidden status; add objectives and closing summaries. Build 320 editable ODP slides and
  302 visible PDF pages, retaining 62 explicit `@replaceme` slides for difficult conversions.

### Fixes and Maintenance

- Keep seven exemplar gallery WebPs and reuse the existing table screenshot; delete the other
  61 slide previews. Publish the compact gallery and link all 68 authored slides to their Djot
  source definitions instead of individual preview files.
- Archive seven completed root-level planning and review documents and seven completed exemplar
  review reports from `docs/active_plans/` in `docs/archive/`; update inbound and relative links.
- Move the announcement guide, authoring overview, visual rubric, Djot syntax, and SVG diagram
  contract into `docs/slide-specs/`, naming the overview `AUTHORING_GUIDE.md`. Add a short README
  index and update inbound and relative links, including course reviews and archived plans.
  Keep vendored palette/contrast references at their managed paths; retain no compatibility files.
- Review all 460 current replacement-marked slides against rendered diagnostics and mapped
  source pages. Recommend the existing native-table import path as the largest bounded repair
  target: 96 affected slides, compared with 69 artwork-composition candidates. Record the
  per-slide findings in [replaceme_impact_review_2026-11-09.md](archive/replaceme_impact_review_2026-11-09.md).
  Clarify that a composed figure has one artwork image and associated labels that may extend
  outside it; slide titles, captions, and explanatory prose remain native.
- Extend that review with a source-table feature census: 61 of the 96 slides use selective
  borders, 40 have colored cells, nine have horizontal merges, and none has vertical merges.
  Identify selective cell borders as the strongest new table feature; fills, horizontal spans,
  column proportions, and shared column sizing already exist.
- Split former Genetics LECT1X into LECT14 (allele frequencies and Hardy-Weinberg) and
  LECT15 (evolution, selection, drift, and inbreeding), with four B-E decks in each.
  Renumber covers and move original inputs, local assets, includes, and review/source maps
  together. Rebuild 362 authored slides and 361 PDF pages; retain all 136 replacement markers.
  Keep the existing December 8 cover date because the schedule assigns no Lecture 14/15 dates.
- Prepare December 1/8 announcements from the latest current-year deck and matching prior-year
  sources, with current quiz/homework/final dates and shared groups. Retain LECT1X's eight
  separate population-genetics variants and document the supplied folders' schedule mismatch.
- Compare every visible original content page with diagnostic renders. Mark missing tree,
  chromosome, table, and mask relationships; restore basic superscripts and readable colored
  definitions. Record temporary import fallbacks and unresolved work in each lecture review.
- Prepare 2026 Lecture 11 announcements from the latest current-year material and matching
  prior-year lecture, using shared groups and current assessment dates. Record the schedule's
  content/date mismatch and keep the early weather snapshot hidden. Describe this usual
  two-source starting point briefly in the announcement guide and human guidance.
- Review paired original/diagnostic renders, restore the colored GMO comparison columns,
  clear verified color-only deletion-walkthrough flags, and retain markers for missing
  diagram geometry, labels, source reveals, or readable fit. Preserve the original ODP/PDF.

### Developer Tests and Notes

- Slide-specification relocation: 1,384 Markdown link, ASCII, and whitespace checks pass.
  Verify all five old paths are absent, fenced examples are unchanged, and all six local heading
  links in the specification folder resolve. Full suite and slide exports are not repeated for
  the documentation-only move.
- Remove the superseded teaching-methods pointer and record the pre-production preference for
  direct contract/caller updates over compatibility scaffolding. All 143 Markdown link checks
  pass after cleanup; `git diff --check` is clean.
- Slide-specification documentation checks: 1,386 link, ASCII, and whitespace checks pass.
  Direct review confirms the five consolidated documents are ASCII and their 11 local heading
  links resolve; a five-slide temporary formatting example passes project Djot lint. Base suite:
  4,237 passed, 3 failed, 109 setup errors, all failures/errors tracing to existing Biotechnology
  LECT10 parse problems in unchanged sources. No fresh slide exports or classroom validation.
- Replacement-impact review reconciles all 460 physical markers and per-slide findings, with
  no reviewed source/code drift after the sync warning. Documentation checks: 801 passed,
  2 failed on missing links in the separate question pedagogy/voice guides. No production
  behavior changes; the full base suite and attended playback are not rerun for this review.
- LECT14/15 native lint and all-format LibreOffice builds pass. All 353 non-cover PDF pages
  retain identical teaching text, and original input/media hashes and hidden flags reconcile.
  Reviewed the eight updated covers and sampled minor differences in text rendering. Base suite:
  4,051 passed, 3 failed, 87 errors in the pre-existing Biotechnology LECT10 edits.
- LECT12/13/1X strict native lint and all-format LibreOffice builds pass; authored/hidden/PDF
  counts and replacement watermarks reconcile. Base suite: 4,043 passed, 3 failed, 87 errors
  from the existing Biotechnology LECT10 conflicts. All original ODP hashes remain unchanged.
  Attended playback and classroom validation remain unperformed.
- Strict native lint and all-format LibreOffice builds pass for LECT11; source/ODP/PDF
  counts and replacement watermarks reconcile. Base suite: 4,041 passed, 3 failed,
  87 errors in existing Biotechnology LECT10 working-tree edits, which remain untouched.
  Attended Impress playback and classroom validation were not performed.
