"""Behavioral tests for the fast extended-Djot structural linter."""

# Standard Library
import pathlib

# Third-party modules
import pytest

# Local modules
import slide_lib.djot_lint
import slide_lib.djot_parser
import slide_lib.layout_content
import slide_lib.layout_engine
import slide_lib.presentation_theme


#============================================
def write_source(tmp_path: pathlib.Path, content: str) -> pathlib.Path:
	"""Write one small source deck with its referenced local component image."""
	deck = tmp_path / "deck"
	assets = deck / "assets"
	assets.mkdir(parents=True)
	(assets / "gene.png").write_bytes(b"source asset")
	path = deck / "lecture.djot"
	path.write_text(content, encoding="utf-8")
	return path


#============================================
def test_hidden_slide_still_checks_its_assets(tmp_path: pathlib.Path) -> None:
	"""Hiding a slide does not mask a missing source figure."""
	path = write_source(tmp_path,
		"=== layout: one-panel\nhidden: true\n@body\n![Figure](assets/missing.png)\n")
	problems, _summary = slide_lib.djot_lint.lint_paths([path])
	assert problems[0].message == "component image is missing: assets/missing.png"


#============================================
@pytest.mark.parametrize("prefix, suffix, slot", (
	("=== layout: one-panel\n\n@body\n\n", "", "body"),
	("=== layout: two-panels\n\n@left\n\n", "\n\n@right\n\nExplanation.\n", "left"),
	("=== layout: title-only\n\n# Results\n\n", "", "body"),
))
def test_lint_accepts_renderable_prose_table_flow(tmp_path: pathlib.Path,
		prefix: str, suffix: str, slot: str) -> None:
	"""Lint must accept the prose/table sequence used by editable chi-square slides."""
	body = "Hypothesis: a 9:3:3:1 ratio.\n\n"
	body += "| Class | Observed |\n| --- | --- |\n| A-B- | 91 |\n\n"
	body += "- Total offspring: 160\n"
	path = write_source(tmp_path, prefix + body + suffix)
	problems, _summary = slide_lib.djot_lint.lint_paths([path])
	assert problems == []
	deck = slide_lib.djot_parser.parse_deck(path)
	result = slide_lib.layout_engine.compile_layout_deck(
		deck, slide_lib.presentation_theme.default_theme())
	objects = [item for item in result.plan.slides[0].objects if item.slot_id == slot]
	assert [type(item.content) for item in objects] == [
		slide_lib.layout_content.TextContent, slide_lib.layout_content.TableContent,
		slide_lib.layout_content.TextContent]
	assert all(first.rectangle.y + first.rectangle.height <= second.rectangle.y
		for first, second in zip(objects, objects[1:]))


#============================================
def test_valid_two_panel_source_has_no_structural_problems(tmp_path: pathlib.Path) -> None:
	"""The linter accepts a documented layout, slot, and local-image arrangement."""
	path = write_source(
		tmp_path,
		"""=== layout: two-panels

# Genes

@left

- Chromosomes carry genes.

@right

![Chromosome](assets/gene.png)
""",
	)

	problems, summary = slide_lib.djot_lint.lint_paths([path])

	assert problems == []
	assert summary == slide_lib.djot_lint.LintSummary(1, 1, 1)


#============================================
def test_linter_reports_source_located_parser_failures(tmp_path: pathlib.Path) -> None:
	"""The semantic linter reports recognized deferred actions at their source line."""
	path = write_source(
		tmp_path,
		"""=== layout: one-panel

@body

<= blue overlay
""",
	)

	problems, _summary = slide_lib.djot_lint.lint_paths([path])
	problem = problems[0]

	assert problem.line == 5
	assert problem.message == "blue overlay is recognized but not yet supported"


#============================================
def test_linter_keeps_component_image_safety_after_semantic_parse(tmp_path: pathlib.Path) -> None:
	"""A parsed component image must still name an existing local asset."""
	path = write_source(
		tmp_path,
		"""=== layout: one-panel

# Genes

@body

![Chromosome](assets/missing.png)
""",
	)

	problems, _summary = slide_lib.djot_lint.lint_paths([path])

	assert problems[0].line == 7
	assert problems[0].message == "component image is missing: assets/missing.png"


#============================================
def test_linter_rejects_component_image_symlink_outside_deck_root(tmp_path: pathlib.Path) -> None:
	"""A local path cannot escape the parsed deck root through a symlink."""
	path = write_source(
		tmp_path,
		"""=== layout: one-panel

# Genes

@body

![Chromosome](assets/escape.png)
""",
	)
	outside = tmp_path / "outside.png"
	outside.write_bytes(b"outside asset")
	(path.parent / "assets" / "escape.png").symlink_to(outside)

	problems, _summary = slide_lib.djot_lint.lint_paths([path])

	assert problems[0].line == 7
	assert problems[0].message == "component image must be inside the repository: assets/escape.png"
