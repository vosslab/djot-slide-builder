"""Focused behavior for multiple-choice source-region overlays."""

# PIP3 modules
import pytest

# local repo modules
import slide_lib.importers.geometry as geometry
import slide_lib.importers.slide_plan as slide_plan
import slide_lib.importers.source_regions as source_regions


#============================================
@pytest.mark.parametrize("visuals", [
	(source_regions.SourceImageRegion(
		"source-connector-9", geometry.NormalizedBounds(0.01, 0.01, 0.05, 0.05), "connector", 9,
	),),
	(
		source_regions.SourceImageRegion(
			"assets/figure.png", geometry.NormalizedBounds(0.30, 0.22, 0.70, 0.32), "picture", 10,
		),
		source_regions.SourceImageRegion(
			"source-connector-11", geometry.NormalizedBounds(0.01, 0.01, 0.05, 0.05), "connector", 11,
		),
	),
])
def test_multiple_choice_declines_unconsumed_connector_visuals(
	visuals: tuple[source_regions.SourceImageRegion, ...],
) -> None:
	"""Connector visuals never disappear behind a recognized structural question."""
	question = source_regions.SourceTextRegion(
		((0, "Prompt"), (1, "Choice one")),
		geometry.NormalizedBounds(0.08, 0.20, 0.82, 0.68), False, 1.0, source_ordinal=4,
	)
	answer = source_regions.SourceTextRegion(
		((0, "Answer"),), geometry.NormalizedBounds(0.72, 0.78, 0.92, 0.86),
		False, 0.0, source_ordinal=8,
	)

	assert slide_plan.plan_slide((question, answer), visuals).multiple_choice is None
