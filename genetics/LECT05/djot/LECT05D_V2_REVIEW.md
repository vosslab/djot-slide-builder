# Lecture 05D v2 review

The 53-slide [lect05d-v2-probability_concepts.djot](lect05d-v2-probability_concepts.djot)
is a separate teaching revision of
[lect05d-probability_concepts.djot](lect05d-probability_concepts.djot). The original teaching
content remains intact; its cover chapter label and opening/closing bookends follow the other decks.
All questions, equations, tables, and allele labels remain native text; Venn diagram labels
are editable in their SVG sources. All 53 slides have `@notes`.

## Teaching sequence

| Slides | Teaching job |
| --- | --- |
| 1-5 | Cover, objectives, section heading, hard pollen challenge, OR versus AND |
| 6-16 | Addition rule, tempting claim that every offspring qualifies, disproof, overlap correction |
| 17-19 | Derive multiplication from the same square; name independence |
| 20-28 | Return to pollen; count successful pollen, normalize, fill the square, solve the opener |
| 29-31 | Introduce conditioning; exclude aa and count two Aa routes among three remaining |
| 32-40 | Conditional inheritance; separate parent and child risks, reverse the condition, derive Bayes |
| 41-43 | Compare independence and exclusivity; predict the next offspring after three aa |
| 44-45 | Exit question and answer |
| 46-48 | Summary section heading, Addition Rules reference, Multiplication Rules reference |
| 49-51 | Study references: rule choice, pollen calculation, and conditioning; skip in class |
| 52-53 | Final takeaways, THE END |

Six multiple-choice votes occur on slides 10, 20, 30, 35, 38, and 42. Answers: B, B, C, B, D, and B;
the following worked slides explain why. Slides 11 and 24 ask students to fill a square before
the completed version appears. Other question-answer pairs separate prediction from explanation.
The notes suggest about 25 minutes, with flexible pauses for discussion or Zoom chat.

## Content and assumptions

- The three question screenshots supply the same underlying problems: unequal pollen success,
  four alleles at one locus, and Huntington inheritance. V2 paraphrases their questions into native
  text and removes textbook exercise numbers. It uses no screenshot assets.
- Ordinary four-allele cross: equal segregation and random fertilization. The inclusive-OR result
  is `1/2 + 1/2 - 1/4 = 3/4`; independence does not make events mutually exclusive.
- Pollen problem: equal initial gamete production, relative A-pollen success half that of a,
  unaffected eggs, random fertilization among successful gametes, and equal offspring survival.
  Successful-pollen frequencies are `1/3` and `2/3`. Offspring probabilities are
  `AA = 1/6`, `Aa = 1/3 + 1/6 = 1/2`, and `aa = 1/3`: ratio `1:3:2`.
- Illustrative pollen counts: 100 of each allele produced; 50 A and 100 a successful. These are
  one possible realization of the relative-success model, not a claim of measured survival rates.
- Conditioning warmup: Aa x Aa with equally likely gamete combinations; excluding aa leaves
  AA, Aa, and Aa, so the conditional heterozygote probability is `2/3`.
- Independence checkpoint: for known Aa x Aa parents, equal segregation, random fertilization,
  and independent offspring, three earlier aa outcomes leave the next aa probability at `1/4`.
  Notes distinguish this from using offspring evidence to infer unknown parental genotypes.
- Family problem: stipulate an affected `Hh` father, `hh` mother and other parent, no new mutation,
  and a simplified late-onset model in which young symptom absence is uninformative and H carriers
  eventually develop disease. The son's inheritance probability is `1/2`; his child's is `1/4`.
  `P(child H | son H) = 1/2`, whereas `P(son H | child H) = 1` under these assumptions.
  This corrects the reversed conditional in the original deck.

## Build and review

Build only this version:

```bash
source source_me.sh && python3 deck_tools.py build \
  genetics/LECT05/djot/lect05d-v2-probability_concepts.djot --format all
```

Artifacts are `output/odp/lect05d-v2-probability_concepts.odp` and
`output/pdf/lect05d-v2-probability_concepts.pdf`. A folder-wide Lecture 05 build includes both
the original and v2 as separate decks.

Validation on 2026-09-29: strict Jotdown and semantic lint pass; capacity inspection reports no
concerns. The final deck contains 53 slides with notes.
The initial sandboxed LibreOffice invocation aborted during macOS application registration;
the same repository build completed outside the sandbox.

Reviewed all pages as rendered contact sheets, with full-size checks of revised calculations,
tables, and summary. Shortened wrapping labels and exposed the normalization denominator on its
own slide. Checked note-only passages are absent from extracted PDF text. The deck uses manual
slide advances; attended classroom playback and timing were not tested. Content checks use
temporary verification; the later backend font-role change has focused behavior coverage.

Typography follow-up: fractions now use Unicode halves, quarters, thirds, and sixths, authored
with numeric character references in both slide content and notes. Strict lint and capacity
checks pass after rebuilding. PDF text extraction preserves all six fraction glyphs; full-size
render checks cover the addition equation, normalization calculation, and weighted square.

Final wrapping pass: shortened labels, placed pollen headings above the weighted tables, and
used wide, shallow family crosses (now slides 32-33). Plant labels use ovules/pollen. The original
41-page version was fully reviewed; the added count-first teaching sequence is checked below.

The backend selects ordinary, monospace, and condensed fonts. This deck contains no font-name
overrides. The PDF uses Atkinson Hyperlegible Next for ordinary text; LibreOffice supplies
missing Unicode glyphs from other fonts. A separate four-page specimen verifies all four styles
of Next, Mono, and IBM Plex Sans Condensed. The affected functional suite passes 196 tests.

Textbook terminology check: the 2001 [Introduction to Molecular Genetics and Genomics](../../genetics_textbooks/Introduction_to_Molecular_Genetics_and_Genomics-2001.md)
uses ovule/pollen labels for reciprocal crosses in Figure 3.4. The 2012
[Introduction to Genetics: A Molecular Approach](../../genetics_textbooks/Introduction_to_Genetics_A_Molecular_Approach-2012.md)
calls pollen the male gametes in Figure 14.4. Follow that teaching shorthand in this probability
lesson: slides 22-24 use Ovules/Successful pollen, without an egg/sperm anatomy sidebar.

Probability teaching follow-up: use natural-frequency reasoning before symbolic normalization,
then a two-slide question and answer that makes conditioning an explicit exclusion step. These
ideas follow the probability chapter of the local
[Genetics: Analysis of Genes and Genomes](../../genetics_textbooks/Genetics_Analysis_of_Genes_and_Genomes-2019.md).
The round-seed problems in Lectures 05E and 05G later reuse the same two-out-of-three reasoning.
The 43-page revision passes strict native lint and capacity checks. Rebuilt ODP/PDF and reviewed
slides 20-21 and 29-30 at presentation resolution, shortening the answer heading to avoid an
orphan word. Each of the 43 slides retains instructor notes.

Independence follow-up: the same textbook's Section 3.6 explains why earlier births do not
force later outcomes to balance a ratio. Adapt that lesson into an Aa x Aa vote and answer
on slides 41-42. The square represents possible outcomes for each offspring, not a quota
across four offspring. Notes connect this to the earlier conditioning example and explicitly
keep parental genotypes known. The final 45-slide revision passes strict native lint and
capacity checks; rebuilt PDF/ODP both have 45 pages, with 45 nonempty ODP note sections.
Reviewed both added slides at 1440-pixel resolution: no awkward wrapping, overlap, or clipping.

Cover follow-up: replace the tagline with Chapter 5 and Sept 29, 2026. The title now carries
only the lecture identifier, subject, chapter, instructor, and teaching date. The shared native
metadata frame has no fill and remains behind both editable text boxes after LibreOffice saves
the ODP. Rebuilt the deck and visually reviewed its title slide; all 45 slides still pass
strict native lint and capacity inspection. Direct mouse selection in Impress was not tested.

Rule-color follow-up: blue consistently marks addition/OR and orange marks multiplication/AND,
including general rules, mixed calculations, callbacks, and the final summary. Move unrelated
answer and gamete-frequency highlights to green. Rule section openers use white backgrounds
so both text colors stay readable. No slides were added. Rebuilt the ODP/PDF and visually checked
all 30 affected pages; strict lint and capacity checks pass. The same rule-color convention
extends to authored teaching text in the other relevant Lecture 05 decks.

Opening-question follow-up: slide 3 now states the full cross, unequal pollen success,
assumptions, and requested offspring ratio in complete sentences. A single wide panel keeps
the problem together; hints remain in notes. Rebuilt ODP/PDF and visually checked the revised
slide at 1600-pixel resolution. Strict lint and capacity checks pass; the deck remains 45 slides.

Deck-sequence follow-up: add an opening section heading on slide 3 and restore the separate
THE END slide. The full opening question moves to slide 4, the summary to slide 46, and
THE END is slide 47. Both new slides include notes. Rebuilt and visually checked the bookends;
source, ODP, and PDF counts match. The other Lecture 05 content decks follow the same opening
and closing structure, with optional early definitions where needed.

Student-review follow-up: keep all probabilities as fractions or the boundary values 0 and 1.
Remove percentage answer choices and callbacks; explain the result as three of four equally
likely outcomes. Expand the four-allele setup and independence definition into complete text.
Slides 46-48 now provide paragraph-based study references for rule choice, the pollen cross,
and conditioning, with notes directing the instructor to skip them during class. The summary
and THE END remain the last two slides, now 49-50. Strict native lint and capacity checks pass;
rebuilt ODP/PDF and visually reviewed all nine revised or added pages. Source and ODP contain
50 slides, and all source slides retain notes. Equations on the pollen reference stay together.

## Venn diagram sources

Slides 5, 8, 14, and 19 restore the original deck's visual explanations of union,
intersection, disjoint events, and double-counted overlap. The four authored SVGs are in
[assets/lect05d-v2-probability_concepts](assets/lect05d-v2-probability_concepts).
Neutral outlines define events B and C; blue shading marks the union, and orange marks
the intersection. Text labels identify every region without relying on color alone.
The geometry is schematic: area is not a probability measurement, and overlap does not
establish independence. Notes connect each diagram to the genetic examples.

The original deck's images 002, 003, and 006 supplied the conceptual visual reference.
Local construction references were `Mastering_SVG-2018.md`, sections "viewBox and viewport
in SVG" and "Clipping and masking", and `A_Handbook_of_Biological_Illustration-1988.md`,
"CLARITY". These are under the SVG creator skill's `references/local-only/` corpus,
in `svg_authoring/` and `scientific_illustration/`, respectively. They informed the common
800-by-450 coordinate system, clipped intersection, consistent outlines, and simple shading.

SVGs retain live Atkinson Hyperlegible Next labels, named groups, and accessible titles and
descriptions. The deck embeds the adjacent 2400-pixel PNG exports because its image-size
reader currently uses Pillow and cannot load SVG directly. Regenerate each PNG with:

```bash
rsvg-convert -w 2400 -o path/to/venn-union.png path/to/venn-union.svg
```

No backend changes were needed. The ODP retains the full-resolution PNGs; the existing PDF
export downsamples images to 100 dpi. Review the actual slide renders as well as the SVGs.

## Closing reference section

The closing Summary section starts on slide 46. Addition Rules (47) and Multiplication
Rules (48) repeat and consolidate the earlier cards into self-contained homework references.
Each includes the special and general forms, their conditions, and the explanation needed
to interpret them. The multiplication reference defines the conditional-probability bar and
shows both valid orders of the general rule. The three study explanations follow, then
the final takeaways and THE END. This follow-up adds three reference-section slides;
the live teaching sequence remains unchanged. Rebuilt and visually reviewed all three new
slides; strict native lint and capacity checks pass for the 53-slide deck.
