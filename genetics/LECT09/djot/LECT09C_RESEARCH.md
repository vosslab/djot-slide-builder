# Mitotic crossover story and sources

The current 19-slide deck starts from the instructor's story: crossing over between linked
genes can also happen in a body cell, and twin spots make the result visible. The five researched
additions remain, with repair near the end. Explain the cell and patch first; name the genotype
change afterward. This order is a teaching choice, not a new biological claim.

## Current sequence

| Page | Teaching Step |
| --- | --- |
| 1-4 | Cover, objectives, Beyond Meiosis section, and the naturally occurring body-cell exchange. |
| 5 | Subsection: How Twin Spots Form. |
| 6-7 | Retain the chromosome diagram, both segregation outcomes, and the yellow/singed fly patches. |
| 8-9 | Predict daughter genotypes and yellow/singed patches, then work through the answer. |
| 10 | Follow daughter cells into patches; define clone and mosaic. |
| 11 | Section: What Changes in the Cell? |
| 12-13 | Name loss of heterozygosity, then follow the existing RB1 allele into the cancer example. |
| 14-15 | Following Cell Growth divider and the marked-cell experiment. |
| 16-17 | How Exchanges Start divider and the brief repair explanation. |
| 18-19 | Summarize the twin-spot story and close. |

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

The five background additions use primary research; the drawings are original conceptual diagrams.
The prediction problem applies the existing fly model with original classroom wording.

| Current Page | Teaching Point | Primary Evidence |
| --- | --- | --- |
| 10 | Cell descendants form patches; developmental timing affects clone size. | [Graf (1995)](https://pubmed.ncbi.nlm.nih.gov/7875256/) measures timing-dependent spot sizes in flies. Growth and survival also affect size. |
| 12 | A crossover and suitable segregation can produce homozygous daughter loci while retaining two chromosome copies. | [Hagstrom and Dryja (1999)](https://pubmed.ncbi.nlm.nih.gov/10077618/) identify regional somatic homozygosity compatible with recombination. The retained lecture diagram shows both segregation outcomes. |
| 13 | LOH can expose an existing tumor-suppressor mutation. | [Cavenee et al. (1983)](https://pubmed.ncbi.nlm.nih.gov/6633649/) link retinoblastoma genotypes to chromosomal mechanisms that remove heterozygosity. |
| 15 | Paired labels let researchers compare cell lineages. | [Griffin et al. (2009)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2720837/) demonstrate twin-spot labeling and its use in observing cell behavior. |
| 17 | Sister-template repair often finishes without an exchange. | [Johnson and Jasin (2000)](https://pmc.ncbi.nlm.nih.gov/articles/PMC313931/) distinguish repair from crossover outcomes in mammalian cells. |

The research-to-classroom choices are instructional judgments: use familiar A/a notation,
retain the twin-spot story, then extend it to an RB1 example and an experimental question.
Cancer is a possible consequence at a relevant locus; the slides do not equate all recombination
with cancer. The original research heading, LOH Can Supply a Second Hit, is now the concrete
A Cancer Example. The R/r, r/r, R/R table and all working-copy counts remain.

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

## Twin-spot homework ideas

The strongest direct textbook exercise is Brooker's linked-marker twin-spot problem. The
integrated text supplies a useful extension about the location of the exchange. These are
research notes and an original classroom problem, now taught on C8-9 after the two original
twin-spot figures. C8 gives the starting genotype and exchange/separation assumptions; C9
matches the two daughter genotypes to their patches and explains why neither mutation nor
chromosome loss is needed. The existing 17 slides remain intact and in order.

Local books below are under `~/nsh/MARKDOWN_BOOKS/inheritance_genetics/`. Line numbers locate
the Markdown conversion; they are not printed page numbers.

| Source | Location | Fit for this lecture |
| --- | --- | --- |
| `Genetics_Analysis_and_Principles-Brooker-2012.md` | Chapter 6, conceptual question C4; line 1301. | Best starting point: linked fur-color and hair-length markers in opposite combinations; follow an exchange into two different patches. |
| `Concepts_of_Genetics-Brooker-2012.md` | Chapter 7, conceptual question C15; line 1842. | The same exercise, rather than an independent second problem. |
| `Genetic_Analysis_An_Integrated_Approach-2015.md` | Section 5.8 and Figure 5.25 discussion; lines 3146-3148. | A harder extension: relate crossover location to twin spots or a single visible mutant patch. |
| `Genetics_Principles_and_Analysis_Hartl_Jones-1998.md` | Section 4.6; lines 5826-5843. | Clear background on the two chromosome-separation outcomes and descendant cell patches. |
| `A_Dictionary_of_Genetics_King_Stansfield_Mulligan-2006.md` | Entries for mitotic recombination, somatic crossing over, and twin spots. | Definitions and terminology, rather than a worked homework problem. |

### Implemented prediction problem

Use the fly markers already taught in 09C, with original wording and separate short tasks.
Brooker's exercise supplies the teaching idea; the following records the classroom model.

A female fly has the chromosome combinations `y sn+ / y+ sn`. The recessive `y` allele gives
yellow body color; the recessive `sn` allele gives singed bristles. The normal alleles are
`y+` and `sn+`. Along each X chromosome the order is `centromere -- sn -- y`.

DNA has been copied. One crossover occurs between the centromere and `sn` in a body cell.
Assume normal mitosis: both daughters keep two X chromosomes. The two exchanged chromatids
go to opposite daughter cells. Each daughter then produces a patch of descendants.

1. Predict the two patches. Choose two: yellow with normal bristles, normal body color with
   singed bristles, yellow with singed bristles, or normal for both traits.
2. Match each predicted patch to its genotype: `y sn+ / y sn+`, `y+ sn / y+ sn`, or the
   original heterozygous combination.
3. Did either recessive allele first appear during this event? Did a daughter lose an X?

Answer key:

- Yellow/normal-bristled patch: `y sn+ / y sn+`. Normal-color/singed patch: `y+ sn / y+ sn`.
- Both recessive alleles were already present. Each daughter retains two X chromosomes.
- Most surrounding tissue has normal body color and normal bristles: each normal allele
  covers its corresponding recessive allele.

The slides use a short prediction prompt and a native answer table. They specify an exchange
between the centromere and both genes; the exact order of the two genes is unnecessary for
this prediction. The more detailed order above is retained for the optional extensions below.
No textbook figure or question text is added. No generator is implemented in this revision.
The distinction between opposite-pole and same-pole recombinant segregation is also described
in [Griffin et al. (2009), Figure 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC2720837/).

### Useful extensions

- **Change chromosome separation.** If both exchanged chromatids go to the same daughter,
  both daughters remain heterozygous at these markers and show the normal phenotype. A crossover
  need not be visibly detectable. Keep this as a follow-up to the simple prediction.
- **Move the exchange.** For the same `centromere -- sn -- y` order and starting genotype,
  put one exchange between `sn` and `y`. Ask which locus can become homozygous. One separation
  pattern makes a yellow patch beside phenotypically normal tissue; `sn` remains heterozygous.
  This is the best follow-up to the first problem.
- **Change the starting combinations.** Compare `Ab / aB` with `AB / ab`, explicitly stating
  complete dominance and an exchange between the centromere and both genes. The first can
  yield `AAbb` and `aaBB`; the second can yield `AABB` and `aabb`. Students must read the
  starting chromosomes rather than memorize that every exchange gives two different mutant traits.
- **Compare clone growth.** Supply a small, explicitly invented dataset of marked sister
  patches, such as 8 versus 32 cells. Ask whether the snapshot alone distinguishes fewer
  divisions from more cell death. It does not; ask for an additional observation that could.
  This is an interpretation exercise, not a measured result from a paper. Paired labeling
  for lineage and cell-behavior analysis is supported by
  [Griffin et al. (2009)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2720837/).

### Source qualifications

Brooker's neighboring eye-color question uses a one-locus brown/blue model. It is a weaker
choice here: use the fly markers or an explicitly hypothetical animal instead. Figure 5.25's
single-singed route introduces double crossovers and extra assumptions; reserve it as a challenge
after the basic diagram is understood. A lone visible spot does not by itself prove that route:
the other clone may not grow, survive, or be detected.

Do not turn the integrated text's 21/45 cM comparison into a general spot-count-to-distance
formula. Hartl and Jones Section 4.6 explicitly notes that mitotic and meiotic interval
frequencies can differ. Spot visibility and subsequent growth add further conditions.
Keep the first homework focused on allele combinations, crossover position, segregation,
and patches. The dictionary hits are useful definitions, not enough to construct the exercise.

## Current problem verification

Add the prediction and worked answer at C8-9, preserving all 17 preceding source slides
and their PDF text after page shifts. Source, ODP, and PDF agree on 19 visible pages. All
other Lecture 09 Djot sources and artwork remain byte-identical. Strict native lint,
capacity, and typography checks are clean. The two new pages and their surrounding transition
were visually inspected; the answer remains a native editable table with real allele superscripts.
A small chromatid model confirms the two daughter genotypes and the alternative heterozygous
separation outcome. Eight PDFKit point selections pass, including both daughter genotypes
and patch phenotypes. Selection points bracket whole text lines; points on a glyph boundary
can select a neighboring line and are not a reliable test of an obstruction. No renderer changes
or permanent content-specific tests are needed. No classroom playback or full-suite run was performed.
Evidence is in `_temp/09c_twin_spot_problem/`.

## Earlier divider verification

Add dividers at C5, C9, C12, and C14. Keep all 13 preceding slides in order, producing 17
pages with two sections and three subsections. Source-block identity, unchanged artwork
and other Djot sources, matching original PDF text after page shifts, strict native lint,
capacity, and typography checks pass. All 17 rendered pages were inspected; all four new headings
fit one line, and their native PDFKit text selections match. The existing decoration regression
passes all 14 cases. A small chromatid model confirms the draft's two patch genotypes and the
alternative heterozygous separation outcome. No classroom playback or full-suite run was performed.
Evidence is in `_temp/09c_sections_homework/`; the page numbers describe that 17-page revision.

## Earlier story-revision verification

The earlier seven-to-twelve-slide expansion was reviewed in `_temp/mitotic_expansion/`; the
section revision then brought C to 13 pages. Current story-revision evidence is in
`_temp/mitotic_story/`.

- [x] Preserve all 13 slides, all six figure uses, the original fly genotype, both chromosome
  separation outcomes, clone/mosaic meanings, the RB1 working-copy counts, and the experiments.
- [x] Preserve every artwork file and every other Djot source. Update only 09C's prose/order
  and its source ledger, plus the review, page map, catalog, and guidance documents.
- [x] Pass strict native lint, a clean capacity check, and zero typography-audit findings.
- [x] Build ODP/PDF through the repository CLI with LibreOffice outside the sandbox. Both
  exports have 13 pages, all six clickable citations, and the final teaching notes.
- [x] Compare every figure's proportions with its preceding export; preserve ratios within
  0.3% PDF rounding tolerance. No figures are stretched or redrawn.
- [x] Review all 13 rendered pages; inspect the genotype, cancer, and repair slides at full
  size after the final wording changes. Figures, text, tables, and titles remain readable.

No permanent tests or renderer changes. The full unrelated test suite, classroom pacing,
physical projection, and Impress playback are untested.
