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

## Single-chromatid chromosomes

`chromosomes.chromosome_svg(name, genes, *, centromere_after=None, junctions=(),
pitch=64, height=62, allele_labels=False)` returns `(fragment, width, boundaries)`. Give each fragment a
document-unique XML-safe `name`, and supply ordered `(label, "#RRGGBB")` pairs.
Empty labels draw an unlabeled rod. The returned boundary coordinates are indexed
by the number of preceding regions; use them to position cut arrows without
reconstructing the geometry. At a centromere boundary the coordinate is the
collar center. Placement belongs to an enclosing SVG transform.

`centromere_after=5` inserts a pale outlined, slightly narrowed collar after the
fifth region. `None` deliberately draws no centromere. Explicit `junctions=(3,)`
adds a white zigzag after region three; a join cannot occupy the collar boundary.
Neutral rounded endcaps are illustrative chromosome ends, never extra genes.
Subtle irregular bands are decorative, not measured G-bands. Region spacing is
schematic; deletion and duplication change width when the number of regions changes.
Keep colors attached to source segments through rearrangements. Labels remain
flat editable Atkinson Hyperlegible Next text; XML escaping is automatic.

Opt in to `allele_labels=True` for one lowercase ASCII gene letter followed by
`+` or `-`, such as `a+` or `b-`. It renders a live italic gene and raised sign;
minus uses the readable mathematical minus. Empty labels still represent unlabeled
arm material, never an additional gene. Unsupported allele labels raise `ValueError`.
Ordinary labels are never automatically reinterpreted. The specimen includes both modes.

The helper adapts the established BPQ HTML/CSS chromosome vocabulary into native
SVG: continuous outlined rods, terminal treatment, pale collars and explicit joins.
It draws straight single chromatids. Replicated/X shapes, curved pairing diagrams,
measured cytological band maps and internal telomere distractors need separate
source-specific construction; they are not supported by this helper.

The durable recipe is [chromosome_examples.py](chromosome_examples.py). From the
repository root, run Python 3.12 directly (no bootstrap or Git invocation):

```bash
/opt/homebrew/bin/python3.12 -B -m svg_tools.chromosome_examples
```

It writes the [specimen](../docs/slide-specs/illustration_examples/chromosome_language.drawn.svg)
and four review candidates under `_temp/chromosome_visual_language/implementation/`.
It does not overwrite course assets. The recipe contains the explicit source gene
orders, colors and cut positions; all chromosome geometry comes from the shared helper.
See the [illustration guide](../docs/slide-specs/GENETICS_ILLUSTRATION_GUIDE.md)
for the scientific meanings and review boundary.

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
