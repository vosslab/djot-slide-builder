# Lecture 05D v2 narrative review

The current [44-slide revision](lect05d-v2-probability_concepts.djot) replaces the fragmented
58-slide v2. The original deck remains intact. All 44 slides have speaker notes.
The preceding v2 source, ODP, and PDF are preserved in output/lect05d_before_narrative/.

## Teaching sequence

| Slides | Purpose and connection |
| --- | --- |
| 1-4 | Orientation, objectives, early vocabulary, opening section |
| 5-6 | Pose the F2 pollen problem and explain why we will first practice with simpler probabilities |
| 7-9 | Addition section: one gamete, two exclusive alternatives, specific rule |
| 10-14 | Full four-allele question, parent-to-gamete diagram, tempting wrong answer, square, double count |
| 15-19 | General addition; multiplication calculates the shared cell in the same cross; compare conditions |
| 20-27 | Return to the pollen problem, count successful pollen, multiply cells, add Aa routes, answer 1:3:2 |
| 28-33 | One family extension: unknown son genotype, child probability, new information, general multiplication |
| 34-35 | Exit check and answer using the three examples already taught |
| 36-38 | Summary section and the two standalone rule references |
| 39-42 | Reference-only explanations: rule choice, pollen cross, family example, reverse conditioning/Bayes |
| 43-44 | Final takeaways and THE END |

The multiple-choice votes are slides 11, 21, and 30; correct choices are B, C, and A.
Slides 12 and 23 invite students to complete a square before revealing the answer.
Notes explain the purpose of each revised teaching step and supply a spoken transition.

## Changes intended to make the story easier to teach

- Keep the four-allele cross through both rules, instead of changing contexts between formulas.
- Let the failed addition calculation motivate overlap correction, then calculate that same
  overlap with multiplication.
- Explain why the opening problem is temporarily set aside, and explicitly resolve it before
  moving into conditional probability.
- Restore parent-to-gamete branching graphics inspired by the original slides. Use full-width,
  editable Punnett tables with shared column sizing across each question/answer sequence.
- Use a family branching diagram to explain the child's probability and what changes when the
  son's genotype becomes known.
- Move reverse conditioning and Bayes to an optional study reference. Remove the separate
  not-aa warmup and next-offspring detour from the live narrative.
- Retain section headings, three votes, complete question statements, early definitions,
  allele italics, Unicode fractions, blue/orange rule colors, and summary references.

## Graphics and evidence

Three new editable SVG sources live beside the existing Venn assets:
gamete_branch_single.svg, gamete_branches.svg, and family_branches.svg.
The ODP embeds high-resolution PNG renders of these diagrams; their SVG text and geometry
remain editable in source. Questions, formulas outside diagrams, and Punnett tables are native
ODP text. The diagrams are schematic, with probabilities derived from the stated cross models.

PNG files follow the repository's generated-image convention and are ignored by Git.
Regenerate a diagram from its SVG with the established rsvg-convert workflow, for example:

```bash
rsvg-convert -w 3300 -o genetics/LECT05/djot/assets/lect05d-v2-probability_concepts/gamete_branches.png genetics/LECT05/djot/assets/lect05d-v2-probability_concepts/gamete_branches.svg
```

The original ODP/PDF slides 12-13 supplied the teaching reference for parent-to-gamete branches
and the large square. SVG construction used the local Mastering SVG viewBox discussion and
Preparing Scientific Illustrations guidance to clarify and simplify through figures.

Strict native Djot validation and capacity checks pass. The rendered review covers all 44 pages,
with full-size checks of revised figures, table sequences, and repaired wrapping.
Review images are in output/narrative_review/. Generated deliverables are:

- output/odp/lect05d-v2-probability_concepts.odp
- output/pdf/lect05d-v2-probability_concepts.pdf

Rendered cleanliness is not evidence that the teaching flow will feel natural to the instructor.
This version is ready for that teaching review, especially slides 5-19 and the return on 20-27.
