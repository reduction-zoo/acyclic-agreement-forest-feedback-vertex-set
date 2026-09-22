# Maximum Acyclic Agreement Forest → Minimum Directed Feedback Vertex Set

**Status: ready for expert review.** This repository provides deterministic
polynomial-time maps `F` and `G`: every globally minimum DFVS of the explicit
target graph recovers a minimum-component acyclic agreement forest, including
all target ties. This is an agent-reviewed rule reconstruction, not human
certification or a claim of a new complexity classification.

- [Manuscript PDF](campaigns/acyclic-agreement-forest-feedback-vertex-set/work/manuscript.pdf) and [native Typst source](campaigns/acyclic-agreement-forest-feedback-vertex-set/work/manuscript.typ).
- [Executable maps](campaigns/acyclic-agreement-forest-feedback-vertex-set/work/algorithm.py) and [general proof](campaigns/acyclic-agreement-forest-feedback-vertex-set/work/proof.md).
- [Independent advance review](campaigns/acyclic-agreement-forest-feedback-vertex-set/reviews/rank-threshold/review.md) and [focused follow-up](campaigns/acyclic-agreement-forest-feedback-vertex-set/reviews/rank-threshold/follow-up.md).
- [Preparation](campaigns/acyclic-agreement-forest-feedback-vertex-set/work/preparation.md), [verification](campaigns/acyclic-agreement-forest-feedback-vertex-set/work/verification.md), and [PDF inspection](campaigns/acyclic-agreement-forest-feedback-vertex-set/work/evidence/manuscript/inspection.md).
- [Fixed question](campaigns/acyclic-agreement-forest-feedback-vertex-set/question.md), [state and budget](campaigns/acyclic-agreement-forest-feedback-vertex-set/state.md), and [Round 006](campaigns/acyclic-agreement-forest-feedback-vertex-set/rounds/006/round.md).

## Result and overhead

Monotone ranks encode forest components and their ancestral order. Guarded
threshold formulas become unweighted bidirected cover graphs; a directly
validated feasible forest prunes the threshold range. Both maps use only the
Python standard library and call no solver.

For `m` augmented labels the target has O(m^4) vertices/arcs and O(m^4 log m)
encoding bits. On the fixed seven-leaf sample, median vertices fell from 77,799
to 15,267.5 and median arcs from 254,150 to 60,440 against the campaign's
component-slot baseline. These are still large expansions of small trees.
No minimum-overhead bound, best-published-encoding comparison or practical
solver speed advantage is claimed.

## Evidence and limits

The final maps pass all 327 prepared input records and 38,427 minimum-target
recoveries. The 300 nonempty targets cap enumeration at 128 outputs; the 27
empty targets are exhaustively checked. Additional independent Verify passes
12 records and 33 recoveries. The reviewer adds 47 targeted recovery calls,
including complete selected-rank projections and forced infeasible-threshold
patterns. Iterative traversal also passes a 1,200-leaf depth regression.

Source oracles agree on 113,194 partition predicates and 956 minimum forests;
target oracles agree on 766 minimum sets across 631 tiny graphs. Exhaustive
tree-pair coverage stops at four original leaves; larger inputs are sampled
through seven. Finite tests do not replace the universal proof. No Lean
formalization is claimed. The eight-page PDF has been compiled and inspected.

## Reproduction

From the repository root:

```sh
uv sync --locked --python 3.12.11
cd campaigns/acyclic-agreement-forest-feedback-vertex-set/work
uv run --locked python check.py --self-test
uv run --locked python check.py --candidate algorithm.py
uv run --locked python verify.py --candidate algorithm.py
uv run --locked python ../rounds/006/reproduce_modes.py
uv run --locked python ../rounds/006/deep_tree_check.py
typst compile manuscript.typ manuscript.pdf
```

The [JSON contract](campaigns/acyclic-agreement-forest-feedback-vertex-set/work/contract.md)
specifies inputs and outputs. `algorithm.py` performs F; `algorithm.py --extract`
performs G on an object containing `source` and `target_solution`. The reproduction
script independently solves an actual emitted graph and exercises both modes.
The lockfile supplies the tested oracle dependencies. No solver or subprocess
timeout is used.

## Research record

The user-requested Prepare restart found a source-definition error in the old
candidate, which is withdrawn and retained in Git at `a056e65`. The corrected
foundation was committed before constructing the current rule. Failed and
interrupted rounds remain in the record. Three of the twenty newly authorized
rounds were used, with seventeen unused; including history, six rounds were
charged and five distinct construction/literature mechanisms were attempted.

The workflow is [research-session](.agents/skills/research-session/SKILL.md)
under the [reduction contract](research/reduction.md) and
[repository standard](research/repository.md). Research artifacts stay under
the campaign directory; reusable findings are in [research/experience](research/experience/).
No board update, publication, or production integration has been performed.
