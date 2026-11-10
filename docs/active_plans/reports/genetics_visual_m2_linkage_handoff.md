# M2 cis/trans source handoff

Saved workstream evidence for [genetics_visual_renewal_plan.md](../active/genetics_visual_renewal_plan.md).
Source owner: `/root/m2_linkage`.
Local source: `_temp/genetics_visual_renewal/m2_linkage/HANDOFF.md`. This is a saved snapshot;
see [genetics_visual_renewal_progress.md](genetics_visual_renewal_progress.md)
for current authorization, dependencies and acceptance status. Scratch paths remain local.
Non-ASCII source characters use numeric HTML character references.

Status: canonical sources complete; central LibreOffice export and fresh reviews pending.

## Scope and source map

Owned roots:

- `genetics/LECT08/djot/lect08b-chap8-linked_genes.djot`
- `genetics/LECT08/djot/lect08c-gene_mapping.djot`

New files, both owned by the LECT08B asset directory:

- `genetics/LECT08/djot/assets/lect08b-chap8-linked_genes/cis_trans_wide.drawn.svg`
- `genetics/LECT08/djot/assets/lect08b-chap8-linked_genes/cis_trans_portrait.drawn.svg`

| Root | Physical source slide | Anchor/stage | Original asset | New asset |
| --- | --- | --- | --- | --- |
| LECT08B | 14 | Cis and Trans Configurations | image_006.jpg | cis_trans_wide.drawn.svg |
| LECT08B | 17 | What gametes are produced? / prediction | image_006.jpg | cis_trans_portrait.drawn.svg |
| LECT08B | 18 | What gametes are produced? / unlinked scaffold | image_006.jpg | cis_trans_portrait.drawn.svg |
| LECT08B | 19 | What gametes are produced? / linked answers | image_006.jpg | cis_trans_portrait.drawn.svg |
| LECT08B | 20 | What gametes are produced? / conclusion | image_006.jpg | cis_trans_portrait.drawn.svg |
| LECT08C | 7 | Cis and Trans Configurations | image_001.jpg | cis_trans_wide.drawn.svg |

B has 44 physical and parsed slides. C has 49 physical slides and 50 parsed slides;
its includes/hidden slide mean these physical numbers should not be assumed to be PDF page numbers.
Both source slide counts are unchanged. The wide asset has two demonstrated root consumers;
its C reference intentionally points to the B-owned asset without a duplicate file.

Original B image_006.jpg and C image_001.jpg are identical SHA-256:
`b360854726b053c0f0ee7e277aab037cb48a942985d9e1cc7f58c0d1878df578`.
Both originals remain present. Adjacent B image_008.png/image_009.png (Morgan cross prose and
parental-type introduction) remain unchanged for M3, as do all other LECT08 assets and content.

## Scientific and instructional preservation

- Cis homologs: blue wm, orange ++. Trans homologs: blue w+, orange +m.
- Identical w/m locus positions within each homolog pair; stable blue/orange identities across
  wide/portrait versions, prediction stages and answers.
- Two schematic unreplicated homologs per arrangement, with schematic centromeres. Shapes,
  distances and centromere placement are conventional visual cues, not a physical gene map.
- Native introductory genotype notation retains cis wm/++ and trans w+/+m. Native text explains
  that the slash separates homologs; it does not encode a gamete answer as new image prose.
- Each of the four gamete stages explicitly assumes no crossing over between w and m.
- Stage 1 asks for both linked arrangements. Stage 2 supplies the original unlinked comparison
  (++/w+/+m/wm) while still asking for the linked answers. Stage 3 supplies cis wm/++ and trans
  w+/+m. Stage 4 retains those results and the original two-of-four conclusion.
- Original fragmented conclusion "only half of the normal gametes" is clarified to refer to
  two of four gamete *types*, avoiding an implication that fewer gametes are made.
- C retains the original claim that recombination frequency does not depend on cis/trans.
- Four gamete `@replaceme` markers are removed with the reconstruction; central actual export
  still must establish that the reconstruction meets the slide acceptance criteria.

## Construction and inspection

The approved pilot's chromosome-shaped wide and portrait SVGs were promoted with unchanged
geometry, fonts and colors. Added semantic arrangement/homolog groups and source comments.
Portrait 580 by 660 is used beside native questions/answers; wide 1050 by 390 is used in the
full-width introductory/recap slots. There are no new renderer dependencies or generator API.
SVGs use self-contained vector paths, live text, explicit viewports, title/description, ARIA
references, and unique semantic group IDs. The ODP should package each as one SVG image object;
explanatory prose and genotype notation remain native Djot.

Standalone white-background rsvg previews inspected:

- `portrait_320.png`: smallest stress preview, alleles and arrangement labels remain distinct.
- `portrait_1200.png`: larger inspection, no clipping or overlaps.
- `wide_1000.png`: comparison preview, shared locus positions and homolog identities visible.

These are standalone checks, not evidence of actual canonical slide export or playback.
The pilot's actual export established portrait as the preferred side-panel construction;
central integration must inspect the new actual slots and adjacent sequence.

## Checks and results

Strict native lint:

```bash
source source_me.sh && python3 deck_tools.py lint --require-native \
  --native-executable "$(command -v jotdown)" \
  genetics/LECT08/djot/lect08b-chap8-linked_genes.djot \
  genetics/LECT08/djot/lect08c-gene_mapping.djot
```

Result: exit 0; 2 sources, 94 parsed slides, 59 image uses.

One-time XML/source checks (recorded in `verification.json`) pass positive viewport, static and
image-free SVG, unique IDs, local references, title/description/ARIA, all four homolog allele
combinations, aligned locus positions, homolog colors, unchanged source slide counts, four-stage
question ordering, absent early linked answers, unlinked scaffold and final conclusion.

Capacity was run separately per root with `python3 deck_tools.py capacity ROOT`:

- B: five concerns on unchanged slides, at current source lines 37, 152, 158, 351, 447.
- C: two concerns on unchanged material, C line 44 and evergreen three-point-testcross line 7.
- No capacity concern identifies a changed cis/trans slide.

Preview command template:

```bash
rsvg-convert -b white -w 320 -o _temp/genetics_visual_renewal/m2_linkage/portrait_320.png \
  genetics/LECT08/djot/assets/lect08b-chap8-linked_genes/cis_trans_portrait.drawn.svg
```

No LibreOffice process was launched by this owner. No full base suite was run; this task changes
only Djot and static assets. Central integration owns serialized ODP/PDF export, direct SVG
packaging checks, rendered slide inspection, fresh specification/quality review and final tests.

## Focused references

- Repository SVG_DIAGRAMS, COLOR_GUIDE, VOICE_GUIDE and PEDAGOGY_GUIDE; original B/C raster and
  their surrounding source sequence.
- Approved experiment FINDINGS linkage row and assets linkage_strips, linkage_chromosomes,
  linkage_portrait; inspected original source and portrait render before editing.
- SVG creator skill task-selection/project-workflow guidance for diagram route and embed mode.
- Local `A_Handbook_of_Biological_Illustration-1988.md`, lettering passage at line 578 and
  common-reduction plate composition at line 636: plan labels at reduced output size and use
  consistent component style.
- Local `Generative_Art_with_JavaScript_and_SVG-2024.md`, "Grouping and Reusing Elements" at
  lines 2349-2384: semantic groups improve editing and transformation without requiring symbols.

Local books are under
`/Users/vosslab/.codex/skills/experts/svg-creator-expert/references/local-only/`, respectively
`scientific_illustration/` and `svg_authoring/`.
