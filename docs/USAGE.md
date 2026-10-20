# Usage

Use repository-owned `.djot` source to produce editable ODP and ODP-derived PDF output.
Existing-presentation import is a one-time source migration workflow.

## Audit image shrinkage

Compare original ODP image coverage with the actual displayed area in a converted Djot deck:

```bash
source source_me.sh && python3 deck_tools.py image-audit \
    genetics/LECT06/lect06d-x_linked_genes_1.odp \
    genetics/LECT06/djot/lect06d-x_linked_genes_1.djot --loss-threshold 30
```

The JSON report includes original/converted percentages of slide area, percentage-point change,
relative area loss, and exact-white/transparent margin estimates. The default warning threshold is
30% relative loss. New imports also record this audit and print shrinkage warnings. Slide order
must match; replaced artwork and transformed frames are marked for manual review. The audit does
not trim images, modify slides, or select layouts. See
[image_area_regression_followup.md](active_plans/image_area_regression_followup.md) for limitations.

## Generate a YouTube slide

Generate a thumbnail, editable title, and full clickable YouTube watch URL:

```bash
source source_me.sh && python3 tools/make_youtube_slide.py \
    -v WXPBoFDqNVk -o genetics/LECT07/djot/youtube_chi_squared_test.djot
```

`-v` also accepts a YouTube watch URL or `youtu.be` URL. Place the output fragment beside
the master deck, then insert it at the desired slide boundary:

```djot
=== include: youtube_chi_squared_test.djot
```

The generator uses yt-dlp to fetch metadata and one thumbnail, never video or audio.
It validates the downloaded image and saves a PNG in `assets/youtube/` beside the fragment.
Downloads are staged under root `_temp/` and removed when the command finishes. Failed downloads
or image validation leave existing outputs intact. The generated slide uses the ordinary
`big-image` layout; titles are literal text and URLs omit tracking and playlist parameters.

Regeneration explicitly replaces the output fragment and its thumbnail, including any manual
edits to that fragment. Normal builds use saved files offline. Included fragments inherit the
master deck's theme and are omitted as standalone decks by folder builds.

## Refresh the podcast announcement

Preview the latest published Stump the Vibe Coder episode in a lecture's announcement deck:

```bash
source source_me.sh && python3 tools/refresh_podcast.py genetics/LECT07
```

Save it after reviewing the diff:

```bash
source source_me.sh && python3 tools/refresh_podcast.py genetics/LECT07 --write
```

Supply multiple lecture folders or specific `lect##a-*.djot` files to refresh several decks
in one run. Folder selection includes all matching announcement files beneath that folder;
use explicit filenames when it contains historical variants.

The helper reads the playlist's public YouTube Atom feed and chooses the newest publication
date among its recent entries. YouTube limits this feed to recent entries; it is not a complete
playlist archive. No API key or video download is needed. It downloads the full-size episode
thumbnail when available, otherwise the standard thumbnail, to `assets/stump_the_vibe_coder/`
beside each source. The `big-image` slide has the full episode title and visible clickable URL.

The slide goes immediately after the unique slide mentioning YouTube. Its `@notes` marker
identifies it for replacement on future runs; retain that marker when editing. Missing or
ambiguous insertion points stop the command before source writes. A refresh replaces the
previous podcast slide rather than adding another. Old thumbnail files are retained.

For historical announcements, select by each cover's lecture date:

```bash
source source_me.sh && python3 tools/refresh_podcast.py genetics biotech --by-lecture-date --write
```

This selects the newest episode published on or before the lecture date in America/Chicago,
including same-day publications. It never substitutes a later episode. If the recent RSS feed
has no eligible entry, the command stops before changing decks; an older archive is needed.
Folder discovery includes announcement filenames, not other `lect##a` course-introduction decks.
All required thumbnails are fetched and validated before source writes.

Build the selected decks normally afterward. Builds use saved local assets and never refresh
the episode automatically, so a past lecture retains the episode selected for it.

## Build native decks

Check every tracked standalone deck's slide 1 against the universal title format:

```bash
source source_me.sh && python3 -m pytest tests/test_slide_one.py
```

The check resolves includes, allows an unknown chapter to be omitted, and requires announcement
topics to be exactly "Announcements" with no chapter. Failures identify the source location and
write `report_slide_one.txt`: correct that cover using
[HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md#slide-1-title-slide), then rerun the check.
Canonical chapter assignments still require editorial verification against BPW.

The separate native export acceptance runner checks that cover text survives into the PDF:

```bash
source source_me.sh && python3 -m pytest tests/e2e/test_slide_one_pdf.py
```

On macOS agents must run LibreOffice conversions outside the sandbox. Extractable PDF text does
not replace checking selection and copying in the intended PDF viewer.

Write editable ODP for one source deck:

```bash
source source_me.sh && python3 deck_tools.py build \
	genetics/LECT01/djot/lect01b-genetic_disorders.djot -f odp
```

Select one output format for a deck or a recursively searched source folder:

```bash
source source_me.sh && python3 deck_tools.py build genetics --format pdf
```

Build every eligible source deck recursively below a folder as ODP and PDF:

```bash
./build_slides.sh genetics
```

Build only one lecture by targeting its lecture folder:

```bash
./build_slides.sh genetics/LECT04/
```

The same selector builds the Biotechnology lecture folder:

```bash
./build_slides.sh biotech/LECT04/
```

`deck_tools.py build` accepts `--format all`, `odp`, or `pdf`; `all` is the default. It recognizes
`.djot` source only, and folder discovery recursively selects only `.djot` files. Every deck compiles
once: `odp` writes the editable format, `pdf` writes native ODP plus its LibreOffice-derived PDF,
and `all` writes both. Outputs are written below `output/odp/` and `output/pdf/`.

Large decks can use a master `.djot` containing ordered `include: chapter.djot` lines.
Edit each chapter separately and build the master for one combined ODP/PDF. Folder builds and lint
select that master once, and errors retain the chapter filename and line. See
[chapter includes](DJOT_SLIDE_SYNTAX.md#chapter-files-and-includes) for paths and theme inheritance.

A slide marked `hidden: true` stays in the Djot source and is written with native hidden page-style
metadata in ODP; LibreOffice PDF export and classroom playback omit it. Capacity inspection and lint
include hidden slides and their assets. Remove that line or use `hidden: false` to show it. See
[DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md#hidden-slides).

Use `@notes` for instructor reminders. Notes end at the next named slot or slide directive and
become editable ODP speaker notes; the normal PDF export omits them. See
[DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md#instructor-notes) for an example.

Use `@replaceme` when an existing slide cannot be faithfully represented in Djot. It adds a large red
**REPLACE ME** watermark in ODP and PDF while retaining the editable slide underneath. New imports
add it wherever the import report records review reasons. Evaluate those findings during conversion:
keep it for representation failures and remove it after a faithful repair. It is not a general
editorial-review flag.
See [DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md#slides-needing-replacement).

The 16:10 master-slide theme comes from `genetics/xlect99-template_2023.otp`. ODP pages use that
native master and LibreOffice exports PDF from the themed ODP; no CSS or browser rendering is part
of the build.

## Inspect capacity before a build

Inspect one Djot deck or a recursively discovered folder without writing presentation artifacts:

```bash
source source_me.sh && python3 deck_tools.py capacity genetics/LECT04/
```

The command parses and compiles each selected deck once. It does not create ODP or PDF
files, and it does not invoke LibreOffice. Each concern line identifies the source path and line,
layout, slot, selected required size or serializer-safe minimum, readable floor, and the compiler
region that constrained the slide. Its final line groups concerns by cause. It exits `0` with no
output when every selected region stays at its floor and exits `1` after reporting any representable
recovery or physical-capacity boundary. A normal `build` still reports representable recovery from
the same compilation it exports.

The project-owned `multiple-choice` teaching layout retains its question, choices, and answer-popup
semantics. Its adaptive capacity selection evaluates supported choice geometries before reporting
only the final selected recovery or physical boundary.

Use `big-image` for one focal image with a short full-width caption at the bottom. The image and
caption remain separate editable native objects.

## Import existing slides

Import a trusted ODP into a new extended-Djot deck and adjacent asset directory:

```bash
source source_me.sh && python3 deck_tools.py import genetics/lecture.odp \
  --output genetics/lecture.djot
```

Save a legacy PPTX as ODP in LibreOffice, then import that ODP.

Djot is the only import target. Inspect resolved source-slide visibility before import:

```bash
source source_me.sh && python3 deck_tools.py visibility genetics/lecture.odp
```

The ODP importer reads a validated, bounded ODF package directly; it does not create a temporary
PPTX. It refuses an existing output target or its asset directory and keeps text, tables when their
native source metadata is available, ordinary images, and geometry-supported layouts editable.
Difficult spatial compositions become standard native source-order panels with a review reason.
Unsupported relationships remain visibly incomplete or fail with a source-located diagnostic; the
importer never renders the source slide or a composite region as substitute content.

Import retains hidden slides in source order with `hidden: true`, including their referenced
assets and import-report notes. Each report record includes `hidden`; hidden records have no
`visible_page`. Even an entirely hidden deck can be imported for later editing.

If final publication fails after the importer publishes its new asset leaf, it removes that exact
leaf and publishes no Djot source. Fix the reported failure, then rerun the command.

This is a one-time migration aid. Choose and maintain one canonical source after review; the
imported ODP does not become a second authoring source. See [PIPELINE.md](PIPELINE.md) for
ownership and [genetics/README.md](../genetics/README.md) for the regenerable corpus boundary.

## Validate Djot source

Run the fast, source-only structural check while authoring:

```bash
source source_me.sh && python3 deck_tools.py lint genetics/LECT04/
```

Before a Djot source-acceptance decision, run the separate strict native-parser gate followed by
the same semantic lint:

```bash
source source_me.sh && python3 deck_tools.py lint \
  --require-native --native-executable "$(command -v jotdown)" genetics/LECT04/
```

Fast lint is a permanent, offline behavior check. Strict Jotdown validation, real native export,
and visual/Office review are one-time acceptance evidence, not replacements for each other. The
LibreOffice Impress animation implementation, structural tests, native ODP package inspection,
headless ODP open/save preservation, and PDF final-state export have passed. Attended click playback
in Impress remains the sole open visual gate; do not infer it from a successful export. See
[ROADMAP.md](ROADMAP.md).

## Authoring boundaries

Use [DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md) for the normative source language, including
layouts, slots, content blocks, component images, tables, and reveals. Build and capacity commands
report source-located unsupported-content and fitting concerns.

## Known gaps

- [ ] Record attended LibreOffice Impress click playback before claiming native animation playback
  support.

## Local course links

Keep private Discord and Zoom URLs in ignored root `course_links.local.yaml`. Keys are course theme
names, matching `color-theme` in Djot:

```yaml
genetics:
  discord: https://example.org/genetics-invite
  office_hours: https://example.org/office-hours
  zoom_short: https://example.org/meeting
biotechnology:
  discord: https://example.org/biotech-invite
  office_hours: https://example.org/office-hours
  zoom_short: https://example.org/meeting
  zoom: https://example.org/biotech-meeting
```

Write `{{course_url:discord}}` wherever the visible, clickable URL belongs. Any key can be
used for additional private links. Public links, including all YouTube URLs, stay directly
in tracked Djot sources. Existing QR images remain alongside links; update their targets
when changing a URL. Included chapters use the deck's course theme. Missing configuration,
missing referenced keys, and invalid HTTPS URLs stop the build with a diagnostic. Decks
without references do not need this file. Copy the local YAML separately to a new checkout.
Generated ODP/PDF files contain the URLs and remain student distribution artifacts. Ignoring
the configuration does not erase URLs already committed in source or Git history.
