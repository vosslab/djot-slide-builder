# Protected raster inputs correction

Three production JSON raster payloads are now explicit sibling-file references. Runtime recipes hydrate the original data URIs from ignored local inputs. Canonical SVGs and copyright/provenance metadata remain unchanged. Plain *.svg and *.png ignore rules already protect these inputs; no ignore exceptions or Git commands were used.

## Exact inputs

- Source: `genetics/LECT13/djot/lect13bc_chromosome_sources.json`
- Local input: `genetics/LECT13/djot/lect13bc_inversion_exercise_source.png`
- Original MIME: `image/png`; decoded bytes: 89210
- Raster SHA-256: `21eec189a0b24c096a7f2c19a7ef9eb9fd74f77c8877f5a9c38ea107d50822a6`
- Full original URI SHA-256: `8880704ca318743c60f3e8c486b3fd874bdde7c7cead2325e56f3a8a59b48cfe`
- Canonical artwork: `genetics/LECT13/djot/assets/lect13b-chromo_alter_3-inversion/inversion_problem_829_exercise.svg`

- Source: `genetics/LECT08/djot/chromosome_recipes/b31_sources.json`
- Local input: `genetics/LECT08/djot/chromosome_recipes/b31_micrograph_source.svg`
- Original MIME: `image/webp`; decoded bytes: 40802
- Raster SHA-256: `5eda5d637753a9aa0ed6a4594adc29ff3797193ed39c43de5a9672120e989a35`
- Full original URI SHA-256: `7063b8031bce66ea2c1b20fc9db0cc9084166ed84243f931755ca68e69623a21`
- Canonical artwork: `genetics/LECT08/djot/assets/lect08b-chap8-linked_genes/b31_labeled.svg`

- Source: `genetics/LECT13/djot/lect13b_loop_chromosome_sources.json`
- Local input: `genetics/LECT13/djot/lect13b_inversion_loop_callout.png`
- Original MIME: `image/png`; decoded bytes: 9961
- Raster SHA-256: `7ea982fcd7dd45381f1003b56febe172a23b67b0436025bb6712c108494bd471`
- Full original URI SHA-256: `2672b31b03240234b5ee248fca0434f9775bacf495b29bd6a5748ba1c4fc459a`
- Canonical artwork: `genetics/LECT13/djot/assets/lect13b-chromo_alter_3-inversion/image_006_replacement.svg`

The b31 input is a valid normal SVG wrapper containing the exact original image/webp data URI and its positive 492.6050109863281 by 467.8770046234131 viewport. It is not a drawn.svg or a mislabeled PNG. The recipe reads its known image href. Both LECT13 inputs are exact decoded PNGs, encoded at runtime with standard-library base64. The loop callout_png field now names its sibling PNG input.

## Verification

- Original BC, b31 and loop recipes were regenerated before mutation. All 25 affected recipe outputs matched canonical SVG bytes.
- Updated recipes regenerated all 15 BC outputs, 9 loop outputs and b31: all 25 match both baseline and canonical bytes exactly.
- All 12 LECT08 recipes regenerated all 16 outputs and matched canonical bytes. Combined BC24 plus LECT08 gives 40/40 unchanged current SVG hashes.
- Clean copied local package regenerated all 25 affected recipe outputs from redirected locations with identical canonical bytes.
- All three original raster SHAs and full data-URI SHAs were verified against current canonical SVG embeddings.
- Pyflakes passes for all three recipes. Existing executable modes, shebangs, and typed signatures retained.
- Whole production scan: 466 discoverable JSON/Python files, excluding ignored scratch/output files. URI-prefixed and bare base64 strings were decoded and checked for PNG/JPEG/WebP/GIF magic. Zero raster payload literals remain.
- Additional prepromotion scan of _temp/chromosome_migration/lect06 and _temp/chromosome_migration/lect0813/lect13d_attachment_v3 found zero raster base64 literals in their JSON/Python files. Staged roots were not modified.

## Evidence

- payload_manifest.json: exact MIME, decoded raster hashes, original data-URI hashes, and canonical SVG mapping.
- svg_manifest.json: unchanged hashes for all 40 current outputs.
- package_manifest.json: current local package paths, hashes and modes, including all three ignored private inputs and existing b31 destinations.json.
- production_scan.json: clean whole-production JSON/Python raster scan.
- staging_scan.json: clean prepromotion scan of LECT06 and LECT13D v3 roots.

## Packaging and acceptance

Include both PNGs and the normal SVG wrapper in the self-contained local runtime package. They intentionally remain ignored in public Git; public source JSON/Python does not embed their raster payloads. The frozen v1 review package was not altered. Current source/package metadata hashes change, but all reviewed artwork bytes remain identical; current native artwork acceptance remains applicable.

No LibreOffice, slide URL, Djot, source artwork, .gitignore, frozen snapshot, or canonical output writes were made. No broader suite or fresh image render was run because output bytes are identical.
