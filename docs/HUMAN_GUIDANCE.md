# Human guidance

<!-- VENDORED HEADER: START -->
Record the durable guidance Neil Voss states, or approves for preservation here, in his own words:
first person or close paraphrase, one to three lines per bullet. Material he supplies as a source
may inform [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) once it is settled, and an entry of uncertain
origin belongs there too. Rules: [REPO_STYLE.md](REPO_STYLE.md).
[PROPAGATED HEADER - ENTRIES BELOW ARE YOURS]
<!-- VENDORED HEADER: END -->

## Test maintenance

- Treat permanent tests as liabilities as well as assets. Protect intentionally stable, important
  behavior that could regress; prefer contracts over implementation details. When in doubt, remove.
- Keep one-time tests outside the permanent suite and out of Git in `tests/_temp/`. Promote them
  only when the behavior deserves lasting protection.
- Ground gates in actual needs; avoid arbitrary thresholds, exhaustive matrices, and byte or pixel
  equivalence unless the product depends on them.

## Slide-writing advice

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
- Every content deck (B-H) should ideally use: title, learning objectives, optional new jargon
  definitions, opening section heading, teaching content, summary, and a separate THE END.
  Without a vocabulary slide, put the opening section heading on slide 3.
- Use dedicated colors for addition and multiplication throughout Lecture 05 so students can
  associate a color with each rule as a subtle mnemonic.
- Blue and purple are too close in hue. Prefer Chicago Bears blue/orange or Cubs blue/red
  pairings for concepts that students should distinguish.
- Title slide 1 is for orientation: lecture number and letter, title, chapter, Dr. Neil Voss,
  and date. I do not want taglines. Genetics chapters follow the Biology Problems sequence;
  Lecture 05 is Chapter 5.
- Give the title slide's rounded rectangle no fill and place it below the text boxes so I can
  select and copy the text.
- Apply the supplied plain-language advice to science teaching: use simpler words when they
  preserve the meaning, and keep technical terms when they add precision.
- Define jargon new to the lecture sequence in the first few slides of the deck. Check prior
  decks for earlier definitions, as in Lecture 04, before deciding which terms are new.
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
- URLs may be 2 pt smaller than surrounding text as well as condensed. Check rendered slides
  for awkward URL splits, especially Lecture 05A; do not leave isolated letters or large gaps.
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

- Add variety to two-panel image/text slides: sometimes image left/text right, other times
  text left/image right. Alternate when they are back-to-back.
- Biotechnology Lecture 05 builds on Lecture 04, with different slides shown or hidden.
  After Sept 21, Discord signup and Student Profile are no longer active assignments.
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
