# M2 tree rotation source handoff

Saved workstream evidence for [genetics_visual_renewal_plan.md](../active/genetics_visual_renewal_plan.md).
Source owner: `/root/m2_tree_rotation`.
Local source: `_temp/genetics_visual_renewal/m2_tree_rotation/HANDOFF.md`. This is a saved snapshot;
see [genetics_visual_renewal_progress.md](genetics_visual_renewal_progress.md)
for current authorization, dependencies and acceptance status. Scratch paths remain local.
Non-ASCII source characters use numeric HTML character references.

Status: source ready for central export and fresh independent specification/quality review.
No LibreOffice process was launched by this workstream.

## Changed source and consumers

- `genetics/LECT12/djot/lect12b_gene_trees_part_01.djot`, anchors
  `Rotating Branches in Trees` and `Trees, trees, and trees, oh my` only.
- Root consumer: `genetics/LECT12/djot/lect12b-gene_trees.djot`.
- Root remains 77 slides. Changed slides are 24 and 25 (original ODP/PDF 22 and 23,
  confirmed by `LECT12_SOURCE_MAP.md`). Adjacent slides remain intact.
- New adjacent assets:
  `assets/lect12b-gene_trees/tree_rotation.drawn.svg` and
  `assets/lect12b-gene_trees/tree_rotation_four_forms.drawn.svg`.

## Original-to-new mapping and sequence

I inspected both actual local PNG originals, not only the experimental SVG.

| Original | Actual content | Replacement |
| --- | --- | --- |
| `image_017.png` | WXYZ &#8594; WZYX, orange/red rotation around basal XYZ branch, SAME TREE | `tree_rotation.drawn.svg`, full-width paired geometry; rotation cue retained; conclusion and invariant explanation in native Djot |
| `image_018.png` | Four equality-linked trees: WXYZ, WZYX, WXZY, XZYW | `tree_rotation_four_forms.drawn.svg`, all four forms in original order |

The second slide retains its original three explanation bullets. Its reference to
"the two trees left" becomes "the two trees on the previous slide". Removing the
repeated small pair makes room for readable full-width four-form comparison.
The first slide makes the unchanged relationships explicit as native prose and
states that branch lengths are schematic. No slide was added or removed.

Both PNGs remain in place. No unrelated LECT12 section or production code changed.
The M1 UPGMA issue is outside this workstream.

## Scientific and structural checks

`check_rotation.py` reads the emitted branch paths, reconstructs undirected graphs,
roots each graph at its basal stem endpoint, and recovers descendant leaf sets.
All six trees are connected and acyclic, have exactly the four labeled terminal
leaves plus the root stem, preserve the exact original tip orders, and have the
nontrivial clades YZ and XYZ. W is therefore the outgroup in each. A wrong-outgroup
label swap serves as a negative control and changes the recovered clades.

Both files pass the repository SVG validator, including image-free/static content,
positive dimensions, unique IDs, local references, and title/description checks.
The checks are recorded in `verification.json`.

Scientific interpretation follows the actual source diagrams: lengths are schematic;
blue follows YZ in every form, while labels and topology independently carry identity.
The orange cue marks rotation; it does not mark a new clade or changed relationship.

## Verification commands and evidence

Run from repository root:

```bash
source source_me.sh && python3 _temp/genetics_visual_renewal/m2_tree_rotation/check_rotation.py
source source_me.sh && python3 deck_tools.py lint --require-native --native-executable /Users/vosslab/.cargo/bin/jotdown genetics/LECT12/djot/lect12b-gene_trees.djot
source source_me.sh && python3 deck_tools.py capacity genetics/LECT12/djot/lect12b-gene_trees.djot
rsvg-convert -b white -w 640 -o _temp/genetics_visual_renewal/m2_tree_rotation/pair_640.png genetics/LECT12/djot/assets/lect12b-gene_trees/tree_rotation.drawn.svg
rsvg-convert -b white -w 1600 -o _temp/genetics_visual_renewal/m2_tree_rotation/pair_1600.png genetics/LECT12/djot/assets/lect12b-gene_trees/tree_rotation.drawn.svg
rsvg-convert -b white -w 800 -o _temp/genetics_visual_renewal/m2_tree_rotation/four_800.png genetics/LECT12/djot/assets/lect12b-gene_trees/tree_rotation_four_forms.drawn.svg
rsvg-convert -b white -w 1600 -o _temp/genetics_visual_renewal/m2_tree_rotation/four_1600.png genetics/LECT12/djot/assets/lect12b-gene_trees/tree_rotation_four_forms.drawn.svg
```

Strict native lint passed: 1 root, 77 slides, 33 images. Capacity reports 16 concerns
elsewhere in the root; neither changed slide is reported (`capacity.txt`).
All four white-background previews were inspected. Tip letters, YZ junctions,
rotation cue, and equal signs remain legible at small size; large renders show
clean geometry without clipping. Native slide composition remains to be checked
in the central export, particularly text/image vertical allocation on slide 25.

## Construction references

Skill: `/Users/vosslab/.codex/skills/experts/svg-creator-expert/SKILL.md`.
Focused local book passages, beneath that skill's `references/local-only/`:

- `scientific_illustration/A_Handbook_of_Biological_Illustration-1988.md`,
  "Size and Reduction of Illustrations for Publication", lines 207-225: plan detail
  and lettering for final display size; reserve space for captions.
- `svg_authoring/Mastering_SVG-2018.md`, "viewBox and viewport in SVG",
  lines 635-665: stable intrinsic dimensions with matching coordinate viewport.

The pilot full-width comparison informed placement and a stable colored clade.
New paths are direct schematic geometry, with live SVG text and descriptive IDs;
no raster tracing or external assets. Explanations remain native Djot text.

## Central export acceptance still required

Export the root via repository scripts outside the sandbox. Inspect PDF slides
23-26 in context, with attention to 24/25. Verify 77 output pages, selectable native
explanation text, and both SVG sources packaged byte-for-byte in the ODP. Then run
fresh independent specification and quality review. This handoff does not claim
LibreOffice/PDF acceptance or a full regression suite.
