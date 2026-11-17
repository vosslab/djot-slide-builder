# Gene tree plain-English build evidence

The B, C, and D masters were freshly built in sequence on 2026-11-14. All three builds succeeded; PDF page counts are 36, 34, and 32, respectively. Source-level specification review is recorded separately in [the specification report](genetics_gene_tree_plain_english_spec.md). See the completed [quality](genetics_gene_tree_plain_english_quality.md) and [integration](genetics_gene_tree_plain_english_integration.md) reviews.

## Checks

- Focused tests: 47 passed. Strict native lint: 3 sources, 102 slides, 40 images; passed. Capacity command completed without warnings for each master. Build logs contained no capacity, replacement, or error warnings.
- Native ODP XML contains 9, 13, and 15 tables respectively, including the matrices. PDF text extraction returned 6,487, 6,633, and 5,365 characters, respectively; this establishes extractable text, not manual selection of every element. No `@replaceme` marker appeared in the extracted text or three masters.
- Rendered every page at 1200 pixels wide under `_temp/gene_tree_plain_english/lect11b-gene_trees/`, `lect11c-more_gene_trees/`, and `lect11d-gene_tree_activity/`. Contact sheets are [B](../../slide-specs/illustration_examples/gene_tree_lecture/lect11b.webp), [C](../../slide-specs/illustration_examples/gene_tree_lecture/lect11c.webp), and [D](../../slide-specs/illustration_examples/gene_tree_lecture/lect11d.webp), white-backed WebP quality 90. Inspected all three contact sheets and D page 24 at full render size: the example displays the selected lower-triangle cell and new tree branches together. Final quality judgment is reserved for the independent review.
- Original source PDFs were not modified. Known inherited E and chromosome defects remain outside this scope. No live classroom use was checked.

## Commands

The following build was run for each of `lect11b-gene_trees`, `lect11c-more_gene_trees`, and `lect11d-gene_tree_activity`, sequentially outside the sandbox because it invokes LibreOffice:

```sh
PYTHONPATH="$PWD" MPLCONFIGDIR="$PWD/_temp/mplconfig" /opt/homebrew/bin/python3.12 -B deck_tools.py build genetics/LECT11/djot/<deck>.djot --format all
PYTHONPATH="$PWD" MPLCONFIGDIR="$PWD/_temp/mplconfig" /opt/homebrew/bin/python3.12 -B deck_tools.py capacity genetics/LECT11/djot/<deck>.djot
pdftoppm -scale-to 1200 -png output/pdf/<deck>.pdf _temp/gene_tree_plain_english/<deck>/page
pdfinfo output/pdf/<deck>.pdf
pdftotext output/pdf/<deck>.pdf _temp/gene_tree_plain_english/<deck>.txt
```

```sh
PYTHONPATH="$PWD:$PWD/tests" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest tests/test_table_styles.py tests/test_layout_tables.py tests/test_gene_tree_examples.py -q
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B deck_tools.py lint --require-native --native-executable /Users/vosslab/.cargo/bin/jotdown genetics/LECT11/djot/lect11b-gene_trees.djot genetics/LECT11/djot/lect11d-more_gene_trees.djot genetics/LECT11/djot/lect11e-gene_tree_activity.djot
```

The [C slide 32 correction](genetics_gene_tree_plain_english_summary_fix.md) supersedes the initial C hashes below; B and D remain accepted.

## SHA-256 (initial build)

```text
878f3f73b989eaf10b351b042e647e398bd790548d37e780137d1a6759801503  output/odp/lect11b-gene_trees.odp
762c81e7b68162fd085248c2e424c943d89adec3845e712d1fdb0974121d87b5  output/odp/lect11c-more_gene_trees.odp
d26ba54ac6b89aeaec6ee2b093b5c1122c54e0b34d8f2a603f182998564df9f0  output/odp/lect11d-gene_tree_activity.odp
06563e7afa2852d509ea34dc0616c1369df1d128e830115e3b46293961273072  output/pdf/lect11b-gene_trees.pdf
6bad45b5745b1a1766f3217cc3a2debd85129cee589ea072619d799b62e5ee27  output/pdf/lect11c-more_gene_trees.pdf
10d74e6a3596e6df8b008d67996b6c473e82b884ad53e4534098f5b694f6239c  output/pdf/lect11d-gene_tree_activity.pdf
cee7b2ed796736dce61690fe67c368f234bc6ee760d248911990e71a8897bf54  docs/slide-specs/illustration_examples/gene_tree_lecture/lect11b.webp
d2675835625deee57c766dbcbba2d9c13c1de3827405c2c7fc60cdb9de89d4b9  docs/slide-specs/illustration_examples/gene_tree_lecture/lect11c.webp
4ac6f07852545593ba9193cae2aebb2ff1dd48ce7255fbe8724fc45f3ef4eea7  docs/slide-specs/illustration_examples/gene_tree_lecture/lect11d.webp
```
