"""Source-located capacity evidence shared by compilation and inspection."""

import collections
import enum
import pathlib
from dataclasses import dataclass

import slide_lib.native_model


class CapacityCause(str, enum.Enum):
	"""Name the compiler region whose physical constraint selected a smaller size."""

	TITLE = "title"
	PARAGRAPH_LIST = "paragraph/list"
	TABLE = "table"
	MIXED_FLOW = "mixed-flow"
	LOCAL_HEADING = "local-heading"
	GEOMETRY_SLOT_CONSTRAINT = "geometry/slot-constraint"


@dataclass(frozen=True)
class CapacityDiagnostic:
	"""Record one source region that crossed a readable floor or physical boundary."""

	location: slide_lib.native_model.SourceLocation
	layout: str
	slot: str
	required_size_pt: float | None
	floor_size_pt: float
	cause: CapacityCause
	minimum_size_pt: float | None = None

	def __post_init__(self) -> None:
		"""Require exactly one concrete recovery or physical-boundary representation."""
		if (self.required_size_pt is None) == (self.minimum_size_pt is None):
			raise ValueError("capacity diagnostics require either a required size or a safe minimum")

	def message(self) -> str:
		"""Return a concise safe build-summary description."""
		where = f"{self.layout}/{self.slot}"
		if self.required_size_pt is None:
			if self.minimum_size_pt is None:
				raise ValueError("physical capacity diagnostic has no safe minimum")
			return (f"{self.location.path}:{self.location.line}: {where} requires less than "
				f"{self.minimum_size_pt:g} pt (floor {self.floor_size_pt:g} pt; "
				f"{self.cause.value})")
		return (f"{self.location.path}:{self.location.line}: {where} required "
			f"{self.required_size_pt:g} pt below the {self.floor_size_pt:g} pt floor "
			f"({self.cause.value})")


class PhysicalCapacityError(ValueError):
	"""Report source content that cannot fit an editable serializer-safe frame."""

	def __init__(self, location: slide_lib.native_model.SourceLocation, layout: str,
			slot: str, floor_size_pt: float, cause: CapacityCause,
			minimum_size_pt: float) -> None:
		self.diagnostic = CapacityDiagnostic(location, layout, slot, None, floor_size_pt,
			cause, minimum_size_pt)
		where = f"{layout}/{slot}"
		super().__init__(f"{location.path}:{location.line}: {where} cannot fit at the "
			f"{minimum_size_pt:g} pt serializer-safe minimum")


#============================================
def relative_source_path(location: slide_lib.native_model.SourceLocation,
		repo_root: pathlib.Path) -> str:
	"""Return a stable repository-relative label for one diagnostic source."""
	path = location.path.expanduser().resolve()
	root = repo_root.expanduser().resolve()
	if path.is_relative_to(root):
		return path.relative_to(root).as_posix()
	return path.name


#============================================
def diagnostic_sort_key(diagnostic: CapacityDiagnostic,
		repo_root: pathlib.Path) -> tuple[str, int, str, str, str, float, float]:
	"""Return the complete deterministic inspection order for one concern."""
	return (relative_source_path(diagnostic.location, repo_root), diagnostic.location.line,
		diagnostic.layout, diagnostic.slot, diagnostic.cause.value,
		diagnostic.required_size_pt if diagnostic.required_size_pt is not None else 0.0,
		diagnostic.minimum_size_pt if diagnostic.minimum_size_pt is not None else 0.0)


#============================================
def sorted_diagnostics(diagnostics: tuple[CapacityDiagnostic, ...] | list[CapacityDiagnostic],
		repo_root: pathlib.Path) -> tuple[CapacityDiagnostic, ...]:
	"""Order independent compiler results before plain terminal output."""
	return tuple(sorted(diagnostics, key=lambda diagnostic: diagnostic_sort_key(diagnostic, repo_root)))


#============================================
def format_diagnostic(diagnostic: CapacityDiagnostic, repo_root: pathlib.Path) -> str:
	"""Format one capacity concern as one portable, plain-text inspection line."""
	where = relative_source_path(diagnostic.location, repo_root)
	if diagnostic.required_size_pt is None:
		if diagnostic.minimum_size_pt is None:
			raise ValueError("physical capacity diagnostic has no safe minimum")
		required = f"required<{diagnostic.minimum_size_pt:g}pt"
		minimum = f" minimum={diagnostic.minimum_size_pt:g}pt"
	else:
		required = f"required={diagnostic.required_size_pt:g}pt"
		minimum = ""
	return (f"{where}:{diagnostic.location.line} layout={diagnostic.layout} slot={diagnostic.slot} "
		f"{required} floor={diagnostic.floor_size_pt:g}pt{minimum} "
		f"cause={diagnostic.cause.value}")


#============================================
def format_summary(diagnostics: tuple[CapacityDiagnostic, ...] | list[CapacityDiagnostic]) -> str:
	"""Summarize a nonempty diagnostic collection by its explicit cause taxonomy."""
	counts = collections.Counter(diagnostic.cause.value for diagnostic in diagnostics)
	parts = ", ".join(f"{cause}={counts[cause]}" for cause in sorted(counts))
	return f"Capacity summary: {len(diagnostics)} concerns ({parts})"
