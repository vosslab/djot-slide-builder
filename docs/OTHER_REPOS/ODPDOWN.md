# Odpdown review

- Local snapshot: `OTHER_REPOS/odpdown`
- Upstream: [odpdown](https://github.com/thorstenb/odpdown)
- Local metadata version: 0.5.1; module constant: 0.5.0
- Content type: Direct Python Markdown-to-ODP renderer
- License found: BSD-3-Clause
- Recommendation: Historical native-ODP prior art

## What it contains

Odpdown parses Markdown and writes OpenDocument Presentation objects using odfdo. It uses an ODP
template for master pages and layout geometry, places images with aspect-ratio handling, adds
styles, and renders formatted text and code. Relevant areas include `ODFRenderer`, `ODFFormatter`,
`ODFPartialTree`, whitespace handling, style creation, and master-page lookup.

## Reuse assessment

- Ideas: Template-owned master pages and direct ODP shape construction informed the now-complete
  repository-owned native ODP adapter.
- Code and functions: BSD permits reuse with notice, but the implementation is a large older-style
  module built around another Markdown parser and an old Mistune constraint. It also permits
  network image loading.
- Themes and assets: The ODP template is implementation input, not authored Djot styling.
- Fit: Replacing Djot parsing would create a competing authoring dialect and renderer.

## Decision

Do not fork or integrate Odpdown. Its odfdo object construction and master-page geometry remain
historical comparison points for the narrower repository-owned adapter over `LayoutDeck`.
