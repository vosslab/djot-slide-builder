# Curated exemplar visual evaluation

## Provenance

This report preserves the independent rendered review by `/root/exemplar_image_evaluation`.
The immutable session transcript is
`/Users/vosslab/.codex/sessions/2026/11/09/rollout-2026-11-09T09-11-37-01a1c0dd-66ad-7f20-8528-4f176f787a6f.jsonl`.
The source event is `amsg_01a1c286-baf7-7351-bad9-fe4d141a006e`, at
`2026-11-09T22:56:12.023Z`, line 6400; the raw JSONL line SHA-256 is
`a8138584ca861a57ce802ad2549e968b7acb8e4497cdc55717bc667ef688fd91`.

## Review report

# Curated exemplar visual evaluation

Review date: November 9, 2026\
Mode: Independent standalone rendered review\
Scope: All 68 authored pages in `examples/exemplars/previews/`

## Overall verdict

The collection is broadly useful and mostly models strong teaching practice. It preserves recognizable scientific examples, clear course identities, complete reasoning sequences, and effective quantitative workspaces. It goes well beyond demonstrating that layouts compile.

Two pages need focused correction before the collection can confidently present every page as an exemplar:

- **03, slide 5:** Comparison figures are too small relative to their captions.
- **05, slide 7:** The central equation receives substantially less prominence than the explanatory prose.

These are bounded composition problems. **Broader redesign is not justified.** Preserve the collection's instructional character, table sequences, scientific color relationships, and existing examples.

The rubric distribution is **59 generally strong pages, 7 pages needing contextual review, and 2 pages needing advisory visual attention**. These bands describe judgments, not measured performance. One-point differences should not determine priorities.

## Review basis

I read `~/.codex/agents/image_evaluator.toml` first, followed repository instructions, and used the five dimensions in `docs/slide-specs/SLIDE_VISUAL_REVIEW_RUBRIC.md`. Color, pedagogy, voice, and authoring guidance informed interpretation.

Every page was opened directly at full-page size. The two principal concerns were reopened with original image detail before final judgment. Selected Djot sections were consulted to identify the corresponding authored content. No previous evaluation scores or implementation verdicts informed this review.

Paths in the inventory use this exact convention:

`examples/exemplars/previews/<deck stem>_sNN.webp`

The source for each inventory is:

`examples/exemplars/<deck stem>.djot`

Slide numbers below are authored numbers. Deck 07 slide 9 is the supplied diagnostic rendering of a hidden page; slide 10 corresponds to normal PDF page 9.

## Strengths

- **The quantitative sequences teach reasoning.** Deck 04 carries a consistent dataset through selection, classification, summation, division, and percentage conversion. Deck 05 explains independence, expected counts, units, and changing denominators rather than displaying unexplained formulas.
- **Stable visual anchors reduce searching.** Genotype rows retain their order, and the Punnett-square question and answer use matching cell positions.
- **Color usually carries identifiable meaning.** Gene-pair colors recur in tables and maps. Addition and multiplication retain their blue/orange association. Words, genotypes, P/R labels, position, and symbols supplement color.
- **Most figures receive useful scale.** The ascus, LOH, clone, recombination-bar, and map pages are clear teaching visuals when shown individually.
- **Text remains readable without becoming generic.** Complete questions and study explanations survive alongside concise headings and selective emphasis.
- **Bookends serve their intended purposes.** Covers, major/minor transitions, reference framing, takeaways, and closers are visually distinct. Sparse transition pages appropriately use open space.
- **Logistics examples are practical.** Visible destinations, paired assignment/date rows, meeting-format emphasis, and recognizable tutorial illustrations provide useful authoring references.

## Ranked findings

### 1. Enlarge the comparison figures

**Location:** `exemplar_03_figures_comparisons`, authored slide 5\
**Preview:** `examples/exemplars/previews/exemplar_03_figures_comparisons_s05.webp`\
**Source heading:** "From Daughter Cells to Patches"\
**Call:** Material concern

**Observed:** Both diagrams occupy relatively small islands in the upper portion of the page. Their labels are markedly smaller than those on slides 3 and 4. Large captions occupy most of the lower half. The right caption has an unusually large gap between its first and subsequent lines.

**Judgment:** The page demonstrates an unfavorable figure/caption balance. The viewer can read the prose more readily than inspect the relationship the figures are meant to compare. This particularly weakens its value as a figure-comparison exemplar.

**Recommendation:** Allocate more space to the figures and make the captions subordinate, using the existing content and supported layout choices. Keep each caption immediately associated with its figure and restore ordinary line spacing. No new artwork is needed.

### 2. Give the probability equation appropriate prominence

**Location:** `exemplar_05_equations_worked_examples`, authored slide 7\
**Preview:** `examples/exemplars/previews/exemplar_05_equations_worked_examples_s07.webp`\
**Source heading:** "Why Multiply the Probabilities?"\
**Call:** Material concern

**Observed:** A relatively small step heading and single-line equation sit near the upper-left corner. Most of the left column is empty. The right column uses substantially larger prose across much of the page height. The equation's "independent" subscript is especially small.

**Judgment:** The mathematical relationship is visually subordinate despite being central to the page's teaching job. The reasoning is coherent, but this is a weak model for displaying an equation beside its explanation.

**Recommendation:** Give the equation a larger, more balanced region. A bounded rearrangement or supported reflow of the same equation and explanation should suffice. Preserve the independence condition and numerical chain.

### 3. Improve the directional-notation pair

**Locations:** `exemplar_02_text_explanations`, authored slides 3-4\
**Previews:** `exemplar_02_text_explanations_s03.webp` and `exemplar_02_text_explanations_s04.webp`\
**Call:** Minor concern

**Observed:** Slide 3 places one sentence about 5-prime and 3-prime ends near the top, leaving most of the content area empty. Slide 4 gives answer B, while the answer box displays its equivalent sequence in the opposite reading direction.

**Judgment:** Slide 3 is readable but visually underdeveloped for teaching direction. Slide 4 asks students to perform an additional mental reversal to connect the displayed answer with option B.

**Recommendation:** Rebalance slide 3 around the existing end notation. On slide 4, explicitly connect the displayed antiparallel sequence with option B, preferably through aligned native notation or a brief equivalent-direction label. This is clarity polish, not a claim that the answer is wrong.

### 4. Refine equation/explanation balance

**Location:** `exemplar_05_equations_worked_examples`, authored slides 8, 10, and 11\
**Call:** Minor concern

**Observed:** These pages retain substantial unused space beneath their equations while explanation or table content extends farther down the adjacent column. Slide 8's equation is more prominent than slide 7's, and slides 10-11 remain readable.

**Judgment:** These are usable teaching pages. Their spatial imbalance makes them less persuasive as polished equation-layout references.

**Recommendation:** After correcting slide 7, check these three pages for a consistent equation scale and more comfortable vertical relationship to the explanation. Avoid adding content simply to fill space.

### 5. Tighten question-page grouping

**Location:** `exemplar_06_questions_sequences`, authored slides 2 and 7\
**Call:** Minor concern

**Observed:** Slide 2 places option A in the left area and options B-D in a right-hand stack, with a large revealed answer box below A. Slide 7 has a two-line title and a smaller, lower table than the earlier Punnett workspaces.

**Judgment:** Slide 2 requires more scanning than the clean table sequence that follows. Slide 7 remains understandable but loses some of the earlier workspace's visual stability.

**Recommendation:** Keep alternatives visibly grouped before and after reveal. For slide 7, consider a shorter heading or other small arrangement adjustment that preserves table scale. Static answer visibility alone is not evidence of a playback defect.

### 6. Supply matrix context when copied independently

**Location:** `exemplar_04_data_tables`, authored slide 10\
**Call:** Minor concern

**Observed:** The page shows a readable symmetric matrix, a highlighted lower-triangle minimum, and the instruction "Find smallest value." It does not visibly explain the meaning or units of the entries.

**Judgment:** It works as a table-format example and a simple search task. It is less self-contained as a scientific teaching example, especially after the preceding gene-mapping sequence.

**Recommendation:** Retain a short contextual label when adapting it independently, or clearly treat it as a separate table-format example. No matrix redesign is needed.

## Sequence-level findings

| Deck | Evaluation |
| --- | --- |
| 01: Orientation | Coherent repertoire of covers, objectives, definitions, transitions, rule cards, takeaways, and closure. Blue/orange rule identity survives across the sequence. The rule cards are denser than the bookends but remain usable. |
| 02: Text explanations | Demonstrates readable prose, nested lists, emphasis, and sequence notation. It is intentionally text-led. The direction/answer pair is the main opportunity to improve visual explanation. |
| 03: Figures and comparisons | Strong individual diagrams and an effective gene-order-to-map progression. Slide 5 interrupts that strength by reducing the figures' scale. The excerpt shifts from tetrads to mitotic crossover to mapping; these are distinct borrowing patterns rather than one continuous lesson. |
| 04: Data tables | The strongest sustained workspace example. Fixed row order, masks, persistent original-parent identity, and labeled classification make changing attention clear. Small positional changes occur early in the sequence, but they do not materially disrupt tracking. Slide 10 is a separate matrix example. |
| 05: Equations and worked examples | A complete instructional arc with useful distinction between table-column order and map order. Observed versus expected counts and denominator interpretation receive explicit treatment. Equation prominence needs local correction. |
| 06: Questions and sequences | Strong progression from plausible shortcut to a concrete counterexample, correction, general rule, and overlap calculation. The recurring four-cell workspace is especially useful. Revealed PDF states preserve study value; live reveal behavior remains unverified. |
| 07: Logistics and study support | Good breadth across identity, agenda, resources, schedules, reminders, reference material, and closure. Tutorial illustrations are recognizable schematic cues. The historical context and hidden optional state are appropriate collection metadata. |

The collection covers the requested teaching jobs well. It is strongest for genetics reasoning, tables, schematics, and explanatory text. It does not demonstrate every scientific visual form, such as microscopy interpretation or experimental graph analysis; that is a scope boundary, not a reason to expand this bounded collection now.

## All-page inventory and scores

Scores are **R** readability, **O** visual organization, **H** emphasis/hierarchy, **S** use of space, and **E** overall effectiveness. Each dimension is 0-4.

### 01: Orientation

Deck stem: `exemplar_01_orientation`

| Slide | Page identification | R | O | H | S | E | Total | Concern and visible reason |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 01 | Lecture 05D cover | 4 | 4 | 4 | 4 | 4 | 20 | No concern: clear identity and balanced metadata. |
| 02 | Learning Objectives | 4 | 4 | 4 | 3 | 4 | 19 | No concern: concise objectives remain prominent despite open space. |
| 03 | Probability Conditions | 4 | 4 | 4 | 4 | 4 | 20 | No concern: defined terms and explanations are immediately distinguishable. |
| 04 | Context Before Calculation | 4 | 4 | 4 | 4 | 4 | 20 | No concern: clear reading order and useful rule colors. |
| 05 | Probability Rules divider | 4 | 4 | 4 | 4 | 4 | 20 | No concern: one large cue serves the transition. |
| 06 | Addition Rule subsection | 4 | 4 | 4 | 4 | 4 | 20 | No concern: title and subtitle establish a clear minor boundary. |
| 07 | Addition Rules | 3 | 4 | 3 | 4 | 4 | 18 | No concern: denser rule reference remains readable and grouped. |
| 08 | Multiplication Rule subsection | 4 | 4 | 4 | 4 | 4 | 20 | No concern: matches the earlier subsection treatment. |
| 09 | Multiplication Rules | 4 | 4 | 4 | 3 | 4 | 19 | No concern: conditions, formulas, and notation explanation are coherent. |
| 10 | Key Takeaways | 4 | 4 | 4 | 4 | 4 | 20 | No concern: selective color reinforces the main distinctions. |
| 11 | THE END | 4 | 4 | 4 | 4 | 4 | 20 | No concern: unambiguous closure. |

### 02: Text explanations

Deck stem: `exemplar_02_text_explanations`

| Slide | Page identification | R | O | H | S | E | Total | Concern and visible reason |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 01 | In Vitro DNA Synthesis | 4 | 4 | 3 | 3 | 4 | 18 | No concern: readable paragraphs with clear term emphasis. |
| 02 | What a Reaction Needs | 4 | 4 | 3 | 3 | 4 | 18 | No concern: prose and comparison bullets have a usable hierarchy. |
| 03 | DNA Sequence Direction | 4 | 3 | 3 | 2 | 3 | 15 | Minor concern: sentence is stranded above a large unused area. |
| 04 | Complementary-sequence MC answer | 4 | 4 | 3 | 3 | 3 | 17 | Minor concern: answer direction requires an extra mental reversal. |
| 05 | Chemical DNA Synthesis | 4 | 4 | 4 | 3 | 4 | 19 | No concern: useful emphasis and comfortable list rhythm. |
| 06 | Chemical Synthesis: Strengths and Limits | 4 | 4 | 3 | 3 | 4 | 18 | No concern: nested detail remains distinct and readable. |
| 07 | PCR | 4 | 4 | 4 | 3 | 4 | 19 | No concern: cycle terms receive appropriate emphasis. |
| 08 | PCR: Cycle and Specificity | 4 | 4 | 4 | 3 | 4 | 19 | No concern: specificity statement is clearly prioritized. |

### 03: Figures and comparisons

Deck stem: `exemplar_03_figures_comparisons`

| Slide | Page identification | R | O | H | S | E | Total | Concern and visible reason |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 01 | All Four Products Stay Together | 3 | 4 | 4 | 3 | 4 | 18 | No concern: substantial prose remains paired with a readable ascus. |
| 02 | Why Keep the Four Products Together? | 4 | 4 | 4 | 3 | 4 | 19 | No concern: large labeled figure and explanatory bullets work together. |
| 03 | Two Copies of the Same Allele | 4 | 4 | 4 | 3 | 4 | 19 | No concern: genotype outcomes and arrows clearly support LOH. |
| 04 | One Event Can Make a Patch | 4 | 4 | 4 | 4 | 4 | 20 | No concern: lineage colors and patch diagram support the explanation. |
| 05 | From Daughter Cells to Patches | 2 | 3 | 2 | 2 | 2 | 11 | Material concern: small diagrams lose prominence to oversized captions. |
| 06 | What Is the Gene Order? | 4 | 4 | 4 | 4 | 4 | 20 | No concern: common-scale bars make the comparison immediate. |
| 07 | Three Choices, One Middle Gene | 4 | 4 | 4 | 3 | 4 | 19 | No concern: table makes reversal equivalence easy to inspect. |
| 08 | D-C-H gene-order figure | 4 | 4 | 4 | 3 | 4 | 19 | No concern: large map and caption state the conclusion clearly. |
| 09 | Why Don't the Results Add? | 4 | 4 | 4 | 4 | 4 | 20 | No concern: map sum and observed percentage are clearly distinguished. |
| 10 | Count Both Adjacent Intervals | 4 | 4 | 4 | 3 | 4 | 19 | No concern: classification, counts, and correction remain connected. |

### 04: Data tables

Deck stem: `exemplar_04_data_tables`

| Slide | Page identification | R | O | H | S | E | Total | Concern and visible reason |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 01 | Fruit Fly Inheritance | 4 | 4 | 4 | 3 | 4 | 19 | No concern: trait key and cross diagram establish the problem. |
| 02 | Three-Point Test-Cross Data | 4 | 4 | 4 | 4 | 4 | 20 | No concern: full data and answer workspace fit comfortably. |
| 03 | Most Frequent Types Are Parental | 4 | 4 | 4 | 4 | 4 | 20 | No concern: highlighted rows and parent-phase text agree visibly. |
| 04 | C to D: Which Numbers to Add? | 4 | 4 | 4 | 4 | 4 | 20 | No concern: mask makes the selected pair unmistakable. |
| 05 | Parental and Recombinant C-D Types | 4 | 4 | 4 | 4 | 4 | 20 | No concern: P/R labels supplement the meaningful fills. |
| 06 | Sum Recombinant Counts | 4 | 4 | 4 | 4 | 4 | 20 | No concern: selected counts visibly feed the sum and answer field. |
| 07 | Divide by Total | 4 | 4 | 4 | 4 | 4 | 20 | No concern: denominator and fraction are clear. |
| 08 | Convert to Percent | 4 | 4 | 4 | 4 | 4 | 20 | No concern: completed result retains pair identity. |
| 09 | Complete the Answer Fields | 4 | 4 | 4 | 3 | 4 | 19 | No concern: summary table and map preserve the percentage/map distinction. |
| 10 | Find smallest value | 4 | 3 | 4 | 3 | 3 | 17 | Minor concern: clear matrix lacks scientific context or units. |

### 05: Equations and worked examples

Deck stem: `exemplar_05_equations_worked_examples`

| Slide | Page identification | R | O | H | S | E | Total | Concern and visible reason |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 01 | Fruit Fly Test Cross | 4 | 4 | 3 | 3 | 4 | 18 | No concern: complete setup and abbreviations are readable. |
| 02 | The Gene Order Is Given | 4 | 4 | 4 | 3 | 4 | 19 | No concern: map order and supplied pair values are explicit. |
| 03 | Calculate Interference Between F and P | 4 | 4 | 4 | 4 | 4 | 20 | No concern: large native table retains all genotype/count associations. |
| 04 | Only the Middle Gene Changes | 4 | 4 | 4 | 4 | 4 | 20 | No concern: paired comparisons isolate the changing allele. |
| 05 | Observed Doubles | 4 | 4 | 4 | 4 | 4 | 20 | No concern: count emphasis and title identify the observed total. |
| 06 | Convert Percent to Probability | 4 | 4 | 4 | 4 | 4 | 20 | No concern: conversion and interval identities are clear. |
| 07 | Why Multiply the Probabilities? | 2 | 4 | 2 | 2 | 3 | 13 | Material concern: small equation is overwhelmed by large adjacent prose. |
| 08 | From a Fraction to a Count | 3 | 4 | 3 | 3 | 4 | 17 | Minor concern: equation/table balance leaves the left side underused. |
| 09 | Why Is the Expected Count 67.5? | 4 | 4 | 4 | 3 | 4 | 19 | No concern: expected versus observed interpretation is explicit. |
| 10 | Calculate Coincidence | 3 | 4 | 4 | 3 | 4 | 18 | Minor concern: readable formula and tall prose column feel imbalanced. |
| 11 | Calculate Interference | 3 | 4 | 3 | 3 | 4 | 17 | Minor concern: prose dominates the compact equation region. |
| 12 | What Does the 20% Refer To? | 4 | 4 | 4 | 3 | 4 | 19 | No concern: aligned questions, calculations, and results clarify denominators. |

### 06: Questions and sequences

Deck stem: `exemplar_06_questions_sequences`

| Slide | Page identification | R | O | H | S | E | Total | Concern and visible reason |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 01 | Now ask about one offspring | 4 | 4 | 4 | 3 | 4 | 19 | No concern: full question, assumptions, and gamete diagram are present. |
| 02 | Does every offspring qualify? | 3 | 3 | 3 | 3 | 4 | 16 | Minor concern: uneven option grouping increases scanning. |
| 03 | Test the claim with a Punnett square | 4 | 4 | 4 | 4 | 4 | 20 | No concern: large empty workspace supports student response. |
| 04 | Three offspring types qualify | 4 | 4 | 4 | 4 | 4 | 20 | No concern: same cells now identify the qualifying outcomes. |
| 05 | Shared cell counted twice | 4 | 4 | 4 | 4 | 4 | 20 | No concern: overlap label and correction explain the mistake. |
| 06 | Rule card: general addition | 4 | 4 | 4 | 4 | 4 | 20 | No concern: event labels and rule are locally defined. |
| 07 | Probability of the shared cell | 3 | 4 | 4 | 3 | 3 | 17 | Minor concern: long title reduces table scale and continuity. |

### 07: Logistics and study support

Deck stem: `exemplar_07_logistics_study_support`

| Slide | Page identification | R | O | H | S | E | Total | Concern and visible reason |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 01 | Lecture 08A cover | 4 | 4 | 4 | 4 | 4 | 20 | No concern: clear historical announcement identity. |
| 02 | Today's Agenda | 4 | 4 | 4 | 3 | 4 | 19 | No concern: topics and meeting information are easy to scan. |
| 03 | Important Course Links | 3 | 4 | 4 | 4 | 4 | 19 | No concern: complete URLs remain visibly associated with their purposes. |
| 04 | This Week: Oct 21 | 4 | 4 | 4 | 4 | 4 | 20 | No concern: format, topic, release, and due work are distinct. |
| 05 | Next Week: Oct 28 | 4 | 4 | 4 | 3 | 4 | 19 | No concern: asynchronous format is prominent. |
| 06 | Homework Due Dates | 4 | 4 | 4 | 3 | 4 | 19 | No concern: rows preserve assignment/date relationships and near-term emphasis. |
| 07 | Microbes #4: F-test | 4 | 4 | 4 | 3 | 4 | 19 | No concern: illustration supports the variability-comparison reminder. |
| 08 | Working Through Tutorials | 4 | 4 | 4 | 4 | 4 | 20 | No concern: reference framing and study instructions are clear. |
| 09 | Microbes #5: ANOVA, hidden diagnostic state | 4 | 4 | 4 | 3 | 4 | 19 | No concern: several-year illustration supports the stated comparison. |
| 10 | THE END | 4 | 4 | 4 | 4 | 4 | 20 | No concern: clear course-themed closure. |

## Recommended disposition

Retain the collection and correct the two material composition issues. Re-render and independently review the changed pages, with adjacent pages available to assess continuity. Treat the remaining findings as bounded polish opportunities rather than reasons to reopen every deck.

This is an advisory evaluation, not human approval or a build gate.

## Limits

I did not measure numerical contrast, font sizes, or object coordinates; contrast and scale comments are visual judgments. No requested review was blocked by a missing measurement tool.

I did not run LibreOffice, test live Zoom viewing, attend Impress click playback, verify link destinations, audit scientific answers exhaustively, establish asset ownership, or review the wider course corpus. Rendered previews do not independently establish native editability or reveal timing.

No files were changed. The main remaining risk is that the two weak compositions could be copied as preferred authoring patterns before correction.
