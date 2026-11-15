# Roadmap: extended-Djot native presentations

Djot is the sole authored source front end to the native editable-object pipeline.
Completed M1-M7 implementation and acceptance records are in
[archive/DONE_TODO.md](archive/DONE_TODO.md#native-presentation-implementation).
The current authoring contract is [slide-specs/DJOT_SLIDE_SYNTAX.md](slide-specs/DJOT_SLIDE_SYNTAX.md).
Small tasks and deferred investigations remain in [TODO.md](TODO.md).

## Remaining verification

- [ ] Attend and record Impress playback for object and top-level-list reveals. The earlier
  attempt stopped at macOS Screen Recording and Accessibility permissions, before slideshow
  control. Record click states; headless ODP round-trip and PDF final-state evidence covers
  separate behavior.
- [ ] Complete the remaining strict-Djot formatter/editor-rule suite selection before claiming
  full compatibility-suite coverage.

## Planned layout extension

- [ ] Build a reusable `two-panels-centered-left` layout for slides that pair a full-height right
  image with a large, unbulleted text block centered both vertically and horizontally in the left
  panel. Keep `two-panels` unchanged for ordinary top-aligned comparison content.
