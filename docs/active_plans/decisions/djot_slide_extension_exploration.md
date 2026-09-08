# Djot slide-extension syntax inventory

Status: extended-Djot is an implemented second front end to the shared native pipeline. This page
retains the grammar decisions and strict-Djot boundary. Exact `===`, `@`, `<=`, and `=>` forms are
implemented; component images and dollar-delimited mathematics remain distinct language contracts.
Unassigned forms such as `%%` remain ordinary Djot text, not aliases.

## Governing requirement: strict Djot compatibility

The implemented extended-Djot front end inherits every construct supported by the pinned Djot
syntax revision rather than defining a smaller Djot subset. Strict Djot validity is its top-level
compatibility requirement: the parser and source-only extension linter run only after the pinned
native parser accepts the unmodified source. The extension adds slide semantics after that gate; it
can never waive a Djot failure or accept syntax that strict Djot rejects.

Jotdown 0.10.0 is the pinned native parser currently exercised by the compatibility suite. It was
installed with the optional CLI and is invoked once per source before the local extension check; its
zero exit status is the suite's raw-Djot parser-validation result. Djot does not advertise an
official standalone linter. The exact syntax revision and any applicable formatter, editor-rule,
and lint tools remain open compatibility evidence to record as they are selected.
"Passes all Djot linters" can only mean a clean result from every applicable tool in that recorded
suite, rather than an untestable claim about an unnamed tool. A newly discovered applicable Djot
lint tool requires a documented compatibility decision before it is included in that claim.

## ASCII source and Unicode projection

The language supports ASCII authoring with Unicode in the final native presentation. A documented,
small character-reference projection runs only after the unmodified source has passed the strict
Djot compatibility gate. For example, ordinary text written as ``5&prime;-`ACGT`-3&prime;`` projects
as `5&prime;-ACGT-3&prime;`, with only `ACGT` in an inline-verbatim run.

`&prime;` is ordinary, valid Djot text, not native Djot entity syntax; the native pipeline owns its
projection to U+2032 PRIME. This is a controlled project vocabulary, not adoption of a general HTML
entity parser. Verbatim and raw content remain opaque, so their literal source is never rewritten.
Each additional character reference needs an explicit documented mapping and compatibility case.

## Source suffix

Use the upstream Djot `.djot` suffix for presentation source. Slide semantics belong to the extended
Djot grammar, not a separate `.djp`, `.djs`, or `.djots` filename convention. The source folder and
its `=== layout:` declarations make a deck's presentation role clear while standard Djot tooling
continues to recognize the file.

## Context

The instructor selected Djot because its source is readable when hard-wrapped and does not have
indented code blocks. Djot itself has no slide or spatial-layout semantics. The prior-art evidence
was recorded in the now-retired `LAYOUT_LANGUAGE_SURVEY.md` and
`MARP_ADJACENT_PROJECT_COMPARISON.md`.

The implemented layout catalog includes the default LibreOffice patterns plus `gallery` and
`multiple-choice`. The native registry owns exact slot contracts; an ordinary Djot renderer still
does not become a slide renderer.

## Future ownership boundary

The reusable slide-language work may eventually move to a separate repository from this personal
lecture-content repository. That future split does not authorize a migration, duplicate content, or
a new current source of truth. This page records language exploration where it is happening now.

## Experimental genetics corpus

[`genetics/djot/`](../../../genetics/djot/README.md) holds a regenerable source import of the eight
visible `lect0*` genetics presentations. It exercises real lecture material without replacing the
existing Marp source. Its dedicated ODP/PPTX importers preserve source order, component images, and
source-hidden-slide state while deliberately omitting presenter notes and arbitrary styling or
animation inference.

`deck_tools.py lint` supplies the pyflakes-scale, source-only structural check.
It reports slide declarations, documented slot contracts, action placement, and local image paths;
it invokes the pinned Jotdown 0.10.0 parser before its own checks. The eight imported decks passed
that native-first parser check. This remains only one lane of the required suite: its local
structural result is not a claim that no formatter, editor rule, or future applicable linter exists.

## Implemented slide surface

These exact whole-line roles are parsed into the native model. Strict Jotdown validation runs before
the source-only semantic lint; remaining formatter/editor-rule suite lanes remain open.

| Surface form | Provisional role | Constraint |
| --- | --- | --- |
| `=== layout: <name>` | Starts a slide and selects its layout. | It is the sole slide-start spelling; the catalog contains default LibreOffice layouts plus `multiple-choice`. |
| `@<slot>` | Selects a predefined content slot in the selected layout. | The slot name must be declared by that layout; for example, `@left` and `@right`. |
| `<= <action>` | A terminal animation directive applying to the preceding block or list item. | It is an action only as an exact final suffix; otherwise it is ordinary text. |
| `=> <action>` | A prefix animation directive applying to the following block. | It has no closing marker. |
| `=> cascade appear` | A prefix animation directive for the following outline or list. | It reveals that list's top-level items in source order. |

## Deferred figure action

`<= blue overlay` is recognized by the parser and linter but deliberately raises a source-located
"not yet supported" error. It has no native geometry, timing, or rendering owner. The deferral
keeps the spelling reserved without silently accepting or approximating a visual treatment.

## Titles and subtitles

The language retains familiar Marp heading spelling inside a slide:

```djot
# Slide title
## Slide subtitle
```

In a layout with a title region, `#` supplies the title. In a layout with a subtitle region, `##`
supplies subtitle content. Multiple H2 lines on `title-slide` remain one subtitle region. A layout
without title placement rejects headings rather than silently drawing them somewhere else.

## Djot content boundary

The front end recognizes headings, ordinary lists, links, quotes, inline verbatim, fenced code
blocks, tables, component-image syntax, and the reserved `$inline$` and `$$display$$` mathematics
forms. Inline verbatim renders as editable fixed-width text. A validated table renders only in a
layout with a native table destination. Fenced code, display math, quote blocks, and inline math
remain source-located native-export rejections until their native owners exist. `=== layout:`
replaces Marp's `---` slide separator, and Marp-specific image modifiers are not adopted.

## Linter boundary

After the strict Djot gate, the deterministic source-only extension linter reports source-located
slide-structural errors without opening LibreOffice or rendering a slide. It checks slide
declarations, known layouts, title/subtitle permission, slot names and required/duplicate slots,
action attachment, and special layout contracts such as `multiple-choice`. Geometry, overflow,
animation export, and visual quality remain separate checks.

## Official layout: multiple-choice

`multiple-choice` is the first official extended-Djot layout. It has exactly these predefined
slots:

- `@question` contains the question prompt and its visible choice list. It is visible
  when the slide opens.
- `@answer` contains one or two short, flat editable paragraphs in the layout's fixed bottom-right
  popup region. The popup has one implicit object reveal.

`@question` and `@answer` are each required once. The answer has one implicit object reveal, so
`<= appear` and `=> appear` are invalid on its content. Implementation, structural tests, headless
PPTX-to-ODP package evidence, and PDF final-state export have passed; attended click playback in
LibreOffice Impress remains the sole open visual gate. Open-ended questions use another layout.

Examples:

```djot
=== layout: multiple-choice

@question

- Which molecule carries genetic information?
- A. Lipid
- B. Carbohydrate
- C. DNA
- D. RNA

@answer

Answer: C. DNA
```

## Remaining free block-level surface

| Surface form | Documented Djot behavior | Availability observation |
| --- | --- | --- |
| `@name: value` | Ordinary paragraph text; `@` has no documented block role. | The provisional slot form has no colon; this remains ordinary Djot text. |
| `===== layout: name` | Ordinary paragraph text at block level. | Parse-valid but not an alias of the provisional three-equals slide start. |
| `&& name` | No documented Djot block construct begins with `&&`. | Parse-valid free surface to test; it is not used by the layout survey and visually suggests Boolean or shell-and in some contexts. |
| `%% name` or `%%name` | Ordinary paragraph text at block level. | Parse-valid one-sided surface; `%` is a comment delimiter inside attributes, but no closing marker is required by Djot. |
| `%%name%%` | Ordinary paragraph text at block level. | Marp Extended uses this paired form for custom markers; Djot itself gives it no block meaning. |
| Kova's three-vertical-bar delimiter | No documented one-line Djot table construct is formed by this line alone. | It is notable compact prior art but triple repeated characters are not preferred for ordinary authoring, and `|` is table punctuation. Its literal source is shown below the table. |
| `. . .` | No documented Djot block construct begins with this spaced line. | Quarto Reveal uses it as a bare pause; it remains an unassigned free surface here. |
| `::name::` | Not a Djot generic div fence, which begins with at least three colons. | Slidev uses forms such as `::right::` as named slots; Djot's inline symbol syntax also uses colons, so its exact AST needs testing. |

### Literal Kova delimiter

<pre>|||</pre>

`## name` is deliberately absent: it is already a Djot heading, not free extension surface. The same
is true of attributes, generic divs, definition lists, pipe tables, footnotes, native Djot math,
quotes, lists, code, links, spans, and inline-format delimiters.

The layout survey is evidence of source shapes, not an adoption list: `|||` appears in Kova,
`. . .` in Quarto Reveal, `::right::` in Slidev, and `%%marp-*%%` in Marp Extended. Their survey
semantics do not transfer to Djot merely because their raw lines parse. In particular, the one-sided
`%% name` form is available to test without importing Marp Extended's closing-marker requirement.

## Reserved forms

- `![alt](path)` is the official component-image form. It is unavailable for slide, layout, region,
  reveal, or other extension syntax. This reservation covers the ordinary Marp and Djot image
  surface only; it does not adopt Marp-specific background, sizing, positioning, or filter modifiers.
- `$inline$` and `$$display$$` are the official inline and display mathematics forms. They are
  unavailable for extension structure and remain parse-valid/reserved source forms until a native
  math owner exists.

## Attribute scope

Djot attributes are metadata attached to an element. For example:

```djot
{source=electron-microscopy}
![Microtubule](assets/microtubule.png)
```

The one-line attribute belongs to the next element, here the image, not to a later sequence of
blocks. Attributes are represented in the IR but receive a source-located error until a native
mapping is defined. A generic div can group multiple blocks, but requires `:::` opening and closing
fences. Djot permits multiline attributes; that capability is outside the current supported subset.

## Parse-validity boundaries

- Native Djot accepts all provisional and free forms above as ordinary paragraphs. The
  extended-Djot slide parser, not Djot itself, gives the provisional forms their roles.
- The same is true of `=== layout: name` and `===== layout: name`: even an equals-only line has no
  Djot block meaning.
  Djot thematic breaks use three or more `*` or `-` characters with no other content; it has no
  Setext-style equal-sign heading underline.
- `----- layout: name` is likewise not a thematic break, but it is not glyph-stable: Djot smart
  punctuation converts a run of hyphens in ordinary text to en and em dashes. It is therefore not
  a useful visual-boundary candidate.
- An ordinary Djot renderer displays those lines as content. Parse validity is not native slide
  support.
- Code fences and raw blocks remain opaque: a marker-looking line inside them is code, not an
  extended-Djot language construct.
- Djot's syntax reference is not completely stable. Jotdown 0.10.0 supplies the current native
  parser evidence; pinning formatter, editor-rule, and lint lanes remains open compatibility work,
  not a prerequisite for the implemented front end.
- Djot does not advertise an official standalone linter. This is not an exemption: any eventual
  broad compatibility claim must name the parser, formatter, editor-rule, and linter evidence that
  supports it.

## Deliberately unassigned questions

- Which action words beyond `appear` and `cascade appear` have an observed native timing contract.
- How a floating text box can evolve without turning ordinary authoring into a style-attribute
  language.
- Which currently unsupported Djot attributes and blocks gain editable native mappings.

## Evidence still needed

1. Pin the remaining formatter/editor-rule lanes of the strict-Djot suite.
2. Record attended LibreOffice Impress click playback in
   [wp_a1_animation_fidelity.md](../reports/wp_a1_animation_fidelity.md). This is the sole remaining
   animation acceptance gate; implementation, structural tests, headless PPTX-to-ODP package
   inspection, and PDF final-state export have passed.
3. Keep future native mappings behind a focused source diagnostic, editable-object design, and
   acceptance evidence.

## Primary sources

- [Djot syntax reference](https://htmlpreview.github.io/?https://github.com/jgm/djot/blob/master/doc/syntax.html):
  current block, list, attributes, div, symbol, and ordinary-text behavior.
- [Djot quick start](https://github.com/jgm/djot/blob/main/doc/quickstart-for-markdown-users.md):
  Markdown-user guidance, including list-indentation discussion.
- [Djot repository](https://github.com/jgm/djot): implementation status and rationale.
- [Jotdown](https://github.com/hellux/jotdown): a Rust Djot pull parser with an event interface;
  implementation and validation prior art, not a production dependency or renderer choice.
- [John MacFarlane interview notes](markdown_djot_interview_notes.md): local interview-derived
  design lessons, kept separate from the written primary specifications.
