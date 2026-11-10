# Weekly announcement decks

Use this guide when preparing or reviewing `lect##a` announcement decks. It collects the current
working structure from [../HUMAN_GUIDANCE.md](../HUMAN_GUIDANCE.md). HG retains the instructor's stated
preferences; this file is the practical guide, not a requirement to show every reusable slide.

Use [COLOR_GUIDE.md](COLOR_GUIDE.md) and
[VOICE_GUIDE.md](VOICE_GUIDE.md) for color and wording. The content-deck structure in
[PEDAGOGY_GUIDE.md](PEDAGOGY_GUIDE.md) is separate from the announcement sequence here.

A conversion usually starts with two announcement decks: the most recent current-year
`lect##a`, which may be from an earlier lecture, and the target lecture's `lect##a` from the
prior year. Use the current-year deck for current formatting and course information, and the
prior-year deck for useful week-specific activities and reminders. Combine them into the target
lecture's current-year announcements, checking dates and relevance against the current schedule.

## Opening before sections

1. Title page: lecture number/letter, Announcements, instructor, and lecture date.
2. Today's Agenda: topics and activities in the current content decks.
3. Next Week: dated lookahead, mainly work due and what happens in class the following week.
4. Weather: saved NWS Chicago stories, one slide per published option.
5. Icebreaker: fun content-related prompt, with concrete examples and suggestions.

Keep this opening before the first section divider. Choose a fun question tangentially related
to some aspect of the week's content. Compare the previous two lectures' prompts and examples,
then choose a different premise and type of response. Select or adapt a prompt from
[../../evergreen/icebreakers.yaml](../../evergreen/icebreakers.yaml), write one for the topic, or
use the instructor's explicit choice. The popular-culture question is a fallback for weeks
without a topic idea. Use **Icebreaker** as the title for face-to-face classes, including Genetics.
Use `layout: prompt` with `@prompt` for the main question and `@examples` for participation cues,
concrete examples, and suggestions. The layout supplies a dark red question and dark gray supporting
text inside an ultra light course-color rounded card; write plain text in both slots.
Present examples as sample responses, and use
instructor answers when supplied. The catalog's body fragments contain both required slots.
See [QUESTION_LAYOUTS.md](QUESTION_LAYOUTS.md#open-prompts-and-icebreakers) for the format.
Use the current course schedule for the lookahead's dates, deadlines, and events.

For movie selection, bring the supplied `movie-slide-maker` ODP choices into the announcement
deck using `movie-panel`. Preserve the movie wording, ratings, and posters. Follow the individual
choices with a vote recap showing their titles and posters together. See
[DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md#movie-choices) for the text/poster slots.

## Today's agenda

Use the instructor's original agendas and slide-deck titles as the wording model. Agenda bullets
are short topic labels, usually a few words: **Karyotypes**, **Sex Dosage**, **Natural Selection**.
Put mechanisms, comparisons, and worked details on the teaching slides.

- Preserve the instructor's voice and recognizable topic names. Start with the original agenda;
  use the current deck titles to update its coverage.
- Group short topic labels under a chapter or unit when that matches the original agenda.
- Include the day's group activity, quiz, vote, or movie selection when scheduled.
- Follow the current content and teaching order when topics move between lectures. Use the course
  schedule for dated activities and assessments, and record conflicts between numbered content
  bundles and calendar weeks in the lecture review.
- Choose a layout that keeps the chapter grouping and brief topic labels readable. Inspect the rendered
  agenda for wrapping and fit.

Chapter labels belong in the agenda body; the announcement cover's topic remains **Announcements**.
When a numbered content bundle has no announcement deck or assigned teaching date, an agenda-only
source can supply its topic map. Record its status in the lecture review and add dated logistics
when the teaching week is assigned.

## Three main sections

### Informational Slides

Use `layout: section` for the divider, followed by:

1. YouTube channel.
2. Selected Stump the Vibe Coder episode, with its matching video and game/tool links.
3. Discord server information.
4. Office hours.
5. Ways to contact the instructor.
6. Anonymous-message form.

The evergreen Discord server reminder is separate from the credit-bearing signup assignment.
Keep the reminder when the signup deadline has passed.

Preserve the contact slide's four colored options: Office hours (green), Discord (red),
Email (blue), and Anonymous Google Form (purple). Keep response details nested under their
option and retain hanging list indents. Format visible email addresses as italic `mailto:`
links, for example `[_nvoss@roosevelt.edu_](mailto:nvoss@roosevelt.edu)` in Djot.
The former Gmail warning was a 2019 issue and is retired.

Preserve the established first-person contact and anonymous-message wording. Keep explanatory
text in regular dark type. Give the contact details the slide's full width, and organize related
lines together. The anonymous-message slide pairs plain instructions with the original form image
and a visible clickable form URL.

### Biotechnology classroom Zoom

BIOL 480 Biotechnology has a course Zoom component. Genetics and Biostatistics do not use
this classroom Zoom group. Keep ordinary office-hours information separate.

For Zoom breakout activities, title the selected icebreaker **Breakout Room Chat**.

Include [../../biotech/evergreen/zoom_guidance.djot](../../biotech/evergreen/zoom_guidance.djot) visibly in Informational
Slides, before Course Content. Preserve these three original Lecture 07 reminders:

1. How to Use Zoom Like a Pro: course meeting link, mute when not speaking, headphones or
   earbuds, and video advice for a slow connection.
2. Setting Your Name in Zoom: proper first name or consistent nickname, discussion-mark
   sorting, and renaming during class.
3. Change Name Before a Meeting: set the profile display name before joining.

The class meeting link uses `{{course_url:zoom}}`; office hours uses
`{{course_url:office_hours}}`. Resolve both from the ignored local course-links file.
Refresh software steps against Zoom's official instructions when editing the name slides.

### Course Content

Use `layout: section` for the divider. The current Genetics arrangement is:

1. Textbook.
2. Syllabus Links.
3. PREVIEW Slides.
4. Grading and Assessment subsection.
5. Assignments, Quizzes, and Exams.
6. Graded vs Total Percentage.
7. Exam/Quiz subsection: stable schedule and shared assessment policies.
8. Exam subsection, when relevant.
9. Quiz subsection, when relevant.
10. Weekly Assignments subsection: current work and deadlines.

Use `layout: subsection` for the topic dividers within this main section. Prefer assessment
overview, Exam, Quiz, then Assignments for consistency. The instructor has used both Exam/Quiz
orders; the old reverse order is not a correctness defect. Textbook placement is also flexible:
it may be informational/syllabus material or course-content/logistics material.

Show quiz guidance when a quiz falls in the current or following lecture week. Check exam
relevance against the schedule. Retain reusable groups hidden when they are not needed, with
visibility controlled in the weekly master. Update dated references before showing them again.

On the assessment schedule, keep one abbreviated `item: date` per line. Past assessments are
light gray, next-week assessments dark red, and later assessments black. Keep the list and
positions stable; change status colors rather than adding completion labels.

### General Announcements

Use `layout: section` for the divider. Usually only one seasonal topic is active at a time;
this is a menu of relevant groups, not a list to display every week.

| Topic | Display rule |
| --- | --- |
| Graduating Students | First two weeks of class only; refresh dates before showing. |
| Spring registration and upcoming courses | Midsemester, roughly October 15 through December 1. |
| Course evaluations | End of semester, during the actual evaluation period. |
| Natural Science Club | Hidden for now; the instructor has not decided how to restart it after COVID. |
| One-off announcements | Relevant campus seminars, events, and other timely notices. |

Registration includes the reminder/links, a summary of upcoming teaching, and one slide per
course. Keep tentative assignments visibly tentative. Evaluation incentives belong to the
specific course; do not copy Genetics final-exam incentives into Biotechnology.

The individual upcoming-course pages explain both what students will study and how the course
works. Preserve useful instructor descriptions, activities, and assignments while refreshing
logistics; a title/time/location list is insufficient. See
[../../evergreen/UPCOMING_COURSES_SOURCES.md](../../evergreen/UPCOMING_COURSES_SOURCES.md) for the shared pages' sources.

Finish with THE END. Biotechnology retains its special Veridian Dynamics ending immediately
before THE END, after general announcements. This closes the announcements deck, not the whole
lecture. Leave Veridian Dynamics off Today's Agenda.

Use the selected film's transcript for a short, characteristic tagline or quotation beside the
existing logo. The instructor's local film library has episode-specific text under
`MOVIES/biotech_movies/Veridian_Dynamics/transcripts/`. Match the numbered film and title;
keep transcript/source details in the review report rather than on the slide.

## Signup and profile deadlines

Discord signup and Student Profile assignments run through September 21 in fall and February 14
in spring. Keep their assignment reminders visible through that date, then hide them. Do not use
the graduation notice's first-two-weeks window for these assignments.

## Weekly preparation

- Check the lecture date and the current instructor-maintained course schedule first.
- Start from the most recent current-year lecture, checking the matching prior-year lecture for
  useful activities and reminders. Refresh dates, policies, and links from current sources.
- Update Today's Agenda with short deck titles or topic labels in the instructor's voice, then update
  Next Week, assessment colors, due dates, and conditional visibility.
- Refresh weather on lecture day or the preceding day. Keep original PNGs, full editable
  captions, and a separate dated NWS citation. Builds use saved files and never refresh weather.
- Select the latest regular StVC episode published by the lecture date; skip special episodes
  such as #38. Unless the instructor selects another eligible episode, use publication time,
  not episode-number order. Verify its thumbnail, title, video, and game/tool destination.
- Reuse shared fragments: root `evergreen/` for cross-course groups and the course's own
  `evergreen/` for course-specific material. Keep dated agendas, weather, and episodes weekly.
- Preserve course-specific material: Biotechnology talking marks/news and Veridian Dynamics;
  Biostatistics tutorials, projects, graduate milestones, and meeting format. Biostatistics has
  no exams; do not import Genetics assessment rules into it.
- Keep private Discord/Zoom values in ignored `course_links.local.yaml`, referenced through
  `{{course_url:key}}`. Keep student-visible URLs intact and clickable.
- Lint, build editable ODP and PDF, inspect changed slides, and verify order and hidden groups.
  Record the source schedule, changed visibility, build warnings, and verification in the
  lecture review. Run Python with `source source_me.sh && python3`; run every LibreOffice build
  outside the sandbox. Use root `_temp/` for review artifacts.

For refresh/build commands, see [../USAGE.md](../USAGE.md). For conversion and handoff checks, see
[../SLIDE_CONVERSION_CHECKLIST.md](../SLIDE_CONVERSION_CHECKLIST.md). For layout syntax, see
[DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md). Existing historical decks are not automatically
rewritten when this guide changes; honor any explicit preservation instruction.
