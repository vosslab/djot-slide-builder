# Temporary-file rescue and cleanup recommendation

Audit date: November 16, 2026. **Rescue complete; original `_temp/` is still intact.**

Recommendation: retain the small collection below and remove the entire original `_temp/`
folder. Its approximately 1.2 GB is mostly review renders, repeated working copies, extracted
images, caches, and test fixtures. You do not need to sort 11,000 loose files manually.

## Start here

- [Browse 12 recovered SVG samples](svg_gallery.html), or
  [view their one-page preview](svg_gallery.webp). Open any sample to edit the original SVG.
  S01-S06 are small demos/specimen sheets; S07-S12 show earlier chromosome styles. They are
  unapproved prototypes and historical drafts, not exemplars.
- [Source-history archive](../../LOCAL_ONLY/temp_source_history_2026_11_16.zip): roughly 25 MB,
  containing one verified copy of 1,496 scratch-only source files, including **all 401 unique
  scratch-only SVG variants**, plus four downloaded reference PDFs. This preserves the long tail
  without leaving another loose-file tree. The archive stays in the existing ignored
  `LOCAL_ONLY/` directory because historical sources can contain protected artwork.
- [Biotechnology drawing generator](biotech_set6_drawings.py): a useful script that otherwise
  existed only in scratch. An isolated run reproduced all ten current Set 6 SVG figures
  byte-for-byte. It writes `biotech/LECT11/djot/assets/set6_drawings/` relative to its working
  directory. The untouched historical script is also inside the archive.
- [Small evidence folder](evidence/): final chromosome acceptance/integration/grouping receipts,
  protected-input notes, and Biotechnology validation/recovery receipts.

## Recovered PDF snapshots

Both `output/pdf/` and `output/odp/` were empty at audit time. These three dated PDF backups were
still in scratch, so they were preserved separately. They are snapshots, not a claim that the
present source still produces identical exports.

| Saved PDF | Pages |
| --- | ---: |
| [Biotechnology 11A announcements](recovered_exports/lect11a-2026_biotech_announcements.pdf) | 41 |
| [Biotechnology 11B group project](recovered_exports/lect11b-2026_group_project.pdf) | 28 |
| [Biotechnology 11C Set 6](recovered_exports/lect11c-set_6_regulation_of_biotechnology.pdf) | 308 |

The new [chromosome corpus collection](../chromosome_review.pdf) is already safe in `prototype/`.

## What can go

| Material in `_temp/` | Finding and recommendation |
| --- | --- |
| Finished SVG copies | 1,477 scratch SVG files exactly match files already elsewhere in the repository. Keep their existing canonical locations. |
| Annual-source image extraction | All 519 extracted Biotechnology images, totaling 218 MB, exactly match members of original ODP/PPTX files already in the repository. Delete the extraction cache. |
| Earlier chromosome variants | The 401 scratch-only SVG contents are preserved in the archive, including rejected and superseded versions. Delete their scattered working copies. |
| Page renders, crops, contact sheets, and old export snapshots | These are derived review material. Keep the selected final receipts and recovered PDFs above; discard the bulk renders and superseded exports. |
| Test trees, font caches, generated math SVGs, and temporary symlinks | Disposable. Math and font caches are recreated as needed. Remove symlinks as links, without following them. |

Existing maintained samples are in the [SVG toolkit guide](../../svg_tools/README.md) and
`docs/slide-specs/illustration_examples/svg_toolkit/`. The temporary curve-placement demo was
already an exact copy of its maintained counterpart; it did not need another rescued copy.

## Verification and limits

- The inventory covers **11,127 regular files** and **900 symlinks**. All regular-file hashes and
  the file set remained unchanged throughout this audit. No original scratch file was deleted.
- Parsed **121 current deck roots and 2,949 image placements**, including course decks,
  exemplars, and the prototype. No included source or placed image resolves into `_temp/`,
  and no image was missing. This is an input check, not a fresh LibreOffice build of all decks.
- Every archived source file was SHA-256 checked after compression; the complete ZIP also passed
  its integrity check. All copied SVG samples and recovered PDFs retain their source bytes.
- The rescued generator passed a real isolated 10-output regeneration comparison.
- No full test suite, live playback, or approval of the rescued art was performed.

Historical reports contain `_temp/...` evidence paths. The archive retains original source paths;
`MANIFEST.csv` inside it and [the full inventory](inventory.csv) map paths to hashes and copies
already elsewhere. [Archive manifest](archive_manifest.csv), [rescue receipt](rescue_receipt.json),
[deck-input check](dependency_check.json), and [original-image check](embedded_source_check.json)
provide the detailed evidence. The original paths are historical provenance after cleanup.

Keep these compact artifacts instead of preserving the whole `_temp/` tree. Removing `_temp/`
would reclaim its approximately 1.2 GB while the retained rescue uses about 33 MB.
