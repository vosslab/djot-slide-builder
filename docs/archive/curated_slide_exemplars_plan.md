# Plan: Curated slide exemplars

> Status: Approved plan; implementation complete after independent INTEGRATION ACCEPT.
> See [curated_slide_exemplars_progress.md](curated_slide_exemplars_progress.md) for the evidence ledger
> and [curated_slide_exemplars_results.md](curated_slide_exemplars_results.md) for delivery and limits.

## Goal

Create a self-contained collection of reusable teaching-slide examples for instructors and future
authoring agents. Curate material from Genetics, Biotechnology, and Biostatistics, which together
contain about 4,900 physical slide definitions.

Use lightly polished copies organized into short decks by teaching purpose. Preserve instructional
content, relationships, and course identity. Improve spacing, wrapping, or layout only in the copies.
Do not modify original courses or the existing [table styles example](../../exemplars/table_styles.djot).

## Audience and selection

- Serve instructors and future authoring agents seeking concrete teaching patterns.
- Prefer instructor-authored or cleaned candidates.
- Exclude unresolved `@replaceme` samples.
- Use only original or instructor-owned assets with verified provenance and attribution.
- Do not use textbook or publisher material, screenshots, or assets of unknown origin.
- A `.drawn.svg` file alone does not prove ownership; choose another candidate when ownership is
  uncertain.

## Decks

Create seven flat, buildable Djot decks under `exemplars/`, with these exact names and
teaching purposes:

| Source | Teaching purpose and example content |
| --- | --- |
| `exemplar_01_orientation.djot` | Covers, objectives, definitions, roadmaps, sections and subsections, takeaways, and closing slides. |
| `exemplar_02_text_explanations.djot` | Paragraphs, lists, selective emphasis, scientific notation, fixed-width text, hierarchy, and readable density. |
| `exemplar_03_figures_comparisons.djot` | Large figures, native captions, labeled artwork, comparisons, galleries, and purposeful panels. |
| `exemplar_04_data_tables.djot` | Data interpretation, aligned values, meaningful fills, matrices, and stable working tables. Link to the existing full-table demo instead of replacing it. |
| `exemplar_05_equations_worked_examples.djot` | Equations with explanations, intermediate calculations, units, and consistent references. |
| `exemplar_06_questions_sequences.djot` | Full prompts, choices, feedback, progressive explanation, stable geometry, and supported annotation or reveal. |
| `exemplar_07_logistics_study_support.djot` | Agendas, schedules, visible links, citations, references, notes, and optional material. |

About 50-70 slides is an editorial target, not a quota. Keep each deck short and focused on its
teaching purpose.

## Self-contained files

- Keep the seven decks directly in `exemplars/`.
- Add a visual-index `README.md` with deck and page, source path and heading, teaching purpose,
  why the example works, when to choose an alternative, and possible adaptations for every example.
- Copy required local figures into `assets/<deckstem>/` within the exemplar collection.
- Include WebP previews at 90 percent quality.
- Keep teaching cues in `@notes`. Record source and asset provenance, and authoring design
  rationale, externally in the visual index.
- Do not use links to assets, absolute paths, symlinks, or includes that point into course folders.
- Build without private configuration or live fetching.
- Prefix normal output ODP and PDF filenames with `exemplar_`.

## Discovery and preservation

Update the existing README and authoring overview with links to the collection. Keep all originals
and `exemplars/table_styles.djot` unchanged. Retain source content and instructional relationships;
make spacing, wrapping, and layout polish only in exemplar copies.

## Build and review

- Lint and natively build all seven decks using existing repository tools.
- Run LibreOffice outside the sandbox for any build or export that invokes it.
- Inspect every rendered page for readability, aspect ratio, colors, containment, and sequence
  behavior.
- Compare native editability, links, assets, and source, ODP, and PDF visibility counts.
- Have an independent reviewer use the configured agent from
  `~/.codex/agents/image_evaluator.toml` and the rubric in
  [SLIDE_VISUAL_REVIEW_RUBRIC.md](../slide-specs/SLIDE_VISUAL_REVIEW_RUBRIC.md). Fix material
  defects and review affected pages again.
- Verify documentation links, provenance, previews, and build commands.
- Describe animation structure separately from actual playback evidence.
- Keep temporary evidence under root `_temp/exemplars/`.

## Boundaries

- Do not modify original courses or the existing table styles example.
- Do not add engine features or a new framework; existing build tools are sufficient.
- Do not include material whose ownership or provenance is uncertain.

