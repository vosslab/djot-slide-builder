# Lecture 04 conversion

The nine Lecture 04 decks were imported from `genetics/LECT04/` on 2026-09-21 for the
September 22 lecture. The 2026 announcement ODP is the current-year source. Its announcement
content combines current Lecture 03 guidance with recurring Lecture 04 material corroborated by
the 2025 announcement ODP; the 2025 deck remains comparison evidence rather than a canonical
authoring source.

There are 319 authored slides: 289 visible classroom slides and 30 marked `hidden: true`. Normal
exports contain the 289 visible slides. The page references below refer to visible classroom pages.

| Source | Authored | Visible | Hidden | Classroom outputs |
| --- | ---: | ---: | ---: | --- |
| [lect04a-2026_announcements.djot](lect04a-2026_announcements.djot) | 64 | 36 | 28 | `output/{odp,pdf}/lect04a-2026_announcements.*` |
| [lect04b-mendel_history.djot](lect04b-mendel_history.djot) | 29 | 29 | 0 | `output/{odp,pdf}/lect04b-mendel_history.*` |
| [lect04c-two_principles.djot](lect04c-two_principles.djot) | 36 | 35 | 1 | `output/{odp,pdf}/lect04c-two_principles.*` |
| [lect04d-cross_experiments.djot](lect04d-cross_experiments.djot) | 19 | 19 | 0 | `output/{odp,pdf}/lect04d-cross_experiments.*` |
| [lect04e-segregation.djot](lect04e-segregation.djot) | 12 | 12 | 0 | `output/{odp,pdf}/lect04e-segregation.*` |
| [lect04f-punnett_squares.djot](lect04f-punnett_squares.djot) | 47 | 47 | 0 | `output/{odp,pdf}/lect04f-punnett_squares.*` |
| [lect04g-indep_assort.djot](lect04g-indep_assort.djot) | 53 | 52 | 1 | `output/{odp,pdf}/lect04g-indep_assort.*` |
| [lect04h-indep_assort_problems.djot](lect04h-indep_assort_problems.djot) | 37 | 37 | 0 | `output/{odp,pdf}/lect04h-indep_assort_problems.*` |
| [lect04i-big_crossover_problem.djot](lect04i-big_crossover_problem.djot) | 22 | 22 | 0 | `output/{odp,pdf}/lect04i-big_crossover_problem.*` |
| Total | 319 | 289 | 30 | Nine editable ODPs and nine PDFs |

## Content repairs

- The 04A title and agenda use the current September 22, 2026 Chapter 4 context. Current office
  hours, course links, assignment dates, quiz dates, and the Fall 2026 schedule replace obsolete
  credentials and stale dates. The 2025 announcement material supplies recurring course reminders,
  while current-year policy and schedule information remains authoritative.
- Announcement recording, YouTube, and Discord examples use the shared `big-image` layout with
  editable captions. The full informational sequence now follows the polished Biotechnology
  pattern for Zoom, YouTube, Discord, office hours, contact methods, and the anonymous form. The
  current course links are explicit, and hidden source slides remain available for later teaching
  choices.
- Lecture 04B--04I use the standard genetics title-slide and section treatments with the September
  22 date, while preserving source order, source text, figures, tables, and inherited hidden slides.
- Slides that depended on unsupported or missing source objects retain their teaching text and
  source evidence in Djot; no attempt was made to reproduce legacy vector geometry when the native
  layout could express the same teaching relationship more clearly.

## Review boundary

The import reports under `assets/<deck>/import_report.json` record source extraction evidence and
initial review reasons. They do not describe every later teaching-layout repair. Original ODP/PDF
files remain visual evidence; the Djot sources and adjacent assets now own authoring.

The rebuilt outputs have matching visible-page counts for every deck. Strict Jotdown/native lint
and native `--format all` builds passed. The build still emits inherited capacity warnings on dense
legacy slides; successful export is not an attended visual or Impress-click-through acceptance.
The delivery-path PDFs were spot-checked after rendering, but a full page-by-page visual review and
attended answer-reveal test remain outside this conversion record.

Rebuild one deck with the existing command:

```bash
source source_me.sh && python3 deck_tools.py build \
  genetics/LECT04/djot/lect04f-punnett_squares.djot --format all
```
