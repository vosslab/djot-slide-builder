"""Native PPTX theme semantics shared by every standard Djot slide."""

# Standard Library
from dataclasses import dataclass

# PIP3 modules
from pptx.oxml.xmlchemy import OxmlElement


PX = 9525
TOP_BAND_HEIGHT = 58.0


@dataclass(frozen=True)
class ListLevelStyle:
	"""Bullet and text positions for one native outline level, in CSS pixels."""
	bullet_position: float
	text_position: float
	bullet_character: str


LIST_LEVEL_STYLES = (
	ListLevelStyle(11.0, 45.0, "\u25cf"),
	ListLevelStyle(57.0, 91.0, "\u2013"),
	ListLevelStyle(106.0, 136.0, "\u25cf"),
	ListLevelStyle(159.0, 182.0, "\u2013"),
	ListLevelStyle(204.0, 227.0, "\u25cf"),
	ListLevelStyle(249.0, 272.0, "\u2013"),
	ListLevelStyle(295.0, 318.0, "\u25cf"),
	ListLevelStyle(340.0, 363.0, "\u2013"),
	ListLevelStyle(386.0, 409.0, "\u25cf"),
)


#============================================
def office_coordinate(value: float) -> str:
	"""Convert one theme coordinate into the integer EMUs expected by OOXML."""
	return str(round(value * PX))


#============================================
def apply_list_theme(paragraph: object, level: int, ordered: bool,
		paragraph_only: bool, start: int) -> None:
	"""Apply native bullets, tab stops, and hanging indents to one paragraph."""
	if level >= len(LIST_LEVEL_STYLES):
		raise ValueError(f"list nesting exceeds the {len(LIST_LEVEL_STYLES)} native theme levels")
	properties = paragraph._p.get_or_add_pPr()
	for child in list(properties):
		if child.tag.endswith(("buNone", "buAutoNum", "buChar", "tabLst")):
			properties.remove(child)
	if paragraph_only:
		properties.set("marL", "0")
		properties.set("indent", "0")
		properties.append(OxmlElement("a:buNone"))
		return
	style = LIST_LEVEL_STYLES[level]
	properties.set("marL", office_coordinate(style.text_position))
	properties.set("indent", office_coordinate(style.bullet_position - style.text_position))
	bullet = OxmlElement("a:buAutoNum" if ordered else "a:buChar")
	if ordered:
		bullet.set("type", "arabicPeriod")
		bullet.set("startAt", str(start))
	else:
		bullet.set("char", style.bullet_character)
	properties.append(bullet)
	tabs = OxmlElement("a:tabLst")
	tab = OxmlElement("a:tab")
	tab.set("pos", office_coordinate(style.text_position))
	tabs.append(tab)
	properties.append(tabs)


#============================================
def apply_top_band_gradient(shape: object) -> None:
	"""Replace one shape's solid fill with the native lecture-theme gradient."""
	properties = shape.element.spPr
	solid_fill = next(child for child in properties if child.tag.endswith("solidFill"))
	gradient = OxmlElement("a:gradFill")
	stops = OxmlElement("a:gsLst")
	# ASVS 1.1.2 and 1.2.1: construct typed OOXML only at the final output boundary.
	for position, color in ((0, "94B0CC"), (65000, "DEE8F2"), (100000, "FFFFFF")):
		stop = OxmlElement("a:gs")
		stop.set("pos", str(position))
		value = OxmlElement("a:srgbClr")
		value.set("val", color)
		stop.append(value)
		stops.append(stop)
	gradient.append(stops)
	linear = OxmlElement("a:lin")
	linear.set("ang", "5400000")
	linear.set("scaled", "1")
	gradient.append(linear)
	properties.replace(solid_fill, gradient)
