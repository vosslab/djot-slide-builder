# Release history

## v26.09 - 2026-09-07

### Highlights

- Established `deck_tools.py` as the format-neutral CLI for building, importing, linting, and
  ODP visibility checks.
- Made Djot the sole authored deck source: builds route through `deck_tools.py build`, while
  trusted ODP and PPTX imports emit Djot.
- Added geometry-first ODP/PPTX import planning, source-region provenance, editable source tables,
  and bounded native OOXML animation generation.
- Added newcomer documentation for the architecture, file structure, formats, development,
  classroom workflows, troubleshooting, and related projects.

### Notable fixes

- Preserved imported text, hyperlink, table, and DNA run characters through the Djot output
  boundary.
- Limited recursive folder builds to `.djot` sources and rejected unsafe, missing, or symlinked
  imported assets before publication.
- Clarified current installation, usage, presenter-note, reveal, grammar, and acceptance evidence.

### Compatibility notes

- Authored decks now use `.djot`; the Marp parser, ODP/PPTX-to-Marp routes, target-format switch,
  Markdown decks, CSS theme, and associated dependencies were removed.
- The pre-production fork removed obsolete wrappers and compatibility aliases. Users should build
  with `deck_tools.py` or `build_slides.sh` and import trusted ODP or PPTX sources through
  `deck_tools.py import`.

### Validation

- The permanent offline suite passed 1,689 tests, including CLI, import-boundary, typing,
  security, hygiene, and link checks.
- One-time checks passed for recursive eight-deck builds, strict Djot linting, native PPTX/ODP/PDF
  exports, legacy-corpus regeneration, and a 62-slide ODP import.
