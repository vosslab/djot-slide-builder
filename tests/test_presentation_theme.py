"""Contract tests for the authoritative LibreOffice presentation theme."""

# Standard Library
import pathlib

# PIP3 modules
import pytest

# Local Modules
import slide_lib.presentation_theme


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
