# SVG toolkit capability catalogue

Use `svg_tools` to author static SVG illustrations for slides. Start with the
[gallery](slide-specs/illustration_examples/svg_toolkit/index.webp), its
[Djot showcase](../exemplars/svg_toolkit.djot), and the [cookbook](SVG_TOOLKIT_COOKBOOK.md)
for complete compositions. Follow the [visual style guide](SVG_VISUAL_STYLE.md) for locally authored
geometry, line hierarchy, color, and slide-size review. The [initial implementation report](SVG_TOOLKIT_IMPLEMENTATION_REPORT.md) records
earlier verification and limits; [SVG_AESTHETIC_UPGRADE_REPORT.md](SVG_AESTHETIC_UPGRADE_REPORT.md)
records the current upgrade and its verification. Independent [signaling](slide-specs/illustration_examples/svg_toolkit_trials/new_signaling/README.md)
and [Sxl reconstruction](slide-specs/illustration_examples/svg_toolkit_trials/sxl_reconstruction/README.md)
recipes show complete native slides. The [SVG diagram contract](slide-specs/SVG_DIAGRAMS.md) covers
provenance, `.drawn.svg` eligibility, and slide integration. The code is a set of drawing
parts, not a layout engine: the author supplies geometry, labels, data and relationships.

## Choose a starting point

| Task | Use | Runnable example module |
| --- | --- | --- |
| Place, align and group repeated parts | `parts.transform`, `align`, `distribute`, `group` | `placement` |
| Labels, scripts, wrapping and source text | `text` | `text_labels`, `styled_text` |
| Compose an existing static SVG | `svg_import.import_svg` | `svg_composition` |
| Search for general icons | `icons.search_icons`, `icon` | `icons` |
| Process, decision and relationship arrows | `annotations.box`, `connector` | `annotations` |
| Place objects along a path | `curves.sample_curve` | `curve_samples` |
| Membranes and receptor signaling | `signaling` | `membranes`, `proteins`, `signaling` |
| Cells and organelles | `cells` | `cells`, `organelles`, `yeast_mating` |
| Chromosomes, rearrangements and gene tracks | `chromosomes`, `gene_tracks` | `placement`, `gene_features` |
| Binding and detection | `binding` | `binding`, `western_detection` |
| Seed and flower phenotypes | `phenotypes` | `phenotypes`, `seed_cross` |
| Data plots | `plots` with Matplotlib | `plots`, `genome_composition` |
| Array workflow | icons and annotations | `array_comparison` |
| Schematic equipment | `drawing.project`, `cuboid`, `cylinder` | [equipment instructions](../svg_tools/README.md#constructing-equipment) |

Run an example from the repository root, substituting a module name from the table:

```sh
source source_me.sh && python3 -m svg_tools.examples.placement
```

Component examples write SVGs under `_temp/` by default.
Lecture pilot recipes can default to durable lecture assets, including [seed_cross](../svg_tools/examples/seed_cross.py),
[yeast_mating](../svg_tools/examples/yeast_mating.py), and [western_detection](../svg_tools/examples/western_detection.py).
Check each source for its default and optional output path or directory before running it; supply an
alternative output to avoid overwriting an asset. Run direct scripts through the same repository
bootstrap. The gallery builder is
[build_gallery.py](../svg_tools/examples/build_gallery.py).

For pedigrees, crosses, gels, trees and related generators, check the existing BPQ capabilities;
Virtual Lab already supplies equipment artwork. The [reuse survey](SVG_TOOL_ROADMAP.md#reuse-before-building)
records their paths and limits. The [pedigree guide](slide-specs/GENETICS_ILLUSTRATION_GUIDE.md#pedigrees-reuse-the-bpq-native-svg-renderer)
describes its authoring and provenance requirements.

## Name and place recipes

Keep lecture-specific artwork code with its lecture, normally under `genetics/LECTxx/djot/`
or the corresponding course directory. Shared drawing functionality belongs in `svg_tools/`;
repository maintenance utilities belong in `devel/`.

- `<subject>_recipe.py` defines one illustration, such as
  [hla_region_recipe.py](../genetics/LECT03/djot/hla_region_recipe.py).
- `<subject>_recipes.py` defines a related collection, such as
  [meiosis_assortment_recipes.py](../genetics/LECT02/djot/meiosis_assortment_recipes.py).
- `make_<subject>.py` generates or updates assets, often by running recipes; see
  [make_lect10b_figures.py](../genetics/LECT10/djot/make_lect10b_figures.py).
- `render_` identifies conversion to a particular output format, such as
  [render_tables.py](../genetics/LECT04/djot/render_tables.py), which converts HTML tables to PNG.

General build utilities and toolkit example modules retain their existing names. A recipe's
filename is separate from its output asset names; keep existing slide URLs when renaming code.

Write a module or function docstring that explains what the figure teaches and why its model and
drawing choices serve that purpose. For non-obvious choices, record details such as the reason for
a length or scale, what a color encodes, or which features the schematic simplifies. Use a few
paragraphs when the reasoning needs room. Link to the
[slide development notes](slide-specs/AUTHORING_GUIDE.md#slide-development-notes) for the source record.

Keep generator data in structured JSON. When a recipe preserves existing vector artwork, store the
artwork in an `.svg` file and put its relative path in the data. Generate new chromosome geometry,
labels, and composition from structured data and Python drawing functions.

## Compose parts

Use `lxml.etree` for XML construction and the shared writer for complete figures.
The writer uses the default SVG namespace and the standard `xlink` prefix for LibreOffice.

`SvgPart(fragment, bounds, anchors)` contains SVG markup, conservative painted bounds
`(xmin, ymin, xmax, ymax)`, and named `(x, y)` attachment points in local coordinates.
Inspect `part.bounds` and `part.anchors` before positioning. Anchors can lie outside bounds;
bounds are conservative, and font fallback or imported viewport clipping requires visual review.
Many biological parts are centered on `(0, 0)`, whereas gene tracks and imported viewports use
other origins. Consult their examples and anchors rather than assuming all origins match.

- `transform(part, x=0, y=0, rotation=0, scale=1)` scales, rotates in degrees around the
  local origin, then translates; it returns updated bounds and anchors. Scale must be positive.
- `align(parts, edge, coordinate)` accepts `left`, `right`, `top`, `bottom`, `center_x` or
  `center_y`; alignment uses painted bounds.
- `distribute(parts, axis, gap)` spaces bounds in input order along `x` or `y`, with a positive
  gap; the first part stays in place.
- `group({'name': part, ...})` combines bounds and namespaces fragment IDs. Anchors become
  `name.anchor`; group names are XML-safe identifiers without dots.
- `drawing.write_svg(path, width, height, title, description, body)` wraps trusted fragment
  markup in a complete SVG. Provide positive dimensions and a canvas that includes the painted
  bounds and a small margin. It removes plain white viewport rectangles so the slide background
  remains visible. XML is checked before writing; this is not a sanitizer.
- `drawing.remove_canvas_background(root)` applies the same cleanup to legacy SVG trees before
  serialization or an authored viewport crop. Local white structures and panels retain their fills.
  Fit crops to actual content; the helper does not infer drawing bounds or rearrange a figure.

For a one-off feature, author a trusted SVG fragment and construct `SvgPart(fragment, bounds,
anchors)` directly. Supply bounds that cover its stroke and text and meaningful anchors; then
use the same transforms and grouping. Choose unique IDs, or use grouping to namespace instances.
This escape hatch keeps unusual source-specific geometry and relationships explicit.

## Text and reconstruction

`text.label(x, y, value, size=..., color=...)` returns editable measured text; `(x, y)` is
its baseline. Its `baseline`, `start`, `end` and `center` anchors support positioning.
`text.measure_text` returns relative bounds. `TextRun(text, bold=False, italic=False, color=None,
script=None)` supports `sub` and `super`; `styled_label` makes one line and `wrapped_text`
wraps runs at word boundaries. Supply `width` and optionally `height`; it raises `ValueError`
when text cannot fit, so enlarge the available area or revise placement and review the result.

The `normal` role uses Atkinson Hyperlegible Next; `sequence` uses Mono for aligned sequences.
Measurements use bundled font files. Install the corresponding fonts for the renderer and
LibreOffice: the SVG declares font families and does not embed live fonts. Missing glyphs receive
fallback allowance, but actual fallback metrics can exceed it. Inspect rendered text at intended
slide size. See [installation](INSTALL.md) and [font guidance](slide-specs/SVG_DIAGRAMS.md).

For an existing SVG, `text.extract_text(path)` returns `labels` with text and literal `x`, `y`,
and `id` attributes plus an `unavailable` report. Coordinates are not transformed; raster images
and outlined paths may contain words that cannot be recovered as text. Inspect the source image
and slide context as well. Record all words, values, categories, order, contacts, directions and
relationships; preserve them when composing the replacement. Compare source and replacement,
then render at the actual slide placement and inspect legibility, clipping and biological meaning.

## API reference by subject

Import modules explicitly, for example `from svg_tools import cells, parts`. Width, height, length
and size are drawing units; colors are caller choices. They describe meaning or identity, and need
not follow a course accent hue. Use semantic colors consistently across related figures.

- `annotations.box(label, width, height, fill, shape='process', ...)` accepts a string or a
  `list[svg_tools.text.TextRun]` for a styled label, centers a process box or `shape='decision'`
  diamond at the origin, and rejects labels that do not fit. `connector(points,
  kind='activation', ...)` follows authored points; kinds also include `inhibition`, `binding`,
  `indirect`, `bracket`, and `callout`. Label branches separately.
- `curves.sample_curve(path_d, spacing=...)` returns `(x, y, tangent_degrees)` at regular path
  distances; the endpoint appears only when it falls on a spacing interval.
- `signaling.membrane(path_d, spacing=..., thickness=..., color=..., gaps=())` samples an open
  centerline. Gaps are inclusive distance intervals; allow head and stroke clearance. Side and
  midpoint anchors remain defined even in a gap. `protein(width=..., height=..., color=...,
  kind='globular', activity=None)` also accepts `kinase` and `active`/`inactive` states. An
  activity state draws a visible label and symbol included in the part's bounds; inspect those
  bounds when placing other labels and avoid adding a duplicate activity label.
  `ligand` and `receptor` take width, height and color. The receptor membrane plane is local
  `y=0`. `phosphate(part, site='modification', site_label=None, radius=10)` attaches to a
  named anchor independently of activity; activity is not inferred from phosphorylation.
- `cells.cell_envelope(kind=..., width=..., height=..., color=..., wall_color=None)` accepts
  `animal`, `bacterial`, `yeast`, `fused_yeast`, and `plant`; plant requires a wall color.
  Place `nucleus` and `nucleolus` separately. `organelle(kind=..., width=..., height=...,
  color=...)` accepts `mitochondrion`, `chloroplast`, `er`, `golgi`, `lysosome`, `vesicle`.
  ER is generic; lysosome and vesicle contents are caller-composed. Cardinal boundary anchors
  exclude stroke.
- `binding.antibody`, `antigen`, and `enzyme_tag` each take keyword width, height and color.
  Antibody exposes `Fab_left`, `Fab_right`, and `Fc`; antigen and enzyme tag expose cardinal
  contact anchors. Author actual contacts, labels and ordering.
- `phenotypes.seed(size=..., color=..., shape='round')` also accepts `wrinkled`.
  `flower(size=..., color=..., petals=5)` is a generic radial wildflower, not pea anatomy.
  Place and count individual parts explicitly.
- `chromosomes.Segment`, `Chromosome`, `render_chromosome_layout`, `chromosome_part`,
  `chromosome_path_part` (authored curved single chromatids), `centromere_part`
  (a source-known locus only), `delete_segments`,
  `reciprocal_translocation`, and `read_cytobands` support chromosome models. `gene_tracks.gene_track_part` adapts exon/intron tracks; `gene_feature_part`,
  `landmark_part`, and `operon_part` compose supplied directions and offsets. The detailed
  [chromosome and gene-track reference](../svg_tools/README.md#chromosome-drawing-tool)
  documents sizes, boundaries, source maps and rearrangement limits.
- `svg_import.import_svg(markup, name=..., size=None)` imports supported static SVG markup;
  `size` sets width and bounds are the clipped viewport, not tight paint bounds. Use distinct
  names or `group` for repeated instances. The parser disables entity expansion and external
  resource loading. Raster artists and unsupported SVG features are
  rejected; consult [the importer](../svg_tools/svg_import.py) and example for its scope.
- `icons.search_icons(query)` searches installed Font Awesome Free solid icon names;
  `icons.icon(name, size=..., color=...)` loads one SVG, retaining its attribution comment.
  Install project npm dependencies for the offline assets. Icons are filled shapes; `size` sets
  their width and preserves the original aspect ratio. Slides carry only the selected icons.
- `plots.plot_style(course='genetics')` scopes Matplotlib styling; `figure_to_part(figure,
  name=..., size=None)` imports the caller's vector figure without closing it or changing its
  data. Export uses a transparent, content-fitted canvas with a small margin. Supply the values
  and axes yourself; inspect labels and any clipping.

All these tools produce deterministic static artwork from authored inputs. They do not supply an
embedded AI service or infer a diagram's scientific content. Inspect output in the final slide as
well as standalone renders; native ODP/PDF export can expose different font or placement behavior.

For chromosome output, use `drawing.write_svg()` to retain normal SVG/xlink namespaces
through XML composition and native import. The [migration report](CHROMOSOME_THEME_MIGRATION_REPORT.md)
records current course acceptance separately from toolkit examples.
