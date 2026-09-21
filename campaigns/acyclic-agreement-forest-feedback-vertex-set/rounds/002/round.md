# Round 002 — exact verifier-to-DFVS encoding

## Plan

This round tests a materially different mechanism from the rejected Cycle
Killer reuse: encode the source witness relation and its component objective as
an exact Boolean optimization instance, then use an assignment-preserving
SAT-to-DFVS construction. The intended interface is a graph in which every
minimum feedback vertex set decodes to a satisfying source witness and the
number of deleted assignment or cost vertices is an affine function of the
number of forest components.

The first discriminating check is a finite assignment gadget test. For all
Boolean formulas in a declared small family, enumerate every feedback vertex set
of the gadget at the proposed optimum, decode it, and check both satisfiability
and the cost relation. If a minimum DFVS can use a clause or consistency vertex
in a way that does not decode to an assignment, this mechanism is rejected before
any MAAF encoding is attempted.

Full composition obligations are unresolved at the start: a polynomial-size
Boolean encoding of all legal MAAF partitions, an exact component-count cost,
and a proof that the SAT-to-DFVS gadget preserves every target optimum and tie.
The local gadget test cannot establish those global obligations.

Finite scope: formulas with at most three variables and three clauses, all
clause widths at most three; exhaustive target enumeration has at most 18
vertices and no timeout.

## Evidence and diagnosis

Rusu's primary paper gives an exact assignment correspondence for its
representative graphs: Claim 3 states that a set of variables is a standard
truth assignment exactly when it is a feedback vertex set (apart from the
trivial all-variable set), and Claim 5 equates the minimum FVS size with the
minimum number of true variables. The paper's construction is specialized to
its M-NAE formula family, so it does not directly encode the MAAF verifier or
its component objective. The source used for this audit is the v1 arXiv HTML
version, read with the web tool on 2026-09-21:
<https://arxiv.org/html/1809.01998>, Sections 2--4, especially Claims 2--5.

The implemented candidate uses a more general exact composition. It encodes a
forest with connected slot assignments, rooted-triple agreement clauses,
apex-suppressed retained-edge variables, and a strict total order for the
union acyclicity condition. A finite Z3 check enumerated up to 16 minimum
formula assignments on every prepared case and decoded each through the
candidate's cover representation; all recovered forests passed the independent
source validator. The retained log is
[formula-optimum-check.txt](formula-optimum-check.txt).

The first full candidate-harness run produced a legal graph with 1,118 target
vertices on `one_leaf`, but the independent positional DFVS oracle did not
finish before the run was manually interrupted. The raw status is preserved in
[candidate-harness-interruption.txt](candidate-harness-interruption.txt). This
is an execution failure only. The formula check does not replace the required
independent target check.

The generic composition is therefore supported by the local all-optimum
formula checks and the proof in `work/proof.md`, but executable target-side
verification remains unresolved. The main suspected cause is the baseline
cost and clone expansion of the generic vertex-cover composition, which gives
the prepared positional oracle a large optimization instance; this is a
performance diagnosis, not a correctness claim.

## Next action

Preserve this candidate and use the remaining round to seek a lower-baseline
DFVS composition or an independent target-side check that can enumerate the
same clone graph without changing the fixed harness. Do not treat the
interrupted oracle run as evidence against the construction.

## Experience extraction

Created
[research/experience/optimization-cnf-to-dfvs.md](../../../../research/experience/optimization-cnf-to-dfvs.md),
which records the weighted-cover clone construction, its all-minimum-output
argument, and the baseline-size limitation observed here.
