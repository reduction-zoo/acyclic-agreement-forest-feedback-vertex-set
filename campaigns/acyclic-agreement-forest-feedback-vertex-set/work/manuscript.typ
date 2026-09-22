#import "report.typ": research-report
#show: research-report.with(
  title: "An exact reduction from acyclic agreement forests to directed feedback vertex set",
  date: "22 September 2026",
  status: "Reproducible rule reconstruction — awaiting expert review",
)
#set math.equation(numbering: "(1)")
#let opt = math.op("OPT")
#let lca = math.op("lca")

#heading(numbering: none)[Abstract]
We give deterministic polynomial-time maps from minimum-component acyclic
agreement forests of two rooted binary phylogenetic trees to minimum directed
feedback vertex set. Every globally minimum target solution recovers a globally
minimum source forest, including all ties. Monotone ranks on tree vertices encode
component membership and ancestral order. Parallel feasibility thresholds become
unweighted bidirected cover graphs; a selector bounds the cover penalty at every
infeasible threshold to one vertex. A directly validated feasible forest removes
unneeded thresholds. For $m$ augmented labels, the target has $O(m^4)$ vertices
and arcs and $O(m^4 log m)$ encoding bits. The contribution is an explicit,
checked rule and decoder. No new complexity classification, priority claim, or
minimum-overhead result is asserted.

= Introduction

Acyclic agreement forests express how two rooted phylogenetic trees can be
partitioned into compatible components without conflicting ancestral order.
They connect the comparison of evolutionary trees to hybridization networks
#link("https://arxiv.org/html/1112.5359")[\[1, §2\]]. An exact reduction to a graph
optimization problem must preserve more than the existence of a feasible
forest: an arbitrary optimal graph output must suffice to recover an optimal
forest.

The closest structural reductions to directed feedback vertex set optimize
splittings of a chosen agreement forest. The approximation guarantee in
#link("https://arxiv.org/html/1112.5359")[\[1, §4\]] retains a factor-six comparison
with the unrestricted optimum. Solving that restricted target exactly does not
remove this loss. Polynomial SAT encodings for agreement forests and
hybridization thresholds already exist #link("https://stjohn.github.io/research/sat6.pdf")[\[2, §§3–4\]].
SAT-to-cover constructions and bidirection are classical reduction tools
#link("https://doi.org/10.1007/978-1-4684-2001-2_9")[\[3\]].

This paper supplies a complete instance map and decoder for the unrestricted
exact optimization endpoints. Its rank encoding replaces separate component
membership and ancestral-order tables. Feasible upper bounds prune the
threshold range, and a guarded formula bounds the cost of each infeasible
threshold. These choices reduce the explicit graph compared with the component-slot
baseline measured in the appendix. The construction does not establish a
practical advantage over direct forest solvers or the best published encodings.

*Theorem 1 (exact recovery).* Let $x$ consist of two rooted binary phylogenetic
trees on the same nonempty leaf set, with an additional root label, and let $m$
be the number of augmented labels. There are deterministic polynomial-time maps
$F$ and $G$ such that $F(x)$ is an explicit unweighted digraph and, for every
globally minimum directed feedback vertex set $Y$ of $F(x)$, $G(x,Y)$ is an
acyclic agreement forest with the minimum number of components. The graph has
$O(m^4)$ vertices and arcs and $O(m^4 log m)$ encoding bits. Neither map calls an
optimization solver.

The construction encodes every relevant source threshold in a separate graph.
A minimum solution of their disjoint union is minimum on each threshold graph.
The graph at the true source optimum therefore supplies an optimal forest.
Direct validation lets the decoder discard proposals from infeasible thresholds.

= Definitions and output semantics

Let $X$ be the original leaf set and $ρ ∉ X$ the additional label. Augment
each input tree by placing its root and a new leaf labelled $ρ$ beneath a new
root. Write $X^+ = X union {ρ}$ and $m = |X^+|$. Internal vertices of the two
trees remain distinct, regardless of their input names.

For a nonempty block $B subset.eq X^+$, its connecting subtree is the minimal
subtree joining its leaves, rooted at their lowest common ancestor. Its
restriction suppresses vertices with one retained child. An agreement forest
is a partition $𝒫$ of $X^+$ such that corresponding restrictions agree and the
connecting subtrees are pairwise vertex-disjoint within each input tree.
Its component ancestry graph has an arc $B arrow C$ whenever the root of $B$
is a strict ancestor of the root of $C$ in either tree. The forest is acyclic
when this union of ancestry relations is acyclic. Define $opt(x)$ as the least
number of blocks in such a forest.

A directed feedback vertex set of a digraph is a set whose deletion leaves an
acyclic digraph. The target output must have globally minimum cardinality. The
source output must have globally minimum component count. Both output sets are
nonempty: the singleton partition is a source witness, and all vertices form a
target witness. The empty set is the unique minimum target output on an empty
graph. No no-solution output is admitted.

= Ranks encode acyclic agreement forests

Fix an integer threshold $k$ with $1 ≤ k ≤ m$. Assign every augmented tree vertex
a rank $r(v)$ in $\{0,…,k-1\}$; copies of a labelled leaf share its rank. Impose
three conditions. Ranks do not decrease along parent-to-child edges. Equal-rank
leaves have an LCA of that same rank in each tree. Finally, three leaves cannot
all have equal rank if their rooted triples differ between the two trees.

*Lemma 2 (rank characterization).* These conditions hold for some rank assignment
if and only if an acyclic agreement forest has at most $k$ blocks. Every such
assignment yields a forest by grouping equal-rank leaves.

*Proof.* For a block $B$ with at least two leaves, choose one leaf from each child
branch of its connecting-subtree root. Their LCA is that root, so the LCA condition
gives it the common leaf rank. Edge monotonicity forces this rank throughout all
paths from that root to leaves of $B$. A singleton subtree is its leaf. Thus each
connecting subtree is monochromatic. Different blocks have different ranks and
cannot intersect.

Rooted triples determine a rooted binary labelled tree. To see this, a proper
label subset $C$ of size at least two is a cluster exactly when every pair
$a,b ∈ C$ and every $c$ outside $C$ induce $a b | c$. The forward implication
follows from the cluster root. For the converse, if $C$ is not a cluster, its
LCA has a descendant $c$ outside $C$, while $C$ meets both child branches.
Taking $a,b$ from those branches contradicts the triple condition. Triples
therefore determine the cluster hierarchy. Restrictions to one or two leaves
are unique. Excluding monochromatic disagreeing triples consequently makes
the two restrictions of every block equal.

If a block root is ancestral to another, edge monotonicity gives a nondecreasing
rank between them. Distinct blocks have distinct ranks, so every component
ancestry arc strictly increases rank. The forest is acyclic and uses at most
$k$ blocks.

Conversely, take a forest with $q ≤ k$ blocks. Number the blocks from $0$ through
$q-1$ in a topological order of their component ancestry graph, and assign these
numbers to their leaves. At every other tree vertex, use the minimum rank of a
descendant labelled leaf. This assignment is nondecreasing along edges.

Suppose $v$ belongs to the connecting subtree of block $B$. A leaf of $B$ lies
below $v$. For a leaf below $v$ from another block $C$, both component roots are
ancestors of that leaf. If the root of $C$ were at or above the root of $B$, the
connecting path for $C$ would intersect the subtree of $B$ at $v$. Disjointness
excludes this. The root of $C$ is therefore strictly below the root of $B$, so
$C$ has larger rank in the topological order. The minimum descendant rank at
$v$ is exactly the rank of $B$. Every connecting subtree is monochromatic,
which proves the LCA condition. Agreement of restrictions excludes disagreeing
monochromatic triples. This gives all three rank conditions. $square$

== An explicit Boolean encoding

Use $w=ceil(log_2 k)$ bits for each rank, most significant bit first. Allocate
leaf bits first, sharing them between the trees; allocate fresh bits for internal
vertices. Bound each leaf rank by $k-1$. An internal rank is bounded by every
descendant leaf through edge monotonicity, so it needs no separate upper bound.
For $k=1$, bit vectors are empty and represent zero.

Equality is the conjunction of bit equalities. To compare unsigned vectors
$a$ and $b$, start with a true lower-bit comparison and process bits from least
to most significant. At each position replace that comparison by the majority
of the negated bit of $a$, the bit of $b$, and the previous comparison. Equal
bits preserve the previous result; unequal bits set the comparison correctly.
This proves the comparator by induction.

Encode every gate by both implication directions. Bit equality has its four
truth-table clauses; majority has the six clauses saying that each true input
pair forces the output and that the output requires a true input in every pair.
OR gates and their dual AND gates use their usual equivalence clauses. A
constant variable is fixed true, and a false clause is represented by its
negative unit. Constant and repeated-literal simplifications preserve equivalence.

Assert the parent-child comparisons. For a leaf pair $a,b$ with equality flag
$E_(a b)$, assert
$ E_(a b) ==> r(a) ≤ r(lca(a,b)). $
The reverse inequality follows from tree edges, giving the LCA condition.
Comparisons for a shared LCA and leaf are reused within a tree. For a disagreeing
triple $a,b,c$, assert $not E_(a b) or not E_(a c)$. Call the complete CNF $Φ_k$.
Lemma 2 and the exact gate equivalences prove that $Φ_k$ is satisfiable exactly
when a forest with at most $k$ blocks exists. Every satisfying assignment yields
such a forest.

= The forward map

== A certified threshold range

First compare the full restrictions. If they agree, return the empty graph;
the source optimum is one. Otherwise the source optimum is at least two.
Starting from singleton blocks, try all pairs of current blocks in deterministic
order. Accept the first merge whose resulting partition passes the direct forest
predicate, then restart. Stop when no merge is accepted. Each acceptance reduces
the component count, so at most $m-1$ merges occur. Let $U$ be the final count.

Every accepted partition is feasible. Initially any two singleton labels can
merge: their two-leaf restrictions agree, their connecting subtree meets no
other labelled leaf, and every remaining component is a singleton with no
outgoing ancestry arc. Consequently
$ 2 ≤ opt(x) ≤ U ≤ m-1. $ <range>
Only thresholds $2,…,U$ are needed. The greedy procedure need not find an
optimal forest.

== Guarded formulas and cover graphs

For each $k<U$, add a fresh selector $z$ to every clause of $Φ_k$ and append the
unit clause $not z$. Call the resulting CNF $Ψ_k$. It is equisatisfiable with
$Φ_k$, and its satisfying assignments give the same leaf ranks. At $k=U$, use
$Φ_U$ unchanged because the feasible forest certifies satisfiability.

For any resulting CNF $Θ$, create two endpoints $p_0,p_1$ and an edge for each
Boolean variable $p$. For each clause $C$ of width $d_C$, create a private clique
of occurrence vertices. Join every occurrence to the variable endpoint that
makes its literal true. Let $t$ be the number of variables and define
$ L_Θ = t + sum_(C ∈ Θ) (d_C-1). $ <baseline>
All clauses are nonempty. Replace each undirected edge by its two opposing arcs.
The resulting threshold digraph is $H_k$.

*Lemma 3 (cover baseline and unit gap).* Every cover has size at least $L_Θ$.
If $Θ$ is satisfiable, every minimum cover has size $L_Θ$ and decodes to a
satisfying assignment. A guarded formula has minimum cover size $L_Θ$ when
satisfiable and $L_Θ+1$ otherwise.

*Proof.* A cover selects at least one endpoint of each variable edge and at
least $d_C-1$ vertices in each private clique. These disjoint sets give
@baseline. A satisfying assignment attains it by selecting its truth endpoints
and omitting one true occurrence per clause. Conversely, equality forces exactly
one endpoint per variable and exactly one omitted occurrence per clause. The
omitted occurrence's incident edge forces the corresponding true endpoint.
Every clause is satisfied.

For a guarded formula, select both endpoints of $z$ and one endpoint of every
other variable. In each guarded clause omit the $z$ occurrence and select all
other occurrences; omit the negative unit's occurrence. All edges are covered,
including the unit's edge to $z_0$. This cover has size $L_Θ+1$. An unsatisfiable
formula cannot attain the baseline, which proves the unit gap. $square$

@fig-cover shows the complete graph for a contradictory one-variable formula
after guarding. Selecting both selector endpoints supplies the single extra
vertex permitted by Lemma 3.

#figure(
  image("figures/guarded-cover.svg", width: 88%),
  caption: [Exact cover graph for $(q or z) and (not q or z) and (not z)$.
  Endpoints encode variable values; $c_(j,ℓ)$ is the occurrence of literal $ℓ$
  in clause $j$. Each line represents two opposing arcs. Filled vertices form a
  minimum cover of size $5$; the baseline is $4$. All $9$ vertices and $9$
  undirected edges are drawn. The curved edge attaches the second $z$ occurrence
  directly to $z_1$. No edge is omitted.],
) <fig-cover>

A DFVS in a bidirected graph must hit every directed two-cycle, so it is a vertex
cover. A cover leaves no arc and is a DFVS. Their feasible sets and minimum
solutions are identical. Define $F(x)$ as the disjoint union of $H_2,…,H_U$,
using distinct vertex namespaces. @fig-thresholds illustrates this composition.

#figure(
  image("figures/thresholds.svg", width: 100%),
  caption: [Schematic threshold composition for $U≥4$. Each box is the entire
  digraph $H_k$; all internal vertices and arcs are omitted. There are no arcs
  between boxes. A global minimum DFVS $Y$ restricts to a minimum DFVS in each
  box, since replacing a nonminimum restriction would improve $Y$.],
) <fig-thresholds>

= Recovery from every minimum target solution

Given $x$ and a minimum DFVS $Y$ of $F(x)$, compare the full tree restrictions.
If they agree, output the full-label block. Otherwise, for every
$k=2,…,m-1$, read each leaf bit from membership of its true-value endpoint in
$Y$. The numbering is reconstructed from the sorted label order and the bit
width; selector and gate variables were allocated later. Group equal bit
vectors into blocks.

Validate each proposal directly: it must partition the augmented labels, have
equal restrictions, have vertex-disjoint connecting subtrees in each tree, and
have an acyclic component ancestry graph. Among accepted proposals, return one
with the fewest blocks, breaking ties by increasing threshold. Missing
namespaces give all-zero ranks and propose the full-label block, which fails
agreement on this branch. The decoder does not reconstruct the graph or rerun
the greedy search.

*Proof of Theorem 1.* The forward construction gives an explicit legal graph.
A global minimum DFVS restricts to a minimum DFVS on each threshold graph,
by the disjointness shown in @fig-thresholds. By @range, the threshold
$k=opt(x)$ is present. Its formula is satisfiable, so Lemma 3 implies that every
minimum target restriction decodes to a satisfying rank assignment. Lemma 2
gives a feasible forest with at most $opt(x)$ components, hence exactly that
many. There is therefore at least one accepted optimal proposal. Every other
accepted proposal is feasible and cannot have fewer components. This includes
proposals from infeasible thresholds, which need not encode satisfying
assignments. The decoder returns an optimal forest for every minimum target
output. The equal-tree branch handles source optimum one and empty target
output. Polynomial bounds for both maps follow below. $square$

= Size and running time

At one threshold there are $O(m log m)$ rank bits, $O(m^2 log m)$ equality and
comparison gates, and $O(m^3)$ disagreeing-triple clauses. The only gate of
unbounded fan-in conjoins bit equalities. Before guarding, clause width is at
most $max(4,ceil(log_2 m)+1)$; guarding adds one literal per original clause.
The literal count is $O(m^3+m^2 log m)$, and the sum of squared clause widths
is $O(m^3+m^2 log^2 m)$.

For $t$ variables and clause widths $d_C$, the exact graph counts are
$ |V(H_k)| &= 2t + sum_C d_C, \
  |A(H_k)| &= 2t + sum_C d_C dot (d_C-1) + 2 sum_C d_C. $
There are at most $m$ thresholds. Since $log^2 m=O(m)$, their union has
$O(m^4)$ vertices and arcs. Generated indices use $O(log m)$ bits, giving
$O(m^4 log m)$ explicit encoding length. No weight is expanded or stored
implicitly.

The greedy upper-bound search checks $O(m^3)$ proposals. Each direct forest
validation takes at most $O(m^3)$ combinatorial operations, with polynomial
bit and string costs. In the implemented path representation, a pair-LCA query
scans $O(m)$ ancestors and performs tuple membership tests of $O(m)$ cost.
All pair queries at a threshold take $O(m^4)$ work; all triple queries take
$O(m^5)$. Across all thresholds, $O(m^6 "polylog"(m))$ is a conservative
bound for the forward combinatorial and index work. Parsing and sorting arbitrary
input strings add polynomial work in the actual source encoding length.

The decoder reads the target output into a set, reconstructs leaf-bit indices,
and validates fewer than $m$ partitions. The conservative bound is $O(m^5)$
combinatorial work plus polynomial bit and string work in the combined input
lengths. The output lists each source label once. Tree traversal is iterative.
Restrictions use delimited leaf indices and sorted, parenthesized child strings,
with unary vertices suppressed, so tree depth does not invoke a fixed call-stack
limit. Both maps are deterministic and polynomial in their required input sizes.

#pagebreak()
= Scope and limitations

The rule supplies exact recovery for unrestricted source forests and all target
optima. Its bidirected targets are vertex-cover instances. It establishes no
approximation guarantee, parameterized improvement, optimal size bound, or
practical speed superiority. Polynomial SAT encodings and generic reduction
composition already imply broad existence results; the contribution here is
the explicit rank construction, decoder, proof, and checked implementation.
Priority for the rank characterization or selector technique remains unassessed.

#heading(numbering: none)[References]

[1] Steven Kelk, Leo van Iersel, Nela Lekić, Simone Linz, Celine Scornavacca,
and Leen Stougie. _Cycle killer… qu’est-ce que c’est? On the comparative
approximability of hybridization number and directed feedback vertex set._
arXiv:1112.5359v1, 2011.
#link("https://arxiv.org/html/1112.5359")[Primary manuscript.]

[2] Maria Luisa Bonet and Katherine St. John. _Efficiently Calculating
Evolutionary Tree Measures Using SAT._ Author-hosted manuscript, §§3–4,
printed pp. 6–8. Year and venue are not specified here because the consulted
copy did not establish them.
#link("https://stjohn.github.io/research/sat6.pdf")[Primary manuscript.]

[3] Richard M. Karp. _Reducibility among Combinatorial Problems._ In
_Complexity of Computer Computations_, pp. 85–103, Plenum Press, 1972.
#link("https://doi.org/10.1007/978-1-4684-2001-2_9")[doi:10.1007/978-1-4684-2001-2_9.]

#pagebreak()
#set heading(numbering: "A.1.")
#counter(heading).update(0)
= Verification and reproducibility

== Evidence and finite limits

The tested implementation is `work/algorithm.py` at Git revision `25cab27`.
The proof's local LCA accounting was corrected in `5f3a30b` without changing
either map. The independent review and focused follow-up are retained in
`reviews/rank-threshold/`. The review advances this rule for expert assessment;
it is not a formal proof certificate or publication acceptance.

The prepared family has 327 input records: all 236 ordered labelled binary-tree
pairs through four original leaves, 80 seeded pairs on five through seven leaves,
nine historical inputs, and two explicit regressions. Source oracles independently
agree on 113,194 partition predicates and all 956 minimum partitions. A separate
exhaustive check agrees with all 766 minimum outputs on 631 small directed graphs.
The larger tree pairs use seed 20260922; the committed input file fixes the cases.

The complete current candidate loop executes both maps as subprocesses and
independently solves each emitted target. All 327 inputs and 38,427 minimum-target
recoveries passed. The 300 nonempty-target records stop at 128 outputs each;
the 27 empty targets are exhaustively checked. Thus these counts do not represent
all target ties. Eight disjoint shards cover the exact case-name set and all
exit successfully. A further independent CP-SAT implementation passes 12 input
records and 33 recoveries. Both maps also pass identical-tree regressions at
1, 2, and 1,200 leaves with renamed nodes and reversed child orders.

The reviewer performed 47 targeted recovery calls on three- and four-leaf
pairs. These exhaust the selected optimal-threshold rank projections and include
all 32 binary leaf-rank patterns at an infeasible threshold. They recover all
source optima on those pairs. This projection coverage is distinct from complete
DFVS-set enumeration. Solver unknowns and interrupted runs are never counted
as optimum answers. All tests have finite instance or output bounds; none uses
a solver or process timeout. The universal statement rests on the proof.

== Measured graph overhead

@tab-size compares the current explicit graphs with the earlier component-slot
baseline on the same stored inputs. Each cell is a median over the indicated
number of records. The iterative traversal repair preserves every vertex and
arc on this family. The improvement is relative to this implementation baseline;
no lower bound on possible overhead or comparison to the best published
encoding is claimed.

#figure(
  table(columns: (auto, auto, 1fr, 1fr, 1fr, 1fr), align: right,
    inset: 5pt, stroke: 0.4pt,
    table.header([$|X|$], [Records], [Baseline vertices], [Current vertices], [Baseline arcs], [Current arcs]),
    [4], [231], [12,664], [546], [39,698], [1,610],
    [5], [33], [25,889], [3,081], [82,522], [10,796],
    [6], [32], [46,790.5], [7,452], [151,156], [28,930],
    [7], [16], [77,799], [15,267.5], [254,150], [60,440],
  ),
  kind: table,
  caption: [Graph-size medians on fixed records. Source counts include regression
  records that overlap the exhaustive topological family. The current worst
  seven-leaf graph has 23,437 vertices and 96,142 arcs.],
) <tab-size>

These remain large expansions of small source trees. Timing measurements in
the retained comparison belong to the previous recursive implementation and
are not benchmarks of the current maps or end-to-end solver performance.

#pagebreak()
== Environment and commands

From the repository root, use Python 3.12.11 and uv 0.12.7. The committed
lockfile pins Z3 4.15.4.0, OR-Tools 9.15.6755, and NetworkX 3.6.1. The maps
themselves use only the Python standard library. Typst 0.15.1 compiles this paper.
Lean and Lake are available, but no Lean formalization is claimed.

```sh
uv sync --locked --python 3.12.11
cd campaigns/acyclic-agreement-forest-feedback-vertex-set/work
uv run --locked python check.py --self-test
uv run --locked python check.py --candidate algorithm.py
uv run --locked python verify.py --candidate algorithm.py
uv run --locked python ../rounds/006/deep_tree_check.py
uv run --locked python ../rounds/006/gadget_check.py
uv run --locked python ../rounds/006/reproduce_modes.py
```

The recorded scheduling appends `--shard I 8` to the candidate-check command
for each integer $I$ from $0$ through $7$. The unsharded command checks the
same family. The minimal reproduction script selects a stored three-leaf input,
executes the forward command, obtains a minimum target solution independently,
and executes extraction. Its target has 352 vertices and 1,024 arcs; its
minimum DFVS size is 193, and recovery returns an optimal two-component forest.
It tests one minimum target output and does not exhaust that target's optima.

For a legal source JSON document, the two public command modes are:

```sh
uv run --locked python algorithm.py < source.json > target.json
uv run --locked python algorithm.py --extract \
  < recovery.json > forest.json
```

The extraction input `recovery.json` contains the original `source` object and
a `target_solution` object. The latter has `problem` equal to `dfvs` and
`feedback_vertex_set` equal to a globally minimum deletion list for the actual
`target.json`. The reproduction script constructs this payload automatically.
`contract.md` specifies all JSON fields and the exact legal domain.

The proof, preparation report, verification report, and Round 006 logs retain
full evidence and limitations. The independent review includes primary-source
locations and its bounded literature coverage. Its checks used a fresh reviewer
context with instruction-based write confinement; no filesystem sandbox or
separate model was claimed as a correctness guarantee.

```sh
uv run --locked python figures/draw_gadgets.py
typst compile manuscript.typ manuscript.pdf
```

The figure generator checks the exact gadget's adjacency and minimum cover by
exhaustive subsets. The compiled PDF is inspected page by page for mathematical
notation, figure legibility, clipping, and layout. These presentation checks do
not extend the theorem's formal verification status.
