# Set 4 topic guide

Edit the chapter files; build the [master](lect06c-set_4_tp_chapter_12_16_material.djot) for one combined lecture.
The master lists the files in order and contains no duplicated slide content. Images remain in the
shared `assets/` directory. All 248 slides are visible.

```bash
source source_me.sh && python3 deck_tools.py build \
	biotech/LECT06/djot/lect06c-set_4_tp_chapter_12_16_material.djot --format all
```

## Chapter files

| Editable source | Slides | Combined PDF pages |
| --- | ---: | --- |
| [set4_opening.djot](set4_opening.djot) | 6 | 1-6 |
| [set4_chapter_12.djot](set4_chapter_12.djot) | 57 | 7-63 |
| [set4_chapter_13.djot](set4_chapter_13.djot) | 67 | 64-130 |
| [set4_chapter_14.djot](set4_chapter_14.djot) | 14 | 131-144 |
| [set4_chapter_15.djot](set4_chapter_15.djot) | 69 | 145-213 |
| [set4_chapter_16.djot](set4_chapter_16.djot) | 31 | 214-244 |
| [set4_summary.djot](set4_summary.djot) | 4 | 245-248 |

Chapter boundaries follow the 2026 deck: Brainbow (30) remains in Chapter 15; Chapter 16 starts
with GMO mosquitoes (31). Each topic starts with a numbered overview; supporting slides repeat its
number where the layout has a title.

## Source authority and voice

- [2026_topic_list.txt](../old/2026_topic_list.txt) controls all 33 numbers and topic labels.
- The annual 2021-2026 Talking Points Set 4 files in `../old/` provide questions and examples.
  The 2026 prompts determine coverage; earlier student explanations are teaching leads, not
  scientific authority. Rosters, empty submission pages, and duplicate assignment instructions
  are not copied into the science lecture.
- The original 121-slide material deck remains represented, including all 90 component-image
  references in the converted draft. Notes preserve original slide identifiers after regrouping.
- New explanations use direct questions, mechanisms, comparisons, and concrete experiments.
  Original instructor opinions remain attributed and marked for review where needed; no new
  personal position is invented for Dr. Voss. Explanations stay visible for later study.
- The expansion adds 114 topic slides plus chapter/overview/summary structure: 248 slides total,
  up from the 125-slide conversion. Primary papers and official sources below support bounded
  scientific updates; this is not an exhaustive literature or commercial-status review.

## Topic and source map

PDF pages refer to the combined deck. Original numbers refer to the 121-slide ODP; a dash means
the topic needed new coverage. Reading links also appear in the new slides' speaker notes.

| Topic | 2026 label | Chapter | PDF pages | Original slides | New topic slides | Reading |
| ---: | --- | ---: | --- | --- | ---: | --- |
| 1 | gene mining | [12](set4_chapter_12.djot) | 8-10 | - | 3 | [Source 1](https://www.genome.gov/news/news-release/nih-initiative-to-systematically-investigate-and-establish-function-of-every-human-gene) [Source 2](https://www.nature.com/articles/nmicrobiol201657) |
| 2 | microbe profiling | [12](set4_chapter_12.djot) | 11-20 | 5, 6, 7, 8, 9 | 5 | [Source 1](https://academic.oup.com/nar/article/35/21/7188/2376260) [Source 2](https://www.arb-silva.de/documentation/silva-taxonomy) [Source 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC4927377/) |
| 3 | culture enrichment | [12](set4_chapter_12.djot) | 21-25 | 3, 4 | 3 | [Source 1](https://www.nature.com/articles/35001054) |
| 4 | hydrocarbon rem. | [12](set4_chapter_12.djot) | 26-30 | 10, 11 | 3 | [Source 1](https://www.nature.com/articles/nmicrobiol201657) [Source 2](https://www.nature.com/articles/ismej201259) |
| 5 | chemical spill rem. | [12](set4_chapter_12.djot) | 31-33 | - | 3 | [Source 1](https://pubmed.ncbi.nlm.nih.gov/10388710/) [Source 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC1065153/) |
| 6 | pesticide rem. | [12](set4_chapter_12.djot) | 34-36 | - | 3 | [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC2737934/) |
| 7 | nuclear rem. | [12](set4_chapter_12.djot) | 37-39 | - | 3 | [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC3165427/) |
| 8 | heavy metal rem. | [12](set4_chapter_12.djot) | 40-43 | - | 4 | [Source 1](https://pubs.usgs.gov/publication/pp1885I) |
| 9 | forever chem. rem. | [12](set4_chapter_12.djot) | 44-47 | - | 4 | [Source 1](https://pubmed.ncbi.nlm.nih.gov/39018407/) |
| 10 | fuel cells | [12](set4_chapter_12.djot) | 48-52 | 12, 13 | 3 | [Source 1](https://www.energy.gov/cmei/fuels/fuel-cells) |
| 11 | greenhouse gas rem. | [12](set4_chapter_12.djot) | 53-56 | - | 4 | [Source 1](https://www.energy.gov/science/doe-explainsbiofuels) |
| 12 | plastic enzymes | [12](set4_chapter_12.djot) | 57-60 | - | 4 | [Source 1](https://doi.org/10.1073/pnas.2006753117) [Source 2](https://doi.org/10.1073/pnas.1718804115) |
| 13 | rare earth mining | [12](set4_chapter_12.djot) | 61-63 | - | 3 | [Source 1](https://www.nature.com/articles/s41586-023-05945-5) [Source 2](https://www.nature.com/articles/s41589-026-02176-3) |
| 14 | starch fuel | [13](set4_chapter_13.djot) | 65-75 | 14, 15, 16, 17, 18, 19, 20, 21 | 3 | [Source 1](https://afdc.energy.gov/fuels/ethanol-fuel-basics) [Source 2](https://afdc.energy.gov/fuels/ethanol-e85) |
| 15 | cellulose fuel | [13](set4_chapter_13.djot) | 76-92 | 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35 | 3 | [Source 1](https://pubmed.ncbi.nlm.nih.gov/20829451/) [Source 2](https://www.energy.gov/science/doe-explainsbiofuels) |
| 16 | biodiesel | [13](set4_chapter_13.djot) | 93-100 | 36, 37, 38, 39, 40 | 3 | [Source 1](https://afdc.energy.gov/fuels/biodiesel-production) [Source 2](https://afdc.energy.gov/fuels/biodiesel-blends) |
| 17 | algae diesel | [13](set4_chapter_13.djot) | 101-113 | 41, 42, 45, 46, 47, 48, 49, 50, 51, 52 | 3 | [Source 1](https://www.energy.gov/cmei/fuels/algal-logistics) [Source 2](https://www.energy.gov/cmei/fuels/articles/updated-algae-report-analyzes-national-scale-prospects-converting-microalgae) |
| 18 | xDNA/XNA | [13](set4_chapter_13.djot) | 114-118 | 53, 54 | 3 | [Source 1](https://doi.org/10.1126/science.1088334) [Source 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC3362463/) |
| 19 | artificial cells | [13](set4_chapter_13.djot) | 119-121 | - | 3 | [Source 1](https://www.maxsynbio.mpg.de) [Source 2](https://www.syntheticcell.eu) |
| 20 | synth. chloroplasts | [13](set4_chapter_13.djot) | 122-126 | 43, 44 | 3 | [Source 1](https://pmc.ncbi.nlm.nih.gov/articles/PMC7610767/) |
| 21 | minimal genome | [13](set4_chapter_13.djot) | 127-130 | 2 | 3 | [Source 1](https://www.jcvi.org/publications/design-and-synthesis-minimal-bacterial-genome) [Source 2](https://www.nist.gov/news-events/news/2021/03/scientists-develop-cell-synthetic-genome-grows-and-divides-normally) [Source 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC10396959/) |
| 22 | glucose meters | [14](set4_chapter_14.djot) | 132-137 | 55, 56, 57 | 3 | [Source 1](https://www.fda.gov/medical-devices/safety-communications/do-not-use-smartwatches-or-smart-rings-measure-blood-glucose-levels-fda-safety-communication) |
| 23 | other biosensors | [14](set4_chapter_14.djot) | 138-144 | 58, 59, 60 | 4 | [Source 1](https://www.fda.gov/medical-devices/digital-health-center-excellence/medical-devices-incorporate-sensor-based-digital-health-technology) |
| 24 | Agrobacterium | [15](set4_chapter_15.djot) | 146-151 | 64, 65, 66 | 3 | [Source 1](https://www.aphis.usda.gov/biotechnology) [Source 2](https://www.aphis.usda.gov/vacatur-2020-regulations) |
| 25 | gene guns | [15](set4_chapter_15.djot) | 152-155 | 67 | 3 | [Source 1](https://www.aphis.usda.gov/vacatur-2020-regulations) [Source 2](https://www.aphis.usda.gov/am-i-regulated) |
| 26 | plant transgenes | [15](set4_chapter_15.djot) | 156-166 | 61, 62, 63, 69, 70, 99, 100 | 4 | [Source 1](https://www.fda.gov/food/agricultural-biotechnology/gmo-crops-and-food-animals) |
| 27 | monocultures | [15](set4_chapter_15.djot) | 167-175 | 88, 89, 90, 91, 92 | 4 | [Source 1](https://www.nature.com/articles/s41467-017-01670-6) [Source 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC12392930/) |
| 28 | GMO plants + nature | [15](set4_chapter_15.djot) | 176-196 | 68, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 93, 94, 95, 96, 97, 98 | 4 | [Source 1](https://www.who.int/news-room/questions-and-answers/item/FAQ-genetically-modified-foods) [Source 2](https://www.fda.gov/food/food-new-plant-varieties/understanding-new-plant-varieties) |
| 29 | glyphosate | [15](set4_chapter_15.djot) | 197-207 | 71, 72, 73, 74, 75, 76, 77 | 4 | [Source 1](https://www.iarc.who.int/featured-news/media-centre-iarc-news-glyphosate/) [Source 2](https://www.efsa.europa.eu/en/news/glyphosate-no-critical-areas-concern-data-gaps-identified) [Source 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC6187125/) |
| 30 | brainbow | [15](set4_chapter_15.djot) | 208-213 | 108, 109, 110 | 3 | [Source 1](https://www.nature.com/articles/nature06293) [Source 2](https://pmc.ncbi.nlm.nih.gov/articles/PMC3713494/) |
| 31 | GMO mosquito | [16](set4_chapter_16.djot) | 215-226 | 101, 102, 103, 104, 105, 106, 107 | 5 | [Source 1](https://doi.org/10.1056/NEJMoa2030243) [Source 2](https://www.nature.com/articles/nbt.4245) |
| 32 | trendy mice | [16](set4_chapter_16.djot) | 227-233 | 111, 112, 113 | 4 | [Source 1](https://doi.org/10.1371/journal.pbio.0020294) [Source 2](https://doi.org/10.1038/387083a0) [Source 3](https://doi.org/10.1038/45432) |
| 33 | GMO animals | [16](set4_chapter_16.djot) | 234-244 | 114, 115, 116, 117, 118, 119, 120 | 4 | [Source 1](https://www.fda.gov/animal-veterinary/biotechnology-products-cvm-animals-and-animal-food/intentional-genomic-alterations-igas-animals) [Source 2](https://www.fda.gov/animal-veterinary/intentional-genomic-alterations-igas-animals/qa-consumers-intentional-genomic-alterations-animals) [Source 3](https://www.fda.gov/animal-veterinary/intentional-genomic-alterations-igas-animals/intentional-genomic-alterations-igas-animals-risk-reviewed-igas) |

## Important scientific distinctions

- Gene sequences, community profiles, and demonstrated enzyme activity answer different questions.
  OTU cutoffs in the older figures are explained beside modern ASV inference.
- Organic contaminants can transform into other molecules. Metals and radionuclides require
  accounting for binding, movement, oxidation state, and disposal. PFAS results are limited to
  the compounds and conditions actually studied. Removal is not automatically destruction.
- Compare fuel process steps and whole-system inputs. Distinguish xDNA bases from XNA backbones,
  bottom-up artificial cells from reduced genomes, and a synthetic chloroplast system from a plant.
- Glucose sensing distinguishes blood and interstitial fluid from an unsupported watch-only claim.
- Plant transformation method alone does not establish present USDA regulatory status. Current
  APHIS sources replace the old blanket gene-gun exemption premise.
- GMO food assessment, gene flow, herbicide resistance, and farming-system effects are separate
  questions. Glyphosate assessment slides distinguish hazard from exposure-dependent risk.
- Mosquito transgenes, Wolbachia, and gene drives use different mechanisms; cage results differ
  from field disease outcomes. Animal approval or risk review does not prove retail availability.

## Review and validation

See [LECT06_REVIEW.md](LECT06_REVIEW.md#instructor-review-markers) for the three retained review
markers: two personal-opinion slides and the Roundup Ready graphic. The
[completed factual checks](LECT06_REVIEW.md#completed-factual-checks) resolve nine earlier markers
using primary sources, without changing the 248-page sequence.

Strict lint, capacity, native artifacts, and rendered pages were checked; the same review records
test limitations. Local receipts and hashes are in `output/biotech_lect06_review/talking_points/`
and `output/biotech_lect06_review/final_followthrough/`. The subsequent
[business-plan visual revision](EXECUTIVE_SUMMARY_REVIEW.md) is complete in its own six-section deck.
