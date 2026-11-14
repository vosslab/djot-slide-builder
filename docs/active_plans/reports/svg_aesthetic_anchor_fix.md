# Signaling contact anchor correction

Corrected the protein, ligand, and receptor attachment ports to lie on the authored, un-stroked outlines. The original shapes, anchor names, activity states, and independent phosphate behavior remain intact. Center, membrane, and modification anchors are schematic sites and are not required to touch the contour.

Normalized coordinates (multiply x by width and y by height):

| Shape | Anchor | Coordinate |
| --- | --- | --- |
| Globular | input | (-.4625, .02125) |
| Globular | output | (.449609375, .00216796875) |
| Kinase | input | (-.455, .0825) |
| Kinase | output | (.41279296875, -.01228515625) |
| Ligand | input | (-.43, -.06) |
| Ligand | output | (.43359375, .00501953125) |
| Receptor | output, cytoplasmic | (.03015625, .45169921875) |

The remaining binding, receptor input, and extracellular ports were already on path endpoints. Changed points are exact endpoints or simple parameter values on the existing cubic segments. A regression checks every attachment port against its intended segment at two nonsquare dimensions.

Validation:

```sh
PYTHONPATH="$PWD:$PWD/tests" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest tests/test_svg_proteins.py tests/test_svg_signaling.py tests/test_svg_membranes.py -q
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B _temp/svg_aesthetic/anchor_fix/render.py
```

The tests passed (17 passed). Inspected `_temp/svg_aesthetic/anchor_fix/contacts.png` at its 520 × 210 native pixel size on white: the red markers for input, output and binding meet the rendered outline for all four shapes. The receptor output and cytoplasmic ports coincide, as do its input, binding, and extracellular ports. This focused inspection does not replace fresh independent specification and visual-quality reviews or verification of rebuilt compositions and native exports.
