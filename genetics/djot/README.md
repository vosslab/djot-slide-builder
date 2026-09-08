# Extended-Djot genetics decks

This folder contains the canonical extended-Djot presentation source for the native pipeline. Each
file was imported from the authoritative ODP with `deck_tools.py import`, which
normalizes through a temporary PPTX only to recover text, images, reading order, and source-hidden
slide state.

The generated source uses exact `=== layout: <name>` and `@<slot>` lines, standard Djot headings and
lists, and complete-paragraph `![alt](path)` component images. Legal layout and slot names derive
from `slide_lib.layouts`; current corpus examples include the canonical short names. It deliberately
omits presenter notes and does not infer animation or visual styling from an imported file. Short DNA
sequences use inline verbatim; ordinary `&prime;` text projects to U+2032 PRIME in the native model.

Use `#` and `##` only where the chosen layout permits global title/subtitle content. A title slide
may contain several H2 lines, which become one subtitle region. One-line Djot attributes precede the
element they describe. `$inline$` and `$$display$$` are local math extensions, but editable native
math is not implemented yet. `<= blue overlay` is recognized and reports "not yet supported".

`multiple-choice` requires exactly `@question` and `@answer`. The question contains a visible choice
list; the answer is one or two short flat paragraphs. The parser records implicit answer reveal
intent. The bounded OOXML builder and one-time LibreOffice bridge preserve it through editable ODP
and the PDF final state; attended Impress first-advance playback remains unobserved.

| Deck | Source | Visible | Hidden | Assets | Regions | Reviews |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `lect01a-course_intro.djot` | 40 | 31 | 9 | 18 | 6 | 11 |
| `lect01b-genetic_disorders.djot` | 23 | 23 | 0 | 6 | 0 | 8 |
| `lect02a-2025_announcements.djot` | 75 | 43 | 32 | 14 | 4 | 10 |
| `lect02b-genes_dogma.djot` | 49 | 49 | 0 | 31 | 16 | 18 |
| `lect02c-genome_sizes.djot` | 59 | 59 | 0 | 31 | 2 | 8 |
| `lect02d-dna_structure_overview.djot` | 43 | 43 | 0 | 20 | 4 | 4 |
| `lect02e-restriction_enzymes.djot` | 62 | 62 | 0 | 27 | 25 | 26 |
| `lect02f-dna_electrophoresis.djot` | 27 | 26 | 1 | 20 | 15 | 11 |
| **Total** | **378** | **336** | **42** | **167** | **72** | **96** |

`assets/<deck>/import_report.json` retains the import inventory, including each visible source-slide
number, selected layout, omitted-note count, and extraction-review reason. Image placement count can
exceed the distinct-asset count because a figure may recur across teaching steps.

## Corpus acceptance evidence

The 2026-09-07 one-time acceptance sweep converted and validated all eight authoritative ODP
decks: 378 source slides, 336 visible slides, 42 hidden slides, 167 reachable assets, 72 bounded
source regions, 96 review slides, and 186 image occurrences. Every Djot image reference resolved to
a file; there were no missing or extra assets, symlinks, or exact-full source regions.

A second private regeneration independently reproduced the Djot, import-report, and asset corpus.
The one-time native acceptance also passed: strict lint covered 8 decks, 336 visible
slides, and 186 image occurrences; `build_slides.sh genetics` passed; and the Djot native-layout E2E
passed. Sequential `--format all` exports for every deck retained matching PPTX, ODP, and PDF page
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
