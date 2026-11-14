# SVG toolkit scratch cleanup

Executed after the manager release and final specification review. The exact top-level removal manifest, counts, and protected-tree rollups are in [the JSON report](svg_toolkit_cleanup.json). The earlier snapshot is summarized in [the inventory](svg_toolkit_cleanup_inventory.md).

Removed 664 files, 178 directories, and 56 symlinks (21,019,311 logical bytes). Before and after removal, all 41 regeneration, 42 native proof, and 16 trial hashes matched their durable manifests; both protected Biotechnology tree rollups were unchanged.

The four component PNGs were visually checked against their toolkit examples; `allele_check.svg` identifies the illustrative allele-frequency chart. Shared caches and normal build outputs were retained. Symlinks were removed as links and not followed.

Remaining `_temp` roots: `biotech_lect11`, `biotech_lect11_scope_exclusion`, `matplotlib`, `mplconfig`.
