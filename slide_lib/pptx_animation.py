"""Build the small, editable OOXML timing surface used by native export."""

# PIP3 modules
from pptx.oxml.xmlchemy import OxmlElement

_APPEAR_DURATION_MS = "1"
_FADE_DURATION_MS = "1000"


class AnimationError(ValueError):
	"""Report an unsupported or unsafe timing-tree operation."""


class PptxAnimationWriter:
	"""Collect source-neutral reveals, then write one timing tree for one slide."""
	def __init__(self, slide: object) -> None:
		self.slide = slide
		self.registrations: list[tuple[object, object, tuple[int, int] | None]] = []
		self.next_timing_id = 1
		self.ensure_no_timing()

	#============================================
	def ensure_no_timing(self) -> None:
		"""Reject a slide that already owns timing, including compatibility content."""
		for element in self.slide._element.iter():
			if element.tag.endswith("}timing"):
				raise AnimationError("native export requires a slide without existing timing")

	#============================================
	def register(self, shape: object, reveal: object,
			paragraph_range: tuple[int, int] | None = None) -> None:
		"""Register one whole-shape or inclusive paragraph-range click reveal."""
		if getattr(getattr(reveal, "trigger", None), "value", None) != "on-click":
			raise AnimationError("native export supports on-click reveals only")
		if paragraph_range is None and getattr(getattr(reveal, "sequence", None), "value", None) == "paragraphs":
			raise AnimationError("paragraph timing requires an inclusive paragraph range")
		if paragraph_range is not None and paragraph_range[0] < 0:
			raise AnimationError("paragraph timing ranges must be zero-based and non-negative")
		if paragraph_range is not None and paragraph_range[1] < paragraph_range[0]:
			raise AnimationError("paragraph timing ranges must be inclusive")
		self.registrations.append((shape, reveal, paragraph_range))

	#============================================
	def element(self, name: str, **attributes: str) -> object:
		"""Create one OOXML element with its declared attributes."""
		result = OxmlElement(name)
		for key, value in attributes.items():
			result.set(key, value)
		return result

	#============================================
	def timing_id(self) -> str:
		"""Allocate a timing-node identifier independent from Office shape IDs."""
		value = str(self.next_timing_id)
		self.next_timing_id += 1
		return value

	#============================================
	def shape_id(self, shape: object) -> str:
		"""Return the target shape's non-visual Office ID."""
		matches = shape.element.xpath(".//p:cNvPr")
		if len(matches) != 1:
			raise AnimationError("animation target must have one non-visual shape ID")
		shape_id = matches[0].get("id")
		if shape_id is None:
			raise AnimationError("animation target is missing its non-visual shape ID")
		return shape_id

	#============================================
	def target(self, shape: object, paragraph_range: tuple[int, int] | None) -> object:
		"""Build a whole-shape or paragraph target from a stable native shape ID."""
		target = self.element("p:tgtEl")
		shape_target = self.element("p:spTgt", spid=self.shape_id(shape))
		if paragraph_range is not None:
			text_element = self.element("p:txEl")
			text_element.append(self.element("p:pRg", st=str(paragraph_range[0]), end=str(paragraph_range[1])))
			shape_target.append(text_element)
		target.append(shape_target)
		return target

	#============================================
	def behavior(self, shape: object, paragraph_range: tuple[int, int] | None,
			duration_ms: str, visibility: bool = False) -> object:
		"""Build the common behavior target for a click effect."""
		behavior = self.element("p:cBhvr", override="childStyle")
		behavior.append(self.element("p:cTn", id=self.timing_id(), dur=duration_ms, fill="hold"))
		behavior.append(self.target(shape, paragraph_range))
		if visibility:
			attributes = self.element("p:attrNameLst")
			attributes.append(self.element("p:attrName"))
			attributes[0].text = "style.visibility"
			behavior.append(attributes)
		return behavior

	#============================================
	def effect_step(self, shape: object, reveal: object,
			paragraph_range: tuple[int, int] | None) -> object:
		"""Build one ordered click effect for an appear or fade reveal."""
		parallel = self.element("p:par")
		container = self.element("p:cTn", id=self.timing_id(), fill="hold", nodeType="clickEffect")
		starts = self.element("p:stCondLst")
		starts.append(self.element("p:cond", delay="0", evt="onClick"))
		container.append(starts)
		children = self.element("p:childTnLst")
		if getattr(getattr(reveal, "effect", None), "value", None) == "appear":
			effect = self.element("p:set")
			effect.append(self.behavior(shape, paragraph_range, _APPEAR_DURATION_MS, True))
			to = self.element("p:to")
			to.append(self.element("p:strVal", val="visible"))
			effect.append(to)
		elif getattr(getattr(reveal, "effect", None), "value", None) == "fade":
			effect = self.element("p:animEffect", transition="in", filter="fade")
			effect.append(self.behavior(shape, paragraph_range, _FADE_DURATION_MS))
		else:
			raise AnimationError(f"unsupported plan reveal effect: {getattr(reveal, 'effect', None)}")
		children.append(effect)
		container.append(children)
		parallel.append(container)
		return parallel

	#============================================
	def build_entry(self, shape: object, paragraph_range: tuple[int, int] | None) -> object:
		"""Build the matching PPTX build-list entry for one source reveal."""
		entry = self.element("p:bldP", spid=self.shape_id(shape), grpId="0", uiExpand="1")
		entry.set("build", "p" if paragraph_range is not None else "allAtOnce")
		return entry

	#============================================
	def finalize(self) -> None:
		"""Write exactly one source-ordered timing tree after all layout shapes exist."""
		self.ensure_no_timing()
		if not self.registrations:
			return
		timing = self.element("p:timing")
		timing_nodes = self.element("p:tnLst")
		root_parallel = self.element("p:par")
		root = self.element("p:cTn", id=self.timing_id(), dur="indefinite", restart="never", nodeType="tmRoot")
		root_children = self.element("p:childTnLst")
		sequence = self.element("p:seq", concurrent="1", nextAc="seek", prevAc="skip")
		main = self.element("p:cTn", id=self.timing_id(), dur="indefinite", nodeType="mainSeq")
		steps = self.element("p:childTnLst")
		builds = self.element("p:bldLst")
		for shape, reveal, paragraph_range in sorted(self.registrations,
				key=lambda entry: getattr(entry[1], "activation_order", len(self.registrations))):
			steps.append(self.effect_step(shape, reveal, paragraph_range))
			builds.append(self.build_entry(shape, paragraph_range))
		main.append(steps)
		sequence.append(main)
		root_children.append(sequence)
		root.append(root_children)
		root_parallel.append(root)
		timing_nodes.append(root_parallel)
		timing.append(timing_nodes)
		timing.append(builds)
		self.slide._element.append(timing)
