# Gene tree mathematics contract

Approved data for the four-gene introduction, five-gene guided example, and complete answer
walkthrough of the existing six-gene worksheet. All matrix values are distance units. They
are not dates, elapsed years, or invented biological measurements. Four/five inputs are
new illustrative teaching data; six inputs preserve the existing worksheet exactly.

The production dataset is [gene_tree_example_data.json](../../../genetics/LECT11/djot/gene_tree_example_data.json); this report preserves the independently calculated stages.

## Representation and rules

- Stable dataset keys: `four_gene_intro`, `five_gene_weighted`, `six_gene_worksheet`.
- Tip labels are lowercase. Matrices start in alphabetical label order. Tree tip orders are
  `a,c,b,d`; `a,c,e,b,d`; and `a,c,b,e,d,f`, respectively.
- Cluster IDs sort their members alphabetically: `ac`, `ace`, `abce`, etc. A human label may
  use parentheses and commas. JSON `clusters` determines each matrix's row/column order.
- `step_0` is the original matrix/no completed joins. `step_k` has exactly k completed joins.
  `next_merge` identifies the minimum to ask students to find, before the next reveal.
- Each actual merge has a unique minimum. Equal values elsewhere in a matrix are harmless.
- UPGMA cluster distance is the mean of all original cross-cluster pairs. When updating from
  two existing cluster distances, weight each by its number of original tips.
- Join height = selected cluster distance / 2. Child branch = parent height - child height.
  Leaves have height zero. Every final root-to-tip path has the same length.
- No root stem has a specified biological length. Any drawn root stem is a visual connector,
  not an additional measured branch.
- The tree imposes a constant-rate/ultrametric model. Equal root-to-tip lengths are a model
  assumption, not evidence that the real sequences evolved at exactly the same rate.
- The four-gene input is ultrametric and matches every fitted tree path. Five/six inputs are
  not ultrametric: the tree summarizes their distances and does not reconstruct every raw
  pair exactly. Use "fitted tree distance" when reading a path from those trees.

## Four-gene introduction

Input pairs: `ab18 ac6 ad18 bc18 bd10 cd18`.

| Stage | Current clusters | Off-diagonal distances | Next minimum |
| --- | --- | --- | --- |
| 0 | a,b,c,d | ab18 ac6 ad18 bc18 bd10 cd18 | ac6 |
| 1 | ac,b,d | ac-b18 ac-d18 b-d10 | b-d10 |
| 2 | ac,bd | ac-bd18 | ac-bd18 |
| 3 | abcd | complete | none |

Joins: `ac` height3; `bd` height5; root height9.
Branches: a3, c3, ac-to-root6, b5, d5, bd-to-root4.
Newick: `((a:3,c:3):6,(b:5,d:5):4);`

Suggested active-learning sequence:

1. Predict the closest pair before tracing any path. Reveal a-c: 3+3=6.
2. Trace a-b: 3+6+4+5=18. Why is the root height 9, not 18?
3. Rotate the b-d node. Which matrix entries change? None: topology and path lengths persist.
4. Rebuild the tree from the matrix; after ac joins, do b and d join next or does b join ac?
   b-d=10 is less than either distance18.

## Five-gene guided example

Input pairs: `ab18 ac4 ad22 ae6 bc20 bd12 be22 cd24 ce10 de26`.

| Stage | Current clusters | Off-diagonal distances | Next minimum |
| --- | --- | --- | --- |
| 0 | a,b,c,d,e | ab18 ac4 ad22 ae6 bc20 bd12 be22 cd24 ce10 de26 | ac4 |
| 1 | ac,b,d,e | ac-b19 ac-d23 ac-e8 b-d12 b-e22 d-e26 | ac-e8 |
| 2 | ace,b,d | ace-b20 ace-d24 b-d12 | b-d12 |
| 3 | ace,bd | ace-bd22 | ace-bd22 |
| 4 | abcde | complete | none |

The first update is `(18+20)/2=19`, `(22+24)/2=23`, `(6+10)/2=8`.
The second update is the teaching hinge:

- `d(ace,b)=(18+20+22)/3=(2*19+1*22)/3=20`.
- `d(ace,d)=(22+24+26)/3=(2*23+1*26)/3=24`.
- Averaging the two cluster means equally gives20.5 and24.5. That gives the singleton e
  half the weight and the two-member ac cluster half the weight: each original tip no longer
  contributes equally. The mistaken final distance would be22.5 and root height11.25.
- Correct final distance: `(20+24)/2=22`. Direct original-pair check:
  `(18+22+20+24+22+26)/6=132/6=22`.

Joins: ac height2; ace height4; bd height6; root height11.
Branches: a2, c2, ac-to-ace2, e4, ace-to-root7, b6, d6, bd-to-root5.
Newick: `(((a:2,c:2):2,e:4):7,(b:6,d:6):5);`

Suggested prompts, each followed by its own complete reveal:

1. Find the first pair and predict its height (ac, height2).
2. Calculate ac-to-e. Will e join ac before b joins d? Yes: 8 < 12.
3. Vote on d(ace,b):20 or20.5. Explain what each denominator counts.
4. Calculate the other updated distance (ace-to-d24), then find the next merge (bd12).
5. Finish the root height and both root branches (11; lengths7 and5).
6. Compare raw ae6 with the tree path ae8. Why can both labels be correct? The input is
   not ultrametric; the UPGMA tree supplies fitted distances under its clock assumption.

Fitted pairs: ac4; ae=ce8; bd12; all six ace-versus-bd pairs22.
Residuals (raw minus fitted): ab-4, ac0, ad0, ae-2, bc-2, bd0, be0, cd+2, ce+2, de+4.
Do not call these residuals measurement error without empirical evidence.

## Six-gene worksheet walkthrough

Input pairs: `ab12 ac4 ad15 ae9 af18 bc10 bd13 be6 bf15 cd13 ce9 cf14 de11 df8 ef13`.
Source: migrated `genetics/LECT11/djot/assets/lect11d-gene_tree_activity/image_002.svg`.
All labels and 15 pairs independently agree with its XML text. No new worksheet is required.

| Stage | Current clusters | Off-diagonal distances | Next minimum |
| --- | --- | --- | --- |
| 0 | a,b,c,d,e,f | original matrix above | ac4 |
| 1 | ac,b,d,e,f | ac-b11 ac-d14 ac-e9 ac-f16 b-d13 b-e6 b-f15 d-e11 d-f8 e-f13 | be6 |
| 2 | ac,be,d,f | ac-be10 ac-d14 ac-f16 be-d12 be-f14 d-f8 | df8 |
| 3 | ac,be,df | ac-be10 ac-df15 be-df13 | ac-be10 |
| 4 | abce,df | abce-df14 | abce-df14 |
| 5 | abcdef | complete | none |

Every update, ready to reveal in native slide text:

1. Join ac at4/2=2. New distances:
   ac-b=(12+10)/2=11; ac-d=(15+13)/2=14;
   ac-e=(9+9)/2=9; ac-f=(18+14)/2=16.
2. Join be at6/2=3. New distances:
   be-ac=(11+9)/2=10; be-d=(13+11)/2=12; be-f=(15+13)/2=14.
   Check be-ac directly: (12+9+10+9)/4=40/4=10.
3. Join df at8/2=4. New distances:
   df-ac=(14+16)/2=15; df-be=(12+14)/2=13.
4. Join ac with be at10/2=5. New distance:
   abce-df=(2*15+2*13)/4=14. Equal weighting is valid here because ac and be each contain
   two original genes. Branches from height5 to ac and be have lengths3 and2.
5. Join abce with df at14/2=7. Root branches have lengths7-5=2 and7-4=3.
   Direct final original-pair check:
   (ad15+af18+bd13+bf15+cd13+cf14+de11+ef13)/8=112/8=14.

Final branches: a2, c2, ac-to-abce3, b3, e3, be-to-abce2, abce-to-root2,
d4, f4, df-to-root3.
Newick: `(((a:2,c:2):3,(b:3,e:3):2):2,(d:4,f:4):3);`
Every root-to-tip path equals7; for example a:2+3+2 and d:4+3.

The complete classroom answer should show all five merges, all four reduced distance
matrices, the final branch lengths, and a final path check. Pause for students' predictions
before each reveal; do not replace the existing worksheet or require a new submission.

Final reflection: raw ab12 becomes fitted ab10; raw af18 becomes fitted af14.
The algorithm did not subtract a hidden correction from those observations. It constructed
one ultrametric tree from averaged cross-cluster distances.

Fitted pairs: ac4, be6, df8; ab=ae=bc=ce10; all eight abce-versus-df pairs14.
Residuals (raw minus fitted): ab+2, ac0, ad+1, ae-1, af+4, bc0, bd-1, be0,
bf+1, cd-1, ce-1, cf0, de-3, df0, ef-1.

## Provenance and verification

Read-only BPQ sources:
`biology-problems/problems/inheritance-problems/phylogenetic_trees/` in the separate Biology Problems repository.
Snapshot SHA-256: `gene_tree_choice_plus.py` `86c1dce7a1327c6871c969066bd3851bf23a9f4852f63b4930b15751e5cf212f`;
`treelib/tl_definitions.py` `488cdcca6ab1c4e8fe82e797716ba5f72b2a8c65e8f0ed97f59e8b299d2e0897`. No BPQ source was changed and no external runtime is
needed by the selected datasets.

- Four topology: `tl_definitions.code_library['4balanced']` is `((a1b)3(c2d))`.
  `tl_tools.replace_taxa_letters(base, tuple('acbd'))` returns `((a1c)3(b2d))`.
- Five topology: `tl_definitions.code_library['3comb+pair1']` is `(((a1b)2c)4(d3e))`.
  Replacing with `tuple('acebd')` returns `(((a1c)2e)4(b3d))`.
- Both calls were executed with Python 3.12; `generate_taxa_distance_map` also produced
  all 6/all 10 tip pairs. The catalog keys, replacement orders, selected codes and pair coverage are recorded above.
- Four input uses exact node distances6,10,18. Five starts conceptually from node distances
  4,8,12,22 and deliberately varies the raw distances to make unequal-cluster weighting
  visible. BPQ `map_taxon_distances` and `add_distance_pair_shifts` inspired this approach;
  neither random procedure generated these selected numbers. No random seed is claimed.
- Executed `/opt/homebrew/bin/python3.12 -B _temp/gene_tree_refresh/verify_math.py`.
  All 12 joins agree with manually specified expected clusters/distances. Every current
  minimum is unique; every branch is nonnegative; every root-to-tip path is equal.
- Verification uses exact `Fraction` means over original pairs. Independently, installed
  SciPy 1.18.1 `linkage(..., method='average')` agrees on every cluster and merge distance.
  Four-gene fitted pairs equal the input exactly; five/six inputs fail the ultrametric test.

Misconceptions to catch: halving an internal branch without subtracting its child's height;
and treating each existing cluster as one equally weighted observation after an unequal merge.

This independent mathematical check does not certify slide typography, reveal behavior, or the full suite.
