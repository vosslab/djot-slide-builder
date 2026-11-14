# SVG toolkit audit: style and ownership

## Findings

### Medium: Importing an SVG changes the process-wide XML namespace registry

[svg_tools/svg_import.py:122](../../../svg_tools/svg_import.py#L122) calls `ElementTree.register_namespace` during every `import_svg` call. This changes global serializer behavior for unrelated callers and replaces any existing prefix registered for the XLink namespace. A direct check registered `custom` for XLink, serialized an unrelated element, called `import_svg`, and observed the same element serialize with `xlink` instead. This also conflicts with the implementation report's claim that the corrections do not require global namespace registration ([docs/SVG_TOOLKIT_IMPLEMENTATION_REPORT.md:18](../../SVG_TOOLKIT_IMPLEMENTATION_REPORT.md#L18)). Keep namespace handling local to serialization and remove the process-wide registration; update the report to match the actual solution.

### Medium: Gallery builder leaks working-directory and module state into its caller

[svg_tools/examples/build_gallery.py:45](../../../svg_tools/examples/build_gallery.py#L45) changes the process working directory, and [line 55](../../../svg_tools/examples/build_gallery.py#L55) overwrites the imported curve example's `__file__` without restoring either. Code calling `build()` from Python can subsequently resolve its own relative paths in the wrong directory, and calling the curve example later writes beside the fabricated temporary path. Failures also leave both changes in place. Give the curve recipe an explicit destination as needed and restore the original working directory in a `finally` block, or avoid changing it. This keeps the recipe's output ownership explicit without adding a general framework.

## Evidence and limits

Reviewed the supplied repository guidance, current toolkit modules, example entry points, gallery builder, and command/output guidance. The namespace side effect was reproduced in a direct Python check. This pass did not execute gallery generation or LibreOffice; existing native and regeneration reports were treated as reported evidence, not independently rerun. No additional concrete style finding was identified in the examined dependencies, naming, or command examples. Test adequacy and scientific or visual correctness are outside this pass.
