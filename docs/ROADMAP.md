# Roadmap: extended-Djot native presentations

Status: M1-M7 implementation is complete, including one-time all-eight corpus acceptance,
regeneration reproducibility, native acceptance, and native ODP round-trip/PDF evidence.
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
| M5 | Animation backend | Implementation complete; attended gate open | Bounded ODF/SMIL writer; structural and headless ODP/PDF evidence passed |
| M6 | Linter and corpus | Complete | Strict lint and one-time eight-deck corpus/reproducibility acceptance |
| M7 | Verification and close-out | Complete | Permanent and native acceptance passed; attended animation observation remains separate |

## Completed design and implementation

- [DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md) defines the completed source language, layout,
  content, and reveal contract. The layout registry implements its canonical names and slots.
- M5's bounded adapters support object APPEAR/FADE and paragraph APPEAR on click. Permanent
  structural tests and parser contract tests passed; a LibreOffice ODP round trip retained native
  layouts and editable objects, and PDF export retained the final state.
- The current native-layout evidence covers the 14-layout catalog: twelve LibreOffice identities
  plus the project-owned `multiple-choice` and `gallery` layouts. It establishes editable native
  ODP, a LibreOffice ODP open/save round trip, and ODP-derived PDF; LibreOffice normalizes an empty
  blank page's saved reference to its title-slide definition while preserving the empty page.
- The native-only all-eight imported-corpus acceptance passed: 378 source slides, 336 visible slides,
  42 hidden slides, 150 reachable genuine source-image assets, 72 native normalization relations,
  113 review slides, and 185 image occurrences. No rendered source-slide or composite substitute
  remains.
- One-time native acceptance passed: strict lint covered 8 decks, 336 visible slides, and 185 image
  occurrences; `build_slides.sh genetics`, the Djot native-layout E2E, and eight sequential matching
  ODP/PDF exports passed. Text and direct images remained editable, and Lecture 02e retained its
  native table.

## Remaining gates

1. Attend an Impress slideshow for the object and top-level-list reveal cases after granting the
   automation process Screen Recording and Accessibility, then record the click states. The
   headless ODP round trip and ODP-derived PDF final state already passed.
2. Complete the remaining strict-Djot formatter/editor-rule suite selection before claiming full
   compatibility-suite coverage.
3. Decide whether presenter notes need authored Djot syntax before promoting their losslessly
   retained import-report text into rebuilt native note objects.

## Verification lanes

| Lane | Permanent status | What it proves |
| --- | --- | --- |
| Fast pytest | Permanent, offline | Parser, grammar, layout, suffix, and source diagnostics |
| Strict Jotdown and source lint | One-time/source acceptance | Raw-Djot syntax and project slide semantics |
| Native E2E | Passed explicit E2E | Editable native ODP, ODP round trip, and ODP-derived PDF |
| Imported corpus review | Passed one-time acceptance | Regenerated corpus, provenance, asset integrity, and reproducibility |
| Native all-format output | Passed one-time acceptance | Editable ODP and PDF artifacts for every regenerated deck |
| LibreOffice ODP round trip | Passed explicit E2E | Nonblank built-in identities, editable ODP objects, and PDF final state |
| Impress slideshow | Attended check open | Click-by-click playback observation |

Use the attended Impress check to establish click-by-click timing; fast tests, native lint, and
renders establish their separate evidence lanes.
