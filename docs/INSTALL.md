# Install

This repository runs local Python commands against the checkout to create editable PPTX, ODP, and
PDF presentations. It also imports trusted existing ODP or PPTX into extended-Djot source.

## Requirements

- macOS with Homebrew.
- Python 3.12; run repository Python commands through `source source_me.sh && python3`.
- LibreOffice Impress for ODP input, conversion of native content to editable ODP, application of
  the repository OTP master, and ODP-derived PDF output.
- Poppler, including `pdfinfo`, for native end-to-end PDF verification.
- The packages in `pip_requirements.txt`.
- Jotdown 0.10.0 on `PATH` for strict-Djot source acceptance. `source_me.sh` adds the conventional
  Cargo bin directory when it exists.

## Install tools

From the repository root, install the declared macOS tools and Python packages:

```bash
brew bundle
source source_me.sh && python3 -m pip install -r pip_requirements.txt
```

The Brewfile installs Python 3.12, Poppler, and LibreOffice. Jotdown is a separate strict-Djot
validator. Confirm the required installed version before running the source-acceptance command in
[USAGE.md](USAGE.md):

```bash
source source_me.sh && jotdown --version
```

Expected output: `jotdown 0.10.0`.

To install that optional strict-source validator, use Rust/Cargo 1.82 or later:

```bash
cargo install jotdown --version 0.10.0 --locked --features cli
source source_me.sh && jotdown --version
```

Rust and Cargo are needed only to install Jotdown for strict-source acceptance; the normal build
prerequisites above do not require them.

## Verify install

```bash
source source_me.sh && python3 deck_tools.py --help
```

## Conversion boundary

Close the LibreOffice desktop application before a command that imports ODP or produces ODP/PDF.
The repository invokes LibreOffice headlessly through its established user profile.

Import only trusted instructor-owned ODP or PPTX files. Archive and image validation bounds
repository processing, but it does not sandbox LibreOffice or make an untrusted presentation safe
to open.

Continue with [USAGE.md](USAGE.md) for import, source validation, and native export commands.
