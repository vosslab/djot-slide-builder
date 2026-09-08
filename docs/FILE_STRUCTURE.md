# File structure

## Top-level layout

```text
deck_tools.py        application CLI for build, import, lint, and visibility
slide_lib/           reusable Djot, native-export, and importer package
genetics/            example and lecture Djot corpus
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

- [../slide_lib/](../slide_lib/) contains the application package. Its top-level modules cover the
  command interface, Djot syntax and semantic validation, typed native model, layouts, export,
  LibreOffice conversion, and terminal reporting.
- [../slide_lib/importers/](../slide_lib/importers/) contains the trusted existing-presentation
  import pipeline: ODP/PPTX readers, source records, geometry and topology analysis, slide
  planning, bounded region rendering, and Djot emission.
- [../genetics/djot/](../genetics/djot/) contains the repository's Djot lecture sources and its
  local authoring README. A deck-local asset tree is created beside an imported deck when needed.
- [../tests/](../tests/) holds permanent offline pytest coverage. The
  [../tests/e2e/](../tests/e2e/) subtree holds non-browser whole-system runners that pytest does
  not collect; [../tests/TESTS_README.md](../tests/TESTS_README.md) explains the test lanes.
- [active_plans/](active_plans/) holds in-flight planning, audit, report, decision,
  and workstream records. Durable policy and architecture documents remain directly under
  `docs/`.
- [../devel/](../devel/) contains maintainer scripts for cleanup, versioning, changelog work,
  release preparation, and repository mapping. See [../devel/DEVEL_README.md](../devel/DEVEL_README.md).

## Generated artifacts

- `output/` contains generated `pptx`, `odp`, and `pdf` presentation products.
  The directory is ignored by Git and is not an authored source.
- Imported decks may include local PNG assets under an adjacent `assets/` directory. The importer
  validates and publishes only reachable assets with the Djot source.
- `graphify-out/` contains repository-local Graphify mapping output and is
  ignored by Git.

## Documentation map

- [INSTALL.md](INSTALL.md) states platform requirements and installation commands.
- [USAGE.md](USAGE.md) covers build, import, lint, and authoring workflows.
- [PIPELINE.md](PIPELINE.md) is the detailed conversion flow and component-ownership reference.
- [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) records settled architecture choices.
- [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md) records durable instructor guidance.
- [PYTEST_STYLE.md](PYTEST_STYLE.md) defines permanent-test boundaries and test commands.
- [ROADMAP.md](ROADMAP.md) and [TODO.md](TODO.md) track remaining work.

## Where to add work

- Add reusable presentation behavior under [../slide_lib/](../slide_lib/), grouping import-specific
  code under [../slide_lib/importers/](../slide_lib/importers/).
- Add lecture source and associated local assets under a topic directory such as
  [../genetics/](../genetics/).
- Add durable behavior tests under [../tests/](../tests/) and whole-system acceptance runners under
  [../tests/e2e/](../tests/e2e/).
- Add user and maintainer reference documentation under `docs/`, using the owning
  document's established scope. Add temporary planning material only in the appropriate
  [active_plans/](active_plans/) subtree.
- Add repository-engineering helpers under [../devel/](../devel/) and keep primary user workflows
  behind [../deck_tools.py](../deck_tools.py).
