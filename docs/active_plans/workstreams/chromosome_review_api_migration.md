# Chromosome review API migration ledger

Work follows the approved
[chromosome_review_api_migration_plan.md](../active/chromosome_review_api_migration_plan.md).
The migration baseline has 73 pages, 68 figure IDs, and 71 figure placements. Strict native
Djot lint and 62 focused tests passed at baseline. Seven figures already use the API and seven
reviewed Mini2 figures are available for promotion. Evidence from earlier work is in
[chromosome_review_verification.json](../../../prototype/chromosome_review_verification.json)
and [chromosome_engine_mini2.md](chromosome_engine_mini2.md).

## Workstream assignments

The engine proofs establish the renderer contract before dependent recipes use it. Each recipe
owner supplies a source comparison, representative render, and meaningful invariant checks.
Fresh reviewers assess specification and visual quality. Integration checks the assembled deck.
The scoped implementation workstreams use `gpt-6.2-sol`.

| Owner | Figure IDs or component | Acceptance evidence | Status |
| --- | --- | --- | --- |
| `engine` | Shared paths, closure, and independent sisters | Shared renderer API and focused tests, C48 closed seam, C57 belt geometry. | Integrated |
| `ring_figure` | C48 | Preserved direct repeats and loci, closed excised ring, shortened linear product, conserved material. | Integrated |
| `mini_promotion` | C01, C16, C25, C28, C55, C61, C63 | Reviewed Mini2 models, all full-deck views, and native C25 text. | Integrated |
| `forms` | C02, C03, C05, C06, C36 | Form identity, shared fusion artwork, original map or evidence components, and XY fertilization. | Integrated |
| `division_intro` | C07-C10 | Chromosome and chromatid counts, replication and mitotic stages. | Integrated |
| `division_meiosis` | C11-C14, C21 | Condensation and pairing states, ancestry, and shared C13/C21 artwork with retained evidence. | Integrated |
| `assortment` | C15, C17, C19 | Assortment counts, mitosis/meiosis comparison, and reciprocal cross outcomes. | Integrated |
| `linkage` | C24, C26, C27 | Reciprocal exchange, both loss-of-heterozygosity alternatives, and yeast outcomes. | Integrated |
| `movement` | C30, C32-C35 | Karyotype preparation, centromere placement, movement, and replication state. | Integrated |
| `ploidy` | C37-C43 | Set counts and identity, sister cohesion, and reduced or unreduced products. | Integrated |
| `dosage` | C44-C46 | Barr bodies derived from corresponding active X models and original lineage or crossover outcomes. | Integrated |
| `deletion_maps` | C47, C49-C52 | Deleted material, exact map data, distinct spacing rules, and unchanged empirical images. | Integrated |
| `duplication` | C53-C54 | Unequal crossover and opsin interval order and copy count. | Integrated |
| `inversion` | C56-C60 | Source locus order, paired centromeres, independent C57 sister paths, and crossover products. | Integrated |
| `translocation` | C62, C64, C65, C67, C68 | Identities, centromeres, spindle poses, and gamete products. | Integrated |
| Integration | Canonical generator, references, and exports | Exact inventory, repeatable hashes, strict native checks, export receipts, and independent review. | Complete |

C18, C20, C22, C23, C29, C31, and C66 already used the API. The migration promotes C01, C16,
C25, C28, C55, C61, and C63 from Mini2. The C55 pair and the three C63 views each share a model.
C03/C36 and C13/C21 share artwork and retain their original native captions and citations.

The review has 73 pages, 68 IDs, and 71 figure placements. The inventory contains 70 SVG
placements and 68 unique SVGs. C04 uses its original local course JPEG for export. The generator
uses ten frozen image and blank template inputs in `prototype/assets/chromosome_review_sources/`.
An audit hook blocked opens of all 1,024 tracked Genetics files during successful regeneration,
and all 1,024 tracked Genetics files matched their original bytes.

The shared painter closes the C48 excision ring without telomere caps. C57 uses independent
paths and anchors the belt at the two sister waist centers. C56-C58 use authored paths to show
the schematic inversion pairing loop. C10 and C11 use matching material models when tracing
uncondensed chromatin and rendering the condensed products. The `render_sisters()` default
gives C02, C38, and C67 gentle mirrored curves. C39 requests straight chromatids to fit the
cohesin drawing. Existing explicit-path APIs preserve their behavior.

## Source corrections and clarifications

| Figure | Change and reason |
| --- | --- |
| C06 | Show an X-bearing gamete and a Y-bearing gamete forming an XY zygote. The gamete identities and zygote chromosomes agree. |
| C14 | Match the ancestry color in one miniature to the corresponding enlarged homolog. |
| C24 | Show the reciprocal product documented in the lecture. Explain in native text that the two exchanges restore the parental D-H combination. |
| C26 | Show both outcomes documented in the original notes. |
| C35 | Use unreplicated and replicated to describe the chromosome forms. |
| C42 | Count chromosomes separately from sister cohesion so each stage agrees with its ploidy label. |
| C49 | Increase the map label contrast while preserving the measured Mb and cM positions. |
| C59 | Restore the second crossover cue in the SVG description. |
| C63 | State the example frequencies in the native overview caption. Adjacent-1 and Adjacent-2 each occur 25% of the time, and Alternate occurs 50% of the time. |
| C68 | Fit the diagram alongside a native caption that explains how fertilization can produce trisomy 21. |

C27 retains small live labels inherited from the source composition. The pairing and crossover
stages are static illustrations.

## Verification receipts

| Check | Acceptance evidence | Status |
| --- | --- | --- |
| Recipe specification | Source comparisons and follow-up reviews confirmed conserved material, source locus order, chromosome counts, and product identities where applicable. The C56-C58 poses are schematic. | Pass |
| Empirical evidence | Original C04 JPEG and embedded raster payloads match byte for byte. C49 preserves separate Mb/cM coordinates. C51 retains unequal spacing and distinct V/VI intervals. C52 retains equal slots and deletion membership. | Pass |
| Deterministic generation | Scratch builds with `PYTHONHASHSEED=131`, `229`, and `453` match the 68 canonical SVGs and replacement CSV byte for byte. SVG IDs are unique, references resolve, and fonts and inventory hashes match. | Pass |
| Lecture protection | All 1,024 tracked Genetics files and both preserved review records match baseline SHA-256. Detached regeneration also passed with lecture file opens blocked. | Pass |
| Lint and tests | Pyflakes passed. Strict native Djot lint covered 3 decks, 87 slides, and 85 images. All 72 focused chromosome tests passed. The base suite passed 10,233 tests with one source-length advisory for `svg_tools/chromosomes.py` at 952 lines. | Pass |
| ODP structure | 73 slides and 71 exact image embeds. Native titles, captions, and editable explanations match the source. C18 retains the only speaker note. | Pass |
| PDF structure | 73 pages. Native visible text is selectable. Full review build reported zero fit or capacity findings. | Pass |
| Rendered pages | Independent reviewers covered the 71 figure pages and both bookends. The integration reviewer inspected the 15 changed pages at scale. The remaining 58 pages match the reviewed render pixel for pixel. | Pass |

The initial visual review assignments were `visual_01_18` for C01-C18 and the cover,
`visual_19_35` for C19-C35, `visual_36_53` for C36-C53, and `visual_54_68` for C54-C68 and the
closing page. The integration reviewer found no material issues on final pages 1, 3, 12, 14,
22, 25, 27, 28, 33, 39, 40, 50, 65, 71, and 72.

| Final export | Bytes | SHA-256 |
| --- | ---: | --- |
| `output/odp/chromosome_review.odp` | 17,045,246 | `5ab76de87f0a0738df060d39767abca7ad287f906ca93afbb869d3bcd3bae1ca` |
| `output/pdf/chromosome_review.pdf` | 25,274,269 | `619e4e6d6f82c2b5b31eea80b24c14e28437257062b90f9da886a931171a8a19` |

C16 is the largest PDF figure by page-owned drawing objects at 2,781,710 bytes. Its form
objects account for 2,430,701 of those bytes. The
[verification record](../../../prototype/chromosome_review_verification.json) retains the
final receipt alongside the earlier work.
