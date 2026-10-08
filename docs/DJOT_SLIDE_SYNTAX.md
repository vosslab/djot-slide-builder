# Djot slide syntax

Djot is the one authored source for a lecture. Each source slide compiles to one editable native
ODP slide; hidden source pages remain native hidden ODP pages. Use `deck_tools.py lint --require-native --native-executable <tool> <source>`
for the separate strict-native-Djot validation lane; compilation then applies the repository's
presentation parser and reports source-located errors for constructs without a native destination.

The catalog uses the twelve built-in Impress layouts, with author-facing names where that makes a
teaching choice clearer, plus explicit project layouts. LibreOffice documents the built-ins in
its [Slide Layout help](https://help.libreoffice.org/latest/en-US/text/simpress/01/05080000.html).
The additional `image-comparison` layout and self-contained SVG components are documented in
[SVG_DIAGRAMS.md](SVG_DIAGRAMS.md). Bold, underlined definition terms use
`[*Term*]{underline=true}`; optional semantic color uses `[*Term*]{color=blue underline=true}`.

## Deck color theme

Put one optional `color-theme` line before the first layout directive. The value applies to the
whole deck. Omission uses `genetics` for compatibility with the existing lecture corpus.

```djot
color-theme: biochemistry

=== layout: title-slide

# Lecture 04A
```

Use one of the four course names:

| Value | Course color | Readable accent |
| --- | --- | --- |
| `genetics` | Blue | `#24578F` |
| `biostatistics` | Green | `#127622` |
| `biochemistry` | Purple | `#6B638F` |
| `biotechnology` | Red | `#C9211E` |

The selected theme controls the top band, links, table headers, cover accents, section dividers,
and the closer. Keep the line exact and unindented. A duplicate, an unknown value, or placement
after the first layout is an error.

## Chapter files and includes

A large lecture can use a small master `.djot` file containing ordered chapter includes:

```djot
color-theme: biotechnology

include: set4_opening.djot
include: set4_chapter_12.djot
include: set4_chapter_13.djot
include: set4_summary.djot
```

Each chapter contains complete slides with the ordinary `=== layout:` and `@slot` syntax.
Build, lint, and inspect capacity using the master filename. Its filename also names the combined
ODP/PDF. Folder commands select the master once and omit its included files as separate decks.
Strict native lint visits the master and every included file. Diagnostics retain chapter filenames
and physical line numbers.

The include contract is deliberately small:

- A manifest contains optional leading `color-theme` metadata, blank lines, and exact unindented
  `include: <relative.djot>` lines. Put opening and closing slides in their own files; do not mix
  layout directives with include lines in a manifest.
- Include paths are relative to the file containing the directive. Only UTF-8 `.djot` files are
  accepted. Absolute paths, `..`, backslashes, missing files, and symlinks outside the master
  directory are rejected. Includes use no shell, network lookup, glob expansion, or executable code.
- Nested manifests are supported up to 32 levels. Circular includes fail at the offending
  directive. Repeating a chapter deliberately repeats its slides in the combined deck.
- The master controls the course theme. Chapters inherit it when omitted; an explicitly different
  chapter theme is an error. Keeping a matching theme on a chapter also supports standalone builds.
- Image paths throughout the lecture remain relative to the master file's directory. Keep sibling
  chapter files beside the master when they share its `assets/` directory. Moving slides between
  those files does not require changing image paths. A chapter in a subdirectory still uses the
  master image base when included.
- `include:` inside a slide's notes or prose is ordinary text, not a file-loading instruction.

These local input rules implement ASVS 2.1.1, 2.2.1, and 5.3.2. This is a trusted local authoring
workflow, not a public upload service. If include validation fails, correct the reported path,
theme, or cycle before rebuilding; a partial lecture is not accepted.

## Slide framing

Begin every slide with one exact, unindented layout directive. After optional deck color metadata,
the first layout directive begins the first slide and the next directive begins the next slide.

```djot
=== layout: one-panel

# DNA replication

@body

- Templates guide complementary base pairing.
- Each daughter duplex has one original strand.
```

Use an exact `@slot` line to enter a named layout region.  Every named slot appears once.  Content
before a slot is global content; it supplies titles, subtitles, or root content only when the
chosen layout accepts it.  Keep ordinary prose and lists in normal Djot form; a layout directive
and a slot directive are short, whole lines.

## Slides needing replacement

Put an exact, unindented `@replaceme` line after the layout directive, before headings, notes,
or named slots, when a slide needs human review or replacement. It works with every layout.

```djot
=== layout: one-panel
@replaceme

# Diagram needs reconstruction

@body

The editable source content remains here.

@notes

Rebuild the diagram from the original slide before showing it.
```

The marker adds a large red **REPLACE ME** watermark above the slide content in ODP and PDF.
Its white backing keeps it obvious on dark surfaces. Content, layout, notes, and reveals remain
editable underneath. Remove the marker after review and rebuild to clear the watermark.

The marker applies only to its slide. It can precede or follow `hidden: true`; a hidden marked
slide retains the warning in ODP and stays out of the PDF. Duplicates, indentation, trailing prose,
and placement after content are errors. Inside fenced code or `@notes`, it remains literal text.
The marker does not fill required slots or bypass source validation, image checks, or capacity.

New ODP imports add `@replaceme` to slides with nonempty `review_reasons`. The adjacent
`import_report.json` retains the reasons and original source evidence for human review.

## Instructor notes

Use one optional `@notes` section on any slide. It continues until the next exact named-slot
directive, such as `@body` or `@answer`, the next `=== layout:` line, or the end of the file.
The next slot must belong to the chosen layout; `@section` is not a slot name.

```djot
=== layout: one-panel

# DNA replication

@notes

Ask students which strand serves as the template.
- Pause for discussion before explaining the answer.

@body

- Each daughter duplex has one original strand.
```

Place notes after the title and any `hidden` metadata, before or between named slots, or at the
end of the slide. Notes do not replace required slots. Use an exact, unindented `@notes` line;
duplicates are errors. An empty notes section is allowed as an authoring placeholder.

Notes are plain text: line breaks and internal blank lines remain, and leading/trailing blank
lines are omitted. Complete character references such as `&alpha;` decode once. Bullet markers,
inline markup, links, images, and action-like lines remain literal text. Code fences are also
literal in notes; they do not protect a following slot or slide directive from ending the section.
A `@notes` line inside a visible fenced code block remains part of that code example.

Notes become editable speaker notes in the ODP, including on hidden slides. They do not occupy
slide space or affect capacity checks. The normal PDF export excludes notes and notes pages.
The editable ODP retains them; distribute the PDF when students should receive only slide content.

## Hidden slides

Keep optional or previously hidden material in source with `hidden: true` after the layout line:

```djot
=== layout: one-panel
hidden: true

# Optional review

@body

- Material to keep for a future lecture.
```

The metadata is one exact, unindented line before any heading, slot, or other content. Blank lines
may surround it. Accept only lowercase `true` or `false`, without a semicolon. Duplicate metadata,
invalid values, and metadata after content are errors. Inside a fenced code block it is ordinary
code text.

Omission or `hidden: false` makes the slide visible. Change the value or remove the line to restore
the slide at its existing source position. This setting belongs to one slide and never carries
forward to the next slide.

Hidden slides and their assets remain in Djot, receive the same structural and asset lint checks,
and compile to native hidden pages in ODP. Capacity inspection includes them. PDF export explicitly
excludes hidden pages, and LibreOffice omits them from classroom slideshow playback. An entirely
hidden deck can be imported and linted, but a build reports no visible slides. ODP import preserves
all source slides in order and emits `hidden: true` for hidden pages.

## Heading placement

`#` is the level-one slide title in title-bearing layouts.  In `section`, it is instead the centered
text in that layout's only outline box on the dark transition surface.  `##` is a subtitle on
`title-slide` and `section`. The `theend` layout accepts exactly one level-one `THE END` heading.
Inside a named content slot, `##` is that slot's optional local heading. Other heading levels have
no native slide destination.

## Layout catalog

The first twelve rows are LibreOffice-backed catalog layouts. `multiple-choice`, `gallery`,
`big-image`, and `theend` are intentional project layouts. "Root" means ordinary content may appear
outside a named slot; required named slots still appear where listed.

| Djot layout | Impress layout and AutoLayout | Slots | Root | Choose it when |
| --- | --- | --- | --- | --- |
| `blank` | Blank, `AUTOLAYOUT_NONE` | none | no | You need an intentionally empty teaching pause. |
| `title-only` | Title Only, `AUTOLAYOUT_TITLE_ONLY` | none | H1 plus ordinary root body | A title introduces flexible editable text, lists, component images, or one table below when no panel layout fits. |
| `title-slide` | Title Slide, `AUTOLAYOUT_TITLE` | none | title/subtitle only | You are opening a lecture or major presentation. |
| `one-panel` | Title, Content, `AUTOLAYOUT_TITLE_CONTENT` | `body` | yes | One coherent explanation, outline, table, or contained component image needs the full content area. |
| `reference` | Title, Content, `AUTOLAYOUT_TITLE_CONTENT` | `body` | yes | One-panel study material with an unfilled light gray border and automatic reference-only footer. |
| `section` | Centered Text, `AUTOLAYOUT_ONLY_TEXT` | none | title/subtitle only | A dark framed chapter transition needs one prominent centered heading and little else. |
| `theend` | Centered Text, `AUTOLAYOUT_ONLY_TEXT` | none | `# THE END` plus an optional root image | You are closing a lecture with the framed native closer. |
| `subsection` | Centered Text, `AUTOLAYOUT_ONLY_TEXT` | none | title/subtitle only | A lighter framed topic transition belongs within a chapter. |
| `two-panels` | Title, 2 Content, `AUTOLAYOUT_TITLE_2CONTENT` | `left`, `right` | no | Two related ideas, figures, or comparisons belong side by side. |
| `one-plus-two-panels` | Title, Content over 2 Content, `AUTOLAYOUT_TITLE_CONTENT_2CONTENT` | `left`, `top-right`, `bottom-right` | no | One broad idea pairs with two stacked supporting items. |
| `two-plus-one-panels` | Title, 2 Content over Content, `AUTOLAYOUT_TITLE_2CONTENT_CONTENT` | `top-left`, `bottom-left`, `right` | no | Two stacked supporting items pair with one broad idea. |
| `stacked-panels` | Title, Content over Content, `AUTOLAYOUT_TITLE_CONTENT_OVER_CONTENT` | `top`, `bottom` | no | The reading sequence is top to bottom. |
| `two-over-one-panels` | Title, 2 Content over Content, `AUTOLAYOUT_TITLE_2CONTENT_OVER_CONTENT` | `top-left`, `top-right`, `bottom` | no | Two related upper items lead to one shared conclusion or figure. |
| `four-panels` | Title, 4 Content, `AUTOLAYOUT_TITLE_4CONTENT` | `top-left`, `top-right`, `bottom-left`, `bottom-right` | no | Four comparable items form a compact 2 by 2 teaching grid. |
| `image-comparison` | project custom | `top-left`, `top-right`, `bottom-left`, `bottom-right` | title only | Two diagrams above two independently editable captions; captions determine the shared lower row height. |
| `six-panels` | Title, 6 Content, `AUTOLAYOUT_TITLE_6CONTENT` | `top-left`, `top-center`, `top-right`, `bottom-left`, `bottom-center`, `bottom-right` | no | Six short, comparable items need a 3 by 2 grid. |
| `multiple-choice` | project custom | `question`, `answer` | no | You are asking a closed question with visible choices and a revealed answer. |
| `gallery` | project custom | `gallery` | title only | Two through six component images are the teaching focus. |
| `big-image` | project custom | `image`, `caption` | no | One focal image needs the main page area with a short bottom caption. |

For `two-panels` with an image and text, place either kind in `@left` and the other in `@right`.
Vary the image side through the deck, alternating on consecutive image/text slides. Express the
placement in these existing slots; the compiler renders the sides exactly as authored.

`section` and `title-only` are deliberately different.  `section` is `ONLY_TEXT`: one centered,
Subtitle-style outline box, no title placeholder, and a `#` heading becomes that centered text.
Use it for a divider.  `title-only` is `TITLE_ONLY`: it has a top title placeholder and a native
blank region below.  It begins with one `#` heading; following root paragraphs, lists, component
images, or one table become ordinary editable native objects in source order.  That body region is
not an invented content placeholder, so use `one-panel` when its native outline placeholder is
the useful semantic surface.

`theend` selects a dedicated closer through its layout name. It requires one exact `# THE END`
heading. A single component image may follow the heading; the closer keeps its two large editable
text lines and places the image on the right side of its framed surface.

Bare `http://` and `https://` URLs become editable native hyperlinks automatically. Use a labeled
Markdown link only when the displayed text should differ from the destination URL.

Use the dedicated `theend` layout for a final closer:

```djot
=== layout: theend

# THE END
```

Add one component image after the heading when the closer needs a final teaching figure:

```djot
=== layout: theend

# THE END

![Designed protein folds](assets/protein-folds.png)
```

The layout requires exactly that one heading and renders the words as two giant centered editable
text lines. A native LibreOffice vector star sits inside the D; it is decoration rather than a font
character. Every authored character in the ODP and derived PDF remains a font-backed glyph. The
layout never rasterizes lettering.

Use `big-image` for a single focal image and a short editable caption:

```djot
=== layout: big-image

@image

![Blackboard Discord signup page](assets/discord-signup.png)

@caption

Sign up for the course Discord server through Blackboard.
```

Place an arrow or transparent outline directly after the image when it annotates that image. The
four numbers are percentages of the image content actually displayed after aspect-ratio fitting.
An arrow uses start x, start y, end x, and end y. An outline uses x, y, width, and height. Every
coordinate must remain from 0 through 100, and an outline must stay inside the displayed image.

```djot
=== layout: big-image

@image

![Gel lanes](assets/gel.png)

{color=red}
arrow: 15 20 80 65

=> appear
{color=green}
outline: 35 25 30 35

@caption

The arrow identifies migration; advance once to reveal the sample region.
```

The shapes remain editable LibreOffice vector objects. Omit `color` to use the deck accent. This
first version accepts only one-ended `arrow` and no-fill `outline` records owned by the single image
in `big-image`; it does not expose page coordinates or a general drawing language.

## Teaching content

Component images are whole paragraphs with meaningful alt text and a repository-relative path.
The compiler fits them with preserved proportions.

```djot
![Replication fork diagram](assets/replication-fork.png)
```

Use ordinary Djot paragraphs, unordered or ordered nested lists, strong emphasis, emphasis, and
links.  Use a pipe table when its rows and cells carry the instructional structure.  A table owns
its region, so place mixed prose or images in another slot or another slide.

```djot
| Enzyme | Role |
| --- | --- |
| Helicase | Opens the duplex |
| Ligase | Seals a nick |
```

For tables repeated across question/answer slides, give each table the same semantic group:

```djot
{table-group="overlap-cross"}
| | A3 | A4 |
| --- | --- | --- |
| A1 | ? | ? |
| A2 | ? | ? |
```

The compiler measures all tables in that group before laying out any slide, including later
answers and hidden slides. It pools column needs at the theme's normal body size, then uses
those shared needs when fitting each table. Tables with the same available width receive the
same column widths even if their text sizes differ. Editing an answer updates the whole group.
Groups are scoped to one deck and require the same number of columns; row heights still follow
each table's content. Group names start with a letter and contain letters, digits, `_`, or `-`.
Unrelated tables remain independent. Do not combine `table-group` with `column-widths`.

For deliberate manual proportions, set `column-widths` immediately before a table instead.
Weights apply to the full column widths, including padding:

```djot
{column-widths="1,3,3"}
| | A3 | A4 |
| --- | --- | --- |
| A1 | ? | ? |
| A2 | ? | ? |
```

Supply one positive finite numeric weight per column. Here the label column receives one
seventh of the width and each outcome column receives three sevenths. Omit the attribute for
automatic content-based widths. The table remains editable; wrapping and row heights still
respond to its content. Invalid, duplicate, or non-table uses are rejected.

Use `{color=<name>}` immediately before a paragraph, list, list item, arrow, or outline to color the
whole object. Use a Djot attributed span for a shorter colored run:

```djot
{color=red}
This whole warning is red.

Each child inherits one [red haplotype]{color=red} and one
[green haplotype]{color=green} in this example.
```

The closed names are `accent`, `black`, `red`, `orange`, `green`, `blue`, `purple`, and `gray`.
`accent` follows the deck's course theme. The remaining names resolve to repository colors rather
than arbitrary hexadecimal values. Inline spans additionally accept six-digit RGB values, such as
`[source emphasis]{color=#CC00CC}`, to retain imported colors that have no semantic alias. These
colors still need visual review for contrast and meaning. Duplicate colors, malformed RGB values,
unknown names, and unsupported attribute scopes are source errors.

Preserve emphasis with `*bold*`, `_italic_`, `*_bold italic_*`, and
`[*underlined bold*]{underline=true}`. Color and underline can coexist on the same span. Literal
ALL CAPS remains unchanged; import also applies explicit source uppercase/lowercase transformations.

For numbered allele subscripts, use numeric character references: `A&#x2082;` renders as
A with subscript 2, and `A&#x2081;A&#x2082;` renders both allele indices below the baseline.
These remain editable text and work inside colored spans and table cells.
Generation labels use the same convention: `F&#x2081;` and `P&#x2082;`.
For raised allele letters, use numeric references to modifier letters, such as
`I&#x1D2C;` (I with superscript A), `I&#x1D2E;` (I with superscript B),
and `C&#x1D3F;` (C with superscript R). Preserve the source allele letter case.

Use backticks for a short fixed-width sequence in Atkinson Hyperlegible Mono. Ordinary text uses
Atkinson Hyperlegible Next; literal URLs use IBM Plex Sans Condensed. Font-family choices and
missing-glyph substitutions belong to the backend, not Djot attributes.
Fenced code preserves aligned multiline Djot
source and currently receives a native-destination diagnostic before rendering.

~~~~djot
The template is `ATGC`.

```text
5'-ATGC-3'
3'-TACG-5'
```
~~~~

The inner fence in the example represents source; choose a longer outer fence when copying it into
a Djot document.  Djot recognizes `$inline$` and `$$display$$` mathematics, but native math output
does not yet have an adapter, so the layout validator reports it before rendering.  This preserves
the authored surface without pretending that a noneditable substitute is usable.

Write ASCII source where practical.  In ordinary text, `&prime;` projects to the Unicode prime
character (U+2032).  Verbatim and raw content retain their literal characters.

## Reveals

Use one exact action line beside a block with a native destination.  `=> appear` attaches to the
following paragraph, image, or list.  `<= appear` attaches to the preceding object; after a list it
attaches to its final logical item.  `=> cascade appear` reveals the following list one top-level
item at a time in source order.

```djot
=> cascade appear
- Semiconservative replication
  - Preserves one parental strand.
- Complementary pairing
```

`multiple-choice` has fixed teaching semantics.  `@question` supplies an optional first component
image, an optional prompt, and a visible choice list.  `@answer` supplies one or two editable
paragraphs.  The layout measures the question, choices, and answer, then places the answer popup
in the available left or right region with its bounded on-click appear reveal. The popup is a native
rounded light-gray rectangle with dark-red outline and editable text. Authors write no reveal directive
in `@answer`.

## Supported boundaries

Use the strict-native lint lane above when strict Djot compatibility matters.  The repository's
presentation parser then gives native destinations to headings at their layout-defined levels,
paragraphs, nested lists, component images, links, inline verbatim, and rectangular pipe tables
without alignment metadata.

Raw HTML and XML tokens remain literal editable text under the current subset parser. Generic divs,
footnotes, raw blocks, definition lists, thematic breaks, Djot symbols, paired tilde or caret inline
forms, and inline images have no presentation surface. One-line attributes have native meaning only
for the color scopes, table groups, and column proportions documented above. Fenced code, display math,
block quotes, and inline math are
recognized source forms that currently receive a native-destination diagnostic. Source-located
diagnostics make the available editable forms clear.
