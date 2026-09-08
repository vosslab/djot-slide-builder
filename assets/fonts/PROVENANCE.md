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
- Bundled faces: Regular, Bold, Italic, and Bold Italic in `opendyslexic/`.

## PT Sans Narrow

- Upstream: [Google Fonts ofl/ptsansnarrow](https://github.com/google/fonts/tree/main/ofl/ptsansnarrow)
- Pinned revision: `baa2e5561af8a4873b058859dcfe158bdd033942`
- License: SIL Open Font License 1.1; full text:
  [licenses/PT-Sans-Narrow-OFL-1.1.txt](licenses/PT-Sans-Narrow-OFL-1.1.txt)
- Bundled faces: Web Regular and Web Bold in `pt_sans_narrow/`.
- Google Fonts publishes no italic PT Sans Narrow face. A URL run needing italic must be rejected
  at style selection; this boundary does not synthesize slant or map it to another face.

## Code runs

Inline code is deliberately emitted in OpenDyslexic under the project typography policy. No
monospace face is currently emitted, so none is bundled. A future change that emits a code family
must add its licensed asset, provenance, and immutable profile before the layout measurement owner
can select it.
