# Round 005 — shared leaf ranks and LCA consistency

## Plan

Budget: second of 20 newly authorized rounds; 18 remain after starting this
round. Prior rounds remain recorded. Candidate baseline revision: 43f36e3.

Mechanism: each original tree vertex gets a small integer rank, shared across
copies of each labelled leaf. Parent rank <= child rank. Equal-rank leaf pairs
force their LCA to that same rank. Equal-rank leaves form a component. These
conditions should force its entire connecting subtree to be monochromatic,
make different components disjoint, and make component ancestry strictly
increasing in rank. Rooted-triple disagreements forbid a monochromatic triple.
Every acyclic agreement forest should extend to a rank assignment by propagating
the maximum rank of occupied ancestors through unused vertices. With ranks
0,...,k-1 this is an exact threshold verifier.

Use O(log k) bits per rank and exact Boolean equality/comparison gates. Retain
the parallel-threshold cover/DFVS composition and filter-based decoder from
Round 004. Compare vertex and arc counts on the same 327 prepared source records;
source definitions, optima and test-output cap remain unchanged.

First discriminating checks: all 1,759 prepared thresholds against independent
optima, decoded assignments against the independent partition reference, and
the full actual F/target-optimum/G suite. This mechanism should remove explicit
slot occupation and order clauses and reduce target size. A mismatch refutes
the rank characterization; smaller graphs alone establish no correctness.

Finite scope: same 327 inputs, up to 128 target optima each; added independent
Verify cases will exercise rank boundary values, label changes and tree-local
renaming. No time limits. Supporting solver repairs do not consume rounds.

Experience consulted: component-ancestry/node-renaming counterexample and Round
004's threshold cover argument and measured size. No claimed novelty for the
standard CNF/cover conversion. Independent review remains required.

## Evidence and diagnosis

Pending.

## Next action

Implement rank constraints and prove both directions before review.
Experience extraction: pending at closure.

Implementation checkpoint: initial rank CNF is retained in this partial commit.
Its running candidate loop and a four-leaf generic MaxSAT diagnostic were
stopped before replacing redundant gate circuits. These are execution
interruptions, not target oracle results. No prepared input or output coverage
is removed. The refinement uses direct equivalence/majority gates and removes
redundant internal-rank domain clauses (leaf bounds and monotone paths imply
those bounds). It is the same rank characterization, not a new mechanism.
