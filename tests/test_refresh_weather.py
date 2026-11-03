"""Protect literal weather snapshots and repeatable announcement insertion."""

import datetime
import io
import pathlib
import types
import urllib.error

import PIL.Image
import pytest

import slide_lib.djot_parser
import slide_lib.layout_validation
import slide_lib.native_model
import tools.refresh_weather


def weather_html() -> bytes:
	"""Use the published page's active-story structure, with a second story."""
	return b'''<div id="tabs" class="c-tabs">
		<div class="c-tabs-nav__link is-active">A *cool* outlook</div>
		<div class="c-tabs-nav__link">Other story</div>
		<div class="c-tab is-active"><div class="graphicast">
		<div class="image"><img src="/images/lot/wxstory/Tab4FileL.png"></div>
		<div class="description">Some <strong>sun</strong> &amp; clouds.<br>Then *rain*.</div>
		</div></div>
		<div class="c-tab"><div class="graphicast">
		<div class="image"><img src="/images/lot/wxstory/Tab1FileL.png"></div>
		<div class="description">Unrelated forecast.</div></div></div></div>'''


def png_bytes(color: str = "blue") -> bytes:
	"""Make one tiny, valid test-owned graphic without a file fixture."""
	data = io.BytesIO()
	PIL.Image.new("RGB", (32, 18), color).save(data, format="PNG")
	return data.getvalue()


def test_all_stories_and_generated_caption_preserve_literal_forecast(tmp_path: pathlib.Path) -> None:
	stories = tools.refresh_weather.weather_stories(weather_html())
	assert len(stories) == 2 and stories[1]["title"] == "Other story"
	assert stories[1]["caption"] == "Unrelated forecast."
	story = stories[0]
	assert story == {"title": "A *cool* outlook", "caption": "Some sun & clouds. Then *rain*.",
		"image_url": "https://www.weather.gov/images/lot/wxstory/Tab4FileL.png"}
	image = tmp_path / "assets/weather_story/saved.png"
	image.parent.mkdir(parents=True)
	image.write_bytes(png_bytes())
	path = tmp_path / "weather.djot"
	path.write_text(tools.refresh_weather.weather_slide(story, image.name, datetime.date(2026, 11, 2)))
	slide = slide_lib.djot_parser.parse_deck(path).slides[0]
	caption = next(cell for cell in slide.cells if cell.name == "caption")
	assert slide.layout_class == "big-image" and not slide.notes
	assert len(caption.blocks) == 1 and len(slide.citation) == 1
	assert slide_lib.layout_validation.inline_text(caption.blocks[0].inlines) == story["caption"]
	assert all(isinstance(inline, slide_lib.native_model.Text) for inline in caption.blocks[0].inlines)
	assert "retrieved Nov 02, 2026" in slide_lib.layout_validation.inline_text(slide.citation[0].inlines)
	link = next(inline for inline in slide.citation[0].inlines if isinstance(inline, slide_lib.native_model.Link))
	assert link.url == tools.refresh_weather.PAGE_URL
	assert slide_lib.layout_validation.inline_text(link.children) == link.url


def test_refresh_previews_then_replaces_snapshots_without_changing_other_slides(tmp_path, monkeypatch) -> None:
	path = tmp_path / "lect09a-2026_announcements.djot"
	source = ("=== layout: one-panel\n# Today's Agenda\n@body\nAgenda.\n\n"
		"=== layout: one-panel\n# [Breakout Room Chat]{color=red}\n@body\nQuestion.\n\n"
		"=== include: repo:evergreen/youtube_channel.djot\n\n"
		"=== layout: one-panel\nhidden: true\n# Later\n@body\nKeep this.\n")
	path.write_text(source)
	(tmp_path / "lect09c-topic.djot").write_text("Not an announcement.")
	assert tools.refresh_weather.announcement_paths([str(tmp_path), str(path)]) == [path.resolve()]
	image = png_bytes()
	monkeypatch.setattr(tools.refresh_weather, "download",
		lambda url, limit: weather_html() if url == tools.refresh_weather.PAGE_URL else image)
	date = datetime.date(2026, 11, 2)
	tools.refresh_weather.refresh([path], False, date)
	assert path.read_text() == source and not (tmp_path / "assets").exists()
	tools.refresh_weather.refresh([path], True, date)
	first = path.read_text()
	assert first.count(tools.refresh_weather.WEATHER_ASSET_PATH) == 2
	assert first.index("Today's Agenda") < first.index("assets/weather_story/") < first.index("Breakout Room Chat")
	assert first.endswith(source[source.index("=== layout: one-panel\n# [Breakout"):])
	tools.refresh_weather.refresh([path], True, date)
	assert path.read_text() == first
	old_image = next((tmp_path / "assets/weather_story").glob("*.png"))
	assert old_image.read_bytes() == image
	image = png_bytes("red")
	tools.refresh_weather.refresh([path], True, date)
	assert path.read_text().count(tools.refresh_weather.WEATHER_ASSET_PATH) == 2
	assert old_image.read_bytes() == png_bytes()
	assert len(list((tmp_path / "assets/weather_story").glob("*.png"))) == 2


@pytest.mark.parametrize("failure", ["network", "image", "caption", "anchor"])
def test_failed_refresh_preserves_every_selected_deck_and_saved_image(tmp_path, monkeypatch, failure) -> None:
	source = "=== layout: one-panel\n# Ice Breaker\n@body\nTalk.\n"
	first = tmp_path / "lect09a-2026_announcements.djot"
	second = tmp_path / "lect10a-2026_announcements.djot"
	first.write_text(source)
	second.write_text(source if failure != "anchor" else "=== layout: one-panel\n# No Anchor\n")
	before = [path.read_bytes() for path in (first, second)]
	asset = tmp_path / "assets/weather_story/earlier.png"
	asset.parent.mkdir(parents=True)
	asset.write_bytes(png_bytes("gold"))
	old_image = asset.read_bytes()

	def download(url, limit):
		if failure == "network":
			raise urllib.error.URLError("Test outage")
		if url == tools.refresh_weather.PAGE_URL:
			return weather_html().replace(b'class="description"', b'class="missing"') if failure == "caption" else weather_html()
		return b"not an image" if failure == "image" else png_bytes()

	monkeypatch.setattr(tools.refresh_weather, "download", download)
	with pytest.raises((ValueError, urllib.error.URLError, PIL.UnidentifiedImageError)):
		tools.refresh_weather.refresh([first, second], True, datetime.date(2026, 11, 2))
	assert [path.read_bytes() for path in (first, second)] == before
	assert asset.read_bytes() == old_image
	assert list(asset.parent.iterdir()) == [asset]


def test_ambiguous_icebreaker_requires_correction() -> None:
	slide = "=== layout: big-image\n@image\n![Story](assets/weather_story/saved.png)\n@caption\nForecast.\n\n"
	anchor = "=== layout: one-panel\n# Breakout Room Chat\n@body\nTalk.\n"
	assert tools.refresh_weather.update_source(slide + slide + anchor, slide) == slide + anchor
	with pytest.raises(ValueError, match="one icebreaker"):
		tools.refresh_weather.update_source(anchor + anchor, slide)


def test_download_bounds_and_redirects_keep_remote_input_on_official_resources(monkeypatch) -> None:
	for url in ("http://www.weather.gov/lot/weatherstory", "https://example.test/graphic.png",
		"https://www.weather.gov/images/lot/wxstory/../../private.png"):
		with pytest.raises(ValueError, match="official"):
			tools.refresh_weather.WeatherRedirectHandler().redirect_request(None, None, 302, "", {}, url)
	response = io.BytesIO(b"oversized")
	response.url = tools.refresh_weather.PAGE_URL
	opener = types.SimpleNamespace(open=lambda request, timeout: response)
	monkeypatch.setattr(tools.refresh_weather.urllib.request, "build_opener", lambda handler: opener)
	monkeypatch.setattr(tools.refresh_weather.time, "sleep", lambda delay: None)
	with pytest.raises(ValueError, match="exceeds"):
		tools.refresh_weather.download(tools.refresh_weather.PAGE_URL, 3)
