# SVG toolkit progress

This ledger tracks execution of [svg_toolkit_plan.md](svg_toolkit_plan.md). The manager accepts a
milestone after its implementation evidence, fresh specification review, fresh quality review, and
applicable integration evidence are recorded here.

| M | Owner role | Dependencies | Status | Evidence | Specification review | Quality review |
| --- | --- | --- | --- | --- | --- | --- |
| M1 | Build owner | None | DONE | Implementation complete; 13 focused include tests passed. | PASS | PASS |
| M2 | Composition owner | None | DONE | 16 focused part, chromosome, and gene tests passed. | PASS; 5 independent parts tests passed. | PASS; 5 independent parts tests passed. |
| M3 | Fresh Terra composition owner | M2 | DONE | 10 combined placement and curve tests passed. [Foundation visual report](../reports/svg_toolkit_foundation_visual.md). | PASS | PASS |
| M4 | Fresh Terra typography owner | M2 | DONE | 4 text and drawing tests passed with the exact direct command. [Foundation visual report](../reports/svg_toolkit_foundation_visual.md). | Accepted by manager disposition. | PASS |
| M5 | Typography owner | M4 | DONE | 4 focused tests passed; blank-line height fixed and superscript reset. | PASS; 24 focused text, extraction, import, and protein tests. | PASS; 24 tests and manager-viewed styled text, SVG composition, and protein white-background WebPs. [Advanced quality report](../reports/svg_toolkit_advanced_quality.md). |
| M6 | Import owner | M2-M4 | DONE | 14 import tests and 23 combined tests with shared namespacing passed; structured XML fixes cover ARIA, data, and comment references. | PASS; 24 focused text, extraction, import, and protein tests. | PASS; 24 tests and manager-viewed styled text, SVG composition, and protein white-background WebPs. [Advanced quality report](../reports/svg_toolkit_advanced_quality.md). |
| M7 | Fresh Terra icon owner | M3, M6 | DONE | Implementation complete. | PASS | PASS; 13 tests. [Icon quality](../reports/svg_toolkit_icon_quality.md). |
| M8 | Fresh Terra annotation owner | M3-M5 | DONE | Implementation complete. | PASS | PASS; 3 tests. [Annotation quality](../reports/svg_toolkit_annotation_quality.md). |
| M9 | Fresh Terra curve owner | M2 | DONE | 7 own tests and 10 combined tests passed; installer recorded svgpathtools 1.8.0 and svgwrite 1.4.3. [Foundation visual report](../reports/svg_toolkit_foundation_visual.md). | PASS | PASS |
| M10 | Signaling owner | M3, M9 | DONE | 2 tests passed; manager viewed and refined membrane proof. [Membrane quality report](../reports/svg_toolkit_membrane_quality.md). | PASS | PASS |
| M11 | Signaling owner | M3, M4, M10 | DONE | Ligand and receptor origins are explicit. | PASS; 24 focused text, extraction, import, and protein tests. | PASS; 24 tests and manager-viewed styled text, SVG composition, and protein white-background WebPs. [Advanced quality report](../reports/svg_toolkit_advanced_quality.md). |
| M12 | Signaling owner | M8, M11 | DONE | Implementation complete; see D18. | PASS | PASS; 13 combined tests, Astra review and manager views. [Biology quality](../reports/svg_toolkit_biology_quality.md). |
| M13 | Fresh Terra plot owner | M4, M6 | DONE | Implementation complete. | PASS | PASS; 15 combined icon and plot tests. [Plot quality](../reports/svg_toolkit_plot_quality.md). |
| M14 | Cell owner | M3, M4, M12 | DONE | Cell API checkpoint below. | PASS | PASS; 6 combined family tests. [Cells, binding, and phenotypes quality](../reports/svg_toolkit_cells_binding_phenotypes_quality.md). |
| M15 | Cell owner | M14 | DONE | ER network corrected with six openings and explicit nucleus contact; lysosome and vesicle outlines documented as generic. Three focused tests passed. | PASS; fresh review. | PASS; fresh review. |
| M16 | Gene-track owner | M3-M5, M8 | DONE | Implementation complete. | PASS | PASS. [Biology quality](../reports/svg_toolkit_biology_quality.md). |
| M17 | Binding owner | M3, M4, M12 | DONE | Antibody API checkpoint below. | PASS | PASS. [Cells, binding, and phenotypes quality](../reports/svg_toolkit_cells_binding_phenotypes_quality.md). |
| M18 | Phenotype owner | M3, M4, M12 | DONE | Seed and flower API checkpoint below. | PASS | PASS. [Cells, binding, and phenotypes quality](../reports/svg_toolkit_cells_binding_phenotypes_quality.md). |
| M19 | Documentation owner | M5-M18 | DONE | Catalogue, cookbook, gallery with 17 SVGs and 17 WebPs, index, and native 17-slide source; source quotations updated. All 41 generated files reproduced byte-for-byte in an ordinary environment. | PASS; fresh review. | PASS; fresh review. |
| M20 | Plot pilot owner | M13 | DONE | Pilot complete. | PASS | PASS; Astra verified inverse SHA and raw values. |
| M21 | Workflow pilot owner | M7, M8 | DONE | Pilot complete. | PASS | PASS; source and byte proof. |
| M22 | Cell pilot owner | M14 | DONE | Two assets and two source URLs with hashes; original SVGs unchanged. | PASS | PASS |
| M23 | Phenotype pilot owner | M18 | DONE | Eight seeds, 22 labels, and one source URL with hashes; original SVG unchanged. | PASS | PASS |
| M24 | Binding pilot owner | M17 | DONE | Seven source URLs with hashes; original SVGs unchanged. | PASS | PASS |
| M25 | Export owner | M1, M19-M24 | DONE | Six ODP/PDF proofs contain 29 pages; 23 canonical SVGs embedded byte for byte. Earlier complete five-deck compilation produced 351 slides. [Native verification](../reports/svg_toolkit_native_verification.md); [native quality](../reports/svg_toolkit_native_quality.md). | PASS | PASS; fresh Astra review of all 29 pages. |
| M26 | Independent trial agents | M19, M25 | DONE | Fresh signaling and reconstruction artifacts accepted; reconstruction recipe promotion completed. Two additional native pages reviewed. [Repeat specification](../reports/svg_toolkit_reconstruction_repeat_spec.md); [trial quality](../reports/svg_toolkit_trials_quality.md). | PASS | PASS |
| M27 | Integration owner | M26 | DONE | Implementation and documentation accepted; [cleanup completed](../reports/svg_toolkit_cleanup.md). [Implementation report](../../SVG_TOOLKIT_IMPLEMENTATION_REPORT.md). | PASS; [final specification](../reports/svg_toolkit_final_spec.md). | PASS; [final quality and integration](../reports/svg_toolkit_final_integration.md). |

## Decisions

| ID | Decision | Evidence | Affected milestones |
| --- | --- | --- | --- |
| D1 | Use ordinary Python recipes and authored placement with `SvgPart(fragment, bounds, anchors)`; each capability has a committed consumer. Adapters measure text with the bundled Atkinson fonts using Pillow. M4 will reuse this measurement boundary; glyph-count approximation was rejected. | Approved plan and implementation. | M2-M24 |
| D2 | Use Atkinson Hyperlegible Next for normal labels and Mono for aligned sequences. Native root discovery requires both the `deck_tools.py` file and `slide_lib` directory, with resolved CWD as fallback. M27 owns documentation reconciliation. | Bundled project fonts, instructor direction, and M1 implementation. | M1, M4-M24, M27 |
| D3 | Use `svgpathtools` for curve geometry, Matplotlib for plots, and selected Lucide assets for icons. | Survey of cloned SVG repositories and installed Matplotlib. | M7, M9, M13 |
| D4 | Keep diagrams deterministic; use generative SVG repositories as design references only. | Editable-label and semantic-component requirements. | M2-M24 |
| D5 | Use agent assessments, automated checks, and focused native proofs as acceptance evidence. | Approved autonomous completion requirement. | M1-M27 |
| D6 | Keep Biotechnology LECT11 unchanged. | Existing manager ownership. | M20-M27 |
| D7 | Measure covered characters with the actual bundled Atkinson font. For missing glyphs, allow a conservative 1em horizontally per missing glyph and 1em vertically when any glyph is missing. Arbitrary host typefaces are outside this guarantee. | M2 review found missing Greek and cmap coverage; explicit fallback bounds address the gap. | M2, M4-M24 |
| D8 | M9 is the sole owner of pip manifest changes and adds `svgpathtools` and `matplotlib>=3.11.2`; M13 reuses the declared Matplotlib dependency. | Coordination decision to prevent concurrent manifest edits. | M9, M13 |
| D9 | M3 exposes `transform(part, x=0, y=0, rotation=0, scale=1)`, `group(dict[str, SvgPart])` with qualified anchors and namespaced IDs, `align(parts, edge, coordinate)`, and `distribute(parts, axis, gap)`. The group namespacing helper will be reused by M6. | Approved shared composition API. | M3, M6 |
| D10 | M4 exposes `label(x, y, value, *, size, color, anchor='middle', role='normal', bold=False, italic=False)` and `measure_text(value, *, size, role, bold, italic, anchor)` returning bounds. | Approved shared typography API. | M4-M24 |
| D11 | Self-contained SVG means geometry and resources are contained; live Atkinson Next and Mono fonts are intentionally unembedded and must be installed. | Typography decision. | M4-M27 |
| D12 | In the M19 placement example, use `labels=False` for the demo label touching the centromere. | Placement proof review. | M19 |
| D13 | Font functions produce finite geometry or raise a clear `ValueError`. Astronomical float matrix inputs are outside committed usage; the existing guard is preserved. | Typography review disposition. | M4, M5 |
| D14 | Membrane centerpoint gaps require caller head clearance; tails have a distinct central gap of +/- 0.04 thickness. | Membrane proof review. | M10-M18 |
| D15 | Protein APIs accept width, height, and color; `protein` accepts `kind='globular'|'kinase'`. Ligand and receptor origins and centered anchors are explicit; the receptor has a membrane stalk. | Signaling component decision. | M11-M18 |
| D16 | Logical wrapping ignores trailing unpainted spaces for fit, and bare whitespace runs no longer add paint bounds. Literal SVG text and cursor positions are preserved; `a b` fits width 12 at size 20. | Typography and extraction review. | M5, M8, M19 |
| D17 | Composition pattern labels use a light backing and Atkinson Hyperlegible Next. | Advanced composition proof review. | M6, M19 |
| D18 | In the M12 example, active kinase owns activation and inhibition; the phosphoinactive comparison remains unconnected. The API independently preserves phosphorylation and activity, including all four combinations. | Corrected signaling example and API review. | M12, M19 |
| D19 | Function annotations in `examples/binding.py` were brought into source style during M27. | Final source-style scan and focused checks. | M27 |
| D20 | `import_svg(markup, *, name, size=None)` preserves width and aspect ratio with a clipped viewport. | Import API decision. | M6, M7, M13 |
| D21 | Text APIs include `TextRun`, `styled_label`, and `wrapped_text(width, size, color, line_height=None, height=None, role)`; `extract_text` accepts a path and returns labels with literal x, y, and id plus candidate counts. | Typography and extraction API decision. | M5, M8, M19 |

## API checkpoints

- M14: `cell_envelope(*, kind, width, height, color, wall_color=None)` requires a wall color for plant cells. `nucleus` and `nucleolus` use centered lobe anchors.
- M15: `organelle(*, kind, width, height, color)` covers six kinds.
- M17: `antibody` exposes `Fab_left`, `Fab_right`, and `Fc` anchors.
- M18: `seed(*, size, color, shape='round')` and `flower(*, size, color, petals=5)` are defined in `svg_tools/phenotypes.py`.

## Baseline and process notes

- An earlier M2 specification review failed when font size 1000 raised `OSError`; the fix measures
  at reference size 1024. A second review exposed missing Greek and cmap coverage, addressed by D7.

- Pilot baseline capture is complete: [baseline manifest](../reports/svg_toolkit_pilot_baseline.json)
  records hashes for 11 files and 12 references. The historical snapshots in `_temp/svg_toolkit/baseline/` were removed during cleanup.
- The M1 quality reviewer reported running a read-only `git diff` before reading the prohibition.
  No file or metadata changes were intentionally made; unchanged metadata was not verified. The
  manager informed the user. Future review briefs restrict reviewers to explicit file reads and Python.
- The final M4 specification reviewer sourced `source_me.sh` against the exact direct Python brief;
  it invokes Git. No intentional file or metadata changes were reported; unchanged metadata was not
  verified. The M4 quality reviewer freshly reran the exact authorized direct command: 4 passed. The
  user was informed. Future briefs explicitly restrict bootstrap and Git.
- All 23 canonical SVG outputs were regenerated and embedded with the current MIME type. A tmux restore killed workers, but all 41 generated-file hashes persisted and were verified; all 41 files were subsequently reproduced from the new source.
- The interoperability audit records the text whitespace correction, focused checks, native export trace, and their limits: [Astra interoperability audit](../reports/svg_toolkit_astra_interop_audit.md).
- A third process deviation occurred when the cookbook semantics fix worker reported running read-only
  `git diff --check` despite the explicit command restriction. No metadata changes were intentional;
  unchanged metadata was not verified. The user was informed.
- Cookbook bootstrap commands and positive direct-runtime SVG guidance in AGENTS were corrected.
  Subsequent cookbook corrections cover inactive phosphorylated response, module imports and tabs,
  and temporary component output versus durable pilot defaults. Fresh specification and quality reviews passed.
- The Astra interoperability audit prompted the plain-label `xml:space` correction. The native chart
  diagnosis isolated LibreOffice namespace and XLINK requirements; shared `write_svg` normalization
  restored the genome chart. Allele endpoint padding and the signaling label were subsequently fixed;
  fresh native specification and quality reviews passed. Earlier failures are superseded.
- The first reconstruction trial failed italic gene-name fidelity. A styled-box API and documentation
  correction enabled a fresh reconstruction, which passed specification and quality review. Promotion
  of the accepted recipe is complete.
- Matplotlib reproducibility uses an intrinsic hash salt and `Date=None`; callers normalize the Next
  font, and the obsolete gallery environment-seed wrapper was removed. Module imports and types were
  cleaned up.
- M27 documentation closeout updated INSTALL, USAGE, DEVELOPMENT, DESIGN_DECISIONS, ROADMAP,
  CHANGELOG, and the cookbook; ASCII and links were verified. The changelog records accepted native
  proofs and the completed final integration review.
- Use explicit file operations and direct Python only; bootstrap and Git are outside the authorized scope.
- [Scratch cleanup](../reports/svg_toolkit_cleanup.md) is complete. Historical report paths under `_temp/` describe removed scratch; protected Biotechnology trees and shared caches were retained.

## Acceptance procedure

1. A fresh implementation agent records exact changed files and focused checks.
2. A fresh specification reviewer checks the milestone against `svg_toolkit_plan.md`.
3. A different fresh quality reviewer checks correctness, scope, maintainability, and rendered output.
4. The manager assigns corrections and repeats the affected review when a finding remains.
5. The integration owner records final cross-component evidence for M27.

