# SVG toolkit native verification: current rebuild

Fresh native proofs comprise 32 pages: the 18-page toolkit showcase (including the chromosome 7 comparison), 12 consumer excerpt pages from five lecture decks, and two independent-author trial pages. Eight fresh ODP/PDF pairs and their 1600-pixel, white RGB quality-90 WebPs are recorded in [the manifest](svg_aesthetic_native.json); the [contact sheet](../../slide-specs/illustration_examples/svg_toolkit_native/native_proof_index.webp) includes all 32 pages. Independent specification and visual-quality review of this rebuild remains pending.

Each SVG referenced by the eight Djot inputs matched an embedded ODP SVG byte for byte, with `image/svg+xml` manifest entries. `pdfinfo` confirmed page counts, `pdftotext -layout` extracted slide and sampled figure text, and `pdffonts` listed embedded Atkinson Hyperlegible Next in every PDF. Sampled text included chromosome q31, genome exons, array reference, the two yeast titles, seed 9/16, Western primary antibody, kinase and Sxl. These checks do not establish independent editing of every object or a per-glyph font audit.

The contact sheet was inspected for gross loss or clipping; none was apparent. Several Western and array figure labels are small in their existing contexts. The builder reported that left-panel text on Western excerpt pages 5 and 7 needed 18.5 pt, below its 20 pt floor. These source contexts were preserved for the proof. No complete consumer deck was rebuilt in this pass: the fresh evidence covers the 12 extracted slides only. A prior verification recorded full-deck compilation of 351 slides, which is historical evidence rather than a fresh check.

The excerpt inputs preserve each whole original slide, its original theme and other images, with relative image paths rewritten to `repo:` references. They cover genome (1), array (1), yeast (2), seed (1), and Western (7). The showcase source is `exemplars/svg_toolkit.djot`; trial sources are in their respective `svg_toolkit_trials` folders. Outputs were staged with unique `aesthetic_` names under `output/odp/` and `output/pdf/`; reconstructed Djot, preparation, build and verification scripts, rendered PNGs and raw results are in `_temp/svg_aesthetic/native/` for scoped cleanup.

Commands run from the repository root, with LibreOffice-backed builds outside the sandbox:

```sh
PYTHONPATH="$PWD" MPLCONFIGDIR="$PWD/_temp/mplconfig" /opt/homebrew/bin/python3.12 -B _temp/svg_aesthetic/native/prepare.py
bash _temp/svg_aesthetic/native/build.sh
PYTHONPATH="$PWD" MPLCONFIGDIR="$PWD/_temp/mplconfig" /opt/homebrew/bin/python3.12 -B _temp/svg_aesthetic/native/verify.py
```

The build script calls `/opt/homebrew/bin/python3.12 -B deck_tools.py build _temp/svg_aesthetic/native/aesthetic_<name>.djot --format all` for each of `toolkit_showcase`, `human_genome`, `array_comparison`, `yeast_mating_and_diploid`, `seed_phenotypes`, `western_detection`, `new_signaling`, and `sxl_reconstruction`, with `PYTHONPATH` and `MPLCONFIGDIR` set as above. Verification uses `pdfinfo`, `pdftotext -layout`, `pdffonts`, `pdftoppm -png -scale-to-x 1600 -scale-to-y -1`, and Pillow WebP quality 90. No interactive Impress editing, other LibreOffice installation, or live Zoom test was performed.

Machine-readable current verification: [svg_toolkit_native_verification.json](svg_toolkit_native_verification.json).
