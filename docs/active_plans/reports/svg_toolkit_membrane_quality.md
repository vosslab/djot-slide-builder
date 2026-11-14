# Membrane toolkit quality review

**PASS** against the M10 membrane specification, based on the current implementation and the fresh render below. `svg_tools/signaling.py` draws two circular heads and four tail paths per sample, with tail endpoints at `±0.04 * thickness`; strokes leave a visible central separation. The sample tangent rotates each lipid pair on the curved centerline. Inclusive gap intervals omit center samples, and the docstring tells callers to allow for painted heads and strokes. The five named anchors describe the path endpoints, midpoint, and the two midpoint sides. A rotation-independent circular envelope including stroke provides conservative bounds around the placed samples. The direct implementation is proportionate to the requested feature.

The selected fresh tests passed: `/opt/homebrew/bin/python3.12 -B -m pytest --noconftest -q tests/test_svg_membranes.py` (2 passed). They check leaflets, tail endpoints, a gap, anchors, bounds, a curved midpoint, and invalid gap rejection. They do not exhaustively test arbitrary curves or gap geometries.

Visual review: `_temp/svg_toolkit/membrane_quality/membranes.webp` (1200 × 810, white background, WebP quality 90). At slide scale, both strips read as opposing leaflets with paired tails and a visible central gap; the straight and curved examples have clear receptor openings, and no clipping is apparent. The curved strip follows its centerline and remains legible. The image uses the example's geometry, rendered with `PANGOCAIRO_BACKEND=fc rsvg-convert` and flattened with Pillow.

Limits: SVG raster rendering was reviewed; no native slide export or full test suite was run. Extreme curvature and user-selected spacing may cause neighboring lipid shapes to overlap; the caller controls these values.
