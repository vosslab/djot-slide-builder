# SVG aesthetic final code specification review

**FAIL: molecule inset shading protrudes beyond the silhouette.** The M3 outline cap,
M5 organelle topology, M7 contact points, M13 plot dispatch, and protected-original
checks pass the scoped code review. This is not visual-quality or native-slide acceptance.

## Required correction

`svg_tools/signaling.py` constructs the inset plane by scaling the silhouette to 92%
then shifting it up and left. For concave silhouettes that operation does not guarantee
containment. An independent 100-point-per-segment polygon approximation at 100 by 80
reports outside areas of 8.52 square units for globular, 14.21 for kinase, and 157.24
for receptor; at 53 by 170 it reports 9.59, 16.01 and 177.10 respectively. The visual
style contract requires shade planes inside the silhouette. The ligand inset and the
separate molecule highlights passed this sampled check. Clip the inset to the outer
silhouette or use contained authored geometry; preserve contact anchors and test the
resulting containment. Recheck composed renders after the correction.

```sh
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B _temp/svg_aesthetic/code_spec/containment.py
```

These are sampled area estimates, not exact analytic curve intersections. They establish
an actual protrusion but not its slide-size visual severity.

## Passing checks

- The shared outer outline is uniform in final coordinates, round capped and joined,
  proportional for small parts and capped at 3 units. The existing test covers a 200 by
  50 part and a 500 by 340 container. The two cell shade planes were sampled against
  their silhouettes, including the inner plant boundary; no protrusions were found.
- The signaling contact regression checks globular, kinase, ligand and receptor contact
  anchors on their intended cubic segments at 100 by 80 and 53 by 170. The anchor names
  and independent activity/phosphate behavior remain available. These are schematic
  attachment sites, not claims of experimentally determined molecular geometry.
- The mitochondrial outer and inner membrane paths are each continuous and closed; the
  focused topology test checks no self-intersections, no envelope intersection, multiple
  fold crossings and cardinal contacts. Inspection of the owner's fresh render shows
  connected folds and open spaces. The chloroplast has three groups of 4/5/4 flattened
  sacs and two lamellae connecting the stacks; those counts are explicitly schematic.
  ER, Golgi and generic vesicle distinctions are retained.
- `build_gallery.build` supplies `source_path` explicitly to the plots recipe, and
  restores the caller's working directory in `finally`. Its regression dispatches the
  real plot recipe while `sys.argv` contains `--output-dir`; caller-state tests exercise
  success and renderer failure without mutation of the imported curve module's file path.
  Namespace collision coverage remains in the focused suite.
- The DNA original and six earlier pilot originals match the baseline hashes below.
  The reviewed source uses locally authored paths; no Servier geometry ingestion was
  identified. Source inspection cannot itself prove independent authorship.

Focused SVG lane, run after the organelle owner declared the source stable:

```sh
mkdir -p _temp/svg_aesthetic/code_spec
PYTHONPATH="$PWD:$PWD/tests" MPLCONFIGDIR="$PWD/_temp/mplconfig" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest --basetemp="$PWD/_temp/svg_aesthetic/code_spec/pytest" tests/test_svg_*.py tests/test_djot_includes.py -q
```

Result: **125 passed in 2.32s**. This run predates any subsequent shading correction.

## Protected originals: current SHA-256

```text
2059903ad86b5aade0249c7ab7d84f6029de0d5f9de52368265bb0d6fc7d6b52  genetics/LECT03/djot/assets/lect03f-whole_genome_analysis/human_genome_composition.plot.svg
b739fac24f49ab7009298acf2a6dbbffd44dfdfef45ab7559a038c1582663f64  genetics/LECT11/djot/assets/lect11d-chromo_alter_1-deletions/array_comparison_workflow.drawn.svg
bebcfacff1292dcdcf9db63a6774bcf4cebbe95a1922dfce6873dc18d17fb05a  genetics/LECT09/djot/assets/lect09d-yeast_unordered_tetrads/yeast_mating.drawn.svg
a4c48c8f2d75c8d41af3abe53ca878acd44ab4e0dda474ae646dd95f7ca0567f  genetics/LECT09/djot/assets/lect09d-yeast_unordered_tetrads/yeast_diploid.drawn.svg
3de072b6d7cc350dc8daf5a397eb52a96fc10276744f55abb3748b449eed0986  genetics/LECT04/djot/assets/lect04g-indep_assort/dihybrid_seed_phenotypes.drawn.svg
a7cc2655e78ca5c3590675360acffe7cfdd8e50a6ff2889748d23c4bdcc09204  biotech/LECT04/djot/assets/lect04c-talking_points_set_3/western_detection_detail.drawn.svg
5559e48a7ccab780408bb402d8585c134667a10cce47e785d38a8c9b2cc037ba  genetics/LECT02/djot/assets/lect02d-dna_structure_overview/b_dna_helix.drawn.svg
```

Each equals `_temp/svg_aesthetic/baseline/manifest.json`. Bounds were inspected in the
changed families and exercised by focused tests; no exhaustive claim is made for every
possible dimension and input. Final regeneration, independent visual review, and native
export review remain pending. No Git, `source_me.sh`, LibreOffice, or full base suite was
run by this reviewer.
