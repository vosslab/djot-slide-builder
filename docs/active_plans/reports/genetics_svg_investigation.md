# Genetics SVG investigation findings

Investigation date: 2026-11-09. This report preserves the completed pre-implementation pilot.
Statements about unchanged sources and unperformed checks describe that investigation, not the
subsequent migration. The instructor subsequently approved the
[genetics_visual_renewal_plan.md](../active/genetics_visual_renewal_plan.md).

Local evidence remains under `_temp/svg_migration_research/experiments/`; scratch paths below
identify those retained files and are not committed download links. This preservation step does
not rerun the investigation or establish additional scientific or classroom acceptance.

## What was actually made

- Eleven image-free, editable SVGs covering five teaching concepts.
- A 12-slide experimental deck (`review_deck.pdf`), its editable ODP (`review_deck.odp`), and
  Djot source (`review_deck.djot`).
- Five freshly exported, copied source-context slides (`source_contexts.pdf`), with an exact
  physical-source map (`source_contexts.json`). Only image URLs were rebased in these copies.
- Final asset contact sheet (`renders/final_assets.webp`) and
  final slide contact sheet (`renders/review_deck_contact.webp`).
- Standalone renders at 320 and 1200 pixels, actual LibreOffice PDF renders at 1440 pixels,
  and retained early versions showing the revisions.
- One-time verification results (`verification.json`), a repeatable scratch drawing script,
  and a source inventory covering the whole genetics folder.

All 118 canonical genetics Djot files have unchanged SHA-256 hashes. All work produced here is
under `_temp/`. There were no production-code changes, course asset replacements, or course exports.

## Conclusions supported by these trials

Basic SVG drawing can produce useful original clipart and schematic explanations in this slide
system. The larger improvement comes from choosing the right view, arranging the explanation,
and keeping labels readable in their actual slide slot. Merely changing the file format does
not accomplish that.

The strongest demonstrations are the recognizable pea artwork reused across a cross, the
portrait chromosome arrangement beside a prediction question, and the deletion diagram combined
with an editable matrix. These are visual/editorial judgments from rendered review, not measured
learning outcomes or instructor acceptance.

One universal art style or one aspect ratio would be a poor rule. Different subjects need different
levels of abstraction, and a wide figure often needs recomposition for a narrow panel.

## Experiment results

| Concept | Approaches tested | Evidence and result | Proposed use |
| --- | --- | --- | --- |
| Pea phenotypes and crosses | Colored tokens; stylized pea plants; reusable blossom groups across P/F1/F2 | Review pages 2-3. Tokens are compact but lose organism identity. The pea banner, wings, keel, stem and tendril add recognition without detailed texture. The cross retains 705 purple and 224 white. | Use pea clipart for introductory and cross figures; use tokens only when the organism is already established and a dense count diagram benefits. |
| Gel electrophoresis | Top view; oblique parallel projection | Pages 4-5. The top view makes lanes and direction easy to compare. The angled view identifies a physical tank. The initial angle trial had a gel plane extending too far and disconnected electrode cues; both were revised. | Use top views for interpreting migration; use the angled view for apparatus orientation. Retain real gels when they are evidence. |
| Cis/trans linkage | Flat strips; chromosome-shaped rods; wide and portrait arrangements | Pages 6-8. Both geometries represent the loci accurately. Wide paired figures become too small in half a slide. Portrait recomposition substantially improves allele-label readability without shrinking the native question. | Use the portrait asset beside explanations; wide arrangements are available for full-width comparisons. Keep the no-crossover assumption explicit. |
| Deletion mapping | New interval geometry plus a native matrix; question and partial-answer states | Pages 9-10. All 30 matrix signs agree with the five drawn deletion intervals. The answer reveals only b at position 1. Automatic table sizing failed; explicit column proportions and padding compiled and rendered successfully. | Rebuild diagram and data together, but preserve native table editing and the existing incremental reasoning. |
| Tree rotation | Original relationship structure with a stable colored clade; full-width and half-width placements | Pages 11-12. Both generated path graphs preserve clades YZ and XYZ. The full-width version gives the comparison more room. The half-width view is usable as a supporting recap but offers weaker label visibility. | Prefer full-width paired trees for first explanation. Use color to follow the same clade, with tip labels and topology carrying the meaning. |

## Lessons from revisions

1. **Target size belongs in the drawing brief.** Initial chromosome and pea-cross labels looked
   adequate in standalone previews but too small beside native prose. The correction was a taller
   chromosome composition and a full-width cross, followed by another export.
2. **Real export matters.** The first native seven-column deletion tables failed compilation with
   `an atomic Unicode code point cannot fit in the available text width`. Setting existing
   `column-widths` and `padding` attributes resolved this without production changes.
3. **Drawing primitives need spatial discipline.** The first angled gel was recognizable but its
   gel plane did not sit convincingly inside the chamber. A consistent oblique projection and
   visible electrode connections improved the explanation.
4. **Reusable geometry pays off before reusable software.** The same blossom groups serve a plant
   and a cross; the chromosome shape supports multiple arrangements. Static SVG files with local
   groups and `use` are sufficient for these examples. No new graphics framework was needed.
5. **A diagram and its explanation have different editing needs.** New SVGs contain short
   identifying labels; the main question, answer, observations and matrix remain native slide
   content. SVG internals remain editable in the SVG source, not individual Impress text boxes.
6. **Source intent is a better preservation target than image layout.** The flower trial changes
   composition and labels while retaining the source experiment and observed numbers. The
   deletion trial preserves the inference and its answer sequence.
7. **A repaired import is not a fair standalone quality benchmark.** Source-context page 2 emits
   the current renderer's REPLACE ME overlay because its imported figure/label layout is not
   viable. The original flower raster was also inspected directly. A better result on that page
   alone would not establish superior artwork; comparison must include the original figure.

The retained initial asset sheet (`renders/initial_assets.webp`), `round_1_assets/`, and
earlier exported deck (`round_2_review_deck.pdf`) document these changes. The earlier deck is
historical evidence and is not the recommended trial result.

## Scientific checks and sources

The adjacent original slide sources and figures own the teaching examples, values, and required
relationships. They are identified in source_contexts.json (`source_contexts.json`).

- **Pea morphology:** the large standard/banner, lateral wings and keel are simplified from
  botanical descriptions, rather than replaced with a generic radial flower. See
  [PlantNET: Pisum](https://plantnet.rbgsyd.nsw.gov.au/cgi-bin/NSWfl.pl?lvl=gn&name=Pisum&page=nswfl)
  and [Kew: Fabaceae](https://powo.science.kew.org/taxon/urn%3Alsid%3Aipni.org%3Anames%3A30000147-2/general-information).
  The plant is teaching clipart, not a measured specimen or a morphology plate.
- **Electrophoresis:** wells are near the negative electrode, with DNA movement toward the
  positive electrode. The band locations are illustrative, not measured data. See the
  [University of Utah gel electrophoresis activity](https://learn.genetics.utah.edu/content/labs/gel/electrophoresis/).
- **Linkage:** the source w/m notation is retained: cis wm/++, trans w+/+m. Chromosomes are
  schematic homologs; the diagrams do not depict DNA replication. Centromere position is
  illustrative. No-crossing-over is an explicit condition on the experimental question.
- **Deletion mapping:** source intervals 1-3, 2-3, 2-4, 3-5 and 4-6 match the matrix under
  b-a-c-e-d-f. The question asset does not show those gene names; the first answer shows only b.
- **Tree rotation:** SVG paths were reconstructed as graphs in the one-time verification. Both
  trees contain the same Y-Z and X-Y-Z clades, with W as outgroup. Branch lengths are schematic.
  See [Cold Spring Harbor Laboratory Press: branch rotation](https://evolution-textbook.org/content/free/figures/05_EVOW_Art/06_EVOW_CH05.pdf).

## Drawing references used

The following local books were consulted through the SVG creator expert skill. They informed
construction, not biological facts. Paths are relative to
`/Users/vosslab/nsh/vosslab-skills/skills/experts/svg-creator-expert/references/`.

| Local source | Focused passage | Application |
| --- | --- | --- |
| `local-only/object_construction/How_to_Draw_Drawing_and_Sketching_Objects_and_Environments_from_Your_Imagination-2013.md` | Drawing boxes in perspective; X-Y-Z coordinate system | Establish the chamber's planes before adding wells, bands and electrode detail; keep projection directions consistent. |
| `local-only/scientific_illustration/A_Handbook_of_Biological_Illustration-1988.md` | Clarity; emphasis and comparison | Choose detail by teaching purpose; emphasize the tracked relationship without distorting it. |
| `local-only/svg_authoring/Mastering_SVG-2018.md` | viewBox and viewport in SVG | Keep stable coordinates, semantic groups, and deliberate scaling into actual slide slots. |

The implementation also follows the skill's task selection, object illustration, project workflow,
rendering, and testing/oracles references. The existing repository SVG contract remains the
delivery boundary: static self-contained content, image-free `.drawn.svg`, and native slide prose.

## Verification evidence

- All 11 SVGs pass the repository's static-resource, positive-viewport and image-free checks.
- IDs and references resolve; each drawing has a title and description.
- Native Djot validation with the installed Jotdown passes for both scratch decks.
- Both decks exported through the existing repository ODP and LibreOffice functions, with
  LibreOffice outside the sandbox and all deliverables under this scratch directory.
- The final ODP contains all 11 exact SVG byte payloads and three native tables.
- The baseline and experiment PDFs contain 5 and 12 pages respectively.
- `pdfimages -list` reports no bitmap image objects in the experimental PDF.
- Both baseline and final PDF contact sheets were inspected; important final pages were enlarged.
- Standalone renders cover 320 and 1200 pixels. The smaller size is a stress preview, not an
  accepted size for every complex diagram's labels.
- All 118 source hashes match source_hashes_before.json (`source_hashes_before.json`).

Run the one-time checks from the repository root:

```bash
source source_me.sh && python3 _temp/svg_migration_research/experiments/verify_trials.py
```

The scratch build script (`build_review.py`) uses the unchanged repository pipeline. It must run
outside the sandbox because it invokes LibreOffice. The script can rebuild both review PDFs;
the drawing script rebuilds only experimental assets.

## Inventory and its limits

image_inventory.csv (`image_inventory.csv`) records 1,782 expanded image uses in 82 root decks,
covering 1,226 unique asset paths: 1,015 rasters, 124 SVGs with embedded images, 85 SVGs without
images, and two metafiles. The master/include-aware parse contains 3,351 visible and 176 hidden
slide occurrences. These counts include shared consumers; they are not counts of unique lessons.

Earlier regex counts were preliminary; the parser-based summary (`inventory_summary.json`) is the
current inventory evidence. Inventory dispositions intentionally remain `unreviewed`: five
experiments and 201 earlier thumbnails do not constitute complete contextual review of the course.

## Limits that remain

- Instructor approval and learner comprehension have not been tested. Rendered clarity is not a
  measured educational outcome.
- Dense meiosis/crossover geometry, detailed animal anatomy, scientific maps, empirical plots,
  complex multistage animation, and whole-lecture consistency were not established by this pilot.
- Art is original geometry, but scientific fact checking and provenance still belong to each
  future task. Image-free markup alone does not establish originality or publication rights.
- Native table presence was verified structurally; attended Impress edit/save/reopen and
  accessibility-reader behavior were not tested in this investigation.
- No permanent tests, new dependencies, renderer changes, or full base-suite run were needed
  for these isolated artifacts. No course migration has started.

The fresh [genetics_visual_renewal_plan.md](../active/genetics_visual_renewal_plan.md) uses the demonstrated approaches,
keeps unresolved visual families as bounded investigations, and records the instructor's subsequent approval for implementation within its boundaries.
