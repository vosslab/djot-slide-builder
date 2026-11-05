# Upcoming-course descriptions

The shared [spring_registration.djot](spring_registration.djot) gives students a sense of the
content and structure of each upcoming course, as well as its meeting details. Refresh years
and logistics without reducing the course descriptions to a title/time/location list.

The November 5, 2026 restoration uses instructor-authored course material and the current
catalog. It is a source-grounded restoration and expansion, not a claim that every sentence
appeared together on an earlier promotion slide.

## Current logistics

[HUMAN_GUIDANCE.md](../docs/HUMAN_GUIDANCE.md) supplies the Spring/Summer 2027 teaching details:
Thursday 1:30-4:30 p.m. biochemistry lecture in Schaumburg; face-to-face biochemistry lab with
a less structured, independent study-like format; tentative BIOL 301 assignment; and summer
film on Tuesday/Thursday evenings over Zoom. Keep BIOL 301 visibly tentative.

Do not carry forward old Zoom delivery for the biochemistry lecture, old lab meeting times,
old summer session dates, old enrollment numbers, or unconfirmed course attributes.

## Biochemistry lecture

Instructor library path, relative to the teaching `CLASS/` directory:

```text
bchm_355-lecture/2026-biochem-1spring/LECTURES-s2026/
  Current-Unit_1-sp2026/lect01a-s2026_announcements.odp
```

- Authored slide 70 says: "We go into great detail on protein structure and enzyme function,
  macromolecules, etc." Restore that central description.
- Authored slide 41 and subsequent assignment pages document protein-structure visualization
  with UCSF Chimera, making images, and answering questions about the assigned protein.
- The same unit's purification, electrophoresis, centrifugation, and chromatography lectures,
  followed by the kinetics unit, corroborate the techniques and enzyme focus.
- The [current biochemistry catalog](https://catalog.roosevelt.edu/undergraduate/courses/bchm/)
  corroborates protein structure and enzyme kinetics.

The old slide's remote-delivery wording is superseded by the instructor's newer face-to-face
guidance. Its "Modeling and Simulation" attribute is not restored as a 2027 registration promise:
the current catalog entry does not establish that attribute.

## Biochemistry laboratory

Instructor library root:
`CLASS/bchm_356-lab/2026-356LAB-1Spring/lab_manuals/`.

| Source | Descriptive content |
| --- | --- |
| `lab04-kinetics/lab04-enzyme_kinetics.odt` | Substrate concentration, standard curves, enzyme assays, reaction rates, and kinetic parameters |
| `labXX-protein_struct/lab03-protein_structure.odt` | Protein sequence, structure, folding, databases, molecular software, and recording observations |
| `lab05-redox/lab05-cytochrome_c-2025.odt` | Cytochrome c redox measurements, experimental design, and data analysis |

The [current biochemistry catalog](https://catalog.roosevelt.edu/undergraduate/courses/bchm/)
also describes enzyme assays and isolation/analysis of biological macromolecules.

These sources support examples of the lab's content and work. They do not establish a new
2027 week-by-week experiment schedule, grading scheme, or meeting time.

## Cellular and molecular biology

The [current biology catalog](https://catalog.roosevelt.edu/undergraduate/courses/biol/)
identifies BIOL 301 as Cellular and Molecular Biology, covering introductory biochemistry,
cell structure/physiology, and lecture, laboratory, and discussion.

The instructor's `CLASS/biol_301-lecture/2024-1spring-301lecture/LECTURES/` material
corroborates the topic examples: cells, transport, respiration, photosynthesis, communication,
DNA, transcription, translation, and gene regulation.

The earlier instructor introduction,
`CLASS/biol_301-lecture/2023-1spring-301lecture/LECTURES/Unit_1-Spring_2023/lect01a-2022_syllabus.odp`,
also establishes the cellular/subcellular focus in authored slides 26-28. Slides 31-44 cover
cells, organelles, gene expression, energy, and feedback regulation.

Use these established course topics while leaving the instructor's 2027 assignment tentative.
Do not invent its meeting time, delivery mode, or future assessment structure. The older
2024 BIOL 301 syllabus PDF contains a copied advanced protein-structure description; that
paragraph is not reliable authority for this course.

## Biology and ethics in film

Instructor library source:
`CLASS/biol_483-film_ethics/2026-1Summer/class08a-2026_announcements.odp`.

- Authored slide 15 sets the flow: feature film followed by post-film discussion.
- Slides 36-50 provide recurring journal prompts asking students to address the question,
  include their own opinions, and use critical thinking.
- Slide 51 describes thoughtful engagement with the journal prompt.
- Slides 54-56 describe brief, unprepared post-film "hot takes."
- Slides 64 and 69-74 describe group movie-review podcasts and film analysis.
- The older Biotechnology Lecture 10A summer-course promotion supplies the retained sentence
  about most of the grade coming from weekly writing prompts and getting the work done.

Restore that description of the learning experience without promising a fixed film lineup,
historical journal deadlines, old Google document links, or exact 2027 session dates.

## Shared consumers

The fragment is included by Genetics Lecture 09A, Genetics Lecture 10A, and Biotechnology
Lecture 10A. Rebuild those masters after changing it. Review the four individual course pages
in each course theme and check that the published dates and tentative assignment remain intact.

Temporary extraction and rendered-review artifacts for this restoration are under
`_temp/upcoming_courses_restore/`. The source correspondence above remains usable after those
temporary files are removed.

On November 5, all three ODP/PDF builds succeeded. The summary and four individual course pages
were visually reviewed in each deck. Source, ODP visibility, and PDF counts agree:

| Announcement deck | Authored | Hidden | PDF pages | Course summary and detail pages |
| --- | ---: | ---: | ---: | --- |
| Genetics 09A | 55 | 16 | 39 | 34-38 |
| Genetics 10A | 54 | 16 | 38 | 33-37 |
| Biotechnology 10A | 41 | 9 | 32 | 26-30 |

Strict native lint and 1,184 focused checks pass. Existing weather-caption size advisories remain
outside this course-description edit; there are no new capacity concerns in the restored pages.
