# Plan: Native ODP layout architecture

Status: completed and archived 2026-09-08. Earlier current-state descriptions and provisional
leading-underscore module names below are historical planning context, not live repository paths.

Final acceptance scope: the durable evidence-tier decision in
[DESIGN_DECISIONS.md](../DESIGN_DECISIONS.md#native-acceptance-uses-evidence-tiers) supersedes
WP-V2's proposed retained proof bundle, fixed 144-DPI ink thresholds, and dedicated acceptance
report. The detailed WP-V2 text remains below as historical planning context.

Primary acceptance deck: `genetics/djot/lect02a-2025_announcements.djot`, especially slide 3.

## Context

The generated ODP is editable, themed, and PDF-capable, but it is not structurally equivalent to a
LibreOffice-authored presentation. The current exporter renders every slide on a blank PPTX layout,
adds generic OOXML text boxes, converts that PPTX to ODP, and then replaces the ODP master and styles.
LibreOffice consequently stores generated text as `draw:custom-shape` objects such as
`draw:type="ooxml-rect"`, not as layout-owned `draw:frame` objects with
`presentation:class="title"` or `presentation:class="outline"`.

The failure is visible on slide 3 of `lect02a-2025_announcements`: applying LibreOffice's One Box
layout creates new empty title and body placeholders on top of the generated content. The existing
objects cannot become layout members merely by changing the master name after conversion. The title
also begins at 36 pt but appears at 30.6 pt because the generated title frame is only about 1.175 cm
high, while the authoritative OTP title placeholder is about 2.921 cm high. Ordinary generated body
text begins at 19.5 pt because 26 logical font units are converted by a 0.75 multiplier, rather than
at the requested 28 pt.

The durable fix is a renderer redesign. Compile Djot into one format-neutral physical layout plan,
then serialize that plan independently to native ODP and optional PPTX. ODP becomes a first-class
artifact whose page layouts, presentation frames, styles, notes, images, tables, hyperlinks, and
animations are written as ODF 1.3 semantics. LibreOffice remains the PDF exporter and a headless
round-trip verification target; it stops being the PPTX-to-ODP construction engine.

## Objectives

- Make every generated ODP slide reference a native ODF presentation page layout that matches its
  declared Djot layout.
- Make title, subtitle, outline, and content slots genuine LibreOffice presentation frames rather
  than imported OOXML custom shapes.
- Compile layout geometry and content flow once into a format-neutral plan consumed by both output
  adapters.
- Make standard titles start at 36 pt and ordinary body/list text start at 28 pt.
- Permit shrink-on-overflow only as bounded renderer protection, with preflight rejecting content
  that cannot remain at or above the readable floor.
- Preserve the complete current editable-object contract, including lists, links, component images,
  tables, notes, and bounded reveals.
- Make PPTX an independent optional interchange artifact instead of an ODP prerequisite.
- Keep PDF dependent on the generated ODP so classroom PDF and editable classroom source agree.
- Supply fast structural tests and an autonomous LibreOffice E2E that progresses through the fixed
  ODP XML contract, captured minimal fixtures, deterministic package-XML layout transitions,
  headless open/save preservation, reveal-state interpretation, and PDF/render metrics.

## Design philosophy

Apply **Fix the design, not the symptom**, **Long-term over short-term**, and **Design for
adaptability** from [REPO_STYLE.md](../REPO_STYLE.md). The one-sentence algorithm is:

> Compile one semantic deck into one validated format-neutral layout plan, then serialize that plan
> independently through native ODP and PPTX adapters.

A frame-height patch, post-conversion XML rename, slide-specific `lect02a` exception, or retained
PPTX bridge would preserve the failed ownership boundary. The plan accepts the larger one-time cost
of a native ODF adapter so new layouts, themes, text policies, and output formats can evolve without
duplicating placement logic.

- Evidence strategy for uncertain methods: first lock the desired ODP XML contract, then commit a
  minimal, versioned ODF reference artifact for each presentation role, compare its package
  semantics with ODF 1.3, implement the smallest conforming writer, and require headless
  LibreOffice open/save preservation before expanding the adapter. Deterministic package-XML
  transition and reveal-state interpreters prove behavior without a fragile automation bridge.

## Scope

- Replace the transitional `slide_lib/layouts.py` authority with the layered physical-plan modules:
  immutable primitives in `slide_lib/layout_primitives.py`, content records in
  `slide_lib/layout_content.py`, the complete plan in `slide_lib/layout_model.py`, the small
  compiler API in `slide_lib/layout_engine.py`, and PPTX projection in
  `slide_lib/pptx_export.py`. Private layout helpers are cohesive implementation modules, never a
  facade or compatibility re-export. WP-L2 leaves the legacy PPTX projection temporarily while it
  extracts format-neutral authority; WP-P1 moves that projection; WP-I1 alone removes `layouts.py`
  after both adapters use the shared plan.
- Add an immutable physical layout model using 1280x800 logical geometry and point-valued typography.
- Extend the OTP theme model to own native frame geometry, page-layout roles, font sizes, list
  geometry, and bounded autofit policy.
- Set the authoritative OTP title default to 36 pt and every ordinary outline/body level to 28 pt.
- Add a direct ODF 1.3 package writer seeded by `genetics/xlect99-template_2023.otp`.
- Emit native ODF page-layout definitions and layout-owned presentation frames for all 18 registered
  Djot layouts.
- Emit native ODF text, lists, tables, images, links, notes, page metadata, and reveal animations.
- Refactor the PPTX path to consume the shared layout plan and retain its editable-object and
  animation behavior.
- Change build orchestration so ODP/PDF paths do not construct or read PPTX.
- Remove superseded conversion/theme-splice code instead of retaining compatibility facades.
- Update permanent tests, live E2E coverage, operator documentation, design decisions, guidance
  records, and changelog records.

## Non-goals

- Preserve slide-specific geometry from the imported lecture decks.
- Make PPTX the theme or layout authority.
- Add a user-facing typography override syntax to Djot in this migration.
- Add general animation choreography beyond the existing appear/fade, object/paragraphs, on-click
  contract.
- Add browser, CSS, Node, or raster slide-rendering dependencies.
- Guarantee a minimum font size after edits made outside the repository; the repository guarantees
  the floor at build time and records that native LibreOffice shrink can exceed that policy after
  later external edits.
- Treat every component picture, diagram label, or decorative shape as a layout placeholder.
- Retain the old PPTX-to-ODP path as a fallback after the native ODP gate passes.

## Current state summary

- `slide_lib/native_export.py` creates every PPTX slide from `presentation.slide_layouts[6]`, the
  blank layout.
- The checked-out transition has `slide_lib/layout_model.py`, but `slide_lib/layouts.py` still
  combines legacy geometry, fit estimation, validation, and python-pptx creation. It is not an
  authority in the target design and must be removed by WP-I1 after all callers use the three
  direct-import modules.
- `slide_lib/layouts.py::add_textbox()` adds OOXML `a:normAutofit`, so the current output does request
  shrink-on-overflow even though LibreOffice exposes different context-menu properties for different
  imported object types.
- `slide_lib/native_export.py::render_template_odp()` converts a background-free PPTX to ODP and then
  calls `slide_lib/odp_theme.py::apply_template_master()`.
- `slide_lib/odp_theme.py` retargets `draw:master-page-name` and replaces `styles.xml`; it does not
  create presentation page layouts or convert custom shapes into presentation frames.
- The authoritative OTP provides a real `Default` master with title and outline placeholders. Its
  current stored title size is 36 pt; its root outline size is approximately 35.5 pt rather than the
  requested 28 pt.
- The OTP currently stores only the page-layout definitions exercised when it was saved. The direct
  writer therefore must emit stable per-layout definitions from the repository layout registry.
- A controlled placeholder-aware PPTX conversion proves that LibreOffice can preserve title and
  outline presentation classes. This rules out the PPTX file format itself as the root cause and
  identifies blank-layout generic text boxes as the current design failure.
- The current ODP outputs inspected during diagnosis contain no native `anim:` timing tree. Reveal
  fidelity is therefore a required migration gate, not an assumed side effect of conversion.

## Architecture boundaries and ownership

The target pipeline is:

```text
Djot source
    |
    v
semantic Deck (content and intent)
    |
    v
layout compiler (geometry, roles, fit, reading order)
    |
    v
immutable LayoutDeck
    |-------------------------------|
    v                               v
native ODP adapter             optional PPTX adapter
    |                               |
    v                               v
editable ODP                   editable PPTX
    |
    v
LibreOffice PDF export
```

Durable component ownership:

- `slide_lib/native_model.py` owns semantic source content and reveal intent only.
- `slide_lib/layout_primitives.py` owns immutable geometry, identifiers, and layout-contract terms.
  `slide_lib/layout_content.py` owns immutable editable content records. `slide_lib/layout_model.py`
  owns their composition into the immutable physical plan: ordered objects, semantic
  placeholder/member kinds, canonical presentation-page-layout keys, point-valued typography, style
  roles, and stable reveal targets.
- `slide_lib/layout_engine.py` is the sole public compiler/registry API for all 18 layouts. It
  exposes only `compile_layout_deck`, `registered_layout_names`, and `layout_contract`, delegates
  to private helpers, and compiles `native_model.Deck` to `layout_model.LayoutDeck`; every adapter
  consumes only `LayoutDeck`.
- `slide_lib/layout_registry.py` owns the declarative 18-`LayoutContract` catalog only.
  `slide_lib/layout_measurement.py` owns pure measurement, preflight, pagination, and local-heading
  calculation. `slide_lib/layout_builders.py` owns construction of planned objects from the already
  resolved registry and measurement results; it never recomputes allocation or fit decisions.
- Continuation is a compiler-owned physical expansion, not an adapter feature. A logical source slide
  starts as exactly one panel. Only a failed true-fit preflight may partition it into continuation
  pages when `paginate: true`; `paginate: false` raises one source-located diagnostic before any
  artifact is serialized. The partitioner preserves paragraph, root-list subtree, table-row-group,
  and atomic-object boundaries; uses the latest fitting mixed partition; repeats the global H1 and
  retains an active local H2 with no stranded heading. It uses the explicit context-handoff policy
  below for detached descendants, preserves the same layout topology and title behavior, assigns
  stable `source_id-pN` physical IDs and contiguous continuation indexes, resets reveals per physical
  page without cross-page targets, repeats qualified notes, and numbers physical pages.
- `slide_lib/presentation_theme.py` owns validated, format-neutral theme tokens read from the OTP.
- New `slide_lib/odp_export.py` owns ODF document structure, page-layout definitions, presentation
  frames, automatic styles, notes pages, deterministic adapter-owned media identities, and package
  publication. It retains template masters, styles, and resources while replacing `content.xml`.
- New `slide_lib/odp_text.py` owns ODF paragraphs, spans, links, lists, tables, and text-style
  projection.
- New `slide_lib/odp_animation.py` owns ODF/SMIL timing trees for the bounded reveal contract.
- New `slide_lib/pptx_export.py` owns python-pptx and OOXML projection from the shared plan.
- `slide_lib/pptx_animation.py` remains the OOXML timing-tree owner used only by the PPTX adapter.
- `slide_lib/odf_package.py` owns bounded ZIP validation, manifest consistency, and atomic ODF
  publication.
- `slide_lib/native_export.py` owns parsing, one layout compilation, artifact selection, and the
  ODP-to-PDF dependency graph.
- `PresentationTheme.template_path` is the sole template authority. It resolves to
  `genetics/xlect99-template_2023.otp`; adapters receive the already validated theme and must not
  discover, substitute, or re-open another template path.

The public compiler and adapter boundaries are exact:

```python
compile_layout_deck(deck: Deck, theme: PresentationTheme) -> LayoutDeck
write_odp(deck: LayoutDeck, theme: PresentationTheme, destination: Path) -> Path
write_pptx(deck: LayoutDeck, theme: PresentationTheme, destination: Path) -> Path
```

The model ownership DAG is `layout_primitives -> layout_content -> layout_model`: primitives are the
lowest-level neutral terms, content is composed from those terms, and the complete physical model is
composed from both. In import direction, `layout_content -> layout_primitives` and
`layout_model -> layout_content, layout_primitives`; `layout_primitives` uses only the standard
library. `native_model` remains the independent source-semantic authority and is imported only by
the compiler-side modules that translate source facts: `_layout_measurement`, `_layout_builders`, and
`layout_engine`. `_layout_registry -> layout_primitives` (declarative data only, no callbacks or
project imports); `_layout_measurement -> native_model, layout_model, layout_content,
layout_primitives, presentation_theme`; `_layout_builders -> native_model, layout_model,
layout_content, layout_primitives, presentation_theme, _layout_registry, _layout_measurement`; and
`layout_engine -> native_model, layout_model, layout_content, presentation_theme, _layout_registry,
_layout_builders`. Private helpers never import `layout_engine`, an adapter, or a format library.
Compiler consumers import only `layout_engine`'s public API; they do not import private helpers or
the registry. Adapters may import the immutable `layout_model` and `layout_content` records they
serialize, but never compiler-private modules. `odp_export`, `odp_text`, `odp_animation`, and
`odf_package` may import `layout_model`, `layout_content`, and `presentation_theme`, but never
`native_model`, `layout_engine`, `pptx_export`, or python-pptx. `pptx_export` and `pptx_animation`
may import `layout_model`, `layout_content`, and
`presentation_theme`, but never ODF modules. `native_export` is the sole composition root allowed
to import the compiler and either adapter. The layered physical-plan modules, compiler API, and
adapters are direct imports; no `layouts.py` facade, compatibility alias, or re-export is permitted.

The template master background is theme-level content outside the planned slide-object stream.
Author-authored decorations are planned objects with normal reading and z-order semantics; an adapter
must never infer them from the template background.

### Mapping (milestones / workstreams -> components / patches)

| Milestone / Workstream | Component | Review boundary |
| --- | --- | --- |
| M1 / WS-E | Evidence and contract | Reference report and acceptance comparator |
| M2 / WS-L | Shared layout compiler | No output-format imports below this boundary |
| M2 / WS-T | Theme contract | OTP and format-neutral theme values |
| M2 / WS-T2 | Font-metric contract | Verified, immutable typeface profiles and measurement evidence |
| M3 / WS-O | Native ODP core | ODF structure without LibreOffice conversion |
| M3 / WS-P | PPTX projection | Optional OOXML artifact from shared plan |
| M4 / WS-A | ODP reveals | ODF/SMIL timing only |
| M5 / WS-I | Build integration | Artifact dependency graph and removal of old path |
| M6 / WS-V | Verification | Fast structural and live LibreOffice evidence |
| M6 / WS-D | Documentation | Durable docs and plan completion |

## User-facing contract

Typography and fitting use explicit point units:

| Role | Start size | Build floor | Overflow policy |
| --- | --- | --- | --- |
| Standard title | 36 pt | 30 pt | Shrink only after preflight |
| Ordinary body and list | 28 pt | 24 pt | Shrink only after preflight |
| Local content heading | 28 pt | 24 pt | Shrink only after preflight |
| Displayed literal URL | Same role size | Same role floor | Use PT Sans Narrow |

The 30 pt title and 24 pt body floors are required initial policy, not hidden renderer constants.
They live in the theme model and can change with one contract edit after visual evidence. Geometry
continues to use logical 1280x800 units; font sizes never pass through the logical-pixel-to-point
conversion.

Text capacity is measured from committed, hash-verified OFL font assets, never from a host font
lookup or a substitution chosen by LibreOffice, Pillow, or the operating system. The theme exposes
immutable face profiles keyed by family, weight, and italic state. The initial profiles cover the
available OpenDyslexic faces used by ordinary text and the actually shipped PT Sans Narrow faces
used for displayed literal URLs. A request for a missing face, a changed asset hash, or an
unapproved styled run is a pre-publication error. In particular, PT Sans Narrow must not pretend to
have an italic face by silently substituting an upright or another-family font.

The measurement owner uses Pillow `getlength()` over resolved styled runs and token-aware line
breaking, real OTP list text-start and hanging-indent geometry, and ascent/descent line boxes that
remain valid when a line mixes faces. It never applies a `0.25em` average-glyph heuristic or a
generic 10-percent list-width cap. Measurement-cache keys include the verified face identity,
styled runs, point size, line spacing, text width, list geometry, and policy revision, so a font or
theme change cannot reuse stale capacity results.

For each generated ODP slide:

- `draw:page` references one `presentation:presentation-page-layout-name` generated from its declared
  layout and canonical placeholder topology. ODP XML names are document-local opaque identifiers;
  the contract compares the resolved topology, not a literal generated name.
- An authored H1 occupies one `draw:frame` with `presentation:class="title"` when the selected layout
  has a title.
- Authored subtitles occupy `presentation:class="subtitle"` frames.
- The primary one-panel body occupies one `presentation:class="outline"` frame.
- Text-capable layout slots use outline/content presentation frames; image-only primary slots use
  object presentation frames. Additional component images and intentional annotations remain native
  draw objects inside the owning slot geometry.
- Presentation frames use the `layout` layer, inherit the matching `Default-*` presentation style,
  and carry fixed-frame shrink-on-overflow behavior.
- Applying the same LibreOffice layout reuses the existing title/body members. It does not add empty
  Click to add Title or Click to add Text placeholders over authored content.
- Applying a compatible different layout retains each compatible presentation member exactly once;
  ordinary component objects remain editable and are not promoted into placeholders by accident.

For transition evidence, One Box is the semantic topology `title + outline-primary`. The compatible
alternate topology is `title + outline-primary + outline-secondary`; the captured local name
`AL4T3` is evidence from one document only, never a writer output identity. Switching One Box to the
alternate retains title and primary body exactly once, creates one empty secondary member only when
the source has no secondary content, and never creates an empty duplicate title or primary body.
Switching back removes an empty secondary member; a populated secondary member must be retained as
ordinary content or rejected source-locally before transition, never silently discarded.

LibreOffice does not expose a minimum value for native shrink-to-fit. The compiler therefore chooses
an explicit size between the start size and floor, rejects content that would require a smaller
size, and enables native shrink only to absorb font-metric differences. A build-time postflight
reports any frame estimated below its floor. Later edits outside the build remain normal
LibreOffice behavior.

## Milestone plan

The migration uses the following dependency order.

| M | Title | Summary | Goal |
| --- | --- | --- | --- |
| M1 | Lock the ODP contract | Capture native role and API evidence | Remove format uncertainty |
| M2 | Compile one layout plan | Separate geometry and theme from formats | Create the stable core |
| M3 | Build independent adapters | Write direct ODP and refactor PPTX | Remove duplicated ownership |
| M4 | Preserve ODP reveals | Add native ODF/SMIL timing | Close the known fidelity gap |
| M5 | Switch the pipeline | Make adapters siblings and remove bridge | Activate the new architecture |
| M6 | Prove and close | Run structural, rendered, and autonomous gates | Ship a verified migration |

### Milestone: M1 lock the ODP contract

- Depends on: none; diagnosis already isolates the current design failure.
- Deliverables: desired ODP XML contract, native-reference artifacts, role-topology map, exact
  package invariants, and a deterministic package-XML layout-transition interpreter.
- Workstreams: WS-E.
- Entry criteria: authoritative OTP and `lect02a` source/output are available.
- Exit criteria: every presentation role and reveal maps to observed ODF 1.3 structure; no core ODP
  implementation choice remains based only on a context-menu label.
- Parallel-plan ready: no; one evidence owner must keep the package, API, and standard observations
  in one coherent contract.

### Milestone: M2 compile one layout plan

- Depends on: WP-E1 because presentation roles and fit properties shape the physical model.
- Deliverables: `layout_model.py`, `layout_engine.py`, point-valued theme policy, updated OTP defaults,
  and a PPTX-independent layout registry.
- Workstreams: WS-L and WS-T.
- Entry criteria: M1 exits.
- Exit criteria: all 18 layouts compile without importing python-pptx or ODF code; the OTP validates
  36 pt titles and 28 pt ordinary body levels.
- Parallel-plan ready: yes; WS-L and WS-T have separate files and meet at the documented theme-model
  interface. Maximum parallel doers: 2.

### Milestone: M3 build independent adapters

- Depends on: WP-L2 and WP-T1 because both adapters consume the stable plan and theme contract.
- Deliverables: direct ODP package/text adapter and refactored PPTX adapter.
- Workstreams: WS-O and WS-P.
- Entry criteria: M2 exits and immutable plan examples exist for one-panel, two-panels, gallery,
  multiple-choice, table, image, and notes cases.
- Exit criteria: direct ODP covers every non-animation object; PPTX preserves current editable
  behavior from the same plan; neither adapter calls the other.
- Parallel-plan ready: yes; the adapters write disjoint modules and share only the frozen plan.
  Maximum parallel doers: 2.

### Milestone: M4 preserve ODP reveals

- Depends on: WP-O2 for stable ODF object IDs and WP-E2 for the observed animation reference.
- Deliverables: native ODF/SMIL appear/fade and object/paragraph timing plus automated state-harness
  evidence.
- Workstreams: WS-A.
- Entry criteria: direct ODP static content opens cleanly in LibreOffice.
- Exit criteria: package inspection and the automated reveal state harness both match source reveal
  order for ordinary and multiple-choice decks.
- Parallel-plan ready: no; ODF timing and target-ID ownership are one tightly coupled change.

### Milestone: M5 switch the pipeline

- Depends on: WP-O3, WP-P1, and WP-A1 because all current output contracts must exist before the old
  path is removed.
- Deliverables: sibling output orchestration, updated CLI semantics, removed bridge/theme splice,
  and migrated unit tests.
- Workstreams: WS-I.
- Entry criteria: direct ODP and PPTX independently pass focused tests.
- Exit criteria: ODP/PDF builds make no PPTX; PDF still comes from ODP; no compatibility facade or
  dead bridge code remains.
- Parallel-plan ready: no; one integrator owns dependency-graph changes and deletions.

### Milestone: M6 prove and close

- Depends on: WP-I1 because verification targets the final pipeline.
- Deliverables: fast test results, native-layout E2E, `lect02a` evidence, machine-readable
  acceptance report, documentation updates, independent review, and archived completed plan.
- Workstreams: WS-V and WS-D.
- Entry criteria: M5 exits.
- Exit criteria: every gate in this plan passes and the active plan is archived with final evidence.
- Parallel-plan ready: yes; verification and documentation can proceed concurrently after
  integration, with documentation consuming the final verification report before plan completion. Maximum
  parallel doers: 2.

## Workstream breakdown

### Workstream: WS-E contract evidence

- Goal: define native LibreOffice behavior from the desired ODP XML contract, captured ODF, and
  headless preservation evidence.
- Owner: tester.
- Work packages: WP-E1 and WP-E2.
- Needs: OTP plus committed minimal one-panel, two-content, and reveal reference artifacts.
- Provides: presentation-role, fit, page-layout, and animation invariants.
- Review boundary, when modifying the repository: reports only; no production workaround is allowed.

### Workstream: WS-L shared layout compiler

- Goal: create a format-neutral physical plan and move all placement decisions into it.
- Owner: architect for WP-L1; expert coder for WP-L2.
- Work packages: WP-L1 and WP-L2.
- Needs: WP-E1 role contract and existing semantic `Deck`.
- Provides: frozen `LayoutDeck` consumed by both adapters.
- Review boundary, when modifying the repository: this layer imports neither python-pptx nor ODF
  serializer modules.

### Workstream: WS-T theme contract

- Goal: make the OTP own reusable geometry and 36/28 point typography.
- Owner: coder.
- Work packages: WP-T1.
- Needs: WP-E1 fit and placeholder evidence.
- Provides: validated `PresentationTheme` tokens and updated OTP.
- Review boundary, when modifying the repository: one binary theme artifact plus its transparent
  XML contract tests.

### Workstream: WS-O native ODP core

- Goal: serialize `LayoutDeck` directly as a conforming, editable ODF presentation.
- Owner: expert coder; independently accepted by a fresh reviewer on 2026-09-08.
- Work packages: WP-O1, WP-O2, and WP-O3.
- Needs: WP-L2 and WP-T1.
- Provides: native ODP without PPTX or LibreOffice conversion.
- Review boundary, when modifying the repository: ODF package/structure, text, and media projection.

### Workstream: WS-P PPTX projection

- Goal: retain optional editable PPTX from the same layout plan.
- Owner: coder.
- Work packages: WP-P1.
- Needs: WP-L2 and WP-T1.
- Provides: independent PPTX artifact and OOXML reveal targets.
- Review boundary, when modifying the repository: python-pptx and OOXML only.

### Workstream: WS-A ODP reveals

- Goal: project the bounded reveal model into native ODF/SMIL.
- Owner: expert coder.
- Work packages: WP-A1.
- Needs: WP-E2 and WP-O2.
- Provides: native Impress reveal-state behavior without an OOXML bridge.
- Review boundary, when modifying the repository: ODF animation nodes and target IDs only.

### Workstream: WS-I integration

- Goal: activate sibling adapters and delete the superseded path.
- Owner: integrator.
- Work packages: WP-I1.
- Needs: WP-O3, WP-P1, and WP-A1.
- Provides: final artifact graph and clean source ownership.
- Review boundary, when modifying the repository: public build behavior and module removal.

### Workstream: WS-V verification

- Goal: prove structural, rendered, and application behavior.
- Owner: tester.
- Work packages: WP-V1 and WP-V2.
- Needs: WP-I1.
- Provides: fast regression evidence and live acceptance report.
- Review boundary, when modifying the repository: durable behavior tests and E2E only.

### Workstream: WS-D documentation

- Goal: make the new architecture discoverable and close superseded claims.
- Owner: maintainer; independent reviewer owns WP-D2.
- Work packages: WP-D1 and WP-D2.
- Needs: WP-I1 and final WP-V2 results for plan completion.
- Provides: current architecture docs, changelog, review, and archived plan.
- Review boundary, when modifying the repository: documentation and read-only audit.

## Work packages

### Work package: WP-E1 capture native layout semantics

- Owner: tester.
- Touch points: new `docs/active_plans/reports/native_odp_layout_contract.md`; committed minimal
  reference artifacts under `tests/fixtures/odp_native_layouts/`; generated probes under `output/`.
- Depends on: none.
- Acceptance criteria: report exact page-layout, frame-class, style-parent, layer, autofit, and
  headless open/save behavior for native title, subtitle, outline, and object frames in LibreOffice
  26.2.6.3; fixtures contain only the minimum role topology needed by the comparator.
- Evidence or review, when useful: the deterministic package-XML transition interpreter applies
  One Box and a compatible alternate layout to synthetic slide 3 content, then records object
  counts, retained roles, text ownership, and package snippets.
- Obvious follow-ons: give the locked invariants to WP-L1, WP-T1, and WP-O1.

### Work package: WP-E2 capture native reveal semantics

- Owner: tester.
- Touch points: the same contract report; committed minimal reveal reference artifact under
  `tests/fixtures/odp_native_layouts/` and generated probe decks under `output/`.
- Depends on: none.
- Acceptance criteria: report target IDs and ODF/SMIL node structure for object appear, object fade,
  and top-level outline cascade under on-click activation.
- Evidence or review, when useful: headlessly open/save the reference, inspect its timing tree, and
  run the synthetic state harness before accepting the XML as a stable comparator.
- Obvious follow-ons: provide the target and ordering contract to WP-A1.

### Work package: WP-L1 define the physical layout model

- Owner: architect.
- Touch points: new `slide_lib/layout_model.py`; `slide_lib/native_model.py` only if a missing
  format-neutral semantic identity is proven.
- Depends on: WP-E1 because native roles must be modeled explicitly.
- Acceptance criteria: immutable records cover deck metadata, the exact 18-layout topology catalog,
  `SlideIdentity` (source slide identity, physical-page identity, parent identity, and continuation
  index), logical rectangles, reading/z order, presentation role, semantic `PlaceholderKind` and
  member kind, resolved `RunStyle`, list levels, table cells, `PicturePlacement` (allocated rect,
  display rect, crop, and alt text), `ObjectAccessibility` and links, notes, theme role, explicit
  point-size bounds and per-frame overflow policy, `presentation_member_id`, and reveal target
  identity. The neutral `LayoutContract` record lives in `layout_primitives.py`, not in the registry
  or engine. `PresentationPageLayoutKey` is canonical and contains layout identity, canvas, and
  ordered placeholder IDs, kinds, roles, and geometry while excluding authored text, media, notes,
  and decorations. Its identifiers remain stable across adapters and continuation pages.
- Acceptance criteria: the model carries an ordered `ContinuationContext` of immutable ancestor
  entries and a display mode of `INLINE_STATIC`, `HANDOFF_STATIC`, or `METADATA_ONLY`; it also marks
  each physical slide as `ContinuationKind.NORMAL`, `AUTHORED`, or `CONTEXT_HANDOFF`. Existing
  `continuation_context` marks static visible repeats. Context entries are never authored units or
  reveal targets. A detached descendant retains full neutral context metadata regardless of visible
  mode, so adapters can preserve the relationship without recovering source text from rendered
  objects.
- Acceptance criteria: the model represents source code, display math, quote, and unsupported
  attributes without pretending they have an editable adapter projection. Before either adapter,
  the compiler either produces the explicitly approved projection or emits one source-located
  rejection; adapters never silently drop or invent a fallback for those constructs.
- Evidence or review, when useful: architect rejects any field named for PPTX, ODF XML, or a
  LibreOffice object implementation rather than a presentation concept. Unit tests prove that equal
  topology yields one key, geometry changes yield a distinct key, and authored-content changes do
  not alter the key.
- Obvious follow-ons: freeze the public model before WP-L2, WP-O1, and WP-P1 begin.

### Work package: WP-L2 extract the layout compiler

- Owner: expert coder.
- Touch points: `slide_lib/layout_engine.py`, `slide_lib/layout_primitives.py`,
  `slide_lib/layout_content.py`, and new private `layout_registry.py`, `layout_measurement.py`, and
  `layout_builders.py`; extract and migrate all format-neutral authority to the layered plan and
  migrate its callers to direct imports. Retain the legacy PPTX projection in `slide_lib/layouts.py`
  temporarily; WP-P1 moves that projection to `pptx_export.py`; WP-I1 alone removes `layouts.py`
  after both adapters use the shared plan. Update layout consumers and focused tests.
- Depends on: WP-L1, WP-T1, and WP-T2 because compilation consumes the physical model, theme policy,
  and verified font-metric profiles.
- Acceptance criteria: `layout_engine.py` is at most 350 physical lines and exposes only
  `compile_layout_deck(Deck, PresentationTheme) -> LayoutDeck`, `registered_layout_names`, and
  `layout_contract`. It is the sole compiler for the complete 18-layout topology catalog and
  produces physical `LayoutSlide` values,
  including deterministic pagination expansion, `SlideIdentity.parent_id`/continuation values, and a
  page-number object only where the theme/layout policy requires it. Adapters receive `LayoutDeck`
  only and do not select layouts, allocate slot geometry, crop pictures, resolve links/accessibility,
  paginate, or fit text. Preflight selects a size no smaller than the role floor or raises a
  source-located error before serialization; no output-format library is imported.
- Acceptance criteria: pagination is a true fit gate, never a cosmetic page split. A one-panel
  source remains one physical page when it fits. Otherwise the compiler applies this ordered
  fallback: reduce role size only to its 24 pt ordinary-text floor; partition at ordinary atomic
  boundaries (paragraphs, whole root-list subtrees, table-row groups, and atomic objects); then,
  only when one root-list subtree alone cannot fit, recursively partition between its descendant
  list-item subtrees. A leaf list item that cannot fit fails at its source location. The compiler
  first places an ordered minimum ancestor trail and new authored descendant together as
  `INLINE_STATIC` when both fit. If that combined page cannot fit, it emits one deterministic
  `CONTEXT_HANDOFF` physical page with `HANDOFF_STATIC` context immediately before the detached
  descendant; that page contains static context only. If the trail itself cannot fit, it records
  `METADATA_ONLY` context on the descendant. The descendant must fit at its original list level or
  fail source-locally. No abbreviated, clipped, subfloor, or text-specific continuation branch is
  permitted. Every authored unit occurs exactly once; context is static and non-revealable.
  Continuations have stable `source_id-pN` identity and continuation index, local reveals only,
  physical page numbers, and qualified continuation notes. Ordinary repeated H1 behavior is separate
  from the ancestor trail and remains unchanged. `paginate: false` and an unsplittable atomic unit
  fail at the relevant source location before publication.
- Acceptance criteria: the compiler owns `DECOMPOSE_TO_ONE_PANEL` for a failed true-fit generic
  grid only. Its eligible contracts are `two-panels`, `one-plus-two-panels`,
  `two-plus-one-panels`, `stacked-panels`, `two-over-one-panels`, `four-panels`, and `six-panels`.
  A fitting grid retains its authored topology. With `paginate: true`, every nonempty source slot is
  gathered in canonical reading order and passed through the ordinary one-panel splitter; every
  physical result uses one-panel topology, repeats H1/active context/qualified notes but never slot
  labels, applies canonical one-panel image/table placement, carries source-grid and source-slot
  origin provenance, gives every content unit and reveal exactly one physical occurrence, and uses
  deterministic continuation identities. Title, centered-text, vertical, gallery, and
  multiple-choice semantic layouts are excluded. `paginate: false`, an excluded layout, and an
  unsplittable atomic unit fail at the originating source location before serialization.
- Acceptance criteria: `layout_registry.py` is at most 450 physical lines, contains the declarative
  18 `LayoutContract` catalog, and has no callback or project-module import.
  `layout_measurement.py` is at most 650 physical lines and owns only pure
  measurement/preflight/pagination/local-heading work. `layout_builders.py` is at most 700 physical
  lines and builds planned objects without recomputing a registry, allocation, or fit result.
  `layout_primitives.py`, `layout_content.py`, and `layout_model.py` are each at most 500 physical
  lines; `pptx_export.py` is at most 700 physical lines; and no relevant module may reach 1,000
  physical lines. The repository physical-line test is the sole measurement method. Splitting by a
  cohesive subdomain is required instead of restoring a facade if a target is exceeded. Compile-time
  topology and import-graph tests prove every layout's slot/member catalog, exact
  `PicturePlacement` allocation/display/crop invariants, stable `presentation_member_id`, resolved
  run styles, link/accessibility preservation, continuation ordering, and early code/math/quote/
  attribute rejection or approved projection.
- Evidence or review, when useful: fast tests compare semantic properties such as containment,
  non-overlap, reading order, role assignment, and floor enforcement rather than tunable coordinates.
- Acceptance criteria: compiler capacity acceptance is blocked until WP-T2 has supplied a verified
  face profile for every styled run it measures. `ParagraphProperties` carries the resolved theme
  list text-start and hanging indents. The OTP outline style and theme policy set nominal ordinary
  line spacing to 130 percent (1.30em); for every wrapped line the compiler records in the physical
  plan an exact safe line advance equal to `max(nominal_1_30em, mixed_face_ascent_plus_descent)`.
  Both adapters serialize that carried value unchanged. Measurement uses resolved run/token widths,
  those list indents, and mixed-face ascent/descent line boxes; no heuristic width fraction or
  system-font fallback may decide a fit.
- Context-handoff addendum owner: WP-L2 expert coder. Success condition: immutable plan objects
  preserve an ordered ancestor trail, a display mode, and physical continuation kind while every
  authored unit occurs exactly once; static handoff pages immediately precede their detached
  descendants and carry no reveal targets. Validation: fast committed-fixture tests prove inline
  context, generic handoff, metadata-only context, and source-local leaf failure; scripted
  `lect02a` line 293, Student Profile line 470, and full-deck compilation run without human input.
- Implementation evidence: accepted with 171 focused tests. The compiler produces all 18 layouts
  without output-format imports and compiles the complete `lect02a` source deterministically to 99
  physical pages; a cold compilation took about 0.69 seconds on the acceptance machine (recorded
  for regression investigation, not a performance threshold). Physical-line counts are
  `layout_engine.py` 290, `layout_registry.py` 77, `layout_measurement.py` 634, and
  `layout_builders.py` 669. The implementation measures committed face profiles at exact point
  sizes, including quarter-point values, and caches by the full font/session and measurement
  identity. It applies the 36 pt / 28 pt defaults and 30 pt / 24 pt floors, resolves grapheme-safe
  explicit line breaks, preserves recursive unsupported facts and table parity, and proves recursive
  `INLINE_STATIC`, `HANDOFF_STATIC`, and `METADATA_ONLY` context behavior. Eligible grids co-pack
  their canonical stream into one-panel continuations with immutable origin provenance. The
  `lect02a` line 243 case resolves through the shared title floor rather than fragmenting an atomic
  leaf. Validation: `source source_me.sh && python3 -m pytest tests/test_layout_engine.py
  tests/test_layout_model.py` (171 passed) plus deterministic full-deck compilation. This completes
  WP-L2 only; WP-O1, WP-P1, and the migration-level adapter and LibreOffice gates remain open.
- Obvious follow-ons: publish immutable plan examples to WP-O1 and WP-P1.

### Work package: WP-T1 complete the OTP theme contract

- Owner: coder.
- Touch points: `genetics/xlect99-template_2023.otp`, `slide_lib/presentation_theme.py`,
  `slide_lib/pptx_theme.py`, and `tests/test_presentation_theme.py` or the current owning theme test.
- Depends on: WP-E1.
- Acceptance criteria: theme loading exposes title/outline frame geometry, presentation-style names,
  title 36 pt, all ordinary outline levels 28 pt, title floor 30 pt, body floor 24 pt, OpenDyslexic,
  list positions, the resolved 1.30em ordinary line-spacing policy (OTP `fo:line-height="130%"`),
  and shrink-only overflow policy; the OTP itself stores the 36/28 defaults so newly inserted
  LibreOffice placeholders match generated content.
- Evidence or review, when useful: inspect the real shipped OTP ZIP XML in fast tests and compare
  the generated fitting specimen's point-valued text properties with the fixed 36.0/28.0 contract
  before adding overflow.
- Obvious follow-ons: provide the frozen theme object to the compiler and both adapters.

### Work package: WP-T2 establish the deterministic font-metric contract

- Owner: expert coder.
- Touch points: committed OFL font assets and provenance record; `slide_lib/presentation_theme.py`;
  the format-neutral measurement owner; focused font-asset, theme, and layout-capacity tests; and
  V2 runtime-drift evidence. This package changes neither the authored font policy nor slide
  geometry: it makes their metrics reproducible.
- Depends on: WP-T1 because it freezes the theme's font families, role sizes, list styles, and
  frame geometry.
- Acceptance criteria: each permitted face is a repository-owned OFL asset with recorded source,
  license/provenance, and SHA-256. Theme profiles are immutable and identify exact family, weight,
  italic state, asset path, and hash. OpenDyslexic supplies the ordinary-text faces the theme uses;
  PT Sans Narrow is available only for the committed face states actually used by displayed literal
  URLs. No code may invent an italic PT Sans Narrow profile or substitute another face for it.
- Acceptance criteria: production capacity measurement resolves every styled run to one approved
  profile and uses Pillow `getlength()` with token-aware wrapping, actual OTP list text-start and
  hanging-indent geometry, and ascent/descent line boxes for mixed-face lines. It resolves the
  nominal 1.30em theme spacing and supplies the safe `max(nominal, mixed-face ascent+descent)`
  line advance that WP-L2 stores in the physical plan. Cache keys contain all face identities/hashes
  and measurement inputs. Missing assets, changed hashes, unresolved style states, and unsupported
  face requests fail before artifact publication with a source- or style-located diagnostic.
- Acceptance criteria: permanent offline tests validate asset hashes/provenance, immutable profile
  selection, absence of host/system substitution, styled-run and token wrapping, real list
  geometry, mixed-face line boxes, cache invalidation, and the rejection paths. V2 records a
  reproducible runtime-drift specimen proving that the current Pillow/LibreOffice environment does
  not silently replace a profile; any detected drift fails the acceptance report.
- Evidence or review, when useful: compare measured profile facts and line breaks against captured
  fixture text rather than a hand-tuned average-glyph estimate. Explicitly reject the historical
  `0.25em` heuristic and generic 10-percent width cap as non-contractual.
- Obvious follow-ons: WP-L2 receives only verified profiles and capacity facts; WP-O1 and WP-P1
  serialize the resolved family/style without performing their own font discovery or substitution.

### Work package: WP-O1 write the ODF package skeleton

- Owner: expert coder.
- Touch points: new `slide_lib/odp_export.py`, `slide_lib/odf_package.py`, and
  `tests/test_odp_export.py`.
- Depends on: WP-L2, WP-T1, and WP-T2.
- Acceptance criteria: copy the authoritative OTP package as the base; retain theme masters,
  `styles.xml`, and reachable template resources; replace `content.xml`; reconcile
  `META-INF/manifest.xml`; publish the ODP mimetype first and uncompressed; and atomically publish
  a valid ODF 1.3 package without invoking LibreOffice. Validation rejects duplicate ZIP member
  names, unsafe member paths, missing manifest entries, manifest entries without a member (except
  required directory entries and the root `/`), missing referenced members, unmanifested reachable
  non-directory members, and unreachable generated media. Template-owned resources may remain
  reachable through retained masters/styles even when no slide object references them.
- Evidence or review, when useful: fast tests inspect only XML/package semantics with inline data and
  `tmp_path`; a serialized headless LibreOffice open/save preservation run is an E2E/review gate,
  not WP-O1 pytest coverage.
- Acceptance criteria: serialize the compiler-carried safe line advance and resolved list start/
  hanging indents identically in native ODP paragraph/list styles; preserve explicit static
  `continuation_context` as context rather than authored/revealable content. Serialize every
  nonvisual continuation trail into the accessibility description and a generated continuation note,
  with exact ODP/PPTX semantic parity. Focused package tests compare these values against the
  immutable `LayoutDeck` rather than remeasuring text.
- Context-handoff addendum owner: WP-O1 expert coder. Success condition: ODP preserves the
  compiler-selected visible/static mode and writes every nonvisual trail as both accessibility
  description and generated continuation note. Validation: package/XML fixtures compare those
  projections directly with `LayoutDeck`; no LibreOffice or attended interaction is required.
- Obvious follow-ons: expose stable page and style builders to WP-O2.

### Work package: WP-O2 emit native layouts and frames

- Owner: expert coder.
- Touch points: `slide_lib/odp_export.py`, `tests/test_odp_export.py`, and
  `tests/e2e/e2e_djot_native_layouts.py`.
- Depends on: WP-O1.
- Acceptance criteria: de-duplicate `style:presentation-page-layout` values by the canonical
  `PresentationPageLayoutKey`, including placeholder geometry; assign the resolved opaque ODP name
  to every `draw:page`; emit title/subtitle/outline/object members as `draw:frame` objects on the
  layout layer with matching `presentation:class`; use local automatic presentation styles parented
  to shipped OTP `Default-*` styles; never emit text-bearing `ooxml-rect` shapes.
- Evidence or review, when useful: all 18 layout specimens pass package topology checks; `lect02a`
  slide 3 contains exactly one title and one outline presentation frame.
- Obvious follow-ons: expose stable object IDs to WP-A1 and content containers to WP-O3.

### Work package: WP-O3 project all static content

- Owner: expert coder.
- Touch points: new `slide_lib/odp_text.py`, `slide_lib/odp_export.py`,
  `slide_lib/odf_package.py`, and focused ODP tests.
- Depends on: WP-O2.
- Acceptance criteria: `write_odp(LayoutDeck, PresentationTheme, Path) -> Path` serializes formatted
  resolved runs, line breaks, links, ordered/unordered nested lists, hanging indents, tables,
  `PicturePlacement` display/crop values, `ObjectAccessibility`, intentional shapes, notes, and
  metadata from the layout plan. Generate deterministic media identities in the ODP adapter from validated media
  bytes and type, not from caller paths or insertion order; every emitted media reference resolves to
  exactly one manifest-backed member and every generated member is reachable.
- Evidence or review, when useful: headless LibreOffice open/save preserves independent editable
  objects and a second package inspection retains presentation classes and text/list hierarchy.
- Obvious follow-ons: hand the feature-complete static adapter to WP-I1 and WP-V2.

### Work package: WP-P1 project the shared plan to PPTX

- Owner: coder.
- Touch points: new `slide_lib/pptx_export.py`, `slide_lib/pptx_theme.py`,
  `slide_lib/pptx_animation.py`, and existing PPTX tests.
- Depends on: WP-L2, WP-T1, and WP-T2.
- Acceptance criteria: `write_pptx(LayoutDeck, PresentationTheme, Path) -> Path` reproduces editable
  PPTX text, resolved runs, lists, tables, picture allocation/display/crop, links, accessibility,
  notes, page numbers, and current bounded OOXML reveals from `LayoutDeck`; use 36/28 point
  typography; contain no layout-allocation, pagination, crop-selection, or fit-selection logic.
- Acceptance criteria: serialize the exact safe line advance and resolved list start/hanging indents
  already carried by `LayoutDeck`; render `continuation_context` as static repeated ancestry and
  never as a duplicate authored or reveal target. Serialize every nonvisual continuation trail into
  the accessibility description and a generated continuation note, with exact ODP/PPTX semantic
  parity. Focused projection tests compare plan and PPTX semantic projections without remeasuring or
  selecting a fallback.
- Context-handoff addendum owner: WP-P1 coder. Success condition: PPTX projects the same trail,
  physical kind, static visibility, accessibility description, and generated continuation note as
  ODP. Validation: deterministic cross-adapter semantic projection tests use compiled fixtures only
  and require exact parity with the plan.
- Evidence or review, when useful: existing semantic PPTX tests pass after changing their entry point;
  a cross-adapter comparator asserts for each compiled physical slide the same `SlideIdentity`,
  ordered `presentation_member_id` values, text/run content, links, accessibility, list/table
  semantics, picture placement/crop intent, notes, page-number policy, and reveal target/order.
  It compares semantic projections, never package bytes or adapter-specific layout names.
- Obvious follow-ons: provide the independent adapter to WP-I1.

### Work package: WP-A1 write native ODP reveals

- Owner: expert coder.
- Touch points: new `slide_lib/odp_animation.py`, `slide_lib/odp_export.py`, focused animation tests,
  and the native-layout E2E.
- Depends on: WP-E2 and WP-O2.
- Acceptance criteria: emit conforming ODF/SMIL on-click object appear/fade and top-level paragraph
  cascade nodes targeting stable draw IDs; preserve source order; reject unsupported reveal shapes
  with source-located diagnostics rather than dropping intent.
- Evidence or review, when useful: fast tests check timing semantics from inline miniature plans;
  the synthetic reveal state harness confirms first-frame visibility, click count, order, and effect.
- Obvious follow-ons: allow WP-I1 to remove the OOXML bridge without losing classroom behavior.

### Work package: WP-I1 activate sibling adapters

- Owner: integrator.
- Touch points: `slide_lib/native_export.py`, `slide_lib/cli.py`, `slide_lib/terminal_output.py`,
  build tests, and removal of `slide_lib/odp_theme.py` plus `slide_lib/layouts.py` only after WP-P1
  has moved the legacy PPTX projection and both adapters consume the shared plan.
- Depends on: WP-O3, WP-P1, and WP-A1.
- Acceptance criteria: parse and compile once; `--format odp` renders only ODP; `--format pdf` renders
  ODP then PDF; `--format pptx` renders only PPTX; `--format all` renders both siblings then PDF from
  ODP; no ODP path imports python-pptx, constructs a temporary PPTX, or converts PPTX to ODP.
- Evidence or review, when useful: mocked artifact-graph tests and one real build per format;
  source search proves no bridge call, compatibility facade, or direct import outside the
  three-module ownership boundary.
- Obvious follow-ons: trigger WP-V1, WP-V2, and WP-D1.

### Work package: WP-V1 add durable fast coverage

- Owner: tester.
- Touch points: `tests/test_layout_engine.py`, `tests/test_odp_export.py`, existing theme/PPTX/build
  tests, and removal or rewriting of tests that pin the old architecture.
- Depends on: WP-I1.
- Acceptance criteria: permanent pytest covers capacity-floor errors, adapter independence, native
  ODF frame roles, page-layout binding, text/list semantics, manifest reachability, reveal target
  semantics, and artifact selection using inline inputs and `tmp_path`; no real LibreOffice,
  subprocess conversion, date, network, or committed binary fixture enters pytest.
- Evidence or review, when useful: focused tests and the complete offline suite pass under
  `source source_me.sh && pytest tests/`.
- Obvious follow-ons: report exact test counts and failures to WP-D1.

### Work package: WP-V2 prove LibreOffice behavior

Archived resolution: the fixture-free 18-layout E2E, LibreOffice round trip, ODP-derived PDF check,
and one-time 99-page production build were accepted. The snapshot-specific artifact and pixel-metric
requirements below were not adopted as permanent gates.

- Owner: tester.
- Touch points: `tests/e2e/e2e_djot_native_layouts.py`, optional new
  `tests/e2e/e2e_odp_layout_semantics.py`, and
  `docs/active_plans/reports/native_odp_layout_acceptance.md`.
- Depends on: WP-I1.
- Acceptance criteria: rewrite `tests/e2e/e2e_djot_native_layouts.py` to build (1) a deterministic
  live-registry Djot specimen spanning all 18 layouts and (2)
  `genetics/djot/lect02a-2025_announcements.djot`. Canonical pages are the specimen's one-panel,
  two-panels, gallery, and multiple-choice physical pages plus physical page 3 of `lect02a`.
  The source IDs and SHA-256 values are recorded before build. The test asserts ODP/PDF page count
  equals compiled physical-slide count; exact 36.0/28.0 XML typography and native role topology;
  One Box and the semantic compatible alternate transition rules; one overflow-above-floor case;
  every reveal state; `lect02a` line 293 inline context; a generic context-handoff case; a
  metadata-only case; a source-local too-tall-leaf failure; `lect02a` Student Profile at line 470;
  and complete `lect02a` compilation.
- Acceptance criteria: each generated ODP runs `ODP -> FODP -> ODP` through two fresh isolated
  LibreOffice profiles. Each conversion must exit zero, create exactly one expected output, emit no
  `repair`, `recover`, `corrupt`, or error diagnostic (case-insensitive), and leave a package that
  validates manifest, bindings, role topology, style parents, sentinels, and timing. On either
  failure the harness retains both command streams, package excerpts, and diagnostic classification;
  it never converts a warning into a pass.
- Acceptance criteria: render PDFs at 144 DPI. Project compiled title/body rectangles into that
  coordinate system, expand each by 3 percent of its page dimension, and require nonzero dark
  foreground ink in every expected canonical text region. Title/body projected rectangles must not
  intersect. After excluding the footer/page-number margin, foreground ink outside the union of
  expected content regions is at most 5 percent. Every PDF page must be 16:10 within 0.5 percent.
- Evidence or review, when useful: write each run to
  `output/e2e/native_odp_layout_acceptance/latest/`: source IDs plus SHA-256, ODP/PDF artifacts,
  pre/post XML excerpts, per-command stdout/stderr, 144-DPI PNGs, and `acceptance.json`. Publish
  the durable human-readable report at
  `docs/active_plans/reports/native_odp_layout_acceptance.md`. Record LibreOffice version/build ID,
  package findings, transition records, metric results, and state-harness output. Failure of repair
  detection, layout reuse, reveal state, typography, or any metric blocks completion.
- Obvious follow-ons: give the machine-readable acceptance report to WP-D1 and WP-D2.

### Work package: WP-D1 update durable documentation

- Owner: maintainer.
- Touch points: [CODE_ARCHITECTURE.md](../CODE_ARCHITECTURE.md),
  [PIPELINE.md](../PIPELINE.md), [FILE_FORMATS.md](../FILE_FORMATS.md),
  [USAGE.md](../USAGE.md), [E2E_TESTS.md](../E2E_TESTS.md),
  [DESIGN_DECISIONS.md](../DESIGN_DECISIONS.md), and [CHANGELOG.md](../CHANGELOG.md).
- Depends on: WP-I1; completion language also depends on WP-V2.
- Acceptance criteria: after implementation evidence exists, docs describe ODP-first sibling adapters,
  the layered physical-plan modules, compiler/adapters, and their size targets,
  `PresentationTheme.template_path` as sole
  template authority, 36/28 defaults, bounded preflight, executable repair detection, V2 artifacts
  and metrics, cross-adapter parity, and removed modules. Before implementation completes, wording
  distinguishes current bridge behavior from approved target behavior. Old statements that make PPTX
  the ODP builder are replaced rather than contradicted elsewhere.
- Evidence or review, when useful: Markdown links and repo hygiene tests pass; changelog distinguishes
  plan publication, implementation, and observed verification accurately.
- Obvious follow-ons: archive this plan only after WP-D2 accepts the completed implementation.

### Work package: WP-D2 audit the completed migration

- Owner: independent reviewer.
- Touch points: read-only review of every changed source, test, binary, and documentation artifact.
- Depends on: WP-V1, WP-V2, and WP-D1.
- Acceptance criteria: reviewer finds no hidden PPTX-to-ODP path, duplicate geometry authority,
  compatibility facade, forbidden adapter import, stale `layouts.py` authority, discarded reveal
  intent, font-unit conversion, missing code/math/quote/attribute diagnostic, stale design claim,
  unowned repair/failure path, absent cross-adapter parity, or undocumented V2 artifact; every plan
  gate has linked evidence.
- Evidence or review, when useful: execute the D2 architecture searches after WP-I1:
  `rg -n "layouts\\.py|from slide_lib import layouts|import slide_lib\\.layouts" slide_lib tests`
  must report only explicitly documented historical/migration references; and
  `rg -n "pptx.*odp|odp.*pptx|render_template_odp|apply_template_master|odp_theme" slide_lib tests`
  must report no active bridge/theme-splice code. Inspect imports to confirm the exact compiler and
  writer boundaries, then compare the two adapter semantic projections page by page.
- Evidence or review, when useful: issue-severity report with all blockers and high-risk findings
  resolved before plan completion.
- Obvious follow-ons: integrator moves this plan with `git mv` to `docs/archive/` and records final
  acceptance evidence.

## Acceptance criteria and gates

### Architecture gate

- The format-neutral layout compiler imports no python-pptx or ODF serializer module.
- The ODP adapter imports no python-pptx module and makes no LibreOffice conversion call.
- ODP and PPTX serialize the same immutable layout plan independently.
- The `odp` and `pdf` format paths do not create a PPTX, including as a temporary file.
- The former theme-splice and PPTX-to-ODP construction path is removed.

### ODP structure gate

- Every page references one native presentation page layout matching the declared Djot layout.
- All 18 registered layouts have verified placeholder topology.
- A standard title is a `draw:frame` with `presentation:class="title"`.
- A one-panel body is a `draw:frame` with `presentation:class="outline"`.
- Generated text does not live in a text-bearing `draw:custom-shape` of type `ooxml-rect`.
- A headless LibreOffice open/save round trip retains page-layout references and presentation classes.
- The package passes bounded ZIP, XML, manifest, and ODF mimetype validation.

### Typography gate

- The OTP itself stores 36 pt standard title and 28 pt ordinary body/list defaults.
- Every measured face resolves to a committed, hash-verified OFL asset and immutable theme profile;
  missing, hash-mismatched, or unsupported style faces fail before publication instead of using a
  system substitute. PT Sans Narrow uses only its shipped applicable faces and never a fabricated
  italic fallback.
- The package-XML comparator reports a 36.0 pt title and 28.0 pt body for the fitting `lect02a`
  slide 3 specimen before and after the headless round trip.
- Compiled titles remain at or above 30 pt and ordinary text remains at or above 24 pt.
- Content that cannot meet its floor fails before an artifact is published and names the source
  location and affected slot.
- The capacity proof uses Pillow styled-run/token measurements, true OTP list text-start/hanging
  indents, and mixed-face ascent/descent line boxes. Its cache key includes font hashes and all
  measurement inputs; neither a `0.25em` heuristic nor a generic 10-percent width cap is allowed.
- Shrink-on-overflow is enabled on fixed presentation frames; scale-up-to-fill is not required.

### Layout-transition gate

- The deterministic package-XML transition interpreter reapplying One Box to `lect02a` slide 3
  leaves one authored title and one authored body.
- No empty Click to add Title or Click to add Text objects overlap existing content.
- The generated and captured-reference frames expose the same ODF presentation class, resize, and
  autofit properties before and after a headless LibreOffice round trip.
- The deterministic package-XML transition interpreter switching to one compatible alternate layout
  retains compatible title/body content exactly once.

### Continuation gate

- `lect02a-2025_announcements.djot` line 112 compiles to two or more physical pages at no less than
  24 pt ordinary text, with the same one-panel topology on every continuation page.
- The continuation plan preserves exact paragraph, root-list-subtree, table-row-group, and atomic
  object boundaries at the ordinary partition stage. Only an oversized root-list subtree may split,
  recursively, between descendant list-item subtrees; a too-tall leaf fails source-locally. The
  compiler uses `INLINE_STATIC` only when the minimum ancestor trail plus new descendant fits;
  otherwise it emits one immediately preceding static `CONTEXT_HANDOFF` page with
  `HANDOFF_STATIC`, or `METADATA_ONLY` when the trail itself cannot fit. The descendant then keeps
  its original level and must fit. Context remains static/no-reveal and every authored unit occurs
  exactly once without leaving a heading stranded at a page bottom.
- Physical IDs are deterministically `source_id-pN`, indexes are contiguous, page numbers count
  physical pages, qualified notes repeat, and reveal activation resets on each page with no
  cross-page target.
- Direct ODP and sibling PPTX adapters have identical physical-page count and source/continuation
  order for the same `LayoutDeck`; each adapter serializes the exact compiler-carried safe line
  advance and list indents, and package-level semantics are asserted separately.
- A synthetic failure specimen for each eligible grid proves the `DECOMPOSE_TO_ONE_PANEL` result has
  one-panel topology on every page, canonical reading-order slot provenance, repeated H1/context/
  qualified notes without labels, canonical image/table placement, one occurrence of each content
  unit and reveal, and deterministic identities. Fitting-grid specimens prove no decomposition.
  `paginate: false` and each excluded semantic layout fail source-located rather than changing
  topology.
- `lect02a-2025_announcements.djot` line 362 and the full deck compile successfully through the
  public CLI. Direct ODP and sibling PPTX must have identical page count, physical identity,
  source/continuation order, and per-page topology for the resulting `LayoutDeck`.
- The V2 report records the display mode, physical continuation kind, trail metadata, note, and
  accessibility projection for `lect02a` line 293, generic handoff and metadata-only specimens, the
  expected leaf failure, Student Profile at line 470, and the full deck. All gates run from committed
  fixtures and scripted commands without an attended LibreOffice interaction.

### Content and reveal gate

- Text, emphasis, links, nested lists, tables, images, alt text, and notes remain independent editable
  native objects.
- Object appear, object fade, and outline cascade reveals preserve first-frame visibility, source
  order, click count, target identity, and effect in the synthetic reveal state harness.
- Unsupported content or reveal intent fails with a source-located diagnostic; it is never dropped
  or rasterized.

### Integration gate

- PDF is exported from the direct native ODP.
- PPTX remains independently editable and passes its existing semantic/animation tests.
- The full Genetics build completes with matching source, ODP, PPTX where requested, and PDF page
  counts and no full-slide raster fallback.
- The complete fast suite and native-layout E2E pass in the documented Python 3.12 environment.
- An independent review resolves all blockers and high-risk findings.

## Test and verification strategy

### Autonomous evidence ladder

The desired static ODP XML contract is fixed by WP-E1 before implementation begins. It names the
required page-layout, presentation-frame, style-parent, layer, autofit, and object-count invariants
for each role. The committed minimal reference artifacts are stable comparators, not test inputs for
permanent pytest: they document the smallest known-good LibreOffice structure and remain outside the
fast suite's fixture policy.

Each successive level answers a different question and is executable by the manager and subagents:

1. Package/XML inspection is primary. Fast tests and the E2E inspect generated ODF structure,
   manifest reachability, styles, frame roles, typography, and timing nodes against the fixed
   contract.
2. A headless LibreOffice open/save round trip confirms that the installed application preserves the
   generated package without repair or role loss. The E2E compares the saved package with the same
   invariants; it never treats byte identity as a requirement.
3. A deterministic package-XML transition interpreter applies One Box and a compatible alternate
   layout to generated and captured-reference slides, then asserts presentation-member counts,
   roles, text retention, resize/autofit properties, and absence of duplicate placeholders.
4. Structural timing inspection and a deterministic reveal-state interpreter interpret each ODF/
   SMIL activation state. The harness asserts initial visibility, activation count, target identity,
   source order, and effect for object appear, object fade, outline cascade, and multiple-choice
   answer reveals.

The E2E writes machine-readable JSON and package excerpts for each level. A failed level blocks its
work package with a reproducible artifact and command; a passing level is sufficient to dispatch its
dependent package. No acceptance step depends on interactive operation.

Fast pytest protects stable behavior only:

- Compile small inline semantic decks to `LayoutDeck` and assert role, containment, order, and floor
  behavior.
- Serialize miniature plans to `tmp_path` and inspect XML with restrictive parsing.
- Assert page-layout/frame relationships rather than volatile generated style names or ZIP bytes.
- Assert manifest reachability and atomic publication failure behavior.
- Assert adapter selection with mocks; never invoke LibreOffice from pytest.
- Preserve meaningful existing PPTX semantic and animation tests at the adapter boundary.

Live E2E protects application behavior:

- Run through `source source_me.sh && python3 tests/e2e/e2e_djot_native_layouts.py`.
- Build `lect02a-2025_announcements` through the public CLI in each relevant format.
- Headlessly open/save the ODP through a dedicated temporary profile and inspect the saved package.
- Export the PDF from that ODP and compare selected page-image metrics with explicit tolerances.
- Keep generated probes and converted files in `output/`. Keep only the explicitly justified minimal
  reference artifacts under `tests/fixtures/odp_native_layouts/`; permanent pytest does not load
  those binary artifacts.

Autonomous acceptance protects layout transitions and reveal semantics that package inspection alone
cannot prove:

- Create reference and generated documents from inline fixtures through a dedicated headless
  LibreOffice profile; inspect title/body properties in package XML and apply One Box plus a
  compatible alternate layout through the deterministic transition interpreter.
- Assert the 36.0/28.0 point values on fitting content and an overflow specimen at or above its
  build-time floor.
- Drive object appear, object fade, outline cascade, and multiple-choice answer reveals through a
  deterministic state harness that validates each activation state against the ODF/SMIL timing tree.

Any repair dialog, duplicate placeholder, missing reveal, sub-floor build, or intermediate PPTX on the
ODP/PDF path blocks progression.

## Migration and compatibility policy

- Replace the pre-production architecture directly; do not keep a legacy rendering flag.
- Keep Djot source and `native_model.Deck` stable. The migration changes output implementation, not
  the authoring grammar.
- Keep public format names `odp`, `pdf`, `pptx`, and `all` stable while making each request generate
  only its required dependency graph.
- Preserve PPTX as an optional artifact, but do not promise PowerPoint slide-layout membership in
  this migration. Its contract is editable semantic content and bounded OOXML reveals.
- Version the output behavior through the changelog and release notes rather than embedding a
  compatibility mode in files.
- Delete `odp_theme.py` once its only caller disappears. WP-I1 alone deletes `layouts.py`, only after
  WP-L2 has migrated format-neutral authority, WP-P1 has moved the legacy PPTX projection, and both
  adapters consume the shared plan; it leaves no facade, compatibility alias, or re-export.

## Risk register

| Risk | Impact | Trigger | Owner | Mitigation |
| --- | --- | --- | --- | --- |
| ODF written by tests differs from Impress behavior | High | Open/save changes roles or repairs file | WP-O1 | Compare native sample, ODF 1.3, and live save |
| Mixed text/image slots lack one placeholder mapping | High | Applying layout detaches content | WP-L1 | Model primary slot member separately from components |
| Native ODF reveals differ across LibreOffice builds | High | State-harness order/effect mismatch | WP-A1 | Use bounded effects and exact native reference |
| OTP binary edit hides unintended changes | Medium | Unrelated ZIP members or styles change | WP-T1 | Inspect member diff and assert explicit theme contract |
| Font metrics shrink slightly across machines | Medium | Fitting content crosses floor | WP-L2 | Conservative estimator, full placeholder height, safety margin |
| Host substitutes or metric drift changes capacity | High | Font face/hash/style differs or line break moves | WP-T2 | Committed OFL assets, immutable profiles, hash checks, and V2 drift evidence |
| Adapter refactor regresses PPTX | Medium | Existing semantic tests fail | WP-P1 | Preserve tests and compare through shared plan |
| Duplicate geometry survives in an adapter | High | Adapter computes slot rectangles | WP-D2 | Architecture search and independent review |
| Plan drifts during implementation | Medium | New path lacks owner or gate | WP-D1 | Keep this plan current and report by work-package ID |

## Rollout and release checklist

- [x] WP-E1 and WP-E2 publish native LibreOffice contract evidence.
- [x] WP-L1 freezes the physical layout model.
- [x] WP-T1 updates and verifies the OTP 36/28 contract.
- [x] WP-T2 verifies committed font assets, immutable profiles, exact measurement, and runtime-drift evidence before compiler capacity acceptance.
- [x] WP-L2 compiles all 18 layouts without format imports (171 focused tests; independently
  accepted 2026-09-08).
- [x] WP-O1 through WP-O3 produce feature-complete static native ODP.
- [x] WP-P1 preserves independent PPTX output.
- [x] WP-A1 passes structural and state-harness reveal acceptance.
- [x] WP-I1 removes the PPTX-to-ODP path and obsolete modules.
- [x] WP-V1 passes focused and full permanent pytest.
- [x] WP-V2 resolves through the bounded evidence-tier decision: the native-layout E2E and one-time
  `lect02a` build pass without retaining snapshot-specific proof machinery.
- [x] WP-D1 synchronizes all durable documentation and changelog entries.
- [x] WP-D2 resolves every blocker and high-risk audit finding.
- [x] The integrator archives this completed plan with final evidence.

## Documentation close-out requirements

- Active plan / progress tracker: keep this file current by work-package ID while implementation is
  active, then move it with `git mv` to `docs/archive/` after acceptance.
- `docs/CHANGELOG.md` entry: record the initial plan separately from the implementation, removed
  bridge, 36/28 behavior, tests, live LibreOffice version, and any failed approach.
- Architecture docs: update the diagram and ownership in [CODE_ARCHITECTURE.md](../CODE_ARCHITECTURE.md)
  and [PIPELINE.md](../PIPELINE.md).
- Operator docs: document artifact selection, direct ODP, typography floor semantics, and autonomous
  E2E in [USAGE.md](../USAGE.md) and [E2E_TESTS.md](../E2E_TESTS.md).
- Design records: replace superseded PPTX-parent statements in
  [DESIGN_DECISIONS.md](../DESIGN_DECISIONS.md); do not append contradictory decisions.
- Completion notes: link the evidence-tier decision and independent review from the archived plan.

## Patch plan and reporting format

- Patch 1, `ODP-CONTRACT`: WP-E1, WP-E2, and the locked evidence report.
- Patch 2, `LAYOUT-CORE`: WP-L1, WP-L2, and WP-T1.
- Patch 3, `NATIVE-ODP`: WP-O1, WP-O2, and WP-O3.
- Patch 4, `PPTX-ADAPTER`: WP-P1.
- Patch 5, `ODP-REVEALS`: WP-A1.
- Patch 6, `PIPELINE-SWITCH`: WP-I1 and removal of superseded code.
- Patch 7, `ACCEPTANCE`: WP-V1, WP-V2, WP-D1, and WP-D2 findings.

Every implementation report states:

- patch label and completed work-package IDs;
- files changed and architectural boundary affected;
- focused and full validation commands with outcomes;
- remaining dependencies, risks, and next dispatchable package;
- whether output evidence came from package inspection, deterministic package-XML transition,
  headless conversion, PDF/render metrics, or the reveal-state interpreter.

## Open questions and decisions needed

- Manager/subagent decision procedure:
  - Decision owner or dedicated class: WP-E1 tester proposes exact ODF properties; WP-L1 architect
    accepts them only when native LibreOffice output, ODF 1.3 semantics, and open/save behavior agree.
  - Evidence and decision rule: when native output and documentation differ, use the smallest ODF
    structure that LibreOffice 26.2.6.3 writes and preserves without repair, then record the observed
    extension explicitly. The decision changes serialization details, not the direct-ODP architecture.
- Non-blocking follow-up: consider native PPTX slide-layout membership after ODP acceptance if it
  improves interchange editing without weakening the shared-plan boundary.
- Non-blocking follow-up: consider user-selectable typography policies only after the single
  repository theme contract has stable evidence across representative Genetics decks.
