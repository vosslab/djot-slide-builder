# SVG visual style

Use one coherent family of locally authored scientific illustrations: clear silhouettes,
recognizable anatomy, restrained depth, and readable live labels. The audience is upper-level
biology students viewing slides over Zoom. A figure must explain its subject at slide size.
The API and composition contract remain in [SVG_TOOLKIT.md](SVG_TOOLKIT.md); provenance and
native slide rules remain in [slide-specs/SVG_DIAGRAMS.md](slide-specs/SVG_DIAGRAMS.md).

## Visual direction

Servier Medical Art is a **style reference only** for calm semi-flat 2.5D illustration: broad
color masses, soft contour changes, shallow depth, and selective internal structure. Author
all geometry locally from biological requirements. Do not import, trace, adapt, or copy Servier
paths or images. General drawing principles inform the work; external silhouettes do not
become local artwork through recoloring.

Begin with the silhouette, then add the structures that identify the subject. Use overlap and
two or three flat tones to describe volume. The characteristic anatomy should remain clear
when the shading is removed. Organic contours can be slightly asymmetric, but each deviation
should express form. Keep schematic relationships and plots geometrically direct.

### Shape and line hierarchy

For a nominal biological part whose shorter dimension is 100 drawing units:

| Element | Starting weight | Purpose |
| --- | --- | --- |
| Outer contour | 2 units; usually 1.6-2.2 | Establish the silhouette. |
| Internal anatomy | 1 unit; usually 0.8-1.2 | Explain structure without dividing the body into heavy fragments. |
| Fine optional detail | Omit if it disappears at slide size | Protect the teaching feature from visual noise. |
| Process connector | Match nearby contour weight | Show direction or contact clearly; retain arrow meanings. |

These values are drawing defaults, not quantitative biological measurements or acceptance
thresholds. Scale contour widths from the shorter dimension, capped at 3 drawing units for
large containers, so their outlines do not overpower internal anatomy. Bake anisotropic geometry before applying a
uniform stroke where the existing implementation needs it. Preserve intentional separate
weights for small icons, data axes, sequence tracks, and other established conventions.
Use rounded caps and joins on organic contours. Retain square or crisp boundaries when they
communicate a measurement, gene interval, or diagram structure.

### Color and depth

Preserve caller-supplied and course-specific semantic colors. Follow
[slide-specs/COLOR_GUIDE.md](slide-specs/COLOR_GUIDE.md): a course theme and a biological identity
serve different purposes. Stable gene, phenotype, chromosome, and sample associations take
precedence over decorative palette changes.

Use `#344651` as the shared charcoal contour and default label color where suitable against
the background. Use a base body fill plus one darker same-family plane, optionally adding a
small lighter plane. As an initial visual recipe, use about 12-18% darkening and 15-25%
lightening; adjust from rendered evidence. Native SVG opacity overlays are acceptable and
keep caller colors usable without adding a color parser. Inspect the resulting color on the
actual base fill and background.

Place light toward the upper left and shading toward the lower right. Keep tone shapes
inside the silhouette and use them to explain curvature, a fold, or a near/far surface.
A small highlight is optional. Flat explanatory boxes, gene tracks, and data plots do not
need highlights. Biological state must not depend on a decorative shine, shadow, or hue alone.

Avoid broad cast shadows, glossy spots, gradients that disguise anatomy, and texture added
only to make a blank area busy. Keep a transparent SVG background when the composition
allows it; gallery previews can use white. Inspect fine edges on the intended slide surface.

### Text and composition

Use Atkinson Hyperlegible Next for editable labels, and Atkinson Hyperlegible Mono for
aligned sequences. The fonts are installed renderer dependencies, not embedded live fonts.
Use the existing text helpers for measurement, wrapping, gene italics, and scripts. Keep
text horizontal when possible, with a consistent visual hierarchy across related panels.
Preserve labels, values, scientific notation, ordering, and relationship meanings.

Place labels next to their objects with clear whitespace. Use callouts only when a direct
label is ambiguous. Keep title and caption text native in Djot; an SVG is one illustration
with its associated object labels. Preserve existing teaching content while adjusting the
layout. Review the whole figure at its actual slide placement; a readable standalone image
can become unreadable in a small panel.

## Family-specific recognition

| Family | Feature that must carry identity | Treatment |
| --- | --- | --- |
| Cells and nuclei | Cell envelope, wall where specified, and separately authored nuclear counts | Use a soft silhouette and a modest lower plane. Preserve fused yeast continuity and caller-placed contents. |
| Mitochondria | Envelope and folded inner membrane | Distinguish membrane boundaries and open fold spaces; shading supports the body. |
| Chloroplasts | Envelope, stacked thylakoids, and connecting lamellae | Make stacks legible as structures rather than decorative stripes. |
| ER and Golgi | Distinct cisternal arrangements | Keep generic ER generic; use layered curved Golgi sacs with clear gaps. |
| Lysosomes and vesicles | Membrane boundary and caller-defined contents | Keep simplified identities explicit in labels; invent no diagnostic contents. |
| Membranes | Two leaflets, heads outward, tails inward, deliberate gaps | Keep the bilayer readable along bends; do not obscure insertion or receptor contacts. |
| Proteins and ligands | Distinct silhouettes and binding/contact sites | Use smooth locally authored lobes and contained planes; preserve active/inactive labels and phosphorylation independence. |
| Antibodies and binding | Two Fab arms, Fc stem, correct contact topology | Round the body without moving contact anchors; show binding through contact, not mere proximity. |
| Chromosomes | Arms, centromere, homolog identity, and supplied bands | Preserve lengths, loci, bands, and segment identities; restrained tone supports the cylinder. |
| Gene tracks | Exon/intron, strand direction, and supplied offsets | Keep intervals and arrowheads crisp and flat; never make a drawing length look measured unless it is. |
| Phenotypes | Visible round/wrinkled contrast and preserved color classes | Use shape and folds before tone; generic radial flowers remain generic wildflowers. |
| Diagrams and icons | Reading order, connector semantics, and object identity | Keep boxes quiet, icons optically consistent, and labels dominant over decoration. |
| Plots | Exact values, labels, axes, units, uncertainty, and series identity | Use clean flat marks, restrained grids, and coordinated typography; no pictorial depth. |

These are drawing conventions for the existing schematic toolkit. They do not authorize new
anatomical claims, content inference, automatic organelle counts, or changed biological states.
Check the owning lecture and source facts whenever a visual alteration could change meaning.

## DNA and scale boundary

Retain the original Genetics LECT02 `b_dna_helix.drawn.svg` unchanged. It is an existing
course illustration, not an upgrade target. Calling a schematic "not to scale" means that
its pitch, diameter, and distances are not quantitative claims. It does not justify changing
strand connectivity, orientation, handedness, or the feature being taught. The aesthetic
upgrade does not introduce a new B-DNA model or a measured-pitch claim.

## Editable SVG delivery

Keep existing callable APIs, named anchors, and biological meanings stable. Bounds cover
all painted geometry, stroke, and labels. New shade planes must fit the source silhouette;
features outside it need deliberate bounds and attachment-point review. Preserve deterministic
static vector output, unique grouped IDs, live text, and useful accessibility descriptions.
Use established helpers and installed dependencies; add only mechanics required by actual
families. An isolated shading patch does not need a new configurable rendering system.

Verification is both structural and visual. Inspect a representative part at small and large
sizes, then inspect composed galleries and the actual native slide exports. Compare against
the saved baseline for silhouette, internal structure, tone, line hierarchy, label legibility,
clipping, and stable semantic colors. Judge figures together as a family. A passing XML parser
or screenshot hash is not aesthetic acceptance.

## Reference background

Servier's current official [image-use guidance](https://smart.servier.com/using-smart-images-what-you-can-do/)
states CC BY 4.0, also described in its
[citation guidance](https://smart.servier.com/how-to-cite-servier-medical-art/).
The local Bioicons copy contains historical Servier entries in `static/icons/cc-by-3.0/`,
and the [Bioicons README](https://github.com/duerrsimon/bioicons/blob/main/README.md) illustrates
CC BY 3.0 attribution. Those are separate source records; a local historical license label
is not evidence of the current website's license. Both are background references here.
No Servier-derived geometry enters this upgrade, and the project's own artwork licensing
continues to apply to its locally authored outputs.

The following machine-local passages informed this guide. They are conceptual drawing
references, not current biological authorities or required files for a clean checkout.
Paths below are relative to the corresponding skill's `references/` directory under
`/Users/vosslab/.codex/skills/experts/`.

| Skill and local source | Passage | Applied decision |
| --- | --- | --- |
| `svg-creator-expert`: `local-only/scientific_illustration/A_Handbook_of_Biological_Illustration-1988.md` | Lines 274-294: observation, clarity, shading convention, perspective | Teach the identifying feature, retain open spaces, use upper-left light and line hierarchy. |
| `svg-creator-expert`: same handbook | Lines 210-228: reduction and copy size | Inspect the rendered figure at its real slide size before accepting detail. |
| `svg-creator-expert`: `local-only/svg_authoring/Mastering_SVG-2018.md` | Lines 635-687: viewBox and viewport | Keep drawing units, viewport scaling, and visible bounds explicit. |
| `css-creative-expert`: `local-only/css-creative/Working_With_Colors_Guide-2016.md` | Lines 330-342: color, atmosphere, shadows | Use value relationships to explain depth while preserving semantic hues. |

The CSS reference informs visual craft only. This toolkit produces static SVG rather than
interactive CSS; browser effects, animation, filters, and a new cascade system are outside
the requested scope.
