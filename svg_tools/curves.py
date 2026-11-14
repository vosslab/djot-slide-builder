"""Distance-based placement along SVG paths."""

import math

import svgpathtools


#============================================
def sample_curve(path_d: str, *, spacing: float) -> list[tuple[float, float, float]]:
	"""Return x, y, and tangent angle in degrees at regular path distances.

	The start is included. The end is included only when its distance is a whole
	spacing interval, allowing for floating-point rounding.
	"""
	if not math.isfinite(spacing) or spacing <= 0:
		raise ValueError("Spacing must be finite and positive")
	path = svgpathtools.parse_path(path_d)
	length = path.length()
	if not math.isfinite(length) or length <= 0:
		raise ValueError("Path length must be finite and positive")
	count = math.floor(length / spacing)
	samples = []
	for index in range(count + 1):
		distance = min(index * spacing, length)
		parameter = path.ilength(distance) if distance else 0.0
		point = path.point(parameter)
		tangent = path.unit_tangent(parameter)
		angle = math.degrees(math.atan2(tangent.imag, tangent.real))
		samples.append((point.real, point.imag, angle))
	if math.isclose((count + 1) * spacing, length, rel_tol=1e-12, abs_tol=1e-12):
		point = path.point(1.0)
		tangent = path.unit_tangent(1.0)
		angle = math.degrees(math.atan2(tangent.imag, tangent.real))
		samples.append((point.real, point.imag, angle))
	return samples
