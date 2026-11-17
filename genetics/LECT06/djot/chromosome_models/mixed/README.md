# LECT06 preserved artwork and chromosome models

`make_chromosome_mixed.py` in the owning Djot directory regenerates seven SVG assets
using these frozen inputs and `svg_tools.chromosomes`. Run it from the repository root:

```sh
source source_me.sh && python3 genetics/LECT06/djot/make_chromosome_mixed.py
```

Each family contains its body geometry in a named `_recipe.py` or `_recipes.py` module
and immutable source artwork in `sources/`. Original SVGs retain the source labels, callouts, molecular images,
and layout. Cleaned PNG layers replace only measured chromosome body regions;
the corresponding mask PNGs preserve the preparation boundaries. The overview
also retains the original raster rendering used to measure those boundaries.
Crossovers keeps its original embedded images and applies a local white mask
under the separate molecular inset.

`frozen_input_hashes.json` records original and prepared input SHA-256 hashes.
`provenance.json` maps originals and reviewed candidate hashes to owning asset
destinations. Its `candidate` paths identify the reviewed staging outputs and
are provenance only; regeneration never reads them. Source cleanup was prepared
and visually reviewed before freezing. Runtime generation performs no inpainting
or image manipulation and needs no OpenCV dependency.

The generator creates missing asset directories and writes only the seven SVG
assets. It does not read existing production assets or create previews, audit
reports, temporary files, or bytecode caches when run through the repository bootstrap.
