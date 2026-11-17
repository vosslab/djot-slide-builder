#!/usr/bin/env python3
"""Regenerate LECT12D chromosome scenes with the shared chromosome renderer.

Scene backdrops preserve source callouts and phenotype wording. Source evidence is
retained where its chromosome bands cannot be reconstructed. Run with PYTHONPATH=$PWD.
"""
# Standard Library
import re
import math
import base64
from pathlib import Path
import xml.etree.ElementTree as ET

# Local repo modules
from svg_tools.chromosomes import (
	Centromere, Chromosome, Segment, chromosome_path_part, render_chromosome_layout,
)

NS = '{http://www.w3.org/2000/svg}'
ET.register_namespace('', NS[1:-1])
ASSETS = Path(__file__).parent / 'assets/lect12d-chromo_alter_1-deletions'

MODELS = {'deletion_overview': [('deletion-before',
                        [('A', '#D9C9EF', 64.0),
                         ('B', '#D9C9EF', 64.0),
                         ('C', '#D9C9EF', 64.0),
                         ('D', '#B48CDE', 64.0),
                         ('E', '#D9C9EF', 64.0),
                         ('F', '#D9C9EF', 64.0),
                         ('G', '#D9C9EF', 64.0),
                         ('H', '#D9C9EF', 64.0)],
                        5,
                        62.0,
                        ()),
                       ('deletion-after',
                        [('A', '#D9C9EF', 64.0),
                         ('B', '#D9C9EF', 64.0),
                         ('C', '#D9C9EF', 64.0),
                         ('E', '#D9C9EF', 64.0),
                         ('F', '#D9C9EF', 64.0),
                         ('G', '#D9C9EF', 64.0),
                         ('H', '#D9C9EF', 64.0)],
                        4,
                        62.0,
                        (3,))],
 'duplication_overview': [('duplication-before',
                           [('A', '#D9C9EF', 64.0),
                            ('B', '#B48CDE', 64.0),
                            ('C', '#B48CDE', 64.0),
                            ('D', '#D9C9EF', 64.0),
                            ('E', '#D9C9EF', 64.0),
                            ('F', '#D9C9EF', 64.0),
                            ('G', '#D9C9EF', 64.0),
                            ('H', '#D9C9EF', 64.0)],
                           5,
                           62.0,
                           ()),
                          ('duplication-after',
                           [('A', '#D9C9EF', 64.0),
                            ('B', '#B48CDE', 64.0),
                            ('C', '#B48CDE', 64.0),
                            ('B', '#B48CDE', 64.0),
                            ('C', '#B48CDE', 64.0),
                            ('D', '#D9C9EF', 64.0),
                            ('E', '#D9C9EF', 64.0),
                            ('F', '#D9C9EF', 64.0),
                            ('G', '#D9C9EF', 64.0),
                            ('H', '#D9C9EF', 64.0)],
                           7,
                           62.0,
                           (3, 5))],
 'inversion_overview': [('inversion-before',
                         [('A', '#D9C9EF', 64.0),
                          ('B', '#B48CDE', 64.0),
                          ('C', '#B48CDE', 64.0),
                          ('D', '#B48CDE', 64.0),
                          ('E', '#D9C9EF', 64.0),
                          ('F', '#D9C9EF', 64.0),
                          ('G', '#D9C9EF', 64.0),
                          ('H', '#D9C9EF', 64.0)],
                         5,
                         62.0,
                         ()),
                        ('inversion-after',
                         [('A', '#D9C9EF', 64.0),
                          ('D', '#B48CDE', 64.0),
                          ('C', '#B48CDE', 64.0),
                          ('B', '#B48CDE', 64.0),
                          ('E', '#D9C9EF', 64.0),
                          ('F', '#D9C9EF', 64.0),
                          ('G', '#D9C9EF', 64.0),
                          ('H', '#D9C9EF', 64.0)],
                         5,
                         62.0,
                         (1, 4))],
 'translocation_overview': [('translocation-before-1',
                             [('A', '#B48CDE', 64.0),
                              ('B', '#B48CDE', 64.0),
                              ('C', '#D9C9EF', 64.0),
                              ('D', '#D9C9EF', 64.0),
                              ('E', '#D9C9EF', 64.0),
                              ('F', '#D9C9EF', 64.0),
                              ('G', '#D9C9EF', 64.0),
                              ('H', '#D9C9EF', 64.0)],
                             5,
                             62.0,
                             ()),
                            ('translocation-before-2',
                             [('M', '#77CBDC', 64.0),
                              ('N', '#77CBDC', 64.0),
                              ('O', '#77CBDC', 64.0),
                              ('P', '#C1E7EE', 64.0),
                              ('Q', '#C1E7EE', 64.0),
                              ('R', '#C1E7EE', 64.0)],
                             5,
                             62.0,
                             ()),
                            ('translocation-after-1',
                             [('M', '#77CBDC', 64.0),
                              ('N', '#77CBDC', 64.0),
                              ('O', '#77CBDC', 64.0),
                              ('C', '#D9C9EF', 64.0),
                              ('D', '#D9C9EF', 64.0),
                              ('E', '#D9C9EF', 64.0),
                              ('F', '#D9C9EF', 64.0),
                              ('G', '#D9C9EF', 64.0),
                              ('H', '#D9C9EF', 64.0)],
                             6,
                             62.0,
                             (3,)),
                            ('translocation-after-2',
                             [('A', '#B48CDE', 64.0),
                              ('B', '#B48CDE', 64.0),
                              ('P', '#C1E7EE', 64.0),
                              ('Q', '#C1E7EE', 64.0),
                              ('R', '#C1E7EE', 64.0)],
                             4,
                             62.0,
                             (2,))],
 'deletion_parent': [('parent-intact',
                      [('', '#B8D9EC', 86.0),
                       ('a+', '#E5ADC3', 86.0),
                       ('b+', '#B8D5AB', 86.0),
                       ('c+', '#CDB49D', 86.0),
                       ('d+', '#F1BC8F', 86.0),
                       ('e+', '#E7D17F', 86.0),
                       ('f+', '#CDB4E6', 86.0)],
                      1,
                      52.0,
                      ()),
                     ('parent-deleted',
                      [('', '#B8D9EC', 86.0),
                       ('a+', '#E5ADC3', 86.0),
                       ('b+', '#B8D5AB', 86.0),
                       ('f+', '#CDB4E6', 86.0)],
                      1,
                      52.0,
                      ())],
 'mutant_tester': [('tester-1',
                    [('', '#B8D9EC', 86.0),
                     ('a-', '#E5ADC3', 86.0),
                     ('b-', '#B8D5AB', 86.0),
                     ('c-', '#CDB49D', 86.0),
                     ('d-', '#F1BC8F', 86.0),
                     ('e-', '#E7D17F', 86.0),
                     ('f-', '#CDB4E6', 86.0)],
                    1,
                    52.0,
                    ()),
                   ('tester-2',
                    [('', '#B8D9EC', 86.0),
                     ('a-', '#E5ADC3', 86.0),
                     ('b-', '#B8D5AB', 86.0),
                     ('c-', '#CDB49D', 86.0),
                     ('d-', '#F1BC8F', 86.0),
                     ('e-', '#E7D17F', 86.0),
                     ('f-', '#CDB4E6', 86.0)],
                    1,
                    52.0,
                    ())],
 'deletion_progeny': [('progeny-wildtype-mutant',
                       [('', '#B8D9EC', 86.0),
                        ('a-', '#E5ADC3', 86.0),
                        ('b-', '#B8D5AB', 86.0),
                        ('c-', '#CDB49D', 86.0),
                        ('d-', '#F1BC8F', 86.0),
                        ('e-', '#E7D17F', 86.0),
                        ('f-', '#CDB4E6', 86.0)],
                       1,
                       52.0,
                       ()),
                      ('progeny-wildtype-intact',
                       [('', '#B8D9EC', 86.0),
                        ('a+', '#E5ADC3', 86.0),
                        ('b+', '#B8D5AB', 86.0),
                        ('c+', '#CDB49D', 86.0),
                        ('d+', '#F1BC8F', 86.0),
                        ('e+', '#E7D17F', 86.0),
                        ('f+', '#CDB4E6', 86.0)],
                       1,
                       52.0,
                       ()),
                      ('progeny-deletion-mutant',
                       [('', '#B8D9EC', 86.0),
                        ('a-', '#E5ADC3', 86.0),
                        ('b-', '#B8D5AB', 86.0),
                        ('c-', '#CDB49D', 86.0),
                        ('d-', '#F1BC8F', 86.0),
                        ('e-', '#E7D17F', 86.0),
                        ('f-', '#CDB4E6', 86.0)],
                       1,
                       52.0,
                       ()),
                      ('progeny-deletion-deleted',
                       [('', '#B8D9EC', 86.0),
                        ('a+', '#E5ADC3', 86.0),
                        ('b+', '#B8D5AB', 86.0),
                        ('f+', '#CDB4E6', 86.0)],
                       1,
                       52.0,
                       ())],
 'deletion_testcross_outcomes': [('chromosome-parent-intact',
                                  [('', '#B8D9EC', 58.0),
                                   ('a+', '#E5ADC3', 58.0),
                                   ('b+', '#B8D5AB', 58.0),
                                   ('c+', '#CDB49D', 58.0),
                                   ('d+', '#F1BC8F', 58.0),
                                   ('e+', '#E7D17F', 58.0),
                                   ('f+', '#CDB4E6', 58.0)],
                                  1,
                                  54.0,
                                  ()),
                                 ('chromosome-parent-deleted',
                                  [('', '#B8D9EC', 58.0),
                                   ('a+', '#E5ADC3', 58.0),
                                   ('b+', '#B8D5AB', 58.0),
                                   ('f+', '#CDB4E6', 58.0)],
                                  1,
                                  54.0,
                                  ()),
                                 ('chromosome-tester-upper',
                                  [('', '#B8D9EC', 58.0),
                                   ('a-', '#E5ADC3', 58.0),
                                   ('b-', '#B8D5AB', 58.0),
                                   ('c-', '#CDB49D', 58.0),
                                   ('d-', '#F1BC8F', 58.0),
                                   ('e-', '#E7D17F', 58.0),
                                   ('f-', '#CDB4E6', 58.0)],
                                  1,
                                  54.0,
                                  ()),
                                 ('chromosome-tester-lower',
                                  [('', '#B8D9EC', 58.0),
                                   ('a-', '#E5ADC3', 58.0),
                                   ('b-', '#B8D5AB', 58.0),
                                   ('c-', '#CDB49D', 58.0),
                                   ('d-', '#F1BC8F', 58.0),
                                   ('e-', '#E7D17F', 58.0),
                                   ('f-', '#CDB4E6', 58.0)],
                                  1,
                                  54.0,
                                  ()),
                                 ('chromosome-gamete-intact',
                                  [('', '#B8D9EC', 58.0),
                                   ('a+', '#E5ADC3', 58.0),
                                   ('b+', '#B8D5AB', 58.0),
                                   ('c+', '#CDB49D', 58.0),
                                   ('d+', '#F1BC8F', 58.0),
                                   ('e+', '#E7D17F', 58.0),
                                   ('f+', '#CDB4E6', 58.0)],
                                  1,
                                  54.0,
                                  ()),
                                 ('chromosome-gamete-deleted',
                                  [('', '#B8D9EC', 58.0),
                                   ('a+', '#E5ADC3', 58.0),
                                   ('b+', '#B8D5AB', 58.0),
                                   ('f+', '#CDB4E6', 58.0)],
                                  1,
                                  54.0,
                                  ()),
                                 ('chromosome-gamete-tester',
                                  [('', '#B8D9EC', 58.0),
                                   ('a-', '#E5ADC3', 58.0),
                                   ('b-', '#B8D5AB', 58.0),
                                   ('c-', '#CDB49D', 58.0),
                                   ('d-', '#F1BC8F', 58.0),
                                   ('e-', '#E7D17F', 58.0),
                                   ('f-', '#CDB4E6', 58.0)],
                                  1,
                                  54.0,
                                  ()),
                                 ('chromosome-offspring-wild-tester',
                                  [('', '#B8D9EC', 58.0),
                                   ('a-', '#E5ADC3', 58.0),
                                   ('b-', '#B8D5AB', 58.0),
                                   ('c-', '#CDB49D', 58.0),
                                   ('d-', '#F1BC8F', 58.0),
                                   ('e-', '#E7D17F', 58.0),
                                   ('f-', '#CDB4E6', 58.0)],
                                  1,
                                  54.0,
                                  ()),
                                 ('chromosome-offspring-wild-intact',
                                  [('', '#B8D9EC', 58.0),
                                   ('a+', '#E5ADC3', 58.0),
                                   ('b+', '#B8D5AB', 58.0),
                                   ('c+', '#CDB49D', 58.0),
                                   ('d+', '#F1BC8F', 58.0),
                                   ('e+', '#E7D17F', 58.0),
                                   ('f+', '#CDB4E6', 58.0)],
                                  1,
                                  54.0,
                                  ()),
                                 ('chromosome-offspring-uncovered-tester',
                                  [('', '#B8D9EC', 58.0),
                                   ('a-', '#E5ADC3', 58.0),
                                   ('b-', '#B8D5AB', 58.0),
                                   ('c-', '#CDB49D', 58.0),
                                   ('d-', '#F1BC8F', 58.0),
                                   ('e-', '#E7D17F', 58.0),
                                   ('f-', '#CDB4E6', 58.0)],
                                  1,
                                  54.0,
                                  ()),
                                 ('chromosome-offspring-uncovered-deleted',
                                  [('', '#B8D9EC', 58.0),
                                   ('a+', '#E5ADC3', 58.0),
                                   ('b+', '#B8D5AB', 58.0),
                                   ('f+', '#CDB4E6', 58.0)],
                                  1,
                                  54.0,
                                  ())]}

BACKDROPS = {
	'deletion_overview': '<svg xmlns="http://www.w3.org/2000/svg" width="980" height="340" viewBox="0 0 980 340" role="img" aria-labelledby="title desc"><title id="title">Deletion</title><desc id="desc">Before ABCDE, centromere, FGH; after ABCE, centromere, FGH. The D region is emphasized; red arrows mark source cuts. Hollow purple markers are centromeres; white zigzags mark joins. Single chromatids; equal gene spacing and subtle bands are schematic.</desc><text x="48" y="103" font-size="32" fill="#344651" text-anchor="start" font-family="Atkinson Hyperlegible Next">Before</text><text x="48" y="263" font-size="32" fill="#344651" text-anchor="start" font-family="Atkinson Hyperlegible Next">After</text><g transform="translate(218 60)"><g data-chromosome="deletion-before" /><path d="M 206.88 -32 V -12" stroke="#BD2929" stroke-width="4" /><path d="M 199.88 -15 L 206.88 -3 L 213.88 -15 Z" fill="#BD2929" /><path d="M 270.88 -32 V -12" stroke="#BD2929" stroke-width="4" /><path d="M 263.88 -15 L 270.88 -3 L 277.88 -15 Z" fill="#BD2929" /></g><g transform="translate(218 220)"><g data-chromosome="deletion-after" /></g></svg>',
	'duplication_overview': '<svg xmlns="http://www.w3.org/2000/svg" width="980" height="340" viewBox="0 0 980 340" role="img" aria-labelledby="title desc"><title id="title">Duplication</title><desc id="desc">Before ABCDE, centromere, FGH; after ABCBCDE, centromere, FGH. The BC region is emphasized; red arrows mark source cuts. Hollow purple markers are centromeres; white zigzags mark joins. Single chromatids; equal gene spacing and subtle bands are schematic.</desc><text x="48" y="103" font-size="32" fill="#344651" text-anchor="start" font-family="Atkinson Hyperlegible Next">Before</text><text x="48" y="263" font-size="32" fill="#344651" text-anchor="start" font-family="Atkinson Hyperlegible Next">After</text><g transform="translate(218 60)"><g data-chromosome="duplication-before" /><path d="M 78.88 -32 V -12" stroke="#BD2929" stroke-width="4" /><path d="M 71.88 -15 L 78.88 -3 L 85.88 -15 Z" fill="#BD2929" /><path d="M 206.88 -32 V -12" stroke="#BD2929" stroke-width="4" /><path d="M 199.88 -15 L 206.88 -3 L 213.88 -15 Z" fill="#BD2929" /></g><g transform="translate(218 220)"><g data-chromosome="duplication-after" /></g></svg>',
	'inversion_overview': '<svg xmlns="http://www.w3.org/2000/svg" width="980" height="340" viewBox="0 0 980 340" role="img" aria-labelledby="title desc"><title id="title">Inversion</title><desc id="desc">Before ABCDE, centromere, FGH; after ADCBE, centromere, FGH. The BCD region is emphasized; red arrows mark source cuts. Hollow purple markers are centromeres; white zigzags mark joins. Single chromatids; equal gene spacing and subtle bands are schematic.</desc><text x="48" y="103" font-size="32" fill="#344651" text-anchor="start" font-family="Atkinson Hyperlegible Next">Before</text><text x="48" y="263" font-size="32" fill="#344651" text-anchor="start" font-family="Atkinson Hyperlegible Next">After</text><g transform="translate(218 60)"><g data-chromosome="inversion-before" /><path d="M 78.88 -32 V -12" stroke="#BD2929" stroke-width="4" /><path d="M 71.88 -15 L 78.88 -3 L 85.88 -15 Z" fill="#BD2929" /><path d="M 270.88 -32 V -12" stroke="#BD2929" stroke-width="4" /><path d="M 263.88 -15 L 270.88 -3 L 277.88 -15 Z" fill="#BD2929" /></g><g transform="translate(218 220)"><g data-chromosome="inversion-after" /></g></svg>',
	'translocation_overview': '<svg xmlns="http://www.w3.org/2000/svg" width="980" height="580" viewBox="0 0 980 580" role="img" aria-labelledby="title desc"><title id="title">Reciprocal translocation</title><desc id="desc">ABCDE, centromere, FGH and MNOPQ, centromere, R exchange terminal AB and MNO. Products: MNOCDE, centromere, FGH and ABPQ, centromere, R. Color follows segment identity; red arrows mark B/C and O/P cuts; white zigzags mark joins, distinct from pale centromere collars. Single chromatids; spacing and decorative bands are schematic.</desc><text x="48" y="124" font-size="32" fill="#344651" text-anchor="start" font-family="Atkinson Hyperlegible Next">Before</text><text x="48" y="424" font-size="32" fill="#344651" text-anchor="start" font-family="Atkinson Hyperlegible Next">After</text><g transform="translate(218 50)"><g data-chromosome="translocation-before-1" /><path d="M 142.88 -32 V -12" stroke="#BD2929" stroke-width="4" /><path d="M 135.88 -15 L 142.88 -3 L 149.88 -15 Z" fill="#BD2929" /></g><g transform="translate(218 160)"><g data-chromosome="translocation-before-2" /><path d="M 206.88 -32 V -12" stroke="#BD2929" stroke-width="4" /><path d="M 199.88 -15 L 206.88 -3 L 213.88 -15 Z" fill="#BD2929" /></g><g transform="translate(218 350)"><g data-chromosome="translocation-after-1" /></g><g transform="translate(218 460)"><g data-chromosome="translocation-after-2" /></g></svg>',
	'deletion_parent': '<svg xmlns="http://www.w3.org/2000/svg" width="750" height="290" viewBox="0 0 750 290" role="img" aria-labelledby="title desc"><title id="title">Deletion heterozygote</title><desc id="desc">Two separate unreplicated homologs: a+ b+ c+ d+ e+ f+ and a+ b+ f+. Wildtype phenotype for all genes because the intact homolog supplies the deleted functions. Blue unlabeled arms precede the centromeres. Equal spacing and bands are schematic.</desc><text x="40" y="34" font-size="30" fill="#172B3A" text-anchor="start" font-family="Atkinson Hyperlegible Next">Wildtype phenotype for all genes</text><g transform="translate(40 57)"><g data-chromosome="parent-intact" /></g><g transform="translate(40 129)"><g data-chromosome="parent-deleted" /></g><text x="40" y="225" font-size="27" fill="#172B3A" text-anchor="start" font-family="Atkinson Hyperlegible Next">Intact homolog supplies the missing</text><text x="40" y="259" font-size="27" fill="#172B3A" text-anchor="start" font-family="Atkinson Hyperlegible Next">c, d and e functions.</text></svg>',
	'mutant_tester': '<svg xmlns="http://www.w3.org/2000/svg" width="750" height="290" viewBox="0 0 750 290" role="img" aria-labelledby="title desc"><title id="title">Recessive tester crossed with the deletion parent</title><desc id="desc">Two separate complete unreplicated homologs, each a- b- c- d- e- f-. The multiplication sign connects this tester to the parent, not the two homologs. Blue unlabeled arms precede the centromeres. Equal spacing and bands are schematic.</desc><text x="40" y="34" font-size="30" fill="#172B3A" text-anchor="start" font-family="Atkinson Hyperlegible Next">&#215; Recessive tester</text><g transform="translate(40 57)"><g data-chromosome="tester-1" /></g><g transform="translate(40 129)"><g data-chromosome="tester-2" /></g><text x="40" y="225" font-size="27" fill="#172B3A" text-anchor="start" font-family="Atkinson Hyperlegible Next">Homozygous recessive mutant</text><text x="40" y="259" font-size="27" fill="#172B3A" text-anchor="start" font-family="Atkinson Hyperlegible Next">for all six genes.</text></svg>',
	'deletion_progeny': '<svg xmlns="http://www.w3.org/2000/svg" width="750" height="460" viewBox="0 0 750 460" role="img" aria-labelledby="title desc"><title id="title">Two progeny genotypes and phenotypes</title><desc id="desc">Upper group: complete mutant homolog paired with complete wildtype homolog; all genes wildtype phenotype. Lower group: complete mutant homolog paired with a+ b+ f+ deletion homolog; wildtype a,b,f and mutant c,d,e. Deletion uncovers recessive c-,d-,e- alleles, which are hemizygous, not homozygous. Each rod is one unreplicated chromosome; blue unlabeled arms precede centromeres. Spacing and bands are schematic.</desc><text x="40" y="34" font-size="30" fill="#172B3A" text-anchor="start" font-family="Atkinson Hyperlegible Next">Wildtype phenotype for all genes</text><g transform="translate(40 56)"><g data-chromosome="progeny-wildtype-mutant" /></g><g transform="translate(40 122)"><g data-chromosome="progeny-wildtype-intact" /></g><text x="40" y="233" font-size="30" fill="#172B3A" text-anchor="start" font-family="Atkinson Hyperlegible Next">Wildtype a, b, f; mutant c, d, e</text><g transform="translate(40 255)"><g data-chromosome="progeny-deletion-mutant" /></g><g transform="translate(40 321)"><g data-chromosome="progeny-deletion-deleted" /></g><text x="40" y="425" font-size="27" fill="#172B3A" text-anchor="start" font-family="Atkinson Hyperlegible Next">Deletion uncovers recessive c, d, e alleles.</text></svg>',
	'deletion_testcross_outcomes': '<svg xmlns="http://www.w3.org/2000/svg" width="1562" height="1031.5" viewBox="0 0 1562 1031.5" role="img" aria-labelledby="title desc">\n<title id="title">Deletion testcross outcomes</title>\n<desc id="desc">A deletion heterozygote crossed to a recessive tester produces intact and deletion-bearing offspring. Eleven separate unreplicated chromosome rods preserve all 57 alleles and both phenotype outcomes. Each pale centromere lies in an unlabeled blue left arm before a. Equal locus pitch and sparse bands are schematic. The deleted homolog lacks c, d and e, shortening the rod by three regions. In the lower offspring those recessive loci are hemizygous, not homozygous. One tester gamete class crosses two parental gamete classes.</desc>\n<rect width="1562" height="1031.5" fill="white" />\n<g font-family="Atkinson Hyperlegible Next" fill="#202328">\n<g id="outcome-panels"><rect x="765" y="452" width="490" height="270" fill="#f3e391" /><rect x="765" y="732" width="490" height="280" fill="#f3e391" /></g>\n<g data-chromosome="chromosome-parent-intact" transform="translate(220 78)" /><g data-chromosome="chromosome-parent-deleted" transform="translate(220 147)" /><g data-chromosome="chromosome-tester-upper" transform="translate(755 78)" /><g data-chromosome="chromosome-tester-lower" transform="translate(755 147)" /><g data-chromosome="chromosome-gamete-intact" transform="translate(300 573)" /><g data-chromosome="chromosome-gamete-deleted" transform="translate(300 808)" /><g data-chromosome="chromosome-gamete-tester" transform="translate(785 370)" /><g data-chromosome="chromosome-offspring-wild-tester" transform="translate(785 483)" /><g data-chromosome="chromosome-offspring-wild-intact" transform="translate(785 545)" /><g data-chromosome="chromosome-offspring-uncovered-tester" transform="translate(785 761)" /><g data-chromosome="chromosome-offspring-uncovered-deleted" transform="translate(785 824)" /><text x="445" y="51" font-size="30" font-weight="700" text-anchor="middle">Wildtype chromosome</text>\n<text x="980" y="51" font-size="30" font-weight="700" text-anchor="middle">Mutant chromosome</text>\n<text x="710" y="151" font-size="40" font-weight="400" text-anchor="middle">&#215;</text>\n<g id="parent-process" fill="none" stroke="#272727" stroke-width="2.7"><path d="M285 215 V703 Q285 729 311 729 H526" /><path d="M506 720 L526 729 L506 738" /></g>\n<text x="546" y="738" font-size="26" font-weight="400" text-anchor="start">Gametes</text>\n<g id="tester-process" fill="none" stroke="#272727" stroke-width="2.7"><path d="M1050 215 V318" /><path d="M1041 297 Q1047 306 1050 318 Q1053 306 1059 297" /></g>\n<text x="1050" y="354" font-size="26" font-weight="400" text-anchor="middle">Gametes</text>\n<g id="callout-1"><rect x="12" y="230" width="222" height="478" fill="#d5e2f1" stroke="#4e81b3" stroke-width="1.4" />\n<text x="26" y="259" font-size="26" xml:space="preserve">An organism </text>\n<text x="26" y="288" font-size="26" xml:space="preserve">with these </text>\n<text x="26" y="317" font-size="26" xml:space="preserve">chromosomes </text>\n<text x="26" y="346" font-size="26" xml:space="preserve">has the wildtype </text>\n<text x="26" y="375" font-size="26" xml:space="preserve">phenotype for </text>\n<text x="26" y="404" font-size="26" xml:space="preserve"><tspan font-style="italic">a</tspan><tspan font-size="18" baseline-shift="super">+</tspan> through <tspan font-style="italic">f</tspan><tspan font-size="18" baseline-shift="super">+</tspan> </text>\n<text x="26" y="433" font-size="26" xml:space="preserve">because the </text>\n<text x="26" y="462" font-size="26" xml:space="preserve">wildtype </text>\n<text x="26" y="491" font-size="26" xml:space="preserve">chromosome </text>\n<text x="26" y="520" font-size="26" xml:space="preserve">provides the </text>\n<text x="26" y="549" font-size="26" xml:space="preserve">gene functions </text>\n<text x="26" y="578" font-size="26" xml:space="preserve">missing in the </text>\n<text x="26" y="607" font-size="26" xml:space="preserve">deleted </text>\n<text x="26" y="636" font-size="26" xml:space="preserve">chromosome.</text>\n</g>\n<g id="callout-2"><rect x="425" y="247" width="285" height="144" fill="#d5e2f1" stroke="#4e81b3" stroke-width="1.4" />\n<text x="439" y="276" font-size="26" xml:space="preserve">Chromosome </text>\n<text x="439" y="305" font-size="26" xml:space="preserve">deleted for region </text>\n<text x="439" y="334" font-size="26" xml:space="preserve">including genes <tspan font-style="italic">c</tspan><tspan font-size="18" baseline-shift="super">+</tspan> </text>\n<text x="439" y="363" font-size="26" xml:space="preserve">through <tspan font-style="italic">e</tspan><tspan font-size="18" baseline-shift="super">+</tspan></text>\n</g>\n<g id="callout-3"><rect x="1280" y="24" width="270" height="310" fill="#d5e2f1" stroke="#4e81b3" stroke-width="1.4" />\n<text x="1294" y="53" font-size="26" xml:space="preserve">Homozygous mutant </text>\n<text x="1294" y="82" font-size="26" xml:space="preserve">for recessive allele </text>\n<text x="1294" y="111" font-size="26" xml:space="preserve">of each of the genes </text>\n<text x="1294" y="140" font-size="26" xml:space="preserve"><tspan font-style="italic">a</tspan> through <tspan font-style="italic">f</tspan>; the </text>\n<text x="1294" y="169" font-size="26" xml:space="preserve">phenotype is mutant </text>\n<text x="1294" y="198" font-size="26" xml:space="preserve">for all the genes.</text>\n</g>\n<g id="callout-4"><rect x="1280" y="375" width="270" height="124" fill="#d5e2f1" stroke="#4e81b3" stroke-width="1.4" />\n<text x="1294" y="404" font-size="26" xml:space="preserve">All gametes carry </text>\n<text x="1294" y="433" font-size="26" xml:space="preserve">multiple recessive </text>\n<text x="1294" y="462" font-size="26" xml:space="preserve">alleles.</text>\n</g>\n<g id="callout-5"><rect x="1280" y="866" width="270" height="146" fill="#d5e2f1" stroke="#4e81b3" stroke-width="1.4" />\n<text x="1294" y="895" font-size="26" xml:space="preserve">The recessive alleles </text>\n<text x="1294" y="924" font-size="26" xml:space="preserve"><tspan font-style="italic">c</tspan><tspan font-size="18" baseline-shift="super">&#8722;</tspan>, <tspan font-style="italic">d</tspan><tspan font-size="18" baseline-shift="super">&#8722;</tspan>, and <tspan font-style="italic">e</tspan><tspan font-size="18" baseline-shift="super">&#8722;</tspan> are </text>\n<text x="1294" y="953" font-size="26" xml:space="preserve">uncovered by the </text>\n<text x="1294" y="982" font-size="26" xml:space="preserve">deletion.</text>\n</g>\n<g id="callout-leader-1" stroke="#28699e" fill="#28699e"><path d="M184 230 L216 205" fill="none" stroke-width="3" /><circle cx="216" cy="205" r="4.5" stroke="none" /></g>\n<g id="callout-leader-2" stroke="#28699e" fill="#28699e"><path d="M518 247 L432.88 206" fill="none" stroke-width="3" /><circle cx="432.88" cy="206" r="4.5" stroke="none" /></g>\n<g id="callout-leader-3" stroke="#28699e" fill="#28699e"><path d="M1280 147 L1221 143" fill="none" stroke-width="3" /><circle cx="1221" cy="143" r="4.5" stroke="none" /></g>\n<g id="callout-leader-4" stroke="#28699e" fill="#28699e"><path d="M1280 417 L1246 402" fill="none" stroke-width="3" /><circle cx="1246" cy="402" r="4.5" stroke="none" /></g>\n<g id="callout-leader-5" stroke="#28699e" fill="#28699e"><path d="M1280 939 L1160 960" fill="none" stroke-width="3" /><circle cx="1160" cy="960" r="4.5" stroke="none" /></g>\n<g id="phenotype-wild">\n<text x="805" y="652" font-size="28" font-weight="400" text-anchor="start">Phenotype:</text>\n<text x="805" y="687" font-size="28" font-weight="400" text-anchor="start">wildtype for all the genes</text>\n</g><g id="phenotype-uncovered">\n<text x="805" y="918.0" font-size="28" font-weight="400" text-anchor="start">Phenotype:</text>\n<text x="805" y="953.0" font-size="28" font-weight="400" text-anchor="start">wildtype for <tspan font-style="italic">a</tspan><tspan font-size="18" baseline-shift="super">+</tspan>, <tspan font-style="italic">b</tspan><tspan font-size="18" baseline-shift="super">+</tspan>, and <tspan font-style="italic">f</tspan><tspan font-size="18" baseline-shift="super">+</tspan>;</text>\n<text x="805" y="988.0" font-size="28" font-weight="400" text-anchor="start">mutant for <tspan font-style="italic">c</tspan><tspan font-size="18" baseline-shift="super">&#8722;</tspan>, <tspan font-style="italic">d</tspan><tspan font-size="18" baseline-shift="super">&#8722;</tspan>, and <tspan font-style="italic">e</tspan><tspan font-size="18" baseline-shift="super">&#8722;</tspan></text>\n</g></g></svg>',
}

def render_rods() -> None:
	for stem, models in MODELS.items():
		root = ET.fromstring(BACKDROPS[stem])
		for name, regions, centromere, thickness, joins in models:
			model = Chromosome(tuple(Segment(label, color, length)
				for label, color, length in regions),
				centromeres=() if centromere is None else (Centromere(centromere),))
			layout = render_chromosome_layout(name, model, thickness=thickness,
				junctions=joins, allele_labels=any(len(label) > 1 for label, _, _ in regions))
			placeholder = root.find('.//' + NS + 'g[@data-chromosome="' + name + '"]')
			placeholder.append(ET.fromstring('<g xmlns="http://www.w3.org/2000/svg">'
				+ layout.svg + '</g>'))
			placeholder.attrib.pop('data-chromosome')
			parent=next(node for node in root.iter() if placeholder in list(node))
			red=[node for node in parent if node.get('stroke')=='#BD2929' or node.get('fill')=='#BD2929']
			old_starts=[]; x=thickness*.24
			for index,(_,_,length) in enumerate(regions):
				if index==centromere:x+=thickness*.48
				old_starts.append(x);x+=length
			for line,head in zip(red[::2],red[1::2]):
				old_x=float(re.match(r'M\s*([0-9.]+)',line.get('d')).group(1))
				index=min(range(len(old_starts)), key=lambda i:abs(old_starts[i]-old_x))
				new_x=layout.segments[index].start[0]
				line.set('d',f'M {new_x} -32 V -12')
				head.set('d',f'M {new_x-7} -15 L {new_x} -3 L {new_x+7} -15 Z')
		write_svg(root, ASSETS / (stem + '.drawn.svg'))


CHROMOSOME_COMPLEMENTS_BACKDROP = '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="620" viewBox="0 0 1200 620" role="img" aria-labelledby="complement-title complement-desc">\n  <title id="complement-title">Drosophila chromosome complements</title>\n  <desc id="complement-desc">Two Drosophila chromosome complements, XX on the left and XY on the right. Both contain two copies each of chromosomes 2, 3 and 4: four long bent autosomes and two small dot chromosomes. The lower pair contains two X rods on the left, and one X rod and one hooked Y on the right. Each complement contains eight separate chromosomes. Aligned positions support comparison; they do not depict pairing or a cell-cycle phase. Schematic, not to scale.</desc>\n  <rect width="1200" height="620" fill="#FFFFFF" />\n  <g id="complement-guides" fill="none" stroke="#D7E0E5" stroke-width="2">\n    <path d="M600 22 V568" />\n    <path d="M56 350 H544 M656 350 H1144" />\n  </g>\n  <g font-family="Atkinson Hyperlegible Next" text-anchor="middle" fill="#213547">\n    <g id="complement-XX">\n      <text x="300" y="67" font-size="48" font-weight="bold">XX</text>\n      <g id="complement-XX-autosomes">\n        <g id="complement-XX-pair-2">\n          <text x="126" y="313" font-size="34">2</text>\n        </g>\n        <g id="complement-XX-pair-3">\n          <text x="316" y="313" font-size="34">3</text>\n        </g>\n        <g id="complement-XX-pair-4">\n          <text x="488" y="313" font-size="34">4</text>\n        </g>\n      </g>\n      <g id="complement-XX-sex-chromosomes">\n        <text x="225" y="561" font-size="34" fill="#086898">X</text>\n        <text x="355" y="561" font-size="34" fill="#086898">X</text>\n      </g>\n    </g>\n    <g id="complement-XY" transform="translate(600,0)">\n      <text x="300" y="67" font-size="48" font-weight="bold">XY</text>\n      <g id="complement-XY-autosomes">\n        <g id="complement-XY-pair-2">\n          <text x="126" y="313" font-size="34">2</text>\n        </g>\n        <g id="complement-XY-pair-3">\n          <text x="316" y="313" font-size="34">3</text>\n        </g>\n        <g id="complement-XY-pair-4">\n          <text x="488" y="313" font-size="34">4</text>\n        </g>\n      </g>\n      <g id="complement-XY-sex-chromosomes">\n        <text x="225" y="561" font-size="34" fill="#086898">X</text>\n        <text x="355" y="561" font-size="34" fill="#417521">Y</text>\n      </g>\n    </g>\n    <text x="600" y="608" font-size="24" fill="#526879">Schematic, not to scale</text>\n  </g>\n</svg>'

DELETION_INTERVALS_BACKDROP = '<svg xmlns="http://www.w3.org/2000/svg" width="870" height="520" viewBox="0 0 870 520" role="img" aria-labelledby="deletion-intervals-title deletion-intervals-desc">\n\t<title id="deletion-intervals-title">Deletion intervals for the source mapping problem</title>\n\t<desc id="deletion-intervals-desc">Five deletion intervals reproduce the source membership across six numbered positions. A solid magenta segment denotes the region deleted, not retained. Del 1 covers 1-3, Del 2 2-3, Del 3 2-4, Del 4 3-5, and Del 5 4-6. Source: Lecture 11D mapping problem, original images 018 and 019. Positions are schematic, not genetic distances.</desc>\n\t<g font-family="Atkinson Hyperlegible Next">\n\t\t<text x="240" y="42" font-size="40" fill="#253342" text-anchor="middle">1</text>\n\t\t<path d="M240 85 V455" fill="none" stroke="#DFE6EC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />\n\t\t<text x="345" y="42" font-size="40" fill="#253342" text-anchor="middle">2</text>\n\t\t<path d="M345 85 V455" fill="none" stroke="#DFE6EC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />\n\t\t<text x="450" y="42" font-size="40" fill="#253342" text-anchor="middle">3</text>\n\t\t<path d="M450 85 V455" fill="none" stroke="#DFE6EC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />\n\t\t<text x="555" y="42" font-size="40" fill="#253342" text-anchor="middle">4</text>\n\t\t<path d="M555 85 V455" fill="none" stroke="#DFE6EC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />\n\t\t<text x="660" y="42" font-size="40" fill="#253342" text-anchor="middle">5</text>\n\t\t<path d="M660 85 V455" fill="none" stroke="#DFE6EC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />\n\t\t<text x="765" y="42" font-size="40" fill="#253342" text-anchor="middle">6</text>\n\t\t<path d="M765 85 V455" fill="none" stroke="#DFE6EC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />\n\t\t<text x="135" y="194" font-size="36" fill="#253342" text-anchor="end">Del 1</text>\n\t\t<path id="deletion-1" d="M210 185 H480" fill="none" stroke="#CC0066" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" />\n\t\t<text x="135" y="256" font-size="36" fill="#253342" text-anchor="end">Del 2</text>\n\t\t<path id="deletion-2" d="M315 247 H480" fill="none" stroke="#CC0066" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" />\n\t\t<text x="135" y="318" font-size="36" fill="#253342" text-anchor="end">Del 3</text>\n\t\t<path id="deletion-3" d="M315 309 H585" fill="none" stroke="#CC0066" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" />\n\t\t<text x="135" y="380" font-size="36" fill="#253342" text-anchor="end">Del 4</text>\n\t\t<path id="deletion-4" d="M420 371 H690" fill="none" stroke="#CC0066" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" />\n\t\t<text x="135" y="442" font-size="36" fill="#253342" text-anchor="end">Del 5</text>\n\t\t<path id="deletion-5" d="M525 433 H795" fill="none" stroke="#CC0066" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" />\n\t\t<text x="435" y="505" font-size="32" fill="#CC0066" text-anchor="middle">Magenta segment = deleted region</text>\n\t</g>\n</svg>'

DIRECT_REPEAT_LOOP_BACKDROP = '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="630" viewBox="0 0 1000 630" role="img" aria-labelledby="title description">\n<title id="title">Direct-repeat recombination</title>\n<desc id="description">Two parallel ribbons contain directly oriented purple and blue repeat copies enclosing A B ... Y Z. The ribbons fold together, bringing the purple repeat above the blue repeat at one black exchange X. Both open paths pass through A B ... Y Z; the outgoing flanks cross over the right bend without joining it. Recombination produces paired deletion ribbons with a purple-then-blue junction and a separate paired ring retaining A B ... Y Z with a blue-then-purple junction across its top. The source does not identify the molecular or replication state of the paired ribbons. Continuation chevrons are not chromosome termini; no centromere position or length scale is asserted.</desc>\n<g font-family="Atkinson Hyperlegible Next" fill="#20252b" font-size="24">\n\n<g id="initial">\n<text id="repeat-callout-1" x="330" y="36" font-size="25" text-anchor="middle">Repeated DNA sequences with</text>\n<text id="repeat-callout-2" x="330" y="65" font-size="25" text-anchor="middle">same (direct) orientation.</text>\n<path id="repeat-leader-purple" d="M205 77 L180 103" fill="none" stroke="#424a54" stroke-width="1.8" />\n<path id="repeat-leader-blue" d="M460 77 L485 103" fill="none" stroke="#424a54" stroke-width="1.8" />\n<g id="initial-1">\n<text id="initial-1-gene-A" x="239" y="125" font-size="23" text-anchor="middle" font-style="italic">A</text>\n<text id="initial-1-gene-B" x="270" y="125" font-size="23" text-anchor="middle" font-style="italic">B</text>\n<text id="initial-1-gene-dotdotdot" x="330" y="125" font-size="23" text-anchor="middle">...</text>\n<text id="initial-1-gene-Y" x="394" y="125" font-size="23" text-anchor="middle" font-style="italic">Y</text>\n<text id="initial-1-gene-Z" x="426" y="125" font-size="23" text-anchor="middle" font-style="italic">Z</text>\n</g>\n<g id="initial-2">\n<text id="initial-2-gene-A" x="239" y="160" font-size="23" text-anchor="middle" font-style="italic">A</text>\n<text id="initial-2-gene-B" x="270" y="160" font-size="23" text-anchor="middle" font-style="italic">B</text>\n<text id="initial-2-gene-dotdotdot" x="330" y="160" font-size="23" text-anchor="middle">...</text>\n<text id="initial-2-gene-Y" x="394" y="160" font-size="23" text-anchor="middle" font-style="italic">Y</text>\n<text id="initial-2-gene-Z" x="426" y="160" font-size="23" text-anchor="middle" font-style="italic">Z</text>\n</g>\n</g>\n<path id="initial-to-folded" d="M300 186 L300 232 M307.0 217.0 L300 232 L293.0 217.0" fill="none" stroke="#30363d" stroke-width="2.7" />\n<g id="folded">\n<path id="overpass-clearance" d="M280 367 H510 V438 H280 Z" fill="white" stroke="none" stroke-width="0" />\n<path id="exchange-X" d="M264 338 L285 359 M285 338 L264 359" fill="none" stroke="#000000" stroke-width="3" />\n<text id="folded-1-gene-A" x="359" y="289" font-size="22" text-anchor="middle" font-style="italic">A</text>\n<text id="folded-1-gene-B" x="421" y="327" font-size="22" text-anchor="middle" font-style="italic">B</text>\n<text id="folded-1-gene-dotdotdot" x="300" y="555" font-size="22" text-anchor="middle">...</text>\n<text id="folded-1-gene-Y" x="210" y="542" font-size="22" text-anchor="middle" font-style="italic">Y</text>\n<text id="folded-1-gene-Z" x="176" y="484" font-size="22" text-anchor="middle" font-style="italic">Z</text>\n<text id="folded-2-gene-A" x="340" y="322" font-size="22" text-anchor="middle" font-style="italic">A</text>\n<text id="folded-2-gene-B" x="389" y="348" font-size="22" text-anchor="middle" font-style="italic">B</text>\n<text id="folded-2-gene-dotdotdot" x="300" y="520" font-size="22" text-anchor="middle">...</text>\n<text id="folded-2-gene-Y" x="238" y="515" font-size="22" text-anchor="middle" font-style="italic">Y</text>\n<text id="folded-2-gene-Z" x="211" y="479" font-size="22" text-anchor="middle" font-style="italic">Z</text>\n</g>\n<path id="folded-to-deletion" d="M545 338 L650 252 M633.9600936697965 256.08918144844415 L650 252 L642.8310386498448 266.91998636594485" fill="none" stroke="#30363d" stroke-width="2.7" />\n<path id="folded-to-ring" d="M545 484 L658 461 M641.9052287869613 457.13239872790126 L658 461 L644.6975328443957 470.8511099666013" fill="none" stroke="#30363d" stroke-width="2.7" />\n<g id="deletion">\n<text id="deletion-label" x="820" y="303" font-size="27" text-anchor="middle">Deletion</text>\n</g>\n<g id="ring">\n<text id="ring-1-gene-A" x="882.27" y="380.74" font-size="22" text-anchor="middle" font-style="italic">A</text>\n<text id="ring-1-gene-B" x="918.0" y="461.0" font-size="22" text-anchor="middle" font-style="italic">B</text>\n<text id="ring-1-gene-dotdotdot" x="810.0" y="569.0" font-size="22" text-anchor="middle">...</text>\n<text id="ring-1-gene-Y" x="702.0" y="461.0" font-size="22" text-anchor="middle" font-style="italic">Y</text>\n<text id="ring-1-gene-Z" x="737.73" y="380.74" font-size="22" text-anchor="middle" font-style="italic">Z</text>\n<text id="ring-2-gene-A" x="858.85" y="406.75" font-size="22" text-anchor="middle" font-style="italic">A</text>\n<text id="ring-2-gene-B" x="883.0" y="461.0" font-size="22" text-anchor="middle" font-style="italic">B</text>\n<text id="ring-2-gene-dotdotdot" x="810.0" y="534.0" font-size="22" text-anchor="middle">...</text>\n<text id="ring-2-gene-Y" x="737.0" y="461.0" font-size="22" text-anchor="middle" font-style="italic">Y</text>\n<text id="ring-2-gene-Z" x="761.15" y="406.75" font-size="22" text-anchor="middle" font-style="italic">Z</text>\n<text id="ring-label" x="810" y="603" font-size="24" text-anchor="middle">Acentric ring fragment (lost)</text>\n</g></g></svg>'

def path_body(
	parent: ET.Element, name: str, regions: list[tuple[str, float]], path: str,
	thickness: float = 28, closed: bool = False, cut: bool = False,
) -> None:
	# Source colors and intervals remain ordered through each bend.
	model = Chromosome(tuple(Segment('', color, length)
		for color, length in regions))
	part = chromosome_path_part(name, model, path, thickness=thickness,
		closed=closed, cut_ends=cut, labels=False)
	parent.append(ET.fromstring('<g xmlns="http://www.w3.org/2000/svg">'+part.fragment+'</g>'))

def write_svg(root: ET.Element, path: Path) -> None:
	body=ET.tostring(root,encoding='unicode').encode('ascii','xmlcharrefreplace').decode('ascii')
	path.write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+body,encoding='ascii')

def write_scene(stem: str, root: ET.Element) -> None:
	write_svg(root, ASSETS / (stem+'.drawn.svg'))

def render_complements() -> None:
	root = ET.fromstring(CHROMOSOME_COMPLEMENTS_BACKDROP)
	for complement in ['XX','XY']:
		group = root.find('.//' + NS + 'g[@id="complement-'+complement+'"]')
		bodies = ET.Element(NS+'g', {'id': 'shared-'+complement})
		group.insert(0,bodies)
		for x in [80,125]:
			path_body(bodies,complement+'-2-'+str(x),[('#54798D',1)],
				f'M{x} 126 C{x+24} 151 {x+46} 171 {x+48} 190 C{x+46} 210 {x+23} 233 {x} 258',21)
		for x in [270,315]:
			path_body(bodies,complement+'-3-'+str(x),[('#54798D',1)],
				f'M{x+48} 126 C{x+24} 151 {x+2} 171 {x} 190 C{x+2} 210 {x+25} 233 {x+48} 258',21)
		for x in [465,510]:
			path_body(bodies,complement+'-4-'+str(x),[('#54798D',1)],f'M{x} 204 L{x} 208',21)
		for i,x in enumerate([225,355]):
			if complement=='XY' and i==1:
				path_body(bodies,'XY-Y',[('#417521',1)],f'M{x} 499 C{x-3} 467 {x-3} 431 {x} 393 C{x+15} 393 {x+29} 402 {x+40} 413',25)
			else:
				path_body(bodies,complement+'-X-'+str(i),[('#086898',1)],f'M{x} 393 C{x-3} 428 {x-3} 471 {x} 512',25)
	write_scene('chromosome_complements',root)

def render_intervals() -> None:
	root = ET.fromstring(DELETION_INTERVALS_BACKDROP)
	# Intervals stay at reference coordinates: their magenta marks mean missing DNA.
	path_body(root,'reference-six-bands',[('#24578F',1)]*6,'M195 88 H810',24)
	for x in [240,345,450,555,660,765]:
		ET.SubElement(root,NS+'path',{'d':f'M{x} 76 V100','stroke':'white','stroke-width':'2'})
	write_scene('deletion_intervals',root)

def render_repeat_loop() -> None:
	root = ET.fromstring(DIRECT_REPEAT_LOOP_BACKDROP)
	neutral,purple,brown,blue = '#a6bac7','#c695d4','#d8b98e','#8dbce0'
	initial=root.find('.//'+NS+'g[@id="initial"]')
	for i,y in [(1,117),(2,152)]:
		g=initial.find(NS+'g[@id="initial-'+str(i)+'"]')
		path_body(g,'shared-initial-'+str(i),[(neutral,105),(purple,70),(brown,235),(blue,70),(neutral,90)],f'M40 {y} H610',28,cut=True)
		# Keep editable allele labels on top of the shared body.
		for text in list(g.findall(NS+'text')):g.remove(text);g.append(text)
	fold=root.find('.//'+NS+'g[@id="folded"]')
	for i,path in [(1,'M310 278 H330 C400 278 450 325 450 420 C450 510 390 548 300 548 C200 548 175 520 175 475 C175 420 200 385 240 385'),(2,'M310 313 H330 C365 313 415 340 415 420 C415 485 375 513 300 513 C230 513 210 500 210 475 C210 445 225 420 240 420')]:
		path_body(fold,'shared-fold-'+str(i),[(brown,1)],path,28,cut=True)
	# Outgoing paths are drawn over the bends, preserving the source overpass topology.
	for i,y in [(1,278),(2,313)]:
		path_body(fold,'shared-fold-in-'+str(i),[(neutral,175),(purple,70)],f'M65 {y} H310',28,cut=True)
	clearance=fold.find(NS+'path[@id="overpass-clearance"]')
	fold.remove(clearance);fold.append(clearance)
	for i,y in [(1,385),(2,420)]:
		path_body(fold,'shared-fold-out-'+str(i),[(blue,70),(neutral,190)],f'M240 {y} H500',28,cut=True)
	for el in list(fold):
		if el.tag==NS+'text' or el.get('id')=='exchange-X':fold.remove(el);fold.append(el)
	deletion=root.find('.//'+NS+'g[@id="deletion"]')
	for i,y in [(1,220),(2,255)]:
		path_body(deletion,'shared-deletion-'+str(i),[(neutral,90),(purple,30),(blue,30),(neutral,110)],f'M690 {y} H950',28,cut=True)
	ring=root.find('.//'+NS+'g[@id="ring"]')
	for i,radius in [(1,108),(2,73)]:
		# Source order starts at the junction, purple then intervening DNA then blue.
		circ=2*math.pi*radius; repeat=.40*radius
		path=f'M810 {453-radius} A{radius} {radius} 0 1 1 810 {453+radius} A{radius} {radius} 0 1 1 810 {453-radius} Z'
		path_body(ring,'shared-ring-'+str(i),[(purple,repeat),(brown,circ-2*repeat),(blue,repeat)],path,28,True)
	for el in list(ring.findall(NS+'text')):ring.remove(el);ring.append(el)
	for i,y,xs in [(1,117,[40,610]),(2,152,[40,610]),(1,278,[65]),(2,313,[65]),(1,385,[500]),(2,420,[500]),(1,220,[690,950]),(2,255,[690,950])]:
		for x in xs:
			direction=1 if i==1 else -1
			ET.SubElement(root,NS+'path',{'d':f'M{x-5*direction} {y-9} L{x+5*direction} {y} L{x-5*direction} {y+9}', 'fill':'none','stroke':'#344651','stroke-width':'1.5'})
	write_scene('direct_repeat_loop',root)


def text_at(
	root: ET.Element, x: float, y: float, text: str, size: float = 22,
	color: str = '#344651', anchor: str = 'start',
) -> ET.Element:
	el=ET.SubElement(root,NS+'text',{'x':str(x),'y':str(y),'font-size':str(size),
		'fill':color,'text-anchor':anchor,'font-family':'Atkinson Hyperlegible Next'})
	el.text=text
	return el

def scene(width: float, height: float, title: str, desc: str) -> ET.Element:
	root=ET.Element(NS+'svg',{'width':str(width),'height':str(height),
		'viewBox':f'0 0 {width} {height}','role':'img','aria-labelledby':'title desc'})
	ET.SubElement(root,NS+'title',{'id':'title'}).text=title
	ET.SubElement(root,NS+'desc',{'id':'desc'}).text=desc
	return root

def photo(root: ET.Element, name: str, width: float, height: float) -> None:
	# Embed the original source bytes, including any panel covered by an overlay.
	payload=base64.b64encode((ASSETS/name).read_bytes()).decode('ascii')
	ET.SubElement(root,NS+'image',{'href':'data:image/png;base64,'+payload,
		'width':str(width),'height':str(height)})

def render_quantitative_map() -> None:
	root=scene(1000,660,'Drosophila melanogaster chromosomes',
		'Source chromosome lengths and map labels retained. Mbp and approximate cM '
		'labels are separate scales. Arm extents follow the source schematic, not a new measured reconstruction.')
	# Explicit source y coordinates retain the reference centromere line and arm proportions.
	ET.SubElement(root,NS+'path',{'d':'M20 250 H965','stroke':'#72508C','stroke-width':'1.5'})
	text_at(root,890,244,'centromere',20,'#72508C')
	for name,x,y0,y1 in [('X',105,42,250),('Y',280,72,475),('2',455,42,460),('3',625,30,510),('4',805,242,250)]:
		path_body(root,'map-'+name,[('#54798D',1)],f'M{x} {y0} V{y1}',14)
		ET.SubElement(root,NS+'ellipse',{'cx':str(x),'cy':'250','rx':'11','ry':'6',
			'fill':'none','stroke':'#72508C','stroke-width':'1.6'})
		text_at(root,x,570,name,40,anchor='middle')
	for x,y,txt,c in [(38,46,'0 cM','#D40000'),(122,46,'0 Mbp','#344651'),
		(18,242,'~75 cM','#D40000'),(123,242,'22.4 Mbp','#344651'),
		(297,76,'0 Mbp','#344651'),(297,486,'~40 Mbp','#344651'),
		(392,46,'0 cM','#D40000'),(472,46,'0 Mbp','#344651'),
		(373,242,'~55 cM','#D40000'),(472,242,'23.0 Mbp','#344651'),
		(472,277,'0 Mbp','#344651'),(358,460,'~107 cM','#D40000'),(472,466,'21.1 Mbp','#344651'),
		(562,31,'0 cM','#D40000'),(642,31,'0 Mbp','#344651'),
		(540,274,'~47 cM','#D40000'),(642,242,'24.5 Mbp','#344651'),(642,277,'0 Mbp','#344651'),
		(527,513,'~110 cM','#D40000'),(642,518,'27.9 Mbp','#344651'),
		(815,227,'0 Mbp','#344651'),(815,275,'1.4 Mbp','#344651')]:text_at(root,x,y,txt,20,c)
	for x,y,txt in [(474,122,'2L'),(474,156,'arm'),(474,333,'2R'),(474,367,'arm'),
		(644,122,'3L'),(644,156,'arm'),(644,333,'3R'),(644,367,'arm')]:text_at(root,x,y,txt,28)
	text_at(root,500,614,'Drosophila melanogaster chromosomes',34,anchor='middle')
	text_at(root,500,649,'Data from the National Center for Biotechnology Information (NCBI) and Carvalho (2002)',16,anchor='middle')
	write_scene('drosophila_quantitative_map',root)

def render_mixed_figures() -> None:
	root=scene(968,628,'Cri-du-chat chromosome 5 pair',
		'The original chromosome 5 micrograph and adjacent banded schematic are retained, '
		'including the deleted-region label and comparison line.')
	photo(root,'image_006.png',968,628)
	write_svg(root, ASSETS/'chromosome5_mixed.svg')
	root=scene(663,500,'Drosophila polytene chromosomes',
		'The complete original empirical polytene micrograph, arrows, labels and caption are '
		'retained. Only the upper-left diagrammatic inset is replaced with shared chromosome parts.')
	photo(root,'image_015.png',663,500)
	ET.SubElement(root,NS+'rect',{'x':'183','y':'42','width':'151','height':'133','fill':'white'})
	for side in [0,1]:
		x=207+side*18
		path_body(root,'inset-2-'+str(side),[('#54798D',1)],f'M{x} 59 L{x+24} 88 L{x} 122',8)
		x=293+side*18
		path_body(root,'inset-3-'+str(side),[('#54798D',1)],f'M{x} 59 L{x-24} 88 L{x} 122',8)
		path_body(root,'inset-4-'+str(side),[('#54798D',1)],f'M{253+side*10} 88 V89',5)
	path_body(root,'inset-X',[('#086898',1)],'M246 116 V146',8)
	path_body(root,'inset-Y',[('#417521',1)],'M262 146 V116 Q271 116 275 124',8)
	for x,y,txt in [(188,57,'R'),(188,133,'L'),(321,57,'R'),(321,133,'L'),
		(209,96,'2'),(295,96,'3'),(253,77,'4'),(242,169,'X'),(258,169,'Y')]:text_at(root,x,y,txt,12)
	write_svg(root, ASSETS/'polytene_mixed.svg')

def main() -> None:
	render_rods()
	render_complements()
	render_intervals()
	render_repeat_loop()
	render_quantitative_map()
	render_mixed_figures()


if __name__ == '__main__':
	main()
