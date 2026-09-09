# Presentation-language brainstorming

Status: decision rationale and historical comparison, not a syntax guide. Djot is the selected
source-language foundation; the spatial slide grammar and public language name remain unfinished.
This page retains the comparison that led there. It authorizes neither parser work nor a public name.

## The actual problem

This is not a search for a cleverer Marp theme. Markdown is good at content hierarchy; slides also
need spatial hierarchy. Classic Marp remains a useful migration and conformance baseline, but it
cannot name the regions needed for the teaching layouts in this repository. The foundation decision
is resolved: extend Djot. The remaining question is which small syntax adds spatial semantics while
retaining strict Djot compatibility.

The repository will own the Python parser, native editable-object builders, LibreOffice conversion boundary, and
validation regardless of the source language. An external renderer or presentation pipeline is
therefore not the deciding factor. The decision is about what an instructor can comfortably write
and what the parser can understand without guessing.

## Why Djot is attractive

A recent John MacFarlane interview prompted this line of thought: Markdown accumulated ambiguous
cases and competing interpretations, while Djot began with a more deliberate grammar. That is an
important design lesson for a slide language. The grammar must settle ambiguities before course decks,
tooling, and compatibility expectations grow around them.

Djot is the selected base language. Its source does not display as ordinary Markdown on GitHub, and
it does not by itself answer the spatial-slide question. The extension inherits Djot syntax and its
specification discipline:

- Define the legal spelling and scope of every construct.
- State what a near-match means instead of silently guessing.
- Define how a construct interacts with code fences, lists, and other blocks.
- Reject source that has no stable native-slide meaning.

Djot's published syntax also includes tables, mathematics, footnotes, definition lists, attributes,
and generic containers. The extension inherits every form in its pinned Djot revision, but none
alone names a slide layout or content region.

The timestamped transcript analysis is in
[markdown_djot_interview_notes.md](markdown_djot_interview_notes.md). It identifies the interview
lessons without treating the interview as a substitute for Djot's specification. The narrower
[djot_slide_extension_exploration.md](djot_slide_extension_exploration.md) records the strict
compatibility requirement, provisional directive surface, and experiments still needed.

## GitHub and GFM

GitHub is where a deck is reviewed, linked, and read in raw source. It is not designed to display
spatial slides, so no authoring syntax can make its normal Markdown rendering a faithful slide view.
GitHub readability is therefore useful but must not decide the source foundation by itself.

GFM cannot be the complete slide language because it has no spatial model. Its familiar document
syntax and broad generic display remain useful historical comparison points, but it is not the
selected foundation.

CommonMark itself does not define tables. GFM adds a table extension, which makes GFM rather than
bare CommonMark the relevant familiar-document starting point when ordinary source tables matter.

### Optional display projection

The deck has one canonical Djot-authored source. If browsing on GitHub proves valuable, the pipeline
could optionally emit a derived, read-only GFM-friendly display view: title, content in layout
reading order, images, captions, and accessible links, but not a claim to reproduce slide geometry
or builds. This is an optional display artifact, not a second source, authoring input, or parser
input. It may be unnecessary and must not alter the selected Djot foundation.

## What authoring should feel like

- Write ordinary nested bulleted and numbered lists inside a named region.
- Use ordinary Markdown image source where an image belongs.
- Use hand-writable, LaTeX-compatible inline and display math.
- Name a recurring teaching layout instead of repeating geometry or CSS.
- Name the region where content belongs instead of relying on its ordinal position.
- Keep routine structure shorter than HTML tags, HTML comments, or deeply nested containers.
- Reveal an authored item or outline one item at a time without a general animation language.
- Preserve text, lists, practical equations, and images as editable native PPTX and ODP objects.

Raw HTML tags and `<!-- ... -->` comments are technically precise but spend too many characters on
routine structure. They are poor default authoring syntax even when they pass through a Markdown
renderer. Content-shape inference is also not enough: an author must be able to request asymmetry,
captions, galleries, and repeated teaching layouts explicitly.

## Starting points considered (historical)

| Start with | What it contributes | Open concern |
| --- | --- | --- |
| GFM | Familiar document syntax and broad generic display. | The extension must close Markdown's layout ambiguities. |
| Djot | Deliberate grammar discipline and normal document syntax. | Selected foundation; slide semantics still need design. |
| Marp-derived surface | Familiar slide headings and migration continuity. | Classic Marp lacks spatial semantics and must not constrain the successor. |
| Surveyed presentation format | Individual prior-art ideas. | No direct-adoption candidate currently meets the authoring requirements. |

The prior-art evidence was recorded in the now-retired `LAYOUT_LANGUAGE_SURVEY.md` and
`MARP_ADJACENT_PROJECT_COMPARISON.md`.

## Primary technical sources

- [CommonMark specification](https://spec.commonmark.org/): the core Markdown grammar and its
  intentionally small feature set.
- [GitHub Flavored Markdown specification](https://github.github.com/gfm/): the GitHub-readable
  CommonMark extension set, including tables.
- [Djot](https://djot.net/): Djot's published feature overview, syntax status, and implementations.
- [Djot repository](https://github.com/jgm/djot): the reference implementation and its rationale
  for unambiguous parsing, local inline parsing, and list behavior.
- [markdown_djot_interview_notes.md](markdown_djot_interview_notes.md): timestamped analysis of the
  supplied John MacFarlane interview transcript, kept separate from these primary specifications.

## Candidate syntax idea

This shape is worth exploring because it makes a layout and its regions visible without containers,
tags, comments, or per-slide geometry:

```markdown
@layout: two-panels

# Actin and microtubules
```

The possible reading is simple:

- `@layout: two-panels` starts a new slide and selects a title-plus-two-peer-boxes layout. It does
  not ask the renderer to infer that the material is a comparison.
- `#` remains a familiar slide title.
- Layout names describe body geometry; the title area is assumed. No official successor-language
  layout catalog has been selected yet.
- The `@name: value` family leaves a visible namespace for later, explicitly defined slide
  directives. The named-region form remains an open choice; it must not require a closing fence or
  source-order guessing.

That reading is an illustration, not a contract. The final language may keep these tokens, revise
them, or choose a better visible form. Djot is the selected foundation; the principle is more
important than the spelling: its extension needs a small structural layer for spatial slides that
remains valid strict Djot source.

## What must be unambiguous

The first grammar proposal must choose exact answers rather than leaving them to implementation.

| Topic | Rule the grammar must state |
| --- | --- |
| Slide boundary | How slides divide without confusing a normal GFM horizontal rule. |
| Layout line | Where it may occur, its exact name syntax, and whether every slide needs one. |
| Slot line | Where it may occur, its exact name syntax, how it ends, and how literal matching text is escaped. |
| Title and subtitle | Which headings have slide-level meaning and which remain region content. |
| Layout contract | Which slots are required, optional, repeatable, and ordered for each layout. |
| Content-language scope | The selected source specification and allowed extensions inside a slot. |
| Code and YAML | Whether directive-looking text is inert inside YAML, indented code, and fenced code. |
| Images and captions | Whether each uses an explicit region or another equally unambiguous construct. |
| Mathematics | The exact inline and display delimiters, including currency and escaping rules. |
| Reveals | A short source form for item builds and arbitrary-item appearance, plus nesting behavior. |
| Failure | The source-located error for unknown layouts, slots, directives, duplicates, and omissions. |

No grammar rule should depend on CSS, source order, content shape, accidental whitespace, or a
browser's recovery behavior. The parser should either construct a typed native-slide model or state
what needs correction.

## Naming thoughts

The successor should not be called Marp+ by default. It may diverge far enough from Marp that a new
name is clearer for authors and readers. Naming should follow the approved grammar, not lead it:
calling it Marp+ too early would suggest a compatibility promise that the project does not intend to
make.

## Next small experiment

Pin the Djot revision and complete compatibility suite, then express the survey fixtures and
deliberately ambiguous near-matches using provisional Djot extension forms. Review source
readability, strict-Djot results, extension diagnostics, and native model together before approving
the grammar, naming the language, creating its guide, or writing implementation code.
