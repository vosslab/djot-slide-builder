# Lecture 02 syntax-gap survey

Status: exploratory content survey. This records the authoring needs visible in the six local legacy
`genetics/lect02*` ODP/PDF pairs. It assumes every default LibreOffice layout and the custom
`multiple-choice` layout exist. It does not authorize a deck migration or a parser implementation.

## Evidence examined

The survey visually reviewed the current PDF exports and extracted text and animation metadata from
the editable ODP files. A fresh, temporary LibreOffice PDF export produced the same visible-page
counts as the supplied PDFs.

| Deck | Visible slides | ODP slides with animations | Observed animation use |
| --- | ---: | ---: | --- |
| `lect02a-2025_announcements` | 43 | 0 | None |
| `lect02b-genes_dogma` | 49 | 6 | Multiple-choice answers |
| `lect02c-genome_sizes` | 59 | 5 | Multiple-choice answers |
| `lect02d-dna_structure_overview` | 43 | 4 | Multiple-choice answers |
| `lect02e-restriction_enzymes` | 62 | 3 | Stepwise labels and highlights on sequence diagrams |
| `lect02f-dna_electrophoresis` | 26 | 1 | Stepwise gel-band labels |

The six decks contain 282 visible slides. The 15 animated multiple-choice slides use only an
on-click answer appearance; the remaining four use on-click appearance for individual diagram
elements.

## Already covered

These source forms need no new slide-extension syntax, given the assumed layout catalog.

| Authoring need | Examples in Lecture 02 | Existing surface or decision |
| --- | --- | --- |
| Title, subtitle, and section divider | Every deck | `#`, `##`, and selected layout |
| Ordinary and nested teaching lists | Agendas, definitions, quiz policy, problem prompts | Djot lists |
| Static photographs, screenshots, charts, and textbook figures | Announcements, genetics history, genome-size, and gel slides | Marp image syntax with descriptive alt text |
| Multiple-choice question followed by a short answer | Genes, genome-size, and DNA-sequence questions | `multiple-choice` with automatic `@answer` appearance |
| Worked reasoning shown one stage at a time | Palindrome, restriction-map, and gel problems | A normal series of slides, not reveal syntax |
| Links and cited clarifications | Zoom, YouTube, and textbook material | Djot links and audience-facing footnotes |

In particular, a multi-step worked problem should remain a series of slides. It does not justify a
clone, continuation, or step-by-step problem language feature.

## Settled content surface

These are settled parts of the Djot-compatible content surface, not syntax gaps or requests for new
extension punctuation. The future implementation must render them as native editable content.

| Need | Lecture 02 evidence | Required behavior |
| --- | --- | --- |
| Tables | Experimental-result grids, genome comparisons, recognition-site reference | Use Djot tables and render them as native readable tables. Table cells may remain static across a slide series. |
| Fixed-width sequence text | Complementary-DNA and restriction-site exercises | Use Djot inline verbatim for short sequences and fenced code blocks for aligned multi-line sequences. |
| Inline and display mathematics | Base composition, genome-size values, and chemistry notation | Use reserved `$inline$` and `$$display$$` forms through MathJax or a similar plugin. |
## Slides outside the proposed surface

None. The four non-multiple-choice click builds are covered by slot-scoped `blue overlay` behavior:

| Deck slide | Current legacy behavior | Proposed source coverage |
| --- | --- | --- |
| `lect02e-restriction_enzymes`, slide 25 | Five on-click labels and highlights on a palindrome diagram | One image in a selected slot, followed by overlay blocks |
| `lect02e-restriction_enzymes`, slide 26 | Six on-click labels and highlights on a palindrome diagram | One image in a selected slot, followed by overlay blocks |
| `lect02e-restriction_enzymes`, slide 27 | Eight on-click labels and highlights on a palindrome diagram | One image in a selected slot, followed by overlay blocks |
| `lect02f-dna_electrophoresis`, slide 15 | Three on-click gel-band labels | One image in a selected slot, followed by overlay blocks |

The slot supplies the image coordinate system. A `blue overlay` block in a slot containing exactly
one Marp image is anchored to that image. Multiple overlay blocks may use the same image; no
image-specific identifier, coordinate, or style bag is needed. The linter rejects a `blue overlay`
block if the selected slot has zero or more than one Marp image.

For example:

```djot
@left

![Palindrome diagram](assets/palindrome.png)

Central unpaired base <= blue overlay unpaired
```

## Deliberately not gaps

- The observed grids, two-panel slides, vertical title slides, galleries, and centered prompts do
  not establish a layout gap because this survey assumes the complete LibreOffice catalog.
- The multiple-choice answer reveals do not establish a general popup requirement; the selected
  `multiple-choice` layout already gives `@answer` its automatic first-advance behavior.
- The source does not justify presenter-note syntax, arbitrary timing tracks, motion paths, or a
  generic color or geometry attribute bag.
- Red and colored words in legacy slides are not yet a separate inline-language requirement. First
  test whether ordinary emphasis, named callout treatment, or the proposed annotation action keeps
  their intended teaching meaning.

## Survey outcome

Djot tables, inline verbatim, fenced code blocks, dollar-delimited math, Marp images, slot-scoped
blue overlays, and accessible text cover every surveyed slide. No additional slide layout,
worked-problem, multiple-choice, or figure-anchor syntax is indicated.
