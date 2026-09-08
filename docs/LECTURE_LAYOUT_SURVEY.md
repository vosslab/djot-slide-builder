# Legacy lecture layout survey

## Scope and method

This survey examines the actual legacy slide documents for `lect01a` and `lect01b`, not their
imported or generated Markdown. It supports the language-choice evidence without selecting a
grammar or authoring syntax.

The sources are the rendered PDFs and the structured ODP drawing pages in the local legacy inputs:

- `genetics/lect01a-course_intro.pdf` and `genetics/lect01a-course_intro.odp`
- `genetics/lect01b-genetic_disorders.pdf` and `genetics/lect01b-genetic_disorders.odp`

The PDFs were rendered to images and visually inspected for actual spatial composition. The ODP
packages were read directly for visible-slide state, text/list/image objects, and animation metadata.
No Markdown deck was used as evidence for this survey.

| Deck | ODP pages | Visible rendered pages | Hidden ODP pages | Primary purpose |
| --- | --- | --- | --- | --- |
| `lect01a-course_intro` | 40 | 31 | 9 | Course logistics, instructor introduction, and announcements |
| `lect01b-genetic_disorders` | 23 | 23 | 0 | Concept introduction, class activity, and disease reference material |

Both decks use a 16:10 slide frame. `lect01a` source pages 19 through 25 and 38 through 39 are
hidden and are not PDF pages; the visible PDF sequence jumps over them. The survey below names PDF
page numbers so the content can be located in the actual presented deck.

## Course introduction deck

`lect01a` begins and separates major topics with sparse title slides, then uses a mix of ordinary
lists, one-visual-plus-text slides, and screenshots that explain a concrete student action.

| PDF pages | Actual slide content and composition | Layout evidence |
| --- | --- | --- |
| 1 | `Lecture 01A`: course, subtitle, instructor, and date centered on an otherwise empty slide | Title slide with several metadata lines |
| 2 | `Instructor Information` alone | Section/interstitial title |
| 3 | Instructor portrait at left and contact/biography facts at right | Image plus nested text list |
| 4 | `Ways to Contact Dr. Voss` with a numbered list and nested detail | Deep ordinary list without a visual region |
| 5 | Large YouTube mark with a link and one explanatory bullet | Hero image plus short caption/text |
| 6 | Discord explanation beside logo and QR code | Text region plus two visual components |
| 7 | Blackboard screenshot identifying Discord signup | Full visual/screenshot slide |
| 8 | Anonymous-message instructions beside an annotated Blackboard screenshot | Text plus screenshot and callout arrow |
| 9 | Office-hours list with a Zoom logo | Text plus component image |
| 10 | `Course Information` alone | Section/interstitial title |
| 11 | Two textbook covers with a large red X comparison mark | Paired visual comparison with annotation |
| 12 | New OER textbook description at left and cover at right | Text plus image, asymmetric visual emphasis |
| 13 | Explanation of the "build the plane" idiom beside an illustration | Text plus image |
| 14 | External resources in a nested list | Dense ordinary list |
| 15 | `How to be successful` with multi-level advice | Dense ordinary list |
| 16 | `Blackboard` alone | Section/interstitial title |
| 17 | Blackboard-page screenshot and displayed URL | Screenshot with a single textual locator |
| 18 | `Course Policies` alone | Section/interstitial title |
| 19 | `Other Required Credit` alone | Section/interstitial title |
| 20 | Discord-credit requirements as an ordinary nested list | Text/list slide |
| 21 | Discord instructions with logo and QR code | Text region plus two visual components |
| 22 | Signup screenshot with directional arrow | Screenshot and annotation |
| 23 | Student-profile requirement with portrait and profile facts | Text plus image/facts card |
| 24 | Student-profile prompts as a nested list | Text/list slide |
| 25 | Instructor academic profile as a multi-paragraph list | Text/list slide |
| 26 | Three cryo-electron-microscope photographs | Three-image gallery |
| 27 | Personal profile as a short list | Text/list slide |
| 28 | Ranked movie list and honorable mentions | Dense numbered-list slide |
| 29 | `General Announcements` alone | Section/interstitial title |
| 30 | Graduation deadline beside a reference screenshot | Text plus screenshot |
| 31 | `THE END` display text | Closing/title-only slide |

The nine hidden source pages are policy and student-club material. They do not appear in the PDF,
so they are excluded from the visual count rather than treated as a second current deck.

## Genetic disorders deck

`lect01b` uses deliberate question slides before definitions, then shifts from activity instructions
to dense reference material. It makes the need for both classroom pacing and compact multi-column
lists especially clear.

| PDF pages | Actual slide content and composition | Layout evidence |
| --- | --- | --- |
| 1 | `Lecture 1B`: lecture title, instructor, and date | Title slide with metadata |
| 2 | `What is a genetic disorder?` alone | Prompt/interstitial title |
| 3 | Difference between a disorder and disease, alone | Prompt/interstitial title |
| 4 | Definitions of disease and disorder in three bullets | Text/list explanation |
| 5 | `What is a genetic disorder?` repeated alone | Prompt before explanation |
| 6 | Genetic-disorder definition with nested categories | Nested explanatory list |
| 7 | Question about genetic anomalies, alone | Prompt/interstitial title |
| 8 | Gene-disorder types at left and chromosome diagrams at right | Text/list plus diagram |
| 9 | Breakout-room activity overview and one nested icebreaker prompt | Instructional list |
| 10 | Detailed activity questions in a nested list | Dense instructional list |
| 11 | Multi-card student presentation template | Full visual reference/template |
| 12 | Two columns of named genetic disorders | Dense equal two-column reference list |
| 13 | Fall 2024 group-presentation links | Dense link list |
| 14 | Fall 2023 group-presentation links | Dense link list |
| 15 | Fall 2022 group-presentation links | Dense link list |
| 16 | Presented disorders by group | Text/list reference |
| 17 | Fall 2021 group-presentation links | Dense link list |
| 18 | One shared disease-list link | Text/link locator |
| 19 | First half of a 23andMe carrier-status-report screenshot | Screenshot reference |
| 20 | Second half of the carrier-status-report screenshot | Screenshot reference |
| 21 | `Human Viruses` in two dense columns | Dense equal two-column list |
| 22 | `Bacterial Diseases` in two dense columns | Dense equal two-column list |
| 23 | `THE END` display text | Closing/title-only slide |

## Cross-deck findings

The visible slides give concrete, non-Markdown evidence for the structures the future language must
represent.

| Observed pattern | Slide examples | Requirement it supports |
| --- | --- | --- |
| Title, section, prompt, and ending slides | `lect01a` 1, 2, 10, 16, 18, 19, 29, 31; `lect01b` 1, 2, 3, 5, 7, 23 | Title-only and title/subtitle layouts must be first-class, not a body-layout accident |
| Ordinary and nested lists | `lect01a` 4, 14, 15, 20, 24, 25, 28; `lect01b` 4, 6, 9, 10 | Nested Markdown must remain ordinary inside any named text region |
| Text plus image or diagram | `lect01a` 3, 5, 6, 8, 9, 12, 13, 21, 23, 30; `lect01b` 8 | A two-region layout must support text/image in either direction and more than one image component |
| Screenshot plus instruction or annotation | `lect01a` 7, 8, 17, 22; `lect01b` 19, 20 | Screenshots are component images; a layout needs predictable placement and room for short guidance |
| Visual comparison and gallery | `lect01a` 11 and 26; `lect01b` 11 | Paired images, a gallery, and a full visual reference are recurring patterns, not variants of a bullet list |
| Dense equal text columns | `lect01b` 12, 21, 22 | Equal two-column lists must be explicit, readable, and independently capacity-checked |
| Question before explanation | `lect01b` 2 through 8 | The language needs a compact way to support classroom pacing without duplicating a complete slide for every small reveal |

There is no visible use of a 2x2 or 3x2 independently authored content grid in these two decks.
Those layouts remain in the broader teaching-layout wishlist because they are planned patterns, not
because this limited sample proves they are common today. Similarly, no equation appears in either
deck; equation support remains an independent requirement for other courses.

The red arrows and textbook-cross mark in `lect01a` are evidence for occasional visual annotation.
They do not yet establish a new slide-language requirement: they can remain part of a prepared image
asset until native annotation semantics are separately evaluated.

## Animation evidence and requirement

The ODP packages contain no `anim:*`, `presentation:animations`, `presentation:effect`,
`presentation:node-type`, or transition metadata. The legacy decks currently pace discussion with
separate prompt and answer slides rather than stored ODP builds.

Simple staged reveals are nevertheless a new explicit requirement for future lectures:

- On an advance, an authored text or visual item may appear.
- An outline may reveal one list item at a time in source order, including its nested structure.
- The author does not need motion paths, timing tracks, complex effect choreography, or a general
  animation timeline.

This capability is intentionally separate from the recorded imported-deck behavior. Its semantics
must still be shown to become editable native PPTX and ODP animation objects.

## Implications for the selected Djot grammar

The evidence rules out treating a lecture deck as a linear title-and-bullet document. Extended-Djot
now supplies the selected spatial presentation grammar.

The implemented vocabulary distinguishes these semantic cases:

- title and prompt slides;
- a title plus one ordinary text region;
- an explicit equal or asymmetric two-region layout;
- a named multi-region/gallery layout;
- a full visual reference slide; and
- bounded staged-reveal behavior for an authored item or list outline.

Geometry, image fitting, capacity checks, and native editable output continue to belong to the
repository-owned typed slide model and layout registry, not to CSS or per-slide pixel coordinates.
