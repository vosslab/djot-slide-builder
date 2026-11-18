# Chromosome engine

Define the material once, then draw it in different poses or cut and join it into new products.
Use `svg_tools.chromosome_topology` for biology and `svg_tools.chromosomes.render()` for drawing.
The renderer uses the same BPQ surface paint as the existing chromosome drawing functions.

Start with biological definitions in Python or load them from structured data. Keep source
regions and annotations in the model. Pass numeric `(x, y)` pose points and a separate color
palette to `render()`. The C18, C20, C29, and C66 recipes also define their panels and labels
in Python and structured data. The drawing helpers generate the SVG markup for the parts and
write the composed SVG.

## Draw one chromatid

From the repository root, save the Python examples in order to `_temp/chromosome_example.py`.
The first Python block works on its own and writes `_temp/linked.drawn.svg`.

```bash
mkdir -p _temp
source source_me.sh && python3 _temp/chromosome_example.py
```

```python
import svg_tools.chromosome_topology as topology
import svg_tools.chromosomes as chromosomes
import svg_tools.drawing as drawing
import svg_tools.palette as palette

linked = topology.chromosome('linked', length=240, centromere=.48,
	genes={'w': .27, 'm': .76})
straight = ((20, 40), (260, 40))
blue = {('linked', 'body'): palette.shade('sky_blue', 'dark')}
part = chromosomes.render('linked-straight', linked, points=straight, width=22, palette=blue)
drawing.write_svg('_temp/linked.drawn.svg', 280, 80, 'Two linked loci',
	'A single chromatid carries w and m at separate loci.', part.fragment)
```

Give each rendered part a distinct XML-safe `name`, such as `linked-straight`. This name labels
the SVG fragment and its internal IDs. The model ID `linked` identifies its biological source.

Use `centromere_styles` to give a collar an upright label, a six-digit hex fill, or both.
Key each style by `(source_id, site_id)`. The same style colors the shared belt when you
render sisters.

```python
collar = chromosomes.CentromereStyle(label='2', fill=palette.shade('sky_blue', 'extra_light'))
collars = {('linked', 'linked.cen'): collar}
labeled = chromosomes.render('linked-labeled', linked, points=straight, width=22,
	palette=blue, centromere_styles=collars)
```

## Draw the same material again

This render keeps the same allele occurrences, centromere, and color in a new pose.

```python
curved_points = ((20, 48), (105, 25), (185, 62), (260, 43))
curved = chromosomes.render('linked-curved', linked, points=curved_points,
	width=22, palette=blue)
```

Two points give a straight centerline. Three or more fit a smooth spline through the shape.
The renderer rescales the curve around its first point until its arc length equals
`model.length * scale`, with `scale=1` by default. The other point coordinates, including the
last point, may move.
Use `part.anchors['end']` for the actual endpoint. `width` is the body width in display units
and stays fixed as `scale` changes. Keep one scale when comparing material lengths. Supply
finite points with distinct neighbors and distinct ends. Use gentler bends if a curve doubles
back locally or bends too tightly for its width. The engine handles open, linear material.

For an axis-aligned telomere, put three collinear points at that end of a curved pose.
Give them the same y coordinate for a horizontal arm or the same x coordinate for a
vertical arm. Keep the outermost span at least one cap length after scaling
(`8 * width / 30` on a full-size rod). This holds both sides of the cap at the same angle.
For an angled tip, use collinear points along its intended direction.

## Name source material and loci

- `chromosome()` takes a positive length and optional feature fractions from 0 to 1, measured
  along its source. Choose one length unit for all material in the figure. A centromere is an
  independent point with site ID `<source_id>.cen`. Genes map logical locus IDs to positions.
  Each allele initially uses its locus ID as its display label.
- `regions=((0, 'body'), (.58, 'band'))` assigns semantic names to consecutive source
  intervals. Start at zero, put the start fractions in strictly increasing order, and let the
  last interval extend to the end. Omitting `regions` gives one region named `body`.
  Supply a six-digit hex color in `palette[(source_id, region_id)]` for each retained region.
- A source ID names the immutable biological source. A copy ID names one physical occurrence of
  its material. The factory initially uses the same string for both. A homolog has a new source
  and copy ID. `copy(model, copy_id)` keeps source IDs and gives the new occurrence fresh copy
  IDs. Choose a fresh copy ID in your recipe's namespace each time you need a new physical copy.
  `replicate(model)` derives two distinct sister IDs from the input model ID. Keep source and
  copy IDs unique for their intended meanings across the models you combine. IDs belong to the
  recipe's namespace, so repeating `replicate()` on the same model yields the same pair of IDs.
- Use the factory and operations to build partial material. They retain the original source
  coordinates and track the orientation and ends as you cut and join. The `project_regions()`,
  `project_genes()`, and `project_centromeres()` functions report distances from the current start
  of a chromatid, in material units. They retain source IDs, and projected genes and centromeres
  include copy IDs. Use the rendered part's anchors to place objects in SVG coordinates.

## Make homologs and sisters

Make a homolog from one intact source chromosome. Use the same logical locus IDs `w` and `m`
and set its alleles explicitly. The homolog inherits the region intervals and locus positions.
Render each homolog separately.

```python
wild = topology.homolog(linked, 'wild', alleles={'w': 'w+', 'm': 'm+'})
wild_part = chromosomes.render('wild-straight', wild, points=((20, 95), (260, 95)),
	width=22, palette={('wild', 'body'): palette.shade('dark_orange', 'dark')})
```

Use `replicate()` and one sequence of shape points to draw sisters. This pose is the reference
between the two translated bodies. The automatic belt requires one corresponding active
centromere per sister. The two chromatids remain available as `sisters.first` and `sisters.second`
for separate poses or material operations. For a deep U-shaped bend, give each sister
its own pose. The automatic pair uses one translation per sister, so their arms can
overlap where the curve turns parallel to that translation.

```python
sisters = topology.replicate(linked)
paired = chromosomes.render('linked-sisters', sisters, points=curved_points,
	width=22, palette=blue)
```

## Exchange two terminal pieces

Split at a fraction strictly between 0 and 1, measured along the current input in its current
direction. Each product retains one prefix and the other chromosome's terminal piece.
The lengths change from 240 and 180 to 201 and 219, preserving the total material.

```python
other = topology.chromosome('other', length=180, centromere=.32, genes={'r': .85})
linked_start, linked_tip = topology.split(linked, .65)
other_start, other_tip = topology.split(other, .75)
first_product = topology.join(linked_start, other_tip)
second_product = topology.join(other_start, linked_tip)
topology.validate_conservation((linked, other), (first_product, second_product))

ancestry = {('linked', 'body'): blue['linked', 'body'],
	('other', 'body'): palette.shade('red', 'dark')}
first_result = chromosomes.render('first-product', first_product, points=straight,
	width=22, palette=ancestry)
second_result = chromosomes.render('second-product', second_product,
	points=((20, 95), (260, 95)), width=22, palette=ancestry)
drawing.write_svg('_temp/exchanged.drawn.svg', 280, 135, 'Terminal exchange',
	'Two products retain the material from both chromosomes.',
	first_result.fragment + second_result.fragment)
```

`reverse(fragment)` flips the material's order and swaps its ends. Source intervals are
half-open. A gene or centromere exactly on a cut belongs to the piece on the higher-coordinate
side of that cut in the original source. Reversal changes its display position and preserves
its ownership. A point at the last native coordinate belongs to the interval ending there.

Read `Chromatid.spans` to inspect source coverage and copy ownership. The spans are read-only
and appear in the order of the current chromatid. `span.source.id` identifies the original
source and `span.source.length` gives its full length. `span.copy_id` identifies the physical
copy. `span.start` and `span.stop` give the lower and upper bounds of the retained half-open
interval in native source units. `span.orientation` is `1` when the span runs from lower to
higher native coordinates and `-1` when it runs from higher to lower. `Chromatid.length` sums
`span.stop - span.start` over all its spans.

The first exchange product retains native intervals `[0, 156)` of copy `linked` and
`[135, 180)` of copy `other`. Inspect the source ID, copy ID, and interval for each span.

```python
for span in first_product.spans:
	print(span.source.id, span.copy_id, span.start, span.stop)
```

`join(*fragments)` consumes the facing ends in the supplied order and preserves the outer
ends. Drawn fragments automatically get a gray cap at a native telomere and a flat edge at a
break. The renderer can mark internal joins where they are clear of a centromere collar. Two
independent drawings can visually cross without joining their DNA.

For a rearrangement that retains all material, call `validate_conservation(before, after)` on
the complete sets of chromatids. It raises `ValueError` when a native source interval is missing
or reused, even if the total lengths agree. Product order, orientation, and cuts can change.

An activity change leaves a site on its material. The drawing shows collars at active sites.
Use `(copy_id, site_id)` when more than one retained copy has the same site ID.

```python
inactive = topology.with_centromere_activity(second_product, 'other.cen', active=False)
```

## Place labels and compose

`render()` returns an `SvgPart`. Use its `fragment` to write an SVG, its `bounds` to fit the
canvas, and its `anchors` to position labels and leaders. Bounds are in SVG coordinates in the
order `(xmin, ymin, xmax, ymax)` and include painted collars, leaders, and measured external
label text. The key anchors refer to the final shape in SVG coordinates.

| Feature | Anchor |
| --- | --- |
| Start and end | `start`, `end` |
| Arc midpoint | `center` |
| Active centromere | `centromere` for the first, plus `centromere_0`, `centromere_1`, and so on in material order |
| Gene locus | `gene_w` when `w` is unique on the chromatid. `gene:linked/linked/w` always identifies source, copy, and locus explicitly. Each qualified component is URL-encoded. |

Active sites at the same position each retain an indexed anchor and share one visible collar.
Adjacent regions with the same color paint as one continuous stroke. Each region retains its
source identity and boundary anchors.

Sister bodies have `first.` and `second.` anchor prefixes. For example,
`paired.anchors['first.gene_w']` belongs to the first sister, and `paired.anchors['centromere']`
marks the midpoint of their shared belt. The unprefixed `start`, `end`, and `center` follow the
reference pose.

Internal gene cards leave one telomere-cap length of body color beside each telomere,
centromere collar, and visible junction. A card that cannot fit raises `ValueError`.
Use `gene_palette` to assign card fills by `(source_id, locus_id)`. A locus keeps its color
as it moves to another product or changes alleles.

Set `allow_external_genes=True` to allow dot-and-leader labels at loci with too little room
for a card. The leader follows the local normal and points outward on sisters. The locus
anchor stays on the body. Check spacing among external labels and neighboring objects in the
complete figure.

Cutting at `m` puts `terminal_part.anchors['gene_m']` at the start of the fragment. Add a
10-unit margin around the reported bounds and write a transparent SVG.

```python
import svg_tools.parts as parts

_, terminal = topology.split(linked, .76)
terminal_part = chromosomes.render('terminal-fragment', terminal, points=straight,
	width=22, palette=blue, allow_external_genes=True)

xmin, ymin, xmax, ymax = terminal_part.bounds
margin = 10
shifted = parts.transform(terminal_part, x=margin-xmin, y=margin-ymin)
drawing.write_svg('_temp/terminal.drawn.svg', xmax-xmin+2*margin, ymax-ymin+2*margin,
	'Terminal fragment', 'A leader labels the m locus at the cut.', shifted.fragment)
```

Use [parts.py](../svg_tools/parts.py) to move or group fragments with their anchors. Use
[CHROMOSOME_GENE_LABELS.md](CHROMOSOME_GENE_LABELS.md) for allele conventions and the
[SVG_TOOLKIT_COOKBOOK.md](SVG_TOOLKIT_COOKBOOK.md) to place the SVG in a slide. Keep slide titles,
captions, and explanatory prose native in Djot so they stay editable in the exported ODP.

For segment-based illustrations, cytobands, and SVG-path poses, see the chromosome drawing
section in [README.md](../svg_tools/README.md#chromosome-drawing-tool).
