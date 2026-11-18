# Chromosome gene labels

This is the shared gene-label convention and rendering pipeline for chromosome
illustrations. C28 demonstrates curved chromatids and internal alleles; C53 demonstrates
distinct gene blocks. The evaluation deck is
[chromosome_review.djot](../prototype/chromosome_review.djot).

## What the label identifies

- A gene or allele belongs to a locus on one explicitly identified chromatid. Show a
  contrasting region of chromosome material with its label inside when space permits.
- A haplotype such as `aB` describes two loci. Place `a` and `B` at their separate loci;
  keep a combined haplotype or cell genotype outside as a summary when useful.
- Chromosome numbers, arm names, cell genotypes and product names label whole objects.
  Keep them outside the chromosome, separate from locus labels.
- BPQ texture is decorative. Gene regions, parental ancestry, heterochromatin and
  cytogenetic bands each communicate different information. Preserve their meanings.

## Shared rendering pipeline

1. The lecture recipe supplies gene identity, allele state, source position, chromosome
   ownership and meaningful spacing. Record schematic positions as schematic. A displayed
   gene block's width does not establish the gene's physical size.
2. Use labeled `Segment` values for genes and unlabeled segments for intervening material.
   The ordered `Chromosome` model carries these regions through rearrangements. A deletion
   removes material; it does not replace that material with a differently colored block.
3. Render through `chromosome_path_part()` or the straight/sister wrappers. The shared
   renderer places regions and labels on the final smoothed centerline. It owns text
   measurement, centering, contrast, orientation and allele suffix formatting.
4. For an existing source composition whose loci are separate annotations, use
   `gene_locus_part(name, surface, center, gene)`. Supply the known chromatid's `Surface`
   and arc distance. This adapter uses the same label renderer as the chromosome model.
   Project source coordinates with `nearest_distance(surface.path, source_point)`.
5. Regenerate the prototype, inspect the complete figure at slide size, and inspect its
   native slide export. Confirm allele order and ownership as well as appearance.

Use the existing [chromosomes.py](../svg_tools/chromosomes.py) model and
[chromosome_surface.py](../svg_tools/chromosome_surface.py) geometry. Keep adapters small:
they translate source data into the shared pipeline, rather than drawing their own gene
cards or positioning independent text over the chromosome.

The source-addressed engine uses logical locus IDs and allele labels on retained material.
Both `render()` and `gene_locus_part()` leave at least one cap-length of chromosome body
color between a telomere cap and the inked edge of an internal gene block, measured along
the centerline. `render()` reserves the same clearance beside collars and visible junctions,
and raises `ValueError` when a card cannot fit. Pass `allow_external_genes=True` to allow
external dot-and-leader labels. Check their placement in the complete figure. See
[CHROMOSOME_ENGINE.md](CHROMOSOME_ENGINE.md).

## Label appearance

Keep letters upright on the page while the colored region follows the local chromosome
curve. Use the shared Atkinson font, measured centering and contrasting ink. Preserve
multi-letter gene symbols such as `rb` and `dp`; a trailing `+` or `-` appears as an allele
superscript. Keep source spelling and case.

Reserve room between labels and centromeres, telomeres and neighboring loci. A label
should fit both the region's length and the chromatid's thickness. When a diagram is too
dense, first simplify its composition or consistently widen its schematic rods. Use an
external label with a visible leader to the explicit locus when that improves readability.
Preserve measured scales and biologically meaningful lengths when adjusting a composition.

External gene labels still use the locus anchor; the recipe owns their layout among the
surrounding objects. Repeated coordinates or the nearest chromosome on the page do not
establish locus ownership, particularly at a crossing.

## Minimal model example

```python
import svg_tools.chromosomes as chromosomes
import svg_tools.palette as palette

blue = palette.shade('sky_blue', 'dark')
gene = palette.shade('light_orange', 'light')
model = chromosomes.Chromosome((
	chromosomes.Segment("", blue, 60),
	chromosomes.Segment("rb+", gene, 32),
	chromosomes.Segment("", blue, 108),
))
part = chromosomes.chromosome_path_part(
	"ruby", model, "M0 0 C60 -20 140 20 200 0", thickness=30,
)
```

The lengths are relative arc spans. For source-backed maps, derive them from source
intervals on the final centerline rather than copying this example's schematic lengths.
The API examples and output assembly belong to
[svg_tools/README.md](../svg_tools/README.md#chromosome-drawing-tool); the chromosome body
conventions belong to [SVG_VISUAL_STYLE.md](SVG_VISUAL_STYLE.md#chromosome-family-authority).

## Review checklist

- Each allele remains on its intended chromatid and locus, including through crossings.
- Homologous loci align intentionally; unequal source spacing and changed gene order survive.
- Text is readable at the actual slide size and clear of centromeres and chromosome ends.
- Gene colors remain distinct from source ancestry and biological banding.
- Titles, captions and explanatory prose remain native slide text.

These are visual and biological review criteria. They do not add a separate configuration
system or a snapshot test for each illustration.
