# M2 deletion mapping handoff

Saved workstream evidence for [genetics_visual_renewal_plan.md](../active/genetics_visual_renewal_plan.md).
Source owner: `/root/m2_deletion`.
Local source: `_temp/genetics_visual_renewal/m2_deletion/HANDOFF.md`. This is a saved snapshot;
see [genetics_visual_renewal_progress.md](genetics_visual_renewal_progress.md)
for current authorization, dependencies and acceptance status. Scratch paths remain local.
Non-ASCII source characters use numeric HTML character references.

Status: source complete and frozen for centralized export; export acceptance pending.

## Scope and consumers

- Source: `genetics/LECT11/djot/lect11d_deletion_mechanisms.djot`, lines 263-687.
- Root consumer: `genetics/LECT11/djot/lect11d-chromo_alter_1-deletions.djot`.
- Changed slides: 28-43 inclusive in both the fragment and expanded root; 16 slides remain 16 slides.
- New original vector: `genetics/LECT11/djot/assets/lect11d-chromo_alter_1-deletions/deletion_intervals.drawn.svg`.
- Retained originals: images 018, 019, 020 remain on disk. Earlier figures 016/017 remain unchanged: the distinct named polytene example is M3 scope.
- Entire source before and after the mapping range is byte-identical to the snapshot `source_before.djot`.

## Exact source-to-result map

| Original source | Result |
| --- | --- |
| Slide 28, image 018 full problem | Native setup prose and shared interval SVG. The original data follows immediately on slide 29. Explicit task: infer gene order. |
| Slide 29, images 019/020 | Shared interval SVG, native full matrix, blank native position row, explicit phenotype legend. |
| Slides 30-43, images 019/020 and progressive native prose | Same full matrix and interval geometry on every slide; native six-position row preserves every question mark, blank, and revealed gene. Comparison and missing/present hint prose retained. |

All 13 mapping `@replaceme` markers were removed only after full comparison of the staged source and original image 018 problem, image 019 intervals, and image 020 matrix. The unmodified earlier `@replaceme` markers remain. Their removal here records completed source reconstruction; it does not assert rendered acceptance.

| Slide | Gene state (positions 1-6) | Comparison / hint |
| --- | --- | --- |
| 30 | `? _ _ _ _ _` | - [compare Del 1 and Del 2]{color=#D40000} |
| 31 | `b _ _ _ _ _` | - [compare Del 1 and Del 2]{color=#D40000} |
| 32 | `b _ _ ? _ _` | - [compare Del 2 and Del 3]{color=#D40000} |
| 33 | `b _ _ e _ _` | - [compare Del 2 and Del 3]{color=#D40000} |
| 34 | `b ? _ e ? _` | - [compare Del 3 and Del 4]{color=#D40000} |
| 35 | `b ? _ e ? _` | - [compare Del 3 and Del 4]{color=#D40000} / - [missing in Del 3]{color=#007A00} / - [present in Del 4]{color=#007A00} |
| 36 | `b a _ e ? _` | - [compare Del 3 and Del 4]{color=#D40000} / - [missing in Del 3]{color=#007A00} / - [present in Del 4]{color=#007A00} |
| 37 | `b a _ e ? _` | - [compare Del 3 and Del 4]{color=#D40000} / - [present in Del 3]{color=#B74300} / - [missing in Del 4]{color=#B74300} |
| 38 | `b a _ e d _` | - [compare Del 3 and Del 4]{color=#D40000} / - [present in Del 3]{color=#B74300} / - [missing in Del 4]{color=#B74300} |
| 39 | `b a ? e d ?` | - [compare Del 4 and Del 5]{color=#D40000} / - [missing in Del 4]{color=#007A00} / - [present in Del 5]{color=#007A00} |
| 40 | `b a c e d ?` | - [compare Del 4 and Del 5]{color=#D40000} / - [missing in Del 4]{color=#007A00} / - [present in Del 5]{color=#007A00} |
| 41 | `b a c e d ?` | - [compare Del 4 and Del 5]{color=#D40000} / - [present in Del 4]{color=#B74300} / - [missing in Del 5]{color=#B74300} |
| 42 | `b a c e d f` | - [compare Del 4 and Del 5]{color=#D40000} / - [present in Del 4]{color=#B74300} / - [missing in Del 5]{color=#B74300} |
| 43 | `b a c e d f` | - [final answer!]{color=#D40000} |

## Protected scientific data

Matrix columns are a, b, c, d, e, f. Native entries are exactly:

```text
Del 1: - - - + + +
Del 2: - + - + + +
Del 3: - + - + - +
Del 4: + + - - - +
Del 5: + + + - - -
```

Deleted positions: Del 1 = 1-3; Del 2 = 2-3; Del 3 = 2-4; Del 4 = 3-5; Del 5 = 4-6. The diagram marks deleted intervals, not retained chromosome portions. Positions are schematic, not genetic distances. The original recessive-allele heterozygote setup determines the legend: plus is wildtype phenotype/present wildtype allele; minus is mutant phenotype/missing wildtype allele.

The unique solution for the fixed numbered intervals is b a c e d f. Reveal order is b, e, a, d, c, f. The prompt state always precedes its answer; no gene labels are hidden in SVG titles or descriptions.

## Construction and editability

Reused the investigated interval construction after independently checking all source memberships. Added semantic IDs for the five deletion paths and replaced pilot description wording that referred to an answer version. Stable 870 x 520 viewBox, live labels, blue reference chromosome, magenta deleted intervals. Two-panel slides stack diagram plus native position table on the left and native matrix plus current comparison on the right. All related native tables use explicit `column-widths="2.3,1,1,1,1,1,1"` and 4pt padding. Native prose stays outside the SVG. Source green/orange missing/present hints keep their roles using readable house palette colors.

Local passages used:

- `/Users/vosslab/.codex/skills/experts/svg-creator-expert/references/local-only/scientific_illustration/A_Handbook_of_Biological_Illustration-1988.md`, lines 274-284 (observation, clarity, emphasis/comparison): simplify to the exact intervals without decorative chromosome banding or amplified differences.
- `/Users/vosslab/.codex/skills/experts/svg-creator-expert/references/local-only/svg_authoring/Mastering_SVG-2018.md`, lines 635-663 (viewBox and viewport): stable coordinate system and proportional scaling.
- Repository `SVG_DIAGRAMS.md`, `TABLE_AUTHORING_GUIDE.md`, color, voice, and pedagogy guides: native matrices/prose, stable reveal layouts, gene italics, retained comparison voice.

## Checks completed

- Strict native lint passed for root: 112 slides, 45 images. Command: `source source_me.sh && python3 deck_tools.py lint --require-native --native-executable "$(command -v jotdown)" genetics/LECT11/djot/lect11d-chromo_alter_1-deletions.djot`.
- An independent permutation check tested all 720 orders against the 30 signs and five fixed intervals: one solution, b a c e d f.
- All 15 full native matrices (450 signs) match the 30-sign source.
- Extracted original stage strings equal the 14 new native gene-row strings in order, with each blank and question mark intact.
- XML parses; IDs unique; title/description ARIA IDs resolve; positive viewBox; no image, feImage, script, foreignObject, animation, or external href. Five path endpoint checks reproduce interval membership.
- Standalone librsvg renders inspected at 480px and 870px width against white; clear labels and all five intervals, no clipping. Evidence: `intervals_small.png`, `intervals_large.png`, `checks.txt`.
- Source outside owned sequence unchanged. No renderer, dependency, fixture, or test-suite changes.

## Pending centralized acceptance

- Build root ODP/PDF with serialized unsandboxed repository scripts.
- Inspect all slides 28-43 at presentation size: native table text, diagram sizing, stage stability, no overlap, and complete setup/problem matrix.
- Verify SVG bytes packaged, native tables/cell text retained.
- Perform requested native table edit/save/reopen evidence.
- Fresh specification and quality reviews after the actual exports.

## Frozen source hashes

- `genetics/LECT11/djot/lect11d_deletion_mechanisms.djot`: `6b0d650c3d1b03e98171ff056bb2ce249dfdb615670e7d17ad65e451710321d1`
- `genetics/LECT11/djot/assets/lect11d-chromo_alter_1-deletions/deletion_intervals.drawn.svg`: `0d7bd69afca51f884bb9dd18187b41b371597f55f2f20a04126008eb9d2b9447`
