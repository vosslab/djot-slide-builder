# Binding and phenotype visual update

## Scope and decisions

Updated `svg_tools/binding.py` and `svg_tools/phenotypes.py`. Existing examples and public
function signatures remain unchanged. Shapes use locally authored paths and the shared
`svg_tools._style` outline and dimension-baking functions. Antibody tips and Fc preserve
the original anchor coordinates; ovals, seeds, and antibodies have contained upper-left
highlights and lower shadows. Wrinkled seeds retain folds and an irregular outline. The
flower remains a generic radial wildflower. Servier was a style reference only; no Servier
geometry was used.

The vector source is generated as SVG fragments and placed by existing composition helpers.
The four examples retain their labels and layout. Western contacts are target to primary Fab,
primary Fc to secondary Fab, and secondary Fc to enzyme. Seed-cross retains eight seeds,
22 text labels, and the existing fractions and color associations.

Consulted `docs/SVG_VISUAL_STYLE.md`; the local SVG creator references `targeted_editing.md`
and `project_workflow.md`; *A Handbook of Biological Illustration*, Planning the Copy Size
(lines 210-224, reduction and legibility); and *Quick and Easy Vector Graphics* (lines
455-469, drawing order and grouping). These are drawing guidance, not anatomical sources.

## Verification

```
PYTHONPATH="$PWD:$PWD/tests" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest tests/test_svg_binding.py tests/test_svg_phenotypes.py -q
```

Result: 4 passed. The silhouette test now checks baked coordinates and uniform-stroke bounds;
flower tests follow the grouped petals. Contact tests verify coincident named anchors.

```
mkdir -p _temp/svg_aesthetic/binding_phenotypes
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B -m svg_tools.examples.binding
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B -m svg_tools.examples.phenotypes
cp _temp/svg_toolkit/binding/binding.svg _temp/svg_aesthetic/binding_phenotypes/binding.svg
cp _temp/svg_toolkit/phenotypes/phenotypes.svg _temp/svg_aesthetic/binding_phenotypes/phenotypes.svg
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B -m svg_tools.examples.western_detection _temp/svg_aesthetic/binding_phenotypes/western_detection.svg
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B -m svg_tools.examples.seed_cross _temp/svg_aesthetic/binding_phenotypes/seed_cross.svg
for f in _temp/svg_aesthetic/binding_phenotypes/*.svg; do rsvg-convert -w 1200 "$f" -o "${f%.svg}-1200.png"; rsvg-convert -w 400 "$f" -o "${f%.svg}-400.png"; done
```

Inspected all four 1200-pixel renders, refined the antibody hinge, regenerated, and inspected
all four 400-pixel renders. The seed shapes and binding topology remain discernible at 400 px;
small gallery labels require the intended larger placement. The transparent gallery examples
need a light slide background for their dark labels. The canonical lecture assets and native
slide exports were not regenerated in this workstream; integration owns those checks.
