# Round 006 — unit-gap threshold graphs

## Plan

Third of the 20 newly authorized rounds; 17 remain after starting. Previous
candidate/solver snapshot: 771e52e; Round 005 evidence is retained separately.

Keep the rank characterization. For an original threshold CNF Phi introduce a
fresh selector z, replace every clause C by z OR C, and add unit NOT z. This is
equisatisfiable with Phi. In the associated cover graph the usual lower bound
is L. Selecting both endpoints of z, one endpoint of every other variable, and
omitting the z occurrence in every guarded clause gives a cover of size L+1.
Consequently the optimum is exactly L for SAT and L+1 for UNSAT. Every optimum
at a satisfiable threshold still decodes correctly, including all ties.

Reduce graph overhead by recognizing identical whole-tree restrictions: their
source optimum is one, so F returns the empty graph and G returns the full
label block. Otherwise the optimum is at least two and at most m-1: the block
{rho,a} plus every other leaf as a singleton is always an acyclic agreement
forest. Emit only thresholds 2,...,m-1. The last is always satisfiable and need
not use a selector. These are universal structural facts, not fixture shortcuts.

First discriminating checks: preserve all source threshold checks, compare
emitted graph sizes on the fixed 327 inputs, and run the entire prepared
F/independent optimum/G suite with 128-output cap and four disjoint shards.
Independently verify additional encodings with CP-SAT and the separate source
reference. No input family or output validity requirement is weakened.

Finite bounds: same 327 prepared inputs, same 12 additional Verify inputs,
same output caps; no timeout. The selector lemma and recovery proof require
independent review after executable verification. The possible tradeoff is a
larger clause clique but a tightly bounded UNSAT optimum; measure both graph
size and actual validation, without claiming optimal overhead.

Experience: Round 005 supplied the rank argument and measured improvement;
Round 004 supplied the all-optima threshold-cover proof. Neither unfinished
candidate is accepted merely because it is recorded.

## Evidence and diagnosis

Pending.

## Next action

Implement guards and the two proven structural simplifications; rerun all checks.
Experience extraction: pending.

Planned upper-bound refinement before full execution: obtain a feasible forest
by starting with singleton blocks and greedily accepting pairwise merges only
when the direct polynomial forest validator accepts them. At most m-1 merges
occur, with polynomially many pair checks; this is not an exact source solver.
Its final component count U is a certified upper bound on OPT. Emit thresholds
2,...,U only, and omit the guard at U because its feasibility is already
witnessed. The initial singleton forest always admits a pair merge, so U<=m-1.
This refines the planned structural threshold pruning and retains the same
unit-gap composition and general O(m^4) graph-size bound. G need not repeat the
greedy search; absent threshold namespaces decode to a full-label block, which
is rejected for the nonidentical inputs on this branch.
