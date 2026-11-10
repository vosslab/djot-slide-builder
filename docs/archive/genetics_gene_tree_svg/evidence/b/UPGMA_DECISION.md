# Authorized B consistency repair

Root authorized the original manual rule: average the two current entries after each join, not taxon-count weighted averages. All21 starting inputs and merge order BF, AD, BFG, ADBFG, ADBFGC, ADBFGCE remain unchanged. Source overview image021 supplies all displayed rounding. Its complete exact-data check is current_cluster_average_check.json.

Old detail image023: AD-BFG16.50; C-BFG30.67; E-BFG33.00; ADBFG-C29.00; ADBFG-E32.60; final34.00; heights8.25,14.5,17.0. These are taxon-weighted, unlike the intended manual example.

New detail copies overview image021 displayed values: AD-BFG15.80; C-BFG30.30; E-BFG31.80; ADBFG-C28.40; ADBFG-E31.90; final36.40; heights7.9,14.2,18.2. The exact unrounded manual computation gives15.75,30.25,31.75,28.375,31.875,36.4375 and heights7.875,14.1875,18.21875. Source rounding is preserved at display precision rather than silently replacing it with freshly rounded intermediates.

The full6matrix/6tree teaching sequence retains every source matrix and branch increment, now consistently with the overview. The method heading and original definition remain; native text explicitly states current-entry averaging. This is an instructor-authorized source consistency change, not a claim that equal-current-cluster averaging is standard size-weighted UPGMA.
