# WP-A1 animation fidelity evidence

Date: 2026-09-07

Status: implementation and headless acceptance complete; attended playback observation open.
The earlier PowerPoint-authored-deck premise is superseded; it recorded a real host inventory but
was not a project requirement.

## Current contract

LibreOffice Impress and ODP are the editing and playback contract. PPTX is a convenient native
builder and interchange artifact because Python support is stronger than ODP support. Microsoft
PowerPoint is neither a compatibility oracle nor an acceptance gate.

WP-A1 establishes the smallest useful evidence for the supported animation surface:

- `appear` and `fade` effects;
- `object` and `paragraphs` sequences;
- `on-click` trigger;
- a top-level list item and its descendants for a paragraph sequence.

Use official OOXML documentation and LibreOffice importer/exporter behavior to guide the builder.
`slide_lib/pptx_animation.py` is the sole programmatic OOXML owner. It builds the required
timing tree directly; no runtime XML templates or PowerPoint-authored reference decks are needed.

## Historical evidence retained

The 2026-09-06 check found no PowerPoint app in the bounded macOS paths. LibreOffice 26.2.5.2 is
installed. A direct UNO Python route was killed after its local dependency/process route proved
unsuitable for this task; the existing headless LibreOffice bridge works. The command evidence is
retained in [ENVIRONMENT.md](../../../devel/animation_reference/ENVIRONMENT.md).

## Acceptance evidence

The following evidence is recorded for minimal generated decks:

1. PASS -- permanent offline structural tests verify one timing root, source-ordered shape targets,
   inclusive top-level paragraph ranges, APPEAR visibility, FADE transition, and rejection of any
   existing timing tree. Parser tests separately verify source-located cascade restrictions; `fade`
   remains a direct-IR backend capability rather than new Djot spelling.
2. PASS -- one-time PPTX package inspection and headless LibreOffice 26.2.5.2 conversion preserved
   timing roots, native shape/paragraph targets, editable ODP text/drawing objects, and the bounded
   APPEAR/FADE semantics.
3. OPEN -- an attended Impress launch reached `soffice`, but macOS denied Screen Recording and
   Accessibility before F5 or any click could be sent. It did not establish object or outline
   playback. Repeat with those permissions granted to the automation process.
4. PASS -- one-time ODP-to-PDF export produced final-state pages containing all revealed content.
   This confirms final-state presentation, not click-by-click playback.

The attended Impress check is the only visual playback gate. Package inspection and conversion are
one-time implementation evidence, not permanent pytest work. The permanent tests remain fast,
offline structural checks of the builder's supported semantic model.

## Recorded implementation evidence

The permanence-audited suite contains 1,635 tests, including the four focused structural M5 tests.
The Djot native-layout PPTX-to-ODP-to-PDF E2E also passed as separate one-time evidence. A direct-IR
FADE fixture used a one-second OOXML duration and LibreOffice retained it as a one-second ODP fade
transition.

The disposable artifacts and detailed execution reports used a private temporary directory. They
are implementation evidence, not repository fixtures or a permanent test dependency. No PowerPoint
artifact, application, or acceptance check is part of this contract.
