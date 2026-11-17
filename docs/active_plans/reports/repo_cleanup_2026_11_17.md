# Repository cleanup audit

The request covered independent code review, pruning repository-owned tests, preserving
the ASCII requirement, and passing `source source_me.sh && pytest tests/`.
The baseline was 9,380 passed and 133 failed.

## Independent review passes

All six passes completed with fresh reviewers. Each reported findings.

| Pass | Concrete findings | Resolution |
| --- | --- | --- |
| Plan | Failing acceptance checks, executable alignment, support-directory imports | Repair the sources and entrypoints; run the complete requested suite. |
| Test | Fragile artwork checks, serialized coordinates, arbitrary size thresholds, duplicate cases | Prune the low-value checks while retaining distinct behavioral protection. |
| Style | Import grouping, source annotations, verification gaps | Correct grouping and annotations; retain temporary regeneration and visual evidence. |
| Docs | Links to ignored local outputs and stale lecture paths | Link maintained sources; describe local exports as code paths; repair current source links. |
| Legacy | Orphaned output and test machinery | Retire the unused output and low-value test modules; preserve the referenced rescue material. |
| Comment | Missing function separators/docstrings and misleading import headings | Add concise descriptions where needed and align the import sections. |

Reviewers also consulted older work plans. The latest explicit human instructions and
[REPO_STYLE.md](../../REPO_STYLE.md) determine the current scope. The positive-prompting
entry in human guidance records an explicit human request.

## Cleanup performed

- Use the existing safe XML parser for parsing and retain standard ElementTree builders,
  namespace registration and serialization.
- Correct source annotations, indentation, entrypoint permissions and support-directory
  import violations. Call standalone generators through their entrypoints.
- Preserve teaching content while replacing unsupported source characters with ASCII text
  or character references. The encoding checks remain active.
- Correct invalid documentation links and the biotechnology cover metadata. Review collections
  and illustration galleries keep their purpose-specific introductions; lecture covers retain
  their authoring checks.
- Prune one-time artwork checks, tuning matrices, serialized geometry snapshots and duplicate
  layout cases. Preserve mathematical geometry, chromosome identity and replication conservation,
  XML safety, editable export, fonts, source containment, atomic output and authoring contracts.

## Verification

- `source source_me.sh && pytest tests/`: 9,281 passed.
- Pruning reduced repository-owned test/support modules from 64 to 54 and test functions
  from 313 to 240. The owned suite shrank from 7,606 to 6,044 lines. Shared support still
  has active consumers; the vendored hygiene checks remain in place.
- The full prototype regeneration succeeds. All 68 review assets are byte-identical to the
  cleanup baseline, and all 1,040 original lecture SVGs retain their hashes.
- ASCII, source-format, link, security, authoring and executable checks pass with the full suite.
- The bytecode-cache directory scan is empty.

The removed tests mainly maintained fixed artwork, font/layout tuning, serialized paths and
mocked implementation arrangements. The retained tests protect data and scientific invariants,
input boundaries, native output, font embedding, source preservation and explicit repository rules.

The permanent E2E lanes remain separate from the base suite. Removed artwork/layout checks
increase the importance of rendered review when changing those illustrations; they did not
establish actual LibreOffice rendering correctness.
