# Plan: LLM-facing scientific SVG toolkit

Status: COMPLETE. See the [progress ledger](svg_toolkit_progress.md).

## Context

This toolkit lets a coding LLM reconstruct an existing slide illustration or create a new one
from a request. It extends the existing chromosome and gene-track helpers with reusable,
editable SVG parts, clear recipes, and stable visual conventions.

## Objectives

- Deliver biological parts, annotations, icons, plots, and text helpers through small Python APIs.
- Give a fresh coding agent enough examples to make a finished illustration independently.
- Use one consistent visual language in the gallery and selected lecture replacements.
- Complete implementation and verification through manager and subagent work.

## Design philosophy

Apply Keep it simple (KISS) and Finish the obvious. Use ordinary Python functions, authored
coordinates, one shared part value, and runnable recipes. Each component earns its place through
a committed gallery example or a demonstrated failure it prevents.

## Scope

- Implement composition, typography, annotations, icons, curves, plots, signaling, cells, gene
  features, antibody parts, and phenotype tokens.
- Publish a capability catalogue, cookbook, gallery, and native showcase.
- Replace the five selected lecture illustration families and produce native proof exports.
- Add direct project-root discovery so focused native exports run through configured Python.

## Non-goals

- Keep diagram layout authored; alignment and distribution cover the committed recipes.
- Keep scientific relationships and quantitative models explicit in recipes.
- Keep generative models and automatic SVG optimization outside this deterministic toolkit.
- Keep realistic human anatomy and Biotechnology LECT11 outside this version.
- Reuse established BPQ and Virtual Lab capabilities for pedigrees, gels, trees, crosses, and lab
  equipment.

## Architecture boundaries and ownership

### Shared interfaces

`SvgPart` holds an SVG fragment, conservative painted bounds, and named attachment points.
Transforms return a new part with transformed bounds and points. Grouping and alignment operate
on parts. Existing chromosome and gene-track interfaces remain available through adapters.

Text measurement uses bundled Atkinson Hyperlegible Next for ordinary labels and Mono for aligned
sequences; renderers require those font families to be installed.
Text helpers measure, wrap, style, support scripts, and report overflow. SVG composition preserves
viewBox geometry, inherited presentation, editable text, and local definitions while namespacing
instance identifiers and references.

The toolkit uses `svgpathtools` for concrete curve geometry, installed Matplotlib for plots, and
individual Lucide assets for general icons. Output contains its geometry and resources with editable
labels; the named fonts are external and must be installed.

### File scope

| Area | Intended change |
| --- | --- |
| `slide_lib/djot_sources.py` | Discover project root by ancestor markers for direct Python builds. |
| `svg_tools/parts.py` | Add `SvgPart`, transforms, grouping, alignment, and distribution. |
| `svg_tools/text.py` | Add font-backed labels, styled runs, wrapping, and extraction. |
| `svg_tools/svg_import.py` | Normalize imported figure SVGs and namespace IDs/references. |
| `svg_tools/icons.py` | Search and load selected Lucide icons. |
| `svg_tools/annotations.py` | Add flow and explanatory annotation parts. |
| `svg_tools/curves.py` | Add sampled curve placement helpers. |
| `svg_tools/signaling.py` | Add membrane, receptor, ligand, protein, activity, and phosphate parts. |
| `svg_tools/plots.py` | Convert scoped Matplotlib figures into parts. |
| `svg_tools/cells.py` | Add cell envelopes, nuclei, and organelles. |
| `svg_tools/gene_tracks.py` | Add directional features and operon assembly. |
| `svg_tools/binding.py` | Add antibody, antigen, and enzyme-tag parts. |
| `svg_tools/phenotypes.py` | Add seed, flower, and population parts. |
| `svg_tools/examples/` | Keep each runnable recipe beside its generated illustration. |
| `tests/test_svg_*.py` | Keep focused behavior tests that protect public contracts. |
| `docs/` | Publish the catalogue, cookbook, gallery, completion report, and changelog entry. |

## Milestone plan

| M | Deliverable | Dependencies | Completion evidence |
| --- | --- | --- | --- |
| M1 | Marker-based project-root discovery | None | Copied/nested project and include checks pass. |
| M2 | `SvgPart` and existing-renderer adapters | None | Bounds and attachment points match representative parts. |
| M3 | Transform, group, align, distribute helpers | M2 | Repeated parts retain transformed identities. |
| M4 | Font-backed labels and Atkinson default | M2 | Valid escaped XML renders bundled ordinary text. |
| M5 | Styled text, scripts, wrapping, extraction | M4 | Words and styled runs survive round-trip; overflow is explicit. |
| M6 | SVG import normalization and namespacing | M2-M4 | Repeated imported figures preserve text and local references. |
| M7 | Icon search and loading | M3, M6 | Icons render offline with correct color and proportions. |
| M8 | Boxes, arrows, inhibition bars, callouts | M3-M5 | A branching workflow renders within declared bounds. |
| M9 | Distance-based curve placement | M2 | Repeated parts follow tangent orientation and spacing. |
| M10 | Curved/straight membrane components | M3, M9 | Bilayer orientation remains coherent around receptor gaps. |
| M11 | Protein, ligand, receptor components | M3, M4, M10 | Shared-family parts expose useful anchors. |
| M12 | Activity and phosphorylation states | M8, M11 | Independent active/inactive and phosphate states render. |
| M13 | Scoped Matplotlib plot import | M4, M6 | Four plot types retain data and editable labels. |
| M14 | Animal, bacterial, yeast, plant cell envelopes | M3, M4, M12 | Cell types and nucleus counts remain distinct. |
| M15 | Organelle parts | M14 | Composed cell has recognizable labeled organelles. |
| M16 | Gene features and operon assembly | M3-M5, M8 | Direction/order and exon/intron proportions remain supplied. |
| M17 | Antibody, antigen, enzyme-tag parts | M3, M4, M12 | Western and sandwich contacts are explicit. |
| M18 | Seeds, flowers, population arrangements | M3, M4, M12 | Correct four seed combinations and counted populations render. |
| M19 | Catalogue, cookbook, gallery, showcase | M5-M18 | Every public API has a runnable visible example. |
| M20 | Genetics 03F genome-composition adoption | M13 | Six source values/categories remain without normalization. |
| M21 | Genetics 11D array-workflow adoption | M7, M8 | Both methods, arrays, labels, and relationships remain. |
| M22 | Genetics 09D yeast-stage adoption | M14 | Stages and one-vs-two nuclei remain clear. |
| M23 | Genetics 04G seed-phenotype adoption | M18 | Four phenotype combinations and labels remain correct. |
| M24 | Biotechnology 04C Western adoption | M17 | Correct contacts appear in all seven source uses. |
| M25 | Native showcase and focused proof exports | M1, M19-M24 | ODP/PDF proofs preserve text, placement, and proportions. |
| M26 | Fresh-agent new-slide and reconstruction trials | M19, M25 | Both tasks succeed using published documentation alone. |
| M27 | Integration closeout | M26 | Fresh integration review accepts all required artifacts. |

Milestones with separate files run in parallel after their dependencies pass. Shared part contracts are
completed before dependent biological families begin.

## Test and verification strategy

Permanent tests protect marker root discovery, include containment, part transforms, text escaping and
overflow, imported SVG reference namespacing, curve spacing, independent signaling states, directional
gene features, and invalid-write preservation. Run focused selected tests with direct Python and
`--noconftest`.

Render every gallery example and lecture replacement at intended slide size. An independent visual agent
checks labels, states, counts, clipping, semantic colors, and common visual language. Build focused native
proofs through the LibreOffice wrapper outside the sandbox. Fresh coding agents perform the documented
new-slide and reconstruction exercises; failures become focused fixes and a repeated trial.

## Migration and compatibility policy

Existing chromosome and gene-track public interfaces remain available. New calls use Atkinson by default
while explicit font selection remains valid. New lecture assets sit beside originals; only the selected
Djot image paths change. All surrounding source text, ordering, hidden states, and native slide content
remain preserved.

## Risk register

| Risk | Trigger | Owner | Correction |
| --- | --- | --- | --- |
| Visual drift | Components lose shared styling | Signaling owner | Establish and apply the signaling composite conventions. |
| Scientific distortion | States, contacts, values, or counts change | Component owner | Compare supplied source facts and regenerate. |
| Composition loss | Imported figures collide or inherit styling | Import owner | Correct normalization and retain focused regression coverage. |
| Text clipping | Rendered font metrics differ | Typography owner | Compare renders and correct measurement/wrapping. |
| Unused architecture | Helper has no committed consumer | Manager | Remove it or connect it to a required artifact. |
| Agent usability failure | Fresh agent cannot complete documented task | API/docs owners | Correct the smallest responsible gap and repeat the trial. |

## Documentation close-out requirements

- Maintain this plan and `svg_toolkit_progress.md` during implementation.
- Publish the capability catalogue, cookbook, examples, gallery, provenance, actual checks, and limits.
- Update `svg_tools/README.md`, the roadmap, installation guidance, and `docs/CHANGELOG.md`.
- Retain canonical generators and final proofs; clear disposable artifacts from `_temp/`.

