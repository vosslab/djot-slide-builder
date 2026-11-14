# SVG aesthetic upgrade plan

## Outcome and authority

Upgrade the existing SVG toolkit into one cohesive, locally authored scientific illustration
family following [SVG_VISUAL_STYLE.md](../../SVG_VISUAL_STYLE.md). Preserve editable geometry,
live Atkinson text, semantic colors, biological relationships, public APIs, anchors, and
accurate bounds. Use Servier semi-flat 2.5D drawing as a style reference only; import, tracing,
and adaptation of its geometry or images are outside this approved work.

All 14 milestones are complete; the [integration review](../reports/svg_aesthetic_integration.md)
records final acceptance after [cleanup](../reports/svg_aesthetic_cleanup.md).

The [SVG_AESTHETIC_UPGRADE_REPORT.md](../../SVG_AESTHETIC_UPGRADE_REPORT.md) records the
current results and limits. The separate [svg_aesthetic_progress.md](svg_aesthetic_progress.md)
ledger owns current status,
assigned owners, evidence, and unresolved findings. This plan owns scope and completion checks.
The completed [svg_toolkit_plan.md](svg_toolkit_plan.md) and its prior evidence are background;
previous passing renders do not establish acceptance of newly changed artwork.

## Scope and preserved content

Reach the shared drawing mechanics, all existing toolkit illustration families, their callers
and focused tests, gallery recipes, chromosome v2 demonstration, six active toolkit pilot SVGs,
two complete trial compositions, and native proof exports. Keep the original six pre-toolkit
pilot SVGs and original Genetics LECT02 `b_dna_helix.drawn.svg` byte-identical. Retain source
values, labels, scientific notation, counts, data, contacts, directions, and ordering.

Keep `biotech/LECT11`, `_temp/biotech_lect11*`, `_temp/matplotlib`, and `_temp/mplconfig` intact.
Use only repository-root `_temp/` for temporary work. Run no Git commands or `source_me.sh`.
Use `/opt/homebrew/bin/python3.12 -B` with `PYTHONPATH="$PWD"`; plotting uses the existing
repository-local Matplotlib cache. Every command that can launch LibreOffice runs outside
the sandbox through repository scripts.

## Milestones and acceptance

Each milestone has one accountable owner in the ledger. Owners adapt to concurrent changes
and preserve work outside their assigned files. Raise anatomy, API, or integration conflicts
early with a concrete example; investigate the conflict before accepting a visual compromise.

| Milestone | Work | Evidence required for completion |
| --- | --- | --- |
| M1 | Establish visual guide and immutable before baseline | Guide, 17 gallery WebPs plus index, gallery SVGs, chromosome v2, 6 pilot and 2 trial SVG snapshots, 7 protected-source hashes, ASCII and link checks. |
| M2 | Fix the two audited shared-state leaks | Focused namespace and gallery-caller state checks; no global state survives an import or build. |
| M3 | Add minimal uniform stroke and tone mechanics | Small geometry/bounds checks and rendered representative parts; caller colors remain usable. |
| M4 | Polish cells and nuclei | Clear envelopes and walls, uniform contours, stable nuclei counts and fused-yeast continuity; small and large renders. |
| M5 | Polish organelles | Distinctive internal anatomy with restrained tone, visible membrane gaps and correct generic claims; family render. |
| M6 | Polish membranes | Readable bilayer, bend spacing, deliberate gaps, and insertion/contact geometry; focused render and geometry checks. |
| M7 | Polish proteins and ligands | Distinct silhouettes, readable activity labels, independent phosphorylation, unchanged anchors; composed signaling render. |
| M8 | Polish binding | Antibody anatomy and exact contact topology preserved through individual and composed renders. |
| M9 | Polish chromosomes and gene tracks | Stable loci, bands, lengths, directions, identities, and anchors; chromosome v2 and gene-feature renders. |
| M10 | Polish phenotypes | Shape and color classes, proportions/counts, generic flower identity, and seed-cross content preserved in renders. |
| M11 | Harmonize diagram, text, and icon compositions | Consistent type, spacing and hierarchy across placement, annotation, curve, icon, text, import, and trial compositions. |
| M12 | Harmonize plots | Exact data and labels with coordinated typography and clear flat marks; inspect all plot examples and genome pilot. |
| M13 | Regenerate the complete durable artifact set | 17 gallery SVG/WebP pairs plus index, chromosome v2, 6 toolkit pilots, 2 trials; reproducible recipe/hash evidence and individual visual review. |
| M14 | Verify, review, document, and clean | Focused tests, 31 native proof pages plus chromosome page, fresh specification then quality then integration review, complete docs/report, protected-source checks, and scoped cleanup. |

## Dependencies and ownership

M1 precedes family polish. M2 can proceed during guide work. M3 establishes shared mechanics
before M4-M10 integrate them. M11 and M12 can proceed with the early visual contract, then
check against the completed guide. M13 follows family completion and coordinated examples.
M14 follows regeneration; its fresh reviews run in order: specification, quality, integration.
Fix discovered failures and recheck affected artifacts before the next acceptance step.

The manager assigns fresh bounded implementation and review tasks, identifies exclusive file
ownership, and resolves cross-file handoffs. Each implementation owner checks callers and
provides the smallest meaningful regression check for changed nontrivial behavior. Prefer
existing helpers and installed dependencies. Add no settings, generalized style engine, or
new package without a demonstrated requirement from this scope.

## Verification and finish

Use the focused SVG test lane from the repository instructions:

```sh
PYTHONPATH="$PWD:$PWD/tests" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest <selected_svg_test_paths>
```

Select the actual affected test files after implementation. Test API behavior, scientific
invariants, state restoration, bounds, and important regressions. Do not freeze decorative
path strings or exact output bytes as permanent style assertions. Use hashes for provenance,
regeneration consistency, protected sources, and ODP-embedded current SVG verification.

Inspect all 17 gallery pages individually and as a family, the chromosome example, all six
pilots, and both trial compositions. Review the rebuilt native proof set: 17 showcase pages,
12 pilot-use pages, and 2 trials (31 pages), plus the chromosome page. Confirm exact current
SVG embedding, live native slide titles/captions, extractable text, installed-font behavior,
clipping, scale, color meaning, contact topology, and biological fidelity. Keep independent
fresh acceptance records separate from implementation notes.

The final report states what changed, how it was verified, which claims are schematic, and
any remaining limits. Aesthetics need rendered inspection; compilation and focused tests
alone do not close a milestone. Clean only owned temporary artifacts after final acceptance
and durable evidence preservation. Preserve baseline evidence until comparison is finished.
