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

## Chromosome drawing tool

Use [chromosomes.py](chromosomes.py) for schematic segments, colors, sizes, rounded-X sisters
and source-backed named cytobands.
The returned fragment is editable static SVG; wrap it with `drawing.write_svg()`:

```python
import pathlib

import svg_tools.drawing
import svg_tools.chromosomes

pathlib.Path("_temp").mkdir(exist_ok=True)
rod = svg_tools.chromosomes.Chromosome((svg_tools.chromosomes.Segment("", "#00775F"),))
fragment, width, boundaries = svg_tools.chromosomes.render_chromosome(
	"plain", rod, width=300, height=50, bands=False,
)
svg_tools.drawing.write_svg("_temp/plain.drawn.svg", width + 20, 70, "Plain chromosome",
	"A schematic single chromatid.", f'<g transform="translate(10 10)">{fragment}</g>')
```

`Segment(label, color, length=64, band=0)` takes a six-digit hex fill, positive finite
schematic length and decorative band index 0-4. `Chromosome(segments, centromere_after=None)`
keeps their order. Colors, lengths and bands follow segment identity through transformations;
bands are not a measured cytological map. Use document-unique XML-safe fragment names.

`render_chromosome(name, chromosome, *, width=None, height=62, bands=True, sisters=False,
junctions=(), allele_labels=False)` returns `(fragment, width, boundaries)`. Width covers the
whole outline; height covers the whole sister pair when requested. Strokes need additional
margins, as above. Boundaries are indexed by the number of preceding segments; at the
centromere the coordinate is the collar center. Short live Atkinson Hyperlegible Next labels
work best. Font-size fitting is approximate: inspect actual font rendering at the intended
placement, and enlarge the drawing or shorten labels when necessary.

Continue the example with a known centromere after segment two:

```python
parent = svg_tools.chromosomes.Chromosome(tuple(
	svg_tools.chromosomes.Segment(letter, "#8356A8", length, band)
	for letter, length, band in zip("ABCDE", (70, 90, 60, 80, 100), (0, 1, 2, 3, 4))
), centromere_after=2)
sisters, sister_width, cuts = svg_tools.chromosomes.render_chromosome(
	"sisters", parent, height=100, sisters=True,
)
shorter = svg_tools.chromosomes.delete_segments(parent, 3, 4)
deleted, deleted_width, cuts = svg_tools.chromosomes.render_chromosome(
	"deleted", shorter, junctions=(3,),
)
other = svg_tools.chromosomes.Chromosome(tuple(
	svg_tools.chromosomes.Segment(letter, "#3479A8") for letter in "MNOPQ"
), 2)
product_a, product_b = svg_tools.chromosomes.reciprocal_translocation(parent, 3, other, 3)
```

For portrait sisters with a labelable centromere, continue with the same `parent`:

```python
layout = svg_tools.chromosomes.render_chromosome_layout(
	"portrait", parent, length=600, thickness=180, orientation="vertical",
	sisters=True, marker_label="cen",
)
svg_tools.drawing.write_svg("_temp/portrait.drawn.svg", layout.width + 20,
	layout.height + 20, "Replicated chromosome", "Identical rounded-X sisters.",
	f'<g transform="translate(10 10)">{layout.svg}</g>')
```

`render_chromosome_layout()` accepts `length`, `thickness`, `orientation`, `bands`, `sisters`,
`junctions`, `allele_labels`, `labels`, `marker_size` and `marker_label`. Length is longitudinal;
thickness covers the complete transverse envelope, including the centromere marker. Portrait
returns `width=thickness`, `height=length`, with the first segment at the top and upright text.
The broad hollow purple oval marks a short real neck without hiding the underlying bands;
it is a diagram convention, not swollen chromosome material. Short internal
`marker_label` text remains available; `marker_label=None` omits its text only. Optional
`marker_size=(along_axis, across_axis)` must fit the envelope; marker settings require a
centromere. The legacy narrow collar remains pale and filled.

The result contains `svg`, `width`, `height`, `boundaries`, `segments`, `centromere` and
`marker_bounds`. Boundary and centromere coordinates are `(x, y)` in the fragment's final
orientation. Each `SegmentAnchor` has the original `segment`, `sister` index (0 or 1),
centerline `start`/`end` points and conservative annotation `bounds`. Bounds and `marker_bounds`
use `(xmin, ymin, xmax, ymax)` and exclude stroke; reserve outer margins. Segment bounds are
not exact path intersections. Marker edge midpoints provide exterior label attachments.

Sisters require a centromere and repeat the same segment content on two attached chromatids;
they are not independently supplied homologs. Deletion removes the half-open range `[start, stop)`
with `0 < start < stop < n`. It can touch but cannot cross the centromere. If its join `start`
equals the resulting centromere boundary, omit `junctions` there. Reciprocal translocation
exchanges right tails only, requiring `c < cut < n` on both known-centromere inputs. Neither
operation changes its inputs. This is not a general rearrangement simulator.

Render before/after models at natural width with equal heights and one common enclosing scale.
Independently stretching products to the same width would conceal a deletion. Explicit width
is useful for standalone placement. Recipes own cut arrows, join annotations and biological labels.

### Named cytobands

Load the bundled 44-row UCSC hg38 chromosome 7 map from the repository root:

```python
model, records = svg_tools.chromosomes.read_cytobands(
	pathlib.Path("svg_tools/data/chr7_hg38_cytobands.tsv"),
)
banded = svg_tools.chromosomes.render_chromosome_layout(
	"chr7", model, length=700, thickness=100, orientation="vertical",
	bands=False, labels=False, marker_size=(18, 100), marker_label=None,
)
selected = next(record for record in records if record.segment.label == "q31.2")
anchors = tuple(anchor for anchor in banded.segments if anchor.segment is selected.segment)
source_label = f"{selected.chromosome}: {selected.segment.label}"
xmin, ymin, xmax, ymax = banded.marker_bounds
centromere_label_start = (xmax, (ymin + ymax) / 2)
```

This thin hollow marker fits inside the source-free collar, including its stroke, at the shown
700-by-100 size. Use the right-edge midpoint `centromere_label_start` for a leader to an
exterior centromere label; reserve space outside the chromosome for that label. A short
internal label also works when space permits. Keep dense map labels outside and check that
both `acen` intervals remain visible around the collar. Marker and collar space are schematic
additions, not genomic length. Recheck clearance when changing size.

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

The revised specimen uses the same 44-band chr7 model for its single and rounded-X sister
forms. Both have a 520-unit longitudinal scale, 64-unit per-chromatid width, matching band
boundaries, rounded ends and a hollow 100-by-38 purple centromere marker. The linked q31
detail reuses the whole map at fivefold isotropic scale and has flat cut ends: it is an
internal crop, not another capped chromosome. Vector brackets retain the q/q3/q31/q31.2
hierarchy; the brown CFTR frame denotes an approximate cytoband location.

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
This compatibility entry draws straight single chromatids; use `render_chromosome()` above
for joined sisters, or `render_chromosome_layout()` for portrait orientation and named-band
anchors. Curved pairing diagrams and internal telomere distractors need separate
source-specific construction.

The durable recipe is [chromosome_examples.py](chromosome_examples.py). From the
repository root, run Python 3.12 directly (no bootstrap or Git invocation):

```bash
/opt/homebrew/bin/python3.12 -B -m svg_tools.chromosome_examples
```

It writes only the new v2 specimen linked above. Historical recipe functions and saved v1
artwork remain available; explicit calls to old recipes use today's renderer and do not
reproduce the rejected v1 sister shape. The module command does not overwrite historical
specimens or course assets. All chromosome geometry comes from the shared helper.
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
