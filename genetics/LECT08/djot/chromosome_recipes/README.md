# LECT08 chromosome figures

The recipes in this directory rebuild the LECT08 chromosome figures from their adjacent
source data and the shared chromosome drawing tools. From the repository root, regenerate
all sixteen figures in their course asset folders:

```bash
for recipe in genetics/LECT08/djot/chromosome_recipes/*_recipe.py; do
    PYTHONPATH="$PWD" /opt/homebrew/bin/python3.12 -B "$recipe"
done
```

To inspect a recipe's outputs in another directory, pass `--output-root /path/to/output`.
