# Preparation — testing foundation status

Stage: **Prepare** (started 2026-09-21). This record states the current state of
the testing foundation honestly, including what is not finished. Preparation
establishes no reduction-correctness claim.

Commands (no Python project needs to exist for the current foundation; `check.py`
uses only the standard library plus Z3, which is present in the environment):

```sh
cd campaigns/acyclic-agreement-forest-feedback-vertex-set/work
python3 check.py --self-test                 # 91 checks, 0 failures
python3 evidence/rspr_reference.py           # independent rSPR distances
```

## 1. What is complete

| Artifact | State |
|---|---|
| `contract.md` | Fixed JSON encodings for both endpoints, legality predicates, candidate CLI contract, checker interface |
| `cases.json` | Nine source fixtures covering the degenerate and the discriminating instances, plus target-side validity fixtures |
| `check.py` target side | Independent min-DFVS oracle: exhaustive subset enumeration and a Z3 decision oracle; explicit Kahn witness validation |
| `check.py` source output validator | Recomputes components from the source instance; checks the partition, disjointness, coverage, isomorphism of component trees, and acyclicity |
| `evidence/rspr_reference.py` | Independent breadth-first search over rooted subtree prune and regraft moves |
| `evidence/agreement_forest_reference.py` | Second, independent edge-cut enumeration written against the same definition (being repaired, see §4) |

The target oracle is validated: on 30 seeded random digraphs (1–6 vertices) the
exhaustive and the Z3 decisions agree, every returned set passes the explicit
Kahn check, and the deliberate fixtures (a directed triangle, a two-cycle, a
self-loop, an acyclic input, an undeclared vertex, a repeated vertex) are
accepted or rejected as they must be.

## 2. What is pending

The **source oracle is not trustworthy yet** and its values are not used as
ground truth. `cases.json` stores `null` for every source optimum; the self-test
prints a `PENDING` line per case instead of accepting anything. The finite search
family is already declared and enforced (`SOURCE_ORACLE_LEAF_CAP = 7` leaves,
i.e. all cut subsets of both trees), and the intended rendering rule is fixed in
`contract.md` §1.3; what is missing is a correct implementation of the component
rendering and its cross-check against `evidence/rspr_reference.py`.

This is a missing capability reported as pending, not a passing check.

## 3. Encodings and predicates

Both endpoints are optimization endpoints and both output sets are nonempty on
the admitted domain, so no `NO-SOLUTION` output is admitted on either side.

- Source instances are two rooted binary phylogenetic trees on a shared node-id
  set with a separate `root_label`, so that the union ancestry relation of
  condition (d) is a relation on one vertex set.
- Source outputs list the two cut sets and, per component, its label set plus its
  vertex set and induced arc set in each tree. Validity is decided from the source
  instance alone.
- Target instances are an explicit vertex list and arc list; `num_components` is
  a redundant echo that is cross-checked.
- Target outputs are a list of vertex ids; validity is feasibility plus exact
  minimum cardinality, the latter established by an independent oracle.

## 4. Diagnosis log (why the source side is pending)

During Prepare the source side was attacked in this order. Each entry names the
reading tried, the observed defect and the evidence.

1. **Partition + minimal connecting subtrees.** Let a block's connecting subtree
   be the minimal rooted subtree spanning its members, require the trees to be
   vertex-disjoint across blocks, and take the fewest blocks. This reading makes
   the all-singleton partition valid on every instance, because a singleton's
   connecting subtree is a single vertex — including the root label's singleton,
   which is why the root label must be modelled as an actual pendant leaf rather
   than as a synonym for the declared root. The reading is therefore degenerate.
2. **Edge cuts (the standard model).** Components are the parts of `T - S` after
   deleting unlabelled leaves and suppressing degree-2 vertices; an agreement
   forest is a pair of cut sets whose components match bijectively on label set
   and component tree. This is the model of Bordewich-Semple 2005 and of
   arXiv:2202.09904 §2, and it is the reading fixed in `contract.md` §1.3.
3. **Rendering.** The subtlest defect found is in rendering a part as a rooted
   tree. A part's apex is *not* always the root of the rendered tree: when the
   apex is an unlabelled vertex of degree 2 it must be suppressed, which lifts
   one child. Naive implementations either keep the apex (wrong component tree)
   or delete it without lifting its child (component tree split into several
   roots). The self-test's `component ['b', 'c'] is not a rooted labelled tree`
   failures recorded below are this defect.
4. **Failing run retained.** The self-test output showing the rendering defect is
   retained in §7. No expectation was changed to make it pass; the affected
   checks were removed and the underlying capability is reported pending.
5. **Cross-check not yet available.** `evidence/agreement_forest_reference.py`
   currently reuses the same rendering, so it cannot yet serve as an independent
   cross-check. Its status is "being repaired" and it is not cited as evidence.
6. **Unresolved discrepancy in the reference table.** For the five-leaf instance
   `T1 = (((a,b),(c,d)),e)`, `T2 = (((a,b),(d,e)),c)`, the breadth-first search
   reports `d_rSPR = 2` while an edge-cut search finds a two-component forest
   (cutting `(c,·)` in both trees). Either the move generator of
   `evidence/rspr_reference.py` misses valid rSPR moves on five leaves, or the
   agreement-forest identity fails on that instance. Both readings are recorded;
   neither is trusted, and the instance is not used as a stored expectation.

## 5. Reference values the repaired oracle must reproduce

These are established independently of the source oracle and are the checks that
will settle it.

| Instance | Value | Independent evidence |
|---|---|---|
| `T1 = T2 = ((a,b),(c,d))` | one component | `evidence/rspr_reference.py`: `d_rSPR = 0` |
| `T1 = ((a,b),c)`, `T2 = ((a,c),b)` | `\|F\| = 2` | `evidence/rspr_reference.py`: `d_rSPR = 1` |
| `T1 = ((a,b),(c,d))`, `T2 = ((a,c),(b,d))` | `\|F\| = 3` | `evidence/rspr_reference.py`: `d_rSPR = 2`, exhibited path `((a,b),(c,d)) → (((a,b),c),d) → ((a,c),(b,d))` |
| one leaf | one component | the degenerate instance |
| the cited issue's worked example | the issue's `\|S\| = 3` and the review comment's `h = 1` are both wrong | `contract.md` §5 |

The identity `d_rSPR(T1,T2) = |F| − 1` for a maximum agreement forest is
Theorem 2.1 of arXiv:2202.09904; the finite checks above instantiate it on
instances small enough to search exhaustively.

## 6. Finite bounds declared in advance

- Source search family: all cut subsets of both trees, admitted only for
  instances with at most `SOURCE_ORACLE_LEAF_CAP = 7` leaves.
- Target oracle: exhaustive subset enumeration for at most
  `EXHAUSTIVE_DFVS_VERTEX_CAP = 18` vertices; otherwise the Z3 decision oracle
  with pseudo-Boolean cardinality constraints and a positional acyclicity
  encoding.
- Distinct minimum target sets passed to `--extract` per instance:
  `OPTIMAL_DFVS_ENUM_CAP = 128`.

No wall-clock, solver, subprocess or wrapper timeout appears anywhere. A harness
limit that kills a run is an execution failure, not an oracle answer.

## 7. Retained failing run

```
$ python3 check.py --self-test
...
self-test: 125 checks, 30 failures
  FAIL case rSPR1_3: encoded optimum validates: component ['b', 'c'] is not a rooted labelled tree
  FAIL case quartet_swap_4: encoded optimum validates: component ['b', 'c', 'd'] is not a rooted labelled tree
  FAIL case pseudorooted_5: encoded optimum validates: component ['b', 'c', 'd', 'e'] is not a rooted labelled tree
  ...
```

This is the rendering defect of §4.3. The run is retained rather than repaired
silently; the current self-test reports the source optima as pending and exits 0
on the checks that do hold.

## 8. Consequence for the campaign

A candidate reduction must not be constructed while the source objective is
ambiguous: the recovered forest would be checked against a source optimum this
foundation cannot yet establish. The blocking work is (i) fix the component
rendering, (ii) cross-check the repaired oracle against
`evidence/rspr_reference.py` on the instances of §5, and only then (iii) restore
the stored ground truth in `cases.json`. If the campaign instead adopts the
minimal-subtree reading named in `contract.md` §6, that is a different source
problem and the question must be amended first.
'''
