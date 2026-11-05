# Related projects

This guide points visitors to the source language and validation tool used by
this project, plus a text-authored presentation alternative with a different
output contract.

## Confirmed related projects

### Djot

- Relationship: Upstream source language
- Link: https://djot.net/
- Why visitors may care: Djot supplies the strict document-language foundation
  for the concise, hard-wrap-friendly source that this project extends into
  editable lecture slides.
- Evidence: Djot's official project describes a light markup language and its
  implementations. This repository explicitly selects Djot as its
  source-language foundation.

### Jotdown

- Relationship: Companion validation tool
- Link: https://docs.rs/jotdown/latest/jotdown/
- Why visitors may care: Jotdown provides the strict-Djot parser-validation
  step before this project's slide-specific lint and native export, so authors
  can check the underlying source language independently.
- Evidence: Jotdown's official crate documentation describes a pull parser for
  Djot. This repository pins its CLI as the native parser-validation lane.

## Possible related projects

### Quarto presentations

- Relationship: Direct alternative
- Link: https://quarto.org/docs/presentations/
- Why visitors may care: Quarto offers another text-authored presentation
  workflow for instructors and technical authors who need RevealJS,
  PowerPoint, or Beamer output.
- Evidence: Quarto's official presentation guide documents Markdown slide
  authoring and its RevealJS, PowerPoint, and Beamer presentation formats.
- Confidence: Medium

## Evidence notes

The confirmed entries are tied directly to this repository's selected Djot
source contract and pinned strict-parser gate. The possible entry has an
overlapping authoring workflow, but is not a drop-in replacement for this
repository's native editable-ODP output contract.
