"""Crop static slide drawings to their visible content and remove plain canvas fills."""

import argparse
import copy
import io
import math
import os
import pathlib
import re
import stat
import subprocess
import tempfile

import lxml.etree
import PIL.Image

import slide_lib.svg_images
import svg_tools._xml


SVG = f"{{{svg_tools._xml.SVG}}}"
NON_DRAWING_ELEMENTS = {SVG + name for name in ("title", "desc", "defs", "metadata", "style")}


def _canvas_rectangle(root: lxml.etree._Element,
		viewport: tuple[float, ...]) -> lxml.etree._Element | None:
	"""Recognize a plain, unreferenced rectangle behind all of the artwork."""
	first = next((node for node in root if isinstance(node.tag, str)
		and node.tag not in NON_DRAWING_ELEMENTS), None)
	if first is None or first.tag != SVG + "rect":
		return None
	if set(first.attrib) - {"x", "y", "width", "height", "rx", "ry", "fill", "stroke"}:
		return None
	if first.get("stroke", "none") != "none" or not re.fullmatch(
			r"white|#[0-9a-f]{3}(?:[0-9a-f]{3})?", first.get("fill", ""), re.IGNORECASE):
		return None
	try:
		box = tuple(size if first.get(name) == "100%" and index >= 2
			else float(first.get(name, "0").removesuffix("px"))
			for index, (name, size) in enumerate(zip(("x", "y", "width", "height"), viewport)))
	except ValueError:
		return None
	return first if box == viewport else None


def _bounds(root: lxml.etree._Element, width: float, height: float) -> tuple[float, ...]:
	"""Measure painted pixels, including text, strokes, and arrowheads."""
	scale = min(1.0, 2048 / max(width, height))
	pixel_width, pixel_height = math.ceil(width * scale), math.ceil(height * scale)
	probe = copy.deepcopy(root)
	probe.attrib.update({"width": str(pixel_width), "height": str(pixel_height),
		"preserveAspectRatio": "none"})
	# ASVS 1.2.5: pass validated SVG through stdin with a fixed command and no file base URL.
	result = subprocess.run(["rsvg-convert"], input=lxml.etree.tostring(probe),
		capture_output=True, check=True, timeout=30, env=dict(os.environ, PANGOCAIRO_BACKEND="fc"))
	with PIL.Image.open(io.BytesIO(result.stdout)) as image:
		bounds = image.convert("RGBA").getchannel("A").getbbox()
	if bounds is None:
		raise ValueError("no visible artwork after removing the canvas")
	left, top, right, bottom = bounds
	return (left * width / pixel_width, top * height / pixel_height,
		right * width / pixel_width, bottom * height / pixel_height)


def normalize(original: bytes, source: str, padding: int = 10) -> tuple[bytes, str]:
	"""Return normalized drawing bytes and a description of the edit."""
	if not source.endswith(".drawn.svg"):
		raise ValueError("expected a .drawn.svg drawing")
	if padding < 0:
		raise ValueError("padding must be nonnegative")
	# ASVS 1.5.1: reuse the slide embed validator before handing bytes to a renderer.
	intrinsic_width, intrinsic_height = slide_lib.svg_images.dimensions_blob(original, source)
	root = svg_tools._xml.parse(original)
	if any(node.get("{http://www.w3.org/XML/1998/namespace}base") is not None for node in root.iter()):
		raise ValueError("SVG resources must be local to the document")
	old = tuple(float(number) for number in root.get("viewBox", "").replace(",", " ").split())
	if len(old) != 4 or not all(math.isfinite(number) for number in old) or min(old[2:]) <= 0:
		raise ValueError("expected a finite, positive viewBox")
	x, y, width, height = old
	if not math.isclose(intrinsic_width / intrinsic_height, width / height, rel_tol=1e-3):
		raise ValueError("viewport and viewBox have different aspect ratios")
	canvas = _canvas_rectangle(root, old)
	fill = canvas.get("fill") if canvas is not None else None
	if canvas is not None:
		root.remove(canvas)
	left, top, right, bottom = _bounds(root, width, height)
	left = max(0, math.floor(left) - padding)
	top = max(0, math.floor(top) - padding)
	right = min(width, math.ceil(right) + padding)
	bottom = min(height, math.ceil(bottom) + padding)
	new = (x + left, y + top, right - left, bottom - top)
	if fill is None and new == old:
		return original, "no changes"
	if new != old:
		root.set("viewBox", " ".join(f"{value:.12g}" for value in new))
		root.set("width", f"{new[2] * intrinsic_width / width:.12g}")
		root.set("height", f"{new[3] * intrinsic_height / height:.12g}")
	encoding = "ascii" if original.isascii() else "UTF-8"
	output = lxml.etree.tostring(root.getroottree(), encoding=encoding, xml_declaration=False)
	if original.endswith(b"\n"):
		output += b"\n"
	slide_lib.svg_images.dimensions_blob(output, source)
	canvas_report = f"remove canvas {fill}" if fill is not None else "no plain canvas rectangle"
	return output, f"{canvas_report}; bounds {old} -> {new}"


def normalize_file(path: pathlib.Path, *, write: bool = False, padding: int = 10) -> str:
	"""Inspect one .drawn.svg, optionally writing a normalized viewport in place."""
	if not path.name.endswith(".drawn.svg") or path.is_symlink() or not path.is_file():
		raise ValueError("expected a regular .drawn.svg file")
	original = path.read_bytes()
	output, report = normalize(original, str(path), padding)
	if write and output != original:
		# ASVS 5.3.2: stage beside the explicit local target before replacing it.
		with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as file:
			temporary = pathlib.Path(file.name)
			try:
				file.write(output)
				file.close()
				temporary.chmod(stat.S_IMODE(path.stat().st_mode))
				temporary.replace(path)
			finally:
				temporary.unlink(missing_ok=True)
	return report


def main() -> int:
	"""Report proposed changes by default; write only when requested."""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("files", nargs="+", type=pathlib.Path)
	parser.add_argument("--write", action="store_true", help="apply the reported changes")
	parser.add_argument("--padding", type=int, default=10, help="margin in SVG units (default 10)")
	args = parser.parse_args()
	for path in args.files:
		try:
			print(f"{path}: {normalize_file(path, write=args.write, padding=args.padding)}")
		except (ValueError, OSError, lxml.etree.XMLSyntaxError, subprocess.SubprocessError) as exc:
			detail = exc.stderr.decode(errors="replace").strip() if isinstance(
				exc, subprocess.CalledProcessError) and exc.stderr else str(exc)
			parser.exit(1, f"{path}: {detail}\n")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
