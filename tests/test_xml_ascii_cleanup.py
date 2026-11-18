"""Keep ASCII cleanup from corrupting XML-based artwork."""

# Standard Library
import pathlib
import sys

# Third-Party Modules
import lxml.etree
import pytest

# Local Modules
import fix_ascii_compliance


#============================================
@pytest.mark.parametrize("suffix", (".svg", ".xml"))
def test_xml_cleanup_preserves_text_and_attributes(
	tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch, suffix: str,
) -> None:
	"""Numeric references preserve scientific labels and existing XML escapes."""
	path = tmp_path / f"labels{suffix}"
	label = "\u03b1 &amp; &lt; \u03b2\u00b2"
	path.write_text(f'<svg label="{label}"><text>{label}</text></svg>', encoding="utf-8")
	monkeypatch.setattr(sys, "argv", ["fix_ascii_compliance.py", "-i", str(path)])
	assert fix_ascii_compliance.main() == 2
	output = path.read_bytes()
	assert output.isascii()
	root = lxml.etree.fromstring(output)
	assert root.attrib["label"] == root.find("text").text == "\u03b1 & < \u03b2\u00b2"
