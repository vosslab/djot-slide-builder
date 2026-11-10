# Gene-tree SVG work archive

This snapshot preserves working drawing code, artwork, and evidence from the withdrawn LECT12
visual renewal. The user excluded all gene-tree work from the current SVG plan. Original LECT12
Djot sources are restored; this archive is future-work material, not approved course delivery.
Historical reports describe the earlier implementation state and do not override that decision.

## What is preserved

- `artwork/`: 46 valid SVGs, including staged trees, two M2 rotation drawings, conceptual gene
  diagrams, and the Adh wrapper with its original embedded empirical pixels. The early B tree
  ending at 17.0 and the withdrawn six-stage version ending at 18.2 are both retained.
- `sources/original/` and `sources/withdrawn/`: exact original and pre-normalization experimental
  versions of the six changed Djot files, stored as `.djot.txt` archival text rather than live
  decks. Their bytes and hashes are unchanged; relative asset links remain as they were in the
  course source directory. Provenance `source` paths retain the historical filenames, while
  `archive` paths name the stored copies.
- `reference_only/`: generator and check source copies, named `.py.txt` to distinguish
  them from supported runnable tools. These include the B, C/D, E, artwork, and M2 rotation work.
  Some scripts copy files into canonical course assets or rewrite canonical Djot. Inspect them
  as text; do not execute them in the repository. Their original paths and hashes are recorded.
- `evidence/`: historical source maps, arithmetic and topology checks, alignment data, decisions,
  handoffs, and compact previews. Reports predate withdrawal unless named `archive_smoke.json`.
- [provenance.json](provenance.json): source and archived hashes and exact restoration records.

SVG copies come from the preserved pre-normalization snapshot. Non-ASCII XML text is encoded as
numeric references where needed, preserving text without introducing invalid HTML named entities.
The source hash identifies the exact earlier bytes; the archive hash identifies the XML-safe copy.
Original assets were not deleted or overwritten. The copied `svg_tools/` backend remained untouched
at the time of this archive; unused copied tools were subsequently removed from the project.

All archived text is ASCII. Two reference scripts use Unicode escapes with identical parsed Python
ASTs; one handoff uses numeric character references. Four CSVs use LF line endings with identical
parsed records. These changes prevent repository hygiene autofixes from invalidating archive
hashes. Original source hashes remain intact; changed archive hashes and reasons are recorded in
[provenance.json](provenance.json). The existing whitespace scan excludes SVGs, whose bytes remain
unchanged.

## Run the preserved example

From the repository root with Python 3.12:

```bash
source source_me.sh
python3 docs/archive/genetics_gene_tree_svg/draw_cd_examples.py
```

[draw_cd_examples.py](draw_cd_examples.py) is a small adaptation of the historical C/D generator,
using the existing `defusedxml` dependency for XML checks. It writes fourteen SVGs only beneath
`_temp/gene_tree_archive_replay/`.
It does not read or rewrite course files, and imports have no drawing side effects. It reproduces
all fourteen archived C/D SVGs byte-for-byte: seven-species reveals, the five-taxon example,
Hartl question/answer, and five activity stages. The models are fixed examples, not a general
phylogenetic inference engine.

Optional preview uses the existing `rsvg-convert` command; no LibreOffice is required:

```bash
rsvg-convert -w 900 _temp/gene_tree_archive_replay/phy_c_five_taxa.drawn.svg \
  -o _temp/gene_tree_archive_replay/five_taxa.png
```

Historical B/E rendering scripts depend on `rsvg-convert`; the original C/D script used CairoSVG.
They also contain session-specific paths and are retained as reference text. The safe replay has
neither dependency. The [five_taxa_replay.webp](evidence/five_taxa_replay.webp) preview shows the
preserved geometry; small internal node letters touch their branches, a known unfinished detail.

## Scientific boundaries

The B original detailed calculation reaches 17.0, while its source overview reaches 18.2 through
a different averaging rule and displayed rounding. The experimental rewrite harmonized the detail
to 18.2; that rewrite is withdrawn. The exact original Djot, early 17.0 drawing, withdrawn 18.2
sequence, and historical arithmetic record remain available. Restoring the original source does
not resolve the inconsistency. See [UPGMA_DECISION.md](evidence/b/UPGMA_DECISION.md) for the earlier
calculation; its historical authorization is superseded by the current exclusion.

The C instructor example uses manual averaging of two current entries and ends at 16.5. Preserve
that made-up-species dataset; it is not standard taxon-count-weighted UPGMA. Seven-species and D
activity trees use their own recorded merge heights. Conceptual gene/allele trees have schematic
lengths. These drawing scripts do not infer arbitrary trees from new distance matrices.

The examined biology-problems HTML tree library has no SVG export. A BPQ SVG export backend remains
future TODO/ROADMAP work; none is implemented or approved here. Historical evidence distinguishes
rendered trials from final slide acceptance and does not establish attended animation, native
edit/save/reopen, or learner validation.

## Verification and remaining work

[archive_smoke.json](evidence/archive_smoke.json) records 46 XML parses, fourteen exact replay
matches, staged-reveal counts, and all 105 baseline LECT12 assets unchanged. The six restored
canonical Djots match their initial baseline hashes exactly and are ASCII. Strict native jotdown
lint passes the four roots: 184 slides, 97 image uses. One replay render was inspected at 900 pixels.
No LibreOffice export or full test suite was run for this archival task.

The 45 task-created canonical SVG duplicates were removed after checking that none existed in
the initial baseline or HEAD and none was referenced in 186 canonical Djots. Forty-four matched
archived bytes; one had equivalent XML with numeric character references. The cleanup removed
44 staged additions and one untracked file, preserving every unrelated index entry. All 105
baseline assets and six restored Djots remain unchanged; all 46 archived SVGs parse, all 90
provenance-recorded payloads retain their hashes, and the fourteen safe replay outputs still
match exactly. [duplicate_cleanup.json](evidence/duplicate_cleanup.json) records each removal
and archive match. No task-created LECT12 SVG duplicates remain. Full local preservation is also
recorded in
`_temp/genetics_visual_renewal/scope_narrowing/INDEX.md`; that temporary snapshot is not needed to
run the safe example or inspect the durable artwork.
