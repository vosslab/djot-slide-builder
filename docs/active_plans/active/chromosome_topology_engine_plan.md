# Plan: Build the chromosome topology engine

## Context

The four selected review figures expose three limits in their current recipes. Centromeres depend on
paint boundaries, chromosome poses depend on manually authored SVG curves, and the fusion product
has its arms and centromere painted separately. This plan supersedes the implementation limits in
[chromosome_svg_tool_plan.md](chromosome_svg_tool_plan.md) and
[chromosome_svg_tool_v2_plan.md](chromosome_svg_tool_v2_plan.md) for the work below. Those plans
retain their historical evidence.

## Objectives

- Model material, annotations, and replication with immutable, source-addressed biology.
- Draw chromatids and sister pairs from authored points with the existing BPQ surface paint.
- Regenerate and review C18, C20, C29, and C66 in the complete native chromosome review deck.
- Have an author unfamiliar with the implementation build a new example from the public contract.

## Design philosophy

Apply Keep it simple (KISS) and Atomic task decomposition. A chromosome is an ordered walk of
retained source intervals. Pure operations return the resulting material. A figure recipe chooses
the product, layout, visual crossings, and interpretation, and the shared surface painter draws it.
Use a short authoring exercise and four real figures to check the division of responsibility.

## Scope

- Add pure split, reverse, copy, join, homolog, replicate, and centromere-activity operations.
- Add a points-to-spline pose and a projection from topology into the existing renderer.
- Keep the current generator entrypoints. Select only the four branches in the table below for
  engine-based rendering. Publish only their four prototype SVG replacements.
- Check the staged full review deck as editable ODP and rendered PDF. Address the preexisting C31
  caption slot failure by merging paragraph breaks while retaining its text and meaning.

## Non-goals

- Defer persistent `Site` addressing, topology history, and an event or graph framework.
- Defer broader figure migration and lecture SVG publication.
- Defer dedicated public methods for named rearrangements. Use inversion and four-chromatid
  examples to check what the linear primitives can express. Treat a ring as a conceptual sketch.
  A closed walk would need explicit closure and a pose API that accepts coincident endpoints.
  The initial engine models linear material and draws open poses.

## Baseline

The baseline is in `_temp/chromosome_engine/baseline/`. The two existing SVG test modules passed
all 18 checks. The base suite at `cbfdf5cbacac5e7fed2416936fec6192e9e4e875` reported 9,417 passed,
one failed, and one warning. The failure is C31 at line 881 of
[chromosome_review_part_01.djot](../../../prototype/chromosome_review_part_01.djot), where the
`big-image` caption contains three paragraphs and the native layout allows one or two. The warning
concerns the source line count of [HUMAN_GUIDANCE.md](../../HUMAN_GUIDANCE.md). The C31 source
now has one fewer paragraph break, and its focused native caption check passes.

The baseline freezes 206 prototype SVGs, 1,124 lecture SVGs, and 29 selected source and output
files. At baseline, each target's prototype and lecture SHA-256 agreed with its CSV row.
Staging the four entrypoints reproduced all four baseline target SVGs byte for byte among 48 outputs.
The staged C18 sibling `autosome_set_nomenclature.drawn.svg` already differs from its published
prototype counterpart. Compare sibling regeneration to `generated_svg.sha256` and check the
published tree against the separate prototype and lecture manifests.

## Architecture boundaries and ownership

### Mapping (milestones -> components)

| Milestones | Component | Review boundary |
| --- | --- | --- |
| M1-M2 | Plan and baseline | Scope, source mappings, and interfaces |
| M3-M4 | Pure topology | Source identity, annotation projection, and operation invariants |
| M5 | Geometry | Authored points, spline length, and placement |
| M6-M7 | Rendering | Topology projection and existing BPQ paint |
| M8-M11 | Figure recipes | Each selected branch and its source composition |
| M12-M13 | Independent authoring and review | Public contract and evidence on actual SVG output |
| M14-M15 | Integration | Bounded publication, native export, and closeout |

### File scope

- `svg_tools/` owns the pure topology, spline, and projection. The existing `chromosomes.py` and
  `chromosome_surface.py` paint implementation serves both current and engine-backed callers.
- The four recipes below own the figure-specific model, palette, poses, and composition. Each
  selected branch follows this flow.

  ```text
  Python, JSON, or YAML biological definitions
      -> topology -> spline -> BPQ renderer -> SvgPart
      -> Python and structured-data composition -> final SVG
  ```

  The selected branches build their panels, leaders, labels, and legends in Python with shared
  SVG helpers. JSON stores generator-owned definitions and layout data. Use YAML for
  human-edited configuration. The engine starts with biological definitions and numeric pose
  points. The selected compositions start with generated engine parts and structured layout
  data. SVG/XML is serialized at the drawing and composition steps. The C29 composition adds
  group elements around its generated fragments during output assembly. Exercise the normal
  generators and isolate each selected branch with existing SVG/XML reads denied. Check
  regenerated sibling bytes against the baseline.
- `prototype/chromosome_replacements.csv` records the four reviewed replacements and their hashes.
  The review deck retains native Djot titles and captions. The lecture rows are frozen in the
  baseline's `target_samples.csv`.
- Use focused tests for enduring contracts and `_temp/chromosome_engine/` for staged figures,
  native exports, one-time probes, and review evidence. Update durable usage and changelog docs
  during closeout.

| Review ID | Recipe and selected branch | Prototype replacement path |
| --- | --- | --- |
| C18 | `genetics/LECT06/djot/make_chromosome_xlinked.py`, Drosophila complements | `prototype/assets/lect06d-x_linked_genes_1/drosophila_chromosome_complements.drawn.svg` |
| C20 | `genetics/LECT08/djot/chromosome_recipes/cis_recipe.py`, wide panel | `prototype/assets/lect08b-chap8-linked_genes/cis_trans_wide.drawn.svg` |
| C29 | `genetics/LECT09/djot/make_centromere.py`, `chromosome_body()` | `prototype/assets/lect09_tetrad_concepts/centromere.drawn.svg` |
| C66 | `genetics/LECT13/djot/lect13d_chromosome_recipes.py`, `fusion()` | `prototype/chromosome_assets/assets/lect13d-meiosis_translocation/robertsonian_centromeric_fusion.drawn.svg` |

### Topology and rendering contracts

- Source material owns length and immutable half-open native intervals. Chromatids retain ordered,
  oriented slices of source material. Regions carry semantic IDs. Loci and centromeres retain
  source identity and position, independent of paint boundaries. Homologs share locus coordinates
  and can carry different alleles under distinct source IDs. Centromere activity is copy-specific.
- Fractions for operations are measured along the current input, in its current order. Split at an
  interior fraction and return both fragments. Clip source intervals when projecting and reverse
  their display positions with the walk. At a split exactly on a point annotation, the interval on
  the higher side in native coordinates owns it regardless of walk orientation. The final native
  interval owns any annotation at the source's distal endpoint.
- Give copied material a distinct copy ID. Join oriented pieces in the supplied order, consuming
  facing ends and retaining the two outer ends. Model true ends, fresh cut ends, and deliberate
  joins from material adjacency. Store connections at integer span boundaries and derive public
  junction distances from the flattened walk. Pairing and visual crossing do not join DNA.
- Pose code resolves authored points into a centerline and maps the ordered material by arc length.
  Use an open Catmull-Rom spline, fixed body width, and a shared material-to-display scale when
  comparing product lengths. Check for local folds. The pair API translates two copies of one
  reference pose along the normal at their corresponding active centromeres.
- The renderer resolves paint through a palette keyed by `(source_id, region_id)`. Reuse BPQ
  contour, texture, sheen, marker, and label painting. Place projected loci and centromeres at their
  own coordinates. True ends receive telomere caps. A replicated pair draws two complete sister
  bodies and one shared foreground belt when each sister has exactly one corresponding active site.
  Other centromere counts use the individual chromatid renderer. Fit gene letters
  through the shared locus label pipeline and use external labels where body paint lacks
  clearance. Report exact locus anchors and conservative ink bounds.

## Milestone plan

The dependency column identifies the evidence needed to begin each milestone. Independent model,
geometry, and figure source inspection can proceed in parallel after their boundaries are agreed.

| M | Title | Depends on | Deliverable and exit evidence | Status |
| --- | --- | --- | --- | --- |
| M1 | Freeze the boundary | Approved scope | Four exact CSV mappings, pre-change hashes, staged generator hashes, and baseline test results. | Complete |
| M2 | Record the contracts | M1 source inspection | Define source and current coordinates, copy and fragment semantics, pose and paint boundaries, and the four branch selections. This plan records the agreed contracts. | Complete |
| M3 | Build the model | M2 material contract | Construct immutable source material, oriented slices, chromatid annotations, and their projection. Check clipped and reversed features and exact-cut ownership. | Complete |
| M4 | Implement generic operations | M3 values | Demonstrate split, reverse, copy, join, homolog, replicate, and activity changes. Check explicit products, conservation where applicable, and retained source identity. | Complete |
| M5 | Build the spline | M2 pose contract | Resolve authored point poses, verify interpolation and arc length, and check rejection of malformed geometry. | Complete |
| M6 | Project into the renderer | M3 and M5 | Reuse BPQ paint on the projected source regions, loci, and centromeres. Check output anchors, paint order, and end and join semantics. | Complete |
| M7 | Draw sisters | M4 and M6 | Verify two equal-length chromatids, corresponding attachments, and one shared foreground belt. | Complete |
| M8 | Migrate C20 | M6 and wide-panel layout | Preserve the wide comparison and the two locus positions. Verify cis ownership `w m` / `+ +` and trans ownership `w +` / `+ m`, and check portrait sibling output. | Complete |
| M9 | Migrate C29 | M7 and centromere layout | Verify the pair, the source-positioned centromere belt, and the legibility and leader targets of the composition. | Complete |
| M10 | Migrate C66 | M4, M6, and fusion source | Join the long-arm material in one continuous product, return removed material explicitly, and verify source ancestry and the declared centromere activity. Check the artwork and native caption agree. | Complete |
| M11 | Migrate C18 | M6 and complement data | Verify two unreplicated eight-chromosome complements, XX and XY, preserving the 2/3/4 pairs, central heterochromatin, and one centromere per rod. | Complete |
| M12 | Test unfamiliar authoring | M4-M7 public usage | Have a fresh author build a new example using public instructions and record any workarounds or missing explanations. | Complete |
| M13 | Review independently | M8-M12 staged results | Fresh reviewers check code quality, biology, readability, and the selected composition inputs. Fix findings and rerun affected checks. | Complete |
| M14 | Publish and verify natively | M13 and valid C31 caption | Update the four prototype SVGs and their inventory rows. Verify all other SVG hashes, editable native text, and the four rendered placements in a full ODP/PDF build. | Complete |
| M15 | Close checks and docs | M14 publication | Rerun focused checks, pyflakes, and the base suite. Update authoring and changelog docs and record final commands, outputs, and review evidence. | Complete |

## Verification evidence

Paths in the table are relative to `_temp/chromosome_engine/`.

| Milestones | Evidence |
| --- | --- |
| M1-M2 | `baseline/` contains the source and SVG manifests, exact replacement mappings, baseline generation, and test logs. |
| M3-M5 | The independent spec review passed 331 checks after the fixes for nested decimal junction cuts and closed poses. The independent quality review passed with 2,500 operation probes and 280 pose probes. The new topology module has 486 lines. |
| M6-M7 | The initial renderer kept 48 legacy outputs byte-for-byte compatible. A correction passed 49 focused checks with rotated collars and external terminal or crowded labels. See `render/correction/`. The shared painter refactor preserved the bytes of all 44 sibling SVGs. See `painter_refactor/comparison.log` for pixel comparisons. The final correction maps locus anchors directly from arc length. Fresh specification and quality reviews each passed 16 renderer tests and pyflakes. The serialized-spline probe checked six qualified and short anchor pairs across a single curved body and both sisters, with internal and external labels. Maximum coordinate deviation was `1.99e-12` display units. All 48 generated SVGs remained byte-identical across the anchor correction. |
| M8 | The wide branch loads one structured JSON entry. Its isolated build matched the accepted wide rendering pixel for pixel. The 858 x 323 crop preserves all eight internal gene labels. The portrait sibling matches the baseline bytes. See `composition/c20/c20_wide_white_q90.webp`. |
| M9 | Python composes the sister bodies, belt and locus anchors, leaders, and labels with `centromere.json`. The schematic q-arm locus `A` corresponds to the native question. See `composition/c29/c29.webp`. |
| M10 | Python composes the input and product `SvgPart` objects, labels, and arrow. The model retains B's inactive centromere in the long-arm fusion and draws A's active collar. It uses q lengths 100 and 46, p lengths 10 and 5.6, and total input length 161.6 at scale 5.2 and width 30. B's p arm is about 12.2% of its q arm in the schematic for visibility. All 39 generated siblings match the baseline. See `composition/c66/c66.webp` and `composition/c66/verification.log`. |
| M11 | JSON describes the two unreplicated complements and their shared arms, leaders, panels, and legend. The model has 16 distinct source IDs and equal lengths within homolog pairs. Quality review corrected the 3L leader. All four generated siblings match the baseline. See `composition/c18/c18-1100.webp`. |
| M12 | A fresh author used [CHROMOSOME_ENGINE.md](../../CHROMOSOME_ENGINE.md) to make alternate poses, a homolog, a sister pair from one pose, and a reciprocal terminal exchange. The products conserve all 448 source units as 196 + 252. The exercise led to clearer native span and bounds examples, and an external label that keeps a junction visible. See `authoring/AUTHORING_REPORT.md` and its three final WebPs. The guide examples also ran together during closeout in `doc_correction/`. |
| M13 | Independent review accepted all four staged compositions after the C18 leader and C20 crop corrections. Isolated builds of all four selected branches passed with existing SVG/XML reads denied. A fresh C66 import and build also passed with the legacy shell JSON read denied after moving that load to the sibling path. See `composition/c66_lazy/isolation_after.log`. All 44 siblings matched baseline bytes. The two final anchor reviews accepted the correction in M6-M7. |
| M14 | The pre-publication scope check matched all 1,330 baseline SVGs. Publication updated exactly the four selected prototype SVGs and their replacement CSV digests. The other 202 prototype and all 1,124 lecture SVGs retained their hashes and paths. The complete native deck has 73 slides and PDF pages. The four replacements are embedded byte for byte, with editable ODP titles and captions and selectable PDF text. See `final_publication/native_evidence.json`, `publish.log`, and `scope_after_build.log`. |
| M15 | The anchor correction passed 119 focused checks. After publication, `source source_me.sh && pytest tests/` exited 0 with 9,515 passed in 23.44 seconds. It reported line-count advisories for [HUMAN_GUIDANCE.md](../../HUMAN_GUIDANCE.md) at 938 lines and [chromosomes.py](../../../svg_tools/chromosomes.py) at 935. Pyflakes passed for 10 Python files and strict ASCII passed for 24 changed source and inventory files. The pre- and post-suite bytecode scans were clear and the obsolete C66 scratch check was removed. See `final_checks/` for the resulting logs. |

## Native review outputs

The full native build ran outside the sandbox and exited 0 in 18 seconds.

```bash
source source_me.sh && python3 deck_tools.py build prototype/chromosome_review.djot --format all
```

Both artifacts have 73 pages. SHA-256 hashes are from `final_publication/native_evidence.json`.
See `final_publication/commands.txt` and `build.log` for the build receipt.

| Artifact | SHA-256 |
| --- | --- |
| `output/odp/chromosome_review.odp` | `a40329beb75d22a05852f4bca17d93dd935ea3cf2c16533312478cbdf3dbe476` |
| `output/pdf/chromosome_review.pdf` | `15924f36ee55e9b9a82e7cb4028114ebcf2594b03df2b2fb94e815fad79b33c3` |

The independent visual review reproduced the PDF page renders byte for byte and accepted all four
placements. C18 appears on page 19, C20 on page 21, C29 on page 30, and C66 on page 70. The native
check verified all 68 review IDs, all 138 sample and replacement inventory hashes, all 70 prototype
SVG references, the cover timestamp, and the closing discussion slide. See
`final_publication/native_visual_review.md` and the page renders and extracted text in that folder.

## Final acceptance

The independent final integration review passed all 15 milestones, confirming the architecture,
scope hashes, four native placements, and material conservation in inversion and four-chromatid
exchange examples using the public API. The post-edit Markdown link, Djot link, and source line
count checks passed all 947 tests in 1.72 seconds with the same two line-count advisories.
Independent agent reviews and automated checks satisfy all completion gates. Instructor assessment
and live presentation remain optional follow-up.

## Test and verification strategy

- Run `source source_me.sh && python3 -m pytest tests/` and rerun focused tests for the changed
  model and render behavior. Use `pyflakes` for changed Python. The baseline exit codes and logs
  are `pytest_base.exit`, `pytest_base.log`, `pytest_svg.exit`, and `pytest_svg.log`.
- Stage generators at explicit temporary destinations. Check generated siblings against their
  baseline hashes and inspect target SVGs for ancestry, allele ownership, centromeres, caps,
  labels, and composition. If a sibling changes, trace the shared path and restore compatibility
  before publishing the four targets.
- Rerender the candidate SVGs and inspect the actual full native placements. Keep label text
  readable and figure titles and captions editable. Run LibreOffice through the existing scripts
  outside the sandbox. Record ODP and PDF evidence after visually checking the exported pages.
- Compare all preexisting non-target prototype SVGs and all lecture SVGs to the frozen manifests.
  If an asset differs, resolve the unexpected change before closing publication.
