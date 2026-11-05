# Announcement standardization review: October 20, 2026

Applied recent instructor guidance to existing announcement slides. Each retained source
keeps its slide count, order, and hidden flags. The explicit request to delete obsolete
2025 announcement decks is the only deck-removal exception.

- Anonymous-message slides use the cleaned biotech layout, image, wording, and intact URL.
- Graded/Total comparisons use matching blue/magenta emphasis without changing explanations.
- YouTube pages retain a visible channel link and use the existing image-focused layouts.
- Homework tables use Assignment/Due date columns, Week NN labels, compact padded dates,
  and lecture-relative status colors. Existing assignment subparts are retained.
- Exam schedules use item: date with status colors. The published 2026 Genetics schedule
  supplies assessment dates, following explicit instructor approval.
- Cover structures already met the announcement title requirements.
- Newer hide/show rules were not applied retroactively; existing visibility is preserved.

## Structure verification

| Source | Slides | Hidden |
| --- | ---: | ---: |
| `biotech/LECT03/djot/lect03a-2026_announcements.djot` | 39 | 22 |
| `biotech/LECT04/djot/lect04a-2026_announcements.djot` | 18 | 0 |
| `biotech/LECT05/djot/lect05a-2026_biotech_announcements.djot` | 38 | 18 |
| `biotech/LECT06/djot/lect06a-2026_biotech_announcements.djot` | 38 | 16 |
| `biotech/LECT07/djot/lect07a-2026_biotech_announcements.djot` | 35 | 15 |
| `biotech/djot/lect03a-2026_announcements.djot` | 39 | 22 |
| `genetics/LECT03/djot/lect03a-2026_announcements.djot` | 66 | 26 |
| `genetics/LECT04/djot/lect04a-2026_announcements.djot` | 65 | 28 |
| `genetics/LECT05/djot/lect05a-2026_announcements.djot` | 35 | 0 |
| `genetics/LECT06/djot/lect06a-2026_announcements.djot` | 36 | 0 |
| `genetics/LECT07/djot/lect07a-2026_announcements.djot` | 37 | 13 |

## Validation and delivery

All retained sources built through the repository scripts with LibreOffice outside the
sandbox. Changed visible slide families were visually sampled in rendered PDFs.
Existing capacity warnings on unrelated slides remain; this was not a content rewrite.

Genetics and biotech share LECT03/LECT04 output basenames. Separate reviewed copies are in
`output/pdf/genetics/`, `output/pdf/biotech/`, and the corresponding `output/odp/` folders.
The exporter still writes flat default output paths on ordinary future builds; the
course copies here are snapshots from this audit, not a change to exporter behavior.

2025 announcement Djot/ODP/PDF decks were removed, including old directories and generated
outputs. Referenced assets and non-announcement source decks were retained.

## Historical StVC follow-up

The instructor subsequently authorized adding one managed podcast slide after each
YouTube channel page. Other slides and hidden flags remain unchanged, except for the
authorized removal of unused icebreaker agenda entries. The earlier structure table
records the pre-podcast audit.

| Source | Lecture date | Episode | Video ID |
| --- | --- | --- | --- |
| `biotech/LECT03/djot/lect03a-2026_announcements.djot` | 2026-09-17 | StVC 33 | `gNA7VV_AGp0` |
| `biotech/LECT04/djot/lect04a-2026_announcements.djot` | 2026-09-24 | StVC 34 | `_9HjPmVv_MU` |
| `biotech/LECT05/djot/lect05a-2026_biotech_announcements.djot` | 2026-10-01 | StVC 34 | `_9HjPmVv_MU` |
| `biotech/LECT06/djot/lect06a-2026_biotech_announcements.djot` | 2026-10-08 | StVC 35 | `vcB4skacFNw` |
| `biotech/LECT07/djot/lect07a-2026_biotech_announcements.djot` | 2026-10-15 | StVC 36 | `0zhh6g-DJFs` |
| `biotech/djot/lect03a-2026_announcements.djot` | 2026-09-17 | StVC 33 | `gNA7VV_AGp0` |
| `genetics/LECT03/djot/lect03a-2026_announcements.djot` | 2026-09-15 | StVC 32 | `h1qDheNahLs` |
| `genetics/LECT04/djot/lect04a-2026_announcements.djot` | 2026-09-22 | StVC 33 | `gNA7VV_AGp0` |
| `genetics/LECT05/djot/lect05a-2026_announcements.djot` | 2026-09-29 | StVC 34 | `_9HjPmVv_MU` |
| `genetics/LECT06/djot/lect06a-2026_announcements.djot` | 2026-10-06 | StVC 34 | `_9HjPmVv_MU` |
| `genetics/LECT07/djot/lect07a-2026_announcements.djot` | 2026-10-20 | StVC 36 | `0zhh6g-DJFs` |

The 10 current lecture decks rebuilt successfully. All five distinct episode slides
were visually checked. Repeat-refresh checks passed for all 11 sources (including the
legacy duplicate biotech source); two focused tests protect historical selection and
repeatable insertion.
