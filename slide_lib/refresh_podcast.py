"""Preview or refresh the Stump the Vibe Coder slide in announcement decks."""

# Standard Library
import argparse
import datetime
import difflib
import io
import pathlib
import random
import re
import tempfile
import time
import urllib.error
import urllib.request
import urllib.parse
import zoneinfo

# Third-Party Modules
import lxml.etree
import PIL.Image

import slide_lib.djot_sources

PLAYLIST_ID = "PL5LJPD9b2pRYsw2sU3LRCDhvDSiZ26E48"
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?playlist_id={PLAYLIST_ID}"
PODCAST_ASSET_PATH = "assets/stump_the_vibe_coder/"
PODCAST_SLIDE_PATH = "shared/stump_the_vibe_coder/"
PODCAST_INCLUDE = f"=== include: repo:{PODCAST_SLIDE_PATH}"
NAMESPACES = {"atom": "http://www.w3.org/2005/Atom",
	"yt": "http://www.youtube.com/xml/schemas/2015",
	"media": "http://search.yahoo.com/mrss/"}


#============================================
def download(url: str, limit: int) -> bytes:
	"""Read a bounded public YouTube resource with a network timeout."""
	parsed = urllib.parse.urlsplit(url)
	# ASVS 13.2.4: permit only the public feed and thumbnail service hosts.
	if parsed.scheme != "https" or parsed.hostname not in {"www.youtube.com", "i.ytimg.com"}:
		raise ValueError(f"Expected an allowed YouTube HTTPS URL: {url}")
	time.sleep(random.random())
	request = urllib.request.Request(url, headers={"User-Agent": "djot-slide-builder/1.0"})
	with urllib.request.urlopen(request, timeout=30) as response:  # nosec B310
		data = response.read(limit + 1)
	if len(data) > limit:
		raise ValueError(f"Resource exceeds {limit} bytes: {url}")
	return data


#============================================
def latest_episode(data: bytes, on_date: datetime.date | None = None) -> dict[str, str]:
	"""Select the most recently published regular episode in the recent playlist feed."""
	parser = lxml.etree.XMLParser(resolve_entities=False, load_dtd=False, no_network=True)
	root = lxml.etree.fromstring(data, parser=parser)
	if root.getroottree().docinfo.doctype:
		raise ValueError("Playlist feed must not contain a DTD")
	entries = root.findall("atom:entry", NAMESPACES)
	entries = [entry for entry in entries if not re.search(r"\bspecial\b",
		entry.findtext("atom:title", namespaces=NAMESPACES) or "", re.IGNORECASE)]
	if on_date is not None:
		entries = [entry for entry in entries if datetime.datetime.fromisoformat(
			entry.findtext("atom:published", namespaces=NAMESPACES)).astimezone(
				zoneinfo.ZoneInfo("America/Chicago")).date() <= on_date]
	if not entries:
		raise ValueError("No eligible public episodes in the recent playlist feed; "
			"historical coverage may be insufficient. Decks were not changed")
	entry = max(entries, key=lambda item: datetime.datetime.fromisoformat(
		item.findtext("atom:published", namespaces=NAMESPACES)))
	video_id = entry.findtext("yt:videoId", namespaces=NAMESPACES)
	# ASVS 1.2.2: fixed HTTPS origins and validated IDs form URLs and local filenames.
	if not video_id or not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
		raise ValueError("Invalid YouTube video ID in playlist feed")
	title = entry.findtext("atom:title", namespaces=NAMESPACES)
	if not title or not title.strip():
		raise ValueError("Episode has no title")
	episode = {"id": video_id, "title": " ".join(title.split()),
		"published": entry.findtext("atom:published", namespaces=NAMESPACES),
		"project_url": project_url(entry.findtext(
			"media:group/media:description", namespaces=NAMESPACES) or "")}
	return episode


def project_url(description: str) -> str:
	"""Require one published GitHub Pages destination, never a repository URL."""
	url_pattern = r"https://[A-Za-z0-9-]+\.github\.io(?:/[^\s<>\"\)]*)?"
	projects = re.findall(rf"(?mi)^Project:[ \t]*({url_pattern})[ \t]*$", description)
	urls = set(projects or re.findall(url_pattern, description))
	if len(urls) != 1:
		raise ValueError("Expected one GitHub Pages project URL in the episode description; "
			"decks were not changed")
	return urls.pop()


def lecture_date(source: str) -> datetime.date:
	"""Read the lecture date from the cover, not deadlines in later slides."""
	parts = re.split(r"(?m)(?=^===\s+layout:)", source)
	cover = next(part for part in parts if part.startswith("=== layout:"))
	dates = re.findall(r"(?m)^##\s+([A-Za-z]+ \d{1,2}, \d{4})\s*$", cover)
	if len(dates) != 1:
		raise ValueError("Expected exactly one lecture date on the cover")
	month, day, year = dates[0].replace(",", "").split()
	months = ("jan", "feb", "mar", "apr", "may", "jun",
		"jul", "aug", "sep", "oct", "nov", "dec")
	return datetime.date(int(year), months.index(month[:3].lower()) + 1, int(day))


#============================================
def djot_text(text: str) -> str:
	"""Encode title punctuation and Unicode as literal Djot character references."""
	# Encode at the output boundary so feed text cannot introduce Djot structure.
	encoded = "".join(char if char.isascii() and (char.isalnum() or char == " ")
		else f"&#{ord(char)};" for char in text)
	return encoded


#============================================
def podcast_slide(episode: dict[str, str]) -> str:
	"""Keep the episode title and visible clickable URL editable beneath its thumbnail."""
	title = djot_text(episode["title"])
	caption = re.sub(r"^(?:StVC\s+|Stump the Vibe Coder,\s*Episode\s+)(\d+)",
		r"Stump the Vibe Coder #\1",
		episode["title"].split(" | Stump the Vibe Coder")[0])
	caption = djot_text(caption)
	video_id = episode["id"]
	video_label = f"https://www.youtube.com/watch?v={video_id}".replace("_", "&#95;")
	slide = "=== layout: big-image\n\n@image\n\n"
	slide += f"![{title}](repo:shared/{PODCAST_ASSET_PATH}{video_id}.webp)\n\n"
	slide += f"@caption\n\n{caption}\\\n"
	slide += f"Watch the Video: [{video_label}](https://www.youtube.com/watch?v={video_id})\\\n"
	slide += f"Play the Game: {episode['project_url']}\n\n"
	return slide


#============================================
def update_source(source: str, episode: dict[str, str]) -> str:
	"""Replace the managed slide and insert it directly after the YouTube channel slide."""
	parts = re.split(r"(?m)(?=^===\s+(?:layout|include):)", source)
	managed = [part for part in parts if part.startswith(PODCAST_INCLUDE) or PODCAST_ASSET_PATH in part]
	if len(managed) > 1:
		raise ValueError("Multiple managed podcast slides; resolve duplicates before refreshing")
	parts = [part for part in parts if part not in managed]
	anchors = [index for index, part in enumerate(parts)
		if re.search(r"youtube", re.split(r"(?m)^@speaker-notes\r?$", part, maxsplit=1)[0], re.IGNORECASE)]
	if len(anchors) != 1:
		raise ValueError(f"Expected one YouTube channel slide, found {len(anchors)}; deck unchanged")
	index = anchors[0]
	parts[index] = parts[index].rstrip() + "\n\n"
	parts.insert(index + 1, f"{PODCAST_INCLUDE}{episode['id']}.djot\n\n")
	return "".join(parts)


#============================================
def announcement_paths(selectors: list[str]) -> list[pathlib.Path]:
	"""Accept specific announcement files or lecture folders, across either course."""
	paths = set()
	for selector in selectors:
		path = pathlib.Path(selector)
		if not path.exists():
			raise ValueError(f"Path does not exist: {path}")
		candidates = path.rglob("*.djot") if path.is_dir() else [path]
		matches = [item for item in candidates
			if re.match(r"lect\d+a[-_]", item.name) and "announcements" in item.stem
			and item.suffix == ".djot"]
		if not matches:
			raise ValueError(f"No lect##a announcement decks found: {path}")
		paths.update(item.resolve() for item in matches)
	return sorted(paths)


#============================================
def thumbnail(video_id: str) -> bytes:
	"""Save the full-size or standard YouTube thumbnail as a shared WebP."""
	url = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
	try:
		data = download(url, 10_000_000)
	except urllib.error.HTTPError as error:
		if error.code != 404:
			raise
		data = download(f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg", 10_000_000)
	with PIL.Image.open(io.BytesIO(data)) as image:
		# ASVS 5.2.2, 5.2.6: verify the type and limit dimensions before decoding pixels.
		if image.format != "JPEG" or image.width > 1280 or image.height > 720:
			raise ValueError("Episode thumbnail must be a JPEG no larger than 1280 x 720")
		webp = io.BytesIO()
		image.save(webp, format="WEBP", quality=90)
	return webp.getvalue()


#============================================
def save(path: pathlib.Path, data: bytes) -> None:
	"""Publish complete files for other decks using the same episode."""
	path.parent.mkdir(parents=True, exist_ok=True)
	with tempfile.TemporaryDirectory(dir=path.parent) as directory:
		staged = pathlib.Path(directory) / path.name
		staged.write_bytes(data)
		staged.replace(path)


#============================================
def main() -> None:
	"""Preview by default, or save the fetched episode to explicitly selected decks."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("decks", nargs="+", help="lect##a Djot files or lecture folders")
	parser.add_argument("--write", action="store_true", help="save changes (default: show diff)")
	parser.add_argument("--by-lecture-date", action="store_true",
		help="select the latest episode published by each cover date (America/Chicago)")
	args = parser.parse_args()
	paths = announcement_paths(args.decks)
	data = download(FEED_URL, 2_000_000)
	updates = []
	shared = {}
	# Validate every anchor before writing any files.
	for path in paths:
		source = path.read_text(encoding="utf-8")
		on_date = lecture_date(source) if args.by_lecture_date else None
		episode = latest_episode(data, on_date)
		print(f"{path.name}: {on_date or 'latest'}: {episode['title']} ({episode['published']})")
		updated = update_source(source, episode)
		if updated != source:
			updates.append((path, updated))
		video_id = episode["id"]
		root = slide_lib.djot_sources.repository_root(path)
		# ASVS 5.3.2: feed IDs are validated before use and resolved paths stay in this checkout.
		slide_path = (root / PODCAST_SLIDE_PATH / f"{video_id}.djot").resolve()
		image_path = (root / "shared" / PODCAST_ASSET_PATH / f"{video_id}.webp").resolve()
		if not path.is_relative_to(root) or not all(
				saved.is_relative_to(root) for saved in (slide_path, image_path)):
			raise ValueError("Episode files and announcement deck must stay in the same repository")
		shared[slide_path] = (image_path, episode)
		print("".join(difflib.unified_diff(source.splitlines(keepends=True),
			updated.splitlines(keepends=True), fromfile=str(path), tofile=str(path))), end="")
	if not args.write:
		print("Preview only. Run again with --write to save the episode and thumbnail.")
		return
	# Fetch every required image before mutating any deck; reuse shared episodes.
	video_ids = {episode["id"] for _, episode in shared.values()}
	thumbnails = {video_id: thumbnail(video_id) for video_id in video_ids}
	for slide_path, (image_path, episode) in shared.items():
		save(image_path, thumbnails[episode["id"]])
		if not slide_path.exists():
			save(slide_path, podcast_slide(episode).encode("utf-8"))
		print(f"Refreshed {image_path}")
	for path, updated in updates:
		save(path, updated.encode("utf-8"))
		print(f"Updated {path}")


if __name__ == "__main__":
	main()
