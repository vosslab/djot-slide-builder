# Preserve vector metafile figures

Status: implemented and checked on October 6, 2026. No new layouts introduced.

The instructor's genotype-notation table is sharp in the source presentation but pixelated after
conversion. Preserve text as glyphs rather than pixels; investigate GDI/metafile to SVG conversion.

## Original behavior

`slide_lib/importers/odp_metafile.py` handles SVM, EMF, and WMF component files.
`frame_image` prefers an embedded PNG/JPEG/GIF preview over the original metafile. If no preview
exists, `raster_image` wraps the component in an ODG and exports PNG through LibreOffice, targeting
roughly 1600 pixels on its longest side. A small embedded preview bypasses that conversion entirely.

## Implemented conversion

The importer now prefers the original SVM/EMF/WMF or SVG over alternate raster previews.
Metafiles use the existing component-only ODG wrapper and sequential LibreOffice converter,
exporting SVG at original geometry. SVG assets pass the shared static/self-contained validation
and are embedded directly in ODP. No PNG intermediate is used.

Conversion failures create explicit source review reasons rather than silently choosing a preview.
Converted SVGs with no live text also require review: they may contain outlines or bitmap content.
The importer does not claim that every SVG has preserved text merely because its suffix is SVG.

Two observed export quirks required small corrections:

- Remove LibreOffice's exact unused external SVG DTD declaration before shared validation.
  Other DTDs remain rejected; external resources are not fetched.
- Correct spurious `direction="rtl"` flags in figures with no strong RTL characters. The original
  exported left-edge positions then render correctly. Figures with RTL text retain their direction.

## Experiments and evidence

| Source slide | SVG text elements | Vector paths | Bitmap images |
| --- | ---: | ---: | ---: |
| Lecture 06D 13: genotype notation | 56 | 34 | 0 |
| Lecture 06D 56: unfilled pigeon cross | 4 | 18 | 0 |
| Lecture 06D 57: filled pigeon cross | 8 | 18 | 0 |

Element counts alone were insufficient: the first PDF showed displaced headers and superscripts
because of the direction flags. The corrected PDF was visually inspected and its text extracted.
Headers, allele case, superscript plus signs, X-linked notation, and rules remain legible vectors.
The original source's wording, including its spelling, was retained.

A complete import of a temporary one-slide source copy published one SVG with no review reasons.
The three canonical Lecture 06D image references now use SVG; existing layouts and the replacement
markers on slides 56-57 remain. Original presentations and raster assets are preserved.

Validation: 48 focused tests pass, including original-over-preview preference, explicit conversion
failure, SVG package preservation, and Latin/RTL direction handling. Strict Djot lint passes.
All 46 referenced Lecture 06 SVGs match their packaged ODP bytes; all 203 pages and 22 markers
remain accounted for. New/changed module Pyflakes checks pass.

Local experiment evidence is in `output/metafile_svg_experiment/`: raw exports, acceptance counts,
the temporary source/import, and `genotype_export.png`. Final output is
`output/odp/lect06d-x_linked_genes_1.odp` and `output/pdf/lect06d-x_linked_genes_1.pdf`.

## Preserved requirements

- Prefer original vector data over a raster preview.
- Investigate exporting the component ODG to SVG through LibreOffice.
- Inspect actual SVG output: an SVG containing only a bitmap does not solve this problem.
- Prefer SVG text with preserved characters, superscripts, positions, and font information.
  Glyph outlines retain sharpness but lose text search/editing; report that distinction.
- Preserve vector table rules and fills, and retain any genuine embedded photographs as images.
- Check native ODP embedding and exported PDF at presentation size and high zoom.
- Identify unsupported conversion explicitly rather than silently accepting a low-resolution preview.

Use the "Different Representation of Genotypes" table as an acceptance example: verify allele
case, superscript plus signs, X-linked notation, borders, and source text. A higher-resolution PNG
could improve appearance temporarily but does not meet the vector/text-preservation objective.

Live visual acceptance covered these three SVM figures. EMF/WMF use the same converter but have
not received equivalent live acceptance here. Font availability can affect appearance; the result
retains the fonts chosen by the converter. No universal fidelity claim or new layout is needed.
