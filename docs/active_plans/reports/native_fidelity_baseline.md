# Native fidelity gap closure

Date: 2026-09-15

## Corpus evidence

- The 15 current Genetics decks contain 21 Djot tables. The restriction-site table in Lecture 02e
  supplied the long-row specimen; the blood/HLA tables supplied short and mixed-width specimens.
- The original ODP text uses six meaningful nondefault colors: red, orange, green, blue, purple,
  and gray. HLA offspring slides 33 through 36 use four colors to preserve parental haplotypes, so
  they require mixed-run color rather than a block-only treatment.
- Direct ODF inspection found 33 arrow-ended lines in the original lecture decks. None has both
  endpoints inside one source picture: some belong to diagrams without a component image, while
  others begin beside an image or a separately positioned label. Import therefore keeps these
  legacy drawings in its explicit review lane. Recasting them as image annotations would invent
  page coordinates or discard their positioned labels.
- No original transparent rectangle had unambiguous ownership by one component image. The first
  shipped outline contract remains useful for new image annotations and imported objects that meet
  that ownership rule.

## Settled native forms

- Text color uses ordinary editable `text:span` elements. Authored `{color=name}` values resolve
  through a closed repository palette; no arbitrary hexadecimal source values pass through.
- Arrows use native `draw:line` with explicit directional endpoints and a reusable ODF marker.
  Outlines use native `draw:rect` with `draw:fill="none"`. Both map percentages through the
  picture's aspect-preserving displayed rectangle.
- Tables keep native `table:table` structure. Header cells use the deck accent, body cells use the
  light panel surface, and serialized column widths and row heights come from the same measurement
  result used for fitting.
- The bounded ODP importer uses the repository's scoped `lxml` package parser. It follows admitted
  style inheritance for text color and shape properties, accepts only the two supported vector
  forms, and emits annotations only when exactly one picture owns them.

## Verification evidence

- A temporary generated ODP retained its arrow, revealed transparent outline, semantic colors, and
  caption through a LibreOffice ODP open/save cycle and direct ODP-to-Djot import with zero review
  reasons.
  The emitted coordinates matched the authored `15 20 80 65` arrow and `35 25 30 35` outline.
- LibreOffice rendered the temporary ODP and PDF with the arrow and outline aligned over the
  aspect-preserved image. Package XML retained `draw:line`, the native marker, and a no-fill
  `draw:rect`; the PDF reported embedded Atkinson Hyperlegible Next text rather than Type 3 glyphs.
- The repaired Lecture 02e table rendered all rows and its bottom border with light body cells.
  Content-aware allocation gave the long explanatory column more width while preserving the table
  frame width.
- HLA offspring slides 33 through 36 now restore the original parent/haplotype color grouping with
  attributed Djot spans.

## Remaining attended evidence

The strict-Djot executable is not installed in this checkout, so the repository's separate pinned
strict-source lane remains pending. The attributed-span spelling follows Djot's documented generic
span syntax; repository parsing, native export, ODP import, and round-trip validation cover the
implemented delivery path.
