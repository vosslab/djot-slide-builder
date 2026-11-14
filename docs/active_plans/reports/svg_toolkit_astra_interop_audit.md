# SVG toolkit Astra interoperability audit

Date: 2026-11-13

## Scope and evidence

Astra reviewed interoperability across the SVG toolkit and ran 71 focused tests. A nested plot and
icon composition retained 80 unique IDs, 28 references, 20 live text elements, and license
information; Matplotlib `rcParams` were restored. A transformed nonzero-viewBox example had the
expected pixel bounding box `(20, 60, 100, 220)`.

A static trace followed the CLI through native XML and ZIP assembly, including marker root handling.
The ODP output root is `output/odp`. This trace did not invoke LibreOffice or verify an actual native
export; M25 owns that verification.

## Finding and correction

Astra found that ordinary labels could collapse multiple spaces in SVG rendering even though advance
measurement accounted for them. `text.label` was corrected to preserve XML whitespace, and 12
regression tests passed. A fresh review remains pending; the correction has not yet been claimed as
rendered and accepted.

An earlier M15 quality review failed the ER illustration: its network needed connected geometry,
six openings, and explicit contact with the nucleus. The correction addresses those features and
documents lysosome and vesicle outlines as generic. Fresh specification and quality reviews passed,
with three focused tests.

The import comment-mask cleanup was removed because the shared namespacing implementation preserves
comments. Required type annotations were completed in four files; 23 focused tests passed.

## Remaining work

- Regenerate the gallery and pilots, including all 23 canonical SVG outputs, under the serial owner.
- Complete fresh core and documentation reviews of the latest corrections.
- Verify actual native output in M25, run fresh independent trials in M26, and complete M27 closeout.

The M19 catalogue, cookbook, 17-SVG and 17-WebP gallery, index, and native 17-slide deck are
assembled and remain in review. M20-M24 passed specification and quality review. The M22, M23, and
M24 pilot records contain respectively two, one, and seven source URLs with hashes; their original
SVGs were unchanged.
