# SVG drawing helpers

`drawing.py` supports small local drawing recipes with editable SVG fragments:

- `text(x, y, value, *, size, color, anchor="middle", font="Arial, sans-serif")`
  returns an editable SVG text fragment.
- `line(x1, y1, x2, y2, *, color, width=3, dash="")` returns a round-ended line fragment.
- `write_svg(path, width, height, title, description, body)` writes a complete SVG with
  a matching `viewBox`, accessible title and description, and finite positive dimensions.

Pass plain strings to labels and metadata: XML escaping is automatic. Unicode scientific
symbols become numeric character references in ASCII output and retain their displayed meaning.
The body is one string of trusted SVG markup; its groups, live text, definitions, and paths remain
editable. Reserve IDs `title` and `desc` for the document metadata. Malformed XML is rejected
before opening the destination. This is a writer for authored recipes, not an SVG sanitizer.

Keep subject geometry, arrow markers, colors, and scientific relationships in each recipe.
The helpers were extracted from repeated label/line/document code in the nucleotide and yeast
drawing recipes. No new dependency or command-line interface is needed.

## Constructing equipment

Three additional functions support the demonstrated cutaway electrophoresis chamber and pipette:

- `project(x, y, z)` returns `(x + 0.46*y, -0.36*y - z)`. Coordinates are schematic drawing
  units: x points right, y recedes up-right, and z points up. This fixed parallel oblique
  projection keeps depth edges parallel. Translate the enclosing SVG group to position the object.
- `cuboid(name, x, y, z, width, depth, height, *, colors, stroke, stroke_width=2)` builds
  the front, right and top faces from a lower-front-left corner.
- `cylinder(name, x, y, z, radius, height, *, colors, stroke, stroke_width=2, top_radius=None)`
  builds an upright circular part from its bottom center. Give a different `top_radius` for a
  tapered barrel, nozzle or tip. Its circular cap lies in the same projected XY plane as box tops.

Both solid functions return an editable group with `name` as its ID. Supply a unique ID, a
`(top, front, right)` three-value palette and an outline color. Attributes are XML-escaped.
Sizes must be finite and positive; origins must be finite and stroke widths nonnegative.
The cylinder side is a sampled schematic surface suitable for the demonstrated upright pipette
and terminal proportions. These helpers do not resolve intersections or hide other objects:
the recipe owns draw order, cutaways, transparency, materials and labels.

For example, the same coordinate system places a terminal beside a shallow tray:

```python
body = '<g transform="translate(30 180)">'
body += svg_tools.drawing.cuboid(
	"tray", 0, 0, 0, 200, 100, 12,
	colors=("#EDF8FC", "#C0DCE7", "#7DAABA"), stroke="#213547",
)
body += svg_tools.drawing.cylinder(
	"terminal", 180, 80, 12, 8, 65,
	colors=("#F6F8FA", "#BC382D", "#8B2921"), stroke="#213547",
)
body += '</g>'
svg_tools.drawing.write_svg(
	"_temp/tray.svg", 300, 220, "Tray and terminal",
	"Projected construction example in schematic units, not to scale.", body,
)
```

Use `project()` for local wells, buffer surfaces and electrode lines that must align with the
solids. Choose colors for each figure's meaning; the example palette is not a universal default.
The apparatus recipe and 1200/320-pixel review renders live in the local scratch directory
`_temp/svg_creative_refinements/construction/`. That demonstration does not establish engineering
accuracy or exported-slide acceptance.

## Example

Save this as `_temp/draw_example.py` and run it from the repository root with
`source source_me.sh && python3 _temp/draw_example.py`:

```python
import pathlib

import svg_tools.drawing

body = '<g id="signal">'
body += svg_tools.drawing.line(30, 65, 270, 65, color="#345B91", dash="7 6")
body += svg_tools.drawing.text(150, 40, "\u03b1 factor", size=24, color="#A43F77")
body += '</g>'
svg_tools.drawing.write_svg(
	pathlib.Path("_temp/signal.drawn.svg"), 300, 100,
	"Mating signal", "A label and line example, not a complete biological diagram.", body,
)
```

Preview with `rsvg-convert` from the repository root, keeping its output in `_temp/`:

```bash
rsvg-convert -w 900 _temp/signal.drawn.svg -o _temp/signal.png
```

Review actual renders at the intended display sizes. Follow
[the SVG diagram contract](../docs/slide-specs/SVG_DIAGRAMS.md) for labels, provenance,
`.drawn.svg` eligibility, and slide integration. The deterministic fixer for existing non-ASCII
source files is `tests/fix_ascii_compliance.py`; for SVG it preserves symbols using numeric XML
references. Run `source source_me.sh && python3 tests/fix_ascii_compliance.py -i PATH.svg`.

The drawing helpers are original to this project and use its MIT license.
