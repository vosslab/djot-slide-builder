# Question layouts

Choose the layout for the teaching task. Keep slide text editable in ODP and selectable in PDF.
The [DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md) layout catalog supplies the complete vocabulary;
[PEDAGOGY_GUIDE.md](PEDAGOGY_GUIDE.md#ask-questions-with-a-purpose) covers teaching sequences.

| Layout | Teaching use | Authored content |
| --- | --- | --- |
| `question-ask` | An occasional question to ponder during the lesson | One H1 question. |
| `prompt` | An icebreaker with examples and suggestions | Optional H1, required `@prompt` and `@examples`. |
| `multiple-choice` | A choice-based problem with a revealed answer | Required `@question` and `@answer`. |
| `bookend` | A complete talking-point question set before its teaching content | H1 topic number/questions title and `@body`. |

## Talking-point setup slides

Put each topic's complete assigned questions on one `bookend` slide immediately after its
`subsection` divider, then show the content. This reuses the Key Takeaways frame. Preserve the
questions verbatim; smaller text is acceptable on this setup page. The exception does not extend
to explanatory slides. See [../TALKING_POINT_DECK_RECIPE.md](../TALKING_POINT_DECK_RECIPE.md).

## Questions to ponder

Use `question-ask` sparingly for a divider-like slide whose central text is a question to ponder.
Write one H1 question. Its editable text is large, bold, centered, and dark red (`#7B1E2B`)
inside an ultra light course-color hexagon with dark course-color corners. The following teaching
slides supply the explanation. Genetics Lecture 04H slide 5 and Lecture 06D slide 43 are examples.

```djot
=== layout: question-ask

# What Are the Parental Phenotypes and Genotypes for a Color-Blind Female?
```

## Open prompts and icebreakers

Use `prompt` for an icebreaker supported by concrete examples or suggestions. The required
`@prompt` slot holds one nonempty paragraph; the required `@examples` slot accepts nonempty
editable paragraphs and lists. An optional H1 supplies the slide title. Both regions are visible
by default. Put brief participation instructions before the example list.

The layout supplies a large, bold dark red prompt (`#7B1E2B`) and dark gray supporting text
(`#333333`) inside an ultra light course-color rounded card on the ordinary slide background.
The optional title sits above the card. Write ordinary text in the slots to inherit these styles.

```djot
=== layout: prompt

# Icebreaker

@prompt

Is a hot dog a sandwich?\
Is ice cream a soup?

@examples

State your name, major, and post-grad plans.

- Pick one and defend your rule: ingredients, shape, temperature, or how it is eaten.
- Examples: "A sandwich needs two slices." "Ice cream becomes soup when it melts!"
```

## Multiple choice and answers

`multiple-choice` has fixed teaching semantics. `@question` supplies an optional first component
image, an optional prompt, and a visible choice list. `@answer` supplies one or two editable
paragraphs. The layout measures the question, choices, and answer, then places the answer popup
in the available left or right region with its bounded on-click appear reveal. The popup is a
rounded light-gray rectangle with dark-red outline and editable text. Plain `@answer` text inherits
bold dark-red answer styling automatically. Use that default for ordinary answer feedback.
The layout supplies the answer's reveal automatically.
