# Install

This checkout provides a local Python CLI for compiling extended-Djot source into editable ODP
presentations and ODP-derived PDFs. Run commands from the repository root.

## Requirements

- macOS with Homebrew.
- Python 3.12. Use `source source_me.sh && python3` for every repository Python command.
- LibreOffice Impress for ODP import, ODP output, and PDF export.
- Poppler for PDF inspection tools such as `pdfinfo`.
- Node.js and the locked npm dependencies for local MathJax rendering.
- Packages declared in `pip_requirements.txt`, including yt-dlp for the explicit YouTube-slide tool.

`Brewfile` declares Python 3.12, Node.js, Poppler, and LibreOffice. The normal compiler uses
saved local assets and does not need network access. The YouTube, weather, and podcast helpers
fetch external content only when explicitly invoked.

## Install tools

```bash
brew bundle
source source_me.sh && python3 -m pip install -r pip_requirements.txt
npm ci
```

`npm ci` installs MathJax and its locked dependencies locally. Generated equation SVGs are reusable
artifacts below `_temp/math/`.

Keep the root `package.json` and `package-lock.json` dependency entries for `@mathjax/src` at
`>=4.1.3`; do not restore the older `^4.0.0` range. Keep the root `@xmldom/xmldom` override at
`>=0.9.12` when regenerating the lockfile.

## Optional strict Djot gate

Project lint runs without external Djot software. A separate source-acceptance gate currently
uses Jotdown 0.10.0 on `PATH`; this is the recorded accepted version, not a claim that newer
versions are supported. Install it only when that gate is needed:

```bash
cargo install jotdown --version 0.10.0 --locked --features cli
source source_me.sh && jotdown --version
```

Rust and Cargo are needed only for this optional command.

## Verify install

```bash
source source_me.sh && python3 deck_tools.py --help
```

## Local course links

Keep private Discord and Zoom URLs in the ignored root file `course_links.local.yaml`; do not put
them in tracked Djot. Use `{{course_url:key}}` in a deck, with keys selected from its
`color-theme`. Public URLs remain directly in tracked source. A missing local configuration,
referenced key, or invalid HTTPS URL stops a build that needs it.

```yaml
genetics:
  discord: https://example.org/genetics-invite
  zoom_short: https://example.org/meeting
biotechnology:
  discord: https://example.org/biotech-invite
  zoom: https://example.org/biotech-meeting
```

Copy this local file separately when setting up another checkout. Built ODP and PDF artifacts
contain the resolved URLs and are suitable for student distribution.

## LibreOffice boundary

Import only trusted, instructor-owned ODP files. Save legacy PPTX as ODP in LibreOffice before
importing it. LibreOffice runs external to an agent sandbox on this macOS host; run any command
that can invoke it outside the sandbox. A successful conversion does not make an untrusted
presentation safe to open.

See [USAGE.md](USAGE.md) for build, lint, import, and helper commands.

## Known gaps

- [ ] Establish and record compatibility evidence before treating a Jotdown version other than
  0.10.0 as accepted for the strict source gate.
