"""Conservation and identity checks for chromosome material operations."""

import pytest

import svg_tools.chromosome_topology as topology


#============================================
def test_native_boundary_annotations_stay_with_the_same_material_after_reverse() -> None:
	chromatid = topology.chromosome('A', length=20, centromere=.25,
		genes={'p-tip': 0, 'at-cut': .25, 'q-tip': 1}, regions=((0, 'p'), (.5, 'q')))
	p, q = topology.split(chromatid, .25)
	reverse_q, reverse_p = topology.split(topology.reverse(chromatid), .75)
	assert q.length == reverse_q.length == 15
	assert p.length == reverse_p.length == 5
	assert reverse_q.ends == ('telomere', 'break')
	assert reverse_p.ends == ('break', 'telomere')
	assert topology.project_regions(reverse_q) == (
		topology.ProjectedRegion(0, 10, 'A', 'q'),
		topology.ProjectedRegion(10, 15, 'A', 'p'),
	)
	assert [g.locus_id for g in topology.project_genes(q)] == ['at-cut', 'q-tip']
	assert [(g.locus_id, g.position) for g in topology.project_genes(reverse_q)] == [
		('q-tip', 0), ('at-cut', 15),
	]
	assert [g.locus_id for g in topology.project_genes(p)] == ['p-tip']
	assert [g.locus_id for g in topology.project_genes(reverse_p)] == ['p-tip']
	assert topology.project_centromeres(p) == topology.project_centromeres(reverse_p) == ()
	assert topology.project_centromeres(reverse_q) == (
		topology.ProjectedCentromere('A', 'A', 'A.cen', 15, True),
	)
	decimal = topology.chromosome('D', length=31, centromere=.3)
	reverse_q, reverse_p = topology.split(topology.reverse(decimal), .7)
	assert [site.id for site in topology.project_centromeres(reverse_q)] == ['D.cen']
	assert topology.project_centromeres(reverse_p) == ()


#============================================
def test_validate_conservation_rejects_lost_or_reused_material() -> None:
	first = topology.chromosome('A', length=10)
	second = topology.chromosome('B', length=15)
	first_head, first_tip = topology.split(first, .4)
	second_head, second_tip = topology.split(second, 7/15)
	left = topology.join(first_head, second_tip)
	right = topology.join(second_head, first_tip)
	assert (left.length, right.length) == (12, 13)
	before = (first, second)
	topology.validate_conservation(before, (topology.reverse(right), left))

	for head_length, total in ((8, 26), (2, 20)):
		head, _ = topology.split(second, head_length/second.length)
		with pytest.raises(ValueError, match=f'total length 25 before, {total} after'):
			topology.validate_conservation(before, (left, topology.join(head, first_tip)))

	with pytest.raises(ValueError, match='total length 25 before, 25 after'):
		topology.validate_conservation(before, (left, topology.copy(right, 'extra-copy')))


#============================================
def test_robertsonian_products_conserve_arms_and_separate_site_activities() -> None:
	first = topology.chromosome('A', length=10, centromere=.2, regions=((0, 'p'), (.2, 'q')))
	second = topology.chromosome('B', length=20, centromere=.15, regions=((0, 'p'), (.15, 'q')))
	a_p, a_q = topology.split(first, .2)
	b_p, b_q = topology.split(second, .15)
	b_q = topology.with_centromere_activity(b_q, 'B.cen', active=False)
	long = topology.join(topology.reverse(a_q), b_q)
	short = topology.join(a_p, topology.reverse(b_p))
	assert long.junctions == (8,)
	assert short.junctions == (2,)
	assert topology.project_centromeres(long) == (
		topology.ProjectedCentromere('A', 'A', 'A.cen', 8, True),
		topology.ProjectedCentromere('B', 'B', 'B.cen', 8, False),
	)
	assert topology.project_centromeres(short) == ()
	assert topology.project_regions(long) == (
		topology.ProjectedRegion(0, 8, 'A', 'q'),
		topology.ProjectedRegion(8, 25, 'B', 'q'),
	)
	assert topology.project_regions(short) == (
		topology.ProjectedRegion(0, 2, 'A', 'p'),
		topology.ProjectedRegion(2, 5, 'B', 'p'),
	)


#============================================
def test_material_identity_rejects_overlap_and_conflicting_sources() -> None:
	first = topology.chromosome('A', length=10)
	other_definition = topology.chromosome('A', length=12)
	with pytest.raises(ValueError, match='Overlapping material'):
		topology.join(first, topology.reverse(first))
	with pytest.raises(ValueError, match='Conflicting definitions'):
		topology.join(first, topology.copy(other_definition, 'B'))
	first_part, second_part = topology.split(first, .4)
	assert topology.join(first_part, second_part).length == 10
	assert topology.join(first, topology.copy(first, 'C')).length == 20
