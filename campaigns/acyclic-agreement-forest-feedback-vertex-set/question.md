---
status: open
openness: rule-completion
difficulty: uncertain
importance: unassessed
tags:
  - maximum-acyclic-agreement-forest
  - directed-feedback-vertex-set
  - phylogenetics
  - exact-optimization-endpoints
  - rule-reconstruction
last-literature-check: 2026-09-18
---

# Research question — Maximum Acyclic Agreement Forest → Minimum Directed Feedback Vertex Set

## Exact question and acceptance target

- Primary origin: board record `acyclic-agreement-forest-feedback-vertex-set.json`
  on the Open Question Board (`Construction open`), citing upstream issue
  <https://github.com/CodingThrust/problem-reductions/issues/1047>. The board's
  acceptance target is a complete, reproducible rule; no new complexity
  classification is claimed.
- Mathematical objects, definitions, complete domain, and hypotheses. The board
  record fixes them as follows, and they are quoted here rather than restated:
  - Source Π_A = Maximum Acyclic Agreement Forest. I_A: two rooted binary
    phylogenetic trees on the same labeled leaves, with an additional root label.
    S_A(x): the acyclic agreement forests with the fewest components. A forest is
    a partition of the labels into leaf blocks; the restrictions to each leaf
    block must agree in both trees, their connecting subtrees must be
    vertex-disjoint within each tree, and the union of the two component-ancestry
    relations must be acyclic. "All finite combinatorial structures are explicit
    and numerical data use binary encoding."
  - Target Π_B = Minimum Directed Feedback Vertex Set. I_B: an explicit digraph.
    S_B(x): the vertex sets of globally minimum cardinality whose deletion leaves
    an acyclic digraph. "The empty set is valid and optimal for an acyclic input."
- Fully quantified statement to prove: there exist deterministic polynomial-time
  maps F and G with F(x) ∈ I_B for every x ∈ I_A and G(x, y) ∈ S_A(x) for every
  y ∈ S_B(F(x)). Both endpoints are **optimization** endpoints, so S_A(x) is the
  set of all minimum-component acyclic agreement forests and S_B is the set of all
  minimum-cardinality feedback vertex sets, ties included.
- Total domain and no-solution semantics: the board record for this pair lists
  optimization endpoints only, with no thresholded feasibility endpoint, so no
  NO-SOLUTION output is admitted on either side. This is consistent because both
  sets are nonempty for every legal input: the all-singleton partition is always
  an acyclic agreement forest, and deleting every vertex always leaves an acyclic
  digraph.
- Does a disproof qualify? No. A disproof would have to show that no such rule
  exists.
- Required deterministic construction or algorithm: F and G implemented over a
  fixed JSON encoding, with recovery available as a separate extraction mode, and
  neither map calling a solver, using randomness or consulting an LLM.
- Worst-case time, representation, and encoding bounds: polynomial time and
  output bit size for F in |x|, and for G in |x| + |y|, measured on the binary
  input encoding, so every constructed number must have polynomially many bits.
- Source and target problems (I, S), encodings and no-solution semantics: as
  above; the exact JSON encodings are fixed in `work/contract.md` during Prepare.
- Forward map F and target legality to prove: F emits a legal target instance —
  an explicit digraph with an explicit vertex set and arc list — for every legal
  source instance.
- Output sets S_A/S_B and recovery G: prove G(x, y) ∈ S_A(x) for **every**
  globally minimum feedback vertex set y of F(x), including ones the construction
  did not "intend", and prove the optimality of the recovered forest rather than
  only its feasibility.
- Valid output restrictions, totality, and composition obligations: degenerate
  source instances (one leaf, two leaves, identical trees), instances whose
  optimal forest has one component, and instances whose optimal feedback vertex
  set is empty must all be covered explicitly.
- New complexity-theoretic contribution beyond applicable known reductions: none
  claimed at launch. The board asks for a complete exact rule, and the record does
  not assume that the cited construction already contains one.

## Known results and remaining gap

| Primary result | Exact hypotheses | Conclusion/bounds | Why it does not settle the target |
|---|---|---|---|
| Board record `acyclic-agreement-forest-feedback-vertex-set.json`, literature check 2026-09-18 | The endpoint pair above, fixed as in the record | Records that the cited proposal establishes only an **approximation-preserving** relationship between these problems | An approximation-preserving relationship does not supply the exact solution-recovery contract: it says nothing about decoding an *optimal* forest from *every* minimum feedback vertex set |
| Upstream issue <https://github.com/CodingThrust/problem-reductions/issues/1047> | The same endpoint pair | Cited by the board record as the origin of the proposed rule; the record states the exact endpoint semantics and the remaining deliverable | The record itself states that the exact rule's "existence in the cited construction is not assumed"; the issue has not been read in this campaign and must be audited in Prepare or the first literature round |

- Strongest applicable positive and negative results: the approximation-preserving
  relationship recorded above is the positive lead; no negative result is recorded
  by the board beyond the fact that no complete exact rule is present.
- General theorem or composition consequences checked: none yet.
- Exact gap and mathematical significance: a complete exact rule (F, G) for this
  endpoint pair is missing, and the recorded approximation-preserving relationship
  is insufficient in exactly the step the contract measures — recovering a
  globally optimal source solution from an arbitrary optimal target solution.
- Weakest result meeting acceptance: executable F and G, a general proof of target
  legality and of recovery optimality for every valid target output, and passing
  independent checks that include alternate optimal target solutions. Partial
  results that would not suffice: a rule whose recovery is only feasible (not
  optimal), or one verified only against target optima produced by the candidate's
  own reasoning.

## Openness evidence

| Search date and query | Primary URL and version | Theorem/page | Effect on target |
|---|---|---|---|
| 2026-09-18 (board import inventory review) | Board record `acyclic-agreement-forest-feedback-vertex-set.json`; upstream issue 1047 | The record fixes the endpoints, states the remaining deliverable and records the approximation-preserving relationship | Establishes the rule-completion gap as recorded on the board |

- Equivalent formulations and synonymous statements checked: not yet; the board
  record's own phrasing is treated as the fixed statement.
- Historical progress, latest versions, and follow-ups checked: only the board's
  dated import review (2026-09-18). Issue 1047 has not been read in this campaign.
- Failed approaches and applicable lower bounds: none recorded in the board
  record for this pair.
- Evidence of present openness; unavailable sources and coverage limits: the board
  record states the rule is open and that the cited construction's exactness is not
  assumed, but its own `coverage` field says the primary proofs "have not been
  independently re-audited" and that availability of a complete reconstruction
  elsewhere "remains unassessed". Treating the question as open is therefore based
  on the board's review, not on an independent literature audit. Reading issue 1047
  and the phylogenetic literature it cites is an open obligation.

## Proof route and initial investigation

No construction route has been selected and no attempt has been executed. This
document is committed before Prepare, as the repository standard requires. The
following is the recorded starting position, not a hypothesis that has been
tested.

- Existing lemmas or constructions to build on: the board record's
  approximation-preserving relationship is the only recorded lead. Its exact
  statement, hypotheses and direction must be read from the cited source before it
  can be used, because an approximation-preserving map does not by itself imply
  the exact recovery obligation here.
- Focused missing argument (untested): the step that must be supplied is exactness
  — for an arbitrary globally minimum feedback vertex set of the constructed
  digraph, the decoded forest must have the minimum possible number of components,
  not merely a number within some factor. The board record's difficulty note names
  the two concrete risks: recovering an optimal forest "needs more than an
  approximation guarantee", and "a graph formed from one chosen agreement forest
  may lose globally better source solutions".
- Candidate encoding structures to fix during Prepare: how a pair of rooted binary
  phylogenetic trees, its label set, an agreement forest, and a digraph with an
  explicit vertex and arc list are written as JSON, including bit-length bounds for
  any numerical field.
- Failure modes; observations that would refute a proposed approach: a minimum
  feedback vertex set whose recovery yields a forest with more components than the
  source optimum; a construction whose digraph encodes one chosen forest and
  thereby excludes an optimal source solution; a recovery map that is well defined
  only for target optima of a special form.
- Bounded experiment or proof exercise, tools, and time/compute budget: during
  Prepare, build independent oracles for both endpoints over small instances — an
  exhaustive enumeration of acyclic agreement forests, and a minimum-cardinality
  directed feedback vertex set computed by an independent exact method — plus
  injected and malformed fixtures, with all bounds finite and explicit. The first
  counted round tests the first candidate construction against those oracles
  exhaustively on small instances. No timeouts; bounds are declared in advance.
- Executed commands, actual results, and counterexamples: none.
- What those results establish and what they do not: —.
- Remaining route to a general proof and independent checking plan: fix the
  encodings and oracles in Prepare; construct F and G in Propose with a general
  proof of target legality, of optimality of the recovered forest for every valid
  target output, and of polynomial time and output bit size; verify independently
  including alternate optimal target solutions; then request independent review.

## Difficulty, importance, and reporting summary

| Dimension | Assessment | Evidence and uncertainty |
|---|---|---|
| Difficulty | uncertain | The board's difficulty field reads "Difficulty is uncertain" and names two specific risks (exactness beyond an approximation guarantee; loss of globally better source solutions when the digraph is built from one chosen forest). No construction attempt exists, so no difficulty estimate is supported here |
| Importance | unassessed | The board's importance field is the summary sentence itself: an exact structural reduction would connect phylogenetic agreement-forest optimization to directed cycle deletion and its solver ecosystem. No external novelty or significance audit has been performed |

- Why the difficulty and importance judgments support the proposed priority: they
  do not yet; this campaign was opened because the record matches the requested
  filter (`Construction open`, no submitted solution), not because of a ranking.
- Overlap with other candidates and the distinct contribution of this target: not
  assessed. Other `Construction open` records on the board also target minimum
  directed feedback vertex set from different sources; overlap must be checked
  before any novelty claim.
- Next bounded proof exercise and what its result would change: read issue 1047 and
  the cited source to establish what the recorded approximation-preserving
  relationship actually states. If it is only approximation-preserving, the exact
  rule must be derived independently, and the first candidate mechanism will be
  recorded as a round before it is executed.

## Screening decision

| Gate | Result | Evidence and reason |
|---|---|---|
| 1. Precise mathematical question | pass | Both (I, S) are fixed by the board record, including the optimization endpoints and the acyclicity condition on the forest |
| 2. Applicable known results | partial | Only the board's dated review is available in-repository; the cited source has not been read. This is an open obligation, not a settled gate |
| 3. Supported openness | pass, as recorded | The board's `openness` field states the exact rule is not assumed to exist in the cited construction, and its `coverage` field limits that claim to an import inventory review |
| 4. Mathematical significance | unresolved | The board's summary sentence is the only evidence; no independent significance audit has been done |
| 5. Plausible proof route | unresolved | No route has been selected; the recorded risks are explicit but no mechanism has been proposed or tested |
| 6. Bounded initial investigation | hold | Not executed: this record is committed before Prepare; the first counted round is the bounded probe |

Overall decision and first blocking gate: campaign opened under the user's
authorization to pick one `Construction open` rule and research it. Gates 2, 4 and
5 remain open obligations, to be addressed before or during the first rounds; Gate
6 is deliberately held until the initial commit exists.

## Research history

- 2026-09-21: campaign repository created under
  `~/Codes/reduction-zoo/acyclic-agreement-forest-feedback-vertex-set`, selected
  as the first `Construction open` board record with an empty `solutions` list in
  alphabetical order, after excluding slugs with an existing research repository.
  The launching session ran the DSH `standard` preset, so no independent review has
  occurred and the `research_reviewer` registration is only installed.
- Related problems, proof artifacts and reproducible checks: none yet.

## Campaign contract

- Fixed statement and qualifying positive outcome: a complete deterministic rule
  (F, G) for Maximum Acyclic Agreement Forest → Minimum Directed Feedback Vertex
  Set, with recovery of a minimum-component forest from every minimum-cardinality
  feedback vertex set. No negative outcome qualifies.
- Allowed approaches, tools, resource budget, and stopping conditions:
  deterministic construction with a general proof; Python with uv and a committed
  lockfile once Python is first used; exact oracles derived from the definitions
  (which must not import the candidate and must not be LLMs); an initial round
  budget of three, which the user may extend; stop conditions and early-exit
  obligations from the session skill.
- Required general proof and applicable construction/extraction bounds:
  polynomial worst-case time and output bit size for F in |x| and for G in
  |x| + |y|, with optimality of the recovered forest for every valid target output.
- Independent verification obligations and literature recheck: independent oracles
  and injected cases in Verify, including alternate optimal target solutions; an
  independent reviewer through the registered reviewer child in a session started
  on the `research` preset; and a re-audit of issue 1047 and the sources it cites.
- Record partial progress honestly; a different theorem needs a new campaign.

The target is a deterministic polynomial-time reduction under the
[shared contract](../../research/reduction.md), with forward instance
construction and deterministic polynomial-time recovery from any valid target
output. Production integration would require a mature result and separate
authorization.
