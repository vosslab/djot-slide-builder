# Slide voice guide

This is the authoritative working specification for slide wording. Your current instructions and
recorded preferences in [../HUMAN_GUIDANCE.md](../HUMAN_GUIDANCE.md) take precedence. Use
[COLOR_GUIDE.md](COLOR_GUIDE.md) for color and [PEDAGOGY_GUIDE.md](PEDAGOGY_GUIDE.md) for teaching sequences.
The [AUTHORING_GUIDE.md](AUTHORING_GUIDE.md#authority-and-evidence) explains how
to distinguish explicit preferences, established conventions, and observed habits.

## Practical summary

Write direct, concrete scientific teaching in the instructor's recognizable voice. Use familiar
words when they preserve meaning. Keep useful technical terms, complete questions, explanations,
humor, and deliberate emphasis. Match the amount of text to the teaching task.

- Preserve existing instructor wording during conversion, including useful informal phrasing.
- Write new material plainly; name the particular mechanism, comparison, prediction, or task.
- Use short labels where labels suffice and complete sentences where students need reasoning.
- Give students enough visible information to solve the problem and study afterward.
- Distinguish actual instructor wording from proposed examples and generated prose.

## Preserve before polishing

Conversion preserves approximately 98% of the original slide prose, allowing minor grammar and
clarity corrections. This is an approximate preservation target, not an exact automated test.
Preserve the examples, questions, explanations, scientific meaning, and relative sequence.
Color and layout improvements do not authorize a rewrite.

Retain deliberate ALL CAPS, bold, italics, underline, color, and meaningful punctuation. A
spelling correction is different from replacing an informal question with a formal explanation.
When the original wording works, keep it. Refer suspected scientific errors and substantive
changes to the instructor, respecting any correction already authorized for that task.

New objectives, a missing closing summary, and an optional early definitions slide can be written
from the lecture's existing content under the recorded conversion policy. Other new instructional
material follows the scope of the current request. See
[../SLIDE_CONVERSION_CHECKLIST.md](../SLIDE_CONVERSION_CHECKLIST.md).

## Ground the voice in evidence

These source phrases illustrate the recorded requirement to preserve teaching voice:

| Source wording | What the example illustrates |
| --- | --- |
| "How do we do questions like this???" | A conversational problem-solving question. |
| "where did we go wrong???" | An invitation to inspect a tempting mistake. |
| "completely cover up the third so it does not confuse you!!!" | Direct procedural advice with deliberate emphasis. |

The first two occur in
[lect05d-probability_concepts.djot](../../genetics/LECT05/djot/lect05d-probability_concepts.djot);
the third is in
[three_point_testcross_steps.djot](../../genetics/evergreen/three_point_testcross_steps.djot).
They illustrate source wording, not a requirement to add triple punctuation to new slides or a
claim that every part of those decks is an ideal template.

Prefer instructor-authored originals and identified instructor-cleaned material when choosing
examples. A recent import, generated expansion, unusual line break, or inconsistent old title is
not evidence of an intentional preference by itself. Corroborate a proposed rule with recorded
guidance or an established convention before making it mandatory.

## Write to the student

Use direct questions and instructions. "You" suits a task the student performs; "we" suits a
shared assumption or a calculation being developed together. Avoid inventing personal opinions,
anecdotes, or statements attributed to Dr. Voss.

Use concrete nouns and verbs. Name what changes, what is measured, or what students must decide.
Prefer a useful biological explanation to a generic paragraph that could fit any topic. A
citation or caveat belongs visibly when it is necessary to interpret the claim; administrative
provenance and repair history belong in separate review documents.

Illustrative new wording, not instructor quotations:

- General: "Consider the importance of vector design."
- More specific: "Will the Gene Fit in This Vector?"
- General: "Evaluate the implications of this result."
- More specific: "Which Progeny Classes Did This Calculation Leave Out?"

Use these as comparisons of specificity, not instructions to turn every explanation into a
question.

## Match wording to purpose

| Slide purpose | Useful wording |
| --- | --- |
| Diagram or visual anchor | Short, direct labels near the objects they identify. |
| Definition or rule | A plain definition, its condition, and enough context to use it. |
| Teaching explanation | Concise sentences that preserve the causal or logical connection. |
| Problem statement | The full setup, relevant assumptions, data, and an explicit task. |
| Guided worked step | Name what changed or ask students to attempt the next step. |
| Study reference | Complete sentences or coherent paragraphs explaining reasoning and assumptions. |
| Announcement or assignment | Direct instructions with accurate dates, expectations, and course context. |
| Speaker notes | Natural speaking prompts, transitions, explanations, reminders, and expected answers. |

For example, "hydrophobic core," "signal amplification," and "structure determines function"
can be useful labels. "This pathway amplifies the signal by activating many downstream
molecules" can be a useful explanation. The sentence is not wrong merely because it is complete.
Do not force four-word lines or fragments when meaning needs more space.

Preserve meaningful list hierarchy. Prefer a comparison, figure, sequence, or table when that
expresses the relationship better; a real list can remain a list. There is no universal word or
bullet quota, and these choices do not authorize splitting an existing slide.

## Keep the humor recognizable

Preserve useful humor, seriously absurd choices, familiar references, opinions, and asides already
present in the source. The Biotechnology Veridian Dynamics ending is an explicit course-specific
convention; follow [ANNOUNCEMENT_DECK_GUIDE.md](ANNOUNCEMENT_DECK_GUIDE.md).

When writing new humor within the authorized task, keep the science and instructions clear.
An absurd choice can be delivered deadpan and in the same grammatical form as the other choices.
A rhetorical question or brief aside can also carry the voice. Humor is not restricted to
invented names or answer choices, and jokes are not required on every slide.

Use notes for delivery-only jokes or personal reminders. Keep student-facing humor visible when
it is part of the source's intended teaching character.

## Introduce terms and notation

Use technical vocabulary when it adds precision. Check earlier decks in teaching order before
deciding a term is familiar: mentioning it is different from explaining it. Define essential
terms new to the sequence visibly in the first few slides, before students need them.

Keep definitions in familiar words and pair them with an example or visual when useful:

**mutually exclusive** = **cannot both occur**

Treat notation as vocabulary too. Explain `P(...)` and event labels before using them in
probability examples. Distinguish event placeholders from allele names. Reuse terms
consistently, and explain a new meaning of a familiar word.

Use the repository's native Djot conventions:

- Italicize allele and genotype symbols in prose, headings, tables, and equations: `_A_`, `_a_`,
  `_Aa_`. Ordinary words and answer-choice letters stay upright. Do not infer allele formatting
  from a matching letter alone.
- Render the null hypothesis with a subscript zero, `H~0~`; preserve superscripts and generation
  indices. Native chi-square title notation is `(&chi;^2^)`.
- Label the 5-prime and 3-prime ends of sequences when their direction matters; use the semantic
  monospace role when fixed-width sequence text helps.
- Keep visible spacing on both sides of multiplication signs.
- Use straight ASCII quotes/apostrophes and character references for non-ASCII symbols, such as
  `&alpha;`, `&times;`, or `&#x00BD;`. Let the backend own font selection.

See [DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md) for supported syntax. Blackboard HTML and
PGML conventions do not define this slide format.

## Keep numbers and choices consistent

State what is counted, the relevant units, and any rounding needed to interpret an answer.
Keep units and numeric formats consistent through questions, calculations, choices, and answers.
Use a space between a value and its unit. Do not introduce doubled wording such as "two (2)"
as a universal slide convention.

Avoid switching among fractions, percentages, and decimals while teaching another concept.
Lecture 05D v2 specifically uses fraction glyphs, with 0 for impossible and 1 for certain;
author those glyphs as character references in ASCII source. This scoped choice does not require
converting every course's probabilities to fractions. Counts and genotype ratios keep their
usual forms; teach conversions explicitly when conversion is the objective.

For newly written multiple-choice slides, use a direct question and short, parallel alternatives
of the same kind. Use a natural numeric or scientific order when it helps. If more than one
answer is expected, state the selection task clearly. Avoid a formatting or length difference
that gives away the intended answer. Preserve existing question wording during conversion.

## Write useful titles

Use Title Case for slide titles while preserving acronyms, proper names, gene symbols, and
scientific notation. This differs from sentence-case Markdown documentation headings. Prefer a
short title that fits on one line and identifies the slide's job.

Inherited title examples, normalized to the existing title-case convention:

- Topic: `Gel Electrophoresis`
- Question: `Which Band Moved Farthest?`
- Contrast: `Kinetics vs. Thermodynamics`
- Takeaway: `Smaller DNA Fragments Move Farther`

Shorten generated titles when useful. Flag a proposed substantive change to an instructor-authored
title rather than silently rewriting it to fit. Remove textbook figure identifiers while keeping
useful captions and diagram content, following the recorded conversion guidance.

## Review the wording

- Is the original task, scientific meaning, humor, and useful emphasis still present?
- Does new prose sound direct and specific rather than generic or falsely attributed?
- Can students read the complete problem and its assumptions without access to speaker notes?
- Are unfamiliar terms and symbols introduced before use?
- Are choices, quantities, units, sequence direction, and notation clear and consistent?
- Are spelling, articles, agreement, punctuation, and spacing polished in rendered output?

This review supports [SLIDE_VISUAL_REVIEW_RUBRIC.md](SLIDE_VISUAL_REVIEW_RUBRIC.md); it does
not turn lecture wording into a pytest gate.

## Adaptation boundary

The BPQ voice guide contributed clear tasks, lean wording, parallel choices, and mechanical
polish. Its assessment-specific limits on explanations and hints do not govern a teaching
sequence. Statement-bank clauses, entry-widget rules, mandatory word/digit counts, universal
monospace genotypes, and Blackboard markup are not imported as slide requirements.
