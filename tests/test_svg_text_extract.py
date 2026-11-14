"""Read real SVG files without claiming to recognize outlined text."""

import pytest
import defusedxml.common

import svg_tools.text


def test_extract_live_text_and_report_candidates(tmp_path):
	path = tmp_path / 'figure.svg'
	path.write_text('<svg xmlns="http://www.w3.org/2000/svg"><text id="gene" x="4" y="5">'
		'BRCA<tspan>1</tspan></text><image/><path d="M0 0"/></svg>')
	result = svg_tools.text.extract_text(path)
	assert result.labels == (svg_tools.text.ExtractedLabel('BRCA1', '4', '5', 'gene'),)
	assert '1 image(s) and 1 path(s)' in result.unavailable
	path.write_text('<!DOCTYPE svg [<!ENTITY x "bad">]><svg><text>&x;</text></svg>')
	with pytest.raises(defusedxml.common.EntitiesForbidden):
		svg_tools.text.extract_text(path)
