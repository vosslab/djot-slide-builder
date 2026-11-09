# File formats

This guide maps the presentation files accepted and produced by `deck_tools.py`.
It is for instructors who need to choose a canonical source, migrate one trusted deck, or
locate editable deliverables.

## Canonical source

- Author decks as repository-local `.djot` files. The build command accepts one file or searches a
  repository-local folder recursively for `.djot` files.
- Reference component images relative to the master deck's directory, including images in included
  chapters. Use `repo:` for assets explicitly relative to the repository root. Paths must name
  existing local files and remain inside the allowed source tree. An imported deck keeps its generated media
  beside the source as `assets/<deck-name>/`; its `.djot` image references point directly into that
  deck-local namespace.
- [slide-specs/DJOT_SLIDE_SYNTAX.md](slide-specs/DJOT_SLIDE_SYNTAX.md) defines the source language and editable native
  destinations. [USAGE.md](USAGE.md) provides build and import commands.
- Write Djot source as ASCII, using character references such as `&alpha;` or `&#8242;` for
  non-ASCII visible text. Code and math retain their context-specific notation.
- Keep copyrighted teaching images outside Git. Djot lint checks their local existence and safety;
  the Markdown gate separately checks GitHub-browsable `.md` documentation links.

## Imported presentations

- `deck_tools.py import` accepts one trusted `.odp` presentation and writes a new `.djot` source
  file. Save a legacy PPTX as ODP in LibreOffice before importing it.
- The importer does not overwrite an existing `.djot` target or `assets/<deck-name>/` directory.
  Choose a new destination when repeating an import.
- Text, supported source tables, ordinary images, and recognized layouts become editable Djot.
  Difficult spatial compositions normalize into standard native source-order panels. A limitation
  remains visible in the generated source or import report; no rendered slide or composite source
  region is inserted as substitute content.
- The asset directory includes `import_report.json`, which records source-slide visibility, selected
  layouts, asset inventory, review reasons, presenter-note text, and lossless text/link/geometry
  facts for normalized spatial regions. After review, maintain the Djot deck as the one canonical
  source; imported presentations remain one-time migration evidence.

## Build products

All build products use the 16:10 theme from `genetics/xlect99-template_2023.otp`. The ODP contains
that template's native master page and supplies the PDF. CSS and browser rendering are not involved.

| Requested format | File written | Meaning |
| --- | --- | --- |
| `odp` | `output/odp/<deck-name>.odp` | Native editable LibreOffice Impress presentation using the OTP master. |
| `pdf` | `output/odp/<deck-name>.odp`, then `output/pdf/<deck-name>.pdf` | PDF derived from the native editable ODP. |
| `all` | Both output paths | Native ODP followed by its LibreOffice-derived PDF. |

The deck filename stem supplies each output filename. A PDF is a distribution and review artifact;
revise canonical Djot for reproducible changes, or edit the ODP for classroom use. Build commands are
in [USAGE.md](USAGE.md); installation and macOS conversion prerequisites are in [INSTALL.md](INSTALL.md).

## Local configuration and notes

- `course_links.local.yaml` stores private course-to-URL mappings and remains ignored. Djot uses
  `{{course_url:key}}` tokens; runtime builds require valid configured HTTPS destinations.
- Source-only lint recognizes course URL tokens without requiring the private configuration.
  It does not establish that those destinations are configured or reachable.
- An authored `@notes` section exports as native ODP speaker notes. Notes remain separate from
  projected slide content; their syntax is defined in [slide-specs/DJOT_SLIDE_SYNTAX.md](slide-specs/DJOT_SLIDE_SYNTAX.md).

## OpenDocument package boundary

ODP and OTP inputs are ZIP-based OpenDocument packages. Validation requires the correct
`mimetype` content, required XML members, safe unique member names, and
entity-safe XML. It rejects encrypted or symbolic-link members. Limits are 256 MB compressed,
128 MB for one member, 512 MB expanded, and 2,000 members. The theme writer stages and validates a
complete ODP before replacing the destination.

The authoritative OTP must contain exactly one 16:10 master, one full-width native gradient band,
one centered title placeholder, and outline levels 1 through 9. Master-page images are currently
rejected because applying `styles.xml` alone would not copy their package assets. These checks make
an unsupported template fail visibly rather than produce a partially themed presentation.
