"""Composition records for the format-neutral physical presentation plan."""

from dataclasses import dataclass
import pathlib

import slide_lib.layout_content
import slide_lib.layout_primitives
import slide_lib.native_model


@dataclass(frozen=True)
class DeckIdentity:
	deck_id: str
	source_path: pathlib.Path

	def __post_init__(self) -> None:
		slide_lib.layout_primitives.require_nonempty(self.deck_id, "deck identity")


@dataclass(frozen=True)
class MetadataEntry:
	name: str
	value: str

	def __post_init__(self) -> None:
		slide_lib.layout_primitives.require_nonempty(self.name, "metadata name")


@dataclass(frozen=True)
class SlideIdentity:
	"""Stable source-relative slide identity."""
	slide_id: str
	index: int
	source: slide_lib.native_model.SourceLocation

	def __post_init__(self) -> None:
		slide_lib.layout_primitives.require_nonempty(self.slide_id, "slide identity")
		slide_lib.layout_primitives.require_nonnegative_integer(self.index, "slide index")


@dataclass(frozen=True)
class LayoutIdentity:
	layout_name: str
	topology: slide_lib.layout_primitives.PlaceholderTopology

	def __post_init__(self) -> None:
		slide_lib.layout_primitives.require_nonempty(self.layout_name, "layout name")
		if self.layout_name != self.topology.declared_layout_id:
			raise ValueError("layout name must match its declared presentation layout identity")


@dataclass(frozen=True)
class UnsupportedSourceFact:
	"""A source construct requiring a projection decision before physical layout."""
	location: slide_lib.native_model.SourceLocation
	source_kind: str
	attributes: tuple[slide_lib.native_model.Attribute, ...] = ()

	def __post_init__(self) -> None:
		slide_lib.layout_primitives.canonicalize_tuple(self, "attributes")
		slide_lib.layout_primitives.require_nonempty(self.source_kind, "unsupported source kind")
		for attribute in self.attributes:
			slide_lib.layout_primitives.require_nonempty(attribute.name, "unsupported source attribute name")

	def diagnostic(self) -> str:
		"""Return the one source-located compiler rejection for this fact."""
		location = self.location
		message = f"{location.path}:{location.line}: {self.source_kind} has no physical projection"
		if self.attributes:
			names = ", ".join(attribute.name for attribute in self.attributes)
			message += f"; unsupported attributes: {names}"
		return message


def reject_unsupported_source_facts(facts: tuple[UnsupportedSourceFact, ...]) -> None:
	"""Stop compilation before a physical deck could expose an invented projection."""
	for fact in facts:
		raise ValueError(fact.diagnostic())


@dataclass(frozen=True)
class LayoutSlot:
	slot_id: str
	placeholder_kind: slide_lib.layout_primitives.PlaceholderKind
	role: slide_lib.layout_primitives.PresentationRole
	rectangle: slide_lib.layout_primitives.LogicalRectangle
	reading_order: int
	properties: slide_lib.layout_primitives.PlaceholderProperties

	def __post_init__(self) -> None:
		slide_lib.layout_primitives.require_nonempty(self.slot_id, "layout slot identity")
		slide_lib.layout_primitives.require_nonnegative_integer(self.reading_order, "layout slot reading order")
		slide_lib.layout_primitives.validate_placeholder_role(self.placeholder_kind, self.role)

	def topology_member(self) -> slide_lib.layout_primitives.PlaceholderTopologyMember:
		return slide_lib.layout_primitives.PlaceholderTopologyMember(
			self.slot_id, self.placeholder_kind, self.role, self.rectangle, self.properties,
		)


@dataclass(frozen=True)
class RevealTarget:
	target_id: str
	object_id: str
	reveal: slide_lib.native_model.Reveal
	activation_order: int
	paragraph_indexes: tuple[int, ...] = ()

	def __post_init__(self) -> None:
		slide_lib.layout_primitives.canonicalize_tuple(self, "paragraph_indexes")
		slide_lib.layout_primitives.require_nonempty(self.target_id, "reveal target identity")
		slide_lib.layout_primitives.require_nonnegative_integer(self.activation_order, "reveal activation order")
		for index in self.paragraph_indexes:
			slide_lib.layout_primitives.require_nonnegative_integer(index, "reveal paragraph index")
		if self.reveal.sequence is slide_lib.native_model.RevealSequence.PARAGRAPHS and \
				not self.paragraph_indexes:
			raise ValueError("paragraph reveals require an inclusive paragraph range")
		if self.paragraph_indexes and self.paragraph_indexes != tuple(range(
				self.paragraph_indexes[0], self.paragraph_indexes[-1] + 1)):
			raise ValueError("paragraph reveal indexes must form one inclusive range")


@dataclass(frozen=True)
class LayoutObject:
	object_id: str
	role: slide_lib.layout_primitives.PresentationRole
	style_role: slide_lib.layout_primitives.StyleRole
	rectangle: slide_lib.layout_primitives.LogicalRectangle
	layer: slide_lib.layout_primitives.ObjectLayer
	z_index: int
	reading_order: int
	content: slide_lib.layout_content.ObjectContent
	frame_text: slide_lib.layout_primitives.FrameTextProperties | None = None
	slot_id: str | None = None
	presentation_member_id: str | None = None
	placeholder_kind: slide_lib.layout_primitives.PlaceholderKind = slide_lib.layout_primitives.PlaceholderKind.NONE
	source: slide_lib.native_model.SourceLocation | None = None
	reveal_targets: tuple[RevealTarget, ...] = ()
	origin: slide_lib.layout_primitives.LayoutObjectOrigin = slide_lib.layout_primitives.LayoutObjectOrigin.AUTHORED

	def __post_init__(self) -> None:
		slide_lib.layout_primitives.canonicalize_tuple(self, "reveal_targets")
		slide_lib.layout_primitives.require_nonempty(self.object_id, "layout object identity")
		slide_lib.layout_primitives.require_nonnegative_integer(self.z_index, "layout object z order")
		slide_lib.layout_primitives.require_nonnegative_integer(self.reading_order, "layout object reading order")
		if not isinstance(self.origin, slide_lib.layout_primitives.LayoutObjectOrigin):
			raise ValueError("layout object origin must be a LayoutObjectOrigin")
		if not slide_lib.layout_content.adapter_projectable_content(self.content):
			raise ValueError("layout objects require adapter-projectable content")
		if self.slot_id is not None:
			slide_lib.layout_primitives.require_nonempty(self.slot_id, "layout object allocation slot identity")
		if self.presentation_member_id is not None:
			slide_lib.layout_primitives.require_nonempty(self.presentation_member_id, "presentation member identity")
		if self.placeholder_kind is not slide_lib.layout_primitives.PlaceholderKind.NONE and self.presentation_member_id is None:
			raise ValueError("placeholder layout objects require a presentation member identity")
		slide_lib.layout_primitives.validate_placeholder_role(self.placeholder_kind, self.role)
		if slide_lib.layout_content.text_capable_content(self.content) and self.frame_text is None:
			raise ValueError("text-capable layout objects require explicit frame text properties")
		if not slide_lib.layout_content.text_capable_content(self.content) and self.frame_text is not None:
			raise ValueError("non-text layout objects must not carry frame text properties")
		for target in self.reveal_targets:
			if target.object_id != self.object_id:
				raise ValueError("layout object reveal targets must name their owning object")
			if target.paragraph_indexes:
				if not isinstance(self.content, slide_lib.layout_content.TextContent):
					raise ValueError("paragraph reveal targets require TextContent")
				paragraph_count = len(self.content.paragraphs)
				if any(index >= paragraph_count for index in target.paragraph_indexes):
					raise ValueError("paragraph reveal targets must name top-level paragraphs in range")


@dataclass(frozen=True)
class SpeakerNote:
	note_id: str
	text: str

	def __post_init__(self) -> None:
		slide_lib.layout_primitives.require_nonempty(self.note_id, "speaker note identity")


@dataclass(frozen=True)
class LayoutSlide:
	identity: SlideIdentity
	layout: LayoutIdentity
	slots: tuple[LayoutSlot, ...]
	objects: tuple[LayoutObject, ...]
	notes: tuple[SpeakerNote, ...]

	def __post_init__(self) -> None:
		for name in ("slots", "objects", "notes"):
			slide_lib.layout_primitives.canonicalize_tuple(self, name)
		slide_lib.layout_primitives.validate_unique((slot.slot_id for slot in self.slots), "slide slot identities")
		slide_lib.layout_primitives.validate_unique((item.object_id for item in self.objects), "slide object identities")
		reveal_targets = tuple(target for item in self.objects for target in item.reveal_targets)
		# Native animation adapters require stable unique target identities.
		slide_lib.layout_primitives.validate_unique((target.target_id for target in reveal_targets),
			"slide reveal target identities")
		# Native animation adapters consume this sequence as the click order.
		if tuple(target.activation_order for target in reveal_targets) != tuple(range(len(reveal_targets))):
			raise ValueError("slide reveal targets must use contiguous source-ordered activation")
		# Native presentation layouts can only receive the topology they declare.
		if tuple(slot.topology_member() for slot in self.slots) != self.layout.topology.members:
			raise ValueError("slide slots must match the declared presentation layout topology")
		slot_ids = {slot.slot_id for slot in self.slots}
		members = {member.member_id: member for member in self.layout.topology.members}
		occupied: set[str] = set()
		for item in self.objects:
			# An emitted object may only occupy an allocation slot on this slide.
			if item.slot_id is not None and item.slot_id not in slot_ids:
				raise ValueError("layout object references unknown allocation slot")
			if item.presentation_member_id is None:
				continue
			if item.presentation_member_id not in members:
				raise ValueError("layout object references unknown presentation member")
			# LibreOffice placeholders are one editable object per presentation member.
			if item.presentation_member_id in occupied:
				raise ValueError("presentation members accept at most one occupying object")
			occupied.add(item.presentation_member_id)
			member = members[item.presentation_member_id]
			if (member.placeholder_kind is not item.placeholder_kind or member.role is not item.role or
					member.properties.style_role is not item.style_role or
					member.properties.frame_text != item.frame_text):
				raise ValueError("layout object is incompatible with its presentation member")

@dataclass(frozen=True)
class LayoutDeck:
	identity: DeckIdentity
	canvas: slide_lib.layout_primitives.LogicalCanvas
	metadata: tuple[MetadataEntry, ...]
	slides: tuple[LayoutSlide, ...]
	presentation_page_layouts: tuple[slide_lib.layout_primitives.PresentationPageLayoutKey, ...] = ()

	def __post_init__(self) -> None:
		slide_lib.layout_primitives.canonicalize_tuple(self, "metadata")
		slide_lib.layout_primitives.canonicalize_tuple(self, "slides")
		self._validate_slide_identities()
		expected = tuple(dict.fromkeys(
			slide.layout.topology.key_for_canvas(self.canvas) for slide in self.slides
		))
		if self.presentation_page_layouts:
			slide_lib.layout_primitives.canonicalize_tuple(self, "presentation_page_layouts")
			if self.presentation_page_layouts != expected:
				raise ValueError("deck presentation layout catalog must resolve every slide exactly once")
		else:
			object.__setattr__(self, "presentation_page_layouts", expected)

	def _validate_slide_identities(self) -> None:
		"""Keep source order deterministic for adapters."""
		identities = tuple(slide.identity for slide in self.slides)
		slide_lib.layout_primitives.validate_unique((identity.slide_id for identity in identities),
			"deck slide identities")
		indexes = tuple(identity.index for identity in identities)
		slide_lib.layout_primitives.validate_unique(indexes, "deck physical slide indexes")
		if indexes != tuple(range(len(identities))):
			raise ValueError("deck slides must be in contiguous physical index order")
