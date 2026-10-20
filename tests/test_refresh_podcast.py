"""Protect historical episode selection and repeatable announcement insertion."""

import datetime
import pathlib

import pytest

import tools.refresh_podcast


def test_historical_selection_excludes_future_and_requires_feed_coverage() -> None:
	"""A past lecture must not acquire a newer episode or silently use no history."""
	feed = b'''<feed xmlns="http://www.w3.org/2005/Atom"
		xmlns:yt="http://www.youtube.com/xml/schemas/2015">
		<entry><yt:videoId>aaaaaaaaaaa</yt:videoId><title>Earlier</title>
		<published>2026-09-10T15:00:00+00:00</published></entry>
		<entry><yt:videoId>bbbbbbbbbbb</yt:videoId><title>Later</title>
		<published>2026-09-18T01:00:00+00:00</published></entry></feed>'''
	assert tools.refresh_podcast.latest_episode(feed, datetime.date(2026, 9, 15))["title"] == "Earlier"
	# The later publication is still September 17 in the lecture's timezone.
	assert tools.refresh_podcast.latest_episode(feed, datetime.date(2026, 9, 17))["title"] == "Later"
	with pytest.raises(ValueError, match="coverage"):
		tools.refresh_podcast.latest_episode(feed, datetime.date(2026, 9, 1))


def test_refresh_is_repeatable_and_keeps_other_slides(tmp_path: pathlib.Path) -> None:
	"""Refreshing twice leaves one managed slide and retains hidden source slides."""
	source = ("=== layout: title-slide\n\n# Lecture\n\n## Announcements\n"
		"## Dr. Neil Voss\n## Sept 15, 2026\n\n"
		"=== layout: one-panel\n\n# YouTube\n\n@body\n\nChannel.\n\n"
		"=== layout: one-panel\nhidden: true\n\n# Later\n\n@body\n\nUnchanged.\n")
	episode = {"id": "aaaaaaaaaaa", "title": "Episode *title*", "published": "2026-09-10T15:00:00Z"}
	updated = tools.refresh_podcast.update_source(source, episode)
	assert tools.refresh_podcast.lecture_date(source) == datetime.date(2026, 9, 15)
	assert tools.refresh_podcast.update_source(updated, episode) == updated
	assert updated.count(tools.refresh_podcast.MARKER) == 1
	assert updated.endswith(source[source.index("=== layout: one-panel\nhidden:"):])
	announcement = tmp_path / "lect03a-2026_announcements.djot"
	announcement.write_text(source)
	(tmp_path / "lect01a-course_intro.djot").write_text(source)
	assert tools.refresh_podcast.announcement_paths([str(tmp_path)]) == [announcement.resolve()]
