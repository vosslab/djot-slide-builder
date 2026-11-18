"""Build the chromosome review's additional views of the Mini2 figures."""

# Standard Library
import pathlib

# Local repo modules
import make_chromosome_engine_mini2


#============================================
def build(output_dir: pathlib.Path) -> None:
	"""Write the inversion and gamete views from the shared Mini2 recipes."""
	output_dir.mkdir(parents=True, exist_ok=True)
	# ASVS 5.3.2: Recipe-owned filenames keep output paths independent of figure data.
	make_chromosome_engine_mini2.build_c55(output_dir / 'c55-overview.drawn.svg')
	make_chromosome_engine_mini2.build_c55(output_dir / 'c55-loop.drawn.svg', loop_only=True)
	columns = make_chromosome_engine_mini2.C63_COLUMNS
	make_chromosome_engine_mini2.write_c63_view(
		output_dir / 'c63-left-middle.drawn.svg', 'Adjacent segregation gametes',
		'Adjacent-1 gives 1 + 2 and 3 + 4. Adjacent-2 gives 1 + 3 and 2 + 4. '
		'The pale collars identify each centromere and the white zigzags mark exchanged chromosome tips.',
		columns[:2], column_width=540, scale=8.1, chromatid_width=38)
	make_chromosome_engine_mini2.write_c63_view(
		output_dir / 'c63-right.drawn.svg', 'Alternate segregation gametes',
		'Alternate gives 1 + 4 and 2 + 3. '
		'The pale collars identify each centromere and the white zigzags mark exchanged chromosome tips.',
		columns[2:], column_width=540, scale=8.1, chromatid_width=38)
