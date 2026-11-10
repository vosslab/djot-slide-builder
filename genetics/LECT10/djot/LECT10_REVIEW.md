# Lecture 10 conversion review

Current revision and verification appear first. Earlier conversion proposals, inventories, and
checks are preserved in [LECT10_CONVERSION_HISTORY.md](LECT10_CONVERSION_HISTORY.md).
Original ODP/PDF files remain unchanged.

Rejected LLM drawings and future repair targets are inventoried in
[SVG_REPAIR_BACKLOG.md](../../../docs/SVG_REPAIR_BACKLOG.md). Eleven drawings have been removed,
including the four chromosome-shape drawings in the final queue pass. The inventory
records exact paths, source baselines, current replacements, and the teaching detail to restore.

## November 10 chromosome topic boundaries

Add Chromosome Arms before the first band/arm figures and Chromosome Groups before the A-G
sequence in 10C. Keep Reading Chromosome Addresses and Reading a Karyotype as subsections
within Chromosomal Positions, with Summary as the closing section. All 28 existing slide blocks
remain unchanged and in order; the two inserted subsection cards bring the deck to 30 slides.
Temporary source comparison and rendered cards: `_temp/lect10c_subsections/`.
Native lint passed; rebuilt ODP/PDF and visually checked both blue subsection cards.

## November 10 HeLa bullet hierarchy

Restore B48 from original B45's native ODP paragraphs and PDF: the death-date detail belongs
under the Henrietta Lacks origin point; contamination belongs under durability/proliferation.
Restore the omitted oldest/most commonly used cell-line point and original wording. Remove the
conversion's added date and name mnemonic from this slide. Keep all other slides unchanged.
Temporary comparison and render: `_temp/lect10b_hela_hierarchy/`.

## November 10 Brainbow teaser

At the instructor's request, shorten B28 Command and Control Center into three brief teaching
points about neuronal circuits, fluorescent protein combinations, and distinguishing neighboring
neurons. Use the existing two-panel layout to pair native text with the original B31 Brainbow
micrograph (`image_021.jpg`). Keep the full-size micrograph on B31 and the B29-30 mechanism
figures in place. All other source blocks remain unchanged, with 55 slides. Temporary source,
export, and rendered comparison: `_temp/lect10b_brainbow/`.

Rebuilt and visually inspected B28. The text and original micrograph are readable side by side;
the other 54 source blocks and PDF page word sets remain intact. Native lint and capacity pass,
along with 327 focused source/link/guidance checks. No permanent tests were added.

## November 10 SKY explanation and comparison

The instructor selected established B22-23 for a wording/format revision. Shorten B22 into a
probe-library, sequence-matching, dye-combination, and software-readout sequence. Keep complete
short statements and move the yellow/red display example into teaching notes. The chromosome
type, rather than a particular homolog, receives the color identity.

Use two editable panels on B23: mFISH in orange `#B74300`, SKY in purple `#A719DB`, with dark
supporting text and the original 1996 author references in the footer. Repeat purple on B22's
SKY label. Titles remain black; the G/R-band teal/magenta key retains its separate role.
The comparison contrasts separate filter images with spectral readout. Preserve 55 slides and
all other source blocks. Temporary source/export comparison and renders:
`_temp/lect10b_sky_voice/`.

Check the technical wording against the original primary reports:
[Speicher et al., 1996](https://www.nature.com/articles/ng0496-368) describes chromosome paints
labeled with different fluor combinations, filters, and software;
[Schrock et al., 1996](https://pubmed.ncbi.nlm.nih.gov/8662537/) describes chromosome-specific
spectra and computer classification. This replaces the oversimplified one-dye-per-chromosome
wording. Both method-label colors meet 5.5:1 against the actual white panel surfaces.

Rebuild and visually inspect B22-23. Native styles preserve the orange/purple labels, and
neither page has off-page text or capacity concerns. The other 53 source blocks and PDF page
word sets remain unchanged. Source/ODP/PDF counts agree at 55, and both B answer reveals remain.
Native lint and 327 focused source/link/guidance checks pass. No permanent tests were added.

## November 10 sections and ultralight

Restore the three major sections as the organizing structure for A. The opening remains title,
agenda, weather, icebreaker, Next Week (A1-5). Informational Slides occupies A6-12. Course Content
is A13-29, with the assessment schedule at A23 and Quiz 5 Vote at A24-27 in the normal Quiz
position before Weekly Assignments. General Announcements is A30-44: add a Movie Night
subsection at A31, then the original setup, four choices, and poster vote at A32-37, followed by
registration. Every pre-existing source block and hidden flag is preserved; only a new Movie Night
subsection card is added. A now has 65 authored / 45 visible / 20 hidden slides. Lecture totals
are 213 authored / 193 visible / 20 hidden. This supersedes the earlier front-loaded vote order.

Set ultra light to 90% HSL lightness across all four course palettes, retaining the original
accent hue/saturation within 8-bit rounding. Genetics is `#D6E5F5`, Biostatistics `#D3F8D9`,
Biochemistry `#E3E1EA`, and Biotechnology `#F8D3D3`. Dark/medium/light values remain unchanged.
The regenerated source-derived palette audit passes all 44 role-specific comparisons, with
minimum text contrast 7.13:1. Rebuild all four LECT10 ODP/PDF decks. Temporary source-order,
palette, contrast, and rendered evidence: `_temp/lect10a_sections_ultralight/`.

Visually inspect the new cover/icebreaker tint and the section/vote boundaries. All 44 prior A
page word sets remain, plus the new Movie Night card. Source/ODP/PDF counts agree across all
four decks and all eight native answer reveals remain. Native lint passes. The full base suite
passes 5,907 checks with the same two pre-existing LECT14/15 agenda-cover failures outside this
LECT10 scope. Existing A weather/movie/contact/registration font-size advisories remain.

## November 10 WebP weather snapshot

Refresh the current A3 weather story with the updated script: validate the NWS PNG, then save
only a quality-90 WebP at the original 1536x864 dimensions. The current graphic falls from
1,962,461 PNG bytes to 229,772 WebP bytes, an 88.3% reduction. Only the weather image path
changes in the source; the full editable caption and dated citation remain intact.

Rebuild A and visually inspect its exported weather page. The ODP embeds the WebP directly;
all 44 visible page word sets remain unchanged. Existing size advisories remain. The focused
weather/link/guidance suite passes 224 checks. Historical snapshots in other decks retain their
existing paths. Temporary encoding, size, export, and rendered evidence: `_temp/weather_webp/`.

## November 10 chromosome-shape restoration

The queue-completion audit found that the four recommended chromosome-shape reversions had
remained recommendations. Restore B33-36 to their original textbook PNGs, verified byte-for-byte
against the original ODP: `image_022.png` through `image_025.png`. The original figures better
preserve replicated-chromosome structure, spindle relationships, unequal arms, and the V/J/I
shape distinctions. Retain native editable slide headings and the existing matching exercise.
All other B source blocks remain intact, with 55 slides. Update the rejected-SVG inventory to
eleven completed removals; retain the SVG source files for future repairs. Temporary comparison
and rendered verification: `_temp/lect10b_shape_restore/`.

Rebuilt all four current LECT10 ODP/PDF decks and visually inspected the four restored shape
pages. The other 51 B pages retain their PDF words; all four original PNG byte streams are
embedded unchanged. ODP/PDF counts agree at A64/44 (20 hidden), B55/55, C28/28, and D65/65.
All eight native answer reveals remain. Native lint and 327 focused source/link/guidance checks
pass. All eleven rejected drawings remain available for repair and have no current LECT10
references. Existing A weather/movie/contact/registration font-size advisories remain.

## November 10 lecture-day weather refresh

The previous A deck kept a hidden November 1 weather story. Run the existing weather script
with `--write` on November 10, matching the lecture date. It retrieves one NWS Chicago Five Day
Outlook, saves the original PNG, retains its full editable caption and dated citation, and makes
the weather visible as A3 before the icebreaker (now A4). All other source blocks remain intact.
A retains 64 authored slides, now 44 visible and 20 hidden. The movie vote moves to A17 and
contact slides to A23-24. Lecture totals are 212 authored / 192 visible / 20 hidden.
Clarify the required today/tomorrow script step and visibility check in the announcement guide.
Temporary source/export comparison and rendered evidence: `_temp/lect10a_weather_refresh/`.

Rebuilt and visually inspected A3: the graphic is dated November 10, 2026 at 3:29 AM, and the
complete caption and dated source are readable. The full caption remains editable; the original
PNG is embedded unchanged. All other source blocks and all 43 prior visible page word sets are
unchanged. ODP visibility agrees with the 44-page PDF. Native lint and 222 focused weather/link/
guidance checks pass. The weather caption fits at 16 pt, below the 18 pt capacity target; existing
movie, contact, and registration size advisories remain.

## November 10 original homolog question restored

Original B15 (current B16) asks about a pair in a human karyotype. The conversion replaced
its wording and choices, adding "even before DNA replication" to the X-shaped choice and
changing the original answer from all of the above to A-D. Restore the original stem and
five choices, with only "maybe" corrected to "may be" in the instruction. Keep the native
answer reveal and restore "Answer: all of the above". On B17, replace the generated explanation
with the original answer traits and original chromosome-pair figure; put the replicated-karyotype
context in speaker notes. All other B source blocks remain intact, with 55 visible slides.
Temporary original/current comparisons and rendered evidence: `_temp/lect10b_question_compare/`.

Rebuilt and visually inspected B16-17. The original stem and all five choices match the original
ODP; the original answer figure is embedded byte-for-byte. Native XML retains the on-click answer
reveal. The other 53 source blocks and PDF page words are unchanged. Source/ODP/PDF counts agree
at 55, with no off-page text on the changed pages. Native lint, capacity, and 325 focused
source/link/guidance checks pass.

## November 10 banding color roles

On B12-14, use teal (`#00775F`) for G-bands/heterochromatin and magenta (`#C80085`) for
R-bands/euchromatin. Reserve these cues for the contrasted labels; Giemsa, shared condensation,
and explanatory prose remain neutral. Remove generic blue/gold emphasis from the generated
objectives, homolog question/explanation, chromosome-painting definitions, and takeaways while
retaining their bold text. Preserve the original wording and images, original red karyotype
term, chromosome-shape color key, answers/reveals, 55-slide count, and blue course theme.
Document the comparison key in the color guide. Temporary native/source/contrast checks and
rendered evidence: `_temp/lect10b_color_roles/`.

Rebuilt and inspected the eight changed pages. All 55 PDF pages retain their words; native
run checks confirm the seven G/R/chromatin label occurrences use the intended colors, with
Giemsa and shared condensation in neutral text. Native labels contrast at 5.52:1 (teal) and
5.53:1 (magenta) on their actual white surface. Original figures retain their source colors.
Native lint, capacity, and 325 focused source/link/guidance checks pass.

## November 10 opening chromosome-set question

The original 10B ODP/PDF has "Sets of Chromosomes in Human Cells" with its two explanatory
bullets on the same slide; neither original contains a separate question-only card. Restore the
instructor's intended early discussion by adding B5 as `question-ask`: "How Many Sets of
Chromosomes in Human Cells?" Original/current answer wording remains unchanged on B6.
Speaker notes distinguish two sets of 23 chromosomes in somatic cells from 23 homologous pairs
and one set in gametes. All pre-existing B source blocks remain intact and in order.
B now has 55 visible slides. Temporary comparison and rendered evidence:
`_temp/lect10b_opening_question/`.

Rebuilt and inspected B5-6. The new question is editable; all 54 prior source blocks and visible
page texts remain unchanged in order. ODP/PDF agree at 55 slides. Native lint and capacity
pass, along with 325 focused source/link/guidance checks.

## November 10 movie-vote poster size

The existing A16 vote recap already used the `four-panels` layout. Its two rows constrained
portrait posters to about 115-118 pt tall. Use the existing `gallery` layout instead: four posters
across at 257.19 pt tall, about 2.2 times their former height. Keep the same image order and
original poster files, current title, and editable movie-name/year legend in the footer. All
other A source blocks remain unchanged; A retains 64 authored / 43 visible / 21 hidden slides.
This revision changes authoring only; the shared pipeline remains unchanged. Temporary comparison
and final rendered evidence: `_temp/lect10a_vote_layout/`.

Rebuilt and inspected A16. Only the vote source block changes; all 43 visible pages retain their
words (the legend adds separators), and the four original poster byte streams are embedded
unchanged. The vote page has no capacity warning; the prior movie-description/contact/registration
advisories remain. After both restorations, native lint passes across 211 authored slides and
94 images; 325 focused source/link/guidance checks pass.

## November 10 chromosome groups restored

The instructor identified a substantive coverage error: original C5-7 taught chromosome groups
in three consecutive "Karyotype Definitions" slides before "Banding Pattern". The conversion
collapsed this sequence into two Summary references and explicitly labeled it untaught. Those
labels and that classification are superseded by the instructor's correction.

Restore all three teaching steps as C9-11, preserving the original sentences about seven groups
A-G, X in C, and Y in G, the original chromosome 13-17 and X/Y figures, and the original SRY locus
callout (Yp11.3). Use native editable text with existing layouts; retain the five component colors
in the restored address. C12 is now Banding Pattern. Add chromosome groups to the generated
objectives. Remove the two former Summary references; 10C now has 28 visible slides.

The CFTR question/answer/enlarged figure move to C15-17; the band-order question/answer to C19-20;
the karyotype table/question/answer to C22-24; Summary to C25. Original covers and all other
teaching blocks remain intact. Temporary original/source/export comparison and rendered checks:
`_temp/lect10c_groups_restore/`. The voice and pedagogy guides now explicitly preserve the
instructor's coverage decisions and repeated visual teaching sequence.
Rebuilt and visually compared C9-11 with original C5-7. Original group sentences, all other
source blocks except the expanded objective, and both native answer reveals are preserved.
ODP/PDF counts agree at 28; no exported text is off-page, and capacity reports no concerns.
The original SRY address is preserved as authored; this pass restores coverage rather than
rechecking every original scientific claim.

The instructor also suggested course-aware general accents: teal/magenta for Genetics and
blue/gold for Biotechnology. Record the generic selection principle in the color guide; retain
the approved address-component key and existing authored content while evaluating this suggestion.
Preferred teal `#00775F` and magenta `#C80085` each exceed 5.5:1 against white,
but measure approximately 2:1 against the sampled header blue `#6F9FD5`. General accent hue
selection complements the explicit-black question-header treatment; the five-part address key
and existing authored emphasis remain intact.

## November 10 question-header contrast

Set both 10C multiple-choice stems (C16 and C20) explicitly black over the course header gradient.
C20's current ODP used dark navy; black gives clearer separation from the blue surface. C16's
new component colors also crossed that gradient; keep the stem neutral and retain the component
key throughout its choices and worked answer. Words, choices, reveals, and 27 slides remain.
Check the rendered gradient under the whole prompt footprint, rather than assuming white.
Document this treatment in the color guide. Temporary evidence: `_temp/lect10c_question_contrast/`.

Rebuilt and visually checked C16/C20. The first question paragraph is explicitly `#000000` in
both ODP styles and PDF text. Sampling the rendered horizontal gradient at every row across
the complete prompt footprint gives a minimum 7.596:1 contrast (darkest background `#6F9FD5`),
above the 5.5:1 target. All 27 visible texts and both native answer reveals remain; only C16/C20
source formatting changes in this pass. Native lint, capacity, and 325 focused checks pass.

## November 10 address-color continuity

Carry the established five component colors through 10C's editable definitions, question prompts,
complete addresses, band-order choices and answers, address ranges, and takeaways. Chromosome
red, arm orange (both p and q), region green, band blue, and subband purple now keep their roles
instead of recoloring a whole address for proximity or answer status. Region numerals in the
worked comparison share green. C12's target address remains neutral while students identify its
parts; C16 treats every alternative equally and retains its answer reveal. Preserve all words,
27 slides, existing table font/alignment overrides, original figures, and separate karyotype keys.
Document the reusable address key in [COLOR_GUIDE.md](../../../docs/slide-specs/COLOR_GUIDE.md).
Temporary comparison and contrast/render evidence: `_temp/lect10c_address_colors/`.

Rebuilt ODP/PDF and inspected the twelve color-key/context pages. All 27 visible pages retain
their words, both native reveals remain, and no PDF text extends off-page. Native table runs
match the component key; colors against actual white cell fills measure at least 5.5027:1.
All six source text colors pass the 5.5:1 white-background audit. The extraction invocation
enables `.djot` locally for the skill scanner; shared skill files are unchanged. Native lint
passes across 210 Lecture 10 slides and 92 image references. Capacity reports no concerns for
10C; 372 focused table/source/link/guidance checks pass. No permanent tests are added.

## November 10 address-table emphasis

Center and enlarge the key cells in 10C using the existing per-cell overrides, following the
10D trisomy table. C11 uses centered bold 28 pt part labels and 30 pt example tokens; their
colors match the existing C13 address components. C13 uses 32 pt address parts, and C19 uses
36 pt karyotype parts. Reduce vertical padding on the five-row tables to preserve readable
left-aligned explanations. Center their identifying column headers. C15's two comparison addresses use centered bold 32 pt text. Wording, answers,
figures, order, and the 27-slide count remain unchanged. Temporary rendered checks and native
cell verification: `_temp/lect10c_table_emphasis/`. Rebuilt and visually inspected all four
tables; native cell sizes, centering, and bold text agree. All 27 pages retain their words.
Native lint, capacity, and 261 focused table/documentation checks pass.

## November 10 chromosome band figures

Replace the insufficient unbanded chromosome-arm and CFTR hierarchy SVGs in 10C with the
original banded figures. C5 pairs original chromosomes 1-3 with 21-22, as in original C2.
C8 restores the original C4 full-width chromosome 11-14 band diagram. C13 pairs the existing
editable answer table with the original CFTR chromosome-7 figure, explicitly showing region 3,
band 1, and subband 2. C14 retains the enlarged original figure for discussion. C12 remains an
unanswered question. The "Landmarks, not a band map" text leaves the deck with its discarded
SVG references; earlier favorable assessments of those replacements are superseded.
Keep 27 slides and all other source blocks unchanged. Temporary comparison and rendered
verification: `_temp/lect10c_band_restore/`.

Rebuilt ODP/PDF and visually inspected C5, C8, C13, and C14. Both exports retain 27 slides;
source comparison limits this pass to C5/C8/C13, and the original image bytes are embedded
unchanged in ODP. Native lint, capacity, and 325 focused source/link/guidance checks pass.

## November 10 prenatal raster restoration

At the instructor's request, replace the SVG drawings on D54 (Amniocentesis) and D55
(Chorionic Villus Sampling) with the original labeled raster figures. Render each complete
figure from original D28-29 at 3x, preserving the overlaid anatomy/workflow labels and credit;
the separate imported JPEGs alone omit those labels. Keep current editable titles, order, and
all 65 slides. Earlier positive assessments of the replacement SVGs are superseded.
Temporary comparison and rendered evidence: `_temp/lect10d_prenatal_raster/`.

## November 10 Down syndrome sequence

The instructor's original D13-20 already follows the broad sequence retained by the conversion:
karyotype, forms, prevalence/survival, health, maternal-age graphs, and cohesion. The conversion
substantially rewrote the fertility answer from original D43, losing its numerical evidence and
men/women contrast. This follow-up restores that teaching point and improves the visual sequence.

- D32: new `subsubsection` for Down Syndrome within Autosomal Trisomies.
- D33-36: karyotype, three forms, survival, then health. Pair the original standalone photograph/
  karyotype from former D39 with the established health wording on D36 (formerly D35).
- D37-39: incidence graph, maternal-age context, then a new two-state cohesion schematic.
  Blue sisters and orange cohesin rings distinguish maintained versus weakened connections.
  Labels remain editable text. The schematic is illustrative, not microscopy or a measured
  age comparison, and cites [Tsutsumi et al. (2014)](https://doi.org/10.1371/journal.pone.0096710).
- D41: retain the `question-ask` pause, "Can People with Down Syndrome Have Children?"
- D42: restore the original women/men contrast and four pregnancies fathered by three men,
  explicitly dated as of 2005. Keep male fertility frequency uncertain while acknowledging
  documented paternity. The historical counts come from the instructor's original D43;
  [Pradhan et al. (2006)](https://doi.org/10.1016/j.fertnstert.2006.03.071) and the
  [2015 primary case report](https://pmc.ncbi.nlm.nih.gov/articles/PMC4595396/) support documented
  male fertility. They are not a current census or a claim of universal male sterility.
- D43-48: retain the explicit segregation-model assumptions and answer. D44 becomes the
  `subsubsection` "How Three Homologs Separate during Meiosis", introducing the visual explanation.
  D42 returns to the original offspring question, removing the duplicate homolog-separation prompt.

Adding the divider and pairing the loose image keeps 65 authored/ODP/PDF slides. D1-31 and D40-41,
D43, D45-65 remain unchanged in source. All original images remain present; the two new SVGs use
no external resources. One-time comparison, XML checks, and rendered review are under
`_temp/lect10d_down_revision/`; this content revision adds no permanent tests.

Rebuilt the editable ODP and PDF and visually inspected D32-48, including the two-state
schematic at full size. All 65 pages fit; capacity reports no concerns, all 30 original image
references remain, and exported text is selectable with no off-page text. Strict native lint
passes for all four Lecture 10 sources (210 authored slides, 93 image references). The 214
focused documentation checks pass. The full base suite has 5,901 passes and two cover failures
in the unchanged Lecture 14/15 agenda-only sources, outside this Lecture 10 revision. Image-free
authored schematics use the repository's tracked `.drawn.svg` suffix.

## November 10 presentation order and trisomy table

The ordering below is superseded by
[the section-grouping correction](#november-10-sections-and-ultralight). The D30 table styling remains.

Reorder 10A as approved: cover, agenda, icebreaker, Next Week, quiz schedule and Quiz 5 vote,
movie choices and movie vote, then the routine announcements. All existing source blocks, wording,
images, and hidden states remain. The icebreaker is A3, Quiz 5 vote is A7-10, movie choices are
A12-15, and the movie-vote recap is A16. Counts remain 64 authored / 43 visible / 21 hidden.

On D30, make chromosome numbers 13, 18, and 21 bold, centered, and 36 pt. Match each to the
existing syndrome color: Patau green, Edwards orange, and Down blue. Keep the table editable and
leave D31's two-image layout as it is. Native `font-size` cell overrides now participate in column
widths, row heights, and text export. Temporary verification: `_temp/lect10a_order/` and
`_temp/lect10d_30/`.

Rebuilt all four decks; native lint passes. The D30 colors measure 5.52-6.66:1 against their white
cells. The 94 focused table/export checks pass; the full suite has 5,897 passes and two cover
failures in the Lecture 14/15 agenda-only sources, outside this Lecture 10 pass.

## November 10 movie choices

Add the four choices from `~/genetics/LECTURES-2026-351genetics/movie_choices.odp` after the
existing Movie Night introduction: Our Times (2025), Biosphere (2023), Vesper (2022), and
The Animal Kingdom (2023). The supplied ODP is authoritative; its text differs from the older
companion PDF. Preserve its wording, ratings, list hierarchy, and four original JPEG posters.
Use the new `movie-panel` layout, with editable text on the left and a narrower 2:3 poster area
on the right. A fifth inserted page recaps the titles and posters for the vote.

10A now has 64 authored / 43 visible / 21 hidden slides. B-D remain 54, 27, and 65 visible pages,
for 210 authored / 189 visible overall. Earlier review counts and page references below describe
their preceding revisions. Temporary source comparison and visual evidence: `_temp/movie_panel/`.

Rebuilt 10A and inspected all five inserted pages, the introduction, icebreaker, and contact
slides. Poster bytes and every movie paragraph/rating match the supplied ODP; the other 37 visible
pages retain their text. All 5,880 base tests and strict native lint pass. Full descriptions fit at
15.5-16.75 pt; this remains denser than the ordinary 20 pt house target.

## November 10 instructor wording correction

The preceding voice review overreached: established instructor prose was changed into fragments,
and incidental emphasis made some announcements harder to read. Restore the pre-review wording
and emphasis on 39 established-content B-D pages. Restore 10A's shared announcement prose,
first-person policies, and homework encouragement. Current dates, earlier scientific corrections,
question layouts, eight answer reveals, and the D59 table-width repair remain intact. The voice
review applies to LLM-authored additions; established instructor slides supply the baseline.

The contact slide uses the original full-width wording with colored method labels and dark
details. Anonymous-message instructions use the original prose in regular dark text, paired with
the existing form image and visible link. Verification and final renders for this correction are
temporary under `_temp/contact_restore/`.

Rebuilt all four editable ODPs and PDFs and visually reviewed the 53 restored/changed visible
pages. The 39 B-D restorations match their pre-review source blocks exactly. Source/ODP/PDF counts
remain 205 authored / 184 visible with eight native answer reveals; contact links remain clickable
and exported text remains selectable. Strict native lint and 213 documentation/guidance checks
pass. No PDF text extends beyond its page. The contact body has a 19.5 pt capacity advisory;
two registration regions have 19.75 pt advisories. Their restored prose fits the rendered slides.
The existing hidden weather-caption advisory remains. No permanent tests were added.

## November 10 text and color review (superseded in part)

The initial pass revised wording or emphasis on 96 pages and inspected 112 text-rich or changed
pages. The instructor rejected its edits to established prose; the correction above supersedes
those changes. The retained LLM-authored material preserves all eight answers/reveals and the
D59 table-width fix. Earlier one-time evidence remains under `_temp/lect10_text_review/`.

## November 10 appearance reference

The instructor's nine-page `section_headers.odp` / `section_headers.pdf` supplies the appearance
reference. Match its appearance and color roles with editable text and the measured course palette:
dark framed sections, light center bands with medium edges for subsections, dark inset subsubsections with
light edges, and ultra light question-to-ponder hexagons with dark corners. Icebreakers use a
separate prompt/examples card. Cover cards are ultra light,
headers fade from medium to white, and THE END uses ultra light text on dark color.

Rebuilt all four Lecture 10 decks and the seven Lecture 09-15 agenda decks with these defaults.
The following whole-lecture comparison records the preceding content review; this follow-up
checks the new styles in all four course colors and selected Lecture 10 contexts. Counts and
content remain unchanged. All 44 measured color pairs pass (minimum text contrast 6.81:1),
all 5,878 base tests pass, and strict native lint passes. The current implementation uses native
master shapes with editable slide text; decoration editability is optional. The 36 design-proof
pages and 14 catalog prompts have rendered review; existing weather, registration, and newborn-table
capacity advisories remain.

The instructor identified Genetics 04H slide 5 and 06D slide 43 as question-to-ponder examples.
Both now use `question-ask`, as do the existing question-only dividers on 10D pages 41 and 44.
Use this treatment sparingly. Rebuilt and visually checked those four cards and the separate
10A icebreaker; wording, source positions, and slide counts remain unchanged. Question cards
contain one centered question; icebreakers retain their required examples and suggestions.

Reference extraction, palette evidence, final renders, and artifact checks are temporary under
`_temp/section_headers_reference/`. Existing behavior/export tests cover the shared contracts;
the lecture-specific renders and measurements add no permanent fixtures or tests.

## November 10 slide 26 readability

Restore full-width choices on D26, corresponding to original D39. Shorten the shared setup,
state the choices as counts out of four gametes, and emphasize one daughter cell and meiosis II.
The existing adaptive layout now fits every choice on one line at 28 pt, with the answer popup
below. Rebuilt and visually checked the PDF; text is editable in ODP, Answer C retains its reveal,
and all 65 source/ODP/PDF pages remain. Source comparison confirms only D26 changed in this pass.
Temporary evidence: `_temp/lect10d_26/`.

## November 10 whole-lecture comparison

**Assessment: improved overall for classroom use.** Reviewed the four original PDFs beside the
current LibreOffice-rendered Djot exports: all 149 original pages and all 184 current visible
pages, using the migration-comparison criteria in the
[visual rubric](../../../docs/slide-specs/SLIDE_VISUAL_REVIEW_RUBRIC.md). This is an instructional
revision with deliberate consolidations, new practice, reordered explanations, and corrected
claims; it is not a claim of word-for-word preservation or improved student learning outcomes.

| Deck | Original visible pages | Current authored / ODP | Current visible PDF | Hidden |
| --- | --- | --- | --- | --- |
| 10A announcements | 25 | 59 | 38 | 21 |
| 10B karyotypes | 50 | 54 | 54 | 0 |
| 10C nomenclature | 19 | 27 | 27 | 0 |
| 10D aneuploidy | 55 | 65 | 65 | 0 |

The original announcements ODP also contains 37 hidden slides (62 authored total). Their text
was compared separately from the visible-page review. Current hidden groups retain quiz policies,
exam preparation, first-week reminders, evaluations, and club information. Dated homework,
graduation, registration, and movie-form alternatives are superseded or retired. The current quiz
guidance uses in-class groups of 3-4; the original Zoom breakout instructions are gone. Hidden
slides received a text comparison, rather than the full rendered review used for visible pages.

### Improvements supported by the comparison

| Original pages | Current pages | Judgment and teaching reason |
| --- | --- | --- |
| A1-2, A18-24 | A1-5, A21-25, A29, A31-37 | Improved: current dates and schedule, explicit movie-night cue, complete quiz-vote choices, and usable upcoming-course details. |
| A5-7 | A9-12 | Improved: readable contact options, current office-hours source, native links, and usable Discord/form visuals. |
| B9-13 | B9-13 | Improved: shorter preparation explanation and corrected interphase euchromatin statement, with the original banding evidence retained. |
| B15-16 | B15-16 | Improved: explicit select-all question, native answer reveal, and a correct explanation separating homolog identity from replication-dependent X shape. |
| B32-37 | B31-38 | Improved: consistent topic divider, complete centromere-shape sequence, and a matching answer that repeats descriptions beside the terms. |
| B41 | B43 | Improved after this audit: the fusion sequence remains visible and the inaccurate no-centromere-remnant statement is corrected. |
| B45-49 | B47-51 | Improved: the HeLa origin, contamination, research, and consent story remains recognizable; unsupported mass claims and misleading HPV wording are corrected. |
| C2-4, C11-18 | C5-8, C11-17, C25 | Improved after this audit: the address rule is taught in a table, tried without answer labels, explained with a schematic, and then connected to the original location illustration. |
| C9-10 | C19-21 | Revised scope: readable simple karyotype notation and practice replace the tiny advanced notation table. The old table's complete structural-symbol vocabulary is not retained here. |
| D4, D22-23, D38 | D6, D9, D25 | Improved: chromosome sets, replicated chromatids, rearrangements, and diploid zygote notation are distinguished explicitly. |
| D33-41 | D19-28 | Improved: meiosis-I and meiosis-II errors are compared before the clinical examples, all eight illustrated gametes remain present, and the X-linked problem has complete assumptions and a readable reveal. |
| D11-19, D42-50 | D30-48 | Improved: readable comparisons, graph interpretation, and a clearly stated segregation model replace dense prose and an unqualified live-birth prediction. |
| D25-32 | D50-59 | Improved after this audit: screening is distinguished from diagnosis, sample types are compared, and ultrasound/workflow visuals support the explanation. |
| D51-54 | D60-63 | Improved: original reading/video topics and link targets remain; overlapping URLs are removed and the rare-screening infographic is readable. |

Original FISH/SKY evidence, Brainbow photographs and constructs, ape comparisons, the Neanderthal
and human/mouse figures, and HeLa karyotypes remain recognizable. Many are roughly equivalent
visual references rather than newly improved illustrations. Repeated preparation/address views
were consolidated. The dated 2025 corrections notice and old schedules were superseded. Structural
rearrangement teaching remains assigned to the December 1 continuation, following the current
[course schedule](https://vosslab.github.io/syllabus/fall_2026/genetics/SCHEDULE/).

### Seven repairs made during this comparison

1. **C12:** remove the answer-labeled CFTR figure from the question; C13 retains the worked answer.
2. **C14:** restore the original chromosome-7 band-location illustration. Its embedded bytes match
   the original C13 ODP image, rather than substituting the hierarchy schematic a third time.
3. **D13:** remove the hint that already calculated the correct choice; D14 retains the calculation.
4. **D36:** replace prose risk numbers that disagreed with the plotted series with graph-reading
   prompts. The original graph and its population trend remain.
5. **D52:** stack the two original ultrasound images in the existing three-panel layout, making
   both NT markers visible while keeping the simpler screening explanation.
6. **D61:** enlarge the rare-screening infographic beside its headline and preserve both article
   targets as concise footer links.
7. **B43:** clarify centromere instability and retain the distinction between an inactive
   centromere and detectable ancestral centromeric DNA, supported by
   [Avarello et al. (1992)](https://pubmed.ncbi.nlm.nih.gov/1587535/).

The agenda at A2 uses the original chapter grouping and brief topic labels: Karyotypes,
Chromosome Nomenclature, Chromosome Aneuploidy, and Polyploidy, plus Prenatal Testing,
Movie Selection, and Quiz 5 Vote. The Lecture 09-15 wording correction follows the instructor's
original agendas and short deck titles; rendered evidence is in `_temp/genetics_agenda_voice/`.
The original agenda explicitly named polyploidy and used chapter groupings; the abbreviated
conversion lost both. Gene-mapping review and sex dosage were also on the old agenda, but are
absent from the current B-D content, so the restored agenda describes today's actual decks.

### Remaining limits

- The complete C9 band atlas is dense and smaller than the legacy stretched presentation.
  The enlarged individual examples in C5, C8, C23, and C24 supply the usable teaching references.
- B23-24 article/table scans and D5's historical frequency table remain dense reference images.
  This review does not certify every old infographic as a current clinical estimate.
- D59's newborn-screening reference table retains its 18.5 pt capacity advisory. Three shared
  registration regions and the hidden weather caption retain their existing advisories.
- Projector readability, live animation playback, external-link availability, and student learning
  gains were not measured. Native answer-reveal definitions were checked in all eight questions.

### Verification and evidence

Rebuilt all four ODP/PDF decks after repairs and inspected the eight affected context pages at
1200-pixel width, including the unchanged C13 worked answer. Rebuilt A again after the agenda
follow-up and inspected A2 at the same width; its chapter grouping and all topics fit cleanly.
All embedded image references resolve.
Counts and hidden states agree. After the agenda follow-up, the other 176 visible pages retain
their extracted text; D52's unchanged text accompanies its layout repair. All eight choice-based
questions retain native reveal
targets. Strict native Jotdown lint passes on 205 authored slides and 83 image references.
The comparison's 319 focused Djot/Markdown link and asset checks pass. The subsequent Lecture
09-15 agenda update also passes all 5,871 base tests.

One-time contact sheets, original/current text inventories, native checks, and before/final
screenshots are in `_temp/lect10_comparison/`. No permanent tests or fixtures were added for this
lecture-specific audit. Earlier test results below belong to their dated implementation batches.

