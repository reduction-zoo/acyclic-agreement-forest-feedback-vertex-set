# Unit-gap covers for parallel feasibility thresholds

Tags: exact optimization, all optimal outputs, CNF, vertex cover, bidirected DFVS.

## Claim and applicability

Let Phi be an explicit CNF with nonempty clauses. Add a fresh Boolean z to every
clause and add the unit clause NOT z. The resulting formula is equisatisfiable.
In the usual variable-edge / clause-clique vertex-cover construction, write
L = number of variables + sum(clause width minus one). Its optimum is exactly
L when Phi is satisfiable and L+1 otherwise: for the latter upper bound select
both endpoints of z, one per other variable, all non-z occurrences in guarded
clauses, and no occurrence of the negative unit.

Every size-L cover still selects exactly one endpoint per variable and decodes
to a satisfying assignment. Replacing edges by opposing arcs preserves all
cover sets as DFVS sets. Thus disjoint threshold graphs can encode an exact
optimization problem without optimizing arbitrary unsatisfied-clause penalties
at infeasible thresholds. A feasible polynomially obtained upper bound may
prune thresholds, provided the true optimum's threshold remains represented.
Recovery must independently validate proposals from infeasible thresholds.

The lemma does not establish the source CNF's correctness, permit an approximate
target solver, or give an approximation ratio for the source problem. The graph
can grow because every guarded clause gains one vertex and its incident edges.

## Evidence and status

General argument in the current [proof](../../campaigns/acyclic-agreement-forest-feedback-vertex-set/work/proof.md),
sections on guarded formulas and recovery. Independent advance review completed; see the
[review](../../campaigns/acyclic-agreement-forest-feedback-vertex-set/reviews/rank-threshold/review.md)
and [focused follow-up](../../campaigns/acyclic-agreement-forest-feedback-vertex-set/reviews/rank-threshold/follow-up.md). Candidate
map revision: `8b2e404`. The finite [gadget diagnostic](../../campaigns/acyclic-agreement-forest-feedback-vertex-set/rounds/006/gadget_check.py)
checks the actual graph on all 256 subsets of the eight nonempty two-variable
clauses, against exhaustive assignments and an independent exact graph solver.
It passes; this does not replace the general lemma.

## Consequence for search

Use the guard when the decoder needs only feasible thresholds but the exact
target contract would otherwise demand difficult irrelevant optimization on
infeasible ones. Measure its clause-clique cost. A graph-only exact oracle can
also count surplus above disjoint clique bounds instead of all selected vertices;
this is an equivalent solver encoding, not a source-informed oracle shortcut.

## Use history

- 2026-09-22: extracted during [Round 006](../../campaigns/acyclic-agreement-forest-feedback-vertex-set/rounds/006/round.md).
  At extraction, full candidate verification and review were in progress; no completed-rule
  success is inferred from the local gadget check.

- 2026-09-22 closeout: the current complete rule passes all 327 prepared inputs
  and 38,427 target recoveries, plus 12 additional inputs and 33 recoveries.
  Independent review supports the general argument and contributes 47 targeted
  recovery checks. The inspected manuscript retains finite-coverage and
  novelty/overhead qualifications. Earlier pending labels describe the extraction
  stage; the current review status is advance for rule completion.
