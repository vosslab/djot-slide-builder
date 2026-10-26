# Mixed-content conversion strategy review

Date: 2026-10-26.

## Implemented strategy

A panel groups a teaching sequence, not a fixed number of objects. The normative
[mixed-content example](../../DJOT_SLIDE_SYNTAX.md#mixed-content-in-one-panel) shows PNG,
editable text, and SVG in one `@body`. The conversion workflow now explicitly asks reviewers to
try that arrangement for sequential content before assigning one region per object or marking
an otherwise representable layout for replacement.

The existing planner already recognized vertical mixed flows, but caption pairing ran first.
For LECT07B slide 24, the PNG and following sentence became a caption pair, leaving the SVG
in a second equal-height region. Vertical-flow recognition now runs first for non-table content.
It uses the existing separation and horizontal-alignment evidence and existing emitter; it
introduces no layout name, lecture-specific rule, or manual geometry. Side-by-side content,
image-owned annotations, spatial reconstructions, and native tables retain their existing paths.

Import staging also measures mixed flows through the shared compiler. Failed bounds add
`@replaceme` to generated source and a recommendation to split in the import report, preserving
other reasons and hidden state. Existing markers are not duplicated. Authored teaching prose is
not rewritten. The compiler continues to add its visible review watermark and split note.

## Evidence

Temporary original-ODP extraction and before/after evidence live in `_temp/mixed_conversion/`.
Original B/C/D ODPs were read outside the sandbox because metafile extraction can invoke
LibreOffice. Cached source facts were re-planned with the new precedence; supported text reveal
flags retained on source slot regions were carried into that comparison.

| Deck | Source slides changed from stacked to one panel | Before/after marked-slide counts |
| --- | --- | --- |
| LECT07B | 24, 34 | 18 / 18 |
| LECT07C | 12, 27 | 18 / 19 |
| LECT07D | None | 32 / 32 |

No existing review reason was cleared. C32 gains a readability/split reason. Other crowded
slides gain the same reason alongside existing reasons without changing the marked-slide count.
This experiment confirms better grouping; it does not establish that this narrow automatic
change rescues existing replacement slides. Human review can apply the documented strategy
more broadly where source spatial meaning is understood.

Five editable ODP/PDF exports were rendered and visually inspected: B24 before/after, B34 after,
C12 after, and C27 after. All five compile without capacity concerns. The contact sheet is
`_temp/mixed_conversion/conversion_examples.png`; the imported B24 after example retains the
PNG/sentence/SVG sequence with larger figures. Source wording and scientific expressions,
including any original inconsistencies, were preserved.

Both baseline and revised raw B/C drafts have an existing semantic validation failure on a slide
with more than six component images. The changed drafts have the same failure; D passes semantic
lint. These full raw drafts are diagnostic evidence, not accepted re-imports. Existing reviewed
LECT07 Djot and published lecture outputs were not replaced.

## Six images

Six is the supported per-slide image limit. Six images in one mixed panel are independently
allocated, with at most 6 * 2^5 = 192 endpoint candidates per font, or 3,264 across the current
17 half-point font sizes. A temporary six-strip-image specimen fits without a replacement
requirement, with widths approximately 100%, 73.3%, and four at 71.4% of panel width; its cold
compile took about 58 ms on this host. Tall images may instead require splitting. Image-only
panels and gallery layouts retain their own rules.

## Checks

- `source source_me.sh && python3 -m pytest -q tests`: 1,299 passed.
- New durable coverage: mixed sequence before caption pairing; original animation reasons
  survive; crowded visible/hidden drafts receive source markers and report split guidance;
  marker insertion preserves prose and remains idempotent. Existing column/table tests pass.
- Five selected source-import examples rendered through repository exporters outside the sandbox.
- Six-image mixed-panel compile checked.
- `git diff --check` passed.

Full-deck visual acceptance, attended animation playback, and resolving the existing raw
B/C image-count failures remain outside this strategy change.
