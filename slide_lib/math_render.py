"""Compile LaTeX expressions once per deck into measured, self-contained SVG."""

import dataclasses
import hashlib
import json
import pathlib
import subprocess

import slide_lib.native_model
import slide_lib.svg_images


#============================================
def validate_equation_blocks(blocks: tuple[slide_lib.native_model.Block, ...]) -> None:
	"""Require each math-bearing paragraph, list item, or cell to be one equation."""
	def check(inlines: tuple[slide_lib.native_model.Inline, ...],
			location: slide_lib.native_model.SourceLocation) -> None:
		leaves = []
		def collect(values: tuple[slide_lib.native_model.Inline, ...]) -> None:
			for inline in values:
				if hasattr(inline, "children"):
					collect(inline.children)
				elif isinstance(inline, slide_lib.native_model.Text) and not inline.value.strip():
					continue
				else:
					leaves.append(inline)
		collect(inlines)
		if any(isinstance(inline, slide_lib.native_model.InlineMath) for inline in leaves) \
				and len(leaves) != 1:
			raise ValueError(f"{location.path}:{location.line}: mixed text and math are unsupported; "
				"use native Djot notation or put one complete equation in its own paragraph, list item, or table cell")
	for block in blocks:
		if isinstance(block, (slide_lib.native_model.Paragraph, slide_lib.native_model.Heading)):
			check(block.inlines, block.location)
		elif isinstance(block, slide_lib.native_model.ListBlock):
			for item in block.items:
				check(item.inlines, item.location)
				validate_equation_blocks(item.children)
		elif isinstance(block, slide_lib.native_model.Table):
			for row in (block.headers,) + block.rows:
				for cell in row:
					check(cell.inlines, block.location)


@dataclasses.dataclass(frozen=True)
class RenderedMath:
	"""Vector artwork and baseline extents in units of the selected math em."""

	svg: str
	width: float
	ascent: float
	descent: float

	def image_path(self, color: str, directory: pathlib.Path) -> str:
		"""Materialize one resolved foreground without changing explicit TeX colors."""
		blob = self.svg.replace("currentColor", f"#{color}").encode("utf-8")
		slide_lib.svg_images.dimensions_blob(blob, "rendered equation")
		digest = hashlib.sha256(blob).hexdigest()
		directory.mkdir(parents=True, exist_ok=True)
		path = directory / f"{digest}.svg"
		if not path.is_file():
			path.write_bytes(blob)
		return str(path)


#============================================
def render_equations(requests: dict[tuple[str, bool], slide_lib.native_model.SourceLocation]
		) -> dict[tuple[str, bool], RenderedMath]:
	"""Render unique equations in one Node invocation, retaining author locations."""
	if not requests:
		return {}
	payload = [{"tex": tex, "display": display} for tex, display in requests]
	command = ["node", str(pathlib.Path(__file__).with_suffix(".mjs"))]
	process = subprocess.run(command, input=json.dumps(payload), text=True,
		capture_output=True, check=False)
	if process.returncode:
		raise ValueError("MathJax could not start; install the local dependencies with npm ci.\n"
			+ process.stderr.strip())
	results = json.loads(process.stdout)
	rendered = {}
	for key, result in zip(requests, results, strict=True):
		location = requests[key]
		if "error" in result:
			raise ValueError(f"{location.path}:{location.line}: invalid equation: {result['error']}")
		rendered[key] = RenderedMath(**result)
	return rendered


#============================================
def lower_display_math(source: slide_lib.native_model.Slide) -> slide_lib.native_model.Slide:
	"""Give display equations the ordinary paragraph flow and alignment machinery."""
	def blocks(values: tuple[slide_lib.native_model.Block, ...]
			) -> tuple[slide_lib.native_model.Block, ...]:
		result = tuple(slide_lib.native_model.Paragraph(block.location,
			(slide_lib.native_model.InlineMath(block.value, display=True),),
			attributes=block.attributes) if isinstance(block, slide_lib.native_model.DisplayMath)
			else block for block in values)
		return result
	return dataclasses.replace(source, blocks=blocks(source.blocks),
		cells=tuple(dataclasses.replace(cell, blocks=blocks(cell.blocks)) for cell in source.cells))
