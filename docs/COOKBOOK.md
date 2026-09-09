# Classroom presentation recipes

These recipes combine the command reference in [USAGE.md](USAGE.md) into small teaching workflows.
They keep one extended-Djot deck as the source of truth and treat exported presentations as
replaceable classroom artifacts.

## Revise one lecture

Use this loop when you are changing wording, a question, or a figure in an existing lecture.

1. Edit the `.djot` source. [DJOT_SLIDE_SYNTAX.md](DJOT_SLIDE_SYNTAX.md) defines layout directives
   and the slots each layout supports.
2. Check the deck's structural contract before producing a presentation:

   ```bash
   source source_me.sh && python3 deck_tools.py lint \
     genetics/djot/lect01b-genetic_disorders.djot
   ```

3. Build the editable classroom file you need:

   ```bash
   source source_me.sh && python3 deck_tools.py build \
     genetics/djot/lect01b-genetic_disorders.djot --format odp
   ```

The result is `output/odp/lect01b-genetic_disorders.odp`. A successful lint proves source
structure and image references; it does not prove that a changed visual reads well on a projected
slide. Open the output for that review before class.

## Prepare a course folder

Use this workflow when the full set of decks under a course area needs refreshed editable and PDF
materials.

```bash
source source_me.sh && python3 deck_tools.py lint genetics/djot
./build_slides.sh genetics
```

The first command checks all discovered Djot decks without rendering them. The second writes ODP
and ODP-derived PDF files under `output/odp/` and `output/pdf/`. Check the
PDF for final-state handouts or upload, and retain the Djot files for the next revision rather than
editing an export.

## Migrate a trusted legacy deck

Use import once to begin maintaining an instructor-owned ODP as Djot. Save legacy PPTX as ODP in
LibreOffice first. Pick a new target
name; import refuses to replace an existing Djot file or asset directory.

```bash
source source_me.sh && python3 deck_tools.py visibility genetics/lecture.odp
source source_me.sh && python3 deck_tools.py import genetics/lecture.odp \
  --output genetics/djot/lecture.djot
source source_me.sh && python3 deck_tools.py lint genetics/djot/lecture.djot
```

For an ODP source, visibility reports the resolved visible and hidden slide state before migration.
After import, inspect the new Djot source and its `assets/lecture/` folder, then build and review
the resulting deck. Text, lists, ordinary images, supported tables, and geometry-supported layouts
remain editable. Difficult spatial compositions normalize to standard native source-order panels
and carry review reasons instead of rendered source substitutes. Once reviewed, edit the new Djot
file rather than maintaining parallel source decks.

## Accept source deliberately

Use the strict native-parser gate when deciding that authored Djot is ready for source acceptance:

```bash
source source_me.sh && python3 deck_tools.py lint \
  --require-native --native-executable "$(command -v jotdown)" genetics/djot
```

This gate complements fast structural lint. Native export and a visual LibreOffice review remain
separate acceptance evidence; attended Impress click playback is still an open validation task.
