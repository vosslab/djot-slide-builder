# Markdown and Djot interview notes

Status: research notes supporting the selected Djot foundation. This page records what a supplied
John MacFarlane interview contributes to the extension's design; it is not a Djot tutorial or a
slide-language specification.

## Source and limits

The evidence is a supplied automatic-caption transcript of the
[John MacFarlane interview](https://www.youtube.com/watch?v=oVIQ0rR_BF0). The transcript is not a
tracked repository artifact.

Automatic captions are useful for locating discussion, not for exact quotation. The notes below
paraphrase the relevant passages and retain timestamps so a reader can check the source. The
interview discusses general markup design, not this repository's layout grammar.

## Interview observations

| Time | Paraphrased observation | Language-design lesson |
| --- | --- | --- |
| 00:06:30-00:07:50 | CommonMark arose because implementations disagreed even about core Markdown. Participants also valued different things because they used Markdown differently. | The lecture-authoring use case must drive decisions; do not inherit ambiguous defaults merely for compatibility. |
| 00:20:20-00:21:23 | Djot grew from MacFarlane's essay Beyond Markdown, which identifies parts of Markdown that have remained difficult to specify. | A new language can define hard cases directly instead of trying to patch every historical interpretation. |
| 00:21:48-00:23:00 | Djot's uniformity principle keeps a block's meaning stable when it appears inside a list. Its blank-line requirement before a sublist is a deliberate, controversial tradeoff that helps avoid accidental lists. | Nested-list behavior needs a stated invariant and deliberate syntax; concise source and unambiguous parsing may conflict. |
| 00:24:11-00:24:18 | Markdown should remain readable without a special tool. | GitHub raw-source readability is a real design requirement, not an afterthought. |
| 00:46:37-00:46:44 | Normalizing an old language resolves much, but some remaining problems require a rewrite. | Extending Marp or GFM is not automatically preferable to a separately named language. |

## What this supports

- Specify the source language before implementation rather than letting parser behavior become the
  specification.
- Give each structural marker a precise scope, including behavior in code blocks, lists, and YAML.
- Define nested-list semantics before selecting compact shorthand.
- Test friendly-looking syntax against accidental structural matches and clear diagnostics.
- Treat source readability and punctuation cost as first-class constraints, alongside formal
  regularity.
- Djot is now the selected base language. Retain the historical GFM-display and Marp-migration
  tradeoffs, but test every proposed spatial extension against strict Djot compatibility.

## What this does not support

- Adopting Djot without evaluating its GitHub-readability cost and missing slide semantics.
- Copying Djot's blank-line-before-sublist rule into the future slide language.
- Assuming that an unambiguous grammar must use more structural punctuation than authors will
  tolerate.
- Selecting the current layout and slot marker illustration as final syntax.
- Treating an interview as an authoritative substitute for a written grammar and fixture suite.

## Relevance to slide syntax

The strongest lesson is not a particular token. It is to make a small number of structural forms
precise before authoring depends on them. If a layout line and named-region line are explored, the
grammar must say exactly where each works, how its body ends, what it means in a list or code block,
and how a literal matching line is written.

That work belongs in
[presentation_language_choices.md](presentation_language_choices.md), followed by a fixture-based
grammar proposal. It does not authorize parser or exporter implementation.
