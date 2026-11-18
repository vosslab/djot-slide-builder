# Human guidance

<!-- VENDORED HEADER: START -->
Record the durable guidance Neil Voss states, or approves for preservation here, in his own words:
first person or close paraphrase, one to three lines per bullet. Material he supplies as a source
may inform [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) once it is settled, and an entry of uncertain
origin belongs there too. Rules: [REPO_STYLE.md](REPO_STYLE.md).
[PROPAGATED HEADER - ENTRIES BELOW ARE YOURS]
<!-- VENDORED HEADER: END -->

- Use fixed palette hues across figures. Keep a consistent hue and choose from extra light,
  light, medium, dark, and extra dark as the figure requires (November 18, 2026).

- I prefer SVGs without a canvas background so the natural slide background shows through.
  Use tighter crops, including C44, rather than unnecessary outer padding (November 17, 2026).

- For chromosome gene labels, C53 does it best, with C01/C47 second best. Use consistent
  locus placement and distinguish gene regions from chromosome banding and colored sections
  (November 17, 2026).
- Revisit C25, C26, C60 and C63's gene labels and establish official gene-label guidance
  and a shared pipeline (November 17, 2026).

- Add the rendering date/time, including seconds and time zone, to slide 1 and the final THE END.
  Use small IBM Plex Sans Condensed type that blends into the background and stays clear of
  the ending outline so I can tell whether the deck has been updated (November 17, 2026).

- By "fully formed" I mean condensed chromosomes. Uncondensed, stringy DNA in early
  prophase should use simple paths without the full BPQ polish. Keep SVG files smaller
  (November 17, 2026).

- Reserve `exemplars/` for pre-approved best examples that agents should model. Put corpus
  collections awaiting instructor critique in `prototype/`, outside the growing `_temp/` folder;
  inclusion does not imply approval.

- Keep authoritative color, voice, and pedagogy specifications together in `docs/slide-specs/`;
  other documentation should cross-link to them. Consolidate my established preferences without
  reinterpreting them; BPQ guidance and research supply supplementary ideas.

Working specifications: [slide-specs/COLOR_GUIDE.md](slide-specs/COLOR_GUIDE.md),
[slide-specs/VOICE_GUIDE.md](slide-specs/VOICE_GUIDE.md), and
[slide-specs/PEDAGOGY_GUIDE.md](slide-specs/PEDAGOGY_GUIDE.md).

- Avoid "Down syndrome vs normal"; I prefer "Down syndrome vs wildtype." Check posed
  questions as well as explanations, so the wording does not classify people as "other."
- In Genetics 10D, connect the testing sequence to the disorder: Down syndrome, then the
  easy blood and ultrasound screening tests, then invasive diagnostic sampling for a karyotype
  after a positive screen. Keep false positives and false negatives explicit.
- Finish the Genetics 10D content, including CVS/PUBS, before the Iceland video. Leave space
  afterward for parental choice vs eugenics, then the NYTimes testing-too-much discussion.
- Introduce companies advertising eye-color selection and ask what else students would consider:
  other diseases, ADHD, or athletic ability.

- Ground my voice guide in evidence from my established slides, with exact examples and sources.
  Distinguish what the slides demonstrate from my stated preferences and editorial suggestions.

- I consider quality-90 WebP a permanent replacement for PNG: smaller, with similar quality.
  For weather stories, fetch the PNG and save it as WebP.

- Use 90% HSL lightness for the ultra light course color, retaining its hue and saturation.

- Keep an extensive, reusable recipe in `docs/` for future talking-point slide builds,
  covering best practices, tools, organization, and the input files.

- Implement queued messages and finish their requests. Do not depend on feedback questions;
  I may never see them. Use the recorded guidance and available evidence to complete the work.

- Use `source source_me.sh && python3 ...` for Python commands, including SVG work.
  Follow [REPO_STYLE.md](REPO_STYLE.md) as the master repository guidance (November 17, 2026).

- Retain tests enforcing Djot syntax and authoring guidelines even when their exact assertions
  would otherwise look fragile. Tests must not force implementation to stay in monolithic files.

- Keep bytecode caches visible to detect agent mistakes; do not add a `__pycache__` ignore rule.
  Honor the bootstrapped Python environment when running checks.
- Use `pyflakes` and focused pytest checks in the bootstrapped environment; keep validation
  bytecode-free (November 17, 2026).
- Phrase task briefs positively, naming the actions and tools needed for the work. Positive
  instructions plus omission of irrelevant tools work best for small models (November 17, 2026).

- Keep source provenance portable instead of embedding machine-specific absolute paths.

- Divide overly long files cohesively by responsibility instead of trimming them to pass
  the source-file line limit.

- Keep Biotechnology Djot folders inside their corresponding `LECT##/` folders.
- Delete obsolete Djot assets along with their obsolete source copies instead of saving
  another `old/djot_assets/` folder.

- Remove obsolete retired slide sources once their replacements are accepted; preserve the
  meaningful history in documentation rather than keeping duplicate source files.

- I must be able to select and copy PDF slide text, including framed bookends, definitions,
  sections, THE END, and reference slides. Decorative borders must not block selection; outline-only borders should have no fill.

- Use black table-header text on light course-colored backgrounds.

- Use comfortable default table-cell padding, center all table headings, and vertically
  align table-cell content in the middle.

- Frame three-gene order as three choices: choose the middle gene. Show that reversed
  orders represent the same map.

- Color the three-point testcross procedure like the LECT07 chi-square steps, and repeat the
  matching colored roadmap before starting a new problem. Preserve colored text during conversion and explicitly check that preservation in the conversion checklist.
- LECT08D and LECT08F must use the same canonical six-step three-point testcross slide and
  identical colors throughout. Reference the shared slide rather than maintaining separate copies.
- Use black procedure-roadmap titles so attention stays on the colored steps. Repeat the shared
  six-step slide at gene-pair transitions, before new practice problems, and when returning to genotype summaries or distance calculations; do not limit it to the initial introduction.

- Handle detected runts automatically by pushing more words onto the final line when useful.
  Preserve wording, styling, and font size; prefer balancing line breaks over manual rewriting.

- Use a thin, angular frame with matching diagonal breaks at opposite corners for bookend
  and definitions slides. Preserve the reference image's symmetry, use one course hue with light/dark variations, and keep the frame out of the content area. Accents are welcome; omit the earlier arbitrary thick corner segment.

- Use Title Case for all slide titles. This is the general slide-title rule, not a special
  treatment for Learning Objectives or Key Takeaways. Preserve standard spelling of acronyms, proper names, gene symbols, and scientific notation.

- Keep bookend and definitions frames and accents in the selected course hue. Saturation
  and lightness may vary for visual emphasis and contrast; avoid unrelated accent hues.

- Use one dedicated `bookend` layout for both Learning Objectives and Key Takeaways.
  Give these lecture bookends similar visual attention. Use a dedicated `definitions` layout that enforces term formatting and gives definitions a recognizable frame.

- Use straight ASCII quotation marks and apostrophes in Djot text. Write a plain apostrophe
  instead of `&#8217;`; normalize literal curly quotes and their numeric or named entities.

- Use `@speaker-notes` as presentation note cards for lecturing, with speaking prompts,
  explanations, and reminders useful while teaching.
- Keep citation research, data provenance, and slide development notes in a separate file
  beside the decks. See [slide development notes](slide-specs/AUTHORING_GUIDE.md#slide-development-notes).
- Give Python recipe docstrings room to explain the motivation for figure choices and the
  assumptions behind them.

- Ignore runts when the font is at its maximum size and the paragraph is the final displayed
  paragraph of its text block. Keep title-wrap and URL-width checks active.
- Run the Djot audit on Genetics LECT08 and reduce warnings with simple changes.

- Build a Python Djot auditing script, prioritizing title line wrapping and runt checks.
  Keep lecture-quality checks in the audit rather than making lecture wording a pytest gate.

- Avoid single-word final lines in generated learning objectives; aim for final lines at least
  one-third of the text width. Generated objective wording may be shortened or lengthened for this purpose. Preserve instructor-authored wording unless changes are separately authorized.

- Go through LECT08 and use a labeled image with a quality-90 WebP embedded in SVG where
  it makes sense. Limit each figure to one image and its associated labels; labels can sit
  outside the image. Keep slide titles, captions, and surrounding text native.

- Managers must follow the [slide conversion checklist](SLIDE_CONVERSION_CHECKLIST.md).
  Keep its items concrete actions with verifiable results; keep broader content policies here.

- Keep Lecture 07B's intro and miscellaneous material, including peer evaluation, in the main
  file. Split Three Ideas, One Great Idea, Shark Tank, and Executive Summary into chapter files; allow one hidden flag to hide the entire One Great Idea section.  Number these chapter files `lect07b1-`, `lect07b2-`, `lect07b3-`, and `lect07b4-`.

- Source slide animations should flag conversions that lose a question/answer reveal. Make the
  importer fix durable rather than repairing only Lecture 06D slide 36.

<!-- VENDORED HEADER: START --> Record the durable guidance Neil Voss states, or approves for preservation here, in his own words: first person or close paraphrase, one to three lines per bullet. Material he supplies as a source may
inform [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) once it is settled, and an entry of uncertain origin belongs there too. Rules: [REPO_STYLE.md](REPO_STYLE.md).  [PROPAGATED HEADER - ENTRIES BELOW ARE YOURS] <!-- VENDORED HEADER: END -->

## Content titles

- I prefer slide titles to fit on one line, leaving more room for the content.  - Remove textbook figure identifiers such as `Figure 15.12`, `Figure 15.UN01`, and `Fig. 17-4`
  from converted slides, including headings, captions, citations, and editable diagram labels.  They are textbook-slide artifacts. Preserve the useful explanatory caption and diagram content.

- Subsection backgrounds should be a variation of the course-dependent section color.
- Keep divider backgrounds recognizably course-colored, with the original course hue and saturation.
- Define dark, medium, light, and ultra light course colors. Keep the steps from black through
  dark, medium, and light to white at least 2:1, aiming near `21**(1/4)` (2.14:1).
- Use my November 10 `section_headers.odp` / `section_headers.pdf` as the appearance reference.
  Their colors are guesses; use the measured course colors.
- Keep slide text editable. Decorative shapes are an implementation choice; my LibreOffice
  shapes demonstrate the appearance I want using the tool available to me.
- Sections use dark color, white text, and a rounded frame. Subsections use a light center band,
  medium top/bottom, and black text. Subsubsections use a dark center panel, light edges, and
  white text.
- Use an ultra light center hexagon and dark corners for the open-ended `question-ask` layout,
  with dark red question text. Use ultra light cover cards,
  a medium-to-white header gradient, and dark end slides with ultra light THE END text.
- Use question-ask slides sparingly: a divider-like card with a question to ponder. Genetics
  Lecture 04H slide 5 and Lecture 06D slide 43 are examples. Icebreakers use the separate `prompt`
  layout with a colored prompt and required dark supporting examples.

## Labeled diagram reconstruction

- Evaluate raster-to-SVG replacements directly at their intended display size whenever possible.
  Keep the drawing checks simple; use Djot-to-PDF only when a specific consumer concern needs it.

- I ignore SVGs with copyright information for a reason. Preserve that protection when
  adding tracking exceptions.
- We need a better way to distinguish drawn SVGs from SVGs containing images, because
  the images are typically copyrighted.

- Refresh 09H's images when I update the ordered-tetrad generator visuals. Add an opening
  definitions slide for FDS, SDS, and spore.

- In 09G, cover the unused gene while comparing a pair. Keep the main parental-ditype
  row highlighted across pairs: its genotypes and count do not change.
- Show a whole page of my handout on the Your Turn slide. I like visuals.  - In 09G, keep the bottom-right distance table the same size through slides 11-15,
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
  A figure contains one image and its associated labels, including labels outside the image.
  Keep slide titles, captions, ordinary prose, and layout outside that figure in native Djot.

- Implement the LECT08B source-6 Punnett-square cover relative to its image content, so the
  box follows the image and disappears on click.

## Equation pipeline

- Build better conceptual bridges into the tetrad equations. Keep my voice and break the
  concepts into small pieces.
- The centromere connection for unordered tetrads is not needed. Cover ordered tetrads and
  their centromere connection, with a worked problem from the ordered-centromere generator.

- Editability inside ODP/PPTX is not a repository requirement; keep equations editable in Djot.  - Use rich LaTeX math syntax with MathJax-to-SVG rendering. Genetics LECT07C, with its many
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
  Use a pale, desaturated course-color fill behind the text. If filling it prevents copying, use an unfilled rectangle with a thicker, course-colored outline instead.
- Include parenthesized chi-squared in the chi-square title, authored as `(&chi;^2^)` for editable
  native superscript text.
- Enforce the universal Djot slide 1 format with pytest across courses and lectures.

## Exam and quiz schedule

- On the quiz/exam dates slide, show past assessments in light gray, future assessments in
  black, and assessments at the next class meeting in dark red.
- Exam and quiz schedule text is fixed: one "item: date" per line, using abbreviated month and
  day, such as "Quiz 1: Sept 22". Change only status colors; do not add "completed", descriptions, combined assessments, or mixed bolding. Put a long schedule URL in `@citation`; reserve `@speaker-notes` for presentation note cards used while lecturing.
- Think of the exam and quizzes page as a progress bar: keep the list and positions stable,
  with colors showing completed, next-class, and future assessments.

- Show the quiz-guidance slides when a quiz falls in the current lecture week or the following
  week; hide the group otherwise. Use the current lecture date and course schedule to decide.
- Keep quiz and exam guidance in course-wide evergreen Djot groups so one `hidden: true`
  or `hidden: false` setting in each weekly master controls the entire group. Use `genetics/evergreen/` for Genetics and explicit `repo:` includes, rather than copies under LECT08.
- After the weekly agenda and chosen icebreaker, share the constant opening material, including
  the YouTube channel, contact information, textbooks, course links, grading explanations, and assessment policies. Keep weekly agenda content, icebreaker selection, podcast episode, assessment status colors, and dated deadlines in the weekly master.

## Course links and evergreen announcements

- Keep subsection dividers bilaterally symmetric, with a light center band and equal medium-color
  regions at the top and bottom, following the November 10 reference.

- Remove the obsolete Gmail-account warning from my contact slide; that issue was in 2019.
  Preserve the purple anonymous-form option and hanging bullet indents. Email addresses
  should be italic and styled as clickable links, like URLs.

- BIOL 480 Biotechnology has a course Zoom link, unlike Genetics and Biostatistics. Include
  the class Zoom link and headphones/earbuds reminder in Biotechnology announcements, and
  preserve its course-specific Zoom guidance in the announcement-deck guide.
- Use my established slides as the wording model for talking-point guidance; the syllabus
  manager made prose changes I have not cleaned up. It is 90 seconds in Fall 2026 because the
  class is smaller. Discussion Marks were dropped because some students attend face-to-face.
- Keep visuals in the Zoom name reminders and optional textbook slide. Use the shared genetics
  contact slide. Include the three historical film-course schedules as movie-content examples.

- Put a Veridian Dynamics subsection transition before its episode slide. Make section and
  subsection dividers visibly distinct; their previous treatments were hard to tell apart.

- Give course slides nested bullet hierarchy rather than a flat list. Use a textbook-cover
  image for BCHM 355/455, using the LibreTexts image I supplied (November 5, 2026).

- Use my November 5 Course Finder listings for Spring/Summer 2027 logistics: biochemistry
  lecture Thursday 2-4:30 p.m. (SCH 612), lab Tuesday 10 a.m.-1:55 p.m. (SCH 550),
  and film Tuesday/Thursday 6-9 p.m. on Zoom, July 6-August 9. Preserve the course descriptions.

- The working guide for `lect##a` preparation is [slide-specs/ANNOUNCEMENT_DECK_GUIDE.md](slide-specs/ANNOUNCEMENT_DECK_GUIDE.md). This section records the instructor's stated preferences; the guide assembles them into the current weekly workflow.

- Canonical announcement order: title, agenda, weather, icebreaker, Next Week, Informational Slides,
  YouTube channel, Stump the Vibe Coder, Discord, office hours, contact, anonymous messages, Course Content, textbook, Syllabus Links, PREVIEW Slides, Grading and Assessment, Assignments/Quizzes/Exams, Graded vs Total Percentage, Quiz/Exam
  schedule and policies, Exam when needed, Quiz when needed, Weekly Assignments, General Announcements, spring registration when needed, evaluations in their display period, Natural Science Club (hidden for now), then THE END (November 3, 2026).
- The three main sections are Informational Slides, Course Content, and General Announcements.
  Title, agenda, weather, icebreaker, and Next Week are before the first section. Informational Slides contains YouTube/STVC and contact information. Course Content contains textbook/syllabus, Grading and Assessment, Exam/Quiz overview,
  Exam, Quiz, and Weekly Assignments. Use subsection dividers for these course groups and for registration, evaluations, and club under General Announcements.
- Keep the original opening order; registration belongs after course logistics.  - Weekly announcement decks have not always been aligned; missing items often reflect
  forgetting them, not an intentional alternate structure. Apply the consistent template going forward while keeping seasonal groups conditional.
- Put a Next Week slide after the icebreaker, focused on work due and what
  happens in class the following week. Use the current course schedule; do not invent events.
- Keep the major announcement sections guiding the deck. Put Quiz 5 Vote at the normal Quiz
  position under Course Content, and movie selection under General Announcements, with subsection
  cards. Participation order does not mean putting all activities at the front.
- Keep my voice in agenda slides. Use slide-deck titles and a few words for topic labels,
  such as "Natural selection". Match my original agenda examples.
- For new live teaching text, use concise statements, phrases, and labels; I do the talking.
  Short complete sentences are fine. Target LLM-authored additions in a voice review; preserve
  my established prose and first-person wording as the baseline.
- Use color for meaningful distinctions. Keep announcement explanations in regular dark type;
  use spacing and hierarchy to make them readable, with the original contact-method colors.
- Use a `movie-panel` layout for movie-slide-maker output: editable text fills the left, with a
  designated portrait-poster area on the right that preserves the poster's consistent aspect ratio.
- Textbook placement can be informational/syllabus or course-content/logistics; neither is a
  correctness failure. The current shared Genetics group places it under Course Content.
- There is no fixed historical Exam/Quiz order. Prefer assessment overview, Exam, Quiz,
  then Assignments for consistency, rather than treating the reverse order as an error.
- Discord signup and Student Profile assignments run until September 21 in fall and February 14
  in spring; hide their assignment reminders afterward.
- Biotechnology has a special Veridian Dynamics ending: retain it after general announcements
  and before THE END in the announcements deck. It closes announcements, not the lecture;
  leave Veridian Dynamics off the agenda. Use the local film transcripts to give its slide flair.
- For Fall 2026 Biotechnology Lecture 10, the individual projects are complete. Adapt the
  prior-year group guidelines using the current syllabus schedule.
- Use my original ODP language and formatting for the group-project slides; use the syllabus
  for the timeline. Restore my color, emphasis, hierarchy, and visuals instead of walls of black text.
- Roll out group-project details as needed. With presentations a month away, hide the finer
  presentation details; the current focus is group formation and the group vision form.
- For now, show only that the group presentation exists, its point value, and its date.
- Selecting the group project means completing the Company Vision Report (Form). Both are due
  November 19, 2026; December 3 is too late.
- Enrich the talking-point slides with more useful images from the annual student decks.
  The instructional content is fine; improve the overly plain visual presentation while preserving it.
- Put each talking point's complete questions on one setup slide after its subsection, then content.
  Smaller text is okay there; use the Key Takeaways frame to make the questions stand out.
- Use question-answer layouts for the Discovery or Invention guessing game, and the movie layout
  for Dark Waters. Keep low-quality images in regular panels rather than enlarging them.
- Use the successful Set #4 approach for Set #5: combine the Fall 2021-2026 student material
  with my expanded instructor ODP, using the 37-topic 2026 list to control coverage and order.
- General Announcements rarely has more than one active topic: Graduating Students in the first
  two weeks, registration midsemester, evaluations at semester end, and one-off events such as campus seminars when relevant. Natural Science Club remains hidden for now; the instructor has not decided how to bring it back since COVID.

- Use root-level `evergreen/` for slides shared across courses. Keep course-specific reusable
  slides in that course's `evergreen/` folder, and dated weather/podcast snapshots with the lecture.
- Keep `icebreakers.yaml` and similar reusable teaching content in `evergreen/`.

- Spring registration slides are evergreen. Show them roughly October 15 through December 1,
  including in Genetics 09A and 10A.
- I mostly teach seniors and graduate students. Give only the first registration day; students
  can look up the registration date that applies to them.
- Point students to the Registrar and Course Finder for registration. Do not assume which
  registration system they use. The Course Finder is https://banner.roosevelt.edu/ssbprod/bwskzenr.P_CourseFinder.
- Keep my original spring-registration wording and the Registrar/Course Finder links;
  do not expand it with new advising instructions.
- Include a summary of all my upcoming courses and an individual slide on each in the
  shared spring-registration group (November 3, 2026).
- The individual upcoming-course pages should give students a sense of the course's structure
  and content. Preserve those descriptions instead of reducing each page to scheduling details.
- I generally teach the same courses every year; mostly change the year to 2027 and also
  list my summer course.
- BCHM 355/455 Biochemistry Lecture: Thursday afternoons, 2-4:30 p.m. (November 5
  listing supersedes my earlier 1:30 start), face-to-face Schaumburg. BCHM 356/456: face-to-face Schaumburg, less structured and more independent study-like (November 3, 2026).
- I am probably teaching BIOL 301 this spring as a third course, but it is not locked down yet.
  Mark the teaching assignment as tentative in course announcements.

- A prior lecture's announcement deck copied into a new lecture folder is a starter for the
  new weekly A deck. Do not keep that starter or its unused extracted assets in the new folder.
- Announcement conversions usually start with the most recent current-year deck, even if it
  is from an earlier lecture, plus the target lecture's prior-year deck. Use both as starting points.

- Evergreen content is used across courses or across more than a single week. Tetrad content
  is for a single lecture; keep it with Lecture 09, including the repeated procedure slides.

- Support `@citation` on all slide layouts for URLs or article citations in smaller condensed
  text at the bottom. Normal layouts keep their full space; citations use the bottom margin.
- Put very long URLs in `@citation` when they crowd slide content. Keep the complete URL
  visible and clickable, following the instructor-edited Genetics LECT08 announcements.

- Use a YouTube slide generator with the existing StVC-style `big-image` layout: thumbnail,
  title, and visible clickable full `https://www.youtube.com/watch?v=...` URL.  A separate layout type is unnecessary; there is room for the full URL.

- Course Zoom and Discord URLs are not on the syllabus; include the actual course URLs in the
  student slides. Only Biotechnology has a Zoom meeting this semester (Fall 2026).
- Any URL for the course should be in the slides. The slides are generally available only to
  students, and we already give them QR codes. Keep the URLs visible and clickable alongside the QR codes; do not substitute "The sign-up link is available on Blackboard."
- Store private Discord and Zoom URLs in ignored root `course_links.local.yaml` and import
  them into slides with `{{course_url:key}}` references, keeping the configuration out of GitHub.
- The YouTube channel slide must include a visible, clickable link to Dr. Voss's channel.  - YouTube URLs, including Dr. Voss's channel, and other public course links remain directly in
  tracked Djot sources; they do not need private configuration.
- The opening "Discord Server" slide is evergreen and stays in the deck. After the signup
  deadline, hide the Discord signup assignment; retain it for reuse rather than deleting it.
- Carry the first weeks' assignments, including Student Profile and Discord signup credit,
  forward as hidden slides after their deadlines. Retain eventual course-evaluation slides hidden until they are needed. Preserve this reusable inventory when preparing each new week; use separate included groups for convenient visibility
  control. Refresh evaluation deadlines before displaying them; never copy an obsolete date forward as a current deadline.

## Robustness and simplicity

- This codebase is pre-production and has no users. Improve foundational schemas, contracts,
  abstractions, and ownership boundaries when that produces the stronger long-term design.
  Update callers directly and remove obsolete interfaces instead of retaining compatibility pointers.

- Builds must work without a `.git` checkout. If `git rev-parse` is unavailable or fails,
  use the current working directory as the project root.

- Focus on important issues, not bikeshedding. Address the highest-impact risks first.
  Spend review time on correctness, maintainability, validation, and delivery.
- Robust software continues to function despite imperfect inputs, data, state, or behavior.
  Handle imperfections according to context and impact; recover gracefully to preserve useful operation whenever possible.
- Apply KISS aggressively: prefer the smallest coherent design that satisfies actual requirements
  and known failure modes. Mechanisms, abstractions, policies, state, and tests must solve a demonstrated need. Complexity must earn its place.

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

## Slide authoring and conversion

- See [HUMAN_SLIDE_GUIDANCE.md](HUMAN_SLIDE_GUIDANCE.md) for slide-writing advice,
  conversion review, and teaching voice.

## StVC office-door flyer (2026-10-28)

- Make a standalone printable PDF for an office door. Lead with Dr. Voss' Stump the
  Vibe Coder podcast. Use existing episode thumbnails featuring the hosts to show the show itself and their collaboration. Restore the portrait from `~/nsh/syllabus/` to reinforce the personal invitation, keeping "Stump the Vibe Coder" dominant.
- Use the human's invitation: "Check out Dr. Voss' podcast!" and "We use AI LLM agents
  to make science and biology games you can play. Watch us build them and see what happens!"  The podcast is about people experimenting with AI together.
- Invite participation: "Join us live on YouTube!" followed by "Wednesdays, typically
  around 8 p.m. Central." and "Scan to watch us live, or catch up on past episodes."
- Enlarge the main QR when space permits. Prefer more photographic host thumbnails;
  the "Science Throws Hands" thumbnail is more cartoonish than the human likes.
- Preserve the approved podcast/game balance and two-by-two game section. Recompose
  the podcast through alignment, grouping, spacing, and natural text wrapping: invitation and dominant title lead into the description, livestream information, and QR. Keep the episode thumbnail relatively small and the portrait
  recognizable but secondary.
- Use mixed-case Atkinson Hyperlegible Next for surrounding text and stylized SVG
  wordmarks for game identities. Preserve original logo proportions.
- Include Ms Taq Man, Plaque Attack, Isp & Pac: Bad Cell Day, and Steroid Quest from
  `/Users/vosslab/nsh/TYPESCRIPT`. Plaque Attack replaces the early Fold Spacer choice.
- Put the YouTube logo inside the prominent main QR. Smaller game QR codes may be
  1 to 1.2 inches square, with colors from [COLOR_PALETTE.md](COLOR_PALETTE.md).  Remove logos from the game QR codes: the tiny images add noise.
- Treat the games as miniature advertisements, with compelling artwork and short hooks
  explaining the experience. The evergreen podcast receives at least half the page; the four recent games together receive at most half. This supersedes the earlier request for roughly 60% games. Recompose the page rather than simply resizing rows.
- Explore genuinely different visual concepts through independent designers and reviews;
  the previous flyer is a content reference, not a layout template.
- Design primarily for physical printing: predominantly white, generous negative space,
  no large solid-color fields or filled card backgrounds. Use typography, borders, small accents, and illustrations to distinguish games.
- Adapt source SVG fills and strokes for light backgrounds, preserving recognizable game
  identities. Prefer intentionally composed action scenes over copied dark landing pages.
- Make game wordmarks intentionally light-mode: strong filled lettering, without the
  pale outlined lettering inherited from dark-mode logos. Improve the games' personality and appeal while reducing their footprint.
- Judge by whether a passerby would stop, look, and try a game; layout organization alone
  does not meet the brief. Inspect Letter-size rendering and verify QR functionality.

## Illustration script organization

- C28 is exemplary; the only addition I want is our white zigzag for joined chromosome material.
  I am considering a differentiability requirement because C18, C30, and C57 have awkward corners.
- Use consistent recipe names for slide-specific SVG illustration scripts.
- Keep lecture-specific artwork code with its lecture; keep shared drawing tools in `svg_tools/`
  and repository development utilities in `devel/`.

## General icons

- For general icons, I prefer Font Awesome.

## MathJax minimum version

- Require `"@mathjax/src": ">=4.1.3"`. Agents keep putting back `"@mathjax/src": "^4.0.0"`;
  do not restore that older range (November 3, 2026).

- Do not allow vulnerable xmldom 0.9.10: require `@xmldom/xmldom >=0.9.12` across the
  dependency tree, not only in the current resolved lockfile (November 3, 2026).

- NEVER repeat an icebreaker in the same course semester, including reworded repeats.
  The manager must check the whole semester. If no fresh prompt can be found or verified,
  I would rather have a visible REPLACEME placeholder with `@replaceme` than a repeat.

- Agenda content must be grouped under its chapter. Genetics LECT11 groups Gene Trees,
  Gene Tree Group Activity, and Evolutionary Time under Chapter 11.

- "Next Week" means the next week of class. Keep a relevant break/no-class reminder,
  then focus on the next class meeting; omit later deadlines and exam dates.

- Use the original `genetics/**/lect??a*.odp` agenda slides as references for grouping
  and wording. ARTIFACTS was a folder in another repository.

- Use compact weekday/time labels such as "Wed 2:30-3:30pm" on Office Hours.
  Make the days and times stand out above the room and Zoom details.

- Keep homework off the agenda. Retain a quiz-status reminder when a quiz has moved
  from the previous schedule, as with LECT11's "Today: No Quiz".

- On Syllabus Links, keep the content labels flat and put the URLs on bullets.
  URLs should automatically be condensed and clearly smaller than ordinary text.
- Use an outline on the next-class slide: topics, quiz, and homework due at that meeting.
  Keep the break reminder and omit deadlines from later weeks.

- On Exam and Quiz Schedule, make an assessment red when it is at the next class
  meeting, including across breaks. LECT11 Quiz 4 on December 1 is red.

- Movie-slide conversion must preserve its character: popcorn/tomato rating marks,
  score highlighting, and source formatting, alongside the movie text and poster.

- Upcoming-course slides use course colors: Biochemistry Lecture purple, Biochemistry
  Lab red, Cellular and Molecular Biology blue like Genetics, and Biology and Ethics
  in Film a slightly darker purple than Biochemistry Lecture.

- Preserve original instructional images and visual character during slide conversion,
  especially annotated tree rotations and Khan Academy figures. Plain replacement
  trees must not reduce teaching quality; restore original content when time is limited.
