# Candidate proof — slot CNF, weighted cover, and DFVS

This is the proof for the executable candidate in `algorithm.py`. The finite
formula checks in Round 002 support the encoding on the prepared fixtures; the
independent target harness run is still pending because its positional Z3
oracle did not finish the first expanded graph before the run was interrupted.

## Source encoding

Let (L=X\cup\{\rho\}), and attach the root leaf (ho) to each input tree.
Use (|L|) component slots. For each augmented-tree vertex (v), tree index
(i), and slot (s), the formula has a variable (z_{i,v,s}). Exactly one
slot is assigned to each vertex. The two copies of every labelled leaf are
identified by clauses, so both trees give every label the same slot. A variable
(u_s) records that slot (s) contains a label; the clauses

\[
 z_{i,v,s}\Rightarrow u_s,
 \qquad
 u_s\Rightarrow\bigvee_{\ell\in L}z_{0,\ell,s}
\]

make the used slots exactly the blocks of the partition.

For each tree and slot, `top` variables mark vertices whose parent is outside
the slot. The clauses make `top` equivalent to being the unique top vertex and
allow at most one top vertex per slot. Hence every nonempty slot is one
connected part of the tree, and the differing tree edges are precisely the cut
edges.

For every triple of labels, the rooted triple displayed by the two augmented
trees is computed directly from their fixed parent maps. If the two rooted
triples differ, a clause forbids all three labels from receiving one slot.
Rooted triples characterize rooted binary labelled trees, so these clauses are
equivalent to agreement of the restrictions for every block.

For each tree edge (c\to p) and slot (s), a `keep` variable represents an
edge retained in the rendered component. It requires both endpoints in the
slot. If (p) is the apex of a part, the edge is retained exactly when the
other child of (p) is also in the slot; otherwise the unlabelled unary apex is
suppressed. This is the renderer used by the prepared source validator.

Finally, Boolean variables encode a strict total order on the common node ids.
For every retained edge (c\to p), the formula requires (c<p). Pairwise
comparability and transitivity make this order exist exactly when the union of
the retained component arcs is acyclic.

Therefore satisfying assignments of the formula are in correspondence with
valid acyclic agreement forests, after forgetting slot permutations, and

\[
 \sum_s u_s = \text{number of forest components}.
\]

The forward direction assigns each cut part one slot and chooses a topological
order. In the reverse direction, the connected slot parts define cuts; the
triple clauses give agreement and the order gives acyclicity. Every slot is
labelled, so no label-free component is introduced.

## CNF to unweighted DFVS

The formula has only positive or negative literals and is satisfiable on every
legal source instance because the source always has an agreement forest. Let

\[
 B=|L|+1.
\]

For each formula variable (q), make two vertex-cover endpoints (q_0,q_1)
joined by an edge. Endpoint (q_b) has weight (B+1) exactly when (q) is a
slot-use variable and (b=1); every other endpoint has weight (B). For a
clause (C=(\lambda_1,\ldots,\lambda_d)), make a (d)-vertex clique of
clause vertices, each of weight (B). Join the clause vertex for
(\lambda_j) to the endpoint (q_b) representing that literal.

In a weighted vertex cover, a clause clique costs at least ((d-1)B), and it
costs exactly that amount only if an omitted clause vertex has a true literal.
There is a satisfying assignment, so a cover attaining the sum of these
baseline clause costs exists. Any cover with an extra clause vertex costs at
least (B) more. Since changing all slot-use choices can save at most
(|L|<B), no minimum cover has an extra clause vertex. A variable edge requires
at least one endpoint; selecting both costs at least (B>|L|) above the
one-endpoint baseline, so no minimum cover selects both. Thus every minimum
cover selects exactly one endpoint per formula variable, satisfies every clause,
and minimizes the number of true slot-use variables.

To remove weights, replace a cover vertex of weight (w) by (w) independent
clones. For every cover edge, join every clone of one endpoint to every clone
of the other endpoint in both directions. The resulting graph is an explicit
unweighted digraph. Its directed 2-cycles are exactly the clone pairs for
cover edges, so its DFVSs are exactly vertex covers of the clone graph.

The clone groups of a minimum cover are whole groups: the clones in one group
have identical neighbours and no edges within the group, so an independent set
containing one clone can be enlarged to contain the whole group. Taking
complements, every minimum vertex cover contains either all or none of each
group. Hence every minimum DFVS decodes to the same weighted-cover choices
described above, including ties.

## Recovery

`--extract` identifies the selected clone groups, reads the unique selected
endpoint for every formula variable, and obtains the (z)-slot of every tree
vertex. It lists each used slot's labels and raw tree part, recomputes the
retained component arcs with the same apex-suppression rule, and emits the two
cut sets. The preceding argument shows that every minimum target output
decodes to a satisfying formula assignment with the minimum number of used
slots, so the emitted forest is feasible and globally minimum.

## Polynomial bounds

The augmented trees have (O(n)) vertices and there are (O(n)) slots. The
slot, connectivity, triple, retained-edge, and order clauses use polynomially
many variables and clauses; the explicit total-order encoding is
(O(n^3)). The number of formula variables and clauses is therefore
polynomial in the source encoding. Every weight is at most (B+1=O(n)), so
clone expansion and the explicit complete bipartite arc lists are polynomial.
Both maps scan these explicit structures a polynomial number of times. Recovery
also scans the target output once and reconstructs the same bounded formula, so
its time and output length are polynomial in (|x|+|y|).
