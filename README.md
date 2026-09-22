# Maximum Acyclic Agreement Forest → Minimum Directed Feedback Vertex Set

An independent AutoResearch campaign for one fixed reduction rule: reconstruct,
prove and independently verify deterministic polynomial-time maps `F` and `G`
between the maximum acyclic agreement forest problem on two rooted binary
phylogenetic trees and minimum directed feedback vertex set on an explicit
digraph.

- Fixed question and acceptance target:
  [campaigns/acyclic-agreement-forest-feedback-vertex-set/question.md](campaigns/acyclic-agreement-forest-feedback-vertex-set/question.md)
- Current progress, budget, capability probe and round table:
  [campaigns/acyclic-agreement-forest-feedback-vertex-set/state.md](campaigns/acyclic-agreement-forest-feedback-vertex-set/state.md)
- Workflow: [research-session](.agents/skills/research-session/SKILL.md) over the
  [reduction contract](research/reduction.md); repository layout and Git policy in
  [research/repository.md](research/repository.md)
- Provenance: the board record
  `acyclic-agreement-forest-feedback-vertex-set.json` in
  `/Users/xiweipan/Codes/autoresearch-gadgets/website/questions/`, which cites
  upstream issue <https://github.com/CodingThrust/problem-reductions/issues/1047>

## Why this target

The board lists this endpoint pair under `Construction open` with no submitted
solution: an exact structural reduction would connect phylogenetic
agreement-forest optimization to directed cycle deletion and its solver
ecosystem. The cited proposal records an approximation-preserving relationship,
which does **not** establish the exact solution-recovery contract requested here,
so the existence of a complete exact rule in the cited construction is not
assumed. The deliverable is a complete, reproducible rule — every globally
minimum directed feedback vertex set of the constructed instance must decode to a
globally minimum acyclic agreement forest of the source, ties included.

## Status

Prepare was rebuilt on 2026-09-22 after a reproducible source-definition error
invalidated the former candidate and its checker evidence. The replacement
rank-threshold candidate has a general proof; full target verification is in
progress and independent review is pending. The new foundation checks 327 source inputs and 631
target digraphs against independent exhaustive references, including all minimum
outputs in those finite families. See the [preparation report](campaigns/acyclic-agreement-forest-feedback-vertex-set/work/preparation.md).
The current [proof](campaigns/acyclic-agreement-forest-feedback-vertex-set/work/proof.md)
and [verification report](campaigns/acyclic-agreement-forest-feedback-vertex-set/work/verification.md)
distinguish the universal theorem from finite evidence. The construction emits
O(m^4) vertices/arcs for m augmented labels and uses no solver in either map.

## Layout

| Path | Contents |
|---|---|
| `campaigns/acyclic-agreement-forest-feedback-vertex-set/question.md` | Fixed target, definitions, literature evidence, screening gates, campaign contract |
| `campaigns/acyclic-agreement-forest-feedback-vertex-set/state.md` | Claim, obligations, capability probe, round table, budget, next action |
| `campaigns/acyclic-agreement-forest-feedback-vertex-set/work/` | Current contract, cases, checkers, algorithm, proof and manuscript |
| `campaigns/acyclic-agreement-forest-feedback-vertex-set/rounds/` | One record per round with its scripts and retained evidence |
| `campaigns/acyclic-agreement-forest-feedback-vertex-set/reviews/` | Independent reviews and their checks |
| `research/experience/` | Reusable findings from this campaign |
| `harness/`, `.codex/`, `.agents/skills/` | Harness reviewer registration, reviewer configuration and the research skills |

## Reproduction

From the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/acyclic-agreement-forest-feedback-vertex-set/work/check.py --self-test
```

The dataset generator, retained counterexample and finite coverage are documented
in `work/preparation.md`. The withdrawn candidate and proof remain in Git at
`a056e65`; their old test results do not establish the fixed source predicate.
