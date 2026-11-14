# Organelle corrective construction

Implemented in `svg_tools/cells.py`; regression coverage in
`tests/test_svg_organelles.py`. The public API and caller colors remain unchanged.
Mitochondrial and chloroplast cardinal anchors now lie on the new envelopes.
Existing conservative part bounds contain the new paint. No examples, DNA source,
biotech LECT11 source, or external artwork were edited or imported in this pass.

## Construction

The mitochondrion is a locally authored asymmetric section with a closed outer
membrane and one closed inner membrane. Three upper and two lower invaginations
interleave without crossing. Their lumens remain open to the peripheral
intermembrane space, and the matrix is one connected interior. Rounded roots and
unequal fold lengths avoid the former unattached wave. The caller's base color
fills the envelope and fold lumens; a translucent white matrix and a restrained
lower rim shade distinguish spaces and shallow depth.

The chloroplast has rounded outer and inner envelopes instead of pointed ends.
Three schematic grana contain flattened, rounded thylakoid sacs with visible top
faces and narrow side faces. Two lamellae visibly join representative sacs across
the stacks. Their connections continue behind the sac faces; the oblique schematic
does not enumerate every hidden connection in the three-dimensional thylakoid
network. Stack and fold counts are illustrative, not measured biological claims.

Internal mitochondrial, chloroplast and nuclear strokes derive from the actual
outer stroke, preserving line hierarchy when the shared outline cap applies.
Generic ER, Golgi, lysosomes and vesicles retain their existing anatomy.

## Evidence

Ran the required direct-interpreter lane:

```
PYTHONPATH="$PWD:$PWD/tests" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest tests/test_svg_cells.py tests/test_svg_organelles.py -q
```

Result: **4 passed in 0.74 s**. The added regression checks continuous closure,
nonadjacent-segment intersections, separation of inner and outer membranes,
multiple transverse crossings representing folds, and envelope contact anchors.
It tests anatomical behavior rather than a frozen path string.

Temporary verification:

```
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B _temp/svg_aesthetic/organelle_fix/check_geometry.py
PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B _temp/svg_aesthetic/organelle_fix/render.py
```

`geometry.json` records checks at 130x86, 90x50, 250x165 and 1000x620 drawing
units. Each has a simple matrix polygon contained by the outer envelope, a
connected matrix and connected intermembrane/crista lumen region, twelve transverse
inner-membrane crossings, and painted geometry inside the declared bounds. The
independent polygon check samples each segment 100 times and rounds sub-billionth
unit numerical closing noise; exact Bezier intersection tests remain in pytest.
Installed Shapely was used only for this scratch verification, with no new runtime
dependency. Large-size outer/inner strokes are respectively 3 and 1.5 units.

Rendered with CairoSVG on white and inspected with `view_image`:

- `_temp/svg_aesthetic/organelle_fix/organelles-1200.png`
- `_temp/svg_aesthetic/organelle_fix/organelles-400.png`
- `_temp/svg_aesthetic/organelle_fix/mitochondrion-1200.png`
- `_temp/svg_aesthetic/organelle_fix/mitochondrion-400.png`
- `_temp/svg_aesthetic/organelle_fix/chloroplast-1200.png`
- `_temp/svg_aesthetic/organelle_fix/chloroplast-400.png`
- `_temp/svg_aesthetic/organelle_fix/composed-organelles-1200.png`

The corresponding editable SVGs are alongside these previews. The final composed
render uses the current organelle example through a redirected scratch output;
its source and canonical output were not changed. Cristae remain recognizable in
the small composed cell; rounded stacked sacs replace the previous ladder motif.

## References and limitations

Anatomical facts were checked independently against Cooper, *The Cell: A Molecular
Approach*, [Mitochondria](https://www.ncbi.nlm.nih.gov/books/NBK9896/) and
[Chloroplasts and Other Plastids](https://www.ncbi.nlm.nih.gov/books/NBK9905/), and
NCERT's [Cell: The Unit of Life](https://ncert.gov.in/textbook/pdf/kebo108.pdf),
section 8.5.5, for connecting stroma lamellae. These sources informed compartment
relationships only. All paths were constructed locally; Servier is a style
reference only and supplied no geometry, tracing or adapted artwork.

Construction guidance: `docs/SVG_VISUAL_STYLE.md`; SVG creator skill
`references/task_selection.md` and `references/targeted_editing.md`; its local-only
*A Handbook of Biological Illustration* lines 210-228 and 274-294 (reduction,
clarity, upper-left light, perspective), and *Mastering SVG* lines 635-687
(viewBox and viewport). The biological-spec failure report guided the regression.

This pass does not establish native LibreOffice export acceptance, independent
final specification/quality acceptance, whole-suite success, or topology for every
possible aspect ratio. Those broader final reviews remain with their assigned
owners. Illustrations are schematic, not ultrastructural reconstructions.
