# Round 001 — cited-construction exactness audit

## Plan

This round is a standalone literature investigation. Its finite scope is the
upstream issue 1047, the primary source cited by that issue, and the exact
construction or decoder statements those two sources reference. The mechanism
under audit is the cited relationship between agreement forests and directed
feedback vertex sets as a possible exact rule for the fixed endpoint pair.

The first discriminating check is: does the cited material define executable
polynomial-time maps `F` and `G` such that every globally minimum feedback vertex
set of `F(x)` recovers a globally minimum acyclic agreement forest, including
ties? Evidence of that statement would justify reusing the construction as the
first candidate. Evidence that the material only proves an approximation,
one-way objective relation, or recovery from a selected witness would exclude
that reuse and leave a new exact construction as the next mechanism.

The scope is bounded by the three source artifacts above and their theorem,
definition and algorithm locations. No source solver, candidate implementation
or runtime timeout is used. The prepared source and target oracles remain
unchanged.

## Evidence and diagnosis

Audit date: 2026-09-21. The issue and primary source were fetched with the
Codex web tool.

- Upstream issue [#1047](https://github.com/CodingThrust/problem-reductions/issues/1047)
  is labeled `IncompleteReduction` and `Wrong`. Its prose claims an edge-pair
  auxiliary graph, a minimum DFVS of size 3 on the quartet swap, and a lifted
  forest with four components. That worked example conflicts with the fixed
  campaign endpoint: the prepared source oracle finds a three-component
  optimum for the augmented-root contract, and the issue supplies no proof of
  the claimed lifting statement.
- The primary paper is [arXiv:1112.5359](https://arxiv.org/html/1112.5359).
  Section 2 defines MAAF using the augmented root label `ρ`, restrictions
  `T|L_i`, vertex-disjoint minimal subtrees, and the inheritance graph. This
  matches the source-side structure audited during Prepare.
- Section 4, Theorem 4 states an approximation result from weighted DFVS to
  MinimumHybridization with factor 6. The construction uses a chain forest and
  a weighted graph whose FVSs correspond to `B_T`-splittings, not to all MAAF
  forests.
- Section 4, Lemma 7 proves only
  `OPT(B_T-splitting) < 6 h(T,T')`. The proof constructs a restricted
  splitting by taking the union of cuts from an optimum forest and the chain
  forest; it does not prove equality with the global MAAF optimum. Theorem 5
  expands bounded weights to unweighted DFVS while preserving that
  approximation route.
- Section 5, Theorem 6 is the reverse approximation-preserving direction,
  from DFVS to MAAF, so it does not supply the requested source-to-target rule.

The first discriminating check therefore fails for exact reuse: the cited
material does not provide a solver-free `G` that recovers a globally minimum
source forest from every globally minimum target FVS. It provides a restricted
family and approximation guarantees. The issue’s claimed construction is not a
candidate for this fixed contract.

## Next action

Extract the restricted-splitting obstruction as reusable experience, then open
Round 2 around a materially different exact construction mechanism. The next
round must address how arbitrary optimal forests and all target ties are
represented without assuming the chain-forest normal form.

## Experience extraction

Created `research/experience/cycle-killer-restricted-splitting.md`, linking this
round and the primary theorem locations. It records that the Cycle Killer graph
is evidence for restricted splitting and approximation, not exact global
solution recovery.
