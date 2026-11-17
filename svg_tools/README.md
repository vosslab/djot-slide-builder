# SVG drawing helpers

For the complete task-oriented API catalogue, see [SVG toolkit](../docs/SVG_TOOLKIT.md).
The [visual style guide](../docs/SVG_VISUAL_STYLE.md) and [gallery](../docs/slide-specs/illustration_examples/svg_toolkit/index.webp)
show the shared illustration direction. Servier Medical Art is a style reference only; author
all geometry locally. Preserve the original Genetics LECT02 B-DNA illustration unchanged.

See [SVG_TOOL_ROADMAP.md](../docs/SVG_TOOL_ROADMAP.md) for the 1,039-path repository SVG inventory and reuse-aware priorities: cells,
flowchart parts, and extensions to gene tracks.

`drawing.py` supports small local drawing recipes with SVG fragments:

- `text(x, y, value, *, size, color, anchor="middle", font="Arial, sans-serif")`
  returns an SVG text fragment.
- `line(x1, y1, x2, y2, *, color, width=3, dash="")` returns a round-ended line fragment.
- `write_svg(path, width, height, title, description, body)` writes a complete SVG with
  a matching `viewBox`, accessible title and description, and finite positive dimensions.

Pass plain strings to labels and metadata: XML escaping is automatic. Unicode scientific
symbols become numeric character references in ASCII output and retain their displayed meaning.
The body is one string of trusted SVG markup. Reserve IDs `title` and `desc` for the document
metadata. Malformed XML is rejected
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

Both solid functions return a group with `name` as its ID. Supply a unique ID, a
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

## Chromosome drawing tool

Use [chromosomes.py](chromosomes.py) for schematic segments, colors, sizes, independently
constructed sisters, condensation, and source-backed named cytobands. Follow the all-course
chromosome authority in [SVG_VISUAL_STYLE.md](../docs/SVG_VISUAL_STYLE.md#chromosome-family-authority):
BPQ black body outlines, modestly rounded gray ends, gene labels, and labelable rectangular
centromeres. Production recipes compose shared bodies rather than defining silhouettes. Segment
colors retain source identity independently of course accent hues.

```python
import pathlib

import svg_tools.drawing
import svg_tools.chromosomes

pathlib.Path("_temp").mkdir(exist_ok=True)
rod = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment("", "#00775F"),))
layout = svg_tools.chromosomes.render_chromosome_layout(
	"plain", rod, length=300, thickness=50, bands=False,
)
svg_tools.drawing.write_svg("_temp/plain.drawn.svg", layout.width + 20, layout.height + 20,
	"Plain chromosome", "A schematic single chromatid.",
	f'<g transform="translate(10 10)">{layout.svg}</g>')
```

`Segment(label, color, length=64)` takes a six-digit hex fill and positive finite
schematic length. `Chromosome(segments, centromeres=())` keeps region order and accepts
`Centromere(after, active=True, label=None)` sites, including terminal sites. Biological
bands are explicit colored segments; the optional BPQ surface texture is decorative.

The shared surface follows BPQ's paint order: base colors, irregular texture, translucent
sheen, inset light/shadow, outline, and labels. Reference dimensions scale from a 30-unit
chromatid height. Straight surfaces use SVG gradients; curved surfaces sample the same
alpha function along local normals. No BPQ package is needed at runtime.

`thickness` always means one chromatid's width. Straight sisters occupy 2.2 times that
width, with a common foreground centromere belt extending beyond both outer edges.
`centromere_part(..., across=span)` covers an explicitly authored pair when the scene
owns its centerlines. Along-axis collar width remains proportional to one chromatid.

Use document-unique XML-safe names and short gene labels. Font-size
fitting is approximate: inspect the intended placement, then enlarge the drawing or revise
label placement when necessary. `chromosome_part()` accepts the same options as the layout
API below and returns an `SvgPart` with conservative painted bounds and `start`, `end`,
`center`, `boundary_N` and, when present, `centromere` anchors. Compose it with the standard
part transforms; the recipe owns biological annotations and connector meanings.

Continue the example with a known centromere after segment two:

```python
parent = svg_tools.chromosomes.Chromosome(tuple(
	svg_tools.chromosomes.Segment(letter, "#8356A8", length)
	for letter, length in zip("ABCDE", (70, 90, 60, 80, 100))
), (svg_tools.chromosomes.Centromere(2),))
shorter = svg_tools.chromosomes.delete_segments(parent, 3, 4)
deleted = svg_tools.chromosomes.chromosome_part(
	"deleted", shorter, junctions=(3,),
)
other = svg_tools.chromosomes.Chromosome(tuple(
	svg_tools.chromosomes.Segment(letter, "#3479A8") for letter in "MNOPQ"
), (svg_tools.chromosomes.Centromere(2),))
product_a, product_b = svg_tools.chromosomes.reciprocal_translocation(parent, 3, other, 3)
```

`render_chromosome_layout()` and `chromosome_part()` create straight forms. Their centromeres
are pale, dark-outlined rounded rectangles. `sister_chromatid_parts()` takes two independently
specified chromatid models and centerlines. `condensed_chromosome_part()` produces a compact
state without removing material. Segment anchors report local positions for recipe annotations.

Deletion removes a half-open internal range and does not cross a centromere. Reciprocal
translocation exchanges right tails distal to supplied sites. These bounded operations do not
mutate their inputs and are not a general rearrangement simulator.

Render physical before/after models with `length=None`, equal thickness and one common
enclosing scale. Independently stretching products to the same length would conceal a deletion.
An aligned evidence track may retain a labeled reference gap; that gap is not chromosome
material. Explicit length is useful for standalone placement. Recipes own cut arrows, join annotations and biological labels.

### Curved chromatid bodies

Use `chromosomes.chromosome_path_part(name, chromosome, path_d, *, thickness=28,
closed=False, cut_ends=False, labels=True)` for a single authored curved chromatid. It follows
the centerline with native constant-width strokes; thickness is per chromatid. Segment lengths
give relative arc spans along one continuous centerline; source colors and local band boundaries
follow the segments.

```python
curved = svg_tools.chromosomes.chromosome_path_part(
	"curved", parent, "M 30 90 C 120 10 210 170 300 90", thickness=28,
)
svg_tools.drawing.write_svg("_temp/curved.drawn.svg", 340, 190,
	"Curved chromatid", "One schematic chromatid with source-ordered segments.", curved.fragment)
```

Anchors include `boundary_N`, `segment_N` midpoints and `center`, plus `start`/`end` on open
paths and centromere anchors when present. Keep labels upright and inspect their clearance along
bends. `cut_ends=True` makes flat ends for internal fragments. `closed=True` requires a closed
path and an acentric model; it omits terminal caps and `start`/`end` anchors and cannot combine
with `cut_ends`. Open/closed path geometry must agree with the flag. Recipes own the bends,
spacing, crossing order, pairing and biological claims; the helper does not infer crossover
mechanisms or turn separate homologs into sisters. Use the straight layout API for parallel sisters and source cytoband maps.

Write completed artifacts with `drawing.write_svg()`. XML fragment composition must preserve
the normal SVG and xlink namespaces; a prefixed root alone can import incorrectly in
LibreOffice. See the dated [course migration report](../docs/CHROMOSOME_THEME_MIGRATION_REPORT.md)
for accepted native receipts and remaining gates.

### Named cytobands

Load the bundled 44-row UCSC hg38 chromosome 7 map from the repository root:

```python
model, records = svg_tools.chromosomes.read_cytobands(
	pathlib.Path("svg_tools/data/chr7_hg38_cytobands.tsv"),
)
banded = svg_tools.chromosomes.render_chromosome_layout(
	"chr7", model, length=700, thickness=100, orientation="vertical",
	bands=False, labels=False,
)
selected = next(record for record in records if record.segment.label == "q31.2")
anchors = tuple(anchor for anchor in banded.segments if anchor.segment is selected.segment)
source_label = f"{selected.chromosome}: {selected.segment.label}"
```

The centromere is a large pale rectangle placed at the source-known boundary; it is schematic
and does not establish genomic length. Keep dense map labels outside and inspect clearance at
the actual placement size.

`bands=False` suppresses decorative texture; the source stain fills remain. Decorative band
modes and caller colors do not have to use the source stain palette. `labels=False`
suppresses dense internal band names. Use selected anchors for external labels such as
`CFTR: 7q31.2`. Match records to anchors by Segment identity (`is`), including after deletion
or exchange; original source addresses and coordinates stay with their segments. Keep the
records alongside rearranged products. Prefix groups `q`, `q3`, `q31` and `q31.2` are recipe
annotations over these same records; preserve separate runs after rearrangement.

`Cytoband(chromosome, start, end, stain, segment)` stores original 0-based half-open coordinates;
its address is `segment.label`. The adapter accepts one full contiguous five-column UCSC map
starting at zero, with p then q arms and adjacent p/q `acen` rows. It rejects unsupported maps.
Supported stains are white `gneg`, progressively darker `gpos25/50/75/100`, lavender `acen`,
pale-blue `gvar` and teal `stalk`; the last fill does not add satellite anatomy. There is no
runtime download. Source URL, retrieval date and checksum are recorded in
[chr7_hg38_cytobands.provenance.json](data/chr7_hg38_cytobands.provenance.json).
The bundled intervals are approximate cytoband positions, not precise CFTR
molecular coordinates. The schematic `17q41.3` teaching exercise is not a real chromosome 17 map.

### Gene tracks and specimen

For DNA exons and introns, use the separate [gene_tracks.py](gene_tracks.py):

```python
import svg_tools.gene_tracks

exons = (
	svg_tools.chromosomes.Segment("1", "#3479A8", 80),
	svg_tools.chromosomes.Segment("2", "#3479A8", 60),
	svg_tools.chromosomes.Segment("3", "#3479A8", 90),
)
genomic, genomic_width, exon_starts = svg_tools.gene_tracks.gene_track_svg(
	"genomic", exons, (50, 70),
)
joined, joined_width, exon_starts = svg_tools.gene_tracks.gene_track_svg("joined", exons, (0, 0))
```

`gene_track_svg(name, exons, intron_lengths, *, width=None, height=50)` requires exactly one
finite nonnegative intron length between each pair of exons. Positive introns are thin lines;
zero introns make adjacent blocks. It ignores bands and draws no chromosome caps, centromeres
or sisters. Its boundaries are exon starts plus the final exon end, unlike chromosome
inter-region boundaries. The recipe supplies molecule names and any RNA/cDNA colors; the
helper does not infer a biological process. Wrap fragments with margins as in the first example.

The current specimen is
[chromosome_tool_v2.drawn.svg](../docs/slide-specs/illustration_examples/chromosome_tool_v2.drawn.svg).
Generate a scratch copy from the repository root:

```bash
/opt/homebrew/bin/python3.12 -B -c 'import pathlib; import svg_tools.chromosome_examples; svg_tools.chromosome_examples.make_tool_v2_specimen(pathlib.Path("_temp/chromosome_tool_v2.drawn.svg"))'
PANGOCAIRO_BACKEND=fc rsvg-convert -w 1440 _temp/chromosome_tool_v2.drawn.svg -o _temp/chromosome_tool_v2.png
```

This historical specimen uses the same 44-band chr7 model for its single and rounded-X sister
forms. The current family instead uses rectangular centromeres; regenerate it only when the
specimen is updated to the current renderer. Its linked q31 detail has flat cut ends because it
is an internal crop, not another capped chromosome.

Demonstrated proofs are the full gallery at 1600 x 860 and 1000 x 538, whole forms at
775 x 535 and q31 detail at 530 x 385. A 1800 x 270 centromere diagnostic shows both
narrow source `acen` strips around the hollow markers; they are subtle at reduced size.
These proof sizes are not universal placement minima. All 44 source stains remain in each
whole form. With `PANGOCAIRO_BACKEND=fc`, the rendered font diagnostic matched installed
Atkinson Hyperlegible Next glyph operations and advances. Inspect text at the intended
placement; a font-family declaration alone does not prove actual font selection. The user
rejected the previous v2 gallery's inconsistent theme; the current revision follows the
root-approved shared-family direction. Fresh specification, quality and integration reviews PASS; root viewed all five
final production proofs. The standalone shared-theme revision is DONE. Standalone rendering does not establish instructor, classroom, print or native
slide/export acceptance.

The saved [chromosome_tool.drawn.svg](../docs/slide-specs/illustration_examples/chromosome_tool.drawn.svg)
is historical v1 evidence. Its sister shape was rejected and is superseded by the rounded-X
renderer; its rejection remains recorded in
[SVG_REPAIR_BACKLOG.md](../docs/SVG_REPAIR_BACKLOG.md). Its earlier 1150-pixel sister and
480-pixel overview proofs are historical, not v2 placement requirements.

The `make_banded_chromosomes_1_3(path)` recipe uses the three hg38 source TSVs
`data/chr1_hg38_cytobands.tsv`, `data/chr2_hg38_cytobands.tsv`, and
`data/chr3_hg38_cytobands.tsv`; portable source and retrieval details are in
[data/chr1_2_3_hg38_cytobands.provenance.json](data/chr1_2_3_hg38_cytobands.provenance.json).
Regenerate to a scratch path from the repository root:

```sh
/opt/homebrew/bin/python3.12 -B -c 'import pathlib; import svg_tools.chromosome_examples as e; e.make_banded_chromosomes_1_3(pathlib.Path("_temp/banded_chromosomes_1_3.drawn.svg"))'
```

The 187 true intervals share one genomic scale; 46 band labels, 16 region numbers, six arm
labels and three group labels are teaching selections. Caps and centromeres are schematic;
genomic spans do not establish exact physical arm ratios.

## Recipes and boundaries

The helper adapts the useful BPQ visual vocabulary into native SVG: continuous outlined rods,
subtle terminal treatment, rectangular centromeres, segment colors, bands, and explicit joins.
Recipes own pairing, exchange, layering, telomere relationships, and all biological claims.

The durable recipe is [chromosome_examples.py](chromosome_examples.py). From the
repository root, run Python 3.12 directly (no bootstrap or Git invocation):

```bash
/opt/homebrew/bin/python3.12 -B -m svg_tools.chromosome_examples
```

The module writes its specimen without overwriting course assets. All chromosome geometry comes
from the shared helper.
See the [illustration guide](../docs/slide-specs/GENETICS_ILLUSTRATION_GUIDE.md)
for the scientific meanings and review boundary.

## Example

Save this as `_temp/draw_example.py` and run it from the repository root with
`PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B _temp/draw_example.py`:

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
references. Run `PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B tests/fix_ascii_compliance.py -i PATH.svg`.

The drawing helpers are original to this project and use its MIT license.
