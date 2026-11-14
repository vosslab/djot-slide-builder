# Independent Sxl reconstruction trial

## References and scope

- `docs/SVG_TOOLKIT.md` and `docs/SVG_TOOLKIT_COOKBOOK.md`, especially the reconstruction, styled flow node, and native slide recipes.
- Original: `genetics/LECT06/djot/assets/lect06e-x_linked_genes_2/sxl_signal_flow.drawn.svg`. Its text and vector shapes were inspected directly; the original was not edited.
- No other trial directory was consulted. No toolkit API changes or maintainer hints were requested or used.

## Comparison

The figure preserves the source's exact visible words, capitalization and gene formatting: italic *Sxl* with upright ON/OFF, upright SXL protein, and the original descriptions and result labels. High signal leads to ON, protein produced, female-specific transcripts and normal female; low leads to OFF, protein not produced, male-specific transcripts and normal male. Intermediate has separately connected ON in some cells and OFF in other cells, followed by the source's shared mixed protein and transcript statements and intersex symbol. The female, combined, and male symbols retain the source's red/blue visual distinction. The reconstruction uses consistent toolkit boxes and connector arrows rather than the original's mixed unboxed text and colored gene boxes. Colored ON/OFF boxes distinguish states. The sex-symbol geometry is the sole custom `SvgPart`.

## Toolkit and commands

Public interfaces used: `annotations.box`, `annotations.connector`, `text.label`, `text.TextRun`, `parts.transform`, `parts.SvgPart`, `parts.group`, and `drawing.write_svg`. Signatures were inspected with Python's `inspect.signature` as permitted. Toolkit documentation and the chosen interfaces were usable; no API failure occurred. The first visual render revealed a low-branch line crossing its text and weak box text contrast; positions and stroke color were adjusted and re-rendered.

Run from the repository root:

```sh
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B docs/slide-specs/illustration_examples/svg_toolkit_trials/sxl_reconstruction/build.py
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B deck_tools.py build docs/slide-specs/illustration_examples/svg_toolkit_trials/sxl_reconstruction/sxl_reconstruction_trial.djot --format all
pdftotext -layout docs/slide-specs/illustration_examples/svg_toolkit_trials/sxl_reconstruction/sxl_reconstruction_trial.pdf -
```

The build command was run outside the sandbox per repository LibreOffice instructions. It wrote `output/odp/sxl_reconstruction_trial.odp` and `output/pdf/sxl_reconstruction_trial.pdf`, which were copied here. The SVG build includes a canvas-bound assertion. The standalone illustration and rendered PDF page were visually inspected; PDF text extraction recovered the title, branch descriptions and outcomes. The slide title is native, and the diagram is a single SVG; the SVG retains live text and vector geometry. Editing behavior in LibreOffice was not separately tested.

## Artifacts

- [build.py](build.py), [sxl_reconstruction_trial.drawn.svg](sxl_reconstruction_trial.drawn.svg), and [sxl_reconstruction_trial.djot](sxl_reconstruction_trial.djot)
- [sxl_reconstruction_trial.webp](sxl_reconstruction_trial.webp) (white background, quality 90)
- [sxl_reconstruction_trial.odp](sxl_reconstruction_trial.odp) and [sxl_reconstruction_trial.pdf](sxl_reconstruction_trial.pdf)
- [sxl_reconstruction_trial_native.webp](sxl_reconstruction_trial_native.webp) is the PDF page at 1600 pixels wide, white background and quality 90.

The first independent reconstruction failed source fidelity because the gene names were upright. After a small styled-box API and documentation fix, this fresh repeat was authored independently without hints or API edits during the repeat.
