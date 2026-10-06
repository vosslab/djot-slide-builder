# Track image shrinkage during conversion

Status: audit implemented; layout remedies and automatic trimming deferred. The instructor clarified
that audit code is welcome but new special layouts are not requested.

## Observed example

Genetics Lecture 06D, slide 9: red-eyed and white-eyed Drosophila photographs.
The original gives the photograph much more prominence than the converted slide.
A one-time comparison of the original ODP image frame and the compiled Djot image rectangle found:

| Measurement | Value |
| --- | ---: |
| Original image area as a fraction of the slide | 47.19% |
| Converted displayed image area as a fraction of the slide | 12.13% |
| Change in slide coverage | -35.06 percentage points |
| Relative image area reduction | 74.29% |

The identical image bytes were matched in both sources. Exact white-border detection found only
about 0.27% empty area, so trimming alone would not resolve this example. These measurements use
image rectangles, not a measure of the visual content within the photograph.

## Requested future behavior

- Compare displayed image area as a percentage of the slide before and after conversion.
- Flag changes beyond a threshold for review, without assuming every intentional resize is wrong.
- Investigate automatic border trimming, such as `mogrify -trim`, as a separate improvement.
- Review image-and-text allocation using existing layouts; do not add special layouts for this work.
- Preserve labels and artwork when trimming; keep original assets and account for crop offsets.

The initial default warning threshold is a 30% relative reduction, an agent-selected starting point
that can be adjusted with `--loss-threshold`. Warnings are non-blocking. Both relative reduction
and percentage-point change are reported. Repeated uses of identical artwork on one slide are
aggregated; changed artwork, SVG composites, and transformed frames require manual review.

Run `python3 deck_tools.py image-audit SOURCE.odp CONVERTED.djot --loss-threshold 30` after
activating the repository environment. Sources must retain matching slide order and count.
New imports also store the measurements in `import_report.json` and print shrinkage warnings.
If compilation cannot measure the output, the report records the audit error rather than a pass.

The audit compares original frame area with actual aspect-fitted compiled image area, not an
allocated slot. Exact-white/transparent border measurements are suggestions only. Cropped source
artwork and overlays can make frame area differ from meaningful visual area. No automatic trimming
or layout changes occur. Existing decks can be audited without rebuilding or editing them.
