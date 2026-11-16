# Prototype collections for instructor critique

The [temporary-file rescue index](temp_cleanup/README.md) identifies material worth keeping
before clearing `_temp/`, including a browsable SVG sample gallery and a compact source archive.

These collections sample existing course material for review. Inclusion does not establish an
approved style. `exemplars/` is reserved for instructor-approved models that agents should follow.

## Chromosome corpus collection

[Open the PDF](chromosome_review.pdf) or
[open the editable presentation](chromosome_review.odp).

The single 70-slide deck contains 68 unchanged current figures from 24 source decks across
Genetics LECT01, LECT02, LECT03, LECT04, LECT06, LECT08, LECT09, LECT10, LECT12, and LECT13.
It samples simple rods and replicated sisters, division scenes, crossover and tetrad diagrams,
centromere positions and movement, ploidy and dosage, inversions, and translocations. Empirical
photos, measured maps, and mixed figures are labeled separately so their purpose remains clear.
This is a broad sample, not an exhaustive image inventory or a ranking of preferred artwork.

Each figure has a stable ID, **C01-C68**, and its original deck and slide number. Source numbers
follow expanded source/ODP order, including hidden slides. Full paths and snapshot hashes are in
[chromosome_samples.csv](chromosome_samples.csv). The original images are referenced directly;
the exported ODP embeds them. Original lecture sources and artwork remain unchanged.

C21 flags an existing rendering issue: its TEM area appears blank in the exported view.

Critique by ID, for example: "C12: keep the body shape; change the centromere and label size."
Compare body shape, sister spacing, centromere treatment, outlines, ancestry colors, labels, and
amount of detail. Use the editable speaker notes or the optional
[feedback sheet](chromosome_feedback.csv) to record what to keep, change, and why.

[chromosome_review.djot](chromosome_review.djot) is the one build target. Its two included source
parts keep the editable source files manageable; they export as a single presentation.

```bash
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B deck_tools.py build prototype/chromosome_review.djot --format all
```

The build command writes `output/odp/chromosome_review.odp` and
`output/pdf/chromosome_review.pdf`. The reviewed copies linked above are kept beside the
prototype source. On the agent host, commands that invoke LibreOffice run outside the sandbox,
as specified in `AGENTS.md`.
