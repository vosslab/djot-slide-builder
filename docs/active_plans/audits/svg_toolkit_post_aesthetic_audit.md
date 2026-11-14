# SVG toolkit post-aesthetic audit

The 2026-11-14 pruning and six-pass audit are complete. No high or blocking finding was
identified. Findings below distinguish current risks from findings corrected during closeout.
The earlier artwork and native-proof evidence remains in
[SVG_AESTHETIC_UPGRADE_REPORT.md](../../SVG_AESTHETIC_UPGRADE_REPORT.md).

## Findings

### Medium: gallery failure coverage

- **Evidence:** The retained `tests/test_svg_gallery_state.py` exercises successful output;
  `svg_tools/examples/build_gallery.py` restores the working directory in `finally`, but pruning
  removed the failure-path assertion. The completed plan's M2 addressed a demonstrated state leak.
- **Impact:** A regression in cleanup after a failed recipe could affect later relative paths
  without failing the retained test. A temporary sentinel probe passed: the same exception
  propagated and the caller's working directory was restored. The probe code was removed.
- **Smallest fix proposed:** With approval, add one lean failure-path test using separate temporary
  caller and gallery directories, a sentinel recipe failure, and test-owned cleanup. Assert the
  exception and restored working directory. Do not restore the earlier mock-heavy renderer and
  module-state checks. This is the sole permanent-test proposal: it protects a demonstrated leak
  and stable process-state boundary, is not covered by the retained success test, needs only one
  offline failure case, and a failure directs the maintainer to restore `finally` cleanup. No
  permanent test was added in this audit.

### Medium: completed plan location

- **Evidence:** [svg_aesthetic_plan.md](../active/svg_aesthetic_plan.md) and
  [svg_aesthetic_progress.md](../active/svg_aesthetic_progress.md) record completed milestones
  but remain in the active-plan directory. Repository guidance calls for completed records to be
  archived using Git.
- **Impact:** Their location can suggest work is still active despite their `DONE` status.
- **Disposition:** Administrative finding remains open under the explicit Git-free restriction.
  Keep the paths and links intact; archive them and update links when that workflow is authorized.

### Medium: original deck snapshot ownership

- **Evidence:** [original_deck_facts.json](../../../tests/original_deck_facts.json) has no current
  test or production consumer. The [archived plan](../../archive/abundant-painting-bird.md)
  describes it as durable original-source evidence for an earlier parity runner.
- **Impact:** Its location under tests can imply coverage that does not exist. It is historical
  evidence, not an active fixture or proof of parity; keeping it provides no runtime savings.
- **Disposition:** Legacy review proposed retiring the snapshot or restoring parity; Test review
  favored preserving its provenance while removing its apparent active-test role. The decision is
  to preserve the existing file as historical evidence, without restoring a parity gate or moving
  or deleting it under the Git restriction.

### Low: serialized table heights

- **Evidence:** The removed row-height serialization test was not fully duplicated by retained
  compiled-geometry assertions. A temporary real ODP serialization probe measured short and long
  body rows at 1.689806 and 10.219972 cm, respectively, matching compiled heights to within
  0.000001 cm. The probe and ODP were removed.
- **Impact:** No retained owned assertion directly gates serialized `style:row-height`; the probe
  establishes current serialization, not future protection or LibreOffice layout.
- **Disposition:** Record this coverage loss; no second permanent test is proposed.

### Corrected findings

- **Medium, Style:** The direct curve example wrote a generated SVG beside its source. Its default
  and docstring now point to root `_temp/`, documentation agrees, and the misplaced artifact was
  removed. The gallery keeps its explicit path. A direct invocation confirmed the new output.
- **Low, Test:** Duplicate capacity and notes checks, incidental decorative and style-count
  assertions, and a fixed-segment contour oracle were removed. Semantic checks remain; direct
  contour-contact and recipe-inventory assertions were lost.
- **Low, Legacy:** The uncalled private `_source_runs()` helper was deleted without replacement.
- **Low, Comment:** Required function separators were restored in changed test modules.
- **Low, Docs:** The current changelog entry was refiled under its canonical category.

All six passes raised findings: Plan and Test independently identified the same gallery gap;
Style found the generated-output location; Docs found the plan location and changelog category;
Legacy found snapshot ownership and dead code; Comment found missing separators. Other reviewed
areas had no established finding. The audit made no artwork geometry changes and removed no
production dependency.

## Pruning and retained protection

All-owned inventory changed from 61 to 59 modules, 335 to 303 test definitions, and 7,443 to
7,020 lines: 32 definitions, two modules, and 423 net lines removed across 21 modified and two
deleted files. These are definitions and lines, not collected case counts. The eligible boundary
excludes two Git-dependent propagated-hygiene integrations (four definitions, 186 lines): 59 to
57 modules, 331 to 299 definitions, and 7,257 to 6,834 lines. It includes two E2E pytest modules
and a standalone E2E runner, none run in this check.

The smaller suite reduces duplicate setup, implementation-specific assertions and maintenance
constraints; raw count alone does not establish better coverage or a meaningful speedup. Retained
checks cover authored Djot syntax, input safety, source-preserving import/export, scientific
contracts, SVG topology and references, and the required MathJax minimum. The removal also loses
specific checks, including gallery failure cleanup, serialized row height, fixed-segment contour
contact, exact mocked conversion command behavior and the exact xmldom override. The membrane
anchor test does not itself prove gap rendering. No new permanent tests were added.

## Verification and limits

The final direct Python 3.12 `-B --noconftest` run passed 476 cases in 4.84 seconds across 55
owned top-level modules; the slowest case took 0.14 seconds. Converter-boundary commands ran
outside the sandbox. The following explicit selection reproduces that scope, subject to normal
fixture and environment requirements:

```sh
PYTHONPATH="$PWD:$PWD/tests" MPLCONFIGDIR="$PWD/_temp/mplconfig" \
  /opt/homebrew/bin/python3.12 -B -m pytest --noconftest \
  tests/test_course_links.py \
  tests/test_djot_audit.py \
  tests/test_djot_includes.py \
  tests/test_djot_parser.py \
  tests/test_djot_slide_lint.py \
  tests/test_emission_component_geometry.py \
  tests/test_fix_ascii_compliance.py \
  tests/test_footer_topology.py \
  tests/test_image_area_audit.py \
  tests/test_image_covers.py \
  tests/test_layout_engine.py \
  tests/test_layout_media.py \
  tests/test_layout_tables.py \
  tests/test_layout_text.py \
  tests/test_libreoffice.py \
  tests/test_make_youtube_slide.py \
  tests/test_math_layout.py \
  tests/test_mathjax_dependency.py \
  tests/test_metafile_svg.py \
  tests/test_multiple_choice_visual_region.py \
  tests/test_native_export.py \
  tests/test_odp_export.py \
  tests/test_odp_reader.py \
  tests/test_odp_table_import.py \
  tests/test_odp_to_djot.py \
  tests/test_presentation_theme.py \
  tests/test_refresh_podcast.py \
  tests/test_refresh_weather.py \
  tests/test_slide_planning.py \
  tests/test_svg_and_definition_contracts.py \
  tests/test_svg_annotations.py \
  tests/test_svg_binding.py \
  tests/test_svg_cells.py \
  tests/test_svg_chromosomes.py \
  tests/test_svg_curves.py \
  tests/test_svg_drawing.py \
  tests/test_svg_gallery_state.py \
  tests/test_svg_gene_features.py \
  tests/test_svg_gene_tracks.py \
  tests/test_svg_icons.py \
  tests/test_svg_import.py \
  tests/test_svg_membranes.py \
  tests/test_svg_organelles.py \
  tests/test_svg_parts.py \
  tests/test_svg_phenotypes.py \
  tests/test_svg_placement.py \
  tests/test_svg_plots.py \
  tests/test_svg_proteins.py \
  tests/test_svg_signaling.py \
  tests/test_svg_style.py \
  tests/test_svg_text.py \
  tests/test_svg_text_extract.py \
  tests/test_table_styles.py \
  tests/test_terminal_output.py \
  tests/test_tetrad_svg_tables.py
```

Pyflakes passed for all `svg_tools` and 21 modified test files. Earlier focused checks passed
164 cases after test cleanup and 16 after code cleanup, with pyflakes clean. The content baseline
had 174 passes and one fixture failure because its symlink target was still inside the actual
repository; the fixture was corrected to establish its own repository boundary, and the final
safe content lane passed 173 cases. This was not a product defect. Vendored hashes were unchanged.

The full base and hygiene suite, real LibreOffice conversion, E2E runners, full consumer decks,
live Zoom and interactive Impress were not checked in this audit. The previous native and visual
reviews are historical evidence, not fresh results here.
