# Inheritance classification evidence

Saved workstream evidence for [genetics_visual_renewal_plan.md](../active/genetics_visual_renewal_plan.md).
Source owner: `/root/classify_inheritance`.
Local source: `_temp/genetics_visual_renewal/inheritance/EVIDENCE.md`. This is a saved snapshot;
see [genetics_visual_renewal_progress.md](genetics_visual_renewal_progress.md)
for current authorization, dependencies and acceptance status. Scratch paths remain local.
Non-ASCII source characters use numeric HTML character references.

Date: 2026-11-09. M1 classification only; canonical sources were read-only for this agent.

## Coverage

- 567 original inventory uses, 395 asset paths, 364 distinct SHA-256 values.
- 30 physical sources, 28 root decks; 51 concept packages.
- 217 uses: original SVG redesign.
- 261 uses: native-content repair.
- 87 uses: retain with reason.
- 2 uses: source clarification needed.
- 0 uses: already suitable. Existing image-free SVG tables still need native table editing;
  no illustrative raster was kept solely because it was convenient or visually acceptable.

`classify.py` verifies a multiset equality of all original inventory fields except disposition,
which is separately preserved as `original_disposition`. Every repeated or hidden use is retained.
It also asserts exactly one asset decision for IDs 1-395 and a nonempty reason and concept ID.
Run from repository root:

```bash
source source_me.sh && python3 _temp/genetics_visual_renewal/inheritance/classify.py
```

The script completed with `EXACT ORIGINAL-USE COVERAGE VERIFIED`.

## Visual and contextual review

All twenty contact sheets `contact_01.webp` through `contact_20.webp` were opened and inspected.
They display all 395 distinct asset paths in inventory order, including image-containing SVGs.
The original paths, complete source-slide blocks, repeated uses and review IDs are in
`manifest.json` and `contexts.txt`. Every concept has its full source contexts in
`concept_contexts/`, so brief dispatch does not depend on terse filename descriptions.

The reviewer read source context across the entire set and the complete 04C/D sources for M2.
Enlargements inspected for dense labels, quantitative values, biology and conflicts:
IDs 28,29,37,42,44-48,54,55,83,84,89,100,101,112,125,128,130,161,171,182,208,
272,273,278,290,303,313,375,385,389,394. These remain as `asset_NNN.webp`.
All other assets were reviewed in contact sheets with corresponding native source context.

Pillow created thumbnail/review derivatives only, not replacement artwork. SVG previews used
`rsvg-convert`; an initial CairoSVG attempt failed on an embedded image near asset357, so the
complete set was regenerated successfully using librsvg. No LibreOffice command was run.

## Original source recovery

The blank `image_034.jpg` in LECT06C contains only header bars. Direct read-only extraction
from `genetics/LECT06/lect06c-meiosis.odp`, original slide48, recovered its complete mitosis/
meiosis comparison. Original slide52 similarly supplied labels missing from image035.
See [genetics_visual_inheritance_source_recovery.md](genetics_visual_inheritance_source_recovery.md). These are implementation inputs, not final
rendered repairs. Both original ODP/PDF inputs exist locally; no new export was needed.

## Ownership and external consumers

`physical_ownership.csv` is the assignment boundary: a physical source has one owner even when
several concept packages touch it. Native repairs and art within a source travel together.
Inventory-wide lookup found no roots outside LECT04-07 consuming the exact physical source
paths or asset paths in this workstream. Shared-looking local copies have distinct paths and
must be coordinated for consistency, not edited as one invisible shared source.

M2 pea artwork has local copies in 04E/F and 05H. 05H's second experiment is a different
white x white cross with 382/269 and approximately9:7; it must not inherit Mendel705/224.
The two YouTube physical include files have their owning LECT07 roots explicitly in the CSV.

## Scientific decisions and cautions

- D1 is user-approved: correct 04C's dominance-from-frequency claim using F1 hybrid evidence,
  preserve the purple/white pea example, and document the change. M2 brief reflects this.
- INH-20 is unresolved: LECT05C images013/015 explicitly say sex-influenced male/female
  dominance while native headings say X-linked recessive/dominant. The parent manager was
  notified; changing family topology or declaring a different model requires a content decision.
- INH-10: inspected egg/sperm image shows XX in egg and XY in sperm. These cannot be copied
  as ordinary human haploid gamete labels. The replacement owner must establish the intended
  organism/count model with the parent before creating a scientifically corrected schematic.
- INH-15: 04H's claim of a32x32 Punnett square for the given3.4 parents should be checked;
  the genotype answer36 is separately preserved.
- INH-22: original 05D Huntington conditional-probability prose contains contradictory
  P(A|B) and P(B) statements. Preserve the problem and resolve the derivation before migration.
  05D-v2 supplies a coherent separate explanation but is not blanket authority to replace05D.
- INH-26: human hair single-locus simplification, patterned flowers as codominance, and the
  horned/polled dominance claim need explicit source verification. Retaining their photographs
  does not certify those assertions.
- INH-36: the6^7 wheat combination assertion needs a pairing-model explanation; do not treat
  six chromosome sets as six alternative haploid homolog choices without supporting biology.
- INH-44/45: the yellow-dominant example and graph show seed color, while native heading says
  pea pod color. INH-44 also flags a second-alpha typo where the sequence requires beta.
- INH-46: source challenge calls Tt short-tailed but asks tailless; preserve its lethal-TT
  model and resolve wording explicitly rather than reverse the allele meaning.
- INH-48: native worksheet transcription must retain a ledger distinguishing source rounded
  expected counts from exact3:1 expectations and their resulting chi-square/P differences.

These are bounded source/scientific review items within their packages, not a finding that all
51 packages are blocked. None was silently changed in canonical teaching content by this agent.

## Handoff package

Required dispatch inputs: `classification.csv`, `BRIEFS.md`, `M2_PEA_BRIEF.md`,
`SOURCE_RECOVERY.md`, `physical_ownership.csv`, `summary.json`, and `concept_contexts/`.
`manifest.json`, original inventory, source artwork and the review WebPs supply evidence.
`prepare.py` and `classify.py` are temporary repeatability/check scripts, not product code.

The approved plan, experimental FINDINGS and SVG expert skill informed classification.
Repository SVG_DIAGRAMS, pedagogy, color, voice, repo and Markdown guidance were consulted.
Scientific facts were read from owning sources; unfamiliar detailed organisms/meiosis require
bounded family trials and domain-source verification before migration as specified in briefs.

## Verification limits

No canonical edits, new SVGs, family trials, ODP/PDF builds, attended playback, external source
verification, or base-suite run were performed by this classification agent. This is complete
M1 disposition coverage and dispatch material, not evidence of completed classroom migration.
