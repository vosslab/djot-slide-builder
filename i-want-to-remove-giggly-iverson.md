# Make the fork Djot-first

## Context

`djot-slides` is a fork of `marp-slides`, pre-production, with no users. It carries two source
languages -- canonical Marp Markdown and extended-Djot -- feeding one format-neutral backend
(`native_model` -> `layouts` -> python-pptx -> LibreOffice ODP -> PDF).

**Goal, in the user's words: make the fork Djot-first; remove Marp and remove legacy compatibility.**

Build the architecture this project would have if it were written today as a Djot slide system with a
legacy-deck importer. The Djot language and the semantics of the imported deck are the sources of
truth. Existing code, tests, and example decks are evidence of the current implementation; keep what
belongs in the Djot-first design.

Exploration turned up a concrete reason this matters. `slide_lib/importers/pptx_to_marp.py` is named
for an output format, and the Djot importer reaches into it for two Markdown escapers:

```python
# pptx_to_djot.py:153, 159
line = " | ".join(djot_text(pptx_common.markdown_text(cell)) for cell in cells)
text = djot_text(pptx_common.paragraph_markdown(paragraph))
```

Source text is escaped for Markdown, then escaped again for Djot. Backslashes and HTML entities that
Markdown inserts and `djot_text()` does not reverse land in the generated `.djot` file. Table cells
fare worse: `shape_inventory():263` glues them into a pipe-joined text line with no header and no
separator row, so `djot_blocks.py:391 parse_table` never sees a table -- the structure of the source
slide is destroyed at read time.

`pptx_to_djot.py` also carries its own copies of `ConversionSummary`, `validate_image_blob`,
`image_asset`, `shape_inventory`, `slide_notes`, `extract_slides`, `render_slide`, `convert_pptx`,
and `run_import`. The extraction was forked, not shared; what remains shared is mostly the wrong
half.

Four pieces of work follow from that:

1. A clear ownership boundary: readers extract source facts, emitters render Djot.
2. One extraction path per input format.
3. Djot-first vocabulary in module and identifier names.
4. Marp removed -- format, parser, modules, content, docs, dependencies.

Out of scope: the Djot language itself (see [Language contract](#language-contract)), and layout,
grammar, or pipeline behavior.

## Decisions taken (confirmed with the user)

- Delete every Marp doc outright.
- Delete `genetics/lect01a-course_intro.md`, `genetics/lect01b-genetic_disorders.md`,
  `genetics/assets/`, `themes/genetics.css`.
- Convert `tests/test_marp_export.py` into `tests/test_native_export.py` with Djot fixtures.
- Use plain `mv` / `rm`; review with `git status` / `git diff`. Deliberate exception to the
  `git mv` / `git rm` rule in [docs/REPO_STYLE.md](docs/REPO_STYLE.md),
  approved by the user.
- Importing an instructor's existing `.odp` and `.pptx` decks stays a first-class feature. What is
  being removed is compatibility with the *fork*: Marp-era output shapes, duplicated extraction, and
  naming that marks code as pre-Djot.

## Language contract

Use the current Djot grammar and parser as the language contract for this plan. `djot_parser.py`,
`djot_blocks.py`, `djot_inline.py`, `djot_grammar.py`, and `djot_lint.py` are the specification to
build against.

Pipe tables are part of that contract -- `djot_blocks.py:215 split_table_row` and `:391 parse_table`
implement them, and `genetics/djot/lect02e-restriction_enzymes.djot:412-419` is a real one. So the
importer renders imported tables as Djot pipe tables. Questions about evolving table syntax belong
to a separate language-design task.

Implement this plan in the importer, source-model, emitter, backend, test, content, and
documentation layers.

## Architecture this plan builds

| Layer | Owns |
| --- | --- |
| `importers/source_model.py` | the vocabulary of an imported slide: blocks, table rows and cells, inline runs, images, notes, geometry |
| `importers/pptx_reader.py`, `odp_reader.py` | opening the container, safety validation, and reading raw structured facts out of it |
| `importers/slide_plan.py` and its geometry siblings | turning read geometry into a semantic slide plan and layout choice |
| `importers/djot_emitter.py`, `pptx_to_djot.py`, `odp_to_djot.py` | rendering a plan as Djot: syntax, escaping, links, images, table separators |

Each layer takes its input from the layer above and returns its own vocabulary. Readers return raw
text; the emitter applies `djot_text()` once, at the output boundary.

`source_model.py` mirrors the vocabulary already established in `slide_lib/native_model.py` --
`Table` there carries `headers: tuple[tuple[Inline, ...], ...]` and
`rows: tuple[tuple[tuple[Inline, ...], ...], ...]` (`native_model.py:171-176`), and inline content is
`Text` / `Strong` / `Emphasis` / `Link`. The source model uses the same shapes for the same concepts
so one vocabulary runs through the repo. It stays a separate module: `native_model` is the backend's
post-parse model, and the importer depends on neither the parser nor the backend.

Layout inference currently sits in `pptx_to_marp.py:381 render_slide()`. It belongs in the planning
layer; move it there if a Djot consumer needs its result, otherwise it leaves with the emitter it was
written for.

## Autonomy

Every step is executable by the manager and subagents with no human in the loop. The baseline commit
exists, so `git checkout -- <path>` restores anything at any point.

The implementation stops short of `git commit` --
[docs/REPO_STYLE.md](docs/REPO_STYLE.md) reserves that for the human.
The work reaches a verified, reviewable tree with `docs/CHANGELOG.md` updated and ends there.

If LibreOffice is unavailable, `slide_lib/libreoffice.py` preflight reports it; run the behavioral
acceptance with `-f pptx`, record that the ODP and PDF stages were unverifiable for environment
reasons, and continue.

## Success conditions

| # | Condition | How it is checked |
| --- | --- | --- |
| A | Active files, modules, and symbols use Djot-first names | tracked filenames; `slide_lib/`, `tests/`, `devel/`, root scripts |
| B | `.djot` is the only deck source; dependencies match what is imported | `native_export`, `cli`, `pip_requirements.txt` |
| C | Current documentation describes the Djot-first system | `README.md`, top level of `docs/` |
| D | Readers return raw structured facts; the emitter owns Djot syntax | `pptx_reader.py`, `odp_reader.py`, `source_model.py` |
| E | One extraction path per input format, one source model, one Djot emission path | `slide_lib/importers/` |
| F | An imported deck parses and lints as valid Djot, and its tables are table blocks | round-trip check on a real `.odp` |

Historical records stay as written and are outside A-C: `docs/CHANGELOG.md` (repo style keeps every
entry), `docs/active_plans/decisions/*` (records of how decisions were reached, per
[docs/REPO_STYLE.md](docs/REPO_STYLE.md) -- they hold the provenance of
the Djot decision itself), and the gitignored `OTHER_REPOS/`.

## Step 1a: one extraction path per format

**PPTX.** `pptx_to_djot.py` already holds the more capable extraction -- it owns source regions,
visual inventory, placeholder roles, and connector handling that the Marp copy never received. Keep
that one.

- Create `slide_lib/importers/pptx_reader.py` and move the extraction into it: `shape_inventory`,
  `image_asset`, `slide_notes`, `extract_slides`, `source_text_inventory`, `source_visual_inventory`,
  and the shape-inspection helpers, together with the container-level pieces `validate_pptx`,
  `validate_member_name`, `validate_image_blob`, `image_suffix`, `title_shape_id`,
  `is_subtitle_shape`, `SUPPORTED_IMAGE_SUFFIXES`, `MAX_IMAGE_PIXELS`, and the PPTX archive limits.
- `slide_lib/importers/pptx_to_marp.py` is deleted; its extraction is the copy that goes.
- `pptx_to_djot.py` keeps `ConversionSummary` (a report of one conversion run, not a source fact),
  `djot_text`, and the Djot rendering, and becomes a thin orchestrator over `pptx_reader` ->
  `slide_plan` -> `djot_emitter`. If a large planning function still sits in it after the move, that
  function belongs in the planning layer -- finish the move rather than leaving it half-done.

**ODP.** `odp_to_marp.py` owns `read_slides`, `validate_odp`, `convert_odp_to_pptx`, `SourceSlide`,
`ODP_MIMETYPE`, and `NS`, with no twin anywhere, so it is a rename:

```bash
mv slide_lib/importers/odp_to_marp.py slide_lib/importers/odp_reader.py
```

Keep the reading and validation, let its Marp rendering (`convert_odp`, `run_import`) go, and
rewrite the docstring.

**Source model.** Create `slide_lib/importers/source_model.py` holding the vocabulary readers
produce and emitters consume: `TextBlock`, `ImageAsset`, `SlideData`, and the table and inline types
added in Step 1b. Today these live in a module named for an output format, which is why
`djot_emitter` imports its own domain types from `pptx_to_marp`.

Reconcile the two archive-limit sets while merging: PPTX allows 4000 archive members, ODP 2000.
Where that reflects a real property of the format it stays reader-local with a comment saying why;
otherwise pick one value.

Update every import site:

| File | Reference |
| --- | --- |
| `slide_lib/cli.py` | lines 13, 16 |
| `slide_lib/importers/odp_to_djot.py` | lines 8, 21, 30 |
| `slide_lib/importers/pptx_to_djot.py` | line 26 and its ~30 `pptx_common.` call sites; most become local once extraction moves |
| `slide_lib/importers/legacy_djot_emitter.py` | lines 9, 39, 71, 157 |
| `slide_lib/importers/source_region_render.py` | lines 21-22, 99, 101, 153 |
| `slide_lib/importers/odp_visibility.py` | lines 127-131 (deferred import) |
| `tests/test_odp_to_djot.py`, `test_pptx_to_djot.py`, `test_emission_component_geometry.py`, `test_legacy_slide_visual_planning.py` | type constructions and `ODP_MIMETYPE` |

Use the absolute local-import idiom (`import slide_lib.importers.pptx_reader as pptx_reader`) per
[docs/PYTHON_STYLE.md](docs/PYTHON_STYLE.md).

**Gate:** `source source_me.sh && pytest tests/` passes before Step 1b.

## Step 1b: readers return raw facts, the emitter renders Djot

Three structures to model properly, each replacing a place where output syntax was computed during
reading.

**1. Inline runs.** Add `TextRun` to `source_model.py`: `text: str` holding the characters as they
appear in the source deck, and `link: str` for a hyperlink. `TextBlock.lines` becomes
`tuple[tuple[int, tuple[TextRun, ...]], ...]` -- indent level plus runs.

`paragraph_markdown()` becomes a reader function returning those runs.
The link-scheme allow-list stays in the reader as a security control on source data (keep the ASVS
1.2.2 comment); percent-encoding of `(` and `)` is Djot link syntax and moves to the emitter, which
renders `[text](url)`.

**2. Tables, as first-class source facts.** Add `TableBlock` to `source_model.py`, mirroring
`native_model.Table`:

```python
headers: tuple[tuple[TextRun, ...], ...]              # one cell per column
rows: tuple[tuple[tuple[TextRun, ...], ...], ...]     # rows of cells of runs
left: int
top: int
```

`SlideData` gains a `tables: tuple[TableBlock, ...]` field, so a PPTX or ODP table arrives at the
emitter as rows and cells. The emitter renders a Djot pipe table: leading and trailing pipes, the
header row, and the header-separator row `parse_table` requires, escaping cell text once and
escaping a literal `|` inside cell text so `split_table_row` reads it as content.

Modeling rows and cells directly, rather than a flag on a text block, is what keeps the emitter free
of guesswork about what a line of text was meant to be.

**3. Image references.** `ImageAsset.markdown_path` becomes `asset_path`: it is a POSIX path.
Update `legacy_djot_emitter.py:73, 160` and `pptx_to_djot.py:120, 456`.

With those in place, `djot_text()` applies once, to raw source text, at the Djot output boundary, and
the double-escape at `pptx_to_djot.py:153, 159, 224, 250` is gone. Notes arrive as plain lines rather
than HTML-comment-encoded ones.

**Judge the result against the imported deck and the Djot language.** For an imported deck, ask: does
every slide's text, table, image, and note faithfully represent the source slide, and does the file
parse through `djot_parser.parse_deck()` and lint clean? Answer that directly. A diff against a
pre-change import is a quick way to spot surprises, and nothing more -- the old output came from the
escaping path being replaced.

**Gate:** full `pytest tests/` passes; imported decks lint clean; the Step 1b round-trip invariants
hold.

## Step 1c: Djot-first module names

Every one of these modules lives in `slide_lib/importers/`, which already marks them as handling
imported decks. Drop the redundant prefix:

```bash
mv slide_lib/importers/legacy_slide_plan.py           slide_lib/importers/slide_plan.py
mv slide_lib/importers/legacy_geometry.py             slide_lib/importers/geometry.py
mv slide_lib/importers/legacy_topology.py             slide_lib/importers/topology.py
mv slide_lib/importers/legacy_heading_relation.py     slide_lib/importers/heading_relation.py
mv slide_lib/importers/legacy_new_visual_relations.py slide_lib/importers/visual_relations.py
mv slide_lib/importers/legacy_rotated_vector_label.py slide_lib/importers/rotated_vector_label.py
mv slide_lib/importers/legacy_djot_emitter.py         slide_lib/importers/djot_emitter.py
```

These names are package-scoped and specific to imported-deck planning -- verified: nothing outside
`slide_lib/importers/` imports `legacy_geometry` or `legacy_topology`. `visual_relations` also
retires a self-contradictory name ("legacy new").

Sweep the identifiers the prefix reached:
- Import aliases at `pptx_to_djot.py:23-25` and the ~40 `legacy_*.` call sites that follow.
- `LegacySlidePlan` -> `SlidePlan`.
- The `legacy_blocks` parameter at `pptx_to_djot.py:470, 477, 489` -> `text_blocks`.
- `tests/test_legacy_slide_visual_planning.py` -> `tests/test_slide_visual_planning.py`, plus imports
  in `test_pptx_to_djot.py`, `test_emission_component_geometry.py`, `test_footer_topology.py`,
  `test_multiple_choice_visual_region.py`.

**Vocabulary for prose and docstrings.** An `.odp` or `.pptx` input is an **imported deck**. Reserve
"source" for the authored `.djot`. Update `cli.py:54, 72`, `odp_to_djot.py:1`,
`source_region_render.py:53`, and the `odp_reader.py` docstring from Step 1a.

Mechanical, no behavior change; same `pytest tests/` gate.

## Step 2: remove the Marp front end

```bash
rm slide_lib/marp_parser.py
rm tests/test_marp_parser.py tests/test_odp_to_marp.py tests/test_pptx_to_marp.py
```

`marp_parser.py` is the only consumer of `yaml` and `markdown_it` in the repo (verified by grep
across `slide_lib/`, `tests/`, `devel/`); both dependencies go with it.

## Step 3: `.djot` as the only deck source

**`slide_lib/native_export.py`**
- Rewrite the line 1 docstring for the Djot-first pipeline.
- Remove the `marp_parser` import (19), `MARP_TRUE_PATTERN` (24-27), `has_marp_front_matter()`
  (63-72).
- `parse_deck()` calls `djot_parser.parse_deck()` directly. Retire `PARSER_BY_SUFFIX` -- a one-entry
  dispatch table is a mechanism for a second source language, and reintroducing a table is a
  five-line change if one ever arrives.
- Give suffix admission a single owner: define `SUPPORTED_SUFFIX = ".djot"` once; `validate_input`
  raises on anything else with "input must use the .djot extension", and the folder branch of
  `discover_decks` (92-95) filters on the same constant.

**`slide_lib/cli.py`**
- Drop the imports for the removed Marp routes (13, 16).
- `select_importer` keeps the `.odp` and `.pptx` Djot routes. Retire the `target_format` parameter
  and the `-t/--to` flag (56-57) now that Djot is the only target -- argparse minimalism,
  [docs/PYTHON_STYLE.md](docs/PYTHON_STYLE.md).
- Keep the ASVS 2.2.1 allow-list comment; the suffix allow list remains the control.
- Sweep callers of the retired flag:
  ```bash
  grep -rn "deck_tools\|--to \|-t marp\|-t djot\|target_format" \
    --include='*.py' --include='*.sh' --include='*.md' \
    . --exclude-dir=OTHER_REPOS --exclude-dir=.git --exclude-dir=graphify-out
  ```
  Known hits: `README.md:58`, `docs/USAGE.md:57`, `tests/test_cli.py:35-47`.

**`slide_lib/terminal_output.py`** -- drop the `marp_parser` import (19); `DjotParseError` becomes
the only parse-failure type in the exception tuple (151).

**`slide_lib/layouts.py:990` + `slide_lib/pptx_animation.py:166`** --
`_marp_animation_writer` -> `_slide_animation_writer`, both sites together.

**`slide_lib/layout_validation.py:293`** -- update the comment to describe current reveal handling.

**`build_slides.sh:11`** -- update the help text to describe `.djot` deck discovery.

**`pip_requirements.txt`** -- remove `markdown-it-py[linkify]` and `PyYAML` (4-5), and the
`"markdown_it": "markdown-it-py"` alias at `tests/test_import_requirements.py:50`.
`tests/test_import_requirements.py` keeps every declared pin matched to a real import.

## Step 4: tests at their owning layer

```bash
mv tests/test_marp_export.py tests/test_native_export.py
```

This 802-line file imports only `layouts`, `native_export`, `layout_validation`, `native_model`. Its
41 tests cover layout fit, titleless panels, tables, vertical text direction, gallery, named slots,
multiple-choice popups, missing images, folder discovery, and export staging -- backend behavior,
reached through Marp decks because that was the parser available when they were written.

Rule: **preserve the behavior each test proves, and express that proof at the layer that owns it.**

1. A test proving backend behavior gets its native model constructed directly, so it exercises
   `layouts` and `layout_validation` without a parser in the path.
2. A test proving parser-to-model behavior, source-located errors, or deck discovery keeps a `.djot`
   source and becomes a Djot integration test.
3. A test proving Marp parsing has no subject any more and goes: the `HEADER` constant (line 20), the
   `has_marp_front_matter` monkeypatch block (773-778), the discovery cases about `.md` files
   (461, 762).
4. Write inputs inline, into `tmp_path` at runtime, per the fixture policy in
   [docs/PYTEST_STYLE.md](docs/PYTEST_STYLE.md). A committed
   `tests/fixtures/` directory needs explicit human sign-off and is not warranted here.
   `genetics/djot/lect01a-course_intro.djot` and `tests/test_djot_parser.py` are the syntax
   reference.

The repo limit is 999 lines. Splitting by layer as items 1 and 2 suggest is the natural outcome and
the preferred way to stay inside it.

**Edit**
- `tests/test_cli.py` (13-15, 29-30, 35-47): keep the assertions that `.odp` and `.pptx` route to the
  Djot importer and that an unsupported suffix raises `CliUsageError`.
- `tests/test_terminal_output.py` (17, 47): `.djot` fixture deck; failure path uses `DjotParseError`.
- `tests/e2e/e2e_all_native_layouts.py` (127): `e2e_djot_native_layouts.py` covers the same ground in
  Djot. Diff the two, port any layout case the Djot runner lacks, then retire the Marp one.

**Importer coverage across Step 1.** `test_pptx_to_djot.py`, `test_odp_to_djot.py`,
`test_emission_component_geometry.py`, `test_legacy_slide_visual_planning.py`,
`test_source_region_render.py`, and `test_footer_topology.py` pin extracted geometry, notes,
visibility, and image sets. Step 1 changes how those facts are represented, not what is read, so
those assertions should keep passing once updated for the new types (`TextRun`, `TableBlock`,
`asset_path`).

Assertions on escaped text strings will change, and correctly so. Check each against the imported
deck and update it to the right value. An update that is not obviously right is a finding about the
new escaping path worth investigating.

**Permanent tests added by this plan: two.**
1. `validate_input` rejects a `.md` path -- meaningful because Step 3 makes it the single owner of
   suffix admission.
2. A table imported from a legacy deck parses back as a table block. This is a round-trip invariant,
   the strongest shape in
   [docs/PYTEST_STYLE.md](docs/PYTEST_STYLE.md), and it pins the exact
   defect being fixed. Lives in `tests/test_pptx_to_djot.py`.

Repo-wide name greps stay one-time implementation proofs; see
[One-time checks](#one-time-checks-vs-permanent-tests).

## Step 5: content and theme

Confirm nothing else references these:

```bash
grep -rn "genetics/assets\|themes/genetics\|genetics.css\|lect01a-course_intro.md\|lect01b-genetic_disorders.md" \
  . --exclude-dir=.git --exclude-dir=OTHER_REPOS --exclude-dir=graphify-out --exclude-dir=output
```

Expect hits only in the two `.md` decks, `docs/CHANGELOG.md`, and docs being rewritten anyway. A
reference from a `.djot` deck or from `slide_lib/` is a finding to report.

```bash
rm genetics/lect01a-course_intro.md genetics/lect01b-genetic_disorders.md
rm -r genetics/assets
rm themes/genetics.css
rmdir themes
```

`genetics/assets/` holds the asset trees for those two decks only; the Djot decks use
`genetics/djot/assets/`, which covers all eight lectures. No Python reads `themes/genetics.css`.

## Step 6: documentation

**Remove**

```bash
rm docs/MARP_SYNTAX_GUIDE.md docs/MARP_ADJACENT_PROJECT_COMPARISON.md
rm docs/LAYOUT_LANGUAGE_SURVEY.md docs/RELATED_PROJECTS.md
rm docs/OTHER_REPOS/AWESOME_MARP.md docs/OTHER_REPOS/MARP_CLI.md \
   docs/OTHER_REPOS/MARP_COMMUNITY_THEMES.md docs/OTHER_REPOS/MARP_CORE.md \
   docs/OTHER_REPOS/MARP_DECK_DIRECTORY.md docs/OTHER_REPOS/MARP_SLIDES.md \
   docs/OTHER_REPOS/MARP_SLIDES_TEMPLATE.md docs/OTHER_REPOS/MARP_TO_EDITABLE_PPTX.md \
   docs/OTHER_REPOS/MARP2PPTX.md docs/OTHER_REPOS/MARPX.md \
   docs/OTHER_REPOS/MY_MARP_THEMES.md docs/OTHER_REPOS/PPTX2MARP.md
rm docs/archive/piped-hugging-whale.md docs/archive/sprightly-hugging-stallman.md
rmdir docs/archive
```

The archive files are completed plans for the `marp_lib/` -> `slide_lib/` rename, and they are the
directory's only contents. The other eight `docs/OTHER_REPOS/*.md` review non-Marp projects -- keep
those files and update their incidental mentions.

**Rewrite `README.md`** for the Djot-first system.
- Title `# djot-slides`.
- First paragraph is the GitHub About source: pure prose, under 250 characters, no links or code
  spans, shaped `[what it is] + [who/use case] + [distinctive detail]`.
  `tests/test_readme_first_paragraph.py` enforces this.
- Pipeline diagram (10-18): extended-Djot source.
- Quick start (36-44): `genetics/djot/lect01b-genetic_disorders.djot`,
  `./build_slides.sh genetics/djot`.
- Import section (51-64): the Djot import route.
- Documentation list (66-82): current docs, plus
  [docs/PIPELINE.md](docs/PIPELINE.md) and the Djot syntax reference.

**Update**
- `docs/PIPELINE.md` -- lines 3-5, 23, 28, 45-46, 53, 133, 154-165, 217. The ownership table is the
  natural home for the reader/planner/emitter boundary from this plan; describe it there.
- `docs/DESIGN_DECISIONS.md` -- retire the "Marp is an authoring-language specification" section
  (40-60) and the Marp-parity sections (316-324, 520-533); update mentions at 74, 96, 101, 194, 205,
  278. Keep the `Decision` / `Why` / `Consequence` / `Owner` shape that
  `tests/test_guidance_doc_format.py` checks. Add two decisions: the fork is Djot-first, and readers
  extract while emitters render (`Owner`: `docs/PIPELINE.md`).
- `docs/HUMAN_GUIDANCE.md` -- 24 mentions (15-26, 42-48, 71-93, 137-177). Classify each bullet from
  its surrounding context and act:
  - Guidance that still applies and reads correctly as written -> **keep the wording exactly as it
    is**, including a historical Marp mention. This is the user's own voice.
  - Guidance that still applies but names Marp as the thing to do -> **replace the Marp term with its
    Djot equivalent**, leaving the rest of the sentence intact.
  - Guidance whose subject is the Marp front end -> **remove the bullet**.
  Record each removed and each term-updated bullet in the changelog.
- `docs/USAGE.md` (3, 38, 57, 93), `docs/TODO.md` (3, 40), `docs/ROADMAP.md` (6), `docs/INSTALL.md`,
  `docs/LECTURE_LAYOUT_SURVEY.md` (146).
- `genetics/djot/README.md:4` -- describe the Djot decks as the deck source.
- `tools/TOOLS_README.md` (69, 74-75) -- describes a `marp-slides` tool group and
  `tools.pptx_to_marp` writing into `marp_lib/`, none of which exists, and `tools/` holds only this
  README. Per [docs/REPO_STYLE.md](docs/REPO_STYLE.md), `tools/` holds
  optional user utilities; with none present, remove the README and the directory.

**Keep as written:** `docs/CHANGELOG.md`, `docs/active_plans/decisions/*`, and the gitignored
`OTHER_REPOS/`.

## Step 7: changelog

Add a `## 2026-09-07` block in the standard section order:
- `### Additions and New Features` -- `slide_lib/importers/source_model.py`, `pptx_reader.py`, the
  reader/planner/emitter boundary, and `TableBlock` as a first-class imported-slide fact.
- `### Behavior or Interface Changes` -- `.djot` is the deck source; `deck_tools.py import` always
  emits Djot and drops `-t/--to`; imported decks carry faithful text and real Djot tables.
- `### Fixes and Maintenance` -- the double-escape defect, imported tables now emitted as Djot pipe
  tables, the module renames, `_slide_animation_writer`.
- `### Removals and Deprecations` -- Marp parser, importers, tests, docs, decks, theme CSS,
  `markdown-it-py` / `PyYAML`, `PARSER_BY_SUFFIX`, `tools/`, `docs/archive/`, and the duplicate PPTX
  extraction (`ConversionSummary`, `shape_inventory`, `extract_slides`, `image_asset`, `slide_notes`,
  `convert_pptx` each existed twice).
- `### Decisions and Failures` -- the fork is Djot-first; the pre-production state was used to fix
  the extraction boundary; the Djot language was held fixed for this work;
  `docs/CHANGELOG.md` and `docs/active_plans/decisions/` keep their Marp references by design.
- `### Developer Tests and Notes` -- which `test_marp_export.py` cases became backend tests, which
  became Djot integration tests, which were retired; the `HUMAN_GUIDANCE.md` bullets removed and
  term-updated; LibreOffice availability if stages went unverified.

## Dispatch and parallelism

Steps 1a, 1b, and 1c are the architectural core and run **sequentially, by one owner**, each gated on
a full `pytest tests/`. They rewrite the imports every other step depends on.

Step 5 touches only content and can start immediately, in parallel with Step 1. After the 1c gate:

| Track | Files | Depends on |
| --- | --- | --- |
| Marp removal + code edits (Steps 2, 3) | `slide_lib/`, `pip_requirements.txt`, `build_slides.sh` | 1c |
| Test rework (Step 4) | `tests/test_native_export.py`, `test_cli.py`, `test_terminal_output.py`, `tests/e2e/` | 1c, and Step 3 for the CLI assertions |
| Content (Step 5) | `genetics/`, `themes/` | nothing |
| Documentation (Step 6) | `docs/`, `README.md`, `tools/` | Steps 3 and 5, for accurate command examples |

The manager writes Step 7 last, from all tracks' results.

## One-time checks vs permanent tests

The greps in Verification are implementation proofs: run them during this work, then let them go.
They do not meet the checklist in
[docs/PYTEST_STYLE.md](docs/PYTEST_STYLE.md) -- a repo-wide name grep
proves a one-time migration rather than logic that could plausibly be wrong, and it would fail later
on legitimate changelog text.

The permanent guards this change needs already exist: `test_import_requirements.py` (declared pins
match imports), `test_pyflakes_code_lint.py` (dead imports), `test_markdown_links.py` (doc links),
`test_source_file_line_limit.py` (file size). The two new tests in Step 4 join them.

## Verification

```bash
git status
git diff --stat
```

**A -- Djot-first names** (one-time)

```bash
git ls-files | grep -iE "marp|legacy"                      # expect: no output
grep -rniE "marp|legacy" slide_lib tests devel *.py *.sh *.txt   # expect: no output
```

**B -- one deck source, matching dependencies** (one-time)

```bash
grep -rni "marp\|markdown_it\|import yaml" slide_lib       # expect: no output
grep -ni "markdown-it\|PyYAML" pip_requirements.txt        # expect: no output
```

**C -- current documentation** (one-time)

```bash
grep -rni marp README.md docs --exclude=CHANGELOG.md --exclude-dir=active_plans
```

Expect only past-tense historical sentences in surviving `docs/HUMAN_GUIDANCE.md` bullets. A line
presenting Marp as something a reader can author or build today is a finding.

**D -- readers return raw facts** (one-time)

```bash
grep -n "markdown\|escape\|join\|!\[" \
  slide_lib/importers/pptx_reader.py slide_lib/importers/odp_reader.py \
  slide_lib/importers/source_model.py
```

Pipe-table rendering, `(` / `)` percent-encoding, and the `[text](url)` shape live in the emitter.

**E -- one path per format** (one-time)

```bash
grep -rn "def shape_inventory\|def extract_slides\|def image_asset\|def slide_notes\|class ConversionSummary" \
  slide_lib/importers
```

Each name appears once.

**Automated gate**

```bash
source source_me.sh && pytest tests/
```

The full suite covers pyflakes, typing, ASCII, markdown links, README first paragraph, guidance-doc
format, import requirements, and the line limit.

**Behavioral acceptance**

```bash
# orientation snapshot, before edits
./build_slides.sh genetics/djot 2>&1 | tee /tmp/djot_build_before.txt

# after
./build_slides.sh genetics/djot 2>&1 | tee /tmp/djot_build_after.txt
source source_me.sh && python3 deck_tools.py lint genetics/djot
source source_me.sh && python3 deck_tools.py import \
  genetics/lect02b-genes_dogma.odp -o /tmp/genes_dogma.djot
source source_me.sh && python3 deck_tools.py lint /tmp/genes_dogma.djot
source source_me.sh && python3 deck_tools.py visibility genetics/lect02b-genes_dogma.odp
source source_me.sh && python3 tests/e2e/e2e_djot_native_layouts.py
```

The standard is the imported deck and the Djot language. Byte-equality and pixel-equality do not
apply -- PPTX and ODP are zip containers with embedded ids and timestamps, so identical input yields
different bytes each run. No wall-clock budget applies either.

Authored decks (the eight `.djot` lectures, which this plan does not rewrite):
- All eight produce PPTX, ODP, and PDF; exit code zero; no `terminal_output` failure panel.
- Slide count and layout selection per deck match the snapshot. Nothing here touches the parser or
  the layout engine, so a change is a bug.
- Text is present and editable; every slide keeps native objects rather than a full-slide raster.
- Image warnings match the snapshot.
- `deck_tools.py lint genetics/djot` is clean.

Imported deck, judged against the source `.odp`:
- `/tmp/genes_dogma.djot` lints clean and parses through `djot_parser.parse_deck()`.
- Slide count equals the source deck's visible slide count; `deck_tools.py visibility` agrees.
- Every source image appears once with a resolvable path.
- Text matches the source characters: no stray backslashes, no entities where the source had plain
  characters, notes as plain lines.
- A source table appears as a Djot table block.

## Risk notes

- Step 1a is a merge, not a rename: two divergent copies of the PPTX extraction become one. Read both
  before choosing what survives -- the Djot copy is more capable, and the Marp copy may hold a fix the
  fork never received. Full `pytest tests/` gates it.
- Step 1b changes generated importer output by design. Judging that output against the imported deck
  is where a mistake in the new escaping path will surface, so it is the acceptance step, not a
  formality.
- `tests/test_marp_export.py` is 802 lines of real backend coverage. Reworking it by behavior, and
  moving backend-owned cases off the parser, is the largest chunk of work in this plan.
- `docs/HUMAN_GUIDANCE.md` is the user's own voice. Applicable guidance keeps its wording.
