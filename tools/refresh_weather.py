#!/usr/bin/env python3
"""Preview or refresh the NWS Chicago weather story before an announcement icebreaker."""

# Standard Library
import argparse
import datetime
import difflib
import hashlib
import io
import pathlib
import random
import re
import time
import urllib.parse
import urllib.request
import zoneinfo

# Third-Party Modules
import lxml.html
import PIL.Image


PAGE_URL = "https://www.weather.gov/lot/weatherstory"
WEATHER_ASSET_PATH = "assets/weather_story/"


def validate_url(url: str) -> None:
	"""Admit only the official HTTPS story page and Chicago PNG graphics."""
	parsed = urllib.parse.urlsplit(url)
	# ASVS 2.2.1/1.2.2: fetched markup cannot choose arbitrary hosts or local paths.
	if (parsed.scheme != "https" or parsed.netloc not in ("www.weather.gov", "weather.gov")
			or not (parsed.path == "/lot/weatherstory" or
				re.fullmatch(r"/images/lot/wxstory/[A-Za-z0-9_-]+\.png", parsed.path))):
		raise ValueError(f"Expected an official NWS Chicago weather-story URL: {url}")


class WeatherRedirectHandler(urllib.request.HTTPRedirectHandler):
	"""Keep redirect requests on the same approved public resources."""

	def redirect_request(self, request, response, code, message, headers, new_url):
		validate_url(new_url)
		return super().redirect_request(request, response, code, message, headers, new_url)


def download(url: str, limit: int) -> bytes:
	"""Fetch one bounded official resource with certificate validation and a timeout."""
	validate_url(url)
	time.sleep(random.random())
	request = urllib.request.Request(url, headers={"User-Agent": "djot-slide-builder/1.0"})
	opener = urllib.request.build_opener(WeatherRedirectHandler())
	with opener.open(request, timeout=30) as response:
		validate_url(response.url)
		data = response.read(limit + 1)
	if len(data) > limit:
		raise ValueError(f"Weather resource exceeds {limit} bytes: {url}")
	return data


def weather_story(data: bytes) -> dict[str, str]:
	"""Read the initially displayed graphic and its own description, without running scripts."""
	root = lxml.html.fromstring(data, parser=lxml.html.HTMLParser(no_network=True))
	tabs = root.xpath('//*[@id="tabs"]')
	if len(tabs) != 1:
		raise ValueError("Expected one NWS weather-story tab container; decks unchanged")
	active = [item for item in tabs[0].find_class("c-tab") if "is-active" in item.classes]
	titles = [item for item in tabs[0].find_class("c-tabs-nav__link") if "is-active" in item.classes]
	if len(active) != 1 or len(titles) != 1:
		raise ValueError("Expected one initially displayed NWS story; decks unchanged")
	graphics = active[0].find_class("graphicast")
	if len(graphics) != 1:
		raise ValueError("Expected one graphic in the displayed NWS story; decks unchanged")
	images = graphics[0].xpath('.//div[@class="image"]/img[@src]')
	descriptions = graphics[0].find_class("description")
	if len(images) != 1 or len(descriptions) != 1:
		raise ValueError("Expected a weather image and its description; decks unchanged")
	# A line break separates words even when the source HTML has no surrounding spaces.
	for line_break in descriptions[0].xpath(".//br"):
		line_break.tail = " " + (line_break.tail or "")
	title = " ".join(titles[0].text_content().split())
	caption = " ".join(descriptions[0].text_content().split())
	if not title or not caption:
		raise ValueError("Weather story has an empty title or description; decks unchanged")
	image_url = urllib.parse.urljoin(PAGE_URL, images[0].attrib["src"])
	validate_url(image_url)
	story = {"title": title, "caption": caption, "image_url": image_url}
	return story


def djot_text(value: str) -> str:
	"""Keep fetched text literal, ASCII-authored, and separate from Djot structure."""
	value = value.translate(str.maketrans({"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"'}))
	encoded = "".join(char if char.isascii() and (char.isalnum() or char == " ")
		else f"&#{ord(char)};" for char in value)
	return encoded


def weather_slide(story: dict[str, str], image_name: str, retrieved_on: datetime.date) -> str:
	"""Keep the forecast in the caption and its dated source in the citation footer."""
	slide = "=== layout: big-image\n\n@image\n\n"
	slide += f"![{djot_text(story['title'])}]({WEATHER_ASSET_PATH}{image_name})\n\n"
	slide += f"@caption\n\n{djot_text(story['caption'])}\n\n"
	date = retrieved_on.strftime("%b %d, %Y")
	slide += f"@citation\n\nNWS Chicago, retrieved {date}: {PAGE_URL}\n\n"
	return slide


def update_source(source: str, slide: str) -> str:
	"""Replace one managed weather slide and put it immediately before the icebreaker."""
	parts = re.split(r"(?m)(?=^===\s+(?:layout|include):)", source)
	if sum(WEATHER_ASSET_PATH in part for part in parts) > 1:
		raise ValueError("Multiple managed weather slides; resolve duplicates before refreshing")
	parts = [part for part in parts if WEATHER_ASSET_PATH not in part]
	anchors = [index for index, part in enumerate(parts) if re.search(
		r"(?im)^# .*\b(?:breakout room chat|ice[ -]?breaker)\b", part.split("@notes")[0])]
	if len(anchors) != 1:
		raise ValueError(f"Expected one icebreaker slide, found {len(anchors)}; decks unchanged")
	parts.insert(anchors[0], slide)
	return "".join(parts)


def announcement_paths(selectors: list[str]) -> list[pathlib.Path]:
	"""Select explicit announcement files or matching files below lecture folders."""
	paths = set()
	for selector in selectors:
		path = pathlib.Path(selector)
		if not path.exists():
			raise ValueError(f"Path does not exist: {path}")
		candidates = path.rglob("*.djot") if path.is_dir() else [path]
		matches = [item for item in candidates if re.match(r"lect\d+a[-_]", item.name)
			and "announcements" in item.stem and item.suffix == ".djot"]
		if not matches:
			raise ValueError(f"No lect##a announcement decks found: {path}")
		paths.update(item.resolve() for item in matches)
	return sorted(paths)


def refresh(paths: list[pathlib.Path], write: bool, retrieved_on: datetime.date) -> None:
	"""Validate the forecast and every insertion point before saving any selected deck."""
	story = weather_story(download(PAGE_URL, 2_000_000))
	image_data = download(story["image_url"], 10_000_000)
	with PIL.Image.open(io.BytesIO(image_data)) as image:
		if image.format != "PNG":
			raise ValueError("NWS weather graphic must be a PNG; decks unchanged")
		image.verify()
	# Immutable asset names keep other decks' earlier snapshots intact.
	image_name = f"chicago_{hashlib.sha256(image_data).hexdigest()}.png"
	slide = weather_slide(story, image_name, retrieved_on)
	updates = []
	for path in paths:
		source = path.read_text(encoding="utf-8")
		updated = update_source(source, slide)
		updates.append((path, updated))
		print(f"{path.name}: {story['title']} (retrieved {retrieved_on})")
		print("".join(difflib.unified_diff(source.splitlines(keepends=True),
			updated.splitlines(keepends=True), fromfile=str(path), tofile=str(path))), end="")
	if not write:
		print("Preview only. Run again with --write to save the weather story and graphic.")
		return
	for path, updated in updates:
		image_path = path.parent / WEATHER_ASSET_PATH / image_name
		image_path.parent.mkdir(parents=True, exist_ok=True)
		image_path.write_bytes(image_data)
		path.write_text(updated, encoding="utf-8")
		print(f"Updated {path}")


def parse_args() -> argparse.Namespace:
	"""Read announcement selectors and the explicit save flag."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("decks", nargs="+", help="lect##a Djot files or lecture folders")
	parser.add_argument("--write", action="store_true", help="save changes (default: show diff)")
	return parser.parse_args()


def main() -> None:
	"""Capture today's published weather story only when explicitly invoked."""
	args = parse_args()
	retrieved_on = datetime.datetime.now(zoneinfo.ZoneInfo("America/Chicago")).date()
	refresh(announcement_paths(args.decks), args.write, retrieved_on)


if __name__ == "__main__":
	main()
