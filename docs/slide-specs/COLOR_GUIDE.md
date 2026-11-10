# Slide color guide

This is the authoritative working specification for slide color. Your current instructions and
recorded preferences in [../HUMAN_GUIDANCE.md](../HUMAN_GUIDANCE.md) take precedence. Use
[VOICE_GUIDE.md](VOICE_GUIDE.md) for wording and [PEDAGOGY_GUIDE.md](PEDAGOGY_GUIDE.md) for teaching sequences.
The [AUTHORING_GUIDE.md](AUTHORING_GUIDE.md#authority-and-evidence) explains how
to distinguish explicit preferences, established conventions, and observed habits.

## Practical summary

Use color to help students recognize a concept, follow a relationship, or find the current step.
Keep useful distinctions and repeat them consistently. Select fewer incidental words to highlight
when prose becomes busy; preserve meaningful multicolor roadmaps, figures, and comparisons.

- Start with [../COLOR_PALETTE.md](../COLOR_PALETTE.md), including its existing role mappings.
- Match references to the objects, concepts, or numbered steps they identify.
- Carry associations through the question, explanation, worked calculation, and summary.
- Pair color with words, symbols, labels, position, or shape.
- Check text against its actual background, including filled cells and gradients.

## Preserve source meaning

During conversion, preserve deliberate text color, bold, italics, underline, and capitalization.
These can carry teaching meaning. Standardizing colors does not authorize changing the wording,
answer, example, sequence, or reveal. Follow the
[../SLIDE_CONVERSION_CHECKLIST.md](../SLIDE_CONVERSION_CHECKLIST.md).

Use the preferred explicit hex colors for new emphasis. An isolated imported shade is evidence of
that source slide, not a new palette requirement. Preserve useful source relationships when
standardizing; investigate uncertain relationships before recoloring them.

## Distinguish color roles

| Role | What color communicates | How to preserve the meaning |
| --- | --- | --- |
| Course theme | Course identity and navigation | Keep bookend/definition accents in the course hue, with light/dark variations. |
| Concept identity | A recurring rule, category, or entity | Reuse its color in labels, equations, diagrams, and callbacks. |
| Procedure step | A place in a method | Keep the same step colors and cross-references on repeated roadmaps. |
| Biological or data identity | A phenotype, chromosome, progeny class, or gene pair | Preserve the source's meaningful mapping through related views. |
| Current focus | The object or change being discussed now | Use a clear outline, arrow, mask, or selective highlight while retaining stable identities. |
| Answer or feedback | A result after students respond | Preserve the intended reveal and include a verbal or symbolic explanation. |

Theme colors and concept colors serve different purposes. A red Biotechnology theme does not
require every concept to be red. A procedure can use the same palette entries as a data figure
without implying that a step and a gene pair are the same thing; make their local roles clear.
These are local teaching associations, not a global dictionary assigning every scientific term
one color across all courses.

## Distinguish divider levels

Use a saturated course-color section with white text and its rounded frame. Use a pale course
tint for subsections, with black text and symmetric black full-width horizontal stripes. Keep
background contrast above 3:1 between these two levels, and keep text and stripes at the 5.5:1
house readability target against their own surfaces. Shape and type size reinforce the hierarchy.

## Highlight the important reference

Color the words students need to distinguish. A short label can carry color across its full name.
In a longer statement, a compact reference may do enough: color `H~0~` or the term it refers to,
leaving the surrounding explanation comfortable to read. Preserve scientific notation and useful
bold or underline.

Incidental words such as "sample," "organism," and "reaction" do not automatically deserve
color. They may deserve it when they are the concepts being compared. Do not color every technical
word just because it has a palette entry.

An explanation that refers to another concept should use that referenced concept's established
color. For example, a statement about the alternative hypothesis can refer to the null hypothesis
in the null hypothesis's color. The color identifies the reference, not the truth of the sentence.

Use coordinated, visibly distinct colors when several concepts need tracking. Preserve existing
assignments where they work. There is no universal maximum number of colors: a six-step roadmap
and a two-concept comparison have different jobs. Judge whether the distinctions remain useful in
the rendered slide.

## Carry associations through sequences

Keep recurring concepts consistent across related decks in a lecture. Carry the association into
singular/plural forms, aliases, labels, worked steps, and summary references when they identify
the same concept.

Established examples:

- **Probability rules:** Genetics Lecture 05 uses blue for addition/OR and orange for
  multiplication/AND. Keep the rule names and operators visible. In mixed calculations, color
  each operation according to its own rule, including general and special forms.
- **Procedure roadmaps:** use the recorded step colors and matching colored step references.
  Keep roadmap titles black so the steps receive attention. Reuse the canonical shared roadmap
  rather than maintaining slightly different copies.
- **Three-point testcross:** original parental rows stay green; other pairwise parental rows use
  lime; gene-pair recombinants and results retain their pair colors. The covered gene remains
  gray. A step color and a data-class color are separate roles.
- **Tetrads:** retain PD gold, TT magenta, and NPD green through related formulas and examples,
  following the instructor's labeled-diagram guidance.
- **Chromosome alterations:** use the full alteration names and the mappings recorded in
  [../COLOR_PALETTE.md](../COLOR_PALETTE.md); chromosome fills still identify source chromosomes.
- **Contact options:** preserve green Office hours, red Discord, blue Email, and purple
  Anonymous Google Form, with their nested details. See
  [ANNOUNCEMENT_DECK_GUIDE.md](ANNOUNCEMENT_DECK_GUIDE.md).
- **Assessment schedule:** past assessments are light gray, future assessments black, and next
  week's assessments dark red. This is a progress cue, not a global red-means-wrong convention.

The palette reference owns the exact text/fill values and new-step rainbow selections. Retain a
legacy method's established colors unless its recoloring is requested. Repeat roadmaps at useful
problem and gene-pair transitions, not only at the method's first appearance.

See the actual shared
[three_point_testcross_steps.djot](../../genetics/evergreen/three_point_testcross_steps.djot)
for a multicolor procedure with cross-references. It illustrates recorded instructor guidance;
its punctuation and line breaks are not universal requirements for new methods.

## Preserve questions and reveals

Before students answer, apply concept colors equally to correct and incorrect alternatives.
Avoid introducing a visual key that supplies an answer the student is meant to reason out.
After the response, color can intentionally show the answer, classification, or current worked
step. Keep question, scaffold, and answer states distinguishable.

This distinction does not require stripping color from questions. Colored terms and diagrams can
help students recognize what they are comparing. Preserve an existing reveal instead of judging
its final PDF state as though it had been visible before the question.

When converting, compare question/answer slides and any original animations or masks. Use labels
and more than color alone to distinguish changed conditions. Hints and worked explanations may
be visible teaching scaffolds; their placement follows [PEDAGOGY_GUIDE.md](PEDAGOGY_GUIDE.md).

## Keep theme and content readable

Use black table-header text on light course-colored backgrounds. Explicit cell fills do not
automatically change text color; check headers, colored rows, and total rows together. Distinguish
totals visually and keep numbers readable over their fills.

Preserve meaningful figure colors, such as purple flowers, rather than repurposing them as an
unrelated emphasis scheme. For concepts students must distinguish, the instructor prefers
blue/orange or blue/red over the too-similar blue/purple pairing in that context. This is not a
ban on using purple elsewhere.

Use [../COLOR_CONTRAST_ACCESSIBILITY.md](../COLOR_CONTRAST_ACCESSIBILITY.md) for the contrast
method and house target. Measure the actual foreground/background pair; passing against white
does not prove readability over a colored cell, photo, or gradient. Hue separation alone does not
prove contrast or distinguishability for every viewer.

The instructor's optional color-wheel tool is described in
[../COLOR_PALETTE.md](../COLOR_PALETTE.md). Keep chosen values explicit in Djot; building slides
must not depend on a sibling checkout or regenerate a different palette.

## Review as a student

- Are the concepts or steps that need tracking easy to find?
- Do repeated colors still refer to the same things through this teaching sequence?
- Is surrounding prose quiet enough to read without erasing useful colorful structure?
- Can words, symbols, labels, or position carry the meaning when colors are hard to distinguish?
- Does the question preserve its intended uncertainty until the appropriate reveal?
- Are text, labels, table fills, and summary references readable in the rendered output?

These questions support the advisory
[SLIDE_VISUAL_REVIEW_RUBRIC.md](SLIDE_VISUAL_REVIEW_RUBRIC.md); they do not create a new build gate.

## Adaptation boundary

The BPQ color guide contributed selective concept highlighting and the distinction between
concept identity and answer clues. Bank shuffling, term-pool assignments, and hue-angle recipes
are assessment-specific and are not slide requirements. Existing instructor mappings remain the
starting point.
