# Shared outline cap

The shared outline now uses `min(0.02 * min(width, height), 3.0)` drawing units.
The charcoal ink and round caps and joins are unchanged. A 500-by-340 container now
uses a 3.0-unit outline instead of 6.8; a 200-by-50 part still uses 1.0. The visual
style guide records the cap and its purpose.

Validation: the focused style, cells, and signaling tests passed (6 tests) using
`PYTHONPATH="$PWD:$PWD/tests" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest tests/test_svg_style.py tests/test_svg_cells.py tests/test_svg_signaling.py`.
The style test checks the large-container bound and the existing smaller-part behavior.

The cell implementation is being edited concurrently. A fresh composed organelle render
and visual quality review are left to the composition owner after that work is ready.
