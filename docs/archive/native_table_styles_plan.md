# Plan: Themed native tables with simple authoring and verified ODP output

> Status: This approved plan is a planning snapshot. See the [progress ledger](native_table_styles_progress.md)
> and [dated results](native_table_styles_results.md) for current implementation and verification status.

## Context

The goal is simple Djot authoring that produces attractive, theme-consistent, native editable tables. The backend may use dedicated models, style resolution, measurement, and ODF serialization wherever these improve reliability and maintainability.

The surveyed teaching corpus contains **421 native tables**, overlapping with **96 flagged slides** requiring table repairs. Refresh these counts before migration.

A baseline check on the installed **LibreOffice 26.2.7.3, build 08dfbf04dcac895fc3a8d30dbf5a00de1b9dda5e**, established:

- Two generated native tables retained all 53 cells and their horizontal merges through ODP -> FODP -> ODP.
- Before/after PDFs rendered identically at the checked resolution.
- LibreOffice consolidated 53 cell-style definitions into seven and normalized formatting into its own property structures.

This verifies the existing native-table foundation. New per-side borders, reusable styles, and edit/resize behavior still require a focused implementation experiment.

## Objectives

- Give ordinary tables attractive defaults with no styling markup.
- Provide named styles and occasional local overrides for specialized teaching needs.
- Produce reliable, native editable ODP tables and matching PDFs.
- Repair flagged tables and review native tables throughout the teaching corpus.
- Deliver an authoring guide and a maintained production demonstration deck.

## Design philosophy

Optimize authoring simplicity and rendering quality. Keep backend responsibilities clear, while allowing the complexity needed for correct native output.

Use CSS terminology as a small authoring vocabulary. The internal representation describes resolved appearance and geometry independently of CSS.

Apply the repository's **Use the scientific method** and **Fix the design, not the symptom** principles: investigate native LibreOffice behavior before finalizing the adapter, then refine visual designs through rendered comparisons.

## Scope

- Survey existing native tables, including hidden slides and shared sources.
- Implement shared styles, reliable automatic formatting, and local overrides.
- Coordinate style resolution, measurement, native ODF formatting, and import.
- Verify practical behavior with the installed LibreOffice.
- Migrate the corpus, repair the 96 flagged table cases, and publish documentation and demonstration artifacts.

## Non-goals

- Change SVG tables, artwork, or their generators.
- Add image-in-cell support, general CSS selectors, or browser rendering.
- Repair unrelated drawings, reveals, or lecture prose.
- Rewrite scientific content, remove rows, or split source slides.
- Translate Impress edits back into Djot.

## Architecture boundaries and ownership

### Djot authoring

Ordinary tables receive the course-themed default automatically. Specialized treatments require one designation:

```djot
{table-style=working}
| Stage | Count |
| --- | --- |
| Observed | 980 |
| Total | [1,000]{border-top="1pt solid #24578F"} |
```

Retain the useful existing forms: `background-color`, `text-align`, `colspan`, `column-widths`, and `table-group`.

Add named styles, individual borders, padding, and vertical alignment. Keep whole-cell overrides local to the affected cell.

Precedence remains:

**theme defaults -> named style and region rules -> table attributes -> cell attributes**

Preserve existing inline text formatting independently.

### Backend data flow

Use this ownership chain:

**Djot content and overrides -> resolved table/cell formatting -> measured table geometry -> native ODF styles and objects -> editable ODP -> LibreOffice PDF**

The internal model carries concrete fills, four borders, padding, alignment, resolved text formatting, spans, and final geometry. ODF serialization does not reinterpret style names or choose new formatting.

Consolidate current scattered defaults. The pre-production codebase permits direct changes to internal records and callers without compatibility wrappers.

### Native ODF translation

The writer already emits a `draw:frame` containing a native `table:table`, column and row definitions, cells, covered positions, and editable paragraphs.

Extend those existing structures. The practical mapping must distinguish:

| Concern | Export responsibility |
| --- | --- |
| Table placement | Native drawing frame and measured table dimensions. |
| Column widths and row heights | Column/row styles referenced by the table grid. |
| Fills, padding, vertical alignment | Cell-style properties using the representation proven with installed Impress. |
| Individual borders | Cell-style border properties, including neighboring and merged-cell interactions. |
| Horizontal alignment | Paragraph formatting inside native cells. |
| Fonts and emphasis | Resolved paragraph/run formatting, preserving mixed inline content. |
| Merges | Native span attributes and covered grid positions. |

Actual LibreOffice-saved files guide the compatibility profile. Observed native files place some borders in paragraph properties within cell styles, and padding/alignment in drawing properties. The existing writer's table-cell properties also survived the baseline save.

The implementation experiment compares extending the existing representation with LibreOffice's normalized representation. Keep the existing approach if it behaves correctly; otherwise adopt the native representation that passes the same checks. Avoid duplicating properties across multiple locations without evidence that both are needed.

### Native style sharing

Reusable Djot presets need not correspond one-to-one with Impress's Table Design presets.

Use a document-scoped style registry keyed by formatting family and effective properties. Equivalent cell formatting shares one native style; local overrides create distinct styles only when their appearance differs.

Apply the same approach to table-related paragraph, text, and dimension styles where duplication occurs. Keep style identifiers separate from object identities.

Sharing must preserve independent editing: changing one cell in Impress must not unexpectedly change other cells sharing its generated style.

### Measurement consistency

Resolve formatting before fitting tables.

For each candidate text size:

- Measure the actual styled content, including bold totals, scripts, and equations.
- Compute usable cell space from column widths, spans, resolved padding, border insets, and the existing text clearance.
- Derive row heights from the measured content.
- Pool grouped-column requirements using those same effective properties.
- Store final geometry for export and equation positioning.

Centralize unit conversion and cell-content inset calculations. Calibrate border occupancy and LibreOffice's rounding through the native experiment rather than assuming browser box-model behavior.

Table-frame dimensions, row heights, and equation placement must agree. Investigate Impress row stretching and ordinary editing before changing the current row-height policy.

### Structural defaults and teaching roles

Use reliable existing facts:

- Headers come from authored header structure.
- Plain numeric cells receive numeric alignment, subject to explicit overrides.
- Existing total-label recognition handles `Total`, `Totals`, and `Grand total`.
- Appropriate named styles can designate first-column row headings.
- Matrix treatments use corresponding row/column labels, including observed cropped axes.

Document role-rule ordering. Ambiguous cases use explicit formatting rather than speculative classification. Never infer scientific identity from a matching letter, discard matrix values, or infer missing distances.

Role recognition happens during the build; ODP contains its resulting native formatting.

### Visual design

Explore noticeably different treatments using representative tables: open horizontal rules, restrained grids, and stronger grouping of sections or headings.

Consider hierarchy, spacing, numeric alignment, totals, and teaching highlights. The seven proposed treatments remain prototypes:

`standard`, `comparison`, `working`, `testcross`, `punnett`, `matrix-lower`, and `matrix-upper`.

Retain separate treatments where they support different teaching jobs. Merge or revise them when rendered evidence supports a more coherent family.

Apply the updated slide specifications:

- Prefer instructor-authored originals and cleaned examples as design references.
- Preserve instructional colors independently of course decoration.
- Keep default headers black on light course-colored fills; explicit fills do not automatically recolor text.
- Review related teaching slides together, preserving recognizable workspaces, reference rows, masks, and classifications.
- Use the existing visual rubric as advisory review without numerical build gates.

### Import repair

Preserve intentional blanks, horizontal spans, fills, borders, alignment, widths, and scientific notation.

Read the property locations actually used by source ODPs, including inherited formatting. Suppress same-frame bitmap previews only when a usable native table has been emitted.

Keep unrelated pictures and separate replacement reasons. Clear a marker only after the table passes comparison and no other blocker remains.

### Mapping (milestones -> components)

- M1 owns corpus evidence and source references.
- M2 owns native feasibility, the style contract, resolution, measurement, export, visual design, documentation, and demonstration.
- M3 owns importer repair and corpus adoption.
- M4 owns final reconciliation and verification.

Each task has one owner, a reviewable result, and an independent verification step. Parallel work uses disjoint source ownership.

### File scope

- Add the shared registry and resolver under `slide_lib/table_styles.*`.
- Update existing parser, table records, measurement, layout construction, ODF serialization, and importers.
- Update course Djot sources and meaningful contract tests.
- Add `docs/slide-specs/TABLE_AUTHORING_GUIDE.md`.
- Add the maintained source deck `exemplars/table_styles.djot`.
- Update syntax, documentation navigation, architecture guidance, and changelog.

Use safe YAML loading and existing source-located validation conventions. Load shared definitions once per compilation.

## Milestone plan

| M | Title | Summary | Goal |
| --- | --- | --- | --- |
| M1 | Corpus baseline | Refresh inventory, select source references, and identify actual layout limitations. | Establish evidence without treating provisional imports as design authority. |
| M2a | Native implementation experiment | Carry one named style and local overrides through a representative table, installed LibreOffice, save/reopen, and PDF export. | Resolve the ODF compatibility profile before broad implementation. |
| M2b | Style model and authoring | Implement validated shared definitions, overrides, role recognition, and resolution using the demonstrated architecture. | Establish the complete authoring contract. |
| M2c | Measurement | Integrate resolved formatting into widths, row heights, fitting, groups, and equation placement. | Use one consistent geometry model. |
| M2d | Native serialization and sharing | Complete ODF property emission and document-scoped style reuse. | Preserve formatting and independent editability without redundant styles. |
| M2e | Visual family, guide, and demo | Compare visual alternatives, refine treatments, draft the guide, and build the production demo. | Demonstrate the final design and authoring workflow before migration. |
| M3a | Import repair | Preserve source table formatting and safely suppress duplicate previews. | Produce complete native tables from representative flagged sources. |
| M3b | Corpus adoption | Apply appropriate treatments and complete table repairs throughout the surveyed corpus. | Account for every table and remaining non-table blocker. |
| M4 | Final verification | Reconcile content, inspect renders, verify editing, run checks, and finalize documentation and artifacts. | Deliver verified tables, guide, demo source, ODP, and PDF. |

Dependencies: M2a follows M1. M2b follows the experiment; M2c and M2d use the established model and may proceed independently with coordinated interfaces. M2e follows working measurement and serialization. M3 follows the demonstrated visual family. Existing-table adoption can proceed alongside importer repairs; affected flagged slides follow the repaired import path.

Parallel-plan ready: **yes once the native profile and shared model are established**.

## Native implementation experiment

Use root `_temp/` and the installed LibreOffice through repository scripts, outside the sandbox.

The representative table includes:

- One named style applied to repeated cells.
- Individual borders, including explicit `none` beside inherited borders.
- Fills, asymmetric padding, horizontal and vertical alignment.
- A merged heading, numeric values, and wrapping text.

Verify generated ODP, LibreOffice-saved ODP, and corresponding PDFs. Inspect native objects, style references, values, dimensions, and visible formatting.

Perform actual edits on a temporary copy: change cell text, fill, and a border; resize the table; save and reopen. Confirm that other cells retain their formatting and the table remains native. Record ordinary row-height behavior and any manual resizing needed for longer text.

Core fills, solid/absent side borders, padding, alignment, and spans must work before migration. Investigate dashed/dotted borders in the same experiment; publish them only if their appearance survives reliably. Unsupported values must produce clear errors rather than silently changing appearance.

This is implementation evidence within M2, not a separate approval gate. Failures direct changes to the native adapter or measurement model.

## Production demo and authoring documentation

The demo is a maintained production artifact, separate from temporary design experiments.

Its normal build produces:

- `output/odp/table_styles.odp`
- `output/pdf/table_styles.pdf`

Include these outputs in the production artifact handoff, following repository policy for generated files. Keep the Djot source versioned and update it whenever supported table styles or capabilities change.

Demonstrate every shipped style and author-facing capability, including local borders, fills, padding, alignment, merged headings, totals, widths, grouped question/answer tables, matrices, wrapping, and scientific notation.

Keep the deck readable and useful as a visual reference, with brief native captions identifying each feature.

The authoring guide is an explicit M2 deliverable, verified in M4. It provides:

- A minimal default-table quick start.
- Style selection with rendered examples.
- Copyable teaching-table recipes.
- Local overrides, semantic colors, column sizing, and stable sequences.
- A small reusable-style definition and precedence explanation.
- Troubleshooting and the boundary for SVG artwork.

Use the production demo as the source for documentation illustrations. The syntax reference owns exact property rules. Link the guide and demo from the existing authoring documentation.

## Test and verification strategy

- Retain focused tests for validation, precedence, reliable role recognition, matrix ambiguity, spans, shared styles, and preservation of authored formatting.
- Check agreement among measurement, native properties, and rendered results for dense, wrapping, merged, and equation-bearing tables.
- Verify representative imported tables and preview suppression.
- Compare migrated values, ordering, spans, and instructional colors.
- Review native-table slides and teaching sequences in ODP-derived PDFs; enlarge ambiguous cases and review normal presentation readability.
- Verify actual edit/save/reopen behavior separately from XML structure and headless conversion.
- Run focused checks, documentation links, lint, and the base suite. Keep permanent tests behavior-focused.
- Build and review the maintained demo through the normal Djot -> ODP -> PDF workflow.
- Keep exploratory comparisons temporary; retain the demo source and useful documentation images.

## Assumptions and material risks

- The installed LibreOffice and practical ODP behavior are the primary compatibility evidence.
- Refresh corpus counts before migration; count the demonstration separately from teaching tables.
- Native editability includes cell formatting and table resizing. Arbitrary added text may require normal manual resizing in Impress.
- Equation rendering retains its established exception to native editable text.
- Recheck Biotechnology LECT10 source blockers and report any resulting verification limits.
- Refresh files before editing to respect concurrent work and Synology synchronization.

At plan approval: Only the existing-table baseline had been built and checked. The new style system, per-side overrides, edit/resize experiment, and production demo remained implementation work.
