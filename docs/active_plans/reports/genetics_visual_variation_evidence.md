# Variation M1 evidence and handoff

Saved workstream evidence for [genetics_visual_renewal_plan.md](../active/genetics_visual_renewal_plan.md).
Source owner: `/root/classify_variation`.
Local source: `_temp/genetics_visual_renewal/variation/EVIDENCE.md`. This is a saved snapshot;
see [genetics_visual_renewal_progress.md](genetics_visual_renewal_progress.md)
for current authorization, dependencies and acceptance status. Scratch paths remain local.
Non-ASCII source characters use numeric HTML character references.

Review date: 2026-11-09. Scope: every original inventory row whose root deck is under
LECT10, LECT11 or LECT13. Canonical files were read only by this classification agent.

## Coverage

- 403/403 original image-use rows, preserving original fields and original order.
- 248 unique asset paths: 213 PNG, 23 JPG and 12 SVG.
- 20 physical sources and 13 root consumers.
- 59 concept briefs, with physical-source dispatch index and exact heading/layout/slot anchors.
- 235 uses assigned original SVG redesign; 77 native-content repair; 86 retained with reason;
  5 source clarification needed; 0 already-suitable uses in this scoped source snapshot.
- Repeated roots/includes remain separate CSV rows. `all_physical_consumers`,
  `shared_asset_consumers` and `identical_asset_paths` include cross-course consumers from the
  complete original inventory, not merely this workstream. These fields prevent duplicate owners.
- Row-level mixed-panel exceptions are intentional: the native M2 matrix differs from its SVG
  interval graphic; genuine photos within mixed figures remain original evidence.

The 59 concept units are not 59 independent canonical file editors. Dispatch by the physical-source
index in BRIEFS.md. Concepts sharing a physical file use one final file editor; assets can be
prepared independently in scratch. M2 already owns the mapping sequence inside
`lect11d_deletion_mechanisms.djot`; earlier mechanism diagrams are reserved for M3. All exports
are centrally serialized by `m2_exports`.

## Inspection performed

All 248 unique assets were rendered or opened on 13 contact sheets, `contact_00.jpg` through
`contact_12.jpg`. Each ID is mapped to its original path in `assets.txt` and CSV. SVGs were rendered
with rsvg-convert for inspection; no LibreOffice command was launched.

Full-size enlargement inspection additionally covered:

- 020/021: all 24 chromosome-code entries and distinct M-FISH/SKY fluorophore keys.
- 138: full male/female heterogamety reference table, species and genotype columns.
- 184: exact underdeveloped/overdeveloped clinical-model claims and source attribution.

All 14 nonannouncement teaching physical files were read for local content, totaling 6,440 lines;
the retained `.context.txt` copies are the preintegration source snapshot. Image-bearing local
slides in the six announcement/shared physical files were read separately. This included full
prompts, answer text, progressive comparisons, hidden announcements and retained evidence context.
No classification is inferred from filenames alone.

Read guidance: AGENTS.md; COLOR_GUIDE.md; VOICE_GUIDE.md; PEDAGOGY_GUIDE.md;
SVG_DIAGRAMS.md; the approved GENETICS_VISUAL_RENEWAL_PLAN.md; experimental FINDINGS.md;
SVG creator expert SKILL.md, task_selection.md and project_workflow.md. This is classification
and design specification, so no new drawing is claimed and no construction-book passage is claimed
as consulted for a finished artifact.

## Scientific source checks

Executed through `source source_me.sh && python3`:

1. Asserted complete 403-row identity against original inventory, including preservation of every
   original field (`original_disposition` preserves its previous value).
2. Asserted 248 unique assets, coverage of IDs 000-247 exactly once by concept assignment, and
   nonempty disposition/reason/concept for every row.
3. Recomputed all 30 deletion-mapping signs from intervals 1-3, 2-3, 2-4, 3-5 and 4-6 and order
   **b a c e d f**. Exact source rows, columns a b c d e f:

   ```text
   Del 1  - - - + + +
   Del 2  - + - + + +
   Del 3  - + - + - +
   Del 4  + + - - - +
   Del 5  + + + - - -
   ```

4. Enumerated all 720 permutations for extra problems 8.14, 8.15 and 8.16. Found respectively
   4, 2 and 4 valid directed orders, including reversal. The source's unresolved a/d and a/e
   groups remain unresolved; problem 8.15 has unique order up to reversal.

Results are recorded in `coverage.json` and `source_checks.json`. The original M2 assets are
`_temp/svg_migration_research/experiments/assets/deletion_question.drawn.svg` and
`deletion_answer.drawn.svg`; their existing first answer reveals only b. The complete canonical
sequence must continue through b &#8594; e &#8594; a &#8594; d &#8594; c &#8594; f, maintaining each preceding prompt and
intermediate unknown. BRIEFS.md names every source slide anchor.

## Instructor-visible source decisions

The parent manager agreed that these source conflicts require clarification; originals remain:

| Source anchor | Asset ID | Issue and intended decision |
| --- | --- | --- |
| `lect10b-karyotypes.djot:348` | 033 | Single versus replicated chromosome is labeled haploid versus diploid, conflicting with the deck's correct replication distinction. Decide on unreplicated/replicated replacement or removal from this example. |
| `lect11c_sex_determination.djot:345` and `:381` | 128,129 | SRY heading contains myoD/muscle-determination figure and labels without an explicit analogy. Decide whether analogy or different mechanism is intended. |
| `lect11e-chromo_alter_2-duplications.djot:173` | 173 | Infographic asserts ten rainbow colors and one hundred million distinguishable colors, unlike surrounding qualified claims. Decide source-as-claim treatment or verified replacement. |
| `lect11e-chromo_alter_2-duplications.djot:306` | 184 | Autism/schizophrenia underdevelopment/overdevelopment diagram is a specific attributed hypothesis. Decide its evidential framing before redrawing. |

Additional source flags are in the relevant briefs, rather than silently corrected: source fly
compensation-complex location statement; historical clinical language; source CAG-range differences;
translocation solution-summary letter transposition; conditional 25/25/50 segregation probabilities;
and the distinction between human chromosome-2 telomeric fusion and Robertsonian fusion. These are
scientific-review checkpoints, not excuses to retain unrelated illustration families.

## Retention and trial rationale

Retentions are actual people/organisms, microscopy, karyotype evidence, measured curves, residue
maps, quantitative comparative maps, identified media, functional QR code or source branding.
Specific reasons appear on every retained row. No diagram is retained solely because it is dense,
time-consuming, or unfamiliar. Empirical curve/branch-length regeneration needs numerical data;
no smooth curves or evolutionary distances were invented from pixels.

Untested mitosis/meiosis, inverted/direct-repeat recombination, chromosome crossover, multivalent
segregation, anatomy, detailed fly-eye/bird forms and dense reference-table layouts are explicitly
assigned bounded scratch trials. Trials compare two plausible constructions where representation
is uncertain, preserve source invariants, and require actual centrally managed export before
scaling. The existing pilot establishes only its investigated families.

## Companion files and limits

Required for dispatch: `classification.csv`, `BRIEFS.md`, `EVIDENCE.md`, `assets.txt`, contact sheets
00-12, and original repository source/assets. `source_checks.json` gives the computed M2/problem
oracle. `.context.txt` files preserve original local teaching sequence for future comparisons.
`concepts.json` is a machine-readable copy of concept contracts; `retained_evidence_reasons.json`
holds per-image evidence reasons. `classify.py` is a one-time scratch classification generator,
not a production dependency. Its initial generic retained reasons were refined in the final CSV;
the final CSV and reports are authoritative for dispatch.

Not performed: canonical edits, new drawings, external scientific-source verification, whole-course
scientific correction, ODP/PDF exports, attended playback, or learner acceptance. The classification
is complete; construction and export evidence belong to subsequent implementation/review milestones.
