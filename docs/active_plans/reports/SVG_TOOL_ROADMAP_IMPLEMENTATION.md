# SVG tool roadmap implementation

Date: 2026-11-13. Status: complete. Specification, quality, and integration reviews passed.

## Settled scope and decisions

The user chose a roadmap first, focused on reusable drawing parts. The complete repository SVG
inventory includes archives, documentation, temporary material, and read-only Biotechnology
LECT11; inclusion is survey scope, not permission to modify it. No tools, API, slide sources,
source SVGs, or question generators are changed. Prior provisional rankings of gels and
pedigrees were rejected because existing work covers them. Format alone does not turn an adapter
into a new subject gap.

Priorities are cells and cell structures, basic explicitly placed flowchart parts, and extending
the existing gene-track helper for oriented features and operon composition. Later candidates
are conditional on real inventory evidence. Labware is already represented by Virtual Lab
assets. Existing projects supply other coverage in SVG, HTML, Pillow, PGML, or canvas.

## Deliverables and ownership

| Work | Owner | Status |
| --- | --- | --- |
| Inventory and category survey | Inventory team | Complete; [CSV](svg_inventory_2026_11_13.csv) is the path-level record. |
| Overview of existing artwork and existing gene-track helper | Visual owner and lead | Complete; lead accepted the preview. |
| [Roadmap](../../SVG_TOOL_ROADMAP.md), helper README, changelog, and this record | Documentation owner | Complete; ready for review. |
| Specification and quality review | `svg_full_survey_spec` and `svg_full_survey_quality` | Passed. |
| Integration and closure | Integration reviewer and lead | Passed; lead accepted the preview. |

## Evidence and method

The 2026-11-13 CSV has 1,039 paths and 1,011 unique SHA-256 hashes, including 28 duplicate
paths in 25 groups. Its SHA-256 is
`e5de1a0e5776e71d59a7c719378ab8943f2559e8ae3a4d77c4fa0654231d29ea`.
It includes 882 vector, 126 mixed and 31 raster-wrapper paths, with embedded images in 157
paths. Scope counts are 965 coursework, 46 archive, 17 documentation examples, 10 temporary,
and one development path. These scopes include Biotechnology LECT11. Each path has a primary
category; the CSV holds category, hash, duplicate, scope, kind, references, tags and review basis.

Four content partitions were audited, with 85 paths reviewed by visual render, 427 by XML
geometry and text, and 527 by source context. Source context is not visual review. There were
zero parse errors and no uncertain category labels. Confirmed visible-object tags occur on 418
paths and are lower bounds from the reviewed subset. Keyword mentions are not visible-object
counts. Identical content can inherit reviewed tags or category without each duplicate being
rendered. References are literal Markdown or Djot matches, not proof of a compiled live use.
Categories establish neither artistic acceptance nor rights. Five blank imports observed in the
review are converter artifacts, not proposed tool needs. The survey is not classroom validation.

The preview combines whole existing mitosis and array-workflow sources, a cropped lysosome detail,
and a demonstration of the existing gene-track helper. Sources and demonstration parameters are
identified in the roadmap; no new source SVG was created or changed. Preview acceptance does not
constitute acceptance of all inventoried images.

Reuse checks cover local chromosome, gene-track, drawing and tetrad helpers; BPQ pedigrees, gels,
Punnett squares, maps, asci, trees, phenotype artwork, membrane motifs, enzymes, sequence and
chemical rendering, and statistics; and Virtual Lab equipment assets and their per-asset
provenance. Virtual Lab's browser renderer is not a general Python SVG API. No flowchart,
exon/intron/operon, or general organelle counterpart was found in inspected Virtual Lab source;
unlabelled static assets were not exhaustively reviewed. The archived enhancer illustration is
not an operon tool. No confirmed native operon component was found in inspected sources.

Future work should retain stable semantic colors and use the project's Next and Mono font roles.
The current `drawing.text` Arial default is a future fix only. No font repair is part of this work.

## Review limits

Independent specification and quality reviewers passed the deliverables. Final integration checked
the roadmap, inventory, preview, helper README, changelog, and local Markdown links. After removal
of nine current-task scratch directories, all 1,039 CSV paths still existed with matching SHA-256
hashes; no additional repository SVG paths were found. The two protected Biotechnology LECT11
temporary directories remain, including the 10 catalogued temporary SVGs. The CSV SHA-256 is
recorded above; the preview SHA-256 is
`e7a26897a9f72160829385c7f2d2a79bb39f3d65d2cbde2408041841700f6847`.

Process deviation: the specification reviewer ran read-only `git status --short` despite the
explicit no-Git instruction and reported no project content edits. Index metadata was not verified.
No LibreOffice export, slide build, full test suite, source-science or licensing audit, or classroom
assessment was performed for this documentation-only roadmap. Category review is not artwork
acceptance.
