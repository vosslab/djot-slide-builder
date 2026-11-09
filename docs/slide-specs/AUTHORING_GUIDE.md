# Slide authoring overview

Use this overview for source organization, typography, layouts, and artifact conventions.
The authoritative subject specifications are:

- [COLOR_GUIDE.md](COLOR_GUIDE.md): concept colors, emphasis, continuity, and reveals.
- [VOICE_GUIDE.md](VOICE_GUIDE.md): student-facing wording and preservation of voice.
- [PEDAGOGY_GUIDE.md](PEDAGOGY_GUIDE.md): teaching structure, methods, and study support.

These specifications consolidate the earlier slide style and teaching-methods guides.
Their examples apply across Genetics, Biotechnology, Biochemistry, and other science courses.

## Authority and evidence

Apply the instructor's current request first, then explicit recorded preferences in
[../HUMAN_GUIDANCE.md](../HUMAN_GUIDANCE.md). The specifications are the working authority for their
subjects; this overview routes authors to them and retains presentation conventions.

When consolidating or extending guidance, distinguish the evidence:

| Evidence | How to use it |
| --- | --- |
| Explicit preference | Preserve its scope, exceptions, and strength. A scoped approval is not general permission. |
| Established convention | Corroborate it with recorded guidance, a settled decision, or identified instructor-cleaned material. |
| Observed habit | Treat it as an example to investigate, not automatically a requirement. |
| Inherited recommendation | Retain useful methods as recommendations; do not attribute them to the instructor without evidence. |
| Supplementary BPQ or research idea | Adapt when compatible and label a new suggestion clearly. |

Prefer instructor-authored originals and instructor-cleaned decks when selecting examples.
A provisional import or generated expansion does not establish instructor approval merely by
being recent. Repetition can suggest a habit; it does not by itself prove intention.

Investigate conflicts before replacing guidance. Use explicit corrections and their context to
resolve them. Keep an unresolved proposal identified as a proposal while retaining established
behavior. Preserve useful explanations and exceptions when moving rules, not just their titles.
Keep "prefer," "usually," and "when useful" distinct from requirements and keep approximate
targets approximate.

The specifications distinguish conversion from new authoring. Improving documentation does not
authorize rewriting slides, adding new scientific content, splitting source slides, or changing
the teaching sequence. Use [../SLIDE_CONVERSION_CHECKLIST.md](../SLIDE_CONVERSION_CHECKLIST.md) for
conversion and [../TALKING_POINT_DECK_RECIPE.md](../TALKING_POINT_DECK_RECIPE.md) for an authorized
annual-source merge.

## Source organization

Maintain canonical Djot with reachable local assets. ODP and PDF are generated delivery artifacts.
Keep large lectures divided into their established decks and cohesive chapter files; use includes
instead of duplicate shared slides. Do not merge decks solely for tidiness.
Keep visible slide-number footers off the slides, following the instructor's recorded preference.
[DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md) owns includes, layouts, slots, tables, and notes.

Content-deck bookends and their teaching purpose are specified in
[PEDAGOGY_GUIDE.md](PEDAGOGY_GUIDE.md#give-each-deck-a-structure).
Weekly announcements follow [ANNOUNCEMENT_DECK_GUIDE.md](ANNOUNCEMENT_DECK_GUIDE.md).

## Cover and layout conventions

Keep the lecture number and letter above the title metadata. Use the intended teaching date and
the current course's chapter sequence; verify a known chapter rather than deriving it from the
lecture number. Do not invent a chapter to fill the field.

- Unknown chapter: topic, instructor, and date on separate metadata lines.
- Known chapter: topic and chapter on separate lines, or `Chapter ##: Topic` on one metadata line,
  then instructor and date.
- Announcements: the topic is exactly `Announcements`, followed by instructor and date;
  announcements never have chapters.
- Keep taglines and vertical-bar separators off covers.

For example, a known-chapter cover can have these separate lines: Lecture 05D, Probability
Concepts, Chapter 5, Dr. Neil Voss, and Sept 29, 2026. This illustrates the format, not a rule that
every deck needs five fields. The detailed authority is [../HUMAN_GUIDANCE.md](../HUMAN_GUIDANCE.md#slide-1-title-slide).

Use supported layouts for recurring jobs. The shared `bookend` layout serves Learning Objectives
and Key Takeaways; `definitions` gives terms a recognizable frame. Keep their thin angular frames,
opposite-corner symmetry, and light/dark accents in the selected course hue. Section/subsection
hierarchy and backgrounds follow the course theme. The `reference` layout supplies its gray
outline and later-study footer, described in [PEDAGOGY_GUIDE.md](PEDAGOGY_GUIDE.md#keep-explanations-visible).

## Typography and visible URLs

The backend owns font-family selection. Use semantic formatting in Djot rather than font-name
overrides. Its established roles are:

- Atkinson Hyperlegible Next for ordinary text, including titles and prompts.
- Atkinson Hyperlegible Mono when fixed-width text helps.
- IBM Plex Sans Condensed for narrow text, including visible URLs.
- Backend-selected supporting fonts for missing glyphs and mathematics.

Use readable type, clear hierarchy, sensible margins, and preserved image proportions.
The visual rubric uses 36 pt titles, 28 pt body text, and a repository-owned readable floor.
Keep essential diagram labels and captions readable at the intended viewing size. Review a slide
at classroom distance or its normal Zoom display size, not only enlarged on the author's screen.

Show complete clickable destinations as visible URLs, with helpful context alongside them.
URLs start 2 pt below surrounding text and can shrink independently down to 12 pt. Move an intact
URL to the next line when needed; flag one still too wide. Preserve the full address and target,
including an explicit link whose display differs from its target. Do not insert spaces, hide
the address behind "Read online," or force ordinary prose to shrink with it.

Resolve crowding within the authorized task. Balance line breaks and preserve instructor wording;
do not treat generic advice to shorten text or split slides as conversion permission.
[VOICE_GUIDE.md](VOICE_GUIDE.md) owns title case, notation, and wording by purpose.

## Editable artifacts and review

Keep titles, body text, tables, links, definitions, and reference text native and selectable.
Place decorative frames behind text with no fill where needed so borders do not obstruct copying.
Equations remain editable in Djot; their MathJax SVG output is an established exception to native
text inside the presentation. Use the figure-plus-labels pipeline for actual figures, keeping
titles, captions, and ordinary prose native.

Use [../COLOR_PALETTE.md](../COLOR_PALETTE.md) for exact palette mappings and
[COLOR_GUIDE.md](COLOR_GUIDE.md) for their meaning.
Use [SLIDE_VISUAL_REVIEW_RUBRIC.md](SLIDE_VISUAL_REVIEW_RUBRIC.md) for advisory rendered review;
source checks do not prove classroom quality, editability, or playback.

Commands and validation lanes are in [../USAGE.md](../USAGE.md) and [../DEVELOPMENT.md](../DEVELOPMENT.md).
Run any command that can invoke LibreOffice outside the sandbox on this macOS host. Keep temporary
source comparisons and review artifacts in root `_temp/`.
