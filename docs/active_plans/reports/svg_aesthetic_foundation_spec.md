# SVG aesthetic foundation SPEC review

**Verdict: FAIL.** The reviewed snapshot has a namespace collision that violates the static SVG and process-state contract.

## Finding

- `svg_tools/svg_import.py:123-131` manually adds `xmlns:xlink` after ElementTree has chosen prefixes from the process-wide registry. If a caller previously registered `xlink` for the SVG namespace, importing an SVG with `xlink:href` returns a fragment with two conflicting `xmlns:xlink` declarations. `ElementTree.fromstring` rejects it with `ParseError: duplicate attribute`. The existing test at `tests/test_svg_import.py:30-37` covers a different prior mapping, so it does not expose this collision. The registry remains unchanged, but the returned fragment is unusable.
- Removing the importer's manual prefix rewrite allows ElementTree to emit a self-contained fragment and resolves the specific SVG-prefix collision. It is not sufficient end to end: `svg_tools/drawing.py:134-147` repeats the same manual declaration and fails validation if the registry maps `xlink` to a retained foreign namespace. Independently reproduced using a Dublin Core `metadata` title and an XLink reference: `write_svg` raises `ParseError: duplicate attribute`. Verify both direct fragments and final document writing with colliding registrations while preserving the registry; preserve the final output compatibility contract.

## Other scoped checks

The gallery restores the caller's working directory in `finally` and passes a path to the curve recipe without modifying its `__file__`; focused success and renderer-failure tests passed. The shared style helper bakes authored path geometry before a uniform shorter-dimension stroke and retains closure for its documented current path subset. The three plot recipes retain their plotted data; the genome values total 99.5 with the approximate intron label and no normalization. Matplotlib styling and temporary font properties are restored, with live Atkinson labels in the focused checks. Reviewed diagram recipes preserve their displayed relationships, live labels, and existing shared annotation primitives. No other concrete contract failure was identified in the scoped source review.

Focused command, direct Homebrew Python and root scratch space:

```sh
PYTHONPATH="$PWD:$PWD/tests" MPLCONFIGDIR="$PWD/_temp/mplconfig" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest --basetemp="$PWD/_temp/svg_aesthetic/spec/pytest" -q tests/test_svg_import.py tests/test_svg_gallery_state.py tests/test_svg_style.py tests/test_svg_plots.py tests/test_svg_annotations.py tests/test_svg_text.py tests/test_svg_text_extract.py tests/test_svg_icons.py
```

**44 passed.** The first run produced six setup errors because the requested scratch parent did not yet exist; after creating it, the complete command passed. The two namespace collision probes above failed as described. This is a source and focused behavioral review, not visual acceptance, a full gallery build, a full suite, or LibreOffice validation. Other concurrently edited SVG families were outside this review.
