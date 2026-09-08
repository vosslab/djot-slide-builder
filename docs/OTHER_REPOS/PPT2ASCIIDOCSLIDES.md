# PPT to AsciiDoc slides review

- Local snapshot: `OTHER_REPOS/ppt2asciidocslides`
- Upstream: [ppt2asciidocslides](https://github.com/ullenboom/ppt2asciidocslides)
- Local project version: 1.1
- Content type: Java PPTX importer with AsciiDoc and Marp writers
- License found: GPLv3
- Recommendation: Architecture reference only

## What it contains

This Java and Apache POI project reads PPTX into a small renderer-neutral document model, then uses
a `DocumentWriter` to produce AsciiDoc or Marp. Its model contains documents, blocks, headers,
paragraphs, lists, images, and related content objects.

The conversion is intentionally simple. The snapshot contains no substantive automated tests and
does not demonstrate preservation of presenter notes, visibility, or measured slide geometry.

## Reuse assessment

- Ideas: Separating extraction from a target-format writer confirms the architecture already used
  by the local structured importer.
- Code and functions: GPLv3 Java source should not be copied into this MIT Python project.
- Markup: The Marp writer emits some raw HTML for superscript, subscript, and image dimensions,
  which is less compatible with the local minimal-HTML convention.
- Fit: It imports PPTX rather than ODP and offers less source fidelity than the current importer.

## Decision

Keep it as independent support for the intermediate-model pattern. It does not justify a code,
dependency, or workflow change.
