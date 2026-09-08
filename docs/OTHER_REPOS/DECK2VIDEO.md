# Deck2video review

- Local snapshot: `OTHER_REPOS/deck2video`
- Upstream: [deck2video](https://github.com/pjdoland/deck2video)
- Local version: 0.1.0
- Content type: Slide-to-narrated-video Python pipeline
- License found: None
- Recommendation: Ideas only; do not copy code

## What it contains

Deck2video renders Marp or Slidev decks to images, converts presenter notes to speech, and assembles
audio and frames into MP4 output with ffmpeg. It includes pronunciation substitutions and can split
notes around click steps. Relevant functions include `parse_marp`, `split_notes_on_clicks`,
`expand_slides_to_steps`, `render_slides`, and `assemble_video`.

## Reuse assessment

- Ideas: Presenter notes as narration, pronunciation overrides, and frame-aligned audio segments
  could help asynchronous or Zoom-based teaching.
- Code and functions: No license file grants permission to copy the implementation. Its Marp parser
  also splits naively on `---`, which can misread fenced content.
- Themes and assets: It has no theme material needed here.
- Architecture: Text-to-speech and video production should be an optional downstream lane, not
  part of canonical slide building.

## Decision

Do not reuse this repository's code. If narrated output becomes a real requirement, design a
repository-owned companion that reads canonical presenter notes, uses a fence-aware slide model,
and has explicit audio-service and privacy boundaries.
