# Genetics evergreen slides

For weekly order and conditional display rules, use
[ANNOUNCEMENT_DECK_GUIDE.md](../../docs/ANNOUNCEMENT_DECK_GUIDE.md).

Evergreen content is used across courses or across more than one week. Content for a single
lecture belongs with that lecture, including its repeated procedure slides.

Keep content shared across courses in [../../evergreen/](../../evergreen/), including the YouTube
channel and spring registration. Genetics announcements include those groups using
`repo:evergreen/youtube_channel.djot` and `repo:evergreen/spring_registration.djot`.

Course-specific announcements reference the sources below with `=== include: repo:genetics/evergreen/<name>.djot`.
Each weekly master controls visibility with its include's `hidden: true` or `hidden: false`.

- `course_information.djot`: contact information, textbook, course links, and grading explanations.
- `assessment_policies.djot`: technical difficulties and illness policies.
- `quiz_guidance.djot`: quiz rules and grade guidance; show when a quiz is this week or next week.
- `exam_guidance.djot`: exam rules, what to bring, and reviewing old quiz answers.
- `first_week_assignments.djot`: Student Profile and Discord signup credit; show through September 21 in fall or February 14 in spring, then hide.
- `course_evaluations.djot`: evaluation instructions and final-exam extra-time information; hide until needed.

Use three main sections: Informational Slides, Course Content, and General Announcements.
Title, agenda, a dated Next Week lookahead, weather, and icebreaker precede them. The shared course-information group starts
Course Content before the textbook; assessment and assignment groups use subsection dividers.

Keep the weekly agenda, chosen icebreaker, selected podcast, assessment schedule colors, and dated
exam/homework details in the announcement master. Refresh deadlines before showing seasonal slides.
Shared figures live in `assets/` and use explicit repository-relative image paths.

See [HUMAN_GUIDANCE.md](../../docs/HUMAN_GUIDANCE.md) and
[DJOT_SLIDE_SYNTAX.md](../../docs/DJOT_SLIDE_SYNTAX.md) for the content and include contracts.

- `three_point_testcross_steps.djot`: the six-step pairwise mapping roadmap, repeated before full problems.
  Active LECT08F now follows the six-step pairwise method; its textbook predecessor is retired.
