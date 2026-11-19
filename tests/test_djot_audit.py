"""Protect advisory typography detection without making lecture wording a test gate."""

import json
from unittest import mock

import slide_lib.cli
import slide_lib.native_export


def test_audit_cli_reports_source_and_keeps_warnings_advisory(tmp_path: object, capsys: object) -> None:
	"""A wrapping title is reported without changing source or failing the command."""
	path = tmp_path / "deck.djot"
	source = "=== layout: one-panel\n\n# " + "Linked genes and chromosomes " * 5
	source += "\n\n@body\n\nGenes.\n\n=== layout: one-panel\nhidden: true\n\n# "
	source += "Linked genes and chromosomes " * 5 + "\n\n@body\n\nGenes.\n"
	path.write_text(source, encoding="utf-8")
	with mock.patch.object(slide_lib.native_export, "find_repo_root", return_value=tmp_path):
		assert slide_lib.cli.main(["audit", str(path)]) == 0
	report = json.loads(capsys.readouterr().out)
	assert report["skipped"]["hidden-slides"] == 1
	finding = next(item for item in report["findings"] if item["check"] == "title-wrap")
	assert (finding["slide"], finding["source_line"]) == (1, 3)
	assert finding["file"] == str(path)
	assert len(finding["lines"]) > 1
	assert path.read_text(encoding="utf-8") == source
