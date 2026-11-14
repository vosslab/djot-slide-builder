# File structure

## Top-level layout

```text
deck_tools.py        application CLI for build, capacity, import, lint, and visibility
slide_lib/           reusable Djot, native-export, and importer package
svg_tools/           reusable SVG figure authoring tools and examples
genetics/            example and lecture Djot corpus
biotech/             lecture-organized Biotechnology Djot corpus
evergreen/           slides, prompt collections, and assets shared across courses
tests/               fast tests and explicitly separate native E2E runners
docs/                durable project documentation and working plans
devel/               maintainer and repository-engineering helpers
output/              generated presentation products
build_slides.sh      convenience folder-build wrapper
source_me.sh         required local Python environment setup
pip_requirements.txt runtime Python dependencies
Brewfile             declared macOS command-line and desktop dependencies
```

## Key subtrees

- [../svg_tools/](../svg_tools/) creates SVG assets for Djot decks; the
  [SVG toolkit catalogue](SVG_TOOLKIT.md) covers its authoring tools.

- [../slide_lib/](../slide_lib/) contains the application package. Its top-level modules cover the
  command interface, Djot syntax and semantic validation, typed native model, layouts, export,
  LibreOffice conversion, and terminal reporting.
- [../slide_lib/importers/](../slide_lib/importers/) contains the trusted existing-presentation
  import pipeline: ODP reader, source records, geometry and topology analysis, slide
  planning, native normalization, Djot emission, and lossless migration reports.
  `odp_media.py` owns bounded imported-media validation, `odp_tables.py` reconstructs ODF tables,
  `source_regions.py` owns normalized text and visual regions, `source_tables.py` owns source-table
  plans, and `emission_flow.py` owns reading-flow grouping before Djot emission.
  `odp_geometry.py` and `odp_page_objects.py` separate document geometry from page extraction;
  `figure_regions.py`, `multiple_choice_plan.py`, and `emission_topology.py` isolate recognition
  policies from planner and emitter orchestration.
  `image_annotations.py` owns the bounded image-overlay import projection, while `odf_styles.py`
  resolves inherited properties from already-admitted ODF XML.
- Physical measurement is divided among `layout_measurement.py` for text/font metrics,
  `layout_size_selection.py` for fitting, `layout_table_measurement.py` for tables, and
  `layout_flow_measurement.py` for mixed image/text allocation. `table_styles.yaml`,
  `table_styles.py`, and `table_formatting.py` define the validated named-style registry, format
  resolution, and shared cell-formatting records; `odp_text.py` interns equivalent native ODF
  table styles for the document.
- [../slide_lib/make_youtube_slide.py](../slide_lib/make_youtube_slide.py),
  [../slide_lib/refresh_weather.py](../slide_lib/refresh_weather.py),
  [../slide_lib/refresh_podcast.py](../slide_lib/refresh_podcast.py), and
  [../slide_lib/render_tetrad_tables.py](../slide_lib/render_tetrad_tables.py) are reusable
  instructor utility implementations and their supported module command-line interfaces.
- [../genetics/](../genetics/) contains lecture-organized Djot sources. Each `LECT##/` folder owns
  `djot/` canonical sources and adjacent assets plus `old/` original ODP/PDF/ODS evidence. The
  top-level [genetics README](../genetics/README.md) records the corpus inventory.
- [../biotech/](../biotech/) follows the same lecture layout: each `LECT##/` folder owns `djot/`
  sources and assets plus `old/` original decks, PDFs, and course source material. The
  [Lecture 04 review](../biotech/LECT04/djot/LECT04_REVIEW.md) records its conversion scope.
- [../evergreen/](../evergreen/) owns shared announcement groups, the
  [icebreaker catalog](../evergreen/icebreakers.yaml), and their assets, including the recording
  reminder graphic. Fonts remain under `assets/fonts/`. Course-specific
  reusable groups remain in folders such as `genetics/evergreen/`; dated weather and podcast
  snapshots remain with their lecture.
- `genetics/xlect99-template_2023.otp` is the sole master-slide theme authority.
  `presentation_theme.py` validates and reads it; `odp_export.py` projects the compiled physical
  plan directly to editable ODP, and `odp_text.py` writes its editable text objects.
- [../tests/](../tests/) holds permanent offline pytest coverage. The
  [../tests/e2e/](../tests/e2e/) subtree holds non-browser whole-system runners that pytest does
  not collect; [../tests/TESTS_README.md](../tests/TESTS_README.md) explains the test lanes.
- [active_plans/](active_plans/) holds in-flight planning, audit, report, decision,
  and workstream records. It currently retains two Biotechnology Lecture 03 review reports with
  unresolved teaching-content follow-up, tracked in [TODO.md](TODO.md). Completed implementation
  plans and historical evidence live in [archive/](archive/); archived snapshots retain their
  original status text beneath an archive notice. Durable slide specifications live in
  `docs/slide-specs/`; other durable reference docs remain directly under `docs/`.
- [../devel/](../devel/) contains maintainer scripts for cleanup, versioning, changelog work,
  release preparation, and repository mapping. See [../devel/DEVEL_README.md](../devel/DEVEL_README.md).

## Generated artifacts

- `output/` contains generated `odp` and `pdf` presentation products.
  The directory is ignored by Git and is not an authored source. Folder PDF conversion stages a
  complete set below it before replacing published PDFs.
- Imported decks may include genuine source-image assets under an adjacent `assets/` directory. The
  importer validates and publishes only reachable assets with the Djot source. Local deck assets
  may be ignored rather than Git-tracked, including copyrighted images: the Djot lint validates
  their local existence and safe containment, not Git index membership.
- `graphify-out/` contains repository-local Graphify mapping output and is
  ignored by Git.

## Documentation map

- [slide-specs/README.md](slide-specs/README.md) indexes the slide authoring specifications,
  announcement structure, diagram contract, supported syntax, and visual review criteria.
- [slide-specs/COLOR_GUIDE.md](slide-specs/COLOR_GUIDE.md), [slide-specs/VOICE_GUIDE.md](slide-specs/VOICE_GUIDE.md), and
  [slide-specs/PEDAGOGY_GUIDE.md](slide-specs/PEDAGOGY_GUIDE.md) own authoritative slide guidance.
  [slide-specs/AUTHORING_GUIDE.md](slide-specs/AUTHORING_GUIDE.md) is the authoring overview.
- [INSTALL.md](INSTALL.md) states platform requirements and installation commands.
- [USAGE.md](USAGE.md) covers build, import, lint, and authoring workflows.
- [TALKING_POINT_DECK_RECIPE.md](TALKING_POINT_DECK_RECIPE.md) covers recurring annual-source
  Biotechnology study-deck merges, inputs, organization, assets, tools, and review.
- [PIPELINE.md](PIPELINE.md) is the detailed conversion flow and component-ownership reference.
- [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) records settled architecture choices.
- [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md) records durable instructor guidance.
- [PYTEST_STYLE.md](PYTEST_STYLE.md) defines permanent-test boundaries and test commands.
- [ROADMAP.md](ROADMAP.md) and [TODO.md](TODO.md) track remaining work.

## Where to add work

- Add reusable presentation behavior under [../slide_lib/](../slide_lib/), grouping import-specific
  code under [../slide_lib/importers/](../slide_lib/importers/). Put reusable utility logic and
  its supported module command-line interface in `slide_lib/`.
- Add lecture source and associated local assets under the matching lecture folder, such as
  [../genetics/LECT04/djot/](../genetics/LECT04/djot/) or
  [../biotech/LECT04/djot/](../biotech/LECT04/djot/). Keep original presentation evidence in that
  lecture's `old/` folder.
- Add durable behavior tests under [../tests/](../tests/) and whole-system acceptance runners under
  [../tests/e2e/](../tests/e2e/).
- Add user and maintainer reference documentation under `docs/`, using the owning
  document's established scope. Add temporary planning material only in the appropriate
  [active_plans/](active_plans/) subtree.
- Add repository-engineering helpers under [../devel/](../devel/) and keep primary user workflows
  behind [../deck_tools.py](../deck_tools.py).
