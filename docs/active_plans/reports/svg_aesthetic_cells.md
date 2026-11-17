# Cell and organelle aesthetic work

The cell toolkit now uses locally authored shapes, uniform final-space outlines,
and restrained edge planes. Nuclear envelopes have two explicit boundaries. Plant
walls remain caller-colored and fused yeast remains a single two-lobed envelope.
Nuclei and organelle contents remain separately composed by callers. ER is a
folded network with alternating bridges; Golgi is a stack of separate curved sacs.
Mitochondria show an inner boundary and connected folds, and chloroplasts show a
separate envelope and linked thylakoid stacks. These are simplified schematics,
not measurements or images of particular cells. No Servier geometry was used.

## Checks and proof

- `PYTHONPATH="$PWD:$PWD/tests" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest tests/test_svg_cells.py tests/test_svg_organelles.py` - 3 passed.
- Generated `svg_tools/examples/cells.py`, `organelles.py`, and `yeast_mating.py`
  with `PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B`; yeast used
  `--output-dir _temp/svg_aesthetic/cells`.
- Rendered using `rsvg-convert -w 1200` and `-w 480`; outputs are in
  `_temp/svg_aesthetic/cells/`, named `cells`, `organelles`,
  `yeast_mating_toolkit.drawn`, and `yeast_diploid_toolkit.drawn` with width
  suffixes. The larger organelle proof is `organelles-review.png`.
- Inspected generated cell and organelle galleries and both yeast stages at large
  and reduced sizes. Small gallery labels naturally require sufficient slide space.
  Final native slide import/export is outside this workstream.

## Sources and construction

- [Mitochondria](https://www.ncbi.nlm.nih.gov/books/NBK9896/) describes the
  inner membrane and cristae; [Chloroplasts and Photosynthesis](https://www.ncbi.nlm.nih.gov/books/NBK26819/)
  describes the separate thylakoid system. [The Endoplasmic Reticulum](https://www.ncbi.nlm.nih.gov/books/NBK9889/)
  describes the connected network; [Compartmentalization of Cells](https://www.ncbi.nlm.nih.gov/books/NBK26907/)
  describes Golgi cisternal stacks.
- The local `svg-creator-expert` corpus informed construction: *A Handbook of
  Biological Illustration*, lines 278-294 (clarity and line hierarchy), and
  *Mastering SVG*, lines 635-687 (viewport and coordinate conventions).
  Paths are under `/Users/vosslab/.codex/skills/experts/svg-creator-expert/references/local-only/`.
