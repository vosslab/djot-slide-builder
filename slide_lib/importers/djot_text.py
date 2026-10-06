"""Escape and preserve imported inline formatting in canonical Djot."""

import dataclasses
import re

import slide_lib.importers.source_model as source_model

# LibreOffice normalization may place the trailing prime before the strand number.
PRIMED_SEQUENCE = re.compile(
	r"([35])[\u2032\u2019'']-([ACGTU][ACGTU|/,.]{2,}[ACGTU])-[\u2032\u2019'']([35])"
)
# Imported source text commonly retains the conventional number-then-prime order.
CONVENTIONAL_PRIMED_SEQUENCE = re.compile(
	r"([35])[\u2032\u2019'']-([ACGTU][ACGTU|/,.]{2,}[ACGTU])-([35])[\u2032\u2019'']"
)
PRIME_MARK = re.compile(r"([35])[\u2032\u2019'']")
DNA_SEQUENCE = re.compile(r"(?<![A-Za-z0-9`])([ACGTU][ACGTU|/,.]{2,}[ACGTU])(?![A-Za-z0-9`])")
DJOT_PUNCTUATION = frozenset("\\`*_[]$~^{}:")

def djot_text(text: str) -> str:
	"""Escape raw source characters once and project settled DNA notation."""
	# ASVS 1.2.1: output escaping occurs only at the Djot rendering boundary.
	escaped = "".join(f"\\{character}" if character in DJOT_PUNCTUATION else character for character in text)
	escaped = PRIMED_SEQUENCE.sub(r"\1&prime;-`\2`-\3&prime;", escaped)
	escaped = CONVENTIONAL_PRIMED_SEQUENCE.sub(r"\1&prime;-`\2`-\3&prime;", escaped)
	escaped = PRIME_MARK.sub(r"\1&prime;", escaped)
	return DNA_SEQUENCE.sub(r"`\1`", escaped)


#============================================
def djot_link_target(target: str) -> str:
	"""Encode delimiter and whitespace characters in one allowed link target."""
	# ASVS 1.2.2: encode an already allow-listed URL at its output context.
	return target.replace(" ", "%20").replace("(", "%28").replace(")", "%29")


#============================================
def render_runs(runs: tuple[source_model.TextRun, ...]) -> str:
	"""Render raw source runs into Djot inline syntax exactly once."""
	# Join equal-style neighbors so formatting-only splits cannot break DNA recognition.
	coalesced: list[source_model.TextRun] = []
	for run in runs:
		if coalesced and dataclasses.replace(coalesced[-1], text=run.text) == run:
			previous = coalesced[-1]
			coalesced[-1] = dataclasses.replace(previous, text=previous.text + run.text)
		else:
			coalesced.append(run)
	segments: list[str] = []
	for run in coalesced:
		# Keep spaces outside emphasis delimiters so adjacent runs remain valid Djot.
		leading = run.text[:len(run.text) - len(run.text.lstrip())]
		trailing = run.text[len(run.text.rstrip()):]
		if not run.text.strip():
			segments.append(run.text)
			continue
		text = djot_text(run.text.strip())
		if run.italic:
			text = f"_{text}_"
		if run.bold:
			text = f"*{text}*"
		if run.link:
			text = f"[{text}]({djot_link_target(run.link)})"
		attributes = []
		if run.color:
			attributes.append(f"color={run.color}")
		if run.underline:
			attributes.append("underline=true")
		if attributes:
			text = f"[{text}]{{{' '.join(attributes)}}}"
		segments.append(leading + text + trailing)
	return "".join(segments)


#============================================
