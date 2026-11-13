# Reusable SVG drawing-tool roadmap

This roadmap ranks **drawing parts**, not finished figures. The user chose a roadmap first;
implementation, an API, and changes to slides or existing illustrations are outside this work.
The order reflects teaching value and reuse after checking current slide artwork and nearby
projects. Biotechnology LECT11 is excluded. Effort is relative, not a commitment.

![Existing cell and workflow illustrations and a gene-track helper demonstration](slide-specs/illustration_examples/svg_tool_candidates.webp)

The overview combines three fixed existing illustrations with a demonstration of the existing
`gene_track_svg` helper. It is evidence of current material, not proposed tool output. The source
key follows reading order, left to right and top to bottom:

1. [Mitosis: interphase and prophase](../genetics/LECT06/djot/assets/lect06b-intro_cells/mitosis_interphase_prophase.drawn.svg) (existing illustration).
2. [Tay-Sachs lysosome comparison](../genetics/LECT14/djot/assets/lect14c-hardy_weinberg_1/tay_sachs_lysosome_comparison.drawn.svg) (existing illustration).
3. [Pyruvate branch](../biotech/LECT06/djot/assets/lect06c-set_4_tp_chapter_12_16_material/pyruvate_branch.drawn.svg) (existing illustration).
4. Existing [gene-track helper](../svg_tools/gene_tracks.py) demonstration; parameters to be recorded with the preview.

## Priority and scope

| Order | Priority | Drawing parts | Reason |
| --- | --- | --- | --- |
| 1 | High | Cells and cell structures | Broad teaching need; existing figures show useful shared anatomy but are fixed illustrations. |
| 2 | High | Basic flowchart parts | Repeated nodes, branches, and arrows support many processes. |
| 3 | High | Extend gene tracks | Exons and introns already exist; orientation and operon composition would fill a teaching need. |

Reuse existing work for labware, gels, pedigrees, Punnett squares, circular maps, and membrane
bilayers or transporters. Their existing format does not make them candidates for a duplicate
engine. Antibodies and flowers or seeds are possible later opportunities; no counterpart was
found in the bounded survey, but they are not the leading priorities.

## 1. Cells and cell structures

The [mitosis illustration](../genetics/LECT06/djot/assets/lect06b-intro_cells/mitosis_interphase_prophase.drawn.svg)
in [lect06b-intro_cells.djot](../genetics/LECT06/djot/lect06b-intro_cells.djot) depicts cell
membranes, intact nuclei, nucleoli, chromatin, and centrosomes. The
[Tay-Sachs comparison](../genetics/LECT14/djot/assets/lect14c-hardy_weinberg_1/tay_sachs_lysosome_comparison.drawn.svg)
in [lect14c_hardy_weinberg_1_part_01.djot](../genetics/LECT14/djot/lect14c_hardy_weinberg_1_part_01.djot)
combines whole cells and lysosomes. The
[pyruvate branch](../biotech/LECT06/djot/assets/lect06c-set_4_tp_chapter_12_16_material/pyruvate_branch.drawn.svg)
in [set4_chapter_13.djot](../biotech/LECT06/djot/set4_chapter_13.djot) includes a schematic
mitochondrion, and [liposome therapy](../biotech/LECT10/djot/assets/set5_gene_therapy/liposome_therapy.drawn.svg)
in [set5_gene_therapy_05_08.djot](../biotech/LECT10/djot/set5_gene_therapy_05_08.djot) shows
cells and nuclear delivery. These are fixed, authored figures, not a generic cell renderer.
A plant-cell cross section was not confirmed by this survey.

- Start with a cell outline or membrane, nucleus and nucleolus, and selected organelle glyphs.
  Let the recipe choose positions, size, labels, and which structures to show.
- Compare these examples before defining a shared boundary. Preserve the anatomical feature
  being taught; do not imply that one schematic describes every cell or biological scale.
- Reuse BPQ membrane and transporter motifs where needed instead of creating competing ones.
  A meaningful first component is medium to large relative effort.

## 2. Basic flowchart parts

The [trihybrid forked line](../genetics/LECT04/djot/assets/lect04h-indep_assort_problems/trihybrid_forked_line.drawn.svg)
in [lect04h-indep_assort_problems.djot](../genetics/LECT04/djot/lect04h-indep_assort_problems.djot)
uses repeated nodes and branching connectors. The pyruvate example above combines a branching
process with labels and arrows. The [cell-cycle figure](../genetics/LECT06/djot/assets/lect06b-intro_cells/cell_cycle_phases.drawn.svg)
in [lect06b-intro_cells.djot](../genetics/LECT06/djot/lect06b-intro_cells.djot) shows a cycle.

- Start with basic nodes, straight and elbow arrows, and supplied branch labels. The author
  explicitly places the parts and provides the scientific relationships.
- Cyclic arcs and automatic graph layout are not needed in the first generalization. The
  importer's connector recognition is not a standalone SVG drawing API; do not import the
  whole builder to draw a flowchart. Initial effort is small to medium.

## 3. Extend existing DNA gene tracks

[gene_tracks.py](../svg_tools/gene_tracks.py) already draws configurable exon blocks and intron
spans, including zero-gap mature RNA; it accepts width and height and returns track width and
exon offsets. Extend this helper rather than building a parallel chromosome engine.

- Consider oriented genes and arrows, promoter and operator landmarks, and composition of an
  operon from supplied parts. Keep biological names, order, direction, and relationships in the
  authored recipe. These features are targets for future work, not existing capabilities.
- The Genetics 02B DNA/RNA/protein gene strips and Biotechnology 04 insulin scene are related
  partial examples, not evidence of a live native operon. No live native operon was confirmed
  in the bounded survey. Prototype against a concrete teaching example; effort is medium.

## Reuse before building

Paths below are relative to `/Users/vosslab/nsh/PROBLEMS/biology-problems` (BPQ), unless
otherwise noted. Their output formats vary; reuse or adapt the existing work when a slide needs
it rather than using format differences to justify another generator.

| Need | Existing work |
| --- | --- |
| Gels | `problems/dna_profiling-problems/gellib.py` |
| Pedigrees | `problems/inheritance-problems/pedigrees/pedigree_lib/svg_output.py` and `layout.py` |
| Punnett squares | `problems/inheritance-problems/punnett_choice.py` |
| Circular restriction maps | `problems/molecular_biology-problems/restriction_enzymes/dna_render_lib.py` |
| Tetrads and asci | `problems/inheritance-problems/gene_mapping/genemap_art/asci.py`, already reused by [render_tetrad_tables.py](../slide_lib/render_tetrad_tables.py) |
| Membranes and transporters | `problems/biochemistry-problems/membranes/phospholipid-unit.svg`, `transporter-protein.svg`, and `identify_transporter_type.pgml`; `tools/sync_membrane_svgs.py` |
| Enzymes and substrates | `problems/biochemistry-problems/enzymes/enzyme_simulation.pgml` canvas cartoons |
| Sequences and chemical bases | `seqlib.py` and `PUBCHEM/NUCLEOBASES/nucleobaselib.py` |

For laboratory components, the separate
`/Users/vosslab/nsh/TYPESCRIPT/virtual-lab-protocol-simulation/assets/equipment/` contains
standalone SVG artwork across `static`, `binary_state`, `multi_state`, and `variable_volume`:
tubes, pipettes, plates, racks, microscopes, incubators, centrifuges, water baths, electrophoresis
equipment, flasks, and more. Reuse artwork and anchors as needed; its SolidJS scene renderer and
state machinery are not a general slide API. Check `assets/equipment/SOURCES.md` and
`docs/THIRD_PARTY_ASSETS.md` there and record attribution for each reused asset: sources include
Servier CC BY 3.0, DBCLS CC BY 4.0, CC0, and repository-authored work. Its microscope cell
observation panels are not general organelle figures. No lab generator rewrite is proposed.

Also reuse [chromosomes.py](../svg_tools/chromosomes.py), the existing gene-track helper, and
`project`, `cuboid`, and `cylinder` in [drawing.py](../svg_tools/drawing.py) where appropriate.
The surveyed BPQ and Virtual Lab paths are references, not new runtime dependencies.

## Survey and design limits

The bounded survey inspected slide examples and consumers plus candidate BPQ source files
(`.py`, `.pgml`, `.pg`, `.svg`, `.yml`, `.yaml`, `.js`, and `.html`) and Virtual Lab source and
assets. It did not exhaustively classify unlabelled static images or external repositories.
No flowchart, exon/intron/operon, or general organelle counterpart was found in that bounded
cross-repository search; this is not proof that none exists elsewhere.

Prefer editable SVG fragments composed by existing writers. Keep titles and captions native in
Djot and leave figure-specific labels and scientific relationships with the recipe. Add anchors
or bounds only where they help real composition, and use document-unique IDs where needed.
Do not settle a full API before trying the parts against concrete figures.

Reference illustrations may retain legacy fonts; they are not future style authority. Future
normal labels use Atkinson Hyperlegible Next and aligned sequences use the Mono role when
needed. The current `drawing.text` Arial default is a future fix, not a change in this roadmap.
Follow [COLOR_GUIDE.md](slide-specs/COLOR_GUIDE.md): preserve stable relational meanings for
biological colors while keeping the course hue distinct. No new theme framework is proposed.
Review rendered artwork at its intended slide size.
