# Lecture 09H Artwork and Definitions Review

Use the instructor-updated ordered-centromere generator artwork and add opening definitions
for FDS, SDS, and spore. Include ascus to distinguish the sac from its contents. Preserve the
fixed problem, all original teaching content, and the question/answer sequence.

## Page changes

09H grows from 27 to 28 visible pages. The new definitions slide is H3, after the objectives.
Former H3-27 shift forward one page. No existing slides are removed or split.

| Current Page | Figure or Content |
| --- | --- |
| 3 | New terms: spore/ascospore, ascus, FDS, SDS. Blue FDS and orange SDS match the class table. |
| 7 | Refreshed 4:4, 2:2:2:2, and 2:4:2 figures with matching colored definition terms. |
| 11 | Refreshed four-product/eight-spore figure; pair brackets follow measured spore bounds. |
| 12 | All six refreshed generator patterns and original counts. |
| 14-15 | Refreshed question/classified tables; retain static answer reveal and every class/count. |

## Artwork and data

Call the current generator's `generate_html_for_pattern` for each saved pattern, using its
current default allele palette. Save the exact HTML and capture all six asci at 3x CSS
resolution as quality-90 WebP. Embed those captures in the existing SVG figures, keeping
live set/count/class labels, headers, block lengths, and brackets. Preserve native slide prose.

The current ascus is 423 by 62 CSS pixels; capture size is 1269 by 186 pixels. Scale both axes
equally and center the drawing within each existing row. Recalculate the four pair brackets
from the actual eight spore cells, rather than the previous artwork's coordinate assumptions.
The allele colors are schematic and are still explained in the slide captions.

The source, function, and capture hashes are recorded in
[ordered_problem_data.json](assets/lect09c-tetrad_worked_examples_bpw/ordered_problem_data.json).
The numeric problem keeps its original generator revision and reproducibility record;
the updated artwork has separate working-tree source identification. The exact current
markup is [ordered_generator_art.html](assets/lect09c-tetrad_worked_examples_bpw/ordered_generator_art.html).

Keep all six sequences and counts: 188/39/44/30/37/162. Sets 1/6 are FDS, while 2/3/4/5 are
SDS. The original sums remain 350 FDS + 150 SDS = 500 asci; half of 30% gives 15 cM.
The centromere-origin half-weight diagram, map, original mechanism figures, photographs,
references, roadmap, cover metadata, and all other decks remain unchanged.

## Verification

- [x] Independently classify each sequence by run lengths, check identical mitotic pairs,
  and recompute the sums and distance with exact fractions.
- [x] Match every HTML allele sequence to the fixed data; embed the exact new capture bytes.
- [x] Preserve all original prose and equations after accounting for the new slide and term colors.
- [x] Validate SVGs, unique IDs, table states, image proportions, row bounds, and pair brackets.
- [x] Reconcile source/ODP/PDF counts at 28, with no replacement markers.
- [x] Pass strict native lint, zero typography/capacity findings, existing SVG/definition tests,
  and the 09H cover test. No new permanent tests or dependencies.
- [x] Inspect all 28 exported pages and the affected definitions/figures at full size.
- [x] Update the source map, course catalog, guidance, design record, and changelog.

Evidence is in `_temp/ordered_h_update/`: baseline sources/PDF, capture measurements and
artwork, one-time authoring, independent verification, build/test logs, and quality-90 review
WebPs. Ordinary builds use the saved assets; the generator and browser are not needed.
Physical classroom projection and pacing remain untested.
