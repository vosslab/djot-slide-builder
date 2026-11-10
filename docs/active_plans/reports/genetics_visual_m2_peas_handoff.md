# M2 pea phenotype/cross handoff

Saved workstream evidence for [genetics_visual_renewal_plan.md](../active/genetics_visual_renewal_plan.md).
Source owner: `/root/m2_peas`.
Local source: `_temp/genetics_visual_renewal/m2_peas/HANDOFF.md`. This is a saved snapshot;
see [genetics_visual_renewal_progress.md](genetics_visual_renewal_progress.md)
for current authorization, dependencies and acceptance status. Scratch paths remain local.
Non-ASCII source characters use numeric HTML character references.

Source work complete; ready for central export and fresh specification/quality review.
No LibreOffice process was launched by this agent. Original images remain untouched.

## Owned canonical sources and root consumers

- `genetics/LECT04/djot/lect04c-two_principles.djot` (same-named root deck):
  four repeated Principle of Dominance summaries and the two-panel `Dominance` slide.
- `genetics/LECT04/djot/lect04d-cross_experiments.djot` (same-named root deck):
  `True Breeding`, `Hybrid Plants`, three formerly unheaded experiment states,
  and `Hybrid Cross Terminology`.
- No renderer, dependency, test-suite, or other lecture source changed.

## Original/new anchor mapping

All filenames below are relative to `genetics/LECT04/djot/assets/`.

| Source slide | Original local asset | New local asset / native content |
| --- | --- | --- |
| 04C Dominance | `lect04c-two_principles/image_006.png` | `lect04c-two_principles/pea_dominance_population.drawn.svg`; native corrected dominance explanation |
| 04D True Breeding | `lect04d-cross_experiments/image_001.png` | `lect04d-cross_experiments/pea_true_breeding.drawn.svg` |
| 04D Hybrid Plants | `lect04d-cross_experiments/image_002.png` | `lect04d-cross_experiments/pea_hybrid_plants.drawn.svg` |
| 04D unheaded P experiment | `lect04d-cross_experiments/image_003.jpg` | `lect04d-cross_experiments/pea_experiment_p.drawn.svg`; heading `Cross Experiment: P Generation` |
| 04D unheaded P/F1 experiment | `lect04d-cross_experiments/image_004.jpg` | `lect04d-cross_experiments/pea_experiment_f1.drawn.svg`; heading `Cross Experiment: F1 Generation` |
| 04D unheaded P/F1/F2 experiment | `lect04d-cross_experiments/image_005.jpg` | `lect04d-cross_experiments/pea_experiment_f2.drawn.svg`; heading `Cross Experiment: F2 Generation` |
| 04D Hybrid Cross Terminology | `lect04d-cross_experiments/image_006.png` | `lect04d-cross_experiments/pea_cross_recap.drawn.svg`; native count/ratio recap |

## Scientific facts and approved corrections

- Source `image_001` already showed AA purple at P/F1/F2; new figure preserves all six AA labels.
- Source `image_002` already showed AA purple x aa white, Aa x Aa F1, and F2 purple AA or Aa / white aa. The early overview remains in place before the experimental reveal sequence.
- The three experiment assets deliberately contain no genotypes. State 1 has P only; state 2 adds purple F1 only; state 3 adds both F2 phenotypes. Earlier stage positions, artwork, and labels are identical across the state files. Native prediction prompts pause before each new result.
- Observed counts **705 purple-flowered plants and 224 white-flowered plants** remain native Djot on the final experiment and recap. The data are not recast as exact 3:1 counts. The recap says approximately 3:1.
- The source's self- or cross-pollination of F1 is retained in native explanation.
- 04C source nine plants remain in original reading order: WW, Ww, ww / WW, Ww, ww / Ww, Ww, WW. WW and Ww purple; ww white. These are illustrative population icons, not experimental sample counts.
- Decision D1, relayed by parent: user explicitly requested **'Correct the errors and document them.'** The incorrect 04C sentence `Since purple is more common than white, purple is likely dominant to white` is replaced with the causal evidence: Ww hybrids are purple, and WW x ww produces purple Ww F1. Native text explicitly says phenotype frequency does not establish dominance.
- The adjacent false universal `In each genotype there is a dominant allele, the phenotype is determined by dominant allele` is corrected in all four repeated principle summaries to `Under complete dominance, a heterozygote displays the dominant phenotype`. The two-panel explanation is more specific to Ww/WW. Homozygous recessive individuals therefore no longer contradict the stated rule.
- Parent explicitly authorized qualifying recap `homozygous/heterozygous for all genes` to the flower-color gene. The revised recap retains P/F1/F2/F3/F4 terms and the phenotype example.
- Scope of D1 here is the 04C dominance misconception. X-linked arithmetic belongs to another owner. No tree/UPGMA change was made.

## Construction and evidence

The reviewed pilot `flowers_botanical.drawn.svg` supplied original banner/wings/keel, leaves,
stem, and tendril geometry. These are teaching clipart, not measured specimens. Every SVG
has self-contained reusable groups, live short labels, title/description/source anchor,
unique IDs, and no images. Genotype labels use italic text. Main explanations, observations,
and prediction prompts remain native slide text.

Local skill reading:
- `/Users/vosslab/.codex/skills/experts/svg-creator-expert/SKILL.md` plus task selection,
  project workflow, and local books references.
- `references/local-only/scientific_illustration/A_Handbook_of_Biological_Illustration-1988.md`,
  lines 278-294: clarity, comparison, and restrained line/depth hierarchy.
- `references/local-only/svg_authoring/Generative_Art_with_JavaScript_and_SVG-2024.md`,
  lines 2349-2390: semantic grouping and reusable elements.
- Pilot `FINDINGS.md` supplies prior botanical evidence from PlantNET Pisum / Kew Fabaceae;
  the source figures own every cross/genotype/count above.

Scratch evidence is in this directory:
- `before.djot`, `before_04c.djot`: exact pre-edit sources.
- `originals.png`, `original1.png`, `original2.png`: original-image inspection, including
  transparency composited on white for the genotype schematics.
- `draw_peas.py`: one-time composition script, not a production generator.
- `verify_peas.py`: actual-artifact assertions for genotype/phenotype associations, nine-plant
  order, observed data, three reveal states, unchanged revealed-group geometry, structure,
  local references, title/desc, static/image-free contract, and original slide counts.
- Seven `*_320.png` and seven `*_1200.png` previews; `previews.png` (first six small
  assets), `pea_dominance_population.drawn_320.png`, and `large_previews.jpg` inspected.
  No clipping, overprinted labels, unresolved uses, or generic radial-flower substitution seen.

Commands/results (all Python commands prefixed `source source_me.sh &&`):

1. `python3 deck_tools.py lint --require-native --native-executable "$(command -v jotdown)" genetics/LECT04/djot/lect04c-two_principles.djot genetics/LECT04/djot/lect04d-cross_experiments.djot`
   passes: 2 sources, 55 slides, 17 images (04C 36 source slides including hidden; 04D 19).
2. `python3 _temp/genetics_visual_renewal/m2_peas/verify_peas.py` passes all seven SVG and
   domain/reveal/native-count checks.
3. `rsvg-convert -w 320/1200 ...` produced all previews without errors; visually inspected.
4. `python3 deck_tools.py capacity genetics/LECT04/djot/lect04d-cross_experiments.djot`
   now reports only the unchanged Reciprocal Crosses mixed-readability concern at line 148.
   The initially crowded recap was shortened until its new content passed the capacity floor.
5. 04C capacity scan reports other pre-existing content/layout concerns outside the pea
   figure anchor; this task does not claim the whole deck satisfies capacity guidance.

## Central export/review requirements and limits

Build both exact root source paths through the normal repository pipeline, serialized and
unsandboxed as required for LibreOffice. Inspect 04D pages 3-4 and 7-10 plus their adjacent
pages; inspect 04C Dominance and the repeated principle-summary pages. Verify direct original
SVG packaging in ODP and readable text in the exported PDF. Count statements should remain
native/selectable. Source edits are handed off and frozen pending that review.

Only standalone SVG previews and native/static source checks are complete here. Actual slide
PDF appearance, ODP packaging, and attended playback await central export/review. Later
04E/04F/05H consumers are inventoried in the M1 brief and left for M3. In particular, the
Bateson/Punnett 382/269 (9:7) examples must not acquire this example's 705/224 counts.
