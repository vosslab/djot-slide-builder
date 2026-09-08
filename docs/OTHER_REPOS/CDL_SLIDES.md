# CDL slides review

- Local snapshot: `OTHER_REPOS/cdl-slides`
- Upstream: [cdl-slides](https://github.com/ContextLab/cdl-slides)
- Local version: 1.2.0
- Content type: Python slide preprocessor, Marp wrapper, themes, fonts, and tests
- License found: MIT for the project; bundled font terms require separate review
- Recommendation: Use as a language-design reference, not a compiler

## What it contains

CDL Slides adds a substantial authoring layer above Marp. It preprocesses callouts, flow diagrams,
charts, animations, split tables, and scale directives before invoking Marp. Notable areas include
`compiler.py`, `marp_cli.py`, `assets.py`, content analysis in `preprocessor.py`, and themes under
`src/cdl_slides/assets/themes/`.

Its theme provides semantic note, warning, tip, definition, example, important, gallery, column,
and scale classes. The package also attempts density warnings and SVG generation.

## Reuse assessment

- Ideas: Teaching callouts, accessible flow diagrams, SVG charts, and rendered density warnings
  are relevant. A fixture gallery for theme classes would also be valuable.
- Language model: Its feature inventory helps identify the small number of teaching layouts an
  extension needs. Its broad preprocessor, automatic source changes, and renderer coupling should
  not define the local design.
- Code and functions: The parser and preprocessor are broad and tightly coupled to another
  Markdown dialect. Heavy Manim, Pillow, ffmpeg, YAML, and CLI dependencies do not fit.
- Themes: MIT CSS may be reused with notice, but the theme is too large and assumes raw HTML.
- Assets: Do not copy bundled Avenir files; no separate Avenir license was found in the snapshot.

## Decision

Use CDL as an inventory and counterexample when maintaining the bounded Djot extension for repeated
teaching needs. Do not adopt its compiler: it routes its language through Marp CLI, which is
excluded from the current native rendering path.
