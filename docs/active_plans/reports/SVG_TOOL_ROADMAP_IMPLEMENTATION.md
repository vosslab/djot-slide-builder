# SVG tool roadmap implementation

Date: 2026-11-13. Status: documentation and visual draft ready for independent review;
completion depends on specification, quality, and integration reviews coordinated by the lead.

## Outcome and boundaries

Deliver a ranked roadmap of reusable SVG drawing parts from current Genetics, Biotechnology,
and Biostatistics slides. The user selected the roadmap first and drawing parts over complete
figures. Biotechnology LECT11 is excluded. No drawing tools, APIs, slides, existing artwork,
or question generators are changed. A pilot and a full API specification are outside this work.

## Tasks and owners

| Task | Owner | Status |
| --- | --- | --- |
| Survey live SVG geometry and Djot use; rank candidates | Documentation owner | Draft complete |
| Write roadmap, README link, and changelog entry | Documentation owner | Draft complete |
| Prepare contact overview from existing illustrations | Visual owner | Draft complete; revised ELISA panel requested |
| Review specification, quality, and integration | Lead and independent reviewers | Pending |
| Resolve review findings and record closure | Lead and assigned owners | Pending |

## Decisions and evidence

- Rank gels and pedigree parts first; ELISA wells and Punnett grids next. Defer cells and
  circular maps because their reusable boundaries need more evidence.
- Reuse existing chromosome, gene-track, equipment, and tetrad work. BPQ references are
  repository-relative code paths; related HTML/Pillow output is not an SVG component.
- Preserve local biological color identity independently of course hue. Existing reference
  art can retain legacy fonts; future normal SVG text uses Atkinson Hyperlegible Next.
- [SVG_TOOL_ROADMAP.md](../../SVG_TOOL_ROADMAP.md) links current source SVGs and their Djot
  consumers. Its contact overview is an index to existing figures, not generated tool output.
- The `drawing.text` Arial default is identified as a future prerequisite only; this work
  does not change code or start a font-repair project.

## Checks and limits

The documentation owner checked the cited SVG and Djot paths and reviewed the relevant BPQ
renderer boundaries. The lead must record final review results and any additional checks here.
No LibreOffice export, slide build, or test campaign was requested for this documentation-only
work. Existing reference illustrations have not undergone a new license or font audit.
