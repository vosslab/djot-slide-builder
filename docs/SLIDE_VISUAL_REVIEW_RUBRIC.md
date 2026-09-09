# Slide visual review rubric

## Purpose and status

This document defines the project's advisory visual-quality review for rendered slide pages. It
judges whether a generated slide works as a classroom artifact and whether a migration preserves
useful visual intent. It is a permanent review definition, but it is non-gating and runs on demand.
A finding directs the next improvement; it never fails a build.

The review scores every slide on every dimension. The fixed total is 20 points: five dimensions,
each scored from 0 to 4. Scores focus attention, while the qualitative call gives the actionable
reason. The five dimensions supply the scores; similarity to an original slide informs the
migration classification.

This is a holistic visual review. A reviewer considers image quality, crowding, type size, and
alignment within the relevant dimension rather than adding conditional criteria or an N/A
denominator.

## Project visual guidance

The review uses classroom-readable typography: 36 pt titles, 28 pt body text, and a repository-owned
readable floor. It favors a consistent, rule-based theme and simple teaching layouts over arbitrary
legacy geometry. Clear hierarchy, sensible margins, a balanced 16:10 area, and preserved image
proportions with natural fit make slides easy to understand. Simplification preserves instructional
content and teaching sequence.

[HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md) remains the authoritative source for this guidance.

## Review modes

### Standalone visual quality

Give the reviewer the generated ODP-derived PDF page, produced from the generated ODP by
LibreOffice, and this rubric. Ask the reviewer to judge the page as a classroom slide on its own
merits. Record all five dimension scores, the 20-point total, and one qualitative call based on the
visible teaching effect and a specific reason.

### Migration comparison

Give the reviewer the original PDF page, its corresponding generated ODP-derived PDF page produced
by LibreOffice, and this rubric. Ask the reviewer to use Readability, Visual organization, Emphasis
and hierarchy, Use of space, and Overall effectiveness as comparison lenses. Record whether the
generated slide is `improved`, `roughly equivalent`, or `materially worse`, with the most important
visible teaching reason.

This comparison judges functional visual equivalence: whether the generated slide preserves useful
hierarchy, grouping, emphasis, balance, and instructional character while using cleaner standardized
composition. It accommodates changed coordinates, wrapping, and legacy style quirks, and records a
direct categorical judgment rather than a subtraction of two 20-point totals.

- Improved: The generated slide uses a substantially different arrangement while preserving the
  instructional emphasis and relationships and improving readability or balance.
- Roughly equivalent: The compositions differ, but the same material has similar prominence,
  grouping, and visual weight, with no meaningful teaching advantage for either version.
- Materially worse: The generated slide loses an important visual relationship, makes a key figure
  inconspicuous, obscures hierarchy, or creates substantially worse density or whitespace.

## Scores and calls

For each slide, report these fields:

| Field | Required value |
| --- | --- |
| Readability | Integer from 0 to 4 |
| Visual organization | Integer from 0 to 4 |
| Emphasis and hierarchy | Integer from 0 to 4 |
| Use of space | Integer from 0 to 4 |
| Overall effectiveness | Integer from 0 to 4 |
| Total | Sum of the five scores, from 0 to 20 |
| Concern | `no concern`, `minor concern`, or `material concern`, with a reason |
| Migration comparison | In migration mode only: `improved`, `roughly equivalent`, or `materially worse`, with a reason |

Use `no concern` when the slide needs no follow-up, `minor concern` when a visible issue merits
attention but does not substantially impair teaching, and `material concern` when the issue
substantially impairs the slide's teaching use. State the reason in a short sentence. Base each
concern call on its visible teaching effect and its specific reason; use scores as supporting
evidence.

## Dimension anchors

### Readability

Question: Can the slide be comfortably read and understood in a classroom?

- 4: Text, images, and relationships are immediately legible at presentation distance; the slide
  can be understood without straining or decoding its presentation.
- 3: The slide is comfortably readable overall, with only a minor local density, contrast, or
  legibility weakness.
- 2: A noticeable readability weakness makes part of the slide harder to follow, though its main
  instructional content remains usable.
- 1: Readability substantially interferes with understanding important material.
- 0: The slide is unusable as a classroom visual because important material cannot be read or
  understood.

Scoring prototypes:

- 4: A student can read the title, labels, figure, and their relationship immediately from a normal
  classroom viewing distance.
- 2: The main point remains usable, but dense text or a small label makes part of the explanation
  take extra effort to read.
- 0: Important text, labels, or relationships cannot be read or understood as a classroom visual.

### Visual organization

Question: Does the arrangement make the slide easy to follow?

- 4: Clear, coherent organization supports immediate comprehension and makes the intended reading
  path obvious.
- 3: Organization is generally clear, with only a minor awkward grouping, order, or relationship.
- 2: A noticeable organizational weakness makes the slide take extra effort to follow.
- 1: Organization substantially obscures important relationships or the intended reading path.
- 0: Disorganization makes the slide unusable for its teaching purpose.

Scoring prototypes:

- 4: Related material is visibly grouped, the reading path is immediate, and the major
  relationships are clear without searching.
- 2: The major elements are understandable, but grouping or placement makes the viewer work to
  determine which text, image, or idea belongs together.
- 0: The arrangement supplies no usable reading path or grouping for the instructional
  relationships.

### Emphasis and hierarchy

Question: Does attention go naturally to the important material?

- 4: The most important material is immediately apparent, and titles, lists, images, and supporting
  material form a clear instructional hierarchy.
- 3: Hierarchy is clear overall, with only a minor competing emphasis or locally weak distinction.
- 2: A noticeable hierarchy weakness makes it unclear what deserves attention first or how details
  support the main point.
- 1: Competing or missing emphasis substantially interferes with the slide's instructional point.
- 0: The slide provides no usable hierarchy for understanding its important material.

Scoring prototypes:

- 4: The instructional focus is immediately apparent, while supporting material remains clearly
  subordinate.
- 2: The main point is present, but a competing element divides attention enough to weaken the
  intended emphasis.
- 0: Similar visual weight across elements, or emphasis on the wrong element, leaves the
  instructional focus unclear.

### Use of space

Question: Does the content feel appropriately sized, balanced, and placed?

Score open space highly on a title or section transition when one large, clear cue becomes the
obvious focus. Score it lower when the remaining teaching content is too small or unframed to state
the point.

- 4: Space supports the content naturally, with no conspicuous wasted or overcrowded area and with
  well-balanced placement.
- 3: Space is generally effective, with only a minor awkward empty, crowded, or imbalanced area.
- 2: A noticeable empty, crowded, or imbalanced area weakens the slide.
- 1: Space allocation substantially harms the presentation of important content.
- 0: Crowding, waste, or placement makes the slide unusable for its teaching purpose.

Scoring prototypes:

- 4: Text and images receive the space they need, and the occupied and open areas make the slide
  feel balanced.
- 2: A visibly crowded or empty area weakens balance while the main instructional content remains
  usable.
- 0: Crowding, wasted area, or placement prevents important content from serving its teaching use.

### Overall effectiveness

Question: Does this work as a teaching slide?

- 4: The slide communicates its instructional point effectively and supports teaching without a
  meaningful visual obstacle.
- 3: The slide works well for teaching, with only a minor weakness in how it communicates its point.
- 2: The slide remains usable, but a noticeable weakness reduces its teaching effectiveness.
- 1: A substantial weakness prevents the slide from reliably supporting its instructional purpose.
- 0: The slide does not work as a teaching slide.

Scoring prototypes:

- 4: The slide communicates its teaching point promptly and supports the instructor without a
  meaningful visual obstacle.
- 2: The slide remains usable, but a visible weakness reduces how effectively it communicates the
  teaching point.
- 0: The slide cannot reliably communicate or support its intended teaching point.

## Deterministic verification

Use deterministic verification for page count, image aspect ratio, layout identity, centering,
chrome, full-slide raster checks, and other mechanically measurable properties. Use this rubric for
holistic visual quality and functional visual equivalence.

A reviewer may describe the visible quality effect of a deterministically verified result.

## Calibration status

WP-S4 calibrated this advisory rubric with 20 opaque rendered pages spanning title, section-divider,
outline, image-heavy, and dense teaching slides. Three independent primary-model passes and one
alternate-model pass found that qualitative concern calls and their visible teaching reasons are more
stable and actionable than single-point totals.

Record the exact total for audit and communicate it in broad bands: **18--20 generally strong**,
**15--17 contextual review**, and **0--14 advisory visual attention**. Treat a one-point difference
as contextual evidence. Use the concern call and its specific visible teaching reason to set
follow-up priority.

Request advisory visual follow-up when a total is 14 or below, any dimension is 2 or below, or the
reviewer records a material concern. This attention rule is non-gating.

The five dimensions correlate strongly in this holistic review. Their intentional overlap provides
useful lenses for a teaching slide. Use them as complementary lenses rather than independent
measurements.

Standalone calibration is complete. A small, disposable paired original/generated PDF check will
calibrate repeatability of the migration-comparison categories; until then, record the categorical
functional-equivalence reason whenever original and generated PDF pages are compared.
