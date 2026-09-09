# Native ODP layout contract

Archived 2026-09-08. The binary fixtures and one-time fixture readers described below were removed
after direct native ODP generation and the inline-input all-layout LibreOffice E2E replaced them.

## Scope and method

This WP-E1 report locks the structural contract for title, subtitle, outline, and graphic object frames.
It uses package XML and headless LibreOffice only; it does not make an attended UI action a dependency.
The source set is `genetics/xlect99-template_2023.otp`, the native
`genetics/lect02a-2025_announcements.odp`, and the generated
`output/odp/lect02a-2025_announcements.odp`.

The installed local executable reports `LibreOffice 26.2.6.3
8221e31b3ac356a1623c672912a3d2b492f7e3d1`, the same build ID the user reported.
The screenshots remain useful diagnosis of the One Box failure, but package and headless evidence
below is the automated acceptance basis.

## WP-L2 implementation handoff

WP-L2, the format-neutral compiler that will feed the direct ODP and sibling PPTX writers, is
implemented and independently accepted. Its 171 focused tests establish all-18-layout compilation
without output-format imports; exact committed-font measurement and cache/session identity,
including quarter-point sizes; 36 pt / 28 pt defaults and 30 pt / 24 pt floors; grapheme-safe
explicit breaks; recursive context modes; table and unsupported-fact parity; and generic-grid
stream co-packing with immutable provenance. The complete `lect02a` source deterministically
produces 99 physical pages. A cold compile of about 0.69 seconds is diagnostic evidence, not a
release threshold. The compiler's modules meet their established budgets: public engine 290 lines,
registry 77, measurement 634, and builders 669.

The compiler resolves the `lect02a` line 243 title through its shared title floor, preserving it as
one atomic semantic object; it does not use rejected leaf fragmentation. Atomic leaf failure remains
the policy when content truly cannot fit. This establishes plan authority only. WP-O1 and WP-P1 must
still project that `LayoutDeck` without remeasurement or pagination, and their native ODP/PPTX and
LibreOffice acceptance evidence remains open.

## Native role topology

The OTP `Default` master declares title and outline placeholders on the `backgroundobjects` layer:

```xml
<draw:frame presentation:class="title" presentation:style-name="Default-title"
 draw:layer="backgroundobjects" svg:x="1.4cm" svg:y="0.698cm"
 svg:width="25.199cm" svg:height="2.921cm"/>
<draw:frame presentation:class="outline" presentation:style-name="Default-outline1"
 draw:layer="backgroundobjects" svg:x="1.4cm" svg:y="4.094cm"
 svg:width="25.199cm" svg:height="11.146cm"/>
```

Authored slide content is a distinct, layout-owned member. Its page references a named presentation
layout and authored frames use the `layout` layer. The native `lect02a` samples resolve their
`presentation:style-name` through automatic styles.

| Role and observed variant | Native element and class | Parent style | Layer | Observed fit properties |
| --- | --- | --- | --- | --- |
| OTP master title placeholder | `draw:frame`, `title` | `Default-title` | `backgroundobjects` | `draw:auto-grow-height="true"`, `fo:min-height="2.921cm"`. |
| Authored native title | `draw:frame`, `title` | automatic style parented to `Default-title` | `layout` | `draw:auto-grow-height="true"`, with the same 2.921 cm minimum. |
| OTP master subtitle placeholder | `draw:frame`, `subtitle` | `Default-subtitle` | `backgroundobjects` | `draw:auto-grow-height="true"` and a slot-specific minimum height. |
| Authored native subtitle | `draw:frame`, `subtitle` | automatic style parented to `Default-subtitle` | `layout` | `draw:auto-grow-height="true"` and its slot-specific minimum height. |
| Outline | `draw:frame`, `outline` | `Default-outline1` | `layout` | Slot-specific `fo:min-height`; inherited root style fixes height and requests shrink. |
| Graphic object | `draw:frame`, `graphic`, containing `draw:image` | Graphic style, not `Default-*` | `layout` | Image geometry owns object fitting; no shrink contract was observed. |

The inherited root outline behavior in the OTP is:

```xml
<style:style style:name="Default-outline1" style:family="presentation">
  <style:graphic-properties draw:auto-grow-height="false" draw:fit-to-size="false"
   style:shrink-to-fit="true"/>
</style:style>
```

Native fixed outline frames use shrink-on-overflow, not proportional scale-up. Title and subtitle
samples instead use auto-grow-height. This is historical reference evidence, not a reason to weaken
the approved target: generated standard title/body slots must be fixed frames with explicit
`style:shrink-to-fit="true"`, after compiler preflight protects the 30 pt / 24 pt floors.

## Slide 3 comparison

Slide 3 is the smallest complete One Box comparator. Its document-local layout identifier is
`AL2T1`, which resolves in this package to the ordered `title + outline` topology. Layout identifiers
are opaque serialization details: the contract validates their resolved placeholder topology, not a
literal identifier. The generated ODP has only a master-page reference. Counts include direct
children of slide 3 and exclude master-page background objects.

| Artifact and state | Page-layout name | Direct title frames | Direct outline frames | Text-bearing `ooxml-rect` shapes | Direct content objects |
| --- | --- | ---: | ---: | ---: | ---: |
| Native `lect02a`, before headless round trip | `AL2T1` | 1 | 1 | 0 | 2 |
| Native `lect02a`, after headless round trip | `AL2T1` | 1 | 1 | 0 | 2 |
| Generated `lect02a`, before headless round trip | absent | 0 | 0 | 3 | 3 |
| Generated `lect02a`, after headless round trip | absent | 0 | 0 | 3 | 3 |

The native authored objects are exactly one title and one outline frame:

```xml
<draw:frame presentation:style-name="pr1" draw:layer="layout"
 presentation:class="title">...</draw:frame>
<draw:frame presentation:style-name="pr6" draw:layer="layout"
 presentation:class="outline" presentation:user-transformed="true">...</draw:frame>
```

`pr1` is a `presentation` style parented to `Default-title`; `pr6` is parented to
`Default-outline1`. The generated slide instead starts with three generic imported shapes:

```xml
<draw:custom-shape draw:name="TextBox 1" draw:style-name="gr7" draw:layer="layout">...
  <draw:enhanced-geometry draw:type="ooxml-rect"/>
</draw:custom-shape>
```

The other two are `TextBox 2` and `TextBox 3`; none has `presentation:class` or a
`presentation:style-name`. The title shape is `1.175cm` high, while native slide 3's title is
`2.921cm` high. That approximately 40 percent frame-height difference supports the hypothesis that
LibreOffice's existing shrink-on-overflow policy produced the observed 30.6 pt display from a 36 pt
stored run. Geometry alone does not measure the resolved display size, so this report does not claim
that it has directly observed 30.6 pt through UNO.

## Comparator fixtures

The user explicitly requested captured fixtures so this work has no attended UI dependency. The
fixture directory contains two deterministic, XML-only role comparators in addition to WP-E2's
reveal fixture:

- `one_box_native_roles.odp` is a pruned captured comparator with the six ODP members required by
  its XML contract. It retains a document-local `AL2T1` layout identifier that resolves to
  `title + outline`, one native frame per role, exact role sentinels, the required
  `Default-title` / `Default-outline1` style chains, and explicit fixed shrink-only overrides.
- `one_box_generic_text.odp` contains the equivalent short sentinel text in generic text boxes on a
  blank layout. It preserves the negative text-bearing `ooxml-rect` topology that caused the One
  Box overlap.

These compact fixtures are deterministic XML-contract inputs, not standalone LibreOffice
round-trip documents. In particular, the pruned positive comparator is deliberately not passed to
LibreOffice by the E2E. The actual serialized preservation proof uses the complete
`genetics/lect02a-2025_announcements.odp` and inspects slide 3 after `ODP -> FODP -> ODP`.
Fixture provenance, package shape, visual styling, and timestamps are not contract data beyond the
recorded structural assertions.

| Fixture | Bytes | SHA-256 |
| --- | ---: | --- |
| `one_box_native_roles.odp` | 13,551 | `bb6b6d547943a8bd9b84f2825cb889fba99b922268d188f0c47bbf7b1b9a0469` |
| `one_box_generic_text.odp` | 21,060 | `32a372812a5e6d74b1ab5ee45da5c43cda88a3503803ea983eb8623ca5029512` |

### Direct-content predicate

Every `Direct content objects` count uses one executable predicate. A direct content member is a
direct child of `draw:page` whose QName is `draw:frame`, `draw:custom-shape`, `draw:g`, or
`draw:connector`; it is not `draw:forms`, not a descendant of `draw:forms`, and not descended from
`presentation:notes`. Text-bearing `ooxml-rect` counts are the subset of direct
`draw:custom-shape` members with `draw:enhanced-geometry draw:type="ooxml-rect"` and non-blank
descendant text. The harness implements this over direct page children, excluding note thumbnails,
controls, and master-page background objects.

## Automated transition contract

The layout transition is testable without driving the GUI:

1. A One Box page is structurally satisfied only by one direct `title` frame and one direct
   `outline` frame whose page-layout identifier resolves to that ordered topology.
2. The native slide already satisfies that topology, so applying the same layout has no missing role
   to synthesize: its structural count stays two content members.
3. The generated slide has neither role. Repairing the topology requires two placeholders while its
   three generic text objects remain ordinary objects, producing the five-object overlap pattern
   reported in the user's One Box screenshot.
4. The captured compatible alternate's document-local identifier is `AL4T3`. It resolves to the
   ordered `title + outline-primary + outline-secondary` topology. The identifier is evidence about
   this captured package only; transition expectations use the resolved ordered roles. Applying this
   compatible topology to the native One Box source maps the authored title and primary outline once
   each, then creates only one empty secondary outline. It creates no duplicate authored content or
   empty title/primary-outline placeholder.

The deterministic package-XML interpreter rejects malformed source membership, duplicate authored
slot mappings, duplicate compatible-layout definitions, and target topologies that would displace an
authored primary slot. It is a contract for the direct writer, not a claim that parsing XML invokes
LibreOffice's UI command. It gives the direct ODP adapter an objective postcondition: after a
compatible layout assignment, slide 3 contains exactly one title frame and one primary outline frame,
no text-bearing `ooxml-rect`, and at most one empty secondary outline when the target topology adds
that compatible slot. The user screenshot independently corroborates the three-plus-two failure
state but is not required to run this check.

`tests/e2e/e2e_odp_layout_semantics.py` is the autonomous executable implementation of this
contract. Its deterministic XML checks validate both fixtures: direct native frames and roles,
`layout` layer, opaque layout-id resolution to `title + outline`, exact normalized sentinels,
the `Default-title` / `Default-outline1` parent chains, and explicit fixed shrink-only policy.
The negative fixture must retain exactly two generic text-bearing `ooxml-rect` shapes, no role
classes, no page-layout binding, and its exact sentinels. The harness also mutates copied XML to
prove rejection of missing layout resolution, style parentage, shrink policy, sentinel changes,
generic shapes pretending to be title frames, duplicate authored mappings, duplicate compatible
layouts, and incompatible target-role ordering. Run the XML-only contract without LibreOffice:

```text
source source_me.sh && python3 tests/e2e/e2e_odp_layout_semantics.py --xml-only
```

The serialized portion runs only against the complete native deck's slide 3. It converts that deck
through isolated `ODP -> FODP -> ODP` LibreOffice processes, then rechecks its resolved title-plus-
outline topology, role classes, exact source sentinels, and title/outline style-parent chains. It
does not import `pyuno`, depend on a numeric UNO `Layout` mapping, use network or GUI interaction,
or require an attended cleanup step.

## Headless round-trip evidence

Using two isolated LibreOffice profiles, the autonomous E2E converts the complete native deck from
ODP to FODP and then back to ODP in a temporary workspace. It removes that workspace after XML
inspection, so it has no human cleanup dependency. It does not claim an ODP-to-ODP conversion is a
save operation and does not round-trip the pruned comparator fixture.

```text
/Applications/LibreOffice.app/Contents/MacOS/soffice --headless \
  -env:UserInstallation=file:///private/tmp/<profile-one> \
  --convert-to fodp --outdir /private/tmp/<fodp-output> \
  genetics/lect02a-2025_announcements.odp
/Applications/LibreOffice.app/Contents/MacOS/soffice --headless \
  -env:UserInstallation=file:///private/tmp/<profile-two> \
  --convert-to odp --outdir /private/tmp/<odp-output> \
  /private/tmp/<fodp-output>/lect02a-2025_announcements.fodp
```

The saved complete native deck retains slide 3's title-plus-outline resolved layout topology, the
two frame classes, their style parents, and its exact title/body sentinel text. The historical
generated-deck comparison established that its blank-layout PPTX path retained no page-layout
binding and serialized generic `ooxml-rect` shapes; LibreOffice does not infer presentation
membership from a master-page reference or generic text geometry.

Headless conversion confirms structural preservation. It cannot establish context-menu enablement or
visual overlap; those former manual observations are intentionally excluded from completion criteria.

## Locked implementation contract

WP-L1, WP-T1, and WP-O1 must implement these invariants:

- Give each page an explicit `presentation:presentation-page-layout-name` derived from layout
  topology. The serialized name is document-local and opaque; validate that it resolves to the
  intended ordered placeholder topology rather than requiring `AL2T1`.
- Emit standard title/body text as `draw:frame` elements on the `layout` layer with
  `presentation:class="title"` or `presentation:class="outline"`, plus a
  `presentation:style-name`. Do not serialize standard text into `ooxml-rect` custom shapes.
- Parent title, subtitle, and outline automatic styles to `Default-title`, `Default-subtitle`,
  and `Default-outlineN`, respectively. Use point-valued 36 pt / 28 pt defaults and the approved
  fixed-frame shrink-only policy.
- Emit an image primary slot as a `draw:frame presentation:class="graphic"` with a graphic style
  and contained `draw:image`; it is not a text placeholder and does not inherit
  `Default-outlineN`.
- Preserve role classes and page-layout bindings through a LibreOffice headless ODP round trip.
  The automated comparator must reject every text-bearing `ooxml-rect`.

## Residual risks

- The OTP stores only the layouts exercised when it was saved. The direct writer needs stable native
  page-layout definitions for all 18 registry topologies; this report validates the role model, not
  every future layout name.
- Native title/subtitle samples use auto-grow-height while the target requires fixed title/body
  frames with bounded shrink. WP-T1 must set and test that policy explicitly rather than copy one
  historical automatic style.
- Headless testing proves structure is retained, not that a particular LibreOffice UI control is
  enabled. Automated acceptance compares ODF role topology and save preservation.
- This report does not cover reveal timing; WP-E2 owns ODF/SMIL target and playback semantics.

## WP-E2 native reveal contract

### Evidence, provenance, and reproducibility

This section locks the bounded ODF/SMIL reveal surface for WP-A1. The captured comparator is a
hand-authored, minimal native ODP package rather than a LibreOffice export or a PPTX derivative:
`tests/fixtures/odp_native_layouts/native_reveal_contract.odp`. It contains only the required ODP
members: uncompressed `mimetype`, `content.xml`, `styles.xml`, `meta.xml`, `settings.xml`, and its
manifest. It has no master pages, themes, thumbnails, notes, media, or imported style baggage.

The fixture is 2,145 bytes as a ZIP file (5,607 bytes uncompressed), with SHA-256
`91c29afe5510d42bef9fd333aad5907982ea2f305bcfeec4a8d825deffc14e0c`. It deliberately contains
four slides only: object appear, top-level outline cascade with a structurally nested child,
multiple-choice answer appear, and object fade. The package uses native `draw:frame` object targets,
not OOXML bridge shapes.

Run the complete reproducible check with the repository Python 3.12 environment:

```text
source source_me.sh && python3 tests/e2e/e2e_odp_reveal_semantics.py \
  tests/fixtures/odp_native_layouts/native_reveal_contract.odp
```

The executable first performs XML-only interpretation. It then creates two fresh temporary,
isolated LibreOffice profiles and performs the real transition `ODP -> FODP -> ODP`; it reruns the
same strict interpreter on the resulting ODP before deleting the workspace. The equivalent
headless commands are:

```text
/Applications/LibreOffice.app/Contents/MacOS/soffice --headless \
  -env:UserInstallation=file:///private/tmp/<profile-one> \
  --convert-to fodp --outdir /private/tmp/<fodp-output> <fixture>.odp
/Applications/LibreOffice.app/Contents/MacOS/soffice --headless \
  -env:UserInstallation=file:///private/tmp/<profile-two> \
  --convert-to odp --outdir /private/tmp/<odp-output> <fixture>.fodp
```

The verified command exits 0 on LibreOffice 26.2.6.3 for macOS. The verifier never imports pyuno,
uses no network, clock, GUI interaction, or attended slideshow playback, and does not accept
same-format conversion as preservation evidence.

### Exact target and timing-tree topology

Every specimen has one direct timing root on `draw:page`. In normalized form the common tree is:

```xml
<anim:par presentation:node-type="timing-root">
  <anim:seq smil:dur="indefinite" presentation:node-type="main-sequence">
    <anim:par smil:begin="next" smil:fill="hold"
     presentation:node-type="on-click">
      <!-- exactly one effect node -->
    </anim:par>
  </anim:seq>
</anim:par>
```

`smil:begin="next"` is the on-click advance contract. Sibling on-click `anim:par` nodes are the
source-ordered click sequence. `smil:fill="hold"` keeps the revealed state after its activation.
The direct ODP writer must emit one root and one `main-sequence` per slide with reveals; a static
slide must emit no timing root. It must not create one timing root per effect.

| Specimen | Stable target identity and target node | Click effect node | Locked semantic state |
| --- | --- | --- | --- |
| Object appear | `id1`, a `draw:frame` with both `xml:id="id1"` and `draw:id="id1"`, text `Object appear target` | `<anim:set smil:dur="0.001s" smil:fill="hold" smil:targetElement="id1" smil:attributeName="visibility" smil:to="visible"/>` | Hidden at frame 0; visible after click 1. |
| Outline cascade | `id2` then `id3`, top-level `text:p` nodes with matching `xml:id` and `text:id`, text `Cascade parent` then `Cascade second` | One otherwise-identical `anim:set` per target, in that source order | Both top-level items hidden at frame 0; click 1 reveals the parent and its child list; click 2 reveals the second root item. The child has no identity or click. |
| Multiple-choice answer | `id4`, a `draw:frame` with both `xml:id="id4"` and `draw:id="id4"`, text `Answer: A. Question` | Same `anim:set` visibility node with target `id4` | Question and choices are initially visible; answer popup is hidden at frame 0 and visible after click 1. |
| Object fade | `id5`, a `draw:frame` with both `xml:id="id5"` and `draw:id="id5"`, text `Object fade target` | `<anim:transitionFilter smil:dur="1s" smil:fill="hold" smil:targetElement="id5" smil:type="fade" smil:subtype="crossfade"/>` | Hidden at frame 0; target becomes visible through a one-second crossfade after click 1. |

Object identities are valid only when `xml:id` and `draw:id` both exist and match. Paragraph
identities are valid only when `xml:id` and `text:id` both exist and match. All target IDs are
unique within their slide. WP-A1 must target those identities directly, never a serialized object
ordinal, generated style name, or visible text string.

### Deterministic source-state interpretation

The state harness is intentionally small and explicit:

1. Require exactly one direct `timing-root`, containing only one `main-sequence` with
   `smil:dur="indefinite"`; reject all timing nodes outside that root.
2. Require each direct sequence child to be an `on-click` `anim:par` with exactly
   `smil:begin="next"` and `smil:fill="hold"`.
3. Require each click to have exactly one effect child and no unsupported attributes: either an
   `anim:set` with `visibility -> visible`, `0.001s`, and `hold`, or a `transitionFilter` with
   `fade`, `crossfade`, `1s`, and `hold`. Both effect forms are leaves.
4. Resolve object targets only through a native `draw:frame` with its matching `xml:id` and
   `draw:id`; a `draw:custom-shape` never satisfies an object reveal target. Resolve paragraph
   targets through their matching identity pair. Require unique targets and require click
   activation order to equal visual source order.
5. Require the cascade's `Cascade child` list to be structurally nested in the first root list item;
   it must have no target identity and no independent click.
6. Reject every extra timing root, animation-namespace descendant outside the sole timing-root
   subtree, node, attribute, effect child, target, or unsupported source reveal intent the bounded
   writer cannot encode. The executable includes XML-only negative self-tests for a custom-shape
   target, a stray nested animation node, and an effect child; they run before LibreOffice.

Running the interpreter with the repository Python 3.12 command produced the following exact
ordered states:

```text
slide 1: appear object id1 Object appear target: hidden -> visible (click 1)
slide 2: appear paragraph id2 Cascade parent: hidden -> visible (click 1)
         appear paragraph id3 Cascade second: hidden -> visible (click 2)
slide 3: appear object id4 Answer: A. Question: hidden -> visible (click 1)
slide 4: fade object id5 Object fade target: hidden -> visible (click 1, 1s crossfade)
```

This is a structural state interpretation, not an assertion that package XML can rasterize or
visually simulate LibreOffice's interpolation. It locks first-frame membership, click count, target
identity, source ordering, and the effect attributes that WP-A1 must preserve. A future live E2E
may compare rendered first/final frames, but no attended playback is a prerequisite for this plan.

### Handoff to WP-A1

WP-A1 owns `slide_lib/odp_animation.py` and must implement this complete contract now: allocate
stable draw IDs for object-reveal objects and XML IDs for top-level cascade paragraphs in the
format-neutral layout plan; write the single-root tree; emit the two exact effect forms above; and
reject unsupported source intent with a source-located error. Its success condition is that generated
direct ODP packages produce the same deterministic state sequence for ordinary and multiple-choice
specimens, survive the ODP-to-FODP-to-ODP transition, and retain native ODP target nodes. Its
validation step is a fast inline-plan structural test plus the autonomous E2E state harness; neither
loads this binary comparator from permanent pytest.

### Negative evidence and residual risks

- No LibreOffice headless API was found that advances a slideshow click timeline and exposes a
  rendered intermediate frame. The contract consequently does not claim pixel-level fade playback;
  it uses saved ODF/SMIL semantics and deterministic state transitions.
- LibreOffice normalization can omit redundant timing-root duration/restart attributes. Tests must
  not reject that normal save behavior.
- The controlled fixture confirms LibreOffice preservation of paired native object/paragraph target
  identities and a genuinely nested cascade through an ODP-to-FODP-to-ODP conversion. It does not
  prove arbitrary nested-list depths or simultaneous/choreographed effects; those are outside the
  bounded reveal surface and must be rejected.
- The state harness validates serialized ODF/SMIL semantics and ordering, not pixel interpolation
  during attended playback. A future visual E2E can add rendered-frame evidence without weakening
  this deterministic contract.
