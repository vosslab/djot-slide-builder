"""PPTX theme projection helpers with no ambient theme authority."""

# PIP3 modules
from pptx.oxml.xmlchemy import OxmlElement

# local repo modules
import slide_lib.presentation_theme


#============================================
def office_coordinate(value: float, theme: slide_lib.presentation_theme.PresentationTheme) -> str:
	"""Convert one theme coordinate into the integer EMUs expected by OOXML."""
	return str(round(value * theme.emu_per_logical_pixel))


#============================================
def apply_list_theme(paragraph: object, level: int, ordered: bool,
		paragraph_only: bool, start: int,
		theme: slide_lib.presentation_theme.PresentationTheme) -> None:
	"""Apply native bullets, tab stops, and hanging indents to one paragraph."""
	if level >= len(theme.list_levels):
		raise ValueError(f"list nesting exceeds the {len(theme.list_levels)} native theme levels")
	properties = paragraph._p.get_or_add_pPr()
	for child in list(properties):
		if child.tag.endswith(("buNone", "buAutoNum", "buChar", "tabLst")):
			properties.remove(child)
	if paragraph_only:
		properties.set("marL", "0")
		properties.set("indent", "0")
		properties.append(OxmlElement("a:buNone"))
		return
	style = theme.list_levels[level]
	properties.set("marL", office_coordinate(style.text_position, theme))
	properties.set("indent", office_coordinate(style.bullet_position - style.text_position, theme))
	bullet = OxmlElement("a:buAutoNum" if ordered else "a:buChar")
	if ordered:
		bullet.set("type", "arabicPeriod")
		bullet.set("startAt", str(start))
	else:
		bullet.set("char", style.bullet_character)
	properties.append(bullet)
	tabs = OxmlElement("a:tabLst")
	tab = OxmlElement("a:tab")
	tab.set("pos", office_coordinate(style.text_position, theme))
	tabs.append(tab)
	properties.append(tabs)


#============================================
def apply_top_band_gradient(shape: object,
		theme: slide_lib.presentation_theme.PresentationTheme) -> None:
	"""Replace one shape's solid fill with the native lecture-theme gradient."""
	properties = shape.element.spPr
	solid_fill = next(child for child in properties if child.tag.endswith("solidFill"))
	gradient = OxmlElement("a:gradFill")
	stops = OxmlElement("a:gsLst")
	# ASVS 2.2.1: gradient colors come only from the validated template contract.
	for position, color in ((0, theme.gradient_start_color),
			(100000, theme.gradient_end_color)):
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
