# Shared dated content

Use this folder for dated material that more than one course can include. Put reusable material
without a date-dependent selection in [../evergreen/README.md](../evergreen/README.md).

- `stump_the_vibe_coder/<YouTube ID>.djot` is one editable Stump the Vibe Coder episode slide.
- `assets/stump_the_vibe_coder/<YouTube ID>.webp` is that episode's thumbnail.

Announcement masters include their selected episode explicitly after the YouTube channel slide:

```djot
=== include: repo:shared/stump_the_vibe_coder/<YouTube ID>.djot
```

The explicit include pins each deck to its selected episode. The refresh preview shows the
selected references. With `--write`, it saves the thumbnail, creates the shared Djot file when
absent, and updates the selected master references. Existing curated fragments supply their
captions and links.
