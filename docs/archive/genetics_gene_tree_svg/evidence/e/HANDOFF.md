# LECT12E M3 source handoff

Status: canonical source revised after first full-deck export; second export queued. No LibreOffice was run by this owner.

## Owned source and consumers

- `genetics/LECT12/djot/lect12e-evol_time.djot`: 20 slides after splitting the source rate/context and alignment into adjacent slides10/11; source order retained. See source_map.csv.
- Four original diagrams: `phy_e_allele_sorting.drawn.svg`, `phy_e_enhancer_losses.drawn.svg`,
  `phy_e_globin_homology.drawn.svg`, `phy_e_duplication_speciation.drawn.svg` (four files).
- Retained empirical Adh pixels plus restored anchored labels: `phy_e_adh_annotated.svg`.
  This ordinary local SVG embeds the exact source PNG bytes; it is not original drawn artwork.
- C part_01 also consumes `assets/lect12e-evol_time/phy_e_allele_sorting.drawn.svg`.

## Source-to-replacement map

| Original use | New source | Preservation and repair |
| --- | --- | --- |
| E4 image002, also C41 image031 | allele_sorting drawn | A1 fixed ancestor; A2 mutation before splits; both species nodes; A1 loss in1/2, A2 loss in3; species2/3 and allele1/2 contrast. Fullwidth with native explanation. |
| E6 image003 | unchanged raster plus native caption | Actual substitution-rate evidence and units retained. |
| E7 image004+empty image005 | adh_annotated ordinary SVG; native prose | Exact empirical pixels; insertion/deletion, exon/intron brackets, six coordinate labels and site1490 association recovered from original E PDF5. 43 variable sites,18 in4exons,1aminoacid change preserved. |
| E8 image006 | unchanged raster | Empirical genome-size/mutation-rate log/log plot retained. |
| E10 image007 | native7row50column table | Literal hemoglobin alignment, source147aa/29difference/first50/8 and1.23rate/80Myr examples retained. Exact table from B independently transcribed source; C independently recovered all21 matrix differences. |
| E11 image008 | unchanged raster plus native caption | Molecular clock evidence for3proteins and axes retained. |
| E15 image009 | globin_homology drawn + native caption | Early globin duplication, alpha/beta, frog/chick/mouse in each, orthology groups and mousealpha/beta paralogy preserved. |
| E16 image010 | duplication_speciation drawn + native examples | Ancestralalpha, duplication before species1/2, all4gene descendants; original ortholog/paralog examples recovered as native text. |
| E17 image011 | enhancer_losses drawn + native caption | Original6enhancer order, two intact copies and3successive losses each. Copy1 retains all tissue1 elements; copy2 all tissue2. No promoter/coding loss. |

E13/E14 definitions now use origin by speciation/duplication, with function allowed to conserve or change;
this local clear-error correction was specifically authorized by root. Source examples remain.

## Trials and review

Four frozen scratch trial pages: `e/trial_e.djot`. Exported by central owner to
`_temp/genetics_visual_renewal/exports_m3/phylogenetics_e/trial.pdf` and page WEBPs.
Both author and exporter inspected full-size pages1,3,4; author also reviewed all standalone SVG
renders. Chosen page1 fullwidth allele scaffold and page4 horizontal enhancer sequence. Page2
shrunk the allele labels; page3 vertical enhancer arrangement left less space at delivery size.
No claim of attended Impress playback or classroom acceptance.

First canonical export reviewed at full size: allele, globin/homology, enhancer and retained empirical pages accepted. Adh page7 lost its first strip in LibreOffice despite standalone success. Repaired nestedSVG viewports to flat clipPaths with positioned unchanged images. The native alignment used confirmed AtkinsonHyperlegibleMono14pt; split it from numerical context, use3ptpadding, now18.5pt capacity estimate. Revision is queued for actual page7 and10/11 proof. Later pages shift+1; all source facts/order retained.

## Checks

`source source_me.sh && python3 _temp/genetics_visual_renewal/m3_phylogenetics/e/check_e.py`

- Static XML, positive viewBox, unique IDs and title/description on all5SVG files.
- No image nodes in original `.drawn.svg` assets.
- Reconstructed edges from the emitted SVG paths for both homology trees; terminal sets and
  required rooted clades match source.
- Read all9emitted enhancer locus states: original and both intact duplicated copies, then
  exact cumulative losses1/2/3 on each branch. Remaining functional sets complementary.
- Both Adh embedded payloads byte-identical to source image004; hashes record retained data.
- Exact literal agreement with independently transcribed7x50native alignment.
- Strict Jotdown lint passes:20slides8images. No production code or permanent tests changed.

`verification.json` contains the checks and hashes. Every original drawn asset was rendered
at320/1200pixels through librsvg; real delivery uses the central LibreOffice export.

## Construction sources

- SVG skill `references/project_workflow.md` and `task_selection.md`: semantic groups,
  editable labels, diagram/native prose separation, real delivery proof.
- Local `Mastering_SVG-2018.md` lines635-675: stable viewport/viewBox sizing.
- Local `A_Handbook_of_Biological_Illustration-1988.md` lines205-224: plan detail/label hierarchy
  for final reduction; standalone large renders do not prove small-slide readability.
- Repository `docs/slide-specs/SVG_DIAGRAMS.md`, COLOR_GUIDE, VOICE_GUIDE and PEDAGOGY_GUIDE.
- Scientific authority is the actual original E PDF and image002/004/009/010/011, not a generic
  replacement dataset. Topology-only figures explicitly use schematic branch lengths.
