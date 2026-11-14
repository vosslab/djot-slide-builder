# SVG toolkit biology quality

What this change does: M12 demonstrates independent protein activity and phosphorylation.
M16 composes directional gene features and matching genomic and joined exon tracks. M20 replaces
the genome-composition illustration while preserving the supplied categories and values.

This fresh quality review follows the approved
[svg_toolkit_plan.md](../active/svg_toolkit_plan.md). Production files were read only.
The expected use is an authored teaching illustration, not an inferred biological pathway or model.

| Milestone | Quality verdict | Required corrections |
| --- | --- | --- |
| M12 signaling states | PASS | None |
| M16 gene features | PASS | None |
| M20 genome-composition pilot | PASS | None |

## Scientific and visual evidence

- **M12:** Viewed `_temp/svg_toolkit/signaling/signaling.webp` at 900 by 595 pixels and read
  [signaling.py](../../../svg_tools/signaling.py), its
  [example](../../../svg_tools/examples/signaling.py), and focused state tests. The receptor
  crosses the membrane opening. The active kinase inhibits the upper inactive response protein
  and activates the lower active response protein; arrowheads, inhibition bar, and branch labels
  agree. The independent phosphorylated kinase is spatially separate and unconnected. Its P badge
  visibly overlaps its own molecular outline, with `site A` adjacent. Activity has its own symbol
  and explicit word, so phosphorylation does not substitute for activity. This is a valid generic
  demonstration; the drawing does not establish a named pathway or a specific phosphosite mechanism.
  The ligand is shown above the receptor with a visible gap, so it reads as a separate nearby ligand,
  not as proof of a bound complex. Labels, connectors, and membrane tails remain distinguishable;
  no clipping or label collisions are visible.
- **M16:** Rendered `_temp/gene_features.svg` onto white and inspected
  `_temp/svg_toolkit/biology_quality/gene_features.webp` at 1020 by 570 pixels. Read
  [gene_tracks.py](../../../svg_tools/gene_tracks.py) and the
  [example](../../../svg_tools/examples/gene_features.py). Promoter, operator, genes A/B/C, and
  terminator appear in the authored order. The three gene tips and promoter arrow point right;
  the separate reverse gene points left. Genomic and joined tracks both retain exon lengths
  90/120/75, colors, order, and labels; only intron lengths change from 60/90 to 0/0. The joined
  row is appropriately shorter. The unlabeled intron spans are visually thin and distinct from
  exon blocks. All labels fit. The operon and exon tracks are separate schematic examples; the
  figure makes no explicit claim that these introns belong to the illustrated bacterial operon.
- **M20:** Viewed `_temp/svg_toolkit/genome_pilot.webp` at 700 by 700 pixels and read the
  [generator](../../../svg_tools/examples/genome_composition.py), current Djot source, and
  [svg_toolkit_pilot_baseline.json](svg_toolkit_pilot_baseline.json). All six category labels and
  the source values 1.5, 5, about 20, 15, 44, and 14 percent remain. Bar endpoints use the raw
  values, not a normalized total. The horizontal scale retains 0%, 10%, 20%, 30%, 40%, and 50%.
  The wrapped transposable-element category and end labels fit without collisions. Horizontal
  bars are an appropriate comparison for approximate source percentages that need not sum to
  exactly 100. Inverse replacement of the single new image filename reproduces the baseline
  Djot SHA-256, confirming surrounding source preservation.

## Shared family guidance

These examples share flat fills, dark blue-gray outlines and labels, Atkinson text, and restrained
color. Rounded molecular shapes and small attached badges work together. Keep rectangular exon
blocks and quantitative bars geometrically faithful; rounding every object is unnecessary.

- Use a stable fill for the same entity across states; give activity its own readable word and
  symbol. Keep modification badges attached to the relevant molecule, with their labels clear.
- Keep arrowheads and inhibition bars separated from labels and visually associated with the
  intended source and target. Physical binding diagrams need visible contact at their stated
  attachment points; a regulatory arrow alone does not establish a molecular contact.
- Preserve scientific counts, orientation, lengths, and raw values before adjusting spacing.
  Cell, antibody, and phenotype examples should inherit the flat fill, outline, and text family
  without sacrificing distinctive silhouettes or adding decorative marks that imply biology.

Optional presentation polish: if the M12 gallery entry describes ligand binding, either describe
the ligand as nearby or dock it at the receptor anchor. If the M16 examples are taught together,
short captions identifying the operon and exon-splicing examples would remove any possible
cross-example association. Neither change is required for the current generic demonstration.

## Verification and limits

Fresh focused check: `PYTHONPATH="$PWD:$PWD/tests" /opt/homebrew/bin/python3.12 -B -m pytest
--noconftest tests/test_svg_signaling.py tests/test_svg_gene_features.py tests/test_svg_plots.py`
completed with **7 passed**. A separate assert check confirmed the six raw values, display strings,
and inverse Djot hash. M16 was rendered with `PANGOCAIRO_BACKEND=fc rsvg-convert` and flattened to
white WebP with Pillow at quality 90. M12 and M20 used the supplied current rendered proofs.

Verdict: Ship these milestones to the next integration stage.

Not checked: native ODP/PDF export, the full suite, or a named biological pathway; native proof
exports remain assigned to M25. The small `site A` annotation should be rechecked at its final
slide placement size.
