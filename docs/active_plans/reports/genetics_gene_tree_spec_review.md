# Genetics gene-tree refresh: fresh specification review

Status: **PASS for the source content and instructional sequence reviewed**, November 14, 2026. No blocking specification finding. This review treats a question as a new prediction when its specific result has not already been explicitly stated; supplying raw inputs, completed branches, or a tree for a subsequent path calculation is appropriate. It does not demand that every follow-up reasoning question be independent of previous teaching.

Historical naming note: the November 14 review called the five-sequence and class-activity
materials Lectures 11C and 11D. Their current source paths are Lecture 11D and Lecture 11F.

## Evidence

- [Lecture 11A](../../../genetics/LECT11/djot/lect11a-2026_announcements.djot#L20) states no quiz, homework 09 and 10 due, the November 24 break, December 1 Quiz 4, December 8 Quiz 5 and homework 11 and 12, December 15 final, and The Animal Kingdom (2023). [Lecture 12A](../../../genetics/LECT12/djot/lect12a-2026_announcements.djot#L15) is dated December 1 and lists the chromosome topics and Quiz 4.
- [Lecture 11B](../../../genetics/LECT11/djot/lect11b-interpreting_gene_trees.djot#L54) asks about shared nodes, rotations and path distances before each answer. Its [four-gene walkthrough](../../../genetics/LECT11/djot/gene_tree_four_steps.djot#L3) asks for each merge and update before revealing it, then asks for root-to-tip paths before the completed tree and check. It includes a concise comparison of tree methods.
- [Current Lecture 11D](../../../genetics/LECT11/djot/lect11d-upgma_weighted_averages.djot#L55) explains cluster membership and original-pair averages. In its [five-gene walkthrough](../../../genetics/LECT11/djot/gene_tree_five_steps.djot#L105), the 20 versus 20.5 question precedes the weighted calculation and explanation. Every merge and update has a prior prediction. The finished-tree discussion distinguishes the fitted path from non-ultrametric raw values.
- [Current Lecture 11F](../../../genetics/LECT11/djot/lect11f-upgma_class_activity.djot#L32) uses the existing worksheet. Its [six-gene walkthrough](../../../genetics/LECT11/djot/gene_tree_six_steps.djot#L3) preserves all 15 original pairs and shows five joins, four reduced matrices, heights, all ten child branches and a root-to-tip check. Each merge and update is prompted first. The [fitted a-to-b question](../../../genetics/LECT11/djot/lect11f-upgma_class_activity.djot#L65) precedes the explicit answer; the earlier raw matrix, completed tree and branch table supply information needed to calculate it, not the explicit result.
- The native lower-triangle tables use size-specific groups; SVG tree text declares Atkinson Hyperlegible Next. The [math contract](genetics_gene_tree_math.md) records local recipe/data provenance, exact original-pair averaging, heights, branches and independent BPQ topology checks. Four inputs match their fitted paths; five and six do not, and their slides explain that distinction.

## Checks and boundaries

- Read the approved [plan](../active/genetics_gene_tree_refresh_plan.md), repository guidance, masters and included walkthroughs in their actual include order; compared worksheet matrices and all merge/branch answers with the independently documented contract.
- `/opt/homebrew/bin/python3.12 -B _temp/gene_tree_refresh/verify_math.py`: exit 0; 12 expected merges, SciPy average linkage and root-to-tip checks agree; four input is ultrametric and five/six are not. This check writes its temporary dataset under `_temp/`.
- `rg -n -i '@replaceme|replace\s*me' genetics/LECT11/djot/lect11[bcd]*.djot genetics/LECT11/djot/gene_tree_{four,five,six}_steps.djot`: exit 1, no source matches.
- This is a source specification review, not independent certification of the 323-path migration, original-media hashes, untouched external repositories, E preservation, rendered capacity/markers, native editability, or presentation playback. Those require the separate quality and integration reviews. The final D export was still in progress during this review; no LibreOffice command was run here.
