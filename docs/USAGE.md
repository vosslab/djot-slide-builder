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

Both module commands accept lecture folders or `lect##a` Djot files. They fetch and validate required
images before a `--write` update. The weather helper captures the current Chicago NWS story; the
podcast helper uses the public feed and can select the latest episode on or before each lecture
date with `--by-lecture-date`.

Rebuild the saved two-gene tetrad working-table SVGs from their adjacent data and ascus drawings:

```bash
source source_me.sh && python3 -m slide_lib.render_tetrad_tables \
  genetics/LECT09/djot/assets/lect09c-tetrad_worked_examples_bpw/problem_data.json
```

The utility writes four SVGs beside its input. It does not rebuild the separate saved three-gene
homework snapshots.

## More authoring guidance

Use [DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md) for layouts, slots, tables, speaker notes, and
chapter includes. Use [SLIDE_CONVERSION_CHECKLIST.md](SLIDE_CONVERSION_CHECKLIST.md) while
converting a lecture and [ANNOUNCEMENT_DECK_GUIDE.md](ANNOUNCEMENT_DECK_GUIDE.md) for weekly
announcement decks. Put private course URLs in the ignored
[`course_links.local.yaml` setup](INSTALL.md#local-course-links), rather than tracked source.

## Known gaps

- [ ] Record attended LibreOffice Impress click-playback evidence before claiming native animation
  playback support.
