# Extended-Djot genetics decks

This folder contains the canonical extended-Djot presentation source for the native pipeline,
organized by lecture. Each source was imported from the authoritative ODP with `deck_tools.py
import`, which reads native ODP directly to recover text, images, reading order, and source-hidden
slide state. The corpus preserves that source evidence while using the shared native theme and
layout system.

[DJOT_SLIDE_SYNTAX.md](../docs/DJOT_SLIDE_SYNTAX.md) is the normative authoring reference for
these decks. This README records corpus provenance, inventory, and validation evidence.

Each lecture owns both sides of its migration boundary:

```text
genetics/LECT04/djot/   canonical Djot sources and adjacent assets
genetics/LECT04/old/    original ODP/PDF/ODS evidence
```

Build one lecture, including only its recursively discovered Djot sources, with:

```bash
./build_slides.sh genetics/LECT04/
```

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
| `lect03a-2026_announcements.djot` | 66 | 40 | 26 | 15 | 3 | 15 |
| `lect03b-blood_hla_typing.djot` | 44 | 44 | 0 | 16 | 11 | 27 |
| `lect03c-fingerprinting.djot` | 51 | 51 | 0 | 23 | 5 | 26 |
| `lect03d-genotyping_1.djot` | 51 | 51 | 0 | 46 | 4 | 19 |
| `lect03e-genotyping_2.djot` | 28 | 28 | 0 | 15 | 4 | 11 |
| `lect03f-whole_genome_analysis.djot` | 24 | 24 | 0 | 9 | 0 | 9 |
| `lect03g-chap2_challenges.djot` | 11 | 11 | 0 | 2 | 7 | 8 |
| `lect04a-2026_announcements.djot` | 64 | 36 | 28 | 14 | 3 | 33 |
| `lect04b-mendel_history.djot` | 29 | 29 | 0 | 19 | 2 | 7 |
| `lect04c-two_principles.djot` | 36 | 35 | 1 | 6 | 6 | 23 |
| `lect04d-cross_experiments.djot` | 19 | 19 | 0 | 10 | 4 | 8 |
| `lect04e-segregation.djot` | 12 | 12 | 0 | 3 | 3 | 7 |
| `lect04f-punnett_squares.djot` | 47 | 47 | 0 | 6 | 31 | 38 |
| `lect04g-indep_assort.djot` | 53 | 52 | 1 | 10 | 9 | 31 |
| `lect04h-indep_assort_problems.djot` | 37 | 37 | 0 | 5 | 0 | 8 |
| `lect04i-big_crossover_problem.djot` | 22 | 22 | 0 | 0 | 0 | 18 |
| **Total** | **972** | **874** | **98** | **349** | **164** | **401** |

`LECT##/djot/assets/<deck>/import_report.json` retains the import inventory, including each visible
source-slide number, selected layout, omitted-note count, and extraction-review reason. Image
placement count can exceed the distinct-asset count because a figure may recur across teaching
steps.

The inventory records the initial import review counts, before manual teaching-layout repairs.
Lecture 03 uses the 2026 announcements; the older 2025 announcements remain only in the legacy
input folder. Lecture 04A combines current 2026 announcement guidance with recurring Lecture 04
material from the 2025 deck; the 2025 deck was used as comparison evidence and is not a canonical
source. Hidden source slides remain in Djot with `hidden: true`. The earlier Lecture 01/02 imports
still record their omitted hidden slides in their reports; they have not been reimported. See
[LECT03_REVIEW.md](LECT03/djot/LECT03_REVIEW.md) and
[LECT04_REVIEW.md](LECT04/djot/LECT04_REVIEW.md) for the conversion, repairs, and verification
boundaries.

## Lecture 04 acceptance evidence

The 2026-09-21 conversion covered nine authoritative Lecture 04 ODP decks: 319 authored slides,
289 visible classroom slides, 30 retained hidden slides, 73 distinct source-image assets, and 92
image references. Strict native lint covered all nine sources. Sequential `--format all` builds
produced matching editable ODP and PDF page counts of 36, 29, 35, 19, 12, 47, 52, 37, and 22.
The source decks and their adjacent assets are the canonical Lecture 04 authoring set; generated
ODP/PDF files remain delivery artifacts under `output/`.

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

Run the fast local structural check for the whole reorganized corpus with:

```bash
source source_me.sh && python3 deck_tools.py lint genetics
```

Use `genetics/LECT04/` instead of `genetics` to lint only Lecture 04.

It validates the full local slide contract and image references without rendering a slide. It is
source-only: it does not establish native geometry, animation timing, or visual quality. Jotdown
0.10.0 is the pinned native parser and runs before semantic lint:

```bash
source source_me.sh && python3 deck_tools.py lint \
  --require-native --native-executable "$(command -v jotdown)" genetics
```

Jotdown is the raw-Djot parser-validation lane; it complements rather than replaces a formatter,
editor rule, or standalone linter. The remaining compatibility-suite lanes still need explicit
decisions before this corpus can claim to pass every applicable Djot tool. See the
[language exploration record](../docs/active_plans/decisions/djot_slide_extension_exploration.md)
for that governing requirement and the upstream Djot and Jotdown sources.

Native acceptance is one-time evidence, not a permanent test. The permanent suite remains separately
offline, fast, and deterministic. M5 structural tests are permanent; its headless LibreOffice
bridge/PDF evidence passed once, while attended Impress click playback remains open in
[wp_a1_animation_fidelity.md](../docs/active_plans/reports/wp_a1_animation_fidelity.md).
