# Round 004 — parallel component thresholds and CNF vertex covers

## Plan (recorded before construction)

Authorization: user allocated up to 20 additional exploratory rounds on
2026-09-22, following the Prepare restart. Retain rounds 001–003; this is the
first newly authorized round. Preparation commit: cf9f979.

Gap: polynomial executable encoding of the actual component-ancestry predicate,
and recovery from every globally minimum DFVS, without fixing one source forest.

Mechanism: polynomial Boolean verifier for partitions into canonical label
slots, minimal connecting subtrees, agreement of rooted triples, and a common
strict component order. Make one threshold formula for each k=1,...,|X|+1.
Convert each formula to the standard unweighted CNF vertex-cover graph and take
the disjoint union of their bidirected graphs. Every satisfiable threshold has
cover size equal to the variable/clause lower bound, so every minimum cover
there yields a satisfying assignment. Decode and independently validate all
threshold partitions and return one with the fewest components. The optimal
threshold ensures one decoded optimum; any other accepted partition is feasible.

This changes the mechanism from weighted clone penalties to parallel thresholds
and unweighted covers. The component predicate is also rebuilt after the audit.
No candidate calls a solver or enumerates all label subsets.

Experience searched: local and board-local entries by CNF, satisfiability,
vertex cover, feedback, ancestry and agreement forest. The local
component-ancestry entry requires invariance under tree-local node identifiers.
The generic CNF cover baseline argument is reusable, but its former MAAF
application is withdrawn. The old clone construction's size and solver limits
motivate avoiding weight expansion. No additional relevant board-local entry
matched. Mere presence is not evidence.

First discriminating check: independent SAT checks of the threshold formulas
and all decoded assignments on the complete prepared source family, followed
immediately by the actual F/independent minimum DFVS/G harness once executable.
A formula mismatch refutes the encoding. Matching thresholds alone does not
validate the target construction. A full candidate pass supports only its stated
finite coverage; the general proof and independent reviewer remain required.

Finite scope: all 327 prepared source records, candidate suite cap 128 distinct
minimum target outputs per source, plus targeted degeneration and composition
checks. No solver, subprocess, shell or campaign time limits.

## Evidence and diagnosis

Pending.

## Next action

Implement the polynomial verifier and full maps, prove each correspondence,
then run the prepared suite. Preparation/source ground truth remains fixed.

Experience extraction: pending at round closure.

### Closeout (2026-09-22)

Local formula diagnostics passed all 327 prepared records: 1,759 thresholds and
759 decoded minimum partitions. `formula_check.py` imports the candidate only
to obtain its CNF; independent source-reference code supplies validity and stored
ground truth supplies optima. This is not an independent target-oracle result.
The graph-size probe reached 77,199 vertices and 252,350 arcs at seven leaves.
The user added a preference to minimize overhead where practical.

The full target loops were started with the prepared positional solver and then
an independent CP-SAT vertex-cover encoding for bidirected graphs. Neither full
loop completed before this mechanism was superseded. Stopping the obsolete
runs is recorded as an execution interruption, not UNSAT, an optimum, an
exhausted family or a correctness counterexample. The CP-SAT oracle passed the
complete Prepare self-test (`oracle-self-test.txt`). A separate first-instance
CP-SAT optimization diagnostic obtained optimum 88, but it did not complete
the 128-output recovery loop and is not counted as a candidate pass.

Outcome: **inconclusive** as an executable reduction, with a candidate general
proof and passing source-formula diagnostics. No independent review occurred.
New mechanism for Round 005: monotone integer ranks on original tree vertices,
with equal-leaf ranks propagated to their LCA. It replaces explicit component
slot occupancy/order circuits and can eliminate an asymptotic clause factor.

Experience extraction: no new general claim promoted from this round; the
parallel-threshold cover proof remains a candidate argument to be reviewed with
the next mechanism. The size evidence and its consequences are retained here.
New allocation used 1/20; remaining 19. Historical total rounds 4, distinct
mechanisms including the historical literature audit 3.
