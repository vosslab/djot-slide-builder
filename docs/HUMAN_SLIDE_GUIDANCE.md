# Human guidance for slide authoring

These instructor preferences continue [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md).

## Slide-writing advice

- For original Genetics artwork, use source images for scientific facts and teaching purpose, not
  as visual templates. Develop a shared visual language from representative equipment, organism
  and scientific-diagram examples; allow different compositions and drawing techniques by subject.

- Use plain, concrete language. Prefer familiar words and direct sentences. Technical terms
  should add precision; vocabulary and jargon add cognitive load. When in doubt, use the simpler word.
- For Mitotic Cross-Over, start from crossing over between linked genes, then use twin spots.
  Keep that story clear when adding the DNA-repair connection and other examples.

- Use sections for broad units and subsections for the teaching topics within them. Keep the
  hierarchy consistent across a lecture's content decks, and aim for a subsection every ten slides
  or so at conceptual transitions, particularly in long Genetics decks such as 09B.
- Add more section/subsection slides to 09C because it moves quickly between topics.
  Look in my local genetics books for twin-spot homework ideas.
- I like the simple twin-spot prediction problem.  - Put the twin-spot prediction problem into Lecture 09C, not just the research notes.

- A bad font license file must not block slide rendering; license validation is not a build gate.

- Djot source must be ASCII with character references for non-ASCII text; replace corrupted
  dash sequences with plain hyphens.

- Encoding errors should identify the editor line; a byte position is not useful for locating
  corrupted text in a long Djot source.

- Support all standard inline formatting shown in the Djot reference, including highlighting
  `{=Shark Talk presentations=}` in the agenda slide.
- Use the established external LibreOffice export path on macOS; sandboxed launches crash soffice.

- I do not want redundant `[URL](URL)` markup to be required when a bare URL suffices.

- Style the Lecture 05C Theranos timeline dates like genetics definition terms so the dates
  stand out visually.

- Compile Biotechnology Lecture 04 talking points into a single ODP.

- In Biotechnology Lecture 06C, give every talking point a subsection slide and each chapter
  a major section slide. Use the decks under `old/` to check chapter boundaries.

- Expand and improve Biotechnology Talking Points Set 4 using the added annual decks; do not
  reduce its content. Match the numbers and topics in `old/2026_topic_list.txt`.
- Keep these slides in my voice, style, and tone. The Lecture 06 source material is now in `old/`.  - Finish the talking points first, then improve the business-plan lecture.  - The business-plan slides need visual pop alongside the
- tables I like. Use screenshots,
  paragraphs, formatting choices, and logos from the sample submissions; keep my voice and tone.
- I want large Djot decks to support separate chapter files so they are easier to edit.

- Convert Biotechnology `LECT06/` to Djot, including the business-plan guidance deck. Modernize
  that guidance using the submissions in `biol_480-biotech/01-Sample_Executive_Summaries/`.

- Preserve deliberate text color, ALL CAPS, underline, bold, and italics during conversion and
  LLM rewriting. These can carry teaching meaning; review formatting as well as the words.

- `@replaceme` is an acceptable conversion result. Use it when the agent decides the existing
  slide cannot be faithfully represented as Djot, not as a request for human judgment.  Eliminating every marker is not a completion requirement.

- Deterministic ODP-to-Djot conversion alone is not good enough. Keep LLM evaluation in the
  middle of the conversion workflow to judge whether the teaching intent survives.

- Track significant image shrinkage during conversion by comparing displayed image area as a
  percentage of the slide and eventually flagging excessive changes.  Audit code is welcome now; do not create new special layouts to solve shrinkage today.
- Conversion managers may cut, split, and crop images to fit the teaching layout. I favor
  automatic border trimming, like `mogrify -trim`, across images where it preserves meaningful content. This image-editing permission is separate from approval to split slides.
- For mixed text/image scaling, evaluate font candidates at half-point precision and allow
  each image an independent scale. Score text by font size and images by displayed width, using consistent physical units rather than summing individual areas.
- Everything in a layout region, including local headings, goes through the same size
  optimization. Keep it simple; avoid special-case allocation rules that reserve heading space before the rest of the content is considered.
- If mixed-content readability constraints cannot be met, retain the source slide with
  `@replaceme`. Prefer this designation over splitting; do not recommend splitting as the default repair. Any slide split requires human approval.
- Treat mixed text/image flow within one panel as a powerful conversion strategy: several
  objects can share a region, rather than receiving one panel each. LECT07B slide 24's PNG, sentence, and SVG work better together in one panel than split across stacked panels.  Document this strategy and teach it to the converter;
  consider it before marking a sequential-content layout for replacement, while preserving meaningful spatial relationships.
- Keep text as glyphs rather than pixels when converting GDI/metafile figures. Prefer a
  vector-preserving route such as SVG over a low-resolution raster preview.

- For labeled diagrams, build SVG files containing embedded images and editable labels.  - Put the two M-checkpoint diagrams in separate SVG files, with their explanatory sentences in
  regular text boxes beneath them in a 2 by 2 layout. Give the diagrams the larger row.
- Make defined words stand out with bold and underline; some selective color is welcome.  - Embed SVG directly in ODP. Apply suitable diagram repairs throughout Lecture 06 and retain
  `@replaceme` wherever conversion cannot preserve the pedagogical intent.

- For Lecture 06, use local tools to convert to custom Djot; use `@replaceme` where conversion
  cannot preserve pedagogical intent. Update this week's announcements and show the exam slides because the exam is next week. (October 6, 2026.)
- For slides that do not translate and need human review, add an obvious `@replaceme` option
  in Djot that makes a large red "REPLACE ME" watermark on the slide.
- Repeat key slides in a Summary section at the end. This emphasizes their importance and
  makes them easy to find during homework. The original 05D's Addition Rules and Multiplication Rules slides are useful offline single-slide references; retain that function in v2.
- Retain the original 05D's visual explanations, especially Venn diagrams. Reuse them or
  make simple SVGs that show the same concepts in v2.
- Switching between percentages and fractions in 05D v2 may confuse biology students who
  are less comfortable with mathematics. Keep the probability notation consistent.
- Concise slides do not mean only four words per line. I want students to listen during class,
  but complete text-heavy slides that I skip can help them study afterward. Include those explanations in the slides students receive, not only in speaker notes.
- Every content deck (B-H) should use: title, required learning objectives, optional new jargon
  definitions, opening section heading, teaching content, summary, and a separate THE END.  Without a vocabulary slide, put the opening section heading on slide 3.
- Use dedicated colors for addition and multiplication throughout Lecture 05 so students can
  associate a color with each rule as a subtle mnemonic.
- Blue and purple are too close in hue. Prefer Chicago Bears blue/orange or Cubs blue/red
  pairings for concepts that students should distinguish.
- Apply the supplied plain-language advice to science teaching: use simpler words when they
  preserve the meaning, and keep technical terms when they add precision.
- When authoring or revising lectures, define jargon new to the lecture sequence in the first
  few slides. During conversion, check prior decks for earlier definitions. Managers may add a definitions slide near the beginning for important terms new to the lecture sequence, using concise definitions limited to terms already
  used in the lecture.
- Add instructor notes to the custom Djot slide format; `@speaker-notes` works as the section marker.  - "Be a Visual Storyteller - limit the amount of text - you do the talking, not your slide."  - "Images Are Required: Try to have several
- pictures on your slide to maintain audience
  attention. You should have some text though."
- By avoiding complete sentences, I mean fully decorated, elaborated sentences, usually longer
  than 10-15 words; long subjects allow more room. "Billy threw the ball" is fine. Break up long
  embedded definitions and clauses, as in my trisomy 21 example in [slide-specs/VOICE_GUIDE.md](slide-specs/VOICE_GUIDE.md#keep-statements-easy-to-scan).
- "These slides are not for presentation, so the 'instructor does the talking, not the slides' is
  not fully true."
- "Split the 04C protein material into 04C, 04D, 04E, and 04F by chapter; structural biology is a
  chapter I added that is not in the book."
- Keep `set_3` in the filenames; it is the major hierarchy for my content-based slide decks in
  Biotechnology.
- I don't want slide numbers; they make students watch the clock instead of the presenter.  - For Lecture 05D v2, preserve the hard-question opening, the context-dependent addition-rule
  trap, and callbacks to rule slides. Rewrite textbook question screenshots as editable text.
- Put learning objectives on slide 2, a summary immediately before THE END, and flow cues in `@speaker-notes`.
  Aim for 30-40 slides; up to 50 is fine when the extra slides teach without adding bloat.
- More multiple-choice and question-answer slides are welcome in Lecture 05D v2.  - Use Unicode fraction glyphs in Lecture 05D v2 instead of literal slash fractions.  - Fix awkward wrapping through sensible wording and layout; manually
- added nonbreaking spaces
  have been a workaround, not the preferred solution.
- Keep font roles: Atkinson Hyperlegible Next for ordinary text, Atkinson Hyperlegible Mono for
  monospace, and IBM Plex Sans Condensed for narrow text. Remove ad hoc font-family overrides.
- Let the backend select fonts for missing glyphs and mathematics (a math font such as STIX is
  fine); keep font substitutions out of Djot files. Preserve student-facing prose about fonts.
- Djot specifies semantic font families or roles, not concrete font names. The backend owns the
  mapping from ordinary, monospace, and condensed text to installed or bundled font faces.
- LibreOffice must display the real font family names, not renamed Djot-prefixed families.  - Show the URLs being clicked so their destinations can be inspected for spam or security
  concerns. Render visible URLs in the backend's narrow/condensed font; retain helpful context beside the address rather than hiding it behind a descriptive link label.
- ALL visible URLs use the condensed font and visibly smaller type, then allow
  independent shrinking down to 12 pt to avoid wrapping. Keep ordinary text at its own size; preserve the complete visible URL and clickable destination, including explicit links with a different target. Move an intact URL to the next
  line when necessary; flag addresses still too wide at 12 pt. Check rendered slides for awkward URL splits.
- Prefer pollen/ovule labels for plant examples and sperm/egg labels for animal examples.  - Add colorful plant emoji to Lecture 05D v2 to make the plant examples more visually interesting.  - Explicitly label longer slides intended
- for future student reference with a short phrase
  saying they are not covered in lecture.
- Use a dedicated one-panel layout for reference-only slides, with a light gray slide outline.  - Make allele symbols stand out from surrounding prose, using italics or another clear distinction.  - Present probability rules directly:
- name the Specific or General Rule, state its condition,
  then give the formula. Keep both multiplication orders in the summary reference.
- Give Lecture 05D v2 clearer section and subsection breaks. Addition Rule should be a section;
  distinguish major concepts from the worked applications within them.
- Lecture 05D v2 became confusing: the purpose of individual slides was unclear and transitions
  felt jarring. Rebuild a connected narrative around the original sequence and visual explanations; more prompts, fragments, or section dividers do not by themselves make the lecture clearer.
- Apply the early-jargon guidance to probability notation too: explain P and event labels near
  the front of the deck, before students encounter them in worked problems.
- Preserve the opening pollen problem's mutant-allele context and callback to last week's
  F1-to-F2 monohybrid cross. Explicitly ask students to complete the Punnett square and predict the F2 genotype ratio; do not replace that structure with a generic offspring question.
- The original textbook question looked different from the surrounding slides, which made
  it feel special and recognizable as a problem statement. Preserve that visual distinction using editable text, not the original image; the durable layout approach is still undecided.
- Keep column widths stable across the repeated left-hand Punnett tables starting with
  "Does every offspring qualify?" so students can follow the same cells between slides.
- Prefer an elegant, durable compiler solution for consistency over manual per-slide tuning,
  even if expressing the intended relationship adds a little Djot markup.
- Compare terminology with my local genetics textbooks; anatomical precision should fit the
  teaching context rather than adding an unnecessary distinction to a probability lesson.
- Add useful lessons from those textbooks to Lecture 05D v2 to improve clarity and engagement.  - Add learning objectives and a closing summary to each relevant Lecture 05 deck: B, C, E, F,
  G, and H, following the pedagogical slide style guide.

## Conversion review

- Review Lecture 10 against Topic 09 homework in `genetics_tasks2.csv`; consider replacing
  some slide content with worked homework problems. Topic 09 is the intended homework group.
- Lecture 10 is disease-focused. Apply the review's fixes, but leave deletion mapping and
  translocation segregation for Lecture 11.
- Restore Lecture 10D's explanation of how DNA copying without completed cell division
  can produce tetraploidy; keep this mechanism alongside the new counting problems.

- Use the three-point interference problem generator for Lecture 09B so the slides match
  the homework more closely.
- Remove the reference problems in 09B and add a second generated example instead.  - Add 3-5 researched slides to 09C on other useful mitotic-crossover topics.  - Split 09D's Products of Meiosis into two slides and add one or two section headings.

- Keep Lecture 09B as interference and split the tetrad material into six smaller topic decks:
  mitotic crossover; yeast/asci; crossover classes and distance formula; two genes; three genes; then ordered tetrads and centromeres. Repair the draft figures we retain.
- The slides teach students how to do the homework. Keep the homework's table appearance,
  with all three genes in separate spore boxes and the pairwise classification columns.  Cover the unused gene in 09G's pairwise views; keep the full table for reference.  The stripped-down genotype tables on the former 09C pages 37-43
  do not look good.

- Replace the old tetrad worked examples with fixed BPW examples: a linked two-gene problem,
  an unlinked two-gene problem, and then a distinct three-gene problem. Keep my updated handout for in-class practice; one authored version of each example is sufficient.

- Starting in 2025, my Genetics class meets face to face and uses handouts for group
  activities. Use handout instructions for the current class activity; prior-year Google Slides links may remain visible for students who want to practice outside class.


- Include the latest regular Stump the Vibe Coder podcast episode after the `lect##a-` YouTube slide.
  Make this a semi-automated process reusable across lectures, with the episode thumbnail, title, and visible link in a `big-image` layout.
- Skip StVC special episodes, including #38, when selecting the announcement slide.
- Every StVC slide must link to both the episode video and the GitHub Pages game or tool
  so students can try it. Use `big-image` with three lines in the caption box: shorter title, `Watch the Video: <URL>`, and `Play the Game: <URL>`. Format titles as `Stump the Vibe Coder #36: Bad Cell Day -- Two Drugs, One Keyboard`
  (with an em dash); retain the episode subtitle and omit the repeated YouTube SEO series suffix. Do not link GitHub repositories. Citations are for a single line.
- Use the 2026 announcements as canonical and update them for the current lecture week.  - Use properly typeset, stacked fractions (`\frac{a}{b}`) in equations rather than slash
  fractions. Use the standard binomial coefficient (`\binom{n}{k}`), not `C(n,k)`.  Parsing dollar-delimited math is not sufficient: verify the rendered equations in the PDF.
- Lecture 07 probability of progeny needs careful math formatting. Chi-square is mainly
  step-by-step table completion. The first conversion contained more images than expected.
- Add variety to two-panel image/text slides: sometimes image left/text right, other times
  text left/image right. Alternate when they are back-to-back.
- Biotechnology Lecture 05 builds on Lecture 04, with different slides shown or hidden.
  After Sept 21, Discord signup and Student Profile are no longer active assignments.  This does not remove the evergreen opening "Discord Server" slide.
- Preserve source colors and bold key labels in announcements. Anonymous-message instructions
  need the source image; keep clickable URLs visible and intact, using the condensed font role.
- Check static versus weekly announcement ownership, and use the instructor's schedule spreadsheet
  to update assessment dates.
- Use the edited 2026 Lecture 04 slides as examples of the changes I needed after Djot conversion.  - "When I see libreoffice/soffice crashes, I know you are using it wrong."  - Automatically convert embedded LibreOffice GDI content
- into an image, as with the
  Biotechnology talking points.
- Lecture 05C needs its source text colors preserved in Djot, including inheritance labels and
  sex-specific emphasis.
- Double-check the other Lecture 05 files for missing source text colors as well as Lecture 05C.  - Use subscripts for the numbered alleles in Lecture 05D, such as A with subscript 2.  - Give Lecture 05H a deep review; we can do better
- than the initial conversion.  - Lecture 05F needs its missing allele superscripts and generation subscripts restored,
  including I with superscript A and F/P generation indices.

## Preserve teaching voice

- This is a pure SVG goal, with no raster deliverables or embedded-raster SVG replacements.
  Use quality-90 WebP for raster previews/review assets. Keep original rasters as fallbacks or
  references; an SVG wrapper does not count as a completed original vector drawing.

- If a raster drawing is too difficult to replace convincingly, defer or skip it with a brief
  reason. I am fine with that limit; do not force a weak replacement.

- Prioritize Genetics and Biostatistics because I want to write my own books for those courses.
  Biotechnology is lower priority. Finish useful artwork already started in `_temp/`.

- The prenatal fetus looks like a monster and is unusable to me. Avoid drawing human figures;
  cells with chromosomes should be more straightforward, but those results also need improvement.
  The prenatal drawings also look too close to the source artwork, which raises copyright concerns.

- Keep the report of new SVG content deemed unusable easy to find, including nondisjunction
  and CVS. Record my rejection even when an earlier manager review accepted the drawings.

- Prioritize high-quality original SVG replacements for rasterized drawings and clipart by
  potential visual improvement and creation difficulty: achievable high-impact art first,
  complex work later. `@replaceme` status does not determine artwork priority.

- For this SVG goal, edit Djot only to switch an existing image URL/path to SVG; preserve all
  other slide content and directives. The master scope is
  [active_plans/active/genetics_visual_renewal_plan.md](active_plans/active/genetics_visual_renewal_plan.md).

- For a pure-text image, faithful OCR becomes an editable SVG card styled like a blockquote,
  with only the image URL changed in Djot. Preserve wording, errors and voice, retain the source
  image, and do not convert it to native Djot prose or a native blockquote.

- This job is drawing and clipart replacement for rasterized images. Preserve my voice, titles,
  prose, examples, layouts and sequence; check sources only as needed to draw accurately, not for
  a global science audit. Focus on important issues and avoid bikeshedding.

- Any slide splitting requires human approval. Keep existing content slides one-to-one with
  their source slides through the middle of the lecture. Added opening and closing slides may shift numbering; record those additions in the slide map without treating them as permission to split source slides.

- Conversion preserves existing teaching content and sequence; it does not authorize pedagogical
  redesign. Missing learning objectives, a closing summary, and an optional definitions slide for terms used in the lecture are authorized additions. Other substantive instructional changes require separate authorization; section
  dividers may label existing topic boundaries without reorganizing the lecture.

- When converting ODP slides to Djot, preserve approximately 98% of the original slide prose,
  allowing minor grammatical corrections and clarity improvements. Maintain the original author's voice, wording, and instructional content. Treat this as an approximate preservation target for existing prose, with required instructional
  additions considered separately.

- Managers must ensure that each converted lecture deck includes learning objectives and
  summary slides. Preserve existing objectives and summaries where present; create missing ones from the lecture's existing instructional content, following [slide-specs/PEDAGOGY_GUIDE.md](slide-specs/PEDAGOGY_GUIDE.md). Use
  specific, student-centered objectives on slide 2 and a closing summary immediately before the separate THE END slide. These source-grounded additions are part of conversion and are authorized without a separate request.

- Standardize layout, typography, spacing, colors, and reusable slide formats while retaining
  the original teaching substance. Preserve the lecture's examples, questions, explanations, scientific meaning, and relative sequence of existing content. Ground missing instructional components in that content and express them in
  the author's voice. Refer substantive content changes and suspected scientific errors to the instructor for a decision.

- Keep question wording and explanations substantially intact, making minor grammar or clarity
  improvements where helpful while preserving the original task and instructional intent.

- For Genetics Lecture 08 conversion, apply this prose-preservation policy and try the existing
  built-in layouts; use `@replaceme` when they cannot faithfully represent difficult source material.
- Use the question-and-answer layout for every multiple-choice or select-all-that-apply problem,
  including added homework problems. Keep extended explanations on following slides. Emphasize
  changed conditions with more than color alone, and separate alternatives visually in word problems.

- Put visible spacing on both sides of multiplication signs in equations and factorial examples.

- Preserve source tables, graphs, and their slide sequence. If content cannot be rendered,
  mark it `@replaceme`; never silently omit it or substitute a later reference slide.

- Never run LibreOffice inside the sandbox on this Mac. This also applies to indirect
  launches from ODP imports and tests, not just PDF exports. Use the repository scripts outside the sandbox. Keep this warning near the top of AGENTS.md.

- Right-align numbers in tables. Distinguish total rows visually from ordinary data rows.

- Consult the instructor-cleaned latest biotech announcements for shared presentation
  patterns, preserving each course's own content. Use `big-image` for the YouTube channel slide, with a visible clickable channel URL; replace the older stacked-panel versions.
- Clear @replaceme only after comparison with the original confirms complete content and
  sound rendering; attractive appearance alone does not establish completeness.

- A one-panel slide without an authored title should have a taller body text box that
  uses the title area. Prefer this automatic behavior over another layout type.

- The canonical repository temporary folder is `_temp/`, not `tmp/`.

- Render the null hypothesis consistently as H with a subscript zero (`H~0~` in Djot),
  including colored definitions and worked examples; never baseline H0.

- Use the instructor's standard saturated text colors from
  `~/nsh/PROBLEMS/biology-problems/problems/matching_sets/TEMPLATE.yml` for step emphasis.  The palette is encoded in HTML span styles under replacement entries. Match colored step-number references to the corresponding step color.

- For the approved LECT07D terminology/decision split, apply scientific corrections
  while preserving the instructor's voice as much as possible. This is explicit permission for that revision, not general permission to rewrite slide content.  Replace the old "accept hypothesis" wording with "do not reject" for the
  null hypothesis and "support" for the alternative, including repeated editable examples.

### Preferred color palette

- Significance-level labels should use preferred purple `#A719DB`; the imported dark
  purples were too dark.

- For new colored step sequences, choose well-separated colors from the fixed
  [COLOR_PALETTE.md](COLOR_PALETTE.md) palette in rainbow order. Keep cross-references matched to their items and reuse the identical colors when repeating a procedure slide.

- Slide colors are no longer constrained to LibreOffice's named palette. Use the
  instructor's preferred explicit hex colors documented in [COLOR_PALETTE.md](COLOR_PALETTE.md).
- For additional palettes, use the instructor-developed
  `~/nsh/PROBLEMS/qti-package-maker/qti_package_maker/common/color_wheel.py` tool. See [REPO_COLOR_PALETTE.md](REPO_COLOR_PALETTE.md) for existing color-wheel use.
- Preserve the source's meaningful emphasis and color relationships when standardizing
  slides. Color changes do not authorize wording or content changes.

### Titleless text slides

- Balance short text vertically on titleless one-panel slides instead of placing it
  in the top gradient with excessive empty space below. Prefer vertical centering at the standard body size.

### Readable capacity reports

- Body sizes above 17 pt are usually acceptable; below 17 pt warrants layout review.  - Build capacity warnings should identify authored slide numbers, not source line numbers.  - Keep factorial-table rows consecutive; start at 3 when
- trimming. A 17 pt table is
  acceptable. Do not shrink short slide titles to preserve a 20 pt body.

### Homework due-date slides

- Label table rows "Week 08" (zero-padded week numbers), retaining "Assignment"
  as the column heading.

- Title these pages "Homework Due Dates (Part 1/2)" without a platform name. Include
  future assignment deadlines from the syllabus for the current part.

- Color both assignment and due date relative to the lecture date: past due light gray
  (`#AAAAAA`), due this week or next week red (`#990000`), and later dates black (`#000000`), matching exam schedule status colors.

- Use a scannable two-column assignment/due-date table with abbreviated months and
  two-digit days (Nov 03).
- Keep separate Part 1 and Part 2 pages; hide Part 1 during Part 2.  - Omit redundant statements that earlier deadlines passed or dates are in the course schedule.

### Exam review visibility

- Keep "Reviewing Old Quiz Questions" in the Exam section. During Part 2, keep
  that section and its review slides hidden until the final exam is closer.

### Retrospective announcement standardization

- Apply shared slide guidance to past Genetics and biotech announcements while preserving
  the existing slide inventory, order, and hidden status. Do not apply newer visibility or slide-addition rules retrospectively when this preservation is requested.
- Graded vs Total Percentage uses preferred blue for Graded and magenta for Total,
  matching heading and body emphasis.
- Use the cleaned biotech LECT07 anonymous-message slide with text left, image right,
  and a visible intact form URL.

### Reusable icebreakers

- Use the NWS Chicago weather story before the icebreaker, refreshed manually on lecture day
  or the day before. I like that the forecast office always finds something interesting.
- Keep a saved weather story in upcoming announcements as a reminder to update it before class.  - Use `big-image` with the full NWS description as its caption. Start with the initially
  displayed story; deal with tab selection later. About 15 pt is fine, and the caption can have a little more room downward.
- When the weather page has two options, make a slide for both (November 3, 2026).  - Put "NWS Chicago, retrieved [date]: https://www.weather.gov/lot/weatherstory" in
  `@citation`, not in the weather caption.

- Make icebreakers fun and tangentially related to some aspect of the week's content. Use the
  new-movie/popular-culture question as a fallback for weeks without a topic idea.
- Vary the premise, type of response, and example answers across weeks. Compare the previous
  two lectures when choosing the next icebreaker.
- Always color the main icebreaker prompt with the preferred palette. Every icebreaker requires
  concrete examples and suggestions in black or dark gray to help students start talking.
- Use a reusable `prompt` layout for icebreakers and discussion questions, with automatic main
  prompt emphasis and dark supporting examples.

- Build a reusable collection from old announcement slides, preserving prompt wording, examples,
  and source provenance. Keep subject-specific prompts and general fallbacks.
- Use "Icebreaker" for face-to-face classes, including Genetics. Give the reusable catalog
  neutral "Icebreaker" titles.
- For Genetics on October 20, 2026, ask about pets: dog, cat, none, other.  - For Genetics 09A on November 3, 2026, ask: "What everyday task would you permanently
  hand over to a robot?"
- The collection is in `evergreen/icebreakers.yaml`; select prompts explicitly for each class.

### LECT07D title wording

- Omit redundant "(continued)" from LECT07D titles; it causes unnecessary wrapping.
  Retitling these slides for clarity is authorized.

- Use prominent mathematical minus signs (-) for negative values and right-align them
  with positive numbers. Render chi-square with the Greek lowercase chi and superscript two, never a Latin X or a legacy Symbol-font character.

- Introduce the shared six-step testcross roadmap in LECT08C immediately before Pandora
  Plant Inheritance (formerly PDF slide 26); this is its first use, before the D/F recaps.

- Retire the textbook-based LECT08F deck and replace it with one worked BPW three-point
  testcross example. Follow 08C/08D's teaching style and show every shared-roadmap intermediate step.
- Add cell-background attributes so editable Djot tables can show instructional progress.
  Align property naming with CSS: use `background-color` in the Djot attribute syntax.

- In the BPW testcross slides, make the three gene columns equal widths, use visibly stronger
  colors, and add section/subsection dividers between the major teaching phases.
- Merge the Total label across the three gene columns with `colspan` rather than widening
  the first gene column. Center gene symbols and classification labels for readable separation.

- Use slide space deliberately: compact instructional legends such as P/R keys may use the
  `@citation` footer or short bullets instead of wrapping through the main working panel.
- Keep the two original parental rows in a fixed color throughout testcross solutions, including
  after a gene is covered. They remain the reference for classifying the other rows. Distinguish these original rows from other offspring that share a parental combination for the selected pair.

- Keep original parental rows permanently green, and color the other pairwise parental rows
  lime green so every classified row is colored. Give each gene pair a distinct fixed-palette color and use it for that pair's recombinants and summary-table results.

- Improve the BPW example to enhance understanding, rather than adding complexity. Change the
  visual focus as the task changes: after all pairwise results are known, replace the full progeny table with the evidence needed to build and explain the map.
- Use restrained scientific diagrams and the fly emoji for context. Avoid decorative filler;
  let each visual explain the current reasoning step.
- Add a short question/answer side step for choosing parental versus recombinant types, where
  students often struggle. Explain whole-pair matching against either original parent, including why an offspring can be parental for a selected pair despite a difference at the covered gene.
- Repeat the "Match the Pair, Not the Count" answer slide for every gene pair as a reminder.  - Set up the discrepancy between outer-pair recombination and the map sum before explaining it.
  Use a generated example with a clearly visible gap and show why double recombinants escape the outer-pair count. Retain a simple teaching sequence rather than adding complexity.
- Keep semantic color hues and saturation stable across tables, diagrams, and number lines;
  vary lightness for readable fills. The instructor clarified that saturation changes, rather than inconsistent hues, made the earlier color relationship difficult to follow.
