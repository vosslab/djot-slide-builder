"""Render imported-slide facts and geometry plans as bounded Djot source."""

# Standard Library
import dataclasses

# local repo modules
import slide_lib.importers.emission_topology as emission_topology
import slide_lib.importers.djot_text as djot_text
import slide_lib.importers.emission_flow as emission_flow
import slide_lib.importers.source_regions as source_regions
import slide_lib.importers.geometry as geometry
import slide_lib.importers.image_annotations as image_annotations
import slide_lib.importers.import_report as import_report
import slide_lib.importers.native_normalization as native_normalization
import slide_lib.importers.slide_plan as slide_plan
import slide_lib.importers.source_model as source_model
import slide_lib.importers.source_table_styles as source_table_styles
import slide_lib.importers.visual_relations as visual_relations


@dataclasses.dataclass(frozen=True)
class PlannedSlide:
	"""Imported-slide facts and their geometry-first projection."""
	data: source_model.SlideData
	plan: slide_plan.SlidePlan | None
	text_regions: tuple[source_regions.SourceTextRegion, ...] = ()
	image_regions: tuple[source_regions.SourceImageRegion, ...] = ()
	visible_page_index: int | None = None
	overlays: tuple[image_annotations.SourceOverlay, ...] = ()
#============================================
def image_djot(image: source_model.ImageAsset) -> str:
	"""Render one imported-deck image as a Djot component image."""
	return f"![{djot_text.djot_text(image.alt_text)}]({image.asset_path})"


#============================================
def region_lines(regions: tuple[source_regions.SourceTextRegion, ...]) -> list[str]:
	"""Project retained source text without changing its paragraph hierarchy."""
	lines: list[str] = []
	for region in regions:
		for level, runs in region.paragraphs:
			text = djot_text.render_runs(runs)
			if region.is_subtitle:
				lines.append(f"## {text}")
			else:
				lines.append(f"{'  ' * level}- {text}")
	return lines


#============================================
def multiple_choice_question_lines(region: source_regions.SourceTextRegion) -> list[str]:
	"""Keep a source prompt before nested choices when hierarchy supplies one."""
	paragraphs = region.paragraphs
	first_level = paragraphs[0][0]
	choice_start = 1 if any(level > first_level for level, _text in paragraphs[1:]) else 0
	lines = [] if choice_start == 0 else [djot_text.render_runs(paragraphs[0][1]), ""]
	choice_level = min(level for level, _text in paragraphs[choice_start:])
	for level, runs in paragraphs[choice_start:]:
		lines.append(f"{'  ' * (level - choice_level)}- {djot_text.render_runs(runs)}")
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
	answer_lines = tuple(djot_text.render_runs(runs) for _level, runs in choice.answer.paragraphs)
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
		if table.cell_rows:
			cell_styles = []
			for row in table.cell_rows:
				for cell in row:
					if cell.covered:
						continue
					attributes, reason = source_table_styles.cell_attributes(cell)
					if reason:
						raise ValueError(f"source table requires review: {reason}")
					cell_styles.append(attributes)
			common = {name: value for name, value in cell_styles[0].items()
				if name != "colspan" and all(attributes.get(name) == value for attributes in cell_styles)}
			defaults = dict(common)
			if table.column_widths:
				widths = ",".join(f"{width / min(table.column_widths):.6g}" for width in table.column_widths)
				defaults["column-widths"] = widths
			if defaults:
				encoded = source_table_styles.attribute_text(defaults)
				lines.append(f"{{{encoded}}}")
			for row_index, row in enumerate(table.cell_rows):
				values: list[str] = []
				for cell in row:
					if cell.covered:
						continue
					text = djot_text.render_runs(cell.runs).replace("|", "\\|")
					attributes, reason = source_table_styles.cell_attributes(cell)
					if reason:
						raise ValueError(f"source table requires review: {reason}")
					attributes = {name: value for name, value in attributes.items() if name not in common}
					if attributes:
						encoded = source_table_styles.attribute_text(attributes)
						text = f"[{text}]{{{encoded}}}"
					values.append(text)
				lines.append(f"| {' | '.join(values)} |")
				if row_index == 0 and table.headers:
					lines.append(f"| {' | '.join('---' for _cell in row)} |")
			continue
		if table.headers:
			header_values = tuple(djot_text.render_runs(cell).replace("|", "\\|") for cell in table.headers)
			lines.append(f"| {' | '.join(header_values)} |")
			lines.append(f"| {' | '.join('---' for _cell in table.headers)} |")
		for row in table.rows:
			values = tuple(djot_text.render_runs(cell).replace("|", "\\|") for cell in row)
			lines.append(f"| {' | '.join(values)} |")
	return lines


#============================================
def slot_image_lines(
	regions: tuple[source_regions.SourceImageRegion, ...],
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
		text_regions: tuple[source_regions.SourceTextRegion, ...],
		image_regions: tuple[source_regions.SourceImageRegion, ...],
) -> tuple[source_regions.SourceTextRegion, ...]:
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
	if any(item.bounds.width < span * emission_flow.FOOTER_MIN_WIDTH_RATIO or
		item.bounds.top < peer.bounds.bottom - emission_flow.FOOTER_IMAGE_PADDING_RATIO or
		item.bounds.top < image.bounds.bottom - emission_flow.FOOTER_IMAGE_PADDING_RATIO for item in footer):
		return ()
	return footer


#============================================
def emit_components(
	planned: PlannedSlide,
) -> tuple[list[emission_flow.EmissionComponent], list[str]]:
	"""Project planned components, retaining proven mixed vertical flows in one cell."""
	if planned.plan is None:
		raise ValueError("component emission requires a visible slide plan")
	components: list[emission_flow.EmissionComponent] = []
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
			components.append(emission_flow.EmissionComponent(
				region_bounds(tuple(item[3] for item in flow_items)), tuple(lines), "flow",
				tuple(image_references), tuple(source_image_ids), source_ordinals=tuple(source_ordinals),
				member_footprints=tuple(item[0] for item in flow_items),
				source_order=min((item[3].z_order for item in flow_items if item[3].z_order), default=()),
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
				components.append(emission_flow.EmissionComponent(
					text.bounds, tuple(region_lines((text,))), "text", (), (),
					text.placeholder_confidence >= 0.75, text.source_kind, (text.source_ordinal,), (text.bounds,),
					placeholder_confidence=text.placeholder_confidence,
					rotation_degrees=text.rotation_degrees,
					classification_reason=slot.relation_id,
					source_order=text.z_order,
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
					components.append(emission_flow.EmissionComponent(
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
						source_order=min((item.z_order for item in (region, caption)
							if item is not None and item.z_order), default=()),
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
			[f"## {' '.join(djot_text.render_runs(runs) for _level, runs in local_heading.paragraphs)}"])
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
		components.append(emission_flow.EmissionComponent(
			content.bounds if local_heading is None else content.bounds.union(local_heading.bounds),
			tuple(lines), "flow", tuple(image_references), tuple(source_image_ids),
			source_kind="native-reconstruction",
			source_ordinals=(() if local_heading is None else (local_heading.source_ordinal,)) +
				tuple(item[1] for item in flow_items),
			member_footprints=tuple(region.bounds for region in (*content.image_regions, *content_text_regions)) +
				(() if local_heading is None else (local_heading.bounds,)),
			classification_reason=content.kind,
			source_order=min((item.z_order for item in
				(*content.image_regions, *content_text_regions,
					*(() if local_heading is None else (local_heading,))) if item.z_order), default=()),
		))
	tables_by_id = {table.source_ordinal: table for table in planned.data.tables}
	for table in planned.plan.tables:
		if table.table_id not in tables_by_id:
			raise ValueError(f"source table facts are missing for shape {table.table_id}")
		source_table = tables_by_id[table.table_id]
		if table.unsupported_reason and not source_table.unsupported_reason:
			raise ValueError(f"source table requires review: {table.unsupported_reason}")
		components.append(emission_flow.EmissionComponent(
			table.bounds, tuple(table_lines((source_table,))), "table",
			member_footprints=(table.bounds,),
			source_ordinals=(table.table_id,),
			source_order=min((item.z_order for item in table.text_regions if item.z_order), default=()),
		))
	return sorted(emission_flow.coalesce_text_flows(emission_flow.coalesce_bottom_footer(components)), key=emission_flow.component_read_key), reasons


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


def render_big_image_with_overlays(planned: PlannedSlide) -> tuple[list[str], str, list[str]] | None:
	"""Emit one proven image-owned annotation composition as native big-image Djot."""
	if not planned.overlays:
		return None
	data = planned.data
	if len(data.images) != 1 or len(planned.image_regions) != 1 or data.tables:
		return None
	image = planned.image_regions[0]
	if image.source_kind != "picture" or image.asset_reference != data.images[0].asset_path:
		return None
	title_region = None if planned.plan is None else planned.plan.title.region
	caption_regions = tuple(region for region in planned.text_regions if region is not title_region)
	if len(caption_regions) > 2:
		return None
	caption_lines = []
	for region in (() if title_region is None else (title_region,)) + caption_regions:
		caption_lines.extend(djot_text.render_runs(runs) for _level, runs in region.paragraphs)
	if not caption_lines:
		caption_lines.append(data.images[0].alt_text)
	return image_annotations.render_big_image(planned.overlays, image,
		image_djot(data.images[0]), caption_lines, data.review_reasons)


#============================================
def _render_planned_slide(planned: PlannedSlide, is_first: bool) -> tuple[list[str], str, list[str]]:
	"""Emit one geometry plan with mixed flows or separate cells as relations require."""
	if planned.plan is None:
		raise ValueError("slide has no import plan")
	data = planned.data
	plan = planned.plan
	if plan.multiple_choice is not None:
		return render_multiple_choice(planned)
	reasons = list(data.review_reasons)
	heading = []
	if plan.title.region is not None:
		heading = [f"# {' '.join(djot_text.render_runs(runs) for _level, runs in plan.title.region.paragraphs)}"]
	if data.page_evidence is not None and data.page_evidence.is_section_page():
		section_lines = [djot_text.render_runs(runs) for block in data.text_blocks for _level, runs in block.lines]
		if section_lines:
			return ["=== layout: section", "", f"# {' '.join(section_lines)}"], "section", reasons
	big_image = render_big_image_with_overlays(planned)
	if big_image is not None:
		return big_image
	if planned.overlays:
		reasons.append("native annotations could not be assigned to exactly one image")
	components, component_reasons = emit_components(planned)
	reasons.extend(component_reasons)
	if plan.review_reason:
		reasons.append(plan.review_reason)
	if not components:
		if heading:
			layout = "title-slide" if is_first else "title-only"
			return [f"=== layout: {layout}", "", *heading], layout, reasons
		return ["=== layout: blank"], "blank", reasons
	emitted_image_ids = [image_id for component in components for image_id in component.source_image_ids]
	emitted_ids = set(emitted_image_ids)
	required_regions = tuple(image for slot in plan.slots for image in slot.image_regions) + (() if plan.content_region is None else plan.content_region.image_regions)
	available_references = {image.asset_path for image in data.images}
	required_ids = {(image.source_ordinal, image.asset_reference) for image in required_regions if image.asset_reference in available_references}
	if emitted_ids != required_ids or len(emitted_image_ids) != len(required_ids):
		raise ValueError("did not preserve every outside picture exactly once")
	if emission_topology.components_overlap(components):
		if any(component.kind == "table" for component in components):
			reasons.append("normalized overlapping legacy components into a table-safe native grid")
			lines, layout = native_normalization.table_grid_lines(heading, components)
			return lines, layout, reasons
		reasons.append("normalized overlapping legacy components into one native source-order panel")
		return native_normalization.one_panel_lines(heading, components), "one-panel", reasons
	if is_first and heading and len(components) == 1 and components[0].kind == "text" and all(line.startswith("## ") for line in components[0].lines):
		return ["=== layout: title-slide", "", *heading, "", *components[0].lines], "title-slide", reasons
	if emission_topology.gallery_eligible(components):
		return ["=== layout: gallery", "", *heading, "", "@gallery", "", *(line for component in components for line in component.lines)], "gallery", reasons
	try:
		layout, slots, order = emission_topology.component_layout(components)
	except ValueError as error:
		if any(component.kind == "table" for component in components):
			reasons.append(f"normalized {error} into a table-safe native source-order grid")
			lines, layout = native_normalization.table_grid_lines(heading, components)
			return lines, layout, reasons
		reasons.append(f"normalized {error} into one native source-order panel")
		return native_normalization.one_panel_lines(heading, components), "one-panel", reasons
	lines = [f"=== layout: {layout}", "", *heading]
	for index, slot in zip(order, slots, strict=True):
		component = components[index]
		lines.extend(("", f"@{slot}", "", *component.lines))
	return lines, layout, reasons


#============================================
def render_planned_slide(planned: PlannedSlide, is_first: bool) -> tuple[list[str], str, list[str]]:
	"""Emit one planned slide with source coordinates on every ValueError."""
	try:
		return _render_planned_slide(planned, is_first)
	except ValueError as error:
		contextual_error = contextualize_slide_error(planned, error)
		if contextual_error is error:
			raise
		raise contextual_error from error


#============================================
def render_planned_djot(planned_slides: list[PlannedSlide]) -> tuple[str, list[dict[str, object]]]:
	"""Emit every planned slide, preserving source order and hidden metadata."""
	lines: list[str] = []
	records: list[dict[str, object]] = []
	for planned in planned_slides:
		if lines:
			lines.append("")
		slide_lines, layout, reasons = render_planned_slide(planned, planned.visible_page_index == 1)
		if planned.data.hidden:
			slide_lines.insert(1, "hidden: true")
		if reasons:
			slide_lines.insert(1, "@replaceme")
		lines.extend(slide_lines)
		records.append(import_report.slide_record(planned.data, planned.plan, planned.visible_page_index, layout, reasons))
	return "\n".join(lines).rstrip() + "\n", records
