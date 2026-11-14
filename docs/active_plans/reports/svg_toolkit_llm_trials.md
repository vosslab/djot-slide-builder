# SVG toolkit independent author trials: M26 verification

Both independent trial slides passed specification and quality review. These two native pages are separate from the base 29-page set. See [repeat specification review](svg_toolkit_reconstruction_repeat_spec.md) and [quality review](svg_toolkit_trials_quality.md).

## New signaling: PASS

The slide shows a ligand and membrane receptor leading to an active kinase that activates Response A and inhibits phosphorylated, inactive Response B. Title and takeaway are native slide text. The author reported no command errors, and resolved an initial activity-label overlap by adjusting label placement and figure height. The documentation gap concerning automatic activity labels and their spacing has since been fixed. No maintainer hints or API changes were used in the trial.

## Sxl reconstruction: initial failure, fresh repeat PASS

The first reconstruction failed source fidelity: all four gene names were upright rather than italic, although words, branches and symbols matched. Its author encountered failed sandboxed `qlmanage` thumbnailing and missing box labels with `rsvg-convert -b white`; transparent rendering and white compositing worked. That behavior alone did not establish a toolkit defect.

A small styled-box API and documentation fix preceded an independently authored fresh repeat. No hints or API edits occurred during that repeat. Its four italic gene names, upright ON/OFF and protein labels, word inventory, branch states and symbols match the source. The repeat passed specification and quality reviews. Its durable build recipe changes only the output path and helper type annotations; rebuilding yields the exact accepted SVG SHA-256 `6a0e61eb148aedf638e48a00e1fc0dceb9afbf20d35474af3befad0d3de32c07`.

## Native checks and limits

Each durable build script ran from the repository root using `PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B`. Both resulting SVGs are byte-identical to the SVG embedded in their accepted ODPs; each ODP manifest declares `image/svg+xml`. The accepted PDFs have one page each; `pdftotext -layout` extracts title and figure text, and `pdffonts` reports embedded Atkinson Hyperlegible Next. The standalone WebPs are white-composited RGB at quality 90; native WebPs are white RGB at quality 90, rendered from the accepted PDFs at 1600 pixels wide. Identical embedded SVGs provide traceability without a new native conversion. Interactive Impress editing, live Zoom, and other LibreOffice installations were not tested.

Durable artifacts and build instructions: [new signaling](../../slide-specs/illustration_examples/svg_toolkit_trials/new_signaling/README.md) and [Sxl reconstruction](../../slide-specs/illustration_examples/svg_toolkit_trials/sxl_reconstruction/README.md).

## Artifact SHA-256

### new_signaling

```text
fded5ea8b13b9e3b64a3b832ddcec027d2b821304461efc00c009ac6770c3c23  README.md
23460cd8da5fdd14a1e928a70fa83212a329cc492770cdbfff9d94ab10729312  build.py
a3ef6e452ce921c88829221026564d3cdc76c8997f93ecc911170d8fd06ffc2b  new_signaling_trial.djot
9e488367de49e81b7ec4177b9bc19d2804ed70ca3b2a9cec66d0d392cd360a5e  new_signaling_trial.drawn.svg
219824c30d280d994fc8831252ceef0effb86601edb2e2200b45cabc7c6369c9  new_signaling_trial.odp
16f76dd0a39ef9e1c9c5884d1378759ba72a72501fc0879d657e084adc4b7d49  new_signaling_trial.pdf
79ab6dc37ca9dfafd1e7a218609a9056be58e9ef619bdff748f9809365aef5b8  new_signaling_trial.webp
0060c7aaae0d04c9ec03abd2f74f2580ee58dd7411be61657db5f001aa8cf5f2  new_signaling_trial_native.webp
```

### sxl_reconstruction

```text
8bfc87c13e318a43e16422706736e62bc46fd435b05b1b9030395f7c3454e72e  README.md
804ce4e9a60553c11a86c48fd4f9d79b25b8f9159f178e81b1735e7cc016b94b  build.py
8a7e3d89b9759a76d122764a145814bff89be6ff1b793076e61b88adbe25c24b  sxl_reconstruction_trial.djot
6a0e61eb148aedf638e48a00e1fc0dceb9afbf20d35474af3befad0d3de32c07  sxl_reconstruction_trial.drawn.svg
b77d2726632c2e17d9804e65f19489073c2c4702b0e2966d15dc26537e5a83bf  sxl_reconstruction_trial.odp
aafb44e30cdd600f2738881cb9e7bc236731dfa6656bb2d0316869b3d0ba5073  sxl_reconstruction_trial.pdf
c0fe2f98297c0ca90079f91abff2342f00a1b01365bf793190d22055bf41104b  sxl_reconstruction_trial.webp
33c21c2c27992b44b43c7eb8569acf0d8d02a4eb014ac58a00b40d3e8e2c0b47  sxl_reconstruction_trial_native.webp
```

