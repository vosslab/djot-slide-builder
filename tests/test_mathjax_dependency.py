"""Prevent the repeatedly reintroduced older MathJax dependency requirement."""

import json
import pathlib


def test_mathjax_requirement_preserves_instructor_minimum() -> None:
	root = pathlib.Path(__file__).resolve().parents[1]
	manifest = json.loads((root / "package.json").read_text(encoding="utf-8"))
	lock = json.loads((root / "package-lock.json").read_text(encoding="utf-8"))
	assert manifest["dependencies"]["@mathjax/src"] == ">=4.1.3", (
		"Keep the instructor-required MathJax floor; do not restore ^4.0.0."
	)
	assert lock["packages"][""]["dependencies"]["@mathjax/src"] == ">=4.1.3", (
		"Regenerate package-lock.json from the required manifest before committing."
	)


def test_xmldom_override_excludes_vulnerable_versions() -> None:
	root = pathlib.Path(__file__).resolve().parents[1]
	manifest = json.loads((root / "package.json").read_text(encoding="utf-8"))
	assert manifest["overrides"]["@xmldom/xmldom"] == ">=0.9.12", (
		"Exclude vulnerable xmldom versions across the entire dependency tree."
	)
