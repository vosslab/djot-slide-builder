# Teaching 11H: molecular clocks

The message to repeat is: **Sequence differences need a calibrated rate to become a time estimate.**
The 49-slide sequence breaks the reasoning into short advances; the extra slides mostly supply
missing definitions, questions, and worked steps. Speaking prompts are also in the ODP notes.

## Teaching route

| Pages | Purpose | Transition to say aloud |
| --- | --- | --- |
| 3-4 | Connect to the distance trees students just built | Our tree distances did not have units of years. We need a rate to add those units. |
| 5-12 | Choose comparable gene copies | First check which event separated the copies: a species split or a gene duplication. |
| 13-24 | Explain what changes and why rates differ | DNA can change without changing the protein. Selection also affects which changes persist. |
| 25-35 | Calibrate and calculate | A rate belongs to a particular kind of sequence. The pairwise distance includes two descendant branches. |
| 36-44 | Interpret assumptions and gene ancestry | The arithmetic gives a date under a model. We still need to ask what ancestor that date describes. |
| 45-48 | Explain the answer and keep a usable reference | Give the date, explain the rate assumption, and distinguish a gene ancestor from a species split. |

## Worked example to rehearse

Two sequences differ at 20 of 1,000 aligned sites. Approximate their distance as 0.020 substitutions
per site. For this teaching example, independent evidence places the split at 5 million years and
we assume the gene divergence coincides with it. Both branches have changed for 5 million years,
so the per-lineage rate is 0.020 / (2 x 5) = 0.002 substitutions per site per million years.

A new pair has distance 0.032. At that rate, its estimated divergence time is
0.032 / (2 x 0.002) = 8 million years. Check forward: each branch contributes 0.016,
which adds to the observed 0.032. A rate half as fast would require twice the time.

The two-branch picture is page 30. Calibration is pages 31-32; the question is page 33 and
its answer is page 34. The reusable formula and unit definitions are on page 47.

## Scientific corrections and preserved examples

- Orthologs are separated by speciation; paralogs by duplication. Function does not define either.
  Paralogs can occur in different species if duplication preceded speciation.
- Mutations and substitutions are distinguished. The Adh sample contains variable sites;
  its 43 variants are not presented as 43 fixed substitutions.
- Synonymous and nonsynonymous changes are defined by the amino acid outcome, with codon examples.
  The former claim that four nucleotide types cause a faster rate than 20 amino acid types is removed.
- The unsupported universal mutation-rate number is removed. Generation-time effects are explained
  without confusing per-generation mutation rates with yearly substitution rates.
- The historical beta-globin example retains 147 sites, 1.23 replacements per site per billion years,
  80 million years, and approximately 29 replacements. The calculation now states the per-lineage
  convention and the factor of two. The 80-million-year value is an inherited teaching assumption,
  not a newly established mouse-human divergence estimate.
- The protein plot is a historical rate illustration. Substitutions per 100 residues can exceed 100
  because the same site can change repeatedly; these are not percentages of differing residues.
- All nine substantive original figures are retained. The Adh map uses unchanged source-image
  pixels with readable vector labels placed in the unused whitespace.
  The blank imported SVG fragment is superseded by those labels. Source assets remain intact.
- The allele-sorting example is introduced after ancestral variation is explained. Gene ancestry
  can predate species divergence. Ortholog selection does not eliminate incomplete lineage sorting.

## Cognitive walkthrough and acceptance record

Method: an expert cognitive walkthrough of a live Zoom lecture and its distributed slides.
Users are upper-level biology students, including international students, and an instructor who
needs a sequence that is easy to explain aloud. This is an inspection, not a participant study.
The baseline was the original 19-page deck: unprepared jargon, changing topics, implicit units,
no calibration walkthrough, and a broken Adh figure with a replacement marker.

Success measures were set before rendering: each new term precedes its application; each worked
step retains its givens; questions precede answers; the final example can be solved from visible
content; all original substantive figures remain available; no replacement marker or clipped text.

| Task or error | Guideline and acceptance criterion | Evidence |
| --- | --- | --- |
| Decide what the lesson is doing | Show the goal and current step | Opening message and four numbered sections |
| Choose gene copies | Define terms before requiring a decision | Definitions 6-7; globin question 9; feedback 10 |
| Interpret rate differences | Pair vocabulary with a concrete example | Codons 15; Adh 16-17; rate figure 19-21 |
| Convert distance to time | Expose intermediate steps and units | Two-branch diagram 30; calibration 31-32; new problem 33-34 |
| Avoid the missing factor of two | Show a forward check | Two contributions of 0.016 on 34 |
| Avoid treating one gene as a species history | Explain ancestral alleles before the figure question | Setup 40; figure 41; question 42; feedback 43 |
| Explain a result independently | Ask for the number and its assumptions | Closing question 45 and answer 46 |
| Read labels without relying on color | Use text and branch position alongside color | New clock diagram labels both branches; blue/purple contrast measured against white |

The inspection adapts W3C cognitive guidance on [clear steps](https://www.w3.org/WAI/WCAG2/supplemental/patterns/o4p07-step-instructions/)
and [keeping needed information available](https://www.w3.org/WAI/WCAG2/supplemental/patterns/o6p05-low-cognition/)
to this slide sequence. These are supplemental design principles, not a claim of WCAG certification.
The local HCI book corpus was absent. No interactive UI implementation or platform-control audit
was needed for this static presentation.

Scientific checks used the [NLM ortholog/paralog explanation](https://www.nlm.nih.gov/ncbi/workshops/2023-08_BLAST_evol/ortho_para.html),
[Moorjani et al. on lineage rate variation](https://www.pnas.org/content/pnas/113/38/10607.full.pdf),
[Warnock et al. on calibration uncertainty](https://pmc.ncbi.nlm.nih.gov/articles/PMC4262156/),
and [Pollard et al. on incomplete lineage sorting](https://pmc.ncbi.nlm.nih.gov/articles/PMC1626107/).
The calibration numbers are explicitly invented teaching data.

Humanizer pass: removed vague generalizations and compressed jargon; kept biological terms with
plain definitions. The first draft still had long figure titles and small images. The final pass
gives the main figures full image pages and short captions, with explanations on following slides.
The wording and calculations are inspectable in the Djot source and the rebuilt ODP/PDF.

Final checks: 49 exported pages, 41 nonempty speaking notes, strict native lint, 343 focused
checks, independently recomputed arithmetic, and no extracted words outside the page.
All pages were reviewed in rendered contact sheets; focal figures were also inspected at larger
scale. New diagram blue and purple measure 6.66:1 and 5.52:1 against white; dark labels measure
16.29:1. Existing figure colors were retained. No live teaching, student comprehension study, or
attended Impress playback was conducted.
