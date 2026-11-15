"""Protect the illustrative examples and their weighted cluster averages."""

import json
import pathlib
import importlib.util

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'genetics/LECT11/djot/gene_tree_examples.py'
SPEC = importlib.util.spec_from_file_location('gene_tree_examples', SCRIPT)
examples = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(examples)


def test_weighted_example_and_worksheet() -> None:
	data = json.loads(SCRIPT.with_name('gene_tree_example_data.json').read_text())
	five = examples.steps(data['five_gene_weighted'])
	assert [(s['left'], s['right'], s['height']) for s in five] == [
		('a', 'c', 2), ('ac', 'e', 4), ('b', 'd', 6), ('ace', 'bd', 11)]
	assert examples.distance('ace', 'b', data['five_gene_weighted']['pairs']) == 20
	six = examples.steps(data['six_gene_worksheet'])
	assert [(s['left'], s['right'], s['height']) for s in six] == [
		('a', 'c', 2), ('b', 'e', 3), ('d', 'f', 4), ('ac', 'be', 5), ('abce', 'df', 7)]
	assert data['six_gene_worksheet']['pairs'] == {
		'ab': 12, 'ac': 4, 'ad': 15, 'ae': 9, 'af': 18, 'bc': 10,
		'bd': 13, 'be': 6, 'bf': 15, 'cd': 13, 'ce': 9, 'cf': 14,
		'de': 11, 'df': 8, 'ef': 13}


def test_reveals_highlight_only_the_distance_and_show_new_merge(tmp_path, monkeypatch) -> None:
	data = json.loads(SCRIPT.with_name('gene_tree_example_data.json').read_text())['five_gene_weighted']
	assets = tmp_path / 'assets/lect11_gene_tree_examples'
	assets.mkdir(parents=True)
	monkeypatch.setattr(examples, 'HERE', tmp_path)
	examples.generate('five_gene_weighted', data, 'five')
	slides = (tmp_path / 'gene_tree_five_steps.djot').read_text().split('=== layout: ')
	answers = [s for s in slides if '# Join the Closest Clusters' in s]
	for index, answer in enumerate(answers, 1):
		assert answer.count('background-color=') == 1
		assert f'five_{index}.svg' in answer
		assert f'id="merge-{index}"' in (assets / f'five_{index}.svg').read_text()
