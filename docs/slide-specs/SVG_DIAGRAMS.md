# SVG diagram components

Use a self-contained SVG for a labeled diagram: embedded original artwork, editable SVG text,
and vector leaders or arrows. Compose one artwork image with its associated labels; labels may
extend beyond the image rectangle. Size the SVG viewport to include those labels and leaders.
Keep slide titles, captions, and explanatory prose in native Djot text boxes. The SVG remains
one image object in Impress; edit its labels in the SVG source rather than as Impress text boxes.
Do not convert a complete slide into a bitmap to preserve its layout.

## Asset contract

- Store SVGs beside the deck's other local assets. Include a title, description, and source slide.
- Supply positive absolute width/height or a finite, positive-size `viewBox`.
- Embed PNG/JPEG component artwork with data URIs. Preserve transparency and source geometry.
- Keep labels as text, with explicit coordinates, fonts, sizes, and subscript positioning.
- Keep leaders and arrows as vector paths. Use stable group and element IDs for later edits.
- Use static, self-contained content; external resources, scripts, and foreign objects are rejected.
- The ODP contains the original SVG bytes with `image/svg+xml` MIME type. Sizing reads the SVG
  viewport directly; there is no PNG conversion step. LibreOffice produces the PDF.

An embedded bitmap retains its original resolution; wrapping it in SVG does not add detail.

## Drawing and image-wrapper filenames

- Use `name.drawn.svg` for a reviewed original drawing composed of vector shapes and text.
  Git permits this suffix. Lint and builds reject `image` and `feImage` elements anywhere
  inside it, including nested SVGs and filter definitions.
- Keep image-containing figures as ordinary `name.svg` files. Git ignores these by default.
  The exact-file exceptions in [.gitignore](../../.gitignore) cover reviewed captures of our own
  generator artwork; importing or repairing textbook art does not qualify it for an exception.
- Review ownership separately. Image-free geometry and the `.drawn.svg` suffix do not prove
  that a drawing is original or that its source permits redistribution.

If validation finds an image inside `.drawn.svg`, use an ordinary `.svg` filename and retain
the file locally, ignored, until its provenance supports tracking. Do not remove source or
copyright information to pass this check. Git ignore rules do not untrack existing files;
`git rm --cached -- PATH` stops tracking while preserving the local file. This does not remove
previous versions from Git history.

The October 31, 2026 migration renamed 31 reviewed drawings with unchanged bytes and stopped
tracking 38 image wrappers while preserving them locally. Fifteen original-generator captures
remain explicit tracking exceptions. Earlier vector assets retain their existing filenames.

ODP import prefers original metafiles over raster previews and converts them directly to SVG.
Failures and converted figures without live text receive review reasons. The measured behavior
and LibreOffice compatibility corrections are recorded in
[../archive/metafile_vector_followup.md](../archive/metafile_vector_followup.md).

Existing labels already baked into source artwork remain raster labels. Newly reconstructed labels
are editable text. Review both at presentation scale, particularly after changing crops or fonts.

## Comparison layout

`image-comparison` gives two diagrams equal-width upper slots and two native captions a shared
lower row. Caption measurement determines the lower row height; diagrams receive the remaining
space and retain their aspect ratios. Each upper slot accepts one image. Each lower slot accepts
one or two paragraphs. A title is optional. Ordinary `four-panels` behavior is unchanged.

```djot
=== layout: image-comparison

# M checkpoint

@top-left

![Stop state](assets/checkpoint_stop.svg)

@top-right

![Go-ahead state](assets/checkpoint_go.svg)

@bottom-left

Without full chromosome attachment, a stop signal is received.

@bottom-right

With full chromosome attachment, a go-ahead signal is received.
```

Keep short identifying labels within the SVG. Keep conclusions, conditions, and teaching prompts
in the caption slots. If a figure depends on shared stage labels, preserve those labels when
splitting it; a single larger SVG can be preferable to two ambiguous fragments.

## Definition emphasis

Use `[*Sister chromatids*]{underline=true}` for bold, underlined terms. Selective color composes
with both: `[*Homologous chromosomes*]{color=blue underline=true}`. The definition remains plain
text. Inherited ODF bold and underline are retained by import; explicit normal/none resets prevent
formatting from leaking into the rest of a paragraph. Unknown span attributes are rejected.

## Visual acceptance

Record rejected LLM drawings and their repair targets in
[../SVG_REPAIR_BACKLOG.md](../SVG_REPAIR_BACKLOG.md). Keep exact asset paths and distinguish
completed removals from drawings still in use with replacement recommended.

Compare each repaired slide with its original source and the actual exported PDF. Check labels,
leaders, subscripts, transparency, crop boundaries, and readable captions. Confirm direct SVG
packaging in ODP. Keep source provenance in separate import reports, slide maps, or review files,
not in Djot notes or comments. Reserve `@notes` for instructor notes. Retain `@replaceme` where the original
teaching relationships or reveal sequence still need reconstruction.

Lecture 06 results and remaining work are recorded in
[../../genetics/LECT06/djot/LECT06_REVIEW.md](../../genetics/LECT06/djot/LECT06_REVIEW.md).
