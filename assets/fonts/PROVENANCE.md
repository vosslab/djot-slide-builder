# Bundled presentation fonts

The slide compiler measures and emits only the files declared in
`slide_lib.presentation_theme.FONT_FACE_PROFILES`. The repository validates each file's SHA-256
before loading the theme. It never queries the operating system for a replacement face.
[`font_provenance.json`](font_provenance.json) is the machine-readable record of every source URL,
pinned revision, asset hash, face index, and local license hash.

## Atkinson Hyperlegible Next

- Upstream: [official Atkinson Hyperlegible Next source](https://github.com/googlefonts/atkinson-hyperlegible-next)
- Pinned revision: `7925f50f649b3813257faf2f4c0b381011f434f1`
- License: SIL Open Font License 1.1; full text:
  [licenses/Atkinson-Hyperlegible-Next-OFL-1.1.txt](licenses/Atkinson-Hyperlegible-Next-OFL-1.1.txt)
- Bundled faces: Regular, Bold, Italic, and Bold Italic version 2.001 static TTF files in
  `atkinson_hyperlegible_next/`.

## PT Sans Narrow

- Upstream: [Google Fonts ofl/ptsansnarrow](https://github.com/google/fonts/tree/main/ofl/ptsansnarrow)
- Pinned revision: `baa2e5561af8a4873b058859dcfe158bdd033942`
- License: SIL Open Font License 1.1; full text:
  [licenses/PT-Sans-Narrow-OFL-1.1.txt](licenses/PT-Sans-Narrow-OFL-1.1.txt)
- Bundled faces: Web Regular 2.003W OFL and Web Bold 2.003W OFL in `pt_sans_narrow/`.
- Google Fonts publishes no italic PT Sans Narrow face. A URL run needing italic must be rejected
at style selection; this boundary does not synthesize slant or map it to another face.

## Generated ODP resources

Generated ODPs derive package-only copies with the unique families
`DjotAtkinsonHyperlegibleNext` and `DjotPTSansNarrow`. The derivation changes only name-table
identity; it retains each pinned asset's outlines and metrics. This prevents a same-name
operating-system font from replacing the measured font while keeping the repository asset and its
provenance immutable.

The machine-readable provenance records the exact recipe
`TTFont(recalcTimestamp=False); rename name IDs 1, 4, 6, and 16 only` and the
SHA-256 of every resulting package derivative. Export validates those hashes before publication.

Every generated ODP also carries the two applicable OFL notice texts under `Fonts/licenses/` with
their manifest entries. This keeps the notices beside the distributed derivatives as required by
OFL condition 2.

## Code runs

Inline code is deliberately emitted in Atkinson Hyperlegible Next under the project typography
policy. No monospace face is currently emitted, so none is bundled. A future change that emits a
code family must add its licensed asset, provenance, and immutable profile before the layout
measurement owner can select it.
