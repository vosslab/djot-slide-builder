# B selection and taxonomy artwork

Owner: phy_b_art. Physical Djot integration: phy_b. No canonical Djot edited.

Scratch `trial.djot` requested from shared export owner; family acceptance and canonical promotion await actual PDF inspection.

## Source and meaning

- Selection: image_003.png and original B PDF page 4. Plants and birds, stages 3/6/3, variant counts 0/1/3. Bird beak is separate from outlined wing; new broad beak and reddish outline retain original distinction. Plant dark leaf phenotype retained. Counts illustrate populations, not measurement.
- Taxonomy: image_005.png composited on white, original B PDF page 7. Topology `((((salamander,frog),caecilian),((snake,bird),(human,cow))),fish)`. Six numbered nodes 1 Vertebrates, 2 Tetrapods, 3 Amphibians, 4 Amniotes, 5 Reptiles, 6 Mammals; salamander/frog join unnumbered. Herpetofauna covers first four tips, excluding bird. All source bracket extents retained. Source terminology retained rather than modernized.

## Composition and integration

Selection candidates: compact `selection_a.svg` (900x660) for half-width; wide `selection_b.svg` (1200x550) for full-width. Native explanatory captions must state original trait, new variant in population, variant prevalent under selection. No explanatory prose is baked into SVG.

Taxonomy `taxonomy.svg` (1040x740) includes live short taxon/node/group labels. Recommend full-width for reading labels over Zoom. Native statement: branch lengths are schematic. The taxonomy figure retains every group and organism.

## Checks

Scratch make_art.py includes assert checks: unique IDs, XML parse, no bitmap elements, organism and variant counts, exact rooted clades. All pass. Standalone rsvg-convert previews at 320/1200 inspected: silhouettes recognizable, topology clear; small taxonomy labels naturally require enlarged classroom placement.

## Construction references

SVG creator skill; local A_Handbook_of_Biological_Illustration-1988.md CLARITY and PERSPECTIVE (lines 278-294): remove distracting detail, emphasize compared parts, coherent overlap. Mastering_SVG-2018.md viewBox and viewport (lines 635-651): explicit coordinate frame and viewport. Original paths/primitives authored here; no third-party art copied.

## Remaining acceptance

Actual exported trial and canonical lecture page review pending. No LibreOffice launched by this worker. No permanent tests or dependencies added.

## Trial accepted and canonical assets frozen

Actual exported proof: `_temp/genetics_visual_renewal/exports_m3/phylogenetics_art/trial.pdf` and page_001.webp through page_005.webp. Inspected all five pages. Selection compact and wide both recognizable; compact chosen to accompany original native questions/captions. Taxonomy full-width chosen because bracket/taxon labels read better than the half-width comparison. Organism sheet confirms characteristic silhouettes. Export owner released source after matching captured hashes.

Promoted exact bytes:
- `selection_a.svg` -> `genetics/LECT12/djot/assets/lect12b-gene_trees/phy_b_selection.drawn.svg`, SHA256 3a5b3919bc0d48128ed7d62ff9792202e16d58d82361fb3ff1ed6510733255f8
- `taxonomy.svg` -> `genetics/LECT12/djot/assets/lect12b-gene_trees/phy_b_taxonomy.drawn.svg`, SHA256 34246c5a95a5af6cda0854077401a186031dcf48bd3bf73dc3493c1c79361d5b
- Trial source SHA256 fef64193d2839bc04bc851f14d5dd821ac2a53b0b2472baf8fe282da12e08238.

Canonical lecture integration and final lecture export review remain with phy_b/manager. No attended playback or full suite run.
