# Preparation — testing foundation status

Stage: **Prepare** (2026-09-21). This record states the current foundation
honestly. Preparation establishes no reduction-correctness claim.

Commands:

```sh
cd campaigns/acyclic-agreement-forest-feedback-vertex-set/work
python3 check.py --self-test
python3 evidence/agreement_forest_reference.py
python3 evidence/rspr_reference.py
```

The foundation uses only the standard library plus the environment's Z3 module;
no Python project is needed yet.

## 1. What is complete

| Artifact | State |
|---|---|
| `contract.md` | Fixed JSON encodings for both endpoints, legality predicates, the source model, the candidate CLI contract and the checker interface |
| `cases.json` | Nine source fixtures with stored optima and minimum cut-pair counts, plus target-side validity fixtures |
| `check.py` source oracle | Exhaustive search over all cut subsets of both trees for instances with at most 7 leaves, block-restriction signatures, explicit acyclicity filtering and an output validator |
| `check.py` target oracle | Exhaustive subset enumeration and a Z3 positional-acyclicity decision oracle, with explicit Kahn witness validation |
| `evidence/agreement_forest_reference.py` | Standalone JSON-based cut enumeration with an independent augmented-tree representation and restriction renderer |
| `evidence/rspr_reference.py` | Independent breadth-first search over rooted subtree prune and regraft moves |

The target oracle is validated on 30 seeded random digraphs with 1–6 vertices:
the exhaustive and Z3 decisions agree, every returned set passes the explicit
Kahn check and has minimum cardinality, and the deliberate validity fixtures
behave as required.

## 2. Source oracle results

```
one_leaf                 |F|=1  n_min_cut_pairs=1
two_leaves_identical     |F|=1  n_min_cut_pairs=1
three_leaves_identical   |F|=1  n_min_cut_pairs=1
identical_4              |F|=1  n_min_cut_pairs=1
common_cherry_4          |F|=1  n_min_cut_pairs=1
rSPR1_3                  |F|=2  n_min_cut_pairs=3
quartet_swap_4           |F|=3  n_min_cut_pairs=14
quartet_swap_other_4     |F|=3  n_min_cut_pairs=14
pseudorooted_5          |F|=3  n_min_cut_pairs=10
```

The counts are cut-pair representations accepted by the fixed output encoding;
the objective is the component count. Every optimum round-trips through the
source output encoding and validates: component vertex sets are disjoint and
cover both trees, label sets partition `X ∪ {ρ}`, paired component trees agree,
and the union of component arc sets is acyclic.

## 3. The modelling decision

`contract.md` §1.3 fixes the cut-based model. A cut partitions each augmented
tree into labelled parts. For a part with label block `B`, agreement compares the
rooted labelled restriction on the minimal subtree `T[B]`, with unlabelled leaves
deleted and unlabelled degree-2 vertices suppressed. The output retains each
cut part's vertex set and component arcs so the validator can check coverage,
disjointness and the acyclicity relation. This is the model used by the cited
agreement-forest literature and by the repaired oracle.

## 4. Repaired discrepancy

The earlier source oracle rendered a component's key from the entire cut part.
For `T1 = ((a,b),c)`, `T2 = ((a,c),b)`, cutting `(a,n3)` in both trees gives
the block `{b,c,ρ}`. The two cut parts retain different containing shapes if
rendered directly, although their restrictions to `T[{b,c,ρ}]` are the same
cherry. That implementation defect reported `|F|=3` instead of `|F|=2`.

The repaired implementation derives the key from the block restriction and
filters matched cut pairs through the explicit acyclicity predicate. The
independent reference reproduces every stored value, including the formerly
pending cases:

| Instance | source oracle | independent reference | rSPR distance |
|---|---:|---:|---:|
| `T1 = T2 = ((a,b),(c,d))` | 1 | 1 | 0 |
| quartet swap | 3 | 3 | 2 |
| mirror quartet swap | 3 | 3 | 2 |
| `T1 = ((a,b),c)`, `T2 = ((a,c),b)` | 2 | 2 | 1 |
| five-leaf fixture | 3 | 3 | 2 |

The rSPR values are a cross-check only; the source oracle's ground truth is the
fixed cut-based, acyclic-agreement-forest definition.

## 5. Finite bounds

- Source search family: all cut subsets of both trees, admitted only for
  instances with at most `SOURCE_ORACLE_LEAF_CAP = 7` leaves.
- Target oracle: exhaustive subset enumeration up to
  `EXHAUSTIVE_DFVS_VERTEX_CAP = 18` vertices; otherwise the Z3 decision oracle.
- Distinct minimum target sets passed to `--extract` per instance:
  `OPTIMAL_DFVS_ENUM_CAP = 128`.

No wall-clock, solver, subprocess or wrapper timeout appears anywhere. A harness
limit that kills a run is an execution failure, not an oracle answer.

## 6. Retained evidence

- `evidence/self-test-output.txt` and `evidence/self-test-exit.txt` — the current
  self-test run.
- `evidence/agreement-forest-reference-output.txt` — independent source-oracle
  values and minimum cut-pair counts.
- `evidence/rspr-distances.txt` — independent rSPR distances.
- `evidence/agreement_forest_reference.py` — the executable independent source
  cross-check.

## 7. Consequence for the campaign

Preparation is complete for the declared finite domain: both endpoints have
independent executable checks, the disputed source fixtures are resolved, and
incorrect, suboptimal and malformed outputs are exercised. The next action is to
commit this testing foundation and begin Propose; no research round has been
consumed.
