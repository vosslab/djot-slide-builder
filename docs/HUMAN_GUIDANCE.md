# Human guidance

<!-- VENDORED HEADER: START -->
Record the durable guidance Neil Voss states, or approves for preservation here, in his own words:
first person or close paraphrase, one to three lines per bullet. Material he supplies as a source
may inform [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) once it is settled, and an entry of uncertain
origin belongs there too. Rules: [REPO_STYLE.md](REPO_STYLE.md).
[PROPAGATED HEADER - ENTRIES BELOW ARE YOURS]
<!-- VENDORED HEADER: END -->

## Current presentation decision (2026-09-09)

- ODP is the sole editable artifact. LibreOffice makes every classroom PDF and every generated
  review PDF from that ODP. Save legacy PPTX as ODP in LibreOffice before one-time import.

## Slide migration and presentation

- This is a requirement 1 slide in original source is 1 slide in djot and 1 slide in output, no taking one
  slide and making it three to get all of the content in.
- I want better formatting match to the original slides (not byte nor exact) but like title and section
  layouts should be centered; the outline layouts do appear better
- images must always maintain their original aspect; never stretch images, it always looks wrong.
- I do not own any microsoft products, Powerpoint is not a blocker, we only use PPTX because
  python supports PPTX better than ODP
- An existing ODP is imported once; Djot and its local assets then become authoritative.
- Do not show slide numbers; they encourage the audience to track remaining time and watch the
  clock instead of the presenter.
- Compile canonical Djot through repository-owned Python into a shared format-neutral layout plan.
  Build native editable ODP directly and make PDF from that ODP through LibreOffice.
- Keep LibreOffice closed, preflight that desktop state once, then convert each generated ODP in
  source order with direct `soffice --headless --norestore --convert-to --outdir` commands.
  Use the two-second settling interval from `~/nsh/junk-drawer/makePDFSlides.sh` between files.
- Presentation PDFs use `pdf:impress_pdf_Export`; the command verifies its expected PDF before
  continuing. Do not add profiles, GUI/AppleScript control, process groups, or timeout cleanup.
- `~/nsh/junk-drawer/makePDFSlides.sh` is workflow evidence. Quality 70, image reduction,
  maximum image resolution 100 DPI, and `SelectPdfVersion=3` are current defaults, not gates.
- Implement the twelve standard LibreOffice grid layouts as native editable objects. The registry
  records project vocabulary and extensions in [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md). The grid
  is a visual catalog, not a rendering dependency.
- Give every slide exactly one explicit layout. Keep `-` as ordinary list syntax and use named
  `@<slot>` directives for layout structure.
- Preserve text, lists, component images, links, layouts, and presenter notes as native objects.
- Use one consistent, rule-based Djot theme rather than preserving slide-specific quirks. Use the
  old lecture decks only as visual guidance: a shallow blue-to-white top band, centered standard
  titles, sensible margins, and hierarchical bullets with hanging indents and aligned wraps.
- Use `genetics/xlect99-template_2023.otp` solely as the master-slide theme authority. ODP and PDF
  are the classroom outputs.
- Keep every presentation at 16:10. The physical page dimensions are not important; authoring and
  layout should use a stable 1280x800 logical canvas instead of paper-size assumptions.
- Do not use a browser or CSS as the presentation theme engine. Preserve theme and list behavior as
  native ODP presentation semantics so LibreOffice can edit and export them.
- Remove full-slide and large composite screenshot substitution from import and production. Keep
  genuine source figures, photographs, diagrams, and intentional screenshots as normal images.
- An imperfect native reconstruction is useful diagnostic information. Normalize hard legacy slides
  into standard Djot layouts, leave limitations visible, and simplify or redesign them rather than
  photographing the old rendering.
- Simplification is the overall goal. Present the same instructional content through an existing
  Djot layout whenever possible instead of preserving the original slide composition.
- Treat every full-slide raster image or raster fallback in generated ODP or PDF production
  as a failed product result. A browser is not a normal build dependency.
- Use the heavily edited `md2pptx` clone for native-object implementation ideas while retaining
  Djot syntax as this repository's authoring contract.
- Make `deck_tools.py` the sole user-facing application CLI and keep reusable application behavior
  in `slide_lib/`.
- Let `./build_slides.sh genetics` recursively build only the Djot slide files below `genetics/`.
- Delete the old `tools/*.py` wrappers because this pre-production repository has no external
  compatibility callers. Add `launchers/` only for a concrete independent launcher use case.
- Keep permanent tests on meaningful application behavior. Treat rename sweeps and representative
  CLI or end-to-end runs as one-time migration evidence.
- Keep presentation-build output concise: show the current deck and stage transiently, then leave
  one compact summary with relative paths, file sizes, and one elapsed total. Hide successful
  third-party conversion chatter.
- Prefer simple teaching layouts instead of copying arbitrary legacy ODP geometry. Keep authored
  text and images within the 1280x800 16:10 frame, and fit component images with `contain`.
- Preserve the teaching sequence unless I explicitly approve a change.
- My ODP slides are hand-authored structured documents, not scans; normal conversion uses text and
  image objects rather than OCR.
- Use OpenDyslexic for ordinary slide text and PT Sans Narrow only when a long URL is displayed.
- Make standard titles default to 36 pt and ordinary body text default to 28 pt.
- Use shrink-on-overflow for native presentation frames only after build preflight proves the text
  remains above a readable floor; LibreOffice's unbounded manual shrink is not the floor owner.
- I want five universal gestalt dimensions for visual review; keep objective gates and standalone
  versus migration review separate, and make the concern reason more important than the total.
- Calibrate roughly 20 pages across vision models before setting precision or an attention threshold;
  centralize rubric provenance instead of repeating brittle source-line references.
- I want visual review to use the original slide PDF and the generated ODP rendered to PDF by
  LibreOffice. Assess the generated page on its classroom value and assess the pair for functional
  visual equivalence: preserved teaching emphasis, grouping, relationships, balance, and character.
- Use positive reviewer prompts: give appropriate PDF artifacts, ask for effects with a reason, and
  use deterministic checks for mechanical facts. Small language models follow direct desired-action
  phrasing; omission is often stronger than naming unwanted actions.
- Use LibreOffice for every ODP-to-PDF conversion so generated review artifacts and classroom PDFs
  share one consistent conversion authority.
- Make generated title and content objects real LibreOffice layout members. Reapplying One Box must
  reuse the authored title and body instead of adding empty placeholders over them.
- Every implementation milestone must complete without my participation. When I am unavailable, the
  manager and subagents use captured fixtures, desired XML contracts, and deterministic package-XML
  transitions.
- The autonomous acceptance path also uses headless LibreOffice preservation, PDF/render metrics,
  and automated reveal-state checks.
- Use OpenDyslexic for ordinary and inline-code runs. Apply PT Sans Narrow only to a displayed
  literal URL; keep ordinary linked labels in OpenDyslexic with their native hyperlink.
- Treat `slide_*_source` raster names as retired full-slide fallback evidence, not component images.
- Use lots of images and aim for a visual image on every slide.
- Hold image-bearing slide PNGs out of publication until their copyright status is assessed;
  text-only slide-page screenshots may be published in `docs/screenshots/`.
- Avoid raw HTML or XML in Djot. Keep visual geometry in the shared native layout registry.
- A normal instructor workflow must not require VS Code, npm, TypeScript, or Node.
- This pre-production repository uses direct replacements when terminology or architecture changes.
  Improve foundational schemas, contracts, abstractions, and ownership boundaries directly; do not
  preserve compatibility shims or legacy support.

- Keep a separate Markdown review for every repository in `OTHER_REPOS/` that identifies its
  content and whether its ideas, code, functions, themes, or assets fit this project.
- Evaluate these repositories for useful ideas rather than license analysis when source copying is
  out of scope. Prioritize correctness, maintainability, validation, and delivery risks over
  trivial details.
- Review each repository for whether it improves an active task or offers a stronger pipeline model.
- Judge the choice by hand-authoring quality, ordinary nested Markdown, structural punctuation and
  comment burden, semantic layout names, and a clean mapping to typed editable native slide
  objects. Treat the repository Python parser and exporter as the rendering boundary.
- The future slide-language wishlist is:
  - Multiple named teaching layouts, including title slide, title plus content, two equal columns,
    asymmetric columns, stacked regions, 2x2, 3x2, and related LibreOffice-style patterns.
  - Ordinary nested bulleted and numbered lists inside every content region.
  - Simple Markdown image insertion with predictable placement inside a named region.
  - Equation support, using LaTeX-compatible syntax or a similarly capable hand-writable equation
    syntax, for both inline and display math without turning the language into a
    scientific-publishing framework.
  - Simple teaching animation: on an advance, make an authored item appear or reveal an outline one
    bullet at a time. Complex motion paths, timing tracks, and animation choreography are not needed.
  - Hand-writable source with very little structural punctuation or comment scaffolding.
  - Native editable output: text, lists, practical equations, and images remain real ODP objects,
    never slide screenshots.
- These are requirements for the language choice, not approval for a particular grammar.
- Regardless of the chosen source language, the repository will own the parser, native editable
  ODP builder, LibreOffice conversion boundary, and validation. "Adopt a language" means adopt or adapt
  its source grammar and semantics, never its runtime or presentation pipeline.
- No surveyed presentation format is a direct-adoption target. The successor language is extended
  Djot; its implemented spatial grammar remains adaptable as new native owners gain evidence.
- Require accepted source to remain strict Djot and pass the pinned compatibility suite before
  extension lint applies slide semantics. No slide feature may waive a Djot failure.
- Treat the pinned native Djot parser as a syntax-validation lane of that suite: in ordinary use, it
  is a validator/linter for raw Djot structure. The extension linter adds only slide-specific
  diagnostics after the parser validates the underlying document.
- Hands-on Djot specimens confirm this choice: its visible, line-by-line parsing behavior, removal
  of indented code blocks, and simpler list-item indentation rule make authored source easy to read
  and reason about.
- I want the extended Djot language to retain Djot's design goals: linear and local parsing, simple
  list and inline behavior, hard-wrap-friendly source, uniform composition, preserved attributes and
  containers, and the simplest syntax consistent with those constraints.
- I particularly value source that remains readable when hard-wrapped. Keep every slide directive
  short and single-line so wrapping ordinary teaching prose never creates or changes structure.
- Avoid braces and other paired punctuation in normal slide authoring. Retain one-line Djot
  attributes for exceptional content or renderer overrides, never as the default layout, slot,
  gallery, reveal, size, or color vocabulary; never use multiline brace structures.
- The Djot slide surface uses `=== layout: <name>` to start a slide and choose its layout, and
  `@<slot>` to select a predefined slot from that layout. The parser and layout catalog implement
  these spellings while keeping new grammar decisions evidence-driven.
- The Djot layout catalog includes every default LibreOffice layout plus the custom
  `multiple-choice` layout. Preserve familiar Markdown content where compatible with Djot;
  `=== layout:` starts each slide, and extra image modifiers are not adopted.
- In title-bearing layouts, `#` supplies the title; in subtitle-bearing layouts, `##` supplies the
  subtitle. Layouts without title placement reject both headings.
- Use `<= <action>` as a terminal animation directive for the preceding item or block and
  `=> <action>` as a prefix directive for the following block. `=> cascade appear` reveals the
  following outline or list one top-level item at a time in source order.
- Kova's `|||` split delimiter is notable prior art, but triple repeated characters are not ideal for
  ordinary authoring.
- `multiple-choice` requires `@question` and `@answer`. The question and choices show initially;
  the answer is revealed in an editable, measured layout-owned popup selected in the available
  left or right region. Use another layout for open-ended questions.
- Reserve `![alt](path)`, `$inline$`, and `$$display$$` for component images and mathematics.
  A repository-owned adapter may accept the math surface without adopting extra image modifiers.
- The Djot language supports normal Djot syntax. Use Djot tables for tabular source, inline
  verbatim for short fixed-width sequences, and fenced code blocks for aligned multiline sequence
  text; do not introduce special biological-sequence syntax.
- Support ASCII source that projects to Unicode after strict-Djot validation. The literal ASCII
  token `&prime;` maps to Unicode code point U+2032 PRIME; never rewrite verbatim or raw content.
- Use the upstream `.djot` suffix for extended-Djot presentation source. The extension's slide
  semantics come from its grammar, not a separate `.djp`, `.djs`, or `.djots` filename convention.
- Do not add a successor-language presenter-note syntax. Djot footnotes are audience-facing
  citations or clarifications, not hidden speaker notes; the existing importer still preserves
  notes from historical decks.
- A declared layout, rather than image count, should ultimately own slot capacity and geometry. Do
  not silently change a slide's selected layout because of image count.
- Keep teaching reveals within a small predefined action set rather than a general animation
  language. The provisional `<=` and `=>` spellings do not settle floating-answer geometry.
- Explore `<= blue overlay` as a bounded action for an authored annotation or popup highlight. It
  may become a predefined treatment, never a general coordinate attribute bag. With exactly one
  Djot component image in a slot, it anchors there; otherwise the linter reports an error.
- For an inline blue highlight, write the target as the unquoted remainder of `<= blue overlay`.
  It must occur exactly once in the preceding logical item; the linter rejects missing or ambiguous
  targets. This preserves hard-wrapping and avoids escaping DNA prime marks inside quoted strings.
- Write a simple, fast, source-only linter with pyflakes-level enforcement. It must report
  source-located structural mistakes without rendering or opening LibreOffice; geometry, overflow,
  native animation export, and visual quality remain separate validation lanes.
- Treat Djot's explicit, unambiguous grammar as the compatibility basis for the extension. Do not
  require raw HTML tags or `<!-- ... -->` comments for normal slide structure.
- Keep one canonical authored source. Do not characterize the language discussion as a proposal for
  a separate GFM review copy and a presentation copy.
- Eventually separate reusable slide-language work from this repository's personal lecture content.
  Until an explicit migration plan exists, keep the current language exploration and course content
  together here; do not create a second content authority or prematurely split implementation.

## Working style

- Use a 350-character limit for the plain-prose GitHub About paragraph at the top of README.md.
- This repository is an application/toolchain, not a PyPI package as currently written. Do not add a
  root `pyproject.toml` merely for release-version cross-checking; resolve date-block release versions
  from root `VERSION` unless a future packaging decision changes that need.
- Keep `PYTHONDONTWRITEBYTECODE=1` active and do not run explicit bytecode-compilation commands that
  create `__pycache__`; the absence of an ignore rule makes accidental cache writes visible.
- Have single-repository propagation add a `devel/changelog_lib.py`-compatible changelog entry only
  when it makes real changes; recurring `.gitignore` churn must not create one.
- Classify one-time implementation checks separately from permanent tests. Apply the permanent
  pytest checklist, keep temporary proof out of the suite, and remove a test when in doubt.
- Before letting a test block progress, ask whether it protects a current requirement, known
  failure mode, or stable boundary.
- Remove a test or keep it as temporary verification when it mainly proves a hypothetical edge,
  exact implementation detail, or one-time migration or recovery behavior.
- Follow the repository test rules before adding fixtures or special hooks. Treat a test design as
  suspect when it requires awkward production machinery users did not ask for.
- Preserve behavior tests for credential routing, stale-result fencing, fallback semantics, exact
  child binding, and updater deletion safety. Keep rollout, archive restoration, and artifact
  comparison checks outside the permanent suite unless repository rules justify them.
- Prompt positively: state the desired action directly and keep safety or correctness boundaries
  explicit.
- Use parallel, atomic delegation when it reduces wall time; subagents and tokens are cheap.
- Fix the design that allowed incorrect behavior. Use a narrow fallback or special case only when it
  is part of the intended design.
- Prefer durable long-term fixes, accepting a small immediate cost to avoid larger maintenance costs.
- Make adaptability a primary design goal so changing requirements and new evidence do not require
  repeated architectural rewrites.
- Make the software robust: imperfect inputs, data, state, or behavior should preserve useful
  operation through context-appropriate graceful recovery whenever possible.
- Prefer the smallest coherent design that satisfies actual requirements and known failure modes.
  Mechanisms, abstractions, policies, state, and tests earn their place by solving demonstrated
  needs.
- Prefer clear boundaries, stable domain concepts, and replaceable components over speculative
  edge-case machinery. Address concrete requirements and likely failure modes now.
- Build on the repository's ambition, then turn the strongest version into practical, owned,
  verifiable work.
- Treat this pre-production codebase as a place to keep only durable tests with meaningful behavior.
- Keep test-only file inputs inline and create them under `tmp_path`; do not retain committed fixture
  trees that conflict with the repository pytest policy.
- Reserve leading-underscore filenames for temporary-only work. Permanent modules need descriptive
  snake_case names without a leading underscore.
- Finish LibreOffice layout synchronization through the user-visible build path and remove migration
  scaffolding or drift instead of preserving unfinished compatibility code.
