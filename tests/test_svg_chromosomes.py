"""Stable ordering, geometry and composition contracts for chromosome fragments."""

import re
import math
import pathlib
import xml.etree.ElementTree

import pytest

import svg_tools.chromosomes


#============================================
def test_explicit_allele_typography() -> None:
	"""Allele mode keeps empty arms and live italic genes with raised readable signs."""
	genes = [("", "#C1E7EE"), ("a+", "#D9C9EF"), ("b-", "#C1E7EE")]
	fragment, width, boundaries = svg_tools.chromosomes.chromosome_svg(
		"alleles", genes, centromere_after=1, allele_labels=True)
	labels = xml.etree.ElementTree.fromstring(fragment).findall(".//text")
	assert ["".join(node.itertext()) for node in labels] == ["", "a+", "b\u2212"]
	for label in labels[1:]:
		assert label[0].attrib["font-style"] == "italic"
		assert float(label[1].attrib["dy"]) < 0
	assert fragment.isascii()
	plain, plain_width, plain_boundaries = svg_tools.chromosomes.chromosome_svg(
		"alleles", genes, centromere_after=1)
	assert (width, boundaries) == (plain_width, plain_boundaries)
	assert xml.etree.ElementTree.fromstring(plain).findall(".//text")[2].text == "b-"
	for invalid in ("A+", "abc-", "a", "a++"):
		with pytest.raises(ValueError, match="Allele labels"):
			svg_tools.chromosomes.chromosome_svg("bad", [(invalid, "#FFFFFF")], allele_labels=True)


#============================================
def test_order_locus_and_composition() -> None:
	"""Deletion changes length; collars, joins and unique local refs stay distinct."""
	parts = []
	widths = []
	for name, sequence, centromere, joins in (
		("before", "ABCDEFGH", 5, ()), ("after", "ABCEFGH", 4, (3,)),
	):
		fragment, width, boundaries = svg_tools.chromosomes.chromosome_svg(
			name, [(letter, "#B48CDE" if letter == "D" else "#D9C9EF")
				for letter in sequence],
			centromere_after=centromere, junctions=joins)
		root = xml.etree.ElementTree.fromstring(fragment)
		assert "".join(node.text for node in root.iter("text")) == sequence
		assert all(a < b for a, b in zip(boundaries, boundaries[1:]))
		assert len(boundaries) == len(sequence) + 1
		assert root.find(f".//*[@id='{name}-centromere']") is not None
		labels = root.findall(".//text")
		assert float(labels[centromere-1].attrib["x"]) < boundaries[centromere]
		assert float(labels[centromere].attrib["x"]) > boundaries[centromere]
		parts.append(fragment)
		widths.append(width)
	assert widths[0] > widths[1]
	root = xml.etree.ElementTree.fromstring("<svg>" + "".join(parts) + "</svg>")
	ids = [node.attrib["id"] for node in root.iter() if "id" in node.attrib]
	assert len(ids) == len(set(ids))
	for node in root.iter():
		if "clip-path" in node.attrib:
			assert node.attrib["clip-path"][5:-1] in ids
	assert root.find(".//*[@id='after-join-3']") is not None
	assert root.find(".//*[@id='before-join-5']") is None
	assert root.find(".//*[@id='before-region-3']/rect").attrib["fill"] == "#B48CDE"


#============================================
def test_explicit_absence_and_escaped_labels() -> None:
	"""Unlabeled and special-character labels compose as ordinary live XML text."""
	fragment, _, _ = svg_tools.chromosomes.chromosome_svg(
		"plain", [("", "#FFFFFF"), ("A&B<\u03b1", "#FFFFFF")])
	root = xml.etree.ElementTree.fromstring(fragment)
	assert root.findall(".//text")[1].text == "A&B<\u03b1"
	assert root.find(".//*[@id='plain-centromere']") is None
	assert fragment.isascii()


#============================================
def test_invalid_geometry_and_boundaries() -> None:
	"""Reject nonfinite geometry and ambiguous topology rather than drawing it."""
	genes = [("A", "#FFFFFF"), ("B", "#FFFFFF")]
	for kwargs in ({"pitch": 0}, {"height": -1}, {"pitch": math.inf},
		{"height": math.nan}, {"centromere_after": 0}, {"junctions": (2,)},
		{"centromere_after": 1, "junctions": (1,)}, {"junctions": (1, 1)}):
		with pytest.raises(ValueError):
			svg_tools.chromosomes.chromosome_svg("bad", genes, **kwargs)
	with pytest.raises(ValueError):
		svg_tools.chromosomes.chromosome_svg("bad id", genes)
	with pytest.raises(ValueError):
		svg_tools.chromosomes.chromosome_svg("empty", [])
	with pytest.raises(ValueError):
		svg_tools.chromosomes.chromosome_svg("bad-fill", [("A", "url(external)")])


#============================================
def test_immutable_segments_and_bounded_rearrangements() -> None:
	"""Deletion and exchange preserve ancestry, unequal lengths and centromere location."""
	c = svg_tools.chromosomes
	segments = tuple(c.Segment(letter, '#D9C9EF', 35 + 9 * i, i % 5)
		for i, letter in enumerate('ABCDEFG'))
	parent = c.Chromosome(list(segments), 3)
	assert parent.segments == segments
	with pytest.raises(AttributeError):
		segments[0].length = 99
	with pytest.raises(AttributeError):
		parent.centromere_after = 2
	left_deleted = c.delete_segments(parent, 1, 3)
	right_deleted = c.delete_segments(parent, 3, 5)
	assert left_deleted.centromere_after == 1
	assert right_deleted.centromere_after == 3
	assert all(actual is expected for actual, expected in zip(left_deleted.segments, segments[:1] + segments[3:]))
	assert all(actual is expected for actual, expected in zip(right_deleted.segments, segments[:3] + segments[5:]))
	before_width = c.render_chromosome('before', parent)[1]
	after_width = c.render_chromosome('after', left_deleted)[1]
	assert before_width - after_width == pytest.approx(sum(s.length for s in segments[1:3]))
	for start, stop in ((0, 2), (2, 4), (1, 7), (3, 3), (True, 2)):
		with pytest.raises(ValueError):
			c.delete_segments(parent, start, stop)
	donor_segments = tuple(c.Segment(letter, '#00775F', 50 + i * 13, (i + 2) % 5)
		for i, letter in enumerate('WXYZ'))
	donor = c.Chromosome(donor_segments, 1)
	first, second = c.reciprocal_translocation(parent, 5, donor, 2)
	assert (first.centromere_after, second.centromere_after) == (3, 1)
	assert first.segments == segments[:5] + donor_segments[2:]
	assert second.segments == donor_segments[:2] + segments[5:]
	assert sorted(map(id, first.segments + second.segments)) == sorted(map(id, segments + donor_segments))
	for cut in (True, 3, 7):
		with pytest.raises(ValueError):
			c.reciprocal_translocation(parent, cut, donor, 2)
	with pytest.raises(ValueError):
		c.reciprocal_translocation(c.Chromosome(segments), 5, donor, 2)
	assert parent.segments == segments and parent.centromere_after == 3


#============================================
def test_segment_validation_and_plain_scaling() -> None:
	"""Invalid model data cannot enter SVG; plain caps retain requested fill at any width."""
	c = svg_tools.chromosomes
	for kwargs in ({'length': 0}, {'length': math.inf}, {'length': True}, {'band': -1}, {'band': 5}, {'band': True}):
		with pytest.raises(ValueError):
			c.Segment('A', '#FFFFFF', **kwargs)
	for label, color in (('A', 'url(external)'), ('A\x00', '#FFFFFF')):
		with pytest.raises(ValueError):
			c.Segment(label, color)
	segment = c.Segment('', '#00775F')
	for centromere in (True, 0, 1):
		with pytest.raises(ValueError):
			c.Chromosome((segment,), centromere)
	with pytest.raises(ValueError):
		c.Chromosome((c.Segment('', '#FFFFFF', 1e308),) * 2)
	rod = c.Chromosome((segment,))
	fragment, width, boundaries = c.render_chromosome('plain', rod, width=300, height=50, bands=False)
	root = xml.etree.ElementTree.fromstring(fragment)
	assert width == 300 and 0 < boundaries[0] < boundaries[1] < width
	assert {node.attrib['fill'] for node in root.iter() if 'fill' in node.attrib and node.tag != 'text'} == {'#00775F', 'none'}
	assert not root.findall('.//g/path[@stroke-opacity]')
	for kwargs in ({'width': math.nan}, {'height': True}, {'sisters': True}):
		with pytest.raises(ValueError):
			c.render_chromosome('bad', rod, **kwargs)


#============================================
def test_sisters_duplicate_content_with_local_ids_and_one_attachment() -> None:
	"""Joined sisters conserve ordered colors/bands, fit their envelope and compose safely."""
	c = svg_tools.chromosomes
	parent = c.Chromosome(tuple(c.Segment(letter, color, length, band)
		for letter, color, length, band in (
			('A', '#D9C9EF', 72, 4), ('B', '#D9C9EF', 94, 1),
			('C', '#00775F', 60, 3), ('D', '#C1E7EE', 86, 2))), 2)
	fragment, width, boundaries = c.render_chromosome('pair', parent, width=520, height=100, sisters=True)
	root = xml.etree.ElementTree.fromstring(fragment)
	assert width == 520 and all(0 < x < width for x in boundaries)
	assert [node.text for node in root.findall('.//text')] == list('ABCDABCD')
	ids = [node.attrib['id'] for node in root.iter() if 'id' in node.attrib]
	assert len(ids) == len(set(ids))
	assert sum(name.endswith('-centromere') for name in ids) == 1
	for node in root.iter():
		if 'clip-path' in node.attrib:
			assert node.attrib['clip-path'][5:-1] in ids
	for i, segment in enumerate(parent.segments):
		upper = root.find(f".//*[@id='pair-sister-0-region-{i}']")
		lower = root.find(f".//*[@id='pair-sister-1-region-{i}']")
		assert upper.find('rect').attrib['fill'] == lower.find('rect').attrib['fill'] == segment.color
		assert [node.attrib for node in upper.findall('path')] == [node.attrib for node in lower.findall('path')]
		u, l = upper.find('text'), lower.find('text')
		uy, ly = float(u.attrib['y']), float(l.attrib['y'])
		assert 0 < uy < 100 and 0 < ly < 100
		assert (uy < ly) == (i < parent.centromere_after)
		assert u.attrib['fill'] == ('#FFFFFF' if segment.color == '#00775F' else '#172B3A')
	# Check absolute silhouette coordinates rather than fixing a particular path shape.
	for node in root.findall('.//clipPath/path'):
		previous = (0, 0)
		for command, values in re.findall(r"([MLHVQCZ])([^MLHVQCZ]*)", node.attrib['d']):
			numbers = [float(value) for value in values.split()]
			if command == 'C':
				points = [previous] + list(zip(numbers[::2], numbers[1::2]))
				for step in range(101):
					t = step/100
					weights = ((1-t)**3, 3*(1-t)**2*t, 3*(1-t)*t*t, t**3)
					xy = [sum(p[axis]*w for p, w in zip(points, weights)) for axis in (0, 1)]
					assert 0 <= xy[0] <= 520 and 0 <= xy[1] <= 100
				previous = points[-1]
				continue
			limits = [100 if command == 'V' else 520] * len(numbers)
			if command in ('M', 'L', 'Q'):
				limits = [520, 100] * (len(numbers) // 2)
			assert all(0 <= number <= limit for number, limit in zip(numbers, limits))
			if len(numbers) >= 2:
				previous = tuple(numbers[-2:])
	assert fragment.isascii() and not any(node.tag in ('image', 'script', 'use') for node in root.iter())


#============================================
def test_source_map_identity_and_portrait_geometry(tmp_path: pathlib.Path) -> None:
	"""Real band intervals drive upright maps, sister copies and rearrangement ancestry."""
	c = svg_tools.chromosomes
	path = pathlib.Path(__file__).parents[1] / 'svg_tools/data/chr7_hg38_cytobands.tsv'
	model, records = c.read_cytobands(path)
	assert len(records) == 44 and records[-1].end == 159345973
	assert all(record.segment is segment for record, segment in zip(records, model.segments))
	q = next(record for record in records if record.segment.label == 'q31.2')
	assert (q.start, q.end, q.stain) == (115000000, 117700000, 'gneg')
	assert records[model.centromere_after].start == 60100000
	layout = c.render_chromosome_layout('map', model, length=600, thickness=250,
		orientation='vertical', sisters=True, bands=False, labels=False, marker_label='cen')
	assert (layout.width, layout.height) == (250, 600)
	assert all(a[1] < b[1] for a, b in zip(layout.boundaries, layout.boundaries[1:]))
	assert len(layout.segments) == 88
	for copy in (0, 1):
		anchors = [a for a in layout.segments if a.sister == copy]
		assert all(a.segment is s for a, s in zip(anchors, model.segments))
		assert all(a.start[1] < a.end[1] for a in anchors)
		assert all(0 <= a.bounds[0] < a.bounds[2] <= 250 for a in anchors)
	x0, y0, x1, y1 = layout.marker_bounds
	assert 0 <= x0 < x1 <= 250 and 0 <= y0 < y1 <= 600
	assert layout.centromere == pytest.approx(((x0+x1)/2, (y0+y1)/2))
	root = xml.etree.ElementTree.fromstring(layout.svg)
	assert [node.text for node in root.iter('text')] == ['cen']
	assert root.find(".//*[@id='map-centromere']").attrib['fill'] == 'none'
	assert root.find(".//*[@id='map-centromere']").attrib['stroke'] == '#72508C'
	for index in (model.centromere_after-1, model.centromere_after):
		region = root.find(f".//*[@id='map-sister-0-region-{index}']/rect")
		assert region.attrib['fill'] == records[index].segment.color == '#D9C9EF'
	assert not root.findall('.//*[@stroke-opacity]')
	assert all('transform' not in node.attrib for node in root.iter('text'))
	rod = c.render_chromosome_layout('rod-map', model, length=600, thickness=100,
		orientation='vertical', bands=False, labels=False)
	assert rod.boundaries[0][1] > 10
	assert rod.height-rod.boundaries[-1][1] > 10
	assert rod.marker_bounds[2]-rod.marker_bounds[0] == 100
	marker = xml.etree.ElementTree.fromstring(rod.svg).find(".//*[@id='rod-map-centromere']")
	assert (marker.attrib['fill'], marker.attrib['stroke']) == ('none', '#72508C')
	deleted = c.delete_segments(model, 1, 3)
	first, second = c.reciprocal_translocation(deleted, 25, model, 27)
	known = {id(record.segment) for record in records}
	assert all(id(segment) in known for segment in first.segments+second.segments)
	for text in ('chr7\t0\t10\tp11\tacen\nchr7\t11\t20\tq11\tacen\n',
		'chr7\t0\t10\tp11\tunknown\nchr7\t10\t20\tq11\tacen\n',
		'chr7\t0\t10\tq11\tacen\nchr7\t10\t20\tp11\tacen\n'):
		bad = tmp_path / 'bad.tsv'
		bad.write_text(text)
		with pytest.raises(ValueError):
			c.read_cytobands(bad)
	for kwargs in ({'orientation': 'diagonal'}, {'marker_size': (20, 260)},
		{'marker_size': (20, 1)}, {'marker_label': '\x00'}):
		with pytest.raises(ValueError):
			c.render_chromosome_layout('bad', model, length=600, thickness=250, **kwargs)
