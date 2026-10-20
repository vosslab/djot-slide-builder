## LibreOffice: never run inside the sandbox

On this macOS host, LibreOffice crashes when launched inside the sandbox. Run every command
that can invoke LibreOffice outside the sandbox (`sandbox_permissions="require_escalated"`),
using the provided repository scripts. This includes PDF builds/exports, conversion tests,
and ODP imports: the importer can launch LibreOffice indirectly to convert metafiles to SVG.
Do not retry a sandboxed LibreOffice crash or assume an import is LibreOffice-free.

## Temporary files
Use `_temp/` at the repository root for temporary scripts, renders, and review artifacts.

## Coding Style
See Python coding style in docs/PYTHON_STYLE.md.
See Markdown style in docs/MARKDOWN_STYLE.md.
See repo style in docs/REPO_STYLE.md.
When making edits, document them in docs/CHANGELOG.md.
Record human-stated guidance in docs/HUMAN_GUIDANCE.md; record design decisions in docs/DESIGN_DECISIONS.md.

## Python Environment
AI agents (Codex/Claude) must run Python using `source source_me.sh && python3` (use Python 3.12 only).
On this user's macOS (Homebrew Python 3.12), Python modules are installed to `/opt/homebrew/lib/python3.12/site-packages/`.
