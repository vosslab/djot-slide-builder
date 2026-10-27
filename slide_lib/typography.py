"""Shared typography decisions for advisory detection and automatic line balancing."""


def has_runt(lines: list[tuple[str, float]]) -> bool:
	"""Recognize the existing single-word or shorter-than-one-third wrapped tail."""
	if len(lines) < 2:
		return False
	text, width = lines[-1]
	result = bool(text and (len(text.split()) == 1 or width < lines[-2][1] / 3))
	return result
