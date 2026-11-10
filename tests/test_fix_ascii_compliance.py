"""Keep ASCII cleanup from corrupting XML-based artwork."""

# Standard Library
import sys
import pathlib
import defusedxml.ElementTree

# Third-Party Modules
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
	path.write_bytes(f'<svg label="{label}">\r\n<text>{label}</text>\r\n</svg>'.encode("utf-8"))
	monkeypatch.setattr(sys, "argv", ["fix_ascii_compliance.py", "-i", str(path)])
	assert fix_ascii_compliance.main() == 2
	output = path.read_bytes()
	assert output.isascii() and b"\r" not in output
	root = defusedxml.ElementTree.fromstring(output)
	assert root.attrib["label"] == root.find("text").text == "\u03b1 & < \u03b2\u00b2"
	assert fix_ascii_compliance.main() == 0


#============================================
def test_djot_cleanup_retains_named_entities(
	tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
	"""Djot keeps the established HTML entity replacements."""
	path = tmp_path / "labels.djot"
	path.write_text("\u03b1 &alpha;\n", encoding="utf-8")
	monkeypatch.setattr(sys, "argv", ["fix_ascii_compliance.py", "-i", str(path)])
	assert fix_ascii_compliance.main() == 2
	assert path.read_text(encoding="ascii") == "&alpha; &alpha;\n"
