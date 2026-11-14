# SVG toolkit text and import quality review

Reviewed the M5 text and M6 import implementations, their focused tests, and the two runnable examples. This is a quality review, not a native slide export or a general SVG/CSS compatibility certification.

## M5: styled text and extraction

**Visual result: PASS.** The [styled text render](../../../_temp/svg_toolkit/text_import_quality/styled_text.webp) is readable: the gene name is bold and italic, the subscript is visible, and the remaining text returns to its normal style. The XML preserves editable text and explicit run styles. Extraction reports literal text-element positions and explicitly identifies raster and outlined labels as unavailable. Blank lines count toward the height overflow check.

**Wrapping edge case: needs a contract decision.** At size 20, `wrapped_text` with `TextRun('a b')` and width 12 raises width overflow: the individual words measure approximately 10.50 and 11.32, but the preserved trailing space makes the first line approximately 16.10. This is consistent with treating every preserved space as occupying line width, but means an ordinary word wrap may fail even when each word fits. Clarify whether whitespace must survive unchanged at line boundaries before calling this an implementation defect.

## M6: SVG import

**Visual result: FAIL for the example.** The [composition render](../../../_temp/svg_toolkit/text_import_quality/svg_composition.webp) retains both patterned imports and their live labels, but dark diagonal stripes pass directly through the dark labels, making them difficult to read. Give the labels a clear background or otherwise increase local contrast in the example, then render it again.

The implementation preserves a positive clipped viewBox viewport, root presentation, definitions, live text, and local references in the reviewed paths. IDs and href, URL, and accessibility references are namespaced again when grouped. Parsing uses defused XML and the importer rejects unsupported active or external resources. The scoped Matplotlib universal stylesheet handling is not a general CSS editor; ordinary installed fonts remain unembedded by design.

## Checks and limits

- `PYTHONPATH="$PWD:$PWD/tests" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest tests/test_svg_text.py tests/test_svg_text_extract.py tests/test_svg_import.py tests/test_svg_parts.py -q`: **24 passed**.
- Generated both example SVGs and inspected white-background, quality-90 WebP renders made with `PANGOCAIRO_BACKEND=fc rsvg-convert` and Pillow.
- The suite includes a real existing Matplotlib SVG, repeated namespaced imports, comments and accessibility references, malformed XML, and prohibited resources. It does not establish support for arbitrary SVG or every installed font.
- No LibreOffice or native slide exports were run.
