# News

## v26.09 - 2026-09-07

### Highlights

- Djot is now the sole authored deck format, with one CLI for builds, imports, linting, and ODP
  visibility checks.
- Trusted ODP imports preserve editable text, source tables, bounded image regions, and
  source provenance in generated Djot.
- Native ODP and LibreOffice-derived PDF exports now have a clearer documented path, backed by permanent
  offline tests and one-time native-chain checks.
- New architecture, setup, workflow, format, troubleshooting, and related-project guides make the
  project easier to enter.

### Upgrade notes

- Move authored decks to `.djot` and use `deck_tools.py build`; the Marp parser, target-format
  switch, and ODP/PPTX-to-Marp routes are no longer available.
