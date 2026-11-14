# Native chart namespace diagnosis

> Historical note: `_temp` SVG toolkit paths in this report were scratch evidence and have been removed after review. See the [final toolkit implementation report](../../SVG_TOOLKIT_IMPLEMENTATION_REPORT.md) for durable results.


The blank human-genome chart is caused by LibreOffice's handling of SVG namespace
prefixes. On this host, the same SVG paints with unprefixed SVG elements or the literal
`svg:` prefix, but paints blank with the equivalent `ns0:` or `custom:` prefixes.
Nesting, viewBox, clipping, and paint styles are not the cause in this chart.

Production source, generated assets, consumer Djot, and canonical proof files were not
changed. All comparison artifacts are under `_temp/svg_toolkit/native_chart_diagnosis/`.
This is a diagnosis and a tested fix recommendation, not an implemented M25 pass.

## Controlled native comparisons

`comparisons.odp` was built using `native_export.parse_deck` and
`native_export.render_native_odp`, then exported using
`slide_lib.libreoffice.convert_file` outside the sandbox. Its seven pages use the
following SVGs, in this order. The existing canonical image is the baseline.

| Page | Variant | Native PDF result |
| --- | --- | --- |
| 1 | `canonical.svg` | Entire chart blank |
| 2 | `no_svg_prefix.svg`: remove only SVG element prefix and its declaration | All six bars and labels visible |
| 3 | `nested_as_root.svg`: promote nested SVG, retain prefix | Entire chart blank |
| 4 | `nested_as_root_no_prefix.svg`: promote and unprefix SVG | All six bars and labels visible |
| 5 | `no_overflow.svg`: remove overflow style only | Entire chart blank |
| 6 | `no_clip.svg`: remove clip-path attributes only | Entire chart blank |
| 7 | `raw_matplotlib.svg`: capture actual recipe's Matplotlib savefig input | All six bars and labels visible |

The raw producer output has only its standard external SVG DOCTYPE removed: the native
image reader correctly rejects DTD-bearing XML. Its paths, styles, text, dimensions,
viewBox, and references otherwise remain the producer output.

`prefix_comparisons.odp` / `.pdf` supplies the tighter control:

| Page | Variant | Native PDF result |
| --- | --- | --- |
| 1 | `svg_prefix.svg`: change `ns0:` to `svg:` | All six bars and labels visible |
| 2 | `other_prefix.svg`: change `ns0:` to `custom:` | Entire chart blank |

Viewed white-background quality-90 WebP evidence:

- `_temp/svg_toolkit/native_chart_diagnosis/comparisons_index.webp`
- `_temp/svg_toolkit/native_chart_diagnosis/prefix_comparisons_index.webp`
- Individual `comparison-1.webp` through `comparison-7.webp` and `prefix-1.webp`, `prefix-2.webp`.

## Shared-path recommendation

Normalize SVG element names in `svg_tools.drawing.write_svg` after parsing the body and
before final serialization. Strip only the exact `{http://www.w3.org/2000/svg}` QName
prefix, retaining the existing outer default `xmlns`. Do not change geometry, nesting,
viewBox, clip paths, style values, IDs, href targets, text, font attributes, or bounds.
This is a small loop in the existing final writer, not a new SVG framework.

Keep `xlink:href` serialized with the literal `xlink` prefix. The current importer already
registers this namespace. An isolated fresh-process normalizer that let ElementTree
rename it to `ns3:href` lost `<use>` markers and tick marks in LibreOffice; explicitly
retaining `xlink` restored them. The final proof below includes that retention.

Do not solve this by globally registering `svg` for the SVG namespace. ElementTree's
registry is process-global, and `slide_lib.odp_export` registers that same prefix for the
*different* ODF svg-compatible namespace. The current writer emits whatever prefix that
registry supplies: the failing canonical genome uses `ns0:`, whereas the passing plot
showcase assets use `svg:`. Local final-tree normalization avoids import-order dependence
and does not interfere with native ODP serialization.

A focused regression should pass namespaced imported SVG through the final writer,
include a local clip and xlink `<use>` reference, and check expanded XML names, references,
editable text, and serialization under a conflicting namespace registration. No public
API, plot recipe, or consumer wording needs to change.

## General-path proof

The current native showcase's pages 5 (SVG import), 6 (icons), 11 (line, bars, error bars,
histogram), and 17 (allele-frequency lines and markers) already paint. Their inspected
contact sheet is `original_import_gallery.webp`. This rules out a universal Matplotlib or
nested-SVG failure.

`normalize_proof.py` applies the proposed local QName normalization to private copies of
five actual gallery/pilot assets, retaining `xlink`. It asserts that the complete sequence
of parsed element names, attributes, and text is identical before and after serialization.
`normalization_checks.json` records these successful checks:

| Asset | Parsed nodes |
| --- | --- |
| Genome composition | 101 |
| SVG composition | 22 |
| Lucide icon gallery | 43 |
| Four-format plot gallery | 369 |
| Allele frequencies | 149 |

The resulting five-page `normalized_gallery.odp` / `.pdf` was exported natively and viewed.
All plot types paint; error-bar point markers, axis ticks, allele markers, and legend
markers remain visible. `normalized_gallery-1.webp` through `normalized_gallery-5.webp`
are 1600-pixel-wide quality-90 white-background proofs. The plot and allele pages were also
viewed individually at full size.

`genome_consumer_normalized.odp` is a private copy of the existing canonical genome ODP
with exactly its one matching embedded SVG replaced. Every other ZIP member is retained.
Its native PDF paints all six raw bars and labels: 1.5%, 5%, about 20%, 15%, 44%, and 14%.
The original title, right-hand bullets, layout, and frame remain intact. The full-size
`genome_consumer_normalized-1.webp` was viewed. `pdftotext -layout` extracts the chart's
category labels and values as well as the native bullets; no rasterization or label
outlining was performed. `pdffonts` lists embedded Atkinson Hyperlegible Next Regular
(Type 3 and TrueType) and Helvetica. This is evidence of retained extractable text, not
proof of exact font identity for every glyph or interactive Impress editing.

`normalized_index.webp` shows all five normalized gallery pages plus the original genome
consumer context. The initial normalization trial that omitted xlink prefix retention
was rejected and overwritten by this corrected final proof.

## Commands and scope

All commands used configured Homebrew Python directly, with no environment bootstrap or
Git invocation. Initial generation:

```bash
PYTHONPATH="$PWD" MPLCONFIGDIR="$PWD/_temp/mplconfig" /opt/homebrew/bin/python3.12 -B _temp/svg_toolkit/native_chart_diagnosis/prepare.py
/opt/homebrew/bin/python3.12 -B _temp/svg_toolkit/native_chart_diagnosis/normalize_proof.py
```

Native builds used the following operations, now collected in `export.py` for replay.
Run this command outside the sandbox, as required by AGENTS.md:

```bash
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B _temp/svg_toolkit/native_chart_diagnosis/export.py
```

The initial comparison build stopped safely on raw Matplotlib's DTD; after removing only
that DTD, all native build/export commands succeeded. Rendering used `pdftoppm`, e.g.:

```bash
pdftoppm -scale-to-x 1600 -scale-to-y -1 -png _temp/svg_toolkit/native_chart_diagnosis/normalized_gallery.pdf _temp/svg_toolkit/native_chart_diagnosis/normalized_gallery
pdftoppm -scale-to-x 1600 -scale-to-y -1 -png _temp/svg_toolkit/native_chart_diagnosis/genome_consumer_normalized.pdf _temp/svg_toolkit/native_chart_diagnosis/genome_consumer_normalized
pdftotext -layout _temp/svg_toolkit/native_chart_diagnosis/genome_consumer_normalized.pdf _temp/svg_toolkit/native_chart_diagnosis/genome_consumer_normalized.txt
pdffonts _temp/svg_toolkit/native_chart_diagnosis/genome_consumer_normalized.pdf
```

Pillow converted the RGB renders to WebP with `quality=90`; proof contact sheets use white
backgrounds. Initial seven-page and two-page control renders are 1200 pixels wide.

No permanent tests, full lecture rebuilds, other-host LibreOffice checks, or interactive
Impress editing were performed. Production implementation, regeneration, refreshed
canonical native proofs, and verification hashes remain the implementer's work. The small
signaling `site A` label is a separate already-recorded projection issue, not a cause of
this chart failure.
