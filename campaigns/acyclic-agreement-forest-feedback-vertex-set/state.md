# Campaign state — Maximum Acyclic Agreement Forest → Minimum Directed Feedback Vertex Set

## Fixed target

`campaigns/acyclic-agreement-forest-feedback-vertex-set/question.md` is
immutable. A different theorem is a new campaign.

## Authorization and budget

- Authorized by the user on 2026-09-21: pick one `Construction open` rule from the
  board and open a campaign under `~/Codes/reduction-zoo`.
- Research round budget: **3**, the session default disclosed because the user
  gave no number. Only the user extends it.
- Any harness continuation budget (for example a DSH goal round limit or an
  auto-continuation cap) is a guardrail and never the research round count; the
  round table below is authoritative.

## Capability probe (2026-09-21, re-probed at campaign resume)

| Capability | Actual version / provider | Path | Status |
|---|---|---|---|
| python3 | 3.14.7 | `/opt/homebrew/bin/python3` | ok |
| uv | 0.12.7 | `~/.local/bin/uv` | ok |
| git | 2.55.0, identity `Xiwei Pan <xiwei.pan@connect.hkust-gz.edu.cn>` | `/opt/homebrew/bin/git` | ok |
| z3 | 5.1.0 (binary and Python module) | `/opt/homebrew/bin/z3` | ok; candidate route for exact minimum-cardinality oracles |
| ortools | 9.15.6755 | Python module | ok; independent CP-SAT route |
| networkx / numpy / scipy / pulp | 3.6.1 / 2.5.3 / 1.17.1 / 3.3.0 | Python modules | ok |
| ripgrep | 15.2.0 | `/Users/xiweipan/.codex/packages/standalone/releases/0.155.1-aarch64-apple-darwin/codex-path/rg` | ok |
| typst | 0.15.1 | `/opt/homebrew/bin/typst` | ok |
| PDF rasterizers | pdftoppm, pdftocairo, gs | `/opt/homebrew/bin` | ok |
| lean / lake | 4.34.0 / 5.0.0 | `~/.elan/bin` | ok |
| `how-to-technical-writing` skill | installed | `~/.agents/skills/how-to-technical-writing` | ok |
| `web_fetch` for primary sources | works (HTTP 200 to `https://example.com/`) | harness | ok; shell `curl` remains a fallback, and the method used must be recorded |
| Reviewer registration | Codex `research-reviewer` child route; DSH preset also present in the repository | `.codex/agents/research-reviewer.toml`; `harness/dsh/presets/research` | Codex route available in this session; `DSH_HOME` and the DSH binary are unset/unavailable, so the DSH preset is not mounted |
| Formal proof comparator (Comparator / nanoda / lean4checker) | absent | — | pending; blocks final formal certification only, and no formal verification has been requested |

The current Codex web tool is available for primary-source lookup; the fetch
method and date will be recorded with any literature evidence. The formal proof
comparators remain pending and block only optional final formal certification.

## Round table

| Round | Mechanism / standalone literature scope | First discriminating check | Outcome | Record |
|---|---|---|---|---|
| 1 | Cycle Killer 2012 / upstream issue 1047 exactness audit | Does Section 4 provide exact global recovery from every minimum DFVS? | refuted for direct reuse: only restricted-splitting approximation guarantees | [rounds/001/round.md](rounds/001/round.md) |
| 2 | Exact MAAF verifier CNF -> weighted vertex cover -> unweighted DFVS clone groups | Do minimum formula assignments and the resulting cover outputs decode to minimum forests on every prepared case? | local exact formula checks supported the construction; full target harness was an execution failure after the first expanded graph, so target-side verification remains pending | [rounds/002/round.md](rounds/002/round.md) |

The budget is 3; used 2, remaining 1; distinct mechanisms attempted 2. Prepare
is complete: both endpoint oracles run, all nine source fixtures have
independently reproduced optima, and the source validator exercises malformed
and suboptimal outputs. Round 1 found no exact reuse of Cycle Killer. Round 2
left an executable candidate and a general proof, with independent target-side
verification pending after the positional target oracle did not finish its
first expanded graph before manual interruption.

## Artifacts

- `question.md` fixed. `work/contract.md`, `work/cases.json`, `work/check.py`,
  `work/preparation.md` and `work/evidence/` now contain the completed Prepare
  foundation.
- `work/algorithm.py` and `work/proof.md` contain the current candidate. Round
  002 retains the local formula-all-optima check and the interrupted target
  harness run. No `reviews/` or `formal/` content. No `pyproject.toml` or
  `uv.lock`: `check.py` uses only the standard library plus the environment's Z3,
  so no Python project has been created yet; add one when the foundation first
  needs a locked dependency.
- Copied into this repository with relative paths intact: `.agents/skills/`
  (research skills and `find-open-problems`), `research/` specifications except
  the board-local `research/experience/entries/` collection, `harness/` and
  `.codex/agents/research-reviewer.toml`.

## Checks

- `python3 check.py --self-test` — 236 checks, 0 failures; retained in
  `work/evidence/self-test-output.txt`. All nine source optima and their minimum
  cut-pair counts are stored and asserted.
- `python3 evidence/agreement_forest_reference.py` — independent source values
  and cut-pair counts agree on all nine fixtures; retained in
  `work/evidence/agreement-forest-reference-output.txt`.
- Target-side oracle validated on 30 seeded random digraphs (exhaustive subset
  enumeration agrees with the Z3 decision oracle; every returned set passes the
  explicit Kahn check) and on the deliberate valid/invalid fixtures.
- `python3 evidence/rspr_reference.py` — independent rSPR distances; retained in
  `work/evidence/rspr-distances.txt`.
- Candidate source-CNF verification: up to 16 minimum formula assignments per
  prepared case decoded to forests accepted by the independent validator; see
  [rounds/002/formula-optimum-check.txt](rounds/002/formula-optimum-check.txt).
- `python3 work/check.py --candidate work/algorithm.py` was started. It emitted
  a legal 1,118-vertex target for `one_leaf`, then its independent target
  oracle run was manually interrupted; see
  [rounds/002/candidate-harness-interruption.txt](rounds/002/candidate-harness-interruption.txt).

## Review

None. The candidate has not passed the independent target-side suite, so review
is premature. The Codex reviewer registration is available and will be used
after the candidate and its proof pass the relevant checks.

## Next action

Use the remaining round to reduce the target baseline or independently verify
the current clone graph, then rerun the fixed candidate harness. Do not treat
the interrupted target oracle as an oracle result. If no lower-baseline route is
found, preserve the candidate as incomplete rather than calling the question
solved; independent target verification and review remain required.
