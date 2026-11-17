# Gene tree C summary correction

The five bullets on slide 32 were shortened to clarify the cluster join, average, branch length, equal root-to-tip paths, and rate assumption. The new render fits within the frame with clear spacing; the manager also inspected and accepted it. No other source content was changed. The rebuilt PDF has 34 pages, and strict native lint passed (34 slides, 10 images).

Historical naming note: this November 14 record calls the source Lecture 11C. Its current source
path is `genetics/LECT11/djot/lect11d-upgma_weighted_averages.djot`; the output names below are
the original build artifacts.

Before rebuilding, the prior PDF and page renders were saved under `_temp/gene_tree_plain_english/summary_before/`. All pages were rendered again at 1200 pixels wide, and the C contact sheet was refreshed. Extracted PDF text differs only on page 32. Pixel comparison found page 25 identical; the other 32 unchanged-content pages have small pixel differences confined to their title text (including the centered divider and end titles), consistent with rendering variation. They are therefore not pixel-identical; the page 1 before/after renders were visually compared and show the same layout and text. No body-region pixel differences occurred outside page 32.

Commands:

```sh
PYTHONPATH="$PWD" MPLCONFIGDIR="$PWD/_temp/mplconfig" /opt/homebrew/bin/python3.12 -B deck_tools.py build genetics/LECT11/djot/lect11d-upgma_weighted_averages.djot --format all
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B deck_tools.py lint --require-native --native-executable /Users/vosslab/.cargo/bin/jotdown genetics/LECT11/djot/lect11d-upgma_weighted_averages.djot
pdftoppm -scale-to 1200 -png output/pdf/lect11c-more_gene_trees.pdf _temp/gene_tree_plain_english/lect11c-more_gene_trees/page
pdfinfo output/pdf/lect11c-more_gene_trees.pdf
pdftotext -layout output/pdf/lect11c-more_gene_trees.pdf _temp/gene_tree_plain_english/lect11c-more_gene_trees.txt
```

The build ran outside the sandbox as required for LibreOffice. These hashes supersede the initial C hashes in the build report:

```text
217a46ae307b467210f170b070c053718887a454a83a228e33dfe2ab00565771  output/odp/lect11c-more_gene_trees.odp
5d96767b1dc9984d23d9064cae6386ea325c64784713edc0876561980d2dbae0  output/pdf/lect11c-more_gene_trees.pdf
75130f1109c623db2d14642520c156d950c1448de23b4fcef8c5336230fc285d  docs/slide-specs/illustration_examples/gene_tree_lecture/lect11c.webp
```
