# Independent review: rank-threshold reduction

**Decision: ADVANCE for the fixed rule-completion target.** The current rule
supplies deterministic polynomial maps and a convincing general proof that
every globally minimum target DFVS recovers an exactly optimal source forest.
This means eligible for expert review, not publication acceptance. No blocking
correctness defect was found. There is one nonblocking runtime-accounting
correction below. Novelty is limited to an explicit construction and checked
implementation; neither existence of a polynomial reduction nor use of SAT is
a new complexity result. Significance is sufficient for this campaign's
explicit rule-completion acceptance criteria, not established as a research
breakthrough or practical solver improvement.

Review date: 2026-09-22. Repository HEAD: `83664d0`; `work/algorithm.py` and
`work/proof.md` agree with `25cab27` (verified with `git diff`). Paths below are
relative to `campaigns/acyclic-agreement-forest-feedback-vertex-set/` unless
otherwise stated. This is the first review in the assigned directory. The
earlier recursive implementation's failure and repair were assessed from the
current files and retained Round 006 evidence, not treated as an outstanding
defect in the repaired implementation.

## Correctness judgment

**Supported on the stated legal domain.** I read the fixed question, executable
contract, entire implementation and proof, preparation and verification reports,
relevant Round 006 evidence, independent source reference, Verify implementation,
and the actual prepared recovery loop. The source predicate is the augmented
label partition with agreeing restrictions, vertex-disjoint connecting subtrees,
and acyclic union of component ancestry relations. It does not identify internal
vertices between trees. Both valid-output sets are nonempty: singleton forests
and deleting all graph vertices give feasible solutions, hence finite optima.
No NO-SOLUTION answer is appropriate.

The substantive proof checks are:

1. **Ranks characterize exactly the feasible forests.** In `work/proof.md`,
   “Rank characterization,” equal-rank leaves force their connecting subtree to
   be monochromatic by the LCA condition and edge monotonicity. Distinct blocks
   cannot intersect. Conflicting rooted triples forbid precisely the restriction
   disagreements for binary trees, and strict rank increase along every
   intercomponent ancestry arc excludes cycles. Conversely, topologically
   ordered component numbers extend by minimum descendant-leaf rank. The crucial
   premise is disjointness: a different component with a leaf below a vertex of
   B cannot have its root at or above B's root, since its connecting path would
   intersect B. Thus its rank exceeds B's. The proof includes that premise.
   Neither arbitrary internal-node renaming nor unused vertices breaks the
   argument. The supporting monotone-ranks experience entry has exactly these
   premises; its pending-review label was not used as evidence.
2. **CNF and implementation agree.** `work/algorithm.py:68–161` implements exact
   Boolean gate equivalences, shared leaf bits, unsigned comparisons, and the
   pair/triple implications. The comparator processes low bits first so each
   higher unequal bit overrides the accumulated result. Internal ranks are
   bounded through descendant leaves. The constant variable's unit clause is
   retained even though later gate clauses simplify constant literals.
   Appending the selector preserves leaf-bit indices.
3. **Pruning retains the optimum threshold.** `algorithm.py:181–208` validates
   every accepted greedy merge. Starting with singleton blocks is feasible, and
   merging any two initial singleton labels is feasible: the other singleton
   components are leaves and have no outgoing ancestry arcs. Thus for distinct
   input topologies, `2 <= OPT <= U <= m-1`. Agreement of whole restrictions
   handles the optimum-one branch, including one- and two-leaf instances.
4. **Every target optimum has the needed local property.** The variable edges
   and private clause cliques in `algorithm.py:164–178` give the lower bound
   `L = V + sum(d-1)`. Equality forces exactly one truth endpoint per variable
   and one omitted occurrence per clause; its incident edge forces a true
   literal. This proves the property for every minimum cover at a satisfiable
   threshold, not only covers generated from intended assignments. The guarded
   formula admits the explicit size-L+1 cover using both selector endpoints,
   proving the stated unit gap. The guarded-threshold experience entry's
   nonempty-clause premise holds, including represented false clauses.
   Bidirection makes covers and DFVS sets identical. Disjoint threshold
   namespaces make minimum cardinality additive, so a global optimum is locally
   minimum at every threshold. No uniqueness or tie-breaking assumption is used.
5. **Recovery is exact.** `algorithm.py:237–259` reads the same sorted label
   order and bit indices as F, then validates every proposed partition using
   the actual source definition (`algorithm.py:211–234`). At threshold OPT,
   every minimum DFVS yields a feasible forest with at most OPT blocks, hence
   exactly OPT. All other accepted proposals have at least OPT. Missing
   namespaces propose the full-label block, rejected on the distinct-tree
   branch. Unsatisfiable thresholds need not yield meaningful assignments;
   validation prevents them from spoiling the output. The minimum accepted
   proposal therefore belongs to the complete optimal source output set.

The iterative repair is sound: construction numbers parents before descendants,
so reversing that order suffices for canonical restrictions. Delimited leaf
indices and balanced binary-parenthesis encodings are injective, with unary
vertices suppressed. No operation on tree depth requires Python recursion.
Flat JSON nodes also avoid encoding the tree by deeply nested JSON. The
1,200-leaf regression exercises the identical-tree branch only; general
totality on other depths comes from the iterative code argument, not that test.

## Bounds, determinism, and a minor correction

For a threshold formula with V variables and clause widths d_C, the emitted
graph has exactly

`N = 2V + sum_C d_C`,

`A = 2V + sum_C d_C(d_C-1) + 2 sum_C d_C`

vertices and directed arcs respectively. Its namespaces are disjoint and all
arc endpoints exist. With `m=|X|+1`, the proof's gate/literal counts give
`N,A = O(m^4)` over all thresholds and `O(m^4 log m)` target encoding bits.
No exponential weight expansion or implicit graph is hidden. Rank numbers and
generated indices have O(log m) bits; arbitrary input strings contribute their
actual lengths to reading, sorting, and output costs.

F and G contain no solver calls, runtime randomness, exponential enumeration,
or external state dependence. All output-relevant set choices are sorted or
singletons; unordered sets in validation affect only Boolean outcomes.
F's O(m^3) greedy proposals each require at most O(m^3) combinatorial validation
work, up to polynomial bit/string costs. G considers fewer than m proposals and
has the conservative O(m^5) combinatorial bound stated in the proof.

**Nonblocking finding, `work/proof.md:191–194`: the local LCA work estimate is
too optimistic for the actual tuple representation.** `algorithm.py:37–39`
scans candidate ancestors and tests membership in tuples. A pair LCA can cost
O(m^2), not O(m), since each membership test can scan O(m) entries. There is no
pair-LCA table cached by the implementation. Consequently the safe bounds are
O(m^4) for all pair queries per threshold and O(m^5) for all triple queries per
threshold. Multiplying by O(m) thresholds still fits the stated overall
`O(m^6 polylog m)` F bound. This does not invalidate polynomiality, graph size,
or the acceptance theorem. Correct those two local estimates when polishing the
proof; no algorithm change or full test rerun is needed for that correction.

## Independent targeted checks and reused evidence

`check_recovery.py` in this directory invokes F and G as fresh subprocesses and
imports no candidate code. Its new target solver reads actual bidirected graph
adjacency, imposes cover constraints, and proves optimum cardinality by
successive exact surplus checks above a disjoint-clique packing bound. Neither
source optima nor threshold metadata enter target optimization. The source
oracle is the unchanged, definition-based `work/source_reference.py`, reused
after inspection; it exhaustively enumerates partitions and never imports the
candidate. Candidate vertex names are used only afterward to select targeted
rank projections, not to establish the target optimum.

Reproduction from repository root:

```sh
.venv/bin/python -B campaigns/acyclic-agreement-forest-feedback-vertex-set/reviews/rank-threshold/check_recovery.py
```

Results in `check_recovery.txt`:

| Source pair | Source optimum / number of optimal forests | Target vertices / arcs / optimum | Complete optimal-threshold rank projections | Forced infeasible-threshold patterns |
|---|---|---|---|---|
| Three-leaf cherry swap | 2 / 3 | 361 / 1050 / 198 | 3 | 0 |
| Four-leaf quartet swap | 3 / 6 | 2209 / 7692 / 1375 | 12 | 32 |

All 47 recovery calls passed source feasibility and membership in the independently
enumerated source optimum set. The quartet probes force every binary leaf-rank
pattern at infeasible threshold 2, while requiring a globally minimum target
solution. All six quartet source optima and all three cherry-swap source optima
were recovered. Repeated F calls agreed, source node namespaces and list orders
differ, and target deletion-list order is reversed before recovery. Projection
enumeration ends in solver-proved infeasibility. This is complete enumeration
of those projected assignments, **not** of all target DFVS sets or all
cross-threshold combinations. The 47 calls are not asserted to be 47 distinct
target sets across the different checks.

An initial direct-cardinality-objective check was manually terminated to replace
that formulation with the graph-derived surplus formulation (exit 143, no
completed result). Its script is retained as `check_recovery_direct.py`; it is
not passing evidence or an oracle answer. The completed replacement exited zero.
No solver, subprocess, shell, or wrapper timeout or wall-clock limit was set.

I independently checked the retained shard log names and totals against
`work/cases.json`; `evidence_audit.txt` records exact coverage of 327 names,
38,427 recoveries, and 300 capped records. This verifies log consistency, not
historical process exits. `work/verification.md` records the eight zero exits.
The prepared recovery loop executes actual F, independently solves the graph,
executes G, and checks exact source optimality. The retained additional Verify
log reports 12 inputs and 33 recoveries. Its independent implementation and
the depth-repair evidence remain relevant; I did not rerun those whole suites.

Limits remain material: exhaustive source topology coverage stops at four
original leaves; larger cases are sampled through seven leaves. The 300
nonempty-target records cap enumeration at 128 optima; the 27 completely
enumerated records have empty targets. Formula/gadget diagnostics establish
their finite scopes only. None of these counts replaces the universal proof.

## Novelty judgment and primary-source audit

**Adequate provenance for rule completion; no claim of a new complexity
classification or established first discovery.** Searches and primary-source
retrievals below were performed on 2026-09-22 using the Codex web tool, with a
shell-curl fallback for the SAT paper. Queries covered MAAF/DFVS reductions,
hybridization-number exact optimization, SAT encodings, integer programming,
and rank formulations.

| Primary location checked | Consequence for this candidate |
|---|---|
| [Upstream issue 1047](https://github.com/CodingThrust/problem-reductions/issues/1047), “Reduction Algorithm,” “Example,” and labels | The edge-pair proposal asserts exactness without furnishing the needed audited proof. The quartet example claims four components; the current independent source check finds three including the added label. Its Wrong/IncompleteReduction labels are context, not the reason for rejecting its mathematical claim. |
| [Kelk et al., Cycle killer, arXiv:1112.5359v1](https://arxiv.org/html/1112.5359), §2; §4 Theorem 4, Lemma 7, construction and Theorem 5; §5 Theorem 6 | §2 matches the source convention. §4 optimizes splittings of a chain forest and has a factor-six loss against global hybridization optimum; exact solving of that restricted graph does not eliminate the loss. §5 is the opposite reduction direction. These are not the present exact rule. |
| [van Iersel et al., Approximation algorithms for nonbinary agreement forests](https://arxiv.org/html/1210.3211), Theorem 1 and §3.2, especially Lemma 11 and its concluding inequalities | Its weighted DFVS construction optimizes refinement of a supplied agreement forest. The final bound is d(c+3), again not arbitrary global source optimality from an exact DFVS solver. Nonbinary refinement conventions also require care when comparing domains. |
| [Bonet and St. John, Efficiently Calculating Evolutionary Tree Measures Using SAT](https://stjohn.github.io/research/sat6.pdf), §§3–4, printed pp. 6–8 | Polynomial threshold encodings, shared component memberships, conflicting rooted triples, and SAT-based exact search precede this work. Their encoding uses component membership and explicit ancestry/transitive-closure variables. Thus SAT encoding and triple exclusion are not new; the present monotone-rank compression and complete DFVS decoder are the narrower implementation contributions assessed here. |
| [Min (A)cyclic Feedback Vertex Sets and Min Ones Monotone 3-SAT](https://arxiv.org/html/1809.01998), §2 Claims 2–5 | Exact relationships between satisfying-assignment objectives and minimum FVS, including tightly bounded optimum values, are prior art. This paper does not itself instantiate the present forest rule; it further limits any broad novelty claim for the optimization-gadget method. |

There is also a general composition consequence, not a literature-search
discovery: a polynomial source-witness verifier can be encoded as SAT for each
of polynomially many objective thresholds, then converted to cover graphs and
bidirected graphs. Parallel thresholds and validation give the same all-optima
strategy. Hence bare existence of some polynomial exact rule is not a credible
new hardness/classification claim. The fixed question expressly accepts an
executable, proved reconstruction, so that observation does not trigger a stop
for this acceptance target.

The literature audit is bounded. It does not establish priority for the rank
lemma or the selector trick, exclude an equivalent decoder in all SAT/ILP
software, or exhaust subsequent literature. The attempted Wu–Wang author PDF
at `https://www.engr.uconn.edu/~ywu/Papers/ISBRA10WuWang.pdf` was unavailable
through the web tool; I make no theorem claim about its unseen contents. The
UPC repository initially returned 403 to the web tool; shell curl retrieved
its SAT paper successfully (`sat-paper.pdf`, with `sat-paper.txt` from
pdftotext), and the author-hosted version above was also read through the web
tool. These limits preclude a first-in-literature claim, not acceptance of the
audited implementation under the fixed rule-completion criterion.

## Significance and overhead judgment

**Sufficient for the fixed deliverable, modest beyond it.** The contribution is
a reproducible exact source-to-target rule with an arbitrary-optimum decoder,
explicit polynomial bounds, and independently tested source semantics. It
avoids fixing a particular forest whose refinements could exclude better
solutions. The unweighted bidirected target is exactly a vertex-cover instance;
no advantage specific to directed cycles is demonstrated. This does not imply
an approximation-preserving result, an FPT improvement, a small kernel, or a
better phylogenetic solver.

`rounds/006/overhead.txt` supports a substantial measured reduction against the
campaign's Round 004 baseline on its fixed records. At seven leaves, median
vertices fall from 77,799 to 15,267.5 and arcs from 254,150 to 60,440; the
largest recorded rank graph has 23,437 vertices, 96,142 arcs and 2,782,605 JSON
bytes. These remain large expansions for tiny trees. The equivalence evidence
reports unchanged explicit graphs after the iterative repair, so the graph
counts transfer. Single-run timings in that table belong to the prior recursive
implementation and do not benchmark the current code. No comparison to the
best published encodings or direct MAAF solvers, no optimal-overhead lower
bound, and no current end-to-end speed superiority is established. The user
does not require a minimum-overhead proof; these limitations do not block
advancement.

## Actual isolation and model route

The review ran in the Codex harness with the supplied GPT-6-based Codex model
identity. The exact backend model identifier/version and any parent routing
decision are not independently visible here. The developer instructions match
`.codex/agents/research-reviewer.toml`, which was read; that registration itself
sets no model field. I do not claim use of DSH's mounted research preset or a
different model from the proposer.

The effective permissions were `danger-full-access`, network enabled, approval
policy `never`: **no filesystem sandbox enforced the review-directory boundary**.
Write confinement and the prohibition on spawning agents were instructions
followed by this reviewer, not verified tool-denial or depth-cap mechanisms.
No agents were spawned. Candidate execution used subprocesses; source/target
oracles did not import the candidate. Candidate files, tests, reports, prior
evidence and unrelated harness deletions were left unchanged. All new artifacts
were written under this review directory, with bytecode writing disabled for
review Python execution. These mechanisms describe separation of work; they
are not evidence that a mathematical conclusion is correct.

Recommended next step: advance to manuscript/expert review, retaining the
limited novelty and overhead claims, and correct the local LCA accounting in
the next proof edit. No restart or new construction is required by this review.
