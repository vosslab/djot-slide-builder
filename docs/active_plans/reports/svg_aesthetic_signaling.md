# Membrane and signaling visual update

Implemented in `svg_tools/signaling.py`: authored curved lipid tails and four distinct schematic molecular silhouettes; flat lower depth and upper-left highlights; baked dimensions and uniform rounded ink outlines. Leaflet placement, gaps, centerline orientation, receptor membrane anchor, state annotations and phosphate independence remain supported. Binding and modification anchors are schematic composition points, not structural claims. No Servier geometry was used.

Checks:

```sh
PYTHONPATH="$PWD:$PWD/tests" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest tests/test_svg_membranes.py tests/test_svg_proteins.py tests/test_svg_signaling.py -q
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B -m svg_tools.examples.membranes
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B -m svg_tools.examples.proteins
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B -m svg_tools.examples.signaling
/opt/homebrew/bin/python3.12 -B _temp/svg_aesthetic/signaling/render.py
```

Focused tests: 9 passed. CairoSVG previews inspected at native size and 50%: `_temp/svg_aesthetic/signaling/{membranes,proteins,signaling}_{actual,reduced}.png`. No clipping found; text and symbols remain recognizable at 50%, though small labels benefit from larger display. Existing example scripts write SVGs to `_temp/svg_toolkit/`. Canonical gallery exports are reserved for integration.

Construction references: local SVG creator corpus, *A Handbook of Biological Illustration*, "Size and Reduction of Illustrations for Publication" (lines 207-216), for reduced-size review; *Mastering SVG*, "viewBox and viewport in SVG" (lines 635-648), for viewport awareness. These informed construction and verification, not copied shapes. No LibreOffice or full suite run.
