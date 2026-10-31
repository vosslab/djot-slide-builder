# Mitotic crossover teaching additions

Five additions expand 09C from seven to twelve slides. The core connection is loss of
heterozygosity (LOH): chromosome number can stay unchanged while allele combinations change.
This connects the existing fly twin spots to somatic mosaics, recessive alleles, and gene function.

## Evidence and teaching choices

All biological additions use primary research; the new drawings are original conceptual diagrams.

| Added Page | Teaching Point | Primary Evidence |
| --- | --- | --- |
| 4 | Sister-template repair often finishes without an exchange. | [Johnson and Jasin (2000)](https://pmc.ncbi.nlm.nih.gov/articles/PMC313931/) distinguish repair from crossover outcomes in mammalian cells. |
| 5 | A crossover and suitable segregation can produce homozygous daughter loci while retaining two chromosome copies. | [Hagstrom and Dryja (1999)](https://pubmed.ncbi.nlm.nih.gov/10077618/) identify regional somatic homozygosity compatible with recombination. The retained lecture diagram shows both segregation outcomes. |
| 8 | Cell descendants form patches; developmental timing affects clone size. | [Graf (1995)](https://pubmed.ncbi.nlm.nih.gov/7875256/) measures timing-dependent spot sizes in flies. Growth and survival also affect size. |
| 9 | LOH can expose an existing tumor-suppressor mutation. | [Cavenee et al. (1983)](https://pubmed.ncbi.nlm.nih.gov/6633649/) link retinoblastoma genotypes to chromosomal mechanisms that remove heterozygosity. |
| 10 | Paired labels let researchers compare cell lineages. | [Griffin et al. (2009)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2720837/) demonstrate twin-spot labeling and its use in observing cell behavior. |

The research-to-classroom choices are instructional judgments: use familiar A/a notation,
introduce one meaning per slide, retain the fly phenotype images, then extend the same idea
to an RB1 example and an experimental question. Cancer is a possible consequence at a relevant
locus; the slides do not equate all recombination with cancer.

## Clarifications to the original introduction

- Explain repair in cycling cells before the next mitosis, rather than locating all exchange
  in mitotic chromosome segregation itself.
- Replace the universal "no more than once per million divisions" bound with a qualitative
  uncommon-crossover description. Experimental rates depend on substrate, organism, and damage;
  the primary repair study does not support that universal ceiling.
- Define LOH as an allelic-state change. The pictured outcome is copy-neutral, but LOH can
  also result from other mechanisms. The existing alternative-segregation figure remains.
- Define retinoblastoma briefly as a retinal cancer. Keep the R/r to r/r model at the cellular
  level; it illustrates a second hit without requiring a new point mutation at that locus.

## Figures and reproducibility

The authoritative figures and source ledger live in
[assets/lect09c-mitotic_crossover/](assets/lect09c-mitotic_crossover/):

- `repair_templates.svg`: damaged chromatid, sister copy, and homolog; dashed arrow means
  template use, not physical exchange.
- `loh_outcome.svg`: pre-replication starting cell and postmitotic diploid daughters. The
  replicated intermediate is omitted; the outcome assumes a crossover between the centromere
  and marker, followed by LOH-producing segregation. Proximal origins remain reciprocal.
- `clonal_patches.svg`: two lineages within a heterozygous background. Cell counts, positions,
  and scale are schematic; these are not experimental measurements.
- [research_sources.json](assets/lect09c-mitotic_crossover/research_sources.json): sources,
  scientific simplifications, color roles, dimensions, and slide titles.

SVGs have live text and native geometry with internal markers and unique IDs. They load as
ordinary Djot image blocks; titles, prose, tables, and DOI citations remain native. A narrow
ignore exception keeps these authored SVG source files versionable. Drawing references were
the SVG skill corpus's biological-illustration *Clarity* passage and *Mastering SVG*'s
viewBox/viewport passage. Ordinary builds need no browser, generator, or network access.

## Verification

Strict native lint, the existing focused 09C cover test, SVG structure checks, and unchanged
other-deck checks pass. The source, ODP, and PDF have twelve visible slides, with no replacement
markers. The typography audit has no findings and the capacity report has no concerns.
All twelve exported pages and the new diagrams were inspected; DOI links are clickable.
Review evidence and one-time scripts are in `_temp/mitotic_expansion/`.
Physical projection, classroom pacing, and Impress playback remain untested.
