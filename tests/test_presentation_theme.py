"""Contract tests for the authoritative LibreOffice presentation theme."""

# Standard Library
import pathlib

# PIP3 modules
import pytest

# Local Modules
import slide_lib.presentation_theme


#============================================
def test_license_notices_are_nonblocking_packaging_metadata(tmp_path: pathlib.Path) -> None:
	"""Missing or changed license text must not prevent rendering with valid font records."""
	theme = slide_lib.presentation_theme
	assert theme.odf_font_license_payloads(tmp_path) == ({}, {})
	license_path = tmp_path / "assets/fonts/licenses/notice.txt"
	license_path.parent.mkdir(parents=True)
	license_path.write_bytes(b"Changed notice text\n")
	payloads, _media_types = theme.odf_font_license_payloads(tmp_path)
	assert payloads[f"Fonts/licenses/{license_path.name}"] == b"Changed notice text\n"


#============================================
def test_font_selection_is_exact_and_never_synthesizes_an_unbundled_style() -> None:
	"""The run-style boundary accepts only real bundled faces."""
	bold_italic = slide_lib.presentation_theme.select_font_face("Atkinson Hyperlegible Next", True, True)
	assert bold_italic.bold and bold_italic.italic
	mono = slide_lib.presentation_theme.select_font_face("Atkinson Hyperlegible Mono", True, True)
	assert mono.bold and mono.italic
	with pytest.raises(slide_lib.presentation_theme.ThemeError, match="Unknown Family"):
		slide_lib.presentation_theme.select_font_face("Unknown Family")


#============================================
def test_font_embedding_requires_an_editable_os2_permission() -> None:
	"""The ODP writer reports a restrictive face instead of allowing host substitution."""
	profile = slide_lib.presentation_theme.FONT_FACE_PROFILES[0]
	slide_lib.presentation_theme.validate_editable_embedding_permission(profile, 0)
	slide_lib.presentation_theme.validate_editable_embedding_permission(profile, 8)
	with pytest.raises(slide_lib.presentation_theme.ThemeError, match="forbids editable embedding"):
		slide_lib.presentation_theme.validate_editable_embedding_permission(profile, 4)
	with pytest.raises(slide_lib.presentation_theme.ThemeError, match="forbids editable embedding"):
		slide_lib.presentation_theme.validate_editable_embedding_permission(profile, 8 | 0x0200)


#============================================
def test_font_validation_rejects_missing_or_unreadable_assets(tmp_path: pathlib.Path) -> None:
	"""A changed package cannot silently fall back to a system-installed lookalike."""
	profile = slide_lib.presentation_theme.FontFaceProfile("Example", False, False,
		pathlib.PurePosixPath("assets/fonts/example.ttf"), "0" * 64, 0)
	with pytest.raises(slide_lib.presentation_theme.ThemeError, match="missing"):
		slide_lib.presentation_theme.validate_font_face(profile, tmp_path)
	asset_path = tmp_path / profile.relative_path
	asset_path.parent.mkdir(parents=True)
	asset_path.write_bytes(b"not a font")
	with pytest.raises(slide_lib.presentation_theme.ThemeError, match="unreadable"):
		slide_lib.presentation_theme.validate_font_face(profile, tmp_path)


#============================================
