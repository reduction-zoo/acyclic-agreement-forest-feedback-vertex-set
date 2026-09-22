# Prepare — definition-based restart, 2026-09-22

The user requested a restart from Prepare. The fixed mathematical question is
unchanged. This foundation replaces the source semantics implemented at a056e65;
previous candidate-correctness evidence is withdrawn, not reused.

## Definition audit and retained counterexample

The fixed question defines a graph **on forest components**, with an arc when
one component root is an ancestor of another in either input tree. The previous
checker instead took the union of component **tree edges on shared node ids**.
It also required the input trees to share internal ids and their root id.
These are different predicates. Two identical labelled caterpillar trees, with
only two internal ids interchanged in the second tree, have source optimum 1;
the old checker reports 2. See
[evidence/prepare-restart/internal-renaming.json](evidence/prepare-restart/internal-renaming.json)
and the executable [reproducer](evidence/prepare-restart/reproduce_old.py).

Primary-source corroboration was retrieved with the web tool on 2026-09-22:
Linz, Semple and Stadler, *Analyzing and reconstructing reticulation networks
under timing constraints*, Section 4.1, printed page 14, explicitly defines
vertex-disjoint connecting subtrees and the directed graph on components:
<https://www.math.canterbury.ac.nz/~c.semple/papers/LSS10.pdf>.
A PMC fetch was blocked by a browser challenge; the author-hosted PDF was read.
This lookup verifies the fixed definition, not a new construction round.

`contract.md` now encodes outputs directly as label partitions. Cut-pair
representations are not counted as distinct forest outputs. The old nine
source optima happen to agree with the corrected values; that coincidence did
not detect the modelling error. Their original inputs and previous values are
retained in `evidence/prepare-restart/legacy-source-cases.json`.

## Declared finite coverage

| Source family | Instances |
|---|---:|
| All ordered pairs of rooted binary labelled trees on 1 leaf | 1 |
| Same, 2 leaves | 1 |
| Same, 3 leaves | 9 |
| Same, 4 leaves | 225 |
| Seeded distinct ordered pairs on 5 leaves | 32 |
| Seeded distinct ordered pairs on 6 leaves | 32 |
| Seeded distinct ordered pairs on 7 leaves | 16 |
| Previous named inputs, recomputed | 9 |
| Internal-id permutation regression | 1 |
| Agreement forest with an ancestry 2-cycle | 1 |
| Total stored input records | 327 |

Counts are records; regressions deliberately overlap the exhaustive topological
family. `prepare.py` constructs each unordered-child tree once by placing the
smallest label on the left of every recursive bipartition. There are 1, 1, 3,
and 15 such trees through four leaves. Both orders of each tree pair are tested.
The larger-family sampling uses Python `random.Random(20260922)` without
replacement among ordered pairs. The committed JSON fixes the actual inputs.

The reference enumerates **all** label partitions for every source input,
including the root label. The self-test compares feasibility on 113,194
partitions and compares the complete sets of 956 minimum partitions across
327 records. Every minimum partition is also checked after independent node
renaming, node-list reversal and child-order reversal. These metamorphic checks
are additional output checks, not additional stored source instances.

Target coverage: all 531 digraphs on 0–3 vertices, including self-loops, plus
20 seeded graphs for each size 4–8 (100 more). All 766 minimum target sets in
these 631 records are cross-checked. Empty input, empty optimal deletion,
self-loops, multiple optima and capped-enumeration reporting are exercised.

A hand-constructed forest `{a,b}, {c,d}, {ρ}` agrees and has disjoint connecting
subtrees in the two opposite caterpillars, but its component ancestry graph has
a 2-cycle. It must be rejected. Hand-known singleton/identical-tree optima,
three-leaf optimum 2 with three minimum partitions, malformed outputs,
suboptimal singleton partitions, and malformed trees are asserted explicitly.
Controlled subprocess fixtures exercise the actual candidate harness, including
a decoder correct on one target optimum but suboptimal on the other, non-JSON
output, and nonzero process exit.

## Independent oracles and correspondence

`check.py` uses Z3 4.15.4, locked as `z3-solver==4.15.4.0`, with Python 3.12.11.
The source oracle enumerates nonempty label blocks only inside the finite test
oracle (maximum 7 original leaves). It computes each block's restrictions and
original connecting-subtree vertices. A Boolean selects each agreeing block.
Exactly-one constraints cover each label; pairwise conflicts forbid intersecting
connecting subtrees. If selected block roots are ancestral in either tree,
integer ranks must increase. Thus a model is exactly an acyclic agreement
forest: forward, a forest admits a topological ranking; backward, strict rank
increase forbids every component cycle. Increasing exact cardinalities proves
the first SAT cardinality globally minimum. Blocking selected block sets
enumerates all optima until UNSAT. Returned partitions are checked directly.

`source_reference.py` imports no project implementation. It enumerates set
partitions, recursively prunes nested tree expressions, represents original
vertices by root-to-node bit paths, and computes transitive closure of the
component ancestry relation. This differs from the SMT oracle's vertex-index,
LCA, conflict and ranking implementation. No source oracle imports or reads a
candidate. Enumeration is appropriate as a small independent cross-check;
it is not proposed as a polynomial-time reduction.

For a bidirected graph, the current target oracle uses the exact equivalence
between DFVS and vertex cover: every undirected edge is a directed two-cycle.
It splits connected components, packs disjoint cliques from actual adjacency,
and obtains a lower bound by summing their cover bounds. A packed loop vertex
is forced; a loop-free clique contributes its size minus one, plus one exactly
when fully selected. Vertices outside the packing contribute their deletion
Booleans. Increasing exact surplus cardinalities therefore proves the first
SAT cover globally minimum. All witnesses receive a separate DAG validity
check. No candidate import, source optimum or threshold metadata is used.
NetworkX 3.6.1 computes graph components and cliques; Z3 solves the constraints.
The revised oracle passes the same 631-graph exhaustive comparison; see
`../rounds/006/oracle-surplus.txt`.

For graphs that are not bidirected, the target SMT oracle uses one deletion Boolean and one integer rank per vertex.
Each arc u->v requires `delete(u) or delete(v) or rank(u)<rank(v)`. This is
satisfiable exactly when the remaining digraph is acyclic. Binary search over
cardinality with conclusive SAT/UNSAT proves the optimum, then blocking deletion
sets enumerates distinct minimum witnesses. Witness validity uses a separate
vertex-removal DAG check. The target reference enumerates all deletion subsets
and uses Floyd-Warshall closure, including diagonal cycles. Unknown is always
an exception, never exhaustion or an optimum. Integer arithmetic is exact.

## Reproduction and evidence

From repository root:

```sh
uv sync --locked
uv run --locked python campaigns/acyclic-agreement-forest-feedback-vertex-set/work/prepare.py --generate
uv run --locked python campaigns/acyclic-agreement-forest-feedback-vertex-set/work/check.py --self-test
uv run --locked python campaigns/acyclic-agreement-forest-feedback-vertex-set/work/evidence/prepare-restart/reproduce_old.py
```

Retained outputs: `evidence/prepare-restart/generate.txt`, `self-test.txt`, and
`audit-output.txt`. The previous logs remain historical evidence of the old
predicate, not checks of the fixed problem. No wall-clock or solver timeout is
used. Candidate checks execute every stored input and report distinct target
outputs and enumeration completeness separately; they cannot be replaced by
source-only or formula-only checks.

## Limits

Finite tests do not establish a general theorem. Larger source pairs are sampled,
not exhaustive. Candidate target graphs may exceed the target oracle's practical
capacity; that would leave verification pending, not permit shrinking away the
prepared suite. Candidate checks enumerate at most 128 target optima per input
and explicitly report truncation. This Prepare stage establishes no valid
candidate and no independent review of a candidate.
