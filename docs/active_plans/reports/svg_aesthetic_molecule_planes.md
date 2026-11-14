# Molecule tone-plane containment

The globular protein, kinase, ligand, and receptor retain their original outer paths, anchors, and APIs. Their former scaled and translated body copy could overhang concave boundaries. Each now has an authored lower-edge shadow that follows exact outer contour segments and closes inside the body; the upper-left highlights remain separate contained paths. No clip IDs are introduced.

The 500-samples-per-segment polygon probe at `_temp/svg_aesthetic/molecule_planes/containment.py` checked both shadow and highlight for each shape at 100 × 80 and 53 × 170. All sampled polygons were valid and outside areas were below 3e-15 square units. This is numerical sampling, not a formal curve proof.

White-background renders `_temp/svg_aesthetic/molecule_planes/proteins.png` and `signaling.png` were inspected: the silhouettes and binding notches remain legible, the planes stay within their outlines, and the shading reads as restrained volume in the example compositions.

Commands:

```sh
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B _temp/svg_aesthetic/molecule_planes/containment.py
PYTHONPATH="$PWD:$PWD/tests" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest tests/test_svg_proteins.py tests/test_svg_signaling.py tests/test_svg_membranes.py
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B -m svg_tools.examples.proteins
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B -m svg_tools.examples.signaling
```

The focused suite passed 17 tests. The two SVG examples were rasterized with CairoSVG at 2× on white for inspection. LibreOffice export and full-suite checks were not part of this workstream.
