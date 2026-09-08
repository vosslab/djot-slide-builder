"""Contract tests for the authoritative LibreOffice presentation theme."""

# Standard Library
import hashlib
import pathlib
import zipfile
import xml.etree.ElementTree

# PIP3 modules
import defusedxml.ElementTree
import pytest

# Local Modules
import slide_lib.presentation_theme


#============================================
def shipped_styles_root() -> xml.etree.ElementTree.Element:
	"""Load the styles member from the production OTP package."""
	with zipfile.ZipFile(slide_lib.presentation_theme.DEFAULT_TEMPLATE_PATH) as archive:
		root = defusedxml.ElementTree.fromstring(archive.read("styles.xml"))
	return root


#============================================
def theme_style(root: xml.etree.ElementTree.Element, name: str) -> xml.etree.ElementTree.Element:
	"""Return one named presentation style from the shipped OTP."""
	style = slide_lib.presentation_theme.presentation_style(root, name)
	return style


#============================================
def otp_without_title_shrink_policy(tmp_path: pathlib.Path) -> pathlib.Path:
	"""Build one otherwise-identical OTP whose title loses its required overflow policy."""
	styles_root = shipped_styles_root()
	title = theme_style(styles_root, "Default-title")
	graphics = title.find("style:graphic-properties", slide_lib.presentation_theme.NS)
	if graphics is None:
		raise ValueError("production OTP title lacks graphic properties")
	del graphics.attrib[slide_lib.presentation_theme.qname("style", "shrink-to-fit")]
	output_path = tmp_path / "missing-title-shrink.otp"
	with zipfile.ZipFile(slide_lib.presentation_theme.DEFAULT_TEMPLATE_PATH) as source:
		members = [(member, source.read(member.filename)) for member in source.infolist()]
	with zipfile.ZipFile(output_path, "w") as destination:
		for member, content in members:
			if member.filename == "styles.xml":
				content = xml.etree.ElementTree.tostring(styles_root, encoding="utf-8",
					xml_declaration=True)
			destination.writestr(member, content, compress_type=member.compress_type)
	return output_path


#============================================
def otp_with_outline_line_height(tmp_path: pathlib.Path, line_height: str | None) -> pathlib.Path:
	"""Build one otherwise-identical OTP with a changed ordinary line-height."""
	styles_root = shipped_styles_root()
	outline = theme_style(styles_root, "Default-outline1")
	paragraph = outline.find("style:paragraph-properties", slide_lib.presentation_theme.NS)
	if paragraph is None:
		raise ValueError("production OTP outline lacks paragraph properties")
	attribute = slide_lib.presentation_theme.qname("fo", "line-height")
	if line_height is None:
		del paragraph.attrib[attribute]
	else:
		paragraph.attrib[attribute] = line_height
	output_path = tmp_path / "drifted-outline-line-height.otp"
	with zipfile.ZipFile(slide_lib.presentation_theme.DEFAULT_TEMPLATE_PATH) as source:
		members = [(member, source.read(member.filename)) for member in source.infolist()]
	with zipfile.ZipFile(output_path, "w") as destination:
		for member, member_content in members:
			if member.filename == "styles.xml":
				member_content = xml.etree.ElementTree.tostring(styles_root, encoding="utf-8",
					xml_declaration=True)
			destination.writestr(member, member_content, compress_type=member.compress_type)
	return output_path


#============================================
def font_sizes(properties: dict[str, str]) -> tuple[str, str, str]:
	"""Return the Western, Asian, and complex default sizes from resolved properties."""
	sizes = (
		properties[slide_lib.presentation_theme.qname("fo", "font-size")],
		properties[slide_lib.presentation_theme.qname("style", "font-size-asian")],
		properties[slide_lib.presentation_theme.qname("style", "font-size-complex")],
	)
	return sizes


#============================================
def test_theme_exposes_point_valued_native_placeholder_contract() -> None:
	"""Adapters receive native frames, fonts, floors, and bounded overflow policy."""
	theme = slide_lib.presentation_theme.default_theme()
	assert (theme.western_font_name, theme.standard_title_size_pt, theme.ordinary_body_size_pt,
		theme.ordinary_line_spacing_em, theme.title_floor_size_pt, theme.body_floor_size_pt,
		theme.overflow_policy) == (
		"OpenDyslexic", 36.0, 28.0, 1.30, 30.0, 24.0,
		slide_lib.presentation_theme.OverflowPolicy.SHRINK_ONLY)
	assert theme.title_style_name == "Default-title" and theme.outline_style_names[0] == "Default-outline1"
	assert theme.title_frame.width_cm > 0.0 and theme.outline_frame.height_cm > 0.0
	assert all(metric.face in slide_lib.presentation_theme.FONT_FACE_PROFILES
		and metric.units_per_em > 0 and metric.ascender > 0 and metric.descender < 0
		for metric in theme.font_metrics)


#============================================
def test_bundled_font_profiles_are_hash_verified_repository_assets() -> None:
	"""Every emitted family resolves to its licensed asset rather than a host font path."""
	for profile in slide_lib.presentation_theme.FONT_FACE_PROFILES:
		path = slide_lib.presentation_theme.font_asset_path(profile)
		with path.open("rb") as asset_file:
			digest = hashlib.file_digest(asset_file, "sha256").hexdigest()
		assert path.is_relative_to(slide_lib.presentation_theme.REPOSITORY_ROOT)
		assert not profile.relative_path.is_absolute() and ".." not in profile.relative_path.parts
		assert digest == profile.sha256
	assert slide_lib.presentation_theme.validated_font_metrics()


#============================================
def test_machine_readable_font_provenance_covers_each_registered_face() -> None:
	"""The pinned upstream and OFL records cannot drift away from face profiles."""
	provenance = slide_lib.presentation_theme.validate_font_manifest()
	assert tuple(item.profile for item in provenance) == slide_lib.presentation_theme.FONT_FACE_PROFILES
	assert all(item.upstream_url.startswith("https://") and item.upstream_revision and
		item.license_path.parts[:2] == ("assets", "fonts") for item in provenance)


#============================================
def test_font_selection_is_exact_and_never_synthesizes_an_unbundled_style() -> None:
	"""The run-style boundary accepts only real bundled faces."""
	bold_italic = slide_lib.presentation_theme.select_font_face("OpenDyslexic", True, True)
	assert bold_italic.bold and bold_italic.italic
	with pytest.raises(slide_lib.presentation_theme.ThemeError, match="PT Sans Narrow"):
		slide_lib.presentation_theme.select_font_face("PT Sans Narrow", italic=True)
	with pytest.raises(slide_lib.presentation_theme.ThemeError, match="Unknown Family"):
		slide_lib.presentation_theme.select_font_face("Unknown Family")


#============================================
def test_font_validation_rejects_missing_or_tampered_assets(tmp_path: pathlib.Path) -> None:
	"""A changed package cannot silently fall back to a system-installed lookalike."""
	profile = slide_lib.presentation_theme.FontFaceProfile("Example", False, False,
		pathlib.PurePosixPath("assets/fonts/example.ttf"), "0" * 64, 0)
	with pytest.raises(slide_lib.presentation_theme.ThemeError, match="missing"):
		slide_lib.presentation_theme.validate_font_face(profile, tmp_path)
	asset_path = tmp_path / profile.relative_path
	asset_path.parent.mkdir(parents=True)
	asset_path.write_bytes(b"not a font")
	with pytest.raises(slide_lib.presentation_theme.ThemeError, match="hash differs"):
		slide_lib.presentation_theme.validate_font_face(profile, tmp_path)


#============================================
def test_shipped_otp_defaults_match_native_title_and_outline_contract() -> None:
	"""New LibreOffice placeholders inherit the same 36/28-point defaults as adapters."""
	root = shipped_styles_root()
	title = theme_style(root, "Default-title")
	title_properties = slide_lib.presentation_theme.effective_text_properties(root, title, "Default-title")
	outline_styles = tuple(theme_style(root, f"Default-outline{level}") for level in range(1, 10))
	outline_properties = tuple(slide_lib.presentation_theme.effective_text_properties(root, style,
		f"Default-outline{level}") for level, style in enumerate(outline_styles, start=1))
	outline_paragraph_properties = tuple(
		slide_lib.presentation_theme.effective_paragraph_properties(root, style,
			f"Default-outline{level}") for level, style in enumerate(outline_styles, start=1))
	title_graphics = title.find("style:graphic-properties", slide_lib.presentation_theme.NS)
	outline_graphics = outline_styles[0].find("style:graphic-properties", slide_lib.presentation_theme.NS)
	assert font_sizes(title_properties) == ("36pt", "36pt", "36pt") and \
		title_properties[slide_lib.presentation_theme.qname("fo", "font-family")] == "OpenDyslexic"
	assert all(font_sizes(properties) == ("28pt", "28pt", "28pt") and
		properties[slide_lib.presentation_theme.qname("fo", "font-family")] == "OpenDyslexic"
		for properties in outline_properties)
	assert all(properties[slide_lib.presentation_theme.qname("fo", "line-height")] == "130%"
		for properties in outline_paragraph_properties)
	for graphics in (title_graphics, outline_graphics):
		assert graphics is not None and graphics.attrib[
			slide_lib.presentation_theme.qname("draw", "auto-grow-height")] == "false" and \
			graphics.attrib[slide_lib.presentation_theme.qname("draw", "fit-to-size")] == "false" and \
			graphics.attrib[slide_lib.presentation_theme.qname("style", "shrink-to-fit")] == "true"


#============================================
def test_theme_loader_rejects_a_title_without_the_fixed_shrink_only_policy(tmp_path: pathlib.Path) -> None:
	"""The loader prevents a template title from silently restoring frame adaptation."""
	with pytest.raises(slide_lib.presentation_theme.ThemeError, match="Default-title"):
		slide_lib.presentation_theme.load_theme(otp_without_title_shrink_policy(tmp_path))


#============================================
def test_theme_loader_rejects_outline_line_spacing_drift(tmp_path: pathlib.Path) -> None:
	"""The native ordinary placeholder keeps the same nominal advance as the plan."""
	with pytest.raises(slide_lib.presentation_theme.ThemeError, match="1.30em"):
		slide_lib.presentation_theme.load_theme(otp_with_outline_line_height(tmp_path, "120%"))
	with pytest.raises(slide_lib.presentation_theme.ThemeError, match="line height"):
		slide_lib.presentation_theme.load_theme(otp_with_outline_line_height(tmp_path, None))


#============================================
def test_shipped_master_title_and_outline_are_real_placeholders() -> None:
	"""The ODP master exposes editable native title and outline layout slots."""
	root = shipped_styles_root()
	master = root.find(".//style:master-page", slide_lib.presentation_theme.NS)
	if master is None:
		raise ValueError("production OTP is missing a master page")
	title = slide_lib.presentation_theme.master_frame(master, "title")
	outline = slide_lib.presentation_theme.master_frame(master, "outline")
	assert title.attrib[slide_lib.presentation_theme.qname("presentation", "placeholder")] == "true"
	assert outline.attrib[slide_lib.presentation_theme.qname("presentation", "placeholder")] == "true"
