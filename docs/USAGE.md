# Usage

Use repository-owned `.djot` source to produce editable ODP and ODP-derived PDF output.
Existing-presentation import is a one-time source migration workflow.

## Build native decks

Write editable ODP for one source deck:

```bash
source source_me.sh && python3 deck_tools.py build \
	genetics/djot/lect01b-genetic_disorders.djot -f odp
```

Select one output format for a deck or a recursively searched source folder:

```bash
source source_me.sh && python3 deck_tools.py build genetics --format pdf
```

Build every eligible source deck recursively below a folder as ODP and PDF:

```bash
./build_slides.sh genetics
```

`deck_tools.py build` accepts `--format all`, `odp`, or `pdf`; `all` is the default. It recognizes
`.djot` source only, and folder discovery recursively selects only `.djot` files. Every deck compiles
once: `odp` writes the editable format, `pdf` writes native ODP plus its LibreOffice-derived PDF,
and `all` writes both. Outputs are written below `output/odp/` and `output/pdf/`.

The 16:10 master-slide theme comes from `genetics/xlect99-template_2023.otp`. ODP pages use that
native master and LibreOffice exports PDF from the themed ODP; no CSS or browser rendering is part
of the build.

## Inspect capacity before a build

Inspect one Djot deck or a recursively discovered folder without writing presentation artifacts:

```bash
source source_me.sh && python3 deck_tools.py capacity genetics/djot
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

If final publication fails after the importer publishes its new asset leaf, it removes that exact
leaf and publishes no Djot source. Fix the reported failure, then rerun the command.

This is a one-time migration aid. Choose and maintain one canonical source after review; the
imported ODP does not become a second authoring source. See [PIPELINE.md](PIPELINE.md) for
ownership and [genetics/djot/README.md](../genetics/djot/README.md) for the regenerable corpus
boundary.

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
