# Source pipeline decisions

Part of [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md).

### Historical (2026-09-08): geometry-first import accepted ODP and PPTX

**Status.** Superseded by the current direct bounded-ODP import boundary. This entry preserves the
geometry-first normalization rationale.

**Decision.** Normalize trusted ODP/PPTX content into `SlidePlan` before emitting extended-Djot. The
plan carries source geometry, title evidence, independent editable components, true table metadata,
and positive visual-relation evidence used only to choose a native standard layout.

**Why.** Existing teaching slides mix ordinary semantic content with diagrams whose labels depend on
their original arrangement. Geometry-first planning can identify those relationships without making
the old rendering authoritative. A difficult slide is useful redesign evidence.

**Consequence.** The importer chooses titles from bounded upper-lane geometry and assigns native
components atomically. Ambiguous or overlapping legacy geometry normalizes into one standard
source-order panel with a review reason. A table-bearing fallback isolates each table in its own
native cell. Difficult slides retain their instructional text and genuine images through an
existing registered layout; when dense labels cannot remain useful on-slide, the import report
retains their lossless text/link/geometry facts beside a visible redesign diagnostic. Ordinary
source pictures remain independent image assets; unsupported vectors stay explicit in diagnostics.
No rendered source slide or composite region is an import product.

**Owner.** `slide_lib/importers/slide_plan.py`, `slide_lib/importers/djot_emitter.py`,
`slide_lib/importers/pptx_to_djot.py`, and [PIPELINE.md](PIPELINE.md).

### Source table metadata controls native tables

**Decision.** Emit an editable native table only from actual source table metadata. Preserve its
source-derived header status and intentional blanks; send merged or spanned cells to review before
publication.

**Why.** A visual grid does not establish table semantics. Retaining genuine source structure keeps
native tables editable without misclassifying diagram labels as rows and columns.

**Consequence.** Inferred lattices remain diagrams or review cases. A merged or spanned source table
fails source-located rather than receiving an invented table projection. Native table rendering
therefore has a bounded, extensible input contract for future span support.

**Owner.** `slide_lib/importers/slide_plan.py`,
`slide_lib/importers/djot_emitter.py`, and `slide_lib/layout_engine.py`.

### Ordinary layouts preflight optional titles and local headings

**Decision.** Ordinary panel layouts accept zero or one global H1, and each ordinary cell accepts
at most one local H2. Preflight title, heading, table, image, and text capacity before creating
native shapes.

**Why.** Imported slides sometimes have an absent global title or a component-local heading. The
same source allocation must remain readable whether the title is present or absent.

**Consequence.** A titleless layout receives its full content region. Local headings and ordinary
body/list text retain the shared point-valued readability contract: ordinary text starts at 28 pt,
and a representable fit below 24 pt records a source-located capacity diagnostic. Content below the
shared serializer-safe minimum reports one source-located physical-capacity error before publication.

**Owner.** `slide_lib/layout_engine.py` and [PIPELINE.md](PIPELINE.md).

### Physical plans own safe line advance and list geometry

**Decision.** Ordinary theme text has nominal 1.30em line spacing, matching the OTP outline
`fo:line-height="130%"`. The compiler resolves list start and hanging indents into
`ParagraphProperties`, and records an exact safe advance for each wrapped line as the greater of
that nominal spacing and the mixed-face ascent-plus-descent required by the resolved runs.

**Why.** Measuring with one spacing rule while serializing another can make an apparently fitting
deck wrap, shrink, or overflow in either adapter. Adapter-local list or leading choices would also
recreate the original format-dependent layout behavior.

**Consequence.** WP-T1 exposes the nominal OTP policy; WP-T2 supplies only verified font metrics;
WP-L2 carries resolved indents and safe advances in immutable physical plan records; WP-O1 and WP-P1
serialize those values identically without remeasurement. Offline plan/package/projection tests and
WP-V2 LibreOffice round-trip/render parity tests reject a changed leading, indent, or list hierarchy.
This is a target contract, not an implementation-completion claim.

**Owner.** WP-T1, WP-T2, WP-L2, WP-O1, WP-P1, and WP-V2 in the native ODP layout migration.

### Historical (2026-09-08): one source slide used two native adapters

**Status.** Superseded by the current ODP-only serializer. This entry preserves the one-to-one
compilation and capacity-diagnostic rationale.

**Decision.** `layout_engine` emits exactly one `LayoutSlide` for every authored source slide. A
structured capacity diagnostic records a representable sub-floor recovery; content that cannot fit
at the shared serializer-safe minimum raises one source-located physical-capacity error.

**Why.** A fixed one-to-one source-to-artifact relationship preserves author intent and lets a
normal build show a usable deck's compromises directly rather than hiding them in continuation or
decomposition machinery.

**Consequence.** Notes, revealed objects, and authored content stay together on their single
source-derived slide with deterministic `slide-N` identities. Both native adapters serialize the
same immutable plan without generating continuation pages or page chrome.

**Owner.** `slide_lib/layout_engine.py`, `slide_lib/layout_model.py`,
`slide_lib/odp_export.py`, and `slide_lib/pptx_export.py`.

### Historical (2026-09-08): capacity fed ODP and PPTX adapters

**Status.** Superseded by the current ODP-only projection. This entry preserves the shared
measurement and readable-floor rationale.

**Decision.** The layout compiler, rather than either output adapter, owns one-to-one capacity and
title-floor resolution. It measures hash-verified theme faces at exact requested sizes, including
fractional point values, and keeps cache/session identity in the measurement inputs. Explicit line
breaks are grapheme-safe. A title that reaches its shared 22 pt floor remains one atomic title; it is
not rewritten into leaf fragments to make a page fit.

**Why.** The original drift arose when each artifact path could treat text boxes and fit behavior as
format-local details. A fractional-size or grapheme boundary must not turn the same source into a
different plan on a later run. Fragmenting a title to satisfy one local constraint would weaken the
source's semantic structure and recreate adapter-specific fallback behavior.

**Consequence.** The compiler uses 36 pt / 28 pt defaults with corpus-derived 22 pt / 20 pt
title/body floors. It
selects a full-fit recovery at or above the shared 1 pt serializer-safe minimum and records a
structured source-location/layout/slot diagnostic when a selected size is below a readable floor.
Content below the serializer-safe minimum raises one source-located physical-capacity error. The
custom multiple-choice layout first tries its full visible question region at the ordinary body
floor, then separates context, stem, and choices into editable regions using that same floor.
ODP and PPTX project the completed `LayoutDeck` from the same `CompilationResult`; normal build
summaries report those diagnostics without a second compilation.

**Owner.** `slide_lib/layout_engine.py`, `layout_measurement.py`,
`multiple_choice_layout.py`, and `layout_builders.py`; WP-O1, WP-P1, and WP-V2 consume and verify
the plan.

### Corpus-derived typography recovery floors

**Decision.** Keep the 36 pt title and 28 pt body teaching defaults.  Use a 22 pt title floor and
20 pt body floor only when compiler preflight must recover a representable source slide.

**Why.** The measured original corpus contains normal, readable explanatory material at 20 pt and
a readable exceptional title at 22 pt.  Its smaller tail is chiefly figure labels, URLs, staged
diagram material, or visibly broken legacy compositions.  The floor therefore admits established
teaching density without making that tail the normal classroom standard.

**Consequence.** The constants in `presentation_theme.py` carry the corpus rule.  Systematic
sub-floor diagnostics remain compiler work for WP-A6; a later floor change re-measures the corpus
and records why it improves normal teaching use.  The first 20 pt / 22 pt corpus scan recorded 105
diagnostics: 82 paragraph/list, 10 title, 8 local-heading, 4 mixed-flow, and 1 table.  These are
explicit residual layout work, not evidence to lower the ordinary teaching floor.

### Specialty slide paths preserve hierarchy and native output

**Decision.** Title slides use the native master rectangles and select the largest readable title
that preserves the 20 pt body floor; otherwise the body records its capacity diagnostic. Covers add
a rounded metadata frame with no fill, behind the editable text, and an accent rule.
Sections use the deck's course accent and center white text
in a rounded frame. The explicit `theend` layout renders its required `# THE END` heading as two
giant lines with a native star in the D.
`big-image` places one focal image above a short full-width bottom caption, and ordinary content
reserves a visible bottom margin.

**Why.** The hand-written cover frame made metadata tiny, body-driven title shrinking hid the real
constraint, and the master section outline appeared 42 logical pixels below the page midpoint.
Recurring cover, transition, closer, and image-focus roles need a clear identity without rasterized
lettering.

**Consequence.** Course covers use `Lecture ##<letter>` and separate subject, chapter, instructor,
and teaching-date paragraphs, following [PEDAGOGICAL_SLIDE_STYLE_GUIDE.md](PEDAGOGICAL_SLIDE_STYLE_GUIDE.md).
The unfilled metadata frame precedes both text boxes in the exported stacking order so the
decoration does not obstruct text selection. `LayoutSlide.surface` controls the native page style and master visibility.
Deck-level `color-theme` metadata selects the band and readable accent for native decorations,
links, tables, and transitions; every letter stays an editable font glyph. Existing layouts stay unchanged.

**Owner.** `slide_lib/layout_model.py`, `slide_lib/layout_builders.py`,
`slide_lib/layout_specialty_builders.py`, `slide_lib/odp_export.py`, and
[DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md).

### Imported evidence keeps relations adaptable

**Decision.** Preserve direct source evidence for shape style, placeholder role, actual top/group
z-paths, and signed rotation beside normalized geometry. Route through the shared registry-topology
matcher before special relations; do not duplicate layout geometry in individual import relations.

**Why.** Style and ordering distinguish explanatory callouts and labels from ordinary prose, while a
single topology authority lets the importer gain layouts without changing each relation classifier.

**Consequence.** The importer may retain a visible degenerate connector through a bounded normalized
footprint and may recognize only positive, bounded relation classes. A narrow coarse-body and
picture-inset pair stays as direct editable objects in `two-panels`, with exact provenance and one
explicit permission. Caption pairing is one shared positive relation, grouped before topology and
reusing the existing `two-plus-one` and footer permission. Adaptive vertical image flow starts text
at 28 pt and records a fit below its 20 pt floor before scaling every image uniformly. Visual
relations retain source membership only long enough to normalize it into standard native components;
no private render or geometry exception is a routing mechanism. Ambiguous arrangements become a
native source-order panel with review evidence.
Geometry, heading relations, topology, and Djot emission symbols are imported from their owning
modules. Slide planning and conversion consume those owners directly and do not re-export
compatibility facades.

**Owner.** `slide_lib/importers/geometry.py`, `slide_lib/importers/topology.py`,
`slide_lib/importers/visual_relations.py`, and `slide_lib/importers/slide_plan.py`.

### Historical (2026-09-08): imported assets used the PPTX importer owner

**Status.** Superseded by the direct ODP importer. This entry preserves the reachability and
self-contained-publication rationale.

**Decision.** Publish only generated assets reachable from the parsed Djot deck and keep them below
that deck's local `assets/` directory.

**Why.** Reachability makes a regenerated deck self-contained and prevents stale extracted files from
becoming unreviewed source dependencies.

**Consequence.** Missing, unsafe, or symlinked asset references stop publication. The staged importer
prunes unreachable files before its atomic publication step. Published assets are genuine imported
content rather than rendered reconstructions of source layout.

**Owner.** `slide_lib/importers/pptx_to_djot.py`.

### Historical (2026-09-08): Djot followed ODP or PPTX import

**Status.** Superseded by the current ODP-only import boundary. This entry preserves the
single-canonical-source rationale.

**Decision.** Import an existing ODP or PPTX once, then make the generated Djot and local assets the sole
editable source.

**Why.** One canonical state prevents Djot, PPTX, and ODP from silently diverging.

**Consequence.** Generated artifacts are reproducible. Imported ODP and temporary normalization PPTX
remain migration evidence, not future editing surfaces.

**Owner.** `deck_tools.py`, `slide_lib/importers/odp_to_djot.py`,
`slide_lib/importers/pptx_to_djot.py`, and [USAGE.md](USAGE.md).

### Historical (2026-09-08): structured import read ODP and PPTX

**Status.** Superseded by the current direct ODP reader. This entry preserves the structured-data
preference over OCR.

**Decision.** Extract imported ODP/PPTX text, lists, notes, and component images as document objects.

**Why.** The source decks are authored structured documents; OCR is lower fidelity and discards
available semantics.

**Consequence.** Whole-slide source images are conversion failures. OCR is reserved only for text
that genuinely exists within a component image.

**Owner.** `slide_lib/importers/odp_reader.py` and `slide_lib/importers/pptx_reader.py`.

### Local reference projects remain outside runtime

**Decision.** Keep every `OTHER_REPOS/` clone outside the production runtime and dependency graph.

**Why.** Prior art can inform bounded implementation choices without importing incompatible syntax,
workflows, licenses, or renderer assumptions.

**Consequence.** The repository adapts verified ideas into local Python. The inventory records the
specific evidence and limitations for each clone.

**Owner.** `docs/OTHER_REPOS/` and `docs/USAGE.md`.

### Biotechnology Lecture 05 adapts canonical Lecture 04 source

**Decision.** Keep three current Djot decks under `biotech/LECT05/djot/`: announcements,
individual project, and Theranos. Reuse the Lecture 04 Djot content for stable announcements
and project guidance; use legacy Lecture 05 visibility as teaching evidence. Original ODP/PDF
and copied Set #3 files remain reference inputs in the lecture root.

**Why.** Lecture 05 changes the teaching selection and calendar without requiring a second
conversion of already editable content. Completed early-semester assignments belong in the
hidden archive, while current project steps need the published Fall 2026 dates.

**Consequence.** Native hidden slides remain in Djot and ODP; classroom PDFs omit them.
The announcement source includes `biotech` in its filename to avoid overwriting the Genetics
Lecture 05 output. Imported Theranos evidence remains in its original import report, and the
lecture review records subsequent authoring and visibility changes.

**Owner.** `biotech/LECT05/djot/`, [USAGE.md](USAGE.md), and
[DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md).

### Explicit table groups share compiler-measured column needs

**Decision.** Authors name related tables with `table-group`. A compile-scoped prepass pools
widest-token and full-line column needs at the theme's ordinary body size across all group
members. Each member uses those same bounds to allocate its available width before fitting text.

**Why.** A later answer must inform an earlier question's column layout. Explicit membership
records teaching intent without guessing from coincidental table shapes or hand-tuning ratios.

**Consequence.** Equal-width members have identical columns even when their selected text sizes
differ. Groups include hidden slides, are local to one deck, and require matching column counts.
Different available widths remain responsive; row heights remain content-dependent. Manual
`column-widths` is an alternative and cannot be combined with a group. Ordinary tables are unchanged.

**Owner.** `slide_lib/layout_engine.py`, `slide_lib/layout_measurement.py`,
`slide_lib/native_model.py`, and `slide_lib/djot_blocks.py`.

### Authored table proportions preserve repeated column boundaries

**Decision.** Tables optionally carry positive finite `column-widths` weights, one per column.
Parse these into typed column weights and resolve them in shared table measurement as proportions
of full table width. Keep automatic content-based widths as the default.

**Why.** Question/answer sequences need stable columns even when cell text changes; invisible
padding text would mix layout instructions with student content.

**Consequence.** Repeated tables can share `column-widths="1,3,3"` while remaining editable.
Row heights and text fitting remain content-dependent. Invalid source fails before export.

**Owner.** `slide_lib/djot_blocks.py`, `slide_lib/native_model.py`, and
`slide_lib/layout_measurement.py`.

### Reference slides reuse the one-panel body geometry

**Decision.** Register `reference` as an explicit author-selected layout with the ordinary
title/body placeholders, a backend-owned reference footer, and an unfilled light gray border.
Keep the border behind editable text and the footer below the standard body allocation.

**Why.** Students can distinguish later-study material without repeated source labels or reduced
space for explanations. Ordinary one-panel slides retain their existing appearance and geometry.

**Consequence.** Djot authors select `=== layout: reference` and supply a title and `@body`.
The importer does not infer this teaching intent from geometry alone.

**Owner.** `slide_lib/layout_registry.py`, `slide_lib/layout_measurement.py`,
`slide_lib/layout_builders.py`, and `slide_lib/layout_specialty_builders.py`.

### Native ODP is the sole editable build artifact

**Decision.** Build Djot directly to editable ODP and derive PDF only from that ODP through
LibreOffice. Import accepts bounded ODP; a legacy PPTX is saved as ODP in LibreOffice before import.

**Why.** One native editable artifact and one PDF provenance path keep classroom builds inspectable
and remove a duplicate OOXML renderer, reader, animation writer, temporary conversion path, and
their dependency.

**Consequence.** `all` produces ODP and LibreOffice-derived PDF; `odp` produces ODP; `pdf` writes
ODP then derives PDF. The format-neutral compiler, ODF/SMIL reveals, and the custom
`multiple-choice` layout remain unchanged.

**Owner.** `slide_lib/odp_export.py`, `slide_lib/importers/odp_reader.py`,
`slide_lib/native_export.py`, and `slide_lib/libreoffice.py`.
