# M26 repeat reconstruction: specification review

**PASS** for the supplied reconstruction and slide. The recipe portability issue below is separate from artifact acceptance.

- Source: `genetics/LECT06/djot/assets/lect06e-x_linked_genes_2/sxl_signal_flow.drawn.svg`.
- Trial: `_temp/svg_toolkit/trial_reconstruct_repeat/sxl_reconstruction_trial.drawn.svg`, `.odp`, and `.pdf`.
- Compared case-sensitive word counters from SVG text nodes, joining separately positioned text spans with spaces: identical. Four `Sxl` spans have italic style, paired ON/OFF spans have normal style; SXL protein is upright. This corrects the earlier upright-gene failure.
- Inspected the independently rendered PDF: high, intermediate, and low branches have the correct ON/OFF states, protein and transcript statements, female/intersex/male symbols and labels. Intermediate splits to two states and rejoins at the shared protein outcome. Content is visible within the slide; no clipping or overlaps observed. The SVG viewBox is `0 0 1330 550`; the build script asserts group bounds against this canvas.
- ZIP inspection: embedded `Pictures/6a0e61eb148aedf638e48a00.svg` equals the standalone SVG byte for byte, SHA-256 `6a0e61eb148aedf638e48a00e1fc0dceb9afbf20d35474af3befad0d3de32c07`; the manifest assigns `image/svg+xml`. ODP `draw:text-box` contains the native title `X-Linked Signal and Sxl Activity`.
- `pdftotext -layout _temp/svg_toolkit/trial_reconstruct_repeat/sxl_reconstruction_trial.pdf -` recovers the title and diagram text. `pdfinfo` identifies one 793.701 x 496.063 pt page. `pdftoppm -f 1 -singlefile -png -r 120 _temp/svg_toolkit/trial_reconstruct_repeat/sxl_reconstruction_trial.pdf _temp/svg_toolkit/repeat_spec_pdf` produced the independently inspected render.
- XML and ZIP checks used `/opt/homebrew/bin/python3.12 -B`, Python `xml.etree.ElementTree`, `collections.Counter`, `zipfile`, and `hashlib`, with `PYTHONPATH="$PWD"`. Text was tokenized with `[A-Za-z]+(?:-[A-Za-z]+)?` after joining SVG text chunks with spaces.

**Promotion follow-up:** `build.py` sets `OUT` to a fixed `_temp/svg_toolkit/trial_reconstruct_repeat/` path relative to the current directory. Make the output path relative to `__file__` when promoting the recipe so relocation does not write to the old trial directory.

Limit: no LibreOffice editing or conversion was run in this review; the existing ODP and PDF were inspected. Visual and PDF extraction checks do not establish interactive editing behavior.
