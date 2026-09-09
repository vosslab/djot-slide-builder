"""Immutable result produced by one layout compilation."""

from dataclasses import dataclass

import slide_lib.capacity_report
import slide_lib.layout_model
import slide_lib.layout_primitives


@dataclass(frozen=True)
class CompilationResult:
	"""Pair one format-neutral render plan with its recorded compromises."""
	plan: slide_lib.layout_model.LayoutDeck
	capacity_diagnostics: tuple[slide_lib.capacity_report.CapacityDiagnostic, ...]

	def __post_init__(self) -> None:
		slide_lib.layout_primitives.canonicalize_tuple(self, "capacity_diagnostics")
