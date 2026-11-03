# Weekly announcement decks

Use this guide when preparing or reviewing `lect##a` announcement decks. It collects the current
working structure from [HUMAN_GUIDANCE.md](HUMAN_GUIDANCE.md). HG retains the instructor's stated
preferences; this file is the practical guide, not a requirement to show every reusable slide.

Older decks are useful sources, but inconsistent inventories can reflect forgotten material.
Check the current schedule and this guide rather than treating the previous week as complete.

## Opening before sections

1. Title page: lecture number/letter, Announcements, instructor, and lecture date.
2. Today's Agenda: topics and activities in the current content decks.
3. Next Week: dated lookahead, mainly work due and what happens in class the following week.
4. Weather: saved NWS Chicago stories, one slide per published option.
5. Icebreaker: selected prompt and concrete examples.

Keep this opening before the first section divider. Select the icebreaker from
`icebreakers.yaml` or the instructor's explicit choice. Use the current course schedule for the
lookahead; do not infer deadlines or events from last year's dates.

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

Finish with THE END. Biotechnology retains its special Veridian Dynamics ending immediately
before THE END, after general announcements.

## Signup and profile deadlines

Discord signup and Student Profile assignments run through September 21 in fall and February 14
in spring. Keep their assignment reminders visible through that date, then hide them. Do not use
the graduation notice's first-two-weeks window for these assignments.

## Weekly preparation

- Check the lecture date and the current instructor-maintained course schedule first.
- Start from the current-year previous lecture, checking the matching prior-year lecture for
  useful activities and reminders. Refresh dates, policies, and links from current sources.
- Update both agendas, assessment colors, due dates, and conditional visibility.
- Refresh weather on lecture day or the preceding day. Keep original PNGs, full editable
  captions, and a separate dated NWS citation. Builds use saved files and never refresh weather.
- Select the latest StVC episode available on the lecture date unless the instructor chooses
  another; verify its thumbnail, title, episode number, video, and game/tool destination.
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

For refresh/build commands, see [USAGE.md](USAGE.md). For conversion and handoff checks, see
[SLIDE_CONVERSION_CHECKLIST.md](SLIDE_CONVERSION_CHECKLIST.md). For layout syntax, see
[DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md). Existing historical decks are not automatically
rewritten when this guide changes; honor any explicit preservation instruction.
