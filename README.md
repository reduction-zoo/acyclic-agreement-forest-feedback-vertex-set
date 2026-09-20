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

Open; no construction attempt has been made. This repository currently contains
only the fixed question, the campaign state and the copied skills and
specifications. Nothing here is a correctness, novelty or verification result.

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

No Python project exists yet; `pyproject.toml` and `uv.lock` are added when the
testing foundation first uses Python, after which every command runs as:

```sh
uv sync --locked
uv run --locked python check.py --self-test
uv run --locked python check.py --candidate algorithm.py
```

The tool versions this machine actually provides are recorded in the capability
probe in `state.md`. Run the campaign from a session whose workspace is this
repository, started on the `research` agent preset so that the registered
independent reviewer (`research_reviewer`) is mounted; the launching session that
selected the question from the board ran the `standard` preset and could only
leave the registration installed.
