# SlideSonnet review

- Local snapshot: `OTHER_REPOS/slideSonnet`
- Upstream: [slideSonnet](https://github.com/avivz/slideSonnet)
- Content type: Narrated slide-video toolkit and editor
- License found: MIT
- Python requirement: 3.13 or newer
- Recommendation: Future companion ideas only

## What it contains

SlideSonnet combines a PDF deck with a narration sidecar, text-to-speech, cached audio, subtitles,
transitions, and video assembly. A NiceGUI editor supports narration work. Its design includes
stable page IDs embedded in PDF markers, page-ID deduplication, diagnostics, content hashing,
audio-file naming, subtitle splitting, timelines, and PDF rendering.

## Reuse assessment

- Ideas: Stable slide identity, content-hash caching, pronunciation-aware narration, SRT or VTT
  output, and preflight diagnostics could support remote teaching.
- Code and functions: MIT permits reuse with notice, but the package requires Python 3.13 while
  this repository is fixed at 3.12. It also brings NiceGUI, TTS services, ffmpeg, and broad media
  dependencies.
- Source ownership: Its PDF plus sidecar model risks making a frozen output a second authority.
  imported presenter notes already provide a narration source here.
- Themes and assets: It does not improve the local theme or import pipeline.

## Decision

Do not integrate it into the slide build. If narrated video becomes a goal, create a separate
companion lane and first decide whether imported notes or a sidecar owns narration so the two cannot
drift.
