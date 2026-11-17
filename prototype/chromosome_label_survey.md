# Chromosome labels and bands

The November 17 survey uses C53's embedded gene blocks and C01/C47's internal
gene-order labels as references. The revised artwork remains in the review prototype.
Original lecture artwork is preserved.

The official convention and shared rendering pipeline are in
[CHROMOSOME_GENE_LABELS.md](../docs/CHROMOSOME_GENE_LABELS.md).

## Shared construction

- A labeled `Segment` represents a colored region of chromosome material. Short gene
  intervals have unlabeled material between them; their positions need not be evenly spaced.
- Internal labels stay upright, with contrasting ink and no white outline halo.
- Source-coordinate loci project onto their explicitly assigned chromosome centerline
  using shared arc-length geometry. A crossing does not change which chromatid owns a locus.
- External labels remain useful for small chromosomes, dense diagrams, whole-chromosome
  numbers, arm names, genotype summaries and magnification callouts.
- `texture` controls BPQ's faint decorative stripes. Explicit region colors separately
  represent genes, chromosome ancestry, heterochromatin or cytogenetic staining.
  Turning texture off preserves these regions and the chromosome's depth layers.

## Figure decisions

| Figures | Treatment |
| --- | --- |
| C01, C47 | Retain internal schematic gene-order labels; shared contrast replaces C01's local outline removal. |
| C03/C36 | Preserve the identical irregular fusion-material colors and chromosome lengths. |
| C04 | Preserve the empirical karyotype reference. |
| C18 | Preserve chromosome/arm callouts and distinct heterochromatin colors. |
| C20 | Retain existing embedded gold loci. |
| C22 | Embed both alleles in gold regions; preserve parental/recombinant identities and centromere locations. |
| C24 | Attach the six allele blocks directly to their thin recombination traces; retain interval labels and exchange numbers. |
| C25 | Show separate A/a and B/b gene regions, both distal to the exchange; their positions are schematic. Keep cell-genotype summaries outside and explanatory prose native. |
| C26 | Embed each A/a at its source distal locus; keep cell-genotype summaries outside. |
| C27 | Retain external letters in the dense repair-template composition. |
| C28 | Embed eight locus labels along their chromatids; distal alleles follow exchanged ancestry and match the named products. |
| C31 | Preserve the specific G-, R- and C-staining patterns without decorative texture. |
| C48 | Embed A/B/Y/Z along each initial, folded and ring path; keep ellipses as sequence shorthand and purple/blue repeats distinct. |
| C53 | Preserve the reference repeat blocks and unequal-crossing-over construction. |
| C54 | Preserve molecular opsin gene tracks and their magnification callout. |
| C56-C59 | Use the shared locus adapter for gold regions and measured labels swept inside assigned rods/curves; preserve all alleles and source order. |
| C60 | Embed `w+` at both source positions, separate from heterochromatin and the inversion breakpoints. |
| C63 | Build embedded `rb+`, `dp+` and `dp` gene regions in reusable components; retain ancestry colors and chromosome identifiers. Keep the overview plus two enlarged detail views for readable gene names. |
| C65 | Retain chromosome-number labels as chromosome identifiers. |

The numerical positions in the recipes remain schematic unless their source explicitly
provides measured intervals. A colored gene patch does not establish a gene's physical size.

Inspect the local `output/pdf/chromosome_review.pdf` native slide export for the current
rendered figures. The earlier [chromosome_review_verification.json](chromosome_review_verification.json)
records the original replacement audit, preceding the subsequent labeling revisions.
