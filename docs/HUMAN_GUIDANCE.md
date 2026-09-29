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

- Add instructor notes to the custom Djot slide format; `@notes` works as the section marker.
- "Be a Visual Storyteller - limit the amount of text - you do the talking, not your slide."
- "Images Are Required: Try to have several pictures on your slide to maintain audience
  attention. You should have some text though."
- "Limit Text: No complete sentences on slides; use short phrases and keywords only."
- "These slides are not for presentation, so the 'instructor does the talking, not the slides' is
  not fully true."
- "Split the 04C protein material into 04C, 04D, 04E, and 04F by chapter; structural biology is a
  chapter I added that is not in the book."
- Keep `set_3` in the filenames; it is the major hierarchy for my content-based slide decks in
  Biotechnology.
- I don't want slide numbers; they make students watch the clock instead of the presenter.
- For Lecture 05D v2, preserve the hard-question opening, the context-dependent addition-rule
  trap, and callbacks to rule slides. Rewrite textbook question screenshots as editable text.
- Put learning objectives on slide 2, a summary at the end, and flow cues in `@notes`.
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
- Prefer pollen/ovule labels for plant examples and sperm/egg labels for animal examples.

## Conversion review

- Preserve source colors and bold key labels in announcements. Anonymous-message instructions
  need the source image; use readable clickable labels instead of broken long URL fragments.
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
