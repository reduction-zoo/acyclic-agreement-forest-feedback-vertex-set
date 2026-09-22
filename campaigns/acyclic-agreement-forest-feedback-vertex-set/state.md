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
and rounds remain. The replacement candidate at `25cab27` has a general rank-characterization proof;
the full actual-target suite now passes. Independent review and writing remain
pending, so this is not yet ready for expert review.

## Authorization and budget

- 2026-09-22 continuation: user authorized up to **20 additional rounds**.
  New allocation used: 3 started (004–006), remaining: 17. Historical 3
  retained; total allocation 23, total started 6. Five distinct mechanisms
  appear in the table (Round 003 was supporting verification). Current Round
  006 combines rank thresholds, certified feasible upper bounds, and unit-gap
  covers; see `rounds/006/round.md`. Correctness and low graph overhead are both
  user priorities; no minimum-overhead claim is required or made.

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
| OR-Tools / NetworkX | 9.15.6755 / 3.6.1, locked uv dependencies | installed; independent CP-SAT verifier / graph decomposition |
| Typst | 0.15.1 | executable verified; no manuscript yet |
| Lean / Lake | 4.34.0 / 5.0.0 | executable verified |
| Mathlib | no campaign Lake project | pending; formalization not requested |
| External writing skill | `/Users/xiweipan/.agents/skills/how-to-technical-writing/SKILL.md` | path found; load when writing |
| Web | web tool read author-hosted PDF | available; lookup recorded in preparation |
| Reviewer | `research-reviewer` role exposed by spawn tool; `.codex/agents/research-reviewer.toml` exists | registered, not invoked; candidate checks pending |

Old global Python/Z3 versions and the old harness availability claims are not
used for current reproduction. `uv sync --locked` supplies the tested dependency.

## Historical round table

Rounds 001–003 are historical attempts, with their evidence scope corrected by
the Prepare audit. Later rounds use the rebuilt independent foundation.

| Round | Mechanism / standalone literature scope | First discriminating check | Outcome | Record |
|---|---|---|---|---|
| 1 | Cycle Killer exactness audit | Does the cited construction recover every globally optimal source solution? | Direct reuse rejected; approximation/restricted splitting only | [001](rounds/001/round.md) |
| 2 | Source CNF -> weighted cover -> clone DFVS | Do minimum assignments decode to valid minimum forests? | Source semantics invalidated by the 2026-09-22 audit; earlier target run also interrupted | [002](rounds/002/round.md) |
| 3 | Twin-group / CP-SAT target verification | Can an expanded target optimum be certified? | Execution failure; no optimum certificate, and source model now invalidated | [003](rounds/003/round.md) |
| 4 | Canonical component-slot CNF and parallel unweighted threshold covers | Independent source thresholds followed by actual target recovery | Inconclusive: local formulas passed, full target runs interrupted | [004](rounds/004/round.md) |
| 5 | Monotone node ranks replace component slots, reducing graph order | All 1,759 source thresholds and actual target recovery | Inconclusive: local formulas passed; only 22 prepared records completed | [005](rounds/005/round.md) |
| 6 | Unit-gap guarded covers with feasible-forest threshold pruning | Full fixed 327-record suite, 12 independent inputs, graph-size comparison | Supported by proof and all prepared/additional checks; review pending | [006](rounds/006/round.md) |

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

The current candidate at `25cab27` passes all 327 prepared records and 38,427
minimum-target recoveries; 300 records were capped at 128 outputs, and 27 empty
targets were exhaustively checked. All eight process exits and their exact
case-name union passed. Independent Verify passed 12 records and 33 recoveries.
Both maps also pass identical-tree depth regressions at 1, 2 and 1,200 leaves.
See [verification](work/verification.md). The general all-input/all-optimum claim
still requires independent review; finite tests do not prove that quantifier.

## Experience and next action

The existing CNF-to-DFVS entry has been corrected to retract its former MAAF
application. One new entry records the concrete failure of node-id-dependent
ancestry checking. This restart creates 3 experience entries and updates 1. The rank and guarded-cover
entries are awaiting independent review; presence alone is not evidence.

Request a fresh registered review of F, G, the general proof, novelty and significance.
The current proof gives O(m^4) target vertices/arcs and O(m^4 log m) bits.
Measured seven-leaf median vertices fell from 77,799 (Round 004) to 15,267.5
(Round 006), on the same 16 inputs; median arcs fell from 254,150 to 60,440.
This comparison is not a proof of optimal overhead. Exact overhead and solver
coverage remain separate evidence obligations.
