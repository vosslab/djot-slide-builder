"""Shared styling for normalized schematic paths."""

import re

import svgpathtools


#============================================
def scaled_path(path: str, width: float, height: float) -> str:
	"""Bake dimensions into authored path coordinates, preserving close commands."""
	chunks = re.split(r'([zZ])', path)
	result = []
	for chunk in chunks:
		if chunk in ('z', 'Z'):
			result.append('Z')
		elif chunk.strip():
			result.append(svgpathtools.parse_path(chunk).scaled(width, height).d())
	return ' '.join(result)


#============================================
def outline(width: float, height: float) -> dict[str, str]:
	"""Return a uniform outline in the part's final coordinate space."""
	return {'stroke': '#344651', 'stroke-width': str(min(.02 * min(width, height), 3.0)),
		'stroke-linecap': 'round', 'stroke-linejoin': 'round'}
