# SVG toolkit scratch cleanup inventory

The original snapshot contained 889 paths: 869 conditional removals, 10 trial paths awaiting promotion, one conditional container, and nine retained paths. The compact [JSON inventory](svg_toolkit_cleanup_inventory.json) preserves the original top-level entries and counts rather than individual pytest descendants.

Cleanup was executed after promotion, independent review, and manager release; later owned review scratch was included. See the [cleanup report](svg_toolkit_cleanup.md) and its JSON manifest for exact top-level removals, counts, and verification. Protected Biotechnology trees, shared caches, durable artifacts, and normal build outputs were retained.
