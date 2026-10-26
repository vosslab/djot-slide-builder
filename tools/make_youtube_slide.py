#!/usr/bin/env python3
"""Generate one local big-image Djot slide from a YouTube video."""

# Standard Library
import re
import sys
import time
import json
import random
import pathlib
import argparse
import tempfile
import subprocess
import urllib.parse

# Third-Party Modules
import PIL.Image


#============================================
def video_id(value: str) -> str:
	"""Accept a bare ID or one supported public YouTube video URL."""
	value = value.strip()
	if re.fullmatch(r"[A-Za-z0-9_-]{11}", value):
		return value
	url = urllib.parse.urlsplit(value)
	candidate = ""
	if url.scheme in ("http", "https"):
		if url.netloc.lower() == "youtu.be":
			candidate = url.path.removeprefix("/")
		elif url.netloc.lower() in ("youtube.com", "www.youtube.com", "m.youtube.com"):
			if url.path == "/watch":
				query = urllib.parse.parse_qs(url.query)
				values = query.get("v", [])
				if len(values) == 1:
					candidate = values[0]
	if not re.fullmatch(r"[A-Za-z0-9_-]{11}", candidate):
		raise ValueError("Expected a YouTube video ID, youtu.be URL, or YouTube watch URL")
	return candidate


#============================================
def literal_title(title: str) -> str:
	"""Keep fetched punctuation and Unicode literal in Djot captions and alt text."""
	result = "".join(char if char.isascii() and (char.isalnum() or char == " ")
		else f"&#{ord(char)};" for char in title)
	return result


#============================================
def slide_source(identifier: str, title: str) -> str:
	"""Emit ordinary offline Djot with editable title and full clickable URL."""
	escaped = literal_title(title)
	url = f"https://www.youtube.com/watch?v={identifier}"
	source = "=== layout: big-image\n\n@image\n\n"
	source += f"![{escaped}](assets/youtube/{identifier}.png)\n\n"
	source += f"@caption\n\n{escaped}\n\n[{url}]({url})\n\n"
	return source


#============================================
def generate_slide(identifier: str, output: pathlib.Path) -> None:
	"""Fetch and validate all inputs before publishing the PNG and slide fragment."""
	if output.suffix != ".djot":
		raise ValueError("Output must be a .djot slide fragment beside the master deck")
	repo_root = pathlib.Path(subprocess.check_output(
		["git", "rev-parse", "--show-toplevel"], text=True).strip())
	scratch = repo_root / "_temp"
	scratch.mkdir(exist_ok=True)
	with tempfile.TemporaryDirectory(prefix="youtube_slide_", dir=scratch) as directory:
		staging = pathlib.Path(directory)
		url = f"https://www.youtube.com/watch?v={identifier}"
		# Ignore user download settings and fetch no audio or video.
		time.sleep(random.random())
		subprocess.run([
			sys.executable, "-m", "yt_dlp", "--ignore-config", "--no-cache-dir",
			"--skip-download", "--write-thumbnail", "--write-info-json", "--no-playlist",
			"-o", str(staging / "%(id)s.%(ext)s"), url,
		], check=True)
		info_path = staging / f"{identifier}.info.json"
		metadata = json.loads(info_path.read_text(encoding="utf-8"))
		if metadata["id"] != identifier:
			raise ValueError("YouTube metadata does not match the requested video")
		title = " ".join(metadata["title"].split())
		if not title:
			raise ValueError("YouTube video has no title")
		thumbnails = [path for path in staging.glob(f"{identifier}.*") if path != info_path]
		if len(thumbnails) != 1:
			raise ValueError("Expected one downloaded YouTube thumbnail")
		# Pillow validates the downloaded image and normalizes WebP/JPEG to portable PNG.
		png_path = staging / "thumbnail.png"
		with PIL.Image.open(thumbnails[0]) as thumbnail:
			thumbnail.convert("RGB").save(png_path, format="PNG")
		source_path = staging / "slide.djot"
		source_path.write_text(slide_source(identifier, title), encoding="utf-8")
		image_path = output.parent / "assets" / "youtube" / f"{identifier}.png"
		image_path.parent.mkdir(parents=True, exist_ok=True)
		png_path.replace(image_path)
		source_path.replace(output)
	print(f"Generated {output}: {title}")


#============================================
def parse_args() -> argparse.Namespace:
	"""Read the video and explicit slide destination."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("-v", "--video", dest="video", required=True,
		help="YouTube video ID, watch URL, or youtu.be URL")
	parser.add_argument("-o", "--output", dest="output", required=True, type=pathlib.Path,
		help=".djot fragment beside its master deck (replaced on regeneration)")
	return parser.parse_args()


#============================================
def main() -> None:
	"""Generate a saved slide for explicit inclusion in a lecture."""
	args = parse_args()
	generate_slide(video_id(args.video), args.output)


if __name__ == "__main__":
	main()
