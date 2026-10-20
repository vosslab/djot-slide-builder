"""Protect local-link resolution and failures without real course URLs."""

import pytest

import slide_lib.course_links


def test_local_links_preserve_source_and_resolve_by_course(tmp_path):
	config = tmp_path / 'links.yaml'
	config.write_text('genetics:\n  discord: https://example.org/join?a=1&b=2\n')
	text = '# Discord Server\n- {{course_url:discord}}\n'
	result = slide_lib.course_links.expand(text, 'genetics', config)
	assert result == '# Discord Server\n- https://example.org/join?a=1&b=2\n'
	assert slide_lib.course_links.expand('# No links', 'genetics', tmp_path / 'absent') == '# No links'
	with pytest.raises(ValueError, match='Missing'):
		slide_lib.course_links.expand(text, 'genetics', tmp_path / 'absent')
	with pytest.raises(ValueError, match='missing biotechnology.discord'):
		slide_lib.course_links.expand(text, 'biotechnology', config)


@pytest.mark.parametrize('url', ['javascript:alert(1)', 'https://example.org/[bad]', 'https://'])
def test_invalid_local_url_is_rejected(tmp_path, url):
	config = tmp_path / 'links.yaml'
	config.write_text(f'genetics:\n  discord: "{url}"\n')
	with pytest.raises(ValueError):
		slide_lib.course_links.expand('{{course_url:discord}}', 'genetics', config)
