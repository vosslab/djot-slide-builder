# Usage

Use extended-Djot source to create editable ODP presentations and ODP-derived PDFs. The primary
entry point is `deck_tools.py`; selected utilities run as `slide_lib` modules.

## Quick start

Build one lecture deck as editable ODP:

```bash
source source_me.sh && python3 deck_tools.py build \
  genetics/LECT01/djot/lect01b-genetic_disorders.djot --format odp
```

Build all eligible Djot decks below a lecture folder as ODP and PDF:

```bash
./build_slides.sh genetics/LECT04
```

Outputs are written under `output/odp/` and `output/pdf/`. Open the ODP in LibreOffice Impress
to edit it. Run the build outside an agent sandbox because PDF output invokes LibreOffice.

## Author an SVG figure

Use the [toolkit catalogue](SVG_TOOLKIT.md), [cookbook](SVG_TOOLKIT_COOKBOOK.md), and
[gallery](slide-specs/illustration_examples/svg_toolkit/index.webp) to choose and compose parts.
For SVG work, use the repository bootstrap and a local plot cache:

```bash
source source_me.sh && MPLCONFIGDIR="$PWD/_temp/mplconfig" python3 -m \
  svg_tools.examples.allele_frequencies _temp/allele_frequencies.svg
```

The cookbook explains adding the SVG to a native slide. Check example output paths before running
them: some recipes default to lecture assets.

For source-addressed chromosome figures, see [CHROMOSOME_ENGINE.md](CHROMOSOME_ENGINE.md).

## Core commands

```bash
# Validate extended-Djot structure, links, and local assets without building.
source source_me.sh && python3 deck_tools.py lint genetics/LECT04

# Require the recorded strict Jotdown source gate as well.
source source_me.sh && python3 deck_tools.py lint --require-native \
  --native-executable "$(command -v jotdown)" genetics/LECT04

# Inspect fitting concerns without writing ODP or PDF artifacts.
source source_me.sh && python3 deck_tools.py capacity genetics/LECT04

# Report title wrapping and short final lines as JSON.
source source_me.sh && python3 deck_tools.py audit genetics/LECT04
```

`lint` is the project-specific Djot checker: it validates Djot assets and hyperlinks from the
working tree, including untracked local images. The repository Markdown checker separately scans
only `.md` documentation links; it does not interpret Djot source.

Use `build --format all`, `build --format odp`, or `build --format pdf`; `all` is the default.
Folder selection is recursive and includes `.djot` source only. In a copied checkout without Git
metadata, run commands from the top-level folder containing `build_slides.sh` and `slide_lib/`.

Each build adds a subdued rendering timestamp to slide 1 and the last visible `theend` slide,
when present. Both show the same local date, time with seconds, and time-zone abbreviation.
The small IBM Plex Sans Condensed text remains selectable in ODP/PDF and updates when you rebuild the source.
It is generated automatically; no `@caption` or date text needs to be added to the source.

### Count images and text-only slides

```bash
source source_me.sh && python3 deck_tools.py stats biotech/LECT12/djot/lect12c-set_7_bioethics_in_biotechnology.djot
```

Give `stats` a single Djot deck or its main include file. Add `--json` for machine-readable
counts and percentages. The command reads the source, follows chapter includes and reports
the number of hidden slides. All percentages use visible slides in the named row.

- **Panel layouts** combines `one-panel` with all `*-panels` layouts. Moving a slide from
  `one-panel` to `two-panels` to add a figure keeps the total number of panel slides the same.
- **Without section headings** omits `section`, `subsection`, and `subsubsection`.
- **Content slides** also omits the opening title, closer, and blank slides.
  **Content without bookends** also omits the `bookend` layout often used for objectives and questions.
- **Dedicated image layouts** groups `big-image`, `gallery`, `image-comparison`, and `movie-panel`.
  The layout table also shows image use in ordinary layouts such as `two-panels`.

An image, a native table, or a display equation counts as a visual. A slide with several
such elements counts once under **Any visual**. **Image placements** counts each authored
image reference, including repeated uses. **Text only** includes inline math. **No visual**
also includes blank slides. Theme artwork and speaker notes do not contribute to coverage.
Use `lint` to check that the referenced image files exist.

## Build the table demonstration

The maintained [../exemplars/table_styles.djot](../exemplars/table_styles.djot) demonstrates the
ordinary default, all seven named treatments, scientific notation, local overrides, merges,
matrices, and related question/answer workspaces:

```bash
source source_me.sh && python3 deck_tools.py build exemplars/table_styles.djot --format all
```

Open `output/odp/table_styles.odp` for native table editing and `output/pdf/table_styles.pdf` for
the distribution copy. Run outside the sandbox because PDF export invokes LibreOffice. See
[slide-specs/TABLE_AUTHORING_GUIDE.md](slide-specs/TABLE_AUTHORING_GUIDE.md) for authoring recipes.

## Import an existing deck

```bash
# Report resolved source-slide visibility first.
source source_me.sh && python3 deck_tools.py visibility genetics/lecture.odp

# Create Djot source and an adjacent asset folder from one trusted ODP.
source source_me.sh && python3 deck_tools.py import genetics/lecture.odp \
  --output genetics/lecture.djot
```

The importer accepts trusted ODP only. Save a legacy PPTX as ODP in LibreOffice first. It refuses
an existing output target or asset directory, so use a new destination. Imported Djot becomes the
canonical editable source after review; the original presentation is migration evidence, not a
second authoring source.

## Audit image shrinkage

Compare artwork in a source ODP and its corresponding Djot conversion:

```bash
source source_me.sh && python3 deck_tools.py image-audit \
  SOURCE.odp CONVERTED.djot --loss-threshold 30
```

Replace the placeholders with existing files. The audit requires matching authored slide count
and order; it compares identical artwork's displayed share of the slide and reports relative
area loss. Cropped, reconstructed, or transformed figures need manual correspondence review.
For a reorganized annual-source merge, use the topic map and the method in
[TALKING_POINT_DECK_RECIPE.md](TALKING_POINT_DECK_RECIPE.md#compare-figure-size).

## Practical helpers

Generate a Djot fragment and saved thumbnail for one YouTube video:

```bash
source source_me.sh && python3 -m slide_lib.make_youtube_slide \
  --video WXPBoFDqNVk --output genetics/LECT07/djot/youtube_chi_squared_test.djot
```

Insert the fragment in its master deck with `=== include: youtube_chi_squared_test.djot`. The
tool fetches only metadata and a thumbnail; ordinary builds use the saved image offline.

Preview a weather or podcast announcement update. Add `--write` only after reviewing the printed
diff; preview is the default.

```bash
source source_me.sh && python3 -m slide_lib.refresh_weather genetics/LECT09
source source_me.sh && python3 -m slide_lib.refresh_podcast genetics/LECT07 --by-lecture-date
```

Both module commands accept lecture folders or `lect##a` Djot files. The weather helper fetches the
current Chicago NWS PNG graphics and saves only quality-90 WebP snapshots at their original dimensions.
It retains complete captions. The podcast helper skips episodes marked special and uses publication time
to select the latest regular episode. Use `--by-lecture-date` to limit selection to episodes published
by each lecture date.

Podcast preview prints the selected shared fragment and master references. With `--write`, the helper
downloads and validates the thumbnail, writes
`shared/assets/stump_the_vibe_coder/<YouTube ID>.webp`, and creates
`shared/stump_the_vibe_coder/<YouTube ID>.djot` only when it is absent. It preserves an existing
curated fragment, then updates each selected master to use the explicit
`repo:shared/stump_the_vibe_coder/<YouTube ID>.djot` include. A legacy inlined managed podcast slide
can be converted during that update. Each master pins its historical episode choice. For Episode 39,
use its explicitly labeled `Project:` destination, Red Dead Cell Counter, rather than Plaque Attack.

Rebuild the saved two-gene tetrad working-table SVGs from their adjacent data and ascus drawings:

```bash
source source_me.sh && python3 -m slide_lib.render_tetrad_tables \
  genetics/LECT09/djot/assets/lect09c-tetrad_worked_examples_bpw/problem_data.json
```

The utility writes four SVGs beside its input. It does not rebuild the separate saved three-gene
homework snapshots.

## More authoring guidance

Use the authoritative slide specifications for
[slide-specs/COLOR_GUIDE.md](slide-specs/COLOR_GUIDE.md),
[slide-specs/VOICE_GUIDE.md](slide-specs/VOICE_GUIDE.md), and
[slide-specs/PEDAGOGY_GUIDE.md](slide-specs/PEDAGOGY_GUIDE.md). The
[slide-specs/AUTHORING_GUIDE.md](slide-specs/AUTHORING_GUIDE.md) overview retains layout,
typography, and source-evidence conventions.

Use [slide-specs/DJOT_SLIDE_SYNTAX.md](slide-specs/DJOT_SLIDE_SYNTAX.md) for layouts, slots,
tables, `@speaker-notes`, and chapter includes. Record deck provenance and design decisions in
[slide development notes](slide-specs/AUTHORING_GUIDE.md#slide-development-notes).
Use [SLIDE_CONVERSION_CHECKLIST.md](SLIDE_CONVERSION_CHECKLIST.md) while
converting a lecture and [slide-specs/ANNOUNCEMENT_DECK_GUIDE.md](slide-specs/ANNOUNCEMENT_DECK_GUIDE.md) for weekly
announcement decks. Use [TALKING_POINT_DECK_RECIPE.md](TALKING_POINT_DECK_RECIPE.md) to merge
annual student sources with expanded instructor material into an ordered study deck.
Put private course URLs in the ignored
[`course_links.local.yaml` setup](INSTALL.md#local-course-links), rather than tracked source.

## Known gaps

- [ ] Record attended LibreOffice Impress click-playback evidence before claiming native animation
  playback support.
