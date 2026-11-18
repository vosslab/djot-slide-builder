# Prototype collections for instructor critique

The [temporary-file rescue index](temp_cleanup/README.md) identifies material worth keeping
before clearing `_temp/`, including a browsable SVG sample gallery and a compact source archive.

These collections sample existing course material for review. Inclusion does not establish an
approved style. `exemplars/` is reserved for instructor-approved models that agents should follow.

C28 is an instructor-approved reference within this collection: smooth independent chromatids,
embedded allele regions, subtle banding, and clear crossing depth. Its four white zigzags mark
the exchanges between homologs; the figure illustrates meiotic crossing over.

## Chromosome corpus collection

The local review exports are `output/pdf/chromosome_review.pdf` and
`output/odp/chromosome_review.odp`.

The single 73-slide deck contains 68 current figures from 24 source decks across
Genetics LECT01, LECT02, LECT03, LECT04, LECT06, LECT08, LECT09, LECT10, LECT12, and LECT13.
It samples simple rods and replicated sisters, division scenes, crossover and tetrad diagrams,
centromere positions and movement, ploidy and dosage, inversions, and translocations. Empirical
photos, measured maps, and mixed figures are labeled separately so their purpose remains clear.
This is a broad sample, not an exhaustive image inventory or a ranking of preferred artwork.

SVG canvases are transparent so the slide theme shows through. C31/C44-C46 use tighter
inspected viewports; white structures, panels and source image content retain their fills.

Each figure has a stable ID, **C01-C68**, and its original deck and slide number. Source numbers
follow expanded source/ODP order, including hidden slides. Original paths and snapshot hashes are
in [chromosome_samples.csv](chromosome_samples.csv); prototype replacement paths and hashes are
in [chromosome_replacements.csv](chromosome_replacements.csv). The discoverable
[source record](chromosome_review_sources.md) preserves the review snapshot, multi-view mappings,
and C18 factual citations. The empirical C04 reference and the source coordinates in C51 are
preserved. C51/C52 use BPQ deletion rows: gray retained
material and thin magenta markers for missing intervals. C51 keeps unequal gene spacing
and distinct V/VI breakpoints; C52 uses equal gene slots. Original lecture Djot and generated
artwork remain unchanged; shared recipes are updated.

C03/C36 use one shared fusion figure based on C03. The ancestral material forms a continuous
dicentric chromosome with two outer telomeres. Its length and bands remain identical through
centromere inactivation and the final stage; removing the inactive collar leaves the body intact.

C13/C21 reuse the same crossing-over figure from two lectures, including its original TEM label.
The working C13 construction restores C21's cell backdrop and micrograph. Their 1-3 markers stay
in the image, while the matching explanations are native slide text. C25/C56/C59 likewise keep
their bottom explanations outside the SVG. C55 uses two independent SVGs on consecutive slides
so the overview and loop remain large; its index entry points to the first slide.
C63 keeps its three-column overview and adds two enlarged detail slides so the source
gene names remain readable. These views use the same chromosome components and positions.

Critique by ID, for example: "C12: keep the body shape; change the centromere and label size."
The [sister_chromatid_survey.md](sister_chromatid_survey.md) records the survey using C16 as
the reference, including corrections to short pairs and sister-centromere connections.
The [chromosome_label_survey.md](chromosome_label_survey.md) records gene-label and banding
decisions, using C53 and C01/C47 as references. Colored loci follow the chromosome geometry;
external labels remain where they improve readability.
Compare body shape, sister spacing, centromere treatment, outlines, ancestry colors, labels, and
amount of detail. Use the [feedback sheet](chromosome_feedback.csv) to record what to keep,
change, and why; C55 and C63 cover each of their companion detail views.

[chromosome_review.djot](chromosome_review.djot) is the one build target. Its two included source
parts keep the source files manageable; they export as a single presentation.

Regenerate the prototype-owned chromosome SVGs before building when shared chromosome geometry
changes. This command gives every source recipe an explicit prototype output path and never writes
lecture assets.

```bash
source source_me.sh && python3 prototype/make_chromosome_review.py
```

```bash
source source_me.sh && python3 deck_tools.py build prototype/chromosome_review.djot --format all
```

The build command writes `output/odp/chromosome_review.odp` and
`output/pdf/chromosome_review.pdf`. On the agent host, commands that invoke LibreOffice run outside the sandbox,
as specified in `AGENTS.md`.

The BPQ layer revision follows the requests archived in
[human_chromosome_requests.md](../docs/archive/human_chromosome_requests.md). Numerical BPQ
values establish a reference scale, not fixed dimensions for every illustration. Curved surfaces
use the same layer colors and alpha values mapped around the authored centerline. The review
prototype is the evaluation environment; the implementation lives in the shared SVG tools.
Uncondensed chromatin, including stringy DNA in early prophase, retains simple paths.
BPQ surface layers apply to condensed chromosome bodies; redundant curved-surface coordinates
are removed to keep the SVGs compact without splitting them into dependent files.
