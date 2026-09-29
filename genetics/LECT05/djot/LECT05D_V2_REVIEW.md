# Lecture 05D v2 review

The 41-slide [lect05d-v2-probability_concepts.djot](lect05d-v2-probability_concepts.djot)
is a separate teaching revision of
[lect05d-probability_concepts.djot](lect05d-probability_concepts.djot). The original remains intact.
All questions, equations, tables, and allele labels are editable; all 41 slides have `@notes`.

## Teaching sequence

| Slides | Teaching job |
| --- | --- |
| 1-4 | Cover, objectives on slide 2, hard pollen challenge, OR versus AND |
| 5-15 | Addition rule, tempting 100% answer, square-based disproof, overlap correction |
| 16-18 | Derive multiplication from the same square; name independence |
| 19-27 | Return to pollen; normalize weights, fill the square, combine routes, solve the opener |
| 28-37 | Conditional inheritance; separate parent and child risks, reverse the condition, derive Bayes |
| 38-41 | Compare independence and exclusivity, exit question and answer, final summary |

Four multiple-choice votes occur on slides 9, 19, 32, and 35. Their answers are B, B, B, and D;
the following worked slides explain why. Slides 10 and 23 ask students to fill a square before
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
concerns. The exported ODP contains 41 slides and 41 note sections; the PDF contains 41 pages.
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
used wide, shallow family crosses on slides 30-31. Plant labels use ovules/pollen; slide 22 and
its notes identify the egg/sperm alleles. All 41 pages were reviewed again after rebuilding.

The backend selects ordinary, monospace, and condensed fonts. This deck contains no font-name
overrides. The PDF uses Atkinson Hyperlegible Next for ordinary text; LibreOffice supplies
missing Unicode glyphs from other fonts. A separate four-page specimen verifies all four styles
of Next, Mono, and IBM Plex Sans Condensed. The affected functional suite passes 196 tests.
