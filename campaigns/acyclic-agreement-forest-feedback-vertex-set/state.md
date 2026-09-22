# Campaign state — Maximum Acyclic Agreement Forest → Minimum DFVS

## Current established result (2026-09-22)

The user requested a restart from Prepare. Preparation has been rebuilt against
the unchanged definition in `question.md`. Its source oracle is cross-checked
against an independent exhaustive partition implementation on 327 stored inputs;
all minimum output sets agree. The target oracle is cross-checked against
exhaustive deletion on 631 digraphs. See [work/preparation.md](work/preparation.md).

**The previous candidate is withdrawn.** Both earlier source checkers and the
candidate encoded acyclicity of a union of tree-node arcs, rather than acyclicity
of the component ancestry graph. A change to internal node names in identical
trees changes the old oracle optimum from 1 to 2. The previous claim that only
solver capacity blocked completion is false. Old candidate/proof/verifier files
are preserved in Git at `a056e65` and removed from current `work/`; raw evidence
and rounds remain. No valid current reduction or proof is claimed.

## Authorization and budget

- 2026-09-22 continuation: user authorized up to **20 additional rounds**.
  New allocation used: 1 in progress (004), remaining: 19. Historical 3
  retained; total allocation 23, total started 4. Round 004 uses parallel
  thresholds and unweighted CNF covers; see `rounds/004/round.md`.

- Original authorization: 2026-09-21, research this fixed question; default
  allocation 3 rounds. The historical record charged all three below.
- 2026-09-22: the user explicitly requested redoing the problem from Prepare.
  Definition auditing, oracle repair and preparation do not consume a discovery
  round. The next construction must be planned after committing this foundation;
  no new construction is part of this Prepare record.
- Historical round counts are retained, not reset or retroactively merged.
  The third recorded round was target-verifier work, which the skill normally
  treats as supporting verification rather than a new mathematical mechanism.
  Historical distinct mathematical mechanisms: 2. No new mechanism attempted
  in this preparation restart.

## Capability probe (2026-09-22)

| Tool/capability | Actual version/provider | Status |
|---|---|---|
| Python | uv environment, 3.12.11 | verified by command |
| uv | 0.12.7 | verified by command |
| Z3 | 4.15.4, `z3-solver==4.15.4.0` in `uv.lock` | installed and exercised |
| Typst | 0.15.1 | executable verified; no manuscript yet |
| Lean / Lake | 4.34.0 / 5.0.0 | executable verified |
| Mathlib | no campaign Lake project | pending; formalization not requested |
| External writing skill | `/Users/xiweipan/.agents/skills/how-to-technical-writing/SKILL.md` | path found; load when writing |
| Web | web tool read author-hosted PDF | available; lookup recorded in preparation |
| Reviewer | `research-reviewer` role exposed by spawn tool; `.codex/agents/research-reviewer.toml` exists | registered, not invoked; no current complete candidate |

Old global Python/Z3 versions and the old harness availability claims are not
used for current reproduction. `uv sync --locked` supplies the tested dependency.

## Historical round table

These are the original attempts, with their evidence scope corrected by the
Prepare audit. They are not current correctness evidence.

| Round | Mechanism / standalone literature scope | First discriminating check | Outcome | Record |
|---|---|---|---|---|
| 1 | Cycle Killer exactness audit | Does the cited construction recover every globally optimal source solution? | Direct reuse rejected; approximation/restricted splitting only | [001](rounds/001/round.md) |
| 2 | Source CNF -> weighted cover -> clone DFVS | Do minimum assignments decode to valid minimum forests? | Source semantics invalidated by the 2026-09-22 audit; earlier target run also interrupted | [002](rounds/002/round.md) |
| 3 | Twin-group / CP-SAT target verification | Can an expanded target optimum be certified? | Execution failure; no optimum certificate, and source model now invalidated | [003](rounds/003/round.md) |

## Current preparation checks

- 327 source input records: all 236 ordered tree pairs through 4 leaves,
  80 seeded pairs on 5–7 leaves, 9 old named inputs, and 2 explicit regressions.
- 113,194 label partitions: direct predicate agrees with independent enumeration.
- 956 minimum source partitions: complete set agreement, including 177 input
  records with multiple optima; every optimum also survives node/child reordering
  and independent node renaming.
- 631 target digraphs: all 531 on 0–3 vertices including self-loops, plus 100
  seeded graphs on 4–8 vertices. All 766 minimum deletion sets agree.
- The actual subprocess candidate harness accepts a controlled correct decoder
  on both optima of a 2-cycle and rejects a decoder faulty only on the alternate
  optimum, malformed output, and process failure. These are checker tests,
  not reduction results.
- Retained evidence: [generation](work/evidence/prepare-restart/generate.txt),
  [self-test](work/evidence/prepare-restart/self-test.txt),
  [old-oracle counterexample](work/evidence/prepare-restart/audit-output.txt).

No actual new candidate has been tested. No independent candidate review has
occurred. Finite test coverage does not establish the universal reduction theorem.

## Experience and next action

The existing CNF-to-DFVS entry has been corrected to retract its former MAAF
application. One new entry records the concrete failure of node-id-dependent
ancestry checking. This restart creates 1 experience entry and updates 1; no
entry is pending promotion or used as evidence by its mere presence.

After the preparation commit, the next responsibility is Propose using the
label-partition contract and the full prepared candidate suite. The source model
must represent connecting-subtree disjointness and **component** ancestry. Any
candidate must pass the whole actual-target/recovery loop, including alternate
optimal target outputs, before independent review.
