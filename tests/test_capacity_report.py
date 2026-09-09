"""Behavior coverage for structured capacity evidence and plain inspection lines."""

import pathlib

import pytest

import slide_lib.capacity_report
import slide_lib.native_model


def diagnostic(path: pathlib.Path, line: int, layout: str, slot: str, required: float | None,
		floor: float, cause: slide_lib.capacity_report.CapacityCause,
		minimum: float | None = None) -> slide_lib.capacity_report.CapacityDiagnostic:
	"""Build one compact source-located capacity specimen."""
	return slide_lib.capacity_report.CapacityDiagnostic(
		slide_lib.native_model.SourceLocation(path, line), layout, slot, required, floor,
		cause, minimum)


#============================================
@pytest.mark.parametrize(("required", "minimum"), ((None, None), (12.0, 1.0)))
def test_capacity_diagnostic_requires_one_recovery_or_physical_representation(
		tmp_path: pathlib.Path, required: float | None, minimum: float | None) -> None:
	"""Malformed diagnostic states fail clearly before they reach terminal reporting."""
	with pytest.raises(ValueError, match="either a required size or a safe minimum"):
		diagnostic(tmp_path / "deck.djot", 3, "one-panel", "body", required, 24,
			slide_lib.capacity_report.CapacityCause.PARAGRAPH_LIST, minimum)


#============================================
def test_plain_lines_preserve_recovered_and_physical_capacity_boundaries(
		tmp_path: pathlib.Path) -> None:
	"""Inspection lines state either a chosen size or the serializer-safe lower bound."""
	path = tmp_path / "genetics" / "djot" / "lecture.djot"
	recovered = diagnostic(path, 42, "two-panels", "left", 19.5, 24,
		slide_lib.capacity_report.CapacityCause.PARAGRAPH_LIST)
	physical = diagnostic(path, 77, "one-panel", "body", None, 24,
		slide_lib.capacity_report.CapacityCause.TABLE, 1)
	assert slide_lib.capacity_report.format_diagnostic(recovered, tmp_path) == (
		"genetics/djot/lecture.djot:42 layout=two-panels slot=left required=19.5pt "
		"floor=24pt cause=paragraph/list")
	assert slide_lib.capacity_report.format_diagnostic(physical, tmp_path) == (
		"genetics/djot/lecture.djot:77 layout=one-panel slot=body required<1pt "
		"floor=24pt minimum=1pt cause=table")


#============================================
def test_sort_and_aggregate_are_stable_across_compilation_order(tmp_path: pathlib.Path) -> None:
	"""The reporting order uses every requested source and concern field."""
	alpha = tmp_path / "djot" / "alpha.djot"
	beta = tmp_path / "djot" / "beta.djot"
	diagnostics = (
		diagnostic(beta, 3, "one-panel", "body", 18, 24,
			slide_lib.capacity_report.CapacityCause.TABLE),
		diagnostic(alpha, 9, "two-panels", "right", None, 24,
			slide_lib.capacity_report.CapacityCause.MIXED_FLOW, 1),
		diagnostic(alpha, 9, "two-panels", "left", 18, 24,
			slide_lib.capacity_report.CapacityCause.PARAGRAPH_LIST),
		diagnostic(alpha, 4, "one-panel", "body", 20, 24,
			slide_lib.capacity_report.CapacityCause.TITLE),
	)
	ordered = slide_lib.capacity_report.sorted_diagnostics(diagnostics, tmp_path)
	assert tuple((item.location.path.name, item.location.line, item.slot, item.cause.value)
		for item in ordered) == (
		("alpha.djot", 4, "body", "title"),
		("alpha.djot", 9, "left", "paragraph/list"),
		("alpha.djot", 9, "right", "mixed-flow"),
		("beta.djot", 3, "body", "table"),
	)
	assert slide_lib.capacity_report.format_summary(ordered) == (
		"Capacity summary: 4 concerns (mixed-flow=1, paragraph/list=1, table=1, title=1)")


#============================================
def test_physical_capacity_error_retains_the_same_structured_event(
		tmp_path: pathlib.Path) -> None:
	"""The exception transports its diagnostic to a corpus inspection caller."""
	location = slide_lib.native_model.SourceLocation(tmp_path / "deck.djot", 11)
	error = slide_lib.capacity_report.PhysicalCapacityError(location, "one-panel", "body", 24,
		slide_lib.capacity_report.CapacityCause.GEOMETRY_SLOT_CONSTRAINT, 1)
	assert error.diagnostic.required_size_pt is None
	assert error.diagnostic.minimum_size_pt == 1
	assert error.diagnostic.cause is slide_lib.capacity_report.CapacityCause.GEOMETRY_SLOT_CONSTRAINT
	assert "one-panel/body cannot fit at the 1 pt serializer-safe minimum" in str(error)
