# Set 6 topic guide

Build the master for one combined deck; edit its small included topic files.

- Master: [lect11c-set_6_regulation_of_biotechnology.djot](lect11c-set_6_regulation_of_biotechnology.djot).
- Teaching date: November 12, 2026. Set 6 is internet-based; no textbook chapter is invented.
- Authority: all 38 topics and questions in the current 2026 source, in their exact numbered order.
- Merge authorized by the instructor on November 12: use the Set 4/5 method, annual sources, and expanded instructor material.
- All science slides are visible, including the study explanations and questions without an assigned presenter.
- Objectives, definitions, four parts, numbered topic dividers, summaries, and a separate THE END are retained.

## Editing and build

```bash
source source_me.sh && python3 deck_tools.py build \
  biotech/LECT11/djot/lect11c-set_6_regulation_of_biotechnology.djot --format all
```

Run LibreOffice operations outside the sandbox. Outputs use the master stem under `output/odp/` and `output/pdf/`.

## Topic and page map

PDF page numbers refer to the final combined deck.

| Topic | Current Topic | Editable File | PDF Pages | Primary Reading |
| ---: | --- | --- | --- | --- |
| 1 | The Biologics Control Act of 1902 | [set6_part1_01_04.djot](set6_part1_01_04.djot) | 8-15 | [FDA: milestones in U.S. food and drug law](https://www.fda.gov/about-fda/fda-history/milestones-us-food-and-drug-law) |
| 2 | The Pure Food and Drug Act of 1906 | [set6_part1_01_04.djot](set6_part1_01_04.djot) | 16-21 | [FDA: milestones in U.S. food and drug law](https://www.fda.gov/about-fda/fda-history/milestones-us-food-and-drug-law) |
| 3 | The Food, Drug, and Cosmetic Act of 1938 | [set6_part1_01_04.djot](set6_part1_01_04.djot) | 22-27 | [FDA: milestones in U.S. food and drug law](https://www.fda.gov/about-fda/fda-history/milestones-us-food-and-drug-law) |
| 4 | FIFRA: Registration, Risk, and Bt Crops | [set6_part1_01_04.djot](set6_part1_01_04.djot) | 28-35 | [EPA: plant-incorporated protectants](https://www.epa.gov/regulation-biotechnology-under-tsca-and-fifra/overview-plant-incorporated-protectants) |
| 5 | The Durham-Humphrey Amendment of 1951 | [set6_part1_05_07.djot](set6_part1_05_07.djot) | 36-42 | [FDA: milestones in U.S. food and drug law](https://www.fda.gov/about-fda/fda-history/milestones-us-food-and-drug-law) |
| 6 | The Kefauver-Harris Amendments of 1962 | [set6_part1_05_07.djot](set6_part1_05_07.djot) | 43-48 | [FDA: milestones in U.S. food and drug law](https://www.fda.gov/about-fda/fda-history/milestones-us-food-and-drug-law) |
| 7 | Plant Breeders' Rights and Farmers' Rights | [set6_part1_05_07.djot](set6_part1_05_07.djot) | 49-55 | [USDA: Plant Variety Protection](https://www.ams.usda.gov/services/plant-variety-protection) |
| 8 | Asilomar and Recombinant DNA | [set6_part2_08_11.djot](set6_part2_08_11.djot) | 58-65 | [NIH: biosafety and biosecurity policy](https://osp.od.nih.gov/policies/biosafety-and-biosecurity-policy/) |
| 9 | NIH Guidelines and Biosafety | [set6_part2_08_11.djot](set6_part2_08_11.djot) | 66-75 | [CDC/NIH: BMBL, sixth edition](https://www.cdc.gov/labs/bmbl/index.html) |
| 10 | Engineered Microbes under TSCA | [set6_part2_08_11.djot](set6_part2_08_11.djot) | 76-81 | [EPA: biotechnology under TSCA](https://www.epa.gov/regulation-biotechnology-under-tsca-and-fifra/overview-biotechnology-under-tsca) |
| 11 | The Coordinated Framework | [set6_part2_08_11.djot](set6_part2_08_11.djot) | 82-89 | [FDA: U.S. GMO oversight](https://www.fda.gov/food/agricultural-biotechnology/how-gmos-are-regulated-united-states) |
| 12 | APHIS and the Plant Protection Act | [set6_part2_12_14.djot](set6_part2_12_14.djot) | 90-96 | [APHIS: current biotechnology processes and suspended SECURE processes](https://www.aphis.usda.gov/biotechnology-guidance) |
| 13 | The Food Safety Modernization Act | [set6_part2_12_14.djot](set6_part2_12_14.djot) | 97-101 | [FDA: Food Safety Modernization Act](https://www.fda.gov/food/guidance-regulation-food-and-dietary-supplements/food-safety-modernization-act-fsma) |
| 14 | SECURE: the 2020 Rule and What Changed | [set6_part2_12_14.djot](set6_part2_12_14.djot) | 102-107 | [APHIS: current biotechnology processes and suspended SECURE processes](https://www.aphis.usda.gov/biotechnology-guidance) |
| 15 | Drug Scheduling | [set6_part3_15_18.djot](set6_part3_15_18.djot) | 110-114 | [DEA: drug scheduling](https://www.dea.gov/drug-information/drug-scheduling) |
| 16 | Federal and State Regulation | [set6_part3_15_18.djot](set6_part3_15_18.djot) | 115-119 | [DOJ: medical-marijuana registrations and scope of the 2026 order](https://www.justice.gov/opa/pr/justice-department-announces-issuance-federal-registrations-medical-marijuana-dispensaries) |
| 17 | Marijuana Legalization | [set6_part3_15_18.djot](set6_part3_15_18.djot) | 120-125 | [DOJ: medical-marijuana registrations and scope of the 2026 order](https://www.justice.gov/opa/pr/justice-department-announces-issuance-federal-registrations-medical-marijuana-dispensaries) |
| 18 | Psilocybin and Other Substances | [set6_part3_15_18.djot](set6_part3_15_18.djot) | 126-131 | [Oregon Health Authority: regulated psilocybin services](https://www.oregon.gov/oha/PH/PREVENTIONWELLNESS/Pages/oregon-psilocybin-services.aspx) |
| 19 | Drug Approval and Clinical Evidence | [set6_part3_19_21.djot](set6_part3_19_21.djot) | 132-139 | [FDA: drug review process](https://www.fda.gov/drugs/information-consumers-and-patients-drugs/fdas-drug-review-process-ensuring-drugs-are-safe-and-effective) |
| 20 | Clinical Trial Phases | [set6_part3_19_21.djot](set6_part3_19_21.djot) | 140-149 | [FDA: clinical research](https://www.fda.gov/patients/drug-development-process/step-3-clinical-research) |
| 21 | Orphan Drugs and Expedited Programs | [set6_part3_19_21.djot](set6_part3_19_21.djot) | 150-156 | [FDA: expedited programs](https://www.fda.gov/patients/learn-about-drug-and-device-approvals/fast-track-breakthrough-therapy-accelerated-approval-priority-review) |
| 22 | Supplements and DSHEA | [set6_part3_22_25.djot](set6_part3_22_25.djot) | 157-169 | [FDA: dietary supplement questions and answers](https://www.fda.gov/food/information-consumers-using-dietary-supplements/questions-and-answers-dietary-supplements) |
| 23 | Generic Drug Regulation | [set6_part3_22_25.djot](set6_part3_22_25.djot) | 170-178 | [FDA: generic drug facts](https://www.fda.gov/drugs/generic-drugs/generic-drug-facts) |
| 24 | International Generic Drug Quality | [set6_part3_22_25.djot](set6_part3_22_25.djot) | 179-185 | [DOJ: documented Ranbaxy manufacturing and false-statement case, 2013](https://www.justice.gov/archives/opa/pr/generic-drug-manufacturer-ranbaxy-pleads-guilty-and-agrees-pay-500-million-resolve-false) |
| 25 | PFAS: Forever Chemicals | [set6_part3_22_25.djot](set6_part3_22_25.djot) | 186-194 | [EPA: drinking-water PFAS standards and proposed changes](https://www.epa.gov/dwreginfo/pfas-rule-implementation) |
| 26 | Patents, Discovery, and Other Intellectual Property | [set6_part4_26_29.djot](set6_part4_26_29.djot) | 197-220 | [USPTO: patent basics](https://www.uspto.gov/patents/basics) |
| 27 | Diamond v. Chakrabarty | [set6_part4_26_29.djot](set6_part4_26_29.djot) | 221-227 | [U.S. Supreme Court: Diamond v. Chakrabarty, 1980](https://tile.loc.gov/storage-services/service/ll/usrep/usrep447/usrep447303/usrep447303.pdf) |
| 28 | The Cohen-Boyer Recombinant DNA Patents | [set6_part4_26_29.djot](set6_part4_26_29.djot) | 228-232 | [Stanford OTL: Cohen-Boyer licensing history](https://otl.stanford.edu/news/otls-first-50-years-executive-roundtable) |
| 29 | Genentech, Recombinant Insulin, and Licensing | [set6_part4_26_29.djot](set6_part4_26_29.djot) | 233-239 | [FDA: 100 Years of Insulin](https://www.fda.gov/about-fda/fda-history-exhibits/100-years-insulin) |
| 30 | AMP v. Myriad Genetics | [set6_part4_30_32.djot](set6_part4_30_32.djot) | 240-245 | [U.S. Supreme Court: AMP v. Myriad Genetics, 2013](https://tile.loc.gov/storage-services/service/ll/usrep/usrep569/usrep569576/usrep569576.pdf) |
| 31 | CRISPR/Cas9 Patent Disputes | [set6_part4_30_32.djot](set6_part4_30_32.djot) | 246-252 | [Federal Circuit: Regents v. Broad, May 12, 2025](https://www.cafc.uscourts.gov/opinions-orders/22-1653.OPINION.5-12-2025_2512679.pdf) |
| 32 | First Inventor to File and Prior Art | [set6_part4_30_32.djot](set6_part4_30_32.djot) | 253-258 | [USPTO: first-inventor-to-file applicability](https://www.uspto.gov/web/offices/pac/mpep/s2159.html) |
| 33 | Patents, Instruments, and Data | [set6_part4_33_35.djot](set6_part4_33_35.djot) | 259-264 | [USPTO: subject matter eligibility, including Diehr](https://www.uspto.gov/web/offices/pac/mpep/s2106.html) |
| 34 | Right to Repair | [set6_part4_33_35.djot](set6_part4_33_35.djot) | 265-270 | [FTC: Nixing the Fix](https://www.ftc.gov/system/files/documents/reports/nixing-fix-ftc-report-congress-repair-restrictions/nixing_the_fix_report_final_5521_630pm-508_002.pdf) |
| 35 | Copyleft and the Public Domain | [set6_part4_33_35.djot](set6_part4_33_35.djot) | 271-279 | [Creative Commons: license conditions](https://creativecommons.org/cc-licenses/) |
| 36 | Patent Trolls and Overbroad Claims | [set6_part4_36_38.djot](set6_part4_36_38.djot) | 280-291 | [USPTO: patent basics and claim scope](https://www.uspto.gov/patents/basics) |
| 37 | Nondisclosure Agreement Pitfalls | [set6_part4_36_38.djot](set6_part4_36_38.djot) | 292-297 | [USPTO: trade secrets](https://www.uspto.gov/ip-policy/trade-secret-policy) |
| 38 | Noncompetes and Biotechnology Employees | [set6_part4_36_38.djot](set6_part4_36_38.djot) | 298-302 | [Illinois: Freedom to Work Act, Section 10](https://www.ilga.gov/legislation/ilcs/fulltext?DocName=082000900K10) |

## Input inventory

Authored slide numbers, source-PDF pages, and final-PDF pages are distinct. PPTX order follows presentation relationships. Hidden state comes from source metadata. Annual PDFs provide visual references; text exports supply searchable questions.

| Source | Authored | Hidden Slides | Animation Slides | PDF Pages |
| --- | ---: | --- | --- | ---: |
| `../old/Fall_2021-Talking_Points_Set_6-Regulation_of_BioTech.pptx` | 38 | None | None | 38 |
| `../old/Fall_2022-Talking_Points_Set_6-Regulation_of_BioTech.pptx` | 43 | None | None | 43 |
| `../old/Fall_2023_Talking_Points_Set_6-Regulation_of_BioTech.pptx` | 69 | 14, 37 | None | 69 |
| `../old/Fall_2024_Talking_Points_Set_6-Regulation_of_BioTech.pptx` | 73 | 45 | 57, 67 | 73 |
| `../old/Fall_2025_Talking_Points_Set_6-Regulation_of_BioTech.pptx` | 90 | 63 | None | 90 |
| `../old/Fall_2026_Talking_Points_Set_6-Regulation_of_BioTech.pptx` | 95 | None | None | 95 |
| `../old/lect11a-2025_announcements.odp` | 48 | 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 18, 19, 24, 37, 43, 44, 45, 46, 47 | None | 28 |
| `../old/lect11b-2025_group_project_guide.odp` | 43 | 3, 4, 5, 6, 20, 21, 22, 27, 28, 29, 30, 31, 32, 33, 34, 36, 39, 41 | None | 25 |
| `../old/lect12a-2025_announcements.odp` | 49 | 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 19, 20, 25, 36, 37, 38, 44, 45, 46, 47, 48 | None | 26 |
| `../old/lect12b-2025_group_project_guide.odp` | 44 | 3, 4, 5, 6, 20, 21, 22, 27, 28, 29, 30, 31, 32, 33, 34, 36, 39, 41, 42 | None | 25 |
| `../old/lect12c-set_6_TP-patent_talking_points.odp` | 67 | 41, 42, 43 | 37, 38, 39, 40, 41, 42, 43 | 64 |
| `../old/lect13b-2025_group_project_guide.odp` | 45 | 3, 4, 5, 6, 41, 42, 43 | None | 38 |
| `../old/lect14b-2025_group_project_guide.odp` | 47 | 3, 4, 5, 6, 12, 13, 14, 41, 42, 43, 44 | None | 36 |
| `../old/lect15b-2025_group_project_guide.odp` | 48 | 3, 4, 5, 6, 12, 13, 14, 17, 18, 19, 41, 42, 43, 44, 45, 46 | None | 32 |

The separate `2025_group_project_guide_2.pdf` is the three-page collaboration extract. It corroborates the collaboration sequence. The prior reviewed LECT10 Djot supplies native group material and current reusable announcements.

## Annual-source survey

- 2021-2022: the older 16-topic organization supplies FDA history, trials, generics, supplements, PFAS, plant rights, Myriad, data, licensing, and NDA examples. Its numbers are not reused.
- 2023: separates international generics, repair, data, and other IP topics; retains useful questions and examples.
- 2024: separates NIH/USDA/EPA/FDA crop responsibilities. Selected source images include the sulfanilamide bottle, gene-flow route map, cannabis photo, mushroom photo, and USP mark.
- 2025: expands regulatory history and biosafety; supplies the animal-source photo, historical labels, recombinant-plasmid figure, greenhouse context, pharmacology comparison, and PFAS film recommendation.
- 2026: controls the four part boundaries and all 38 prompts. Its supplement label is used as a real claim-reading example. Decorative clip art and unsupported infographics were omitted.
- Student claims are leads. The new explanations distinguish mechanisms, evidence, jurisdiction, and current legal status using primary references.

## Instructor source correspondence

The original 67-slide instructor deck is regrouped under the current topics, rather than converted one-to-one. Duplicate prompts and dividers are superseded by the current questions and hierarchy. Useful content, examples, and the game are retained or reconstructed.

| Original Slide | Destination or Disposition |
| ---: | --- |
| 1 | Opening |
| 2 | 11; agency responsibilities and lab/field/food comparison |
| 3 | 11; agency responsibilities and lab/field/food comparison |
| 4 | 11; agency responsibilities and lab/field/food comparison |
| 5 | 11; agency responsibilities and lab/field/food comparison |
| 6 | 11; agency responsibilities and lab/field/food comparison |
| 7 | 11; agency responsibilities and lab/field/food comparison |
| 8 | 4; glyphosate hazard/exposure comparison, dated claims corrected |
| 9 | 4; glyphosate hazard/exposure comparison, dated claims corrected |
| 10 | 1-6, 21, 23; history, efficacy, and Hatch-Waxman |
| 11 | 1-6, 21, 23; history, efficacy, and Hatch-Waxman |
| 12 | 1-6, 21, 23; history, efficacy, and Hatch-Waxman |
| 13 | 1-6, 21, 23; history, efficacy, and Hatch-Waxman |
| 14 | 19-21; clinical evidence; dated cost/success figures superseded |
| 15 | 19-21; clinical evidence; dated cost/success figures superseded |
| 16 | 19-21; clinical evidence; dated cost/success figures superseded |
| 17 | 19-21; clinical evidence; dated cost/success figures superseded |
| 18 | 19-21; clinical evidence; dated cost/success figures superseded |
| 19 | 19-21; clinical evidence; dated cost/success figures superseded |
| 20 | 19-21; clinical evidence; dated cost/success figures superseded |
| 21 | 23-24; generic quality, data integrity, Bottle of Lies |
| 22 | 23-24; generic quality, data integrity, Bottle of Lies |
| 23 | 22; supplement claims, vitamin C, quality programs |
| 24 | 22; supplement claims, vitamin C, quality programs |
| 25 | 25; PFAS and Dark Waters |
| 26 | 25; PFAS and Dark Waters |
| 27 | 26; IP types, patent term, disclosure, investment, criteria |
| 28 | 26; IP types, patent term, disclosure, investment, criteria |
| 29 | 26; IP types, patent term, disclosure, investment, criteria |
| 30 | 26; IP types, patent term, disclosure, investment, criteria |
| 31 | 26; IP types, patent term, disclosure, investment, criteria |
| 32 | 26; IP types, patent term, disclosure, investment, criteria |
| 33 | 32, 36; filing/prior art and the original cartoon |
| 34 | 26; discovery/invention comparisons and all seven game examples |
| 35 | 32, 36; filing/prior art and the original cartoon |
| 36 | 26; discovery/invention comparisons and all seven game examples |
| 37 | 26; discovery/invention comparisons and all seven game examples |
| 38 | 26; discovery/invention comparisons and all seven game examples |
| 39 | 26; discovery/invention comparisons and all seven game examples |
| 40 | 26; discovery/invention comparisons and all seven game examples |
| 41 | 26; discovery/invention comparisons and all seven game examples |
| 42 | 26; discovery/invention comparisons and all seven game examples |
| 43 | 26; discovery/invention comparisons and all seven game examples |
| 44 | 33-34; instruments, data, and repair |
| 45 | 33-34; instruments, data, and repair |
| 46 | 35; CC/GPL/public domain; January date refreshed |
| 47 | 35; CC/GPL/public domain; January date refreshed |
| 48 | 35; CC/GPL/public domain; January date refreshed |
| 49 | 7; plant rights; U.S./India/treaty distinctions corrected |
| 50 | 7; plant rights; U.S./India/treaty distinctions corrected |
| 51 | 7; plant rights; U.S./India/treaty distinctions corrected |
| 52 | 7; plant rights; U.S./India/treaty distinctions corrected |
| 53 | 30; Myriad and cDNA, eligibility qualification added |
| 54 | 30; Myriad and cDNA, eligibility qualification added |
| 55 | 30; Myriad and cDNA, eligibility qualification added |
| 56 | 26, 29-30; engineered products, claims, and disclosure |
| 57 | 26, 29-30; engineered products, claims, and disclosure |
| 58 | 26, 29-30; engineered products, claims, and disclosure |
| 59 | 26, 29-30; engineered products, claims, and disclosure |
| 60 | 36; patent disputes; original phone/one-click images retained |
| 61 | 36; patent disputes; original phone/one-click images retained |
| 62 | 36; patent disputes; original phone/one-click images retained |
| 63 | 36; patent disputes; original phone/one-click images retained |
| 64 | 37-38; NDA pitfalls and distinct contract restrictions |
| 65 | 37-38; NDA pitfalls and distinct contract restrictions |
| 66 | 37-38; NDA pitfalls and distinct contract restrictions |
| 67 | Closing and THE END |

Raster paragraphs about agency roles were reconstructed as native text and tables. The FDA-only-for-Agrobacterium claim was corrected. The old glyphosate news item and unsupported serving calculation were replaced with a dated hazard/exposure comparison. Cost/success figures without a clear transferable basis are explained as dataset-dependent rather than repeated as universal current estimates.

## Material corrections

- CSA 1970 and DEA 1973 are separate events; prescription status is distinct from scheduling.
- Optional Phase 0 is not a mandatory step in every development program.
- SECURE history is separated from vacatur and the restored APHIS pathways.
- The 2026 medical-marijuana order is distinguished from broader pending rescheduling and activities outside its scope.
- Supplement regulation before DSHEA is not equated with universal drug-style efficacy review; quality marks do not establish benefit.
- Bioequivalence intervals concern exposure comparisons, not permission to misstate tablet strength.
- Humulin approval in 1982 is distinguished from patent dates, Cohen-Boyer licenses, and the separate growth-hormone dispute.
- Steamboat Willie is a copyright example; naturally occurring DNA, cDNA, synthetic molecules, and eligibility requirements are distinguished.
- The CRISPR explanation includes the 2025 appeal/remand; it does not call 2022 a final settlement of all rights.
- Google/Oracle at the Supreme Court is identified as copyright/fair use.
- Illinois thresholds are dated to November 2026; proposed laws are not treated as enacted law.

## Figure provenance

- [assets/set6_sources/PROVENANCE.md](assets/set6_sources/PROVENANCE.md): 14 selected annual-source images, exact authored slides and original members.
- [assets/set6_instructor/PROVENANCE.md](assets/set6_instructor/PROVENANCE.md): three instructor-selected prior-art/interface examples.
- [assets/set6_drawings/PROVENANCE.md](assets/set6_drawings/PROVENANCE.md): 10 original SVG schematics, with live labels and native Djot captions.
- Original image bytes and proportions are retained. The antitoxin horse photograph is not independently identified as Jim.
- The exposure-ratio diagram and trial-result exercise use explicitly invented values. They are not treatment data.

## Primary reference register

Primary pages/papers were opened for bounded fact-checking. Some direct command-line requests met access restrictions or bot challenges; those are recorded in the temporary receipt rather than counted as successful content verification. This is not an exhaustive legal clearance or clinical literature review.

- [FDA: milestones in U.S. food and drug law](https://www.fda.gov/about-fda/fda-history/milestones-us-food-and-drug-law)
- [EPA: plant-incorporated protectants](https://www.epa.gov/regulation-biotechnology-under-tsca-and-fifra/overview-plant-incorporated-protectants)
- [USDA: Plant Variety Protection](https://www.ams.usda.gov/services/plant-variety-protection)
- [NIH: biosafety and biosecurity policy](https://osp.od.nih.gov/policies/biosafety-and-biosecurity-policy/)
- [CDC/NIH: BMBL, sixth edition](https://www.cdc.gov/labs/bmbl/index.html)
- [EPA: biotechnology under TSCA](https://www.epa.gov/regulation-biotechnology-under-tsca-and-fifra/overview-biotechnology-under-tsca)
- [FDA: U.S. GMO oversight](https://www.fda.gov/food/agricultural-biotechnology/how-gmos-are-regulated-united-states)
- [APHIS: current biotechnology processes and suspended SECURE processes](https://www.aphis.usda.gov/biotechnology-guidance)
- [FDA: Food Safety Modernization Act](https://www.fda.gov/food/guidance-regulation-food-and-dietary-supplements/food-safety-modernization-act-fsma)
- [DEA: drug scheduling](https://www.dea.gov/drug-information/drug-scheduling)
- [DOJ: medical-marijuana registrations and scope of the 2026 order](https://www.justice.gov/opa/pr/justice-department-announces-issuance-federal-registrations-medical-marijuana-dispensaries)
- [Oregon Health Authority: regulated psilocybin services](https://www.oregon.gov/oha/PH/PREVENTIONWELLNESS/Pages/oregon-psilocybin-services.aspx)
- [FDA: drug review process](https://www.fda.gov/drugs/information-consumers-and-patients-drugs/fdas-drug-review-process-ensuring-drugs-are-safe-and-effective)
- [FDA: clinical research](https://www.fda.gov/patients/drug-development-process/step-3-clinical-research)
- [FDA: expedited programs](https://www.fda.gov/patients/learn-about-drug-and-device-approvals/fast-track-breakthrough-therapy-accelerated-approval-priority-review)
- [FDA: dietary supplement questions and answers](https://www.fda.gov/food/information-consumers-using-dietary-supplements/questions-and-answers-dietary-supplements)
- [FDA: generic drug facts](https://www.fda.gov/drugs/generic-drugs/generic-drug-facts)
- [DOJ: documented Ranbaxy manufacturing and false-statement case, 2013](https://www.justice.gov/archives/opa/pr/generic-drug-manufacturer-ranbaxy-pleads-guilty-and-agrees-pay-500-million-resolve-false)
- [EPA: drinking-water PFAS standards and proposed changes](https://www.epa.gov/dwreginfo/pfas-rule-implementation)
- [USPTO: patent basics](https://www.uspto.gov/patents/basics)
- [U.S. Supreme Court: Diamond v. Chakrabarty, 1980](https://tile.loc.gov/storage-services/service/ll/usrep/usrep447/usrep447303/usrep447303.pdf)
- [Stanford OTL: Cohen-Boyer licensing history](https://otl.stanford.edu/news/otls-first-50-years-executive-roundtable)
- [FDA: 100 Years of Insulin](https://www.fda.gov/about-fda/fda-history-exhibits/100-years-insulin)
- [U.S. Supreme Court: AMP v. Myriad Genetics, 2013](https://tile.loc.gov/storage-services/service/ll/usrep/usrep569/usrep569576/usrep569576.pdf)
- [Federal Circuit: Regents v. Broad, May 12, 2025](https://www.cafc.uscourts.gov/opinions-orders/22-1653.OPINION.5-12-2025_2512679.pdf)
- [USPTO: first-inventor-to-file applicability](https://www.uspto.gov/web/offices/pac/mpep/s2159.html)
- [USPTO: subject matter eligibility, including Diehr](https://www.uspto.gov/web/offices/pac/mpep/s2106.html)
- [FTC: Nixing the Fix](https://www.ftc.gov/system/files/documents/reports/nixing-fix-ftc-report-congress-repair-restrictions/nixing_the_fix_report_final_5521_630pm-508_002.pdf)
- [Creative Commons: license conditions](https://creativecommons.org/cc-licenses/)
- [USPTO: patent basics and claim scope](https://www.uspto.gov/patents/basics)
- [USPTO: trade secrets](https://www.uspto.gov/ip-policy/trade-secret-policy)
- [Illinois: Freedom to Work Act, Section 10](https://www.ilga.gov/legislation/ilcs/fulltext?DocName=082000900K10)
- [NIH: vitamin C evidence](https://ods.od.nih.gov/factsheets/VitaminC-HealthProfessional/)
- [FDA: Statistical Approaches to Establishing Bioequivalence, 2026](https://www.fda.gov/media/163638/download)
- [U.S. Copyright Office: duration of protection](https://www.copyright.gov/help/faq/faq-duration.html)
- [FTC: current status of the noncompete rule](https://www.ftc.gov/legal-library/browse/rules/noncompete-rule)
- [IARC: glyphosate classification, 2015](https://www.iarc.who.int/wp-content/uploads/2018/07/MonographVolume112-1.pdf)
- [UCSF: the growth-hormone dispute, reported May 1999](https://synapse.ucsf.edu/articles/2019/05/21/date-ucsf-history-ucsf-genentech-battle)
- [NIH: recombinant/synthetic nucleic-acid guidelines, April 2024](https://osp.od.nih.gov/wp-content/uploads/NIH_Guidelines.htm)
- [FTC: Herbalife settlement statement, 2016](https://www.ftc.gov/system/files/documents/public_statements/971213/160715herbalifestatement.pdf)
- [Supreme Court: Google v. Oracle, 2021](https://www.supremecourt.gov/opinions/20pdf/18-956_d18f.pdf)
- [U.S. patent US6368227B1: Method of swinging on a swing](https://patents.google.com/patent/US6368227B1/en)

Additional primary context: [FAO farmers' rights](https://www.fao.org/plant-treaty/areas-of-work/farmers-rights/en/) and [Asilomar conference statement](https://pmc.ncbi.nlm.nih.gov/articles/PMC432675/).

For final validation, artifacts, and unperformed checks, see [LECT11_REVIEW.md](LECT11_REVIEW.md).
