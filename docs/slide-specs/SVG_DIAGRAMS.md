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
- Use a transparent canvas so the slide background shows through. Crop unused outer space while
  keeping labels, strokes and arrowheads clear of the viewport edge. Preserve white fills that
  belong to biological structures, annotation panels or embedded source images.
- Embed PNG/JPEG component artwork with data URIs. Preserve transparency and source geometry.
- Keep labels as text, with explicit coordinates, fonts, sizes, and subscript positioning.
- Apply the font roles in [HUMAN_GUIDANCE.md](../HUMAN_GUIDANCE.md): Atkinson Hyperlegible Next for
  ordinary SVG text, Atkinson Hyperlegible Mono for monospace and IBM Plex Sans Condensed for
  narrow text. Use the installed families by name; keep font files out of individual SVGs.
- Use simple shapes/paths and flat live text. Add a text outline only when it improves readability.
- Keep leaders and arrows as vector paths. Use stable group and element IDs for later edits.
- Use static, self-contained content; external resources, scripts, and foreign objects are rejected.
- The ODP contains the original SVG bytes with `image/svg+xml` MIME type. Sizing reads the SVG
  viewport directly; there is no PNG conversion step. LibreOffice produces the PDF.

An embedded bitmap retains its original resolution; wrapping it in SVG does not add detail.

## Drawing and image-wrapper filenames

- Use `name.drawn.svg` for a reviewed original drawing composed of vector shapes and text.
  Git permits this suffix. Lint and builds reject `image` and `feImage` elements anywhere
  inside it, including nested SVGs and filter definitions.
- Use `name.image.svg` for a reviewed SVG with embedded images. Git permits this suffix.
  Examples include original generator captures and the C31 chromosome staining figure.
- Keep SVGs awaiting provenance review under ordinary `name.svg` filenames, which Git ignores.
  Review ownership and redistribution rights before tracking a figure under either suffix.

If validation finds an image inside `.drawn.svg`, use an ordinary `.svg` filename and retain
the file locally, ignored, until its provenance supports tracking. Do not remove source or
copyright information to pass this check. Git ignore rules do not untrack existing files;
`git rm --cached -- PATH` stops tracking while preserving the local file. This does not remove
previous versions from Git history.

The October 31, 2026 migration renamed 31 reviewed drawings with unchanged bytes and stopped
tracking 38 image wrappers while preserving them locally. The reviewed captures that had file
exceptions now use `.image.svg`, along with the handout preview and C31.

ODP import prefers original metafiles over raster previews and converts them directly to SVG.
Failures and converted figures without live text receive review reasons. The measured behavior
and LibreOffice compatibility corrections are recorded in
[../archive/metafile_vector_followup.md](../archive/metafile_vector_followup.md).

Existing labels already baked into source artwork remain raster labels. Newly reconstructed labels
are editable text. Review both at presentation scale, particularly after changing crops or fonts.

### Normalize a drawn SVG

Run the normalizer from the repository root with `rsvg-convert` installed:

```bash
source source_me.sh
python3 -m svg_tools.normalize_svg path/to/*.drawn.svg
python3 -m svg_tools.normalize_svg --write path/to/*.drawn.svg
```

The first command reports the proposed edits. With `--write`, the tool removes a plain
canvas-sized rectangle behind the artwork and fits the viewport to the painted content with
10 SVG units of clearance where available. `--padding` sets that clearance. Text, shapes,
and internal fills stay editable. The tool measures static drawings with absolute viewports.
Review other background constructions by hand, and inspect the exported slide after cropping.
Recipes that use `svg_tools.drawing.write_svg` can set `crop=True` to normalize before saving.

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

Start with one candidate, one original SVG and one direct preview at intended display size.
Brief artist and manager review checks taught relationships, labels, leaders, subscripts,
transparency and figure boundaries. Keep captions and surrounding prose native; use the known
image frame when available.

Use extra sizes, independent review or a targeted consumer/export check for a concrete concern:
a known LibreOffice SVG failure, crop, overlay, reveal or uncertain image frame. Inspect only the
placement and context needed to resolve it. Complete ordinary art milestones through the brief
review and image-URL integration; classroom, playback, printing and instructor feedback are optional.

Keep source provenance in [slide development notes](AUTHORING_GUIDE.md#slide-development-notes).
Use `@speaker-notes` for instructor delivery cues. Retain `@replaceme` where teaching relationships
or reveals still need reconstruction, and record unresolved targets with a reason.

Lecture 06 results and remaining work are recorded in
[../../genetics/LECT06/djot/LECT06_REVIEW.md](../../genetics/LECT06/djot/LECT06_REVIEW.md).
