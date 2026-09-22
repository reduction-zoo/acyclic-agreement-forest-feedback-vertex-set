# Rank thresholds and unit-gap covers: MAAF to minimum DFVS

Let m=|X|+1 count all labels, including the added root label. The source and
output encodings are fixed in `contract.md`. This proof describes `algorithm.py`.
A solver is used only by the test harness, never by F or G.

## Rank characterization of acyclic agreement forests

Fix a threshold k in {1,...,m}. Give every augmented tree vertex an integer rank
in {0,...,k-1}; copies of the same labelled leaf share one rank variable. Impose:

1. For every parent-child edge, rank(parent) <= rank(child).
2. For every pair of leaves a,b in each tree, if rank(a)=rank(b), their LCA
   has that same rank.
3. If the two input trees disagree on a rooted triple a,b,c, its three leaf
   ranks are not all equal.

**Rank assignment implies a forest.** Partition labels by equal ranks. For a
block B containing at least two leaves, some pair a,b in B has LCA equal to the
root of its connecting subtree: take leaves in the two child branches of that
root. Condition 2 gives this root rank r_B. Condition 1 forces every vertex on
a root-to-B-leaf path to have rank r_B. A singleton's connecting subtree is
just its labelled leaf. Thus every connecting subtree is monochromatic, and
different blocks cannot intersect because they have different ranks.

Condition 3 gives agreement of restrictions. Here is the rooted-triples fact
used in this inference: a proper label subset C with at least two elements is
a cluster of a rooted binary tree iff every pair x,y in C and z outside C
induces xy|z. One direction follows from the cluster's root. Conversely, if C
is not a cluster, its LCA has an extra descendant z outside C, while C meets
both of its child branches. Choose x,y in those two branches; the triple is
not xy|z, a contradiction. Hence triples determine the cluster hierarchy and
therefore the rooted labelled tree. Restrictions to one or two labels are
unique. Restricting to a block preserves its constituent triples.

If a component root B is an ancestor of a distinct component root C in either
tree, Condition 1 gives r_B <= r_C, and distinct blocks have unequal ranks.
Every component ancestry arc thus strictly increases rank. Its union is
acyclic. The number of blocks is at most k.

**Forest implies a rank assignment.** Take any acyclic agreement forest with
q<=k blocks, and number its blocks 0,...,q-1 in a topological order of their
union ancestry graph. Give a leaf its block's number. For every tree vertex v,
define its rank to be the minimum rank among its descendant labelled leaves.
This is nondecreasing from parent to child and lies in {0,...,k-1}.

If v belongs to the connecting subtree of block B, some leaf of B is below v.
Any leaf c below v from a different block C must have its component root below
the root of B: both roots are ancestors of c; if the root of C were at or
above B's root, the connecting path to c would intersect B at v. Disjointness
excludes this. Hence r_C>r_B, and the minimum descendant rank at v is exactly
r_B. The entire connecting subtree of B therefore has rank r_B. Equal-rank
leaves belong to B and their LCA belongs to its connecting subtree, establishing
Condition 2. Agreement of each block's restrictions establishes Condition 3.

This proves the equivalence for every k, using the component ancestry graph,
with no identification of internal vertices across the two trees.

## Polynomial CNF implementing ranks

Use w=ceil(log_2 k) bits per rank, most significant bit first (w=0 when k=1).
Leaf rank bits are allocated first and shared by both trees. Other vertex ranks
use fresh bit variables. Bound each leaf rank by k-1. Internal ranks need no
separate bound: every vertex has a descendant leaf, and the parent inequalities
already bound it above by that leaf's rank. Bit vectors are nonnegative.

The implementation encodes a<=b by comparing bits from least significant to
most significant. Starting with tail=true, replace tail by
majority(NOT a_bit, b_bit, tail). Equal current bits preserve the lower-bit
comparison; a current 0/1 makes it true, and 1/0 makes it false. This proves the
comparator by induction. The majority gate has the six usual clauses: every
true input pair forces its output, and a true output requires one true input
in each pair. Bit equality uses its four truth-table clauses; vector equality
is an AND of bit equalities. OR gates use both implication directions; AND is
the dual. Constant and repeated-literal simplifications are exact identities.
Literal 1 is fixed true. Empty clauses are represented by the false unit -1.

For every original tree edge assert its comparison. For each leaf pair with
equality flag E_ab, assert E_ab -> (rank(a)<=rank(LCA(a,b))). The reverse
inequality already follows from the tree edges, so this is Condition 2 exactly.
Shared (LCA,leaf) comparisons are emitted once within each tree. For a disagreeing
triple assert NOT E_ab OR NOT E_ac. All gates are equivalences; no implicit
existential extension can falsify the asserted comparisons. Call the resulting
formula Phi_k. The characterization proves:

Phi_k is satisfiable iff the input admits an acyclic agreement forest with at
most k components. Every satisfying assignment decodes to one, and every such
forest extends to a satisfying assignment. Phi_m is always satisfiable.

## Certified pruning and unit-gap formulas

First compare the full rooted labelled restrictions. If they agree, the optimum
is one; F emits an empty digraph and G emits the single full-label block. This
is invariant under node renaming. Otherwise the optimum is at least two.

Starting from singleton blocks, repeatedly try every pair of current blocks in
deterministic order, accept the first merge whose resulting partition passes the
direct forest validator, and restart. Stop when no pair can merge. At most m-1
merges occur and at most O(m^3) proposals are checked. Every accepted partition
is a feasible acyclic agreement forest, so its final size U satisfies OPT<=U.
Initially any two singleton labels can merge: their two-leaf restrictions agree,
the connecting path meets no other labelled leaf, and all other components are
singletons, so there is no ancestry cycle. Hence U<=m-1. No claim that this
greedy procedure finds an optimum is needed or made. Emit only thresholds
k=2,...,U. This is a polynomial feasibility heuristic inside F, not an oracle.

For k<U, transform Phi_k by introducing a fresh selector z, replacing every
clause C by C OR z, and adding the unit clause NOT z. Call this Psi_k. The unit
forces z=false, so satisfiability and decoded source ranks are unchanged. For
k=U use Phi_U unchanged, since the greedy forest witnesses its satisfiability.
The rank-bit variable numbers do not change when the selector is appended.

## A CNF formula becomes a bidirected cover graph

For every Boolean variable q create endpoints q_0,q_1 joined by an undirected
edge. For every clause with d literal occurrences create a clique on d private
vertices. Join each occurrence vertex to q_b where b is the truth value making
that occurrence's literal true. Unit clauses are one-vertex cliques and still
have their occurrence edge. There are no empty clauses.

Every vertex cover has at least one endpoint per variable and at least d-1
vertices per clause clique. Write L = V + sum_C(|C|-1). A satisfying assignment
gives a cover of size L: select the true-value endpoint for each variable and
omit one true-literal occurrence from each clause clique. Conversely a cover
of size L selects exactly one endpoint per variable and omits exactly one
occurrence per clause. That occurrence's incident edge forces its literal's
true endpoint to be selected. It therefore decodes to a satisfying assignment.
Consequently whenever a threshold formula is satisfiable, **every** minimum cover in its graph
has size L_k and decodes to a satisfying assignment.

For a guarded threshold formula, a cover of size L+1 always exists: select
both endpoints of z and one endpoint of every other variable; in every guarded
clause omit its z occurrence and select all other occurrences; omit the unit
clause's occurrence. All occurrence edges are covered, including the negative
selector occurrence's edge. Thus a guarded threshold optimum is exactly L when
satisfiable and exactly L+1 otherwise. This promise removes an unnecessary
optimization problem on unsatisfiable thresholds without weakening the target's
global-optimality contract. The unguarded final threshold is satisfiable and
therefore has optimum L.

Replace every undirected edge by its two directed arcs. A DFVS must hit each
resulting directed 2-cycle and is therefore a vertex cover. A vertex cover
leaves no arc and is therefore a DFVS. The valid sets, including their optima,
are exactly equal.

F emits the disjoint union of these bidirected graphs over k=2,...,U, using
disjoint vertex namespaces. Any minimum DFVS restricts to a minimum DFVS of
each threshold graph: otherwise replacing one restriction by a smaller solution
strictly improves the whole. This statement includes all tied optima.

## Recovery from an arbitrary minimum DFVS

G reconstructs the leaf-rank bit numbering for each threshold k from the
source label list and w=(k-1).bit_length(). It examines k=2,...,m-1.
Threshold namespaces omitted by F supply no selected true endpoints, so they
propose a single all-zero-rank block. On this nonidentical-tree branch that
block fails agreement and is rejected; no source optimization is repeated. It reads whether each corresponding
true endpoint belongs to the target deletion set and partitions labels by the
resulting bit values. It does not need to trust proposals from unsatisfiable
thresholds. Each proposal passes a direct polynomial check of label coverage,
agreement of restrictions, connecting-subtree disjointness, and acyclicity of
the component ancestry graph. G returns the accepted proposal with the fewest
blocks; increasing threshold order breaks ties deterministically.

Let OPT be the minimum possible source component count. On the nonidentical
branch, 2<=OPT<=U, so its threshold is emitted and satisfiable.
The restriction of **any** minimum target DFVS to that threshold graph
produces a satisfying rank assignment, hence a valid partition with at
most OPT components. By definition it has exactly OPT components. Thus at least
one proposal is valid, all accepted proposals have at least OPT components,
and the chosen one has exactly OPT. Proposals from unsatisfiable thresholds
cannot compromise the argument because they must pass direct validation.
This proves the full quantified implication for every source input and every
minimum target output, not only outputs built from source solutions.

## Worst-case time and encoding length

All augmented trees have O(m) vertices. At threshold k, there are O(m log m)
rank bits, O(m^2 log m) equality/comparison gates, and O(m^3) disagreeing-triple
clauses. Before guarding, clause width is at most max(4,ceil(log_2 m)+1):
the only unbounded fan-in gate conjoins bit equalities. Guarding adds one
literal per original clause. Total literal count is
O(m^3+m^2 log m), and total squared clause width is
O(m^3+m^2 log^2 m). Thus one cover graph has that order of vertices/edges, and
the m-threshold union has O(m^4+m^3 log^2 m)=O(m^4) vertices and arcs (for
asymptotically large m, log^2 m=O(m)). Vertex indices require O(log m) bits,
giving O(m^4 log m) target encoding length. No numeric weight is expanded.

The greedy feasibility search uses O(m^3) direct validations, each bounded by
O(m^3) combinatorial operations. It therefore adds at most O(m^6) operations.
The code's direct tree paths and triple calculations use at most polynomial
extra work. A pair-LCA query scans O(m) candidate ancestors and uses tuple
membership tests of O(m) cost, so it costs O(m^2). There is no cached pair-LCA
table. The O(m^2) pair queries cost O(m^4) per threshold; the O(m^3) triple
queries cost O(m^5) per threshold. Over O(m) thresholds, a conservative
O(m^6 polylog(m)) bound covers all of F excluding input-string costs.
Lexicographic sorting and parsing of arbitrary-length input labels and node ids
adds polynomial work in |x|; bit lengths are never assumed unit-cost.

G scans y into a set, reconstructs only O(m log m) rank indices per threshold,
and checks m proposed partitions on O(m)-vertex trees. Root/path scans, rooted
restriction comparisons and ancestry DAG checks are polynomial; O(m^5) is a
conservative combinatorial bound, plus polynomial string work in |x|+|y|.
G neither reconstructs the target graph nor calls an optimization oracle. The
output contains each label once. Both maps are deterministic and polynomial in
the required input bit lengths.

Tree traversal is iterative. To compare restrictions, process retained vertices
from descendants to ancestors: encode a leaf of index i as `Li;`, suppress a
one-child vertex, and encode a binary vertex by parentheses enclosing its two
lexicographically sorted child strings. Delimited leaf indices and balanced
parentheses make this representation injective on unordered rooted labelled
binary trees. Its size is O(m log m) per restriction root and its construction
uses polynomial string work. Thus neither traversal nor shape equality relies
on a fixed interpreter recursion limit.

## Status and provenance

This is a candidate proof awaiting independent review. Local formula diagnostics
are not actual-target checks. Full prepared verification is recorded in Round
006. The graph conversion uses classical SAT/vertex-cover and bidirection
constructions; no new complexity classification is claimed. The claimed
contribution is an explicit, checked instance map and all-optima decoder for the
fixed optimization endpoints. The earlier withdrawn source model is not used.
