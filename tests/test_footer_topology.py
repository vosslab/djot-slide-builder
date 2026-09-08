"""Behavior tests for generic coarse-column and footer topology grouping."""

# PIP3 modules
import pytest

# local repo modules
import slide_lib.importers.djot_emitter as djot_emitter
import slide_lib.importers.geometry as geometry


#============================================
def component(bounds: tuple[float, float, float, float], *, coarse: bool = False,
		source_kind: str = "text", kind: str = "text", reason: str = "", confidence: float = 0.0) -> djot_emitter.EmissionComponent:
	"""Build one concise geometric text component."""
	return djot_emitter.EmissionComponent(
		geometry.NormalizedBounds(*bounds), ("- item",), kind,
		coarse_text_container=coarse, source_kind=source_kind, classification_reason=reason,
		placeholder_confidence=confidence,
	)


#============================================
def test_coarse_columns_and_wide_footer_flow_match_existing_three_cell_layout() -> None:
	"""Two coarse columns plus aligned bottom text become the native footer topology."""
	components = [
		component((0.05, 0.20, 0.42, 0.70), coarse=True),
		component((0.58, 0.20, 0.95, 0.70), coarse=True),
		component((0.05, 0.67, 0.95, 0.75), source_kind="text-box"),
		component((0.05, 0.79, 0.95, 0.87), source_kind="text-box"),
	]

	grouped = djot_emitter.coalesce_bottom_footer(components)

	assert djot_emitter.component_layout(grouped)[0] == "two-over-one-panels"
	assert not djot_emitter.components_overlap(grouped)


#============================================
#============================================
@pytest.mark.parametrize(
	"components",
	[
		[
			component((0.05, 0.20, 0.55, 0.80), coarse=True),
			component((0.65, 0.50, 0.90, 0.69)),
		],
		[
			component((0.05, 0.20, 0.55, 0.80), coarse=True),
			component((0.50, 0.21, 0.75, 0.40)),
		],
	],
)
def test_asymmetric_explanatory_pair_leaves_nonrelations_to_ordinary_matching(
		components: list[djot_emitter.EmissionComponent],
) -> None:
	"""Only direct, separated, aligned one-coarse text pairs enter the local path."""
	assert djot_emitter.asymmetric_explanatory_pair_layout(components) is None


#============================================
def test_wide_lower_component_preserves_top_peer_and_footer_axis_relations() -> None:
	"""A lower span across both peers selects the existing top-and-footer topology."""
	components = [
		component((0.05, 0.20, 0.42, 0.45)),
		component((0.58, 0.20, 0.95, 0.45)),
		component((0.05, 0.58, 0.95, 0.85)),
	]
	near_miss = [*components[:2], component((0.43, 0.58, 0.57, 0.85))]

	assert djot_emitter.component_layout(components)[0] == "two-over-one-panels"
	with pytest.raises(ValueError, match="ambiguous topology"):
		djot_emitter.component_layout(near_miss)
