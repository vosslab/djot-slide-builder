# SVG aesthetic: diagrams and typography

The annotation example retains its authored geometry and semantic node fills. Shorter arrowheads
and bold branch labels improve the hierarchy without changing connector semantics. The shared
annotation primitives already use the agreed ink and stroke width, so their API, anchors, bounds,
and overflow behavior remain unchanged.

The text examples use the shared ink for ordinary text, show an italic gene name, and show two
aligned monospace sequence rows. The wrapped example has a wider text measure to avoid an isolated
final word. Icons use the shared ink and retain the existing Lucide import and embedded license.
The imported SVG example uses a quieter pattern so its live text leads. The placement example was
reviewed unchanged; its chromosome geometry and spacing remain intact.

## Checks

`PYTHONPATH="$PWD:$PWD/tests" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest tests/test_svg_annotations.py tests/test_svg_text.py tests/test_svg_text_extract.py tests/test_svg_icons.py -q` - 21 passed.

Each of `annotations`, `text_labels`, `styled_text`, `icons`, `svg_composition`, and `placement`
was generated using `PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B -m svg_tools.examples.NAME`.
Each SVG was rendered on white with `PANGOCAIRO_BACKEND=fc rsvg-convert --background-color white`
at widths 1200 and 360. Both sizes were visually inspected; no clipping or overlap was observed.
SVG copies and previews are in `_temp/svg_aesthetic/diagrams/`, named `NAME.svg`,
`NAME_1200.png`, and `NAME_360.png`.

This is a local SVG rendering check; no native presentation export or full test suite was run.
