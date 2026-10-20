"""Resolve private course URLs only when a deck references them."""

import pathlib
import re
import urllib.parse

import yaml


TOKEN = re.compile(r"\{\{course_url:([a-z][a-z0-9_]*)\}\}")
CONFIG_PATH = pathlib.Path(__file__).resolve().parent.parent / "course_links.local.yaml"


#============================================
def expand(text: str, course: str, config_path: pathlib.Path = CONFIG_PATH) -> str:
	"""Insert validated URLs without changing physical source line numbers."""
	if "{{course_url:" not in text:
		return text
	if not config_path.is_file():
		raise ValueError(f"Missing {config_path.name}; configure local course URLs before building")
	config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
	if not isinstance(config, dict):
		raise ValueError(f"{config_path.name} must contain course mappings")
	links = config.get(course, {})
	if not isinstance(links, dict):
		raise ValueError(f"{config_path.name}: {course} must be a mapping")

	def replace(match: re.Match) -> str:
		key = match.group(1)
		if key not in links:
			raise ValueError(f"{config_path.name}: missing {course}.{key}")
		url = links[key]
		# ASVS 1.1.2: reject Djot delimiters before inserting a bare URL;
		# the existing inline parser and XML writer own final output escaping.
		if (not isinstance(url, str) or not url.startswith("https://") or
				any(char.isspace() or char in '<>()[]{}*`\\"' for char in url)):
			raise ValueError(f"{config_path.name}: {course}.{key} needs a plain HTTPS URL")
		if not urllib.parse.urlsplit(url).hostname:
			raise ValueError(f"{config_path.name}: {course}.{key} needs a URL host")
		return url

	result = TOKEN.sub(replace, text)
	if "{{course_url:" in result:
		raise ValueError("Malformed course URL reference; use {{course_url:key}}")
	return result
