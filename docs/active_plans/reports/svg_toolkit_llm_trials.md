# SVG toolkit independent author trials: M26 verification

The earlier versions of both independent trial slides passed specification and quality review. These two native pages are separate from the base 29-page set. See [repeat specification review](svg_toolkit_reconstruction_repeat_spec.md) and [quality review](svg_toolkit_trials_quality.md).

## New signaling: PASS

The slide shows a ligand and membrane receptor leading to an active kinase that activates Response A and inhibits phosphorylated, inactive Response B. Title and takeaway are native slide text. The author reported no command errors, and resolved an initial activity-label overlap by adjusting label placement and figure height. The documentation gap concerning automatic activity labels and their spacing has since been fixed. No maintainer hints or API changes were used in the trial.

## Sxl reconstruction: initial failure, fresh repeat PASS

The first reconstruction failed source fidelity: all four gene names were upright rather than italic, although words, branches and symbols matched. Its author encountered failed sandboxed `qlmanage` thumbnailing and missing box labels with `rsvg-convert -b white`; transparent rendering and white compositing worked. That behavior alone did not establish a toolkit defect.

A small styled-box API and documentation fix preceded an independently authored fresh repeat. No hints or API edits occurred during that repeat. Its four italic gene names, upright ON/OFF and protein labels, word inventory, branch states and symbols match the source. The repeat passed specification and quality reviews. Its durable build recipe changes only the output path and helper type annotations; the earlier build yielded the accepted SVG SHA-256 `6a0e61eb148aedf638e48a00e1fc0dceb9afbf20d35474af3befad0d3de32c07`.

## Current native rebuild and limits

The refreshed aesthetic trial SVGs were embedded byte for byte in newly rebuilt one-page ODPs with SVG MIME entries. Their PDFs were rebuilt and checked for page counts, extractable slide and figure text, and embedded Atkinson Hyperlegible Next fonts; white RGB native WebPs were rendered at 1600 pixels and quality 90. The prior reviews above apply to the earlier artifacts; the refreshed outputs await independent review. Current hashes and PDF details are in [svg_toolkit_llm_trials.json](svg_toolkit_llm_trials.json) and [svg_aesthetic_native.json](svg_aesthetic_native.json). Interactive Impress editing, live Zoom, and other LibreOffice installations were not tested.

Durable artifacts and build instructions: [new signaling](../../slide-specs/illustration_examples/svg_toolkit_trials/new_signaling/README.md) and [Sxl reconstruction](../../slide-specs/illustration_examples/svg_toolkit_trials/sxl_reconstruction/README.md).
