## 2026-09-08

### Additions and New Features

- Made `genetics/xlect99-template_2023.otp` the authoritative master-slide theme. Added a validated
  format-neutral reader for its 16:10 page, top gradient, centered title typography, and nine native
  outline levels, plus ODP and PPTX adapters over that shared model.
- The ODP build now creates editable content, applies the real OTP master and styles, and exports
  PDF from that themed ODP. PPTX remains an editable interchange artifact that mirrors the same
  theme.
- Kept layout authoring on a stable 1280x800 logical canvas. The 16:10 ratio is mandatory while the
  template's physical centimeter or inch dimensions are not an authoring constraint.

### Fixes and Maintenance

- Ran the requested six-pass code audit over the native Djot theme, legacy importer normalization,
  screenshot-fallback removal, tests, documentation, dead code, and comments.
- Removed permanent tests that pinned tunable theme coordinates, exact gradient colors, the dense
  label threshold, and one geometry-specific diagnostic phrase. Retained semantic native bullet,
  gradient, and centered-title coverage.
- Removed unused import-planning return state and unused vector fields. Replaced the obsolete root
  migration plan with a concise retired marker because repository file discovery still includes the
  tracked path while Git operations remain outside this work.
- Corrected current changelog wording that described the superseded bounded-raster implementation as
  live behavior, and clarified the canonical theme and simplification behavior for newcomers.
- Replaced residual `CSS px` terminology with format-neutral logical units; CSS and browser
  rendering are not part of the presentation theme pipeline.

### Decisions and Failures

- Simplification retains the same instructional text and genuine content images through an existing
  Djot layout whenever possible; a review diagnostic accompanies content instead of replacing it.
- The audit found two unresolved importer defects: dense positioned-label normalization currently
  drops label text, and a table-bearing fallback can choose an invalid one-panel layout. Source-order
  normalization also currently receives geometry-ordered components. These require a focused native
  normalization redesign rather than audit-cleanup patches.

### Developer Tests and Notes

- Theme, native-export, importer, and hygiene verification passed 757 focused tests. The full
  permanent offline suite passed 1,682 tests, and strict native Jotdown validation retained 8 Djot
  sources, 336 slides, and 185 genuine image references.
- The native-layout E2E passed through editable PPTX, OTP-master ODP, and ODP-derived PDF with
  distinct native list levels. The full Genetics build produced 24 artifacts; all 336 slides had
  matching counts, every ODP used the exact template styles and master, every PPTX was 16:10, and no
  PPTX contained a full-slide picture substitution.
- Cropped ODP-derived PDF checks, rather than whole-slide screenshots, confirmed the shallow
  gradient, centered title, level-specific bullet forms, and wrapped-line hanging alignment.
- The first full-suite cleanup run stopped during collection because the deleted tracked migration
  plan remained in repository file discovery. Git operations were out of scope, so the path was
  restored as a concise retired marker; the corrected full suite then passed.

## 2026-09-07

### Additions and New Features

- Added `deck_tools.py` as the sole format-neutral application CLI for build, import, Djot lint,
  and ODP visibility workflows.
- Renamed the reusable application package from `marp_lib/` to `slide_lib/` so its ownership covers
  both Marp and Djot without implying a Marp-only pipeline.
- Added the geometry-first legacy-import architecture: semantic ODP/PPTX normalization now produces
  `LegacySlidePlan` records for atomic editable components, true source tables, and bounded coupled
  spatial regions.
- Added the bounded native OOXML animation backend: object APPEAR/FADE and top-level outline
  paragraph APPEAR reveals are emitted through one programmatic timing-tree owner without widening
  Djot's authoring syntax.
- Added `source_model.py` and `pptx_reader.py` so imported-presentation readers retain raw runs,
  links, images, notes, and first-class `TableBlock` facts.
- Added `pptx_theme.py` as the native lecture-theme owner: every standard slide receives a shallow
  blue-to-white top band, centered title, and nine explicit list levels with bullet positions, text
  tab stops, and hanging indents.
- Added native source-order normalization for ambiguous legacy geometry and visible redesign
  diagnostics for dense positioned-label fields that do not map cleanly to standard slide language.
- Defined the intended `pptx_reader` -> `slide_plan` -> `djot_emitter` ownership boundary.
- Added newcomer-facing `CODE_ARCHITECTURE.md`, `FILE_STRUCTURE.md`, `FILE_FORMATS.md`,
  `DEVELOPMENT.md`, `COOKBOOK.md`, `TROUBLESHOOTING.md`, and `RELATED_PROJECTS.md` guides, plus
  differentiated `NEWS.md` and `RELEASE_HISTORY.md` v26.09 release views from `VERSION` and the
  current changelog.
- Added a static, text-only rendered slide page to the README as an output-proof example.

### Behavior or Interface Changes

- `build_slides.sh genetics` and folder-valued `deck_tools.py build` commands now recursively find
  only `.djot` sources, so imported ODP files and ordinary Markdown are never treated as decks.
- Made `deck_tools.py build` dispatch `.md` and `.djot` sources through the same command, and made
  Djot the concise default target for trusted ODP/PPTX imports.
- Changed `build_slides.sh` into a thin folder-build convenience around `deck_tools.py build`.
- An intermediate ODP/PPTX import path used bounded Poppler renders for difficult regions. The
  same-day native-only redesign removed that path before acceptance; current imports normalize
  difficult slides through standard Djot layouts.
- Ordinary panel layouts now describe optional global titles and one local H2 per cell, with
  source-located capacity preflight before native shapes are created. Source tables remain editable
  only when the source provides actual table metadata; merged or spanned cells require review.
- Legacy source records now retain direct style, placeholder, z-order, rotation, and connector
  evidence. A shared registry-topology matcher and bounded positive relation classes preserve
  coupled visual teaching structures while retaining ordinary source content as editable objects.
- Top/group z-paths now retain actual source order. Reusable coarse-body/picture-inset, caption,
  and adaptive vertical-image relations preserve native objects through topology-first routing;
  they use exact provenance and narrow permissions rather than global or crop exceptions.
- Imported Djot assets now publish only when reachable from the parsed deck in its local asset tree;
  unsafe, missing, and symlinked references fail staged publication.
- Made `.djot` the sole authored deck source. `deck_tools.py import` always emits Djot from trusted
  ODP or PPTX input and no longer accepts `-t` / `--to`.
- Imported text and hyperlinks now remain raw reader facts until the emitter renders Djot, and
  source tables retain rows, cells, headers, blanks, and exact shape binding.
- Adjacent nested Djot lists now retain their semantic hierarchy without requiring a blank line.
- `two-over-one-panels` now allocates its footer from actual content need while preserving the
  readable minimum for both upper panels.
- Ordinary native panels now retain up to six legitimate component images without requiring a
  composite representation.

### Fixes and Maintenance

- Refreshed install and usage guidance for Python 3.12 environment activation, Homebrew tools, a
  validated pinned Jotdown 0.10.0 Cargo install route, and native import/export workflows.
- Corrected current acceptance documentation to name the one retained Djot native-layout E2E after
  the duplicate runners were removed.
- Removed claims that authored Djot or the current native E2E preserves presenter notes. Import
  readers retain raw note lines, but generated Djot currently records their omission pending a
  non-Djot preservation design.
- Corrected stale documentation that still treated the selected Djot grammar as unnamed, qualified
  the README's unobserved reveal claim, and documented non-obvious DNA run normalization.
- Pruned redundant serialization assertions while retaining the observed LibreOffice-prime and
  split-run DNA regressions. Reviewed all six test functions added or materially rewritten for the
  Djot-first fork; retained their current-boundary or known-regression coverage and consolidated the
  table round trip to two semantic assertions.
- Made missing animation-writer reveal intent fail loudly and corrected source/native-renderability
  documentation.
- Synchronized shared style guides, tests, and repository support files from the starter template.
- Fixed imported text and links being escaped before the output boundary; the Djot emitter now
  escapes raw characters exactly once and encodes link-target delimiters only while rendering.
- Fixed the PPTX reader inventing spaces between adjacent alphanumeric runs; formatting-only run
  boundaries now preserve the source characters exactly.
- Fixed imported source tables so supported tables emit as parseable Djot pipe tables rather than
  flattened text, including literal pipes, links, blank cells, and DNA prime projection.
- Renamed imported-deck planning modules and `LegacySlidePlan` to package-scoped Djot-first names,
  and renamed the private animation-writer attachment to `_slide_animation_writer`.
- Refreshed the README newcomer route and `INSTALL.md` / `USAGE.md` workflows; updated
  `ROADMAP.md` and `TODO.md` to describe current open boundaries.
- Recorded the 350-character GitHub About limit and the publication boundary: image-bearing slide
  PNGs remain unpublished pending copyright assessment, while text-only slide pages may publish.

### Removals and Deprecations

- Removed the nine `tools/*.py` package-import wrappers without compatibility aliases; this
  pre-production repository has no external callers for the obsolete paths.
- Removed three tracked Python bytecode caches that still embedded the former `marp_lib` name.
- Removed dead importer wrappers, enums, and re-exports instead of retaining compatibility facades.
- Removed duplicate and brittle tests that did not meet the permanent pytest contract.
- Removed the Marp parser, ODP/PPTX-to-Marp routes, target-format switch, suffix-dispatch table,
  parser/importer tests, Markdown decks, deck asset tree, CSS theme, dedicated documentation, and
  `markdown-it-py` / `PyYAML` dependencies.
- Removed Marp-only title-size state, the duplicate PPTX extraction implementation, the obsolete
  native-layout E2E, `tools/`, and completed rename-plan archives instead of retaining compatibility
  shims in this pre-production fork.
- Removed the `source_region` raster subsystem completely: implementation, importer hooks, crop and
  protected-render state, dedicated tests, generated composite references, and stale corpus assets.

### Decisions and Failures

- Exact full-slide rasterization remains outside the importer contract. Ambiguous geometry and
  source-table spans stop for review so a later native owner can extend the model deliberately.
- Exact legacy appearance is not an import contract. Difficult slides normalize to the shared Djot
  theme or expose a visible native limitation; genuine source figures remain ordinary image assets.
- Final acceptance passed 1,660 permanent tests, strict Djot validation for 8 decks/336 slides/185
  image references, the native-layout E2E, and the full 8-deck/24-artifact PPTX/ODP/PDF build.
- `multiple-choice` answers allow one or two short flat paragraphs and carry implicit reveal intent;
  M5 is reopened around a bounded OOXML builder with LibreOffice Impress as the playback authority.
- Corrected the animation architecture: PPTX is the Python-friendly native-builder and interchange
  artifact, while LibreOffice Impress/ODP is the editing and playback contract. The builder will use
  official OOXML and programmatic timing construction in `pptx_animation.py`, with no runtime XML
  templates or Microsoft compatibility gate.
- M5 implementation and its permanent structural/parser tests are complete. One-time LibreOffice
  bridge and ODP-derived PDF checks passed. The sole remaining M5/M7 evidence is attended Impress
  click playback; macOS denied Screen Recording and Accessibility before slideshow control, so no
  playback conclusion is claimed.
- Made the fork Djot-first while holding the implemented Djot grammar and layout behavior fixed.
  Historical changelog and language-decision records retain their provenance; they are not runtime
  compatibility promises.
- For this non-PyPI application, `VERSION` supplies the date-block release identity; a root
  `pyproject.toml` is not required solely as a release-document cross-check.
- Used the pre-production state to replace the extraction boundary directly rather than preserving
  old output-shaped records or aliases.
- The six-pass Djot-first audit found two open design issues: `pptx_reader.py` still constructs
  planner region records, and generated Djot records presenter-note omissions rather than preserving
  the content. These findings remain open rather than being hidden behind compatibility shims or an
  invented Djot note syntax.

### Developer Tests and Notes

- After the Djot-first removal, the permanent offline suite passed 1,634 tests. The final one-time
  name checks found zero Marp references in `slide_lib/` and `tests/`, and no Python bytecode-cache
  directories remained.
- The exact `./build_slides.sh genetics` workflow found only the eight recursive Djot sources and
  produced 24 PPTX, ODP, and PDF files. Strict eight-deck lint and the Djot native-layout E2E passed.
- A fresh 62-slide Lecture 02e ODP import passed strict Jotdown validation and native parsing. Its
  source table parsed back as one native table, and split-run DNA sequences retained prime marks
  and restriction-enzyme cut markers.
- The permanent offline suite passed 1,869 tests, including CLI routing, import boundaries,
  pyflakes, typing, security, support-directory, root-script-budget, shebang, and link checks.
- One-time migration evidence passed for public help and eight-deck lint, representative Marp and
  Djot ODP builds through the same CLI, both native-layout PPTX-to-ODP-to-PDF E2Es, and the retained
  folder-build wrapper. The first sandboxed ODP attempt lacked `ps` access; the same command passed
  with the established LibreOffice preflight permission.
- The one-time eight-deck legacy-corpus acceptance and reproducibility gates passed: 378 source
  slides yielded 336 visible and 42 hidden slides, 167 reachable assets, 72 bounded source regions,
  96 review slides, and 186 image occurrences. References resolved only to files with no missing or
  extra assets, symlinks, or exact-full regions; an independent private regeneration reproduced the
  Djot, report, and asset corpus.
- One-time native acceptance passed: strict lint covered 8 decks, 336 visible slides, and 186 image
  occurrences; `build_slides.sh genetics`, both explicit native E2Es, and sequential `--format all`
  exports passed. Every deck retained matching PPTX, ODP, and PDF counts, editable text/direct images,
  and Lecture 02e retained its native table.
- Before the CLI-boundary migration, the permanence-audited suite contained 1,914 tests, including
  all hygiene checks. The two native PPTX-to-ODP-to-PDF E2Es also passed as one-time evidence. M5
  animation acceptance remains unclaimed only pending attended Impress playback.
- The permanence audit removed static CSS, tunable geometry and catalog assertions, redundant broad
  importer and topology proofs, and the duplicate native E2E. Focused behavior and safety tests
  remain, alongside two explicit native-chain runners for one-time acceptance.
- Converted backend tests to direct native-model construction or Djot fixtures. Retired tests whose
  only subject was Marp parsing, front-matter discovery, old class modifiers, or duplicate E2E
  migration proof; added permanent `.md` rejection, imported-table round-trip, and raw-run
  character-preservation tests.
- Removed the permanent CLI assertion for the retired `--to` flag because it was one-time migration
  proof rather than a current behavior boundary.
- Updated human guidance from the superseded front end to Djot for canonical source, build flow,
  layout slots, `md2pptx` borrowing, raw-markup avoidance, component-image wording, and normal local
  tooling. Removed obsolete guidance for the old parser, compatibility baseline, class-size option,
  theme workflow, survey work, and pre-selection naming decision.
- Recorded the instructor's test-triage and bytecode-cache guidance. An explicit `py_compile`
  diagnostic created two `__pycache__` directories despite `PYTHONDONTWRITEBYTECODE`; both were
  removed, and subsequent Python verification used `source source_me.sh` without explicit bytecode
  compilation.
- The final documentation refresh ran the current permanent offline suite: 1,689 passed.

## 2026-09-06

### Additions and New Features

- Added extended-Djot as a second source front end to the shared presentation-neutral IR and native
  editable PPTX -> ODP -> PDF pipeline. `.md` and `.djot` now dispatch by suffix without changing
  the Marp migration baseline.
- Added the registry-derived Djot directive contract, named-cell normalization, short canonical
  layout names, and the `multiple-choice` question/answer layout contract.
- Added the source-side parser, grammar, inline/block handling, source-only semantic lint, and
  regenerated eight-deck genetics Djot corpus on short layout names.

### Behavior or Interface Changes

- Replaced the long layout vocabulary with canonical short names and no alias layer. Named slots,
  including asymmetric panel layouts, now bind by declared name rather than source order.
- Made one-line attributes attach to the following element, complete image paragraphs component
  images, and multiple H2 lines on `title-slide` one subtitle region. `$inline$` and `$$display$$`
  are intentional local math syntax pending an editable native math owner.

### Fixes and Maintenance

- Updated pipeline, roadmap, TODO, grammar exploration, and corpus guidance to distinguish durable
  parser tests, source-only Jotdown/lint checks, native E2E, and attended Office acceptance checks.
- Recorded the passed Djot native-layout E2E through editable PPTX, LibreOffice ODP, and PDF,
  including gallery images and distinct multiple-choice shapes.

### Decisions and Failures

- `<= blue overlay` is recognized but deliberately reports a source-located "not yet supported"
  diagnostic; it has no silent approximation.
- M5 animation timing remains unimplemented and unverified. PowerPoint is absent on the available
  host, so timing XML, first-advance playback, and ODP animation survival await the attended
  experiment in [wp_a1_animation_fidelity.md](active_plans/reports/wp_a1_animation_fidelity.md).

### Developer Tests and Notes

- The PowerPoint-dependent fidelity experiment is a one-time attended check, not a permanent test.
  Fast tests remain offline and behavior-focused; the native chain remains explicit E2E evidence.

## 2026-09-05

### Documentation and Design Research

- Removed the standalone `REUSE_DECISION_MATRIX.md` and replaced its focused Marp prior-art
  comparison with `docs/MARP_ADJACENT_PROJECT_COMPARISON.md`. Kept
  `docs/RELATED_PROJECTS.md` as the broader visitor-facing related-project guide.
- Rewrote `docs/LAYOUT_LANGUAGE_SURVEY.md` as a literal, syntax-first thirteen-fixture comparison
  of Markdown presentation languages and real Marp-extension approaches. The survey now frames the
  two remaining branches -- extend Marp or adopt another format -- without selecting either;
  classic Marp is retained only as the upstream compatibility baseline.
- Restored `docs/MARP_SYNTAX_GUIDE.md` to its single purpose: classic Marp Core v5 and Marp
  CLI-compatible syntax. It does not define the current native transition or an unapproved future
  extension.
- Recorded the native `_cell` marker plan as a provisional candidate rather than an adopted public
  language, and deferred both parser work and a parallel extension guide until the language choice.
- Recorded the instructor's canonical slide-language requirements in both human guidance and design
  decisions, independently of any grammar choice.
- Clarified older guidance and related-project framing so classic Marp remains the current migration
  baseline rather than a prematurely selected long-term spatial-layout language.
- Expanded the language requirements and survey with named LibreOffice-style layout patterns,
  predictable Markdown image placement, minimal inline/display equations, low-punctuation
  hand-authoring, and editable native-object output.
- Clarified that required equation support means LaTeX-compatible or similarly capable,
  hand-writable syntax for both inline and display mathematics.
- Corrected the authoring-property scorecard's GFM separator row so its ten columns render on
  GitHub.
- Reclassified MarkItDown as a PPTX-to-Markdown source-import bridge and added a descriptive,
  equal-weight average to the authoring-property scorecard.
- Recalibrated the MDPR YAML override model as readable and practical to hand-write, while retaining
  the title-addressed sidecar as its source-coordination limitation.
- Reframed the scorecard as language-format completeness against the instructor wishlist, replacing
  the pipeline-oriented native-parse score and adding a score for MarkItDown's Markdown output.
- Clarified that every language branch retains the repository-owned parser and native editable-object
  pipeline; adoption concerns source grammar and semantics, not an external renderer or build stack.
- Added a rendered-legacy lecture layout survey and recorded simple on-advance reveals as a
  language requirement: appear an authored item or outline one bullet at a time, without requiring
  a general animation language.
- Completed the literal source comparison and language-only scorecard dimension for simple staged
  reveals; it distinguishes list builds, arbitrary-item appearance, nested-list behavior, and
  comment or container burden.
- Narrowed and sorted the wishlist-completeness scorecard, moved its rationale to a separate
  context table, and recorded Quarto Reveal's bare `. . .` arbitrary-content pause as a full
  simple-reveal capability.
- Added an open presentation-language choices record: retain GFM-readable content, use Djot's
  grammar discipline as a reference, and resolve every structural ambiguity before adopting a
  small, independently named language. Condensed the survey's score explanation and updated its
  post-survey status.
- Set aside the comment-based `_cell` transition candidate. Reframed the roadmap and TODO around a
  grammar-design gate before any parser, exporter, importer, deck, or language-guide work.
- Expanded the open language-choice record into a brainstorming page that preserves the Djot/GFM
  tradeoff, GitHub-readable-source goal, low-character authoring preference, and grammar questions.
- Corrected the brainstorming record: the language discussion retains one canonical source and does
  not propose a separate GFM review copy alongside a presentation source.
- Corrected the source-language status: GFM is an attractive candidate, not a selected foundation;
  the brainstorming, survey, roadmap, and TODO now retain GFM, Djot, and a Marp-derived surface as
  alternatives to compare before approving extension syntax.
- Added a separate, timestamped analysis of the supplied John MacFarlane interview transcript so
  its Markdown and Djot lessons remain evidence for the language choice rather than informal memory.
- Clarified that GitHub cannot be a faithful slide renderer. The brainstorming page now records an
  optional, derived read-only GFM display projection as a possible browsing artifact, not a second
  source or a constraint on the source-language decision.
- Added direct CommonMark, GFM, Djot, and Djot-reference-implementation links to the presentation
  language brainstorming record, distinguishing document-language features from missing slide
  spatial semantics.
- Recorded the instructor's current preference to extend Djot, particularly its lack of indented
  code blocks and simpler list-item indentation rule, without treating the source foundation or
  spatial grammar as settled.
- Added an exploratory Djot slide-extension syntax inventory. It records Djot constructs and
  parse-valid free block-level surface without assigning slide, layout, slot, gallery, reveal, or
  styling semantics.
- Recorded the instructor's requirement that a Djot-based slide language preserve Djot's parsing,
  composition, simple-source, attributes, and generic-container design goals.
- Clarified that hard-wrap-friendly source is a specific instructor priority and that Djot attributes
  remain content metadata rather than a second layout syntax.
- Replaced the missing local automatic-caption transcript link in the Djot interview note with the
  source video, while retaining the note's limits on caption-derived evidence.
- Recorded the instructor's preference to avoid paired punctuation and C++/CSS-style attribute bags
  in normal slide authoring. Retained one-line Djot attributes only for exceptional overrides and
  rejected multiline brace structures.
- Recorded the requirement for a visibly distinctive future slide-boundary line, while retaining
  `@`, `=>`, and `%%` as speculative Djot-compatible surface rather than assigning grammar roles.
- Made ordinary `![alt](path)` the official component-image form, reserving it from all extension
  structure without adopting Marp-specific image modifiers.
- Made `$inline$` and `$$display$$` the official mathematics forms for a repository-owned
  MathJax-compatible port, reserving those delimiters from extension structure.
- Kept gallery capacity and bounded reveal behavior as language requirements while leaving their
  syntax and floating-answer geometry unassigned.
- Expanded the unassigned Djot syntax inventory with `&&`, `|||`, `. . .`, `::name::`, and paired
  `%%name%%` forms found in or suggested by the layout-language survey; documented their Djot
  collision and parser-testing boundaries without assigning them semantics.
- Recorded the instructor's preference to examine one-sided `%% name` markers without inheriting
  Marp Extended's XML-like closing pairs or assigning a scope rule.
- Recorded Kova's `|||` as notable delimiter prior art, while preserving the preference against
  triple repeated characters in ordinary source.
- Corrected the Djot inventory table: moved reserved dollar mathematics out of the free-surface
  table and moved Kova's literal three-pipe specimen into a standalone GFM `<pre>` block so Markdown
  table renderers preserve the row.
- Added `===== layout: name` to the unassigned Djot surface inventory and distinguished it from
  Djot's three-character `*` and `-` thematic-break rule.
- Recorded that a hyphen-run boundary with trailing layout text avoids a thematic break but is
  changed by Djot smart punctuation, so it is not source-glyph-stable.
- Recorded the instructor's stronger hands-on preference for Djot after testing its line-level
  parsing and rendering behavior.
- Recorded the provisional Djot grammar direction: `=== layout: <name>` starts a slide and selects
  its layout, `@<slot>` selects a layout-defined slot, and `<=`/`=>` attach bounded animations to
  preceding/following content. Kept parser adoption, layout names, and floating-answer geometry open.
- Made `multiple-choice` the first official future-language layout. Its required `@question` and
  `@answer` slots show the prompt and choices initially, then reveal the short answer automatically
  in a fixed bottom-right popup; open-ended questions use another layout.
- Recorded the full future-layout scope: every default LibreOffice layout plus the custom
  `multiple-choice` layout. Retained `#` titles and `##` subtitles only where a layout declares
  their regions, and preserved compatible Marp content apart from explicit Djot-language changes.
- Required a fast, source-only, pyflakes-level linter for the future language. It reports structural
  mistakes with source locations while geometry, overflow, native animation, and visual checks stay
  in separate validation lanes.
- Clarified that grammar validation uses small, inline source cases rather than a shared test-data
  corpus, consistent with the repository pytest policy.
- Recorded the future intent to separate reusable slide-language work from personal lecture content,
  without authorizing a migration, duplicate content authority, or premature repository split.
- Surveyed the six `genetics/lect02*` legacy decks against the proposed language. Found no gap for
  worked-problem sequences, multiple-choice answers, or Marp images. `<= blue overlay` needs no
  extra figure-anchor syntax: in a slot with exactly one Marp image, overlay blocks bind to that
  image. The linter rejects an unanchored or ambiguous overlay, never adding a general styling
  language.
- Confirmed settled Djot content forms from the Lecture 02 survey: tables, inline verbatim, and
  fenced code blocks inherited from Djot, plus MathJax-compatible `$inline$` and `$$display$$`
  mathematics. These cover sequence text without a custom DNA delimiter.
- Defined an unquoted literal target for inline `blue overlay` highlights. The target must match one
  preceding logical item; this preserves hard-wrapping and avoids quoting or escaping DNA primes.
- Made extended Djot the settled successor-language foundation. Elevated strict Djot compatibility
  to the top language requirement: source must pass every parser, formatter, editor rule, and linter
  in a future pinned compatibility suite before the extension linter evaluates slide semantics.
- Defined an ASCII-to-Unicode native projection after strict Djot validation. The literal ASCII token
  `&prime;` maps to Unicode code point U+2032 PRIME; this is a narrow project vocabulary, not a
  general HTML-entity parser, and does not rewrite verbatim or raw content.
- Selected the upstream `.djot` suffix for extended-Djot presentation source, retaining standard
  Djot tooling association instead of inventing a slide-specific filename extension.
- Added an experimental, ODP-derived extended-Djot corpus for all eight `genetics/lect0*` decks:
  336 visible slides, source-hidden slides excluded, component images retained, and presenter notes
  deliberately omitted. Added dedicated ODP/PPTX-to-Djot import commands and a fast structural
  linter. Pinned Jotdown 0.10.0 as its native-first parser and verified all eight sources through
  it; formatter, editor-rule, and linter-suite selection remain open. `source_me.sh` now exposes
  an installed Cargo-bin validator to repository commands. The Marp import commands remain unchanged.
- Clarified that the pinned native parser is the compatibility suite's raw-Djot syntax-validation
  lane; the extension linter supplies the separate slide-semantic diagnostics.

### Fixes and Maintenance

- Synchronized shared style guides, tests, and repository support files from the starter template.
## 2026-09-01

### Additions and New Features

- Added `docs/MARP_SYNTAX_GUIDE.md` as the concise authoring contract. It distinguishes standard
  Marp syntax from repository-specific layout meanings, documents the supported native subset, and
  sets `paginate: false` as the no-page-number authoring convention. Its external-links section
  separates primary Marp Core v5 and Marpit references from secondary quick-reference material.
- Added `docs/ROADMAP.md` and `docs/TODO.md` to separate ordered Marp+ capability work from small
  next actions. The first milestone replaces blockquote layout cells with explicit named `_cell`
  markers while retaining the syntax guide as the current production contract.

### Behavior or Interface Changes

- Replaced the browser-rendered, flattened presentation baseline with the native-output contract:
  repository-owned Python interprets authoritative Marp Markdown into editable PPTX objects, then
  LibreOffice writes editable ODP and PDF from that ODP.
- Added bounded Marp multi-class H1 display presets (`font-size-64` through `font-size-200`). The
  source-located typed request applies only to the editable top-level H1, rejects title-region
  overflow instead of shrinking, and makes `font-size-200` a 150-point native Office title.
- Split native ownership: `marp_lib/marp_parser.py` interprets the supported Marp language subset,
  `marp_lib/layouts.py` owns layout builders and geometry, and `marp_lib/native_export.py`
  orchestrates native PPTX, notes, pagination, and conversion. The destination-named commands retain
  single-deck ownership, while `build_slides.sh` retains folder-level ownership.
- Implemented every LibreOffice layout-grid pattern as a distinct native builder: `blank`,
  `title-only`, `title-slide`, `title-content`, `centered-text`, `title-two-content`,
  `title-content-and-two-content`, `title-two-content-and-content`, `title-content-over-content`,
  `title-two-content-over-content`, `title-four-content`, `title-six-content`,
  `vertical-title-vertical-text`, `vertical-title-text-chart`, `title-vertical-text`, and
  `title-two-vertical-text-clipart`, plus the repository `gallery` layout.
- Made one explicit native layout class mandatory per canonical slide and established top-level
  blockquotes as multi-cell content in layout reading order.
- Defined Marp as an authoring-language specification only. The newly added local `marp-core` and
  `marp-cli` clones provide conformance evidence outside the production dependency/runtime graph.
- Added destination-named `tools/marp_to_pptx.py` and `tools/marp_to_odp.py` commands backed by one
  validated `marp_lib/native_export.py` implementation.
- Replaced the presentation-build output stream with one shared Rich interface for folder and
  single-deck commands. Builds now leave a borderless artifact-size table, relative output paths,
  and one elapsed total while keeping current deck stages transient.
- Made `tools/marp_export.py` accept either one Markdown file or a folder. Folder builds now select
  sorted direct-child Marp decks and run them through one Python process behind the stable
  `build_slides.sh FOLDER` wrapper.
- Calibrated native Office typography from CSS pixels and fitted native text to its assigned layout
  region; balanced nested-list columns by height and restored paragraph separation in native cells.
- Preserved Markdown links, slide title metadata, and component-image descriptions in native
  PPTX and ODP output.
- Added deterministic per-layout source validation that rejects blocks which a layout would omit
  or place in overlap, with a clear diagnostic for the source author.

### Design Decisions

- Adopted Marp Core v5 as the only upstream authoring and conformance baseline. The version-pinned
  reference snapshot is 5.0.1 at commit `06c5a54`; v4 and earlier behavior and highlight.js theme
  contracts are outside scope, while optional v5 plugins require explicit native capability
  decisions.
- Recorded full-slide rasterization and raster fallbacks as failed presentation results. Normal
  presentation builds require no browser, Marp code, Marp CLI, Node, or rendering engine.
- Recorded the heavily edited local `md2pptx` clone as implementation prior art for native objects,
  image fitting, list construction, and notes while retaining Marp syntax rather than its dialect.

### Fixes and Maintenance

- Replaced disposable LibreOffice `UserInstallation` profiles with the established user profile,
  centralized conversion in `marp_lib/libreoffice.py`, added `--norestore`, and made a running
  LibreOffice desktop session an actionable preflight error. This removes repeated first-profile
  macOS task-policy diagnostics while retaining temporary directories for converted artifacts.
- Applied the documented Impress PDF filter with 70 percent JPEG quality, a supported 150 DPI image
  limit, and `SelectPdfVersion=3` for PDF/A-3b rather than passing Writer's PDF filter or an
  unsupported 100 DPI value.
- Hardened the native typed boundary: CRLF Markdown preserves physical source lines, retired
  `slide_*_source` raster names fail at their image line, and layout, cell, and overflow errors
  identify the most precise authored block or cell.
- Applied OpenDyslexic to ordinary and inline-code native text while reserving PT Sans Narrow for a
  displayed literal URL; labeled hyperlinks retain their native hyperlink and ordinary typeface.
- Gave all seventeen registry entries distinct named native builders and aligned the vertical
  preview contracts with fixed native geometry and one-root-body authoring.
- Captured LibreOffice stdout and stderr so successful conversions remain quiet while failed
  conversions retain actionable diagnostics in the concise expected-error panel.

- Corrected the native authoring contract: formatted/link/inline-code runs, nested lists, component
  images, blockquote cells, directives, and presenter-note comments are supported; tables and fenced
  or indented code report a source location until native editable-object owners are implemented.
  Documented `gallery` as two through six component images and `title-content` as the one-image
  layout.

### Developer Tests and Notes

- Added the native semantic E2E gate. Run
  `source source_me.sh && python3 tests/e2e/e2e_all_native_layouts.py` from an ordinary macOS user
  session. It inspects native PPTX and editable ODP text, lists, links, notes, component images,
  slide count, and full-slide-image absence.
- Hardened the ODP E2E gate with `defusedxml`, numeric page-relative full-slide-image detection,
  and verification that component-image descriptions survive editable ODP conversion.
- Kept focused permanent pytest coverage for folder selection, progress ordering, LibreOffice
  capture and diagnostics, concise single-format summaries, expected failures, and unexpected
  defect propagation. Removed redundant single-file discovery and broad presentation-detail tests
  after applying the permanent-test checklist. The complete fast suite reports 937 passes.
- Classified the redirected and terminal `./build_slides.sh genetics/` runs as one-time
  implementation checks. Both modes produced all six PPTX, ODP, and PDF artifacts; redirected
  output was static and ANSI-free, terminal progress was transient, and successful LibreOffice
  conversions emitted no chatter.

## Historical renderer and migration records

The entries below retain evidence from the former Marp CLI/browser-rendered PPTX path and earlier
migration work. They are historical records, not the current presentation contract, except where
an entry explicitly identifies the current native package or native semantic E2E gate above.

### Additions

- Added `docs/LAYOUT_LANGUAGE_SURVEY.md`, a 20-project comparison of layout grammars, visual
  theme catalogs, output transformations, and validation approaches.
- Added a one-page prior-art matrix for all 20 reviews, focused on stronger task solutions,
  pipeline models, and Marp theme possibilities.
- Added `docs/PIPELINE.md` as the canonical component architecture for the import and build engine,
  including its interfaces, ownership boundaries, success properties, verification lanes, extension
  seams, and current architectural risks.
- Added a related-projects guide that inventories every local prior-art clone, distinguishes
  themes, templates, importers, and output converters, and records what to adapt or reject.
- Added 20 individual repository reviews under `docs/OTHER_REPOS/` covering content, licenses,
  ideas, code and function candidates, themes and assets, architectural fit, and a concrete reuse
  decision for every repository present when the audit began.
- Added a bounded Python ODP importer that preserves structured slide text, content images, notes,
  visibility, and geometry without using full-slide screenshots as converted content.
- Added a central genetics Marp theme with accessible teaching colors and reusable lead, two-pane,
  and auto-fitting gallery layouts.
- Added `build_slides.sh` to generate PDF and PPTX with Marp 4.5.0 or newer and convert the PPTX
  into a classroom ODP with LibreOffice.
- Added installation, usage, design, human-guidance, and measured palette documentation plus a
  useful repository landing page.
- Added the first canonical migration candidate, `genetics/lect01b-genetic_disorders.md`, with its
  extracted content assets.
- Added `genetics/lect01a-course_intro.md` as the first recurring announcements/course-information
  deck with all 31 visible source slides represented as editable Marp layouts.
- Added deterministic importer tests for simple conversion, unsafe archive paths, and safe
  presenter-note comments, including drawing-page visibility and style-cascade behavior.

### Behavior Changes

- Made all six presentation command modules directly executable with canonical Python shebangs,
  `argparse` entry points, and aligned executable permissions; `odp_visibility.py` now reports each
  source slide's resolved visible or hidden state.
- Made the repository Python-only and moved Marp ownership from npm to the Homebrew `marp-cli`
  formula; Node remains only a transitive formula dependency.
- Established a one-way migration contract: legacy ODP is imported once, Marp Markdown becomes
  authoritative, and generated ODP is used for classroom presentation.
- Protected canonical Markdown by refusing to overwrite an existing deck or asset directory.
- Made hidden-slide detection preserve the source presentation sequence while excluding its nine
  hidden `lect01a` slides.
- Documented the importer and build trust boundaries: archive validation does not sandbox the
  LibreOffice ODP-to-PPTX normalization step, so legacy inputs must be instructor-owned and trusted.
- Made `build_slides.sh` reuse the same exporter as the destination-named commands so PPTX-only,
  ODP, and all-output workflows enforce one conversion contract.
- Made `build_slides.sh` batch-build every Marp deck directly inside a selected folder while
  keeping the destination-named Python converters single-deck commands.
- Recorded the instructor's stricter slide-layout contract: use the simple default layout
  vocabulary, keep all authored content inside the 1280x800 frame, use OpenDyslexic exclusively,
  and reserve PT Sans Narrow for long URLs.
- Established post-conversion polish as a separate phase from mechanical ODP import, with built-in
  Marp layouts preferred before adding custom per-slide geometry.
- Rejected full-slide PNGs as conversions: source renders are visual QA evidence only, never Marp
  slide content.
- Preserved the 31-slide `lect01a` teaching sequence while replacing all 11 source-rendered slides.

### Design Decisions

- Recorded the search for a coherent Marp extension language: CDL is a language-design reference,
  and Marp CLI is excluded from the future extension rendering path.
- Chose simple editable layouts over automatic reconstruction of arbitrary ODP drawing geometry.
- Chose successive build slides for classroom reveals because Marp browser fragments do not become
  native animations in the generated ODP.
- Centralized recurring visual layout in `themes/genetics.css` instead of raw per-slide HTML or XML.
- Simplified split-slide typography and recurring Discord and office-hours image placement so the
  weekly-edit deck remains readable without per-slide HTML.
- Standardized authored slide text on OpenDyslexic and displayed URL text on PT Sans Narrow in the
  central genetics theme.
- Limited PT Sans Narrow to slides that explicitly display long URLs; ordinary link labels continue
  to use OpenDyslexic with all other authored text.
- Made content images auto-fit their theme-owned panes and gallery cells instead of using per-image
  pixel dimensions.
- Made multi-image panes and galleries divide their available width from the number of images at
  render time rather than encoding two-image or three-image dimensions in the slide source.
- Reserved theme-owned gallery space for pagination so automatically fitted images do not sit
  beneath the slide number.
- Added a shared auto-fitting single-figure layout so screenshots remain below their Markdown title
  without per-slide dimensions or overlap.
- Chose structured slide-object extraction over OCR and measured temporary PPTX plus `python-pptx`
  as the geometry-normalization path for inconsistent legacy ODP layouts.
- Kept all `OTHER_REPOS/` clones as prior art only; future repository-owned work may adapt their
  ideas without adopting their code, dependencies, Markdown dialects, or VS Code workflows.
- Recorded an ordinary Marp-rendered PPTX followed by LibreOffice conversion as the temporary
  classroom baseline after a measured bakeoff; it was later retired for native output.

### Developer Tests

- Ran the repository-owned suite as `python3 -m pytest tests`: 827 passed and 1 skipped, including
  239 focused ASCII, Markdown-link, and source-line-limit checks against all 20 new reports.
- Confirmed `git diff --check` is clean with the new untracked reports represented in an isolated
  temporary Git index; the real index and staging area were not changed.
- Verified the `lect01a` ODP-to-PPTX bakeoff as 40 source slides, the same 9 hidden slides, one
  preserved source note slide, and separate text/image geometry on every former rasterized slide.
- Verified Marp and LibreOffice generate matching 23-slide PDF, PPTX, and ODP outputs and that
  LibreOffice can reopen the generated ODP and export all 23 pages at 16:10, with all 23 note
  parts and about 6,460 note characters preserved.
- Ran the official Marp `--pptx-editable` bakeoff: it yielded native objects but lost all notes and
  visibly broke two-pane geometry, so it is reserved for manual experiments on simple slides.
- Verified the Markdown-only two-pane layout through Marp, PPTX, LibreOffice ODP, and a rendered
  visual inspection.
- Measured every theme foreground at the 5.5:1 target: 16.27:1, 7.41:1, and 6.31:1 against white.
- Ran `bash -n build_slides.sh`, `git diff --check`, and the non-index-dependent pytest suite:
  661 passed and 1 skipped. The focused importer and import-requirements checks add 49 passes.
- Reconciled the human guidance, implementation decisions, usage guide, and README with the open
  output-design direction; documented the related-project inventory without linking ignored output
  artifacts.
- Confirmed `brew bundle check` reports every Brewfile dependency installed and Marp CLI reports
  version 4.5.0.
- Verified both destination-named commands against `lect01a-course_intro.md`; PPTX-only export and
  PPTX-to-ODP conversion completed successfully, and 302 focused hygiene tests passed.
- Verified the folder-level batch command discovered and regenerated both genetics decks as PDF,
  PPTX, and ODP; `bash -n build_slides.sh` passed, and the project-owned suite reported 683 passed
  and 1 skipped.
- Rendered all 31 `lect01a` slides after post-conversion polish and inspected both a full contact
  sheet and the dense split layouts at full size; no authored text or images cross a slide edge.
- Compared structured and OCR extraction across the 31-slide source PDF: structured extraction
  retained 99.6% of estimated words versus 95.8% for OCR, confirming OCR is unnecessary here.
- Ran the complete repository suite: 683 passed and 1 skipped.
- Rebuilt both canonical decks with Homebrew Marp 4.5.0 and regenerated their rendered PPTX and
  classroom ODP outputs.
- Reopened both final ODP files with LibreOffice 26.2.5.2 and exported them as 16:10 PDFs: `lect01a`
  retained 31 pages and `lect01b` retained 23 pages.
- Inspected full ODP-readback contact sheets plus the dense lists, three-image microscope gallery,
  and tall carrier-report panes; no authored text or teaching image crosses a slide edge.
- Ran six independent audit passes covering plan conformance, tests, style, documentation, dead
  code, and comments; after the low-risk repairs, the project-owned suite reported 717 passed and
  1 skipped, and 221 focused command/documentation hygiene checks passed.
- Validated the component-focused pipeline architecture with ASCII, line-width, Markdown-link, and
  full project checks; the suite reported 722 passed and 1 skipped.

### Fixes and Maintenance

- Fixed the importable `odp_visibility.main()` entry point, aligned the standalone PPTX importer's
  shebang and executable permission, removed a dead duplicate presenter-note encoder, and documented
  both diagnostic import commands and their bounded trust contract.
- Removed the redundant `split` and `compact` classes from `lect01a`: Marp's `bg right` directive
  already reserves the text pane, so the old theme padding was constraining it a second time.
- Replaced all `slide_*_source.png` references in `lect01a` with editable text and extracted content
  images while keeping the source slide count unchanged.
- Replaced the six remaining `lect01b` full-slide fallbacks and two fixed-width galleries with
  structured Markdown and shared auto-fitting layouts while preserving all 23 source slides.
- Mapped the two tall-image carrier-report pairs to the shared figure layout plus Marp's native
  auto-fitting right pane after rendered review exposed intrinsic-height distortion in a generic
  one-row gallery and in paired replaced elements.
- Kept the second carrier-report slide as a visually untitled continuation after Marp repeatedly
  painted its tall screenshot over the redundant repeated heading; the title remains in source as
  a continuation comment and the 23-slide sequence is unchanged.
- Made the Marp exporter reject retired source-fallback classes and `slide_*_source` image
  references before rendering.
- Added required shebangs to the initial executable Marp commands and normalized four legacy
  line-separator characters in `lect01b`; `odp_visibility.py` was later promoted from a library
  helper to a documented command.
- Synchronized shared style guides, tests, and repository support files from the starter template.
