# Component ancestry is invariant under internal node renaming

Tags: agreement forest, inheritance graph, oracle independence, metamorphic tests

## Claim and applicability

For acyclic agreement forests, the cycle predicate is on forest components:
connect two blocks when one connecting-subtree root is ancestral to the other
in either input tree. Taking the union of tree edges under a shared internal
node-id set computes a different predicate. Internal node ids are local encoding
details and must not affect forest feasibility or optimum. This observation
applies to the fixed rooted-tree problem, not to graph problems with an explicitly
specified cross-instance vertex identification.

## Evidence and status

Concrete counterexample, reproduced on 2026-09-22: two identically shaped,
identically leaf-labelled caterpillars have optimum 1. Interchanging two internal
ids in the second tree makes the old source oracle at `a056e65` report 2.
See [reproducer](../../campaigns/acyclic-agreement-forest-feedback-vertex-set/work/evidence/prepare-restart/reproduce_old.py)
and [definition audit](../../campaigns/acyclic-agreement-forest-feedback-vertex-set/work/preparation.md).
No independent agent review has yet assessed the rebuilt foundation.

## Consequence for search

Derive component relations from the original trees, then test their union on
block identities. Include independent node renaming in oracle tests. A second
implementation of the same wrong definition is not a definition-level check.
Nine old objective values agreeing did not detect this counterexample.

## Use history

- 2026-09-22: the Prepare restart replaced the incorrect source predicate and
  withdrew the old candidate. All 956 finite-family minimum partitions also
  validate after independent node renaming. No new reduction follows from this.
