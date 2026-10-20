"""Protect video selection and literal, clickable generated slide content."""

import pathlib

import PIL.Image
import pytest

import slide_lib.djot_parser
import slide_lib.layout_validation
import slide_lib.native_model
import tools.make_youtube_slide


def test_video_inputs_keep_the_selected_video_and_drop_tracking() -> None:
	"""Accepted URL forms resolve to one video; unrelated URLs cannot select a video."""
	identifier = "Mfk_L4Nx2ZI"
	for value in (identifier, f"https://youtu.be/{identifier}?si=tracking",
			f"https://www.youtube.com/watch?v={identifier}&list=playlist",
			f"https://m.youtube.com/watch?v={identifier}"):
		assert tools.make_youtube_slide.video_id(value) == identifier
	for value in ("invalid", f"https://example.com/watch?v={identifier}",
			f"https://www.youtube.com/watch?v={identifier}&v=WXPBoFDqNVk"):
		with pytest.raises(ValueError, match="Expected a YouTube"):
			tools.make_youtube_slide.video_id(value)


def test_generated_slide_preserves_literal_title_and_full_link(tmp_path: pathlib.Path) -> None:
	"""Fetched titles cannot introduce markup; captions retain an editable exact URL."""
	identifier = "Mfk_L4Nx2ZI"
	title = "Zero *factorial* _test_ [link] & \u03b1"
	image = tmp_path / "assets" / "youtube" / f"{identifier}.png"
	image.parent.mkdir(parents=True)
	PIL.Image.new("RGB", (32, 18)).save(image)
	path = tmp_path / "video.djot"
	path.write_text(tools.make_youtube_slide.slide_source(identifier, title), encoding="utf-8")
	deck = slide_lib.djot_parser.parse_deck(path)
	slide = deck.slides[0]
	caption = next(cell for cell in slide.cells if cell.name == "caption")
	assert slide.layout_class == "big-image"
	assert slide_lib.layout_validation.inline_text(caption.blocks[0].inlines) == title
	link = caption.blocks[1].inlines[0]
	assert isinstance(link, slide_lib.native_model.Link)
	assert link.url == f"https://www.youtube.com/watch?v={identifier}"
	assert slide_lib.layout_validation.inline_text(link.children) == link.url
