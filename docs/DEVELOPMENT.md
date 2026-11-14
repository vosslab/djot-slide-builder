# Development workflow

This guide helps maintainers change the Djot slide builder while preserving its single authored-source
model and native editable outputs. It complements the canonical repository, Python, Markdown, and
pytest rules rather than repeating them.

## Start a maintainer session

- Work from the repository root and use the required Python environment for general repository work:

  ```bash
  source source_me.sh && python3 <command>
  ```

- Inspect the affected owner before changing it. The [pipeline map](PIPELINE.md) identifies the
  parser, import, layout, export, and terminal-output boundaries.
- Treat `.djot` files and their reachable local assets as authored inputs. ODP and PDF files
  are reproducible products; repair the source or its generator instead of editing a generated deck.
- Record an intentional source, interface, or validation change in [CHANGELOG.md](CHANGELOG.md).
  Put human requirements in [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md) and settled technical choices in
  [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md).

## Make and check a focused change

1. Lint the relevant Djot source before an export:

   ```bash
   source source_me.sh && python3 deck_tools.py lint path/to/deck.djot
   ```

2. Build the smallest affected deck in the format needed for the check:

   ```bash
   source source_me.sh && python3 deck_tools.py build path/to/deck.djot --format odp
   ```

3. Run the focused pytest module, then the fast lane when the change is ready:

   ```bash
   source source_me.sh && python3 -m pytest tests/test_<topic>.py -q
   source source_me.sh && python3 -m pytest tests/ -q
   ```

4. Inspect changed files before handoff. For SVG work, use direct Python to check whitespace and
   changed documentation links; do not invoke Git or `source_me.sh`.
   [TROUBLESHOOTING.md](TROUBLESHOOTING.md) covers current failure recovery;
   [GATE_AUDIT.md](GATE_AUDIT.md) retains historical gate-removal decisions.

For SVG work, use direct Homebrew Python and the focused test lane instead of the bootstrap above:

```bash
PYTHONPATH="$PWD:$PWD/tests" MPLCONFIGDIR="$PWD/_temp/mplconfig" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest tests/test_<svg_topic>.py
```

Use `PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B` for SVG scripts, and set
`MPLCONFIGDIR="$PWD/_temp/mplconfig"` when plotting. Keep temporary review artifacts in `_temp/`.

The permanent suite establishes fast, deterministic source and native-object behavior. Follow
[PYTEST_STYLE.md](PYTEST_STYLE.md) to decide whether new coverage belongs there; use the separate
acceptance lanes for real LibreOffice conversion, strict native Djot validation, and rendered review.

Layout regressions are grouped by responsibility:

- [../tests/test_layout_engine.py](../tests/test_layout_engine.py): source preservation, capacity
  diagnostics, and teaching-layout semantics.
- [../tests/test_layout_tables.py](../tests/test_layout_tables.py): table sizing, grouped reveals,
  spans, and native cell formatting.
- [../tests/test_layout_text.py](../tests/test_layout_text.py): links, citations, and text wrapping.
- [../tests/test_layout_media.py](../tests/test_layout_media.py): images, captions, mixed content,
  and question/answer separation.

Use `tests/_temp/` for temporary pytest checks, then promote or delete them before handoff.
Lecture-specific counts, rebuild comparisons, and rendered acceptance checks stay task evidence;
they do not become permanent tests or fixtures. Keep renders and review artifacts in root `_temp/`.

## Validate a presentation change

Use `deck_tools.py` as the application front door. Build a folder only when the change requires
cross-deck coverage:

```bash
./build_slides.sh genetics
```

The same folder wrapper can target one lecture, for example `./build_slides.sh genetics/LECT04/`.

The folder wrapper delegates to `deck_tools.py build --format all`, producing editable ODP followed
by an ODP-derived PDF. Inspect each artifact for the question at hand: semantic tests do not
prove visual containment, and a rendered page does not prove editability. The [pipeline verification
lanes](PIPELINE.md#verification-lanes) define the evidence each check establishes.

When changing import behavior, begin with a trusted ODP input and review the emitted Djot and local
assets before treating them as canonical. Save legacy PPTX as ODP in LibreOffice first. ODP imports
read bounded native ODF facts directly. The supported command shapes and native-lint option are in
[USAGE.md](USAGE.md); importer ownership and publication constraints are in
[PIPELINE.md](PIPELINE.md).

## Review rendered teaching pages

Use [slide-specs/SLIDE_VISUAL_REVIEW_RUBRIC.md](slide-specs/SLIDE_VISUAL_REVIEW_RUBRIC.md) on demand after a presentation
change that may affect classroom clarity, hierarchy, or visual balance. Generate each review page by
building editable ODP and letting LibreOffice create its PDF. Standalone review uses the generated
PDF page. Migration review pairs the original PDF page with its corresponding LibreOffice-generated
PDF page and records functional visual equivalence as `improved`, `roughly equivalent`, or
`materially worse` with a visible teaching reason.

Record the qualitative concern and specific reason first, then use the advisory total band to select
follow-up. The rubric gives 18--20 as generally strong, 15--17 as contextual review, and 0--14 as
advisory visual attention. A small disposable paired-PDF check is the next calibration step for
migration-category repeatability; it belongs with rendered-review evidence rather than the permanent
offline test suite.

## Maintain repository tooling

- Run refresh utilities with `python3 -m slide_lib.refresh_weather` or
  `python3 -m slide_lib.refresh_podcast` after sourcing the environment. Reusable refresh and
  generation code belongs in `slide_lib/`; tests import those owning modules directly.
- Keep temporary verification in `_temp/`. Use in-memory `compile()` for syntax-only checks:
  `py_compile` and `compileall` explicitly write bytecode despite `PYTHONDONTWRITEBYTECODE=1`.
- Run `tests/test_markdown_links.py` for GitHub-browsable documentation and
  `tests/test_djot_links.py` for locally available slide assets and hyperlinks. Ignored teaching
  images remain outside Git; source-only checks do not establish rendered layout or playback.
- Split source modules by responsibility before reaching the 1,000-line limit. The advisory band
  begins at 900 lines. Update callers to the new owners rather than adding re-export facades.
- Use `devel/` for repository engineering commands. [devel/DEVEL_README.md](../devel/DEVEL_README.md)
  documents Graphify mapping and its generated, untracked `graphify-out/` data.
- Preview a version or release operation before it writes changes:

  ```bash
  source source_me.sh && python3 devel/bump_version.py --help
  source source_me.sh && python3 devel/make_release.py --dry-run
  ```

- `devel/clean_build.sh` removes build and test output while retaining installed dependencies.
  `devel/dist_clean.sh` also removes dependency installs and is appropriate only when that wider
  cleanup is intended.
- Keep new maintainer scripts small and place reusable application behavior in `slide_lib/`. The
  placement and source-size rules live in [REPO_STYLE.md](REPO_STYLE.md#scripts-and-executables).

## Useful routes

- [INSTALL.md](INSTALL.md) - dependency and platform prerequisites.
- [USAGE.md](USAGE.md) - build, import, lint, and visibility commands.
- [PIPELINE.md](PIPELINE.md) - architecture, import contract, and evidence lanes.
- [PYTEST_AUTHORING_GUIDE.md](PYTEST_AUTHORING_GUIDE.md) - implementation patterns after the pytest
  policy approves a permanent test.
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - recovery paths for common local failures.
