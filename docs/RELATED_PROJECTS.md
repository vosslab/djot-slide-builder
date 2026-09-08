# Related projects

This guide points visitors to the upstream markup language, validation tool, and
presentation-authoring alternatives most relevant to an extended-Djot native-slide workflow.

## Confirmed related projects

### Djot

- Relationship: Upstream source, fork, or successor
- Link: https://djot.net/
- Why visitors may care: Djot supplies the strict document-language foundation for writing the concise, hard-wrap-friendly source that this project extends into editable lecture slides.
- Evidence: Djot's official project describes a light markup language, publishes the `.djot` extension, and lists Jotdown among its implementations; this repository explicitly selects Djot as its source-language foundation.

### Jotdown

- Relationship: Companion project, extension, or interoperability tool
- Link: https://docs.rs/jotdown/latest/jotdown/
- Why visitors may care: Jotdown provides the strict-Djot parser-validation step before this project's slide-specific lint and native export, so it helps authors check the underlying source language independently.
- Evidence: Jotdown's official crate documentation describes it as a Rust parser that turns Djot input into events, and this repository pins its CLI as the native parser-validation lane.

## Possible related projects

### Quarto presentations

- Relationship: Direct alternative or competitor
- Link: https://quarto.org/docs/presentations/index.html
- Why visitors may care: Quarto offers another text-authored presentation workflow for instructors and technical authors who need slide output in RevealJS, PowerPoint, or Beamer formats.
- Evidence: Quarto's official presentation guide documents slide authoring from Markdown headings and its supported RevealJS, PowerPoint, and Beamer outputs.
- Confidence: medium

## Evidence notes

The confirmed entries are tied directly to this repository's selected Djot source contract and
pinned strict-parser gate. The possible entries come from official presentation or project
documentation that establishes an overlapping authoring workflow; they are not recommended as
drop-in replacements for this repository's native editable-output contract.
