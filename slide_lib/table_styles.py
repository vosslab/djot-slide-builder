"""Validate shared table styles and resolve their native cell formatting."""

import re
import math
import pathlib
import colorsys
import dataclasses

import yaml

import slide_lib.djot_errors
import slide_lib.native_model
import slide_lib.table_formatting
import slide_lib.presentation_theme


SIDES = ("top", "right", "bottom", "left")
AUTHOR_PROPERTIES = frozenset({"background-color", "text-align", "vertical-align", "border", "padding"} |
	{f"{kind}-{side}" for kind in ("border", "padding") for side in SIDES})
REGIONS = ("numeric", "row-header", "header", "total", "matrix-diagonal", "matrix-unused")
_NUMERIC = re.compile(r"[-+\u2013\u2212]?(?:[0-9][0-9,]*(?:\.[0-9]+)?|\.[0-9]+)%?")
_IDENTIFIER = re.compile(r"[a-z][a-z0-9-]*")


@dataclasses.dataclass(frozen=True)
class StyleDefinition:
	"""Validated base values and a closed vocabulary of structural regions."""

	defaults: slide_lib.table_formatting.CellOverrides
	regions: dict[str, slide_lib.table_formatting.CellOverrides]
	row_headings: bool = False
	matrix: str | None = None


@dataclasses.dataclass(frozen=True)
class StyleRegistry:
	"""One compilation's immutable-by-convention shared definitions."""

	styles: dict[str, StyleDefinition]


@dataclasses.dataclass(frozen=True)
class ResolvedTable:
	"""Formatting in semantic row order, retaining actual cells rather than span placeholders."""

	cells: tuple[tuple[slide_lib.table_formatting.CellFormatting, ...], ...]


def _fail(location: slide_lib.native_model.SourceLocation, message: str) -> None:
	"""Give style failures the same source-location contract as Djot parsing."""
	raise slide_lib.djot_errors.source_error(location, message)


def _color(value: object, location: slide_lib.native_model.SourceLocation,
		property_name: str, internal: bool) -> str:
	"""Accept bounded RGB values and the existing palette where permitted."""
	if isinstance(value, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", value):
		return value.upper()
	if isinstance(value, str) and internal and value in (
			*slide_lib.presentation_theme.text_color_names(), "accent-tint"):
		return value
	_fail(location, f"{property_name} requires a six-digit hex color (#RRGGBB)" +
		(" or an existing color role" if internal else ""))
	return ""


def _points(value: object, location: slide_lib.native_model.SourceLocation,
		property_name: str) -> float:
	"""Read a nonnegative finite point dimension without admitting expressions."""
	if not isinstance(value, str) or re.fullmatch(r"(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)pt", value) is None:
		_fail(location, f"{property_name} requires a nonnegative point value such as 4pt")
	result = float(value[:-2])
	if not math.isfinite(result):
		_fail(location, f"{property_name} requires a finite point value")
	return result


def _border(value: object, location: slide_lib.native_model.SourceLocation,
		property_name: str) -> slide_lib.table_formatting.Border:
	"""Validate the published native border shorthand, including explicit absence."""
	if value == "none":
		return slide_lib.table_formatting.Border(0.0, "none", "#000000")
	parts = value.split() if isinstance(value, str) else []
	if len(parts) != 3 or parts[1] not in ("solid", "dashed", "dotted"):
		_fail(location, f"{property_name} requires none or '<width>pt solid|dashed|dotted <color>'")
	width = _points(parts[0], location, property_name)
	if width <= 0:
		_fail(location, f"{property_name} width must be positive; use none for no border")
	color = _color(parts[2], location, property_name, True)
	if color == "accent-tint":
		_fail(location, f"{property_name} requires a hex color or existing text color role")
	result = slide_lib.table_formatting.Border(width, parts[1], color)
	return result


def parse_overrides(properties: dict, location: slide_lib.native_model.SourceLocation,
		internal: bool = False) -> slide_lib.table_formatting.CellOverrides:
	"""Validate CSS-named author properties or the slightly richer shared registry values."""
	# ASVS 2.2.1: allowlisted property names, grammar, and finite dimensions at the source boundary.
	allowed = AUTHOR_PROPERTIES | ({"color", "font-weight"} if internal else set())
	if not isinstance(properties, dict) or any(name not in allowed for name in properties):
		_fail(location, "unsupported table formatting property; use " + ", ".join(sorted(allowed)))
	values: dict = {}
	for name, value in properties.items():
		if name == "background-color":
			values["background_color"] = _color(value, location, name, internal)
		elif name == "color":
			values["text_color"] = _color(value, location, name, True)
		elif name == "font-weight":
			if value not in ("normal", "bold"):
				_fail(location, "font-weight requires normal or bold")
			values["bold"] = value == "bold"
		elif name in ("text-align", "vertical-align"):
			options = ("left", "center", "right") if name == "text-align" else ("top", "middle", "bottom")
			if value not in options:
				_fail(location, f"{name} requires " + ", ".join(options))
			values["text_alignment" if name == "text-align" else "vertical_alignment"] = value
	# Expand shorthands first, so specific sides win independently of attribute order.
	if "border" in properties:
		border = _border(properties["border"], location, "border")
		values.update({f"border_{side}": border for side in SIDES})
	if "padding" in properties:
		value = properties["padding"]
		parts = value.split() if isinstance(value, str) else []
		if not 1 <= len(parts) <= 4:
			_fail(location, "padding requires one to four point values")
		points = tuple(_points(part, location, "padding") for part in parts)
		indexes = {1: (0, 0, 0, 0), 2: (0, 1, 0, 1), 3: (0, 1, 2, 1), 4: (0, 1, 2, 3)}[len(points)]
		values.update({f"padding_{side}_pt": points[index] for side, index in zip(SIDES, indexes)})
	for side in SIDES:
		if f"border-{side}" in properties:
			values[f"border_{side}"] = _border(properties[f"border-{side}"], location, f"border-{side}")
		if f"padding-{side}" in properties:
			values[f"padding_{side}_pt"] = _points(properties[f"padding-{side}"], location, f"padding-{side}")
	result = slide_lib.table_formatting.CellOverrides(**values)
	return result


class _RegistryLoader(yaml.SafeLoader):
	"""Safe YAML loader that rejects silently overwritten duplicate definitions."""

	def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict:
		keys = [self.construct_object(key, deep=deep) for key, value in node.value]
		if any(not isinstance(key, str) for key in keys) or len(keys) != len(set(keys)):
			raise yaml.constructor.ConstructorError(None, None,
				"table style keys must be unique strings", node.start_mark)
		result = super().construct_mapping(node, deep=deep)
		return result


def load_registry(path: pathlib.Path | None = None) -> StyleRegistry:
	"""Load safe shared definitions once at the compilation's measurement-session boundary."""
	registry_path = path if path is not None else pathlib.Path(__file__).with_suffix(".yaml")
	location = slide_lib.native_model.SourceLocation(registry_path, 1)
	# ASVS 1.5.2: SafeLoader admits data only; duplicate identifiers never silently overwrite styles.
	try:
		loader = _RegistryLoader(registry_path.read_text(encoding="utf-8"))
		try:
			data = loader.get_single_data()
		finally:
			loader.dispose()
	except yaml.YAMLError as error:
		_fail(location, f"invalid table style YAML: {error}")
	if not isinstance(data, dict) or set(data) != {"styles"} or not isinstance(data["styles"], dict):
		_fail(location, "table style YAML requires one styles mapping")
	styles = {}
	for name, definition in data["styles"].items():
		if _IDENTIFIER.fullmatch(name) is None or not isinstance(definition, dict):
			_fail(location, "table style names require lowercase identifiers and mapping definitions")
		if set(definition) - {"defaults", "regions", "row-headings", "matrix"}:
			_fail(location, f"unsupported table style definition property in {name}")
		defaults = parse_overrides(definition.get("defaults", {}), location, internal=True)
		regions = definition.get("regions", {})
		if not isinstance(regions, dict) or any(region not in REGIONS for region in regions):
			_fail(location, f"unknown table style region in {name}")
		parsed_regions = {region: parse_overrides(values, location, internal=True)
			for region, values in regions.items()}
		row_headings = definition.get("row-headings", False)
		matrix = definition.get("matrix")
		if type(row_headings) is not bool or matrix not in (None, "lower", "upper"):
			_fail(location, f"{name}: row-headings requires boolean; matrix requires lower or upper")
		styles[name] = StyleDefinition(defaults, parsed_regions, row_headings, matrix)
	if "standard" not in styles:
		_fail(location, "table style registry requires standard")
	return StyleRegistry(styles)


def _resolved_color(value: str, theme: slide_lib.presentation_theme.PresentationTheme) -> str:
	"""Turn semantic tokens into final RGB before measurement or serialization."""
	if value == "accent-tint":
		rgb = tuple(int(theme.accent_color[index:index + 2], 16) / 255 for index in (0, 2, 4))
		hue, lightness, saturation = colorsys.rgb_to_hls(*rgb)
		tint = colorsys.hls_to_rgb(hue, max(lightness, 0.8), saturation)
		return "".join(f"{round(channel * 255):02X}" for channel in tint)
	result = slide_lib.presentation_theme.resolve_text_color(value, theme.accent_color)
	return result


def _apply(current: slide_lib.table_formatting.CellFormatting,
		overrides: slide_lib.table_formatting.CellOverrides, priority: int,
		theme: slide_lib.presentation_theme.PresentationTheme) -> slide_lib.table_formatting.CellFormatting:
	"""Apply one cascade layer without changing source inline content."""
	values = {}
	for field in dataclasses.fields(overrides):
		value = getattr(overrides, field.name)
		if value is None:
			continue
		if field.name in ("background_color", "text_color"):
			value = _resolved_color(value, theme)
		elif isinstance(value, slide_lib.table_formatting.Border):
			value = dataclasses.replace(value, color=_resolved_color(value.color, theme), priority=priority)
		values[field.name] = value
	result = dataclasses.replace(current, **values)
	return result


def _label(inlines: tuple[slide_lib.native_model.Inline, ...]) -> str:
	"""Read plain labels conservatively through source inline formatting."""
	parts = []
	for inline in inlines:
		if isinstance(inline, (slide_lib.native_model.Text, slide_lib.native_model.InlineCode)):
			parts.append(inline.value)
		elif isinstance(inline, (slide_lib.native_model.Strong, slide_lib.native_model.Emphasis,
				slide_lib.native_model.StyledSpan, slide_lib.native_model.Link)):
			parts.append(_label(inline.children))
		elif isinstance(inline, slide_lib.native_model.Break):
			parts.append("\n")
		else:
			# Equations are not reliably recognized as numeric labels or corresponding axes.
			parts.append("[equation]")
	return "".join(parts).strip()


def _matrix_offset(table: slide_lib.native_model.Table) -> int:
	"""Require unique corresponding labels and one consistent cropped-axis offset."""
	message = "matrix axes are ambiguous; use standard with explicit cell borders for this table"
	rows = [_label(row[0].inlines) for row in table.rows]
	columns = [_label(cell.inlines) for cell in table.headers[1:]]
	all_rows = ((table.headers,) if table.headers else ()) + table.rows
	if not columns or not rows or any(cell.column_span != 1 for row in all_rows for cell in row):
		_fail(table.location, message)
	if any(not label or label == "[equation]" for label in rows + columns) or \
			len(set(rows)) != len(rows) or len(set(columns)) != len(columns):
		_fail(table.location, message)
	offsets = {rows.index(label) - columns.index(label) for label in set(rows) & set(columns)}
	if len(offsets) != 1:
		_fail(table.location, message)
	offset = offsets.pop()
	for row_index, label in enumerate(rows):
		column = row_index - offset
		if 0 <= column < len(columns) and columns[column] != label:
			_fail(table.location, message)
	return offset


def winning_border(first: slide_lib.table_formatting.Border,
		second: slide_lib.table_formatting.Border) -> slide_lib.table_formatting.Border:
	"""Resolve precedence, then width; second is the lower/right candidate on a tie."""
	result = first if (first.priority, first.width_pt) > (second.priority, second.width_pt) else second
	return result


def _normalize_edges(rows: tuple[tuple[slide_lib.native_model.TableCell, ...], ...],
		cells: tuple[tuple[slide_lib.table_formatting.CellFormatting, ...], ...],
		) -> tuple[tuple[slide_lib.table_formatting.CellFormatting, ...], ...]:
	"""Copy one winning border to both sides of every connected native edge."""
	parents = {}
	for row_index, row in enumerate(rows):
		for cell_index, cell in enumerate(row):
			for side in SIDES:
				key = (row_index, cell_index, side)
				parents[key] = key

	def root(key: tuple) -> tuple:
		"""Find an edge component, compressing its already-validated grid path."""
		while parents[key] != key:
			parents[key] = parents[parents[key]]
			key = parents[key]
		return key

	def connect(first: tuple, second: tuple) -> None:
		"""Join opposing sides, including the complete side of a merged cell."""
		parents[root(first)] = root(second)

	grids = []
	for row_index, row in enumerate(rows):
		grid = tuple(index for index, cell in enumerate(row) for column in range(cell.column_span))
		grids.append(grid)
		for index in range(len(row) - 1):
			connect((row_index, index, "right"), (row_index, index + 1, "left"))
		if row_index > 0:
			for upper, lower in zip(grids[row_index - 1], grid):
				connect((row_index - 1, upper, "bottom"), (row_index, lower, "top"))
	winners = {}
	# A native merged side has one appearance across all touching neighbors.
	# Later row/cell declarations give equal-priority ties to the lower/right cell.
	for key in parents:
		row_index, cell_index, side = key
		border = getattr(cells[row_index][cell_index], f"border_{side}")
		component = root(key)
		winners[component] = winning_border(winners[component], border) if component in winners else border
	result = tuple(tuple(dataclasses.replace(cell, **{
		f"border_{side}": winners[root((row_index, cell_index, side))] for side in SIDES})
		for cell_index, cell in enumerate(row)) for row_index, row in enumerate(cells))
	return result


def resolve_table(table: slide_lib.native_model.Table,
		theme: slide_lib.presentation_theme.PresentationTheme, registry: StyleRegistry) -> ResolvedTable:
	"""Resolve reliable structural roles, table defaults, then whole-cell source overrides."""
	if table.style_name not in registry.styles:
		_fail(table.location, f"unknown table-style {table.style_name!r}; expected " + ", ".join(registry.styles))
	definition = registry.styles[table.style_name]
	none = slide_lib.table_formatting.Border(0.0, "none", "000000")
	base = slide_lib.table_formatting.CellFormatting("FFFFFF", "151B2E", "left", "middle", False,
		none, none, none, none, 4.0, 9.0, 4.0, 9.0)
	base = _apply(base, definition.defaults, 10, theme)
	offset = _matrix_offset(table) if definition.matrix is not None else 0
	rows = ((table.headers,) if table.headers else ()) + table.rows
	resolved = []
	for row_index, row in enumerate(rows):
		header = bool(table.headers) and row_index == 0
		total = not header and _label(row[0].inlines).casefold() in ("total", "totals", "grand total")
		projected = []
		for column, cell in slide_lib.native_model.table_cell_positions(row):
			roles = []
			if not header and _NUMERIC.fullmatch(_label(cell.inlines)):
				roles.append("numeric")
			if definition.row_headings and column == 0 and not header:
				roles.append("row-header")
			if header:
				roles.append("header")
			if total:
				roles.append("total")
			if definition.matrix is not None and not header and column > 0:
				difference = (row_index - 1) - (column - 1) - offset
				if difference == 0:
					roles.append("matrix-diagonal")
				elif (difference < 0) == (definition.matrix == "lower"):
					roles.append("matrix-unused")
			current = base
			for role in roles:
				if role in definition.regions:
					current = _apply(current, definition.regions[role], 20 + REGIONS.index(role), theme)
			current = _apply(current, table.formatting, 30, theme)
			current = _apply(current, cell.formatting, 40, theme)
			projected.append(current)
		resolved.append(tuple(projected))
	return ResolvedTable(_normalize_edges(rows, tuple(resolved)))
