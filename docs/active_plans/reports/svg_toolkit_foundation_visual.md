# SVG toolkit foundation visual review

Reviewed the existing generated SVGs using `rsvg-convert` with `PANGOCAIRO_BACKEND=fc`, then composited onto white and saved as quality 90 WebP. Previews were visually inspected at the dimensions below. Fontconfig resolves both Atkinson Hyperlegible Next and Atkinson Hyperlegible Mono to installed Atkinson font files.

| Example | Result | Source viewport | Preview dimensions | Preview |
| --- | --- | --- | --- | --- |
| Placement | PASS | 250 × 180 | 1000 × 720 px | `_temp/svg_toolkit/foundation/placement_preview.webp` |
| Text labels | PASS | 500 × 150 | 1500 × 450 px | `_temp/svg_toolkit/foundation/text_labels_preview.webp` |
| Curve samples | PASS | 360 × 260 | 1080 × 780 px | `_temp/svg_toolkit/foundation/curve_samples_preview.webp` |

Placement shows two complete chromosomes with preserved proportions, the second rotated consistently with its label and centromere; no viewport clipping is visible. The purple centromere outline touches the edge of the upper A, an intentional-looking overlay that may merit adjustment if label separation is desired.

Text labels are legible and complete, including Greek letters, bold italic text, and the monospaced sequence. Their appearance and fontconfig resolution are consistent with the requested Atkinson families; visual inspection alone does not prove the font selected for every glyph.

Curve samples show complete repeated circles and tangent marks, with each mark following the local curve direction and no visible clipping. Spacing appears even along the curve.

This checks the existing SVGs through librsvg on this host, not native LibreOffice imports or exports, other renderers, or every possible geometry and font environment.
