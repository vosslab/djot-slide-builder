# djot-slides

Open-source Python toolchain for building complete, lecture-ready presentations from concise, human-editable 
Djot. Supports structured teaching layouts, text, nested lists, images, tables, and links; imports existing 
ODP/PPTX decks; and exports editable PPTX and LibreOffice ODP files plus PDF.

Build editable classroom presentations from concise Djot source, preserving native text, lists,
links, images, and tables through PPTX, ODP, and PDF.

## One source, native outputs

```text
canonical extended-Djot source
  -> repository-owned Djot parser
  -> typed native slide-object model
  -> slide_lib.layouts native layout builders
  -> python-pptx editable PPTX
  -> LibreOffice editable ODP
  -> LibreOffice PDF from that ODP
```

Every generated slide uses native editable objects. The repository owns the parser, layout
registry, and exporters; normal builds do not need Node, a browser, or a full-slide raster stage.

## Quick start

Install the dependencies, then build one deck:

```bash
brew bundle
source source_me.sh && python3 -m pip install -r pip_requirements.txt
source source_me.sh && python3 deck_tools.py build \
  genetics/djot/lect01b-genetic_disorders.djot -f odp
```

Build PPTX, ODP, and PDF for every Djot deck below `genetics/`:

```bash
./build_slides.sh genetics
```

## Import an existing presentation

Import a trusted instructor-owned ODP or PPTX as a new Djot deck:

```bash
source source_me.sh && python3 deck_tools.py import genetics/lecture.odp \
  -o genetics/djot/lecture.djot
```

The importer preserves raw source facts, uses geometry to choose semantic layouts, and emits Djot
plus validated local assets. Review the result once, then maintain the Djot deck as the canonical
source.

## Documentation

- [docs/INSTALL.md](docs/INSTALL.md) - dependencies and the trusted-import boundary.
- [docs/USAGE.md](docs/USAGE.md) - build, import, lint, and authoring commands.
- [docs/PIPELINE.md](docs/PIPELINE.md) - component ownership and artifact flow.
- [genetics/djot/README.md](genetics/djot/README.md) - syntax examples and corpus evidence.
- [docs/DESIGN_DECISIONS.md](docs/DESIGN_DECISIONS.md) - settled architecture decisions.
- [docs/HUMAN_GUIDANCE.md](docs/HUMAN_GUIDANCE.md) - durable instructor requirements.
- [docs/ROADMAP.md](docs/ROADMAP.md) - current milestones and remaining acceptance work.
- [docs/TODO.md](docs/TODO.md) - remaining language and validation tasks.

## License

Source code: [LICENSE.mit](LICENSE.mit).
