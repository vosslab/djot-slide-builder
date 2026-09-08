# AI lesson planner review

- Local snapshot: `OTHER_REPOS/ai-lesson-planner`
- Upstream: [ai-lesson-planner](https://github.com/saniales/ai-lesson-planner)
- Content type: Agent prompts, lesson templates, and shell orchestration
- License found: GPLv3
- Recommendation: Reference the planning boundary only

## What it contains

This project organizes a course-planning sequence around specialized agents. The workflow moves
from a course plan through co-teacher and moderator reviews to lesson planning and slide creation.
Its lesson artifacts separate highlights, discourse, and slide material.

The repository is mostly Markdown instructions and templates with shell helpers. It is not a Marp
renderer, importer, or reusable theme library.

## Reuse assessment

- Ideas: Separating learning objectives, instructional discourse, and final slide cues is useful
  for teaching-first authoring. Source-grounded review between stages is also sensible.
- Code and functions: The shell and agent workflow is unnecessary for the current slide pipeline.
- Templates: Its fixed lesson structures are generic and should not become course requirements.
- License: Copying GPL templates or scripts into this MIT repository would add copyleft
  obligations. General workflow ideas can instead be implemented independently.

## Decision

Keep this as a planning reference only. Do not adopt its agents, scripts, prompt files, or fixed
lesson template. Slide conversion and rendering should remain independent of course-planning
automation.
