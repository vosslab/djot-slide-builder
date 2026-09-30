# Bundled presentation fonts

The slide compiler measures and emits only the files declared in
`slide_lib.presentation_theme.FONT_FACE_PROFILES`. The repository validates each file's SHA-256
before loading the theme. Base-face selection never queries the operating system. The rendering
backend may substitute individual glyphs absent from a selected face; Djot contains no font choices.
[`font_provenance.json`](font_provenance.json) is the machine-readable record of every source URL,
pinned revision, asset hash, face index, and local license hash.

## Atkinson Hyperlegible Next

- Upstream: [official Atkinson Hyperlegible Next source](https://github.com/googlefonts/atkinson-hyperlegible-next)
- Pinned revision: `7925f50f649b3813257faf2f4c0b381011f434f1`
- License: SIL Open Font License 1.1; full text:
  [licenses/Atkinson-Hyperlegible-Next-OFL-1.1.txt](licenses/Atkinson-Hyperlegible-Next-OFL-1.1.txt)
- Bundled faces: Regular, Bold, Italic, and Bold Italic version 2.001 static TTF files in
  `atkinson_hyperlegible_next/`.

## Atkinson Hyperlegible Mono

- Upstream: [official Atkinson Hyperlegible Mono source](https://github.com/googlefonts/atkinson-hyperlegible-next-mono)
- Pinned revision: `154d50362016cc3e873eb21d242cd0772384c8f9`
- License: SIL Open Font License 1.1; full text:
  [licenses/Atkinson-Hyperlegible-Mono-OFL-1.1.txt](licenses/Atkinson-Hyperlegible-Mono-OFL-1.1.txt)
- Bundled faces: Regular, Bold, Italic, and Bold Italic version 2.001 in
  `atkinson_hyperlegible_mono/`.

## IBM Plex Sans Condensed

- Upstream: [Google Fonts ofl/ibmplexsanscondensed](https://github.com/google/fonts/tree/main/ofl/ibmplexsanscondensed)
- Pinned revision: `9a7e4a0cbf313f8a1774725977c00274fcb7815b`
- License: SIL Open Font License 1.1; full text:
  [licenses/IBM-Plex-Sans-Condensed-OFL-1.1.txt](licenses/IBM-Plex-Sans-Condensed-OFL-1.1.txt)
- Bundled faces: Regular, Bold, Italic, and Bold Italic version 1.3 in `ibm_plex_sans_condensed/`.

## Generated ODP resources

Generated ODPs embed the original bundled font bytes unchanged. Editable text uses the public
families Atkinson Hyperlegible Next, Atkinson Hyperlegible Mono, and IBM Plex Sans Condensed,
so LibreOffice shows the same names users know from their installed fonts. Internal ODF resource
identifiers are not font family names.

The machine-readable provenance records each original file's SHA-256. Export validates that
hash before embedding; there are no renamed derivatives or separate derivative hashes.

Every generated ODP also carries the applicable OFL notice texts under `Fonts/licenses/` with
their manifest entries. This keeps the notices beside the distributed fonts as required by
OFL condition 2.

## Code runs

Inline code uses Atkinson Hyperlegible Mono in both measurement and output. Authors request this
semantic role with backticks, including inside links. Literal URL labels use IBM Plex Sans
Condensed unless explicitly marked as code. Ordinary link labels retain Atkinson Hyperlegible Next.
