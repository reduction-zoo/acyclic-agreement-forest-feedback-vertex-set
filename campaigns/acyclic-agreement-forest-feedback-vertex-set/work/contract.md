# Executable contract

The fixed mathematical question in `../question.md` is unchanged. All encodings
are explicit JSON. Node identifiers are local to each tree; their spelling,
ordering, and overlap between trees have no mathematical meaning.

## Source instance

`{"problem":"maaforest","labels":["a","b"],"root_label":"ρ",
"t1":{"root":"r","nodes":[{"id":"r","children":["a","b"],"label":null},
{"id":"a","children":[],"label":"a"},{"id":"b","children":[],"label":"b"}]},
"t2": ...}`

The leaf-label list is nonempty and consists of distinct nonempty strings.
The extra root label is a nonempty string outside that list. Each tree is finite,
connected, rooted and binary, with each internal vertex having two distinct
children and no label. Leaves are labelled bijectively by `labels`. Identifiers
are distinct nonempty strings within each tree. The roots and node-id sets of
the two trees need not agree. The single-leaf tree is admitted.

Adjoin a fresh root above the original root, with the original root and a fresh
leaf carrying `root_label` as its two children. Synthetic vertices are fresh
internal indices, never user-chosen strings. For a nonempty label block B,
T(B) is the minimal connecting subtree rooted at the LCA of B, and T|B is
obtained by suppressing unary vertices. The source output is a partition of all
leaf labels including the added label into nonempty blocks such that:

1. For each block B, the two rooted labelled restrictions T1|B and T2|B agree.
2. The subtrees T_i(B) are pairwise vertex-disjoint within each input tree.
3. The graph on blocks, with B -> C whenever the root of T_i(B) is a strict
   ancestor of the root of T_i(C) in either original augmented tree, is acyclic.

All such partitions with the minimum number of blocks are valid source outputs.
Unlabelled vertices outside the connecting subtrees need not be covered.

## Source output

`{"problem":"maaforest","components":[["a","b","ρ"]],"num_components":1}`

`components` is a nonempty list of nonempty lists of labels. Block/label order
has no meaning. `num_components` is an integer equal to the list length; Boolean
values are not integers in this interface. Duplicates and missing labels are
invalid. No cuts, tree-node assignments, or redundant edge data are required.

## Target instance and output

`{"problem":"dfvs","vertices":["u","v"],"arcs":[["u","v"],["v","u"]]}`

Vertex ids are distinct nonempty strings; every arc endpoint is a declared
vertex. Empty digraphs, self-loops and repeated arcs are admitted; repeated arcs
have set semantics. A target output is
`{"problem":"dfvs","feedback_vertex_set":["u"]}`. It lists distinct declared
vertices and must have globally minimum cardinality among sets whose deletion
leaves a DAG. The empty set is optimal exactly for acyclic inputs.
Neither endpoint admits NO-SOLUTION. Solver unknown or execution failure is an
error, never a mathematical answer.

## Candidate command interface

`python algorithm.py` reads one source JSON value from stdin and emits one
legal target JSON value to stdout. `python algorithm.py --extract` reads
`{"source": SOURCE, "target_solution": TARGET_OUTPUT}` and emits one optimal
source output. Each invocation is a fresh process; metadata must be reconstructible
from the source. Diagnostics use stderr and errors have nonzero exit status.
Neither map may call a solver or enumerate an exponential family. Both maps
must be deterministic and polynomial in their specified input bit lengths.

## Prepared tests

`uv run --locked python campaigns/acyclic-agreement-forest-feedback-vertex-set/work/check.py --self-test`
checks the independent finite oracles and validators.
`--candidate PATH` runs F on every stored case, independently proves the actual
target optimum, passes up to 128 distinct minimum target sets through G, and
checks source feasibility and optimality against independently recomputed ground
truth. It reports whether target-optimum enumeration is complete for each case.
No wall-clock limits are used. Any mismatch or execution failure exits nonzero.
Finite checks cannot replace the universally quantified proof.
