# Cycle Killer graph captures restricted splittings

## Claim and applicability

The Cycle Killer construction of Kelk, van Iersel, Lekić, Linz, Scornavacca and
Stougie is an approximation-preserving route from MAAF or hybridization number
to weighted DFVS, then to unweighted DFVS. Its graph encodes splittings of a
chain forest, not an established exact encoding of every globally minimum
acyclic agreement forest. Apply this finding when considering the construction
as a source-to-target exact reduction with arbitrary target ties.

## Evidence and status

Confirmed by the primary source [arXiv:1112.5359](https://arxiv.org/html/1112.5359),
Section 4, Theorem 4, Theorem 5 and Lemma 7. Theorem 4 proves a factor-6
approximation through `B_T`-splittings; Lemma 7 bounds the best restricted
splitting by `< 6h` rather than identifying it with the global optimum. The
upstream [issue #1047](https://github.com/CodingThrust/problem-reductions/issues/1047)
states a stronger exact lifting claim without supplying that missing equality or
the required all-ties recovery proof. Status: confirmed literature finding;
independent review of the paper’s full proof is outside this entry.

Supporting record: [Round 001](../../campaigns/acyclic-agreement-forest-feedback-vertex-set/rounds/001/round.md).

## Consequence for search

Do not reuse the chain-forest graph as the exact candidate without a new proof
that every source optimum has the required normal form and that every minimum
target FVS decodes to one. A new mechanism must represent arbitrary source
component choices or prove a stronger canonicalization theorem.

## Use history

- 2026-09-21: created from Round 001; it ruled out direct exact reuse of the
  cited construction and set the next round’s design constraint.
