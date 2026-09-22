# Exact optimization CNF to unweighted DFVS through clone covers

## Claim/applicability

For a satisfiable CNF whose minimum objective is the number of true variables
in a designated set (U), an exact all-optimum reduction to unweighted DFVS
can be built by first using weighted vertex cover. Give every Boolean variable
an endpoint edge, make each clause a clique of clause vertices joined to the
endpoints for its literals, and use a baseline (B>|U|). Give every variable
endpoint weight (B), add one to the true endpoint for variables in (U), and
give each clause vertex weight (B). Replace each weighted cover vertex by
that many independent clones and replace each cover edge by all bidirected
clone pairs.

## Evidence/status

The cover argument is direct. A satisfying assignment attains the clause
baseline. An unsatisfied clause costs an extra (B), which is larger than any
possible saving in the designated objective. Selecting both endpoints of a
variable costs an extra (B), so every minimum cover selects one endpoint per
variable and every minimum cover decodes to a minimum satisfying assignment.
In the clone graph, every maximum independent set contains either all or none
of each clone group because a group's clones have identical neighbourhoods;
complementation gives the same property for every minimum vertex cover and
therefore every minimum DFVS.

Round 002 applied this construction to a purported polynomial CNF encoding of MAAF.
**Correction (2026-09-22):** that source encoding and both original source
checkers used tree-node arc unions instead of component ancestry. Its MAAF
application is withdrawn; the generic CNF/cover argument is a separate claim.
See [Prepare audit](../../campaigns/acyclic-agreement-forest-feedback-vertex-set/work/preparation.md).
The following records the historical, invalidated evidence. Up
to 16 minimum CNF assignments per prepared source case all decoded to valid
minimum forests. The independent positional DFVS harness did not finish its
first expanded graph before manual interruption, so the construction is a
supported candidate mechanism with target-side execution evidence pending.

## Consequence for search

The route supplies a general proof template for exact recovery from all target
ties, but its clone expansion creates a large baseline DFVS instance. A future
attempt should retain the all-minimum group argument while reducing the target
baseline or using a target-side verifier that can exploit the clone structure.
The independent twin-group verifier reduced `common_cherry_4` to 5,670 groups,
but Z3 did not finish its exact optimum and CP-SAT returned only a feasible
incumbent, so this compression does not discharge target-side verification.

## Use history

- 2026-09-21: created from Round 002 of the acyclic agreement forest campaign.

## Evidence links

- [Round 002](../../campaigns/acyclic-agreement-forest-feedback-vertex-set/rounds/002/round.md)
- Historical candidate and proof: Git revision `81e6d3a`, `work/algorithm.py` and `work/proof.md`.
