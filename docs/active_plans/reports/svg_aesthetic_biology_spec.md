# Biological aesthetic specification review

**FAIL**: signaling contact ports miss intended molecular contours, and the
mitochondrial inner membrane is open.
This is a fresh specification review, not visual-quality or native-slide acceptance.

## Finding: protein contact anchors miss the silhouette

In `svg_tools/signaling.py:125` and `:133`, the globular and kinase input and
output coordinates were retained as composition points while their locally
authored contours were reshaped. For a 100 by 100 part, the globular input is
2.178 drawing units inside the nearest outline, kinase input 1.550 units inside,
and kinase output 2.114 units outside. The outline is 2 units wide, so the kinase
output is 1.114 units outside its painted stroke. Joining another object exactly
at that output leaves a gap; using an inside port overlaps the shape rather than
meeting its boundary. The receptor output/cytoplasmic anchor at line 228 is
1.457 units inside. By contrast, the checked protein binding and receptor input
anchors lie on their outlines. The current tests in `tests/test_svg_proteins.py:13`
check that anchors are in bounds, not that contact ports meet their silhouettes.

Reproduce with:

```
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B _temp/svg_aesthetic/biology_spec/port_distances.py
```

Nearest points were found independently against each Bezier segment; a sampled
closed-contour point-in-polygon check determined which side of the contour each
port occupies. Keep the public anchor names and their intended scientific roles;
make the authored geometry and anchors meet and add a behavior-level contact
check. Recheck actual composed assets after a fix. Generic internal anchors and
phosphate modification sites are not asserted to be boundary contacts.

## Finding: mitochondrial inner membrane is open

In `svg_tools/cells.py:116`, the inner membrane feature is a single open path:
it starts at normalized `(-.31, -.19)`, runs around the right and lower
perimeter, then follows the folds to `(.30, 0)` without closing. Its first
endpoint is left unattached. The open endpoint is visible in
`_temp/svg_aesthetic/cells/organelles-review.png`, where the inner structure
reads as an ellipse and a wave rather than a continuous folded membrane.
Revise the path topology to form a continuous inner membrane with recognizable
connected cristae, preserving the outer envelope and open fold spaces; inspect
the resulting render and test the meaningful topology rather than freezing a
path string.

## Evidence checked

- Read `docs/active_plans/active/svg_aesthetic_plan.md`,
  `docs/SVG_VISUAL_STYLE.md`, and family reports for cells, signaling, genetics,
  binding and phenotypes. Inspected family source, recipes and focused tests.
- The membrane construction in `svg_tools/signaling.py:20` places head circles
  on opposite outer faces with tails toward the center, samples the supplied
  curve and omits inclusive gap samples. The example's receptor is placed in a
  deliberate gap. Phosphate and activity are independent in code and tests.
- Binding part terminals are on their contours; `tests/test_svg_binding.py`
  checks coincident named target/Fab/Fc/enzyme contacts in both compositions.
  The phenotype recipe retains eight seeds, yellow/green and round/wrinkled
  associations, and the 9:3:3:1 proportions. The flower is explicitly generic.
- The chromosome tests cover 44 source cytobands, sisters, model identity,
  deletion and reciprocal translocation; `svg_tools/chromosome_examples.py:262`
  builds the q31 crop from the same rendered whole via an isotropic transform.
  Gene tests cover exon order, lengths, gaps, colors and landmark direction.
- Inspected `_temp/svg_aesthetic/cells/organelles-review.png` and current
  `svg_tools/cells.py`: the ER cisternae have alternating connections, Golgi
  sacs remain separate, chloroplast stacks have links, mitochondrial folds
  are open as described above, and generic vesicles contain no invented contents.
  Nuclei and other contents remain separately authored. Fused yeast uses one
  continuous closed envelope. This is a schematic-anatomy check, not an
  assessment of visual polish.
- Recomputed SHA-256 against `_temp/svg_aesthetic/baseline/manifest.json`:
  all seven protected originals, including the LECT02 DNA illustration, match.
- Ran:

```
PYTHONPATH="$PWD:$PWD/tests" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest tests/test_svg_cells.py tests/test_svg_organelles.py tests/test_svg_membranes.py tests/test_svg_proteins.py tests/test_svg_signaling.py tests/test_svg_binding.py tests/test_svg_phenotypes.py tests/test_svg_chromosomes.py tests/test_svg_gene_tracks.py tests/test_svg_gene_features.py -q
```

  Result: **30 passed**. Passing tests do not resolve the port finding.

No external images or paths were found in the inspected family implementations;
local authorship is also stated by their owners, but authorship cannot be proved
solely from the generated paths. Bounds were reviewed in the touched code and
focused tests, not exhaustively verified for every possible input. The separate
quality review, regenerated gallery and native exports remain outside this review.
