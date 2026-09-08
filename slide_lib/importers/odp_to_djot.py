"""Convert an imported ODP into supported Djot slide source."""

# Standard Library
import pathlib
import tempfile

# local repo modules
import slide_lib.importers.odp_reader as odp_reader
import slide_lib.importers.pptx_to_djot as pptx_to_djot


#============================================
def convert_odp(
	input_path: pathlib.Path,
	output_path: pathlib.Path,
) -> pptx_to_djot.ConversionSummary:
	"""Convert trusted ODP through a temporary PPTX while retaining visibility."""
	input_path = input_path.resolve()
	output_path = output_path.resolve()
	pptx_to_djot.validate_output_path(output_path)
	imported_slides = odp_reader.read_slides(input_path)
	if not imported_slides:
		raise ValueError("ODP contains no presentation slides")
	hidden_indexes = {slide.source_index for slide in imported_slides if slide.hidden}
	if len(hidden_indexes) == len(imported_slides):
		raise ValueError("ODP contains no visible presentation slides")
	output_path.parent.mkdir(parents=True, exist_ok=True)
	with tempfile.TemporaryDirectory(prefix=".odp_to_djot_", dir=output_path.parent) as name:
		temporary_root = pathlib.Path(name)
		pptx_path = odp_reader.convert_odp_to_pptx(input_path, temporary_root)
		summary = pptx_to_djot.convert_pptx(
			pptx_path,
			output_path,
			expected_slide_count=len(imported_slides),
			expected_hidden=hidden_indexes,
			source_name=input_path.name,
			render_source_path=input_path,
		)
	return summary


#============================================
def run_import(input_file: pathlib.Path, output_file: pathlib.Path | None = None) -> None:
	"""Run one ODP-to-Djot conversion."""
	output_path = input_file.with_suffix(".djot") if output_file is None else output_file
	summary = convert_odp(input_file, output_path)
	print(
		f"Converted {summary.visible_slides} visible slides: "
		f"{summary.editable_slides} editable, {summary.review_slides} layout review, "
		f"{summary.hidden_slides} hidden, {summary.extracted_images} content images"
	)
	print(f"Djot: {summary.output_path}")
	print(f"Import report: {summary.report_path}")
