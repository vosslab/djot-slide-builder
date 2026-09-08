# File formats

This guide maps the presentation files accepted and produced by `deck_tools.py`.
It is for instructors who need to choose a canonical source, migrate one trusted deck, or
locate editable deliverables.

## Canonical source

- Author decks as repository-local `.djot` files. The build command accepts one file or searches a
  repository-local folder recursively for `.djot` files.
- Start every slide with `=== layout: <name>` and place content in the slots that layout declares.
  Standard Djot headings, paragraphs, lists, links, complete-paragraph images, and supported tables
  remain editable native content.
- Reference component images with paths relative to the `.djot` deck's directory. Paths must name
  existing local files and remain inside the repository. An imported deck keeps its generated media
  beside the source as `assets/<deck-name>/`; its `.djot` image references point directly into that
  deck-local namespace.
- Raw HTML and XML are not authoring inputs. See [USAGE.md](USAGE.md) for the supported authoring
  subset and [PIPELINE.md](PIPELINE.md) for layout and ownership details.

## Imported presentations

- `deck_tools.py import` accepts one trusted `.odp` or `.pptx` presentation and writes a new `.djot`
  source file. An `.odp` is normalized through a temporary PPTX only for import analysis.
- The importer does not overwrite an existing `.djot` target or `assets/<deck-name>/` directory.
  Choose a new destination when repeating an import.
- Text, supported source tables, ordinary images, and recognized layouts become editable Djot.
  A coupled visual that cannot be faithfully reconstructed becomes a bounded title-excluded PNG in
  the adjacent asset directory, never a full-slide raster.
- The asset directory includes `import_report.json`, which records source-slide visibility, selected
  layouts, asset inventory, and review reasons. After review, maintain the Djot deck as the one
  canonical source; imported presentations remain one-time migration evidence.

## Build products

| Requested format | File written | Meaning |
| --- | --- | --- |
| `pptx` | `output/pptx/<deck-name>.pptx` | Editable PowerPoint presentation generated from Djot. |
| `odp` | `output/pptx/<deck-name>.pptx`, then `output/odp/<deck-name>.odp` | Editable LibreOffice Impress presentation. |
| `pdf` | `output/pptx/<deck-name>.pptx`, `output/odp/<deck-name>.odp`, then `output/pdf/<deck-name>.pdf` | PDF derived from the editable ODP. |
| `all` | All three paths above | Default build sequence. |

The deck filename stem supplies each output filename. A PDF is a distribution and review artifact;
edit the PPTX or ODP rather than treating the PDF as source. Build and format-selection commands are
in [USAGE.md](USAGE.md); installation and macOS conversion prerequisites are in [INSTALL.md](INSTALL.md).
