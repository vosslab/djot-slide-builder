# Preferred slide colors

This reference owns the exact palette values and recorded mappings. Use
[slide-specs/COLOR_GUIDE.md](slide-specs/COLOR_GUIDE.md) for authoritative guidance on where to apply color,
how associations persist, and how question and answer states differ.

The instructor's preferred emphasis palette is independent of LibreOffice's named colors.
Use explicit hex values in Djot, for example `[Predict]{color=#D40000}`.
Preserve meaningful color relationships in the original slides; match references to the
items they identify. Course theme colors and pale background fills serve separate roles.

## Standard text palette

These values come from the HTML span styles in `replacement_rules` in
`~/nsh/PROBLEMS/biology-problems/problems/matching_sets/TEMPLATE.yml`.
Names below preserve that source's labels.

| Color | Hex |
| --- | --- |
| Red | `#D40000` |
| Dark orange | `#B74300` |
| Light orange | `#935D00` |
| Dark yellow | `#6C6C00` |
| Lime green | `#3B7600` |
| Green | `#007A00` |
| Teal | `#00775F` |
| Cyan | `#007576` |
| Sky blue | `#076DAD` |
| Blue | `#003FFF` |
| Navy | `#0067CC` |
| Purple | `#A719DB` |
| Magenta | `#C80085` |
| Pink | `#CC0066` |

## Genetics 11A red consolidation

For Genetics 11A, use the standard Red `#D40000` for every authored red, including
assessment reminders, the icebreaker, policy emphasis, contact labels, and Biochemistry
Lab promotions. This overrides the earlier dark-red reminder and icebreaker shades
and the Lab accent in this lecture. Keep the icebreaker's original typeface and size.
Local evergreen snapshots apply this lecture-specific consolidation without recoloring
other decks. Embedded photographs and artwork retain their own colors.

## Chromosome alteration names

Use full alteration names and these fixed text colors in chromosome-alteration questions.
Chromosome fills continue to identify the source chromosome; these text colors identify the
type of alteration.

| Alteration | Color role | Hex |
| --- | --- | --- |
| Deletion | Magenta-red (Pink) | `#CC0066` |
| Duplication | Forest green (Green) | `#007A00` |
| Inversion | Yellow-orange (Light orange) | `#935D00` |
| Translocation | Navy | `#0067CC` |

## Procedure sequences

Use well-separated colors from the fixed palette in rainbow order for new colored step sequences.
For six steps, use Red, Dark orange, Dark yellow, Green, Blue, Purple. For four steps, use Red,
Green, Blue, Purple. For other sequence lengths up to 14, choose evenly spaced entries from the
14 colors in the standard text palette above, including its first and last entries. Longer
sequences cycle through that palette. In randomized ordering questions, assign colors after the
display order is shuffled so colors do not reveal the correct order. Keep each repeated roadmap
identical and match step cross-references to its own method's colors. Preserve meaningful source
colors when converting existing material unless recoloring is requested.

## Genetics 11F/11G merge stages

Use five evenly spaced standard-palette colors for the five joins, restarting the
same sequence for the extension problem. Match the stage label, selected matrix
cell, new cluster label, newly added branches, and node-height label. Earlier branches
and cluster labels keep their original stage colors. Pale selected-cell fills share
the stage hue; the numbered Join labels also identify stages without color.

| Join | Text and branch color | Selected-cell fill |
| --- | --- | --- |
| 1 | Red `#D40000` | `#FFB8B8` |
| 2 | Dark yellow `#6C6C00` | `#FFFFB8` |
| 3 | Teal `#00775F` | `#B8FFF0` |
| 4 | Navy `#0067CC` | `#B8DCFF` |
| 5 | Pink `#CC0066` | `#FFB8DC` |

## Three-point testcross pairs

Reserve green for the two original parental rows and lime green for other offspring with a
parental combination for the selected gene pair. Color each pair's recombinant rows, summary
label/results, and final percentage consistently. The fixed base colors identify the pair;
lighter fills keep dark table text readable. Keep each role's hue and HSL saturation stable;
vary lightness between text/line colors and fills. Pair labels also use the base text color
so a pale background and a saturated map line have a direct visual connection.

| Meaning | Fixed palette base | Table fill |
| --- | --- | --- |
| Original parental rows | Green `#007A00` | `#8FFF8F` |
| Other pairwise parental rows | Lime green `#3B7600` | `#D6FFAD` |
| CD recombinants/results | Red `#D40000` | `#FF8F8F` |
| CH recombinants/results | Blue `#003FFF` | `#8FABFF` |
| DH recombinants/results | Purple `#A719DB` | `#DC9AF4` |

These fills use 78% HSL lightness, except lime at 84% to distinguish it from the original
parents. Saturation matches the base (100% except purple at approximately 79.5%), within
8-bit RGB rounding. Repeat these same fills in the allele-comparison diagrams and tables.

Retain gray on the covered gene column, including its intersection with colored rows.
Unknown classifications/results stay unrevealed. The six-step roadmap retains its own established
step colors; pair colors track the data through the calculation and summary tables.

## Instructor's color-wheel tool

For additional color sets, use the instructor-developed tool at
`~/nsh/PROBLEMS/qti-package-maker/qti_package_maker/common/color_wheel.py`.
Its public `generate_color_wheel(num_colors, backend="cam16", **kwargs)` API generates
perceptually distinct colors. CAM16 is the default backend; `legacy` is also available.
The module exposes named `dark_color_wheel`, `light_color_wheel`, and
`extra_light_color_wheel` dictionaries generated with modes `dark`, `light`, and `xlight`.

Returned hex strings omit the leading `#`; add it when authoring Djot color attributes.
Generated wheels are an option for additional palettes, not an exact reproduction of the
fixed template palette above. Keep chosen values explicit in slide sources so rebuilding a
deck does not depend on a sibling checkout or silently change its colors.

Choose text and background colors for their actual role and check the rendered result.
Perceptual separation does not by itself guarantee readable text contrast.
See [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md) for the instructor's presentation requirements.

## Upcoming-course promotions

Use these course identities for titles, course-summary entries, and selected teaching
labels. Keep ordinary explanatory text dark and retain the red tentative-assignment warning.

| Course | Accent |
| --- | --- |
| Biochemistry Lecture | `#6B638F` |
| Biochemistry Lab | `#C9211E` |
| Cellular and Molecular Biology | `#24578F` |
| Biology and Ethics in Film | `#45405C` |

### Genetics distance-matrix teaching cues

In 11D/11E, purple row/column bands identify genes or clusters being merged. Each
new distance uses one shared cell fill and text color across the original pairs and the
matching calculation: teal #00775F/#B8FFF0, blue #0067CC/#B8DCFF, orange #B74300/#FFD2B8,
and purple #A719DB/#F0B8FF. Distance-matrix labels and values are centered.
