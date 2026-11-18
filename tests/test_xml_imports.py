"""Enforce lxml as the shared XML object model."""

# Standard Library
import ast

# Third-Party Modules
import pytest

# Local Modules
import file_utils


FILES = file_utils.discover_files(extensions=(".py",), test_key="xml_imports")
REPORT_NAME = file_utils.report_name(__file__)
VIOLATIONS_BY_FILE: dict[str, list[str]] = {}


#============================================
def check_file(rel: str, tree: ast.Module) -> list[str]:
	"""Find imports of alternate XML tree libraries, including aliased imports."""
	issues = []
	for node in file_utils.iter_imports(tree):
		prefix = ""
		if isinstance(node, ast.ImportFrom):
			if node.level:
				continue
			prefix = f"{node.module}."
		for alias in node.names:
			module = prefix + alias.name
			if (module + ".").startswith(("defusedxml.", "xml.etree.")):
				issues.append(f"{rel}:{node.lineno}: replace {module} with lxml.etree")
	return issues


#============================================
@pytest.fixture(scope="module", autouse=True)
def collect_report() -> None:
	"""Scan tracked Python once and write a report if legacy imports return."""
	file_utils.clear_stale_reports()
	VIOLATIONS_BY_FILE.clear()
	VIOLATIONS_BY_FILE.update(file_utils.collect_python_violations(FILES, check_file))
	lines = file_utils.format_violation_report("XML import violations:", VIOLATIONS_BY_FILE)
	if lines:
		file_utils.write_report_lines(REPORT_NAME, lines)


#============================================
@pytest.mark.parametrize("path", FILES, ids=file_utils.rel_id)
def test_xml_imports(path: str) -> None:
	"""Keep tracked Python on the shared XML object model."""
	rel = file_utils.rel_to_root(path)
	assert rel not in VIOLATIONS_BY_FILE, file_utils.format_violation_assert_message(
		rel, VIOLATIONS_BY_FILE.get(rel, []), REPORT_NAME
	)
