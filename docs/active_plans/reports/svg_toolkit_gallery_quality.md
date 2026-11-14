# SVG toolkit gallery and plot quality review

**M19 QUALITY PASS**, subject to final regeneration and the separate M26 fresh-user trials.
**Plot and sequence-spacing fix: PASS** on the focused checks below.

The catalogue provides task-to-module routes, explicit coordinate and bounds contracts, a direct `SvgPart` escape hatch, reconstruction instructions to preserve source information, and a warning to inspect final slides. The cookbook supplies runnable new-figure, reconstruction, plot, icon, and slide examples; the toolkit README links to the catalogue. The gallery builder enumerates 17 examples, and the showcase references all 17 corresponding SVGs with native caption text. The plot recipe's generation, p, and q arrays match its example source and plotted locations. The sample SVG path in the slide snippet is intentionally relative to its generated temporary deck.

I inspected the gallery index and full-size signaling, cells, organelles, allele-frequency, and icon previews. Full-size labels and plotted axes are legible, with no evident clipping; the index is a navigational overview, and its small internal labels are not intended for reading. Signaling shows separate activity and phosphorylation states, and the organelle legend identifies generic lysosome and vesicle shapes. The 17 SVG files parse as XML, each has a WebP preview, and each is referenced by the showcase. Other families have separate reviews.

A fresh `text.label` rendering with the sequence role preserved the distinction between `A   G` and `A G`: their ink bounding boxes were respectively `(21, 47, 170, 81)` and `(21, 47, 109, 81)` pixels; measured end anchors were 171.68 and 111.01. The two-space advance difference agrees with the visible separation and conservative bounds. Evidence is in `_temp/svg_toolkit/gallery_quality/{three,one}.{svg,png}`. Rendering used `rsvg-convert` with `PANGOCAIRO_BACKEND=fc` and a white background. The implementation emits `xml:space="preserve"`.

Focused plot and text tests: `MPLCONFIGDIR="$PWD/_temp/mplconfig" PYTHONPATH="$PWD:$PWD/tests" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest tests/test_svg_plots.py tests/test_svg_text.py` — **6 passed**. The plot tests cover editable labels, data and font-property preservation, raster rejection, and repeatability without `SOURCE_DATE_EPOCH`.

Limits: the final byte-hash manifest awaits canonical regeneration after import-only cleanup. This review does not establish native ODP/PDF rendering or actual LLM recipe usability; M25 and M26 remain separate gates. Index and preview appearance was checked on the current artifacts, not a subsequent regeneration.
