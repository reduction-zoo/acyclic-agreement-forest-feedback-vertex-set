# Contract — encodings, legality predicates and the candidate command interface

This file fixes the JSON encodings used by every artifact of this campaign. It is
derived from the fixed question in `../question.md` and from the board record
`acyclic-agreement-forest-feedback-vertex-set.json`, not from any candidate
reduction. No candidate exists yet; nothing here is a correctness claim.

Two problems are fixed:

- **Source** Π_A = Maximum Acyclic Agreement Forest (MAAF) on two rooted binary
  phylogenetic trees with an additional root label.
- **Target** Π_B = Minimum Directed Feedback Vertex Set (min-DFVS) on an explicit
  digraph.

Both endpoints are optimization endpoints. Following `research/reduction.md`,
`S_A(x)` is the set of **all globally minimum-component** acyclic agreement
forests of `x` and `S_B(G)` is the set of **all globally minimum-cardinality**
feedback vertex sets of the digraph `G`. Ties are members of these sets. Both sets
are nonempty on every legal instance (the all-singleton partition is always an
acyclic agreement forest; deleting every vertex leaves an acyclic digraph), so
no `NO-SOLUTION` output is admitted on either side.

---

## 1. Source instances

### 1.1 Encoding

```json
{
  "problem": "maaforest",
  "labels": ["a", "b"],
  "root_label": "#",
  "t1": {"root": "n1",
         "nodes": [{"id": "n1", "label": null, "children": ["a", "n2"]},
                   {"id": "n2", "label": null, "children": ["b"]}]},
  "t2": {"root": "n1",
         "nodes": [{"id": "n1", "label": null, "children": ["a", "b"]}]}
}
```

| Field | Meaning |
|---|---|
| `problem` | Literal `"maaforest"`. |
| `labels` | The leaf label set `X`; a JSON array of distinct nonempty strings, in arbitrary order. |
| `root_label` | The extra root label `ρ`, distinct from every element of `X`. |
| `t1`, `t2` | The two rooted binary phylogenetic trees on `X`. |
| `t.root` | The id of the root node of that tree. |
| `t.nodes` | A JSON array of nodes with distinct ids; a node id is any nonempty string. |

A node is written as `{"id": <string>, "label": <string|null>,
"children": [<id>, ...]}`. The `label` field carries one of the `X` labels when
the node is a leaf and is `null` for every internal node. `ρ` is **not** a node of
either tree: it is an artificial extra label used only by the partition, as the
board record states ("Include an additional root label"). The natural extension
`f : X ∪ {ρ} → V(T)` maps `ρ` to the root of `T`.

The two trees must be given on the **same node id set**, so that the union
relation of §1.3(d) is a relation on one vertex set. This is the explicit form of
the "display graph identifies corresponding leaves" convention.

### 1.2 Legal-instance constraints

Write `V(T)` for the node ids of `T`, `E(T) = {(u,v) : v ∈ children(u)}` for its
arcs, and `L(T)` for the set of labels of its leaf nodes. `T` is legal iff:

1. `t.root ∈ V(T)` and `V(T)` is nonempty.
2. Every node id is unique inside a tree, and the ranges of `label` and of
   `children` are consistent: a node with `children == []` carries a label from
   `labels`; a node with nonempty `children` carries `label == null`.
3. Every internal node has exactly two children (`|children| == 2`), and the two
   children are distinct — `T` is *binary* (degree-0 or degree-2 roots allowed,
   which is the standard reading and admits the degenerate one-leaf instance).
4. `E(T)` is a rooted tree: every node other than `t.root` occurs exactly once as
   a child, and `t.root` occurs zero times; consequently `E(T)` has no undirected
   cycle and every node is reachable from `t.root`.
5. `L(T) == labels` as sets: both trees are on the same leaf set `X`.

The instance is legal iff both trees are legal **and** `V(t1) == V(t2)` as sets
and `t1.root == t2.root`. Requiring the two roots to coincide is a normalisation,
not a restriction: it follows from constraint 4 that each tree has a unique
root, and `ρ` is mapped to that root independently in each tree, so the union
relation of §1.3(d) is unaffected by renaming. Fixing a common root id makes the
encoding canonical and lets a recovery algorithm build the union relation without
any extra convention.

### 1.3 Agreement forests

The declared root is regarded as a vertex `ρ` adjoined to it by a pendant edge,
and `ρ` belongs to the label set — the convention of Bordewich-Semple 2005 and
of van Iersel et al. 2012, as restated in arXiv:2202.09904, Section 2.

A **cut set** `S` of a tree `T` is a set of arcs of `T`. Removing `S` from `T`
splits it into connected parts. A part becomes a **component** after deleting
unlabelled leaves and suppressing non-root vertices of degree 2; the component is
rooted at the apex of its part, or at `ρ` when the part carries the root label.

An **agreement forest** of `(T1, T2)` is a pair of cut sets `(S1, S2)` whose
components pair up bijectively so that paired components have the same label set
and are isomorphic as rooted labelled trees. Its **size** is the number of
components, and `S_A(x)` is the set of forests of globally minimum size.

Of the four conditions the campaign question states:

- **(a) partition.** The component label sets partition `X ∪ {ρ}`, because the
  parts of a cut partition the vertex set and each label lies in exactly one part.
- **(b) agreement.** Requiring the paired component trees to be isomorphic is
  exactly the condition that the restrictions to each block agree.
- **(c) disjointness.** The component vertex sets are disjoint within each tree
  and cover it: they are the parts of a cut.
- **(d) acyclicity.** `E(F)` is the union of the component arc sets of both
  trees, with arcs oriented child → parent; it must be acyclic. Each component's
  arc set is a rooted tree, so cycles can only come from mixing the two trees.

Conditions (a) and (c) are therefore consequences of the cut construction rather
than separate checks; the validator recomputes them from the source instance for
every output it accepts. Section 6 records the modelling question this leaves
open.

### 1.4 Source outputs

```json
{"problem": "maaforest",
 "cuts": {"t1": [["a", "n3"]], "t2": [["a", "n3"]]},
 "components": [
   {"labels": ["a"],
    "t1_vertices": ["a"], "t1_edges": [],
    "t2_vertices": ["a"], "t2_edges": []},
   {"labels": ["b", "c", "d", "ρ"],
    "t1_vertices": ["b", "c", "d", "n6", "n7", "ρ", "__above__n7"],
    "t1_edges": [["b", "n3"], ["c", "n6"], ["d", "n6"], ["n6", "n7"],
                 ["n7", "__above__n7"], ["ρ", "__above__n7"]],
    "t2_vertices": ["b", "c", "d", "n3", "n6", "n7", "ρ", "__above__n7"],
    "t2_edges": [["b", "n6"], ["c", "n3"], ["d", "n6"], ["n3", "n7"],
                 ["n6", "n7"], ["n7", "__above__n7"], ["ρ", "__above__n7"]]}
 ],
 "num_components": 2}
```

A source output lists the two cut sets and, for every component, its label set
and its vertex set and induced arc set in each tree. It is **valid** iff

1. the decoded label sets partition `X ∪ {ρ}` and are pairwise distinct,
2. in each tree the component vertex sets are pairwise disjoint and cover every
   vertex of the tree, each vertex set is a connected part of that tree, and the
   listed arcs are exactly the arcs induced on it,
3. for each component the two rendered component trees are isomorphic as rooted
   labelled trees, and
4. the union of all listed arcs is acyclic.

`validate_source_output` in `check.py` performs exactly these checks against the
source instance and never trusts a value carried by the output.

### 1.5 Independent source oracle

**Status: pending.** `check.py` contains an edge-cut enumerator
(`source_oracle`) that searches the finite family of all cut subsets of both
trees and matches signatures, but its component rendering is not yet correct and
its values are therefore not used as ground truth: `cases.json` stores `null`
for every source optimum and the self-test reports them as pending. The finite
family and the intended rendering are declared; the implementation and its
cross-check against `evidence/rspr_reference.py` are the blocking work recorded
in `preparation.md`. This is a missing capability, reported as pending, not a
successful check.

Reference findings that the repaired oracle must reproduce (independently
computed, see `preparation.md` section 5):

| Instance | value |
|---|---|
| `T1 = T2`, any `n ≥ 1` | the all-one-block forest is valid; `\|F\| = 1` |
| one leaf | `\|F\| = 1` |
| `T1 = ((a,b),(c,d))`, `T2 = ((a,c),(b,d))` | `d_rSPR = 2`, so `\|F\| = 3` |
| `T1 = ((a,b),c)`, `T2 = ((a,c),b)` | `d_rSPR = 1`, so `\|F\| = 2` |

## 2. Target instances

### 2.1 Encoding

```json
{"problem": "dfvs",
 "vertices": ["v0", "v1", "v2"],
 "arcs": [["v0", "v1"], ["v1", "v2"], ["v2", "v0"]]}
```

`vertices` is a list of distinct nonempty strings; `arcs` is a list of ordered
pairs of members of `vertices`; self-loops are permitted and are legal. The
instance is legal iff ids are distinct and every arc endpoint is listed in
`vertices`. The empty vertex set is legal and its minimum feedback vertex set
is the empty set.

### 2.2 Target outputs

```json
{"problem": "dfvs", "feedback_vertex_set": ["v1"]}
```

A target output is **valid** iff every element is a listed vertex, no element
repeats, and deleting the set from the digraph leaves an acyclic digraph. The
last property is checked by an explicit Kahn topological sort of the remaining
digraph, independent of any solver encoding. `S_B(G)` is the set of valid target
outputs of cardinality `OPT_B(G) = min{|S| : S valid}`.

### 2.3 Independent target oracle

`check.py` decides `OPT_B(G)` and enumerates `S_B(G)` on a finite domain by an
oracle that never reads a candidate:

1. **Exhaustive subset enumeration.** For `|V| ≤ 12`, all subsets are tested in
   increasing cardinality; the first cardinality admitting a valid set is
   `OPT_B`, and every valid set of that cardinality is a member of `S_B`.
2. **SMT decision oracle (Z3).** For larger graphs, `OPT_B` is found by
   increasing `k` and asking Z3 for a set of at most `k` vertices whose deletion
   leaves an acyclic digraph, using a positional acyclicity encoding derived
   directly from the definition: `level[v] ∈ {0..n−1}` for every vertex, and for
   every arc `(u,v)`, `u ∈ S ∨ level[u] < level[v]`. Feasibility of that system
   is equivalent to acyclicity of the remainder (a DAG has a topological order;
   conversely, levels induce one).
3. **Independent CP-SAT cross-check (OR-Tools).** The same decision problem is
   encoded a second time with a *different* propagation-based acyclicity
   encoding (per-vertex reachability ranks are replaced by "keep" variables and
   transitive-closure ordering constraints), so that a shared encoding bug is
   unlikely to survive both backends.
4. **Witness validation.** Every set returned by any oracle is validated by the
   explicit Kahn test of §2.2; a set is accepted only after that check passes.
   A negative answer (`OPT_B > k`) is accepted only from an infeasibility result
   of the decision oracle; `unknown` is never read as a decision.

`OPT_B` is additionally bounded by `|V| − 1` whenever `|V| ≥ 1`, which is
attained by deleting every vertex but one.

---

## 3. Candidate command contract

`algorithm.py` implements both maps of the rule.

**Forward map F.**

```
python3 algorithm.py            < source_instance.json > target_instance.json
```

Reads exactly one legal source instance as JSON on stdin and writes exactly one
legal target instance as JSON on stdout. Diagnostics go to stderr. Any execution
error exits with a nonzero status. F is deterministic: the same stdin produces
byte-identical stdout, and it uses no randomness, no solver and no LLM.

**Recovery map G.**

```
python3 algorithm.py --extract  < {"source": ..., "target_solution": ...} > source_output.json
```

Reads a JSON object with keys `source` (forward input encoding) and
`target_solution` (target output encoding) and writes one valid source output as
JSON. G may reconstruct any metadata it needs from `source`; it must not rely on
state retained by an earlier forward subprocess. G is deterministic and calls no
solver, no randomness and no LLM.

**Obligation to be proven later.** For every legal `x` and every
`y ∈ S_B(F(x))`, `G(x, y) ∈ S_A(x)`. In particular the recovered forest must
have the globally minimum component count `OPT_A(x)`, ties included. Feasibility
alone does not satisfy the contract. No obligation for nonoptimal `y` is
implied.

**Bounds to be proven later.** F runs in time polynomial in `|x|` and outputs
`O(poly(|x|))` bits; G runs in time polynomial in `|x| + |y|` and outputs
`O(poly(|x| + |y|))` bits.

---

## 4. Checker interface

`check.py` provides

```
python3 check.py --self-test
python3 check.py --candidate PATH
```

- `--self-test` runs hand-verifiable cases, stored ground truth, oracle
  cross-validation on a finite enumerated family, and deliberately incorrect
  outputs and recovery fixtures. It must detect wrong answers, suboptimal
  solutions and malformed outputs, and exits nonzero on any mismatch.
- `--candidate PATH` runs F on every injected source instance, solves the
  produced target instance independently, hands each obtained valid target
  output (including every enumerated minimum set and several distinct optima
  found by a deterministic vertex-order search) to `--extract`, and checks the
  recovered output against `S_A(x)` — feasibility *and* the independently
  established source optimum. It exits nonzero on mismatch, invalid output or
  execution failure.

All bounds are finite and declared in `preparation.md`. No wall-clock, solver,
subprocess or wrapper timeout is used anywhere.

---

## 5. The cited worked example

For `T1 = ((a,b),(c,d))`, `T2 = ((a,c),(b,d))` the cited upstream issue states
that `F = {{a},{b},{c},{d}}` is "the only acyclic agreement forest achieving"
its claimed optimum, and the review comment on the same issue asserts the
hybridisation number is 1 with `F = {{ρ,a,b},{c,d}}`. Neither is consistent with
the definitions:

- `{{a},{b},{c},{d}}` is not a partition of `X ∪ {ρ}`; the root label is
  unplaced.
- The rooted-SPR distance of the pair is **2**, computed independently by breadth
  first search over rSPR moves in `evidence/rspr_reference.py`
  (`((a,b),(c,d)) → (((a,b),c),d) → ((a,c),(b,d))`). The 2-block forest
  `{{ρ,a,b},{c,d}}` of the review comment would give distance 1, so it cannot be
  a maximum agreement forest.

`evidence/agreement_forest_reference.py` is a second, independent edge-cut
enumeration written against the same definition. It is currently being repaired
together with the source oracle; its values are not used as ground truth.
Section 6 records the open modelling question.

## 6. Open modelling question (recorded, not resolved)

The campaign question phrases the source conditions as: the restrictions to each
leaf block must agree in both trees, "their connecting subtrees must be
vertex-disjoint within each tree", and the union of the two component-ancestry
relations must be acyclic, with "fewest components" as the objective. Reading
"connecting subtree" as the minimal rooted subtree that connects a block's
members is not compatible with the standard rSPR agreement-forest model on
every instance: for the quartet swap `T1 = ((a,b),(c,d))`,
`T2 = ((a,c),(b,d))`, every partition into fewer than five blocks either has
overlapping minimal connecting subtrees in one of the two trees or has blocks
whose restrictions disagree. The standard model instead derives the components
from cuts, and under it the quartet swap has a 3-block forest.

Which reading the fixed question intends therefore changes the source optimum on
small instances. This file fixes the **cut-based** reading, because it is the
model of the cited literature and reproduces the `d_rSPR = |F| − 1` identity,
and `preparation.md` records the discrepancy and the evidence. If the intended
reading is the minimal-subtree one, this is a different source problem and the
question must be amended before a candidate is constructed; it is not resolved
here.
