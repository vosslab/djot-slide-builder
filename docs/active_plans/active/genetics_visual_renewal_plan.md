# Master plan: Original SVG artwork for lecture decks

## Goal and authority

Create substantially better, original, recognizable and attractive SVG illustrations throughout
the lecture decks, starting with Genetics. Genetics and Biostatistics have priority because the
instructor plans original books for those courses. Biotechnology is lower priority; finish useful
already-started work without expanding its queue.

This is the authoritative scope and execution plan, refreshed November 11, 2026. Existing
implementation approval continues; this refresh introduces no new approval cycle. It governs
older workstream briefs where they differ. The
[genetics_visual_renewal_progress.md](../reports/genetics_visual_renewal_progress.md) records
progress and evidence; historical reviews and exports do not establish acceptance of later art.

## Scope and priorities

- Draw suitable clipart, organisms, apparatus, biological structures and mechanisms, and other
  scientific illustrations. Keep or reuse strong accepted artwork and refine promising work.
- Select images actually used in lectures, including raster artwork inside mixed SVGs, by likely
  visual improvement and drawing difficulty. `@replaceme` status does not determine eligibility.
- Convert pure-text raster images through faithful OCR into editable SVG cards styled like
  blockquotes. Preserve the original wording, errors and voice; retain the source image.
- Check source facts, labels, examples and scientific relationships needed to draw accurately.
  Preserve meaningful counts, identities, data and staged answers while composing original art.
- Use existing inventories, source maps, drawing books and successful examples as resources.
  File counts are accounting, not drawing quotas. Do not restart the M1 inventory campaign.
- Prefer achievable, high-impact work. Retain, defer or skip difficult or ambiguous drawings with
  a brief reason and continue other candidates; do not force weak art to complete a queue.

## Preserve the slide boundary

**The only permitted Djot edits are existing image URL/path substitutions to SVG artwork.** This
includes replacing mixed raster wrappers, reusing accepted art and OCR-to-SVG quote cards.
OCR does not authorize conversion to native Djot blockquotes or prose.

Preserve alt text, titles, body prose, notes, tables, formulas, examples, layouts, dimensions and
other directives, reveals, markers, slide order, hidden states and includes. Fit the artwork to
its existing placement. If it cannot work there, refine the SVG or retain/defer the original;
do not restructure or split slides, resize their frames or migrate native content.

Retain photographs, empirical gels/data and identity images where their appearance is evidence.
Mixed figures are eligible only when their replacement preserves this evidence and the slide
boundary; retain/defer them when a pure-vector replacement cannot do so. Global scientific
revision, curriculum changes and independent native-content conversion are outside this goal.

Human-figure and prenatal drawings are deferred. Preserve the instructor's rejected-art record in
[SVG_REPAIR_BACKLOG.md](../../SVG_REPAIR_BACKLOG.md) and retain original lecture fallbacks.
Gene-tree/phylogeny work is excluded; keep its saved code and archive, and the future BPQ SVG
export task in [TODO.md](../../TODO.md).

## Artwork and deliverables

Apply **Dream big** and **Keep it simple (KISS)** from [REPO_STYLE.md](../../REPO_STYLE.md):
ambitious artwork with small, useful implementation. Simpler workflow does not mean crude art.
Sources establish meaning and teaching purpose, not contours to trace or pixels to match.
Artists may change viewpoint, composition, perspective and style while preserving the science.

Build a flexible visual language from successful illustrations and relevant drawing books. Use
simulated depth, shading, object primitives or flat diagrams when they help the particular
subject. Reuse existing helpers and small useful parts; new toolkits, frameworks, configuration
or tests require a demonstrated need. The provisional
[GENETICS_ILLUSTRATION_GUIDE.md](../../slide-specs/GENETICS_ILLUSTRATION_GUIDE.md) is a resource,
subject to this plan and the instructor's later rejections.

Each finished asset is a static, self-contained, pure-vector SVG with editable geometry and live
text. Use ASCII source with numeric XML entities where needed, a positive `viewBox`, resolved
local references and no external resources. No `<image>` elements, embedded bitmaps or raster
wrappers qualify. Preserve original assets as references/fallbacks; they are not SVG deliveries.
Use quality-90 WebP only for raster previews and review assets.
Do not render publisher copyright notices copied from source images in replacement SVGs.

Use flat, editable Atkinson Hyperlegible Next text and Atkinson Hyperlegible Mono for sequences,
code or aligned text. Reference installed families by name; the Djot pipeline already uses
these fonts. Do not embed fonts per SVG. Add a simple outline only for readability; text gradients
are unnecessary. Keep labels legible at intended size without converting live text to paths.
Use these families regardless of fonts in the source artwork.

## Approach

1. Select one useful candidate from existing work. Inspect its source, current placement and
   relevant reveal states; identify the teaching purpose and the visible improvement to pursue.
   Name the physical asset owner and shared consumers before editing.
2. Create one original SVG, or reuse accepted artwork. Use Astra for artwork and Terra for OCR
   when useful, as requested. For OCR, check transcription against the raster and style the SVG
   quote card without rewriting the words. Keep experiments and previews under root `_temp/`.
3. Render one intended-size preview and complete brief artist and manager review. Check that the
   subject is recognizable, the explanation and labels are clear, and the art visibly improves
   the candidate. Correct consequential drawing issues; avoid automatic rounds of extra reviews.
4. Integrate accepted art through only the necessary image URL/path substitutions, or refine an
   existing SVG in place. Check the scoped source difference and the simple SVG contract. A real
   compatibility, clipping, reveal or frame concern justifies the smallest targeted consumer
   check that resolves it; ordinary full-deck builds remain a separate workflow.
5. Record delivered artwork, exact checks and retained/deferred reasons in the existing ledger
   and relevant workstream brief. Continue approved work autonomously with manager/subagents;
   instructor feedback, playback and printing are optional feedback, not milestone gates.

Follow the runtime boundaries in [HUMAN_GUIDANCE.md](../../HUMAN_GUIDANCE.md): use configured
Python 3.12 directly and filesystem checks; the instructor handles all Git commands, including
indirect invocations. Any necessary LibreOffice command runs outside the sandbox through the
repository scripts. Do not turn a normal art task into repeated baseline/candidate/canonical
full-deck conversions, a full-suite campaign or permanent per-artwork tests.

## File scope

- Course asset folders, initially `genetics/` and then `biostats/`, plus specifically owned
  shared assets: original SVGs and existing authoring scripts where useful. Finish useful started
  Biotechnology work within its existing folders; retain original source assets.
- Existing course `.djot` files: image URL/path substitutions only, with every other byte preserved.
- Existing SVG helpers: only small changes justified by real drawings; preserve their behavior
  and use a focused check for new nontrivial shared logic. No dependency/configuration changes
  are planned.
- Root `_temp/`: experiments, intended-size WebP previews and any targeted consumer evidence.
  Normal build outputs change only when a concrete concern calls for that consumer check.
- Existing ledger, workstream briefs, illustration guide and changelog: concise current results,
  useful drawing guidance and evidence limits. Preserve historical receipts and rejected-art reports.

## Completion checks and references

A delivered drawing has a visible recognition or explanation gain, preserves the necessary
science, fits its unchanged placement and passes brief artist/manager visual review. OCR cards
preserve all original words and errors in live SVG text. Simple XML, ASCII and resource checks
confirm the pure-vector contract; source comparison confirms image-path-only Djot changes.
Resolve demonstrated consumer defects or retain/defer the candidate. Claim only checks actually
performed; standalone rendering does not establish full-deck, classroom or print acceptance.

The broader goal remains open while useful in-scope artwork remains unfinished. Accepted art
and reasoned retained/deferred choices establish coverage; raw file counts and old test/export
receipts do not establish creative completion. Reuse existing records:

- [genetics_visual_workstreams.md](../workstreams/genetics_visual_workstreams.md): current tasks,
  source maps and family briefs under this plan's scope.
- [genetics_visual_renewal_progress.md](../reports/genetics_visual_renewal_progress.md): delivery
  status, checks and remaining work.
- [genetics_illustration_reassessment.md](../reports/genetics_illustration_reassessment.md):
  historical findings and the reasons for the current creative direction.
