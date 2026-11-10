# M2 deletion layout correction

Saved workstream evidence for [genetics_visual_renewal_plan.md](../active/genetics_visual_renewal_plan.md).
Source owner: `/root/m2_deletion_layout_fix`.
Local source: `_temp/genetics_visual_renewal/m2_deletion_layout_fix/HANDOFF.md`. This is a saved snapshot;
see [genetics_visual_renewal_progress.md](genetics_visual_renewal_progress.md)
for current authorization, dependencies and acceptance status. Scratch paths remain local.
Non-ASCII source characters use numeric HTML character references.

Status: source frozen for centralized rerender. Export acceptance pending.

## Scope

- Source: `genetics/LECT11/djot/lect11d_deletion_mechanisms.djot`, original owned mapping range lines 263-687.
- Root: `genetics/LECT11/djot/lect11d-chromo_alter_1-deletions.djot`.
- Actual affected PDF pages: 29-43. Mapping setup page 28 is unchanged.
- Source before and after the owned sequence is byte-identical to `source_before.djot` here.
- No SVG, renderer, dependencies, fixtures or permanent tests changed. No LibreOffice invoked by this worker.

## Actual correction

All 30 mapping tables now use `column-widths="4,1,1,1,1,1,1" padding="0pt 4pt"`.
This gives the full words Position and Deletion sufficient width without abbreviating them.

On reveal pages 30-43, each matrix has three borderless full-width native cells below its five data rows. These carry the original comparison/hint text and colors; shorter states leave the unused rows empty. All 14 stages therefore reserve the same geometry. The former list bullets become plain native hint lines; wording, colors, order and visibility remain unchanged. The page 29 phenotype legend stays as its original two bullets.

The existing authoring vocabulary has no table font-size override. Width/padding alone left variable scale because the number of hint lines changed. Reserving three rows uses existing colspan/border controls and avoids renderer changes or hidden filler text.

## Checks and evidence

Read AGENTS.md, the approved plan, TABLE_AUTHORING_GUIDE.md, SVG_DIAGRAMS.md and PEDAGOGY_GUIDE.md. Reviewed the original worker's scientific handoff and inspected full-size old PDF pages 30 and 36; these exhibit split words and different matrix sizes.

Commands (repository root):

```bash
source source_me.sh && python3 deck_tools.py lint --require-native --native-executable "$(command -v jotdown)" genetics/LECT11/djot/lect11d-chromo_alter_1-deletions.djot
source source_me.sh && PYTHONPATH=. python3 _temp/genetics_visual_renewal/m2_deletion_layout_fix/verify.py
```

Results:

- Strict lint passed: 112 slides, 45 images (`lint.txt`).
- All 450 signs in 15 matrices match the pre-fix source; all 15 gene rows, including 14 reveal states, are unchanged.
- All comparison/missing/present/final-answer wording and colors match the pre-fix source.
- The 16-slide mapping sequence remains 16 slides; outside source unchanged.
- Compiled-only inspection: identical native table rectangles, row heights, column widths and selected font sizes across pages 30-43. Left position table is 28 pt, right matrix/hint table is 26.25 pt. Header runs contain no line breaks. This is source/layout evidence, not rendered acceptance.
- Scientific invariants were already independently checked against source evidence by the original owner: 30 signs, interval memberships, unique order b a c e d f, reveal order b/e/a/d/c/f. This correction preserves those exact rows and does not reinterpret the science.

Frozen source SHA-256: `a76bbcd86ef8e203721b124bc0a5d768cb5789e2e62c5e01601201613a8cdd78`.

## Required centralized follow-up

Sole exporter must rebuild the named root ODP/PDF and inspect pages 29-43 at full presentation size. Confirm single-line headers, readable six sign columns, stable tables across pages 30-43, no clipped hints at the bottom, correct table-to-hint boundary, and preserved native editability. Page 29 has a separate long legend and may have a smaller matrix than the subsequent staged pages; the 14 reveal pages are the explicitly stabilized sequence.

Fresh specification and quality review must inspect the new actual exports. No classroom or playback acceptance is claimed here.
