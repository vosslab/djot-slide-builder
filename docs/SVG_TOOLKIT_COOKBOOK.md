# SVG toolkit cookbook

Use these recipes from the repository root. The [capability catalogue](SVG_TOOLKIT.md) lists
parts and their examples; the [gallery](slide-specs/illustration_examples/svg_toolkit/index.webp)
and [native showcase](../exemplars/svg_toolkit.djot) show them together. See the
[slide illustration rules](slide-specs/SVG_DIAGRAMS.md) for editable assets and review. The
[implementation report](SVG_TOOLKIT_IMPLEMENTATION_REPORT.md) links accepted independent trials
and records verification limits.

Choose parts from the catalogue for the relationships you need, then place and connect them with
explicit coordinates. `SvgPart` contains an SVG fragment, painted bounds, and named anchors;
`transform` moves all three. Use `group` to combine parts and isolate their IDs. If no factory
fits, construct a `SvgPart(fragment, bounds, anchors)` with valid self-contained SVG, honest
painted bounds, and authored attachment points. That escape hatch does not infer biology.

## New signaling diagram

Save this complete script as `_temp/signaling_recipe.py` and run it from the repository root:

```python
import pathlib

import svg_tools.annotations
import svg_tools.drawing
import svg_tools.parts
import svg_tools.signaling
import svg_tools.text


source = svg_tools.parts.transform(svg_tools.signaling.protein(
	width=100, height=90, color='#e5d7ef', kind='kinase', activity='active'), x=110, y=100)
target = svg_tools.parts.transform(svg_tools.signaling.phosphate(
	svg_tools.signaling.protein(width=100, height=90, color='#d6e7c0', activity='inactive'),
	site_label='site A'), x=330, y=100)
parts = {
	'source': source,
	'target': target,
	'inhibition': svg_tools.annotations.connector(
		[source.anchors['output'], target.anchors['input']], kind='inhibition'),
	'source_label': svg_tools.text.label(110, 185, 'Kinase', size=16, color='#344651'),
	'target_label': svg_tools.text.label(330, 185, 'Response protein', size=16, color='#344651'),
}
output = pathlib.Path('_temp/signaling_recipe.svg')
output.parent.mkdir(parents=True, exist_ok=True)
svg_tools.drawing.write_svg(output, 450, 200, 'Signaling example',
	'An active kinase inhibits a phosphorylated inactive response protein.',
	svg_tools.parts.group(parts).fragment)
```

```bash
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B _temp/signaling_recipe.py
```

Protein activity and phosphate are separate authored states; neither implies the other. The
protein `input`, `output`, `binding`, and `modification` anchors are schematic attachment points.
An `activity` value draws its own visible label and symbol, included in the protein's bounds;
inspect those bounds when placing other labels and avoid duplicating the activity label.
An unknown phosphate site raises `ValueError`; inspect `part.anchors` to choose a real one.
`connector` supports activation, inhibition, binding, indirect, bracket, and callout relationships.
Provide at least two points with a nonzero final segment. A connector cannot infer its meaning.

## Style a gene in a flow node

Save this complete script as `_temp/svg_toolkit/styled_flow/example.py` and run it from the
repository root. The gene name is italic, while its state and protein name remain upright.

```python
import pathlib

import svg_tools.annotations
import svg_tools.drawing
import svg_tools.parts
import svg_tools.signaling
import svg_tools.text


gene = svg_tools.parts.transform(svg_tools.annotations.box([
	svg_tools.text.TextRun('Sxl', italic=True),
	svg_tools.text.TextRun('\nON'),
], 110, 60, '#e5d7ef', font_size=17), x=80, y=70)
protein = svg_tools.parts.transform(svg_tools.signaling.protein(
	width=100, height=90, color='#d6e7c0'), x=280, y=70)
parts = {
	'gene': gene,
	'protein': protein,
	'arrow': svg_tools.annotations.connector([gene.anchors['right'], protein.anchors['input']]),
	'protein_label': svg_tools.text.label(280, 145, 'SXL protein', size=16, color='#344651'),
}
output = pathlib.Path('_temp/svg_toolkit/styled_flow/styled_flow.svg')
output.parent.mkdir(parents=True, exist_ok=True)
svg_tools.drawing.write_svg(output, 370, 170, 'Gene and protein',
	'An active Sxl gene produces SXL protein.', svg_tools.parts.group(parts).fragment)
```

```bash
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B _temp/svg_toolkit/styled_flow/example.py
```

## Reconstruct an existing figure

First inventory the source: identify every object, label, value, relationship, arrow direction,
state, and meaningful spatial grouping. For an SVG with live text, run:

```python
import svg_tools.text

result = svg_tools.text.extract_text('path/to/source.svg')
for item in result.labels:
	print(item.text, item.x, item.y, item.id)
print(result.unavailable)
```

The x and y attributes are literal, not transformed positions. Outlined and raster labels are not
extractable: inspect the original image and surrounding slide text as well. Record relationships
separately from extracted labels. Adapt the complete signaling recipe above with those objects,
labels, states, and connector directions, then compare the result with the source at slide size.
Keep supplied values, categories, and ordering unchanged; do not invent missing information.

## Plot supplied allele frequencies

The complete [allele frequency script](../svg_tools/examples/allele_frequencies.py) accepts an
optional output path and exposes `generate(pathlib.Path) -> pathlib.Path` for other Python code:

```bash
MPLCONFIGDIR="$PWD/_temp/mplconfig" PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B -m svg_tools.examples.allele_frequencies _temp/allele_frequencies.svg
```

It passes these illustrative values directly to Matplotlib, without fitting, normalization, or a
claim about an evolutionary mechanism:

```python
generation = [0, 1, 2, 3, 4, 5]
p = [0.40, 0.45, 0.43, 0.50, 0.55, 0.60]
q = [0.60, 0.55, 0.57, 0.50, 0.45, 0.40]
```

For another data set, replace the arrays in a copy of the script. `plot_style()` scopes the course
color and editable Atkinson text; `figure_to_part(figure, name='plot', size=600)` imports the
vector figure, and `write_svg` writes the complete document. Raster artists are rejected; the
caller owns the figure. Keep axis labels, units, legend, and ranges appropriate to the data.

## Align icons or import a vector figure

```python
import pathlib

import svg_tools.drawing
import svg_tools.icons
import svg_tools.parts
import svg_tools.svg_import

print(svg_tools.icons.search_icons('microscope'))
source = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 60">'
	'<circle cx="30" cy="30" r="24" fill="#dceef4"/></svg>')
# icon() loads a bundled icon; import_svg() accepts SVG text or bytes.
items = [svg_tools.icons.icon('microscope', size=60, color='#195f82'),
	svg_tools.svg_import.import_svg(source, name='imported', size=60)]
items = svg_tools.parts.distribute(svg_tools.parts.align(items, 'top', 20), 'x', 30)
combined = svg_tools.parts.group({'icon': items[0], 'imported': items[1]})
output = pathlib.Path('_temp/icon_recipe.svg')
output.parent.mkdir(parents=True, exist_ok=True)
svg_tools.drawing.write_svg(output, 180, 100, 'Microscope icons',
	'Two aligned vector icons.', combined.fragment)
```

Use `search_icons` to discover available names. `align` uses painted bounds and `distribute`
keeps the first part in place. Imported SVG must be self-contained and supported by the importer;
unsupported content raises an error rather than silently becoming editable geometry. For arbitrary
source art, check provenance before reuse.

## Put the figure on a native slide

For a deck at `_temp/allele_slide.djot`, with the generated SVG beside it, use:

```djot
=== layout: one-panel

# Allele Frequencies Across Generations

@body

![Illustrative p and q allele frequencies across six generations.](allele_frequencies.svg)

These supplied values illustrate how two allele frequencies can change over generations.
```

Build from the repository root using the configured Python:

```bash
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B deck_tools.py build _temp/allele_slide.djot --format odp
```

The command writes `output/odp/allele_slide.odp`. Run commands that invoke LibreOffice,
including PDF exports and ODP imports, outside the sandbox.
The slide title and caption are native Djot; the single SVG contains editable figure labels and
vector geometry. Inspect the rendered result for clipping, legibility, and the intended relationships.
