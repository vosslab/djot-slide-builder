"""Render imported-slide facts and geometry plans as bounded Djot source."""

# Standard Library
import dataclasses
import itertools
import re

# local repo modules
import slide_lib.layout_engine
import slide_lib.importers.geometry as geometry
import slide_lib.importers.native_normalization as native_normalization
import slide_lib.importers.topology as topology
import slide_lib.importers.slide_plan as slide_plan
import slide_lib.importers.source_model as source_model
import slide_lib.importers.visual_relations as visual_relations


GALLERY_AREA_VARIATION_RATIO = 1.30
GALLERY_ASPECT_VARIATION_RATIO = 1.30
GALLERY_LINE_CENTER_TOLERANCE = 0.12
FLOW_VERTICAL_GAP_RATIO = 0.03
FLOW_MIN_HORIZONTAL_OVERLAP_RATIO = 0.60
FLOW_LANE_SPAN_VARIATION_RATIO = 1.35
FLOW_LANE_CENTER_OFFSET_RATIO = 0.20
FOOTER_MIN_WIDTH_RATIO = 0.70
FOOTER_MAX_HEIGHT_RATIO = 0.50
FOOTER_COLUMN_BOTTOM_PADDING_RATIO = 0.08
FOOTER_VERTICAL_PADDING_RATIO = 0.05
FOOTER_IMAGE_PADDING_RATIO = 0.05
COARSE_IMAGE_ROW_CENTER_RATIO = 0.35
COARSE_IMAGE_SIDE_BY_SIDE_RATIO = 0.50
BOTTOM_FOOTER_SCORE_CEILING = 0.35
BOTTOM_FOOTER_RELATION_REASON = "bottom-footer structural topology"
ASYMMETRIC_EXPLANATORY_PAIR_MAX_SCORE = 0.33
ASYMMETRIC_EXPLANATORY_COMPACT_AREA_RATIO = 0.75
SHALLOW_FLOW_MAX_VERTICAL_OVERLAP = 0.03
SHALLOW_FLOW_MAX_SMALLER_HEIGHT_RATIO = 0.25
# LibreOffice normalization may place the trailing prime before the strand number.
PRIMED_SEQUENCE = re.compile(
	r"([35])[\u2032\u2019'']-([ACGTU][ACGTU|/,.]{2,}[ACGTU])-[\u2032\u2019'']([35])"
)
# Direct PPTX text commonly retains the conventional number-then-prime order.
CONVENTIONAL_PRIMED_SEQUENCE = re.compile(
	r"([35])[\u2032\u2019'']-([ACGTU][ACGTU|/,.]{2,}[ACGTU])-([35])[\u2032\u2019'']"
)
PRIME_MARK = re.compile(r"([35])[\u2032\u2019'']")
DNA_SEQUENCE = re.compile(r"(?<![A-Za-z0-9`])([ACGTU][ACGTU|/,.]{2,}[ACGTU])(?![A-Za-z0-9`])")
DJOT_PUNCTUATION = frozenset("\\`*_[]$~^{}:")
@dataclasses.dataclass(frozen=True)
class PlannedSlide:
	"""Imported-slide facts and their geometry-first projection."""
	data: source_model.SlideData
	plan: slide_plan.SlidePlan | None
	text_regions: tuple[slide_plan.SourceTextRegion, ...] = ()
	image_regions: tuple[slide_plan.SourceImageRegion, ...] = ()
	visible_page_index: int | None = None
@dataclasses.dataclass(frozen=True)
class EmissionComponent:
	"""One bounded, single-kind source component assigned to one Djot Cell."""
	bounds: geometry.NormalizedBounds
	lines: tuple[str, ...]
	kind: str
	image_references: tuple[str, ...] = ()
	source_image_ids: tuple[tuple[int, str], ...] = ()
	coarse_text_container: bool = False
	source_kind: str = ""
	source_ordinals: tuple[int, ...] = ()
	member_footprints: tuple[geometry.NormalizedBounds, ...] = ()
	classification_reason: str = ""
	placeholder_confidence: float = 0.0
	rotation_degrees: float = 0.0
@dataclasses.dataclass(frozen=True)
class OverlapPermission:
	"""One exact component-pair overlap allowed by a uniquely matched composition."""
	first_index: int
	second_index: int
	relation: str
	first_footprints: tuple[geometry.NormalizedBounds, ...]
	second_footprints: tuple[geometry.NormalizedBounds, ...]
	vertical_overlap: float
	layout: str
	order: tuple[int, ...]
#============================================
def djot_text(text: str) -> str:
	"""Escape raw source characters once and project settled DNA notation."""
	# ASVS 1.2.1: output escaping occurs only at the Djot rendering boundary.
	escaped = "".join(f"\\{character}" if character in DJOT_PUNCTUATION else character for character in text)
	escaped = PRIMED_SEQUENCE.sub(r"\1&prime;-`\2`-\3&prime;", escaped)
	escaped = CONVENTIONAL_PRIMED_SEQUENCE.sub(r"\1&prime;-`\2`-\3&prime;", escaped)
	escaped = PRIME_MARK.sub(r"\1&prime;", escaped)
	return DNA_SEQUENCE.sub(r"`\1`", escaped)


#============================================
def djot_link_target(target: str) -> str:
	"""Encode delimiter and whitespace characters in one allowed link target."""
	# ASVS 1.2.2: encode an already allow-listed URL at its output context.
	return target.replace(" ", "%20").replace("(", "%28").replace(")", "%29")


#============================================
def render_runs(runs: tuple[source_model.TextRun, ...]) -> str:
	"""Render raw source runs into Djot inline syntax exactly once."""
	# Join equal-link neighbors so formatting-only splits cannot break DNA recognition while
	# hyperlink boundaries remain distinct.
	coalesced: list[source_model.TextRun] = []
	for run in runs:
		if coalesced and coalesced[-1].link == run.link:
			previous = coalesced[-1]
			coalesced[-1] = source_model.TextRun(previous.text + run.text, previous.link)
		else:
			coalesced.append(run)
	segments: list[str] = []
	for run in coalesced:
		text = djot_text(run.text)
		if run.link:
			segments.append(f"[{text}]({djot_link_target(run.link)})")
		else:
			segments.append(text)
	return "".join(segments)


#============================================
def image_djot(image: source_model.ImageAsset) -> str:
	"""Render one imported-deck image as a Djot component image."""
	return f"![{djot_text(image.alt_text)}]({image.asset_path})"


#============================================
def region_lines(regions: tuple[slide_plan.SourceTextRegion, ...]) -> list[str]:
	"""Project retained source text without changing its paragraph hierarchy."""
	lines: list[str] = []
	for region in regions:
		for level, runs in region.paragraphs:
			text = render_runs(runs)
			if region.is_subtitle:
				lines.append(f"## {text}")
			else:
				lines.append(f"{'  ' * level}- {text}")
	return lines


#============================================
def multiple_choice_question_lines(region: slide_plan.SourceTextRegion) -> list[str]:
	"""Keep a source prompt before nested choices when hierarchy supplies one."""
	paragraphs = region.paragraphs
	first_level = paragraphs[0][0]
	choice_start = 1 if any(level > first_level for level, _text in paragraphs[1:]) else 0
	lines = [] if choice_start == 0 else [render_runs(paragraphs[0][1]), ""]
	choice_level = min(level for level, _text in paragraphs[choice_start:])
	for level, runs in paragraphs[choice_start:]:
		lines.append(f"{'  ' * (level - choice_level)}- {render_runs(runs)}")
	return lines


#============================================
def render_multiple_choice(planned: PlannedSlide) -> tuple[list[str], str, list[str]]:
	"""Emit one complete structural question without inferring any animation."""
	if planned.plan is None or planned.plan.multiple_choice is None:
		raise ValueError("multiple-choice emission requires a multiple-choice slide plan")
	choice = planned.plan.multiple_choice
	lines = ["=== layout: multiple-choice", "", "@question", ""]
	reasons = list(planned.data.review_reasons)
	visual = choice.question_visual_region
	if visual is not None:
		image_lines, image_reasons = slot_image_lines(visual.image_regions, planned.data.images)
		reasons.extend(image_reasons)
		for image_line in image_lines:
			lines.extend((image_line, ""))
		for region in visual.text_regions:
			lines.extend((*region_lines((region,)), ""))
		reasons.append(
			f"normalized {visual.classification_reason} into native source-order content"
		)
	elif choice.image is not None:
		image_lines, image_reasons = slot_image_lines((choice.image,), planned.data.images)
		if image_reasons:
			raise ValueError("multiple-choice figure requires a native raster asset")
		lines.extend((*image_lines, ""))
	lines.extend(multiple_choice_question_lines(choice.question))
	answer_lines = tuple(render_runs(runs) for _level, runs in choice.answer.paragraphs)
	lines.extend(("", "@answer", ""))
	for index, text in enumerate(answer_lines):
		if index:
			lines.append("")
		lines.append(text)
	return lines, "multiple-choice", reasons


#============================================
def table_lines(tables: tuple[source_model.TableBlock, ...]) -> list[str]:
	"""Project supported source tables as canonical editable Djot pipe tables."""
	lines: list[str] = []
	for table in tables:
		if table.unsupported_reason:
			raise ValueError(f"source table requires review: {table.unsupported_reason}")
		if lines:
			lines.append("")
		if table.headers:
			header_values = tuple(render_runs(cell).replace("|", "\\|") for cell in table.headers)
			lines.append(f"| {' | '.join(header_values)} |")
			lines.append(f"| {' | '.join('---' for _cell in table.headers)} |")
		for row in table.rows:
			values = tuple(render_runs(cell).replace("|", "\\|") for cell in row)
			lines.append(f"| {' | '.join(values)} |")
	return lines


#============================================
def slot_image_lines(
	regions: tuple[slide_plan.SourceImageRegion, ...],
	images: tuple[source_model.ImageAsset, ...],
) -> tuple[list[str], list[str]]:
	"""Resolve extracted image references; retain an explicit review lane otherwise."""
	by_reference = {image.asset_path: image for image in images}
	lines: list[str] = []
	reasons: list[str] = []
	for region in regions:
		image = by_reference.get(region.asset_reference)
		if image is None:
			reasons.append("unprojected non-raster visual requires review")
			continue
		lines.append(image_djot(image))
	return lines, reasons


#============================================
def region_bounds(regions: tuple[object, ...]) -> geometry.NormalizedBounds:
	"""Return the geometry union of one nonempty homogeneous source component."""
	bounds = regions[0].bounds
	for region in regions[1:]:
		bounds = bounds.union(region.bounds)
	return bounds


#============================================
def shared_footer_sources(
		text_regions: tuple[slide_plan.SourceTextRegion, ...],
		image_regions: tuple[slide_plan.SourceImageRegion, ...],
) -> tuple[slide_plan.SourceTextRegion, ...]:
	"""Recognize one or more broad bottom references under a text/direct-picture pair."""
	if len(image_regions) != 1 or image_regions[0].source_kind != "picture":
		return ()
	image = image_regions[0]
	footer = tuple(item for item in text_regions if item.source_kind == "text-box" and item.placeholder_confidence == 0.0)
	peers = tuple(item for item in text_regions if item not in footer)
	if len(peers) != 1 or not footer:
		return ()
	peer = peers[0]
	span = max(peer.bounds.right, image.bounds.right) - min(peer.bounds.left, image.bounds.left)
	if any(item.bounds.width < span * FOOTER_MIN_WIDTH_RATIO or
		item.bounds.top < peer.bounds.bottom - FOOTER_IMAGE_PADDING_RATIO or
		item.bounds.top < image.bounds.bottom - FOOTER_IMAGE_PADDING_RATIO for item in footer):
		return ()
	return footer


#============================================
def emit_components(
	planned: PlannedSlide,
) -> tuple[list[EmissionComponent], list[str]]:
	"""Project each planned component without combining text, tables, and images."""
	if planned.plan is None:
		raise ValueError("component emission requires a visible slide plan")
	components: list[EmissionComponent] = []
	reasons: list[str] = []
	for slot in planned.plan.slots:
		if slot.flows_in_source_order:
			flow_items: list[tuple[geometry.NormalizedBounds, int, str, object]] = []
			for region in slot.text_regions:
				flow_items.append((region.bounds, region.source_ordinal, "text", region))
			for region in slot.image_regions:
				flow_items.append((region.bounds, region.source_ordinal, "image", region))
			flow_items.sort(key=lambda item: (item[0].top, item[0].left, item[1]))
			lines: list[str] = []
			image_references: list[str] = []
			source_image_ids: list[tuple[int, str]] = []
			source_ordinals: list[int] = []
			for _bounds, _ordinal, kind, item in flow_items:
				if lines:
					lines.append("")
				if kind == "text":
					lines.extend(region_lines((item,)))
					source_ordinals.append(item.source_ordinal)
					continue
				lines_for_image, image_reasons = slot_image_lines((item,), planned.data.images)
				reasons.extend(image_reasons)
				if lines_for_image:
					lines.extend(lines_for_image)
					image_references.append(item.asset_reference)
					source_image_ids.append((item.source_ordinal, item.asset_reference))
			components.append(EmissionComponent(
				region_bounds(tuple(item[3] for item in flow_items)), tuple(lines), "flow",
				tuple(image_references), tuple(source_image_ids), source_ordinals=tuple(source_ordinals),
				member_footprints=tuple(item[0] for item in flow_items),
			))
			continue
		shared_footer = set(shared_footer_sources(slot.text_regions, slot.image_regions))
		pairs = visual_relations.caption_pairings(
			tuple(text for text in slot.text_regions if text not in shared_footer),
			slot.image_regions,
		)
		paired_text = set(pairs.values())
		for text in slot.text_regions:
			if text not in paired_text:
				components.append(EmissionComponent(
					text.bounds, tuple(region_lines((text,))), "text", (), (),
					text.placeholder_confidence >= 0.75, text.source_kind, (text.source_ordinal,), (text.bounds,),
					placeholder_confidence=text.placeholder_confidence,
					rotation_degrees=text.rotation_degrees,
					classification_reason=slot.relation_id,
				))
		for region in slot.image_regions:
				lines, image_reasons = slot_image_lines((region,), planned.data.images)
				reasons.extend(image_reasons)
				if lines:
					caption = pairs.get(region)
					if caption is not None:
						lines.extend(("", *region_lines((caption,))))
						bounds = region.bounds.union(caption.bounds)
					else:
						bounds = region.bounds
					components.append(EmissionComponent(
						bounds,
						tuple(lines),
						"image",
						(region.asset_reference,),
						((region.source_ordinal, region.asset_reference),),
						source_kind=region.source_kind,
						source_ordinals=(region.source_ordinal,) if caption is None else
							(region.source_ordinal, caption.source_ordinal),
						member_footprints=(region.bounds,) if caption is None else (region.bounds, caption.bounds),
						classification_reason=slot.relation_id,
					))
	content = planned.plan.content_region
	if content is not None:
		local_heading = content.local_heading
		content_text_regions = tuple(region for region in content.text_regions if region is not local_heading)
		positioned_label_count = len(content_text_regions)
		if positioned_label_count > native_normalization.MAX_POSITIONED_LABELS:
			content_text_regions = ()
			reasons.append(f"{positioned_label_count} positioned labels require native redesign")
		flow_items: list[tuple[geometry.NormalizedBounds, int, str, object]] = []
		for region in content_text_regions:
			flow_items.append((region.bounds, region.source_ordinal, "text", region))
		for region in content.image_regions:
			flow_items.append((region.bounds, region.source_ordinal, "image", region))
		flow_items.sort(key=lambda item: (item[1], item[0].top, item[0].left))
		lines: list[str] = ([] if local_heading is None else
			[f"## {' '.join(render_runs(runs) for _level, runs in local_heading.paragraphs)}"])
		image_references: list[str] = []
		source_image_ids: list[tuple[int, str]] = []
		for _bounds, _ordinal, kind, item in flow_items:
			if lines:
				lines.append("")
			if kind == "text":
				lines.extend(region_lines((item,)))
				continue
			image_lines, image_reasons = slot_image_lines((item,), planned.data.images)
			reasons.extend(image_reasons)
			if image_lines:
				lines.extend(image_lines)
				image_references.append(item.asset_reference)
				source_image_ids.append((item.source_ordinal, item.asset_reference))
		if positioned_label_count > native_normalization.MAX_POSITIONED_LABELS:
			if lines:
				lines.append("")
			lines.append(f"Native reconstruction needed: {positioned_label_count} positioned diagram labels.")
		if not lines:
			lines.append(f"Native reconstruction needed: {content.classification_reason}.")
		reasons.append(
			f"normalized {content.classification_reason} into native source-order content"
		)
		components.append(EmissionComponent(
			content.bounds if local_heading is None else content.bounds.union(local_heading.bounds),
			tuple(lines), "flow", tuple(image_references), tuple(source_image_ids),
			source_kind="native-reconstruction",
			source_ordinals=(() if local_heading is None else (local_heading.source_ordinal,)) +
				tuple(item[1] for item in flow_items),
			member_footprints=tuple(region.bounds for region in (*content.image_regions, *content_text_regions)) +
				(() if local_heading is None else (local_heading.bounds,)),
			classification_reason=content.kind,
		))
	tables_by_id = {table.source_ordinal: table for table in planned.data.tables}
	for table in planned.plan.tables:
		if table.table_id not in tables_by_id:
			raise ValueError(f"source table facts are missing for shape {table.table_id}")
		source_table = tables_by_id[table.table_id]
		if table.unsupported_reason and not source_table.unsupported_reason:
			raise ValueError(f"source table requires review: {table.unsupported_reason}")
		components.append(EmissionComponent(
			table.bounds, tuple(table_lines((source_table,))), "table",
			member_footprints=(table.bounds,),
		))
	return sorted(coalesce_text_flows(coalesce_bottom_footer(components)), key=component_read_key), reasons


#============================================
def coalesce_bottom_footer(components: list[EmissionComponent]) -> list[EmissionComponent]:
	"""Merge one or more broad bottom text boxes beneath exactly two disjoint peers."""
	footer = [item for item in components if item.kind == "text" and item.source_kind == "text-box"]
	peers = [item for item in components if item not in footer]
	if len(peers) != 2 or not footer or raw_components_overlap(peers):
		return components
	if any(not shallow_broad_footer(components, item) or item.bounds.top < peer.bounds.bottom - column_footer_padding(peer)
		for item in footer for peer in peers):
		return components
	footer.sort(key=component_read_key)
	if any(not follows_footer_lane(first, second) for first, second in zip(footer, footer[1:])):
		return components
	lines = tuple(line for index, item in enumerate(footer)
		for line in ((*item.lines, "") if index < len(footer) - 1 else item.lines))
	merged = EmissionComponent(union_bounds(tuple(item.bounds for item in footer)), lines, "flow",
		source_kind="text-box", source_ordinals=tuple(ordinal for item in footer for ordinal in item.source_ordinals),
		member_footprints=tuple(footprint for item in footer for footprint in component_footprints(item)),
		classification_reason=BOTTOM_FOOTER_RELATION_REASON)
	return [item for item in components if item not in footer] + [merged]


#============================================
def column_footer_padding(column: EmissionComponent) -> float:
	"""Bound source padding by both normalized and column-relative footer limits."""
	return min(FOOTER_IMAGE_PADDING_RATIO, FOOTER_COLUMN_BOTTOM_PADDING_RATIO * column.bounds.height)


#============================================
def component_read_key(component: EmissionComponent) -> tuple[float, float, int]:
	"""Order components geometrically; immutable source ordinals break exact ties."""
	return component.bounds.top, component.bounds.left, min(component.source_ordinals, default=0)


#============================================
def component_footprints(component: EmissionComponent) -> tuple[geometry.NormalizedBounds, ...]:
	"""Return immutable component members, with direct bounds for synthetic callers."""
	return component.member_footprints or (component.bounds,)


#============================================
def coalesce_text_flows(components: list[EmissionComponent]) -> list[EmissionComponent]:
	"""Join unique vertically stacked editable text blocks within one source lane."""
	available = set(range(len(components)))
	groups: list[tuple[int, ...]] = []
	for first in sorted(available, key=lambda index: component_read_key(components[index])):
		if first not in available or components[first].kind != "text":
			continue
		group = [first]
		while True:
			candidates = sorted((index for index in available - set(group)
				if components[index].kind == "text" and follows_text_lane(components[group[-1]], components[index])),
				key=lambda index: component_read_key(components[index]))
			if len(candidates) != 1 or image_interleaves_lane(components, components[group[-1]], components[candidates[0]]) or \
				(shallow_overlap_text_lane(components[group[-1]], components[candidates[0]]) and
					(shallow_overlap_lane_competes(components, components[group[-1]], components[candidates[0]]) or
						nontext_interleaves_lane(components, components[group[-1]], components[candidates[0]]))):
				break
			group.append(candidates[0])
		if len(group) > 1:
			groups.append(tuple(group))
			available.difference_update(group)
	result = [component for index, component in enumerate(components) if index in available]
	for group in groups:
		members = tuple(components[index] for index in group)
		lines = tuple(line for member_index, member in enumerate(members)
			for line in ((*member.lines, "") if member_index < len(members) - 1 else member.lines))
		result.append(EmissionComponent(union_bounds(tuple(member.bounds for member in members)), lines, "flow",
			source_ordinals=tuple(ordinal for member in members for ordinal in member.source_ordinals),
			member_footprints=tuple(footprint for member in members for footprint in component_footprints(member)),
			source_kind=members[0].source_kind if all(member.source_kind == members[0].source_kind for member in members) else ""))
	return result


#============================================
def follows_text_lane(first: EmissionComponent, second: EmissionComponent) -> bool:
	"""Recognize a separated next text block that shares a substantial lane."""
	gap = second.bounds.top - first.bounds.bottom
	return gap >= 0.0 and follows_same_lane(first, second) or shallow_overlap_text_lane(first, second)


#============================================
def shallow_overlap_text_lane(first: EmissionComponent, second: EmissionComponent) -> bool:
	"""Recognize one direct text-box continuation with a bounded source border overlap."""
	if component_read_key(first) >= component_read_key(second) or any(item.kind != "text" or
		item.source_kind != "text-box" or item.coarse_text_container or abs(item.rotation_degrees) >= 1.0 or
		len(component_footprints(item)) != 1 for item in (first, second)):
		return False
	overlap = min(first.bounds.bottom, second.bounds.bottom) - second.bounds.top
	return abs(first.bounds.left - second.bounds.left) <= .01 and \
		abs(first.bounds.width - second.bounds.width) <= max(first.bounds.width, second.bounds.width) * .02 and \
		0.0 < overlap <= SHALLOW_FLOW_MAX_VERTICAL_OVERLAP and overlap <= min(first.bounds.height, second.bounds.height) * SHALLOW_FLOW_MAX_SMALLER_HEIGHT_RATIO


#============================================
def shallow_overlap_lane_competes(components: list[EmissionComponent], first: EmissionComponent,
		second: EmissionComponent) -> bool:
	"""Leave two independent overlapping text lanes unmerged for manual topology review."""
	for candidate_first, candidate_second in itertools.permutations(components, 2):
		if (candidate_first, candidate_second) != (first, second) and shallow_overlap_text_lane(candidate_first, candidate_second) and \
			abs(candidate_first.bounds.left - first.bounds.left) > .01:
			return True
	return False


#============================================
def follows_footer_lane(first: EmissionComponent, second: EmissionComponent) -> bool:
	"""Allow bounded source padding only for ordered full-width footer members."""
	gap = second.bounds.top - first.bounds.bottom
	return component_read_key(first) < component_read_key(second) and gap >= -FOOTER_VERTICAL_PADDING_RATIO and \
		first.bounds.width >= FOOTER_MIN_WIDTH_RATIO and second.bounds.width >= FOOTER_MIN_WIDTH_RATIO and \
		follows_same_lane(first, second)


#============================================
def follows_same_lane(first: EmissionComponent, second: EmissionComponent) -> bool:
	"""Require substantial overlap, span agreement, and center agreement in one lane."""
	overlap = min(first.bounds.right, second.bounds.right) - max(first.bounds.left, second.bounds.left)
	overlap_ratio = overlap / min(first.bounds.width, second.bounds.width)
	center_offset = abs((first.bounds.left + first.bounds.right - second.bounds.left - second.bounds.right) / 2)
	return overlap_ratio >= FLOW_MIN_HORIZONTAL_OVERLAP_RATIO and \
		max(first.bounds.width, second.bounds.width) <= min(first.bounds.width, second.bounds.width) * FLOW_LANE_SPAN_VARIATION_RATIO and \
		center_offset <= min(first.bounds.width, second.bounds.width) * FLOW_LANE_CENTER_OFFSET_RATIO


#============================================
def image_interleaves_lane(components: list[EmissionComponent], first: EmissionComponent,
		second: EmissionComponent) -> bool:
	"""Preserve a spatial image component instead of folding text around it."""
	for component in components:
		if component.kind != "image" or not first.bounds.top <= component.bounds.top <= second.bounds.bottom:
			continue
		overlap = min(component.bounds.right, max(first.bounds.right, second.bounds.right)) - max(component.bounds.left, min(first.bounds.left, second.bounds.left))
		if overlap > 0:
			return True
	return False


#============================================
def nontext_interleaves_lane(components: list[EmissionComponent], first: EmissionComponent,
		second: EmissionComponent) -> bool:
	"""Keep a shallow text flow out of a lane occupied by another rendered component."""
	for component in components:
		if component in {first, second} or component.kind == "text" or \
			not first.bounds.top <= component.bounds.top <= second.bounds.bottom:
			continue
		if min(component.bounds.right, max(first.bounds.right, second.bounds.right)) > \
			max(component.bounds.left, min(first.bounds.left, second.bounds.left)):
			return True
	return False


#============================================
def components_overlap(components: list[EmissionComponent]) -> bool:
	"""Return whether direct components materially overlap beyond border contact."""
	permitted_pairs = {(record.first_index, record.second_index) for record in overlap_permissions(components)}
	for index, first in enumerate(components):
		for second_index, second in enumerate(components[index + 1:], start=index + 1):
			if (index, second_index) in permitted_pairs:
				continue
			for first_footprint in component_footprints(first):
				for second_footprint in component_footprints(second):
					if geometry.substantially_overlaps(first_footprint, second_footprint):
						return True
	return False


#============================================
def raw_components_overlap(components: list[EmissionComponent]) -> bool:
	"""Check member collisions without treating any composition as an allowed relation."""
	for index, first in enumerate(components):
		for second in components[index + 1:]:
			if any(geometry.substantially_overlaps(left, right) for left in component_footprints(first)
				for right in component_footprints(second)):
				return True
	return False


#============================================
def overlap_permissions(components: list[EmissionComponent]) -> tuple[OverlapPermission, ...]:
	"""Return only component-pair permissions proven by one unique native topology."""
	records: list[OverlapPermission] = []
	if coarse_inset_key_layout(components):
		record = pair_permission(components, 0, 1, "coarse-body-styled-inset", "two-panels")
		if record is not None:
			records.append(record)
	if coarse_picture_inset_layout(components):
		record = pair_permission(components, 0, 1, "coarse-body-picture-inset", "two-panels")
		if record is not None:
			records.append(record)
	if coarse_image_geometry(components) and not coarse_picture_inset_layout(components):
		record = pair_permission(components, 0, 1, "coarse-image-peer", "two-panels")
		if record is not None:
			records.append(record)
	if len(components) == 3:
		footer_indexes = [index for index, item in enumerate(components) if item.kind == "flow" and item.source_kind == "text-box"]
		if len(footer_indexes) == 1 and bottom_footer_structure(components, footer_indexes[0]):
			footer_index = footer_indexes[0]
			try:
				selected, _slots, _order = component_layout(components)
			except ValueError:
				selected = ""
			if selected in {"two-over-one-panels", "two-plus-one-panels"}:
				for peer_index in range(len(components)):
					if peer_index == footer_index:
						continue
					overlap = max(vertical_overlap(left, right) for left in component_footprints(components[footer_index])
						for right in component_footprints(components[peer_index]))
					if 0.0 < overlap <= FOOTER_IMAGE_PADDING_RATIO:
						record = pair_permission(components, peer_index, footer_index, "bottom-footer-padding", selected)
						if record is not None:
							records.append(record)
		caption_footer_indexes = [index for index, item in enumerate(components) if item.kind == "text" and item.source_kind == "text-box"]
		caption_indexes = [index for index, item in enumerate(components) if item.kind == "image" and
			item.source_kind == "picture" and len(component_footprints(item)) == 2]
		if len(caption_footer_indexes) == 1 and len(caption_indexes) == 1:
			footer_index, image_index = caption_footer_indexes[0], caption_indexes[0]
			footer, image = components[footer_index], components[image_index]
			overlap = vertical_overlap(component_footprints(image)[-1], footer.bounds)
			if shallow_broad_footer(components, footer) and 0.0 < overlap <= FOOTER_IMAGE_PADDING_RATIO and \
				not geometry.substantially_overlaps(component_footprints(image)[0], footer.bounds):
				record = pair_permission(components, footer_index, image_index, "caption-footer-padding", "two-plus-one-panels")
				if record is not None:
					records.append(record)
	return tuple(records)


#============================================
def pair_permission(components: list[EmissionComponent], first_index: int, second_index: int,
		relation: str, layout: str) -> OverlapPermission | None:
	"""Record one exact pair only after the full component set selects its native layout."""
	try:
		selected, _slots, order = component_layout(components)
	except ValueError:
		return None
	if selected != layout:
		return None
	if first_index > second_index:
		first_index, second_index = second_index, first_index
	first, second = components[first_index], components[second_index]
	return OverlapPermission(first_index, second_index, relation, component_footprints(first),
		component_footprints(second), max(vertical_overlap(left, right) for left in component_footprints(first)
		for right in component_footprints(second)), selected, order)


#============================================
def vertical_overlap(first: geometry.NormalizedBounds, second: geometry.NormalizedBounds) -> float:
	"""Measure signed vertical intersection for a recorded source-padding relation."""
	return min(first.bottom, second.bottom) - max(first.top, second.top)


#============================================
def bottom_footer_structure(components: list[EmissionComponent], footer_index: int) -> bool:
	"""Validate one merged footer against exactly two disjoint top peers."""
	footer = components[footer_index]
	peers = [item for index, item in enumerate(components) if index != footer_index]
	return len(peers) == 2 and not raw_components_overlap(peers) and shallow_broad_footer(components, footer) and \
		all(footprint.top >= peer.bounds.bottom - column_footer_padding(peer)
			for footprint in component_footprints(footer) for peer in peers)


#============================================
def shallow_broad_footer(components: list[EmissionComponent], footer: EmissionComponent) -> bool:
	"""Recognize one short lower textbox broad enough to be a footer reference."""
	envelope = union_bounds(tuple(item.bounds for item in components))
	return footer.bounds.width >= envelope.width * FOOTER_MIN_WIDTH_RATIO and \
		footer.bounds.height <= envelope.height * FOOTER_MAX_HEIGHT_RATIO


#============================================
def coarse_image_geometry(components: list[EmissionComponent]) -> bool:
	"""Recognize source geometry eligible for the explicit coarse-picture relation."""
	if len(components) != 2:
		return False
	coarse = next((item for item in components if item.kind == "text" and item.coarse_text_container), None)
	image = next((item for item in components if item.kind == "image" and item.source_kind == "picture"), None)
	if coarse is None or image is None or len(component_footprints(coarse)) != 1 or len(component_footprints(image)) != 1:
		return False
	coarse_center_y = (coarse.bounds.top + coarse.bounds.bottom) / 2
	image_center_y = (image.bounds.top + image.bounds.bottom) / 2
	coarse_center_x = (coarse.bounds.left + coarse.bounds.right) / 2
	image_center_x = (image.bounds.left + image.bounds.right) / 2
	if abs(coarse_center_y - image_center_y) > min(coarse.bounds.height, image.bounds.height) * COARSE_IMAGE_ROW_CENTER_RATIO or \
		abs(coarse_center_x - image_center_x) < min(coarse.bounds.width, image.bounds.width) * COARSE_IMAGE_SIDE_BY_SIDE_RATIO:
		return False
	return True


#============================================
def gallery_eligible(components: list[EmissionComponent]) -> bool:
	"""Allow gallery only for equal-status, non-overlapping image components."""
	if not 2 <= len(components) <= 6 or not all(item.kind == "image" for item in components):
		return False
	if components_overlap(components):
		return False
	areas = [item.bounds.width * item.bounds.height for item in components]
	aspects = [item.bounds.width / item.bounds.height for item in components]
	if max(areas) > min(areas) * GALLERY_AREA_VARIATION_RATIO or \
		max(aspects) > min(aspects) * GALLERY_ASPECT_VARIATION_RATIO:
		return False
	if len(components) == 2:
		return False
	if len(components) == 3:
		centers_x = [(item.bounds.left + item.bounds.right) / 2 for item in components]
		centers_y = [(item.bounds.top + item.bounds.bottom) / 2 for item in components]
		return (
			min(centers_x) < max(centers_x) and
			max(centers_y) - min(centers_y) <= GALLERY_LINE_CENTER_TOLERANCE
		) or (
			min(centers_y) < max(centers_y) and
			max(centers_x) - min(centers_x) <= GALLERY_LINE_CENTER_TOLERANCE
		)
	try:
		component_layout(components)
	except ValueError:
		return False
	return True


#============================================
def component_layout(components: list[EmissionComponent]) -> tuple[str, tuple[str, ...], tuple[int, ...]]:
	"""Match source components to native cell geometry without source-specific rules."""
	if not 1 <= len(components) <= 6:
		raise ValueError("source components require manual layout review before Djot emission")
	if coarse_inset_key_layout(components):
		return "two-panels", slide_lib.layout_engine.layout_contract("two-panels").slot_names, (0, 1)
	if coarse_picture_inset_layout(components):
		picture_index = next(index for index, item in enumerate(components) if item.kind == "image")
		body_index = next(index for index, item in enumerate(components) if item.kind == "text")
		return "two-panels", slide_lib.layout_engine.layout_contract("two-panels").slot_names, (picture_index, body_index) \
			if components[picture_index].classification_reason.endswith(":left") else (body_index, picture_index)
	footer_match = bottom_footer_layout(components)
	if footer_match is not None:
		_score, order = footer_match
		return "two-over-one-panels", slide_lib.layout_engine.layout_contract("two-over-one-panels").slot_names, order
	explanatory_match = asymmetric_explanatory_pair_layout(components)
	if explanatory_match is not None:
		_score, order = explanatory_match
		return "two-panels", slide_lib.layout_engine.layout_contract("two-panels").slot_names, order
	match = topology.ordinary_layout_match(
		tuple(component.bounds for component in components), not coarse_image_geometry(components),
	)
	if match is None:
		bounds = ", ".join(str(component.bounds) for component in components)
		raise ValueError(f"ambiguous topology bounds [{bounds}]")
	name, order = match
	return name, slide_lib.layout_engine.layout_contract(name).slot_names, order


def coarse_inset_key_layout(components: list[EmissionComponent]) -> bool:
	"""Assign one body and wholly contained compact key to the existing two panels."""
	if len(components) != 2:
		return False
	body = next((item for item in components if item.coarse_text_container), None)
	key = next((item for item in components if item is not body), None)
	return body is not None and key is not None and key.source_kind == "native-reconstruction" and \
		key.classification_reason == "styled-inset-key" and \
		key.bounds.left >= .65 and key.bounds.width <= .25 and key.bounds.height <= .20 and \
		body.bounds.left <= key.bounds.left and key.bounds.right <= body.bounds.right and \
		body.bounds.top <= key.bounds.top and key.bounds.bottom <= body.bounds.bottom


def coarse_picture_inset_layout(components: list[EmissionComponent]) -> bool:
	"""Assign one proven coarse body and direct picture inset to opposite panels."""
	if len(components) != 2 or any(not item.classification_reason.startswith("coarse-body-picture-inset:") for item in components):
		return False
	return sum(item.kind == "text" and item.coarse_text_container for item in components) == 1 and \
		sum(item.kind == "image" and item.source_kind == "picture" for item in components) == 1 and \
		len({item.classification_reason for item in components}) == 1


#============================================
def bottom_footer_layout(components: list[EmissionComponent]) -> tuple[float, tuple[int, ...]] | None:
	"""Accept only a unique same-band peer/footer relation within its local score ceiling."""
	footer_indexes = [index for index, item in enumerate(components) if item.kind == "flow" and
		item.source_kind == "text-box" and item.classification_reason == BOTTOM_FOOTER_RELATION_REASON]
	if len(components) != 3 or len(footer_indexes) != 1 or not bottom_footer_structure(components, footer_indexes[0]):
		return None
	peers = [item for index, item in enumerate(components) if index != footer_indexes[0]]
	if not topology.material(peers[0].bounds.top, peers[0].bounds.height, peers[1].bounds.top, peers[1].bounds.height):
		return None
	source = topology.normalized_boxes(tuple(component.bounds for component in components))
	slots = slide_lib.layout_engine.layout_contract("two-over-one-panels").topology_slots
	matches = [(topology.score(source, slots, order), order) for order in itertools.permutations(range(3))
		if order[2] == footer_indexes[0] and topology.relations_match(source, slots, order)]
	if not matches:
		return None
	score = min(item[0] for item in matches)
	if score > BOTTOM_FOOTER_SCORE_CEILING:
		return None
	order = min(item for item_score, item in matches if abs(item_score - score) <= 1e-9)
	return score, order


#============================================
def asymmetric_explanatory_pair_layout(components: list[EmissionComponent]) -> tuple[float, tuple[int, ...]] | None:
	"""Accept one aligned, disjoint coarse-plus-compact text pair at a local ceiling."""
	if not asymmetric_explanatory_pair(components):
		return None
	source = topology.normalized_boxes(tuple(component.bounds for component in components))
	candidates: list[tuple[str, list[tuple[float, tuple[int, ...]]]]] = []
	for name in slide_lib.layout_engine.registered_layout_names():
		spec = slide_lib.layout_engine.layout_contract(name)
		if not spec.topology_matchable or spec.cell_count != 2:
			continue
		slots = spec.topology_slots
		matches = [(topology.score(source, slots, order), order) for order in itertools.permutations(range(2))
			if topology.relations_match(source, slots, order)]
		if matches:
			candidates.append((spec.name, matches))
	if [name for name, _matches in candidates] != ["two-panels"]:
		return None
	matches = candidates[0][1]
	score = min(item[0] for item in matches)
	if score > ASYMMETRIC_EXPLANATORY_PAIR_MAX_SCORE:
		return None
	order = min(item for item_score, item in matches if abs(item_score - score) <= 1e-9)
	return score, order


#============================================
def asymmetric_explanatory_pair(components: list[EmissionComponent]) -> bool:
	"""Recognize only two direct, aligned textual components with asymmetric roles."""
	if len(components) != 2 or any(item.kind != "text" or not any(line.strip() for line in item.lines) or
		item.source_kind in {"table", "native-reconstruction"} or item.classification_reason or
		len(component_footprints(item)) != 1 for item in components):
		return False
	coarse = [item for item in components if item.coarse_text_container]
	compact = [item for item in components if not item.coarse_text_container]
	if len(coarse) != 1 or len(compact) != 1 or compact[0].placeholder_confidence != 0.0 or \
		raw_components_overlap(components):
		return False
	large, small = coarse[0], compact[0]
	if small.bounds.width * small.bounds.height > large.bounds.width * large.bounds.height * \
		ASYMMETRIC_EXPLANATORY_COMPACT_AREA_RATIO:
		return False
	left, right = sorted(components, key=lambda item: item.bounds.left)
	return right.bounds.left - left.bounds.right >= 0.05 and abs(left.bounds.top - right.bounds.top) <= 0.03


#============================================
def union_bounds(bounds: tuple[geometry.NormalizedBounds, ...]) -> geometry.NormalizedBounds:
	"""Return the geometric union of already-normalized source rectangles."""
	result = bounds[0]
	for item in bounds[1:]:
		result = result.union(item)
	return result


#============================================
def source_slide_context(planned: PlannedSlide) -> str:
	"""Return the stable source coordinates for one emission diagnostic."""
	context = f"source slide {planned.data.source_index}"
	if planned.visible_page_index is not None:
		context += f" (visible page {planned.visible_page_index})"
	return context


#============================================
def contextualize_slide_error(planned: PlannedSlide, error: ValueError) -> ValueError:
	"""Attach one source location while preserving the underlying diagnostic."""
	if str(error).startswith("source slide "):
		return error
	return ValueError(f"{source_slide_context(planned)}: {error}")
#============================================
def _render_planned_slide(
	planned: PlannedSlide,
	is_first: bool,
) -> tuple[list[str], str, list[str]]:
	"""Emit one geometry plan, never combining text and imagery in one cell."""
	if planned.plan is None:
		raise ValueError("hidden slides cannot be emitted")
	data = planned.data
	plan = planned.plan
	if plan.multiple_choice is not None:
		return render_multiple_choice(planned)
	reasons = list(data.review_reasons)
	heading = []
	if plan.title.region is not None:
		heading = [f"# {' '.join(render_runs(runs) for _level, runs in plan.title.region.paragraphs)}"]
	components, component_reasons = emit_components(planned)
	reasons.extend(component_reasons)
	if plan.review_reason:
		reasons.append(plan.review_reason)
	if not components:
		if heading:
			layout = "title-slide" if is_first else "title-only"
			return [f"=== layout: {layout}", "", *heading], layout, reasons
		return ["=== layout: blank"], "blank", reasons
	emitted_image_ids = [
		image_id for component in components for image_id in component.source_image_ids
	]
	emitted_ids = set(emitted_image_ids)
	required_regions = tuple(image for slot in plan.slots for image in slot.image_regions) + (
		() if plan.content_region is None else plan.content_region.image_regions
	)
	available_references = {image.asset_path for image in data.images}
	required_ids = {
		(image.source_ordinal, image.asset_reference)
		for image in required_regions if image.asset_reference in available_references
	}
	if emitted_ids != required_ids or len(emitted_image_ids) != len(required_ids):
		raise ValueError("did not preserve every outside picture exactly once")
	if components_overlap(components):
		reasons.append("normalized overlapping legacy components into one native source-order panel")
		return native_normalization.one_panel_lines(heading, components), "one-panel", reasons
	if is_first and heading and len(components) == 1 and components[0].kind == "text" and \
		all(line.startswith("## ") for line in components[0].lines):
		return ["=== layout: title-slide", "", *heading, "", *components[0].lines], "title-slide", reasons
	if gallery_eligible(components):
		return ["=== layout: gallery", "", *heading, "", "@gallery", "",
			*(line for component in components for line in component.lines)], "gallery", reasons
	try:
		layout, slots, order = component_layout(components)
	except ValueError as error:
		reasons.append(f"normalized {error} into one native source-order panel")
		return native_normalization.one_panel_lines(heading, components), "one-panel", reasons
	lines = [f"=== layout: {layout}", "", *heading]
	for index, slot in zip(order, slots, strict=True):
		component = components[index]
		lines.extend(("", f"@{slot}", "", *component.lines))
	return lines, layout, reasons


#============================================
def render_planned_slide(
	planned: PlannedSlide,
	is_first: bool,
) -> tuple[list[str], str, list[str]]:
	"""Emit one planned slide with source coordinates on every ValueError."""
	try:
		return _render_planned_slide(planned, is_first)
	except ValueError as error:
		contextual_error = contextualize_slide_error(planned, error)
		if contextual_error is error:
			raise
		raise contextual_error from error


#============================================
def render_planned_djot(
	planned_slides: list[PlannedSlide],
) -> tuple[str, list[dict[str, object]]]:
	"""Emit all visible planned slides and an auditable geometry import report."""
	lines: list[str] = []
	records: list[dict[str, object]] = []
	for planned in (item for item in planned_slides if not item.data.hidden):
		if lines:
			lines.append("")
		slide_lines, layout, reasons = render_planned_slide(
			planned, planned.visible_page_index == 1,
		)
		lines.extend(slide_lines)
		content = planned.plan.content_region if planned.plan else None
		records.append({
			"source_slide": planned.data.source_index,
			"visible_page": planned.visible_page_index,
			"layout": layout,
			"text_blocks": len(planned.data.text_blocks),
			"images": len(planned.data.images),
			"notes_omitted": len(planned.data.notes),
			"review_reasons": sorted(set(reasons)),
			"native_table_count": len(planned.plan.tables) if planned.plan else 0,
			"content_region": None if content is None else {
				"region_key": content.region_key,
				"kind": content.kind,
				"classification_reason": content.classification_reason,
				"local_heading_source_ordinal": None if content.local_heading is None else content.local_heading.source_ordinal,
			},
			"multiple_choice": None if planned.plan is None or planned.plan.multiple_choice is None else {
				"reason": planned.plan.multiple_choice.reason,
				"question": {
					"source_ordinal": planned.plan.multiple_choice.question.source_ordinal,
					"bounds": dataclasses.asdict(planned.plan.multiple_choice.question.bounds),
				},
				"answer": {
					"source_ordinal": planned.plan.multiple_choice.answer.source_ordinal,
					"bounds": dataclasses.asdict(planned.plan.multiple_choice.answer.bounds),
				},
				"image": None if planned.plan.multiple_choice.image is None else {
					"source_ordinal": planned.plan.multiple_choice.image.source_ordinal,
					"bounds": dataclasses.asdict(planned.plan.multiple_choice.image.bounds),
				},
				"question_visual_region": None if planned.plan.multiple_choice.question_visual_region is None else {
					"region_key": planned.plan.multiple_choice.question_visual_region.region_key,
					"classification_reason": planned.plan.multiple_choice.question_visual_region.classification_reason,
				},
			},
		})
	return "\n".join(lines).rstrip() + "\n", records
