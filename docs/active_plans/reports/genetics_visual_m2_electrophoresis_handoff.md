# M2 electrophoresis handoff

Saved workstream evidence for [genetics_visual_renewal_plan.md](../active/genetics_visual_renewal_plan.md).
Source owner: `/root/m2_electrophoresis`.
Local source: `_temp/genetics_visual_renewal/m2_electrophoresis/HANDOFF.md`. This is a saved snapshot;
see [genetics_visual_renewal_progress.md](genetics_visual_renewal_progress.md)
for current authorization, dependencies and acceptance status. Scratch paths remain local.
Non-ASCII source characters use numeric HTML character references.

Status: canonical source ready for centralized export and fresh review, 2026-11-09.
No LibreOffice process was launched by this owner. No commits or production-code changes.

## Owned files and consumers

- Source/root consumer: `genetics/LECT02/djot/lect02f-dna_electrophoresis.djot`.
- New assets in `genetics/LECT02/djot/assets/lect02f-dna_electrophoresis/`:
  `electrophoresis_apparatus.drawn.svg`, `electrophoresis_loading.drawn.svg`,
  `electrophoresis_migration.drawn.svg`.
- No other Djot includes this physical source (repository reference search).
- 26 source slides before and after; only slides 7 and 11 differ.

## Exact source map

| Slide | Old anchor/asset | New anchor/asset | Preserved teaching content |
| --- | --- | --- | --- |
| 7 | Size separation of DNA fragmentsby electrophoresis in agarose gels; image_003.jpg | Size separation in an agarose gel; electrophoresis_apparatus.drawn.svg | Angled tank, buffer, gel, sample slots/wells, electrodes and signs, bands, DNA migration toward positive pole, bands visible after suitable treatment. |
| 11 | Untitled image_008.jpg and missing-label placeholder | Load the samples, then separate the fragments; electrophoresis_loading.drawn.svg plus electrophoresis_migration.drawn.svg | Two stages on the same slide: mixed DNA sizes loaded near cathode, power source, anode/cathode signs, gel, longer/shorter molecules after separation. |

Inspect exported pages 6-12, especially pages 7 and 11. The adjacent real micrograph
(image_002.png), gel evidence (image_004.jpg), and photo (image_009.jpg) remain untouched.
The image_005.jpg interpretation, image_006.jpg sieve mechanism, graph, and all problem/reveal
slides remain byte-identical in their source sections. Original image_003.jpg and image_008.jpg
remain in place as source evidence.

## Source facts and drawing choices

Inspected original image_003.jpg and image_008.jpg directly. Read original ODP `content.xml`
from both `genetics/LECT02/lect02f-dna_electrophoresis.odp` and its `old/` version. Their page 11
supplies the lost native labels: mixture of DNA molecules of different sizes, power source,
longer molecules, shorter molecules, gel, anode, cathode, technique, 1 and 2, and polarity signs.
Administrative figure numbers were retained in this provenance rather than copied into lecture art.

The angled apparatus extends the approved pilot with missing source labels. The two stage
figures adapt the pilot top view to a matched side-by-side comparison. All coordinates are
schematic. The three repeated lanes and band locations are illustrative, not recovered measurements;
this is stated visibly in native prose and in SVG descriptions. Longer fragments remain closer
to wells, shorter fragments move farther toward positive. No numerical size data were added.
The load stage shows the completed loading state; the native caption supplies the action.

Static original SVG geometry with semantic group IDs, live short labels, title/description,
and native explanatory prose. SVG internals are editable in the SVG source, not separate
Impress shapes. No external resources or bitmap-containing SVGs.

## Checks and evidence

- `verification.json` records the one-time checks; `verify.py` reproduces them.
- XML, positive viewport, repository static/image-free checks, unique IDs, accessibility ID
  references, and local references pass for all three assets.
- Scientific check verifies negative-side wells and positive-direction band displacement.
- Source comparison verifies exactly slides 7 and 11 changed, with all other source sections
  and reveal ordering identical. There are 26 slides and 40 image uses after the replacement.
- Strict native lint passes with `deck_tools.py lint --require-native --native-executable
  /Users/vosslab/.cargo/bin/jotdown genetics/LECT02/djot/lect02f-dna_electrophoresis.djot`.
- All six standalone previews (320 and 1200 pixels per asset) rendered with `rsvg-convert` and
  visually inspected. Labels, arrows and matching stage geometry are legible; 320 is a stress
  preview, not the classroom target.
- `deck_tools.py capacity` reports 12 concerns elsewhere, none on changed slides 7/11.
  Those inherited whole-deck concerns require accurate reporting during export review.
- `before.djot` is the original owned source; `draw.py` is a scratch-only reproduction script.

## Focused drawing references

Read SVG creator skill and task selection/project workflow/local books references, plus repository
SVG, color, voice and pedagogy guides. Focused local passages:

- `.../svg-creator-expert/references/local-only/object_construction/How_to_Draw_Drawing_and_Sketching_Objects_and_Environments_from_Your_Imagination-2013.md`, lines 341-358:
  drawing boxes and X-Y-Z coordinate system. Used to retain consistent chamber planes.
- `.../svg-creator-expert/references/local-only/svg_authoring/Mastering_SVG-2018.md`, lines 635-670:
  viewBox/viewport. Used for predictable scaling and intact label margins.

## Remaining validation

Central exporter must build the root consumer, verify exact SVG bytes in ODP, native caption
text, page count and actual PDF pages 7 and 11 plus adjacent context. Fresh scientific/specification
and visual reviews follow that export. No attended Impress playback, accessibility-reader test,
whole-suite test, or student learning validation was performed. The inherited deck still has
capacity concerns outside this bounded replacement.
