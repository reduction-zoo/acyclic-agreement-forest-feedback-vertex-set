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

## Capability probe (2026-09-21)

| Capability | Actual version / provider | Path | Status |
|---|---|---|---|
| python3 | 3.14.7 | `/opt/homebrew/bin/python3` | ok |
| uv | 0.12.7 | `~/.local/bin/uv` | ok |
| git | 2.55.0, identity `Xiwei Pan <xiwei.pan@connect.hkust-gz.edu.cn>` | `/opt/homebrew/bin/git` | ok |
| z3 | 5.1.0 (binary and Python module) | `/opt/homebrew/bin/z3` | ok; candidate route for exact minimum-cardinality oracles |
| ortools | 9.15.6755 | Python module | ok; independent CP-SAT route |
| networkx / numpy / scipy / pulp | 3.6.1 / 2.5.3 / 1.17.1 / 3.3.0 | Python modules | ok |
| ripgrep | 15.2.0 | `/opt/homebrew/bin/rg` | ok |
| typst | 0.15.1 | `/opt/homebrew/bin/typst` | ok |
| PDF rasterizers | pdftoppm, pdftocairo, gs | `/opt/homebrew/bin` | ok |
| lean / lake | 4.34.0 / 5.0.0 | `~/.elan/bin` | ok |
| `how-to-technical-writing` skill | installed | `~/.agents/skills/how-to-technical-writing` | ok |
| `web_fetch` for primary sources | works (HTTP 200 to `https://example.com/`) | harness | ok; shell `curl` remains a fallback, and the method used must be recorded |
| Reviewer registration | DSH `research` preset installed with tool `research_reviewer` | `$DSH_HOME/.agent-presets/research`; copied at `harness/dsh/presets/research` | installed, **not mounted**: the launching session ran the `standard` preset (`$DSH_HOME/settings.yaml` has `agent-presets.default: standard`, and the session record reports `agentPreset: standard`). Only a session started on `research` mounts the reviewer |
| Formal proof comparator (Comparator / nanoda / lean4checker) | absent | — | pending; blocks final formal certification only, and no formal verification has been requested |

Re-probe when the environment changes and record the delta here rather than
relying on this table.

## Round table

| Round | Mechanism / standalone literature scope | First discriminating check | Outcome | Record |
|---|---|---|---|---|
| — | none started | — | — | — |

No research round has been opened. The budget is 3; used 0, remaining 3; distinct
mechanisms attempted 0. Prepare was executed and is **nearly complete**: both
oracles exist and run, seven source optima are established and validated, and two
instances are disputed between the cut search and the independent rSPR
cross-check. Per the
session skill, preparation and routine implementation stay with the work they
serve and do not consume a research round; the source-model investigation was
infrastructure, not a construction hypothesis. No candidate was constructed.

## Artifacts

- `question.md` fixed. `work/contract.md`, `work/cases.json`, `work/check.py`,
  `work/preparation.md` and `work/evidence/` now exist (Prepare, partial).
- No `rounds/`, `reviews/` or `formal/` content. No `pyproject.toml` or
  `uv.lock`: `check.py` uses only the standard library plus the environment's Z3,
  so no Python project has been created yet; add one when the foundation first
  needs a locked dependency.
- Copied into this repository with relative paths intact: `.agents/skills/`
  (research skills and `find-open-problems`), `research/` specifications except
  the board-local `research/experience/entries/` collection, `harness/` and
  `.codex/agents/research-reviewer.toml`.

## Checks

- `python3 check.py --self-test` — 143 checks, 0 failures; retained in
  `work/evidence/self-test-output.txt`. Seven source optima are stored and
  asserted; two are reported `PENDING` because they are disputed (see
  `work/preparation.md` section 4).
- Target-side oracle validated on 30 seeded random digraphs (exhaustive subset
  enumeration agrees with the Z3 decision oracle; every returned set passes the
  explicit Kahn check) and on the deliberate valid/invalid fixtures.
- `python3 evidence/rspr_reference.py` — independent rSPR distances; retained in
  `work/evidence/rspr-distances.txt`.
- No candidate exists, so `--candidate` has never been run.

## Review

None. No candidate exists, so there is nothing to review. The registered
independent reviewer is mounted in this session (the session runs the `research`
preset), and it will be used when a candidate and its proof exist.

## Next action

Finish [Prepare](../../.agents/skills/research-prepare/SKILL.md) before
constructing anything:

1. Settle the two disputed source optima recorded in `work/preparation.md`
   section 4: for `T1 = ((a,b),c)`, `T2 = ((a,c),b)` the oracle reports `|F| = 3`
   while the independent rSPR search reports `d_rSPR = 1`; the same identity
   fails on the five-leaf instance. Decide whether the oracle's rendering is
   still wrong there or whether the cross-check identity has a different form,
   then store the two missing optima in `work/cases.json`.
2. Repair `work/evidence/agreement_forest_reference.py` so that it is genuinely
   independent of the oracle rather than reusing its rendering idea.
3. Only then begin Propose. Per the session skill, preparation does not consume a
   research round: the round table stands at 0 used of 3, and no candidate has
   been constructed.
