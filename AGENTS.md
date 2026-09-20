# Local research instructions

This repository is one AutoResearch campaign for the fixed question in
`campaigns/acyclic-agreement-forest-feedback-vertex-set/question.md`. It is not
the website board: the board repository's website-only `AGENTS.md` does not apply
here.

Run the workflow from [research-session](.agents/skills/research-session/SKILL.md)
and read the shared [reduction contract](research/reduction.md). Load Prepare,
Propose, Verify, Review, Write and Formalize only when their responsibility is
needed. Keep the question and acceptance criteria fixed; a different theorem is a
new campaign.

- Write all repository content in English.
- Keep algorithms, proofs, tests, round records and reviews under
  `campaigns/acyclic-agreement-forest-feedback-vertex-set/`. Follow
  [research/repository.md](research/repository.md) for layout, artifact
  ownership and the Git policy: create no research artifact before the initial
  commit, commit the testing foundation before constructing a candidate, commit
  every completed round including failures, and never rewrite or fabricate
  history.
- This question fixes **exact optimization endpoints on both sides**. A valid
  target output is a *globally minimum-cardinality* directed feedback vertex set,
  and a valid source output is a *minimum-component* acyclic agreement forest.
  Recovery must hold for every such target output, including ties; a feasible but
  non-optimal forest, or one recovered only from a particular minimum feedback
  vertex set, does not satisfy the contract.
- Both output sets are nonempty on the admitted domain (the all-singleton
  partition is always an acyclic agreement forest; deleting every vertex always
  leaves an acyclic digraph), so no NO-SOLUTION output is admitted on either
  side.
- Derive oracles from the problem definitions and never let an oracle import the
  candidate. A missing solver is reported as pending, never replaced by an LLM
  oracle.
- Use finite instance or search-family bounds. Never add solver, subprocess,
  shell or wrapper timeouts, and never add wall-clock limits to a check.
- A harness-imposed limit that kills a run is an execution failure to record,
  not an oracle answer.
- Missing capability is reported as pending work, never as a successful check.
- Reusable findings go in `research/experience/`. The board repository keeps a
  local, uncommitted cross-question collection at
  `/Users/xiweipan/Codes/autoresearch-gadgets/research/experience/entries/`:
  read it there, do not copy it into this repository, and treat presence there
  as no evidence.

## Harness

The reviewer registration for DSH is [harness/dsh](harness/dsh/README.md); the
independent reviewer is the `research_reviewer` child of the mounted `research`
agent preset. The preset is installed at `$DSH_HOME/.agent-presets/research`, but
it is only mounted for a session that **starts** on the `research` preset — a
session cannot change preset after it has produced anything. The session that
created this repository ran the `standard` preset, so no review has used the
registered route yet; the first campaign session must be started on `research`.
Codex would instead read `.codex/agents/research-reviewer.toml`.

Network note: `web_fetch` reached `https://example.com/` with HTTP 200 on
2026-09-21 from the launching session, so primary-source fetching through the
harness is available; shell `curl` remains a fallback and the method used must be
recorded.
