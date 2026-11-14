# New signaling trial

This independent trial builds a student-facing receptor/kinase signaling slide using the public toolkit. The source is [build.py](build.py); the generated illustration is [new_signaling_trial.drawn.svg](new_signaling_trial.drawn.svg); the native slide source is [new_signaling_trial.djot](new_signaling_trial.djot); [new_signaling_trial.odp](new_signaling_trial.odp) is the generated native deck; and [new_signaling_trial.webp](new_signaling_trial.webp) is a white-background, quality-90 preview of the illustration; [new_signaling_trial_native.webp](new_signaling_trial_native.webp) previews the PDF page at 1600 pixels wide.

## References and APIs

Consulted `docs/SVG_TOOLKIT.md`, `docs/SVG_TOOLKIT_COOKBOOK.md`, their linked runnable examples `svg_tools/examples/signaling.py`, `membranes.py`, and `proteins.py`, and `docs/slide-specs/VOICE_GUIDE.md`. The cookbook provides the native one-panel Djot and ODP build route. Used `signaling.membrane`, `receptor`, `ligand`, `protein`, and `phosphate`; `parts.transform`; `annotations.connector`; `text.label`; and `drawing.write_svg`. No custom geometry was necessary. Activity and phosphate were explicitly specified independently. No library or API changes and no maintainer hints.

## Commands and results

Run from repository root:

```sh
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B docs/slide-specs/illustration_examples/svg_toolkit_trials/new_signaling/build.py
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B deck_tools.py build docs/slide-specs/illustration_examples/svg_toolkit_trials/new_signaling/new_signaling_trial.djot --format odp
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B deck_tools.py build docs/slide-specs/illustration_examples/svg_toolkit_trials/new_signaling/new_signaling_trial.djot --format pdf
cp output/odp/new_signaling_trial.odp docs/slide-specs/illustration_examples/svg_toolkit_trials/new_signaling/new_signaling_trial.odp
cp output/pdf/new_signaling_trial.pdf docs/slide-specs/illustration_examples/svg_toolkit_trials/new_signaling/new_signaling_trial.pdf
```

Both deck builds succeeded; PDF export ran outside the sandbox. The rendered slide preview was inspected after rebuilding. PDF is at `output/pdf/new_signaling_trial.pdf` and the original ODP at `output/odp/new_signaling_trial.odp`. The native preview is a rasterization of that PDF; it does not establish behavior in other LibreOffice installations.

## Observations

No command failed. The first rendered slide showed overlap between authored labels and the activity labels automatically drawn by `protein(activity=...)`. Moving the authored labels down and increasing the figure height resolved the overlap in the final preview. The activity-label spacing documentation gap identified in this trial has since been fixed. The final figure retains both the automatic activity labels and explicit labels for clarity. The native ODP was built and rendered via PDF; individual ODP objects were not interactively edited.
