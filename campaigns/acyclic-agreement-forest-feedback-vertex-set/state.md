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

No round has been opened. The budget is 3; used 0, remaining 3; distinct
mechanisms attempted 0. A round starts when a construction hypothesis, proof
strategy or standalone literature investigation is committed to; preparation and
routine implementation stay with the work they serve.

## Artifacts

- `question.md` fixed; no `work/`, `rounds/`, `reviews/` or `formal/` content
  exists yet. No `pyproject.toml` or `uv.lock` yet; they are added when the testing
  foundation first uses Python.
- Copied into this repository with relative paths intact: `.agents/skills/`
  (research skills and `find-open-problems`), `research/` specifications except
  the board-local `research/experience/entries/` collection, `harness/` and
  `.codex/agents/research-reviewer.toml`.

## Checks

None. Nothing has been built or executed; the initial commit precedes any test,
construction search or proof attempt, as the repository standard requires.

## Review

None. No candidate exists, and the launching session could not mount the
registered independent reviewer.

## Next action

Continue with the [Prepare](../../.agents/skills/research-prepare/SKILL.md) stage
in a session whose workspace is this repository and which is started on the
`research` agent preset: read `README.md`, `AGENTS.md` and
`campaigns/acyclic-agreement-forest-feedback-vertex-set/{question,state}.md`, fix
the JSON encodings for both endpoints in `work/contract.md`, and build
self-tested, independent oracles for minimum-component acyclic agreement forests
and minimum-cardinality directed feedback vertex sets before constructing any
candidate.
