# Verification of the rank-threshold reduction

Candidate: `algorithm.py` and `proof.md` at commit `25cab27`.
Current independent checker implementation: `84f67a9`.
The source and target endpoints are exact optimization problems; both output
sets are nonempty. No source or target oracle imports the candidate.

## Prepared actual-target checks

The fixed `cases.json` has 327 records. Eight disjoint index-modulo-eight shards
execute the actual F subprocess, solve its explicit target graph independently,
and execute the actual G subprocess on up to 128 distinct minimum target outputs.
Every recovery is checked for feasibility and equality with the independently
computed minimum source component count. Enumeration truncation is reported
separately from input coverage.

Status: passed on the current candidate. All eight processes exited zero and
the exact case-name union equals the fixed dataset: **327 inputs, 38,427 distinct
minimum-target recoveries across those inputs**, 300 capped records and 27
completely enumerated empty-target records. Logs: `../rounds/006/iterative-shard-0.txt`
through `iterative-shard-7.txt`; union audit: `../rounds/006/coverage.txt`.
The previous recursive implementation passed all 327 records and 38,427
recoveries, with 300 capped records; those runs remain `shard-*.txt`.
It subsequently failed on a legal deep-tree input and was repaired. Prior
small-input success alone did not establish implementation totality.

## Additional independent implementation

`verify.py` imports neither `algorithm.py` nor `check.py`. The source reference
enumerates partitions with tree-path representations and transitive closure.
The target solver uses OR-Tools CP-SAT to maximize an independent set on the
actual bidirected graph, proving its optimum by consecutive exact cardinality
checks from a graph-derived packing bound. Complements are minimum covers and
therefore minimum DFVSs. Every selected deletion set covers every explicit arc.
Both maps are executed as subprocesses; recovered partitions must belong to
the reference's complete set of minimum source forests.

All 12 inputs passed, with 33 distinct minimum-target recoveries across those
inputs. The family uses one through five original leaves, independent internal
node namespaces, reversed labels/node lists, Unicode and punctuation in labels,
and an additional root label distinct from the ordinary leaf named rho. It tests
up to four target optima per input; empty targets have just one. See
`../rounds/006/iterative-verify.txt` for the current candidate.

## Oracle and gadget checks

- `../rounds/006/oracle-surplus.txt`: all 113,194 source partition predicates and
  all 956 minimum source partitions agree on 327 inputs; all 766 minimum
  deletion sets agree on 631 tiny directed graphs. Metamorphic, malformed,
  suboptimal, ancestry-cycle and alternate-target-decoder checks pass.
- `../rounds/006/gadget-check-surplus.txt`: the independent CP-SAT target oracle
  agrees with exhaustive subset enumeration on every optimum of all 75
  bidirected graphs with zero through three vertices, including loops.
- The same diagnostic checks actual guarded cover graphs for all 256 subsets
  of the eight nonempty clauses on two variables. Exhaustive truth assignments
  determine satisfiability independently; target optima are exactly L or L+1.
- The rank CNF is unchanged from Round 005: its independent source diagnostic
  checked all 1,759 thresholds across the 327 records and 815 decoded minimum
  rank assignments. This formula-only evidence is reused and is not counted as
  an actual-target recovery test.
- `../rounds/006/deep-tree-after.txt`: both F and G handle identical caterpillars
  with 1, 2 and 1,200 leaves, independently renamed internal nodes and reversed
  node/child orders. Expected target is empty and source optimum is one.
  Iterative traversal and delimited canonical restriction strings remove
  the previously observed fixed call-stack limit.

## Reproduction

From the repository root, using Python 3.12.11, uv 0.12.7, Z3 4.15.4.0,
OR-Tools 9.15.6755 and NetworkX 3.6.1, as locked in `uv.lock`:

```sh
uv sync --locked
uv run --locked python campaigns/acyclic-agreement-forest-feedback-vertex-set/work/check.py --self-test
uv run --locked python campaigns/acyclic-agreement-forest-feedback-vertex-set/work/check.py --candidate campaigns/acyclic-agreement-forest-feedback-vertex-set/work/algorithm.py
uv run --locked python campaigns/acyclic-agreement-forest-feedback-vertex-set/work/verify.py --candidate campaigns/acyclic-agreement-forest-feedback-vertex-set/work/algorithm.py
uv run --locked python campaigns/acyclic-agreement-forest-feedback-vertex-set/rounds/006/gadget_check.py
```

For the recorded scheduling, append `--shard I 8` to the candidate-check command
for each I from 0 through 7. Their record counts are 41 for shards 0–6 and 40
for shard 7. The unsharded command
checks the same family. No solver or process timeout is used.

## Coverage limits

All ordered tree pairs through four leaves are included; larger inputs are
sampled up to seven leaves. Most target optimum families exceed 128 outputs.
Thus finite evidence does not quantify over all inputs or target ties; that is
the obligation of `proof.md` and independent review. No optimum runtime, smallest
graph-size claim, or practical superiority over direct MAAF solvers follows.
The overhead comparison `../rounds/006/overhead.txt` is against the campaign's
Round 004 baseline on the same 327 inputs, with single-run timing measurements
of the earlier recursive implementation. `iterative-equivalence.txt` confirms
that all 327 explicit target graphs remain identical after the traversal repair;
the graph-size measurements apply unchanged, but those timings do not benchmark
the current implementation.
Independent review is pending.
