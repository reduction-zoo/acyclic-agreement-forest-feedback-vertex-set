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

Oracle repair: the bidirected graph solver now derives a valid lower bound by
packing vertex-disjoint cliques and edges directly in the actual target graph.
At that bound every group must be tight and every uncovered vertex omitted;
these logical consequences are added explicitly for enumeration. Below-bound
impossibility follows from the graph certificate; higher bounds are rejected
only by exact SAT UNSAT. Neither vertex-name conventions nor source values are
used. The CP-SAT candidate loop stopped after one source record and 128 recovered
target optima; it is an interrupted run, not a completed suite. A native Z3
Boolean/PB encoding replaces its search, with the same graph predicate and
128-output cap. No source expectations or target-output requirements changed.

Further exact oracle decomposition: solve weak connected components separately
and take products of their minimum outputs. Minimum DFVS/cardinality is additive
on these components. The cap stays 128; each component has an independently
proved optimum and distinct output enumeration. This removes search coupling
between disconnected thresholds without changing the target predicate. The
prior Z3 run completed three source records (384 recoveries) before replacement;
the prior additional CP-SAT run completed one (4 recoveries). Both incomplete
runs remain as interruption evidence. The final runs use separate new log paths.
Recovery subprocesses are independent and can execute eight at a time; solver
calls and source validation remain in the main process.

The sequential full-suite run is superseded by four disjoint shards of the same
327 records. Its partial output remains in `candidate-final.txt`; it is not
added to the new recovery count. `check.py --shard INDEX 4` selects the indices
congruent to INDEX modulo 4, without changing target output cap or any predicate.
All four exit statuses and their union of case names must be checked before
claiming suite completion. This is scheduling, not a smaller search family or
a new construction round. No wall-clock limit is introduced.

## Closeout

Rank characterization and refined CNF passed all 327 source records, all 1,759
thresholds and 815 decoded minimum rank assignments. Overhead comparison on the
same records is in `overhead.txt`: at seven leaves median vertices fell from
77,799 to 29,220 and median arcs from 254,150 to 99,202. The rank construction
has an O(m^4) graph-size bound instead of the slot baseline's O(m^5).
The generated per-input `sizes.json` is excluded as reproducible bulk output:
from the repository root at revision `9b0ef14`, with its locked environment,
run `uv run --locked python campaigns/acyclic-agreement-forest-feedback-vertex-set/rounds/005/formula_check.py`.
It uses the committed cases, no new sampling. The compact full diagnostic log
is retained as `formula-check.txt`.

Actual target verification completed 22 distinct prepared records in the four
shards, with 128 minimum-target recoveries each (2,816). Earlier sequential
prefixes are duplicates and are not added. Additional independent CP-SAT checks
completed 6 inputs and 24 recoveries. No mismatch was found; the full families
remain incomplete. These runs are stopped before the construction changes and
are recorded as execution interruptions, not oracle answers on remaining inputs.

Diagnosis: the ordinary CNF cover gadget has no fixed gap above its cover lower
bound on an unsatisfiable formula. Optimizing those unsatisfiable threshold
components is irrelevant to the decoder but still required by the target
contract. A new selector-guard construction can force every threshold optimum
to be exactly L or L+1. This is a different composition strategy and starts
Round 006. It will also remove the identical-tree and known-unneeded thresholds.

Outcome: inconclusive executable verification; candidate rank theorem supported
by a general proof and finite source checks, not independently reviewed.
Experience extraction: the rank lemma is retained as a candidate proof, not
promoted as an established reusable result until review. No new experience file.
New allocation used 2/20, remaining 18; total historical rounds 5, distinct
mechanisms 4 (including the original literature audit).
