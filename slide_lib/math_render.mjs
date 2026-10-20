// Render a compilation's equations locally; stdout is the Python bridge's JSON.
import {mathjax} from '@mathjax/src/js/mathjax.js';
import {TeX} from '@mathjax/src/js/input/tex.js';
import {SVG} from '@mathjax/src/js/output/svg.js';
import {MathJaxStix2Font} from '@mathjax/mathjax-stix2-font/js/svg.js';
import {MathJaxMhchemFontExtension} from '@mathjax/mathjax-mhchem-font-extension/js/svg.js';
import {liteAdaptor} from '@mathjax/src/js/adaptors/liteAdaptor.js';
import {RegisterHTMLHandler} from '@mathjax/src/js/handlers/html.js';
import '@mathjax/src/js/util/asyncLoad/esm.js';
import '@mathjax/src/js/input/tex/base/BaseConfiguration.js';
import '@mathjax/src/js/input/tex/ams/AmsConfiguration.js';
import '@mathjax/src/js/input/tex/newcommand/NewcommandConfiguration.js';
import '@mathjax/src/js/input/tex/color/ColorConfiguration.js';
import '@mathjax/src/js/input/tex/boldsymbol/BoldsymbolConfiguration.js';
import '@mathjax/src/js/input/tex/textmacros/TextMacrosConfiguration.js';
import '@mathjax/src/js/input/tex/mhchem/MhchemConfiguration.js';

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const output = new SVG({
	fontData: MathJaxStix2Font,
	fontCache: 'none',
	linebreaks: {inline: false},
});
output.addExtension(MathJaxMhchemFontExtension);
let input = '';
for await (const chunk of process.stdin) input += chunk;
const results = [];
for (const request of JSON.parse(input)) {
	try {
		// Definitions belong to one expression, never to a previous slide or deck.
		const tex = new TeX({
			packages: ['base', 'ams', 'newcommand', 'color', 'boldsymbol', 'textmacros', 'mhchem'],
			formatError(_jax, error) { throw error; },
		});
		const document = mathjax.document('', {InputJax: tex, OutputJax: output});
		const container = await document.convertPromise(request.tex, {
			display: request.display, em: 16, ex: 8, containerWidth: 1000000,
		});
		const svg = adaptor.firstChild(container);
		const [x, y, width, height] = adaptor.getAttribute(svg, 'viewBox').split(/\s+/).map(Number);
		adaptor.setAttribute(svg, 'width', `${width / 1000 * 16}px`);
		adaptor.setAttribute(svg, 'height', `${height / 1000 * 16}px`);
		adaptor.removeAttribute(svg, 'style');
		results.push({
			svg: adaptor.outerHTML(svg), width: width / 1000,
			ascent: -y / 1000, descent: (y + height) / 1000,
		});
	} catch (error) {
		results.push({error: error.message});
	}
}
process.stdout.write(JSON.stringify(results));
