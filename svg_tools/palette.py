"""Illustration shades from the fixed hues in docs/COLOR_PALETTE.md."""

import colorsys


_BASE_COLORS = {
	'red': '#D40000',
	'dark_orange': '#B74300',
	'light_orange': '#935D00',
	'dark_yellow': '#6C6C00',
	'lime_green': '#3B7600',
	'green': '#007A00',
	'teal': '#00775F',
	'cyan': '#007576',
	'sky_blue': '#076DAD',
	'blue': '#003FFF',
	'navy': '#0067CC',
	'purple': '#A719DB',
	'magenta': '#C80085',
	'pink': '#CC0066',
}

_LIGHTNESS = {
	'extra_light': .90,
	'light': .75,
	'medium': .55,
	'dark': .353,
	'extra_dark': .20,
}


#============================================
def shade(color: str, tone: str) -> str:
	"""Keep the palette hue and saturation while choosing an HSL lightness."""
	base = _BASE_COLORS[color]
	rgb = tuple(int(base[index:index+2], 16)/255 for index in (1, 3, 5))
	hue, _, saturation = colorsys.rgb_to_hls(*rgb)
	channels = colorsys.hls_to_rgb(hue, _LIGHTNESS[tone], saturation)
	value = '#' + ''.join(f'{round(channel*255):02X}' for channel in channels)
	return value
