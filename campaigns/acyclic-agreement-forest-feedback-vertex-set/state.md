# Campaign state — Maximum Acyclic Agreement Forest → Minimum DFVS

## Current established result (2026-09-22)

Status: **ready_for_expert_review**. This is an agent assessment, not human
certification or publication acceptance. The exact fixed rule is implemented:
every globally minimum DFVS of the explicit target recovers a minimum-component
acyclic agreement forest. Both deterministic maps are polynomial-time and use
no solver. For m augmented labels, target vertices/arcs are O(m^4) and encoding
length is O(m^4 log m). No minimum-overhead or new complexity-classification
claim is made.

- [Executable maps](work/algorithm.py), unchanged since `25cab27`.
- [General proof](work/proof.md); local runtime accounting corrected at `5f3a30b`.
- [Complete verification](work/verification.md): 327 prepared records / 38,427
  recoveries, 12 additional inputs / 33 recoveries, and depth regressions.
- [Independent advance review](reviews/rank-threshold/review.md) and
  [focused follow-up](reviews/rank-threshold/follow-up.md): 47 targeted recovery
  calls pass; the sole nonblocking LCA accounting issue is resolved.
- [Eight-page manuscript](work/manuscript.pdf), [Typst source](work/manuscript.typ),
  and [page-by-page inspection](work/evidence/manuscript/inspection.md).

The user-requested Prepare restart rebuilt independent oracles against the
unchanged question before new construction. The original candidate remains
withdrawn: it and its source checkers used tree-node arc unions instead of
component ancestry. Internal-node renaming changed its answer on identical
trees. The claim that only solver capacity blocked it was false. Its files
remain in Git at `a056e65`, and the counterexample and failed rounds are retained.
The current rule uses the corrected partition semantics; see
[preparation](work/preparation.md).

## Authorization and budget

- 2026-09-22 continuation: user authorized up to **20 additional rounds**.
  New allocation used: 3 completed (004–006), remaining: 17. Historical 3
  retained; total allocation 23, total started 6. Five distinct mechanisms
  appear in the table (Round 003 was supporting verification). Completed Round
  006 combines rank thresholds, certified feasible upper bounds, and unit-gap
  covers; see `rounds/006/round.md`. Correctness and low graph overhead are both
  user priorities; no minimum-overhead claim is required or made.

- Original authorization: 2026-09-21, research this fixed question; default
  allocation 3 rounds. The historical record charged all three below.
- 2026-09-22: the user explicitly requested redoing the problem from Prepare.
  Definition auditing, oracle repair and preparation do not consume a discovery
  round. The foundation was committed at `cf9f979` before Round 004 began.
- Historical round counts are retained, not reset or retroactively merged.
  The third recorded round was target-verifier work, which the skill normally
  treats as supporting verification rather than a new mathematical mechanism.
  Historical distinct construction/literature scopes: 2. Prepare itself did
  not consume a discovery round.

## Capability probe (2026-09-22)

| Tool/capability | Actual version/provider | Status |
|---|---|---|
| Python | uv environment, 3.12.11 | verified by command |
| uv | 0.12.7 | verified by command |
| Z3 | 4.15.4, `z3-solver==4.15.4.0` in `uv.lock` | installed and exercised |
| OR-Tools / NetworkX | 9.15.6755 / 3.6.1, locked uv dependencies | installed; independent CP-SAT verifier / graph decomposition |
| Typst | 0.15.1 | eight-page paper compiled and visually inspected |
| Lean / Lake | 4.34.0 / 5.0.0 | executable verified |
| Mathlib | no campaign Lake project | pending; formalization not requested |
| External writing skill | `/Users/xiweipan/.codex/plugins/cache/sci-brain/sci-brain/0.5.0/skills/how-to-technical-writing/SKILL.md` | loaded before drafting and final language pass |
| Web | web tool read author-hosted PDF | available; lookup recorded in preparation |
| Reviewer | `research-reviewer` role exposed by spawn tool; `.codex/agents/research-reviewer.toml` exists | fresh registered child completed advance review and focused follow-up |

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
| 6 | Unit-gap guarded covers with feasible-forest threshold pruning | Full fixed 327-record suite, 12 independent inputs, graph-size comparison | Supported: complete checks, independent advance review, inspected manuscript | [006](rounds/006/round.md) |

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
See [verification](work/verification.md). The independent review supports the general all-input/all-optimum proof;
finite tests do not prove that quantifier. The reviewer additionally checked
all selected optimum rank projections and all 32 binary patterns at an
infeasible threshold on its quartet instance (47 recovery calls total).

## Experience and next action

Experience closeout for this restart: **3 created, 1 updated, 0 pending
extractions**. Entries created:

- [Component ancestry and node identifiers](../../research/experience/component-ancestry-and-node-identifiers.md).
- [Monotone ranks](../../research/experience/monotone-ranks-for-acyclic-forests.md).
- [Guarded threshold covers](../../research/experience/guarded-threshold-cover-gap.md).

The [earlier weighted CNF entry](../../research/experience/optimization-cnf-to-dfvs.md)
was updated to withdraw its invalid MAAF application. The historical
[Cycle Killer restriction](../../research/experience/cycle-killer-restricted-splitting.md)
was preserved. The two current mathematical entries are covered by independent
review; no entry's presence is itself evidence. No cross-question collection
was copied or published.

Measured seven-leaf median vertices fell from 77,799 (Round 004) to 15,267.5
(Round 006), on the same 16 inputs; median arcs fell from 254,150 to 60,440.
The graph-size data transfer exactly after the iterative repair. These remain
large graphs for small trees; there is no best-published-encoding comparison,
practical solver speed claim, or optimal-overhead lower bound.

Stop new discovery because the fixed rule-completion workflow is complete,
with 17 authorized rounds unused. Recommended next action: human expert review
of the proof and artifact. Further overhead improvement is an optional research
continuation; prospects are unknown (uncalibrated judgment), not an impossibility
claim. Lean/Mathlib formalization was not requested and remains unperformed.
No remote publication, board update, or production integration was authorized
or performed. Unrelated user deletions under `harness/` remain untouched.
