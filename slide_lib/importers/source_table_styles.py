"""Project supported native ODF table properties into authoring attributes."""

# Standard Library
import re

# Local Modules
import slide_lib.importers.odf_text as odf_text
import slide_lib.importers.odp_geometry as odp_geometry
import slide_lib.importers.source_model as source_model


COLOR = re.compile(r"#[0-9a-fA-F]{6}")
BORDER = re.compile(r"(\S+)\s+(solid|dashed|dotted)\s+(#[0-9a-fA-F]{6})")


def attribute_text(attributes: dict[str, str]) -> str:
	"""Encode validated table authoring values at the final Djot boundary."""
	# ASVS 1.1.2: source properties become syntax only after allow-list validation.
	result = " ".join(f'{name}="{value}"' if " " in value else f"{name}={value}"
		for name, value in attributes.items())
	return result


def length_points(value: str) -> str:
	"""Normalize a source physical length, including zero padding, to points."""
	matched = odp_geometry.LENGTH_VALUE.fullmatch(value)
	if matched is not None and float(matched.group(1)) == 0:
		return "0pt"
	points = odp_geometry.parse_length(value, field_name="table cell length", allow_negative=False)
	return f"{points:.6g}pt"


def cell_attributes(cell: source_model.SourceTableCell) -> tuple[dict[str, str], str | None]:
	"""Return validated native authoring attributes and an explicit support limit."""
	properties = dict(cell.properties)
	attributes: dict[str, str] = {}
	if cell.column_span > 1:
		attributes["colspan"] = str(cell.column_span)
	fill = properties.get(odf_text.qname("draw", "fill"))
	if fill not in {None, "none", "solid"}:
		return attributes, f"source table fill {fill} requires reconstruction"
	background = None
	if fill != "none":
		# Native Impress cells use drawing color even when draw:fill is omitted.
		background = properties.get(odf_text.qname("draw", "fill-color"),
			properties.get(odf_text.qname("fo", "background-color")))
	if background is not None and background != "transparent":
		if COLOR.fullmatch(background) is None:
			return attributes, "source table background is not a supported solid color"
		attributes["background-color"] = background.upper()
	alignment = properties.get(odf_text.qname("fo", "text-align"))
	if alignment is not None:
		alignment = {"start": "left", "end": "right"}.get(alignment, alignment)
		if alignment not in {"left", "center", "right"}:
			return attributes, f"source table alignment {alignment} requires reconstruction"
		attributes["text-align"] = alignment
	vertical = properties.get(odf_text.qname("draw", "textarea-vertical-align"),
		properties.get(odf_text.qname("style", "vertical-align")))
	if vertical is not None:
		if vertical not in {"top", "middle", "bottom"}:
			return attributes, f"source table vertical alignment {vertical} requires reconstruction"
		attributes["vertical-align"] = vertical
	for name in ("border", "border-top", "border-right", "border-bottom", "border-left"):
		value = properties.get(odf_text.qname("fo", name))
		if value is None:
			continue
		if value == "none":
			attributes[name] = value
			continue
		matched = BORDER.fullmatch(value)
		if matched is None:
			return attributes, f"source table {name} is not a supported border"
		width, pattern, color = matched.groups()
		attributes[name] = f"{length_points(width)} {pattern} {color.upper()}"
	for name in ("padding", "padding-top", "padding-right", "padding-bottom", "padding-left"):
		value = properties.get(odf_text.qname("fo", name))
		if value is not None:
			attributes[name] = length_points(value)
	# Keep equal side values concise without changing any resolved source property.
	for name in ("border", "padding"):
		sides = tuple(f"{name}-{side}" for side in ("top", "right", "bottom", "left"))
		if all(side in attributes for side in sides) and len({attributes[side] for side in sides}) == 1:
			attributes[name] = attributes[sides[0]]
			for side in sides:
				del attributes[side]
		if name in attributes:
			for side in sides:
				if attributes.get(side) == attributes[name]:
					del attributes[side]
	return attributes, None
