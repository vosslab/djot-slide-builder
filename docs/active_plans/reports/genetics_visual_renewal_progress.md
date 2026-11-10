# Genetics visual renewal progress

Status: guide/helper/ABO/bottleneck batch complete, including canonical ABO/drift exports and
final batch checks. Chromosome, folded hemoglobin, corn and CCR5 artwork and the ten-page
original-voice contextual proof are accepted. Art-only integration, canonical four-root exports
and fresh final checks are complete. Yeast/mouse and DNA quote canonical exports are accepted;
three cousin-pedigree SVGs and the SVG tool pruning are complete. Broader creative renewal
remains open. The second challenge quote and nine Biotechnology artworks are delivered with
retained small-panel concerns. Seven unequal-crossing/meiosis drawings and all 22 actual-source
context pages are accepted. Canonical art-only integration, both full-root exports and fresh
final checks are complete, with fine-detail display limits retained.
Three accepted ordered-tetrad drawings and two accepted prenatal landscape drawings are integrated
through five image URLs. Both canonical full-root exports and fresh final checks are complete,
with dense ordered-mitosis fine text requiring the large view.
Five inversion drawings and two fuel-cell cutaways are now integrated and canonically delivered
with fresh final checks; inherited inversion overlays and fine-text limits remain.
Updated 2026-11-10. This is the single execution ledger for
[genetics_visual_renewal_plan.md](../active/genetics_visual_renewal_plan.md).
All delegated agents use `gpt-6-astra`, as explicitly requested.

The overall goal now covers all production lecture slides, with original high-quality SVG art
and preserved voice, scientific concepts and existing content. Artists retain creative freedom
within the shared visual language. Genetics remains first; `remaining_lecture_art_survey`
covers Biotechnology, Biostatistics and shared lecture art as reference inventory only.
Genetics completion alone will not establish completion of the broader goal.

## Current scope and state

The outcome is ambitious original SVG art throughout Genetics, with a shared visual language
established from representative examples before broad dispatch. Source images supply scientific
facts and teaching purpose, not required pixels, contours, perspective or composition. Preserve
course examples, data and question/reveal states. Existing native tables/styles remain resources;
independent table, math, problem-text and sequence migration is excluded. All gene-tree work,
including LECT12 teaching and great-ape comparisons, remains deferred. Pedigrees remain eligible.

The latest explicit scope is drawing/clipart replacement for rasterized images. Preserve the
instructor's voice, titles, native prose, alt text, examples, layouts and sequence. Check source
science only as needed for the drawing; this is not a global scientific or prose audit.
Prioritize potential visual improvement balanced against creation difficulty: achievable
high-impact art first, complex work later. `@replaceme` status is irrelevant to that ordering.

The instructor's latest clarification recognizes that useful work was already happening: the
pixel-equivalence wording was the concern. Those comparisons validated a serializer refactor and
archive preservation; they were not an art-quality criterion. Keep strong existing drawings and
improve specific weaknesses. No blanket redraw or discarded-work restart is proposed.

The [reassessment](genetics_illustration_reassessment.md) records creative findings and the
reviewed direction and source findings. Detailed task ownership and deliverables are in
[genetics_visual_workstreams.md](../workstreams/genetics_visual_workstreams.md).

## Completed maintenance evidence

- All five source-group cleanup handoffs are complete under
  `_temp/genetics_visual_renewal/scope_narrowing/{foundations,inheritance,linkage,variation,population}/HANDOFF.md`.
  `scope_narrowing/SPEC_REVIEW.md` accepts source reconciliation/archive preservation, subject to
  delivery checks; it explicitly does not accept the full art/construction-toolkit objective.
- Broader work remains at `_temp/genetics_visual_renewal/scope_narrowing/INDEX.md` and
  `normalized_observed_state/files/`: 434 captured files, including 49 changed Genetics Djots,
  328 new assets and 57 task documents. Initial and normalized captures preserve the history.
- Gene-tree preservation and duplicate cleanup are complete; see
  [README.md](../../archive/genetics_gene_tree_svg/README.md). Six original Djot hashes, 105
  original asset hashes, 46 SVG parses and 14 replay matches were recorded. The 45 verified
  canonical duplicates were removed. The archive remains future-work material, not delivered art.
- The shared ASCII fixer's XML branch and deterministic repair are complete. The temporary repair
  replaced 59 named entities in 12 SVGs and was idempotent. Valid numeric XML references retain
  visible characters. Original Djot Unicode was subsequently normalized centrally.
- The original `svg_tools/drawing.py` serializer foundation retains `text()`, `line()` and
  `write_svg()` behavior. Accepted construction additions are recorded below; the normalizer
  was not ported.
- Clean baseline: `source ./source_me.sh && pytest tests/` exited 0 with **5321 passed, 2 warnings
  in 24.07s**. Final run changed zero files; 118 Genetics Djots were ASCII and 376 source SVGs
  parsed. Exact evidence: `_temp/genetics_visual_renewal/final_verification/base_pytest_run2.log`
  and `run2_postchecks.json`. This is the checked maintenance state, not proof of future edits or
  creative acceptance.
- Later reassessment closeout: **5322 passed, 2 warnings in 28.66s**, exit 0; zero mutations
  across 1,143 hashed files, 118 ASCII Genetics Djots and 376 parseable source SVGs. Receipt:
  `_temp/genetics_visual_renewal/final_verification/reassessment_closeout/pytest.log`,
  `pytest.status` and `postchecks.json`. The final bounded batch run is recorded below.

## Milestone overview

| Milestone | Current status | Remaining evidence |
| --- | --- | --- |
| M1 | Inventory preserved; scope dispositions reconciled. | No new inventory campaign. |
| M2 | Historical pilots, source cleanup and archives retained. | Do not transfer historical acceptance to all artwork. |
| M3 | Six-pair audit, three family experiments and seven-page prototype review complete. | Reviewed direction released for the bounded original-art batch. |
| M4 | Provisional illustrated guide and demonstrated construction helpers accepted by specification and quality reviews. | Apply their documented limits in further artwork. |
| M5 | ABO/bottleneck and chromosome/folded-hemoglobin/corn/CCR5 artwork accepted; three family surveys complete. | Surveyed future families remain open. |
| M6 | ABO/drift and four-family art-only delivery complete, including canonical exports and fresh final checks. | Remaining families and whole-course delivery stay open. |

The 1,782 uses, 82 roots and 1,226 unique asset paths describe the original inventory, not art
completion. Classifications retain original identity/anchor fields and historical M1 rationale.
Native-only rows are not-targeted existing content; deferred trees remain excluded. No CSV churn
is part of this reassessment.

## Decisions and authority

| ID | Authority and state | Current consequence |
| --- | --- | --- |
| D0 | Instructor approval of original implementation and all-Astra delegation. | Preserve the ambitious art goal and model requirement. |
| D1 | Explicit earlier scientific corrections. | Keep authorized dominance and ratio corrections already retained; do not expand into general prose/math repair. |
| D2 | Preserve made-up species and manual pairwise averages. | Keep this evidence with deferred gene-tree work. |
| D3 | Historical broad M3 release. | Earlier blanket completion/acceptance claims do not settle current creative delivery. |
| D4 | Instructor scope correction: original SVG illustrations, with native tables/styles as resources. | Exclude independent native migration; permit original composition and necessary integration. |
| D5 | Instructor deferral of gene trees and preservation of working code. | Archive completed; future BPQ export remains in TODO. |
| D6 | Instructor requires clean base pytest and ASCII Djot; entities allowed. | Recorded clean baseline passes; recheck after final implementation changes. |
| D7 | Manager chose three serializer helpers as the small toolbox implementation. | Corrected attribution: limiting the toolbox to those helpers was not a user requirement and is superseded by construction experiments. Keep the useful maintenance work. |
| D8 | Instructor requests creative reassessment, drawing-book investigation, useful geometric primitives and a shared visual language. | Representative investigation and review are complete; accepted provisional guidance and demonstrated helpers support bounded art batches. |
| D9 | Instructor clarifies that pixel-equivalence evidence raised concern and existing work may be good. | Treat equality as refactor/preservation evidence only; retain strong art and improve demonstrated weaknesses without a blanket restart. |
| D10 | Manager releases the reassessment hold for the reviewed bounded original-art batch under existing implementation authorization. | Proceed with accepted contextual integration; no new permission gate. This is not broad redesign or course-completion acceptance. |
| D11 | Instructor reiterates raster-image drawing/clipart scope and preservation of slide voice. | Limit source checks to the artwork; cancel the three scratch CCR5 prose qualifications and preserve all canonical native wording. |

## Creative evidence and next results

- Six actual source/current pairs are rendered under `_temp/svg_creative_reassessment/`.
  Apparatus and peas offer useful work to retain/refine. Nucleotide needs selective refinement;
  ABO hierarchy, bottleneck identity and Drosophila chromosome-complement context need focused redesign/investigation.
- Equipment: `_temp/svg_construction_primitives/findings.md` records book passages, two massing
  alternatives, selected fresh cutaway, construction sheet and 1200/320-pixel previews.
  Cuboids and projected cylinders help real equipment parts. The ellipsoid is demonstrated on
  the sheet but its usefulness for organisms is not yet established. These are scratch artifacts.
- Organism: `_temp/svg_visual_language/organism/` compares compact form-based and organic
  Drosophila. `REVIEW.md` selects organic anatomy for a large figure and compact forms for
  repeated small comparisons. Diagram: `_temp/svg_visual_language/diagram/NOTES.md` selects
  the flat three-stage crossover composition because it makes the starting four chromatids and
  reciprocal ancestry change explicit. These are candidate directions, not a fixed style API.
- Combined scratch proof: `_temp/svg_visual_language/export/visual_language_proof.odp` and
  `.pdf` both contain seven pages, matching source, with no hidden pages. `evidence.json` records
  embedded SVG hashes, text and page renders. Fresh review accepts all seven actual PDF pages
  without clipping, label or export defects; three-stage crossover ancestry is coherent.
  Equipment and organic fly are strong examples to keep. One rear fly leg is occluded, limiting
  its use as a leg-counting diagram. This accepts prototypes, not the final course consumers.
  Detailed review: `_temp/svg_visual_language/VISUAL_REVIEW.md`.
- The provisional guide and small construction toolkit are accepted. ABO/bottleneck refinements
  pass standalone reviews; their eight-page contextual proof is independently accepted. Source investigation
  supports the now-accepted XX/XY chromosome-complement redraw.
- Six yeast drawings and one mouse-selection comparison passed independent art/context review
  and canonical integration through exactly seven image-URL substitutions. Full-root ODP/PDF
  exports and fourteen changed/adjacent pages were reviewed in `_temp/svg_yeast_mouse_final/REVIEW.md`.
  The inherited mouse placement remains tiny; its projected readability is not established.
- The pure-text DNA polarity question was faithfully transcribed as an editable SVG quote card,
  independently reviewed in `_temp/ocr_blockquote_export/QUALITY_REVIEW.md`, and integrated by
  one image-URL substitution. It is a visual card, not a native Djot blockquote; the original PNG
  remains. Canonical export is accepted at 47 source/ODP/PDF pages with zero hidden pages;
  slides 27-29 pass rendered review, exact embedded-SVG and native-paragraph checks. Receipt:
  `_temp/quote_pedigree_delivery/REVIEW.md`. The slide-2 capacity advisory is outside the art
  review and is not a confirmed clipping defect. Final suite verification is recorded below.
- Three first-cousin pedigree SVGs pass source/specification review and independent art review
  in `_temp/svg_cousin_pedigree_art/SPEC_REVIEW.md` and
  `_temp/quote_pedigree_delivery/PEDIGREE_ART_REVIEW.md`. The four-page LibreOffice placement
  proof preserves 16 native paragraphs and embeds the three exact accepted SVG payloads.
  Canonical integration changes exactly five image URLs on slides 45-48 of LECT15E; reversing
  those URLs restores the original source bytes. All original raster assets remain unchanged,
  all three SVGs match accepted hashes, and the source still parses to 61 slides. Receipt:
  `_temp/svg_cousin_pedigree_integration/HANDOFF.md`. Canonical source/ODP/PDF counts are
  61/61/61, and changed and adjacent pages passed rendered review. Prose, formulas, alt strings,
  layouts and markers are unchanged.
- The prior 49 suite failures in copied SVG tools and archived sources were repaired without
  extra engineering. Twelve historical `.djot.txt` source files remain byte-preserved; root MIT
  and copied LGPL notices are documented in `svg_tools/README.md`. The subsequent base suite
  passed 5973 tests with 2 warnings in 23.86s and zero tracked snapshot hash changes
  (`_temp/cleanup_final_review/`); that run predates tool pruning, quote integration and pedigree
  integration; the later final suite is recorded below.
  The subsequent pruning removes 36 unused copied tool files, their LGPL notice and unused
  `imagehash`, `shapely` and `tinycss2` requirements. All six original drawing helpers remain;
  six local recipes resolve their helper references and two focused tests pass. Receipt:
  `_temp/svg_tools_prune/RESULT.md`; original working-tree copies remain in its `before/` folder.
  Complex inversion work waits for tractable higher-payoff candidates. The existing 916-line
  `tests/test_layout_engine.py` advisory is nonblocking maintenance.

## Family survey handoff

Three completed reports under `_temp/svg_family_renewal/` establish the next focused families,
not a new broad plan or redraw quota. `survey_foundations_inheritance/REPORT.md` ranks
hemoglobin, corn and four-stage meiosis; `survey_linkage_variation/REPORT.md` ranks six-slot
yeast, inversion mechanisms and two active Morgan fly assets; `survey_population_shared/REPORT.md`
ranks mouse selection and CCR5, with first-cousin paths a later integration task. Chromosome
complements are a separate accepted assignment. Exact sources, edit boundaries, scientific
invariants, keep decisions and consumer limits are recorded in
[genetics_visual_workstreams.md](../workstreams/genetics_visual_workstreams.md) and its five
group briefs; detailed coverage is in
[genetics_illustration_reassessment.md](genetics_illustration_reassessment.md).

Surveys are read-only standalone comparisons, not canonical acceptance or final lecture proof.
Keep reviewed guide/helpers/ABO/bottleneck, original/empirical assets and native content;
classification CSVs remain unchanged. Shared Office Hours is visually suitable; outstanding
shared/cleanup exports are delivery tasks, not a reason to invent new art. Final accepted bytes
and actual export/review receipts update this ledger as each batch reaches delivery.

## Accepted four-family art batch

The four drawings and the ten-page original-voice proof pass independent integration review
at `_temp/svg_family_renewal/export/INTEGRATION_REVIEW.md`. The authoritative artifacts are
`export/exact_source/contextual_proof.{djot,odp,pdf}` under that same family-renewal directory:
10 source/ODP/PDF pages, 18 preserved native paragraphs and 12 exact embedded image payloads.
The reviewer inspected all ten pages and confirmed selectable native text. The corn quality
review also accepts the minor return-arrow contact as nonblocking; no polishing cycle is needed.

| Accepted drawing | Canonical consumer | Visible gain |
| --- | --- | --- |
| Chromosome complements | [lect11d_deletion_mechanisms.djot](../../../genetics/LECT11/djot/lect11d_deletion_mechanisms.djot), slide 23 | Aligned XX/XY complements with separate, countable shapes. |
| Folded hemoglobin | [lect02b-genes_dogma.djot](../../../genetics/LECT02/djot/lect02b-genes_dogma.djot), slide 44 | Recognizable folded subunits contrasted with a continuous clump. |
| CCR5 receptors | [lect14b-allele_freq.djot](../../../genetics/LECT14/djot/lect14b-allele_freq.djot), slide 10 | Three recognizable virus/membrane/receptor scenes with R5 HIV-1 scope inside the artwork. |
| Corn life cycle | [lect06c-meiosis.djot](../../../genetics/LECT06/djot/lect06c-meiosis.djot), slide 43 | Recognizable maize anatomy, two reproductive tracks and a closed developmental cycle. |

The [GENETICS_ILLUSTRATION_GUIDE.md](../../slide-specs/GENETICS_ILLUSTRATION_GUIDE.md)
remains the accepted provisional drawing reference. Exact candidate hashes and original source
comparisons remain in the integration review and four local artist handoffs.

The three native CCR5 wording qualifications in `export/contextual_proof.*` and
`ccr5_native_correction.diff` are **cancelled** after the instructor's scope clarification.
They were scratch-only, never canonical, and remain historical evidence only. The accepted
`exact_source/` proof preserves original native prose; its descriptive alt substitutions are
also unnecessary canonical changes.

`integrate_family_art_only` completed two existing SVG overwrites (hemoglobin and CCR5), two
new SVGs (chromosome and corn), and exactly two image-URL substitutions (chromosome and corn).
The four canonical files match accepted candidate hashes. Native prose, titles, alt text,
examples, layouts and sequence remain unchanged; the entire CCR5 Djot is byte-identical.
Original assets and the previous chromosome SVG remain available. The receipt is
`_temp/svg_family_renewal/integration/HANDOFF.md`, with `evidence.json`, `before_hashes.json`
and `source_urls_only.diff`. Four roots parse/compile to unchanged counts of 51 hemoglobin,
53 corn, 31 CCR5 and 112 chromosome slides; 16 capacity advisories are recorded without edits.
Canonical exports of all four owning roots and fresh final checks pass. Source/ODP/PDF counts
match at 112 chromosome, 51 hemoglobin, 31 CCR5 and 53 corn pages, with no hidden slides.
All 128 referenced images retain exact embedded bytes, including the four accepted SVGs;
18 native paragraphs match the accepted `exact_source/` proof. The ten changed/adjacent pages
pass visual review. The remaining 237 rebuilt pages were not individually visually reviewed;
known capacity advisories remain recorded and do not authorize unrelated fixes.

The fresh base suite passes **5324 tests, 2 warnings in 25.68s**, exit 0, with zero source/doc
mutations across 1,434 hashed files. This run precedes this documentation-only receipt.
Evidence is local under `_temp/svg_family_renewal/final_verification/`: `REVIEW.md`,
`artifact_evidence.json`, `pytest.log`, `pytest.status`, the four `build_*.log`/`build_*.status`
pairs and the pre/post source manifests and checks. Delivery preserves all original native
wording, with **zero CCR5 prose changes**; the cancelled scratch variant is not delivered.
Prior ABO/drift acceptance remains intact and the broader renewal goal remains open.

## Export and final checks

One owner runs LibreOffice outside the sandbox using repository scripts. Scratch experiment
exports establish only those examples. Course delivery still requires each changed consumer and
restored root with obsolete broad outputs, with changed/adjacent question and reveal pages
inspected at actual lecture size. Known dense placements include 04C SBEI, 14B CCR5, 14C flower/
curve figures, 15D stages and chemical labels. Use the five cleanup maps for exact page coverage.

Run the base suite after final implementation and inspect normalization mutations; the clean
maintenance run above is not a promise about later drawings. ODP/PDF inspection, attended
playback and instructor/learner acceptance remain separate. Historical native-table edit/reopen
proof is neither a new task nor a current creative acceptance criterion.

## Baseline and authority


- Setup owner: `/root/migration_setup`, model `gpt-6-astra` as explicitly requested by the user.
- Captured before source edits at 2026-11-10 01:48:01 UTC (2026-11-09 local date).
- Baseline covers 2,126 files: all 118 genetics Djot files, three shared evergreen Djot files,
  all genetics/evergreen assets, and every root/source/asset in the pilot's parsed inventory.
- Git status was clean at capture. The exact status is retained locally at
  `_temp/genetics_visual_renewal/setup/git_status_before.txt`.
- Local SHA-256 manifest: `_temp/genetics_visual_renewal/setup/source_asset_sha256_before.json`.
  Manifest SHA-256: `860a6244c31b2a7c03e33da8a502ee52c945a3ddf4ec3ea5e424608a744efb21`.
- Local capture metadata: `_temp/genetics_visual_renewal/setup/baseline_summary.json`.
- The historical plan and experiment files remain intact under `_temp/svg_migration_research/`.
  Scratch evidence is local and ignored; its literal paths do not promise GitHub availability.

Setup does not change course sources or assets. Hash baselines measure later changes; they do not
substitute for source/figure comparisons, rendered inspection, or evidence preservation.

## Historical M2 evidence

The following evidence describes the broader M2 milestone before D4-D5. It does not authorize
independent table work or current gene-tree integration. Electrophoresis, peas, cis/trans and
deletion drawings remain useful precedents; tree work is preserved for later use.

The historical M2 evidence covers 15 original SVGs across seven canonical roots and 62 inspected
changed/adjacent PDF pages. ODP/PDF counts, hidden states, native text/table contents and exact
packaged SVG bytes were checked. Original assets remain retained. Deletion table text, fill,
border and size were changed in a real LibreOffice scratch copy, saved, closed and reopened;
persisted edits and untouched neighbor styling passed. The canonical output was unchanged.

Accepted reviews and export evidence are local, ignored artifacts:

- M1 specification: `_temp/genetics_visual_renewal/review_m1_spec/REPORT.md`; accepted after
  correcting the original fourth tree's tip-order description to XZYW.
- M2 specification, `/root/m2_spec_review`:
  `_temp/genetics_visual_renewal/review_m2_spec/REPORT.md`; all five concepts accepted after
  final source/artifact freeze and corrective exports.
- Independent M1/M2 quality, `/root/m1_m2_quality_review`:
  `_temp/genetics_visual_renewal/review_m1_m2_quality/REPORT.md`; accepted, with no blocking
  finding or additional gate requested.
- Export owner `/root/m2_exports`: `_temp/genetics_visual_renewal/exports_m2/EXPORTS.md`,
  `manifest.json` and `HANDOFF.md`; seven final output pairs, exact page coverage, hashes,
  failed first-pass evidence and native edit/reopen proof. The handoff releases LibreOffice
  ownership with no export/client jobs or temporary listener remaining.

Owner handoffs and initial source maps remain indexed in
[genetics_visual_workstreams.md](../workstreams/genetics_visual_workstreams.md).
Final corrective/export reports supersede earlier layout dimensions and source hashes.
These were accepted milestone examples under the earlier scope, not current delivery acceptance.
Inherited placeholders and whole-root placement issues still need the relevant final delivery
review. Final course integration, attended playback and instructor/learner acceptance remain
separate.

## Provisional illustration guide handoff

- Visual-language owner `/root/illustration_guide` created
  [GENETICS_ILLUSTRATION_GUIDE.md](../../slide-specs/GENETICS_ILLUSTRATION_GUIDE.md), explicitly
  provisional and accepted by fresh specification and quality reviews. It explains shared ink/line hierarchy, selective
  detail, semantic color, subject-appropriate projection/light, live labels, original
  composition, source facts and editable SVG delivery through three durable illustrations.
- Durable examples are
  [gel_apparatus.drawn.svg](../../slide-specs/illustration_examples/gel_apparatus.drawn.svg),
  [drosophila_organic.drawn.svg](../../slide-specs/illustration_examples/drosophila_organic.drawn.svg)
  and [crossover_three_stage.drawn.svg](../../slide-specs/illustration_examples/crossover_three_stage.drawn.svg).
  They preserve the reviewed prototype content. The apparatus is byte-identical; the fly and
  crossover encode non-ASCII punctuation as numeric XML references. All three parsed SVG trees
  match their scratch sources, and those sources match the copies in the seven-page proof.
- Focused checks pass: guide/example ASCII, SVG XML, unique IDs, internal references, absence
  of raster/script/external resources, and guide local Markdown links. Fresh `rsvg-convert`
  renders at 1200 and 320 pixels match the source renders exactly. All six quality-90 WebP
  previews were opened and inspected: the apparatus, organic fly and ancestry diagram remain
  recognizable; lecture-size labels are unclipped. This equality verifies copying/encoding,
  not artistic quality. Earlier independent prototype review supplies the creative judgment.
- Local check receipt and previews: `_temp/genetics_illustration_guide/validation.json` and
  `_temp/genetics_illustration_guide/*_1200.webp` / `*_320.webp`. Prior review/export evidence:
  `_temp/svg_visual_language/VISUAL_REVIEW.md` and
  `_temp/svg_visual_language/export/evidence.json`. The guide links durable reports and uses
  literal paths for ignored local evidence so its committed links remain usable.
- The fly's occluded far hind leg is explicitly unsuitable for six-leg counting. Small labels
  need lecture-size display. Canonical lecture sources/art, construction toolkit and course
  exports were not changed by the guide author. No full suite or LibreOffice command ran for that documentation
  task; final placement, playback and instructor/learner acceptance remain unverified.
- ABO and bottleneck scratch refinement were dispatched separately. This guide handoff does
  not accept those drawings or claim overall renewal completion. Both fresh guide reviews accept
  the bounded guide and durable examples: `_temp/genetics_illustration_guide/SPEC_REVIEW.md` and
  `QUALITY_REVIEW.md`.

## Reviewed bounded art batch

- The manager releases the reassessment hold for this bounded batch under existing implementation
  authorization; no new permission gate is required. This does not accept a broad redesign or
  declare course completion.
- Construction specification and quality reviews accept `project()`, `cuboid()` and `cylinder()`
  with two focused tests passing. Existing serializer callers remain usable. The apparatus
  demonstrates recognizable connected volumes; sampled upright cylinders/tapers have the
  documented shallow/wide and zero-radius limits. Local reviews:
  `_temp/svg_creative_refinements/construction/{SPEC_REVIEW,QUALITY_REVIEW}.md`.
- ABO and all three bottleneck candidates pass separate standalone specification and quality
  reviews. ABO aligns each symbolic glycan and chemical chain in one row, preserving source
  topology and emphasizing the terminal sugar. Bottleneck art restores bottle recognition,
  irregular schematic beads and the cumulative two-falling-blue/five-blue-one-white outcome.
  Durable findings and exact scientific limits are in
  [genetics_illustration_reassessment.md](genetics_illustration_reassessment.md).
- The eight-page contextual proof covers ABO authored slides 8-10 and drift authored slides
  10-14. The export owner reports preserved native content/reveals and clean final placement.
  Reviewed drift corrections remove three review markers and three references to a fully
  transparent image; its asset remains retained. Evidence:
  `_temp/svg_creative_refinements/export/REVIEW.md` and `evidence.json`. Independent contextual
  review accepts the exact proof and bounded source edits in `INTEGRATION_REVIEW.md`. These
  scratch exports are not whole-course delivery.
- Canonical integration is complete: four SVGs match accepted candidates byte-for-byte; the
  drift edit removes exactly those six lines on authored slides 11-13. ABO Djot is unchanged;
  all other assets, including original rasters and the invisible spacer, are retained unchanged.
  Source counts remain 44 ABO and 35 drift slides. ASCII/XML, complete-source parsing/compiling,
  structural lint and scoped diff checks pass. Backups, hashes and exact delta are local at
  `_temp/svg_creative_refinements/integration/{HANDOFF.md,evidence.json,source.diff}`. Canonical
  full-root ODP/PDF rebuilds and the final base suite now pass, as recorded below.
- Chromosome source investigation supports XX/XY complements using the adjacent labeled inset
  and sex-dosage lecture. Each group has four large autosomes, two dots and two sex chromosomes.
  Applying direct source labels to the unlabeled comparison is an inference, explicitly recorded
  in the reassessment. The later accepted redraw is recorded above; no banding or scale is invented.
- Remaining course-wide art work and course delivery checks stay open. Standalone review, contextual
  export, canonical integration, attended playback and learner acceptance remain distinct.

## Final bounded batch verification

- The accepted guide/helper/art batch is complete. Canonical ABO and drift builds exit 0 with
  source/ODP/PDF counts of 44/44/44 and 35/35/35, respectively, and no hidden slides. This
  establishes the bounded batch, not whole-course creative renewal or delivery.
- Fresh base suite: **5324 passed, 2 warnings in 28.23s**, exit 0. The retained log's completion
  timestamp is `2026-11-09T21:27:38.398986-06:00` (America/Chicago filesystem modification time).
  That run precedes this documentation-only receipt; it is not a rerun of the receipt edits.
  The warnings concern AnyIO's deprecated import and the existing test-file length advisory.
- No source/document mutation occurred during the suite or builds across 1,432 hashed files.
  All 118 Genetics Djots are strict ASCII. All 612 Genetics SVGs parse as XML; the expanded
  authored-file check passes for 682 SVGs, including those 612 Genetics files.
- All 35 referenced images (32 unique payloads) are embedded byte-for-byte, including the four
  accepted SVGs. The 28 reviewed native paragraphs match the contextual proof; ABO slide 9
  retains live SVG labels rather than native Impress paragraphs. Reviewed PDF text is selectable.
- All eight changed/adjacent pages were individually inspected: ABO 8-10 and drift 10-14. No
  blocking clipping, collision, missing-glyph or replacement-overlay defect was found. Minor
  inherited label-size/open-space observations and the accepted bottleneck stage-size difference
  remain in the review. The other 71 rebuilt pages were not individually visually reviewed.
- Unrelated capacity advisories remain at ABO slides 2, 5 and 43 and drift slide 30. In particular,
  ABO 5 requests `@replaceme` because mixed content cannot fit within readability bounds. These
  out-of-batch pages are not newly accepted as visually sound.
- Exact local evidence directory: `_temp/svg_creative_refinements/final_verification/`.
  `REVIEW.md` records commands, page findings and limits; `artifact_evidence.json` records exact
  artifact/payload/native-text checks; `receipt_sha256.json` records receipt hashes. Suite evidence
  is `pytest.log` and `pytest.status`; build evidence is `build_abo.log`, `build_abo.status`,
  `build_drift.log` and `build_drift.status`. Source evidence is `pre_suite_source_sha256.json`,
  `post_suite_source_sha256.json`, `post_build_source_sha256.json`, `post_suite_checks.json`,
  `post_build_checks.json`, `post_build_mutations.json` and `authored_svg_checks.json`. Individual
  page WebPs are in the two consumer-named subdirectories. Evidence is local and ignored.
- This earlier batch left chromosome redraw and further families open; the four-family receipt
  above now records chromosome delivery. Further families and full-course exports remain open.
  Strict native Djot executable validation, attended Impress edit/save/reopen, Zoom/projection testing and
  instructor/learner acceptance were not performed. LibreOffice build ownership is released.

## Completed delivery checkpoint (2026-11-09)

- DONE: the DNA polarity quote card, three cousin-pedigree SVGs and SVG tool pruning. The
  quote retains native slide voice through one image URL; canonical source/ODP/PDF counts are
  47/47/47. The pedigree uses five image URLs and counts are 61/61/61. Six yeast drawings and
  the mouse comparison were delivered earlier in this ledger. The mouse's inherited tiny
  placement was not changed.
- DONE: `svg_tools/` retains `drawing.py` and `README.md`, with six helpers used by actual
  recipes. Thirty-six unused files and three unused dependencies were removed; backups are in
  `_temp/svg_tools_prune/`. Eight authored SVGs had 17 characters encoded as XML references;
  parsed XML remained exactly equal (`_temp/svg_ascii_finish/REVIEW.md`).
- Final base suite after pruning and integration: 5656 passed, 2 warnings in 22.99s, with zero
  mutations across 1167 tracked files. Strict ASCII/XML checks passed for 118 Genetics Djot
  files and 275 authored SVGs. The earlier 5973-test receipt predates pruning and integration.
  Full evidence, canonical artifact links and rendered reviews: `_temp/overnight_art_delivery/REVIEW.md`.
- DONE_WITH_CONCERNS: existing display limits remain, including the mouse's tiny placement,
  the pedigree's inherited marker and capacity advisories, and two reviewed pedigree pages
  below the font policy floor. Projection and whole-deck review were not performed.
- OPEN: the broader all-lecture art goal, Genetics first. The second challenge quote and
  Biotechnology artwork have advanced beyond this completed batch, as recorded below.

## Prior Biotechnology delivery checkpoint

- The second challenge quote passes independent proof review and is installed through exactly
  one image URL in `genetics/LECT03/djot/lect03g-chap2_challenges.djot`, authored slide 3.
  `assets/lect03g-chap2_challenges/challenge-problem-2.drawn.svg` matches the accepted SVG;
  the original `image_001.png`, source typo, alt text and remaining source bytes are preserved.
  Evidence: `_temp/challenge_quote_integration/HANDOFF.md`, with exact hashes and URL-only diff;
  proof acceptance: `_temp/challenge_quote_quality/REVIEW.md` and
  `_temp/challenge_quote_export/REVIEW.md`. Canonical export is complete, as recorded below.
- Nine original Biotechnology drawings pass independent source/art review at
  `_temp/biotech_art_source_review/REVIEW.md`. Insulin has four states replacing five raster
  paths across eight uses; frozen art and maps are in `_temp/svg_insulin_art/`.
  Chromatography has five drawings across 37 uses; frozen art and maps are in
  `_temp/svg_chromatography_art/`. Canonical integration installs ten SVG files containing
  those nine artworks and changes exactly 45 image URLs in three physical sources. URL reversal
  restores every original source byte; original rasters and native voice remain unchanged.
  Evidence: `_temp/biotech_art_integration/HANDOFF.md` and `checks.json`.
- Paired original/candidate proofs from actual source contexts have matching source/ODP/PDF
  counts: chromatography 27/27/27 and insulin 7/7/7, with zero hidden pages. Native paragraphs
  match exactly and accepted image payloads are embedded byte-for-byte. Evidence:
  `_temp/biotech_art_export/source_checks.json` and `artifact_checks.json`; paired page renders
  are in `chromatography_pairs/` and `insulin_pairs/` beneath that directory.
- Fresh contextual review accepts both families across all 34 actual-source candidate pages:
  `_temp/biotech_art_context_quality/REVIEW.md`. Inherited small panels remain recap illustrations;
  fine labels require the existing large-figure pages or PDF zoom. This is not a claim that
  inset labels are readable at audience distance or after screen-sharing compression.
- **DONE_WITH_CONCERNS:** all three canonical builds exit 0. Source/ODP/hidden/PDF counts are
  11/11/0/11 for the challenge quote, 390/390/6/384 for Biotechnology LECT04 and 281/281/0/281
  for LECT06. All 46 accepted SVG placements are verified. The 35 changed and two quote-adjacent
  contexts match proof native paragraphs, frame geometry, image payloads and selectable PDF
  text. Twenty-two representative canonical pages were visually inspected, four individually.
  Full receipt and artifact paths/hashes: `_temp/biotech_art_delivery/REVIEW.md` and
  `artifact_checks.json`. LibreOffice ownership is released.
- Fresh exact base suite: **5678 passed, 2 warnings in 22.39s**, with zero changes across 1054
  monitored files during suite/builds. Exactly eleven accepted SVG files were staged; other
  index entries were unchanged. This documentation-only receipt follows that suite. The earlier
  5656-test receipt remains evidence for its prior batch.
- Inherited chromatography inset labels around 3.7-4 pt, smaller charge marks, small insulin
  labels and existing capacity advisories remain. No whole-deck visual audit, attended playback,
  Zoom or learner validation is claimed. The broader all-lecture art goal remains open.

## Current division artwork checkpoint

- **ACCEPTED:** three unequal-crossing drawings across four LECT11E uses and four meiosis
  sequence drawings across four LECT06C uses. Fresh source/art review accepts all seven frozen
  SVGs at `_temp/genetics_division_source_review/REVIEW.md`; artist files and exact maps remain
  in `_temp/svg_unequal_crossing_art/` and `_temp/svg_meiosis_sequence_art/`.
- Independent contextual review accepts all 22 actual-source candidate pages at
  `_temp/genetics_division_context_quality/REVIEW.md`. Paired original/candidate proofs contain
  10/10/10 source/ODP/PDF pages for unequal crossing and 12/12/12 for meiosis, with no hidden
  pages. All seven accepted hashes and eight uses match; native prose, host alt text, captions,
  layouts, markers and sequence remain unchanged. Every SVG label remains selectable in PDF.
  No new clipping, cropped label or import defect is reported. Export receipt:
  `_temp/genetics_division_export/REVIEW.md`. LibreOffice ownership is released.
- **INTEGRATED:** seven exact accepted SVGs and eight image-URL substitutions in
  [lect11e-chromo_alter_2-duplications.djot](../../../genetics/LECT11/djot/lect11e-chromo_alter_2-duplications.djot)
  and [lect06c-meiosis.djot](../../../genetics/LECT06/djot/lect06c-meiosis.djot).
  Reversing those URLs restores both original source byte streams. All 98 preexisting assets
  remain byte-identical; words, alt text, layout directives, reveal markers and sequence are
  unchanged. The roots still parse to 37 and 53 slides respectively, with zero hidden slides.
  Exact promotion and preservation evidence: `_temp/genetics_division_integration/HANDOFF.md`
  and `integration_hashes.json`.
- **DONE_WITH_CONCERNS:** both canonical builds exit 0. Source/ODP/hidden/PDF counts are
  53/53/0/53 for LECT06C and 37/37/0/37 for LECT11E. All seven accepted SVG hashes and eight
  placements match. All 22 accepted new proof contexts match canonical native paragraphs,
  frame geometry, image payloads and selectable PDF text. All eight changed canonical pages
  and two adjacent pages were opened at 1800 px; no new artwork defect was found. Receipt:
  `_temp/genetics_division_delivery/REVIEW.md` and `final_receipt.json`, with artifact paths
  and hashes in `canonical_checks.json`. LibreOffice ownership is released.
- Fresh exact base suite: **5692 passed, 2 warnings in 24.98s**, with no tracked-file mutations
  during builds/tests. Only the seven accepted SVGs were staged; other index entries remain
  unchanged. This documentation-only receipt follows that run. The prior 5678-test receipt
  remains evidence for the Biotechnology/challenge-quote batch. The provisional
  [GENETICS_ILLUSTRATION_GUIDE.md](../../slide-specs/GENETICS_ILLUSTRATION_GUIDE.md) adds one
  canonical meiosis example alongside the retained equipment and crossover examples.
- Fine anatomy labels and spindle/centromere detail require the large lecture view; inherited
  dense context and raster neighbors remain. No attended playback, Zoom or learner validation
  is claimed. This bounded acceptance does not complete the broader all-lecture artwork goal.

## Ordered and prenatal delivery checkpoint

- **INTEGRATED:** three final ordered-tetrad SVGs in
  `_temp/svg_ordered_tetrads_art/` pass source/art review at
  `_temp/ordered_prenatal_source_review/REVIEW.md` and actual-context quality review at
  `_temp/ordered_prenatal_context_quality/REVIEW.md` across ten pages. The three source uses are
  LECT09H `lect09h-ordered_tetrads_centromeres.djot` lines 91/103/115; the full root has 31 slides
  and zero hidden slides. Exactly three image-URL substitutions install the accepted art;
  reversing them restores all original source bytes. All 155 preexisting assets are unchanged.
  `_temp/ordered_tetrad_integration/HANDOFF.md` and `CHECKS.json` record the completed integration.
- **INTEGRATED:** the two selected prenatal landscape SVGs in `_temp/svg_prenatal_landscape_art/`
  pass fresh source review at `_temp/prenatal_landscape_source_review/REVIEW.md` and actual-slide
  quality review at `_temp/prenatal_landscape_quality/REVIEW.md`. The four-page actual export
  at `_temp/prenatal_landscape_export/REVIEW.md` and `final_checks.json` confirms the gain:
  main labels increase from 8.529/8.204 pt to 13.394 pt (57%/63%); anatomy enlarges 72%/79%.
  Source words, branches, timings and native content remain unchanged. Accepted portrait
  parents remain unchanged and unpromoted in `_temp/svg_prenatal_sampling_art/`.
- Exactly two URL substitutions install the landscape pair in LECT10D
  `lect10d-chromo_aneuploid.djot`, lines 696/704, authored slides 53/54. URL reversal restores
  all original source bytes; all 105 preexisting assets remain unchanged. The root still parses
  to 63 slides with zero hidden slides. `_temp/prenatal_landscape_integration/HANDOFF.md` and
  `checks.json` record promotion. Native voice, layout and prose are preserved; no clinical
  update is in scope. The provisional
  [GENETICS_ILLUSTRATION_GUIDE.md](../../slide-specs/GENETICS_ILLUSTRATION_GUIDE.md) adds this
  wide-area composition example without establishing a global font-size rule.
- The accepted proof contexts cover ten ordered and four selected prenatal pages for five
  placements. The original paired proofs remain at `_temp/ordered_prenatal_export/REVIEW.md`;
  the selected landscape proof supersedes only its prenatal candidate.
- **DONE_WITH_CONCERNS:** canonical source/ODP/hidden/PDF counts are 31/31/0/31 for ordered
  tetrads and 63/63/0/63 for prenatal sampling. All five accepted SVGs appear exactly once in
  their intended places. All fourteen accepted new proof contexts match canonical native words,
  notes, frame geometry, image payloads, selectable text and rendered hashes. All 172 SVG labels
  remain selectable. The reviewer opened all five changed pages and four neighbors; no new
  cropping, lost branch or title collision was found. Canonical prenatal labels confirm
  13.394 pt and the selected landscape gain. All 260 preexisting assets and portrait parents
  remain unchanged. Receipt: `_temp/ordered_prenatal_delivery/REVIEW.md` and `final_checks.json`;
  artifact paths/hashes are in `artifact_hashes.json`. LibreOffice ownership is released.
- Fresh exact base suite: **5702 passed, 2 warnings in 22.94s**, with zero mutations across
  1190 tracked files. Only the five authorized SVGs were staged; all other index entries remain
  unchanged. This documentation-only receipt follows that run. The **5692-test** receipt above
  remains evidence for the earlier seven-artwork division batch.
- Dense ordered-mitosis fine text and pair brackets require the large view; reduced Zoom or
  projector readability remains untested. Existing prenatal capacity advisories on slides 11
  and 57 remain outside this artwork change. No attended playback or learner acceptance is
  claimed. This bounded delivery is complete; the broader all-lecture artwork goal remains open.
  Checkpoint backups, hashes and bounded checks are in `_temp/ordered_prenatal_checkpoint/`.

## Inversion and fuel artwork checkpoint

- **ACCEPTED:** five inversion drawings pass source/art review at
  `_temp/inversion_loop_source_review/REVIEW.md`; two final fuel-cell compatibility copies pass
  `_temp/fuel_cell_compatibility_review/REVIEW.md`. Frozen candidates remain in
  `_temp/svg_inversion_loop_art/` and `_temp/svg_fuel_cell_compat_art/` respectively.
- Fresh contextual review accepts all seven drawings at
  `_temp/inversion_fuel_context_quality/REVIEW.md`. Paired actual-source exports contain
  14/14/0/14 source/ODP/hidden/PDF pages per inversion variant and 6/6/0/6 per final fuel
  variant: forty paired pages, seven candidate placements and 156 selectable SVG text elements.
  Native paragraphs, notes, tables, markers and non-target image payloads are preserved.
  Export receipt: `_temp/inversion_fuel_export/REVIEW.md`. LibreOffice ownership is released.
- Only `fuel_final_{original,candidate}.{djot,odp,pdf}` are the accepted fuel proofs. Earlier
  `fuel_candidate.*` exports rendered both drawings blank with `encoding="ASCII"`. A controlled
  declaration-only UTF-8 probe isolated the import issue; final copies retain ASCII bytes and
  identical parsed XML. Fresh compatibility and contextual reviews accept those final copies.
  Failed proofs, the diagnostic probe and original candidates remain historical evidence.
- Inversion target proof slides 2/6/8/10/12 map to root slides 8/12/14/16/18 in
  [lect13b-chromo_alter_3-inversion.djot](../../../genetics/LECT13/djot/lect13b-chromo_alter_3-inversion.djot).
  Fuel proof slides 3/4 map to root slides 59/60; physical URLs are in
  [set4_chapter_12.djot](../../../biotech/LECT06/djot/set4_chapter_12.djot), included by
  [lect06c-set_4_tp_chapter_12_16_material.djot](../../../biotech/LECT06/djot/lect06c-set_4_tp_chapter_12_16_material.djot).
  Companion image 012, including both microscopy insets, remains unchanged.
- **DONE_WITH_CONCERNS for contextual review:** protected inversion overlays obscure primary
  proof pages 8/10 and unchanged neighbor 4. Separate exact-frame diagnostics establish the
  underlying artwork's fit without authorizing marker removal. Half-width overview fine text
  is 6.61 pt and small composite A labels are 4.86 pt; larger viewing remains necessary.
  One inherited arrow extracts after its gene sequence but is visually present and selectable.
- **INTEGRATED:** seven accepted SVG additions and exactly seven image-URL substitutions across
  the two physical sources. Reversing those URLs restores every original source byte; full-root
  parsed models also match after reversing only those image sources. Native voice, prose, alt
  text, layouts, markers, tables, microscopy and prior insulin art remain unchanged. All 132
  preexisting assets retain their hashes. Receipt: `_temp/inversion_fuel_integration/HANDOFF.md`.
- **DONE_WITH_CONCERNS:** both canonical builds exit 0, with source/ODP/hidden/PDF counts of
  48/48/0/48 for inversion and 281/281/0/281 for fuel. All seven accepted SVGs occur exactly
  once in the intended positions. All twenty accepted new-proof contexts match canonical native
  paragraphs, notes, frame geometry, image payloads and selectable PDF text; all 156 SVG text
  elements remain selectable. All seven changed pages were opened individually and all twenty
  contexts inspected through contact sheets, with no visible fit regression.
- Nine of twenty canonical WebPs match proof bytes exactly. The other eleven inversion renders
  have small documented differences, with mean absolute channel delta 0.069-0.299 on a 0-255
  scale; these renders are not byte-identical. Canonical overlays remain on inversion slides
  10/14/16. Fine labels and inherited capacity advisories remain concerns. Receipt and exact
  artifact hashes: `_temp/inversion_fuel_delivery/REVIEW.md`, `final_checks.json` and
  `artifact_hashes.json`. LibreOffice ownership is released.
- Fresh exact base suite: **5716 passed, 2 warnings in 23.16s**, exit 0, with zero tracked-file
  mutations. Exactly seven accepted SVGs were staged; all preexisting index entries remain
  intact. This documentation-only receipt follows that run. The 5702-test receipt above remains
  evidence for the completed ordered/prenatal batch. No new suite or export ran for this receipt.
- This batch is complete; no artwork remains pending in its queue. The broader all-lecture
  artwork goal remains **OPEN**. No wider whole-deck audit, attended playback, Zoom or learner
  acceptance is claimed. Checkpoint snapshots and bounded documentation checks are in
  `_temp/inversion_fuel_checkpoint/`.

## Animal and gamete delivery

All four drawings are **ACCEPTED for source/art and actual-context quality**. The original
source review is `_temp/animal_gamete_source_review/REVIEW.md`; the final human bytes have
a separate source-scope acceptance in `_temp/human_cycle_compat_source_review/REVIEW.md`.
Artist handoffs and frozen hashes remain in `_temp/svg_animal_human_cycle_art/` and
`_temp/svg_oogenesis_gametogenesis_art/`.

| Root slide | Source line | Original asset | Integrated drawing |
| --- | --- | --- | --- |
| 39 | 483 | `image_027.jpg` | `mouse_life_cycle.drawn.svg` |
| 40 | 490 | `animal_life_cycle.svg` | `human_life_cycle.drawn.svg` |
| 41 | 508 | `oogenesis.svg` | `oogenesis.drawn.svg` |
| 42 | 515 | `image_030.png` | `gametogenesis_comparison.drawn.svg` |

All four integrated uses are in
[lect06c-meiosis.djot](../../../genetics/LECT06/djot/lect06c-meiosis.djot), with assets in
`genetics/LECT06/djot/assets/lect06c-meiosis/`. The two original SVGs wrap raster content.
The source reference remains `genetics/LECT06/lect06c-meiosis.odp`. Native voice, content,
alt text, markers, layout and sequence remain protected; this batch makes no global science
or prose corrections.

The first combined actual-source proof of root slides 38-43 is complete in
`_temp/animal_gamete_export/REVIEW.md`: six source/ODP/PDF pages, zero hidden pages and 49
selectable SVG text elements, with frozen inputs and native content preserved. The original
exporter has released LibreOffice ownership.

Initial independent review in `_temp/animal_gamete_context_quality/REVIEW.md` accepted mouse,
detailed oogenesis and the gametogenesis comparison, but required a human export correction:
diagonal skin bands appeared in LibreOffice/PDF output while standalone skin was smooth.
The original striped proof and unsuccessful percentage-gradient probe remain as evidence.

The final human in `_temp/svg_human_cycle_compat_art/` changes exactly four skin fills to
existing palette solids; all other bytes, including anatomy, text and routes, are preserved.
Accepted SHA256: `20017be3d097f3ec98602455dde8beba2a2e9176aba193d34066d2fdf4faed44`.
This is a demonstrated scoped compatibility workaround, not a diagnosis of the renderer cause.
Fresh review in `_temp/human_cycle_compat_context_review/REVIEW.md` accepts the final combined
six-page proof in `_temp/animal_gamete_compat_export/animal_candidate.odp` and
`animal_candidate.pdf`: bands are gone, all 49 SVG labels remain selectable, and native content,
frames, both neighbors and the other three accepted drawings are preserved.

Canonical source/art integration is **DONE** in
`_temp/animal_gamete_integration/HANDOFF.md`: exactly four accepted SVG additions and four
image URL substitutions at the lines above. All 70 preexisting assets are unchanged. Reversing
only those URLs restores both source bytes and the complete parsed model; the root retains
53 authored slides and zero hidden slides. The integrated human is the final flat-skin version.
Post-integration source SHA256:
`c5f630857b5e2cc6344309cbd3d1ea23e8889a9d0ed8dab71cba9d43ed5534eb`.

Canonical delivery is **DONE_WITH_CONCERNS** in `_temp/animal_gamete_delivery/REVIEW.md` and
`final_checks.json`. The full-root build passes with source/ODP/hidden/PDF counts of
53/53/0/53. All four exact accepted SVG payloads occur once on pages 39-42. All six canonical
contexts match the selected final new proof in native paragraphs and referenced styles, notes,
frames, image signatures and selectable text; all 49 SVG text elements remain selectable.
All six canonical pages were viewed individually. Human skin is smooth without bands, and
half-width oogenesis labels fit. Fine detail still requires the full slide view.

Five of six canonical WebPs match the accepted proof bytes exactly. The human raster hash
differs, but direct visual and signature checks show no meaningful fit or content change;
the human renders are not byte-identical. The sole delivery concern is the inherited,
unchanged slide 37 capacity advisory, outside this four-artwork batch.

Fresh exact base suite: **5724 passed, 2 warnings in 23.46s**, exit 0, run once. Build and suite
produce zero tracked-file mutations. All 70 original assets, frozen receipts and three frozen
documentation files remain intact through those checks. Exactly four accepted SVG additions
are staged; other index entries remain unchanged. LibreOffice ownership is released.
This documentation-only receipt follows the run; no suite, export or index operation runs for it.

The earlier **5716 passed, 2 warnings in 23.16s** receipt remains evidence only for the completed
seven-artwork inversion/fuel batch. This four-artwork batch is complete, with no new queue.
The broader all-lecture artwork goal remains **OPEN**. No whole-deck visual/scientific audit,
interactive playback, Zoom/projection or learner acceptance is claimed. Initial queue evidence
remains in `_temp/animal_gamete_art_checkpoint/`; documentation snapshots, diffs, hashes and
scoped checks are in `_temp/animal_gamete_delivery_checkpoint/`. The pre-delivery documentation
freeze is retained there alongside this final receipt.

## Ames, checkpoint and Neurospora delivery

The bottle, algae and liposome batch is complete; its five-drawing delivery receipt below
remains unchanged. All three new drawing packages are frozen and independently **ACCEPTED
for source/art specification**: seven target figures and seven current uses across three roots.
Independent actual-context review accepts all seven placements. Canonical source integration,
full-root builds and final checks are complete: **DONE_WITH_CONCERNS**.

Exact source-preservation and dispatch contracts remain in
`_temp/remaining_art_selection/genetics/REPORT.md`
and
`_temp/remaining_art_selection/biotech/REPORT.md`.
These completed selections are **DONE_WITH_CONCERNS**, not a redraw quota.

- Ames: one apparatus drawing and one use in Biotechnology LECT10. Frozen package:
  `_temp/svg_ames_assay_art/HANDOFF.md` and
  `_temp/svg_ames_assay_art/freeze.json`.
  Candidate `ames_comparison.drawn.svg` SHA256:
  `3edd066fb1583ce1b51935451953c1684c76f85f74ab738c7a10682e4090a9df`.
- Checkpoint gates: five drawings and five uses on three Genetics LECT06 slides.
  Frozen package:
  `_temp/svg_checkpoint_gate_art/HANDOFF.md`,
  `_temp/svg_checkpoint_gate_art/freeze.json`
  and `_temp/svg_checkpoint_gate_art/context_map.json`.
  The overview and G1/M stop/go states preserve their existing captions and native prose.
- Neurospora: one mixed illustration and one use in the Genetics LECT09 ordered-tetrad root.
  Frozen package:
  `_temp/svg_neurospora_cycle_art/HANDOFF.md`,
  `_temp/svg_neurospora_cycle_art/FREEZE.json`
  and `_temp/svg_neurospora_cycle_art/BOUNDARY.json`.
  Intended `neurospora_life_cycle.svg` SHA256:
  `23ff21abf867f6760a0a20ee26b3a52af13475c6519488a8c28d2585feea4d3e`.
  Separate pure `neurospora_life_cycle.drawn.svg` SHA256:
  `622b81cbec5476b0bf9cdd808354947d6cb1307d1cbae29c1798bb3ff3f9bb72`.

Independent source/art review accepts all three families in
`_temp/ames_checkpoint_neurospora_source_review/REVIEW.md`.
The empirical boundary is **ACCEPTED**: the complete 470 x 478 photo rectangle at half-open
bounds `[1668, 4, 2138, 482]` retains every original RGBA pixel. Its embedded PNG file bytes
also equal the retained crop file. The pure drawing contains zero images; the intended ordinary
mixed SVG contains exactly that one photograph. This composition follows existing
[SVG_DIAGRAMS.md](../../slide-specs/SVG_DIAGRAMS.md); no exception or new policy is needed.
Original assets remain retained.

Independent actual-context review accepts all seven drawings in
`_temp/ames_checkpoint_neurospora_context_quality/REVIEW.md`.
Serialized original/candidate proofs cover three Ames, six checkpoint and three Neurospora
contexts per variant: 24 PDF pages, all twelve paired contexts viewed individually, followed
by all five changed candidate pages. Native paragraphs, notes, frame geometry and non-target
images remain unchanged. All 99 SVG text elements remain selectable: 21 Ames, 52 across the
five checkpoint drawings and 26 Neurospora. Exact export evidence is in
`_temp/ames_checkpoint_neurospora_export/REVIEW.md`.
LibreOffice ownership is released after the proof exports.

Actual-context acceptance retains minor nonblocking concerns: Ames has a plain experimental
incubation connector beside the control arrowhead, and the Neurospora loop arcs touch the
beginnings of their lower captions. Fine signs, spindle fibers and cycle labels need the
larger lecture view. The retained Neurospora photo pixels and PNG bytes remain exact in the
SVG and actual ODP. Normal PDF export resamples it to a 141 x 144 JPEG with a separate alpha
mask; its observed field and teaching function remain recognizable. Detailed empirical
inspection uses the retained source, SVG or ODP. PDF pixel/byte equality is not claimed.

Canonical source integration passes in
`_temp/ames_checkpoint_neurospora_integration/HANDOFF.md`.
Eight exact accepted SVG files cover seven target figures: Ames, five checkpoint drawings,
and both the separate pure Neurospora drawing and its intended mixed composition. The mixed
SVG embeds its photograph; no external PNG dependency is added. Exactly seven image URLs
change in three physical Djot files. URL reversal restores complete source bytes and parsed
models. All 89 preexisting assets and eleven other included source dependencies are unchanged.
Fresh source counts are Biotechnology medicinal 244/zero hidden, Genetics cells 24/zero hidden
and Genetics ordered tetrads 31/zero hidden. Native prose, titles, alt text, notes, layouts,
markers, reveals, states, sequence and voice remain protected.

Canonical delivery passes in `_temp/ames_checkpoint_neurospora_delivery/final_checks.json`.
Source/ODP/hidden/PDF counts are 244/244/0/244 for Biotechnology medicinal, 24/24/0/24 for
Genetics cells and 31/31/0/31 for Genetics ordered tetrads. All twelve accepted proof contexts
match native paragraphs, notes, frame geometry, non-target payloads and selectable text.
All 99 SVG text elements remain selectable; all 32 native paragraph XML structures and their
referenced styles match after page-ID mapping. All seven target payload placements are exact.
Every changed and neighboring context was inspected. Nine of twelve canonical renders match
proof bytes: all three Ames and six checkpoint pages. The three Neurospora renders differ
without meaningful visual or signature changes. The exact retained photo remains in SVG/ODP;
the normal PDF representation remains the accepted 141 x 144 JPEG with alpha mask.

The first exact `source source_me.sh && pytest tests/` run reported **1 failed, 5750 passed,
2 warnings in 23.34s**. Fourteen newly added Markdown links pointed to ignored `_temp` evidence,
which the Git-browsable link check correctly rejected. Converting only those links to inline
path references preserved their wording and all historical receipts. The affected ledger
parameter then passed: **1 passed, 1 warning in 0.44s**. The exact base command ran again:
**5751 passed, 2 warnings in 24.59s**, exit 0. Both suite runs and the focused check have zero
tracked-file mutations; canonical builds also have zero tracked-file mutations. Failed-run
logs, the original documentation freeze and the corrected freeze remain available.
The **5734 passed** result below covers only the completed previous five drawings.

All 313 integration-frozen files, four corrected frozen documents, 89 original assets and
eleven other source dependencies remained intact through delivery. Only the eight exact
accepted SVG additions entered the index; other index entries stayed unchanged. Thirteen
preexisting cached EOF whitespace warnings remained unchanged; scoped worktree/index whitespace
checks passed. LibreOffice ownership is **RELEASED**, with no export process remaining.

Delivery is **DONE_WITH_CONCERNS** for the accepted Ames connector asymmetry, Neurospora
loop-caption proximity, fine-detail viewing scale, PDF photo resampling and unchanged
full-root capacity advisories. No attended slideshow/Zoom playback, learner acceptance or
whole-deck science/clinical-prose audit is claimed. This batch is complete.

Gene trees remain out of scope; `@replaceme` does not govern selection. No new migration plan
or global audit is added. The broader all-lecture artwork goal remains **OPEN**.
Initial queue evidence remains in `_temp/ames_checkpoint_neurospora_queue/`; source-art,
pre-delivery and final snapshots, diffs, hashes and scoped documentation checks are in
`_temp/ames_checkpoint_neurospora_checkpoint/`. The original `pre_delivery_freeze.json`,
`corrected_pre_delivery_freeze.json` and final documentation receipt remain separate.
Required changelog rotation keeps November 10 and November 9 active and preserves every older
byte in [CHANGELOG-2026-11a.md](../../CHANGELOG-2026-11a.md); existing archives are unchanged.
This documentation-only final receipt follows the successful suite and runs no new exports,
pytest commands or index actions.

## Bottle, algae and liposome delivery

**DONE_WITH_CONCERNS; canonical delivery complete.** Five original SVGs cover
eight uses: one allele bottle in Genetics LECT15, one algae-fuel scene in Biotechnology
LECT06, and three liposome drawings across six Biotechnology LECT10 uses. Independent source
review is `_temp/bottle_algae_liposome_source_review/REVIEW.md`; the therapy-only correction
is accepted in `_temp/liposome_therapy_leader_source_review/REVIEW.md`.

The final therapy derivative is `_temp/svg_liposome_therapy_leader_fix/liposome_therapy.drawn.svg`,
SHA256 `55d9140eb1dce9537397953ea46b0f9544329ef5de97d0be4eaf200249510e01`.
Only its plasmid-label leader changed: it now paints above the vesicle and ends on the
plasmid in the aqueous core. Parent artwork and the other four accepted drawings are intact.
Original handoffs remain in `_temp/svg_allele_bottle_art/`, `_temp/svg_algae_fuel_art/` and
`_temp/svg_liposome_delivery_art/`.

Independent actual-context review accepts all five drawings and eight placements in
`_temp/bottle_algae_liposome_context_quality/REVIEW.md`. Paired original/candidate proofs
cover fourteen actual contexts per variant, with all 28 PDF pages inspected. Bottle and
algae each contribute three contexts; liposomes contribute eight, including all six changed
half-width/big-image uses. Export evidence in `_temp/bottle_algae_liposome_export/REVIEW.md`
verifies native text, notes, frame geometry, non-target images and selectable SVG labels:
five bottle, fourteen algae, and eleven/eighteen/twenty-three for each liposome drawing.
The liposome labels remain selectable in each reuse. LibreOffice ownership is released.

Fresh parsed root counts are Genetics LECT15 77 authored/one hidden, Biotechnology LECT06
281/zero hidden, and Biotechnology LECT10 244/zero hidden. Bottle targets authored48 /
visible47; algae targets126; liposome uses target47-52. The historical 235-slide LECT10 count
is not the current root. These are source/proof checks, not canonical full-root build results.

The review status is **DONE_WITH_CONCERNS**: fine liposome labels and the long therapy
sentence need their preserved adjacent big-image reading views, which were also inspected.
The inherited bottle-neighbor overlay remains unchanged. Entry retains source-specific direct
fusion; therapy retains both routes and its complete expression pathway. Native prose,
titles, alt text, layouts, markers, reveals, states, photographs and data remain protected;
clinical/prose reconciliation and a global science audit are outside this artwork batch.

Integration is **DONE_WITH_CONCERNS** in
`_temp/bottle_algae_liposome_integration/HANDOFF.md`: five exact SVGs copied and exactly eight
URL spans changed in three physical Djot files. Reversing those URLs restores complete source
bytes and parsed models. All 151 preexisting assets and eighteen other source dependencies
are unchanged. Corrected therapy, not the rejected parent, is canonical. Source counts remain
77/one hidden/76 visible, 281/zero hidden/281 visible and 244/zero hidden/244 visible.

Fresh canonical delivery passes in `_temp/bottle_algae_liposome_delivery/REVIEW.md` and
`final_checks.json`. Source/ODP/hidden/PDF counts are 77/77/1/76 for Genetics LECT15,
281/281/0/281 for Biotechnology LECT06 and 244/244/0/244 for Biotechnology LECT10. All
fourteen reviewed contexts match accepted new-proof native paragraphs, notes, geometry,
payloads and selectable text. All 123 SVG text-line instances remain selectable across the
eight placements. Every changed placement and supplied adjacent context was inspected; the
corrected therapy leader reaches the core plasmid in both views. Twelve of fourteen renders
match proof bytes; two bottle renders differ without meaningful visual or signature changes.

The exact base command `source source_me.sh && pytest tests/` ran once after canonical builds:
**5734 passed, 2 warnings in 28.49s**, exit 0. Build and test tracked-file mutations are both
empty. Only five accepted SVG additions were staged; other index entries stayed unchanged.
All 151 old assets, eighteen other dependencies, integration frozen inputs and three frozen
documents remained intact through delivery. LibreOffice ownership is **RELEASED**.

Delivery is **DONE_WITH_CONCERNS** for inherited viewing limits: fine half-width liposome
labels use the preserved adjacent big-image views, the bottle neighbor retains its overlay,
and algae's preceding slide retains a low bottom text margin. Unchanged full-root capacity
advisories remain outside this artwork batch. No live slideshow/Zoom playback, learner
acceptance or clinical/prose reconciliation is claimed.

This final documentation-only receipt follows the completed suite and invokes no new tests,
exports or index actions. Before/after snapshots, diffs, hashes and scoped ASCII/relative-link/
diff checks are in `_temp/bottle_algae_liposome_checkpoint/`; `pre_delivery_freeze.json`
retains the earlier documentation freeze and `final_checks.json` records the final update.
The prior **5724 passed, 2 warnings in 23.46s** animal/gamete receipt remains unchanged.
This five-drawing batch is complete; the broader all-lecture artwork goal remains **OPEN**.
No new drawing queue was assigned at that delivery checkpoint; the current queue is above.

## Fly, cycle and industrial queue

Current dispatch checkpoint, 2026-11-10: **six scratch artists, eight target figures and
eight current uses across three roots**. Frozen selections are complete in
`_temp/next_raster_selection/genetics/REPORT.md` (three families, four uses) and
`_temp/next_raster_selection/biotech/REPORT.md` (three families, four uses), with
`_temp/next_raster_selection/biotech/ethanol/REPORT.md`,
`_temp/next_raster_selection/biotech/wells/REPORT.md` and
`_temp/next_raster_selection/biotech/cellulosome/REPORT.md` supplying the industrial briefs.
This is selection and drawing status; no candidate acceptance or delivery is claimed.

The six scratch-only owners and their complete target sets are:

- `/root/drosophila_sex_clipart`: `_temp/svg_drosophila_sex_art/`;
  `image_003.png` -> `drosophila_female_male.drawn.svg`.
- `/root/morgan_eye_cross_clipart`: `_temp/svg_morgan_eye_cross_art/`;
  `morgan_cross_experiment.svg` -> `morgan_cross_experiment.drawn.svg` and
  `morgan_cross_chromosomes.svg` -> `morgan_cross_chromosomes.drawn.svg`.
- `/root/sexual_cycle_comparison_clipart`: `_temp/svg_sexual_cycle_comparison_art/`;
  `sexual_life_cycles.svg` -> `sexual_life_cycles.drawn.svg`.
- `/root/cellulosic_ethanol_clipart`: `_temp/svg_cellulosic_ethanol_art/`;
  `image_025.jpg` -> `cellulosic_ethanol.drawn.svg`.
- `/root/bioremediation_wells_clipart`: `_temp/svg_bioremediation_wells_art/`;
  `image_009.png` -> `bioremediation_wells.drawn.svg`.
- `/root/cellulosome_assembly_clipart`: `_temp/svg_cellulosome_assembly_art/`;
  `image_027.jpg` -> `cellulosome_assembly.drawn.svg` and
  `image_029.png` -> `cellulosome_cellulose_interface.drawn.svg`.

Current source locations and authored root slides are fixed by those selections:

| Target | Physical Djot | Line | Root slide |
| --- | --- | --- | --- |
| Female/male flies | `genetics/LECT06/djot/lect06d-x_linked_genes_1.djot` | 72 | 6 |
| Morgan experiment | `genetics/LECT06/djot/lect06d-x_linked_genes_1.djot` | 115 | 11 |
| Morgan chromosomes | `genetics/LECT06/djot/lect06d-x_linked_genes_1.djot` | 125 | 12 |
| Sexual cycles | `genetics/LECT06/djot/lect06c-meiosis.djot` | 531 | 44 |
| Cellulosic ethanol | `biotech/LECT06/djot/set4_chapter_13.djot` | 238 | 100 |
| Bioremediation wells | `biotech/LECT06/djot/set4_chapter_12.djot` | 260 | 31 |
| Cellulosome assembly | `biotech/LECT06/djot/set4_chapter_13.djot` | 265 | 102 |
| Cellulose interface | `biotech/LECT06/djot/set4_chapter_13.djot` | 277 | 103 |

The two Genetics physical files are their roots: LECT06d has 62 authored slides and LECT06c
has 53, both with zero hidden slides. All four industrial uses belong to
`biotech/LECT06/djot/lect06c-set_4_tp_chapter_12_16_material.djot`, with 281 authored slides
and zero hidden slides. These are selection counts, not new export results.

All six early source checkpoints are received and **ACCEPTED by the root manager**; all six
artists proceed scratch-only, with no unresolved source-glyph ambiguity. Biotechnology source
evidence is `_temp/svg_cellulosic_ethanol_art/source_ledger.json` and `CONSTRUCTION.md`,
`_temp/svg_bioremediation_wells_art/SOURCE_CHECKPOINT.md` and
`_temp/svg_cellulosome_assembly_art/SOURCE_CHECKPOINT.md`. Early checkpoint acceptance does
not accept finished artwork. Finished candidates, independent source/art review, actual-source
exports, fresh context-quality review, integration, canonical delivery and fresh canonical
tests remain pending. The **5751 passed** receipt above covers only the completed
Ames/checkpoint/Neurospora batch; it establishes no acceptance for these eight targets.

All eight selected sources are schematic. The adjacent mixed `image_028.gif` stays whole,
including its microscopy and labels. Cellulosome root slide 102's small top-right slot is a
known fit risk requiring actual-context review. Preserve all original assets, native content,
voice, photographs and data. Gene trees remain excluded; `@replaceme` is irrelevant to
selection, and genuine good SVGs remain KEEP. Later energy wrappers are not dispatched.

This checkpoint adds no plan, policy, global inventory quota or acceptance receipt. All earlier
ledger bytes remain unchanged. Before/after snapshots, exact diff, hashes and bounded ASCII,
whitespace, no-new-Markdown-link and scoped Git diff checks are in
`_temp/fly_cycles_industrial_queue_checkpoint/`. No LibreOffice, export, pytest or index action
runs for this documentation update. The broader all-lecture artwork goal remains **OPEN**.

## Fly and industrial review checkpoint

Updated 2026-11-10 after the dispatch checkpoint above: all six artists have frozen their
standalone candidates, and all eight SVGs have independent source/art **ACCEPT** verdicts.
Final source reviews are `_temp/fly_cycles_source_review/REVIEW.md` for the four Genetics
figures and `_temp/industrial_cellulosome_source_review/REVIEW.md` for the four Biotechnology
figures. The selection briefs, owners and eight targets above remain the current queue.
Original native content, source assets, photographs and the complete mixed microscopy GIF
remain protected; these acceptances do not authorize prose or lesson redesign.

Actual-source export is in progress under `_temp/fly_cycles_industrial_export/`.
The completed `_temp/fly_cycles_context_quality/REVIEW.md` portions accept the female/male
fly and both Morgan figures in their real placements, preserving native text, notes, frames,
non-target images and selectable labels. The sexual-cycle review is pending, including the
plant leader. Biotechnology actual-context review is pending under
`_temp/industrial_cellulosome_context_quality/`; the small root-slide-102 assembly slot
remains a specific fit risk. No pending review is counted as accepted.

Canonical integration, full-root exports and the fresh base suite remain **PENDING** for
this batch. The completed **5751 passed, 2 warnings in 24.59s** receipt remains specific to
the prior Ames/checkpoint/Neurospora delivery; the earlier **5734 passed** receipt likewise
remains specific to bottle/algae/liposome delivery.

A separately reviewed maintenance fix changes only `write_svg()` serialization from
`xml_declaration=True` to `False`, plus its explanatory comment. Repeated blank LibreOffice
imports with an ASCII encoding declaration motivated this small shared fix; current artists
had already normalized their candidates manually. ASCII bytes, numeric character references,
safe XML parsing and metadata validation before writing are preserved. Caller inspection
found no dependency on the declaration. Both existing SVG drawing tests pass, and disposable
checks confirm parsed XML/Unicode equivalence, ASCII output and the invalid-metadata data-loss
guard. Evidence is `_temp/svg_writer_declaration_fix/HANDOFF.md`, `change.diff` and adjacent
caller/check records. No art was regenerated, and no new live LibreOffice validation of the
helper is claimed. The full base suite after this code change remains **PENDING**.

This documentation-only update preserves the earlier ledger bytes and all completed receipts.
Before/after snapshots, exact diff, hashes and scoped ASCII, whitespace and canonical-link
checks are in `_temp/fly_cycles_industrial_checkpoint/`. No export, pytest or index action
runs here. The broader all-lecture artwork goal remains **OPEN**.

## Fly and industrial integration

**DONE_WITH_CONCERNS for contextual review and integration; canonical delivery pending.**
All eight final drawings have independent source/art and actual-context **ACCEPT** verdicts.
The first Genetics actual review accepted the fly and Morgan pair but requested a sexual-cycle
leader correction: the original leader pointed ambiguously into the leafy gametophyte.
The retained parent and first-pass proofs are evidence, not the final accepted cycle.

The corrected cycle is `_temp/svg_sexual_cycle_leader_fix/sexual_life_cycles.drawn.svg`,
SHA256 `9f6c7f934443914225fa9ac5b0ca4feca38a1e6cc1e15a20db8c3591ef4a653c`.
Only one leader path's `d` changes, reaching the exposed capsule without crossing visible
routes or label letters. All 52 labels and the remaining artwork bytes are preserved.
Fresh source acceptance is `_temp/sexual_cycle_leader_source_review/REVIEW.md`; fresh actual
acceptance is `_temp/sexual_cycle_leader_context_review/REVIEW.md`. The corrected proof in
`_temp/sexual_cycle_leader_export/HANDOFF.md` and `final_freeze.json` supersedes only the
initial cycle candidate. All original baseline Djot/ODP/PDF bytes remain intact.

The initial six proof pairs in `_temp/fly_cycles_industrial_export/REVIEW.md` cover twenty
contexts per variant and forty inspected PDF pages. All 213 SVG text elements are selectable;
46 native paragraphs and their referenced styles match. Final Genetics acceptance uses
`_temp/fly_cycles_context_quality/REVIEW.md` for the fly/Morgan figures and the fresh corrected
cycle review above. All four Biotechnology drawings are accepted in
`_temp/industrial_cellulosome_context_quality/REVIEW.md`. Both initial and corrected exporters
released LibreOffice ownership. Native text, notes, frames, neighboring assets and the whole
mixed microscopy GIF remain protected and verified in the relevant completed proofs.

Integration passes in `_temp/fly_cycles_industrial_integration/HANDOFF.md`: eight exact
accepted SVGs and eight image-URL substitutions in four physical Djot files. The corrected
cycle alone is canonical. All 222 preexisting assets and six other source dependencies are
unchanged. Final parsed root counts remain 62/zero hidden, 53/zero hidden and 281/zero hidden;
these are source counts, not canonical export results. The integration freeze covers 684 files.

One inherited degree sign in `biotech/LECT06/djot/set4_chapter_13.djot:222` was separately
escaped as `&#176;`, with no other normalization. This encoding maintenance preserves complete
75-slide parsed models, inline/style runs and rendered wording. Evidence is
`_temp/fly_cycles_djot_degree_escape/HANDOFF.md`, `source.diff` and `checks.json`.
The integration preserves its pre-escape URL-only snapshots. Reversing eight URLs plus that
single entity restores every original source byte; complete full-root models match after URL
reversal alone, without entity normalization. All four edited Djot files are now ASCII.

Accepted viewing limits remain: the small assembly panel has PDF labels of 6.92, 7.79 and
8.36 pt and no large repeat. Full-size viewing or zoom is needed for those fine labels.
Morgan alleles, cycle detail, ethanol captions and wells chemistry also need the large view;
neighboring low bottom margins remain unchanged. These are bounded display limitations,
not a new global font rule. Two demonstrated Morgan/ethanol composition examples are added to
[GENETICS_ILLUSTRATION_GUIDE.md](../../slide-specs/GENETICS_ILLUSTRATION_GUIDE.md).

The three documents are frozen for delivery in
`_temp/fly_cycles_industrial_checkpoint/pre_delivery_freeze.json`, with before/after snapshots,
exact diff and scoped checks alongside. The existing changelog archive is unchanged.
Canonical full-root exports, final changed/neighbor inspection and the exact base suite after
both this integration and the SVG writer fix remain **PENDING**. No new live LibreOffice
validation of the helper is inferred from manually normalized candidate art. The prior
**5751 passed** and **5734 passed** delivery receipts retain their original batch scope.
No tests, exports or index actions run for this documentation update; the broader goal is **OPEN**.

## Fly and industrial delivery

**DONE_WITH_CONCERNS; canonical delivery complete.**
`_temp/fly_cycles_industrial_delivery/REVIEW.md` and `final_checks.json` record fresh canonical
source/ODP/hidden/PDF counts of 62/62/0/62 for LECT06d, 53/53/0/53 for LECT06c, and
281/281/0/281 for Biotechnology LECT06. All three serial builds exit zero.

All eight placements embed the exact accepted SVGs, including only the corrected cycle.
All 213 SVG text elements remain selectable. Nineteen unique canonical context pages were
individually inspected, representing twenty proof-context instances because Biotechnology
page 101 belongs to two proof families. Native paragraphs, notes, geometry, image payloads
and selectable text match the accepted final proofs; all 46 native paragraph/style instances
match after generated page-number style ID normalization. The whole original mixed GIF stays
byte-identical on page 102. The corrected leader reaches the exposed sporophyte capsule;
the degree escape retains selectable `>700` and the degree sign followed by C on page 98.

Thirteen of twenty proof-instance render hashes match; all twenty content signatures and
selectable-text comparisons match. All changed placements and supplied adjacent contexts were
opened individually, with no new material clipping, banding, missing content or fit regression.
The scratch degree-sign check first selected page 99, then correctly used page 98; its failed
log is retained. This mapping correction required no source change, rebuild or rerender.

The exact command `source source_me.sh && pytest tests/` ran **once** after canonical builds:
**5767 passed, 2 warnings in 23.43s**, exit 0. This is fresh full-suite validation after the
SVG writer declaration fix and final artwork/source integration. The two warnings are the
existing anyio deprecation and layout-engine test-length advisory. Build and suite tracked-file
mutation dictionaries are empty. Only the eight exact accepted SVG additions entered the index;
all other index entries and thirteen preexisting cached EOF warnings remain unchanged.

Two prior canonical PDFs frozen as evidence were first saved byte-exact, then explicitly
superseded by authorized builds. Their original hashes remain in `superseded_outputs.json`;
the original manifests were not rewritten. The other 682 integration-frozen entries, all three
pre-delivery documents and the existing archive remain unchanged through delivery. All 222
original assets, six other dependencies, final ASCII sources and the SVG writer helper remain
intact. LibreOffice ownership is **RELEASED**, with no owned export process remaining.

Accepted concerns remain: assembly labels require full-size viewing or zoom, with no large
repeat; other fine labels and inherited neighbor margins/capacity advisories remain. No attended
Impress/Zoom playback, learner acceptance or whole-deck scientific audit is claimed.
This final documentation-only receipt follows the successful suite and runs no tests, exports
or index actions. The provisional guide/examples and existing archive remain byte-identical
to their pre-delivery freeze. Final snapshots, exact diff, hashes and scoped ASCII, whitespace
and Git-aware canonical-link checks are in `_temp/fly_cycles_industrial_checkpoint/`.
The prior **5751 passed** and **5734 passed** receipts remain intact. This eight-drawing batch
is complete; the broader all-lecture artwork goal remains **OPEN**.

## Mitosis and organelle queue

**Selection complete; scratch drawing in progress, 2026-11-10.** Frozen selections are
`_temp/remaining_art_round3/genetics/REPORT.md` (two families, four drawings) and
`_temp/remaining_art_round3/biotech/REPORT.md` (three families, three drawings).
The queue has seven targets, seven current uses and three roots. Five Astra artists are live;
each owns scratch artwork only. All five early source checkpoints are accepted by the manager,
including `_temp/remaining_art_round3_art/photosynthesis/LEDGER.md`. These are construction
checkpoints, not finished-candidate or scientific acceptance.

- Mitosis stages: `_temp/svg_mitosis_stages_art/`, three candidates:
  `mitosis_interphase_prophase.drawn.svg`, `mitosis_prometaphase_metaphase.drawn.svg` and
  `mitosis_anaphase_telophase.drawn.svg`. Physical/root source
  `genetics/LECT06/djot/lect06b-intro_cells.djot`, lines 229/239/249, root pages 20/21/22;
  24 authored slides, zero hidden.
- Division comparison: `_temp/svg_division_comparison_art/`,
  `mitosis_meiosis_comparison.drawn.svg`. Physical/root source
  `genetics/LECT06/djot/lect06c-meiosis.djot:556`, root page 47; 53 slides, zero hidden.
- Plant primary wall: `_temp/remaining_art_round3_art/plant_wall/`,
  `plant_primary_wall.drawn.svg`, replacing `image_022.jpg`; physical line 177, root page 95.
- Pyruvate branch: `_temp/remaining_art_round3_art/pyruvate_branch/`,
  `pyruvate_branch.drawn.svg`, replacing `figure_021_labeled.svg`; line 95, root page 87.
- Photosynthesis exchange: `_temp/remaining_art_round3_art/photosynthesis/`,
  `photosynthesis_exchange.drawn.svg`, replacing `figure_044_labeled.svg`;
  line 740, root page 144.

All three Biotechnology drawings use `biotech/LECT06/djot/set4_chapter_13.djot`, included in
`biotech/LECT06/djot/lect06c-set_4_tp_chapter_12_16_material.djot` (281 slides, zero hidden).
The Biotechnology selection freeze includes governing documents. Authorized progress-log
updates record workflow state; they are not changed source illustration or deck evidence.

All selected source media are wholly illustrative; no empirical image is being replaced.
Photographs, the neighboring chemistry figure, originals and native teaching voice remain
protected. Wall scale cues and source-relative geometry, mitotic counts and reciprocal ancestry,
and organelle carrier directions require drawing-contract review. This is not a global science
audit. Gene trees remain excluded; `@replaceme` does not determine eligibility.

Finished candidates, independent source/art review, actual-context review, integration,
canonical delivery and validation for this queue are all **PENDING**. The **5767 passed** receipt
above belongs only to the previous delivered eight-drawing batch. No candidate or canonical
acceptance is claimed here. Before/after snapshots, exact diff, hashes and scoped checks are in
`_temp/mitosis_organelle_queue_checkpoint/`. This prose checkpoint runs no LibreOffice export,
pytest or index action. The broader all-lecture artwork goal remains **OPEN**.

## Mitosis and organelle review

**Seven source/art candidates accepted; contextual review underway, 2026-11-10.**
All five artists have finished and frozen the seven drawings selected in
`_temp/remaining_art_round3/genetics/REPORT.md` and
`_temp/remaining_art_round3/biotech/REPORT.md`. Independent source/art review accepts all seven:
`_temp/mitosis_division_source_review/REVIEW.md` and
`_temp/wall_organelle_source_review/REVIEW.md`. These receipts supersede the pending candidate
state in the historical queue checkpoint above.

Actual-source ODP/PDF proofs are underway in `_temp/mitosis_wall_organelle_export/`.
`_temp/mitosis_division_context_quality/REVIEW.md` accepts all three mitosis drawings and the
division comparison: eight paired contexts retain all 74 selectable SVG text elements and
25 native paragraphs, with chromosome counts, ancestry and leader endpoints verified in the
actual slides. `_temp/wall_organelle_context_quality/PYRUVATE_REVIEW.md` accepts the pyruvate
cutaway in its three-page context, including all 17 selectable SVG labels and 9 native
paragraphs. Wall and photosynthesis contextual verdicts remain **PENDING** at this checkpoint.

The frozen source-plan and guide versions are recorded in the selection/review evidence.
Authorized ledger updates record progress; they do not claim source-art drift. All seven targets
are pure illustrations. Photographs, neighboring chemistry, original assets and native teaching
voice remain preserved. Drawing review retains source chromosome counts and branches, the wall's
50 nm meaning and contacts, and organelle carrier directions while allowing original artistic
composition. It does not require old-pixel replication. Gene trees remain excluded and
`@replaceme` remains irrelevant to selection.

Canonical integration, full-root delivery and the fresh base suite remain **PENDING** for this
seven-drawing batch. No new production code change or source cleanup is planned. The SVG writer
declaration fix and degree-entity repair belong to the completed **5767 passed** eight-drawing
baseline above; that receipt does not validate these seven new drawings. Fine labels and
chromatid tips need the full lecture view; the inherited division-neighbor overlay remains.
This documentation-only checkpoint runs no exports, tests or index actions. Before/after bytes,
exact diff, hashes and scoped checks are in `_temp/mitosis_wall_organelle_checkpoint/`.
The broader all-lecture artwork goal remains **OPEN**.

## Mitosis and organelle integration

**All seven actual-context ACCEPT; art-only integration complete, 2026-11-10.**
`_temp/mitosis_division_context_quality/REVIEW.md` and
`_temp/wall_organelle_context_quality/REVIEW.md` accept all seven unchanged frozen drawings.
The completed `_temp/mitosis_wall_organelle_export/REVIEW.md` records seventeen paired contexts,
34 inspected PDF pages, 119 selectable SVG text elements and 52 native paragraph/style instances.
This supersedes the pending wall/photosynthesis contextual state above.

`_temp/mitosis_wall_organelle_integration/HANDOFF.md` records seven exact accepted SVG copies
and seven image-URL substitutions in three ASCII Djot files. URL reversal restores complete
original bytes and parsed models. All 210 preexisting assets, seven other source dependencies
and 96 runtime files remain unchanged. No source normalization or production code edit was needed.
The three roots retain authored/hidden counts of 24/0, 53/0 and 281/0. The integration's
`accepted_hashes.json` identifies every canonical copy; its `delivery_freeze.json` seals 837 files.

The prior Biotechnology canonical ODP/PDF are saved byte-exact under the integration's
`prior_canonical/`, with old hashes and explicit authorized output supersession recorded in
`canonical_supersession.json`. Governing document versions remain separate historical evidence.
One demonstrated wall example is added to the provisional
[GENETICS_ILLUSTRATION_GUIDE.md](../../slide-specs/GENETICS_ILLUSTRATION_GUIDE.md): the 50 nm bar
preserves source-relative fibril scale while exploded layer spacing remains schematic.

The three delivery documents and unchanged existing changelog archive are frozen in
`_temp/mitosis_wall_organelle_checkpoint/pre_delivery_freeze.json`; before/after snapshots,
exact diff and scoped checks are alongside. Canonical full-root builds, changed/neighbor
inspection and the fresh exact base suite remain **PENDING**. The **5767 passed** receipt remains
specific to the preceding eight-drawing delivery. Fine labels, chemistry and chromosome tips
need the full lecture view; the inherited division-neighbor overlay remains unchanged.
No tests, exports or index actions run for this documentation update. The broader goal is **OPEN**.

## Mitosis and organelle delivery

**DONE_WITH_CONCERNS; canonical delivery complete.**
`_temp/mitosis_wall_organelle_delivery/REVIEW.md` and `final_checks.json` record all three serial
builds exiting zero. Source/ODP/hidden/PDF counts are 24/24/0/24 for LECT06b, 53/53/0/53 for
LECT06c and 281/281/0/281 for Biotechnology LECT06. All seven exact accepted SVGs embed at
their intended placements, and all 119 SVG text elements remain selectable.

All seventeen unique canonical contexts, including every changed placement and its neighbors,
were opened individually. Native content, full notes, frame geometry, target/non-target payloads
and selectable text match the accepted final proofs. All 52 native paragraph/style instances
match after generated page-number style ID mapping. The G2 caption's separately emitted PDF
subscript remains visibly correct and matches the accepted proof; no source/export repair was
needed. Thirteen of seventeen render hashes match; all seventeen content signatures and text
streams match. No new material clipping, banding, missing glyphs or placement defect was found.

The exact command `source source_me.sh && pytest tests/` ran **once** after canonical builds:
**5781 passed, 2 warnings in 23.70s**, exit 0. The warnings are the existing anyio deprecation
and layout-engine test-length advisory. Build and suite tracked-file mutation dictionaries are
empty. Exactly seven accepted SVG additions entered the index; other index entries and thirteen
preexisting cached EOF warnings remain unchanged.

All 837 integration-freeze entries and all four pre-delivery document/archive entries remained
intact through delivery. The 210 original assets, seven other source dependencies, 96 runtime
files, current SVG helper and final ASCII sources remain unchanged. Prior Biotechnology ODP/PDF
files were independently saved byte-exact before explicit authorized supersession; archived
copies and original manifests remain intact. LibreOffice ownership is **RELEASED**, with no
owned export process remaining. The previous writer fix and degree escape remain unchanged.

Accepted concerns remain: fine labels, chromosome tips and neighboring chemistry need the full
lecture view; wall layer spacing is schematic. The inherited division page-48 overlay and
existing capacity advisories remain. No attended Impress/Zoom playback, learner acceptance or
whole-deck scientific audit is claimed. This final documentation-only receipt follows the suite
and runs no tests, exports or index actions. The provisional guide/example and existing archive
remain byte-identical to their pre-delivery freeze. Final snapshots, exact diff, hashes and
scoped ASCII, whitespace and Git-aware nonignored canonical-link checks are in
`_temp/mitosis_wall_organelle_checkpoint/`. Earlier **5767 passed**, **5751 passed** and other
historical receipts retain their original scope. This seven-drawing batch is complete;
the broader all-lecture artwork goal remains **OPEN**.

## Mouse, strawberry and mass-spectrometry queue

**Source selection DONE_WITH_CONCERNS; artwork underway, 2026-11-10.**
The approved art-only plan continues while the instructor is away. This restartable checkpoint
preserves the queue if a usage cap interrupts work. Fresh selection reports are
`_temp/remaining_art_round4/genetics/REPORT.md` (SHA256
`fcc478c10592a5a0db083b60ba71c1fa68717e0d40d580aac2ca714ceafe9277`) and
`_temp/remaining_art_round4/biotech/REPORT.md` (SHA256
`445dd3e18259a62cdd2aa0966c7e4540f4e3cae9bfb803f7fa8102efce3f30ff`). Their target/use maps
record **five SVGs in four families, 24 uses across three roots**: six Genetics uses and
18 Biotechnology uses. This bounded selection does not establish exhaustion of remaining art.

The current roots retain authored/hidden counts of 55/0 for Genetics LECT05f, 49/1 for Genetics
LECT11b and 390/6 for Biotechnology LECT04c. Mouse grafts have five uses; strawberry has one;
MALDI has three; electrospray has seven; magnetic sector has eight. Biotechnology edits belong
to the shared physical proteomics source, not the including root. Exact locations, alt text,
layouts and source blocks remain in Genetics `targetmap.json`/`usemap.json` and Biotechnology
`dispatch_targets.json`/`current_consumers.json` beside the selection reports.

Four active `gpt-6-astra` artists use high reasoning. Root-assigned ownership and candidate
names below supersede the selection reports' suggested scratch paths and names:

- `/root/mouse_graft_network_clipart`: `_temp/svg_mouse_graft_network_art/`,
  `mouse_graft_network.drawn.svg`.
- `/root/strawberry_polyploid_clipart`: `_temp/svg_strawberry_polyploid_art/`,
  `strawberry_polyploid.drawn.svg`.
- `/root/maldi_electrospray_clipart`: `_temp/svg_mass_ionization_art/`,
  `maldi_ionization.drawn.svg` and `electrospray_ionization.drawn.svg`.
- `/root/magnetic_sector_clipart`: `_temp/svg_magnetic_sector_art/`,
  `magnetic_sector_analyzer.drawn.svg`.

Artists own scratch artwork and evidence only. Source/art acceptance, actual-source ODP/PDF
proofs, fresh independent quality review, canonical integration, full-root builds and the fresh
base suite are all **PENDING**. LibreOffice owner is **NONE**; no agent may invoke LibreOffice
until the manager assigns its serialized phase. On restart, check these owners and their
handoffs, freeze candidate bytes, then resume the pending gates without treating dispatch as
acceptance. The **5781 passed, 2 warnings in 23.70s** receipt above belongs to the delivered
seven-drawing batch; it is not a new check or validation of these five candidates.

Original creative geometry must preserve the same concepts, labels and relationships. Keep
native voice, prose, tables, layouts, markers, reveals, notes and slide order unchanged. Retain
original assets and empirical companions. The mouse network needs four identities and twelve
neutral directed arrows, with no baked-in answers. Strawberry retains two circles labelled
`2n`, the branch/merge route, A-D stages and fruit comparison; its separate exact photograph
stays unchanged. The apparatus drawings retain source particle identities, charges and flow;
magnetic sector retains three trajectories, three detector cups and all live wording, including
`Faradays Detector`. These are drawing contracts, not a global science or prose revision.

The mouse's final 1.15 cm placement and prior-output overlay are inherited observations; a new
actual export determines their current condition. Small equipment slots need their larger repeat
views or zoom for detail. Inspect real placements without imposing a global font-size gate or
silently changing layouts. Cellulose remains eligible for a future chemistry-specialist source
map and composition study; its deferral here is not permanent exclusion.

This queue checkpoint accepts no artwork and runs no pytest, LibreOffice, builds or index
operations. Existing ledger bytes and receipts remain exact. Before/after snapshots, append-only
diff, hashes and scoped ASCII, whitespace, Git-aware canonical-link and unchanged-index checks
are in `_temp/mouse_strawberry_mass_queue_checkpoint/`. The broader all-lecture artwork goal
remains **OPEN**.

## Mouse, strawberry and mass-spectrometry integration

**Five drawings integrated; canonical delivery pending, 2026-11-10.** Independent source/art
reviews accept all five SVGs in `_temp/mouse_strawberry_source_review/REVIEW.md` and
`_temp/mass_equipment_source_review/REVIEW.md`. Fresh actual-context reviews also accept all five:
`_temp/mouse_strawberry_context_quality/REVIEW.md` and
`_temp/mass_equipment_context_quality/REVIEW.md`. These supersede the pending artwork and
integration state in the queue checkpoint above; its historical bytes and receipts remain intact.

The paired proofs in `_temp/mouse_strawberry_mass_export/REVIEW.md`, `GENETICS_REVIEW.md` and
`MASS_REVIEW.md` cover 34 contexts per variant, 68 individually inspected PDF pages, 18 changed
pages and all 24 uses. They retain 131 selectable SVG text-element instances and 140 native
paragraph/style instances. All six serial proof exports exit zero outside the sandbox;
LibreOffice ownership is released. The separate strawberry photograph, including its embedded
credit, stays byte-exact; the credit is part of the photograph, not native slide prose.

`_temp/mouse_strawberry_mass_integration/HANDOFF.md`, `accepted_hashes.json` and `checks.json`
record five exact canonical additions and 24 image-URL-only substitutions in three ASCII sources:
mouse graft network (5), strawberry polyploidy (1), MALDI (3), electrospray (7) and magnetic
sector (8). Complete URL reversal restores source bytes and parsed models. Native voice,
prose, titles, alt text, tables/styles, notes, layouts, markers, reveals and sequence remain
unchanged. All 174 original assets, four other source dependencies, 96 runtime files and the
SVG helper remain intact; the index is unchanged. No source cleanup or general science
correction is included. Root authored/hidden/visible counts remain 55/0/55, 49/1/48 and 390/6/384.

The integration's `delivery_freeze.json` seals 906 entries, SHA256
`ad8b810b8accca5a59ab217fb34e56b12c136786f92426a498218b50debc1497`.
Six prior canonical ODP/PDF files are archived byte-exact under `prior_canonical/`, with their
original hashes and explicit output supersession mapping in `canonical_supersession.json`.
Unrelated LECT06 outputs remain unchanged historical references, outside this delivery.
Governing document versions are separately archived; authorized ledger appends are version
history, not source-art drift. One reviewed botanical construction example is added to
[GENETICS_ILLUSTRATION_GUIDE.md](../../slide-specs/GENETICS_ILLUSTRATION_GUIDE.md).

The three delivery documents and unchanged changelog archive are sealed in
`_temp/mouse_strawberry_mass_checkpoint/pre_delivery_freeze.json`, alongside before/after
snapshots, exact diff and scoped checks. Canonical full-root builds, changed/neighbor inspection
and a fresh exact base suite remain **PENDING**. The previous **5781 passed, 2 warnings in
23.70s** receipt belongs only to the earlier mitosis/organelle batch.

Accepted limits persist: mouse page 35 is tiny beneath its inherited REPLACE ME overlay;
the first four mouse uses improve. Fine equipment annotations need existing large visible
pages 92, 93 and 96 or zoom. The unchanged Time of Flight neighbor on visible page 97 clips
exactly `different times.` after `detector at`; complete source/ODP wording remains. These
bounded drawing reviews do not establish attended playback, learner acceptance or a whole-deck
science audit. No tests, exports or index actions run for this documentation checkpoint.
The broader all-lecture artwork goal remains **OPEN**.

## Mouse, strawberry and mass-spectrometry delivery

**DONE_WITH_CONCERNS; canonical delivery complete.**
`_temp/mouse_strawberry_mass_delivery/REVIEW.md` and `final_checks.json` record three serial
builds exiting zero. Source/ODP/hidden/PDF counts are 55/55/0/55 for LECT05f, 49/49/1/48 for
LECT11b and 390/390/6/384 for Biotechnology LECT04c. All 24 placements embed the five exact
accepted SVGs; all 131 SVG text-element instances remain selectable. All 34 mapped canonical
contexts were individually viewed, including every changed placement and its neighbors.

Native page content, notes, geometry, non-target payloads and all 140 native paragraph/style
instances match the accepted proofs. Thirty-one render hashes match; the three strawberry
pairs were individually compared, with matching content/styles and no meaningful visual change.
The complete strawberry photograph and embedded credit remain byte-exact in ODP; PDF pixel
identity is not claimed. The initial comparison failed on generated section-style IDs;
recursive comparison of complete referenced definitions resolved the equivalent IDs without
source/export changes or rebuilds. Its original log and raw XML remain preserved.

The exact command `source source_me.sh && pytest tests/` ran **once** after canonical builds:
**5791 passed, 2 warnings in 26.79s**, exit 0. The warnings are the existing AnyIO plugin
`CallSpec2` deprecation and layout-engine test-length advisory. Build and suite tracked-file
mutation dictionaries are empty. Exactly five accepted SVG additions entered the index;
every prior entry and all thirteen preexisting cached EOF warnings remain unchanged.

All 906 integration-freeze entries and four pre-delivery document/archive entries stayed intact
through delivery. The six prior canonical output archives remain byte-exact after authorized
live-output supersession; unrelated LECT06 references remain unchanged. The delivery's
`completed_hashes.json` seals 95 artifacts, SHA256
`5010a14db832330a7b19935a52241973d970921206161c2a5c51abaadb1ecaa4`.
LibreOffice ownership is **RELEASED**, with no owned build, export or suite process remaining.

Accepted concerns remain: mouse page 35 retains its tiny network and large REPLACE ME overlay;
the unchanged TOF neighbor on visible page 97 clips exactly `different times.` in PDF while
source/ODP retains the complete sentence. Fine mouse digits and equipment annotations require
the full lecture view, existing large repeats or zoom. Existing capacity/low-margin conditions
remain. No attended Impress/Zoom playback, learner acceptance or whole-deck science audit is
claimed. The previous **5781 passed** receipt and all earlier receipts retain their batch scope.

This final documentation-only receipt follows the suite and runs no tests, exports or index
actions. The provisional guide/example and existing changelog archive remain byte-identical
to the pre-delivery freeze. Final snapshots, exact diffs, hashes and scoped ASCII, whitespace
and Git-aware canonical nonignored-link checks are in `_temp/mouse_strawberry_mass_checkpoint/`.
This five-drawing batch is complete; the broader all-lecture artwork goal remains **OPEN**.

## Flower, cattle and assay queue

**QUEUE checkpoint DONE_WITH_CONCERNS; artwork underway, 2026-11-10.** The manager promotes
the optional Four-o-clock drawing from the frozen Genetics selection. The resulting queue is
**16 SVGs in seven artist families, 60 uses: 57 visible and three hidden**, across three roots.
Authored/hidden/visible counts remain Genetics LECT05f **55/0/55**, Genetics LECT05h **89/0/89**
and Biotechnology LECT04c **390/6/384**. Current sources are ASCII. Frozen selection reports:
`_temp/remaining_art_round5/genetics/REPORT.md`, SHA256
`f7d2806e6505b240694dd1f083b6c42921dee1fecb0b85560129f6d82d1c2437`, and
`_temp/remaining_art_round5/biotech/REPORT.md`, SHA256
`f5ba53985d14cb4b2daa678c48de0c43358422e2083ee612a9f72be728edf802`.
Their maps retain exact physical owners, placements, source blocks and original-media evidence.

Seven active `gpt-6-astra` artists use high reasoning, with scratch-only ownership:

- `/root/pea_flower_states_clipart`: `_temp/svg_pea_flower_states_art/`; six candidates
  `pea_mendel_p.drawn.svg`, `pea_mendel_f1.drawn.svg`, `pea_mendel_f2.drawn.svg`,
  `pea_complementary_p.drawn.svg`, `pea_complementary_f1.drawn.svg` and
  `pea_complementary_f2.drawn.svg`, covering ten uses.
- `/root/snapdragon_generations_clipart`: `_temp/svg_snapdragon_generations_art/`;
  `snapdragon_generations.drawn.svg`, one use.
- `/root/cattle_color_cross_clipart`: `_temp/svg_cattle_color_cross_art/`;
  `cattle_color_cross.drawn.svg`, one use.
- `/root/four_oclock_cross_clipart`: `_temp/svg_four_oclock_cross_art/`;
  `four_oclock_incomplete_cross.drawn.svg`, one use.
- `/root/western_workflow_clipart`: `_temp/remaining_art_round5_art/western_workflow/`;
  `western_transfer_primary.drawn.svg` (11 uses) and `western_secondary_detection.drawn.svg`
  (ten uses, with three hidden placements across the pair).
- `/root/western_detection_clipart`: `_temp/remaining_art_round5_art/western_detection/`;
  `western_detection_detail.drawn.svg`, seven uses.
- `/root/elisa_assay_clipart`: `_temp/remaining_art_round5_art/elisa/`;
  `elisa_indirect_sandwich.drawn.svg` (six uses), `elisa_indirect_hrpo.drawn.svg` (three),
  `elisa_sandwich_biotin.drawn.svg` (seven) and `elisa_plate_readout.drawn.svg` (three).

Independent source/art review, actual-source proofs and fresh quality review, canonical
integration, full-root builds and a fresh base suite are all **PENDING**. LibreOffice owner is
**NONE**; artists do not run LibreOffice. No staging changes occur for this queue. On restart,
check owner handoffs and freeze candidate bytes before the manager dispatches fresh reviewers
and assigns the single LibreOffice owner. The completed five-drawing delivery's **5791 passed,
2 warnings in 26.79s** is historical evidence only; it validates none of this new artwork.

Create original geometry rather than pixel tracing. Preserve native voice, prose, tables,
layouts, markers, reveals, notes, hidden states, examples and original assets; replace art only.
The inherited LECT05h three-purple/one-white icons beside native 382/269 counts and 9:7 wording
remain documented, not globally repaired. Current LECT05f Four-o-clock wording governs that
subject over the old ODP's snapdragon caption; its artist independently checks a primary
botanical reference. Keep it distinct from the actual snapdragon family. New roan artwork
depicts the taught intermixed red/white hair instead of copying old patch contours; native
wording stays unchanged, and the separate `image_022.png` photograph stays exact.

The narrow source-label exception follows [HUMAN_GUIDANCE.md](../../HUMAN_GUIDANCE.md), lines
104-105: omit only textbook identifiers `Figure 6-23 part 1`, `Figure 6-23 part 2` and
`Figure 5.22` from the new SVGs. Preserve full useful captions, credits, stage text and the
descriptive `Diagram 1`/`Diagram 2` web-source captions. This supersedes the manager's broad
all-words brief only for those textbook identifiers; no other omission is authorized.

Hidden placement review covers three Western uses on authored pages 77-78: `image_030.jpg`
twice and `image_031.jpg` once. Read-only explorer `/root/hidden_slide_review_export_route`
found no CLI option: `slide_lib/libreoffice.py` fixes `ExportHiddenSlides` to false. The scratch
route is recorded in `_temp/flower_assay_queue_checkpoint/HIDDEN_EXPORT_ROUTE.md`: a process-local
`unittest.mock.patch.object` changes only that exact property for the existing
`slide_lib.native_export.convert_odps_to_pdfs` call on untouched paired ODPs, writing distinct
scratch supplemental PDFs. Require exactly one matching property and identical ODP hashes
before/after. Ordinary proofs and canonical PDFs retain false; source/ODP hidden flags remain.
The sole export owner must run all actual LibreOffice commands outside the sandbox. This route
has not been externally validated and adds no production feature, option, framework or test.
A full 390-page ODP would yield 390 supplemental pages; extracted-proof counts must derive
from their actual authored counts. Supplements serve hidden-placement review only.

This append accepts no artwork and runs no tests, builds, exports or index operations. Existing
ledger bytes, other files and index entries remain intact; the existing changelog archive/link
baseline is preserved. Before/after snapshots, exact append diff, hashes and scoped
ASCII, whitespace, Git-aware canonical-link and unchanged-index checks are in
`_temp/flower_assay_queue_checkpoint/`. The broader all-lecture artwork goal remains **OPEN**.

## Flower, cattle and assay integration

**Sixteen drawings integrated; canonical delivery pending, 2026-11-10.** Independent source/art
and actual-context reviews accept all nine Genetics and seven assay SVGs. The final contextual
verdicts are `_temp/flower_dominance_context_quality/REVIEW.md`,
`_temp/elisa_context_quality/REVIEW.md` and `_temp/western_context_quality/REVIEW.md`.
They supersede the queue's pending artwork state; the Western review's later R0 runtime-hash
failure remains historical evidence, qualified by the separate current-runtime receipt below.

`_temp/flower_assay_context_export/REVIEW.md` records 78 authored contexts per variant,
including three hidden contexts: 75 ordinary PDF pages per variant, all 150 ordinary images
and all six paired hidden images individually opened. All 306 native paragraph/style instances
are preserved. The 1,082 SVG text instances comprise 1,060 selectable instances and 22 outlined
decorative book-cover words, two words at eleven placements. Those words remain live in the
exact embedded SVGs and visibly identifiable; no teaching label is waived. The small Weight
leader crosses the initial letters of Biochemistry without a material reading defect.
Native Biotechnology PDF export varies horizontally by at most 0.214 pt, with no vertical
shift and exact source/ODP frames, styles and character streams; this is not artwork drift.

`_temp/flower_assay_runtime_revalidation/HANDOFF.md` and `equivalence.json` resolve the runtime
qualification for these six exact proof sources. R1 compilation reproduces every reviewed R0
ODP ZIP payload byte-exact, including native tables, styles, graphics and fonts; only ZIP
timestamps differ. Existing inspected PDFs therefore represent this R1 content. The receipt
does not establish unchanged tables elsewhere in the course. Its 279 current dependencies
are distinct from the historical 579-entry census with five unrelated source changes and four
cleared generated outputs; no old manifest or failure is rewritten.

`_temp/flower_assay_integration/HANDOFF.md`, `accepted_hashes.json` and `checks.json` record
sixteen exact canonical SVG additions and 60 image-URL-only substitutions in three ASCII
sources: ten pea, three dominance/cattle and 47 assay uses, including three hidden uses.
Complete URL reversal restores source bytes and parsed models. Native voice, prose, titles,
alt text, tables/styles, notes, layouts, markers, reveals, hidden states and sequence remain
unchanged. All 277 other actual inputs and 514 sealed proof/review/runtime artifacts remain
intact, including original assets, empirical photographs and experimental images.
Authored/hidden/visible counts stay 89/0/89 for Genetics LECT05h, 55/0/55 for LECT05f and
390/6/384 for Biotechnology LECT04c. No source cleanup or general science correction is made.

Only textbook identifiers Figure 6-23 part 1, Figure 6-23 part 2 and Figure 5.22 are omitted
under [HUMAN_GUIDANCE.md](../../HUMAN_GUIDANCE.md); useful captions, credits and Diagram 1/2
remain. The corrected ELISA plate retains brown well r2c8 at all three uses; its rejected parent
is not promoted. The accepted source is `_temp/elisa_plate_color_fix/elisa_plate_readout.drawn.svg`,
SHA256 `a4e16baeb35ae50212d918492088ac30674bb50c7ba60d56ae5a13867c919dde`.

The existing hidden-export route is now validated: process-local `ExportHiddenSlides=true`
produces 58-page scratch supplements for the paired Biotechnology proofs, with unchanged ODP
hashes and visibility. The filter is restored; ordinary proofs retain 55 pages. No production
code, CLI option or permanent test is added. All LibreOffice work is released.

Four matching prior Genetics ODP/PDF files are preserved byte-exact from frozen copies under
`_temp/flower_assay_integration/prior_canonical/`. The two Biotechnology outputs were already
unavailable and have historical hashes only; six preserved output archives are not claimed.
`availability_supersession.json` records the authorized future canonical output replacements.
The integration's 869-entry `delivery_freeze.json` has SHA256
`abf94adfff13b13c5da78447c69ec528a7011fd74a53e9707892738a85ae8911`; governing documents are
archived by version. External work added four test-only intent-to-add entries after preflight;
all preflight entries remain exact. Integration made no index writes. This documentation
checkpoint preserves that current index, flags, external edits and commits.

One paragraph in the existing botanical section of
[GENETICS_ILLUSTRATION_GUIDE.md](../../slide-specs/GENETICS_ILLUSTRATION_GUIDE.md) compares reviewed
pea and Four-o-clock anatomy within a shared drawing language. The guide remains provisional.
The three delivery documents and unchanged changelog archive are sealed in
`_temp/flower_assay_checkpoint/pre_delivery_freeze.json`, with before/after snapshots, exact
diff and scoped ASCII, whitespace, Git-aware canonical-link and unchanged-index checks.

Canonical full-root builds, changed/neighbor inspection and a fresh exact base suite remain
**PENDING**. The prior **5791 passed, 2 warnings in 26.79s** belongs only to the five-drawing
mouse/strawberry/mass-spectrometry batch. Accepted limits persist: three-purple/one-white pea
icons beside native 9:7 wording, fine snapdragon/assay labels requiring full view or existing
large repeats, and inherited tight native margins. These bounded reviews do not establish
attended playback, learner acceptance or a whole-deck science audit. No tests, builds, exports
or index operations run for this prose checkpoint. The broader artwork goal remains **OPEN**.
