"""Protect historical episode selection and repeatable announcement insertion."""

import datetime
import io
import pathlib

import pytest

import slide_lib.refresh_podcast as refresh_podcast




def test_selection_skips_newer_special_episodes() -> None:
	"""A special must not replace the latest regular classroom game episode."""
	feed = b'''<feed xmlns="http://www.w3.org/2005/Atom"
		xmlns:yt="http://www.youtube.com/xml/schemas/2015"
		xmlns:media="http://search.yahoo.com/mrss/">
		<entry><yt:videoId>aaaaaaaaaaa</yt:videoId><title>Stump the Vibe Coder, Episode 37</title>
		<media:group><media:description>https://vosslab.github.io/game/</media:description></media:group>
		<published>2026-10-22T14:00:00+00:00</published></entry>
		<entry><yt:videoId>bbbbbbbbbbb</yt:videoId><title>StVC Special Episode</title>
		<published>2026-10-23T08:00:00+00:00</published></entry></feed>'''
	episode = refresh_podcast.latest_episode(feed)
	assert episode["id"] == "aaaaaaaaaaa"
	assert "Stump the Vibe Coder &#35;37" in refresh_podcast.podcast_slide(episode)
	assert refresh_podcast.latest_episode(feed, datetime.date(2026, 11, 5))["id"] == "aaaaaaaaaaa"
	special_only = feed.replace(b"Stump the Vibe Coder, Episode 37", b"Another SPECIAL")
	with pytest.raises(ValueError, match="coverage"):
		refresh_podcast.latest_episode(special_only)


def test_download_admits_thumbnails_and_rejects_other_origins(monkeypatch: pytest.MonkeyPatch) -> None:
	"""The thumbnail CDN must work without opening downloads to arbitrary origins."""
	monkeypatch.setattr(refresh_podcast.time, "sleep", lambda _seconds: None)
	monkeypatch.setattr(refresh_podcast.urllib.request, "urlopen",
		lambda _request, timeout: io.BytesIO(b"image"))
	assert refresh_podcast.download("https://i.ytimg.com/vi/aaaaaaaaaaa/maxresdefault.jpg", 64) == b"image"
	for url in ("http://i.ytimg.com/image.jpg", "https://example.com/image.jpg"):
		with pytest.raises(ValueError, match="HTTPS"):
			refresh_podcast.download(url, 64)


def test_historical_selection_excludes_future_and_requires_feed_coverage() -> None:
	"""A past lecture must not acquire a newer episode or silently use no history."""
	feed = b'''<feed xmlns="http://www.w3.org/2005/Atom"
		xmlns:yt="http://www.youtube.com/xml/schemas/2015"
		xmlns:media="http://search.yahoo.com/mrss/">
		<entry><yt:videoId>aaaaaaaaaaa</yt:videoId><title>Earlier</title>
		<media:group><media:description>https://vosslab.github.io/earlier/</media:description></media:group>
		<published>2026-09-10T15:00:00+00:00</published></entry>
		<entry><yt:videoId>bbbbbbbbbbb</yt:videoId><title>Later</title>
		<media:group><media:description>https://vosslab.github.io/later/</media:description></media:group>
		<published>2026-09-18T01:00:00+00:00</published></entry></feed>'''
	assert refresh_podcast.latest_episode(feed, datetime.date(2026, 9, 15))["title"] == "Earlier"
	# The later publication is still September 17 in the lecture's timezone.
	assert refresh_podcast.latest_episode(feed, datetime.date(2026, 9, 17))["title"] == "Later"
	with pytest.raises(ValueError, match="coverage"):
		refresh_podcast.latest_episode(feed, datetime.date(2026, 9, 1))


def test_refresh_is_repeatable_and_keeps_other_slides(tmp_path: pathlib.Path) -> None:
	"""Refreshing twice leaves one managed slide and retains hidden source slides."""
	source = ("=== layout: title-slide\n\n# Lecture\n\n## Announcements\n"
		"## Dr. Neil Voss\n## Sept 15, 2026\n\n"
		"=== layout: one-panel\n\n# YouTube\n\n@body\n\nChannel.\n\n"
		"=== layout: one-panel\nhidden: true\n\n# Later\n\n@body\n\nUnchanged.\n")
	episode = {"id": "aaaaaaaaaaa", "title": "StVC 36: Bad Cell Day \u2014 Two Drugs, One Keyboard | Stump the Vibe Coder Episode 36",
		"published": "2026-09-10T15:00:00Z", "project_url": "https://vosslab.github.io/game/"}
	updated = refresh_podcast.update_source(source, episode)
	assert refresh_podcast.lecture_date(source) == datetime.date(2026, 9, 15)
	assert refresh_podcast.update_source(updated, episode) == updated
	assert updated.count(refresh_podcast.PODCAST_ASSET_PATH) == 1
	next_episode = dict(episode, id="bbbbbbbbbbb")
	refreshed = refresh_podcast.update_source(updated, next_episode)
	assert refreshed.count(refresh_podcast.PODCAST_ASSET_PATH) == 1
	assert episode["id"] not in refreshed
	assert next_episode["id"] in refreshed
	assert "@notes" not in updated
	assert episode["published"] not in updated
	assert "@citation" not in updated
	assert "Watch the Video: [https://www.youtube.com/watch" in updated
	assert "@caption\n\nStump the Vibe Coder &#35;36&#58; Bad Cell Day &#8212;" in updated
	assert "https://www.youtube.com/watch?v=aaaaaaaaaaa)\\\nPlay the Game: https://vosslab.github.io/game/" in updated
	assert updated.endswith(source[source.index("=== layout: one-panel\nhidden:"):])
	announcement = tmp_path / "lect03a-2026_announcements.djot"
	announcement.write_text(source)
	(tmp_path / "lect01a-course_intro.djot").write_text(source)
	assert refresh_podcast.announcement_paths([str(tmp_path)]) == [announcement.resolve()]


def test_project_link_uses_pages_and_never_substitutes_a_repository() -> None:
	"""Students need the runnable site; missing or ambiguous destinations need correction."""
	description = "Project: https://vosslab.github.io/game/\nRepo: https://github.com/vosslab/game"
	assert refresh_podcast.project_url(description) == "https://vosslab.github.io/game/"
	for invalid in ("https://github.com/vosslab/game", "",
		description + "\nhttps://vosslab.github.io/another/"):
		with pytest.raises(ValueError, match="GitHub Pages"):
			refresh_podcast.project_url(invalid)


def test_refresh_preserves_evergreen_includes() -> None:
	"""Updating a weekly episode must retain the shared channel and following course slides."""
	source = ("=== layout: title-slide\n# Announcements\n"
		"=== include: repo:evergreen/youtube_channel.djot\n\n"
		"=== include: repo:genetics/evergreen/course_information.djot\n\n"
		"=== include: repo:genetics/evergreen/exam_guidance.djot\nhidden: true\n")
	episode = {"id": "aaaaaaaaaaa", "title": "Example", "published": "2026-10-22T00:00:00Z",
		"project_url": "https://vosslab.github.io/game/"}
	updated = refresh_podcast.update_source(source, episode)
	assert refresh_podcast.update_source(updated, episode) == updated
	assert updated.index("youtube_channel.djot") < updated.index(episode["id"])
	assert updated.index(episode["id"]) < updated.index("course_information.djot")
	assert updated.endswith("exam_guidance.djot\nhidden: true\n")
