# Monotone tree ranks characterize acyclic agreement forests

Tags: phylogenetic trees, component ancestry, rooted triples, polynomial CNF.

## Claim and applicability

For two rooted binary trees on the same augmented leaf set, an acyclic agreement
forest with at most k components exists exactly when each tree vertex can be
assigned a rank in 0,...,k-1 with shared leaf ranks, nondecreasing ranks along
tree edges, equal-rank leaf pairs sharing that rank with their LCA, and no
monochromatic rooted triple on which the trees disagree.

Equal leaf ranks define blocks. Their original connecting subtrees are
monochromatic and disjoint; conflicting triples are excluded; every component
ancestry arc increases rank. Conversely topologically number the forest blocks
and give each tree vertex the minimum rank of a descendant leaf. Disjointness
ensures that this extends each component's rank throughout its connecting
subtree. The full proof includes this extension step, which cannot be replaced
by identifying internal vertices of the two trees.

This applies to rooted binary trees and component-ancestry acyclicity. It does
not cover nonbinary refinements, a union of tree-node arcs, or arbitrary graph
partition constraints without a separate proof.

## Evidence and status

General proof and binary CNF are in [work/proof.md](../../campaigns/acyclic-agreement-forest-feedback-vertex-set/work/proof.md)
and `algorithm.py`, first implemented in Round 005. Independent advance review completed; see the
[review](../../campaigns/acyclic-agreement-forest-feedback-vertex-set/reviews/rank-threshold/review.md)
and [focused follow-up](../../campaigns/acyclic-agreement-forest-feedback-vertex-set/reviews/rank-threshold/follow-up.md).
The [formula diagnostic](../../campaigns/acyclic-agreement-forest-feedback-vertex-set/rounds/005/formula-check.txt)
checks 1,759 thresholds on 327 inputs and 815 decoded minimum rank assignments.
This is source/formula evidence, not a substitute for actual-target verification.

## Consequence for search

Use ranks to represent component identity and ancestral order together, avoiding
a separate component-slot occupancy array and order relation. Binary comparison
gates and rooted-triple clauses produce O(m^3 + m^2 log^2 m) cover edges per
threshold. Encoding equality alone would miss subtree disjointness; the LCA
condition and edge monotonicity are both essential.

## Use history

- 2026-09-22: extracted during [Round 006](../../campaigns/acyclic-agreement-forest-feedback-vertex-set/rounds/006/round.md)
  from the unchanged rank mechanism of Round 005. Its measured graph-size
  reduction is recorded there; full current target checks and review were pending at extraction.

- 2026-09-22 closeout: the current complete rule passes all 327 prepared inputs
  and 38,427 target recoveries, plus 12 additional inputs and 33 recoveries.
  Independent review supports the general argument and contributes 47 targeted
  recovery checks. The inspected manuscript retains finite-coverage and
  novelty/overhead qualifications. Earlier pending labels describe the extraction
  stage; the current review status is advance for rule completion.
