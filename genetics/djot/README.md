# Extended-Djot genetics decks

This folder contains the canonical extended-Djot presentation source for the native pipeline. Each
file was imported from the authoritative ODP with `deck_tools.py import`, which reads native ODP
directly to recover text, images, reading order, and source-hidden slide state. The corpus preserves
that source evidence while using the shared native theme and layout system.

[DJOT_SLIDE_SYNTAX.md](../../docs/DJOT_SLIDE_SYNTAX.md) is the normative authoring reference for
these decks. This README records corpus provenance, inventory, and validation evidence.

| Deck | Source | Visible | Hidden | Images | Normalized | Reviews |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `lect01a-course_intro.djot` | 40 | 31 | 9 | 18 | 6 | 11 |
| `lect01b-genetic_disorders.djot` | 23 | 23 | 0 | 6 | 0 | 5 |
| `lect02a-2025_announcements.djot` | 75 | 43 | 32 | 15 | 4 | 10 |
| `lect02b-genes_dogma.djot` | 49 | 49 | 0 | 22 | 16 | 19 |
| `lect02c-genome_sizes.djot` | 59 | 59 | 0 | 32 | 2 | 10 |
| `lect02d-dna_structure_overview.djot` | 43 | 43 | 0 | 19 | 4 | 6 |
| `lect02e-restriction_enzymes.djot` | 62 | 62 | 0 | 18 | 25 | 35 |
| `lect02f-dna_electrophoresis.djot` | 27 | 26 | 1 | 20 | 15 | 17 |
| **Total** | **378** | **336** | **42** | **150** | **72** | **113** |

`assets/<deck>/import_report.json` retains the import inventory, including each visible source-slide
number, selected layout, omitted-note count, and extraction-review reason. Image placement count can
exceed the distinct-asset count because a figure may recur across teaching steps.

## Corpus acceptance evidence

The 2026-09-07 native-only acceptance sweep converted and validated all eight authoritative ODP
decks: 378 source slides, 336 visible slides, 42 hidden slides, 150 reachable genuine source-image
assets, 72 native normalization relations, 113 review slides, and 185 image occurrences. Every Djot
image reference resolved to a file; no rendered slide or composite-region substitute remains.

The one-time native acceptance also passed: strict lint covered 8 decks and 336 visible slides;
`build_slides.sh genetics` passed; and the Djot native-layout E2E
passed. Sequential `--format all` exports for every deck retained matching ODP and PDF page
counts (31, 23, 43, 49, 59, 43, 62, and 26), editable text and direct images, and the native table
in Lecture 02e. This does not establish attended animation acceptance.

## Validation boundary

Run the fast local structural check with:

```bash
source source_me.sh && python3 deck_tools.py lint genetics/djot
```

It validates the full local slide contract and image references without rendering a slide. It is
source-only: it does not establish native geometry, animation timing, or visual quality. Jotdown
0.10.0 is the pinned native parser and runs before semantic lint:

```bash
source source_me.sh && python3 deck_tools.py lint \
  --require-native --native-executable "$(command -v jotdown)" genetics/djot
```

Jotdown is the raw-Djot parser-validation lane; it complements rather than replaces a formatter,
editor rule, or standalone linter. The remaining compatibility-suite lanes still need explicit
decisions before this corpus can claim to pass every applicable Djot tool. See the
[language exploration record](../../docs/active_plans/decisions/djot_slide_extension_exploration.md)
for that governing requirement and the upstream Djot and Jotdown sources.

Native acceptance is one-time evidence, not a permanent test. The permanent suite remains separately
offline, fast, and deterministic. M5 structural tests are permanent; its headless LibreOffice
bridge/PDF evidence passed once, while attended Impress click playback remains open in
[wp_a1_animation_fidelity.md](../../docs/active_plans/reports/wp_a1_animation_fidelity.md).
