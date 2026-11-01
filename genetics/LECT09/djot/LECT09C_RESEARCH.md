# Mitotic crossover story and sources

The current 13-slide deck starts from the instructor's story: crossing over between linked
genes can also happen in a body cell, and twin spots make the result visible. The five researched
additions remain, with repair near the end. Explain the cell and patch first; name the genotype
change afterward. This order is a teaching choice, not a new biological claim.

## Current sequence

| Page | Teaching Step |
| --- | --- |
| 1-3 | Cover, objectives, and Beyond Meiosis section. |
| 4 | Connect linked-gene crossing over to an uncommon, naturally occurring exchange in a body cell. |
| 5 | Retain the original chromosome figure and both ways the chromosomes can separate. |
| 6 | Retain the original yellow/singed fly patches and their parental genotype. |
| 7 | Follow the daughter cells into patches; define clone and mosaic in that setting. |
| 8 | Show A/a becoming A/A and a/a in one separation pattern; then name loss of heterozygosity. |
| 9-10 | Extend the same idea to an existing RB1 allele and marked-cell experiments. |
| 11 | Explain one route to an exchange: repair using matching DNA. |
| 12-13 | Summarize the twin-spot story and close. |

## Natural events and DNA repair

Mitotic crossing over can occur spontaneously. "Spontaneous" does not mean that DNA stays
unbroken, or that repair is absent. DNA breaks and copying problems can arise during ordinary
cell activity. Repair using a matching chromosome can sometimes produce an exchange. The slides
explain this route without claiming that an experimental treatment is required, or that every
natural event has the same initiating lesion.

- [Lee et al. (2009)](https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1000410)
  directly measure spontaneous exchanges between homologs in dividing yeast cells. This supports
  the natural-event introduction and the two possible chromosome-separation outcomes.
- [Saleh-Gohari et al. (2005)](https://pubmed.ncbi.nlm.nih.gov/16055725/) provide evidence for
  breaks arising within cells and problems during DNA copying as sources of spontaneous
  recombination. Their assay concerns repair generally; it does not establish that every event
  is a homolog-to-homolog crossover.
- [Johnson and Jasin (2000)](https://pmc.ncbi.nlm.nih.gov/articles/PMC313931/) support matching-copy
  repair using sisters and frequent repair without an exchange. Using a copy to guide repair
  and physically exchanging chromosome segments are different outcomes.
- [Keeney et al. (1997)](https://pubmed.ncbi.nlm.nih.gov/9039264/) identify the protein that starts
  meiotic recombination by cutting DNA. Controlled breaks also occur in normal meiosis. This is
  instructor background in notes; the deck does not add a repair-pathway lesson.

## Evidence and teaching choices

All biological additions use primary research; the new drawings are original conceptual diagrams.

| Current Page | Teaching Point | Primary Evidence |
| --- | --- | --- |
| 7 | Cell descendants form patches; developmental timing affects clone size. | [Graf (1995)](https://pubmed.ncbi.nlm.nih.gov/7875256/) measures timing-dependent spot sizes in flies. Growth and survival also affect size. |
| 8 | A crossover and suitable segregation can produce homozygous daughter loci while retaining two chromosome copies. | [Hagstrom and Dryja (1999)](https://pubmed.ncbi.nlm.nih.gov/10077618/) identify regional somatic homozygosity compatible with recombination. The retained lecture diagram shows both segregation outcomes. |
| 9 | LOH can expose an existing tumor-suppressor mutation. | [Cavenee et al. (1983)](https://pubmed.ncbi.nlm.nih.gov/6633649/) link retinoblastoma genotypes to chromosomal mechanisms that remove heterozygosity. |
| 10 | Paired labels let researchers compare cell lineages. | [Griffin et al. (2009)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2720837/) demonstrate twin-spot labeling and its use in observing cell behavior. |
| 11 | Sister-template repair often finishes without an exchange. | [Johnson and Jasin (2000)](https://pmc.ncbi.nlm.nih.gov/articles/PMC313931/) distinguish repair from crossover outcomes in mammalian cells. |

The research-to-classroom choices are instructional judgments: use familiar A/a notation,
retain the twin-spot story, then extend it to an RB1 example and an experimental question.
Cancer is a possible consequence at a relevant locus; the slides do not equate all recombination
with cancer. The original research heading, LOH Can Supply a Second Hit, is now the concrete
An Existing Allele Can Matter. The R/r, r/r, R/R table and all working-copy counts remain.

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

- `repair_templates.drawn.svg`: damaged chromatid, sister copy, and homolog; dashed arrow means
  template use, not physical exchange.
- `loh_outcome.drawn.svg`: pre-replication starting cell and postmitotic diploid daughters. The
  replicated intermediate is omitted; the outcome assumes a crossover between the centromere
  and marker, followed by LOH-producing segregation. Proximal origins remain reciprocal.
- `clonal_patches.drawn.svg`: two lineages within a heterozygous background. Cell counts, positions,
  and scale are schematic; these are not experimental measurements.
- [research_sources.json](assets/lect09c-mitotic_crossover/research_sources.json): sources,
  scientific simplifications, color roles, dimensions, and slide titles.

SVGs have live text and native geometry with internal markers and unique IDs. They load as
ordinary Djot image blocks; titles, prose, tables, and DOI citations remain native. The reviewed
drawings use the `.drawn.svg` suffix. Drawing references were
the SVG skill corpus's biological-illustration *Clarity* passage and *Mastering SVG*'s
viewBox/viewport passage. Ordinary builds need no browser, generator, or network access.

## Verification

The earlier seven-to-twelve-slide expansion was reviewed in `_temp/mitotic_expansion/`; the
section revision then brought C to 13 pages. Current story-revision evidence is in
`_temp/mitotic_story/`. Verification below is updated after the revised 13-page export is checked.
