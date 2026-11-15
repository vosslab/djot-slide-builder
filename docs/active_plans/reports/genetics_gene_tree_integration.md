# Genetics gene-tree refresh: final integration review

Status: **PASS**, November 14, 2026, after independent verification of the documentation link
correction below. The instructional implementation and native outputs passed the scoped checks below. The independent
fresh specification, specification delta, and quality reviews pass; the final C quality review
supersedes the earlier C failure. This is not approval of every inherited chromosome or E page.

## Resolved documentation finding

The initial integration verdict failed because [exemplars/README.md:423](../../../exemplars/README.md#L423)
linked and named a retired C fragment. The label, link, and displayed path now identify the
[archived original](../../archive/genetics_gene_tree_svg/sources/original/lect12c_more_gene_trees_part_01.djot.txt),
which preserves the historical 2025 matrix's identity. The target exists, and a fresh check found
no missing local README link targets; the README is ASCII. No deck build was needed for this
documentation fix. The mechanism link in `docs/SVG_TOOL_ROADMAP.md` resolved in the initial review.

## Integration evidence

- The [approved plan](../active/genetics_gene_tree_refresh_plan.md), fresh
  [specification review](genetics_gene_tree_spec_review.md), [C delta](genetics_gene_tree_spec_delta.md),
  [A/B quality review](genetics_gene_tree_quality_ab.md), [C/D quality review](genetics_gene_tree_quality_cd.md)
  and [final C quality review](genetics_gene_tree_quality_c_final.md) cover the calendar, agenda,
  instructional sequence, mathematical content and visual acceptance. The individual quality reviews
  inspected all 173 current pages of 11A-D and 12A; their hashes match current PDFs below. Remaining
  E and chromosome pages were sampled, not fully reviewed.
- Reconciled all 323 entries of the [migration manifest](genetics_lecture_11_12_renumber.json):
  310 match the recorded post-migration hashes, nine are intentional authored source or documentation
  edits, and four are the intentionally retired B/C fragments. All 286 recorded original media files
  exist and match their before hashes; this verifies manifest coverage, not an independently exhaustive
  pre-migration inventory. Original source fragments were archived. The six-gene worksheet values
  are independently checked in the math report and focused test; the recorded original media matches.
- The initial search of external Markdown links targeting these lecture folders found the one broken
  link resolved above. Strict native lint resolves the masters' current included sources and image references. Old
  2025 input names remain provenance paths where applicable; their recorded bytes match.
- All ten canonical master stems have both root `output/odp/` and `output/pdf/` artifacts. XML
  inspection shows B/C/D have 7/12/11 native tables, 112/264/288 native cells, and 7/5/6 embedded
  SVG files. All 15 current generated example SVGs are embedded byte-for-byte in their matching
  ODPs. PDFs contain extractable text; normalized `REPLACE\s*ME` searches found zero in B-D.
  Native object inspection does not establish interactive editing in Impress.
- The final frozen C source hashes and the unchanged four/six generated fragments, data, and 15 SVG
  hashes all verify. The local recipe and JSON supply the generated content; the
  [math report](genetics_gene_tree_math.md) records BPQ topology provenance, all original-pair
  averages, merge heights, child branches, fitted-versus-raw limits, and independent calculations.
  The independent SciPy check rerun here agrees on all 12 joins and root-to-tip checks. Four is
  ultrametric; five and six are not.
- Current recipe and focused test are ASCII; their shebangs and executable bits are consistent.
  Pyflakes reported no findings for either file. No unnecessary framework or full base-suite test
  was introduced for this check.

## Commands and results

From the repository root, using the prescribed direct Python lane:

```sh
PYTHONPATH="$PWD" MPLCONFIGDIR="$PWD/_temp/mplconfig" /opt/homebrew/bin/python3.12 -B deck_tools.py lint --require-native --native-executable /Users/vosslab/.cargo/bin/jotdown genetics/LECT11/djot genetics/LECT12/djot
PYTHONPATH="$PWD:$PWD/tests" MPLCONFIGDIR="$PWD/_temp/mplconfig" /opt/homebrew/bin/python3.12 -B -m pytest --noconftest tests/test_table_styles.py tests/test_layout_tables.py tests/test_gene_tree_examples.py -q
/opt/homebrew/bin/python3.12 -B _temp/gene_tree_refresh/verify_math.py
shasum -a 256 -c _temp/gene_tree_refresh/c_inputs_source_frozen.sha256
shasum -a 256 -c _temp/gene_tree_refresh/c_inputs_immutable_before.sha256
/opt/homebrew/bin/python3.12 -B -m pyflakes genetics/LECT11/djot/gene_tree_examples.py tests/test_gene_tree_examples.py
```

Native lint passed 10 masters, 498 slides and 208 images; 46 focused tests passed; math, hash and
pyflakes checks passed. A direct Python audit hashed the ledger and outputs, inspected ODP ZIP/XML
native objects and SVG bytes, and extracted PDF text and replacement markers. The ten ODP/PDF
exports were produced previously with actual LibreOffice outside the sandbox; no export was rerun
for this review.

After the README correction, a fresh direct Python check verified the archive target and local
README links and rehashed all 20 ODP/PDF artifacts against the table below. Both frozen-input hash
lists were also rechecked: the C sources, four- and six-gene fragments, data, and all 15 SVGs
matched. These checks did not repeat the tests, visual reviews, or LibreOffice exports.

## Current artifacts

SHA-256 values identify the files inspected; PDF page counts reflect visible pages.

| Stem | Pages | ODP SHA-256 | PDF SHA-256 |
| --- | ---: | --- | --- |
| lect11a-2026_announcements | 34 | fe67859d2fdea13848bd89465748cd1c2238a5d2969bbeec1a2e674dfb765984 | b72ec23ece5c6ec0d77ec560d468776002f248c0dd035e05db9acc54c2154909 |
| lect11b-gene_trees | 36 | 90eafc39a944b188da83e6d1d7f256134f073c8e0cbb202ee20490cb7bad5b9d | e13e33fbc4dbf3a44552a017426b4478be8b0b33a66f22ce050ea956cafa2717 |
| lect11c-more_gene_trees | 34 | e5860d68b9470b1bf3042e62ab340468d4a3ccc044128189dbbd3df1c29aac23 | d5e0dd36e0f2abf106e7d612572faa4a754881f75e2553a79b9784fcaeb068d6 |
| lect11d-gene_tree_activity | 32 | eb455a3572fb191e552d48d2470986ce6cac18223bf4737104e6aed0f4365b01 | 606e8b24b39075f8f1bd586f7dd6340fbcc4f4509b3a6c3f9ba493e9ce52d46d |
| lect11e-evol_time | 19 | 77e1a3e6b7ecc127cbc4515e0fc7748748867cb5e96847d981dfbc54ca0601ec | 2e88e420f13f9382442121365ee96a9aefcfc68bde49aeea56d78cee218aa8d3 |
| lect12a-2026_announcements | 37 | 19fefa993c983cfa2aa61887eaa4f525b281b2375ec44291d94eaf91eae7f96e | de11397858992a03bb3936f34b07c0131fd2d468bcada5de6a24c1d15b24b6f6 |
| lect12b-polyploidy | 48 | fe2a1a2612b80e6bbcc3dd09e2527e7c7bcce8b1b5772aafe8f1c89ceb3808e5 | 21438b7f258e04ab033a4c0d0ddafec8d05b94620eee8b4726a9b3d8a4e93465 |
| lect12c-sex_dosage | 69 | a15898b3c71210fae2391902f1650b45c1963a3a29c5888f774ddf925273d305 | 40c85b1dc6fb41ad86d861e61c0e42169572d7a04fe12f68850631430c02132b |
| lect12d-chromo_alter_1-deletions | 112 | 472a98cae4b460cff87dae14eda69c3e0b8fc1be8db5cf1e078d0bf93f0e5051 | 3c543bfc4da0460b2eb46825aed6aedf9c20f3f71a7c01d4eb8562a7d373dc04 |
| lect12e-chromo_alter_2-duplications | 37 | 04e6c5bd662830ff96b44e18e3830a5941b8c4f46efba2b24d97494a28cec8ec | 5504195a38d8b85115c09922239a7fdb824fb882e6f19f169a912f32d3b2a7c7 |

## Remaining boundaries and closeout

E retains three PDF replacement overlays arising from an inherited source marker and other capacity
limitations. Some announcement decks retain evergreen font warnings. Chromosome 12C page 5 has a
large inherited `REPLACE ME` overlay obscuring material; the complete 12C deck is not established
as classroom-ready. Other chromosome replacement markers and limitations are inherited. These
preserve-only issues are outside this refresh and must remain visible in the final report.

Interactive Impress, live Zoom, classroom use and the full base suite including Git-dependent
hygiene were not checked. The closeout owner must replace stale initial counts and pending-review language in the final report,
record accepted reviews and limitations in the progress log, preserve durable evidence, and only
then remove `_temp/gene_tree_refresh/`. These are required project closure steps, not pending deck
implementation or a request for user approval.
