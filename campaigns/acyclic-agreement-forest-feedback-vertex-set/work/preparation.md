# Preparation — testing foundation status

Stage: **Prepare** (2026-09-21). This record states the current state honestly,
including what is still unresolved. Preparation establishes no
reduction-correctness claim.

Commands (no Python project is needed for the current foundation; `check.py` uses
only the standard library plus the environment's Z3):

```sh
cd campaigns/acyclic-agreement-forest-feedback-vertex-set/work
python3 check.py --self-test            # 143 checks, 0 failures
python3 evidence/rspr_reference.py      # independent rSPR distances
```

## 1. What is complete

| Artifact | State |
|---|---|
| `contract.md` | Fixed JSON encodings for both endpoints, legality predicates, the source model, the candidate CLI contract and the checker interface |
| `cases.json` | Nine source fixtures (degenerate and discriminating) with stored optima where they are confirmed, plus target-side validity fixtures |
| `check.py` source oracle | Exhaustive search over all cut subsets of both trees for instances with at most 7 leaves, with component rendering, signature matching and an independent output validator |
| `check.py` target oracle | Exhaustive subset enumeration and a Z3 positional-acyclicity decision oracle, with explicit Kahn witness validation |
| `evidence/rspr_reference.py` | Independent breadth-first search over rooted subtree prune and regraft moves |

The target oracle is validated: on 25 seeded random digraphs (1–6 vertices) the
exhaustive and Z3 decisions agree, every returned set passes the explicit Kahn
check and has minimum cardinality, and the deliberate fixtures (directed
triangle, two-cycle, self-loop, acyclic input, undeclared vertex, repeated
vertex) behave as required.

## 2. Source oracle results

```
one_leaf                 |F|=1  nsols=1
two_leaves_identical     |F|=1  nsols=1
three_leaves_identical   |F|=1  nsols=1
identical_4              |F|=1  nsols=1
common_cherry_4          |F|=1  nsols=1
rSPR1_3                  |F|=3  nsols=1   (disputed, see section 4)
quartet_swap_4           |F|=3  nsols=2
quartet_swap_other_4     |F|=3  nsols=2
pseudorooted_5           |F|=3  nsols=1   (disputed, see section 4)
```

Every optimum round-trips through the source output encoding and validates: the
component vertex sets are disjoint and cover both trees, the label sets
partition `X ∪ {ρ}`, the paired component trees are isomorphic, and the union of
the component arc sets is acyclic.

## 3. The modelling decision

`contract.md` §1.3 fixes the **cut-based** model: components are the parts of a
cut after deleting unlabelled leaves and suppressing degree-2 apices, and an
agreement forest is a pair of cut sets whose components match bijectively on
label set and component tree. `contract.md` §6 records the alternative reading
in which a block's "connecting subtree" is its minimal rooted subtree; that
reading makes the all-singleton partition valid on every instance, because a
singleton's minimal connecting subtree is a single vertex, and it is therefore
degenerate. The cut-based reading is the one the cited literature uses.

## 4. Unresolved: two instances where `|F| − 1 = d_rSPR` fails

The identity `d_rSPR(T1,T2) = |F| − 1` (Theorem 2.1 of arXiv:2202.09904) is
reproduced by the oracle on `identical_4` (`0 = 0`), `common_cherry_4` (`0 = 0`)
and `quartet_swap_4` (`2 = 2`). It fails on two instances:

| Instance | oracle `|F|` | `evidence/rspr_reference.py` `d_rSPR` | `|F| − 1` |
|---|---|---|
| `T1 = ((a,b),c)`, `T2 = ((a,c),b)` | 3 | 1 | 2 |
| `T1 = (((a,b),(c,d)),e)`, `T2 = (((a,b),(d,e)),c)` | 3 | 2 | 2 |

Both values are retained and neither is settled. The reason for keeping both is
that they are computed by genuinely different methods: the oracle enumerates cut
sets and matches component trees; the reference performs breadth-first search
over rSPR moves. For `T1 = ((a,b),c)`, `T2 = ((a,c),b)` the reference is
certainly right that one rSPR move suffices (prune `c`, regraft it as a sibling
of `a`), so either the oracle's component rendering is still wrong for that
instance or the identity does not hold in the form above for three leaves. This
must be resolved before the stored optima for those two cases are trusted, so
`cases.json` leaves them `null` and the self-test prints a `PENDING` line for
each instead of asserting a value.

This is the one blocking item for Prepare. It does not affect the target side.

## 5. Diagnosis log

The defects found and fixed while building the source oracle, in order:

1. **Encodings that used a leaf's label as its node id.** Ambiguous when a label
   equals an internal node id. Fixed: node ids of leaves are ordinary strings and
   `label` is a separate field.
2. **The root label modelled as a synonym for the declared root.** This made
   every singleton block's connecting subtree a single vertex, so the
   all-singleton partition was always valid. Fixed: `ρ` is a real pendant leaf
   above the declared root, as in the references.
3. **A part's apex was not suppressed when it was an unlabelled degree-2 vertex.**
   Suppressing it in the wrong order swallowed the entire subtree below it, so
   the rendered component collapsed to a single vertex. Fixed: the apex is
   suppressed only when it is unlabelled and has fewer than two children in the
   part, and its single child is lifted.
4. **The empty-list trap.** Suppressing an apex by deleting it without lifting
   its child left the child with no parent and destroyed the subtree; lifting the
   child into the deleted vertex's parent fixes it.
5. **A non-terminating lifting rule.** An early version appended lifted children
   without removing the victim from the child lists, so the loop never reached a
   fixed point. The self-test hung; the run was killed by the harness and is
   recorded as an execution failure, not as an oracle answer.

## 6. Finite bounds declared in advance

- Source search family: all cut subsets of both trees, admitted only for
  instances with at most `SOURCE_ORACLE_LEAF_CAP = 7` leaves.
- Target oracle: exhaustive subset enumeration up to
  `EXHAUSTIVE_DFVS_VERTEX_CAP = 18` vertices; otherwise the Z3 decision oracle.
- Distinct minimum target sets passed to `--extract` per instance:
  `OPTIMAL_DFVS_ENUM_CAP = 128`.

No wall-clock, solver, subprocess or wrapper timeout appears anywhere. A harness
limit that kills a run is an execution failure, not an oracle answer.

## 7. Retained evidence

- `evidence/self-test-output.txt` and `evidence/self-test-exit.txt` — the current
  self-test run (143 checks, 0 failures, two `PENDING` lines).
- `evidence/rspr-distances.txt` — the independent rSPR distances.
- `evidence/agreement_forest_reference.py` — a second edge-cut enumeration. It
  currently reuses the oracle's rendering idea and is therefore **not** an
  independent cross-check yet; it is retained for repair, not cited as evidence.

## 8. Consequence for the campaign

A candidate reduction must not be constructed while two source optima are
disputed: the recovered forest would be checked against a source optimum this
foundation cannot yet establish for those instances. The remaining work is to
settle section 4 — either repair the rendering for the three-leaf instance or
establish that the identity used to cross-check it has a different form there —
then store the two missing optima and re-run the self-test.
