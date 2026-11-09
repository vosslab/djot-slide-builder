## Synology Drive warning

This folder is sync'ed via Synology Drive, so sometimes weird things happen to files

## LibreOffice: never run inside the sandbox

On this macOS host, LibreOffice crashes when launched inside the sandbox. Run every command
that can invoke LibreOffice outside the sandbox (`sandbox_permissions="require_escalated"`),
using the provided repository scripts. This includes PDF builds/exports and conversion tests.

## Temporary files

Use `_temp/` at the repository root for temporary scripts, renders, and review artifacts.

## Repository guidance

- docs/REPO_STYLE.md
- docs/PYTHON_STYLE.md
- docs/MARKDOWN_STYLE.md
- docs/PYTEST_STYLE.md
- docs/DEVELOPMENT.md
- docs/INSTALL.md
- docs/USAGE.md
- docs/CHANGELOG.md
- docs/HUMAN_GUIDANCE.md
- docs/DESIGN_DECISIONS.md
- [docs/slide-specs/README.md](docs/slide-specs/README.md)
- [docs/slide-specs/COLOR_GUIDE.md](docs/slide-specs/COLOR_GUIDE.md)
- [docs/slide-specs/VOICE_GUIDE.md](docs/slide-specs/VOICE_GUIDE.md)
- [docs/slide-specs/PEDAGOGY_GUIDE.md](docs/slide-specs/PEDAGOGY_GUIDE.md)

## Runtime constraints

- Run repository Python with `source source_me.sh && python3`; use Python 3.12. Homebrew packages are under `/opt/homebrew/lib/python3.12/site-packages/`.
- Run every command that can invoke LibreOffice outside the sandbox (`sandbox_permissions="require_escalated"`), including exports, conversion tests, and ODP imports.
- Use root `_temp/` for temporary scripts, renders, and review artifacts.
- Keep `"@mathjax/src": ">=4.1.3"` in `package.json` and the root `package-lock.json` dependency entry; do not restore `^4.0.0`.
- Run the base suite with `source source_me.sh && pytest tests/`.
