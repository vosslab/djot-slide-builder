# Chromosome and gene-track aesthetic pass

The existing chr7 v2 specimen already provides the approved matched single chromatid, sisters and literal q31 crop. The broad hollow marker leaves the acen fills visible. No geometry, interval, stain, per-chromatid width, orientation, label position, crop or caption change was justified by the baseline. The original 44 hg38 rows remain the source; the CFTR caption identifies a band rather than a gene interval.

- `svg_tools/chromosomes.py`: increased the broad hollow marker stroke from 0.035 to 0.045 of chromatid body height. Its fill, bounding box and contour remain unchanged.
- `svg_tools/gene_tracks.py`: gave exon outlines a 0.05-height stroke, introns a subordinate 0.03-height stroke, and updated the part's painted margin accordingly. Label sizing now caps at 0.45 of height and estimates character width, producing consistent sizes for labels that fit while retaining width fitting for narrow blocks. Operon arrows and landmarks retain their existing simple flat shapes and anchors.
- `svg_tools/chromosome_examples.py` and `svg_tools/examples/gene_features.py` needed no changes. No DNA helix generator or existing DNA SVG was modified.

Scientific illustration reference: `references/local-only/scientific_illustration/Preparing_Scientific_Illustrations_a_Guide_to_Better_Posters_Presentations-1996.md`, around line 771, recommends distinguishing information with line weight and label size. The output uses the repository's editable SVG fragments and live Atkinson Hyperlegible Next labels; source-based bands and schematic shapes remain distinct in meaning.

Proofs: `_temp/svg_aesthetic/genetics/chr7-before.png`, `chr7-after.png`, `chr7-reduced.png`, `gene-before.png`, `gene-after.png`, `gene-reduced.png`, with corresponding before/after SVG files. Inspected 1200/600 px chromosome and 1000/500 px gene-track renders using `PANGOCAIRO_BACKEND=fc rsvg-convert`; reduced views remain legible at their intended overview scale. Exon details should be displayed larger when they are the teaching focus.

Checks: focused `tests/test_svg_chromosomes.py tests/test_svg_gene_tracks.py tests/test_svg_gene_features.py` passed (14 tests). A parsed before/after chr7 comparison found exactly two changes, the single and sister marker stroke widths (2.24 to 2.88); all other XML attributes, elements and text matched. The source map was checked for 44 contiguous rows and two acen rows. This is rendered inspection and focused structural verification, not slide export or independent biological review.
