# Plan: Reusable chromosome SVG drawing tool

## Context

The instructor requests a reusable Python tool for consistently banded chromosomes in requested
colors and sizes, including sisters, centromeres, deletions, translocations and introns. This is
authorized functionality. Implementation follows internal review without another human approval.
This document specifies the technical implementation; the separate task ledger records dispatch.
Status: DONE for the reusable Python library and standalone SVG specimen. Date: 2026-11-12.
Fresh specification, rendered quality and integration reviews PASS; root accepted all seven
final proofs. Broader artwork goal remains ACTIVE; native compatibility is future work.

## Completed verification

All requested modes are implemented through the shared chromosome engine and distinct gene-track
renderer. Existing callers and historical specimens are preserved. Ten focused tests pass;
specification review also records clean pyflakes, 140 deletion checks and 75 sister checks.
Integration review executes all three README Python examples and confirms that the real recipe
reproduces the shipped specimen byte for byte. The 13 fixed specimen evidence members verify.
Actual-font evidence identifies Next Regular and 14 matched semibold glyphs.

The 480-pixel gallery is overview-only; review uses the 1440-pixel gallery and separate components,
including sisters at 1150 pixels wide with approximately 19-pixel smallest C labels. Label fitting
is approximate; other placements require inspection. No full-suite, native slide/export,
classroom/Zoom or print acceptance is claimed. No course migration is part of this delivery.
See [README.md](../../../svg_tools/README.md#chromosome-drawing-tool) for usage and
[closure.md](../../../_temp/chromosome_svg_tool/closure.md) for the bounded evidence receipt.
The remaining sections preserve the approved design and milestone criteria as historical scope.

The existing [chromosomes.py](../../../svg_tools/chromosomes.py) is the starting point. The named
DNA reference establishes a separate exon/intron representation, not an intron-shaped chromosome.

## Objectives

- Generate editable, self-contained ASCII SVG through a small reusable Python library.
- Retain existing callers while adding requested size, plain/banded bodies, joined sisters,
  explicit segment rearrangements and a biologically distinct exon/intron track.
- Demonstrate every requested mode in original rendered specimens, with actual font evidence.

## Design philosophy

Apply **Keep it simple (KISS)** from [REPO_STYLE.md](../../REPO_STYLE.md): extend the existing
renderer, use its XML construction and the existing document writer, and keep authored examples
as ordinary Python. Explicit ordered segments are sufficient; genomic coordinates, a biological
simulator and a generic graphics framework would add unsupported scope.

Separate source facts from drawing conventions. Sparse bands are decorative schematic texture.
Color and band identity follow segments through transformations; neither implies a cytological map.
Use the smallest rendered comparison to settle sister geometry and label fit before polishing.

## Scope

- Extend the shared chromosome engine with variable segment lengths and explicit output dimensions.
- Add joined replicated chromosomes using identical sister content and a source-specified centromere.
- Add bounded within-arm deletion and reciprocal terminal exchange at segment boundaries.
- Add a separate exon/intron track renderer using thick exon blocks and thin connecting spans.
- Reuse the engine in the existing recipe and a new complete capability specimen.
- Document supported inputs, unsupported transformations and reproducible drawing/review commands.

## Non-goals

- Add a CLI, dependency, GUI, configuration schema, registry or generalized scene graph.
- Implement inversion, duplication, Robertsonian fusion, meiosis simulation or curved crossovers.
- Infer centromeres, exon coordinates, chromosome identity or measured band maps from labels.
- Edit Biotechnology LECT11, other course decks, existing raster sources, reveals or alt text.
- Expand the course artwork queue or replace the broader visual-renewal plan.

## Current state summary

Observed: `chromosome_svg(name, genes, *, centromere_after=None, junctions=(), pitch=64,
height=62, allele_labels=False)` returns `(fragment, width, boundaries)`. It draws equal-width
straight single chromatids with neutral ends, optional pale constricted collars, sparse bands,
live Atkinson Hyperlegible Next labels and white zigzag joins. Callers are
[chromosome_examples.py](../../../svg_tools/chromosome_examples.py) and
[test_svg_chromosomes.py](../../../tests/test_svg_chromosomes.py).

Stability evidence: direct Python 3.12 focused baseline on 2026-11-12 passed four tests in 0.02s:
`/opt/homebrew/bin/python3.12 -B -m pytest --noconftest -p no:cacheprovider
tests/test_svg_chromosomes.py -q`. This establishes the existing helper's tested contracts, not
repository-wide stability. No unresolved helper failure is known. The normal conftest calls Git;
no Git command or bootstrap is authorized in this task. A discovered core failure pauses the
extension and gets a separate narrow stabilization plan and experiment log. If the algorithm is
wrong, replace its approach in a separately reviewed algorithm plan before resuming.

Reference evidence supplied by the manager: Biotechnology deck11C slide 220 of 274 corresponds
to `set6_part4_30_32.djot:62`, local slide 6. Its `assets/set6_drawings/dna_cdna.drawn.svg`
has three blue genomic-DNA exon blocks and two intron spans on a thin gray backbone; mature RNA
and cDNA retain the three exons in order, adjacent, in green and ochre. The reference contains
no chromosome, centromere, helix or direction annotation. Its SHA-256 is
`2a717011a58f9e810dff67b902ae43b29a66b1d0caf7b311e76ffda800cc9f6b`.
The reference is read-only and owned by another manager.
Root personally inspected the current PDF page and source SVG proofs under
`_temp/chromosome_svg_tool/reference/`: `lect11c-page220.webp`, `dna_cdna-large.webp`,
and `dna_cdna-small.webp`. Those observations confirm the distinct thin-intron/block-exon contract.

BPQ reference findings supplied by the manager: `translocation/translocationlib.py` supplies
HTML/CSS chromosome vocabulary, not a drop-in SVG library; `deletion_mutants/deletionlib.py`
supplies deletion evidence/table logic. Preserve scientific distinctions when adapting style.

Focused local drawing references read under the SVG expert skill's `references/local-only/`:
`scientific_illustration/A_Handbook_of_Biological_Illustration-1988.md`, lines 276-285
(clarity and comparison), and `svg_authoring/Mastering_SVG-2018.md`, lines 635-663
(viewport versus viewBox). They inform restrained detail and scale, not biological assertions.

## Architecture boundaries and ownership

Architecture below is approved by `chromosome_architecture_resume` in
`_temp/chromosome_svg_tool/architecture_review.md`; its required corrections are incorporated.
No further architecture round is required for this bounded scope. One owner controls the shared
library and its tests. The recipe owner follows the approved contract.
Existing [drawing.py](../../../svg_tools/drawing.py) remains the document writer; use its
`write_svg()` for title/description, namespace and ASCII serialization.

### Shared contract

Use small immutable standard-library values in `svg_tools/chromosomes.py`:

- `Segment(label, color, length=64, band=0)`: schematic positive length, six-digit hex color,
  string label, and fixed decorative-pattern index. Band assignment is explicit and stable;
  legacy inputs assign their current positional pattern once on construction.
- `Chromosome(segments, centromere_after=None)`: nonempty ordered tuple of segments and an
  optional internal boundary. The model carries source content, not SVG placement or IDs.
- `render_chromosome(name, chromosome, *, width=None, height=62, bands=True,
  sisters=False, junctions=(), allele_labels=False) -> (fragment, width, boundaries)`.
  Width defaults to summed segment lengths plus existing caps/collar. Explicit width scales
  horizontal geometry to that outline width; height controls total body height, including both
  sisters when requested. Stroke extends beyond the outline and needs document margins.
  Labels retain live text and are not stretched with the geometry. Returned boundaries are
  actual rendered x coordinates; centromere boundary remains its collar center.
- Keep `chromosome_svg()` signature and return contract unchanged as the compatibility entry.
  It constructs equal-length segments and uses the same rendering engine. Preserve accepted
  old geometry, allele typography and visual treatment without demanding byte-identical XML.

One unlabeled segment with the requested color and `bands=False` supplies a plain rod, including
caps in that same fill. Preserve the legacy helper's neutral caps through a private core setting
if needed; do not add a public palette option or a second renderer:

```python
rod = Chromosome((Segment("", "#00775F"),))
fragment, width, boundaries = render_chromosome("plain", rod, width=300, height=50, bands=False)
```

Different
segment lengths support meaningful deletion shortening without a coordinate engine. Rendering
the result at its natural width preserves length differences; explicitly normalizing both
before and after to the same width is a caller choice and must not imply unchanged length.
All before/after and exchange specimens use a common length scale, preserving each surviving
segment's relative length and band coordinates. Prefer natural width for model comparisons;
apply the same enclosing scale to an entire comparison when resizing. Explicit width is useful
for standalone placement and plain rods, not independent normalization of comparison products.

Sisters require a centromere boundary. Draw two matched sister bodies visibly attached at that
boundary, with separate arms and matching order, colors and texture on both. A narrow shared
connection and diverging arms should make the joined silhouette readable at reduced size.
The complete sister outline stays within the requested width and total height envelope; margins
for outline strokes and external recipe annotations are additional, just as for single rods.
`sisters=True` means replicated copies of this chromosome, never two independently supplied
homologs. Flat single bodies remain the default. Renderer validation rejects missing centromeres
for sisters and impossible geometry. Use a modest conservative width-based font-size adjustment
shared by the core, preserving default single-letter/allele sizing where it fits. Preserve legacy
accepted strings, including XML-sensitive text and the existing Greek-alpha escaping case, as
live text with allele tspans. Do not add arbitrary minimum-font-size rejection, horizontal glyph
stretching or a font discovery/shaping dependency. Document short-label usage: width estimates
are approximate, and actual Next-font proof at the intended display size establishes legibility.
Callers enlarge the presentation or shorten text when needed.

Transformation functions return new models; inputs remain unchanged:

- `delete_segments(chromosome, start, stop) -> Chromosome`: remove the half-open segment range.
  First support internal within-arm deletion only: `0 < start < stop < n`, and, when a
  centromere exists, require `stop <= c` or `start >= c`: reject only strict crossing
  `start < c < stop`. The centromere is a boundary; adjacent segment deletion preserves it.
  Preserve surviving segment objects, lengths, colors and bands; shift `c` left by the removed
  count for left-arm deletion and retain it for right-arm deletion. The endpoint rule preserves
  nonempty arms. Reject centromere-crossing, terminal and empty deletions with explanatory errors.
- `reciprocal_translocation(left, left_cut, right, right_cut) -> (Chromosome, Chromosome)`:
  exchange right tails after explicit internal cuts strictly distal to each known centromere
  (`c < cut < n`). Each product keeps its centromere-bearing prefix and one donor tail in
  original order. Require a known centromere on both inputs. Reject a cut at/proximal to the
  centromere and unsupported acentric/dicentric outcomes. Do not reverse a tail or recolor it.

This first operation contract deliberately supports one orientation. Existing recipes with
explicit left-tail products continue to render their provided data; do not claim they were
computed by the new right-tail operation. Diagram recipes own cut arrows and join markers;
use returned boundary coordinates, deletion join `start`, and exchange join `cut`. When a
deletion junction equals the resulting centromere boundary, omit the optional white zigzag and
annotate the cut in the recipe. Keep the renderer's distinct join/centromere rule; no extra model
field is needed.

Add `gene_track_svg(name, exons, intron_lengths, *, width=None, height=50)` in a small
`svg_tools/gene_tracks.py`. Exons reuse `Segment` values for label/color/length; chromosome
texture indices have no meaning here and are ignored. Require exactly `len(exons)-1`
finite nonnegative intron lengths. Positive spans connect exon blocks with thin continuous
lines; zero spans make adjacent exon blocks for the demonstrated mature RNA/cDNA relationship.
Return `(fragment, width, boundaries)` with boundaries defined as each exon start plus final
exon end; document this distinction from chromosome inter-region boundaries. Draw no caps,
centromeres, sisters or cytological bands. The recipe owns biological row names and process
arrows; this renderer does not infer splicing or transcription from colors.

Share only actual drawing conventions: XML escaping, Next text, outline palette and proportional
stroke hierarchy. Reuse private chromosome segment validation if useful; do not create a new
style/configuration layer. Preserve requested source colors. Ensure readable contrasting label
ink for both light and dark requested fills. Names are caller-supplied unique XML-safe prefixes;
all nested IDs remain local to that prefix, including sister instances.

### Mapping (milestones -> components)

| Milestone | Component | Review boundary |
| --- | --- | --- |
| M1 | Segment and renderer contracts | Architect approval and focused baseline |
| M2 | Chromosome engine and transformations | Scientific invariants and compatibility |
| M3 | DNA track and example recipes | Distinct anatomy and genuine shared reuse |
| M4 | Rendered artifacts and documentation | Independent spec, quality and integration review |

### File scope

| File or directory | Intended change | Canonical source, for generated output |
| --- | --- | --- |
| `svg_tools/chromosomes.py` | Model, core renderer, legacy entry and transformations | Authored Python |
| `svg_tools/gene_tracks.py` | Separate exon/intron geometry | Authored Python |
| `svg_tools/chromosome_examples.py` | Keep existing callers on shared engine; new capability specimen | Authored Python |
| `tests/test_svg_chromosomes.py` | Extend meaningful compatibility and transformation tests | Inline test cases |
| `tests/test_svg_gene_tracks.py` | Exon order, gaps and biological separation | Inline test cases |
| `svg_tools/README.md` | Minimal usage and limitations | Implemented APIs |
| `docs/slide-specs/GENETICS_ILLUSTRATION_GUIDE.md` | Link reviewed capability specimen | Actual review evidence |
| `docs/slide-specs/illustration_examples/chromosome_tool.drawn.svg` | New complete specimen | Existing example recipe |
| `docs/slide-specs/illustration_examples/chromosome_language.drawn.svg` | Regenerate only if needed | Existing example recipe |
| `_temp/chromosome_svg_tool/` | Render/font proof and review reports | Generated specimens |
| `docs/CHANGELOG.md` | Scoped completed-tool entry | Verified implementation |

Existing generated scratch candidates may be regenerated by the existing recipe. No course
asset is overwritten. Other agents' changes remain intact; coordinate shared documentation edits.

## Milestone plan

| M | Title | Summary | Goal |
| --- | --- | --- | --- |
| M1 | Approve bounded contracts | Review architecture and recorded baseline | Implementable shared interface |
| M2 | Extend chromosome engine | Model, geometry and bounded operations | Reusable tested chromosomes |
| M3 | Demonstrate distinct tracks | DNA renderer and complete specimen | All requested modes visible |
| M4 | Verify delivery | Render, font proof, review and usage docs | Reviewable finished tool |

### Milestone: Approve bounded contracts

M1 depends on the observed existing helper and named DNA reference. Entry: this draft and the
four-test baseline. Complete: architect approved the shared API and scientific bounds in
`_temp/chromosome_svg_tool/architecture_review.md`; required corrections are reflected here.
Root verified the existing four tests pass again this turn. Implementation may proceed without
another human approval or architecture round.
Parallel-plan ready: no; model and geometry decisions precede dependent work.

### Milestone: Extend chromosome engine

M2 depends on M1. Entry: approved contracts. Deliverables: shared engine, old API compatibility,
bounded transformations and focused tests. Exit: prior helper tests pass, transformation tests
prove segment/centromere conservation, and first small/large single/sister previews show distinct
joined sisters. Correct localized defects before proceeding; record any algorithm failure in a
separate stabilization document rather than layering geometry patches.
Parallel-plan ready: no; one owner avoids competing changes to the same engine.

### Milestone: Demonstrate distinct tracks

M3 depends on M2's stable contract. Deliverables: gene track helper, tests and example-recipe
extension producing the new complete specimen. Include plain one-color rod, banded rod, optional
centromere, joined sisters, deletion before/after, both reciprocal translocation products, and
genomic exon/intron versus adjacent RNA/cDNA tracks. Preserve ancestry via labels and colors;
document that RNA/cDNA row colors identify molecule type. Use variable segment lengths in at
least one example. Exit: every mode is generated through shared functions, existing examples
still work, and the original DNA reference remains unchanged.
Parallel-plan ready: yes; after the shared contract is stable, track implementation and specimen
composition can be separately owned with explicit file boundaries.

### Milestone: Verify delivery

M4 depends on M2 and M3. Deliverables: focused results, complete specimen previews at 480 and
1440 pixels wide (small comparison and large lecture review), actual-font proof, independent
specification/quality/integration reports, and usage docs. Entry: all required examples exist.
Exit: root personally views both proofs; fresh reviewers accept science, geometry, labels,
purity and shared reuse; all material defects are corrected and rerendered. Record full-suite
and native-export limits honestly. Parallel-plan ready: yes; independent reviews may inspect
the same frozen artifacts while one implementation owner applies resulting corrections.

## Test and verification strategy

Retain compact behavior tests for model validation, finite positive dimensions, legacy return
geometry/allele labels and accepted strings, adjacent deletion acceptance and strict-crossing
rejection, deletion order/length/centromere shift, reciprocal conservation of all
source segments, deterministic band identity after relocation, and joined sister duplication.
Use two parents with distinguishable unequal lengths/colors/bands so accidental recoloring or
positional regeneration is visible. Gene-track tests check exon order, thin positive introns,
zero-span adjacency and absence of chromosome-only features. XML composition checks protect
escaping, ASCII bytes, unique IDs/local references and pure-vector self-contained output. Check
plain-rod caps match the requested fill while legacy caps retain their neutral treatment. Include
a narrow/long-label example in scratch review without adding permanent visual fixtures.
Avoid path-string snapshots, pixel-perfect baselines and test-per-helper coverage.

Run focused tests using direct Python with `--noconftest -p no:cacheprovider`; inspect any added
test imports before execution for indirect Git/LibreOffice. Run required applicable lint checks
only through a verified Git-free path. Normal `pytest tests/` is not currently permitted because
conftest invokes Git; several repository checks may also use Git directly. Execution records
this limitation rather than disabling rules, modifying runtime configuration or claiming a
full-suite pass. If a supported Git-free full-suite route is established, inspect it first and
run it; otherwise this limitation is explicit in handoff.

Render with `PANGOCAIRO_BACKEND=fc` for rsvg on this host. Default rsvg silently substitutes
Helvetica. Verify actual selected/embedded fonts using the established method in
`_temp/hemophilia_problem_183/art_v2/font_verification.json`; family declarations and `fc-match`
alone are insufficient. Save reproducible proof and font identities in this task's scratch
directory. Correct backend/font selection and rerender before visual acceptance.

Review at both sizes for joined sister silhouette, centromere continuity, stable bands,
distinct thin introns, legible live labels, uncut endcaps/strokes and unambiguous before/after
length. If geometry loses meaning at small size, simplify detail or increase presentation size
and document the supported minimum. Do not manufacture biological features to improve silhouette.

The library deliverable does not claim lecture/native export acceptance. If claiming Impress/PDF
compatibility, make a scratch Djot specimen under this task's directory, use a repository wrapper
outside the sandbox for every LibreOffice-capable command, and inspect that actual ODP/PDF.
Check wrappers for indirect Git before execution. No unrelated course export is required.

## Migration and compatibility policy

The existing public helper remains usable without caller changes. The existing example recipe
must actually use the shared engine; do not maintain a second body implementation for new modes.
Existing explicit source arrangements remain explicit. The new transformations are bounded
operations, not retroactive claims that every prior illustration was scientifically simulated.
Retain editable original SVGs and all source course/raster/reveal content unchanged.

## Risk register

| Risk | Impact | Trigger | Owner | Mitigation |
| --- | --- | --- | --- | --- |
| Sisters read as homologs | Wrong chromosome count | Separate unjoined rods | Renderer owner | Shared centromere and rendered science review |
| Bands/colors follow positions | False ancestry | Deletion/exchange renumbers texture | Model owner | Preserve segment values and test conservation |
| DNA inherits centromeres | Wrong abstraction | Reusing chromosome geometry for gene tracks | Track owner | Separate geometry and named-reference review |
| Narrow geometry clips text | Lost labels | Small requested width/dark fill | Renderer owner | Conservative font fitting, short-label guidance, contrast and two-size review |
| Font substitution | Misleading visual acceptance | Default host rendering backend | Review owner | Actual font proof before acceptance |

## Documentation close-out requirements

Document shortest working calls for plain rod, sisters, deletion/exchange and exon/intron track.
Explain width versus biological length and explicit operation limits. Link the generated specimen
from the illustration guide, with source recipe and review scope. Record dated implementation and
verification in the changelog and this task ledger; broader plan updates belong to the root
manager. Keep temporary evidence under `_temp/`; permanent tests must earn their maintenance.

## Open questions and decisions needed

No human input is required to implement this bounded scope. The architecture entry gate is
complete with required corrections incorporated. The implementer may refine names or internal
geometry if contracts remain intact;
cross-cutting changes return to the architect. Source-specific course migration is future work
requiring actual course scope, not an unresolved condition for delivering this tool.
