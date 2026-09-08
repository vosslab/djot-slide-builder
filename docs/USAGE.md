# Usage

Use repository-owned `.djot` source to produce editable PPTX, ODP, and ODP-derived PDF output.
Existing-presentation import is a one-time source migration workflow.

## Build native decks

Write editable PPTX for one source deck:

```bash
source source_me.sh && python3 deck_tools.py build \
	genetics/djot/lect01b-genetic_disorders.djot -f pptx
```

Write editable PPTX and ODP for one source deck:

```bash
source source_me.sh && python3 deck_tools.py build \
	genetics/djot/lect01b-genetic_disorders.djot -f odp
```

Select one output format for a deck or a recursively searched source folder:

```bash
source source_me.sh && python3 deck_tools.py build genetics --format pdf
source source_me.sh && python3 deck_tools.py build \
	genetics/djot/lect01b-genetic_disorders.djot --format pptx
```

Build every eligible source deck recursively below a folder as PPTX, ODP, and PDF:

```bash
./build_slides.sh genetics
```

`deck_tools.py build` accepts `--format all`, `odp`, `pdf`, or `pptx`; `all` is the default. It
recognizes `.djot` source only, and folder discovery recursively selects only `.djot` files. Every
build begins with editable PPTX: `pptx` stops there, `odp` adds editable ODP, and `pdf` adds the
ODP-derived PDF. Outputs are written below `output/pptx/`, `output/odp/`, and `output/pdf/`.

The 16:10 master-slide theme comes from `genetics/xlect99-template_2023.otp`. ODP pages use that
native master and PDF is exported from the themed ODP. PPTX mirrors the same gradient, centered
title, and hierarchical list rules as an optional interchange format; no CSS or browser rendering
is part of the build.

## Import existing slides

Import a trusted ODP into a new extended-Djot deck and adjacent asset directory:

```bash
source source_me.sh && python3 deck_tools.py import genetics/lecture.odp \
  --output genetics/lecture.djot
```

Import a trusted PPTX directly when it is the source evidence:

```bash
source source_me.sh && python3 deck_tools.py import genetics/lecture.pptx \
  --output genetics/lecture.djot
```

Djot is the only import target. Inspect resolved source-slide visibility before import:

```bash
source source_me.sh && python3 deck_tools.py visibility genetics/lecture.odp
```

The importer refuses an existing output target or its asset directory. It keeps text, tables when
their native source metadata is available, ordinary images, and geometry-supported layouts
editable. Difficult spatial compositions become standard native source-order panels with a review
reason. Unsupported relationships remain visibly incomplete or fail with a source-located
diagnostic; the importer never renders the source slide or a composite region as substitute content.

This is a one-time migration aid. Choose and maintain one canonical source after review; the
imported ODP or PPTX does not become a second authoring source. See [PIPELINE.md](PIPELINE.md) for ownership and
[genetics/djot/README.md](../genetics/djot/README.md) for the regenerable corpus boundary.

## Validate Djot source

Run the fast, source-only structural check while authoring:

```bash
source source_me.sh && python3 deck_tools.py lint genetics/djot
```

Before a Djot source-acceptance decision, run the separate strict native-parser gate followed by
the same semantic lint:

```bash
source source_me.sh && python3 deck_tools.py lint \
  --require-native --native-executable "$(command -v jotdown)" genetics/djot
```

Fast lint is a permanent, offline behavior check. Strict Jotdown validation, real native export,
and visual/Office review are one-time acceptance evidence, not replacements for each other. The
LibreOffice Impress animation implementation, structural tests, headless PPTX-to-ODP package
inspection, and PDF final-state export have passed. Attended click playback in Impress remains the
sole open visual gate; do not infer it from a successful export. See [ROADMAP.md](ROADMAP.md).

## Authoring boundaries

Begin each slide with `=== layout: <name>` and use `@<slot>` only where that
layout declares a slot. The layout registry is the authority for supported names and capacity;
source-located diagnostics identify unsupported or overflowing content instead of approximating it.

Keep source explanations, lists, links, and ordinary images as editable content. Use complete image
paragraphs for component images. Tables require real source metadata, and difficult legacy
compositions normalize into ordinary native layouts; raw HTML and raw XML are not authoring inputs.

## Known gaps

- [ ] Record attended LibreOffice Impress click playback before claiming native animation playback
  support.
