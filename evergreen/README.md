# Shared evergreen slides

For weekly order and conditional display rules, use
[ANNOUNCEMENT_DECK_GUIDE.md](../docs/ANNOUNCEMENT_DECK_GUIDE.md).

Keep slides used across courses here. Course-specific reusable slides belong in the course's
own `evergreen/` folder; single-lecture content and dated snapshots stay with the lecture.

- [youtube_channel.djot](youtube_channel.djot): Informational Slides divider and channel slide.
  Insert the weekly podcast episode immediately afterward. The channel image is in
  `assets/youtube_channel.png`.
- [natural_science_club.djot](natural_science_club.djot): club subsection and overview. Include
  after evaluations with `hidden: true` until requested.
- [spring_registration.djot](spring_registration.djot): registration divider and original biotech
  advising reminder, with Registrar and Course Finder links, an upcoming-course summary,
  and individual slides for the spring biochemistry lecture/lab, tentative BIOL 301 teaching
  assignment, and summer film course.
  Show roughly October 15 through
  December 1; refresh the spring year each fall.

Include either group from any course with an explicit repository-relative path:

```djot
=== include: repo:evergreen/youtube_channel.djot

=== include: repo:evergreen/spring_registration.djot
hidden: false
```

Set the registration include to `hidden: true` outside its display window. Each weekly master
controls visibility. Place general announcement groups after course-specific announcements,
with registration and evaluations near the end before THE END. Shared fragments inherit the master's course theme and contain no
`color-theme` declaration. Shared images use `repo:evergreen/assets/<filename>`.

The weather and podcast refresh tools are shared utilities; their saved graphics, captions,
and dates stay with the weekly announcement deck.

See [HUMAN_GUIDANCE.md](../docs/HUMAN_GUIDANCE.md) and
[DJOT_SLIDE_SYNTAX.md](../docs/DJOT_SLIDE_SYNTAX.md) for authoring rules.
