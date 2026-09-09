# Bundled presentation fonts

The slide compiler measures and emits only the files declared in
`slide_lib.presentation_theme.FONT_FACE_PROFILES`. The repository validates each file's SHA-256
before loading the theme. It never queries the operating system for a replacement face.
[`font_provenance.json`](font_provenance.json) is the machine-readable record of every source URL,
pinned revision, asset hash, face index, and local license hash.

## OpenDyslexic

- Upstream: [official OpenDyslexic source](https://forge.hackers.town/antijingoist/opendyslexic)
- Pinned revision: `48218028cc8bd9f4f244cd4ce4049e6c879d4d1a`
- License: SIL Open Font License 1.1; full text:
  [licenses/OpenDyslexic-OFL-1.1.txt](licenses/OpenDyslexic-OFL-1.1.txt)
- Bundled faces: Regular 0.990, Bold 0.990, Italic 0.950, and Bold Italic 0.940 in
  `opendyslexic/`. These are the hash-pinned OFL assets selected by the repository. The locally
  installed OpenDyslexic 2.001 identifies CC BY 3.0 in its internal records; no official,
  downloadable OFL 2.001 artifact and hash is established here.

## PT Sans Narrow

- Upstream: [Google Fonts ofl/ptsansnarrow](https://github.com/google/fonts/tree/main/ofl/ptsansnarrow)
- Pinned revision: `baa2e5561af8a4873b058859dcfe158bdd033942`
- License: SIL Open Font License 1.1; full text:
  [licenses/PT-Sans-Narrow-OFL-1.1.txt](licenses/PT-Sans-Narrow-OFL-1.1.txt)
- Bundled faces: Web Regular 2.003W OFL and Web Bold 2.003W OFL in `pt_sans_narrow/`.
- Google Fonts publishes no italic PT Sans Narrow face. A URL run needing italic must be rejected
at style selection; this boundary does not synthesize slant or map it to another face.

## Generated ODP resources

OpenDyslexic and PT Sans carry reserved names in their OFL records. Generated ODPs therefore
derive a package-only copy with the unique families `DjotOpenDyslexic` and `DjotPTSansNarrow`.
The derivation changes only name-table identity; it retains each pinned asset's outlines and metrics.
This prevents a same-name operating-system font from replacing the measured font while keeping the
repository asset and its provenance immutable.

The machine-readable provenance records the exact recipe
`TTFont(recalcTimestamp=False); rename name IDs 1, 4, 6, and 16 only` and the
SHA-256 of every resulting package derivative. Export validates those hashes before publication.

Every generated ODP also carries the two applicable OFL notice texts under `Fonts/licenses/` with
their manifest entries. This keeps the notices beside the distributed derivatives as required by
OFL condition 2.

## Code runs

Inline code is deliberately emitted in OpenDyslexic under the project typography policy. No
monospace face is currently emitted, so none is bundled. A future change that emits a code family
must add its licensed asset, provenance, and immutable profile before the layout measurement owner
can select it.
