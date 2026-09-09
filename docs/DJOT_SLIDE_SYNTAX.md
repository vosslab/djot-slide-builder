# Djot slide syntax

Djot is the one authored source for a lecture.  Each declared source slide compiles to one editable
native ODP slide.  Use `deck_tools.py lint --require-native --native-executable <tool> <source>`
for the separate strict-native-Djot validation lane; compilation then applies the repository's
presentation parser and reports source-located errors for constructs without a native destination.

The catalog uses the twelve built-in Impress layouts, with author-facing names where that makes a
teaching choice clearer, plus two explicit project layouts.  LibreOffice documents the built-ins in
its [Slide Layout help](https://help.libreoffice.org/latest/en-US/text/simpress/01/05080000.html).

## Slide framing

Begin every slide with one exact, unindented layout directive.  A deck begins with a directive, and
the next directive begins the next slide.

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

`#` is the level-one slide title in title-bearing layouts.  In `section`, it is instead the centered
text in that layout's only outline box.  `##` is a subtitle on `title-slide` and `section`; inside a
named content slot, it is that slot's optional local heading.  Other heading levels have no native
slide destination.

## Layout catalog

The first twelve rows are LibreOffice-backed catalog layouts.  `multiple-choice` and `gallery` are
intentional project layouts.  "Root" means that ordinary content may appear outside a named slot;
required named slots still appear where listed.

| Djot layout | Impress layout and AutoLayout | Slots | Root | Choose it when |
| --- | --- | --- | --- | --- |
| `blank` | Blank, `AUTOLAYOUT_NONE` | none | no | You need an intentionally empty teaching pause. |
| `title-only` | Title Only, `AUTOLAYOUT_TITLE_ONLY` | none | H1 plus ordinary root body | A title introduces flexible editable text, lists, component images, or one table below when no panel layout fits. |
| `title-slide` | Title Slide, `AUTOLAYOUT_TITLE` | none | title/subtitle only | You are opening a lecture or major presentation. |
| `one-panel` | Title, Content, `AUTOLAYOUT_TITLE_CONTENT` | `body` | yes | One coherent explanation, outline, table, or contained component image needs the full content area. |
| `section` | Centered Text, `AUTOLAYOUT_ONLY_TEXT` | none | title/subtitle only | A section divider needs one prominent centered heading and little else. |
| `two-panels` | Title, 2 Content, `AUTOLAYOUT_TITLE_2CONTENT` | `left`, `right` | no | Two related ideas, figures, or comparisons belong side by side. |
| `one-plus-two-panels` | Title, Content over 2 Content, `AUTOLAYOUT_TITLE_CONTENT_2CONTENT` | `left`, `top-right`, `bottom-right` | no | One broad idea pairs with two stacked supporting items. |
| `two-plus-one-panels` | Title, 2 Content over Content, `AUTOLAYOUT_TITLE_2CONTENT_CONTENT` | `top-left`, `bottom-left`, `right` | no | Two stacked supporting items pair with one broad idea. |
| `stacked-panels` | Title, Content over Content, `AUTOLAYOUT_TITLE_CONTENT_OVER_CONTENT` | `top`, `bottom` | no | The reading sequence is top to bottom. |
| `two-over-one-panels` | Title, 2 Content over Content, `AUTOLAYOUT_TITLE_2CONTENT_OVER_CONTENT` | `top-left`, `top-right`, `bottom` | no | Two related upper items lead to one shared conclusion or figure. |
| `four-panels` | Title, 4 Content, `AUTOLAYOUT_TITLE_4CONTENT` | `top-left`, `top-right`, `bottom-left`, `bottom-right` | no | Four comparable items form a compact 2 by 2 teaching grid. |
| `six-panels` | Title, 6 Content, `AUTOLAYOUT_TITLE_6CONTENT` | `top-left`, `top-center`, `top-right`, `bottom-left`, `bottom-center`, `bottom-right` | no | Six short, comparable items need a 3 by 2 grid. |
| `multiple-choice` | project custom | `question`, `answer` | no | You are asking a closed question with visible choices and a revealed answer. |
| `gallery` | project custom | `gallery` | title only | Two through six component images are the teaching focus. |

`section` and `title-only` are deliberately different.  `section` is `ONLY_TEXT`: one centered,
Subtitle-style outline box, no title placeholder, and a `#` heading becomes that centered text.
Use it for a divider.  `title-only` is `TITLE_ONLY`: it has a top title placeholder and a native
blank region below.  It begins with one `#` heading; following root paragraphs, lists, component
images, or one table become ordinary editable native objects in source order.  That body region is
not an invented content placeholder, so use `one-panel` when its native outline placeholder is
the useful semantic surface.

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

Use backticks for a short fixed-width sequence.  Fenced code preserves aligned multiline Djot
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
in the available left or right region with its bounded on-click appear reveal.  Authors write no
reveal directive in `@answer`.

## Supported boundaries

Use the strict-native lint lane above when strict Djot compatibility matters.  The repository's
presentation parser then gives native destinations to headings at their layout-defined levels,
paragraphs, nested lists, component images, links, inline verbatim, and rectangular pipe tables
without alignment metadata.

Raw HTML and XML tokens remain literal editable text under the current subset parser.  Generic
divs, footnotes, raw blocks, definition lists, thematic breaks, Djot symbols, paired tilde or caret
inline forms, and inline images have no presentation surface.  One-line Djot attributes are parsed
as metadata but await a native presentation mapping.  Fenced code, display math, block quotes, and
inline math are recognized source forms that currently receive a native-destination diagnostic.
Source-located diagnostics make the available editable forms clear.
