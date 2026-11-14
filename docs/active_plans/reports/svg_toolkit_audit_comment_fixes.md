# SVG toolkit comment cleanup

Added the repository's function separator before missing module-level functions, including before decorators where applicable. Added brief explanations of the fixed font measurement size and fallback bounds in `svg_tools/parts.py` and `svg_tools/text.py`. The fallback adds one em per missing glyph to each horizontal side and one em vertically; wrapping counts both horizontal sides. The allowance is conservative and does not guarantee bounds for every fallback typeface.

Changed toolkit modules: `parts.py`, `text.py`, `svg_import.py`, `icons.py`, `plots.py`, and `phenotypes.py`.

Changed examples: `allele_frequencies.py`, `annotations.py`, `array_comparison.py`, `build_gallery.py`, `cells.py`, `gene_features.py`, `genome_composition.py`, `icons.py`, `organelles.py`, `phenotypes.py`, `placement.py`, `plots.py`, `seed_cross.py`, `signaling.py`, `styled_text.py`, `svg_composition.py`, `text_labels.py`, and `yeast_mating.py`.

Verification: parsed 34 owned Python files before and after, removed docstrings from both ASTs, and compared the resulting trees: no executable changes. A token scan found no non-ASCII comments, and checks of all 76 module-level functions found no missing or duplicate separators. No tests were added or run for comment-only changes. Namespace mutation and gallery state findings remain outside this cleanup.
