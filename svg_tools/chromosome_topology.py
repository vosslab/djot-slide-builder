"""Immutable chromosome material, annotations, and linear rearrangements."""

import sys
import math
import itertools
import dataclasses
import collections.abc


#============================================
def _finite(value: float) -> bool:
	valid = (isinstance(value, (int, float)) and not isinstance(value, bool)
		and -sys.float_info.max <= value <= sys.float_info.max)
	return valid


#============================================
def _identifier(value: str) -> bool:
	valid = isinstance(value, str) and bool(value)
	return valid


#============================================
@dataclasses.dataclass(frozen=True)
class Region:
	"""A semantic region in native source coordinates."""

	id: str
	start: float
	stop: float


#============================================
@dataclasses.dataclass(frozen=True)
class Gene:
	"""A stable locus and the allele carried at its native position."""

	locus_id: str
	position: float
	allele: str


#============================================
@dataclasses.dataclass(frozen=True)
class CentromericSite:
	"""A centromere position carried by source material."""

	id: str
	position: float


#============================================
@dataclasses.dataclass(frozen=True)
class SourceMaterial:
	"""An ordered source with native coordinates from zero to length."""

	id: str
	length: float
	regions: tuple[Region, ...]
	genes: tuple[Gene, ...]
	centromeres: tuple[CentromericSite, ...]

	def __post_init__(self) -> None:
		if not _identifier(self.id) or not _finite(self.length) or self.length <= 0:
			raise ValueError('Source material needs an ID and a finite positive length')
		object.__setattr__(self, 'regions', tuple(self.regions))
		object.__setattr__(self, 'genes', tuple(self.genes))
		object.__setattr__(self, 'centromeres', tuple(self.centromeres))
		stop = 0
		for region in self.regions:
			if (not isinstance(region, Region) or not _identifier(region.id)
				or not _finite(region.start) or not _finite(region.stop)
				or not stop == region.start < region.stop <= self.length):
				raise ValueError('Source regions must cover contiguous, ordered intervals')
			stop = region.stop
		if stop != self.length:
			raise ValueError('Source regions must cover the full source length')
		gene_ids = set()
		for gene in self.genes:
			if (not isinstance(gene, Gene) or not _identifier(gene.locus_id)
				or not _identifier(gene.allele) or not self._has_position(gene.position)
				or gene.locus_id in gene_ids):
				raise ValueError('Source genes need distinct locus IDs, alleles, and valid positions')
			gene_ids.add(gene.locus_id)
		site_ids = set()
		for site in self.centromeres:
			if (not isinstance(site, CentromericSite) or not _identifier(site.id)
				or not self._has_position(site.position) or site.id in site_ids):
				raise ValueError('Source centromeres need distinct site IDs and valid positions')
			site_ids.add(site.id)

	def _has_position(self, position: float) -> bool:
		valid = _finite(position) and 0 <= position <= self.length
		return valid


#============================================
@dataclasses.dataclass(frozen=True)
class Span:
	"""A native interval of one physical copy, read in either direction."""

	source: SourceMaterial
	copy_id: str
	start: float
	stop: float
	orientation: int = 1

	def __post_init__(self) -> None:
		if (not isinstance(self.source, SourceMaterial) or not _identifier(self.copy_id)
			or not _finite(self.start) or not _finite(self.stop)
			or not 0 <= self.start < self.stop <= self.source.length):
			raise ValueError('A span needs a copy ID and a positive interval within its source')
		if type(self.orientation) is not int or self.orientation not in (-1, 1):
			raise ValueError('Span orientation must be 1 or -1')

	@property
	def length(self) -> float:
		length = self.stop - self.start
		return length

	def _contains(self, position: float) -> bool:
		# Native boundary points belong to the span that starts there in source order.
		inside = self.start <= position < self.stop or position == self.stop == self.source.length
		return inside

	def _distance(self, position: float) -> float:
		distance = position - self.start if self.orientation == 1 else self.stop - position
		return distance


#============================================
def _centromere_keys(spans: tuple[Span, ...]) -> tuple[tuple[str, str], ...]:
	keys = tuple((span.copy_id, site.id) for span in spans for site in span.source.centromeres
		if span._contains(site.position))
	return keys


#============================================
@dataclasses.dataclass(frozen=True)
class Chromatid:
	"""Linear material with two outer ends, internal junctions, and centromere activity."""

	id: str
	spans: tuple[Span, ...]
	ends: tuple[str, str] = ('telomere', 'telomere')
	connections: tuple[int, ...] = ()
	inactive_centromeres: tuple[tuple[str, str], ...] = ()

	def __post_init__(self) -> None:
		object.__setattr__(self, 'spans', tuple(self.spans))
		object.__setattr__(self, 'ends', tuple(self.ends))
		object.__setattr__(self, 'connections', tuple(self.connections))
		object.__setattr__(self, 'inactive_centromeres', tuple(self.inactive_centromeres))
		if not _identifier(self.id) or not self.spans or not all(
			isinstance(span, Span) for span in self.spans):
			raise ValueError('A chromatid needs an ID and at least one valid span')
		if len(self.ends) != 2 or any(end not in ('telomere', 'break') for end in self.ends):
			raise ValueError('A chromatid needs two telomere or break ends')
		length = self.length
		if not _finite(length):
			raise ValueError('Chromatid length must be finite')
		previous = 0
		for connection in self.connections:
			if type(connection) is not int or not previous < connection < len(self.spans):
				raise ValueError('Connections must be distinct, ordered interior span indexes')
			previous = connection
		sources = {}
		copies = {}
		for span in self.spans:
			source = sources.setdefault(span.source.id, span.source)
			if source != span.source:
				raise ValueError(f'Conflicting definitions for source {source.id!r}')
			copies.setdefault((source.id, span.copy_id), []).append((span.start, span.stop))
		for intervals in copies.values():
			stop = 0
			for start, next_stop in sorted(intervals):
				if start < stop:
					raise ValueError('Overlapping material requires an explicit copy')
				stop = next_stop
		keys = _centromere_keys(self.spans)
		if len(keys) != len(set(keys)):
			raise ValueError('Centromere occurrences must have distinct copy and site ID pairs')
		if any(key not in keys for key in self.inactive_centromeres):
			raise ValueError('Inactive centromeres must be present on the chromatid')
		if len(set(self.inactive_centromeres)) != len(self.inactive_centromeres):
			raise ValueError('Inactive centromere entries must be distinct')

	@property
	def length(self) -> float:
		length = 0
		for span in self.spans:
			length += span.length
		return length

	@property
	def junctions(self) -> tuple[float, ...]:
		"""Current material distances to the stored span connections."""
		ends = tuple(itertools.accumulate(span.length for span in self.spans))
		junctions = tuple(ends[connection - 1] for connection in self.connections)
		return junctions


#============================================
@dataclasses.dataclass(frozen=True)
class SisterPair:
	"""Two independently usable chromatids from one replication."""

	first: Chromatid
	second: Chromatid


#============================================
@dataclasses.dataclass(frozen=True)
class ProjectedRegion:
	"""A clipped source region within current material distances."""

	start: float
	stop: float
	source_id: str
	region_id: str


#============================================
@dataclasses.dataclass(frozen=True)
class ProjectedGene:
	"""One allele occurrence positioned on the current material."""

	source_id: str
	copy_id: str
	locus_id: str
	allele: str
	position: float


#============================================
@dataclasses.dataclass(frozen=True)
class ProjectedCentromere:
	"""One centromere occurrence positioned on the current material."""

	source_id: str
	copy_id: str
	id: str
	position: float
	active: bool


#============================================
def project_regions(chromatid: Chromatid) -> tuple[ProjectedRegion, ...]:
	"""Clip and position source regions along the current material."""
	regions = []
	offset = 0
	for span in chromatid.spans:
		for region in span.source.regions:
			start = max(span.start, region.start)
			stop = min(span.stop, region.stop)
			if start < stop:
				first, second = sorted((span._distance(start), span._distance(stop)))
				regions.append(ProjectedRegion(offset + first, offset + second,
					span.source.id, region.id))
		offset += span.length
	projected = tuple(sorted(regions, key=lambda region: region.start))
	return projected


#============================================
def project_genes(chromatid: Chromatid) -> tuple[ProjectedGene, ...]:
	"""Position each retained allele occurrence along the current material."""
	genes = []
	offset = 0
	for span in chromatid.spans:
		for gene in span.source.genes:
			if span._contains(gene.position):
				position = offset + span._distance(gene.position)
				genes.append(ProjectedGene(span.source.id, span.copy_id,
					gene.locus_id, gene.allele, position))
		offset += span.length
	projected = tuple(sorted(genes, key=lambda gene: gene.position))
	return projected


#============================================
def project_centromeres(chromatid: Chromatid) -> tuple[ProjectedCentromere, ...]:
	"""Position each retained centromere with its current activity."""
	sites = []
	offset = 0
	for span in chromatid.spans:
		for site in span.source.centromeres:
			if span._contains(site.position):
				position = offset + span._distance(site.position)
				active = (span.copy_id, site.id) not in chromatid.inactive_centromeres
				sites.append(ProjectedCentromere(span.source.id, span.copy_id, site.id, position, active))
		offset += span.length
	projected = tuple(sorted(sites, key=lambda site: site.position))
	return projected


#============================================
def _native_position(fraction: float, length: float) -> float:
	if not _finite(fraction) or not 0 <= fraction <= 1:
		raise ValueError('Feature positions must be fractions from zero to one')
	position = fraction * length
	return position


#============================================
def chromosome(id: str, *, length: float, centromere: float | None = None,
	genes: dict[str, float] | None = None,
	regions: tuple[tuple[float, str], ...] | None = None) -> Chromatid:
	"""Create intact material with feature coordinates given as fractions of length."""
	if not _finite(length) or length <= 0:
		raise ValueError('Chromosome length must be finite and positive')
	if regions is None:
		regions = ((0, 'body'),)
	starts = [(_native_position(fraction, length), region_id) for fraction, region_id in regions]
	stops = [start for start, _ in starts[1:]] + [length]
	source_regions = tuple(Region(region_id, start, stop)
		for (start, region_id), stop in zip(starts, stops))
	source_genes = tuple(Gene(locus, _native_position(fraction, length), locus)
		for locus, fraction in genes.items()) if genes is not None else ()
	sites = ()
	if centromere is not None:
		sites = (CentromericSite(f'{id}.cen', _native_position(centromere, length)),)
	source = SourceMaterial(id, length, source_regions, source_genes, sites)
	chromatid = Chromatid(id, (Span(source, id, 0, length),))
	return chromatid


#============================================
def homolog(chr: Chromatid, new_id: str, *, alleles: dict[str, str] | None = None) -> Chromatid:
	"""Make a distinct intact homolog with matching regions and locus positions."""
	if len(chr.spans) != 1 or chr.ends != ('telomere', 'telomere'):
		raise ValueError('A homolog requires one intact source chromosome')
	span = chr.spans[0]
	source = span.source
	if span.start != 0 or span.stop != source.length:
		raise ValueError('A homolog requires one intact source chromosome')
	if new_id in (source.id, span.copy_id):
		raise ValueError('A homolog needs a distinct source and copy ID')
	if alleles is None:
		alleles = {}
	if alleles.keys() - {gene.locus_id for gene in source.genes}:
		raise ValueError('Allele overrides must identify existing loci')
	genes = tuple(dataclasses.replace(gene, allele=alleles.get(gene.locus_id, gene.allele))
		for gene in source.genes)
	sites = tuple(CentromericSite(f'{new_id}.cen' if index == 0 else f'{new_id}.cen{index + 1}',
		site.position) for index, site in enumerate(source.centromeres))
	new_source = dataclasses.replace(source, id=new_id, genes=genes, centromeres=sites)
	inactive = tuple((new_id, new.id) for old, new in zip(source.centromeres, sites)
		if (span.copy_id, old.id) in chr.inactive_centromeres)
	new_span = dataclasses.replace(span, source=new_source, copy_id=new_id)
	new_chromatid = Chromatid(new_id, (new_span,), inactive_centromeres=inactive)
	return new_chromatid


#============================================
def _snap_position(position: float, coordinates: collections.abc.Iterable[float],
	tolerance: float) -> float:
	nearest = min(coordinates, key=lambda point: abs(point - position), default=position)
	if abs(nearest - position) <= tolerance:
		return nearest
	return position


#============================================
def split(fragment: Chromatid, cut: float) -> tuple[Chromatid, Chromatid]:
	"""Cut at an interior fraction, preserving feature ownership at rounding-equivalent cuts."""
	if not _finite(cut) or not 0 < cut < 1:
		raise ValueError('Cut must be a fraction strictly between zero and one')
	ends = tuple(itertools.accumulate(span.length for span in fragment.spans))
	length = ends[-1]
	# Fraction conversion and reversal can move a boundary by floating-point roundoff.
	tolerance = 2 * math.ulp(length)
	distance = _snap_position(cut * length, ends[:-1], tolerance)
	left_spans, right_spans = [], []
	offset = 0
	for span, end in zip(fragment.spans, ends):
		if end <= distance:
			left_spans.append(span)
		elif offset >= distance:
			right_spans.append(span)
		else:
			local = distance - offset
			point = span.start + local if span.orientation == 1 else span.stop - local
			features = itertools.chain((region.start for region in span.source.regions),
				(gene.position for gene in span.source.genes),
				(site.position for site in span.source.centromeres))
			point = _snap_position(point,
				(value for value in features if span.start < value < span.stop), tolerance)
			if span.orientation == 1:
				left_spans.append(dataclasses.replace(span, stop=point))
				right_spans.append(dataclasses.replace(span, start=point))
			else:
				left_spans.append(dataclasses.replace(span, start=point))
				right_spans.append(dataclasses.replace(span, stop=point))
		offset = end
	# Each connection belongs to a fragment only when both adjacent spans remain there.
	right_offset = len(fragment.spans) - len(right_spans)
	left_connections = tuple(index for index in fragment.connections if index < len(left_spans))
	right_connections = tuple(index - right_offset
		for index in fragment.connections if index > right_offset)
	left_keys = _centromere_keys(tuple(left_spans))
	right_keys = _centromere_keys(tuple(right_spans))
	left = Chromatid(f'{fragment.id}.left', tuple(left_spans), (fragment.ends[0], 'break'),
		left_connections, tuple(key for key in fragment.inactive_centromeres if key in left_keys))
	right = Chromatid(f'{fragment.id}.right', tuple(right_spans), ('break', fragment.ends[1]),
		right_connections, tuple(key for key in fragment.inactive_centromeres if key in right_keys))
	return left, right


#============================================
def reverse(fragment: Chromatid) -> Chromatid:
	"""Read the same material from its opposite end."""
	spans = tuple(dataclasses.replace(span, orientation=-span.orientation)
		for span in reversed(fragment.spans))
	connections = tuple(len(spans) - index for index in reversed(fragment.connections))
	reversed_fragment = dataclasses.replace(fragment, spans=spans,
		ends=(fragment.ends[1], fragment.ends[0]),
		connections=connections)
	return reversed_fragment


#============================================
def copy(fragment: Chromatid, copy_id: str) -> Chromatid:
	"""Make an explicit physical copy while retaining provenance and activity."""
	if not _identifier(copy_id):
		raise ValueError('Copy needs a nonempty ID')
	old_ids = sorted({span.copy_id for span in fragment.spans})
	if len(old_ids) == 1:
		new_ids = {old_ids[0]: copy_id}
	else:
		new_ids = {old_id: f'{copy_id}.{index}' for index, old_id in enumerate(old_ids, start=1)}
	if set(old_ids).intersection(new_ids.values()):
		raise ValueError('New physical copy IDs must differ from the originals')
	spans = tuple(dataclasses.replace(span, copy_id=new_ids[span.copy_id])
		for span in fragment.spans)
	inactive = tuple((new_ids[old_id], site_id) for old_id, site_id in fragment.inactive_centromeres)
	copied = dataclasses.replace(fragment, id=copy_id, spans=spans, inactive_centromeres=inactive)
	return copied


#============================================
def join(*fragments: Chromatid) -> Chromatid:
	"""Concatenate oriented material, replacing facing ends with junctions."""
	if len(fragments) < 2:
		raise ValueError('Join requires at least two fragments')
	spans = []
	connections = []
	for fragment in fragments:
		offset = len(spans)
		if offset:
			connections.append(offset)
		connections.extend(offset + index for index in fragment.connections)
		spans.extend(fragment.spans)
	ends = (fragments[0].ends[0], fragments[-1].ends[1])
	inactive = tuple(key for fragment in fragments for key in fragment.inactive_centromeres)
	joined = Chromatid('+'.join(fragment.id for fragment in fragments), tuple(spans), ends,
		tuple(connections), inactive)
	return joined


#============================================
def validate_conservation(before: collections.abc.Sequence[Chromatid],
	after: collections.abc.Sequence[Chromatid]) -> None:
	"""Require the same native intervals of each physical copy across a rearrangement."""
	# Opposite changes at a shared boundary cancel regardless of how spans are split or oriented.
	boundaries = collections.Counter()
	for sign, chromatids in ((1, before), (-1, after)):
		for chromatid in chromatids:
			for span in chromatid.spans:
				boundaries[span.source, span.copy_id, span.start] += sign
				boundaries[span.source, span.copy_id, span.stop] -= sign
	if any(boundaries.values()):
		input_length = sum(chromatid.length for chromatid in before)
		output_length = sum(chromatid.length for chromatid in after)
		raise ValueError(f'Chromosome material must be conserved across products '
			f'(total length {input_length:g} before, {output_length:g} after)')


#============================================
def replicate(fragment: Chromatid) -> SisterPair:
	"""Make two equivalent sister chromatids with distinct physical copy IDs."""
	pair = SisterPair(copy(fragment, f'{fragment.id}.s1'), copy(fragment, f'{fragment.id}.s2'))
	return pair


#============================================
def with_centromere_activity(fragment: Chromatid, site_id: str | tuple[str, str], *,
	active: bool) -> Chromatid:
	"""Set activity on one site by ID or by its (copy ID, site ID) occurrence."""
	if type(active) is not bool:
		raise ValueError('Centromere activity must be a boolean')
	keys = _centromere_keys(fragment.spans)
	matches = [key for key in keys if site_id in (key[1], key)]
	if len(matches) != 1:
		raise ValueError('Centromere activity requires one unambiguous current occurrence')
	key = matches[0]
	inactive = set(fragment.inactive_centromeres)
	if active:
		inactive.discard(key)
	else:
		inactive.add(key)
	ordered = tuple(key for key in keys if key in inactive)
	updated_fragment = dataclasses.replace(fragment, inactive_centromeres=ordered)
	return updated_fragment
