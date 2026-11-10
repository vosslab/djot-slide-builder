# Population-genetics M1 evidence

Saved workstream evidence for [genetics_visual_renewal_plan.md](../active/genetics_visual_renewal_plan.md).
Source owner: `/root/classify_population`.
Local source: `_temp/genetics_visual_renewal/population/EVIDENCE.md`. This is a saved snapshot;
see [genetics_visual_renewal_progress.md](genetics_visual_renewal_progress.md)
for current authorization, dependencies and acceptance status. Scratch paths remain local.
Non-ASCII source characters use numeric HTML character references.

Date: 2026-11-09. Scope: original inventory rows with root_deck LECT14 or LECT15. All writes are under this scratch directory. No canonical source, course artwork, ODP, or PDF was modified. No LibreOffice process was launched.

## Coverage and artifacts

- `classification.csv`: all **208** uses, original columns preserved; original `disposition` is also stored as `original_disposition`, assigned disposition/reason/concept_id added.
- **121 unique assets**, **8 root decks**, **10 physical Djot files**, **41 concept briefs**.
- Original SVG redesign: 76 uses / 53 assets.
- Native-content repair: 92 uses / 44 assets.
- Retain with reason: 23 uses / 18 assets.
- Source clarification needed: 17 uses / 6 assets.
- Already suitable: 0; the equation SVGs in this subset are legacy imported equations with poor typesetting, and the five bitmap-bearing SVGs are transparent placeholders.
- `BRIEFS.md`: exact source/line/root-slide/heading/hidden-state anchors, facts, reveal order, compositions, checks, physical-source dispatch matrix.
- `uses.txt`: numeric asset ID &#8594; exact path.
- `coverage.txt`, `shared_sources.txt`: checked counts and duplicate-hash consumers, including external LECT07/08/13 matches.
- `build_classification.py`: repeatable one-time ledger plus assertion-based coverage/hash checks. Run `source source_me.sh && python3 _temp/genetics_visual_renewal/population/build_classification.py`.

Every original identifying field is checked as a multiset against the filtered inventory, including repeated uses. All121 asset files still match original inventory SHA-256. No row was dropped because its lesson was hard or source art was low-quality.

## Context and visual inspection

Read the full ten current Djot physical sources into `contexts.txt`, the approved plan, pilot FINDINGS, AGENTS.md, HUMAN_GUIDANCE, and slide authoring/color/voice/pedagogy guidance. Read SVG creator skill plus task-selection/project-workflow instructions. The pilot's recognizable organism versus compact token distinction informed P06/P29; native data beside SVG informed P03/P14/P18. No drawing was created during M1.

All121 unique assets were rendered or loaded and visually inspected on these contact sheets:

- `contact_000.jpg`: IDs000&#8211;023.
- `contact_024.jpg`: IDs024&#8211;047.
- `contact_048.jpg`: IDs048&#8211;071.
- `contact_072.jpg`: IDs072&#8211;095.
- `contact_096.jpg`: IDs096&#8211;119.
- `contact_120.jpg`: ID120.

Enlarged inspections used `detail_001.jpg`, `detail_018.jpg`, `detail_021.jpg`, `detail_036.jpg`, `detail_046.jpg`, `detail_048.jpg`, `detail_050.jpg`, `detail_058.jpg`, `detail_060.jpg`, `detail_070.jpg`, `detail_073.jpg`, `detail_080.jpg`, `detail_084.jpg`, `detail_088.jpg`, `detail_092.jpg`, `detail_098.jpg`, `detail_102.jpg`, `detail_114.jpg`, `detail_117.jpg`, and `detail_083.png`.

The bread-dog GIF contains24 frames. All frames were inspected in `gif_all_frames.jpg`; original animation is retained. No attended playback or export timing was tested.

Legacy equation SVG XML was read to recover exact symbols where previews overlapped. Five equal-hash imported SVGs (IDs015,038,045,066,078) each contain a PNG with **all RGBA extrema(0,0)**, proving complete transparency. Thus the white-looking sheet slots are transparent no-content embeds, not hidden missing equation text. Keep source files; remove only the unnecessary use after owning slide repair.

## Original-source recovery

`original_odp_text.txt` extracts all text from the eight original ODP files using ZIP/XML read-only. Original text supplies missing labels that were separate from raster figures.

- 15D original slides3&#8211;5 establish flower drift states: first5red/4pink/1white (p=.7), next3red/4pink/3white(p=.5), last10red(p=1);5then2 highlighted plants reproduce.
- Original 15D slide14 provides the prairie-chicken table missing from current Djot. `original_prairie.png` renders existing original PDF page14 with Poppler and was inspected against the ODP extraction. Illinois1930&#8211;1960s:1000&#8211;25000,5.2alleles/locus,93%hatch;1993:<50,3.7,<50%;Kansas1998:750000,5.8,99%;Nebraska1998:75000&#8211;200000,5.8,96%. Map labels1820/1993 are restored natively while historical map and actual bird photo remain evidence.
- `drift_activity_data.csv` recovers all64 class drift values from `genetics/LECT15/lect15x-genetic_drift_graph.ods`, expanding ODS repeated-cell attributes. First row all6; last row2,5,0,4,6,8,10,5. All intermediate values match enlarged screenshot. This plot is dispatchable with actual recorded values; it is not blocked like the overlapping12-population textbook paths.
- Enlarged bottleneck survivor cup contains5blue and1white bead; yellow is absent. Two blue beads are visibly falling during the event. Original dense bottles are schematic, not an empirical counted dataset.

## Decisions and unresolved source content

**D1 received from manager:** user approved correcting clear errors and documenting them. In14C final X-linked frequency slide, source means male/female ratio but writes `.09/.3=3.33`. P08 now authorizes `.3/.09=3.33`, preserving the original q=.3 example. No canonical correction was made here.

**P28 needs a source-method decision:** problem17.29 states fitnesses .90:1:.50 but source answers adult heterozygosity .323, and .167 afteraa becomes lethal. For the first case the normalized weighted calculation gives wbar11/12 andadultAa10/33&#8776;.303030. In the lethal case it gives wbar10/11 andadultAa2/11&#8776;.181818. Zygotic frequencies are different quantities. Preserve the entire sequence until manager/instructor decides its intended stage/method; do not hide this behind a native-text conversion.

**P25 model recovery:** favored dominant/additive/recessive curves lack exact initial frequency and selection coefficient; lethal-mutation equilibrium figure lacks a stated approximation/life-cycle convention. Recover figure source before quantitative redraw. A labeled conceptual alternative must preserve the original quantitative figure as reference unless instructor approves substitution.

**P34 trajectory recovery:** twelve overlapping hypothetical population paths have no recovered numerical table. No new random simulation is claimed equivalent to these paths. Retain original while recovery or an explicitly approved conceptual substitution proceeds.

Other source flags are local to implementation checks: old disease-frequency tables remain historical given examples; broad CCR5/Tay-Sachs clinical wording needs subject review; a native Phlox17.14 prompt asks expected numbers while its solution reports percentages; rounding such as .324 for.57&#178; and malformed superscripts should be checked under D1. These do not block independent drawing/native repairs. Clinical/legal updates are not part of this M1 classification.

## Limits and next acceptance checks

This handoff establishes contextual inventory coverage and dispatchable work, not completed visual replacements. It does not establish canonical export quality, attended Impress reveal playback, native table edit/save/reopen, external source validation for new scientific illustrations, learner acceptance, or base-suite results. Existing original PDFs were read; no fresh course build was produced.

Implementers must perform bounded trials for count/population figures, formula-derived plots, empirical-data plots, detailed organisms, pedigrees if no accepted trial exists, and regional map geometry. The manager serializes actual LibreOffice export outside sandbox. Retained empirical selection/drift distributions and geographic evidence remain explicit source evidence, not a failure to eliminate raster files.
