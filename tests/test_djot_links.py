"""Validate Djot component assets without requiring they be Git-tracked."""

import pathlib

import pytest

import file_utils
import slide_lib.djot_lint
import slide_lib.djot_sources


REPORT_NAME = file_utils.report_name(__file__)
FILES = [str(path) for path in slide_lib.djot_sources.root_sources([
	pathlib.Path(path) for path in file_utils.discover_files(
		extensions=(".djot",), test_key="djot_links")])]
VIOLATIONS_BY_FILE: dict[str, list[str]] = {}


#============================================
def check_file(relative_path: str) -> list[str]:
	"""Use the slide resolver so ignored local assets remain supported."""
	path = pathlib.Path(file_utils.get_repo_root()) / relative_path
	problems, _slides, _images = slide_lib.djot_lint.lint_source(path)
	return [f"{problem.path}:{problem.line}: {problem.message}" for problem in problems]


#============================================
@pytest.fixture(scope="module", autouse=True)
def collect_report() -> None:
	"""Write one actionable report before parametrized assertions run."""
	file_utils.clear_stale_reports()
	VIOLATIONS_BY_FILE.clear()
	VIOLATIONS_BY_FILE.update(file_utils.collect_file_violations(FILES, check_file))
	lines = file_utils.format_violation_report("Djot link errors detected:", VIOLATIONS_BY_FILE)
	if lines:
		file_utils.write_report_lines(REPORT_NAME, lines)


#============================================
@pytest.mark.parametrize("path", FILES, ids=file_utils.rel_id)
def test_djot_links(path: str) -> None:
	"""Djot assets exist locally and satisfy the resolver's containment rules."""
	rel = file_utils.rel_to_root(path)
	assert rel not in VIOLATIONS_BY_FILE, file_utils.format_violation_assert_message(
		rel, VIOLATIONS_BY_FILE.get(rel, []), REPORT_NAME)
