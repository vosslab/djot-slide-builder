# SVG toolkit capability catalogue

Use `svg_tools` to author editable, static SVG illustrations for slides. Start with the
[gallery](slide-specs/illustration_examples/svg_toolkit/index.webp), its
[Djot showcase](../exemplars/svg_toolkit.djot), and the [cookbook](SVG_TOOLKIT_COOKBOOK.md)
for complete compositions. The [implementation report](SVG_TOOLKIT_IMPLEMENTATION_REPORT.md) records
verification and limits; independent [signaling](slide-specs/illustration_examples/svg_toolkit_trials/new_signaling/README.md)
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
/opt/homebrew/bin/python3.12 -B -m svg_tools.examples.placement
```

Most component examples write SVGs under `_temp/`; `curve_samples` writes beside its source.
Lecture pilot recipes can default to durable lecture assets, including [seed_cross](../svg_tools/examples/seed_cross.py),
[yeast_mating](../svg_tools/examples/yeast_mating.py), and [western_detection](../svg_tools/examples/western_detection.py).
Check each source for its default and optional output path or directory before running it; supply an
alternative output to avoid overwriting an asset. For direct scripts outside the repository root,
make the repository importable with `PYTHONPATH` pointing to that root. The gallery builder is
[build_gallery.py](../svg_tools/examples/build_gallery.py).

For pedigrees, crosses, gels, trees and related generators, check the existing BPQ capabilities;
Virtual Lab already supplies equipment artwork. The [reuse survey](SVG_TOOL_ROADMAP.md#reuse-before-building)
records their paths and limits. The [pedigree guide](slide-specs/GENETICS_ILLUSTRATION_GUIDE.md#pedigrees-reuse-the-bpq-native-svg-renderer)
describes its authoring and provenance requirements.

## Compose parts

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
  bounds and margins. XML is checked before writing; this is not a sanitizer.

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
  `delete_segments`, `reciprocal_translocation`, and `read_cytobands` support chromosome
  models. `gene_tracks.gene_track_part` adapts exon/intron tracks; `gene_feature_part`,
  `landmark_part`, and `operon_part` compose supplied directions and offsets. The detailed
  [chromosome and gene-track reference](../svg_tools/README.md#chromosome-drawing-tool)
  documents sizes, boundaries, source maps and rearrangement limits.
- `svg_import.import_svg(markup, name=..., size=None)` imports supported static SVG markup;
  `size` sets width and bounds are the clipped viewport, not tight paint bounds. Use distinct
  names or `group` for repeated instances. Raster artists and unsupported SVG features are
  rejected; consult [the importer](../svg_tools/svg_import.py) and example for its scope.
- `icons.search_icons(query)` searches installed Lucide names; `icons.icon(name, size=...,
  color=..., stroke_width=2)` loads one. Install project npm dependencies for the offline assets.
- `plots.plot_style(course='genetics')` scopes Matplotlib styling; `figure_to_part(figure,
  name=..., size=None)` imports the caller's vector figure without closing it or changing its
  data. Supply the values and axes yourself; inspect labels and any clipping.

All these tools produce deterministic static artwork from authored inputs. They do not supply an
embedded AI service or infer a diagram's scientific content. Inspect output in the final slide as
well as standalone renders; native ODP/PDF export can expose different font or placement behavior.
