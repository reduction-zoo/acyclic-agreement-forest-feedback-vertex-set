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

## 4. Divergence from the classic rSPR identity, and why

The oracle requires the two cut sets of a forest to have the **same size**, so
that their component counts agree (`|S1| + 1 = |S2| + 1 = |F|`). The classic
identity `d_rSPR(T1,T2) = |F| − 1` (Theorem 2.1 of arXiv:2202.09904) does not
impose that: its agreement forest is built from a hybridisation network and may
cut fewer edges in one tree than in the other. The two notions therefore
coincide only when the optimal forest happens to be symmetric.

| Instance | oracle `|F|` | `d_rSPR` | `|F| − 1` | agrees? |
|---|---|---|---|
| `T1 = T2 = ((a,b),(c,d))` | 1 | 0 | 0 | yes |
| `T1 = ((a,b),(c,d))`, `T2 = ((a,b),(d,c))` | 1 | 0 | 0 | yes |
| `T1 = ((a,b),(c,d))`, `T2 = ((a,c),(b,d))` | 3 | 2 | 2 | yes |
| `T1 = ((a,b),(c,d))`, `T2 = ((a,d),(b,c))` | 3 | 2 | 2 | yes |
| `T1 = ((a,b),c)`, `T2 = ((a,c),b)` | 3 | 1 | 2 | **no** |
| five-leaf instance `(((a,b),(c,d)),e)` vs `(((a,b),(d,e)),c)` | 3 | 2 | 2 | yes |

The one disagreement is explained and checked directly. For
`T1 = ((a,b),c)`, `T2 = ((a,c),b)` the rSPR search is right that one move
suffices: prune `c` in `T1` and regraft it as a sibling of `a`, giving
`((a,c),b)`. An exhaustive search over cut pairs shows that no pair of cut sets
of **equal** size yields matching component signatures: cutting one edge in each
tree never produces the same label partition, and cutting two edges gives three
components in each tree. The oracle's `|F| = 3` is therefore the correct minimum
for the symmetric reading this contract fixes, and the rSPR value 1 belongs to
the asymmetric reading. Nothing is wrong with either computation; the two
readings are different problems.

The five-leaf instance agrees (`3 − 1 = 2`), so its optimum is stored.

The three-leaf divergence is recorded, not resolved. `cases.json` stores `null`
for that case and the self-test prints a `PENDING` line. If the campaign's fixed
question is read as the classic asymmetric rSPR agreement forest, the source
model in `contract.md` §1.3 must be replaced; that is a change to the fixed
objective and needs the question to be amended first.

## 5. Root cause of the remaining discrepancy

The oracle renders a component from **the part of the cut** — the connected piece
of `T - S` — while the standard definition renders it from **the block's minimal
subtree**, `T[B]` with degree-2 vertices suppressed. The two differ on the
containing shape, and the difference is the whole of the three-leaf divergence.

For `T1 = ((a,b),c)`, `T2 = ((a,c),b)`, cut the edge `(a,n3)` in both trees. The
label partition is `{a} | {b,c,ρ}` in both, so the blocks match. But the oracle
renders the part `{b,c,n3,n5,ρ}` inside each tree, and the part retains a
tree-specific branching vertex:

| tree | part rendered by the oracle | key |
|---|---|---|
| `T1 = ((a,b),c)` | `{b,c,n3,n5,ρ}` with `n3={a,b}` cut down to `b` | `(((b),c),ρ)` |
| `T2 = ((a,c),b)` | `{b,c,n3,n5,ρ}` with `n3={a,c}` cut down to `b` | `(((c),b),ρ)` |

The keys differ, so the oracle rejects the two-block forest and reports
`|F| = 3`. The standard rule instead takes `T[{b,c,ρ}]`, whose shape is the
cherry `(b,c)` in **both** trees, so the blocks agree and `|F| = 2`, matching
`d_rSPR = 1` by the identity. The same defect is why the earlier attempt reported
`|F| = 4` and `|F| = 5` on instances whose true optima are 3.

So the fix is local and precisely stated: in `check.py`, a component's rendered
tree and key must come from `T[B]` (minimal subtree of the block, degree-2
vertices suppressed, unlabelled leaves deleted, rooted at `ρ` when the block
carries it and at the apex otherwise), not from `cut_components`. The vertex
sets, the signature matching and the validator's data model stay as they are.

Attempts at this fix in this session are recorded below; the working tree keeps
the version whose self-test is green, so nothing is half-edited.

## 5b. Diagnosis log## 6. Finite bounds declared in advance

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
