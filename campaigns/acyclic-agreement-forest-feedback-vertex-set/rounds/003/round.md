# Round 003 — exact independent solving of clone targets

## Plan

Round 002 left a mathematically specified candidate but the fixed positional
DFVS oracle and the first generic independent target solver were too slow on
the expanded clone graphs. This round tests a solver-level verification route:
compress the actual bidirected target to its twin-group weighted vertex-cover
instance and solve that instance with an independent exact CP-SAT model.

The first discriminating check is the `common_cherry_4` target: if CP-SAT can
obtain its global optimum and an alternate optimum without a wall-clock limit,
pass both recovered outputs through the independent source validator. A solver
failure is recorded as pending or execution failure, never as a target answer.

Finite scope: the prepared cases, with no solver or wall-clock timeout. The
clone grouping is derived only from the explicit target graph; this verifier
does not import `algorithm.py` or `check.py`.

## Evidence and diagnosis

The actual `common_cherry_4` target has 34,025 vertices. Twin compression
produces 5,670 weighted groups and 9,552 group-level cover edges. An independent
single-worker CP-SAT model returned a feasible incumbent of objective 20,929
after 112.87 seconds but did not prove optimality. The raw result is retained in
[cp-sat-output.txt](cp-sat-output.txt). Because a feasible incumbent is not a
minimum target output, it was not used for recovery and supplies no oracle
answer. The fixed positional Z3 oracle and the independent weighted Z3 model
also remained unresolved on the larger cases.

The solver-level route therefore did not remove the execution bottleneck. This
does not refute the candidate proof: the graph is a polynomial explicit clone
construction, and the smaller independent run already checked four actual
minimum target outputs. It leaves all-target-tie verification and independent
review pending.

## Next action

The three-round campaign budget is exhausted. Preserve the candidate as
incomplete and resume only with additional authorization or a materially smaller
exact target construction; do not report the feasible CP-SAT incumbent as a
minimum solution.

## Experience extraction

No new mathematical entry. The execution finding updates the existing
[optimization CNF to DFVS experience](../../../../research/experience/optimization-cnf-to-dfvs.md):
twin compression reduces the `common_cherry_4` target to 5,670 groups, but both
exact solvers still fail to certify its optimum within the bounded session.
