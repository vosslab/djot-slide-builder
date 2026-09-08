# Roadmap: extended-Djot native presentations

Status: M1-M6 implementation is complete, including one-time all-eight corpus acceptance, private
regeneration reproducibility, native acceptance, and M5's headless LibreOffice bridge/PDF evidence.
M5's attended Impress click-playback observation remains open because macOS permissions blocked the
attempt before slideshow control. Djot is the sole authored source front end to the native
editable-object pipeline.

## Current milestones

| M | Title | Status | Evidence boundary |
| --- | --- | --- | --- |
| M1 | IR and catalog | Complete | Presentation-neutral nodes and registry-derived grammar |
| M2 | Djot parser | Complete | `.djot` source parses to named cells with source locations |
| M3 | Short layouts and multiple choice | Complete | Canonical names and slot contracts, no aliases |
| M4 | Djot export | Complete | `.djot` is the only admitted deck source suffix |
| M5 | Animation backend | Implementation complete; attended gate open | Bounded OOXML builder; permanent structural and one-time bridge/PDF evidence passed |
| M6 | Linter and corpus | Complete | Strict lint and one-time eight-deck corpus/reproducibility acceptance |
| M7 | Verification and close-out | In progress | Permanent and native acceptance passed; attended animation observation remains |

## Completed design and implementation

- The layout registry owns geometry, canonical short layout names, and legal slot names.
- Djot grammar is exact and whole-line based: `=== layout: <name>`, `@<slot>`, `<= appear`,
  `=> appear`, and `=> cascade appear`.
- Source is normalized into global title/subtitle blocks and named cells. Multiple H2 lines on a
  title slide form one subtitle region.
- One-line attributes precede and attach to the next element. A standalone component image is a
  complete image paragraph; mixed image paragraphs are source-located unsupported input.
- `$inline$` and `$$display$$` are intentional local math extensions after strict-Djot validation.
  Their editable native rendering remains future work.
- `multiple-choice` uses required `question` and `answer` slots. Its answer has implicit object
  reveal intent and permits one or two short flat paragraphs; package and bridge semantics passed,
  while attended Impress click playback remains unobserved.
- M5's bounded builder supports object APPEAR/FADE and paragraph APPEAR on click. Its four permanent
  structural tests and parser contract tests passed; the one-time LibreOffice bridge retained timing,
  editable objects, and the final PDF state.
- `blue overlay` is a recognized, explicit deferral rather than a silent no-op.
- The explicit Djot native-layout E2E passed through editable PPTX, LibreOffice ODP, and PDF across
  the registry, including gallery images and distinct editable multiple-choice shapes/final state.
- The native-only all-eight imported-corpus acceptance passed: 378 source slides, 336 visible slides,
  42 hidden slides, 150 reachable genuine source-image assets, 72 native normalization relations,
  113 review slides, and 185 image occurrences. No rendered source-slide or composite substitute
  remains.
- One-time native acceptance passed: strict lint covered 8 decks, 336 visible slides, and 185 image
  occurrences; `build_slides.sh genetics`, the Djot native-layout E2E, and eight sequential matching
  PPTX/ODP/PDF exports passed. Text and direct images remained editable, and Lecture 02e retained its
  native table.

## Remaining gates

1. Attend an Impress slideshow for the object and top-level-list reveal cases after granting the
   automation process Screen Recording and Accessibility, then record the click states. The
   headless bridge and ODP-derived PDF final state already passed.
2. Complete the remaining strict-Djot formatter/editor-rule suite selection before claiming full
   compatibility-suite coverage.
3. Move positioned-content region projection from `pptx_reader.py` into `slide_plan.py`, restoring
   the documented raw-reader-to-geometry-planner ownership boundary.
4. Define a non-Djot preservation design for imported presenter notes before claiming that imported
   note content survives normalization.

## Verification lanes

| Lane | Permanent status | What it proves |
| --- | --- | --- |
| Fast pytest | Permanent, offline | Parser, grammar, layout, suffix, and source diagnostics |
| Strict Jotdown and source lint | One-time/source acceptance | Raw-Djot syntax and project slide semantics |
| Native E2E | Passed explicit E2E | The real editable PPTX -> ODP -> PDF chain |
| Imported corpus review | Passed one-time acceptance | Regenerated corpus, provenance, asset integrity, and reproducibility |
| Native all-format output | Passed one-time acceptance | Editable PPTX, ODP, and PDF artifacts for every regenerated deck |
| LibreOffice bridge | Passed one-time check | Timing package semantics, editable ODP objects, and PDF final state |
| Impress slideshow | Attended check open | Click-by-click playback observation |

Do not treat a fast test, native lint, or render as a substitute for the attended timing checks.
