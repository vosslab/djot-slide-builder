"""Behavioral tests for the fast extended-Djot structural linter."""

# Standard Library
import pathlib

# Local modules
import slide_lib.djot_lint


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
