# Parallel threshold reduction from MAAF to minimum DFVS

Let m=|X|+1 count all labels, including the added root label. The source and
output encodings are fixed in `contract.md`. This proof describes `algorithm.py`.
A solver is used only by the test harness, never by F or G.

## Polynomial Boolean verifier for a forest

Number labels 0,...,m-1 in lexicographic order. A membership variable a[l,s]
exists for 0<=s<=l<m. Each label belongs to exactly one slot. The implication
a[l,s] -> a[s,s] makes a nonempty slot s contain s, and no smaller label can
belong to it. Thus slots are exactly the partition blocks, canonically named by
their least labels; a[s,s] indicates whether slot s is used. Conversely every
partition has exactly this membership assignment.

For each input tree and slot, down[v,s] is the disjunction of membership over
labels below v. Compute it bottom-up. Compute outside[v,s] top-down as the OR
of outside[parent,s] and down[sibling,s], starting with false at the augmented
root. These are precisely the selected labels in the different directions
incident to a tree vertex.

A labelled leaf v is occupied by slot s exactly when its label belongs to s.
An internal binary vertex v is occupied exactly when at least two of its three
incident directions contain selected labels (the direction above the augmented
root is empty). This is precisely the condition for v to lie in the minimal
connecting subtree of the selected labels. For one selected label only that
leaf is occupied; for an empty slot no vertex is occupied. Require at most one
occupied slot at every vertex in each tree. This is exactly pairwise
vertex-disjointness of connecting subtrees. It does not require unused vertices
to be assigned to any component.

For every triple of labels whose induced rooted binary triples disagree between
the input trees, forbid placing all three in one slot. A rooted binary labelled
tree is determined by its induced rooted triples: for at least three labels,
the rooted cluster hierarchy is recovered from its triples; restrictions to
one or two labels are unique. Therefore these clauses are equivalent to
agreement of every block's two restrictions. Restriction followed by restriction
equals direct restriction, so the triples used are exactly those of each block.

## Encoding the component ancestry graph

Boolean comparisons orient every pair of slots into a tournament. For each
triple, forbid the two cyclic orientations. A tournament without a directed
triangle is transitive (a shortest directed cycle of length at least four has
a chord producing a shorter directed cycle). Thus the comparisons describe a
strict total order, including unused slots.

For each tree, let above[v,s] be true exactly when some **strict ancestor** of v
is occupied by slot s. Compute it top-down by
above[child,s] = above[parent,s] OR occupied[parent,s]. For distinct s,t require
above[v,s] AND occupied[v,t] -> s<t in the slot order.

These constraints express exactly the union of component ancestry relations.
If the root of connecting subtree s is above the root of subtree t, the clause
at the latter root enforces s<t. Conversely, suppose an occupied vertex u of s
is a strict ancestor of an occupied vertex v of t. The two subtree roots are
both ancestors of v, so they are comparable. If the root of t were an ancestor
of the root of s, the path inside connecting subtree t from its root to v would
contain u (or the root of s), intersecting s. Disjointness rules this out.
Hence the root of s is a strict ancestor of the root of t. Every imposed
comparison is therefore an actual component ancestry arc. A finite graph is
acyclic exactly when it admits a strict total order extending its arcs. Any
order of used slots extends to all slots. This proves both directions, without
identifying internal vertices of the two input trees.

All gate outputs are introduced by exact Tseitin equivalences, not merely
one-way implications. The OR gate is encoded by input -> output for each input
and output -> OR(inputs); AND is obtained by negation. Literal 1 is fixed true.
Constant simplifications preserve the exact Boolean function. An empty clause
is represented as the false unit (-1), which is inconsistent with literal 1.

## Component thresholds

A sequential Boolean counter has c[i,j] true iff at least j of the first i
representative variables a[s,s] are true:

c[i,j] = c[i-1,j] OR (c[i-1,j-1] AND a[i-1,i-1]),

with c[i,0]=true and c[0,j]=false for j>0. Its correctness follows by induction.
For k=1,...,m, append NOT c[m,k+1], omitting this clause at k=m. Call the result
Phi_k. The preceding equivalences prove:

Phi_k is satisfiable iff the source has an acyclic agreement forest with at most
k components. Every satisfying assignment supplies such a forest; every such
forest extends to a satisfying assignment. In particular Phi_m is satisfiable.

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
Consequently whenever Phi_k is satisfiable, **every** minimum cover in its graph
has size L_k and decodes to a satisfying assignment.

Replace every undirected edge by its two directed arcs. A DFVS must hit each
resulting directed 2-cycle and is therefore a vertex cover. A vertex cover
leaves no arc and is therefore a DFVS. The valid sets, including their optima,
are exactly equal.

F emits the disjoint union of these bidirected graphs over all k=1,...,m, using
disjoint vertex namespaces. Any minimum DFVS restricts to a minimum DFVS of
each threshold graph: otherwise replacing one restriction by a smaller solution
strictly improves the whole. This statement includes all tied optima.

## Recovery from an arbitrary minimum DFVS

G reconstructs the membership variable numbering from the source labels. In each
threshold graph it reads the selected true endpoints for membership variables
and obtains a proposed partition. Some unsatisfiable threshold graphs may
produce malformed proposals. G validates each proposal directly: label partition,
agreement of restrictions, connecting-subtree disjointness, and acyclicity of
the component ancestry graph. It returns a valid proposal with the fewest blocks,
with threshold order breaking ties deterministically.

Let OPT be the minimum possible source component count. Phi_OPT is satisfiable,
so the restriction of **any** minimum target DFVS to that threshold graph
produces a satisfying membership assignment, hence a valid partition with at
most OPT components. By definition it has exactly OPT components. Thus at least
one proposal is valid, all accepted proposals have at least OPT components,
and the chosen one has exactly OPT. Proposals from unsatisfiable thresholds
cannot compromise the argument because they must pass direct validation.
This proves the full quantified implication for every source input and every
minimum target output, not only outputs built from source solutions.

## Worst-case time and encoding length

All augmented trees have O(m) vertices. There are O(m^2) membership, comparison
and gate variables; the sequential counter also has O(m^2) gates. Membership
uniqueness, disjointness, ancestry comparisons and order transitivity generate
O(m^3) clauses. Rooted triple disagreement generates at most O(m^4) clauses.
Every clause has length at most m, and only O(m) uniqueness clauses have that
length; all remaining clauses have constant length (gate fan-in is at most 3).
Total literal occurrences and total squared clause lengths are O(m^4).

Each threshold graph consequently has O(m^4) vertices and edges, and their union
has O(m^5) vertices and arcs. Identifier indices require O(log m) bits, giving
O(m^5 log m) graph encoding length. Input label and identifier strings require
polynomial preprocessing in |x|; no bound assumes unit-cost arbitrary-length
strings. Tree paths and triples can be calculated by direct polynomial scans;
a conservative O(poly(|x|)+m^6) elementary-operation bound covers this code's
lists, sets, sorting, gate emission and graph construction. F is deterministic.

G scans the target output, reconstructs only O(m^2) primary variable indices,
and validates m proposed partitions on two O(m)-vertex trees. Direct root/path
and closure computations and all string operations take polynomial time in
|x|+|y|, conservatively O(poly(|x|+|y|)+m^5). It does not reconstruct the entire
graph, solve an optimization problem, or enumerate label subsets or partitions.
It emits at most m blocks and each label exactly once. Thus F and G satisfy the
required deterministic polynomial worst-case time and output-bit-length bounds.

## Status and provenance

This is a candidate proof awaiting independent review. Local formula diagnostics
are not actual-target checks. Full prepared verification is recorded in Round
004. The graph conversion uses classical SAT/vertex-cover and bidirection
constructions; no new complexity classification is claimed. The claimed
contribution is an explicit, checked instance map and all-optima decoder for the
fixed optimization endpoints. The earlier withdrawn source model is not used.
