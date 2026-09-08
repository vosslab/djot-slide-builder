# Lectern slides review

- Local snapshot: `OTHER_REPOS/lectern-slides`
- Upstream: [lectern-slides](https://github.com/bsletten/lectern-slides)
- Local version: 0.2.0
- Content type: Python deck assembler and multi-renderer CLI
- License found: MIT
- Recommendation: Adapt accessibility and diagnostic ideas

## What it contains

Lectern assembles Markdown fragments and ranges into decks, resolves assets, records source maps,
and targets several renderers. It also includes live serving, handout output, themes, image fitting,
and an accessibility audit.

The strongest implementation areas are `a11y.audit`, slide-warning helpers, the fence-aware slide
splitter, `Source`, `FilesystemSource`, `SourceMap`, `AssetResolver`, range parsing, and renderer
capability declarations.

## Reuse assessment

- Ideas: Source-aware error messages and checks for missing alt text, weak headings, empty links,
  and dense slides are directly useful.
- Code and functions: MIT allows reuse with notice, but functions must be evaluated independently.
  A narrow audit module is a better fit than importing Lectern's framework.
- Themes: The local central theme already owns typography, geometry, and colors.
- Architecture: Its transclusion dialect, TOML manifests, multiple renderers, and server conflict
  with one canonical Djot workflow and the no-server requirement.

## Decision

Use Lectern as high-priority prior art for a future accessibility checker and source-aware
diagnostics. Do not adopt its assembler, renderer abstraction, server, themes, or authoring syntax.
