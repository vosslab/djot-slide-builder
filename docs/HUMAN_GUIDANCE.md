# Human guidance

- I must be able to select and copy PDF slide text, including framed bookends, definitions,
  sections, THE END, and reference slides. Decorative borders must not block selection;
  outline-only borders should have no fill.

- Use black table-header text on light course-colored backgrounds.

- Use comfortable default table-cell padding, center all table headings, and vertically
  align table-cell content in the middle.

- Frame three-gene order as three choices: choose the middle gene. Show that reversed
  orders represent the same map.

- Color the three-point testcross procedure like the LECT07 chi-square steps, and repeat the
  matching colored roadmap before starting a new problem. Preserve colored text during conversion
  and explicitly check that preservation in the conversion checklist.
- LECT08D and LECT08F must use the same canonical six-step three-point testcross slide and
  identical colors throughout. Reference the shared slide rather than maintaining separate copies.
- Use black procedure-roadmap titles so attention stays on the colored steps. Repeat the shared
  six-step slide at gene-pair transitions, before new practice problems, and when returning to
  genotype summaries or distance calculations; do not limit it to the initial introduction.

- Handle detected runts automatically by pushing more words onto the final line when useful.
  Preserve wording, styling, and font size; prefer balancing line breaks over manual rewriting.

- Use a thin, angular frame with matching diagonal breaks at opposite corners for bookend
  and definitions slides. Preserve the reference image's symmetry, use one course hue with
  light/dark variations, and keep the frame out of the content area. Accents are welcome;
  omit the earlier arbitrary thick corner segment.

- Use Title Case for all slide titles. This is the general slide-title rule, not a special
  treatment for Learning Objectives or Key Takeaways. Preserve standard spelling of acronyms,
  proper names, gene symbols, and scientific notation.

- Keep bookend and definitions frames and accents in the selected course hue. Saturation
  and lightness may vary for visual emphasis and contrast; avoid unrelated accent hues.

- Use one dedicated `bookend` layout for both Learning Objectives and Key Takeaways.
  Give these lecture bookends similar visual attention. Use a dedicated `definitions` layout
  that enforces term formatting and gives definitions a recognizable frame.

- Use straight ASCII quotation marks and apostrophes in Djot text. Write a plain apostrophe
  instead of `&#8217;`; normalize literal curly quotes and their numeric or named entities.

- Treat `@notes` as presentation note cards for lecturing: speaking prompts, explanations,
  and reminders useful while teaching.
- Keep this administrative material out of Djot files, including comments; use separate
  reports or slide maps only when traceability is needed.

- Ignore runts when the font is at its maximum size and the paragraph is the final displayed
  paragraph of its text block. Keep title-wrap and URL-width checks active.
- Run the Djot audit on Genetics LECT08 and reduce warnings with simple changes.

- Build a Python Djot auditing script, prioritizing title line wrapping and runt checks.
  Keep lecture-quality checks in the audit rather than making lecture wording a pytest gate.

- Avoid single-word final lines in generated learning objectives; aim for final lines at least
  one-third of the text width. Generated objective wording may be shortened or lengthened for
  this purpose. Preserve instructor-authored wording unless changes are separately authorized.

- Go through LECT08 and use a labeled image with a quality-90 WebP embedded in SVG where
  it makes sense. Limit each figure to one image and its overlapping text boxes; keep slide
  titles and surrounding text native. This does not authorize whole-slide image conversion.

- Managers must follow the [slide conversion checklist](SLIDE_CONVERSION_CHECKLIST.md).
  Keep its items concrete actions with verifiable results; keep broader content policies here.

- Keep Lecture 07B's intro and miscellaneous material, including peer evaluation, in the main
  file. Split Three Ideas, One Great Idea, Shark Tank, and Executive Summary into chapter files;
  allow one hidden flag to hide the entire One Great Idea section.
  Number these chapter files `lect07b1-`, `lect07b2-`, `lect07b3-`, and `lect07b4-`.

- Source slide animations should flag conversions that lose a question/answer reveal. Make the
  importer fix durable rather than repairing only Lecture 06D slide 36.

<!-- VENDORED HEADER: START -->
Record the durable guidance Neil Voss states, or approves for preservation here, in his own words:
first person or close paraphrase, one to three lines per bullet. Material he supplies as a source
may inform [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) once it is settled, and an entry of uncertain
origin belongs there too. Rules: [REPO_STYLE.md](REPO_STYLE.md).
[PROPAGATED HEADER - ENTRIES BELOW ARE YOURS]
<!-- VENDORED HEADER: END -->

## Content titles

- I prefer slide titles to fit on one line, leaving more room for the content.
- Remove textbook figure identifiers such as `Figure 15.12`, `Figure 15.UN01`, and `Fig. 17-4`
  from converted slides, including headings, captions, citations, and editable diagram labels.
  They are textbook-slide artifacts. Preserve the useful explanatory caption and diagram content.

- Subsection backgrounds should be a variation of the course-dependent section color.

## Labeled diagram reconstruction

- I ignore SVGs with copyright information for a reason. Preserve that protection when
  adding tracking exceptions.
- We need a better way to distinguish drawn SVGs from SVGs containing images, because
  the images are typically copyrighted.

- Refresh 09H's images when I update the ordered-tetrad generator visuals. Add an opening
  definitions slide for FDS, SDS, and spore.

- In 09G, cover the unused gene while comparing a pair. Keep the main parental-ditype
  row highlighted across pairs: its genotypes and count do not change.
- Show a whole page of my handout on the Your Turn slide. I like visuals.
- In 09G, keep the bottom-right distance table the same size through slides 11-15,
  20-24, and 29-33. Give the handout page on slide 39 a visible page outline.

- Make classification answers large; separate question/answer slides are fine instead of
  animation for this content. Use my better colored tetrads in the crossover figures.
- Keep PD gold, TT magenta, and NPD green through the tetrad formulas and examples.
  Check 09F and 09G for the same presentation issues as 09E.
- We do cover unlinked tetrads, even when the example comes later in the deck.

- Stretched images are a pet peeve; I cannot tolerate them. Preserve image proportions,
  including artwork embedded inside SVGs. Use the generator's ascus artwork in 09D.

- Use the ordered-centromere problem generator's existing ordered-tetrad artwork in the slides.

- When the export path cannot put SVG tetrads in table cells, use a whole-table SVG builder.

- Use the artwork-plus-labels SVG pipeline only for labeled images, not whole-slide conversion.
  A figure contains one image and its overlapping text boxes. Keep slide titles, ordinary prose,
  and layout outside that figure in native Djot.

- Implement the LECT08B source-6 Punnett-square cover relative to its image content, so the
  box follows the image and disappears on click.

## Equation pipeline

- Build better conceptual bridges into the tetrad equations. Keep my voice and break the
  concepts into small pieces.
- The centromere connection for unordered tetrads is not needed. Cover ordered tetrads and
  their centromere connection, with a worked problem from the ordered-centromere generator.

- Editability inside ODP/PPTX is not a repository requirement; keep equations editable in Djot.
- Use rich LaTeX math syntax with MathJax-to-SVG rendering. Genetics LECT07C, with its many
  binomial expressions, should be the target example.
- Remove mixed inline SVG support. Keep standalone equations and equation-only bullets;
  use native Djot formatting for ordinary text.
- Treat permanent tests as liabilities as well as assets. Use the checklist in
  `PYTEST_STYLE.md`; keep one-time implementation checks separate, and remove tests when in doubt.

## Slide 1: title slide

- Across every course and lecture, keep the lecture number and letter above the title metadata.
  Use the same universal format, with no taglines. Vertical bars are never acceptable.
- Unknown chapter: three metadata lines, "Slide Deck Topic", "Dr. Neil Voss", lecture date.
  Do not invent a chapter number to fill the field.
- Known, canonical chapter: either three lines, "Chapter ##: Slide Deck Topic", "Dr. Neil Voss",
  lecture date; or four lines, "Slide Deck Topic", "Chapter ##", "Dr. Neil Voss", lecture date.
- Announcements slides NEVER have chapters. The topic is exactly "Announcements"; follow it
  with "Dr. Neil Voss" and the lecture date.
- Verify known chapter numbers against the relevant BPW course index, rather than deriving them
  from lecture numbers. For genetics, use the [BPW Genetics index](https://biologyproblems.org/genetics/).
- I must be able to select and copy the slide 1 text in the PDF. Keep title metadata as real text.
  Use a pale, desaturated course-color fill behind the text. If filling it prevents copying,
  use an unfilled rectangle with a thicker, course-colored outline instead.
- Include parenthesized chi-squared in the chi-square title, authored as `(&chi;^2^)` for editable
  native superscript text.
- Enforce the universal Djot slide 1 format with pytest across courses and lectures.

## Exam and quiz schedule

- On the quiz/exam dates slide, show past assessments in light gray, future assessments in
  black, and next week's assessments in dark red.
- Exam and quiz schedule text is fixed: one "item: date" per line, using abbreviated month and
  day, such as "Quiz 1: Sept 22". Change only status colors; do not add "completed", descriptions,
  combined assessments, or mixed bolding. Put a long schedule URL in `@citation`; reserve
  `@notes` for presentation note cards used while lecturing.
- Think of the exam and quizzes page as a progress bar: keep the list and positions stable,
  with colors showing completed, next-week, and future assessments.

- Show the quiz-guidance slides when a quiz falls in the current lecture week or the following
  week; hide the group otherwise. Use the current lecture date and course schedule to decide.
- Keep quiz and exam guidance in course-wide evergreen Djot groups so one `hidden: true`
  or `hidden: false` setting in each weekly master controls the entire group. Use
  `genetics/evergreen/` for Genetics and explicit `repo:` includes, rather than copies under LECT08.
- After the weekly agenda and chosen icebreaker, share the constant opening material, including
  the YouTube channel, contact information, textbooks, course links, grading explanations, and
  assessment policies. Keep weekly agenda content, icebreaker selection, podcast episode,
  assessment status colors, and dated deadlines in the weekly master.

## Course links and evergreen announcements

The working guide for `lect##a` preparation is
[ANNOUNCEMENT_DECK_GUIDE.md](ANNOUNCEMENT_DECK_GUIDE.md). This section records the
instructor's stated preferences; the guide assembles them into the current weekly workflow.

- Canonical announcement order: title, agenda, Next Week, weather, icebreaker, Informational Slides,
  YouTube channel, Stump the Vibe Coder, Discord, office hours, contact, anonymous messages,
  Course Content, textbook, Syllabus Links, PREVIEW Slides, Grading and Assessment,
  Assignments/Quizzes/Exams, Graded vs Total Percentage, Quiz/Exam schedule and policies,
  Exam when needed, Quiz when needed, Weekly Assignments, General Announcements,
  spring registration when needed, evaluations in their display period, Natural Science Club
  (hidden for now), then THE END (November 3, 2026).
- The three main sections are Informational Slides, Course Content, and General Announcements.
  Title, agenda, Next Week, weather, and icebreaker are before the first section. Informational Slides
  contains YouTube/STVC and contact information. Course Content contains textbook/syllabus,
  Grading and Assessment, Exam/Quiz overview, Exam, Quiz, and Weekly Assignments. Use subsection dividers
  for these course groups and for registration, evaluations, and club under General Announcements.
- Keep the original opening order; registration belongs after course logistics.
- Weekly announcement decks have not always been aligned; missing items often reflect
  forgetting them, not an intentional alternate structure. Apply the consistent template going
  forward while keeping seasonal groups conditional.
- Put a Next Week slide immediately after the existing agenda, focused on work due and what
  happens in class the following week. Use the current course schedule; do not invent events.
- Textbook placement can be informational/syllabus or course-content/logistics; neither is a
  correctness failure. The current shared Genetics group places it under Course Content.
- There is no fixed historical Exam/Quiz order. Prefer assessment overview, Exam, Quiz,
  then Assignments for consistency, rather than treating the reverse order as an error.
- Discord signup and Student Profile assignments run until September 21 in fall and February 14
  in spring; hide their assignment reminders afterward.
- Biotechnology has a special Veridian Dynamics ending: retain it after general announcements
  and before THE END.
- General Announcements rarely has more than one active topic: Graduating Students in the first
  two weeks, registration midsemester, evaluations at semester end, and one-off events such as
  campus seminars when relevant. Natural Science Club remains hidden for now; the instructor
  has not decided how to bring it back since COVID.

- Use root-level `evergreen/` for slides shared across courses. Keep course-specific reusable
  slides in that course's `evergreen/` folder, and dated weather/podcast snapshots with the lecture.

- Spring registration slides are evergreen. Show them roughly October 15 through December 1,
  including in Genetics 09A and 10A.
- I mostly teach seniors and graduate students. Give only the first registration day; students
  can look up the registration date that applies to them.
- Point students to the Registrar and Course Finder for registration. Do not assume which
  registration system they use. The Course Finder is
  https://banner.roosevelt.edu/ssbprod/bwskzenr.P_CourseFinder.
- Keep my original spring-registration wording and the Registrar/Course Finder links;
  do not expand it with new advising instructions.
- Include a summary of all my upcoming courses and an individual slide on each in the
  shared spring-registration group (November 3, 2026).
- I generally teach the same courses every year; mostly change the year to 2027 and also
  list my summer course.
- BCHM 355/455 Biochemistry Lecture: Thursday afternoons, 1:30-4:30 p.m., face-to-face
  Schaumburg. BCHM 356/456: face-to-face Schaumburg, less structured and more independent
  study-like (November 3, 2026).
- I am probably teaching BIOL 301 this spring as a third course, but it is not locked down yet.
  Mark the teaching assignment as tentative in course announcements.

- A prior lecture's announcement deck copied into a new lecture folder is a starter for the
  new weekly A deck. Do not keep that starter or its unused extracted assets in the new folder.

- Evergreen content is used across courses or across more than a single week. Tetrad content
  is for a single lecture; keep it with Lecture 09, including the repeated procedure slides.

- Support `@citation` on all slide layouts for URLs or article citations in smaller condensed
  text at the bottom. Normal layouts keep their full space; citations use the bottom margin.
- Put very long URLs in `@citation` when they crowd slide content. Keep the complete URL
  visible and clickable, following the instructor-edited Genetics LECT08 announcements.

- Use a YouTube slide generator with the existing StVC-style `big-image` layout: thumbnail,
  title, and visible clickable full `https://www.youtube.com/watch?v=...` URL.
  A separate layout type is unnecessary; there is room for the full URL.

- Course Zoom and Discord URLs are not on the syllabus; include the actual course URLs in the
  student slides. Only Biotechnology has a Zoom meeting this semester (Fall 2026).
- Any URL for the course should be in the slides. The slides are generally available only to
  students, and we already give them QR codes. Keep the URLs visible and clickable alongside
  the QR codes; do not substitute "The sign-up link is available on Blackboard."
- Store private Discord and Zoom URLs in ignored root `course_links.local.yaml` and import
  them into slides with `{{course_url:key}}` references, keeping the configuration out of GitHub.
- The YouTube channel slide must include a visible, clickable link to Dr. Voss's channel.
- YouTube URLs, including Dr. Voss's channel, and other public course links remain directly in
  tracked Djot sources; they do not need private configuration.
- The opening "Discord Server" slide is evergreen and stays in the deck. After the signup
  deadline, hide the Discord signup assignment; retain it for reuse rather than deleting it.
- Carry the first weeks' assignments, including Student Profile and Discord signup credit,
  forward as hidden slides after their deadlines. Retain eventual course-evaluation slides
  hidden until they are needed. Preserve this reusable inventory when preparing each new week;
  use separate included groups for convenient visibility control. Refresh evaluation deadlines
  before displaying them; never copy an obsolete date forward as a current deadline.

## Robustness and simplicity

- Builds must work without a `.git` checkout. If `git rev-parse` is unavailable or fails,
  use the current working directory as the project root.

- Focus on important issues, not bikeshedding. Address the highest-impact risks first.
  Spend review time on correctness, maintainability, validation, and delivery.
- Robust software continues to function despite imperfect inputs, data, state, or behavior.
  Handle imperfections according to context and impact; recover gracefully to preserve useful
  operation whenever possible.
- Apply KISS aggressively: prefer the smallest coherent design that satisfies actual requirements
  and known failure modes. Mechanisms, abstractions, policies, state, and tests must solve a
  demonstrated need. Complexity must earn its place.

## Test maintenance

- Audit all gates and remove those without a demonstrated need. When in doubt, remove the test
  or gate; this overrides older repository policies requiring the removed checks.

- Treat permanent tests as liabilities as well as assets. Protect intentionally stable, important
  behavior that could regress; prefer contracts over implementation details. When in doubt, remove.
- Keep one-time tests outside the permanent suite and out of Git in `tests/_temp/`. Promote them
  only when the behavior deserves lasting protection.
- Ground gates in actual needs; avoid arbitrary thresholds, exhaustive matrices, and byte or pixel
  equivalence unless the product depends on them.
- New gates need a failure plan: failure must lead to a decision or concrete recovery action.
  If it would not change the implementation or identify a real correctness problem, remove the gate.
- A different tool version alone must not stop working software. Require version gates only for
  demonstrated compatibility needs.
- Apply the permanent-test checklist in [PYTEST_STYLE.md](PYTEST_STYLE.md). Separate one-time rebuild
  checks from permanent tests; temporary checks must not become permanent without earning their place.

## Slide-writing advice

- Use plain, concrete language. Prefer familiar words and direct sentences. Technical terms
  should add precision; vocabulary and jargon add cognitive load. When in doubt, use the simpler word.
- For Mitotic Cross-Over, start from crossing over between linked genes, then use twin spots.
  Keep that story clear when adding the DNA-repair connection and other examples.

- I would like more section and subsection slides, particularly in long decks such as 09B.
  Aim for about one divider per ten slides, placed at conceptual transitions.
- Add more section/subsection slides to 09C because it moves quickly between topics.
  Look in my local genetics books for twin-spot homework ideas.
- I like the simple twin-spot prediction problem.
- Put the twin-spot prediction problem into Lecture 09C, not just the research notes.

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
- Keep these slides in my voice, style, and tone. The Lecture 06 source material is now in `old/`.
- Finish the talking points first, then improve the business-plan lecture.
- The business-plan slides need visual pop alongside the tables I like. Use screenshots,
  paragraphs, formatting choices, and logos from the sample submissions; keep my voice and tone.
- I want large Djot decks to support separate chapter files so they are easier to edit.

- Convert Biotechnology `LECT06/` to Djot, including the business-plan guidance deck. Modernize
  that guidance using the submissions in `biol_480-biotech/01-Sample_Executive_Summaries/`.

- Preserve deliberate text color, ALL CAPS, underline, bold, and italics during conversion and
  LLM rewriting. These can carry teaching meaning; review formatting as well as the words.

- `@replaceme` is an acceptable conversion result. Use it when the agent decides the existing
  slide cannot be faithfully represented as Djot, not as a request for human judgment.
  Eliminating every marker is not a completion requirement.

- Deterministic ODP-to-Djot conversion alone is not good enough. Keep LLM evaluation in the
  middle of the conversion workflow to judge whether the teaching intent survives.

- Track significant image shrinkage during conversion by comparing displayed image area as a
  percentage of the slide and eventually flagging excessive changes.
  Audit code is welcome now; do not create new special layouts to solve shrinkage today.
- Conversion managers may cut, split, and crop images to fit the teaching layout. I favor
  automatic border trimming, like `mogrify -trim`, across images where it preserves meaningful
  content. This image-editing permission is separate from approval to split slides.
- For mixed text/image scaling, evaluate font candidates at half-point precision and allow
  each image an independent scale. Score text by font size and images by displayed width,
  using consistent physical units rather than summing individual areas.
- Everything in a layout region, including local headings, goes through the same size
  optimization. Keep it simple; avoid special-case allocation rules that reserve heading space
  before the rest of the content is considered.
- If mixed-content readability constraints cannot be met, retain the source slide with
  `@replaceme`. Prefer this designation over splitting; do not recommend splitting as the
  default repair. Any slide split requires human approval.
- Treat mixed text/image flow within one panel as a powerful conversion strategy: several
  objects can share a region, rather than receiving one panel each. LECT07B slide 24's PNG,
  sentence, and SVG work better together in one panel than split across stacked panels.
  Document this strategy and teach it to the converter; consider it before marking a
  sequential-content layout for replacement, while preserving meaningful spatial relationships.
- Keep text as glyphs rather than pixels when converting GDI/metafile figures. Prefer a
  vector-preserving route such as SVG over a low-resolution raster preview.

- For labeled diagrams, build SVG files containing embedded images and editable labels.
- Put the two M-checkpoint diagrams in separate SVG files, with their explanatory sentences in
  regular text boxes beneath them in a 2 by 2 layout. Give the diagrams the larger row.
- Make defined words stand out with bold and underline; some selective color is welcome.
- Embed SVG directly in ODP. Apply suitable diagram repairs throughout Lecture 06 and retain
  `@replaceme` wherever conversion cannot preserve the pedagogical intent.

- For Lecture 06, use local tools to convert to custom Djot; use `@replaceme` where conversion
  cannot preserve pedagogical intent. Update this week's announcements and show the exam slides
  because the exam is next week. (October 6, 2026.)
- For slides that do not translate and need human review, add an obvious `@replaceme` option
  in Djot that makes a large red "REPLACE ME" watermark on the slide.
- Repeat key slides in a Summary section at the end. This emphasizes their importance and
  makes them easy to find during homework. The original 05D's Addition Rules and Multiplication
  Rules slides are useful offline single-slide references; retain that function in v2.
- Retain the original 05D's visual explanations, especially Venn diagrams. Reuse them or
  make simple SVGs that show the same concepts in v2.
- Switching between percentages and fractions in 05D v2 may confuse biology students who
  are less comfortable with mathematics. Keep the probability notation consistent.
- Concise slides do not mean only four words per line. I want students to listen during class,
  but complete text-heavy slides that I skip can help them study afterward. Include those
  explanations in the slides students receive, not only in speaker notes.
- Every content deck (B-H) should use: title, required learning objectives, optional new jargon
  definitions, opening section heading, teaching content, summary, and a separate THE END.
  Without a vocabulary slide, put the opening section heading on slide 3.
- Use dedicated colors for addition and multiplication throughout Lecture 05 so students can
  associate a color with each rule as a subtle mnemonic.
- Blue and purple are too close in hue. Prefer Chicago Bears blue/orange or Cubs blue/red
  pairings for concepts that students should distinguish.
- Apply the supplied plain-language advice to science teaching: use simpler words when they
  preserve the meaning, and keep technical terms when they add precision.
- When authoring or revising lectures, define jargon new to the lecture sequence in the first
  few slides. During conversion, check prior decks for earlier definitions. Managers may add
  a definitions slide near the beginning for important terms new to the lecture sequence,
  using concise definitions limited to terms already used in the lecture.
- Add instructor notes to the custom Djot slide format; `@notes` works as the section marker.
- "Be a Visual Storyteller - limit the amount of text - you do the talking, not your slide."
- "Images Are Required: Try to have several pictures on your slide to maintain audience
  attention. You should have some text though."
- "Limit Text: No complete sentences on slides; use short phrases and keywords only."
- Clarification: "I think the opening question should be a full question, which allows it to
  have complete sentences. There are exceptions to most rules."
- "These slides are not for presentation, so the 'instructor does the talking, not the slides' is
  not fully true."
- "Split the 04C protein material into 04C, 04D, 04E, and 04F by chapter; structural biology is a
  chapter I added that is not in the book."
- Keep `set_3` in the filenames; it is the major hierarchy for my content-based slide decks in
  Biotechnology.
- I don't want slide numbers; they make students watch the clock instead of the presenter.
- For Lecture 05D v2, preserve the hard-question opening, the context-dependent addition-rule
  trap, and callbacks to rule slides. Rewrite textbook question screenshots as editable text.
- Put learning objectives on slide 2, a summary immediately before THE END, and flow cues in `@notes`.
  Aim for 30-40 slides; up to 50 is fine when the extra slides teach without adding bloat.
- More multiple-choice and question-answer slides are welcome in Lecture 05D v2.
- Use Unicode fraction glyphs in Lecture 05D v2 instead of literal slash fractions.
- Fix awkward wrapping through sensible wording and layout; manually added nonbreaking spaces
  have been a workaround, not the preferred solution.
- Keep font roles: Atkinson Hyperlegible Next for ordinary text, Atkinson Hyperlegible Mono for
  monospace, and IBM Plex Sans Condensed for narrow text. Remove ad hoc font-family overrides.
- Let the backend select fonts for missing glyphs and mathematics (a math font such as STIX is
  fine); keep font substitutions out of Djot files. Preserve student-facing prose about fonts.
- Djot specifies semantic font families or roles, not concrete font names. The backend owns the
  mapping from ordinary, monospace, and condensed text to installed or bundled font faces.
- LibreOffice must display the real font family names, not renamed Djot-prefixed families.
- Show the URLs being clicked so their destinations can be inspected for spam or security
  concerns. Render visible URLs in the backend's narrow/condensed font; retain helpful context
  beside the address rather than hiding it behind a descriptive link label.
- ALL visible URLs use the condensed font. Start 2 pt below surrounding text, then allow
  independent shrinking down to 12 pt to avoid wrapping. Keep ordinary text at its own size;
  preserve the complete visible URL and clickable destination, including explicit links with a
  different target. Move an intact URL to the next line when necessary; flag addresses still
  too wide at 12 pt. Check rendered slides for awkward URL splits.
- Prefer pollen/ovule labels for plant examples and sperm/egg labels for animal examples.
- Add colorful plant emoji to Lecture 05D v2 to make the plant examples more visually interesting.
- Explicitly label longer slides intended for future student reference with a short phrase
  saying they are not covered in lecture.
- Use a dedicated one-panel layout for reference-only slides, with a light gray slide outline.
- Make allele symbols stand out from surrounding prose, using italics or another clear distinction.
- Present probability rules directly: name the Specific or General Rule, state its condition,
  then give the formula. Keep both multiplication orders in the summary reference.
- Give Lecture 05D v2 clearer section and subsection breaks. Addition Rule should be a section;
  distinguish major concepts from the worked applications within them.
- Lecture 05D v2 became confusing: the purpose of individual slides was unclear and transitions
  felt jarring. Rebuild a connected narrative around the original sequence and visual explanations;
  more prompts, fragments, or section dividers do not by themselves make the lecture clearer.
- Apply the early-jargon guidance to probability notation too: explain P and event labels near
  the front of the deck, before students encounter them in worked problems.
- Preserve the opening pollen problem's mutant-allele context and callback to last week's
  F1-to-F2 monohybrid cross. Explicitly ask students to complete the Punnett square and predict
  the F2 genotype ratio; do not replace that structure with a generic offspring question.
- The original textbook question looked different from the surrounding slides, which made
  it feel special and recognizable as a problem statement. Preserve that visual distinction
  using editable text, not the original image; the durable layout approach is still undecided.
- Keep column widths stable across the repeated left-hand Punnett tables starting with
  "Does every offspring qualify?" so students can follow the same cells between slides.
- Prefer an elegant, durable compiler solution for consistency over manual per-slide tuning,
  even if expressing the intended relationship adds a little Djot markup.
- Compare terminology with my local genetics textbooks; anatomical precision should fit the
  teaching context rather than adding an unnecessary distinction to a probability lesson.
- Add useful lessons from those textbooks to Lecture 05D v2 to improve clarity and engagement.
- Add learning objectives and a closing summary to each relevant Lecture 05 deck: B, C, E, F,
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
- Remove the reference problems in 09B and add a second generated example instead.
- Add 3-5 researched slides to 09C on other useful mitotic-crossover topics.
- Split 09D's Products of Meiosis into two slides and add one or two section headings.

- Keep Lecture 09B as interference and split the tetrad material into six smaller topic decks:
  mitotic crossover; yeast/asci; crossover classes and distance formula; two genes; three genes;
  then ordered tetrads and centromeres. Repair the draft figures we retain.
- The slides teach students how to do the homework. Keep the homework's table appearance,
  with all three genes in separate spore boxes and the pairwise classification columns.
  Cover the unused gene in 09G's pairwise views; keep the full table for reference.
  The stripped-down genotype tables on the former 09C pages 37-43 do not look good.

- Replace the old tetrad worked examples with fixed BPW examples: a linked two-gene problem,
  an unlinked two-gene problem, and then a distinct three-gene problem. Keep my updated handout
  for in-class practice; one authored version of each example is sufficient.

- Starting in 2025, my Genetics class meets face to face and uses handouts for group
  activities. Use handout instructions for the current class activity; prior-year Google Slides
  links may remain visible for students who want to practice outside class.


- Include the latest Stump the Vibe Coder podcast episode after the `lect##a-` YouTube slide.
  Make this a semi-automated process reusable across lectures, with the episode thumbnail,
  title, and visible link in a `big-image` layout.
- Every StVC slide must link to both the episode video and the GitHub Pages game or tool
  so students can try it. Use `big-image` with three lines in the caption box: shorter title,
  `Watch the Video: <URL>`, and `Play the Game: <URL>`. Format titles as `Stump the Vibe Coder #36: Bad Cell Day
  -- Two Drugs, One Keyboard` (with an em dash); retain the episode subtitle and omit the
  repeated YouTube SEO series suffix. Do not link GitHub repositories. Citations are for a single line.
- Use the 2026 announcements as canonical and update them for the current lecture week.
- Use properly typeset, stacked fractions (`\frac{a}{b}`) in equations rather than slash
  fractions. Use the standard binomial coefficient (`\binom{n}{k}`), not `C(n,k)`.
  Parsing dollar-delimited math is not sufficient: verify the rendered equations in the PDF.
- Lecture 07 probability of progeny needs careful math formatting. Chi-square is mainly
  step-by-step table completion. The first conversion contained more images than expected.
- Add variety to two-panel image/text slides: sometimes image left/text right, other times
  text left/image right. Alternate when they are back-to-back.
- Biotechnology Lecture 05 builds on Lecture 04, with different slides shown or hidden.
  After Sept 21, Discord signup and Student Profile are no longer active assignments.
  This does not remove the evergreen opening "Discord Server" slide.
- Preserve source colors and bold key labels in announcements. Anonymous-message instructions
  need the source image; keep clickable URLs visible and intact, using the condensed font role.
- Check static versus weekly announcement ownership, and use the instructor's schedule spreadsheet
  to update assessment dates.
- Use the edited 2026 Lecture 04 slides as examples of the changes I needed after Djot conversion.
- "When I see libreoffice/soffice crashes, I know you are using it wrong."
- Automatically convert embedded LibreOffice GDI content into an image, as with the
  Biotechnology talking points.
- Lecture 05C needs its source text colors preserved in Djot, including inheritance labels and
  sex-specific emphasis.
- Double-check the other Lecture 05 files for missing source text colors as well as Lecture 05C.
- Use subscripts for the numbered alleles in Lecture 05D, such as A with subscript 2.
- Give Lecture 05H a deep review; we can do better than the initial conversion.
- Lecture 05F needs its missing allele superscripts and generation subscripts restored,
  including I with superscript A and F/P generation indices.

## Preserve teaching voice

- Any slide splitting requires human approval. Keep existing content slides one-to-one with
  their source slides through the middle of the lecture. Added opening and closing slides may
  shift numbering; record those additions in the slide map without treating them as permission
  to split source slides.

- Conversion preserves existing teaching content and sequence; it does not authorize pedagogical
  redesign. Missing learning objectives, a closing summary, and an optional definitions slide
  for terms used in the lecture are authorized additions. Other substantive instructional changes
  require separate authorization; section dividers may label existing topic boundaries without
  reorganizing the lecture.

- When converting ODP slides to Djot, preserve approximately 98% of the original slide prose,
  allowing minor grammatical corrections and clarity improvements. Maintain the original
  author's voice, wording, and instructional content. Treat this as an approximate preservation
  target for existing prose, with required instructional additions considered separately.

- Managers must ensure that each converted lecture deck includes learning objectives and
  summary slides. Preserve existing objectives and summaries where present; create missing
  ones from the lecture's existing instructional content, following
  [the pedagogical slide style guide](PEDAGOGICAL_SLIDE_STYLE_GUIDE.md). Use specific,
  student-centered objectives on slide 2 and a closing summary immediately before the separate
  THE END slide. These source-grounded additions are part of conversion and are authorized
  without a separate request.

- Standardize layout, typography, spacing, colors, and reusable slide formats while retaining
  the original teaching substance. Preserve the lecture's examples, questions, explanations,
  scientific meaning, and relative sequence of existing content. Ground missing instructional
  components in that content and express them in the author's voice. Refer substantive content
  changes and suspected scientific errors to the instructor for a decision.

- Keep question wording and explanations substantially intact, making minor grammar or clarity
  improvements where helpful while preserving the original task and instructional intent.

- For Genetics Lecture 08 conversion, apply this prose-preservation policy and try the existing
  built-in layouts; use `@replaceme` when they cannot faithfully represent difficult source material.
- Use the question-and-answer layout for multiple-choice questions. Emphasize changed
  conditions with more than color alone, and separate alternatives visually in word problems.

- Put visible spacing on both sides of multiplication signs in equations and factorial examples.

- Preserve source tables, graphs, and their slide sequence. If content cannot be rendered,
  mark it `@replaceme`; never silently omit it or substitute a later reference slide.

- Never run LibreOffice inside the sandbox on this Mac. This also applies to indirect
  launches from ODP imports and tests, not just PDF exports. Use the repository scripts
  outside the sandbox. Keep this warning near the top of AGENTS.md.

- Right-align numbers in tables. Distinguish total rows visually from ordinary data rows.

- Consult the instructor-cleaned latest biotech announcements for shared presentation
  patterns, preserving each course's own content. Use `big-image` for the YouTube channel
  slide, with a visible clickable channel URL; replace the older stacked-panel versions.
- Clear @replaceme only after comparison with the original confirms complete content and
  sound rendering; attractive appearance alone does not establish completeness.

- A one-panel slide without an authored title should have a taller body text box that
  uses the title area. Prefer this automatic behavior over another layout type.

- The canonical repository temporary folder is `_temp/`, not `tmp/`.

- Render the null hypothesis consistently as H with a subscript zero (`H~0~` in Djot),
  including colored definitions and worked examples; never baseline H0.

- Use the instructor's standard saturated text colors from
  `~/nsh/PROBLEMS/biology-problems/problems/matching_sets/TEMPLATE.yml` for step emphasis.
  The palette is encoded in HTML span styles under replacement entries. Match colored
  step-number references to the corresponding step color.

- For the approved LECT07D terminology/decision split, apply scientific corrections
  while preserving the instructor's voice as much as possible. This is explicit
  permission for that revision, not general permission to rewrite slide content.
  Replace the old "accept hypothesis" wording with "do not reject" for the null
  hypothesis and "support" for the alternative, including repeated editable examples.

### Preferred color palette

- Significance-level labels should use preferred purple `#A719DB`; the imported dark
  purples were too dark.

- For new colored step sequences, choose well-separated colors from the fixed
  [COLOR_PALETTE.md](COLOR_PALETTE.md) palette in rainbow order. Keep cross-references matched
  to their items and reuse the identical colors when repeating a procedure slide.

- Slide colors are no longer constrained to LibreOffice's named palette. Use the
  instructor's preferred explicit hex colors documented in [COLOR_PALETTE.md](COLOR_PALETTE.md).
- For additional palettes, use the instructor-developed
  `~/nsh/PROBLEMS/qti-package-maker/qti_package_maker/common/color_wheel.py` tool.
  The local palette reference documents its CAM16 API and dark, light, and extra-light wheels.
- Preserve the source's meaningful emphasis and color relationships when standardizing
  slides. Color changes do not authorize wording or content changes.

### Titleless text slides

- Balance short text vertically on titleless one-panel slides instead of placing it
  in the top gradient with excessive empty space below. Prefer vertical centering
  at the standard body size.

### Readable capacity reports

- Body sizes above 17 pt are usually acceptable; below 17 pt warrants layout review.
- Build capacity warnings should identify authored slide numbers, not source line numbers.
- Keep factorial-table rows consecutive; start at 3 when trimming. A 17 pt table is
  acceptable. Do not shrink short slide titles to preserve a 20 pt body.

### Homework due-date slides

- Label table rows "Week 08" (zero-padded week numbers), retaining "Assignment"
  as the column heading.

- Title these pages "Homework Due Dates (Part 1/2)" without a platform name. Include
  future assignment deadlines from the syllabus for the current part.

- Color both assignment and due date relative to the lecture date: past due light gray
  (`#AAAAAA`), due this week or next week red (`#990000`), and later dates black (`#000000`),
  matching exam schedule status colors.

- Use a scannable two-column assignment/due-date table with abbreviated months and
  two-digit days (Nov 03).
- Keep separate Part 1 and Part 2 pages; hide Part 1 during Part 2.
- Omit redundant statements that earlier deadlines passed or dates are in the course schedule.

### Exam review visibility

- Keep "Reviewing Old Quiz Questions" in the Exam section. During Part 2, keep
  that section and its review slides hidden until the final exam is closer.

### Retrospective announcement standardization

- Apply shared slide guidance to past Genetics and biotech announcements while preserving
  the existing slide inventory, order, and hidden status. Do not apply newer visibility
  or slide-addition rules retrospectively when this preservation is requested.
- Graded vs Total Percentage uses preferred blue for Graded and magenta for Total,
  matching heading and body emphasis.
- Use the cleaned biotech LECT07 anonymous-message slide with text left, image right,
  and a visible intact form URL.

### Reusable icebreakers

- Use the NWS Chicago weather story before the icebreaker, refreshed manually on lecture day
  or the day before. I like that the forecast office always finds something interesting.
- Keep a saved weather story in upcoming announcements as a reminder to update it before class.
- Use `big-image` with the full NWS description as its caption. Start with the initially
  displayed story; deal with tab selection later. About 15 pt is fine, and the caption can
  have a little more room downward.
- When the weather page has two options, make a slide for both (November 3, 2026).
- Put "NWS Chicago, retrieved [date]: https://www.weather.gov/lot/weatherstory" in
  `@citation`, not in the weather caption.

- Use restrained color on icebreaker slides: emphasize the main prompts with the preferred
  palette, keeping example answers mostly in ordinary text.

- Give students concrete examples with icebreaker questions to help them get talking and share.

- Build a reusable collection from old announcement slides, preserving their Breakout Room Chat
  format and wording. Keep subject-specific prompts and general fallbacks.
- For Genetics on October 20, 2026, ask about pets: dog, cat, none, other.
- For Genetics 09A on November 3, 2026, ask: "What everyday task would you permanently
  hand over to a robot?"
- The collection is in `icebreakers.yaml`; select prompts explicitly for each class.

### LECT07D title wording

- Omit redundant "(continued)" from LECT07D titles; it causes unnecessary wrapping.
  Retitling these slides for clarity is authorized.

- Use prominent mathematical minus signs (-) for negative values and right-align them
  with positive numbers. Render chi-square with the Greek
  lowercase chi and superscript two, never a Latin X or a legacy Symbol-font character.

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
  after a gene is covered. They remain the reference for classifying the other rows. Distinguish
  these original rows from other offspring that share a parental combination for the selected pair.

- Keep original parental rows permanently green, and color the other pairwise parental rows
  lime green so every classified row is colored. Give each gene pair a distinct fixed-palette
  color and use it for that pair's recombinants and summary-table results.

- Improve the BPW example to enhance understanding, rather than adding complexity. Change the
  visual focus as the task changes: after all pairwise results are known, replace the full
  progeny table with the evidence needed to build and explain the map.
- Use restrained scientific diagrams and the fly emoji for context. Avoid decorative filler;
  let each visual explain the current reasoning step.
- Add a short question/answer side step for choosing parental versus recombinant types, where
  students often struggle. Explain whole-pair matching against either original parent, including
  why an offspring can be parental for a selected pair despite a difference at the covered gene.
- Repeat the "Match the Pair, Not the Count" answer slide for every gene pair as a reminder.
- Set up the discrepancy between outer-pair recombination and the map sum before explaining it.
  Use a generated example with a clearly visible gap and show why double recombinants escape
  the outer-pair count. Retain a simple teaching sequence rather than adding complexity.
- Keep semantic color hues and saturation stable across tables, diagrams, and number lines;
  vary lightness for readable fills. The instructor clarified that saturation changes, rather
  than inconsistent hues, made the earlier color relationship difficult to follow.

## StVC office-door flyer (2026-10-28)

- Make a standalone printable PDF for an office door. Lead with Dr. Voss' Stump the
  Vibe Coder podcast. Use existing episode thumbnails featuring the hosts to show
  the show itself and their collaboration. Restore the portrait from `~/nsh/syllabus/`
  to reinforce the personal invitation, keeping "Stump the Vibe Coder" dominant.
- Use the human's invitation: "Check out Dr. Voss' podcast!" and "We use AI LLM agents
  to make science and biology games you can play. Watch us build them and see what happens!"
  The podcast is about people experimenting with AI together.
- Invite participation: "Join us live on YouTube!" followed by "Wednesdays, typically
  around 8 p.m. Central." and "Scan to watch us live, or catch up on past episodes."
- Enlarge the main QR when space permits. Prefer more photographic host thumbnails;
  the "Science Throws Hands" thumbnail is more cartoonish than the human likes.
- Preserve the approved podcast/game balance and two-by-two game section. Recompose
  the podcast through alignment, grouping, spacing, and natural text wrapping: invitation
  and dominant title lead into the description, livestream information, and QR. Keep the
  episode thumbnail relatively small and the portrait recognizable but secondary.
- Use mixed-case Atkinson Hyperlegible Next for surrounding text and stylized SVG
  wordmarks for game identities. Preserve original logo proportions.
- Include Ms Taq Man, Plaque Attack, Isp & Pac: Bad Cell Day, and Steroid Quest from
  `/Users/vosslab/nsh/TYPESCRIPT`. Plaque Attack replaces the early Fold Spacer choice.
- Put the YouTube logo inside the prominent main QR. Smaller game QR codes may be
  1 to 1.2 inches square, with colors from [COLOR_PALETTE.md](COLOR_PALETTE.md).
  Remove logos from the game QR codes: the tiny images add noise.
- Treat the games as miniature advertisements, with compelling artwork and short hooks
  explaining the experience. The evergreen podcast receives at least half the page;
  the four recent games together receive at most half. This supersedes the earlier
  request for roughly 60% games. Recompose the page rather than simply resizing rows.
- Explore genuinely different visual concepts through independent designers and reviews;
  the previous flyer is a content reference, not a layout template.
- Design primarily for physical printing: predominantly white, generous negative space,
  no large solid-color fields or filled card backgrounds. Use typography, borders, small
  accents, and illustrations to distinguish games.
- Adapt source SVG fills and strokes for light backgrounds, preserving recognizable game
  identities. Prefer intentionally composed action scenes over copied dark landing pages.
- Make game wordmarks intentionally light-mode: strong filled lettering, without the
  pale outlined lettering inherited from dark-mode logos. Improve the games' personality
  and appeal while reducing their footprint.
- Judge by whether a passerby would stop, look, and try a game; layout organization alone
  does not meet the brief. Inspect Letter-size rendering and verify QR functionality.

## MathJax minimum version

- Require `"@mathjax/src": ">=4.1.3"`. Agents keep putting back `"@mathjax/src": "^4.0.0"`;
  do not restore that older range (November 3, 2026).

- Do not allow vulnerable xmldom 0.9.10: require `@xmldom/xmldom >=0.9.12` across the
  dependency tree, not only in the current resolved lockfile (November 3, 2026).
