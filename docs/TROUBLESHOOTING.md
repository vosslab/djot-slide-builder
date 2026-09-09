# Troubleshooting

Use this guide when a local build, import, or source-validation command stops. Commands report
source paths and line numbers where possible; correct the named source or environment condition,
then repeat the smallest affected command.

## Set up the command environment

### Python cannot import project modules

Run Python commands from the repository root through the required environment setup:

```bash
source source_me.sh && python3 deck_tools.py --help
```

The setup places the repository on `PYTHONPATH` and makes a Cargo-installed Jotdown available when
`$HOME/.cargo/bin` exists. Use Python 3.12 and install the declared packages as described in
[INSTALL.md](INSTALL.md).

### Strict Djot validation cannot start

The strict gate requires both flags and a discoverable Jotdown executable:

```bash
source source_me.sh && jotdown --version
source source_me.sh && python3 deck_tools.py lint --require-native \
  --native-executable "$(command -v jotdown)" genetics/djot
```

The required version is Jotdown 0.10.0. If the version command does not report it, resolve the
local Jotdown installation before treating a deck as source-accepted. The ordinary `lint` command
continues to provide the repository's fast semantic check, but it does not run native validation.

## Repair source failures

### Lint names a source line

Run fast lint against the individual deck first:

```bash
source source_me.sh && python3 deck_tools.py lint path/to/deck.djot
```

Fix the directive, slot, block, inline syntax, or local image path named in the diagnostic. Every
deck begins with an exact `=== layout: <name>` directive, and `@<slot>` names only slots declared
by that layout. Component image paths are relative to the `.djot` deck directory, must name existing
local files, and must remain inside the repository. The authoring contract and full commands are in
[USAGE.md](USAGE.md).

### Build rejects an input path

`deck_tools.py build` accepts an existing `.djot` file inside this repository or a repository folder
containing `.djot` files. Supply a source path rather than an ODP, Markdown file, missing path, or
folder with no Djot decks. Use `deck_tools.py import` for a trusted ODP source.

### Capacity inspection reports a concern

Use the compile-only inspection command to see every current capacity concern in one source deck or
folder:

```bash
source source_me.sh && python3 deck_tools.py capacity genetics/djot
```

Each line identifies the source location, layout slot, readable floor, and explicit compiler cause.
`required=<size>pt` records content that remains representable at a reduced size; the normal build
keeps that authored slide and reports the same compromise. `required<1pt` records content beyond the
shared serializer-safe minimum, so no editable native slide can represent it. The command continues
after those physical-capacity findings and returns `1` whenever it reports a concern. A silent `0`
means the selected decks are floor-safe. Capacity inspection creates no presentation artifacts and
uses no LibreOffice conversion.

## Restore Office conversions

### Build says LibreOffice is running

Close the LibreOffice desktop application, then rerun the build. ODP and PDF conversions preflight
that desktop state once, then run direct headless conversions sequentially.

### Build says LibreOffice is not installed

Install the declared macOS tools from the repository root, then repeat the build:

```bash
brew bundle
```

The dependency bundle installs LibreOffice and Poppler for PDF verification. A nonzero conversion
or absent generated artifact remains a failed Office conversion; preserve its displayed diagnostic
and retry only after resolving the local LibreOffice condition.

## Recover an import workflow

### Import will not write the destination

Import refuses to overwrite an existing `.djot` destination or its adjacent `assets/<deck>/`
directory. Choose a new output path with `--output`, review the resulting deck, and only then make
the reviewed Djot file the canonical authoring source. Do not use an import to replace an
established source automatically.

### Import rejects the source format

The `import` command accepts trusted `.odp` inputs only. Save a legacy PPTX as ODP with LibreOffice
before importing. Use `visibility` to inspect resolved ODP slide visibility before importing. An
import that reports no presentation slides or no visible presentation slides needs a source
presentation with visible slides.

See [INSTALL.md](INSTALL.md) for tool prerequisites, [USAGE.md](USAGE.md) for workflows, and
[PIPELINE.md](PIPELINE.md) for source and artifact ownership.
