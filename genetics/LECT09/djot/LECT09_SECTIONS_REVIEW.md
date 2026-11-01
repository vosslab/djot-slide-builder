# Lecture 09 section revision

This records the divider-only revision. The later 09C story revision keeps 13 pages, retitles
its opening section, and reorders the examples; see [LECT09C_RESEARCH.md](LECT09C_RESEARCH.md).

Add conceptual breaks to the Lecture 09 content decks, using roughly one divider per ten
slides as a guide. Major sections use the existing dark Genetics surface; subsections use
a darker course-hue variant. All teaching slides retain their wording, order, layouts,
notes, images, equation markup, and fixed problem data.

## Current inventory

The 199 preceding slides become 213, including 24 section/subsection dividers.
The six C-H topic decks total 163 slides. Announcements and Lecture 10 are outside this revision.

| Deck | Before | After | Sections | Subsections | New Divider Pages |
| --- | ---: | ---: | ---: | ---: | --- |
| 09B | 46 | 50 | 4 | 2 | 3, 17, 24, 30 |
| 09C | 12 | 13 | 1 | 0 | 3 |
| 09D | 17 | 17 | 2 | 0 | None |
| 09E | 30 | 34 | 2 | 2 | 5, 12, 19, 23 |
| 09F | 24 | 25 | 2 | 1 | 10 |
| 09G | 42 | 43 | 2 | 3 | 34 |
| 09H | 28 | 31 | 2 | 1 | 4, 12, 19 |

09B's complete divider sequence is:

| Page | Layout | Teaching Phase |
| --- | --- | --- |
| 3 | Section | Hidden Double Crossovers |
| 7 | Section | Homework Problem |
| 17 | Subsection | Expected Doubles |
| 24 | Subsection | Interpret Interference |
| 30 | Section | Reading a Genetic Map |
| 37 | Section | Another Homework Problem |

The first worked example now separates counting observed doubles, predicting an independent
expectation, and interpreting the ratio. The outer-pair check leads directly into mapping
functions, chromatin, and genetic versus physical distance. The second example remains one
practice sequence, with its existing roadmap and complete answer.

09C gains an opening section. 09D's existing breaks already fit its short sequence. 09E
separates reading classes, connecting them to crossover histories, counting recombinant
spores, and correcting for hidden exchanges. 09F marks the transition from classification
and linkage to map distance. 09G adds map construction after its three pairwise estimates.
09H separates ordered-spore biology, the worked problem, and the half-weight calculation.
Dividers precede repeated roadmaps where appropriate; question/answer pairs stay together.

## Verification

- [x] Compare parsed slides with the saved baseline: all 199 preceding slides preserve content
  and order, including notes, colors, equations, tables, and question/answer pairs.
- [x] Preserve all 152 adjacent asset/data files byte-for-byte. Keep 09D's source and exports unchanged.
- [x] Pass strict native lint for seven masters, 213 slides, and 69 image uses. Typography audits
  have zero findings. C-H capacity checks pass; B retains its eight accepted 19 pt table advisories.
- [x] Rebuild six changed masters through the repository CLI, with LibreOffice outside the sandbox.
  Source/ODP/PDF counts agree. New dividers are native editable text; all 14 titles fit on one line.
- [x] Compare every retained PDF page's text and image count/placement with its prior page.
  Text is unchanged; the maximum image-box difference is 0.000 pt.
- [x] Review contact sheets for all 196 rebuilt pages and inspect every final new divider at
  full size. Check course colors, title fit, section hierarchy, and surrounding teaching flow.
- [x] Refresh current page ownership and catalog counts, record the human's pacing preference,
  and check edited documentation links and whitespace.

No new permanent tests, renderer changes, or dependencies. The full unrelated test suite and
physical classroom pacing/projection are untested; the existing small-table advisories remain.

Current page ownership is maintained in [LECT09_SOURCE_MAP.md](LECT09_SOURCE_MAP.md).
Earlier review documents describe their dated revisions and retain those page numbers.
Scratch evidence is under `_temp/lecture09_sections/`.
