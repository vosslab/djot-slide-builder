take a look at the HTML table/CSS chromosome generation in the BPQ code
`~/nsh/PROBLEMS/biology-problems/problems/inheritance-problems/translocation/`
`~/nsh/PROBLEMS/biology-problems/problems/inheritance-problems/deletion_mutants/`

particularly the output of:

`robertsonian.py`
`translocation_meiosis_table.py`
`letter_translocation_problem_visual.py`
`chromosome_alterations_visual.py`
`deletion_mutant_random.py`/`deletion_mutant_words.py`

`robertsonian.py`/`translocation_meiosis_table.py` have the centrosomes that I like, larger rounded rects that can be used for labeling. For some reason the djot repo SVG tools went narrow and I complained so they added an oval around it that makes not sense.

`robertsonian.py` does a great job with Acrocentric chromosomes.

`translocation_meiosis_table.py`/`chromosome_alterations_visual.py` show how we can have two colors on the arms of a chromosome, which I think serves for a better model for showing banding for the cytogenic nomenclature diagrams. we can color the heterochormatin one color and the euchormatin a different color to show the banding, which is better than the hack we have now.

I am thinking of using more rounded rect chromosomes with a subtle end curve, I prefer the rounded rect over the typical full-rounded textbook illustrations. `letter_translocation_problem_visual.py`/`chromosome_alterations_visual.py` has a nice telomere representation at the ends for clear endings as well.

further, the deletion mutants in BPQ `deletion_mutant_random.py`/`deletion_mutant_words.py` are quite good in that the deletions show that chromosomal content is missing in a nice way.

there are some key features to chromosomes in our lecture, that are missing in BPQ:
1. paired sister chromatids connected at the centromere
2. curved chromosomes for use in deletion/inversion synapsis, cross-over, genetic exchange, translocation/Robertsonian metaphase orientations, and anaphase separation
3. banding patterns
4. inactived chromosomes (i.e. Barr bodies in X inactivation)

#1/#2 for curved chromosomes, I would like to maintain a consistent width. https://css-tip.com/rounded-tab/ https://blog.92learns.com/border-radius-rules/ https://designtoolkit.app/blog/css-border-radius-rounded-corners-tutorial https://www.linkedin.com/posts/asmanaeem3342_uidesign-uxtips-borderradius-activity-7359625090453372929-Bu5L https://flexicajourney.com/linkedin-posts/master-border-radius-perfect-corners/

I addressed #3 already with "
`translocation_meiosis_table.py`/`chromosome_alterations_visual.py` show how we can have two colors on the arms of a chromosome, which I think serves for a better model for showing banding for the cytogenic nomenclature diagrams. we can color the heterochormatin one color and the euchormatin a different color to show the banding, which is better than the hack we have now."

I am quite disappointed with the result

some changes I want
(1) C28 and many others: centromeres should always go past the edges of the chromosome, probably like a belt it goes vertically  (perpendicular to the chromosome) but stay about the same horizontal width (along the chromosome)
(2) C16 and many others: currently the curve of the chromosome coming out of the centromere is parabolic, I think it should have a more a cubic curve with an inflection point
(3) C08 the sense of scale is off, in the same diagram the chromosome lengths need to be conserve, unless duplicated through cellular means, etc.
(4) C20: I would represent alleles as genes like in the `chromosome_alterations_visual.py` and perhaps make the gene a different color from the rest of the chromosome
(5) C03 the centromeres appear in a layer behind the chromosomes.
(6) C05 and many other telomeres are complete garbage
(7) none of the chromosomes have the 3D effect of the BPQ
