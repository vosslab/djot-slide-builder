# SVG toolkit documentation audit fixes

- Installation now distinguishes bundled measurement fonts from renderer-installed fonts and
  gives macOS installation and Font Book verification steps for all four faces of both families.
  It identifies librsvg as optional for gallery and preview rendering.
- Architecture and file structure now identify `svg_tools/` and link the toolkit catalogue. The
  plan states that SVG geometry and resources are contained while fonts require installation.
- The toolkit changelog entry uses the required additions category, and the unused CairoSVG
  requirement was removed. Archived reference-only CairoSVG code remains unchanged.

## Checks and limits

- Both bundled font directories contain regular, bold, italic, and bold-italic TTF files.
- `rsvg-convert --version` reports 2.63.4 at `/opt/homebrew/bin/rsvg-convert` on this host.
- All remaining requirements parse with `packaging.requirements.Requirement`. A case-insensitive
  repository search found no live CairoSVG consumer; the historical archived script retains one.
- Relative Markdown links outside code in the five edited documentation files resolve locally.
- Font installation commands were documented but not executed; no clean-machine installation,
  gallery regeneration, LibreOffice conversion, or native visual review was performed. Existing
  shared-state code findings and changelog rotation remain outside this work.
