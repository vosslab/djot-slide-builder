# Genetics gene-tree C: fresh source specification delta

Status: **PASS**, November 14, 2026, for the frozen C source delta and its connected instructional sequence. The earlier [full specification review](genetics_gene_tree_spec_review.md) remains the baseline; this is not a new visual or migration review.

- The three update prompts show the current native lower-triangle matrix alongside the question: [first](../../../genetics/LECT11/djot/gene_tree_five_steps.djot#L43), [second](../../../genetics/LECT11/djot/gene_tree_five_steps.djot#L114), and [third](../../../genetics/LECT11/djot/gene_tree_five_steps.djot#L193). Their matrix values and group identifiers match the corresponding preceding merge states; the group and left panel remain consistent. Cluster membership follows the established concatenated labels, explained before the walkthrough with a hypothetical example in [the master](../../../genetics/LECT11/djot/lect11d-more_gene_trees.djot#L55). The updates can be calculated from the displayed values and cluster sizes without recalling earlier numbers.
- Each update answer follows its question. In particular, [the 20 versus 20.5 prediction](../../../genetics/LECT11/djot/gene_tree_five_steps.djot#L132) precedes [the correct weighted answer 20](../../../genetics/LECT11/djot/gene_tree_five_steps.djot#L142). All four merge prompts precede their answers; their distances, heights and eight branches agree with the [independent math contract](genetics_gene_tree_math.md#L55). The other eight merge answers remain covered by the original full review.
- [The root-to-tip prompt](../../../genetics/LECT11/djot/gene_tree_five_steps.djot#L256) displays the completed height-labeled tree. Node heights 2, 4, 6 and 11 provide branch differences 2, 2, 7 and 6, 5 for paths to a and d; both total 11. The explicit answer follows at [the check](../../../genetics/LECT11/djot/gene_tree_five_steps.djot#L294). The fitted a-to-e example is only introduced later; no question asks for that value before it.
- The generator confines these layout changes to five-gene output in [gene_tree_recipes.py](../../../genetics/LECT11/djot/gene_tree_recipes.py#L120), with the root prompt similarly conditional at line 143. This inspection did not rerun the generator or alter production files.

## Evidence and boundary

`shasum -a 256 -c _temp/gene_tree_refresh/c_inputs_source_frozen.sha256` returned OK for all three files:

- `gene_tree_examples.py`: `edadf90c2e093b8d6ed4f2c65c5075914f0df12ed4aa45c60408a5e858fb3bcf`
- `gene_tree_five_steps.djot`: `a9586ffe09a355c513cf7bab009bd58409393463c766acf3617c13f8590804c8`
- `lect11d-more_gene_trees.djot`: `240115879f9def321ce1b49108c1d23dc5dbb7f8c31d284e52471a5a1683ed03`

Read the plan, prior specification and math reports, changed generator and C source, and the completed SVG's text and paths. No test or LibreOffice export was run. Actual slide rendering, readability, shape position, all-page visual quality, byte-preservation and migration remain for the separate quality and integration reviews.
