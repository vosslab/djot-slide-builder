# Plan: Add reusable Djot deck includes

## Context

Announcement decks repeat a substantial set of classroom-stable slides across courses and
weeks: recording reminders, Zoom guidance, YouTube and Discord information, office hours, contact
instructions, and other informational material. The current compiler parses one `.djot` file as
one deck. Authors therefore copy those slides into each lecture deck and must update several copies
when a shared slide changes.

The desired workflow is to keep changing lecture-specific slides in the lecture file while
importing a maintained sequence of shared slides from another Djot file. The existing workflow
must remain valid, including:

- `./build_slides.sh genetics/LECT04/` selecting only Lecture 04;
- one authored source slide becoming one physical output slide;
- hidden slides remaining in source and lint scope;
- local images retaining their aspect ratio and remaining native editable objects; and
- source-located diagnostics and the current native Djot validation lane.

The current parser has no composition layer. `parse_deck()` reads one file, `split_slides()` owns
layout-boundary detection, and the native `Deck` has one deck-level asset root. Included slides
need their own source locations so their relative images can continue to resolve beside the file
that authored them.

## Objectives

- Add a small, deterministic way for one Djot deck to include the slides from another Djot file.
- Preserve the included file's slide order, hidden metadata, source locations, notes, and local
  image references.
- Allow includes to be placed between ordinary parent slides, so a common informational block can
  remain in the same classroom position without copying it into every course deck.
- Keep `deck_tools.py` and `./build_slides.sh` commands unchanged for authors.
- Make lint, capacity inspection, native ODP export, and LibreOffice-derived PDF output operate on
  the flattened composed deck as one compilation.
- Provide a first real announcement migration using the polished Biotechnology informational
  slide treatment as the reusable source pattern.

## Design philosophy

Use literal inclusion, not inheritance. An include contributes complete authored slides in source
order; it does not provide a class, override mechanism, selector language, variable substitution,
or parent/child metadata merge. This keeps a shared announcement file readable as an ordinary
Djot slide source and preserves the existing one-source-slide/one-output-slide contract.

Composition happens before semantic slide parsing. Once expansion is complete, the existing layout
registry, slot validation, native layout compiler, and ODP exporter continue to see ordinary
`Slide` objects. Source provenance is not flattened: each block and slide retains the physical path
and line from the file that authored it.

Relative component images resolve beside the source file recorded on the image's
`SourceLocation`. This is the smallest change that makes a shared fragment genuinely reusable;
rewriting every image path into the parent's namespace would obscure ownership and make source
review harder.

## Scope

- Add one exact include directive to the extended-Djot grammar.
- Recursively expand included Djot sources with deterministic order and source-local diagnostics.
- Resolve include paths relative to the including file and constrain them to the repository.
- Detect missing files, non-Djot targets, include cycles, and included deck-level color metadata.
- Preserve included-file paths for image linting, measurement, physical picture planning, and ODP
  package payload collection.
- Teach recursive source discovery not to build a file merely because it is reachable as an
  included fragment when that file is selected through a course-folder build.
- Add focused parser, linter, asset-resolution, discovery, and native-package tests.
- Add a shared announcement fragment and migrate a representative Genetics announcement deck and
  the Biotechnology announcement deck only after the implementation contract passes.
- Document authoring syntax, source ownership, build behavior, and migration evidence.

## Non-goals

- General slide inheritance, overrides, mixins, variables, macros, or conditional content.
- Merging or replacing individual blocks inside an imported slide.
- Per-include color themes, deck titles, output names, or export settings.
- Importing ODP/PDF at build time or making generated ODP/PDF alternate authored sources.
- Copying included assets into the parent deck or generating source files during a build.
- Changing the folder selector's meaning for ordinary lecture sources.
- Solving announcement content revision policy; the included file remains the canonical owner of
  the slides it contains.

## Current state summary

| Area | Current authority | Change required |
| --- | --- | --- |
| Source parsing | `slide_lib/djot_parser.py` reads one file and splits exact `=== layout:` directives. | Add an include expansion phase that emits the same internal slide-source records in order. |
| Grammar | `slide_lib/djot_grammar.py` owns exact whole-line directives. | Add an exact `=== include: <relative-path>` form and reserve it outside fenced code. |
| Semantic model | `SourceLocation.path` already records the physical source for every parsed block and slide. | Reuse that provenance; do not add a second authored-file field unless implementation evidence requires it. |
| Asset lint | `slide_lib/djot_lint.py` currently resolves images from `Deck.asset_root`. | Resolve each image beside `image.location.path`, with the same repository and traversal checks. |
| Image measurement | `slide_lib/layout_measurement.py` currently resolves images from `Deck.asset_root`. | Use the same source-local resolver as lint and export. |
| Physical picture plan | `slide_lib/layout_object_builders.py` stores the authored image path in `PictureContent`. | Store the resolved source path for included images so the ODP exporter can package the right file. |
| ODP packaging | `slide_lib/odp_export.py` resolves relative picture paths from the root deck. | Accept the resolved picture paths produced by the builder; retain package deduplication by digest. |
| Build discovery | `native_export.discover_decks()` recursively selects `.djot` files. | Exclude reachable include targets from folder-level top-level deck selection, while retaining explicit-file behavior. |
| Documentation | `docs/DJOT_SLIDE_SYNTAX.md`, `docs/USAGE.md`, `docs/PIPELINE.md`, and decision records define the current source contract. | Add the include contract only after focused implementation tests pass. |

## Proposed authoring contract

Use an exact whole-line directive at the same source level as a layout directive:

```djot
color-theme: genetics

=== layout: title-slide

# Lecture 04A

=== include: ../../../shared/djot/announcements/informational.djot

=== layout: one-panel

# Today's Agenda
```

The included file contains ordinary layout blocks and may itself contain include directives:

```djot
=== layout: section

# Informational Slides

=== layout: two-panels

# How to Use Zoom Like a Pro

@left

- Mute yourself when you are not speaking.

@right

![Zoom guidance](assets/zoom.png)
```

Contract rules for the first implementation:

- Include targets use the `.djot` suffix and are resolved relative to the including file.
- The target must resolve to a regular file inside the repository.
- A composed root deck owns the single `color-theme`; an included file must not declare
  `color-theme`.
- Include directives are structural only when they occur outside fenced code. A directive inside a
  code fence remains code text.
- Included files may contain hidden slides, and those slides remain in their authored positions in
  the composed source model.
- Include expansion is textual at the slide-boundary level: included slides appear exactly where
  the directive occurs, with no implicit title, section, or metadata insertion.
- Cycles fail with the include chain in the diagnostic. Repeated non-cyclic inclusion is literal
  and therefore produces repeated slides intentionally.

## Architecture boundaries and ownership

### Mapping

| Workstream | Components | Review boundary |
| --- | --- | --- |
| WS-P source composition | `slide_lib/djot_grammar.py`, `slide_lib/djot_parser.py`, `slide_lib/djot_errors.py` | Include syntax, recursive expansion, source locations, cycle/path diagnostics, and color-theme ownership. |
| WS-A asset provenance | `slide_lib/djot_lint.py`, `slide_lib/layout_measurement.py`, `slide_lib/layout_object_builders.py`, `slide_lib/odp_export.py` | One source-local image resolver is used by lint, measurement, physical planning, and package export. |
| WS-D discovery | `slide_lib/native_export.py`, `slide_lib/djot_lint.py` | Folder selection distinguishes top-level decks from reachable included fragments without changing explicit-file builds. |
| WS-T tests | `tests/test_djot_parser.py`, `tests/test_djot_slide_lint.py`, `tests/test_layout_engine.py`, `tests/test_odp_export.py`, `tests/test_native_export.py` | Permanent behavior tests cover order, hidden slides, failures, source-local assets, and native package payloads. |
| WS-C corpus integration | `shared/`, `genetics/LECT04/djot/lect04a-2026_announcements.djot`, `biotech/djot/lect03a-2026_announcements.djot` | One representative shared informational fragment proves the requested announcement workflow. |
| WS-DOC documentation | `docs/DJOT_SLIDE_SYNTAX.md`, `docs/USAGE.md`, `docs/PIPELINE.md`, `docs/DESIGN_DECISIONS.md`, `docs/HUMAN_GUIDANCE.md`, `docs/CHANGELOG.md` | Syntax, ownership, rationale, user guidance, and evidence agree with the implementation. |

## Milestone plan

| Milestone | Title | Goal | Exit gate |
| --- | --- | --- | --- |
| M1 | Freeze the include contract | Confirm directive spelling, placement, path policy, metadata policy, and source-local asset semantics. | The contract above is reflected in focused parser specimens and has no unresolved ambiguity that changes implementation scope. |
| M2 | Implement source composition | Expand nested includes into ordered slide sources while preserving physical locations and rejecting unsafe graphs. | Parser tests pass for order, nesting, cycles, missing targets, path escapes, fenced-code text, and child color metadata. |
| M3 | Carry asset provenance through native compilation | Make linter, measurement, physical planning, and ODP packaging resolve included images beside their authored file. | A parent deck including a fragment with a fragment-local image lints, compiles, and packages the image without copying it. |
| M4 | Integrate source discovery and CLI behavior | Keep folder builds focused on top-level decks and keep explicit-file parsing predictable. | `./build_slides.sh genetics/LECT04/` builds the expected lecture decks and does not build shared fragments. |
| M5 | Migrate announcements and close documentation | Lift the shared Biotechnology informational slides into a reusable source and use it from representative class decks. | Native lint, targeted tests, native ODP/PDF build, page-count/source-order checks, and visual spot checks all pass. |

## Workstream breakdown

### Workstream: WS-P source composition

- Goal: make included slides indistinguishable from ordinary authored slides after expansion.
- Dependencies: M1.
- Deliverables: exact grammar pattern, recursive source graph resolver, cycle stack, include-chain
  diagnostics, and retained `SourceLocation` values.
- Permanent tests: include order around parent slides; nested include order; repeated include;
  cycle; missing file; non-Djot target; repository escape; child `color-theme`; fenced-code line;
  and one malformed child slide reporting the child's path and line.
- Review boundary: no layout or ODP edits until the flattened semantic deck is correct.

### Workstream: WS-A asset provenance

- Goal: make relative images owned by the file that authored their slide.
- Dependencies: M2.
- Deliverables: one shared helper or equivalent single authority for safe image resolution, used by
  lint, measurement, physical picture construction, and native package export.
- Permanent tests: parent-local image; included-local image; missing included image; traversal
  rejection; symlink/repository containment behavior; and a package test proving the included image
  is present in `Pictures/`.
- Review boundary: no path rewriting in source text and no generated asset copy.

### Workstream: WS-D discovery

- Goal: preserve the distinction between a build target and a dependency source.
- Dependencies: M2.
- Deliverables: reachable-include discovery or an equivalent exclusion rule for folder builds,
  with explicit-file parsing still available for diagnostics and authoring.
- Permanent tests: a folder with one root deck and one included fragment selects one build target;
  nested fragments remain excluded; an unrelated `.djot` remains a target; and an explicit fragment
  path reports its normal source behavior.
- Review boundary: the existing `genetics/LECT04/` selection contract remains unchanged.

### Workstream: WS-C corpus integration

- Goal: prove that recurring announcement slides can be maintained once.
- Dependencies: M2, M3, and M4.
- Deliverables: a shared informational announcement fragment with its owned assets, a Genetics
  Lecture 04 announcement include, and a Biotechnology announcement include or equivalent
  representative consumer.
- Migration rule: preserve the current course-specific title, agenda, dates, policy, and weekly
  reminders in each parent; move only slides that are truly constant across the selected consumers.
- Review boundary: compare source order and visible-page count before and after migration. Do not
  silently move lecture-specific reminders into the shared file.

## Work packages

### WP-P1: grammar and recursive expansion

1. Add the exact include directive pattern to `djot_grammar.py`.
2. Refactor parser source loading so root and child files share UTF-8, fence, and source-location
   handling.
3. Expand child layout records at each include boundary without changing ordinary no-include parse
   behavior.
4. Track the active include stack and report the complete chain for cycles.
5. Enforce repository containment and `.djot` suffix before reading a target.
6. Reject child `color-theme` metadata with a child-local diagnostic.

### WP-A1: source-local image resolution

1. Establish one resolver from `Image.location.path.parent` plus the authored relative source.
2. Retain existing rejection of absolute and `..` image source spellings.
3. Use the resolver in source lint and intrinsic image measurement.
4. Give `PictureContent` the resolved path needed by ODP packaging while keeping semantic source
   text unchanged.
5. Keep repository containment and regular-file checks identical across lint and build paths.

### WP-D1: dependency-aware discovery

1. Identify reachable include targets without compiling the deck.
2. Exclude reachable targets from folder-level top-level deck lists.
3. Preserve sorted relative-path ordering for independent root decks.
4. Keep explicit-file behavior source-located and deterministic.

### WP-C1: announcement pilot

1. Extract the polished recording, Zoom, YouTube, Discord, office-hours, contact, and related
   informational slide sequence that is genuinely constant for the pilot consumers.
2. Move or establish its assets under the shared fragment's adjacent asset namespace.
3. Replace the duplicated pilot blocks with an include at the intended sequence point.
4. Keep changing lecture title, date, agenda, current deadlines, course links, and class-specific
   material in the parent deck.
5. Rebuild both pilot consumers and compare visible slide order, page count, and representative
   rendered pages.

## Acceptance criteria and gates

### Semantic gate

- A no-include deck parses identically to the current implementation.
- An include contributes exactly its authored slides, in place, with no slide splitting or merging.
- `hidden: true` survives expansion and remains linted while omitted from physical output.
- Every included block and slide reports the physical included-file path and line.
- Include cycles, missing targets, non-Djot targets, repository escapes, and child color metadata
  fail before layout compilation with actionable diagnostics.

### Native gate

- A parent deck with an included fragment-local image passes strict native validation for every
  reachable source and passes repository semantic lint.
- The generated ODP contains the included image as a native editable picture object and the PDF is
  derived from that ODP through the existing LibreOffice path.
- Source slide count, hidden-slide count, visible-page count, and output order are deterministic.
- No full-slide raster or generated source copy is introduced.

### Workflow gate

- `./build_slides.sh genetics/LECT04/` still builds only Lecture 04 top-level decks.
- Authors can update a shared announcement fragment once and rebuild each consuming deck without
  editing copied slide blocks.
- Existing direct `deck_tools.py build`, `lint`, `capacity`, and `visibility` workflows remain
  usable.

### Visual gate

- Render representative included announcement pages from ODP-derived PDF and inspect them beside
  the current polished Biotechnology reference.
- Check that included images retain their original aspect ratios, titles remain centered where
  authored, shared informational slides keep their intended order, and no parent-specific slide is
  accidentally absorbed into the fragment.
- Record the build command, native lint result, output page counts, and visual sample paths in the
  final review note.

## Test and verification strategy

Focused permanent tests should be added before corpus migration:

- `tests/test_djot_parser.py`: grammar, order, nesting, metadata, source locations, and failures.
- `tests/test_djot_slide_lint.py`: included-file image ownership and safety checks.
- `tests/test_layout_engine.py`: one visible and one hidden included slide compile with stable
  source identities and output order.
- `tests/test_odp_export.py`: included image payload is packaged once from its source-local path.
- `tests/test_native_export.py`: dependency-aware discovery and explicit-file behavior.

One-time acceptance evidence should then use the real workflow:

```bash
source source_me.sh && python3 -m pytest tests/test_djot_parser.py tests/test_djot_slide_lint.py \
  tests/test_layout_engine.py tests/test_odp_export.py tests/test_native_export.py
source source_me.sh && python3 deck_tools.py lint --require-native \
  --native-executable "$(command -v jotdown)" genetics/LECT04/
./build_slides.sh genetics/LECT04/
```

The build command requires the repository's existing LibreOffice desktop preflight and may need
the approved execution environment for process inspection. Record capacity warnings separately;
they are not include failures.

## Risk register

| Risk | Effect | Mitigation | Trigger to revisit |
| --- | --- | --- | --- |
| A child deck declares a conflicting theme | Parent output becomes ambiguous. | Make theme ownership root-only and reject child metadata. | A real course requires mixed-theme slides; then add an explicit per-slide theme contract rather than implicit inheritance. |
| Folder discovery builds shared fragments independently | Duplicate or incomplete output decks appear. | Track reachable include dependencies during folder discovery. | A user intentionally wants a fragment as a standalone deck; document an explicit standalone wrapper instead of weakening dependency exclusion. |
| Included image paths resolve from the wrong directory | Lint passes but native build packages the wrong or missing image. | Use one source-local resolver in lint, measurement, and physical picture planning. | Any discrepancy between source lint and package payload tests. |
| Include cycles are hard to diagnose | Authoring becomes confusing and can recurse indefinitely. | Maintain an active canonical-path stack and print the chain. | A valid use case needs recursive repetition; use explicit repeated non-cyclic includes instead. |
| Shared fragment absorbs course-specific content | A class deck loses its weekly teaching sequence. | Pilot only clearly constant informational slides and compare source order/page counts. | Visual or semantic review finds a changed date, link, deadline, or course identity in the fragment. |
| Strict native validation sees the include directive differently from the local parser | Source acceptance becomes inconsistent. | Run native validation on every reachable source and record the exact directive specimen before migration. | The pinned native parser rejects the directive; choose a compatible exact surface before implementation. |

## Rollout and release checklist

- [ ] Add and pass parser/composition tests.
- [ ] Add and pass source-local asset tests.
- [ ] Add and pass dependency-aware discovery tests.
- [ ] Document the include syntax in `docs/DJOT_SLIDE_SYNTAX.md` and the build model in
  `docs/USAGE.md` and `docs/PIPELINE.md`.
- [ ] Record the settled root-theme and literal-inclusion decisions in `docs/DESIGN_DECISIONS.md`.
- [ ] Keep the instructor's reusable-announcement guidance in `docs/HUMAN_GUIDANCE.md`.
- [ ] Add the shared informational fragment and migrate only the pilot announcement consumers.
- [ ] Run strict native lint, focused tests, and the lecture-folder native build.
- [ ] Render and inspect representative shared slides and one parent-specific slide.
- [ ] Update `docs/CHANGELOG.md` with implementation, migration, and validation evidence.

## Open questions and decisions needed

The proposed contract intentionally leaves only two choices before implementation:

1. Confirm the exact shared-fragment location. The recommended location is a repository-level
   `shared/djot/announcements/` directory so it is outside `genetics/LECT##/` and `biotech/`
   lecture discovery roots.
2. Confirm the pilot migration order. The recommended first pilot is the shared Biotechnology
   informational block consumed by Genetics Lecture 04A and Biotechnology Lecture 03A, followed by
   other recurring announcement blocks only after page-order review.

No production parser or corpus source changes are part of this planning artifact. Once the contract
is approved, implementation should proceed through M1--M4 before changing announcement sources.
