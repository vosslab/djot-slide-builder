# Sister chromatid survey

Reviewed C01-C68 in the chromosome review prototype on November 16, 2026. C16 is the
reference for clear, elongated sister chromatids, smooth shoulders, and a common foreground
centromere belt. Its artwork stays unchanged. Different chromosome types retain their lengths;
genuinely short chromosomes and acrocentric short arms are intentional.

The survey uses rendered SVGs and source metadata to distinguish sister chromatids from
homologs, individual crossover strands, and separated products. Connecting every nearby rod
would misrepresent several figures.

## Changes

- C17: replace the squat mitotic metaphase crosses with longer paired chromatids. All 90
  chromatids now retain their 76-, 58-, or 40-unit length class at a 6-unit width throughout
  the sequence. Rotate the mitotic metaphase pairs to fit the plate, regroup the parent rods,
  and use smooth cubic shoulders. Retain chromosome counts and recombination colors.
- C37: give independent ploidy copies and their separate belts visible spacing.
- C18 follow-up: center collars on their curved chromosome paths using the model's
  segment-boundary anchors; remove the older manual-coordinate override.
- C56-C58: join confirmed sisters in the pairing stage with two foreground belts. Preserve
  the separate centromeres on anaphase products, including the dicentric bridge.
- C59: connect the normal sister pair and the inverted sister pair with separate belts.
- C67: assemble 18 sister chromatids as nine pairs with common foreground belts.

## Figure coverage

| Figures | Assessment and action |
| --- | --- |
| C01-C03 | Individual chromosome transfer/fusion diagrams; no sister change. |
| C04 | Empirical karyotype reference; preserve the image. |
| C05-C07 | Single chromosome regions, gamete rods, or unreplicated chromosome; no sister change. |
| C08-C09 | Clear paired chromatids and belts; keep the recent replication-length correction. |
| C10 | Separated anaphase/telophase products; keep individual centromeres. |
| C11-C12 | Simplified prophase/chiasma strands; retain their pairing conventions. |
| C13 | Clear replicated and recombinant states; retain. |
| C14 | Simplified meiosis strands and cell sequence; retain. |
| C15-C16 | Good compact paired forms; preserve C16 as the reference. |
| C17 | Correct short pairs, stage-to-stage length drift, and crowded metaphase layout. |
| C18 | Preserve curved rods and short chromosome 4; center collars on their boundary anchors. |
| C19-C24 | Single rods, gene tracks, evidence, or crossover strands; retain the depicted connections. |
| C25 | Clear recombination pairs; retain. |
| C26 | Individual chromatids and daughter states; retain. |
| C27-C29 | Clear paired chromatids, crossover strands, and centromere connections; retain. |
| C30 | Karyotype preparation and reference context; retain. |
| C31-C36 | Good sister/banding/morphology examples; preserve unequal arms and fusion anatomy. |
| C37 | Separate ploidy-copy belts so independent chromosomes do not look joined. |
| C38 | Small paired chromosomes remain clear within the cell sequence; retain. |
| C39 | Parallel sisters and cohesin rings are the teaching target; preserve them. |
| C40 | Chromosome-set copies; retain independent chromosomes. |
| C41-C43 | Clear replicated chromosomes in meiotic/polyploid contexts; retain. |
| C44-C46 | Active/inactive X states and X/Y rods; no sister change. |
| C47-C52 | Single chromosome alterations, homolog pairing, or evidence maps; retain. |
| C53 | Clear matched sisters during unequal crossing over; retain. |
| C54 | Individual chromosome/gene-copy context; retain. |
| C55 | Two homologs, explicitly not four chromatids; keep their centromeres separate. |
| C56 | Two belts in Stage A; preserve the four separate centromeres in Stage B. |
| C57 | Two belts across the confirmed sister pairs; preserve the inversion loops. |
| C58 | Two belts in Stage A; preserve the four separate centromeres in Stage B. |
| C59 | Two belts across the two confirmed sister pairs; preserve gene order and crossovers. |
| C60-C61 | Individual position-effect/translocation chromosomes; retain. |
| C62 | Clear paired chromosomes, belts, and spindle orientation; retain. |
| C63-C66 | Gamete products or individual chromosome strips; retain. |
| C67 | Nine shared belts across 18 chromatids; preserve all segregation configurations. |
| C68 | Unreplicated gamete chromosomes; retain. |

## Validation

The final native PDF/ODP review and focused checks are recorded in
[chromosome_review_verification.json](chromosome_review_verification.json). Generated artwork
changes are confined to the prototype. Full repository tests are not part of this figure review.
