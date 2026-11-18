# Chromosome review provenance

The original figure inventory dates to November 16, 2026. Source slide numbers follow
the expanded ODP order, including hidden slides. The review decks display subsequent
prototype revisions where the replacement inventory lists them.

## Source records

[chromosome_samples.csv](chromosome_samples.csv) is the authoritative 68-record source map for
**C01-C68**. Its columns retain each review ID, review-slide number, title, family, original deck
and slide, source-definition path and line, original asset path, and SHA-256 snapshot hash.
[chromosome_replacements.csv](chromosome_replacements.csv) records all 70 replacement placements
in deck order, including the recipe and SHA-256 hash of each SVG. C03/C36 and C13/C21 share
artwork, so the inventory covers 68 distinct SVGs. C04 links directly to its original JPEG from
the source inventory. Each shared figure retains its own review caption and original citation.

## Multi-view review records

C55 has an overview and a loop view of the same Mini2 synapsis model based on LECT13B. C55 in
[chromosome_feedback.csv](chromosome_feedback.csv) applies to both views. C63 has a three-column
overview plus enlarged first-two-column and final-column views of the same Mini2 products
based on LECT13D. C63 in the feedback sheet applies to all three views. The feedback sheet's
`keep`, `change`, and `reason` fields replace the former on-slide review prompts.

## C18 scientific and visual references

- The whole-chromosome map shows broad euchromatic and heterochromatic regions, including
  the nearly entirely heterochromatic mitotic Y. The amount of X heterochromatin varies
  among fly stocks. [Adams et al., Figure 1](https://doi.org/10.1126/science.287.5461.2185)
- The Y has unequal arms, both carrying regions needed for male fertility.
  [Kennison, 1981](https://doi.org/10.1093/genetics/98.3.529)
- The XY panel uses a schematic metaphase I orientation. The X pairing region lies in
  proximal heterochromatin, and the Y pairing region lies near the centromere on its short
  arm. [Thomas and McKee, 2007](https://pmc.ncbi.nlm.nih.gov/articles/PMC2034643/)
  [Weber et al., 2020, Fig. S7](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1008928#pgen.1008928.s007)
- The pale centromere fills and bold chromosome IDs follow the BPQ question
  *Gametes from Balanced Translocation Segregation*. Its recipe is
  `translocation_meiosis_table.py`, and the BPW example is
  `site_docs/genetics/topic09/bbq-translocation_meiosis_table-questions.txt`.
