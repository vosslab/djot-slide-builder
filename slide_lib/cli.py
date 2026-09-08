"""Provide one format-neutral command line for presentation deck workflows."""

# Standard Library
import sys
import pathlib
import argparse
import collections.abc

# Local Modules
import slide_lib.djot_lint
import slide_lib.terminal_output
import slide_lib.importers.odp_to_djot
import slide_lib.importers.odp_visibility
import slide_lib.importers.pptx_to_djot


ImportOperation = collections.abc.Callable[[pathlib.Path, pathlib.Path | None], None]


class CliUsageError(ValueError):
	"""Report a command combination that argparse cannot express directly."""


#============================================
def select_importer(source_suffix: str) -> ImportOperation:
	"""Select the Djot import operation for one imported-deck suffix."""
	importers = {
		".odp": slide_lib.importers.odp_to_djot.run_import,
		".pptx": slide_lib.importers.pptx_to_djot.run_import,
	}
	# ASVS 2.2.1: select import behavior only from the supported suffix allow list.
	if source_suffix.lower() not in importers:
		raise CliUsageError("import source must use the .odp or .pptx extension")
	operation = importers[source_suffix.lower()]
	return operation


#============================================
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
	"""Parse one presentation application command."""
	parser = argparse.ArgumentParser(description=__doc__)
	subparsers = parser.add_subparsers(dest="command", required=True)

	build_parser = subparsers.add_parser("build", help="build one deck or a deck folder")
	build_parser.add_argument("input_path", help="source deck or folder tree")
	build_parser.add_argument("-f", "--format", dest="output_format",
		choices=("all", "pptx", "odp", "pdf"), default="all")

	import_parser = subparsers.add_parser("import", help="import one trusted ODP or PPTX deck")
	import_parser.add_argument("input_file", type=pathlib.Path, help="trusted ODP or PPTX")
	import_parser.add_argument("-o", "--output", dest="output_file", type=pathlib.Path)

	lint_parser = subparsers.add_parser("lint", help="validate extended-Djot source")
	lint_parser.add_argument("sources", nargs="+", type=pathlib.Path,
		help=".djot source or folder")
	lint_parser.add_argument("--native-executable", dest="native_executable",
		help="pinned Djot parser, formatter, or lint executable run once per source")
	lint_parser.add_argument("--native-argument", dest="native_arguments", action="append",
		default=[], help="one fixed argument to pass before each source path; may be repeated")
	lint_parser.add_argument("--require-native", dest="require_native", action="store_true",
		help="fail unless --native-executable names a pinned strict-Djot tool")

	visibility_parser = subparsers.add_parser("visibility",
		help="report resolved ODP slide visibility")
	visibility_parser.add_argument("input_file", type=pathlib.Path, help="trusted imported ODP")

	args = parser.parse_args(argv)
	return args


#============================================
def main(argv: list[str] | None = None) -> int:
	"""Dispatch one parsed command to its reusable application operation."""
	args = parse_args(argv)
	if args.command == "build":
		return slide_lib.terminal_output.run_build(args.input_path, args.output_format)
	if args.command == "import":
		try:
			operation = select_importer(args.input_file.suffix)
		except CliUsageError as error:
			# ASVS 16.5.3: a usage validation failure stops before file processing.
			print(f"error: {error}", file=sys.stderr)
			return 2
		# ASVS 2.2.2 and 5.3.2: trusted importer operations validate file content and paths.
		operation(args.input_file, args.output_file)
		return 0
	if args.command == "lint":
		return slide_lib.djot_lint.run_lint(args.sources, args.native_executable,
			args.native_arguments, args.require_native)
	if args.command == "visibility":
		slide_lib.importers.odp_visibility.run_visibility(args.input_file)
		return 0
	raise RuntimeError(f"unknown command: {args.command}")
